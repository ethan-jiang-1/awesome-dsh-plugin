---
title: "GM-HZ/agent-dag-workflow"
domain: agent-pipelines
kind: sample
positioning: "`@gm-hz/agent-dag-workflow@1.0.1`：声明式 WorkflowTemplate + ready 队列 DAG 引擎；checkpoint 管恢复、artifact 管 recorded 重放、宿主限额封顶。"
takeaway: "图在模板里、恢复靠 semanticHash、重放靠 artifact；额度是 min(模板, 宿主)，不是模板说了算。"
read_when: "要暂停/恢复、人工审批、可重放审计，而不是「一口气跑完」的脚本。"
status: observed
also_in: "teams"
updated: 2026-11-01
tier: 典型
life: active
evidence: L1
answers: Q4
---
# 18 · `@gm-hz/agent-dag-workflow`

> **一句话**：用一份 `WorkflowTemplate` JSON 声明节点与边，引擎按 ready 队列调度；**恢复**靠 checkpoint 与 `semanticHash`，**重放**靠已提交的外部输出与 Artifact——三种模式不是一回事。
> **边界**：单进程引擎 + SQLite 持久化；跨进程/分布式只提供可选的 Queue/Runner 适配器。
> **影响力**（2026-10-31 采样）：**7★** · npm **1,500 次/月**（2026-09-30..10-29）· MIT。
> **什么时候找它**：你要「跑一半停下、重启继续、事后重放取证」，而不是「一口气跑完的脚本」。

> 导航：[样本索引](../../encyclopedia.md) · [域章程](../../00-map.md) · [本家族篇](../README.md) · [编排模型 01](../01-graph-vs-code.md)
> **证据链**：npm `1.0.1` ↔ tag `v1.0.1` ↔ commit `9e9d006`（同 SHA 的 4 个 CI check-run 全绿）；模板/引擎/重放/限额的行号见[`18 源码复核`](../_证据/18-agent-dag-workflow-源码复核.md)。

## 设计思路

**它把「编排」从代码搬回数据**。一份 `WorkflowTemplate` v1 声明 enums/node/edge/outputs/policies；节点种类含 `core.condition` / `core.foreach` / `core.script`，以及 `gateway.tool.execute` / `gateway.agent.execute` / `gateway.approval.request` / `gateway.workflow.call`（[SRC-TARGET] `lib/core/nodes.js:44,311,364,392`）。**代价是图必须能被静态校验**——这恰好是代码即编排（[`03`](./03-omdsh-dev-dsh_workflow.md)）放弃的那一半。

**引擎是 ready 队列**：start 节点进 `ready`，`sortReady` 排序后逐个激活；恢复时重建 ready 队列（[SRC-TARGET] `lib/core/engine.js:55-56,214`）。它不做「整段重跑」，也不把控制面放在内存里当唯一真相。

**恢复与重放是两条不同的路**：

| 动作 | 做什么 | 前提 |
|---|---|---|
| `resume` | 从 checkpoint 恢复未完成 run | run 存在、authority 一致、**semanticHash 与存档一致**（[SRC-TARGET] `lib/core/engine.js:173-184`） |
| `replay: recorded` | 用已提交的外部输出重跑，可取证 | plan 可重放、**源 run 已完成**、外部输出与 Artifact 齐全（[SRC-TARGET] `lib/runtime/runtime.js:257-266`） |
| `replay: live` | 按模板重新执行外部调用 | 只需要 run 的输入与模板 |

**额度是「模板 ≤ 宿主」**：模板 policies 默认 `4 并发 / 100 节点次 / 10 分钟`；部署限额 `16 / 1000 / 1 小时`，并发硬顶 64；执行器与恢复路径都取 `min(template/default, deployment)`（[SRC-TARGET] `lib/core/limits.js:4-27,47-54`）。**模板不能给自己提额度。**

