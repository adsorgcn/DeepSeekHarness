#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""视频/音频 → 文字 + 字幕（本地 SenseVoice，流程照 k2-fsa/sherpa-onnx 官方 generate-subtitles.py）。

用法:
  python tools/transcribe.py <链接或文件路径> [--lang auto|zh|en|ja|ko|yue] [--threads N]
  python tools/transcribe.py --selftest      # 一句话自检：读引擎目录的 selftest-zh.wav

退出码: 0 成功；2 引擎/模型缺失；3 下载失败；4 没有识别到语音；5 自检文字不符。
输出: media/<名>.txt（整篇）与 media/<名>.srt（分段带时间），打印两个绝对路径。
音频不出本机；允许出现的网络只有 yt-dlp 自己的下载。
仅依赖标准库 + sherpa_onnx。
引擎与模型在用户目录 ASR_HOME（~/.deepseekharness/asr）下，media/ 在仓库根。
"""
import argparse
import array
import glob
import os
import shutil
import subprocess
import sys

ASR_HOME = os.path.join(os.path.expanduser("~"), ".deepseekharness", "asr")
VENV = os.path.join(ASR_HOME, ".asr-venv")
MODELS = os.path.join(ASR_HOME, "models", "sensevoice")
SELFTEST_WAV = os.path.join(MODELS, "selftest-zh.wav")


def venv_python():
    if sys.platform.startswith("win"):
        return os.path.join(VENV, "Scripts", "python.exe")
    return os.path.join(VENV, "bin", "python")


def check_engine_ready(venv_py, models_dir, import_fn=None):
    """引擎/模型缺失返回 2；就绪返回 None。"""
    if not os.path.exists(venv_py):
        print("先装视频转文字引擎：python tools/free_station.py install sherpa-onnx")
        return 2
    if import_fn is None:
        try:
            import sherpa_onnx  # noqa: F401
        except ImportError:
            print("先装视频转文字引擎：python tools/free_station.py install sherpa-onnx")
            return 2
    for f in ("model.int8.onnx", "tokens.txt", "silero_vad.onnx"):
        if not os.path.exists(os.path.join(models_dir, f)):
            print("先装视频转文字引擎：python tools/free_station.py install sherpa-onnx")
            return 2
    return None


def reexec_if_needed():
    """当前解释器不是引擎 venv 里的，就用 venv 的 Python 重新执行自己并透传退出码。"""
    vp = venv_python()
    if os.path.realpath(sys.executable) == os.path.realpath(vp):
        return
    if not os.path.exists(vp):
        print("先装视频转文字引擎：python tools/free_station.py install sherpa-onnx")
        sys.exit(2)
    r = subprocess.run([vp, "-X", "utf8"] + sys.argv)
    sys.exit(r.returncode)


def is_url(x):
    return x.startswith("http://") or x.startswith("https://")


def srt_timestamp(seconds):
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def build_ffmpeg_cmd(src, dst):
    return ["ffmpeg", "-y", "-i", src, "-ac", "1", "-ar", "16000", "-f", "wav", dst]


def refresh_path(key=None):
    """Windows：注册表机器/用户 PATH 并入当前 PATH；非 Windows 原样返回。"""
    key = key or ("windows" if sys.platform.startswith("win") else sys.platform)
    cur = os.environ.get("PATH", "")
    if key != "windows":
        return cur
    parts = [p for p in cur.split(os.pathsep) if p]
    try:
        import winreg
        for hkey, sub in (
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
            (winreg.HKEY_CURRENT_USER, "Environment"),
        ):
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


def resolve_exe(name):
    """找可执行文件：PATH（含注册表刷新）→ WinGet Links → WinGet Packages；找不到返回 None。"""
    full = shutil.which(name, path=refresh_path())
    if full:
        return full
    if sys.platform.startswith("win"):
        local = os.environ.get("LOCALAPPDATA", "")
        for cand_dir in (
            os.path.join(local, "Microsoft", "WinGet", "Links"),
            os.path.join(local, "Microsoft", "WinGet", "Packages"),
        ):
            try:
                for hit in glob.glob(os.path.join(cand_dir, "**", name + ".exe"), recursive=True):
                    return hit
            except OSError:
                pass
    return None


def download_audio(url):
    ytdlp = resolve_exe("yt-dlp")
    if not ytdlp:
        print("找不到 yt-dlp：请先装视频转文字引擎与 yt-dlp（免费全家桶）")
        sys.exit(3)
    out_tpl = os.path.join("media", "%(id)s.%(ext)s")
    tmpdir = os.path.abspath(os.path.join("media", ".ytdlp-tmp"))
    os.makedirs(tmpdir, exist_ok=True)
    env = dict(os.environ)
    env["TMP"] = tmpdir
    env["TEMP"] = tmpdir  # 工作区沙箱下 %TEMP% 不可建目录，PyInstaller 需在工作区内解包
    p = subprocess.run([ytdlp, "-f", "bestaudio", "-o", out_tpl,
                        "--print", "after_move:filepath", url],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=env)
    if p.returncode != 0:
        print(p.stderr.strip())
        sys.exit(3)
    lines = [ln for ln in p.stdout.splitlines() if ln.strip()]
    if not lines:
        print(p.stderr.strip() or "yt-dlp 未返回文件路径")
        sys.exit(3)
    return lines[-1].strip()


def pcm16_to_floats(raw):
    """PCM16 转 float list，只用标准库。"""
    a = array.array("h")
    a.frombytes(raw[: (len(raw) // 2) * 2])
    return [x / 32768.0 for x in a]


def transcribe_wav(wav_path, lang, threads, so=None):
    """照官方 generate-subtitles.py：边喂边取段识别，EOF 后 flush 再取一遍（否则丢最后一段）。"""
    if so is None:
        import sherpa_onnx as so
    import wave

    recognizer = so.OfflineRecognizer.from_sense_voice(
        model=os.path.join(MODELS, "model.int8.onnx"),
        tokens=os.path.join(MODELS, "tokens.txt"),
        num_threads=threads,
        language=lang,
        use_itn=True,
    )
    vad_config = so.VadModelConfig()
    vad_config.silero_vad.model = os.path.join(MODELS, "silero_vad.onnx")
    vad_config.silero_vad.threshold = 0.2
    vad_config.silero_vad.min_silence_duration = 0.25
    vad_config.silero_vad.max_speech_duration = 5
    vad_config.sample_rate = 16000
    vad = so.VoiceActivityDetector(vad_config, buffer_size_in_seconds=100)

    texts = []

    def decode_segment(start, samples):
        stream = recognizer.create_stream()
        stream.accept_waveform(16000, samples)
        recognizer.decode_stream(stream)
        text = (stream.result.text or "").strip()
        if text:
            texts.append((start / 16000.0, (start + len(samples)) / 16000.0, text))

    def drain():
        while not vad.empty():
            segment = vad.front
            start = segment.start
            samples = list(segment.samples)  # 必须在 pop 前拷贝，pop 会抽空
            vad.pop()
            if samples:
                decode_segment(start, samples)

    with wave.open(wav_path, "rb") as f:
        assert f.getframerate() == 16000, "wav 采样率必须是 16000"
        samples_per_read = int(0.1 * 16000)  # 官方例子：每 0.1 秒读一次，读太短会吃掉段首字
        while True:
            raw = f.readframes(samples_per_read)
            if not raw:
                break
            vad.accept_waveform(pcm16_to_floats(raw))
            drain()
    vad.flush()  # 官方例子：EOF 后 flush 一次，吐出最后一段（否则丢尾）
    drain()
    return texts


def main(argv=None):
    ap = argparse.ArgumentParser(description="视频/音频转文字与字幕（本地）")
    ap.add_argument("input", nargs="?", help="链接或本地文件路径（--selftest 时省略）")
    ap.add_argument("--lang", default="auto", choices=("auto", "zh", "en", "ja", "ko", "yue"))
    ap.add_argument("--threads", type=int, default=2)
    ap.add_argument("--selftest", action="store_true", help="跑自检音频并验证引擎可用")
    args = ap.parse_args(argv)

    reexec_if_needed()
    code = check_engine_ready(venv_python(), MODELS)
    if code is not None:
        sys.exit(code)

    if args.selftest:
        import wave
        with wave.open(SELFTEST_WAV, "rb") as f:
            assert f.getframerate() == 16000 and f.getnchannels() == 1, "自检音频必须是 16000 Hz 单声道"
        texts = transcribe_wav(SELFTEST_WAV, "", args.threads)
        joined = "\n".join(t[2] for t in texts)
        print(joined)
        if "开放时间" in joined:
            print("SELFTEST OK")
            return 0
        return 5

    if not args.input:
        ap.error("需要输入链接或文件路径（或加 --selftest）")

    os.makedirs("media", exist_ok=True)
    src = args.input
    if is_url(src):
        src = download_audio(src)

    stem = os.path.splitext(os.path.basename(src))[0]
    if stem.endswith(".16k"):
        stem = stem[:-4]
    wav_path = os.path.join("media", stem + ".16k.wav")
    ffmpeg = resolve_exe("ffmpeg")
    if not ffmpeg:
        print("找不到 ffmpeg：请先装视频转文字引擎与 FFmpeg（免费全家桶）")
        sys.exit(3)
    cmd = build_ffmpeg_cmd(src, wav_path)
    cmd[0] = ffmpeg
    p = subprocess.run(cmd,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print(p.stderr.strip())
        sys.exit(3)

    lang = "" if args.lang == "auto" else args.lang
    texts = transcribe_wav(wav_path, lang, args.threads)
    if not texts:
        print("没有识别到语音")
        sys.exit(4)

    txt_path = os.path.join("media", stem + ".txt")
    srt_path = os.path.join("media", stem + ".srt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(t[2] for t in texts) + "\n")
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, (start, end, text) in enumerate(texts, 1):
            f.write("%d\n%s --> %s\n%s\n\n" % (i, srt_timestamp(start), srt_timestamp(end), text))
    print(os.path.abspath(txt_path))
    print(os.path.abspath(srt_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
