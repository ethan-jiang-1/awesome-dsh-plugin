# dsh-TUI — 把 DSH 换成终端应用:自带启动器、自带组装根,不是给 web 壳加面板

> 证据等级:★★★(源码级;`repo@commit 2d6c9a13fc30358913e88129c79640d50ca0c6db`,2026-11-17)。
> 数据截止 `29b3ed46e`(2026-11-17)。⚠ 星标/下载为 2026-08-19 历史采样。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `ccch1mneyyy/dsh-TUI`([registry](../../data/plugins/ccch1mneyyy__dsh-TUI.yml)) |
| 类目 | ui(路线:`replace-shell` 换壳,见 [replace-shell/README.md](replace-shell/README.md)) |
| 自述 | "Claude Code 风格全屏终端 UI:像素鲸鱼顶栏、实时工作状态行、思考流式展开"(registry 一句话;实际体量比这句大一个量级) |
| 星标 ⚠ | 2009(2026-08-19;ui 内第二,第一是 better-sidebar 2216) |
| npm 月下载 ⚠ | 16959(2026-08-19) |
| 扩散 | 8 条第三方提及:**2 条真在对接**(`Enc-hanted/dsh-pulse` 的"dsh-tui 终端面"、`jakehemmerle/dsh-speed` 要求"patched dsh-TUI"),1 条并列提及(`jakehemmerle/dsh-web-search-exa`),5 条同名/同类独立实现(`fan56/dsh-tui-pi`、`kouyichi/dsh-tui-app`、`lk251066/dsh-tui-pro`、`tomowang/dsh-tui`、`xiaoshihou514/dsh-tui`)。复现:`grep -ril "dsh-tui" data/plugins/*.yml \| wc -l` → 9(含自身) |
| 仓库 commit | `2d6c9a1`,2026-11-17 17:59 +0800;包版本 `@deepseek-harness-tui/dsh-tui@0.20.1`,MIT |
| 包形态 | npm 包 + DSH bundle 双角色:`bin` 提供 `dsh-tui` / `dst` 启动器;`package.json:602-605` 的 `dsh.bundle.patch: "./cordis.patch.yml"` 让同一包又是 DSH profile 的一个 bundle 层。**全仓没有 `dsh.plugin.json`**(`find -name 'dsh.plugin.json'` 无结果) |
| 代码规模 | `src/` 1835 文件 / 251,109 行 TS/TSX(1659 `.ts` + 174 `.tsx`);`bin/dsh-tui.js` 1800 行;`scripts/` 870 文件、`package.json` 156 个 script(其中 137 个 `verify:*`);`cordis.patch.yml` 48 个行条目 / 499 行 |

## 它到底是什么

三条来自代码的断言:

1. **它已经不是一个"插件",而是自带入口与组装根的终端应用。**`bin/dsh-tui.js:79` 定义 profile 名 `dsh-tui`,首跑调 `dsh plugin --profile dsh-tui add <pkg>@<ver>` 自举(`bootstrapProfile`,约 1376 行),成功后 spawn `lib/types/dsh-adapter/host-entry.js`(源码 `src/dsh-adapter/host-entry.ts`)。host-entry 用 `findHostDsh()` 沿 PATH 按 realpath 定位已安装的 `dsh`,把**宿主自己的** `Context` / `appBoot` / Loader / `homePaths` 加载起来,建一个 Cordis 根,再把这个根的 profile 组合进去(`host-dsh.ts:1-20` 头注释;`host-contract.ts:31` 的 `HOST_MODULES`)。内核仍是 DSH,宿主进程变成 dsh-TUI 自己的。
2. **它不接管 web UI,它根本不起 web UI。**`cordis.patch.yml` 展开是:20 条 `insert`(全是自己的 `dsh-tui-*` 行)+ 6 条 config override(`system-prompt`/`llm-deepseek`/`agent-loop`/`sandbox-policy`/`approval`/`session-persistence-jsonl`)+ 21 处 `disabled: true` 把 dsh-base 的工具/命令行让给 agent preset(`cordis.patch.yml:57-171`)。`patch-surface.snapshot.json` 的 `webAppComparisons` 对 21 个宿主版本都记着 `insertsSharedWithWebApp: []`——与官方 web-app 的插入行**零交集**。
3. **一个进程只有一棵 UI 树。**`plugin.ts:3578-3610` 组树(fullscreen 时 `AlternateScreen` → `PageMargin` → `Chat`),`render(tree, { exitOnCtrlC: false })` 挂载,`instance.waitUntilExit().then(handleExit, handleExit)`(3859 行)在 TUI 卸载时收进程。patch 里 `dsh-tui` 行(408 行起)的注释写的是同一件事:"disposes the whole app tree (exiting the process) when the TUI unmounts"。

