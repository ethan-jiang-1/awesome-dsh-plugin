# notes — 两条能力共用一个 HTTP 客户端;所谓「便签 PNG」是服务端开 headless Chromium 截出来的

> 证据等级:★★★(源码级;`zhaoolee/notes@416035cdccd0226aa94f045e8474b45bfd533961`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 147 / 下载 239 为 2026-08-19 历史采样,**星标是仓库级**(主项目是「开源版锤子便签」全栈 web 应用,插件在其 `dsh-plugin/` 子目录);2026-11-18 实时星标 **334**。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `zhaoolee/notes#dsh-plugin`([registry](../../../data/plugins/zhaoolee__notes--dsh-plugin.yml)) |
| 类目 | tools([census](../../ecosystem/census.py) 1639 条 / 全表 11 744 条);子分类 `single-purpose` |
| 自述 | 「把 DSH 对话导出为锤子便签风格 PNG,或在配置的账号工作区新建/更新 Markdown 便签」——两句话对应同一个工具的两次分叉,不是两个能力两个入口 |
| 星标 ⚠ | **147**(2026-08-19 采样;**仓库级**,非插件级,归属拆解见「为什么它突出」);2026-11-18 实时 **334** |
| 下载 ⚠ | **239**(2026-08-19,npm `@zhaoolee/dsh-notes`)。该值与 npm 官方 API 同期窗口(2026-08-14~08-19 = 516)不一致,口径不同,只当量级用;2026-11-18 实时:近月 685、近周 178 |
| 扩散 | **0**。口径:`grep -ril 'notes' data/plugins/` 命中 **288** 条泛词,逐条筛选后无第三方引用;改用有辨识度的 token 复核,`zhaoolee` / `锤子便签` / `smartisan` 各只命中自身。筛选过程与命令见末节 |
| 仓库 commit | `416035cd`(2026-10-31,`main`);`dsh-plugin/` 最后提交 `23463d79`(2026-08-15),此后代码未动 |
| 包形态 | npm `@zhaoolee/dsh-notes@0.1.2`(共 3 个版本,全部 2026-08-14/15 发布)+ Cordis bundle:`package.json` 的 `dsh.bundle.patch` → 7 行 `cordis.patch.yml`;一个工具,无命令、无 UI、无 service |
| 代码规模 | DSH 面 `src/**/*.ts` **808 行**(index 210 + notes-client 510 + types 88);测试 **758 行**;随源码提交的预编译 `lib/` 509 行 js + 172 行 d.ts;子目录 20 个文件共 2,495 行(含 27 KB `package-lock.json`)。主仓库 421 个 git 文件、`*.ts/*.tsx` 49,069 行,GitHub 记 63.7 MB |

## 它到底是什么

先定性:**它是一个 host 面工具插件(HTTP 客户端 + 一个工具壳),既不是配置包,也不是渲染器。** 想在 DSH 侧找「锤子便签风格」的实现会扑空——样式、字体、截图、长文切片全在同一个仓库的 web 应用与 `server/index.ts` 里;`dsh-plugin/` 只做三件事:读配置、发 HTTP、把结果拼成工具返回值。

只有一个工具 `notes_export_conversation`(`src/index.ts:62-64`),参数 6 个:`markdown`(必填)、写入模式的 `note_id`/`folder`/`starred`/`pinned`、图片模式的 `theme`(`src/index.ts:66-94`)。所谓「两条能力」是**同一个工具在 `execute` 开头的一次 if/else**:

1. `readConfiguredBaseUrl(config)` 返回 `undefined` → **匿名导出图片**(`src/index.ts:145-169`):把 markdown POST 到演示服务器的 `/api/export`,拿回 PNG 字节,写进系统临时目录,返回 `action: "exported-image"` + 本地路径 + 服务端公开 URL。
2. 配了 `baseUrl` → **写入便签**(`src/index.ts:171-183`):拉当前账号的整个工作区,改完再写回去,返回 `action: "created" | "updated"` + 便签 ID + 前端链接。

共用的部分全在 `src/notes-client.ts`:`NotesServiceConfig` 解析(`:61-99`)、`NotesApiError` 错误类型(`:28-38`)、标题提取 `extractNoteTitle`(`:102-119`)、`fetch` 封装(`:235-262`)。分叉点是 `NotesClient` 的两个方法 `exportNote`(`:357-460`)与 `exportImage`(`:466-509`)。于是「数据模型」也是两套,且都只活在传输层:`types.ts:2-25` 的 `NoteDocument`/`NoteWorkspace`(镜像服务端 JSON)与 `types.ts:50-57` 的 `ImageExportResult`(镜像 `/api/export` 的响应体 + 响应头)。

一个容易读错的点:**默认路径是出网的**。读不到配置时不报错、不提示,直接落到 `DEFAULT_DEMO_SERVER = "https://notes.fangyuanxiaozhan.com"`(`notes-client.ts:25,61-75`);写模式才要求显式配置,缺地址直接抛错(`:86-91`,注释明写「不得探测本地端口,也不得回退到任何公网服务」)。两条路径的默认值方向相反,是这插件最该先讲清的一行。

## 怎么接进 DSH

接入面只有四个文件,没有一处 DSH 特例:

- **manifest**:`package.json:44-48` 的 `"dsh": { "bundle": { "patch": "./cordis.patch.yml" } }`。宿主只认这个键:`dsh-app-boot` 的 `bundlePatchFiles()` 校验它必须是字符串或字符串数组(`dsh-app-boot/lib/index.js:517-519`),`dsh-plugin-manager` 用它判断「这是 profile 层还是普通依赖」(`dsh-plugin-manager/lib/index.js:336,339`)。
- **patch**:`cordis.patch.yml` 全文 7 行,一个 `insert`,`id: notes-export`、`name: "@zhaoolee/dsh-notes"`、`config: {}`(`:4-7`)。头注释写明 `id` 是「后续 patch 层覆盖整行 `config` 时的稳定身份」(`:1-3`)——这是它给出的唯一配置覆写路径。
- **插件形状**:导出 `name = "notes-export"`、`inject = ["tools"]`、schemastery 的 `Config`(5 个键**全部可选**,所以 `config: {}` 合法)、`apply(ctx, config)`(`src/index.ts:23-42,61`)。注册点只有一处:`ctx.tools.register(defineTool({...}))`(`:62`)。
- **依赖**:`dependencies` 只有 `@deepseek-ai/schemastery`;`@deepseek-ai/cordis` 与 `@deepseek-ai/dsh-tools` 是 **peer**(`package.json:56-62`)。原因写在测试头注释里(`tests/package-metadata.test.ts:1-3`):DSH profile 用 hoisted node_modules 且关闭 peer 自动安装,宿主运行时若进了 `dependencies`,插件副本就会遮蔽 DSH 自带副本、内部 Symbol 不一致,第一次工具调用即在 `scheduler.prepare` 崩。`:33-54` 把这条钉成断言。

宿主契约在三处细节上与源码对得上:① `output` 必须同时给 `schema` 和 `render` **函数**,否则注册即抛(`dsh-tools/lib/index.js:2978`);插件在 `src/index.ts:95-139` 两样都给,`render` 按 `action` 分支产出人读文本。② `timeoutMs: 60_000`(`src/index.ts:140`)由宿主在注册时校验(`dsh-tools/lib/index.js:2979-2980`)。③ 插件**没有**声明 `isConcurrencySafe`,宿主按 `{kind:"exclusive"}` 处理(`dsh-tools/lib/index.js:3155`),即同一 agent 的工具调用串行——对一个「整工作区读改写」的工具,这是正确的默认。

安装有两条路:`dsh plugin --profile web add @zhaoolee/dsh-notes`(npm)或 `dsh web --patch /abs/path/cordis.patch.yml`(不装,直接叠 patch)(`README.md:22-56`)。`dsh plugin` 本身只是把参数转发给 pnpm,`--profile` 是必填项(`dsh/lib/bin.js:116-117`)。仓库随源码提交预编译 `lib/`(`files` 含 `lib`,`package.json:38-43`),为的是绕开 DSH 对依赖构建脚本的审批(`allowBuilds`,`dsh-plugin-manager/lib/index.js:1099,1126`);`tests/package-metadata.test.ts:56-79` 断言入口产物存在,`:81-116` 重跑一次 `tsc` 并**逐字节**比对 `lib/`——用测试禁止「改了 src 忘了提交产物」。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `dsh-plugin/src/index.ts` | 210 | 工具定义、两级模式分叉、错误包装 | `:62-64` 注册;`:143` 分支判据;`:145-169` 图片;`:171-183` 写入;`:194-199` 错误重抛 |
| `dsh-plugin/src/notes-client.ts` | 510 | 纯 HTTP 客户端,不 import 任何 dsh 包 | `:61-99` 配置;`:201-211` 临时文件;`:305-327` token;`:357-460` 读改写;`:466-509` 图片 |
| `dsh-plugin/src/types.ts` | 88 | 工作区 / 输出两套形状 | `:2-31`;`:50-57`;`:80-88` |
| `dsh-plugin/cordis.patch.yml` | 7 | 唯一 manifest 载体 | `:4-7` |
| `dsh-plugin/tests/notes-client.test.ts` | 440 | 13 个单测,mock `fetch` | `:297-330` 409 重试 |
| `dsh-plugin/tests/e2e-export.test.ts` | 201 | 起真实后端跑两条链路 | `:79-95`;`:167-189` |
| `dsh-plugin/tests/package-metadata.test.ts` | 117 | 3 个打包契约测试 | `:33-54`,`:56-79`,`:81-116` |
| `server/index.ts` | 5,419 | **PNG 真身**:Playwright 渲染 + 便签 API | `:287-292`;`:3429-3450`;`:3125-3180`;`:3088-3123`;`:4886-4927` |
| `src/components/NoteSheet.tsx` / `src/styles.css` | 127 / 10,803 | 截图对象(便签纸 DOM 与 6 套主题) | `NoteSheet.tsx:30`;`styles.css:1-23` 字体;`note-card-theme-styles.ts` 309 行 |

数据流两条,别混:

```
① 写入模式(配了 baseUrl)
   DSH 模型 ──notes_export_conversation──▶ index.ts execute
     └─ resolveServiceConfig ──▶ NotesClient.exportNote
          ├─ POST /api/auth/skill-token(仅当无 token;用户名密码换 notes_sk_v1.*,只存内存)
          ├─ GET  /api/workspace            → { workspace, updatedAt }   整份工作区
          ├─ 内存里改一张 NoteDocument       → PUT /api/workspace(expectedUpdatedAt)
          └─ 409 → 回读重试,最多 4 次       → hash 链接 #note=<id>&view=preview

② 图片模式(未配置,默认)
   DSH 模型 ──同一工具──▶ index.ts execute
     └─ new NotesClient({ baseUrl: demoServer }).exportImage
          └─ POST https://notes.fangyuanxiaozhan.com/api/export {markdown, theme, filename}
               └─ 服务端 server/index.ts:4886
                    ├─ Playwright chromium.newPage(deviceScaleFactor 3, 1280×960)
                    ├─ goto <本应用前端>?renderMode=playwright&theme=<id>
                    ├─ fill #markdown-editor ← markdown;等字体/图片/高度稳定
                    ├─ screenshot .note-sheet → 超高则切片 + 自写 PNG 缝合
                    └─ 写 storage/images/<name>.png → 响应头 X-Export-Url(公开 URL)
          └─ 插件把 PNG 写进 mkdtemp(0700)+ 文件 0600 → 返回本地路径与公开 URL
```

**写入路径**(`exportNote`,`notes-client.ts:357-460`):`resolveToken` → 最多 4 次循环:GET `/api/workspace` 拿 `{workspace, updatedAt}` → 在内存里新建或改写一张 `NoteDocument`(`:382-427`)→ PUT 回整份工作区并带 `expectedUpdatedAt`(`:336-351`)→ 409 就回读重试(`:446-456`),4 次仍冲突则抛「工作区在连续重试期间一直变化」。新建便签的 `id` 是客户端 `randomUUID()`,`normalOrder` 取「现有最小值 - 1」,置顶则 `pinnedAt = max(now, 最新 + 1)`(`:154-184`)。前端链接固定为 hash 路由 `${baseUrl}/#note=<id>&view=preview`(`:122-124`)。

**图片路径**(`exportImage`,`:466-509`):POST `/api/export`,`Accept: image/png`,body 只有 `{markdown, theme?, filename?}`;响应体是 PNG 字节,`X-Export-Url` / `X-Export-Theme` 从响应头读回(`:504-508`)。落到本地那一步在 `savePngToTempFile`(`:201-211`):`mkdtemp(tmpdir()/dsh-notes-)` 建 0700 私有目录 + `writeFile(..., { mode: 0o600 })`。

**PNG 到底怎么来的**(`server/index.ts`,本卡最该记住的一段):服务端用 **Playwright + headless Chromium**(`:13` import,`:799-822` 单例 browser,断连自动重建),开新页 `deviceScaleFactor: 3`、视口 1280×960(`:3429-3437`),`goto` 到**本应用自己的前端**并带 `?renderMode=playwright&theme=<id>`(`:339-364`);等 `#markdown-editor`(前端 `src/components/EditorPanel.tsx:1307`)出现后 `fill(markdown)`,再等 `document.fonts.ready` + 所有 `<img>` 落定(`:2784-2802`)、等 `.note-sheet` 高度连续采样稳定(`:2804-2819`),最后对 `.note-sheet`(`NoteSheet.tsx:30`)截图。字体是自带的 OPPOSans 三个 woff2(`src/styles.css:1-23`),主题是 6 套 CSS 变量(`src/lib/note-card-theme-styles.ts`),`theme` 枚举与服务端 `supportedThemes`(`server/index.ts:259`)对得上。**没有 HTML→canvas 库,没有 satori/resvg,也没有「分页」概念**——长文是一张无限长的纸:当「高 × 3 > 30000」时切成 2,999 px 高的块,滚动、逐块截图,再用自写的 PNG 拼接器重写 `IHDR` 并重新 deflate `IDAT`(`:3088-3123` 拼接,`:3125-3180` 分块,常量在 `:287-292`)。所以「长文分页」实际是**切片再缝合**,不是排版分页。

**同一能力还有第二个扩展点**:仓库里 `skills/notes-export-api/scripts/notes_api.mjs`(1,105 行)做同样的事,给其他 agent(Hermes/OpenClaw)用;`notes-client.ts:1-8` 的注释直接说「读写逻辑与该脚本保持一致」,两边的 `/api/auth/skill-token`、`/api/workspace`、409 重试都同构(`notes_api.mjs:211,341,569-586`)。**判断:插件是这份脚本的 DSH 专用瘦客户端,不是一套独立实现。**

## 为什么它突出

**先拆星标。** GitHub 星标是仓库级,而 `zhaoolee/notes` 是一个成熟产品仓库(React + Express 全栈),DSH 只是它的一个集成面。时间线:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-03-15 | 仓库创建 | GitHub API `created_at` |
| 2026-08-14 | `feat: add DSH notes plugin`(`6d22816c1d`)与 npm 0.1.0 发布 | `commits?path=dsh-plugin` / npm registry |
| 2026-08-15 | 子目录最后一个提交 `23463d79a9`(`chore: release dsh notes 0.1.2`)与 npm 0.1.2 | 同上 |
| **2026-08-19** | **⚠ 星标 147 / 下载 239 采样点** | registry 边车 |
| 2026-10-31 | 仓库 HEAD(`docs: record 1.15.1 production verification`) | 本地 `git log -1` |
| 2026-11-18 | 实时星标 **334** | GitHub API |

仓库在 DSH 插件出现前已经跑了 **5 个月**;插件从首发到采样点只有 **5 天**。**147 里能归给 DSH 适配层的,最多是这 5 天的增量,无法拆分,不能默认算给插件。** 反向证据更硬:插件代码自 2026-08-15 冻结,而星标从 147 涨到 334(+187)全部发生在冻结之后——**这 187 个星不可能来自插件迭代,只能来自主项目。** 主 README 把 DSH 放在能力清单的第 15 条(18 条 bullet 里,`README.md:32`),另有一个 `## 通过DSH调用` 小节(`:37-53`)排在 `## 通过skill调用` 之前——**有正式入口,但定位是「N 个集成之一」**(同仓还有 skill、公众号粘贴、微信文章导入、站点发布、Hermes/OpenClaw 等入口),不是一等公民。

**扩散是筛出来的 0。** `grep -ril 'notes' data/plugins/` 命中 288 条,几乎全是泛词(便签墙、笔记面板、决策笔记);其中 9 条名字带 `dsh-notes`(如 `suomir1995/dsh-notes`、`EchoTint/dsh-notes-wall`)**是不同 owner 的本地 Markdown 笔记工具,与本插件没有引用关系**。改用有辨识度的 token 复核:`zhaoolee` → 1(自身)、`锤子便签` → 1(自身)、`smartisan` → 1(自身)、`notes_export` → 0、`fangyuanxiaozhan` → 0、`@zhaoolee` → 0。**第三方提及 0。** 同交互(会话 → 长图 PNG)的条目在 registry 里确实有(`7starsseeker/dsh-card-export`、`Fruneng/dsh-share-session` 自述里都写「长图」;前者自述复用本机 Chromium),但都各自实现,**既不引用本插件,也不共用任何扩展点**——本插件没有 service key、没有 UI slot、没有事件钩子,对外只剩一个工具名。

**类内位置**:tools 1639 条里 ⚠147 排第二,仅次于 `superdesigndev/treg` 477。但要立刻补分母:1639 条里只有 **173 条**有边车星标记录(覆盖 10.6%),所以「类内第二」是「有星标记录者中的第二」,不是全类第二。

**为什么是这种形态(输出侧能力)**。判断,三条依据都在源码里:

1. **它把能力押在「产物」而不是「查询」上**。多数工具是取数/检索/执行,输入在 DSH、输出回 DSH;这个工具的输出是**能离开 DSH 独立存在的东西**(PNG 文件或云端便签),因此必须依赖一个 DSH 之外的持久系统,插件只能是客户端。这解释了「为什么薄」:薄不是偷懒,是产物必须在别处。
2. **薄适配层 + 厚宿主 → 星标涨、下载不涨、衍生不涨**。可仿制的只有 808 行,仿出来还得自己有一个便签服务(或白嫖作者的演示服务器);而 `dsh-notes` 三个版本在 2026-08-15 之后停止发版,`lib/` 与 `src/` 还被测试锁死一致,没有 API 演进空间留给衍生者跟。下载量级也支持「一次装成、长期不动」:⚠ 239(2026-08-19),实时近月 685(2026-10-18~11-16)——对一个三个月不更新的单工具插件,这更像存量用户重装与 CI 拉包,而不是增长。
3. **星标高的是产品,不是插件**。147 与 334 都记在「开源版锤子便签」这个产品名下,插件是它第 N 个导出通道。**结论:明星,不是锚;影响力应记在主项目,不应记在 DSH 适配层。**

## 代价与边界

**隐私(最硬,且默认发生)**:不配置任何东西时,对话正文会被 POST 到 `https://notes.fangyuanxiaozhan.com/api/export`(`notes-client.ts:25,485`)。该演示服务器 2026-11-18 实测:`/api/health` → `{"ok":true}`,`/api/auth/session` → `{"requireLogin":false}`,`POST /api/export` 用空 body 打过去 → **500**(「Missing markdown or markdownPath」)而不是 401——**匿名可达,没有鉴权**。按同仓服务端代码(线上未逐项复现),它会把渲染出的 PNG **写进 `storage/images`(`:247`)并以 `/images/<name>` 公开静态托管**,`immutable` + 一年缓存(`server/index.ts:4194,3397-3412`),插件还把这个公开 URL 原样返回给模型和用户(`src/index.ts:164`)。README 的说法是「不留存内容到任何账号工作区」(`README.md:109-112`)——**字面成立,但「不落盘」不成立**:图在服务器上,而且公开可取。图里还带服务端默认页脚「由开源版锤子便签发送 / Powered by zhaoolee/notes」(`src/lib/footer.ts:6-11`,插件从不传 `footerBrand`/`footerVia`),即每张图都带作者水印。本地那一份是私有的(0700 目录 + 0600 文件,`notes-client.ts:206-209`),远端那一份不是。

**同一端点还有两个服务端问题**(不在 `dsh-plugin/` 内,但正是它调用的那条路):① `/api/export` 匿名可调,`resolveMarkdown` 接受 `markdownPath` 并 `fs.readFile` 任意路径、再渲染成图片返回(`server/index.ts:831-841`)——对公网实例,这是把「任意文件读」变成「可下载的图」;② 该路由**没有速率限制**(全仓只有微信导入有 limiter,`server/index.ts:80`),而每次调用都要起一个 Chromium 页面渲染,是明确的资源放大面。强制登录开关 `REQUIRE_LOGIN`(`:251`,取值为 `1/true/yes/on`)只作用于 `/api/`(`:4131-4137`,白名单在 `:4095-4117`),`/images` 在它之外(`:4194`),所以即便运营者开了登录,导出的图仍然公开。

**失败模式(按发生顺序)**:

1. **没有配置** → 不报错,直接出网到演示服务器。用户以为在本地导出,内容已经过第三方。
2. **演示服务器不可达/超时** → `fetch` 抛 `TypeError`,不是 `NotesApiError`,被原样重抛(`src/index.ts:194-199`),模型看到底层错误串,拿不到「该配置自己的服务」这类可行动提示。
3. **配了 `baseUrl` 但没凭据** → `resolveToken` 明确拒绝(`notes-client.ts:310-317`),消息可读。
4. **token 失效 / 4xx** → `NotesApiError` 带 status,**不重试**(只有 409 重试,`:446-456`),外层包成「导出便签失败:<msg>」。
5. **并发编辑** → 4 次尝试后失败;`now` 在循环外只取一次(`:368`),重试期间 `updatedAt` 不变(小瑕疵,不影响正确性)。
6. **`folder` 不存在 / `note_id` 不存在 / 便签在回收站** → 三种都直接抛(`:147,388,392`),不会静默落成未分类。
7. **主题名不被服务端接受** → `resolveTheme` 抛 `UnsupportedExportThemeError`(`server/index.ts:848-853`),出口处映射成 400(`:4920`);插件 6 个枚举与服务端 `supportedThemes` 一致,正常不会踩。
8. **服务端没装 Chromium** → 500,`hint` 明说要跑 `npx playwright install chromium`(`server/index.ts:4914-4924`)——自建服务的第一道坎。
9. **工具 60 秒超时**:`timeoutMs: 60_000`(`src/index.ts:140`)。服务端一次渲染要起页、等字体、等图片、可能分块截图,长对话在慢机器上会撞上限;abort 只会取消 `fetch`(`notes-client.ts:241-250` 传 `signal`),服务端的浏览器页仍在跑。

**维护成本**:`dsh-plugin/` 自 2026-08-15 后无提交,而宿主已走过 `0.1.0-rc.6`(`peerDependencies` 仍写 `^0.1.0-rc.6`,`package.json:59-62`)。README 自述 `0.1.0` 在 rc.6 上会「因宿主运行时重复安装而中止会话」(`README.md:36-37`)——**这类崩溃正是 peer 依赖那条规则的由来**,也说明它的宿主兼容是靠人工踩坑修的,没有版本矩阵。另外,整工作区读改写意味着写入成本随便签数量线性增长:便签多了以后每次导出都要搬全量 JSON。

## 可信度与复现

- **★★★ 覆盖**:`dsh-plugin/` 20 个文件全读(含 `lib/` 对照);PNG 链路读了 `server/index.ts` 的渲染、导出、鉴权、静态托管相关段;前端只读了 `NoteSheet.tsx`、`EditorPanel.tsx:1307`、`App.tsx` 的 renderMode 分支、`footer.ts`、`note-card-theme-styles.ts`。宿主侧读了 `dsh-tools` 的 `defineTool`/`register`/并发语义、`dsh-app-boot` 的 `bundlePatchFiles`、`dsh-plugin-manager` 的 bundle 判定与 `allowBuilds`、`dsh/lib/bin.js` 的 `plugin` 命令。
- **未读**:`server/index.ts` 5,419 行里其余业务(公众号、站点发布、微信导入、AI 审阅、归档打包)、`src/` 76 个前端文件的大部分、`backend/tests/` 与 `frontend/tests/`。**没有实跑** `npm test`(单测 mock `fetch`,可离线跑;e2e 需要 Playwright Chromium,本轮未装)。

```sh
# 1) 克隆与提交(浅克隆 + blob 过滤,421 个文件)
git clone --depth 1 --filter=blob:none https://github.com/zhaoolee/notes.git notes
cd notes && git log -1 --format='%H %ad %s' --date=iso     # 416035cd… 2026-10-31
git log -1 --format='%H %ad %s' --date=iso -- dsh-plugin   # 23463d79… 2026-08-15
# 浅克隆没有历史,用一次 API 补(查询日 2026-11-18):
curl -s "https://api.github.com/repos/zhaoolee/notes/commits?path=dsh-plugin&per_page=100" | grep -c '"sha"'  # → 4

# 2) 规模
wc -l dsh-plugin/src/*.ts        # 210 + 510 + 88 = 808
wc -l dsh-plugin/tests/*.ts      # 201 + 440 + 117 = 758
git ls-files | wc -l             # 421
git ls-files '*.ts' '*.tsx' | xargs wc -l | tail -1   # 49069

# 3) 扩散(在 awesome-dsh-plugin 仓库根;data/plugins 有 11744 个文件,必须用目录形式)
grep -ril 'notes' data/plugins/ | wc -l         # 288 —— 泛词,逐条人工筛(简报记 283,本机复现 288)
grep -ril 'zhaoolee' data/plugins/ | wc -l      # 1(自身)
grep -ril 'dsh-notes' data/plugins/ | wc -l     # 9 —— 不同 owner 的本地笔记工具,无引用关系
grep -ril '锤子便签' data/plugins/ | wc -l       # 1(自身)
grep -ril 'notes_export' data/plugins/ | wc -l  # 0
grep -ril 'fangyuanxiaozhan' data/plugins/ | wc -l  # 0

# 4) 实时量(npm 官方 API,2026-11-18 查)
curl -s "https://api.npmjs.org/downloads/point/last-month/@zhaoolee/dsh-notes"          # 685
curl -s "https://api.npmjs.org/downloads/point/2026-08-14:2026-08-19/@zhaoolee/dsh-notes"  # 516(与边车 239 口径不同)
```

**抽样核对**(每条都能 `sed -n` 到):`src/index.ts:140` = `timeoutMs: 60_000`;`src/notes-client.ts:206` = `mkdtemp(...)`;`server/index.ts:287` = `const exportDeviceScaleFactor = 3`;`server/index.ts:4194` = `app.use("/images", express.static(...))`;`tests/package-metadata.test.ts:45-48` = dependencies/peerDependencies 断言。

## 待验证

1. **147 里到底多少来自 DSH**:需要 stargazers 时间序列。`api.star-history.com` 对该仓库返回 `GitHub refused access`,未授权 `stargazers` API 也拿不到 `starred_at`(2026-11-18 尝试)。拿到曲线才能把「5 天增量」从未知变成数字。
2. **演示服务器是否就是本仓库代码的部署**:README 指向同一仓库,但线上是否同版本未验。我只做了两个只读探针(`/api/health`、`/api/auth/session`)和一次空 body 的 `POST /api/export`(500,参数缺失,渲染前就失败、未落盘),**没有真正导出内容**(那会在别人服务器上留一张公开的图)。要断言「公开发布 + 一年缓存」,应在自建实例上复现。
3. **官方插件市场是否收录**:README 说「在 DSH 插件市场搜 `notes` 能装」(`README.md:19-20`)。本机 DSH 有 `dsh-plugin-market` / `dsh-plugin-market-index` 两个包,但我没找到默认索引 URL,也没做搜索实测。
4. **`/api/export` 的 `markdownPath` 风险面**:代码匿名可传(`server/index.ts:831-841`),线上也无鉴权(见上),所以这条路径在演示服务器上大概率可达;我没有用它去读服务器文件(那属于利用),因此只标风险、不下结论。
5. **60 秒超时在真实长对话上的表现**:没跑过长文导出,不知道典型对话是否触发分块拼接、单次渲染耗时多少;这决定「能不能稳定出图」。
6. **`npm test` 未跑**:13 个单测与 3 个打包契约测试是读的,不是跑的;e2e 需 Playwright Chromium。
7. **`skills/notes-export-api` 与插件是否漂移**:注释声称两边逻辑一致(`notes-client.ts:1-8`),我只比了 409 重试与三处端点;脚本 1,105 行里的其余命令(软删除、回收站、公众号 HTML)插件没有,长期是否同构未跟踪。
