# -*- coding: utf-8 -*-
"""市场行为测试（纯标准库 + 本机 git，零网络）。

场景：registry 结构；三条 skill 清单过校验器且 linted>=1；sha 漂移检测；
mem-forever 围栏副本逐字一致；index.json 守官方格式 1；bundle 集合一致；
市场页行区与零外部加载；market_build --check；market_admit 三个 git 夹具
（ADMIT / REJECT 无清单 / REJECT 无 dsh.bundle）。

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


def test_registry_structure():
    r = load_json("docs/market/registry.json")
    ok = r.get("format") == 1 and "en" in r["title"] and "zh" in r["title"] \
        and isinstance(r.get("gate"), dict) and all(k in r["gate"] for k in ("manifest", "validator", "pin", "license", "veto")) \
        and r.get("ranking") == "none"
    entries = r["entries"]
    names = [e["name"] for e in entries]
    skills = [e for e in entries if e.get("kind") == "skill"]
    ok = ok and len(names) == len(set(names)) and {"mem-forever", "site-design-engine", "deai"} <= set(names) \
        and all(e.get("kind") in ("skill", "bundle") for e in entries) \
        and all(all(k in e for k in ("name", "title", "description", "version", "author", "license", "manifest", "procedure", "sha256_lf", "validated")) for e in skills) \
        and all("zh" in e["description"] and "en" in e["description"] for e in skills)
    check("registry_structure", ok)


def test_skill_manifests_validator():
    r = load_json("docs/market/registry.json")
    ok = True
    for e in [x for x in r["entries"] if x.get("kind") == "skill"]:
        p = os.path.join(ROOT, e["manifest"])
        text = read(e["manifest"])
        if text.count("::ILANG::v5.0") < 1:
            ok = False
            break
        res = subprocess.run([PY, "-B", "-X", "utf8", os.path.join(ROOT, "tools", "ilang_grammar_validator.py"),
                              "--lint", p, "--strict"], capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
        m = re.search(r"linted=([0-9]+)", res.stdout + res.stderr)
        if res.returncode != 0 or int(m.group(1) if m else 0) < 1:
            ok = False
            break
    check("skill_manifests_validator", ok)


def test_sha_drift():
    r = load_json("docs/market/registry.json")
    bad = [e["name"] for e in r["entries"] if e.get("kind") == "skill"
           and lf_sha256(os.path.join(ROOT, e["manifest"])) != e.get("sha256_lf")]
    check("sha_drift", not bad, "bad=%s" % bad)


def test_mem_forever_fence_copy():
    gene_re = re.compile(r"::GENE[{]mem-forever[^\n]*\n(?:[ \t]+[TA]:[^\n]*\n)+")
    a = gene_re.search(read(".dsh/skills/mem-forever/SKILL.md")).group(0).strip()
    b = gene_re.search(read(".dsh/skills/mem-forever/MARKET.md")).group(0).strip()
    check("mem_forever_fence_copy", a == b and a.count("\n") >= 15)


def test_index_rules():
    i = load_json("docs/market/index.json")
    r = load_json("docs/market/registry.json")
    B = {e["name"] for e in r["entries"] if e.get("kind") == "bundle"}
    plugins = i["plugins"]
    names = [p["name"] for p in plugins]
    md = i.get("metadata", {})
    lab = md.get("labels", {})
    ok = i.get("format") == 1 and "en" in i["title"] and "zh" in i["title"] \
        and "en" in i.get("description", {}) and "zh" in i.get("description", {}) \
        and "ilang" in lab and "en" in lab["ilang"]["title"] \
        and not md.get("sortKeys") and not md.get("categories") \
        and set(names) == B and len(names) == len(set(names))
    for p in plugins:
        ok = ok and isinstance(p.get("versions"), list) and p["versions"] \
            and not p.get("metadata", {}).get("sortKeys") \
            and "ilang" in p.get("metadata", {}).get("labels", []) \
            and set(p["metadata"].get("labels", [])) <= set(lab)
        for v in p["versions"]:
            ok = ok and isinstance(v.get("publishTimestamp"), int) \
                and isinstance(v.get("version"), str) and v["version"].strip() \
                and isinstance(v.get("engines", {}).get("dsh"), str) \
                and v["engines"]["dsh"].strip() \
                and (v["source"].get("type") == "npm" or
                     (v["source"].get("type") == "git"
                      and v["source"]["url"].startswith("https://")
                      and re.fullmatch("[0-9a-f]{40}", v["source"].get("commit", ""))))
    check("index_rules", ok)


def test_bundle_name_parity():
    i = load_json("docs/market/index.json")
    r = load_json("docs/market/registry.json")
    B = {e["name"] for e in r["entries"] if e.get("kind") == "bundle"}
    check("bundle_name_parity", {p["name"] for p in i["plugins"]} == B)


def test_page_rows():
    r = load_json("docs/market/registry.json")
    m = read("docs/market/index.html")
    ext = re.findall(r"<a [^>]*href=['\"]https?://[^'\"]*['\"][^>]*>", m)
    ok = all(e["name"] in m for e in r["entries"]) \
        and "https://dsh.ilang.guide/market/index.json" in m \
        and "market:skills" in m and "market:bundles" in m \
        and "<script src=" not in m \
        and not re.search(r"<link [^>]*href=['\"]https?://", m) \
        and "@import" not in m \
        and bool(ext) and all("target=" in a and "_blank" in a for a in ext) \
        and "0 个" not in m and "0个" not in m and "暂无" not in m
    check("page_rows", ok, "ext=%d" % len(ext))


def test_build_check():
    res = subprocess.run([PY, "-B", "-X", "utf8", os.path.join(ROOT, "tools", "market_build.py"), "--check"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
    check("build_check", res.returncode == 0, res.stdout.strip()[-120:])


def make_fixture(name, package, license_file=True, manifest=None):
    """建一个临时 git 仓库；manifest 为 None 则不写清单文件。"""
    tmp = tempfile.mkdtemp(prefix="market-fixture-%s-" % name)
    with open(os.path.join(tmp, "package.json"), "w", encoding="utf-8") as f:
        json.dump(package, f, ensure_ascii=False)
    if license_file:
        with open(os.path.join(tmp, "LICENSE"), "w", encoding="utf-8") as f:
            f.write("MIT License\nCopyright (c) 2026 test\n")
    if manifest is not None:
        with open(os.path.join(tmp, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write(manifest)
    subprocess.run([GIT, "init", "-q", "-b", "main"], cwd=tmp, check=True)
    subprocess.run([GIT, "config", "user.email", "test@example.com"], cwd=tmp, check=True)
    subprocess.run([GIT, "config", "user.name", "test"], cwd=tmp, check=True)
    subprocess.run([GIT, "add", "-A"], cwd=tmp, check=True)
    subprocess.run([GIT, "commit", "-q", "-m", "fixture"], cwd=tmp, check=True)
    subprocess.run([GIT, "tag", "v1.0.0"], cwd=tmp, check=True)
    return tmp


def run_admit(repo, ref):
    res = subprocess.run([PY, "-B", "-X", "utf8", os.path.join(ROOT, "tools", "market_admit.py"), repo, ref],
                         capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
    return res


MANIFEST_OK = """# test skill

