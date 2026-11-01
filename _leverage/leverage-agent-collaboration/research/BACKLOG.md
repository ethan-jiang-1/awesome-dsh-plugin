---
title: "BACKLOG · 分诊结果与缺口候选"
domain: agent-collab
kind: index
positioning: "18 张样本的机制族分诊（14 典型 + 4 变体）、生命状态，以及十问缺口的候选方向与不立卡理由。"
read_when: "要补样本、想知道某张卡为什么是变体/退役，或某个问题为什么还没有卡。"
status: living
updated: 2026-11-01
budget: 115
---
# BACKLOG · 分诊与缺口

> **规则**：候选先过 [`00-map` §7](../00-map.md#7-三道门先过门再立卡) 三道门；不过就留一行，**不立卡、不占卡位、不进 catalog**。
> 本表是分级与去重的**决定记录**；卡片上的 `tier` 由 B4 批次统一写入。

## 0. 分诊口径

- **机制族**：一个「状态归属 + 控制流」的组合。同族只留一个典型。
- **分级**：典型 / 变体 / 反例（[`00-map` §9](../00-map.md#9-样本分级与强制去重)）。
- **生命状态**：`active` / `retired` / `unpublished` / `blocked`（与分级正交，进 `reference/COMPAT.md`）。

## 1. 分诊表（18/18）

| # | 样本 | 机制族 | 分级 | 生命状态 | 理由 |
|---|---|---|---|---|---|
| 01 | `NanmiCoder/dsh-agent-teams` | T1 有状态团队运行时 | **典型** | active | captain + 可续子代理 + 磁盘 team.json + idle 边沿调度，本族最完整骨架 |
| 02 | `toolclub/dsh-agent-team-gui` | T1 | 变体 | unpublished | 与 01 同族；差异在 pre-step 派工与 on-demand 调度。细节留 memo |
| 05 | `Mlte0907/dsh-teams-x` | T1 | 变体 | blocked | 与 01 同骨架；差异在质量门自动返工 + 跨进程文件锁。0.11.5 从未发布 |
| 12 | `2507483326/dsh-eteams` | T1 | 变体 | blocked | 与 01 同族；差异在 SQLite + persona 走请求参数。该参数仅 0.1.x 成立 |
| 04 | `limuyang2/agent-team` | T2 独立根 Agent 团队 | **典型** | blocked | 成员是独立根 Agent（禁 parentSession），与 T1 是成员模型的分水岭；peer 不含 rc.3 |
| 10 | `Asher-2000/dsh-expert-mode` | T3 无插件路线 | **典型** | blocked | 全册唯一「不写插件、用 composition 写协作」；rc.3 五处硬伤，正好当兼容性教材 |
| 16 | `tkaiz0406/dsh-subagent-route-pin` | D1 子代理模型路由 | **典型** | active | rc.3 上真正生效的是 `startActivation` 钩子，是接缝事实的锚 |
| 15 | `Garybot126/dsh-subagent-models` | D1 | 变体 | active | 与 16 同族；差异在 `agent/request` 覆写而非 provider 包装 |
| 17 | `aleskxyz/dsh-subagent-fork-lite` | D2 子代理上下文窗口 | **典型** | blocked | 唯一「截断 fork seed」样本；面向 0.1.x，peer 与 capabilities 均不含 rc.3 |
| 03 | `omdsh-dev/dsh_workflow` | P1 可重放编排 | **典型** | unpublished | 不可变胶囊 + 内容键缓存，本册唯一可重放机制 |
| 11 | `february2015/dsh-taskswarm` | P2 文件隔离 | **典型** | retired | 每 lane 一个 worktree；npm 已全量下架，只能源码参考 |
| 09 | `IKEASven69/dsh-takeover` | C1 会话接力 | **典型** | unpublished | 文件总线 + `open(claim,'wx')` 恰好一次；替换的是会话不是进程 |
| 08 | `Chinesezjc/dsh-interconnect` | C2a 直连实例消息 | **典型** | active | 每对端一条持久 WS；无幂等、无离线队列，正好标出边界 |
| 13 | `Noelune/dsh-agent-relay` | C2b broker | **典型** | unpublished | 与 08 的直连 WS 不是同一机制：HTTP broker + 租约投递 + 幂等键 + wake；0.6–0.8 未发布，0.5.0 没有这些机制 |
| 06 | `zbzbhs/dsh-remote-agent` | C3 远端执行 | **典型** | active | 副机跑完整 loop；凭证不过协议但 hub 可 exec，信任边界代表 |
| 14 | `PerryLink/dsh-team-rooms` | C4 跨会话持久化 | **典型** | retired | 房间存储为权威 + 单写链；仓库 archived，且 rc.3 禁写 `team-room/fact` |
| 07 | `Nwflower/dsh-file-claim` | X1 写冲突拦截 | **典型** | active | 唯一在写路径上返回 deny 的样本；无 epoch 是它的已知洞 |
| 18 | `GM-HZ/agent-dag-workflow` | P3 声明式 DAG | **典型** | active | 唯一把「模板 + 断点 + 三档重放 + 宿主限额」做全的样本；npm/tag/commit/CI 四层对齐 |

**结论**：14 族 / 14 典型 / 4 变体；8 张有明确兼容问题（04/05/10/11/12/13/14/17）。**08 直连与 13 broker 拆族**（C2a/C2b）——机制不同，不是近重复。

## 2. B4 要执行的降级动作

1. 4 张变体卡（02/05/12/15）在卡首加「定位（变体）」差异段；正文深度保留，机制细节仍以 memo 为准。
2. 17 张卡页头补 `tier` / `life` / `evidence` / `answers` 四个字段。
3. `encyclopedia` 主表分两段：14 典型在前，4 变体在后；计数不手写。
4. `00-map` §3 的样本坐标改为按族列，不再按编号列。
5. 任一降级都要在 `catalog` 保留行（去重不删档）。

## 3. 十问缺口的候选方向

不点名未核实的仓库；按判据去搜、去分诊。

| 缺口 | 要找什么 | 判据（过了才立卡） | 上限 |
|---|---|---|---|
| ~~Q4 声明式 DAG / 重放~~ | 已立卡：样本 18 | 模板在 spec 里、恢复与重放分开、额度可核 | 已完成 |
| Q6 fencing / 租约 | 写路径上带 epoch 或 CAS 的协调插件 | 能指出拒绝发生在哪一行；有失锁路径 | **本轮无合格样本**（见 §2.1） |
| Q5 离线队列 | 断链后可补投的消息通道 | 队列持久化位置可指认；幂等键存在 | **本轮无合格样本**（见 §2.1） |
| Q1/Q8/Q9 | **不靠新样本**：章节 + 文献 `[LIT]` + 试验台 R 记录 | 能给出判据与默认选择 | 0 张 |

**若 Q4/Q6 都搜不到合格样本**：不硬凑，改用「宿主已有能力 + 反例」写判据，并在本表记原因。

## 2.1 B3 分诊记录（2026-11-01）

召回口径：`data/plugins/*.yml` 按 `dag / graph / 拓扑 / 依赖图 / epoch / 租约 / 幂等 / offline` 粗筛；只对通过初筛的 6 个读 README/package。

| 候选 | 命中缺口 | 判定 | 理由 |
|---|---|---|---|
| `GM-HZ/agent-dag-workflow` | Q4 | **立卡（18）** | 模板/引擎/重放/限额四段齐全；npm↔tag↔commit↔CI 对齐 |
| `hoyyang/dsh-plan-board` | Q4 | 不立卡 | 规划看板 + 人审门，没有执行引擎；答案在「规划」不在「编排」 |
| `LeemanCheung/dsh-task-dag` | Q4 | 不立卡 | 只做投影/可视化，不调度 |
| `hunmer/dsh-team-control` | Q4/团队 | 暂缓 | 有 DAG 自动派发与四域权限，但属 teams 同族；先解决「同族只留一个典型」再议 |
| `zzd1990/dsh-parallel-dev` | Q4 | 不立卡 | 是验收门/看板，不是编排模型 |
| `nicecx/dsh-task-queue` | Q6 | 不立卡 | 租约 + 并发 1 是「避免并发」，不是 fencing；无 epoch token |

**Q5/Q6 的结论**：没有「写路径上带 epoch 的 fencing」样本，也没有「断链后补投」的离线队列样本。按宪章 §0「不按名单写」，不硬凑；Q5/Q6 留「中」，等真实候选出现。

## 4. 不立卡的理由（已排除）

- **同族第二、第三个团队 runtime**（02/05/12）：机制谱不变，降为变体。
- **同机制第二张路由卡**（15）：差异只在挂载点，降为变体。
- **未发布机制的 broker**（13）：保留为变体而非典型，因为 npm 0.5.0 不含该机制；照 npm 版本抄会落空。
- **任何 ★ 高但机制与已有典型重复的候选**：读 README 即可排除，不进 L3。

## 5. 复核触发条件

| 触发 | 动作 |
|---|---|
| 上游 `dsh-experimental-agent-team` 毕业或改限制 | 重读 §6 边界表与 `reference/SEAMS.md`；受影响的典型卡改版本 |
| DSH 基线从 `0.2.1-rc.3` 升级 | `COMPAT` 全表复核；`blocked` 项逐条重判 |
| 某 `retired` 样本复活 | 生命状态改 `active`，证据等级重评 |
| B2 实测推翻某张卡的机制 | 该卡 `tier` 改 `反例`，`TRAPS` 记「曾经这么以为」 |
| 连续 3 个候选都只是变体 | 本批停止扩样本（饱和判据） |
