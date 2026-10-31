# 11 · `february2015/dsh-taskswarm`

> **一句话**:**每 lane 一个 git worktree**(不是每成员一个),按依赖分波并行,失败时**刻意什么都不清理**。
> **边界**:2 同工作区多成员(靠 worktree 而不是靠裁决) · **定位**:**worktree 流派**代表:本域 worktree 隔离最完整的样本 · **证据级别**:`observed`(源码逐文件读过)
> **影响力**(2026-10-31 实时采样):**3★** / npm **0 次/月**(近 30 天零下载);catalog 快照 1★ → ×3
> **什么时候找它**:想知道 worktree 到底怎么用、或者想要一份真实的故障档案

> 导航:[样本索引](../03-sample-encyclopedia.md) · [域章程](../README.md) · [三笔税机制谱](../02-coordination-mechanisms.md) · [四道边界](../01-collab-topology.md)

## 设计思路

**`february2015/dsh-taskswarm` 回答的是「worktree 到底怎么用」:每 lane 一个,不是每成员一个**。路径 `<stateRoot>/worktrees/<taskId>/` 加一个常驻的 `_orch` 集成 worktree;新 lane 以 `taskswarm/orch` HEAD 为基线,`mergeLane()` 在 `_orch` 里 `git merge`,**失败时刻意什么都不清理**(不移 worktree、不删分支、保留冲突标记)。它的 `docs/known-issues.md` 是本域最好的一份故障档案,其中三条正好命中本卡的主题:KI-003「内存态整份落盘覆盖兄弟 lane」是典型的第二真相源失步;KI-007「`await spawn()` 无超时让整批卡死」是缺看门狗;而**代码里仍可见的缺陷**是 `updateLane()` 依旧「读整份 JSON → 改一条 → 整份写」,并发 lane 之间**仍是 last-write-wins**——KI-003 的修复只是少了一次更糟的整份写,没引入队列或文件锁。

它的 `docs/known-issues.md` 是本域**最好的一份故障档案**:8 个已知问题里三条正好命中本域主题——KI-003「内存态整份落盘覆盖兄弟 lane」是典型的第二真相源失步;KI-007「`await spawn()` 无超时让整批卡死」是缺看门狗。

**但代码里仍可见的缺陷**:`updateLane()` 依旧是「读整份 JSON → 改一条 → 整份写」,并发 lane 之间**仍是 last-write-wins**——KI-003 的修复只是少了一次更糟的整份写,**没引入队列或文件锁**。另外 `reviewLevel` 被解析但从不消费,reviewer 可被实现者跳过;KI 文档说 90 分钟超时,代码写的是 180。

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`february2015/dsh-taskswarm`](https://github.com/february2015/dsh-taskswarm) |
| **npm 包名** | `dsh-taskswarm` |
| **版本(本次读)** | `0.2.38` |
| **License** | MIT |
| **npm 近 30 天** | **0 次**——有 3★ 但近一个月零下载 |
| **安装** | `dsh plugin add dsh-taskswarm`,或 `dsh plugin add https://github.com/february2015/dsh-taskswarm.git` |
| **附带 CLI** | `taskswarm-dashboard`(bin 字段)——dashboard 是**纯读 SSE** 的 |
| **接线方式** | `main: lib/orchestrator/index.js`(`lib/orchestrator/` 说明重心在编排器);`dsh.bundle.patch`;无 client 注入 |

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | `.taskswarm/batches/<id>.json` 为权威;dashboard 只读 | 内存态与盘上状态并存,KI-003 就是失步 |
| 冲突裁决 | **worktree 隔离**——每 lane 一个 worktree,物理上不共享 | 合并冲突推给 git,失败时不清理也不自动解决 |
| 失败收敛 | `mergeLane()` 失败**刻意什么都不清理**:不移 worktree、不删分支、保留冲突标记 | `await spawn()` 无超时(KI-007),整批可卡死 |

## 借用指南

### 可借鉴(直接抄)

1. **每 lane 一个 worktree,再加一个常驻 `_orch` 集成 worktree** —— 路径 `<stateRoot>/worktrees/<taskId>/`;新 lane 以 `taskswarm/orch` HEAD 为基线。**用 git 做隔离,就不用自己写裁决。**
2. **合并失败时什么都不清理** —— 不移 worktree、不删分支、保留冲突标记。让现场保持可诊断,比「清理干净」有用得多。
3. **`docs/known-issues.md` 写成带编号的故障档案(KI-001…)** —— 这是本域最好的一份,后来的读者能直接对着它判断「我能不能接受这些缺陷」。

### 别照抄

- 别把 `updateLane()` 那种「读整份 → 改一条 → 整份写」当并发安全 —— 它仍是 last-write-wins。
- 别指望 `reviewLevel` 生效 —— 它被解析但从不消费,reviewer 可被实现者跳过。
- 别照抄 3★ 背后的「有人用」假设:近 30 天 npm 下载 **0**。
