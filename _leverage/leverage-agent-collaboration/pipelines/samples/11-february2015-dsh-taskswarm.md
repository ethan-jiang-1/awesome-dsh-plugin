---
title: "february2015/dsh-taskswarm"
domain: agent-pipelines
kind: sample
positioning: "`february2015/dsh-taskswarm`：每 lane 一个 git worktree，按依赖分波并行；npm 已全量下架（安装串 404），合并失败保留、abort/卸载会清 lane。"
takeaway: "每 lane 一个 worktree；合并不清理但 abort/卸载/同 task 重跑会清；npm 已下架，只能源码装。"
read_when: "想知道 worktree 到底怎么用，或要一份真实的故障档案。"
status: observed
updated: 2026-10-31
also_in: "coordination"
---
# 11 · `february2015/dsh-taskswarm`

> **一句话**:**每 lane 一个 git worktree**(不是每成员一个),按依赖分波并行,合并失败时**刻意不清理**（但 abort/插件卸载/同 task 重跑会移除 lane worktree）。
> **边界**:2 同工作区多成员(靠 worktree 而不是靠裁决) · **定位**:**worktree 流派**代表:本域 worktree 隔离最完整的样本 · **证据级别**:`observed`(源码逐文件读过)
> **影响力**(2026-10-31 实时采样):**3★** / npm **0 次/月**(近 30 天零下载);catalog 快照 1★ → ×3
> **什么时候找它**:想知道 worktree 到底怎么用、或者想要一份真实的故障档案

> 导航:[样本索引](../../encyclopedia.md) · [域章程](../../00-map.md) · [三笔税机制谱](../../coordination/02-mechanisms.md) · [四道边界](../../coordination/01-taxonomy.md)
> **证据链**：tag `v0.2.38`=`3164995`（源码 tip `032e2c9`，src 相同）；npm 已全量下架、安装串 404，清理/resume/KI 偏差见[`11 源码复核`](../_证据/11-taskswarm-源码复核.md)。

## 设计思路

**`february2015/dsh-taskswarm` 回答的是「worktree 到底怎么用」:每 lane 一个,不是每成员一个**。路径 `<stateRoot>/worktrees/<taskId>/` 加一个常驻的 `_orch` 集成 worktree;新 lane 以 `taskswarm/orch` HEAD 为基线,`mergeLane()` 在 `_orch` 里 `git merge`,**失败时刻意什么都不清理**(不移 worktree、不删分支、保留冲突标记)。它的 `docs/known-issues.md` 是本域最好的一份故障档案,其中三条正好命中本卡的主题:KI-003「内存态整份落盘覆盖兄弟 lane」是典型的第二真相源失步;KI-007「`await spawn()` 无超时让整批卡死」是缺看门狗;而**代码里仍可见的缺陷**是 `updateLane()` 依旧「读整份 JSON → 改一条 → 整份写」,并发 lane 之间**仍是 last-write-wins**——KI-003 的修复只是少了一次更糟的整份写,没引入队列或文件锁。

它的故障档案是双语的：英文 `docs/known-issues.md` 有 7 条，KI-007 只在中文 `known-issues.zh-CN.md`（8 条）里。三条命中本域主题——KI-003「内存态整份落盘覆盖兄弟 lane」是第二真相源失步；KI-007「`await spawn()` 无超时让整批卡死」是缺看门狗。

**但代码里仍可见的缺陷**：`updateLane()` 是同步 RMW，同一进程内 lane 不会交错；真正的残余风险是波边界/stopLane/switchLaneModel 的整份写、无跨进程锁、批次 JSON 写入非原子。KI-003 的根因（陈旧整份写）已移除，但并发模型没升级。另外 `reviewLevel` 被解析但从不消费,reviewer 可被实现者跳过;KI 文档说 90 分钟超时,代码写的是 180。

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`february2015/dsh-taskswarm`](https://github.com/february2015/dsh-taskswarm) |
| **npm 包名** | `dsh-taskswarm`（**已全量下架，registry 404**；临时包 `dsh-taskswarm2@0.2.38` 的 patch 名不匹配） |
| **版本(本次读)** | `0.2.38` |
| **License** | MIT |
| **npm 近 30 天** | **0 次**——包已下架，0 是结构性结果，不是采用率信号 |
| **安装** | `dsh plugin add dsh-taskswarm` = 404；只能 `git clone` + 构建（`lib/` 不在仓库、`prepare` 生成）或 GitHub 安装 |
| **附带 CLI** | `taskswarm-dashboard`(bin 字段)——只读流为主，但会写 `<stateRoot>/dashboard-preferences.json` |
| **接线方式** | `main: lib/orchestrator/index.js`(`lib/orchestrator/` 说明重心在编排器);`dsh.bundle.patch`;无 client 注入 |

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | `.taskswarm/batches/<id>.json` 为权威;dashboard 只读 | 内存态与盘上状态并存,KI-003 就是失步 |
| 冲突裁决 | **worktree 隔离**——每 lane 一个 worktree，但共享 `.git`、`tasks/` 与 `_orch` | 合并冲突推给 git；合并失败保留，abort/卸载/重跑会清 lane（只剩分支） |
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
