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
from html import escape
from urllib.parse import quote
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


def external_link(url, label):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (escape(url, quote=True), escape(label))


def meta_field(label, value_html):
    return "<div><dt>%s</dt><dd>%s</dd></div>" % (label, value_html)


def entry_source(e):
    up = e.get("upstream") or {}
    fields = [
        meta_field("作者", escape(e["author"])),
        meta_field("许可", escape(e["license"])),
    ]
    if e["kind"] != "plugin":
        fields.append(meta_field("工具包文件", external_link(
            "https://github.com/adsorgcn/DeepSeekHarness/blob/main/" + quote(e["manifest"]),
            e["manifest"])))
    if up.get("repo"):
        fields.append(meta_field("上游仓库", external_link(up["repo"], up["repo"].removeprefix("https://github.com/"))))
    if up.get("doi"):
        fields.append(meta_field("DOI", external_link("https://doi.org/" + up["doi"], up["doi"])))
    if up.get("tag"):
        fields.append(meta_field("版本标签", external_link(
            up["repo"] + "/tree/" + quote(up["tag"], safe=""), up["tag"])))
    if up.get("commit"):
        fields.append(meta_field("来源提交", external_link(
            up["repo"] + "/commit/" + up["commit"], up["commit"])))
    if e.get("npm"):
        npm = e["npm"]
        fields.append(meta_field("npm 包", external_link(
            "https://www.npmjs.com/package/" + quote(npm["name"]), npm["name"])))
        fields.append(meta_field("npm integrity", '<code>%s</code>' % escape(npm["integrity"])))
    elif e.get("sha256_lf"):
        fields.append(meta_field("SHA-256 · LF", '<code>%s</code>' % escape(e["sha256_lf"])))
    return "\n".join(fields)


def catalog_rows(reg, kind):
    cards = []
    display_names = {"site-design-engine": "网站设计", "deai": "写作去 AI 味"}
    for e in reg["entries"]:
        if e["kind"] != kind:
            continue
        name = escape(e["name"], quote=True)
        title = escape(display_names.get(e["title"]["zh"], e["title"]["zh"]))
        say = e.get("say")
        description = e["description"]["zh"]
        invocation = ""
        if say:
            lead = re.match(r"^(说一句「[^」]+」(?:或「[^」]+」)*)[，,]\s*", description)
            if lead:
                command = lead.group(1)
                description = description[lead.end():]
            else:
                command = "说一句" + "或".join("「%s」" % word for word in say.split(" / "))
            invocation = '\n  <p class="invocation">%s</p>' % escape(command)
        identifier = '<span class="identifier">%s</span>' % name if title != name else ""
        cards.append(f'''<article class="entry" id="entry-{name}" data-kind="{kind}">
  <header class="entry-head">
    <span class="entry-mark" aria-hidden="true"><i></i></span>
    <div><h3>{title}</h3>{identifier}</div>
    <span class="version" aria-label="版本 {escape(e['version'])}">v{escape(e['version'])}</span>
  </header>
  <p class="entry-description">{escape(description)}</p>{invocation}
  <details class="entry-details">
    <summary>版本与来源<span class="visually-hidden"> · {title}</span></summary>
    <dl class="entry-meta">{entry_source(e)}</dl>
  </details>
</article>''')
    return "\n".join(cards)


def books_region(reg):
    rows = catalog_rows(reg, "book")
    if rows:
        return ('<div class="entries">%s</div>\n' % rows
                + '<p class="section-note">工程书装了工具包就有，说出卡片上的口令即可开始。</p>')
    return '<p class="section-note">收录的工程书装了工具包就有。</p>'


def render_page(reg):
    text = io.open(INDEX_HTML, encoding="utf-8").read()
    categories = (("skills", "skill", "内置技能"), ("books", "book", "工程书"), ("plugins", "plugin", "官方插件"))
    nav = []
    for section, kind, label in categories:
        count = sum(e["kind"] == kind for e in reg["entries"])
        nav.append(f'<a href="#{section}">{label}<span class="count">{count}</span></a>')
    regions = {
        "nav": "\n".join(nav),
        "skills": catalog_rows(reg, "skill"),
        "books": books_region(reg),
        "plugins": catalog_rows(reg, "plugin"),
    }
    for name, content in regions.items():
        start, end = f"<!-- market:{name} -->", f"<!-- /market:{name} -->"
        if text.count(start) != 1 or text.count(end) != 1 or text.index(start) >= text.index(end):
            raise ValueError("index.html 缺少成对的 %s 标记" % name)
        text = re.sub(re.escape(start) + r".*?" + re.escape(end),
                      lambda _m: start + "\n" + content + "\n" + end, text, flags=re.S)
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
