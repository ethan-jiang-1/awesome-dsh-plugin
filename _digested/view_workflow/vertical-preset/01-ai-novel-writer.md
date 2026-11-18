# ai-novel-writer — 不是桌面应用的适配层，而是在 DSH 里重写的第二个小说工作台

> 证据等级:★★★(源码级;`EthanYoQ/Pagekin@3f24e58b9a0eb468fbe115c196654bd9aeaf2af7`,2026-11-18)。
> 仓库已改名:旧 `EthanYoQ/AI-Novel-Writer` 现 301 到 `EthanYoQ/Pagekin`,registry 里的 URL 已陈旧。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 393 为 2026-08-19 历史采样且属**主应用仓库**;⚠ 下载:边车无记录(2026-08-19 采样缺口)。2026-11-18 实时 2684(GitHub API)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `EthanYoQ/AI-Novel-Writer#dsh-ai-novel-writer`([registry](../../../data/plugins/EthanYoQ__AI-Novel-Writer--plugins-dsh-ai-novel-writer.yml));旧 URL `…/AI-Novel-Writer/tree/master/plugins/dsh-ai-novel-writer` → 新 URL `https://github.com/EthanYoQ/Pagekin/tree/master/plugins/dsh-ai-novel-writer` |
| 类目 | workflow([census](../../ecosystem/census.py) 703 条 / 全表 11 744 条) |
| 子分类 | `vertical-preset`(整包交付一种工作方式:预设 + 工作台) |
| 状态 | ⛔ **冻结**:0.1.0 preview 已冻结,20 个 peer 中 6 个在当前 DSH 不存在;仓库已改名 Pagekin。**不建议新装**,保留作垂直预设/写权限机制参考。 |
| 自述 | 「安装专用 AI 小说创作预设与工作台:带修订号的本地项目资产、紧凑侧边工作台、需原生审批的逐文件变更」——三项在源码里都能落地,但自述漏了第四项:V2 的**提案箱**才是主线 |
| 星标 ⚠ | **393**(2026-08-19 采样,**主应用仓库级星标**,非本插件);2026-11-18 实时 **2684** |
| 下载 ⚠ | 边车无记录(2026-08-19 采样缺口);npm 实时读数见"为什么它突出" |
| 扩散 | **0**(口径:`grep -ril 'ai-novel-writer' data/plugins/` 命中 1 条,即自身;`grep -ril 'pagekin' data/plugins/` 0 命中;`grep -ril 'ai.novel'` 同为 1 条) |
| 仓库 commit | 整仓 `3f24e58b`(2026-11-18);插件子目录最后提交 `364cecbe`(2026-10-22),子目录共 **8** 个提交 |
| 包形态 | npm `@ethanyoq/dsh-ai-novel-writer@0.1.0`(2026-08-21 发布,仅此一版):`dsh.bundle.patch` + `dsh.client.platform=web`,4 个导出入口 |
| 代码规模 | `src/**` 23 文件 **15 323 行**(不含测试;`find src -type f \| xargs wc -l`);`tests/*.spec.ts*` 41 文件 13 437 行;presets 4 文件 42 行 |

## 它到底是什么

**一句话:它是一个 vendor 发布的、与桌面应用没有任何代码共享的 DSH 原生重写。**

最容易误判的一点:README 首段(README.md:5)说 "It does not open desktop projects",`package.json:3` 的包描述是 "A local-first novel project plugin"。核对成立——`grep -rn "from '\.\./\.\./\.\./" src/` 与 `grep -rn "vela" src/` 在插件里都 0 命中,反向 `grep -rn "dsh-ai-novel-writer" src/ electron/` 在桌面应用里也 0 命中。**两边是两套实现,共用的只有"小说"这个领域词**。桌面应用 `src/` 877 个 TS/TSX 文件、186 049 行;插件 23 个文件、15 323 行,约为主应用 `src/` 的 8%。

插件里同时存在**两代互不兼容的数据模型**,这是读源码前必须先分清的事:

**V1——文件资产 + 逐文件 SHA-256 修订。** 五个固定资产,路径由 `novelAssetSource()` 硬编码,不含任何调用方提供的路径段(`src/novel-project.ts:369-378`):

| 资产 | 路径 |
|---|---|
| `project` | `.ai-novel/project.json` |
| `characters` | `.ai-novel/characters.json` |
| `story-blueprint` | `.ai-novel/blueprints/story.json` |
| `chapter-blueprint` | `.ai-novel/blueprints/chapters/NNNN.json` |
| `chapter-draft` | `chapters/NNNN.md` |

修订号就是写入字节的 SHA-256(`novel-project.ts:56-58`);读不到的非清单资产返回 `revision: 'absent'` 而不是报错(`novel-project.ts:513-518`)。核心循环是 **read → 提案 → 原生审批 → 原子替换单文件 → CommitReceipt**。