## 怎么接进 DSH

- **manifest**:没有独立清单文件。接口就是 `package.json` 的 `dsh.bundle.patch`(`package.json:602-605`,**字符串**;对照官方 `@deepseek-ai/dsh-web-app` 同字段是 5 个 patch 的数组,`@deepseek-ai/dsh-base` 是 1 个)。DSH 侧消费点是 `@deepseek-ai/dsh-plugin-manager` 的 `bundleManifest()`(本机装的 0.2.1-rc.5,`lib/index.js:313`:`manifest.dsh?.bundle?.patch === void 0 ? void 0 : manifest`)——没有这个字段的包不算 bundle。
- **插件入口**:`src/index.ts` 只有一行 re-export;插件面在 `src/dsh-adapter/index.ts`:`export const name = 'dsh-tui'`(23 行)、`export const inject = ['agents']`(33 行)、`export const Config`(315 行,Schemastery schema)、`apply` 用动态 import 转给 `plugin.js`(506-517 行)。真正的运行时是 `plugin.ts:969` 的 `apply(ctx, runtimeConfig, configOwner, runtimeOptions)`。
- **接管方式**:**换 profile,不是加面板**。`dsh plugin --profile dsh-tui add` 建一个以 dsh-base 为底的 profile,把本包追加为 bundle 层;这个 profile 里唯一的界面行就是 `- id: dsh-tui`(`cordis.patch.yml:408`)。所谓"接管",其实是**这个 profile 里没有第二个壳**——web 界面不在组合里,而不是被顶掉。
- **与内置 web UI 的关系**:可共存,且每条宿主面行都会让位。insert 的行普遍带 `disabled: !!js "[...ctx.loader.entries()].some(e => e.options.id === '<官方 id>' && e.options.name === '<官方包>' && !e.disabled)"` 这类自检(218-290 行的 storage/workspace/code-runtime 组、321-376 行的 preset 组同理);`dsh-tui-webserver`(377 行)只在有 DeepSeek 账号服务、需要 OAuth 回环时才开(`host: 127.0.0.1, port: 0`),没有账号服务就整行 disable。`scripts/verify-web-coexistence.mjs` 是这条纪律的回归闸门(文件头注明"mixed dsh-web + dsh-tui profiles")。
- **注册点**:`package.json` 的 `exports` 给了 12 个服务子路径 + 1 个 `./invariant`;其中 9 个在 patch 里有对应行:`/workspaces`(273)、`/command-trees`(278)、`/settings-sections`(282)、`/scenes`(288)、`/panels`(294)、`/plugin-host`(303)、`/extensions`(312)、`/oauth`(399)、`/working-activity`(495);`/api`、`/preset-patch`、`/jsx-runtime` 是给插件 import 的库面,不占行。**这些都不是给 DSH 的,是给它自己生态里的第三方插件用的**(见「关键实现」末段);给 DSH 的注册点只有 `- id: dsh-tui` 一行。

## 关键实现

**文件结构(行数为实测)**

