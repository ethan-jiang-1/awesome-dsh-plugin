---
title: "样本百科：协作插件逐个深读"
domain: agent-collab
kind: index
positioning: "14 个协作样本的同表对照：设计思路、成员是什么、三笔税、代价、标杆六项。"
takeaway: "一张可逐格填的判断表；新插件拿它过一遍。"
read_when: "要横向比较多个协作样本；或要给一个新插件填判断表。"
status: observed
updated: 2026-10-31
---
# 03 · 样本百科：十四个协作插件逐个深读

> **状态**:`observed` · **基线**:DSH `0.2.1-rc.3` · 名单 @ `efe602e7b` · **源码**:14 个仓库浅克隆逐文件读过；**14 张样本均已配固定版本证据 memo**，卡头“证据链”可直达
> **一句话**:每个样本按同一张表读完——**设计思路 → 成员是什么 → 状态/冲突/收敛 → 子代理的具体做法 → 代价 → 标杆六项**。要判断一个新插件,拿这张表逐格填。

## 1. 命题

> 生态里“能派活”的插件有几百个,但真正**定义形状**的只有少数几个。它们的差别不在功能数量,而在**对同一个宿主接缝做了不同的假设**——假设不同,失效条件就不同。

可证伪点:若十四个样本在「成员是什么」这一格上高度一致,说明这门手艺已经收敛,本卡无价值。

## 2. 入选与影响力口径

**旧口径失效了。** 本域原准入规则里的 **A（目录内被引 ≥3 次）在这个生态里几乎无法区分样本**——用  自己的 `citation_counts()` 重算,下表样本里只有 `limuyang2/agent-team` 达到 被按名提到,其余全是 0。原因是目录里的 `description` 是各自写的推销语,极少互相点名。

**新口径：实时拉取、标注日期。** 下表所有 GitHub 数字为 **2026-10-31** 实时 API 采样(脚本与输出留档在仓库外的 `.work/` 工作区,不随文档发布);`catalog` 列是 `data/stars.json` 的 **2026-08-19** 旧快照,用来看涨幅。

| 样本 | 实时 ★ | fork | 实时 star 涨幅(catalog→now) | npm 近 30 天 | 类别 | 边界 | 能力披露 |
|---|---|---|---|---|---|---|---|---|
| `NanmiCoder/dsh-agent-teams` | **2610** | 223 | 573 → 2610(×4.6) | **50,995** | workflow | 1+2 | 5 |
| `toolclub/dsh-agent-team-gui` | **286** | 6 | 84 → 286(×3.4) | — | workflow | 1+2 | 0 |
| `omdsh-dev/dsh_workflow` | **153** | 11 | 82 → 153(×1.9) | — | workflow | 1 | 6 |
| `limuyang2/agent-team` | 47 | 7 | — | 2,416 | workflow | 2 | 6 |
| `Chinesezjc/dsh-interconnect` | 38 | 3 | 34 → 38 | — | session | 3 | 0 |
| `Asher-2000/dsh-expert-mode` | 13 | — | 5 → 13 | — | tools | 1(preset 路线) | 3 |
| `Nwflower/dsh-file-claim` | 7 | — | 6 → 7 | 331 | session | 2 | 4 |
| `Mlte0907/dsh-teams-x` | 3 | — | — | 89 | workflow | 1+2 | 9 |
| `zbzbhs/dsh-remote-agent` | 4 | — | — | — | remote | 3 | 0 |
| `IKEASven69/dsh-takeover` | 0 | 0 | — | 0（npm 404） | session | 3（会话接力） | 0 |
| `february2015/dsh-taskswarm` | 3 | — | — | 0（包已下架） | workflow | 2 | 0 |
| `2507483326/dsh-eteams` | 2 | — | — | 1,251 | workflow | 1 | 0 |
| `Noelune/dsh-agent-relay` | 4 | — | — | latest 0.5.0（0.6–0.8 未发布） | remote | 3 | 6 |
| `PerryLink/dsh-team-rooms` | 3 | 0 | — | 2,099 | session | 2 | 4 |

> **给未来的读者**:星标在这门生意里是**滞后指标**。`dsh-agent-teams` 的通行度几乎是第二名的 9 倍,但在 2026-08 的快照里它只有 573 星,和第八名只差一个数量级。**任何拿静态 star 排序的资料,读起来都要减一个月。**

### 2.1 九项必答(本域「缺一不立卡」的对照表)

每个样本在 §3 的正文里都答了下面九格。先给一张横表,便于横向比较:

| 样本 | 过门值 | 边界 | 成员形态 | 权威状态 | 冲突裁决 | 失败收敛 |
|---|---|---|---|---|---|---|
| `dsh-agent-teams` | C+D+G | 1+2 | 可续子代理 | 磁盘 `team.json` | 无(完成时审计) | parked+冷恢复 |
| `dsh-agent-team-gui` | C+G | 1+2 | 可续子代理 | storageDomain 8 表 | 无 | 不收敛(全 interrupted) |
| `dsh_workflow` | C+D+G | 1 | 一次性子代理 | 不可变胶囊快照 | 无 | 快照重跑+缓存 |
| `agent-team` | A+D | 2 | **独立根 Agent** | storageDomain 5 表 | 无(`leases` 空表) | 启动恢复+重投 |
| `dsh-teams-x` | D+G | 1+2 | 可续子代理 | 磁盘 `.teams-x/` | 无(完成时审计) | 对账器(软收敛) |
| `dsh-remote-agent` | F+G | 3 | **不是子代理**(远端独立 agent) | 副机本地 | 不适用 | 心跳+断点续传 |
| `dsh-file-claim` | C+F+G | 2 | **无成员概念**(只有会话 tag) | 工作区边车 | **`pre-execute` deny** | 租约过期+pid 判活 |
| `dsh-interconnect` | F+G | 3 | 不适用(投递到对端 session) | 对端 inbox | 不适用 | 无幂等/无离线队列 |
| `dsh-takeover` | F+G | 3 | 不适用(卡片即工作单元) | `~/.handoff/` | 认领文件 `wx`+冲突副本 | 认领 60s 清扫 |

**读法**:横着看每一行,能立刻看出这个样本在哪一笔税上是空的;竖着看每一列,能立刻看出这门手艺在哪个问题上还没有共识——**「冲突裁决」一列有七行是空的**,这就是整个生态最大的共同缺口。

## 3. 主样本：九个逐文件深读 + 五个补充

每个样本独立成篇,**单看一篇就能判断要不要借鉴,不需要来回翻**。每篇固定五段,顺序一致:

```text
① 头部四行 —— 一句话 / 边界 / 过门值 / 影响力(带采样日) / 什么时候找它
② 设计思路与子代理做法 —— 它到底怎么实现的(含代码行号级细节)
③ 三笔税与代价 —— 状态归属 / 冲突裁决 / 失败收敛,各写「它的答案」与「代价」
④ 精确坐标 —— 仓库 URL / npm 包名 / 版本 / License / 安装串 / 接线方式 / 复现要点
⑤ 借用指南 · 可借鉴(直接抄) —— 编号清单,每条给原理
⑥ 借用指南 · 别照抄 —— 那些「读起来像能力、实际是空壳」的地方
```

**为什么这样切**:借鉴时人是按「我要解决哪个问题」去找的,不是按「生态里都有谁」去找的。所以每篇头部都给一句**什么时候找它**,而不是给一句「它很优秀」。而 ④ 那一段存在的理由更直接:**万一要回源精确挖掘,得知道到哪去挖、包叫什么、装哪个串**——这个生态里仓库名、npm 包名、安装串三者经常对不上(见下表「拼写陷阱」列)。

