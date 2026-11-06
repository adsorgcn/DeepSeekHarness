#!/bin/sh
# clip_shot.sh — 把剪贴板里的截图存成 shots/<UTC 时间戳>.png，打印绝对路径（macOS / Linux）
# 用法: sh tools/clip_shot.sh
# 无图或取不到时打印 NO_IMAGE 并退出 2；成功打印绝对路径并退出 0。输出目录: <仓库根>/shots/
set -u

HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
REPO="$(dirname -- "$HERE")"
DIR="$REPO/shots"
mkdir -p "$DIR"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$DIR/$STAMP.png"

case "$(uname -s)" in
  Darwin)
    if osascript -e 'set pngData to the clipboard as «class PNGf»' -e "set f to open for access POSIX file \"$OUT\" with write permission" -e 'write pngData to f' -e 'close access f' >/dev/null 2>&1 && [ -s "$OUT" ]; then
      echo "$OUT"
      exit 0
    fi
    echo "NO_IMAGE"
    exit 2
    ;;
  Linux)
    if command -v wl-paste >/dev/null 2>&1; then
      wl-paste -t image/png > "$OUT" 2>/dev/null
      if [ -s "$OUT" ]; then
        echo "$OUT"
        exit 0
      fi
    fi
    if command -v xclip >/dev/null 2>&1; then
      xclip -selection clipboard -t image/png -o > "$OUT" 2>/dev/null
      if [ -s "$OUT" ]; then
        echo "$OUT"
        exit 0
      fi
    fi
    echo "NO_IMAGE"
    exit 2
    ;;
  *)
    echo "NO_IMAGE"
    exit 2
    ;;
esac