```
bin/dsh-tui.js              1800   零 lib 依赖启动器:版本对齐、doctor、safe(救援 profile)、update、migrate
src/dsh-adapter/          65,403   250 文件;唯一允许 import @deepseek-ai/* 的目录
  ├─ host-entry.ts / host-dsh.ts / host-contract.ts   取宿主 root、装载宿主模块、复刻指纹
  ├─ plugin.ts             4,662   TTY 门禁、服务注册、agent 创建/恢复、React 树挂载与收尾
  ├─ index.ts                568   插件面(name/inject/Config/apply)
  └─ backend/{session,translate}.ts  一个 Agent → AgentSession 的翻译层
src/ink/                  36,721   132 文件;Ink 系渲染器(自有 reconciler、DOM、布局、帧差分、输入)
src/components/           44,536   202 文件;design-system/ 是主题感知原语
src/backends/             29,179   975 文件;claude(Agent SDK)、codex(app-server) 两个非 DSH 后端
src/adapter/              13,717   88 文件;ports/(19 个端口文件)+ kernel/ + standard/ + upstream/
src/screens/Chat.tsx       7,741   交互协调器:按键优先级、模式、面板、选区
src/channel/               5,244   21 文件;共享投影器与其他后端中立的 store
src/native-ts/yoga-layout  3,303   纯 TS 移植的 Yoga flexbox(单文件 index.ts 100 KB)
```

**渲染栈**:用的不是 npm 的 `ink`(`dependencies` 里没有它,只有 `keywords` 里有)。`src/ink/reconciler.ts:4-5` 直接 `import createReconciler from 'react-reconciler'` 并配本地 `dom.ts`;布局不用 `yoga-layout` 包,用 `src/native-ts/yoga-layout/index.ts` 的纯 TS 移植(文件头自述覆盖 "the subset of features Ink actually uses")。对外门面 `src/ui.ts` 导出 `render` / `Box` / `Text` / `AlternateScreen` / `ScrollBox` / `useInput` 等。全屏是默认:patch `fullscreen: true`(`cordis.patch.yml:437`),schema 注释也写默认 true(`index.ts:114-118`),两侧注释互相要求同步翻转;实现是 DEC 1049 alt-screen + SGR 鼠标跟踪(`plugin.ts:3578-3587` 注释)。

**数据流(DSH → 屏幕)**

```
DSH 内核 Agent / Session
  ├─ 用户提交: session.submit(input, placement) → agent.followup(message)     backend/session.ts:326-345
  ├─ 回放种子: opened.history → feed.bind(history)                            channel/core/compose.ts:936-988
  └─ 实时事件: ctx.on('session/event', (subject, event) => …)                  backend/session.ts:120
        → rawListeners(DSH 扩展先看)→ translate.ts 翻成 AgentEvent
        → channel/projection.ts 折成 ChatRow
        → ChannelState → screens/Chat.tsx → src/ink 渲染成帧
```

`session/event` 同时只挂一个前台监听(`eventTap`,单订阅期共享,`backend/session.ts:104-135`);压缩进度另从 `llm/stream` 的 `purpose === 'compaction'` 分支取(同文件 306-320 行)。后端中立层意味着 Claude/Codex 后端复用同一条 channel——它们没有 `native.dsh` 能力,`channel/extensions.ts` 就不挂 DSH 扩展(`channel.ts:1-6` 头注释)。

**它自己也是一个插件宿主**:`src/dsh-adapter/plugin-host.ts:1-40` 声明 `ctx.tuiPluginHost` 提供 `generationId`(每次行激活一个新 UUID)、`grants`(统一 8 权限 GrantStore)、`hostDescriptor()`、`selfCheck()`、`registerCommand()`(带 C-041 归属校验)。权限清单在 `tui-profile/registry/permissions-0.1.json`(8 条:`storage.local.read/write`、`messages.observe.read`、`commands.invoke` 及 4 个 `session.*.intercept`,后者默认 deny),私有协议坐标是 `tui.dsh/v1alpha1`(`tui-profile/protocols/tui-contributions.js:3`),准入册 `tui-profile/registry/registry-0.15.json`(161 行)配 conformance runner(`tui-profile/scripts/conformance.mjs`)。

