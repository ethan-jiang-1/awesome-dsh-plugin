# mengzhongjie/dsh-superagent-local — 把"一个 GitHub 仓库"换成"坐在这台机器前的人"

> `repo@fe5929a`(2026-11-08 19:12 +0800;11★ / 1 fork,pushed 2026-11-08)。上游 `deepseek-ai/dsh-superagent-prototype@8c32a9dc`(`dsh-superagent@0.1.0`,24,570★ / 3,081 forks,API 2026-11-25)。注册表条目 [`mengzhongjie__dsh-superagent-local.yml`](../../../data/plugins/mengzhongjie__dsh-superagent-local.yml),类目 workflow。证据等级 ★★★(README、CHANGELOG、SETUP、`docs/`、`package.json`、`cordis.patch.yml` 与 `src/` 关键模块都读过;**没有**实装运行)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 / 类目 | mengzhongjie/dsh-superagent-local / workflow |
| 声量 | 11★ / 1 fork,pushed 2026-11-08(实时值,非冻结边车) |
| repo@commit | `fe5929a`,HEAD 提交是"插件自建会话改用静态样式表收起" |
| 包形态 | `dsh-superagent@0.2.2`,`private: true`,MIT;DSH bundle(`dsh.bundle.patch` + `dsh.client` web);新增 `./local-watch` 导出(`package.json:19`) |
| 分发 | 不发 npm(`dsh-superagent-local` 在 npm 是 404);`dsh plugin add github:mengzhongjie/dsh-superagent-local`,或 release tarball `v0.2.1`(HTTP 200) |
| 宿主钉版 | 23 个 peer `^0.2.1-alpha.2`,`cordis 4.0.5-alpha.1`;`engines.dsh` 同范围(`package.json:56-88`) |
| 与上游的关系 | 整树 D1:上游 111 个 `src` 文件里 62 个有差异、新增 5 个、删 1 个;但 `core/` 只有 4 个文件、不到 20 行差异(见第 5 节第 2 条) |
| 复现 | `git clone https://github.com/mengzhongjie/dsh-superagent-local && git checkout fe5929a` |

## 影响力

- 数字(GitHub API,2026-11-25):**11★ / 1 fork / 0 watcher**;2026-11-01 创建,最后 push 2026-11-08T11:12Z;topics 为 `deepseek-harness`、`dsh-plugin`。
- 分发:**没有 npm**——`dsh-superagent-local` 与包名 `dsh-superagent` 在 registry 都是 404;只能 `dsh plugin add github:…` 或用 release tarball `v0.2.1`(HTTP 200)。注册表收录在 [`mengzhongjie__dsh-superagent-local.yml`](../../../data/plugins/mengzhongjie__dsh-superagent-local.yml),条目直接带 tarball 字段。
- **被使用的证据**有两个,都比星标硬:唯一的 fork `limian22/dsh-superagent-local`(0★,pushed 2026-11-23);以及这个 fork 的人在 2026-11-23 开的 issue #1——"Superagent Local 0.2.1 on Windows, loaded in a DSH host alongside the GitHub Forge plugin… the same process-wide environment update is present on main at `fe5929a`",报告 worker 的 CLI 环境遮蔽宿主 `gh`、打断 Forge 的 PR 状态查询。issue 至今 0 回复。
- 被引用/被抄:除这一支,**未见**其它仓库引用、下游依赖或安装量证据(没发 npm,注册表也不统计安装)。
- 在注册表里的位置:它是 6 个 D1 代码级依赖之一,也是其中**第二高星**的分叉(138★ 的 HiSeax 之后、10★ 的 Nelson 之前);条目带 `tarball` 字段,比其它分叉多一条"直接下载"的入口。
- 判断:**不算有影响,但算"有人在用"**。11★ 在这批分叉里排第二(仅次于 HiSeax 的 138),但它的目标读者是"没有 GitHub 仓库的 DSH 用户",这批人不在 GitHub 上发声;真正的信号是那条 issue:有人把它和另一个插件装在同一个宿主里,并被进程级环境注入打到。

## 1. 它要解决什么问题

