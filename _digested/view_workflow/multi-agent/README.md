# multi-agent — 多智能体编排

> 多个 agent 分工、共享任务板、按角色协作。

## 定义

插件提供多智能体的结构:团队、任务板、角色划分、仲裁。判定标准:存在"不止一个 agent"的实体与状态。

## 成员(人工确认)

| 条目 | 星标 ⚠ | 说明 |
|------|--------|------|
| NanmiCoder/dsh-agent-teams | 573 | 队长=当前会话,成员=宿主 continuable subagent,任务板=工作区 `.agent-teams/<teamId>/team.json`;6 条真衍生/硬依赖([01](01-agent-teams.md) ★★★) |
| toolclub/dsh-agent-team-gui | 84 | 持久多模型小队,设置中选择,Composer 中调用 |
| omdsh-dev/dsh_workflow | 82 | 可生成/保存/治理/观测/恢复的多 agent 编排 |
| whyihaveyou/dsh-suite#plugin-team-board | 42 | Cordis service key 上的共享任务板 |
| shengsheng90/DSH-taskboard | 40 | SQLite 单一权威 + 8 个 `taskboard_*` 窄工具(无 accept),验收权在人手里;真衍生 0([02](02-dsh-taskboard.md) ★★★) |

## 立卡条件

≥500 星,或被 ≥5 个条目引用其任务板协议。

> 本轮:agent-teams 573 达标;taskboard 40 星、真衍生 0,按"状态权威 + 人验收闸的机制样本"破例。门槛未变。

## 生长

这是 workflow 里**最可能长出标准协议**的分支(任务板 = 共享状态接口)。写卡时重点看:状态存在哪、冲突怎么裁决、失败怎么收敛——这正是 `_leverage/leverage-agent-collaboration` 的证据面。

**两张卡给出的答案:收敛发生在命名与一条不变量上,不在协议上。**

- **agent-teams** 的队长就是当前会话(不新增实体),成员是宿主自己的 continuable subagent;状态写在 `<workspace>/.agent-teams/<teamId>/{team.json,inbox/*.jsonl}`。冲突裁决只有**进程内**一把 promise 队列加单调 `attemptId` 代次令牌,没有文件锁、没有 revision 比较——多个进程同时驱动时后写者静默覆盖。
- **taskboard** 把状态压进一个 SQLite 文件,并发靠"单写者 `BEGIN IMMEDIATE` + `expected_version` CAS + 唯一部分索引"三层;模型只有 8 个 `taskboard_*` 工具,**没有 accept**,`accept()` 首行 `requireHuman`,自我验收在代码层不可能。它的 workflow 18 种节点全是 design-only,真正执行的是定时认领器(claim 一个 todo → 起真 Agent → 完成只到 `in_review`)。
- 两者都没有被第三方复用为协议:taskboard 的 11 条同 token 条目里真衍生为 **0**(3 条独立实现只在 `taskboard_*` 前缀与"agent 不能做人验收的那一步"上趋同,列数、存储、驱动方式全不同);agent-teams 的 6 条衍生接的是**配置行与团队文件**,不是调度协议。

**判断**:本分支的"标准"目前只到"人保留验收权"这一条心智模型;把它读成"任务板协议正在形成"会高估。真正的收敛信号应是第三方复用同一份 schema 或同一个存储布局——现在一个都没有。
