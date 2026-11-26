# 更新记录（每次改动即发版）

**v1.1.58** · 2026-11-26 · 专家包同步到 WorkBuddy 2.3.67：选题技能多一条 Apify 数据路（低粉爆文日榜、微信指数、留言、联想词、按词找号、历史发文倍率）

- .dsh/books/ai-global-media/expert 的 agents/ 与 skills/ 原样换成 adsorgcn/WorkBuddy 2.3.67（9dc5cd9）：选题技能新增 scripts/apify_wechat.py 与 references/apify-wechat.md，用用户自己的 Apify 令牌调公众号采集器，跑之前报价、默认封顶 1 美元、令牌不进输出；五个文件的 IML 链头换成 0.6；sources.json 停一个英文源；其余文件一字未变
- SOURCE.json 重钉：提交 9dc5cd91c1919ef1dcb00604360cd74ee2c2a048、版本 2.3.67、30 个文件的 sha256（CRLF 换 LF 后算）；test_market 的 expert_package_pinned 过
- 主书 0.2.10 正文不动：RULE expert_as_is 让选题照专家原样做，Apify 这条路随专家包进来；出海插件随带的专家包另发 0.3.6 跟上
- 来源：2026-11-26 owner「你先看迭代后有没有需要修改的 如果没有DSH 那边就同步」

**v1.1.57** · 2026-11-25 · 货架钉 dsh-plugin-seo 0.1.0；落地页加「SEO 体检」一卡；线上 MCP 1.3.4 共 25 项已部署

- 货架登记官方插件 dsh-plugin-seo 0.1.0（npm integrity、commit 80c412413f7133f959bc78d9e5e357a25804cc1e、标签 v0.1.0 钉死，npm test 10/10，仓库 adsorgcn/dsh-plugin-seo MIT）；官方索引 docs/market/index.json 加 seo 分类与这条；市场页由 market_build 重生成，官方插件 3 个
- 落地页 docs/index.html：「从第一篇文章」一节加「SEO 体检」宽卡（报告示意：六维逐条、每条带证据与 Google 官方页地址、非 Google 的建议另列）；03 卡计数改 7 本工程书、三个官方插件并列出 dsh-plugin-seo；MCP 段 25 项并加「SEO 体检」；首页公告句改本次；样式在 docs/redesign.css
- Worker ilang-dsh-mcp 已按 main 的 server/content.mjs 1.3.4 重新部署并验：healthz 1.3.4、overview 25、MCP resources 25、SEO 书 sha 82a64b16 一致
- 来源：2026-11-25 owner 对三件拍「1，放 2，过 3，出」，第 3 件插件已发 npm，第 2 件落地页与 Worker 是这一版

**v1.1.56** · 2026-11-25 · SEO 体检：按 Google 官方文档逐条判六维，一页报告，点头才改，不批量产页不做外链不抓结果页；MCP 1.3.4 共 25 项（DSH-SEO-S1-S6）

- 新书说一句「SEO 体检」并给网址：先读 Google Search Central 当天的官方页，抓站落快照，按技术地基、你是谁、站点聚焦、页面可读、信任与站外、数据六个维度逐条判，一页报告每条带证据和 Google 页地址；改法你点头一条改一条，只改工作区里的站文件，部署是你做。Google 说 AI Overviews 与 AI Mode 没有额外要求、不要特殊 schema、没有 magic word count；自动只能是自动体检和改稿建议，不能自动产页、自动外链、自动抓排名，书里四条边界钉死
- 货架登记 seo（version 1.0），口令三处：AGENTS.local.md 触发行与一段、README 市场与 MCP 行、dsh-新手起手式.md 表
- MCP 1.3.4 共 25 项，发现文件同步（content.mjs、worker.test.mjs、server/README、openapi.json、mcp.json、server-card.json、agents/index.html、llms.txt）；Worker 由 @SUN 侧重新部署
- check_rubrics 加 R12 钉住书的四条边界与入口
- code-chain 门禁放过 upstream-sync 的自动提交（它们没有 owner 的话可封，2a217e2 那笔就是）
- 来源：2026-11-25 owner 看过对照报告后拍「做 写工程书」；门禁那条是他同日拍的「放」

**v1.1.55** · 2026-11-19 · code_chain.py 的文件头注释跟上正典 code-chain 1.1

- `tools/code_chain.py` 第 2 行注释：products/code-chain 1.0 → 1.1（正典 5.0.18 同日发，第 16 行反模式改为讲原因：旁边文件随后面每个提交走、谁都能改，提交信息只属于这一个提交）；链的格式、门禁的行为都没变
- 来源：2026-11-19 owner 拍「DSH 那个注释也改了 发」

