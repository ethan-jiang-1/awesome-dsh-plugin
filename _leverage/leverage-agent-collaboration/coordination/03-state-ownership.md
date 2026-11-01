---
title: "状态归属：真相源只有一个吗"
domain: agent-coordination
kind: card
positioning: "横向比较协作状态放在哪：会话日志、磁盘、storageDomain、broker、同步盘；以及“第二真相源”如何失步。"
takeaway: "先指定唯一权威，再谈并发；出现第二份可写状态时，必须有明确的合并/审计规则。"
read_when: "要给协作状态定权威，或排查“面板和 agent 记忆不一致”时。"
status: observed
updated: 2026-11-01
---
# 03 · 状态归属

> 协作系统的第一笔税。权威位置决定：重启后剩什么、并发时谁覆盖谁、面板显示的是不是真的。

## 1. 五种权威位置

| 位置 | 样本 | 优点 | 代价 |
|---|---|---|---|
| 会话日志（event-sourced） | DSH 原生；`team-rooms` 的成员日志 | 可重放、宿主持久化 | 投影/重建依赖宿主事件；事实可能不在日志里 |
| 磁盘文件 | `agent-teams`（team.json）、`teams-x`（.teams-x） | 简单、可读 | 跨进程覆盖；写坏/半写 |
| `storageDomain` | `agent-team`（5 表）、`team-gui`（8 表） | 宿主持久化/事务边界 | 只能读自己域；表结构也是契约 |
| broker DB | `agent-relay`（SQLite） | 跨运行时、离线队列 | 多一套部署/备份；会话层仍可能丢 |
| 同步盘 | `takeover`（~/.handoff） | 零协议、跨机 | 冲突语义由同步盘决定；无回执 |

## 2. 第二真相源的三种失步

- **面板 vs agent**：`team-gui` 面板读 storageDomain 快照，agent 读自己的任务上下文；不同步时用户看到“已完成”而 agent 仍在跑。
- **磁盘 vs 会话事件**：`agent-teams` 把磁盘升为真相源、会话日志降为审计；两者不一致时以磁盘为准。
- **内存 vs 磁盘**：`teams-x` 的波次/暂停状态在内存，崩溃后剩磁盘批次；`taskswarm` 的批次 JSON 非原子写会让 resume 静默失效。

## 3. 借用与判定

1. 哪份状态是权威？谁可以写？有没有只读副本？
2. 权威写失败时，内存还继续吗？用户看到“成功”了吗？
3. 重启后从哪读？读到旧/坏数据时是报错、回默认，还是静默继续？
4. 跨进程/跨机时，权威还能被单写吗？

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 01 磁盘 team.json 是权威、日志是审计 | `[SRC-TARGET]`/`[DOC]` | [`01 memo`](../teams/_证据/01-agent-teams-源码复核.md) | 进程内锁；跨进程覆盖 |
| 02 面板/任务在 storageDomain 8 表 | `[SRC-TARGET]` | [`02 memo`](../teams/_证据/02-team-gui-源码复核.md) | 轮询更新，不是推送 |
| 14 房间存储权威、日志重建依赖 fact | `[SRC-TARGET]` | [`14 memo`](../crossing/_证据/14-team-rooms-源码复核.md) | rc.3 禁 fact，投影为空 |
| 13 消息真相在 broker SQLite，presence 在内存 | `[SRC-TARGET]` | [`13 memo`](../crossing/_证据/13-agent-relay-源码复核.md) | 重启后 presence 归零 |
| “权威只能有一个” | `[OBS]` | 本章归纳 | 经验原则；允许只读副本 |

**未验证**：各样本在真实崩溃后的权威恢复、坏数据路径，均 `[OPEN]`。