上游把"谁在要活"写死在平台身份里。`docs/001-domain.md:39` 说得很直白:人不是领域概念,允许名单是"Source 的那一部分 Policy",而且**按该 Source 自己的身份**表达。于是整个授权链的前提是:有人拿 GitHub 账号在 issue 里 @ 机器人,或拿飞书账号在群里说话;执行器再从"那个仓库"的 clone 里开 `git worktree`(`docs/003-execution.md:53`)。

坐在机器前的人不满足这个前提,而且是逐条不满足:

- **没有来源**。他有的是编辑器里打开的一个目录,不是 issue。想派活只能先造一个仓库、再造一个机器人账号、再把自己写进允许名单。
- **没有"原对话"**。上游的 Channel 是 issue 评论、review 讨论、飞书话题(`docs/001-domain.md:71`)。本机操作的"原对话"就是侧栏里的那条会话。
- **没有单数的主会话**。上游只有一条主 Session:`KV.runtime.masterId`,`orchestrator-<stateDir 的 hash>`(`src/app/runtime.ts:120`)。DSH 的用户却按 workspace 组织,一个 workspace 一个项目;上游这条假设直接和宿主的侧栏结构冲突。
- **没有仓库时它根本不启动**。上游 `resolveDeployment` 拿不到 repository 就 `throw new SetupError('repositoryUnset')`(`upstream src/deployment.ts:90`),整块部署检查不过,面板只会显示"缺仓库"。

所以痛点的形状是:能力都在(评估、工单、独立 worker 会话、回原对话),但入口、归属和落点三件事全部绑在 GitHub 上。这个 fork 把这三件事一起换掉,而不是加一个渠道。

在上游管线上,替换点可以一格一格指出来:

```text
Source       GitHub / 飞书          →  dsh:主会话里人手输入的消息(sources/dsh.ts:307-317)
Trigger      issue 评论/群消息       →  thread = 会话 id,channel = { sessionId }(sources/dsh.ts:150,156)
Eval         gate 按 Source 身份准入 →  gate 只认 operator,明确请求直接过(sources/dsh.ts:249-279)
Ticket       落 work/<工单名>        →  落 trigger.meta.workspace(executor/dsh.ts:123-129)
Executor     worker-<id> + git worktree → worker-<id>,目录就是你的工作区,不 prepare(executor/dsh.ts:508-518)
Reply        回 issue/群             →  回发起那条主会话(runtime.ts:232-235)
```

## 2. 它的路径

三处改动是耦合的,拆开任何一处都不成立:

1. **新的 Source kind `dsh`**:`src/sources/dsh.ts`,注册为"本机操作者(所有工作区)"(`dsh.ts:203-206`)。它不听网络,只听宿主事件 `session/event` 里的 `user/message`(`dsh.ts:307-317`);Trigger 的 thread 就是会话本身、Channel 地址就是 `{ sessionId }`(`dsh.ts:150,156`),于是"回原对话"变成"回这条主会话"。
2. **一个 workspace 一条主会话**:`KV.runtime.masters` 存 `workspaceId → sessionId`(`src/kv.ts:34-35`),`masterFor(workspaceId)` 按需创建,会话 id 由工作区路径确定性地推出来:`orchestrator-${key(workspace.path)}`(`runtime.ts:288`);HTTP 上是 `GET /orchestrator/api/master?workspace=`(`src/app/http.ts:259-263`)。上游的 `isMaster` 只认一条,这里改成"认一组"(`runtime.ts:236-242`)。
3. **工单落在工作区目录、且一条需求一张单**:`ticketExecution` 对 `source === 'dsh'` 用 `trigger.meta.workspace` 当执行目录,没指定才退回默认(`src/executor/dsh.ts:117-129,157`);Trigger 带 `meta.newTicket: true`(`dsh.ts:162`),Intake 见到它**只阻止复活已结束的工单**,正在跑的工单仍接得住补充消息(`src/core/intake.ts:36-45`,注释明说这是刻意的;`engine.ts:114-119`、`tickets.ts:262`)。

