#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""市场准入检查器：<https 仓库地址> <tag 或 commit> 逐门核验一本 iLang 工程书，全过打印 ADMIT 与可贴进 registry.json 的条目。

用法:
  python -X utf8 tools/market_admit.py <仓库 https 地址> <tag 或 commit> [--book 工程书路径] [--json]

四条门：
  清单    工程书的第一行和最后一行都是 ::ILANG::v5.0::ENGINEERING_BOOK，全文恰好两行
  校验器  tools/ilang_grammar_validator.py --lint --strict 0 错 0 警告
  钉死    记下 40 位 commit 与工程书的 sha256（CRLF 换 LF 后算）
  许可    仓库根目录有 OSI 许可文件

退出码: 0 ADMIT；1 REJECT（逐条原因）；2 网络或 git 出错。
只用标准库与本机 git；绝不运行被检查仓库的任何代码；绝不写 registry.json，也不把书放进本仓库。
ADMIT 之后由 owner 说收，才把这本书原样内置到 books/<name>/BOOK.md 并登记。
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

GIT = shutil.which("git") or shutil.which("git", path=r"C:\Program Files\Git\cmd") or "git"
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
MARKER = "::ILANG::v5.0::ENGINEERING_BOOK"
BOOK_CANDIDATES = ("BOOK.md", "book.md", "BOOK.ilang.md")
LICENSE_SIGNS = (
    ("MIT", "MIT License"),
    ("Apache-2.0", "Apache License"),
    ("BSD", "Redistribution and use in source and binary forms"),
    ("ISC", "ISC License"),
    ("MPL-2.0", "Mozilla Public License"),
    ("GPL", "GNU GENERAL PUBLIC LICENSE"),
    ("LGPL", "GNU LESSER GENERAL PUBLIC LICENSE"),
    ("AGPL-3.0", "GNU AFFERO GENERAL PUBLIC LICENSE"),
    ("Unlicense", "This is free and unencumbered software"),
)


