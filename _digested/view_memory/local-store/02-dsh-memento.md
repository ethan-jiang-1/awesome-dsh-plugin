# dsh-memento — 自建 `ctx.memory` 服务缝:零依赖 SQLite 双层记忆,写路径过审批与审计,快照按会话冻结,协议 v1 以 22 例套件自证

> 证据等级:★★★(源码级;`PerryLink/dsh-memento@26b5bf61505ba56f011cab03fed2b0df22e9d2cf`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 58、下载 910 均为 2026-08-19 历史采样。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `PerryLink/dsh-memento`([registry](../../../data/plugins/PerryLink__dsh-memento.yml)) |
| 类目 | memory([census](../../ecosystem/census.py) 504 条 / 全表 11 744 条) |
| 子分类 | `local-store`(本地存储与检索)——单文件 SQLite,断网可用,数据路径可检查 |
| 自述 | 「有界、分层、审批门控、可审计的跨会话记忆:typed `ctx.memory` seam + 零依赖 SQLite provider + `memory` 工具 + 冻结快照注入,外加 dsh-memory-protocol v1 预演(适配器注册表 + 可分发一致性套件)」——逐项在源码里都有落点,见下 |
| 星标 ⚠ | **58**(2026-08-19 冻结采样;仓库 2026-08-13 创建,即公开后 6 天内累积);2026-11-18 实时 144,4 fork |
| 下载 ⚠ | **910**(2026-08-19 冻结采样;边车无 start/end。按 npm 首发 2026-08-14 判断,这是首几天的量,不是整月口径);npm 2026-08 整月 2 941,2026-10-18~11-16 为 7 731 |
| 扩散 | **0**(口径:`grep -ril memento data/plugins/` 命中 1 条 = 自身;`grep -ril 'dsh-memory-protocol'` 命中 2 条,除自身外是同名无关条目;详见"为什么它突出") |
| 仓库 commit | `26b5bf61505ba56f011cab03fed2b0df22e9d2cf`(2026-11-14,`main`;本卡证据日 2026-11-18)。npm latest `0.5.31` 的 `gitHead` 正是此 commit,但树内 `package.json` 写 `0.5.30` |
| 包形态 | npm `dsh-memento`,Cordis bundle:`dsh.bundle.patch` → 4 行 `cordis.patch.yml`;`dsh.client` Web 面板;`bin` 另有只读 MCP 入口。**0 个运行时 npm 依赖**(无 `dependencies` 键),5 个 peer(`dsh-tools`/`dsh-session`/`dsh-settings`/`cordis`/`schemastery`) |
| 代码规模 | host 面 `index.mjs` 2 221 + `lib/*.mjs` 3 320 + `bin` 18 = **5 559 行**;`client/client.js` 1 226;`types.d.ts` 325;测试 21 个 `test/*.test.mjs` + 一致性套件 3 文件 = **5 081 行 / 209 个 `node:test` 用例**;一致性套件 **22 case**;git 文件 115 |

## 它到底是什么

**一句话:它不只是一个存储型插件,而是一个自带 Service Definition 的插件——它把 `ctx.memory` 这个服务键、写语义、审计格式和一套验收用例一起定义了,然后自己当第一个实现。**

它不是配置包(没有外部引擎可挂),也不是某个外部系统的适配层:SQLite 存储、检索、审批门、审计表、命令与面板都在本仓库实现;`lib/adapters.mjs` 里的三个适配器只服务于 import/export 的数据转换(`lib/adapters.mjs:1-10`)。

三个角色在 `index.mjs:1-12` 的模块头自述里就写明,源码可逐条核对:

- **Service Definition**:`MemoryService extends MemoryProtocolCore`(`index.mjs:356-375`)。公开面是 `budgets()` / `query()` / `add()` / `replace()` / `remove()` / `consolidate()` / `seed()`(`types.d.ts:131-158`)。写方法内部强制走审批回调;读方法不审批。
- **Provider**:`lib/store.mjs` 的单文件 SQLite(`node:sqlite`,`WAL`,`0600`)。Provider 不做预算裁决,也不截断(`lib/store.mjs:1-10` 注释 + 全文无 `slice`/`substring` 写路径)。
- **Consumer**:`memory` 工具(`index.mjs:451-698`)、`memory_recall` 工具(`index.mjs:1882-2010`)、冻结快照段(`index.mjs:1166-1206`);外加三条非模型面:`/memory` 命令(`index.mjs:1516-1527`)、Web 面板三路由(`index.mjs:2143-2203`)、独立进程的只读 MCP server(`bin/mcp-server.mjs:1-18`)。

**数据模型是两层正交维度 + 一个隔离键,不是"一条条笔记"**:

| 维度 | 取值 | 语义 | 证据 |
|---|---|---|---|
| track | `user` / `agent` | 用户事实 vs 环境/项目约定/教训 | `lib/constants.mjs:7` |
| scope | `user-global` / `workspace` | 跨工作区 vs 只对会话 cwd 生效 | `lib/constants.mjs:10`、`lib/workspace.mjs:16-20` |
| agentKey | `''` 或 `agentPreset` 规范化键 | 第三维隔离;`''` = 所有 agent 共享层 | `lib/workspace.mjs:27-31`、`lib/store.mjs:708-714` |

条目本身带 `id`(UUID v4)、`text`、`source`、`tags`(≤16×≤32 字符)、`version`(replace 自增)、`createdAt/updatedAt`、`lastRecalled/recallCount`、`sessionId`(`docs/protocol-v1.md:50-64`;机器校验在 `lib/protocol.mjs:100-160`)。预算按 (track, scope) 四格分别硬算,默认 user 2 000 / agent 4 000 字符每层(`index.mjs:130-137`、`lib/budget.mjs:47-50`)。

**核心循环只有一条,写与读在时间上错开:**

```
写(会话 N):memory 工具 / /memory 命令 / 其它插件的 seed
  → 预算预检 → 审批传输(ctx.approval 或自定义 gate)→ 预算复审
  → SQLite 事务(唯一子串定位 + 落盘)→ audit 行 →(可选)memory/* 会话事件
读(会话 N+1):首个 systemPrompt assemble
  → listEntries → 按 cwd/agentPreset 过滤可见集 → 渲染带用量头的块
  → WeakMap 按 Session 冻结 → 同一文本写 audit(snapshot) → 注入
```

**协议 v1 是这件插件里最"外推"的部分**:写语义被抽进 `lib/protocol.mjs`(`MemoryProtocolCore`,零 DSH 依赖;`docs/protocol-v1.md:178-184` 明说这是"normalization and extension"),`index.mjs` 只注入两件宿主物——审批传输与 `memory/*` 事件派发(`index.mjs:356-375`)。协议文档、JSON Schema、适配器注册表、22 例一致性套件都随 npm 包发布(`package.json:55-56` 的 `files` 含 `test/protocol-conformance`)。它是**自定协议**,不是既有标准:文档头行自标 "community rehearsal — a candidate shape for an official `ctx.memory` seam"(`docs/protocol-v1.md:3`),并另附一份写给 harness 维护者的采纳论证(`docs/upstream-proposal.md:1-13`)。

## 怎么接进 DSH

**① manifest 是两层:一行 bundle patch + 一个 client 面。**

- `package.json:68-82`:`dsh.manifestVersion = 1`,`dsh.bundle.patch = "./cordis.patch.yml"`,`dsh.client = { platform: "web", immediately: true }`,`dsh.capabilities = ["network:egress","tools:register"]`。
- `cordis.patch.yml:1-4` 全文只有 `- insert: [{ id: memento, name: dsh-memento }]`;`id: memento` 同时是设置表单的 namespace(见下)。
- `exports["./client"]`(`package.json:26-29`)是宿主 `dsh.client` 机制要求的浏览器半入口:DSH 的 `dsh-client-modules` 解析 `dsh.client.platform`、要求包导出 `./client`,再以 `__ModuleLoader__.load({id, factory})` 握手(`dsh-client-modules/lib/index.js:64-75, 732-745`;本插件实现见 `client/client.js:19-30`)。
- 安装:`dsh plugin --profile <p> add dsh-memento`(npm)或 `github:PerryLink/dsh-memento`(README.en.md:50-58,命令是宿主行为,本次未实跑)。

**② 四个注册点 + 一个注入声明,全部走公开服务:**

| 注册 | 位置 | 作用 |
|---|---|---|
| `inject = ['tools','systemPrompt','approval']` | `index.mjs:130` | 三者缺一,fiber 不激活(含审批服务——没有 approval 就没有记忆面) |
| `ctx.provide('memory', service)` | `index.mjs:1108` | 主服务键;别处可 `ctx.get('memory')` 或 `inject: ['memory']` |
| `ctx.provide('memoryAdapters'/'memoryEmbedding'/'memoryRetrieval', …)` | `index.mjs:1115, 1124, 1132` | 协议适配器 / 嵌入 / 检索三个附属 seam,均为本插件自定义键 |
| `ctx.on('approval/request', answerer, { prepend: true })` | `index.mjs:1145-1160` | 认领 `toolName === 'memory'` 且 reason 带 `[dsh-memento]` 的审批请求,按 `writePolicy` 裁决 |
| `ctx.tools.register(makeMemoryTool(...))` | `index.mjs:1160` | `memory` 工具(add/replace/remove/consolidate/query) |
| `ctx.tools.register(makeMemoryRecallTool(...))` | `index.mjs:1214` | `memory_recall`:记忆 + `ctx.sessionQuery` 历史两段式召回 |
| `ctx.systemPrompt.section({ name, order, text })` | `index.mjs:1166-1206` | 冻结快照;`order` 默认 -50 |
| `ctx.on('session/event', …)` | `index.mjs:1219-1221` | compaction 摘要 → 提案表(不写记忆、不调模型) |
| `commands.register({ name: 'memory', … })` | `index.mjs:1516-1527` | `/memory list/query/budgets/audit/proposals/adapters/export/import/add/remove/consolidate` |
| `webServer.register` × 3 | `index.mjs:2150-2200` | `/api/memento/entries`、`/audit`、`/proposals`,只读 |
| `ctx.effect(() => () => store.close())` | `index.mjs:1109` | 卸载即关库 |

**③ 设置面走 DSH 的两代契约。** 0.1.7-alpha 起:插件自己的 `Config` 就是设置面,namespace 等于 profile entry id(`SETTINGS_ENTRY_ID = 'memento'`,`index.mjs:260-266`),可编辑字段用 `.volatile()` 标出(`index.mjs:150-250`),编辑由 Loader 提交进实时引用并广播 `loader/volatile-update`(`index.mjs:1058`),热字段即时生效、启动期字段(`dbPath`/`snapshotOrder`)留痕并要求重载(`index.mjs:918-1035`)。旧线(0.1.2-rc.1 / 0.1.5-alpha.1 / 0.1.6-0)回落到 `installSection`(`index.mjs:1060-1094`)。测试直接读 `cordis.patch.yml` 断言两个 `memento` 字面量一致(`test/settings.test.mjs:209-216`)。

**④ 与官方 `ctx.memory` 的关系:没有官方 `ctx.memory`,这是社区提案。** 我把本机 DSH 0.2.1-rc.5 的 `@deepseek-ai/*` 包里所有 `ctx.provide(...)` 服务键枚举了一遍,没有 `memory`(命令见末节)。DSH 的服务机制是 Cordis `ctx.provide(name, value)`(`cordis/lib/index.js:800-826`),服务键在 root isolate 内唯一,**重复提供会直接抛** `service "memory" has been registered at <fiber>`(`:813`)。因此:

- 这个 seam 的"typed"来自本包的声明合并 `declare module '@deepseek-ai/cordis' { interface Context { memory: MemoryService; … } }`(`types.d.ts:264-273`),不是宿主类型。
- 第三方确实能消费:我用真实 Cordis 起了一个 `inject: ['memory']` 的消费者插件,拿到 4 行预算并调用 `ctx.memory.budgets()`(复现见末节)。
- 但它是**独占槽位**:同时启用两个都 `provide('memory')` 的插件,第二个加载失败(我实测 `service "memory" has been registered at <memento>`)。
- 官方现在有 `ctx.storage`/`ctx.storageDomain`(本机 DSH 的服务键列表里有 `storageDomain`),作者在 `docs/upstream-proposal.md:78-160` 里已把采纳路径改写为"挂到 `ctx.storage.domain`",但**代码里没有任何 storage 引用**(`grep -rn storage index.mjs lib/` 为空)——文档领先实现一步。

## 关键实现

### 文件结构

| 文件 | 行数 | 作用 | 关键位置 |
|---|---:|---|---|
| `index.mjs` | 2 221 | 唯一的 host 面:Config/apply、服务、工具、快照、命令、面板、设置 | `:130` inject、`:356` 服务、`:913-1110` 装载、`:1145-1226` 注册、`:1516` 命令、`:1882` recall、`:2143` 路由 |
| `lib/protocol.mjs` | 678 | 协议核心:写流水线、唯一子串定位、校验、denied 审计 | `:24-30` 协议常量、`:319-507` 五个写方法、`:509-535` 审批门、`:592-610` 定位、`:612-623` 预算/裁决门 |
| `lib/store.mjs` | 731 | SQLite Provider:表、迁移、事务、审计、提案 | `:121-127` PRAGMA、`:130-146` 0600、`:154-165` 路径、`:232-250` 打开、`:619-725` 迁移与 DDL |
| `lib/gate.mjs` | 131 | 审批认领、reason 编解码、策略解析 | `:23-29` 认领、`:38-42` reason、`:73-81` 粒度策略、`:113-120` ask/auto/off |
| `lib/snapshot.mjs` | 115 | 可见集过滤 + 冻结块渲染(纯函数) | `:31-35` 可见集、`:90-115` 渲染 |
| `lib/registry.mjs` | 128 | `ctx.memoryAdapters` 注册表 | `:26-127` |
| `lib/adapters.mjs` | 294 | 三个参考适配器:mem0 / Hermes memory.md / CLAUDE.md | `:24, :90, :111, :132` |
| `lib/budget.mjs` | 110 | 四格字符预算 | `:47-50`、`:69-80` |
| `lib/retrieval.mjs` | 204 | 检索 seam:substring 主路径 + 可选 vector | `:33-66`、`:68-110`、`:113-124` |
| `lib/mcp.mjs` | 287 | 只读 stdio MCP server(`memory_search`/`memory_stats`) | `:30-50`、`:149-200` |
| `client/client.js` | 1 226 | Web 面板 + 设置卡片(零构建) | `:19-30` 握手、`:166` 面板探测 |
| `types.d.ts` | 325 | 服务与 `memory/*` 事件词汇的声明合并 | `:264-325` |
| `cordis.patch.yml` | 4 | 唯一 bundle 行 | `:1-4` |

### 写路径:预算 → 审批 → 复审 → 事务 → 审计

五个写方法共享同一条不变量(`lib/protocol.mjs:1-16` 的协议头注释,逐行可核):

1. **预检**(`lib/protocol.mjs:321` / `:350` / `:431` / `:461` / `:475`):`checkBudget(used, limit, addition)`,替换算净变化,整合先减后加。超限抛 `BudgetExceededError`,带 `used/limit/needed`,不写、不截断。
2. **审批**(`lib/protocol.mjs:509-535`):`#ask` 返回 `allowed-once` 之外的任何结果都在抛出前落 `<action>-denied` 审计行(`:516-531`)。
3. **复审**:`replace`/`consolidate` 在审批返回后**重新定位**目标并以此刻用量重算(`:360-363`、`:473-476`),复审与写入之间没有 `await`,注释称"不存在窗口"(`:355-357`)。测试用「审批期间并发写满预算」和「审批期间目标被改写」两条用例钉住(`test/index.test.mjs:357-417`)。
4. **事务**:`store.replaceEntry` / `removeEntry` / `consolidateEntries` / `seedEntries` 全部包在 `BEGIN IMMEDIATE` 里(`lib/store.mjs:606-617`);整合是"逐一定位→全删→插一条新的",任一步零/多命中整体回滚(`lib/store.mjs:333-388`)。
5. **审计**:成功后落一行 `{seq, ts, action, track, scope, entry_id, text, outcome, source, session_id}`(`lib/store.mjs:452-463`),`outcome` 写真实裁决来源,如 `allowed-once (via approval, writePolicy auto)`(`lib/protocol.mjs:537-543`;`test/index.test.mjs:197-209` 断言这一字面量)。

**唯一子串定位**是这套写语义的支点:replace/remove/consolidate 都要求一个大小写不敏感的子串,0 命中 → `ENTRY_NOT_FOUND`,多命中 → `AMBIGUOUS_MATCH` 带候选数与样例(`lib/protocol.mjs:592-610`,`lib/match.mjs:16-42`)。SQL 用 `instr(lower(text), lower(?))` 绕开 `LIKE` 转义(`lib/store.mjs:373-398`);作者的取舍是"不用 FTS5":trigram 无法索引单字 CJK,`unicode61` 只支持前缀,而本插件语料以中文为主(`ARCHITECTURE.md:104-108`)。代价是 `lower()` 只折叠 ASCII,非 ASCII 大小写语言不享受大小写不敏感(判断,未测)。

### Provider:一个文件、四张表、四个 schema 版本

- **路径**:`dbPath` 为空 → `$DSH_HOME/dsh-memento/memory.db`,未导出 `DSH_HOME` 回退 `~/.dsh`;相对路径相对 harness 主目录解析(`lib/store.mjs:154-165`;`test/store.test.mjs:369-380`)。
- **PRAGMA**:`journal_mode=WAL`、`busy_timeout=5000`、`synchronous=NORMAL`(`lib/store.mjs:121`)。
- **权限**:主库与已存在的 `-wal`/`-shm` 边车 chmod `0600`,Windows 跳过(`lib/store.mjs:130-146`;`test/store.test.mjs:25-45` 断言实际文件模式)。
- **表**:`meta` / `entries` / `audit`(`lib/store.mjs:659-687`),`proposals`(`:689-706`),v3 加 `agent_key`/`last_recalled`/`recall_count`(`:708-714`),v4 加 `tags`/`version`(`:716-719`)。`SCHEMA_VERSION = 4`(`lib/constants.mjs:22`)。
- **迁移**:按 `meta.schema_version` 逐级 `BASE → v2 → v3 → v4`;版本高于本插件 → `STORE_UNSUPPORTED_VERSION` 响亮拒绝(`lib/store.mjs:619-657`;`test/store.test.mjs:259-270`)。**注意:迁移梯子不在一个事务里**,每一步是独立 DDL,版本号最后才写;我人为制造"DDL 已跑、版本未写"的中断状态后重开,得到 `STORE_CORRUPT: table proposals already exists`(复现见末节),没有自动回滚或备份。
- **检索**:默认 `SubstringRetriever`(大小写不敏感 + 召回频次/更新时间/id 排序,`lib/retrieval.mjs:33-66`);`Config.retrieval.vector=true` 且探测到 embedding 时换 `VectorRetriever`(内存内暴力余弦,不打包 sqlite-vec,`lib/retrieval.mjs:68-110, 113-124`),缺 embedding 优雅降级回 substring。`memory_recall` 走检索器时先按 `visibleEntries` 过滤,再 `bumpRecall` + `recalled` 审计(`index.mjs:2018-2036`);历史段经 `ctx.sessionQuery` 的 `filterSessions`(cwd + created-at 窗口)与 `filterEvents`(text)下推,片段从 `readSession` 按 seq 抽取,服务缺失时返回 `available:false` 而不是报错(`index.mjs:2055-2100`)。
- **排序**:`queryEntries` 按 `recall_count DESC, updated_at DESC, id`;命中页的条目 `recall_count + 1`、`last_recalled` 更新(`lib/store.mjs:388-397`)。副作用是**任何** query(包括 `/memory list` 与面板浏览)都会抬高召回计数,排序信号并不只来自模型召回(判断,代码如此)。
- **审计保留**:默认 `auditRetentionDays = 0` 不裁剪;>0 时只在**打开库时**删一次旧行(`lib/store.mjs:727-731`,`index.mjs:971-978` 换库时重开),长跑进程不会周期清理。

### 冻结快照:注入时机与失效条件

- **时机**:`ctx.systemPrompt.section({ name: 'dsh-memento:memory', order: live.snapshotOrder, text })`(`index.mjs:1166-1206`)。`text` 在会话第一次 assemble 时同步执行:读 `store.listEntries()` → `visibleEntries()` 按 `session.header.cwd` 的 workspaceKey 与 `agentPreset` 的 agentKey 过滤 → `renderSnapshot()` 渲染带 `used/limit` 头的块(`lib/snapshot.mjs:31-35, 90-115`)。
- **冻结**:渲染结果存进以 **Session 对象为键**的 `WeakMap`(`index.mjs:1165, 1175, 1190`),同一会话后续 assemble 直接返回同一字符串。DSH 的 section provider 是同步调用(`dsh-system-prompt/lib/index.js:388` 不 `await`),SQLite 同步读满足这一点。
- **失效**:新 Session 对象(新会话、fork、进程重启后恢复)→ 重新渲染;`snapshotOrder` 是注册期字段,改它要重载(`index.mjs:1020-1023`);`dbPath` 热切换会重开库,但**不会清空已冻结的旧会话快照**(`index.mjs:971-980` 无 `snapshots.clear()`,判断)。会话内新增/删除条目对当前会话不可见——这是设计目的(system prompt 前缀缓存稳定),代价是模型在长会话里看到的是旧记忆。
- **空也冻结**:首次 assemble 若库为空,`renderSnapshot` 返回 `''`,`WeakMap` 存的是 `''` 而非 `undefined`;本次会话内之后写入的条目不会出现在 system prompt 里(代码判断,`index.mjs:1175-1190`)。
- **可重建**:快照文本同时写 `audit(snapshot)` 行(`index.mjs:1191-1199`),并在宿主收录 `memory/snapshot` 时派发会话事件;`test/index.test.mjs:419-448` 断言"第二次 assemble 与第一次逐字相同"且"审计文本 == 模型所见文本",新会话能看到新条目。

### 审批与审计:谁批、批在哪、拒了怎么办

- **谁批**:DSH 的 `ctx.approval.request`(`dsh-user-approval/lib/index.js:130-150`)。审批服务先看会话级策略:`never` 在 answerer 之前直接 `rejected`(`dsh-user-approval/lib/index.js:175-176`),然后才发 `approval/request` waterfall,无 answerer 则 `unavailable`。本插件以 `prepend` 在链首挂 answerer,只认领 `toolName === 'memory'` 且 reason 以 `[dsh-memento]` 开头的请求,防止误伤同名工具(`lib/gate.mjs:23-29`;`test/index.test.mjs:150-196` 证明服务直写也绕不过)。
- **策略**:`writePolicy` 是 Config,模型不可见、不可改(`index.mjs:174-176` 的字段注释;`lib/gate.mjs:113-120`)。`ask` 委托续链(人类 UI/ACP),`auto` 直接 `allowed-once`,`off` 直接 `rejected`;还支持按 `track/scope` 或 `source:<name>` 的粒度覆盖(`lib/gate.mjs:73-81`;测试 `test/index.test.mjs:619-652`)。
- **批在哪**:turn 内是宿主会话日志的 `approval/asked`(reason 含完整载荷)+ `approval/decided`(`dsh-user-approval/lib/index.js:130-150`);插件自己的 SQLite `audit` 表是第二条链。turn 外(`/memory` 命令)宿主审批服务会拒绝(`request()` 要求 open turn,`:130`),因此命令路径用 `makeCommandGate` 直接走同一 `approval/request` waterfall 并在派发前预检会话 `never`(`index.mjs:1329-1346`),代价是这一路没有 `approval/asked+decided` 审计对,只有插件审计表与 `command/done`(见 `ARCHITECTURE.md:99`)。
- **审什么**:每次写一行(动作/条目 id/全文/裁决来源/来源标注/会话 id);被拒写一行 `<action>-denied`;**读召回**也落 `recalled` 行,**快照**落 `snapshot` 行(全文);设置热更失败/启动期字段变更也落 `settings-*` 行(`index.mjs:992-1035`)。
- **拒绝后**:零写入 + `WriteDeniedError`(code `WRITE_DENIED`,带 `outcome`);工具把它转成 `{ ok: false, error }` 的结构化结果而不是抛异常(`index.mjs:685-691`),模型可据此放弃或改写;基础设施异常才抛(`isError`)。
- **"审批门"的边界(重要)**:门在 **Service 的写方法**内部,模型路径(工具/命令)确实绕不过;但同一进程里持有 `ctx.memory` 的代码有两条旁路:① `service.store` 是公开属性(`lib/protocol.mjs:263`;面板与命令都直接用它),`service.store.insertEntry()` 不经过任何审批与审计——我实测在 `writePolicy: 'off'` 下直插成功;② 写上下文允许传入自定义 `write.gate`(`lib/protocol.mjs:509-514`),我实测返回 `allowed-once` 即可在 `off` 策略下落盘。作者在 CHANGELOG 的 Unreleased 段已把措辞收窄为"no model path 可绕过;in-process holder 仍可触达 store"。判断:这是**进程内信任边界**,不是安全沙箱。

### 协议 v1:自定标准、适配器表、22 例套件

- **身份**:`PROTOCOL_ID = 'dsh-memory-protocol'`,`PROTOCOL_VERSION = 1`,`PROTOCOL_URI = 'dsh-memory-protocol/v1'`(`lib/protocol.mjs:24-30`)。文档自称"community rehearsal",并把"官方应采纳"写成提案(`docs/protocol-v1.md:3`、`docs/upstream-proposal.md:1-13`)。它**不是**外部既有标准:我按名字检索,结果只指向本仓库与一个同名但无关的插件(见下)。
- **机器可读**:`docs/schemas/dsh-memory-protocol-v1.schema.json`(165 行,JSON Schema 2020-12)定义 `entry` / `entryInput` / `budgetRow` / `exportEnvelope` / `auditRow` / `error` 六组数据形状;它**不**描述 provider 方法面(方法契约在 `test/protocol-conformance/README.md:10-39`)。
- **适配器注册表**:`MemoryAdapterRegistry` 提供 `register`(返回 disposer,id 冲突响亮)/`list`/`adapt`/`export`(`lib/registry.mjs:26-127`),注册期校验 id/name/version/formats/函数(`:102-127`)。三个参考适配器是纯数据转换,不做模型抽取(`lib/adapters.mjs:1-10, :24, :90, :111`),随插件生命周期经 `ctx.effect` 注册(`index.mjs:1113-1118`)。命令面:`/memory adapters`、`export --adapter=<id>`、`import --adapter=<id> <path|inline>`(后者转换成条目后走 `seed`,一次审批 + 全量预算预检 + 单事务,`index.mjs:1803-1844`)。
- **一致性套件**:`test/protocol-conformance/` 是**可分发**的:任何 Provider 实现 `makeProvider({dbPath, budgets, gate})` 并返回 `add/replace/remove/consolidate/seed/query/budgets/listEntries/auditList/close` 即可跑同一套用例(`test/protocol-conformance/README.md:10-39`)。22 个 case 分五组:A1-A7 条目模型(含缺 agent 失败封闭)、B1-B7 写语义(version 自增、歧义候选、零命中、双删防护、整批原子、审批载荷 from/to)、C1-C3 预算(超限不落盘、seed 整批拒绝、报表)、D1-D3 审计(放行行、denied 行、recalled 行)、E1-E2 导出信封。runner 每次 case 用全新临时目录,`--provider` 加载第三方工厂,`--filter` 前缀过滤,`--json` 出机器可读报告,失败数决定退出码(`test/protocol-conformance/run.mjs:25-67, 70-108`)。黄金参考就是本仓库的 `store + MemoryProtocolCore + 自动放行 gate`(`test/protocol-conformance/golden.mjs:25-46`),CI 以它全绿自证(`test/protocol-conformance.test.mjs:14-19` 断言 `total === 22 && failed === 0`)。我实跑:**22/22 通过**。

### 测试钉住的契约(读过的部分)

- `test/index.test.mjs`(870 行 / 32 例):服务直写仍被审批门拦截(150)、被拒写落 `add-denied` 且 `outcome` 带策略(150-169)、`enabled:false` 时工具/服务/快照/answerer 全消失且不建库(484)、dispose 后服务消失且库关闭(495)、冻结快照与审计逐字一致(419)、跨 agent/跨工作区写定位不误伤(300)、审批窗口并发(357/385)、`writePolicies` 粒度(619)、`memory/*` 未收录时不 append(742-851)。
- `test/store.test.mjs`(382 行 / 22 例):`0600`(25)、事务回滚(142/196)、`instr` 大小写与 CJK(220)、召回排序(232)、坏库响亮失败(248)、版本过新拒绝(259)、v1→v2 迁移数据完好(272)、路径解析(369)。
- `test/lifecycle.test.mjs`(103 行 / 3 例):**真实 Cordis** + 真实 `SystemPrompt`/`ToolRuntime`,dispose 后 `ctx.memory`、`memoryAdapters`、两个工具一起消失(50-67);面板路由卸载后重挂不撞 duplicate route(73)。
- `test/composition.test.mjs`(148 行 / 5 例):**真实 Loader** 读 `cordis.yml` 挂载,断言 `memoryService === true`、工具列表含 `memory`/`memory_recall`、`queryOk`(57-60);另有非法配置与 default 导出负例。
- `test/v2.test.mjs`(598 行 / 19 例):命令写走 turn 外审批门(121)、被拒落 denied 行(150)、`never` 不派发(166)、`memory_recall` 两段式与会话历史降级(194/244)、export/import 回程与坏信封(255-366)、面板只读与上限钳制(435/470)、`enabled:false` 时 V2 面消失(590)。
- `test/settings.test.mjs`(488 行 / 17 例):`SETTINGS_ENTRY_ID` 必须等于 `cordis.patch.yml` 的行 id(209);热更、启动期字段留痕、非法 live 值留痕、关→开两次无残留(453)。

## 为什么它突出

**先拆星标归属。这个仓库不是 monorepo,也没有宿主项目——星标就是插件本身的。**时间线因此干净:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-13 | 仓库创建 | GitHub API `created_at` |
| 2026-08-14 | npm `0.2.0` 首发 | npm registry `time` |
| 2026-08-15 | `0.3.0`(approve-what-you-see、denied 审计行) | `CHANGELOG.md:336-342` |
| 2026-08-16 | `0.4.0`(协议 v1 + 适配器 + 22 例套件) | `CHANGELOG.md:312-321` |
| **2026-08-19** | **58 星 / 910 下载采样点** | registry ⚠ |
| 2026-08-26 | `0.5.0` | npm registry |
| 2026-11-05 | `0.5.30` | `CHANGELOG.md:3` |
| 2026-11-14 | 本卡 commit | `git log -1` |
| 2026-11-15 | npm `0.5.31`(`gitHead` = 本卡 commit) | npm registry |
| 2026-11-18 | 144 星、4 fork、4 open issue;近月下载 7 731 | GitHub API + npm API(本卡实测) |

也就是说:**58 星是仓库公开后 6 天内的数字,协议 v1 在 3 天内就落地**(0.4.0),不是长期积累的宿主背书。到本卡日期已翻到 144 星、近月 7 731 次下载——**它有真实使用量,但在本 registry 里没有第三方提及**。

**扩散 0,复核如下**(全部在仓库根执行,可复现):

```sh
grep -ril memento data/plugins/ | wc -l                                  # 1(仅自身)
grep -ril memento data/plugins/ | grep -v 'PerryLink__dsh-memento' | wc -l      # 0
grep -ril 'dsh-memory-protocol' data/plugins/ | wc -l                    # 2
grep -ril 'memoryAdapters' data/plugins/ | wc -l                         # 0
grep -ril 'ctx\.memory' data/plugins/ | wc -l                            # 1(仅自身)
```

第二行是"第三方提及数 = 0"。第三条命令的 2 条命中里,除自身外是 `baaai123/dsh-memory-protocol`——它自述"桥接 opencode-memory MCP server、工具调用前强制 memory_weave",条目文本只把 `dsh-memory-protocol` 当作自己的名字,没有出现 `memento`、`ctx.memory`、适配器或套件字样;判为**同名不同物**,不是采纳,也不是衍生。这也解释了为什么"协议名"这个词在 registry 里看似有 2 条,实际采纳为 0:`memoryAdapters`/`ctx.memory` 的提及数说明**没有第三方插件接过这个 seam 或协议**。

**那为什么值得一张卡?**因为它把三件通常分散的东西放进了一个仓库,而且都能执行:

1. **机制**:服务定义 + Provider + 三个 Consumer + 命令 + 面板 + 只读 MCP,5 559 行 host 面代码,零 npm 运行时依赖;写路径的预算/审批/复审/事务/审计五段是显式不变量,不是 README 口号。
2. **协议**:`dsh-memory-protocol/v1` 有规范文档、JSON Schema、适配器注册表、可分发套件;套件不是摆设——`--provider` 能对任何第三方 Provider 跑同一套 22 case,黄金参考就是本仓库自己的实现,不存在"套件过、实现另写"的漂移面。
3. **可执行自证**:209 个 `node:test` 用例(我实跑全绿)+ 22/22 一致性 + 真实 Cordis 生命周期 + 真实 Loader composition;这些测试钉的是服务方法直写仍过审批门、冻结快照可重建、拒绝有证据链、迁移失败响亮这类**契约**,不是覆盖率数字。

按本册"声量 × 扩散"两轴:它是**明星,不是锚**——星标不大但可核(58 ⚠ → 144 实测)、扩散为零。零扩散不写成"无影响力":它的下载量(910 ⚠ → 近月 7 731)与 3 天出协议 v1 的节奏说明有人在用,只是**用的人没有在 registry 里再写一个插件**。两个可解释的原因(判断):① 它是"能力提供方",第三方要提它得先写一个 `inject: ['memory']` 的消费者,而 Registry 里第三方 `ctx.memory` 提及为 0;② 作者自营一个 catalog source(README.en.md:96 的 `perrylink-dsh-catalog` 源)作为分发渠道,这条渠道不产生 registry 条目。协议要成为"标准",还差第三方实现——这正是"待观察"的部分。

## 代价与边界

按发生顺序:

1. **装载期最硬的两个前置**:`inject` 把 `approval` 列为必需(`index.mjs:130`)——profile 里没有审批服务,fiber 永远 PENDING,不是降级而是整个记忆面不存在。库打不开(`STORE_CORRUPT`)、版本比插件新(`STORE_UNSUPPORTED_VERSION`)、配置非法,都在 `apply` 里响亮抛错,插件不挂载(`index.mjs:913-914`;`test/store.test.mjs:248-270`)。这是"fail loud"的设计,但也意味着**没有只读降级模式**。
2. **迁移不是原子的**:v2/v3/v4 每步独立 DDL,`schema_version` 最后写(`lib/store.mjs:619-657`)。我复现的中断状态会让下一次打开直接 `STORE_CORRUPT: table proposals already exists`,没有自动备份/回滚;恢复要手工改库或删库(会丢记忆);仓库里没有看到迁移回滚或备份文档(判断)。
3. **审批失败=写失败**:`ask` 策略下没有 answerer → `unavailable`;会话 `never` → `rejected`;`off` → `rejected`。三者都零写入 + denied 审计行 + 结构化错误,模型只能换动作或放弃。`auto` 策略等于"自动放行但留痕",别把 `auto` 当成审批门(`lib/gate.mjs:113-120`)。
4. **预算是硬墙,不是建议**:超 2 000/4 000 字符即 `BUDGET_EXCEEDED`,必须由模型先 `consolidate`/`remove` 再重试;没有自动压缩、没有截断、没有 LRU。层写满时一次失败的写会多花一轮模型调用(判断,交互成本)。
5. **定位是条件写**:同名/近似文本越多,`AMBIGUOUS_MATCH` 越频繁;模型必须给更长的唯一子串。没有模糊匹配、没有 id 直改(id 只出现在结果里,工具不暴露按 id 定位,`index.mjs:455-485` 的参数表)。CJK 场景 `lower()` 不折叠非 ASCII 大小写(判断,代码如此)。
6. **跨进程只有"最后写者赢"**:`busy_timeout=5000` 之后的行为未测;两个进程共用一个 `$DSH_HOME` 时,README 自己写的是 last-writer-wins(README.en.md:381)。WAL 边车的 `0600` 只在打开时尽力设置(`lib/store.mjs:130-146`)。
7. **审计链有三处缺口**:① 宿主未收录 `memory/*` 时,会话事件被跳过并只告警一次(`index.mjs:319-343`);② `/memory` 命令路径没有 `approval/asked+decided` 审计对,只有插件审计表(ARCHITECTURE.md:99);③ 条目插入与审计插入不在同一事务(`lib/protocol.mjs:328-337`),崩溃落在两者之间会留下"无审计的条目"(判断,未测)。**`audit` 表默认不裁剪**,每次 query/快照都长一行(`index.mjs:1191-1199`、`lib/store.mjs:452-463`),长期使用会持续膨胀,只能靠 `auditRetentionDays` 在打开时清一次。
8. **"审批门"是进程内约定**:`service.store` 公开、`write.gate` 可注入,同进程代码可绕过审批直接写(我在 `off` 策略下两种方式都实测成功)。模型面(工具/命令)不可绕,但任何拿到 `ctx.memory` 的插件都在这道门之内——把它当防越权边界会高估。
9. **快照是"会话级陈旧"**:会话内写入不更新注入;空库首次 assemble 会把空串冻结到会话结束;`dbPath` 热切换不清旧会话快照。设计目的是前缀缓存稳定,代价是长会话看不到新记忆(`index.mjs:1165-1206`;`test/index.test.mjs:419-448`)。
10. **Web 面没有插件侧鉴权**:三个 `/api/memento/*` 路由只读,但会返回**全量**条目、审计尾和 pending 提案(管理视图,不带 agentKey 过滤,`index.mjs:2150-2200`)。插件没有 token/来源检查;是否暴露到 loopback 之外由宿主 web server 与 remote-access 配置决定——本次未验证(待验证)。本机 DSH 的 `dsh-host-webserver` 在注册面上没有鉴权参数(`dsh-host-webserver/lib/index.js:326-340`),但 remote-access/gateway 层是否加鉴权本次未读,所以这条要看上层。
11. **manifest 自相矛盾**:`dsh.capabilities` 声明 `network:egress`(`package.json:77-80`),`dshWorkshop.permissions` 写 `network:none`(`:100-108`),而代码里没有出站 HTTP(`grep` 只命中 `client.js` 对同源 `/api/memento/*` 的 `fetch` 和 `new URL(..., 'http://localhost')`)。读者不该把 `network:egress` 当成"会外发"。
12. **兼容矩阵有两套说法**:`peerDependencies`/`engines.dsh` 覆盖 `0.1.2-rc.1 → 0.2.2-0`(`package.json:135-141, 187-190`),`dshWorkshop.compatibility.dshVersions` 却停在 `0.2.1-rc.2`(`package.json:110-120`);本机装的是 `0.2.1-rc.5`,不在那份列表里。CI 的 `compat.yml` 声称在 scratch profile 里装 tarball + `dsh-base`/`dsh-headless` 跑一次无钥 headless 任务并验证卸载可逆,但**本次没有实跑**。
13. **运行时依赖是 Node 内置的 `node:sqlite`**:零 npm 依赖是真的,但 Node 22.23.1 上仍会打印 `ExperimentalWarning: SQLite is an experimental feature`(我实测);`engines.node` 要求 `^22.19.0 || >=24.9.0`(`package.json:188`)。
14. **发布版本号漂移**:npm `0.5.31` 的 `gitHead` 指向本卡 commit,但树内 `package.json` 是 `0.5.30`,远端也没有 `v0.5.31` tag——发布时改过版本号但没回写源码树(判断;待验证)。

## 可信度与复现

**★★★**:host 面、协议核心、Provider、审批/策略、快照、注册表、适配器、命令/面板关键段、MCP、类型声明,以及 21 个测试文件中的 10 个关键文件逐段读过;`client/client.js` 只读了握手/面板探测段,`scripts/` 与 CI workflow 只读了 `compat.yml`/`release.yml` 的头部。

```sh
# 1) 克隆与提交
git clone --depth 1 --filter=blob:none https://github.com/PerryLink/dsh-memento.git .work/mine/cards/dsh-memento/repo
cd .work/mine/cards/dsh-memento/repo
git log -1 --format='%H %ad %s'
# → 26b5bf61505ba56f011cab03fed2b0df22e9d2cf Sat Nov 14 00:20:45 2026 +0800 fix(ci): ...

# 2) 规模
cat index.mjs lib/*.mjs bin/mcp-server.mjs | wc -l     # → 5559
cat test/*.test.mjs test/protocol-conformance/*.mjs | wc -l  # → 5081
git ls-files | wc -l                                   # → 115

# 3) 两套可执行验收(本机 Node 22.23.1;先装 devDependencies)
npm ci --ignore-scripts --cache ../npm-cache           # → added 57 packages
node test/protocol-conformance/run.mjs                 # → 22/22 cases passed (0 failed)
node --test "test/*.test.mjs"                          # → tests 209 / pass 209 / fail 0

# 4) 扩散(在 awesome-dsh-plugin 根)
grep -ril memento data/plugins/ | wc -l                             # → 1
grep -ril memento data/plugins/ | grep -v 'PerryLink__dsh-memento' | wc -l # → 0
grep -ril 'dsh-memory-protocol' data/plugins/ | wc -l               # → 2(自身 + 同名无关)
grep -ril 'memoryAdapters' data/plugins/ | wc -l                    # → 0
grep -ril 'ctx\.memory' data/plugins/ | wc -l                       # → 1

# 5) 本机 DSH 对照:官方没有 memory 服务键
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh
grep -rhoE "provide\(['\"][a-zA-Z_:]+['\"]" $DSH/node_modules/@deepseek-ai/*/lib/*.js \
  | sed -E "s/provide\(['\"]//; s/['\"]$//" | sort -u | grep -x memory   # → 空
grep -n 'has been registered at' $DSH/node_modules/@deepseek-ai/cordis/lib/index.js   # → :813
grep -n 'HARNESS_IDENTITY\|DEPLOYMENT_PERSONA_PREFIX' \
  $DSH/node_modules/@deepseek-ai/dsh-system-prompt/lib/index.js       # → :11 -1000 / :12 0
grep -n 'KNOWN_SESSION_EVENT_TYPES = new Set' \
  $DSH/node_modules/@deepseek-ai/dsh-session/lib/index.js             # → :79(无 memory/*)
grep -n 'PLUGIN_RECORD_TYPE =' $DSH/node_modules/@deepseek-ai/dsh-session/lib/index.js # → :1248

# 5b) 声量/发布口径(本卡 2026-11-18 实测;数值会变,日期必须跟着报)
curl -s https://api.github.com/repos/PerryLink/dsh-memento \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['created_at'], d['stargazers_count'], d['forks_count'])"
# → 2026-08-13T19:29:14Z 144 4
curl -s https://api.npmjs.org/downloads/point/last-month/dsh-memento              # → 7731
curl -s https://api.npmjs.org/downloads/point/2026-08-01:2026-08-31/dsh-memento   # → 2941
curl -s https://registry.npmjs.org/dsh-memento/0.5.31 \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['gitHead'])"
# → 26b5bf61505ba56f011cab03fed2b0df22e9d2cf

# 6) 迁移中断复现(本卡新增,不在仓库测试里)
node --input-type=module -e "
import { mkdtempSync, rmSync } from 'node:fs'; import { tmpdir } from 'node:os'; import path from 'node:path';
import { openMemoryStore } from './lib/store.mjs';
const dir = mkdtempSync(path.join(tmpdir(),'memento-crash-')); const p = path.join(dir,'memory.db');
const s = openMemoryStore(p); s.close();
const { DatabaseSync } = await import('node:sqlite'); const db = new DatabaseSync(p);
db.prepare(\"UPDATE meta SET value='1' WHERE key='schema_version'\").run(); db.close();
try { const s2 = openMemoryStore(p); console.log('OPENED'); s2.close() } catch (e) { console.log('THREW', e.code, e.message.slice(0,120)) }
rmSync(dir,{recursive:true,force:true})"
# → THREW STORE_CORRUPT ... table proposals already exists

# 7) seam 实测:第三方 inject + 独占槽位 + 进程内旁路
#    (真实 Cordis + 本插件;消费者 inject ['memory'] 拿到 budgets();第二个插件 mount 抛
#     service "memory" has been registered at <memento>;writePolicy:'off' 下
#     service.store.insertEntry() 与 write.gate=()=> 'allowed-once' 都能落盘)
```

**未读/未跑**:`client/client.js` 的面板与设置页实现(仅握手/探测段)、`lib/mcp.mjs` 的完整协议分支(只读了头与工具定义)、`scripts/*`、`.github/workflows/*` 全文、`docs/adapters-guide*`、五语 README 的其余语言版本;未在真实 `dsh` profile 里装载,也未跑 `compat.yml` 的无钥 headless 任务。

## 待验证

1. **对真实宿主版本的端到端装载**:本机 DSH 是 `0.2.1-rc.5`,而测试用的是 `0.2.2-rc.3` devDependencies;`dsh plugin --profile ... add dsh-memento` 后 `dump-config` 是否出现 `memento` 行、首个 assemble 是否真注入快照,未实跑(CI 声称覆盖)。
2. **跨进程并发**:`busy_timeout=5000` 到期后是 `SQLITE_BUSY` 抛错、还是静默丢写?两个 dsh 进程共用一个 `$DSH_HOME` 时的实际行为未测。
3. **Web 面板的鉴权边界**:`/api/memento/*` 在 `dsh web` 的 remote-access / 反向代理配置下是否会暴露到非 loopback;宿主上层是否有路由级鉴权,未验证。
4. **迁移中断的官方恢复路径**:我复现的 `STORE_CORRUPT` 是否需要手工 `ALTER`/删库?仓库没有恢复文档,也没有备份机制;值得确认是否有 issue 讨论。
5. **协议采纳**:`baaai123/dsh-memory-protocol` 只是同名;GitHub 全站是否有第三方 Provider 实现 `makeProvider` 并通过套件,本卡未查(按纪律,扩散只统计 registry)。
6. **`write.gate` 的真实使用面**:除 `/memory` 命令外,是否有其它插件/未来 auto-review 依赖它;它是否会被代际宿主收紧(例如要求 gate 必须来自 approval 服务)。
7. **版本与兼容矩阵**:npm `0.5.31` 与本卡 commit 的 `gitHead` 一致但树内版本是 `0.5.30`,且无 `v0.5.31` tag;`dshWorkshop.compatibility.dshVersions` 停在 `0.2.1-rc.2` 而 `engines` 允许到 `0.2.2` —— 哪个才是发布时的真实支持面。
