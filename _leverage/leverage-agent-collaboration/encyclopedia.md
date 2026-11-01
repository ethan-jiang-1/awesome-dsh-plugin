---
title: "样本百科：17 个协作样本的主家族与交叉角色"
domain: agent-collab
kind: index
positioning: "17 个协作样本的同表对照：主家族、交叉角色、一句话机制与证据链；不复述卡片细节。"
read_when: "要横向比较多个协作样本，或给一个新样本找主家族/参照系。"
status: observed
updated: 2026-11-01
---
# 样本百科：17 个协作样本

> **用法**：先按主家族缩小范围，再看「交叉角色」判断它能否借用别卷的机制；机制细节与代价在样本卡，证据在 memo。
> **影响力**只作为采样事实，不参与主家族判定；最新数字以各卡页头（带日期）为准。

## 1. 主表

| # | 样本 | 主家族 | 交叉角色 | 一句话机制 | 证据链 |
|---|---|---|---|---|---|
| 01 | [`NanmiCoder/dsh-agent-teams`](./teams/samples/01-NanmiCoder-dsh-agent-teams.md) | teams | pipelines（邮箱/调度） | 可续子代理 + 磁盘 team.json 真相源 + idle 边沿调度 | [`memo`](./teams/_证据/01-agent-teams-源码复核.md) |
| 02 | [`toolclub/dsh-agent-team-gui`](./teams/samples/02-toolclub-dsh-agent-team-gui.md) | teams | delegation（pre-step 派工） | 它自己就是 runtime（8 表/2 工具/pre-step）；on-demand 非默认 | [`memo`](./teams/_证据/02-team-gui-源码复核.md) |
| 03 | [`omdsh-dev/dsh_workflow`](./pipelines/samples/03-omdsh-dev-dsh_workflow.md) | pipelines | teams（成员 spawn） | 代码即编排 + 胶囊快照 + 内容键缓存重放 | [`memo`](./pipelines/_证据/03-dsh_workflow-源码复核.md) |
| 04 | [`limuyang2/agent-team`](./teams/samples/04-limuyang2-agent-team.md) | teams | delegation（独立根 Agent） | 成员=独立根 Agent；入队冻结配置（权限/推理可变） | [`memo`](./teams/_证据/04-agent-team-源码复核.md) |
| 05 | [`Mlte0907/dsh-teams-x`](./teams/samples/05-Mlte0907-dsh-teams-x.md) | teams | pipelines（质量门返工） | 质量门自动派生返工；跨进程文件锁只串行写 | [`memo`](./teams/_证据/05-teams-x-源码复核.md) |
| 06 | [`zbzbhs/dsh-remote-agent`](./crossing/samples/06-zbzbhs-dsh-remote-agent.md) | crossing | delegation（远端 loop） | hub/worker 双角色；副机跑完整 loop（in-process 或 headless） | [`memo`](./crossing/_证据/06-remote-agent-源码复核.md) |
| 07 | [`Nwflower/dsh-file-claim`](./coordination/samples/07-Nwflower-dsh-file-claim.md) | coordination | teams（写冲突） | 边车认领 + pre-execute deny；无 epoch，pid 进程粒度 | [`memo`](./coordination/_证据/07-file-claim-源码复核.md) |
| 08 | [`Chinesezjc/dsh-interconnect`](./crossing/samples/08-Chinesezjc-dsh-interconnect.md) | crossing | teams（inbox 投递） | 每个已配置对端一条 WS；共享 token、无幂等、无离线队列 | [`memo`](./crossing/_证据/08-interconnect-源码复核.md) |
| 09 | [`IKEASven69/dsh-takeover`](./crossing/samples/09-IKEASven69-dsh-takeover.md) | crossing | delegation（会话接力） | 只替换会话：新建 + 投递 `/resume-*`；文件总线恰好一次 | [`memo`](./crossing/_证据/09-takeover-源码复核.md) |
| 10 | [`Asher-2000/dsh-expert-mode`](./teams/samples/10-Asher-2000-dsh-expert-mode.md) | teams | delegation（preset 造成员） | 17 个委派工具别名 + prompt 约定；rc.3 装不起来 | [`memo`](./teams/_证据/10-expert-mode-源码复核.md) |
| 11 | [`february2015/dsh-taskswarm`](./pipelines/samples/11-february2015-dsh-taskswarm.md) | pipelines | coordination（worktree 隔离） | 每 lane 一个 worktree + 分波并行；npm 已全量下架 | [`memo`](./pipelines/_证据/11-taskswarm-源码复核.md) |
| 12 | [`2507483326/dsh-eteams`](./teams/samples/12-2507483326-dsh-eteams.md) | teams | delegation（continuable） | 领队拆任务、成员子会话；persona 仅 0.1.x 成立 | [`memo`](./teams/_证据/12-eteams-源码复核.md) |
| 13 | [`Noelune/dsh-agent-relay`](./crossing/samples/13-Noelune-dsh-agent-relay.md) | crossing | pipelines（投递/幂等） | HTTP broker + 长轮询 + wake；npm 0.5.0 不含这些 | [`memo`](./crossing/_证据/13-agent-relay-源码复核.md) |
| 14 | [`PerryLink/dsh-team-rooms`](./crossing/samples/14-PerryLink-dsh-team-rooms.md) | crossing | coordination（持久化游标） | 房间存储权威；rc.3 禁 fact，重建副本不可用 | [`memo`](./crossing/_证据/14-team-rooms-源码复核.md) |
| 15 | [`Garybot126/dsh-subagent-models`](./delegation/samples/15-Garybot126-dsh-subagent-models.md) | delegation | —（委派路由） | 在 agent/request 上覆盖 child 的 provider/model/effort | [`memo`](./delegation/_证据/15-subagent-models-源码复核.md) |
| 16 | [`tkaiz0406/dsh-subagent-route-pin`](./delegation/samples/16-tkaiz0406-dsh-subagent-route-pin.md) | delegation | teams（startActivation 缝） | rc.3 上靠 startActivation 钩子写路由；provider.start 只走外部分支 | [`memo`](./delegation/_证据/16-route-pin-源码复核.md) |
| 17 | [`aleskxyz/dsh-subagent-fork-lite`](./delegation/samples/17-aleskxyz-dsh-subagent-fork-lite.md) | delegation | —（截断 fork） | 只 seed 最近 N 个完成 turn；面向 0.1.x | [`memo`](./delegation/_证据/17-fork-lite-源码复核.md) |

