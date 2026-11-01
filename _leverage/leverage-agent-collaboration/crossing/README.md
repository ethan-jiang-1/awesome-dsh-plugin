---
title: "跨会话/实例/机器：替换的是什么、谁在信任谁、断了丢不丢"
domain: agent-crossing
kind: index
positioning: "家族篇：原生只给远程控制一个实例、不给实例间总线；五个样本的四类替换对象、三条判据与失效。"
read_when: "要跨会话接力、跨实例投递或跨机执行，或判断某条通道的信任与丢失语义。"
status: living
updated: 2026-11-01
budget: 135
---
# 跨会话/实例/机器

> 本家族篇固定四段：**原生怎么做 → 样本怎么偏离 → 三条判据 → 失效与开放问题**。样本细节在卡，证据在 memo。

## 1. 原生怎么做（`@deepseek-ai/dsh@0.2.1-rc.3`）

**原生只给「远程控制一个实例」，不给「实例之间发消息」。**

| 接缝 | 提供什么 | 不提供什么 |
|---|---|---|
| `dsh-api-gateway` | 带类型的远程调用与流：`/api/remote.mux` WebSocket（`lib/index.js:133`），每次调用必须指明 Peer | 实例间消息总线、离线队列 |
| `dsh-api-remote-access` | 非 owner Peer 的**方法级**访问控制：按 role/resources 判定，列表逐项过滤，每 Peer 一份访问快照 | 资源级以外的授权模型 |
| `dsh-acp` | 受信程序控制持久会话：创建/恢复/取消、模型选择、MCP 挂载、标准更新 | fork、删除、transcript 回放、附加目录 |

三条硬事实：

1. **拒绝发生在激活 Session 之前**：Gateway 对非 owner 的调用先解析资源、再问 `ctx.remoteAccess.decide(...)`，被拒抛 `remote-access/denied`，此时还没有任何 Session 被激活 `[SRC-DSH]` `dsh-api-gateway/README.md`（Host 服务节）。
2. **Peer 没有默认值**：`InvokeRemoteRequest.peer` 与 `wireStream.open()` 的 `peer` 都必填，Gateway 从不提供默认 Peer `[SRC-DSH]` 同上。
3. **ACP 是「受信控制器」模型**：`authenticate` 立即成功（服务器不需要身份验证），权限提示是一次性允许/拒绝 `[SRC-DSH]` `dsh-acp/README.md:65,74`；**每个会话只允许一个正在处理的提示词** `:112`。

**原生空白**：没有 broker、没有离线队列、没有跨实例 inbox 路由、没有房间存储。这四样都是样本自己造的。

## 2. 样本怎么偏离

| 样本 | 分级 | 替换对象 | 关键机制与代价 |
|---|---|---|---|
| [`09-takeover`](./samples/09-IKEASven69-dsh-takeover.md) | **典型** | **会话**（不是进程/端口/profile） | 文件总线 + `open(claim,'wx')` 恰好一次；四态证据账本；零实时性、无回执 |
| [`06-remote-agent`](./samples/06-zbzbhs-dsh-remote-agent.md) | **典型** | **机器** | 副机跑完整 loop；凭证不过协议，但 hub 可 `exec`/`remote_read`——信任边界而非「永不出机」 |
| [`08-interconnect`](./samples/08-Chinesezjc-dsh-interconnect.md) | **典型** | **DSH 实例** | 每对端一条持久 WS，投对端 session inbox；**无幂等、无离线队列**，断链即丢 |
| [`14-team-rooms`](./samples/14-PerryLink-dsh-team-rooms.md) | **典型** | **跨会话房间** | 房间存储是权威 + 单写链；但 rc.3 的投影退化（见下），仓库已 archived |
| [`13-agent-relay`](./samples/13-Noelune-dsh-agent-relay.md) | 变体 | **异构运行时** | HTTP broker + 长轮询；机制只在未发布的 0.6–0.8，npm 0.5.0 没有 |

**14 的失效要说得比卡片更准**：不是「宿主拒绝 append」，而是三层叠加——宿主已知事件表不含 `team-room/fact` `[SRC-DSH]` `dsh-session/lib/types/known-event-types.js:21-80`；未标记 `ignorable` 的未知类型不会被当作 surface 保留（`lib/types/surface.js:201-206`）；插件自己的版本策略对 `0.2.x` 判 `forbidden`，于是根本不写这条 fact（目标仓 `src/audit.ts:105-112`）。结果是新日志的 `teamRoom` 投影为空 fold。**「房间是权威」成立，「日志重建」只在旧宿主成立。**

## 3. 三条判据

1. **先问替换的是什么。** 会话（09）可以只换会话、留着进程；实例（08）换的是实例边界而不是机器；机器（06）才谈凭证与远端信任。**说不清替换对象，就会把「跨实例投递」说成「跨机派活」。**
2. **信任边界有三个不同答案，别混。** ACP 是「受信控制器 + 一次性权限提示」；Gateway 是「Peer + 资源级 policy」；插件自建通道是「共享 token / 同步盘」。选哪一种，决定你要不要自己写鉴权。
3. **没有幂等与离线队列，就不要承诺投递。** 08 的 `reqId` 只做关联、超时不重投；13 的 broker 默认回环但无强制校验。**「至少一次」需要消息 id + 去重，两者都不在原生接缝里。**

## 4. 失效与开放问题

- **14 已退役**：仓库 archived、npm deprecated，且新版宿主上投影为空。
- **13 的机制未发布**：0.6–0.8 只在源码里，装着 0.5.0 就没有 wake/长轮询。
- **09 的「恰好一次」靠文件系统原语**：`O_EXCL` 可靠，但残留认领 60s 后才扫，且 scan 只在列目录时触发。
- `[OPEN]` 真实断链后的重投计数、ACP 取消与后续消息的竞态、Gateway 在慢链路上的 uplink 溢出。**下次核法**：B2 试验台起两个本地实例，kill 一端看对端游标与重投。

## 5. 读法

[`01-session-handoff`](./01-session-handoff.md) → [`02-broker-and-relay`](./02-broker-and-relay.md) → [`03-remote-worker-trust`](./03-remote-worker-trust.md) → [`04-acp-remote-execution`](./04-acp-remote-execution.md) → [`05-rooms-and-persistence`](./05-rooms-and-persistence.md)；样本按 09 → 06 → 08 → 14 → 13（变体）。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| Gateway 拒绝发生在 Session 激活前 | `[SRC-DSH]` | `dsh-api-gateway/README.md`（Host 服务节） | 只覆盖非 owner Peer |
| Peer 必填、无默认 | `[SRC-DSH]` | 同上；`lib/index.js:133` | 只覆盖该 Gateway 版本 |
| ACP 每会话单在途提示词 | `[SRC-DSH]` | `dsh-acp/README.md:112` | 只覆盖 ACP v1 服务器 |
| `team-room/fact` 不在宿主已知事件表 | `[SRC-DSH]` | `dsh-session/lib/types/known-event-types.js:21-80` | 未知类型仍可入日志，但非 surface |
| 14 的投影退化为空 fold | `[SRC-TARGET]` | 目标仓 `src/audit.ts:105-112` + `src/facts.ts:66-75` | 插件自设策略，非宿主拒绝 |
