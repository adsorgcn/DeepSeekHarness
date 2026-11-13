# 更新记录（每次改动即发版）

**v1.1.24** · 2026-11-13 · 主书 0.2.5：内容源加 AI 破局与自拉热点，视角卡加易洋；货架钉官方插件 0.2.3

- 第二环改成两层：先自己拉热点（专家包自带的 `hot_sources.py` 加 83 个公开源，在用户机器上跑，落 `library/feed/<日期>.json`，不读任何网站的文件），再选案例库：生财有术 / AI 破局俱乐部 / 两家都接 / 先不接。先不接的也能走到第一篇
- AI 破局照生财那条复刻：装官方 CLI（没有 Node 先装 Node，走免费全家桶注册表，先问用户同意）→ `breakout auth login --no-browser` 打印链接，用户本人在浏览器点「确认登录」→ DSH 照官方文档把一条 MCP 客户端条目（stdio 跑 `breakout mcp serve`）合并进用户 patch 层，不装别的插件 → 只读搜一次列标题。能力名先查清单再调，不写死；写操作永不调；不用浏览器碰官网
- 视角卡二选一：亦仁默认，易洋可选。易洋那张在 `.dsh/books/ai-global-media/lens-yiyang.md`，13 组规矩 43 条，每条带他原帖或 AI 洋哥回答的原话做证据，不用词频。写稿工具还是公众号爆文专家，不动
- 海报多一张 `poster-poju.jpg`（破局七天会员）。验收项 B3 B6 B7 改，加 B15 B16 B17；FALLBACK 加三条、改一条；BOUNDARY 加两条（破局只读、不用浏览器碰官网）
- 免费全家桶注册表加 node（winget OpenJS.NodeJS.LTS）和 breakout-cli（npm）两条，各带 verify
- 货架：registry.json 的 plugin 条目钉 dsh-plugin-chuhai 0.2.3（integrity、发包提交、tag v0.2.3）；index.json 顶部加 0.2.3；市场页那一行跟着改。插件 0.2.3 随带的书、视角卡、两张海报和这里的同哈希，目录里报出随带文件的位置
- 来源：2026-11-12 @SUN 工程书 AI-GLOBAL-MEDIA-025-BRIEF-E1-E3 v1.1；破局那条在官方 DSH 命令行沙盒验过：DSH 自己照文档把条目写进用户 patch 层，新开一个会话 15 个工具出现、一次调用拿到账号

**v1.1.23** · 2026-11-12 · 市场页每行末尾的小标签删了（F53）

- 每行末尾的 m-kit 小标签（随工具包 / 贴那句话时顺手装上）与它的「 · 」分隔符一并删掉；节标题与每节下面的那句已经说了同一件事，不再逐行重复

**v1.1.22** · 2026-11-12 · 货架钉住官方插件 0.2.2（integrity、发包提交、tag）；market_admit 加 --plugin

- registry.json 加 plugin 门：钉 npm 包的 integrity（必须等于 registry.npmjs.org 的 dist.integrity）、发包提交的 40 位 commit 和 tag；dsh-plugin-chuhai 条目钉 0.2.2
- docs/market/index.json 的 versions 顶部加 0.2.2；市场页官方插件行加版本、integrity 前 16 位与 Release 链接
- market_build 认 kind plugin（必填 npm.*/upstream.*，sha 与校验记录跳过）；market_admit 加 --plugin：核 npm 的 integrity 与 gitHead=tag，只读包不跑代码
- test_market 加 plugin_pin 与索引版本一致性断言（14 场景全过）
- 插件那边的改动：分页 与 两处措辞（0.2.2）

**v1.1.21** · 2026-11-12 · 记忆的门认给定人格；交接单模板占位符不算条目；主书 0.2.4

- 记忆的门（`brain.py review` 和 `provenance`）：`soul/agent.md` 的「Part one · given soul」整段按用户给的算——里面的 BOUNDARY 和 A: 行不用补来源，换新版人格时旧边界跟着走；`provenance init` / `repair` 不碰这一段。此前第一环装专家人格一提交就被拦（正文里 28 行 A: 加 1 条 BOUNDARY 没有 by:），只能往正文里加键，记下的 sha256 就对不上原文了
- 交接单：模板里 `<...>` 这种占位符不再当成条目，第一次写真实进度不会被「dropped without a word」拦下
- 主书 0.2.4：取专家包后用 git status 核一次就算取到，不再因退出码回退；人格正文不补来源，门拦了先更新工具包；ima 技能包解压后先删 .DS_Store
- 官方索引列上 dsh-plugin-chuhai 0.2.1（随带的书同为 0.2.4），市场页那行跟着改
- 工具包测试加两条（给定人格过门与整块替换、模板占位符不算条目）；来源：2026-11-12 另一台电脑上 DS 从 dsh.ilang.guide 走一遍的报告，三步、第一环、第二环都通，报的三个点两个是真问题

