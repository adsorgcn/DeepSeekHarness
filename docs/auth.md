# auth.md — iLang DSH 工具包：公开访问

## 当前可用：公开只读，无需认证

读取 iLang DSH 工具包的安装说明、文档和技能市场，不需要注册、登录、密码、API Key 或访问令牌。

- MCP（Streamable HTTP）：https://dsh.ilang.guide/mcp
- HTTP API：https://dsh.ilang.guide/openapi.json
- 接入说明：https://dsh.ilang.guide/agents/
- 文档导航：https://dsh.ilang.guide/llms.txt

在 MCP 客户端中选择认证方式「无」。连接后调用 `tools/list` 查看工具，再用 `tools/call` 查询资料。服务只返回公开资料，不读取个人记忆，不执行安装、发布或账户操作。

## Coming soon：认证能力尚未启用

**Coming soon. Authentication is unavailable. Public lookups remain available without authentication.**

```json
{
  "status": "under_construction",
  "available": false,
  "capabilities_status": "planned_contract_only",
  "launch_date": null
}
```

OAuth 发现文件描述的是未启用的未来接口声明，不是正在运行的认证服务，也不代表已提供登录或令牌校验。`grant_types_supported`、`response_types_supported`、身份类型及 scope 等标准字段在这些文件中仅为计划占位值，以同一文件中的不可用状态为准。

当 `available` 为 `false` 时，Agent 不应尝试注册、认领、发起授权或请求令牌，也不应向这些地址提交密码、密钥或身份资料。继续使用上面的公开 MCP 和 HTTP API 即可。

## 未来接口的当前行为

以下路径当前都返回 **HTTP 503** 和 `Cache-Control: no-store`，说明认证未启用。它们不创建账户、不签发令牌、不发送邮件、不发起 OAuth 跳转，也不读取或存储提交的身份资料。

| 路径 | 声明用途 | 当前状态 |
| --- | --- | --- |
| `/agent-auth/authorize` | 未来授权入口 | 未启用，HTTP 503 |
| `/agent-auth/token` | 未来令牌入口 | 未启用，HTTP 503 |
| `/agent-auth/register` | 未来注册入口 | 未启用，HTTP 503 |
| `/agent-auth/claim` | 未来认领入口 | 未启用，HTTP 503 |
| `/agent-auth/resource` | 未来受保护资源 | 未启用，HTTP 503 |

这类 503 是明确的未启用状态，不是需要用户登录后解决的错误。不要因此向公开 `/mcp` 或 `/api/*` 添加认证要求。

## 发现文件

- [OAuth 未来接口声明](https://dsh.ilang.guide/.well-known/oauth-authorization-server)
- [未来资源声明](https://dsh.ilang.guide/.well-known/oauth-protected-resource)
- [停用的密钥集合](https://dsh.ilang.guide/.well-known/jwks.json)：`keys` 为空，不用于令牌验证。
- [未启用接口的状态规范](https://dsh.ilang.guide/openapi-auth.json)：只描述当前 503 响应，不提供可执行认证流程。

公开资料来源：https://github.com/adsorgcn/DeepSeekHarness
