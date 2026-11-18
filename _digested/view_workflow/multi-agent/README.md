# multi-agent — 多智能体编排

> 多个 agent 分工、共享任务板、按角色协作。

## 定义

插件提供多智能体的结构:团队、任务板、角色划分、仲裁。判定标准:存在"不止一个 agent"的实体与状态。

## 成员(人工确认)

| 条目 | 星标 ⚠ | 说明 |
|------|--------|------|
| NanmiCoder/dsh-agent-teams | 573 | 队长=当前会话,成员=宿主 continuable subagent,任务板=工作区 `.agent-teams/<teamId>/team.json`;6 条真衍生/硬依赖([01](01-agent-teams.md) ★★★) |
| toolclub/dsh-agent-team-gui | 84 | 小队=Settings 里的持久数据;派工按有界 DAG,Run Center 逐成员 token;peer 钉 0.1.5.x,0.2.x 需改造;0 扩散([04](04-agent-team-gui.md) ★★★) |
| omdsh-dev/dsh_workflow | 82 | workflow 不是 DAG:QuickJS capsule + 内容寻址 effect cache 回放续跑;main 停 0.1.2,0.2.x 只读路径 fail-closed([03](03-dsh-workflow.md) ★★★) |
| whyihaveyou/dsh-suite#plugin-team-board | 42 | Cordis service key 上的共享任务板 |
| shengsheng90/DSH-taskboard | 40 | SQLite 单一权威 + 8 个 `taskboard_*` 窄工具(无 accept),验收权在人手里;真衍生 0([02](02-dsh-taskboard.md) ★★★) |

## 立卡条件

≥500 星,或被 ≥5 个条目引用其任务板协议。

> 本轮:agent-teams 573 达标;taskboard 40、dsh_workflow 82、agent-team-gui 84 均未达,按"四种状态权威 + 四种失败收敛的机制样本"破例。门槛未变。

## 生长

这是 workflow 里**最可能长出标准协议**的分支(任务板 = 共享状态接口)。写卡时重点看:状态存在哪、冲突怎么裁决、失败怎么收敛——这正是 `_leverage/leverage-agent-collaboration` 的证据面。

**四张卡给出的答案:四种状态权威,没有一种变成协议。**

- **agent-teams**:队长就是当前会话(不新增实体),成员是宿主自己的 continuable subagent;状态写在 `<workspace>/.agent-teams/<teamId>/{team.json,inbox/*.jsonl}`。冲突裁决只有**进程内**一把 promise 队列加单调 `attemptId` 代次令牌,没有文件锁、没有 revision 比较——多个进程同时驱动时后写者静默覆盖。
- **taskboard**:状态压进一个 SQLite 文件,并发靠"单写者 `BEGIN IMMEDIATE` + `expected_version` CAS + 唯一部分索引"三层;模型只有 8 个 `taskboard_*` 工具,**没有 accept**,`accept()` 首行 `requireHuman`。它的 workflow 18 种节点全是 design-only,真正执行的是定时认领器。
- **dsh_workflow**:workflow 不是图,是一段 QuickJS 里的 `async function run(wf, args)` + capsule;节点是运行时 `wf.runAgent/spawnAgent` 调出来的 `task-N`,执行者是 DSH 原生 subagent。**没有检查点**:`resume` 是按 `sha256(manifest+source+runtime+路由+输入)` 回放已完成且无警告的 task 结果——幂等的是单个 task 的成功效果,不是整条 run 的决策路径。main 停在 0.1.2(而 tag 到 0.1.4),0.2.x 的 `SubagentCapabilities` 已无 `toolFilter`,只读路径会在第一个子 agent 前 fail-closed。
- **agent-team-gui**:小队是 Settings 里的持久数据(逐成员模型/工具策略),从 Composer 选择;派工按有界 DAG,审核/返工与 Run Center 是 UI 资产。**团队不是别人能接过去的协议**;21 个 peer 全钉 `>=0.1.5-rc.1 <0.1.6-0`,而 0.2.x 已把 `toolFilter`/`persona` 换成 `agentPreset`,跟代是它最硬的成本。

**判断**:本分支的"标准"目前只到"人保留验收权"这一条心智模型;四张卡都没有被第三方复用为协议。真正的收敛信号应是第三方复用同一份 schema、同一个存储布局或同一套调度语义——现在一个都没有。把"任务板/工作流协议正在形成"读成事实,会高估。
