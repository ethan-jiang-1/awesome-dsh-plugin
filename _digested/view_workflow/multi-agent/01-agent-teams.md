# agent-teams — 队长就是当前会话，成员是宿主自己的 continuable subagent，任务板是磁盘上的 `team.json`

> 证据等级:★★★(源码级;`NanmiCoder/dsh-agent-teams@4354b0f6a793b75c1904c0ee85eef4043a37c733`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 573、下载 10525 为 2026-08-19 历史采样;2026-11-18 实时星标 3005(约 5.2 倍),实时值与 ⚠ 值不同期,下文不混排。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `NanmiCoder/dsh-agent-teams`([registry](../../../data/plugins/NanmiCoder__dsh-agent-teams.yml)) |
| 类目 | workflow([census](../../ecosystem/census.py) 703 条 / 全表 11 744 条) |
| 子分类 | `multi-agent` |
| 自述 | registry 只有「AgentTeams 多智能体团队」一句;真正的自述在 README:队长 + 持久成员 + 带依赖任务 + 直接消息 + Web 树状监视 + 可选质量门 |
| 星标 ⚠ | **573**(2026-08-19 采样);2026-11-18 实时 **3005**。⚠ 口径下 workflow 类第 3(前两名 5565、860),全表第 18 |
| 下载 ⚠ | **10525**(2026-08-19);workflow 类**第一**,是类内第二(1951)的 5.4 倍;全表第 7 |
| 扩散 | **6 条真衍生/硬依赖**(另 1 条互操作适配、2 条仅提及/撞名);口径与命令见「为什么它突出」末节。raw grep 两个 token 取并集 10 条(含自身) |
| 仓库 commit | `4354b0f`(2026-11-13,`main`,`Merge pull request #355 from NanmiCoder/codex/harness-022-rc2-compat`);仓库创建 2026-08-12,首提交同日、提交信息已是「AgentTeams plugin for DeepSeek Harness」;314 个提交、25 个 release、247 fork、88 open issue |
| 包形态 | npm `@nanmicoder/dsh-agent-teams@0.1.30`,Cordis **bundle**:`dsh.bundle.patch` → `cordis.patch.yml`(21 行),外加 `dsh.client.inject` 8 个浏览器侧包、`engines.dsh >= 0.1.2-alpha.2` |
| 代码规模 | `src/**/*.ts(x)` **17 387 行**(宿主侧 12 840 + 浏览器侧 4 547);测试/验证脚本 **13 287 行**(37 个 `.test.mjs` 6 151 + 5 个 `*-tdd.mjs` 2 475 + 9 个 `*verify*.mjs` 4 661;326 处 `test(...)`);`lib/` 是提交进仓库的构建产物(18 666 行 JS / 1.6 MB),这也是 GitHub 把仓库语言标成 JavaScript 的原因 |

## 它到底是什么

**它不是编排引擎,也不是某个外部 AgentTeams 的适配层。** 仓库里没有第二套 agent 运行时:`AgentTeams` 是这个插件自己定义的数据模型,而"团队成员"直接复用 DSH 的 continuable subagent 原语。证据是 `src/state.ts:1-14` 与 `src/scheduler.ts:1-13` 的模块注释——mailbox 布局"mirroring the Claude Code AgentTeams mailbox layout",调度器则解释"Claude Code 的队友靠轮询共享任务表,而 DSH 的 continuable agent 有显式 idle/running 边"。也就是说:概念借自 Claude Code AgentTeams,**实现是 DSH 原生重写**,依赖面只有 `@deepseek-ai/*`(peerDependencies 24 个,`package.json:117-142`)。

四个实体,全部可从类型定义读出:

- **team** — 一个目录 `<workspace>/<stateDir>/<teamId>/`,`stateDir` 默认 `.agent-teams`(`src/index.ts:133`),内含 `team.json` + `inbox/<agentKey>.jsonl`(`src/state.ts:4-7`,`src/types.ts:356-398`)。**没有数据库、没有常驻服务**。
- **captain** — **不是新实体,就是发起会话本身**。`captainSessionId` 记在 `team.json`(`src/types.ts:366`);授权靠 `teamLeadMatch`(`src/lineage.ts:162-175`):允许顶层 fork 沿 `header.parentSession` 继承队长身份,但**列在 members 里的会话永远不是队长**(:169),member 的 fork 也不是(:173)。
- **member** — 一个 DSH **continuable subagent**:`ctx.subagents` 建出子会话,child session id 写回 `member.id`(`src/members.ts:1032-1066`);类型注释直说「Durable continuable subagent session id」(`src/types.ts:263`)。不是一次性 spawn、不是独立进程、不是新会话类型。默认 provider 是 `spawn`(`src/index.ts:134`),要求 provider 具备 `prepareContinuable` + persona + toolFilter 能力,缺一项就在**首次 spawn 时**抛可读错误(`src/members.ts:1008-1024`)——注释解释了为什么把校验放在这里而不是挂载时(provider 是兄弟插件在并发激活里注册的,`src/index.ts:210-214`)。
- **task** — `team.json` 里的数组,`t1/t2…` 编号,状态机 `pending → claimed → in_progress → completed|failed|cancelled`(`src/types.ts:14-23`,转移表 `src/state.ts:148-162`),带 `dependencies`、单调递增的 `attempt` 与能力令牌 `attemptId`、可选的六类质量字段(`objective/inScope/acceptance/verify/verdict/findings`,`src/types.ts:163-256`)。

**核心循环是事件驱动的推,没有轮询线程。** `agent/status` 的 idle 边(`src/scheduler.ts:547`)→ 对该成员 `kickMember` → **在团队锁内**重读 `team.json`、取一张 ready 任务、`beginTaskAttempt` 生成新 `attemptId`、成员置 `working`、写盘(`src/scheduler.ts:353-438`)→ 拼 assignment prompt 直接投进成员会话(`deliverToMember` → `queueMemberPrompt`,`src/members.ts:1093-1110`)。成员干完调 `agent_teams_update_task`(`src/tools.ts:1871`)再 `send_message` 回报;队长被这条消息唤醒。

## 怎么接进 DSH

**① manifest 是 bundle patch + 浏览器侧注入,没有别的字段。** `package.json:68-85`:

```json
"dsh": { "bundle": { "patch": "./cordis.patch.yml" },
         "client": { "inject": ["@deepseek-ai/dsh-client-locale", "…-ui-conversation",
                     "…-ui-layout", "…-ui-sidebar-right", "…-ui-model-selection",
                     "…-api-session-controller", "…-ui-session", "…-ui-chat"],
                     "platform": "web" } }
```

`cordis.patch.yml:10-21` 全文只有一条 `insert`:`id: agent-teams`、`name: '@nanmicoder/dsh-agent-teams'`、`stateDir: .agent-teams`、`memberProvider: spawn`。注释 :17-18 自己写明状态落在 `<session workspace>/<stateDir>/<teamId>/`。

**② 服务注入只有 5 个,其余全是有兜底的可选。** `src/index.ts:57`:

```ts
export const inject = ['tools', 'llm', 'subagents', 'systemPrompt', 'agents']
```

`commands` 走 `ctx.inject(['commands'], …)` 惰性注入——注释明说最小组合里没有命令注册表也要能跑,只是少一个斜杠命令(`src/index.ts:232-241`);Web 服务器与工作区用两代 service key 兜底(`webServer|httpServer`、`workspaceRegistry|workspace`,`src/index.ts:52-54,249-255`);`sessions`/`sessionPersistence` 用 `ctx.get` 探测(`src/lineage.ts:55-63,69-95`)。所以 headless profile 只丢 UI,工具面照常。

**③ 五个事件钩子,全部是 Cordis 订阅,不改宿主文件:**

| 事件 | 位置 | 干什么 |
|---|---|---|
| `agent/created`(旧宿主回退 `agent/session-start`) | `src/harness-compat.ts:296-306` | 每个 agent 就绪时装一个 capability scope(成员/队长各一套系统提示与工具面) |
| `agent/pre-step` | `src/mailbox.ts:74-182` | **信箱准入**:认出带 receipt 的注入消息,在锁内核对 `attemptId` 仍是当前代,ack 后改写成纯正文放行;过期邮件丢弃,若整轮只由废邮件触发就 `reject`(:168-180) |
| `agent/pre-step` | `src/command.ts:125-145` | 纯文本 `/agent-teams` 手势边界,补一条 activation directive(给没有命令注册表的宿主用) |
| `agent/status` | `src/scheduler.ts:547-551` | 派活、停放、冷恢复的唯一驱动 |
| `internal/service` | `src/index.ts:523-528` | Web/工作区服务晚绑定时补注册路由 |

**④ 注册点。** `ctx.tools.register` 14 个 `agent_teams_*`(`src/tools.ts:944,1156,1280,1312,1416,1475,1633,1764,1871,2097,2178,2313,2460,2512`;名单 `src/tool-names.ts`)。`ctx.systemPrompt.section({ name: 'agent-teams:usage', order: 117 })`(`src/capabilities.ts:101-106`),文本按身份二选一:队长拿 10 条 captain protocol(`src/index.ts:180-191`),成员拿 6 句约束(`src/capabilities.ts:13`)。`ctx.commands.register('/agent-teams' + 每个 profile 一个闭合命名空间别名)`(`src/command.ts:87-122`)。4 条 Web 路由 `/plugins/dsh-agent-teams/{state,halt,plan,assets}`(`src/index.ts:260,281,336,488`),**全部过宿主的 connection 鉴权门**(`src/web-routes.ts:100-127`:Connection 缺失返回 503、401/403 直传,失败即关闭)。

**⑤ 浏览器侧 6 个 slot + 一个 conversation node。** `src/client/index.tsx:88-138`:`shell.overlay`(活动浮层)、`conversation.chat.node`(key `agent-teams` 的团队卡)、`conversation.session.header.actions`、`conversation.chat.turnTail`、`sidebar.right.pane.tab`、`conversation.chat.commandview`,外加 `ctx.uiConversation.events.register(agentTeamsCardDefinition)`;语言包走官方 `locale.register`(:62),槽位全部 `ctx.inject` 惰性——`sidebarRight` 缺席时整块原生贡献消失而不报错(:86-88)。

**⑥ 没有 patch 宿主文件,但有一处就地接管。** `guardSubagentCreation` 用 `Object.defineProperty` 把 `ctx.subagents` 上的 `start`/`startContinuable`/`startActivation` 换成自己的包装(给成员的派生创建上深度预算),dispose 时按原 descriptor 还原(`src/harness-compat.ts:167-199`)。这是**进程内改共享服务对象**,不是改包。

**⑦ 安装**:`dsh plugin --profile <p> add @nanmicoder/dsh-agent-teams`,或桌面端插件面板直接贴仓库 URL;另提供 `bin` 诊断器 `dsh-agent-teams-doctor`(`package.json:254-256`)。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `src/index.ts` | 529 | 插件入口:Config schema、注入、4 条路由、启动恢复 | :57 inject、:132-176 Config、:216-224 装配、:523 service 事件 |
| `src/tools.ts` | 2938 | 14 个工具 + 派发器 + staged/running 两相控 | :664 注册入口、:674-723 `dispatchMember`、:831-868 批准、:557-600 halt |
| `src/quality-gates.ts` | 2109 | 六类质量门、审查回路、覆盖矩阵、升级 | :44-47 默认轮数、:936/:985 escalate、:2013 提示词 |
| `src/state.ts` | 1315 | 全部持久化 + 纯规则 + 损坏诊断 | :67-84 团队锁、:245-260 读、:300-302 写、:437 信箱追加、:669-703 原子替换 |
| `src/members.ts` | 1204 | 成员 spawn/投递/失败归因/守卫 | :991-1074 `spawnMember`、:1093-1110 `deliverToMember`、:250-278 失败分类、:1139-1144 退役守卫 |
| `src/scheduler.ts` | 554 | 事件驱动派活与停放 | :301-311 `kickTeam`、:353-438 锁内领取、:364-398 停放、:457-484 回滚 |
| `src/harness-compat.ts` | 673 | 4 代宿主 API 的适配缝 | :23-40 私有 symbol、:150-164 `startMember`、:167-199 创建守卫、:296-306 ready 钩子 |
| `src/tool-policies.ts` | 219 | 成员工具白/黑名单解析 | :205-218 `resolveMemberToolFilter`、:31 深度禁用名 |
| `src/mailbox.ts` | 183 | 信箱准入与投递回执 | :11-19 代次过滤、:74-182 pre-step |
| `src/command.ts` | 145 | 斜杠命令 + 手势边界 | :87-122、:124-145 |
| `src/capabilities.ts` | 113 | 按身份切系统提示与工具面 | :93-95 `tools.restrict`、:101-106 section |
| `src/lineage.ts` | 248 | fork 血缘下的队长身份 | :162-175 `teamLeadMatch`、:206-237 `nearestLiveLead` |
| `src/snapshot.ts` | 316 | 面板快照(磁盘为准 + 活体活动) | :134 组装、:249/:292 活跃/归档 |
| `src/client/*` | 4547 | 浮层、团队卡、路线图、staged 计划编辑器 | `src/client/index.tsx:88-138` |
| `scripts/*` | 13287(测试/验证) | 假宿主驱动的对抗式一致性验证 | `scripts/lifecycle-verify.mjs` 1556 行、`scripts/stress-verify.mjs` 548 行 |

**写入路径**(`agent_teams_update_task` → `src/tools.ts:1871`):锁内重读 team → 校验调用者身份(队长/该任务的成员)→ 校验 `attempt_id` 是当前代 → 校验状态转移合法 → 写质量字段 → `writeTeam`。终态不可改判,但允许追加 `acceptanceResults/commandsRun/evidence_note` 作为**归因的补充证据**(描述里明说 append-only、不改 verdict)。

**派活路径**(`src/scheduler.ts:313-486`):

```
agent/status(idle) ──▶ kickMember ──▶ serializeMember(成员级队列)
   └─ 锁内: 是否有 ownedOpenTask?
        ├─ 有且本进程没见过(冷启动) → 一次恢复,立即 parked 标记
        ├─ 有且本进程见过 idle → 停放,不自动重试(等队长 reassign)
        └─ 无 → nextReadyTask(先自己名下,再未分配) → beginTaskAttempt
   └─ 投递失败 → 锁内回滚「仅自己那张票」:attemptId 不匹配就认输(:461)
```

**消息路径**(`send_message` → `src/tools.ts:2178`):写收件人 `inbox/<key>.jsonl`(`src/state.ts:437`)→ 队长直接 `steer`,成员走 `queue`(`src/members.ts:1093-1110`)→ 对方 `agent/pre-step` 认出 receipt,核对代次后 ack。投递租约 60 秒(`src/state.ts:54`),防"直接投递与兜底投递"并发重复。

**恢复路径**:`team.json` 是唯一真源,成员 id、`attemptId`、`phase`、`halted` 全在里面;冷进程的 `parkedAttempts` 是空 Map,所以每个未收尾的 attempt 恰好有一次冷恢复机会(`src/scheduler.ts:364-398`);被移除成员进磁盘黑名单 `retired-members.json`,不允许冷恢复(`src/state.ts:55-56`,`src/members.ts:1139-1144`)。

## 为什么它突出

**先拆星标归属:整份 3005 都记在这个插件头上。** GitHub 星标是仓库级,而本条目就是仓库根(不是 monorepo 子目录),不存在母项目:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-12 | 仓库创建 13:41Z;**同日首提交**,信息即「dsh-agent-teams: AgentTeams plugin for DeepSeek Harness」 | GitHub API `created_at` / `git log --reverse` |
| **2026-08-19** | **⚠ 573 星 / 10525 下载采样点**(仓库 7 天龄,尚无 release) | `data/stars.json`、`data/downloads.json` |
| 2026-08-21 | 第一个 GitHub release `v0.1.10` | releases API |
| 2026-11-13 | `v0.1.30` + HEAD(`4354b0f`),适配 Harness `0.2.2-rc.2` | releases API / `git log -1` |
| 2026-11-18 | 实时 **3005** 星、247 fork、88 open issue | GitHub API |

仓库**没有前史也没有第二个宿主**:peerDependencies 全部是 `@deepseek-ai/*`,没有别的 harness 适配目录。所以不存在"主项目星标借给插件"的问题,唯一需要说明的是**名字与概念借自 Claude Code 的 AgentTeams**(`src/state.ts:7` 等 7 处注释自述"mirroring"),这不影响星标归属,但影响"原创性"判断:原创在 DSH 侧的实现,不在团队模型本身。

**扩散接的是哪一层,比扩散数量更有信息量。** 两个 token 取并集:

```sh
grep -ril 'agent-teams' data/plugins/ | wc -l          # 5(含自身)
grep -ril -i 'agentteams' data/plugins/ | wc -l        # 8(含自身)
grep -rilE 'agent-?teams' data/plugins/ | wc -l        # 10(含自身)= 9 条第三方
grep -rl 'nanmicoder/dsh-agent-teams' data/plugins/    # 1(只有 Kippythisway 点名 npm 包)
```

| 类型 | 条目 | 接的是哪一层 |
|---|---|---|
| **fork / 独立设计分支** | `ChenXu233/dsh-agent-teams` | 整份代码;自述警告"两者注册同一个 `agent-teams` 行,不要同装"——反向证实 patch 行 id 是公开契约 |
| **配置层扩展** | `Kippythisway/dsh-team-v3` | 按 `id: agent-teams` 指向本引擎、**整段替换其 config**;三套编制 + seed 任务 DAG,正好落在 `profiles` 里 `tasks`/`members` 的形状上(`src/index.ts:139-170`) |
| **UI / 状态层扩展** | `dadgrand/dsh-agent-teams-dashboard` | 侧栏面板:成员、任务路线图、按时段 token 花费与成本、归档。自述"需先安装 Agent Teams 插件" |
| **工具参数桥** | `dsh-agent-roster/dsh-agent-roster` | 把 YAML/JSON 编制校验后**桥接成 `add_member` 的建员参数**,再对照运行中的团队核对 |
| **打包 / 消费** | `yyyy231209/ai-company-framework`、`sxwer001/dsh-collab-dev` | 前者把"AgentTeams 运行时与活动面板"打包进公司框架;后者"通过原生 AgentTeams 并行开发与独立审查" |
| 互操作适配 | `samirliu/dsh-goalloop-agentteams` | 只对**任务 claim 语义**做适配(自述:多任务 Agent Teams 循环不死锁),插件名里带 agentteams |
| 仅提及 / 撞名 | `zhuto666/dsh-compact-agents`(把"AgentTeams 成员"当作一类活会话)、`MythGreenLand/dsh-local-delegate`(自建并行子 agent 的开关叫 `SlaveAgentTeams`) | 不接任何一层 |

判断:**收敛发生在"团队文件格式 + patch 行配置"这一层,不在调度协议层**。六个真衍生里,四个直接读写它的配置或磁盘状态/工具参数,没有一个复用 `attemptId` 代次、停放或冷恢复语义——那条路只有源码级 fork(`ChenXu233`)才碰得到。这与本插件自己的设计一致:它**没有**把任务板注册成宿主级 service 或对外协议(`ctx.tools` + 磁盘文件就是全部对外面),所以别人只能接文件和参数,接不到协议。

## 代价与边界

- **权限放大是真的**。成员是完整 agent,与队长共用同一工作区和同一套 `fs`/`bash` 权限;插件只裁剪**工具可见性**:成员恒被拒 10 个队长工具(`src/tool-policies.ts:42,212`),`memberMaxDepth: 0`(默认)时再拒 `subagent`/`send_message`(:31,209-211);部署方可在 `toolPolicies` 里声明具名 allow/deny,模型只能**选一个已存在的 id**,永远不能提交原始名单(`src/tool-policies.ts:1-8`,`src/index.ts:182`)。源码自己把边界写得很清楚:「This is tool visibility / invocation policy for global tools, **not an OS sandbox**」(`src/tool-policies.ts:14`)。给 8 个成员开文件写权限,等于把 8 个不受文件级约束的写者放进同一棵树。
- **成本随成员线性走**。每个成员可以独立 provider/model/`reasoningEffort`(`src/index.ts:74-83`),经 `ctx.llm.resolveCallConfig` 解析成真实路由(`src/members.ts:494-590`)——即**独立计费**;不指定时继承队长的路由。并发上限只有 `maxMembers`(默认 8,`src/index.ts:173`;创建时校验 `src/tools.ts:1363`),`kickTeam` 会对每个成员各 kick 一次(`src/scheduler.ts:307-310`),所以最坏情况是 8 条同时跑的会话,加上队长自己。没有全局 token 预算或并发闸。
- **失败模式,按发生顺序**:
  1. **成员卡住不回报**。本进程见过它 idle 就**停放**(`parkedAttempts`,`src/scheduler.ts:279,364-369`),不会自动重试——必须队长 `reassign_task` 显式撤销;`stopping` 的成员不再派活(`src/scheduler.ts:191-195`)。设计上这是刻意的("Automatic retry is reserved for cold recovery",:9-11),代价是**没有心跳超时**:一个既没 idle 也没报错的成员可以一直占着 attempt。
  2. **队长丢失**。`captainSessionId` 是持久的,`nearestLiveLead` 会退到最近的活 fork 后代(`src/lineage.ts:206-237`),但**派活必须有活着的 lead**:`liveCaptain` 取不到就直接 return(`src/scheduler.ts:182-185,305-306`),不写盘、不告警。**关掉队长会话 = 整个团队静默停摆**,重新打开同一会话才继续。
  3. **任务板写入冲突**。裁决只有一把**进程内**的 promise 队列(`withTeamLock`,`src/state.ts:58-84`),`team.json` 是整文件重写(`src/state.ts:300-302`),靠同目录临时文件 + rename 保证单次写原子(:669-703)。**没有文件锁、没有 revision 比较**:判断:同一工作区被两个 DSH 进程(例如 `dsh web` + headless/桌面端)同时驱动时,后写者静默覆盖前者,且没有任何检测或告警。信箱侧也只有进程内租约(`src/types.ts:320`)。
  4. **进程重启**。这是设计过的:冷启动 `parkedAttempts` 为空 → 每个未收尾 attempt 恰好一次恢复;被移除成员有磁盘黑名单防止冷恢复(`src/members.ts:1139-1144`)。但恢复后成员是新的一次 `queue` 投递,`attempt` 号会加一,之前那轮的上下文只留在子会话自己的历史里。
  5. **状态文件损坏**。`readTeam` 抛错(:245-260);`agent/pre-step` 的信箱准入降级为"原样放行"(`src/mailbox.ts:106-111`),委派创建则被守卫拒绝并给可读错误(`scripts/corrupt-teamjson.test.mjs` 的 B1/B4/B5 就钉这三条)。结果是**普通对话可用、团队操作全废**,且降级只打 warn。
  6. **宿主 API 漂移(最贵的一条)**。`src/harness-compat.ts` 673 行专门吃这个:私有 symbol `Symbol.for('dsh.subagent.queuePrompt')` / `deliverPrompt`(:23-40)、`tree.manager.deliverToMember`/`resident`(:82-88)、`startActivation` vs `startContinuable`(:150-164)、`KNOWN_SESSION_EVENT_TYPES`(`src/events.ts:45-54`)。`compatibility.json` 列了 13 个宿主版本、分 recommended/preview/legacy 三轨;`unsupported()` 会抛带指引的错误(:205-207)。但**私有缝没有版本承诺**:新宿主换掉那个 symbol,插件不会报错,只会少掉某些路径(注释自承 `appendTeamEvent` 在宿主不认事件类型时直接丢弃,:39-54)。
- **数据/隐私**:全本地。`src/` 里没有任何出站网络调用(仅浏览器侧同源 `fetch` 打自己的 4 条路由:`src/client/activity-monitor.ts:315`、`src/client/ActivityPanel.tsx:582`、`src/client/StagingPlanEditor.tsx:43`)。团队状态、消息、审查结论都落在工作区 `.agent-teams/` 下,会**进版本库**——`.gitignore` 是否覆盖由使用者决定,插件不装 gitignore 规则。这也意味着团队历史会随仓库被分享。
- **维护成本**:314 提交 / 25 release / 3 个月,仓库里还有 11 个 `.dsh/skills/*` 维护技能、`docs/harness-0.2.x` 逐版本审计目录、`scripts/doctor.mjs` 诊断器。**这是本批里少见的"带齐 CI 矩阵 + 升级审计"的插件**,但反过来说,它的工作量主要花在追宿主 API 上,不是团队协作本身。
- **兼容成本落在使用者身上**:`engines.dsh >= 0.1.2-alpha.2` 但只有 `compatibility.json` 里列出的 13 个版本被 CI 验证过;README 明确"推荐 0.2.1-rc.2 + 0.1.30"、"host 仍是 RC"。

## 可信度与复现

证据等级 ★★★:宿主侧 12 840 行逐文件通读(`index/tools/state/scheduler/members/mailbox/command/capabilities/lineage/harness-compat/tool-policies/quality-gates` 的关键段与全部导出),浏览器侧只读了入口与路由,`src/client/ActivityPanel.tsx`(1395 行)、`src/client/StagingPlanEditor.tsx`(829 行)、`src/quality-gates.ts`(2109 行)只读了导出与关键分支——**渲染细节与质量门全部判定分支未逐行读**。

```sh
# 1) 克隆(仓库含构建产物 lib/,只读源码目录)
git clone --depth 1 --filter=blob:none https://github.com/NanmiCoder/dsh-agent-teams.git /tmp/an-agent-teams
cd /tmp/an-agent-teams && git log -1 --format='%H %ad %s'
# → 4354b0f6a793b75c1904c0ee85eef4043a37c733 2026-11-13 Merge pull request #355 ...

# 2) 规模
find src -name '*.ts' -o -name '*.tsx' | xargs wc -l | tail -1        # → 17387
find src -name '*.ts' -not -path 'src/client/*' | xargs wc -l | tail -1 # → 12840
ls scripts/*.test.mjs | wc -l                                          # → 37
cat scripts/*.test.mjs scripts/*tdd.mjs scripts/*verify*.mjs | wc -l   # → 13287
grep -ho "test('[^']*'" scripts/*.test.mjs scripts/*tdd.mjs | wc -l    # → 326

# 3) 形态
sed -n '10,21p' cordis.patch.yml      # 唯一一条 insert + 两个配置项
sed -n '68,85p' package.json          # dsh.bundle.patch + dsh.client.inject

# 4) 扩散(在 awesome-dsh-plugin 仓库根;11744 个 yml 必须用目录形式,展开会 argument list too long)
grep -ril 'agent-teams' data/plugins/ | wc -l        # 5
grep -ril -i 'agentteams' data/plugins/ | wc -l      # 8
grep -rilE 'agent-?teams' data/plugins/ | wc -l      # 10 ← 含自身,9 条第三方

# 5) 归属与时效(2026-11-18 当日)
curl -s https://api.github.com/repos/NanmiCoder/dsh-agent-teams | grep -E 'created_at|stargazers_count|forks_count'
# → created_at 2026-08-12T13:41:50Z, stargazers_count 3005
curl -s 'https://api.github.com/repos/NanmiCoder/dsh-agent-teams/releases?per_page=100' | grep -c '"tag_name"'  # → 25
```

## 待验证

1. **跨进程并发到底会不会互相覆盖**:`withTeamLock` 只在进程内(`src/state.ts:58-84`),`team.json` 无 revision 字段。要证实这条风险,需要同时起 `dsh web` 与 headless 两个进程写同一 `.agent-teams/<teamId>`,看是否产生丢失更新——本次只做静态判断,未实测。
2. **`agent_teams_delete` 之后成员会话的命运**:`archiveTeamDir`(`src/state.ts:1189`)把团队目录移进 `archive/`,同时 `stopTeamMemberActivations` 停掉激活;归档成员的子会话历史是否还能在 UI 里打开,取决于 `direct-child catalog`(`src/members.ts:1127-1137` 的注释),未在真实宿主演示。
3. **staged 计划的两相批准在 headless 下的体验**。Web `/plan` 的 approve 会给队长 `steer` 一条 `stagedPlanApprovedContext`(`src/index.ts:376-393`);纯 CLI 没有这条路由,只能靠模型在同一会话里再调 `agent_teams_approve`。这条路径的可靠性未验证。
4. **`dsh find`/registry 之外的扩散**:本卡的 9 条只统计本 registry 的 11 744 条。GitHub 上是否还有 fork(247 个 fork 里多少是改过代码的)、AtomGit 镜像(README 顶部挂了 AtomGit 星标徽章)都未统计。
5. **8 成员并发的真实成本**:`maxMembers: 8` 是硬上限,但没有 token 预算。一次 8 成员 + 审查回路的实际花费未量化,`dadgrand` 的面板自述统计成本,或可作旁证,但其源码未读。
6. **质量门的判定质量**:`src/quality-gates.ts` 2109 行里 review 只能 `verdict=pass` 才完成、`maxRepairAttempts: 2` 后 `escalated`(:44-47,:985)——规则读到了,但"审查是否真能挡住错"需要跑真实任务,未做。
7. **README 声称的 CI 矩阵是否真的跑过**:`compatibility.json` 列 13 个宿主版本,`.github/workflows/` 未读,无法确认每个版本都在 CI 里被执行(而非仅登记)。
