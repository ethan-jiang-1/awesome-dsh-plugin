---
title: "源码复核：toolclub/dsh-agent-team-gui 1.3.0（跨边界样本 02）"
domain: cross-boundary
kind: evidence
positioning: "1.3.0（tag v1.3.0 → 14ea1196；无 npm 包）复核：GUI 只占 4 槽，runtime 有 8 表/工具/RPC/预步派工。"
read_when: "核对 team-gui 的归属、数据源、槽位、退化与「默认不派活」口径。"
status: observed
updated: 2026-11-01
---
# 源码复核：`toolclub/dsh-agent-team-gui` 1.3.0

> 取证时点 2026-11-01（Asia/Shanghai）。只读 npm registry、GitHub API/codeload、release 资产与校验和、本机 DSH `0.2.1-rc.3` 发行包；**未安装、未构建、未运行目标插件，未执行其测试与 workflow，未写任何 profile**。`[DOC]` = 目标仓库文档主张；`[SRC-TARGET]` = 固定 commit 实现；`[SRC-DSH]` = 本机宿主契约；`[TEST]` = 测试源码（只证覆盖意图）；`[CI]` = 同 SHA check-run；`[RUN]` = 本轮只读事实。

## Provenance（npm ↔ tag ↔ commit）

- `[RUN]` **没有 npm 包可对**：`registry.npmjs.org/dsh-agent-team-gui` = `404`，`@toolclub%2Fdsh-agent-team-gui` = `404`；npm 搜索 `dsh-agent-team-gui` 只命中官方的 `@deepseek-ai/dsh-experimental-agent-team*` 系列，**不是本仓库**。故本文的“版本”只有两层：Git tag 与 GitHub release 资产，**不存在 npm 版本/`gitHead`/provenance**。
- `[RUN]` 仓库：默认分支 `main`；286★ / 6 fork（2026-11-01 采样；卡片写 285★/5 fork，属采样日漂移）；MIT；`created_at 2026-08-15T03:40:19Z`，`pushed_at 2026-10-12T19:57:27Z`。
- `[RUN]` `refs/tags/v1.3.0` 是**轻量 tag**，直接指向 commit [`14ea11960b20b1f93c33541ba9df7746ed16d08a`](https://github.com/toolclub/dsh-agent-team-gui/commit/14ea11960b20b1f93c33541ba9df7746ed16d08a)（tree `6a4fd3c`，parent `81ad963` = v1.2.0）；commit 由 GitHub 验签 `verified: true`（web-flow），时间 `2026-09-19T04:57:34Z`，标题 `feat: let the lead choose when to use a team (#78)`。**以下所有链接钉在此 SHA。**
- `[RUN]` `main` 比 `v1.3.0` **超前 3 个 commit**（`0c83f34`、`8d2356e`、`9e952e0`，2026-10-08，只改 README/docs/CI，不改代码）。其中 `8d2356e` 才加入“DSH `0.1.7-rc.2` 被 peer 范围拒绝并回滚”的段落——**该句不在 1.3.0 的 tag 里**，卡片把它当成 1.3.0 的事实引用，需降级为 `[DOC]`（main，2026-10-08）。
- `[RUN]` release `v1.3.0` 资产：`dsh-agent-team-gui-1.3.0.tgz` + `SHA256SUMS`。tgz 1,251,230 B，sha256 `e0981167b3e2577225bc3c491de963104777e20250943ef5b57a733f326e76a2`，与 `SHA256SUMS` **逐字相同**。tar 内 `package.json` 的 `version = 1.3.0`。
- `[SRC-TARGET]` 资产↔tag 内容核对：`CHANGELOG.md`、`README-zh.md`、`docs/on-demand-flow.md`、`examples/full-stack-delivery.recipe.json`、`cordis.patch.yml`、`LICENSE` 与 tag 归档**逐字节相同**；`lib/client.js.map` 的 **15 个 `sourcesContent` 全部与 tag 的 `src/client/*` 逐字节相同**。→ 发布包由该 tag 源码构建，不是另一份快照。
- `[OPEN]` `lib/index.js` **没有 sourcemap**，host 产物无法做同等的源码级比对；只能说“同一构建批次 + 资产哈希 + 同 API version 6”，不能说 host 字节等价。

## DOC（tag 的 README/CHANGELOG，只证作者主张）

- `[DOC]` 兼容矩阵：**1.3.0 → `>=0.1.5-rc.1 <0.1.6-0`**，“v1.3.0 release was verified against DSH `0.1.5-rc.1`”（[`README.md:43-L62`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/README.md#L43-L62)）。
- `[DOC]` **默认口径是分裂的**：“New editor drafts and built-in templates default to **Lead decides when to delegate**. … Saved/imported choices and **legacy missing-field defaults remain unchanged**”（[`README.md:140-L142`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/README.md#L140-L142)）；CHANGELOG 同句补“legacy guaranteed defaults remain intact”（[`CHANGELOG.md:3-L10`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/CHANGELOG.md#L3-L10)）；`docs/on-demand-flow.md:8` 写“新建小队和内置模板默认按需使用；旧记录缺少该字段时仍按原来的 guaranteed 解释”。
- `[DOC]` 持久化与运行中心：“Every execution is written before planning starts”（[`README.md:189`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/README.md#L189-L189)）；coverage 明确 full/partial/unavailable（[`:210-L213`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/README.md#L210-L213)）；无 Jobs 时后台跑在进程内，重启后“reconciles unfinished durable state as **Interrupted**”（[`:224-L228`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/README.md#L224-L228)）。
- `[DOC]` 续跑与失效：“**one continuation per execution chain**”（[`:410-L412`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/README.md#L410-L412)）；“Web profile only; there is no headless Settings UI”（[`:425`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/README.md#L425-L425)）；“Model-tool trigger mode is **best-effort** because DSH exposes no `toolChoice` control. **Guaranteed** normal-send mode is Host-driven and durable-message-idempotent”（[`:437-L438`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/README.md#L437-L438)）。
- `[DOC]` 安装后必须重启已运行的 Web 进程（[`:72`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/README.md#L72-L72)）；release 包免 `prepare` 构建。

## SRC-TARGET（commit `14ea1196`）

### 1. GUI 与 runtime 各拥有什么；有没有 server

- `[SRC-TARGET]` 这是一个**全栈插件**，不是“GUI 套在别家 runtime 上”。Host 侧 `AgentTeamService` 的 `static inject = ['storageDomain','tools','subagents','llm','agents','sessions','systemPrompt']`（[`src/index.ts:35-L36`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/index.ts#L35-L36)）；它自己开存储域（`:53`）、挂 8 张表（`:55-L64`）、注册 2 个模型工具 + 子代理工具 guard（`:72-L74`）、注入 systemPrompt 段（`:76-L80`）、监听 `agent/pre-step` 做派工（`:86-L171`）。
- `[SRC-TARGET]` “GUI”部分只在浏览器侧：`inject = ['slots','connection','locale']`（[`src/client/index.ts:20`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/client/index.ts#L20-L20)），4 个槽位（`:59-L87`）、Settings 表单、输入区控件、Run Center、i18n、样式。**团队语义（DAG、planner、质量门、续跑、用量）全在 host，不在 GUI。**
- `[SRC-TARGET]` **它不启动 server，也不 attach 到外部 server**：RPC 通过 `connection.fetch.register({ path: '/api/agentTeamGui', methods:['POST'], … })` **挂进宿主已有的认证 `/api` 通道**（[`src/rpc.ts:583-L592`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/rpc.ts#L583-L592)），channel `/api`、method `agentTeamGui`、`AGENT_TEAM_RPC_API_VERSION = 6`（[`:14-L17`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/rpc.ts#L14-L17)）。浏览器侧只调 `connection.rpc.call('/api','agentTeamGui',{endpoint,payload})`（[`src/client/index.ts:30-L36`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/client/index.ts#L30-L36)）。全仓无 `http.createServer`/端口/监听。
- `[SRC-TARGET]` **没有“底层 team 插件”依赖**：`peerDependencies` 全是宿主核心包（[`package.json:102-L123`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/package.json#L102-L123)），没有 `dsh-agent-teams`/官方 experimental team 包；`agent-teams` 字符串只作为 Settings 槽位 id 出现（`client/index.ts:61`）。

### 2. “team”数据源与 live-update

- `[SRC-TARGET]` 唯一真相是宿主 storageDomain：`defineDomain({ name:'agent_team_gui', version:0, tables:{…8 表…} })`（[`src/spec.ts:377-L393`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/spec.ts#L377-L393)）；`version: 0` 是刻意的——storage-domain 拒绝版本升级、无迁移 API（`:381-L382`）。**没有** `.agent-teams/` 之类文件：不写目录、不读目录。
- `[SRC-TARGET]` GUI 读的是单个 `snapshot` RPC：返回 agents/squads/models/tools/capabilities/defaults，并对模型目录设 1.5 s 上限、单 provider 失败降为空列表（[`src/rpc.ts:299-L301`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/rpc.ts#L299-L301)、schema [`:170-L207`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/rpc.ts#L170-L207)、读取 [`:219-L283`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/rpc.ts#L219-L283)）。客户端只在首次、每次 mutation 之后、以及 Connection generation 变化时重取（[`src/client/controller.ts:510-L534`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/client/controller.ts#L510-L534)，退避 100 ms→30 s）。
- `[SRC-TARGET]` **live-update 是轮询，不是推送**：Run Center 的 `RunPollStore` 在存在 `isLive` 运行时 **850 ms** 调一次 `run/list`，全部 settled 后 **5 s**，失败后 5 s 重试（[`src/client/run-store.ts:43-L58`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/client/run-store.ts#L43-L58)）；展开详情时再补一次 `run/get`（`:61-L75`）。没有 websocket / SSE / 事件总线。
- `[SRC-TARGET]` 运行记录**在规划前落盘**，因此 UI 能看到 planning 态；进程启动时 `reconcileInterrupted` 把 `planning/queued/running` 改成 `interrupted`、把 pending/running 成员改成 `interrupted`（[`src/tools/run-history.ts:123-L145`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/tools/run-history.ts#L123-L145)）。
- `[SRC-TARGET]` 实时 token 只影响**持久运行记录**，不单独推 UI：`sessionProjections.snapshot(...).values['tokenUsage']` 读四桶，`onChanged` 时串行 `publishUsage`（[`src/tools/infrastructure/official-usage-meter.ts:42-L75`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/tools/infrastructure/official-usage-meter.ts#L42-L75)、[`:110-L114`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/tools/infrastructure/official-usage-meter.ts#L110-L114)）；`totalTokens === 0` 返回 `undefined`（`:74`），不伪造 0。

### 3. 状态持久化、并发与所有权

- `[SRC-TARGET]` 8 张表：`agents`、`squads`、`session_modes`、`next_modes`、`message_claims`、`runs`、`squad_versions`、`project_defaults`（[`src/spec.ts:383-L392`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/spec.ts#L383-L392)）；打开后 `attachTables`（[`src/index.ts:53-L64`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/index.ts#L53-L64)）。运行历史/版本保留默认 `0` = 不自动删（`index.ts:42-L44`）。
- `[SRC-TARGET]` 多表写用**进程内 FIFO** 串行化并补偿回滚：`WriteCoordinator` 自述“Storage-domain tables only promise atomic single-key updates”（[`src/tools/infrastructure/write-coordinator.ts:1-L6`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/tools/infrastructure/write-coordinator.ts#L1-L6)、[`:41-L51`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/tools/infrastructure/write-coordinator.ts#L41-L51)）。**这把锁只在一个 DSH 进程内有效**。
- `[SRC-TARGET]` 所有权/去重的粒度是“一条人类消息一次派工”：`claimGuaranteedMessage` 在 FIFO 内查 `message_claims` 与 `runs.sourceMessageId`，再写 claim（[`src/tools/application/definition-service.ts:655-L665`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/tools/application/definition-service.ts#L655-L665)）；重复消息返回既有结果而不是再起队（`execution-service.ts:230`、`:1367-L1369`）。claim 保留上限 2,000 条 / 90 天（`definition-service.ts:668-L675`）。
- `[SRC-TARGET]` 成员并发 = `min(maxConcurrency ?? 成员数, 成员数)`，成员 schema 上限 32（[`src/tools/application/execution-service.ts:1522-L1530`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/tools/application/execution-service.ts#L1522-L1530)、[`src/rpc.ts:37`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/rpc.ts#L37-L37)）。子代理 `maxDepth: 1` **只在 provider 声明 `depthLimit` 能力时才传**（[`execution-service.ts:620-L636`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/tools/application/execution-service.ts#L620-L636)）。
- `[SRC-TARGET]` 续跑只有 1 次、且仅对 `failed|partial`：`maxContinuations: 1`（[`execution-service.ts:1379`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/tools/application/execution-service.ts#L1379-L1379)）；`continuationAvailability` 明确拒绝 `interrupted`：“Only settled failed or partial runs may continue; cancellation and interruption require user review”（[`:247-L258`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/tools/application/execution-service.ts#L247-L258)）。
- `[OPEN]` 跨进程：FIFO 与 `lastGuaranteedMessage` 都是进程内，claim 的“读表→写表”不是原子 CAS；两个 DSH 进程共享同一 storage 后端时能否重复派工，未测。

### 4. 侧栏/槽位注册

- `[SRC-TARGET]` 4 个 additive 槽位（[`src/client/index.ts:59-L87`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/client/index.ts#L59-L87)）：`settings.section`（Settings → 小队，id `agent-teams`）、`conversation.input.right`（输入区模式控件）、`conversation.input.dock`（运行 dock）、`conversation.view`（Team runs 视图）。
- `[SRC-TARGET]` **没有侧栏（sidebar/side panel）注册**：“Run Center”是会话视图 tab + 输入区 dock，不是独立侧栏。每个槽位都包 `SlotErrorBoundary`（[`src/client/RunCenter.tsx:28`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/client/RunCenter.tsx#L28-L28)、[`:280`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/client/RunCenter.tsx#L280-L280)、[`SettingsPage.tsx:37`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/client/SettingsPage.tsx#L37-L37)、[`ComposerControl.tsx:43`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/client/ComposerControl.tsx#L43-L43)），宿主坏 payload 只炸本槽位并给 Retry。

### 5. 缺件时的退化（底层 team 插件 / 宿主服务）

- `[SRC-TARGET]` 必需宿主服务：`storageDomain`/`tools`/`subagents`/`llm`/`agents`/`sessions`/`systemPrompt`（`index.ts:36`）。缺任一，Cordis 不会构造服务 → 工具、prompt 段、槽位数据全无；**没有“降级成纯前端”这条路**。
- `[SRC-TARGET]` 可选 `jobs`：`backgroundJobsAvailable()` 就是 `ctx.get('jobs') !== undefined`（[`execution-service.ts:109-L111`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/tools/application/execution-service.ts#L109-L111)）；没有它后台跑仍走进程内，只是 `capabilities.backgroundRuns=false`，重启后由 interrupted 收敛（`:1823-L1830` 只 warn）。
- `[SRC-TARGET]` 可选 `sessionProjections`：缺失/异常 → 用量 `undefined`，coverage `none`，不抛错（`official-usage-meter.ts:42-L60`）。
- `[SRC-TARGET]` 可选 `connection`：RPC 用 `ctx.inject(['connection'])` 才注册（`rpc.ts:584`）。缺它时 host 工具/预步仍工作，但浏览器半没有路由，所有调用失败；客户端把 `error` 态渲染出来并可重试（`controller.ts:69-L84`），槽位由 ErrorBoundary 兜底。
- `[SRC-TARGET]` **不存在“底层 team 插件缺席”这一情形**：本插件就是 runtime；与官方/其他 team 插件无 import、无 peer、无 channel 名冲突（唯一同名是 `settings.section` 的 id）。
- `[SRC-TARGET]` 派工失败**不是静默**：预步 catch 后注入一条 user 角色 notice，要求 lead 直接回答并简短披露失败（[`src/index.ts:151-L160`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/index.ts#L151-L160)）；后台启动失败同样注入 notice 且明说“Do not silently run it in foreground”（`:120-L142`）。

## SRC-DSH（本机 `0.2.1-rc.3`，只在相关处引用）

- `[SRC-DSH]` `agent/pre-step` 是真实 waterfall，默认返回 `{ kind:'enter', messages }`（`dsh-agent-loop/lib/index.js:909-L921`）——插件用 `next()` 后改写/追加消息的写法成立。
- `[SRC-DSH]` storage-domain 要求 `version` 为非负整数，且 `compatibleVersions` 必须小于 `version`（`dsh-storage-domain/lib/index.js:63-L64`）——解释了插件为何钉 `version: 0` 并靠“加表”演进。
- `[SRC-DSH]` `connection.fetch.register(route)` 挂在 `connection` 服务的 fetch 网关上（`dsh-client-connection/lib/index.js:727-L734`）——插件没有自建 HTTP server。
- `[SRC-DSH]` **peer 交集为空**：插件声明 `>=0.1.5-rc.1 <0.1.6-0`（`package.json:104-L123`），本机/本册基线 `0.2.1-rc.3` 落在范围外。按作者自己记录的安装器行为，它应与 `0.1.7-rc.2` 一样被拒并回滚。→ 本文所有 `[SRC-TARGET]` 都是**源码阅读**，不是在 0.2.1-rc.3 上跑出来的。

## TEST（只查存在，不执行）

- `[TEST]` `tests/` 下 17 个 spec（host 用 `vitest.host.config.ts`，client 用 `vitest.client.config.ts` + happy-dom/testing-library），含 `v05-host.spec.ts`(1739 行)、`service.spec.ts`(714)、`settings.client.spec.tsx`(768)、`run-center.client.spec.tsx`(460)、`continuation.spec.ts`、`rpc.spec.ts`、`on-demand.spec.ts`、`workflow-issues.spec.ts`、`import-export.spec.ts`，以及 `tests/smoke/{quality-helpers,release-contract}.spec.ts`；共 26 个 `describe(`。
- `[TEST]` 覆盖面只按文件名/引用判断：`interrupted`/`reconnect`/`jobs`/`connection` 在 `v05-host`、`client-controller`、`client-entry`、`rn-center`、`continuation`、`rpc` 等文件里被引用；**未运行，不证通过**。

## CI（同 SHA check-run 才算）

- `[CI]` `.github/workflows/ci.yml`：`quality` 矩阵 Node 22.19.0 / 24.x，依次 `check:whitespace` → `typecheck` → `test` → `build` → `audit:pack`（[`ci.yml:16-L44`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/.github/workflows/ci.yml#L16-L44)）；`hermetic-web-smoke` 安装 **`@deepseek-ai/dsh@0.1.5-rc.1`**，`API_VERSION=6`，`smoke:install` + `smoke:browser`（Playwright chromium）（[`:46-L71`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/.github/workflows/ci.yml#L46-L71)）。
- `[CI]` `.github/workflows/release-preflight.yml`：`push tags v*` 或手动 dispatch 时构建/校验 release candidate；**没有 npm publish job**，与“无 npm 包”一致。
- `[CI]` 同 SHA（`14ea1196`）check-runs 共 10 条，2026-09-19 的 6 条全部 `success`：`Node 22.19.0 quality`、`Node 24.x quality`、`Community plugin doctor`、`Install exact pushed GitHub revision`、`Fresh Web profile and browser smoke`、`release-candidate`；其余 4 条是 9/21–10/5 的 Dependabot。**只证明该 SHA 的 CI 结果，不证明 0.2.x 宿主可装。**
- `[OPEN]` 未读 check-run 日志内容；不知道 smoke 用哪个浏览器/是否覆盖 host 缺席场景。

## RUN

`[RUN]` 本轮只做只读取数：npm registry（2 个 404 + search）、GitHub API（repo/tags/releases/compare/check-runs/tag ref）、codeload tar 归档、release tgz 与 `SHA256SUMS` 的 sha256 校验、本机 DSH 发行包 grep。**未安装、未构建、未运行、未跑测试/CI、未写 profile。**

## 与样本卡偏差表（card-deviation）

| 卡片断言（02 卡） | 本轮证据 | 判定 |
|---|---|---|
| 版本 `1.3.0`；未发 npm；MIT；`dsh.bundle.patch` + `dsh.client platform: web` | tag v1.3.0 → `14ea1196`；npm 404；MIT；`package.json:37-L51` 的 `dsh` 块与 `cordis.patch.yml` 一致 | **成立** |
| 285★ / 5 fork | 286★ / 6 fork（2026-11-01） | 采样漂移，非错误 |
| “小队是用户预存配置，**默认由主 Agent 按需决定**用不用”；takeaway“「默认不派活」写进 systemPrompt” | 新建草稿默认 `model-tool`（[`forms.ts:58`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/client/forms.ts#L58-L58)）；但**运行时缺字段默认 `guaranteed`**（[`index.ts:114`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/index.ts#L114-L114)、[`definition-service.ts:711`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/tools/application/definition-service.ts#L711-L711)、编辑旧队默认 `guaranteed`：[`forms.ts:100`](https://github.com/toolclub/dsh-agent-team-gui/blob/14ea11960b20b1f93c33541ba9df7746ed16d08a/src/client/forms.ts#L100-L100)）；**随包唯一配方 `triggerMode: "guaranteed"`**；README/CHANGELOG 自陈 legacy 仍是 guaranteed | **偏差（最重要）**：默认只在“新建草稿/自称模板”；现有 1.3.0 配方与旧记录是 host 先派。卡片应写“可选 on-demand，运行时缺省 guaranteed”。 |
| “`agent/pre-step` 在 `triggerMode: 'model-tool'` 下读到 squad 就直接 return——不启规划器/成员/run” | 早退条件更宽：squad 缺失、`manual`、非 `guaranteed`、或 claim 失败都 return（`index.ts:113-L119`）；model-tool 路径确实不派工，由 lead 调工具 | 成立，但“直接 return”不等于“保证不派”，见上条 |
| 成员是“真子代理 `ctx.subagents.start(provider,{… maxDepth:1})`” | `maxDepth: 1` **仅当** provider 声明 `depthLimit`（`execution-service.ts:620-L636`） | **部分成立**（条件性） |
| 成本读官方 `tokenUsage` 四桶；0 样本返回 `undefined`；full/partial/none 覆盖度 | `official-usage-meter.ts:42-L75`（`totalTokens===0 → undefined`）；`run-history.ts:30-L71` 的 `runMeteringCoverage` 三值 | **成立** |
| 宿主 `storageDomain` 8 表，有官方持久化后端 | `spec.ts:383-L392` 8 表，`version:0` | **成立** |
| 重启后活动 run / pending·running 成员全 `interrupted`，且 interrupted 排除在可续跑之外 | `run-history.ts:123-L145`；`execution-service.ts:247-L258` 明拒 interrupted | **成立** |
| “派工失败**静默**降级为主 Agent 自答” | 失败会注入可见 notice（`index.ts:120-L160`），并要求披露失败 | **偏差**：是可见降级，不是静默 |
| 无执行级检查点 | 只有逐成员 run 记录；无断点状态；续跑仅 failed/partial 下一步 | **成立** |
| 有界 DAG：节点 ≤32、每节点依赖 ≤32、并发 ≤32、重试 1、质量 2 轮、续跑 1、不限深度 | `rpc.ts:37`（members/assignments ≤32）、`rpc.ts:41-L71`（maxConcurrency ≤32）、`maxContinuations:1`、quality `maxRounds 0..2`；DAG 按 wave 跑、代码无深度上限 | 成立（“≤32”是 schema 上限，不是宿主调度器上限） |
| “DSH `0.1.7-rc.2` 被 v1.3.0 的 peer range 拒绝并回滚（作者已复现）” | 该句只在 **main** 的 README（commit `8d2356e`，2026-10-08），**不在 v1.3.0 tag**；peer 范围 `>=0.1.5-rc.1 <0.1.6-0` 同样排除本册基线 `0.2.1-rc.3` | **需改写**：应写“任何 ≥0.1.6 的宿主都在声明范围外”，并注明该复现记录晚于 tag |
| “只能走 Git/GitHub release 包” | release tgz + `SHA256SUMS` 校验通过；Git 装会跑 `prepare`（`package.json:83` 脚本） | **成立** |
| 暗示这是“GUI 面板”类样本 | 全栈插件：host 拥有 8 表、2 工具、预步派工、planner、续跑、用量；GUI 只有 4 个槽位 + 表单/视图；无自建 server、无侧栏 | **需改写定位**：不是“team 的 GUI”，是“自带 runtime 的 team 插件，带 Web 面” |

## [OPEN]（未验证，不升格）

- `[OPEN]` 在 `0.2.1-rc.3`（本册基线）上安装是否真被 peer 拒绝、或是否存在运行时兼容；**未跑安装器**。
- `[OPEN]` host 产物 `lib/index.js` 与 tag 源码的字节等价性（release 无 host sourcemap）。
- `[OPEN]` 跨进程重复派工：FIFO 与 claim 都在进程内，共享 storage 后端时不保证一次；未构造双进程。
- `[OPEN]` host 半缺失（无 `connection`/无 RPC 路由）时浏览器实际表现，仅由 controller/ErrorBoundary 源码推断。
- `[OPEN]` 850 ms 轮询下的实际延迟、请求量与长会话开销；未测。
- `[OPEN]` `jobs` 服务在 `0.1.5-rc.1` 宿主是否存在、API 是否匹配（peer 标记 optional）；未核对该版本包。
- `[OPEN]` main 上的 0.1.7-rc.2 复现记录（macOS arm64 / Node 26.5.0 / pnpm 12.6.0）未独立复现。
- `[OPEN]` 卡片影响力数字（285★/5 fork、catalog 84★ → ×3.4）未在本轮重新采样 catalog。
