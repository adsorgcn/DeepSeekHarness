::ILANG::v5.0::ENGINEERING_BOOK
[TYPE:engineering_book]
[ID:DSH-INSTALL]
[VERSION:1.0]
[DATE:2026-11-19]
[LANG:zh]

::FACT{context|conf:confirmed}
  T:用户在 DeepSeek Harness 里贴了一句 帮我装 iLang DSH 工具包 照 https://dsh.ilang.guide/install.md 做 这页就是那句话的全文 你读完照做 用户什么都不用懂
  T:工具包仓库 https://github.com/adsorgcn/DeepSeekHarness 国内镜像 https://gitee.com/monetize/DeepSeekHarness 两边同源
  T:安装脚本在仓库根目录 Windows 用 bootstrap.ps1 macOS 和 Linux 用 bootstrap.sh 默认只检测不改动 加 -Install -Yes 才执行
  T:官方插件 dsh-plugin-chuhai 在 npm 上 用你装插件的工具装 只填包名 国内连不上 npm 官方源 DSH 会自动走镜像

::STATE{@USER, role:decision_maker, is:刚装好 DeepSeek Harness 的人 可能什么都不懂, does:选创造模式 贴那一句 每次你问装不装时点头或摇头, never:自己敲命令 自己找软件}
::STATE{@AGENT, role:you_DeepSeek_Harness_in_creator_mode, has:装插件的工具 下载文件 跑脚本, does:按这页一步一步做 缺什么先问再装 卡住自己修, never:没问过就装任何软件 从非官方源装 把用户的密码或钥匙写进任何文件}
::STATE{@MODE, need:创造模式 只有它手里有装插件的工具 装不上东西时它能自己修, check:看你现在手里有没有装插件的工具 没有就不是创造模式}
::STATE{@SOURCES, repo:https://github.com/adsorgcn/DeepSeekHarness, mirror:https://gitee.com/monetize/DeepSeekHarness, raw:https://raw.githubusercontent.com/adsorgcn/DeepSeekHarness/main/, mirror_raw:https://gitee.com/monetize/DeepSeekHarness/raw/main/, docs:https://dsh.ilang.guide/, docs_cn:https://ilang.cn/guide/dsh/}
::STATE{@BOOTSTRAP, windows:bootstrap.ps1 检测 powershell -ExecutionPolicy Bypass -File bootstrap.ps1 执行加 -Install -Yes, unix:bootstrap.sh 检测 bash bootstrap.sh 执行加 -Install -Yes, does:检测 git python 等 克隆仓库 注入 AGENTS 发现技能 跑 brain.py check 建档案 写交接单, installs_only_from:官方源 winget 官方包 Git.Git 和 Python.Python.3.12 没有 winget 就给官方下载链接让用户点一下}

::OBJECTIVE{id:install_kit|owner:user|trust:trusted|version:1|status:active}
  target: 工具包装在用户电脑上 brain.py check 0 错 官方插件装上或用户说不装 用户知道以后每个新窗口怎么一句话回来 知道 自媒体出海 这句话怎么用
  ACCEPT: RUBRIC 每项通过
  NON_GOALS: 装不在清单上的软件 改系统设置 上传任何东西 替用户注册账号 把钥匙写进文件
  DONE_WHEN: 用户关掉窗口再打开同一个工作区 说一句 进我的记忆体 看看上次到哪了 你能接上

::BOUNDARY{never:install_anything_before_the_user_says_yes_to_that_item|scope:permanent}
::BOUNDARY{never:install_from_a_source_that_is_not_the_official_one_named_in_@BOOTSTRAP|scope:permanent}
::BOUNDARY{never:write_a_password_a_key_or_a_token_into_any_file_or_chat|scope:permanent}
::BOUNDARY{never:claim_a_step_is_done_before_you_saw_it_succeed|scope:permanent}

::RULE{mode_first then 不是创造模式就先别动手 告诉用户 新开一个任务 模式选 创造模式 再把那一句贴一遍 到此为止|source:owner}
::RULE{one_question then 一次只问一件事 用他能懂的话 不说术语 等他答了再往下|source:kit_onboarding}
::RULE{detect_then_ask then 脚本默认只检测 缺什么列给用户 一样一样问 他点头的才装 都从官方源|source:bootstrap}
::RULE{fix_dont_stop then 哪一步装不上或卡住 你自己想办法修好 装好再往下走 被权限拦了就向用户申请一次放行 不绕过|source:owner}
::RULE{mirror then GitHub 打不开就从 @SOURCES 的 mirror 取同名文件 iLang 官方资料走 ilang.cn|source:kit}
::RULE{quiet then 用户看到的是一句话进展和一个问题 不是你的命令行 他问了再给|source:kit}

::MODULE{M0_MODE|title:第一步 看自己是不是创造模式}
  [STEP] 1 看手里有没有装插件的工具 有就是创造模式 往下
  [STEP] 2 没有 用一句话告诉用户 请他新开一个任务 模式选 创造模式 再把那一句贴一遍 然后停下 什么都不做
::MODULE{M1_GET|title:第二步 取脚本}
  [STEP] 1 看用户的系统 Windows 取 bootstrap.ps1 macOS 或 Linux 取 bootstrap.sh 从 @SOURCES 的 raw 取 取不到从 mirror_raw 取同名文件
  [STEP] 2 放到用户能找到的目录 告诉他一句放在哪了
::MODULE{M2_DETECT|title:第三步 只检测}
  [STEP] 1 照 @BOOTSTRAP 的检测跑法跑一次 不加 -Install
  [STEP] 2 把缺的软件列给用户 一样一行 这是什么 为什么要 从哪装 一样一样问他装不装
  [STEP] 3 没缺的 直接到 M3
::MODULE{M3_INSTALL|title:第四步 装}
  [STEP] 1 用户点头的 照 @BOOTSTRAP 的执行跑法跑 加 -Install -Yes 脚本会克隆仓库 注入 AGENTS 发现技能 跑 brain.py check 建档案 写交接单
  [STEP] 2 哪一步失败 看报错 自己修 修好接着跑 被权限拦了向用户申请一次放行
  [STEP] 3 跑完看 brain.py check 是不是 0 错 不是就修到是
::MODULE{M4_PLUGIN|title:第五步 官方插件 问一次}
  [STEP] 1 问用户一次 要不要装官方插件 dsh-plugin-chuhai 做自媒体出海用的 他点头才装
  [STEP] 2 用你装插件的工具装 包名 dsh-plugin-chuhai 装不上不拦别的事 告诉他一句就行
::MODULE{M5_HANDOFF|title:第六步 告诉他怎么回来}
  [STEP] 1 告诉用户 以后每个新窗口 打开同一个工作区 说一句 进我的记忆体 看看上次到哪了 就接着上次
  [STEP] 2 告诉用户 想做自媒体出海 说一句 自媒体出海 工具包会一步一步带 他只管点头
  [STEP] 3 问几个问题认识他 叫什么 做什么 想先做哪件事 记进工作区的 MEMORY.md
::MODULE{REPORT|title:做完回四行}
  [LINE] 装了什么 没装什么 为什么
  [LINE] 工作区在哪 brain.py check 结果
  [LINE] 插件装了没
  [LINE] 以后怎么回来那一句
::RUBRIC{I1: brain.py check 0 错|check:cmd|run:"python -X utf8 tools/brain.py check"|expect:0}
::RUBRIC{I2: 每个装上的软件都是用户点过头的 都来自官方源|check:human}
::RUBRIC{I3: 用户关窗口再开 说一句 进我的记忆体 看看上次到哪了 能接上|check:human}
::RUBRIC{I4: 聊天和文件里没有任何密码或钥匙|check:human}
::FALLBACK{not_creator_mode then 停下 请用户新开任务选创造模式再贴一遍|github_unreachable then 走 gitee 镜像取同名文件|no_winget then 给官方下载链接 用户点一下 装完接着跑|script_fails then 看报错自己修 修不好把报错原样给用户 不编|plugin_fails then 告诉用户一句 不拦别的事 以后再装}
::PRIORITY{ BOUNDARY > 用户点头 > 官方源 > 修好再走 > 快 }
::ILANG::v5.0::ENGINEERING_BOOK