**v1.1.54** · 2026-11-19 · code-chain 门禁开拦：从 v1.1.53 起缺链就不放行

- CI 的 code-chain 门禁加 `--require v1.1.53`：v1.1.52 起照数，v1.1.53 之后的提交没有链或链不合法，CI 直接挂；v1.1.53 之前的旧提交只数不拦
- README「放心」加一段：每笔改动末尾都带谁要的、怎么判的，读法两条命令，规范指向正典 products/code-chain
- 官网同日开页 https://ilang.ai/code-chain/（中文站 ilang.cn 同步）
- 来源：2026-11-19 owner 拍「从 v1.1.53 起缺链就拦 页也开」

**v1.1.53** · 2026-11-19 · code-chain 第一次跑：每个提交的末尾带谁要的、怎么判的

- 正典 5.0.17 新产品 products/code-chain：提交信息末尾空一行、一行标签 ai.ilang.chain、再五行——一行 FACT 记 owner 的原话和这次改了什么，一个 JUDGE 块记十一维向量、模式、理由；提交哈希盖住它，签名提交绑住它；模式只看 M 行
- 这个仓库第一个跑：tools/code_chain.py 三个命令，seal 用正典的 f_v5 算模式并过两个校验器后打印六行，check 从 git log 读回来数链、过校验器，show 看一个提交的链；tools/ilang_judge_validator.py 是正典判断校验器的副本；CI 加一步 check --since v1.1.52，先只数、只在链写错时失败
- 从这一笔起本仓库的提交都带链；第一笔就是本次（见 git log -1 --format=%B）
- 来源：2026-11-19 owner 拍「做 先在DSH自己的commit上跑」
- 补：CI 的 checkout 改成取全历史（fetch-depth 0），不然门禁在 CI 里找不到 v1.1.52；首跑挂在这里，内容没错

**v1.1.52** · 2026-11-19 · 爆文公式：专家写完稿之后的一道节奏自查，209 条标题与 15 篇正文量出来的

- 新书 .dsh/books/baowen/BOOK.md（DSH-BAOWEN-FORMULA 1.0）：标题命中至少 3 个要素（金额 49%、赚或月入 63%、副业 30%、普通人 28%、AI 25%、数字列表 22%、时间周期 15%、零成本 6%）、3000 到 5000 字、每 300 到 500 字一个金额或案例、每 500 字一个问句、段落不超 3 句 50 字、禁词、第一人称经历有来源或标占位；owner 的草稿改了三处才收：结尾不再引导关注或社群（专家包合规写明引导点赞转发收藏关注可能限流封号），PRIORITY 加「合规」压在公式上，@DATA 写实 209 条标题与 15 篇正文并注明节奏五个数样本小攒到 50 篇重算
- 它是加在专家外面的一道，不是另一条写稿路：主书 0.2.10 第四环写完稿、辨识度检查之后自动过一遍（第 7 步），配图顺延；说一句「爆文公式」也能单独量一篇稿，没给稿就请用户先说「AI全球自媒体」
- 货架 book baowen（say 爆文公式）；AGENTS.local 口令说明；README 第五本与 MCP 24 项；起手式一行；MCP 服务 1.3.3 白名单加这本（24 项），openapi、well-known、llms.txt、agents 页同步，线上 Worker 重新部署
- 数据来源：owner 2026-11-18 用 Apify 拉公众号得到；拉取数 143 篇与书里 209 条标题的口径由 owner 定，书里按 209/15 写
- 来源：2026-11-19 owner 贴来草稿说「你看看」，拍「改」
- 货架：plugin 条目钉 dsh-plugin-chuhai 0.3.5（随带主书 0.2.10 与爆文公式那本，目录工具多报一行它在哪），index.json 顶部加 0.3.5，市场页由构建器从登记表重画；来源：2026-11-19 owner 拍「弄完」

**v1.1.51** · 2026-11-19 · 国内优先，国际兜底：那一句指向 ilang.cn，脚本先走 gitee

- 那一句改成「帮我装 iLang DSH 工具包，照 https://ilang.cn/guide/dsh/install.md 做。」，README、首页、一键安装.md、llms.txt、agent-skills 卡同一句；https://dsh.ilang.guide/install.md 是同一份，国际兜底。install.md 1.2 写明国内优先国际兜底，ilang.cn 打不开就读国际那份
- bootstrap.ps1 与 bootstrap.sh 的自动探测改成国内镜像优先：先探 gitee，不通再 GitHub；-Source 强制参数不变
- MCP 安装说明工具 1.3.2：bootstrap 的 url 给 gitee、mirror 给 GitHub，guide 指 ilang.cn 那份；openapi、well-known 版本同步
- 来源：2026-11-19 owner 说「dsh 优先国内镜像 比如 ilang.cn 国际的兜底 毕竟 dsh 是中文产品」

