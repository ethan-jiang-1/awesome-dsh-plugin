---
title: "NanmiCoder/dsh-agent-teams"
domain: cross-boundary
kind: sample
positioning: "`NanmiCoder/dsh-agent-teams`：把当前会话变成 captain，成员做成可续聊子代理，磁盘状态 + 事件驱动调度 + JSONL 邮箱。"
takeaway: "磁盘 team.json 为真相源 + idle 边沿调度 + 消息 ack 在准入时。"
read_when: "成员需要被反复追问、记住上一轮、人先批准再派工。"
status: observed
updated: 2026-10-31
---
# 01 · `NanmiCoder/dsh-agent-teams`

> **一句话**:把当前会话变成 captain,成员做成**可续聊子代理**,用磁盘状态 + 事件驱动调度器 + JSONL 邮箱,不造 workflow 引擎。
> **边界**:1 同进程父子 + 2 同工作区多成员 · **过了哪些门**:C + D + G · **证据级别**:`observed`(源码逐文件读过)
> **影响力**(2026-10-31 实时采样):**2592★ / 222 fork / npm 50,995 次/月**;catalog 2026-08-19 快照 573★ → 两个半月 ×4.5
> **什么时候找它**:成员需要被反复追问、需要记住上一轮、需要人先批准再派工

> 导航:[样本索引](../03-sample-encyclopedia.md) · [域章程](../README.md) · [三笔税机制谱](../02-coordination-mechanisms.md) · [四道边界](../01-collab-topology.md)

## 设计思路

**一句话设计思路**:不造 workflow 引擎,把当前会话变成 captain,成员做成**可续聊子代理**,用磁盘状态 + 事件驱动调度器 + JSONL 邮箱把 Claude Code 式的 teammate 体验搬到 DSH 上。作者 README 原话:「without requiring a separate workflow engine」。

**成员是什么**:真子代理,且**可续**。`spawnMember` 走 `startMember(ctx.subagents, {provider, label, request:{parent: captain, persona, toolFilter, agentOptions}})`,成员跨轮、跨宿主重启保留会话。这是它与其余样本最根本的区别——`limuyang2/agent-team` 的成员是**独立根 Agent**,用它自己的架构守卫明令禁止 `parentSession`/`delegationDepth`。

**它为什么必须可续**(本卡最重要的一条推论):子代理的**最终文本不可被程序化读取**,只能作为父通知投递一次。所以凡是需要“队长回头追问成员”的设计,都必须让成员活着。`members.ts` 的模块注释把这条写成了因果链:「Its final assistant message is not readable programmatically, so the member persists its report into the captain's mailbox and the task records」。**成员可续不是炫技,是结果不可读的补丁。**

**子代理做法的三个细节**(可以直接抄的):

1. **调度借 idle 边沿**。`agent/status` 的 idle 触发在锁内**原子认领**一个 ready 任务并唤醒成员;为了让成员不必像 Claude Code teammates 那样轮询,它把 `agent/status` 事件当成调度器的时钟。
2. **邮箱三态 + step 准入**。`deliveryClaimedAt`（60s 租约）→ `deliveredAt` → `readAt`;只有**被 `agent/pre-step` 准入进该 step 的消息才 ack**。代码注释原文:「Acceptance by Harness is not evidence that a model step consumed input」。
3. **执行代际过滤**。邮件带 `attemptId`/`sourceAttemptId`,准入时用 `isCurrentMail` 判过期——上一代 attempt 留下的指令不会污染下一代成员。

**并行度**:等于活跃成员数,默认上限 8——**恰好等于 `dsh-subagent` 的 `maxActiveSubagents` 默认值**。它不是巧合:超出宿主容量的并行度会直接撞 `ACTIVATION_LIMIT_REACHED`。

**代价与具名失效**:`second-process-lost-update`(两进程写同一 `.agent-teams/`);`parked-attempt-orphan`;`spawn-in-flight-race`(spawn 成功但落盘失败 → 子会话存在、花名册不认);`halt-non-anchor`(captain 不驻留时 halt 不收敛成员)。

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | 磁盘 `team.json` 是真相源,会话事件只作审计 | 锁是进程内 promise 链,多进程覆盖写 |
| 冲突裁决 | **不做**。只在完成时审计 `changedPaths`,作者明说不做 worktree | 共享 checkout 完全裸露 |
| 失败收敛 | parked 停驻 + 冷恢复;移除成员时任务回池 | 模型忘调 `update_task` → attempt 永久 parked |

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`NanmiCoder/dsh-agent-teams`](https://github.com/NanmiCoder/dsh-agent-teams) |
| **npm 包名** | `@nanmicoder/dsh-agent-teams`(唯一带 scope 的样本) |
| **版本(本次读)** | `0.1.28` · **声明版本** `0.1.28` |
| **License** | MIT |
| **安装** | `dsh plugin add @nanmicoder/dsh-agent-teams@0.1.28` 或 `github:NanmiCoder/dsh-agent-teams` |
| **附带 CLI** | `dsh-agent-teams-doctor`(可选,bin 字段) |
| **接线方式** | `dsh.bundle.patch` → `cordis.patch.yml`;**还带 `dsh.client.inject`**(有 Web 端 UI) |
| **复现要点** | 桌面端 pnpm 11 默认「最短发布年龄 24h」,装 `@latest` 可能拿到上一版导致 peer 不匹配——**必须钉精确版本**(README:87) |

## 借用指南

### 可借鉴(直接抄)

1. **邮箱三态 ack** ——`deliveryClaimedAt`(60s 租约) → `deliveredAt` → `readAt`,**只有被 `agent/pre-step` 准入进该 step 才 ack**;代码注释写着 `Acceptance by Harness is not evidence that a model step consumed input`。「投递成功」与「被消费」之间那道缝,是所有丢消息 bug 的老家。
2. **调度挂 idle 边沿** ——`agent/status` 空闲时在锁内原子认领一个 ready 任务并唤醒成员,而不是让成员轮询。宿主已经知道谁空了,轮询是在重新发现一件已知的事。
3. **消息带执行代际** ——邮件带 `attemptId`/`sourceAttemptId`,准入时 `isCurrentMail` 判过期,上一代 attempt 的指令不会污染下一代成员。
4. **两段式派工** ——先出花名册与 DAG,人批准,再运行。

### 别照抄

- 把磁盘 `team.json` 当唯一真相源、却用进程内 promise 链当锁——多进程就是覆盖写(`second-process-lost-update`)。
- 还有一件事别误会:**`maxMembers` 默认 8 与宿主 `maxActiveSubagents` 默认 8 相同不是巧合**,它是硬天花板,不是可调参数。
