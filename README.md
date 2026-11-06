<img src="assets/social-preview.png" alt="别人的 DSH 是个聊天框。你的，一句话满配。" width="100%">

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23998664.svg)](https://doi.org/10.5281/zenodo.23998664)

# DeepSeek Harness

**别人的 DSH 是个聊天框。你的，一句话满配。**

> One sentence and your DeepSeek Harness remembers you. Memory · tutorial · one-click install · skills.

记忆体 · 新手教程 · 一键安装 · 技能库。你只做两件事：粘贴、点头。

在线门面：https://dsh.ilang.guide/ （微信、QQ 里分享用下面的指导站地址）

指导站：https://ilang.cn/guide/dsh/ ——一页讲清贴哪句、会发生什么、怎么验收，Agent 可读的孪生在同一页；微信、QQ 里分享用这个地址。

## 那句话

在任意 DSH 会话里，把下面这句原样贴给它：

> 帮我把 https://github.com/adsorgcn/DeepSeekHarness 装成本地 DSH 全套：先按我的系统下载并运行仓库里的 bootstrap.ps1（Windows）或 bootstrap.sh（macOS、Linux），打不开 GitHub 就从 https://gitee.com/monetize/DeepSeekHarness 取同名文件；它默认只检测，缺什么软件列给我，逐个征得我同意后再从官方源安装；装完告诉我以后每个新窗口怎么一句话回到这里。

剩下它全包：装环境先问你再动手，放好全套，问几个问题认识你。Windows 走 bootstrap.ps1，macOS 与 Linux 走 bootstrap.sh，由 DSH 按系统选；软件只从官方源装；默认本机模式，什么都不上传。

连不上 GitHub：自动走国内镜像 gitee.com/monetize/DeepSeekHarness，iLang 官方资料自动走 ilang.cn。

在 DeepSeek Harness 0.2.2-rc.1 上验证（DSH 还是 Developer Preview，官方说可能有破坏性变更；装不上先看这一行）。

## 验收时刻

关掉窗口。重开。把那个文件夹选为工作区，什么都不说。它第一句就汇报上次做到哪。看到了，就是装好了。

## 里面有什么

**记忆体** · 窗口关了，进度还在。你的习惯、决定、规矩写成本地文件；换窗口不忘，换电脑贴一句「把我的记忆体备份到我自己的私有仓库」。每笔记忆 = 一次 git 提交，哈希链就是防伪链。

**新手教程** · 第一句，先学 iLang。教程不教你用 DSH：第一句让它去读 iLang 运行文件，读完用三句话告诉你学到了什么；第二句让它把你跑起来；第三句配模型，新手默认 deepseek-flash；第四句把灵魂写进去。四句话照抄，配模型、选协议、写人格全是它的活。

**一键安装** · 新电脑，一句话装齐。缺什么补什么，每步问你，只走官方源。可选免费全家桶：视频下载与视频转文字、笔记、语音，一件一审批。只装你点头同意的；删掉工作区项目文件就没了，另装的工具单独卸。

**技能库** · 好技能，随装随用。mem-forever、site-design-engine 起步，新技能持续进来；你刷到什么好东西，说一句「迭代进去」，它就进仓库。

## 以后每个新窗口

> 进我的记忆体，看看上次到哪了。

或者把目录选成 DSH 的工作区，连这句话都不用说。

更新引擎：

> 把 DeepSeekHarness 的引擎更新到最新，不要动我的记忆。

看图：新手用 Flash，截图直接贴；说「认真想」才请 Pro。

视频转文字：贴链接或文件，出文字和字幕，本地跑，不上传。

## 放心

你的记忆，只在你的电脑上。笔记是纯文本，随时能看、能改、能删。出网的只有两件事：你向模型提问的 API 请求，和你主动配置的备份（自己的私有仓库或同步盘）。不记密码，密钥只进本机加密 vault。

## 引用与致谢

本仓库站在公开学术工作之上，每一层都带 DOI / arXiv 锚点，作者有 ORCID 的挂 ORCID：

- iLang（[Long Quan Zhu](https://orcid.org/0009-0004-4540-8082)）：[DOI 10.5281/zenodo.21821452](https://doi.org/10.5281/zenodo.21821452)
- Mem-Forever（同作者）：[DOI 10.5281/zenodo.22865160](https://doi.org/10.5281/zenodo.22865160)
- DeepSeek-V4（DeepSeek-AI，arXiv 提交人 Wenfeng Liang）：[DOI 10.48550/arXiv.2606.19348](https://doi.org/10.48550/arXiv.2606.19348)

完整清单（R1 / V3 / SenseVoice / DSec 与标准组件）见 [docs/CITATIONS.md](docs/CITATIONS.md)。

## 想看更多

- [dsh-新手起手式.md](dsh-新手起手式.md) · 四句话，从零开始
- [一键安装.md](一键安装.md) · 装的时候发生了什么
- [CHANGELOG.md](CHANGELOG.md) · 更新记录，每次改动即发版
- [ROADMAP.md](ROADMAP.md) · 迭代清单
- [插件点评-ilang视角.md](插件点评-ilang视角.md) · 现在的插件缺什么

基于 [iLang](https://ilang.ai) v5.0 与 [Mem-Forever](https://github.com/ilang-ai/Mem-Forever) · MIT