**V2——本地 SQLite 聚合 + 非权威提案箱。** `.ai-novel/novel.db`,`node:sqlite` 的 `DatabaseSync`,`APPLICATION_ID = 0x41_4e_4f_56`(即 `ANOV`)、`USER_VERSION = 4`(`src/novel-store.ts:14-16`),15 张表(`novel-store.ts:726-889`):`project` 同时存 `global_revision` 与 `project_revision`,每个聚合(架构/人物集合/章节/任务)各有自己的 `revision`,正文是 `artifacts` + `chapter_finals` 的版本链,提案是 `proposals`/`proposal_changes`/`proposal_items` 三层。核心循环变成 **read state → 提交恰好一条 typed change → 提案入箱(pending)→ 人在工作台 apply → 事务内校验 aggregate+global 双修订号 → receipt**。

两代的分界不在"新旧",而在**谁能写权威状态**:V1 里模型自己写(经审批),V2 里模型**永远不能写**——`novel_propose_change` 的 description 直说 "this tool never writes authoritative project state"(`src/agent.ts:557`),写入只发生在提案箱 apply 的事务里。

这四件东西拼起来才叫"垂直预设":

1. **preset 模板**:`presets/ai-novel-writer/` 与 `presets/ai-novel-writer-v2/` 各两个文件(`preset.yml` + `agent.cordis.yml`),装在包里,由用户点一次"安装"才复制到用户 preset 根——**不是加载即生效**。
2. **agent 面**:`./agent`(V1,两个工具)与 `./agent-v2`(V2,两个工具),各自是一个 Cordis 插件入口。
3. **host 面**:根入口只做三件事——注册 `/ai-novel` loopback RPC、托管 preset 安装器、把 workspace 路径喂给只读投影(`src/index.ts:312-331`)。**根入口不注册任何模型工具**(`cordis.patch.yml:1-3` 的注释就是这句话)。
4. **client 面**:侧边栏入口 + `shell.overlay` 抽屉 + 设置页状态卡,三个 slot。

**去掉主应用还能用吗?能**——它不 import 主应用任何东西,也不连本地服务、不读 `.vela` 项目。
**去掉 DSH 的 preset 机制还能用吗?不能**——工具面完全由 preset 挂载,根入口一个工具都没有。

## 怎么接进 DSH

**① manifest:一行 insert + 一个 client 声明。** 真正被读的是 6 行的 `cordis.patch.yml`:

```yaml
- insert:
    - id: ai-novel-writer
      name: '@ethanyoq/dsh-ai-novel-writer'
```

`package.json:53-67` 同时声明 `dsh.bundle.patch: ./cordis.patch.yml` 与 `dsh.client.{platform: web, inject: [5 个 client 包]}`——前者让 profile 把它当层,后者让 Web 侧加载 `./client`。

**② host 面:两个注入、一个 loopback 频道、18 个 endpoint。** `inject = ['connection', 'workspaceRegistry']`(`src/index.ts:111`),`apply()` 里 `connection.rpc.handle('/ai-novel', handler, { authority: 'loopback' })`(`:324`)。endpoint 是白名单式分发(`:215-268`):

| 组 | endpoint |
|---|---|
| preset | `preset/status`、`preset/install` |
| V2 读写 | `workspace/initialize`、`workspace/state/read`、`state/read`、`chapter/context`、`task/read`、`proposal/list`、`command/preview`、`command/commit`、`proposal/apply`、`proposal/retry`、`proposal/discard`、`proposal/regenerate` |
| 恢复 | `workspace/reattach`、`workspace/clone` |
| 只读投影 | `context/read`、`asset/read` |

只读投影那条路径先要求 payload **只含 workspace UUID + 正文章节号**(`:238-252`,UUID 用正则硬校验、拒绝多余字段),再由 host 从 `workspaceRegistry` 取路径(`:253-256`)。**浏览器拿不到本地路径**。

**③ preset 安装器:显式动作 + 原子发布 + 永不覆盖。** `templateRoot()` 是包内 `presets/`(`src/index.ts:124-126`),`presetRoot` 默认 `dshHomePath('.agent-presets')`(`:120-122`;README.md:105 说明默认 `$DSH_HOME/.agent-presets`)。安装流程:`status` 判定 → `mkdtemp` 暂存目录 → 逐文件 `writeFileAtomic` → `rename` 发布(`src/preset-installer.ts:54-80`)。冲突判定极严(`:129-159`):目录条目集合必须恰好是 `agent.cordis.yml` + `preset.yml`、必须都是普通文件、不是符号链接、且**与包内字节完全相等**,否则 `conflict`,一个字节都不改。

**④ agent 面:两个独立入口,各自用 `tools.restrict()` 做整会话掩码。** `./agent` 注入 `['agents','systemPrompt','tools']`(`src/agent.ts:595`);`./agent-v2` 额外注入 `workspaceRegistry`(`src/agent-v2.ts:10`)。两者都调 `installDedicatedPresetSurface()`(`agent.ts:125-204`),机制是三层:

