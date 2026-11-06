#!/usr/bin/env bash
# bootstrap.sh — DeepSeekHarness 记忆体一键引导（macOS / Linux）
#
# 原则：全部软件只从官方源安装；每步要不要人审批由 DSH 的审批模式决定——
#   · 不需要审批的（检测、克隆、切目录、验收）→ 自动跑
#   · 需要审批的（装 git / python 等系统软件）→ agent 先问用户，同意后执行
#
# 用法：
#   bash bootstrap.sh                          # 只检测并打印计划（默认，零改动）
#   bash bootstrap.sh -Install -Yes            # 按计划执行（用户已审批后）
#   bash bootstrap.sh -Install -Yes -TargetDir "$HOME/dsh-memory"

set -u

TARGET="${HOME}/dsh-memory"
INSTALL=0
YES=0
while [ $# -gt 0 ]; do
  case "$1" in
    -Install) INSTALL=1 ;;
    -Yes) YES=1 ;;
    -TargetDir) TARGET="$2"; shift ;;
  esac
  shift
done

has() { command -v "$1" >/dev/null 2>&1; }

GIT_OK=0; has git && GIT_OK=1
PY_OK=0; has python3 && PY_OK=1
BREW_OK=0; has brew && BREW_OK=1
APT_OK=0; has apt-get && APT_OK=1
REPO_OK=0; [ -f "$TARGET/AGENTS.md" ] && REPO_OK=1
OS="$(uname -s)"

say() { printf '%s\n' "$1"; }
ok() { if [ "$1" = "1" ]; then say "已装"; else say "缺（需审批安装）"; fi; }

say "== DeepSeekHarness 记忆体引导 =="
printf 'git     : %s\n' "$(ok $GIT_OK)"
printf 'python3 : %s\n' "$(ok $PY_OK)"
if [ "$OS" = "Darwin" ]; then
  printf 'brew    : %s\n' "$(ok $BREW_OK)"
else
  printf 'apt-get : %s\n' "$(ok $APT_OK)"
fi
if [ "$REPO_OK" = "1" ]; then say "目标仓库: 已存在 -> $TARGET"; else say "目标仓库: 待克隆 -> $TARGET"; fi
say ""

PLAN=""
[ "$GIT_OK" = "1" ] || PLAN="$PLAN  - 安装 git —— 官方源：$([ "$OS" = "Darwin" ] && say 'brew install git' || say 'apt-get install -y git')\n"
if [ "$PY_OK" != "1" ]; then
  if [ "$OS" = "Darwin" ]; then PLAN="$PLAN  - 安装 python3 —— 官方源：brew install python@3.12\n"; else PLAN="$PLAN  - 安装 python3 —— 官方源：apt-get install -y python3\n"; fi
fi
[ "$REPO_OK" = "1" ] || PLAN="$PLAN  - 克隆 https://github.com/adsorgcn/DeepSeekHarness -> $TARGET\n"
PLAN="$PLAN  - 切目录 $TARGET 并跑 brain.py check 验收"

say "计划："
printf '%b\n' "$PLAN"
say ""

[ "$INSTALL" = "1" ] || { say "（默认只出计划，不做任何改动。确认后：agent 逐项征得你同意，再以 -Install -Yes 执行。）"; exit 0; }

# 1) git（官方源）
if [ "$GIT_OK" != "1" ]; then
  if [ "$OS" = "Darwin" ]; then
    [ "$BREW_OK" = "1" ] || { say "brew 不可用。请从官方安装：https://brew.sh ，装好后重跑本脚本。"; exit 1; }
    brew install git || true
  else
    [ "$APT_OK" = "1" ] || { say "apt-get 不可用。请用系统包管理器安装 git 后重跑本脚本。"; exit 1; }
    sudo apt-get update && sudo apt-get install -y git || true
  fi
  say "git 安装完成。"
fi

# 2) python（官方源）
if [ "$PY_OK" != "1" ]; then
  if [ "$OS" = "Darwin" ]; then
    [ "$BREW_OK" = "1" ] || { say "brew 不可用。请从官方安装：https://brew.sh ，装好后重跑本脚本。"; exit 1; }
    brew install python@3.12 || true
  else
    [ "$APT_OK" = "1" ] || { say "apt-get 不可用。请用系统包管理器安装 python3 后重跑本脚本。"; exit 1; }
    sudo apt-get update && sudo apt-get install -y python3 || true
  fi
  say "python3 安装完成。"
fi

# 3) 克隆仓库（无需审批）
if [ "$REPO_OK" != "1" ]; then
  say "克隆仓库..."
  has git || { say "git 仍不可用：请重跑本脚本。"; exit 1; }
  git clone https://github.com/adsorgcn/DeepSeekHarness.git "$TARGET"
fi

# 4) 验收（无需审批）
cd "$TARGET" || exit 1
PY=python3
has python3 || PY=python3.12
"$PY" -X utf8 tools/brain.py check

say ""
say "完成。在 DSH 里把 $TARGET 选为工作区（或说一句话让 agent 切进去），记忆体即上线。"
