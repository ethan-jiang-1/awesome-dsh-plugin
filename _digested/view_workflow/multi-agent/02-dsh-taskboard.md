# dsh-taskboard — 把共享任务状态压进一个 SQLite 文件，用 8 个窄工具把验收权锁在人手里

> 证据等级:★★★(源码级;`shengsheng90/DSH-taskboard@69a3db3b46ee04a960968af64a26f0ac901c82a5`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 40 为 2026-08-19 历史采样;该 URL 在下载边车里无记录(采样缺口,不是零下载)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `shengsheng90/DSH-taskboard`([registry](../../../data/plugins/shengsheng90__DSH-taskboard.yml)) |
| 类目 | workflow([census](../../ecosystem/census.py) 703 条 / 全表 11 744 条) |
| 子分类 | `multi-agent`(多 agent 共享一块任务板;本卡要回答的是"谁改哪一态、并发怎么裁决、失败怎么收敛") |
| 自述 | 「本地 SQLite 任务板,以原生覆盖页呈现:项目、任务、评论、关联、附件与工作流自动化,…`taskboard_*` 工具(Agent 只能提交到 `in_review`)、无头 JSON CLI 与打包 skill」。逐条对得上源码,**两处要打折**:workflow 节点没有执行器(18 种全是 design-only),skill 只打包不注册(见"代价与边界") |
| 星标 ⚠ | **40**(2026-08-19 采样);**2026-11-18 实时 328**(8.2 倍)。采样点距仓库创建 **5 天**、距 npm 首发 **3 天** |
| 下载 ⚠ | 边车无记录;2026-11-18 实时查 npm `@shengsheng/dsh-taskboard` 为 **1695 次/月**(2026-10-18 ~ 11-16),非边车数,仅作实时对照 |
| 扩散 | **0 个真衍生**(口径:`grep -ril 'taskboard' data/plugins/` 命中 **12** 条,减去自身 11 条逐条判定,见"为什么它突出"——其中 1 条是本仓库自述的祖先、1 条接同一祖先,其余是别人的派生或纯同类,都**不是**从本仓库派生) |
| 仓库 commit | `69a3db3b46ee04a960968af64a26f0ac901c82a5`,2026-11-01(-0800,`Merge pull request #43 … release-v0.1.11`),push 至 2026-11-02;仓库创建 2026-08-14,Apache-2.0,约 2 MB |
| 包形态 | npm/Cordis **bundle + 浏览器插件 + CLI** 三面一包:`dsh.bundle.patch` 指 `cordis.patch.yml`,`dsh.client.inject` 列 7 个前端服务,`bin.dsh-taskboard` 指 `lib/cli.js`(`package.json:13-15,86-102`) |
| 代码规模 | `src/` **8 262 行 / 24 个 `.ts`·`.tsx`**(其中 `src/sqlite/provider.ts` 1 808、`src/client/index.tsx` 1 764、`src/service/index.ts` 845);测试 **4 063 行 / 17 个 spec / 146 个 `test(`**;README 两份 836 行 + `docs/*.md` 652 行 |

## 它到底是什么

**不是配置包,是宿主内插件**:一个 `apply()` 挂起四件事——SQLite 权威、8 个模型工具、自动化调度器、浏览器覆盖页(`src/index.ts:65-91`)。DSH 侧零 patch:`docs/implementation-plan.md:21` 明说页面挂在既有 `sidebar.footer.action` / `shell.overlay` 两个 slot 上,"needs no patch to Harness-owned UI or Host source"。

**数据模型:11 张 STRICT 表 + 1 张单行 meta**(`src/sqlite/schema.ts:84-230`),版本号 `TASKBOARD_SCHEMA_VERSION = 4`(`:6`):

| 表 | 作用 | 关键约束(行) |
|---|---|---|
| `taskboard_meta` | 单行 `global_revision` | `CHECK (singleton = 1)`,`:87-91` |
| `projects` | 项目 + 可读 key | `key UNIQUE`、`next_issue_number`、`version`,`:93-103` |
| `tasks` | 任务主体 | **7 态 `CHECK`**(`backlog/todo/in_progress/in_review/blocked/done/canceled`)、`version`、`archived_at`、`development_context_json`、`workflow_id`,`:105-127`;索引 `:128` |
| `task_claims` | **独立的第四类实体**:谁在什么 session 上持有 | 状态 `active/orphaned/released/submitted/reclaimed`;唯一部分索引 `task_one_active_claim ON task_claims(task_id) WHERE state IN ('active','orphaned')`,`:130-142` |
| `task_relations` | `parent` / `blocks` / `related` | `UNIQUE(source,target,kind)`、`CHECK(source<>target)`、`task_one_parent` 部分唯一索引(一任务最多一个父),`:144-155` |
| `comments` / `task_activities` | 协作记录 / 审计流水 | `:157-178`(activity 按 `(task_id, created_at, id)` 建索引 `:178`) |
| `attachments` | 元数据;**字节在文件系统** | `storage_key UNIQUE`,`:180-189` |
| `attachment_cleanup` | 删不掉的字节进队列重试 | `attempts`,`:191-197` |
| `workflow_workspaces` | **编辑器的 JSON 文档**,不是运行记录 | `document_json`,`:199-207` |
| `automation_rules` / `automation_runs` | 真正会执行的自动化 | `config_json`、`last_decision_json`、`next_eligible_at`,`:209-226` |

注意 registry 自述里的 "workflow" 对应的是 `workflow_workspaces`(画布文档);**真正有执行语义的是 `automation_rules`**——两者不是一回事,别读混。

**状态机与权限**(每一格都在 provider 里强制,不是 UI 层约定):

| 迁移 | 谁能触发 | 代码 |
|---|---|---|
| (新建)→ `backlog` \| `todo` | 人;创建时**只能**落这两态 | `domain/types.ts:168`、`cli.ts:80-86` |
| `backlog` → `todo` | 人 `approve` | `provider.ts:560-563` |
| `todo` → `in_progress` | agent/automation `claim`(同事务内重查依赖 + 独占 claim) | `provider.ts:565-606` |
| `todo` → `in_progress` | 人把原生 Session 绑到任务 `bindHumanSession` | `provider.ts:613-632` |
| 任意 → 任意(拖拽) | 人 `moveStatus`;离开 `in_progress` 时释放 claim | `provider.ts:693-731` |
| `in_progress` → `in_review` | **仅持有 active claim 的那个 agent/automation** | `provider.ts:634-655` |
| `in_review` → `done` | **仅人** `accept` | `provider.ts:688-691` |
| `in_review` → `todo` \| `in_progress` | 仅人 `returnForRework`(可原子建新 claim) | `provider.ts:657-686` |
| `todo` \| `in_progress` → `blocked` | 人;agent 只有在**自己持有的 `in_progress`** 上才能 | `provider.ts:733-751` |
| `blocked` → `todo` \| `in_progress` | 仅人 `resume` | `provider.ts:753-781` |
| 非 `done` → `canceled` | 仅人 | `provider.ts:783-786` |
| `done` \| `canceled` → `todo` | 仅人 `reopen`(必须给理由,落一条评论) | `provider.ts:788-801` |
| 归档 / 删除 | 仅人;有活 claim 不能归档,未归档不能删除 | `provider.ts:827-854`、`:988-1004` |

"人"由 `requireHuman` 断言(`domain/policy.ts:17-22`),每个入口第一行调用;`HUMAN_ONLY` 集合(`policy.ts:4-7`)只是可用性清单,真正拦人的是这些断言。**这套表就是"Agent 只能做到 `in_review`"的全部机制**——不是提示词,是 `accept()` 第一行的 `requireHuman`,加上工具面根本不存在 `accept`(见下节)。

## 怎么接进 DSH

**① manifest 只有两个键。** `dsh.bundle.patch → ./cordis.patch.yml`(`package.json:86-89`)让 DSH 把它当 profile 层;`dsh.client.inject` 列 7 个前端服务 + `"platform": "web"`(`:90-101`)让浏览器侧被打包加载。后者由宿主 `dsh-client-modules` 校验(`DSH/node_modules/@deepseek-ai/dsh-client-modules/lib/client.js:39-63`),前者由 `dsh-app-boot` 读取(`…/dsh-app-boot/lib/index.js:513-525`)。

**② patch 是一行 `insert`,全部行为来自 config。** `cordis.patch.yml:1-17`:`id: taskboard`、`name: '@shengsheng/dsh-taskboard'`,以及 12 个配置项——数据库/附件路径(带 `!!js process.env` 回退)、`pageSize`、两级附件上限、`minAutomationIntervalMs: 30000`、`maxProjectWorkers: 2` / `maxGlobalWorkers: 4`、`allowSharedWorktrees: false`、`clientRefreshIntervalMs: 15000`、`maxChangeWaiters: 128`、`maxChangeWatchMs: 30000`、`defaultAgentPreset: standard`。类型与默认值在 `src/index.ts:42-62`(schemastery)。

**③ 五个注册点,全是 DSH 公共 API:**

| 注入 | 干什么 | 行 |
|---|---|---|
| `ctx.inject(['tools'])` | `registerTaskboardTools` 逐个 `ctx.tools.register(defineTool(...))` | `src/index.ts:67`、`tool/index.ts:173-175` |
| `ctx.inject(['agents','goals','workspaceRegistry','agentPresets','agentDefaultModel'])` | 建 worker + 调度器;启动时先 `reconcile()` 再 `start()`,**reconcile 失败也照常启动**(注释说明:一次瞬时失败曾让整个 Host 没有定时器) | `src/index.ts:68-90` |
| `ctx.inject(['connection','webServer'])` | 在宿主 web server 上挂 `/taskboard` 前缀路由做写通道 | `service/index.ts:297-338` |
| `ctx.inject(['webServer'])` | 挂 `/taskboard/attachments` 字节路由 | `service/index.ts:421-423`、`attachments.ts:37-49` |
| `ctx.inject(['skills'])` / `ctx.inject(['tools'])` | **只读**:给 workflow 编辑器列出可引用的 skill / `mcp__*` 工具 | `service/index.ts:424-443` |

**④ 浏览器侧:两个 slot,没有自制路由。** `client/index.tsx:1708-1709` 把 `TaskboardNavButton` 注到 `sidebar.footer.action`、把 `TaskboardPage` 注到 `shell.overlay`(`PropsRuntime<'shell.overlay'>`,`:128`)。两个 slot 名在本机 DSH 里真实存在:`dsh-client-ui-layout/lib/client.js:643`、`dsh-client-ui-sidebar/lib/client.js:515,643`。Remote 贡献用 `remote.$mount(taskboardRemote)`(`:1673`),不写 hash 路由——导航到别的 Session 时靠订阅 session store 自动关页(`:1695-1703`)。

**⑤ 写通道为什么绕开 Typert Remote。** 读走 Typert(`snapshot` / `taskDetail` / `changes.watch`,只读),写必须走 `/taskboard/<endpoint>`:注释写明 DSH `0.2.0-rc.2` 起 `Connection.rpc.handle()` 不再挂上 webServer,导致"/taskboard 没被服务、但页面还能打开、每次写静默失败"(`service/index.ts:289-296`)。于是它自己 `webServer.register({kind:'prefix', path:'/taskboard'})`,**只借 Connection 的 `requestRejection()` 做鉴权判定**(`:301-303,342-347`),不自己实现 authority。反过来,Typert 的 `remoteMutate` 对一切非 `changes.watch` 的端点直接返回 `loopback-required`(`:542-573`)——两条通道不会互相绕过。

**⑥ 不需要 patch 宿主,但需要 Node 22.19+** 的 `node:sqlite`(`package.json:8-10`)。安装:`dsh plugin --profile web add -w git+https://github.com/shengsheng90/DSH-taskboard.git`(`README.md:94-96`);`dsh plugin` 本身只是把参数转发给 pnpm(`DSH/lib/bin.js:116-120`)。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `src/sqlite/provider.ts` | 1 808 | **唯一权威**:所有状态迁移、CAS、事务、附件、健康度 | `transaction` `:1759-1793` |
| `src/sqlite/schema.ts` | 231 | DDL + 1→2→3→4 单调迁移 | `:30-49`、`:51-82` |
| `src/sqlite/paths.ts` | 244 | 相对路径绑到 git root / `$DSH_HOME`,并写 `.gitignore` | `:109-171`、`:213-244` |
| `src/service/index.ts` | 845 | `TypertRemoteService` 外壳 + `/taskboard` RPC + 长轮询 | `:297-420`、`:575-615` |
| `src/tool/index.ts` | 175 | 8 个模型工具,**刻意没有 accept** | `:30-31`、`:32-169` |
| `src/automation/index.ts` | 325 | 持久调度器:定时、并发槽、决策落库 | `:156-246`、`:248-256` |
| `src/execution/index.ts` | 354 | 把一次 claim 变成一个真 Agent + Goal | `:223-278`、`:280-313` |
| `src/cli.ts` | 365 | 无头 JSON CLI | `:16-36`、`:123-357` |
| `src/client/index.tsx` | 1 764 | 原生覆盖页(看板/列表/甘特/工作流/仪表盘) | `:1666-1716` |
| `src/workflow/index.ts` | 228 | 18 种节点目录 + 文档校验与编辑算子 | `:8-27`、`:50-77` |
| `tests/*.spec.ts` | 4 063 | 146 个用例,见下 | — |

**工具面(为什么模型只能到 `in_review`)。** `taskboardToolDefinitions` 返回**恰好 8 个**名字:`taskboard_list`/`get`/`claim`/`comment`/`submit_review`/`block`/`release_claim`/`relate`(`tool/index.ts:32-169`),`tests/tool.spec.ts:10-22` 用 `deepEqual` 钉死这个清单并断言 `names.includes('taskboard_accept') === false`。没有 `accept`、没有 archive/delete、没有通用改状态。`submitReview` 还要求非空 `verification` 与非空 `result_comment`(`provider.ts:636-637`),并把证据拼进评论(`:643-648`)。**模型无法自我验收:能走到的终点是 `in_review`;`done` 只有 `accept()` 一个入口,而它第一行就是 `requireHuman`(`:689`)。**

**身份从哪来。** 工具的 actor 不是参数,是运行时:`exec.agent.id` 同时当 `agentId` 与 `sessionId`(`tool/index.ts:15-20`),所以 `assertOwningClaim` 比的是 agent id(`provider.ts:1448-1454`)。**浏览器侧的"人"是常量** `human('human:web-client')`(`service/index.ts:300`)——凡是能过 `requestRejection` 的请求都算人,没有 per-user 身份。

**并发:三层防重,裁决点只有一个。**
1. 外层唯一部分索引 `task_one_active_claim`(schema.ts:142),`claim()` 先查活 claim 再插入(`provider.ts:573-575`),DB 层兜底;
2. 中层 CAS:`mutableTask` 校验 `expected_version`(`provider.ts:1379-1384`),`writeStatus` 的 `UPDATE … WHERE version = ?` 要求 `changes === 1`(`:1396-1400`);
3. 事务:`BEGIN IMMEDIATE` 一把拿写锁,提交后才 `publish` 失效事件;订阅者抛错也不回滚(`:1759-1793`)。
   `claim()` 还在**同一事务内**重查 `blocks` 依赖(`:577-590`)和"独占开发上下文"(同分支/同 worktree 只能有一个持有者,`:1529-1557`)——注释说明拖拽入列曾绕过这道检查(`:711-715`)。

**自动化 = 定时认领器,不是工作流引擎。** `TaskboardAutomationCoordinator` 从 SQLite 读规则、按 `nextEligibleAt` 设 timer(`automation:95-104`),`drain()` 每次取 `todo`、按 `min(全局余量, 项目余量, 规则余量)` 起 worker(`:248-256`),把每次决策写回 `automation_runs`(claimed/empty/dependency-blocked/error/quota-paused,`:198-200,236-242`)。**单个候选被抢不算失败**:`TASK_ALREADY_CLAIMED`/`TASK_STALE_VERSION`/`TASK_DEVELOPMENT_CONTEXT_BUSY`/`TASK_INVALID_TRANSITION` 被归为"换下一个"(`:23-25,220-221`)。worker 先**同步** `claim()` 再 spawn(`execution:176-186`),这样调度器不会把输掉事务竞争的候选算进并发;随后 `ctx.agents.create/resume` + `installModelSelection` + `agentPresets.mount` + `goals.create`,`followup` 一条带 `source: {kind:'taskboard', taskId, claimId}` 的用户消息(`:231-263`)。**Goal 完成 → `submitReview`;Goal blocked → `block`**;`todo` 永远不会被自动认领之外的路径改(`:280-313`)。人改任务时还会 `steer()` 一条"重读任务"的追加消息(`:329-353`)。

**工作流节点没有执行器。** `WorkflowNodeRegistry.catalog()` 只在注册了 `provider.execute` 时标 `executable`,否则 `design-only`(`workflow/index.ts:43-48`);全仓 `workflowNodes.register` **零调用**(`grep -rn 'workflowNodes.register' src/` 无输出),所以 18 种节点恒为 design-only,`docs/architecture.md:26` 也承认"assigning a workflow renders its ordered document into the Agent task instruction as guidance; the scheduler does not implicitly execute nodes"。`renderWorkflowGuidance` 把文档渲染成文本塞进任务指令(`execution:98-108`)。

**CLI 契约。** 每次输出一行 `{schemaVersion:1, value}` 或 `{schemaVersion:1, error:{code,message,details}}`(`cli.ts:27-36`);退出码 `0/2/3/4/5`(成功/用法/存储不可用/领域拒绝/版本冲突,`:16-20`),冲突码 `TASK_STALE_VERSION` 单独映射 5(`:352`)。命令组 `project|task|relation|attachment|workflow|automation|storage` 共 40 余条(`:174-344`),`storage status` 直接吐 `storageHealth()`(`:336-344`)。**所以可以完全不开 UI 操作任务板**,甚至用 `task accept` 完成人工验收。呈现层另有 `examples/taskboard/run.mjs` + `browser-fixture.html` 的确定性浏览器脚本(`docs/browser-e2e.md`)。

**测试钉住的是契约,不是实现。** 146 个 `test(`:认领/评审/人工验收全链路(`sqlite-provider.spec.ts:69-99`)、陈旧写不改变已提交状态(`:168-180`)、claim 事务内重查依赖(`:181-212`)、父环拒绝(`:213-230`)、孤儿 claim 不可被偷(`:231-252`)、独占开发上下文全入口一致(`:598-643`)、重启往返(`:333-353`)、调度器并发与"换候选"(`automation.spec.ts:168,369,403,462`)、CLI 五类退出码与七域往返(`cli.spec.ts:19-38`)、RPC 鉴权与载体拒绝(`rpc-routes.spec.ts`)、页面路由与 i18n(`client-route.spec.ts`,26 例)。CI 另有 5 个 DSH 版本 × Node 22/24 的安装加载矩阵(`ci.yml:36-52`)。

## 为什么它突出

**先拆星标:40 不是它的位置,是它的出生日期。** 仓库 2026-08-14 建、npm 0.1.0 于 2026-08-16 首发、⚠ 采样日 2026-08-19——**采样点落在上线第 3 天**。之后 2026-11-18 实时 328,即 8.2 倍;同期 npm 实测 1695 次/月。判断:⚠40 是"上线首周"读数,不能当"低星项目"用;但 328 也谈不上头部,它的信号强度在**1695 次/月的下载量与 11 个 fork**,不在星标。

**扩散:真衍生 0,但有血缘的 2 条,而且它自己也是衍生。**
`grep -ril 'taskboard' data/plugins/` 命中 12 条,减去自身后逐条判定:

| 条目 | 判定 | 依据 |
|---|---|---|
| `chuspeeism/dashi-taskboard#deepseek-harness` | **祖先**(非衍生) | 本仓库 `THIRD_PARTY_NOTICES.md:5` 自述"independently reimplemented with reference to `chuspeeism/dashi-taskboard` at `9b2aeb53…`(Apache-2.0),No source file … is copied"。该条目的 npm 包名是 `codex-taskboard`、bin 是 `taskctl`(2026-11-18 实读其 `package.json`),属另一条 Codex 血统 |
| `ttmouse/dsh-taskboard` | **同宗不同枝** | 其 `package.json` 自述 "forked from reasonix-taskboard (dashi-taskboard)"——接的是 dashi 血统,不是本仓库(该 `reasonix-taskboard` 与 `chuspeeism/dashi-taskboard` 是否同一仓库,未核) |
| `cloader/dsh-taskboard` | **同类(独立实现)** | 10 个 `taskboard_*` 工具、"agent 永远移不到 done"的协议闸、host 侧 cron、SSE(2026-11-18 实读其 README/package.json);无任何指向本仓库的署名 |
| `zirscard/dsh-taskboard-epic` | 衍生于 cloader | registry 自述 "Requires the cloader/dsh-taskboard plugin" |
| `ijry/…#dsh-plugin-taskboard` | **同类(独立实现)** | 其 `package.json` 自述 "modeled on codeg-plus's 任务看板: four codeg-plus columns (todo/inProgress/attention/done), human-only acceptance" ——列数与列名都不同 |
| `ijry/…#dsh-plugin-repopanel` | 衍生于 ijry 同 monorepo 的 taskboard | registry 自述把 issue "file one as a task on dsh-plugin-taskboard" |
| `SilenZerOrz/taskboard-workbench` | 同类(独立实现) | registry 自述:侧栏看板 + 本地 SQLite + 派发给编码 agent;未读源码,不判血缘 |
| `1070296335-create/dph-taskboard` | 同类不同物 | 卡片对象是 **Session**,不是任务(registry 自述) |
| `Asher-2000/dsh-expert-mode` | 只是同词 | 文件系统状态机 `pending/ready/running/done/failed` + 依赖 DAG,**不是** SQLite 任务板 |
| `mario841859784/dsh-expert-orchestrator` | 只是同词 | 依赖 DAG 任务板 + 文件消息总线,agent preset |
| `fffgfffff/cike-taskboard` | 只是同词 | 个人日程排程器(今日任务/午休分段/7 天日历) |

**计数(合计 11):真衍生 0;祖先 1(`chuspeeism`)、同宗 1(`ttmouse`)、同类独立实现 3(`cloader`、`ijry` 的 taskboard、`SilenZerOrz`)、同类不同物 1(`dph`,卡片对象是 Session)、纯派生 1(`zirscard`→`cloader`)、同 monorepo 派生 1(`repopanel`→`ijry`)、纯同词 3(`Asher`/`mario`/`cike`)。** GitHub 层面另有 11 个 fork,全部 0 星,且**没有一个进入 registry**(其中 `drscrewdriver` 在 registry 里有 29 条别的条目,也没把这份 fork 列进去)——说明在这个生态里"fork 一个仓库"和"被当成一个实现"是两件事。

**那么 3 个独立实现同时在写 `taskboard_*` 说明什么?** 判断:**收敛发生在接口命名与一条不变量上,不在状态机或存储上**。三个互不署名的代码库(shengsheng90、cloader、ijry)都收敛到 `taskboard_*` 前缀 + "agent 不能把人验收的那一步做掉";而列数(shengsheng90 是 7 态 / cloader 五列 / ijry 四列)、存储(SQLite+Typert 长轮询 / SQLite+SSE / 未读)、驱动方式(显式 claim+自动化调度 / 新建会话自动拉取 / workspace-bound claim)全不相同。也就是说:**"人验收"是被反复独立重新发明的一条最小心智模型,而具体协议并没有收敛**——如果真收敛,衍生者会复用同一个存储格式或同一份 schema,这里一个都没有。另一半解释更朴素:任务板是"最小可共享状态"里最容易从零写的一个,门槛低到每个作者都会自己写一遍,12 条里 3 条纯属名字撞车(`cike-taskboard` 是排程器)。**两条原因叠加,才是"低星 + 多实现"的真相;把它读成"标准正在形成"会高估这个分支。**

## 代价与边界

- **运行时门槛硬**:`node:sqlite`,要求 Node `^22.19.0 || >=24.0.0`(`package.json:8-10`);实测在 v22.23.1 上每次打开都打 `ExperimentalWarning: SQLite is an experimental feature`。22 个 `peerDependencies` 全部标 `optional`(`package.json:103-126,172-239`),其中 19 个 `@deepseek-ai/dsh-*` 写成 `*`(不设版本门),只有 `@deepseek-ai/cordis@^4.0.2`、`schemastery@^3.18.2`、`react@^18.2.0` 带下界。`optional` 只是让包管理器不要再装一套 Harness/React,**不是 API 可以缺失**;兼容性靠 CI 矩阵自证,宿主升级后仍可能踩 API 漂移(`docs/plugin-compatibility.zh.md:42`)。
- **跨进程并发没有排队,直接失败。** 代码里没有 `PRAGMA busy_timeout`,`DatabaseSync` 构造也没传超时(`schema.ts:30-34`)。实测(本机 v22.23.1,两进程对同一 WAL 库):第二个进程的 `BEGIN IMMEDIATE` 在 **0 ms** 就以 `database is locked` 失败。后果:Host 与 `dsh-taskboard` CLI 同时写、或两个 Host 进程共用一个库,写会**立刻**报错,且这是原生 SQLite 错误而非 `TaskboardError`(事务 catch 只 `rollback()` 再抛,`provider.ts:1768-1771`),在 RPC 侧会落到 `code: 'internal'`。读不受影响。
- **同进程内的"并发"其实是串行。** `node:sqlite` 是同步 API,provider 单实例、`BEGIN IMMEDIATE` 贯穿整个 `operation()`;多 agent 只能在 await 边界交错,真正裁决的是 `expected_version` 与唯一索引。**所以它的并发安全是"单写者 + 乐观锁",不是"多写者协调"。**
- **`blocks` 环不检测。** 只有 `parent` 走 `wouldCreateParentCycle`(`provider.ts:1516-1527,1120-1122`);`A blocks B` + `B blocks A` 会双双通过,而 `claim()` 要求所有 `blocks` 依赖 `status = 'done'`(`:577-590`)——两个任务从此**永久不可认领**,也没有任何界面提示这是环。
- **迁移只单向。** `user_version > 4` 直接拒绝并关库(`schema.ts:36-43`),没有降级路径;1→2→3→4 全是 `BEGIN IMMEDIATE` 里的 DDL(`:51-82`)。V4 迁移会跳过缺失表的索引(`:22-27`),这是为"半创建"的库留的活口。
- **打不开库 = 整块看板消失。** `new SqliteTaskboardProvider` 直接写在 `apply()` 里(`src/index.ts:66`),没有 try/catch;库文件损坏/权限不足会让插件挂载失败,而不是降级成只读。构造时还会同步跑 `quick_check(1)` 与一次清理重试(`provider.ts:316-317`)——这发生在 Host 启动路径上。
- **附件字节与元数据是两套一致性域。** 字节先 `openSync(...,'wx')` + `fsync` + `rename` 落盘,再提交行(`provider.ts:1663-1681`);删除失败进 `attachment_cleanup` 队列,重试 10 次后转 `stalled`(`:1695-1718`)。但上传/下载的 capability ticket 只在**内存 Map**、TTL 60 s(`attachments.ts:32,35`):Host 重启或换进程,已签发的 URL 直接 404。
- **"人"没有身份粒度。** 浏览器写一律记成 `human:web-client`(`service/index.ts:300`),审计里区分不出是谁点的验收。安全边界等于宿主的 `Connection.requestRejection`(`service/index.ts:342-347`)。
- **分发包落后于仓库。** `package.json` 是 0.1.11,但 npm `latest` 停在 **0.1.9**(2026-10-13),git tag 也只到 `v0.1.9`;`dsh plugin --profile web add -w @shengsheng/dsh-taskboard` 与 `… add -w git+https://…` 装到的不是同一份代码。`lib/` 是提交进仓库的构建产物,靠 CI `git diff --exit-code -- lib` 保鲜(`ci.yml:31`)。
- **skill 只在包里,不在宿主里。** `skills/manage-taskboard/SKILL.md` 被打进 tarball(`package.json:82`),但 `src/` 里**没有任何注册/安装动作**;`ctx.inject(['skills'])` 只 `snapshot()` 读宿主已有 skill(`service/index.ts:424-434`)。模型要看到它,得由人或安装 prompt 手工拷进宿主的 skills 目录(README 未给这一步)。**"打包 skill" 目前等于"随包附一份操作手册"。**
- **数据位置会挑目录。** 相对路径绑到最近的 git 项目根,而不是 cwd;不在项目里就退到 `$DSH_HOME`(`paths.ts:109-127`);还会往 `.dsh/` 写一个 `*` 的 `.gitignore`(`:213-244`)。同一台机器上从不同目录起 Host,可能落到不同的库——README 专门有一节"Upgrading from a cwd-relative store"(`README.md:369`)。
- **文档漂移。** `docs/acceptance-audit.md` 写 "The current suite passes 53 tests",源码里是 146 个 `test(`;两处口径至少有一处滞后。
- **失败模式,按发生顺序**:① 库打不开/损坏 → 插件挂载失败,看板整块不见;② schema 超前 → `STORAGE_SCHEMA_UNSUPPORTED` + 关库,同样挂载失败;③ 跨进程写 → 立即 `database is locked`(原生错误);④ 版本竞争 → `TASK_STALE_VERSION` / `TASK_ALREADY_CLAIMED`,模型侧表现为"重读再试",自动化侧表现为"换下一个候选";⑤ agent 进程死亡 → claim 转 `orphaned`,**不会被静默偷走**,只能人 `force-takeover` 或原 automation 在原 Session 上恢复(`execution:189-200`),坏处是任务会一直挂在 `in_progress` 等人;⑥ `blocks` 环 → 永久不可认领;⑦ 附件字节丢 → 下载失败,cleanup 队列 `stalled` 计数上升,`storageHealth().status` 变 `degraded`(`provider.ts:1744`);⑧ 页面断连 → 长轮询封顶 30 s(`maxChangeWatchMs`),另有 15 s 周期快照兜底(`clientRefreshIntervalMs`)。**恢复路径**:`storage status`(CLI)或 `storage.check-integrity`(RPC)看健康度;`docs/security.md:15` 明说备份必须同时含 SQLite(含 WAL)与附件目录,且"恢复前先停 Harness"。

## 可信度与复现

★★★,但边界要说清:`src/` 24 个文件里逐行读了 provider / schema / paths / tool / service / automation / execution / cli / workflow / client(注册段与错误处理段);**`src/client/index.tsx` 1 764 行只读了注册、slot、样式与错误处理段,看板/甘特/工作流编辑器的渲染逻辑未逐行读**。`lib/` 与 `generated/` 是产物,未读。测试读了全部用例名 + 3 个用例正文,**没有实跑**(仓库无 `node_modules`,`pnpm install` 未执行)。扩散判定里 4 个"同类独立实现"各读了其 `package.json` 或 README(2026-11-18,非源码级),其余只依据 registry 自述。

```sh
# 1) 克隆与提交
git clone --depth 1 --filter=blob:none https://github.com/shengsheng90/DSH-taskboard.git /tmp/an-taskboard
cd /tmp/an-taskboard && git log -1 --format='%H %ad %s'
# → 69a3db3b46ee04a960968af64a26f0ac901c82a5 Sun Nov 1 17:49:50 2026 -0800 Merge pull request #43 …

# 2) 规模
find src -type f \( -name '*.ts' -o -name '*.tsx' \) | xargs wc -l | tail -1     # → 8262
grep -c "^test(" tests/*.spec.ts | awk -F: '{s+=$2} END {print s}'                # → 146

# 3) 扩散(在 awesome-dsh-plugin 根;注意 data/plugins 有 11 744 个文件,直接用目录形式)
grep -ril 'taskboard' data/plugins/ | wc -l        # → 12(含自身)
grep -rl 'taskboard_' data/plugins/                # → 2(自身 + ijry 的独立实现)
grep -ril 'shengsheng' data/plugins/ | wc -l       # → 3,其中 2 条是同名子串误命中

# 4) "模型没有验收权"的两处硬证据
sed -n '10,22p' tests/tool.spec.ts                 # deepEqual 8 个工具名 + 断言无 accept
sed -n '688,691p' src/sqlite/provider.ts           # accept() 第一行 requireHuman

# 5) 工作流节点没有执行器
grep -rn 'workflowNodes.register' src/             # → 无输出
grep -rn 'workflowNodes.register' src/ | wc -l     # → 0

# 6) 跨进程写冲突(本机 v22.23.1 实测,两进程同一 WAL 库)
#    第一个进程 BEGIN IMMEDIATE 持锁 → 第二个进程 0 ms 报 "database is locked"

# 7) 星标/下载
curl -s https://api.github.com/repos/shengsheng90/DSH-taskboard | grep -E 'stargazers_count|forks_count|created_at|pushed_at'
curl -s https://api.npmjs.org/downloads/point/last-month/@shengsheng/dsh-taskboard
```

## 待验证

1. **`pnpm test` 实跑**:仓库无 `node_modules`,146 个用例只是静态计数;`docs/acceptance-audit.md` 的 "53 tests" 与源码是否同一口径,跑一次才能定。
2. **跨进程并发在真实 Host 里的表现**:实测是 `database is locked`,但没验证 DSH 的 RPC 层把它翻成什么(`code: 'internal'` 是读代码推断),也没验证 CLI 与 Host 同时写时的用户可见表现。
3. **两份 npm 源是否等价**:npm `latest = 0.1.9`(2026-10-13)、仓库 0.1.11、tag 到 v0.1.9。0.1.10/0.1.11 是否有 GitHub Release tarball 未查;两条安装路径装到的代码差多少未 diff。
4. **`blocks` 环的实际后果**:代码没有环检测,但没实跑构造 `A blocks B` + `B blocks A` 后 `claim()` 的报错形状,也没确认 UI 是否会给出可理解的提示。
5. **skill 是否真的能被模型看到**:`skills/manage-taskboard` 未被任何代码注册;若宿主不扫包内 `skills/`,则它对模型完全不可见,需一次实机确认(`dsh` 的 skills 目录约定未查)。
6. **`dsh.client.inject` 的 7 个服务名是否都是当前宿主的真实 key**:只在 DSH 包里确认了 `dsh-client-modules` 会校验这个字段,没有逐名核对 `remote`/`uiWorkspace`/`conversation` 在当前版本是否仍以此名暴露。
7. **11 个 GitHub fork 是否有实质改动**:全部 0 星、未进 registry,但没有 diff 任何一个 fork,不能断言"无人改动"。