**v1.1.50** · 2026-11-19 · 第三个国内镜像：腾讯 CNB，三处镜像随 GitHub 发版自动同步

- mirror-sync 加 cnb.cool/ilang/DeepSeekHarness 一步；Gitee 与 CNB 的令牌已进仓库密钥，Gitee 镜像从 11-18 的 92b0758 追平到当前 main，CNB 从空仓一次性推平（本地克隆原来是浅的，CNB 不收浅推送，取全历史后才推上）
- README 国内那句加上 CNB
- 来源：2026-11-19 owner 给了 CNB 与 Gitee 仓库级令牌
- 补：mirror-sync 加串行锁 concurrency mirror-sync。一次发版是两个推送事件（分支和标签），首跑时两个任务同时推同一个标签，一个报 failed to update ref；镜像内容没错，串行后不再撞

**v1.1.49** · 2026-11-19 · GitHub 发版自动同步到 GitCode 与 Gitee 两个镜像

- 新增 .github/workflows/mirror-sync.yml：每次推 main 和打 v* 标签，把 main 和标签推到 gitcode.com/monetize/DeepSeekHarness 与 gitee.com/monetize/DeepSeekHarness；令牌没配的镜像跳过不报错；只做普通推送，镜像分叉就让任务失败让人来看，不强推。GitCode 的令牌已配进仓库密钥，Gitee 的等 owner 给
- GitCode 镜像今天一次性推平到 GitHub 的 main（之前空着）；GitCode 不提供 raw 文件直链（raw.gitcode.com 回「暂不支持预览」），只当 clone 镜像，install.md 的 raw 来源仍是 gitee；Gitee 镜像停在 11-18 的 92b0758，等令牌一到就自动追平
- 来源：2026-11-19 owner 说「我导入了一份 你设置下一次性推了之后 都同步发版 做成 github 发版 gitcode 跟 gitee 并行」

**v1.1.48** · 2026-11-19 · 国内镜像的权重排前面：install.md 先走 gitee，再走 GitHub

- 有人贴了那一句之后 Agent 说无法访问 git。从国内探测点实测：gitee 三网都快，GitHub raw 三个点有一个超时，dsh.ilang.guide 三个点有一个超时。docs/install.md 1.1：@SOURCES 把 gitee 镜像排第一，取脚本先 mirror_raw 再 raw，两边都不通就把两个地址给用户在浏览器里下；README 国内那句同步
- 那一句的全文在国内多放一份：https://ilang.cn/guide/dsh/install.md ，和 docs/install.md 一字不差；国内孪生页上那一句指向这份
- 来源：2026-11-19 owner 说「我里面有 gitee 镜像 我觉得这个权重要拉前面来」

**v1.1.47** · 2026-11-19 · 那句话换成一句短的：帮我装 iLang DSH 工具包，照 https://dsh.ilang.guide/install.md 做

- 新手贴的只剩这一句；原来 250 字的长指令全文改写成给 Agent 读的工程书 docs/install.md（创造模式、取脚本、只检测、一样一样问、官方源、问一次装插件、卡住自己修、最后告诉用户怎么回来），strict 0 错 0 警告，线上 https://dsh.ilang.guide/install.md
- README、首页、一键安装.md 三处改到同一句（之前 README 和 一键安装.md 里的长句已经是两个不同版本）；MCP 安装说明工具 1.3.1 返回这一句并把 guide 指向 install.md；Worker 测试、openapi、well-known 版本同步；agent-skills 的 dsh-install 卡补一句并重算摘要；llms.txt 与 agents 页各加一条
- 来源：2026-11-19 owner 说「首页复制粘贴的命令提示词 一些新手蠢到没办法理解」并拍「过」

**v1.1.46** · 2026-11-19 · 出片 Bot 书 1.5：交片六行每行开头给固定标签

- 第一次真人跑回来的出片报告内容齐、壳子散（没写 CLIP-READY、S 写成 DONE、少了花费那行、瑕疵混进六行），所以 REPORT 六行每行开头给标签 CLIP-READY、成品、版本、花费、门禁、S=，让 Bot 照抄；瑕疵另起一段写在六行之后。其余一个字不动
- DSH 这边 BOOK.md 1.6 核新 sha256；货架 chupian 1.6
- 来源：2026-11-19 owner 看了 Bot 的报告拍「那个批」

**v1.1.45** · 2026-11-19 · 一稿多发：一篇稿照平台卡改版本、排队、由手发出；MCP 1.3.0 共 23 项；官网补两处

