::ILANG::v5.0::ENGINEERING_BOOK
[TYPE:engineering_book]
[ID:DSH-CHUPIAN]
[VERSION:1.2]
[DATE:2026-11-18]
[LANG:zh]

::STATE{@USER, role:decision_maker, is:会用 DSH 出文章的人, does:说一句话或丢一张图 看样片 点头或给意见, never:写提示词 画分镜 装工具 交钥匙}
::STATE{@AGENT, role:you_the_user_s_own_AI_running_in_DeepSeek_Harness_with_the_iLang_DSH_kit, does:把出片书交到手上 收回成片 账和系列文档 记进交接单, never:自己生成图或视频 替用户扫码 登录 付款 点发布}
::STATE{@HANDS, first:Grok Bot 用户在「自媒体出海」里装好的 Premium 起带, second:Muse 用户在手脚那一步开的, none:先走「自媒体出海」到装 Grok Bot 那一环, model:手自带什么出图出片模型就用什么 不装别的 不要任何钥匙}
::STATE{@BOOK, kit_copy:.dsh/books/chupian/bot-chupian-book.md 随工具包带着, kit_sha256:97cd661c91476bf98523460c57a25b18263962b17a559335a341bc364224db8a, workspace_copy:bot-chupian-book.md 放在工作区根目录 和 kit_copy 一字不差, same_for:Grok Bot 与 Muse 同一本}
::STATE{@CANON, media_chain_mother:https://raw.githubusercontent.com/ilang-ai/ilang-spec/main/products/media-chain/mother/MEDIA-CHAIN-MOTHER.ilang.md, mother_sha256:040481ffea57b1d40fb38dcbdb7a99e649aea65eb6fef802c9c70e051a373049, mother_page:https://ilang.ai/media-chain/, validator:tools/ilang_grammar_validator.py}
::STATE{@SOURCES, vem:IML-VEM v1.2.2 自 https://x.com/ai_chuhai/status/2113817133838713167 所引的 X 文章, onecmd:AI-VIDEO-ONECMD v1.0 自 https://x.com/ai_chuhai/status/2118812420521054659 它由 @EianLu 发表的流程整理而来, where:.dsh/books/chupian/sources 与 SOURCE.json, rule:两本原文一字不改 随书带着}
::STATE{@SCOPE, covers:出图 出视频 一句话或一张图起 成品带媒体链, later:多语言版本 多平台发 以后逐版加}

::OBJECTIVE{id:first_clip_delivered|owner:user|trust:trusted|version:1|status:active}
  target: 用户说一句 出片 之后 出片书到了手上 手按书出了图或片 文件里带着请求和判决 系列文档回到工作区 用户看到成品并说行 做到哪一步记进交接单
  ACCEPT: RUBRIC 每项通过
  NON_GOALS: 你自己生成图或视频；替用户在手那边点任何按钮；多语言版本；发到任何平台
  DONE_WHEN: 用户说这条行 系列文档 成片和账记进交接单

::BOUNDARY{never:generate_an_image_or_a_video_yourself_the_hand_does_it|scope:permanent}
::BOUNDARY{never:change_one_character_of_bot-chupian-book.md_or_of_the_two_original_books_inside_it|scope:permanent}
::BOUNDARY{never:print_a_key_a_token_or_a_password_in_chat_or_write_one_anywhere|scope:permanent}
::BOUNDARY{never:scan_a_code_log_in_authorize_pay_or_press_publish_for_the_user|scope:permanent}
::BOUNDARY{never:post_or_send_a_finished_clip_anywhere|scope:permanent}

::RULE{one_question then 一次只问用户一件事 等他答了再往下|source:kit_onboarding}
::RULE{resume then 每做完一步在交接单里记一行；下次用户再说 出片 从没做完的那一步接着做|source:kit_handoff}
::RULE{least_hands then 用户能不动手的都由你做；拖文件 说一句话 点头 由他本人|source:owner_2026-11-10}
::RULE{hand_order then 两只手都有时 Grok Bot 优先 Muse 其次 用户点名就用点名的|source:owner_2026-11-18}
::RULE{title_unchanged then 输入是一篇文章 片名就是文章标题 一个字不改 译文照译不另起|source:owner_2026-11-18}

::MODULE{M0_HANDS|title:第一步 看手在不在}
  [STEP] 1 看交接单和工作区 Grok Bot 装了没 Muse 开了没 两样都没有就告诉用户 先说一句 自媒体出海 走到装 Grok Bot 那一环 到此为止
  [STEP] 2 有手就照 hand_order 定用哪只 一句话告诉用户
::MODULE{M1_BOOK|title:第二步 把出片书放到工作区}
  [STEP] 1 把 @BOOK 的 kit_copy 原样复制到工作区根目录 文件名不变 不改一字 UTF-8 LF
  [STEP] 2 核 sha256 和 kit_sha256 一样 再跑 python -X utf8 tools/ilang_grammar_validator.py --lint bot-chupian-book.md --strict 不是 0 错就停下说出来
  [STEP] 3 工作区里已经有这个文件且 sha256 一样 就不重复复制 直接到 M2 第 2 步
::MODULE{M2_HANDOFF|title:第三步 交书 用户说一句话}
  [STEP] 1 告诉用户 打开 Grok Bot 的聊天 Muse 同理 把工作区里的 bot-chupian-book.md 拖进去 打一句 照这本书做 发出去 再把想要的那句话或那张图发给它
  [STEP] 2 之后选路 故事 分镜 样片 闸门都在手那边 用户直接跟手说 你不替他答
  [WAIT] 用户说 手交片了
::MODULE{M3_COLLECT|title:第四步 收片 收账 收系列文档}
  [STEP] 1 请用户把手回的六行贴给你 把成片 系列文档和 sidecar 放进工作区 chupian/series/<系列ID>/ 手没给系列文档就请用户让手补
  [STEP] 2 照 @CANON 的母版取门禁 跑一遍 0 失败才算 跑不了就把原因告诉用户 不说过了
  [STEP] 3 交接单记一行 系列 ID 走的哪条路 版本数 花费 手是谁
::MODULE{REPORT|title:每做完一步告诉用户什么}
  [LINE] 用的哪只手 书放在哪 怎么拖 说哪一句
  [LINE] 收到的成片 时长 分辨率 文件在哪
  [LINE] 门禁结果 系列文档在哪
  [LINE] 下一步 他要新版本就直接跟手说 不用再找你
::RUBRIC{C1: 工作区根目录的出片书和工具包里那份一字不差|check:cmd|run:"python -X utf8 -c \"import hashlib,io,sys;h=lambda p:hashlib.sha256(io.open(p,'rb').read().replace(b'\\r\\n',b'\\n')).hexdigest();sys.exit(0 if h('bot-chupian-book.md')==h('.dsh/books/chupian/bot-chupian-book.md') else 1)\""|expect:0}
::RUBRIC{C2: 系列文档回到了工作区|check:cmd|run:"python -X utf8 -c \"import glob,sys;sys.exit(0 if glob.glob('chupian/series/*/*.ilang.md') else 1)\""|expect:0}
::RUBRIC{C3: 用户看到了成品并说行|check:human}
::RUBRIC{C4: 全程没有在聊天或文件里出现任何钥匙|check:human}
::RUBRIC{C5: 输入是文章时 片名等于文章标题|check:human}
::RUBRIC{C6: 用户亲手做的只有 拖文件 说一句话 在手那边点头|check:human}
::RUBRIC{C7: 出片书过校验器 strict 0 错|check:cmd|run:"python -X utf8 tools/ilang_grammar_validator.py --lint bot-chupian-book.md --strict"|expect:0}
::FALLBACK{no_hand then 告诉用户先说 自媒体出海 走到装 Grok Bot 那一环 到此为止|book_fails_validator then 停下 把校验器的话原样给用户 不发给手|hand_returns_no_series_document then 请用户让手按 TAIL 补 没有就记门禁未跑|gate_fails then 把失败项原话给用户 让手出下一个版本}
::PRIORITY{ BOUNDARY > 用户点头 > 原书与母版的规则 > 省钱 > 快 }
::ILANG::v5.0::ENGINEERING_BOOK
