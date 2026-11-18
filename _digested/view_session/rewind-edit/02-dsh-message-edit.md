# dsh-message-edit — 每次编辑都分叉出一个真实会话,版本树是 DSH 谱系的读时投影

> 证据等级:★★★(源码级;`Moeblack/dsh-message-edit@b78a167064ca612f1c400060d2bfc1dc9bc46436`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 32 为 2026-08-19 历史采样;下载 1250 同为该日;2026-11-18 实时星标 56。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `Moeblack/dsh-message-edit`([registry](../../../data/plugins/Moeblack__dsh-message-edit.yml)) |
| 类目 | session([census](../../ecosystem/census.py) 914 条 / 全表 11 744 条) |
| 子分类 | `rewind-edit`(回退与编辑) |
| 状态 | ⚠ **停更**:最后 push 2026-08-16、0 测试;0.2.1-rc.5 上 3 处疑似不兼容。**不建议新装**,保留作"消息级分支"机制参考。 |
| 自述 | 「基于分支的消息编辑、reroll、重试与版本时间线」;英文原文为 branch-based message editing + reroll + retry + version timeline |
| 星标 ⚠ | **32**(2026-08-19 边车);2026-11-18 实时 **56**(+24,同日 GitHub API) |
| 下载 ⚠ | **1250**(2026-08-19 边车;与星标同日采样) |
| 扩散 | **3** 个第三方条目引用它:2 个明示代码谱系的 fork + 1 个 vendor 集成;另 1 个同名独立实现不计(口径与命令见「为什么它突出」) |
| 仓库 commit | `b78a167064ca612f1c400060d2bfc1dc9bc46436`(2026-08-16,`main`,`性能修复: timeline 按需分层读取 + 客户端刷新风暴治理 (v0.2.3)`) |
| 包形态 | npm `dsh-message-edit@0.2.3`;Cordis **bundle**(`dsh.bundle.patch`)+ Web client bundle(`dsh.client`),单包,无原生依赖、无外部服务 |
| 代码规模 | `src/**/*.{ts,tsx}` **2 292 行**(host 1 026 / browser 1 266);CSS Modules 717 行;构建脚本 206 行;**测试文件 0 个、无 test 脚本** |
| 仓库体量 | 23 个跟踪文件;GitHub `size` **230 KB**;24 forks / 21 open issues(2026-11-18 API);仓库创建 2026-08-06,最后 push 2026-08-16 |

## 它到底是什么

**它不是消息重写器,而是一个会话分叉器 + 版本注记层。** 形态上它是 DSH 原生双端插件:host 半是 Cordis plugin(`src/index.ts`),浏览器半是 UI bundle(`src/client/`),通过 `dsh.bundle.patch` 与 `dsh.client` 两个 manifest 键接入(`package.json:20-32`);不是 MCP 配置包,也不是对某个外部记忆/检索系统的适配层。

### 数据模型:版本 = 一个真实的子 Session

这是它最核心的设计,也是本卡要回答的第一个问题:

| 概念 | 存在哪 | 源码 |
|---|---|---|
| 一个「版本」 | 一个**新的 DSH Session**(子会话),不是源会话里的一条记录 | `src/index.ts:513-524` |
| 版本树的边 | 子会话 header 的 `parentSession` 指向源会话 | `src/index.ts:516-521`;`src/index.ts:598-608` |
| 分支历史 | 源会话日志到目标回合 `turn/start` 之前的前缀,作为 `seed` 传入 | `src/index.ts:430-437`、`477-486` |
| 版本效果 | 子会话**自己**的日志段里最多一个 `message-edit/version` 事件(插件创建的分支恰好一个) | `src/shared.ts:20-43`;`src/index.ts:483`、`589-595` |
| 效果/逆 | 同一事件里 `effect`(正向,带 UUID、operation、cascade、目标 turn/seq/block、before/after)与 `inverse`(`restore-version` + 源 sessionId)成对 | `src/shared.ts:20-43`;`src/index.ts:143-152` |
| 继承边界 | 子会话头里的 `seedLength`:区分「自己写的版本事件」与「从祖先继承的同名事件」 | `src/index.ts:588-591`、`693-698` |
| 版本树本身 | **不单独存储**,读时由 `ctx.sessionQuery.traceSession()` + `parentSession` 链重建 | `src/index.ts:701-777` |
| 撤销/重做 | 同样是投影:`undoStack` 沿 inverse 链向上,`redoSessionIds` 是直接子效果 | `src/index.ts:752-763` |

也就是说:**源会话的消息历史没有被改写**。每次「编辑 / reroll / 重试」都是 `ctx.agents.create({ seed, meta })` 创建一个子会话,子会话在内存中的 append-only 日志 = 源前缀的副本 + 一个版本事件(+ 助手块编辑时一个手工回合),宿主还会在 seed 末尾补一个 `session/end-seed` 标记(`dsh-session/lib/index.js:1427-1428`);源消息日志保持原样。这既不是「重写日志」,也不是「只改 UI 视图」,而是**会话级影子分支**。

插件把 `seedLength` 放进子会话 `meta`(`src/index.ts:518-520`),意图是让子会话头记录继承前缀;本机 DSH 的等价语义见 `dsh-session-log-deepseek/lib/index.js:33` 与 `dsh-session-persistence-jsonl/lib/index.js:813-823`、`2927-2930`。这条契约在当前宿主上是否仍成立,见「代价与边界」第 1 条。

### 回合原子性:整个 turn 是效果单位

`closedTurns()` 只认有 `turn/start` 与 `turn/end` 的**已闭合**回合,并要求用户事件 `source.kind === 'user'`(`src/index.ts:183-212`)。所有操作的边界都是 `turn.startSeq - 1`:

- 用户消息编辑:边界前的前缀 + 编辑后的用户消息;`preserve` 时把目标回合之后的用户消息依次克隆排队(`src/index.ts:288-306`、`258-262`)。
- 助手块编辑:前缀 + 一个**手工构造的闭合回合**(`turn/start` → 用户消息 → `step/start` → 编辑后的 assistant 消息 → `step/end` → `turn/end`),不复制原回合的任何 tool call/result(`src/index.ts:309-335`、`464-475`)。
- Retry:目标回合的用户输入重新排队;`preserve` 时从目标回合起连同后续用户消息一起排队(`src/index.ts:338-359`)。
- Reroll:从后往前找最后一个「有用户消息且助手消息含文本/思考块」的已闭合回合,边界取其 `turn.startSeq - 1`,只排队该回合的用户输入,`cascade` 固定 `truncate`(`src/index.ts:361-379`)。

### reroll 的语义:新建分支重采样,不是原地重采样

代码上没有「替换某条 assistant 消息」的路径。`rerollPlan()` 产出的是一个新子会话的 `OperationPlan`:边界在目标回合之前,`queuedUsers` 是**原用户消息的克隆**(`cloneUser` 生成新 id,`src/index.ts:165-172`、`375`),然后由子 Agent 重新跑一轮。旧助手回复所在的整个旧会话仍然是版本树里的一个兄弟节点。

- **旧分支怎么保留**:作为 sibling Session 保留;版本树列出全部后代(`src/index.ts:721-742`),包括宿主自己创建的外部 fork,后者在 UI 里显示为「外部分支」(`src/client/MessageEditTimelineView.tsx:66-68`)。
- **怎么切换**:`controller.openVersion()` 等 Session 列表发布目标 id 后调用 `this.sessions.open(sessionId)`(`src/client/controller.ts:459-483`);标题栏的 `←`/`→` 分别打开 `undoStack[0]` 与 `redoSessionIds.at(-1)`(`src/client/MessageEditHeader.tsx:41-75`)。
- **怎么删除**:**插件没有删除操作**。`MessageEditOperation` 只有 `edit`/`reroll`/`retry`(`src/shared.ts:134-135`);若用户在宿主里删掉当前版本的祖先(或逆链上的某个版本),逆链会指向一个不在可见树里的 id,下一轮 `timeline()` 直接抛 `恢复目标 … 不在可见版本树中`(`src/index.ts:754-759`)。也就是说,删除不是插件功能,而是会破坏版本树完整性的外部操作。

## 怎么接进 DSH

**① manifest:两个键,没有宿主 patch。**

- `package.json:20-23` 的 `dsh.bundle.patch` 指向 `cordis.patch.yml`;后者只有一条 `insert`(`cordis.patch.yml:1-3`),`id: message-edit`、`name: dsh-message-edit`。
- `package.json:24-31` 的 `dsh.client` 声明 `platform: "web"` 与三个 `inject` 包(`dsh-client-connection`、`dsh-client-runtime`、`dsh-client-ui-conversation`)。这不是自造字段:本机 DSH 的 `parseDshClient()` 校验 `platform`/`inject`/`external`/`immediately`(`dsh-client-modules/lib/index.js:57-75`)。
- 发布安装命令:`dsh plugin --profile web add dsh-message-edit`(`README.md:10`、`107-109`);本地开发另有 `link:` 变体(`README.md:111-115`)。
- 不需要改 DSH 源码、`app.asar` 或 apiproxy;`README.md:124-128` 把「不改写 Session 事件、不修改引擎」写成范围边界,源码核对成立。

**② host 半:一个 `apply()`,六个公开 service,一条精确路由。**

- `inject = ['sessions', 'agents', 'sessionPersistence', 'sessionQuery', 'workspaceRegistry', 'webServer']`(`src/index.ts:102-109`),全部是宿主公开服务;没有私有 API、没有 `ReactLoopAgent`/apiproxy 的内部 RPC。
- 唯一的注册点是 `ctx.effect(() => ctx.webServer.register({ kind: 'exact', path: '/message-edit', handler }))`(`src/index.ts:879-885`;路径常量 `src/shared.ts:2`)。`webServer.register` 的 `{ kind: 'exact', path, handler }` 形状与返回 disposer 的语义,与宿主实现一致(`dsh-host-webserver/lib/index.js:326-334`)。
- 路由同时承担读与写:GET 返回时间线投影,POST 执行 `edit`/`reroll`/`retry`(`src/index.ts:858-876`)。
- **没有宿主 patch**,但有一条 DOM 级侵入:插件注释称官方消息行的 `MessageIconActions` 没有插件 slot(`src/client/InlineMessageEdit.tsx:1-7`),所以 `InlineMessageEdit` 用 `MutationObserver` 扫 `[class*="actions"]` 行,按文本前 24 字符匹配消息,再 `insertAdjacentElement` 注入「编辑 / 重试」两个图标按钮(`:214-286`)。这是全插件唯一不依赖公开 slot 的地方。

**③ browser 半:两个 slot,一个 per-session controller。**

- `inject = ['slots', 'conversation', 'connection', 'sessions']`(`src/client/index.ts:10`)。
- `conversation.view`:id `message-edit-timeline`,order `15`,label `Timeline`(`src/client/index.ts:28-34`;order 常量在 `src/shared.ts:5`,README 自述它位于 Trajectory 10 与 Prompt Studio 20 之间)。
- `conversation.session.header.actions`:id `message-edit-controls`,order 同样是 15(`src/client/index.ts:36-41`)。
- 两个入口共享同一个按 `sessionId` 缓存的 `MessageEditController`(`src/client/index.ts:14-22`);`connection/reset` 时只刷新已经加载过的 controller(`src/client/index.ts:24-26`、`src/client/controller.ts:421-425`)。
- 宿主侧确实在这两个 slot 名上 `renderSlot`(`dsh-client-ui-conversation/lib/client.js:18035`、`18215`),所以 slot 名不是自述。

**④ 与服务端 / 本地文件的关系:没有自己的存储。**

- 宿主半不写配置文件、不建数据库;版本数据就是 DSH 自己的 session 日志。
- 读:优先 live Session(`ctx.sessions.get`),其次 `sessionPersistence.inspect` / `readFrom`,最后 `sessionQuery.readSession`(`src/index.ts:682-699`)。
- 写:子 Agent 创建后 `await ctx.sessions.flush(child.agent.session)` 作为耐久性屏障,再返回 HTTP 成功(`src/index.ts:525-531`);没有外部网络请求。
- 依赖 `webServer` 意味着它只在带 Web 服务的 profile 里激活;没有 headless/CLI 形态。

## 关键实现

### 文件结构

| 文件 | 行数 | 作用 | 关键位置 |
|---|---:|---|---|
| `src/index.ts` | 885 | host 半:回合折叠、三种操作的计划、seed 构造、子 Agent 创建、时间线投影、HTTP 路由 | `183-256`、`279-379`、`430-532`、`552-631`、`701-777`、`858-885` |
| `src/shared.ts` | 141 | 双端共享的类型、路由路径、slot order、版本事件 schema | `2`、`5`、`17`、`20-59`、`99-108` |
| `src/client/controller.ts` | 484 | per-session 状态机:GET 解码、300ms 防抖、单飞 + 一次重跑、POST 变更、导航等待 | `34-35`、`151-169`、`350-419`、`427-456`、`459-483` |
| `src/client/index.ts` | 42 | 两个 slot 的注册与 controller 缓存 | `10`、`14-26`、`28-41` |
| `src/client/MessageEditTimelineView.tsx` | 352 | 版本时间线 + 回合/块编辑 + retry | `60-105`、`180`、`226-248`、`261-288`、`318-325` |
| `src/client/MessageEditHeader.tsx` | 78 | 标题栏 `←`/`→`/重生成,并挂载 InlineMessageEdit | `36-75` |
| `src/client/InlineMessageEdit.tsx` | 310 | DOM 注入编辑/重试按钮、内联编辑弹层、块选择器 | `1-7`、`57-112`、`214-306` |
| `src/client/*.module.css` | 717 | CSS Modules,`--dsw-*` 语义 token | 仅统计行数,未逐条审样式 |
| `scripts/build.mjs` | 29 | `tsc` + `tsdown`,把 `dist/index.js`→`index.mjs`、`dist/client.js`→`client.js` | `20-28` |
| `scripts/dsh-client-preset.ts` | 177 | 从官方 `tsdown.client.ts` 裁剪的 client bundle 预设:module-loader 契约、CSS Modules 内联、纯度门 | `1-11`、`55-70`、`166-173` |
| `package.json` / `cordis.patch.yml` | 67 / 3 | manifest 与 profile 行 | `package.json:13-36`;`cordis.patch.yml:1-3` |

### 数据流

```text
GET /message-edit?sessionId
  → traceSession(sessionId)
  → 找到可见根(root 或最后一个可见祖先)
  → traceSession(root) → flattenLineage(depth, createdAt 排序)
  → 每个节点读 own 日志段:
       live ? events.slice(seedLength)
            : persistence.readFrom(id, seedLength) / sessionQuery.readSession(...).slice(seedLength)
  → ownVersionEvent():schemaVersion / inverse 与 parentSession 一致 / 每分支唯一
  → { messages, retryableTurns, versions, undoStack, redoSessionIds }
  → controller 全量解码(缺字段/类型错即报错)

POST /message-edit { action, sessionId, ... }
  → withSourceAgent():live agent 或 resume + runMaintenance
  → planOperation(closedTurns(source.events))
  → inheritedSeed(boundary) [+ message-edit/version] [+ manualTurn]
  → ctx.agents.create({ sessionId: childId, seed, meta: { cwd, parentSession, seedLength, agentPreset } })
  → ctx.sessions.flush(child.agent.session)
  → workspace.attachSession(childId)   (若源会话属于某个 workspace)
  → child.agent.followup(message) × queuedUsers
  → { sessionId: childId, queuedTurns }
```

分叉的失败恢复是「结构性逆」而不是回滚日志:`runOperation` 在一个 `inverses[]` 里依次压入 `child.dispose()`、`workspace.detachSession(childId)`,失败时倒序执行;若逆也失败,抛 `AggregateError`(`src/index.ts:552-582`、`540-550`)。

### 版本/时间线契约(没有测试,只有运行时断言)

仓库**没有测试文件、没有 `test` 脚本、没有 CI workflow**(`package.json:33-36` 只有 `build`/`prepublishOnly`;`git ls-files` 无 `test`/`spec`/`.github`;`git log --diff-filter=D` 只显示历史删除过 `dsh.plugin.json` 与 `scripts/dsh-env.mjs`)。因此下面这些契约不是被测试钉住的,而是被读路径的 `throw` 钉住的:

| 契约 | 强制点 | 违反时 |
|---|---|---|
| 目标消息必须属于已闭合回合 | `editPlan()` / `closedTurns()` | POST 409,消息 `所选消息不属于已落定回合` |
| 分支边界必须是连续事件 | `inheritedSeed()`(`src/index.ts:430-437`) | 抛 `分支边界不是连续会话事件` |
| 每个子会话最多一个 own 版本事件 | `ownVersionEvent()`(`src/index.ts:589-595`) | GET 409,`包含多个自身版本效果` |
| 版本 schema 必须是 2 | `ownVersionEvent()`(`src/index.ts:599-609`) | 抛 `使用不支持的版本效果结构` |
| inverse 必须指向 parentSession | `ownVersionEvent()`(`src/index.ts:604-608`) | 抛 `版本效果与逆不匹配` |
| effect id 在可见版本树内唯一 | `timeline()`(`src/index.ts:744-749`) | 抛 `版本效果 … 重复` |
| 逆链无环、目标在可见树内 | `timeline()`(`src/index.ts:752-760`) | 抛 `版本效果逆链包含循环` / `恢复目标 … 不在可见版本树中` |
| 响应形状 | 客户端逐字段解码(`src/client/controller.ts:81-169`) | 前端 `status=error`,显示解码错误 |

旧版平面事件的读兼容也在:`schemaVersion` 不存在的旧事件被规范化为同一 `effect` 结构(`src/shared.ts:46-59`;`src/index.ts:612-630`),但**没有写入迁移器**,只有读时归一化。

## 为什么它突出

**先拆星标归属。** 这是单包仓库,不是 monorepo 子目录,所以没有「主项目星标被记到插件头上」的问题;GitHub 星标就是仓库级,可以归给这个插件。时间线也简单:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-06 | 仓库创建;首提交即 `v0.2.0 release` | GitHub API + `git log` |
| 2026-08-16 | 最后一次 push,`v0.2.3` | `git log -1` |
| **2026-08-19** | **32 星 / 1250 下载(冻结边车)** | `data/stars.json`、`data/downloads.json` |
| 2026-11-18 | **56 星**(+24,+75%)、24 forks、21 open issues | GitHub API 当日 |

也就是说,**星标在涨、代码没动**:最后三个月零提交,星标从 32 涨到 56;而在 2026-08-19 的采样点上,下载已经是 1250(约星标的 39 倍)。**判断**:它主要不是靠仓库曝光被安装,而是通过 npm/registry 进入 profile。仓库历史只有 7 个提交(2026-08-06 ~ 08-16),首提交就是 v0.2.0;更早的 v0.1 不在本仓库历史里,所以不能拿提交历史解释最初 13 天的 32 星——只能说采样点距创建仅 13 天。

**扩散结构比星标更能说明它在生态里的位置。** 口径是先跑 `grep -ril 'message-edit' data/plugins/`,得 **5** 条(含自身);再逐条读 README 确认归属:

| 条目 | README 证据 | 判定 |
|---|---|---|
| `Moeblack/dsh-message-edit` | — | 自身,不计 |
| `sh1robana/dsh-plugin-message-edit` | `sh1robana README:62`:「基于 [Moeblack/dsh-message-edit] 继续开发」 | **fork**(明示代码谱系) |
| `SpookySandwich/dsh-plugin-message-edit` | `SpookySandwich README:76`:「宿主端的分支逻辑源自 [dsh-message-edit](MIT © Moeblack),在其基础上重做…」 | **fork**(明示代码谱系) |
| `huhu23333/dsh-reasoning-distill` | `huhu23333 README:89` 给出插件 URL;`:96`「通过 `vendor/dsh-message-edit-0.2.3-patched4.tgz` 加 `scripts/patch-message-edit.py` 来安装与修补它」 | **vendor 集成**(不是 fork) |
| `xt765/dsh-message-edit` | README 里没有 `Moeblack`;按其 README 自述走 `ctx.sessions.fork`/`create`,是另一套实现 | 同名独立,**不计** |

所以「第三方引用」是 **3**(2 fork + 1 集成);若只算代码谱系是 **2**。把 `Moeblack` 也加进 token 会得 7 条,多出的两个是同一 owner 的无关条目(`Moeblack/dsh-prompt-studio`、`Moeblack/deepseek-manners`),只匹配了作者名,不计。补充:两个 fork 的源码里都能搜到 `message-edit/version` / `restore-version` / `seedLength` 等本插件特有标识(只用于确认谱系,未读其实现);`xt765` 的 clone 里这些标识为 0。

这个结构值得单独说:两个 fork 都明确写了归属,其中一个(`SpookySandwich`)在 2026-11-17 还在 push——比原仓库的最后 push 晚三个月;另一个把「宿主端的分支逻辑」当作可复用的数据模型接走。**判断:能被接走的是数据模型,不是服务**——版本树完全建在 DSH 的 `parentSession` + 一个自定义事件上,没有私有后端,所以第三方可以只重写 UI 或只换语义,而继续复用分支事务。反过来,原仓库没有 CI、没有测试、21 个 open issue,维护已经停了三个月,这使「概念活着、实现停着」成为它最突出的特征。

**机制上的独特性**还在于它把版本树读成宿主谱系:连宿主自己创建的 fork 都会出现在版本列表里,标成「外部分支」(`src/client/MessageEditTimelineView.tsx:66-68`;`src/index.ts:722-742`)。所以它不只是编辑器的历史面板,也是一个**按谱系深度与创建时间排序的会话谱系浏览器**;`undoStack`/`redoSessionIds` 都是这个谱系的派生值,不是另一份可变状态。

## 代价与边界

**1. 宿主版本错位(最硬)。** 插件按 `@deepseek-ai/*@0.1.0-rc.6` 编译(`package.json:51-59`),本机安装的是 `0.2.1-rc.5`。在当前宿主上:

- `meta.seedLength` 不在 `SessionStore.prepare()` 的 header 白名单里,会被静默丢弃(`dsh-session/lib/index.js:1818-1827`);当前版本的 seeded 语义是 `meta.isSeeded` + 顶层 `inheritedEventCount`(`dsh-agent/lib/types/index.d.ts:64-78`),插件两者都没传(`src/index.ts:516-521`)。结果是子会话以 `isSeeded: false` 创建。
- 当前 `SessionHeader`(内存/类型)没有 `seedLength` 字段(`dsh-session/lib/types/types.d.ts:74-77`),而插件用它切 own 段(`src/index.ts:588-591`、`693-698`)。`undefined ?? 0` 会把继承来的版本事件也当成自己的:第二代分支(对已有分支再编辑)会看到「继承的一条 + 自己的一条」,触发 `包含多个自身版本效果`(`src/index.ts:593-595`),时间线 GET 返回 409。
- 这是**读代码得出的判断,未实跑**;但它决定了「在本机 0.2.1-rc.5 上还能不能用」,见「待验证」。

**2. 自定义事件缺 `ignorable`,持久化读回可能被拒。** 当前 DSH 对仓库外插件事件的规则是:未识别的类型必须带 `ignorable: true`,否则读路径**必须拒绝重建**而不是静默丢弃(`dsh-session/lib/types/types.d.ts:500-508`);format v4 的 restore 在遇到未知类型且非 ignorable 时抛 `SessionFormatUnsupportedMigrationError`(`dsh-session-format-v3-to-v4/lib/index.js:989`)。插件只写 `{ type, seq, time, data }`(`src/index.ts:440-446`),全仓库没有 `ignorable`(`grep -rn ignorable src/ scripts/` 为 0)。**判断**:在当前宿主上,带 `message-edit/version` 的分支日志重启后可能无法被 restore;插件面向的 rc.6 是否也要求该标记,未验证。

**3. 助手块编辑的 seed 在当前宿主上会被 surface 校验拒绝。** 手工回合给 `assistant/message` 写的是 `surfaceOp: 'append'` + `sourceEventSeqs: []`(`src/index.ts:469-472`);当前宿主对 `assistant/message` 携带 `sourceEventSeqs` 直接抛 `assistant/message embeds its source stream and cannot carry sourceEventSeqs`(`dsh-session/lib/index.js:315`),对空引用数组另有 `sourceEventSeqs must not be empty`(`:320`);seed 构造会走 `validateSurfaceMetadata`(`:358-366`、`:1408`)。用户编辑 / reroll / retry 不构造手工回合,不受这一条影响。**判断**:在当前宿主上,只有「编辑助手回复/思考」这一条路会在创建子会话时失败。

**4. 操作失败可能留下孤儿分支。** 顺序是 `agents.create` → `flush` → `workspace.attachSession` → `followup`(`src/index.ts:561-569`)。`flush` 是耐久性屏障;如果它成功、后面的 attach/followup 失败,`recoverOperation` 只能 `dispose` 子 Agent、`detachSession`,**不能删除已经持久化的子会话**(`src/index.ts:540-550`、`562-580`)。用户看到 POST 失败,刷新后却可能多出一个分支;插件没有清理命令。

**5. 版本树完整性靠外部目录,删掉逆链上的祖先即破链。** 源日志不可变是优点,但逆链依赖所有祖先会话仍在 `sessionQuery` 的可见语料里:根被删/被裁剪时 `rootId` 退到最后一个可见祖先(`src/index.ts:702-707`),逆链上的 id 不在树里就直接抛错(`src/index.ts:754-759`)。没有修复、没有「忽略缺失版本」的降级;`undo` 也不是撤销写入,而是切换到仍然存在的父版本(`README.md:32`)。

**6. 并发/幂等:服务端没有锁。** 客户端只用每个 controller 的 `pending` 挡住重复点击(`src/client/controller.ts:427-433`),两个标签页或两个客户端可以同时 POST;两边都基于同一个源日志规划,于是产生两个兄弟分支、两次模型/工具执行。数据不会互相覆盖(源不可变),但版本列表会多出重复语义的分支,且没有 nonce/去重。

**7. 工具副作用不回滚。** `preserve` 会把后续用户消息重新排队,assistant 输出与整条工具链重新生成(`README.md:30-31`);工作区文件、终端外部效果、既有产物都不在插件的回滚范围(`README.md:126-127`)。如果目标回合里的工具改过文件,新分支看到的是**已被旧分支改过的工作区**,不是「回合开始时」的文件状态。助手块编辑更窄:手工回合只保留文本/思考块,原 assistant 消息里的 tool-call 块被 `filter` 掉(`src/index.ts:264-277`),原回合的工具链整体不进入新版本。

**8. 压缩摘要不参与建模。** `closedTurns()` 只按 `turn/*` 折叠,不识别 `compaction/start` ~ `compaction/end`(`dsh-session` 的类型里明确有这对括号,`dsh-session/lib/types/types.d.ts:424-425`)。边界之后被丢弃的压缩事件不会重算;边界之前继承的摘要原样保留。**判断**:新分支的上下文长度可能回到压缩前,或与摘要描述的历史不一致;插件既不重算摘要,也不提示。未实跑压缩场景。

**9. DOM 注入是脆的。** 按钮绑定依赖 `[class*="actions"]` 这个类名片段 + 消息文本前 24 字符匹配(`src/client/InlineMessageEdit.tsx:214-240`);两条前缀相同的消息可能绑到错误的 `eventSeq`;虚拟列表重建行时按钮会被清理后重新匹配,依据仍是文本而不是事件 id。MutationObserver 观察整个 `document.body` 子树,只用 rAF 合并(`:288-298`);长会话里这是持续成本。两个入口的级联策略还不一致:Timeline 有 `truncate`/`preserve` 选择器(`src/client/MessageEditTimelineView.tsx:229-240`),内联编辑器却硬编码 `'truncate'`(`src/client/InlineMessageEdit.tsx:90`、`259`)。

**10. HTTP 路由没有鉴权。** 路由注册在 `webServer` 的 exact 表上,处理器里没有 token、Origin、CSRF 或方法级权限检查(`src/index.ts:858-876`);宿主 Web 服务通常只在本机绑定,所以暴露面首先是本机进程/同源页面。但一个 POST 就能创建分支并 `followup`(会触发模型与工具执行),没有二次确认。**判断**:依赖宿主 web server 的本地信任边界,不是插件自己建立的授权。

**11. 规模成本。** `inheritedSeed` 用 `source.events.slice(0, boundary + 1)` 把前缀复制进内存(`src/index.ts:430-437`);时间线对每个谱系节点读日志,并发上限 4(`src/index.ts:660-679`、`708-712`),没有分页/懒加载版本列表。v0.2.3 的提交信息正是「timeline 按需分层读取 + 客户端刷新风暴治理」,说明这些成本已经在真实会话上出现过。

**12. 维护与法务小缺口。** 仓库没有 `LICENSE` 文件(`git ls-files` 无;GitHub API `license: null`),但 `package.json:48` 与 README 徽章都写 MIT,两个 fork 的归属说明都指向它(其中一个明写 MIT © Moeblack);没有 CI、没有测试、21 个 open issue、最后 push 2026-08-16。`files` 只发布 `index.mjs`/`client.js`/`client.js.map`/`cordis.patch.yml`/`README.md`(`package.json:13-19`),源码不在 npm 包里;构建产物是提交进仓库的,人工 `npm run build` 生成,没有「产物与 src 一致」的 CI 门。

## 可信度与复现

**★★★(源码级)**:插件的 host 半、shared、全部 client TS/TSX、构建脚本、manifest、cordis patch、README 都逐行读过,7 个提交的信息与删除文件历史也核过;CSS 只统计行数,未逐条审样式;`package-lock.json` 未读;生成的 `index.mjs`/`client.js` 只做了体量与用途核对,没有逐行审计。宿主侧对照的是本机 `@deepseek-ai/dsh@0.2.1-rc.5` 的 `dsh-session`、`dsh-agent`、`dsh-session-query`、`dsh-client-modules`、`dsh-host-webserver`、`dsh-session-log-deepseek`、`dsh-session-persistence-jsonl`、`dsh-session-format-v3-to-v4`。**没有实际安装、启动或编辑过任何会话**;所有关于「当前宿主上会失败」的句子都是读码判断,已在正文标「判断」。

```sh
# 1) 克隆与提交
git clone --depth 1 https://github.com/Moeblack/dsh-message-edit.git .work/mine/cards/message-edit/repo
git -C .work/mine/cards/message-edit/repo log -1 --format='%H %ad %s'
# → b78a167064ca612f1c400060d2bfc1dc9bc46436 2026-08-16 19:33:35 +0800 性能修复… (v0.2.3)

# 2) 规模(2 292 = 885 + 141 + 484 + 42 + 310 + 78 + 352)
cd .work/mine/cards/message-edit/repo
wc -l src/index.ts src/shared.ts src/client/*.ts src/client/*.tsx | tail -1
wc -l src/client/*.css | tail -1          # 717
wc -l scripts/*.mjs scripts/*.ts | tail -1 # 206
git ls-files | wc -l                       # 23

# 3) 零测试 / 零 CI
git ls-files | grep -Ei 'test|spec|\.github' || echo 'no test/CI files'
node -e "const p=require('./package.json'); console.log(p.scripts)"  # 只有 build/prepublishOnly

# 4) 扩散(在 awesome-dsh-plugin 仓库根;用目录形式避免 Argument list too long)
grep -ril 'message-edit' data/plugins/ | wc -l              # 5
grep -ril 'message-edit' data/plugins/                      # 自身 + 4 个第三方
grep -ril 'message-edit\|Moeblack' data/plugins/ | wc -l    # 7(多 2 个同 owner 无关条目)
curl -sL https://raw.githubusercontent.com/sh1robana/dsh-plugin-message-edit/HEAD/README.md | grep -n Moeblack
# → 62: 基于 Moeblack/dsh-message-edit 继续开发
curl -sL https://raw.githubusercontent.com/SpookySandwich/dsh-plugin-message-edit/HEAD/README.md | grep -n Moeblack
# → 76: 宿主端的分支逻辑源自 dsh-message-edit（MIT © Moeblack）
curl -sL https://raw.githubusercontent.com/huhu23333/dsh-reasoning-distill/HEAD/README.md | grep -n Moeblack
# → 89, 96: 第三方插件 URL 与 vendor/dsh-message-edit-0.2.3-patched4.tgz
curl -sL https://raw.githubusercontent.com/xt765/dsh-message-edit/HEAD/README.md | grep -n Moeblack || echo '同名但无归属'

# 5) 宿主版本与关键契约
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh
node -e "console.log(require('$DSH/package.json').version)"          # 0.2.1-rc.5
grep -n 'const header = {' $DSH/node_modules/@deepseek-ai/dsh-session/lib/index.js        # 1818
grep -n 'seedLength' $DSH/node_modules/@deepseek-ai/dsh-session/lib/index.js             # 1043
grep -n 'readonly inheritedEventCount' $DSH/node_modules/@deepseek-ai/dsh-agent/lib/types/index.d.ts # 78
grep -n 'unknown event type' $DSH/node_modules/@deepseek-ai/dsh-session-format-v3-to-v4/lib/index.js # 989
```

**未读 / 未跑**:没有 `npm install`、没有 `npm run build`、没有实际加载插件;没有在真实会话上创建分支;没有跑压缩、并发、删除分支、工具副作用回放等场景。CSS 的视觉与可访问性未审;`client.js.map` 的内容未审;宿主 0.1.0-rc.6 的源码没有,插件面向版本的 `seedLength`/`ignorable` 语义只能由插件代码反推。

## 待验证

1. **在本机 0.2.1-rc.5 上安装并跑两类编辑**:先确认 `meta.seedLength` 被丢弃后子会话的 `isSeeded`/`inheritedEventCount` 实际值;再对已有分支执行一次用户消息编辑,看时间线是否真的抛 `包含多个自身版本效果`(`src/index.ts:593-595`);最后触发一次「编辑助手回复」,确认 `sourceEventSeqs: []` 是否命中 `assistant/message … cannot carry sourceEventSeqs`(`dsh-session/lib/index.js:315`)或 `sourceEventSeqs must not be empty`(`:320`)。这两件事决定「插件当前还能不能用」。
2. **持久化读回**:创建分支后重启 `dsh web`,重新打开该会话;带 `message-edit/version` 的日志是否被 restore 拒绝(`dsh-session-format-v3-to-v4/lib/index.js:989`),还是能作为 log-only 事件保留。若被拒,数据是否还能从 live 会话导出。
3. **前缀复制成本**:对一条几千事件的会话连续做 5 次编辑,量一下子会话 JSONL 的物理大小(是否只有 header + 后缀,还是把 seed 前缀也落盘)与进程内存;验证 `seedLength` 的持久化收益是否成立。
4. **并发编辑**:两个标签页同时 POST 同一 `sessionId`,确认产生两个兄弟分支、两次 followup,且没有 nonce/去重;再检查 `undoStack`/`redoSessionIds` 是否把两个分支都正确表示。
5. **删除一个版本会话**:在宿主 UI 删除中间分支后打开时间线,确认 `恢复目标 … 不在可见版本树中`(`src/index.ts:757`)是否是唯一结果,以及是否有任何降级/修复入口。
6. **压缩场景**:对一条已压缩的会话做目标回合在压缩点之前的编辑,观察新分支的上下文是否重新变长、摘要是否被丢弃;插件没有 `compaction/*` 分支,预期不会重算摘要。
7. **工具副作用**:在一个含破坏性 bash 的回合上执行 `preserve` 重试,确认命令被再次执行且工作区文件不回滚(`README.md:126-127`);这是使用前最需要知道的语义边界。