- 新书 .dsh/books/yigaoduofa/BOOK.md，说一句「一稿多发」或直接说「发到 X 和公众号」「明天发到所有平台」：取最近成稿，照 publish/cards.md 每个平台的卡改成该平台的版本（只改排版、长度、标签、配图、链接、语言，不改观点、数字、标题、论证），每版先给你看，你说「发」才进 publish/queue/<平台>.json；公众号推草稿你点发布，X 由你的 Grok Bot 走官方接口，YouTube 先私密；发完链接写回队列，发错的原样记一行进 publish/log/errors.md；队列文件是两头共用的唯一排期账本，DSH 不常驻、到点的事由 Bot 的 routine 做
- 随包 Bot 书 bot-yigaoduofa-book.md：到点 pull 队列，只发 approved 且到时间的，X 走第一本书 B2/B4，YouTube 走 B15，公众号走云端分身的固定出口，一条一次提交；用户在手机上直接说「发到 X 和公众号」它也能照卡出版本给看再排
- 随包平台卡 cards.md 九张：第一波公众号、X、YouTube 这版就发；第二阶段小红书、抖音、哔哩哔哩、LinkedIn、Medium、Substack 由 Grok Bot 指挥 Muse 在 Muse 内置电脑的真实浏览器里发，这版只出版本放 outbox（Medium 已停发新接入令牌、Substack 没有发帖接口、小红书官方不给个人接口、抖音与哔哩哔哩要应用过审，都查过）
- 货架加 book yigaoduofa（say 一稿多发）；AGENTS.local 口令说明；README 第四本；起手式一行；MCP 服务 1.3.0 白名单加两本（23 项），openapi、well-known、llms.txt、agents 页同步，线上 Worker 已重新部署
- 官网两处文案：MCP 段补「一稿多发」「SEM 与付费投流」；03 卡片加官方插件两枚 dsh-plugin-chuhai、adspilot
- 来源：2026-11-19 owner 看过一稿多发需求单后拍「做 一起把官网那两处也改了」，并定第二波平台走「grok 控制 muse 在 muse 内置电脑的真实浏览器里弄」
- 货架：plugin 条目钉 dsh-plugin-chuhai 0.3.4（进度行加「一稿多发」，再往后的环写明第二阶段平台由 Grok Bot 指挥 Muse 在它的真实浏览器里发），index.json 顶部加 0.3.4，市场页那行同步；来源：2026-11-19 owner 拍「发 把进度行改了」

**v1.1.44** · 2026-11-18 · 补 v1.1.43：发现文件同步 21 项与 1.2.0

- docs/openapi.json 版本 1.2.0、五处文档路径枚举加 .dsh/books/adspilot-sem/BOOK.md；.well-known 的 mcp.json 与 server-card.json 工具参数枚举同步；llms.txt 与 agents 页各加这本书一条
- 来源：v1.1.43 的 CI 发现测试（test_agent_site）挂在这几份清单上，线上服务本身已是 1.2.0、21 项

**v1.1.43** · 2026-11-18 · MCP 服务 1.2.0：公开资源加 AdsPilot 的工程书，共 21 项

- server/content.mjs 白名单加 .dsh/books/adspilot-sem/BOOK.md，服务版本 1.1.0 → 1.2.0，概览描述加「SEM 与付费投流」；worker.test.mjs 把这本书加进发现、读取、检索、HTTP 入口的测试；server/README、根 README、.well-known 的 mcp.json 与 server-card.json 同步 21 项与 1.2.0
- 线上 dsh.ilang.guide/mcp 已重新部署，模块与本提交一字不差
- 来源：2026-11-18 owner 对「MCP 固定资源表没加 AdsPilot 书」拍「加」

**v1.1.42** · 2026-11-18 · 货架收第二个官方插件 AdsPilot 2.2.0：说一句「SEM」或「付费投流」

- 货架加两条：工程书 adspilot-sem（AdsPilot 的 BOOK.md 原样内置到 .dsh/books/adspilot-sem/，strict 0 错 0 警告，sha256 cf2d789e…，也是插件在线更新的锚点）和官方插件 adspilot 2.2.0（npm integrity 钉死、标签 v2.2.0 = 04536fe、仓库 npm test 16 过 0 败）；index.json 加 adspilot 与 advertising 分类；市场页官方插件区加一行
- AGENTS.local 加「SEM」「付费投流」口令说明：克隆 AdsPilot 仓、六环、默认 dry-run、KYC 绑卡申诉用户自己做
- 工具：market_admit.py 核标签时优先取 ^{} 解引用到的提交，附注标签不再误报不一致；test_market 官方插件索引按包名核全部插件
- 来源：2026-11-18 AdsPilot 发 2.2.0 并交来上架单，逐项实测后 owner 拍「批」