**放弃了什么**:一是"直接用上游"——不行,不是因为不好用,而是因为上游的 gate 只认 Source 身份、执行目录由 `work/<工单名>` 决定(`docs/003-execution.md:25`)、主会话是单例,三件事分别落在 domain/app、executor、runtime 三处,配置文件改不动。二是"只写一个 Source 插件"(D2 那条路)——Source 契约能声明的只有配置、scope、policy、channel、threadContext 与 execution 变量(`src/sources/kind.ts`,例如 environment 在 `:140-141`),它能造 Trigger,但决定不了"哪条会话是主会话""工单在哪个目录跑""这条消息要不要另开一张单"。所以它必须动 app 与 executor,分叉是必然的,不是图省事。

## 3. 它如何利用 dsh-superagent

- **原样保留的是领域模型**:Source → Trigger → Thread → Eval → Ticket(+Mandate/Subscription/Assignment) → Executor → Report 全部沿用;`core/` 只多了 `newTicket` 这一根线和两个新错误码(`src/core/errors.ts` 的 `foreignWorkerFile`、`freshRequestEndedTicket`)。Ticket 仍然"定义自己的状态、不跟随 DSH 会话"(`docs/001-domain.md:35`),所以 worker 会话被删掉后工单还在。
- **复用 Executor 的既有约定**:一条工单仍然一个 `worker-<ticketId>` 会话(`src/executor/dsh.ts:25`),仍然在 router/worker 两套 preset 下跑(`cordis.patch.yml:23-127` 与 `:128-197`;常量见 `src/app/sessions.ts:50`)。只是 preset 的选择条件从"是不是那唯一的主子"改成"是不是某一主子"(`sessions.ts:131`)。
- **Policy 仍然在域内**:新 Source 声明 `policy.allowed`,默认 `[{ id: 'operator' }]`,准入表只有一行"操作者本人,总是接收"(`dsh.ts:249-279`)。授权没有被绕开,只是身份从平台账号退化成"跑这个宿主进程的 OS 用户"。
- **附件走 Trigger 元数据**:`meta.attachments` 记 id,执行器把 `~/.dsh/attachments/v1/objects/<前两位>/<id>` 写进任务说明(`dsh.ts:55-96`、`executor/dsh.ts:141-156`),worker 用 `read_image` 打开。附件 id 用正则收紧、并复核拼出的路径没有越出附件库(`dsh.ts:80-96`),注释把理由写清楚了:否则消息内容能决定读取边界。
- **回执路由改成"从哪来回哪去"**:`masterOf(trigger)` 对 `dsh` 来源取 thread id、否则退回默认主子(`runtime.ts:232-235`);执行器的 `homeOf(ticketId)` 同理(`executor/dsh.ts:494-498`);`relay`/`notice` 的载荷因此带上 `sessionId`(`CHANGELOG.md:54-57`)。
- **把"没有仓库"变成一种稳态**。上游遇到空仓库是 setup 失败;这里 `resolveDeployment` 返回空 `repositories` 继续跑(`deployment.ts:103-110`),GitHub 来源上报 `paused` + `localMode`,并在 healthCodes 里把该码声明成 `steady`(`src/sources/github.ts:43,79,159-160`),这样面板显示"本地模式"而不是"正在启动/出错"。这是它改得最像上游的一处:新状态不是靠特判,而是靠 Source 自己声明生命周期语义。
- **Policy 层的两处小改**:本地来源必须已注册且实际启用,残留配置或空名单不能证明可用(`src/policy.ts:137-140`);成员身份来自部署本身,不需要操作者先把自己写进名单(`policy.ts:122-126`)。

## 4. 技术思考

**状态放哪。** 没有新建库:workspace 到主会话的映射就存在原来的 `orchestrator.sqlite` KV 里(`kv.ts:34-35`),重启后从 KV 恢复(`runtime.ts:120-122`),和工单、触发器同一个事务边界。这比另起一份 `masters.json` 稳:不会出现"工单在、主子没了"的半状态。

