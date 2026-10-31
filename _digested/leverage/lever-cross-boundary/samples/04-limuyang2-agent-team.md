# 04 · `limuyang2/agent-team`

> **一句话**:先挑助手再建队,每个助手是一套完整配置;入队冻结快照。Leader 只在运行时分配任务,不生成成员。
> **边界**:2 同工作区多成员 · **过了哪些门**:**A**(in-degree 3,全表唯一)+ D · **证据级别**:`observed`(源码逐文件读过)
> **影响力**(2026-10-31 实时采样):**47★ / 7 fork / npm 2,416 次/月**
> **什么时候找它**:每个成员要用**不同的模型/权限/技能包/MCP**

> 导航:[样本索引](../03-sample-encyclopedia.md) · [域章程](../README.md) · [三笔税机制谱](../02-coordination-mechanisms.md) · [四道边界](../01-collab-topology.md)

## 设计思路

**一句话设计思路**:用户在建队前从**助手库**挑人,每个助手是一套完整配置(provider/model/preset/权限/skillAllowlist/mcpServers/instructions);入队时**冻结快照**不可变。Leader 只在运行时分配任务,不生成成员。

**这是本域最诚实的一次取舍**。它要的是「一个成员一套异构配置 + 逐 Session 改权限与思考档位」——而官方 `spawn_teammate` 只带 name/description/prompt。为了拿到这个,它把成员做成**独立根 Agent**(`ctx.agents.create/resume`),并用 `scripts/check-architecture.mjs` **在架构层面禁止** `dsh-subagent`、`parentSession`、`delegationDepth`。

**代价付得非常干脆**:

| 它拿到了 | 它放弃了 |
|---|---|
| 每成员独立 provider/model/preset/权限/Skills/MCP | 运行时 spawn / interrupt / wait 工具 |
| 上下文按成员 Session 隔离 | 依赖图——`dependencyIds` **硬写 `[]`,且没有任何接口能设置** |
| Leader 独占建任务与改派权 | 租约——`leases` 表在 schema 里存在,但全仓只有 `leases: {}` 的清空赋值 |
| 持久 outbox + 幂等键去重 | 文件裁决——`fileScopes` 只是拼进分配消息的**文案** |
| 启动恢复 + 消息重投 | 定时重投(重投只在启动 `recoverTeams` 时发生) |

**「schema 里有、代码里没有」是本卡最值得警惕的一类现象**:读它的 schema 会以为有租约和依赖图,读它的代码才知道两者都是空壳。**验收一个协作插件,必须读到实现,不能读字段表。**

**与官方的共存**:它的服务键是 `agentTeam`,官方是 `agentTeams`——只差一个字母,同装无符号冲突,但**两套团队概念、两个 UI 入口、两块互不相通的任务板**。

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | 宿主 `storageDomain` 5 表 + 持久 outbox | 与官方 `agentTeams` 各写各的盘,任务板互不相通 |
| 冲突裁决 | **完全没有**:`leases` 表是空壳,`fileScopes` 只是拼进消息的文案 | 零仲裁 |
| 失败收敛 | 启动 `recoverTeams` 恢复 + 幂等键重投 | 重投**只在启动时**发生,没有定时重投 |

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`limuyang2/agent-team`](https://github.com/limuyang2/agent-team)(仓库名**不带** `dsh-` 前缀) |
| **npm 包名** | `@limuyang2/dsh-agent-team`(**包名带前缀**,与仓库名不同) |
| **版本(本次读)** | `0.1.4` |
| **License** | MIT |
| **安装** | `dsh plugin add --save-exact @limuyang2/dsh-agent-team@0.1.4`(README:136,**作者本身就要求 `--save-exact`**) |
| **接线方式** | `dsh.bundle.patch` → `cordis.patch.yml` + `dsh.client` |
| **前置条件** | 需要 `pnpm`;README:260 明确写了装不上时的排查第一步就是 `npm install -g pnpm` |

## 借用指南

### 可借鉴(直接抄)

1. **成员=助手模板 + 入队冻结快照** ——配置不可变,比运行时随手改好推理得多。
2. **把架构约束写成 CI 断言** ——`scripts/check-architecture.mjs` 直接禁 `dsh-subagent`/`parentSession`/`delegationDepth`。这条**工程手法本身**比它的团队功能更值钱:凡是「我选了独立根 Agent 就绝不能再退回子代理」这类决心,都该由脚本执行,而不是由文档执行。
3. **leader 独占建任务与改派**,单事务写 outbox + followup,避免多方同时改归属。
4. **启动恢复 + 幂等键重投**。

### 别照抄

- **schema 里有 `leases` 表就当有租约** ——全仓只有 `leases: {}` 的清空赋值;`dependencyIds` 硬写 `[]` 且没有 setter,依赖图根本不存在;`fileScopes` 只是拼进分配消息的文案。
- **读字段表会高估一个协作插件,必须读到实现。
- ** 另外别指望服务键只差一个字母(`agentTeam` vs 官方 `agentTeams`)就能共存出一套统一团队——它们各写各的盘,任务板互不相通。