**v1.1.20** · 2026-11-12 · 官方插件 0.2.0：能单独用了

- `docs/market/index.json` 列上 dsh-plugin-chuhai 0.2.0（0.1.0 保留）：前半段的书「AI全球自媒体」随插件带着，不先装工具包也能走；两本书都按段取，不再撞 DSH 工具结果的长度上限
- 市场页那一行跟着改
- 刚发的版本 pnpm 有一段等待期，等待期内不钉版本号装到的还是上一版；DSH 的安装完成页会写明两个版本并给出该装的精确 `名字@版本`，照它说的装一次就是新版

**v1.1.19** · 2026-11-12 · 第一个官方插件上架：自媒体出海

- 官方插件 dsh-plugin-chuhai（npm）：说一句「自媒体出海」，从装好工具包一直带到 X 开蓝 V；出海那段书不在这个仓库里，插件自己去取
- 那句话多一步：装完顺手把官方插件装上（问一次）；入口指令开场看一眼装没装，没装问一句
- 市场：`docs/market/index.json` 恢复 DSH 官方索引格式（实验性插件里添加这条索引源就能看到），市场页加「官方插件」区
- 首页：三步旅程（装 DSH、贴那句话、说「自媒体出海」）加一行「目前进度：到 X 开蓝 V，更新中」

**v1.1.18** · 2026-11-12 · 引擎更新补上 .cursorrules

- 引擎更新那条命令的清单加上 `.cursorrules`；更新到这一版之后，以后每次更新五份入口指令一起换新，不再多出一条警告

**v1.1.17** · 2026-11-12 · 更新记录重新上传

- CHANGELOG.md 重新上传；工具包内容不变

**v1.1.16** · 2026-11-12 · 更新记录精简

- v1.1.14、v1.1.15 两条改短；工具包内容不变

**v1.1.15** · 2026-11-12 · 内容回到 v1.1.13



**v1.1.3** · 2026-11-08 · 1.1.2 的标签缺两份派生指令文件，1.1.3 补齐

**v1.1.2** · 2026-11-08 · 记忆引擎升 Mem-Forever 3.1（审计 DSH-MEM3-ADAPT-A1-A8）

- 修每周同步：原 checkout 名单里有上游不存在的 `.dsh/skills/mem-forever/SKILL.md` 路径，整条命令 pathspec 失败、什么都同步不进来；新工作流只取上游引擎文件，五份指令文件由 `instructions sync` 从技能正文生成，`.dsh` 副本由 cp 得到，市场登记由 market_build 刷新
- 引擎升 2.1：账本 env/ledger.env 一行一扇门，值静态编码（enc1，用 env/pepper 可逆，不是加密），本机授权走 git config（brain.py grant），密钥扫描改 WARN 加 ledger harvest 收割，不再拒提交；新文件 docs/LEDGER.md、tools/hooks/pre-commit 与 pre-push、tools/test_brain.py、.gitattributes
- 推送保护并入 3.1 钩子：tools/guard-pre-push.sh 退场，bootstrap 跑 brain.py init .；提交前 review+check，推送前核远端私有（GitHub/Gitee 自动核，其他远端一次性确认）
- 市场登记 mem-forever 升 3.1.0：skill 版本跟随 procedure frontmatter，MARKET.md 围栏由构建脚本自动与技能正文对齐
- 自家文案去掉 2.1 说法（docs/README.zh.md 三方套用、适配.md、CITATIONS 加 3.1.0 版本 DOI）；CI 加 Brain engine tests 与 Instruction files identical 两步

**v1.1.1** · 2026-11-08 · 市场文案与布局修正（审计 DSH-MARKET-FIX-S1-S4）

- 否定排比换肯定句：市场页副题/meta/og/twitter/作者段末句按书逐字替换；落地页市场一幕同口径
- 句号归位：索引地址的 code 块独立成行；落地页市场一幕改整宽居中（去分栏与内联样式）
- 构建脚本补两种渲染态：有行时给出官方三步（自定义插件索引/添加索引源），空态只给索引地址；index.json 描述同口径（收录顺序就是显示顺序）
- 测试加到 11 场景（page_copy、render_states）；site-design-engine 全新上下文两页评审