- `agent.ctx.tools.restrict({ allow: [...toolNames] })`(`:143`)把**继承来的全局工具**全部掩掉,只留两个小说工具;
- `ctx.on('tools/pre-execute')` 对非白名单工具直接 `kind: 'deny'`(`:189-195`);
- `ctx.on('system-prompt/assemble', { prepend: true })` 每轮重建 tools 数组,数量或重名不符就**抛错**(`:167-188`)——宁可整轮失败,也不让模型看到多余工具。

同一段代码还解决了一个真实生命周期缺口:preset 选择可以在**不重建 agent** 的情况下重挂,所以它同时监听 `agent/created`、`agent-preset/selected` 与每次 `system-prompt/assemble`(`:167-202`),并用 `Symbol.for('@ethanyoq/dsh-ai-novel-writer/dedicated-surface-installation')` 挂在 live Agent 上(`:41-56`)避免 V1/V2 互相覆盖掩码——注释原话是 V2 会把 `novel_propose_change` 丢给 V1 的 allow-list。

**⑤ 依赖:3 个运行时包 + 20 个 peer + 零原生二进制。** `dependencies` 只有 `@deepseek-ai/dsh-atomic-write`、`@deepseek-ai/dsh-home-paths`、`@deepseek-ai/schemastery`(`package.json:78-82`);peer 共 20 个,**17 个精确** `0.1.0-rc.6`,另 3 个是 `@deepseek-ai/cordis@4.0.1` 与 `react`/`react-dom@^18.2.0`(`:83-104`)。SQLite 用 `node:sqlite` 动态 `import()`(`novel-store.ts:3023`),所以没有 `better-sqlite3`、没有编译产物,`engines` 卡在 `^22.19 || >=24`(`package.json:68-70`)。

**⑥ client 面:三个 slot、五个注入。** `inject = ['slots','connection','sessions','workspaces','layout']`(`src/client/index.ts:103`),注册点(`:760-778`):

| slot | id | order | 组件 |
|---|---|---|---|
| `sidebar.footer.action` | `ai-novel-workbench` | 90 | `NovelWorkbenchTrigger`(侧栏「小说工作台」按钮) |
| `shell.overlay` | `ai-novel-workbench` | 90 | `NovelWorkbenchOverlay`(抽屉本体) |
| `settings.plugin.item` | `ai-novel-writer` | 90 | `NovelPluginStatusCard`(preset 安装/状态卡) |

**⑦ 安装命令。** `dsh plugin --profile web add @ethanyoq/dsh-ai-novel-writer`(README.md:16),然后**手动几步**:开工作台 → 点安装 preset → 新建会话选「AI 小说作家 V2」→ 选工作区(README.md:25-31)。README.md:33 明确警告仓库根包是 Electron 应用,不要当插件装。

## 关键实现

### 文件结构

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `src/novel-store.ts` | 3 241 | V2 权威存储:SQLite schema、聚合修订、提案箱、artifacts 版本链、工作区绑定与恢复 | schema `:726-889`;提案 `:818-859`;提交 `:2275-2346`;apply `:2565-2622`;修订校验 `:2845-2849`;打开/降级 `:3099-3241` |
| `src/client/workbench-store.ts` | 2 057 | 工作台控制器:目标选择、读、提案组装、审批可用性判定、结果回读 | 审批判定 `:298-310`;prompt 端口 `:171` |
| `src/client/workbench-view.tsx` | 1 818 | V1 抽屉与 V2 工作台的全部表单/差异/提案审阅 UI | 抽屉正文 `:1360-…`;V2 正文 `:848-…` |
| `src/client/workbench-v2.ts` | 1 544 | V2 客户端状态机(阶段、编辑草稿、提案生命周期) | — |
| `src/novel-project.ts` | 718 | V1 文件项目:五资产、SHA-256 修订、单文件原子替换、锁 | 路径 `:369-378`;替换 `:451-502` |
| `src/command-rpc.ts` | 680 | V2 loopback 命令面:payload 解析、预览 diff、稳定错误码 | handler `:493-…`;状态投影 `:53-…` |
| `src/novel-migration.ts` | 789 | V1→V2 显式迁移:五源指纹、归档、发布、可恢复 | 指纹 `:396-404`;源清单 `:407-435` |
| `src/agent.ts` | 616 | 两代工具定义、原生审批门、preset 工具面隔离、V2 提示协议 | 工具集 `:29-31`;掩码 `:125-204`;审批 `:435-441`;V2 工具 `:509-589` |
| `src/preset-installer.ts` | 174 | 两个 preset 的安装/状态/冲突判定 | 安装 `:54-80`;判定 `:129-159` |
| `src/index.ts` | 332 | host 入口:loopback RPC、安装器装配、HMR 排空 | 频道 `:324`;生命周期 `:283-303` |
| `src/client/index.ts` | 779 | client 入口:三个 slot、RPC 端口、连接观察 | slot `:760-778`;rail 兼容 `:120-128` |
| `presets/*/agent.cordis.yml` | 19×2 | preset 组合:persona + agent-instructions + novel-agent | `:18-19` 挂 `@ethanyoq/dsh-ai-novel-writer/agent(-v2)` |

