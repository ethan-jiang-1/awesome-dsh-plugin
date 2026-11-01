---
title: "主-子代理：一次委派怎么发生"
domain: agent-delegation
kind: index
positioning: "`delegation/` 家族：dsh-subagent 宿主契约、continuable vs one-shot、结果回传与消息权威、模型路由/包装 provider。"
read_when: "要设计主-子委派，或判断子代理能不能续、结果怎么拿。"
status: living
updated: 2026-11-01
---
# 主-子代理：一次委派怎么发生

> 主-子代理家族：先读宿主契约，再看样本怎么在接缝上做路由。

## 样本与证据

| 样本 | 证据链 |
|---|---|
| [`15-Garybot126-dsh-subagent-models.md`](./samples/15-Garybot126-dsh-subagent-models.md) | [`15-subagent-models-源码复核.md`](./_证据/15-subagent-models-源码复核.md) |
| [`16-tkaiz0406-dsh-subagent-route-pin.md`](./samples/16-tkaiz0406-dsh-subagent-route-pin.md) | [`16-route-pin-源码复核.md`](./_证据/16-route-pin-源码复核.md) |
| [`17-aleskxyz-dsh-subagent-fork-lite.md`](./samples/17-aleskxyz-dsh-subagent-fork-lite.md) | [`17-fork-lite-源码复核.md`](./_证据/17-fork-lite-源码复核.md) |

## 章节

- [`01-host-contract.md`](./01-host-contract.md)：dsh-subagent 的深度/容量/权限/结果回传。
- [`02-fork-and-resume.md`](./02-fork-and-resume.md)：fork/外部一次性/冷恢复的差别。

## 证据与边界

- 证据规约见 [`../EVIDENCE.md`](../EVIDENCE.md)；跨家族对照见 [`../encyclopedia.md`](../encyclopedia.md)。
- 章节已成稿；引用样本机制前先读其 memo，冲突以章节与卡片为准。
