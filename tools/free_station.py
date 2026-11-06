#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DeepSeekHarness 免费全家桶可选安装器（只装官方源，逐项审批，失败即停）。

注册表：.dsh/free-station.json（数据文件；新工具=加一条目+发 patch，机制不变）

用法:
  python -X utf8 tools/free_station.py plan              # 检测缺什么（零改动）
  python -X utf8 tools/free_station.py status            # 每件装/缺状态
  python -X utf8 tools/free_station.py install           # 逐项问 y/N 后安装（交互终端）
  python -X utf8 tools/free_station.py install --yes     # 仅在 DSH 已逐项征得用户同意后使用
  python -X utf8 tools/free_station.py install <id> --yes  # 只装指定条目
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

REGISTRY = ".dsh/free-station.json"


def load_registry(path=REGISTRY):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def platform_key():
    if sys.platform.startswith("win"):
        return "windows"
    if sys.platform == "darwin":
        return "macos"
    return "linux"


def plan(registry, runner, key=None):
    """返回 [(id, name, state, detail)]；只检测，不改任何东西。"""
    key = key or platform_key()
    rows = []
    for t in registry.get("tools", []):
        cmd = (t.get("verify") or {}).get(key)
        if not cmd:
            manual = t.get("manual") or "该平台未提供官方一键方式"
            rows.append((t["id"], t["name"], "unsupported", manual))
            continue
        ok = runner(cmd) == 0
        rows.append((t["id"], t["name"], "installed" if ok else "missing", " ".join(cmd)))
    return rows


def install_tools(registry, ids, yes, runner, approve, key=None):
    """逐件：已装跳过；无官方方式跳过；未同意跳过；安装失败或装后验证失败即停。
    返回 (results, exit_code)。"""
    key = key or platform_key()
    results = []
    tools = [t for t in registry.get("tools", []) if (not ids) or t["id"] in ids]
    for t in tools:
        vcmd = (t.get("verify") or {}).get(key)
        if vcmd and runner(vcmd) == 0:
            results.append((t["id"], "already", ""))
            continue
        inst = (t.get("install") or {}).get(key)
        if not inst:
            manual = t.get("manual") or "该平台未提供官方一键方式"
            results.append((t["id"], "unsupported", manual))
            continue
        if not yes and not approve(t["name"]):
            results.append((t["id"], "skipped", "未同意"))
            continue
        rc = runner(inst)
        if rc != 0:
            results.append((t["id"], "failed", "install exit %d" % rc))
            return results, 1
        if vcmd and runner(vcmd) != 0:
            results.append((t["id"], "failed", "装后验证失败"))
            return results, 1
        results.append((t["id"], "installed", ""))
    return results, 0


def refresh_path(key=None):
    """Windows：把注册表里的机器/用户 PATH（expandvars 展开）并入当前 PATH 返回；
    非 Windows 原样返回当前 PATH。
    CreateProcess 查找可执行文件用的是父进程的 PATH 快照，给 subprocess 传 env
    不改变查找结果——所以新装的命令要用 shutil.which 换全路径执行。"""
    key = key or platform_key()
    cur = os.environ.get("PATH", "")
    if key != "windows":
        return cur
    parts = [p for p in cur.split(os.pathsep) if p]
    try:
        import winreg
        targets = (
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
            (winreg.HKEY_CURRENT_USER, "Environment"),
        )
        for hkey, sub in targets:
            try:
                with winreg.OpenKey(hkey, sub) as k:
                    val, _ = winreg.QueryValueEx(k, "Path")
                for p in os.path.expandvars(str(val)).split(os.pathsep):
                    p = p.strip()
                    if p and p not in parts:
                        parts.append(p)
            except OSError:
                pass
    except ImportError:
        pass
    return os.pathsep.join(parts)


def resolve_cmd(cmd):
    """把命令首项换成可执行的全路径：python 用当前解释器（macOS/Linux 可能没有 python 命令），其余走 shutil.which。"""
    if cmd and cmd[0] == "python":
        return [sys.executable] + list(cmd[1:])
    full = shutil.which(cmd[0], path=refresh_path())
    if not full:
        return None
    return [full] + list(cmd[1:])


def _runner(cmd, timeout=1800):
    resolved = resolve_cmd(cmd)
    if resolved is None:
        print("  [run] %s -> 未找到该命令（视为缺）" % " ".join(cmd))
        return 1
    try:
        r = subprocess.run(resolved, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout)
    except FileNotFoundError:
        print("  [run] %s -> 未找到该命令（视为缺）" % " ".join(cmd))
        return 1
    if r.returncode != 0:
        tail = ((r.stderr or "").strip() or (r.stdout or "").strip())[:120]
        print("  [run] %s -> %d%s" % (" ".join(resolved), r.returncode, (" | " + tail) if tail else ""))
    return r.returncode


def main(argv=None):
    ap = argparse.ArgumentParser(prog="free_station.py", description="免费全家桶可选安装器")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("plan", help="只检测，零改动")
    sub.add_parser("status", help="每件装/缺状态")
    i = sub.add_parser("install", help="逐项审批后安装（官方源，失败即停）")
    i.add_argument("ids", nargs="*", help="只装指定条目 id；缺省全部")
    i.add_argument("--yes", action="store_true", help="仅在 DSH 已逐项征得用户同意后使用")
    args = ap.parse_args(argv)
    registry = load_registry()
    key = platform_key()

    if args.cmd in ("plan", "status"):
        labels = {"installed": "已装", "missing": "缺", "unsupported": "无官方一键方式"}
        for tid, name, state, detail in plan(registry, _runner, key):
            print("%-12s %-26s %s%s" % (tid, name, labels[state], (" (" + detail + ")") if detail else ""))
        for z in registry.get("zero_install", []):
            print("%-12s %-26s 零安装（%s）" % (z["id"], z["name"], z["how"]))
        if args.cmd == "plan":
            print("以上只检测，不改任何东西。安装：python -X utf8 tools/free_station.py install（逐项审批）")
        return 0

    def approve(name):
        if sys.stdin.isatty():
            a = input("  需要安装: %s [y/N] " % name)
            return a.strip().lower() == "y"
        print("  需要安装: %s —— 未确认（--yes 未给出且非交互终端），已停止。" % name)
        return False

    results, rc = install_tools(registry, args.ids, args.yes, _runner, approve, key)
    labels = {"already": "已装", "installed": "已装好", "skipped": "跳过", "failed": "失败", "unsupported": "无官方一键方式"}
    for tid, state, detail in results:
        print("%-12s %s%s" % (tid, labels.get(state, state), (" " + detail) if detail else ""))
    print("零安装：%s" % "；".join(z["name"] for z in registry.get("zero_install", [])))
    if key == "windows" and any(state == "installed" for _, state, _ in results):
        print("提示：新装的命令要重启 DSH 后才会在 DSH 自己的终端里可用。")
    return rc


if __name__ == "__main__":
    sys.exit(main())