**v1.1.41** · 2026-11-18 · 云端分身加 routine：勾了它到点自己出文、自己盯公众号后台的反馈

- 分身书 1.2：搬完回六行之后手问用户一次，出选择卡两样各自勾不勾：每天到点自己出文（几点、几篇）、每天盯一次公众号后台的反馈；勾了才用 Grok Bot 自己的 routine 建（最短 5 分钟、一只 50 条），到点出文和他说一句「出文」一模一样，稿子还是草稿他点发布；盯反馈只写不改，变化和一句改法进 library/feedback/日期.md，后台不给看的说看不到不假装；他说「停」当场关
- DSH 这边 BOOK.md 1.2：核对分身书新的 sha256，对账时提醒手会问这一句、你不替他答，反馈里的改法他点头了才照着改；货架 fenshen 1.2，AGENTS.local 口令说明与 README 第三本各补一句
- 来源：2026-11-18 Grok Bot 团队 lauren（@poteto）长文说 routine 是让 Bot 自己到点干活的那一步，我们的书里一条没用；owner 拍「加」

**v1.1.40** · 2026-11-18 · 官网说明跟上货：进度与规划、已接入三家、全平台单子

- docs/index.html：首屏第 03 步与出海段写到 X 开蓝 V、Grok Bot 与手脚，技能卡片补「云端分身」；「未来规划」改成「进度与规划」，X 与 YouTube 标已接入并写清在哪一环，Medium 仍规划中；新增中国与全球自媒体平台单子（已接入的带点），问答同步；redesign.css 加平台单子样式
- 来源：2026-11-18 owner 问「官网的说明是不是要改了」拍「改」，又说「未来会加入所有的中国以及全球的自媒体平台 你去列举下」

**v1.1.39** · 2026-11-18 · 发给真人测之前的两处修正

- 云端分身：Bot 的出口 IP 是固定的（owner 确认），分身书量一次就给你加公众号白名单，不再隔半天量两次；白名单加了测试草稿还推不出去，才经你出海那台服务器推
- 出片：交接单里没记 Muse 开没开就问你一句，不再当没开把你打回「自媒体出海」
- 来源：2026-11-18 owner 说「固定的 bot 不用测 要修的修完 发完直接丢别人测」
- 货架：plugin 条目钉 dsh-plugin-chuhai 0.3.3（进度行写到手脚续篇：Railway、家宽 IP、YouTube 频道；工具包那边的「出片」「云端分身」两句口令），index.json 顶部加 0.3.3，市场页插件行同步（补记，不升版本）

**v1.1.38** · 2026-11-18 · 云端分身：工作区进私有仓库，Grok Bot 克隆同一个仓库，出门用手机说三句口令

- 新书 .dsh/books/fenshen/BOOK.md，说一句「云端分身」：DSH 把工作区推成私有仓库（钩子只许私有），把随包带的分身书交给你的 Grok Bot；它克隆、跑一次 brain.py init、装人格、读主书和出片书、账本的门要你在它那台机器上点头、量自己的出口 IP 两次一样就给你加公众号白名单，不一样就经你出海那台服务器推草稿；搬完回 TWIN-READY 六行，两头对一次
- 以后出门用手机对它说「出文」「出片」「发到 YouTube」，成品进同一个仓库；两头每次开工先 git pull，做完立刻 commit 和 push；电脑上的 DSH 从交书那天起也先 pull
- 货架加 book 条目 fenshen（say 云端分身）；AGENTS.local 口令说明；README 第三本；起手式一行
- 来源：2026-11-18 owner 说「dsh 能够迁移到云端的工作 全迁移一次 在外面手机控制的时候用」「只需要 IP 加白 公众号」并拍「做」

**v1.1.37** · 2026-11-18 · 出片书 1.4：媒体链母版升到 1.2，书里钉的 sha 跟上

- 正典 products/media-chain 1.2（修正案 MC-CX-001：多个 take 剪成的成片有自己的 GEN 行、一行 FACT 记 takes、链走 XMP sidecar）与母版 1.2 已上，出片书 @CANON 钉的母版 sha256 换成 94c57c4e…，SOURCE.json 记母版 1.2；书的正文不变
- 来源：2026-11-18 owner 拍「进 1.2」

**v1.1.36** · 2026-11-18 · 出片书 1.3：门禁修好了，嵌入那句改回母版的口径

