# -*- coding: utf-8 -*-
"""transcribe.py 行为测试（纯标准库、注入式、零网络、零模型）。

覆盖：链接/文件分辨；SRT 时间戳格式；引擎缺失退出 2；ffmpeg 命令 16k 单声道；无云端字样；
无 numpy；flush 恰好一次且 flush 后段进结果；官方 VAD 参数；边喂边识别（decode 先于 flush）；
引擎目录在用户目录（仓库外）。

用法: python -X utf8 tools/test_transcribe.py （工作目录=仓库根）
"""
import array
import importlib.util
import os
import sys
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_t():
    spec = importlib.util.spec_from_file_location("transcribe", os.path.join(ROOT, "tools", "transcribe.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


T = load_t()
RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print("[%s] %s %s" % (name, "PASS" if cond else "FAIL", detail))


def test_url_detect():
    ok = T.is_url("https://www.bilibili.com/video/BV1xx411c7mD")
    ok = ok and T.is_url("http://example.com/a.mp4")
    ok = ok and not T.is_url("media/a.mp4")
    ok = ok and not T.is_url("C:/tmp/a.wav")
    check("url_detect", ok)


def test_srt_format():
    check("srt_format", T.srt_timestamp(3723.345) == "01:02:03,345",
          T.srt_timestamp(3723.345))


def test_engine_missing_exit_2():
    code = T.check_engine_ready(os.path.join(ROOT, ".definitely-missing", "python.exe"),
                                os.path.join(ROOT, "models", "sensevoice"),
                                import_fn=lambda: None)
    check("engine_missing_exit_2", code == 2, "code=%s" % code)


def test_ffmpeg_cmd_is_16k_mono():
    cmd = T.build_ffmpeg_cmd("media/a.mkv", "media/a.16k.wav")
    check("ffmpeg_cmd_is_16k_mono",
          cmd == ["ffmpeg", "-y", "-i", "media/a.mkv", "-ac", "1", "-ar", "16000", "-f", "wav", "media/a.16k.wav"],
          str(cmd))


def test_no_cloud():
    s = open(os.path.join(ROOT, "tools", "transcribe.py"), encoding="utf-8").read().lower()
    bad = [k for k in ("openai", "whisper", "api.deepseek", "api.openai") if k in s]
    check("no_cloud", not bad, "found=%s" % bad)


def test_no_numpy():
    s = open(os.path.join(ROOT, "tools", "transcribe.py"), encoding="utf-8").read().lower()
    check("no_numpy", "numpy" not in s)


def test_engine_home_outside_repo():
    home = os.path.expanduser("~")
    ok = T.ASR_HOME.startswith(home) and not T.ASR_HOME.startswith(ROOT + os.sep)
    check("engine_home_outside_repo", ok, T.ASR_HOME)


def make_test_wav(path, seconds=1):
    with wave.open(path, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        a = array.array("h", [0] * (16000 * seconds))
        f.writeframes(a.tobytes())
    return path


def make_fake_so():
    """假 sherpa_onnx：记录事件顺序；第三个 accept 起吐出段，flush 后吐最后一段。"""
    events = []
    configs = []
    pending = []
    accepts = [0]

    class FakeSilero:
        window_size = 512
        model = None
        threshold = None
        min_silence_duration = None
        max_speech_duration = None

    class FakeVadConfig:
        def __init__(self):
            self.silero_vad = FakeSilero()
            self.sample_rate = None
            configs.append(self)

    def seg(start, n):
        return type("Seg", (), {"start": start, "samples": [0.0] * n})()

    class FakeVAD:
        def __init__(self, config, buffer_size_in_seconds):
            events.append(("init", buffer_size_in_seconds))

        def accept_waveform(self, samples):
            accepts[0] += 1
            events.append(("accept", len(samples)))
            if accepts[0] == 3:
                pending.append(seg(0, 4096))  # 喂到一半吐一段

        def empty(self):
            return not pending

        @property
        def front(self):
            return pending[0]

        def pop(self):
            seg0 = pending.pop(0)
            events.append(("pop", seg0.start))
            return None

        def flush(self):
            events.append(("flush",))
            pending.append(seg(32000, 4096))  # flush 后吐出最后一段

    class FakeResult:
        text = "FIXED TEXT"

    class FakeStream:
        def __init__(self):
            self.result = FakeResult()

        def accept_waveform(self, rate, samples):
            events.append(("stream_accept", rate, len(samples)))

    class FakeRecognizer:
        def create_stream(self):
            events.append(("decode",))
            return FakeStream()

        def decode_stream(self, stream):
            events.append(("decode_stream",))

    class FakeOfflineRecognizer:
        @staticmethod
        def from_sense_voice(**kw):
            return FakeRecognizer()

    mod = type("so", (), {
        "VadModelConfig": FakeVadConfig,
        "VoiceActivityDetector": FakeVAD,
        "OfflineRecognizer": FakeOfflineRecognizer,
    })()
    return mod, events, configs


def run_fake():
    wav = make_test_wav(os.path.join(ROOT, "media-test.wav"))
    try:
        so, events, configs = make_fake_so()
        texts = T.transcribe_wav(wav, "zh", 1, so=so)
    finally:
        if os.path.exists(wav):
            os.remove(wav)
    return texts, events, configs


def test_flush_at_eof():
    texts, events, _ = run_fake()
    flushes = [e for e in events if e[0] == "flush"]
    ok = len(flushes) == 1 and len(texts) == 2 and any(t[0] >= 2.0 for t in texts)
    check("flush_at_eof", ok, "flushes=%d texts=%d starts=%s" % (len(flushes), len(texts), [t[0] for t in texts]))


def test_vad_params_official():
    _, _, configs = run_fake()
    cfg = configs[0].silero_vad
    ok = cfg.threshold == 0.2 and cfg.min_silence_duration == 0.25 and cfg.max_speech_duration == 5
    check("vad_params_official", ok, "t=%s ms=%s mx=%s" % (cfg.threshold, cfg.min_silence_duration, cfg.max_speech_duration))


def test_drain_during_feed():
    _, events, _ = run_fake()
    idx_decode = events.index(("decode",))
    idx_flush = events.index(("flush",))
    check("drain_during_feed", idx_decode < idx_flush, "decode@%d flush@%d" % (idx_decode, idx_flush))


def main():
    os.chdir(ROOT)
    test_url_detect()
    test_srt_format()
    test_engine_missing_exit_2()
    test_ffmpeg_cmd_is_16k_mono()
    test_no_cloud()
    test_no_numpy()
    test_flush_at_eof()
    test_vad_params_official()
    test_drain_during_feed()
    test_engine_home_outside_repo()
    failed = [n for n, ok, _ in RESULTS if not ok]
    print("-" * 60)
    print("SUMMARY:", "ALL PASS (%d scenarios)" % len(RESULTS) if not failed else ("FAIL: " + ", ".join(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
