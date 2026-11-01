---
title: "拓扑谱：四道边界与它们各自的税"
domain: agent-coordination
kind: playbook
positioning: "协作域的第一张卡：用「跨了哪道边界」给任何协作插件定位，并列出每道边界的税。"
takeaway: "四道边界 + 三笔税；生态不是填坑，是换一张表重画。"
read_when: "判断一个协作插件属于哪类；或写多 agent 功能前先确认它会碰上哪笔税。"
status: observed
updated: 2026-10-31
---
# 01 · 拓扑谱：四道边界与它们各自的税

> **状态**:`observed` · **基线**:DSH `0.2.1-rc.3` · 名单 @ `efe602e7b` · **样本**:9 组深读 + 5 组旁支,回读仓库源码
> **一句话**:从“一个 agent”到“一支团队”要跨四道边界。**每跨一道，新增的不是能力，而是三笔税：状态归属、冲突裁决、失败收敛。**

> **2026-10-31 修订**:官方「已知限制」按原话逐字核对(7 条,不是 4 条);子代理深度/容量/权限三条税补上源码行号;影响力口径从「目录自述」改为「实时 GitHub + npm 数据 + census 探针」;新增失败模式「假成功 / 重启归零 / 静默失锁」。样本深读见 [02](02-mechanisms.md) 与 [03](../encyclopedia.md)。

## 1. 命题

> 协作的难点不在派活，在**状态放在哪一层、失败在哪一层收敛**。官方在边界 2（同工作区多成员）留下的 7 条已知限制里最要命的三条——共享 checkout、单进程、owner 不自动释放——是生态插件真正在赛跑的对象；但生态的选择不是「填坑」，而是**换一张表重画**：谁要成员异构配置，谁就必须自己造 roster。

可证伪点：如果存在一批插件**根本不需要回答状态归属**就实现了稳定协作，命题不成立。

## 2. 杠杆点

| 边界 | 跨越的东西 | 阶梯级 | 供给(证据) |
|---|---|---|---|
| 0 同 agent | 无 | — | 全部 |
| 1 同进程父子 | 上下文 + 结果 | 5(seam backend)+6(preset) | `subagent` 259 条、`子代理` 189 条 `[CAT]` |
| 2 同工作区多成员 | 文件 + 任务 + 消息 | 6(bundle) | `team` 102 条、`团队` 59 条、`captain` 5 条 `[CAT]` |
| 3 跨进程/跨机 | 身份 + 传输 + 信任 | 7(protocol) | `relay` 81 条、`handoff` 73 条、`worktree` 45 条、`mailbox` 8 条 `[CAT]` |

> 检索式:(2026-10-31 冻结基线,单标、描述原文命中)。旧稿的「`subagent` 文件名 49 条 / `team` 36 条 / `remote` 62 条」是文件名口径,与本表描述口径不可比,已整表替换。

**关键不对称**:边界 1 是 DSH **免费给的**（一个 config 就开）；边界 2 官方只给实验原型且写明三条硬限制；边界 3 官方只给**协议原语**（网关、ACP、worktree），不给你任何现成的“跨机团队”。

## 3. 机制：每一道边界收什么税

### 边界 1 · 同进程父子 `[DSH]`

**白送的东西**:挂上 `dsh-subagent` + 一个 provider + 一个工具行，agent 就能委派。本地 spawn/fork **保留持久会话，可继续**；ACP / DSH SDK / Codex / Claude Code 是**一次性**执行，只暴露一次，拒绝继续输入。

**三道暗税**:

| 税 | 具体 | 出处 |
|---|---|---|
| 深度 | `maxDepth` 默认 **1**——只有直接子代理，子代理不能再雇人。深度以父 session header 为**单调下限**,被 resume 的子代理不能从零重新计深度 | `dsh-subagent` README:49;`lib/index.js:104-116` |
| 容量 | `maxActiveSubagents` 默认 **8**，每棵 activation 树共享;根父不占槽;创建与冷恢复**先预留再物化**;**耗尽不排队**,直接 `ACTIVATION_LIMIT_REACHED`(浏览器侧转 `subagent/delivery-unavailable`) | `dsh-subagent` README:53/57;`lib/index.js:1047` |
| 权限 | 子代理的权限范围**在启动时固定，会话内不能扩大**;`approval` 被钉为 `never`——需要审批的操作**自动拒绝**是机制强制,不只是提示词 | `dsh-subagent` README:181;`lib/index.js:363,400-414` |

