# dsh-auto-memory — 把"召回"从模型手里挪到宿主侧：本地判定核先决定要不要想起，命中后只往历史尾部追加一段固定边界引用块

> 证据等级:★★★(源码级;`Aik358/dsh-auto-memory@a244cf03f6f409b655d86e02d6c0a7b86d7496f4`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 16、下载 3,782 为 2026-08-19 历史采样;2026-11-18 实时星标 204。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `Aik358/dsh-auto-memory`([registry](../../../data/plugins/Aik358__dsh-auto-memory.yml)) |
| 类目 | memory(504 条,[census](../../ecosystem/census.py) 全表 11 744 条) |
| 子分类 | `context-shaping` —— 但它**同时写持久化 Markdown**;按本册"是否产生持久化"的划线标准,这张卡落在交界带上(见「它到底是什么」末段) |
| 自述 | 「主动联想记忆 + Astra 式上下文管理:自动唤回(固定边界注入,前缀缓存友好)/自动沉淀/技能固化/交接账本与 PLAN 白板跨窗口续命/水位感知。本地 Markdown 存储,模型无关,零依赖」——五项在源码里都各有落点,但"零依赖"要拆开看:零**第三方**运行库,不零可选项 |
| 星标 ⚠ | **16**(2026-08-19 边车);2026-11-18 实时 **204**(GitHub API,约 12.75×) |
| 下载 ⚠ | **3,782**(npm 月下载,2026-08-19 边车;口径见 [`_method/01-fresh-probe.md`](../../_method/01-fresh-probe.md)) |
| 扩散 | **0**(`grep -ril 'auto-memory' data/plugins/` 命中 5 条,减去自身 4 条,逐条人工判断后**全部不是**对本插件的提及:3 条指 Claude Code 的同名特性、1 条是另一个作者的同名仓库。命令与逐条判定见末节) |
| 仓库 commit | `a244cf03f6f409b655d86e02d6c0a7b86d7496f4`(2026-10-31,`fix(release): 补提交 lib/index.js 静态 import 的两个模块`);`pushed_at` 2026-11-12(别的分支);仓库建于 2026-08-14 |
| 包形态 | npm `@a9i5k4/dsh-auto-memory@3.3.17`,**双面包**:宿主面 `exports['.'] → lib/index.js` + 浏览器面 `exports['./client'] → lib/client.js`;`dsh.bundle.patch` + `dsh.client` 两条 manifest 契约 |
| 代码规模 | `lib/*.js` **115 个文件 / 75 564 行**(宿主面 55 811 行 + `lib/client.js` 19 753 行);测试 `tests/smoke/*.mjs` **443 个套件 / 76 783 行**;仓库 1 772 个受管文件、工作树 151.8 MiB、GitHub 仓库体积字段 357 602 KB |

## 它到底是什么

**形态判定:一张自带引擎、自带 GUI 的双面 Cordis 插件。** 不是配置包(有 5.5 万行宿主代码),不是外部服务适配层(没有远端 API,数据全在本机;`lib/` 只 import `node:` 内建,见复现节),也不是"薄壳 + 大依赖"——它的重量全在自己身上。

它的机制核心只有一句:**召回这个动作的所有权不在模型手里。** 模型不需要"记得去查",因为宿主在每一轮自己判断要不要想起、想起哪条,然后把结果塞进下一个请求。源码里能指到的三件事:

1. **观察**:`session/event` 与 `tools/result` 两个只读入口把会话事件流和工具执行结果喂进 per-session runtime(`lib/index.js:17541-17547`);`agent/pre-step` 在放行每个 step 前刷新状态(`lib/index.js:17440`)。
2. **决策**:宿主侧判定核,不是模型调用。默认走 `lib/semantic-decide.js` 的 JS 闭环——意图头特征 + 一个**落在仓库里的 Logistic Regression 工件** `lib/policies/recall_intent_lr_v1.json`(Platt 校准 `a/b` + 46 个系数),顶层注释明说"纯函数、零依赖、工件加载 fail closed"(`lib/semantic-decide.js:1-20`)。
3. **投递**:命中后组包,在 `systemPrompt.context()` 的**固定尾巴**渲染成 Reference Tail——首行固定标记行、每条 4-5 行、末两行固定收尾,整包 UTF-8 字节封顶(`lib/activation-inbox.js:29-31,58,60-63,269-312`)。

**数据模型:三层 Markdown + 一层 JSON 中枢。**

| 层 | 位置 | 形态 | 写者 |
|---|---|---|---|
| 用户级 | `~/.dsh/memory/MEMORY.md`(`lib/index.js:3659`) | Markdown,整篇/追加,容量 24 000 字符 | 模型(`memory_user`)、`memory_rules` 条目级增删改 |
| 项目层 | `~/.dsh/memory/workspaces/--<ws>--/MEMORY.md`(集中式;旧 `{ws}/.dsh-memory/` 自动复制迁入,`lib/index.js:3600-3614`) | Markdown,容量同上 | 模型(`memory_note`)、自动沉淀升格 |
| 每日日志 | 同目录 `YYYY-MM-DD.md` | Markdown,**append-only**(`lib/index.js:3663`) | 模型(`memory_log`)、自动沉淀(`[自动沉淀]` 标记) |
| 交接面 | 同目录 `handoff/PLAN.md` + `handoff-YYYYMMDD-HHMMSS.md` | Markdown,PLAN 带 sha256 revision、旧版归档 | 模型;骨架由宿主首建 |
| 记忆中枢 | `~/.dsh/memory/hub/procedures.json` 等(`lib/index.js:16135,16163`) | **JSON** 状态机,不是 Markdown | procedure 引擎 |
| 技能导出 | `~/.dsh/skills/mem-skill-*/SKILL.md`(`lib/skill-export-host.js:28-40`) | Markdown,进 DSH 技能系统 | 晋升为 active 后自动导出 |

所以问"它到底新不新增长期存储"——**新增,而且新增得很实**:三层 Markdown 全是它自己维护的文件,不是 DSH 官方会话日志的投影。它落在 `context-shaping` 的理由是**注入侧**的机制(见下),不是因为它不写盘。

## 怎么接进 DSH

**① manifest 是两条契约,不是一条。** `package.json:28-31` 的 `dsh.bundle.patch` 让它成为 profile 层;`package.json:32-42` 又声明 `dsh.client`(`inject` 六个 `@deepseek-ai/dsh-client-*` 服务 + `"platform": "web"`),让浏览器半以 `exports['./client']` 加载。`cordis.patch.yml` 只有一行 insert:

```yaml
- insert:
    - id: auto-memory
      name: '@a9i5k4/dsh-auto-memory'
```
(`cordis.patch.yml:7-9`;文件头注释自己说明宿主半跑 `/api/dsh-auto-memory` 路由 + 工具 + 注入,浏览器半挂在 `/plugins/<id>/client.js`)

**② 服务注入五个**:`export const inject = ['webServer', 'tools', 'systemPrompt', 'subagents', 'llm']`(`lib/index.js:335`)。`subagents` 是为自动沉淀的子代理,`llm` 是给提炼任务,`webServer` 是那 73 条路由。

**③ 绑 6 个生命周期事件 + 1 个 `session/event` 观察口**(全部在 `apply()` 内):

| DSH 事件 | 行 | 干什么 |
|---|---|---|
| `agent/session-start` | `lib/index.js:17376` | 建 runtime、补放既有事件(`seedRuntimeFromSession`)、刷新缓存;子代理会话不顶 `_lastAgent` |
| `agent/turn-stopping` | `:17398` | 轮末测量水位 + 600ms 后启动自动沉淀 |
| `agent/pre-step` | `:17440` | **注入前置**:刷状态、写请求键、`checkWaterLevelAtStep`、activation claim |
| `agent/disposed` | `:17532` | 放弃该 session 的 runtime |
| `session/disposed` | `:17535` | 同上,按 session 粒度 |
| `session/event` | `:17541` | 结构化事件流(只观察) |
| `tools/result` | `:17544` | 工具执行终态(只观察) |

另有 `ctx.on('dispose')` 置位(`:17333`)与 `ctx.effect(() => disposeSurfaces, ...)`(`:15736`)。

**④ 注入面是三个,不是一个**(这是本卡的关键,三个面语义完全不同):

| 面 | 注册 | order | 内容 | 为什么这样放 |
|---|---|---|---|---|
| 静态纪律 | `ctx.systemPrompt.section({name:'dsh:auto-memory-pre-rules'})` `lib/index.js:18294-18302` | 10000 | `renderMemoryStatic()` 返回**常量字符串数组**(`lib/index.js:8709-8752`),零动态数据 | system prompt 字节级稳定 = 前缀缓存的锚;注释直说"固定不变,是 DeepSeek 前缀缓存的锚" |
| 动态记忆快照 | `ctx.systemPrompt.context({name:'dsh:auto-memory-pre'})` `lib/index.js:17551` | 10000 | 完整版/精简版交替 + 每轮节流 | 走 context 而不是 section,动态内容就不进 system prompt |
| 唤回尾注(Reference Tail) | `ctx.systemPrompt.context({name:'dsh:m6-reference-tail-pre'})` `lib/index.js:18304` | 10001 | 只渲染**已 claim** 的 packet | 渲染即投递:返回非空 = 真进了 messages → 同步 `markDelivered` + `seen` 证据(`lib/activation-host.js:1-14`) |

**⑤ 19 个工具**,注册点 `ctx.tools.register`(`lib/index.js:21207`):`memory_log/note/user/rules/read/recall/maintain/status/reflect/external/consolidate/procedure/procedure_list` + `calendar_add/list/done/remove`,再加两个只在 `boardMode=graph` 挂载的 `memory_expand`/`memory_trace`(`:19114,19118`)。

**⑥ 73 条 HTTP 路由**(`lib/index.js:393-410` 起),默认只允许回环:HOST 必须 localhost 且来源 IP 是 `127.0.0.1/::1`(`:14086`)。3.3.16 起加了私网白名单形态——四条**同时**满足才放行,缺一条仍 403(`:793-800`)。

**⑦ 依赖**:`peerDependencies` 只有 `@deepseek-ai/cordis ^4.0.1`(`package.json:55-57`),`optionalDependencies` 只有 `@huggingface/transformers ^3.7.6`(`:58-60`),**没有 `dependencies`**。

## 关键实现

**文件结构(宿主面,按"机制责任"列)**:

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `lib/index.js` | 21 212 | 引擎全部:事件、三个注入面、19 工具、73 路由、水位、接续、自动沉淀 | `:335` 服务;`:17551/18294/18304` 注入面;`:5101` 水位;`:5612` 接续;`:13257` 沉淀 |
| `lib/tier-layer-inject.js` | 774 | **三层注入装配**:Tier-0 目录每轮在场、Tier-1 闸门下探、Tier-2 按需取原文;任何一层缺数据必须写 `[降级]` 行 | `:44-52` 冻结预算 `B0=800 token / L1=140 字 / K=8 / B2=2400 字`;`:101-118` 状态闸 |
| `lib/tier0-catalog.js` | 852 | Tier-0 目录生成:每条 1 行「标题 · 一句结论 · layer · status · 日期」,预算硬上限 | `:1-30` 契约与裁剪优先级;`:31-40` CJK 预算口径(保守 `ceil(字符/2)`) |
| `lib/activation-inbox.js` | 494 | **固定边界 Reference Tail 渲染器** + 卫生 guard | `:29-31` `maxPacketBytes=4096`;`:58` 首行标记;`:269-312` 逐条装填/超预算整条丢 |
| `lib/activation-host.js` | 614 | capability 探测(有没有 `systemPrompt.context`)、pre-step claim 四重门、delivered/seen | `:31-40` capability;`:63-64` 双门默认关 |
| `lib/procedure-store.js` | 1 097 | 技能库状态机 `observed → validated → active → deprecated` | `:71` 枚举;`:102-103` 晋升门;`:440-441` 判定式 |
| `lib/skill-export.js` + `-host.js` | 400 + 408 | procedure → `SKILL.md` 渲染 + 写盘/清扫/退役 | `:8-40` 目录与自检标记;`:60-78` 旧目录清扫 |
| `lib/water-window.js` | 545 | 窗口解析(settings.yaml 双风格 + 会话 request/header 模型边界亲和) | `:13-70` YAML 解析;`:88-120` 模型边界亲和 |
| `lib/handoff-anchor.js` | 114 | 账本四段**权重化截断** | `:18-22` 权重表;`:91-114` 截断顺序 |
| `lib/path-write-queue.js` / `lib/fs-retry.js` | 52 / 46 | 按路径串行原子写(tmp+rename);rename 瞬时错误退避重试 | `path-write-queue.js:1-22`;`fs-retry.js:18-24` |

**A. 固定边界到底在哪注入**(最常被自述含糊掉的一处)

**动态记忆与唤回尾注都不进 system prompt**,而是 `systemPrompt.context()` 投影出来的 **user 消息**;留在 system prompt 里的只有那段常量纪律。DSH 侧证据(`dsh-agent-loop/lib/index.js`):

- `RuntimeContextProjection.project()` 把渲染结果包成 `createUserMessage({source:{kind:'runtime-context'}})`,**且仅当文本与上一条保留的快照不同才返回新消息**;相同返回 `undefined`(`:334-352`)。
- `preStep()` 的顺序是:assemble → `agent/pre-step` 瀑布 → 默认回调才 `project()` 并把 context 追加进本轮待投递消息(`:902-920`)。
- `step()` 里,`preStep` 那份帧会被**结构性丢弃**,只有 `refreshContext()` 重新渲染的那份进模型(`:1044-1075`,`contextAdmitted` 分支)。

于是"前缀缓存友好"在源码上是两件事叠加:①system prompt 通道只放常量(`lib/index.js:18294`),字节不变;②动态内容全部**追加在历史尾部**成新消息,已发出的前缀不动。插件把这条纪律写在三处注释里(`lib/index.js:8158-8162`、`:8419-8421`、`:17549-17550`),DSH 侧的 `project()` 去重是它的实现前提。

**B. 一次请求调两次 `text()`,所以有"请求键"**

插件实测:宿主在同一个模型请求里调 `context().text()` **恰好两次**(`lib/index.js:17443-17456` 注释,实测差 1)。第一次(preStep assemble)的结果被丢弃,第二次(refreshContext)才生效。于是:

- 若两帧渲染不同,完整版会被后一帧的精简版覆盖 —— 这就是 `requestIdPre()` 的存在理由。
- 请求键不能用 `step/start`,也不能用事件条数(两帧之间宿主会 append `step/start`);它用**最近一次 `step/end` 的 seq**(`lib/index.js:8352-8382`),两帧之间恒定、下一请求自动翻新。
- 返回前把定稿写进 `stF._reqTextPre`(`:17608-17620`),后续帧原样复读。副产物:`renderReflectionRequest()` 是**一次性**的(调用即置位),不缓存拼接结果两帧根本不可能逐字节相同。

**C. 三层注入与"降级必须可见"**

`lib/tier-layer-inject.js` 的三个 tier 不是"记忆的三层",是**检索的三层宽度**:Tier-0 目录每轮在场(≤800 token)、Tier-1 只在语义命中时给 top-8 摘要(每条 ≤140 字)、Tier-2 只在问句带"原文/行号/命令/报错"语义时给命中块原文(单块 ≤2400 字)。未命中时**只给目录层**——这是省 token 的关键(`:1-16`)。缺数据写 `[降级]`、逐层摆候选/进目录/裁剪数写 `[层账]`,禁止静默丢弃(`:17-27`)。注入侧还要挡下非 `current` 条目:直接 import 检索侧的 `isCurrentPre` 而不复制一份,避免"检索放行、注入挡下"的双源漂移(`:38-46`);#431 之前目录是从原文重建的,被撤回的条目会**换个位置重新进注入**(`:20-30`)。

**D. 水位 → 换窗口,而不是裁剪**

- 分子:官方 `tokenMeter`(`agent.ctx.get('tokenMeter').measure`, `lib/index.js:5186-5192`),`baseline.kind !== 'none'` 才采信。
- 分母:三源 + 兜底。`manual` 覆盖 > 会话自报 `request/context.contextWindow` > `settings.yaml` 解析 > `fallback 131072`(`lib/water-window.js:1-10`;`lib/index.js:4886`)。冲突取**较大**值,但 provider 400 文本里的真实窗口取**较小**(`lib/index.js:5158-5172` 有完整方向性论证)。
- 阈值:默认 `waterLevelThresholdMode='auto'`,**镜像官方压缩公式** `officialRatio = min(thresholdRatio, ((W−O)−B)/W)`,`×0.9` 留余量,保证先于官方 80% 触发(`lib/index.js:517-538`)。手算不可读 `resolveCompactSpec`(模块私有、引擎不导出),所以只能镜像——注释写明了这一点。
- 触发后不是压缩,是 `armAutoContinue`(`lib/index.js:5612`):倒计时(默认 35s,浏览器活着时出确认卡)→ 到期由宿主直调 `sessionController` **建新会话** → 把 18 000 字符的接续材料当**第一条 user 消息**投进去(`:5925`)。材料分 `head`(指令)/`nav`(逃生出入口)/`bulk`(正文):`head`+`nav` **永不截断**,`bulk` 截断时必须显式写出"以下内容未包含"(`lib/index.js:1378-1420`)。
- 接续前先跑**刷新仪式**:向旧会话投一条 prompt,要求它 `memory_note(kind=plan)` 重写白板 + `memory_note(kind=handoff)` 写一份新账本,然后只回一句"已刷新"(`lib/index.js:6253-6261`)。

**E. 自动沉淀的写者与闸门**

`turn-stopping` → 600ms 后 `consolidateTurn`(`lib/index.js:17430-17434`)。跳过条件全部是硬判据:子代理会话、`autoConsolidate=false`、本轮 <240 字符、30 分钟冷却(22:00-08:00 翻倍)、每天 ≤8 次、同 turn 已处理(`lib/index.js:13269-13290`)。提炼由一个**子代理**做(`callSubagentStartPre`,兼容 `startActivation`/`start` 两代签名,`:1879-1918`),并登记进 `_ownSubagents` 防套娃。

最值得记的一条:[USER] 要点**不得直接进全局用户级记忆**。自动沉淀产出的用户级候选先写 `<userDir>/PENDING-USER-MEMORY.md` 等人工确认(`lib/index.js:13486-13501`;门槛函数 `lib/consolidate-filter.js:62-70`)。过滤层是纯函数、零 IO、零时钟,同输入逐字节确定(`lib/consolidate-filter.js:1-16`)——四类穿透(空壳变体/过程叙述开头/过短/重复)各有一条正则。

**F. 技能固化写进 DSH 自己的技能目录**

procedure 晋升到 `active` 后,自动导出 `SKILL.md` 到 **`<dshHome>/skills/`**,即 `~/.dsh/skills`(`lib/skill-export-host.js:28-40`)。这是 DSH `dsh-skill-filesystem` 四条发现根之一(本机对照:`dsh-skill-filesystem/lib/index.js:154,159,171,176` 分别是项目 `.dsh/skills`、项目 `.agents/skills`、`<dshHome>/skills`、`<agentsHome>/skills`)——**与 DSH skill 系统共用同一个目录,不是自己的私有格式**。导出物带 `mem-skill-` 前缀与自检标记 `mem-skill-export-pre-v1`,因此不会覆盖用户手写技能(`lib/skill-export-host.js:24-26`)。

三处只有踩过才写得出来的细节:①frontmatter 的 `name/description` 一律走双引号 YAML 序列化器,因为标题含 `: ` 时宿主解析抛错会**warn 后丢文件**、而插件自己的校验器还返回 `ok:true`(假绿)(`lib/skill-export.js:66-96`);②同一 procedure 改标题会多出一个目录,DSH 会把**两个版本都当有效技能加载**,所以落盘成功后清扫旧目录(`lib/skill-export-host.js:60-78`);③废弃(`deprecate`)时同步退役导出目录,否则"用户以为停用了、DSH 还在加载"(`:181-215`)。

**数据流(三条,别混)**:

```
① 主动召回(每轮,宿主发起)
   会话事件流 ──session/event──▶ runtime ──▶ 判定核(LR 工件 / 可选 e5 语义臂)
        └─命中─▶ 组包 ──pre-step claim(四重门)──▶ systemPrompt.context 固定尾巴
              ──▶ user 消息(历史尾部)──▶ 模型  ──返回非空──▶ markDelivered + seen 证据

② 自动沉淀(turn-stopping 后 600ms)
   本轮 user+assistant ──consolidateTurn──▶ 子代理提炼 ──▶ 今日日志(append-only)
                                              ├─▶ 项目笔记(升格)
                                              └─▶ PENDING-USER-MEMORY.md(用户级必须人工确认)

③ 水位 → 换窗口
   tokenMeter/窗口解析 ──▶ ratio ≥ 阈值 ──▶ arm 倒计时 ──▶ 刷新仪式 ──▶ 建新会话
        ──▶ 18 000 字符接续材料作为首条 user 消息 ──▶ 旧会话收到"已接续到 X"的队列消息
```

**测试**:443 个 `tests/smoke/*.mjs`、76 783 行,串行运行器零第三方依赖、每套件独立超时(`tools/run-smoke.mjs:1-32`,注释里记了"单个套件忙等 29 分钟使全量门失效"的实测)。与本卡四个问题直接对应的套件:

| 契约 | 套件 | 规模 |
|---|---|---|
| 注入两帧保真 | `smoke-test-inject-frame-fidelity.mjs` | 241 行 / 20 断言 |
| 固定边界尾注 | `smoke-test-m63.mjs` | 239 行 / 20 断言 |
| 三层注入预算 | `smoke-test-c5-tier-inject.mjs` | 282 行 / 77 断言 |
| 沉淀过滤 + [USER] 门槛 | `smoke-test-audit-g-consolidate-filter.mjs` | 214 行 / 30 断言 |
| 水位窗口/模型亲和 | `smoke-test-issue349-water-window-cache.mjs`(另有 `smoke-test-a08-model-window-affinity.mjs` 同契约) | 182 行 / 32 断言 |
| 续命事务 | `smoke-test-continuation-transaction.mjs` | 205 行 / 49 断言 |

两个套件我实跑过,`exit 0`(命令在末节)。测试风格是**带负控**的:`issue349` 有一条"删掉宿主调用后守卫失配"的断言,证明判据不是恒真守卫。

## 为什么它突出

**先拆星标,再谈下载。** 这是 memory 里"星标低、下载高"的典型样本,而且两个数都来自同一天:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-14 | 仓库创建 | GitHub API `created_at` |
| **2026-08-19** | **⚠ 16 星 / 3,782 次 npm 月下载** | `data/stars.json`、`data/downloads.json` |
| 2026-10-23 | 3.3.17(CHANGELOG 第 52 个版本标题) | `CHANGELOG.md` |
| 2026-10-31 | 当前 HEAD `a244cf0` | `git log -1` |
| 2026-11-12 | `pushed_at`(非 main 分支) | GitHub API |
| **2026-11-18** | **实时 204 星 / 19 fork / 36 open issues** | GitHub API |

采样点上,**下载/星标 ≈ 236 : 1**。这不是异常值而是使用形态的直接读数:它是一个"装上就不用管"的记忆插件,用户把它当依赖而不是当项目来 star;而 204 星是采样后 3 个月内长出来的(12.75×),同期 `19` fork 与 `52` 个版本标题说明它一直在被追。星标属于这个仓库本身——单条目仓库、无 monorepo 子目录、无母项目,归属没有歧义。

**零第三方提及,而且是"真的零"——但要求人工排除,`auto-memory` 这个词本身撞了通用名。** 4 条命中逐条判定:

| 命中条目 | 为什么不算 |
|---|---|
| `jayhchen/dsh-cc-auto-memory` | 描述里 `auto-memory` 只出现在**自己的仓库名/URL/icon 路径**里,正文讲的是 Claude Code 兼容的 `MEMORY.md` 索引注入 |
| `Bcy2020/dsh-cc-ecosystem` | 说的是"Claude Code 的 auto-memory 特性"被接进系统提示 |
| `Lovenndme/dsh-workspace-memory` | 说的是"布局仿 Claude Code 的 auto-memory" |
| `AskTheWay/dsh-auto-memory` | **另一个作者的同名仓库**(registry 里两条互不引用),不是本插件的衍生或 fork |

也就是说,`auto-memory` 在 2026 年的 DSH 生态里首先是**Claude Code 那个特性的名字**。用更窄的 token 复核:`grep -rl 'dsh-auto-memory' data/plugins/` 只有 2 条(它自己 + 上面那个同名仓库),`grep -rl '固定边界' data/plugins/` 只有 1 条(它自己)。**判断:零扩散的原因不是"没人用"(下载 3 782),而是①名字撞通用词、②条目自述里没有一个可被引用的概念名、③它以中文文档为主且 3 个月走完 52 个版本,外部很难在快速移动的接口上跟。**

**机制上的取舍是一句话:不把"想起来"交给模型,也不把"快满了"交给压缩。** 召回由宿主在 `pre-step` 决定(判定核是仓库里的一个 LR 工件,不是提示词),到水位就**开新会话并交接**(`lib/index.js:5612-5925`)——把"压缩"换成"换窗口 + 18 000 字符结构化交接"。后者的代价很硬(见下),但它换来一个性质:上下文满了不等于信息被摘要掉了。

## 代价与边界

失败模式按发生顺序(每条都有源码位置):

1. **写盘半截/丢更新**。三处状态文件曾是 `readFileSync → 改 → writeFileSync` 整写,并发时后写覆盖先写、中断时留半截 JSON 让读取端静默归零(`lib/path-write-queue.js:1-14` 自述)。现在统一 tmp+rename、按路径串行;Windows 下 `rename` 的 `EPERM/EBUSY` 走有界退避 `[0,50,150,400,1000]ms`(`lib/fs-retry.js:18-24`),而且**明确不做** unlink/copy 回退(会同时丢源与目标)。
2. **配置迁移窗口内写入落进旧根**。所有生产写通道挂同一道 admission:窗口内新写**明确拒绝**(409),窗口前已受理的写登记 flight 并等它落盘后才迁移(`lib/memory-mutation-transaction.js:6-30`)。数据目录改名(`-pre` → 裸名)的策略是"**失败朝重复,不朝丢失**":目标缺失或目标是空壳才复制,绝不覆盖已有真实数据(`lib/datadir.js:1-40`)。
3. **索引/文件变脏 → fail-closed,而症状在另一条路上**。记忆条目靠 `<!-- memory:mem_<32hex> -->` 锚点切分;一旦出现重复锚点,解析判 `dirty-file`,压缩链 fail-closed ⇒ **笔记永久写不进**(`lib/index.js:7821,7879,13587`)。这是本插件最阴的失败形态:报错发生在"写",但看起来像"记忆不生效"。
4. **水位误判有三种已记录的形态**,数字都在注释里:①窗口 fallback 到 131 072(真实 1 M)⇒ 470 572 被算成 180%;②会话自报 262 144 无条件盖掉 settings 的 1 000 000 ⇒ 同样 180%;③跨模型"借窗口"(新小模型 + 旧大模型窗口)⇒ 系统性低估 ⇒ 该触发时不触发(`lib/water-window.js:1-10,88-120,240-260`;`lib/index.js:5158-5172`)。修复方向是"声明冲突取大、硬墙取小"——误判"要炸"的代价高于误判"还早"。
5. **技能固化冲突**:改标题会留下多个 `mem-skill-*` 目录,DSH 同时加载两个版本(`lib/skill-export-host.js:64-70` 实测 3 个目录);退役/清扫靠四条件交集 + 删前重读复核(TOCTOU)。
6. **长会话注入重复/覆盖**:宿主一请求两帧,不设幂等闸就会出现"完整版被后一帧精简版覆盖"(`lib/index.js:17608-17620`);节流用内容指纹 + `snapshotMinGapRounds`,并区分"完整版间隔"与"精简版间隔"两个独立配置。
7. **接续没有事务性回滚**。`rollbackContSeq` 是**显式 no-op**——序号"允许空洞、永不回收",因为已预留的号可能已被别的消费者持有(`lib/index.js:5603-5606`)。接续失败只能进 pending 状态阻塞二次接续,并由 `lib/continuation-maintenance.js` 的人工 CLI(`complete`/`release`/`status`,必须带 `--confirmed-delivered` 或 `--confirmed-not-delivered`)恢复。**这是唯一一处"自动化承认自己需要人"的地方。**

其余边界:

- **成本是真的**。精简版每轮约 900 字符(注释里有实测:从 9 566 字砍到约 900,`lib/index.js:8198-8199`);自动沉淀每天最多 8 次**真实子代理调用**(`autoConsolidateDailyMax`),3.3.15 修好 `subagents.start` 之后"这项开销从静默失败、零成本变成真实花钱"(`lib/index.js:7418`)。语义档还要下模型资产(5 文件,e5-small q8,`lib/semantic-js.js:1-12`);Python 侧车装齐约 850 MB(`lib/index.js:400-402` 的卸载注释)。"零依赖"指的是零第三方 npm 运行库,不是零磁盘。
- **隐私**:记忆是明文 Markdown(`lib/index.js:344` 自述限制里明写),没有加密;插件会扫描其他 AI 工具的记忆目录(`memory_external`),但用"纯链接模式"——只写一条绝对路径指针,不抄内容(`:18590`)。73 条路由默认回环,私网白名单要四条同时满足。
- **维护成本**:52 个版本标题 / 2.5 个月,`CHANGELOG.md` 247 KB。功能开关高度解耦(水位、接续、白板、自动沉淀、语义档各自独立),但也意味着配置面很大(设置页按 `engine/memory/appearance/behavior` 分组,`lib/client.js:11650`)。

## 可信度与复现

- **★★★(宿主面机制)**:`lib/index.js` 的事件段、三个注入面、水位段、接续段、沉淀段逐段读过;`tier-layer-inject/tier0-catalog/activation-inbox/activation-host/procedure-store/skill-export*/water-window/handoff-anchor/consolidate-filter/plan-store/datadir/dsh-home/file-boundary/path-write-queue/fs-retry/memory-mutation-transaction/semantic-js/semantic-decide/l0-extract` 读过头部或关键段;两个 smoke 套件实跑 `exit 0`。
- **对照本机 DSH 官方实现**:`dsh-agent-loop`(runtime-context 投影/去重、preStep/step 两帧、`contextAdmitted`)、`dsh-system-prompt`(`context()`/`section()` 的 effect 形状)、`dsh-skill-filesystem`(四条技能发现根)。
- **未读**:`lib/client.js` 19 753 行(只读注释与路由表引用)、`python/` 7 个 `.py`、73 条路由的处理函数体、`docs/` 119 MB(513 个 md + 357 张 png,含论文/宣发/审计报告)。

```sh
# 1) 克隆 + 提交(仓库 357 MB,必须 blobless + depth 1)
git clone --depth 1 --filter=blob:none https://github.com/Aik358/dsh-auto-memory.git repo
cd repo && git log -1 --format='%H %ad %s' --date=iso
# a244cf03f6f409b655d86e02d6c0a7b86d7496f4 2026-10-31 17:26:21 +0800

# 2) 规模
wc -l lib/*.js | tail -1                    # 75564 total(115 文件)
wc -l lib/client.js                         # 19753(浏览器面)
ls tests/smoke/*.mjs | wc -l                # 443
wc -l tests/smoke/*.mjs | tail -1           # 76783 total
git ls-files | wc -l                        # 1772

# 3) 零第三方运行库(输出应只有 node: 内建)
grep -rhoE "from '[^']+'" lib/*.js | sed "s/from '//;s/'//" | grep -v '^\.' | sort -u
# node:crypto node:path node:fs node:fs/promises node:os node:child_process
# node:timers/promises node:async_hooks node:util node:url node:module node:zlib
# node:stream node:stream/promises node:sqlite node:readline node:https node:http

# 4) 固定边界三面
grep -n "systemPrompt.context(\|systemPrompt.section(" lib/index.js
# 17551(:10000 动态) 18294(:10000 静态) 18304(:10001 尾注)

# 5) 扩散(在 awesome-dsh-plugin 仓库根;必须用目录形式,11744 个文件会 Argument list too long)
grep -ril 'auto-memory' data/plugins/ | wc -l            # 5(含自身)
grep -ril 'auto-memory' data/plugins/                    # 4 条第三方,逐条判定见正文
grep -rl 'dsh-auto-memory' data/plugins/ | wc -l         # 2(自身 + 同名不同作者)
grep -rl '固定边界' data/plugins/ | wc -l                 # 1(只有它自己)

# 6) 实跑两个契约测试
node tests/smoke/smoke-test-audit-g-consolidate-filter.mjs   # 27 passed, 0 failed
node tests/smoke/smoke-test-issue349-water-window-cache.mjs  # 32 passed, 0 failed
```

## 待验证

1. **`pushed_at` 2026-11-12 对应哪个分支**。`main` 停在 2026-10-31,`git ls-remote` 显示还有 `preview`、`merge/pr-batch`、`v4-collaboration` 等 5 个分支。若 11 月有实质提交只在 `preview`,卡头日期会低估活跃度。
2. **73 条路由的处理函数体**。本卡只确认了回环/私网守卫的存在与四条同时满足的条件,没有逐条核每个写路由是"实际写哪个根、写前是否过 mutation admission"。
3. **`python/` 侧车(7 个 `.py`)在决策链中的权重**。默认 `activationSource='fake'`,JS 判定核是主路径;`python` 分支要过三重门。侧车不可用时降级路径是否真的等价,未验证。
4. **PENDING-USER-MEMORY.md 的人工确认入口**。写入侧(`lib/index.js:13486-13501`)确认了,确认之后如何晋升进 `~/.dsh/memory/MEMORY.md` 的 UI/路由未读。
5. **e5-small 语义档的实际收益**。资产 5 文件 SHA256 冻结、双源下载都在 `lib/semantic-js.js`,但没有 benchmark 数字;`docs/M7-EMBEDDING-BENCHMARK.md` 存在,未读。
6. **357 MB / 119 MB docs 的构成**。357 是 GitHub 仓库体积字段(含历史);工作树 151.8 MiB、`.git` 113 MiB。119 MB 的 `docs/` 里 357 张 png 只有 `screenshots/` 18 MB,剩下的分布在论文 HTML/宣发素材/审计报告,未逐个统计。
7. **204 星的增长曲线**。只有两点(08-19 的 16、11-18 的 204),中间没有采样;`stargazers` 带 `starred_at` 需鉴权,本次没拿到。
