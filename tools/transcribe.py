#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""视频/音频 → 文字 + 字幕（本地 SenseVoice，流程照 k2-fsa/sherpa-onnx 官方 generate-subtitles.py）。

用法:
  python tools/transcribe.py <链接或文件路径> [--lang auto|zh|en|ja|ko|yue] [--threads N]

退出码: 0 成功；2 引擎/模型缺失；3 下载失败；4 没有识别到语音。
输出: media/<名>.txt（整篇）与 media/<名>.srt（分段带时间），打印两个绝对路径。
音频不出本机；允许出现的网络只有 yt-dlp 自己的下载。
"""
import argparse
import os
import subprocess
import sys

VENV = ".asr-venv"
MODELS = os.path.join("models", "sensevoice")


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
    """当前解释器不是 .asr-venv 里的，就用 venv 的 Python 重新执行自己。"""
    vp = venv_python()
    if os.path.realpath(sys.executable) == os.path.realpath(vp):
        return
    if not os.path.exists(vp):
        print("先装视频转文字引擎：python tools/free_station.py install sherpa-onnx")
        sys.exit(2)
    os.execv(vp, [vp] + sys.argv)


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


def download_audio(url):
    out_tpl = os.path.join("media", "%(id)s.%(ext)s")
    p = subprocess.run(["yt-dlp", "-f", "bestaudio", "-o", out_tpl,
                        "--print", "after_move:filepath", url],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print(p.stderr.strip())
        sys.exit(3)
    lines = [ln for ln in p.stdout.splitlines() if ln.strip()]
    if not lines:
        print(p.stderr.strip() or "yt-dlp 未返回文件路径")
        sys.exit(3)
    return lines[-1].strip()


def transcribe_wav(wav_path, lang, threads):
    import sherpa_onnx
    import wave

    recognizer = sherpa_onnx.OfflineRecognizer.from_sense_voice(
        model=os.path.join(MODELS, "model.int8.onnx"),
        tokens=os.path.join(MODELS, "tokens.txt"),
        num_threads=threads,
        language=lang,
        use_itn=True,
    )
    vad_config = sherpa_onnx.VadModelConfig()
    vad_config.silero_vad.model = os.path.join(MODELS, "silero_vad.onnx")
    vad_config.silero_vad.min_silence_duration = 0.5
    vad_config.silero_vad.threshold = 0.5
    vad_config.sample_rate = 16000
    window_size = vad_config.silero_vad.window_size
    buffer = sherpa_onnx.VoiceActivityDetector(vad_config, buffer_size_in_seconds=100)

    segments = []
    with wave.open(wav_path, "rb") as f:
        assert f.getframerate() == 16000, "wav 采样率必须是 16000"
        samples_per_read = int(window_size * f.getframerate())
        while True:
            samples = f.readframes(samples_per_read)
            if not samples:
                break
            samples = sherpa_onnx.float32_samples(samples)
            buffer.accept_waveform(samples)
            while not buffer.empty():
                segment = buffer.front
                buffer.pop()
                segments.append(segment)

    texts = []
    for seg in segments:
        stream = recognizer.create_stream()
        stream.accept_waveform(seg.samples)
        recognizer.decode_stream(stream)
        text = (stream.result.text or "").strip()
        if text:
            texts.append((seg.start, seg.start + len(seg.samples) / 16000.0, text))
    return texts


def main(argv=None):
    ap = argparse.ArgumentParser(description="视频/音频转文字与字幕（本地）")
    ap.add_argument("input", help="链接或本地文件路径")
    ap.add_argument("--lang", default="auto", choices=("auto", "zh", "en", "ja", "ko", "yue"))
    ap.add_argument("--threads", type=int, default=2)
    args = ap.parse_args(argv)

    reexec_if_needed()
    code = check_engine_ready(venv_python(), MODELS)
    if code is not None:
        sys.exit(code)

    os.makedirs("media", exist_ok=True)
    src = args.input
    if is_url(src):
        src = download_audio(src)

    stem = os.path.splitext(os.path.basename(src))[0]
    wav_path = os.path.join("media", stem + ".16k.wav")
    p = subprocess.run(build_ffmpeg_cmd(src, wav_path),
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
