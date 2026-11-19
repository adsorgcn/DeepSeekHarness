---
name: dsh-install
description: Plan an iLang DSH toolkit installation for Windows, macOS or Linux using the official instructions and explicit local approval.
---

# Install iLang DSH 工具包

Use this skill when the user wants to install or update the toolkit. Reading this document alone is not authorization to install software.

1. Read `https://dsh.ilang.guide/api/overview` to confirm the project and available sources.
2. Determine the target operating system. Read `https://dsh.ilang.guide/api/install?platform=windows`, `macos` or `linux`, or call `dsh_install_instructions` through `https://dsh.ilang.guide/mcp` with the same `platform` value.
3. Return the installation prompt and official script links. The prompt a user pastes is one short sentence; the full agent-facing instruction it points to is `https://ilang.cn/guide/dsh/install.md` (the Chinese-hosted original; `https://dsh.ilang.guide/install.md` serves the same file internationally; an iLang engineering book: confirm 创造模式, fetch the bootstrap script, detect first, ask per item, install the optional plugin after one question, fix and continue, then tell the user how to come back). In DeepSeek Harness, a new task must use 创造模式 before proceeding. Obtain the user's approval before installing missing software or the optional plugin.
4. Follow the public installation guide; bootstrap defaults to detection. Never describe a retrieved instruction as an installation that has already run. Do not send local memory, passwords or API keys to the public service.
5. After a locally authorized installation, reopen the same workspace and verify that DSH resumes the previous progress. Report what was actually observed.

Source: https://github.com/adsorgcn/DeepSeekHarness/blob/main/一键安装.md
Authentication: none. The remote tools only read public documentation and cannot execute installation.