| # | 仓库 | npm 包名 | 拼写陷阱 | 一句话 | 什么时候找它 |
|---|---|---|---|---|---|
| [01](teams/samples/01-NanmiCoder-dsh-agent-teams.md) | [`NanmiCoder/dsh-agent-teams`](https://github.com/NanmiCoder/dsh-agent-teams) **2592★** | `@nanmicoder/dsh-agent-teams` | 唯一**带 scope** | 成员=可续子代理;磁盘 `team.json` 为真相源;idle 边沿调度 | **成员要能被反复追问、要记住上一轮** |
| [02](teams/samples/02-toolclub-dsh-agent-team-gui.md) | [`toolclub/dsh-agent-team-gui`](https://github.com/toolclub/dsh-agent-team-gui) 285★ | `dsh-agent-team-gui` | **未发 npm**(只能 Git 装) | 「默认不派活」写在提示词里;有界 DAG;借官方 `tokenUsage` 计量 | 想省掉「先起规划器」那次调用 |
| [03](pipelines/samples/03-omdsh-dev-dsh_workflow.md) | [`omdsh-dev/dsh_workflow`](https://github.com/omdsh-dev/dsh_workflow) 153★ | `@dsh-external/workflow` | **包名与仓库名完全不同**;未发 npm | 没有 DAG,JS 控制流即编排;快照重跑+缓存回放 | 要一条**可复现**流水线,接受不是断点续跑 |
| [04](teams/samples/04-limuyang2-agent-team.md) | [`limuyang2/agent-team`](https://github.com/limuyang2/agent-team) 47★ | `@limuyang2/dsh-agent-team` | 仓库名**无**前缀、包名**有** | 成员=**独立根 Agent**,为成员异构放弃子代理 | 每成员要用**不同模型/权限/技能包** |
| [05](teams/samples/05-Mlte0907-dsh-teams-x.md) | [`Mlte0907/dsh-teams-x`](https://github.com/Mlte0907/dsh-teams-x) 3★ | `dsh-teams-x` | — | 与官方最要命的三条限制逐条应战 | 想要质量门自动派生返工 |
| [06](crossing/samples/06-zbzbhs-dsh-remote-agent.md) | [`zbzbhs/dsh-remote-agent`](https://github.com/zbzbhs/dsh-remote-agent) 4★ | `dsh-remote-agent` | **npm 3,103/月**,星标看不出 | 副机本地跑完整 agent loop;跨机=信任问题 | 要跨机且**不能被网络拖死** |
| [07](coordination/samples/07-Nwflower-dsh-file-claim.md) | [`Nwflower/dsh-file-claim`](https://github.com/Nwflower/dsh-file-claim) 7★ | `dsh-file-claim` | **npm 1,064/月**;唯一 `.mjs` 入口 | `tools/pre-execute` 返回 deny——唯一真拦住写 | 怕两个人改同一文件 |
| [08](crossing/samples/08-Chinesezjc-dsh-interconnect.md) | [`Chinesezjc/dsh-interconnect`](https://github.com/Chinesezjc/dsh-interconnect) 38★ | `dsh-interconnect` | 插入**三个**插件行 | 跨 DSH 实例的消息总线;无幂等、无离线队列 | 要跨实例投消息/同步事件 |
| [09](crossing/samples/09-IKEASven69-dsh-takeover.md) | [`IKEASven69/dsh-takeover`](https://github.com/IKEASven69/dsh-takeover) 0★ | `dsh-takeover` | **未发 npm** + 0★ | 没有协议,只有文件;`open(claim,'wx')` 做恰好一次 | 要跨机但**不想写任何协议** |


**三篇值得先读**:[01](teams/samples/01-NanmiCoder-dsh-agent-teams.md)(骨架最完整,可当模板)、[07](coordination/samples/07-Nwflower-dsh-file-claim.md)(唯一真裁决,且它的「无 fencing」是最重要的反面教材)、[06](crossing/samples/06-zbzbhs-dsh-remote-agent.md)(最值钱的一条失败语义:假成功)。

## 4. 旁支：五个,同样一样本一文件

旁支不「不深读」。凡是机制核清了的,**一样一个文件**,因为它们各自补的正是本域最缺的几块拼图:worktree、broker、跨会话持久、preset 打包、`persona` 的合法路径。

| # | 样本 | 它补的是哪块空白 | 一句话 |
|---|---|---|---|
| [10](teams/samples/10-Asher-2000-dsh-expert-mode.md) | `Asher-2000/dsh-expert-mode` 13★ | **不用插件写协作**:preset 路线 | 17 条静态工具行 = 17 个成员;但**在当前宿主装不起来** |
| [11](pipelines/samples/11-february2015-dsh-taskswarm.md) | `february2015/dsh-taskswarm` 3★ | **worktree 到底怎么用** | 每 lane 一个 worktree,失败时刻意不清理 |
| [12](teams/samples/12-2507483326-dsh-eteams.md) | `2507483326/dsh-eteams` 2★ | **`persona` 的合法路径** | 走 `startContinuable` 请求参数,不走 config 字段 |
| [13](crossing/samples/13-Noelune-dsh-agent-relay.md) | `Noelune/dsh-agent-relay` 4★ | **跨异构运行时** + 对端离线怎么办 | 回环 broker + `wake_command` 兜底;删掉自己的一半 |
| [14](crossing/samples/14-PerryLink-dsh-team-rooms.md) | `PerryLink/dsh-team-rooms` 3★ | **跨会话持久化** | 房间存储是权威,成员日志是重建副本;游标只在落地后前进 |

**它们合起来的结论**:五个旁支各补一个具体空白,但**没有一家把三笔税答完两笔以上**——这不是巧合,是「补一个尖角」比「补齐三笔税」容易得多,也正是本域命题要提醒的事。

## 5. 横切结论

**① 成员可续 = 结果不可读的补丁。** 凡是需要队长追问成员的样本(`agent-teams`/`teams-x`/`team-gui`),成员都是可续子代理;凡是把成员做成独立根 Agent 的(`agent-team`),就必须自己实现全部编排且放弃 spawn/interrupt/wait。**这条因果链由宿主能力决定,不是品味。**

**② 「schema 里有」不等于「代码里有」。** `agent-team` 的 `leases` 表与 `dependencyIds` 都是空壳;`teams-x` 的 `verify` 只是字符串清单,插件不执行;`agent-teams` 的 `writeScopes` 类审计是完成时的,拦不住。**读字段表会高估一个协作插件。**

**③ 三笔税没人交齐。** 见 [02 §4](coordination/02-mechanisms.md#4-三笔税的联合分布九家各选了什么) 的九家分布表。

**④ 影响力与不可替代性不相关。** `file-claim` 7 星,但它是唯一做写权裁决的;`agent-teams` 2592 星,但它的冲突裁决是空白。**选型要按需要哪笔税来选,不按星标选。**

**⑤ 成本优化最便宜的一刀在提示词里。** `team-gui` 把「要不要派活」塞进本来就一定会发生的那次推理,零额外调用;而所有 router Agent 方案都要先花一次调用才知道该不该花。

## 6. 体验

**人**:九个样本的操作面差异巨大——`agent-teams` 是「批准后运行」的两段式(先看花名册与 DAG,再批准),`team-gui` 是「存好小队、按需触发」,`dsh_workflow` 是「生成/保存/运行胶囊」,`agent-team` 是「先挑助手再建队」。**共同点是:人总要在派工之前对“谁来做”做一次确认**,只是确认的时机不同(建队前 / 派工前 / 计划后)。

**模型**:成员都只看到自己的工具与自己的上下文;队长看到的是任务板与邮箱,不是成员的过程。跨实例/跨机时,`interconnect` 的 `source`/`sender` 甚至**不进模型上下文**,`remote-agent` 的副机 agent「不知道自己在被远程派单」。**协作在模型侧是层层隔断的。**

## 7. 失败模式(跨样本汇总)

| 失败 | 谁踩过 | 根因一句话 |
|---|---|---|
| 假成功 | `remote-agent` | 完成判据没看 `agent/error` |
| 重启归零 | `team-gui`、`dsh_workflow` | 没有执行级检查点 |
| 静默失锁 | `file-claim` | 租约无 fencing,接管不通知原主 |
| 空壳字段 | `agent-team` | schema 先行、实现未跟上 |
| 自述当证据 | `teams-x`、`agent-teams` | 质量门只校验自洽,不执行 verify |
| 重复投递 | `interconnect`、`teams-x` | 无消息级幂等 |
| 第二真相源失步 | `agent-teams`、`teams-x` | 磁盘做真相,会话日志降级为审计 |
| 容量墙 | `agent-teams`(8)、`team-gui`(32) | 撞宿主 `maxActiveSubagents` |
| 误识别成别家 | `teams-x` | 名字近似,prepublish guard 防误认 |

## 8. 评估清单(给下一个待评样本)

1. **成员是子代理,还是独立根 Agent?** 这决定它能不能用 `followup` 追问、能不能被 `interrupt`。
2. **不续聊时,结果怎么拿到?** 若靠「读成员的最终文本」,它一定是错的——那是不可程序化读取的。
3. **权威状态在会话日志里,还是它自己的一份盘上文件?** 后者要检查并发假设。
4. **它的 `capabilities` 声明与代码一致吗?** 抽查 `leases`/`dependencies`/`verify` 这类容易被做成空壳的字段。
5. **完成判据是自述还是证据?**
6. **重启后会发生什么?** interrupted 是否可续跑?
7. **它和官方 `dsh-experimental-agent-team` 同装会怎样?** 有没有互斥声明,还是只是名字不同。
8. **它的成员配置粒度是什么?** 一个成员能不能有自己的模型/权限/技能包——不能的话,它就是官方 roster 的薄包装。

## 9. 开放问题

- [x] `[OPEN]` preset 路线能否支撑成员生命周期 → **暂不能**:`persona` 配置键已被宿主移除、preset 目录已失效、子代理只能被父唤醒。三条都不是插件能补的 → 本卡 §4
- [ ] `[OPEN]` 若宿主把成员人格配置**挪回 preset 声明**(而非 tool config),preset 路线会不会吃掉一部分 roster 插件?目前看它是唯一能绕开 roster 状态机的路。
- [ ] `[OPEN]` worktree 隔离的正解:每成员一个 worktree,还是每任务一个快照(`dsh-taskswarm`)?`worktree` 45 条样本里两者的比例,尚无盘点。
- [ ] `[OPEN]` 为什么生态里没人给自己加 **epoch/fencing**?候选解释:宿主只给了 `tools/pre-execute` 这一个写面钩子,而 shell 一绕就失效,所以 fencing 的收益上限被锁住了。
- [ ] `[OPEN]` `dsh-agent-teams` 用 2592 星确立了事实标准吗?若它继续领先,别的 roster 插件会退化成它的兼容层,还是继续分裂?
- [ ] `[OPEN]` 本域的 A 门(目录内被引 ≥3 次)在这门生态里失效了。是否需要一个新的、可复核的默认影响力口径(实时 stars 涨幅 + npm 下载 + fork)?——这已超出单域可改范围,须提给杠杆层统筹。