- 出片书 TAIL 那句不再说「门禁读不到所以 sidecar」：平台已签名的文件照母版只用 sidecar，没签名的原件能嵌就嵌，门禁从 2026-11-18 起读得到 c2patool 0.29.0 的嵌入（数据集 i-Lang/media-chain 提交 0836390b）；成片仍是 sidecar 加一行 FACT 记由哪几个 take 剪成（正典 products/media-chain/records 的 MC-CX-001）
- 来源：2026-11-18 owner 拍「门禁脚本修了 登记反例」「改书发一版」

**v1.1.35** · 2026-11-18 · 出片书 1.2：Grok Bot 复跑 1.1 回包后的五处修正

- 出视频前的闸门按路写清：ONECMD 路是故事和分镜，VEM 路是镜头计划，首个样片是它自己那道闸门前唯一准出的片；VID_ONECMD 那步不再写「三道」，闸门照 RULE gates 设四处
- 分辨率按路算：ONECMD 路按首尾帧同给时手的模型能出的最高档，VEM 路按只给首帧时算，不查订阅；原书没给默认的音乐记 no，预算按 @INPUT 记 minimize
- 媒体链：母版要 c2patool 嵌入的也先用 sidecar，因为门禁 check_series.py 配母版指定的 c2patool 0.29.0 --detailed 读不到嵌入的断言（Bot 实测：嵌入回读对、门禁判 FAIL）；脚本另修，书里先绕
- 来源：2026-11-18 owner 的 Grok Bot 按出片书 1.1 复跑的回包（strict 0/0，原文逐字一致，出图路线门禁 PASS JEJU-TANGERINE-20261118，两条出片路线停在第一道闸门等用户点头，S=0.92）
- 货架：registry.json 的 plugin 条目钉 dsh-plugin-chuhai 0.3.2（进度行写到手脚：邮箱、Gmail、InstaBox、Muse），index.json 顶部加 0.3.2；来源：出片环 Bot 实跑过、2026-11-18 owner 说「出片了 没啥问题了」后拍发（补记，不升版本）

**v1.1.34** · 2026-11-18 · 出片书 1.1：Grok Bot 实跑回包后的七处修正

- 闸门不再死锁：改成「故事和分镜过了才准出视频，首个样片是它自己那道闸门前唯一准出的片」；两条路都设用户闸门（ONECMD 路 故事、分镜、首个样片、成片四处；VEM 路 镜头计划、首个样片、成片三处），首个样片是最难的那一镜，用户点头才出其余
- 分辨率不查订阅：以手自己的模型在给首尾帧时能出的最高档为准，低了后期用 ffmpeg 放大，不装超分模型；原书 PREFLIGHT 的四个问题用户没说就用原书默认值，不问，默认值写进系列文档
- 母版 SETUP 要的工具（校验器、门禁、c2patool）照母版装，不算「别的」，装不上用 sidecar；成片是 ffmpeg 从几个 take 剪出来的不是生成器原件，GEN 行写用户要的那件成品、一律 sidecar、加一行 FACT 写明由哪几个 take 剪成，原件留在 chupian/takes/
- 回报第 2 行改成「成品」，图的时长和帧率写 none；ONECMD 原文补回 X 上 ART_STYLE 和 REVIEW 前的两个空行（词句不变）
- 原书 AI-VIDEO-ONECMD 自身的前后不一致（L419 写三道闸门到首个样片，L530 的 GATE 3 是成片）原文不动，总书的闸门规则压过去
- 来源：2026-11-18 owner 的 Grok Bot 按出片书 1.0 实跑一遍的回包（出图路线连门禁走通，两条出片路线走到第一次花钱前，S=0.92）

**v1.1.33** · 2026-11-18 · 出片：一句话或一张图，交给你的 Grok Bot 出图出视频，成品带媒体链

- 新书 .dsh/books/chupian/BOOK.md，说一句「出片」：DSH 把随包带的出片书 bot-chupian-book.md 原样放进工作区，你拖给自己的 Grok Bot（或 Muse）说「照这本书做」，一句话或一张图，手自己出图出视频；没装 Grok Bot 先走「自媒体出海」到装它那一环
- 出片书里：按输入分流，广告片照 IML-VEM v1.2.2，叙事片照 AI-VIDEO-ONECMD v1.0，只要图直接走媒体链母版；两本原书原文一字不改随书带着（正本在 sources/，来源与哈希在 SOURCE.json，都是 owner 在 X 上发过、在 Grok Bot 上走通的那两段）；出片模型就是手自带的，不要任何钥匙；每一件成品照媒体链母版 1.1 把 GEN 行和 JUDGE 块留在文件里，系列文档记每个版本
- 货架：registry.json 加 book 条目 chupian（say 出片），市场页重建；AGENTS.local 口令说明加一段；README 市场一节加第二本；落地页技能卡加一句；起手式加一行
- 来源：2026-11-18 owner 拍「做」（综合版自动分流、不出选项卡、手只有 Grok Bot 与 Muse）

