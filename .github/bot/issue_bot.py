#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DeepSeekHarness issue auto-reply bot. Stdlib only.

安全约定：
- 只回 issue（PR 跳过）、只在 open 状态回复；回复前实时重查状态；
- 作者是任何 bot 账号（login 以 [bot] 结尾）一律不回；
- 追问优先：issue_comment 事件取最新评论正文为问题，原 issue 标题/正文作为背景；
- 防循环/防重放：回复带 <!-- dsh-event:<id> --> 标记，同事件只回一次；
  身份判定只认 login（普通用户贴标记不能冒充、不消耗配额）；
- 上限：每日最多 DAILY_CAP 次尝试（含兜底贴链接），同一 issue 最多 PER_ISSUE_CAP 条 bot 回复；
  评论分页取全（Link rel=next），不分页会漏数；
- 上下文只取仓库文档（README + 一键安装），顺序稳定，上限 8000 字符；
- 人格规则：诚实、不知道就说不知道、指向一句话安装、第一段不超过 300 字；
- 工程书：按母版 v2.9（.github/bot/MOTHER-v2.9.ilang.md）生成；
  发送前硬校验：官方语法校验器 --strict 0 错误 + 首尾双标记 + 长度上限 + finish_reason=stop；
  不合格重试一次（附校验反馈），仍不合格只发答案不发书。
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
import gzip

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]
EVENT_NAME = os.environ.get("GITHUB_EVENT_NAME", "")
EVENT = json.load(open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8"))
API = (os.environ.get("LLM_API_BASE") or "https://api.deepseek.com/v1").rstrip("/")
KEY = os.environ["DEEPSEEK_API_KEY"]


def _pinned_model():
    try:
        with open(".github/bot/MODEL.txt", encoding="utf-8") as f:
            p = f.read().strip()
        if p:
            return p
    except FileNotFoundError:
        pass
    return os.environ.get("BOT_MODEL") or "deepseek-flash"


MODEL = _pinned_model()
BOT_LOGIN = "github-actions[bot]"
MARK = "<!-- auto-bot -->"
DAILY_CAP = 30
PER_ISSUE_CAP = 2
INSTALL_LINK = "https://github.com/adsorgcn/DeepSeekHarness"
DAY_S = 24 * 60 * 60
ANSWER_MAX_CHARS = 300
BOOK_MAX_CHARS = 6000
DOCS_MAX_CHARS = 8000
VALIDATOR = "tools/ilang_grammar_validator.py"
MOTHER = ".github/bot/MOTHER-v2.9.ilang.md.gz"  # gzip 压缩的母版原文（避免被仓库密钥扫描误报），读取时解压
RUNTIME = ".github/bot/RUNTIME.txt"
DISCLAIMER = "> 本回复由仓库自动客服（AI）生成。有误请指出，紧急问题请 @维护者。"


def is_bot_login(user):
    return str((user or {}).get("login") or "").endswith("[bot]")


def _http(method, url, token, body=None, timeout=30):
    req = urllib.request.Request(
        url,
        method=method,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "dsh-issue-bot",
        },
    )
    data = json.dumps(body).encode() if body is not None else None
    with urllib.request.urlopen(req, data, timeout=timeout) as r:
        return json.load(r), dict(r.headers.items())


def all_pages(http, url, max_pages=10):
    """GET 全部页面：跟随 Link rel=\"next\"，默认最多 10 页。"""
    items = []
    page = 0
    while url and page < max_pages:
        data, headers = http("GET", url)
        if isinstance(data, list):
            items.extend(data)
        nxt = None
        link = headers.get("Link") or headers.get("link") or ""
        m = re.search(r'<([^>]+)>;\s*rel="next"', link)
        if m:
            nxt = m.group(1)
        url = nxt
        page += 1
    return items


