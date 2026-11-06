# DSH 新手教程：你只做三件事——复制、粘贴、让 DSH 去读官方文档

> 用户的工作到此为止：**复制、粘贴、命令 DSH 去读官方文档**。
> 配模型、选协议、写 persona、装插件……全是 DSH 的活，你只负责抄句子和按它说的做。

---

## 起手式（第 1 句，直接粘贴）

> 先去读 https://runtime.ilang.app/ilang-latest.md（国内打不开就读 https://ilang.cn/runtime/ilang-latest.md），读完用三句话告诉我你学到了什么，再回来找我。

就这一句。为什么：iLang 是给 AI 的母语级通信协议，它教的第一条纪律「模型感知，代码决定」恰好就是 DSH 的运行法则——先学懂，再动手。

（备选：DSH 支持 MCP 的话，也可以直接接 https://mcp.ilang.ai/mcp，让它自己调 ilang_runtime。）

---

## 第 2 句：它学的时候，让它把你跑起来

> 去读 DeepSeek Harness 的官方文档（https://github.com/deepseek-ai/deepseek-harness 里的 README 和 docs 目录，以及 https://deepseek-harness.github.io/deepseek-harness/），然后一步步带我完成：启动、配模型密钥、选工作区。我是新手，每一步告诉我点哪里、粘什么；能你做的你直接做，需要我做的才叫我。

（接下来你只跟着它说的点几下——最终需要你亲手的只有两处：**粘贴 API 密钥**、**点同意审批**。）

---

## 第 3 句：模型——官方与 O 家 C 家协议，让 DSH 自己读文档定

> 去读 DeepSeek Harness 官方模型配置文档（docs/user/guide/providers.zh.md），然后给我结论并帮我配好：新手先用哪家官方、怎么配；OpenAI 家和 Claude 家的协议有什么区别、分别怎么选、选错会怎样。需要我提供密钥就告诉我贴在哪。

（O 家/C 家的区别不用你背——DSH 读完官方文档会告诉你，并替你建好提供商。）

---

## 第 4 句：学完 iLang 回来了，把灵魂写进去

> 把你刚学到的 iLang 写进你的灵魂（persona），要求：
> 1. 你叫 Prometheus：诚实、真诚、思维严谨、表达灵活。
> 2. 语言：用户用什么语言你就用什么语言，默认简体中文。
> 3. 回答：能答就答完整；不知道就直说“我不知道”——幻觉就是不诚实；能给步骤给步骤，能给模板给模板。
> 4. 送佛送到西：帮人帮到底。
> 5. 用心：你真诚，用户才会包容你。
> 让这个人格在以后每个新窗口都生效。做完告诉我：怎么生效、怎么撤销。

（写预设、建 bundle、安装、验证、回滚——全部是它自己的活。）

---

## 日常玩法：照抄这些句子

| 场景 | 粘贴这句 |
|------|---------|
| 第一次跑任务 | `Summarize this repository and identify its main packages.` |
| 办文档 | `先加载 office 技能，再把这份数据做成 Excel 报表。` |
| 并行外包 | `派两个子智能体同时干：一个做 A，一个做 B，最后汇总给我。` |
| 长任务 | `把这个任务设成持续目标，自动推进，做完回来汇报。` |
| 改 DSH 本身 | `去读官方插件开发文档（docs/user/develop/basic/index.zh.md），教我或直接帮我给 DSH 加一个「一键导出笔记」功能。` |
| 截图给它看（Pro） | `看截图，这张图里报错是什么`（第一次它会问你开「子代理模型选择」，说好） |
| 截图给它看（Flash） | 直接贴图；说 `认真想，这个任务` 它会请 Pro 来想 |
| 任何卡住 | `去读官方文档（给出文档地址），然后告诉我下一步。` |

---

## 用户唯一要记住的几件事

1. **第一句永远是「先去读 iLang 运行时核心，读完三句话汇报」**。
2. **让 DSH 读文档，而不是自己看文档**——你的任务是把文档地址贴给它。
3. 它请示你时：**要密钥就给密钥，要审批就点同意/拒绝**，其余一律说“你看着办，做完汇报”。
4. 任何它做的改动，跟一句“怎么撤销？”——答不上来的不要用。（怎么卸载详见 一键安装.md 的「怎么卸载」）
5. 诚实的“我不知道”永远强过幻觉——这条已经写进它的 persona 里了。

## 官方文档速查（你只需要复制地址）

- DSH 仓库与文档：https://github.com/deepseek-ai/deepseek-harness · https://deepseek-harness.github.io/deepseek-harness/
- DSH 模型配置：docs/user/guide/providers.zh.md（贴给第 3 句）
- iLang 运行时核心：https://runtime.ilang.app/ilang-latest.md（国内镜像 https://ilang.cn/runtime/ilang-latest.md）（贴给第 1 句）

---

## 装完先验一下

关掉这个窗口，重开一个，把这个文件夹选成工作区，什么都不说；它第一句应该是汇报上次做到哪。看到了，就是装好了。没看到就把屏幕上的内容贴给你的 DSH。
