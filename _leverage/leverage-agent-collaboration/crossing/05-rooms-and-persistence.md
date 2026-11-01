---
title: "房间持久化：权威存储与重建副本"
domain: agent-crossing
kind: card
positioning: "跨会话持久化的两种状态：房间存储权威 + 成员日志重建；以 14 team-rooms 为例，看宿主禁写 fact 后重建如何退化。"
takeaway: "“日志是重建副本”依赖宿主允许写入投影事件；宿主禁写时，权威还在，副本不在了。"
read_when: "要做跨会话共享时间线/房间，或评估持久化游标语义时。"
status: observed
updated: 2026-11-01
---
# 05 · 房间持久化

> `dsh-team-rooms` 的核心句是“房间存储是跨会话权威，成员日志是重建副本”。这句话有一半依赖宿主能力：**rc.3 禁止写 `team-room/fact`**，副本就 fold 不出来。

## 1. 权威与副本

- 权威：`team_rooms` 域 4 表（store 跨会话/重启）。
- 副本：时间线写进成员日志时带 `team-room/fact` 与 `timelineSeq`；`teamRoom` 投影 fold 成员自己的日志。
- **rc.3**：`factEventPolicyForVersion()` 判 `forbidden`，新 timeline 不落盘；无旧 fact 的日志投影为空。

## 2. 游标不是“落地后才前进”

- live 路径：消息进 durable inbox（`agent/inbox/spliced`）后前进游标，不是 `user/message` 落地后。
- `lastFactSeq` 在 fact 被跳过时仍推进；`catchUp` 在 agent 缺失时也把两个游标推到末尾。
- retention 外消息会被跳过且游标仍前进。

## 3. 生命周期

- 最后一人 leave / owner 删除 → 直接 purge，不广播 fact、无 room-deleted 类型；leaver 自己的日志也没有 member-left。
- 没有 session 删除/agent dispose 监听 → ghost member 永久占 `maxMembersPerRoom`。
- `pruneRoom` 唯一调用点是 `postMessage`，只做任务/成员变更的房间会突破窗口。

## 4. 借用与判定

1. 权威存储在哪？副本依赖哪些宿主事件？宿主禁写时降级成什么？
2. 游标在哪个事件后前进？跳过段会补发还是静默丢？
3. 删除/离开房间时，谁清理成员、任务、投影？有没有 ghost？
4. 留存窗口在哪些写路径执行？只在发消息时够吗？

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 房间存储权威、成员日志重建 | `[SRC-TARGET]` | [`14 memo`](./_证据/14-team-rooms-源码复核.md)（1.0.8/c1c485e） | 副本依赖 fact 事件 |
| rc.3 禁写 `team-room/fact`，投影退化 | `[SRC-TARGET]` | 同上（audit.ts:105-112） | 旧 fact 仍可 fold |
| 游标会为跳过段推进 | `[SRC-TARGET]` | 同上（catchUp 566-585） | live 路径是 inbox 入队后 |
| 删除不广播、ghost 无清理 | `[SRC-TARGET]` | 同上（leave/delete 路径） | 未跑真实删除/重启 |
| 仓库已 archived、npm deprecated | registry | 同上 Provenance | 2026-10-05 RETIRED |

**未验证**：真实重启后的 catch-up 竞态、ghost 对成员上限的实际影响、旧 fact 与新 timeline 混用，均 `[OPEN]`。