容量不排队这一条值得单独说：官方给的理由是「**Admission does not queue, because a parent waiting for descendants must not wait for its own occupied slot.**」这是一个**死锁规避**设计，代价是**父代理必须自己实现重试与排队**——生态里那一批“模型路由 / 名额监控”插件，本质上都是在补这层调度。

“可续”也不是容器属性而是**后端能力**:只有当 provider 暴露 `prepareContinuable` 时,`startActivation` 才接受保留的 `childId`,`dsh-subagent` 直接抛 `UNSUPPORTED_CAPABILITY`(“reserved child ids require a local backend”)。ACP / DSH SDK / Codex / Claude Code 这类进程外 provider 因此只有一次性执行,`interrupt_agent` 的描述逐字写着「External executions stop permanently and cannot receive follow-ups」。

**结果怎么回**:`delivery: 'parent'` 在**结算之后**发一条 user-role 完成通知（含子代理非空最终文本块与 `Structured result:` 结构化输出块,reasoning 与非文本块被排除）；`delivery: 'caller'` 不发通知，由工作流 await 收集。**父代理看到的是子代理的最终文本，不是过程**——正因为过程不可读,dsh-agent-teams 才要求成员把报告**写进队长的邮箱与任务记录**,而不是靠“读子代理最后一句话”。

### 边界 2 · 同工作区多成员 `[DSH]`

官方 `dsh-experimental-agent-team` 给了 roster + inbox + 持久任务板。它的设计理念是三条：“持久日志、派生状态”“进程内归属”“显式权限”。

**它的「已知限制」一共 7 条**(README:203-207，逐字核对过)，其中**三条正好是边界 2 的三笔税**:

| 官方原话(逐字) | 中译 | 这意味着什么 |
|---|---|---|
| **One process and one shared checkout** — members share cwd and observe edits immediately; this package provides no worktree, remote member, merge, or filesystem lock. | 一个进程、一个共享 checkout——成员共享 cwd 并即时看到彼此的修改;本包不提供 worktree、远端成员、合并或文件系统锁 | 文件冲突**没有任何机制裁决**;冲突裁决这一笔税原样留给生态 |
| **Advisory write scopes** — Bash, formatters, code generators, and direct external writers can bypass filesystem version checks. | 写范围只是建议性的——Bash、格式化器、代码生成器以及直接的外部写入者可以绕过文件版本检查 | 唯一的写范围声明是**建议，不是强制** |
| **No automatic ownership release** — inactivity, interruption, process exit, and failed work do not release a task owner. | 没有自动的归属释放——不活跃、被中断、进程退出与失败的工作都不会释放任务归属 | 任务卡住后**无人回收**,失败收敛这一笔税留给生态 |
| **No send retry guarantee** — Team does not retain or deduplicate new attempts; **concurrent processes over one Team are unsupported**. | 无发送重试保证——不保留也不去重新尝试;同一个 Team 上的并发进程不被支持 | 消息可能静默丢失;状态归属锁死在单进程 |

> **勘误**:旧稿把「no cross-process mailbox」当成官方的一条限制,这不准确。官方把 `cross-process mailbox transactions` 写在 Dev Note 的**未定方向**里(README:223,且该段自述 non-authoritative),限制清单里对应的事实是「concurrent processes over one Team are unsupported」。写引用时两者不能合并成一条 README 限制。

同时它给了两件很硬的东西：任务用**完整版本快照 + `expectedRevision`**，陈旧调用方拿 `TEAM_TASK_STALE_REVISION` 而不是覆盖；已删除任务保留 tombstone 维持 id 稳定(`get()` 仍返回墓碑,`list()` 与 `maxTasks` 不数它),id 空间耗尽报 `TEAM_TASK_LIMIT` 而不是复用末号。这是 CAS 的教科书实现。

**所以边界 2 的真实图景**:官方把**协作元数据**做得很硬（CAS、日志派生、tombstone 保 id），把**工作区与生命周期**留成空白。生态插件的分工因此非常清楚——

- 一拨人补**文件隔离**:`worktree` 45 条样本（`february2015/dsh-taskswarm` 等）
- 一拨人补**调度与回收**:`team` 102 条、`captain` 5 条
- 一拨人干脆**绕过官方团队**,自己实现 roster——但“补上空白”这个说法需要修正:**三家都没有真去填官方那三条限制的坑,而是各自重画了一张表**

