# -*- coding: utf-8 -*-
"""transcribe.py 行为测试（纯标准库、注入式、零网络、零模型）。

覆盖：链接/文件分辨；SRT 时间戳格式；引擎缺失退出 2；ffmpeg 命令 16k 单声道；源码无云端字样。

用法: python -X utf8 tools/test_transcribe.py （工作目录=仓库根）
"""
import importlib.util
import os
import sys

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


def main():
    os.chdir(ROOT)
    test_url_detect()
    test_srt_format()
    test_engine_missing_exit_2()
    test_ffmpeg_cmd_is_16k_mono()
    test_no_cloud()
    failed = [n for n, ok, _ in RESULTS if not ok]
    print("-" * 60)
    print("SUMMARY:", "ALL PASS (%d scenarios)" % len(RESULTS) if not failed else ("FAIL: " + ", ".join(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
