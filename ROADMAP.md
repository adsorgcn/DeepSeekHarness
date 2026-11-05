# 迭代协议：owner 丢什么，这里长什么

> 这是给维护本仓库的 agent 的**长期任务书**。owner 看到好技能、好插件、好文章，随手丢过来；agent 按下面的方式把它迭代进本仓库，然后 commit + push。

## 接入规则（按东西的类型）

| owner 丢来 | 落点 | 动作 |
|---|---|---|
| 好技能（SKILL.md 等） | `.dsh/skills/<名字>/SKILL.md` | 补 `name`/`description` frontmatter，README 清单登记 |
| 可安装插件（bundle） | `plugins/<名字>/`（package.json + cordis.patch.yml） | 验证可安装，README 登记，附一句话安装说明 |
| 文档 / 点评 / 教程 | `docs/` 或仓库根（面向新手的中文文档放根） | README 文档列表登记 |
| MCP / 外部数据源 | `mcp/` 配置样例 | 密钥一律占位符（`YOUR_API_KEY`），真实密钥进 vault 或环境变量，绝不进文本 |
| 好 prompt / 起手式 | `.dsh/skills/` 或 `prompts/` | 同上 |

## 每次迭代的验收

1. `python -X utf8 tools/brain.py check` → 0 错误 0 警告（含密钥扫描）；
2. 逐笔 `git add` + `git commit -m "<type>: <what>"` + `git push`，不攒批；
3. 更新本文件上方的「已接入清单」和 README。

## 已接入清单（截至 2026-11-05）

- [x] 记忆体核心：Mem-Forever 2.1 模板（DSH 适配版）
- [x] 技能：`mem-forever`（`.dsh/skills/mem-forever/`）
- [x] 文档：`dsh-新手起手式.md`（起手式教程）
- [x] 文档：`mem-forever-dsh适配.md`（适配方案）
- [x] 文档：`插件点评-ilang视角.md`（旧范式点评）
- [x] 文档：`一键安装.md`（一句话进记忆体）
- [ ] 把仓库做成可 `github:` 一键安装的 DSH bundle（next）
- [ ] 好技能持续接入（长期，owner 驱动）

## 长期约定

- 本仓库是**公开模板**：不包含任何个人档案、真实密钥、私人记忆。
- 私人记忆属于 owner 的私有 brain（本地或私有仓库），与本仓库分离。
- owner 说「迭代进去」就按上面做，做完一句话汇报接入了什么、放哪了。
