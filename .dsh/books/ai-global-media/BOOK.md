::ILANG::v5.0::ENGINEERING_BOOK
[TYPE:engineering_book]
[ID:AI-GLOBAL-MEDIA]
[VERSION:0.1.2]
[DATE:2026-11-10]
[LANG:zh]

::STATE{@USER, role:decision_maker, is:只会用豆包问问题的新手, does:说一句话 点头 扫码 粘贴 自己付钱}
::STATE{@AGENT, role:you_the_user_s_own_AI_running_in_DeepSeek_Harness_with_the_iLang_DSH_kit, does:everything_the_user_does_not_have_to_do, never:替用户扫码 登录 授权 付款}
::STATE{@KIT, persona_slot:soul/agent.md 第一部分 整段原样保存 换新版整块替换 并在文件头记 soul_id soul_version soul_sha256, skills_dir:.dsh/skills, poster:.dsh/books/ai-global-media/poster.jpg}
::STATE{@EXPERT, name:公众号爆文专家, repo:https://github.com/adsorgcn/WorkBuddy, mirror:https://gitee.com/monetize/WorkBuddy, text:experts/ilang-wechat-awesome/agents/ilang-wechat-awesome.md 开头两行分隔线之后的全部, skills:experts/ilang-wechat-awesome/skills 下的文件夹 至少 wechat-article wechat-draft-push wechat-topic-hunter}
::STATE{@SCYS, what:生财有术的官方 MCP, server:https://mcp.scys.com/shengcai-web/mcp, auth:OAuth 用户自己在浏览器里用生财账号登录 配置里没有密钥, mode:只读, entry:https://scys.com/mcp 生财的官方接入页 只在 FALLBACK 里请用户自己打开}
::STATE{@BRIDGE, what:开源桥接器 mcp-remote 许可 MIT 作者 Glen Maddern, why:DeepSeek Harness 的 MCP 管理器目前没有 OAuth 流程 由桥接器在本机拉起浏览器代办授权, args:-y mcp-remote@0.8.6 https://mcp.scys.com/shengcai-web/mcp --resource https://mcp.scys.com/shengcai-web/mcp --transport http-only --auth-timeout 300, needs:本机有 npx 也就是装了 Node.js}
::STATE{@DSH_MCP, doc:deepseek-ai/deepseek-harness 仓库的 packages/mcp/mcp-manager/README.zh.md, says:每台服务器是 MCP 管理器那一行 config.servers 里的一项 支持 stdio 与 streamable-http；写 profile 的 cordis.patch.yml 会整份替换 servers 所以已有的服务器要一并写回}
::STATE{@SCOPE, covers:装写作专家定成人格 与 接上内容源, later:知识库 出文章 公众号 出海 一稿多发 变现 以后逐版加}

::OBJECTIVE{id:persona_and_source_ready|owner:user|trust:trusted|version:1|status:active}
  target: 用户说一句 AI全球自媒体 之后 公众号爆文专家整段成为你的人格 生财 MCP 接上 只读搜一次列得出标题
  ACCEPT: RUBRIC 每项通过
  NON_GOALS: 知识库及以后各步；生财的任何写操作；替用户注册 付款 扫码或授权
  DONE_WHEN: 你用一句话告诉用户人格装好了 内容源接好了 并把做到哪一环记进交接单

::BOUNDARY{never:call_any_scys_write_tool_like_favorite_coin_feedback_or_publish|scope:permanent}
::BOUNDARY{never:open_scys_pages_with_a_browser_tool_or_a_crawler_yourself;use_the_mcp_tools_only|scope:permanent}
::BOUNDARY{never:print_or_store_a_key_a_token_or_a_password_anywhere|scope:permanent}
::BOUNDARY{never:change_one_character_of_the_expert_text_or_of_the_expert_skill_files|scope:permanent}
::BOUNDARY{never:scan_a_code_log_in_authorize_or_pay_for_the_user|scope:permanent}

::RULE{one_question then 一次只问用户一件事 等他答了再往下|source:kit_onboarding}
::RULE{resume then 每做完一环在交接单里记一行；下次用户再说 AI全球自媒体 从没做完的那一环接着做|source:kit_handoff}
::RULE{least_hands then 用户能不动手的都由你做 不让他复制配置 不让他找地址 不让他填表；只有扫码 登录 授权 付款必须他本人|source:owner_2026-11-10}
::RULE{official_first then 豆包工作只给官方入口 接入步骤指向它自己的官方页面|source:kit_third_party_boundary}

::MODULE{PERSONA|title:第一环 装写作专家定成人格}
  [STEP] 1 persona_slot 里已经有公众号爆文专家的正文：告诉用户已装好 跳到 SOURCE
  [STEP] 2 从 repo 取最新发布的专家包；取不到就从 mirror 取同一份；两处都取不到：用一句话告诉用户 然后停
  [STEP] 3 把 skills 的文件夹原样拷进 skills_dir
  [STEP] 4 把 text 整段放进 persona_slot 不删不改；在文件头记下 soul_id 与 soul_version 与 soul_sha256
  [STEP] 5 报三行：技能装到了哪 哪几个在技能列表里 人格放在哪

::MODULE{SOURCE|title:第二环 内容源}
  [STEP] 1 先把 poster 那张海报打开给用户看 说一句：用微信扫码领三天体验卡 再点开通链接；你本身是生财会员就说 跳过
  [STEP] 2 用户说领好了或跳过：接下来的配置全由你做 不让用户复制或填写任何东西。先看本机有没有 npx；没有就问一句 用户点头后从 Node.js 官方源装长期支持版 做法同工具包装 Git 与 Python
  [STEP] 3 读 @DSH_MCP 的 doc 照官方做法加一台名叫 scys 的 stdio 服务器：command 填本机 npx 的绝对路径 Windows 上是 npx.cmd；args 照 @BRIDGE 的 args 逐项填；原有的服务器一台都不能少；需要用户点同意就告诉他点哪一项
  [STEP] 4 桥接器拉起浏览器之后 用户自己用生财账号登录授权；你不代扫码不代登录
  [STEP] 5 授权后只读搜一次最近加精的帖 列出标题；列得出就告诉用户内容源接好了
  [STEP] 6 说一句：推荐在本机装豆包工作 也接上生财 接入步骤看生财官方给豆包写的那一页

::MODULE{REPORT|title:做完告诉用户什么}
  [LINE] 人格：公众号爆文专家 版本号 放在哪
  [LINE] 内容源：生财 MCP 已接上 只读
  [LINE] 下一步：知识库 这一版还没有 等下一版

::RUBRIC{B1: 人格位置里是公众号爆文专家的正文|check:cmd|run:"python -c \"import io,sys;s=io.open('soul/agent.md',encoding='utf-8').read();sys.exit(0 if '[PROJECT:wechat_awesome]' in s else 1)\""|expect:0}
::RUBRIC{B2: 三个写作技能在技能目录里|check:cmd|run:"python -c \"import os,sys;sys.exit(0 if all(os.path.isdir(os.path.join('.dsh','skills',n)) for n in ('wechat-article','wechat-draft-push','wechat-topic-hunter')) else 1)\""|expect:0}
::RUBRIC{B3: 生财接上之后只读搜一次列出了标题 全程没有调用写操作|check:human}
::RUBRIC{B4: 第二环里用户没有复制或填写任何配置 只做了扫码 登录 授权|check:human}

::FALLBACK{expert_package_unreachable_on_both_sources then 用一句话告诉用户网络取不到专家包 然后停|user_has_no_scys_account_and_skips_the_card then 再给他看一次海报 说没有体验卡就接不上生财|bridge_cannot_start_or_the_browser_never_opens then 把报错原样给用户看 请他用自己的生财账号打开 @SCYS 的 entry 把那一页给的接入配置复制给你 照那一页再接一次 还不行就停在这一环并记进交接单|mcp_authorization_fails then 把屏幕上的报错原样给用户看 请他重新授权一次 还不行就停在这一环并记进交接单}

::PRIORITY{
  user_decision > BOUNDARY > OBJECTIVE > RUBRIC > RULE > MODULE
}
::ILANG::v5.0::ENGINEERING_BOOK
