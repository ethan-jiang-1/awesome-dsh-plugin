# plugin-session-export — 458 行单文件,把 live session 日志投影成一份人读文档

> 证据等级:★★★(源码级;`whyihaveyou/dsh-suite@10152cc3076a199762f7eb5b4b8bd14571a89e4c`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 42 为 2026-08-19 历史采样,**且是仓库级**(同仓库四条子目录条目同值);2026-11-18 实时 69。下载:⚠ 边车无记录(2026-08-19 采样缺口);2026-11-18 实时 npm 近 30 天 188。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `whyihaveyou/dsh-suite#plugin-session-export`([registry](../../../data/plugins/whyihaveyou__dsh-suite--packages-plugins-plugin-session-export.yml)) |
| 类目 | session(914 条,[census](../../ecosystem/census.py)) |
| 子分类 | `import-export`(数据跨越 DSH 边界:日志 → 磁盘文件) |
| 自述 | 「把 append-only 会话日志导出为按轨迹来源分组的可读 Markdown 或 HTML」——**"按轨迹来源分组"这个说法在源码里没有对应的字段**,见下节 |
| 星标 ⚠ | 42(2026-08-19 采样,**仓库级**;2026-11-18 实时 **69**,+27/91 天) |
| 下载 ⚠ | 边车无记录;实时 npm `@dsh-suite/plugin-session-export` 近 30 天 **188**(2026-10-18~11-16,2026-11-18 查询) |
| 扩散 | **0**(口径:`grep -ril 'whyihaveyou' data/plugins/` = 4,全是本仓库四条子目录条目;`export_session` = 0;`session-export` = 6,其中 5 条是别人的同名实现,逐条人工排除,见「为什么它突出」) |
| 仓库 commit | `10152cc3076a199762f7eb5b4b8bd14571a89e4c`(2026-11-18,`data: hourly refresh [skip ci]`);子目录最后提交 `4312f59b4044eb92ac258c6ef69aeed89eb077a7`(2026-08-30,仅改 README 的皮肤契约声明) |
| 包形态 | npm `@dsh-suite/plugin-session-export@0.2.0`;`dsh.bundle.patch` → `cordis.patch.yml` 一行 `insert`;tarball 4 个文件 / 24 846 B;无 client 面、无 HTTP 路由 |
| 代码规模 | `src/index.ts` **458 行**(全部逻辑,单文件)+ `cordis.patch.yml` 10 + `package.json` 36 + `tsconfig.json` 20 + `scripts/render-smoke.mjs` 55 + `README.md` 137 = 716 行;命令:`find . -type f -not -path './.git/*' \| xargs wc -l` |
| 主项目体量 | 743 个 git 文件(其中 `site/` 369、`data/` 212、`packages/` 95),GitHub API `size` 520 468 KB(≈508 MiB);`README.md` 2 468 行 / 387 908 B。**星标来自这个"插件目录"项目,不是这个插件** |

## 它到底是什么

**一个宿主侧工具插件,不是格式、不是服务、也没有第二个入口。** 它注册一个名为 `export_session` 的模型工具(`src/index.ts:13-89`),被调用时把**当前 DSH 进程内存里**的某个 live session 的 `events` 数组投影成一份 Markdown 或 HTML 文本,写到宿主路径。

数据模型只有两层,都在同一个文件里:

- **`Section[]`** —— 一次遍历日志得到的中间表示(`src/index.ts:102-107`),五种:turn / user / assistant(+reasoning) / tool(+isSubagent) / todo;
- **`Meta`** —— 从 `session.header` 与两条日志事件里抽出的头部信息(`src/index.ts:109-121`、`135-161`):标题、sessionId、createdAt、cwd、origin、委托深度、父会话、preset、model、systemPrompt、usage 汇总。

两种输出共用同一份 `Section[]`(`src/index.ts:128-133`),这正是它结构上最干净的一处:Markdown 与 HTML 不是两条渲染路径,而是同一投影的两个 emitter,不会出现"md 有、html 没有"的漂移。

**关键:所谓"按轨迹来源分组"不是按某个 `source`/`trajectory` 字段,而是按事件类型 switch**(`src/index.ts:180-220`)。只有 8 种事件进入渲染:

| 事件类型 | 落成 | 位置 |
|---|---|---|
| `request/header` | 系统提示(`header.system`) | `src/index.ts:140-142` |
| `request/context` | `provider/model` 一行 | `src/index.ts:143-145` |
| `turn/start` | `### Turn N` | `src/index.ts:182-184` |
| `user/message` | 👤 用户 | `src/index.ts:185-189` |
| `assistant/message` | 🤖 助手 + 折叠思维链 | `src/index.ts:190-197` |
| `tool/call` | 🔧 工具调用 / 🤝 子agent 委派 | `src/index.ts:198-209` |
| `tool/result` | 先建 callId → 结果 的 Map | `src/index.ts:229-239` |
| `todo/write` | 📋 任务列表 | `src/index.ts:210-214` |

而本机 DSH 0.2.1-rc.5 的事件词表有 **63 种**(`dsh-session/lib/types/known-event-types.js:21-84`)。被丢弃的不是边角:`system/message`、`developer/message`、`compaction/summary`、`approval/*`、`plan/mode`、`subagent/descriptor`、`tool-workflow/*`、`team/*`、`feedback/*`、`command/*` 全部走 default 分支(`src/index.ts:215-219`,注释自承"reconstructed from the durable log but not surface prose")。

其中三处丢弃会产生读者会察觉的错:

1. **`source` 被无视。** `user/message` 的文档明说三种来源——真人输入、`agent.inject()` 注入的上下文(文件变更通知、AGENTS.md、skill 内容、cron)、goal 续轮——"`source` tells them apart"(`dsh-session/lib/types/types.d.ts:288-295`;`source` 字段定义见 `dsh-llm/lib/types/message.d.ts:95-107`)。本插件把所有 `user/message` 一律渲染成 **"👤 用户"**(`src/index.ts:261`、`313`),注入上下文读起来与用户原话一模一样。我实测:构造一条 `source.kind='plugin'` 的 user 事件,导出结果与真人消息同标签、无任何区分。
2. **`surfaceOp` 被无视。** 每条 surface 事件都带 `surfaceOp: 'append' | {op:'replace',…}`(`dsh-session/lib/types/types.d.ts:443-465`),DSH 明确说替换副本"stay model-only",而 append 事件才是人读转录的素材(`dsh-session/lib/types/surface.d.ts:50-57`)。插件遍历 `session.events` 时不过滤,compaction 之类的替换副本会被当成普通消息再渲染一遍。
3. **`tool/result` 只取消息里第一个 block。** `collectToolResults` 读 `event.data.message.content[0]`(`src/index.ts:233`),同一消息里的第二个 tool-result block 直接消失;`error.reason`(用户可读的失败原因,`types.d.ts:375-392`)也从未读取,只保留一个 `（失败）` 字样。

**保留了什么**:思维链保留并折叠(`src/index.ts:190-197`、`265-275`),工具参数与结果默认保留并折叠(`276-289`),`includeToolDetails: false` 时只留工具名(`278-281`),用量按 token 三类汇总(`163-175`)。
**没保留什么**:每条消息的时间戳(`event.time` 在整个文件里从未被读)、turn 结束原因、附件与图片(只取 `type === 'text'` 的 block,`src/index.ts:383-392`,图片块连占位符都没有)、失败原因文本。所谓"人读文档"里只有一个会话级 `创建时间`(`src/index.ts:367`)。

## 怎么接进 DSH

三件东西,全在 `package.json` 与 10 行 patch 里:

1. **manifest 就是 bundle patch。** `package.json:15-19` 只有 `"dsh": { "bundle": { "patch": "./cordis.patch.yml" } }`;`exports` 只有 `"." → ./dist/index.js`(`package.json:8-10`)——**没有任何浏览器入口**,所以它天生没有 UI。
2. **patch 只有一行 insert。** `cordis.patch.yml:8-10`:`id: plugin-session-export`、`name: '@dsh-suite/plugin-session-export'`,与包名一致,因此 `dsh plugin --profile <p> add @dsh-suite/plugin-session-export` 能自动注册(`README.md:45-47`)。
3. **服务注入两条。** `inject = ['tools', 'sessions']`(`src/index.ts:10`);`ctx.tools.register(defineTool({...}))`(`src/index.ts:13`)。注册是 Cordis effect(`dsh-tools/lib/index.js:2974-2982` 的 `register` 返回 `this.layers.effect(...)`),插件卸载时工具会随之撤下——README 说的"注册即 effect"成立。

依赖只有三个 peer(`package.json:24-28`):`@deepseek-ai/cordis ^4.0.1`、`@deepseek-ai/dsh-session ^0.1.0-rc.6`、`@deepseek-ai/dsh-tools ^0.1.0-rc.6`。**没有相对导入,没有 workspace 依赖,没有从同套件其他插件借代码**(`src/index.ts:1-5` 只 import `node:fs/promises`、`node:path` 与三个 DSH 包)。monorepo 根 `pnpm-workspace.yaml` 声明 `packages/*` 与 `packages/plugins/*`,但这个插件的 458 行是自足的。

**版本漂移是本卡最该被读者看到的一条。** peer 范围钉在 `dsh-session ^0.1.0-rc.6`,而本机装的是 **0.2.1-rc.5**。在那个版本里 `EpochHeader.system` 已经是 `system?: never`,注释写着"Retired request text; system prompts belong to `system/message` events"(`dsh-session/lib/types/types.d.ts:225-228`)。插件仍从 `event.data.header.system` 取系统提示(`src/index.ts:140-142`),同时又不处理 `system/message`(`215-219`)。**结论:在 0.2.x 上,"## 系统提示"这一节只可能为空**。运行时倒不会炸:`SessionId` 在 0.2.1-rc.5 里仍作为函数导出(实测 `typeof m.SessionId === 'function'`),所以是静默丢内容,不是加载失败。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `src/index.ts` | 458 | 全部逻辑:工具定义 + 投影 + 两个 emitter + 路径解析 | `13-89` 工具;`102-107` Section;`177-222` 投影;`249-295` md;`297-346` html;`348-364` CSS;`431-437` 转义;`447-458` 路径 |
| `cordis.patch.yml` | 10 | 唯一被 DSH 读的装载声明 | `8-10` |
| `package.json` | 36 | bundle 标记、peer 范围、`files: [dist, cordis.patch.yml]` | `11-19`、`24-28` |
| `tsconfig.json` | 20 | `target es2022`、`module esnext`、`strict`、`noEmitOnError` | `2-19` |
| `scripts/render-smoke.mjs` | 55 | **唯一的测试**:手搓 12 条事件 → 4 份输出 → 14 条断言 | `22-42` |
| `README.md` | 137 | 特性、示例输出、验证清单、皮肤契约 | `110-116` 自述验证状态 |

**数据流(一次调用)**:

```
模型/CLI 调 export_session(args)
  └─ 选 session(src/index.ts:62-74)
        all      → ctx.sessions.list()          ← live 会话,创建序
        sessionId→ ctx.sessions.get(SessionId)  ← 只查 live
        默认     → exec.agent?.session,否则 list() 最后一个
  └─ renderSession(session, format, {includeToolDetails})   (128-133)
        buildMeta   : 扫一遍 events,取 header.system / provider+model / usage  (135-161)
        buildSections: 再扫一遍,先建 tool/result Map,再 switch 出 Section[] (177-222)
        emitter     : md 或 html,同一份 Section[]                (249-346)
  └─ outputPath(...) → mkdir -p → writeFile(utf8)              (82-85, 447-458)
```

**五次全量遍历**:`buildMeta`(`139`)、`sumUsage`(`167`)、`buildSections`(`180`)、`sessionTitle`(`407`),外加 `outputPath` 里再算一次标题(`449`);然后一次整串拼接、一次 `writeFile`。没有分页、没有流式、没有分块、没有大小上限,也**从不检查 `exec.signal`**(`ToolExecutionInput.signal` 是必填的取消信号,`dsh-tools/lib/types/index.d.ts:241`)。大 session 的代价是整份文档驻留内存 2–3 倍:一遍 Section 数组 + 一遍拼接字符串。

**读取面是"服务",不是文件。** 全程只碰 `ctx.sessions`(`src/index.ts:60-74`),不打开任何 session 文件、不 import 持久化包;写文件是单向的(`84`)。**日志不会被改**:没有 `session.append`、没有 flush、没有任何写回。副作用只有 `mkdir` 与 `writeFile`,且 `writeFile` **静默覆盖**同名文件。

代价是它只能看见这个进程里的 live session:`get` 的契约是"Look up a live session …undefined when no live session has that id"(`dsh-session/lib/types/index.d.ts:487-491`),`list` 是"All live sessions, in creation order"(`493-496`)。源码注释把 `sessions` 写成"durable session store"(`src/index.ts:9`),与 API 文档相反:**进程重启后,`all: true` 导不出任何历史会话**,指定历史 `sessionId` 会走进 `sessions.length === 0` 抛错(`75-77`)。官方导出的对照实现走的是 `sessionPersistence` 读句柄 + `sessionQuery.traceSession`(`dsh-session-log-export/lib/index.js:53-59`、`287-300`),冷会话与 subagent 树都能导——本插件没有注入这两个服务。

**自指细节**:`tool/call` 事件先落日志、再执行工具(`dsh-agent-loop/lib/index.js:680-688` 的 `appendToolCall`),所以导出文件里**一定会包含触发它的那次 `export_session` 调用**:参数可见、结果为空(该 callId 在 `collectToolResults` 里查不到,`src/index.ts:199-207`)。

**HTML 的自包含与安全**:`<style>` 内联(`src/index.ts:345`、`348-364`),无 `<script>`、无 `<link>`、无 CDN、无外链字体(字体栈是系统字体);`<!DOCTYPE html>`、`charset=utf-8`、`viewport` 齐全,并有 `@media print` 规则(`363`)。离线可开,实测 2 768 字符的单文件不含任何外链。**转义是完整的**:`escapeHtml`(`431-437`)覆盖 `& < > "`,且每一处插入用户内容的地方都过了它(`299`、`302`、`306`、`313`、`316`、`321`、`329`、`334`、`336`、`338`、`342`、`345`);不转义单引号但没有任何属性位拼接,不构成问题。我用含 `<script>alert(1)</script>` 与 `<img onerror>` 的用户消息实测:HTML 里是 `&lt;script&gt;…`,标签数为 1 个 `<details>`(工具),无注入。

**但 Markdown 侧完全没有转义**(`src/index.ts:251`、`261`、`264`):用户/助手正文原样拼进去,工具参数与结果却用了自适应反引号围栏(`fence()`,`424-429`,按内容里最长反引号串加一)。实测同一条含 `</details><script>alert(1)</script>` 的用户消息:Markdown 里是裸 `<script>`,而且 `</details>` 的闭合标签总数变成 4——插件自己写 1 个,标题、正文、工具结果各注入 1 个,折叠块被提前闭合。所以它的 `.md` 是"能看",不是"能安全渲染成 HTML";而输出结构本身依赖 Markdown 里的原始 `<details>` 标签(`282-289`),这意味着非 GFM 渲染器(飞书文档、部分周报系统)只会看到一堆标签。

## 为什么它突出

**先把星标拆干净。** GitHub 只有仓库级星标,而这个条目是 monorepo 子目录:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-13 13:32:50Z | 仓库创建 | GitHub API `created_at` |
| 2026-08-13 14:50:35Z | 启动提交 `a68e96ae9` 已包含 `packages/plugins/plugin-session-export` | `commits?path=…` |
| 2026-08-13 15:16:39Z | npm `0.1.0` 首发 | npm registry `time` |
| 2026-08-16 09:54:35Z | `v0.2.0`(HTML 自包含 + `includeToolDetails`),此后**功能零提交** | 子目录历史 7 条 |
| **2026-08-19** | **42 星采样点** | ⚠ 边车 |
| 2026-08-30 | 子目录最后一条提交(只改 README 皮肤声明) | `4312f59b4` |
| 2026-11-18 | 69 星、14 fork、30 open issues | GitHub API |

与"仓库跑了很久、插件后加"的形态不同,**这个插件在仓库创建 78 分钟后就在里面了**,所以时间线不能用来切分归属。真正的证据是另外两条:

1. **边车把同一个 42 复制给了同仓库四条子目录条目**(plugin-manager / plugin-notify / plugin-session-export / plugin-team-board,`data/stars.json` 逐条同值),下载字段也只有 manager 1584 与 team-board 423 两条。这是采样器按 URL 抓仓库级数字的直接痕迹,**不是四次独立测量**。
2. **这个仓库的自我介绍是目录,不是插件集**:`package.json:5` 写 "Bilingual curated DeepSeek Harness plugin directory — daily compat CI, create-dsh-plugin scaffold, own plugins";743 个文件里 `site/` 369、`data/` 212,`packages/`(四个插件 + `create-dsh-plugin`)只有 95;README 是 2 468 行的大表。判断:42 与 69 都属于这个"活目录"项目,无法拆到这个插件头上,**不应记作插件热度**。

**扩散为 0,而且 0 得很有信息量。** 名字落在 `session-export` 这一簇的,本 registry 里有 **6 个互不相干的实现**(见复现命令的人工排除清单),彼此零引用,也没有任何第三方条目引用它们中的任何一个。这只能说明"没有引用边":除本插件外我未读那 5 个的源码,它们各自的文档形状是否兼容,不能从 registry 描述推断(判断)。

机制层面能解释这个现象,而且只靠本插件自身的证据:**它的输出不是格式,是一份散文**。Markdown/HTML 里没有 schema、没有版本号、没有机器可读字段(头部信息是给人看的中文行,`src/index.ts:366-376`);对外没有一个 service key、没有 `plugin:` 事件、没有 HTTP 路由;入口只有一个模型工具,输出只落到一个路径。**没有任何可供第三方引用或依赖的接口面**——所以"零扩散"不是"没人用"(npm 近 30 天 188 次下载是反证),而是"用了也没法引用"。

同一个结构也解释了它为什么存在:官方 `dsh-session-log-export` 明确只做浏览器 ZIP(原始 JSONL + 子会话 + 附件),"Avoid it when a programmatic or Host-side export is needed: this package produces a browser download, not a Host path write"(`dsh-session-log-export/README.md:34`)。本插件补的正是这一格:**模型可调、写宿主路径、散文而非 JSONL**。这一格是真的,但也仅此一格。

**判断:不是锚,是"补一格"的薄工具。** 声量来自宿主目录项目,扩散为 0,机制上没有可被复用的接口。

## 代价与边界

按发生顺序列:

1. **冷会话直接失败。** 重启 DSH 后 `all: true` 得到空列表,指定 `sessionId` 得到 `export_session: 没有可导出的会话`(`src/index.ts:75-77`)。README 与工具描述都没写这个限制(`README.md:23-24` 只说"当前/指定/全部 live")。
2. **系统提示静默消失。** 在 DSH 0.2.x 上 `header.system` 已被 `system/message` 取代(`types.d.ts:225-228`),插件不读后者,于是导出文档没有系统提示,也没有任何警告。
3. **大 session 无保护。** 五次全量遍历 + 整串拼接 + 单次 `writeFile`,不看 `exec.signal`、无超时、无上限。一个把 50 MB 工具输出读进上下文的会话,导出时要在内存里再复制数份;取消工具调用也不会中止导出。
4. **路径语义有洞。** `path` 以 `.md`/`.html` 结尾且非 `all` 时被当作精确文件(`src/index.ts:451-453`),但扩展名只按**字符串**判断、不看 `format`:传 `{format:'html', path:'out.md'}` 会把 HTML 写进 `.md`。`all: true` 时同一路径被当目录(`454`),若它本身是 `x.md` 就会 `mkdir` 出一个名为 `x.md` 的目录。
5. **静默覆盖 + 默认落在工作区。** 默认目录是 `session.header.cwd ?? process.cwd()`(`456-457`),文件名是"首条用户消息前 60 字 slug + sessionId"(`449`、`439-445`),`writeFile` 无 `wx` 标志(`84`)。在仓库里跑一次导出,产物就落在仓库根,容易被 `git add`;重复导出覆盖旧文件,没有提示。
6. **隐私面无任何处理。** 导出的内容是完整思维链 + 工具参数 + 工具结果,没有脱敏、没有排除规则;默认落在会话 cwd,而 cwd 往往就是被版本控制的仓库。叠加第 2 节的三处丢弃:`source` 不分(把注入内容当用户原话)、`surfaceOp` 不过滤(替换副本重复)、`feedback/*` 删除标记不处理——**用户在 UI 里删掉的消息仍会出现在导出文件里**。这条我只从事件词表(`known-event-types.js` 含 `feedback/message-delete`、`feedback/message-put`)与"插件不读任何 `feedback/*`"两头确认,`feedback` 事件的具体载荷未在本机类型里定义,标为判断。
7. **附件永远丢失且无占位。** `extractTexts` 只认 `type === 'text'`(`383-392`),图片/文件块在 Markdown 与 HTML 里都不留痕迹。对"截图很多"的会话,导出的"完整复盘"是残缺的,而读者无法从文档看出缺了什么。
8. **Markdown 可注入。** 用户或工具输出里的 `<script>`、`</details>`、裸 ``` 原样留在 `.md` 里(`251`、`261`、`264`),把这份 md 贴进任何会渲染 HTML 的地方都要先消毒。
9. **维护面。** 功能提交停在 2026-08-16,此后 94 天只有文档改动;peer 范围锁在 `0.1.0-rc.6`,与当前 0.2.x 已经错代。npm scope `@dsh-suite` 由作者单方控制,升级路径只有重新 `dsh plugin add`(README 没有升级/回滚说明)。

## 可信度与复现

- **★★★ 的范围**:插件目录 716 行全部读过(`src/index.ts` 逐行),并对照了本机 DSH 0.2.1-rc.5 的 `dsh-session`、`dsh-tools`、`dsh-llm`、`dsh-agent-loop`、`dsh-session-log-export` 的相关实现。
- **渲染函数实跑过**:把 `src/index.ts` 的 5 行 import 换成 stub(仅 `defineTool`/`SessionId` 两个空壳,渲染逻辑逐字未改),用 `node --experimental-strip-types` 跑了两组合成事件(冒烟脚本原样 12 条 + 一组含注入内容/多 block/图片/错误原因的探针)。本文所有"实测"结论来自这两次运行,不是推断。
- **未跑**:真实 DSH profile 里的端到端(需要 API key 与真实会话),这也是 README:116 自承未闭环的那一段。
- **未读**:仓库的 `data/plugins.json`(它自己的目录数据)、`site/` 生成器、`compat-check.mjs`;`dist/index.js` 只做了抽查(404 行,`102`/`196-197` 与源码同构,确认 npm 产物与仓库一致)。

```sh
# 1) 稀疏克隆(主项目 508 MiB,必须 sparse)
git clone --depth 1 --filter=blob:none --sparse https://github.com/whyihaveyou/dsh-suite.git repo
cd repo && git sparse-checkout set packages/plugins/plugin-session-export
git log -1 --format='%H %aI %s'
# → 10152cc3076a199762f7eb5b4b8bd14571a89e4c 2026-11-18T04:23:40Z data: hourly refresh [skip ci]

# 2) 子目录历史(浅克隆拿不到,走一次 API,查询日 2026-11-18)
curl -s "https://api.github.com/repos/whyihaveyou/dsh-suite/commits?path=packages/plugins/plugin-session-export&per_page=100" \
  | python3 -c "import json,sys;[print(c['sha'][:10],c['commit']['author']['date'],c['commit']['message'].splitlines()[0][:60]) for c in json.load(sys.stdin)]"
# → 7 条:4312f59b40 2026-08-30 / f0c1a42374 2026-08-16(v0.2.0) / … / a68e96ae95 2026-08-13(launch)

# 3) 仓库级事实(星标归属)
curl -s https://api.github.com/repos/whyihaveyou/dsh-suite | python3 -c \
 "import json,sys;d=json.load(sys.stdin);print(d['created_at'],d['stargazers_count'],d['forks_count'],d['size'])"
# → 2026-08-13T13:32:50Z 69 14 520468

# 4) 扩散(只在本 registry,分母 11744)
grep -ril 'whyihaveyou' data/plugins/ | wc -l        # 4,全为本仓库四条子目录条目
grep -ril 'export_session' data/plugins/ | wc -l    # 0
grep -ril 'session-export' data/plugins/ | wc -l    # 6
grep -ril 'session-export' data/plugins/
#   JohnXu22786__session-export.yml            ← 别人,人工排除
#   yangyongzhen__dsh-session-export.yml       ← 别人,人工排除
#   kittimzhe__dsh-session-export.yml          ← 别人,人工排除
#   bwndlct__dsh-session-export.yml            ← 别人,人工排除
#   cnhenaihui__dsh-session-export.yml         ← 别人,人工排除
#   whyihaveyou__dsh-suite--…-session-export.yml ← 自身
grep -ril '会话导出' data/plugins/ | wc -l          # 10,除自身外 9 条都是别人自述里提到会话导出,零引用本插件
grep -ril 'dsh-suite' data/plugins/ | wc -l        # 5 = 4 条自身 + STARDUSTLC666/dsh-suite(同名异库)

# 5) npm 侧(边车缺口的替代证据)
curl -s "https://registry.npmjs.org/@dsh-suite%2Fplugin-session-export" | python3 -c \
 "import json,sys;d=json.load(sys.stdin);print(d['dist-tags'],list(d['versions']),d['time']['created'])"
curl -s "https://api.npmjs.org/downloads/point/last-month/@dsh-suite/plugin-session-export"
# → {"downloads":188,"start":"2026-10-18","end":"2026-11-16"}
```

## 待验证

1. **端到端是否真能落盘**:`README.md:116` 自承"模型调 → 落盘 → 读回"未闭环。需要在真 profile 里跑一次 `export_session({path:'/tmp/x'})`,确认 `exec.agent.session` 在 Web 会话里始终非空、`header.cwd` 与工作区一致。
2. **0.2.x 上的系统提示**:本机类型说 `header.system` 是 `never`,但旧日志(0.1.x 写入)可能仍带该字段——`request/header` 的校验会拒收还是容忍,未实测;这决定"系统提示为空"是永久还是仅新会话。
3. **大文件边界**:未测 10 MB / 100 MB 级会话的内存峰值与耗时;`Section[]` + 拼接串的实际放大倍数未知。
4. **`feedback/*` 的删除语义**:`known-event-types.js` 列出 `feedback/message-delete`/`message-put`,但本机 `types.d.ts` 没有它们的载荷定义(应由某个包做模块扩展)。"删掉的消息仍会导出"目前是判断,不是断言。
5. **子agent 归类的误判率**:`isSubagentTool` 是名字正则(`src/index.ts:241-243`),`codex`/`fork`/`spawn` 这类子串会误伤同名普通工具,`team_*` 类委派又会漏判;真实会话里各占多少未统计。
6. **42 → 69 的曲线**:需要 stargazers API 的 `starred_at`(未授权 401)或 star-history,才能证明增长主要发生在目录/site 功能上线之后,而不是 v0.2.0 之后。
7. **npm 188 次下载的分布**:按版本拆分(0.1.0 vs 0.2.0)与来源(CI 拉取 vs 真人安装)未知;188 也可能是兼容性巡检机器人的重复安装。
