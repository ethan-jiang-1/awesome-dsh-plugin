---
title: "怎么借：Agent 协作的选型与抄法"
domain: agent-collab
kind: guide
positioning: "按协作家族路由：先判断你缺的是委派、编队、流水线还是跨界，再给最小集、三笔税与回源入口。"
read_when: "要做多 agent 方案、比较团队/流水线/跨机做法，或评审一个协作设计。"
status: living
updated: 2026-11-01
---
# 怎么借：Agent 协作

## 0. 先判断你缺哪一类

| 你的问题 | 家族 | 先读 |
|---|---|---|
| 一次委派怎么发生、能不能续、结果怎么拿 | 主-子代理 | [`delegation/README`](./delegation/README.md) |
| 多成员怎么编队、谁调度、任务板归谁 | 团队 | [`teams/README`](./teams/README.md) |
| 控制流用 DAG 还是代码、重放/暂停怎么做 | 流水线 | [`pipelines/README`](./pipelines/README.md) |
| 跨会话/实例/机器怎么接 | 跨会话/实例/机器 | [`crossing/README`](./crossing/README.md) |
| 状态/冲突/失败收敛怎么比 | 横向 | [`coordination/README`](./coordination/README.md) |

## 1. 三笔税（任何协作方案都要回答）

1. **状态归谁**：roster、任务、消息、证据的权威副本在哪（进程内 / 磁盘 / broker / 宿主日志）。
2. **冲突谁裁决**：共享 checkout 有没有真拦截；没有 fencing 的“锁”只是别人写你会被拒。
3. **崩了谁收敛**：重启后是恢复到断点、整体重跑，还是留下 stale 记录要人工 `--force`。

## 2. 家族最小集

- **delegation**：深度/容量默认值、continuable vs one-shot、结果回传通道、消息权威。
- **teams**：roster 与 captain、调度触发（idle/邮箱）、ack 语义、任务板与质量门。
- **pipelines**：图还是代码、缓存键、暂停/恢复、幂等与失败保留。
- **crossing**：会话替换对象、broker/relay 鉴权、远端 worker 信任、持久化游标。

## 3. 回源纪律

- 每个样本先读卡头「证据链」→ 同家族 `_证据/NN-*-源码复核.md`；memo 里有 npm/tag/commit、偏差表与 `[OPEN]`。
- 不要把 README 当实现；不要把宿主行为当目标行为。
- 未验证行为保留 `[OPEN]`，不写成保证。

## 证据与边界

- 规程见 [`EVIDENCE.md`](./EVIDENCE.md)；样本索引见 [`encyclopedia.md`](./encyclopedia.md)。
- 本文件只做路由；具体机制与代价以样本卡/章节为准。
