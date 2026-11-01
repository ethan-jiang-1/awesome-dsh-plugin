---
title: "流水线：DAG 与代码即编排"
domain: agent-pipelines
kind: index
positioning: "`pipelines/` 家族：声明式 DAG vs 代码控制流、重放/缓存、暂停恢复、worktree lane。"
read_when: "要搭多 agent 流水线，或判断该用图还是代码表达控制流。"
status: living
updated: 2026-11-01
---
# 流水线：DAG 与代码即编排

> 本家族 README。迁移后先保留样本与证据链；章节扩写与排序在下一阶段完成。

## 样本与证据

| 样本 | 证据链 |
|---|---|
| [`03-omdsh-dev-dsh_workflow.md`](./samples/03-omdsh-dev-dsh_workflow.md) | [`03-dsh_workflow-源码复核.md`](./_证据/03-dsh_workflow-源码复核.md) |
| [`11-february2015-dsh-taskswarm.md`](./samples/11-february2015-dsh-taskswarm.md) | [`11-taskswarm-源码复核.md`](./_证据/11-taskswarm-源码复核.md) |

## 章节

- [`01-graph-vs-code.md`](./01-graph-vs-code.md)：DAG vs 代码控制流的取舍。
- [`04-worktree-lanes.md`](./04-worktree-lanes.md)：worktree lane 的隔离与未隔离项。

## 证据与边界

- 证据规约见 [`../EVIDENCE.md`](../EVIDENCE.md)；跨家族对照见 [`../encyclopedia.md`](../encyclopedia.md)。
- 本家族章节尚在扩写；引用样本机制前先读其 memo。
