# -*- coding: utf-8 -*-
"""市场行为测试（纯标准库 + 本机 git，零网络）。

货架模式：过门的技能与工程书都内置在工具包里，没有供用户添加的索引。

场景：registry 结构；技能清单过校验器且 linted>=1；工程书首尾标记且过校验器；
sha 漂移检测；mem-forever 围栏副本逐字一致；技能与工程书版本跟随正文；
没有插件索引也没有加源的说法；市场页行区与零外部加载；市场页文案；
market_build --check；行区两种渲染态；market_admit 四个 git 夹具
（ADMIT / REJECT 无工程书 / REJECT 标记不对 / REJECT 无许可）；入口指令里的货架规矩。

用法: python -X utf8 tools/test_market.py （工作目录=仓库根）
"""
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
GIT = shutil.which("git") or shutil.which("git", path=r"C:\Program Files\Git\cmd") or "git"
MARKER = "::ILANG::v5.0::ENGINEERING_BOOK"
RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print("[%s] %s %s" % (name, "PASS" if cond else "FAIL", detail))


def lf_sha256(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read().replace(b"\r\n", b"\n")).hexdigest()


def read(p):
    return io.open(os.path.join(ROOT, p), encoding="utf-8").read()


def load_json(p):
    return json.load(io.open(os.path.join(ROOT, p), encoding="utf-8"))


