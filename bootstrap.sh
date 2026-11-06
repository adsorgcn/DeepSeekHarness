#!/usr/bin/env bash
# bootstrap.sh — DeepSeekHarness 记忆体一键引导（macOS / Linux）
#
# 原则：全部软件只从官方源安装；每步要不要人审批由 DSH 的审批模式决定——
#   · 不需要审批的（检测、克隆、切目录、验收）→ 自动跑
#   · 需要审批的（装 git / python 等系统软件）→ agent 先问用户，同意后执行
# 国内网络：GitHub 不可达时自动切换产品仓库到国内镜像
#   https://gitee.com/monetize/DeepSeekHarness（镜像与 GitHub 同源，由 owner 维护）
#
# 用法：
#   bash bootstrap.sh                                    # 只检测并打印计划（默认，零改动）
#   bash bootstrap.sh -Install -Yes                      # 按计划执行（用户已审批后）
#   bash bootstrap.sh -Install -Yes -TargetDir "$HOME/dsh-memory"
#   bash bootstrap.sh -Install -Yes -Source gitee        # 强制走国内镜像

set -u

TARGET="${HOME}/dsh-memory"
INSTALL=0
YES=0
SOURCE="auto"
GITHUB_URL="https://github.com/adsorgcn/DeepSeekHarness.git"
GITEE_URL="https://gitee.com/monetize/DeepSeekHarness.git"
GITHUB_PROBE="https://github.com"

while [ $# -gt 0 ]; do
  case "$1" in
    -Install) INSTALL=1 ;;
    -Yes) YES=1 ;;
    -TargetDir) TARGET="$2"; shift ;;
    -Source) SOURCE="$2"; shift ;;
  esac
  shift
done

has() { command -v "$1" >/dev/null 2>&1; }

GIT_BIN="$(command -v git 2>/dev/null || true)"
PY_BIN="$(command -v python3 2>/dev/null || command -v python 2>/dev/null || true)"
OS="$(uname -s)"
BREW_OK=0; has brew && BREW_OK=1
APT_OK=0; has apt-get && APT_OK=1

dsh_installed() {
  [ -f "$1/AGENTS.md" ] && [ -f "$1/tools/brain.py" ] && [ -f "$1/CITATION.cff" ]
}

github_reachable() {
  [ "$SOURCE" = "gitee" ] && return 1
  [ "$SOURCE" = "github" ] && return 0
  if has curl; then
    curl -s --max-time 8 -o /dev/null "$GITHUB_PROBE" && return 0
  fi
  [ -n "$GIT_BIN" ] && "$GIT_BIN" ls-remote --heads "$GITHUB_URL" main >/dev/null 2>&1
}

say() { printf '%s\n' "$1"; }
ok() { if [ "$1" = "1" ]; then say "已装"; else say "缺（需审批安装）"; fi; }

product_source="auto"
if [ "$SOURCE" = "gitee" ]; then product_source="gitee"; elif [ "$SOURCE" = "github" ]; then product_source="github"; elif github_reachable; then product_source="github"; else product_source="gitee"; fi
CLONE_URL="$GITHUB_URL"
[ "$product_source" = "gitee" ] && CLONE_URL="$GITEE_URL"

say "== DeepSeekHarness 记忆体引导 =="
printf 'git     : %s\n' "$(ok "$([ -n "$GIT_BIN" ] && echo 1 || echo 0)")"
printf 'python3 : %s\n' "$(ok "$([ -n "$PY_BIN" ] && echo 1 || echo 0)")"
if [ "$OS" = "Darwin" ]; then
  printf 'brew    : %s\n' "$(ok $BREW_OK)"
else
  printf 'apt-get : %s\n' "$(ok $APT_OK)"
fi
if dsh_installed "$TARGET"; then say "目标仓库: 已安装（完整） -> $TARGET"; else say "目标仓库: 待克隆 -> $TARGET"; fi
if [ "$SOURCE" = "auto" ]; then say "产品源  : 自动探测（GitHub 优先，不可达走国内镜像 gitee.com/monetize/DeepSeekHarness）——本轮: $product_source"
elif [ "$SOURCE" = "gitee" ]; then say "产品源  : 国内镜像 gitee.com/monetize/DeepSeekHarness（强制）"
else say "产品源  : github.com/adsorgcn/DeepSeekHarness（强制）"; fi
say ""

PLAN=""
[ -n "$GIT_BIN" ] || PLAN="$PLAN  - 安装 git —— 官方源：$([ "$OS" = "Darwin" ] && say 'brew install git' || say 'apt-get install -y git')\n"
if [ -z "$PY_BIN" ]; then
  if [ "$OS" = "Darwin" ]; then PLAN="$PLAN  - 安装 python3 —— 官方源：brew install python@3.12\n"; else PLAN="$PLAN  - 安装 python3 —— 官方源：apt-get install -y python3\n"; fi
