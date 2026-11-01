---
title: "NanmiCoder/dsh-agent-teams"
domain: agent-teams
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

> 导航:[样本索引](../../encyclopedia.md) · [域章程](../../00-map.md) · [三笔税机制谱](../../coordination/02-mechanisms.md) · [四道边界](../../coordination/01-taxonomy.md)
> **证据链**：npm 0.1.28 ↔ tag `v0.1.28` ↔ commit `3331b90`；机制、签名与偏差见[`01 源码复核`](../_证据/01-agent-teams-源码复核.md)。

## 设计思路

**一句话设计思路**:不造 workflow 引擎,把当前会话变成 captain,成员做成**可续聊子代理**,用磁盘状态 + 事件驱动调度器 + JSONL 邮箱把 Claude Code 式的 teammate 体验搬到 DSH 上。作者 README 原话:「without requiring a separate workflow engine」。

**成员是什么**:真子代理,且**可续**。`spawnMember` 经 `startMemberWithLenientFilter` 调 `ctx.subagents.start`；spec 除 `provider/label/request{parent,persona,toolFilter,agentOptions}` 外还必填 `prompt` 与 `signal`；rc.3 上 persona/toolFilter 被剥离后经 `runtimeSetup` 装回。成员跨轮、跨宿主重启保留会话。这是它与其余样本最根本的区别——`limuyang2/agent-team` 的成员是**独立根 Agent**,用它自己的架构守卫明令禁止 `parentSession`/`delegationDepth`。

**它为什么必须可续**(本卡最重要的一条推论):子代理**没有可拿来取结果的调用帧**;父收到的 notice 是散文、带 closing message 且可能重复,插件主动忽略它，改用邮箱持久化结构化报告。所以需要“队长回头追问成员”的设计,必须让**会话持久、setup 可恢复**（宿主可冷恢复缺席的 continuable 子会话）。`members.ts` 的模块注释把这条写成了因果链:「Its final assistant message is not readable programmatically, so the member persists its report into the captain's mailbox and the task records」。**成员可续不是炫技,是结果不可读的补丁。**

**子代理做法的三个细节**(可以直接抄的):

1. **调度借 idle 边沿**。`agent/status` 的 idle 触发在锁内**原子认领**一个 ready 任务并唤醒成员;为了让成员不必像 Claude Code teammates 那样轮询,它把 `agent/status` 事件当成调度器的时钟。
2. **邮箱三态 + 准入 ack**。`deliveryClaimedAt`（60s 租约，过期只在 `readPendingMailbox` 生效）→ `deliveredAt` → `readAt`；ack 只发生在 **`agent/pre-step` 准入** 或 **`agent_teams_status` 读取**，reject 不算消费。代码注释原文:「Acceptance by Harness is not evidence that a model step consumed input」。
3. **执行代际过滤**。邮件带 `attemptId`/`sourceAttemptId`,准入时用 `isCurrentMail` 判过期——上一代 attempt 留下的指令不会污染下一代成员。

**并行度**:活跃成员数上限默认 8，与宿主 `maxActiveSubagents` 默认 8 相同；但 `maxMembers` **可配**（`z.natural().min(1)`），源码没有“对齐宿主容量”的表述，超出宿主容量仍会撞 `ACTIVATION_LIMIT_REACHED`——**默认值相同，不等于硬天花板**。

**代价与具名失效**:`second-process-lost-update`(两进程写同一 `.agent-teams/`，上游无此术语，属 `[OBS]` 命名);`parked-attempt-orphan`(本进程内停驻，需显式动作或冷启动恢复一次);`spawn-in-flight-race`(只剩进程崩溃窗口，正常失败有补偿);`halt-non-anchor`(captain 不驻留时 halt 不收敛成员)。

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | 磁盘 `team.json` 是真相源,会话事件只作审计 | 锁是进程内 promise 链,多进程覆盖写 |
| 冲突裁决 | **不做**。只在完成时审计 `changedPaths`；**源码没有 worktree 支持**（不是 README 明说的设计边界） | 共享 checkout 完全裸露 |
| 失败收敛 | parked 停驻 + 冷恢复;移除成员时任务回池 | 模型忘调 `update_task` → attempt 永久 parked |

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`NanmiCoder/dsh-agent-teams`](https://github.com/NanmiCoder/dsh-agent-teams) |
| **npm 包名** | `@nanmicoder/dsh-agent-teams`（本册还有其它带 scope 的包，非唯一） |
| **版本(本次读)** | `0.1.28` · **声明版本** `0.1.28` |
| **License** | MIT |
| **安装** | `dsh plugin --profile web add --save-exact @nanmicoder/dsh-agent-teams@0.1.28`（README 精确命令）或 GitHub 安装 |
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
