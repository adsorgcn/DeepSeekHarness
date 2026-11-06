# 引用与致谢（Citations & Attribution）

本仓库的每一层都站在公开学术工作之上。规则：**有 DOI 挂 DOI，有 arXiv 挂 arXiv，作者有公开 ORCID 就做 ORCID 锚文本，查不到的不编。** 所有条目均已逐条核实。

## 我们构建于其上（直接依赖）

| 工作 | 作者（锚文本） | DOI / 标识 |
|---|---|---|
| iLang Protocol Specification 5.0（v3/v4/v5 全层：88 动词、f_v5、11 维向量、M1–M8） | [Long Quan Zhu](https://orcid.org/0009-0004-4540-8082)（静水流深） | [10.5281/zenodo.21821452](https://doi.org/10.5281/zenodo.21821452)（规范）· [10.5281/zenodo.23990334](https://doi.org/10.5281/zenodo.23990334)（5.0.5） |
| The Missing Definition of Right（iLang 判断层预印本） | [Long Quan Zhu](https://orcid.org/0009-0004-4540-8082) | [10.5281/zenodo.22960030](https://doi.org/10.5281/zenodo.22960030) |
| Mem-Forever（记忆层：交接单、一文件一记忆、OKF） | [Long Quan Zhu](https://orcid.org/0009-0004-4540-8082) | [10.5281/zenodo.22865160](https://doi.org/10.5281/zenodo.22865160) |
| METHOD-TO-BOOK-MOTHER v2.9（工程书母版，随仓库 gzip 分发，SHA256 见 .github/bot/MOTHER.source.txt） | iLang（作者同上） | [ilang.ai 源文件](https://ilang.ai/source-book/METHOD-TO-BOOK-MOTHER-v2.9-2026-10-30.ilang.md)（无 DOI） |
| ilang_grammar_validator（官方语法校验器，随仓库发布） | ilang-spec | [github.com/ilang-ai/ilang-spec](https://github.com/ilang-ai/ilang-spec)（MIT，无 DOI） |

## 模型（使用）

| 工作 | 作者 | DOI |
|---|---|---|
| DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence（`deepseek-flash` = DeepSeek-V4.1-Flash-1017 所属系列；1M 上下文） | DeepSeek-AI（arXiv 提交人：Wenfeng Liang） | [10.48550/arXiv.2606.19348](https://doi.org/10.48550/arXiv.2606.19348) |
| DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning | DeepSeek-AI | [10.48550/arXiv.2501.12948](https://doi.org/10.48550/arXiv.2501.12948) |
| DeepSeek-V3 Technical Report | DeepSeek-AI | [10.48550/arXiv.2412.19437](https://doi.org/10.48550/arXiv.2412.19437) |
| Qwen3 Technical Report（本地备用模型 qwen3:8b） | Qwen Team, Alibaba Group（An Yang 等） | [10.48550/arXiv.2505.09388](https://doi.org/10.48550/arXiv.2505.09388) |
| Robust Speech Recognition via Large-Scale Weak Supervision（DSH 实验性语音转写的 Whisper 底座） | OpenAI（Alec Radford 等） | [10.48550/arXiv.2212.04356](https://doi.org/10.48550/arXiv.2212.04356) |

## 延伸阅读（同源哲学，非直接依赖）

| 工作 | 作者 | DOI |
|---|---|---|
| DeepSeek Elastic Compute (DSec): A Sandbox Infrastructure for Effective Agentic Training at Scale（智能体沙盒基础设施；与本仓库「代码决定、隔离执行」的工程哲学同源） | DeepSeek 团队（arXiv 提交人：Wenfeng Liang） | [10.48550/arXiv.2609.22978](https://doi.org/10.48550/arXiv.2609.22978) |

## 组件与标准（本身无 DOI，按规范引用）

- gzip（母版文件压缩）：[RFC 1952](https://www.rfc-editor.org/rfc/rfc1952)
- age（密钥库加密）：[age 规范 v1](https://age-encryption.org/v1)（Filippo Valsorda 与 Ben Cartwright-Cox）
- Git（记忆的版本控制与哈希链）：[git-scm.com](https://git-scm.com)
- Markdown / CommonMark：语言标准，无 DOI

## 关于本仓库自己的 DOI

owner 已于 2026-11-06 在 GitHub 启用 Zenodo 自动归档：**下一个 Release 起，每个版本自动铸 DOI，同一 concept DOI 覆盖全部版本**。首个 DOI 铸成后，回填本节、README 徽章与 CITATION.cff 的 identifiers 字段。本仓库的引用建议在 DOI 就位后以 DOI 为准。

## ORCID 说明

- Long Quan Zhu：[0009-0004-4540-8082](https://orcid.org/0009-0004-4540-8082)（已核实）
- Wenfeng Liang（梁文锋）：**公开 ORCID 未查到**——ORCID 库中 7 位同名者均非 DeepSeek 相关；他在 arXiv 上以提交人身份出现在 DeepSeek-V4（2606.19348）与 DSec（2609.22978）两文。按本仓库纪律不编造，锚文本用 arXiv 页面。
