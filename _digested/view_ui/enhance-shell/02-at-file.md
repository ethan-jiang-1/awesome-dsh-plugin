# at-file — 输入框里的 `@` 补全只交路径,文件字节从不进上下文

> 证据等级:★★★(源码级;`FSMargoo/dsh-at-file@da602d1a8f1b417b8a1d8d4059e0f4cb1c353524`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 394 为 2026-08-19 冻结采样,下载无记录(同日采样缺口);实时星标 570 为 2026-11-18 GitHub API 查询值,两者不可混用。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `FSMargoo/dsh-at-file`([registry](../../../data/plugins/FSMargoo__dsh-at-file.yml)) |
| 类目 | ui(2351 条,全表最大;[census](../../ecosystem/census.py));子分类 [enhance-shell](README.md) |
| 状态 | ⛔ **已被官方 `@file` 取代**(DSH 0.2.1 内置);0.2.1-rc.5 上 `ctx.settings.register` 消失,Host 半疑似加载失败。**不建议新装**,保留作兼容断代/权限边界参考。 |
| 自述 | 「Codex 风格的 `@file` 文件引用,输入框里直接搜索并引用工作区文件」——registry 的 en 描述仍是旧口径「attach their contents to prompts」,仓库 `package.json` 描述已改成「without injecting file content」,源码站后者(0.3.0 起只传路径) |
| 星标 ⚠ | **394**(2026-08-19 冻结采样;仓库 2026-08-13 创建,即发布第 6 天已 394);**实时 570**(2026-11-18,GitHub API) |
| 下载 ⚠ | 边车无记录(2026-08-19 采样缺口) |
| 扩散 | **3**(口径:`grep -ril 'at-file' data/plugins/` 命中 5,减去自身 1、减去子串误命中 1(`data/plugins/nico-zhuang__dsh-chat-file-actions.yml` 里 "chat-file" 含 "at-file");3 条中 **1** 条接同一扩展点、2 条只抄交互,见「为什么它突出」) |
| 仓库 commit | `da602d1a8f1b417b8a1d8d4059e0f4cb1c353524`(2026-09-01,`main`,tag `v0.7.0`;2026-08-13 起 36 个提交) |
| 包形态 | GitHub tag tarball(`v0.7.0`)+ 提交了 `lib/` 构建产物;host 为 ESM(`lib/index.js`),client 为单文件 CJS bundle,用 `window.__ModuleLoader__.load(...)` 自注册(`build.mjs:78-80`) |
| 代码规模 | `src/**` **3229** 行 = host 1144(`src/*.ts`)+ client 2085(`src/client/*`);测试 2910 行 / 13 个 spec;`wc -l src/*.ts src/client/*`。`lib/` 构建产物 3.4 MB(全部 tracked 文件 4.4 MB)计入仓库体积 |

## 它到底是什么

一个**纯客户端交互 + 一条 pre-step 边界**的插件,而不是内容注入器。它的中心承诺写在 `src/contract.ts:5-6` 与 `AGENTS.md:31`:文件字节永不越过 wire,也永不越过 Host 的提及边界;插件只确认「这个工作区路径存在」,读不读、怎么读交给 agent 手里现有的工具。

两个半各自独立:

- **Host 半**(`src/index.ts:61-112`)挂一个 Typert Remote 服务 `atFile`,暴露 `search` / `getSettings` / `updateSettings`(`src/runtime.ts:55-71`、`src/contract.ts:113-175`),并在每个 agent 的 `agent/pre-step` 上做一次「提及 → 引用标记」的改写。
- **Client 半**(`src/client/index.ts:88-324`)向 DSH web 的输入触发器注册一个 `@` 源,渲染引用条与设置页,不读文件。

核心循环(全部有源码落点):

1. 用户在输入框敲 `@`,DSH 的输入触发器把「光标前的 query」交给插件注册的源(`src/client/source.ts:165-175`)。
2. 源按 session 取整棵工作区索引(30s 缓存、跨按键复用),在浏览器里本地排序取前 50(`src/client/source.ts:32,117-150,174`)。
3. 选中后 `onPick` 只落一个纯文本 token:`@相对路径`,目录补尾斜杠(`src/client/source.ts:181-188`)。没有 chip、没有附件、没有 id。
4. 提交时 Host 的 `agent/pre-step` 用 `@([^\s@]+)` 扫描**只属于 user 的文本块**(`src/mention.ts:34,106-121`),逐 token 做存在性与包含检查,然后为每条提及**追加一条独立 user 消息**,内容只有 `<workspace-reference path="…" kind="file|directory" />`(`src/mention.ts:93-96,127-130`)。
5. 模型看到的是「用户引用了这个路径」,要不要 `read` / `read_image` 由它自己决定。

所以数据模型很小:`FileEntry { path, relative, kind }`(`src/contract.ts:12-16`)、settings 段 `{ enabled, ignoreFiles, workspaceIgnoreFiles, ignorePastedMentions }`(`src/contract.ts:37-48`)。**没有 token 预算、没有截断、没有编码处理**——因为没有任何内容经过这里。大文件、PDF、二进制与文本走完全相同的路径,这一点被测试固定下来(`tests/mention.spec.ts:32` 起:引用只带路径不带内容;大二进制与 PDF 与文本一致)。

## 怎么接进 DSH

**manifest。** `package.json:23-32` 只有 `dsh.bundle.patch → ./cordis.patch.yml` 与 `dsh.client.{platform:"web", inject:[input-trigger, slots, locale]}`;真正被 Loader 读的是 3 行 patch,`insert` 一条 `id/name = dsh-at-file`(`cordis.patch.yml:1-3`)。`dsh.plugin.json:1-12` 是同一信息的第二份声明。

**Host 注册点**(`src/index.ts`):

| 位置 | 作用 |
|---|---|
| `src/index.ts:33` | `inject = ['typert','settings','agents']`,三个服务缺一不加载 |
| `src/index.ts:51-54` | `Config` schema:`maxIndexedFiles` 默认 **5000**、`ignoreDirs` 默认 60 项(`src/defaults.ts:4-65`) |
| `src/index.ts:65` + `src/settings.ts:48-50` | `ctx.settings.register('at-file', schema, { applies:'live' })`,拿到 live scope |
| `src/index.ts:87-90` | `ctx.typert.register(TYPERT_MANIFEST)`,strict 描述符在 `src/typert.ts:15-49`、codec 在 `src/contract.ts:113-175` |
| `src/index.ts:98-112` | `agent/created` → `agent.ctx.on('agent/pre-step', …)`,监听器随 agent 作用域注销 |
| `src/runtime.ts:32` | `super(ctx,'atFile')`,wire 命名空间即服务键 |

`search` 的参数是**一个 live Agent**,由 Typert 的 `agent` lookup 按 `agentId` 解析(`src/contract.ts:120-130`),codec 的 `typeSymbol` 必须精确等于 `@deepseek-ai/dsh-session/types#SessionId`(`src/contract.ts:128`)。索引根取 `agent.session.header.cwd`(`src/runtime.ts:61`),不是进程 cwd。

**Client 注册点**(`src/client/index.ts`):

- `inject = ['inputTriggers','sessions','connection','remote','slots','locale']`(`src/client/index.ts:42`)。
- `ctx.remote.$mount(AT_FILE_REMOTE)` 挂命名空间,但读取**故意不走** `ctx.remote.atFile`,而是 `ctx.reflect.get('remote.atFile')`(`src/client/index.ts:160-172`;注释 `src/client/index.ts:109-114` 说明点号读取会沿 fiber 链断在 Loader 的 runtime-less fork 上)。
- `inputTriggers.registerSource(source)`(`src/client/index.ts:231`,受设置开关动态挂/卸 `src/client/index.ts:221-247`)。
- 三个 slot:`conversation.input.dock`(引用条,`src/client/index.ts:276-285`)、`conversation.input.overlay`(目录右箭头导航,`src/client/index.ts:287-296`)、`settings.section`(设置页,`src/client/index.ts:298-323`)。
- locale 字典(`src/client/index.ts:90`)与注入式样式串(`src/client/index.ts:89`;`src/client/styles.ts:1-6` 自述「web 端每个客户端插件只发一个文件,所以不能有 CSS 产物」)。

**不改宿主文件、不 patch 宿主。** 卸载后界面只剩「少了一个 `@` 源、少了一个 dock、少了一个设置页」:注册全部包在 `ctx.effect` 的 disposer 里(`src/index.ts:87-90`、`src/client/index.ts:160-172,240-247`),`@` 源用 `registerSource` 返回的 disposer 撤销(`src/client/index.ts:233-237`)。这是纯客户端插件的标准形态。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `src/index.ts` | 114 | host 入口:settings、runtime、typert manifest、pre-step 挂载 | `src/index.ts:33,51-54,87-112` |
| `src/runtime.ts` | 72 | `AtFileRuntime`:search 与设置读写 | `src/runtime.ts:32,55-71` |
| `src/files.ts` | 218 | 有界 `node:fs` 工作区遍历 | `src/files.ts:111-217` |
| `src/mention.ts` | 182 | pre-step 扫描 / 校验 / 注入引用 | `src/mention.ts:42-55,64-81,151-182` |
| `src/defaults.ts` | 211 | 忽略目录/文件清单、规则规范化、缓存 key | `src/defaults.ts:4-72,194-199` |
| `src/contract.ts` | 175 | 共享 wire 描述符 + zod codec | `src/contract.ts:113-175` |
| `src/settings.ts` | 50 | `at-file` 设置命名空间 | `src/settings.ts:18-41,48-50` |
| `src/typert.ts` | 50 | 手写 strict manifest | `src/typert.ts:15-49` |
| `src/paste.ts` | 24 | 粘贴 `@` 的不可见标记 | `src/paste.ts:7-24` |
| `src/client/index.ts` | 324 | 客户端装配 | `src/client/index.ts:160-172,221-323` |
| `src/client/source.ts` | 205 | `@` 源、per-session 索引缓存 | `src/client/source.ts:100-204` |
| `src/client/search.ts` | 97 | 纯函数排序 | `src/client/search.ts:11-96` |
| `src/client/FilesDock.tsx` | 103 | 从 draft 解析 token、开/删 | `src/client/FilesDock.tsx:40-71,93` |
| `src/client/FolderNavigator.tsx` | 147 | `ArrowRight` 进目录 + 粘贴打标记 | `src/client/FolderNavigator.tsx:101-144` |
| `src/client/SettingsSection.tsx` | 403 | 全局/工作区 Exact/Regex 过滤规则 | `src/client/SettingsSection.tsx:19-38` |
| `src/client/styles.ts` | 515 | 注入式 CSS 字符串(不能有 CSS 产物) | `src/client/styles.ts:1-6,13-20` |

**数据流**(一次 `@` 到一条模型消息):

```text
浏览器                                                  Host
敲 @ → 触发器的 @ 源
  candidates(query) ──── atFile/search(sessionId) ────► AtFileRuntime.search
                                                         └ indexWorkspace(agent.cwd)
  rankFiles(files, query, 50) 本地排序                     ← FileEntry[]（无内容）
  onPick → 纯文本 "@rel/path "（目录带 /）
提交 ───────────────────────────────────────────────► agent/pre-step
                                                         scanMentions（只扫 source.kind==='user'）
                                                         isAbsolute 拒绝 → resolve/relative 包含检查 → stat
                                                         每条提及注入 1 条 user 消息 <workspace-reference/>
                                                      模型看到的只有路径 + kind
```

**索引遍历**(`src/files.ts:111-217`)。BFS 队列,`opendir` 逐 dirent 读取(注释 `src/files.ts:2-6` 强调内存只有一层),忽略**按目录 basename** 匹配(`src/files.ts:117,185,196`),文件过滤规则只匹配 basename(`src/files.ts:122-127`),因此 **不解析 `.gitignore`/`.ignore`**——忽略面只有内置 58 个目录名加用户规则。符号链接先 `realpath` 再 `stat`(`src/files.ts:172-183`),按目标类型当文件或目录入索引,目录链接会继续下钻(`src/files.ts:184-188`);`ancestors` 集合只阻止「回到当前路径上的祖先」(`src/files.ts:144-146`),不阻止链接指向工作区之外。达到 `maxFiles` 时置 `truncated` 并停(`src/files.ts:167-170,214`),最后按 `relative` 排序(`src/files.ts:216`)。失败处理分层:根打不开抛错(`src/files.ts:130-135,152`)、子目录打不开只 `console.warn` 跳过(`src/files.ts:153`)、断链跳过(`src/files.ts:178-183`)。

**排序**(`src/client/search.ts:11-96`)。空 query 是「浅层优先、同深度目录在前」(`src/client/search.ts:32-39`);普通 query 只匹配 basename(精确 5000 / 前缀 4500 / 子串 4000 / 子序列 3000,`src/client/search.ts:79-96`),所以字母散落在长路径里不会误命中;含 `/` 才按路径段顺序匹配(`src/client/search.ts:42-76`)。上限 50 条(`src/client/source.ts:32`)。

**缓存**(`src/client/source.ts:100-204`)。每个 session 一份 `IndexCache`:30s TTL(`src/client/source.ts:35`)、在飞的请求 join 而不重发(`src/client/source.ts:117-125`)、失败就删 key 让下次重试(`src/client/source.ts:139-142`)、`warm` 在 session 出生时预热(`src/client/source.ts:176-180`)、`lexicon`/`subscribeLexicon` 给装饰层同步名称表(`src/client/source.ts:189-201`)。`connection/reset` 时清空索引与路径映射(`src/client/index.ts:210-214`)。

**引用条**(`src/client/FilesDock.tsx:40-71`)。用与 Host 完全相同的 `@([^\s@]+)` 语法解析 draft,只渲染「在当前 session 已落定索引里存在」的 token,点路径调 `openWorkspacePath`(新契约)或回退 `host.openPath`(`src/client/index.ts:249-265`),点 × 精确删那一段(`src/client/FilesDock.tsx:93`)。

**pre-step 边界**(`src/mention.ts:151-182`)。先 `await next()` 拿下游决策,再只清理/注入 user 文本;关掉开关时**仍**执行标记清理(`src/mention.ts:174-176`)。`expandMentions` 只读 `source.kind === 'user'`(`src/mention.ts:115`),所以它自己注入的 `at-file-mention` 消息不会被下一轮再扫一遍;注入用 `createUserMessage` 并带自定义 source(`src/mention.ts:127-130`),XML 属性做转义(`src/mention.ts:84-90`)。路径校验是:拒绝绝对路径、`resolve` 后 `relative` 不以 `..` 开头(`src/mention.ts:69-74`)、`stat` 存在(`src/mention.ts:76-78`)。注意这是**词法包含检查**,不 `realpath`。

**粘贴语义**(`src/paste.ts:7-24`、`src/client/FolderNavigator.tsx:119-144`)。默认策略是「粘贴进来的 `@` 不算引用」:在 `paste` 捕获阶段把剪贴板 `text/plain` 里每个 `@` 后插一个 U+2060 word joiner,靠改 `DataTransfer.getData` 让 InputBar 读到标记版文本,显示不变;Host 发送前把标记剥掉(`src/mention.ts:162-173`)。`text/plain` 之外的格式、以及不可扩展的 `DataTransfer` 都是 best-effort,注释自承(`src/client/FolderNavigator.tsx:137-140`)。

**测试能证明的契约**(2910 行,13 个 spec):截断诚实(`tests/files.spec.ts:160`)、外部目录链接会被索引(`tests/files.spec.ts:69`)、循环链接不重入(`tests/files.spec.ts:96`)、逃逸 token 被拒(`tests/mention.spec.ts:129`)、search 在关闭或无 cwd 时拒绝(`tests/runtime.spec.ts:200-212`)、失败 fetch 会被丢弃以便重试(`tests/source.spec.ts`)。覆盖率门槛是每文件 100%(`AGENTS.md:41`)。

## 为什么它突出

**星标是发布窗口的产物,不是长期声量。** 仓库 2026-08-13 创建,2026-08-19 采样时已 394(第 6 天),2026-11-18 实时 570——三个月只多了 176,曲线形状是「发布即峰值 + 长尾」。仓库是单包仓库(无 monorepo 子目录),所以 570 属于这个插件本身,归属上没有歧义(API `full_name` 就为 `FSMargoo/dsh-at-file`,`created_at` 2026-08-13)。按边车值它在 ui 内排第 3(编排者口径;全类 2351 条)。

**扩散 3 条,但只有 1 条真的接同一扩展点。** 口径与判定:

```sh
grep -ril 'at-file' data/plugins/ | wc -l      # 5
grep -ril 'at-file' data/plugins/              # 自身 + 4;其中 chat-file-actions 是 "chat-file" 子串误命中
```

| 衍生 | 接的是什么 | 判定 |
|---|---|---|
| `hatsuyuki0103/dsh-at-any` | 同一扩展点:`inject = ['inputTriggers', …]`(`dsh-at-any/src/client/index.ts:46`)、`inputTriggers.registerSource`(`dsh-at-any/src/client/index.ts:184`)、`sessionOf`(`dsh-at-any/src/client/index.ts:240`),`dsh-at-any/src/client/source.ts:1-9` 的 JSDoc 与本源逐字相同,package 描述也逐字相同 | **硬分叉**:把默认索引上限抬到 1,000,000(`dsh-at-any/src/defaults.ts:9`,其 `src/index.ts:53` 注释写 "No practical truncation"),README 明说「replaces dsh-at-file」,理由是 5000 上限静默丢文件 |
| `SIMON-WORLD/dsh-toolkit#dsh-at-file` | `ctx.tools.register(defineTool({...}))`(`dsh-toolkit/packages/dsh-at-file/src/index.ts:20`),注册 `at_file_read` 工具把文件内容注入会话 | **只抄交互**:同一个 `@` 语汇,扩展点是 tools,不是输入框 |
| `backkom/dsh-at-file-everything` | 实现的是官方 Host 的 `ctx.fileReferences`(`dsh-at-file-everything/src/index.ts:91,125`),外加 `find_files` 工具,客户端只做一个设置卡片(`dsh-at-file-everything/src/client.ts:137` 的 `inject = ['slots','locale']`) | **不接本插件的扩展点**:它接的是官方内置 `@file` 的 provider 面 |

也就是说:扩散发生在「`@` 这个交互形状」上,只有被分叉这一条说明它的客户端实现被当成起点;而生态真正收敛的扩展点是**宿主的** `fileReferences`,不是它的 `atFile`。

**它自己的 README 已经承认被取代**:文件顶部 IMPORTANT 明写「最新官方 DSH release 已内置 `@file` / `@session`,新装请优先用官方实现,本插件仅 best-effort 维护」。本机 DSH `0.2.1-rc.5` 里确实同时存在 `@deepseek-ai/dsh-client-ui-reference`(`@` 源名为 `reference`,`dsh-client-ui-reference/lib/client.js:294-295`)与宿主侧 `@deepseek-ai/dsh-file-reference-local`(默认 `maxEntries: 5e4`,`dsh-file-reference-local/lib/index.js:17,335`)。

**机制上的独特点**是那个反向取舍:别人把内容拼进 prompt,它把「引用」压缩成一个路径 + 一个 kind。判断:这让 token 成本与文件大小、编码、二进制完全解耦,代价是把「读不读、读多少」的责任全部推给 agent 的工具与沙箱。

## 代价与边界

按发生顺序:

1. **忽略规则不是 `.gitignore`。** 只有目录 basename 清单(60 项,`src/defaults.ts:4-65`)与文件名规则;一个不在清单里的构建目录(`out-2026/`、`Library2/`)会整棵进索引;反过来清单里的 `bin`、`build`、`target`、`Library` 会误伤同名的源码目录。用户只能在设置里加 basename 规则,无法按路径排除。
2. **5000 条上限是静默的。** `indexWorkspace` 老老实实返回 `truncated`(`src/files.ts:27,167-170`),但 `search` 只返回 `index.files`(`src/runtime.ts:65-70`),这个标志**没有过 wire**。菜单看起来完全正常,实际只是一个按 BFS 顺序截断的子集;实际丢哪些文件取决于遍历顺序(目录本身也占名额,`src/files.ts:167` 对 dir/file 一视同仁),不按扩展名。第三方分叉把症状描述成「丢 .java/.vue」;判断:按本源看更像遍历顺序问题而非扩展名筛选,但「静默」这点成立。
3. **权限边界等于宿主进程。** Host 半直接 `node:fs` 遍历与 `stat`(`src/files.ts:8-10`、`src/mention.ts:10,76`),不经过 DSH 的 sandbox/policy 链,也不走 `dsh-api-workspace-files`(那个服务的读操作本来也不做工作区包含,只做 UI 预览)。索引根是 `session.header.cwd`,**但符号链接会被 `realpath` 后跟随**:`ws/ext -> /etc` 会把 `/etc` 的条目以 `ext/...` 的名字放进菜单(`src/files.ts:172-193`,`tests/files.spec.ts:69` 明确覆盖「外部目录链接」)。提及校验只是 `resolve` + `relative` 的词法包含(`src/mention.ts:69-74`),`stat` 跟随链接(`src/mention.ts:76`),所以 `@ext/passwd` 会被判成「工作区内」并注入引用。文件字节仍不经插件,读不读由 agent 的 `read` 与其自身沙箱决定——但「工作区内」这个语义已经被绕过。
4. **没有内容 = 没有编码/二进制/大小问题,也没有摘要。** 这是设计优点,同时也是成本:模型必须再花一次工具调用才知道文件是什么;相对路径对模型是充分的,但对「这个 PDF 讲了什么」不提供任何帮助。
5. **失败模式**:`search` 抛错(设置关闭 `src/runtime.ts:58-60`、无 cwd `src/runtime.ts:61-64`、根不可读 `src/files.ts:130-135`)→ client 清空索引并 reject(`src/client/index.ts:194-198`)→ DSH 输入触发器只 `console.error` 并让该源这一轮无候选(`dsh-client-ui-input-trigger/lib/client.js` 内 `candidates failed` 分支),用户看到的是空菜单而不是错误。文件在选中后被删:引用条不再渲染(不在已落定索引里,`src/client/FilesDock.tsx:47`),Host `stat` 失败则静默跳过(`src/mention.ts:76-78`),token 退回普通文本。遍历慢时没有超时,只有 `AbortSignal`(TTL 过期/新查询/重连会中断旧 walk,`src/files.ts:42-70`),菜单在此期间就是等待。
6. **粘贴标记是 best-effort。** 剪贴板 `DataTransfer` 不可扩展时(`src/client/FolderNavigator.tsx:137-140`),粘贴的 `@` 可能被当成真引用;若粘贴时开关为开、发送前改为关,标记会留在正文(判断:按 `src/mention.ts:161-173` 的控制流,关闭时不做清理,未实测)。
7. **兼容成本:2026-09-01 之后 DSH 侧已经断代。** 具体到接口,不是泛泛的「可能不兼容」:

   - **已断**:`ctx.settings.register(ns, schema, {applies:'live'})`(`src/settings.ts:48-50`)。本机 `0.2.1-rc.5` 的 `ctx.settings` 是 `SettingsForms`,公开面只有 `configure/describe/update/replace/mutate` 加 `writable`/`prepareDocument`(`dsh-settings/lib/types/index.d.ts:27,62-116`);全树 grep `.settings.register(` **0 命中**,`SettingsScope` 类型 **0 命中**。判断:插件 `apply()` 会在 `src/settings.ts:49` 抛 `TypeError`,Host 半加载失败,`atFile` 端点与 pre-step 边界都不会出现。
   - **半断**:`@deepseek-ai/dsh-client-store`(`src/client/store.ts:11`)。它在本机安装树里**没有对应包目录**,但仍有 **44** 个官方 client bundle `require("@deepseek-ai/dsh-client-store")`,说明该模块名由 web 端模块表提供;而插件为 0.1.1/0.1.2 写的 fallback(`build.mjs:18-40`,回退到 `@deepseek-ai/dsh-client-runtime/client`)在本机树里 grep 不到 `createSnapshotStore` 导出。哪条分支在 0.2.1 上成立,未验证。
   - **最脆的一处**:`ctx.reflect.get('remote.atFile')`(`src/client/index.ts:162`)。它绕开了公开的点号读取,依赖 cordis 服务存储按 isolation label 解析;注释自承点号路径会断在 Loader 的 fork 上。这是「宿主内部实现」级别的依赖。
   - **仍匹配**:`inputTriggers.registerSource` 与其 `InputTriggerSource`(`candidates/warm/onPick/lexicon/subscribeLexicon` 子集)在 0.2.1 仍在(`dsh-client-ui-input-trigger/lib/types/client/contract.d.ts:10-24`;服务键 `super(ctx,"inputTriggers")`),`PickOutcome` 仍接受 `{text}`(`dsh-client-ui-conversation/lib/types/client/contract/input.d.ts:53-58`);`agent/pre-step` 的 `(payload{agent,messages,signal}, next)` 形状未变(`dsh-agent/lib/types/runtime-types.d.ts:304-310`);`conversation.input.dock` / `conversation.input.overlay` / `settings.section` 三个槽位仍在(`dsh-client-ui-conversation/lib/types/client/contract/slots.d.ts:301-310,470-473`)。
   - **共存副作用**:官方 `reference` 源也绑 `@`。`registerSource` 只对重复的 `(trigger,name)` 抛错,`at-file` 与 `reference` 名字不同,所以两者会**同时出现在一个 `@` 菜单里**,一个插纯文本 token、一个插原子引用。是否互相干扰键盘导航未实测。
8. **维护与体积**:2026-09-01 后 2.5 个月无提交;`lib/` 提交进仓库以便 `file:` 安装免构建,代价是每次改动带 1.2 MB 构建产物(host 599 KB / client 614 KB;`build.mjs:16,51,76` 只把 `@deepseek-ai/*` 设为 external,所以 `zod` 被内联进两个 bundle)。README 里的安装命令仍指向旧 URL `omdsh-dev/dsh-at-file`(2026-11-18 实测 301 → `FSMargoo/dsh-at-file`,tarball 也会跳转,能用但已陈旧),registry 用的是新 URL。

## 可信度与复现

证据等级 ★★★:host 与 client 两侧源码逐文件读过,13 个 spec 的用例清单读过(未逐行读断言),`lib/` 未读,未安装运行。与 DSH `0.2.1-rc.5` 的对照是本机官方包源码与 `grep`,不是运行结果;凡属推断都写了「判断:」。

```sh
git clone --depth 1 https://github.com/FSMargoo/dsh-at-file /tmp/an-at-file
cd /tmp/an-at-file && git log -1 --format='%H %ad %s'   # da602d1a… 2026-09-01
git log --oneline | wc -l                               # 36
wc -l src/*.ts src/client/*                             # host 1144 + client 2085 = 3229
wc -l tests/*                                           # 2910

# 扩散(在 awesome-dsh-plugin 仓库根)
grep -ril 'at-file' data/plugins/ | wc -l               # 5
grep -ril 'at-file' data/plugins/                       # 减去自身与 chat-file 子串误命中 → 3

# 三条衍生的源码坐标(2026-11-18 各自浅克隆,只读入口文件)
git clone --depth 1 https://github.com/hatsuyuki0103/dsh-at-any /tmp/an-at-any          # c085adae 2026-09-10
git clone --depth 1 https://github.com/backkom/dsh-at-file-everything /tmp/an-every     # 61791828 2026-10-27
git clone --depth 1 --filter=blob:none --sparse https://github.com/SIMON-WORLD/dsh-toolkit /tmp/an-toolkit
#   cd /tmp/an-toolkit && git sparse-checkout set packages/dsh-at-file                   # 7574d61 2026-08-24

# 对照本机 DSH
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh
node -e "console.log(require('$DSH/package.json').version)"                # 0.2.1-rc.5
grep -rn "settings: SettingsForms" $DSH/node_modules/@deepseek-ai/dsh-settings/lib/types/index.d.ts
grep -rn "\.settings\.register(" $DSH --include=*.js | wc -l               # 0
grep -l 'require("@deepseek-ai/dsh-client-store")' \
  $DSH/node_modules/@deepseek-ai/*/lib/client.js | wc -l                   # 44
curl -sS -o /dev/null -w '%{http_code} %{redirect_url}\n' \
  https://github.com/omdsh-dev/dsh-at-file                                 # 301 → FSMargoo
```

读过的文件:`package.json`、`dsh.plugin.json`、`cordis.patch.yml`、`build.mjs`、`AGENTS.md`、`README.md`、`README.zh.md`(未逐行)、`src/index.ts`、`src/runtime.ts`、`src/files.ts`、`src/mention.ts`、`src/defaults.ts`、`src/contract.ts`、`src/settings.ts`、`src/typert.ts`、`src/paste.ts`、`src/invariant.ts`、`src/types.ts`、`src/client/index.ts`、`src/client/source.ts`、`src/client/search.ts`、`src/client/FilesDock.tsx`、`src/client/FolderNavigator.tsx`、`src/client/remote.ts`、`src/client/model.ts`、`src/client/store.ts`、`src/client/locales.ts`、`src/client/icons.tsx`(头部)、`src/client/SettingsSection.tsx`(前 60 行)、`src/client/styles.ts`(头部)、`tests/*`(用例名与关键行)。

三个衍生仓库只读了入口文件(`dsh-at-any` 的 `src/client/index.ts`、`src/client/source.ts`、`src/defaults.ts`;`dsh-at-file-everything` 的 `src/index.ts`、`src/client.ts`;`dsh-toolkit` 的 `packages/dsh-at-file/src/index.ts`),其余未读。

未读:`src/client/SettingsSection.tsx` 的规则编辑器主体(60-403)、`src/client/styles.ts` 的 515 行 CSS、`src/client/icons.tsx` 其余部分、`lib/*` 全部、README 截图、`pnpm-lock.yaml`。

## 待验证

1. 在一次性 profile 里 `dsh plugin --profile <tmp> add <v0.7.0 tarball>` 后启动 `dsh web`,确认第一个失败点是不是 `src/settings.ts:49` 的 `ctx.settings.register`(本卡只能从 API 形状推断)。
2. web 端模块表在 `0.2.1-rc.5` 里是否仍提供 `@deepseek-ai/dsh-client-store` 给第三方 bundle;若不提供,`build.mjs:18-40` 的 fallback 名字是否真能拿到 `createSnapshotStore`。
3. 官方 `reference` 源与 `at-file` 源同时挂在 `@` 上时,菜单分组、键盘导航、`ArrowRight` 目录导航是否互相抢事件(插件的 `FolderNavigator` 用 document 捕获阶段监听,`src/client/FolderNavigator.tsx:101-117`)。
4. 570 星标的时间分布:发布 6 天 394、之后 2.5 个月 176 的曲线是否与官方内置 `@file` 的发布/公告同步(GitHub stargazers API 分页可取)。
5. `maxIndexedFiles=5000` 在超大仓库(第三方描述里的 ~1.5M 文件、`Library/` 占 1.2M)下的实际第一屏构成:是「只剩少数顶层目录」还是「按 BFS 均匀截断」。
6. 符号链接逃逸的真实后果:`@ext/passwd` 注入后,agent 的 `read` 是否会被 DSH 自己的 sandbox 拦下;若不被拦,这等于一个稳定的「声明为工作区内」的越权通道。
7. 粘贴标记的残留:粘贴时开、发送前关,正文里的 U+2060 是否真的进入 provider 请求体(看请求日志即可确认)。
