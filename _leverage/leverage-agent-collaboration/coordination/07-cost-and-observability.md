---
title: "成本、容量与观测：把三笔税变成可读的数"
domain: agent-coordination
kind: playbook
positioning: "判断层第二篇：三层额度、七个可测指标、宿主可观测面与验收五问；回答十问的 8/9。"
takeaway: "先定额度（宿主池/编排上限/预算），再选指标（token、重投、stale、人工介入），最后用验收五问收口；测不了的项一律 [OPEN]。"
read_when: "要估一个协作方案的成本、给团队设并发/预算，或验收一个多 agent 系统。"
status: living
updated: 2026-11-01
budget: 125
---
# 成本、容量与观测

> 三笔税（状态/冲突/收敛）谈的是**正确性**；这一篇谈**代价**：谁会撞上限、钱花在哪、坏了怎么看见。
> **原则**：能量化的写成数，不能量化的写成 `[OPEN]`；不要把「感觉快了」当结论。

## 1. 三层额度（从下到上，任一层都能卡死你）

| 层 | 额度 | 超了会怎样 | 证据 |
|---|---|---|---|
| **宿主池** | `maxDepth` 默认 1；`maxActiveSubagents` 默认 8 | 抛 `ACTIVATION_LIMIT_REACHED`，**不排队** | `[SRC-DSH]` `dsh-subagent/lib/index.js:2979-2980`、`:1046-1047` |
| **编排上限** | 模板默认 `4 并发 / 100 节点次 / 10 分钟`；宿主 ceiling `16 / 1000 / 1h`；并发硬顶 64 | 模板值被 `min` 压回；超限报错或截断 | `[SRC-TARGET]` 样本 18 `lib/core/limits.js:4-27,47-54` |
| **预算** | token、审批次数、人工时间 | 看不见，只能从日志估 | 见 §2 |

**判据**：评估一个方案，先问「它的并发上限是谁定的」。如果答案是「插件自己配的」而没有 ceiling，那它迟早会撞宿主池。

## 2. 七个可测指标

| # | 指标 | 怎么读 | 为什么重要 |
|---|---|---|---|
| 1 | **token / 任务** | `ctx.tokenMeter` 的 `tokenUsage`（uncached/cache/output 四桶） | 多 agent 的系统性成本；按任务归一，别报总量 |
| 2 | **上下文压力** | `contextPressure` / `contextBreakdown` | 接近上限先压缩或换子代理，不是加更多成员 |
| 3 | **并发峰值 / 撞限次数** | 宿主池 vs 编排上限 | 撞限=失败重试，不是「忙」 |
| 4 | **重投 / 重复投递** | 邮箱三态（`deliveryClaimedAt` → `deliveredAt` → `readAt`） | 没有幂等键的通道，重试就是重复执行 |
| 5 | **stale / 孤儿记录** | 任务板 owner、租约、claim 边车 | 崩溃残留；不清理会永久占位 |
| 6 | **收敛步数 / 时长** | run journal / 事件 seq | 收敛慢通常是调度或唤醒问题，不是模型问题 |
| 7 | **人工介入次数** | `approval/asked` + `approval/decided` 审计对 | 它是预算，不是参与度；越高不一定越好 |

**统一口径**：前六个都是「每任务」而不是「每小时」；第七个是「每任务/每人」。**口径不一致的对比没有意义。**

## 3. 宿主能读到什么（不用自己造）

- **token 与上下文**：`ctx.tokenMeter` 估算会话的请求与上下文压力，或给单条消息计价；它**回放持久会话日志**、确定性、不调模型，`tokenUsage` / `contextPressure` / `contextBreakdown` 可直接消费 `[SRC-DSH]` `dsh-token-meter/README.zh.md`（概述节）、`lib/index.js:316-368`。
- **状态**：`agent/status` 只有 `idle` / `running` `[SRC-DSH]` `dsh-agent-loop/lib/index.js:791,798`；更细的「空闲多久」要自己记。
- **消息**：`agent/inbox/spliced` 是读取侧的事实来源，`next-turn` / `next-step` 两目标 `[SRC-DSH]` `dsh-experimental-agent-team/lib/index.js:772-775`。
- **审批**：`approval/asked` 与 `approval/decided` 成对落日志，可当审计与预算 `[SRC-DSH]` `dsh-user-approval/lib/index.js:139`。
- **后台工作**：`run_in_background` 注册为 `ctx.jobs` 任务，有 `job_output` / `job_kill` `[SRC-DSH]` `dsh-tool-workflow/README.md:42`。

**没有现成的东西**：跨成员的「任务级」成本汇总、收敛时延、重投统计。这些要么自己从事件折叠，要么用 §2 的口径自己记。

## 4. 验收五问（发布前逐条回答）

1. **失败可读吗？** 被拒（`denied`）、过期（`stale`）、版本不容（`blocked`）分别能在哪里查到？
2. **指标可查询吗？** token、重投、stale、人工介入，至少三个能按任务拉出来。
3. **可复现吗？** 关键结论有 R 号或行号；没有就标 `[OPEN]`（本册的口径见 [`_证据/00`](../_证据/00_实测环境与账本.md)）。
4. **崩溃后剩什么？** 会话日志、journal、worktree、队列各自留下什么，谁清理。
5. **谁付钱？** token 预算、并发上限、审批人时，分别由谁承担、超了怎么办。

## 5. 最小仪表盘（够用即可）

| 面板 | 数据源 | 采样 | 告警线 |
|---|---|---|---|
| 任务成本 | `tokenUsage` 按任务聚合 | 任务结束 | 超预算 ×1.5 |
| 上下文压力 | `contextPressure` | 每步 | > 80% 容量 |
| 并发与撞限 | 宿主池 + 编排上限 | 运行中 | 撞限 > 0 就查 |
| 失败面 | denied / stale / blocked | 每小时 | stale > 阈值 |
| 人工介入 | approval 审计对 | 每天 | 单任务 > 3 次 |

**别做**：用 ★/下载量当质量指标；只报成功率不报成本；把审批次数当活跃度。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 宿主池默认 1/8，耗尽抛错不排队 | `[SRC-DSH]` | `dsh-subagent/lib/index.js:2979-2980,1046-1047` | 只覆盖 rc.3 |
| `ctx.tokenMeter` 可读四桶与上下文压力 | `[SRC-DSH]` | `dsh-token-meter/README.zh.md`、`lib/index.js:316-368` | 估算含固定启发式，不等于账单 |
| 审批审计成对落日志 | `[SRC-DSH]` | `dsh-user-approval/lib/index.js:139` | 只覆盖该服务版本 |
| 七个指标的口径 | `[OBS]` | 本册 18 样本与 R0–R7 | 经验框架，可增删 |