fi
dsh_installed "$TARGET" || PLAN="$PLAN  - 克隆 $CLONE_URL -> $TARGET\n"
PLAN="$PLAN  - 切目录 $TARGET 并跑 brain.py check 验收（失败即停）\n  - 安装记忆推送保护钩子（私人记忆不确认不得推送）"

say "计划："
printf '%b\n' "$PLAN"
say ""

[ "$INSTALL" = "1" ] || { say "（默认只出计划，不做任何改动。确认后：agent 逐项征得你同意，再以 -Install -Yes 执行。）"; exit 0; }

approve() {
  [ "$YES" = "1" ] && return 0
  if [ -t 0 ]; then
    printf '  需要安装系统软件: %s [y/N] ' "$1"
    read -r a || a="n"
    [ "$a" = "y" ] || [ "$a" = "Y" ]
  else
    say "  需要安装系统软件: $1 —— 未确认（-Yes 未给出且当前不是交互终端），已停止。"
    return 1
  fi
}

# 1) git（官方源）
if [ -z "$GIT_BIN" ]; then
  if approve "git（官方源）"; then
    if [ "$OS" = "Darwin" ]; then
      [ "$BREW_OK" = "1" ] || { say "brew 不可用。请从官方安装：https://brew.sh ，装好后重跑本脚本。"; exit 1; }
      brew install git || { say "git 安装失败，已停止。"; exit 1; }
    else
      [ "$APT_OK" = "1" ] || { say "apt-get 不可用。请用系统包管理器安装 git 后重跑本脚本。"; exit 1; }
      sudo apt-get update && sudo apt-get install -y git || { say "git 安装失败，已停止。"; exit 1; }
    fi
    say "git 安装完成。"
    GIT_BIN="$(command -v git 2>/dev/null || true)"
  else
    say "跳过 git（后续克隆仓库需要它）。"
  fi
fi

# 2) python（官方源）
if [ -z "$PY_BIN" ]; then
  if approve "python3（官方源）"; then
    if [ "$OS" = "Darwin" ]; then
      [ "$BREW_OK" = "1" ] || { say "brew 不可用。请从官方安装：https://brew.sh ，装好后重跑本脚本。"; exit 1; }
      brew install python@3.12 || { say "python3 安装失败，已停止。"; exit 1; }
    else
      [ "$APT_OK" = "1" ] || { say "apt-get 不可用。请用系统包管理器安装 python3 后重跑本脚本。"; exit 1; }
      sudo apt-get update && sudo apt-get install -y python3 || { say "python3 安装失败，已停止。"; exit 1; }
    fi
    say "python3 安装完成。"
    PY_BIN="$(command -v python3 2>/dev/null || command -v python 2>/dev/null || true)"
  else
    say "跳过 python3（brain.py check 需要它）。"
  fi
fi

# 3) 克隆仓库（无需审批，但失败即停）
if ! dsh_installed "$TARGET"; then
  if [ -e "$TARGET" ]; then
    say "目标目录已存在但检测不到完整安装（缺 AGENTS.md / tools/brain.py / CITATION.cff）。为避免覆盖你已有的文件，已停止。请换一个 -TargetDir。"
    exit 1
  fi
  say "克隆仓库（$product_source）..."
  [ -n "$GIT_BIN" ] || { say "git 仍不可用：请重跑本脚本。"; exit 1; }
  "$GIT_BIN" clone "$CLONE_URL" "$TARGET" || { say "克隆失败（$CLONE_URL）。请检查网络，或改用 -Source gitee 后重跑。"; exit 1; }
fi

# 4) 验收（失败即停，不报完成）
cd "$TARGET" || { say "无法进入 $TARGET，已停止。"; exit 1; }
[ -n "$PY_BIN" ] || { say "python 仍不可用：请重跑本脚本。"; exit 1; }
"$PY_BIN" -X utf8 tools/brain.py check || { say "验收失败：brain.py check 未通过，已停止（请按上面 ERROR/WARN 修复）。"; exit 1; }

# 5) 记忆推送保护钩子
if [ -f tools/guard-pre-push.sh ] && [ -d .git ]; then
  cp tools/guard-pre-push.sh .git/hooks/pre-push
  chmod +x .git/hooks/pre-push
  say "已安装记忆推送保护钩子（推私人记忆前需显式确认 DSH_ALLOW_MEMORY_PUSH=1）。"
else
  say "（本次克隆的版本不含推送保护钩子；更新到新版本后重跑即可自动安装。）"
fi

say ""
say "完成。关掉这个窗口重开一个，把 $TARGET 选为工作区，它第一句应该汇报上次做到哪；没看到就把屏幕上的内容贴给你的 DSH。"
