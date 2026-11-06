#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每月检查（model-check 工作流）：两件事，只提醒不自动改。

1. DeepSeek 官方 /models：稳定别名（.github/bot/MODEL.txt）的底层版本是否与
   .github/bot/MODEL_NAME.txt 一致——稳定别名不变、底层换版也能发现；
   官方列表没有 flash 型号或别名消失 → 开 issue 报警并非零退出（不再绿色通过）。
2. iLang 官方 manifest（runtime.ilang.app）版本是否与 .github/bot/RUNTIME.txt 一致。

同类提醒只开一次（按 issue 标题查重）。Stdlib only。
"""
import json
import os
import sys
import urllib.request

API = (os.environ.get("LLM_API_BASE") or "https://api.deepseek.com/v1").rstrip("/")
KEY = os.environ["DEEPSEEK_API_KEY"]
REPO = os.environ["GITHUB_REPOSITORY"]
TOKEN = os.environ["GITHUB_TOKEN"]
MANIFEST_URL = "https://runtime.ilang.app/manifest.json"


def read(path, default=""):
    try:
        with open(path, encoding="utf-8") as f:
            v = f.read().strip()
        return v or default
    except FileNotFoundError:
        return default


def http(method, url, token, body=None):
    req = urllib.request.Request(
        url,
        method=method,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "dsh-model-check",
        },
    )
    data = json.dumps(body).encode() if body is not None else None
    with urllib.request.urlopen(req, data, timeout=30) as r:
        return json.load(r)


def open_issues(token):
    try:
        return http("GET", "https://api.github.com/repos/%s/issues?state=open&per_page=100" % REPO, token)
    except Exception:
        return []


def ensure_issue(token, title, body):
    if any((i.get("title") or "") == title for i in open_issues(token)):
        print("issue already open, skip:", title)
        return
    http("POST", "https://api.github.com/repos/%s/issues" % REPO, token, {"title": title, "body": body})
    print("issue opened:", title)


def main():
    pinned = read(".github/bot/MODEL.txt", "deepseek-flash")
    pinned_name = read(".github/bot/MODEL_NAME.txt", "")
    rc = 0

    # 1) DeepSeek 模型
    try:
        req = urllib.request.Request(API + "/models", headers={"Authorization": "Bearer " + KEY})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        models = data.get("data", [])
    except Exception as e:
        ensure_issue(TOKEN, "模型检查异常：官方 /models 接口调用失败",
                     "每月模型检查：调用 DeepSeek 官方 /models 失败。\n\n- 错误：%s\n请人工检查。"
                     "（本条由 model-check 工作流自动创建。）" % type(e).__name__)
        return 1

    flash_ids = [m.get("id", "") for m in models if "flash" in (m.get("id") or "").lower()]
    if not flash_ids:
        ensure_issue(TOKEN, "模型检查异常：官方列表里没有 flash 型号",
                     "每月模型检查：官方 /models 没有返回任何 flash 型号。\n\n"
                     "- 当前配置：%s\n可能原因：接口异常或官方下线了全部 flash 型号。\n"
                     "请人工检查 https://api.deepseek.com/v1/models 。"
                     "（本条由 model-check 工作流自动创建。）" % pinned)
        return 1

    entry = next((m for m in models if m.get("id") == pinned), None)
    if entry is None:
        ensure_issue(TOKEN, "客服模型可更新：官方列表里没有 %s" % pinned,
                     "每月模型检查：当前锁定的 %s 已不在官方 /models 列表。\n\n"
                     "- 官方 flash 型号：%s\n请人工决定替换或恢复。"
                     "（本条由 model-check 工作流自动创建。）" % (pinned, ", ".join(flash_ids)))
        return 1

    name = entry.get("name") or ""
    if not pinned_name:
        ensure_issue(TOKEN, "模型检查：%s 缺少底层版本记录" % pinned,
                     "每月模型检查：.github/bot/MODEL_NAME.txt 为空，无法比对底层版本。\n\n"
                     "- 官方当前显示名：%s\n建议把 MODEL_NAME.txt 更新为「%s」。"
                     "（本条由 model-check 工作流自动创建。）" % (name or "(空)", name or "待人工确认"))
        rc = 1
    elif name and name != pinned_name:
        ensure_issue(TOKEN, "客服模型可升级：%s 底层已更新" % pinned,
                     "每月模型检查：稳定别名 %s 的底层版本变了。\n\n"
                     "- 记录版本：%s\n- 官方当前版本：%s\n"
                     "- 上下文窗口：%s 输出上限：%s 输入模态：%s\n"
                     "建议人工确认后把 .github/bot/MODEL_NAME.txt 更新为「%s」，并按三档纪律发 patch 版。\n"
                     "（本条由 model-check 工作流自动创建。）"
                     % (pinned, pinned_name, name, entry.get("context_window", "?"),
                        entry.get("max_output_tokens", "?"), ", ".join(entry.get("input_modalities") or []),
                        name))
        rc = 1
    else:
        print("pinned model is current:", pinned, "name:", name)

    # 2) iLang 运行时 manifest
    try:
        req = urllib.request.Request(MANIFEST_URL, headers={"User-Agent": "dsh-model-check"})
        with urllib.request.urlopen(req, timeout=20) as r:
            manifest = json.load(r)
        live_version = manifest.get("version") or ""
        pinned_version = ""
        runtime_lines = read(".github/bot/RUNTIME.txt", "").splitlines()
        for line in runtime_lines:
            if line.startswith("version: "):
                pinned_version = line.split(": ", 1)[1].strip()
                break
        if live_version and pinned_version and live_version != pinned_version:
            ensure_issue(TOKEN, "iLang 运行时更新：manifest 版本 %s" % live_version,
                         "每月模型检查：iLang 官方运行时 manifest 版本与仓库记录不一致。\n\n"
                         "- 记录版本：%s\n- 官方当前版本：%s\n"
                         "- manifest：%s\n"
                         "建议人工确认后更新 .github/bot/RUNTIME.txt 的 version 与 sha256，并按三档纪律发 patch 版。\n"
                         "（本条由 model-check 工作流自动创建。）"
                         % (pinned_version, live_version, MANIFEST_URL))
            rc = 1
        else:
            print("iLang runtime manifest current:", live_version or "(未取得)")
    except Exception as e:
        ensure_issue(TOKEN, "模型检查异常：iLang manifest 获取失败",
                     "每月模型检查：获取 %s 失败。\n\n- 错误：%s\n请人工检查。"
                     "（本条由 model-check 工作流自动创建。）" % (MANIFEST_URL, type(e).__name__))
        rc = 1

    # 3) Gitee 镜像漂移：镜像 main 与 GitHub main 不同要有人知道
    try:
        req = urllib.request.Request(
            "https://gitee.com/api/v5/repos/monetize/DeepSeekHarness/branches/main",
            headers={"User-Agent": "dsh-model-check"})
        with urllib.request.urlopen(req, timeout=20) as r:
            gitee_main = (json.load(r).get("commit") or {}).get("sha") or ""
        req = urllib.request.Request(
            "https://api.github.com/repos/%s/branches/main" % REPO,
            headers={"User-Agent": "dsh-model-check"})
        with urllib.request.urlopen(req, timeout=20) as r:
            github_main = (json.load(r).get("commit") or {}).get("sha") or ""
        if github_main and gitee_main and gitee_main != github_main:
            ensure_issue(TOKEN, "镜像落后：Gitee main 在 %s" % gitee_main[:7],
                         "每月模型检查：Gitee 镜像与 GitHub 不一致。\n\n"
                         "- GitHub main：%s\n- Gitee main：%s\n"
                         "请把 https://gitee.com/monetize/DeepSeekHarness 同步到 GitHub 的 HEAD。\n"
                         "（本条由 model-check 工作流自动创建。）" % (github_main, gitee_main))
            rc = 1
        else:
            print("gitee mirror in sync:", gitee_main[:7] if gitee_main else "(未取得)")
    except Exception as e:
        ensure_issue(TOKEN, "模型检查异常：Gitee 镜像状态获取失败",
                     "每月模型检查：获取 Gitee 镜像状态失败。\n\n- 错误：%s\n请人工检查。"
                     "（本条由 model-check 工作流自动创建。）" % type(e).__name__)
        rc = 1

    return rc


if __name__ == "__main__":
    sys.exit(main())