### 数据流

```text
① V1 写路径(逐文件、需审批)
  模型 --novel_apply_change(kind=replace, targetKind, baseRevision, replacement)-->
  tools/pre-execute 返回 {kind:'ask'} --> DSH 原生审批(一次性)
  --> novel-project #replace:读当前 SHA-256 → 与 baseRevision 比对
  --> withFileLock + 再比对一次 → writeFileAtomic --> CommitReceipt{oldRevision,newRevision}

② V2 提案路径(模型不能写)
  模型 --novel_read{kind:'state'}--> command-rpc 的 projectNovelStateRead
  模型 --novel_propose_change{changes:[1 条]}-->
  submitProposal: argsHash = sha256(canonical JSON) → proposals/proposal_items(pending)
  --> 人 在工作台点「应用」--> proposal/apply --> 逐项 BEGIN IMMEDIATE
  --> #commitChangeInTransaction: aggregate_revision 与 global_revision 双比对
  --> 成功: receipt + item=applied;失败: item=stale|failed,循环停在该项

③ 工作台 → 模型(不是 RPC)
  抽屉把「让当前模型生成」拼成一条普通用户消息(带 [AI_NOVEL_UI_CORRELATION:…] 标记)
  --> session prompt --> 模型自己按 preset persona 调工具 --> 抽屉从会话事件里回读 tool-result
```

关键点:**V2 的写入 RPC 与模型工具是两条完全独立的路径**。模型永远只写 `proposal_items`,写入权威聚合的只有浏览器那条 `proposal/apply`。这也是为什么 README.md:55 反复强调"看到生成文本 ≠ 已保存"。

### 版本化本地素材:三套修订号,别混

1. **V1 文件修订**:SHA-256 十六进制串,`absent` 是"该资产不存在"的哨兵(`novel-project.ts:56-58`、`513-518`)。写入前**比对两次**:进锁前一次、锁内一次(`:469-483`),失败都是 `STALE_REVISION`。这是为了覆盖"审批期间别人改了文件"——`tests/agent-approval.spec.ts:114-144` 就是把这个竞态钉死的用例。
2. **V2 聚合修订**:每个聚合一个整数 `revision`,外加全库一个 `global_revision`。提交时两者都必须等于客户端读到的值(`novel-store.ts:2845-2849`),否则 `STALE_REVISION`。`global_revision` 的作用是发现"别的聚合在我读之后被改了"——单看聚合修订会漏。
3. **提案项状态机**:`pending → applied | stale | failed | discarded | superseded`(`:1225`、`:346`)。`stale` 不是终态,可以 `retry`;`failed` 只能 `discard` 或 `regenerate`(拿一次性 `regenerationTicket`,旧项转 `superseded`,`:2332-2337`)。

**回滚**没有 undo 接口。V1 的回滚是"再写一次旧内容并带当前 revision";V2 的回滚是"再提一条反向 change"。唯一近似快照的是迁移:V1→V2 会把五个源文件按内容指纹归档到 `.ai-novel/v1-archive/<指纹>/`(`novel-migration.ts:494`),且**不覆盖已存在的数据库**。

**与 DSH 工作区/会话 cwd 的关系**是这一块的真正门槛:

- V1 的根就是 `agent.session.header.cwd`,没有 cwd 直接抛错(`agent.ts:371-375`);
- V2 先按 cwd 调 `workspaces.resolveByPath(cwd)` 换出 `{id, path}`(`agent.ts:519-523`),再把 **workspace_id + 规范 realpath** 写进 `meta` 表(`novel-store.ts:3039-3045`);
- 之后每次打开都比对这两个值,不一致就**降级成只读**而不是报错(`:3195-3198`、`:3172-3182`),要恢复必须显式 `workspace/reattach` 或 `workspace/clone`(`:2991-3074`)——`clone` 还会给数据库换一个新 projectId 并重写所有 receipt。

这条设计的效果:把工作区目录复制一份到别处,新目录打开的是**只读项目**,不会静默写坏同一份数据。

### 审批门控:用宿主的,不自己造

只有一处,而且是纯宿主能力(`src/agent.ts:435-441`):

```ts
if (exec.name !== 'novel_apply_change') return next()
return Promise.resolve({ kind: 'ask', reason: '批准后仅修改这一个小说资产。' })
```