## 为什么它突出

**它和 better-sidebar 不是同一类东西,星标接近是巧合。**

| | [better-sidebar](01-better-sidebar.md) | dsh-TUI |
|---|---|---|
| 路线 | 增强现有壳(web UI 里加侧栏/Tab) | 换壳(自己起进程、自己组 profile) |
| 依赖宿主的什么 | 一个注册点(Tab API) | **装载语义**:profile / bundle patch / 行 id / loader 行为 / `session/event` / `Agent.followup` |
| 失效时的表现 | 少一块面板 | 整个界面起不来 |
| 兼容成本落在哪 | 跟随 web 客户端 API | 跟随 40 个官方包的版本线(`peerDependencies` 逐版本枚举,最长一条列了 21 个版本) |
| 扩散形态 | 63 条第三方点名(接入深度待验证) | 8 条提及,其中 2 条真对接 |

比星标更能说明路线代价的是规模:为了"只消费 DSH 公开导出",它养了 137 个 `verify:*` 关卡、一个 `host-replica.snapshot.json`(记录 0.2.2-rc.3 宿主上 8 个被复刻符号的 sha256)、一个 `patch-surface.snapshot.json`(对 21 个版本记录"比 web-app 多关了哪些行",最新一版多关 `tool-ralph` 与 `tool-subagent-list-agents`)。**换壳的成本不在写界面,而在把宿主的每次漂移都变成自己的回归用例。**

另一面是它在把自己做成第二个平台:`tui-profile/` 是它自己的准入册,`plugin-host`/`extensions`/`scenes`/`panels` 是给第三方的接缝。但扩散还没到锚的量级——`dsh-speed` 的自述是"the terminal controls need a patched dsh-TUI",说明 ABI 还没稳到"免补丁"。**声量是锚级,扩散还只是苗子。**

## 代价与边界

- **终端能力边界**:全屏靠 alt-screen + SGR 鼠标跟踪,图片靠 sixel / kitty / iTerm 协议(`src/ink/terminal-image.ts`、`sixel.ts`、`kitty-graphics.ts`),公式与流程图走 `src/math/` + `src/terminal-utils/mermaid.ts`(依赖 `lovely-mermaid`);协议探测不到时退回纯文本。
- **TTY 是硬门禁**:`resolveTuiHostMode()`(`plugin.ts:198-217`)三态——显式 `dsh-tui` 启动且 stdout 非 TTY → **抛错退出**(1099-1103 行);别的 GUI/headless 宿主加载到这一行且非 TTY → **静默跳过**(1105-1110 行),让宿主继续启动。这条设计是它能与 web 混装的前提,也是"换壳但不必独占 profile"的退路。
- **权限**:对 DSH 侧没有权限声明,它可做之事等于 profile 里 dsh-base 给出的行;但它 override 了 `sandbox-policy` 与 `approval`(`cordis.patch.yml:177-190`),并作为交互应答方接管审批与提问(`ApprovalStore`/`QuestionStore`,`plugin.ts` 导入段与 2943 行 `approvalStore.noteSessionEvent`)。**换壳的插件顺手接管了"谁回答权限问题"——这比渲染层敏感得多。**
- **外部依赖**:39 个 runtime 依赖(react 19、react-reconciler 0.34、marked、highlight.js、lovely-mermaid、sixel、ws、zod、yaml;`sharp` 为 optional)+ 40 个 peerDependencies(整套 `@deepseek-ai/*`)。宿主 `dsh` **不在依赖里**:按 PATH realpath 加载;版本错位由 `checkProfileAlignment()`(bin/dsh-tui.js 内)拒绝委托并给对齐命令。
- **失败模式**:启动器自带 `doctor`(环境诊断)、`safe`(救援 profile `dsh-tui-safe`,bin/dsh-tui.js:108)、`update`、`migrate`,四者都写明"零 lib 依赖、profile 炸了也要能跑"。这些子命令本身就是对失败率的承认——文件注释里列着半装/`no-op 假成功`/跨内核会话 id 串台/半更新等具体故障域(`bootstrapUnreadable`、`createRescueProfile` 段落)。