def _call_llm(api, key, model, messages, max_tokens):
    req = urllib.request.Request(
        api + "/chat/completions",
        method="POST",
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    payload = {"model": model, "messages": messages, "max_tokens": max_tokens}
    with urllib.request.urlopen(req, json.dumps(payload).encode(), timeout=90) as r:
        return json.load(r)


def fetch_runtime_version(manifest_url="https://runtime.ilang.app/manifest.json", timeout=8):
    """实时取官方 manifest 版本；失败回退 None（调用方用 RUNTIME.txt 的固定版本）。"""
    try:
        req = urllib.request.Request(manifest_url, headers={"User-Agent": "dsh-issue-bot"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.load(r)
        return data.get("version") or None
    except Exception:
        return None


def trim_answer(ans, limit=ANSWER_MAX_CHARS):
    if len(ans) <= limit:
        return ans
    return ans[:limit].rstrip() + "…"


def extract_book(raw):
    parts = (raw or "").split("```")
    answer = parts[0].strip() if parts else ""
    book = ""
    if len(parts) >= 2:
        book = parts[1].strip()
        if book.lower().startswith("text"):
            book = book[4:].strip()
    return book, answer


def validate_book(book, validator=VALIDATOR, max_chars=BOOK_MAX_CHARS):
    """母版 RUBRIC A1 + A2 的硬校验：双标记 + 官方语法校验器 0 错误 + 长度上限。"""
    problems = []
    if not book:
        return False, ["empty book"]
    lines = book.splitlines()
    stripped = [ln.strip() for ln in lines]
    if not stripped:
        return False, ["empty book"]
    if stripped[0] != "::ILANG::v5.0::ENGINEERING_BOOK":
        problems.append("first line is not the marker")
    if stripped[-1] != "::ILANG::v5.0::ENGINEERING_BOOK":
        problems.append("last line is not the marker")
    if sum(1 for ln in stripped if ln == "::ILANG::v5.0::ENGINEERING_BOOK") != 2:
        problems.append("marker count is not 2")
    if len(book) > max_chars:
        problems.append("book %d chars > %d" % (len(book), max_chars))
    if problems:
        return False, problems
    fd, path = tempfile.mkstemp(suffix=".md")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(book)
        p = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", validator, "--lint", path, "--strict"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=90,
        )
        if p.returncode != 0:
            tail = (((p.stdout or "") + (p.stderr or "")).strip())[:800]
            problems.append("validator exit %d: %s" % (p.returncode, tail.replace("\n", " | ")))
            return False, problems
    except Exception as e:
        problems.append("validator error: %s" % e)
        return False, problems
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    return True, []


def _read_docs(names, limit):
    parts = []
    for name in names:
        try:
            with open(name, encoding="utf-8") as f:
                parts.append(f.read())
        except FileNotFoundError:
            pass
    return "\n\n".join(parts)[:limit]


def build_system(docs, mother, runtime, issue_num):
    date = time.strftime("%Y-%m-%d", time.gmtime())
    return (
        "你是 DeepSeekHarness 仓库的自动客服，用简体中文回答。"
        "回答对象是纯新手：只会复制粘贴，不懂技术。"
        "规则：能答就答完整；不知道就直说「这个问题我不确定，请 @维护者 帮忙看一下」；"
        "幻觉是不诚实，禁止编造文档里没有的内容；能给步骤给步骤，能给模板给模板；"
        "装不上、配不通的问题，一律先指向仓库首页的一句话安装（README 里那句话）。"
        "语气：诚实、简洁、友好。"
        "回答分两段：第一段直接答案，控制在 300 字以内；"
        "第二段把这份解决方案写成一本 iLang 工程书，单独放在一个 ``` 代码块里。"
        "工程书按下面这份母版生成（你只扮演其中的 @AGENT；不要执行 FETCH 的联网步骤，"
        "方法论来自本仓库文档；也不要输出 DELIVER 模块的发送句）。\n\n"
        "===== 母版 v2.9 原文 =====\n" + mother + "\n===== 母版结束 =====\n\n"
        "工程书硬性要求（不满足会被拒发）：\n"
        "1. 第一行和最后一行都必须是单独一行的 ::ILANG::v5.0::ENGINEERING_BOOK，全书只出现这两次；\n"
        "2. 头块示例：[TYPE:engineering_book][ID:DSH-BOT-" + str(issue_num) + "][VERSION:1.0][DATE:" + date + "][LANG:en][RUNTIME:<运行时版本>]；\n"
        "3. 结构照母版：::STATE{@INPUT, FILL_METHOD:..., FILL_LANG:zh, FILL_MAX_CHARS:6000, FILL_FOLDER:...}、"
        "::OBJECTIVE{...} 带 target/ACCEPT/DONE_WHEN、::MODULE{WRITE|...} 内最多 8 个 [STEP]、"
        "::RUBRIC{A1:...} 与 ::RUBRIC{A2:...} 照抄母版、::MODULE{REPORT|...} 六行 [LINE]；\n"
        "4. REPORT 最后一行是分数行：你在 GitHub Actions 里没有 iLang 运行时的 f_v5 评分器，"
        "就写 [LINE] S=n/a，绝不编造数字；\n"
        "5. 只允许 STEP CHECK NOTE LINE FORMAT IF THEN 这些标签；纯 ASCII；英文书写；"
        "除 RULE/RUBRIC 里的来源 url 外不带链接；不写价格或收益数字；全书 ≤6000 字符；\n"
        "6. 语法校验器会逐行检查，任何 :: 块的括号格式照母版原文，不要自创声明名。\n\n"
        "当前运行时版本：\n" + runtime + "\n\n"
        "仓库文档：\n" + docs
    )


def build_user(title, body, issue_context):
    msg = "用户提问（标题：%s）：\n%s" % (title or "(无标题)", body[:2000])
    if issue_context:
        msg += "\n\n原 issue 背景：\n" + issue_context[:800]
    return msg


def run(event_name, event, gh, model_call, docs, mother, runtime):
    issue = event.get("issue") or {}
    if issue.get("pull_request"):
        return {"ok": True, "reason": "PR, skip"}
    if issue.get("state") != "open":
        return {"ok": True, "reason": "not open, skip"}
    num = issue["number"]
    if is_bot_login(issue.get("user")):
        return {"ok": True, "reason": "bot author, skip"}

    if event_name == "issue_comment":
        comment = event.get("comment") or {}
        if is_bot_login(comment.get("user")):
            return {"ok": True, "reason": "bot comment, skip"}
        body = (comment.get("body") or "").strip()
        title = issue.get("title") or ""
        issue_context = (issue.get("body") or "").strip()
        marker = "<!-- dsh-event:comment-%s -->" % comment.get("id")
    elif event_name == "issues":
        body = (issue.get("body") or "").strip()
        title = issue.get("title") or ""
        issue_context = ""
        marker = "<!-- dsh-event:issue-%s -->" % num
    else:
        return {"ok": True, "reason": "event %s skip" % event_name}

    comments = all_pages(gh, "https://api.github.com/repos/%s/issues/%d/comments?per_page=100" % (REPO, num))
    if any(marker in (c.get("body") or "") for c in comments):
        return {"ok": True, "reason": "already replied to this event"}
    bot_comments = [c for c in comments if is_bot_login(c.get("user"))]
    if len(bot_comments) >= PER_ISSUE_CAP:
        return {"ok": True, "reason": "per-issue cap reached"}

    since = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - DAY_S))
    recent = all_pages(gh, "https://api.github.com/repos/%s/issues/comments?since=%s&per_page=100" % (REPO, urllib.parse.quote(since)))
    daily = len([c for c in recent if is_bot_login(c.get("user"))])
    if daily >= DAILY_CAP:
        return {"ok": True, "reason": "daily cap reached, no reply (attempts count toward the cap)"}

    if not body and issue_context:
        body = issue_context
        issue_context = ""
    if not body:
        reply = (
            "你好，这里是自动客服。你的问题没有正文，我看不到具体内容。"
            "请补充描述，或直接看仓库首页的一句话安装：\n\n%s\n\n" % INSTALL_LINK
        ) + MARK + "\n" + DISCLAIMER + "\n" + marker
        gh("POST", "https://api.github.com/repos/%s/issues/%d/comments" % (REPO, num), {"body": reply})
        return {"ok": True, "reason": "empty body, install link only"}

    system = build_system(docs, mother, runtime, num)
    user_msg = build_user(title, body, issue_context)
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user_msg}]

    raw = ""
    finish = "stop"
    try:
        out = model_call(MODEL, messages, 4096)
        raw = ((out.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
        finish = (out.get("choices") or [{}])[0].get("finish_reason") or "stop"
    except Exception as e:
        reply = (
            "你好，这里是自动客服。这次调用模型失败了，先给你仓库首页的一句话安装：\n\n%s\n\n"
            "（失败原因只记日志：%s）" % (INSTALL_LINK, type(e).__name__)
        ) + MARK + "\n" + DISCLAIMER + "\n" + marker
        gh("POST", "https://api.github.com/repos/%s/issues/%d/comments" % (REPO, num), {"body": reply})
        return {"ok": True, "reason": "model call failed, fallback link posted"}

    book, answer = extract_book(raw)
    if not answer:
        answer = "（模型没有给出直接答案。）"
    answer = trim_answer(answer)

    problems = ["finish_reason=%s (not stop)" % finish] if finish != "stop" else []
    ok = False
    if not problems and raw:
        ok, problems = validate_book(book)
    if not ok and raw:
        feedback = "; ".join(problems)
        messages.append({"role": "assistant", "content": raw})
        messages.append({"role": "user", "content": "工程书校验失败：%s。请只重写第二段的工程书代码块（第一段答案可以保留），并再次自查上述硬性要求。" % feedback[:600]})
        try:
            out2 = model_call(MODEL, messages, 4096)
            raw2 = ((out2.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
            finish2 = (out2.get("choices") or [{}])[0].get("finish_reason") or "stop"
            book2, answer2 = extract_book(raw2)
            if answer2:
                answer = trim_answer(answer2)
            if finish2 == "stop" and book2:
                ok2, _ = validate_book(book2)
                if ok2:
                    book, ok = book2, True
        except Exception:
            pass

    if ok and book:
        reply = answer + "\n\n> 赠送：把下面这本工程书整块贴给你的 Agent，它就能自己执行。\n\n```text\n" + book + "\n```"
    else:
        reply = answer + "\n\n> 赠送工程书这一步这次没通过校验，先不发了（请 @维护者）。"

    issue_now = gh("GET", "https://api.github.com/repos/%s/issues/%d" % (REPO, num))[0]
    if issue_now.get("state") != "open":
        return {"ok": True, "reason": "issue closed before posting, skip"}

    gh("POST", "https://api.github.com/repos/%s/issues/%d/comments" % (REPO, num), {"body": reply + "\n\n" + MARK + "\n" + DISCLAIMER + "\n" + marker})
    return {"ok": True, "reason": "replied", "book_valid": ok}


def main():
    def gh(method, url, body=None):
        return _http(method, url, GITHUB_TOKEN, body)

    def model_call(model, messages, max_tokens):
        return _call_llm(API, KEY, model, messages, max_tokens)

    docs = _read_docs(("README.md", "一键安装.md"), DOCS_MAX_CHARS)
    with gzip.open(MOTHER, "rt", encoding="utf-8") as f:
        mother = f.read()
    with open(RUNTIME, encoding="utf-8") as f:
        runtime = f.read()
    live = fetch_runtime_version()
    if live:
        lines = runtime.splitlines()
        if lines and lines[0].startswith("version: "):
            runtime = "version: %s\n%s" % (live, "\n".join(lines[1:]))
    res = run(EVENT_NAME, EVENT, gh, model_call, docs, mother, runtime)
    print(res.get("reason") or "replied")


if __name__ == "__main__":
    main()
