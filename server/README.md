# iLang DSH 工具包的公开 Agent 服务

`worker.mjs` 是无状态 Cloudflare Worker，`content.mjs` 提供工具定义和固定公开文档目录。它不需要第三方 npm 依赖。

## 服务入口

- MCP：`POST https://dsh.ilang.guide/mcp`，Streamable HTTP，JSON 响应。
- REST：`GET /api/overview`、`/api/install?platform=windows`、`/api/search?q=记忆&limit=5`、`/api/docs?path=README.md`、`/api/skills`。
- 主页发送 `Accept: text/markdown` 时返回仓库 README；其他浏览器继续获得原 HTML 页面。HTTP Markdown 中的相对链接按原文所在目录转为 GitHub 绝对链接，图片使用原始文件链接；MCP 工具与资源保留文档原文。
- `/healthz` 返回服务版本和健康状态。

MCP 同时支持 `2026-07-28` 和旧客户端使用的 `2025-11-25`、`2025-06-18`。

- 2026 客户端可以直接发请求，或先调用 `server/discover`。每次请求都在 `params._meta` 中携带 `io.modelcontextprotocol/protocolVersion` 和 `io.modelcontextprotocol/clientCapabilities`；HTTP 头携带匹配的 `MCP-Protocol-Version`、`Mcp-Method`，工具调用和资源读取还携带匹配的 `Mcp-Name`。结果包含 `resultType: "complete"`。错误的头/体映射返回 `-32020`，未知版本返回 `-32022` 及支持版本清单。
- 2025 客户端先发送 `initialize`，接着发送 `notifications/initialized`，再调用 `tools/list`、`tools/call`、`resources/list`、`resources/read`。后续请求携带协商的 `MCP-Protocol-Version`。

POST 的 `Accept` 包含 `application/json, text/event-stream`。本服务不创建会话，不主动推送消息，`GET /mcp` 返回 405。

所有操作公开、只读，无需登录或 API key。工具读取固定 GitHub 仓库的公开资料；返回安装说明不会执行安装。用户的本地记忆、密钥和工作区不在服务数据范围内。文档原文作为资料返回，不改变调用方获得的用户授权。

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