def run_validator(p):
    res = subprocess.run([PY, "-B", "-X", "utf8", os.path.join(ROOT, "tools", "ilang_grammar_validator.py"),
                          "--lint", p, "--strict"], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    m = re.search(r"linted=([0-9]+)", res.stdout + res.stderr)
    return res.returncode, int(m.group(1) if m else 0)


def test_registry_structure():
    r = load_json("docs/market/registry.json")
    ok = r.get("format") == 1 and "en" in r["title"] and "zh" in r["title"] \
        and isinstance(r.get("gate"), dict) \
        and all(k in r["gate"] for k in ("manifest", "validator", "pin", "license", "veto", "shelf")) \
        and r.get("ranking") == "none"
    entries = r["entries"]
    names = [e["name"] for e in entries]
    need = ("name", "title", "description", "version", "author", "license",
            "manifest", "procedure", "sha256_lf", "validated")
    ok = ok and len(names) == len(set(names)) \
        and {"mem-forever", "site-design-engine", "deai", "ai-global-media"} <= set(names) \
        and all(e.get("kind") in ("skill", "book") for e in entries) \
        and all(all(k in e for k in need) for e in entries) \
        and all("zh" in e["description"] and "en" in e["description"] for e in entries) \
        and all(e.get("get") == "kit" for e in entries) \
        and all(e["manifest"].startswith(".dsh/books/") and e.get("say") and e.get("admitted_by") == "@SUN"
                for e in entries if e["kind"] == "book")
    check("registry_structure", ok)


def test_skill_manifests_validator():
    r = load_json("docs/market/registry.json")
    ok = True
    for e in [x for x in r["entries"] if x.get("kind") == "skill"]:
        text = read(e["manifest"])
        rc, linted = run_validator(os.path.join(ROOT, e["manifest"]))
        if text.count("::ILANG::v5.0") < 1 or rc != 0 or linted < 1:
            ok = False
            break
    check("skill_manifests_validator", ok)


def test_book_manifests_validator():
    r = load_json("docs/market/registry.json")
    books = [x for x in r["entries"] if x.get("kind") == "book"]
    ok = bool(books)
    for e in books:
        lines = [x.rstrip("\r") for x in read(e["manifest"]).split("\n")]
        nonempty = [x for x in lines if x.strip()]
        marks = sum(1 for x in lines if x.strip() == MARKER)
        rc, _ = run_validator(os.path.join(ROOT, e["manifest"]))
        if marks != 2 or nonempty[0].strip() != MARKER or nonempty[-1].strip() != MARKER or rc != 0:
            ok = False
            break
    check("book_manifests_validator", ok)


def test_sha_drift():
    r = load_json("docs/market/registry.json")
    bad = [e["name"] for e in r["entries"]
           if lf_sha256(os.path.join(ROOT, e["manifest"])) != e.get("sha256_lf")]
    check("sha_drift", not bad, "bad=%s" % bad)


def test_mem_forever_fence_copy():
    gene_re = re.compile(r"::GENE[{]mem-forever[^\n]*\n(?:[ \t]+[TA]:[^\n]*\n)+")
    a = gene_re.search(read(".dsh/skills/mem-forever/SKILL.md")).group(0).strip()
    b = gene_re.search(read(".dsh/skills/mem-forever/MARKET.md")).group(0).strip()
    check("mem_forever_fence_copy", a == b and a.count("\n") >= 15)


def test_version_follows_text():
    r = load_json("docs/market/registry.json")
    bad = []
    for e in r["entries"]:
        text = read(e["procedure"])
        if e["kind"] == "skill":
            m = re.search(r"^version:\s*(.+)$", text, re.M)
        else:
            m = re.search(r"^\[VERSION:([^\]\n]+)\]", text, re.M)
        if not m or m.group(1).strip() != e.get("version"):
            bad.append(e["name"])
    check("version_follows_text", not bad, "bad=%s" % bad)


def test_official_plugin_index():
    """官方插件走 DSH 官方索引格式 1：docs/market/index.json 列的是 npm 包，钉精确版本，带 engines；市场页教人加这条索引源。"""
    p = os.path.join(ROOT, "docs", "market", "index.json")
    ok = os.path.exists(p)
    detail = "missing"
    if ok:
        idx = load_json("docs/market/index.json")
        plugins = idx.get("plugins") or []
        names = [x.get("name") for x in plugins]
        bad = []
        if idx.get("format") != 1:
            bad.append("format")
        if "zh" not in (idx.get("title") or {}):
            bad.append("title.zh")
        if len(names) != len(set(names)):
            bad.append("dup names")
        for x in plugins:
            vs = x.get("versions") or []
            if not re.match(r"^[a-z0-9][a-z0-9._-]*$", x.get("name", "")):
                bad.append("name:%s" % x.get("name"))
            if not vs:
                bad.append("%s: no versions" % x.get("name"))
            for v in vs:
                if not re.match(r"^\d+\.\d+\.\d+", v.get("version", "")):
                    bad.append("%s: version not pinned" % x.get("name"))
                if (v.get("source") or {}).get("type") != "npm":
                    bad.append("%s: source must be npm" % x.get("name"))
                if not (v.get("engines") or {}).get("dsh"):
                    bad.append("%s: engines.dsh missing" % x.get("name"))
        m = read("docs/market/index.html")
        if "dsh-plugin-chuhai" not in names:
            bad.append("dsh-plugin-chuhai not listed")
        if "market/index.json" not in m or "dsh-plugin-chuhai" not in m:
            bad.append("market page does not show the official plugin / index url")
        ok = not bad
        detail = "bad=%s" % bad
    check("official_plugin_index", ok, detail)


def test_page_rows():
    r = load_json("docs/market/registry.json")
    m = read("docs/market/index.html")
    ext = re.findall(r"<a [^>]*href=['\"]https?://[^'\"]*['\"][^>]*>", m)
    shown = [e["name"] if e["kind"] == "skill" else e["title"]["zh"] for e in r["entries"]]
    ok = all(x in m for x in shown) \
        and all(("说一句「%s」" % e["say"]) in m for e in r["entries"] if e["kind"] == "book") \
        and "market:skills" in m and "market:books" in m and "market:bundles" not in m \
        and "<script src=" not in m \
        and not re.search(r"<link [^>]*href=['\"]https?://", m) \
        and "@import" not in m \
        and bool(ext) and all("target=" in a and "_blank" in a for a in ext) \
        and "0 个" not in m and "0个" not in m and "暂无" not in m
    check("page_rows", ok, "ext=%d" % len(ext))


def test_page_copy():
    m = read("docs/market/index.html")
    l = read("docs/index.html")
    stripped = re.sub(r"<style.*?</style>", "", m, flags=re.S)
    stripped = re.sub(r"<script.*?</script>", "", stripped, flags=re.S)
    body = stripped[stripped.find("<body"):]
    text = re.sub(r"<[^>]+>", "\n", body)
    lines = [x.strip() for x in text.split("\n") if x.strip()]
    ok = not any(k in m for k in ("不看星数", "不爬虫", "不排队", "不排名")) \
        and not any(k in l for k in ("不看星数", "不爬虫", "不排队")) \
        and not any(x.startswith("。") for x in lines) \
        and "收录顺序就是显示顺序" in m and "收录顺序就是显示顺序" in l \
        and "维护者看过准入输出后决定收不收。" in m \
        and "装了工具包就有" in m and "装了工具包就有" in l \
        and "帮你写一版更好的" in m
    check("page_copy", ok)


def test_build_check():
    res = subprocess.run([PY, "-B", "-X", "utf8", os.path.join(ROOT, "tools", "market_build.py"), "--check"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
    check("build_check", res.returncode == 0, res.stdout.strip()[-120:])


def test_render_states():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "market_build", os.path.join(ROOT, "tools", "market_build.py"))
    mb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mb)
    fake = {
        "entries": [{
            "kind": "book", "name": "fake-book",
            "title": {"zh": "假书", "en": "Fake book"},
            "description": {"zh": "假的描述", "en": "fake desc"},
            "version": "1.0.0", "author": "tester", "license": "MIT",
            "manifest": ".dsh/books/fake-book/BOOK.md", "procedure": ".dsh/books/fake-book/BOOK.md",
            "upstream": {"repo": "https://github.com/t/f", "commit": "a" * 40},
            "sha256_lf": "b" * 64, "validated": {}, "say": "假口令", "get": "kit",
        }]
    }
    with_rows = mb.books_region(fake)
    empty = mb.books_region({"entries": []})
    ok = "假书" in with_rows and "说一句「假口令」" in with_rows and "随工具包" in with_rows \
        and "a" * 12 in with_rows and "装了工具包就有" in with_rows \
        and "装了工具包就有" in empty and "m-row" not in empty \
        and "索引" not in with_rows and "索引" not in empty
    check("render_states", ok)


BOOK_OK = """::ILANG::v5.0::ENGINEERING_BOOK
[TYPE:engineering_book]
[ID:TEST-BOOK]
[VERSION:1.0.0]
[DATE:2026-11-10]
[LANG:en]

::STATE{@USER, role:decision_maker}

::OBJECTIVE{id:g1|owner:user|trust:trusted|version:1|status:active}
  target: a test book that does nothing
  ACCEPT: every item of RUBRIC passes
  NON_GOALS: anything else
  DONE_WHEN: the report was sent

::MODULE{HOW|title:how}
  [STEP] 1 say hello

::RUBRIC{A1: it said hello|check:human}
::ILANG::v5.0::ENGINEERING_BOOK
"""


def make_fixture(name, book=None, license_file=True):
    """建一个临时 git 仓库；book 为 None 则不写工程书。"""
    tmp = tempfile.mkdtemp(prefix="market-fixture-%s-" % name)
    with open(os.path.join(tmp, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("fixture\n")
    if license_file:
        with open(os.path.join(tmp, "LICENSE"), "w", encoding="utf-8", newline="\n") as f:
            f.write("MIT License\nCopyright (c) 2026 test\n")
    if book is not None:
        with open(os.path.join(tmp, "BOOK.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write(book)
    subprocess.run([GIT, "init", "-q", "-b", "main"], cwd=tmp, check=True)
    subprocess.run([GIT, "config", "user.email", "test@example.com"], cwd=tmp, check=True)
    subprocess.run([GIT, "config", "user.name", "test"], cwd=tmp, check=True)
    subprocess.run([GIT, "config", "core.autocrlf", "false"], cwd=tmp, check=True)
    subprocess.run([GIT, "add", "-A"], cwd=tmp, check=True)
    subprocess.run([GIT, "commit", "-q", "-m", "fixture"], cwd=tmp, check=True)
    subprocess.run([GIT, "tag", "v1.0.0"], cwd=tmp, check=True)
    return tmp


def run_admit(repo, ref):
    res = subprocess.run([PY, "-B", "-X", "utf8", os.path.join(ROOT, "tools", "market_admit.py"), repo, ref],
                         capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
    return res


def test_admit_fixtures():
    tmp_a = make_fixture("admit", book=BOOK_OK)
    tmp_b = make_fixture("nobook", book=None)
    tmp_c = make_fixture("badmarker", book=BOOK_OK.replace(MARKER + "\n[TYPE", "[TYPE", 1))
    tmp_d = make_fixture("nolicense", book=BOOK_OK, license_file=False)
    try:
        ra = run_admit(tmp_a, "v1.0.0")
        rb = run_admit(tmp_b, "v1.0.0")
        rc = run_admit(tmp_c, "v1.0.0")
        rd = run_admit(tmp_d, "v1.0.0")
        ok = ra.returncode == 0 and "ADMIT" in ra.stdout and '"kind": "book"' in ra.stdout \
            and '"name": "test-book"' in ra.stdout and '"get": "kit"' in ra.stdout \
            and rb.returncode == 1 and "REJECT" in rb.stdout \
            and rc.returncode == 1 and "REJECT" in rc.stdout \
            and rd.returncode == 1 and "REJECT" in rd.stdout
        check("admit_fixtures", ok,
              "admit=%d no_book=%d bad_marker=%d no_license=%d"
              % (ra.returncode, rb.returncode, rc.returncode, rd.returncode))
        if ra.returncode != 0:
            print("   admit out:", (ra.stdout + ra.stderr)[-300:])
    finally:
        for t in (tmp_a, tmp_b, tmp_c, tmp_d):
            shutil.rmtree(t, ignore_errors=True)


def test_shelf_rules_in_instructions():
    a = read("AGENTS.local.md")
    i = a.find("::GENE{dsh_market")
    j = a.find("::GENE{", i + 10)
    gene = a[i:j if j > 0 else len(a)]
    ok = i >= 0 \
        and "ship_inside_the_kit" in gene \
        and "help_you_write_a_better_version" in gene \
        and "submitted_for_review" in gene \
        and "author_repository_address_only" in gene \
        and "index_json" not in gene \
        and "::GENE{dsh_ai_global_media" in a and ".dsh/books/ai-global-media/BOOK.md" in a
    check("shelf_rules_in_instructions", ok)


def main():
    os.chdir(ROOT)
    test_registry_structure()
    test_skill_manifests_validator()
    test_book_manifests_validator()
    test_sha_drift()
    test_mem_forever_fence_copy()
    test_version_follows_text()
    test_official_plugin_index()
    test_page_rows()
    test_page_copy()
    test_build_check()
    test_render_states()
    test_admit_fixtures()
    test_shelf_rules_in_instructions()
    failed = [n for n, ok, _ in RESULTS if not ok]
    print("-" * 60)
    print("SUMMARY:", "ALL PASS (%d scenarios)" % len(RESULTS) if not failed else ("FAIL: " + ", ".join(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
