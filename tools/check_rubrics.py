# -*- coding: utf-8 -*-
"""DSH-FIX-A1-A9 的 RUBRIC 检查器：R1-R9、R11 与 R12（R6 已撤回，R10 由 @SUN 人工走）。

用法: python -X utf8 tools/check_rubrics.py
每项打印「R<n> PASS/FAIL + 命令输出原文」。
"""
import io
import json
import re
import subprocess
import sys

PY = sys.executable
OK = 0


def run(cmd, **kw):
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    out = (p.stdout or "") + (p.stderr or "")
    return p.returncode, out.strip()


def check(name, cmd, expect=0):
    code, out = run(cmd)
    passed = (code == expect)
    print(f"[{name}] {'PASS' if passed else 'FAIL'} (exit={code}, expect={expect})")
    if out:
        print(out)
    print("-" * 60)
    return passed


results = {}

# R1
code, out = run([PY, "-X", "utf8", "tools/ilang_grammar_validator.py", "--lint", "soul/agent.md", "--strict"])
results["R1"] = code == 0
print(f"[R1] {'PASS' if results['R1'] else 'FAIL'} (exit={code}, expect=0)")
print(out)
print("-" * 60)

# R2
code, out = run([PY, "-X", "utf8", "tools/brain.py", "check"])
results["R2"] = code == 0
print(f"[R2] {'PASS' if results['R2'] else 'FAIL'} (exit={code}, expect=0)")
print(out)
print("-" * 60)

# R3
s = io.open("dsh-新手起手式.md", encoding="utf-8").read()
bad = [w for w in ("relayAPI", "hvoy.ai", "runtime/full") if w in s]
results["R3"] = not bad
print(f"[R3] {'PASS' if results['R3'] else 'FAIL'} (forbidden found: {bad or 'none'})")
print("-" * 60)

# R4：仓库自己的标题必须是 DeepSeekHarness（references 里引用 Mem-Forever 是合法的）
c = io.open("CITATION.cff", encoding="utf-8").read()
z = json.load(io.open(".zenodo.json", encoding="utf-8"))
c_lines = c.splitlines()
title_line = next((ln for ln in c_lines if ln.startswith("title:")), "")
ok4 = (
    "DeepSeekHarness" in title_line
    and "adsorgcn/DeepSeekHarness" in c
    and not any(ln.startswith("title:") and "Mem-Forever" in ln for ln in c_lines)
    and "DeepSeekHarness" in z["title"]
    and any(r.get("identifier") == "10.5281/zenodo.22865160" for r in z.get("related_identifiers", []))
)
results["R4"] = ok4
print(f"[R4] {'PASS' if ok4 else 'FAIL'}")
print("-" * 60)

# R5
s = io.open(".github/workflows/upstream-sync.yml", encoding="utf-8").read()
bad5 = [w for w in ("AGENTS.md", "CLAUDE.md") if w in s]
results["R5"] = not bad5
print(f"[R5] {'PASS' if results['R5'] else 'FAIL'} (forbidden found: {bad5 or 'none'})")
print("-" * 60)

# R7
s = io.open("docs/index.html", encoding="utf-8").read()
ext = re.findall(r'<a [^>]*href="https?://[^>]*>', s)
ok7 = bool(ext) and all('target="_blank"' in a for a in ext)
results["R7"] = ok7
print(f"[R7] {'PASS' if ok7 else 'FAIL'} (external links: {len(ext)})")
print("-" * 60)

# R8
import os as _os
bash = "bash"
for cand in ("C:\\Program Files\\Git\\bin\\bash.exe", "/usr/bin/bash", "/bin/bash"):
    if _os.path.exists(cand):
        bash = cand
        break
code, out = run([bash, "-n", "bootstrap.sh"])
results["R8"] = code == 0
print(f"[R8] {'PASS' if results['R8'] else 'FAIL'} (exit={code}, expect=0)")
print(out)
print("-" * 60)

# R9：客服防重复/配额/校验必须真实存在（AST 检查常量与关键机制，不再是字符串存在性）
import ast as _ast
b = io.open(".github/bot/issue_bot.py", encoding="utf-8").read()
w = io.open(".github/workflows/issue-bot.yml", encoding="utf-8").read()
ok9 = True
reasons = []
tree = _ast.parse(b)
caps = {}
for node in tree.body:
    if isinstance(node, _ast.Assign):
        for t in node.targets:
            if isinstance(t, _ast.Name) and t.id in ("DAILY_CAP", "PER_ISSUE_CAP", "BOOK_MAX_CHARS", "ANSWER_MAX_CHARS"):
                try:
                    caps[t.id] = _ast.literal_eval(node.value)
                except Exception:
                    caps[t.id] = None
