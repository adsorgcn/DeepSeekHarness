# Mem-Forever × DSH 适配方案（已落地）

> ⚠️ **历史现场记录**：本文是早期适配回合的现场记录（含当时本机状态与结论），只作方法参考；**不作为新用户的当前验收证据**。当前安装与验收以 README、一键安装.md、bootstrap.* 与仓库 CI 为准（v1.0.8 起含国内镜像与记忆推送保护）。

> 回答一个问题：Mem-Forever 怎么做适配，才能变成「DSH 最配的东西」——新一代记忆体。

## 一句话答案

**Mem-Forever 不需要被改造成 DSH 插件——DSH 的原生机制就是它的宿主。** 适配的全部工作只有一件事：让 brain 仓库落在 DSH 看得见的地方，然后四个原生通道自动接管：工作区锚定、AGENTS.md 自动注入、技能系统、git 化文件审查。

## 接口映射（为什么说它俩天生一对）

| Mem-Forever 的机制 | DSH 的原生载体 | 适配动作 |
|---|---|---|
| brain 仓库（soul/memory/handoff/vault） | **工作区**——DSH 的一切锚定于工作区 | brain 目录即工作区，打开即记忆上线 |
| `AGENTS.md`（五份指令文件之一，模板已备好） | `@deepseek-ai/dsh-agent-instructions` 每次会话自动发现并注入 | **零配置**（本回合已实证：AGENTS.md 在会话中实时注入） |
| `skills/mem-forever/SKILL.md`（规范文本） | DSH 技能系统，技能根 `<project>/.dsh/skills/` | 复制到 `brain/.dsh/skills/mem-forever/`，即可按需 `skill` 加载 |
| `brain.py check / handoff review` | pwsh 工具 + DSH 内置 Python 3.12 | 直接可跑（已跑通：0 错误 0 警告） |
| 评审（review before merge） | **子智能体**——DSH 的 subagent 就是独立上下文评审员 | 可派子代理跑 `handoff review`，与模型自身隔离 |
| claim 锁（status: open → claimed） | git 本身即锁 | 保持原设计不变 |
| 周期收尾（折叠、审计、衰减） | Schedule 插件 | 定时派发到会话 |
| 每次记忆写入 | workspace-changes | UI 上每笔记忆是可见的变更卡 |
| 外部内容沉淀 | RedFox 等 MCP | 抓取 → 由 agent 写入 `memory/*.md` |

**DSH 独有红利**：记忆的每次写入在界面就是一张 diff 卡；评审可以派子智能体隔离上下文；定时收尾用 Schedule；外部内容经 MCP 进 memory/。这是 Claude Code / Cursor 都给不了的部分。

## 本回合已落地（可验证）

1. **brain 落盘**：`default-workspace/brain/`，来自 Mem-Forever 2.1 模板（zip 方式，本机无 git）。
2. **AGENTS.md 自动注入已实证**：brain 目录被触达的瞬间，DSH 就把它作为 `<system-reminder>` 注入了本会话——这就是「打开即记忆上线」的活证据。
3. **技能已挂**：`brain/.dsh/skills/mem-forever/SKILL.md`（DSH 项目技能根）。
4. **灵魂两份已写**：
   - `soul/soul.md`——owner 档案（工作风格、边界，来自这几轮真实交流）；
   - `soul/agent.md`——给定的 persona（PROMETHEUS-SOUL raw-1.0）**verbatim 保存，带版本号与 sha256**，之下是这几轮学到的三条经验。
5. **记忆三份 + 索引**：`dsh-first-move`（起手式：先学 iLang）、`redfox-mcp`（11 服务器 89 工具）、`mem-forever-dsh`（本次适配经验）。
6. **交接单闭环**：适配回合已 `closed` 归档到 `handoff/archive/`，新 `CURRENT.md` 已打开（`status: open`，待下个会话 claim）。
7. **验收**：`brain.py check` → **0 errors, 0 warnings**（8 个 OKF 文件、60 文件密钥扫描通过）。

## 待办（已写进交接单）

- **本机没有 git**：commit/push 环节挂起（记忆已本地保存）。两条路：
  1. 装 Git for Windows，`cd brain && git init -b main && git remote add origin <你的私有仓库> && git push -u origin main`；
  2. 或直接在 GitHub 用 Mem-Forever 模板建私有仓库，把本机文件覆盖上传。
- **新会话验证**：新开一个窗口，把 `default-workspace/brain` 选为工作区——应自动看到交接单汇报，且 `mem-forever` 技能出现在技能目录里。

## 日常用法（用户视角，三句话）

1. 新窗口把 brain 选为工作区 → 开场自动汇报「上次做到哪、接下来做什么、哪些没验证」。
2. 任何里程碑（部署成功/结论达成/要关窗口前）agent 自动更新交接单并 commit。
3. 换模型、换机器、换工具，交接单和记忆都在；密钥在 `vault/`（age 加密），文本里只有指纹。

## 与旧范式的分野（一句话）

旧插件是「装手」：能力焊在代码里，记忆锁在私有格式里。这套是「装脑」：记忆是文件、规则是声明、判断在代码、合并有人审——**每一笔记忆都是一次可读、可审、可迁移的 git 提交**。
