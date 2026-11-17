# Auth.md — iLang DSH 工具包：访问与认证

## 公开只读服务

本网站的 MCP、HTTP API、技能目录和文档均为公开只读内容。无需注册、登录、API Key 或 OAuth 授权，也不要向这些接口发送账户密码、模型密钥或私人记忆。

- MCP（Streamable HTTP）：`https://dsh.ilang.guide/mcp`
- HTTP API 说明：`https://dsh.ilang.guide/openapi.json`
- 接入说明：`https://dsh.ilang.guide/agents/`

MCP 客户端的认证方式选择「无」。建立连接后调用 `tools/list` 查看工具，再用 `tools/call` 读取所需公开资料。

## 权限边界

服务只提供公开仓库中的产品说明、安装指引、文档检索和技能目录。它不能读取你的本地文件，不能写入你的记忆，也不能执行安装、提交、发布或付款。

本地安装由你使用的 Agent 在自己的运行环境里执行。安装软件和插件前，仍须按安装说明取得你的确认。本网站的公开读取权限不构成这些操作的授权。

## 响应与错误

- 成功读取返回 HTTP 200；MCP 通知可返回 HTTP 202。
- 无效参数或不支持的方法按 MCP JSON-RPC / HTTP API 返回错误。
- 公开服务不发放访问令牌；客户端无需发起 OAuth 授权。

源代码与问题反馈：https://github.com/adsorgcn/DeepSeekHarness