**v1.1.0** · 2026-11-07 · 市场上线（审计 DSH-MARKET-P1-P7）

- docs/market/：registry.json 登记三条自家技能（mem-forever / site-design-engine / deai），index.json 按官方格式 1 只收 iLang 合规 bundle（清单过官方校验器 strict 0 错 0 警告，钉 commit，许可在案），市场页 https://dsh.ilang.guide/market/ ，索引地址 https://dsh.ilang.guide/market/index.json ；不排名、不看星数、不爬虫、不收 PR
- tools/market_admit.py 准入（ADMIT/REJECT），tools/market_build.py 生成（--check 只校验），tools/test_market.py 九场景进 CI，ISSUE_TEMPLATE 市场准入申请
- mem-forever 增加 MARKET.md 围栏副本（与 SKILL.md GENE 逐字一致，测试比对）；AGENTS.local 加 dsh_market GENE；README、落地页、甄选页各接一处
- 三个此前未发版的门面提交（品牌统一、SEO、窄屏可读性）随本版一并发出

**v1.0.44** · 2026-11-07 · deai 数字两档（审计 DSH-DEAI-NUMBERS-N1-N4）

- 上游升 v1.6.0（MARK 1.4.0：STEP_3d 改数字两档，去掉 [📊] 标记，RUBRIC 加 no_number_blanks_or_estimates），4 个文件重新 vendor，其余 7 个不变
- 撤掉 v1.0.43 的「估算并标明」口径：个人数字估算等于编造（实测证据：年限、学员数、客单价、续费率全被写成估算数字）；新口径与上游同——公共数字搜索带出处和日期或不写，个人数字不碰：不估、不标、不问

**v1.0.43** · 2026-11-07 · deai 数字口径修正

- 数字类一律搜索权威信息；没有数据时按上下文相关信息估算并标明；绝不把数字留给用户填（覆盖上游 3d，写在技能清单与 dsh_deai GENE，上游文件未动）

**v1.0.42** · 2026-11-07 · 内置 DeAI 1.5.1 技能（审计 DSH-DEAI-EMBED-M1-M7）

- .dsh/skills/deai/：上游 11 个文件原样 vendor（upstream.json 钉 tag v1.5.1 与 LF 归一哈希，更新只换 tag）；技能清单 SKILL.md（去 AI 味，默认 MARK 只标不写，指纹是方言不是脏字）
- AGENTS.local 加 dsh_deai GENE；起手式、README、落地页各提 deai；SUN 画像只在用户点名 profile=SUN 时用
- 三处引用登记 DeAI DOI（10.5281/zenodo.24028757 概念 / 10.5281/zenodo.24028758 版本）；新增 tools/test_deai.py 六场景进 CI

**v1.0.41** · 2026-11-07 · 收录样板二：dsh-media-desk

- 社区插件甄选按市场收录规则 v1 收录 dsh-media-desk（woniuniuniu（蜗牛的科技笔记），MIT，已核仓库 LICENSE）；只给官方描述与官方仓库入口，署名三处登记

**v1.0.40** · 2026-11-07 · 落地页域名 dsh.ilang.guide，README 对齐落地页叙事（审计 DSH-LANDING-DOMAIN-L1-L4）

- docs/CNAME＝dsh.ilang.guide；Pages 自定义域名已设、证书已签、HTTPS 强制；DNS 在 owner 这边（仅 DNS 不代理）；国内分享链接仍是 ilang.cn/guide/dsh/
- README 重写成与落地页同一条叙事：许愿、那句话、验收时刻、里面有什么（记忆体、新手教程、一键安装、技能库）、以后每个新窗口、放心；在线门面换成 https://dsh.ilang.guide/ ，指导站行不动；事实、链接、引用与致谢不变
- docs/index.html 补回看图口径（新手用 Flash，截图直接贴；说「认真想」才请 Pro）与视频转文字口径，v1.0.35 的改版把这两句丢了

**v1.0.39** · 2026-11-07 · 落地页叙事改版（对标苹果发布会：一屏一意，许愿、证据、验收、那句话）

- docs/index.html：开场只卖结果，安装指令移到独立一幕「那句话」（整句展开，不再滚动）；新增「新手教程」一幕（第一句先学 iLang，四句话照抄）和「验收时刻」一幕（关掉窗口重开，第一句就是汇报）；三个样机统一为桌面窗口，去掉手机壳；「基于」一栏改为 iLang · Mem-Forever · DeepSeek Harness；视觉系统、隐私与收尾不变；零外部加载，外链主机集合不变

