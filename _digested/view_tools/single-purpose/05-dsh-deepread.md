# dsh-deepread — 五种模式共用「分段提炼 → 合并」流水线,外面套预算、缓存与后台任务

> 证据等级:★★★(源码级;`xiehuan123/dsh-deepread@9462f1e546b94a7f27e77abaf3d9ee3fedf7f746`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 20 为 2026-08-19 历史采样;下载 1,974 同为该日;2026-11-18 实时星标 71。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `xiehuan123/dsh-deepread`([registry](../../../data/plugins/xiehuan123__dsh-deepread.yml)) |
| 类目 | tools([census](../../../ecosystem/census.py) 1,639 条 / 全表 11,744 条) |
| 子分类 | `single-purpose`——它对外是一个工具,内部却是一整套可复用流程;这个张力见「为什么它突出」 |
| 自述 | 五种模式(快速/深度/知识地图/费曼/全书)精读图书与文章,输出观点—证据—数据报告、四档置信度、Mermaid/XMind 导图,支持批量对比、预算预检、后台任务进度与 MD/HTML 导出 |
| 星标 ⚠ | **20**(2026-08-19 采样);**2026-11-18 实时 71**(91 天 ×3.55)。仓库首个提交就是本插件,无宿主项目可分摊(见「为什么它突出」) |
| 下载 ⚠ | **1,974**(2026-08-19 采样,`data/downloads.json`);同日星标只有 20 |
| 扩散 | **0**(口径:`grep -ril 'deepread' data/plugins/` 命中 2 条 = 自身 + `HaoKuo__DSH-Paper-DeepRead.yml`;后者是 `paper_deepread`/`paper-deepread-html` 的工具名,与本插件无关。`grep -rl 'dsh-deepread'` 只命中自身) |
| 仓库 commit | `9462f1e5…`,2026-09-11 13:13 UTC,`fix: 明确真实 loader 测试版本边界并修正发行说明 (#13)`;main;GitHub **53 个提交**、4 个 release(v0.3.1→v1.0.1);仓库创建 2026-08-15 |
| 包形态 | npm `dsh-deepread@1.0.1`(共 12 个版本):`dsh.bundle.patch` + `dsh.client`(web)+ `dsh.skills`;Host 入口 `lib/types/index.js` |
| 代码规模 | `src/**/*.ts` **5,196 行**(host 3,985 / client 1,205,18 个文件,`wc -l src/host/*.ts src/client/*.ts`);`test/*.mjs` 3,408 行 / 29 个脚本;打包 skill 162 行;生成物 `lib/client.js` 61,476 字节;仓库 162 个 git 文件,GitHub size 10,962 KB |

## 它到底是什么

**一句话:不是配置包,也不是外部服务适配层,而是把「精读」这件事整个做进 DSH 的一个工具——LLM 由宿主注入,其余(抓取、PDF 解析、分块、清洗、缓存、预算、后台任务、导出)全部自带。**

五模式并不是五个产品,而是**同一条 LLM 调用骨架的五种参数化**,源码可以逐条对上:

```
resolveSource(输入)                       source.ts:161-248
  → splitChunks(段落切 6000 字/上限 20 段)  llm.ts:53-84
  → for 每段: callModelJson(模式 system + 该段)   plugin.ts:682-691
  → 压缩各段要点(每段只留 3 条 arguments)  plugin.ts:697
  → 1 次汇总 callModelJson(全文 schema)     plugin.ts:698
  → sanitize*(结构清洗) → DeepreadResult
```

| 模式 | 实际做什么 | 调用图 | 关键位置 |
|---|---|---|---|
| `quick` | 单次调用抓要点;输入截断 30,000 字;输出预算 2,500 token;prompt 限定 arguments/quotes/concepts/questions 各 ≤3/3/4/3 | 1 次 | `plugin.ts:176`、`:594-605` |
| `deep`(默认) | ≤9,000 字单次;超过则逐段 section 提取 + 1 次全文综合,输出 `structure` 与 `citations` | 1 或 N+1 次 | `plugin.ts:680-727`、`:186-197` |
| `book` | 与 `deep` 同一段代码,**只是强制走分段**(短文本也分) | N+1 次 | `plugin.ts:680`、`:722` |
| `map` | ≤9,000 字单次出知识地图;超过先分段做 section 提取,再把「各段要点」合成地图 | 1 或 N+1 次 | `plugin.ts:607-628` |
| `feynman` | >9,000 字先花 1 次调用读开头 5,000 字出目录与阅读问题;再逐段做「观点/数据/证据 + 章节导图 + 合上书讲解 + 找缺口 + 回原文修正」;最后 1 次合并全书导图、终讲与 5 个间隔的复习计划 | N+2 次 | `plugin.ts:630-678`、`:321-379` |
| `batch`(独立入口) | 2-10 篇,每篇 quick(≤30,000 字)+ 1 次跨篇对比;不进 `depth` 枚举 | M+1 次 | `plugin.ts:405-423`、`:475-519`、`:863` |

`depth` 不在枚举里的值一律归为 `deep`(`analysis.ts:34-36`);`batch` 是并列的 `batch[]` 参数,不是第六个模式。**「全书」在当前代码里与「长文深度」没有语义差别**,只是绕过「短文本也单次」的捷径。

**输入来源四种,各有硬边界**(`source.ts:161-248`):

- `url`:先按字符串切 host,**只允许 `mp.weixin.qq.com`、`weixin.qq.com` 及其子域**,其余直接抛错并提示粘贴正文(`source.ts:168-172`)。
- `path`:`.pdf` 走自写解析器;`.txt/.md/.markdown/.html/.csv/.json/.log` 走 Host 的 `fs.readText`(`:237-244`);HTML 复用同一套 `htmlToText`。
- `text`:原样作为来源,`source: '粘贴文本'`。
- `batch[]`:每项各自可带 `url/path/text/focus`,逐篇解析。

**输出格式是「会话内 Markdown + 可选三件落盘」**:默认 `none` 不写盘;`md`、`mm`、`html`、`all` 由 `attachExports` 写到 `deepread-output/`(`export.ts:626-657`)。`.mm` 是 FreeMind XML `<map version="1.0.1">`(`export.ts:406-416`),XMind 可导入——**没有 `.xmind` 二进制输出**;Mermaid 只以文本形式嵌在 Markdown/HTML 里(`export.ts:164`、`:495`),不负责渲染。

## 怎么接进 DSH

| 位置 | 内容 | 作用 |
|---|---|---|
| `package.json:61-64` | `dsh.bundle.patch: "./cordis.patch.yml"` | 唯一的 profile 层声明 |
| `package.json:65-71` | `dsh.client.platform: "web"` + `inject: [session-controller, ui-conversation]` | 浏览器 half 只在 Web 加载 |
| `package.json:72-74` | `dsh.skills: ["./skills/dsh-deepread/SKILL.md"]` | 同时发布一份可移植 skill |
| `cordis.patch.yml:1-4` | `insert: [{id: deepread, name: dsh-deepread}]` | 唯一挂载行,无配置、无门控 |
| `src/host/plugin.ts:67-68` | `name = 'deepread'`、`inject = ['fs','llm','tools','web','agentDefaultModel','sandboxPolicy']` | Cordis 插件名与依赖 key |
| `src/host/plugin.ts:70-72` | `apply` 先做 `isHostContext` 校验,不通过抛 `TypeError` | 拒绝空上下文 |
| `src/host/plugin.ts:1042` | `ctx.effect(() => ctx.tools.register(tool))` | 工具注册点 |
| `src/host/plugin.ts:1044-1066` | 读打包 SKILL.md、切 frontmatter、`skills.register` | skill 注册点;frontmatter 缺 `description` 直接抛错 |
| `src/host/plugin.ts:1140-1146` | `ctx.inject(['webServer'], registerBudgetRoute)`、`ctx.inject(['skills'], ...)` | 可选服务注入;没有就退回直接调用 |
| `src/client/index.ts:41-65` | `shell.overlay` / `conversation.input.left` / `tool.call.toolview`(key `deepread`) | 三处 UI:浮层面板、输入框按钮、工具结果卡 |

**没有命令、没有权限声明。** `dsh-plugin.json:13-18` 是 `permissions: []`、`contributes.commands: []`,Host 侧也没有 `ctx.commands` 注册;用户入口只有模型工具 `deepread`、skill、以及 Web 面板(面板把自然语言指令塞回对话,不直接调工具)。headless 与 dsh-TUI 只加载 Host 入口和 skill,不加载 `lib/client.js`(TUI 读 `dsh-plugin.json` 的 `facets.host.entry`)。

依赖关系是**反向**的:根 `package.json:76-83` 把 `@deepseek-ai/cordis`、`dsh-storage-domain`、`dsh-tools`、`schemastery`、`zod`、`react` 全列为 `peerDependencies`,自己不打包;`src/host/*.ts` 只 import `@deepseek-ai/dsh-tools` 的 `defineTool` 与 `@deepseek-ai/schemastery`/`zod`/`dsh-storage-domain`(`plugin.ts:7`、`config.ts:1`、`cache.ts:1-2`),并用 `as unknown as` 把签名降级为本地接口(`plugin.ts:63`、`config.ts:1`),以容忍上游 rc 期 API 漂移。安装:`dsh plugin --profile web add dsh-deepread`(`README.md:59`),可锁 `@1.0.1`(`README.md:139`)。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `src/host/plugin.ts` | 1,174 | 全部模式、prompt、工具定义、后台任务、路由、skill 注册 | `:155-379` 五套 JSON schema;`:521-728` 主流程;`:736-857` 后台;`:947-1035` 工具;`:1072-1138` 预算路由 |
| `src/host/llm.ts` | 235 | 分块、流式调用、JSON 修复与重试、自校准 | `:53-84` 分块;`:134-163` 调用;`:176-231` 重试;`:188-197` 校准采样 |
| `src/host/source.ts` | 266 | 四种来源、HTML→文本、微信抓取、缓存回退、PDF 采样 | `:106-159` 抓取;`:168-172` host 白名单;`:185-193` 旧缓存回退 |
| `src/host/pdf.ts` | 830 | 纯 JS PDF 文本提取:自写 inflate + ToUnicode CMap + 页树 | `:15`「纯 JS」;`:31` `inflateRaw`;`:806-814` 带页标记;`:817-826` 只采样 2 页 |
| `src/host/export.ts` | 671 | Markdown 渲染、FreeMind、HTML 报告、落盘 | `:129-173` 地图 MD;`:406-416` `.mm`;`:434-618` HTML;`:626-667` 写文件 |
| `src/host/budget.ts` | 76 | token/耗时估算与五模式调用图 | `:9-20` 分词口径;`:22-37` 时间公式;`:39-73` 各模式调用数 |
| `src/host/calibration.ts` | 119 | 实测速率/延迟的 EWMA 与持久化 | `:25-34` 模型默认表;`:108-116` 0.8/0.2 平滑 |
| `src/host/cache.ts` | 88 | 按 URL 缓存全文(存储域 + 内存兜底) | `:24-25` TTL 168h/上限 200;`:66-81` 过期与淘汰 |
| `src/client/view.ts` | 930 | 工具结果卡、预算面板、历史、拖拽 | `:515` `DeepReadCard`;`:581` `Panel`;`:766` `fetch('/api/deepread/budget')` |

**观点—证据—数据与四档置信度是「一次性 LLM 产物 + 结构清洗」,不是可验证链路。** 生成靠 `MAP_SCHEMA`(`plugin.ts:213-235`)与 9 条硬规则(`:242-251`):`items` 的 `type` 十选一、`relations.type` 八选一、`confidence` 四选一(作者原意/原文事实与数据/合理推断/无法确认),原文没证据时必须写「原文未提供证据」,`dataPoints` 必须带数值、时间、对象、基准、来源、位置,「严禁编造数据」「案例不得当普遍证据」「相关不得写成因果」。清洗在 `sanitizeMap`(`:265-318`):`items` 截 40 条、`relations` 截 6 条且 `to` 为空即丢、`dataPoints` 截 30 条且 `value` 为空即丢、`evidence` 缺省填「原文未提供证据」、`summary` 截 100 字。**没有任何一步回去核对 claim 的引文是否真的在原文里**:没有子串匹配、没有页码校验、没有二次模型评审。四档置信度因此是模型自评,`source` 字段也只是模型抄回的字符串(测试只钉住「`第3页` 不被改写」,`test/features.mjs:96-98`)。**判断:这套设计的可审计性上限是「格式一致」,不是「事实可追溯」。**

**预算 preflight 是三段式,且会自我校准。** 分词口径写死:中文 0.6 token/字、拉丁 0.25 token/字符、其他 0.5,外加每次调用 600 token 的 prompt 开销(`budget.ts:9-20`、`:3`);耗时 = `(输入+输出 token)/速率/60 + 调用数×单次延迟/60`(`:22-37`);五模式各自给出调用数与输出预算,`estimate:true` 时**零模型调用**(`test/features.mjs:72-74` 断言 5 行估算且 `calls=0`)。大 PDF 不读全文:只解结构与前 2 页,按「样本字/页 × 总页数」外推,并用样本的 token/字比例(`plugin.ts:566-575`、`pdf.ts:817-826`);原始字节 >2MB 才走采样(`source.ts:251-262`)。Web 面板的「预算预检」按钮走 `POST /api/deepread/budget`(`plugin.ts:1072-1138`),请求体上限 5MB(`:1156`),返回同一份五模式估算,面板内显示一行、不进对话。

校准来自真实调用:每次成功调用用「输出 token / 墙钟秒」算吞吐,EWMA `0.8/0.2` 平滑后写进 `deepread_stats` 存储域(`llm.ts:188-197`、`calibration.ts:19-23`、`:108-116`)。**但延迟这一半是退化的**:`generationMs = tokens / (tokens/elapsed) * 1000` 在代数上恒等于 `elapsedMs`,于是 `elapsedMs - generationMs` 恒为 0,落进 `latencyMs > 0` 的假分支,最终写入默认 800ms(`calibration.ts:110`)。也就是说「实测延迟」实际上从未被测到;`test/calibration.mjs:120` 只断言它是个数字,没抓住这一点。

**后台任务完全托管给官方 `jobs`。** 触发条件:批量恒后台(`plugin.ts:876`)、`path` 是 `.pdf` 且采样外推 > `backgroundMinChars`(默认 9,000,`:904`)、其他文本解析后 > 9,000 字(`:923`);`jobs` 不存在或 `jobs.start` 抛错就退回前台(`:877-886`、`:933-944`),不报错。`jobs.start` 的 spec 有 `kind:'deepread'`、`label`(形如 `deepread 精读「来源」· N 段 · 预算≈X分钟`,`:788`)、`outputLimitBytes: 256*1024`(对齐 `tool-terminal` 的读取上限,`:813-815`)、`owner`:`exec.agent`(`:816`)。返回的 hooks 只有 `cancel/done/readOutput`(`:800-808`),进度是往 `lines[]` 追加文本:PDF 每 5% 一行(`source.ts:226-229`)、「精读第 i/N 段」(`plugin.ts:686`)、批量逐篇三行(`:484-498`)、「汇总中」(`:696`),最后追加「【最终报告】」全文(`:831`)。取消:`job_kill` → `hooks.cancel` 置 `signal.aborted`,流式循环每收一个 chunk 检查一次并抛「任务已取消」(`llm.ts:148`),任务以 `status:'killed'` 结束(`plugin.ts:835-838`)。

**测试把契约钉在行为上,不钉 prompt 质量。** 29 个脚本由 `package.json` 的 `test` 串联,其中与本卡结论直接相关的是:`jobs-progress.mjs`(断言 `kind=background`、`jobId`、`label` 含段数、`outputLimitBytes=256KB`、进度含「精读第 1/2 段」「汇总中」「【最终报告】」、`readOutput` 读完清空,`:126-146`)、`features.mjs`(五模式估算行、`citations.source` 保真、批量 3 次调用,`:72-117`)、`budget-api.mjs`(路由注册与 JSON 返回,`:64-102`)、`calibration.mjs`(三次调用后 `calibrated=true`、重启后从 stats 域读回,`:107-133`)、`pdf-objstm.mjs`(对象流压缩 PDF 能抽出指定文本,`:73-76`)、`client-theme-contract.mjs`(四档置信度标签可见且用 `--dsw-alias-label-primary`,`:152-196`)、`client-smoke-preflight.mjs`、`packaged-skill.mjs`、`compatibility-baseline.mjs`、`data-identity-gate.mjs`。

## 为什么它突出

**星标归属没有歧义:20→71 全部属于这个插件。** 时间线可核:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-15 08:34 UTC | 仓库创建 | GitHub API `created_at` |
| 2026-08-15 | 首个提交 `feat: DeepRead 精读助手 v0.1.0（bundle 插件：deepread 工具…）`;同日 npm 0.3.7、release v0.3.1 | 提交列表 / npm registry |
| 2026-08-18 13:53 | `refactor: migrate deepread host to TypeScript`(`plugin.ts` 仅 3 个提交) | GitHub API |
| **2026-08-19** | **⚠ 20 星 / 1,974 下载采样**;`plugin.ts` 最后一次改动 14:42 | 边车 + 提交历史 |
| 2026-08-20 | release v1.0.0 | GitHub releases |
| 2026-09-09 / 09-11 | v1.0.1 / 最后一个提交 | releases + clone |
| 2026-11-18 | 实时 **71** 星、7 fork;npm 上周下载 1,010(本卡当日查 npm API) | GitHub / npm API |

仓库里没有第二个产品:README 的主体就是 DSH 插件与可移植 skill 两件事,没有「宿主项目带插件」的分摊问题。**所以这里不需要像 monorepo 子目录那样拆归属;需要解释的是「为什么星标不高」。**

三点判断,都基于本插件自身数据:

1. **它是工作流,不是一句 prompt,因此获客慢、留存重。** 同一条骨架长出 5 套 JSON schema(`plugin.ts:155-379`)、4 种导出、预算预检、后台任务、批量对比与 3 处 Web UI;一篇 12 万字的长文最多打 20 段 + 1 次综合的串行调用。用户要的是「读完一本书」,不是「试一下」——这类工具的自然扩散路径是口碑与二次使用,不是收藏。
2. **下载/星标比约 99:1(1,974 / 20),且采样只在发布后第 4 天。** 这说明它被**安装**的强度远高于被**关注**的强度;判断:npm 下载含 CI/镜像与多宿主安装,不能当作纯用户数,但至少说明「有人在用」而不是「只在榜上」。
3. **零扩散是结构性的,不是偶然。** 口径已写在「一屏事实」:唯一第三方命中是另一个插件的 `paper_deepread` 工具名,与本插件无关。原因有三:(a) 没有可依赖的库接口——对外只有一个 `deepread` 工具和一份 SKILL.md,没有导出函数、没有 service key;(b) 可复用的部分被刻意做成**文本工作流**(`skills/dsh-deepread/SKILL.md`,48 行,连 11 步费曼闭环与提示注入纪律都写在里面,`:25`、`:40`),别人抄的是流程,不会在 `data/plugins/` 里留下 token;(c) Host 代码绑死 DSH 的服务形状(`defineTool`、`ctx.effect`、`ctx.get('jobs')`),换宿主必须重写适配层。

**「精读工作流」而非单次摘要,是可以量化的**:五种模式对应 5 套互不相同的输出 schema,而不是同一份摘要换措辞;`map` 额外产出 10 类条目 × 8 类关系 × 4 档置信度 + 数据表 + 导图 + 回忆问题(`plugin.ts:213-235`);`feynman` 是 11 步闭环并以 5 个复习间隔收尾(`:363-379`);`batch` 是逐篇 + 跨篇冲突/互补矩阵(`:405-423`);前面还有预算预检、URL 缓存、后台任务与三种落盘格式。**这套「流程 + 契约 + 成本控制」的组合,才是它区别于「总结一下这篇文章」的地方。**

维护面则相反:**53 个提交、4 个 release 集中在 4 周内,9-11 之后冻结**,`docs/deepseek-harness-integration.md` 自述核对基线是 Harness `0.1.2-rc.1`(2026-09-10)。判断:它是一个完成度很高但**已停更**的实现,读它更像读一份「如何把长任务做成 DSH 工具」的参考实现,而不是在读一个持续演进的产品。

## 代价与边界

- **必须有可用模型。** `pickConfig` 先取 `agentDefaultModel`,没有就退到 `llm.listProviders()` 的第一个 provider/第一个模型(`llm.ts:107-132`);两者都空则直接抛「没有可用的模型 Provider」。没有任何离线/降级摘要路径。
- **串行执行,没有并发。** 三个分段循环都是 `for` + `await`(`plugin.ts:616-622`、`:644-649`、`:685-691`),批量也是逐篇(`:482-499`)。20 段 = 20 次串行 LLM 往返,墙钟时间 ≈ 20 × 单次延迟;换取的是不打爆限流、进度可逐段报告、取消能立刻生效。
- **成本上界是硬的,但截断是静默的。** 输入 > 400,000 字先切(`:589`);分段后 `parts.slice(0, MAX_PARTS)` 只取前 20 段(`:615`、`:642`、`:684`),**超出部分不分析、`meta` 里也不写 note**——120,000 字以上的书会丢尾部内容;`quick` 与批量每篇另有 30,000 字截断(`:595`、`:487`)。预算估算用的也是同一个 20 段上限(`budget.ts:45`),所以「预算准」和「内容全」在这里是同一个上限的两面。
- **JSON 是单点故障,重试预算有限。** 每次调用最多 3 次(`llm.ts:182`),失败/截断时输出预算 ×1.5、硬顶 16,000 token(`:177`、`:210`),并按失败类型换校正提示(`:212-218`)。全文综合仍解析失败时**不报错**,回退为第一部分要点并写 note(`plugin.ts:703-715`);`quick` 与 `map` 的最终解析失败则直接抛错(`:597`、`:626`)。**判断:长文最可能的结果不是失败,而是「拿到了一个只有第一章的完整报告」,note 是唯一线索。**
- **抓取只有微信一条路,且白名单在重定向之前。** Host 的 `web.fetch` 优先,失败后回退 Node 全局 `fetch` 并带浏览器 UA、`redirect: 'follow'`(`source.ts:109-129`);反爬验证页再换 UA 重试一次(`:142-156`)。白名单按 URL 字符串切 host(`:168-172`),**不校验重定向后的落点**——判断:这是本插件最实在的出网口子,`fetch` 之后可以落到任意域。抓取失败时若有旧缓存则回退并写 note(`:185-193`),否则原样抛错。
- **PDF 是自写解析器,能力有上限。** 读文件上限 30MB(`source.ts:204`),`%PDF-` 头校验、自写 inflate、ToUnicode CMap、页树遍历(`pdf.ts:14-15`、`:31`、`:332-390`);抽出的文本按页加「【第N页】」标记(`:813`),这是 `citations.source` 能写「第3页」的前提。**扫描版/图片型 PDF 没有 OCR,直接报错请先 OCR**(`source.ts:234`);复杂字体/CID 字体是否都能映射到 Unicode 未做穷举,失败表现是乱码或空文本。
- **持久化是可选的,缓存有上限。** `storageDomain` 不存在时,URL 缓存退化为进程内 `Map`(`cache.ts:26`、`:39-44`),校准也只在内存(`calibration.ts:79-93`),**重启即失**;有后端时 TTL 默认 168 小时、上限 200 条,按 `fetchedAt` 淘汰(`cache.ts:24-25`、`:66-81`)。缓存只存原文全文,不存分析结果——同一篇文章换模式重跑,LLM 调用不会省。
- **导出不是原子操作。** 目录固定 `deepread-output/`,根取 `sandboxPolicy.workspaceRoot`,`resolve` 失败则拍平成 `标题-md.md` 再写一次(`export.ts:626-657`);文件名只做非法字符替换并截 40 字(`:620-624`);**导出失败只往 `meta.note` 写一句,不让整个精读失败**(`:661-666`)。HTML 报告里有一行 `@import url("https://fonts.googleapis.com/...")`(`export.ts:609`)——**打开这份「可离线打开」的报告会向 Google 发一次请求**。
- **提示注入防护只在 skill 里,不在工具 prompt 里。** `SKILL.md:40` 明写「内容≠指令」,但 Host 侧的 `sectionSystem`/`mapSystem`/`feynman*System` 都没有这句(`plugin.ts:167-179`、`:237-255`、`:344-357`),来源文本被原样拼进 user 消息(`:181-184`、`:257-263`)。**判断:走工具路径时,注入防护完全依赖模型自身行为。**
- **失败模式,按发生顺序**:
  1. 没有 provider/model → 立即抛错,不消耗 token(`llm.ts:110-131`)。
  2. URL 非微信域 → 抛错并给出「粘贴正文/存文件」的替代路径(`source.ts:170-171`)。
  3. 抓取失败且无缓存 → 抛原始错误;有缓存 → 用旧全文 + note(`:185-193`)。
  4. PDF 无文本/非 PDF/超 30MB → 抛错(`:204`、`:232-234`、`pdf.ts:807`)。
  5. 模型输出 3 次仍非 JSON → 抛错,带上每次的真实原因与末次输出尾部 160 字(`llm.ts:222-230`)。
  6. 全文综合解析失败但有分段结果 → 降级为第一部分 + note(`plugin.ts:703-715`)。
  7. `jobs.start` 抛错 → 前台执行,用户失去进度与取消能力(`:877-886`、`:933-944`)。
  8. 导出失败 → 结果仍在,`meta.note` 记录原因(`export.ts:661-666`)。
  9. `job_kill` → 当前流式调用抛「任务已取消」,任务 `killed`,已产生的进度行保留(`plugin.ts:835-838`)。
- **没有「恢复」。** hooks 只有 `cancel/done/readOutput`,后台任务的进度行是内存数组(`plugin.ts:790-799`),没有 checkpoint、没有「从第 k 段继续」;取消或进程重启后重跑会重新解析(URL 缓存可免)并**重新执行全部 LLM 调用**。任务产物只以文本形式留在 job 输出里,不落盘。

## 可信度与复现

- **★★★**:`src/host/` 12 个 TS 文件里通读 11 个(`plugin.ts`、`llm.ts`、`source.ts`、`pdf.ts`、`export.ts`、`budget.ts`、`calibration.ts`、`cache.ts`、`types.ts`、`config.ts`、`analysis.ts`;`optional-storage.ts` 未读,只从其调用点推断)。另外通读 `src/index.ts`、客户端 `index.ts`、`package.json`、`cordis.patch.yml`、`dsh-plugin.json`、`plugin.json`、`skills/dsh-deepread/SKILL.md`、`docs/deepseek-harness-integration.md` 前 60 行、`README.md` 开头;`client/view.ts` 与 `pdf.ts` 中段只读关键段(卡片/面板/预算请求/抽取路径);测试只读 `jobs-progress.mjs`、`features.mjs` 的断言段,其余 4 个脚本(`calibration`、`budget-api`、`pdf-objstm`、`client-theme-contract`)按断言 grep 抽查。合计核心 20 个文件通读、约 7 个文件按需抽查。
- **未读**:`src/client/{store,storage,models}.ts`(客户端历史与拖拽状态)、`test/` 其余 25 个脚本的全文、`pdf.ts` 500-700 行的 xref/ObjStm 细节、`docs/` 与 `examples/` 的其余内容。**因此「UI 细节」「PDF 对复杂字体的覆盖率」本文没有结论。**
- 浅克隆只有 1 个提交(GitHub 上共 53 个),历史与 release 来自 GitHub API(2026-11-18 查询);npm 版本数/上周下载来自 `registry.npmjs.org` 与 `api.npmjs.org`(同日查询)。星标/下载的 ⚠ 值只来自 `data/stars.json`、`data/downloads.json`。

```sh
# 1) 提交与规模(浅克隆即可)
git -C .work/mine/cards/deepread/repo log -1 --format='%H %ad %s' --date=iso
# → 9462f1e546b94a7f27e77abaf3d9ee3fedf7f746 2026-09-11 21:13:19 +0800

wc -l src/host/*.ts src/client/*.ts | tail -1     # → 5196
wc -l test/*.mjs | tail -1                        # → 3408(29 个脚本)
wc -c lib/client.js                               # → 61476

# 2) 零扩散(在 awesome-dsh-plugin 根目录)
grep -ril 'deepread' data/plugins/ | wc -l   # → 2:自身 + HaoKuo__DSH-Paper-DeepRead.yml
grep -ril 'deepread' data/plugins/           # 确认第二条命中的是 paper_deepread 工具名
grep -rl 'dsh-deepread' data/plugins/ | wc -l # → 1(仅自身)

# 3) 边车取数
python3 - <<'EOF'
import json
for f in ('data/stars.json','data/downloads.json'):
    d=json.load(open(f)); print(f, d['https://github.com/xiehuan123/dsh-deepread'])
EOF
# → {'stars': 20, 'checkedAt': '2026-08-19'} / {'downloads': 1974, 'checkedAt': '2026-08-19'}

# 4) 实时数(2026-11-18 当日查,非采样)
curl -s https://api.github.com/repos/xiehuan123/dsh-deepread | grep -E 'created_at|pushed_at|stargazers_count'
curl -s https://registry.npmjs.org/dsh-deepread | python3 -c "import json,sys;print(list(json.load(sys.stdin)['versions']))"
curl -s https://api.npmjs.org/downloads/point/last-week/dsh-deepread

# 5) 关键机制抽查(行号可 sed 复核)
sed -n '68p;815p;1042p;1156p' src/host/plugin.ts
sed -n '170p' src/host/source.ts
sed -n '609p' src/host/export.ts
sed -n '148p;210p' src/host/llm.ts
```

## 待验证

1. **「恢复」到底能不能做**:`jobs.start` 返回的 hooks 只有 `cancel/done/readOutput`(`plugin.ts:800-808`)。需要读本机 `dsh-jobs` 的契约,确认 DSH 是否允许 job 在进程重启后重放/续跑;若允许,本插件也没有把分段索引写进 job 状态,重跑必然全量重来。这一条决定长书场景的可用性上限。
2. **延迟校准是不是真的恒为 800ms**:源码代数推导是 `elapsed - tokens/(tokens/elapsed) ≡ 0`,但未跑一次真实调用抓 `stats` 表里的 `latencyMs` 佐证;也没验证 `calibrated=true` 后时间估算是否可见地偏离。这是本文最可能被后续复核推翻的一条。
3. **重定向后的出网边界**:白名单只在字符串层校验(`source.ts:168-172`),`redirect:'follow'` 在 `:119-122`、`:146-150`。需要实测一个会 302 到非微信域的 URL(以及 Host `web.fetch` provider 是否也 follow),才能判断 SSRF 风险等级——本文只写了判断,没写结论。
4. **20 段截断是否有 note**:`parts.slice(0, MAX_PARTS)` 三处(`plugin.ts:615`、`:642`、`:684`)之后 `meta` 只带 `chunks`,没有截断标记。用一本 >12 万字的书跑 `book` 模式,核对报告是否覆盖末章、`meta` 是否仍显示完整——这决定「静默丢内容」是事实还是我的误读。
5. **四档置信度的实际分布**:没有标注样本,无法判断模型是否真按「作者原意/原文事实与数据/合理推断/无法确认」区分,还是多数落在「合理推断」。需要拿 `examples/` 的 3 篇对照原文人工标注,才能评价这套报告的可用性。
6. **XML/HTML 与字体**:`.mm` 的 FreeMind XML(`export.ts:406-416`)未在 XMind 里导入实测;HTML 的 Google Fonts 外链(`:609`)在离线环境下的降级表现也未测——README 宣称「可离线打开」,需要一次断网验证。
7. **跨 dsh-TUI 的真实装载**:`dsh-plugin.json` 声明 `manifestVersion 0.15`、`permissions: []`、`commands: []`(`dsh-plugin.json:3-18`),但本卡只读了清单与集成文档,没在 TUI 0.8.1 里实际装一次确认 skill 与工具都出现。
