#!/bin/sh
# DeepSeekHarness 记忆推送保护钩子（bootstrap 克隆后自动安装到 .git/hooks/pre-push）。
#
# 规则：本仓库是公开产品模板；soul/ memory/ handoff/ vault/ env/ log.md 是私人记忆。
# 默认拦截任何包含私人记忆文件的 push，防止误推到公共仓库。
# 确认目标是自己的私有仓库后，可显式放行：
#   DSH_ALLOW_MEMORY_PUSH=1 git push ...
#
# 不拦截：不含私人记忆文件的产品更新推送。
set -u

ALLOW="${DSH_ALLOW_MEMORY_PUSH:-0}"
[ "$ALLOW" = "1" ] && exit 0
# 放行也可以来自本机 .git/config（B2 备份模式在用户确认私有仓库后设一次，不随仓库走）
if [ "$(git config --bool dsh.allowMemoryPush 2>/dev/null)" = "true" ]; then
  exit 0
fi

PATTERN='^(soul|memory|handoff|vault|env|projects|mirror|\.ilang)/|^log\.md$'
ZEROS="0000000000000000000000000000000000000000"

blocked=0
while read -r local_ref local_sha remote_ref remote_sha; do
  [ -n "${local_sha:-}" ] || continue
  if [ "$remote_sha" = "$ZEROS" ]; then
    base="$(git rev-parse "${local_sha}^" 2>/dev/null)" || {
      echo "DSH 记忆保护：无法确定比较基线，请确认目标仓库后再推送。"
      exit 1
    }
  else
    base="$remote_sha"
  fi
  files="$(git diff --name-only "$base" "$local_sha" 2>/dev/null)" || continue
  if printf '%s\n' "$files" | grep -qE "$PATTERN"; then
    blocked=1
  fi
done

if [ "$blocked" = "1" ]; then
  echo "DSH 记忆保护：本次推送包含私人记忆文件（soul/ memory/ handoff/ vault/ env/ log.md）。"
  echo "这些是私人记忆，公共仓库（如产品开源仓库）永远不要推送它们。"
  echo "若目标确实是你的私有仓库，请显式放行：DSH_ALLOW_MEMORY_PUSH=1 git push ..."
  echo "推送已取消。"
  exit 1
fi
exit 0
