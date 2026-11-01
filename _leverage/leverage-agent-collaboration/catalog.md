---
title: "catalog · Agent 协作册全量清单"
domain: agent-collab
kind: index
positioning: "本册全部文件的手工索引：家族入口、样本卡、固定版本 memo 与横向章节。"
read_when: "想一次看全本册文件，或按关键词找入口。"
status: living
updated: 2026-11-01
---
# catalog · Agent 协作册

| 文件 | kind | 定位 | 什么时候读 |
|---|---|---|---|
| [`README.md`](./README.md) | index | 本册入口：四家族与迁移说明。 | 第一次进本册。 |
| [catalog.md（本文件）](./catalog.md) | index | 全部 Markdown 的 kind、定位与阅读时机（本文件手工维护）。 | 想一次看全所有文件，或按关键词找入口。 |
| [`00-map.md`](./00-map.md) | charter | 本册宪章：四道边界、三笔税、选型与样本坐标。 | 要判断一个协作方案属于哪类。 |
| [`EVIDENCE.md`](./EVIDENCE.md) | guide | 本册证据规约：样本 memo、章节证据节、分源标签。 | 新增/修订样本或章节前。 |
| [`research/RESEARCH.md`](./research/RESEARCH.md) | guide | 研究规程：漏斗、分诊、五步取证、五条硬检与饱和停止条件。 | 要新增/复核一张卡时。 |
| [`research/BACKLOG.md`](./research/BACKLOG.md) | index | 分诊结果（14 典型 + 4 变体）、兼容状态与十问缺口候选。 | 要补样本或问「为什么没有卡」时。 |
| [`reference/SEAMS.md`](./reference/SEAMS.md) | guide | 接缝选择表：六条立场、四道边界矩阵、偏离登记。 | 要在原生接缝与自建之间选时。 |
| [`reference/COMPAT.md`](./reference/COMPAT.md) | guide | 兼容性墙：18 张样本的生命状态与 rc.3 失效点。 | 引用样本前先确认它成不成立。 |
| [`practice/TRAPS.md`](./practice/TRAPS.md) | guide | 16 条协作反模式，每条带反例。 | 设计/评审前扫一遍。 |
| [`practice/CHECKLIST.md`](./practice/CHECKLIST.md) | guide | 15 项上线前自检，每项写「怎么核」。 | 上线或评审时逐项过。 |
| [`_证据/00_实测环境与账本.md`](./_证据/00_实测环境与账本.md) | evidence | R0–R7 实测账本：环境、工件、观察与一条推翻。 | 引用 01/05/07/11 的 L2 结论前。 |
| [`BORROW.md`](./BORROW.md) | guide | 按家族路由的借用入口。 | 要选型或评审协作方案。 |
| [`coordination/01-taxonomy.md`](./coordination/01-taxonomy.md) | playbook | 四道边界与三笔税的总览（迁移自旧 01）。 | 要理解协作边界与代价。 |
| [`coordination/03-state-ownership.md`](./coordination/03-state-ownership.md) | card | 权威位置与第二真相源失步。 | 设计状态归属。 |
| [`coordination/04-conflict-adjudication.md`](./coordination/04-conflict-adjudication.md) | card | 拦截点阶梯与真裁决代价。 | 设计写冲突方案。 |
| [`coordination/05-failure-and-selection.md`](./coordination/05-failure-and-selection.md) | card | 三类失败 + 选型矩阵 + 七问。 | 选型与评审。 |
| [`coordination/06-when-not-multi-agent.md`](./coordination/06-when-not-multi-agent.md) | playbook | 何时不该多 agent：三条买点、五步判定、反方证据。 | 决策前先读。 |
| [`coordination/07-cost-and-observability.md`](./coordination/07-cost-and-observability.md) | playbook | 三层额度、七个指标、宿主可观测面与验收五问。 | 估成本或验收时。 |
| [`coordination/02-mechanisms.md`](./coordination/02-mechanisms.md) | playbook | 九家样本的机制谱与三张配方（迁移自旧 02）。 | 要比较状态/冲突/收敛的具体做法。 |
| [`encyclopedia.md`](./encyclopedia.md) | index | 18 个样本的同表对照。 | 要横向比较多个协作样本。 |
| [`delegation/01-host-contract.md`](./delegation/01-host-contract.md) | playbook | dsh-subagent 深度/容量/权限/结果契约。 | 设计主-子委派。 |
| [`delegation/samples/15-Garybot126-dsh-subagent-models.md`](./delegation/samples/15-Garybot126-dsh-subagent-models.md) | sample | 子代理模型统一设置样本。 | 要统一子代理模型。 |
| [`delegation/_证据/15-subagent-models-源码复核.md`](./delegation/_证据/15-subagent-models-源码复核.md) | evidence | 0.1.2/a105855；agent/request 覆写与 README 偏差。 | 引用 15 前核对。 |
| [`delegation/samples/16-tkaiz0406-dsh-subagent-route-pin.md`](./delegation/samples/16-tkaiz0406-dsh-subagent-route-pin.md) | sample | provider 包装 + startActivation 钩子钉 child 路由。 | 需要创建前选路由。 |
| [`delegation/_证据/16-route-pin-源码复核.md`](./delegation/_证据/16-route-pin-源码复核.md) | evidence | 固定 commit；provider 包装与 startActivation 分流。 | 引用 16 前核对。 |
| [`delegation/samples/17-aleskxyz-dsh-subagent-fork-lite.md`](./delegation/samples/17-aleskxyz-dsh-subagent-fork-lite.md) | sample | 截断 fork 的 seed 窗口。 | 控制 fork 继承上下文。 |
| [`delegation/_证据/17-fork-lite-源码复核.md`](./delegation/_证据/17-fork-lite-源码复核.md) | evidence | 0.1.1；截断 fork 与 0.2.x 不兼容。 | 引用 17 前核对。 |
| [`delegation/README.md`](./delegation/README.md) | index | delegation 家族入口与样本索引。 | 要做 delegation 相关设计。 |
| [`teams/01-roster-and-captain.md`](./teams/01-roster-and-captain.md) | card | roster 权威位置、成员模型与队长角色。 | 设计团队成员模型。 |
| [`teams/02-scheduling.md`](./teams/02-scheduling.md) | card | idle 边沿、原子认领与容量/深度。 | 设计唤醒与任务认领。 |
| [`teams/03-mailbox-and-ack.md`](./teams/03-mailbox-and-ack.md) | card | 投递/准入/已读三态与幂等键。 | 设计成员消息。 |
| [`teams/05-failure-modes.md`](./teams/05-failure-modes.md) | card | 假成功/覆盖写/孤儿/停驻/假恢复五类失效。 | 设计失败语义与恢复。 |
| [`teams/04-taskboard-and-gates.md`](./teams/04-taskboard-and-gates.md) | card | 任务板权威、完成判据与质量门位置。 | 设计任务板/质量门。 |
| [`teams/README.md`](./teams/README.md) | index | teams 家族入口与样本索引。 | 要做 teams 相关设计。 |
| [`pipelines/README.md`](./pipelines/README.md) | index | pipelines 家族入口与样本索引。 | 要做 pipelines 相关设计。 |
| [`crossing/01-session-handoff.md`](./crossing/01-session-handoff.md) | card | 接管的替换对象与失败语义。 | 设计跨会话接力。 |
| [`crossing/02-broker-and-relay.md`](./crossing/02-broker-and-relay.md) | card | 直连 WS vs broker 的鉴权/幂等/离线。 | 设计跨实例消息。 |
| [`crossing/03-remote-worker-trust.md`](./crossing/03-remote-worker-trust.md) | card | 远端 loop、hub 能力与凭证边界。 | 设计跨机执行。 |
| [`crossing/05-rooms-and-persistence.md`](./crossing/05-rooms-and-persistence.md) | card | 房间权威、fact 禁写与游标。 | 设计跨会话持久化。 |
| [`pipelines/01-graph-vs-code.md`](./pipelines/01-graph-vs-code.md) | card | DAG vs 代码控制流。 | 选择编排模型。 |
| [`pipelines/02-native-workflow-engine.md`](./pipelines/02-native-workflow-engine.md) | card | 宿主 workflow 是脚本编排而非 DAG。 | 判断是否自建 DAG。 |
| [`crossing/04-acp-remote-execution.md`](./crossing/04-acp-remote-execution.md) | card | ACP/外部运行时的一次性边界。 | 接外部 agent。 |
| [`delegation/02-fork-and-resume.md`](./delegation/02-fork-and-resume.md) | card | fork/外部一次性/冷恢复的差别。 | 选择创建语义。 |
| [`pipelines/04-worktree-lanes.md`](./pipelines/04-worktree-lanes.md) | card | worktree lane 的隔离与代价。 | 设计文件隔离。 |
| [`crossing/README.md`](./crossing/README.md) | index | crossing 家族入口与样本索引。 | 要做 crossing 相关设计。 |
| [`coordination/README.md`](./coordination/README.md) | index | coordination 家族入口与样本索引。 | 要做 coordination 相关设计。 |
| [`coordination/samples/07-Nwflower-dsh-file-claim.md`](./coordination/samples/07-Nwflower-dsh-file-claim.md) | sample | 边车认领 + pre-execute deny；唯一真拦写的典型。 | 要读该样本机制与代价。 |
| [`crossing/samples/06-zbzbhs-dsh-remote-agent.md`](./crossing/samples/06-zbzbhs-dsh-remote-agent.md) | sample | hub/worker 双角色；跨机最终是信任边界。 | 要读该样本机制与代价。 |
| [`crossing/samples/08-Chinesezjc-dsh-interconnect.md`](./crossing/samples/08-Chinesezjc-dsh-interconnect.md) | sample | 每对端一条持久 WS；跨实例投递，无幂等/离线队列。 | 要读该样本机制与代价。 |
| [`crossing/samples/09-IKEASven69-dsh-takeover.md`](./crossing/samples/09-IKEASven69-dsh-takeover.md) | sample | 文件总线 + open(claim,'wx') 恰好一次；替换的是会话。 | 要读该样本机制与代价。 |
| [`crossing/samples/13-Noelune-dsh-agent-relay.md`](./crossing/samples/13-Noelune-dsh-agent-relay.md) | sample | HTTP broker + 租约/幂等/wake；机制未发布到 npm。 | 要读该样本机制与代价。 |
| [`crossing/samples/14-PerryLink-dsh-team-rooms.md`](./crossing/samples/14-PerryLink-dsh-team-rooms.md) | sample | 房间存储权威 + 单写链；已归档，rc.3 投影退化。 | 要读该样本机制与代价。 |
| [`pipelines/samples/03-omdsh-dev-dsh_workflow.md`](./pipelines/samples/03-omdsh-dev-dsh_workflow.md) | sample | 内容键缓存 + 胶囊快照：卖可复现，不卖断点。 | 要读该样本机制与代价。 |
| [`pipelines/samples/11-february2015-dsh-taskswarm.md`](./pipelines/samples/11-february2015-dsh-taskswarm.md) | sample | 每 lane 一个 worktree；npm 下架，只作源码参考。 | 要读该样本机制与代价。 |
| [`pipelines/samples/18-GM-HZ-agent-dag-workflow.md`](./pipelines/samples/18-GM-HZ-agent-dag-workflow.md) | sample | 声明式 DAG + 断点恢复 + 三档重放。 | 要暂停/恢复或事后重放。 |
| [`teams/samples/01-NanmiCoder-dsh-agent-teams.md`](./teams/samples/01-NanmiCoder-dsh-agent-teams.md) | sample | 磁盘 team.json + idle 边沿调度；可续成员的团队典型。 | 要读该样本机制与代价。 |
| [`teams/samples/02-toolclub-dsh-agent-team-gui.md`](./teams/samples/02-toolclub-dsh-agent-team-gui.md) | sample | 变体：产品化 runtime + pre-step 派工（相对 01）。 | 要读该样本机制与代价。 |
| [`teams/samples/04-limuyang2-agent-team.md`](./teams/samples/04-limuyang2-agent-team.md) | sample | 成员＝独立根 Agent；异构团队的另一条路。 | 要读该样本机制与代价。 |
| [`teams/samples/05-Mlte0907-dsh-teams-x.md`](./teams/samples/05-Mlte0907-dsh-teams-x.md) | sample | 变体：质量门自动返工；跨进程锁只在未发布源码（相对 01）。 | 要读该样本机制与代价。 |
| [`teams/samples/10-Asher-2000-dsh-expert-mode.md`](./teams/samples/10-Asher-2000-dsh-expert-mode.md) | sample | 不写插件的 preset 路线；rc.3 装不起来。 | 要读该样本机制与代价。 |
| [`teams/samples/12-2507483326-dsh-eteams.md`](./teams/samples/12-2507483326-dsh-eteams.md) | sample | 变体：SQLite + persona 请求参数（仅 0.1.x）。 | 要读该样本机制与代价。 |
| [`coordination/_证据/07-file-claim-源码复核.md`](./coordination/_证据/07-file-claim-源码复核.md) | evidence | main@42f07e2（0.2.0）；deny 覆盖与无 epoch。 | 引用 07 前核对。 |
| [`crossing/_证据/06-remote-agent-源码复核.md`](./crossing/_证据/06-remote-agent-源码复核.md) | evidence | 固定 commit 的 hub/worker 与信任边界。 | 引用 06 前核对。 |
| [`crossing/_证据/08-interconnect-源码复核.md`](./crossing/_证据/08-interconnect-源码复核.md) | evidence | 0.13.0↔v0.13.0↔5547b03；投递/鉴权。 | 引用 08 前核对。 |
| [`crossing/_证据/09-takeover-源码复核.md`](./crossing/_证据/09-takeover-源码复核.md) | evidence | main@afbc55c（0.4.3）；替换对象与入站路由。 | 引用 09 前核对。 |
| [`crossing/_证据/13-agent-relay-源码复核.md`](./crossing/_证据/13-agent-relay-源码复核.md) | evidence | v0.8.1=7e43c54；npm 0.5.0 缺失机制。 | 引用 13 前核对。 |
| [`crossing/_证据/14-team-rooms-源码复核.md`](./crossing/_证据/14-team-rooms-源码复核.md) | evidence | v1.0.8=c1c485e；fact 事件与游标。 | 引用 14 前核对。 |
| [`pipelines/_证据/03-dsh_workflow-源码复核.md`](./pipelines/_证据/03-dsh_workflow-源码复核.md) | evidence | main@44b83c1（0.1.2）；胶囊/缓存与偏差。 | 引用 03 前核对。 |
| [`pipelines/_证据/11-taskswarm-源码复核.md`](./pipelines/_证据/11-taskswarm-源码复核.md) | evidence | v0.2.38↔3164995；清理/resume/KI 偏差。 | 引用 11 前核对。 |
| [`pipelines/_证据/18-agent-dag-workflow-源码复核.md`](./pipelines/_证据/18-agent-dag-workflow-源码复核.md) | evidence | 18 的固定版本复核：模板/引擎/重放/限额行号。 | 引用 18 前核对。 |
| [`teams/_证据/01-agent-teams-源码复核.md`](./teams/_证据/01-agent-teams-源码复核.md) | evidence | 固定版本 0.1.28↔tag↔commit；锁与签名偏差。 | 引用 01 前核对。 |
| [`teams/_证据/02-team-gui-源码复核.md`](./teams/_证据/02-team-gui-源码复核.md) | evidence | release v1.3.0↔14ea119；默认值与 CI。 | 引用 02 前核对。 |
| [`teams/_证据/04-agent-team-源码复核.md`](./teams/_证据/04-agent-team-源码复核.md) | evidence | 0.1.4/a7f3046；独立根 Agent 与 peer 缺口。 | 引用 04 前核对。 |
| [`teams/_证据/05-teams-x-源码复核.md`](./teams/_证据/05-teams-x-源码复核.md) | evidence | 0.11.5 源码 vs npm 0.2.0；锁与 CI 缺口。 | 引用 05 前核对。 |
| [`teams/_证据/10-expert-mode-源码复核.md`](./teams/_证据/10-expert-mode-源码复核.md) | evidence | HEAD ed9a19d；17 行工具别名与 rc.3 五处硬伤。 | 引用 10 前核对。 |
| [`teams/_证据/12-eteams-源码复核.md`](./teams/_证据/12-eteams-源码复核.md) | evidence | 0.2.21/0f8aa30；persona 仅 0.1.x。 | 引用 12 前核对。 |

> 章节扩写后继续补行；本表由 `verify.mjs` 与目录 Markdown 集合双向核对。