**会话怎么隔离。** 主会话与 worker 会话是同一进程里的不同 DSH 会话,不隔离进程;隔离靠 preset 与工具面:router preset 里 `tool-bash`/`tool-pwsh` 被 `disabled: true`、`tool-fs` 关掉 `write`/`edit`(`cordis.patch.yml:160-172`),注释写明"没有 shell 就不能写文件,于是一个请求只能变成工单"。worker 则拿到 shell 与 fs。这条设计把"主会话只路由"从提示词约束变成了工具面约束。

**目录怎么隔离——它选择不隔离。** 本地工单直接落在操作者自己的工作区(`executor/dsh.ts:123-129`),而且**跳过 prepare**:目录已存在就不跑 prepare 命令(`executor/dsh.ts:508-518`),只校验"用户指定的目录必须已存在",免得拼错的路径被当成新项目建出来。换来的是"产物就在你打开的目录里",代价见下一节。

**并发与竞态。** 建主子会话有三道防重复:`spawning` 让同一 workspace 的并发点击共用一次创建(`runtime.ts:92,257-266`);`remember` 排在 `ensure` 之前,因为建会话会立刻触发 `agent/created → decorate`,那一刻必须已经认得出它是主子(`runtime.ts:285-292`);失败时只在映射仍指向这条会话时回滚(`forgetIf`,`runtime.ts:308-320`),并且只对"会话不在了"这类错误重建,投递超时/宿主忙一律按临时故障(`missingSession`,`runtime.ts:48-50`)。

**失败收敛。** 本地 Source 的摄取失败只记 `logger.warn`,不打断会话,也不指望"下一条消息当重试"(`dsh.ts:340-343`);附件 id 不合法直接丢,不让脏记录把整张工单在接单阶段打挂(`executor/dsh.ts:145-147`)。

**被测试钉住的部分。** 仓库有 64 个 `tests/*.spec.ts(x)`,和上游同一套骨架;新增的 `tests/dsh-source.spec.ts`(172 行)专测 Source,`tests/bundle-patch.spec.ts` 校验 patch 里插的 entry 与包名一致。也就是说这类分叉的"证据等级"不只看 README:patch、Source、迁移都有测试兜着。但测试全部跑在 POSIX 假设下(上游 `docs/003` 的 shell/prepare 语义),Windows 上的行为本页未验证。

**宿主兼容。** 侧栏那条入口是 DOM 注入,不是插槽:`ui-workspace` 把侧栏声明成 single 独占插槽、组标题行没有子插槽(`src/client/index.tsx:72-76`),只能用 `data-row-key^="workspace:"` 当锚点,还要兼容主题插件打的 `data-dsh-claude-part~="row-actions"`(`index.tsx:176-179`)。更麻烦的是宿主的 FLIP 动画:事后写行内 `display:none` 会让下方那组先弹一下,所以改成静态样式表在首次布局前生效(`src/client/sidebar-hide.ts:1-27`、`client/index.tsx:270-275`)。这两处说明一件事:**它把产品体验建在宿主 DOM 的形状上**,而宿主 DOM 不是契约。

## 界面体验

- **入口**:侧栏每个 workspace 组行的动作区里一枚圆形 **M** 气泡(`src/client/index.tsx:51,236`),悬停显形、点击打开该 workspace 的主会话(`:122-129`);README 叫它"星形按钮"(`README.md:20`),实际是 M。没有 workspace 就没有入口。
- **会话**:主会话靠一条固定开场白出现在侧栏——"（就绪）这里是 dsh-superagent 的主会话…"(`src/app/runtime.ts:43-52`),因为 DSH 只列有过消息的会话;`worker-*` 与 `orchestrator-*` 行被静态样式表收起(`src/client/sidebar-hide.ts:18-25`),状态目录那个伪工作区行按标题 `superagent` 收起(`index.tsx:156-160`)。
- **面板**:沿用上游 v2 面板——概览 / 评估 / 执行 / 设置(外加 Settings › Logs);本机来源没有独立页签,只在"设置 › 来源"里有一张卡。概览首屏依次是待处理工单、系统问题、每个来源一行状态、24 小时流量、执行器负载(`src/client/overview.tsx:125-170`)。
- **密度与实时性**:面板每 5 秒拉一次 `GET state`,重启中改 1 秒(`src/client/provider.tsx:74,89`);侧栏靠 DOM 观察者,主会话名单 3 秒节流(`index.tsx:163-165`)。工单状态最多晚 5 秒,新主子出现最多晚 3 秒。
- **失败时看到什么**:四态(错误/加载/空/内容)统一由 `ListSection` 渲染,错误带"重试"(`src/client/widgets.tsx:149-150,173-183`);工单等人回答时是一张 banner 加渠道回链(`src/client/ticket.tsx:198-203`);侧栏取不到名单就退化成"只有面板、没有入口"(`index.tsx:85`)。
- **终端**:worker 在独立会话里跑,人可以直接进会话插话,也能从工单行打开它(`src/client/rows.tsx:43,45`)——"能看着它干"这条是面板替代不了的。

