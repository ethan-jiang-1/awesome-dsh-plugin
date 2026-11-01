---
title: "邮箱与 ack：投递成功不等于被消费"
domain: agent-teams
kind: card
positioning: "团队的第三笔账：消息投到哪、什么时候算被消费、重试会不会重复；对照 01/08/14 的投递语义。"
takeaway: "把“已投递 / 已进入 step / 已读”拆成三态；ack 只发生在宿主真正接纳之后，超时重投要有幂等键。"
read_when: "要设计成员间消息、回答“消息丢没丢”，或排查重复执行时。"
status: observed
updated: 2026-11-01
---
# 03 · 邮箱与 ack

> “投递成功”与“模型消费了”之间有一条缝，几乎所有丢消息/重复执行的 bug 都住在那里。

## 1. 三种投递语义

| 样本 | 投递目标 | ack 时机 | 重复风险 |
|---|---|---|---|
| `dsh-agent-teams` | 磁盘 JSONL 邮箱 | `agent/pre-step` 准入或 `agent_teams_status` 读取才 ack；reject 不算消费 | 60s 租约过期重投；带 `attemptId` 的旧消息被过滤 |
| `dsh-interconnect` | 对端 session inbox（`agent/inbox/spliced` 持久化） | 无消息级幂等，`reqId` 只做关联 | 超时重试可能重复投递 |
| `dsh-team-rooms` | 房间时间线 + 成员日志 fact | live 路径入 inbox 后前进游标；catchUp 会为跳过段推进 | 跳过段不会补发，游标却已前进 |

## 2. 宿主侧的事实

- `agent/inbox/spliced` 是持久化事件：splice 由宿主完成，消息落到接收方 session log。
- `agent/pre-step` 是 waterfall：`reject` 或换消息；**`reject` 的 decision 没有理由字段**。
- 因此“被 Host 接受”不等于“被某个 step 消费”；ack 必须绑定到 step 准入或显式读取。

## 3. 幂等键不是装饰

- `agent-teams`：邮件带 `attemptId/sourceAttemptId`，`isCurrentMail` 过滤过期代际；不带字段的邮件一律放行。
- `interconnect`：`reqId` 每次新生成、收端不查重——重试就是重复。
- `agent-team`：`idempotencyKey` 有赋值无读取，去重靠稳定消息 id + inbox splice 扫描。

**判定**：先问清楚“幂等键在发送端生成还是接收端校验”，再问“去重窗口多长”。

## 4. 借用与判定

1. 消息写在哪里？会话日志、磁盘邮箱、broker DB，还是内存 Map？
2. 什么事件算 ack？投递、入 inbox、step 准入、模型输出，四者不同。
3. 重投的幂等键是什么？窗口多久？跨重启还在吗？
4. 接收方不在线时，消息是排队、拒绝，还是静默丢？

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 01 的三态/租约/准入 ack 成立 | `[SRC-TARGET]` | [`01 memo`](./_证据/01-agent-teams-源码复核.md)（0.1.28） | 60s 租约只在 `readPendingMailbox` 生效；无测试 |
| 08 无消息级幂等、无离线队列 | `[SRC-TARGET]` | [`08 memo`](../crossing/_证据/08-interconnect-源码复核.md)（0.13.0） | `reqId` 只关联不去重 |
| 14 的游标不是“落地后才前进” | `[SRC-TARGET]` | [`14 memo`](../crossing/_证据/14-team-rooms-源码复核.md)（1.0.8） | catchUp 跳过段仍推进 |
| `agent/inbox/spliced` 持久化、pre-step 可 reject 但无理由 | `[SRC-DSH]` | `dsh-agent/lib/types/types.d.ts`、`runtime-types.d.ts:92-97,304-310` | 宿主契约，不证明样本用法正确 |
| “投递≠消费”是跨样本共性 | `[OBS]` | 上述 memo 横向对照 | 归纳性判断 |

**未验证**：真实崩溃后租约重投、跨实例重复消息的实际后果、catchUp 跳过段的数据丢失面，均 `[OPEN]`。
