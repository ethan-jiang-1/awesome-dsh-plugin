# toolclub/dsh-agent-team-gui — 小队是 Settings 里的持久数据，不是别人能接过去的协议

> 证据等级:★★★(源码级;`toolclub/dsh-agent-team-gui@9e952e0681d528975444568b70f3c554ac2984be`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 84 为 2026-08-19 历史采样(2026-11-18 实时 288);下载 ⚠ 边车无记录(同日采样缺口)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `toolclub/dsh-agent-team-gui`([registry](../../../data/plugins/toolclub__dsh-agent-team-gui.yml)) |
| 类目 | workflow([census](../../ecosystem/census.py) 703 条 / 全表 11 744 条) |
| 子分类 | `multi-agent` |
| 状态 | ⚠ **需注意**:21 个 peer 钉 `0.1.5.x`,0.2.x 的 `toolFilter/persona` 已改为 `agentPreset`。**需改造后使用**,保留作团队/UI 机制参考。 |
| 自述 | 「持久化多模型小队在 Settings 中配置、从 Composer 选择,支持逐成员模型与工具策略;默认主 Agent 自行完成简单任务,派工按有界 DAG 执行并可有限审核/返工;Run Center 展示重试与官方 usage 的逐成员 token」 |
| 星标 ⚠ | **84**(2026-08-19 采样);2026-11-18 实时 **288**(同日 GitHub API,6 fork / 16 open issues) |
| 下载 ⚠ | 边车无记录(`data/downloads.json` 共 624 条,不含该 URL;2026-08-19 采样缺口,不能读作零下载) |
| 扩散 | **0** 个第三方提及(口径:`grep -ril 'agent-team-gui' data/plugins/` 命中 1,即自身;`grep -ril 'toolclub' data/plugins/` 同样只命中自身) |
| 仓库 commit | `9e952e0`,2026-10-08,`ci: isolate DSH installation to avoid duplicate native types`(main HEAD);发布版 v1.3.0 在 `14ea1196`(2026-09-19),HEAD 只比它多 3 个改 docs/CI 的提交 |
| 包形态 | 单一包的 DSH **Web bundle**:`package.json` 的 `dsh.bundle.patch` + `dsh.client.platform: web`;**未发 npm**(`registry.npmjs.org/dsh-agent-team-gui` → 404),只从 GitHub release tgz 分发 |
| 代码规模 | `src/**/*.ts` + `*.tsx` **9 460 行 / 35 文件**(host 6 261 + client 3 199);测试 **6 275 行 / 17 个 spec**;`cordis.patch.yml` 10 行;仓库 4 512 KB(GitHub `size`,其中 `assets/` 3.5 MB 是演示视频与截图) |

## 它到底是什么

**不是配置包,也不是外部引擎适配层:它自带 runtime 的 team 插件,外加一整套 Web 面。** 判定依据是 host 侧 `AgentTeamService` 自己开存储域、自己挂表、自己起子代理、自己落运行记录(`src/index.ts:35-83`);GUI 是另一个独立入口(`src/client/index.ts:27-87`),只通过一条 RPC 与 host 说话。

**数据模型:一个"小队"是 8 张持久表里的一行,不是一份可执行的协议文档。** `defineDomain({ name: 'agent_team_gui', version: 0, tables: {...} })` 声明了 `agents`、`squads`、`session_modes`、`next_modes`、`message_claims`、`runs`、`squad_versions`、`project_defaults`(`src/spec.ts:378-393`);`version: 0` 是刻意的,注释说 storage-domain 拒绝版本号上调且没有迁移 API(`src/spec.ts:380-382`)。

三张核心表决定能力边界:

- **成员**(`agents`):`name`、`systemPrompt`、`provider`、`model`、`maxTokens`、`toolScope{allow|deny}`、`fallbackProvider/fallbackModel`(`src/spec.ts:31-47`)。**没有 persona 字段**——所谓的"角色人设"就是 `systemPrompt` 这一列 50 000 字符的文本;也没有 temperature、reasoningEffort、preset id。
- **小队**(`squads`):成员 ≤32、`collabNote`、`executionOrder`、`executionMode`、`contextMode`、`leaderAgentId`、`triggerMode`、`failurePolicy`、`maxConcurrency` ≤32、`memberTimeoutMs`、`tokenBudget`、`handoffSummaryMaxChars`、`activationMode`、`memberSelectionMode`、`responseMode`、`planningContext`、`plannerMaxTokens`、`qualityGate{reviewer,repair,maxRounds 0..2,criteria}`(`src/spec.ts:82-107`)。
- **运行**(`runs`):`status` 九态、`phase` 七态、`members[]`(含 `attempts`、`attemptUsage` ≤2、`recovery`、`handoff`、`usageSamples`)、四桶 `usage` + `providerReported`、`plan`、`quality`、`chain`(`src/spec.ts:314-358`)。

**与 DSH 的 agent preset 没有代码关系。** 我在 `src/` 里 `grep -rn 'agentPreset'` 是 0 命中;成员是插件私有的记录,实例化时走的是 0.1.5 那代的 subagent 启动字段:`ctx.subagents.start(provider, { agentOptions: {provider, model, maxTokens, …}, toolFilter, persona })`(`src/tools/application/execution-service.ts:620-636`)。这三个字段在 0.1.5-rc.2 的契约里是一等公民:`SubagentCapabilities` 有 `toolFilter`/`persona`(`@deepseek-ai/dsh-subagent@0.1.5-rc.2` 的 `lib/types/types.d.ts:122-128`),`SubagentStartRequest` 也接受同名可选字段(同文件 `:177-191`)。换句话说,**成员的"模型 + 人设 + 工具集"是插件自己在启动子代理时拼出来的,不是对某个 DSH preset 的引用**;宿主 profile 里定义的 preset 对小队 UI 不可见(它的模型目录来自 `ctx.llm.listProviders()`、工具目录来自 `ctx.tools.schemas()`,`src/rpc.ts:236-259`)。

**核心循环**(全部有源码落点):

1. **模式解析**:一次性选择 `next_modes` > 会话级覆盖 > 项目默认(`project_defaults` 按 `session.header.cwd` 键,`src/tools/application/definition-service.ts:636-648`);一次性选择用 `claimedMessageId` 绑定到具体人类消息(`:609-631`)。
2. **门**:`triggerMode` 缺省按 `guaranteed`,`activationMode: manual` 直接不派(`src/index.ts:113-115`);`guaranteed` 时**在 lead 之前**派工,`model-tool` 时完全交给 lead 决定。
3. **规划**:没有固定 `executionOrder` 时起一个规划子代理——`planningContext: full` 用 `fork` provider(继承历史),其余用 `spawn` 且只喂截断文本(`src/tools/application/execution-service.ts:939-943`);要求结构化输出、禁工具、`maxDepth: 1`(`:1034-1045`)。
4. **执行**:`executionWaves()` 按依赖切波(`src/tools/orchestration.ts:143-157`),每波内按 `min(maxConcurrency ?? 成员数, 成员数)` 分批(`src/tools/application/execution-service.ts:1522-1530`)。
5. **审核/返工**:`qualityGate` 指定一个 reviewer、一个 repair,最多 2 轮;拒绝就只让 repair 改,再回给同一个 reviewer(`:1221-1305`)。
6. **回灌**:结果压成一条 plugin 来源的 user 消息追加给 lead(`src/index.ts:161-170`),正文由 `renderSquadContext` 做二次压缩(`:347`)。

## 怎么接进 DSH

**manifest 只有两处,且不改宿主一行代码。** `package.json:37-52` 声明 `dsh.bundle.patch: ./cordis.patch.yml` 与 `dsh.client{platform: web, inject: [6 个 client 包]}`;`cordis.patch.yml:4-10` 只有一条 `insert`,config 三个默认值(`defaultProvider: spawn`、`defaultExecutionMode: serial`、`defaultContextMode: spawn`)。注释明说 Web profile 已拥有 storage/Connection/browser 模块,所以这层只插自己唯一的 id(`cordis.patch.yml:1-3`)。

**注册点逐项**:

| 位置 | 做什么 | 出处 |
|---|---|---|
| `static inject` | 硬依赖 7 个宿主服务:`storageDomain/tools/subagents/llm/agents/sessions/systemPrompt` | `src/index.ts:36` |
| `storageDomain.open` | 开 8 表,关域挂 `ctx.effect` | `src/index.ts:53-64` |
| `ctx.tools.register` + `guard` | 2 个模型工具 + 1 个执行闸 | `src/index.ts:72-74` |
| `systemPrompt.section` | 段名 `agent-team:squad-mode`,order 118,按会话模式动态生成 | `src/index.ts:76-80` |
| `agent/pre-step` | waterfall 里 `await next()` 后追加/改写消息 | `src/index.ts:86-171` |
| `connection.fetch.register` | 复用宿主 `/api` 认证通道,path `/api/agentTeamGui` | `src/rpc.ts:583-592` |
| 4 个 UI slot | `settings.section`(id `agent-teams`)、`conversation.input.right`、`conversation.input.dock`、`conversation.view` | `src/client/index.ts:59-87` |

**没有自建 server、没有侧栏、没有 websocket。** RPC 是宿主 `connection` 服务上的一条 POST 路由(`src/rpc.ts:586-592`),32 个 endpoint 由同一个 handler 的 `switch` 分发(`:298-553`),并用 `AGENT_TEAM_RPC_API_VERSION = 6` 做浏览器/host 握手(`:19`;客户端校验 `src/client/controller.ts:65`)。Run Center 的新鲜度靠**轮询**:有 live 运行时 850 ms 一次,全部 settled 后 5 s(`src/client/run-store.ts:53`)。

**可选服务全部软降级**:`jobs` 缺席时后台跑仍在进程内,只是 `capabilities.backgroundRuns=false`(`src/tools/application/execution-service.ts:109-111`、`src/rpc.ts:259`);`sessionProjections` 缺席时 token 用量为 `undefined` 而不是 0(`src/tools/infrastructure/official-usage-meter.ts:42-47, 62-75`);`connection` 缺席时 host 侧仍工作、浏览器侧全挂(`src/rpc.ts:584`)。

**依赖面**:21 个 peer,除 `@deepseek-ai/schemastery` 外全是 DSH 包,统一钉 `>=0.1.5-rc.1 <0.1.6-0`(`package.json:102-123`),`@deepseek-ai/dsh-jobs` 标 optional(`:125-129`)。安装走 release tgz,装完必须重启已在跑的 Web 进程(`README.md:64-74`)。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `src/tools/application/execution-service.ts` | 2000 | 派工、DAG、质量环、后台、续跑、取消/重试 | `:1312` 起;`:1522` 并发;`:1654` 后台;`:1914` 取消 |
| `src/tools/application/definition-service.ts` | 1119 | 定义 CRUD、版本、模式、lead 指引 | `:700-757` 指引;`:218-241` 路由校验 |
| `src/tools/orchestration.ts` | 183 | 计划校验、拓扑、波次、handoff 压缩 | `:18-103`;`:143-157` |
| `src/tools/run-history.ts` | 283 | 运行历史、重启收敛、保留策略、洞察聚合 | `:123-142`;`:30-68` |
| `src/spec.ts` | 393 | 8 表 + 全部 zod 契约(v0 宽读、v2 严写) | `:378-393` |
| `src/rpc.ts` | 593 | 32 endpoint、快照、模型/工具目录 | `:236-259` |
| `src/client/SettingsPage.tsx` | 491 | 小队/成员/配方编辑器、版本恢复、工具开关矩阵 | `:345`;`:379` |
| `src/client/RunCenter.tsx` | 304 | 运行卡、依赖阶段、用量、重试/取消/导出、洞察 | `:110`;`:122` |
| `src/client/ComposerControl.tsx` | 302 | 小队选择、durable/一次性的三层开关 | `:181-215`;`:283-301` |
| `src/tools/delegation-policy.ts` | 51 | 子代理内禁再派工的 guard | `:19`;`:38-50` |
| `src/tools/infrastructure/write-coordinator.ts` | 85 | 进程内 FIFO + 补偿写 | `:1-6`;`:41-51` |
| `tests/v05-host.spec.ts` | 1739 | 主机侧主契约(50 个 `it`) | `:196-263` 取消;`:294` 收敛 |

**数据流**:

```
用户消息
 └─ agent/pre-step(waterfall)                         src/index.ts:86
     ├─ 一次性 next_modes 认领                          definition-service.ts:609
     ├─ 有效模式 = 会话覆盖 > 项目默认                    definition-service.ts:636
     ├─ 门:guaranteed 且非 manual                        index.ts:113-115
     ├─ claim 这条人类消息(幂等)                      definition-service.ts:655
     ├─ 先写 run 行,再规划                              execution-service.ts:1426
     ├─ planner 子代理(fork/full 或 spawn) → plan        execution-service.ts:941-1045
     ├─ executionWaves() → 每波按 maxConcurrency 分批     orchestration.ts:143 / execution-service.ts:1522
     │    └─ runMember: start(provider,{agentOptions,persona,toolFilter})  execution-service.ts:620-636
     ├─ 可选 qualityGate:review → repair × ≤2 轮         execution-service.ts:1221
     └─ 结果 + tokenUsage 写回 run 行                    execution-service.ts:1607-1621
 └─ 注入一条 plugin 来源的 user notice 给 lead            index.ts:161-170
```

几处只有读源码才知道的设计:

- **"失败"不一定是失败**:子代理 `stopReason: 'error'` 但交出了非空纯文本时,成员记 `completed`,stopReason 保留并在 UI 上挂 `protocolDeliveryWarning`(`README.md:196-199` 自述;`src/client/RunCenter.tsx:118` 渲染告警)。这条我按文档+UI 代码确认了渲染侧,判定语义在 `src/tools/application/execution-service.ts:542-543`(`settleRun`,整个方法 `:512-562`)。
- **一次派工 = 一条人类消息**:`claimGuaranteedMessage` 同时查 `message_claims` 与 `runs.sourceMessageId`,把重复的工具调用挡在门外(`src/tools/application/definition-service.ts:655-665`);模型工具的 `dispatchFromTool` 还要先定位最新的人类消息 id,否则拒派(`src/tools/application/execution-service.ts:204-227`)。
- **定义在派工时冻结**:run 行里存 `definitionSnapshot`(`src/tools/application/execution-service.ts:1394`),续跑前比对当前定义,变了就要求用户重新审阅(`:325-329`)。这让 8 表里的"配置"和"某次运行"解耦。
- **中断不可续**:重启后 `planning/queued/running` 一律改 `interrupted`、pending/running 成员改 `interrupted`、诊断中的 recovery 改 `failed`(`src/tools/run-history.ts:123-142`);`continuationAvailability` 明确只放行 `failed|partial`(`src/tools/application/execution-service.ts:247-259`),每条链最多 1 次(`:1379`)。
- **重试是显式重放**:整体重试用持久化的 `plan` 原样重放,成员重试只带该成员的原 assignment(`src/tools/application/execution-service.ts:1939-1983`),而不是让模型重新规划。

**测试能证明的契约**(只读未跑):17 个 spec、229 个 `it`、28 个 `describe`。主机侧 `tests/v05-host.spec.ts` 50 个用例覆盖 DAG/波次/取消竞态(`:196-263`)、jobs 与重启收敛(`:264-310`)、重试链接与保留策略(`:310-396`)、用量归因(`:397-528`)、版本/配方/事务回滚(`:397-528`)、一次性认领的并发唯一性(`:530-580`)、以及 `run_code`/作用域别名的 deny 语义(`:1400-1484`)。客户端三个 spec 分别钉配置表单(25 个)、Composer(13 个)、Run Center(17 个,含"Stop 接 run/cancel"`tests/run-center.client.spec.tsx:165`、"整跑/成员重试接新 RPC"`:222`、坏 payload 只在槽位内炸 `:411`)。

## 为什么它突出

**先看星标时间线,84 这个数基本没有解释力。**

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-15 | 仓库创建(03:40Z),同日发 v0.1.0 | GitHub API `created_at` / releases |
| 2026-08-17 | v0.5.0 | releases |
| **2026-08-19** | **⚠ 84 采样点**,同日 02:38Z 发 v1.0.0 | `data/stars.json` / releases |
| 2026-09-19 | v1.3.0,最后一个改代码的提交 `14ea1196` | tag |
| 2026-10-08 | main HEAD `9e952e0`,只改 README/docs/CI | `git diff v1.3.0..HEAD` 7 文件 +44/−10 |
| 2026-11-18 | **288 星**(实时),6 fork,16 open issues | GitHub API |

也就是说:**⚠ 84 是仓库出生第 4 天、v1.0.0 当天的数;此后 3 个月又涨了 204 星(×3.4),而这段时间代码只冻在 v1.3.0。** 增长不是靠迭代:仓库带了 3.5 MB 演示资产(中文导览 mp4(README 称 80 秒)、1 张 gif、10 张截图)和一份成文的推广包(`docs/promotion/launch-kit.zh-CN.md`,含社区短帖与掘金/知乎稿),9 个 release 集中在 35 天内。判断:这是一次**产品化发布**,不是一次协议扩散——星标跟的是"能看懂的界面",不是"能接的接口"。

**零扩散怎么解释。** 三个理由,按解释力排序:

1. **没有可被接走的运行时协议。** 对外只有 2 个模型工具(`dispatch_to_squad`、`continue_squad_run`,`src/tools/dispatch-to-squad.ts:9`、`src/tools/continue-squad-run.ts:10`)和一条 Web RPC;小队本体是 8 张宿主表 + 32 个 endpoint + 4 个 slot。第三方要用它,实际上只能整包安装;要"仿"它,得同时重做 host 状态机(2000 行)与 React 面(3199 行)。
2. **可移植的产物只有文件,没有协议。** `export` 出 `agent-team-gui/definitions` v1/v2、`agent-team-gui/recipe` v1、`agent-team-gui/run` v1(`src/spec.ts:136-174`;`src/tools/application/execution-service.ts:1991-1998`)。配方确实能分享(不含凭证),但它是**单队文档**,没有版本协商、没有服务端校验、也没有第三方实现的动机——拿到配方的人只是把这个插件装满一点。
3. **宿主钉得太窄,跟随者无处落脚。** 21 个 peer 全钉 `>=0.1.5-rc.1 <0.1.6-0`;而 0.2.x 把 `toolFilter`/`persona` 换成了 `agentPreset`(本机 `dsh-subagent@0.2.1-rc.5` 的 `lib/types/types.d.ts:115-121, 130-136`)。想在这个插件上做衍生的人,先要决定跟哪一代宿主。

补充一个测量口径上的坑:`dsh-agent-team` 这个 token 在 registry 里能命中 15 条,但除自身外**没有一条**提到本插件的包名、仓库 URL 或 `agent-team-gui` 字样(`grep -ril 'toolclub' data/plugins/` → 1)。它们是同名前缀的独立条目,不是衍生。所以"0"是真的 0,不是 token 选偏了。

**把"团队"做成 UI/Settings 资产,利弊都很清楚。**

- 利:小队变成**可复用对象**而不是一次性表单——跨会话、跨项目(项目默认表)、可版本化(每次改成员都存成员快照)、可导出配方;用户不需要学任何新协议,选择器就长在输入框旁边。这是"DAG/审核/预算"这些机制能被非工程用户用上的最直接形态。
- 弊:生态杠杆几乎为零。没有共享状态接口、没有事件契约、没有可被别人实现的服务端;连"Run Center"都只是宿主 slot 里的一个 React 视图。它把复杂度从"用户"转移到了"这一个插件",于是受益者只能是安装它的人。

## 代价与边界

- **权限模型是"过滤器 + 执行闸",不是沙箱。** 成员工具策略在子代理启动时以 `toolFilter` 下发(`src/tools/application/execution-service.ts:632`),allow 名单必须能在**父会话作用域**里解析出来,否则直接 `INVALID_DISPATCH`(`:735-745`);deny 只保留全局注册表里可限制的名字,并且 `run_code` 被显式排除在可限制集合外(`:741`),由执行闸 `agentTeamGuiDeniedTools` 兜底(`src/tools/delegation-policy.ts:38-50`)。递归派工工具(含 `subagent`/`workflow`/被改名的同类 schema)在子代理里硬拒(`src/tools/delegation-policy.ts:19-35`)。作者的边界说得很直白:自定义工具和任意外部程序不在 OS 级沙箱内(`README.md:426-427` 自述)。
- **成本是"逐成员独立计量",不是"独立计费"。** 每个成员是一个独立子会话,四桶 token 来自官方 `tokenUsage` 投影(`src/tools/infrastructure/official-usage-meter.ts:27-75`),按成员、按 attempt、按 planner/review/repair 分账(`src/tools/run-history.ts:186-282`);`totalTokens === 0` 返回 `undefined`,不伪造 0(`src/tools/infrastructure/official-usage-meter.ts:74`)。计费仍发生在 provider 账号层,插件只报 token、不报钱。`tokenBudget` 是**软预算**:只在调度前拦后续成员(`src/tools/application/execution-service.ts:1528`),拦不住已经发出的 provider 请求;硬上限只有每成员 `maxTokens`。
- **并发只有队内上限。** 队内 `maxConcurrency ≤32`、成员 ≤32、planner/reviewer/repair 另外产生用量;跨 run 没有全局并发闸,只有"同会话 + 同小队 + 同任务"的去重(`src/tools/application/execution-service.ts:1358-1360`)。多个不同任务可以同时跑,各自持有一条 `AbortController`。
- **默认不清理。** `historyMaxRuns/historyMaxAgeDays/versionMaxPerSquad` 默认全 0 = 永不自动删(`src/index.ts:42-44`),run 行里存的是完整成员输出、任务原文和 handoff;导出是手动 JSON 下载(`src/client/RunCenter.tsx:65`)。长期使用会稳定膨胀。
- **失败模式,按发生顺序**:
  1. **小队配置丢失**——8 表都在宿主 storage domain 里,没有本插件自己的文件或 DB;后端被重置/换掉就是全丢,恢复只能靠之前手工导出的 definitions 或 recipe。删成员有保护:不能删最后一名成员、不能删质量门 owner,其余会级联改写所有引用它的 `squads` 并写新版本(`src/tools/application/definition-service.ts:290-312`)。
  2. **成员模型不可用**——保存时用 `ctx.llm.resolveModelInfo()` 校验主/备路由(`src/tools/application/definition-service.ts:218-241`),但只校验"目录里有";运行期 provider 起不来就是 `start failed`,该成员 `failed`、整跑 `partial`(`src/tools/application/execution-service.ts:696-731`)。`retry-once` 会做一次诊断,只有"可重试的瞬时故障"才原地重试,并可用成员配置的 fallback 路由(`:764-816`)。
  3. **DAG 卡住**——环在计划校验阶段就被拒(`src/tools/orchestration.ts:101`);但 `memberTimeoutMs` 是可选字段,不配就**没有成员级超时**,某一波会一直等下去,只能靠 Run Center 的 Stop 触发 abort(`src/tools/application/execution-service.ts:1914-1921`)。
  4. **运行记录损坏**——run 行是严格 schema(`src/spec.ts:314-358`),而 storage-domain 遇到不合法记录默认整域 `open` 失败(本机 `dsh-storage-domain` 的 `lib/types/spec.d.ts:52-60` 描述 `invalid-record` 行为)。判断:一条坏 run 行可能让整个插件的 `Service.init` 失败,连带工具/slot 全无——这是按宿主契约推的,未构造坏行实测。
  5. **进程重启**——活动 run 一律 `interrupted`,`interrupted` 又不在可续跑集合里(`src/tools/application/execution-service.ts:252`),所以重启 = 该 run 只能人工重试;重试会重放持久化计划,不会重新规划。
  6. **版本错配**——客户端拿不到 `apiVersion: 6` 或 endpoint 不认识时,报"客户端/宿主版本不一致,重启 DSH 并刷新"(`src/client/controller.ts:540-546`),不会静默降级。
  7. **宿主升级**——peer 范围把任何 ≥0.1.6 的宿主排除在外;作者自己记录了 0.1.7-rc.2 被安装器拒绝并回滚(`README.md:76`,自述)。即便绕过安装器,0.2.x 的 start 契约也没有 `toolFilter`/`persona` 的位置。
- **维护成本**:30 个提交、9 个 release,2026-09-19 之后不再改代码,2026-10-08 之后不再提交;30 个提交里 28 个来自同一作者的三个 git 身份(leizihao / lzh19162600626-design / 雷梓豪),另 2 个是 dependabot;21 个 peer 包要跟着 DSH 换代。

## 可信度与复现

**★★★(源码级)**,但只在"读到的文件"范围内:host 侧 `src/index.ts`、`src/spec.ts`、`src/rpc.ts`、`src/tools/application/execution-service.ts`(全文分 6 段读)、`src/tools/application/definition-service.ts`(关键段)、`src/tools/orchestration.ts`(全文)、`src/tools/run-history.ts`(全文)、`src/tools/infrastructure/official-usage-meter.ts`(全文)、`src/tools/infrastructure/write-coordinator.ts`(头 60 行)、`src/tools/delegation-policy.ts`(全文)、两个工具定义、`src/limits.ts`;客户端 `src/client/index.ts`、`src/client/controller.ts`(关键段)、`src/client/run-store.ts`(全文)、`src/client/ComposerControl.tsx`、`src/client/RunCenter.tsx`、`src/client/SettingsPage.tsx`(关键行)、`src/client/forms.ts`(默认值段);测试只读文件头/用例标题/关键行,**未运行**;DSH 侧对照的是本机 `0.2.1-rc.5` 与 npm 上的 `0.1.5-rc.2` 类型声明,**未安装、未跑插件**。文中的 DSH 包内路径按 `<包>/lib/types/*.d.ts` 记(如 `lib/types/types.d.ts`、`lib/types/spec.d.ts`)。

```sh
# 1) 克隆与提交(浅克隆即可,HEAD 就是 main)
git clone --depth 1 https://github.com/toolclub/dsh-agent-team-gui.git .work/mine/cards/agent-team-gui/repo
cd .work/mine/cards/agent-team-gui/repo && git log -1 --format='%H %ad %s'
# → 9e952e0681d528975444568b70f3c554ac2984be 2026-10-08 ci: isolate DSH installation …

# 2) 规模
find src -name '*.ts' -o -name '*.tsx' | xargs wc -l | tail -1      # → 9460
find tests -name '*.spec.ts*' | wc -l                               # → 17
find tests -name '*.ts' -o -name '*.tsx' | xargs wc -l | tail -1    # → 6275

# 3) 零扩散(在 awesome-dsh-plugin 根)
grep -ril 'agent-team-gui' data/plugins/ | wc -l    # → 1(自身)
grep -ril 'toolclub' data/plugins/ | wc -l          # → 1(自身)
grep -ril 'dsh-agent-team' data/plugins/ | wc -l    # → 15,但无一提到本插件(同名前缀)

# 4) 星标与分发
python3 -c "import json;print(json.load(open('data/stars.json'))['https://github.com/toolclub/dsh-agent-team-gui'])"
# → {'stars': 84, 'checkedAt': '2026-08-19'}
curl -sS https://api.github.com/repos/toolclub/dsh-agent-team-gui | grep -E 'stargazers_count|created_at|size'
curl -sS -o /dev/null -w '%{http_code}\n' https://registry.npmjs.org/dsh-agent-team-gui   # → 404

# 5) 关键 seam 对照(0.1.5 有 toolFilter/persona,0.2.x 换成 agentPreset)
curl -sS https://unpkg.com/@deepseek-ai/dsh-subagent@0.1.5-rc.2/lib/types/types.d.ts | sed -n '122,128p;177,191p'
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh
sed -n '115,136p' $DSH/node_modules/@deepseek-ai/dsh-subagent/lib/types/types.d.ts
```

## 待验证

1. **在 0.2.x 上到底会发生什么**:peer 范围排除 ≥0.1.6,所以正常安装会被拒;但"强制装进去后是启动即报错、还是 `toolFilter`/`persona` 被静默忽略",只能实装一次才知道。这是本卡最想验证、也最可能改变结论的一项。
2. **`persona` 落到子代理后还剩什么**:0.1.5 的类型注释说它注册成子作用域的 `deployment:persona-prefix`、**遮蔽**部署级 persona。那么成员的 `systemPrompt` 实际上顶替了部署人设——部署级的 system prompt 段(工具约定、输出格式)是否仍注入、以及它对角色隔离的影响,未在运行时观察。
3. **一条坏 run 行会不会拖垮整个插件**:`invalid-record` 的默认行为按宿主契约是整域拒开,但插件没有用 `backup-and-skip`;需要构造一条 schema 不合法但能落盘的行来实测。
4. **`run_code` 为什么被排除在可限制集合外**:代码只写了 `.filter(name => name !== 'run_code')`(`src/tools/application/execution-service.ts:741`),没有注释。若 `run_code` 能间接调到被 deny 的工具,执行闸是否覆盖嵌套调用,需要一次针对性实验。
5. **跨进程并发**:`WriteCoordinator` 的 FIFO 和 `claimGuaranteedMessage` 的内存快路径都只在单进程内有效;两个 DSH 进程共享同一 storage 后端时能否重复派工,未构造。
6. **850 ms 轮询的真实开销**:长会话里 Run Center 常开时的请求量与首屏延迟,没有测量。
7. **逐成员计费的独立性**:token 归因是源码可证的,但"每个成员走不同 provider 账号时是否真的分开出账",属于 provider 侧行为,本仓库无法证明。