## 用户交互的思路

- **谁发起**:操作者本人在某个 workspace 的主会话里直接说需求,不建 issue、不填表单(`src/sources/dsh.ts:307-337`)。
- **在哪确认**:没有"提交"这一步,消息即请求;确认发生在接单之后——看工单卡片或工单页(`src/client/ticket.tsx:191-205`),卡片带 `workspace` 字段说明产物目录(`CHANGELOG.md:54-57`)。
- **怎么观察**:三条并行——面板(5 秒轮询)、工单详情、worker 会话本身;结果同时回到发起它的主会话(`runtime.ts:232-235`)。
- **怎么打断**:工单页的危险区有 stop 与 retry(都带确认框,`ticket.tsx:263-266`、`:173-175`);更直接的是进 worker 会话说话;全局还有"暂停处理"。
- **与上游的差异**:上游是"消息 → 回执 → 结果回原对话",三段都在外部渠道,人被 IM 通知驱动;本地版把三段全搬进 DSH——发起在主会话、回执回主会话、结果看面板。好处是不用切应用,代价是**离开 DSH 就不知道进展**。
- 一句话:**它把 Super-agent 从"团队 IM 里的同事"变成"你工位上的助手"**。上游那套"异步把人拉回来"的拉力,在这里换成了"人本来就坐在旁边"。

## 5. 代价与边界