- **粒度**:一次调用 = 一个资产。`novel_apply_change` 的 `replacement` 是"完整替换文本"(不是补丁),审批卡片是 `card: 'diff'` 的单文件差异(`agent.ts:408-426`),标题就是模型给的 `summary`。
- **不能批量**:V1 想改 5 个文件就是 5 次调用、5 张审批卡。V2 名义上 `changes` 是数组,但 preset 协议与工具 description 都要求"恰好一条"(`agent.ts:259`、`docs/v2-development-gates.md:30`),存储层只在 `regenerationTicket` 场景硬性断言 `length === 1`(`novel-store.ts:1187-1189`)——**多条的 V2 提案在存储层是合法的,在协议层是不合法的**,这是本次读到的一处口径差。
- **拒绝后的行为**:工具返回 `isError`,磁盘零改动。`tests/agent-approval.spec.ts:76-88` 覆盖 `rejected`/`cancelled`;`:90-96` 覆盖"没有审批应答者";`:98-112` 覆盖 `policy: never` 时**连应答者都不问**。
- **UI 侧的二次门**:工作台在提交前会读会话的 `projectionValues['permissions']`,`danger-full-access` 判为 `never`、`custom` 判为 `unknown`、其它字符串判为 `ask`(`src/client/context-observer.ts:75-81`),`never`/`unknown` 直接挡住提交并给出中文原因(`src/client/workbench-store.ts:298-310`)。这说明作者知道"审批被关掉时提示词会误导模型",所以在人类入口先拦一道。
- **审批后仍需复查**:审批只保证"人同意了这次调用",不保证"文件没被别人改"。所以写路径在锁内又比了一次修订号——这是本插件最值得抄的一处细节。

### 紧凑侧边工作台

- **不是新面板、不是新路由**:一个 `shell.overlay` 里的非模态抽屉(`aria-modal="false"`,`src/client/context-view.tsx:245-255`),portal 到宿主 frame 内(`createPortal`),靠给 frame 加 class 让出列宽(`installWorkbenchLayoutReservation`,`:84-93`)。
- **尺寸**:`.aiNovelContextDrawer{width:440px;min-width:400px;max-width:calc(100vw - 80px)}`,frame 让出 `padding-right:440px`(`src/client/setup-style.ts:5-8`);≤899px 变全宽(`:50`)。
- **V2 是"接管"而不是"更宽"**:≥1360px 时 `left:386px` + 全宽(`:47`),并额外调用宿主的 `layout.acquireSidebarRail()` 租约(`context-view.tsx:202-204`);宿主没有这个 API 就**显式抛错**(`src/client/index.ts:120-128`,注释说得很清楚:不做 DOM/偏好模拟)。
- **状态存哪**:三份。① 浏览器内存里的 controller(`useSyncExternalStore`),关掉即丢;② 会话里的一条普通用户消息(生成请求与结果回读都走会话事件);③ 权威状态只在 `.ai-novel/novel.db` 或 `.ai-novel/*.json`。README.md:57 明说本地表单草稿"不是权威、刷新即失",这是刻意的。
- **与主应用前端共享代码吗?不共享**。上面已列 grep 证据;连 CSS 都是自带的 67 行 `setup-style.ts`(构建脚本还断言 client 产物里必须内联这份样式,`scripts/verify-built.mjs:20-26`)。

### 测试:41 个 spec、13 437 行,而且有几条是真契约

不是摆设。按"证明了什么"排:

| 测试 | 证明了什么 |
|---|---|
| `tests/preset-session.spec.ts:22-89` | 装好 preset 后,该 agent 的工具**恰好**是 `novel_apply_change` + `novel_read`;全局的 `ssh_exec`/`describe_image` 在它的模型请求里消失;preset 卸载后掩码恢复 |
| `tests/agent-approval.spec.ts:55-144` | 审批一次性、拒绝/取消/无应答者/`never` 四种情况磁盘零改动、审批期间外部改文件导致 `STALE_REVISION` |
| `tests/asset-approval.e2e.spec.ts:21-73` | 子进程启真 Loader 跑两个场景(初始化被拒绝 / 审批期间文件被改),读回 `approval/decided` 与 `tool/result` 事件 |
| `tests/preset-installer.spec.ts:24-71` | 同名不同内容 → `conflict` 且用户字节不变;目录/符号链接条目 → `conflict` |
| `tests/web-ui-all-composition.spec.ts:52-55` | 装了第三方 UI 插件后,**每一个**模型请求头里仍然只有那两个工具 |
| `tests/novel-store.spec.ts:229` | 过期/幂等冲突/非法 change 都不改状态 |
| `tests/novel-proposals.spec.ts:324-350` | 提案项复用已占用的 changeSetId → 项 `failed` + `IDEMPOTENCY_CONFLICT`,且不可 retry |
| `tests/workbench-browser.snapshot.spec.ts` + `tests/snapshots/` | 抽屉 UI 的序列化快照(含 v1 旧快照) |

另有一整套发布资格链(`scripts/qualify-release.mjs`,1 255 行):`pnpm pack` 出 tarball → 装进隔离 `DSH_HOME` 的 web profile → 读真实 `--dump-config` → 用 headless Chrome 走"初始化 → AI 提案 → 人工应用 → 同页刷新 → 重启读回"(`README.md:157-167`)。

## 为什么它突出

