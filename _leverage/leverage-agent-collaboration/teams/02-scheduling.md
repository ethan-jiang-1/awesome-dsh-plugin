---
title: "调度：idle 边沿、原子认领与容量"
domain: agent-teams
kind: card
positioning: "团队的第二笔账：任务什么时候被认领、谁来唤醒成员、容量不够时排队还是拒绝；对照 01/02/05 的调度面。"
takeaway: "调度不是轮询：用宿主状态边沿 + 锁内认领；容量默认值不等于可无限扩，先预留再物化。"
read_when: "要设计团队成员唤醒/任务认领，或排查“任务卡住没人做”时。"
status: observed
updated: 2026-11-01
---
# 02 · 调度：idle 边沿、原子认领与容量

> 多成员系统里，“谁来做下一个任务”不能靠成员自己轮询。宿主的 `agent/status` 已经知道谁空了——调度器要做的是**在这个边沿上原子地认领一个 ready 任务**，而不是重新发现一件已知的事。

## 1. 三种触发

| 触发 | 样本 | 机制 | 代价 |
|---|---|---|---|
| 宿主 idle 边沿 | `dsh-agent-teams` | `agent/status` idle 时在锁内认领 ready 任务并唤醒成员；先投邮箱，唤醒在锁外 | 依赖宿主事件；跨进程无协调 |
| 面板/用户触发 | `dsh-agent-team-gui` | `agent/pre-step` 在 on-demand 模式下早退；guaranteed 模式由宿主派工 | “默认不派活”不是运行时默认 |
| 质量门/波次 | `dsh-teams-x` | 60s 对账器回收搁浅、5min 判 orphan 回池、30/60min 提醒 | 无存活心跳、无硬超时，只是软收敛 |

## 2. “原子认领”要看锁的边界

- `agent-teams`：认领与铸 attempt 在锁内，**唤醒在锁外**；锁是进程内 promise 链。
- `teams-x`：默认启用跨进程文件锁（`$TMPDIR/dsh-teams-x-locks`，30s stale/10s 超时），但只串行化写入，不提供跨进程归属。
- `agent-team`：`storageDomain` + revision CAS，`ownership_conflict`/`MEMBER_BUSY` 是单进程窄控制。

**判定**：先问锁保护的是“读-改-写”还是“归属”；只有前者时，两个进程仍可能各自认为自己拥有任务。

## 3. 容量与深度

| 约束 | 默认 | 边界 |
|---|---|---|
| `dsh-subagent` 深度 | `maxDepth=1` | 只允许直接子代理；显式 depth 可覆盖 |
| `dsh-subagent` 容量 | `maxActiveSubagents=8` | 每棵 activation 树共享；根父不占槽；耗尽不排队 |
| 团队成员上限 | 各样本不同（如 `maxMembers=8`） | 是 roster 上限，不自动等于并发上限 |
| `dsh-expert-mode` | 17 行但 `maxActiveSubagents=8` | 17 个专家不可能同时活跃，队列由宿主拒绝 |

## 4. 借用与判定

1. 成员空闲信号从哪来？宿主 `agent/status`、邮箱轮询，还是定时器？
2. 认领在哪个锁内？锁跨进程吗？失败的认领会不会留下 claimed 孤儿？
3. 容量耗尽时是排队、拒绝还是静默丢任务？用户能看到原因吗？
4. 成员崩溃/任务超时，谁把任务放回池？有没有退避与上限？

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| idle 边沿调度在 01 中真实存在，且先投邮箱、唤醒在锁外 | `[SRC-TARGET]` | [`01 memo`](./_证据/01-agent-teams-源码复核.md)（0.1.28/3331b90） | 锁只进程内；跨进程会覆盖 |
| 02 的 on-demand 不是运行时默认（shipped/legacy=guaranteed） | `[SRC-TARGET]` | [`02 memo`](./_证据/02-team-gui-源码复核.md)（v1.3.0/14ea119） | 仅新 Settings 草稿默认 model-tool |
| 05 默认有跨进程文件锁，但只串行写 | `[SRC-TARGET]` | [`05 memo`](./_证据/05-teams-x-源码复核.md)（9c56100） | 无归属/fencing；pinned CI 为红 |
| `maxActiveSubagents` 默认 8、根父不占槽、耗尽不排队 | `[SRC-DSH]` | `dsh-subagent/lib/index.js:2980` 与 README:53 | 每棵 activation 树独立计额 |
| `maxDepth` 默认 1 | `[SRC-DSH]` | `dsh-subagent/lib/index.js:2979` | 显式 tool depth 可覆盖 |

**未验证**：真实并发下两个进程同时认领、idle 事件丢失后的补偿、队列耗尽时用户可见性，均 `[OPEN]`。
