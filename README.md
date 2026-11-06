<img src="assets/social-preview.png" alt="别人的 DSH 是个聊天框。你的，一句话满配。" width="100%">

# DeepSeek Harness

**一句话，让你的 DSH 记住你、教会你、把环境装齐。**

> One sentence and your DeepSeek Harness remembers you. Memory · tutorial · one-click install · skills — 一句话满配。

## 开始（你只做这一件事）

在线门面：https://adsorgcn.github.io/DeepSeekHarness

把下面这句话，原样贴给你的 DSH：

> 帮我把 https://github.com/adsorgcn/DeepSeekHarness 装成本地 DSH 全套：先按我的系统下载并运行仓库里的 bootstrap.ps1（Windows）或 bootstrap.sh（macOS、Linux），打不开 GitHub 就从 https://gitee.com/monetize/DeepSeekHarness 取同名文件；它默认只检测，缺什么软件列给我，逐个征得我同意后再从官方源安装；装完告诉我以后每个新窗口怎么一句话回到这里。

剩下的它全包：装环境（先问你再动手）、放好全套、问几个问题认识你。**你只粘贴、只点头。**（Windows 走 bootstrap.ps1，macOS 与 Linux 走 bootstrap.sh，由 DSH 按系统选。）

连不上 GitHub：自动走国内镜像 gitee.com/monetize/DeepSeekHarness，iLang 官方资料自动走 ilang.cn；私人记忆默认拦在本地，只有你确认的私有仓库才能备份。

在 DeepSeek Harness 0.2.2-rc.1 上验证（DSH 还是 Developer Preview，官方说可能有破坏性变更；装不上先看这一行）。

## 里面有什么

**记忆体** · 记住你的习惯、决定、规矩。换窗口、换电脑都不忘；每个新窗口开场，先汇报上次做到哪了。

**新手教程** · 从零开始玩 DSH。第一句就教你：先去学 iLang，学完再回来。

**一键安装** · 新电脑缺什么装什么。装任何东西前先问你，只走官方。

**技能库** · 好技能不断加进来。你刷到什么好东西，说一句「迭代进去」，它就进这个仓库。

## 以后每个新窗口

一句话：

> 进我的记忆体，看看上次到哪了。

或者把目录选成 DSH 的工作区，连这句话都不用说。

想更新引擎就贴：

> 把 DeepSeekHarness 的引擎更新到最新，不要动我的记忆。

## 放心

笔记是纯文本，你随时能看、能改、能删。**默认只存在你自己电脑上**；本地记忆默认不联网：出网的只有两件事——你向模型提问时的 API 请求，和你主动配置的备份（自己的私有仓库或同步盘）。不记密码：密钥只进你本机的加密 vault。

## 引用与致谢

本仓库站在公开学术工作之上，每一层都带 DOI / arXiv 锚点，作者有 ORCID 的挂 ORCID：

- iLang（[Long Quan Zhu](https://orcid.org/0009-0004-4540-8082)）：[DOI 10.5281/zenodo.21821452](https://doi.org/10.5281/zenodo.21821452)
- Mem-Forever（同作者）：[DOI 10.5281/zenodo.22865160](https://doi.org/10.5281/zenodo.22865160)
- DeepSeek-V4（DeepSeek-AI，arXiv 提交人 Wenfeng Liang）：[DOI 10.48550/arXiv.2606.19348](https://doi.org/10.48550/arXiv.2606.19348)

完整清单（R1 / V3 / Qwen3 / Whisper / DSec 与标准组件）见 [docs/CITATIONS.md](docs/CITATIONS.md)。

## 想看更多

- [CHANGELOG.md](CHANGELOG.md) · 更新记录
- [dsh-新手起手式.md](dsh-新手起手式.md) · DSH 新手从零开始
- [一键安装.md](一键安装.md) · 装的时候发生了什么
- [插件点评-ilang视角.md](插件点评-ilang视角.md) · 现在的插件缺什么
- [ROADMAP.md](ROADMAP.md) · 这个仓库的迭代清单

基于 [iLang](https://ilang.ai) v5.0 与 [Mem-Forever](https://github.com/ilang-ai/Mem-Forever) · MIT