**先把星标拆开,这是本卡最重要的一节。** GitHub 星标是仓库级的,registry 把 393 记在一个 monorepo 子目录条目上,而时间线决定了这 393 基本不可能是插件的:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-04-21 | git 根提交(`initial commit for open source release`) | `git log --reverse` |
| 2026-06-20 | GitHub 仓库 `created_at`(历史比仓库更早,判断是导入/转移) | GitHub API |
| **2026-08-17** | **插件首次提交** `7a557de6` `feat: add DeepSeek Harness AI novel plugin preview (#115)` | 子目录历史 |
| **2026-08-19** | **393 星采样点** | registry ⚠ |
| 2026-08-21 | npm `0.1.0` 发布(`chore(dsh-plugin): prepare npm publication`) | npm registry `time` |
| 2026-08-23 | V2 MVP `59e2d2b4` `feat(dsh-ai-novel): add reviewed V2 authoring MVP (#139)` | 子目录历史 |
| 2026-10-18 | 品牌改名提交 `88fb1ad7` `docs(brand): rename the project to 书童 Pagekin` | 全仓历史 |
| 2026-10-22 | 插件最后一次提交 `364cecbe` | 子目录历史 |
| 2026-11-18 | 实时 2684 星;四条提交开始写"改名后的 Pagekin 仓库" | GitHub API / 全仓历史 |

采样点距插件第一次提交**只有 2 天**,距仓库创建已约 60 天;插件一共只有 8 个提交,而全仓 4 439 个。**判断:393 里没有任何可分离给这层适配的增量,应全部记在主应用名下。** 反向证据更硬:从 393 涨到 2684(约 6.8 倍)的三个月里,插件**一个提交都没有**(最后一次 2026-10-22)——涨的不是插件。

**改名对 registry 的影响,比"链接会 301"更深。**

- 实测(2026-11-18):`curl -o /dev/null -w '%{http_code} %{redirect_url}' https://github.com/EthanYoQ/AI-Novel-Writer` → `301 https://github.com/EthanYoQ/Pagekin`。旧 URL 仍能跳转,所以**人点得开**。
- 但 `package.json:5-13` 的 `repository`、`bugs`、`homepage` **三处仍写旧名**,而 `tests/package.spec.ts:26-32` 把这几个旧 URL **写成了断言**。也就是说:改名不是"文档没跟上",而是**测试把旧名字锁住了**,改一次要动测试。
- 日期边界:品牌改名在 2026-10-18;GitHub 仓库名切换没有 API 字段可读,但仓库内最早出现"改名后的 Pagekin 仓库"字样的提交是 2026-11-18 09:45(`b1bf57bf`、`a3213d32`)与 11:43(`edd84148`、`1638b136`)。**判断:GitHub 侧改名发生在 2026-10-18 之后、2026-11-18 之前**,本卡以重定向后的 `Pagekin` 为准。
- 对采集口径的实际伤害:任何**按 URL 精确匹配**的星标/下载/去重脚本,在改名后会同时看到旧名与新名两条键;而本仓 `data/plugins/` 里 `pagekin` 0 命中,说明改名还没扩散到生态文本层。

**扩散 0,原因是"垂直预设没有可复用的机制,只有可复制的产品"。**

```sh
grep -ril 'ai-novel-writer' data/plugins/ | wc -l   # → 1(只有它自己)
grep -ril 'pagekin' data/plugins/ | wc -l           # → 0
grep -ril 'ai.novel' data/plugins/ | wc -l          # → 1(同一条)
```

四条理由,按解释力排:

1. **复制单位不是代码。** 别的东西能扩散,是因为它提供了一个"接口层"(配置位置、命名约定、服务 API)。这里提供的是"小说写作流程"——抄走它需要另一套小说领域模型,而不是一个 seam。
2. **绑死在自家领域模型上。** 五类资产、阶段枚举(项目设定/架构/人物/大纲/蓝图/初稿/修订/定稿)、提案箱、章节定稿链——全部是这家产品的词汇。第三方拿去做别的垂类要从零改名,收益低于重写。
3. **它是 vendor-published,不是 community primitive。** 作者与主应用同一人,包里没有"给别人扩展用"的钩子;15 323 行里没有一行是为第三方复用设计的。
4. **门槛不在安装,在运行时。** 20 个 peer 里 17 个钉死 `0.1.0-rc.6`,外加一个 2026-08-16 的 DSH 基线 commit(`scripts/qualify-release.mjs:21`)。想跟它对齐,先得把 DSH 固定到那个代次——这压低采用,但不解释"零提及";零提及是 1+3 的结果。

**判断:明星,不是锚。** 声量在应用侧,机制在本插件侧;按本册两轴,它属于"只有声量高"的那一类,而且这份声量还不是它自己的。类内相对位置交给本目录 `README.md` 的成员表,本卡不比较。

补两个只有本插件才有的量:

