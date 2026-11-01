---
title: "Agent 协作册总章：四家族与横向协调"
domain: agent-collab
kind: charter
positioning: "本册宪章：主-子/团队/流水线/跨界四家族 + coordination 横向卷；两根轴、判定树、样本归属与证据门。"
read_when: "要判断一个多 agent 方案属于哪类、该读哪卷；或要新增样本/章节时。"
status: living
updated: 2026-11-01
---
# Agent 协作册 · 四家族与横向协调

> **标语**：*Who collaborates with whom, who owns the state, who converges?* —— 协作先问状态与收敛，再问怎么派活。
> **状态**：由原 `leverage/lever-cross-boundary` 迁出独立成册（2026-11-01）。14 个既有样本按主家族归位、证据 memo 一并迁移；delegation 新增 15/16 路由样本与 17 截断 fork 样本；delegation / pipelines 的空白区在后续批次补研究。
> **本册自足**：`README` / `00-map` / `EVIDENCE` / `catalog` / `BORROW` 都在本目录；不再依赖父册的域 README。

## 1. 为什么单独成册

“多 agent”不是一个功能，而是**一组建模选择**：谁拥有成员、谁拥有任务、谁拥有消息、崩了谁收敛。把它们塞进“门禁/权限”的机制册里，会同时失去两类读者：想搭团队的人找不到编队方法，想审权限的人被协作细节淹没。

所以本册只回答协作结构；质量门禁留在 [`../leverage/lever-prove-output/`](../leverage/lever-prove-output/README.md)，权限/审批留在 [`../leverage/lever-draw-limit/`](../leverage/lever-draw-limit/README.md)，产品化留在 [`../leverage-reshape-product/`](../leverage-reshape-product/README.md)。

## 2. 两根轴先于分类

| 轴 | 取值 | 它决定什么 |
|---|---|---|
| **协作单元** | 一次委派 / 可续子代理 / 独立根 Agent / 外部运行时 | 成员的寿命、上下文与权限边界 |
| **控制流** | 提示词约定 / 声明式 DAG / 代码即编排 | 谁决定下一步，失败能否重放 |
| **协调介质** | 父子消息 / 邮箱 / 任务板 / 文件总线 / broker / 同步盘 | 状态归属、冲突裁决、失败收敛 |

四家族是这两根轴上的区域，不是互斥分类；一个样本可以落在两个家族里，但**只有一个主家族**。

## 3. 四家族 + 横向卷

| 卷 | 回答什么 | 分析单位 | 目录 |
|---|---|---|---|
| **delegation 主-子代理** | 一次委派怎么发生、能不能续、结果怎么回传 | 一条宿主接缝或一个委派样本 | [`delegation/`](./delegation/README.md) |
| **teams 团队** | 多成员如何编队、调度、共享任务板 | 一个团队运行时样本 | [`teams/`](./teams/README.md) |
| **pipelines 流水线** | 控制流怎么写、重放/暂停/幂等怎么做 | 一种编排模型 + 样本 | [`pipelines/`](./pipelines/README.md) |
| **crossing 跨会话/实例/机器** | handoff、broker、远端 worker、房间 | 一种跨界通道 + 样本 | [`crossing/`](./crossing/README.md) |
| **coordination 横向** | 状态归属、冲突裁决、失败收敛、容量/成本 | 跨样本对照 + 判定树 | [`coordination/`](./coordination/README.md) |

## 4. 现有样本的主家族

| 样本 | 主家族 | 交叉角色 | 证据链 |
|---|---|---|---|
| 01 `NanmiCoder/dsh-agent-teams` | teams | pipelines（邮箱/调度） | [`memo`](./teams/_证据/01-agent-teams-源码复核.md) |
| 02 `toolclub/dsh-agent-team-gui` | teams | delegation（pre-step 派工） | [`memo`](./teams/_证据/02-team-gui-源码复核.md) |
| 03 `omdsh-dev/dsh_workflow` | pipelines | teams（成员 spawn） | [`memo`](./pipelines/_证据/03-dsh_workflow-源码复核.md) |
| 04 `limuyang2/agent-team` | teams | delegation（独立根 Agent） | [`memo`](./teams/_证据/04-agent-team-源码复核.md) |
| 05 `Mlte0907/dsh-teams-x` | teams | pipelines（质量门返工） | [`memo`](./teams/_证据/05-teams-x-源码复核.md) |
| 06 `zbzbhs/dsh-remote-agent` | crossing | delegation（远端 loop） | [`memo`](./crossing/_证据/06-remote-agent-源码复核.md) |
| 07 `Nwflower/dsh-file-claim` | coordination | teams（写冲突） | [`memo`](./coordination/_证据/07-file-claim-源码复核.md) |
| 08 `Chinesezjc/dsh-interconnect` | crossing | teams（inbox 投递） | [`memo`](./crossing/_证据/08-interconnect-源码复核.md) |
| 09 `IKEASven69/dsh-takeover` | crossing | delegation（会话接力） | [`memo`](./crossing/_证据/09-takeover-源码复核.md) |
| 10 `Asher-2000/dsh-expert-mode` | teams | delegation（preset 造成员） | [`memo`](./teams/_证据/10-expert-mode-源码复核.md) |
| 11 `february2015/dsh-taskswarm` | pipelines | coordination（worktree 隔离） | [`memo`](./pipelines/_证据/11-taskswarm-源码复核.md) |
| 12 `2507483326/dsh-eteams` | teams | delegation（continuable） | [`memo`](./teams/_证据/12-eteams-源码复核.md) |
| 13 `Noelune/dsh-agent-relay` | crossing | pipelines（投递/幂等） | [`memo`](./crossing/_证据/13-agent-relay-源码复核.md) |
| 14 `PerryLink/dsh-team-rooms` | crossing | coordination（持久化游标） | [`memo`](./crossing/_证据/14-team-rooms-源码复核.md) |
| 15 `Garybot126/dsh-subagent-models` | delegation | —（委派路由） | [`memo`](./delegation/_证据/15-subagent-models-源码复核.md) |
| 16 `tkaiz0406/dsh-subagent-route-pin` | delegation | teams（startActivation 缝） | [`memo`](./delegation/_证据/16-route-pin-源码复核.md) |
| 17 `aleskxyz/dsh-subagent-fork-lite` | delegation | —（截断 fork） | [`memo`](./delegation/_证据/17-fork-lite-源码复核.md) |

