# 迭代协议：owner 丢什么，这里长什么

> 这是给维护本仓库的 agent 的**长期任务书**。owner 看到好技能、好插件、好文章，随手丢过来；agent 按下面的方式把它迭代进本仓库，然后 commit + push。

## 接入规则（按东西的类型）

| owner 丢来 | 落点 | 动作 |
|---|---|---|
| 好技能（SKILL.md 等） | `.dsh/skills/<名字>/SKILL.md` | 补 `name`/`description` frontmatter，README 清单登记 |
| 合作方的工程书或技能 | `.dsh/books/<名字>/BOOK.md` 或 `.dsh/skills/<名字>/`，登记在 docs/market/registry.json | 跑 tools/market_admit.py，ADMIT 且 owner 说收，原样内置并钉版本；用户装了工具包就有，不用挑 |
| 不合作的第三方好东西 | docs/社区插件甄选.md | 只给作者的仓库地址与官方原话，名单由 owner 挑；怎么用让用户的 DSH 自己处理 |
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
- [x] 记忆引擎 3.1 v1.1.2：brain.py 2.1、账本 env/ledger.env（值静态编码，用 env/pepper 可逆，不是加密）、本机授权、hooks 并入 tools/hooks、市场登记 3.1.0
- [x] 记忆推送保护 v1.0.8：钩子随克隆自动安装，私人记忆默认不可推送（显式放行）
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
- [x] 视觉路由 v1.0.27：新手默认 Flash，截图直接贴；视觉路由（看截图→Flash 子代理）是 Pro 开发者路线；输入框贴图在纯文本模型上被宿主拒收是 harness 行为，等官方
- [x] 视频转文字 v1.0.28：本地化（tools/transcribe.py + SenseVoice sherpa-onnx，与 DSH 语音输入同款），Whisper 不进默认包；视频号与快手 yt-dlp 不支持，提示给文件
- [x] 第三方吸收规范 v1.0.31：欢迎好产品——进全家桶=装前问+官方源+CITATIONS 署原作者（首个：REA，morluto/rea，MIT）
- [x] 社区插件甄选 v1.0.32：docs/社区插件甄选.md 只收录 REA；与官方能力重复、要钥匙或记忆、娱乐不稳定的一律不收（署名只给开发者，不给转发者）
- [x] 第三方边界 v1.0.34：市场收录规则 v1——只给官方信息与官方入口、一律可选、不写装法用法例句、署名给原作者、无利益往来；REA 为首个样板（退回零安装入口）
- [x] 收录样板二 v1.0.41：dsh-media-desk（woniuniuniu，MIT）按市场收录规则 v1 入库，三处署名
- [x] 技能：deai（iLang 自家 DeAI 1.6.0 原样内置，.dsh/skills/deai/，upstream.json 钉 tag 与哈希，更新只换 tag，DOI 10.5281/zenodo.24028757；数字两档：公共数字搜索带出处或不写，个人数字不碰）
- [x] 指导站入口 v1.0.37：README 与一键安装.md 指向 ilang.cn/guide/dsh/（备案域名，微信与 QQ 里可分享）；未备案的镜像域名一律不进仓库；面向国内用户的 iLang 链接一律 ilang.cn
- [x] 落地页域名 v1.0.40：dsh.ilang.guide（GitHub Pages 自定义域名，DNS 在 owner 这边，仓库里只有 docs/CNAME，HTTPS 强制）；国内分享链接仍是 ilang.cn/guide/dsh/
- [x] 收敛：网页/图片打开方式用官方设置（设置 → 网页链接默认打开方式），不装插件替代官方开关
- [x] 收敛：识图 = 切模型到 `deepseek-flash`（原生读图，一般人够用）；不立工程书、不装插件，提示用户一句话
- [x] 判断纪律：负向断言先查三层（官方文档 → 用户设置 → 插件配置），只说「哪一层没找到」
- [x] 市场 v1.1.0：docs/market/（registry.json 登记自家技能；market_admit.py 准入；不排名不爬虫不收 PR）
- [x] 货架 v1.1.6：市场改成货架。过了门、owner 说收的技能与工程书原样内置进工具包，用户装了就有，不用挑；撤掉官方格式的插件索引；不合作的第三方只给作者仓库地址；用户想加源或看见别处不错的技能、插件时，agent 提示帮他写一版更好的，照 iLang 母版写成工程书，写好可提交送审；准入脚本与测试改成查工程书
- [x] 工程书：AI全球自媒体 0.1.1（`.dsh/books/ai-global-media/`，说一句「AI全球自媒体」开始；这一版做两环：装公众号爆文专家定成人格，接上内容源）
- [ ] 好技能持续接入（长期，owner 驱动）

## 长期约定

- 本仓库是**公开模板**：不包含任何个人档案、真实密钥、私人记忆。
- 私人记忆属于 owner 的私有 brain（本地或私有仓库），与本仓库分离。
- owner 说「迭代进去」就按上面做，做完一句话汇报接入了什么、放哪了。
- **文件归属**：上游引擎文件（`tools/brain.py`、`rules/GRAMMAR-CARD*.md`、`docs/OKF.md`、`docs/VAULT.md`、`docs/LEDGER.md`、`docs/PRODUCT.md`、`skills/mem-forever/SKILL.md`、`tools/hooks/pre-commit`、`tools/hooks/pre-push`、`tools/test_brain.py`、`env/README.md`）由 upstream-sync 同步，勿本地改；五份指令文件、`.dsh/skills/mem-forever/SKILL.md` 副本与 `MARKET.md` 围栏由同步工作流生成（instructions sync / cp / market_build），勿手改；本仓库的 DSH 补充一律放在 `AGENTS.local.md`、`soul/`、`.dsh/`、`docs/` 内 DSH 文档、`bootstrap.*` 与工作流里。
- **国内镜像**：`gitee.com/monetize/DeepSeekHarness` 只作产品源，永不作私人记忆备份目标；镜像同步方式由 owner 决定（Gitee 官方镜像或手动 push），每次发版后核对两边 HEAD 一致。
- **记忆推送保护**：`bootstrap.*` 跑 `brain.py init .` 装 `tools/hooks` 的两只钩子；提交前 review 加 check，推送前核远端私有（GitHub 与 Gitee 自动核，其他远端一次性确认）；开发仓对公开 origin 一次性 `git config --bool brain.allowPush.origin true`。
- **DSH 版本行**：每次发版同步更新 README 与落地页的「在 DeepSeek Harness X 上验证」一行（X 取自本机 DSH 关于页或 package.json，取不到写「未记录」，不要猜）。
- **引用规范**：凡用到/引到的算法与组件都按 docs/CITATIONS.md 挂 DOI/arXiv；作者有公开 ORCID 的做 ORCID 锚文本；查不到写「未查到」，不编造；仓库自身 DOI 由 Zenodo 发布 webhook 自动铸；写 DSH 有什么功能以 deepseek-ai/deepseek-harness 仓库为准，查不到不写。