- **npm 实时下载**:`https://api.npmjs.org/downloads/point/last-month/@ethanyoq/dsh-ai-novel-writer` → `1617`(窗口 2026-10-18 ~ 2026-11-16)。这是比星标更有意义的采用证据,但它**不是边车值**,只是 2026-11-18 的实时读数;⚠ 边车在 2026-08-19 那次采样里对这条 URL 没有记录,属采样缺口,不能读成"零下载"。
- **包体**:`0.1.0` 的 `unpackedSize` 378 409 字节,加上 `presets/**` 与 4 个入口;没有 `postinstall`、没有原生模块。

## 代价与边界

**失败模式,按用户实际遇到的顺序:**

1. **没装 DSH preset** → 侧栏按钮在,点开只有一段「首次使用」空白(`context-view.tsx:267-272`);模型侧**一个小说工具都不存在**(根入口不注册工具)。这不是 bug,是设计——但用户会以为插件坏了。
2. **同名 preset 冲突** → `install` 返回 `{status:'conflict', changed:false}`,并且**一个字节都不改**(`preset-installer.ts:142-157`);冲突判定包含"多一个文件""是符号链接""内容差一个字节"。用户必须自己 `diff` 后决定留谁,README.md:71 只说"inspect the existing preset"。
3. **审批不可用** → 工作台在提交前就挡住(`workbench-store.ts:303-308`);即便绕过,服务端 `never` 下不会询问应答者,工具直接 `isError`(`tests/agent-approval.spec.ts:98-112`)。**这是最容易被误判成"模型偷懒"的一类失败**。
4. **V1 编辑期间文件被改** → `STALE_REVISION`(`novel-project.ts:469-483`),用户必须重读再合;没有三路合并。
5. **V2 提案部分应用** → 逐项独立事务,失败项标 `stale`/`failed` 并**停在该项**,前面已应用的**不回收**(`novel-store.ts:2565-2622`)。README.md:59 专门提醒"不要因为一项成功就假设全成"。这是最阴的状态:半成功。
6. **提案箱满** → `maxPendingProposals` 默认 20,满了 `PROPOSAL_LIMIT_REACHED`(`:2300-2303`)。同参数重提不会新增,而是 `duplicate: true` 返回旧提案(`:2292-2299`)——防止模型"重试一次"刷爆 inbox。
7. **工作区漂移/复制** → 数据库只读,必须显式 `reattach`/`clone`(`:3195-3198`、`:2991-3074`)。`clone` 会给副本换新 projectId,旧 receipt 全部重写;`reattach` 保留身份,但等于把两处目录都指向同一项目——README 没有警告这一点。
8. **长文生成中断** → 分三种:提案没落库 = 什么都没发生;落库但没 apply = 项目状态不变,提案还在 inbox;`content` 超 `maxProposalBytes`(默认 2 MiB)= `PROPOSAL_TOO_LARGE`(`:2285-2287`)。按章节设计,一次只处理一章(README.md:37),**没有批量生成、没有自动重试、没有断点续写**。
9. **面板/布局路由** → 抽屉挂在 `shell.overlay`,不抢路由;但 V2 要求宿主的 `layout.acquireSidebarRail()`,缺失时**打开 V2 即抛错**(`client/index.ts:120-128`)。本机对照:`grep -rln acquireSidebarRail ~/.nvm/…/@deepseek-ai/dsh/` **0 命中**。
10. **DSH 版本断代(最硬的一条)** → 20 个 peer 里 17 个精确 `0.1.0-rc.6`。本机安装的 DSH 是 `0.2.1-rc.5`,其中 **6 个 peer 已不存在**:`@deepseek-ai/dsh-agent-presets`(0.2.x 改名为 `dsh-agent-preset` / `dsh-agent-preset-registry`)、`dsh-client-runtime`、`dsh-client-ui-slots`、`dsh-client-ui-primitives`、`react`、`react-dom`;`includeUserRoot`、`standingMountFor` 在 0.2.x 里也 0 命中。**判断:在 0.2.x 上装不上或客户端入口导入失败**,未实跑(见"待验证")。

**其他成本:**

- **维护已停**:README.md:3 "The `0.1.0` plugin preview is frozen. No short-term feature work is planned.";插件最后提交 2026-10-22,期间主应用发到 `1.5.0`(2026-11-18)。
- **备份陷阱**:V2 数据库与 sidecar 被 `.ai-novel/.gitignore` 排除(`novel-store.ts:18-26`),所以 `git commit` **不备份小说**;README.md:79 让你自己备份,但插件**没有导出功能**。
- **网络盘/云同步盘不支持**(README.md:81),而 SQLite 在同步盘上正是最容易损坏的场景,这一点作者是自觉的。
- **数据/隐私**:全部本地;浏览器只发 workspace UUID 与资产标识,不发路径(`src/index.ts:238-252`);模型侧读到的是有界投影(单资产 512 KiB、工作集 512 KiB、查询命中上限 20 且**配置不能调高**,`agent.ts:96-102`)。
- **没有 Code Mode / shell / 通用文件写**(两代 preset 第一行注释就写明)。这是安全选择,也意味着这个"工作台"不能做任何跨出 `.ai-novel/` 的自动化。

