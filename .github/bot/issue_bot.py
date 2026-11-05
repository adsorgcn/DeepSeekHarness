#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DeepSeekHarness issue auto-reply bot. Stdlib only.

安全约定：
- 只回 issue（PR 跳过）、只在 open 状态回复；
- 自己的评论 / 已有 bot 回复 => 跳过（防循环）；
- 上下文只取仓库文档（README + 一键安装），顺序稳定；
- 人格规则：诚实、不知道就说不知道、指向一句话安装、不超过 300 字。
"""
import json
import os
import sys
import urllib.request

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]
EVENT = json.load(open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8"))
API = (os.environ.get("LLM_API_BASE") or "https://api.deepseek.com/v1").rstrip("/")
KEY = os.environ["DEEPSEEK_API_KEY"]
MODEL = os.environ.get("BOT_MODEL") or "deepseek-chat"
BOT_LOGIN = "github-actions[bot]"
MARK = "<!-- auto-bot -->"


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


issue = EVENT.get("issue") or {}
if issue.get("pull_request"):
    print("PR, skip")
    sys.exit(0)
if issue.get("state") != "open":
    print("not open, skip")
    sys.exit(0)
num = issue["number"]
action = EVENT.get("action")
if action == "issue_comment":
    comment = EVENT.get("comment") or {}
    if (comment.get("user") or {}).get("login") == BOT_LOGIN:
        print("own comment, skip")
        sys.exit(0)
    if MARK in (comment.get("body") or ""):
        print("bot comment, skip")
        sys.exit(0)
elif action != "opened":
    print("action %s, skip" % action)
    sys.exit(0)

comments = gh("GET", "https://api.github.com/repos/%s/issues/%d/comments?per_page=100" % (REPO, num))
for c in comments:
    if (c.get("user") or {}).get("login") == BOT_LOGIN or MARK in (c.get("body") or ""):
        print("already replied, skip")
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
    "语气：诚实、简洁、友好。回答控制在 300 字以内。\n\n"
    "仓库文档：\n" + context
)
user_msg = "用户提问（标题：%s）：\n%s" % (title, body[:2000])

payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": system},
        {"role": "user", "content": user_msg},
    ],
    "max_tokens": 600,
}
req = urllib.request.Request(
    API + "/chat/completions",
    method="POST",
    headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"},
)
with urllib.request.urlopen(req, json.dumps(payload).encode(), timeout=60) as r:
    out = json.load(r)
reply = (out["choices"][0]["message"]["content"] or "").strip()
reply = reply + "\n\n" + MARK + "\n> 本回复由仓库自动客服（AI）生成。有误请指出，紧急问题请 @维护者。"
gh("POST", "https://api.github.com/repos/%s/issues/%d/comments" % (REPO, num), {"body": reply})
print("replied", num)
