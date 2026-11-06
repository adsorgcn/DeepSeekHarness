# -*- coding: utf-8 -*-
"""free_station.py 行为测试（纯标准库、注入式 runner、零真实安装）。

覆盖：plan 检测已装/缺/无官方方式；install 已装跳过；未同意跳过且不执行安装；
--yes 安装并验证；装后验证失败即停；安装失败即停且不再继续后续条目。

用法: python -X utf8 tools/test_free_station.py （工作目录=仓库根）
"""
import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_fs():
    spec = importlib.util.spec_from_file_location("free_station", os.path.join(ROOT, "tools", "free_station.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


FS = load_fs()
REGISTRY = json.load(open(os.path.join(ROOT, ".dsh", "free-station.json"), encoding="utf-8"))
RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print("[%s] %s %s" % (name, "PASS" if cond else "FAIL", detail))


class FakeRunner:
    """cmd tuple -> exit code；未映射的命令缺省 1（视为缺），记录调用。"""

    def __init__(self, results=None):
        self.results = dict(results or {})
        self.calls = []

    def __call__(self, cmd, timeout=1800):
        self.calls.append(tuple(cmd))
        return self.results.get(tuple(cmd), 1)


def test_plan_detects():
    r = FakeRunner({("ffmpeg", "-version"): 0})
    rows = dict((row[0], row[2]) for row in FS.plan(REGISTRY, r, "windows"))
    check("plan_detects", rows.get("ffmpeg") == "installed" and rows.get("yt-dlp") == "missing",
          str(rows))


def test_unsupported_platform():
    r = FakeRunner()
    rows = dict((row[0], row[2]) for row in FS.plan(REGISTRY, r, "linux"))
    check("unsupported_platform", rows.get("obsidian") == "unsupported", str(rows.get("obsidian")))


def test_install_skips_without_approval():
    r = FakeRunner()
    results, rc = FS.install_tools(REGISTRY, ["ffmpeg"], False, r, lambda name: False, "windows")
    ran_install = any(c[0] == "winget" for c in r.calls)
    check("approval_required", rc == 0 and results[0][1] == "skipped" and not ran_install,
          str(results))


def test_install_yes_runs_and_verifies():
    # 状态化：装前 verify 失败，装后 verify 通过
    def r(cmd, timeout=1800):
        if tuple(cmd) == ("ffmpeg", "-version"):
            r.count = getattr(r, "count", 0) + 1
            return 0 if r.count >= 2 else 1
        return 0
    results, rc = FS.install_tools(REGISTRY, ["ffmpeg"], True, r, lambda name: True, "windows")
    check("install_and_verify", rc == 0 and results[0][1] == "installed", str(results))


def test_verify_fail_stops():
    def r(cmd, timeout=1800):
        return 1 if tuple(cmd) == ("ffmpeg", "-version") else 0
    results, rc = FS.install_tools(REGISTRY, ["ffmpeg"], True, r, lambda name: True, "windows")
    check("verify_fail_stops", rc == 1 and results[0][1] == "failed", str(results))


def test_install_fail_stops_rest():
    def r(cmd, timeout=1800):
        if tuple(cmd) == ("yt-dlp", "--version"):
            return 1
        if tuple(cmd)[0] == "winget" and "yt-dlp.yt-dlp" in tuple(cmd):
            return 2
        return 0
    results, rc = FS.install_tools(REGISTRY, None, True, r, lambda name: True, "windows")
    first = results[0]
    check("install_fail_stops", rc == 1 and first[1] == "failed" and len(results) == 1,
          str(results))


def test_obsidian_windows_via_winget():
    t = {x["id"]: x for x in REGISTRY["tools"]}
    v = t["obsidian"]["verify"]["windows"]
    ok = v[:5] == ["winget", "list", "--id", "Obsidian.Obsidian", "-e"]
    check("obsidian_windows_via_winget", ok, str(v))


def test_path_refresh():
    r_win = FS.refresh_path("windows")
    ok1 = os.environ.get("PATH", "") in r_win
    r_other = FS.refresh_path("linux")
    ok2 = r_other == os.environ.get("PATH", "")
    check("path_refresh", ok1 and ok2, "win_contains=%s nonwin_equal=%s" % (ok1, ok2))


def test_no_local_model():
    raw = open(os.path.join(ROOT, ".dsh", "free-station.json"), encoding="utf-8").read()
    ids = {x["id"] for x in REGISTRY["tools"]}
    ok = not (ids & {"ollama", "qwen3-8b"}) and "ollama" not in raw.lower()
    check("no_local_model", ok, "ids=%s" % sorted(ids))


def test_asr_entry():
    t = {x["id"]: x for x in REGISTRY["tools"]}
    e = t["sherpa-onnx"]
    ok = all(e["install"][k][:2] == ["python", "tools/asr_setup.py"]
             and e["verify"][k][:3] == ["python", "tools/asr_setup.py", "--check"]
             for k in ("windows", "macos", "linux"))
    ok = ok and "160MB" in e["why"]
    check("asr_entry", ok, str(e["why"]))


def test_python_token():
    out = FS.resolve_cmd(["python", "tools/asr_setup.py", "--check"])
    check("python_token", out == [sys.executable, "tools/asr_setup.py", "--check"], str(out))


def test_already_skips_install():
    r = FakeRunner({("yt-dlp", "--version"): 0})
    results, rc = FS.install_tools(REGISTRY, ["yt-dlp"], True, r, lambda name: True, "windows")
    ran_install = any(c[0] == "winget" for c in r.calls)
    check("already_skips", rc == 0 and results[0][1] == "already" and not ran_install,
          str(results))


def main():
    os.chdir(ROOT)
    test_plan_detects()
    test_unsupported_platform()
    test_install_skips_without_approval()
    test_install_yes_runs_and_verifies()
    test_verify_fail_stops()
    test_install_fail_stops_rest()
    test_obsidian_windows_via_winget()
    test_path_refresh()
    test_no_local_model()
    test_asr_entry()
    test_python_token()
    test_already_skips_install()
    failed = [n for n, ok, _ in RESULTS if not ok]
    print("-" * 60)
    print("SUMMARY:", "ALL PASS (%d scenarios)" % len(RESULTS) if not failed else ("FAIL: " + ", ".join(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
