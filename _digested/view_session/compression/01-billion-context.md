# billion-context — 夹在宿主与模型 API 之间的本地压缩代理，DSH 侧只用两行 bundle 条目把宿主原生自动压缩顶掉

> 证据等级:★★★(源码级;`ranxianglei/billion-context@548e396022b9391e28a3c9061560be297779b8e8`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标:**边车无记录(2026-08-19 采样缺口)**,不是 0;⚠ 下载同为该日缺口。
> 实时口径(2026-11-18,GitHub API):星标 7,806(编排者查询)/ 7,808(我 15:0x 复读),属**主项目仓库**;npm `billion-context` 周下载 935,148(2026-11-10~16)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `ranxianglei/billion-context`（[registry](../../../data/plugins/ranxianglei__billion-context.yml)） |
| 类目 | session（[census](../../ecosystem/census.py) 914 条 / 全表 11 744 条） |
| 子分类 | `compression`（上下文压缩代理）——本册新建分型，本卡是它的第一个成员 |
| 自述 | 上下文压缩插件：小窗口够用（100K）、省 token（5 倍）、数月级单会话（几十亿 token） |
| 星标 ⚠ | **无记录（2026-08-19 采样缺口）**；2026-11-18 实时 7,806（我复读 7,808）。⚠ 归属主项目，非 DSH 适配层（见"为什么它突出"） |
| 下载 ⚠ | **边车无记录**（`data/downloads.json` 624 条里没有本仓库）；npm 周下载 935,148（2026-11-18 查 `api.npmjs.org`，区间 11-10~11-16） |
| 扩散 | **6**（口径：`grep -ril 'billion-context' data/plugins/` 命中 7 条，减去自身；命中逐条见"为什么它突出"） |
| 仓库 commit | `548e396022b9391e28a3c9061560be297779b8e8`，2026-11-18 14:08 +0800，`Merge pull request #7083 from ranxianglei/design/6884-wire-client-sidecars`；master；仓库创建 2026-08-06 |
| 包形态 | npm 包 `billion-context` 0.1.216（CLI `bili`/`bili-proxy`）＋ **DSH bundle**（`package.json:122-127` 的 `dsh.bundle.patch` → `dsh.bundle.patch.yml`）＋ 一个由插件自己 spawn 的**本地代理进程**；压缩引擎是同仓 `kernel/`（npm 名 `acp-kernel`，tsup 内联） |
| 代码规模 | 仓库 85,480 KB（≈83.5 MiB）；`src/**/*.ts` 323 文件 **173,530 行**；`kernel/src/**/*.ts` **26,229 行**；`tests/**/*.ts` 365,167 行。**DSH 专属适配 4,694 行**（`dsh-native.ts` 3171 + `dsh-native-client.ts` 1175 + `dsh-compaction-disable.ts` 223 + `dsh-compaction-gate.ts` 20 + `dsh-acp.ts` 105） |
| 宿主面 | README 客户端表列 **22 个具名宿主**＋"everything else"（`README.md:96-118`）；DSH 只是其中一行 |

## 它到底是什么

**一句话：它不是"一个 DSH 插件"，是一台多宿主压缩代理的 DSH 接入口。** 三件套，缺一层都跑不起来：

1. **一个本地 HTTP 代理进程**（`bili start` / 插件自 spawn）。它站在宿主与模型 API 之间，看完整请求体与响应流，把被折叠区间从出站视图里拿掉。
2. **一个压缩引擎库** `kernel/`（npm 名 `acp-kernel`）。`kernel/README.md:9` 把契约写得比任何自述都准："**the model writes the summaries; this library orchestrates everything around them**"——内核自己从不调模型（`:9`），它只决定何时压缩、压哪一段、状态怎么记。API 是纯函数式的 `processTurn({messages,state}) → {messages,state,nudge?}` / `applyCompression({call,state})`（`kernel/README.md:19-21`），"**stateless with respect to storage**"（`:24`）：状态由宿主存。
3. **每个宿主一层薄适配**。DSH 这层不只注册工具，还做三件宿主特有的事：改 `globalThis.fetch`、抢宿主自己的压缩车道、注册 `/acp` 命令。

**数据模型**（`kernel/src/types.ts`）：核心状态是 `blocks[] + messageRefs + tokenSnapshot + nudge + stats`（`:310-330`）。一个 block 带 `blockId/runId/tier(1|2|3)/summary/directMessageIds/effectiveMessageIds/directBlockIds/survivedCount/active/expanded/restoredInline`（`:68-98`），`CompressionTier = 1 | 2 | 3`（`:57`）——所谓"增量分层摘要"就是这个三层的 LSM 式结构（`kernel/README.md:7`），tier-1 块堆到阈值就发 tier-2 蒸馏提示、tier-3 类推（`kernel/README.md:271`）。

**核心循环**（模型主导，不是自动摘要）：模型收到 nudge 后自己调 `compress({startId,endId,summary})`，摘要正文由模型写；内核只把这条 call 记成 block，把覆盖到的消息在出站视图里移除、在原位渲染一条 `role: "system"` 的摘要消息，头是 `"[Compressed conversation section]"`（`kernel/src/prune.ts:4`），带保留前缀 id `acp_summary_`（`:9`，渲染在 `:555-567`）。可逆性由此而来：**原文没有被删**，只是被覆盖渲染；`decompress(b3)` 把块取回（`kernel/README.md:64`），`search_context` 在摘要与可见消息里检索（`kernel/src/compress-tools.ts:19-23`）。

## 怎么接进 DSH

**两条车道，同一个包**（`docs/clients.md:14-25`、`:27-35`）：

- **launcher**：`bili dsh`——写一份 `--patch` overlay 到 `~/.dsh-bili/.bili-acp.patch.yml`（`src/launcher.ts:3598-3620`），用 `dsh web --patch <file>` / `--patch <file>` 拼进 argv（`dshArgsWithPatch`,`:3628-3634`）。
- **profile install**：`bili plugin install dsh` ≡ `dsh plugin --profile <name> add billion-context`，pnpm 装进每个 profile 自己的 `node_modules`，**bundle patch 由 dsh 自己 mount**（`src/launcher.ts:7283`，`docs/clients.md:27-35`）。

**manifest 契约只有两个键**（`package.json:122-127`）：`dsh.bundle.patch` 指向 `./dsh.bundle.patch.yml`，`dsh.client.platform = "web"`（浏览器半边 `dsh-native-client.ts`，1175 行，面板入口）。入口子路径也是契约的一部分：`"./dsh"` → `dist/agent/dsh-native.js`（`:10`）、`"./dsh-compaction-gate"` → `dist/agent/dsh-compaction-gate.js`——bundle 里那两行 `name` 就指着这两个子路径。

**patch 五块，逐块说清**（`dsh.bundle.patch.yml`）：

| 行 | 内容 | 干什么 |
|---|---|---|
| `:21-25` | `insert: [bili-native→billion-context, bili-compaction-gate→billion-context/dsh-compaction-gate]` | 挂两个 cordis entry。**两行同一个包的两个 export**，不是一个插件的两份拷贝 |
| `:26-28` | `- id: compaction-basic / config: auto: false` | 关掉**宿主层**的自动压缩 |
| `:32-39` | `preset-standard/ptc/minimal/cordis` 各 `inject: [biliBasicCompactionPolicy]` | 让四个 Web 预设**等门**再 register |
| `:46-55` | `llm-deepseek` / `llm-deepseek-account` 的 `retryPolicy.retryableCodes` 重述 6 个码 | DSH 默认白名单缺 `MALFORMED_RESPONSE`，一次采样抖动就能打死整轮 |

**`bili-native` 与 `bili-compaction-gate` 各做什么**——这是本卡最值得记的一处工程设计：

- `bili-native`（`src/agent/dsh-native.ts:80-81`，`inject = ["tools","commands","agents"]`）是主体：解析 plan（attach 到已有代理或 spawn 一个）、`ensureProxyRunning`、改 `globalThis.fetch` 与 Codex Responses 的 WebSocket（`installDshIntercepts`,`:2964-2969`）、把代理的 tool manifest 逐字注册成宿主原生工具（`toolDefinition`,`:911-938`；`ctx.tools.register`,`:1010`）、注册 `/acp` 与 `/acp-cache`（`:2926-2935`）。它**还负责声明"本进程抢下了压缩车道"**：`apply()` 里 `declareDshCompactionActive()`（`:1967-1974`）。
- `bili-compaction-gate`（20 行，`src/agent/dsh-compaction-gate.ts:15-20`）只做一件事：`inject = []`，无依赖，`apply()` 调 `registerCompactionDisable(ctx)`。它提供 `biliBasicCompactionPolicy` 这个 service，并注册 `internal/config` 中间件。

**gate 为什么必须独立常驻**：`dsh-compaction-gate.ts:1-10` 写的是事故复盘——早期 gate 的 service 由 `bili-native` 提供，于是"禁用/杀掉 bili-native"会同时拿掉四个 Web 预设 `inject` 等待的 service，**dsh 启动时四个预设永远 pending，新建会话直接砖掉**。拆出来之后：gate 永远活着、service 永远可满足，而"要不要真的 disable"由 `globalThis.__BILI_DSH_COMPACTION_VERDICT__` 上的进程级判决决定（`dsh-compaction-disable.ts:68-77`，判决缺席 = bili-native 没跑过 = 每行按宿主原样放行，`:186-190`）。两种 entry 是**不同 bundle、不同模块实例**，`globalThis` 是唯一能跨的缝（`:69-71`）。

**`preset-*` 的 `inject` 解决什么**：DSH 的 patch 引擎只能按 id 命中**顶层行**与真正的 group 子行，命不中"预设 entry 的 `config.plugins` 里嵌的那一行"（`dsh-compaction-disable.ts:14-16`；宿主侧证据：本机 dsh 0.2.1-rc.5 的 `dsh-web-app/presets/standard.patch.yml:66-76`，`compaction` 组的 `config` 是数组，里面才是 `compaction-basic: '@deepseek-ai/dsh-compaction-basic'` 与 `command-compact: '@deepseek-ai/dsh-command-compact'`）。所以 `auto:false` 落在 Web profile 上等于打在已经关掉的那一行上（`docs/clients.md:117-124`）。`inject` 是**顺序保险**：预设拿不到 service 就不能 register，于是 gate 的 `internal/config` 中间件（`dsh-compaction-disable.ts:186-204`，`{global:true}` 的 waterfall）保证在任何预设解析 config 之前就已就位；真正生效的动作在那个中间件里把嵌套行改成 `disabled: true`（`disableBasicCompaction`,`:155-167`）。注意 `inject` 列表**是被 patch 整体替换、不是追加**（`dsh.bundle.patch.yml:29-31`）——这是这一层最脆的一处，见"代价与边界"。

**`compaction-basic auto:false` 与宿主版本的关系**：它只对**非 Web profile** 有效。当 profile 的 bundles 含 `@deepseek-ai/dsh-web-app` 时，实例活在 agent preset 里，`auto:false` 打空（`dsh.bundle.patch.yml:5-13`）。而 gate 这条 overlay 走的是 **cordis 的 INTERNAL `internal/config` 钩子**，版本敏感：钩子挪了位置就退化成大面积静默失败。作者为此留了两级兜底——① `detectCompactionOverlayGap()`（`dsh-compaction-disable.ts:219-223`）在启动时探测 `ctx.on` / `ctx.reflect.provide` 是否都在，缺就在 boot 期**响一声**（`dsh-native.ts:2905-2917`）；② `#2474` 的 profile 级 full-snapshot 覆盖（把 `preset-standard` 整块 config 抄下来改 `auto:false`），文档明说"partial snippet 会静默丢掉没重述的一切"。本机对照：0.2.1-rc.5 上 `internal/config` 确实存在（`cordis-plugin-loader/lib/index.js:402` 的 `ctx.waterfall(fiber,"internal/config",raw,…)`、`cordis/lib/index.js:1346`），并**没有**给 `preset-standard` 写自己的 `inject`——所以当前版本上"替换而非追加"的雷还没被踩到。

**DSH 侧自研多少行**：4,694 行 TS。其中真正原创的是 `dsh-native.ts`（3,171）+ `dsh-native-client.ts`（1,175）+ 装配/生命周期；`dsh-compaction-disable.ts` 的 overlay 本体注明是 vendored（`deshark42/dsh-compaction-basic-disable` v0.1.1，MIT，`:1-8`），223 行里大半是覆盖率遥测与测试钩子。`src/launcher.ts`（7,794 行）里的 DSH 分支没切出来单算——它是 22 个宿主共用的启动器。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `dsh.bundle.patch.yml` | 55 | DSH 侧唯一的声明式接线：2 个 entry + 1 个 `auto:false` + 4 行 `inject` + 2 块 retry 策略 | `:21-25`、`:26-28`、`:32-39`、`:46-55` |
| `src/agent/dsh-native.ts` | 3,171 | 宿主半边：plan/spawn、fetch+WS 拦截、工具注册、`/acp`、标题通道、归因、gate 判决 | `:1-38`（七步自述）、`:911-938`、`:1062-1075`、`:1967`、`:2926-2935` |
| `src/agent/dsh-compaction-gate.ts` | 20 | 常驻门：`inject=[]`，只 `registerCompactionDisable` | `:15-20` |
| `src/agent/dsh-compaction-disable.ts` | 223 | 载入时 overlay：`internal/config` waterfall 把嵌套 compaction 行改 `disabled:true`；发布 `biliBasicCompactionPolicy`；覆盖率遥测 | `:37-40`、`:52`、`:64-66`、`:155-167`、`:183-208`、`:219-223` |
| `src/agent/dsh-native-client.ts` | 1,175 | 浏览器半边（`dsh.client.platform=web`）：设置面板 iframe 入口 + 代理 origin 轮询 | 文件头 `:1-18`；origin 双路 `#1809` |
| `src/launcher.ts` | 7,794 | `bili dsh` 车道：写 `.bili-acp.patch.yml`、`--patch` 拼参、native-install 时改走 wire 级拒绝 | `:3598-3620`、`:3628-3634`、`:7283-7303` |
| `kernel/src/compress.ts` | 2,654 | 压缩应用端（`createCore`,`:342`） | 全文件 |
| `kernel/src/compress-tools.ts` | 920 | 工具 schema 与三协议 system prompt 的唯一来源：`compress`/`decompress`/`search_context`/`acp_status`/`acp_cache` + 可选 `acp_retire`/`acp_restore`/`acp_rewrite`/`absorb` | `:19-31`、`:217-219` |
| `kernel/src/prune.ts` | 668 | 出站视图渲染：摘要头、`acp_summary_` 保留前缀、摘要锚点 | `:4`、`:9`、`:555-567` |
| `kernel/src/ccr.ts` | 675 | 无损取回（CCR）：超大工具结果到达即换占位符、原文进 per-session content store | `:24-41`（"replace-once-at-arrival … prefix-cache stable"） |
| `kernel/README.md` | 319 | 引擎契约：模型写摘要、内核编排、三层 LSM、tier 触发 | `:7`、`:9`、`:24-28`、`:64`、`:271` |
| `docs/clients.md` | 1,146 | DSH 两车道、WS 腿、Web profile 压缩、常见故障 | `:14-25`、`:27-35`、`:62-70`、`:117-160` |

**数据流（三条，别混）**：

```
① 模型请求（DSH 进程内）
   dsh agent loop ──fetch / Codex-Responses WebSocket──▶ globalThis.fetch 补丁(native-intercept.ts)
        │  重写为 <proxy>/bili/<upstream-url>，盖 x-bili-plugin / x-bili-plugin-conversation
        ▼
② 本地代理进程（ephemeral port，parent-pid watchdog = 这个 dsh 进程）
   kernel：processTurn → 增长 nudge → prune 渲染 <acp_summary_*> → 转发上游（未折叠区间逐字）
        ▼
③ 上游模型 API
```

```
④ 工具回路（模型主动）
   model ──tool_call compress{startId,endId,summary}──▶ ctx.tools.execute(:920-936)
        ──forwardTool──▶ 代理 /__bili/plugin/tool ──▶ kernel applyCompression
        ──▶ 下一轮请求的视图里那一段变成一条摘要
```

**为什么用 fetch 补丁而不是 baseURL 改写**：`dsh-native.ts:11-15` 写的是"改 `globalThis.fetch`，两种模式都把模型 API URL 重写成 `<proxy>/bili/<url>`"；loopback 目标永不代理，于是 launcher 的 MITM 环境变量被自然绕过。第二条腿是 WebSocket：DSH 内嵌 pi-ai 的 `openai-codex` provider 默认 `transport: auto`，一次成功的 WS 往返**从不调用 fetch**，只装 fetch 腿等于整段会话绕过代理（`:2964-2969` 的 `installDshIntercepts` 两条腿都装）。

**prefix-cache 是这套设计的硬约束，不是优化项**：`tokenSnapshot` 在消息首次渲染时写死一次、此后只读，理由就写在注释里——"stable across density recalibration so rendered `<acp tokens>` tags do not churn and bust the provider prefix cache"（`kernel/src/types.ts:313-318`）；CCR 用"到达即替换一次"保证可见字节此后永不变（`kernel/src/ccr.ts:39-41`）。DSH 侧还有一个同类动作：`apply()` 会**等到工具注册落地**才返回（`dsh-native.ts:2940-2953`，2 秒上限），因为宿主每轮按"当前已注册工具集"重组请求——fire-and-forget 注册会让第 1 轮没有 ACP 工具、第 2 轮有，每开一个新会话就把整个前缀缓存打碎一次（`#4134`）。

**测试**（能证明契约的那部分）：`tests/` 里 **45 个 `*dsh*.test.ts`**，加 `tests/e2e/e2e-native-dsh.test.ts`、`e2e-native-dsh-persona.test.ts` 两条真客户端 e2e。其中 `tests/issue3662-dsh-gate-fallback.test.ts:1-15` 直接钉住本卡的机制：从 `dsh-compaction-gate.ts` 与 `launcher.ts` 两侧取真代码，断言"entry 被禁用 / env kill-switch ⇒ 判决缺席 ⇒ 预设回落到**宿主原生压缩**，不是第三种悬挂态"。`tests/dsh-patch-entries.test.ts` 钉 patch 解析的块归属语义（`disabled: true` 只属于自己那个 block）。压缩侧 `kernel/tests/` 150 个文件，含 `compress.test.ts`、`decompress-report.test.ts`、`compress-schema-contract.test.ts`、`ccr.test.ts`。恢复/回滚面另有 `dsh-fork-adopt.test.ts`、`issue2432-dsh-local-compaction.test.ts`、`dsh-authored-compaction.test.ts`。

## 为什么它突出

**先拆星标归属——这是本卡最重要的判断。** 时间线：

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-06 | 仓库创建 | GitHub API `created_at` |
| **2026-08-19** | **边车采样点（本仓库无记录 = 缺口）** | `data/stars.json` |
| 2026-09-18 | 首个 DSH 文件落地：`8eca91f` "feat: dsh-side install channel (#949)" **新增** `dsh.bundle.patch.yml`；`src/agent/dsh-native.ts` 亦在此窗口出现（`until=2026-09-18T12:00Z` 对该路径返回空，`until=2026-09-19` 才命中 `c1bf0e4`） | GitHub API `commits?path=` |
| 2026-11-18 | 实时 7,806 / 我复读 7,808；624 fork；1,245 open issue；master `548e396` | GitHub API |

采样日比第一个 DSH 提交**早 30 天**：边车即便有记录，也不可能包含任何 DSH 侧的增量；而 7,806 这颗星挂在**一个 22 宿主、26,229 行内核、365,167 行测试的主项目**上，DSH 只是 `dsh.bundle.patch.yml` 那 55 行。**结论：星标记在主项目名下，不记在 DSH 适配层。** npm 周下载 935,148 同理——那是 `bili` CLI 的安装量，不是 DSH bundle 的使用量。

**再看扩散 6 条，逐条判断（`grep -ril 'billion-context' data/plugins/` 命中 7，减自身）**：

1. `Tyan66666/billion-context-dsh` —— 独立的 DSH 重写（自述 "Model-driven context compression (Active Context Pruning) for DeepSeek Harness"），星标 ⚠26；
2. `No-ni/billion-context-patched` —— 明写 "A patched build of ranxianglei/billion-context (MIT)"；
3. `wxzjss/dsh-whale-loli` —— 三个 agent 预设，明写"上下文压缩交给 billion-context 插件"；
4. `light-cheng/dsh-strata` —— 安装须知里点名"请先卸载 billion-context"，因为它抢同一行压缩配置；
5. `kkkkk-tubu/dsh-deep-purge` —— 清 DSH 会话时要连 "billion-context SQLite index" 一起 VACUUM；
6. `FenrirCait/dsh-session-leftover-purge` —— 专清 "billion-context snapshots"。

**这 6 条全部指向主项目，没有一条在谈 DSH bundle 那一层。** 但它们的形状值得记：两条是派生（fork / patched build），一条是把压缩**委派**给它，三条是**因它落盘而必须写的清理/冲突工具**。最后这一类说明它已经进入别人的故障模型——在本册里这比"被引用"更硬。

**机制上真正独特的一点**：它不是"再做一个摘要器"，而是**把宿主的压缩车道整体顶掉**，并且用一条 cordis INTERNAL 钩子做到了 patch 引擎表达不了的事（改预设内部嵌套行）。代价是这条路版本敏感、依赖一个非公开钩子；收益是用户不用改 profile 就能让两套压缩不打架。这个"抢车道"的设计在 DSH 上是有必要的——两套压缩同时落地会互相摧毁折叠基底（`dsh-compaction-disable.ts:10-16`）。

## 代价与边界

- **双层压缩冲突是这套设计的原点，也是它最大的脆弱点。** 只要 gate 没 latch 上（钩子改名、profile 形态变了、`inject` 被 patch 替换掉），宿主原生压缩就重新武装；而 `bili` 的 wire 级拒绝只能拦住"经过代理的压缩调用"，**拦不住 dsh 自己在本地写 checkpoint**（`dsh-native.ts:2909` 原话："CANNOT stop dsh writing its checkpoint locally"）。后果不是报错，是折叠基底被 durable 遮蔽，几天后以 "compression conflict" 横幅出现。
- **patch 的 `inject` 是替换不是追加**（`dsh.bundle.patch.yml:29-31`）。哪天 DSH 给 `preset-standard` 自己加了 `inject`，这份 patch 会把它整条覆盖掉，而失败现象是"某个预设起不来"，很难归因。
- **`compaction-basic auto:false` 的覆盖面随宿主形态变化**：非 Web profile 有效、Web profile 无效（靠 gate）、桌面版 `dsh-app://` 又是第三种形态（`docs/clients.md:100-110` 记了 `#5686` 的静默失败）。launcher 在检测到 native install 时会**主动不打**这份 patch（否则 `id: bili-native` 重复、dsh 直接启动失败，`src/launcher.ts:7283-7303`），此时压缩只能靠 wire 级拒绝 + 用户手工上 `#2474` 快照覆盖。
- **隐私：代理看全量 prompt 与响应。** 这是形态决定的，不是实现缺陷——`globalThis.fetch` 被改成把每个模型请求送到 `<proxy>/bili/<upstream>`，压缩必须在本地读完整消息体才能折叠。凭据随请求经过本地代理再转发上游；日志侧有专门的脱敏器（`src/log-mask.ts:1-8`：非公开 LLM 主机名替换为 `<private-host>`，`authorization`/`x-api-key`/`cookie` 换成长度提示），但**脱敏只覆盖日志，不改变"代理能读到 key"这个事实**。
- **落盘**：状态与日志在 `~/.local/state/billion-context/`（`src/paths.ts:96`），统一存储是一个 SQLite（`index.db`，WAL）+ 内容寻址 blob（`src/storage/store.ts:4`），当前版本的默认是**纯 SQLite，不写 JSON 信封**（`CHANGELOG.md` "Unreleased/Changed"）。这三处是第三方清理工具的存在理由（见扩散第 5、6 条）。
- **失败模式，按发生顺序**：
  1. 代理没起来 / 被 kill → 模型流量**直发上游（未压缩）**，会话继续，工具仍在（`dsh-native.ts:960-961`、`:1095`）。
  2. 工具 manifest 拉不到 → 请求以 **wire 模式**走（无 `x-bili-plugin` 头 = 无压缩、匿名会话），重试按 10s 起步的**封顶指数退避**、永不放弃，第 5 次连续失败时在用户面前**说一次**（`dsh-native.ts:84-100`、`:1095`）。
  3. 归因丢失（宿主重试/切模型/睡醒）→ 协商式指纹桥认领，认不出就直发（`dsh-native.ts:1898-1932`）。
  4. 签名类上行（body-covering signature）→ **compress-or-refuse**：没有 re-signer 就本地拒绝，不做无签名透传（`dsh-native.ts:2580`、`:2592`）。
  5. gate 没 latch → 启动期一条持久化告警 + 建议手工快照覆盖（`dsh-native.ts:2905-2917`）；这条是**唯一**会让"两套压缩并存"被用户看见的信号。
- **维护成本**：22 个宿主共用一份内核，任何 kernel 改动要过"人审 + 版本纪律 + 双层测试"（`AGENTS.md` 的 Kernel Boundary）；DSH 侧则要跟一个**非公开钩子**赛跑。
- **兼容成本**：Node ≥ 20（`package.json` `engines`）；profile 里版本漂移有专门的自愈通道（`refreshDshProfileCopy`、`convergeDshLedger`），也说明这条链曾经很脆。

## 可信度与复现

- **★★★（限 DSH 适配层与压缩机制）**：读了 `dsh.bundle.patch.yml` 全 55 行、`src/agent/dsh-native.ts` 的目标段落（文件头 1-38、注册 911-1075、apply 1960-2010、boot 告警 2890-2970）、`dsh-compaction-gate.ts` 全 20 行、`dsh-compaction-disable.ts` 全 223 行、`src/launcher.ts` DSH 两段、`package.json`、`kernel/` 的入口与协议文件（`compress-tools.ts`、`types.ts`、`prune.ts`、`ccr.ts`、`kernel/README.md`）、`docs/clients.md` DSH 段、两份 DSH 测试。**并对本机 dsh 0.2.1-rc.5 做了对照**（`internal/config` 钩子、`presets/standard.patch.yml` 的嵌套 compaction 行）。
- **未读（明确）**：`benchmarks/`、`devlog/`、`paper/`、`advisories/`、`README.ja.md`/`README.zh-CN.md` 等其它语言 README、`src/server/**` 与 `kernel/` 的其余 20k 行、`src/agent/` 里其它宿主的适配（pi/opencode/omp/hermes…）、`website/`、`proof/`、`verif/`。所以关于"压缩质量好不好"的任何判断都**没有**证据支撑，本卡也没写。

```sh
# 1) 提交与规模
git clone --depth 1 https://github.com/ranxianglei/billion-context.git /tmp/an-bili
cd /tmp/an-bili && git log -1 --format='%H %ad'
# → 548e396022b9391e28a3c9061560be297779b8e8 2026-11-18
find src -name '*.ts' | xargs wc -l | tail -1            # → 173530
find kernel/src -name '*.ts' | xargs wc -l | tail -1     # → 26229
wc -l src/agent/dsh-native.ts src/agent/dsh-native-client.ts \
      src/agent/dsh-compaction-gate.ts src/agent/dsh-compaction-disable.ts \
      src/agent/dsh-acp.ts | tail -1                     # → 4694（wc 的 total 行）
ls tests/*dsh*.test.ts | wc -l                           # → 45

# 2) DSH 首个相关提交（浅克隆没有历史，用一次 API；无 token 也可）
curl -s "https://api.github.com/repos/ranxianglei/billion-context/commits?path=dsh.bundle.patch.yml&per_page=1&until=2026-09-18T12:00:00Z"   # → []
curl -s "https://api.github.com/repos/ranxianglei/billion-context/commits?path=dsh.bundle.patch.yml&per_page=1&until=2026-09-20T00:00:00Z"
# → 8eca91f "feat: dsh-side install channel … (#949)" 2026-09-18T13:58:28Z

# 3) 扩散（11 744 个 yml，必须用目录形式，直接展开会 Argument list too long）
grep -ril 'billion-context' data/plugins/ | wc -l   # → 7（含自身 → 第三方 6）
grep -ril 'billion-context' data/plugins/

# 4) 实时取数（2026-11-18）
curl -s https://api.github.com/repos/ranxianglei/billion-context | grep -o '"stargazers_count":[0-9]*'
# → 7808；created_at 2026-08-06T08:27:34Z；default_branch master
curl -s https://api.npmjs.org/downloads/point/last-week/billion-context
# → {"downloads":935148,"start":"2026-11-10","end":"2026-11-16"}

# 5) 宿主侧对照（本机 dsh 0.2.1-rc.5）
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh
grep -n 'internal/config' $DSH/node_modules/@deepseek-ai/cordis-plugin-loader/lib/index.js   # → :402
grep -n 'compaction-basic' $DSH/node_modules/@deepseek-ai/dsh-web-app/presets/standard.patch.yml  # → :73-76（嵌套行）
```

## 待验证

1. **采样日之前的星标曲线**：边车对本仓库是缺口，`stargazers` API 需要 token 才能拿 `starred_at`。拿到才能把"7,806 与 DSH 无关"从时间线推断变成实测。
2. **gate 在真宿主上的覆盖率**：本卡只做了静态对照（钩子存在、嵌套行形态）。`#3962` 的覆盖率遥测（`dshCompactionGateTelemetry()`，`dsh-compaction-disable.ts:125-128`）需要一次真启动才能读到 `covered`/`sawFactoryPreset`。
3. **`#2474` 快照覆盖的实际副作用**：文档说 partial snippet 会丢掉没重述的一切（含预设自己的 `id`/`order`），但我没跑过一次"照 recipe 改完再启动"。
4. **代理落盘的粒度**：`index.db` 里存的是折叠状态、摘要、blob，还是连原始消息体一起留？只读了 `src/storage/store.ts` 的头部注释，没读 schema。
5. **`dshAuthoredCompaction`（`dsh.authoredCompaction`，默认 true）** 的行为边界：它让 bili 在本地**代答** dsh 的压缩请求（`CHANGELOG.md` 0.1.203 段），与 gate 的 disable 是两条独立机制，二者的交互没读。
6. **e2e 未跑**：`tests/e2e/e2e-native-dsh.test.ts` 需要真 dsh + 真模型端点，本卡全部结论来自源码与文档，没有运行时证据。
7. **`BILI_DSH_AUTHORED_COMPACTION` / `BILI_NATIVE_DSH` 等开关的当前默认值**：只从文档与注释读到，没在 `src/knobs.ts` 里逐个核对。
