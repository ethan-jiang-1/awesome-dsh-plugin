---
title: "lever-cross-boundary：协作边界"
domain: cross-boundary
kind: charter
positioning: "本域宪章：四道边界、三笔税、十条可迁移做法、选型决策树与 14 个样本坐标。"
takeaway: "10 条可迁移做法 + 四态证据账本 + 选型决策树 + 6 条别照抄。"
read_when: "要做多 agent/协作/跨机；或要判断一个协作插件跨的是哪道边界。"
status: observed
updated: 2026-10-31
budget: 340
---
# lever-cross-boundary · 协作跨到哪个边界，每跨一界多付什么

> **标语**:*Which boundary does collaboration cross, and what does each crossing cost?* —— 协作是状态问题，不是 spawn 问题。
> **状态**:`observed`(**14 个样本源码逐文件读过**,9 主 + 5 旁支) · **基线**:DSH `0.2.1-rc.3` · 名单 @ `efe602e7b` · **影响力数据采样日**:2026-10-31
> **作业区**:**本目录自足、可独立开工**。只读共享件,不写共享件;不引用其他域的结论,不等待其他域的进度。四域并行契约见 [`../README.md`](../README.md#三域并行作业契约)。
> **只想拿走东西** → 直接跳 [能借鉴什么](#能借鉴什么本域主产出):十条可迁移做法、一条四态证据账本、一张选型决策树、动手前的五个问题、六条「别照抄」。
> **要回源去挖** → 直接跳 [精确坐标速查](#精确坐标速查要回源就去这里):九个**主**样本的仓库 URL / npm 包名 / 版本 / 安装串 / 拼写陷阱;旁支五个的坐标在各自文件里。
> **借阅入口**:想抄 → [能借鉴什么](#能借鉴什么本域主产出) · 想选型 → [选择要求](#选择要求) · 想评审 → [六条别照抄](#六条别照抄) · 想回源 → [精确坐标](#精确坐标速查要回源就去这里) · 跨域 → [BORROW](../BORROW.md)
> **规则源**:准入/分级以 [`horizon`](../horizon.md) 为准;本域的准入副本是摘要。
> **全量卡片**:本表是精选;全部文件(kind/定位/能拿走什么/何时读)见 [`catalog`](../catalog.md)。

## 这个域问什么

从“一个 agent 自己干”到“多个 agent 一起干”，中间要跨四道边界：同一 agent 内、同一进程的父子之间、同一工作区的多名成员之间、不同进程甚至不同机器之间。**每跨一道，做的事多了，但新增的不是“能派活”，而是要回答三个新问题：**

1. **共享状态归谁？** 谁拥有 roster、任务、消息、证据。
2. **冲突谁裁决？** 两个人写同一个文件，谁赢？
3. **崩溃后谁收敛？** 部分失败留下什么，谁来收拾。

**判断标准**：一个协作插件影响的不是“能不能多开几个 agent”，而是**它让协作状态寄生在哪一层**。

## 收录 / 不收录

收录：

- 定义**成员关系与角色**的（team、roster、captain、角色卡片、专家名册）
- 定义**任务与消息传递**的（任务板、邮箱、inbox、handoff、派发路由）
- 定义**工作区隔离与合并**的（worktree、共享 checkout、镜像同步）
- 定义**跨进程/跨机传输**的（SSH、ACP、A2A、远端工作区、移动端接力）

不收录：

- 只做“子代理模型选择/路由”的 → 属杠杆阶梯 4 级（policy 钩子），单独立小卡，见 §4
- 单纯换模型提供方的 → 归 `ecosystem/`
- 团队 UI 面板（看板、活动球、树形视图）→ 只在它**承载了状态**时才收；纯展示归 `lever-reshape-product` 的槽位层

## 准入(本域自带副本,不依赖任何其他文档)

**不是抓到一个就琢磨。** 研究对象不随名单膨胀:**卡片数不随收录量涨,只随「机制被验证」涨**。

> **⚠ A 门在本域不成立,以 C/D/F/G 立卡。** 九个研究对象里,按名互引几乎为零——目录 `description` 极少互相点名,样本之间是**功能竞争**而非引用关系。故本域以 **C**(具名接缝)/ **F**(少见,人工判断)/ **D**(能力披露)/ **G**(机制已核)立卡,影响力改用**实时 GitHub + npm 数据**(采样日标在每张卡里)。这是**域级口径修正**,已在 [horizon](../horizon.md) §4 记录。

| 组 | 证据 | 怎么判 |
|---|---|---|
| 影响力 | **A** 被目录内其他条目按名提到 · **B** 自述替换/接管官方对象 · **C** 自述具名接缝 · **F** 全库同类机制少见 | A/B/C 回读原文;**F 人工判断,标 `[OBS]`,不计数** |
| 深度 | **D** 能力披露 · **E** 明指不可共存 / 同缝取反 · **G** 机制已核且有具名失效条件 | D 查 capabilities;**E/G 人工** |

**缺一不立卡。** 分级:**S** 定义型(后来者的模板)→ 单独卡片 · **A** 代表型(当前优解)→ 卡片「标杆」正例 · **B** 对照型 → **不立卡**,只作一行对照 · **C** 反例型 → 失败模式表一行。

每条进入卡片的样本必须写齐六项:**代表什么典型 / 为什么选它(过的哪几条证据)/ 影响力证据(被谁提到、替换了哪个官方对象、或官方原文;不要求计数)/ 主要特点(机制层)/ 代价与失效条件(具名)/ 证据级别**。缺一项退回。

### 本域专项加分项

- **边界可命名**:必须跨 **边界 1 同进程父子 / 2 同工作区多成员 / 3 跨进程跨机** 中可指认的一道。
- **三问可答**:状态归谁(roster/任务/消息/证据在哪)、冲突谁裁、崩了谁收敛——答不全的,只能算工具,不算协作机制。

### 本域明确不收

- 子代理模型路由 → 那是 `agent/request` 上的 policy 钩子,只做旁支
- 纯看板、活动球、树形视图 → 不承载协作状态
- 只做「能派活」而说不出状态归属的 → 正是本域命题要反驳的东西

### 本域研究对象(主读,单一归属)

**影响力口径已更换。** 原 A 门(目录内按名互引)在本生态里几乎不成立——九个样本里只有 `limuyang2/agent-team` 被其他条目提到。现改为**实时 GitHub + npm 数据**(采样日 2026-10-31),并保留 catalog 旧快照看涨幅。

| 级 | 样本 | 过了哪些门 | 影响力证据(2026-10-31 实时) | 一句话特点 |
|---|---|---|---|---|
| **S** | 官方 `dsh-experimental-agent-team` | G | 不是生态条目,是全域**约束源**;7 条已知限制定义边界 2 的税 | 元数据硬(CAS/tombstone)、工作区与生命周期留白 |
| **S** | `NanmiCoder/dsh-agent-teams` | C + D + G | **2592★ / 222 fork / npm 50,995 月下载**;两个半月从 573★ 涨到 2592★ | 成员=可续聊子代理;磁盘 `team.json` 为真相源;idle 边沿调度 |
| **A** | `toolclub/dsh-agent-team-gui` | C + G | **285★** / **未上 npm**;catalog 84★ → ×3.4 | 「默认不派活」写在提示词里;有界 DAG;借官方 `tokenUsage` 计量 |
| **A** | `omdsh-dev/dsh_workflow` | C + D + G | **153★** / **未上 npm**;catalog 82★ → ×1.9 | 没有 DAG,JS 控制流即编排;可恢复=快照重跑+缓存回放 |
| **A** | `limuyang2/agent-team` | **A**(被其他条目按名提到)+ D | **47★ / npm 2,416 月下载**;全表唯一被按名提到的样本 | 成员=**独立根 Agent**,为换成员异构宁愿放弃子代理 |
| **A** | `Nwflower/dsh-file-claim` | C + F + G | 7★ / **npm 1,064 月下载**;同类机制**少见**(人工判断) | 全生态唯一在写面真拦截(`tools/pre-execute` deny) |
| **A** | `zbzbhs/dsh-remote-agent` | F + G | 4★ / **npm 3,103 月下载**;「副机自主」**少见** | 把跨机从**传输问题**降级为**信任问题** |
| **A** | `Chinesezjc/dsh-interconnect` | F + G | 38★ / **npm 1,017 月下载**;跨实例消息总线**少见** | 跨 DSH **实例**的消息总线;无幂等、无离线队列 |
| **A** | `IKEASven69/dsh-takeover` | F + G | 0★ / **未上 npm**;文件总线**少见** | 最省事的跨机:**没有协议,只有文件** |
| **A** | `Mlte0907/dsh-teams-x` | D + G | 3★ / npm 89 月下载;9 项能力披露(全表最高) | 与官方最要命的三条限制逐条应战,两条自认未解决 |

**旁支(不立卡,但同样一样本一文件)**:五个旁支各补一块具体空白,单看一篇即可判断要不要借鉴。

| # | 样本 | 补的空白 | 为什么只作旁支 |
|---|---|---|---|
| [10](./samples/10-Asher-2000-dsh-expert-mode.md) | `Asher-2000/dsh-expert-mode` 13★ | **不用插件写协作**(preset 路线) | 路线成立但**在当前宿主装不起来**,是反证 |
| [11](./samples/11-february2015-dsh-taskswarm.md) | `february2015/dsh-taskswarm` 3★ | **worktree 隔离**的最完整样本 | 每 lane 一个 worktree(非每成员);npm 近月 **0** 下载 |
| [12](./samples/12-2507483326-dsh-eteams.md) | `2507483326/dsh-eteams` 2★ | **`persona` 的合法路径** | 与 [04](./samples/04-limuyang2-agent-team.md) 同赛道,取法重复 |
| [13](./samples/13-Noelune-dsh-agent-relay.md) | `Noelune/dsh-agent-relay` 4★ | **跨异构运行时 + 对端离线** | 只投消息,不涉及成员与文件 |
| [14](./samples/14-PerryLink-dsh-team-rooms.md) | `PerryLink/dsh-team-rooms` 3★ | **跨会话持久化** | 不调度、不跨机;依赖 storage-domain |

**借用但非主读**(只可一句引用,不深读、不立卡):`dsh-sandbox-policy`(主读在 `lever-draw-limit`)、`dsh-session-checkpoint-policy`(主读在 `lever-prove-output`)、`GDWhisper/dsh-web-startup-auth`(主读在 `lever-reshape-product`)。

## 选择要求

1. **边界可命名**：它跨的是“进程内 / 共享工作区 / 跨机”中的哪一道？说不出边界的，多半只是加了个工具。
2. **状态归属可指认**：roster、任务、消息、证据分别存在哪里（会话日志 / 外部文件 / 第二台机器）？谁的日志是权威的？
3. **失败语义可说清**：成员崩了、链路断了、消息丢了，协作状态往哪收敛？写不出失败语义的样本,在卡里只能标 `inferred`。

## 领域骨架：四道边界

| 边界 | 新增的问题 | 原生支撑 | 代表卡 |
|---|---|---|---|
| 0 同 agent | 无——上下文、工具、权限全共享 | — | [01-collab-topology](./01-collab-topology.md) |
| 1 同进程父子 | 上下文怎么切、深度与容量、结果怎么回 | `dsh-subagent`(spawn/fork 可续、ACP/SDK/Codex/CC 一次性) | 同上 |
| 2 同工作区多成员 | 文件冲突、任务归属、消息投递 | `dsh-experimental-agent-team`(CAS 任务板、inbox) | 同上 |
| 3 跨进程/跨机 | 身份、传输、信任、部分失败 | `dsh-api-gateway` / `dsh-acp` / worktree / SSH | 同上 |

**核心洞察(已核)**:生态的协作插件几乎全部停在边界 1+2，而边界 2 的三个致命约束（**共享 checkout、单进程、owner 不自动释放**）恰好是官方实验包自己写进「已知限制」的(7 条限制里的 3 条,逐字核对见 [01](./01-collab-topology.md) §3)。**插件不是在填空白，是在和官方限制赛跑——而且跑法不是填坑，是换一张表重画。**

三家自建 roster 的样本里,**只有一家(`file-claim`)真的去补了"冲突裁决"这一笔税,还是以放弃成员模型为代价**。其余两家都没补,而是把力气花在别处:一个补调度与邮箱,一个补成员异构配置。这条结论在 [02](./02-coordination-mechanisms.md) §4 有九家联合分布表支撑。

## 卡片索引

| 编号 | 标题 | 状态 | 一句话结论 |
|---|---|---|---|
| [01](./01-collab-topology.md) | 拓扑谱：四道边界与它们各自的税 | `observed` | 跨界的成本不在“派活”，在状态归属与失败收敛；本地最便宜，跨机最贵 |
| [02](./02-coordination-mechanisms.md) | 三笔税的机制谱：九家各怎么交 | `observed` | 每笔税有 5–7 种交法；§5.5 给出**三笔税各自的可落地配方**与依赖顺序 |
| [03](./03-sample-encyclopedia.md) | 样本索引：口径、影响力、九项横表、横切结论 | `observed` | **一样本一文件**,见下表 `samples/` |
| [samples/01](./samples/01-NanmiCoder-dsh-agent-teams.md) … [14](./samples/14-PerryLink-dsh-team-rooms.md) | **14 个样本各自独立成篇**(01–09 主,**10–14 旁支**) | `observed` | 每篇固定六段:头部 / 设计思路 / 三笔税 / **精确坐标** / 可借鉴 / 别照抄 |

### 样本卡片(一样本一文件)

| # | 文件 | 一句话 | 拿它解决什么 |
|---|---|---|---|
| 01 | [NanmiCoder/dsh-agent-teams](./samples/01-NanmiCoder-dsh-agent-teams.md) | 成员=可续子代理;磁盘 `team.json` 为真相源;idle 边沿调度 | 成员要能被反复追问、要记住上一轮 |
| 02 | [toolclub/dsh-agent-team-gui](./samples/02-toolclub-dsh-agent-team-gui.md) | 「默认不派活」写在提示词里;借官方 `tokenUsage` 计量 | 省掉「先起规划器」那次调用 |
| 03 | [omdsh-dev/dsh_workflow](./samples/03-omdsh-dev-dsh_workflow.md) | 没有 DAG,JS 控制流即编排;快照重跑+缓存回放 | 要一条**可复现**流水线 |
| 04 | [limuyang2/agent-team](./samples/04-limuyang2-agent-team.md) | 成员=独立根 Agent,为成员异构放弃子代理 | 每成员要用不同模型/权限/技能包 |
| 05 | [Mlte0907/dsh-teams-x](./samples/05-Mlte0907-dsh-teams-x.md) | 与官方最要命的三条限制逐条应战 | 想要质量门自动派生返工 |
| 06 | [zbzbhs/dsh-remote-agent](./samples/06-zbzbhs-dsh-remote-agent.md) | 副机本地跑完整 agent loop;跨机=信任问题 | 跨机且**不能被网络拖死** |
| 07 | [Nwflower/dsh-file-claim](./samples/07-Nwflower-dsh-file-claim.md) | `tools/pre-execute` 返回 deny——唯一真拦住写 | 怕两个人改同一文件 |
| 08 | [Chinesezjc/dsh-interconnect](./samples/08-Chinesezjc-dsh-interconnect.md) | 跨 DSH 实例的消息总线;无幂等、无离线队列 | 跨实例投消息/同步事件 |
| 09 | [IKEASven69/dsh-takeover](./samples/09-IKEASven69-dsh-takeover.md) | 没有协议,只有文件;`open(claim,'wx')` 做恰好一次 | 跨机但**不想写任何协议** |

### 精确坐标速查(要回源就去这里)

> **拼写陷阱是本表的重点。** 这个生态里仓库名、npm 包名、安装串三者经常对不上;抄错一个字,`dsh plugin add` 就装到别的东西或者报「找不到包」。每一行的完整坐标(含 License、接线方式、复现要点)还写在该样本的 `## 精确坐标` 一节里。

| # | 仓库 | npm 包名 | 版本 | 安装串 | 陷阱 |
|---|---|---|---|---|---|
| 01 | [`NanmiCoder/dsh-agent-teams`](https://github.com/NanmiCoder/dsh-agent-teams) | `@nanmicoder/dsh-agent-teams` | `0.1.28` | `dsh plugin add @nanmicoder/dsh-agent-teams@0.1.28` | 唯一带 scope;**必须钉版本** |
| 02 | [`toolclub/dsh-agent-team-gui`](https://github.com/toolclub/dsh-agent-team-gui) | `dsh-agent-team-gui` | `1.3.0` | Git / release 包 | **未发 npm**;装完必须重启 Web 进程 |
| 03 | [`omdsh-dev/dsh_workflow`](https://github.com/omdsh-dev/dsh_workflow) | `@dsh-external/workflow` | `0.1.2` | `dsh plugin --profile web add "github:dsh-external/dsh_workflow#main"` | **包名与仓库名完全不同**;README 的安装串 owner 是 `dsh-external` 而非 `omdsh-dev`,抄前先核 |
| 04 | [`limuyang2/agent-team`](https://github.com/limuyang2/agent-team) | `@limuyang2/dsh-agent-team` | `0.1.4` | `dsh plugin add --save-exact @limuyang2/dsh-agent-team@0.1.4` | 仓库名**无**前缀、包名**有** |
| 05 | [`Mlte0907/dsh-teams-x`](https://github.com/Mlte0907/dsh-teams-x) | `dsh-teams-x` | `0.11.5` | `dsh plugin --profile web add <node_modules>/dsh-teams-x` | 装完必须重启(`dsh plugin add` 不热加载 bundle) |
| 06 | [`zbzbhs/dsh-remote-agent`](https://github.com/zbzbhs/dsh-remote-agent) | `dsh-remote-agent` | `0.9.11` | `dsh plugin add github:zbzbhs/dsh-remote-agent` | hub 与 worker **同一个包** |
| 07 | [`Nwflower/dsh-file-claim`](https://github.com/Nwflower/dsh-file-claim) | `dsh-file-claim` | `0.2.0` | `dsh plugin add dsh-file-claim` | 入口是 `.mjs`(其余样本都是 `.js`) |
| 08 | [`Chinesezjc/dsh-interconnect`](https://github.com/Chinesezjc/dsh-interconnect) | `dsh-interconnect` | `0.13.0` | `dsh plugin --profile <name> add dsh-interconnect` | 装没装上:请求 `/interconnect/link`,403 即已装 |
| 09 | [`IKEASven69/dsh-takeover`](https://github.com/IKEASven69/dsh-takeover) | `dsh-takeover` | `0.4.3` | `dsh plugin --profile web add github:IKEASven69/dsh-takeover` | **未发 npm**;`@agent-handoff/*` 走 `file:` 链接 |

**影响力看下载量,不看星标。** npm 近 30 天(2026-09-30 ~ 10-29):`agent-teams` **50,995** · `remote-agent` **3,103** · `agent-team` **2,416** · `file-claim` **1,064** · `interconnect` **1,017** · `teams-x` **89**;而 `gui`、`dsh_workflow`、`takeover` 三个**根本没上 npm**。`remote-agent` 4★ 却有 3,103 次下载、`takeover` 0★ 且未发布——**星标与使用量在本域是两个独立的量**。

旁支五个同样一样本一文件([10](./samples/10-Asher-2000-dsh-expert-mode.md) ~ [14](./samples/14-PerryLink-dsh-team-rooms.md)),完整坐标在各自文件里;`dsh-eteams` **1,251** / `team-rooms` **2,099** / `relay` **1,048** / `expert-mode` **374** / `taskswarm` **0** 次月下载——**旁支里两个的下载量超过多数主样本**。

## 能借鉴什么(本域主产出)

> 这一节是本域**唯一以「拿走就能用」为目标**的部分。前面是诊断,这里是处方。每条都标了**借自谁、机制颗粒度、为什么有效、抄的时候注意什么**;代码级细节在 [02](./02-coordination-mechanisms.md) 与 [03](./03-sample-encyclopedia.md)。

### 十条可迁移做法

| # | 做法 | 借自 | 为什么有效(原理) | 抄的时候注意 |
|---|---|---|---|---|
| 1 | **「完成」判据必须看错误事件,不是只看没超时** | `dsh-remote-agent` | DSH 的 `kick()` 是 `try{while(await this.turn())}catch(_e){}`——turn 内错误被吞掉,只经 `agent/error` 露出。判据漏掉它,就会把传输失败标成 `completed`。**看不见的失败,才会报告成功。** | 加上 `hadError`;把 stderr 塞进结束事件;agent 分支在单测里跑不起来时,用**源码正则静态断言**钉死判据 |
| 2 | **消息 ack 放在「被 step 准入」那一刻,不是投递成功那一刻** | `dsh-agent-teams` | 投递成功 ≠ 被消费。三态 `claimedAt`(租约)→`deliveredAt`→`readAt` 把责任逐段收窄,丢消息时能定位到断在哪一段 | ack 必须挂 `agent/pre-step`;配套给消息带 `attemptId`,准入时过滤上一代 attempt 的指令 |
| 3 | **调度挂 `agent/status` 的 idle 边沿,锁内原子认领** | `dsh-agent-teams` | 宿主已经知道成员什么时候空下来;轮询是在重新发现一件已知的事 | 认领必须与状态检查在**同一把锁**内,否则两个成员会认领同一任务 |
| 4 | **任务板用 CAS(`expectedRevision`)+ tombstone 保 id** | 官方 `dsh-experimental-agent-team` | 陈旧调用方必须**失败**而不是覆盖;删除留墓碑,id 才不会复用后指错对象 | 官方也只在任务元数据上做了 CAS,**文件写入没有被保护**——别误以为任务 CAS 能防文件冲突 |
| 5 | **写权裁决落在 `tools/pre-execute` 的 `{kind:'deny'}`** | `Nwflower/dsh-file-claim` | 提示词里的写范围永远是建议:Bash、formatter、代码生成器都能绕。**只有让工具返回 deny 才真的拦住了写** | 认领边车与被保护文件同目录(无中央注册表);补 pid 判活 + TTL 兜底;但**必须自己加 epoch**,否则被接管方静默失锁 |
| 6 | **不可变快照 + 内容键缓存 → 卖「可复现」而不是「可续跑」** | `omdsh-dev/dsh_workflow` | 做不到断点续跑时,把 run 定义冻成不可变单元、整体重跑并按内容键回放结果,得到的是可复现。**两件事不能混着宣传** | 进程重启后活跃 run 会丢;多进程共用绝对 runDirectory 要加锁 |
| 7 | **第一次「要不要派活」的决策放进本来就要发生的那次推理** | `toolclub/dsh-agent-team-gui` | 任何 router agent 方案都要先花一次调用才知道该不该花;写进 systemPrompt 的 on-demand 段则零额外成本 | 这是**提示词引导,不是保证**——文档里别写成「绝对不会派活」 |
| 8 | **成本计量借宿主账本,0 样本返回 `undefined` 而不是 0** | `toolclub/dsh-agent-team-gui` | 自己另记一套账迟早与宿主对不上;把「没测到」写成 0 是最常见的假数据 | 读 `tokenUsage` 四桶 + 覆盖度 full/partial/none;覆盖度也要暴露给人看 |
| 9 | **跨机把「谁在执行」与「谁持有连接」解耦** | `zbzbhs/dsh-remote-agent` | 工作的所有者是副机,链路断了不丢工作;跨机于是从**传输问题**降级成**信任问题** | 副机要独立跑 DSH、独立管凭据;协议只传 `{provider,model}`,永不传 key |
| 10 | **恰好一次用文件系统原语,不用自研锁** | `IKEASven69/dsh-takeover` | `open(claim,'wx')` 的 `EEXIST` 是内核级互斥;配合 rename + 内容相同去重,单机与同步盘场景零基础设施即可成立 | 认领要 60s 清扫;同名归档内容不同时先写 `.conflict-HHMMSS[-n].md` 再 rename |

### 一条数据结构:四态证据账本

`IKEASven69/dsh-takeover` 的 `CURRENT_OBSERVED / HISTORY_REPORTED / MISMATCH / UNAVAILABLE` 是本域**最该被抄走的一个结构**。它的作用是给每一条事实标上「我是看到的,还是别人告诉我的」——接力过来的上下文永远标 `HISTORY_REPORTED`,原文按需分页拉取。

**任何跨边界传递信息的设计都该有这个字段**,因为跨边界之后你收到的都是「报告」,而不是「观察」。`dsh-teams-x` 的质量门与 `dsh-remote-agent` 的交接都缺这一层,于是成员的 `changedPaths` 自述被当成证据。

### 选型决策:按你缺哪笔税来挑,不按星标挑

```
成员要能被我追问 / 记住上一轮?
├── 要 → 必须可续子代理(dsh-experimental…/agent-teams 骨架)
│        接受 maxDepth 1、maxActiveSubagents 8(硬上限,超出直接 ACTIVATION_LIMIT_REACHED)
└── 不要,只扇出收结果 → 一次性子代理 + delivery:'caller',别建团队

每个成员要用不同的模型 / 权限 / 技能包?
├── 是 → 官方 roster 不够(它的 spawn_teammate 只带 name/description/prompt)
│        ├── 愿意放弃运行时 spawn/interrupt/wait → limuyang2 路线(成员=独立根 Agent)
│        └── 想保留子代理 → 只能自己扩官方能力,或等 preset 路线成熟(当前 persona 配置键已被宿主移除)
└── 否 → 官方 roster 够用,别自建

担心两个人改同一个文件?
├── 是 → 只有 tools/pre-execute 的 deny 真能拦(file-claim 路线),其余全是提示词
└── 否 → 别假装有隔离;老实写「共享 checkout」

要跨机,且不能被网络拖死?
├── 要 → 副机自主(remote-agent):副机本地跑完整 agent loop
└── 不介意延迟 / 只要异步 → 文件总线(takeover):没有协议,只有文件

要一条可复现的多 agent 流水线?
└── → 不可变胶囊快照 + 内容键缓存(dsh_workflow);话术是「重跑 + 回放」,不是断点续跑
```

### 动手之前必须回答的五个问题

写任何协作机制之前,先把这五个答案写下来。**答不出来的那一格,就是你会踩的坑。**

1. **权威状态在哪张纸上?** 另一份是审计,还是也是真相?两份都是真相 = 迟早失步。
2. **你的锁有 epoch / fencing token 吗?** 没有的话:被接管时,**原主怎么知道自己已经失去它?** 答不上来就是静默失锁。
3. **你的「完成」看的是哪个事件?** 那个事件真的能表示失败吗?如果只能表示「没超时」,它一定会产出假成功。
4. **进程重启后,在跑的协作变成什么?** 若答案是「全部 interrupted」,你只有持久记录,没有可恢复。
5. **你的消息有幂等键吗?** 没有幂等的重试通道,重投就是重复执行。

### 六条「别照抄」

这些是生态里**读起来很像能力、实际是空壳**的地方,本域已逐个核到源码:

| 别照抄 | 真相 | 出处 |
|---|---|---|
| 「原子认领」 | `limuyang2/agent-team` 之外,`dsh-expert-mode` 的 taskboard 是「读 → 校验 → 整份覆写」,全仓无 `flock`/`O_EXCL`/`temp+rename` | [10 expert-mode](./samples/10-Asher-2000-dsh-expert-mode.md) |
| schema 里的 `leases` / `dependencyIds` 字段 | 空壳:`leases` 只有 `{}` 清空赋值,`dependencyIds` 硬写 `[]` 且无 setter | [02](./02-coordination-mechanisms.md) §7 |
| 「可恢复」 | `dsh_workflow` 是快照重跑,`team-gui` 是重启全 interrupted——都不是断点续跑 | [02](./02-coordination-mechanisms.md) §3.3 |
| 「P2P 直连、零中转」 | 子代理只能被父唤醒;文件总线没有唤醒机制,所以投递仍要协调官再唤起一次 | [10 expert-mode](./samples/10-Asher-2000-dsh-expert-mode.md) |
| 「写范围 / 文件隔离」 | 官方 Team 的 writeScopes「never block anything」;除 `file-claim` 外无人真拦 | [01](./01-collab-topology.md) §3 |
| 静态 star 数当影响力 | 是滞后指标:`dsh-agent-teams` 两个半月从 573★ 涨到 2592★;本域影响力一律标采样日 | [样本索引](./03-sample-encyclopedia.md) §2 |

## 边界契约(声明式,不依赖他域进度)

四域并行研究时,**归属是事先划定的,不是商量出来的**。本域遇到下列情形只写划给自己的那一半,另一半留给它的归属域;若那一边尚未产出,本域照写,不等待、不代笔。

| 情形 | 归属 | 本域只写到哪 |
|---|---|---|
| 跨机传输的**鉴权、配对、凭据** | `lever-draw-limit` | 只写「这道边界多付一笔信任成本」,具体鉴权机制不写 |
| 成员任务的**完成标准与验收退回** | `lever-prove-output` | 只写「状态归谁」,不写「凭什么算完成」 |
| 远端工作区的**沙箱是否仍生效** | 本域(作为边界代价) | 只写「协作边界的特有代价」;策略词汇与其强制点归 `lever-draw-limit` |
| A2A / 网络的**发现** | 本域 | 付费限额的**强制**归 `lever-draw-limit` |
| 团队面板的**槽位与布局** | `lever-reshape-product` | 只写它是否承载状态 |

**契约的两条硬约束**:① 本域结论不得把其他域的结论当作前提;② 需要外部事实时写进本域卡片并自带 `[DSH]`/`[CAT]`,不写「见某域」。

## 本域基线(冻结)

> 快照 **2026-10-31** · 名单 @ `efe602e7b` · DSH `0.2.1-rc.3`。**本域只引用这份快照读到的事实,不维护统计口径。**

四域重叠是正常的:本域与 RESHAPE / PROVE / LIMIT 都有样本交集。四域是**四个并列的提问**,不是互斥分类——独立性靠「编辑权 + 主读归属 + 不依赖他域结论」保证,不靠样本不重叠。

## 复核方式

**不设计数门。** 影响力看 2026-10-31 的实时 stars/fork/npm(连 GitHub API 与 npm registry 现拉,标注日期);`data/stars.json` 只是 2026-08-19 的旧快照,只能用来算涨幅。**「少见 / 唯一」是人工回读判断,标 `[OBS]`,不附命中数。**

## 复核触发条件

- `dsh-subagent` 的 `maxDepth`(默认 1)、`maxActiveSubagents`(默认 8,不排队)语义变化
- 子代理的最终文本变得可程序化读取(这会直接抽掉「成员必须可续」的理由)
- 任一头部样本(`dsh-agent-teams` / `team-gui` / `dsh_workflow`)补上 worktree 隔离或跨进程状态
- `dsh-experimental-agent-team` 从实验升为稳定,或它补上 worktree / 跨进程 mailbox
- `dsh-api-remote-access` 的 principal 种类或 policy 模型变化
- worktree 从 `experimental` 转正

## 待答问题

**已答**(答案落在卡片里,不再挂着):

- [x] 官方边界 2 的限制到底几条、原话是什么 → **7 条**,其中 3 条正是三笔税;「no cross-process mailbox」不在限制清单里,是 Dev Note 的未定方向 → [01](./01-collab-topology.md) §3
- [x] 生态插件是在填官方的坑,还是另起一套 → **另起一套**;唯一真补了冲突裁决的是 `file-claim`,且它没有成员模型 → [01](./01-collab-topology.md) §3 / [02](./02-coordination-mechanisms.md) §4
- [x] 跨机里谁做到了**副机自主运行** → `zbzbhs/dsh-remote-agent`(副机本地跑完整 DSH,断链继续)是唯一明确样本;`dsh-takeover` 走文件总线另一条路 → [06](./samples/06-zbzbhs-dsh-remote-agent.md) / [09](./samples/09-IKEASven69-dsh-takeover.md)
- [x] 成员必须可续聊吗 → **必须,且原因是宿主的**:子代理最终文本不可程序化读取,所以需要追问的队长必须让成员活着 → [样本索引](./03-sample-encyclopedia.md) §5 结论①

**待答**:

- [ ] 边界 2 的“单进程共享 checkout”是短期实验约束还是设计立场？若长期成立，所有团队插件都要自带 worktree。
- [ ] 45 条 worktree 样本里,有多少是“每个成员一个 worktree”,多少只是“任务级快照”？(`dsh-taskswarm` 是前者的候选,尚未盘点全量)
- [ ] `Asher-2000/dsh-expert-mode` 的 preset 路线(17 个静态工具行 + 文件黑板)能否长大成第三条主流？它只缺运行时增删成员与任务板。
- [ ] 为什么没人给自己的租约加 **epoch/fencing**？是成本问题,还是宿主只给了 `tools/pre-execute` 一个可绕过的写面钩子。
