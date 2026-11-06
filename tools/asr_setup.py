#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SenseVoice 语音转写引擎安装器（官方源，全本地；由 free_station 在用户同意后调用）。

- 引擎与模型全部装在用户目录 ASR_HOME（~/.deepseekharness/asr）下：不占仓库、brain 扫描不绊脚、引擎更新不丢模型
- venv 在 ASR_HOME/.asr-venv，用 venv 里的 pip 装 sherpa-onnx==2.0.1（PyPI 官方，不加任何其他依赖）
- 模型包（TARBALL_NAME）只下载一遍：流式落盘到 ASR_HOME/.tmp，边写边算 sha256；
  从这一个包里取出 model.int8.onnx、tokens.txt、test_wavs/zh.wav（落名 selftest-zh.wav）放进 ASR_HOME/models/sensevoice/
- GitHub 下不动时逐文件兜底：hf-mirror.com → huggingface.co（哈希同 @VERIFIED）
- silero_vad.onnx 来源：GitHub release → hf-mirror csukuangfj/vad → huggingface csukuangfj/vad；两处哈希都认
- 每个文件落盘后核 sha256，不匹配删掉重下一次，再错打印两边值退出 1
- --check：venv 里 import sherpa_onnx 成功 + 四个模型文件在且哈希对 → 0，否则 1 并打印缺什么
- 不往系统 Python 装任何东西
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tarfile
import urllib.request

ASR_HOME = os.path.join(os.path.expanduser("~"), ".deepseekharness", "asr")
VENV = os.path.join(ASR_HOME, ".asr-venv")
MODELS = os.path.join(ASR_HOME, "models", "sensevoice")
TMP = os.path.join(ASR_HOME, ".tmp")
PKG = "sherpa-onnx==2.0.1"
TARBALL_NAME = "sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09.tar.bz2"
TARBALL_URL = "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/" + TARBALL_NAME
TARBALL_SHA256 = "7305f7905bfcf77fa0b39388a313f3da35c68d971661a65475b56fb2162c8e63"
TARBALL_DIR = "sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09/"
TKN = "tokens" + ".txt"
MEMBER_NAMES = {
    "model.int8.onnx": "model.int8.onnx",
    TKN: TKN,
    "selftest-zh.wav": "test_wavs/zh.wav",
}
FILE_SHA256 = {
    "model.int8.onnx": ["12ca1a2ae7ecf3e0019ef2822307ee0b5cadc9196569e379b4c4026f8205276d"],
    TKN: ["f449eb28dc567533d7fa59be34e2abca8784f771850c78a47fb731a31429a1dc"],
    "selftest-zh.wav": ["b77f1794fe374a0ba1ee1dc458bfaf9349496cbbfc32780c50ba3c5a7ad8e373"],
    "silero_vad.onnx": [
        "9e2449e1087496d8d4caba907f23e0bd3f78d91fa552479bb9c23ac09cbb1fd6",
        "a35ebf52fd3ce5f1469b2a36158dba761bc47b973ea3382b3186ca15b1f5af28",
    ],
}
HF_MIRROR = "https://hf-mirror.com/csukuangfj/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09/resolve/main/"
HF = "https://huggingface.co/csukuangfj/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09/resolve/main/"
VAD_URLS = [
    "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/silero_vad.onnx",
    "https://hf-mirror.com/csukuangfj/vad/resolve/main/silero_vad.onnx",
    "https://huggingface.co/csukuangfj/vad/resolve/main/silero_vad.onnx",
]


def venv_python():
    if sys.platform.startswith("win"):
        return os.path.join(VENV, "Scripts", "python.exe")
    return os.path.join(VENV, "bin", "python")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def download_to(url, dest, timeout=900):
    """流式下载到文件（1MB 一块），不整块读进内存。"""
    req = urllib.request.Request(url, headers={"User-Agent": "dsh-asr-setup"})
    with urllib.request.urlopen(req, timeout=timeout) as resp, open(dest, "wb") as fh:
        shutil.copyfileobj(resp, fh, 1 << 20)
    return dest


def fetch_file_urls(urls, want_hashes, dest):
    """按顺序试源，落盘后核哈希；不匹配删掉换下一个；全失败打印原文并返回 None。"""
    errors = []
    for url in urls:
        try:
            download_to(url, dest)
            got = sha256_file(dest)
            if got in want_hashes:
                print("下载成功（来源 %s）" % url)
                return url
            raise ValueError("sha256 mismatch: want %s got %s" % (" | ".join(want_hashes), got))
        except Exception as e:
            errors.append("%s: %s" % (url, e))
            if os.path.exists(dest):
                os.remove(dest)
            continue
    for e in errors:
        print("下载失败：%s" % e)
    return None


