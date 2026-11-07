# -*- coding: utf-8 -*-
"""deai 技能行为测试（纯标准库、零网络）。

覆盖：manifest（upstream.json 清单与哈希）、pinned（钉死值）、prompt（上游 prompt 关键行）、
manifest_skill（SKILL.md frontmatter 与边界）、lint（六个 iLang 文件严格校验）、
gene（AGENTS.local.md 的 dsh_deai GENE）。

用法: python -X utf8 tools/test_deai.py （工作目录=仓库根）
"""
import hashlib
import io
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(ROOT, ".dsh", "skills", "deai")
UP = os.path.join(SKILL_DIR, "upstream")
PY = sys.executable
RESULTS = []

PINNED = {
    "prompt.md": "9b08d19829b54d78217207a391971e44e6d88f6960d53cdb524c0f1ba0d49f24",
    "SKILL.md": "d3463a670c239988e7d473b4b6d932da6d66809615b46fb223d8c60bea647df6",
    "sun-writing-v1.2-2026-11-06.ilang.md": "6be862ee42ea7e77691eb7a18558fb9cb45f2217258d499688a1dc85f03e7ee8",
    "references/profile-mode-v1.2-2026-11-06.ilang.md": "08acbf7cc81b1e862e96ca0b20966855d3e2e60d9ce14c1db66cb257fd35e421",
    "profiles/sun-v1.1-2026-10-03.ilang.md": "75c107bb6b27b8e61c9f9a0dc28803b3f3175c43556ae2db12a0197ecdb7dcbf",
    "LICENSE": "997f280b0baa4b3f7bc2bd74eae9402d5bde7979ac8990b9939643d5303c24a2",
}


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print("[%s] %s %s" % (name, "PASS" if cond else "FAIL", detail))


def lf_sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read().replace(b"\r\n", b"\n")).hexdigest()


def test_manifest():
    try:
        m = json.load(io.open(os.path.join(SKILL_DIR, "upstream.json"), encoding="utf-8"))
    except Exception as e:
        check("manifest", False, str(e))
        return
    files = m.get("files", {})
    ok = m.get("tag") == "v1.6.0" and len(files) == 11
    if ok:
        for p, v in files.items():
            fp = os.path.join(UP, p)
            if not os.path.exists(fp) or lf_sha256(fp) != v:
                ok = False
                break
    check("manifest", ok, "tag=%s files=%d" % (m.get("tag"), len(files)))


def test_pinned():
    m = json.load(io.open(os.path.join(SKILL_DIR, "upstream.json"), encoding="utf-8"))
    files = m["files"]
    bad = [p for p, v in PINNED.items() if files.get(p) != v]
    check("pinned", not bad, "bad=%s" % bad)


def test_prompt():
    s = io.open(os.path.join(UP, "prompt.md"), encoding="utf-8").read()
    ok = s.startswith("::ILANG::v5.0") and all(k in s for k in (
        "[VERSION:1.4.0]", "STEP_1B_READER_ESTIMATE", "STEP_5B_TONE", "Never propose profanity",
        "Personal figures", "never estimate one")) and "add specific number" not in s
    check("prompt", ok)


def test_manifest_skill():
    s = io.open(os.path.join(SKILL_DIR, "SKILL.md"), encoding="utf-8").read()
    ok = "name: deai" in s and "version: 1.6.0" in s and "license: MIT" in s \
        and "upstream/prompt.md" in s and "profile=SUN" in s and "npx" not in s \
        and "public_figures_searched_with_source_and_date_or_left_as_written" in s \
        and "不往这块写" in s \
        and "估算" not in s and "contextual_estimate" not in s
    check("manifest_skill", ok)


def test_lint():
    files = [
        os.path.join(SKILL_DIR, "SKILL.md"),
        os.path.join(UP, "prompt.md"),
        os.path.join(UP, "SKILL.md"),
        os.path.join(UP, "sun-writing-v1.2-2026-11-06.ilang.md"),
        os.path.join(UP, "references", "profile-mode-v1.2-2026-11-06.ilang.md"),
        os.path.join(UP, "profiles", "sun-v1.1-2026-10-03.ilang.md"),
    ]
    bad = []
    for f in files:
        r = subprocess.run([PY, "-B", "-X", "utf8", os.path.join(ROOT, "tools", "ilang_grammar_validator.py"),
                            "--lint", f, "--strict"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode != 0:
            bad.append(os.path.relpath(f, SKILL_DIR))
    check("lint", not bad, "bad=%s" % bad)


def test_gene():
    s = io.open(os.path.join(ROOT, "AGENTS.local.md"), encoding="utf-8").read()
    check("gene", "::GENE{dsh_deai" in s
          and "applying_the_SUN_profile_to_a_user_who_did_not_name_it" in s
          and "personal_figures_left_as_written_never_estimated" in s
          and "never_ask_the_user_to_fill_them" not in s)


def main():
    os.chdir(ROOT)
    test_manifest()
    test_pinned()
    test_prompt()
    test_manifest_skill()
    test_lint()
    test_gene()
    failed = [n for n, ok, _ in RESULTS if not ok]
    print("-" * 60)
    print("SUMMARY:", "ALL PASS (%d scenarios)" % len(RESULTS) if not failed else ("FAIL: " + ", ".join(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