| 自建 roster 的样本 | 它真正补的是什么 | 它没补什么 |
|---|---|---|
| `NanmiCoder/dsh-agent-teams` | 事件驱动调度器(idle 边沿原子认领)+ 队长/成员双向邮箱 + 批准后才派工的两段式 + 可选质量门 | 文件隔离(作者明说不做 worktree,只在完成时审计 `changedPaths`);跨进程(锁是进程内 promise 链) |
| `Mlte0907/dsh-teams-x` | 同一套骨架的轻量版:DAG + 磁盘 JSONL 信箱 + 质量门自动派生 repair(上限 3 轮) | 同上;且质量门的 `commandsRun`/`changedPaths` 是成员**自述**,插件不执行 verify 命令 |
| `limuyang2/agent-team` | 成员异构配置(每人独立 provider/model/preset/权限/Skills/MCP) | 依赖图(`dependencyIds` 硬写 `[]`)、租约(`leases` 表存在但无代码)、文件裁决(`fileScopes` 只是文案) |

这三家重画 roster 的真实原因不是「官方 roster 扁平不可变」这一条,而是**官方 roster 的成员不可配置**:官方 `spawn_teammate` 只带 name/description/prompt,不给每个成员单独的模型、预设、权限与技能包。`limuyang2/agent-team` 是最直接的证据——它为了「一个成员一套异构配置」,宁可放弃运行时 spawn/interrupt/wait/DAG,把成员改成**独立根 Agent**而不是子代理。谁要成员异构,谁就得自己造 roster。

### 边界 3 · 跨进程 / 跨机 `[DSH]`

官方给的是**原语，不是产品**：

| 原语 | 它做什么 | 它不做什么 |
|---|---|---|
| `dsh-api-gateway` + `dsh-api-remote-access` | 带类型的 Client↔Host RPC，每次调用**必填 Peer**，非 owner principal 按 role/resource 判定 | 不做传输、不做服务发现 |
| `dsh-acp` | 受信程序用标准 ACP **自动操作持久 agent**：建/恢复会话、选模型、挂 MCP、提交或取消工作 | 不支持删除、fork、transcript 回放、附加目录 |
| `dsh-experimental-worktree` | 从本地提交建**具名分支 + 隔离检出目录**，同一 Session 继续 | 不复制暂存/未暂存/未跟踪/被忽略文件;不提供合并 |

**worktree 的关键细节** `[DSH]`:所有写入仍受现有沙箱约束，创建操作**不会扩大**目标目录或共享 Git 管理目录的写权限。这是边界 3 最重要的一条设计——**隔离不等于放权**。

### 边界 3 的两种流派 `[CAT]`

生态在跨机上分成了方向相反的两种做法：

**A. 镜像流派**——把远端文件当本地文件用。`januory/dsh-remote-workspaces` 明说“不做本地镜像……本地沙箱策略依然生效”；`MingTXin/dsh-remote-workstation` 走 SFTP 挂载，远端 watch 用轮询。共同点是**agent 用同一套工具**，不新增模型工具。

**B. 代理流派**——远端跑完整 agent。`zbzbhs/dsh-remote-agent` 把另一台电脑变成“远程 Agent 同事”：**副机本地跑自己的 DSH 与完整 Agent 循环**，链路断开任务照常继续，模型凭证永不离开那台机器；主机只收回 handoff 摘要与产物清单。`ANetResearch/ANet#dsh-anet` 通过 stdio MCP 接本地 anet 节点，做端到端加密的 A2A 任务与**付费/拒付**。

**B 流派的洞察**:它把“跨机”从**传输问题**降级为**信任问题**。链路断了不会丢工作，因为工作的所有者本来就是副机。代价是副机要独立运行 DSH、独立管凭据。

### 边界 3 的第三形态:接力 `[CAT]`

`IKEASven69/dsh-takeover` 提供 `handoff: 1` 协议：会话卡片**消费即弃**，四态证据账本，补丁随卡走，**用同步盘做跨机接力**，投递失败自动退回复制指令。

这是最朴素也最省事的跨机方案——**没有网络协议,只有文件**。它之所以可行，是因为它把协作状态（卡片 + 账本）做成了**可序列化的自包含单元**。

## 4. 旁支：子代理路由不是协作

