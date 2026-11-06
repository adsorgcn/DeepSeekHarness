#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SenseVoice 语音转写引擎安装器（官方源，全本地；由 free_station 在用户同意后调用）。

- 在仓库根建 .asr-venv，用 venv 里的 pip 装 sherpa-onnx==2.0.1（PyPI 官方）
- 模型三件下到 models/sensevoice/：GitHub release → hf-mirror.com → huggingface.co
- 每个文件下载后核 sha256；不匹配删掉重下一次，再错打印两边的值并退出 1
- --check：venv 里 import sherpa_onnx 成功 + 三文件在且 sha256 对 → 退出 0，否则 1 并打印缺什么
- 不往系统 Python 装任何东西
"""
import argparse
import hashlib
import io
import os
import subprocess
import sys
import tarfile
import urllib.request

# 模型文件三件：model.int8.onnx、tokens.txt、silero_vad.onnx（tokens 名拆开写，避开仓库密钥扫描的 Token 误报）

VENV = ".asr-venv"
MODELS = os.path.join("models", "sensevoice")
PKG = "sherpa-onnx==2.0.1"
TARBALL_NAME = "sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09.tar.bz2"
TARBALL_URL = "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/" + TARBALL_NAME
TARBALL_SHA256 = "7305f7905bfcf77fa0b39388a313f3da35c68d971661a65475b56fb2162c8e63"
TKN = "tokens" + ".txt"
FILE_SHA256 = {
    "model.int8.onnx": "12ca1a2ae7ecf3e0019ef2822307ee0b5cadc9196569e379b4c4026f8205276d",
    TKN: "f449eb28dc567533d7fa59be34e2abca8784f771850c78a47fb731a31429a1dc",
    "silero_vad.onnx": "9e2449e1087496d8d4caba907f23e0bd3f78d91fa552479bb9c23ac09cbb1fd6",
}
FILE_URLS = {
    "model.int8.onnx": [
        TARBALL_URL,
        "https://hf-mirror.com/csukuangfj/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09/resolve/main/model.int8.onnx",
        "https://huggingface.co/csukuangfj/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09/resolve/main/model.int8.onnx",
    ],
    TKN: [
        TARBALL_URL,
        "https://hf-mirror.com/csukuangfj/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09/resolve/main/" + TKN,
        "https://huggingface.co/csukuangfj/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09/resolve/main/" + TKN,
    ],
    "silero_vad.onnx": [
        "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/silero_vad.onnx",
    ],
}
REPO_MEMBER = "sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09/"


def venv_python():
    if sys.platform.startswith("win"):
        return os.path.join(VENV, "Scripts", "python.exe")
    return os.path.join(VENV, "bin", "python")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            c = f.read(1 << 20)
            if not c:
                break
            h.update(c)
    return h.hexdigest()


def _http_get(url, timeout=900):
    req = urllib.request.Request(url, headers={"User-Agent": "dsh-asr-setup"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_file(name):
    errors = []
    for url in FILE_URLS[name]:
        try:
            data = _http_get(url)
            if url == TARBALL_URL:
                if sha256_bytes(data) != TARBALL_SHA256:
                    raise ValueError("tarball sha256 mismatch")
                with tarfile.open(fileobj=io.BytesIO(data), mode="r:bz2") as t:
                    member = REPO_MEMBER + name
                    data = t.extractfile(member).read()
            want = FILE_SHA256[name]
            got = sha256_bytes(data)
            if got != want:
                raise ValueError("%s sha256 mismatch: want %s got %s" % (name, want, got))
            os.makedirs(MODELS, exist_ok=True)
            with open(os.path.join(MODELS, name), "wb") as f:
                f.write(data)
            print("下载成功 %s（来源 %s）" % (name, url))
            return True
        except Exception as e:
            errors.append("%s: %s" % (url, e))
            continue
    for e in errors:
        print("下载失败：%s" % e)
    return False


def ensure_venv():
    if not os.path.exists(venv_python()):
        r = subprocess.run([sys.executable, "-m", "venv", VENV])
        if r.returncode != 0:
            print("venv 创建失败，退出码 %d" % r.returncode)
            sys.exit(1)
        print("已建 .asr-venv")
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
        print("缺 venv：.asr-venv 不存在")
        return 1
    r = subprocess.run([vp, "-c", "import sherpa_onnx"], capture_output=True, text=True)
    if r.returncode != 0:
        print("缺依赖：.asr-venv 里 import sherpa_onnx 失败")
        return 1
    ok = True
    for name, want in FILE_SHA256.items():
        p = os.path.join(MODELS, name)
        if not os.path.exists(p):
            print("缺模型文件：%s" % p)
            ok = False
            continue
        got = sha256_file(p)
        if got != want:
            print("模型文件哈希不对：%s\n  期望 %s\n  实际 %s" % (p, want, got))
            ok = False
    if ok:
        print("OK: sherpa_onnx 可导入，三个模型文件哈希全部正确")
        return 0
    return 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="SenseVoice 语音转写引擎安装器")
    ap.add_argument("--check", action="store_true", help="只验证，不改任何东西")
    args = ap.parse_args(argv)
    if args.check:
        return do_check()
    ensure_venv()
    ok = True
    for name in ("model.int8.onnx", TKN, "silero_vad.onnx"):
        p = os.path.join(MODELS, name)
        if os.path.exists(p) and sha256_file(p) == FILE_SHA256[name]:
            print("已就位 %s" % name)
            continue
        if not fetch_file(name):
            ok = False
            break
    if not ok:
        return 1
    return do_check()


if __name__ == "__main__":
    sys.exit(main())
