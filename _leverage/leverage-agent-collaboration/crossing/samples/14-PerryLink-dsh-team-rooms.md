---
title: "PerryLink/dsh-team-rooms"
domain: agent-crossing
kind: sample
positioning: "`PerryLink/dsh-team-rooms@1.0.8`（已 archived，npm deprecated）：房间存储是权威；但成员日志重建依赖 rc.3 禁止的 `team-room/fact`。"
takeaway: "房间存储为权威 + 单写链；但重建副本在 rc.3 不可用，游标是“入 inbox 后前进”，catchUp 会跳过丢失段。"
read_when: "团队要跨会话活着，且最关心「消息会不会丢、重启后还在不在」。"
status: observed
updated: 2026-10-31
---
# 14 · `PerryLink/dsh-team-rooms`

> **一句话**：房间存储是跨会话权威，但“每个成员的日志是重建副本”只在能写 `team-room/fact` 的宿主成立；**0.2.1-rc.3 明确禁止该事件，`teamRoom` 投影退化为空**。该项目已于 2026-10-05 退役（仓库 archived、npm deprecated）。
> **边界**:2 同工作区多成员(**以会话为成员单位**,跨会话持久) · **定位**:**持久化流派**代表:本域唯一把「重启后还在不在」当核心命题的样本 · **证据级别**:`observed`(源码逐文件读过)
> **影响力**(2026-10-31 实时采样):**3★** / npm **2,099 次/月**——**本域旁支里下载量最高的一个**;唯一 Apache-2.0
> **什么时候找它**:团队要跨会话活着,且你最关心「消息会不会丢、重启后还在不在」

> 导航:[样本索引](../../encyclopedia.md) · [域章程](../../00-map.md) · [三笔税机制谱](../../coordination/02-mechanisms.md) · [四道边界](../../coordination/01-taxonomy.md)
> **证据链**：npm/tag/commit 对齐（`1.0.8`=`c1c485e`），但仓库已 archived、npm 已 deprecated；`team-room/fact` 在 rc.3 被禁、游标语义见[`14 源码复核`](../_证据/14-team-rooms-源码复核.md)。

## 设计思路

**它的核心命题只有一句**:`The room store is the cross-session authority; the session projection is each member's own reconstructed copy.` 房间存储是**跨会话权威**,每个成员看到的是自己那份**重建出来的副本**。这句话把「状态归属」这笔税一次性钉死了。

**四条机制保证它“重启后还在”**（但需限定宿主能力）：

1. **单写链排序** —— 每一次房间变更(create / join / leave / post / 任务状态)都**排在唯一一条 hub 写链**上;`team_rooms` 域的写链就是**排序权威**,所以并发发帖永远不会交错。
2. **「模型可见 ⟺ 已记录」** —— 投递的room消息就是一次官方的 inbox 投递:`agent.followup` 唤醒活着的成员,`agent.inject` 在成员下次启动时把积压交给它。**所以它落成了一条持久的 `user/message`**,而不是只活在内存里。
3. **共享时间线镜像成 log-only 事件** —— 时间线写进每个成员日志时带 `team-room/fact` 事件与规范存储的 `timelineSeq`；`teamRoom` 投影折每个成员自己的日志。**但 rc.3 禁止该事件写入，投影因此为空**——这一条在当前宿主上不成立。
4. **至少一次 + 有序** —— 逐成员游标 `lastDeliveredSeq` 在 live 路径上是**入 inbox 后前进**（不是 `user/message` 落地后）；`lastFactSeq` 依赖 fact。`catchUp` 在 agent 缺失、fact 被跳过、bus 已过留存窗时仍把游标推到末尾，会跳过丢失段。

**安全边界写得异常清楚**(本域最规范的样本):

- **审批门控的交接** —— `room_transfer_task` 走官方 approval seam,没有 approval 服务或没人批准时**fail closed**,拒绝则什么都不变。
- **模型可见 ⟺ 已记录** —— 房间消息**永远不可能「到达模型却没进日志」**。
- **成员身份就是授权边界** —— 每个 `room_*` 工具都按**调用方自己的会话**授权,非成员得到稳定拒绝,而不是部分写入。
- **留存有界** —— bus / timeline / done-task 三个窗口在**每次写**时执行,长期房间不会无限膨胀。
- **不调度、不跨机** —— 成员是本部署的**进程内会话**。