生态里最大的一坨 `subagent-*`（文件名 49 条）做的其实是**模型路由**:把某个委派任务改写到另一个 provider/model。它们都挂在 `agent/request` 钩子或包装 provider 上 `[CAT]`，例如：

- `Garybot126/dsh-subagent-models`：经 `agent/request` 钩子对每个进程内子代理生效，**不注册设置页、不改 agent preset、不给工具加模型参数**
- `tkaiz0406/dsh-subagent-route-pin`：注册包装 provider，单发子代理走 `provider.start`，Agent Teams 成员走 `startActivation` 上的钩子

**这一类的价值在杠杆位置，不在协作**:它们证明 `agent/request` 是一条**能在不改任何 preset 的前提下改变委派行为**的缝。属 4 级（policy），不是边界跨越。本卡只做归类，细节留给后续小卡。

## 5. 标杆

**配额**:本卡只深读 **1 个主标杆 + 2 个对照**。其余 S/A 级样本见本域 [`README.md`](../00-map.md#4-现有样本的主家族)。

### 主标杆 · 官方 `dsh-experimental-agent-team`(S 级,不是生态条目)

| 必答项 | 内容 |
|---|---|
| **代表什么典型** | 边界 2(同工作区多成员)的**唯一原生原型**;它的 7 条已知限制(其中 3 条正是三笔税)定义了这一整道边界的税 |
| **为什么选它** | 过 **G 已核**:机制读自官方 README,且能点出它的失效条件——共享 checkout、单进程、owner 不自动释放、消息无去重重试 |
| **影响力多大** | 不是「被多少人用」,而是**它规定了别人的形状**:生态里 `teams-x`、`eteams`、`agent-team` 三家的 roster 语义都在跟它划分界线 `[CAT]` |
| **主要特点** | 协作元数据做得很硬(CAS + `expectedRevision` → `TEAM_TASK_STALE_REVISION`,tombstone 保 id 稳定),工作区与生命周期留给外面 |
| **代价 / 失效** | 文件冲突**无任何裁决**;`writeScopes` 只是提示(Bash/formatter 可绕过);任务卡住只能 Lead 手动回收 |
| **证据级别** | `[DSH]` 官方包 README「已知限制」段 · 状态 `observed` |

### 对照 · 本域其余样本(只给定位,深读见 [03](../encyclopedia.md))

| 样本 | 边界 | 它解决的税 | 一句话 |
|---|---|---|---|
| `NanmiCoder/dsh-agent-teams` | 1+2 | 状态归属 + 失败收敛 | 成员是**可续聊子代理**,权威状态在磁盘 `team.json`,靠 idle 边沿认领任务 |
| `toolclub/dsh-agent-team-gui` | 1+2 | 状态归属 + 成本 | 「默认不派活」写在**提示词**里而不是代码里 |
| `omdsh-dev/dsh_workflow` | 1 | 失败收敛 | 没有 DAG,JS 控制流就是编排;可恢复 = 快照重跑 + 内容键缓存 |
| `limuyang2/agent-team` | 2 | 成员异构 | 成员是**独立根 Agent**,不是子代理 |
| `Mlte0907/dsh-teams-x` | 1+2 | 三笔都试了一遍 | 与官方最要命的三条限制逐条应战,但两条承认未解决 |
| `zbzbhs/dsh-remote-agent` | 3 | 信任 | 把跨机从传输问题降级为信任问题 |
| `Nwflower/dsh-file-claim` | 2 | 冲突裁决 | 唯一真去做**文件写权**裁决的样本 |
| `Chinesezjc/dsh-interconnect` | 3 | 状态归属 | 跨 DSH **实例**的消息总线,无幂等、无离线队列 |
| `IKEASven69/dsh-takeover` | 3 | 冲突裁决 + 收敛 | 没有网络协议,只有文件 |

> 旁支留档(B 级,不立卡):`february2015/dsh-taskswarm`(worktree 补共享 checkout 的空)、`januory/dsh-remote-workspaces`(SSH/SFTP 不镜像)、`ANetResearch/ANet#dsh-anet`(加密 A2A + 限额付费)、`PerryLink/dsh-team-rooms`(跨会话团队房间)、`Noelune/dsh-agent-relay`(HMAC broker 中继)只出现在本节与失败模式表,各有独立卡片供给时再升。

## 6. 体验

**人看到的**:边界 1 是“子代理下拉框”;边界 2 是侧栏里的成员与任务板;边界 3 是**二维码、配对码、设备列表**——跨机协作的第一次体验几乎全是配对流程,不是协作本身。

**模型看到的**:这一层的不对称最值得记。

- 子代理在自己的运行时上下文里收到一条固定声明:**权限范围启动时已固定、需要审批的操作自动拒绝、不要重试被拒操作** `[DSH]`
- 父代理只收到**完成通知**（最终文本 + 可选结构化输出块），看不到子代理的过程
- 团队成员之间的 peer 消息是**user-role 消息**,但两套原语的措辞不同:Agent Teams 用 `Team message from <name>:`,子代理用 `Agent <senderSessionId> sent a message:`(是 id,不是名字) `[DSH]`
- roster 与任务板**不进模型历史，只进日志**;模型对团队的认知来自工具返回值,不来自“看见一支队伍” `[DSH]`

**而消息头不是身份。** 官方把话说得很直:`dsh-tool-subagent-control` 描述「**the service derives that attribution and never treats it as authority**」,`dsh-subagent` 说「**Agent-message authority is exact adjacency**」,Agent Teams 侧同构地写着「Sibling messages never impersonate the Lead through the public adjacent-Agent messaging operation」。也就是说:**agent 之间的身份来自日志里的 `source.senderSessionId` + 相邻性检查,不来自消息文本**。控制面工具连“冒充他人发送”的参数面都不存在——它把确切的活动调用 agent(`exec.agent`)同时作为 sender 与 authority 传入。

**所以“团队”对模型而言是**:我不能扩权、我看不到同伴的过程、我收到的每条同伴消息都长得像用户说话、而且我说我是谁不算数。任何把团队当“共享大脑”的设计，都在这四条上撞墙。

> **另有两条容易被误解** `[DSH]`:① `subagent` 与 Agent Teams 是**两套并存的协作原语**,`agent-team-profile` 打包时**显式禁用**了 `tool-subagent` / `tool-subagent-fork` / `tool-subagent-control` / `tool-subagent-list-agents`——「装了 Teams 就同时有子代理委派」是错的。② 子代理服务**没有持久的父信箱**(“The service has no durable parent mailbox”),驻留是进程本地的;`listChildren` 不读子日志,只是父拥有的投影,所以是 O(D) 而不是可持久查询的目录。

## 7. 失败模式

| 失败 | 表现 | 根因 | 谁踩过 |
|---|---|---|---|
| 静默丢消息 | Lead 以为发了,成员没收到 | 官方 Team「无发送重试保证、不去重」 | 官方;`teams-x` 补 60s 投递租约 + release 重试,但仍无 message-id 幂等 |
| 任务永挂 | 成员死了,任务还在 in-progress | 「不会自动释放 owner」 | 官方;`agent-teams` 用 parked 语义**刻意**保留停驻,只给一次冷恢复 |
| 同时改同一文件 | 后写的覆盖先写的,无人察觉 | 共享 checkout + write scope 仅提示 | 除 `file-claim` 外**全员**;`agent-teams` 只在完成时审计 `changedPaths` |
| 深度不够 | 子代理想再雇人,失败 | `maxDepth` 默认 1 | 所有两层 roster |
| 全家卡死 | 一棵树 8 个名额占满,所有新委派被拒 | 容量不排队设计 | `agent-teams`(默认成员 8)/ `team-gui`(成员 32) |
| 跨机断链丢工 | 链路一断整批工作失效 | 镜像流派把工作绑在链路上 | 镜像流派;代理流派不受影响 |
| 配对疲劳 | 每个插件一套扫码/配对/令牌 | 边界 3 没有统一的身份层 | 生态普遍;`remote-agent` 的配对码**不过期、不核验**,只是配置打包串 |
| **假成功** | 任务标 completed,实际什么都没产出 | 完成判据缺项:DSH 的 `kick()` 把 turn 内错误吞掉只走 `agent/error`,判据只看超时与中断 | `remote-agent`(已修,并用源码静态断言钉住三条) |
| **重启归零** | 进程一重启,在跑的团队全标 interrupted,进度清零 | 无执行级检查点 | `team-gui`(明说无自动续跑);`dsh_workflow`(进程重启活跃 run 丢失) |
| **静默失锁** | 租约被接管,原主以为自己还持有 | 无 fencing token,原主 `sync` 时 `mine=[]` 也不报错 | `file-claim` |

## 8. 评估清单

1. 它跨的是哪一道边界?说不出边界的,是不是只是个工具?
2. roster / 任务 / 消息 / 证据分别存在哪里?谁是权威日志——**会话日志,还是它自己写的一份盘上状态**?
3. 它怎么处理官方限制里最要命的那三条(共享 checkout / 单进程 / owner 不释放)——绕过、补上,还是假装不存在?补的那条**有没有留下新的空白**?
4. 成员崩溃、消息丢失、链路断开时,协作状态往哪收敛?收敛靠**心跳、对账器、还是人的手动操作**?
5. 跨机方案里,工作和链路是**绑定**还是**解耦**?断链后还能继续吗?
6. 它有没有把协作状态做成可序列化的自包含单元(卡片/账本/快照)?
7. 模型侧看到了什么?roster 与任务板进了上下文,还是只进了日志?
8. **它的“完成”判据是什么?** 是子代理自述、还是自己有独立证据?自述的判据一定会产生假成功。

## 9. 开放问题

- [ ] `[OPEN]` 官方“单进程共享 checkout”是实验期约束还是立场?若长期成立,worktree 就是团队插件的必需品而非可选。
- [ ] `[OPEN]` 两套 roster（官方 Team vs 自建 team）会不会导致一个会话里出现两个“团队”概念?`limuyang2/agent-team` 与官方包服务键只差一个字母(`agentTeam` vs `agentTeams`),两者可同装,任务板互不相通。
- [ ] `[OPEN]` 边界 3 缺少统一身份层,是否意味着长期只能是“每插件一套配对”?DSH 原生 Peer 模型能否被复用成统一身份?
- [ ] `[OPEN]` 代理流派（副机自主）与镜像流派（本地映射）会长期并存,还是其中一个会赢?
- [ ] `[OPEN]` **磁盘上的 team.json 会不会成为事实上的标准?** 三家自建 roster 都在 `<workspace>/.<plugin>/<teamId>/` 下写自己的状态,彼此不可读。若没有共享 schema,团队状态就无法跨插件迁移。

---

## 证据与边界

> 核对时点 2026-11-01；宿主固定为本机 `@deepseek-ai/dsh@0.2.1-rc.3` 安装树。下列路径均相对该安装树的 `node_modules/@deepseek-ai/`。

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| `maxDepth` 默认 1，只允许直接子代理 | `[SRC-DSH]` | `dsh-subagent/lib/index.js:2979`（zod `.default(1)`）；README:49 | 只对通过该设置继承深度的工具生效；显式 depth 可覆盖 |
| `maxActiveSubagents` 默认 8，根父不占槽、先预留再物化、耗尽不排队 | `[SRC-DSH]` | `dsh-subagent/lib/index.js:2980`（`.default(8)`）；README:53/55 | 每棵 activation 树独立计额；调低不杀已驻留子代理 |
| 子代理权限启动时固定、需审批的操作自动拒绝 | `[DOC]` | `dsh-subagent/README.md:181,186`（注入的运行上下文声明） | 未在真实审批场景实测；机制强制点未逐行核 |
| 子代理服务没有持久父信箱；父不在时消息被拒 | `[SRC-DSH]`/`[DOC]` | `dsh-subagent/README.md:207,212` | 只覆盖 in-process continuable child；外部 provider 不适用 |
| Agent Team 是并存原语，profile 显式禁用四个 subagent 工具 | `[SRC-DSH]` | `dsh-experimental-agent-team-profile/cordis.patch.yml:4-14`（精确 id：`tool-subagent-control`、`tool-subagent-list-agents`、`tool-subagent`、`tool-subagent-fork`） | 只证明该 profile 的打包行；不证明装了 Teams 后运行时一定互斥 |
| 目录检索 259 条 `subagent` / 189 条 `子代理` | `[OBS]` | 2026-10-31 目录快照，检索式见本章开头 | 计数随目录增长漂移，不是产品事实 |
| ACP/SDK/Codex/Claude Code 等外部 provider 只支持一次性执行 | `[DOC]` | 本章原文引 `interrupt_agent` 描述；未逐包核 | 具体 provider 能力可能随版本变化，运行前需重核 |

**未验证**：`approval` 被钉为 `never` 的代码路径、外部 provider 的实际中断语义、Teams 与 subagent 在同一 profile 共存时的运行时行为，均标 `[OPEN]`，不作为工程保证引用。
