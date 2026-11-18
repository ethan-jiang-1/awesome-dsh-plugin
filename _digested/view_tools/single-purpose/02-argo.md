# argo-dsh — 约 20 万行 Python 搜索基础设施的 4 千行 DSH 客户端,默认只露 2 个原生工具

> 证据等级:★★★(源码级;`taxueseek/argo@c7cd8599dbca3f642e94ca3f97726c9c23e79195`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 101 为 2026-08-19 历史采样;2026-11-18 实时 271,两者均为主项目仓库级。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `taxueseek/argo#dsh-plugin`([registry](../../../data/plugins/taxueseek__argo--packages-dsh-plugin.yml)) |
| 类目 | [tools](../../ecosystem/census.py)(1,639 条;全表 11,744) |
| 子分类 | `single-purpose`(单点工具;本册成员表给它的注是"工具集成") |
| 自述 | 「统一搜索与证据核验:120+ 引擎多语言路由,垂直域与结构化模态卡,10 个 MCP 工具与 `wide_research` 编排,fetch 核验回填证据分」——三个数字都停在 2026-08 的采样版本:现在 311 个引擎声明、19 个 MCP 工具(默认 `tools/list` 只列 4 个)、模态卡的生产端已在 2026-09-28 移除 |
| 星标 ⚠ | **101**(2026-08-19 冻结采样;**仓库级,属主项目**);2026-11-18 实时 **271**(同一仓库级,不能当插件单独热度) |
| 下载 ⚠ | 边车无记录(2026-08-19 采样缺口);`@taxueseek/argo-dsh` 到 2026-10-21 才首发 npm,采样时这个插件包还没有 npm 安装面 |
| 扩散 | **0** 个第三方(口径见「为什么它突出」:原始 `grep -ril 'argo'` 16 命中,15 条是 owner 名/`cargo`/`Argon`/`jargon` 误命中,1 条是自身) |
| 仓库 commit | `c7cd8599dbca3f642e94ca3f97726c9c23e79195`(2026-11-15,`main`);插件子目录最后提交 `d39866c`(2026-11-15),首个提交 `49f8a80`(2026-08-13),共 97 个提交 |
| 仓库创建 | 2026-07-18(`created_at` 15:06:11Z);923 个提交;GitHub `size` 13,023 KB,工作树 12.34 MB |
| 包形态 | npm `@taxueseek/argo-dsh@2.15.0`:`package.json` 的 `dsh.bundle.patch` 指向 `cordis.patch.yml`,`dsh.client` 挂 web 设置页;另一条安装路径是 GitHub 子目录。**根包 `argo-search` 是另一个 MCP-only bundle,不是本条** |
| 代码规模 | 插件 17 个文件 / 6,561 行:生产 JS/MJS 4,021(其中 `native-tools.mjs` 718 行由 Python 生成)、测试 2,103、同步脚本 171、manifest+README 266;主仓 726 个 `.py` / 198,081 行。口径与命令见末节 |

## 它到底是什么

**它是真 bundle,不是纯配置包。** DSH 侧有 4,021 行 JS,自己实现工具注册、`web_search`/`web_fetch` provider、`wide_research` 编排和设置页;但它**不实现搜索引擎**——检索仍由本机 Python 子进程完成,DSH 层只是把 `tools`/`web`/`subagents`/`credentials`/`systemPrompt` 五个机制接上去。

四个面,默认开启程度完全不同:

| 面 | 数量 | 谁执行 | 入口 |
|---|---|---|---|
| 原生一等工具 | 可注册 **18**(19 个 schema 去掉分钟级 `argo_research`),默认 **2**(`argo_search`/`argo_fetch`) | 每次 spawn 一个 `npx` CLI 进程,走 `call <tool>` | `ctx.tools.register`(`dsh/index.js:342-363`),默认值 `runner.js:50` |
| `web_search`/`web_fetch` seam | 2 个 provider,id 都是 `argo` | 常驻 stdio MCP 连接池,`tools/call` | `web.registerSearchProvider`/`registerFetchProvider`(`dsh/index.js:287-327`) |
| MCP 完整面 | **19** 个 schema,默认 `tools/list` **4** 个 | `npx -y github:taxueseek/argo` → `python3 scripts/mcp_server.py` | `cordis.patch.yml:33-41`(默认整段注释) |
| `wide_research` | 1 个编排工具 | DSH 子代理(planner → workers → synthesis),不直接打网 | `ctx.subagents` + `ctx.tools.register`(`dsh/index.js:376-381`) |

**三个"权威数字"都要拆口径。** 这张卡的 registry 自述来自 2026-08 的 v2.8.0;源码现在是三层数字:

| 说法 | 采样时(2026-08-14) | 现在 | 证据 |
|---|---|---|---|
| "10 个 MCP 工具" | 确为 10 个:`argo_search`/`argo_local_search`/`argo_research`/`argo_evidence`/`argo_clarify`/`argo_crawl`/`argo_fetch`/`argo_screenshot`/`argo_pdf`/`argo_social_search` | `TOOLS` 19 个;另有 `CORE_TOOL_NAMES` 4 个,`tools/list` 默认只返回这 4 个 | `scripts/mcp_tools.py:111-385`、`:37-38`、`:388-399`;采样值用 `git show c4c3c04:scripts/mcp_tools.py` 数得 |
| "120+ 引擎" | 当时 README 的约数 | `engines/specs/*.yaml` **311** 个;`enabled: true` **304** 个;`enabled && !explicit_only` **264** 个可被自动路由 | `assets/readme/counts.json` 也写 311;`docs/CHANGELOG.md:376` 的 "约 120+" 是 v2.6.0 口径 |
| "结构化模态卡" | 有 `modal_card` 域和 `card_type` 输出 | `modal_card` 域仍在(`config.yaml:874-895`,bocha_ai/bocha/train),但 `card_type` 的生产端在 2026-09-28 被移除,只剩排序/缓存的兼容键 | `scripts/engines_builders_cn.py:1267-1271`;`scripts/search_rank.py:388` 仍在读旧键 |

19 = 采样时的 10 个 + 后来补的 `argo_local_read`/`argo_recompute`/`argo_article`/`argo_job`/`argo_extract`/`argo_preflight`/`argo_answer`/`argo_watch`/`argo_cite`。

**包形态有两层,别装错。** 本条是 `packages/dsh-plugin` 子目录里的 `@taxueseek/argo-dsh`:npm 首版 2.9.7(2026-10-21),当前 2.15.0(2026-11-15),unpacked 约 217 KB、10 个文件。仓库根另有 `argo-search@2.15.0`(715 文件、约 7.1 MB),根 `package.json` 只声明 `dsh.bundle.patch`,没有 `dsh.client`;它是 MCP-only bundle。主 README 的 DSH 一行(`README.md:70-73`)装的是根包 `argo-search`,不是注册表这条。两者能力面不同:**根包只挂 MCP(它的 mcp 行同样没设 `ARGO_MCP_TOOLS`,默认也只列 4 个,但注释写 19,`cordis.patch.yml:3`),子目录包才有原生工具、web seam 和 `wide_research`。**

## 怎么接进 DSH

**① manifest 是标准的 bundle + web client 双声明。** `package.json:21-38` 同时给 `dsh.bundle.patch`(指向 `./cordis.patch.yml`)和 `dsh.client`(`platform: "web"`,`inject: ["@deepseek-ai/dsh-client-ui-settings"]`)。DSH 侧对这两个键都有真实校验:`dsh-app-boot/lib/index.js:518-519` 要求 `bundle.patch` 是字符串或字符串数组;`dsh-client-modules/lib/index.js:64-69` 要求 `dsh.client.platform` 是字符串并校验 `inject`。安装命令:

```sh
dsh plugin --profile web add @taxueseek/argo-dsh
# 或从 GitHub 子目录
dsh plugin --profile web add "github:taxueseek/argo#main&path:packages/dsh-plugin"
```

`dsh plugin` 本身只是把剩余参数转发给 pnpm(`$DSH/lib/bin.js:117`;`$DSH` 指本机 `@deepseek-ai/dsh` 安装目录),`--profile` 是必填;没有"子目录插件"特判,`#main&path:` 是 pnpm 的 git 子目录语法。

**② 只 inject 四个宿主服务,注册点全在 `apply()` 里。** `dsh/index.js:87-88` 写死 `name = 'wide-research'`、`inject = ['tools','subagents','systemPrompt','web']`;`apply()`(`:224`)依次做:校验配置(`:230-259`)、接 DSH 凭证服务(`:261-263`)、注册 tool guard(`:277-285`)、注册 search/fetch provider(`:287-327`)、按 `nativeTools` 增删原生工具(`:342-363`)、注册 `wide_research`(`:376-381`)、注入一段 system prompt(`:383-389`)、把设置表单设为懒保存(`:391-397`)。

**③ 设置页是真浏览器插件,不是 DSH 内置面板。** `dsh/client.js:14` 用 `window.__ModuleLoader__.load` 注册包,`:938` 声明 `inject = ['slots','locale','configForms','remote','remote.credentials']`,`:955-975` 同时挂 `settings.section` 和 `plugins.item` 两个 slot;`:981-987` 导出 `TOOLS`/`ENGINE_TOGGLES`/`KEYS` 给漂移测试对拍。设置 namespace 是 `wide-research`(`client.js:26`),不是包名。

**④ web seam 的"启用"是注册,不是选中。** 插件把 provider 注册成 `argo` 且 `available()` 默认 true(`dsh/index.js:288-325`);但 DSH 的选择规则是"配置 id 优先,没配才在所有可用 provider 里选,多个可用直接 `WEB_PROVIDER_AMBIGUOUS`"(`dsh-web/lib/index.js:100-140`,报错在 `:134`)。stock `dsh-base` 的 web 行已经 pin 了 `searchProvider: deepseek-official`、`fetchProvider: http`(`dsh-base/cordis.patch.yml:470-471`),所以**新装后 argo provider 只是注册着,`web_search`/`web_fetch` 仍走宿主默认**;要让宿主内置工具真的走 argo,必须在 profile 的 web 行显式写 `searchProvider: argo`/`fetchProvider: argo`。反过来,如果某个 profile 的 web 行没有 pin,再注册一个可用 fetch provider 就会触发上面的歧义错误——插件 `cordis.patch.yml:6-11` 的警告指的就是这一种 profile。README 说的"已在用户层默认启用"(`packages/dsh-plugin/README.md:31-35`)是作者自己的用户层,不是这个包自带的 patch。

**⑤ 凭据走 DSH 的 credentials 服务,不落插件配置。** `readHostCredentials` 从 `ctx.get('credentials')` 取服务(`dsh/index.js:201-210`),`apply` 时存进模块级变量(`:261-262`);每次新建子进程连接时,`specs.js:115-135` 遍历 `keyRefs`(默认 33 个名字,`runner.js:67-101`),用 `provider.resolve(ref)` 取值,解析成功才写进 overlay。DSH 侧的实现是 `dsh-credentials-local/lib/index.js:480` 的 `resolve(ref)`。工具 guard 和 `keyRefs` 的 POSIX 标识符校验在 `apply` 期 loud fail(`:245-249`)。

**⑥ 运行依赖比 manifest 多。** Node ≥ 18(`package.json:39-41`);`npx` 拉 GitHub 包后由 `bin/argo.js:27-35` 找本机 `python3`,再跑 `scripts/mcp_server.py`;Python 侧要 3.9+ 和 PyYAML(`pyproject.toml` 的 `requires-python` 与 `dependencies`)。插件 README 明说 `pip install pyyaml`(`README.md:101-106`)。DSH 兼容声明是 `^0.2.0-rc.1 || ^0.2.1 || ^0.2.2-0`(`package.json:31-37`),本机对照的是 0.2.1-rc.5。

## 关键实现

**插件文件结构**(`packages/dsh-plugin/`):

| 文件 | 行数 | 作用 | 关键位置 |
|---|---:|---|---|
| `dsh/index.js` | 400 | Cordis 入口:配置、凭证、tool guard、provider、原生工具、`wide_research`、system prompt | `:88`、`:224`、`:287-327`、`:342-363`、`:376-381` |
| `dsh/runner.js` | 744 | 常驻 stdio MCP 连接池、CLI 单发、web 结果映射、错误分类 | `:174-321`、`:342-391`、`:440-513`、`:691-744` |
| `dsh/wide-research.js` | 880 | 轨道规划/分阶段/有界并发/账本/门禁/报告 | `:450-513`、`:719-734`、`:736-767`、`:774-794`、`:796-825` |
| `dsh/specs.js` | 135 | 35 个 `ARGO_*` 行为开关白名单、worker 工具过滤、env 解析 | `:21-37`、`:56-92`、`:115-135` |
| `dsh/native-tools.mjs` | 718 | 18 个原生工具 schema,**由 Python 生成** | `:1-12` 生成说明,`:13-699` |
| `dsh/client.js` | 991 | 浏览器端设置页(7 个 tab) | `:14`、`:938-975` |
| `dsh/diagnostics.js` | 153 | 读本机 `usage_log/route.jsonl` 的路由观测,不含 query 原文 | `:46-105` |
| `test/*.test.js` | 2,103 | 112 个用例,含 schema 漂移、池、凭证、门禁 | `index.test.js:123-300` |
| `test/size-gate.test.js` | 106 | 单文件 1000 行门禁 | `:1-40` |

**三条数据流,别混:**

```text
① 原生工具 / web seam
   DSH tool 或 web_search ──▶ JS 参数白名单 ──▶ 常驻 MCP 池 tools/call
   ──▶ npx -y github:taxueseek/argo（未 pin）──▶ bin/argo.js ──▶ python3 mcp_server.py
   ──▶ search.py ──▶ route.py ──▶ engine_dispatch.py ──▶ 各引擎的第三方 HTTP 端点

② wide_research
   planner（outputSchema）──▶ stageTracks（depends_on 拓扑分层）
   ──▶ boundedMap workers（每轨一个 DSH 子代理）──▶ 跨轨来源账本（URL 去重）
   ──▶ synthesis（只读账本,要求 [S1] 引用）──▶ evaluateGates ──▶ Markdown 报告落盘

③ 证据回填（是可选手工路径,不是 wide_research 的步骤）
   argo_search 返回 fetch_suggested ──▶ 模型调 argo_fetch ──▶ fetch_v3 把正文吸收分写进 URL 缓存
   ──▶ 下一次 argo_search 的 evidence_loop 回填 post_fetch_absorption
```

**统一搜索的路由是规则,不是模型。** `route.py:738-837` 只有三条分支:用户 `engine=` 指定 → 直接返回(`:782-805`);命中域规则 → 用 `config.yaml` 的 `domains` 装配 combo(`:828-839`);否则 TF-IDF 语义路由,再不行走通用保底(`:846` 起)。域规则在 `route_domains.py:1-40` 里定义成声明式数据(patterns/priority/unless/intent_required),`config.yaml` 当前有 **99 个域**;引擎按能力族分组(`engine_families.py:11-32`,web_general/academic/code/finance/news/social/...);语言侧是 `route_lang.py:2-18` 的书写系统判定 + `ENGINE_LANGS` + 18×29 的 `lang_capability` 画像。三个维度都不是 LLM 判断,而是可测试的正则/查表/权重。

**请求发给谁:没有 Argo 云服务。** 每个引擎在 `engines/specs/*.yaml` 里声明自己的 `url`/`method`/headers(例:`brave.yaml:1-20` 直接指向 `api.search.brave.com`,tavily_free 指向 `api.tavily.com`),由本机 Python 进程直接出网;抓取链还可能经 `r.jina.ai`、Parallel、Wayback 或本机 Chrome CDP(`fetch_v3.py:1-31`)。`usage_log.py:1-10` 明确"仅本机,不外发";`route_telemetry_export.py:1-10` 也只有本地脱敏导出。**没有 Argo 托管的中转或计费服务。**

**返回结构是双层。** Python 侧返回 `results[]`(title/url/snippet/source/score/published_at,可选 `selection`/`absorption`/`credibility_fast`/`evidence_flags`/`fetch_suggested`/`post_fetch_absorption`)、`engine_outcomes[]`、`coverage`、`limitations`、`evidence_loop`,以及 envelope 的 `candidates[]`(`search_output.py:576-700`、`candidate_envelope.py:357-410`)。`summary: true` 会裁成 80 字 snippet、只留 4 个 evidence_loop 字段、engine_outcomes 去 detail(`mcp_compact.py:22-99`)。**但 DSH 的 web seam 只映射 `results[].title/url/snippet`**(`runner.js:128-141`),score、authority、evidence 全部丢掉;原生 `argo_search` 则返回原始 compact JSON。所以同一个搜索,走 `web_search` 和走 `argo_search` 拿到的证据面不一样。

**失败隔离做在引擎调度层,单引擎不会拖垮整体。** `engine_dispatch._run_one` 对缺 env(`:388-395`)、远端配额(`:409-421`)、熔断(`:423-436`)、预算(`:459-465`)逐层前置跳过;网络异常被收成 `{error}` 条目而不是抛出(`:497-500`);wave-1 是 primary+backup 的 hedged race,wave-2 才铺第 3 个及以后,串行路径也有 stagger(`:849-981`)。总预算 fast 6s/auto 10s、单引擎 10s(`search.py:372,381,489`),掉队宽限 1.5s(`:425`)。全挂时返回空 `results`,由上层门禁处理。

**`wide_research` 的编排是真的,但证据核验不是自动的。** planner 要求 2–9 条互不重叠的轨道,`depends_on` 缺失只警告、成环则并入最后一阶段(`wide-research.js:272-300`);workers 用 `boundedMap` 限并发,每个子代理 `maxDepth: 1`、必须支持 `outputSchema`/`depthLimit`(`:384-425`);账本只收 http(s) URL,按规范化 URL 去重后编号 S1..Sn(`:302-343`、`:774-794`);synthesis 只拿到账本和全局 sources,提示词要求 `[S1]` 引用且"不要发明 URL"(`:796-825`)。

门禁是结构性的,不是事实核查(`:450-513`):没有 sources 且没有本地一手文件 → `failures`(cap low);没有完成轨道 / 全失败 → failures;部分失败、全部 confidence 不是 high、caveats+unanswered 超阈值、内容农场过半、recompute 未跑或与检索数字无交集 → warnings(cap medium);干净才 high(`:510-512`)。`source.confidence` 是 **worker 自己填的 high/medium/low** 字符串,`normalizeSource` 只做枚举钳制(`:316-324`),没有任何正文抓取或交叉打分。

**可复现性只到流程层。** 报告落盘到 `~/.dsh-research/<ts>-<slug>.md`(`runner.js:65`、`wide-research.js:625-632`),账本有 URL,本地一手文件有 sha256、大小、mtime(`:539-558`),recompute 有 stdout 尾和 values;但 web 来源没有正文快照或内容哈希,`confidence` 是 worker 主观档,重跑同一问题只能复现"流程",不能复现"证据"。**两套证据语言也不互通:** `wide_research` 不调用 `argo_evidence`,门禁用 `confidence` 字符串;`argo_evidence` 的 `credibility.final` 是另一套五维分,二者没有映射。

**证据分在引擎里是另一套东西。** `argo_evidence` 调用 `evidence.compute_credibility`(`mcp_handlers.py:392-408`),代码里的公式是五维加权:

```text
final = selection*0.35 + absorption*0.30 + freshness*0.15
      + original_score*0.10 + traceability*0.10
```

(`evidence.py:733-739`;文件头的 0.40/0.35/0.15/0.10 是旧注释,与代码不一致。)它输出逐条 breakdown,但**不参与搜索排序**;排序层只是复用 `score_authority`/`score_freshness` 两个子分(`search_rank.py:673-730`),`_attach_selection_signals` 还明确写着"独立于排序 score"(`:845-853`)。真正会把正文级证据分写回排序的只有 CLI `--verify`:先 `verify_results` 抓 top-k,再 `reorder_by_evidence` 只对已核验且正文质量低于 0.5 的结果降权(中性点 0.5、权重 0.35、只降不升),调用点在 `search_cli.py:648-670`,`evidence_loop.py:336-436` 是实现。**DSH 插件从不传 `--verify`,编排器本身也不 fetch;所以注册表说的 fetch-verify 闭环在引擎侧成立,在 DSH 适配层不成立。** 模型仍可手工闭合:`argo_fetch` 成功时 `fetch_v3` 会把吸收分写进同一 URL 缓存条目(`fetch_v3.py:1674-1682`),下一次 `argo_search` 就能回填 `post_fetch_absorption`(`evidence_loop.py:249-276`)。

## 为什么它突出

**先拆星标归属,这是本卡的核心。** GitHub 星标只有仓库级,没有路径级;时间线如下:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-07-18 | 仓库创建 | GitHub API `created_at` |
| 2026-08-13 | DSH 插件子目录首个提交 `49f8a80` | `git log -- packages/dsh-plugin` |
| **2026-08-19** | **101 星采样点** | `data/stars.json` |
| 2026-10-21 | `@taxueseek/argo-dsh` 首版 2.9.7 上 npm | npm registry |
| 2026-11-15 | 仓库 HEAD `c7cd8599` / 插件 2.15.0 | `git log -1` |
| 2026-11-18 | 271 星(实时) | GitHub API `stargazers_count` |

采样时仓库 32 天,插件子目录 6 天;插件还没进 npm;主 README 把 DSH 列为五个客户端之一(Claude Code MCP、skills.sh、Cursor/Windsurf、CLI、DSH,`README.md:44-73`),并且 DSH 那一条装的还是根包。**可分离的 DSH 归因上限 = 首提交到采样日的 6 天增量,无法证明任何一颗星来自这层适配;本卡把 101/271 全部记在主项目名下,适配层记 0。** 这不是保守,是仓库级星标拆不出来。

**扩散是 0,而且 16 条原始命中要逐条筛。** 命令与分类:

```sh
grep -ril 'argo' data/plugins/ | wc -l          # 16
grep -ril 'argo' data/plugins/ | grep -v 'taxueseek__argo'
```

| 类型 | 命中 | 数量 |
|---|---|---:|
| 自身 | `taxueseek__argo--packages-dsh-plugin.yml` | 1 |
| owner 名里含 `argo` | `apcamargo__dsh-claude-subscription`、`apcamargo__dsh-review`、`FSMargoo__dsh-at-file` | 3 |
| `cargo`(Rust 包管理器/缓存变量) | `173787247__dsh-wsl-pkg`、`YunaAloft__dsh-rtk-workbench`、`kennethfan__dsh-sandbox-tune`、`JayYuen666__dsh-quality-gate`、`1250589385__dsh-test-autofix`、`988hj7tczd-oss__dsh-dep-vuln-scan` | 6 |
| `Argon`/`Argon2id` | `Francesco502__dsh-quota`、`PipeDream941__dsh-subagent-antigravity`、`hxy91819__dsh-auth` | 3 |
| `jargon` | `zhengqiuyang__dsh-trust-panel`、`miqian-nomad__dsh-browser-playwright-codex`、`yuyu654__dsh-drop-by` | 3 |

**第三方真实提及/衍生 = 0。** 扩散结构不是"有人跟做",而是 vendor 自引用:主 README 的同段列了同 owner 的 4 个 DSH 插件(`README.md:36`),它们都是 taxueseek 自己的分发家族,不是第三方采用。

**按两轴口径:明星,不是锚。** 声量来自主项目(271 星、311 引擎、198k 行 Python),扩散为零;这层 4 千行适配器的独特性在于它把 DSH 的 `tools`/`web`/`subagents`/`credentials`/`systemPrompt` 五个 seam 同时用满,而不是只挂一个 MCP。按本册 `single-purpose` 的 ≥800 星门槛,它不够格;这张卡若成立,靠的是机制样本价值,不是声量。

**可复用的协议面存在,但不在 DSH 适配层。** 两层:① 工具 schema 以 `scripts/mcp_tools.py` 为唯一真源,`gen_native_tools.py` 生成 `native-tools.mjs`,`tests/test_native_tools_sync.py` 做漂移门禁——这是可被任何宿主复用的 MCP/CLI 契约;② `wide_research` 的轨道/账本/门禁语义在 Python 里有一份同构实现 `scripts/wide_research.py:1-26`(给只有 bash 的宿主用),说明这套 JSON 协议是跨宿主的,不只是 DSH 内部形状。但第三方采用为 0,所以它是"可复用",不是"已被复用的标准"。

## 代价与边界

按发生顺序:

1. **安装/激活**:`npx -y github:taxueseek/argo` 拉的是 `main`,不 pin commit(`runner.js:58-61`);`bin/argo.js:27-35` 依赖本机 `python3`,`pyproject.toml` 还要 PyYAML。缺 Python/PyYAML 时原生工具和 MCP 池一起失效,web provider 调用会抛错;`ctx.effect`/`registerFetchProvider` 是可选的,旧宿主会静默少能力(`index.js:307`、`:392`)。
2. **web provider 选择**:包本身不 pin `searchProvider`/`fetchProvider`(`cordis.patch.yml:42-52` 只配 `wide_research`);stock `dsh-base` 已 pin `deepseek-official`/`http`(`dsh-base/cordis.patch.yml:470-471`),所以新装后 argo seam 注册但不被选中;若 profile 没有 pin 且已有另一个可用 fetch provider,则 `WEB_PROVIDER_AMBIGUOUS`(`dsh-web/lib/index.js:134`),`web_fetch` 整个不可用。README 的"默认启用"是作者用户层,不是包。
3. **MCP 工具面**:按 `cordis.patch.yml:33-41` 取消注释后,`tools/list` 默认只返回 4 个 CORE(`mcp_tools.py:37-38`、`:388-399`),不是 README 说的 19;要 19 个得在 MCP 进程 env 里设 `ARGO_MCP_TOOLS=all`,而那段 patch 没设。`tools/call` 仍认全量名,但模型看不到未列出的 schema。
4. **超时/限流/部分结果**:搜索 30s、原生单发 60s、抓取 25s(`runner.js:51,56,62`);常驻池上限 3、空闲 60s 回收(`:63-64`);MCP 请求超时会关闭整条连接(`:222-230`);native 工具会回退到单发 spawn(`:731-741`),web provider 不会回退(`:515-567`)。引擎 spec 还声明 qps/period(例 `engines/specs/tavily_free.yaml:23-24` 是 1 次/秒),由配额层限流;全引擎失败时 `results=[]`,由 `wide_research` 的 `no_sources` 门禁降到 low。
5. **worker 工具白名单在 rc.2 上不生效**:`startStructured` 的 `startActivation` 分支只传 `prompt`/`parent`/`outputSchema`/`maxDepth`/`agentOptions`(`wide-research.js:392-409`),`toolFilter` 只在 legacy `start` 分支写入(`:410-413`);`apply` 的 `ctx.tools.guard` 只拦 `wide_research` 自身(`index.js:277-285`),不拦 `bash`/`write`。README 的"worker 默认只能调 argo 取证工具"(`README.md:45`)在 rc.2 上没有源码支撑;旧 alpha.x 的 `start` 分支才有 `toolFilter`,连带 `argo_research` 的"硬保护"也落在这份 allow 列表上(`specs.js:32-36`),同样只在 legacy 分支生效。
6. **证据可信度**:编排器不 fetch、不校验 URL 存活,只检查 `http(s)` 协议(`wide-research.js:302-315`);`confidence` 由 worker 自填(`:316-324`);worker 可以自己调 `argo_fetch`,但提示词里没有"每条来源必须抓正文"的强制步骤。`argo_preflight` 不在默认面里:原生默认只挂 2 个(`runner.js:50`),MCP 默认只列 4 个(`mcp_tools.py:38`)。因此**编造或过时链接可以进账本**,门禁只数条数和 confidence,不验内容。
7. **代码执行**:`wide_research` 只要模型传了 `recompute.script`,就会带 `allow_exec: true` 调 `argo_recompute`(`wide-research.js:573-581`),等于把"是否授权"也交给模型。执行器确实有沙箱:默认拒绝、输入白名单、Python 层断网、禁 subprocess/ctypes、超时 killpg、内存软限(`recompute.py:1-19,58-90`);但 `recompute.py:10-13` 自承 C 扩展/外部进程不覆盖。
8. **环境与隐私**:子进程环境是 `{...process.env, ...overlay}`(`specs.js:134`),不是白名单——宿主进程里的所有环境变量都会进 argo 子进程;插件绕过了 `dsh-subprocess` 的 `SENSITIVE_ENV_PATTERN` 剥离(`dsh-subprocess/lib/index.js:32,50`)。查询会直接发给选中的第三方引擎;本地 `usage_log` 默认记录 query 原文,掩码开关 `ARGO_USAGE_LOG_MASK` 默认关(`usage_log.py:135-146`),且不在插件 35 个开关白名单里。
9. **计费**:没有 Argo 账户;付费引擎用用户自己的 key。`ARGO_PAID_SEARCH` 默认 `auto`,`ARGO_BUDGET_DEEPSEEK_SEARCH` 默认 ¥5/月、`ARGO_BUDGET_EXA` 默认 $10/月,AnySearch/知乎/元宝/Tavily 各有日/月次数上限(`specs.js:80-86`);配额耗尽才回落免费源。默认 `keyRefs` 包含 `DEEPSEEK_API_KEY`(`runner.js:68`),所以装完插件后搜索可能直接花 DSH 已有的 DeepSeek key。

维护成本不低:4,021 行 JS + 198,081 行 Python;DSH 兼容声明覆盖 0.2.0-rc.1 到 0.2.2-0;工具 schema 由 Python 生成,改 `mcp_tools.py` 后要重跑 `gen_native_tools.py`,否则 `test_native_tools_sync.py` 红;112 个 JS 用例里有 2 个 abort/timeout 时序用例在我两次运行中波动过一次。

## 可信度与复现

证据等级 ★★★:DSH 适配层逐文件读过;Python 侧只读了路由/调度/证据/抓取/输出/重算的关键模块与文件头,311 个引擎 builder 没有逐个读;`wide_research` 没有在真实模型上跑过。卡片头的 commit 是整仓 HEAD `c7cd8599…`(2026-11-15),读取日为 2026-11-18;插件子目录最后提交是 `d39866c`(2026-11-15),两者之间插件文件无变化。

```sh
# 1) 克隆与提交
git clone --depth 1 --filter=blob:none https://github.com/taxueseek/argo.git /tmp/an-argo
cd /tmp/an-argo && git fetch --unshallow --filter=blob:none   # 浅克隆只有 1 个提交,先补历史
git log -1 --format='%H %ad'        # c7cd8599… 2026-11-15
git log -1 --format='%H %ad' -- packages/dsh-plugin   # d39866c… 2026-11-15
git log --reverse --format='%H %ad' -- packages/dsh-plugin | head -1  # 49f8a80… 2026-08-13

# 2) 规模
find packages/dsh-plugin -type f | xargs wc -l | tail -1        # 6561
find packages/dsh-plugin/dsh  -type f | xargs wc -l | tail -1   # 4021
find packages/dsh-plugin/test -type f | xargs wc -l | tail -1   # 2103
find . -path ./.git -prune -o -name '*.py' -print0 | xargs -0 cat | wc -l  # 198081

# 3) 工具/引擎数字
grep -c '"name":' scripts/mcp_tools.py                  # 19
grep -c '^  "argo_[a-z_]*": {' packages/dsh-plugin/dsh/native-tools.mjs  # 18
ls engines/specs/*.yaml | wc -l                         # 311
grep -l '^enabled: true' engines/specs/*.yaml | wc -l    # 304
git show c4c3c0421a676c6295badb1e157386e50906a5a6:scripts/mcp_tools.py | grep -c '"name":'  # 10

# 4) 扩散
grep -ril 'argo' data/plugins/ | wc -l                  # 16
grep -ril 'argo' data/plugins/ | grep -v 'taxueseek__argo'  # 15 条,全是误命中

# 5) 测试
cd packages/dsh-plugin && node --test test/*.test.js     # 112 tests, 111 pass, 1 skip
```

读过的文件:`packages/dsh-plugin/` 下 `package.json`、`cordis.patch.yml`、`README.md`、`dsh/index.js`、`runner.js`、`wide-research.js`、`specs.js`、`native-tools.mjs`、`client.js`、`diagnostics.js`、`test/index.test.js`(用例清单)、`test/size-gate.test.js`、`scripts/sync-local.mjs`;Python 侧 `scripts/mcp_tools.py`、`mcp_transport.py`、`mcp_handlers.py`、`mcp_compact.py`、`route.py`、`route_domains.py`、`route_lang.py`、`engine_families.py`、`engine_dispatch.py`、`search.py`、`search_rank.py`、`search_output.py`、`evidence.py`、`evidence_loop.py`、`search_cli.py`、`fetch_v3.py`、`url_safety.py`、`recompute.py`、`usage_log.py`、`wide_research.py`、`bin/argo.js`、`config.yaml`(域/缓存/模态卡段)、`engines/specs/brave.yaml`、`engines/specs/tavily_free.yaml`、`docs/CHANGELOG.md`;DSH 官方 `dsh-app-boot`、`dsh-web`、`dsh-client-modules`、`dsh-credentials-local`、`dsh-tools`、`dsh-subagent`、`dsh-subprocess`、`lib/bin.js` 的相关段。

未读:311 个引擎 builder 的逐源实现、`semantic_evidence.py`、`research*.py` 的完整流水线、`matrix_search_eval`/`replay_eval` 评测、`tests/` 里除 DSH 外的 Python 门禁。

## 待验证

1. **实际 `tools/list`**:在 Python 3.9+/PyYAML 可用的机器上跑 `npx -y github:taxueseek/argo` 与 `ARGO_MCP_TOOLS=all npx -y github:taxueseek/argo`,确认默认 4/全量 19;本次环境 `python3` 缺 PyYAML,没跑。
2. **web seam 在真实 profile 的选中结果**:本机 `dsh-base` 的确 pin 了 `http`/`deepseek-official`,但用户层是否另有 `searchProvider: argo` 未查;需要在 `dsh web` profile 里看一次 `web_search` 实际走谁。
3. **`wide_research` 端到端**:README 自述 rc.2 上 planner→2 worker→synthesis、14 sources 跑通(`packages/dsh-plugin/README.md:108-119`),本次没有真实模型,未复跑;门禁的 `source.confidence` 分布也没有样本。
4. **`sourceKeys` 是否真的断链**:`wide-research.js:804` 用 `outcome.result.sources.map(s => s.key)`,但 key 是在 `:782-784` 新建对象上赋的,`outcome.result.sources` 没有 key;按代码应恒为空数组。synthesis 仍能从全局 `sources` 拿到 `[S1]`,但轨道→来源的映射会丢。需要一个 fixture 确认报告是否还能按轨道引用。
5. **星标时间线**:需要 GitHub `stargazers` 的 `starred_at` 或 star-history 曲线,才能知道 101 里有多少在插件首提交前就已存在;本次只有仓库级 101/271。
6. **recompute 沙箱边界**:`recompute.py:10-13` 自承 C 扩展/外部进程不覆盖;模型能否用允许的 stdlib 模块读到白名单外文件或逃逸,未做红队测试。
7. **npm 下载量**:边车无记录,`@taxueseek/argo-dsh` 2026-10-21 才发布,真实采用量未采集;不能用 0 表示"无人使用"。