**v1.1.32** · 2026-11-17 · 落地页记忆体一幕补回账本那一句

- docs/index.html 记忆体卡片的说明段末尾补回「钥匙也在：每扇门一行账本，值静态编码，门要在你这台机器上开，先由你点一次头。」这一句（v1.1.4 加的，11-13 首页重做时丢了）；不加节点、不改样式
- 来源：2026-11-17 owner 拍「补」

**v1.1.31** · 2026-11-17 · 地板：工具包自己不设门，拒绝原话给你，下一句就是另一条路（DSH-FLOOR-G1-G4）

- soul/agent.md 出厂的「工作方式」里加 GENE floor：工具包在用户与模型或工具之间不设自己的门（没有登录墙、许可证、次数、地区检查）；模型、工具、服务说不，原话原码给你；说不之后那一句是另一条路；中途触限把手里这一轮答完再停并说从哪接着
- 一键安装.md「遇到问题怎么办」加一段：模型那边的门不是工具包的，原话给你、下一句是路；README「放心」整段换成地板那句话，钥匙那半句改成 3.1 口径（账本、静态编码、不是加密）
- tools/check_rubrics.py 加 R11：钉住上面三处文字，并扫 bootstrap 与 free_station 与 server 五个自有脚本，不许出现激活码、授权码、许可证、license_key、LICENSE_KEY、余额不足、地区不支持 七个门字眼
- 来源：ilang-spec 5.0.15 附录 F CX-009 与 2026-11-17 owner 拍「地板」

**v1.1.30** · 2026-11-17 · 母功能：看见攻略，说一句「变工程书」

- 新技能 source-book：贴来一篇攻略、一个链接或一张截图，说一句「变工程书」，DSH 照母版（Source Book 2.9）写出一本工程书，存在工作区的 books/<名字>/BOOK.md，过官方校验器才算完
- 攻略里的数字去官方来源核实，核实过的写成带出处的规矩；收入和价格不照抄，要用户自己定的留空
- 写好以后说一句「照这本书做」，DSH 照书执行，要你决定、授权、付款的地方停下来；也可以把书拖给 Grok Bot
- 母版用的是仓库里原来就带着的那一份（.github/bot/ 下，和正典 ilang-spec v5.0.14 的文件逐字节相同），不另放副本
- 货架：registry.json 加 source-book 一条；新手起手式加两句话
- 来源：2026-11-17 owner 说把母功能做进工具包

**v1.1.29** · 2026-11-17 · 主书 0.2.9：写到用户自己做了什么，带数字的句子原样照抄

- 拉完热点当场数一遍文件：一共几条、来自几个源，写成一句话在交接单里记成一条 FACT（feed_today）；每轮搬完货也记一句（haul_last）
- 写稿：讲用户自己做了什么、带数字的句子，把交接单和复盘里记着的那一句原样抄进稿子，不凭印象重讲；没记的数不写。成稿检查加这一条
- 交稿时把稿子里讲用户自己的句子一句一行列给他看，有不对的他说一句就改；验收项加 B18
- 恢复：2026-11-16 每周一次的上游同步把 v1.1.21 加的两处改动冲掉了（放进人格位置的专家正文整段算用户给的；交接单模板里的占位不算事项）。GitHub 上的 main 在 11-16 17:37 到 22:24（UTC）之间是坏的：这段时间新装或更新的，第一环装人格、第一次填交接单的提交会被工具包自己的检查拒掉。已恢复，这段时间装过或更新过的，更新到这一版就好。Gitee 镜像没有受影响
- 货架：registry.json 的 plugin 条目钉 dsh-plugin-chuhai 0.3.1，index.json 顶部加 0.3.1；插件的介绍写到装 Grok Bot、把第一本书交给它（2026-11-17 补记，不升版本）
- Linux 和 macOS 上装完，工作区里不再有两个显示成改过的文件：`tools/hooks` 下的两个钩子在仓库里就标成可执行（以前是安装时才改，装完 `git status` 就不干净）。Windows 上没有变化
- 这一版只改书和这一处标记，插件不用更新：装了 dsh-plugin-chuhai 0.3.0 的，联网时自己取到这一版
- 来源：2026-11-16 发版前验收里的一篇成稿把自己拉热点的结果写反了（82 个源有内容写成只有 1 个有内容），数字都对，关系反了

