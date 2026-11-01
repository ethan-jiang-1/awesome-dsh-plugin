---
title: "控制流：声明式 DAG 还是代码即编排"
domain: agent-pipelines
kind: card
positioning: "流水线的第一选择：用图表达还是用代码表达控制流；对照 03 的 run(wf) 与 11 的分波/依赖，列可分析性与失败重放的取舍。"
takeaway: "图换来静态分析与可视化，代码换来并行/条件/循环免费；先承认图的不可判定，再选缓存与重放策略。"
read_when: "要搭多 agent 流水线，或纠结该不该上 DAG/工作流引擎时。"
status: observed
updated: 2026-11-01
---
# 01 · 声明式 DAG vs 代码即编排

> 流水线的“形状”不是审美：它决定能否静态分析、能否暂停、失败后从哪继续。

## 1. 两种形状

| 形状 | 代表 | 得到 | 付出 |
|---|---|---|---|
| 代码即编排 | `dsh_workflow`：`run(wf,args)` 里 `phase/parallel/pipeline/runAgent` | 并行、条件、循环天然可写；每个“节点”就是一次子代理 | 图不可静态分析；并行度/依赖只能运行时知道 |
| 波次/依赖计划 | `dsh-taskswarm`：`wavePlan` + lane 依赖 | 可提前展示波次；按依赖调度 | 控制流被计划器固定；复杂条件要外挂 |
| 声明式 DAG（本册尚无样本） | 待补 | 可静态分析、可视化、按节点重放 | 表达力受限；循环/动态分支需扩展 |

## 2. “节点”到底是什么

- `dsh_workflow` 的节点 = 一次 `ctx.subagents.start`（可带 dispatch adapter 指定 target/effort）；任务书是代码里拼的。
- `taskswarm` 的 lane = 一个 DSH agent session（`agents.create`，`origin:'subagent'`，cwd=worktree），一个 lane 跑一个任务；reviewer/merger 是额外 lane 角色。
- 因此“DAG 引擎”与“多 agent 调度器”常是同一件事：节点执行者就是子代理。

## 3. 可分析性 vs 可恢复性

- 图可静态分析 → 能预演、能按节点重放；但动态分支会退化成“图里藏代码”。
- 代码可自由控制 → 但失败恢复只能靠**快照 + 内容键缓存**（`dsh_workflow`）或**波次边界整份状态**（`taskswarm`），不是断点续跑。
- `dsh_workflow` 明确“可恢复 = 整体重跑 + 回放已有答案”；`taskswarm` 的 `resume()` 从磁盘批次恢复，但批次 JSON 非原子写会让恢复静默失败。

## 4. 借用与判定

1. 你的步骤能静态列出来吗？能→图；不能→代码，但必须设计缓存键。
2. 失败后要“从断点继续”还是“重跑+回放”？前者要持久执行栈，后者只需内容键。
3. 并行度/依赖在运行时才知道吗？若是，别假装有 DAG。
4. 谁拥有 run 状态？进程内存、磁盘快照，还是宿主会话？

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 03 没有 DAG，JS 控制流即编排 | `[SRC-TARGET]` | [`03 memo`](./_证据/03-dsh_workflow-源码复核.md)（0.1.2/44b83c1） | 依赖图不可静态分析；版本门不比较 |
| 03 的“可恢复”是快照重跑 + 内容键缓存 | `[SRC-TARGET]` | 同上；README:137 | 不是断点续跑；控制面重启丢失 |
| 11 每 lane 一个 worktree、按波次/依赖调度 | `[SRC-TARGET]` | [`11 memo`](./_证据/11-taskswarm-源码复核.md)（v0.2.38/3164995） | npm 已下架；批次 JSON 非原子 |
| `dsh_workflow` 不替换 `ctx.workflows`，新增 `ctx.dynamicWorkflows` | `[SRC-TARGET]`/`[DOC]` | 03 memo 的 `docs/ARCHITECTURE.md` 引用 | 只证明服务名，不证明兼容性 |
| “图 vs 代码”的取舍 | `[OBS]` | 本章归纳 | 经验框架，不是对照实验 |

**未验证**：声明式 DAG 在 DSH 上的真实实现、图的可视化/重放工具、暂停后恢复的语义，均 `[OPEN]`。