**v1.0.38** · 2026-11-07 · 记录措辞去未备案域名字样

- ROADMAP 与 CHANGELOG 里说明句不再出现未备案域名字样（该字样本不该出现在仓库任何文件里）

**v1.0.37** · 2026-11-07 · 指导站入口（审计 DSH-GUIDE-ENTRY-K1-K3）

- README 与一键安装.md 各加一行指向 https://ilang.cn/guide/dsh/ （备案域名，微信与 QQ 里可直接分享；未备案域名一律不进仓库）

**v1.0.36** · 2026-11-06 · 落地页线框去版本号

- docs/index.html 记忆体线框里「v1.0.34 已发布」改为「引擎已更新到最新」，避免展示过期版本号

**v1.0.35** · 2026-11-06 · 落地页改版（暗色一屏一意，工程书 DSH-LANDING-REDESIGN v1.0）

- docs/index.html 重建：黑底白字大标题、橙色 #FF4400 品牌色、一屏一意渐进滚动、手机/笔记本 CSS 线框、复制按钮与淡入动效、零外部依赖（系统字体）；全部文案沿用现行核准口径（技能库卡不用已撤的「迭代进去」旧文案）

**v1.0.34** · 2026-11-06 · 第三方边界与市场收录规则 v1（审计 DSH-THIRD-PARTY-BOUNDARY-J1-J6）

- REA 从全家桶安装条目退回零安装入口（zero_install）：只给官方入口，撤装法/验法/用法/例句/分级；署名三处保留
- docs/社区插件甄选.md 改为收录规则 v1（六条），REA 为首个样板条目（官方原话+直译+入口+可选+署名）
- AGENTS.local.md 新增 dsh_third_party_boundary GENE：第三方只给官方信息和官方入口，一律可选，用法问官方文档，署名给原作者
- transcribe.py 自检重执行补 -X utf8（Windows 控制台中文不乱码）

**v1.0.33** · 2026-11-06 · REA 许可证从源仓库核实

- 社区插件甄选：REA 的 MIT 许可证改为「已拉取仓库 LICENSE 核实（Copyright (c) 2026 morluto）」

**v1.0.32** · 2026-11-06 · 社区插件甄选文档

- 新增 docs/社区插件甄选.md：只收录 REA（morluto/rea，MIT）；原则三不收（与官方能力重复、要钥匙或记忆、娱乐不稳定）；署名只给开发者，不给转发者

**v1.0.31** · 2026-11-06 · 吸收第三方优质产品：REA 进全家桶（装+推荐+署名）

- 免费全家桶新增可选条目 REA（morluto/rea，MIT；npx 官方安装，装前问，需 Node.js，新手不必装）
- 起手式加「怎么把话说清楚」三件套（指目标→要证据→要复现，范式署名 REA 官网）+ REA 例句行；一键安装进阶清单同步
- CITATIONS.md / CITATION.cff / .zenodo.json 三处署 REA 原作者；AGENTS.local 记规矩：吸收第三方必须装前问+官方源+署原作者

**v1.0.30** · 2026-11-06 · 视频转文字修复版（审计 DSH-VIDEO-TEXT-FIX-I1-I7）

- transcribe.py 去掉 numpy（标准库 array 转 PCM16）；照官方例子补 EOF flush、边喂边取段、VAD 参数 0.2/0.25/5、0.1 秒读窗（修掉丢尾段与段首字被吃）
- free_station 的 python 命令改为当前解释器（macOS 12.3+/Ubuntu 无 python 命令也能装）
- asr_setup：模型包只下一遍、流式落盘核哈希、自检音频入库、silero_vad 加 csukuangfj/vad 镜像（两哈希都认）
- 引擎与模型搬到用户目录 ~/.deepseekharness/asr，装完 brain check 仍 0 退出；`--selftest` 一句话自检（SELFTEST OK）

**v1.0.29** · 2026-11-06 · 首页全家桶卡补「视频转文字」措辞

- docs/index.html 全家桶卡改「SenseVoice 本地视频转文字与字幕」，与四处口径对齐

**v1.0.28** · 2026-11-06 · 视频转文字内置（审计 DSH-VIDEO-TEXT-H1-H5）

