---
title: "COMPAT · 兼容性墙：17 张样本在 rc.3 上还剩什么"
domain: agent-collab
kind: guide
positioning: "18 张样本的生命状态与 rc.3 失效点：4 类状态、8 张阻断、逐条证据；回答十问第 10 问。"
read_when: "要引用某个样本前先确认它还成不成立，或判断「机制可学」与「能装」的差别。"
status: living
updated: 2026-11-01
budget: 110
---
# 兼容性墙

> **一句话**：机制可学，不等于能装。本表回答 [`00-map` §4](../00-map.md#4-十个问题全册的验收尺子) 的第 10 问。
> 基线：`@deepseek-ai/dsh@0.2.1-rc.3`；样本版本以各卡页头为准。

## 1. 四种生命状态

| 状态 | 含义 | 处置 |
|---|---|---|
| **active** | 在 npm 且有证据表明可用 | 正常引用；带 `*` 表示 peer 范围未逐卡复核 |
| **unpublished** | 不在 npm，或机制只在源码里 | 可学机制；引用时写明安装来源 |
| **blocked** | 发布物或宿主版本不容 | 只能当机制教材，不能当可安装件 |
| **retired** | 仓库归档/包下架，或宿主已废其关键事件 | 只留教训；不推荐安装 |

## 2. 全表（18/18）

| # | 样本 | 族 | 分级 | 生命状态 | 能装吗 | rc.3 上的状态 / 失效点 | 证据 |
|---|---|---|---|---|---|---|---|
| 01 | `agent-teams` | T1 | 典型 | active* | 是 | 可用；persona/toolFilter 被剥离后经 runtimeSetup 装回 | `teams/_证据/01` |
| 02 | `team-gui` | T1 | 变体 | unpublished | 仅 GitHub | npm 404；只有 release 资产 tgz | `teams/_证据/02` |
| 03 | `dsh_workflow` | P1 | 典型 | unpublished | 仅 GitHub | `@dsh-external/workflow` 未发布；安装走 GitHub | 卡 03 §精确坐标 |
| 04 | `agent-team` | T2 | 典型 | blocked | 否 | 21 个 peer 均 `^0.1.1-rc.2`，无 `engines.dsh` | 卡 04 L75 |
| 05 | `teams-x` | T1 | 变体 | blocked | 否 | 0.11.5 从未发布；npm 0.2.0 安装缺 `scripts`，且**无跨进程锁**（R5） | 卡 05 · R5 |
| 06 | `remote-agent` | C3 | 典型 | active* | 是 | 未见阻断证据；peer 未逐卡复核 | `crossing/_证据/06` |
| 07 | `file-claim` | X1 | 典型 | active* | 是 | 可用；无 epoch 是设计缺口，不是兼容问题 | `coordination/_证据/07` |
| 08 | `interconnect` | C2 | 典型 | active | 是 | 0.13.0 可用；无幂等/离线队列是设计缺口 | 卡 08 §精确坐标 |
| 09 | `takeover` | C1 | 典型 | unpublished | 仅 GitHub | npm 404；tag 指向自述 0.4.2 的树 | 卡 09 §精确坐标 |
| 10 | `expert-mode` | T3 | 典型 | blocked | 否 | 无 preset 声明 + 写进无人读的目录；persona 被拒；`persona.text` 字段过时；`workflow-worker-thread` 不在安装树 | 卡 10 L28-31 |
| 11 | `taskswarm` | P2 | 典型 | retired | 否 | npm 全量下架，安装串 404；只能源码装 | 卡 11 §精确坐标 |
| 12 | `eteams` | T1 | 变体 | blocked | 否 | persona 走请求参数仅 0.1.x；rc.3 已无 `startContinuable` | 卡 12 L5 |
| 13 | `agent-relay` | C2b | 典型 | unpublished | 部分 | 0.6–0.8 未发布；npm 0.5.0 没有 wake/长轮询 | 卡 13 L14 |
| 14 | `team-rooms` | C4 | 典型 | retired | 否 | 仓库 archived（2026-10-05）+ npm deprecated；新宿主 `teamRoom` 投影为空 fold | `crossing/_证据/14` |
| 15 | `subagent-models` | D1 | 变体 | active* | 是 | 可用；README 的 preset 优先级与模型校验在实现里不存在 | `delegation/_证据/15` |
| 16 | `route-pin` | D1 | 典型 | active | 是 | 可用；生效的是 `startActivation` 钩子，不是 `provider.start` | `delegation/_证据/16` |
| 17 | `fork-lite` | D2 | 典型 | blocked | 否 | peer 全为 0.1.x；capabilities 声明 5 键而 rc.3 只有 4 键 | 卡 17 L5,L36 |
| 18 | `agent-dag-workflow` | P3 | 典型 | active | 是（npm） | 1.0.1 在 npm；DSH 适配需要 `workflow*` 服务，否则回落内存实现 | 卡 18 · memo 18 |

**统计**：active 7（其中 4 张 peer 未逐卡复核）· unpublished 4 · blocked 5 · retired 2。**8 张有阻断性问题**：04/05/10/11/12/13/14/17。

## 3. 三条可复用的教训

1. **宿主的事件表与类型面是最脆的依赖。** 14 死于已知事件表不含 `team-room/fact`；17 死于 capabilities 键数；10/12 死于 persona 字段搬迁。**引用样本前先看它 pin 的是哪条宿主线。**
2. **「npm 上有」不等于「装得上」。** 05 的安装脚本没进包、09/03 根本不在 npm。**装不装得上要用发布物验证，不看 README。**
3. **退役样本仍然有价值，但只能当教训。** 11 的 worktree 故障档案、14 的单写链设计，都比它们的可用性更有价值。

## 4. 复核触发

| 触发 | 动作 |
|---|---|
| DSH 基线升到 rc.4 | 全表重判；blocked 项逐条看是否解禁 |
| 某样本重新发布或复活 | 状态改回 active，重评证据等级 |
| 宿主新增/删除 Team 事件 | 重跑 14 的投影检查 |
| 新样本入册 | 先在本表占一行，再写卡 |

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 8 张有阻断性问题 | `[SRC-TARGET]`/`[DOC]` | 各卡与 memo 的版本/peer/安装段 | 依赖核对时点 2026-11-01 |
| `team-room/fact` 不在 rc.3 已知事件表 | `[SRC-DSH]` | `dsh-session/lib/types/known-event-types.js:21-80` | 未知类型仍可入日志，只是非 surface |
| `*` 的 4 张 peer 未复核 | `[OPEN]` | 本轮只读了机制段，未逐个 `npm view peerDependencies` | 复核动作：`npm view <pkg> peerDependencies engines` |