## 5. 判定树

1. **你是“一个 agent 叫另一个 agent 干一件事”吗？** → delegation。先回答：成员可续吗？结果通过调用帧、通知还是邮箱回来？
2. **你是“多个成员长期共处、共享任务板”吗？** → teams。先回答：roster 谁写、调度靠什么触发、ack 发生在哪一步。
3. **你是“固定步骤/可重放流水线”吗？** → pipelines。先回答：控制流是图还是代码、缓存键是什么、暂停后从哪继续。
4. **你只是“让另一台机器/另一个会话接上”吗？** → crossing。先回答：替换的是会话还是进程、传输是否加密、断链后消息丢不丢。
5. **上面四个都能套，但争议在状态/冲突/收敛** → coordination 横向卷，用三笔税做对照。

## 6. 四道边界（底层坐标，保留）

| 边界 | 新增的问题 | 原生支撑 |
|---|---|---|
| 0 同 agent | 无——上下文、工具、权限全共享 | — |
| 1 同进程父子 | 上下文怎么切、深度/容量、结果怎么回 | `dsh-subagent`（spawn/fork 可续；ACP/SDK 等外部执行一次性） |
| 2 同工作区多成员 | 文件冲突、任务归属、消息投递 | `dsh-experimental-agent-team`（CAS 任务板、inbox） |
| 3 跨进程/跨机 | 身份、传输、信任、部分失败 | `dsh-api-gateway` / `dsh-acp` / worktree / SSH |

**旧册结论仍然成立**：生态样本大多停在边界 1+2；边界 2 的三个致命约束（共享 checkout、单进程、owner 不自动释放）是官方实验包自己写进限制里的。**插件不是在填空白，是在和限制赛跑。**

## 7. 证据门

- 样本卡：固定 repo/npm/版本/tag/commit，卡头“证据链”链接同家族 `_证据/NN-*-源码复核.md`；memo 必须有 Provenance、DOC、SRC-TARGET、TEST/CI/RUN、与卡片的偏差表。
- 章节：kind 为 `card`/`playbook` 的，必须有 `## 证据与边界`（≥3 行）；宿主断言给包名+文件+行号，样本主张标 `[DOC]`/`[OBS]`，未验证标 `[OPEN]`。
- 细节见 [`EVIDENCE.md`](./EVIDENCE.md)；样本总表见 [`encyclopedia.md`](./encyclopedia.md)。

## 8. 文件与编号

- 根：`README` / `00-map` / `EVIDENCE` / `catalog` / `BORROW` / `encyclopedia`。
- 家族：`<family>/README.md` + `NN-*.md` 章节 + `samples/NN-*.md` + `_证据/NN-*-源码复核.md`。
- 编号：家族内递增、不复用；样本编号保留迁移前的 01–14，新样本从 15 起。
- 生长：新样本先过证据门，再进主家族；跨家族角色写进本文件 §4 与样本卡 `also_in`。

## 9. 空白区（后续批次）

- delegation：宿主契约 + fork/冷恢复 + 15/16 路由 + 17 截断 fork。
- pipelines：声明式 DAG、`dsh-tool-workflow`/worker-thread、重放与幂等；
- crossing：ACP/SDK 远端执行、跨实例订阅；
- coordination：容量/成本、审批预算与协作的交叉（与 draw-limit 分工）。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 本册由原 cross-boundary 域迁出，14 样本与 memo 一一保留 | `[DOC]` | 本仓库迁移提交与 `catalog` | 目录结构，不是机制断言 |
| 四家族覆盖委派/团队/流水线/跨界，coordination 为横向 | `[OBS]` | 本册分类法 | 分类是观察框架，可争论 |
| 样本主家族按“它主要解决哪类协作”分配 | `[OBS]` | §4 表 + 各卡设计思路 | 边界样本可改主家族，需同步 §4 |
| 生态样本多停在边界 1+2 | `[OBS]` | 14 样本横向归纳 | 归纳性判断，不是抽样实验 |