**v1.1.28** · 2026-11-16 · 主书 0.2.8：发版前的机器验收查出的两处措辞

- 接破局那一步写明条目的样子：在用户 patch 层的顶层列表里加一项，键是 insert，它下面才是那一条；直接写成顶层一项是改已有条目的写法，会报找不到。工具没出现时先看这一点
- 易洋视角卡：AI 洋哥两句回答里新的判断另起一节写在抄来的内容之后，不往抄来的各组里加行
- 这一版只改书，插件不用更新：装了 dsh-plugin-chuhai 0.3.0 的，联网时自己取到这一版
- 来源：2026-11-16 发版前验收的两轮运行

**v1.1.27** · 2026-11-16 · 主书 0.2.7：两轮真机走查暴露的问题一次改掉；插件改成现取主书，以后改书不用再发插件

- 破局登录：先跟用户说一声，默认由命令行自己弹出浏览器，用户点一次确认；没弹出来才给链接
- 破局的工具没出现：先等半分钟，再看登录在不在，最后才请用户重启
- 易洋视角卡：那份文件里十二组规矩连同原话整段照抄；案例库没接上时照书里那张卡或那份文件直接写，两句话记进待办
- 第四环：内容清单照选的那位排（亦仁五层、易洋三道尺子）；成稿检查多三条，写到真人的数字要在货仓原文里找得到、写到自己的经历要真有、专家留给作者补的标记不留在稿子里
- 拉热点：结果由 python 按 UTF-8 写进文件；B15 多查一条按 UTF-8 读得出来
- 搬货：搜帖列表里带回来的那一段不当正文存，每条再取一次全文；写明什么算正文在外部文档
- 每天的提醒：建的时候把工作目录填成放 library 的那个文件夹
- 第一环第 1 步的条件写明；第二环第 1 步不再绕到第三环
- 插件 dsh-plugin-chuhai 0.3.0 起，前半段的书联网时先取这里的最新版，按 registry.json 登记的版本和摘要核对，取不到用包里带的
- 货架：registry.json 的 plugin 条目钉 dsh-plugin-chuhai 0.3.0，index.json 顶部加 0.3.0
- 来源：2026-11-16 两轮真机走查的回包

**v1.1.26** · 2026-11-13 · 写作专家包迁进工具包：爆文写法、微信排版、推草稿、看榜选题随书带着；主书 0.2.6

- 公众号爆文专家的专家包从 adsorgcn/WorkBuddy 原样迁进来，放在 `.dsh/books/ai-global-media/expert/`：人格正文（21 组写作基因）和四个技能 wechat-article、wechat-draft-push、wechat-topic-hunter、remote-dispatch，含两种骨架与标题公式、算法与节奏、去 AI 味、十二项自查、合规、封面词、微信排版规则、推草稿脚本、看榜选题与拉热点脚本，共 28 个文件，一个字不改
- 来源钉在 `expert/SOURCE.json`：上游仓库、40 位提交、版本 2.3.58、每个文件的 sha256；`test_market` 加一条 expert_package_pinned，文件和清单对不上就不过
- 主书 0.2.6：第一环不再临时上网去取专家包，用随书带的这一份；只装了插件的用插件目录里报的那一份；没有就让用户更新工具包或插件
- 货架：registry.json 的 plugin 条目钉 dsh-plugin-chuhai 0.2.4，index.json 顶部加 0.2.4；插件随带同一份专家包，目录里多报一行它的位置
- 来源：2026-11-13 @SUN「公众号排版你是不是没在 workbuddy 那边仓库迁移过来 以及爆款写法算法」

**v1.1.25** · 2026-11-13 · 安装指令：先确认创造模式，装不上自己修好；市场页手动装法写准

- 那句话加两处：开头先确认是创造模式（手里有装插件的工具），不是就先别动手、让用户新开一个创造模式的任务再贴一遍；末尾加「哪一步装不上或卡住，你自己想办法修好、装好再往下走，被权限拦了就向我申请一次放行」。首页、README、一键安装三处是同一句
- 首页第二步、常见问题、首屏小字和 README 写明：新开任务一定先选「创造模式」（装插件的工具只有它有，装不上东西时它能自己修）；「你只做两件事」改成三件事：选创造模式、粘贴、点头
- 市场页官方插件那段：「添加插件」只填包名；索引地址要先在「实验性插件」下启用「自定义插件索引」，在多出来的「发现」页签里点「添加索引源」再贴。原来那句让人把索引地址填进了「添加插件」，被当成包去装，解包失败
- 来源：2026-11-13 两位真实用户的截图（标准模式下装 Git 被权限模式拦在临时目录，折腾 22 分钟；把索引地址当插件装）

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
