::ILANG::v5.0::ENGINEERING_BOOK
[TYPE:engineering_book]
[ID:AI-GLOBAL-MEDIA]
[VERSION:0.1.3]
[DATE:2026-11-10]
[LANG:zh]

::STATE{@USER, role:decision_maker, is:只会用豆包问问题的新手, does:说一句话 点头 扫码 粘贴 自己付钱}
::STATE{@AGENT, role:you_the_user_s_own_AI_running_in_DeepSeek_Harness_with_the_iLang_DSH_kit, does:everything_the_user_does_not_have_to_do, never:替用户扫码 登录 授权 付款}
::STATE{@KIT, persona_slot:soul/agent.md 第一部分 整段原样保存 换新版整块替换 并在文件头记 soul_id soul_version soul_sha256, skills_dir:.dsh/skills, poster:.dsh/books/ai-global-media/poster.jpg}
::STATE{@EXPERT, name:公众号爆文专家, repo:https://github.com/adsorgcn/WorkBuddy, mirror:https://gitee.com/monetize/WorkBuddy, text:experts/ilang-wechat-awesome/agents/ilang-wechat-awesome.md 开头两行分隔线之后的全部, skills:experts/ilang-wechat-awesome/skills 下的文件夹 至少 wechat-article wechat-draft-push wechat-topic-hunter}
::STATE{@SCYS, what:生财有术的官方 MCP, auth:OAuth 网页授权 用户自己用生财账号登录 配置里没有密钥, mode:只读, trial:体验卡用户也能接 开放搜索和阅读 每天有使用额度, limit:同一个生财账号可以同时接 7 个 Agent DeepSeek Harness 与豆包各占一个 互不影响, manage:https://scys.com/mcp 生财的接入管理页 用户可以在那里查看和撤销自己的连接}
::STATE{@PLUGIN, what:生财有术官方给 DeepSeek Harness 出的插件 许可 MIT, name:dsh-plugin-scys-mcp, source:npm, install:用 plugin_manager 工具安装这个组合包并启用, by_hand:左侧菜单 插件 右上角 添加插件 填 dsh-plugin-scys-mcp 点 安装 再点 立即启用, after:启用后它自动打开浏览器授权页 授权成功后几秒内工具出现, reauth:调用 mcp__scys-mcp__auth 重新打开授权页}
::STATE{@DOUBAO, what:豆包电脑版 下一环建知识库要用 接法照生财官方教程, path:左侧 技能 连接器 伙伴 再点右上角 新建 选 新建自定义连接器, name:scys-mcp, transport:HTTP, url:https://mcp.scys.com/shengcai-web/mcp, then:点保存 弹出 连接器需要授权 点 去授权 在浏览器里同意 连接器就自动加好, use:对话时选 本地电脑}
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
::RULE{official_first then 生财接进 DeepSeek Harness 与豆包 都照生财官方教程的做法 一个字段都不自己编|source:scys_official_tutorial}

::MODULE{PERSONA|title:第一环 装写作专家定成人格}
  [STEP] 1 persona_slot 里已经有公众号爆文专家的正文：告诉用户已装好 跳到 SOURCE
  [STEP] 2 从 repo 取最新发布的专家包；取不到就从 mirror 取同一份；两处都取不到：用一句话告诉用户 然后停
  [STEP] 3 把 skills 的文件夹原样拷进 skills_dir
  [STEP] 4 把 text 整段放进 persona_slot 不删不改；在文件头记下 soul_id 与 soul_version 与 soul_sha256
  [STEP] 5 报三行：技能装到了哪 哪几个在技能列表里 人格放在哪

::MODULE{SOURCE|title:第二环 内容源}
  [STEP] 1 先把 poster 那张海报打开给用户看 说一句：用微信扫码领三天体验卡 再点开通链接；你本身是生财会员就说 跳过
  [STEP] 2 用户说领好了或跳过：接下来的配置全由你做 不让用户复制或填写任何东西。照 @PLUGIN 的 install 把 name 这个插件装上并启用；这一步要用户点一次批准 就告诉他点哪一项
  [STEP] 3 插件启用后会自动打开浏览器授权页；没打开就照 @PLUGIN 的 reauth 再开一次 把授权链接给用户 请他用电脑上的浏览器打开 微信里打不开
  [STEP] 4 用户自己用生财账号登录 手机扫码 点同意；你不代扫码不代登录
  [STEP] 5 授权后只读搜一次最近加精的帖 列出标题；列得出就告诉用户内容源接好了
  [STEP] 6 说一句：下一环建知识库要用豆包 请在本机装好豆包电脑版。装好后带他把生财也接进豆包：照 @DOUBAO 的 path 走到填写框 你把 name transport url 三项打出来让他照着填 再照 then 授权；最后提醒 use

::MODULE{REPORT|title:做完告诉用户什么}
  [LINE] 人格：公众号爆文专家 版本号 放在哪
  [LINE] 内容源：生财 MCP 已接上 只读
  [LINE] 下一步：知识库 这一版还没有 等下一版

::RUBRIC{B1: 人格位置里是公众号爆文专家的正文|check:cmd|run:"python -c \"import io,sys;s=io.open('soul/agent.md',encoding='utf-8').read();sys.exit(0 if '[PROJECT:wechat_awesome]' in s else 1)\""|expect:0}
::RUBRIC{B2: 三个写作技能在技能目录里|check:cmd|run:"python -c \"import os,sys;sys.exit(0 if all(os.path.isdir(os.path.join('.dsh','skills',n)) for n in ('wechat-article','wechat-draft-push','wechat-topic-hunter')) else 1)\""|expect:0}
::RUBRIC{B3: 生财接上之后只读搜一次列出了标题 全程没有调用写操作|check:human}
::RUBRIC{B4: 接进 DeepSeek Harness 这一段用户没有复制或填写任何配置 只做了点批准 扫码 登录 授权|check:human}

::FALLBACK{expert_package_unreachable_on_both_sources then 用一句话告诉用户网络取不到专家包 然后停|user_has_no_scys_account_and_skips_the_card then 再给他看一次海报 说没有体验卡就接不上生财|plugin_cannot_be_installed_by_you then 把报错原样给用户看 请他照 @PLUGIN 的 by_hand 点一遍 这是生财官方教程的装法 还不行就停在这一环并记进交接单|mcp_authorization_fails then 把屏幕上的报错原样给用户看 请他重新授权一次 还不行就停在这一环并记进交接单}

::PRIORITY{
  user_decision > BOUNDARY > OBJECTIVE > RUBRIC > RULE > MODULE
}
::ILANG::v5.0::ENGINEERING_BOOK
