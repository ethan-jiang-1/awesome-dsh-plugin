---
title: "11 · february2015/dsh-taskswarm 源码复核"
domain: agent-pipelines
kind: evidence
positioning: "对 0.2.38 固定提交的复核：每 lane 一个 worktree + 常驻 _orch，lane 走 DSH agent 分发；失败保留但重跑/abort 会清；npm 正式名已整包下架。"
read_when: "核对 11 卡的 worktree/失败保留/状态归属，或复核 npm 坐标与崩溃恢复。"
status: observed
updated: 2026-11-01
---

# 11 · `february2015/dsh-taskswarm` 源码复核

> 复核对象：样本卡 [`11-february2015-dsh-taskswarm.md`](../samples/11-february2015-dsh-taskswarm.md)。
> 取证时点 2026-11-01（UTC+08:00）。**未安装、未构建、未运行 `npm test`、未启动宿主或插件**；只读 GitHub REST、npm registry、`git clone --depth 100` 的本地副本与 registry tarball 的只读解包，另用两个一次性 `/tmp` 仓库做 git 语义探针（见 RUN）。
> 标签沿用 [`EVIDENCE.md`](../../EVIDENCE.md)：`[DOC]` 目标仓文档主张，`[SRC-TARGET]` 固定 commit 实现，`[SRC-DSH]` 本机 `@deepseek-ai/dsh 0.2.1-rc.3` 发行包，`[TEST]` 测试源码，`[CI]` 同 SHA check-run，`[RUN]` 本轮实做，`[OBS]` 判断。
> **主 pin**：tag `v0.2.38` → commit [`3164995`](https://github.com/february2015/dsh-taskswarm/commit/3164995606fe3e53568b60120fa5318fac0c9698)（2026-08-16T22:57:01+08:00，`package.json` 0.2.38）；默认分支 tip [`032e2c9`](https://github.com/february2015/dsh-taskswarm/commit/032e2c9d228c20cab65fe0ea061d78a7c753ab8c)（2026-08-17T01:08:03+08:00）领先 **5 个提交**，`git diff --stat v0.2.38..032e2c9` 只有 README×2、docs×3、scripts×1 共 6 个文件，**`src/` 与 tag 树逐字节相同**。下文代码行号一律 pin `032e2c9`（与 tag 同树）。
> 一句话结论：**「每 lane 一个 worktree」与「merge 失败保留现场」都成立**，且 lane 不是另开进程，而是**每 lane 一个 DSH agent 会话**（`origin:'subagent'`，cwd=worktree，模型可按 lane 覆盖）；但卡片的绝对措辞有三处要改：**abort/插件卸载会删掉所有 lane worktree**、**同 taskId 重跑会先 `worktree remove --force` 再附着分支**、**npm 正式包 `dsh-taskswarm` 已于 2026-08-16 整包下架，卡片给的安装命令必然 404**。

## Provenance

| 项 | 值 | 核对方式 |
|---|---|---|
| 仓库 | [`february2015/dsh-taskswarm`](https://github.com/february2015/dsh-taskswarm)（id `1333800488`，创建 2026-08-14，MIT，**3★** / 0 fork / 0 open issue @2026-11-01，默认分支 **`master`**，`pushed_at` 2026-08-16T17:08:07Z，size 1537 KB） | `/repos` |
| **主 pin** | tag `v0.2.38` 是**轻量 tag**（`/git/ref/tags/v0.2.38` → `object.type=commit`），指向 [`3164995`](https://github.com/february2015/dsh-taskswarm/commit/3164995606fe3e53568b60120fa5318fac0c9698)（2026-08-16T22:57:01+08:00，`fix(supervisor): stalled 判断加入 step 增长…（0.2.38）`） | `/tags`、`/git/ref` |
| 默认分支 tip | [`032e2c9`](https://github.com/february2015/dsh-taskswarm/commit/032e2c9d228c20cab65fe0ea061d78a7c753ab8c)（2026-08-17T01:08:03+08:00，`revert: 放弃临时包名方案…`）；tag 之后共 5 个提交，全部是 docs/scripts | `git log`、`git diff --stat` |
| package.json | version `0.2.38`（[package.json:3](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/package.json#L3)）；`main: lib/orchestrator/index.js`（[:23](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/package.json#L23)）；`bin.taskswarm-dashboard`（[:76-78](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/package.json#L76-L78)）；`dsh.bundle.patch`（[:71-74](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/package.json#L71-L74)） | 本地 clone |
| **npm 正式名 `dsh-taskswarm`** | **整包已下架**：`time` 记录 **38 个已发布版本**（0.2.1–0.2.38），其中 `0.2.2`/`0.2.3`/`0.2.32` 不进最终下架名单（`time` 仍留发布时间戳，**推断**为更早被逐版本删除），**2026-08-16T15:24:26Z** 的整包下架清掉其余 **35** 个；文档无 `versions`、无 `dist-tags`，只剩 `unpublished` | `registry.npmjs.org`（200，仅 unpublished 记录） |
| **npm 临时名 `dsh-taskswarm2`** | **存在**：唯一版本 `0.2.38`，2026-08-16T15:26:05Z 发布，`gitHead = d589109d973424b6467b168abc78a5cf51984244`；tarball 解包含 `lib/`（46 文件）、`dashboard/`、`docs/`、`templates/`，无 `src/`、无 `tests/` | registry + tarball 只读解包 |
| **npm ↔ tag ↔ commit 对齐** | 正式名不存在 → **无法对齐**。临时名 `gitHead=d589109` **不是** tag 指向的 `3164995`，而是 tag 之后第 1 个提交（`docs(release): 记录 unpublish 需 classic token…`，2026-08-16T23:01:03+08:00）；`git diff --stat v0.2.38..d589109` 只有 `docs/release.md`、`docs/release.zh-CN.md` 两文件 → **代码树相同，但字节级发布物无 tag 可证** | 两棵树对比 |
| **卡片版本核对** | 卡片 L34「版本(本次读) `0.2.38`」= 默认分支 tip 树的自述版本，**不等于任何 npm 发布物**（正式名已删、临时名出自另一个提交（仅 docs 差异））；不 pin 到 `3164995`/`032e2c9` 无法复现 | 同上 |
| 卡片安装命令 | L37 `dsh plugin add dsh-taskswarm` **当前必然失败**（404）；README 自己在 [README.md:3-5](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/README.md#L3-L5) 承认「已整包 unpublish，8/17–8/18 改用 GitHub 安装，8/19 恢复 npm」，但**截至 2026-11-01 并未恢复**，仓库最后提交停在 2026-08-17 | registry + README |
| 发布物缺陷 | 临时名 tarball 的 `cordis.patch.yml` 仍写 `name: 'dsh-taskswarm/orchestrator'`，与实际包名 `dsh-taskswarm2` 不一致（按 Node 解析规则该模块不存在）；未见别名机制 | tarball 内文件 |

## DOC

`[DOC]` 只证明作者主张，不证明实现。

- 拓扑自述：「every task (lane) works in its own worktree; results are merged into the `taskswarm/orch` integration branch」——[README.md:20](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/README.md#L20)；目录示意 `<stateRoot>/worktrees/_orch` 与 `<taskId>`——[README.md:133-134](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/README.md#L133-L134)。
- 失败语义自述：「unresolvable conflicts land the lane in a `conflict` state and pause the batch for supervisor intervention」——[README.md:30](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/README.md#L30)；checkpoint「a crashed worker never loses committed work」——[:22](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/README.md#L22)。
- 崩溃自述：「after a kill/restart you can salvage work, clean up residue, and re-run」——[:27](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/README.md#L27)；「resume/rerun failed lanes through the supervisor without losing completed work」——[:160](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/README.md#L160)；「wave plan is fixed at batch start」——[:161](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/README.md#L161)。
- **`[DOC]` 与实现直接冲突的一处**：「an independent reviewer scores each task **per its `Review Level`**」——[README.md:23](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/README.md#L23)；代码里 `reviewLevel` 只被解析、从不消费（见 SRC-TARGET §5）。
- **KI 文档双语不对称（卡片引用踩空）**：英文 [`docs/known-issues.md`](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/docs/known-issues.md) 只有 **7 条**（KI-008/005/006/004/001/002/003），开头写「OPEN（No open items）」（[:6-8](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/docs/known-issues.md#L6-L8)）；中文 [`docs/known-issues.zh-CN.md`](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/docs/known-issues.zh-CN.md) 有 **8 条**，KI-007 只在中文档——[known-issues.zh-CN.md:29](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/docs/known-issues.zh-CN.md#L29)。
- KI-007 的根因正是卡片说的「`await spawn()` 无超时」：「`runLane()` 第 270 行 `await config.host.spawn(spec)` **无超时**——worker 失联/事件丢失时该 await 永不返回 → execute 卡死在当前 wave」——[known-issues.zh-CN.md:37-40](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/docs/known-issues.zh-CN.md#L37-L40)。
- KI-003 的根因是「stale 内存态整份写」，不是 `updateLane` 之间的 LWW：「`writeBatchState(state)` … writes the **stale in-memory state object** to disk wholesale」——[known-issues.md:262-264](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/docs/known-issues.md#L262-L264)；修复说明「lane persistence now uniformly goes through the per-lane `updateLane`, which is race-free by design」——[:248-251](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/docs/known-issues.md#L248-L251)。
- 运维档对崩溃的口径与代码不一致：`docs/runbook.md` 说「engine's `active` in-memory table is cleared → `pause / resume / abort` all become no-ops」——[runbook.md:63-64](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/docs/runbook.md#L63-L64)，但当前代码的 `resume()` 在 active 为空时会走磁盘恢复（SRC-TARGET §7）；同档也承认「`/tswarm` directly after a crash opens a new batch」——[:491](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/docs/runbook.md#L491)。

## SRC-TARGET

### 1. worktree 拓扑：每 lane 一个，不是每成员

| 事实 | 实现 |
|---|---|
| 集成分支与常驻 worktree | `ORCH_BRANCH = 'taskswarm/orch'`（[worktree.ts:22](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/worktree.ts#L22)）；`worktreesDir = <stateRoot>/worktrees`，`_orch` 常驻（[:30-33](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/worktree.ts#L30-L33)）；分支不存在则 `git branch taskswarm/orch`，目录不存在则 `worktree add -B taskswarm/orch <_orch>`（[:36-50](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/worktree.ts#L36-L50)） |
| 每 lane 一个 worktree/branch | `createLaneWorktree(repoRoot, paths, taskId)` → 分支 `taskswarm/<taskId>`、目录 `<worktreesDir>/<taskId>`（[:58-60](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/worktree.ts#L58-L60)）；新分支以 orch 为基线 `worktree add -b <branch> <dir> taskswarm/orch`（[:78-82](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/worktree.ts#L78-L82)） |
| 已存在分支的续跑 | 附着既有分支 `worktree add <dir> <branch>`，随后在 lane 内 `git merge --no-edit taskswarm/orch`，失败即 `merge --abort`（[:84-89](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/worktree.ts#L84-L89)） |
| 同 taskId 重跑先删旧现场 | 目录存在 → `worktree remove --force`，失败再 `worktree prune`（[:61-67](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/worktree.ts#L61-L67)）。**未提交的改动在这里被丢弃，提交保留在分支上** |
| 成功合并后的清理 | `worktree remove --force` + `branch -d`（[:132-135](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/worktree.ts#L132-L135)） |
| 整批清理 | `removeAllLaneWorktrees()` 只删**非 `_` 前缀**目录（`_orch` 保留）+ `prune`（[:138-152](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/worktree.ts#L138-L152)）；被 `abort()` 调用（[engine.ts:756-770](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L756-L770)） |
| 插件卸载 | `ctx.effect` 的卸载钩子里对每个 engine 调 `abort()` 再回收 dashboard（[index.ts:190-204](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/index.ts#L190-L204)）→ 正常关停同样会删 lane worktree（分支仍在） |

**卡片「每 lane 一个（不是每成员）」判定**：成立。每个 lane 恰好一个 worker；reviewer/merger **不新开 worktree**，reviewer 在 lane worktree 里跑（[reviewer.ts:80-91](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/worker/reviewer.ts#L80-L91)），merger 在 `_orch` 里跑（[merger.ts:48-58](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/worker/merger.ts#L48-L58)）。

**卡片「失败时刻意什么都不清理」判定**：**部分成立**。`mergeLane()` 失败时明确不移 worktree、不删分支、保留 in-progress merge（[worktree.ts:111-131](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/worktree.ts#L111-L131)），注释把「不要用 `branch -D` 销毁 worker 的工作」写成设计理由。但清理会从另外三个口子发生：① `abort`/插件卸载 → §上表；② 同 taskId 重跑 → `worktree remove --force`；③ 成功合并 → 删 worktree+branch。**分支**在 ①② 后都还在（`worktree remove` 不动分支），所以「现场」的可救部分是分支上的 checkpoint，worktree 目录本身不保证。

**一个未在卡上、但会丢 `_orch` 历史的坑**：`ensureOrchWorktree` 用 `worktree add -B taskswarm/orch`。git 对 `-B` 的定义是「create **or reset** a branch」，省略 commit-ish 时重置到当前 HEAD——本地探针原文打印 `Preparing worktree (resetting branch 'taskswarm/orch'; was at 9da62dd)`，重置后该分支只剩 1 个提交（见 RUN）。也就是说：**若 `_orch` 目录丢失（人工清理、`worktree prune`）而 `taskswarm/orch` 分支还在，下一次建 worktree 会把已合并历史重置回主分支 HEAD**，分支上只有 reflog 能捞回。触发条件是目录丢失，不是正常失败路径；标 `[OPEN]` 待运行验证。

### 2. lane 如何被分发到 subagent

- 引擎侧只认 `WorkerHost.spawn(spec)` 这一个 seam（[worker-host.ts:38-50](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/worker-host.ts#L38-L50)）；默认 `host: 'in-process'`（[index.ts:84](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/index.ts#L84)、[:241-252](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/index.ts#L241-L252)）。
- `InProcessWorkerHost.spawn()`：`ctx.agents.create({sessionId: 'session-<uuid>', meta: {cwd: worktree, origin: 'subagent', taskswarmWorker: true}, agentOptions: {provider, model: spec.model ?? 默认}, setup})`（[in-process-host.ts:47-65](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/in-process-host.ts#L47-L65)）。**一个 lane = 一个 DSH agent 会话**，不是进程、不是线程池。
- 派活方式：先 `await agent.whenIdle()`，再 `agent.followup(createUserMessage(buildWorkerMission(...)))`，再 `whenIdle`，用 `turn/end.reason.kind==='completed'` 判定成功（[in-process-host.ts:76-84](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/in-process-host.ts#L76-L84)、[:109-114](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/in-process-host.ts#L109-L114)）。
- 每个 worker 会话挂 5 个桥接工具：`task_runner`（show/advance/done/blocked/amend/log，advance 会 checkpoint 提交）、`review_step`、`notify_supervisor`、`escalate_to_supervisor`、`request_segment_expansion`（[lane-tools.ts:127-332](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/worker/lane-tools.ts#L127-L332)）。
- 权限注入：`grantWorkerFullAccess` + `mountStandardTools` 在 setup 里执行（[in-process-host.ts:56-64](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/in-process-host.ts#L56-L64)、[worker-tools.ts:47-68](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/worker/worker-tools.ts#L47-L68)），后者向会话 append `sandbox/mode=danger-full-access`、`approval/policy=never`（[worker-tools.ts:80-91](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/worker/worker-tools.ts#L80-L91)）。
- 关键区别：**没有 `parentAgent`**（对比 `[SRC-DSH]` 的 subagent 运行时调用会传 `parentAgent`），所以这些会话是「标了 `origin:'subagent'` 的一等会话」，不进入 DSH 的 subagent 委派记账/深度限制/取消语义；关停靠 `handle.dispose()`（[in-process-host.ts:85-94](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/in-process-host.ts#L85-L94)）与 `agent.cancel?.()`（[:103-106](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/in-process-host.ts#L103-L106)）。
- headless 备选：每 lane `spawn('dsh', ['--profile', <workerProfile>, mission], {cwd: worktree, env: TASKSWARM_WORKER_*})`（[worker-host.ts:56-115](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/worker-host.ts#L56-L115)）；注意默认 profile 名两处不一致：`worker-host.ts:64` 写 `taskswarm-worker`，`index.ts:245` 传 `tswarm-worker`（实际生效后者）。
- 同一波内并发是 `Promise.all(wave.map(runLane))`（[engine.ts:297](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L297)），**没有并发上限配置**。

### 3. 状态归属：lane 元数据住在哪

| 状态 | 所有者 | 位置 | 依据 |
|---|---|---|---|
| 批次 + 每 lane 的 phase/worktree/error/log、`wavePlan`、`pausedBy` | 引擎（单写者，进程内） | `<repoRoot>/.taskswarm/batches/<batchId>.json`（`stateRoot` 默认 `join(repoRoot,'.taskswarm')`，[index.ts:237-239](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/index.ts#L237-L239)） | `LaneState`/`BatchState` 定义与读写（[status.ts:16-95](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/status.ts#L16-L95)） |
| 任务步骤进度 | 任务包（主仓，**不在 worktree 内**） | `tasks/<ID>/STATUS.md` 复选框、`.DONE` 标记 | `markTaskDone` 写 STATUS + `.DONE`（[task.ts:462-466](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/task.ts#L462-L466)）；`parseStatusFile` 读 `.DONE`（[:251](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/task.ts#L251)） |
| 评审结论 | worker 会话写文件 | `tasks/<ID>/.reviews/R###-*.md` + `.seq` | `review_step` 写文件（[lane-tools.ts:229-249](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/worker/lane-tools.ts#L229-L249)）；引擎读最新文件判 PASS/REVISE（[engine.ts:645-654](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L645-L654)） |
| 工蜂→蜂王消息 | 文件邮箱 | `<stateRoot>/mailbox/<batchId>/supervisor/inbox/*.json`（tmp+rename 原子写，ack 移入 `_ack/`） | [mailbox.ts:32-50](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/mailbox.ts#L32-L50)、[:71-93](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/mailbox.ts#L71-L93)、[:114-140](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/mailbox.ts#L114-L140) |
| 代码产出 | worker（每 lane 一个分支） | `taskswarm/<taskId>` 分支 + checkpoint 提交；合并进 `taskswarm/orch` | [worktree.ts:97-109](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/worktree.ts#L97-L109)、[lane-tools.ts:161-185](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/worker/lane-tools.ts#L161-L185) |
| 编排器内存态 | 进程 | `active`、`batchOwners`、`pausedOnFailureBatch`、`laneModelOverrides`、`mergeQueue` | [engine.ts:99-114](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L99-L114)；**崩溃即丢**，而 `pausedOnFailureBatch` 会改变 resume 语义 |
| dashboard 偏好 | dashboard 进程 | `<stateRoot>/dashboard-preferences.json` | [history.mjs:58](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/dashboard/history.mjs#L58)、[:233-235](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/dashboard/history.mjs#L233-L235)、[:317-321](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/dashboard/history.mjs#L317-L321) |
| 每仓库一个引擎 | 插件进程 | `engines: Map<repoRoot, EngineRef>`，多会话共享 | [index.ts:227-239](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/index.ts#L227-L239)、[:334-336](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/index.ts#L334-L336) |

**第二真相源的准确位置**（卡片只说「内存态与盘上状态并存」，其实至少三处）：① 引擎内存里的整份 `state` 与磁盘 `updateLane` 写并存——KI-003 的主因，已按注释移除 lane 启动时的整份写（[engine.ts:421-425](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L421-L425)），但**波次边界仍写整份**（[:298-320](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L298-L320)），`stopLane`（[:806](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L806)）与 `switchLaneModel`（[:844](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L844)）也写整份；② STATUS.md/.DONE 是任务进度真源，与 batch JSON 的 lane phase 无事务关系；③ `.reviews/` 文件是评审真源，`readLatestVerdict` 只取最后一份文件。

### 4. 冲突隔离：worktree 隔离到哪一层

- **代码工作区隔离**：每 lane 独立 worktree + 独立分支，起点是创建时刻的 `taskswarm/orch` HEAD（[worktree.ts:78-82](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/worktree.ts#L78-L82)）。同波的两个 lane **互相看不见对方**，冲突只在回合并时出现。
- **合并串行**：orch 里的 `git merge` 用 promise 链串行化（`serializedMerge`，[engine.ts:108-124](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L108-L124)、[:506](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L506)），避免并发 `git merge` 被 git 锁拒绝。这是卡片没写、但真实存在的一层「裁决」。
- **冲突升级链**：`mergeLane` 失败 → 若 host 实现 `spawnMerger` 则起 merger agent（默认在 `_orch` 里解冲突）→ 成功则删 lane worktree+branch 并标 merged；失败/超时（默认 10 分钟，[engine.ts:517](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L517)）则 lane 标 `conflict` 并保留现场（[:541-566](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L541-L566)），波次结束自动暂停（[:333-349](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L333-L349)）。
- **隔离的边界**：lane 之间共享同一个 `.git` 对象库与 refs；**任务包（PROMPT/STATUS/.reviews/.DONE）在主仓 `tasks/`，不在 worktree 内**——KI-005 记录过 worker 直写这些文件触发沙箱审批（[known-issues.md:28-50](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/docs/known-issues.md#L28-L50)），修复方式是给 worker 会话开 full-access，而不是把任务包搬进 worktree。所以「物理上不共享」只对**代码树**成立。
- **一个可证伪的假成功路径**（同一波两个冲突时）：lane A 合并失败后 `_orch` 停在 `MERGE_HEAD=A` + 未合并文件；lane B 的 `mergeLane` 会被 git 拒绝（本地探针原文：`error: Merging is not possible because you have unmerged files.`），引擎把这次 `!ok` 当「lane B 合并失败」交给 merger（[engine.ts:512-527](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L512-L527)）；而 merger 的 prompt 断言「A lane `git merge` of branch B is in progress」（[merger.ts:91-97](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/worker/merger.ts#L91-L97)），实际在解的可能是 A 的冲突。若 merger 报 `CONFLICT_RESOLVED`，引擎直接删 B 的 worktree、`branch -d B`（unmerged 时 git 会拒绝删除，分支侥幸留命）并把 lane B 标 `merged`（[:541-547](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L541-L547)、[:561](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L561)）——**B 的提交其实没进 orch**。此路径为源码推断，触发需同波先后冲突，标 `[OPEN]`。

### 5. reviewLevel 与评审的可跳过性

- `reviewLevel` 在 `parsePrompt` 里解析（默认 2）——[task.ts:173](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/task.ts#L173)；全仓 grep 只有类型声明 [:54](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/task.ts#L54) 与这一处，**没有任何消费方**。
- 评审是 worker **自愿调用**的工具：`review_step` 由 worker 主动调（[lane-tools.ts:211-256](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/worker/lane-tools.ts#L211-L256)），引擎在 lane 收尾时只读 `.reviews/` 最新文件；**没有评审文件时 `verdict='none'`，直接进合并分支**（[engine.ts:491-508](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L491-L508)）。卡片「reviewer 可被实现者跳过」成立。
- reviewer 自己的 verdict 解析是「有 REVISE 就 REVISE，否则 PASS」（[reviewer.ts:106](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/worker/reviewer.ts#L106)）；reviewer 抛错时 `review_step` 返回 REVISE（fail-closed，[lane-tools.ts:250-253](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/worker/lane-tools.ts#L250-L253)），但 REVISE 只把 lane 置 `review`，**不触发暂停**（暂停条件只看 `conflict` 与 `failed`，[engine.ts:337-339](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L337-L339)），批次可以带着 `review` lane 走到 `complete`。收敛语义见下节。
- 文档宣称与实现冲突：README:23「per its `Review Level`」。

### 6. 失败 / 重试收敛

| 失败种类 | 当时行为 | 之后怎么收敛 |
|---|---|---|
| worktree 建不出来 | lane 立即 `failed`，error=`could not create lane worktree`（[engine.ts:437-443](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L437-L443)） | 该波出现 failed → 自动暂停（默认 `pauseOnLaneFailure=true`，[index.ts:92](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/index.ts#L92)）；resume 时**跳过 failed lane（丢弃）**，靠 `pausedOnFailureBatch` 记忆（[engine.ts:692-701](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L692-L701)） |
| worker 非 0 退出 / 任务未标 done | lane `failed`，error 记原因（[engine.ts:494-500](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L494-L500)） | 同上；重跑该 taskId 时附着旧分支、在 lane 里先 merge orch（冲突则 abort），worker 从 STATUS 下一步继续 |
| worker 失联（KI-007） | 看门狗 `laneTimeoutMinutes`（默认 **180**）到点 `host.abort` + failed，worktree/分支保留（[engine.ts:605-638](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L605-L638)） | 看门狗触发前先查磁盘终态，已被人工收尾则跳过（[:613-627](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L613-L627)）；`0`=禁用 |
| 合并冲突 | 现场保留 + merger agent；未解决 → `conflict` + 暂停（[engine.ts:506-566](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L506-L566)） | 冲突 lane 无自动重试；要人/merger 先解掉 `_orch` 的 in-progress merge 才能再合并（代码里**没有任何 `merge --abort`**，merger prompt 还明令禁止 abort，[merger.ts:118-122](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/worker/merger.ts#L118-L122)） |
| 评审 REVISE | lane `review`，不合并（[engine.ts:500-503](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L500-L503)） | **不自动重跑**；靠 supervisor 收到 `lane-revise` 事件（除 `lane-done` 外都唤醒，[supervisor.ts:213-215](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/supervisor.ts#L213-L215)）后人工处置；恢复时 `review` 不算 merged → 会重跑 |

收敛的硬事实：**重试次数没有上限、没有退避、没有 attempt 计数**；`lane.log` 只保留 200 行（[status.ts:111-114](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/status.ts#L111-L114)）。「失败即暂停」把决定权交回 supervisor（`tswarm_supervisor_control`，[supervisor.ts:619-736](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/supervisor.ts#L619-L736)），这是它的收敛模型：**不自动收敛，靠人/LLM 决策**。

### 7. 宿主崩溃 与 重复运行

**崩溃后磁盘上剩下什么**：`batches/<id>.json` 的 phase 仍是 `running/planning/paused`、lane 仍是 `running`；lane 目录与 `taskswarm/<taskId>` 分支都在；`_orch` 可能停在 in-progress merge；worker 会话记录留在 `~/.dsh/sessions/`，`dispose()` 未执行。

**代码提供的恢复路径**（比 runbook 新）：`resume()` 在 `active` 为空时取 `latestBatch`，phase ∈ running/planning/paused 就 `recoverPendingBatch()` 重新挂回执行；**原样复用持久化的 `wavePlan`**，`merged` lane 跳过、`failed` lane 重跑（[engine.ts:678-753](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L678-L753)、[status.ts:40-46](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/status.ts#L40-L46)）。两条约束：① 只认**文件名排序最后一个**批次（`latestBatch`，[status.ts:98-104](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/status.ts#L98-L104)）；② `resume` 走 supervisor 时受 `pausedBy==='operator'` 限制（[engine.ts:682-697](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L682-L697)）。
**runbook 与代码相反**：runbook §7.4 说崩溃后 `resume` 是 no-op、要手工把 batch JSON 改成 `aborted` 再开新批次（[runbook.md:378-410](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/docs/runbook.md#L378-L410)）。以代码为准，runbook 这段已过期。

**崩溃带出的四个真问题**：

1. **batch JSON 不是原子写**：`writeFileSync(JSON.stringify(...))` 直写（[status.ts:74-78](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/status.ts#L74-L78)），崩在写盘中间会留半截 JSON；`readBatchState` 解析失败**返回 null**（[:64-72](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/status.ts#L64-L72)）→ `latestBatch` 也 null → `resume` 静默失败（返回 false）。对比同仓 mailbox 用了 tmp+rename（[mailbox.ts:87-92](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/mailbox.ts#L87-L92)），batch 状态反而没做。
2. **`_orch` 的 in-progress merge 没有启动清理**：崩溃后 `MERGE_HEAD` 仍在；`ensureOrchWorktree` 见目录存在就直接返回（[worktree.ts:43-49](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/worktree.ts#L43-L49)），恢复后第一个 `mergeLane` 会被 git 拒绝（§4 探针），随后走进 merger 分支。
3. **`_orch` 目录丢失会重置集成分支**：`-B` 语义（§1 末，已用探针验证）。
4. **`abort`/卸载删 worktree**：崩前的现场在**正常关停**时会被清（[index.ts:190-204](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/index.ts#L190-L204)、[engine.ts:768](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L768)），只剩分支；「什么都不清理」只对**硬崩溃**成立。

**重复运行的行为**：

- 同一引擎实例：有未 abort 的 active 批次时 `run()` 抛「another batch is still running」（[engine.ts:215-220](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L215-L220)）。但**暂停后 `execute()` 已返回并从 active 移除**（`finally` 删，[:263](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/engine.ts#L263)），所以暂停的批次不挡新批次；旧批次停在磁盘的 `paused`，不会被标 `aborted`。
- 插件层只按 `active` 判断，`/tswarm` 命令**不检查磁盘**（[index.ts:360-378](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/index.ts#L360-L378)）；supervisor 的 `start` 才挡 `running/planning`（[supervisor.ts:679-681](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/orchestrator/supervisor.ts#L679-L681)）。runbook 自己承认「`/tswarm` directly after a crash opens a new batch」（[:491](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/docs/runbook.md#L491)）。
- 跨进程：**没有锁文件**。两个 DSH 宿主打开同一仓库 = 两个 engine 写同一 `batches/`、同一 `taskswarm/orch`、同一 worktree 目录；`worktreePaths` 只按 `stateRoot` 拼（[worktree.ts:30-33](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/worktree.ts#L30-L33)），没有任何 pid/lock 保护。
- 同 taskId 再跑：`createLaneWorktree` 先删旧 worktree（[worktree.ts:61-67](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/worktree.ts#L61-L67)），**旧批次「保留的现场」在重跑同一任务时被覆盖**；未提交内容丢失，已提交内容留在分支。

**updateLane 的并发结论（卡片 L22/L26 需要改写）**：形态确实是「读整份 JSON → 改一条 → 整份写」（[status.ts:86-95](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/core/status.ts#L86-L95)），但**单进程内它是同步的**（`readFileSync`+`writeFileSync` 之间没有 await），两条 lane 的 `updateLane` 在事件循环上不会交错，所以「并发 lane 之间仍然 LWW」这个结论不成立。真正的残留风险是：整份写在波次边界/`stopLane`/`switchLaneModel` 仍在（§3）、跨进程无锁、写盘非原子。`[OBS]` 若把「同一进程」换成「两个宿主进程」，LWW 立刻成立。

## SRC-DSH

本机 `@deepseek-ai/dsh 0.2.1-rc.3`（`/Users/bowhead/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh`）。以下行号是**已编译发行物**行号。

- `ctx.agents` 服务由 `@deepseek-ai/dsh-agent` 提供（`dsh-agent/lib/index.js:332` `super(ctx, "agents")`），`create(options)` 走注册的 factory（`dsh-agent/lib/index.js:453-457`），实际构造在 `dsh-agent-loop`：`setup?.(prepared.agent.ctx, prepared.agent)`（`dsh-agent-loop/lib/index.js:1931`）——**setup 的第一个参数是 agent 作用域 ctx，第二个才是 agent**。以上均为本机发行物路径（`…/node_modules/@deepseek-ai/dsh/`），非远端链接。
- `meta.origin === 'subagent'` 是宿主认得的会话标记：侧边栏分组会隐藏它（`dsh-client-ui-workspace/lib/client.js:965`），`dsh-workspace-changes` 也按它决定是否记 cwd（`dsh-workspace-changes/lib/index.js:960`）。TaskSwarm 用它把 worker 会话藏出用户会话列表（KI-001 的修复）。
- `sandbox/mode` 与 `approval/policy` 是合法会话事件：`dsh-sandbox-policy/lib/index.js:41` 自己就 append `sandbox/mode`；两者在 session 格式里有 disposition 定义（`dsh-session-format-v0-to-v1/lib/index.js:36`、`:123`），权限折叠按这三类 knob 事件计算（`dsh-api-session-controller/lib/typert.host.js:90` 的描述：`permission/preset` + `sandbox/mode` + `approval/policy`）。
- 真正的 subagent 委派是另一条路：`dsh-subagent/lib/index.js:408-431` 从**父侧** `captureDelegatedPolicyOverrides(parent)`，把 override append 到 `childSession`；`dsh-subagent/lib/types/manager.js:795-805` 的 `agents.create` 会带 **`parentAgent: parent`**。TaskSwarm 的 `agents.create` **不带 `parentAgent`**，所以它借用了宿主的事件机制与 `origin` 标记，但**不在 subagent 运行时里**（不受委派深度限制、不进子任务记账、不随父 turn 取消）。
- **`[OPEN]`**：`grantWorkerFullAccess` 通过 `agentCtx.agent.session.append(...)` 取会话（[worker-tools.ts:80-91](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/src/worker/worker-tools.ts#L80-L91)）。我在 `0.2.1-rc.3` 的 `dsh-scope` 里看到 `createScope` 只给 ctx 加 `[kScope]` 标记（`dsh-scope/lib/index.js:296-305`），没有 `ctx.agent` 属性；`dsh-agent-loop` 的 setup 调用把 agent 作为**第二个**参数传入。若 `agentCtx.agent` 确实不存在，这两个 append 会**静默 no-op**（函数开头 `if (!session?.append) return`），worker 就退回到环境策略。KI-005 声称实机验证过 override 生效，但代码路径与我的读法不符，故标 `[OPEN]`，需要一条实机 check（`overrideOf(worker)`）。

## TEST

仅核对存在性，**未运行**。

- 测试源码存在：`tests/` 7 个 `*.spec.mjs`，共 **1783 行**（`cleanup 44`、`core 518`、`dashboard 156`、`engine 861`、`i18n 135`、`plugin 69`），另在 `dashboard/` 下 3 个 `*.spec.mjs`（`adapters`/`history`/`server`，随包发布）。
- 运行入口：`npm test` = `npm run build && node --test tests/*.spec.mjs`（[package.json:80-82](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/package.json#L80-L82)）——**必须先 tsc 构建**，因为 `tests` 全部 `import ... from '../lib/...'`（7 个文件均如此；仓库里没有 `lib/`，`.gitignore` 忽略它）。因此「在干净 clone 上直接 node --test」不可行。另注意 glob 只覆盖 `tests/`：`dashboard/*.spec.mjs` 三个文件**不会**被 `npm test` 跑到。
- 发布物 `files` 不含 `tests/`、不含 `src/`（[package.json:59-70](https://github.com/february2015/dsh-taskswarm/blob/032e2c9d228c20cab65fe0ea061d78a7c753ab8c/package.json#L59-L70)）；临时名 tarball 实测无 `src/`、无 `tests/`——**装到的包无法用测试源码复核**。
- 覆盖意图可从上表推断（`cleanup.spec` 覆盖 worktree 清理、`core.spec` 覆盖 batch 状态），但 `[TEST]` 只证明意图，不证明通过。

## CI

- **没有 CI**。仓库树里无 `.github/`；`gh api repos/february2015/dsh-taskswarm/actions/workflows` → `total_count: 0`；HEAD `032e2c9` 的 check-runs → `total_count: 0`；`releases` → 0。
- 因此任何 SHA 都没有 CI 证据；`[CI]` 对本题为空，不能拿「workflow 存在」倒推质量（连 workflow 都没有）。

## RUN

- `[RUN]` **未安装、未构建、未运行** `npm install` / `npm test` / `tsc` / 插件或宿主。
- 实做的只读取证：`gh api`（repo/tags/refs/workflows/check-runs/releases）、`git clone --depth 100` 到 `/tmp/taskswarm_clone`（随后 `git log`/`git diff --stat`/`git show`）、`curl` npm registry（正式名与临时名）与 `api.npmjs.org` 下载数、`curl + tar -xzf` 临时名 tarball 到 `/tmp/ts_pkg`（只读解包，未执行其中任何代码）。
- 额外做了 **2 个一次性 `/tmp` 仓库的 git 语义探针**（不涉及本项目代码）：① `worktree add -B` 在分支已存在且 worktree 目录丢失时**重置分支**（输出 `resetting branch 'taskswarm/orch'; was at 9da62dd`，重置后分支只剩主分支 HEAD 的 1 个提交）；② 未收敛 `MERGE_HEAD` 时二次 `git merge` 被拒（`error: Merging is not possible because you have unmerged files.`，`UU f.txt` 未变）。这两条是 SRC-TARGET §1/§4/§7 的唯一非纯静态依据。
- 运行时行为（worktree 真建、merge 真跑、崩溃真恢复）**一律未跑**，相关结论标 `[OPEN]` 或写明「源码推断」。

## 卡片偏差表

| 卡片位置 / 主张 | 判定 | 证据（pin `032e2c9`） | 建议 |
|---|---|---|---|
| L5/L13「每 lane 一个 git worktree（不是每成员）」 | **成立** | worktree.ts:58-82；reviewer/merger 不另开 worktree（reviewer.ts:80-91、merger.ts:48-58） | 保留，可补「+常驻 `_orch`」 |
| L22 路径 `<stateRoot>/worktrees/<taskId>/` + `_orch` | **成立** | worktree.ts:30-33、:60 | 无需改 |
| L22「新 lane 以 `taskswarm/orch` HEAD 为基线」 | **成立（有分支）** | worktree.ts:78-82；分支已存在时是「附着 + merge orch」，orch 分支缺失时退回当前 HEAD（:78-82） | 补一句续跑语义 |
| L22/L47/L54「失败时刻意什么都不清理」 | **部分成立** | mergeLane 失败保留（worktree.ts:111-131）；但 abort/卸载删 worktree（engine.ts:768、index.ts:190-204）、同 taskId 重跑 `worktree remove --force`（worktree.ts:61-67） | 改成「合并失败保留现场；abort/重跑不保留 worktree 目录，分支保留」 |
| L22/L24「`docs/known-issues.md` 8 个已知问题」+引用 KI-007 | **不成立（路径错）** | 英文档 7 条、无 KI-007（known-issues.md:6-8 及标题）；KI-007 只在 `known-issues.zh-CN.md:29` | 引用改中文档，或写「中文档 8 条 / 英文档 7 条」 |
| L22「KI-003 内存态整份落盘覆盖兄弟 lane」 | **成立** | known-issues.md:262-264 | 无需改 |
| L22「KI-007 `await spawn()` 无超时让整批卡死」 | **成立** | known-issues.zh-CN.md:37-40；代码已加看门狗 engine.ts:605-638 | 保留，补「默认 180 分钟」 |
| L22/L26「`updateLane()` 读整份→改一条→整份写，并发 lane 仍是 last-write-wins」 | **形态成立、结论要改** | status.ts:86-95 形态对；但单进程同步 RMW 不交错；KI-003 主因是 stale 整份写（engine.ts:421-425）；残留为波次整份写+跨进程+非原子（engine.ts:298-320、status.ts:74-78） | 改成「单进程内读改写是同步的；风险在整份写在别处仍存在、跨进程无锁、写盘非原子」 |
| L26「`reviewLevel` 被解析但从不消费，reviewer 可被实现者跳过」 | **成立** | task.ts:173 唯一消费点缺失；review_step 自愿调用，无评审也会合并（engine.ts:491-508） | 保留，可补 README:23 与实现冲突 |
| L26/表格「KI 文档说 90 分钟，代码写的是 180」 | **成立** | known-issues.zh-CN.md:43、:55 写 90；index.ts:91 默认 180；**index.ts:67-68 的注释也写 90** | 保留，补「注释同样过期」 |
| L34 版本 `0.2.38` | **成立但未 pin** | tag 3164995 与 tip 032e2c9 自述均 0.2.38；src 两树相同 | 补 tag/commit |
| L36「npm 近 30 天 0 次」 | **数字成立、解释错** | registry 只剩 `unpublished`（2026-08-16T15:24:26Z 清掉 35 个版本）；下载 0 是**结构性**的；临时名 `dsh-taskswarm2` 上月 **39** 次 | 改成「正式包已下架；仍在流通的是临时名 `dsh-taskswarm2@0.2.38`」 |
| L37 `dsh plugin add dsh-taskswarm` | **失效** | registry 404；README:3-5 自己说改用 GitHub 安装且 8/19 恢复（未发生） | 改为 `dsh plugin add https://github.com/february2015/dsh-taskswarm.git`；临时名因 patch 包名不符需另验 `[OPEN]` |
| L38「dashboard 是纯读 SSE 的」 | **不成立（窄义）** | SSE 确为读（server.mjs:3、:270-300），但 `/api/preferences` PATCH 会写 `<stateRoot>/dashboard-preferences.json`（history.mjs:58、:233-235、:317-321） | 改成「只读批次状态；另存自己的 UI 偏好文件」 |
| L38「附带 CLI `taskswarm-dashboard`」 | **成立** | package.json:76-78；`dashboard.ts` spawn `dashboard/server.mjs` | 无需改 |
| L39「`main: lib/orchestrator/index.js`、`dsh.bundle.patch`、无 client 注入」 | **成立，但需补「仓库无 `lib/`」** | package.json:23、:71-74；`.gitignore` 忽略 `lib/`；只有发布物含 `lib/`（tarball 46 文件） | 补「从源码装必须先 build」 |
| L15「3★」 | **成立** | `/repos` stargazers 3 @2026-11-01 | 无需改 |
| L46「冲突裁决：worktree 隔离——每 lane 一个 worktree，物理上不共享」 | **部分成立** | 代码树隔离成立；但共享 `.git`、共享主仓 `tasks/` 任务包、共享 `_orch` 合并目标，另需串行 merge 队列（engine.ts:108-124） | 补「共享对象库与任务包；合并侧另有串行队列」 |
| L47「失败收敛：merge 失败什么都不清理」 | **成立（限 merge）** | 同上；另有 `conflict`→暂停（engine.ts:333-349） | 保留并限定范围 |
| L53「用 git 做隔离，就不用自己写裁决」 | **不完全成立** | 仍需 merge 串行队列与 merger agent（engine.ts:108-124、merger.ts:84-135） | 改成「隔离交给 git，合并仍要自己排队/解冲突」 |
| L55「known-issues 是本域最好的故障档案」 | `[OBS]` | 英文档 301 行/7 条、中文档 275 行/8 条，均含根因/位置/候选修复；英文档缺 KI-007 | 保留为判断，注明中英不对称 |

## [OPEN]

1. 所有运行时行为（worktree 实际创建、merge 实际执行、崩溃后 `resume` 实际恢复）**未跑**，只有源码与 git 语义探针。
2. `agentCtx.agent.session` 在 `0.2.1-rc.3` 是否可取：若不可取，`grantWorkerFullAccess` 静默失效（worker 仍按环境策略），KI-005 的修复在代码层面不成立——需一条实机 `overrideOf(worker)` 检查。
3. 同波第二个冲突被 merger 误判为 `CONFLICT_RESOLVED`、lane B 假 `merged` 的路径（SRC-TARGET §4）未运行验证；需构造「同波两 lane 都冲突」批次。
4. `_orch` 目录丢失后 `-B` 重置集成分支由 git 探针证明，但真实触发条件（人为清理 / `worktree prune` 后目录消失）未在 TaskSwarm 运行中复现。
5. 临时名 tarball 的 `cordis.patch.yml` 引用 `dsh-taskswarm/orchestrator` 与包名不符，实际安装是否报模块解析错误未验证。
6. 卡片 L15「catalog 快照 1★ → ×3」属外部快照，本轮未核对来源与日期。