for k in ("DAILY_CAP", "PER_ISSUE_CAP", "BOOK_MAX_CHARS", "ANSWER_MAX_CHARS"):
    v = caps.get(k)
    if not isinstance(v, int) or v <= 0:
        ok9 = False
        reasons.append("%s not a positive int constant" % k)
for needle in ("dsh-event:", 'rel="next"', '!= "open"', "finish_reason"):
    if needle not in b:
        ok9 = False
        reasons.append("missing %r" % needle)
if "issue.number" not in w or "cancel-in-progress" not in w:
    ok9 = False
    reasons.append("concurrency not per-issue")
results["R9"] = ok9
print(f"[R9] {'PASS' if ok9 else 'FAIL'} ({'; '.join(reasons) if reasons else 'constants, event dedup, pagination, live recheck, per-issue concurrency verified'})")
print("-" * 60)

# R11：地板钉在三个文件里，工具包自己的脚本里没有门
soul_t = io.open("soul/agent.md", encoding="utf-8").read()
guide_t = io.open("一键安装.md", encoding="utf-8").read()
readme_t = io.open("README.md", encoding="utf-8").read()
soul_ok = soul_t.count("::GENE{floor|conf:confirmed|scope:global}") == 1 \
    and "T:the_kit_adds_no_gate_of_its_own" in soul_t \
    and "A:a_wall_before_the_other_road" in soul_t
guide_ok = "工具包自己不设门" in guide_t and "原话" in guide_t and "另一条路" in guide_t
readme_ok = "工具包自己不设门" in readme_t and "另一条路" in readme_t
gate_words = ("激活码", "授权码", "许可证", "license_key", "LICENSE_KEY", "余额不足", "地区不支持")
hits11 = []
for _p in ("bootstrap.ps1", "bootstrap.sh", "tools/free_station.py", "server/worker.mjs", "server/content.mjs"):
    try:
        _t = io.open(_p, encoding="utf-8", errors="replace").read()
    except OSError:
        continue
    for _w in gate_words:
        if _w in _t:
            hits11.append("%s:%s" % (_p, _w))
ok11 = soul_ok and guide_ok and readme_ok and not hits11
results["R11"] = ok11
print(f"[R11] {'PASS' if ok11 else 'FAIL'} (soul={soul_ok}, guide={guide_ok}, readme={readme_ok}, gate words found: {hits11 or 'none'})")
print("-" * 60)

# R12：SEO 体检书钉在书、货架、入口三处，四条边界都在
import os as _os12
seo_book_path = ".dsh/books/seo/BOOK.md"
seo_book_ok = _os12.path.isfile(seo_book_path)
if seo_book_ok:
    seo_book_t = io.open(seo_book_path, encoding="utf-8").read()
    seo_book_ok = seo_book_t.startswith("::ILANG::v5.0::ENGINEERING_BOOK") \
        and seo_book_t.rstrip().endswith("::ILANG::v5.0::ENGINEERING_BOOK") \
        and "[ID:DSH-SEO]" in seo_book_t \
        and all(s in seo_book_t for s in (
            "never:fetch_or_scrape_a_google_search_result_page",
            "never:generate_pages_in_bulk",
            "never:create_buy_exchange_or_automatically_submit_a_link",
            "never:deploy_or_touch_the_live_site"))
seo_reg_t = io.open("docs/market/registry.json", encoding="utf-8").read()
seo_reg = json.loads(seo_reg_t)
seo_entries = [e for e in seo_reg["entries"] if e.get("name") == "seo"]
seo_registry_ok = len(seo_entries) == 1 \
    and seo_entries[0].get("kind") == "book" \
    and seo_entries[0].get("say") == "SEO 体检" \
    and seo_entries[0].get("admitted_by") == "@SUN" \
    and seo_entries[0].get("manifest") == ".dsh/books/seo/BOOK.md"
seo_agents_t = io.open("AGENTS.local.md", encoding="utf-8").read()
seo_agents_ok = "T:the_trigger_phrase_of_.dsh/books/seo/BOOK.md_is_written_in_the_note_below" in seo_agents_t \
    and "SEO 体检" in seo_agents_t
ok12 = seo_book_ok and seo_registry_ok and seo_agents_ok
results["R12"] = ok12
print(f"[R12] {'PASS' if ok12 else 'FAIL'} (book={seo_book_ok}, registry={seo_registry_ok}, agents={seo_agents_ok})")
print("-" * 60)

failed = [k for k, v in results.items() if not v]
print("SUMMARY:", "ALL PASS" if not failed else ("FAIL: " + ", ".join(failed)))
sys.exit(0 if not failed else 1)