## 2. 按家族看

- **delegation（3）**：15 在 `agent/request` 上做子代理模型路由；16 包装 provider 在 child 创建前钉路由；17 截断 fork 的 seed 窗口；宿主契约见 `delegation/01`。
- **teams（6）**：01 调度/邮箱、02 全栈 runtime、04 独立根 Agent、05 质量门返工、10 preset 反证、12 continuable 成员。
- **pipelines（2）**：03 代码即编排、11 worktree lane；两者都缺“声明式 DAG”对照，是下一批研究重点。
- **crossing（5）**：06 远端 worker、08 跨实例消息、09 会话接管、13 异构 broker、14 房间持久化。
- **coordination（1 + 横向）**：07 是唯一真拦写的冲突样本；其余靠跨家族对照补。

## 3. 选主家族的规则

1. 看卡片“设计思路”里**它自己拥有的状态**：拥有 roster/任务板 → teams；拥有执行图/缓存 → pipelines；拥有会话/连接 → crossing；只拥有委派调用 → delegation。
2. 一个样本只能有一个主家族；其它角色写进 `also_in` 与本表“交叉角色”。
3. 主家族有争议时，按“用户会从哪个问题进入”决定，并在本表注明。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 14 个样本的主家族与交叉角色 | `[OBS]` | 各样本卡设计思路 + 本册分类法 | 分类是观察框架，可调整 |
| 每张样本都有固定版本 memo | `[DOC]` | 卡头“证据链”与 `_证据/` 文件 | 结构事实，不等于机制已验证 |
| 样本机制一句话概括 | `[SRC-TARGET]`/`[DOC]` | 各自 memo 的偏差表 | 细读请回卡片与 memo；未跑行为见 `[OPEN]` |