**重试要先声明幂等等级**：节点定义标 `retry: never / safe / idempotent`；编译期若 `maxAttempts > 1` 撞上 `never`，直接报 `NODE_RETRY_UNSAFE`（[SRC-TARGET] `lib/core/types.d.ts:103`、`lib/core/compiler.js:71-74`）。子流程网关还要求 `invocationId` 跨进程重启幂等（[SRC-TARGET] `lib/core/types.d.ts:198-200`）。

**权限只收窄**：模板 `requires` 是不可变 allowlist，未声明即 `WORKFLOW_REQUIREMENT_UNDECLARED`；它只缩小可调用面，不授予任何权限（[SRC-TARGET] `spec/workflow-template-v1.md:38-57`；[DOC] `README.md:30`）。

**DSH 接线只有一行 patch**：适配器 `inject = ['tools','subagents','approval','skills']`，SQLite 落在 `dshHomePath('agent-dag-workflow/workflows.db')`（[SRC-TARGET] `lib/adapters/dsh/index.js:3-5`、`cordis.patch.yml:1-5`）。**但持久化是否生效取决于宿主装了哪套 `workflow*` 服务**——适配器既支持外部服务，也会回落到内存实现。

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | SQLite Journal + Checkpoint，run 固化模板、修订、依赖闭包、引擎版本与 NodeDefinition set hash | 库在 `DSH_HOME`；发布物不含 `src/`，只能读构建物；Journal 并发语义未实跑 |
| 冲突裁决 | **不做文件级互斥**；只做「能力收窄」与「节点幂等分级」 | 工作区写冲突仍要 pre-execute deny 或 worktree |
| 失败收敛 | checkpoint 恢复 + 三种重放 + 按幂等分级重试 | `recorded` 要求源 run 完成且 Artifact 齐全；重放不还原模型隐藏思维链（[DOC] `README.md:219`） |

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`GM-HZ/agent-dag-workflow`](https://github.com/GM-HZ/agent-dag-workflow) |
| **npm 包名** | `@gm-hz/agent-dag-workflow` |
| **版本(本次读)** | `1.0.1` @ tag `v1.0.1` = commit `9e9d006`（npm `gitHead` 同 SHA） |
| **License** | MIT |
| **安装** | `npm install @gm-hz/agent-dag-workflow`；DSH 侧由 `dsh.bundle.patch` → `cordis.patch.yml` 插入一行 |
| **接线方式** | `dsh.bundle` + `dsh.client.inject`（web）；适配器 `inject` 宿主 `tools/subagents/approval/skills` |
| **复现要点** | 先确认 profile 里有 `workflowTemplates/workflowRuns/...` 服务，否则适配器回落内存实现，重启即丢 |

## 借用指南

### 可借鉴（直接抄）

1. **图在数据里，恢复靠哈希** —— run 固化 `semanticHash`，恢复前比对；模板改了就不许接着跑旧的 checkpoint。这比「版本号对上就恢复」可靠。
2. **重放分三档** —— `inspect`（读历史）/ `recorded`（用已提交输出）/ `live`（真重跑）。**承诺「可复现」前先说是哪一档**，以及 Artifact 存多久。
3. **额度只做减法** —— 模板写默认值，宿主写 ceiling，执行时取 `min`；模板无法给自己提额。任何「可配并发」的编排都该这么写。
4. **重试先问幂等** —— 节点级 `never/safe/idempotent` + 编译期拒绝不安全重试，比运行时靠日志判断便宜得多。
5. **权限是交集不是授予** —— `requires` 只收窄；未声明的 capability 不可见，声明了但宿主没装就 fail closed。

### 别照抄

- **别把 `recorded` 当「重跑」**：它要求源 run 已完成、外部输出齐全；缺 Artifact 会直接报错，不会退回 live。
- **别把模板 `policies` 当硬上限**：真正的 ceiling 在宿主 deployment limits；模板值只可能更小。
- **别把一行 patch 当零配置**：没有 `workflow*` 服务时走内存实现，重启就丢；SQLite 库也跟着 `DSH_HOME` 走。
- **别在它上面做文件互斥**：它只收窄能力、不做写冲突裁决，冲突仍归 [`07`](../../coordination/samples/07-Nwflower-dsh-file-claim.md) 或 worktree。
