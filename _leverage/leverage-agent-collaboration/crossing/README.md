---
title: "跨会话/实例/机器"
domain: agent-crossing
kind: index
positioning: "`crossing/` 家族：session handoff、broker/relay、远端 worker、跨实例消息、房间持久化。"
read_when: "要跨会话接力、跨实例投递或跨机执行。"
status: living
updated: 2026-11-01
---
# 跨会话/实例/机器

> 本家族 README。迁移已完成：样本、memo 与章节按家族归位；新增按本册 `00-map` §8 的生长规则补。

## 样本与证据

| 样本 | 证据链 |
|---|---|
| [`06-zbzbhs-dsh-remote-agent.md`](./samples/06-zbzbhs-dsh-remote-agent.md) | [`06-remote-agent-源码复核.md`](./_证据/06-remote-agent-源码复核.md) |
| [`08-Chinesezjc-dsh-interconnect.md`](./samples/08-Chinesezjc-dsh-interconnect.md) | [`08-interconnect-源码复核.md`](./_证据/08-interconnect-源码复核.md) |
| [`09-IKEASven69-dsh-takeover.md`](./samples/09-IKEASven69-dsh-takeover.md) | [`09-takeover-源码复核.md`](./_证据/09-takeover-源码复核.md) |
| [`13-Noelune-dsh-agent-relay.md`](./samples/13-Noelune-dsh-agent-relay.md) | [`13-agent-relay-源码复核.md`](./_证据/13-agent-relay-源码复核.md) |
| [`14-PerryLink-dsh-team-rooms.md`](./samples/14-PerryLink-dsh-team-rooms.md) | [`14-team-rooms-源码复核.md`](./_证据/14-team-rooms-源码复核.md) |

## 章节

- [`01-session-handoff.md`](./01-session-handoff.md)：接管的替换对象与失败语义。
- [`02-broker-and-relay.md`](./02-broker-and-relay.md)：直连 WS vs broker 的鉴权/幂等/离线。
- [`03-remote-worker-trust.md`](./03-remote-worker-trust.md)：远端 loop、hub 能力与凭证边界。
- [`04-acp-remote-execution.md`](./04-acp-remote-execution.md)：ACP/外部运行时的一次性边界。
- [`05-rooms-and-persistence.md`](./05-rooms-and-persistence.md)：房间权威、fact 禁写与游标。

## 证据与边界

- 证据规约见 [`../EVIDENCE.md`](../EVIDENCE.md)；跨家族对照见 [`../encyclopedia.md`](../encyclopedia.md)。
- 章节已成稿；引用样本机制前先读其 memo，冲突以章节与卡片为准。