## 可信度与复现

- **★★★**:插件 23 个源文件全读(15 323 行里的主体),4 个 preset、2 篇 docs、`qualify-release.mjs` 头部与关键断言、8 个 spec 的关键用例;DSH 侧只用本机安装包做对照(`@deepseek-ai/dsh@0.2.1-rc.5`)。
- **★★**:`scripts/`(8 文件 2 205 行)只读了 `qualify-release.mjs` 的头部、断言标题与常量;`src/client/workbench-v2.ts` 1 544 行只读了状态机骨架。
- **未读**:桌面应用 `src/` 877 个文件(只做了"零共享"的反向 grep);`tests/` 里 33 个未点开的 spec;npm tarball 的实际内容(用 `unpackedSize` 代替)。

```sh
# 1) 克隆(旧 URL 会 301 到 Pagekin,直接用新名)
git clone --depth 1 --filter=blob:none https://github.com/EthanYoQ/Pagekin.git /tmp/an-novel
cd /tmp/an-novel && git log -1 --format='%H %ad'      # 3f24e58b… 2026-11-18
git fetch --unshallow --filter=blob:none              # 插件子目录只有 8 个提交
git log --format='%H %ad %s' --reverse -- plugins/dsh-ai-novel-writer | head -3
# 7a557de6… 2026-08-17 feat: add DeepSeek Harness AI novel plugin preview (#115)
git rev-list --count HEAD                             # 4439
git rev-list --count HEAD -- plugins/dsh-ai-novel-writer   # 8

# 2) 规模
cd plugins/dsh-ai-novel-writer
find src -type f | wc -l                              # 23
find src -type f -print0 | xargs -0 wc -l | tail -1   # 15323
ls tests/*.spec.ts* | wc -l                           # 41
ls tests/*.spec.ts* | tr '\n' '\0' | xargs -0 wc -l | tail -1   # 13437

# 3) 零扩散(在 awesome-dsh-plugin 仓库根)
grep -ril 'ai-novel-writer' data/plugins/ | wc -l     # 1
grep -ril 'pagekin' data/plugins/ | wc -l             # 0
grep -ril 'ai.novel' data/plugins/ | wc -l            # 1

# 4) 改名
curl -s -o /dev/null -w '%{http_code} %{redirect_url}\n' https://github.com/EthanYoQ/AI-Novel-Writer
# 301 https://github.com/EthanYoQ/Pagekin
grep -n 'AI-Novel-Writer' plugins/dsh-ai-novel-writer/package.json   # :7 :11 :13 三处旧名

# 5) 版本断代对照(本机 DSH)
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh
node -e "console.log(require('$DSH/package.json').version)"          # 0.2.1-rc.5
ls -d $DSH/node_modules/@deepseek-ai/dsh-agent-presets               # 不存在
grep -rln 'acquireSidebarRail' $DSH/ | wc -l                         # 0
```

## 待验证

1. **在 0.2.1-rc.5 上装一次**:`dsh plugin --profile web add @ethanyoq/dsh-ai-novel-writer` 到底停在 peer 解析、host 入口导入,还是 client 入口?本卡只做了静态对照(6 个 peer 不存在),没有实跑,也没有在 0.1.0-rc.6 上实跑。
2. **`presetRoot` 与宿主发现路径是否真的同一个目录**:默认 `$DSH_HOME/.agent-presets`(`src/index.ts:121`),但本机 0.2.1-rc.5 里 `.agent-presets` 只在一份 SKILL.md 出现过。0.1.0-rc.6 的 `includeUserRoot` 默认值未验证——若不是 true,装完 preset 也不会出现在菜单。
3. **V2 多条 `changes` 的真实边界**:协议要求恰好一条,存储层只在 `regenerationTicket` 时强制一条。手工构造两条的提案能否被 apply、会得到什么状态,未实测。
4. **`clone` 恢复的语义**:给副本换新 projectId 后,原目录与被克隆目录的提案 receipt 是否还能互相解释?代码只重写了 receipt 里的 projectId,历史 `changes` 表的 `provenance` 不重写。
5. **npm 1617 次下载的构成**:一个只有一版、2026-08-21 发布的包,月下载 1 617 是真人还是 CI/镜像?npm 不提供分解,需要按周序列拆解。
6. **改名后的去重**:本仓按 URL 精确匹配,`Pagekin` 与 `AI-Novel-Writer` 现在会指向同一仓库却不互相归并;下一轮采集前需要确认上游采集器是否跟随 301。
7. **桌面应用与插件的领域模型是否已分叉**:两边都叫"人物/章节蓝图/定稿",但 V2 的 `status` 枚举(`planned|drafting|reviewing|revising|finalized`)与主应用是否一致未核对;若已分叉,README.md:81 的"不导入 `.vela`"就只是当下的选择,不是永久边界。
