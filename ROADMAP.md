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
5. **每次改动即发版（三档纪律）**：默认只动末位 patch；owner 说「发中版」才动 minor（patch 归零）；owner 说「迭代大版本」才动 major；每次 = CHANGELOG.md 补一行（最新在上）+ git tag + GitHub Release；
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
- [x] 安装安全 v1.0.8：双端引导每步核验退出码、绝对路径执行、`-Yes` 确认门一致、完整身份检查、不覆盖未知目录；旧教程删 `.git` 路线废止
- [x] 国内镜像 v1.0.8：GitHub 不可达自动切 `gitee.com/monetize/DeepSeekHarness`，iLang 资料自动走 `ilang.cn`（按可达性探测，不按地区猜测）
- [x] 记忆推送保护 v1.0.8：`tools/guard-pre-push.sh` 钩子随克隆自动安装，私人记忆默认不可推送（`DSH_ALLOW_MEMORY_PUSH=1` 显式放行）
- [x] 技能：`site-design-engine`（爱出海工程书 v2.1，62 地板规则 + 24 命令 + 高斯/傅里叶，`.dsh/skills/`）
- [x] 门面：README 按工程书重写（受众=纯新手，只粘贴只点头），社媒头图生成
- [x] 工作方式：索引寻址 + iLang 判断层做记/不记裁决 + 注意力不平铺（写入模板 `soul/agent.md` 与一键安装说明）
- [x] 强制规则：`cache_first`（前缀稳定、后缀动态、块确定性，iLang 声明）
- [x] 发版纪律：三档版本（默认 patch / 发中版 minor / 迭代大版本 major），每次改动即 Release
- [x] Issue 自动客服：`.github/workflows/issue-bot.yml` + `.github/bot/issue_bot.py`（文档为脑，新手人格，防循环）
- [x] 客服升级：flash 最新版 + 每月官方模型检查（model-check 工作流）+ 回答后赠 iLang 解决方案工程书（母版格式，用户回填自己的 Agent）
- [x] 客服正确性 v1.0.9：追问优先、事件去重防重放、身份只认账号、评论分页、配额按尝试计、发布前实时重查
- [x] 工程书硬校验 v1.0.9：母版 v2.9 原文随仓库（gzip，带源哈希）、发送前官方语法校验 + 双标记 + 长度 + 完成原因，不合格不发
- [x] 模型检查升级 v1.0.9：显示名元数据比对（稳定别名底层换版可发现）、异常报警、提醒去重、iLang manifest 漂移检查
- [x] 行为测试 v1.0.9：`tools/test_bot.py`（16 场景全 mock）+ `.github/workflows/tests.yml`；R9 升级为真实机制校验
- [x] 文档口径 v1.0.10：隐私表述分层（本地默认不出网，出网仅模型请求与用户主动备份）；适配文档标注为历史现场记录
- [x] 上游同步 v1.0.10：`.dsh/skills/mem-forever/SKILL.md` 副本同步 + 回归门（brain check + rubrics + 行为测试不过不推）
- [x] 发布自愈 v1.0.10：tag 与 Release 分别检查，部分失败重跑自动补齐（仍全自动发版）
- [x] 决策纪律 v1.0.11：agent 先判定做/不做并给默认选择，owner 只答「做/过」，不提问（写入 AGENTS.local.md）
- [x] 视觉路由 v1.0.26：识图与深思考走官方子代理模型选择（`subagent-model-selection-settings` + `list_subagent_models` + `tools/clip_shot.*`），不装第三方视觉插件；输入框贴图在纯文本模型上被宿主拒收是 harness 行为，等官方
- [x] 收敛：网页/图片打开方式用官方设置（设置 → 网页链接默认打开方式），不装插件替代官方开关
- [x] 收敛：识图 = 切模型到 `deepseek-flash`（原生读图，一般人够用）；不立工程书、不装插件，提示用户一句话
- [x] 判断纪律：负向断言先查三层（官方文档 → 用户设置 → 插件配置），只说「哪一层没找到」
- [ ] 插件索引按官方机制（待官方机制稳定）：发布 `docs/plugins/index.json`（GitHub Pages 已在），按官方插件市场文档的格式列出本仓库 bundle（标题、图标、作者、版本、兼容 DSH 版本）；用户路径：DSH 插件页打开「自定义插件索引」→ 添加 `https://adsorgcn.github.io/DeepSeekHarness/plugins/index.json` → 在「发现」里装；做之前先在本机 DSH 实证一遍能装，实证不了就不发安装说明
- [ ] 好技能持续接入（长期，owner 驱动）

## 长期约定

- 本仓库是**公开模板**：不包含任何个人档案、真实密钥、私人记忆。
- 私人记忆属于 owner 的私有 brain（本地或私有仓库），与本仓库分离。
- owner 说「迭代进去」就按上面做，做完一句话汇报接入了什么、放哪了。
- **文件归属**：上游引擎文件（`tools/brain.py`、`rules/GRAMMAR-CARD*.md`、`docs/OKF.md`、`docs/VAULT.md`、`skills/mem-forever/SKILL.md`）由 upstream-sync 同步，勿本地改；`AGENTS.md` 等五份指令文件保持与上游一致；本仓库的 DSH 补充一律放在 `AGENTS.local.md`、`soul/`、`.dsh/`、`docs/` 内 DSH 文档、`bootstrap.*` 与工作流里。
- **国内镜像**：`gitee.com/monetize/DeepSeekHarness` 只作产品源，永不作私人记忆备份目标；镜像同步方式由 owner 决定（Gitee 官方镜像或手动 push），每次发版后核对两边 HEAD 一致。
- **记忆推送保护**：`bootstrap.*` 克隆后自动装 `tools/guard-pre-push.sh` 钩子；开发仓如需推送含 `soul/ memory/ handoff/ vault/ env/ projects/ mirror/ .ilang/ log.md` 的变更，先确认目标是私有仓库，再以 `DSH_ALLOW_MEMORY_PUSH=1` 或 `git config --bool dsh.allowMemoryPush true` 显式放行。
- **DSH 版本行**：每次发版同步更新 README 与落地页的「在 DeepSeek Harness X 上验证」一行（X 取自本机 DSH 关于页或 package.json，取不到写「未记录」，不要猜）。
- **引用规范**：凡用到/引到的算法与组件都按 docs/CITATIONS.md 挂 DOI/arXiv；作者有公开 ORCID 的做 ORCID 锚文本；查不到写「未查到」，不编造；仓库自身 DOI 由 Zenodo 发布 webhook 自动铸；写 DSH 有什么功能以 deepseek-ai/deepseek-harness 仓库为准，查不到不写。
