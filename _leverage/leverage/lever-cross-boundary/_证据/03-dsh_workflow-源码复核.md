---
title: "03 · omdsh-dev/dsh_workflow 源码复核"
domain: cross-boundary
kind: evidence
positioning: "44b83c1 固定复核：subagent 之上的运行态/治理层，不是 DAG 引擎；可复现靠快照+内容键缓存。"
read_when: "要引用 03 号样本的机制断言，或核对它到底是不是断点续跑。"
status: observed
updated: 2026-11-01
---

# 03 · `omdsh-dev/dsh_workflow` 源码复核

> 复核对象：样本卡 [`03-omdsh-dev-dsh_workflow.md`](../samples/03-omdsh-dev-dsh_workflow.md)。
> 一句话结论：卡片的主体机制断言成立；**偏差集中在数字（13 类正则、3 轮修复）、版本坐标（0.1.2 不是最新 tag）、以及"重启"的表述精度（丢控制面 ≠ 丢记录）**。宿主契约另有两处卡片未覆盖：`turn:null` 事件载荷与 peer 版本范围。
> 下次复核只需要看：`package.json`、`compatibility.json`、`src/index.ts:151-152`、`src/source-policy.ts:13-25`、`src/engine.ts:604-636`。

## Provenance

| 项 | 值 | 核对方式 |
|---|---|---|
| 仓库 | [`omdsh-dev/dsh_workflow`](https://github.com/omdsh-dev/dsh_workflow)（repo id `1332243516`，创建 2026-08-12，MIT，TypeScript，154★/11 fork @2026-11-01） | GitHub REST `/repos` |
| **复核固定点** | **`main` @ [`44b83c182aa02d1be8a0803e8446cb495f93cd8f`](https://github.com/omdsh-dev/dsh_workflow/commit/44b83c182aa02d1be8a0803e8446cb495f93cd8f)（2026-08-13T04:20:40Z，`fix: harden workflow handoff preflight`）** | `/commits/main`；tarball 落地 `/tmp` 只读复核 |
| package.json 版本 | `0.1.2`（同 commit） | [package.json](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/package.json) |
| npm 包名 | `@dsh-external/workflow` | 同上 |
| **npm 发布状态** | **未发布**：`registry.npmjs.org/@dsh-external%2Fworkflow` → **404** | 2026-11-01 实取 |
| tag 对齐 | **不对齐**：仅有 `v0.1.3`（→`804e4c3`，2026-08-13T23:53Z）与 `v0.1.4`（→`bdc4554`，2026-09-05T04:09Z）；**不存在 `v0.1.2` tag**。`main` 是 `v0.1.4` 的祖先（compare: ahead 4 / behind 0） | `/tags`、`/compare/44b83c1...bdc4554` |
| 最新 tag | `v0.1.4`，package.json `0.1.4`，GitHub Release 只发到 `v0.1.3` | `/releases` |
| 0.1.4 与固定点差异 | `src/` **仅 `src/index.ts:151-152` 两行**（`pluginVersion`/`dshVersion` 常量），机制代码逐字相同；另改 README 结构、`compatibility.json`、`package.json` | `diff -ru` 两个 tarball |
| 宿主兼容 pin | `compatibility.json` = **私有仓** `dsh2026/test-icetomoyo`，branch `snapshots/20260812T172954Z-final-unwatermarked-5fa48343c7`，commit `7b9644f2b664e46c9518506035aa6c8d5af4d8e8`，version **`0.0.1-rc.2`** | [compatibility.json](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/compatibility.json) |
| tag 处的宿主 pin | v0.1.4 改为公共仓 `deepseek-ai/deepseek-harness` @ `d347e703…`，version **`0.1.3-alpha.1`** | v0.1.4 tarball 内 `compatibility.json` |
| 设计参照 | KodaX @ `2e596638…`，声明 "Behavioral reference only" | [reference.json](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/reference.json) |

**Owner 谜题（卡片最大的坐标错误）**：`api.github.com/repos/dsh-external/dsh_workflow` 返回 **301 → `https://api.github.com/repositories/1332243516`**，即 **`dsh-external/dsh_workflow` 与 `omdsh-dev/dsh_workflow` 是同一个仓库**（改名/转移后的 GitHub 重定向），不是"两个不同 owner、要先确认哪个是活的"。`package.json` 的 `repository`/`homepage`/`bugs` 仍写旧名 `dsh-external/dsh_workflow`（同一文件），说明改名后未回写。安装串 `github:dsh-external/dsh_workflow#main` 目前靠重定向仍可解析，但属于**会随上游再改名而断的地址**。

**版本门现状**：`minDshVersion` 全仓只被赋值与当字符串校验，**无任何比较逻辑**（grep 命中：`src/engine.ts:1448`、`src/author.ts:370`、`src/index.ts:180`、`src/capsule.ts:222,231`，以及测试里的字面量）。0.1.2 的 `dshVersion` 还是**硬编码常量** `'0.0.1-rc.2'`（[src/index.ts:151-152](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/index.ts#L151-L152)），不是运行时探测。唯一的版本检查是 dev 脚本 `scripts/check-compatibility.mjs`，它 `git rev-parse` 一个**兄弟目录快照**（默认 `../test-icetomoyo`）并比对 `compatibility.json`，与本机实际加载的宿主无关。

## DOC

`[DOC]` 只证明作者主张，不证明实现。

| 主张 | 出处 | 备注 |
|---|---|---|
| 不替换原生 workflow 工具，而是"更高一层的流程产品能力：命名、发现、生成、复用、暂停/恢复、重跑/续跑、持久证据、成本记录和治理" | [README.md:24](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/README.md#L24) | 与卡片"明说不替换"一致 |
| run 目录结构：`run.json` / `events.jsonl` / `workflow.workflow.json` / `results/` / `artifacts/` | [README.md:127-133](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/README.md#L127-L133) | 与源码一致 |
| **`resume-run`：相同调用序号 + 相同 task input 命中缓存，其余任务继续执行**（即"重跑+回放"，不是断点续跑） | [README.md:137](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/README.md#L137) | 作者自己就这么写 |
| `runAgent` 普通失败返回 `null`；object JSON Schema 任务原生 capture 缺失时只做**一次**同路由、无工具修复，仍不合规则失败 | [README.md:102](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/README.md#L102) | 源码一致（见 SRC-TARGET §5） |
| 后台 run 用 Session 生命周期事件，启动它的 step/turn 结束后仍保持 `running`，直到真正 `run-end` | [README.md:139](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/README.md#L139) | 实现为叠加的 `turn:null`，见 SRC-DSH |
| trusted-local `.ts` 走 Node 原生 erasable-syntax 剥离，**遵循 Node 模块缓存，改完要重启 DSH**；`.mjs/.js` 才热更 | [README.md:225](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/README.md#L225) | 与 `catalog.ts:137` 一致 |
| `force` 只用于"**重启后**的非终态 stale 记录" | [docs/SECURITY.md:35](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/docs/SECURITY.md#L35) | 作者自己承认重启会留 stale 记录（即不会自动收尾） |
| 不修改 agent loop，也不替换 `ctx.workflows`；新增 `ctx.dynamicWorkflows` | [docs/ARCHITECTURE.md:5](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/docs/ARCHITECTURE.md#L5) | 与 `service.ts:74` 一致 |
| 静态拒绝清单 | [docs/SECURITY.md:14](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/docs/SECURITY.md#L14) | 文档不数数，卡片数成 13 |
| "Pause gates future launches; stop aborts and disposes active children" | [docs/KODAX_PARITY.md:25](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/docs/KODAX_PARITY.md#L25) | 源码一致 |
| 部署信号量"由同一次插件服务拥有的所有 run 与 project engine 共享" | [docs/ARCHITECTURE.md:45](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/docs/ARCHITECTURE.md#L45) | 源码一致；边界是"一次服务"，非跨进程 |
| 接线：只声明 `dsh.bundle.patch` | [package.json](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/package.json)、[cordis.patch.yml](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/cordis.patch.yml) | 只有一条 `insert: id: dsh-external-workflow`；无 client 字段 |

## SRC-TARGET

固定点：`44b83c1`。以下行号均指向该 commit 的 `blob`。

### 1. 是引擎还是约定层？

**两者都是，但都不是卡片暗示的那种东西。** 它没有 DAG/schema：`src/types.ts` 里没有 node/edge/dag 任何类型（grep 空），编排词汇是 `phase`/`spawnAgent`/`runAgent`/`parallel`/`pipeline`/`synthesize`/`workflow`（[src/engine.ts:889-998](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L889-L998)），控制流由一段受限 JS 在 QuickJS 里跑出来。但它**不是薄约定层**：自带 run 管理器（`DynamicWorkflowEngine`）、落盘 store、两级信号量、token 账本、审批、沙箱、三工具一命令一 prompt 段（[src/index.ts:585-680](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/index.ts#L585-L680)）。

准确表述：**一个挂在 `ctx.subagents` 之上的"运行态 + 治理"层，用受限脚本表达控制流**；"engine"指 run/资源/状态管理，不是编排图引擎。

### 2. 状态建模与落盘位置

- 运行态：`MutableRun`（内存）持有 `snapshot`（`WorkflowRunSnapshot`）、`controller`、`writer`、`tasks`、`pauseWaiters`、`reservedTokens`/`spentTokens`、`cacheOccurrences`、`nativeSession`（[src/engine.ts:552-568](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L552-L568)）。
- 状态机：run = `running|paused|completed|failed|denied|stopped`；task = `running|completed|completed_unverified|failed|stopped`（[src/types.ts:22-23](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/types.ts#L22-L23)）。
- 落盘：`.dsh/workflow-runs/<runId>/`（默认，可配 `runDirectory`）内含 `run.json`、`events.jsonl`（append-only）、`workflow.workflow.json`+`script.js`+`manifest.json`（不可变胶囊快照）、`results/<hash>-<n>.json`（内容键结果缓存）、`artifacts/`（[src/store.ts:87-133](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/store.ts#L87-L133)）。
- **分区**：store 与 engine **按 `cwdOf(agent)` 各建一份**（`service.ts:279-311`），所以同一个工作目录下的多个会话共享同一批 run；`runDirectory` 配绝对路径时再加 `projectPartitionKey(cwd)` 与 `.project.json` 归属标记（[src/service.ts:302-311](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/service.ts#L302-L311)）。**无跨进程锁**：写入是 `writeFileSync`/`appendFileSync`，只有归属检查，没有 flock。[SRC-TARGET]

### 3. 步骤如何派发

**不派发工具，不派发"步骤"——派发子代理。** 每个 `wf.runAgent/spawnAgent` 最终落到 `ctx.subagents.start(provider, request)`；只有带 `target`/`effort` 时走可选 `dispatch` 适配器（[src/engine.ts:1113-1132](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L1113-L1132)）。请求里带 `prompt`（`taskPrompt` 生成）、可选 `outputSchema`、只读时 `toolFilter`（默认允许 `read/read_image/glob/grep/lsp/skill/web_search`，并排除 `run_code`，[src/engine.ts:318-325](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L318-L325)）。

准入在派发前判定：`maxAgents` 取 `min(manifest.maxAgents, config.maxAgents)`、readOnly 清单不得派写子代理、provider 必须声明 `toolFilter`/`outputSchema` 能力，否则**子代理根本不会启动**（[src/engine.ts:467-486](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L467-L486)）。

### 4. pause / resume / retry / cancel

| 语义 | 实现 | 边界 |
|---|---|---|
| pause | 只改内存 `snapshot.status='paused'` 并 emit；后续任务在 `waitAdmission()` 的 while 循环上挂起；已排队等信号量的任务在拿证后再检一次 pause（[engine.ts:604-610](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L604-L610)、[849-853](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L849-L853)、[1070-1072](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L1070-L1072)） | 只挡"尚未发布"的任务；**已在跑的子代理不会暂停** |
| resume | 只对**内存里**且状态为 paused 的 run 有效：放行 waiters（[engine.ts:612-620](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L612-L620)） | 非 live run 直接 `return false` |
| retry | **没有任务级自动重试**。仅两类有界"修复"：① structured output 失败后**一次**同 provider、`toolFilter:{allow:[]}`、15s 超时的重排（[engine.ts:1167-1216](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L1167-L1216)）；② verification hard 模式下 **3 次评估、至多 2 次 `followup()` 修复**，第 3 次仍不过就抛 `agent verification failed`（[engine.ts:1274-1319](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L1274-L1319)） | 幂等靠缓存+artifact，不靠重试 |
| cancel | run 级 `controller.abort()` + 逐个 `localAgent.cancel({kind:'parent'})` + `dispose()`（[engine.ts:622-636](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L622-L636)）；任务级 `wf.stop(taskId)` | 语义是"停"，不是"回滚" |

`runAgent` 对失败/停止返回 `null`（[engine.ts:903-912](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L903-L912)），控制类错误（stop/token 超限等）才向上抛——所以脚本能否降级，取决于作者有没有判空。

### 5. 崩溃/重启

- **丢的是控制面**：`runs` 是 `Map`，进程没了就没了（`this.runs.set` / `finish` 里 `this.runs.delete`，[engine.ts:568](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L568)、[704](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L704)）。重启后 `pause/resume/stop` 对这些 run 全部返回 `false`，飞行中的子代理无人认领。
- **不丢的是记录**：`run.json` 会停在最后一次持久化的状态（可能是 `running`）；`list()` 把磁盘快照并进来（[engine.ts:576-580](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L576-L580)、[src/store.ts:151-162](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/store.ts#L151-L162)），于是界面上会出现"永远 running"的僵尸记录，只能 `--force` 删（`delete` 对非终态 run 默认拒绝，[store.ts:184-189](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/store.ts#L184-L189)）。作者在 `SECURITY.md:35` 承认这一点。
- **唯一恢复路径**：`rerun`（新 runId，`resumedFromRunId`）或 `resume-run`（同上 + 缓存回放），从磁盘**不可变胶囊**重新执行整段脚本（[src/service.ts:188-210](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/service.ts#L188-L210)、`types.ts:367`）。
- **缓存只回放"算出来的答案"**：写入条件 = `status==='completed'` 且无 warning（[engine.ts:1342](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L1342)）；读取只认**一个** prior runId、且要求对方 `completed` 且无 `verificationWarnings`（[store.ts:120-130](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/store.ts#L120-L130)）；键 = manifest+source+runtime 版本+routing+input 的 sha256，再叠"调用序号"（[engine.ts:1019-1030](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L1019-L1030)）。**副作用（写文件、发消息）不会回放，也不会回滚**。
- 正常卸载走 `ctx.effect` → `disposeAll()` → 把在跑的 run 逐个 `stop`（[src/service.ts:79](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/service.ts#L79)），这是"优雅停机"，不能当崩溃恢复用。

### 6. 完成/质量门

四层，全部在**任务级**，run 级只看脚本是否抛错：

1. 结构化输出：有 `outputSchema` 且校验不过 → `failed`（除非修复成功）（[engine.ts:1217-1226](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L1217-L1226)）。
2. verification：read 路径被真读过、mutation 工具调用**且** workspace 指纹变化、requiredChangedPaths 真变、`minFinalTextChars`、拒收"我准备…"式预告收尾、可挂外部 `verification` 适配器；hard 模式不过即抛（[engine.ts:1272-1334](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L1272-L1334)）。非只读任务默认 `enforcement:'warn'`（[engine.ts:1090](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L1090)）——**默认是警告不是拦截**。
3. 有 warning 的完成降级为 `completed_unverified`（[engine.ts:1335](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L1335)），不进缓存。
4. run 级投影 `completed|partial|failed|interrupted`，`partial` = 有未 resolve 的任务（[engine.ts:828-834](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L828-L834)）。**没有"质量分"或"必须全绿"的 run 级门**。

artifact 独占：同名二次写直接抛错，且落盘用 `flag:'wx'`（[store.ts:103-109](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/store.ts#L103-L109)）。token：开工前 `reservedTokens += allocation`，结束后 `-=` 并按实测 usage 记账，修复阶段还会补差（[engine.ts:1082-1088](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L1082-L1088)、[1151-1152](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L1151-L1152)、[1228-1232](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L1228-L1232)）。嵌套 workflow 复用同一个 run 的 semaphore/`totalSpawned`/budget，只限一层（[engine.ts:961-967](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L961-L967)）。

### 7. 与宿主会话的关系

- 事件写进**调用方 agent 的会话**（`nativeSession: input.parent.session`，[engine.ts:566](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L566)）：`tool-workflow/run-start`（会话级，`turn:null`）、`tool-workflow/agent-start`、`tool-workflow/agent-end`、`tool-workflow/run-end`（[engine.ts:642](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L642)、[703](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L703)、[1139-1144](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L1139-L1144)、[1344](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L1344)）。子代理自己仍是 DSH 的 subagent 会话。
- `run_workflow` **默认不阻塞**：`wait` 默认 false，直接返回 `{runId,status,jobId}`，并尽量挂到 `ctx.jobs`（kind `workflow`），失败则退回插件自有 run id（[index.ts:169-175](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/index.ts#L169-L175)、[service.ts:244-263](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/service.ts#L244-L263)）。
- 审批分两条：工具路径走 `ctx.approval.request({toolName:'run_workflow'})`（[engine.ts:645-653](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/engine.ts#L645-L653)），命令路径走 `ctx.userQuestions`（[service.ts:235-242](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/service.ts#L235-L242)）；`trusted-local` 另加一次显式确认（[service.ts:120-133](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/service.ts#L120-L133)）。
- 三工具一命令一 prompt 段：`workflow_list` / `run_workflow` / `workflow_manage` + `/workflow` + `systemPrompt.section('tool:dynamic-workflows', order 116)`（[index.ts:585-680](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/index.ts#L585-L680)）；只 `inject:['subagents','tools']`（[index.ts:36](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/index.ts#L36)）。

### 8. 沙箱与静态策略（卡片两个数字要改）

- `FORBIDDEN` 是 **12 条**正则（import / require / process / fs / child_process / exec|spawn / network / Deno|Bun / timers / globalThis[ / __dsh* / eval|Function|.constructor|__proto__），[src/source-policy.ts:13-25](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/source-policy.ts#L13-L25)；另有第 13 条**非常规**检查（`['constructor']` 字符串下标，[第 84 行](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/source-policy.ts#L84)）。
- `node:vm` 的 `new Script(...)` 只做**编译/语法检查**，不执行（[source-policy.ts:90](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/source-policy.ts#L90)）；真正执行在 `quickjs-emscripten` 的 WASM 堆（[runtime.ts:1](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/runtime.ts#L1)、[265-266](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/runtime.ts#L265-L266)）。"双保险"= 正则 + 独立堆，成立。
- 胶囊格式：`format` 必须 `dsh.workflow`、字段精确白名单（`format/version/workflowApiVersion/minDshVersion/manifest/source/intent/inputs/requires/provenance`），任何外来格式/多余字段在执行前 TypeError（[capsule.ts:220-243](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/src/capsule.ts#L220-L243)）。**代码里没有任何 "KodaX 格式" 分支**——卡片说的"拒收 KodaX 格式"是从白名单反推的，不是显式实现。

## SRC-DSH

本机 `@deepseek-ai/dsh` = **0.2.1-rc.3**（`/Users/bowhead/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh`）。

| 宿主契约 | 本机事实 | 与目标的关系 |
|---|---|---|
| 原生 workflow 服务 | `@deepseek-ai/dsh-workflow` 0.2.1-rc.3：`export declare abstract class WorkflowEngine extends Service`（`lib/types/index.d.ts:111`） | 证实"原生 `ctx.workflows` 存在"，插件确实只是叠一层 |
| Session 事件 | `@deepseek-ai/dsh-tool-workflow` 0.2.1-rc.3 `lib/types/types.d.ts:10`：`ToolWorkflowRunStartData = { runId; name }`——**没有 `turn` 字段**；同文件 `39` 行把它挂进 `SessionEventMap` | 插件却写 `{runId,name,turn:null}` 并靠手写类型断言绕过（`engine.ts:304-316`）。**在当前宿主上这是超集字段**：能跑是因为 `Session.append` 未校验载荷，是否有渲染/校验副作用 → `[OPEN]` |
| subagent seam | `@deepseek-ai/dsh-subagent` 0.2.1-rc.3（插件按 `SubagentRuntime.start(provider, request)` 使用） | 与插件调用点一致；未运行验证 |
| peer 版本范围 | 插件 `peerDependencies` 全部写 `^0.0.1-rc.2`（`@deepseek-ai/dsh-workflow` 等），**未声明 `engines.dsh`**；且 `@deepseek-ai/dsh-tool-workflow` 既不在 peer 也不在 devDeps（只 `import type`） | `^0.0.1-rc.2` 与宿主 `0.2.1-rc.3` 不在同一 semver 段。按 DSH 安装门（未满足的 peer 会阻断）**可能装不上**；本轮未安装 → `[OPEN]`，但这是跨宿主版本最该先验的一条 |

## TEST

`[TEST]` 只证明覆盖意图，不证明通过。固定点 `44b83c1` 有 **11 个 vitest spec**、约 **113 个 `it(` 用例**（grep 计数，未运行）：`author` 11 / `builtins` 3 / `capsule` 3 / `catalog` 7 / `engine` 31 / `plugin` 31 / `runtime` 9 / `scoped-review` 7 / `service` 5 / `source-policy` 3 / `store` 3。运行方式 `pnpm test`（`vitest run`），另有 `test:coverage`、`typecheck`、`check:compatibility`（[package.json scripts](https://github.com/omdsh-dev/dsh_workflow/blob/44b83c182aa02d1be8a0803e8446cb495f93cd8f/package.json)）。

覆盖点与卡片主张相关的是 `engine.spec.ts`（pause/resume/stop、cache、verification、token）与 `plugin.spec.ts`（工具/命令/会话事件），但**没有任何崩溃重启测试**（grep 无 restart/crash 用例），与"不是断点续跑"一致。

## CI

**无。** `44b83c1` 的 tree 共 81 项，**没有 `.github/`**；GitHub `/actions/workflows` → `total_count: 0`；`v0.1.4` tarball 同样无 `.github/`。`[CI]` 无同 SHA 结果可引。发布靠手工 tag（`chore: release v0.1.x`），`v0.1.4` 甚至没有 GitHub Release。

## RUN

`[RUN] None`。本轮只做 HTTP 读取：GitHub REST（repo/tags/commits/compare/tree/actions/releases）、`codeload` tarball 解到 `/tmp/wfaudit.cakr79` 只读、npm registry HEAD。**未 install / 未 build / 未 run / 未加载插件**。

## 卡片偏差表

| 卡片断言 | 源码事实（`44b83c1`） | 判定 |
|---|---|---|
| `0.1.2` 为本次读的版本 | `package.json` 确为 `0.1.2`，但**不存在 v0.1.2 tag**；仓库已有 `v0.1.3`/`v0.1.4`（最新 2026-09-05），`main` 落后 4 个提交 | **部分偏差**：版本号对，但"最新"错，卡片未记 tag |
| npm 未发布（404） | 一致（404）；另 `dsh-workflow`（无 scope）是**无关包**（作者 dushaobindoudou） | 一致 |
| "仓库名与安装路径不一致…两者不是同一 owner…去确认哪个是活的" | `dsh-external/dsh_workflow` **301 重定向**到同一 repo id `1332243516`，是**改名**不是两个 owner；旧名只留在 `package.json` 元数据里 | **偏差**：警告方向对、归因错，且"哪个是活的"已有确定答案 |
| "13 类 FORBIDDEN 静态正则" | **12 条**正则 + 1 条字符串下标检查（`[84]`）+ 一次 `vm.Script` 编译检查 | **偏差（数字）** |
| "QuickJS/WASM 独立堆" | 属实；`node:vm` 只编译不执行 | 一致（卡片未提 vm 只是编译） |
| 不可变胶囊 + 内容键缓存 = 可复现 | 属实；缓存写入/读取条件比卡片更严（干净 completed 才写；只认单个 prior runId） | 一致 |
| "进程重启后活跃 run 丢失" | **控制面丢、记录不丢**：磁盘留 stale `running`，pause/resume/stop 全部 false，需 `--force` 清理；作者自己在 SECURITY.md 承认 | **部分偏差**：方向对，粒度不准 |
| "verification hard 修复至多 3 轮" | 3 次评估、**至多 2 次** followup 修复，第 3 次不过即抛 | **偏差（差一）** |
| "结构化输出最多 1 次同路由无工具修复" | 属实（`toolFilter:{allow:[]}`、15s、同 provider） | 一致 |
| "无自动重试，幂等靠缓存 + artifact 独占写" | 属实（无任务重试；artifact `flag:'wx'` + 重名抛错） | 一致 |
| `minDshVersion` "存了但全仓无比较逻辑" | 属实；且 0.1.2 的 `dshVersion` 是**硬编码 `'0.0.1-rc.2'`**，不是宿主探测；唯一检查是 dev 脚本比对兄弟目录 snapshot | 一致（卡片低估了严重度） |
| "全服务共享一个 maxConcurrency 部署信号量" | 属实（service 级 `deploymentSemaphore`）；边界=一次插件加载，**非跨进程** | 一致 |
| "多进程共用绝对 runDirectory 无锁" | 属实（只有 `.project.json` 归属标记，无 flock） | 一致 |
| "嵌套 workflow 与父共享 maxAgents/token 配额" | 属实（同 run、同 semaphore、同 `totalSpawned`、同 budget，限一层） | 一致 |
| "仅 `dsh.bundle.patch` → `cordis.patch.yml`（无 client 注入）" | 属实（单条 insert，无 client 导出/字段） | 一致 |
| "明说不替换原生 `ctx.workflows`" | 属实（ARCHITECTURE:5；新增的是 `ctx.dynamicWorkflows`） | 一致 |
| "三级信任 + 字段精确白名单 + 拒收 KodaX 格式" | 三级信任与白名单属实；**"拒收 KodaX"无显式代码**，是白名单的副作用 | 部分偏差（表述） |
| "trusted-local `.ts` 走 Node 模块缓存，不热更" | 属实（`.js/.mjs` 加 `?mtime=`，`.ts` 不加） | 一致 |
| "153★ / 11 fork" | 2026-11-01 为 **154★ / 11 fork** | 采样漂移，不算错 |
| 未提 | `run_workflow` 默认**不阻塞**（`wait` 默认 false，挂 `ctx.jobs`）；`workflow_manage` 才有 pause/resume/stop | **遗漏**：影响"谁来等 run"的判断 |

## [OPEN]

1. **崩溃后子代理与其副作用如何收尾**：源码无 reaper、无 lease、无心跳；重启后飞行中子代理是否被宿主回收、半写文件是否留下，未验证 → `[OPEN]`。
2. **`turn:null` 是否被当前宿主接受**：0.2.1-rc.3 的 `ToolWorkflowRunStartData` 无 `turn` 字段；插件用类型断言写入。是否被 Session 校验/渲染忽略，未运行 → `[OPEN]`。
3. **peer `^0.0.1-rc.2` vs 宿主 `0.2.1-rc.3`**：是否会阻断 `dsh plugin add`，未安装 → `[OPEN]`（也是这本书该先验的一条）。
4. **0.1.4 是否改了机制**：`src/` 与固定点只差两行常量，判断"结论可外推到 v0.1.4"；但 `lib/` 由 `tsc` 生成、`pnpm-lock` 有 509 行变动，**未验证发布物与源码字节一致** → `[OPEN]`。
5. **真实并发/缓存命中/成本**：卡片与 README 都无实测数字，本轮也未跑 → `[OPEN]`。
