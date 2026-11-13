#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""市场构建器：校验 docs/market/registry.json 里登记的技能与工程书，回写 sha256 与校验记录，生成市场页的行区。

货架模式：过了门、owner 说收的技能与工程书都原样内置在工具包里，装了工具包就有；
这里没有供用户自己添加的索引，也不让用户在一堆条目里挑。

用法:
  python tools/market_build.py           # 校验、回写 version/sha256_lf/validated、生成页面行区
  python tools/market_build.py --check   # 只校验，不写任何文件

只用标准库；绝不运行被登记内容里的任何代码。
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
INDEX_HTML = os.path.join(ROOT, "docs", "market", "index.html")
VALIDATOR = os.path.join(ROOT, "tools", "ilang_grammar_validator.py")
MARKER = "::ILANG::v5.0::ENGINEERING_BOOK"
KINDS = ("skill", "book", "plugin")
TOOL = "tools/ilang_grammar_validator.py --lint --strict"
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def fail(msg):
    print("[market_build] %s" % msg)
    sys.exit(1)


def sha256_lf(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read().replace(b"\r\n", b"\n")).hexdigest()


def run_validator(path):
    r = subprocess.run([sys.executable, "-X", "utf8", VALIDATOR, "--lint",
                        os.path.join(ROOT, path), "--strict"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = r.stdout + r.stderr
    m = re.search(r"linted=([0-9]+)", out)
    return r.returncode, out, int(m.group(1)) if m else 0


def validate_manifest(path):
    """技能清单：返回 linted；违规直接抛异常。"""
    if not os.path.exists(os.path.join(ROOT, path)):
        raise ValueError("%s 不存在" % path)
    text = io.open(os.path.join(ROOT, path), encoding="utf-8").read()
    if "::ILANG::v5.0" not in text:
        raise ValueError("%s 缺少 ::ILANG::v5.0" % path)
    rc, out, linted = run_validator(path)
    if rc != 0:
        raise ValueError("%s 校验器未通过：%s" % (path, out.strip()[:300]))
    if linted < 1:
        raise ValueError("%s 没有 linted 围栏（linted=%d）" % (path, linted))
    return linted


def validate_book(path):
    """工程书：首尾两行都是标记且全文恰好两行，校验器 strict 0 错 0 警告；返回标记行数。"""
    if not os.path.exists(os.path.join(ROOT, path)):
        raise ValueError("%s 不存在" % path)
    text = io.open(os.path.join(ROOT, path), encoding="utf-8").read()
    lines = [x.rstrip("\r") for x in text.split("\n")]
    nonempty = [x for x in lines if x.strip()]
    marks = sum(1 for x in lines if x.strip() == MARKER)
    if not nonempty or nonempty[0].strip() != MARKER or nonempty[-1].strip() != MARKER or marks != 2:
        raise ValueError("%s 的第一行和最后一行必须都是 %s，全文恰好两行（现在 %d 行）" % (path, MARKER, marks))
    rc, out, _ = run_validator(path)
    if rc != 0:
        raise ValueError("%s 校验器未通过：%s" % (path, out.strip()[:300]))
    return marks


def procedure_frontmatter_version(path):
    """读 procedure 文件 frontmatter 里的 version 行；没有则返回 None。"""
    text = io.open(os.path.join(ROOT, path), encoding="utf-8").read()
    m = re.search(r"^version:\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else None


def book_header_version(path):
    """读工程书头部的 [VERSION:...]；没有则返回 None。"""
    text = io.open(os.path.join(ROOT, path), encoding="utf-8").read()
    m = re.search(r"^\[VERSION:([^\]\n]+)\]", text, re.M)
    return m.group(1).strip() if m else None


def sync_market_fence(entry):
    """把 MARKET.md 里 ::GENE 到最后一行 T:/A: 的那一段换成 procedure 文件里同一段。

    manifest 与 procedure 是同一文件时无需同步（site-design-engine、deai）。"""
    if entry["manifest"] == entry["procedure"]:
        return None
    proc_path = os.path.join(ROOT, entry["procedure"])
    manifest_path = os.path.join(ROOT, entry["manifest"])
    proc = io.open(proc_path, encoding="utf-8", newline="").read()
    manifest = io.open(manifest_path, encoding="utf-8", newline="").read()
    gene_re = re.compile(r"::GENE[{][^\n]*\n(?:[ \t]+[TA]:[^\n]*\n)+")
    pm = gene_re.search(proc)
    mm = gene_re.search(manifest)
    if not pm:
        raise ValueError("%s 里没有 GENE 块" % entry["procedure"])
    if not mm:
        raise ValueError("%s 里没有 GENE 块" % entry["manifest"])
    if mm.group(0).strip() != pm.group(0).strip():
        manifest = manifest[: mm.start()] + pm.group(0) + manifest[mm.end():]
        with open(manifest_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(manifest)
    return pm.group(0).strip()


def sha_drift(reg):
    """登记的 sha256 与文件现状不一致的条目名（plugin 条目没有 sha256，跳过）。"""
    bad = []
    for e in reg["entries"]:
        if e.get("kind") == "plugin":
            continue
        p = os.path.join(ROOT, e["manifest"])
        if not os.path.exists(p) or sha256_lf(p) != e.get("sha256_lf"):
            bad.append(e["name"])
    return bad


def fill_meta(reg, write):
    """回写每条的 version、sha256_lf 与 validated；返回是否有变化。write=False 时不动磁盘上的清单副本。

    plugin 条目钉的是 npm 的 integrity 与 commit，不在此回写。"""
    changed = False
    today = datetime.date.today().isoformat()
    for e in reg["entries"]:
        if e["kind"] == "plugin":
            continue
        if e["kind"] == "skill":
            ver = procedure_frontmatter_version(e["procedure"])
            if write:
                sync_market_fence(e)
            linted = validate_manifest(e["manifest"])
            validated = {"tool": TOOL, "strict": True, "errors": 0, "warnings": 0,
                         "fences_linted": linted, "at": today}
        else:
            ver = book_header_version(e["manifest"])
            marks = validate_book(e["manifest"])
            validated = {"tool": TOOL, "strict": True, "errors": 0, "warnings": 0,
                         "markers": marks, "at": today}
        if ver and e.get("version") != ver:
            e["version"] = ver
            changed = True
        sha = sha256_lf(os.path.join(ROOT, e["manifest"]))
        if e.get("sha256_lf") != sha or e.get("validated") != validated:
            e["sha256_lf"] = sha
            e["validated"] = validated
            changed = True
    return changed


def source_html(e):
    up = e.get("upstream")
    if not up:
        return "—"
    html = '<a href="%s" target="_blank" rel="noopener">%s</a>' % (up["repo"], up["repo"])
    if up.get("doi"):
        html += ' · <a href="https://doi.org/%s" target="_blank" rel="noopener">%s</a>' % (up["doi"], up["doi"])
    if up.get("tag"):
        html += " · %s" % up["tag"]
    if up.get("commit"):
        html += ' · <span title="%s">%s</span>' % (up["commit"], up["commit"][:12])
    return html


def skill_rows(reg):
    rows = []
    for e in [x for x in reg["entries"] if x.get("kind") == "skill"]:
        sha = e.get("sha256_lf", "") or ""
        rows.append(
            '<div class="m-row"><div class="m-name">%s</div><div class="m-desc">%s</div>'
            '<div class="m-meta">%s · %s · %s · %s · <span title="%s">%s</span></div></div>'
            % (e["name"], e["description"]["zh"], e["version"], e["author"], e["license"],
               source_html(e), sha, sha[:12])
        )
    return "\n".join(rows)


def book_rows(reg):
    rows = []
    for e in [x for x in reg["entries"] if x.get("kind") == "book"]:
        sha = e.get("sha256_lf", "") or ""
        say = e.get("say", "")
        say_html = ("说一句「%s」 · " % say) if say else ""
        rows.append(
            '<div class="m-row"><div class="m-name">%s</div><div class="m-desc">%s</div>'
            '<div class="m-meta">%s%s · %s · %s · %s · <span title="%s">%s</span></div></div>'
            % (e["title"]["zh"], e["description"]["zh"], say_html, e["version"], e["author"], e["license"],
               source_html(e), sha, sha[:12])
        )
    return "\n".join(rows)


def books_region(reg):
    """market:books 标记之间的内容：有行态（行区 + 一句用法）或空态（一句话，不带数量词）。"""
    rows = book_rows(reg)
    if rows:
        return ("\n" + rows + "\n"
                '    <p class="after">装了工具包就有。说出那句话，它照着书一步一步带你做。</p>')
    return '\n    <p class="after">过了门、owner 说收的工程书放在这里，装了工具包就有。</p>'


def render_page(reg):
    text = io.open(INDEX_HTML, encoding="utf-8").read()
    a, b = "<!-- market:skills -->", "<!-- /market:skills -->"
    c, d = "<!-- market:books -->", "<!-- /market:books -->"
    for x, y in ((a, b), (c, d)):
        if x not in text or y not in text:
            raise ValueError("index.html 缺少 %s 标记" % x)
    text = re.sub(re.escape(a) + r".*?" + re.escape(b),
                  lambda _m: a + "\n" + skill_rows(reg) + "\n    " + b, text, flags=re.S)
    text = re.sub(re.escape(c) + r".*?" + re.escape(d),
                  lambda _m: c + books_region(reg) + "\n    " + d, text, flags=re.S)
    return text


def check_structure(reg):
    if reg.get("format") != 1 or "en" not in reg.get("title", {}):
        fail("registry format/title 违规")
    if reg.get("ranking") != "none":
        fail("ranking 必须是 none")
    names = [e.get("name") for e in reg["entries"]]
    if len(names) != len(set(names)):
        fail("登记表里有重名条目")
    need = ("name", "title", "description", "version", "author", "license",
            "manifest", "procedure", "sha256_lf", "validated")
    for e in reg["entries"]:
        if e.get("kind") not in KINDS:
            fail("%s 的 kind 只能是 skill、book 或 plugin" % e.get("name", "?"))
        if e["kind"] == "plugin":
            npm = e.get("npm") or {}
            up = e.get("upstream") or {}
            if not isinstance(npm.get("name"), str) or not npm.get("name"):
                fail("%s 缺 npm.name" % e["name"])
            if not isinstance(npm.get("version"), str) or not npm.get("version"):
                fail("%s 缺 npm.version" % e["name"])
            if not isinstance(npm.get("integrity"), str) or not npm["integrity"].startswith("sha512-"):
                fail("%s 的 npm.integrity 必须以 sha512- 开头" % e["name"])
            if not isinstance(up.get("commit"), str) or not COMMIT_RE.match(up["commit"]):
                fail("%s 的 upstream.commit 必须是 40 位十六进制" % e["name"])
            if not isinstance(up.get("tag"), str) or up["tag"] != "v" + npm["version"]:
                fail("%s 的 upstream.tag 必须是 v 加 npm.version" % e["name"])
            if e.get("get") != "npm":
                fail("%s 的 get 必须是 npm" % e["name"])
            for k in ("name", "title", "description", "version", "author", "license",
                      "manifest", "procedure", "validated", "say"):
                if k not in e:
                    fail("%s 缺少字段 %s" % (e.get("name", "?"), k))
            continue
        for k in need:
            if k not in e:
                fail("%s 缺少字段 %s" % (e.get("name", "?"), k))
        if e.get("get") != "kit":
            fail("%s 的 get 必须是 kit：过门的条目一律随工具包内置" % e["name"])
        if e["kind"] == "book" and not e["manifest"].startswith(".dsh/books/"):
            fail("%s 的工程书必须内置在 .dsh/books/ 下" % e["name"])


def main(argv=None):
    ap = argparse.ArgumentParser(description="市场构建器")
    ap.add_argument("--check", action="store_true", help="只校验，不写任何文件")
    args = ap.parse_args(argv)

    reg = json.load(io.open(REGISTRY, encoding="utf-8"))
    check_structure(reg)
    try:
        if args.check:
            drift = sha_drift(reg)
            fill_meta(reg, write=False)
            if drift:
                fail("这些条目的 sha256 与登记不一致：%s（先跑 python tools/market_build.py 重新生成）" % ", ".join(drift))
            if render_page(reg) != io.open(INDEX_HTML, encoding="utf-8").read():
                fail("市场页的行区不是最新（先跑 python tools/market_build.py 重新生成）")
            print("[market_build] check OK")
            return 0
        fill_meta(reg, write=True)
        page = render_page(reg)
    except ValueError as exc:
        fail(str(exc))

    with open(REGISTRY, "w", encoding="utf-8", newline="\n") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(INDEX_HTML, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)
    print("[market_build] wrote registry.json / index.html rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
