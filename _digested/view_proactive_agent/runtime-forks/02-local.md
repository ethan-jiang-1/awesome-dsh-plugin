---
kind: card
domain: proactive_agent
subcategory: runtime-forks
repo: mengzhongjie/dsh-superagent-local
commit: fe5929a5b138e0872eb2aacea7a3f270bc71aa46
evidence: 3
status: active
asof: 2026-11-25
---

# dsh-superagent-local — 把入口从"GitHub 仓库"换成"坐在这台机器前的人",代价是整树同名

> 证据等级 ★★★(源码级;`mengzhongjie/dsh-superagent-local@fe5929a`,2026-11-08)。**没有**在干净机器上装/跑,同名冲突的失败形态未实测。
> 星标/forks 为 2026-11-25 GitHub API 实时值。上游基线 `deepseek-ai/dsh-superagent-prototype@8c32a9dc`(0.1.0,schema 11)。

## 它替谁解决什么问题

**一个人,或两三个人的小组,活从自己机器的工作区来,却没有一个能派活的入口。** 他手上是编辑器里打开的一个目录和一个跑着的 DSH,没有一个"有人提 issue"的 GitHub 仓库;他想让 agent 就在这个目录里干,结果回到同一条会话。

上游的前提对他逐条不成立:

- **没有来源**:上游要仓库 + 机器人账号 + 允许名单(`docs/001-domain.md:39`),他这里没有 issue。
- **没有"原对话"**:上游的 Channel 是 issue 评论、review、群话题;他的原对话就是侧栏那条会话。
- **没有单数主会话**:上游只有一条主会话,而 DSH 用户按 workspace 组织,一个 workspace 一个项目。
- **没有仓库就不启动**:上游 `resolveDeployment` 拿不到 repository 直接抛 `repositoryUnset`(`8c32a9dc src/deployment.ts:91`)。

笨办法只有一个方向:先造一个仓库、建机器人账号、把自己写进名单,再把需求"翻译"成 issue——为了用 agent,先给 agent 造一个假的组织。

最疼的是**刚从"给仓库写代码"切到"让 agent 帮我改本地目录"的那一刻**:能力都在(评估、工单、独立 worker、回原对话),但入口、归属、落点三件事全绑在 GitHub 上。

为什么是现在:DSH 0.2 把 `session/event` 的 `user/message` 与 `workspaceRegistry` 暴露给插件,"本机操作者"才有可能作为一个 Source 存在,而不必改宿主。

## 适用面:谁该用、谁别用

**适合**:一个人(默认允许名单里只有 operator 一个身份),或共用同一台机器/同一个 profile 的两三个人;以本机目录为单位工作;能接受为它单开一个 profile(它会改进程级环境);愿意自己看 diff、能回滚。

**不适合**:要与上游 `dsh-superagent` 同 profile 并存(同包名同 id);多仓/多团队、要按仓库或按人分权限;强合规或多租户——worker 无审批、无目录隔离,两张工单会共用同一个 git index;以及"离开 DSH 也要知道进展"的人(回执与结果都在会话与面板里)。

**前置条件**:

- DSH `^0.2.1-alpha.2`(23 个 peer)、Node `^22.19.0 || >=24`;
- 一个专用 profile;`stateDir` 有默认值,但 `DSH_HOME` 非默认时附件路径会错(见代价);
- git;GitHub CLI 只在启用 GitHub Source 时需要,本地模式不需要仓库。

## 业务价值

**能算清的**:

- **派活从一串动作降到一句**:本地模式不需要建仓库、建 issue、配允许名单——在主会话里说一句就是需求;有代码兜底的是"消息即请求"这条 Trigger 构造,不是营销口径。
- **结果有落点**:每张工单有自己的一张卡,产物目录写在卡上,回执与结果回到发起的那条会话;少一次"去别处找结果"。
- **安装**:一条 `dsh plugin add github:...`(`prepare` 自动构建 `lib/`),或一个 release tarball;npm 上是 404,没有第三条路。
- **采用信号(2026-11-25 读数)**:11★ / 1 fork;唯一的 fork 作者 `limian22` 在 11-23 开了 issue #1——是"有人把它和别的插件同宿装"的实证,但量级只有这一例。

**只是预期**(推断):

- "没有 GitHub 仓库也能让 agent 干活"会扩大使用者范围;没有用户数、工单量或留存数据。
- 单开 profile 的隔离成本可能抵消一部分收益——issue #1 说明不单开就会污染同进程的其它插件。

