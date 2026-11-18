# treg — 一页 SKILL.md 加一行 MCP 配置,替一个托管代理挂上 4,197 个外部接口

> 证据等级:★★★(源码级;`superdesigndev/treg@8f9d28d92c6a3549ca47fcdbe66050ea741b928b`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 477 为 2026-08-19 历史采样;该日下载无记录;2026-11-18 实时星标 8326。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `superdesigndev/treg`([registry](../../../data/plugins/superdesigndev__treg.yml)) |
| 类目 | tools([census](../../ecosystem/census.py) 1,639 条 / 全表 11,744 条) |
| 子分类 | `single-purpose`——⚠ 星标类内第一(477,第二名 zhaoolee/notes 147);但星标归属见「为什么它突出」 |
| 自述 | 给 Agent 的工具目录:按「要做的事」检索约 2,600 个外部接口(SEO/SERP、外链、社交、人物与公司补全、抓取),读参数与单次价格后直接调用,凭据由服务端注入;附 skill,加一行在 `TREG_TOKEN` 未设置前保持禁用的 MCP |
| 星标 ⚠ | **477**(2026-08-19 采样);**2026-11-18 实时 8326**(91 天 ×17.4)。两者都属于托管主项目,不属于 DSH 适配层 |
| 下载 ⚠ | **无记录**(2026-08-19 采样缺口:`data/downloads.json` 无此 URL;npm registry 查 `treg-dsh` 返回 404,本仓库没有 npm 下载面可统计) |
| 扩散 | **0**(口径:`grep -ril 'treg' data/plugins/` 命中 4 条,逐条人工判断后 3 条是用户名 `RestRegular` 里的 `tReg` 子串,剩下 1 条是自身) |
| 仓库 commit | `8f9d28d9…`,2026-11-18 03:16 UTC,`Merge pull request #1774 from superdesigndev/fix/localfalcon-price`;仓库创建 2026-07-15 |
| 包形态 | 根 `package.json` 就是 npm 包 `treg-dsh@0.31.0`(**未发布**,registry 404):`dsh.bundle.patch` → `dsh/cordis.patch.yml`;DSH 面 = 1 个 skill provider + 1 行远程 MCP |
| 适配层规模 | 手写 **150 行**(`dsh/index.js` 116 + `dsh/cordis.patch.yml` 34)+ 481 行**生成**的 `dsh/skills/treg/SKILL.md` |
| 主项目规模 | `src/**/*.py` 429 文件 / 129,464 行;`src/treg/catalog/*.yaml` 167 文件 / 165,517 行;**4,197 个 endpoint / 135 个 provider**;全仓 5,261 个 git 文件,GitHub 报 141,954 KB |

## 它到底是什么

**一句话:它不是插件,是一个商业托管代理的官方接入点——DSH 侧只负责"发一页说明书"和"开一扇门",门后面全是服务端。**

DSH 面只有三件事,源码可逐条确证:

1. **一页 skill**:`dsh/skills/treg/SKILL.md`(481 行)由 `scripts/build_plugin.py` 从 `src/treg/web/skill.md` 生成(`scripts/build_plugin.py:14-17`、`:75`、`:194-199`),`dsh/index.js` 把它注册成 `ctx.skills` 的一个 provider(`dsh/index.js:114-116`)。这页纸不需要 token,永远可用。
2. **一行远程 MCP**:`dsh/cordis.patch.yml:26-34` 用 DSH 自带的 `@deepseek-ai/dsh-mcp-client` 挂 `https://treg.to/mcp/`,`transport: streamable-http`,`Authorization: Bearer $TREG_TOKEN`;`disabled` 表达式在 `TREG_TOKEN` 为空时为真(`:28`),所以默认不挂。
3. **DSH 侧零业务代码**:`dsh/index.js` 里没有一次 HTTP 调用、没有一个工具实现,只有读文件、切 frontmatter、返回 `list`/`get`(`dsh/index.js:45-102`)。

真正的机制都在服务端。**目录是仓库里的 YAML,不是数据库里的黑盒**:`CATALOG_DIR` 指向包内 `src/treg/catalog/`(`src/treg/domain/catalog/store.py:31`),启动时 `yaml` 全量解析成进程内单例缓存(`store.py:299-306`),`core` 与 `extended` 两套文件用 `_core_first()` 排序、核心文件先解析(`store.py:310-312`)。一个 endpoint 行的形状(以 `src/treg/catalog/apollo.yaml:47-60` 为例):`id`、`capability`、`platform`、`scope`、`method`、`path`、`input`(参数 JSON Schema)、`cost`(计价)、`cache`、`test_request`。

**当前这份目录有多大,我数过**:167 个 YAML 里 162 个带 `endpoints:`,合计 **4,197 行 endpoint、135 个不同 provider**;`store.headline_counts()` 把非 routed 行数向下取整到百位再加 `+`(`store.py:1882-1894`),所以对 Agent 说的是 "4,100+ tools across 135 providers"(`dsh/skills/treg/SKILL.md:3`)。**registry 的「约 2,600」不是错,是过期**:2026-08-19 那个 commit(`19aa1493`)的目录是 68 个 provider 文件 / **2,631 行 / 47 个 provider**——正好是 "2,600+"。三个月里目录涨了 60%,条目描述没跟上。

**核心循环四步,每一步都有信任含义**:

```
catalog_search(任务词)  → 目录是本地进程内数据,不打网(store.py:299-306)
catalog_get(id)         → 参数 + 单次价 + 实测成功率/延迟(走内部 HTTP 路由补统计,mcp.py:1486-1500)
call(id, params)        → reserve(占用余额) → relay(注入凭据) → settle → archive
balance()/my_tools()    → 余额;以及"你自己的 key/连接/CLI/skill"(永不计量)
```

`call` 的入参同时支持 `params` / `query` / `body` / `form` / `uploads` / `headers` / `idempotency_key`(`src/treg/mcp.py:1577-1582`)。MCP 进程不是另起一个服务:它用 `ASGITransport` **直接调本进程的 ASGI 应用**(`mcp.py:84-87`,注释自称 "a function call wearing an HTTP shape"),所以 MCP 与 HTTP API 走的是同一套 `/call/` 逻辑,不存在两套计费。

## 怎么接进 DSH

**manifest 是 `package.json` 的一个键,不是 `plugin.json`**(`docs/DSH-PLUGIN.md:14-20` 明说 dsh 不读 `plugin.json`)。下表与全文里的 `package.json` / `dsh/*` 都相对仓库根;凡写 `dsh-xxx/lib/index.js` 的,一律指本机安装包 `$DSH/node_modules/@deepseek-ai/dsh-xxx/lib/index.js`(复现命令里给了 `DSH=`):

| 位置 | 内容 | 作用 |
|---|---|---|
| `package.json:12-16` | `dsh.bundle.patch: "./dsh/cordis.patch.yml"` | 唯一被 dsh 识别的声明;`dsh-app-boot` 用它判断"这是 profile 层" |
| `package.json:2,7-11` | `name: treg-dsh`、`files: [dsh/index.js, dsh/cordis.patch.yml, dsh/skills]` | 包名就是 patch 行里 `name: treg-dsh` 解析的目标;`files` 刻意不带 Python |
| `dsh/cordis.patch.yml:19-21` | `id: treg-skill` / `name: treg-dsh` | 挂 `dsh/index.js` 的 Cordis 插件 |
| `dsh/cordis.patch.yml:26-34` | `id: treg-mcp` / `name: '@deepseek-ai/dsh-mcp-client'` | 远程 MCP 行 |
| `dsh/index.js:105-107` | `export const name = 'treg-skill'`、`inject = ['skills']` | Cordis 插件名与依赖的服务 key |
| `dsh/index.js:114-116` | `ctx.skills.registerProvider(() => provider)` | 唯一注册点 |

**`disabled` 的机制是真的,不是装饰**:bundle 行的 `disabled` 允许布尔或 `!!js` 表达式(`dsh-app-boot/lib/index.js:3020-3022` 的 schema,`:3147` 的 `anyOf`),patch 文件里允许 `!!js`(`:3934`);求值在启动时进行,`enabledEntry()` 把**抛异常也算作 disabled**(`:3917-3921`)。`!!js` 的求值环境有 `process`——DSH 自己的 `dsh-base/cordis.patch.yml:251` 就是 `disabled: !!js process.platform === 'win32'`,treg 抄的是同一个形状。所以"设了 `TREG_TOKEN` 就出现工具"依赖两条:环境变量在 **dsh 启动时**已在,**并且**那行确实被重新求值——后者只在重启时发生(`docs/DSH-PLUGIN.md:40-41` 自己写明)。

**为什么非要这道门**:`dsh-mcp-client` 的 streamable-http transport 只传 `requestInit.headers`,没有 `authProvider`(`dsh-mcp-client/lib/index.js:46`)——它能发静态 Bearer,但**不会跑 OAuth**。而 treg 的 `/mcp/` 要 Bearer。若行常开而 token 缺失,就是 14 个永远 401 的工具。作者把这条推理写进了 patch 注释(`dsh/cordis.patch.yml:9-13`)与 `docs/DSH-PLUGIN.md:24-35`。

**skill 这一半是纯配置的对照物**:`dsh/index.js` 手写 provider,而不是依赖 `@deepseek-ai/dsh-skill-filesystem`——理由是"out-of-tree bundle 依赖 in-box 包会装第二份、随后与宿主漂移"(`dsh/index.js:15-19`)。形状与 DSH 自带 `dsh-skill-badge` 完全一致(对照 `dsh-skill-badge/lib/index.js:24-50`):`source: 'bundled'`、`rank: 600`(`dsh/index.js:27,83-85`;常量在 `dsh-skill/lib/index.js:23`)。

**这条 `rank: 600` 有个实际后果**:DSH 的 skill 优先级按 rank 升序,`~/.agents/skills`(用户级)是 500、bundled 是 600(`dsh-skill-filesystem/lib/index.js:20-24`、`:173-185`;排序在 `dsh-skill/lib/index.js:520`)。而 treg 的安装脚本 `src/treg/web/install.sh` 会跑 `treg skill bootstrap`,把**同一页**写进 `~/.agents/skills/treg/`(`dsh/skills/treg/SKILL.md:39-41` 自己提醒)。两者同名时 rank 低的先赢,所以真正常用的是磁盘那份,bundle 里这份被遮住——同样的内容,不冲突,但 bundle 的 skill 行在那种环境下等于空转。作者知道,选择"提一句而不改"。

**安装只有一条路**:`dsh plugin --profile <p> add github:superdesigndev/treg`(`docs/DSH-PLUGIN.md:9-11`)。npm 上 `treg-dsh` 是 404(我查了),所以**没有版本区间可锁**,`dsh plugin add` 取的是 GitHub 上的源码;这也解释了为什么 `dsh/index.js` 必须是"无构建步骤的纯 ESM"(`dsh/index.js:11-14`,pnpm 拒绝跑 git 依赖的 `prepare`)。

## 关键实现

**DSH 侧只有三个文件,全在这里**:

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `dsh/cordis.patch.yml` | 34 | 唯一机制载体:两个 `insert` 行 + 一个 `!!js` 门 + 一个远程 URL | `:19-21` skill 行、`:26-34` MCP 行、`:28` 门 |
| `dsh/index.js` | 116 | 手写 skill provider(`list`/`get`、frontmatter 解析、`resourceBase`) | `:45-58` 解析 description、`:66-71` 读文件、`:73-102` provider、`:114-116` 注册 |
| `dsh/skills/treg/SKILL.md` | 481 | 生成物:两态开头的说明书(有 token / 没 token) | `:1-4` frontmatter、`:8-21` 分支判断 |

**契约测试钉住了三件事**(`tests/test_plugin.py:289-333`):`dsh.bundle.patch` 必须存在且指向真实文件、`files` 里每一项必须存在、`type` 必须是 `module`(`:293-301`);不得有 `prepare`、不得有任何 `dependencies`(`:303-313`);patch 里必须含 `disabled: !!js (process.env.TREG_TOKEN ?? '') === ''`,且**禁止 `!!js !`** 开头(`:315-333`)。最后那条是真踩过的坑:表达式以 `!` 开头会让 YAML 把第二个 `!` 读成又一个 tag 属性,整个 profile 报 "duplication of a tag property"(`tests/test_plugin.py:322-326`、`dsh/cordis.patch.yml:23-25`)。

**服务端侧,四个模块撑起产品**:

- **目录与检索**:`catalog_search` 是唯一入口(`mcp.py:1058,1072`),`limit` 上限 25(`:1110`),排序来自 `application/catalog_search.py` 的"lexical 排名 + 可选 LLM judge",judge 有**每调用方每小时上限**(`catalog_search.py:48-49`、`:243-244`)。`catalog_get` 走内部 HTTP 路由,为的是带上实测成功率与同 capability 的兄弟行(`mcp.py:1486-1500`)。
- **价格元数据**:`cost_view()` 把 provider 自己的计价单位换算成 USD——真货币走 `fx.yaml`、`credit` 走 `credit_rates_usd`、`unit` 走 `unit_rates_usd`;未知就是 `None` 而**不是 0**,因为"不知道"与"免费"不能混(`store.py:156-196`)。`advertised_usd()` 决定 `catalog_search` 报哪个数(搜索一次的价,不是线性切片,`:231-245`)。
- **凭据注入**:注入器是一张按 `injector` 名注册的表,一个 binding 只描述"往 header / query / 顶层 JSON 字段放哪个 secret"(`src/treg/infra/upstream/injectors.py:1-14`);代理层**不对鉴权形状分支**。relay 公开列出它只改六类东西(hop-by-hop 头、treg 自己的 `x-treg-*`、注入的凭据、共享 key 下的 `Idempotency-Key`/`User-Agent`/HMAC 客户码),其余逐字节转发(`src/treg/infra/upstream/relay.py:1-40`)。
- **计费与限流**:调用前 `reserve` 占住余额,结束 `settle`,异常/超时/取消都要"恰好一次"地结或释放。注册送 $1(`src/treg/config.py:309-310`,`promo_grant_micro: 1_000_000`,注释说够约 1,600 次 catalog 调用);默认 `platform_margin = 0.0`,即按供应商原价转收(`config.py:306-307`)。每条 provider 一个容量为 1 的令牌桶做突发平滑,最多等 2 秒,超了就照常发(`src/treg/infra/upstream/limiter.py:1-33`,`:21`);拿不到上游连接则直接 `503 upstream_busy` 且**不计费**(`src/treg/application/call/service.py:398-400`);上游返回 `retry-after` 只有 ≤5 秒才重发一次(`service.py:424-425`)。

**超时是一串数字,记住两个**:代理自己的上游超时 **180 秒**(`config.py:316`,注释说 BrightData 同步抓取要 20-35 秒、有的商户路由 9→105 秒);连接池等待 2 秒、建连 10 秒(`config.py:322-323`);routed 子调用 30 秒(`config.py:565`);检索 judge 2.5 秒、`/catalog/find` 6 秒(`config.py:613,621`)。**而 DSH 侧 `dsh-mcp-client` 的单次工具调用默认 60 秒**(`dsh-mcp-client/lib/index.js:765,788`),treg 的 patch 没有覆写这一项。60 < 180,这是这份集成里最实在的一条缝(见「代价与边界」)。

## 为什么它突出

**先拆星标归属:8326 星属于 treg 这个托管产品,不属于 DSH 适配层。** 时间线是决定性的:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-07-15 | 仓库创建,`Initial import: tools-registry (pre-release, private)` | 完整历史首提交 `a25061cc` |
| 2026-07-16 | PyPI `tools-registry` 0.1.0 | PyPI JSON API |
| 2026-08-15 | `931a5356 feat(plugin): add the DeepSeek Harness bundle` | **`dsh/index.js` 全部历史,只有这 1 个提交** |
| **2026-08-19** | **⚠ 477 星采样**;目录 2,631 endpoint / 47 provider | registry + 该 commit `19aa1493` |
| 2026-10-27 | `eb4c5c76 docs(plugin): dsh's token gate rests on its MCP client…` | `dsh/cordis.patch.yml` 的**第 2 个也是最后一个**提交 |
| 2026-11-07 | 第一个 GitHub Release `v1.0.0-beta.1` | releases API(全仓只有 3 个 release,都在 11 月) |
| 2026-11-18 | 实时 **8326** 星;目录 4,197 / 135 | GitHub API + 当前 clone |

三点可直接核:**(1)** 采样时 DSH bundle 只存在 4 天,477 星里能归给它的最多是 4 天增量;**(2)** 从采样到 8326 星的 91 天里,`dsh/index.js` **零改动**、`cordis.patch.yml` 只在 10-27 加了一段注释——适配层完全没动,星标照涨 17.4 倍;**(3)** 仓库主页 `README.md`(521 行、35 KB,星标落地页)**一次都没提 dsh / DeepSeek**(`grep -in 'deepseek\|dsh' README.md` 零命中),DSH 只在 `plugin/README.md:7-13` 的"五个橱窗"里被一句带过。同期真正在动的是主项目:5,115 个提交、目录 2,631→4,197、PyPI 39 个版本、799 个 fork、339 个未关闭的 issue/PR。

另一个必须点破的计数假象:`git log -- dsh/` 会给出 **222 个**提交,看着"很活跃";按文件拆开是 `dsh/index.js` 1 个、`dsh/cordis.patch.yml` 2 个、`dsh/skills/` **221 个**——后者全是 `scripts/build_plugin.py` 的再生成(provider 数/价格变了就重刷)。**适配层的真实变更次数是 2,不是 222。**

**再解释零扩散。** 口径与筛选:在 `data/plugins/` 内 `grep -ril 'treg'` 命中 4 条,逐条看内容——`data/plugins/RestRegular__dsh-pocket.yml:1-2`、`data/plugins/RestRegular__dsh-memory--packages-dsh-memory.yml:1`、`data/plugins/RestRegular__dsh-skill-center.yml:1-2` 三条里的 "treg" 全部来自**作者名 `RestRegular` 的 `tReg` 子串**,正文与描述都没提 treg;排除后第三方提及为 **0**(大小写敏感 `grep -rl 'treg' data/plugins/` 只命中自身 1 条,可交叉验证)。所以这不是"少",是"没有"。

四个理由,按解释力排序:

1. **没有可仿制的代码。** 150 行里 34 行是 YAML,116 行是"读一个 md 文件并返回"。没有任何算法、没有可扩展的 seam、没有本地能力。抄它只能抄出"指向同一个 `https://treg.to/mcp/`"的配置,不构成新条目。
2. **价值 100% 在服务端,而且是要付费的。** 4,197 行目录、代理、注入器、hold/settle、归档,都在一个托管服务后面;要复现得重建 129,464 行 Python 加 135 个 provider 的商务关系。衍生只剩两种形态:换个 harness 再包一层(无新意),或者直接用同一家服务(那不是新条目)。
3. **它是 vendor-published integration,不是社区 primitive。** 作者自己的定位是"五个橱窗,一个来源"(`plugin/README.md:3-13`):Claude Code / Cursor 一个文件夹、Codex 一个 manifest、`skills/` 给 `npx skills add`、MiniMax skills-only、DSH 是 npm bundle。五个面共用同一份 `src/treg/web/skill.md`,差别只在开头那段 bootstrap(`scripts/build_plugin.py:5-17`、`:194-199`)。这类条目的"扩散"指标本来就不适用——它的对等物是**渠道数量**,不是第三方衍生。
4. **它要联网、要账号、要钱。** 免费额度只有 $1,用完之后任何调用都指向充值;一个连不上商业服务的适配层,不会被别的项目当依赖抄走。

**判断:这是"明星",不是"锚"**——按本册两轴口径,声量(477 ⚠ / 8326 实时)属于宿主产品,扩散为 0。它在 DSH 生态里的位置是**一家商业服务的官方接入点**,而不是被本领域认可、被第三方复用的机制。类内"⚠ 星标第一"这个说法成立,但它量的是 treg 这家公司,不是这一行 MCP 配置。

## 代价与边界

- **必须联网,且必须有一个 treg 账号。** DSH 侧没有任何降级实现:断网、`treg.to` 故障、token 过期,14 个工具全部不可用;skill 给的替代路径是 `curl https://treg.to/install.sh | sh` 加 `treg login`(`dsh/skills/treg/SKILL.md:23-27`),同样要联网。
- **失败模式,按发生顺序**:
  1. **没设 `TREG_TOKEN`** → MCP 行 `disabled` 为真,工具列表里干脆没有 `mcp__treg__*`;skill 仍在,模型会按 SKILL.md 的两态分支走 CLI 路线(`dsh/skills/treg/SKILL.md:8-21`)。安装看起来是成功的。
  2. **设了但没重启 dsh** → 门是启动时求值的(`dsh-app-boot/lib/index.js:3917-3921`),这一轮仍然没有工具。文档明写要重启(`docs/DSH-PLUGIN.md:40-41`)。
  3. **token 无效/过期** → 14 个工具都在,每次调用 401;错误文本是 treg 自己的 `not authenticated` + 去哪取 token(`src/treg/mcp.py:791-802`)。没有 OAuth 兜底(`dsh-mcp-client/lib/index.js:46`)。
  4. **单次调用超过 60 秒** → DSH 侧先超时(`dsh-mcp-client/lib/index.js:765,788`),而 treg 允许 180 秒(`config.py:316`)。**判断:客户端放弃时余额可能已经被 settle**——treg 的不变量是"hold 恰好结或释放一次",但它没承诺客户端断开就等于取消。慢接口(BrightData 同步抓取 20-35 秒,商户路由到 105 秒)正好卡在这条缝上,DSH 里 patch 未覆写 `toolCallTimeoutMs`,要改只能改自己的 profile 层。
  5. **余额不足 / 不在额度内** → 调用前拒,402 类错误,不发起上游请求;注册只送 $1(`config.py:309-310`)。
  6. **上游拥塞** → `503 upstream_busy`,**不计费**(`service.py:398-400`);突发限流最多等 2 秒然后照发(`limiter.py:20-21`),所以 429 仍可能透传给你。
  7. **`retry-after` 很长** → 只有 ≤5 秒才自动重发一次(`service.py:424-425`),其余原样返回。
- **隐私:哪些数据出网。** 出去的:检索词(以及开启 judge 时,检索词会进一次 LLM 判定,`catalog_search.py:243-244`)、`call` 的路径/查询/请求体/你自带的 header、`feedback`/`review`/`mark` 的文本(明确是发给 treg 团队的,`mcp.py:1297-1330`)。**结果也会留在服务端**:catalog 的答案按保留策略进归档(`src/treg/archive.py:1-25`),且 **treg 自有 key 上的答案被当作 "public"**——别的团队问同一个问题时可以直接被服务你的答案;自有 key 的答案按 org 隔离,只在 endpoint 声明 `cache.sharing: public` 时跨团队(`archive.py:11-16`、`store.py:703-707`)。团队可以退出归档(`src/treg/models.py:154` 的 `archive_opt_out_at`),但退出是"不被服务也不再记录",不是"删掉已存的"。token 只存在你的环境变量与 DSH profile 的环境里,不落 treg 侧;但**每一次调用都在对方账上**。
- **供应链**:包不在 npm(404),只能 `github:superdesigndev/treg`,**没有 semver 可锁**;根 `package.json` 的 `version: 0.31.0` 只用于标识。skill 是生成物,内容随目录与价格漂(`dsh/skills/` 221 个提交就是它在漂)。许可证是 **Apache-2.0 + Additional Terms**(`LICENSE:1-12`,含托管服务限制),GitHub 因此报 `NOASSERTION`,而 `package.json:33` 简写成 `"Apache-2.0"`——对外分发时要按前者读。
- **维护成本与版本耦合**:DSH 侧耦合得很松——不 import 任何 `@deepseek-ai/*`、纯 ESM、无依赖、无构建(`tests/test_plugin.py:303-313` 把这条钉死),所以"DSH 升级会不会断"的风险主要在别处:**它依赖的是 treg 服务端的工具名与 `/mcp/` 契约,不是 DSH 版本**。服务端一旦改名或改路径,skill 里写死的 `mcp__treg__catalog_search` / `__call` 就会失效(`dsh/skills/treg/SKILL.md:13-16` 直接列了这五个名字);而仓库里 `/mcp/` 与 `/mcp/v2/` 是**故意不统一**的两套(`AGENTS.md` 的 "Working agreement"),v2 的工具集还绑着 Claude 目录的提交状态。这层风险 DSH 侧无法通过读源码发现,只能靠实际调用。

## 可信度与复现

- **★★★(DSH 适配层与本文引用的服务端模块)**:`dsh/` 三个文件、根 `package.json`、`scripts/build_plugin.py`(DSH 段)、`tests/test_plugin.py:285-369`、`docs/DSH-PLUGIN.md`、`plugin/README.md` 全读;服务端读了 `src/treg/mcp.py`(工具定义、`_need_token`、ASGI 说明、检索实现)、`domain/catalog/store.py`(加载、定价、headline)、`infra/upstream/{relay,injectors,limiter}.py`(头注释与关键常量)、`application/call/service.py`(retry/busy 段)、`archive.py`(头注释)、`config.py`(超时/赠金/余量常量)、`models.py:154`。
- **对照本机 DSH 源码**(`dsh-app-boot` 的 `disabled` schema 与 `enabledEntry`、`dsh-mcp-client` 的 transport/命名/超时、`dsh-skill` 的 `registerProvider` 与 rank、`dsh-skill-filesystem` 的根与 rank、`dsh-skill-badge` 的同形 provider)属于证据,不算搬别卡。
- **未读**:`src/treg/` 129,464 行里的绝大部分——`application/call/settle.py`(1,511 行)只读了注释级的结/释语义,`resolve.py`(2,721 行)、`route.py`(2,063 行)、`application/catalog_find.py`(763 行,judge 的实际请求)未读;`frontend/`、`tests/`(339 个文件)除 `test_plugin.py` 的 DSH 段外未读。**所以"检索准不准""judge 发了什么"这类判断本文一律没下。**

```sh
# 1) 克隆与提交(仓库 77 MB,blob 过滤后够用)
git clone --depth 1 --filter=blob:none https://github.com/superdesigndev/treg.git /tmp/an-treg
cd /tmp/an-treg && git log -1 --format='%H %ad %s' --date=iso
# → 8f9d28d92c6a3549ca47fcdbe66050ea741b928b 2026-11-18 03:16:34 +0000

# 2) 适配层就是三个文件、631 行,其中手写 150 行
find dsh -type f | xargs wc -l        # 34 + 116 + 481

# 3) 目录规模(需要 PyYAML;4,197 与 135 就这么来的)
python3 - <<'EOF'
import glob, yaml
tot = 0; provs = set()
for f in glob.glob('src/treg/catalog/*.yaml'):
    d = yaml.safe_load(open(f))
    if isinstance(d, dict) and isinstance(d.get('endpoints'), list):
        tot += len(d['endpoints']); provs.add(d.get('provider'))
print(tot, len(provs))                # → 4197 135
EOF

# 4) 采样日的目录(2,631 / 47)—— registry 的 "~2,600" 的出处
git fetch --unshallow --filter=blob:none
C=$(git rev-list -1 --before='2026-08-19T23:59:59Z' main)   # 19aa1493
git archive $C src/treg/catalog | tar -x -C /tmp/cat-aug19  # 把第 3 步的 glob 指向 /tmp/cat-aug19/src/treg/catalog 再跑一遍

# 5) 适配层的真实变更次数(注意 222 是假象)
git log --oneline -- dsh/ | wc -l                 # 222
git log --oneline -- dsh/index.js | wc -l         # 1
git log --oneline -- dsh/cordis.patch.yml | wc -l # 2
git log --oneline -- dsh/skills/ | wc -l          # 221(生成物)

# 6) 零扩散(在 awesome-dsh-plugin 根目录,不要展开 11,744 个文件)
grep -ril 'treg' data/plugins/ | wc -l      # 4
grep -ril 'treg' data/plugins/              # 3 条 RestRegular + 自身
grep -rl  'treg' data/plugins/ | wc -l      # 1(大小写敏感,只剩自身)

# 7) DSH 侧机制核实(本机安装的 dsh)
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh
grep -n 'disabled: { anyOf' $DSH/node_modules/@deepseek-ai/dsh-app-boot/lib/index.js
grep -n 'function enabledEntry' $DSH/node_modules/@deepseek-ai/dsh-app-boot/lib/index.js
grep -n 'requestInit: { headers' $DSH/node_modules/@deepseek-ai/dsh-mcp-client/lib/index.js
grep -n 'DEFAULT_TOOL_CALL_TIMEOUT_MS = ' $DSH/node_modules/@deepseek-ai/dsh-mcp-client/lib/index.js
grep -n 'BUNDLED_SKILL_RANK = ' $DSH/node_modules/@deepseek-ai/dsh-skill/lib/index.js
grep -n 'USER_AGENTS_RANK = ' $DSH/node_modules/@deepseek-ai/dsh-skill-filesystem/lib/index.js
```

## 待验证

1. **60 秒 vs 180 秒到底怎么收场**:挑一个已知要跑 60-180 秒的 endpoint,经 DSH 调用后看该次调用是否仍被 settle(需要真实付费调用 + 查余额)。这决定"超时"是丢时间还是丢钱。
2. **`/mcp/` 到底注册几个工具**:我按 `@mcp.tool` 装饰器静态数出 **14**(`catalog_search`、`catalog_request`、`feedback`、`review`、`mark`、`hub_create`、`hub_update`、`hub_mine`、`catalog_get`、`call`、`call_media`、`resources_list`、`balance`、`my_tools`),`/mcp/v2/` 是另一个 FastMCP 实例(`@directory_mcp.tool`)上 6 个 `directory_*` 工具;未跑运行时 `tools/list`(需要 token)。hub 相关三个是否受 `TREG_HUB_ENABLED` 条件注册,也未实测。
3. **`dsh plugin add github:…` 的实际解析**:pnpm 把 git 依赖装成 `treg-dsh` 之后,`name: treg-dsh` 这一行是按 profile 的 `node_modules` 解析还是按别的规则——我没跑安装(`dsh plugin add` 会写 profile)。若解析路径不同,这 150 行就连不上。
4. **星标曲线**:`stargazers` API 需要认证(我实测未授权返回 401),所以 477→8326 的**形状**只有起止两点加中间里程碑,不能排除"某一天暴涨"。要证实"与 DSH 无关"还需 star-history 或带 `starred_at` 的采样。
5. **归档的默认共享面**:`archive.py` 的头注释说自有 key 的答案按 org 隔离、平台 key 的答案 public,`cache.sharing: public` 只能逐 endpoint 声明;但我没跑一次"换团队问同一个问题"的实测,也没查部署默认的 `TREG_ARCHIVE_*` 取值。
6. **judge 究竟发了什么**:`catalog_search` 在实验开启时会把检索词交给一次 LLM 判定,`catalog_find.py`(763 行)未读,所以"检索词是否只用于打分、是否落库"没有源码结论。
7. **`~/.agents/skills/treg` 遮蔽 bundle 的影响**:rank 500 < 600 是源码事实,但"被遮住后用户的 treg skill 是否仍是同一份内容"取决于 `install.sh` 何时跑过、跑的是哪个版本;未做实测。
