# dsh-tongflow — dsh 面只有 1 039 行:19 个工具、一个会话视图 tab、一条 patch 行,引擎全在 Python 侧

> 证据等级:★★★(源码级;`tong-io/tongflow@f7aae7743b3046ebd783f4e704d454ebe3566f2d`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 860 为 2026-08-19 历史采样,**仓库级、属 TongFlow 主项目**;2026-11-18 实时 1047。⚠ 下载 0 同为 2026-08-19。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `tong-io/tongflow#dsh-tongflow`(monorepo 子目录 `packages/dsh-tongflow`)([registry](../../../data/plugins/tong-io__tongflow--packages-dsh-tongflow.yml)) |
| 类目 | workflow([census](../../ecosystem/census.py) 703 条 / 全表 11 744 条) |
| 子分类 | `external-engine`(挂外部引擎) |
| 自述 | 「影视片场」:agent 写 `.tongflow.json` 工作流 → TongFlow 插件执行;内嵌画布、镜头/角色/take 布局、漫剧模板、`@tongflow` 会话进 Studio。**「漫剧模板」已过时**:模板在 2026-08-19 被删(`6ba7fbc`,见末节) |
| 星标 ⚠ | **860**(2026-08-19 采样);2026-11-18 实时 **1047**、fork 136。**属 TongFlow 主项目,不属本适配层**——采样点距本子包首个提交 ≤1 天 |
| 下载 ⚠ | **0**(2026-08-19;口径为 npm 近 30 天窗口,且 `data/downloads.json` 只覆盖 11744 中的 624 条 → **采样缺口**,不可读成「无人使用」) |
| 扩散 | **0**(口径:`grep -ril 'tongflow' data/plugins/` 命中 1 条,即自身;`dsh-tongflow`、`@tongflow` 同样各命中 1) |
| 仓库 commit | 整仓 `f7aae77`,2026-11-13;子目录最后提交 `780f0a1`,2026-11-11 `chore(release): prepare 1.0.0`;仓库 2026-04-08 创建、2026-06-16 首个开源提交 |
| 包形态 | npm `dsh-tongflow@1.0.0`(2026-11-12):Cordis **bundle** — `dsh.bundle.patch` → `cordis.patch.yml`(1 条 insert),`dsh.client` 声明 `platform: web` + 8 个注入包;unpacked 14.6 MB / 14 文件,13 个 peer |
| 代码规模 | dsh 面 `packages/dsh-tongflow/src` **1 039 行 / 9 文件**;整包(含测试、skills、docs)2 385 行;构建期内联的宿主无关 studio `packages/tongflow-studio/src` **9 804 行**;主项目 747 个 git 文件、TS/TSX 69 996 行、Python SDK(`sdk/`)8 302 行 |

## 它到底是什么

**一句话:这不是一个插件,是一个三层产品压在一个 monorepo 里的最外一层。**

三层(`packages/dsh-tongflow/README.md:9-13` 自己这么分,docs/design.md:5-29 有同构的分层图,下面是我按源码核对的职责):

- **dsh 面**(`packages/dsh-tongflow`,1 039 行):把 studio 建起来、把 19 个 host-neutral 工具转成 `defineTool`、注册一段 system prompt、注册一个 skill provider、挂 `/tongflow/*` 路由、注册两个浏览器 slot、按 `@tongflow` 激活。就这些。
- **宿主无关 studio**(`packages/tongflow-studio`,9 804 行):projects / 文件树 / 工作流文件 / run 管理 / 插件仓库 / 画布页 / MCP server 全在这。构建时被 tsdown 内联进 `lib/index.js`(`tsdown.config.ts:66-70` 注释点明「host-neutral studio … is inlined」)。
- **引擎**:`python -m tongflow engine`,来自 PyPI `tongflow`(默认 pin `==0.3.0`,`engine/bootstrap.ts:16`),运行时再 shallow-clone 46 个官方插件仓库(`engine/registry.ts:46-93`)。

所以边界是这样:**去掉主项目,第一层只剩一堆指向不存在命令的 `spawn`;去掉 dsh,第二三层照常工作**——同一批工具同时以 MCP server(`src/mcp/server.ts:1-10`)和独立页面(`src/serve.ts:1-10`)出货。dsh 是三个宿主适配之一,不是这个项目的中心。这决定了「插件太薄」这个判断只对第一层成立:1 039 行是真的,但它调用的 studio 有 9 804 行压在同一张构建产物里(内联),画的每一张图都由包外的 Python 引擎执行。

数据模型(全部可从 `src/shared/types.ts` 与 `src/project/*` 读出):

- **project** —— 一个普通文件夹,磁盘上只有 `project.json`(title / brief / locale)是固定名(`project/manifest.ts:125-145` 创建一个空项目)。布局由 agent 现场设计,用户可以随手改。
- **workflow 文件** —— `*.tongflow.json`,形状 `{ name, description?, flow: { nodes, edges }, executable?, meta }`(`project/workflow-file.ts:1-8`)。`flow` 是画布图,`executable` 是 exporter 从同一张图导出的可执行图。**文件是唯一事实**:工具 hydrate 一个 headless `createFlowStore` → 改 → 再导出 → 写回(`api.ts:240-245`)。
- **run** —— `executeRun` 把 inputs 绑成 `{texts}` / `{fileKeys}`,把 `./x`、`../x`、`bare/key` 解析成绝对路径、把 `{{path}}` 展开成文件内容(`engine/run.ts:211-274`),spawn 引擎(`engine/runner.ts:64-72`),把 NDJSON 翻成 `RunEvent`。
- **输出** —— 落在工作流文件旁边,`<stem>.<no>[.<output>].<ext>`,一次 run 一个号、永不覆盖;文本输出同时写 `.txt`;provenance 追加到 `<stem>.runs.json`(`engine/ingest.ts:1-5`、`shared/types.ts:47-64`)。

**关于「take」**:旧设计里 take 是目录/对象(子包首个提交 `944a393` 的信息里还有 naming / bible / breakdown / takes),现在 **take 就是输出序号**——`mei_ref.01.png`、`mei_ref.02.png`。代码里只剩两处遗迹:`http/util.ts:106` 的路由注释还拿 `/p/:pid/takes/:owner/:pass/:take/circle` 举例,`http/routes.ts:640` 注释写「takes are the library」。落盘层面没有 takes 目录。

一个资产/镜头/角色长什么样(这是 skill 里的方法,不是强制 schema):`characters/mei/{mei.md, mei_ref.tongflow.json, mei_ref.01.png, mei_ref.runs.json}`;镜头 `ep01/sh010/{ref, i2v, lipsync}.tongflow.json` + 每层一个 `<folder>_all.tongflow.json` 组合体(`skills/tongflow-studio.md:54-74`)。「一文件一个可执行节点」写在 skill 里,**工具不校验**——`workflow_new` 只要求路径(`tools/workflow-tools.ts:31-73`)。

**谁生成、谁执行、插件怎么触发**:

1. agent 用 `tongflow_workflow_new` 建文件、`tongflow_workflow_patch` 改图(自称「the ONLY way」,`tools/workflow-tools.ts:76-84`);patch 交给 `tongflow` 包的 `executeGraphTool(..., "apply_graph_patch")`,成功后**立即** `saveWorkflowFile` 写盘,并把渲染后的画布文本回给模型(`api.ts:241-253`)。
2. 人可以在画布上改同一份文件:保存走 `POST /p/:pid/workflow` → `api.saveWorkflowDocument` → 同样 hydrate + 导出 + 写盘(`api.ts:361-377`)。
3. 执行只有一条路:`tongflow_workflow_run` → `RunManager.start` → `executeRun` → 引擎;画布上的「运行单节点」也被包成一份单节点 inline 文档走同一引擎(`engine/single-node.ts:24-40`、`api.ts:516-529`)。没有第二条生成路径。

## 怎么接进 DSH

**分发与清单**

1. 安装:`npx @deepseek-ai/dsh@next plugin --profile web add dsh-tongflow`(`packages/dsh-tongflow/README.md:22`;下文的 `README.md` 均指这个文件)。包已发 npm(`dsh-tongflow@1.0.0`,2026-11-12),不是只能走 git 子目录。
2. `dsh.bundle.patch` → `./cordis.patch.yml`,内容是**一条 insert、一行插件、空配置**(`cordis.patch.yml:4-7`)。dsh 侧校验见本机 `dsh-app-boot/lib/index.js:518-519`。
3. `dsh.client`(`package.json:41-53`):`platform: web` + 8 个 `inject`(session / workspace controller、locale、ui-chat / conversation / renderer / session / workspace)。这不是自定义字段:本机 `dsh-client-modules/lib/index.js:64-69` 逐字段校验 `platform` 与 `inject`(string array),`:92-100` 说明 client 半边按 `<pkg>/client` 子路径装载(对应 `exports["./client"]`,`package.json:30`)。
4. `engines.dsh` 是一串 6 个 range(`package.json:35`);`dsh.compatibility.dshReleases`(`package.json:54-61`)是作者自述——我在本机 dsh 里 grep 不到任何读 `dshReleases` 的代码,真正生效的是 `peerDependencies` 的 13 条 range(`package.json:79-92`)。`README.md:27` 解释了为什么需要这种写法:npm 只有 range 子句带精确 `major.minor.patch` 才匹配预发布。

**注册点**

| 面 | 代码 | 说明 |
|---|---|---|
| tools | `src/index.ts:30`(`inject = ["tools","agents"]`)、`src/tools.ts:194-202` | 19 个 `tongflow_*`,每个包在 `ctx.effect` 里,卸载即摘 |
| system prompt | `src/activation.ts:72-82` | 一段 `tool:tongflow`,order 150 |
| skills | `src/skills/provider.ts:89-108` | `ctx.skills.registerProvider`,`rank: 620`(刻意低于用户/项目 skill,`:16-17`) |
| http | `src/index.ts:60-75` | `webServer.register({kind:"prefix"})`;kind 取值见本机 `dsh-host-webserver/lib/index.js:327` |
| 会话激活 | `src/activation.ts:99-120` | 在 `agent/pre-step` 瀑布里**只判一次** |
| 浏览器视图 | `src/client/index.ts:34-45` | `conversation.view` + id `tongflow-studio` + label `Studio` + order 50 |
| 浏览器 watcher | `src/client/index.ts:46-55` | `conversation.session.header.utilities` + id `tongflow-mode` + order 5 |
| 后台任务 | `src/tools.ts:31-35`、`:70-112` | 扩 `@deepseek-ai/dsh-jobs` 的 `JobKindMap`,把 run 包成 JobSpec(`:76` 用 `"events" in jobs` 判 0.1.5 / 0.1.7+ 两代 API) |
| 附件与模型能力 | `src/tools.ts:115-152`、`:45-61` | `attachments.saveImage` 把图交给 dsh 渲染;`llm.resolveModelInfo` 决定要不要退化成语义描述 |

**激活语义是这张卡最该记住的一段**:`isTriggerText` 只看首条用户消息是否 `^@tongflow`(`activation.ts:16-23`);首条消息先从 durable log 里找,找不到才看本轮(`:37-48`、`:89-96`)。命中则把 tools / prompt / skills 注册进 **agent 自己的 scoped ctx**(`:67-87`),没命中就 `decided.add(agent)` 永久保持普通会话(`:111-117`)。所以普通会话里**没有** `tongflow_*` 工具,不是「有但不建议用」。

**一处自述与实现不符**:`src/index.ts:52-53` 与 `src/client/index.ts:6-8` 的注释都说触发条件还包括「cwd 是 studio 项目」,但 `activation.ts` 和 `StudioModeWatcher` 里都没有 cwd 判断(`grep -rn cwd src/` 只命中 `tools.ts:118` 的会话 cwd 透传与 `StudioView.tsx:97` 的显示)。判断:cwd 触发是计划中的,未实现。

## 关键实现

**dsh 面**(`packages/dsh-tongflow/`)

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `cordis.patch.yml` | 7 | 唯一 patch:1 个 insert | `:4-7` |
| `package.json` | 156 | bundle + client 声明 + 13 peer + `files` 只发 lib/skills/patch/README/LICENSE | `:35`、`:41-53`、`:79-92` |
| `src/index.ts` | 80 | Studio 组装、`inject`、system section 文本、webServer | `:30`、`:35-76`、`:78-80` |
| `src/activation.ts` | 121 | `@tongflow` 触发 → scoped 注册 | `:16-23`、`:99-120` |
| `src/tools.ts` | 202 | ToolSpec → `defineTool`;jobs / attachments / llm 三处适配 | `:45-61`、`:70-112`、`:179-191` |
| `src/config.ts` | 31 | schemastery 校验 10 个配置键(`studioRoot` 默认 `<DSH_HOME>/tongflow`) | `:20-31` |
| `src/skills/provider.ts` | 109 | 打包 skill 的 provider,自带最小 front matter 解析 | `:45-63`、`:89-108` |
| `src/client/index.ts` | 56 | 两个 slot;「打开项目」= `workspaces.create` + `uiWorkspace.startSession` | `:29-33`、`:34-55` |
| `src/client/studio/StudioModeWatcher.tsx` | 117 | **DOM 层**判定与切 tab | `:37-53`、`:64-72`、`:78-109` |
| `src/client/studio/StudioView.tsx` | 127 | 高度/暗色同步 + 内嵌 `StudioShell` | `:34-75`、`:116-124` |
| `src/client/studio/ChatPane.tsx` | 196 | 会话记录的紧凑聊天列(与 dsh 共用 store) | `:67-96` |
| `skills/` | 594 | 方法:1 个 skill(134)+ 5 个 reference(460);方法改编自 MIT 的 Hell Grind AIGC Skill,有 `SOURCES.md` | `tongflow-studio.md:54-96` |
| `test/` | 200 | 2 个测试文件(见下) | `tools-adapter.test.ts:39-101` |

**宿主无关 studio**(`packages/tongflow-studio/src`,构建时内联)

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `studio.ts` | 136 | 配置 / 路径 / venv / registry / run 的唯一组合根 | `:31-58`、`:76-89`、`:108-121` |
| `api.ts` | 858 | projects / tree / workflows / runs / plugins 的 API 面 | `:225-256`、`:389-416`、`:423-505` |
| `engine/run.ts` | 293 | inputs 绑定、引用解析、引擎调用、ingest | `:75-90`、`:127-153` |
| `engine/runner.ts` | 177 | spawn + NDJSON 翻译 + abort(SIGTERM → 5s SIGKILL) | `:61-147` |
| `engine/ingest.ts` | 198 | 编号落盘 + `<stem>.runs.json` | `:1-5` |
| `engine/registry.ts` | 326 | 46 个官方插件、`tongflow scan`、git clone/pull | `:46-93`、`:192-229`、`:251-284` |
| `engine/bootstrap.ts` | 177 | python 探测(≥3.10)+ venv + pip | `:16`、`:56-87`、`:105-139` |
| `project/workflow-file.ts` | 377 | `.tongflow.json` 读写 / 导出 / `canvasView` 引用重写 | `:74-96`、`:252-285`、`:343-363` |
| `http/routes.ts` | 766 | `/tongflow/*` 一个 handler(JSON + SSE + Range) | `:60-93`、`:76-77` |
| `tools/run-tools.ts` | 680 | run / run_status / look / perceive / plugins_* | `:190-278`、`:308-541` |
| `client/CanvasPane.tsx` | 169 | 画布 ↔ 文件同步 | `:32`、`:85`、`:107-149` |
| `mcp/server.ts` | 228 | 同一批工具的另一宿主(stdio JSON-RPC) | `:23-27` |

**数据流(四条,别混)**

```
① 激活
   user "@tongflow …" → agent/pre-step → isStudioSession(首条文本)
   → agent.ctx: 19 tools + system section(order 150) + skill provider(rank 620)

② 写文件
   model → tongflow_workflow_patch → apply_graph_patch(tongflow 包)
   → fillDefaultPlugins + mirrorUpstreamPayloads → exportWorkflow → 写 JSON(原子写)

③ 跑
   tongflow_workflow_run → 付费闸(paidPlugins)→ RunManager 队列(maxConcurrentRuns=2)
   → executeRun:inputs 绑定 / {{file}} 展开 → spawn `python -m tongflow engine`
   → NDJSON → RunEvent → ingest → <stem>.NN.ext + <stem>.runs.json

④ 看 / 改
   StudioShell → CanvasPane:GET /p/:pid/workflow(拿到的是 `./x` 已重写为项目 key 的副本)
   → 画布编辑 → 1s debounce → POST /p/:pid/workflow → 同一个 saveWorkflowFile
```

**Studio 是哪一种 UI 扩展**——这是本插件最值得单独说清的一点:

- 它**不是 webview、也不是独立页面**,而是 dsh `conversation.view` 槽里的一个视图:`StudioView` 直接渲染 `StudioShell`,并把 dsh 的会话数据接进去——`useSessions` 取 cwd、`ChatPane` 用 dsh 的 `useChat` 渲染同一个会话(`StudioView.tsx:95-127`、`ChatPane.tsx:67-96`)。它和 dsh 的聊天共用一份 store 与一个 composer,没有第二套会话。(同一个 studio 确实也能当独立页面跑,但那是 `serve.ts` 给没有宿主的环境准备的,不是 dsh 里这条路径。)
- **进入方式靠 DOM**:`StudioModeWatcher` 在 `document` 里找 `[role="tablist"]`,再找文本等于 `Studio` 的 `[role="tab"]`,命中就 `.click()` 并把整个 tab ring `display:none`(`StudioModeWatcher.tsx:37-53`、`:78-109`),并用 `MutationObserver` 盯 `aria-selected`。判据是三条或:localStorage 备忘、首条用户文本、会话标题(`:64-72`)——第三条是为了「历史窗口加载不到首条消息」的长会话(`:62-63`)。
- dsh 侧这套 DOM 是真的:`conversation.view` 的每个 slot entry 变成 tab(本机 `dsh-client-ui-conversation/lib/client.js:19753-19765` 的 `viewTabs()`),渲染成 `role="tablist"` / `role="tab"` / `aria-selected`(`:18228-18242`)。**路能走,但它依赖 dsh 的 DOM 结构与 label 文本**;`label: "Studio"` 一改,studio 模式就静默失效(不报错,只是不切视图)。
- **文件 ↔ 画布同步是一秒**:画布改动 debounce 1000 ms 后 `saveWorkflow`(`CanvasPane.tsx:32`、`:107-149`),卸载时再 flush 一次;外部改动(agent patch、跑完)靠父组件传来的 `reloadToken` 触发重新加载(`:85`、`PreviewPane.tsx:294`)。**没有版本号、没有锁**:两侧都写同一个文件,谁后写谁赢。`workflowHash` 存在(`workflow-file.ts:304-309`、`run.ts:166`),但只进 provenance,不参与冲突检测。

**测试证明了什么、没证明什么**:

- dsh 面 2 个测试:`tools-adapter.test.ts:39-46` 断言 **19 个**工具都能编译成 dsh tool、并钉住两个 output schema(`node_catalog` 是 string、`workflow_run` 是空);`:65-101` 断言装了 jobs 时 `run_in_background` 真的走 `jobs.start` 并回 jobId,没装 jobs 时退化成 `tongflow_run_status` 轮询。`model-modality.test.ts` 用 7 个用例钉住「只有模型明确声明不支持图片时才退化」——未知一律当作能看图(`tools.ts:45-61` 的注释解释了理由:猜错方向会让每次 look 都白花一次插件运行)。
- studio 侧 1 722 行测试,和工作流 / 文件同步直接相关的是:`engine.test.ts:144-211` 用假 python 跑完整链路(引用解析 → 编号落盘 → `.runs.json` → 第二次 run 拿 `.02`);`project-model.test.ts:241-289` 钉住「文件里保留 `../` 相对引用,给画布的副本重写成项目 key」;`:292-337` 钉住 tree 把输出挂在 workflow 行下;`serve.test.ts:55-116` 钉住独立页的 token / 同源 / cookie 名。
- **没测**:浏览器半一整块(`StudioModeWatcher` 的 DOM 操作、`StudioView` 的高度与暗色同步、`ChatPane`)没有任何测试;`@tongflow` 激活判定(`activation.ts`)也没有——`test/` 里只有两个 `.ts`,没有 `.tsx`,vitest 环境是 node(`vitest.config.ts:5-10`)。所以「怎么接进 DSH」里那条 DOM 路径完全靠手测。

## 为什么它突出

**先拆星标归属,这是本卡的核心。** GitHub 星标是仓库级的,registry 却把 `tong-io/tongflow` 的 860 记在一个**子目录条目**头上,这本身就是口径错配。时间线是决定性的:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-04-08 | 仓库创建 | GitHub API `created_at` |
| 2026-06-16 | 首个提交 `feat: TongFlow initial open-source release (v0.1.0)` | `git log --reverse` |
| 2026-08-18 11:44 +0900 | 子包首个提交 `944a393` | `git log --follow --reverse` |
| 2026-08-19 | 子包删掉模板 `6ba7fbc`;**860 星采样点** | registry ⚠ |
| 2026-11-11 | 子包 `780f0a1 chore(release): prepare 1.0.0` | `git log -1 -- packages/dsh-tongflow` |
| 2026-11-12 | npm `dsh-tongflow@1.0.0`、PyPI `tongflow 1.0.0` | 两个 registry |
| 2026-11-13 | 整仓 HEAD `f7aae77` | `git log -1` |
| 2026-11-18 | **1047** 星、136 fork | GitHub API |

采样点(08-19)距子包首个提交 **≤1 天**,当日该子目录已有 ≤33 个提交。也就是说:**当前 1047 星里的 82%(860)是在 DSH 适配层几乎还不存在时挣到的**;之后 91 天涨 187 星(+21.7%),而同一窗口主项目还发了 0.3.5 / 0.3.6 / 1.0.0、46 个插件和桌面端。**能归给 DSH 适配层的,最多是这 187 里无法归因的一小部分**;把它算成这层接线的声量是错的。

**再解释「高星零扩散」。** 扩散是 0(`grep -ril 'tongflow' data/plugins/` → 1,即自身)。四个理由,按解释力排:

1. **可抄的部分抄了没用。** dsh 面 1 039 行的全部内容是「把一批已有的 ToolSpec 塞进 dsh 的注册点」:19 个工具的名字、参数、执行体都在 `tongflow-studio` 里,适配层只是 `defineTool` 循环 + 两个 slot + 一行 patch。照抄它等于照抄一次注册动作。
2. **有用的部分抄不动。** 要复现能力,得有 Python 引擎(8 302 行 SDK)+ 46 个插件仓库(34 modal / 6 router / 6 api)+ 49 285 行 TS 画布/ABI 核心。**适配层薄 → 抄了没用;引擎厚 → 抄不动。** 它比更薄的形态多出来的那层是画布与项目模型,但那一层仍然只服务同一个引擎的 HTTP 契约,不是可移植的机制。
3. **它由 vendor 自己发布。** 作者就是 TongFlow 官方(`tong-io`)。vendor 接入只会引来「使用」,不会引来「衍生」;第三方要写第二个 DSH 适配,唯一动机是 fork 这个 monorepo。
4. **它不是协议创新。** 19 个工具里没有新协议,工作流文件格式是 TongFlow 自己 ABI 的投影。第三方要讨论它,得先讨论「影视流水线怎么做」——那是产品话题,不是插件生态话题。

**判断:明星,不是锚**(声量高、扩散零)。形态归 `external-engine` 没错,但影响力应记在 TongFlow 主项目名下。它在本领域的真实位置是**一个外部产品的官方接入点**,而不是被同行引用或仿制的机制。

## 代价与边界

- **外部依赖是硬的**:Python ≥3.10 + `venv` + `pip`(`bootstrap.ts:56-87`,找不到时抛一条带安装建议的错)、`git`(clone 插件)、`ffmpeg`(视频接触表,`run-tools.ts:651-678`)。首次使用要建 venv、`pip install tongflow==0.3.0`、再 shallow-clone 最多 46 个插件(`registry.ts:192-229`,并发 4,失败只记日志)。
- **默认 SDK pin 与 npm 核心不同步**:`DEFAULT_TONGFLOW_SDK_VERSION = "0.3.0"`(`bootstrap.ts:16`),而 npm `tongflow` 与 PyPI `tongflow` 都已到 1.0.0(2026-11-12)。默认安装因此是「0.3.0 的 Python 引擎 + 1.0.0 的 JS ABI」——ABI 路径从 npm 包解析(`studio.ts:128-136`),再作为 `--abi` / `abi_path` 传给 `scan` 与 engine(`registry.ts:139`、`run.ts:137`)。跨三个 minor 是否兼容**未验证**(见待验证)。
- **46 个插件是 46 条供应链**:每次启动在后台 clone;每个插件在自己的共享 venv 里装 requirements;插件代码在本机跑,并继承 `env.json` 里的全部 key。
- **API key 是明文**:`studioRoot/env.json`,写后 chmod 0600(`studio.ts:108-121`);键名必须是 `^[A-Z][A-Z0-9_]*$`。
- **失败模式,按发生顺序**:
  1. **没有 Python** → `studio.init()` 压根不碰 python(`studio.ts:60-73` 只 mkdir + 后台装插件),所以插件「装上了、看着正常」;**第一次需要 registry / run 的调用才抛** `no Python >= 3.10 found`。最阴的一档:初始化阶段完全静默。
  2. **首条消息不是 `@tongflow`** → 工具集里没有 `tongflow_*`;注释承诺的 cwd 触发未实现,所以「在项目目录里开会话」不够。
  3. **工作流文件坏或手写** → `parseWorkflowImportJson` 抛错,或导出的 `executable` 缺失;`run` 直接报 `has no executable graph: … — save it once it validates`(`run.ts:75-79`)。注意 `tongflow_workflow_list` 会**静默跳过**不可读文件(`workflow-file.ts:365-377`),「列表里没有」不等于「文件不存在」。
  4. **缺插件** → run 的前置检查报 `no plugin selected for: … — install one with tongflow_plugins_install`(`run.ts:83-90`)。
  5. **画布与文件互相覆盖** → 无锁、无版本号、1 秒 debounce;用户在画布上改的同时 agent patch 同一文件,后写者赢,先写者的编辑丢失(`CanvasPane.tsx:107-149`)。
  6. **长任务** → 插件**没有**给工具设 `timeoutMs`(`tools.ts:179-191`;dsh 的注册器支持该字段,本机 `dsh-tools/lib/index.js:2979-2980`),`runEngine` 也不设超时(`runner.ts:61-147`),只靠 AbortSignal;取消时 SIGTERM 再 5 秒 SIGKILL(`:78-83`)。前台跑视频节点会一直占着这一轮,直到用户中止——README 的指引是 `run_in_background`(任务转 dsh jobs,`tools.ts:70-112`)。
  7. **付费确认只在工具面**:画布的单节点运行不设闸(`docs/design.md:39` 明说),两条路径的「要不要问用户」不一致。
- **UI 维护成本**:studio 模式靠 DOM 选择器 + `label === "Studio"`;dsh 改 tab 结构就静默退化。这是全插件最脆、也最难测的一处。
- **前端体积**:客户端是单文件 CJS bundle,`@xyflow/react`、`zustand`、`use-intl`、`tongflow/canvas` 全部内联,只有 dsh 平台模块 external(`tsdown.config.ts:9-22`、`:32-44`);整包 unpacked 14.6 MB。

## 可信度与复现

- **★★★ 范围**:dsh 面 9 个源文件 + 2 个测试 + patch/manifest + skills 全文;studio 侧读了 `run` / `runner` / `runs` / `ingest` / `bootstrap` / `registry` / `workflow-file` / `api` / `routes` / `studio` / `config` / `single-node` / `session-projects` / `instructions` + 3 个 client 文件;测试读了 dsh 两个文件全文与 `engine` / `project-model` / `serve` 的关键用例;并用本机 dsh **0.2.1-rc.5** 核对了 6 个契约(`bundle.patch`、`dsh.client` 校验、`agents` 服务名、`conversation.view` 的 `role=tablist`/`aria-selected`、`webServer` 的 `kind`、tool `timeoutMs`)。
- **未读**:46 个插件仓库(全部外部)、`packages/tongflow` 49 285 行的 ABI/画布核心(只按调用面理解)、Python `sdk/` 8 302 行的引擎实现(只读 `__main__.py` 的子命令表)、`project/compose.ts` 435 行(只读 `docs/design.md:40` 与测试断言)、根 Next.js 应用 16 584 行。
- **没跑过**:任何 `pip install`、引擎进程、画布、`dsh plugin add`。

```sh
# 1) 克隆与提交(仓库 ~11 MB;blobless 全历史 448 个提交)
git clone --filter=blob:none https://github.com/tong-io/tongflow.git /tmp/an-tongflow
git -C /tmp/an-tongflow log -1 --format='%H %ad %s' --date=short
# → f7aae7743b3046ebd783f4e704d454ebe3566f2d 2026-11-13 Merge pull request #237 …
git -C /tmp/an-tongflow log -1 --format='%H %ad %s' --date=short -- packages/dsh-tongflow
# → 780f0a1888a788eb3505f8c620373ae71bdaf139 2026-11-11 chore(release): prepare 1.0.0
git -C /tmp/an-tongflow log --follow --reverse --format='%h %ad %s' --date=iso -- packages/dsh-tongflow | head -1
# → 944a393 2026-08-18 11:44:49 +0900 feat(dsh-tongflow): scaffold dsh plugin package …

# 2) 规模(口径:ts/tsx 与 py 的物理行数)
cd /tmp/an-tongflow
find packages/dsh-tongflow/src -name '*.ts*' | xargs wc -l | tail -1        # → 1039
find packages/tongflow-studio/src -name '*.ts*' | xargs wc -l | tail -1     # → 9804
git ls-files '*.ts' '*.tsx' | xargs wc -l | tail -1                        # → 69996
find sdk -name '*.py' | xargs wc -l | tail -1                              # → 8302
git ls-files | wc -l                                                       # → 747
grep -c '"tongflow-' packages/tongflow-studio/src/engine/registry.ts       # → 46
grep -n 'DEFAULT_TONGFLOW_SDK_VERSION =' packages/tongflow-studio/src/engine/bootstrap.ts

# 3) 零扩散(11 744 个 yml,直接展开会 Argument list too long,必须用目录形式)
cd <awesome-dsh-plugin>
grep -ril 'tongflow' data/plugins/ | wc -l      # → 1
grep -ril 'tongflow' data/plugins/              # → data/plugins/tong-io__tongflow--packages-dsh-tongflow.yml
grep -ril 'dsh-tongflow' data/plugins/ | wc -l  # → 1(同上)
grep -ril '@tongflow' data/plugins/ | wc -l     # → 1(同上)

# 4) 星标归属(2026-11-18 实时)
curl -s https://api.github.com/repos/tong-io/tongflow \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["created_at"], d["stargazers_count"], d["forks_count"], d["size"])'
# → 2026-04-08T00:21:23Z 1047 136 6959

# 5) 模板被删的那一提交
git -C /tmp/an-tongflow log --diff-filter=D --name-status --format='%h %ad %s' --date=short -- 'packages/dsh-tongflow/skills'
# → 6ba7fbc 2026-08-19 … / D packages/dsh-tongflow/skills/tongflow-manga-drama.md

# 6) dsh 侧契约核实(本机 0.2.1-rc.5)
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh
grep -n 'bundle.patch must be a file path' $DSH/node_modules/@deepseek-ai/dsh-app-boot/lib/index.js
grep -n 'dsh.client.platform must be a string' $DSH/node_modules/@deepseek-ai/dsh-client-modules/lib/index.js
grep -n 'super(ctx, "agents")' $DSH/node_modules/@deepseek-ai/dsh-agent/lib/index.js
grep -n 'role: "tablist"' $DSH/node_modules/@deepseek-ai/dsh-client-ui-conversation/lib/client.js
grep -n 'route.kind === "exact"' $DSH/node_modules/@deepseek-ai/dsh-host-webserver/lib/index.js
```

## 待验证

1. **默认 SDK pin 是否真能跑**:装一次、跑一个节点,看 `tongflow==0.3.0` 引擎是否接受 npm `tongflow@1.0.0` 给的 ABI(`--abi` / `abi_path`)。这是全新安装的**第一条**路径,失败会以引擎报错的形式出现。
2. **studio 模式在选择器上是否真命中**:在 `dsh web` 里开一个 `@tongflow` 会话,看 tab ring 是否隐藏、Studio 是否被选中。我核对了 dsh 侧 DOM 与 label 机制,但没跑。
3. **从 Studio 的「打开项目」新建的会话是不是 studio 会话**:它走 `workspaces.create` + `uiWorkspace.startSession`(`client/index.ts:29-33`),首条消息通常不是 `@tongflow`,而 cwd 触发未实现。判断:不会进 studio 模式,需实测。
4. **画布与 agent 的并发覆盖窗口**:两个客户端同时写同一文件时的实际表现(我判断后写者赢)。
5. **`ffmpeg` 缺失时的降级链**:`run-tools.ts:406-427` 有 catch 并提示改用 `tongflow_perceive`,但 `perceive` 自身还要装 describe 插件——两级降级都没实测。
6. **46 个插件的首次安装真实体积与耗时**(`registry.ts:186-190` 的注释说「a few hundred KB each」,未核实;`:192-229` 的安装循环也不设超时)。
7. **sidecar 的下载 0 是覆盖缺口还是真接近 0**:`data/npm-map.json` 不在本工作区,无法判定;npm 上 `dsh-tongflow` 确实发布过(0.1.x → 1.0.0),这一点可确证。
