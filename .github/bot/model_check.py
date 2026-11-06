#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每月检查 DeepSeek 官方模型列表：flash 家族型号是否与 .github/bot/MODEL.txt 一致。

不一致 → 开 issue 提醒（只提醒，不自动改）。Stdlib only。
"""
import json
import os
import sys
import urllib.request

API = (os.environ.get("LLM_API_BASE") or "https://api.deepseek.com/v1").rstrip("/")
KEY = os.environ["DEEPSEEK_API_KEY"]
REPO = os.environ["GITHUB_REPOSITORY"]
TOKEN = os.environ["GITHUB_TOKEN"]

try:
    pinned = open(".github/bot/MODEL.txt", encoding="utf-8").read().strip()
except FileNotFoundError:
    pinned = ""

req = urllib.request.Request(API + "/models", headers={"Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req, timeout=30) as r:
    data = json.load(r)
ids = [m.get("id", "") for m in data.get("data", []) if "flash" in (m.get("id") or "").lower()]
print("flash ids:", ids)
if not ids:
    print("official list returned no flash models; nothing to do")
    sys.exit(0)

latest = "deepseek-flash" if "deepseek-flash" in ids else sorted(ids)[-1]
if pinned == latest:
    print("pinned model is current:", pinned)
    sys.exit(0)

body = (
    "每月模型检查：官方 flash 最新型号与仓库配置不一致。\n\n"
    "- 官方列表中的 flash 型号：%s\n"
    "- 当前配置：%s\n"
    "- 建议把 `.github/bot/MODEL.txt` 更新为：`%s`\n\n"
    "（由 model-check 工作流自动创建；更新后按三档纪律发 patch 版。）"
) % (", ".join(ids), pinned or "(空)", latest)

req2 = urllib.request.Request(
    "https://api.github.com/repos/%s/issues" % REPO,
    method="POST",
    headers={
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "dsh-model-check",
    },
)
payload = json.dumps({"title": "客服模型可更新：官方 flash 最新型号 " + latest, "body": body}).encode()
with urllib.request.urlopen(req2, payload, timeout=30) as r2:
    print("issue opened:", json.load(r2)["html_url"])
