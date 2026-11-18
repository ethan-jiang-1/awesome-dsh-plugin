# odai — 把五问治理写进 systemPrompt、把职责路由与证据落在独立 JSONL 的 profile 级运行时

> 证据等级:★★★(源码级;`orziz/odai@8bd1289197b4b3c01a50c9e80d2fd355214abf7c`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 89 为 2026-08-19 历史采样;下载 1951 同为该日。
> 提交日 2026-11-11;采样与写卡日 2026-11-18。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `orziz/odai#dsh/plugin`([registry](../../../data/plugins/orziz__odai--dsh-plugin.yml)) |
| 类目 | workflow([census](../../ecosystem/census.py) 703 条 / 全表 11 744 条) |
| 子分类 | `governance`(profile 级治理与路由;本卡新建) |
| 自述 | 「面向整个 DSH profile 的治理与路由 bundle,带职责/证据 Web Control Center,以及压缩、本地作用域语义记忆、安全连续性与真实验收;兼容 DSH 0.1.5-rc.1」——**末句已过期**(见「代价与边界」) |
| 星标 ⚠ | **89**(2026-08-19 采样;**仓库级**,非 `dsh/plugin` 子目录);2026-11-18 实时 **133**(GitHub API 复核,同日 forks 20) |
| 下载 ⚠ | **1 951**(2026-08-19 采样;npm 包级;边车无统计窗口字段,见 `_method/01`) |
| 扩散 | **0**(口径:`grep -ril 'odai' data/plugins/` 命中 1 条,即自身;`grep -ril 'orziz'` 同为 1 条) |
| 仓库 commit | `8bd1289`(2026-11-11,`main`,`fix(dsh): restore routing page scrolling and style compaction settings`);仓库首提交 2026-03-19,首个 `dsh/` 提交 2026-08-14 |
| 包形态 | npm `odai-dsh-plugin@0.3.7`(`latest`,2026-08-14 建包,已发 60 个版本);`package.json` 的 `dsh.bundle.patch` + `dsh.client`(web,4 个 inject);bin 一个;peer `@deepseek-ai/dsh@0.2.2-rc.1` 且 optional;node ≥22.15 |
| 代码规模 | `dsh/plugin/` 15 文件 **2 042 行**(含测试 1 694);包内 `runtime/` 来自 `dsh/runtime/src` **52 文件 13 942 行**,客户端 `dsh/client/src/index.mts` 1 137 行;运行时测试 38 文件 15 392 行 |
| 仓库体量 | 390 个 git 文件,GitHub API `size` 35 736 KB(≈35 MB),20 forks |

## 它到底是什么

**一句话:odai 本体是一个「五问」治理框架 + 可选职责编排;`dsh/plugin` 是让它整层接管一个 DSH profile 的打包壳,机制在打包进来的 1.4 万行共享运行时里。**

先把三层拆开,否则会误判成配置包:

1. **治理正文**——`skills/odai/SKILL.md`(74 行)是 canonical 治理,`manifest.json` 标 `schemaVersion: 5`、`skillVersion: 0.7.1`、`runtimeContract: 9`,并声明 12 个文件(含 `SKILL.md`、`manifest.json`、8 个 `references/*.md`、`agents/openai.yaml`、`assets/task-state.md`)。它按「事 / 实 / 法 / 成 / 界」五问组织(`SKILL.md:12,20,28,37,45`),开篇一句是「事由人定,路由实证;法随势变,成由验定;止于边界,成事而不妄为」(`SKILL.md:8`)。
2. **共享运行时**——`dsh/runtime/src/` 52 个 `.mts`。它不静态 import 任何 `@deepseek-ai/*` 包,宿主形状全部手写在 `runtime-types.mts` 里;**唯一**的宿主包依赖是压缩适配器里的动态 `loader.import`(`compaction-pressure-runtime.mts:107`),用来拿 `BasicCompactionEngine`/`SessionSeq`/`LlmError` 等内部 API。
3. **profile 壳**——`dsh/plugin/` 只有 manifest、7 行 patch、一个已废弃的 bin、README 和 9 个测试/探针文件。`npm pack` 时把 `runtime/`、`skills/`、`client/` 复制进来(`package.json:63`),所以**读 `dsh/plugin/` 目录本身会严重低估工作量**,而读 `runtime/` 又看不出它怎么被装进 DSH。

**五问落在哪(源码可查,不是自述)**:

| 治理面 | 正文 | 运行时落点 | 实际机制 |
|---|---|---|---|
| 事(目标) | `SKILL.md:12-18` | `prompt-runtime.mts:154-158` | canonical 正文作为 `odai:canonical-governance` section 注入,`order: -20`(最靠前);另有需求账本把每条 requirement 绑定到**认证过的直连用户消息**,最多 12 条、4 000 字符、禁止环状取代(`responsibility-gap.mts:31-68`) |
| 实(事实) | `SKILL.md:20-26` | `session-evidence.mts:99-102,249-279` | 每条治理事件写 `$DSH_HOME/odai/session-evidence/<sha256(sessionId)>.jsonl`;工具结果只留结构摘要 `odai/tool-observed`(`tool-runtime.mts:360-374`) |
| 法(做法) | `SKILL.md:28-35` | `router.mts:436-595` | 词面信号只产生 `considerations`(带 `unmet` 缺口),不足以升级;真正触发要结构化 task-state gap 或高风险组合 |
| 成(验收) | `SKILL.md:37-43` | `review-evidence.mts:21-34`、`routing-context.mts:590-609` | reviewer 只拿到本轮不可变证据快照(SHA-256 digest、200 万字符/500 条上限、64 KB/40 次读取预算);diff、write、test、check 各自带「最后一次写之后」的序号判定 |
| 界(授权) | `SKILL.md:45-52` | `governance.mts:4-29,64-80,130-159` | child 只有 8 个工具(读/搜/`odai_review_evidence`/回交);高风险未决时控制器降到 13 个只读工具;两条 guard 各自返回 `ODAI_SUBAGENT_BOUNDARY:` / `ODAI_HIGH_IMPACT_ROUTE_BLOCKED:` 拒绝理由 |

**状态机是「职责范围」而不是「任务」**。`responsibility-scope.mts:8` 只有两个状态:`pending` / `active`;`claim` 必须发生在 `startStep` 这一步(`:104-122`)。停止条件有四类,全部由真实 DSH 事件推导:直连用户插话(`agent/inbox/spliced`)、无工具调用的终态回复(`assistant/message`)、`turn/end`、以及 owner 主动 stop(`:145-164`)。停止时**先**发 `odai/route-protection-released` **再**发 `odai/responsibility-scope-stopped`(`:315-327`);恢复时要求 `sameRequestModelRoute(proposed, temporaryRoute)` 才把临时路由换回 base route(`index.mts` 调 `pendingResponsibilityScopeRestoration`,实现于 `responsibility-scope.mts:267-281`)。

**证据账本是这个插件最不像"prompt 工程"的部分**:id 由 type 与关键字段的 stable-JSON 做 SHA-256(`session-evidence.mts:112-136`),同一 id 去重;追加走 `openSync(..., 0o600)` + 循环 `writeSync` + `fsyncSync`,短写时 `ftruncate` 回滚并重抛(`:249-279`);读用「size:mtimeMs」做 revision 缓存失效(`:285-295`)。`agent` 没有 session id 时事件只进内存并尝试 `session.append`,有 session 才落盘(`:330-352`)——这是它敢声称「插件卸载后旧会话仍可读」的根据(README `dsh/plugin/README.md:32`)。

## 怎么接进 DSH

**manifest 只有四个键真正起作用**(`dsh/plugin/package.json`):

- `main`/`exports["."]` = `./runtime/bootstrap.mjs`(:21,:26);`bin.odai-dsh-plugin`(:22-24);`files` 只发 `build/bin`、`runtime`、`skills`、`client`、patch、README(:36-44)。
- `dsh.bundle.patch = ./cordis.patch.yml`(:45-48)——profile 层身份。
- `dsh.client.inject` 4 个客户端包 + `platform: "web"`(:49-57)——Control Center 只在 Web 传输下出现。
- `peerDependencies."@deepseek-ai/dsh" = "0.2.2-rc.1"`,且 `peerDependenciesMeta.optional = true`(:75-82)——**装到别的版本不会报错,只是没有兼容承诺**。

**patch 全文 7 行**(`cordis.patch.yml:1-7`):一条 `insert`,`id: odai-governance`,`name: odai-dsh-plugin`,`config.routing.mode: auto`、`provider: spawn`。`package.test.mjs:18-21` 用断言禁止 patch 里出现 `roles:`/`planner:`/`model:` 等映射——**模型映射绝不进部署配置,只能由用户当轮显式选择**。

**注册点(逐项对应源码)**:

| 注册点 | 位置 | 内容 |
|---|---|---|
| `ctx.inject` | `index.mts:51` | `["systemPrompt","tools","subagents","sessions","llm"]`;`bootstrap.mts` 刻意不声明 inject,以便在宿主 compaction 引擎激活前挂拦截(`bootstrap.mts:9`) |
| systemPrompt sections | `prompt-runtime.mts:154-189` | 8 个 section,order `-20`(治理)、`-19.75`(编排)、`-19`(路由配置)、`-18.875`(安全连续性)、`-18`(技能源)、`-17`(输出策略)、`-16`(压缩模型)、`-15`(语义记忆);每轮按激活状态重写文本(`:438-449`) |
| `ctx.tools.register` | `tool-runtime.mts:106-115,144-263` | **13 个** `odai_*` 工具,第二个参数 `{ when(context) }` 做「每步只解析一次」的条件准入 |
| `ctx.tools.guard` | `tool-runtime.mts:282-352` | 顺序:命名请求 pending → managed reviewer 白名单 → child guard → 路由保护 guard → 重复失败监控 |
| 生命周期 hooks | `lifecycle-runtime.mts:222,240,244,469,551,794,1613` | `agent/inbox/claimed`、`agent/disposed`、`agent/request`、`agent/request-error`、`session/event`、`agent/turn-stopping`、`agent/pre-step` |
| 其它 hooks | `tool-runtime.mts:353,360`;`compaction-runtime.mts:117` | `agent/created`(给子会话继承限制)、`tools/result`、`llm/stream`(只拦 `purpose === "compaction"`) |
| Control Center RPC | `control-center-runtime.mts:18,70-83` | 通道 `/odai-control-center`,4 个端点(routing/evidence/session/compaction-pressure);`rpc.handle(..., { authority: "loopback" })`,有 `connection.fetch` 时改注册 `/api/...` POST |
| 客户端 slot | `dsh/client/src/index.mts:1023-1073` | 注册 view / event kind / `conversation.session.header.utilities`;RPC 走 `odai-control-center/*`(`:366,374,852,892`) |

**安装**:`dsh plugin --profile web add odai-dsh-plugin`(`dsh/plugin/README.md:27`),前置是 PATH 上有 `pnpm`(:24),装完**必须新起一个 DSH 进程**(:30;运行中的进程一直持有启动时载入的字节,:78)。不需要额外 skill 包:canonical `skills/odai` 已在包内。

**与官方机制的关系**:条件工具准入依赖 DSH 0.2.2-rc.1 的 `tools.register(def, { when })` 与 `agent.ctx.tools.restrict`(`dsh/README.md:25`)。本机安装的是 DSH `0.2.1-rc.5`,其 `register(definition)` 只接受一个参数(`dsh-tools/lib/index.js:2974`),`restrict` 存在(`:2991`)——所以 `when` 会被静默丢弃,回退到「完整目录 + restrict」路径。这不是崩溃,而是**能力退化**,见「代价与边界」。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `dsh/plugin/cordis.patch.yml` | 7 | 唯一部署配置:一条 insert、auto 路由 | :1-7 |
| `dsh/plugin/package.json` | 86 | bundle + client + bin + 精确 peer | :21-57, :75-84 |
| `dsh/plugin/bin/odai-dsh-plugin.mts` | 37 | 只保留一个「已退休」入口 | :3, :33 |
| `dsh/plugin/tests/verify-dsh-load.mjs` | 315 | 真起一个 DSH 进程、临时 `DSH_HOME`,断言 child 写与受保护控制器写都**到不了工具体** | :47-90 |
| `dsh/runtime/src/index.mts` | 357 | 组合根:证据、副作用域、压缩、prompt、scope、tool、lifecycle 依次安装 | :77-93, :140-163, :342-354 |
| `dsh/runtime/src/lifecycle-runtime.mts` | 1 623 | 路由决策、派发、回交、验收、失败回退的主循环 | :244-468, :551-793, :794-900, :1613 |
| `dsh/runtime/src/routing-context.mts` | 840 | 角色上下文包 + reviewer 证据快照 + schema 3 绑定 | :590-609 |
| `dsh/runtime/src/review-evidence.mts` | 127 | 不可变证据读取器(2 MB/500 条/64 KB/40 次) | :6-9, :21-34, :38-42 |
| `dsh/runtime/src/router.mts` | 727 | 决策表:风险、未验证因果、具体改动、紧急度、不可逆 | :66-140, :436-595 |
| `dsh/runtime/src/responsibility-scope.mts` | 366 | `pending→active` 状态机与 owner 去重 | :8, :104-122, :145-164, :315-327 |
| `dsh/runtime/src/session-evidence.mts` | 356 | JSONL 证据账本(id 去重、fsync、回滚) | :99-136, :249-279 |
| `dsh/runtime/src/semantic-memory.mts` | 1 216 | 自动候选发现、受限检索、`odai_memory` 8 个 action | :576-594, :700-800, :926 |
| `dsh/runtime/src/compaction-runtime.mts` | 257 | 拦压缩流、注入目标模型、缓冲后一次重试 | :117-140 |
| `dsh/runtime/src/compaction-pressure-runtime.mts` | 158 | 全局 `internal/listener` 钩子,替换宿主压缩监听器实现「按窗口比例」 | :25-26, :62-101 |
| `dsh/runtime/src/control-center-runtime.mts` | 313 | 4 个 loopback 端点、证据读取上限 2 000 条 | :18, :70-83 |
| `dsh/client/src/index.mts` | 1 137 | 单个中文 Web UI(React + slot 注册),不是独立页面 | :366, :1023-1073 |

**数据流(一轮真实请求)**:

```text
用户消息
  → agent/inbox/claimed: 观察并记录「认证直连输入」(lifecycle-runtime.mts:222-238)
  → agent/pre-step: 语义记忆自动捕获(仅 step 1)、按需激活工具/提示(captureAutomaticMemories)
  → agent/request: 决定 direct / inline / same-turn / child;校验 role route;写入 odai/route-decided
  → 工具调用: tools.register 的 when 先筛声明,tools.guard 再拒执行
  → 副作用: 每条治理事件 → $DSH_HOME/odai/session-evidence/<hash>.jsonl (fsync)
  → agent/turn-stopping: 回交检查、reviewer 证据门、lead-mode 复核提醒
  → Control Center: 只读同一份 JSONL,按 revision 增量拉取(control-center-runtime.mts:242)
```

**职责路由(是否多 agent/模型:是,且是它的一半体量)**。6 个可配职责 `researcher/planner/reviewer/frontend/creative/writer`;dispatch 有 `same-turn`(原地换模型)、`child`(DSH subagent)、`inline`(映射与控制器相同则不二次调用)。默认值写死在 `lifecycle-runtime.mts:91-101`:creative/writer 永远 child,researcher/reviewer child,planner 在 auto 模式 same-turn。API 子代理走 `subagents.startActivation`(带 `subagents.start` 回退,`dsh/README.md:19`);本机 CLI 走 `claude`/`codex`/`antigravity`/`grok`,只读、child-only、超时上限 7 200 秒。**包里不带任何模型映射**(`package.test.mjs:20`),没配就明确报「缺哪个职责、没有调用过任何模型」。

**压缩**:默认继承会话当前 provider/model;用户在自然语言里点名后写入 `$DSH_HOME/odai/compaction.json`(`compaction-runtime.mts:108-115`)。拦截点是 `llm/stream`,`purpose === "compaction"` 才处理;有显式目标时先 `probeModelRoute` 预检,再把目标写进请求,并把流缓冲到「合法终态」才放行,失败则丢弃残片、用未改动的原请求重试一次(`:140-200`)。另有一条**更强但更脆**的路径:`compaction-pressure-runtime.mts:62-101` 监听全局 `internal/listener`,只有当宿主监听器的 callback 恰好是 `BasicCompactionEngine`、且 `agent/pre-step` 与 `agent/request` 各注册一次时才接管(`:25-26`),否则一律 `next()` 放行。

**本地记忆**:默认 `auto`,控制器第 1 步跑一次,不调用任何 provider/model/embedding/subagent/compaction(README `dsh/plugin/README.md:40`)。只读「最近一个 open turn 的认证直连用户消息」,句子级切分后按 `durableStatement` 收候选,再逐条拒绝:问句、记忆否定、假设、临时指令、引用/转述、敏感信息、压制治理的偏好(`semantic-memory.mts:565-594`)。检索上限 1–12 条、512–16 384 字符(`:779-800`),按 token 重合 + 类别/作用域加权排序,未决冲突会把旧 active 记录**抑制**而不是替它选边。存储 `$DSH_HOME/odai/memory/store.json`:目录/文件身份在操作前后比对,拒绝符号链接,`O_EXCL|O_NOFOLLOW` 临时文件 + rename(`semantic-memory-store.mts:192-235`)。

**安全连续性**:与语义记忆**完全分开**的文件 `$DSH_HOME/odai/human-safety-continuity.json`(`human-safety-continuity-store.mts:193-196`),只允许 4 类用户自写条目,上限 80 条 / 600 字符。写入必须逐字节出现在**当轮直连用户消息**里,且拒绝凭据/联系方式(`human-safety-continuity.mts:84-93`);子代理一律拒绝(`:76-82`)。它只在当前会话独立地涉及 care/crisis/记录管理时才作为「历史偏好」注入,永不当作当前风险证据,也永不进子提示(`prompt-runtime.mts:410-423`)。

**真实验收**:reviewer 不是在 prompt 里「要求复核」,而是拿到一份带 digest 的不可变快照;读取必须带对本轮 digest,否则直接抛错(`review-evidence.mts:38`);`completeCapture` 明确区分「捕获完整」与「投递完整」。派发前还要满足「有比最后一次写更新的 diff、且最后一次写之后有成功的 test 或只读 check」(`routing-context.mts:533-609`)。只读职责结束时没有走 `odai_responsibility_return` 会被标 unverified,并在恢复后的控制器路由上自动续跑(`dsh/README.md:19`)。

## 为什么它突出

**先拆星标归属。** GitHub 星标是仓库级,而 registry 把 `orziz/odai` 的 89 记在 `dsh/plugin` 这个子目录条目上。时间线是决定性的:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-03-19 | 仓库创建,首提交 `3d4e092 Initial commit` | `git log --reverse` |
| 2026-08-14 | 首个 `dsh/` 提交 `53f9df9 feat: add DSH routing packages and isolated evaluation` | `git log --reverse -- dsh` |
| **2026-08-19** | **⚠ 89 星 / 1 951 下载采样点** | registry 边车 |
| 2026-11-11 | HEAD `8bd1289` | `git log -1` |
| 2026-11-18 | 实时 133 星(+44)、20 forks、npm `latest` 0.3.7 | GitHub API / npm registry |

采样点距首个 DSH 提交只有 **5 天**,而仓库此前已经以 Odai 技能形态跑了 5 个月。所以 **89 星里能归给 DSH 适配层的最多是 5 天的增量**,主体应记在 Odai 项目名下;`133` 是 DSH 包发布 3 个月后的仓库读数,含 DSH 影响但无法再拆分。**判断:星标是宿主项目背书,不是插件热度。**

**真正属于这个包证据的是下载:⚠ 1 951(2026-08-19)。** 它与 89 星的比例(≈22:1)说明安装量并不来自仓库关注度,而来自 npm 分发路径;npm 包 2026-08-14 建包、60 个版本、`latest` 0.3.7(2026-11-11),发布节奏是 3 个月 60 版——一个高频跟宿主版本的单一产品,而不是被社区接管的协议。注意边车 `downloads.json` **没有统计窗口字段**,所以 1 951 只能当历史锚点,不能算「周下载」或「月下载」。

**扩散为 0,且原因是结构性的**:它是整层治理,不是可复用的原语。第三方要「用它」只能装同一个包;要「仿它」得重写 1.4 万行运行时 + 12 文件治理正文,并跟住 DSH 的内部 API;没有一行配置或一个 schema 可以被单独抄走。

**机制上真正少见的点**(只用本插件自身证据):
1. 治理事件**不写进 DSH 核心 session 事件**,而是自建按 session 哈希命名的 JSONL(`session-evidence.mts:99-102`),并且卸载/升级插件后旧会话仍可读——README 的这条承诺在 `:330-352` 的分支里有实现根据。
2. **权限不来自模型映射**。`tool-runtime.mts:77-84` 把「角色策略 / 模型映射 / dispatch」拆成三个独立输入;只读权限只由 scope 的 `continuationPolicy`、child 身份、风险保护决定。`dsh/README.md:23` 把这句写成了设计原则。
3. **风险与职责选择解耦**。`router.mts:534-546`:高风险 + 未验证因果 + 具体改动 + (具体参数/紧急/不可逆)同时成立时,结论是「控制器只读、去补证据」,而不是「叫 planner」。风险词本身不产生第二次模型调用。
4. **doc-as-contract**:`package.test.mjs` 不只测 manifest,还测「patch 里不许出现映射」「bin 必须对 `--yes` 也拒绝」「Windows 上 taskkill 优先」——把部署纪律写成可执行断言。

## 代价与边界

**失败模式,按发生顺序**:

1. **`pnpm` 不在 PATH** → `dsh plugin add` 这一步就失败(README `dsh/plugin/README.md:24`)。这不是运行时降级,而是装不上。
2. **宿主版本不对**。精确 peer 是 `0.2.2-rc.1`(`package.json:75-76`),但 peer 是 optional,装在别的版本上**不会拒绝**。本机 `0.2.1-rc.5` 的 `tools.register(definition)` 只收一个参数(`dsh-tools/lib/index.js:2974`),`{ when }` 被静默忽略;条件准入退化到 `restrict`(`:2991`)与执行 guard,工具目录可能比设计更宽。DSH 自己在 `dsh/README.md:137` 也承认「宿主缺少 scoped tool restriction 时回退到完整目录」。**这是本插件最该被读者先看到的兼容风险:它只承诺一个精确版本。**
3. **装完没重启**。包在启动时载入字节,不重启则仍是旧运行时;要更新插件文件必须停 DSH(README `dsh/plugin/README.md:30,78`)。
4. **历史 v0 会话读不了**。旧版本把 `odai/*` 写进 DSH 核心日志,`0.1.5-rc.1` 起拒绝未知 v0 历史事件;`legacy-session-repair` 已退休,`--yes` 也只返回错误、不改文件(`bin/odai-dsh-plugin.mts:3,33`;README `:52`)。没有迁移,只有「别删备份」。
5. **窗口比例压缩静默失效**。`compaction-pressure-runtime.mts:25-26` 要求宿主监听器形状完全匹配(callback 是 `BasicCompactionEngine`,且两个事件各注册一次);不匹配就 `next()` 走宿主默认。UI 会把该模式标成不支持,但**不会报错**,用户只会发现「没按 80% 触发」。
6. **存储坏了只关功能,不修数据**。记忆 store 无效或是符号链接时,捕获与召回都停,只有「精确的全局清空授权」能物理重置(`semantic-memory.mts:1019-1028`;store `:192-201`);证据文件出现半行时,非严格读取会**跳过坏行并 warn**(`session-evidence.mts:193-196`),严格路径(追加时)直接抛。
7. **本地 CLI 路由的边界不在 DSH**。CLI 必须自行安装并登录;权限由 CLI 自己执行,不继承 DSH 的工具审批;Antigravity 的 prompt 是 argv 值,本机进程可见;Grok 实现是「按官方文档,未实测」(`dsh/README.md` 本地 CLI 表)。超时/取消会 SIGTERM→SIGKILL,Windows 只杀直接子进程。
8. **同步 I/O 在事件路径上**。每条治理事件一次 `fsync`(`session-evidence.mts:266`),量级不大但会摊到每一步;长会话、多子代理时是真实的延迟成本。

**权限与数据**:所有状态在 `$DSH_HOME/odai/` 下(mode `0700` 目录 / `0600` 文件):`routing.json`、`source.json`、`output.json`、`compaction.json`、`memory/store.json`、`human-safety-continuity.json`、`session-evidence/`。记忆与安全连续性**不发起隐藏模型调用**;但 DSH 会话历史本身仍含聊天原文,作者明确写了「这不是 DLP,别把凭据放进聊天指望过滤」(README `:44`)。本地 CLI 子进程**继承 DSH 进程环境**(含凭据与代理变量),这是它最实的一条数据边界。

**维护成本**:77 个 `dsh/plugin` 提交、60 个 npm 版本、341 个运行时测试、8 个 prompt section、13 个工具、11 个事件挂点、1 个 1 137 行客户端;任何宿主 `tools`/`systemPrompt`/compaction 内部形状变化都要跟。作者用 `compatibility.json` 21 条矩阵 + `release-contracts.json` 的 320 包摘要来管这件事——这既是纪律,也说明跟版是主要工作量。

## 可信度与复现

**★★★(限 DSH 适配层与治理运行时)**:`dsh/plugin/` 15 个文件全部登记,通读 manifest/patch/bin/README/`package.test.mjs`,并读 `verify-dsh-load.mjs`、`live-routing-smoke.mjs` 的探针骨架;`dsh/runtime/src` 逐文件读完了组合根、证据账本、scope 状态机、治理 guard、工具注册/guard、`work-policy`、`review-evidence` 全文,其余按关键段读(约 20 个文件);另读 `skills/odai/SKILL.md`、`manifest.json`、`dsh/README.md`、`dsh/compatibility.json`、`dsh/release-contracts.json`、`docs/evaluation-results.md` 证据边界段;并对照本机安装的 DSH `0.2.1-rc.5`(`dsh-tools` 的 `register`/`restrict`/`guard`)核对注册契约。

```sh
# 1) 克隆与提交(仓库 35 MB,blob 过滤足够)
git clone --filter=blob:none https://github.com/orziz/odai.git /tmp/an-odai
cd /tmp/an-odai && git log -1 --format='%H %ad %s'
# → 8bd1289197b4b3c01a50c9e80d2fd355214abf7c 2026-11-11

# 2) 归属时间线(浅克隆需先 unshallow;378 个提交)
git fetch --unshallow --filter=blob:none
git log --reverse --format='%h %ad %s' --date=short | head -1        # 3d4e092 2026-03-19
git log --reverse --format='%h %ad %s' --date=short -- dsh | head -1 # 53f9df9 2026-08-14

# 3) 代码规模
find dsh/plugin -type f | xargs wc -l | tail -1          # 2042
find dsh/runtime/src -name '*.mts' | xargs wc -l | tail -1 # 13942
find dsh/runtime/tests -type f | xargs wc -l | tail -1     # 15392
ls dsh/runtime/tests/*.test.mjs | wc -l                    # 38
grep -h '^test(' dsh/runtime/tests/*.test.mjs | wc -l      # 341

# 4) 扩散(在 awesome-dsh-plugin 仓库根;11 744 个 yml 必须用目录形式,否则参数过长)
grep -ril 'odai' data/plugins/ | wc -l      # → 1
grep -ril 'odai' data/plugins/              # → data/plugins/orziz__odai--dsh-plugin.yml
grep -ril 'orziz' data/plugins/ | wc -l     # → 1

# 5) 宿主契约核对(本机 DSH 0.2.1-rc.5,而插件 pin 0.2.2-rc.1)
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh
grep -n 'register(definition)' $DSH/node_modules/@deepseek-ai/dsh-tools/lib/index.js  # :2974(单参数)
grep -n 'restrict(filter)' $DSH/node_modules/@deepseek-ai/dsh-tools/lib/index.js      # :2991
```

**未读**:`skills/odai/references/*.md` 8 份全文(只读了 `SKILL.md` 的引用关系)、`skills/odai-orchestration` 的编译器、`dsh/agent/`(18 文件)、`dsh/runtime/src` 里 `routing-config.mts`(673 行)与 `output-config.mts`(425 行)的正文、`dsh/client/src/index.mts` 的 UI 渲染细节、`scripts/` 的评测/打包脚本、`docs/evaluation-results.md` 的 22 项模型记录(只读了证据边界段)。因此**不对治理正文质量、UI 易用性、模型评测分数下判断**。

## 待验证

1. **在 0.2.1-rc.5 上实际加载**:本机未跑 `dsh plugin add`(会写 profile)。需要隔离 `DSH_HOME` + 临时 profile 实测:13 个工具是否全部出现、`when` 被忽略后 `restrict` 是否等价、`systemPrompt.section` 的 8 个槽是否都生效。
2. **89 → 133 的增量归属**:需要 star-history 或 `stargazers?starred_at`;未授权读数不可得,本卡未量化 DSH 包对仓库总星标的贡献。
3. **1 951 下载的统计窗口**:边车 `downloads.json` 只有 `checkedAt`,没有 `start/end`;要判断「周下载/月下载」必须回到上游 `probe-downloads.mjs` 的请求参数。
4. **窗口比例压缩在真实 DSH 上的接管率**:`exact()` 依赖 `fiber.uid`、`runtime.callback`、`events` 计数三件事,任何宿主小版本改动都可能让它静默退化为宿主默认;需要在 0.2.2-rc.1 上跑 `tests/verify-compaction-pressure.mjs` 并观察 Control Center 的 supported 标志。
5. **记忆准入的误杀/漏杀**:敏感匹配器是正则(`containsSensitiveMemory`),中文口语、代码片段、带引号的转述都靠 `sentenceSegments` 的遮罩处理;没有真实语料测试,只有单测。实际误存率未知。
6. **Control Center 的 loopback 边界**:`rpc.handle(..., { authority: "loopback" })` 与 `connection.fetch.register("/api/...")` 两条路径在同一 Web profile 下的鉴权差异未实测;若走 fetch 路径,是否仍只有本机可写需要确认。
7. **本地 CLI 的模型证据**:作者自述 Grok 未实测、Codex/Antigravity 只有本机探测;`route-unverified` 的判定对不同 CLI 输出格式的稳健性未验证。
