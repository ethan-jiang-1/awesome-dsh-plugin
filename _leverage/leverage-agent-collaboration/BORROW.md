---
title: "怎么借：八条协作配方"
domain: agent-collab
kind: guide
positioning: "从 18 个样本里收出的八条可抄做法：触发问题、动作、抄错后果与回源；先过「单 vs 多」再进家族。"
read_when: "要做多 agent 方案、评审协作设计，或想知道某条做法抄错会怎样。"
status: living
updated: 2026-11-01
budget: 95
---
# 怎么借：八条协作配方

> **先决定要不要做多 agent**：默认单 agent；三样买点（并行上下文 / 独立验证 / 异构角色）一样都不占，就停在这里，回 [`06`](./coordination/06-when-not-multi-agent.md)。
> 配方只给「条件 + 动作 + 抄错后果」；机制细节与代价在样本卡/章节，不自成一套。

## 0. 还没定位？先按问题分流

| 你的问题 | 去哪 |
|---|---|
| 该不该多 agent | [`coordination/06`](./coordination/06-when-not-multi-agent.md) |
| 一次委派怎么发生、能不能续 | [`delegation/README`](./delegation/README.md) |
| 多成员怎么编队、任务板归谁 | [`teams/README`](./teams/README.md) |
| 图还是代码、重放怎么做 | [`pipelines/README`](./pipelines/README.md) |
| 跨会话/实例/机器怎么接 | [`crossing/README`](./crossing/README.md) |
| 状态/冲突/收敛怎么比 | [`coordination/README`](./coordination/README.md) |

## 1. 八条配方

### 1. 先判「单 vs 多」

- **触发**：有人提议「上多 agent」。
- **动作**：按 [`06`](./coordination/06-when-not-multi-agent.md) 五步判定——写入是否单线程、任务能否切独立方向、是否需要独立验证、成本付不付得起、失败是否可观测。
- **抄错后果**：跳过判定直接搭团队，最后买到的是 15× token 和更多失败面。

### 2. 委派：先定可续性

- **触发**：一个 agent 要叫另一个干一件事。
- **动作**：要追问/冷恢复 → 本地可续；只要一次结果 → 外部执行；路由钉在 `startActivation`（[`delegation/01`](./delegation/01-host-contract.md)）。
- **抄错后果**：把 `provider.start` 当委派入口，路由静默失效（样本 16）。

### 3. 团队状态：日志还是文件

- **触发**：要 roster + 任务板。
- **动作**：优先放会话日志（原生 `team/member` / `team/task` + CAS）；要跨进程才用自有文件，并自己解决并发（[`teams/README`](./teams/README.md)）。
- **抄错后果**：磁盘 + 进程内锁，两进程丢更新（R4a/R4b）。

### 4. 写冲突：只有 `pre-execute` deny 真拦

- **触发**：两个成员可能改同一文件。
- **动作**：拦截写在 `tools/pre-execute`，返回 deny；覆盖工具列清楚（样本 [`07`](./coordination/samples/07-Nwflower-dsh-file-claim.md)）。
- **抄错后果**：写成提示词约定，等于没有拦截。

### 5. 文件隔离：worktree，不是锁

- **触发**：并行写同一仓库。
- **动作**：每 lane 一个 worktree + 集成树；记住 worktree 只带**已提交**文件（样本 [`11`](./pipelines/samples/11-february2015-dsh-taskswarm.md)、R7）。
- **抄错后果**：以为 worktree 连未跟踪文件一起隔离，合并时才发现。

### 6. 编排：脚本还是模板 DAG

- **触发**：多步、可能暂停/恢复。
- **动作**：一口气跑完 → 代码即编排（[`03`](./pipelines/samples/03-omdsh-dev-dsh_workflow.md)）；要断点/人工审批/取证重放 → 声明式模板 + checkpoint（[`18`](./pipelines/samples/18-GM-HZ-agent-dag-workflow.md)）。
- **抄错后果**：把「有 DAG」当「能暂停」——没有 journal 就恢复不了。

### 7. 跨实例：直连还是 broker

- **触发**：两个 DSH 实例/异构运行时互通。
- **动作**：只要投消息 → 直连 WS（[`08`](./crossing/samples/08-Chinesezjc-dsh-interconnect.md)）；要离线队列/幂等/唤醒 → broker（[`13`](./crossing/samples/13-Noelune-dsh-agent-relay.md)）。
- **抄错后果**：用直连却承诺「消息不丢」——它没有离线队列与幂等键。

### 8. 成本与验收：三层额度 + 五问

- **触发**：方案要上线。
- **动作**：写清宿主池 / 编排上限 / 预算；按 [`07`](./coordination/07-cost-and-observability.md) 的验收五问答一遍；用 [`CHECKLIST`](./practice/CHECKLIST.md) 过一遍。
- **抄错后果**：没有额度，第一次并发高峰就撞宿主池；没有指标，坏了只能猜。

## 2. 三笔税（任何方案都要回答）

1. **状态归谁**：roster、任务、消息、证据的权威副本在哪。
2. **冲突谁裁决**：共享 checkout 有没有真拦截；没有 fencing 的「锁」只是别人写你会被拒。
3. **崩了谁收敛**：恢复到断点、整体重跑，还是留下 stale 记录要人工 `--force`。

## 3. 回源纪律

- 每条配方先读对应卡头「证据链」→ 同家族 `_证据/`；memo 有 npm/tag/commit、偏差表与 `[OPEN]`。
- 不要把 README 当实现；不要把宿主行为当目标行为。
- 未验证行为保留 `[OPEN]`，不写成保证。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 八条配方各自可回源到样本或 R 记录 | `[SRC-TARGET]`/`[RUN]` | 各条内联链接 | 配方是下限，不是全部做法 |
| 「三样买点」是决策框架 | `[OBS]` | [`06`](./coordination/06-when-not-multi-agent.md) | 非实验结论 |
| 「抄错后果」取自样本的失效面 | `[OBS]` | 各样本卡「别照抄」段 | 描述性，不是概率 |
