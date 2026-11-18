# misakanet — 语料与检索都在服务端，DSH 拿到的是「一行 MCP 行 + 3005 行网页半身」

> 证据等级:★★★(源码级;`Ikalus1988/MisakaNet@fc7cd41bce9d4c54ee471aa38bfaf30de5f582da`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 407 为 2026-08-19 历史采样;下载边车**无记录**(采样缺口)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `Ikalus1988/MisakaNet`([registry](../../../data/plugins/Ikalus1988__MisakaNet.yml)) |
| 类目 | memory(504 条;[census](../../ecosystem/census.py) 全表 11 744) |
| 子分类 | `host-backed`(外部记忆系统适配)——默认 npm 安装走公网端点;只有 clone/git+ 安装才退化为可离线的 `local-store` 形态(见下) |
| 自述 | 「失败恢复记忆库:从真实工程会话中搜索和记录失败恢复教训,BM25 + 语义 RAG 检索」 |
| 星标 ⚠ | **407**(2026-08-19 冻结采样);2026-11-18 实时 **564**(GitHub API,编排者当日查得) |
| 下载 ⚠ | **边车无记录**(`data/downloads.json` 624 条里无此 URL,属采样缺口,不是零下载)。自查 npm(2026-11-18):`misakanet` 近一月 **10 349** 次(区间 2026-10-18~11-16),61 个版本,首版 2026-09-01 |
| 扩散 | **0**(口径见末节:`grep -ril 'misakanet' data/plugins/` 命中 1 条,即自身) |
| 仓库 commit | `fc7cd41`(2026-11-18,`main`,`feat(mcp): the endpoint tells a Cindy caller whether its build is behind (#5185) (#5201)`);仓库建于 2026-04-29,3 833 个 tracked 文件,工作树 93 MB |
| 包形态 | npm `misakanet@3.19.0` —— **双面包**:`dsh.bundle.patch`(一行 MCP 行)+ `dsh.client`(网页 GUI);同仓还带 Codex/Claude/Cindy 插件清单、SKILL.md、以及托管端点本身的 Cloudflare Worker |
| 代码规模 | DSH 侧 **3 312 行**(`index.js` 205 + `lib/client.js` 3 005 + `cordis.patch.yml` 62 + `index.d.ts` 40);DSH 测试 **4 873 行**(8 个 `tests/test_dsh_*.py` 3 595 + 面板 harness 708 + 浏览器 e2e 570);全仓 Python 719 文件 / **176 821 行**(不含 `tests/` 为 79 678),`workers/` JS 40 316 行 |

## 它到底是什么

不是"一个 DSH 插件",而是**一套失败经验知识库的三个可分离部件**:① 语料(`lessons/` 下 1 057 个 markdown 文件,公开索引 1 014 条)、② 检索(两套互不共享代码的实现:本地 Python 引擎 + 托管 Worker)、③ 13 个宿主各自的薄适配(DSH 是第 12 个,`packages/misakanet-setup/bin/misakanet-setup.mjs:133-137`)。DSH 只吃到 ③ 里的一小块。

**数据模型:lesson = markdown + YAML frontmatter,触发条件是独立字段。** 必填 `title` / `domain` / `tags` / `status` / `evidence_level`(`lessons/TEMPLATE.md:6-12`,`scripts/lesson_gate.py:40-46`);新 lesson 另加三个"可被检索/可被复述"的字段(`lessons/TEMPLATE.md:13-15`,`scripts/lesson_gate.py:577-627`):

- `trigger` ≤160 字符,**错误原文里最独特的片段**,不是整句问句 —— 这是"从会话里抽取失败条件"的落点。模板用它反例说明:写"我的构建为什么一直失败"检索不到任何东西(`lessons/TEMPLATE.md:92-101`)。实际覆盖 988/1 057 个文件。
- `summary_plain` ≤120 字符,一句可原样复述给非工程师的话;`verify` ≤200 字符,可执行/可观察的通过判据(`lessons/TEMPLATE.md:76-80`)。
- 正文固定四段 `Problem → Root Cause → Solution → Verification`(`lessons/TEMPLATE.md:20-41`;`scripts/lesson_gate.py:495-529` 会拒绝空段)。

覆盖实测(`grep -rl` 于 `lessons/**/*.md`,1 057 个文件):`status` 978 个、`evidence_level` 704 个、`trigger` 988 个、`supersedes` 3 个。

**评分不是"分数",是可晋升的证据阶梯。** `E0` 自述(默认) / `E1` 维护者复核 / `E2` 本地复现 / `E3` CI 或沙箱验证 / `E4` **观测到的复用**,权重 0 / 0.25 / 0.5 / 0.75 / 1.0(`misakanet/evidence.py:29-37`),合成 `trust = quality × (0.7 + 0.3 × weight)`(`misakanet/evidence.py:99-110`)。E4 的定义是硬的:托管端 `search_signals` 里 `COUNT(DISTINCT client_hint) ≥ 2`,**票数与课程自述只能算 E3 提示**(`misakanet/evidence.py:1-20`)。全语料 `evidence_level: E4` 命中 **0 条** —— 不是缺失,是设计上不允许声明。

**去重三层,全部是 CI 门禁而不是运行时。** ① 标题精确重复(`scripts/lesson_gate.py:754`,`validate_file` 在 `:1169` 调用);② 一条 intake 只能对应一篇 lesson,`provenance.issue` 唯一(`scripts/lesson_gate.py:823`,`:1183-1200`);③ 正文近似重复:词级 Jaccard 与"章节骨架 LCS"取最大值,阈值 0.55(`scripts/lesson_gate.py:864-980`,`:1202-1208` 以 warn 形式报告)。另有一条 `detect_fake_verification()`(`:991`),拦"`grep … | wc -l` 假装验证"的占位写法。

**生命周期:6 个状态,实际只用 3 个,且"过期"只降权不删除。** 词表 `{published, draft, archived, active, stale, superseded}`(`scripts/lesson_gate.py:40`);带 `status` 的 977 个 lesson 文件里:published 936 / draft 38 / superseded 3(第 978 个命中是模板文件里的注释行)。`superseded` 在本地引擎里默认**被过滤**(`misakanet/search/engine.py:602-606`),在托管端是**稳定分区降级而非过滤**——被取代的条目仍会在"唯一命中"时返回,因为更正信息随正文一起带出(`workers/register-proxy-sw.js:1169-1184`)。另有一套 freshness 衰减模型(14 天保护期、每天 1 分、5 档,`misakanet/freshness.py:20-43`),但它**只用于展示**:CLI 打在结果里(`search_knowledge.py:86-88`),托管端由 `updated` 日期算一个标签挂在结果上(`workers/register-proxy-sw.js:727`、`:900`),**不参与排序**;脚本与 workflow 里也找不到把 `status` 自动改成 `stale` 的路径(`stale_lesson` 只是 intake 的一种类型,`scripts/intake_pipeline.py:56`、`:205-206`,处置靠人)。

**会话捕获:没有转录解析器。** 抽取由 agent 自己完成,代码只给两样东西:一段注入到 `AGENTS.md` 的规则块(6 条,含"20 轮后提交可泛化片段"与脱敏要求,`packages/misakanet-setup/bin/misakanet-setup.mjs:1532-1542`),以及唯一的自动通道——进程崩溃的 tombstone JSON 转 draft lesson(`scripts/tombstone_to_draft.py`,`misakanet/tombstone.py:1-20` 定义了 `reason`/`timestamp`/`pid` 的最小契约)。

## 怎么接进 DSH

**① manifest 是"双面"的,两半分别被 DSH 的不同子系统读。** `package.json:18-21` 的 `dsh.bundle.patch` 指向 `./cordis.patch.yml`;`package.json:22-30` 另有 `dsh.client`:`platform: web` + 4 个 `inject`(`dsh-client-ui-chat` / `-conversation` / `-sidebar-right` / `-tool`)。后者由 DSH 的 `dsh-client-modules` 消费——它扫 Loader 条目里声明了 `dsh.client` 的包并组合前端模块(`$DSH/node_modules/@deepseek-ai/dsh-client-modules/lib/index.js:40-71`、`:105-106`)。此外还有 `dsh.compatibility.dshReleases`(`package.json:31-37`,声明 3 个兼容版本)与两个 **optional peer**(`package.json:60-71`)。

**② patch 只有一行,而且刻意不写 `@deepseek-ai/*`。** `cordis.patch.yml:52-62`:一个 `insert`,`id: misakanet-mcp`,`name: misakanet`(它自己的包),config 为 `transport: streamable-http` + `url: https://misakanet.org/mcp` + `headers.Origin` + `toolCallTimeoutMs: 60000` + `failOnStartupError: false`。注释里记了原因(`:1-30`):DSH STORE 的预检是**对整份 patch 文本跑正则**(连注释都算),只要出现"insert 行声明 `@deepseek-ai/*` 组件"就判 `SUBMISSION_PATCH_PROTECTED`,评级 `route: blocked`。于是真正的挂载搬进了 JS。

**③ `apply()` 做的事就是动态 import 官方客户端并作为子插件挂上**——`index.js:75-135`:`await import('@deepseek-ai/dsh-mcp-client')`(`:107`)→ `ctx.loader.unwrapExports`(`:129`)→ `ctx.plugin(component, options)`(`:130`)。三条失败路径**都不许抛出**(`:78-92` 的注释写明理由:activation 抛错会让整个 `dsh web` 起不来),分别降级为 warn(`:94-102` 无 `ctx.plugin`、`:104-126` 客户端不可解析、`:131-134` 其余异常);`failOnStartupError` 只透传给 MCP 客户端。`Config` 用 schemastery 生成,且用一个 **try 包裹的 top-level await** 加载,加载不到就 `Config = undefined`,只丢表单不丢行(`index.js:158-205`)。

**④ 网页半身是主要工程量:3 005 行,注册 6 个 slot + 1 个斜杠命令。** `lib/client.js:2843-2900` 逐一 `ctx.slots.inject` 后注册:`sidebar.panellist`(左栏图标)、`main`(主页面)、`conversation.chat.assistant-actions`、`tool.call.toolview`(**键是 wire 工具名**,`:97-99` 同时接受 `mcp__misakanet__misakanet_search` 与 `mcp__misakanet__search` 两种拼法)、`shell.overlay`(全帧 toast)、`sidebar.footer.action`(复制本会话统计);`/misakanet` 命令走 `ctx.inject(["locale"])` + 草稿服务(`:2866-2878`)。所有注册都等 slot 声明后再注册(`registerWhenDeclared`,`:2814-2822`)——注释记了 2026-10-01 因为子 slot 未声明而整插件炸掉的事故(`:2802-2812`)。

**⑤ 没有事件钩子。** `grep -n 'ctx.on(' index.js lib/client.js` 无 `agent/*` 命中:它不订阅 `agent/pre-step`、不读会话事件、不写回任何东西。所谓"规则半身"由一个**独立 npm 包**实现:`npx @misaka-net/misakanet-setup --only dsh` 把规则块写进 `$DSH_HOME/AGENTS.md`(`packages/misakanet-setup/bin/misakanet-setup.mjs:2429-2437`),因为"工具在插件包里,安装器不写这个文件"。

**⑥ 默认工具面是托管的 8 个,不是本地的 11 个。** 这一点最容易误判:托管端点只服务 `search` / `get_lesson` / `submit_intake` / `me_inbox` / `write_lesson` / `preflight` / `register` / `me_events` 8 个;本地 stdio(`python -m misakanet.server`)另有 `submit_usage` / `usage_status` / `memory_context` 3 个(`CLAUDE.md:33-35`;`tests/test_mcp_tool_count_ssot.py` 把两个面的数量钉成 SSOT,`docs/mcp.md` 逐工具对照)。于是"任务开始前主动注入失败记忆"的 `misakanet_memory_context`(`misakanet/server/handlers/memory_context.py:7-84`)在**默认 DSH 安装里根本不存在**。

安装两步,缺一不可:`dsh plugin --profile web add misakanet`(工具)+ `npx @misaka-net/misakanet-setup --only dsh`(规则)。`docs/dsh-installation.md:8-12` 自己写明这个分裂。

## 关键实现

DSH 侧文件:

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `cordis.patch.yml` | 62 | 唯一的 profile 层声明:1 行 insert,30 行历史注释 | `:52-62` |
| `index.js` | 205 | `apply()` 动态挂官方 MCP 客户端;`DEFAULT_MCP_CONFIG`;schemastery `Config` | `:54-61`、`:75-135`、`:158-205` |
| `lib/client.js` | 3 005 | 网页半身:面板/工具行/toast/命令/i18n/本地计数 | `:91`、`:97-99`、`:1279-1340`、`:2843-2900` |
| `package.json` | 97 | 双面 manifest + optional peer + `files` 白名单 | `:7-17`、`:18-37`、`:60-71` |
| `tests/test_dsh_bundle.py` | 363 | bundle 契约(见下) | `:45-105`、`:181-221` |
| `tests/test_dsh_plugin_surface.py` | 1 419 | 宿主**运行前**就会读的字段:icon 契约、兼容列表、npm keywords | 文件头 `:1-40` |
| `tests/test_dsh_plugin_manifest.py` | 233 | 可发现性(`repository` 字段缺失导致插件 hub 解析到错误的包,#1677) | `:1-40` |
| `tests/test_dsh_plugin_panel_render.py` | 799 | 面板渲染 + `tests/dsh_panel_render_harness.cjs` | — |
| `.github/workflows/dsh-client-e2e.yml` | — | 真浏览器 e2e:一次性 `DSH_HOME`、固定 `DSH_VERSION 0.2.0-rc.2`、3 个场景 | `:7-9`、`:50` |

**检索实现(托管,DSH 实际走到的那条)**:BM25 索引是**一个 KV/D1 单行 JSON**,key `worker_search_index`,形状 `{version, built_at, docCount, avgDocLen, k1, b, terms:{t:{df,idf,docs:[{doc,tf,len}]}}, docs:[…]}`(`workers/register-proxy-sw.js:1885-1892`);`k1 = 1.5`、`b = 0.5`(`:2212-2213`,与离线脚本 `scripts/build_worker_index.py:24-26` 的注释互相对齐);重建**最多每 20 小时一次**,TTL 30 天(`:1971-1972`),不是增量——过期就整块重建,再把结果写回同一行(带 `worker_search_index_health` 记录失败原因,`:1899`)。硬上限是 D1 单行 2 MB,注释记了实测 1.63 MB / 463 篇的占用(`:1901-1910`)。

语义那一路**不是并行融合,是级联**:

```
query ──别名展开(scoringQueryFor, :4679)──▶ BM25 索引 (:4694)
                                              │
              ┌─── 有结果 ──▶ 直接返回;仅当 query 含 CJK 才额外融合
              │                 vectorHits(floor 0.45) ──rrfFuse(k=60)──▶ (:4737-4760)
              └─── 空结果 ──▶ Workers AI bge-m3 嵌入 + Vectorize 查询(floor 0.62)(:4718-4736)
```

embedding 来自 **Cloudflare Workers AI**,默认 `@cf/baai/bge-m3`(`:2132`),向量索引用 Vectorize,索引名 `misakanet-lessons-m3`(`workers/wrangler.toml:135`),语义阈值默认 `0.62`(`workers/wrangler.toml:51`,`:2164`)。融合用 RRF 而不是分数加权,理由写在 `:2100-2106`:BM25 无界、余弦有界,加权得按语言调参。任何一个向量失败都被吞掉,只留 `debugLog`(`:4722-4735`)。

**检索实现(本地,clone/git+ 安装才可用)**:BM25 核心**不在本仓**,来自 PyPI 包 `misakanet-core>=2.7.0`(`misakanet/search/engine.py:15`、`requirements.txt:1-3`);本仓写的是加权层:

```
score = bm25_w × norm(bm25) + meta_w × 元数据加分 + base_w × 0.1 + boost
        + 可选 cross-encoder 重排(0.70/0.30)
```
(`misakanet/search/engine.py:588-637`;元数据加分 = domain 命中 0.25 / 标题精确 0.8 / 状态权重,`:24-29`、`:437-452`;boost = core +0.15 / verified +0.10 / 近 30 天 +0.05 / draft −0.20,`:41-45`、`:500-517`)。可选 `--semantic` 用 `BAAI/bge-base-zh-v1.5`(`misakanet/search/embeddings.py:14`),**fail-closed**:模型装不上就抛 `RuntimeError`,除非显式打开仅开发用的 SHA256 伪向量(`misakanet/search/embeddings.py:32-86`)。但 `_vector_similarity()` 只被 `--explain` 的 `_score_breakdown` 调用,**不在排序路径上**,而且每次现算 query 与 doc 两段嵌入、无向量索引(`misakanet/search/engine.py:980-991`、`:1001`)。

**索引存哪**:托管侧=KV/D1 的单行 JSON(上面);本地侧**没有持久倒排索引**,只有 ① `.cache/search_cache.db` 的 SQLite `file_cache`(path/mtime/size + 元数据,增量靠 `stat()` 比对,`misakanet/search/engine.py:101-124`)② 进程内 L1 查询缓存 50 条(`:60-61`、`:345-365`)③ 可选语料 TTL(`set_docs_cache_ttl`,默认 0,`misakanet/search/engine.py:77-92`)。

**语料如何进入检索**:`data/lessons.json`(1 014 条,3.5 MB)由 `scripts/update_lessons_json.py` 从 `lessons/` 逐文件生成(`:1-12`),`scripts/build_worker_index.py` 再把 JSON 编成倒排索引;两份产物都由每日 workflow 重生成,并且生成器**同时写** `data/lessons.json` 与 `docs/data/lessons.json`(浏览器那份),因为 2026-09-29 实测过两份差 8 条、一天无人发现(`scripts/update_lessons_json.py:36-45`)。

**测试证明了什么契约。** DSH 侧测试多于适配代码(4 873 vs 3 312 行),且钉的都是"宿主会不会因此炸":

- `tests/test_dsh_bundle.py:45-105`:patch 必须被 `files` 白名单装载、只能有一个 insert 行、config 必须是 streamable-http + 那个 URL + `failOnStartupError:false`、且**与 `index.js` 的 `DEFAULT_MCP_CONFIG` 逐字段相等**(用 `node -e import()` 实测,`:96-105`)。
- 同文件 `:181-221` 用子进程真跑 `apply()`:没有 `ctx.plugin` 时**必须 RETURNED 不能 THREW**;客户端不可解析时**必须 warn**(注释记了这条曾是唯一静默分支,#2759 的"侧栏只是装饰")。
- `tests/test_dsh_plugin_surface.py:1-40`:icon 契约(绝对路径/超大文件/非法扩展会让插件**加载失败**,不是外观问题)、兼容声明与文档同源、peer 范围与声明版本不矛盾。
- e2e(`.github/workflows/dsh-client-e2e.yml:7-9`、`:18-22`、`:50`)在一次性 `DSH_HOME` 里装本仓、开真浏览器验证三个 DOM 行为;并明说不加 `paths:` 过滤,否则被跳过的 PR 会永远卡在 "Expected"。

## 为什么它突出

**先拆星标归属:407 与 564 都不属于 DSH 适配层。** 时间线是决定性的:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-04-29 | 仓库创建 | GitHub API `created_at` |
| 2026-08-15 | **第一个 DSH 提交** `feat: add dsh plugin packaging …(#1055)` | `cordis.patch.yml` 路径历史 |
| **2026-08-19** | **407 星采样点** | ⚠ 边车 |
| 2026-09-03 / 09-05 / 09-12 / 09-15 | DSH 行四次重写:删 bundle → 恢复 → 避开 STORE 保留字 → 改指公网端点 | 同路径历史(共 5 个提交) |
| 2026-11-18 | 564 星(实时)、npm 近一月 10 349 次 | GitHub API / npm API |

采样时 DSH 支持只有 **4 天**,而仓库已经跑了 3 个半月;13 个宿主里 DSH 排第 12(`packages/misakanet-setup/bin/misakanet-setup.mjs:133-137`)。564 相对 407 是 +157(3 个月 +38.6%)。所以这两个数字属于"一个多宿主失败知识库",不属于这层 DSH 适配。

**再解释"高星标、零扩散"——四条,按解释力排序:**

1. **能力不需要这个包。** DSH 的 `dsh-mcp-client` 原生支持 `streamable-http` + `url` + `headers`(`$DSH/node_modules/@deepseek-ai/dsh-mcp-client/lib/index.js:39-46`),一行 profile 配置就能接同一个端点。本包的价值是"少写一行配置 + 一个面板",**任何人复制它得到的只是一行指向 `misakanet.org` 的 config**,不构成新条目。
2. **可抄的不是代码,是语料。** 3 312 行 DSH 代码里没有可复用的算法:检索在 Worker(11 741 行)与 PyPI 包 `misakanet-core` 里,语料是 1 057 个经 CI 门禁的人工 markdown。照抄适配层等于照抄一次 `insert`。
3. **衍生被贡献模型吸收。** 234 个 fork、563 个 open issue、DCO 签核、`intake → issue → lesson` 的闭环:想改进的人变成 PR 作者,而不是另立一个插件仓库。这条不是推测——`AGENTS.md` §6 把"每个提交都要 `Signed-off-by`"写成硬门禁。
4. **它自己也不在 DSH 生态里社交。** 0 条第三方提及意味着没有任何条目把它当依赖或参照;README 只回链插件目录徽章(`README.md:54-56`),没有反向引用。

**判断:明星,不是锚。** 声量高(564 实时 + 月下载一万)、扩散为零;而且这份声量归主项目(跨 13 宿主的知识库),不归 DSH 适配层。它在 DSH 侧的位置更接近"外来产品的官方接入点":接入面做得足(icon 契约、兼容矩阵、真浏览器 e2e、DSH STORE 合规四项都能在源码里指到),但**再足也只有一行 MCP 行加一个面板是 DSH 独有的**。

## 代价与边界

- **默认外发,和"本地存储"相反。** patch 里写死 `https://misakanet.org/mcp`(`cordis.patch.yml:58`);`package.json:7-17` 的 `files` 白名单**不含 `scripts/`**,所以 npm 安装根本没有本地 Python 服务——补丁注释里"可以覆盖成 stdio"的说法(`:43-45`)只对 git/clone 安装成立。要真正"断网可用",必须 clone 后把行改成 `command: python3, args: [scripts/mcp_server.py]` 并自备 Python 3.11+ 与 `misakanet-core`。
- **查询会留存。** 每次搜索在 D1 写一行 `search_signals`:query **前 80 字符** + 加盐去重键 + `client_hint` / agent / version / os / 延迟(`workers/register-proxy-sw.js:8253-8290`)。设计上明确"不留完整 prompt、不建账号"(`:8265-8272`),但**对使用者而言就是"你搜什么会被记下来"**。DSH 侧没有任何本地脱敏:12 类正则脱敏(`workers/lib/redact-patterns.json`,含私钥/GitHub token/绝对路径/邮箱)只跑在 Claude/Codex 的 checkpoint hook 里(`integrations/agent-autostart/checkpoint_reminder.mjs:228-262`),DSH 路径没有对应钩子。
- **失败模式,按发生顺序**:
  1. `@deepseek-ai/dsh-mcp-client` 解析不到 → `apply()` 只 warn 并返回,但**网页面板照常渲染**(`index.js:104-126` 的注释自承 `lib/client.js` 无论成败都挂浏览器半身)。可观察结果是"侧栏是装饰品、agent 一个工具也没有"(#2759),这条直到 2026-10-08 才从静默改成 warn。
  2. 端点不可达 → 60 s 工具超时 + 断连行,`failOnStartupError:false` 保证 profile 仍能启动(`cordis.patch.yml:61-62`);代价是用户在工具列表消失前看不出问题。
  3. patch 里写了 protected 命名空间 → DSH STORE 预检直接 `route: blocked`,且**正则扫注释**,连引用那行文本都会中招(`cordis.patch.yml:9-23`)。
  4. 插件 hub 解析到错误的包 → 报 `entry file missing: index.js`,实际原因是 `repository` 字段缺失(#1677,`tests/test_dsh_plugin_manifest.py:1-30` 是它的回归测试)。
  5. 旧版 patch 曾让同一个 insert 生效两次 → Cordis 报 `duplicate loader entry id`,级联到 `plugin tree failed to load`(`index.js:15-20`)。
- **文档与 DSH 现实不符一处**:`docs/dsh-installation.md:8-10` 与 `README.md:279` 都说"dsh 没有 prompt 注入扩展点"。本机 DSH 有 `agent/pre-step` waterfall(`$DSH/node_modules/@deepseek-ai/dsh-agent-loop/lib/index.js:909` 派发,`$DSH/node_modules/@deepseek-ai/dsh-agent-instructions/lib/index.js:1406` 消费),代码级注入可行;**判断:这是本包选择不做的实现(它的 `apply()` 不注册任何事件),不是宿主缺少能力**。
- **维护成本不对称。** DSH 适配层 3 312 行要跟着 DSH 的 slot/manifest 语义走(4 次 patch 重写、1 次 slot 未声明事故、1 次 hub 解析失败),而全仓 Python 176 821 行才是主体;对评估者来说,采用它等于依赖一个 13 宿主项目的发布节奏。
- **测试成本高**:DSH e2e 要装固定版本 DSH + Chromium,CI 里 35 分钟超时,且作者自己注明"还没进 required checks"(`.github/workflows/dsh-client-e2e.yml:18-22`)。

## 可信度与复现

★★★(仅限本卡的 DSH 侧与检索路径):`cordis.patch.yml`、`package.json`、`index.js`、`lib/client.js`(注册段、面板/toast/POST 段)、8 个 `tests/test_dsh_*.py` 的头部与关键断言、`misakanet/search/engine.py`(缓存/BM25/加权/重排/向量段)、`misakanet/search/embeddings.py` 全文、`misakanet/evidence.py` 全文、`scripts/lesson_gate.py`(词表/去重/近似重复)、`misakanet/freshness.py`(参数段)、`misakanet/server/handlers/memory_context.py`、`workers/register-proxy-sw.js`(索引常量、RRF、语义兜底、CJK 融合、`search_signals`)、`scripts/update_lessons_json.py` 与 `scripts/build_worker_index.py` 头部、`packages/misakanet-setup/bin/misakanet-setup.mjs`(宿主表/规则块/`installDsh`)、`docs/dsh-installation.md`。

```sh
git clone --depth 1 --filter=blob:none https://github.com/Ikalus1988/MisakaNet.git /tmp/an-misakanet
cd /tmp/an-misakanet && git log -1 --format='%H %ad %s'
# → fc7cd41bce9d4c54ee471aa38bfaf30de5f582da 2026-11-18 ...

# DSH 面行数
wc -l index.js index.d.ts lib/client.js cordis.patch.yml        # 205 40 3005 62

# 全仓规模
git ls-files '*.py' | tr '\n' '\0' | xargs -0 wc -l | tail -1    # 176821(719 文件)
git ls-files '*.py' | grep -v '^tests/' | tr '\n' '\0' | xargs -0 wc -l | tail -1   # 79678
git ls-files 'workers/*.js' 'workers/**/*.js' 'workers/*.mjs' | tr '\n' '\0' | xargs -0 wc -l | tail -1   # 40316

# 扩散(在 awesome-dsh-plugin 根;data/plugins 有 11744 个文件,必须用目录形式)
grep -ril 'misakanet' data/plugins/ | wc -l      # → 1,即 data/plugins/Ikalus1988__MisakaNet.yml
grep -ril 'misaka' data/plugins/ | wc -l         # → 2;第二条是 misakalemon/dsh-session-backup 的**作者名**,非提及

# 语料与字段覆盖
find lessons -name '*.md' | wc -l                # 1057
grep -rh '^status:' lessons/ --include=*.md | sort | uniq -c      # published 936 / draft 38 / superseded 3(+1 模板注释行)
grep -rh 'evidence_level:' lessons/ --include=*.md | grep -c E4    # 0

# 宿主数量与 DSH 的位置
grep -n "const AGENTS" -A 4 packages/misakanet-setup/bin/misakanet-setup.mjs   # 13 个目标
```

**未读**:`workers/register-proxy-sw.js` 11 741 行里只读了索引/融合/信号/路由段;`misakanet/` 其余模块(guard/watcher/profile/remote)未读;`scripts/` 62 657 行只读了 lesson_gate、update_lessons_json、build_worker_index、tombstone_to_draft 的头部;其余 11 个宿主的适配未读;Vectorize 索引内容与 `misakanet-core`(独立 PyPI 包)的 BM25 实现完全未读。凡涉及"检索准不准"的判断都只基于结构与阈值,不基于效果。

## 待验证

1. **564 星里有多少能归 DSH**:需要 stargazers 的 `starred_at` 曲线(未授权 API 返回 401);现在只能靠"DSH 首个提交在采样前 4 天"这条时间线推断。
2. **npm 10 349 次/月里 DSH profile 安装占几成**:npm 不区分宿主;可用 `dsh plugin add` 的下载日志(无公开接口)——目前只能报总量。
3. **线上端点是否等于本 commit**:`/api/health` 会回部署 commit,未查;若线上落后,本卡描述的检索行为只是 `main` 的行为。
4. **`misakanet-core` 的 BM25 实现**:本地检索的 idf/分词/停用词都在那个 PyPI 包里,本仓只调用;不读它就无法判断本地与托管的排序差异。
5. **npm 安装下 stdio override 是否真的走不通**:`files` 白名单不含 `scripts/`,`test_local_stdlib_server_still_ships_for_profiles_that_prefer_it`(`tests/test_dsh_bundle.py:82-84`)只断言**仓库里**存在、不断言**包里**存在;需要 `npm pack` 后核对,或实跑一次 override。
6. **`memory_context` 缺席的实际影响**:DSH 默认 8 工具里没有它;agent 是否因此从不做"开工前的主动召回",需要读会话日志才能确认(本仓有 `search_signals`,但那是搜索侧)。
7. **e2e 未复跑**:`.github/workflows/dsh-client-e2e.yml` 需固定 DSH 0.2.0-rc.2 + Chromium,本次未执行;面板行为(6 个 slot)只从源码与测试断言读到。
