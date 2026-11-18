# dsh-data-agent — 不引驱动:把九种数据库 CLI 包成 7 个工具,再给 schema 建一部版本化目录

> 证据等级:★★★(源码级;`omdsh-dev/dsh-data-agent@6a649fe930aeab4247d3e8b936b6bf393aa71e8c`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 55 为 2026-08-19 历史采样;下载 1746 同为该日。`main` 的 HEAD 停在 2026-09-29。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `omdsh-dev/dsh-data-agent`([registry](../../../data/plugins/omdsh-dev__dsh-data-agent.yml)) |
| 类目 | tools([census](../../ecosystem/census.py) 1639 条) |
| 子分类 | `integration-bridge`(外部服务/数据源)——本册当前唯一成员 |
| 自述 | 「让 AI 帮你连数据库、写 SQL」。实际面比自述大:连接配置 + 读写分道的 SQL 工具 + 版本化 Catalog + 离线 HTML 分析报告 |
| 星标 ⚠ | **55**(2026-08-19 采样;2026-11-18 实时 **226**,约 4.1 倍) |
| 下载 ⚠ | **1746**(2026-08-19 采样;npm 上共 19 个版本,末版 `0.2.2` 发布于 2026-09-29) |
| 扩散 | **0**(`grep -ril 'data-agent' data/plugins/` 命中 2 条,减自身后只剩同名独立实现 `tomowang/dsh-data-agent`;判断,见「为什么它突出」) |
| 仓库 commit | `6a649fe9`(2026-09-29,`main`,`fix: 适配 DSH rc.2 并放宽版本限制 (0.2.2)`);仓库创建 2026-08-11,51 个 commit |
| 包形态 | npm `@yejiming/dsh-data-agent@0.2.2`;一个 Cordis bundle(2 行)+ 一个 Web client 半 + 一个装进 `$DSH_HOME/.agent-presets/data-agent/` 的 preset。**不走 MCP,不需要外部服务** |
| 代码规模 | `src/**/*.{ts,tsx}` **15 201 行 / 47 文件**(服务端 10 653 + Web 半 4 548),另 `src/**/*.css` 1 982 行;`tests/*.spec.*` 9 088 行 / 39 文件;GitHub `size` 17 464 KB |

## 它到底是什么

**它不是数据库驱动插件,而是一层「CLI 客户端调度器 + 语句分类器 + schema 版本库」。** 九种数据库里只有一种走 npm 依赖——`@clickhouse/client`(`package.json:90-97`);另外八种(mysql / postgres / sqlite / oracle / hive / impala / doris / sqlserver)一律要求宿主 PATH 上有对应命令行客户端:`DEFAULT_CLIENTS_COMMAND` 把类型映射到 `mysql`/`psql`/`sqlite3`/`sqlplus`/`beeline`/`impala-shell`/`sqlcmd`(`src/clients.ts:474-484`),Doris 复用 `mysql` 协议,ClickHouse 明确拒绝构造 CLI 模板(`src/clients.ts:650`、`:665`、`:684`)。

这个取舍决定了后面全部机制:能力边界 = 本机客户端版本;注入面 = argv 与 stdin 的分工;首要失败模式 = 二进制缺失。

**连接对象模型**(`src/connections.ts:44-160`,不是 README 转述):

- `DatabaseConnectionInput` 是「所有表面共用的一个连接请求」(`connections.ts:51-66`),`password` 被注释为「仅驻留本进程的临时 Web 密码」,与 `passwordRef` 互斥;
- `PersistedConnectionProfile` 是落盘记录,注释直接写 *Never add secrets here*(`connections.ts:101-116`);`credentialMode` 只有 `none | password | reference` 三态(`connections.ts:48-50`);
- 运行时/持久层是两张表加一张草稿表:`profiles` / `bindings` / `drafts`,zod `.strict()` 拒绝任何 secret 形状字段(`src/storage.ts:61-69`);
- 解析优先级写死为「精确 runtime → 精确 binding → 通配 runtime → 通配 binding」(`connections.ts:340-344`),`'*'` 是给无会话场景的通配默认(`connections.ts:42`)。

**Catalog 的对象模型**(`src/catalog.ts`、`src/catalog-identity.ts`、`src/catalog-storage.ts:46-61`):

- **source** 的身份就是连接 profile id——`catalogSourceId()` 的注释直说「v1 source identity 故意等于稳定 profile id」(`catalog-identity.ts:30-35`)。这是整个包最好复用的一条约定:目录跟着连接档案走,不跟着会话走。
- **asset** 是表/视图/字段,id 由结构化身份(库、schema、relation、name)的稳定 JSON 做 sha256 截 32 位得出(`catalog-identity.ts:52-56`),所以同一张表跨重建仍是同一 id。
- **revision** 是「不可变快照」:指纹不变只更新 `lastSeenAt`,变了才追加 `r000000N`(`catalog.ts:828-857`);覆盖完整的扫描会把本次没观测到的 in-scope 资产标成 `missing`(`catalog.ts:804-825`)。
- **semantic** 是术语/指标/业务含义,同样按版本追加,并有 `inferred → needs_review → verified → retired` 状态机(`catalog.ts:447-500`)。

所以它其实是**两套东西拼在一个包里**:一套是「把 SQL 安全地送到九种客户端」的执行面,一套是「把库表结构做成可 diff、可版本化的目录」。后一套才是它与众不同的部分。

## 怎么接进 DSH

**① manifest 是 Cordis patch,不是字段集合。** `package.json` 的有效声明只有三处:`dsh.bundle.patch → ./cordis.patch.yml`(`package.json:55-57`)、`dsh.engines.dsh: >=0.2.0-rc.1`(`:52-54,DSH 侧由 app-boot 强制`)、`dsh.client`(Web 半,`:58-70`,声明 8 个 `@deepseek-ai/dsh-client-ui-*` 注入)。真正被加载的是 5 行有效 YAML、两条 insert(`cordis.patch.yml:14-18`):

| 行 id | 入口 | 职责 |
|---|---|---|
| `data-agent` | `@yejiming/dsh-data-agent`(`lib/index.js`) | 连接服务、Catalog 服务、安装 preset、把 tool/command 两行注册进行内 preset |
| `data-agent-routes` | `@yejiming/dsh-data-agent/routes` | 只在有 webserver 的组合里挂 `/plugins/data-agent`(`src/routes.ts:107-118`) |

**② preset 不是配置片段,是「装到磁盘再交给注册表」的产物。** `apply()` 先 `installPreset()` 把 `preset/data-agent/` 复制到 `$DSH_HOME/.agent-presets/<presetId>/`(`src/index.ts:256-278`,失败只 warn、不阻断启动);再用 `yaml.load` 读回校验,并把 `tool` 与 `command` 两行**以绝对 `file://` URL** 追加进插件列表(`src/index.ts:378-385`),最后交给 `ctx.agentPresets.register()`(`:386-393`)。注释说明了为什么不写裸包名:`scoped activation never relies on resolving this package again from a different host module root`(`src/index.ts:13-16`)。preset 本体只有两条:persona(`preset/data-agent/agent.cordis.yml:20-50`,一段 26 行的中文人格提示词)与宿主自带的 `@deepseek-ai/dsh-tool-str-replace-editor`(`:55-58`)。

**③ 工具面:7 个工具,全部只在 preset 作用域内可见。** `src/tool.ts:245-424` 注册 4 个(`sql-query` / `sql-write` / `sql-cmd` / `render-analysis`),`src/catalog-tools.ts` 再注册 3 个,合计 **7**:`sql-query`(`tool.ts:255`)、`sql-write`(`:319`)、`sql-cmd`(`:370`)、`render-analysis`(`:423`)、`catalog-search`(`catalog-tools.ts:36`)、`catalog-get`(`:97`)、`metric-get`(`:140`)。repository 里 `ctx.tools.register` 一共 7 次,与 `packaged-runtime.spec.ts:63-72` 冷启动实跑断言的工具清单完全一致。

**④ 工具面收窄靠 DSH 的 `tools.restrict`,不是靠 allowlist。** preset 最后一行 `command` 计算「当前可见但不是我自己的工具名」,一次性 `ctx.tools.restrict({ deny })` 掉(`src/command.ts:130-136`);自己的名单写死在 `DATA_AGENT_TOOL_NAMES` 并额外放行 `render-analysis` 与 `run_code`(`command.ts:46-53`)。本机 DSH 里这条 API 的语义可核:`restrict()` 必须跑在 scoped context 上、未知工具名会抛错、限制只过滤**继承来的**表面(`dsh-tools/lib/index.js:2991-3005`)。测试 `tests/scope-surface.spec.ts:55-100` 把这件事钉成契约:一个 blank agent 从标准 preset 改绑到 data-agent 后,可见工具恰好是 `catalog-get, catalog-search, metric-get, render-analysis, sql-cmd, sql-query, sql-write, str_replace_editor`。

**⑤ 命令面按「真实加载的 Cordis runtime」开关,不按 profile 名。** `/database` 与 `/catalog` 只在检测到 `dsh-tui` 这个 runtime 有活跃 fiber 时才注册(`src/command.ts:88-97`、`:139-147`),并监听 `internal/plugin` 全局事件做增删——因为 `dsh-tui` 可能晚于本插件加载。`/database` 的子命令是 `status|connect|test|disconnect`,明文密码参数被显式拒绝(`command.ts:220-240`);`/catalog` 是 `scan|status|cancel|diff|view`(`src/catalog-command.ts:8-17`)。

**⑥ Web 半是 slot 注入,不是路由页面。** 客户端入口注册三处:`conversation.input.right` 的数据库工作台按钮(`src/client/index.ts:85-94`)、`conversation.hero.agentPreset` 的**影子包装**(把宿主原有的新会话 preset 座位包一层,只在选中 data-agent 时加数据库入口,`:101-158`)、`tool.call.toolview` 里 `key: 'render-analysis'` 的结果卡片(`:162-166`)。

**⑦ 它还带一份「社区清单」,但那份清单不接管任何行为。** `dsh-plugin.json` 声明 `dsh-plugin-0.15`、两个命令、一条 `commands.invoke` 权限(`dsh-plugin.json:4-49`),而 `src/ecosystem.ts:1-25` 的 host facet 只返回 `state: 'degraded'` 的空快照。判断:该文件是生态发现用的声明,DSH 本体不读它——在本机安装包全量 grep `dsh-plugin.json` 命中 0 次,DSH 只读 `dsh.bundle.patch`/`dsh.client`/`dsh.engines`。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `src/connections.ts` | 923 | 表面无关的连接服务:校验、凭据解析、持久化、元数据、交互式查询 | `:351-366` 凭据解析;`:623-638` connect;`:652-658` `resolveForExecution` |
| `src/clients.ts` | 847 | 纯函数:每种方言的 argv/stdin/env 模板 + 元数据 SQL + 输出解析 | `:142-186` 语句分类;`:189-216` 行数改写;`:531-548` 凭据 env |
| `src/query.ts` | 262 | 唯一的执行器:CLI 子进程 / ClickHouse HTTP,超时与输出上限 | `:182-189` 单一 AbortController;`:216-229` spawn |
| `src/sql.ts` | 344 | 词法扫描器(不是解析器):单语句断言、字面量掩码、sqlcmd 元命令拦截 | `:139-151`;`:250-264` |
| `src/structured.ts` | 255 | 每方言的表格输出 → `{columns, rows}` | `:88-117` 分隔符解析;`:231` 入口 |
| `src/catalog.ts` | 1 227 | 扫描生命周期、版本投影、检索、审核、diff、AI 富化编排 | `:226-276` 检索;`:504-599` 执行;`:802-857` 版本化 |
| `src/catalog-adapters.ts` | 666 | 每种方言一条「一 schema 一查」的系统目录 SQL | `:73-85` 注册表;`:226-350` SQL;`:87-99` 能力矩阵 |
| `src/catalog-ai.ts` | 220 | 用当前会话的模型生成业务含义候选(严格 JSON、超 token 二分重试) | `:76-100`;`:102-171` |
| `src/analysis*.ts` | 1 187 | 报告契约(D1-D5)、离线 HTML、图表模型 | `analysis.ts:26-32`;`analysis-html.ts:54` CSP |
| `src/routes.ts` | 470 | `/plugins/data-agent` 的 HTTP 适配层,只做解析与序列化 | `:38`;`:107-118` |
| `src/client/*` | 4 548 | Web 工作台、Catalog 面板、图表、导出 | `index.ts:85/101/162` |

**执行路径(读)**:`sql-query` → `runStructuredReadQuery`(`src/structured-read.ts:93-123`)→ 空串/长度/单语句/只读分类四道闸(`:101-108`)→ `enforceReadRowLimit` 在**方言层**补行数上界(`src/clients.ts:189-216`:普通 `LIMIT n`、SQL Server `TOP (n)`、Oracle `ROWNUM` 包装;无法安全改写的形态直接抛错,如 SQL Server `UNION`/`TOP PERCENT`,见 `:238-263`)→ `runClientQuery` 起子进程,SQL 走 stdin,`stdout/stderr` 各自 `maxBytes` 封顶(`src/query.ts:216-229`)→ 解析时**再**按 `maxRows` 截一次(`src/structured.ts:88-117`)。两道行数限制是刻意的,不是冗余。

**超时**:一个 `AbortController` 同时接管内部 deadline 与调用方 signal(`query.ts:182-189`),deadline 触发时抛「查询超过 N ms 未完成,已终止客户端进程」(`:183-186`),子进程按 5 s 宽限升级终止(`defaults.ts:36`)。默认 30 s(`defaults.ts:18`)。

**写入**:`sql-write` 只接受「分类为 write」的单条语句(`tool.ts:356-366`),每次调用都是独立进程、自动提交;跨调用事务不存在,提示词与错误文案都明说这一点(`src/sql.ts:147-150`)。`readonly` 是连接级覆盖部署级(`tool.ts:362`),默认 **false**(`tool.ts:90`、`index.ts:218`、`routes.ts:56`)。**没有接 DSH 的审批栈**:`src/` 内 `approval` 命中 0 次,`dsh-subprocess` 本体也不含审批逻辑(`node_modules/@deepseek-ai/dsh-subprocess/lib/index.js` 内 `approval` 0 次)。

**凭据怎么走**:持久层只存 `passwordRef`(环境变量形状的引用名,`connections.ts:837-843` 用 `credentialRef()` 校验);每次操作重新 `ctx.credentials.resolve()`(`connections.ts:351-366`),这与 DSH 的凭据契约一致——「per-operation 重新解析,不得跨操作缓存」(`dsh-credentials/lib/types/index.d.ts:100-135`)。进程内临时密码只活在 `runtime` Map 里。真正下发时:MySQL/Doris → `MYSQL_PWD`、Postgres → `PGPASSWORD`、SQL Server → `SQLCMDPASSWORD`(`clients.ts:531-548`);Oracle 与 Hive 把 `connect`/`!connect` 行写进**子进程 stdin 的前缀**(`:557-600`),因为 sqlplus/beeline 的连法不同。这条显式 env 通道是必需的:DSH 的 subprocess 层会把父进程里命中 `/KEY|PASSWORD|SECRET|TOKEN/i` 与全部 `DSH_*` 的变量剥掉,只有 spec 显式给的 env 才在剥离**之后**合并(`dsh-subprocess/lib/index.js:26-53`)。

**Schema 感知**:没有「schema 摘要自动注入模型」这回事——`src/` 内没有任何 system-prompt 注册,模型只能靠工具拉取。两条通道:

1. **即时探查**:`/schemas` `/tables` `/describe` 三个 Web 路由 + `listSchemas/listTables/describe` 服务方法(`connections.ts:684-705`),每种方言一条元数据 SQL(`clients.ts:699-780`),标识符先过白名单校验再按方言加引号(`:350-390`,`METADATA_IDENTIFIER` 只允许 Unicode 字母/组合标记/数字/`_`/`$`)。MySQL/Doris 会逐个库 `SHOW TABLES` 探测权限(`MYSQL_SCHEMA_PROBE_CONCURRENCY=4`),只吞 `ERROR 1044` 并把无权限库隐藏(`connections.ts:416-449`)。
2. **Catalog 扫描**:`richAdapter` 对 7 种方言用**一条 `UNION ALL` 大查询**同时取 relation/column/primary_key/foreign_key/index(`catalog-adapters.ts:226-350`),一 schema 一次往返;hive/impala 能力弱:矩阵直接标 `views: unavailable`、`comments`/`primaryKeys`/`foreignKeys`/`indexes` 全 `unsupported`(`:149-152`),扫描退化为逐表 `DESCRIBE`(`:153-206`);Doris 另注主键/外键/索引 `unsupported`(`:94`)。裁剪靠五个上限:schema 并发 2、表并发 4、单次扫描资产 50 000、单查询捕获 32 MB、单文本字段 4 096 字符(`defaults.ts:39-58`);资产数超限会在进度回调里直接抛错(`catalog.ts:536-546`)——2026-11-17 的 issue #34 正是这条撞上了真实库。

**检索与排序**:不是向量检索,是常驻倒排的朴素版本——把每个资产/语义的 `name+path+comment+dataType`(或公式/别名)拼成一个 `searchText` 建索引(`catalog.ts:964-1000`),查询按词全包含过滤,再按状态固定加权排序:`verified` 语义 0 < `observed` 资产 10 < `needs_review` 20 < `inferred` 30 < `missing` 40(`catalog.ts:1148-1159`)。游标是 base64 的 `{offset, sourceId, query}`,并校验与当前查询一致(`:1170-1186`)——便宜、无状态、不可跨查询复用。

**分析报告**:`render-analysis` 一次调用接 1-6 个只读数据集与 1-8 个视图(`analysis.ts:26-32`),先逐数据集预校验(写语句/多语句/超长任一命中即整单拒绝,零部分执行,`tool.ts:183-194`),再串行执行,任一数据集被截断就报错(`:209-211`);报告 JSON 上限 512 KiB(`:225-228`);HTML 落盘走「临时文件 + 同目录硬链接」(EEXIST 而不是覆盖,`analysis-html.ts:113-138`),页面自带 `default-src 'none'` 的 CSP(`:54`),且报告契约用严格解析器拒绝未知字段——图表库参数、HTML、CSS、URL 都塞不进来(`analysis.ts:1-10`)。

**测试能证明的契约**(9 088 行 / 39 文件,值得单独点出四个):

- `tests/packaged-runtime.spec.ts:11-85`:`npm pack` 出真 tarball、装进临时 profile、用 `dsh 0.2.0-rc.2` 真启动、跑一次真实 SQLite `sql-query`,断言工具清单快照,并断言**数据库文件字节未变**(只读路径真的没写);
- `tests/clients.spec.ts:57-142`、`:223-275`:每种方言 argv 里没有密码、SQL 永不出现在 argv;Oracle 的 `connect` 行只在 stdin;
- `tests/connection-service.spec.ts:380-397`「每次连接与后续每次操作都重新解析凭据」、`:640-653`「stdout/stderr 里的 secret 被 redact」、`:399-450` 1044 权限探测;
- `tests/sql-structured.spec.ts` + `tests/tool.spec.ts:482-497` 多语句、只读拒写、超时终止、截断标记。

## 为什么它突出

**先看星标归属,这里是干净的:单一仓库、没有宿主项目可借。** 仓库 2026-08-11 创建,2026-08-12 首个提交,2026-08-19 采样时 **55 星 / 1746 下载**——采样点落在仓库第 8 天、npm 首版(`0.0.1`,2026-08-14)之后第 5 天。所以 ⚠ 55 与 ⚠ 1746 都是「DSH 时代」的原生数字,不存在 monorepo 子目录那种归属错配。

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-11 | 仓库创建 | GitHub API `created_at` |
| 2026-08-12 | 首个提交(连接 + sqlcmd 工具 + preset + 数据库页) | `git log --reverse` |
| 2026-08-14 | npm `0.0.1` | npm registry `time` |
| **2026-08-19** | **55 星 / 1746 下载采样点**(此刻 npm 到 `0.0.13`) | registry ⚠ |
| 2026-09-29 | 末次提交与末次发版 `0.2.2` | `git log -1` / npm `time.modified` |
| 2026-11-18 | 实时 **226** 星、17 fork、18 open issue(共 31 条 issue/PR) | GitHub API |

也就是说:**开发在 09-29 停了 50 天,星标期间又涨了 4.1 倍。** 这条时间线比星标本身更有信息量——增长发生在发布停止之后,更像 npm/插件站(dshfind 徽章就挂在 README 顶部)带来的持续曝光,而不是功能迭代拉动。判断:按本册口径它是**明星,不是锚**(声量中上、扩散为零),但比「纯明星」多一层真实使用痕迹:17 个 fork、31 条 issue/PR。

**为什么扩散是 0,而且这个 0 需要人工裁一次。** 原始命令会命中两条:

```sh
grep -ril 'data-agent' data/plugins/            # 2:自身 + tomowang__dsh-data-agent.yml
grep -ril 'yejiming'  data/plugins/             # 0:包名/作者名没有任何第三方引用
grep -ril 'omdsh'     data/plugins/ | wc -l     # 50:同一 org 的其他插件,不是对本条的提及
```

第二条命中 `tomowang/dsh-data-agent` 与本条**同名不同源**:registry 自述是另一套机制(「AST 校验的 SQL、每个数据源单独切只读、在设置页里用」),与本条的词法分类器 + preset + Catalog 完全不同;npm 上不存在 `dsh-data-agent` 这个包名(404),本条的包名是 `@yejiming/dsh-data-agent`。**判断:同名独立实现,不计入扩散**(未读其源码,故为判断不是结论)。所以扩散 = **0**。

**为什么「数据接入」在 tools 里是高下载方向。** tools 类 1639 条,其中描述里出现 database/SQL/具体库名的约 **185 条**(`grep -rilE 'database|mysql|postgres|sqlite|sql server|clickhouse|oracle' data/plugins/ | wc -l`,粗筛,含误命中),是最大的单一功能簇之一。1746 ⚠ 在边车 624 条下载记录里排第 79(约 87 分位;中位数 514);55 ⚠ 在 1447 条星标记录里排第 68。我的解释是三条,均为判断:

1. **这是唯一能拿到「公司内部事实」的插件类别。** 模型再强也不知道你库里的数;接上数据库,一次性把「不可得」变成「可得」,收益立刻可验证(一个数字对不对,业务方一眼能判)。
2. **它减技能,不加技能。** 其他工具多要求用户会写 prompt、会配 MCP;这一类直接替代「会写 SQL」,受众是分析师而不是工程师。
3. **装机成本近似为零。** 目标用户的机器上通常已经装了 `mysql`/`psql`/`sqlite3`(这正是它 driverless 设计的红利),`dsh plugin add` 之后填个表单就能问问题。

**它的「协议面」可复用吗?一半可,一半不可。** 可复用的是**数据模型**:`sourceId = profileId`(`catalog-identity.ts:30-35`)、`assetId = sha256(canonical identity)`(`:52-56`)、`semanticId = sha256(sourceId+kind+name)`、`r000000N`/`v000000N` 的版本 id(`:94-100`)、以及状态机 `inferred→needs_review→verified→retired`。这一层是跨方言、跨表面的,任何「schema 目录」都可以照抄。不可复用的是**落点**:Catalog 存在 DSH 的 storage-domain 里,域名 `data_agent_catalog`(`catalog-storage.ts:46-58`),没有导出/导入格式、没有 HTTP 目录 API、也没有给第三方读的 ABI——所以第三方无法与本插件共用同一份目录,只能各自建一份。结论:**它提供的是可仿制的模型,不是可对接的协议**;这也解释了为什么它没有衍生(仿了也接不上,接了也没有第二个消费者)。

## 代价与边界

按发生顺序列失败模式:

1. **客户端二进制缺失(最常见)**。八种类型全部依赖本机 CLI;解析失败时的报错很具体(「已检查:N 个目录;请确认客户端已安装,或配置 `clients.<type>.command`」,`src/client-discovery.ts:365-380`),但它仍然只是**报错**,没有降级实现——工具在,能力不在。回退路径是有界的:先 PATH,再按平台枚举 Homebrew / Postgres.app / Oracle / Program Files 等固定目录,动态目录最多 64 项,不做递归扫描(`client-discovery.ts:230-300`)。显式给了绝对路径则不回退(`:352-361`)。
2. **DSH 版本漂移(当下正在发生)**。`main` 只验证到 `0.2.0-rc.2`(`package.json:171`;README 写「已完成运行验证的版本为 0.2.0-rc.2」),而 preset 的 persona 前缀用了 `{{cwd}}`(`preset/data-agent/agent.cordis.yml:24`)。DSH 的 prompt 变量是严格插值,未知变量在装配期直接抛错(`dsh-system-prompt/lib/index.js:173-176`);本机 0.2.1-rc.5 只注册了 `provider` 与 `model` 两个变量(`dsh-agent-loop/lib/index.js:1591-1592`),`dsh-persona` 内 0 处变量注册——**判断:在 0.2.1-rc.x 上 data-agent preset 会以 `unknown prompt variable "{{cwd}}"` 失败**。这与仓库里 2026-10-17 的 issue #28 与 11-04 的 #32 完全吻合(未读正文,未实机复现)。同一份证据的另一面是提交历史:最近 10 个 commit 里有 4 个是「fix: 适配 DSH X」,`index.ts:281-294` 还维护着一张「允许迁移的旧 preset 文件 SHA-256 白名单」——迁移成本被写进了代码。
3. **连接/认证失败**。`connect` 会先跑一次「列表」查询验证连通性(`connections.ts:408-417`,由 `:627` 调用),所以主机不可达、账号无权、库名错都在连接阶段暴露;保存了档案但凭据没配时,状态返回 `reconnectRequired` 并给出专门文案(`:652-658`、`:543-568`)。
4. **慢查询**。30 s deadline 只杀**客户端进程**(`query.ts:183-186`),不保证杀服务端语句:Postgres 会因连接断开回滚,MySQL/ClickHouse 侧是否立刻停止取决于服务端,本卡未验证。长查询会占住一个子进程,而工具层没有并发上限。
5. **结果过大**。每流 20 000 字符捕获(`defaults.ts:21`)+ 100 行结构化上限(`:24`);`sql-cmd` 只标 `truncated` 并把尾巴给模型(`tool.ts:110-117`),`sql-query` 标 `truncated` 并截断行;`render-analysis` 则**拒绝**被截断的数据集(`tool.ts:209-211`)。Web 工作台走另一套上限:50 000 行 / 32 MB(`defaults.ts:27-30`),超了明确报错而不是静默截断。
6. **Catalog 扫描撞上限**。50 000 资产上限在真实库上会被触发(`catalog.ts:536-546`;issue #34,2026-11-17);MySQL 的 schema 探测还把 `introspectMaxTables`(500)同时当成 schema 数与表数的上限(`connections.ts:430-449`),大实例上目录会不完整而 `coverageComplete` 仍可能为真——待验证。
7. **AI 富化的模型侧失败**。只为「表 + 字段」生成候选,输出被严格 JSON 校验,超 token 时二分重试直到单字段(`catalog-ai.ts:102-127`);会话没有可用模型时直接拒绝扫描(`:81-95`)。

**安全边界,逐条说清:**

- **SQL 注入**:SQL 不在 argv、只在 stdin;标识符走白名单 + 方言引号;`sqlcmd` 的元命令(`:`, `!!`, `GO`, `$(...)`)在执行前被拦(`src/sql.ts:250-264`);SQL Server 的自动限行遇到 `UNION`/`OFFSET`/`TOP PERCENT` 会**拒绝改写**而不是猜(`clients.ts:228-263`)。
- **只读不等于安全**:分类器是「词法读白名单」,代码自己承认 *not a parser*(`clients.ts:135-141`)。据代码判断,**以下形态会被判为 read**:Postgres `EXPLAIN ANALYZE DELETE …`(首 token 是 `explain`)、Postgres/PG 系 `SELECT … INTO new_table`、以及「带写 CTE 的 `WITH`」被 `stripWithBody` 剥到主查询首 token 为 `select` 时(`clients.ts:168-186`);`SELECT nextval(...)`、`lo_import(...)`、`pg_terminate_backend(...)` 这类函数级写同样看不见。这些是**静态推断,未执行验证**。
- **连接串泄漏**:密码不进 argv、不进日志、不进持久层;工具输出与错误消息在跨表面之前统一 redact(`connections.ts:247-264`、`:401-405`;`structured-read.ts:59-73` 再包一层)。但密码会出现在**子进程环境**(`MYSQL_PWD` 等对本机同用户可见)或 Oracle/Hive 的 stdin 前缀里——这是有意的取舍,不是疏漏。
- **跨工作区/多用户**:没有用户概念。连接按 agent session id 索引,profile 全局共享;Web 路由从 query/body 直接取 `sessionId`,**不做归属校验**(`routes.ts:126-190`),Catalog 的 `resolveSource` 只校验 source 与会话连接一致(`catalog.ts:180-197`)。2026-08-30 的 issue #13 标题即「[Security] `/plugins/data-agent` 路由(含 connect 写凭据)缺少来源校验围栏」——与本卡静态读到的行为一致。此外 `sqlite` 相对路径按**宿主进程 cwd** 解析(`connections.ts:287`、`index.ts:454`),子进程 cwd 也是 `process.cwd()`(`query.ts:218`),不是会话工作区;只有分析报告的落盘用了 `exec.agent.session.header.cwd`(`tool.ts:229-233`)。
- **是否等于宿主权限**:是。执行走 `ctx.subprocess.spawn`(`query.ts:216`),不经过 bash 工具的 sandbox/审批栈;数据库侧的有效权限 = 你用哪个账号连 + `readonly` 开关(默认关)。**读写能力事实上等于「你给这个数据库账号的授权」,而审批只看模型选了哪个工具。**

## 可信度与复现

证据等级 ★★★:DSH 接入面、执行面、Catalog 面逐文件读过;Web 工作台与图表两个大文件(`DataAgentWorkbench.tsx` 1 082 行、`CatalogPanel.tsx` 1 120 行)只看了入口与 props,**未逐行读**;`scripts/`、`conformance/` 夹具、`tui-connection-form.ts`、`catalog-tui.ts` 未读。运行期行为一条都没跑(未安装该插件),凡涉及「实际会不会」的句子都已标成判断或待验证。

```sh
# 1) 克隆与提交
git clone --depth 1 https://github.com/omdsh-dev/dsh-data-agent.git .work/mine/cards/data-agent/repo
cd .work/mine/cards/data-agent/repo && git log -1 --format='%H %ad %s'
# → 6a649fe930aeab4247d3e8b936b6bf393aa71e8c Tue Sep 29 19:51:57 2026 +0800 ...
git fetch --unshallow --filter=blob:none && git rev-list --count HEAD   # → 51

# 2) 规模(注意 find 的 -o 要括号,否则只统计到第一种)
find src \( -name '*.ts' -o -name '*.tsx' \) -print0 | xargs -0 cat | wc -l   # → 15201
find src -name '*.css' -print0 | xargs -0 cat | wc -l                          # → 1982
find tests -name '*.spec.*' | wc -l                                            # → 39
grep -c 'ctx.tools.register' src/tool.ts src/catalog-tools.ts                  # → 4 + 3

# 3) 扩散(在 awesome-dsh-plugin 仓库根;目录形式,否则参数过长)
grep -ril 'data-agent' data/plugins/ | wc -l   # → 2(自身 + tomowang 同名条目)
grep -ril 'yejiming'  data/plugins/ | wc -l    # → 0

# 4) 侧车数字与 npm 时间线
python3 -c "import json;d=json.load(open('data/stars.json'));print(d['https://github.com/omdsh-dev/dsh-data-agent'])"
# → {'stars': 55, 'checkedAt': '2026-08-19'}
npm --cache /tmp/npmcache view @yejiming/dsh-data-agent time --json   # 19 个版本,末版 2026-09-29

# 5) DSH 侧对照(本机 0.2.1-rc.5)
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai
grep -n 'unknown prompt variable' $DSH/dsh-system-prompt/lib/index.js      # :174
grep -n 'systemPrompt.variable(' $DSH/dsh-agent-loop/lib/index.js          # :1591-1592 只有 provider/model
grep -n 'restrict(filter)' $DSH/dsh-tools/lib/index.js                     # :2991
grep -n 'SENSITIVE_ENV_PATTERN' $DSH/dsh-subprocess/lib/index.js           # :32
```

## 待验证

1. **`{{cwd}}` 在本机 0.2.1-rc.5 是否真会让 preset 装不上**:静态证据齐(变量白名单只有 provider/model),但没有装插件实测。装一次 `dsh plugin --profile web add @yejiming/dsh-data-agent` 即可定论。
2. **只读模式的实际绕过面**:`EXPLAIN ANALYZE DELETE`、`SELECT … INTO`、写 CTE、`SELECT nextval()` 四条,需在 Postgres/MySQL 沙箱里各跑一次确认。若成立,「只读」应被读成「防误写」而不是「防越权」。
3. **服务端语句是否随客户端进程终止**:30 s deadline 只杀子进程;MySQL/ClickHouse 侧行为未验,决定长查询会不会堆积。
4. **多用户/非 loopback 暴露**:`dsh web` 绑到非回环地址时,`/plugins/data-agent/*` 是否被网关鉴权(路由自身没有),以及 `dsh-authorization` 是否参与——均未验。
5. **ClickHouse 的传输面**:`secure` 只切端口与 scheme(`query.ts:74-80`),证书校验走 Node 默认;ClickHouse Cloud / TLS 组合未实测,preset 提示词里也自承「未经真实部署验证」。
6. **`tomowang/dsh-data-agent` 的谱系**:只读了 registry 自述与其命名的差异,未读其源码或 commit 历史,所以「独立实现」仍是判断。
7. **1746 ⚠ 的时间窗**:边车只给了数值与采样日,未说明是周下载还是累计;采样点时 npm 才发到 `0.0.13`(发布后第 5 天),数字口径直接决定该指标的解读。
