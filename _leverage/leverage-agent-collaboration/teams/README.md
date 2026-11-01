---
title: "团队：多成员如何编队、调度、共享任务板"
domain: agent-teams
kind: index
positioning: "`teams/` 家族：roster/captain、调度、邮箱、任务板与质量门；样本按主家族归位。"
read_when: "要建多 agent 团队或比较各家的编队/调度/失败收敛。"
status: living
updated: 2026-11-01
---
# 团队：多成员如何编队、调度、共享任务板

> 本家族 README。迁移后先保留样本与证据链；章节扩写与排序在下一阶段完成。

## 样本与证据

| 样本 | 证据链 |
|---|---|
| [`01-NanmiCoder-dsh-agent-teams.md`](./samples/01-NanmiCoder-dsh-agent-teams.md) | [`01-agent-teams-源码复核.md`](./_证据/01-agent-teams-源码复核.md) |
| [`02-toolclub-dsh-agent-team-gui.md`](./samples/02-toolclub-dsh-agent-team-gui.md) | [`02-team-gui-源码复核.md`](./_证据/02-team-gui-源码复核.md) |
| [`04-limuyang2-agent-team.md`](./samples/04-limuyang2-agent-team.md) | [`04-agent-team-源码复核.md`](./_证据/04-agent-team-源码复核.md) |
| [`05-Mlte0907-dsh-teams-x.md`](./samples/05-Mlte0907-dsh-teams-x.md) | [`05-teams-x-源码复核.md`](./_证据/05-teams-x-源码复核.md) |
| [`10-Asher-2000-dsh-expert-mode.md`](./samples/10-Asher-2000-dsh-expert-mode.md) | [`10-expert-mode-源码复核.md`](./_证据/10-expert-mode-源码复核.md) |
| [`12-2507483326-dsh-eteams.md`](./samples/12-2507483326-dsh-eteams.md) | [`12-eteams-源码复核.md`](./_证据/12-eteams-源码复核.md) |

## 章节

- [`01-roster-and-captain.md`](./01-roster-and-captain.md)：roster 权威位置、成员模型、队长不可选举。
- [`02-scheduling.md`](./02-scheduling.md)：idle 边沿、原子认领、容量/深度。
- [`03-mailbox-and-ack.md`](./03-mailbox-and-ack.md)：投递/准入/已读三态与幂等。
- [`04-taskboard-and-gates.md`](./04-taskboard-and-gates.md)：任务板权威、完成判据、质量门位置。
- [`05-failure-modes.md`](./05-failure-modes.md)：假成功、覆盖写、孤儿、停驻与假恢复。

## 证据与边界

- 证据规约见 [`../EVIDENCE.md`](../EVIDENCE.md)；跨家族对照见 [`../encyclopedia.md`](../encyclopedia.md)。
- 本家族章节尚在扩写；引用样本机制前先读其 memo。
