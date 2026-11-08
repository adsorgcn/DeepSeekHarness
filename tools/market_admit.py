#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""市场准入检查器：<https 仓库地址> <tag 或 commit> 逐门核验，全过打印 ADMIT 与可贴进 registry.json 的条目。

用法:
  python -X utf8 tools/market_admit.py <仓库 https 地址> <tag 或 commit> [--path 子目录] [--manifest 文件] [--json]

退出码: 0 ADMIT；1 REJECT（逐条原因）；2 网络或 git 出错。
只用标准库与本机 git；绝不运行被检查仓库的任何代码（不 npm install、不 node）；
绝不写 registry.json。
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

GIT = shutil.which("git") or shutil.which("git", path=r"C:\Program Files\Git\cmd") or "git"
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
OSI_LICENSES = (
    "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "MPL-2.0",
    "GPL-2.0", "GPL-3.0", "LGPL-2.1", "LGPL-3.0", "AGPL-3.0", "Unlicense", "0BSD",
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


def find_manifest(root, given, sub):
    base = os.path.join(root, sub) if sub else root
    if given:
        p = os.path.join(root, given)
        return p if os.path.exists(p) else None
    candidates = ["ilang.md", "ILANG.md", "SKILL.md", "README.md"]
    for name in candidates:
        p = os.path.join(base, name)
        if os.path.exists(p):
            return p
    skills_glob = os.path.join(base, ".dsh", "skills", "*", "SKILL.md")
    import glob
    hits = sorted(glob.glob(skills_glob))
    return hits[0] if hits else None


def main(argv=None):
    ap = argparse.ArgumentParser(description="市场准入检查器")
    ap.add_argument("repo", help="仓库 https 地址")
    ap.add_argument("ref", help="tag 或 commit")
    ap.add_argument("--path", default="", help="子目录")
    ap.add_argument("--manifest", default="", help="清单文件路径")
    ap.add_argument("--json", action="store_true", help="条目以 JSON 输出")
    args = ap.parse_args(argv)

    reasons = []
    tmp = tempfile.mkdtemp(prefix="market-admit-")
    try:
        (commit, ts), err = clone(args.repo, args.ref, tmp)
        if err:
            print("REJECT")
            print("网络或 git 出错：%s" % err)
            return 2

        base = os.path.join(tmp, args.path) if args.path else tmp
        pkg_path = os.path.join(base, "package.json")
        if not os.path.exists(pkg_path):
            reasons.append("package.json 不存在")
            pkg = {}
        else:
            with open(pkg_path, encoding="utf-8") as f:
                pkg = json.load(f)

        name = pkg.get("name", "")
        version = pkg.get("version", "")
        license_field = pkg.get("license", "")
        description = pkg.get("description", "")
        author = pkg.get("author", "")
        engines_dsh = ((pkg.get("engines") or {}).get("dsh", ""))
        has_bundle = isinstance(pkg.get("dsh"), dict) and bool(pkg.get("dsh", {}).get("bundle"))

        if not name or not isinstance(name, str):
            reasons.append("package.json 缺 name")
        if not version or not isinstance(version, str):
            reasons.append("package.json 缺精确 version")
        if not engines_dsh or not isinstance(engines_dsh, str) or not engines_dsh.strip():
            reasons.append("engines.dsh 缺失或为空")
        if not has_bundle:
            reasons.append("package.json 缺 dsh.bundle（不是组合包，DSH 安装阶段会拒）")
        if pkg.get("private") is True:
            reasons.append("package.json private=true")

        license_files = [f for f in os.listdir(base) if f.upper().startswith("LICENSE")]
        if not license_files:
            reasons.append("仓库里没有 LICENSE 文件")
        if str(license_field).strip() not in OSI_LICENSES:
            reasons.append("license 字段 %r 不在 OSI 常见清单内" % license_field)

        manifest = find_manifest(tmp, args.manifest, args.path)
        if not manifest:
            reasons.append("没找到 iLang 清单（--manifest 或 ilang.md / ILANG.md / SKILL.md / README.md / .dsh/skills/*/SKILL.md）")
        else:
            with open(manifest, encoding="utf-8", errors="replace") as f:
                text = f.read()
            fence_ok = ("::ILANG::v5.0" in text and "::GENE{" in text)
            if not fence_ok:
                reasons.append("清单里没有以 ::ILANG::v5.0 开头且含 ::GENE{ 的围栏")
            else:
                validator = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                         "tools", "ilang_grammar_validator.py")
                r = subprocess.run([sys.executable, "-X", "utf8", validator, "--lint", manifest, "--strict"],
                                   capture_output=True, text=True, encoding="utf-8", errors="replace")
                m = re.search(r"linted=([0-9]+)", r.stdout + r.stderr)
                linted = int(m.group(1)) if m else 0
                if r.returncode != 0:
                    reasons.append("清单校验未过：%s" % (r.stdout + r.stderr).strip()[:200])
                elif linted < 1:
                    reasons.append("清单 linted=%d（需要不小于 1）" % linted)

        if reasons:
            print("REJECT")
            for i, r_ in enumerate(reasons, 1):
                print("%d. %s" % (i, r_))
            return 1

        entry = {
            "kind": "bundle",
            "name": name,
            "title": {"zh": name, "en": name},
            "description": {"zh": description, "en": description},
            "author": author,
            "license": license_field,
            "repository": {"url": args.repo.rstrip("/")},
            "homepage": pkg.get("homepage", ""),
            "manifest": {"path": os.path.relpath(manifest, tmp), "sha256_lf": None},
            "validated": {"tool": "tools/ilang_grammar_validator.py --lint --strict",
                          "strict": True, "errors": 0, "warnings": 0,
                          "fences_linted": linted, "at": datetime.date.today().isoformat()},
            "versions": [{
                "version": version,
                "commit": commit,
                "publishTimestamp": ts,
                "engines_dsh": engines_dsh,
                "source": {"type": "git", "url": args.repo.rstrip("/"), "commit": commit},
            }],
            "admitted_by": "@SUN",
            "admitted_on": datetime.date.today().isoformat(),
        }
        print("ADMIT")
        print("commit=%s timestamp=%d" % (commit, ts))
        print("entry:")
        print(json.dumps(entry, ensure_ascii=False, indent=2))
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
