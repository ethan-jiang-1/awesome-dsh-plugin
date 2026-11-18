# dsh-openpencil — 预览是外部二进制导出的 PNG,编辑是 loopback 守护进程里的 iframe;插件自己只留能力令牌与草稿事务

> 证据等级:★★★(源码级;`ZSeven-W/dsh-openpencil@56650083e8b1ea01c625b73a4a5c15b98ef53965`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 119、下载 2562 为 2026-08-19 历史采样。
> 2026-11-18 实时星标 **263**(GitHub API,非采样值)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `ZSeven-W/dsh-openpencil`([registry](../../../data/plugins/ZSeven-W__dsh-openpencil.yml)) |
| 类目 | ui([census](../../ecosystem/census.py) 2351 条 / 全表 11744 条) |
| 子分类 | `enhance-shell`(在对话里加一块设计预览/编辑面板,不换壳) |
| 自述 | 「OpenPencil design preview and editing plugin.」——自述只说了形态;源码里是 **14 个工具 + 4 条 HTTP 路由 + 一个受管原生守护进程** |
| 星标 ⚠ | 119(2026-08-19 采样);2026-11-18 实时 263(约 +121%) |
| 下载 ⚠ | 2562(2026-08-19,`data/downloads.json`) |
| 扩散 | **0**(口径:`grep -ril 'openpencil' data/plugins/` 命中 1 条,即本条目自身) |
| 仓库 commit | `56650083e8b1ea01c625b73a4a5c15b98ef53965`(2026-11-11,`fix(runtime): treat workspace-linked npm/<platform> as development package until staged`) |
| 仓库 | 建仓 2026-08-12(API `created_at`),73 个提交,15 个 `v0.1.0-rc.*` 标签,push 到 2026-11-10;TypeScript,5.7 MB(API `size` 5735);15 forks |
| 包形态 | npm `@zseven-w/dsh-openpencil@0.1.0-rc.15`;`dsh.bundle.patch` 一行 insert + **6 个平台二进制可选依赖** + 独立打包的客户端半 `lib/client.js`;engines `node >= 24.11.0` |
| 代码规模 | `src/**/*.ts{,x}` **20 875 行**(其中 `src/client/` 4 928,服务端≈15 947);`tests/*.mjs` 14 165 行 / 18 文件 / 约 370 个 `test()`;`scripts/` 2 993 行 |
| 外部系统 | `ZSeven-W/openpencil`(Rust,7270 星,建仓 2026-02-17,494 MB)——以 submodule 钉死 revision `442c48418697ae944db8bad5bad57f62ee57b1cc`(OpenPencil 0.8.5);另有第二渲染器 `ZSeven-W/jian` |

## 它到底是什么

**不是"一个设计插件",是三层外部系统的 DSH 适配层。** 插件里没有一行光栅化或画布布局代码:预览必须 spawn 一个外部可执行文件,画布必须加载外部 WASM。把它拆成三层最清楚:

| 层 | 归属 | 证据 |
|---|---|---|
| 文档格式 `.op` | OpenPencil | 空文档常量 `{"version":"1.0.0","children":[]}`(`src/editor-host.ts:60`) |
| 精确渲染器 | OpenPencil 的原生二进制 | `--render-shots`(`src/renderer.ts:896`)或 `--mcp` JSON-RPC(`src/renderer.ts:763-800`,工具名 `get_screenshot` / `export_nodes`) |
| 可编辑画布 | OpenPencil 的 Web 宿主 + WASM + CanvasKit | iframe 指向 `${baseUrl}/?embed=vscode`(`src/editor-host.ts:1063`);浏览器侧 `import(sdk.js)` 后 `createViewer({canvas, doc, wasmUrl, canvasKitBaseUrl})`(`src/client/index.tsx:604-609`、`:790`) |
| DSH 适配 | 本插件 | 能力令牌、草稿事务、质量门、版本单调校验、演示元数据恢复 |

**`.op` 的形状**(从代码确证,不是 README 转述):一个 JSON 节点树,顶层 `version` + `children`,可选多页 `pages[]` 与 `editorMeta.activePageIndex`/`active_page_index`(`src/renderer.ts:694-728`);节点字段 `id/type/name/x/y/width/height`(`src/design-tools.ts:35-45`),设计属性含 `layout`/`padding`/`role`/`fill`/`imageSearchQuery`(`src/design-draft-tools.ts:610-624` 的生成契约里可见全貌);测试里的最小样例见 `tests/host-service.test.mjs:313-320`。这是 OpenPencil 自有格式,**不是** SVG、不是 Figma 交换格式——这一条决定了下文的扩散结论。

**三个核心循环**(后文"关键实现"给数据流):

1. **渲染**:`.op` → 冻结快照 → 外部二进制 → PNG → HMAC 签名 URL → `<img>`。
2. **生成/发布**:`pipeline_begin` 开一个 owner 私有草稿 → 至多两个 QuickJS 生成脚本 `I(...)/K(...)` → `finish` 过质量门 → `fs.writeText(kind:'createIfAbsent')` 一次性落盘。
3. **编辑**:能力令牌 → `/editor/<cap>/launch` → 浏览器拿全文 `docJson` 挂 iframe → 用户改 → `POST save` 带 baseline SHA-256 → 同目录临时文件 + `rename` → 发 successor 令牌。

**去掉外部依赖后还剩什么**(这是判断"边界"的关键):质量门(`src/design-quality.ts` 3079 行,纯 JSON 几何/排版/对比度/触控目标/画布契约分析,不碰二进制)、草稿生命周期与 owner 隔离(`src/design-draft-tools.ts:1024-1038`)、文档版本单调性校验(`src/design-draft-controller.ts:936-948`)、签名能力令牌(`src/renderer.ts:350-417`)、Code Mode 演示元数据恢复(`src/presentation-hydration.ts`)、随包 skill 与系统提示(`src/design-skill.ts`)。这些都能跑通并被测试覆盖;**但"预览"和"编辑"两件事会整体消失**——没有二进制就没有 PNG,没有 Web 宿主就没有画布。

## 怎么接进 DSH

**① manifest 只有一行 patch + 一个客户端声明。** `package.json:82-85` 声明 `dsh.bundle.patch → ./cordis.patch.yml`;后者全文 6 行,唯一有效内容是一条 `insert`、`id: dsh-openpencil`、`name: '@zseven-w/dsh-openpencil'`(`cordis.patch.yml:4-6`)。客户端半靠 `dsh.client.inject` 列 5 个官方 UI 包 + `platform: "web"`(`package.json:86-95`);这个键确实被宿主读(`dsh-client-modules/lib/index.js:67`),不是装饰。

**② `dshHostRuntime` 不是契约。** `package.json:97-130` 用 34 行声明 `requiredServices` / `requiredPackages` 与 semver 下限,但 `:129` 自己写着 `"note": "Inert documentation only"`;在本机 DSH 0.2.1-rc.5 全树 `grep -rl dshHostRuntime` **0 命中**。读这张卡时不要把它当成兼容性保障——真正的保障是 `inject` 里的服务名(`src/index.ts:100`)和运行时 `ctx.get('webRuntime')` 的防御式取值(`src/index.ts:164-172`)。

**③ 注册点(服务端,全部走 `ctx.effect`,卸载即撤):**

| 注册 | 位置 | 内容 |
|---|---|---|
| `inject` | `src/index.ts:100` | `tools` / `sessions` / `fs` / `sandboxPolicy`;可选 `webServer`、`connection` |
| `ctx.tools.register` | `src/index.ts:253-283` | 5 个直连工具 + `designDraftTools.createTools()` 的 9 个(7 pipeline + 2 style),共 **14**;名字表 `src/tool-names.ts:2-16,36-45` |
| `skills.register` | `src/index.ts:247` → `src/design-skill.ts:66-81` | 随包 skill `openpencil-design`,`source: 'bundled'`,正文由构建脚本写入 `assets/openpencil-design/SKILL.md`(`src/design-skill.ts:16-19`) |
| `systemPrompt.section` | `src/index.ts:248` → `src/design-skill.ts:84-93` | `name: openpencil:design-skill-guidance`,`order: 130` |
| `agent/request`(waterfall) | `src/index.ts:285-312` | 活跃草稿期间把 DeepSeek 的 `reasoningEffort` 关掉,轮末恢复 |
| `tools/result` | `src/index.ts:313-326` | 观察嵌套结果 + 重新计算草稿归属 |
| `session/event`(`turn/end`) | `src/index.ts:327-335` | 恢复模型档位 |
| `session/disposed` | `src/index.ts:336-352` | 释放 presentation 缓存、模型表,`abortOwner` 清草稿 |
| `connection` | `src/index.ts:354-357` | 把 DSH 的 `requestRejection` 注入编辑器路由(`src/editor-host.ts:261-312`),用于 Desktop 代理不带 `Origin` 的场景 |
| `webServer.register` ×4 | `src/index.ts:363-405` | `/_dsh/dsh-openpencil/render`(prefix)、`/presentation`(exact)、`/viewer-assets`(prefix)、`/editor`(prefix);都很 `kind: 'prefix'/'exact'`,是本机 `dsh-host-webserver` 的真实路由表(`dsh-host-webserver/lib/index.js:327-334,494-501`) |

**④ 注册点(客户端):两个官方 slot + 一次 DOM 改写。** `export const inject = ['slots','theme','locale']`(`src/client/index.tsx:1085`);7 个 `tool.call.toolview` 键(`:1134-1145`,`openpencil_render`/`_new`/`_pipeline_begin`/`_pipeline_finish` + 历史别名 `design_render`,再单列 `_pipeline_inspect`/`_pipeline_batch`),一个 `conversation.input.dock`(`:1147-1150`,`id: 'openpencil-selection'`, `order: 30`)。前者是官方按工具名分发的 keyed slot(`dsh-client-ui-tool/README.md:12`)。**另有一处不是 slot**:后备工作台直接改 DSH 根节点的内联样式 `root.style.marginRight` 并把 `minWidth` 设为 0,带 owner 认领与精确还原(`src/client/editor-dock-layout.ts:22-56`)——这是全仓唯一触碰宿主 DOM 布局的地方。

**⑤ 主题/布局融入**:主题经 `ctx.theme.getTheme().active.colorScheme` + `theme/change` 订阅(`src/client/index.tsx:1089-1090`),再通过 URL/postMessage 传给编辑器 iframe(`src/client/editor-panel.tsx:778-779`);插件自己的卡片只用 DSH 主题变量(`var(--dsw-alias-bg-base)` 于 `src/client/editor-panel.tsx:364`,本机 DSH 安装树里 16 个文件(15 个官方客户端 bundle + web 前端 CSS)用同一变量),没有自带色板。

**⑥ 不需要 patch 宿主**:仓库内没有对 `node_modules` 或宿主源码的改写,安装即 `dsh plugin --profile web add @zseven-w/dsh-openpencil@latest`(`README.md:114-115`)。

## 关键实现

**文件结构(按职责,不是按目录):**

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `src/index.ts` | 412 | 唯一入口:14 个工具、4 条路由、6 个事件钩子、装配与 teardown | `:100`、`:247-283`、`:285-352`、`:363-405` |
| `src/renderer.ts` | 1214 | 二进制发现、快照冻结、PNG 校验、HMAC 能力令牌、符号链接拒绝 | `:498-515`、`:576-616`、`:629-671`、`:763-800`、`:896-926`、`:275-300` |
| `src/editor-host.ts` | 1503 | 受管编辑器:能力令牌、daemon 生命周期、launch/save/selection/recovery、原子写 | `:505-531`、`:989-1100`、`:1199-1255`、`:600-613` |
| `src/design-draft-tools.ts` | 2410 | 7 个 pipeline 工具的契约、质量门编排、`createIfAbsent` 发布 | `:84-95`、`:1127-1135`、`:2194-2249` |
| `src/design-quality.ts` | 3079 | 纯 JSON 设计质量分析(几何/排版/对比/触控/画布契约) | `:1-30`、`:106-160` |
| `src/design-draft-controller.ts` | 1113 | 对 daemon 的 MCP 调用、工具白名单、版本单调性裁决 | `:54-90`、`:890-960` |
| `src/presentation-hydration.ts` | 1173 | 恢复 Code Mode 丢失的浏览器侧元数据(同源 + 会话绑定) | `:52-63`、`:169-170` |
| `src/viewer-assets.ts` | 357 | 4 个 WASM/JS 资产的哈希清单与固定路由,缺失即降级 | `:41-46`、`:162-171`、`:204-210` |
| `src/managed-editor-daemon.ts` | 628 | 拉起原生宿主、握手、只读代理、token 比较 | `:117-125`、`:203-220`、`:379` |
| `src/design-skill.ts` | 94 | 随包 skill + 系统提示段 | `:16-35`、`:66-93` |
| `src/client/editor-panel.tsx` | 1021 | iframe 编辑器面板:消息桥、保存、主题/语言 | `:364`、`:568-620`、`:775-860` |
| `src/client/editor-dock-layout.ts` | 56 | 后备工作台占用宿主右侧布局 | `:22-56` |
| `src/design-tools.ts` | 243 | `create`/`edit`/`selection` 三个直连画布工具 | `:20-23`、`:67-68`、`:103-104` |

**数据流 ①:预览(同步,单次进程)**

```
openpencil_render(path)
  └ resolveInputFile      展开 ~ → realpath → 必须是普通文件且后缀 .op   (renderer.ts:498-515)
  └ createDocumentSnapshot 读字节 → 写进 DSH_HOME/cache/dsh-openpencil/snapshots/<sha>.op  (renderer.ts:519-539, 541-544)
  └ findOpenPencilBinary   OPENPENCIL_BINARY/DESKTOP → /Applications/OpenPencil.app → PATH → 平台包 → op-host-web-server  (renderer.ts:576-600)
      ├ 命中 → spawn --render-shots <doc> <outDir> <scale>   (或回退 --mcp,JSON-RPC 取 base64 PNG)
      └ 未命中/ENOENT → findJianBinary → spawn jian render --out            (renderer.ts:604-616, 629-671)
  └ verifyRenderOutput    PNG 魔数 + 尺寸 + sha256                          (renderer.ts:1186)
  └ RenderAccessController.signArtifact   base64url(payload).hmac           (renderer.ts:394-400)
  └ presentationMeta.$dshOpenPencil   → ToolCallBlock.meta → <img src=/_dsh/.../render/<token>>
```

模型看到的永远是纯 JSON(`render: renderJson`,`src/tool.ts:154`);**故意不返回 ImageBlock**——文件头注释写明 DeepSeek adapter 会在请求任意位置拒绝 image block(`src/index.ts:10-14`、`src/tool.ts:6-9`)。浏览器专属的信封走 `output.presentationMeta`(`src/tool.ts:155`),这与 DSH 官方 `read`/`web` 工具用的是同一条机制(`dsh-tools/lib/types/presentation.d.ts:257`)。路由不可用时 `projectRenderGrant` 原样返回(`src/renderer.ts:1006`),卡片退化成纯 JSON,不会挂死链。

**数据流 ②:生成与发布(事务,owner 隔离)**

```
pipeline_begin  → 建私有草稿(目标 .op 尚不存在)                     design-draft-tools.ts:1060-1280
  ├ sandboxPolicy.resolve + mode==='read-only' → 直接拒绝              :1127-1129
  ├ fs.resolve(workspaceRoot) + lstat 目标不存在                       :1131-1148
  └ 返回 rootNodeId + 两批 QuickJS 契约(第一批 ≤32 次 I/K、≤8 KiB)     :611-624
pipeline_batch  → 模型写 I(parent,node)/K(kitId,...) 脚本 → daemon 执行   :1399-1420
  └ 每次调用前后取文档 version:必须单调增;读工具不许改版               design-draft-controller.ts:936-948
pipeline_finish → 原生 finalize/lint/layout + DSH 质量门 + 精确 PNG
  └ fs.writeText(target, docJson, {kind:'createIfAbsent'}, signal, policy)   :2238-2244
  └ emit('fs/observed', …) 提交后尽力而为                              :2249-2253
```

`createIfAbsent` 是 DSH 的真实守卫意图(存在即 `FS_NOT_OBSERVED` 失败,`dsh-fs/lib/types/types.d.ts:106-112`),所以**发布路径不可能覆盖用户已有文件**;`finish` 之前还会重查目标身份(`:2198-2202`),防 TOCTOU。

**数据流 ③:编辑(长连接,浏览器持有全文)**

```
presentationMeta.editor = /editor/<cap>/launch      grantFor 只接受绝对 .op + 合法 sha256   (editor-host.ts:600-613)
  └ spawn op-host-web-server → 等握手(20s) → 校验 runtime 版本与 revision               (:1040-1051)
  └ 返回 { docJson, iframeUrl, token, saveUrl, selectionUrl, recoveryUrl }              (:1091-1097)
浏览器 iframe(/?embed=vscode) ← postMessage → 面板;主题/语言不重载 iframe              (client/editor-panel.tsx:775-860)
POST /session/<id>/save  { docJson, generation, revision }
  └ sha256(当前磁盘) !== session.baselineSha256 → 409 "source changed outside this editor"   (:1217-1220)
  └ 同目录 .<name>.dsh-save-<uuid>.tmp → fsync → rename                                  (:518-527)
  └ 新 baseline + successor 能力令牌                                                      (:1231-1252)
```

能力令牌是 HMAC-SHA256(`src/renderer.ts:394-400`)、2 小时 launch / 24 小时 refresh(`src/editor-host.ts:46-47`),且 `v2` 载荷**不嵌绝对路径**(只放 filename/bytes/sha256,`src/renderer.ts:236-250`),所以浏览器元数据里拿不到宿主路径。

**测试能证明的契约**:18 个 `*.mjs`、14 165 行、约 370 个 `test()`。分工很清楚——`client.test.mjs`(2521 行 / 99 测试)在伪造的 `__ModuleLoader__` 里加载真实客户端包(`tests/client.test.mjs:11-20`),`editor-host-lifecycle.test.mjs`(1328 行)测 launch→save→刷新→恢复全链,`presentation-hydration.test.mjs`(1324 行)测恢复端点的严格解析,`design-draft-tools.test.mjs`(2309 行)测两批脚本与修复轮。CI 分两个 job:JS 侧 `test:viewer-assets → test:client → test:host-api → test:mcp`(`.github/workflows/check.yml:84-104`),Rust 侧对 submodule 跑 `cargo test -p op-host-web-server`(`:164`)。另有一份 `docs/PATTERN-AUDIT.md`(2026-09-06)记录一次真实驱动里发现的"触控目标 44px 与容器流互斥"缺陷,并有对应回归测试(`tests/pattern-audit-regressions.test.mjs:1-8`)——把审计结论钉成可执行断言。

## 为什么它突出

**先拆星标归属,结论是干净的,但来源要打问号。**

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-02-17 | 同 owner 的 `ZSeven-W/openpencil` 建仓,现 7270 星、Rust、494 MB | GitHub API |
| 2026-08-12 | 本仓库建仓(空) | API `created_at` |
| 2026-08-13 | 首次提交 `feat: add OpenPencil plugin for DSH` | `git log --reverse` |
| **2026-08-19** | **119 星采样点** | registry ⚠ |
| 2026-10-07 | Merge PR #8(style picker 集成) | `git log` |
| 2026-11-10 | `0.1.0-rc.15` + 最后一次 push | tag / API `pushed_at` |
| 2026-11-18 | 263 星(实时)、15 forks、1 个 open issue | GitHub API |

仓库**就是**插件,没有 monorepo 子目录,所以 119 与 263 都记在这个插件头上,不存在"宿主项目背书"的错配。但要看清两件事:① 119 星是在**建仓后 6 天内**(08-12 建仓、08-13 首提交、08-19 采样)拿到的——这个速度不可能是自然传播,发现路径几乎只有主项目 OpenPencil(7270 星)的视线;② 下载 ⚠ 2562 对星标 ⚠ 119 是 21:1,典型的"装了但不 star、更不提"。**判断:声量来自母项目漏斗,不是本插件在 DSH 生态里长出来的。**

**再解释零扩散——这个形态为什么没抄开。四个理由,按解释力排序:**

1. **格式是别人的,而且是私有的。** 预览只认 `.op`(`src/renderer.ts:498-515` 硬性后缀检查),`.op` 是 OpenPencil 的 JSON 节点树。第三方要复现"设计预览",第一步就得先有 `.op` 文件——而产出 `.op` 的工具只有 OpenPencil 自己。
2. **渲染器是别人的原生二进制,不是库。** 精确预览要 spawn `openpencil-desktop` / `op-host-web-server`(`:576-600`);编辑器要拉起一个 loopback HTTP 守护进程并完成端口/token/版本握手(`src/managed-editor-daemon.ts:203-220, 379`)。这不是 `import` 一个包能拿到的能力,连本项目都要靠 submodule + Cargo + wasm-bindgen + Binaryen 在 CI 里编译(`README.md:246-262`)。抄的人得先接管一条 Rust 发布链。
3. **适配层本身厚到不可抄。** 服务端 15 947 行 + 客户端 4 928 行 + 14 165 行测试,里面大量是产品化细节(能力令牌、草稿事务、质量门、元数据恢复、DOM 布局认领)。可复制性与体量成反比:**薄适配层谁都能抄,厚适配层谁都不想抄。**
4. **生态是闭环的。** 设计文档的生产者也是本插件(`openpencil_pipeline_*`),消费者也是本插件(`openpencil_render`),中间是它自己的守护进程。没有留出"别人接进来"的 seam——没有共享配置、没有公共 ABI、没有可供第三方注册的扩展点。

**机制独特性**(只用本插件自身证据):在 11 744 条里,它把"设计文档 → 精确 PNG → 可编辑画布 → 事务化发布"串成**一条**模型可调用的流水线,并且对每个环节都做了内容寻址与版本裁决。最有说服力的一条是版本单调性:每一个 MCP 调用前后都取文档 version,读工具**不许**改版、写工具**必须**改版,回退即销毁会话(`src/design-draft-controller.ts:936-948`)——这是把"模型幻觉式成功"当成可检测故障来处理的写法。

## 代价与边界

- **权限边界不对称,这是最该注意的一条。** 读侧绕开了 DSH 的 fs 层:`openpencil_render` 用裸 `node:fs` 做 `realpath`/`stat`(`src/renderer.ts:498-515`),既不调 `ctx.fs.resolve` 也不读 `sandboxPolicy`(`src/tool.ts` 全文件 0 命中),只验 `~` 展开、普通文件、`.op` 后缀。DSH 官方读工具走的是 `ctx.fs.resolve`(`dsh-tool-fs/lib/index.js:192`),被挂载的 fs 后端可以在这里做隔离;本插件的读路径不经过那一层。**后果:凡是被挂载 fs 拦下的位置,只要宿主进程 OS 权限够,`openpencil_render` 仍能读**——读到的东西不进模型上下文(只有 PNG 给浏览器、快照可下载),但确实是模型触发的一次越层读取。写侧相反:`openpencil_new` 与 `pipeline_finish` 都先 `sandboxPolicy.resolve`、`read-only` 下硬拒绝(`src/new-tool.ts:161-164`、`src/design-draft-tools.ts:1127-1129`、`:2194-2196`),再走 DSH 的 `fs.writeText`。
- **编辑器保存绕开 DSH fs 抽象。** save 是 `node:fs` 直接写:同目录临时文件 + `rename`(`src/editor-host.ts:518-527`),不经过 sandbox 策略,唯一的准入是"路径由本插件先前 mint 过能力令牌 + baseline SHA-256 未变"。这是有意的(要保留文件 mode、要原子替换),但它意味着**保存权限 = 宿主进程权限**,而不是会话的 sandbox 模式。
- **原生二进制是硬依赖。** 无 OpenPencil 二进制时降级到 `jian render`,产物标 `fidelity: 'runtime-preview'` 并附 warning(`src/tool.ts:165-216`);`width`/`height` 只有这条降级路径支持,精确路径传了就抛错(`src/tool.ts:168-171`)。**`jian` 也没有时,错误是裸的 `spawn jian ENOENT`**——`runJianRender` 只 `reject`(`src/renderer.ts:663`),没有像 OpenPencil 分支那样包成 `RendererBinaryMissingError` 并给出可读信息(`:804`)。glibc-only:musl 无平台包(`platforms.json:20-40`)。
- **失败模式,按发生顺序:**
  1. 路径不是普通文件 / 后缀不是 `.op` → 立刻抛错,不 spawn(`src/renderer.ts:498-515`)。
  2. 文档不是合法 JSON → `sourceFrameDescriptors` **静默吞掉**返回 `[]`(`:723-728`),只丢多帧画廊;精确渲染器仍会以非零退出并抛 stderr(`:926`)。
  3. 渲染超时 60 s 或取消 → `SIGKILL` + 超时错误(`:52`、`:812`/`:922`)。
  4. 交付阶段文件被换/被链 → 逐段 `lstat` 拒绝符号链接 + `realpath` 包含检查 → 404(`:275-300`、`:464-468`)。
  5. 编辑器 runtime 缺失 → `available === false`,`grantFor` 返回 `undefined`(`src/editor-host.ts:600-604`),卡片文案为 "Editable OpenPencil canvas is not available for this result."(`src/client/index.tsx:305`)。
  6. 并发编辑 → baseline SHA 不匹配,409 且**不覆盖**(`src/editor-host.ts:1217-1220`);DSH 重载时脏画布落 7 天恢复草稿,需用户显式恢复才回灌(`src/editor-recovery.ts:9-10`、`:306`)。
  7. viewer 资产缺失 → `available === false`,不挂路由、不显示画布按钮(`src/viewer-assets.ts:204-210`),PNG 路径不受影响。
- **资源上限**(每一条都是硬编码,不是可配):PNG 32 MiB、文档 64 MiB、单边 32 768 px / 1.28 亿像素、单次渲染 60 s(`src/renderer.ts:42-52`);生成脚本 256 KiB、首批 8 KiB / 32 次调用、截图 16 MiB、修复轮 2(`src/design-draft-tools.ts:84-95`);质量分析最多 10 000 节点(`src/design-quality.ts:5`);恢复记录 7 天 / 32 个文件(`src/editor-recovery.ts:9-10`);元数据恢复 128 帧(`src/presentation-hydration.ts:63`)。
- **进程与网络**:每次精确渲染 spawn 一个进程;每个可编辑画布常驻一个 loopback daemon(20 s 启动超时、4 h 空闲回收,`src/editor-host.ts:48-50`)。daemon 只监听 `127.0.0.1` 且带 token(`src/managed-editor-daemon.ts:117-125, 379`),但**官方平台包在构建期把两个协作 bootstrap 端点编进原生二进制**(`scripts/collab-bootstrap-config.mjs:6-9, 26-28`),本仓不含端点值;该协作面在 DSH 编辑器里是否暴露未验证。
- **维护成本高且双向耦合**:对 DSH 侧要跟 `reasoningEffort` 锁(0.2.2 变更,`src/index.ts:285-312` 与最近一次修复提交)、locale 返回值形态(`src/client/index.tsx:1095`)、slot 契约三处;对 OpenPencil 侧钉死 `442c484…` 与 0.8.5(`platforms.json:4-6`),升级要重编 wasm + 原生二进制 + 六平台包。15 个 rc 标签、3 个月 73 个提交,基本是一支团队的全职节奏。

## 可信度与复现

证据等级 ★★★,但**只限本插件**:OpenPencil 主项目(Rust,494 MB)与 `jian` 的源码未读,所有关于它们的判断都来自本插件的调用方式、`platforms.json` 与 README。本机 DSH 为 0.2.1-rc.5,插件 devDeps 钉 0.2.0-rc.2,README 声明编辑器面验证于 0.2.1-rc.3——三个版本号不是同一个。

```sh
git clone https://github.com/ZSeven-W/dsh-openpencil.git /tmp/an-openpencil
cd /tmp/an-openpencil && git log -1 --format='%H %ad %s'
# → 56650083e8b1ea01c625b73a4a5c15b98ef53965 Wed Nov 11 02:19:50 2026 +0800 …
git rev-list --count HEAD          # → 73
git tag | wc -l                    # → 15
git ls-tree HEAD vendor/           # → 160000 commit 442c48418697ae944db8bad5bad57f62ee57b1cc vendo…

find src -type f \( -name '*.ts' -o -name '*.tsx' \) -print0 | xargs -0 wc -l | tail -1   # → 20875
find src/client -type f \( -name '*.ts' -o -name '*.tsx' \) -print0 | xargs -0 wc -l | tail -1  # → 4928
find tests -name '*.mjs' -print0 | xargs -0 wc -l | tail -1                              # → 14165
grep -cE '^\s*test\(' tests/*.mjs | awk -F: '{s+=$2} END {print s}'                     # → 370

# 扩散(在 awesome-dsh-plugin 仓库根;data/plugins/ 有 11 744 个文件,必须用目录形式)
grep -ril 'openpencil' data/plugins/ | wc -l        # → 1(只有它自己)
grep -ril 'dsh-openpencil' data/plugins/ | wc -l    # → 1

# DSH 侧契约核实
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh
grep -rl dshHostRuntime $DSH | wc -l                                    # → 0(该字段无人读)
grep -n 'dsh.client.inject' $DSH/node_modules/@deepseek-ai/dsh-client-modules/lib/index.js   # → :67
grep -n 'createIfAbsent' $DSH/node_modules/@deepseek-ai/dsh-fs/lib/types/types.d.ts          # → :106-112
grep -n 'super(ctx, "skills")' $DSH/node_modules/@deepseek-ai/dsh-skill/lib/index.js         # → :132
grep -n "tool.call.toolview" $DSH/node_modules/@deepseek-ai/dsh-client-ui-tool/README.md     # → :12
```

读过的文件:`package.json`、`cordis.patch.yml`、`.gitmodules`、`platforms.json`、`pnpm-workspace.yaml`、`README.md`(全文关键段)、`docs/PATTERN-AUDIT.md`、`.github/workflows/{check,release}.yml`、`src/index.ts`、`src/tool.ts`、`src/tool-names.ts`、`src/renderer.ts`(全文)、`src/viewer-assets.ts`(关键段)、`src/editor-host.ts`(关键段)、`src/editor-runtime.ts`(头部)、`src/editor-recovery.ts`(头部)、`src/managed-editor-daemon.ts`(头部)、`src/design-draft-tools.ts`(关键段)、`src/design-draft-controller.ts`(关键段)、`src/design-tools.ts`、`src/new-tool.ts`(写入段)、`src/design-quality.ts`(头部)、`src/design-skill.ts`(全文)、`src/presentation-hydration.ts`(头部)、`src/client/index.tsx`(关键段)、`src/client/editor-dock-layout.ts`(全文)、`src/client/editor-panel.tsx`(样式与 iframe 段)、`scripts/{build-client,stage-editor-runtime,collab-bootstrap-config}.mjs`、`tests/{client,host-service,pattern-audit-regressions}.test.mjs`(头部与用例清单)。本机 DSH:`dsh-client-modules`、`dsh-fs`(类型)、`dsh-sandbox-policy`、`dsh-skill`、`dsh-system-prompt`、`dsh-host-webserver`、`dsh-tools/presentation` 的类型/实现关键行。

**未读**:`vendor/openpencil`(浅克隆未取子模块,目录为空)、`src/style-planner.ts`/`src/style-catalog.ts`/`src/design-knowledge.ts` 的选风格算法、`src/design-visual-review.ts` 的评审清单生成、`src/client/frame-gallery.tsx` 的画廊交互、`tests/style-picker.test.mjs` 与 `tests/design-quality.test.mjs` 的 2491 行断言细节。

## 待验证

1. **无 `/Applications/OpenPencil.app`、无 `jian` 的干净机器上,`openpencil_render` 的实际报错文本**——按代码应是 `spawn jian ENOENT`(`src/renderer.ts:663`),未实跑;这决定了首个失败体验是否可读。
2. **`openpencil_render` 的越层读取能落多远**:需实测一个被挂载 fs 限制的会话里渲染 `/tmp/x.op` 是否成功、`download=1` 是否能取回快照;若宿主用的是把工作区外读请求整体拒绝的 fs 后端,本插件这条裸 `node:fs` 路径就是唯一没被覆盖的口子。代码上没有拦截,但未跑过。
3. **编辑器 save 的 sandbox 关系**:`sandboxPolicy` 在 `src/editor-host.ts` 里 0 命中已确认;但 DSH 是否在 webServer 路由层对写请求另设准入门,未核。这决定"保存权限 = 宿主权限"这句话的强度。
4. **平台包的实际体积与首启耗时**:`npm/*/bin` 不在 git 里(由 `scripts/stage-editor-runtime.mjs` 构建期生成),⚠ 下载 2562 是否含 6 个平台包也未核;`RENDER_TIMEOUT_MS` 60 s 对真实大文档是否够用也未测。
5. **协作 bootstrap 是否在 DSH 编辑器面暴露**:`scripts/collab-bootstrap-config.mjs` 证明端点被编进二进制,但插件源码里 `grep -rn 'collab' src/` 0 命中——是纯运行时内部行为,还是 DSH 面板可达,需在打包产物上查。
6. **263 星与 2562 下载的时间曲线**:缺 2026-08-19 之后的采样点,无法判断增长是母项目带量还是 DSH 生态内真实扩散;本卡只能给两个时点的快照。
7. **`openpencil_pipeline_agent_run`(engine: 'app-agent')的实跑**:它把生成交给 daemon 内置的 design-agent 循环(`src/design-agent-run.ts:1-40`),本次只读了契约与校验函数,未跑;这条路径与两批 QuickJS 路径的产出质量差异无法判断。