**明确不算**:没有节省工时、没有 token 成本、没有多 workspace 并发吞吐——不做 ROI 推算。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 / 类目 | `mengzhongjie/dsh-superagent-local` / workflow([registry](../../../data/plugins/mengzhongjie__dsh-superagent-local.yml)) |
| 子分类 | `runtime-forks`(D1:整树分叉,换入口与落点) |
| 自述 | GitHub 描述:"dsh-superagent 的本地改造版:每个工作区一个主会话,需求来自本机操作者而不是 GitHub/飞书(fork of dsh-superagent)";自称 fork,但 `fork: false` |
| 星标 / fork | **11★ / 1 fork**(fork 是 `limian22/dsh-superagent-local`,即 issue #1 的作者);创建 2026-11-01,pushed 2026-11-08T11:12Z |
| 包形态 | `dsh-superagent@0.2.2`,`private: true`,MIT;**DSH bundle**:`dsh.bundle.patch` + `dsh.client`(web,6 个 client 注入);新增 `./local-watch` 导出(`package.json:19`) |
| 分发 | **npm 404**(`dsh-superagent` 与 `dsh-superagent-local` 都 404);`dsh plugin add github:mengzhongjie/dsh-superagent-local`,或 release tarball **v0.2.1**(HTTP 200) |
| 代码规模 | `src/` 115 文件(上游 111:62 个有差异、5 新增、1 删除);`tests/` **64 个 spec**(含 `dsh-source.spec.ts` 172 行、`bundle-patch.spec.ts` 73 行) |
| 宿主钉版 | **23 peer**:21 个 `@deepseek-ai/dsh-* ^0.2.1-alpha.2`、`cordis 4.0.5-alpha.1`、`schemastery 3.18.5-alpha.1`;`engines.dsh ^0.2.1-alpha.2` |
| 与上游关系 | 整树 D1:62 差异 + 5 新增 + 删 1(`client/trigger.tsx`);但 `core/` 只有 **4 个文件、17 行**差异 |
| repo@commit | `fe5929a5b138e0872eb2aacea7a3f270bc71aa46`(2026-11-08,HEAD 是侧栏动画修复) |
| 证据等级 | ★★★ |

## 它到底是什么

**一次改三格的分叉,不是"加一个渠道"。** 上游把"谁在要活"写死在平台身份里(`docs/001-domain.md:39`:人不是领域概念,允许名单按 Source 身份表达),执行目录又从"那个仓库"的 clone 里开 worktree(`docs/003-execution.md:53`)。这个 fork 把 Source、归属、落点一起换掉:

```text
Source    GitHub / 飞书           → dsh:主会话里人手输入的消息(sources/dsh.ts:307-337)
Trigger   issue 评论 / 群消息      → thread = 会话 id,channel = { sessionId }(dsh.ts:150,156)
Eval      gate 按 Source 身份准入  → gate 只认 operator,明确请求直接过(dsh.ts:249-279)
Ticket    落 work/<工单名>         → 落 trigger.meta.workspace(executor/dsh.ts:117-129)
Executor  worker-<id> + worktree  → worker-<id>,目录就是你的工作区,跳过 prepare(executor/dsh.ts:506-521)
Reply     回 issue / 群            → 回发起那条主会话(runtime.ts:232-235)
```

三件事是耦合的,**拆开任何一处都不成立**:

1. **新 Source kind `dsh`**:只听宿主事件 `session/event` 里的 `user/message`,只认"是不是主子"、只认 `source.kind === 'user'`(防自己注入的回执回环),再把工作区从会话反查出来(`src/sources/dsh.ts:307-337`);注册为"本机操作者(所有工作区)"(`dsh.ts:203-206`)。
2. **一个 workspace 一条主会话**:`KV.runtime.masters` 存 `workspaceId → sessionId`(`src/kv.ts:34-35`),按需创建,id 由工作区路径确定性推出 `orchestrator-${key(workspace.path)}`(`src/app/runtime.ts:288`);`isMaster` 从"认一条"改成"认一组"(`:236-242`),HTTP 上是 `GET /orchestrator/api/master?workspace=`(`src/app/http.ts:259-263`)。
3. **工单落在工作区目录**:对 `source === 'dsh'` 用 `trigger.meta.workspace` 当执行目录,没指定才退回 `stateDir`(`src/executor/dsh.ts:117-129`);目录已存在就**不跑 prepare**,只校验"用户指定的目录必须已存在"(`:506-521`)。

**它保留了领域模型。** Source → Eval → Ticket(+Mandate/Subscription/Assignment) → Executor → Report 全在;`core/` 只动了 17 行:`newTicket` 一根线和两个新错误码(`foreignWorkerFile`、`freshRequestEndedTicket`)。Ticket 仍"定义自己的状态、不跟随 DSH 会话",worker 会话删了工单还在。

**`newTicket` 的真实语义比名字窄。** 代码里它只做两件事:不把已结束的工单复活(`src/core/tickets.ts:262`、`src/core/engine.ts:114-119`),不折进非活工单(`src/core/intake.ts:36-45`)。注释自己把目的写成"Intake 看到这个标记就不会去复活已结束的工单"(`src/sources/dsh.ts:160-162`)。**正在跑的工单仍然接得住补的一句话**——`intake.ts:43-45` 的注释说明这是刻意的("否则你改个文件名就会多开一张单、两个 Worker 抢同一份活")。所以它是"不复活旧单",不是"每条消息必开新单"。

## 怎么接进 DSH

- **装**:`dsh plugin add github:mengzhongjie/dsh-superagent-local`(`prepare` 跑 `tsdown` 构建 `lib/`),或 `dsh plugin add <release tarball>`;没有 npm 路径。
- **patch**:`cordis.patch.yml:5-15` 插 4 条 entry——`dsh-superagent`(编排器)、`-github`、`-feishu`(默认开,缺机器人 CLI 时自报不影响别的来源)、`-dsh`(本地 Source,一个实例覆盖所有工作区);`:23,128` 两条 preset。
- **stateDir**:有默认值 `<DSH_HOME>/state/superagent`(`src/deployment.ts:17-20`),不写也能启动——但 `cordis.patch.yml:1-3` 与 `docs/006-deployment.md:105` 仍写"必填",见代价。
- **不能与上游并存**:包名同为 `dsh-superagent`(`package.json:2`),entry id 也同为 `dsh-superagent` / `-github` / `-feishu`(`cordis.patch.yml:5-13`)。一个 profile 的 `node_modules` 只能放一个同名包,一个 loader 也只能有一个同名 entry;作者的迁移路径因此是"换掉",不是"并存"。
- **主会话只路由**:router preset 里 `tool-bash` / `tool-pwsh` 被 `disabled: true`、`tool-fs` 关掉 `write`/`edit`(`cordis.patch.yml:163-174`),注释写明"没有 shell 就不能写文件,于是一个请求只能变成工单"——把提示词约束落成工具面约束。

## 关键实现

| 文件 | 作用 | 关键位置 |
|---|---|---|
| `src/sources/dsh.ts` | 本地 Source:事件→Trigger、准入、附件、回执投递 | :150-162 Trigger、:203-206 kind、:249-279 Policy、:307-337 监听 |
| `src/app/runtime.ts` | workspace→主会话的账、创建、回执归属 | :232-235 `masterOf`、:236-242 `isMaster`、:257-280 `masterFor`、:288 id、:309-320 `forgetIf` |
| `src/executor/dsh.ts` | 每张工单的目录、附件说明、会话、回流 | :117-129 目录、:141-156 附件、:494-498 `homeOf`、:506-521 跳过 prepare |
| `src/app/http.ts` | 面板/主会话查找 | `GET /orchestrator/api/master` |
| `src/client/*` | 侧栏 M 气泡、会话行隐藏、面板 v2 | `index.tsx:229-240` 按钮、`sidebar-hide.ts:1-27` 静态样式表 |
| `src/deployment.ts` | 部署与"本地模式" | :17-20 `stateDir` 默认、:103-110 `repositories: []` |

**数据流**:人在某个 workspace 的主会话里打一句话 → `session/event` → Trigger(`newTicket: true`,`meta.workspace` 由 `workspaceOf(session)` 反查)→ Intake 入库 → Eval 的 gate 按"操作者本人"直接放行 → accept 原子建 Ticket+Mandate → Executor 在**那个工作区目录**起 `worker-<id>` → 回执与结果经 `masterOf` / `homeOf` 回到发起会话;工单状态在面板上 5 秒轮询一次。

**附件走 Trigger 元数据**:`meta.attachments` 只记 id,执行器把 `~/.dsh/attachments/v1/objects/<前两位>/<id>` 写进任务说明,worker 用 `read_image` / `read` 打开(`dsh.ts:69,80-96`;`executor/dsh.ts:141-156`)。id 用正则收紧并复核拼出的路径没越出附件库——注释把理由写清了:否则消息内容能决定读取边界。

**进程级环境注入**:DSH 没有 per-session env hook,所以 `Setup.resolve()` 在写完 worker shim 后调 `applyEnvironment`,把 `PATH`(前置 `<stateDir>/worker-bin`)与 `GIT_CONFIG_GLOBAL` 等写进 **`process.env`**(`src/infra/environment.ts:149`、`src/app/setup.ts:108`)。原值先存 `<stateDir>/environment-origin.json`,停止时还原;`docs/006-deployment.md:5-16` 自己承认"同一宿主的其它会话也会看到这些变量",并把"专用 profile"列为隔离手段。

**竞态处理**:同一 workspace 的并发点击共用一次创建(`spawning`,`runtime.ts:257-266`);`remember` 排在 `ensure` 之前,因为建会话会立刻触发 `agent/created → decorate`,那一刻必须已认得出它是主子(`:285-292`);失败只回滚"映射仍指向这条会话"的那次(`forgetIf`,`:309-320`),且只把 `unknown session` 这类错误当"会话不在了",其余按临时故障。

**界面是 DOM 注入,不是插槽**:`ui-workspace` 把侧栏声明成 single 独占插槽、组标题行没有子插槽,只能用 `data-row-key^="workspace:"` 当锚点(`client/index.tsx:74-76`);入口是一枚圆形 **M** 气泡(`:229-240`)。插件自建会话的行用**静态样式表**收起,因为宿主侧栏用 FLIP 动画,事后写行内 `display:none` 会让下方那组先弹一下(`src/client/sidebar-hide.ts:1-27`)。

## 为什么它突出

- **最硬的证据不是星标,是一条没人回的 issue。** #1(2026-11-23,`limian22`,0 回复):在同一个 DSH Web 宿主里同时装本插件与 GitHub Forge,worker 的 `gh` shim 抢在宿主 CLI 前面,报 `gh is unavailable: this installation names no GitHub repository.`,Forge 读不到 PR 状态;issue 明说 `main@fe5929a` 同样存在,并指到 `Setup.resolve()` 调 `applyEnvironment()`。**这是"有人真把它和别的插件同装"的实证**,比 11★ 更能说明它在被使用。
- **改造是"换坐标系",不是"改参数"**:62 个文件差异,却只碰 `core/` 17 行——入口、归属、落点三处全在 app/executor/sources,授权模型一行没重写。这是整树分叉里少见的克制:改部署面而保留裁定面。
- **它把"没有仓库"变成稳态而不是报错**:`resolveDeployment` 在没有 GitHub 仓库时返回空 `repositories` 继续跑(`deployment.ts:103-110`),GitHub Source 报 `paused` + `localMode`、并在 healthCodes 里声明成稳态(`src/sources/github.ts:43,79,160`),面板显示"本地模式"而不是 setup 失败。
- **有测试兜底**:64 个 spec,新增 `dsh-source.spec.ts` 专测 Source,`bundle-patch.spec.ts` 校验 patch 里的 entry 与包名一致;但没看到按平台分支的测试,Windows 行为未验证。
- **分发面只有一条窄路**:npm 404,README 指向的 tarball 还停在 v0.2.1,而包是 0.2.2——安装者必须先看清版本。

## 代价与边界

1. **不能与上游并存**:同包名 + 同 entry id。一个 profile `node_modules` 只能有一个 `dsh-superagent`,loader 也只能有一个同名 entry;确切失败形态(拒绝启动还是后者覆盖)未验证。
2. **基点对不上公开上游**:CHANGELOG 说"相对上游 0.1.0"(`CHANGELOG.md:3`),树里却是 0.2.x 一代——schema **12** 多仓迁移(`src/app/migration.ts:20,598`)、`repositories: []` 建模、面板 v2;公开 `main` 的 HEAD 仍是 0.1.0/schema 11(`8c32a9dc`)。**这棵树没有可对齐的公开前身**,62 个差异里哪些是作者改的、哪些是基点自带的,从克隆里分不出来。
3. **没有目录隔离**:工单直接在你自己的工作区跑,并发两张单共享同一个 git index 与分支;`workspaceOf`/`launch`/`ticketExecution` 里未看到按目录串行化的代码。跳过 prepare 换来"产物就在你打开的目录里",也换来"未提交改动没有护栏"。
4. **进程级环境注入是宿主级副作用**:`applyEnvironment` 改 `process.env`,issue #1 是实测后果。缓解只有"专用 profile"——README/SETUP 确实要求建独立 `superagent` profile,但插件本身不强制,装在常用 profile 里就会污染同进程的其它插件。
5. **附件根写死 `~/.dsh`**(`dsh.ts:69`),与它自己的 `DSH_HOME` 感知(`deployment.ts:17-19`)不一致;`DSH_HOME` 被改过的机器上,worker 拿到的是不存在的路径。
6. **评估层被短路**:操作者消息一律 `human: true`、`addressed: 'direct'`,策略文案写"一律是明确的请求"(`dsh.ts:150-153,269-272`),gate 基本直接放行;`threadContext.read()` 返回空(`:236-242`),`messageText` 只拼 `text` 块(`:45-47`)——评估看不到图片与会话历史,纯附件消息靠占位文本占正文。
7. **一个 Source 覆盖所有工作区**(`cordis.patch.yml:13-15`):省了逐项目配置,换来面板上看不出哪些工作区被覆盖、也无法按工作区分别准入。
8. **文档与代码漂移**:README 说入口是"星形按钮"(`README.md:20`),代码画的是 **M** 气泡(`client/index.tsx:234`);`cordis.patch.yml:1-3` 与 `docs/006-deployment.md:105` 仍说 `stateDir` 必填;`SETUP.md:38` 还在问"哪个 github.com 仓库"、`:55` 还在教建独立 profile;README 的 tarball 链接停在 v0.2.1(`README.md:44`)。
9. **界面建在宿主 DOM 形状上**:单一独占插槽、`data-row-key` 锚点、FLIP 动画——这些都是宿主实现细节,不是契约,升级就可能断。
10. **单维护者 + 无回流**:没有 upstream remote 或 sync 脚本,上游一改只能整树读;上游仓 `has_issues: false`,这些改动没有回流通道。

## 可信度与复现

**读过**:`README.md`、`CHANGELOG.md`、`SETUP.md`、`docs/001`~`007` 与 `ui-redesign-v2.md`、`package.json`、`cordis.patch.yml`,以及 `src/sources/dsh.ts`、`src/app/{runtime,sessions,http,setup,migration}.ts`、`src/core/{intake,engine,tickets,errors}.ts`、`src/executor/dsh.ts`、`src/deployment.ts`、`src/kv.ts`、`src/infra/environment.ts`、`src/client/{index.tsx,sidebar-hide.ts}`。
**比过**:与上游 `8c32a9dc` 做全量文件集与逐字节比较(111→115,62 差异/5 新增/1 删,`core/` 17 行);数了 spec(64)与 peer(23);查了 npm(404×2)、release tarball(200)、issue #1 原文。
**没做**:干净机器安装/运行、同名冲突实测、多 workspace 并发 relay、`DSH_HOME` 迁移后的附件行为、Windows 上的测试通过率。

```sh
git clone https://github.com/mengzhongjie/dsh-superagent-local && cd dsh-superagent-local
git checkout fe5929a
diff -rq /path/to/upstream/src src | wc -l            # → 68(62 差异 + 5 新增 + 1 删除)
find tests -name '*.spec.ts*' | wc -l                # → 64
grep -n "masters\|newTicket" src/kv.ts src/core/intake.ts src/core/tickets.ts
curl -s -o /dev/null -w '%{http_code}\n' https://registry.npmjs.org/dsh-superagent          # → 404
curl -s https://api.github.com/repos/mengzhongjie/dsh-superagent-local/issues/1 | grep -m1 '"title"'
```

## 待验证

1. **同名冲突的确切形态**:同 profile 挂上游与本插件,是 loader 拒绝启动、还是后者覆盖前者;`dsh-superagent` 包名与 entry id 双重撞车时哪一层先报错。
2. **同一目录并发两张工单**:共享 git index 时是否出现 `index.lock` 冲突或分支互踩;`workspaceOf`/`launch` 没有串行化代码,需要真跑两个需求验证。
3. **`DSH_HOME` 非默认时的附件链路**:`ATTACHMENTS_ROOT` 写死 `~/.dsh`,worker 打开附件是否会拿到不存在路径。
4. **0.2.x 那一代是基点自带还是作者所写**:schema 12、多仓、面板 v2 在公开仓找不到前身,只能逐文件读;未做。
5. **issue #1 是否只在 Windows 复现**:`applyEnvironment` 在 POSIX 上也前置 `worker-bin`,同一个 `gh` 遮蔽是否同样发生,未验证。
6. **测试在 Windows 上的真实通过率**:上游 `docs/003` 的 shell/prepare 语义假设 POSIX,本仓测试未做平台分支。
7. **与其它吃 `orchestrator` 服务/`stateDir` 的插件共存**:本插件用一个 Source 实例覆盖所有工作区,别的插件若也注册 Source 或读写同一 KV,边界未验证。

→ 同层其它成员与读法:[runtime-forks/README.md](README.md);逐行材料:[FAQ 深读](../../../_faq_on_digested/02_superagent-dependents/lines/02-local-fork.md)。
