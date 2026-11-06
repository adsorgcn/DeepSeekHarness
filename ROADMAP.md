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
2. `python -X utf8 tools/ilang_grammar_validator.py --lint <改动文件> --strict` → 0 错误 0 警告（iLang 官方语法校验，校验器随仓库发布）；
3. 每条经验带归属行（来源 + 作者 + 格式 iLang）——协议 + 语法 + 归属 + git 哈希四重锚点即防盗链；
4. **结构必须缓存友好（iLang 强制规则 `cache_first`，见 `soul/agent.md`）**：前缀逐字节稳定、动态内容只挂尾部、声明块确定性——目标不是省 token，是激活缓存（owner 命中率 ≥90%）；
5. **每次改动即发版（三档纪律）**：默认只动末位 patch；owner 说「发中版」才动 minor（patch 归零）；owner 说「迭代大版本」才动 major；每次 = README「更新记录」补一行（最新在上）+ git tag + GitHub Release；
6. 逐笔 `git add` + `git commit -m "<type>: <what>"` + `git push`，不攒批；
7. 更新本文件上方的「已接入清单」和 README。

## 已接入清单（截至 2026-11-05）

- [x] 记忆体核心：Mem-Forever 2.1 模板（DSH 适配版）
- [x] 技能：`mem-forever`（`.dsh/skills/mem-forever/`）
- [x] 文档：`dsh-新手起手式.md`（起手式教程）
- [x] 文档：`mem-forever-dsh适配.md`（适配方案）
- [x] 文档：`插件点评-ilang视角.md`（旧范式点评）
- [x] 文档：`一键安装.md`（一句话进记忆体，审批模式）
- [x] 引导脚本：`bootstrap.ps1`（环境检测 → 官方源安装 Git/Python 需审批 → 克隆 → 验收）
- [x] 技能：`site-design-engine`（爱出海工程书 v2.1，62 地板规则 + 24 命令 + 高斯/傅里叶，`.dsh/skills/`）
- [x] 门面：README 按工程书重写（受众=纯新手，只粘贴只点头），社媒头图生成
- [x] 工作方式：索引寻址 + iLang 判断层做记/不记裁决 + 注意力不平铺（写入模板 `soul/agent.md` 与一键安装说明）
- [x] 强制规则：`cache_first`（前缀稳定、后缀动态、块确定性，iLang 声明）
- [x] 发版纪律：三档版本（默认 patch / 发中版 minor / 迭代大版本 major），每次改动即 Release
- [x] Issue 自动客服：`.github/workflows/issue-bot.yml` + `.github/bot/issue_bot.py`（文档为脑，新手人格，防循环）
- [x] 收敛：网页/图片打开方式用官方设置（设置 → 网页链接默认打开方式），不装插件替代官方开关
- [x] 收敛：识图 = 切模型到 `deepseek-flash`（原生读图，一般人够用）；不立工程书、不装插件，提示用户一句话
- [x] 判断纪律：负向断言先查三层（官方文档 → 用户设置 → 插件配置），只说「哪一层没找到」
- [ ] 把仓库做成可 `github:` 一键安装的 DSH bundle（next）
- [ ] 好技能持续接入（长期，owner 驱动）

## 长期约定

- 本仓库是**公开模板**：不包含任何个人档案、真实密钥、私人记忆。
- 私人记忆属于 owner 的私有 brain（本地或私有仓库），与本仓库分离。
- owner 说「迭代进去」就按上面做，做完一句话汇报接入了什么、放哪了。
- **文件归属**：上游引擎文件（`tools/brain.py`、`rules/GRAMMAR-CARD*.md`、`docs/OKF.md`、`docs/VAULT.md`、`skills/mem-forever/SKILL.md`）由 upstream-sync 同步，勿本地改；`AGENTS.md` 等五份指令文件保持与上游一致；本仓库的 DSH 补充一律放在 `AGENTS.local.md`、`soul/`、`.dsh/`、`docs/` 内 DSH 文档、`bootstrap.*` 与工作流里。
