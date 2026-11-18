# integration-bridge — 集成桥

> 把外部服务/协议接进 DSH:MCP server、API 网关、数据源。

## 定义

连接层的工具:把 MCP server、API 网关、数据源接进来。判定标准:价值在"连通性"而非"功能本身"。

## 成员(人工确认)

| 条目 | 星标 ⚠ | 说明 |
|------|--------|------|
| omdsh-dev/dsh-data-agent | 55 | 不引驱动:把九种数据库 CLI 包成 7 个工具,再给 schema 建一部版本化 Catalog([01](01-dsh-data-agent.md) ★★★) |

## 立卡条件

被 ≥5 个条目复用同一桥接协议。

> 本轮破例:55 星、下载 1,746、0 个条目复用其协议;按"本册唯一成员 + 数据接入的高下载样本"立卡。门槛未变。

## 生长

**它不是 MCP 桥,而是 CLI 执行面 + 版本化元数据的组合**:八种库走本机 CLI(argv 只放 flags、SQL 走 stdin、密码只走 `MYSQL_PWD`/`PGPASSWORD`/… 环境变量或 stdin 前缀),唯 ClickHouse 用 npm 客户端;7 个工具靠 preset + `tools.restrict({deny})` 收窄,不靠 allowlist。schema 侧是一条 `/schema` 的 `UNION ALL` 系统目录查询,用 `assetId = sha256(identity)`、`sourceId = profileId` 形成可 diff 的 Catalog——**"连接"本身没有协议,可复用的是这份 Catalog 的形状**。

代价也很直接:`readonly` 默认关闭,`sql-write` 没有接入审批栈,`ctx.subprocess.spawn` 绕开 bash 的 sandbox;Web 路由直接信任调用方传入的 `sessionId`,没有归属校验。另有一条启动风险:preset 的 persona 前缀使用 `{{cwd}}`,而 0.2.1-rc.5 的插值只注册了 `provider/model`,装配期可能直接抛错(卡内标"判断",与仓库 issue 吻合)。