**`inbound`(P2)是它最漂亮的一招**:外部 agent 运行时(OpenAI Agents SDK、CrewAI 之类)可以通过**换行分隔的 JSON-RPC 2.0 over stdio** 往房间里发消息。只需两个 Config 字段指向一个 launcher,它每行吐一个 JSON 通知:

```yaml
inbound:
  enabled: true
  command: "python external_runtime.py --room <room-id>"
```

三种通知各自落回房间已有的表面:`agent_started` → **开任务板卡片**;`agent_message` → **发消息总线**;`agent_finished` → **完成任务卡并附结果**。非法消息 fail closed。**这等于给任何外部框架开了一个零代码适配口。**

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`PerryLink/dsh-team-rooms`](https://github.com/PerryLink/dsh-team-rooms) |
| **npm 包名** | `dsh-team-rooms` |
| **版本(本次读)** | `1.0.8` @ tag `v1.0.8` = commit `c1c485e`（npm 同 SHA）；**仓库 archived、npm deprecated（2026-10-05）** |
| **License** | **Apache-2.0**——本域唯一非 MIT 的样本 |
| **npm 近 30 天** | **2,099 次**——旁支里最高,接近 `agent-team` 的 2,416 |
| **安装** | `npm i -g dsh1024`(CLI 名与包名不同)→ 装进 profile;或从 npm 已发布版本装 |
| **接线方式** | `main: ./lib/index.js`;`dsh.bundle.patch` + **有 client 注入** |
| **硬依赖** | **必须组合 `@deepseek-ai/dsh-storage-domain`**;没有它,`/room` 命令与 `room_*` 工具直接禁用 |
| **兼容性** | 依赖 `Session.append` 的 `ignorable` 标记;早于该标记的 rc 线(含 `0.1.0-rc.8`、`0.1.1-rc.2`)行为不同 |

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | **房间存储是跨会话权威**,成员日志是重建副本;单写链排序 | 强依赖 `dsh-storage-domain`,缺域则整插件禁用 |
| 冲突裁决 | **成员身份即授权边界**;交接走 approval,拒绝则 fail closed | **不调度、不跨机**,成员必须是本部署进程内会话 |
| 失败收敛 | 至少一次 + 有序：live 游标入 inbox 后前进；catchUp 会为跳过段推进游标 | 重建副本依赖 rc.3 禁止的 fact 事件；成本统计不在范围内 |

## 借用指南

### 可借鉴(直接抄)

1. **「模型可见 ⟺ 已记录」当成不变量** —— 任何到达模型的消息必须先是日志里的持久 `user/message`。这一条把所有「模型看见了但机器不记得」的诡异状态直接排除掉,**是本域最该抄的一条设计不变量**。
2. **游标只在落地后前进** —— `lastDeliveredSeq` 提交后才推进,于是崩溃只会**重投**,不会**丢**。比你自研的 ack 协议简单,也比只做「已投递」标记可靠。
3. **单写链做排序权威** —— 所有变更排一条链,并发发帖不可能交错。比自己想锁省事。
4. **JSON-RPC over stdio 当外部框架接入口** —— 任何能吐 JSON 行的运行时都能加入房间;三种通知映射到已有的任务卡/消息/完成三个表面,**不需要为每个框架写适配器**。
5. **approval 门控 + fail closed** —— 交接任务走官方 approval seam,没批准就什么都不变。**拒绝必须是干净的,不能是部分写入。**
6. **留存窗口在每次写时执行** —— 而不是靠后台任务清理;长期房间不会膨胀。
7. **`Not this plugin` 一节** —— README 里有一段明确写「这不做什么、边界在哪」。**主动划清边界比罗列功能更能让人信任。**
8. **`Known limitations` 写全 5 条**(需 storage-domain、成员是会话不是用户、不跨机、交接需 approval answerer、不算成本)——每一条都具体到能直接判断「适不适合我」。

### 别照抄

- 别指望它跨机:**每个成员都是本部署的进程内会话**。
- 别在没有 `dsh-storage-domain` 的 profile 里装它 —— 装了也不会出现 `/room`。
- 别把成员当用户:成员是**会话级**的,`maxMembersPerRoom` 有上限。
- 成本统计不在它的范围内,想记账得自己接 `tokenUsage`。