- 免费全家桶新增 sherpa-onnx 引擎条目 + `tools/asr_setup.py`（.asr-venv + 官方三源下载 + sha256 逐文件校验 + --check）
- 新增 `tools/transcribe.py`：链接或文件 → yt-dlp 下载 → ffmpeg 16k 单声道 → SenseVoice 本地识别 → .txt 与 .srt（照官方 generate-subtitles.py）；`tools/test_transcribe.py` 5 场景进 CI
- AGENTS.local.md 新增 `dsh_video_to_text` GENE：全本机、装前问一次、不编文字、音频不出本机
- 文档四处同口径；CITATIONS 补 yt-dlp 与 FFmpeg；Whisper 不进默认包

**v1.0.27** · 2026-11-06 · 新手默认 Flash（审计 DSH-NEWBIE-FLASH-G1-G5）

- 起手式第 3 句定死 deepseek-flash（看图、1M、便宜；Pro 更贵且不能看图，先不用）
- AGENTS.local.md 新增 `dsh_newbie_model` GENE（看图直接贴、认真想请 Pro、只问一次模型选择）；「看截图」视觉路由标注为 Pro 开发者路线
- 一键安装改「看图直接贴」+「开发者用 Pro」小节；装完先验加贴图验收；起手式玩法表换「看图/想深一点」+ 开发者段；首页与 README 同口径

**v1.0.26** · 2026-11-06 · 视觉路由（审计 DSH-VISION-ROUTE-F1-F5）

- `AGENTS.local.md` 新增 `dsh_vision_routing` GENE：Pro 用户说「看截图」→ 剪贴板存图（`tools/clip_shot.ps1/sh`）→ `list_subagent_models` 核路由 → Flash 子代理 `read_image` 回报文字后继续；Flash 用户说「认真想」→ Pro 子代理；一次性子代理模型选择开关流程（两种开法、同意才写 profile）；全程不叫用户切模型
- 新增剪贴板截图脚本（Windows/macOS/Linux，无图 NO_IMAGE 退出 2），`shots/` 进 .gitignore，CI 加脚本语法步骤
- 一键安装与起手式加「截图给它看」小节；ROADMAP 记录：不装第三方视觉插件，贴图被宿主拒收等官方

**v1.0.25** · 2026-11-06 · 首页功能卡版式修复

- 「装完你就有了」一节：标题缩到 4–5 字并加 `.row.dense` 小字号，修掉窄栏折行（装完先验一／下、客服也过验／收、每版自动发／版）

**v1.0.24** · 2026-11-06 · 技能库卡片面向新手改口

- README 与落地页的「技能库」卡去掉 owner 内部流程话术（「刷到」「迭代进去」），改为对新手成立的口径：技能随装随用、按需加载、随版本更新

**v1.0.23** · 2026-11-06 · 落地页加「装完你就有了」

- docs/index.html 新增 8 项真实功能卡：记忆四件套、装完先验、引擎更新、本机模式、免费全家桶、客服验收、自动发版+DOI、卸载；全部按当前真实行为撰写

**v1.0.22** · 2026-11-06 · 首页口径小重写

- README 与落地页同步三处：记忆体卡改「换窗口不忘；换电脑贴备份句」（本机模式真相）；一键安装卡加免费全家桶一行；落地页页脚挂 Zenodo DOI 徽章

**v1.0.21** · 2026-11-06 · 免费全家桶砍掉本地模型（审计 DSH-FIX-E1-E8 v2.3）

- E1 删除 Ollama 与 Qwen3 8B 条目及全部 Qwen3 引用：新手模型走 DeepSeek API，不装本地模型（别人的清单只示意图，不照搬条目）
- E3–E8 沿用 v1.0.20 已落地修正，本轮回归核验通过（obsidian winget 验证、PATH 刷新、SenseVoice 引用、NotebookLM 标注、concept DOI、Linux 条目）

**v1.0.20** · 2026-11-06 · 审计第四轮 DSH-FIX-E1-E8

- E1 模型条目 verify 改 `ollama show qwen3:8b`（不再用 ollama list 误报已装）
- E2 macOS Ollama 走 cask `ollama-app`（formula 装完 pull 必失败）
- E3 Windows Obsidian 用 `winget list` 验证（不再查 PATH 误报失败）
- E4 Windows 安装器读注册表刷新 PATH 并按全路径执行；装成功提示重启 DSH
- E5 语音引用改正：SenseVoice / FunAudioLLM（2407.04051）+ sherpa-onnx + Silero VAD，撤下 Whisper；DSH 功能描述以官方仓库为准
- E6 NotebookLM 正名并标注海外（需谷歌账号、国内打不开）
- E7 预印本改用 concept DOI 10.5281/zenodo.22882690
- E8 Linux 补 apt 条目（ffmpeg/yt-dlp）与 ollama/obsidian 官方下载页指引

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
