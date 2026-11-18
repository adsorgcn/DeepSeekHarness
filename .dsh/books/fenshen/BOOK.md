::ILANG::v5.0::ENGINEERING_BOOK
[TYPE:engineering_book]
[ID:DSH-FENSHEN]
[VERSION:1.1]
[DATE:2026-11-18]
[LANG:zh]

::STATE{@USER, role:decision_maker, is:在电脑上用 DSH 出过文 出过片 装了 Grok Bot 的人, does:给仓库地址 在 GitHub 加一把钥匙 在公众号后台加一个 IP 点头, never:贴钥匙到聊天}
::STATE{@AGENT, role:you_the_user_s_own_AI_running_in_DeepSeek_Harness_with_the_iLang_DSH_kit, does:把工作区推成私有仓库 把分身书交到手上 以后每次开工先 pull, never:把账本的值写进聊天 替用户注册 付款 点发布}
::STATE{@HANDS, first:Grok Bot 用户在「自媒体出海」里装好的, second:Muse, none:先走「自媒体出海」到装 Grok Bot 那一环}
::STATE{@BOOK, kit_copy:.dsh/books/fenshen/bot-fenshen-book.md 随工具包带着, kit_sha256:91b6766aefefabd3685bc46157f414aed0419bdaea84853a7764f68e6e1d2132, workspace_copy:bot-fenshen-book.md 放在工作区根目录 和 kit_copy 一字不差}
::STATE{@REPO, mode:git config dsh.mode 是 sync 就已经有私有远端 是 local 就还没有, remote:私有 GitHub 仓库 用户自己建 名字他起, guard:tools/hooks/pre-push 拒绝推到公开远端 不绕}
::STATE{@SCOPE, covers:工作区进私有仓库 分身书交到手上 两头共用一个仓库, later:多个分身 多平台 以后逐版加}

::OBJECTIVE{id:cloud_twin_handoff|owner:user|trust:trusted|version:1|status:active}
  target: 用户说一句 云端分身 之后 工作区在私有仓库里 分身书到了手上 手搬完回了六行 用户用手机说一句 出文 稿子进了仓库 电脑上的 DSH pull 到了
  ACCEPT: RUBRIC 每项通过
  NON_GOALS: 替用户建 GitHub 账号或仓库；把账本的值写进聊天；改两本书和人格的字；多个分身
  DONE_WHEN: 手回了 TWIN-READY 六行 用户用手机出了一篇稿 本地 pull 到了

::BOUNDARY{never:push_the_workspace_to_a_public_remote|scope:permanent}
::BOUNDARY{never:print_a_ledger_value_a_key_or_a_password_in_chat_or_write_one_into_a_new_file|scope:permanent}
::BOUNDARY{never:change_one_character_of_bot-fenshen-book.md_or_of_the_books_it_names|scope:permanent}
::BOUNDARY{never:scan_a_code_log_in_authorize_pay_or_press_publish_for_the_user|scope:permanent}

::RULE{one_question then 一次只问用户一件事 等他答了再往下|source:kit_onboarding}
::RULE{resume then 每做完一步在交接单里记一行；下次用户再说 云端分身 从没做完的那一步接着做|source:kit_handoff}
::RULE{pull_first then 从交书那天起 每次开工先 git pull 做完立刻 commit 和 push 分身也这么做 两头共用一个仓库|source:owner_2026-11-18}
::RULE{least_hands then 用户亲手的只有 建私有仓库 加一把钥匙 加一个 IP 点头|source:owner_2026-11-10}

::MODULE{M0_READY|title:第一步 看条件}
  [STEP] 1 看交接单 Grok Bot 装了没 没装就告诉用户先说一句 自媒体出海 走到装 Grok Bot 那一环 到此为止
  [STEP] 2 看 git config dsh.mode 是 sync 就到 M2 是 local 就到 M1
::MODULE{M1_REPO|title:第二步 工作区进私有仓库}
  [STEP] 1 告诉用户 他的工作区要有一个私有仓库 分身和电脑共用 请他在 GitHub 建一个私有仓库 名字他起 建好把地址贴你 没有 GitHub 就请他注册 手机码用他自己的
  [STEP] 2 核地址指向私有仓库 不是私有停下说出来
  [STEP] 3 git remote add origin 用户给的地址 跑 python -X utf8 tools/brain.py check 0 错再推 推之前钩子会拦公开远端 不绕 钩子认不出远端时会要一次 git config --bool brain.allowPush.origin true 照它打印的做
  [STEP] 4 推上去 git config dsh.mode sync 交接单记一行
::MODULE{M2_BOOK|title:第三步 把分身书放到工作区}
  [STEP] 1 把 @BOOK 的 kit_copy 原样复制到工作区根目录 文件名不变 UTF-8 LF 核 sha256 和 kit_sha256 一样
  [STEP] 2 跑 python -X utf8 tools/ilang_grammar_validator.py --lint bot-fenshen-book.md --strict 不是 0 错就停下说出来
  [STEP] 3 commit 并 push 这个文件也在仓库里 手克隆下来就有
::MODULE{M3_HANDOFF|title:第四步 交书}
  [STEP] 1 告诉用户 打开 Grok Bot 的聊天 把工作区里的 bot-fenshen-book.md 拖进去 打一句 照这本书做 发出去 然后把仓库地址发给它
  [STEP] 2 之后加钥匙 加白名单 点头 都听手的 它一次一步教 你不替他答
  [WAIT] 用户说 手回了 TWIN-READY
::MODULE{M4_VERIFY|title:第五步 两头对一次}
  [STEP] 1 git pull 看到手的提交 交接单里有分身那一行才算
  [STEP] 2 请用户用手机对手说一句 出文 等他说稿子出来了 再 git pull 看 articles/ 里多了那一篇
  [STEP] 3 从今天起每次开工先 git pull 把这条记进交接单
::MODULE{REPORT|title:每做完一步告诉用户什么}
  [LINE] 仓库在哪 私有不私有 推没推上去
  [LINE] 书放在哪 怎么拖 说哪一句
  [LINE] 手回的六行里出口走的哪一种 白名单加了没
  [LINE] 两头对过没 以后他在手机上说的三句口令
::RUBRIC{G1: 远端是私有仓库 本地 HEAD 已推上去|check:cmd|run:"git status -sb"|expect:no_ahead}
::RUBRIC{G2: 工作区根目录的分身书和工具包里那份一字不差|check:cmd|run:"python -X utf8 -c \"import hashlib,io,sys;h=lambda p:hashlib.sha256(io.open(p,'rb').read().replace(b'\\r\\n',b'\\n')).hexdigest();sys.exit(0 if h('bot-fenshen-book.md')==h('.dsh/books/fenshen/bot-fenshen-book.md') else 1)\""|expect:0}
::RUBRIC{G3: 手回了 TWIN-READY 六行 交接单里有分身那一行|check:human}
::RUBRIC{G4: 用户用手机出了一篇稿 本地 pull 到了|check:human}
::RUBRIC{G5: 全程没有在聊天或新文件里出现任何钥匙值|check:human}
::FALLBACK{no_bot then 告诉用户先说 自媒体出海 到此为止|remote_not_private then 停下 请用户改成私有|hook_blocks_push then 远端是公开的 不绕 请用户换私有仓库|hand_never_reports then 请用户把手回的话原样贴你 没回就记成没搬完|pull_conflict then 以远端为准 自己的改动另起一次提交 不强推}
::PRIORITY{ BOUNDARY > 仓库私有 > 用户点头 > 两头同一个仓库 > 快 }
::ILANG::v5.0::ENGINEERING_BOOK