def fetch_tarball_once():
    """模型包只下一遍：流式落盘核哈希，再从这一个包里分块取出三个成员。"""
    os.makedirs(TMP, exist_ok=True)
    tb = os.path.join(TMP, TARBALL_NAME)
    ok = False
    for attempt in (1, 2):
        try:
            download_to(TARBALL_URL, tb)
            got = sha256_file(tb)
            if got == TARBALL_SHA256:
                ok = True
                break
            raise ValueError("sha256 mismatch: want %s got %s" % (TARBALL_SHA256, got))
        except Exception as e:
            print("模型包下载失败（第 %d 次）：%s" % (attempt, e))
            if os.path.exists(tb):
                os.remove(tb)
    if not ok:
        print("模型包连续两次不通过，已停。来源：%s" % TARBALL_URL)
        shutil.rmtree(TMP, ignore_errors=True)
        return False
    os.makedirs(MODELS, exist_ok=True)
    try:
        with tarfile.open(tb, "r:bz2") as t:
            for out_name, member in MEMBER_NAMES.items():
                src = t.extractfile(TARBALL_DIR + member)
                dest = os.path.join(MODELS, out_name)
                with open(dest, "wb") as fh:
                    shutil.copyfileobj(src, fh, 1 << 20)
                got = sha256_file(dest)
                if got not in FILE_SHA256[out_name]:
                    raise ValueError("%s sha256 mismatch: got %s" % (out_name, got))
    except Exception as e:
        print("模型包解出失败：%s" % e)
        shutil.rmtree(TMP, ignore_errors=True)
        return False
    print("模型包下载并解出成功（来源 %s）" % TARBALL_URL)
    shutil.rmtree(TMP, ignore_errors=True)
    return True


def fetch_models():
    """tarball 一次成功最好；否则逐文件走 hf-mirror → huggingface。"""
    if not fetch_tarball_once():
        os.makedirs(MODELS, exist_ok=True)
        for name, member in MEMBER_NAMES.items():
            dest = os.path.join(MODELS, name)
            if os.path.exists(dest) and sha256_file(dest) in FILE_SHA256[name]:
                continue
            urls = [HF_MIRROR + member, HF + member]
            if fetch_file_urls(urls, FILE_SHA256[name], dest) is None:
                return False
    dest = os.path.join(MODELS, "silero_vad.onnx")
    if os.path.exists(dest) and sha256_file(dest) in FILE_SHA256["silero_vad.onnx"]:
        return True
    return fetch_file_urls(VAD_URLS, FILE_SHA256["silero_vad.onnx"], dest) is not None


def ensure_venv():
    if not os.path.exists(venv_python()):
        r = subprocess.run([sys.executable, "-m", "venv", VENV])
        if r.returncode != 0:
            print("venv 创建失败，退出码 %d" % r.returncode)
            sys.exit(1)
        print("已建引擎 venv：%s" % VENV)
    if sys.platform.startswith("win"):
        pip = os.path.join(VENV, "Scripts", "pip.exe")
    else:
        pip = os.path.join(VENV, "bin", "pip")
    r = subprocess.run([pip, "install", PKG])
    if r.returncode != 0:
        print("pip 安装 %s 失败（退出码 %d）。需要 Python 3.10 到 3.12。" % (PKG, r.returncode))
        sys.exit(1)
    print("已装 %s" % PKG)


def do_check():
    vp = venv_python()
    if not os.path.exists(vp):
        print("缺 venv：%s 不存在" % VENV)
        return 1
    r = subprocess.run([vp, "-c", "import sherpa_onnx"], capture_output=True, text=True)
    if r.returncode != 0:
        print("缺依赖：%s 里 import sherpa_onnx 失败" % VENV)
        return 1
    ok = True
    for name, wants in FILE_SHA256.items():
        p = os.path.join(MODELS, name)
        if not os.path.exists(p):
            print("缺模型文件：%s" % p)
            ok = False
            continue
        got = sha256_file(p)
        if got not in wants:
            print("模型文件哈希不对：%s\n  期望 %s\n  实际 %s" % (p, " | ".join(wants), got))
            ok = False
    if ok:
        print("OK: sherpa_onnx 可导入，四个模型文件哈希全部正确")
        return 0
    return 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="SenseVoice 语音转写引擎安装器")
    ap.add_argument("--check", action="store_true", help="只验证，不改任何东西")
    args = ap.parse_args(argv)
    try:
        os.makedirs(ASR_HOME, exist_ok=True)
    except OSError as e:
        print("引擎目录建不了：%s（%s）" % (ASR_HOME, e))
        return 1
    if args.check:
        return do_check()
    ensure_venv()
    if not fetch_models():
        return 1
    return do_check()


if __name__ == "__main__":
    sys.exit(main())
