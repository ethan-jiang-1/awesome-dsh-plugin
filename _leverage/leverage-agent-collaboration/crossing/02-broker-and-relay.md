---
title: "broker/relay：跨运行时的消息总线"
domain: agent-crossing
kind: card
positioning: "跨异构运行时的两条路：HTTP broker + 长轮询/唤醒（13）与持久 WebSocket 直连（08）；比较鉴权、幂等与离线语义。"
takeaway: "总线能连通不等于消息不丢：先问幂等键、离线队列与鉴权边界，再问支持几家运行时。"
read_when: "要做跨运行时/跨实例消息，或比较 broker 与直连方案时。"
status: observed
updated: 2026-11-01
---
# 02 · broker / relay

> 08 与 13 解决同一个问题：让不同 DSH 实例/不同 agent 运行时互相投消息。差别在拓扑（直连 vs broker）与投递语义。

## 1. 两种拓扑

| 样本 | 拓扑 | 传输 | 鉴权 |
|---|---|---|---|
| `dsh-interconnect` | 每个已配置对端一条拨号 WS（互配一对=两条 socket） | 持久 WS，消息投对端 session inbox | 一把共享 `DSH_INTERCONNECT_TOKEN`，无 per-peer 授权 |
| `dsh-agent-relay` | 单 broker 星形 | HTTP + 长轮询（0.8.x）；wake 兜底 | HMAC-SHA256 + 300s 时间戳窗口 |

## 2. 投递语义

- `interconnect`：**无消息级幂等**（`reqId` 只关联）、**无离线队列**（链路断即 `unreachable`，事件也不补发）；消息落到接收方 session log。
- `relay`：消息先落库（默认 7 天），租约认领 + 32B 租约令牌 + `UNIQUE(origin,idempotency_key)`（去重窗口=保留期）；DSH 侧 reply 找不到会话映射时 **ack 后丢弃**——broker 不丢，会话层 best-effort。

## 3. 两个“版本错位”教训

- `relay`：源码 0.8.1 有 `wake_command`/长轮询，但 **npm latest 仍是 0.5.0**，装到的是“无唤醒/无长轮询 + 仍含 v1”的旧代。卡片若按 README 写 0.8.1，就会把未发布能力当现状。
- `interconnect`：与上游“逐行同步”的对齐闸已退役（2026-09-16 作废），不能再写“行为等价可机械验证”。

## 4. 借用与判定

1. 消息先落库还是只走 socket？断链后补发吗？
2. 幂等键谁生成、谁校验、窗口多久？
3. 鉴权是一把共享密钥、per-peer token，还是 HMAC+时间戳？本机进程能否伪造？
4. 发布物与源码是否同一代？npm latest 是哪个版本？

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 08 无幂等、无离线队列、共享 token | `[SRC-TARGET]` | [`08 memo`](./_证据/08-interconnect-源码复核.md)（0.13.0/5547b03） | 互配一对有两条 socket |
| 13 源码 0.8.1 有 wake/长轮询，npm 0.5.0 没有 | `[SRC-TARGET]`/registry | [`13 memo`](./_证据/13-agent-relay-源码复核.md)（7e43c54） | 0.6–0.8 均未发布 |
| 13 的鉴权/租约/幂等键语义 | `[SRC-TARGET]` | 同上 | DSH reply 无会话映射会丢 |
| 13 的 broker 回环是默认非强制 | `[SRC-TARGET]` | 同上 | 唯一远端检查在插件状态路由 |
| “总线连通≠不丢” | `[OBS]` | 08/13 横向对照 | 归纳性判断 |

**未验证**：跨机真实网络下的重连/重复投递、relay 0.5↔0.8 协议兼容、wake 的计费影响，均 `[OPEN]`。
