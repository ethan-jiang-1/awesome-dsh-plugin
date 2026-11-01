---
title: "Agent 协作册：主-子、团队、流水线、跨界"
domain: agent-collab
kind: index
positioning: "独立册入口：四家族 + 横向协调卷；17 个样本按主家族归位，证据 memo 与选型判定树可直达。"
read_when: "要判断自己的多 agent 方案属于哪类、怎么选型；或第一次进本册。"
status: living
updated: 2026-11-01
---
# Agent 协作册

> **标语**：*Who collaborates with whom, who owns the state, who converges?*
> 同样是不改上游，协作方案的分水岭不在“能开几个 agent”，而在**状态寄生在哪、冲突谁裁决、崩了谁收敛**。

## 0. 三个入口

| 你要 | 去哪 | 拿到 |
|---|---|---|
| **选型**：我的方案属于哪类 | [00-map §5 判定树](./00-map.md#5-判定树) | 四家族判定 + 三笔税 |
| **抄做法**：按任务找最小集 | [BORROW](./BORROW.md) | 家族路由 + 最小集 + 回源纪律 |
| **查样本**：横向比较 17 个样本 | [encyclopedia](./encyclopedia.md) | 主家族/交叉角色/证据链 |

## 1. 四家族 + 横向卷

| 卷 | 一句话问题 | 已有样本 |
|---|---|---|
| [delegation 主-子代理](./delegation/README.md) | 一次委派怎么发生、能不能续、结果怎么回 | 待补（DSH 契约先行） |
| [teams 团队](./teams/README.md) | 多成员如何编队、调度、共享任务板 | 01/02/04/05/10/12 |
| [pipelines 流水线](./pipelines/README.md) | 控制流怎么写、重放/暂停/幂等怎么做 | 03/11 |
| [crossing 跨会话/实例/机器](./crossing/README.md) | handoff、broker、远端 worker、房间 | 06/08/09/13/14 |
| [coordination 横向](./coordination/README.md) | 状态归属、冲突裁决、失败收敛、容量 | 07 + 跨家族对照 |

## 2. 怎么读（只挑一条）

- **要搭团队**：teams 的样本卡（先读 01 与 04 的对照）→ coordination 的三笔税 → BORROW 最小集。
- **要搭流水线**：pipelines 的 03（代码即编排）与 11（worktree lane）→ 再看缺少的声明式 DAG 章节。
- **要跨机/跨会话**：crossing 的 06/08/09/13/14 → 先确认“替换的是会话还是进程”。
- **要评审**：00-map §5 判定树 + coordination 的三问（状态/冲突/收敛）。

## 3. 与其他册的边界

| 主题 | 归哪册 |
|---|---|
| 质量门禁、证据回执、完成判据 | [`../leverage/lever-prove-output/`](../leverage/lever-prove-output/README.md) |
| 权限、审批预算、沙箱、网络准入 | [`../leverage/lever-draw-limit/`](../leverage/lever-draw-limit/README.md) |
| 插件/profile/独立壳的产品化 | [`../leverage-reshape-product/`](../leverage-reshape-product/README.md) |
| 协作结构、状态、冲突、失败收敛 | **本册** |

## 证据与边界

- 迁移自 `leverage/lever-cross-boundary`；17 个样本与 memo 一一保留（见 [catalog](./catalog.md)）。
- 证据规约：[EVIDENCE](./EVIDENCE.md)；本册仍在扩写，delegation/pipelines 的空白已列入 [00-map §9](./00-map.md#9-空白区后续批次)。
