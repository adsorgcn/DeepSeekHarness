# -*- coding: utf-8 -*-
"""DeepSeekHarness 客服 bot 行为测试（纯标准库、全 mock、零网络、零外部写入）。

覆盖：PR/关闭/bot 作者跳过；追问优先；事件去重；每 issue 与每日配额（含分页）；
空正文兜底；模型异常兜底；答案截断；工程书硬校验（调用随仓库发布的官方语法校验器）；
finish_reason=length 拒发；发布前实时重查关闭；伪造标记不消耗配额。

用法: python -X utf8 tools/test_bot.py （工作目录=仓库根）
"""
import importlib.util
import gzip
import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_bot():
    os.environ.setdefault("GITHUB_TOKEN", "test-token")
    os.environ.setdefault("GITHUB_REPOSITORY", "adsorgcn/DeepSeekHarness")
    os.environ["DEEPSEEK_API_KEY"] = "test-key"
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump({}, f)
    os.environ["GITHUB_EVENT_PATH"] = path
    spec = importlib.util.spec_from_file_location(
        "issue_bot", os.path.join(ROOT, ".github", "bot", "issue_bot.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


BOT = load_bot()

VALID_BOOK = """::ILANG::v5.0::ENGINEERING_BOOK
[TYPE:engineering_book]
[ID:DSH-BOT-TEST]
[VERSION:1.0]
[DATE:2026-11-05]
[LANG:en]
[RUNTIME:2026.11.05-e45fd039752f]
::STATE{@INPUT, FILL_METHOD:the user question text, FILL_LANG:zh, FILL_MAX_CHARS:6000, FILL_FOLDER:current}
::OBJECTIVE{id:b1|owner:user|trust:trusted|version:1|status:active}
  target: FILL_METHOD becomes one English iLang engineering book the user can paste
  ACCEPT: every item of RUBRIC passes
  DONE_WHEN: the book was sent as DELIVER says
::MODULE{WRITE|title:write the book}
  [STEP] 1 read FILL_METHOD
  [STEP] 2 write the promised outcome into OBJECTIVE target
  [STEP] 3 write every constant the user must supply as a FILL_ field
  [STEP] 4 write the actions as STEP lines in HOW at most eight
  [STEP] 5 write acceptance as RUBRIC items
  [STEP] 6 copy the shape plus HOW and a six line REPORT
  [STEP] 7 check the markers and the grammar
  [STEP] 8 fix errors and run again
::RUBRIC{A1: the book opens and closes with the marker|check:count|path:BOOK.md|regex:"(?m)^::ILANG::v5\\.0::ENGINEERING_BOOK$"|expect:2}
::RUBRIC{A2: the grammar validator reports zero errors|check:cmd|run:"python ilang_grammar_validator.py --lint BOOK.md --strict"|expect:0}
::MODULE{REPORT|title:evidence}
  [LINE] what the agent did
  [LINE] evidence found
  [LINE] unverified items
  [LINE] next step
  [LINE] source attribution
  [LINE] S=n/a
::ILANG::v5.0::ENGINEERING_BOOK
"""

GOOD_RAW = "答案：请先看仓库首页的一句话安装。\n\n```\n" + VALID_BOOK + "\n```"

BAD_RAW = "答案：请先看仓库首页的一句话安装。\n\n```\n这不是工程书 ::WRONG\n```"


class FakeGH:
    def __init__(self):
        self.requests = []          # (method, url, body)
        self.responses = {}         # url 子串 -> callable 或 (data, headers) 队列

    def __call__(self, method, url, body=None):
        self.requests.append((method, url, body))
        for key, fn in self.responses.items():
            if key in url:
                if callable(fn):
                    return fn(method, url, body)
                if isinstance(fn, list) and fn:
                    return fn.pop(0)
                return ([], {})
        return ([], {})

    def posts(self):
        return [r for r in self.requests if r[0] == "POST"]


class FakeModel:
    def __init__(self, outputs):
        self.outputs = list(outputs)
        self.calls = []

    def __call__(self, model, messages, max_tokens):
        self.calls.append({"model": model, "messages": messages, "max_tokens": max_tokens})
        if not self.outputs:
            raise RuntimeError("no more outputs")
        return self.outputs.pop(0)


def model_resp(content, finish="stop"):
    return {"choices": [{"message": {"content": content}, "finish_reason": finish}]}


def human_user(login="some-user"):
    return {"login": login}


def bot_user():
    return {"login": "github-actions[bot]"}


def issue_event(num=1, state="open", body="问题正文", title="标题"):
    return {"issue": {"number": num, "state": state, "body": body, "title": title, "user": human_user()}}


def comment_event(num=1, cid=999, body="追问正文", issue_body="原 issue 背景", state="open"):
    ev = issue_event(num=num, state=state, body=issue_body, title="标题")
    ev["comment"] = {"id": cid, "body": body, "user": human_user()}
    return ev


DOCS = "README 一句话安装。\n"
MOTHER = gzip.open(os.path.join(ROOT, ".github", "bot", "MOTHER-v2.9.ilang.md.gz"), "rt", encoding="utf-8").read()
RUNTIME = open(os.path.join(ROOT, ".github", "bot", "RUNTIME.txt"), encoding="utf-8").read()

RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print("[%s] %s %s" % (name, "PASS" if cond else "FAIL", detail))


def scenario_pr_skip():
    gh = FakeGH()
    ev = issue_event()
    ev["issue"]["pull_request"] = {"url": "x"}
    res = BOT.run("issues", ev, gh, FakeModel([]), DOCS, MOTHER, RUNTIME)
    check("pr_skip", res["reason"] == "PR, skip", res["reason"])


def scenario_closed_snapshot():
    gh = FakeGH()
    res = BOT.run("issues", issue_event(state="closed"), gh, FakeModel([]), DOCS, MOTHER, RUNTIME)
    check("closed_snapshot_skip", res["reason"] == "not open, skip", res["reason"])


def scenario_bot_author():
    gh = FakeGH()
    ev = issue_event()
    ev["issue"]["user"] = bot_user()
    res = BOT.run("issues", ev, gh, FakeModel([]), DOCS, MOTHER, RUNTIME)
    check("bot_author_skip", res["reason"] == "bot author, skip", res["reason"])


def scenario_bot_comment():
    gh = FakeGH()
    ev = comment_event()
    ev["comment"]["user"] = bot_user()
    res = BOT.run("issue_comment", ev, gh, FakeModel([]), DOCS, MOTHER, RUNTIME)
    check("bot_comment_skip", res["reason"] == "bot comment, skip", res["reason"])


def scenario_event_dedup():
    gh = FakeGH()
    gh.responses["/comments?per_page=100"] = [
        ([{"id": 1, "body": "旧回复 <!-- dsh-event:comment-999 -->", "user": bot_user()}], {})
    ]
    res = BOT.run("issue_comment", comment_event(), gh, FakeModel([]), DOCS, MOTHER, RUNTIME)
    check("event_dedup", res["reason"] == "already replied to this event", res["reason"])


def scenario_per_issue_cap_page2():
    gh = FakeGH()

    def pages(method, url, body):
        if "page=2" in url:
            return ([{"id": 2, "body": "y", "user": bot_user()},
                     {"id": 3, "body": "z", "user": bot_user()}], {})
        return ([{"id": 1, "body": "x", "user": human_user()}],
                {"Link": '<https://api.github.com/repos/a/b/issues/1/comments?page=2&per_page=100>; rel="next"'})

    gh.responses["/comments"] = pages
    res = BOT.run("issue_comment", comment_event(), gh, FakeModel([]), DOCS, MOTHER, RUNTIME)
    check("per_issue_cap_via_pagination", res["reason"] == "per-issue cap reached", res["reason"])


def scenario_daily_cap():
    gh = FakeGH()
    gh.responses["/comments?per_page=100"] = [([], {})]
    gh.responses["issues/comments?since="] = [
        ([{"id": i, "body": "x", "user": bot_user()} for i in range(30)], {})
    ]
    res = BOT.run("issues", issue_event(), gh, FakeModel([]), DOCS, MOTHER, RUNTIME)
    check("daily_cap_no_post", res["reason"].startswith("daily cap") and not gh.posts(), res["reason"])


def scenario_followup_priority():
    gh = FakeGH()
    gh.responses["/comments?per_page=100"] = [([], {})]
    gh.responses["issues/comments?since="] = [([], {})]
    gh.responses["/issues/1"] = [({"number": 1, "state": "open"}, {})]
    model = FakeModel([model_resp(GOOD_RAW)])
    res = BOT.run("issue_comment", comment_event(), gh, model, DOCS, MOTHER, RUNTIME)
    posted = [p for p in gh.posts() if "/comments" in p[1]]
    user_msg = model.calls[0]["messages"][1]["content"]
    ok = (res["reason"] == "replied" and len(posted) == 1
          and user_msg.startswith("用户提问（标题：标题）：\n追问正文")
          and "原 issue 背景：\n原 issue 背景" in user_msg
          and "dsh-event:comment-999" in posted[0][2]["body"]
          and res.get("book_valid") is True and len(model.calls) == 1)
    check("followup_priority_and_valid_book", ok, res["reason"])


def scenario_invalid_book_no_ship():
    gh = FakeGH()
    gh.responses["/comments?per_page=100"] = [([], {})]
    gh.responses["issues/comments?since="] = [([], {})]
    gh.responses["/issues/1"] = [({"number": 1, "state": "open"}, {})]
    model = FakeModel([model_resp(BAD_RAW), model_resp(BAD_RAW)])
    res = BOT.run("issues", issue_event(), gh, model, DOCS, MOTHER, RUNTIME)
    posted = [p for p in gh.posts() if "/comments" in p[1]]
    ok = (len(posted) == 1 and "没通过校验" in posted[0][2]["body"]
          and "```text" not in posted[0][2]["body"] and len(model.calls) == 2)
    check("invalid_book_not_shipped", ok, res["reason"])


def scenario_finish_length():
    gh = FakeGH()
    gh.responses["/comments?per_page=100"] = [([], {})]
    gh.responses["issues/comments?since="] = [([], {})]
    gh.responses["/issues/1"] = [({"number": 1, "state": "open"}, {})]
    model = FakeModel([model_resp(GOOD_RAW, finish="length"), model_resp(GOOD_RAW, finish="length")])
    res = BOT.run("issues", issue_event(), gh, model, DOCS, MOTHER, RUNTIME)
    posted = [p for p in gh.posts() if "/comments" in p[1]]
    check("finish_length_no_book", len(posted) == 1 and "```text" not in posted[0][2]["body"], res["reason"])


def scenario_empty_body_fallback():
    gh = FakeGH()
    gh.responses["/comments?per_page=100"] = [([], {})]
    gh.responses["issues/comments?since="] = [([], {})]
    model = FakeModel([])
    ev = issue_event(body="")
    res = BOT.run("issues", ev, gh, model, DOCS, MOTHER, RUNTIME)
    posted = [p for p in gh.posts() if "/comments" in p[1]]
    ok = (len(posted) == 1 and "一句话安装" in posted[0][2]["body"] and not model.calls)
    check("empty_body_install_link", ok, res["reason"])


def scenario_model_exception_fallback():
    gh = FakeGH()
    gh.responses["/comments?per_page=100"] = [([], {})]
    gh.responses["issues/comments?since="] = [([], {})]
    gh.responses["/issues/1"] = [({"number": 1, "state": "open"}, {})]

    def boom(model, messages, max_tokens):
        raise RuntimeError("api down")

    res = BOT.run("issues", issue_event(), gh, boom, DOCS, MOTHER, RUNTIME)
    posted = [p for p in gh.posts() if "/comments" in p[1]]
    ok = (len(posted) == 1 and "一句话安装" in posted[0][2]["body"]
          and "RuntimeError" in posted[0][2]["body"])
    check("model_exception_fallback", ok, res["reason"])


def scenario_long_answer_truncated():
    gh = FakeGH()
    gh.responses["/comments?per_page=100"] = [([], {})]
    gh.responses["issues/comments?since="] = [([], {})]
    gh.responses["/issues/1"] = [({"number": 1, "state": "open"}, {})]
    long_ans = "答" * 500
    model = FakeModel([model_resp(long_ans + "\n\n```\n" + VALID_BOOK + "\n```")])
    res = BOT.run("issues", issue_event(), gh, model, DOCS, MOTHER, RUNTIME)
    posted = [p for p in gh.posts() if "/comments" in p[1]]
    first_line = posted[0][2]["body"].split("\n")[0]
    check("long_answer_truncated",
          len(first_line) <= BOT.ANSWER_MAX_CHARS + 1 and first_line.endswith("…"),
          "len=%d" % len(first_line))


def scenario_live_closed_no_post():
    gh = FakeGH()
    gh.responses["/comments?per_page=100"] = [([], {})]
    gh.responses["issues/comments?since="] = [([], {})]
    gh.responses["/issues/1"] = [({"number": 1, "state": "closed"}, {})]
    model = FakeModel([model_resp(GOOD_RAW)])
    res = BOT.run("issues", issue_event(), gh, model, DOCS, MOTHER, RUNTIME)
    posted = [p for p in gh.posts() if "/comments" in p[1]]
    check("live_closed_skip", res["reason"] == "issue closed before posting, skip" and not posted, res["reason"])


def scenario_valid_book_happy_path():
    gh = FakeGH()
    gh.responses["/comments?per_page=100"] = [([], {})]
    gh.responses["issues/comments?since="] = [([], {})]
    gh.responses["/issues/1"] = [({"number": 1, "state": "open"}, {})]
    model = FakeModel([model_resp(GOOD_RAW)])
    res = BOT.run("issues", issue_event(), gh, model, DOCS, MOTHER, RUNTIME)
    posted = [p for p in gh.posts() if "/comments" in p[1]]
    body = posted[0][2]["body"]
    ok = (res.get("book_valid") is True and "```text" in body
          and body.count("::ILANG::v5.0::ENGINEERING_BOOK") == 2
          and "dsh-event:issue-1" in body)
    check("valid_book_happy_path", ok, res["reason"])


def scenario_forged_marker_ignored():
    gh = FakeGH()
    gh.responses["/comments?per_page=100"] = [
        ([{"id": 1, "body": "<!-- auto-bot --> 我冒充", "user": human_user()}], {})
    ]
    gh.responses["issues/comments?since="] = [([], {})]
    gh.responses["/issues/1"] = [({"number": 1, "state": "open"}, {})]
    model = FakeModel([model_resp(GOOD_RAW)])
    res = BOT.run("issues", issue_event(), gh, model, DOCS, MOTHER, RUNTIME)
    posted = [p for p in gh.posts() if "/comments" in p[1]]
    check("forged_marker_ignored", res["reason"] == "replied" and len(posted) == 1, res["reason"])


def main():
    os.chdir(ROOT)
    scenario_pr_skip()
    scenario_closed_snapshot()
    scenario_bot_author()
    scenario_bot_comment()
    scenario_event_dedup()
    scenario_per_issue_cap_page2()
    scenario_daily_cap()
    scenario_followup_priority()
    scenario_invalid_book_no_ship()
    scenario_finish_length()
    scenario_empty_body_fallback()
    scenario_model_exception_fallback()
    scenario_long_answer_truncated()
    scenario_live_closed_no_post()
    scenario_valid_book_happy_path()
    scenario_forged_marker_ignored()
    failed = [n for n, ok, _ in RESULTS if not ok]
    print("-" * 60)
    print("SUMMARY:", "ALL PASS (%d scenarios)" % len(RESULTS) if not failed else ("FAIL: " + ", ".join(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
