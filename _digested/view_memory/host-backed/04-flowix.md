# flowix — 宿主自己就是一份 DSH 发行版,这 380 行只是给它的 agent 开一个 memo 抽屉

> 证据等级:★★★(源码级;`text2future/flowix@aad249469246ed180ae41e3fd01110245447fb0b`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 320 为 2026-08-19 历史采样,属**主项目**(桌面应用)而非本适配层;2026-11-18 实时 **518**。下载:边车无记录,且 npm 未发布(404)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `text2future/flowix#dsh-flowix-memory`([registry](../../../data/plugins/text2future__flowix--dsh-flowix-memory.yml)) |
| 类目 | [memory](../../ecosystem/census.py)(504 条) |
| 子分类 | `host-backed`(外部应用适配);本册星标第 4 |
| 自述 | 「将本地 flowix-cli 注册为 MCP 服务,让 agent 可以搜索、读取、创建和编辑 Flowix 备忘与思维导图产物」 |
| 星标 ⚠ | **320**(2026-08-19 冻结;2026-11-18 实时 **518**,fork 65)。**属主项目**:桌面应用本身,见"为什么它突出"的时间线 |
| 下载 ⚠ | **边车无记录**;npm `dsh-flowix-memory` 返回 404,README:35-36 自述"not yet published to npm" |
| 扩散 | **0**(口径:`grep -ril 'flowix' data/plugins/` 命中 **1** 条,即本条自身) |
| 仓库 commit | `aad24946`(2026-11-15,`main`);仓库创建 2026-05-25,`main`,AGPL-3.0,GitHub `size` 94 215 KB |
| 包形态 | **不是 npm 包,是 monorepo 里的一个目录 bundle**:`dsh.bundle.patch` → 16 行 `cordis.patch.yml`,一行 `insert` 挂 DSH 自带 `@deepseek-ai/dsh-mcp-client` |
| 适配层规模 | `dsh-flowix-memory/` 共 **380 行**(patch 16 + launcher 162 + schema 54 + README 116 + package.json 32);patch 有效配置 **9 行** |
| 工具面在哪 | 不在这个目录里:真正的 MCP server 是 Rust `app/flowix-cli/src/mcp.rs` 778 行 + 同目录 `collection_store.rs` 1683 / `path_store.rs` 351 / `operation.rs` 259 / `plugin.rs` 135 = **3 206 行** |

## 它到底是什么

**先纠正一个方向。** 本册其他条目是"DSH 插件去接一个外部系统";这一条反过来:**宿主项目自己发行 DSH**。`dsh/upstream.lock.json:2-3` 把 DeepSeek Harness 钉在 `477b4f420553e8a52c2fbccc464d7561b239c443`,桌面端下载签名归档、校验 SHA-256 与 minisign、装进版本化目录,再以 stdio 子进程形态拉起 DSH(`app/flowix-desktop/src/dsh.rs:1-8`、`:1470-1504`)。Flowix 的 `flowix` profile 里固定挂三个 bundle:`@deepseek-ai/dsh-base`、`dsh-appserver`(自有 App Server,同仓)、`dsh-flowix-memory`(`dsh.rs:677`、`scripts/build-dsh-prod.mjs:59`)。**所以这个条目是一个厂商在自己发行的 DSH 里给自己应用开的一扇门,不是社区做的通用适配器。**

应用本体是 Tauri 2 桌面笔记应用(Rust 后端 + React 19 前端,`CLAUDE.md` 架构段),自述是"探索 AI Agent 工作空间"(`README.md:2`),核心是让 AI agent 往工作区写的笔记可浏览、可编辑。

**记忆对象是四种,全部落本地磁盘:**

- **memo(笔记)** — 就是 Markdown 文件。定位键是 `(notebook_id, relative_path)`,`types.rs:6-12` 明说"索引不为笔记生成独立 ID";frontmatter 是文件头的 `---\n…\n---` YAML 块(`frontmatter.rs:36` 的正则),持久属性有 `flowix_key`/`tags`/`favorited`/`icon`/`colors`/`properties`(`types.rs:43-70`)。
- **address** — agent 侧唯一句柄,格式 `<notebook-id>::<notebook 内相对路径>`,也接受绝对路径;绝对路径必须落在某个已注册笔记本根下,否则 `note is outside configured notebooks`(`path_store.rs:12-31`);相对路径按段校验,`..`/空段/以 `/` 开头一律拒(`path_store.rs:38-47`)。
- **notebook(笔记本)** — 一个被注册的目录,注册表在 `~/.flowix/db/local.db`(`paths.rs:14-22`)。根目录用 `FLOWIX_HOME` 覆盖(`paths.rs:29-31`);不传 notebook 时用"当前选中 → 默认"兜底,都没有就是 `no notebook is configured`(`store.rs:74-89`)。
- **collection(集合)** — 表 / 混合 / 媒体库 / 工作文档四类,定义是一个 YAML 文档,`collection.read` 返回原始 payload,`collection.query` 返回带 `address` 的记录(README:68-79)。混合集合必须带 `notes` 域才接笔记。
- **artifact(插件产物)** — 思维导图为例:`id: mindmap`、`format: markdown`、`directory: .flowix/plugin/mindmap`、`renderer: markmap`、`parser: mindmap-markdown`(`app/flowix-plugin-runtime/src/lib.rs:17-22`、`:28-56`)。写入的是 `<notebook>/.flowix/plugin/mindmap/*.md` 隐藏产物 + 一份用户可见的"指针笔记"(`lib.rs:1-5`,注释原话:validates it, writes the hidden artifact, and creates the user-facing Flowix pointer note)。

**检索**不是向量,是 SQLite 笔记索引:每次 CLI 调用先 `reconcile_note_index_blocking` 按 stat 增量对账,再走 `search_with_tag_filter`(`path_store.rs:207-214`;`store.rs:37-40` 的注释解释了为什么跨进程必须每次对账)。`flowix-cli` 的依赖里没有 HTTP 客户端,只有 `rusqlite`(`app/flowix-cli/Cargo.toml:14-27`)。

## 怎么接进 DSH

**manifest 只有两行是契约。** `package.json:27-31` 写 `"dsh": { "bundle": { "patch": "./cordis.patch.yml" } }`;`files` 只发四个文件,patch 之外没有任何入口代码(`package.json:7-12`),没有 `main`、没有 `exports`。DSH 侧认这两个键:`dsh-app-boot` 的 `bundlePatchFiles()` 校验 `dsh.bundle.patch` 必须是字符串或字符串数组否则抛错(`dsh-app-boot/lib/index.js:517-520`),`bundlePatchPaths()` 把相对路径拼到包目录(`:530`);`dsh-plugin-manager` 用它判断"这是不是 profile 层",并对没有 `dsh.bundle` 的包警告 `not a profile layer`(`dsh-plugin-manager/lib/index.js:336`、`:339`)。

**patch 全貌**(`cordis.patch.yml:8-16`,16 行里 7 行是注释):

| 字段 | 值 | 说明 |
|---|---|---|
| `insert` | 无 `id` 的列表 | 追加到根条目表。`applyEntryPatches` 里 `else data.push(...insert)`(`dsh-app-boot/lib/index.js:74-90`);匹配不到目标的 patch 只 warn 不报错 |
| `id` / `name` | `dsh-flowix-memory` / `@deepseek-ai/dsh-mcp-client` | 用 DSH 自带插件,不自研(`:9-10`) |
| `serverName` | `flowix` | 决定工具公开名:`mcp__flowix__memo`(`dsh-mcp-client/lib/index.js:96-102` 的 `publicToolName`) |
| `transport` | `stdio` | |
| `command` | `!!js process.execPath` | node 自己;`!!js` 由 `dsh-app-boot` 注册成 YAML tag(`:20-26`),求值时 `with (ctx) { eval(expr) }`(`cordis-plugin-loader/lib/index.js:233-238`),所以 `process` 是 DSH 进程的 global |
| `args` | `DSH_PROFILE_DIR + '/node_modules/dsh-flowix-memory/launcher.mjs'` | **本卡最脆的一行**,见"代价与边界" |
| `env` / `cwd` / 超时 | 全部没写 | 走 mcp-client 默认:`env {}`、`cwd ""`、`toolCallTimeoutMs 60000`、`failOnStartupError false`(`dsh-mcp-client/lib/index.js:766,786-789`) |

**`DSH_PROFILE_DIR` 不是 DSH 给进程设的。** 它由 `dsh-shell-env` 注册给**模型 shell 调用**(`dsh-shell-env/lib/index.js:22`、`:89-94`),官方 skill 文档写得很直白:"set in every shell call of a profile-launched Harness and **absent when the Harness was booted without a profile**"(`dsh-agent-preset/skills/cordis-plugin-development/SKILL.md:34`)。而这行 patch 在**配置装载时**求值,读的是 DSH 进程自己的 `process.env`。真正把它塞进 DSH 进程环境的是 Flowix 自己:`app/flowix-desktop/src/agent_external/deepseek_harness/host_registry.rs:36-43` 与 `dsh.rs:1500-1503` 显式 `.env("DSH_PROFILE_DIR", …/profiles/flowix)`。**这条 bundle 只在 Flowix 拉起的 DSH 里成立。**

**安装路径两条,代价不同:**

1. 产品路径:桌面端把 `dsh-flowix-memory` 拷进 `$DSH_HOME/profiles/flowix/node_modules/` 并跟 `package.json` 的 `dsh.profile.bundles`、`cordis.patch.yml` 一起做事务式替换/回滚(`dsh.rs:440-500`);`flowix` profile 名被占用且 `name != dsh-profile-flowix` 时直接拒绝,不覆盖用户配置(`dsh.rs:444-455`)。
2. 手动路径:`dsh plugin --profile flowix add ./dsh-flowix-memory`(README:40)。`dsh plugin` 不是插件市场,`bin.js:116-118` 把剩余参数**原样转发给 pnpm**,且 `--profile` 是 `requiredOption`——所以这只是 pnpm 装一个本地目录。

**环境隔离两头都在削。** DSH 的 stdio 传输用 `scrubbedParentEnv()`:凡名字匹配 `/KEY|PASSWORD|SECRET|TOKEN/i` 或以 `DSH_` 开头的变量一律不传(`dsh-subprocess/lib/index.js:13,32,52`),再由 mcp-client 合并 spec 的 `env`(`dsh-mcp-client/lib/index.js:25-31,43`);Flowix 给 DSH 子进程的白名单更窄,只放 PATH/HOME/TMPDIR/LANG 与代理变量(`dsh/environment.rs:5-31`)。本 patch 的 `env` 是空的,launcher 能活下来纯粹因为 `PATH`、`HOME` 不在剥离名单里。

## 关键实现

**DSH 侧四个文件,加一个不在目录里的 Rust server:**

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `dsh-flowix-memory/cordis.patch.yml` | 16 | 唯一 manifest 载体,一行 `insert` | `:8-16`;有效配置 9 行 |
| `dsh-flowix-memory/launcher.mjs` | 162 | 找 CLI → 透明代理 stdio → 找不到时**冒充**一个 MCP server | `:23-48` 探测、`:75-95` 代理、`:97-158` 兜底 |
| `dsh-flowix-memory/memo-tool-schema.json` | 54 | 单一工具的入参 schema,24 个属性、17 个 action | `:6` action 枚举、`:33-53` 条件必填、`:53` `additionalProperties: false` |
| `dsh-flowix-memory/package.json` | 32 | `dsh.bundle.patch` + `files` 白名单 | `:7-12`、`:27-31` |
| `app/flowix-cli/src/mcp.rs` | 778 | **真正在跑的 MCP server**,行分隔 JSON-RPC 循环 | `:23-64` 循环、`:83-95` 工具定义、`:97-155` 调用 |
| `app/flowix-cli/src/path_store.rs` | 351 | 地址解析 + 笔记 CRUD / 搜索 | `:12-50`、`:177-210` |
| `app/flowix-cli/src/collection_store.rs` | 1683 | 集合读取(只读) | `:16-54` |
| `app/flowix-cli/src/operation.rs` | 259 | 传输无关的 `FlowixOperation` 枚举 | `:6-40` |
| `app/flowix-plugin-runtime/src/lib.rs` | 1026 | mindmap / webpage 产物运行时 | `:17-56`、`:418` |

**这个 bundle 最硬的一处设计:JSON Schema 是跨语言的单一事实源。** `mcp.rs:84-86` 用 `include_str!("../../../dsh-flowix-memory/memo-tool-schema.json")` 把**这个目录里的文件**在 Rust 编译期嵌进二进制。也就是说:dsh-flowix-memory 和 flowix-cli 共享同一份 schema;文件挪走或改名,Rust 端**编译失败**,不是运行时才崩。反过来,桌面端用 `launcher.mjs` 是否存在当"profile 装好了没"的探针(`dsh.rs:314-320`),打包校验则把 `dsh-flowix-memory` 列进禁运清单、只给 `dsh-profile/flowix/node_modules/` 下那一份开例外(`scripts/verify-flowix-package.mjs:19-29`)。

**数据流(一次工具调用):**

```
模型 → mcp__flowix__memo(action:"search", …)
  └─ dsh-mcp-client(stdio)→ node launcher.mjs(本 bundle)
       ├─ 找到 CLI → spawn flowix-cli mcp,把 stdin/stdout 直接对接(launcher.mjs:75-95)
       │    └─ mcp.rs:97-155 → validate_argument_keys(:157-190) → operation::execute
       │         └─ path_store / collection_store / plugin → ~/.flowix + 各 notebook 目录
       └─ 找不到 → 内置假 server(只实现 initialize/ping/tools/list/tools/call)
            └─ tools/call 恒返回 isError:true + 安装提示(launcher.mjs:140-150)
```

**工具面是一个工具、17 个 action,不是 17 个工具。** `notebooks`/`list`/`tags`/`show`/`search`/`create`/`edit`/`write`/`delete` + `collection.{list,describe,query,read,add-note}` + `artifact.{list,describe,create}`(`memo-tool-schema.json:6`)。多路复用的代价是**模型必须记 action 名**;收益是新动作不改工具清单,`tools/list` 永远只回一个(`mcp.rs:54`)。

几处只有读源码才知道的约束:

- **参数键白名单是硬拒绝**,不是忽略:任何不在 24 个键里的参数会返回 `memo does not accept argument <key>`(`mcp.rs:157-190`)。
- **`action` 与旧 `command` 互斥**(`mcp.rs:113-117`);旧形态 `{command, stdin}` 仍收但标 deprecated(`memo-tool-schema.json:30-31`),且 `command` 会被 `reject_shell_syntax` 扫一遍 shell 元字符(`|`、`;`、`&&`、`>`、`<`、反引号、`$(`、`${`)(`mcp.rs:641-652`),`help`/`--version`/前导 `flowix` 也拒(`:406-418`)——**从模型侧无法把工具变成任意 shell**。
- **`--file` 一律拒**:MCP 读不到客户端本地路径,只能用结构化 `content`(`mcp.rs:448-451,483-487,579-583,596-600`)。
- **结果同时给文本和结构化**:`content[0].text` 是 `Flowix <action> (<address>)` 一行摘要,`structuredContent` 才是完整对象(`mcp.rs:674-697`)。
- **协议版本**:接受 `2024-11-05`/`2025-03-26`/`2025-06-18`/`2025-11-25`,不回显未知版本(`mcp.rs:12-18,66-70`)。
- **破坏性声明**:`annotations: { readOnlyHint: false, destructiveHint: true, idempotentHint: false }`(`mcp.rs:93`)——delete 和 edit 走同一个工具,DSH 侧无法按动作分级授权。

## 为什么它突出

**先拆星标,这是本卡的核心。** GitHub 只有仓库级星标,registry 把 `text2future/flowix` 的 320 记在一个子目录条目头上。时间线:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-05-25 | 仓库创建 | GitHub API `created_at` |
| 2026-07-15 | **可见历史的唯一根提交** `chore: release 1.0.6`(全仓 643 个提交) | `git rev-list --max-parents=0` |
| 2026-08-18 00:35 | `0e05144e feat(dsh): expose Flowix memos to the agent via MCP` — 第一次出现 DSH + 这个 bundle(当时在 `app/flowix-dsh-host/bundles/dsh-flowix-memory/`) | 该提交 stat |
| **2026-08-19** | **⚠ 320 星采样点** | registry 边车 |
| 2026-08-23 16:12 | `c128deaa feat: package Flowix DSH host and memory plugin` — bundle 移到仓库根 | 该路径首次 `A` |
| 2026-08-23 | 同日 `62301a4a chore: finalize desktop repository split` 删掉整个 `app/flowix-dsh-host/`(含 `config/flowix.cordis.yml` 与 `tests/bundle-sync.test.ts`) | `--diff-filter=D` |
| 2026-08-29 | `436bb687 feat(dsh)!: remove @flowix/dsh-flowix-bridge bundle` | 提交标题 |
| 2026-11-15 | `aad24946` 最后一次提交 | `git log -1` |
| 2026-11-18 | 实时 **518** | GitHub API |

**320 星里能归给这层的,是 1 天,不是 320 天。** 采样点距第一个 DSH 提交 **1 天**、距根目录这个 bundle 存在 **−4 天**(它还没被创建)。这 320 星是桌面应用在 2026-05-25→2026-08-18 的 85 天里攒的。**判断:320 与 518 都应记在 Flowix 主项目名下,不记在 DSH 适配层。** 追加一条反向证据:全仓三份 README 只有英文版有这一节(`README.en.md:61-71`),中文 `README.md` 里 `grep -i dsh` **零命中**——作者自己也没把它当卖点。

**再解释零扩散。** `grep -ril 'flowix' data/plugins/` 命中 1 条,就是它自己。三个理由,按解释力排序:

1. **不可迁移的依赖。** 工具的另一头是 `flowix-cli`,它是 Tauri 桌面 app 的 sidecar(`CLAUDE.md` 架构段),不在 npm、不在 PyPI、不在 PATH 默认位置;launcher 的前两个候选是 `/Applications/Flowix.app/Contents/MacOS/flowix-cli` 与 `~/Applications/...`(`launcher.mjs:27-42`)。没有这个 app,插件连假 server 都只剩一句安装提示。**别人抄走 16 行 YAML,得到的是一个指向自己没装的程序的空壳。**
2. **接口是私有的,不是可收敛的。** 对外只有一个 `memo` 工具,入参是 action 字符串 + 24 个键,地址语法是 Flowix 自己的 `<notebookId>::<path>`(`path_store.rs:52-54`)。这套东西没有第三方能对着实现一份——它连"记忆的通用原语"(recall/remember)都没有,只有笔记本 CRUD。
3. **形态上是 vendor 的内部接线,不是生态件。** `package.json` 里 `publishConfig.access: public` 与 `repository` 都写好了,但 npm 至今 404、README:35-36 自述未发布;它现在的分发渠道**只有**"装 Flowix 桌面端"和"从 checkout 里 `dsh plugin add ./…`"两条。

**判断:明星,不是锚**——而且这个"明星"的光还是主项目的。它在 DSH 侧真正的独特性不在适配层,而在**反向的宿主关系**:一个桌面应用把 DSH 当运行时发行、自己钉上游 commit、自己发签名归档,再把自己应用的数据面作为 MCP server 挂回去。这件事的工程量在 `dsh.rs`(2 106 行)+ `dsh/*`(655 行)+ 打包脚本里,不在这 380 行里。

## 代价与边界

按发生顺序:

1. **`DSH_PROFILE_DIR` 缺失 → 整条 patch 指向 `undefined/node_modules/...`。** `undefined + '/x'` 在 JS 里是字符串 `"undefined/x"`,node 找不到模块,mcp-client 起不来,工具消失。**判断**(未实跑):Flowix 拉起的 DSH 有注入,所以产品内正常;而 README:38-41 教的手动 `dsh plugin --profile flowix add ./dsh-flowix-memory` 之后直接 `dsh --profile flowix` 启动,进程环境里没有这个变量——这条路大概率是坏的。这是**文档教了一条只在自己产品里成立的路**。
2. **CLI 没装 → 工具还在,调用必败。** launcher 兜底 server 继续响应 `initialize`/`tools/list`,把 `memo` 列出来,`tools/call` 返回 `isError: true` 加一句安装指引(`launcher.mjs:126-150`,安装地址 `flowix-memo.com/latest.json` 只以字符串出现,`INSTALL_URL` 在 `:12`)。好处是模型能读到"为什么不能用";坏处是**工具列表看起来完全正常**,误判成环境问题的概率很高。
3. **显式覆写写错就彻底静默。** `FLOWIX_DSH_MCP_CLI` / `FLOWIX_CLI_PATH` 只要非空,`findCli()` 立刻 `return isExecutable(...) ? … : undefined`(`launcher.mjs:23-25`)——**不再回退 PATH**。一个过期的绝对路径能把这个工具关掉,而机器上的 `flowix` 明明可用。
4. **CLI 中途崩 → launcher 跟着退出。** `child.once('exit')` 直接把退出码搬过来(`:91-94`)。mcp-client 的 reconnect 默认开着(`enabled: true`,500 ms 起、上限 30 s、最多 10 次,`dsh-mcp-client/lib/index.js:434-439`),会重启 launcher;10 次之后工具掉线。
5. **路径类失败是清晰的**:越界绝对路径 → `note is outside configured notebooks`(`path_store.rs:28-30`);坏地址 → `must be a notebook-relative Markdown path`(`:44-46`);`FLOWIX_HOME` 指错 → `no notebook is configured`(`store.rs:88`)。这类错误会以 `isError` 结构化返回,不是异常。
6. **超时用默认 60 秒。** patch 没写 `toolCallTimeoutMs`,mcp-client 默认 `6e4`(`:766,788`)。`collection.query`/`collection.add-note` 在大会话库上要现算索引对账(`path_store.rs:207`),60 秒是唯一护栏,且不可按工具细分。
7. **隐私:这一层不出网,但"本机"范围比工作区大。** launcher 全文只有一个 URL 字符串、无 fetch(`grep -n 'fetch\|http' launcher.mjs` 只命中 `:12`);`flowix-cli` 的依赖里没有 HTTP 客户端。但 agent 拿到的是**整个 `~/.flowix` + 所有已注册笔记本**,不是当前工作目录——DSH 的 sandbox 管不到 MCP server 内部的文件访问。另外 Flowix 桌面自带 Cloud 同步引擎(`app/flowix-sync/src/lib.rs:1-5` "Flowix Cloud authentication and synchronization engine"),同步一旦开启,被 agent 改过的笔记会进同一个云通道;**这不是本 bundle 的行为,但它是这些数据实际会走的路**。
8. **维护负债已经有一处**:`cordis.patch.yml:6-7` 的注释让后来者"保持与 `config/flowix.cordis.yml` 同步,`tests/bundle-sync.test.ts` 守着漂移"——**这两个文件在 2026-08-23 被同一个提交删掉了**,现在全仓 `grep` 零命中。注释没跟着改,守漂移的测试也没了。

## 可信度与复现

- **★★★(本 bundle + 它在 DSH 里的装载路径)**:`dsh-flowix-memory/` 五个文件全读;`app/flowix-cli/src/mcp.rs` 778 行全读;`path_store.rs`、`store.rs`、`paths.rs`、`plugin.rs`、`operation.rs`(头 40 行)、`collection_store.rs`(头 54 行)按需读;`app/flowix-plugin-runtime/src/lib.rs`(前 200 行);`app/flowix-desktop/src/dsh.rs` 的 profile 安装段与测试段;`dsh/environment.rs` 全文;`host_registry.rs` spawn 段;`scripts/verify-flowix-package.mjs`、`scripts/dsh-dev-profile.patch.yml`、`dsh/upstream.lock.json`。
- **对照 DSH 官方源码**(允许的旁证):`dsh-app-boot`(patch 语义、`!!js`)、`cordis-plugin-loader`(表达式求值)、`dsh-mcp-client`(schema 默认值、工具命名、重连)、`dsh-subprocess`(env 剥离)、`dsh-shell-env` 与 `cordis-plugin-development/SKILL.md`(`DSH_PROFILE_DIR` 的真实作用域)、`lib/bin.js`(`plugin` 转发 pnpm)。
- **未读**:`flowix-core` 的 `memo_file/`(17 974 行,只读了 `types.rs`/`frontmatter.rs` 的关键段)、`collection` 模块的 YAML schema、`dsh-appserver`(804 K,同 profile 的另一个 bundle)、`flowix-web` 前端、`app/flowix-sync` 的云协议。**凡涉及"笔记同步/索引质量"的判断都只到接口层。**

```sh
# 1) 克隆 + 提交(94 MB,浅克隆即可;要看历史再 unshallow)
git clone --depth 1 --filter=blob:none https://github.com/text2future/flowix.git /tmp/an-flowix
cd /tmp/an-flowix && git log -1 --format='%H %ad' --date=iso
# → aad249469246ed180ae41e3fd01110245447fb0b 2026-11-15

# 2) 适配层 380 行、patch 有效 9 行
find dsh-flowix-memory -type f | xargs wc -l | tail -1      # → 380
grep -vE '^\s*#|^\s*$' dsh-flowix-memory/cordis.patch.yml | wc -l   # → 9

# 3) 工具面在 Rust 里
wc -l app/flowix-cli/src/mcp.rs app/flowix-cli/src/collection_store.rs \
      app/flowix-cli/src/path_store.rs                        # → 778 / 1683 / 351
grep -n 'include_str!' app/flowix-cli/src/mcp.rs              # → :84 指向本 bundle 的 schema

# 4) 零扩散(在 awesome-dsh-plugin 仓库根;注意 data/plugins 有 11744 个文件,
#    必须用目录形式,直接展开会 Argument list too long)
grep -ril 'flowix' data/plugins/ | wc -l                      # → 1(只有它自己)
grep -ril 'flowix' data/plugins/                              # → …/text2future__flowix--dsh-flowix-memory.yml

# 5) 星标归属时间线(两次 API,一次 git)
curl -s "https://api.github.com/repos/text2future/flowix" | grep -E 'created_at|stargazers_count'
# → created_at 2026-05-25 / stargazers_count 518
curl -s "https://api.github.com/repos/text2future/flowix/commits?path=dsh-flowix-memory&per_page=100" \
  | grep -c '"sha"'                                            # → 16 个提交
git fetch --unshallow --filter=blob:none && git rev-list --max-parents=0 HEAD
# → daa0c308… 2026-07-15(可见历史只有 643 个提交,更早的看不见)
git log --diff-filter=A --format='%h %ad %s' --date=iso -- dsh-flowix-memory/cordis.patch.yml

# 6) npm 侧确实没有
curl -s -o /dev/null -w '%{http_code}\n' https://registry.npmjs.org/dsh-flowix-memory   # → 404
```

## 待验证

1. **`DSH_PROFILE_DIR` 在独立启动时到底空不空**:跑 `dsh --patch ./dsh-flowix-memory/cordis.patch.yml --dump-config`,看 `args` 求值结果是不是 `undefined/node_modules/...`。这是把"失败模式 1"从判断变成事实的唯一一步。
2. **`dsh plugin --profile flowix add ./dsh-flowix-memory` 的真实行为**:pnpm 对"本地目录 + 无 `main` 但有 `dsh.bundle`"的包会不会留软链、重启后 `launcher.mjs` 是否在 `node_modules/dsh-flowix-memory/` 下。未实跑(会写 `~/.dsh`)。
3. **兜底 server 能不能被 mcp-client 接受**:launcher 只实现 4 个方法,`prompts/list`、`resources/list` 缺失时的行为未测;mcp-client 可能只调 `tools/list`,但这是推断。
4. **518 星的增量归因**:需要 star-history 曲线才能在"2026-08-19 之后新增 198 星"里分出 DSH 相关比例;现在只有时间线推断。
5. **`flowix-cli` 在 macOS 上的沙箱摩擦**:桌面 app 有 security-scoped bookmark 与 entitlements 概念(`CLAUDE.md` 的 ad-hoc 签名段),CLI 以普通进程读同一批笔记目录时是否需要额外授权,未验。
6. **collection 的磁盘格式**:`collection_store.rs` 只读到读取路径,`CollectionDocument` 的 YAML 字段集与 `records.include` 行结构未细读,"agent 能改到哪一层"目前只确证到 `collection.add-note` 能写笔记 + 追加行。
7. **历史被截断**:仓库创建于 2026-05-25,但 git 只有一个 2026-07-15 的根提交。2026-07-15 之前是否已有 DSH 相关工作,git 无法作证,"第一个 DSH 提交是 2026-08-18"这句只在**可见历史**内成立。
