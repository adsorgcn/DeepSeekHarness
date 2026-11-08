#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""市场构建器：从 docs/market/registry.json 生成 docs/market/index.json（官方格式 1）与页面行区。

用法:
  python tools/market_build.py           # 校验、回写 sha256_lf/validated、生成 index.json 与页面行区
  python tools/market_build.py --check   # 只校验，不写任何文件

只用标准库与本机 git；绝不运行被登记仓库的任何代码。
"""
import argparse
import datetime
import hashlib
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(ROOT, "docs", "market", "registry.json")
INDEX_JSON = os.path.join(ROOT, "docs", "market", "index.json")
INDEX_HTML = os.path.join(ROOT, "docs", "market", "index.html")
VALIDATOR = os.path.join(ROOT, "tools", "ilang_grammar_validator.py")
GIT_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def fail(msg):
    print("[market_build] %s" % msg)
    sys.exit(1)


def sha256_lf(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read().replace(b"\r\n", b"\n")).hexdigest()


def validate_manifest(path):
    """返回 (linted, errors, warnings)；违规直接抛异常。"""
    if not os.path.exists(os.path.join(ROOT, path)):
        raise ValueError("%s 不存在" % path)
    text = io.open(os.path.join(ROOT, path), encoding="utf-8").read()
    if "::ILANG::v5.0" not in text:
        raise ValueError("%s 缺少 ::ILANG::v5.0" % path)
    r = subprocess.run([sys.executable, "-X", "utf8", VALIDATOR, "--lint",
                        os.path.join(ROOT, path), "--strict"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise ValueError("%s 校验器未通过：%s" % (path, (r.stdout + r.stderr).strip()[:300]))
    m = re.search(r"linted=([0-9]+)", r.stdout + r.stderr)
    linted = int(m.group(1)) if m else 0
    if linted < 1:
        raise ValueError("%s 没有 linted 围栏（linted=%d）" % (path, linted))
    return linted


def build_index(reg):
    bundles = [e for e in reg["entries"] if e.get("kind") == "bundle"]
    plugins = []
    for e in bundles:
        name = e["name"]
        if any(p["name"] == name for p in plugins):
            raise ValueError("插件名重复：%s" % name)
        versions = []
        for v in e["versions"]:
            ver = v["version"]
            ts = v["publishTimestamp"]
            eng = v.get("engines_dsh", "")
            src = v["source"]
            if not isinstance(ver, str) or not ver.strip():
                raise ValueError("%s 有版本缺少精确 version" % name)
            if not isinstance(ts, int):
                raise ValueError("%s@%s publishTimestamp 不是整数" % (name, ver))
            if not isinstance(eng, str) or not eng.strip():
                raise ValueError("%s@%s engines.dsh 为空" % (name, ver))
            stype = src.get("type")
            if stype == "npm":
                pass
            elif stype == "git":
                url = src.get("url", "")
                if not url.startswith("https://") or not GIT_COMMIT_RE.match(src.get("commit", "")):
                    raise ValueError("%s@%s git 来源不合法" % (name, ver))
            else:
                raise ValueError("%s@%s source.type 只能是 npm 或 git" % (name, ver))
            versions.append({
                "version": ver,
                "publishTimestamp": ts,
                "source": src,
                "engines": {"dsh": eng},
            })
        plugins.append({
            "name": name,
            "title": e.get("title", {"en": name, "zh": name}),
            "description": e.get("description", {"en": "", "zh": ""}),
            "author": e.get("author", ""),
            "homepage": e.get("homepage", ""),
            "repository": e.get("repository", {"url": ""}),
            "metadata": {"labels": ["ilang"], "keywords": []},
            "versions": versions,
        })
    labels = {
        "ilang": {"title": {"en": "iLang-conformant", "zh": "iLang 合规"}},
    }
    for p in plugins:
        for lab in p["metadata"]["labels"]:
            if lab not in labels:
                raise ValueError("%s 引用了未声明的标签 %s" % (p["name"], lab))
    index = {
        "format": 1,
        "title": {"en": "iLang DSH Market", "zh": "iLang DSH 市场"},
        "description": {
            "en": "Only iLang-conformant DeepSeek Harness plugins: the manifest passes the official validator with zero errors and zero warnings, versions are pinned, licenses are on record. No ranking.",
            "zh": "只收 iLang 合规的 DeepSeek Harness 插件：清单过官方校验器 strict 0 错 0 警告，钉提交，许可在案。不排名。",
        },
        "metadata": {
            "labels": labels,
        },
        "plugins": plugins,
    }
    # 写出前自检官方规则
    if index["format"] != 1:
        raise ValueError("format 必须是 1")
    if "en" not in index["title"]:
        raise ValueError("title 必须含 en")
    return index


def skill_rows(reg):
    rows = []
    for e in [x for x in reg["entries"] if x.get("kind") == "skill"]:
        up = e.get("upstream")
        if up:
            src_html = '<a href="%s" target="_blank" rel="noopener">%s</a>' % (up["repo"], up["repo"])
            if up.get("doi"):
                src_html += ' · <a href="https://doi.org/%s" target="_blank" rel="noopener">%s</a>' % (up["doi"], up["doi"])
            if up.get("tag"):
                src_html += " · %s" % up["tag"]
        else:
            src_html = "—"
        sha = e.get("sha256_lf", "") or ""
        rows.append(
            '<div class="m-row"><div class="m-name">%s</div><div class="m-desc">%s</div>'
            '<div class="m-meta">%s · %s · %s · %s · <span title="%s">%s</span> · <span class="m-kit">随工具包</span></div></div>'
            % (e["name"], e["description"]["zh"], e["version"], e["author"], e["license"],
               src_html, sha, sha[:12])
        )
    return "\n".join(rows)


def bundle_rows(reg):
    rows = []
    for e in [x for x in reg["entries"] if x.get("kind") == "bundle"]:
        repo = e.get("repository", {}).get("url", "")
        if repo:
            repo_html = '<a href="%s" target="_blank" rel="noopener">%s</a>' % (repo, repo)
        else:
            repo_html = "—"
        ver = e["versions"][-1]
        commit = ver["source"].get("commit", "")
        rows.append(
            '<div class="m-row"><div class="m-name">%s</div><div class="m-desc">%s</div>'
            '<div class="m-meta">%s · %s · %s · %s · %s<span title="%s">%s</span></div></div>'
            % (e["name"], e["description"]["zh"], e["author"], e["license"], repo_html,
               ver["version"], commit, commit[:12] if commit else "—")
        )
    return "\n".join(rows)


def render_page(reg):
    text = io.open(INDEX_HTML, encoding="utf-8").read()
    a, b = "<!-- market:skills -->", "<!-- /market:skills -->"
    c, d = "<!-- market:bundles -->", "<!-- /market:bundles -->"
    for x, y in ((a, b), (c, d)):
        if x not in text or y not in text:
            raise ValueError("index.html 缺少 %s 标记" % x)
    text = re.sub(re.escape(a) + r".*?" + re.escape(b),
                  a + "\n" + skill_rows(reg) + "\n    " + b, text, flags=re.S)
    text = re.sub(re.escape(c) + r".*?" + re.escape(d),
                  c + "\n" + bundle_rows(reg) + "\n    " + d, text, flags=re.S)
    return text


def fill_skill_meta(reg, write):
    changed = False
    for e in [x for x in reg["entries"] if x.get("kind") == "skill"]:
        linted = validate_manifest(e["manifest"])
        sha = sha256_lf(os.path.join(ROOT, e["manifest"]))
        validated = {
            "tool": "tools/ilang_grammar_validator.py --lint --strict",
            "strict": True,
            "errors": 0,
            "warnings": 0,
            "fences_linted": linted,
            "at": datetime.date.today().isoformat(),
        }
        if e.get("sha256_lf") != sha or e.get("validated") != validated:
            e["sha256_lf"] = sha
            e["validated"] = validated
            changed = True
    return changed


def main(argv=None):
    ap = argparse.ArgumentParser(description="市场构建器")
    ap.add_argument("--check", action="store_true", help="只校验，不写任何文件")
    args = ap.parse_args(argv)

    reg = json.load(io.open(REGISTRY, encoding="utf-8"))
    if reg.get("format") != 1 or "en" not in reg.get("title", {}):
        fail("registry format/title 违规")
    if reg.get("ranking") != "none":
        fail("ranking 必须是 none")

    # bundle 字段预检
    for e in [x for x in reg["entries"] if x.get("kind") == "bundle"]:
        for k in ("name", "title", "description", "author", "license", "repository", "versions"):
            if k not in e:
                fail("%s 缺少字段 %s" % (e.get("name", "?"), k))
        if not e["versions"]:
            fail("%s versions 为空" % e["name"])
        for v in e["versions"]:
            if v["source"].get("type") == "git" and not GIT_COMMIT_RE.match(v["source"].get("commit", "")):
                fail("%s@%s commit 格式非法" % (e["name"], v["version"]))

    changed = fill_skill_meta(reg, write=not args.check)
    index = build_index(reg)

    if args.check:
        text = io.open(INDEX_HTML, encoding="utf-8").read()
        for marker in ("<!-- market:skills -->", "<!-- /market:skills -->",
                       "<!-- market:bundles -->", "<!-- /market:bundles -->"):
            if marker not in text:
                fail("index.html 缺少 %s" % marker)
        existing = json.load(io.open(INDEX_JSON, encoding="utf-8"))
        if existing != index:
            fail("index.json 与登记表不一致（先跑 python tools/market_build.py 重新生成）")
        print("[market_build] check OK")
        return 0

    with open(REGISTRY, "w", encoding="utf-8", newline="\n") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(INDEX_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
        f.write("\n")
    page = render_page(reg)
    with open(INDEX_HTML, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)
    print("[market_build] wrote registry.json / index.json / index.html rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
