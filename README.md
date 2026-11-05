# DeepSeek Harness × iLang：新一代记忆体

> **一个 fork/clone 之后，直接在 DeepSeek Harness 里当工作区打开就能用的记忆体。**
> 上游：[ilang-ai/Mem-Forever](https://github.com/ilang-ai/Mem-Forever)（iLang v5.0 记忆协议）；本仓库是它的 **DSH 适配版**。

## 🚀 一键开始（一句话 + 审批）

在任何 DSH 会话里粘贴：

> 帮我初始化记忆体：先下载运行 https://github.com/adsorgcn/DeepSeekHarness 的 bootstrap.ps1 检测环境；缺什么（git、Python 等）列给我并逐个征得我同意后从官方源安装；然后把仓库克隆到本机、把工作目录切进去、读它的 AGENTS.md 完成初始化。

模式 = **DSH 审批模式**：克隆、切目录、AGENTS.md 注入、技能发现、初始化全部自动；装 Git / Python 等系统软件先问你、同意才装，且**只走官方源**（winget 官方包 / git-scm.com / python.org）。详见 [一键安装.md](一键安装.md)。

## 它是什么

每个 AI 工具每次会话后都会把你忘掉。这个仓库不会——**永远不**。

- 你的档案、偏好、决定、经验 → 一份份纯 Markdown 记忆文件（iLang 声明块，人可读、机可解析、`git diff` 可审）。
- 每次会话开头，agent 读交接单，两句话告诉你「上次做到哪、接下来做什么、哪些没验证」。
- 换窗口、换模型、换机器，记忆都在；密钥在 `vault/`（age 加密），文本里只有指纹。

## 为什么说它和 DSH 是天生一对（本仓库的适配点）

| Mem-Forever 机制 | DSH 原生载体 |
|---|---|
| `AGENTS.md` 会话仪式 | DSH 的 agent-instructions **每次会话自动注入，零配置** |
| `skills/mem-forever/SKILL.md` 规范文本 | DSH 技能系统（挂在本仓库 `.dsh/skills/`，可 `skill` 按需加载） |
| `brain.py check / handoff review` | DSH 内置 Python 3.12 + PowerShell 工具直接可跑 |
| 每笔记忆写入 | DSH workspace-changes 在界面显示为可见的变更卡 |
| 评审 write-back | DSH 子智能体（独立上下文评审员） |
| 周期收尾 | DSH Schedule 定时派发 |

## 用户怎么用（三句话）

1. **Fork 本仓库为你的私有仓库**，`git clone` 到本机（或直接下载 zip）。
2. 打开 DeepSeek Harness，把本目录**选为工作区**。
3. 正常聊天。开场它会自动汇报进度；里程碑自动更新交接单；你说「看看上次到哪了」它就知道。

## 结构

```
BRAIN.md              ← 先读我
AGENTS.md             ← DSH 每次会话自动注入的仪式
handoff/CURRENT.md    ← 交接单：done / next / unverified
soul/soul.md          ← 你是谁（agent 从对话自动建立）
soul/agent.md         ← agent 自己的灵魂：你给它的 persona（verbatim + 哈希）+ 它跟你学到的
memory/*.md           ← 一份记忆一个文件
vault/                ← age 加密的密钥，永不进文本
rules/GRAMMAR-CARD.md ← 记法速查卡（中文版同目录）
tools/brain.py        ← check / vault / handoff review（纯标准库）
docs/                 ← 交付文档（见下）
```

## 文档

- [一键安装.md](一键安装.md) —— 一句话进记忆体（用户只复制粘贴）。
- [dsh-新手起手式.md](dsh-新手起手式.md) —— 第一句「先去学 iLang，学完了再回来」；用户只做三件事：复制、粘贴、让 DSH 读官方文档。
- [mem-forever-dsh适配.md](mem-forever-dsh适配.md) —— 本仓库的适配方案与落地清单。
- [插件点评-ilang视角.md](插件点评-ilang视角.md) —— 用 iLang 的眼光看当前 DSH 插件生态：为什么说范式太老了。
- [ROADMAP.md](ROADMAP.md) —— 迭代协议：owner 丢来好技能/插件/文档，agent 按规则接入并推送。

## 协议

本仓库内的规则与记忆均以 [iLang v5.0](https://ilang.ai) 声明书写。上游协议与验收：`brain.py check` 0 错误；每笔记忆立即 commit + push。

## License

MIT（随上游 Mem-Forever）。
