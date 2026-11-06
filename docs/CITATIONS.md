# 引用与致谢（Citations & Attribution）

本仓库的每一层都站在公开学术工作之上。规则：**有 DOI 挂 DOI，有 arXiv 挂 arXiv，作者有公开 ORCID 就做 ORCID 锚文本，查不到的不编。** 所有条目均已逐条核实。

## 我们构建于其上（直接依赖）

| 工作 | 作者（锚文本） | DOI / 标识 |
|---|---|---|
| iLang Protocol Specification 5.0（v3/v4/v5 全层：88 动词、f_v5、11 维向量、M1–M8） | [Long Quan Zhu](https://orcid.org/0009-0004-4540-8082)（静水流深） | [10.5281/zenodo.21821452](https://doi.org/10.5281/zenodo.21821452)（规范）· [10.5281/zenodo.23990334](https://doi.org/10.5281/zenodo.23990334)（5.0.5） |
| The Missing Definition of Right（iLang 判断层预印本） | [Long Quan Zhu](https://orcid.org/0009-0004-4540-8082) | [10.5281/zenodo.22882690](https://doi.org/10.5281/zenodo.22882690) |
| Mem-Forever（记忆层：交接单、一文件一记忆、OKF） | [Long Quan Zhu](https://orcid.org/0009-0004-4540-8082) | [10.5281/zenodo.22865160](https://doi.org/10.5281/zenodo.22865160) |
| METHOD-TO-BOOK-MOTHER v2.9（工程书母版，随仓库 gzip 分发，SHA256 见 .github/bot/MOTHER.source.txt） | iLang（作者同上） | [ilang.ai 源文件](https://ilang.ai/source-book/METHOD-TO-BOOK-MOTHER-v2.9-2026-10-30.ilang.md)（无 DOI） |
| ilang_grammar_validator（官方语法校验器，随仓库发布） | ilang-spec | [github.com/ilang-ai/ilang-spec](https://github.com/ilang-ai/ilang-spec)（MIT，无 DOI） |

## 模型（使用）

| 工作 | 作者 | DOI |
|---|---|---|
| DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence（`deepseek-flash` = DeepSeek-V4.1-Flash-1017 所属系列；1M 上下文） | DeepSeek-AI（arXiv 提交人：Wenfeng Liang） | [10.48550/arXiv.2606.19348](https://doi.org/10.48550/arXiv.2606.19348) |
| DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning | DeepSeek-AI | [10.48550/arXiv.2501.12948](https://doi.org/10.48550/arXiv.2501.12948) |
| DeepSeek-V3 Technical Report | DeepSeek-AI | [10.48550/arXiv.2412.19437](https://doi.org/10.48550/arXiv.2412.19437) |
| FunAudioLLM: Voice Understanding and Generation Foundation Models for Natural Interaction Between Humans and LLMs（DSH 实验性语音输入的本地 Provider SenseVoiceSmall 所属工作，视频转文字同款） | Tongyi SpeechTeam, Alibaba Group（Keyu An 等） | [10.48550/arXiv.2407.04051](https://doi.org/10.48550/arXiv.2407.04051) |

## 延伸阅读（同源哲学，非直接依赖）

| 工作 | 作者 | DOI |
|---|---|---|
| DeepSeek Elastic Compute (DSec): A Sandbox Infrastructure for Effective Agentic Training at Scale（智能体沙盒基础设施；与本仓库「代码决定、隔离执行」的工程哲学同源） | DeepSeek 团队（arXiv 提交人：Wenfeng Liang） | [10.48550/arXiv.2609.22978](https://doi.org/10.48550/arXiv.2609.22978) |

## 组件与标准（本身无 DOI，按规范引用）

- gzip（母版文件压缩）：[RFC 1952](https://www.rfc-editor.org/rfc/rfc1952)
- age（密钥库加密）：[age 规范 v1](https://age-encryption.org/v1)（Filippo Valsorda 与 Ben Cartwright-Cox）
- sherpa-onnx（语音模型推理运行时，视频转文字同款）：k2-fsa，Apache-2.0，无 DOI，[github.com/k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx)
- Silero VAD（语音活动检测，视频转文字同款）：snakers4，MIT，无 DOI，[github.com/snakers4/silero-vad](https://github.com/snakers4/silero-vad)
- yt-dlp（视频下载）：Unlicense，无 DOI，[github.com/yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
- FFmpeg（音视频处理）：LGPL/GPL，无 DOI，[ffmpeg.org](https://ffmpeg.org)
- REA（第三方，可选，只给官方入口）：morluto，MIT，无 DOI，[github.com/morluto/rea](https://github.com/morluto/rea)
- Git（记忆的版本控制与哈希链）：[git-scm.com](https://git-scm.com)
- Markdown / CommonMark：语言标准，无 DOI

## 关于本仓库自己的 DOI

Zenodo 自动归档已启用（owner 授权，2026-11-06）：

- **Concept DOI（覆盖全部版本）：[10.5281/zenodo.23998664](https://doi.org/10.5281/zenodo.23998664)**
- v1.0.18 版本 DOI：[10.5281/zenodo.23998665](https://doi.org/10.5281/zenodo.23998665)

引用本仓库请优先使用 concept DOI；后续每个 Release 自动追加版本 DOI。

## ORCID 说明（礼貌与铁律：有 ORCID 必挂链接，查不到就明说，不编造）

- Long Quan Zhu：[0009-0004-4540-8082](https://orcid.org/0009-0004-4540-8082)（已核实）
- Wenfeng Liang（梁文锋，DeepSeek-V4 与 DSec 两文作者/提交人）：**无公开 ORCID**——三重核查：① 同名检索 7 人均非 DeepSeek；② affiliation=DeepSeek 检索 48 人无他；③ 论文 HTML 作者块无其 ORCID 徽标。锚文本用 [arXiv 提交人页](https://arxiv.org/abs/2606.19348)。
- Keyu An（FunAudioLLM 一作）：**无公开 ORCID**（检索 5 条同名，均无 Alibaba/通义归属），不挂不编。
- DeepSeek 论文中以下作者有已核实 ORCID（检索口径 affiliation=DeepSeek，逐条比对 V4/DSec 作者名单）：

| 作者 | ORCID |
|---|---|
| Jingchang Chen | [0009-0003-3014-2077](https://orcid.org/0009-0003-3014-2077) |
| Yaohui Wang | [0009-0004-8848-4122](https://orcid.org/0009-0004-8848-4122) |
| Zuofan Wu | [0009-0009-5515-4414](https://orcid.org/0009-0009-5515-4414) |
| Ziwei Xie | [0009-0008-6109-5652](https://orcid.org/0009-0008-6109-5652) |
| Haoling Zhang | [0009-0000-2265-0360](https://orcid.org/0009-0000-2265-0360) |
| Zhizhou Ren | [0009-0004-9962-5816](https://orcid.org/0009-0004-9962-5816) |
| Panpan Huang | [0009-0008-2875-0184](https://orcid.org/0009-0008-2875-0184) |
| Shirong Ma | [0009-0008-1686-407X](https://orcid.org/0009-0008-1686-407X) |
| Yuhan Wu | [0000-0001-7115-5390](https://orcid.org/0000-0001-7115-5390) |
| Longhao Chen | [0009-0008-7803-8208](https://orcid.org/0009-0008-7803-8208) |
| Shiyu Wang | [0009-0007-6607-6568](https://orcid.org/0009-0007-6607-6568) |
| Yuxuan Liu | [0009-0008-2770-7926](https://orcid.org/0009-0008-2770-7926) |
| Damai Dai | [0009-0004-9714-7902](https://orcid.org/0009-0004-9714-7902) |
| Zhe Fu | [0009-0002-3292-1712](https://orcid.org/0009-0002-3292-1712) |
| Jiarui Wang | [0009-0005-1714-4961](https://orcid.org/0009-0005-1714-4961) |
| Yuan Cheng | [0009-0002-0762-4505](https://orcid.org/0009-0002-0762-4505) |
| Haoyu Chen | [0009-0005-9547-5678](https://orcid.org/0009-0005-9547-5678) |
| Junjie Qiu | [0009-0001-4831-6640](https://orcid.org/0009-0001-4831-6640) |
| Honghui Ding | [0009-0007-7231-4892](https://orcid.org/0009-0007-7231-4892) |
| Lingxiao Luo | [0009-0005-7989-8742](https://orcid.org/0009-0005-7989-8742) |
| Yixiao Chen | [0009-0008-5525-5891](https://orcid.org/0009-0008-5525-5891) |
| Han Yu | [0009-0002-1984-3625](https://orcid.org/0009-0002-1984-3625) |
| Shuiping Yu | [0009-0008-5427-998X](https://orcid.org/0009-0008-5427-998X) |
| Bingzheng Xu | [0009-0009-7633-0448](https://orcid.org/0009-0009-7633-0448) |
| Wenjun Gao | [0009-0008-6184-8888](https://orcid.org/0009-0008-6184-8888) |
| Zhangli Sha | [0009-0005-9644-1605](https://orcid.org/0009-0005-9644-1605) |

（其余 DeepSeek 归属 ORCID 记录以 ORCID 官方检索 affiliation=DeepSeek 为准；未逐一列名的作者不做个人锚文本。）
