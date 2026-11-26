# 10 · MYCF711/dsh-session-superagent — 会话级唤醒:留住管线,牺牲 Ticket

> `MYCF711/dsh-session-superagent@fe1c356`(v2.0.0,52★,2026-11-25 实时值)。上游 `deepseek-ai/dsh-superagent@8c32a9dc`(24,565★)。证据等级 ★★★:读了 README、`docs/` 的设计/对比/官方拆解三组文档、`lib/rooms/` 20 个房间、`package.json` 与 `cordis.patch.yml`;**没有**实装运行,也没有逐行 diff 上游(仓库里没有可 diff 的对象)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 层 / 关系 | **D3 设计衍生**:自述"项目起点 = 上游原型",但零上游代码、零上游 id、零上游运行契约 |
| 一句话 | 轮询 GitHub/Gitee,仓库有动静时**叫醒你已经开着的那个会话**;默认 `inline`,不另起执行体 |
| 自述起点 | `README.md:20`「老板把老家的 dsh-superagent-prototype 丢给我……给 DSH 做个会话级 superagent」;`README.md:162`「本项目的起点」 |
| 声量 / HEAD | **52★** / `fe1c356`(Merge PR #69,release 2.0.0) |
| 包形态 | 包名 `dsh-session-superagent`(package.json 写 `2.0.0`,但 `README:191` 自述「未发布 tag / Release / npm」),MIT;`dsh.bundle.patch` + `dsh.client.platform=web`;plugin id **`session-superagent`**(`cordis.patch.yml:8-9`) |
| 宿主钉版 | `engines.dsh: >=0.2.2-rc.1 <0.3.0-0`、node `>=22.19`、peer `@deepseek-ai/cordis ^4.0.1` |
| 运行时依赖 | 只有 `@mycf711/dsh-gate@0.1.5`(自研门禁)与 `@deepseek-ai/schemastery`;**没有**上游包 |
| 代码规模 | `lib/` **12,282 行**(含 `lib/rooms/` 20 个房间);`client.js` 5,765 行;`test/` 94 个测试文件 32,417 行(README:175 自述 1420 项单测) |
| 状态文件 | `~/.dsh/state/session-superagent/watchers.json`(`README:62`;`lib/index.js:316-321`) |
| 上游文档资产 | `docs/official-decomp/` **1,937 行**:5 份分报告 + `BASELINE.txt`/`SOURCE_PATH.txt` 两个锚点文件(基线写死 `8c32a9d`) |
| 复现 | `git clone https://github.com/MYCF711/dsh-session-superagent && git checkout fe1c356` |

## 影响力

- **数字(GitHub API,2026-11-26 取)**:52★ / **12 forks** / 1 watcher / 1 open issue;创建于 2026-11-01,`pushed_at` **2026-11-25T02:21:56Z**;MIT。
- **发布(asof 2026-11-25)**:npm `dsh-session-superagent` 的 `latest` 当时停在 **0.10.12**(2026-11-09),仓库 HEAD 的 2.0.0 未发(`README:191`)。**2026-11-26 复查已变**:`2.0.0`(11-25T17:24Z)、`2.0.1`、`2.0.2` 已发布,latest=`2.0.2`。"看到 52★ 去装"的人此前拿到的是 0.10 线,不是这页分析的 2.0 代码;2.0.2 是否等于本页所读 `fe1c356` **未验证**。
- **注册表位置**:`data/plugins/MYCF711__dsh-session-superagent.yml`,类目 `session`(该类 1,022 条)。条目描述仍写"盯一个 GitHub 仓库"(单数),而插件已支持一条会话守多仓(`README:33`),登记信息落后于实现。
- **时间形状**:2026-11-01 建仓,24 天到 52★,`pushed_at` 与 HEAD 同日(11-25)——增长与提交同步,更像"被注册表/榜单看见"而不是长期口碑积累。star:fork ≈ 4.3:1,旁观者多于改造者。
- **判断:算有影响,但影响的是"品类",不是"依赖图"。**
  - 在 D3 里它是唯一有社区量级的:52★ vs imperial 2★、nattocb 0★;12 forks 说明有人愿意留一份可改的副本,不只是收藏。
  - 它不在这个生态的依赖图里:同批 9 个依赖/衍生仓库没有一个把它当依赖,也没有可被读的 `Source`/`stateDir` 契约(D2 那三条接法它一条都不适用)。它的影响方式是**示范**——"super-agent 可以只是一条唤醒,不必是一个常驻 profile"。
- **量级要放对**:52★ 是上游 24,565★ 的 0.2%,也低于 D1 的 HiSeax(138★)。把它当"社区采用"会重犯 [impact.md](../impact.md) 警告过的错(把机构背书当社区采用);它真正的杠杆是**把部署门槛降到一条安装命令**,不在生态位。

## 1. 它要解决什么问题

上游的隐含前提是**团队仓库 + 无人值守 + 一个 agent 服务一整个团队**:一条事件从 Source 进来,经 Policy 授权、Eval 判研,变成 Ticket,再交给独立 Executor 会话,结果以 PR/评论回原对话(上游 `001-domain.md:7,23`、`003-execution.md:25-29`)。这套前提要求:有团队、有共享仓库、有 bot 账号、有能长期占一个 profile 的部署。

它的用户不满足这些前提。作者把差异写成一份产品文档,而不是写在 issue 里:

- **上游回答的是另一个问题**:「一个 agent 服务一整个团队」——组织级自主(`docs/为什么做这个产品.md:16`);
- **它的用户的瓶颈不是写代码,是注意力**:切到 GitHub 看一眼 issue、回来上下文没了;三天后才看到 bug report(`docs/为什么做这个产品.md:18-28`);
- **所以产品形态被收窄成一句**:「就在你正在用的会话,不新开窗口、不装额外服务」(`docs/为什么做这个产品.md:40-43`);
- 对外也这么说:「official prototype … That is the right shape for a team. This one targets the opposite end: a single person who already has a session per repository」(`docs/awesome-submission.md:51-53`)。

判据是清楚的:一个单人开发者,一个项目一个长期会话,不想为「看一眼」再配 bot、dashboard、webhook。**上游不是不够好,是部署形态与用户规模不匹配**——这是 D3 三页共同的起点。

## 2. 它的路径:保留什么、丢什么

它保留了**管线的形状**,但在默认路径上把记账单位从「Ticket」换成了「水位 + 唤醒」:

| 上游概念 | 上游规则(出处) | 这里 |
|---|---|---|
| Source | kind 可扩展、每个 Source 持读位与 bot 身份(`001-domain.md:27`) | **保留形状,砍掉抽象**:写死 `parseRepoSpec`,只有 GitHub + Gitee,`cursor/seen/lastReported` 挂在 watcher 上(`docs/对比-官方原型.md:22-23`) |
| Trigger / Thread | 幂等、按 Thread 串行 Eval(`001-domain.md:28-29`) | **保留水位,丢掉 Thread**:`seen`/`updated_at` 推进即视为处理过;没有「一个 Thread 同时只能跑一个 Eval」的对象 |
| Eval | 两层 gate + assessment(`001-domain.md:33`) | **降成单层过滤 + 优先级权重**(`docs/对比-官方原型.md:41`);v2.0 补了 `lib/rooms/admission-eval.js`,仍是 gate 先、assessment 后,但 Decision 只是一次返回值,不是可追溯的记录(`admission-eval.js:1-16`) |
| Policy | 版本化、按 Source 维护名单(`001-domain.md:32`) | **只留最小版 `allowAuthors`**(`docs/为什么做这个产品.md:111`);无版本、无变更投递 |
| Mandate | 不可变、只有人能撤回(`001-domain.md:34`) | **丢弃**。授权 = 「装了这个守的那个人」 |
| Ticket | 只由 Eval 创建、自己的状态机、不跟随 Session(`001-domain.md:35,56`) | **v0.9 明确不抄;v2.0 又补了一个**(见 §4.4) |
| Assignment / Executor | 一 Ticket 一会话一目录、可换执行体(`003-execution.md:25`) | **`worker` 模式才有**;默认 `inline` 没有执行体概念 |
| Subscription | 后续讨论自动到达执行体(`001-domain.md:37`) | **丢弃**:每条新动态都要重新唤醒(`docs/对比-官方原型.md:24`) |
| Channel / Delivery | 结果回写原对话(`001-domain.md:31`) | **半保留**:`watch_ack(comment:true)` 回写原条目;默认只打标签 |

两种执行方式是这个取舍的开关:

- **`inline`(默认)**:唤醒消息注入当前会话,用 `Agent.followup()`(`lib/index.js:1659-1671`);不建 Session、不建目录、不装预设(`README:29`)。
- **`worker`(显式)**:每 Ticket 一个持久 Session,名字仍是 `worker-<ticketId>`(`lib/rooms/executor-host.js:6-11`),工作区由 `workspaceRegistry.create(workdir)` 建,预设用内置 **`standard`**(`executor-host.js:43`),不是上游的 `dsh-superagent-worker`(`003-execution.md:29`)。

一句话:**它保留了「Source → 过滤 → 工单 → 回写」这条链,但抽掉了让这条链可授权的三种对象(Policy/Mandate/Assignment),把它们换成了「会话状态 + 水位 + 冷却」。**

## 3. 它如何利用 dsh-superagent

**用在文档、设计和提示词层面,不碰代码。** 可以逐条指认:

1. `README.md:20` + `README.md:162`:血缘自述(「起点」),并给出上游链接。
2. `docs/为什么做这个产品.md:110-112`:把上游核心概括为「Policy → Ticket → Executor → Delivery 这套组织级模型」,并声明「我们只抄它的**第一件事**(谁来派活 = `allowAuthors`)」。
3. `docs/对比-官方原型.md:13`:原样抄下上游链路名 `Source → Trigger → Thread → Policy → Eval → Ticket → Assignment → Executor → Delivery`,再逐项做「它有/我们有」对照(第 15-77 行),连「该抄/不该抄/该警惕」都是按上游概念分组(第 80-86 行)。
4. `docs/设计-会话级导航与运行时.md:21-31`:点名基线 `dsh-superagent-prototype@8c32a9d`,列出「只吸收以下骨架」5 条(薄入口/单一组合根、Engine 单事务、Passes 定时器、Source/Executor/Outbox/投影边界、Ticket 级隔离),再列「不搬」:飞书、多人授权、团队角色、独立 Router 部署、重型 Eval/Settings、独立 SQLite。
5. `docs/设计-模块化房间.md:3`:把 1.0 的目标写成「补齐官方原型中适合单人产品的能力」,并给出房间/Room 的 DTO 与上游概念的对应(Ticket、ThreadSubscription、Assignment、OutboxMessage、Admission,第 20-70 行)。
6. `docs/official-decomp/`:**1,937 行考古**,按目录树逐文件拆上游 `src/app`、`src/core`、`src/sources`、`src/client`、`prompts/`,并给出吸收表与「不吸收」理由(`01-structure-tree.md:293-307` 表、`:333-336` 不吸收)。`03-sources.md:4` 自述把 26 个文件的 blob SHA 与官方提交逐一比对过——**这是文档级核对,不是代码复用**。注意 `BASELINE.txt` 只有一行 `8c32a9d`,没有 vendored 源码目录。

**反证:没有代码/契约依赖。**

- **无同名 id**:上游包名 `dsh-superagent`、预设 `dsh-superagent-router|worker`(`003-execution.md:27-29`);这里是 `session-superagent` 一个 id(`cordis.patch.yml:8-9`),worker 用内置 `standard` 预设(`executor-host.js:43`)。
- **无 vendored 目录**:仓库没有 `src/`,没有上游 `.ts` 文件;`lib/` 全是自有 ESM。
- **无运行契约**:`grep orchestrator` 在 `lib/`、`bin/`、`cordis.patch.yml` 里 **0 命中**;不读 `orchestrator.sqlite`,不挂 `bridge.js`,不共享 `stateDir`(D2 那三条的接法它一条都没用)。
- **自己的状态文件**:`watchers.json` / `secrets.json` / `trigger.json`(`lib/index.js:316-321`),`schemaVersion` + 显式迁移 + `.bak` 回退 + 损坏文件改名(`lib/index.js:355-404`、`lib/state-migration.js:1`)。
- **自己的许可**:`LICENSE:3` 版权人是 MYCF711,不是上游。
- **唯一同名的东西是命名约定**:`worker-<ticketId>`(`executor-host.js:6-11`)。它是会话名前缀,不是注册表 id,也不带来任何契约——这恰好标出 D3 的边界:**同名词汇、异名实现**。

## 4. 技术思考

**4.1 单会话 vs 多会话:默认 inline 是关键判断。** 一个项目一个长期会话,它已经持有项目上下文、历史决策、仓库约定,「由它兼任 Lead 比另起一个 Router 更自然」(`docs/设计-会话级导航与运行时.md:7-15`)。代价是执行体 = 你正在打字的会话,所以唤醒必须**等空闲**:`decideWake(agent.status, runningSubagents)` 不过就 `entry.lastDeferred = '会话正忙，下一轮重试'`(`lib/index.js:2566-2583`)。上游用「worker slot + 给人留一个额外 slot」保证人不会被队列堵住(`003-execution.md:57-61`);这里没有队列对象,**忙就是没有 slot**。

**4.2 隔离与并发。** 隔离是**一次性 `git worktree`**:每次唤醒在目标仓库开一个 worktree + 分支,`maxIsolated`(默认 5)、`isolateKeepDays`(默认 3)回收,回收时 `worktree remove --force` + `prune`(`lib/index.js:1262-1346`)。并发控制是三件土办法的叠加:冷却 3 分钟(`lib/index.js:324`)、单守 6 次/小时、会话 12 次/小时(`README:54-58`;`lib/index.js:140`),外加 3 秒合并窗口把同会话的多条并成一条(`lib/index.js:1469-1475`)。它防的是**叫醒过多**,不是**执行过载**——因为执行就是你自己的会话。

**4.3 授权与人工拍板。** 授权只剩两道:`allowAuthors` 名单(0.9.252 起,`docs/对比-官方原型.md:30`)+ 写操作必须显式 `confirm: true`(`README:153`)。没有 Mandate,所以没有「为什么可以干、能干多远」的记录,也没有「Policy 变了要重验」的路径(`001-domain.md:34`)。人工拍板被降成两种轻动作:`watch_ack` 打「已处理」标签,以及通过就继续聊。上游那套 `person/answer`、`person/review`、`Attention` 六阶段(`003-execution.md:9-19`)**一件都没有**。

**4.4 失败收敛,以及一次被记录下来的设计漂移。** 收敛手段是「不确认就不推进」:未送达不推进水位、失败退避、`readState()` 归一、`.bak` 回退、迁移失败保留现场(`lib/index.js:355-404`)。真正有意思的是**它自己承认撞墙又回头补**:

- v0.9 的拆解报告写「Ticket 的 open/ended …… **不复制完整 Ticket 状态机**」「Assignment/Executor 多实例 **不照搬**」(`docs/official-decomp/01-structure-tree.md:299-300`);
- v1.0 起补 `lib/rooms/ticket-state.js`(`open → assigned / waiting → ended`,人类显式 resume,`ticket-state.js:4-9`)、`thread-subscription.js`、`execution-assignment.js`、`outbox.js`、`admission-eval.js`——20 个房间;
- 动因写在更早的产品文档里:「水位线能表达『这条更新过』,表达不了『这条还在进行中』。这是官方原型最值得我们抄的一块,也是我们未来最可能撞墙的地方」(`docs/为什么做这个产品.md:103-104`)。

所以**被牺牲的上游语义**可以精确列成四条:

1. **Ticket 作为可移交的持久主体**——没有 Assignment,就没有「换一个执行体接着干」;`worker` 模式的 session 仍是 `worker-<ticket>`,ticket 与 session 一一绑定,等价于「一 Ticket 一执行体」的退化版。
2. **Mandate 与 Policy 版本**——授权不可追溯、不可撤销、不可重验;人停止工作的方式只有删守/暂停。
3. **Subscription 扇出**——后续讨论不会自动到达执行体,必须再唤醒一次;`onlyNewComments` 只是把「哪些更新算新」调细(`README:95-101`)。
4. **结构化 Report / Attention**——执行结果没有 `progress/waiting/ready/blocked/failed/dropped` 六态(`001-domain.md:112`),只有 ack 标签与自由文本;「有动作率」靠事后统计补(`docs/为什么做这个产品.md:95-97,105-106`)。

## 界面体验

它没有自己的站点,入口集中在四处,全部长在 DSH 的 slot 里(`client.js`):

| 入口 | slot / 行号 | 看到什么 |
|---|---|---|
| 输入框左侧"卫星环" | `conversation.composer.dock`,`client.js:5745-5756`,order **-10** | 一行环 + 每个活着的守一颗卫星;点开是各守详情与最近错误(`sa-dock-err`,`client.js:2705`) |
| 会话右栏 | `sidebar.right.pane.tab` + `.title`(`client.js:5638-5653`);头部按钮 `conversation.session.header.utilities`(`:5658-5660`)开关 | 只属于本会话的 watcher / Ticket / 执行 / Outbox / 草稿 |
| 左侧全局页 | `main` + `sidebar.panellist`,`client.js:5599-5612` | 全部会话的守、筛选、凭证、诊断 |
| 会话消息流 | `Agent.followup()`,`lib/index.js:1659-1671` | 唤醒是一条普通用户消息,不是 toast、不是系统通知 |

- **信息密度**:面板按官方 IA 分「总览 / 判定 / 触发 / 设置」,有模块化能力时多一个「任务」页(`README:118`);判定页内联 trace 时间线(`client.js:2906`),并把「为什么没叫醒」做成跳过原因分布(`client.js:4697-4744`)。
- **实时性**:UI 每 **5 秒**轮询 `/session-superagent/state`(`POLL_MS = 5000`,`client.js:711`;定时器 `:2491`、`:3919`),没有服务端推送;真正的延迟下限是轮询间隔(`README:155` 自己承认这点)。
- **失败时看到**:状态点转 error(HTTP 304 不算,`client.js:2252`)、行内 `lastError` + 年龄 + 按 `lastErrorKind` 给的修复建议,超过 1 小时标 stale(`client.js:4396-4412`);服务端把 `problem` 与 health 放进 deployment 投影(`lib/index.js:515`)。

## 用户交互的思路

回路五段,确认点被前移到"装守"和"ack"两个动作:

1. **你发起**:在会话里让 agent 调 `watch_start({repo, goal})`(`lib/index.js:5300`),或在面板表单里建;守与 `sessionId` 绑定。
2. **仓库有动静**:插件轮询(GitHub 用 ETag、Gitee 每轮真读),过滤 → 冷却 → 时段 → 批大小,水位只前进(`README:33,95-101`)。
3. **叫醒**:只在会话空闲时注入;消息是**任务书**而非通知——编号/状态/标题/作者/标签/链接、为什么是这几条、完成标准、下一步(`docs/示例-唤醒消息.md:10-23`)。
4. **办完**:回写评论要显式 `comment:true`、写操作要 `confirm:true`(`lib/index.js:4483-4495`、`:4958`),再 `watch_ack` 打标签推进水位,同一条不再叫醒。
5. **打断**:会话忙就排队到下一轮(`lib/index.js:2583`);暂停/删除守、全局 `pause-processing`(`lib/index.js:3628-3634`);3 分钟冷却与小时上限是防打扰的闸。

确认发生在**Modal 里**,不在聊天里:面板的写操作走 `ConfirmDialog`/`ConfirmButton`(触发按钮只开 Modal、取消不执行、确认期间 busy 防重复,`client.js:2143`、`:2192`),唤醒本身是只读注入,所以从不打断你问"要不要叫醒"。

与上游三段式(消息 → 回执 → 结果回原对话,`001-domain.md:7,31`)的差别在**谁是收件人**:上游有第三方提出者,所以要回执、要 Channel、"结果回到那个对话";这里提出者就是你,**回执被唤醒消息本身吸收了**,结果是 `watch_ack` 的一个标签加一条可选评论。代价:没有 per-item 的"已收到/处理中"状态,`watch_trace` 只回答"为什么没叫醒",不回答"办到哪了"。

## 5. 代价与边界

- **设计漂移是双向的**:先「不抄 Ticket」,后被真实缺口逼着补回 Ticket/Subscription/Assignment/Outbox/Admission。它没有抄错,但**文档里的边界(0.9)与代码里的边界(2.0)不是同一条**,读旧文档会误判能力。
- **一旦默认 inline,就没有审计面**:谁让它干的、按哪版规则、干到哪一步,都散落在会话历史里;上游把这些留在域内(`001-domain.md:32-36`)。
- **`worker` 模式是半成品边界**:有独立 Session 与目录,但没有 worker slot、没有 prepare 命令、没有 30 分钟后台收敛(`003-execution.md:31-45`),也没有 `dsh-superagent-worker` 预设的 5 秒转后台(`003-execution.md:27`)。
- **宿主耦合**:`engines.dsh` 钉 `>=0.2.2-rc.1 <0.3.0-0`,并用 `sessionController` / `workspaceRegistry` 的**当前形状**(`executor-host.js:40-43`);与同批的 NattoCB/dsh-plugin-superagent(未单开页)相比,两者对 `controller.create()` 的调用签名已经不同,说明这条边在 rc 之间就变过。
- **单人假设是硬边界**:没有多用户、没有身份映射、没有跨 Source 关联(`001-domain.md:39`);`allowAuthors` 只是「谁能派活」的一个过滤器,不是权限系统。
- **不能与上游并存于同一 profile 的同一职责**:两者都注册面板与工具入口,bundle id 不共享,但都要接管「仓库 → 会话」这条边;是否冲突未验证。

## 未读 / 未验证

- 未实装运行:唤醒注入、worktree 回收、`worker` 模式建会话三条链路只有代码与自述,没有真机记录。
- `docs/official-decomp/03-sources.md:4` 自述的 blob SHA 比对未复核。
- README:175 的「1420 项单测 / 41 PASS」是作者自述,我只数到 94 个测试文件 / 32,417 行。
- 与上游同 profile 共存的真实行为未验证。
