# 05 · `Mlte0907/dsh-teams-x`

> **一句话**:与 `agent-teams` 同骨架,但更轻、更贴官方包;唯一主动做「官方限制逐条对照」的样本。
> **边界**:1 同进程父子 + 2 同工作区多成员 · **过了哪些门**:D + G · **证据级别**:`observed`(源码逐文件读过)
> **影响力**(2026-10-31 实时采样):**3★ / npm 89 次/月**;能力披露 9 项(本域最高)
> **什么时候找它**:想要质量门自动派生返工、且愿意接受「软收敛,无硬超时」

> 导航:[样本索引](../03-sample-encyclopedia.md) · [域章程](../README.md) · [三笔税机制谱](../02-coordination-mechanisms.md) · [四道边界](../01-collab-topology.md)

## 设计思路

**一句话设计思路**:和 `agent-teams` 同一骨架(captain 是主会话、成员是持久子代理、磁盘状态 + JSONL 信箱 + 依赖感知 DAG + 质量门),但**更轻、更贴官方包**。

**它做了官方最要命那三条限制的逐条对照**,这是本域唯一一份主动自评的样本:

| 官方限制 | 它做到哪 |
|---|---|
| 共享 checkout 无隔离 | **未解决** |
| 单进程 | **未解决** |
| owner 不自动释放 | **部分缓解**:`drainChildren` + 退役成员守卫 + 搁浅任务回池 |

它自己的收尾很克制:**无心跳、无硬超时**,定位为「软收敛」——60s 对账回收搁浅任务,会话消失 5min 判 orphan 回池,停车 30min/运行 60min **各提醒一次**。

**质量门的设计**比 `agent-teams` 更显式:建任务时校验 objective/acceptance/inScope/verify,两个写类任务的 inScope 不得重叠(要求串行化);完成时 review/requirements 必须 `verdict='pass'` 且无 high/blocker,`commandsRun` 有 failed **禁止** completed;review 打回自动派生 repair(上限 3 轮、同源去重、源修复后级联取消兄弟)。

**但它的质量门是「格式与承诺的校验」,不是事实验证**:`verify` 只是字符串清单,插件**不执行**命令,`changedPaths` 由成员自述。唯一的结构性防自审是提示词里一句「Do not approve your own implementation」。

**工程侧面值得记**:它的 `sdd/` 三件套**不是团队架构文档**,而是 `/teamsx` 空态提示这一个特性的 spec/design/tasks;价值在工艺——What/How/Order 严格分层、EARS 需求 + 验收条件、硬约束先行、裁决表(备选方案多维对比 → 裁决 → 理由)、非目标 O-1~O-7 逐条写死。

**它与官方的互斥声明**:**全仓未点名任何一句**,既没说替代也没说并存。只有 `tsdown.config.ts` 里一处 `dsh-agent-teams` 字样与 prepublish guard 禁止产物含该名——**它防的是被误认成别家,不是声明关系**。

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | 磁盘 `.teams-x/<teamId>/` + JSONL 信箱 | 锁仍是进程内;成员正式路径要同机 harness 源码 |
| 冲突裁决 | **不做**。质量门在完成时校验 `changedPaths`,但不执行 verify 命令 | 自述当证据;防自审只靠提示词一句 |
| 失败收敛 | 60s 对账器 + 5/30/60 分钟软阈值 | 自认**无心跳、无硬超时**,只是「软收敛」 |

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`Mlte0907/dsh-teams-x`](https://github.com/Mlte0907/dsh-teams-x) |
| **npm 包名** | `dsh-teams-x` |
| **版本(本次读)** | `0.11.5` |
| **License** | MIT |
| **安装** | 两条:`npm i dsh-teams-x && dsh plugin --profile web add <node_modules 路径>/dsh-teams-x`;或 `git clone` 后 `pnpm install` |
| **接线方式** | `dsh.bundle.patch` → `cordis.patch.yml` + `dsh.client` |
| **复现要点** | README:21——装完**必须重启宿主**,`dsh plugin add` **不会热加载新 bundle**。这条对多数样本都成立 |

## 借用指南

### 可借鉴(直接抄)

1. **在建任务与完成两处都卡质量门**,不只在完成时。
2. **review 打回自动派生 repair** ——上限 3 轮、同源去重、源修复后级联取消兄弟任务。
3. **软收敛要分级并如实声明**:60s 对账回收搁浅、会话消失 5min 判 orphan 回池、停车 30min / 运行 60min 各提醒一次,同时明写「**无心跳、无硬超时**」。**把做不到的说出来**,比假装有超时更可信。
4. **`sdd/` 的文档工艺**:EARS 需求 + 验收条件、裁决表(备选多维对比 → 裁决 → 理由)、非目标 O-1~O-7 逐条写死。这套工艺与本域无关,但可以整体搬到任何插件设计里。

### 别照抄

- 质量门只校验「格式与承诺」不执行 `verify`——`verify` 是字符串清单,`changedPaths` 由成员自述,插件一条命令都不跑;唯一的结构性防自审只是提示词里一句「Do not approve your own implementation」。
- 也没有 message-id 幂等,却做了投递重试。
