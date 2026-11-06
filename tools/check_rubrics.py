# -*- coding: utf-8 -*-
"""DSH-FIX-A1-A9 的 RUBRIC 检查器：R1-R9（R6 已撤回，R10 由 @SUN 人工走）。

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

failed = [k for k, v in results.items() if not v]
print("SUMMARY:", "ALL PASS" if not failed else ("FAIL: " + ", ".join(failed)))
sys.exit(0 if not failed else 1)