def git(args, cwd=None):
    r = subprocess.run([GIT] + args, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", cwd=cwd, env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    return r


def clone(url, ref, tmp):
    if COMMIT_RE.match(ref):
        r = git(["clone", "--quiet", url, tmp])
        if r.returncode != 0:
            return None, "clone 失败：%s" % r.stderr.strip()[:200]
        r = git(["fetch", "--quiet", "origin", ref], cwd=tmp)
        if r.returncode != 0:
            return None, "fetch %s 失败：%s" % (ref, r.stderr.strip()[:200])
        r = git(["checkout", "--quiet", ref], cwd=tmp)
        if r.returncode != 0:
            return None, "checkout %s 失败：%s" % (ref, r.stderr.strip()[:200])
    else:
        r = git(["clone", "--quiet", "--branch", ref, "--depth", "1", url, tmp])
        if r.returncode != 0:
            return None, "clone --branch %s 失败：%s" % (ref, r.stderr.strip()[:200])
    r = git(["log", "-1", "--format=%H %ct"], cwd=tmp)
    if r.returncode != 0:
        return None, "git log 失败：%s" % r.stderr.strip()[:200]
    out = r.stdout.strip().split()
    return (out[0], int(out[1])), None


def find_book(root, given):
    if given:
        p = os.path.join(root, given)
        return p if os.path.isfile(p) else None
    for name in BOOK_CANDIDATES:
        p = os.path.join(root, name)
        if os.path.isfile(p):
            return p
    return None


def detect_license(root):
    for f in sorted(os.listdir(root)):
        if not f.upper().startswith("LICENSE"):
            continue
        p = os.path.join(root, f)
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8", errors="replace") as fh:
            text = fh.read(4000)
        for spdx, sign in LICENSE_SIGNS:
            if sign.lower() in text.lower():
                return spdx
        return ""
    return None


def sha256_lf(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read().replace(b"\r\n", b"\n")).hexdigest()


def header_tag(text, key):
    m = re.search(r"^\[%s:([^\]\n]+)\]" % re.escape(key), text, re.M)
    return m.group(1).strip() if m else ""


def main(argv=None):
    ap = argparse.ArgumentParser(description="市场准入检查器（工程书）")
    ap.add_argument("repo", help="仓库 https 地址")
    ap.add_argument("ref", help="tag 或 commit")
    ap.add_argument("--book", default="", help="工程书在仓库里的路径，缺省找根目录的 BOOK.md")
    ap.add_argument("--json", action="store_true", help="只输出条目 JSON")
    args = ap.parse_args(argv)

    reasons = []
    tmp = tempfile.mkdtemp(prefix="market-admit-")
    try:
        (commit, ts), err = clone(args.repo, args.ref, tmp)
        if err:
            print("REJECT")
            print("网络或 git 出错：%s" % err)
            return 2

        book = find_book(tmp, args.book)
        text = ""
        book_id = version = ""
        if not book:
            reasons.append("没找到工程书（--book 指定路径，或根目录放 BOOK.md）")
        else:
            with open(book, encoding="utf-8", errors="replace") as f:
                text = f.read()
            lines = [x.rstrip("\r") for x in text.split("\n")]
            nonempty = [x for x in lines if x.strip()]
            marks = sum(1 for x in lines if x.strip() == MARKER)
            if not nonempty or nonempty[0].strip() != MARKER or nonempty[-1].strip() != MARKER or marks != 2:
                reasons.append("工程书的第一行和最后一行必须都是 %s，全文恰好两行（现在 %d 行）" % (MARKER, marks))
            else:
                validator = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                         "tools", "ilang_grammar_validator.py")
                r = subprocess.run([sys.executable, "-X", "utf8", validator, "--lint", book, "--strict"],
                                   capture_output=True, text=True, encoding="utf-8", errors="replace")
                if r.returncode != 0:
                    reasons.append("工程书校验未过：%s" % (r.stdout + r.stderr).strip()[:200])
            book_id = header_tag(text, "ID")
            version = header_tag(text, "VERSION")
            if not book_id:
                reasons.append("工程书头部缺 [ID:...]")
            if not version:
                reasons.append("工程书头部缺 [VERSION:...]")

        lic = detect_license(tmp)
        if lic is None:
            reasons.append("仓库根目录没有 LICENSE 文件")
        elif lic == "":
            reasons.append("LICENSE 文件不是常见的 OSI 许可")

        if reasons:
            print("REJECT")
            for i, r_ in enumerate(reasons, 1):
                print("%d. %s" % (i, r_))
            return 1

        name = re.sub(r"[^a-z0-9]+", "-", book_id.lower()).strip("-")
        entry = {
            "kind": "book",
            "name": name,
            "title": {"zh": book_id, "en": book_id},
            "description": {"zh": "", "en": ""},
            "version": version,
            "author": "",
            "license": lic,
            "manifest": "books/%s/BOOK.md" % name,
            "procedure": "books/%s/BOOK.md" % name,
            "upstream": {"repo": args.repo.rstrip("/"), "commit": commit,
                         "path": os.path.relpath(book, tmp).replace(os.sep, "/"),
                         "publishTimestamp": ts},
            "sha256_lf": sha256_lf(book),
            "validated": {"tool": "tools/ilang_grammar_validator.py --lint --strict",
                          "strict": True, "errors": 0, "warnings": 0, "markers": 2,
                          "at": datetime.date.today().isoformat()},
            "say": "",
            "get": "kit",
            "admitted_by": "@SUN",
            "admitted_on": datetime.date.today().isoformat(),
        }
        if args.json:
            print(json.dumps(entry, ensure_ascii=False, indent=2))
            return 0
        print("ADMIT")
        print("commit=%s timestamp=%d" % (commit, ts))
        print("下一步：owner 说收之后，把这本书原样放进 %s，补上 title、description、author、say，"
              "把条目加进 docs/market/registry.json，再跑 python -X utf8 tools/market_build.py" % entry["manifest"])
        print("entry:")
        print(json.dumps(entry, ensure_ascii=False, indent=2))
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
