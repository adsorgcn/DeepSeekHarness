# 用 iLang 的眼光看 DSH 插件生态：范式太老了

> 材料：《DeepSeek Harness 实测必装 8 款插件 + 24 小时无人值守 SuperAgent》《最值得装的 5 个插件》《dsh-prompt-inject》《歸藏设计》等近期公众号文章。

## 一句话结论

**这些插件都在给 agent「装手」（能力焊死在代码里），而 iLang / Mem-Forever 在给 agent「装脑」（行为即数据：记忆是文件、规则是声明、判断在代码、合并有人审）。** 手永远有用，但范式之争不在手，在脑。

## 逐条对照：旧范式的问题，与新范式的位置

| 文章里的插件 | 旧范式的问题 | iLang / Mem-Forever 的做法 |
|---|---|---|
| dsh-mnemon 长期记忆（本地 SQLite+向量） | 记忆锁死在单个插件的私有格式里：git 看不见、别的工具读不到、格式作者说了算 | `memory/*.md` + `::FACT`/`::LESSON`/`::GENE` 声明：人可读、`git diff` 可审、任何工具可迁移 |
| dsh-prompt-inject 全局提示词注入 | 规则是一段没有语法、没有 conf/scope、没有审查的裸文本 | `::GENE{conf|scope}` + `T:`/`A:` 行；`::BOUNDARY{never}` 硬边界，不许加 `when:`、不许绕过 |
| cc-safety-net 拦截危险命令黑名单 | 黑名单永远不完整，规则焊在代码里改不动 | `::BOUNDARY{never:force-push main|scope:project}`——边界是数据，可寻址、可审查、可版本化 |
| SuperAgent 三道围栏（白名单/测试必过/人点合并） | 安全体系为一个应用手搓在代码里 | 「合并按钮必须由人来点」就是 iLang 的 `authority:commit`——v4 三级权威 + v5 的 M1–M8，被私刻成了三堵具体的墙 |
| dsh-skills-manager 技能热加载 | 工具为中心，管理的是「手的清单」 | 知识以 `scope:`/`when:` 声明按需生效——Mem-Forever 的记法卡才 400 token，因为它是声明不是清单 |
| sidebar / image-gen / 主题皮肤 | 无协议，纯能力 | 这些本身没错——它们是手；问题在于只有手，没有脑 |

## 三条更深的判断

1. 《最值得装的 5 个插件》自己写了句大实话——「多数时候，你缺的不是插件」。翻译成 iLang 的 DNA 模型：你缺的是 **B（蓝图）和 ∫S（持久记忆）**，不是又一只手。
2. SuperAgent 是这批里最接近新时代的——Router/Worker/自愈/终审权，但它的安全是应用级硬编码。Mem-Forever 把它推广成了协议：**judgment before action, review before merge**——模型只写候选交接单（proposal），`brain.py` 逐块审查（code），owner 决定接受（authority）。这正是 v4 STATUS 三级权威在记忆上的实例化。
3. 连「把 persona 写进 preset」都还是旧范式动作——Mem-Forever 的做法是 persona 成为 `soul/agent.md` 里一个带版本号与哈希、verbatim 保存、可审查的文件。

## 分野

- 旧：装插件 = 装能力（每装一个 = 焊死一条规则/一份记忆/一个能力）。
- 新：装协议 = 装记忆与判断（一份声明文件 = 任何模型、任何工具通用）。
- 旧范式的记忆「属于插件」；新范式的记忆「属于你」——每一笔都是一次可读、可审、可迁移的 git 提交。
