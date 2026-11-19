# iLang DSH 工具包的公开 Agent 服务

`worker.mjs` 是无状态 Cloudflare Worker，`content.mjs` 提供工具定义和固定公开文档目录。公开 MCP 请求不创建会话，不需要账户、认证数据库或第三方 npm 依赖。

## 服务入口

- MCP：`POST https://dsh.ilang.guide/mcp`，Streamable HTTP，JSON 响应。
- REST：`GET /api/overview`、`/api/install?platform=windows`、`/api/search?q=记忆&limit=5`、`/api/docs?path=README.md`、`/api/skills`。
- 主页发送 `Accept: text/markdown` 时返回仓库 README；其他浏览器继续获得原 HTML 页面。HTTP Markdown 中的相对链接按原文所在目录转为 GitHub 绝对链接，图片使用原始文件链接；MCP 工具与资源保留文档原文。
- `/healthz` 返回服务版本和健康状态。

MCP 同时支持 `2026-07-28` 和旧客户端使用的 `2025-11-25`、`2025-06-18`。

- 2026 客户端可以直接发请求，或先调用 `server/discover`。每次请求都在 `params._meta` 中携带 `io.modelcontextprotocol/protocolVersion` 和 `io.modelcontextprotocol/clientCapabilities`；HTTP 头携带匹配的 `MCP-Protocol-Version`、`Mcp-Method`，工具调用和资源读取还携带匹配的 `Mcp-Name`。结果包含 `resultType: "complete"`。错误的头/体映射返回 `-32020`，未知版本返回 `-32022` 及支持版本清单。
- 2025 客户端先发送 `initialize`，接着发送 `notifications/initialized`，再调用 `tools/list`、`tools/call`、`resources/list`、`resources/read`。后续请求携带协商的 `MCP-Protocol-Version`。

POST 的 `Accept` 包含 `application/json, text/event-stream`。本服务不创建会话，不主动推送消息，`GET /mcp` 返回 405。

公开 `/mcp` 和 `/api/*` 无需登录或 API key。MCP 工具读取固定 GitHub 仓库的公开资料；返回安装说明不会执行安装。用户的本地记忆、模型密钥和工作区不在工具数据范围内。文档原文作为资料返回，不改变调用方获得的用户授权。

服务版本 `1.2.0` 的文档白名单共 21 项，包含 `.dsh/skills/source-book/SKILL.md`、`.dsh/books/chupian/BOOK.md`、`.dsh/books/fenshen/BOOK.md`、`.dsh/books/adspilot-sem/BOOK.md`，以及它们的 7 项公开随包依赖：变工程书的母版与来源记录、出片的执行正文与来源记录及两份原书、云端分身的执行正文。它们可通过原有文档读取、检索、资源读取与 HTTP 文档入口获取；工具数量仍为 5 个。市场工具动态读取仓库当前清单，返回已经登记的版本与出处。

`.github/bot/MOTHER-v2.9.ilang.md.gz` 是固定白名单中唯一的 gzip 文档。服务流式解压，超过 600000 字节即取消；随后验证 `MOTHER.source.txt` 记录的 SHA256，再返回 UTF-8 原文。压缩损坏、超限或摘要变化返回 502，不把二进制当文字输出。JSON 来源记录返回 `application/json`，文本记录返回 `text/plain`，其余文档返回 `text/markdown`。外部媒体链母版继续使用原书指明的官方 URL；白名单不读取用户私有仓库、人格、记忆、密钥或任意外部 URL。

「变工程书」「出片」「云端分身」「SEM 与付费投流」描述用户自己的 Agent 与 Grok Bot / Muse 所执行的工作流；本服务只返回公开说明，不具备视频生成、私有仓库同步、平台发布或广告投放权限。

## 未启用的认证声明

当前产品的 `/mcp` 和 `/api/*` 全部公开免认证。OAuth 发现文档只声明未来接口，明确带有 `status: under_construction`、`available: false`、`capabilities_status: planned_contract_only`、`launch_date: null`；它们不是运行中的 OAuth 或 OIDC 服务。

- `/.well-known/oauth-authorization-server` 与 `/.well-known/oauth-protected-resource` 发布上述不可用状态；资源标识是原站 origin，未来操作路径另列于 `planned_resource_endpoint`。
- `/.well-known/jwks.json` 是停用的空密钥集合（`keys: []`），不用于验证令牌。
- `/agent-auth/authorize`、`/agent-auth/token`、`/agent-auth/register`、`/agent-auth/claim`、`/agent-auth/resource` 始终返回 HTTP 503、简短不可用说明与 `Cache-Control: no-store`。处理器不读取或存储身份正文，不创建账户，不签发令牌，不发送邮件，也不发起授权跳转。
- 声明和未来路由不加入 sitemap；响应应标记 `X-Robots-Tag: noindex`。它们不会给公开服务增加 401 门槛、`WWW-Authenticate` 或 OpenAPI security 要求。

[`docs/auth.md`](../docs/auth.md) 告诉 Agent 在不可用期间继续使用公开工具；[`docs/openapi-auth.json`](../docs/openapi-auth.json) 仅记录未来路由当前的 503 合约。发现文件中的计划字段不能作为认证已可用的证据。

## 回源与部署

默认静态回源为 `https://raw.githubusercontent.com/adsorgcn/DeepSeekHarness/main/docs/`；文档回源限定为同一仓库 `main` 的固定白名单。不存在从请求参数读取任意 URL 的通道。

可使用 `STATIC_ORIGIN` 指定另一个明确的 HTTPS 静态资源根目录；不能指向正在处理请求的域名，避免回环。静态页面和资源继续跟随原仓库，Worker 代码变动需重新部署。


## 本地验收

```sh
node --test server/worker.test.mjs
```

测试覆盖五个工具的真实仓库内容、资源读取、路径白名单、传输协议、错误处理、Markdown 协商、静态页面回源和请求大小限制。

线上只读验收使用 `server/smoke.mjs`。安装官方 `@modelcontextprotocol/sdk`，或将 `MCP_SDK_ROOT` 环境变量设为本机已有 SDK 包目录；运行：

```sh
node server/smoke.mjs https://dsh.ilang.guide/mcp report.json
```

该脚本检查现代协议的发现、五个工具、资源读取，以及官方 SDK 的旧协议互操作。可将第一个参数换成预发布 HTTPS 地址，第二个报告路径可省略。

协议依据：[MCP 2026 发现](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)、[MCP 2026 Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)、[旧客户端生命周期](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)。