```ilang
::ILANG::v5.0
::GENE{test|v:1.0|spec:ilang-v5.0}
  T:test_trait
  A:test_anti⇒forbidden
```
"""

PKG_OK = {
    "name": "test-bundle", "version": "1.0.0", "license": "MIT",
    "description": "A test bundle.", "author": "tester",
    "engines": {"dsh": ">=0.2.1 <0.3.0"},
    "dsh": {"bundle": True},
}


def test_admit_fixtures():
    tmp_a = make_fixture("admit", dict(PKG_OK), manifest=MANIFEST_OK)
    tmp_b = make_fixture("nomanifest", dict(PKG_OK), manifest=None)
    pkg_c = dict(PKG_OK)
    del pkg_c["dsh"]
    tmp_c = make_fixture("nobundle", pkg_c, manifest=MANIFEST_OK)
    try:
        ra = run_admit(tmp_a, "v1.0.0")
        rb = run_admit(tmp_b, "v1.0.0")
        rc = run_admit(tmp_c, "v1.0.0")
        ok = ra.returncode == 0 and "ADMIT" in ra.stdout \
            and rb.returncode == 1 and "REJECT" in rb.stdout \
            and rc.returncode == 1 and "REJECT" in rc.stdout
        check("admit_fixtures", ok,
              "admit=%d no_manifest=%d no_bundle=%d" % (ra.returncode, rb.returncode, rc.returncode))
        if rb.returncode != 1:
            print("   no-manifest out:", rb.stdout[-200:])
    finally:
        for t in (tmp_a, tmp_b, tmp_c):
            shutil.rmtree(t, ignore_errors=True)


def main():
    os.chdir(ROOT)
    test_registry_structure()
    test_skill_manifests_validator()
    test_sha_drift()
    test_mem_forever_fence_copy()
    test_index_rules()
    test_bundle_name_parity()
    test_page_rows()
    test_build_check()
    test_admit_fixtures()
    failed = [n for n, ok, _ in RESULTS if not ok]
    print("-" * 60)
    print("SUMMARY:", "ALL PASS (%d scenarios)" % len(RESULTS) if not failed else ("FAIL: " + ", ".join(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
