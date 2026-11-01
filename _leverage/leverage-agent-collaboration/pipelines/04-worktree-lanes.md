---
title: "worktree lane：用物理隔离换冲突裁决"
domain: agent-pipelines
kind: card
positioning: "流水线的隔离方案：每 lane 一个 git worktree、共享 .git 与任务目录；看它买到什么、没买到什么。"
takeaway: "worktree 隔离的是工作树，不是分支/任务/合并；合并仍要串行，失败保留与清理必须写成显式策略。"
read_when: "要在多 agent 间隔离文件改动，或评估 worktree 方案的代价时。"
status: observed
updated: 2026-11-01
---
# 04 · worktree lane

> `dsh-taskswarm` 是本册唯一的 worktree 样本：每 lane 一个 worktree + 常驻 `_orch` 集成树。它证明“物理隔离”可行，也暴露了隔离之外的三笔账。

## 1. 它怎么分

- 每 lane：`<stateRoot>/worktrees/<taskId>/`，分支 `taskswarm/<taskId>`，基线是 orch HEAD。
- 常驻 `_orch`：集成 worktree，`mergeLane()` 在这里 `git merge`；reviewer 在 lane 内跑，merger 在 `_orch`。
- 共享：`.git`、`tasks/` 任务包、`_orch`；lane 只隔离工作树。

## 2. 买到什么

- 文件冲突从“两人同时写”变成“合并时冲突”，可以串行合并、保留冲突标记。
- 每个 lane 可以独立检出/重跑/保留现场。

## 3. 没买到什么

| 问题 | 现实 |
|---|---|
| 任务互斥 | worktree 不解决任务归属；同一任务仍可被重复派发 |
| 合并冲突 | 交给 git；`mergeLane` 失败保留现场，但 abort/插件卸载/同 task 重跑会移除 lane worktree（只剩分支） |
| 跨进程 | 无锁；两个宿主可同时操作同一仓库 |
| 恢复 | 批次 JSON 非原子写；`_orch` 目录丢失时 `worktree add -B` 会重置 orch 分支 |

## 4. 借用与判定

1. 隔离单位是文件、分支还是任务？三者不同。
2. 合并是串行、并行还是交给用户？失败时保留什么、清理什么？
3. worktree 的生命周期谁拥有？崩溃/卸载/重跑各走哪条清理路径？
4. 跨进程有没有锁/租约？没有就写明“单写者”。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 每 lane 一个 worktree + 常驻 `_orch` | `[SRC-TARGET]` | [`11 memo`](./_证据/11-taskswarm-源码复核.md)（v0.2.38） | 合并失败保留，但 abort/卸载/重跑会清 lane |
| 合并串行、冲突交给 git | `[SRC-TARGET]` | 同上（promise 链） | 单进程内串行；跨进程无锁 |
| 批次 JSON 非原子、`_orch` 重置风险 | `[SRC-TARGET]` | 同上 | 未跑真实崩溃恢复 |
| worktree 隔离 ≠ 任务/分支隔离 | `[OBS]` | 本章归纳 | 经验判断 |

**未验证**：真实并发合并、`_orch` 重置触发条件、Windows 路径/权限差异，均 `[OPEN]`。
