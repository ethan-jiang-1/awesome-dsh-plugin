# dsh-mnemon — 41k 行的 DSH 自有记忆框架，native 后端外包给外部 Mnemon CLI 落 SQLite

> 证据等级:★★★(源码级;`omdsh-dev/dsh-mnemon@55b8a5cf5829dc39f59738f81cbb2fe5434c8d05`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 109 为 2026-08-19 历史采样;下载 6799 同为该日。2026-11-18 实时星标 1034。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `omdsh-dev/dsh-mnemon`([registry](../../../data/plugins/omdsh-dev__dsh-mnemon.yml)) |
| 类目 | memory([census](../../ecosystem/census.py) 504 条) |
| 子分类 | `local-store`——**判断:默认形态成立,但它有一个可插拔 Provider 端口**(见下) |
| 自述 | 「跨 Agent、本地优先的持久记忆;运行时记忆、可检索项目档案、语义召回、知识图谱、Sidebar UI」 |
| 星标 ⚠ | **109**(2026-08-19 冻结采样);**1034**(2026-11-18 实时,约 9.5 倍) |
| 下载 ⚠ | **6799**(2026-08-19;边车无 `start/end` 窗口字段,不能读成"周下载"或"总下载") |
| 扩散 | **5**(口径见末节:`grep -ril 'mnemon' data/plugins/` 命中 7 条 − 自身 1 − 同名词误命中 1) |
| 仓库 commit | `55b8a5cf`(2026-11-18 04:29:40 +0800,`Merge pull request #678 … release-v0.5.48-final`),仓库创建 2026-08-10 |
| 包形态 | npm `dsh-mnemon@0.5.48` + **18 个独立发版的子包**(4 Source / 5 Strategy / 9 Provider);`dsh.bundle.patch` + `dsh.client.platform: web` |
| 代码规模 | `src/**/*.{ts,tsx}` 214 文件 **41 340 行**(不含测试)+ `plugins/*/src` 159 文件 **28 740 行**;测试 **66 192 行**;`docs/**/*.md` 650 个 |
| 外部依赖 | 记忆内容面依赖外部 Go 程序 `mnemon`(`@mnemon-dev/mnemon`,npm/brew/go 三种装法);DSH 侧 0 行 SQL |

## 它到底是什么

**先回答"谁依赖谁",因为这张卡的标题容易被读反。**

`dsh-mnemon` 不是某个记忆服务的适配层,而是**一个自带 41k 行、把一个外部 CLI 当可选存储引擎的 DSH 原生记忆框架**。两个方向都要说清:

- **DSH 插件 → Mnemon CLI(硬依赖,但只限一条路)**:Memory Spaces 的默认 Provider `mnemon-native` 每次操作都 spawn 一个 `mnemon` 子进程,命令面是 `status` / `recall` / `search` / `remember` / `import` / `forget` / `related` / `link` / `show` / `viz`(`plugins/dsh-mnemon-provider-mnemon-native/src/driver.ts:126-403`)。CLI 找不到时**只有这一个 Source 变灰**,运行时记忆与项目档案照常工作(`plugins/dsh-mnemon-source-memory-spaces/src/service.ts:591-593`:native space 只在 `commandFound` 为真时进 `active`)。
- **Mnemon CLI → DSH 插件(无依赖)**:CLI 是独立的 Go 仓库(`go install github.com/mnemon-dev/mnemon@latest`,`docs/en/guides/installation.md:202`),npm 包名 `@mnemon-dev/mnemon`,站点 `mnemon.dev`。本仓库只有 `bin/repair-legacy-session.mjs` 一个可执行脚本,**不含 CLI 源码,也不 import 它**(`dependencies` 里没有该包,`package.json:156-179`)。

所以它不是"某产品的插件",而是**这套记忆产品在 DSH 里的本体**;Mnemon 是它选定的本地引擎。

**四个真实分型(自述的四项正好对应四个 Source,不是四句形容词)**:

| Source | 数据模型 | 是否本地 | 落到哪 |
|---|---|---|---|
| Runtime memory | `memories.json` 为真源 + `USER.md` / `MEMORY.md` 两个投影 | 是 | `<root>/runtime/`(`plugins/dsh-mnemon-source-runtime/src/contracts.ts:168-172`) |
| Project Documents | 每条一个 Markdown + `index.json` 索引 | 是 | `<root>/documents/`(`plugins/dsh-mnemon-source-documents/src/contracts.ts:79-87`) |
| Memory Spaces | 每空间一个 SQLite `mnemon.db`,外加 DSH 侧一份空间注册表 | 默认是,**可换 8 个第三方**(2 本地 / 6 远端) | `<root>/data/<spaceId>/mnemon.db`(`plugins/dsh-mnemon-source-memory-spaces/src/contracts.ts:733-737`) |
| Skills(实验) | DSH 的 `SKILL.md` + 版本 / 用例 / 进化轨迹 | 是 | `<root>/…`,自述明说"不进备份"(`README.md:154`) |

**核心循环不是"召回 → 注入",而是"组合 → 冻结 → 超期作废"**:

1. 每个 Source 报 facts(能力、路由、action、revision)(`src/core/composition.ts:595-613`);
2. 选中的 **Strategy** 用这些 facts 纯函数式地提出一个 `ViewSpec`;Core 会**把 compose 跑两遍并比对 canonical JSON**,不相等就判定"Strategy 非确定性"并拒绝(`composition.ts:641-646`);
3. Core 校验成一份**不可变 View**(`deepFreeze({ id: 'view:<digest>', … })`),连同 `ReadGrant`(本轮能读哪些空间)一起钉在这一轮(`composition.ts:711`、`:719-720`);
4. 轮末由 `agent/turn-stopping` 收尾,触发受限的 idle review(`src/host/lifecycle.ts:452-465`);
5. 下一轮重新组合,旧快照**被退休**而不是叠加(见"关键实现")。

这套分层是它对 DSH 的真正贡献:Source / Strategy / Provider 都是**普通 Cordis 插件**,靠 `ctx.mnemonMemory` 注册(`src/core/runtime.ts:15`:`context.provide('mnemonMemory', runtime.service)`),不是靠改核心。

## 怎么接进 DSH

**manifest 是双层声明,不是一层。** `package.json:114-131`:

```json
"dsh": {
  "bundle": { "patch": "./cordis.patch.yml" },
  "client": { "inject": [ …8 个 @deepseek-ai/dsh-client-ui-* / connection / locale 包… ], "platform": "web" }
}
```

- `dsh.bundle.patch` 由 `dsh-app-boot` 读(`$DSH/node_modules/@deepseek-ai/dsh-app-boot/lib/index.js:517-519` 校验类型、`:530` 解析成绝对路径)。
- `dsh.client` 由 `dsh-client-modules` 读:必须有 `platform`,并要求包导出 `./client`(`$DSH/node_modules/@deepseek-ai/dsh-client-modules/lib/index.js:64-71`、`:732-738`)——本包对应 `package.json:76-79` 的 `exports["./client"] → ./lib/client.js`。**Sidebar UI 就是经这条通道进浏览器的,不是 Host 侧的 HTML 注入。**

**`cordis.patch.yml` 只有一个 `insert`,里面是一个 group + 10 行**(`cordis.patch.yml:12-96`):`mnemon-bundle`(`group: true`,`name: dsh-mnemon/bundle`)、核心行 `mnemon`、4 个 Source、1 个默认 Strategy、3 个默认关的增强 Strategy、1 个默认关的 General Strategy。9 个 Provider 不是 loader 行,而是 memory-spaces 行 config 里的 `providers:` 子项(`cordis.patch.yml:44-70`),由 `src/starter-resolution.ts:11-34` 在子 Entry import 之前把依赖闭包做可见。

那个 `disabled:` 表达式值得单说:它读**另一个 Entry(`id: mnemon`)的 `options.disabled`**,而不是自己的有效状态(`cordis.patch.yml:15-20`)。注释写明了原因——避免"祖先门控递归";`src/bundle.ts:17-70` 还专门处理一件事:如果用户又单独装了 stock strategy bundle,就从 profile manifest 里把重复的 `bundles` 摘掉并把旧 Entry `unlink()`,否则 Loader 的下一次 reconcile 会把共享 Entry 删掉。

**绑的事件(全部在 `src/host/lifecycle.ts:283-296`,每个 Agent 一份,注册点 `:911` 的 `agent/created` + `prepend: true`)**:

| DSH 事件 | 去向 | 干什么 |
|---|---|---|
| `session/event` | `sessionEvent` | 跟踪 turn/step 边界与工具计数(`lifecycle.ts:499-516`) |
| `system-prompt/assemble` | `assemblePrompt` | 组合本轮 View,并挂三节 system prompt:strategy / routing / snapshot-history(`src/host/guidance.ts:18-24`) |
| `agent/pre-step`(`prepend: true`) | `preStep` | 把本轮 View 的 Wake 作为**一条 user 消息**追加到批次末尾(`lifecycle.ts:387-431`) |
| `agent/request`(`prepend: true`) | `prepareReviewAccess` | 在真正发请求前裁定 idle review 的准入(`lifecycle.ts:467-498`) |
| `agent/turn-stopping` | `finishTurn` | 释放 View、记轮、排 idle review(`lifecycle.ts:452-465`) |
| `tools/pre-execute` | `registerMemoryWriteApproval` | 写入审批门(`src/host/write-approval.ts:11`) |

另外还有一次性注册:`ctx.tools.register`(16 个工具,`src/host/tools.ts:71-118`)、`ctx.commands`(`src/host/commands.ts`)、`ctx.systemPrompt.section(order 150)`(`guidance.ts:29-36`)、`connection`/`webServer` 上的 RPC(`src/host/plugin.ts:191-224`)。

**service key 用的是自己新开的一个,不是 `ctx.memory`。** `provide = ['mnemonMemory']`(`src/host/plugin.ts:40`),`inject = ['tools','settings','commands','agents','subagents']`(`:41`)。第三方 Source/Strategy 写 `inject: ['mnemonMemory']` 即可挂上(`src/sdk/install.ts:41`、`src/sdk/service.ts:34`)。**这条是它跟 DSH 生态的 ABI,比工具名更硬**——扩散里确实有第三方按这个 SDK 写 Provider(见"为什么它突出")。

**注入的是 user 消息,不是 system prompt。** `source: { kind: 'dsh-mnemon', form: 'recall' | 'instructions' | 'memory-snapshot' | … }`(`src/host/plugin-message.ts:6-37`);历史兼容三种形状(`kind` / `plugin:dsh-mnemon` / `kind: 'plugin'` + `plugin`,`:19-24`)。策略文本走 system prompt 的三个 section,证据走 user 消息——两路分开是刻意的(`guidance.ts:12-15` 的注释:View 是"自己的消息",不进共享上下文快照)。

## 关键实现

```
src/                       41 340 行 / 214 文件
  host/plugin.ts            225  唯一 apply():live 设置、runtime swap、RPC、工具、命令
  host/lifecycle.ts       1 717  每 Agent 的事件绑定、快照退休、idle review、容量维护
  host/subagent.ts        1 364  子 Agent 协调(task Agent、结果 schema、收据)
  host/git-sync.ts        1 837  Git sync:发布 Pack 到自有仓库
  host/pack.ts            1 324  Mnemon Pack(ZIP,fflate)导出/预览/导入
  host/reconcile.ts         444  "记忆和解"提案(模型出操作、人批准才写)
  host/memory-snapshot.ts   122  快照退休与替换(MAX_SNAPSHOTS=4 / 64 KiB)
  host/tools.ts             582  16 个工具的定义与生命周期式注册
  core/composition.ts     1 043  Source facts → Strategy → 不可变 View(双重确定性校验)
  client/index.ts           558  slots 注入、Sidebar、turnTail、assistant-actions
  client/native-sidebar.tsx 133  'sidebar.panellist' 原生入口(id 'mnemon',order 30)
plugins/                   28 740 行 / 159 文件 / 18 个独立包
```

**数据流(四条,别混)**:

```
① 每轮 View(读):DSH turn 开始
   pre-step → AgentMemoryTurn.begin(turn)            src/host/agent-memory-turn.ts:137-166
     → executions.turn() → Composition(所有 Source 的 facts/project)
     → Strategy.compose()(纯函数,跑两遍比对)      src/core/composition.ts:641-646
     → 冻结 View + ReadGrant,钉到 turn 号
     → Wake 文本作为一条 user 消息追加                src/host/lifecycle.ts:387-431

② Runtime memory(常驻):memories.json → USER.md/MEMORY.md 投影
   agent/turn-stopping 后 idle review 才可能写;写入前取 .memories.lock(wx + 30s 过期)
                                                    plugins/dsh-mnemon-source-runtime/src/controller.ts:880-903

③ Memory Spaces(按需):工具/Route 调用 → spawn mnemon 子进程
   --data-dir <root> --store <spaceId>               plugins/dsh-mnemon-source-memory-spaces/src/runner.ts:96-101
   → <root>/data/<spaceId>/mnemon.db(SQLite)         plugins/dsh-mnemon-source-memory-spaces/src/contracts.ts:733-737
   → 所有调用经 withMemoryStorageLock(root) 串行化    src/sdk/storage-lock.ts:10-16

④ 跨机器:Pack(ZIP)或 Git sync → 另一端导入 → 冲突走"和解提案"
                                                    src/host/reconcile.ts:1-16
```

**四块能力分别落在哪(这是本卡最该被引用的对照)**:

| 块 | 模块 | 触发 | 有无 embedding |
|---|---|---|---|
| 运行时记忆 | `dsh-mnemon-source-runtime` | 每轮常驻投影 | 无,纯文本 |
| 项目档案 | `dsh-mnemon-source-documents` | `mnemon_document_search` 等 | **无**——词法检索,中文按二字滑窗切分(`plugins/dsh-mnemon-source-documents/src/search-tokens.ts:1-15`),打分是子串权重 + token 覆盖(`plugins/dsh-mnemon-source-documents/src/controller.ts:266-312`) |
| 语义召回 | `dsh-mnemon-source-memory-spaces` + native Provider | Strategy 的 recall 配额 | **有,但 embedding 由外部 CLI 算** |
| 知识图谱 | 同上,`graph()` / `related()` / `link()` | 图谱页与工具 | 无,读 CLI 的 viz 输出 |

**embedding 到底在哪算**:不在 DSH 里。DSH 只是把三个环境变量传给 CLI——`MNEMON_EMBED_ENDPOINT` / `MNEMON_EMBED_MODEL` / `MNEMON_EMBED_PROTOCOL`(必要时加 `MNEMON_EMBED_API_KEY`,`plugins/dsh-mnemon-source-memory-spaces/src/runner.ts:74-86`),默认值是 `http://localhost:11434` + `nomic-embed-text`(`plugins/dsh-mnemon-source-memory-spaces/src/contracts.ts:540-541`),而且**默认关闭**(`cordis.patch.yml:35-38`:`enabled: false`)。真正打 `/api/embed` 的是那个 Go 程序;仓库里的测试用本地假 Ollama 证明了这条链路(`plugins/dsh-mnemon-provider-mnemon-native/tests/provider.spec.ts:294-350`,测试里直接 `MNEMON_EMBED_ENDPOINT=http://127.0.0.1:<port>`)。

**语义召回不是"把相似度丢给模型"**,而是插了一段质量策略:native Provider 把 CLI 的混合分换成 `signals.similarity`,再夹到 `[0,1]`,`superseded` 的条目还要再降(`driver.ts:245-266`);Source 侧 `strict-v1` 按 0.25 / 0.6 两阈值分成 low / medium / high / ranked / unknown 五档(`plugins/dsh-mnemon-source-memory-spaces/src/recall-quality/policies.ts:15-36`、`cordis.patch.yml:39-46`)。测试里有一个正好说明为什么必须换:CLI 的混合分把相似度 1.0 的正确条目打到 `score < 0.6`,换成分数后升到第一(`provider.spec.ts:336-341`)。

**知识图谱是"解析别人家的 HTML"**:`viz --format html --output -` 拿到可视页,用**正则**抠 `vis.DataSet` 的节点/边,不执行 HTML、不加载 CDN 脚本(`driver.ts:68-109`);边的四种颜色映射成 `temporal/semantic/causal/entity`(`driver.ts:71-76`)。整库读上限被单独抬到 128 MiB,因为约 1000 条 insight 就会产出 3–9 MB(`driver.ts:6-12`)。

**多 Agent 并发怎么裁决(按介质分四层,不是一句话)**:

1. **进程内、同根目录的 CLI 调用全局串行**:`withMemoryStorageLock(dir)` 是模块级 `Map<dir, Promise>` 队列(`src/sdk/storage-lock.ts:3-16`),注释明说"文件锁仍负责跨进程安全"(`:7`)。
2. **跨进程的运行时记忆**:`.memories.lock` 用 `openSync(..., 'wx')` 独占创建,超过 30 s 视为死进程遗留可抢占(`plugins/dsh-mnemon-source-runtime/src/contracts.ts:174-176`、`controller.ts:880-903`)。
3. **跨进程的 Mnemon store**:交给 SQLite 与 CLI。仓库只在注释里交代后果——串行化是为了避免并行 status/viz 撞上 store 迁移产生瞬时 `SQLITE_BUSY`(`plugins/dsh-mnemon-source-memory-spaces/src/runner.ts:92-95`)。
4. **DSH 自己的元数据**:分两种,`documents/index.json` 有**乐观锁**(index revision + 文件内容 hash,不匹配抛 `revision-conflict`,`plugins/dsh-mnemon-source-documents/src/controller.ts:369-371`、`:387-389`);`data/.dsh-memory-bodies.json` 则只是 mtime 变更检测 + 原子 rename,即 last-writer-wins(`plugins/dsh-mnemon-source-memory-spaces/src/memory-spaces.ts:909-935`)。
5. **跨机器**:不是合并,是**提案**——模型读合并后的本地记忆产出 ≤40 条操作,人接受才落地(`src/host/reconcile.ts:1-16`、`MAX_RECONCILE_OPERATIONS=40`)。

**与 DSH 会话/工作区怎么绑**:`agentScope()` 把 `storageScope` + `session.header.cwd` + `sessionId`/`agentId` 拼成 scope(`src/host/runtime.ts:46-49`);存储根由 Host 统一注入到每个默认 Source 的 `dataDir`(`runtime.ts:69-90`),所以 Source 自己不知道 scope 语义。工作区可用黑名单排除,子 Agent **继承父的工作区判定**,哪怕 cwd 不同(`src/host/config/paths.ts:95-114`)。子 Agent 拿的是父轮**捕获的** View,不是实时读(`src/host/agent-memory-turn.ts:122-133`;契约测试 `tests/turn-view-host.spec.ts:259`:"injects the captured parent View after the parent finishes and newer memory is stored")。

**测试能证明的契约(66 192 行,只列点到的)**:
- `tests/lifecycle.spec.ts:174` "pins one immutable Wake across every model step and releases it at the turn boundary" —— 一轮一个 View,不是一步一个。
- `tests/turn-view-host.spec.ts:409` / `:461` —— 退休遗留快照、纠正/删除后立刻 checkpoint。
- `plugins/dsh-mnemon-provider-mnemon-native/tests/provider.spec.ts:294-350` —— 真 CLI + 假 Ollama:store 落在 `<dir>/data/work/mnemon.db`,只读检查**不改动数据库字节**(`expect(await readFile(database)).toEqual(before)`)。

## 为什么它突出

**先确认星标归属:这个仓库只有 DSH 一个宿主,不存在"把母项目光环借给插件"的口径问题。**

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-10 | 仓库创建 | GitHub API `created_at` |
| 2026-08-19 | **109 星采样点**(创建后第 9 天) | 边车 `data/stars.json` |
| 2026-11-18 | **1034 星**、73 fork、21 open issue、299 458 KB | GitHub API(实时) |

README 第一行是 "Composable, view-based context for DeepSeek Harness.",`engines.dsh` 直接写死 DSH 版本区间(`package.json:50-52`),仓库里没有任何第二个 harness 的适配目录。所以 1034 星可以整份记在这套 DSH 记忆实现头上,不需要按子目录再做一次归属剥离:**109 → 1034 是同一个对象在 100 天内涨的。**

增长本身也有机制解释:9 天内 109 星说明发布即被看见,而 v0.5 之后它把"记忆"从单一插件改成了**可组合框架 + 插件市场式安装**(任意 Source/Strategy 都是普通 Cordis 插件,装了就长出自己的设置页与开关,`README.md:150-160`),这正好给了下游"我能写一个自己的 Provider"的入口。

**扩散:7 条命中,逐条判定后是 5 条第三方、其中 4 条明文依赖。**

| 条目 | 判定 | 依据(条目自述) |
|---|---|---|
| `summerscar/dsh-plugins#dsh-mnemon-sync` | **真衍生(备份层)** | 备份/恢复 dsh-mnemon 的三类组件;`node:sqlite` 的 `backup()` 复制在线库、SHA-256、恢复前删 `-wal/-shm`。它读的是本插件的**存储布局** |
| `OverDustD7/dsh-experience-recall` | **真衍生(读同一份库)** | "需要本机 Ollama 以及 dsh-mnemon 记忆库与 mnemon CLI;缺了只观察不注入" |
| `yhPrime/dsh-exp-lib-provider` | **真衍生(接 SDK)** | "需先安装 dsh-mnemon。经验库记忆空间 Provider",注册 `exp_recall` 等工具——走的是 `provider-sdk` 那一层 |
| `OverDustD7/dsh-home-sync` | **真衍生(搬数据目录)** | "同步 DSH 主目录与 Mnemon 记忆数据",冲突时推送前停下。类目是 git,不是 memory |
| `iwtown/dsh-llm-wiki` | **弱提及** | 只在管线列举里出现 "mnemon memory sync",没有一个字说依赖关系;按弱集成记,不计入硬扩散 |
| `wangzhanchao883/dsh-word-vault` | **同名误命中** | 命中的是 "mnemonic hook"(背单词的记忆钩子),与本插件无关 |
| `omdsh-dev/dsh-mnemon` | 自身 | — |

结论:**5 条第三方,4 条硬依赖**。比"话题热度"更有信息量的是依赖的**层次不同**——有人接存储布局(备份)、有人接数据目录(同步)、有人接 `provider-sdk`(扩展)、有人接 CLI(读同一份库)。**四种接法说明扩散发生在"存储约定"这一层,而不只是抄 UI**,这跟"共用一份配置才算标准"的判据一致。用更严的 token 复核:`grep -rl 'dsh-mnemon' data/plugins/` 命中 4 条(自身 + 3 条硬依赖),与上表 4 条硬依赖吻合。

**判断:锚,不是明星。** 声量(同一仓库 100 天 109→1034)与扩散(4 条硬依赖)两轴都成立,且扩散接的是自己定义的 ABI(`ctx.mnemonMemory` + `provider-sdk` + 目录布局)。子分类仍归 `local-store`,但理由要写清:

- **算 local-store 的证据**:断网可用(Runtime/Documents 是纯本地文件,语义召回默认打本机 11434,CLI 是本地二进制);数据路径用户可见且可切换四种 scope(`src/host/config/paths.ts:38-46`:global `~/.mnemon` / workspace `<ws>/.mnemon` / custom / 按工作区哈希隔离),Status 页能逐目录报字节与条目数(`src/host/storage-scope.ts:134-170`)。
- **跟 `host-backed` 的张力**:SQLite 的 schema、SQL、向量检索全在那个 Go 程序里,**本仓库 0 行**;而且 9 个 Provider 里 6 个是远端/自建 HTTP 服务(`docs/en/guides/memory-providers.md:18-26`),一旦选了它们,数据就不在本地了。所以准确说法是:**存储根与元数据由插件拥有、内容引擎外包、后端可切换**——默认落 `local-store`,但不是"纯自研存储"。

## 代价与边界

- **隐私:默认不出网,但出网点比自述多。** 默认路径下(三个本地 Source + native Provider + embedding 关)没有任何必需的网络调用;`src/` 与 `docs/` 里也 grep 不到 telemetry/analytics。但下面每一条都是真实出口:
  - ① 开 embedding 后会把**记忆正文与查询**发给 `endpoint`(`plugins/dsh-mnemon-source-memory-spaces/src/runner.ts:74-86`);默认是本机 Ollama,改成远端就是上传。
  - ② 换第三方 Provider:OpenViking / Honcho / mem0 / Hindsight / RetainDB / Supermemory 走各自的远端或自建 HTTP 服务(要填 `endpoint` + `apiKey`);Holographic(本地 JSON)与 ByteRover(本地 CLI)不出网。
  - ③ Git sync 把 Pack 发布到**你自己名下的仓库**(`README.md:155`)。
  - ④ skill 市场会检索 skills.sh / GitHub / Agent Skills 站点(自述,`README.md:88`)。
  - ⑤ 版本检查与 `mnemon update` 走 npm(`docs/en/guides/operations.md:36-42`)。
  - ⑥ idle review / Save-to-memory / 和解会**调用模型**(`src/host/lifecycle.ts:650` 起):会话内容会进模型 API。这一条与 DSH 本身一致,但记忆插件多了一层后台触发。
- **凭据边界**:embedding 的 key 有三种落法——内联 `apiKey`、环境变量名 `apiKeyEnv`、指向 Host credentials 的 `apiKeyRef`(`plugins/dsh-mnemon-source-memory-spaces/src/config.ts:100-105`);CLI 侧一旦失败,`MNEMON_EMBED_API_KEY` 会在错误信息里被替换成 `[redacted]`(同文件 `runner.ts:124`)。Pack 不含 Provider 凭据(`docs/en/reference/configuration.md:342`)。
- **外部二进制是最硬的边界。** 没有 `mnemon` 就没有 Memory Spaces(哪怕数据都还在盘上):`commandFound=false`(`plugins/dsh-mnemon-source-memory-spaces/src/native-cli.ts:205-267` 依次找 `cliPath` → `MNEMON_CLI_PATH` → PATH → 四个常见路径),native space 直接不进 `active`,`providerReady` 变 false,View 的 revision 也跟着变(`service.ts:591-612`)。恢复要靠装 CLI 或改 `cliPath`,不是重启插件就行。
- **失败模式,按发生顺序**:
  1. **CLI 不在**:Memory Spaces 静默降级为"只 inspect",recall/remember 工具不出现,会话照常跑(Source facts 失败只记 diagnostic 并标 `unavailable`,`src/core/composition.ts:600-610`)。用户要主动看 Status 才知道。
  2. **单次 CLI 超时**:默认 `timeoutMs: 10000`(`cordis.patch.yml:33`),`runProcess` 先 SIGTERM、1.5 s 后 SIGKILL(`plugins/dsh-mnemon-source-memory-spaces/src/providers/process.ts:56-62`)。整库读(snapshot/viz)另有 128 MiB 输出上限,但**超时仍是同一个 10 s**——大库上第一次打开图谱页有实际风险(未实测)。
  3. **输出被截断**:默认 2 MiB 上限,超限按 `output-limit` 失败而不是返回半个 JSON(`plugins/dsh-mnemon-source-memory-spaces/src/providers/process.ts:76-85`)。
  4. **CLI 版本旧**:`<=0.1.2` 不认 `--verbose`,代码先跑一次、只在错误信息精确匹配 `unknown flag: --verbose` 时回退老参数,且**取消/IO 错误不重试**(`driver.ts:226-238`;测试 `provider.spec.ts:129-165`)。
  5. **索引/注册表损坏**:`documents/index.json` 解析失败会报 `invalid` 并给出 issue(`storage-scope.ts:89-103`);删除操作前还会校验托管路径不能越界(`plugins/dsh-mnemon-source-documents/src/controller.ts:376-384`);运行时记忆的投影缺失会标 `invalid` 但数据仍在 `memories.json`。
  6. **并发写冲突**:Documents 抛 `revision-conflict` 失败关闭(`controller.ts:369-371`);空间注册表是 last-writer-wins,后写覆盖先写。
  7. **store 满**:native `rememberMany` 会处理"导入后 CLI 自动剪掉最弱条目"的情况,包括"我复用的那条副本正好被剪掉"要重新导入(`driver.ts:307-321`,issue #339)。
  8. **DSH 版本跨度**:`engines.dsh` 只覆盖 `0.2.0-rc.2 ~ 0.2.2`(`package.json:50-52`),`0.2.1` 一行是显式区间;超出区间不保证事件/工具签名仍匹配。
- **维护成本**:18 个包独立发版、一个 `pnpm verify` 串起 docs 校验 / 双次 typecheck / 确定性构建 / 每包测试 / headless profile / 包内容与导出面校验(`package.json` 的 `scripts.verify`)。`src/host/lifecycle.ts` 单文件 1717 行、`git-sync.ts` 1837 行,读改都重。
- **上下文成本**:一轮的 View 是完整快照,但历史只留 **4 份 / 64 KiB**(`src/host/memory-snapshot.ts:7-9`),旧快照用 shadow 节点退休、原文进 append-only 审计(`:113-118`)。这是"不无限追加"的设计,代价是**模型看不到更早的快照**——所以 guidance 里专门写了一节,说明"更新的一份取代更早的,缺席不等于删除"(`src/host/guidance.ts:9`)。
- **配额会静默截断**:三分层默认每轮 Documents 1 次查询 / 4 条 / 6 000 字符,Recall 2 次查询共享 6 条 / 4 800 字符(`plugins/dsh-mnemon-strategy-default-three-tier/src/retrieval.ts:68-76`),超预算的查询返回 `budgetExhausted` 并在 hint 里告诉模型"空结果不代表没有"(`retrieval.ts:283-289`)。没读 hint 的模型会把"没配额"读成"没记忆"。
- **信任模型**:官方明说 Source/Strategy 是进程内受信 JS,不做沙箱(`README.md:157`),即装一个第三方 Provider 等于给它同等权限。

## 可信度与复现

**★★★,范围限定**:DSH 侧 Host/Core/Client 结构、CLI 调用面与并发/锁、四块能力的落点、失败模式的代码路径,都是逐文件读出来的;行号已抽查过 `src/host/plugin.ts:39-41`、`src/host/lifecycle.ts:283-296`、`src/host/runtime.ts:69-73`、`src/core/composition.ts:600-610`、`plugins/dsh-mnemon-source-memory-spaces/src/runner.ts:96-101`、`src/client/native-sidebar.tsx:100-108` 等 8 处。

**未读**:`git-sync.ts`(1837 行)只读了 Pack/reconcile 的入口语义,没读它的 Git 传输与冲突判定细节;`subagent.ts`(1364 行)、`pack.ts`(1324 行)、`lifecycle.ts` 的 idle review 与容量维护主体、`src/client/**` 的 30 多个页面组件、以及 650 个 docs 里的绝大部分;**Mnemon CLI 本体(Go)完全未读**,凡涉及 SQL schema、分块、混合检索权重的句子都是"从客户端可见面反推",不是引擎事实。

```sh
# 1) 克隆与提交(仓库约 292 MiB,必须收窄)
git clone --depth 1 --filter=blob:none https://github.com/omdsh-dev/dsh-mnemon.git repo
cd repo && git log -1 --format='%H %ad %s'
# → 55b8a5cf5829dc39f59738f81cbb2fe5434c8d05  Wed Nov 18 04:29:40 2026 +0800
#   Merge pull request #678 from omdsh-dev/codex/release-v0.5.48-final

# 2) 规模
find src \( -name '*.ts' -o -name '*.tsx' \) ! -name '*.test.*' | xargs wc -l | tail -1   # → 41340
find plugins -path '*/src/*' \( -name '*.ts' -o -name '*.tsx' \) ! -name '*.spec.*' | xargs wc -l | tail -1  # → 28740
find tests plugins -name '*.spec.ts' -o -name '*.spec.tsx' -o -name '*.spec.mjs' | xargs wc -l | tail -1      # → 66192
ls plugins | wc -l                                                                    # → 18

# 3) CLI 面与存储布局
grep -n "data-dir\|--store" plugins/dsh-mnemon-source-memory-spaces/src/runner.ts
grep -n "MEMORY_SPACE_DATABASE_FILE\|MEMORY_SPACES_DIRECTORY" plugins/dsh-mnemon-source-memory-spaces/src/contracts.ts
grep -n "MNEMON_EMBED" plugins/dsh-mnemon-source-memory-spaces/src/runner.ts        # → :53, :80-84

# 4) 扩散(在 awesome-dsh-plugin 仓库根)
grep -ril 'mnemon' data/plugins/ | wc -l        # → 7
grep -ril 'mnemon' data/plugins/                # 逐条判:5 第三方 / 1 自身 / 1 "mnemonic" 误命中
grep -rl 'dsh-mnemon' data/plugins/ | wc -l     # → 4(自身 + 3 条硬依赖)

# 5) 星标实时值(2026-11-18)
curl -s https://api.github.com/repos/omdsh-dev/dsh-mnemon | grep -E '"created_at"|"stargazers_count"'
```

## 待验证

1. **图谱页在真实体量下的可用性**:`viz --format html` 走的是 10 s 超时 + 128 MiB 输出上限(`driver.ts:12`、`cordis.patch.yml:33`)。1000 条 insight 的库实际要多久、会不会整页失败,我没有可跑的真 CLI 实例。
2. **`mnemon.db` 的 schema 与并发语义**:SQLite 是不是 WAL、写事务粒度、两个进程同时 `remember` 时谁赢——全在 Go 侧,本卡只能引用仓库注释。
3. **混合检索的权重**:`signals.similarity` 之外 CLI 还用 BM25?向量模型缺失时怎么退化?`recall --verbose` 的 `score` 与 `similarity` 到底怎么算,未验证。
4. **embedding 开与不开的召回质量差**:默认 `enabled: false`(`cordis.patch.yml:36`),此时 "语义召回" 实际上退化成 CLI 的混合检索。README 把 semantic recall 当卖点,但**默认配置下没有向量**——这一条值得实测对比。
5. **Git sync 的冲突判定**:`docs` 说两台机器写同一主题会"两种写法都留着,直到接受和解方案",但 `git-sync.ts` 的 diff/conflict 生成我未读。
6. **idle review 的实际模型成本**:默认 `idleReviewMs: 30000`(`cordis.patch.yml:29`)、自动采纳默认关,但一次 review 用哪个模型、多少 token,只能从 `runtimeMemory.maintenanceMaxTokens` 看到一个上限。
7. **`dsh.client.inject` 列的 8 个包是否都是硬需求**:少装其中一个 UI 包时是降级还是整个客户端不加载,未在真 WebUI 里验。