## 可信度与复现

- 证据等级 **★★★**。读了:`package.json` 全文、`cordis.patch.yml` 全文、`bin/dsh-tui.js`(版本/doctor/safe/委托段)、`src/index.ts`、`src/dsh-adapter/{index,plugin,host-entry,host-dsh,host-contract,backend/session,channel/core/compose,plugin-host}.ts`、`src/ui.ts`、`src/ink/reconciler.ts`、`tui-profile/registry/{permissions-0.1,registry-0.15}.json`、`tui-profile/protocols/tui-contributions.js`、两份 snapshot、`AGENTS.md` 仓库地图;并对照本机 DSH 0.2.1-rc.5 的 `dsh-plugin-manager`、`profile-boot`、`dsh-base`、`dsh-web-app` 包。
- 复现:

```sh
git clone --depth 1 https://github.com/ccch1mneyyy/dsh-TUI.git /tmp/an-tui
git -C /tmp/an-tui rev-parse HEAD                                  # 2d6c9a13…c6db
git -C /tmp/an-tui log -1 --format='%ad %s'                        # 2026-11-17 17:59 +0800
node -e "console.log(require('/tmp/an-tui/package.json').dsh)"      # { bundle: { patch: './cordis.patch.yml' } }
grep -c 'id:' /tmp/an-tui/cordis.patch.yml                          # 52(含注释里的 id)
grep -c '^- id:\|^    - id:' /tmp/an-tui/cordis.patch.yml           # 48 个真实行条目
grep -ril 'dsh-tui' data/plugins/*.yml | wc -l                       # 9(含自身)
```

- **未读部分**:
  - `vendor/dsh-std` 是 git submodule,浅克隆里是空目录——`@dsh-std/*` 源码没读到,8 个 `workspace:*` 依赖的真实内容待验证。
  - `plugin.ts`(4662 行)只读了头 140 行、TTY 门禁、`apply` 入口、挂载段、退出段;`Chat.tsx`(7741 行)未细读。
  - `src/backends/claude|codex`(975 文件 / 29179 行)只看了目录,非 DSH 后端的真实成熟度未验证。
  - 没跑构建或任何 `verify:*`;`lib/` 是产物,未编译。

## 待验证

1. **"换壳"是否真的不需要 web 客户端**:单文件 patch + `insertsSharedWithWebApp: []` 支持这个结论,但 `dsh-tui-webserver` 行说明某些路径仍会起回环 HTTP(OAuth 用)。是否有别的路径复用 web-app 的 server,待读 `host-dsh.ts` 后半与 `src/dsh-adapter/oauth/`。
2. **第三方插件能否免补丁接入**:`dsh-speed` 自述要"patched dsh-TUI",与 `tui-profile` 宣称的准入协议矛盾。需读 `plugin-install.ts`、`plugin-manage.ts`、`admission-loader.ts` 才能判断是"插件 API 不够"还是"该插件用了非公开面"。
3. **下载/星比值异常**:16959/2009 = 8.4,对照 better-sidebar 39717/2216 = 17.9——同为 2026-08-19 采样,它的星更"轻"(围观多、装机少)。两点采样不足以下结论,但值得在下一轮边车刷新时复核。
4. **`fullscreen` 两处默认值必须同步**:patch 的 `fullscreen: true` 与 schema 默认各有一份,注释自称"同步翻转,否则覆盖层会盖住 schema 默认"。此说法来自注释,未实测。
5. **"零核心改动"与"复刻"是否兼容**:`host-contract.ts:90-97` 对 `process-shutdown`、`compose-profile`、`run-profile` 等 8 个宿主符号标了 `local:`(本地复刻实现),`host-replica.snapshot.json` 还钉了 sha256。这算"只消费公开导出"还是"复刻内部行为",需读该文件全文的 `HOST_DEVIATIONS` 才能定论。