1. **不能与上游并存**。包名同为 `dsh-superagent`(`package.json:2`),挂载的 entry id 也同为 `dsh-superagent`、`-github`、`-feishu`(`cordis.patch.yml:5-13`),本地再插一个 `dsh-superagent-dsh`(`:13-15`)。一个 profile 的 `node_modules` 只能放一个同名包,一个 loader 也只能有一个同名 entry;注册表条目把这句话写进了描述。作者自己的迁移路径也因此是"换掉",不是"并存"。
2. **基点对不上公开上游**。CHANGELOG 说"相对上游 0.1.0"(`CHANGELOG.md:3`),但树里是 0.2.x 的一代:`migration.ts` 有 schema 12 的多仓迁移(`:20,598`),`deployment.ts` 已经按 `repositories: []` 多仓建模(`:103-110`),面板是 v2(带 `views/logs.ts`、`Settings › Logs`,见 `docs/ui-redesign-v2.md`)。公开仓 `main` 只有一个 0.1.0 的提交(`git ls-remote` 只有 `8c32a9dc`)。结论:**这棵树没有可对齐的公开前身**,62 个差异文件里哪些是作者改的、哪些是基点自带的,从克隆里分不出来。想跟上游同步只能人工读。
3. **文档与代码漂移**。README 说侧栏入口是"星形按钮"(`README.md:20`),代码画的是一枚 M 气泡(`client/index.tsx:234-236`);`cordis.patch.yml:1-3` 与 `docs/006-deployment.md:105` 仍说 `stateDir` 必填,代码其实已给默认值 `<DSH_HOME>/state/superagent`(`deployment.ts:16-20`)——同一件事,`03-desktop` 当成卖点,这里当成了没写进 CHANGELOG 的顺带改动(对比 `CHANGELOG.md` 连一次侧栏动画都记);`SETUP.md:38` 还在问"哪个 github.com 仓库",`:55` 还在教建独立 `superagent` profile,tarball 链接停在 `v0.2.1` 而包是 `0.2.2`(`README.md:44`)。
4. **没有目录隔离 = 你的未提交改动的爆炸半径**。上游至少从克隆里开 worktree(`docs/003-execution.md:53`);本机模式直接在你自己目录里跑,两个工单并发时共享同一个 git index 与分支。读到 `workspaceOf`/`launch`/`ticketExecution`,**没有**按目录串行化的代码。worker 以你的 OS 用户执行命令、无审批(`docs/003-execution.md:27`),`blockedCommands` 只是 `worker-bin` 里的同名 shim,按绝对路径仍可绕过(`docs/003-execution.md:80`)。同一件事在宿主层更明显:`applyEnvironment` 把 `PATH`/`GIT_CONFIG_GLOBAL` 写进 `process.env`(本仓 `docs/006-deployment.md` 新增的 "The worker environment" 一节),issue #1 正是这条的实测——worker 的 `gh` shim 遮蔽了宿主 CLI,GitHub Forge 插件的 PR 状态因此查不到。
5. **附件路径写死 `~/.dsh`**(`src/sources/dsh.ts:69`),与它自己的 `DSH_HOME` 感知(`deployment.ts:16-17`)不一致;`DSH_HOME` 被改过的机器上,worker 拿到的是不存在的路径。
6. **评估层被短路**。操作者消息一律 `human: true`、`addressed: 'direct'`,策略文案写"一律是明确的请求"(`dsh.ts:150-153,269-272`),于是 gate 基本直接放行、模型研判很少参与。省下的是钱和延迟,丢掉的是上游那套"从噪声里推断该不该做"的能力。
7. **线程上下文是空的**。`threadContext.read()` 第一版直接返回空(`dsh.ts:236-242`),`messageText` 也只拼 `text` 块(`:45-47`),所以评估看不到图片、看不到会话历史;纯附件消息靠占位文本占住正文(`:321-325`)。
8. **一个 Source 实例覆盖所有工作区**(`cordis.patch.yml:13-15`),所以工作区不是 Source 配置、而是 Trigger 元数据。换来的是"不用给每个项目配一遍来源";代价是面板上看不出"哪些工作区被覆盖",也没法按工作区分开准入——台账里只有一条 Source。
9. **单维护者 + 无 upstream remote**。11★、1 fork;仓库没有 upstream remote 或 sync 脚本,上游一改只能整树读。上游仓 `has_issues: false`(GitHub API,2026-11-25),这些改动也没有回流通道。

## 证据与未验证

**读过**:`README.md`、`CHANGELOG.md`、`SETUP.md`、`docs/001`~`007` 与 `docs/ui-redesign-v2.md`、`package.json`、`cordis.patch.yml`、`examples/profile.cordis.patch.yml`,以及 `src/sources/dsh.ts`、`src/app/runtime.ts`、`src/app/sessions.ts`、`src/app/http.ts`、`src/core/{intake,engine,tickets}.ts`、`src/executor/dsh.ts`、`src/deployment.ts`、`src/kv.ts`、`src/client/index.tsx`、`src/client/sidebar-hide.ts`。与上游 `8c32a9dc` 做了文件级 `diff -rq` 与抽样逐行 diff;数了 peer 数量(23);查了 npm(`dsh-superagent-local` 404)与 release tarball(200)。

**没做**:没有在干净机器上装/跑;**没有**验证两个同名 entry 在同一个 profile 里的确切失败形态(拒绝启动、还是后者覆盖前者),只知道包名与 id 都撞;没有验证多 workspace 并发时的 relay 顺序;没有验证 `DSH_HOME` 迁移后的附件行为;没有逐行核对"schema 12/面板 v2 是基点自带还是作者所写"——只核到公开仓没有前身。**未验证**项按上文标注,不用"应该/大概"补齐。

**复现**:

```sh
git clone https://github.com/mengzhongjie/dsh-superagent-local && cd dsh-superagent-local
git checkout fe5929a
diff -rq /path/to/upstream/src src | wc -l        # 68 行(62 差异 + 5 新增 + 1 删除)
grep -n "masters\|newTicket\|local-watch" src/kv.ts src/core/intake.ts package.json
```
