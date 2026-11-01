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
| [`00-map.md`](./00-map.md) | charter | 本册宪章：四道边界、三笔税、选型与样本坐标（迁移中）。 | 要判断一个协作方案属于哪类。 |
| [`EVIDENCE.md`](./EVIDENCE.md) | guide | 本册证据规约：样本 memo、章节证据节、分源标签。 | 新增/修订样本或章节前。 |
| [`BORROW.md`](./BORROW.md) | guide | 按家族路由的借用入口。 | 要选型或评审协作方案。 |
| [`coordination/01-taxonomy.md`](./coordination/01-taxonomy.md) | playbook | 四道边界与三笔税的总览（迁移自旧 01）。 | 要理解协作边界与代价。 |
| [`coordination/03-state-ownership.md`](./coordination/03-state-ownership.md) | card | 权威位置与第二真相源失步。 | 设计状态归属。 |
| [`coordination/04-conflict-adjudication.md`](./coordination/04-conflict-adjudication.md) | card | 拦截点阶梯与真裁决代价。 | 设计写冲突方案。 |
| [`coordination/05-failure-and-selection.md`](./coordination/05-failure-and-selection.md) | card | 三类失败 + 选型矩阵 + 七问。 | 选型与评审。 |
| [`coordination/02-mechanisms.md`](./coordination/02-mechanisms.md) | playbook | 九家样本的机制谱与三张配方（迁移自旧 02）。 | 要比较状态/冲突/收敛的具体做法。 |
| [`encyclopedia.md`](./encyclopedia.md) | index | 14 个样本的同表对照。 | 要横向比较多个协作样本。 |
| [`delegation/01-host-contract.md`](./delegation/01-host-contract.md) | playbook | dsh-subagent 深度/容量/权限/结果契约。 | 设计主-子委派。 |
| [`delegation/samples/15-Garybot126-dsh-subagent-models.md`](./delegation/samples/15-Garybot126-dsh-subagent-models.md) | sample | 子代理模型统一设置样本。 | 要统一子代理模型。 |
| [`delegation/_证据/15-subagent-models-源码复核.md`](./delegation/_证据/15-subagent-models-源码复核.md) | evidence | 15 的固定版本复核。 | 引用 15 前核对。 |
| [`delegation/samples/16-tkaiz0406-dsh-subagent-route-pin.md`](./delegation/samples/16-tkaiz0406-dsh-subagent-route-pin.md) | sample | provider 包装 + startActivation 钩子钉 child 路由。 | 需要创建前选路由。 |
| [`delegation/_证据/16-route-pin-源码复核.md`](./delegation/_证据/16-route-pin-源码复核.md) | evidence | 16 的固定版本复核。 | 引用 16 前核对。 |
| [`delegation/samples/17-aleskxyz-dsh-subagent-fork-lite.md`](./delegation/samples/17-aleskxyz-dsh-subagent-fork-lite.md) | sample | 截断 fork 的 seed 窗口。 | 控制 fork 继承上下文。 |
| [`delegation/_证据/17-fork-lite-源码复核.md`](./delegation/_证据/17-fork-lite-源码复核.md) | evidence | 17 的固定版本复核。 | 引用 17 前核对。 |
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
| [`coordination/samples/07-Nwflower-dsh-file-claim.md`](./coordination/samples/07-Nwflower-dsh-file-claim.md) | sample | 07-Nwflower-dsh-file-claim.md 样本卡。 | 要读该样本机制与代价。 |
| [`crossing/samples/06-zbzbhs-dsh-remote-agent.md`](./crossing/samples/06-zbzbhs-dsh-remote-agent.md) | sample | 06-zbzbhs-dsh-remote-agent.md 样本卡。 | 要读该样本机制与代价。 |
| [`crossing/samples/08-Chinesezjc-dsh-interconnect.md`](./crossing/samples/08-Chinesezjc-dsh-interconnect.md) | sample | 08-Chinesezjc-dsh-interconnect.md 样本卡。 | 要读该样本机制与代价。 |
| [`crossing/samples/09-IKEASven69-dsh-takeover.md`](./crossing/samples/09-IKEASven69-dsh-takeover.md) | sample | 09-IKEASven69-dsh-takeover.md 样本卡。 | 要读该样本机制与代价。 |
| [`crossing/samples/13-Noelune-dsh-agent-relay.md`](./crossing/samples/13-Noelune-dsh-agent-relay.md) | sample | 13-Noelune-dsh-agent-relay.md 样本卡。 | 要读该样本机制与代价。 |
| [`crossing/samples/14-PerryLink-dsh-team-rooms.md`](./crossing/samples/14-PerryLink-dsh-team-rooms.md) | sample | 14-PerryLink-dsh-team-rooms.md 样本卡。 | 要读该样本机制与代价。 |
| [`pipelines/samples/03-omdsh-dev-dsh_workflow.md`](./pipelines/samples/03-omdsh-dev-dsh_workflow.md) | sample | 03-omdsh-dev-dsh_workflow.md 样本卡。 | 要读该样本机制与代价。 |
| [`pipelines/samples/11-february2015-dsh-taskswarm.md`](./pipelines/samples/11-february2015-dsh-taskswarm.md) | sample | 11-february2015-dsh-taskswarm.md 样本卡。 | 要读该样本机制与代价。 |
| [`teams/samples/01-NanmiCoder-dsh-agent-teams.md`](./teams/samples/01-NanmiCoder-dsh-agent-teams.md) | sample | 01-NanmiCoder-dsh-agent-teams.md 样本卡。 | 要读该样本机制与代价。 |
| [`teams/samples/02-toolclub-dsh-agent-team-gui.md`](./teams/samples/02-toolclub-dsh-agent-team-gui.md) | sample | 02-toolclub-dsh-agent-team-gui.md 样本卡。 | 要读该样本机制与代价。 |
| [`teams/samples/04-limuyang2-agent-team.md`](./teams/samples/04-limuyang2-agent-team.md) | sample | 04-limuyang2-agent-team.md 样本卡。 | 要读该样本机制与代价。 |
| [`teams/samples/05-Mlte0907-dsh-teams-x.md`](./teams/samples/05-Mlte0907-dsh-teams-x.md) | sample | 05-Mlte0907-dsh-teams-x.md 样本卡。 | 要读该样本机制与代价。 |
| [`teams/samples/10-Asher-2000-dsh-expert-mode.md`](./teams/samples/10-Asher-2000-dsh-expert-mode.md) | sample | 10-Asher-2000-dsh-expert-mode.md 样本卡。 | 要读该样本机制与代价。 |
| [`teams/samples/12-2507483326-dsh-eteams.md`](./teams/samples/12-2507483326-dsh-eteams.md) | sample | 12-2507483326-dsh-eteams.md 样本卡。 | 要读该样本机制与代价。 |
| [`coordination/_证据/07-file-claim-源码复核.md`](./coordination/_证据/07-file-claim-源码复核.md) | evidence | 07-file-claim-源码复核.md 固定版本复核。 | 引用样本断言前核对来源。 |
| [`crossing/_证据/06-remote-agent-源码复核.md`](./crossing/_证据/06-remote-agent-源码复核.md) | evidence | 06-remote-agent-源码复核.md 固定版本复核。 | 引用样本断言前核对来源。 |
| [`crossing/_证据/08-interconnect-源码复核.md`](./crossing/_证据/08-interconnect-源码复核.md) | evidence | 08-interconnect-源码复核.md 固定版本复核。 | 引用样本断言前核对来源。 |
| [`crossing/_证据/09-takeover-源码复核.md`](./crossing/_证据/09-takeover-源码复核.md) | evidence | 09-takeover-源码复核.md 固定版本复核。 | 引用样本断言前核对来源。 |
| [`crossing/_证据/13-agent-relay-源码复核.md`](./crossing/_证据/13-agent-relay-源码复核.md) | evidence | 13-agent-relay-源码复核.md 固定版本复核。 | 引用样本断言前核对来源。 |
| [`crossing/_证据/14-team-rooms-源码复核.md`](./crossing/_证据/14-team-rooms-源码复核.md) | evidence | 14-team-rooms-源码复核.md 固定版本复核。 | 引用样本断言前核对来源。 |
| [`pipelines/_证据/03-dsh_workflow-源码复核.md`](./pipelines/_证据/03-dsh_workflow-源码复核.md) | evidence | 03-dsh_workflow-源码复核.md 固定版本复核。 | 引用样本断言前核对来源。 |
| [`pipelines/_证据/11-taskswarm-源码复核.md`](./pipelines/_证据/11-taskswarm-源码复核.md) | evidence | 11-taskswarm-源码复核.md 固定版本复核。 | 引用样本断言前核对来源。 |
| [`teams/_证据/01-agent-teams-源码复核.md`](./teams/_证据/01-agent-teams-源码复核.md) | evidence | 01-agent-teams-源码复核.md 固定版本复核。 | 引用样本断言前核对来源。 |
| [`teams/_证据/02-team-gui-源码复核.md`](./teams/_证据/02-team-gui-源码复核.md) | evidence | 02-team-gui-源码复核.md 固定版本复核。 | 引用样本断言前核对来源。 |
| [`teams/_证据/04-agent-team-源码复核.md`](./teams/_证据/04-agent-team-源码复核.md) | evidence | 04-agent-team-源码复核.md 固定版本复核。 | 引用样本断言前核对来源。 |
| [`teams/_证据/05-teams-x-源码复核.md`](./teams/_证据/05-teams-x-源码复核.md) | evidence | 05-teams-x-源码复核.md 固定版本复核。 | 引用样本断言前核对来源。 |
| [`teams/_证据/10-expert-mode-源码复核.md`](./teams/_证据/10-expert-mode-源码复核.md) | evidence | 10-expert-mode-源码复核.md 固定版本复核。 | 引用样本断言前核对来源。 |
| [`teams/_证据/12-eteams-源码复核.md`](./teams/_证据/12-eteams-源码复核.md) | evidence | 12-eteams-源码复核.md 固定版本复核。 | 引用样本断言前核对来源。 |

> 章节扩写后继续补行；本表与 `verify.mjs` 的一致性在 Phase 5 接管。
