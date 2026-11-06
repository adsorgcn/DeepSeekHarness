# 更新记录（每次改动即发版）

**v1.0.19** · 2026-11-06 · 自家 DOI 与 ORCID 锚点闭环

- 本仓库 concept DOI：[10.5281/zenodo.23998664](https://doi.org/10.5281/zenodo.23998664)（Zenodo 自动归档已生效，README 挂徽章，CITATION.cff 加 identifiers）
- CITATIONS.md：26 位 DeepSeek 作者已核实 ORCID 逐个挂链；Wenfeng Liang / Alec Radford / An Yang 经核查无公开 ORCID，如实标注不编造

**v1.0.18** · 2026-11-06 · Zenodo 自动 DOI 启用

- owner 已在 GitHub 启用 Zenodo 自动归档；CITATIONS.md 记录启用状态；本版发布即触发首次归档，DOI 铸成后回填徽章

**v1.0.17** · 2026-11-06 · R4 检查器适配引用条目

- `tools/check_rubrics.py` 的 R4 改为精确检查 CFF 的 `title:` 行（references 里引用 Mem-Forever 全名是合法引用，不再误报）

**v1.0.16** · 2026-11-06 · 全量 DOI / arXiv / ORCID 引用

- 新增 [docs/CITATIONS.md](docs/CITATIONS.md)：直接依赖（iLang、Mem-Forever、母版、校验器）、模型（DeepSeek-V4/R1/V3、Qwen3、Whisper）、延伸阅读（DSec）、标准组件（gzip/age/Git）全带 DOI/arXiv 锚点，作者有 ORCID 的挂 ORCID
- README 加「引用与致谢」块；落地页页脚改 DOI 链接；CITATION.cff 加 7 条 references（含 DOI）；.zenodo.json 加 5 条 cites 与 7 条 references
- 核实记录：Wenfeng Liang 无公开 ORCID（不编造，锚 arXiv 提交人页）；本仓库自身 DOI 待 owner 授权 Zenodo 后自动铸

**v1.0.15** · 2026-11-06 · 免费全家桶（数据驱动可选安装器）

- 新增 `.dsh/free-station.json` 注册表 + `tools/free_station.py`：plan（只检测）/ install（逐项审批、官方源、失败即停、装后验证）/ status
- 条目：Ollama + Qwen3 8B（本地备用）、yt-dlp、FFmpeg、Obsidian（winget/brew 官方包，id 已逐一验证）
- 零安装集成：语音（DSH 自带转写 + 系统朗读）、Gemini Notebook（导出交接单）
- 行为测试 `tools/test_free_station.py`（7 场景）进 CI；默认 bootstrap 安装计划不变

**v1.0.14** · 2026-11-06 · 发版摘要取对 Gitee HEAD

- `release-on-version-change.yml`：摘要里的 Gitee HEAD 改用「取第一个 sha」的方式（grep -o + head -1 + cut），修掉 sed 贪婪匹配取到父提交的 bug（审计 DSH-FIX-D1）

**v1.0.13** · 2026-11-06 · SEO 与仓库门面

- 仓库 About：双语简介 + 官网地址 + 20 个主题标签（deepseek、ilang、ai-memory、persistent-memory、tutorial 等）
- 落地页 `<head>`：关键词标题、描述、canonical、Open Graph / Twitter 卡片（配 social-preview.png）
- README 顶部双语关键词句；方便 GitHub 搜索与社交分享卡片识别

**v1.0.12** · 2026-11-05 · 审计第三轮 DSH-FIX-B1-C6

- C1 推送保护钩子覆盖 projects/ mirror/ .ilang/，并认 `git config dsh.allowMemoryPush` 放行
- B9 客服把 issue 文本当数据；B10 维护者不触发、上下文换新手文档（行为测试 18 场景）
- B1 三处合成同一句安装话；B3 装完亲眼看它记得；B2 本机模式默认（push 地址 DISABLED）+ 备份模式规则
- C2 记 dsh.source、克隆失败自动换 Gitee 重试；B7 卸载；B6 密钥库标进阶可选
- B4 引擎更新一句话 + 不动记忆的做法；B8 验证 DSH 版本行（0.2.2-rc.1，取自本机 package.json）
- B11 更新记录移 CHANGELOG.md；C3 手动路线 bash 语法修复；C4 决策流装/推/删/出网写不算安全默认
- C6 删死工作流、同步工作流写明权限；C5 月检带 Gitee 镜像漂移、发布打印双 HEAD；B12 bundle 项改官方插件索引机制（待实证）

**v1.0.11** · 2026-11-05 · 决策纪律入 DNA

- `AGENTS.local.md` 新增决策流：思考全部由 agent 完成，只把结论与推荐摆到 owner 面前；owner 零思考，只回答「做」或「过」；agent 不再提开放式问题；有安全默认时不阻塞等待

**v1.0.10** · 2026-11-05 · 文档口径 + 运维自愈

- 隐私表述分层：本地记忆默认不联网，出网仅模型请求与你主动配置的备份；密钥只进本机加密 vault
- 适配文档标注为历史现场记录，不再当作新用户验收
- 上游同步：`.dsh` 技能副本同步 + 回归门（brain check、rubrics、行为测试不过不推）
- 发布自愈：tag 与 Release 分别检查，部分失败重跑自动补齐（仍全自动发版）

**v1.0.9** · 2026-11-05 · 客服正确性 + 工程书硬校验

- 追问优先：新评论为问题、原 issue 为背景；回复带事件标记，同一事件重跑不重复回复
- 身份只认账号，普通用户贴标记不能冒充；评论分页取全、每日/每 issue 配额按尝试计；发布前实时重查 issue 状态
- 工程书按母版 v2.9 原文生成，发送前硬校验：官方语法校验器 0 错误 + 首尾双标记 + 长度上限 + 完成原因；不合格只发答案不发书
- 模型检查升级：稳定别名底层换版也能发现（比对显示名等元数据）；无 flash 型号、别名消失、manifest 漂移都会报警且提醒去重
- 新增行为测试 `tools/test_bot.py`（16 个场景）与 tests 工作流；R9 检查器从「搜字符串」升级为真实机制校验

**v1.0.8** · 2026-11-05 · 安装安全 + 国内镜像

- 引导脚本：每步核验退出码、失败即停；探测到的程序用绝对路径执行；`-Yes` 确认门双端一致生效；「已安装」改为完整身份检查，不覆盖未知目录
- GitHub 不可达自动切国内镜像 gitee.com/monetize/DeepSeekHarness，iLang 官方资料自动走 ilang.cn（按实际可达性探测，不按地区猜测）
- 克隆后自动装记忆推送保护钩子：私人记忆默认拦在本地，只有你确认的私有仓库才能备份
- 删除旧教程「删 .git 重建」的不安全路线，统一到安全引导

**v1.0.7** · 2026-11-05 · 客服评论路径修复

- 修复 `issue_comment` 事件的 action 判断（事件名 ≠ payload 里的 action），人工评论现在能正确触发回复

**v1.0.6** · 2026-11-05 · 客服升级

- 客服改用 flash 最新版（`.github/bot/MODEL.txt` 锁定，每月 1 日自动对照官方模型列表，落后自动开 issue 提醒）
- 每次回答后尝试赠送「解决方案工程书」（iLang 母版格式；v1.0.9 起发送前硬校验，此前版本未校验）

**v1.0.5** · 2026-11-05 · 审计修复 A1-A9

**v1.0.4** · 2026-11-05 · 识图收敛

- 看不了图 = 一句话提示切 `deepseek-flash`（原生读图，一般人够用）；不搞 OCR 绕路、不装插件

**v1.0.3** · 2026-11-05 · 判断纪律

- 负向断言三层核查（官方文档 → 用户设置 → 插件配置），只报「哪一层没找到」；收敛项：链接打开方式用官方设置，不装插件

**v1.0.2** · 2026-11-05 · Issue 自动客服上线

- GitHub Actions 客服 bot：新 issue 与人工评论自动回复；以仓库文档为脑、新手人格为守则，不知道就说不知道，防循环、防刷屏

**v1.0.1** · 2026-11-05 · 版本纪律确立

- 三档版本规则：每次改动默认只动末位（patch）；owner 说「发中版」才动中间（minor）；owner 说「迭代大版本」才动前面（major）

**v1.0.0** · 2026-11-05 · 首发

- 记忆体：Mem-Forever 2.1 的 DSH 适配版（AGENTS.md 自动注入、技能挂载、brain.py 验收）
- 新手教程、插件点评、适配文档
- 一键安装：`bootstrap.ps1`（官方源安装 + 审批模式），环境、仓库、记忆一次到位
- 落地页：GitHub Pages，按 site-design-engine 工程书建成，独立评审修复后上线
- 技能：`mem-forever`、`site-design-engine`；官方 iLang 语法校验器随仓库发布
- 内置工作方式：索引寻址、可逆性裁决、注意力不平铺、iLang 交叉验证、cache_first
