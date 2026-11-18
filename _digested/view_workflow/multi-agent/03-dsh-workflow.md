# dsh_workflow — workflow 不是 DAG 而是 QuickJS 里的 JS 程序，「可恢复」靠内容寻址的 effect cache 回放

> 证据等级:★★★(源码级;`omdsh-dev/dsh_workflow@44b83c182aa02d1be8a0803e8446cb495f93cd8f`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 82 为 2026-08-19 历史采样;该 URL 在下载边车里无记录(采样缺口,不是零下载)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `omdsh-dev/dsh_workflow`([registry](../../../data/plugins/omdsh-dev__dsh_workflow.yml)) |
| 类目 | workflow([census](../../ecosystem/census.py) 703 条 / 全表 11 744 条) |
| 子分类 | `multi-agent`(多 agent 编排;本卡回答 workflow 的数据模型、谁执行节点、恢复到底恢复什么) |
| 自述 | 「把 UltraCode 式多 Agent 调度带给 DSH:可生成、可保存、可治理、可观察、可恢复的 Workflow 层」——五个词在源码里各有落点(见下节表),但"workflow"在实现里**不是图**,是一段受限 JS 程序 + 一份 capsule |
| 星标 ⚠ | **82**(2026-08-19 采样;2026-11-18 实时 **159**,1.9 倍)。采样点距仓库创建(2026-08-12T16:39Z)**7 天**、距最后一次 main 提交 **6 天**;单仓库,无宿主项目可借星 |
| 下载 ⚠ | 边车无记录;2026-11-18 查 npm `@dsh-external/workflow` 为 **Not found**(只从 git 装) |
| 扩散 | **0**(口径:`grep -ril 'dsh_workflow' data/plugins/` 命中 **1**,即自身;换包名 token `grep -ril 'dsh-external/workflow' data/plugins/` 命中 **0**)。GitHub 侧另有 **13 fork**(2026-11-18 实时,非 registry 口径) |
| 仓库 commit | `44b83c182aa02d1be8a0803e8446cb495f93cd8f`,2026-08-13 12:20 +0800,`fix: harden workflow handoff preflight`;仓库创建 2026-08-12,API 报 546 KB,`git rev-list --count HEAD` = **5**,5 个提交全部在 2026-08-13 |
| 包形态 | Cordis **bundle**:`package.json:79-83` 的 `dsh.bundle.patch` 指 `cordis.patch.yml`,后者只有一条 `insert`、一个插件行(`cordis.patch.yml:4-6`);`lib/` 构建产物已提交,git 源不需要用户侧编译;npm 未发布 |
| 代码规模 | `src/` **5 435 行 / 12 个 `.ts`**(engine 1 453、index 698、scoped-review 533、runtime 497、types 477、author 395、catalog 337、service 328、capsule 281、store 209、builtins 114、source-policy 113);`lib/` 另有 4 997 行已提交构建;测试 **2 609 行 / 11 个 spec / 113 个 `it(` + 10 张 `it.each` 表** |

## 它到底是什么

**是插件,不是配置包,也不是外部引擎的适配层。** DSH 侧零 patch,但插件体内有完整的五件套:自己的 Cordis service(`ctx.dynamicWorkflows`,service.ts:74)、自己的 run store、自己的 catalog、自己的 author 流水线、自己的沙箱。它对宿主只借五样东西:`ctx.subagents`、Session 事件流,以及 `approval`/`jobs`/`userQuestions` 三条互动缝(index.ts:36, 685-687)。

**数据模型:一份 capsule,没有 node,没有 edge。**

- 单位是 `dsh.workflow` v1 capsule:`format`/`version`/`workflowApiVersion`/`minDshVersion` + `manifest` + `source` + `intent`/`inputs`/`requires`/`provenance`(types.ts:84-95;完整样例 examples/review.workflow.json)。
- `manifest` 只有 name、description、phases、readOnly、plannedAgents、maxAgents、maxConcurrency、tokenBudget、mayUseWorktree、patterns、inputSchema 这些**契约字段**,没有节点表(types.ts:38-50;校验 capsule.ts:118-156,未知字段直接拒绝)。
- `source` 是 `async function run(wf, args)` 的 JavaScript 源码(capsule.ts:226;必须匹配这个签名,source-policy.ts:81-83)。**节点是运行时调出来的**:每次 `wf.runAgent`/`wf.spawnAgent` 生成 `task-<n>`(engine.ts:1014),对应一个真实 DSH 子会话(engine.ts:1136 记 `task.childId = childRun.id`)。
- **依赖不是声明的,是 JS 控制流**。`await` 串行、`wf.parallel`/`wf.pipeline` 并发(engine.ts:929-952);`phase` 只进观察投影,不参与调度(engine.ts:864-887, 734-750)。所以没有条件节点、没有循环节点类型、没有可序列化的边。
- **所谓 graph 是事件日志的投影**。`WorkflowProcessItem` 四种 kind:`phase`/`agent`/`step`/`artifact`(types.ts:291-304),由 `events.jsonl` 折叠而成(engine.ts:732-805);18 种事件类型在 types.ts:267-278。run 6 态、task 5 态(types.ts:22-23)。
- **持久化位置**:每个 run 一个目录 `.dsh/workflow-runs/<run-id>/`(默认,index.ts:78),内含 `run.json`(每次 emit 重写)、`events.jsonl`(append-only)、`workflow.workflow.json` + `script.js` + `manifest.json`(仅生成型)、`results/`(effect cache)、`artifacts/`(store.ts:87-132)。catalog 是 `.dsh/workflows/<name>.workflow.json` 与 `$DSH_HOME/workflows`(index.ts:76-77;service.ts:323-327)。不是 SQLite,不是会话事件,是**工作区文件**。
- **没有执行检查点**。没有程序计数器,没有 QuickJS 堆快照,没有"从第 N 步继续"的路径。可恢复的只有两样:不可变 capsule 快照(store.ts:110-113)+ 每个 task 的结果缓存。判断:这是本插件对"恢复"的定义——重跑 + 命中缓存,不是续执行。

**五个词各对应哪段代码:**

| 词 | 落点 | 机制 |
|---|---|---|
| 生成 | author.ts:334-395 | 先 `fast` 档只读 scout,再 `deep` 档结构化 author(带 `AUTHOR_SCHEMA`),失败最多 3 次带错误回炉(:356-393),最后在 QuickJS 里用**惰性假 agent** 空跑一遍冒烟(:320-332, smokeApi 在 :90-289) |
| 保存 / 版本化 | catalog.ts:281-318 | 同目录临时文件 + `link()` 独占发布;替换时先把旧文件 rename 进 `.archive/` 再换入,失败回滚(:287-313);capsule 带 `provenance.createdAt/dshVersion/pluginVersion/fromRunId/revisionOf`(types.ts:74-82),run 侧同时存不可变快照 |
| 治理 | source-policy.ts:13-26, 79-94;runtime.ts;engine.ts:405-486, 709-714 | 静态禁词(import/require/process/fs/shell/fetch/timers/eval/`__dsh*`)、QuickJS 独立堆、确定性守卫、只读工具交集、能力 fail-closed、token 预留 |
| 观察 | engine.ts:716-805;types.ts:267-278 | append-only 事件 + 每事件重写 run.json + process/outcome 投影 + 订阅接口(:587-590);另写宿主原生 `tool-workflow/*` 事件给 DSH 自己的 UI |
| 恢复 | engine.ts:1030-1041;store.ts:116-131 | `resumeFromRunId` 只做一件事:按内容寻址 key 从上一 run 的 `results/` 回放**已完成且无警告**的 task 结果 |

## 怎么接进 DSH

**manifest 是 patch,不是字段集合。** `package.json:79-83` 只声明 `dsh.bundle.patch → ./cordis.patch.yml`;整个 patch 是 6 行 YAML(2 行注释 + 空行 + 3 行 insert),插件名 `@dsh-external/workflow`(cordis.patch.yml:4-6)。`package.json:8-31` 的 exports 暴露 `.`/`capsule`/`catalog`/`runtime`/`store` 五个入口,第三方可以直接 import 它的 store/capsule 实现。

**注册面(全部在 `installSurfaces`,index.ts:581-681):**

| 面 | 数量 | 位置 |
|---|---|---|
| 工具 | **3**:`workflow_list`(0 参)、`run_workflow`(8 参:name/request/source/manifest/args/wait/background/save_scope)、`workflow_manage`(14 个 action) | index.ts:585-666;名字可配(:79-81) |
| 斜杠命令 | **1**:`/workflow`,约 20 个子命令(help/list/create/review/runs/show/pause/resume/stop/rerun/resume-run/save/rename-run/rename-saved/revise/delete-run/delete-saved/delete/rename/prune) | index.ts:439-457, 674-680 |
| system prompt 段 | **1** 段,`order: 116`,教模型何时用 `run_workflow`、命令交接时用 source+manifest 而非 request 模式 | index.ts:668-673 |
| Cordis service | `dynamicWorkflows`,先 `ctx.plugin` 发布再 `ctx.inject(['dynamicWorkflows'])` 装面 | index.ts:688-695;service.ts:23-27 |
| UI slot | **0**。不注册任何前端 slot,改为往调用方 Session 追加宿主原生的 `tool-workflow/` 四类事件(run-start、agent-start、agent-end、run-end),让 DSH 自带的 workflow-run 面板渲染 | engine.ts:303-316, 642, 1139-1142, 1344, 703 |

**依赖与降级**:`inject = ['subagents', 'tools']` 是硬依赖(index.ts:36);`approval`/`jobs`/`userQuestions` 用 `ctx.get` 软取(index.ts:685-687)。缺 approval 时受审批的 run 直接抛(engine.ts:646);缺 jobs 时后台 run 仍存在,只是没有宿主 job 控制(service.ts:244-263);缺 userQuestions 时 `/workflow` 的确认路径抛(service.ts:236)。**没有任何宿主文件被改**:插件只写工作区与 `$DSH_HOME` 下的自有目录。

**安装**:README:60 写 `dsh plugin --profile web add "github:dsh-external/dsh_workflow#main"`。注意旧名 `dsh-external` 已 301 到 `omdsh-dev`(实测),`package.json:59-66` 的 repository/homepage/bugs 仍是旧名。

**两条审批通道,别混**:模型工具走 DSH 当前 turn 的 `ctx.approval.request({toolName:'run_workflow'})`,只认 `allowed-once`(engine.ts:645-653);斜杠命令走 `ctx.userQuestions.ask` 的 Run/Cancel 卡片(service.ts:235-242);`approvalMode` 三档 `never|generated-and-local|always`,默认第二档,只对生成型与 trusted-local 强制(engine.ts:709-714)。

**一个值得单说的治理机制:命令交接的一次性授权。** `/workflow create` 或未知名字的自然语言请求不自己跑,而是把 authoring contract 作为 plugin 消息 `inject` 给当前 agent,再把原始 query 作为**真 user 消息** `steer` 进去,并把授权绑在那条 `user/message` 的 id 上(index.ts:199-225)。之后 `run_workflow` 只有在倒扫事件时**先撞到这条 user 消息、且其间没有 turn 边界**才认账(index.ts:227-242),且只给第一个通过冒烟校验的 inline workflow 用掉(index.ts:611-628)。这解决了"生成 workflow 要不要再批一次"的问题,代价是整套逻辑与 Session 事件形状强耦合。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `src/index.ts` | 698 | Cordis 入口:Config、3 工具、命令、prompt、交接授权 | :38-110, :199-248, :581-696 |
| `src/service.ts` | 328 | `ctx.dynamicWorkflows`;按 cwd 缓存 engine/store;三个 adapter;后台 job | :65-101, :279-312 |
| `src/engine.ts` | 1453 | 预检、审批、run 状态、双层信号量、task 驱动、验证、两种投影 | :499-517, :1001-1391 |
| `src/runtime.ts` | 497 | QuickJS 堆 + JSON-only 桥 + 确定性守卫 + 超时收敛 | :137-258, :260-497 |
| `src/source-policy.ts` | 113 | 禁词策略与质量 lint(无界循环等) | :13-26, :101-112 |
| `src/capsule.ts` | 281 | capsule/manifest/inputSchema 严格校验 | :118-156, :220-280 |
| `src/catalog.ts` | 337 | 发现优先级、trusted-local 导入、原子保存/归档 | :113-130, :158-191, :281-318 |
| `src/author.ts` | 395 | scout→author→3 次修复→QuickJS 冒烟 | :320-395 |
| `src/store.ts` | 209 | run 目录、事件、cache、身份解析、prune | :87-132, :151-189 |
| `src/builtins.ts` | 114 | 2 个内建 + 6 个 pattern | :59-114 |
| `src/scoped-review.ts` | 533 | 内容寻址 review packet + scoped-review workflow | :258-300, :525 |
| `src/types.ts` | 477 | 全部数据模型与扩展点接口 | :84-95, :241-260, :410-451 |

**数据流(一条主链,四个观察点):**

1. 三个入口(`/workflow`、3 个工具、命名 workflow)→ `DynamicWorkflowService.startNamed/startInline/rerun`(service.ts:120-139, 188-210)。
2. `engine.start` → **preflight**:检查 `requires` 的 git/worktree/tools/mcp/skills/modelTiers/userInteraction 是否满足,算出审批摘要,任一不满足直接抛,不降级(engine.ts:499-517, 522)。
3. 审批 → `runRestrictedWorkflowScript` 在 QuickJS 里跑 `run(wf, args)`(engine.ts:645-665)。guest 侧 `wf.*` 每次调用都编码成 JSON,经 `__dshCall`/`__dshSync` 同步或异步回到宿主(runtime.ts:137-258, 297-361)。
4. 宿主侧 `runAgent` → `startTask` 先做准入(agent 上限、readOnly 冲突、能力、token 预算,engine.ts:467-486),再排队进信号量,`waitAdmission` 过暂停闸,最后 `ctx.subagents.start(provider, request)`(engine.ts:1066-1132)。**节点执行者就是 DSH 原生 subagent**,不是独立会话、不是外部进程。
5. child 结束 → structured output 校验(必要时一次 15s、无工具的格式修复,engine.ts:1167-1215)→ verification(非只读任务默认要求 mutation 证据,最多 3 次 followup 修复,:1271-1334)→ 只有 `completed` 且无 warning 才写 cache(:1342)→ 发 `agent-completed` 与原生 `tool-workflow/agent-end`(:1343-1344)。
6. run 终态 → cost/outcome 投影(:688-707, 807-846)→ `run.json` → 原生 `tool-workflow/run-end`(:703)。

**并发:两层信号量,一个准入闸。** 每 run 一把 `WorkflowSemaphore(min(manifest.maxConcurrency, config.maxConcurrency))`(engine.ts:859),全局再一把 `deploymentSemaphore = maxConcurrency`,由 service 持有、所有 run 共享(service.ts:70, 77;engine.ts:1069)。许可释放时若队首已 abort,会把许可**转交**给下一个等待者而不是丢弃(engine.ts:361-380)。同一个 workflow 被两个调用者同时启动,得到两个独立 runId、两个独立目录,只有全局信号量把它们串起来;`resume` 的缓存也按 run 目录隔离,跨 run 不共享。

**恢复:三个不同的东西,名字最容易混。**

| 操作 | 真实语义 | 位置 |
|---|---|---|
| `pause`/`resume` | 只在内存里改状态;pause 只拦**尚未发布**的 task,已跑起来的 child 不动 | engine.ts:604-620, 848-853 |
| `rerun <runId>` | 用该 run 的不可变 capsule 快照重跑,`source: 'run-snapshot'` | service.ts:206-209 |
| `resume-run` | 同一份快照重跑 + 按 cache key 回放已完成 task | engine.ts:1030-1041 |

cache key 是 `sha256({version:2, workflow:{manifest,source}, runtime:{pluginVersion,dshVersion,verificationAdapter.cacheIdentity}, routing:{defaultProvider,modelTiers,readOnlyPolicy}, input})` 再加**同内容出现序号**(engine.ts:1019-1029;store.ts:116-119)。所以改了 source、换了 provider/只读策略、换了验证 adapter,都会自动失效——engine.spec.ts:342-355 专门钉住"只读策略变严则 cacheHits 归零"。

**测试能证明的契约**(静态计数,未运行):`tests/engine.spec.ts:308-330` 钉住 pause 只拦新任务、恢复后继续、原生事件严格成对且 run-start 带 `turn: null`;`:331-340` 钉住同一 task 回放后 `cacheHits:1, agentsStarted:0`;`:582-597` 钉住两个独立 run 共享部署并发(peak=1);`tests/store.spec.ts` 钉住"失败/未验证结果永不回放"与"绝对路径分区绑定项目";`tests/plugin.spec.ts:68-134` 钉住服务先发布、卸载时 abort 并等待所有 run、三工具+命令+prompt 都在。

## 为什么它突出

**先拆星标:这里没有归属错配的余地**。单仓库、非 monorepo 子目录,82/159 都是仓库级、也就是插件级。时间线反而是重点:

| 日期 | 事件 |
|---|---|
| 2026-08-12 16:39Z | 仓库创建 |
| 2026-08-13 | **5 个提交全部落地**(feat + license + 两次 handoff 修复 + preflight 加固),版本 0.1.2 |
| 2026-08-14 | tag v0.1.3:兼容基线从私有 snapshot 挪到公开 `deepseek-ai/deepseek-harness` |
| **2026-08-19** | **82 星采样点**(创建后第 7 天) |
| 2026-09-05 | tag v0.1.4:peer 改成 `^0.1.3-alpha.1`;**两个 tag 都不在 main 上** |
| 2026-10-14 | 远端最后一次 push(`pushed_at`),main 上并无新提交 |
| 2026-11-18 | 实时 159 星、13 fork、npm 仍 404 |

也就是说:**它在诞生后第 7 天就拿到了 82 星,然后用 3 个月零提交涨到 159**。这不是宿主背书,是早期关注 + README 的完成度;判断:可算作插件自身的声量,但绝对量在 703 条里属于长尾,不能当锚。

**零扩散的原因不是"没人用",是"没有可接的协议面"**:
1. 格式是自有的 `dsh.workflow` v1 capsule,而且 README:229 明说与 KodaX capsule **不做 wire compatibility**;要跑就得装这个插件,第三方抄格式没有收益。
2. npm 未发布(404),只能 `github:` 装;安装命令还指向旧组织名。
3. main 冻结在 0.1.2,后续修复只在 tag 上;一个外部开发者 clone 下来看到的代码比发布版旧。
4. 同 owner 在表内有 **44** 条条目(口径 `grep -l '^name: omdsh-dev/' data/plugins/*.yml | wc -l`),是批量发布型账号;另有 6 条别人的条目提到 `omdsh-dev`,但提的是 `dsh-browser`/`dsh-genui`,没有一条提本仓库。这 44 条我没有读,只用于说明"它不是一个靠社区协作长出来的仓库"。

**它的机制独特性在"恢复"和"沙箱"两处,而且都落在代码里**:

- **恢复 = 内容寻址的 effect 回放**,不是提示词里的"请从断点继续"(只说本插件,不对其他条目作横向统计)。key 里同时绑了 workflow 源、运行时版本、路由、只读策略和 task 输入,只有 completed 且无 verification warning 的结果才进缓存(engine.ts:1342;store.ts:127)。跨 run 目录不共享缓存,所以不会串味。
- **沙箱 = 独立 QuickJS 堆 + JSON-only 桥**,不是 `node:vm` 里跑脚本。64 MB 内存、1 MB 栈、同步片 10s、总墙钟 1h(runtime.ts:267-270;index.ts:87-88);`Math.random` 与 `Date.now` 被替换成抛错(runtime.ts:243-255);返回前强制走一遍 JSON 规范化(runtime.ts:411-441, 52-64)。这套东西让"生成的脚本"与"trusted-local 脚本"成了两个真正的信任等级,而不是注释里的两个词。
- **只读是交集,不是名单**:`readOnly` 子 agent 的工具面 = 配置 allow-list ∩ 当前父 agent 实际可见工具,并显式剔除 `run_code`(engine.ts:320-325);provider 不支持工具过滤就直接失败(:483),不会静默放开。

**能被第三方接的复用面,按可接性排序**:

1. **run 目录布局**——`.dsh/workflow-runs/<id>/{run.json,events.jsonl,workflow.workflow.json,script.js,results/,artifacts/}` 是纯文件 + 稳定事件词表(types.ts:267-278),外部做面板/审计/CI 归档都不需要改这个插件。
2. **capsule 格式**——`dsh.workflow` v1 有严格 schema 与 examples/review.workflow.json 样例,可以离线生成、版本控制、评审后再放回 catalog;`package.json:13-28` 还把 `capsule`/`catalog`/`store` 作为子入口导出。
3. **service key 与三个 adapter**——`ctx.dynamicWorkflows` 是 Cordis 服务,任何同进程插件都能 `ctx.inject` 它,并在**首次运行前**注册 `registerVerificationAdapter`/`registerIsolationAdapter`/`registerDispatchAdapter`(service.ts:82-101);注册晚了直接抛。worktree 隔离、existing-agent 目标、非 Git 工作区的证据,都只能从这里进。
4. **三个工具名可配**(`listToolName`/`runToolName`/`manageToolName`,index.ts:79-81),但改名只是换标签,不改协议。

## 代价与边界

**按发生顺序的失败模式:**

1. **装上就版本不对(最早发生)**。main 的 `dshVersion` 硬编码成 `0.0.1-rc.2`(index.ts:151-152),peer 全是 `^0.0.1-rc.2`(package.json:84-98);兼容基线记的是私有 snapshot 仓库(compatibility.json)。公开 DSH 的支持是在 tag v0.1.4 才补的(`^0.1.3-alpha.1`),而 `#main` 装的是 0.1.2。本机装的是 0.2.1-rc.5,peer 必然不满足。
2. **只读任务在 0.2.1-rc.5 上直接失败**。插件要求 `capabilities.toolFilter`(engine.ts:483;author.ts:40),而安装版 `SubagentCapabilities` 只有 `agentOptions`/`agentPreset`/`outputSchema`/`depthLimit` 四个字段(`dsh-subagent/lib/types/types.d.ts:114-121`),`toolFilter` 只剩在旧 session 描述的校验里(`dsh-subagent/lib/types/descriptor.js:44`)。判断:两个内建 workflow 都是 `readOnly: true`(builtins.ts:8),`/workflow review`、`parallel-investigation`、`/workflow create` 都会在第一个子 agent 之前抛 "cannot enforce read-only tool filtering";`readOnly:false` 的 inline workflow 仍可跑。**这是源码对照得出的判断,没有实跑**(见"待验证"第 1 条)。
3. **节点失败没有重试**。`runAgent` 把普通失败吞成 `null`(engine.ts:903-912),`spawnAgent`+`wait` 拿到完整失败结果;硬性 verification 最多 3 次 followup 修复,第三次仍不过就抛(engine.ts:1274-1319)。整个 run 不因为单个 task 失败而停——脚本自己决定降级。
4. **pause 不等于暂停**。已发布的 child 继续跑,只是新任务进不来(engine.ts:604-610, 848-853);要真停只能 `stop`,它会 abort 控制器、对每个 running task 调 `localAgent.cancel` 并 dispose(engine.ts:622-636)。
5. **进程重启后 run 变僵尸**。`run.json` 里仍是 `running`,但 engine 的 Map 是空的:`pause`/`resume`/`stop` 一律返回 false(engine.ts:604, 612, 622),`list` 只是把磁盘记录并进来(engine.ts:576-580),`apply` 里没有任何启动扫描(index.ts:683-696)。唯一清理路径是 `delete --force`(store.ts:184-189);docs/SECURITY.md:35 把它写成了规则:"force is reserved for non-terminal stale records after restart"。判断:「可恢复」在跨进程这一层不成立,能做的只有 `rerun`/`resume-run` 重开一个 run。
6. **run 记录的耐久性弱于 workflow 文件**。`run.json` 用 `writeFileSync` 直接覆盖(store.ts:115),且**每个事件都重写一次**(engine.ts:719);`events.jsonl` 用 `appendFileSync`,没有 fsync(store.ts:100)。读路径是全有全无:`getEvents` 逐行 `JSON.parse`(store.ts:145-149),最后一行截断会让整个 run 的事件读不出来;`get` 对 `run.json` 的 parse 没有 catch(store.ts:135-138),`show` 会抛,只有 `list` 做了逐目录 try/catch(store.ts:156-160)。反观 catalog 的保存是临时文件 + `link()` + rename + `.archive` 回滚(catalog.ts:287-313)——同一个仓库里两套耐久性标准。
7. **恢复不是幂等的**。缓存 key 不含工作区指纹(engine.ts:1019-1025),工作区变了仍会回放旧结果;第一次跑里失败的分支,resume 时可能成功,于是控制流走到另一条路。判断:幂等的是"单个 task 的成功效果",不是"这条 run 的决策路径"。
8. **`minDshVersion` 只是装饰**。它被要求存在、被校验成非空字符串(capsule.ts:231),全仓没有任何版本比较(只有 format/version/workflowApiVersion 必须等于 1)。README:118 说的"版本不兼容会在执行前失败"只覆盖 capsule 格式版本,不覆盖 DSH 版本。
9. **trusted-local 是宿主权限**。`.ts/.mjs/.js` 在显式一次性授权后直接 `import()`(catalog.ts:178-190),不受 QuickJS 约束;README:230 自己提醒不要把第三方源码标成 trusted-local。
10. **数据落在工作区**。`run.json` 的 process 项里存 child 的 finalText 摘要(engine.ts:763),`events.jsonl` 存 `agent-message` 正文(engine.ts:920),review packet 落在 `.agent/tmp/sessions/<sessionId>/review-packets/`(scoped-review.ts:263)。这些目录是否被提交,取决于用户的 `.gitignore`。
11. **测试在 main 上跑不起来**。devDependencies 全是 `link:../test-icetomoyo/*`(package.json:100-113),那个目录不在仓库里;v0.1.4 才改成已发布包。判断:main 的测试是"作者机器上可跑"的证据,不是外部可复现的证据。
12. **文档与宿主的漂移**:`docs/ARCHITECTURE.md:5` 说 "does not replace `ctx.workflows`",而安装版 DSH 的 seam 叫 `ctx.workflowEngine`(dsh-workflow/lib/index.js:61);`turn: null` 这个字段在安装版 `ToolWorkflowRunStartData` 里不存在,UI 判定 interrupted 只看 turn 结束原因是否为 `interrupted`/`forked`(dsh-client-ui-workflow-run/lib/client.js:531-535),不读 `data.turn`。它不会报错,只是不起作用。

## 可信度与复现

★★★:`src/` 12 个文件都打开读过(5 435 行):engine/index/service/store/runtime/capsule/catalog/author/types/source-policy 逐行,`builtins.ts` 与 `scoped-review.ts` 只读结构与关键段(两个内建与 6 个 pattern 的脚本体未逐行读);`lib/` 只用于核对构建产物的存在,未逐行读;`docs/*.md` 读了 ARCHITECTURE、SECURITY 全文与 KODAX_PARITY 头部。文中 `dsh-*` 开头的路径都相对于本机安装的 `~/.nvm/.../@deepseek-ai/dsh/node_modules/@deepseek-ai/`。**没有跑过任何测试或真实 workflow**——devDeps 指向不存在的同级目录,`pnpm install` 在外部 clone 上不可行。

```sh
# 1) 克隆与提交
git clone --depth 1 https://github.com/omdsh-dev/dsh_workflow.git /tmp/an-dsh-workflow
cd /tmp/an-dsh-workflow && git log -1 --format='%H %ad %s'    # 44b83c18… 2026-08-13 +0800
git fetch --unshallow --filter=blob:none && git rev-list --count HEAD   # → 5

# 2) 规模
wc -l src/*.ts | tail -1        # → 5435(12 个文件)
wc -l tests/*.ts | tail -1      # → 2609(11 个 spec)
node -e "const fs=require('fs');let n=0,e=0;for(const f of fs.readdirSync('tests')){const s=fs.readFileSync('tests/'+f,'utf8');n+=(s.match(/(^|\s)it\(/g)||[]).length;e+=(s.match(/it\.each/g)||[]).length}console.log(n,e)"  # → 113 10

# 3) 零扩散(在 awesome-dsh-plugin 仓库根;data/plugins 有 11 744 个文件,必须用目录形式)
grep -ril 'dsh_workflow' data/plugins/ | wc -l              # → 1(只有它自己)
grep -ril 'dsh-external/workflow' data/plugins/ | wc -l     # → 0

# 4) 实时事实(2026-11-18)
curl -s https://api.github.com/repos/omdsh-dev/dsh_workflow | grep -E '"created_at"|"stargazers_count"|"forks_count"|"size"'
# created_at 2026-08-12T16:39:26Z / stars 159 / forks 13 / size 546
curl -s -o /dev/null -w '%{http_code} %{redirect_url}\n' https://github.com/dsh-external/dsh_workflow   # → 301 → omdsh-dev
curl -s https://registry.npmjs.org/@dsh-external%2Fworkflow | head -c 80                                   # → Not found

# 5) main 落后于 tag
git ls-remote --tags origin | grep -E 'v0\.1\.(3|4)'        # v0.1.3 / v0.1.4 都不在 main
```

`data/` 在 `29b3ed46e` 与工作区 `ef5fca2c4` 之间无差异(`git diff --stat 29b3ed46e HEAD -- data/` 为空),所以上面的扩散数字与卡头截止日一致。

## 待验证

1. **只读任务是否真的在 0.2.1-rc.5 上抛错**:本机 `SubagentCapabilities` 没有 `toolFilter`,但只有实跑一次 `run_workflow`(或一个 `readOnly:true` 的 inline workflow)才能确认读的是同一份 descriptor,以及是否有别的 provider 带了这个能力。
2. **恢复的分支稳定性**:构造"第一次跑 task A 失败 → 走 else 分支;resume 时 A 成功"的脚本,确认第二次确实走另一条路——这决定"幂等"能不能说得更强。
3. **崩溃后的可读性**:在 `events.jsonl` 末尾截断一行、把 `run.json` 写成半截,分别测 `list`/`show`/`resume-run` 的行为;顺便确认没有 fsync 时断电的实际损失面。
4. **13 个 fork 里有没有真实衍生**:GitHub fork 列表 + 逐个看是否改了 capsule 格式或 run 目录布局;本卡的"0 扩散"只统计 data/plugins。
5. **README 的 179 tests**:静态只数到 113 + 10 张 `it.each` 表,差额要么来自表展开,要么徽章过期;在 tag v0.1.4 上跑一次 `pnpm test` 可定案(需要公网装依赖)。
6. **`turn: null` 在 0.1.3-alpha.1 里是否存在**:v0.1.4 的兼容基线是 0.1.3-alpha.1,若该版本 `ToolWorkflowRunStartData` 真有 `turn` 字段,则本卡第 12 条要改成"随宿主版本漂移"而不是"从未生效"。
7. **宿主 UI 的实际呈现**:没有实跑,无法确认插件写的 `tool-workflow/*` 事件在 DSH Web 里渲染出的卡片是否正确显示 phase/member,以及后台 run 跨 turn 时是否真的不被标"已中断"。
