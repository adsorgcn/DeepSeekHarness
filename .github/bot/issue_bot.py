#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DeepSeekHarness issue auto-reply bot. Stdlib only.

安全约定：
- 只回 issue（PR 跳过）、只在 open 状态回复；
- 作者是任何 bot 账号（login 以 [bot] 结尾）一律不回；
- 自己的评论 / 已有 bot 回复 => 跳过（防循环）；
- 上限：每日最多 DAILY_CAP 条回复（超出只贴一键安装链接，不调模型）；
  同一 issue 最多 PER_ISSUE_CAP 条 bot 回复；
- 上下文只取仓库文档（README + 一键安装），顺序稳定；
- 人格规则：诚实、不知道就说不知道、指向一句话安装、不超过 300 字。
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

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


def gh(method, url, body=None):
    req = urllib.request.Request(
        url,
        method=method,
        headers={
            "Authorization": "Bearer " + GITHUB_TOKEN,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "dsh-issue-bot",
        },
    )
    data = json.dumps(body).encode() if body is not None else None
    with urllib.request.urlopen(req, data, timeout=30) as r:
        return json.load(r)


def is_bot_login(user):
    return str((user or {}).get("login") or "").endswith("[bot]")


issue = EVENT.get("issue") or {}
if issue.get("pull_request"):
    print("PR, skip")
    sys.exit(0)
if issue.get("state") != "open":
    print("not open, skip")
    sys.exit(0)
num = issue["number"]
action = EVENT.get("action")

if is_bot_login(issue.get("user")):
    print("bot author, skip")
    sys.exit(0)

if EVENT_NAME == "issue_comment":
    if action != "created":
        print("comment action %s, skip" % action)
        sys.exit(0)
    comment = EVENT.get("comment") or {}
    if is_bot_login(comment.get("user")) or MARK in (comment.get("body") or ""):
        print("bot comment, skip")
        sys.exit(0)
elif EVENT_NAME == "issues" and action == "opened":
    pass
else:
    print("event %s action %s, skip" % (EVENT_NAME, action))
    sys.exit(0)

comments = gh("GET", "https://api.github.com/repos/%s/issues/%d/comments?per_page=100" % (REPO, num))
already = [c for c in comments if (c.get("user") or {}).get("login") == BOT_LOGIN or MARK in (c.get("body") or "")]
if len(already) >= PER_ISSUE_CAP:
    print("per-issue cap reached, skip")
    sys.exit(0)

# Daily cap: count bot replies across the repo in the last 24 hours.
since = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - DAY_S))
url = "https://api.github.com/repos/%s/issues/comments?since=%s&per_page=100" % (REPO, urllib.parse.quote(since))
recent = gh("GET", url)
daily = len([c for c in recent if (c.get("user") or {}).get("login") == BOT_LOGIN or MARK in (c.get("body") or "")])
if daily >= DAILY_CAP:
    msg = (
        "你好，这里是自动客服。今天的自动回复额度已用完，请先看仓库首页的一句话安装：\n\n"
        "%s\n\n" % INSTALL_LINK
    ) + MARK + "\n> 本回复由仓库自动客服（AI）生成。有误请指出，紧急问题请 @维护者。"
    gh("POST", "https://api.github.com/repos/%s/issues/%d/comments" % (REPO, num), {"body": msg})
    print("daily cap reached, posted install link only")
    sys.exit(0)

ctx_parts = []
for name in ("README.md", "一键安装.md"):
    try:
        ctx_parts.append(open(name, encoding="utf-8").read())
    except FileNotFoundError:
        pass
context = "\n\n".join(ctx_parts)[:8000]

title = issue.get("title") or ""
body = ((issue.get("body") or "").strip()) or ((EVENT.get("comment") or {}).get("body") or "").strip()

system = (
    "你是 DeepSeekHarness 仓库的自动客服，用简体中文回答。"
    "回答对象是纯新手：只会复制粘贴，不懂技术。"
    "规则：能答就答完整；不知道就直说「这个问题我不确定，请 @维护者 帮忙看一下」；"
    "幻觉是不诚实，禁止编造文档里没有的内容；能给步骤给步骤，能给模板给模板；"
    "装不上、配不通的问题，一律先指向仓库首页的一句话安装（README 里那句话）。"
    "语气：诚实、简洁、友好。"
    "回答分两段：第一段直接答案，控制在 300 字以内；"
    "第二段把这份解决方案写成一本 iLang 工程书，单独放在一个 ``` 代码块里，"
    "工程书遵循母版格式：以 ::ILANG::v5.0 开头，含 [TYPE:engineering_book] 与 [ID]、"
    "::OBJECTIVE、若干 ::RULE 步骤、::RUBRIC 验收、一行操作流水线、"
    "署名行「来源：DeepSeekHarness · iLang IML v5.0」。"
    "工程书是给用户回填自己的 Agent 用的：用户整块复制粘贴即可执行；"
    "若问题只是操作指引，工程书就写操作清单与验收项。\n\n"
    "仓库文档：\n" + context
)
user_msg = "用户提问（标题：%s）：\n%s" % (title, body[:2000])

payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": system},
        {"role": "user", "content": user_msg},
    ],
    "max_tokens": 1600,
}
req = urllib.request.Request(
    API + "/chat/completions",
    method="POST",
    headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"},
)
with urllib.request.urlopen(req, json.dumps(payload).encode(), timeout=60) as r:
    out = json.load(r)
raw = (out["choices"][0]["message"]["content"] or "").strip()
parts = raw.split("```")
answer = parts[0].strip()
book = ""
if len(parts) >= 2:
    book = parts[1].strip()
    if book.lower().startswith("text"):
        book = book[4:].strip()
if book:
    reply = answer + "\n\n> 赠送：把下面这本工程书整块贴给你的 Agent，它就能自己执行。\n\n```text\n" + book + "\n```"
else:
    reply = answer
reply = reply + "\n\n" + MARK + "\n> 本回复由仓库自动客服（AI）生成。有误请指出，紧急问题请 @维护者。"
gh("POST", "https://api.github.com/repos/%s/issues/%d/comments" % (REPO, num), {"body": reply})
print("replied", num)
