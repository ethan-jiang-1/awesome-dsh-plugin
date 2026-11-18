# DSH-better-sidebar — 官方右列里的插件注册表:第三方注册 Tab,它翻译成 DSH 原生 Tab

> 证据等级:★★★(源码级;`repo@commit 2811573c9c0bad51d77db6c3c94d78f5aed8d38a`,2026-11-13)。
> 数据截止 `29b3ed46e`(2026-11-17)。⚠ 星标/下载为 2026-08-19 历史采样。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `omdsh-dev/DSH-better-sidebar`([registry](../../../data/plugins/omdsh-dev__DSH-better-sidebar.yml)) |
| 类目 | ui(全表最大类) |
| 自述 | 侧边栏完整工作台:文件渲染编辑、终端、Git、子代理;三方插件可注册新 Tab(`data/plugins/omdsh-dev__DSH-better-sidebar.yml`) |
| 星标 ⚠ | 2216(2026-08-19,`data/stars.json`;边车口径见 [`_method/00-index.md`](../../_method/00-index.md)) |
| npm 月下载 ⚠ | 39717(2026-08-19,`data/downloads.json`) |
| 扩散 | **63 个第三方条目**在 name/description 里点名它(`delta.py` ③b 口径;本次复现:65 命中 − 2 条锚自身) |
| 仓库 commit | `2811573c9c0bad51d77db6c3c94d78f5aed8d38a`(2026-11-13,"Merge PR #1188 chore/code-slimming") |
| 包形态 | npm `dsh-better-sidebar@0.32.1`(MIT,`publishConfig.access: public`);宿主半 ESM `lib/index.js`,客户端半 **CJS 双产物** `lib/client.js`(官方 profile 通道)+ `lib/client-registry.js`(注册表通道)+ 4 个 lazy chunk;无 postinstall |
| 代码规模 | `src/` 250 个 `.ts/.tsx` / **81,551 行**;`tests/` 328 文件 / 87,823 行;全仓 764 文件、119 篇 markdown |

## 它到底是什么

不是"一个更好的侧栏",而是**建在官方 Web 壳里的一层插件注册表 + 一层宿主适配**。三处源码决定了这个判断:

1. **右列不归它**。自 v0.19.0 起右列由 DSH 自己的右侧栏渲染,插件自己的 shell 只剩底部工作台——`src/client/Sidebar.tsx:1-20` 的原话是 "DSH 0.1.5 owns the right column: its native Sidebar hosts every tab type this plugin registers"。插件把自己的每个 Tab 变成 DSH 的**原生 tab 类型**(`src/client/native/index.ts:470-497`),不是自绘面板。
2. **它对外发的是一张注册表**。`apply()` 开头就 `ctx.provide('betterSidebar', service)`(`src/client/index.tsx:176`),服务接口是 `registerTab / registerFileViewer / registerFileIcon / registerFileAction / registerTabAction`(`src/client/service.ts:764-800`),每个都返回 disposer。
3. **内置功能走同一张表**。`registerBuiltins()` 把 6 个内置 tab、5 个 viewer 注册进同一个 service,注释自称 "eating its own dogfood"(`src/client/builtins/index.ts:1-31`)。外部插件与内置功能是同一等公民,不是插进来的补丁。

所以它的"工作台"其实是三件事叠在一起:**注册表**(API)+ **适配层**(翻译成宿主原生类型)+ **一组用该 API 写的内置功能**(文件树/编辑器/改动/Git/任务/侧聊)。

## 怎么接进 DSH

### manifest 与两套分发通道

- `dsh.plugin.json`(整份 16 行):`id: dsh-external/dsh-better-sidebar`、`main: ./lib/index.js`、`client.main: ./lib/client-registry.js`、`engines.dsh: >=0.2.2-rc.2`、`contributes.tools/skills` 均为空数组。
- `package.json:41-56` 的 `dsh` 字段才是运行期契约:`bundle.patch: ./cordis.patch.yml`、`client.inject` 声明 5 个客户端模块(locale / ui-slots / ui-conversation / ui-sidebar-right / modules)、`client.platform: web`、`manifestVersion: 1`。
- `tsdown.config.ts:345-352` 把**同一份** `src/client/index.tsx` 编两遍:官方 profile 通道用包名 bundle id `dsh-better-sidebar` → `lib/client.js`;第三方注册表通道用 manifest id `dsh-external/dsh-better-sidebar` → `lib/client-registry.js`。注释明说 "DSH never reads that file"(DSH 不读 `dsh.plugin.json`)。

### `cordis.patch.yml` 的语义

整份 patch 只有一条 `insert`,id `better-sidebar`、name `dsh-better-sidebar`;文件头注释说明 `dsh plugin add` 会把包追进 `dsh.profile.bundles`,boot 时合并这条 insert 完成挂载,不必手改 profile。

真正有信息量的是第 42 行的守卫:

```yaml
disabled: !!js "[...ctx.loader.entries()].some((e) => e.options.name === 'dsh-better-sidebar' && e.options.id !== 'better-sidebar' && !e.disabled)"
```

它解决的是**聚合包重复挂载**:聚合包(如 `@linxin666/dsh-web-ui-all`)可能用自己的 entry id 挂同一个包,两个挂载各注册一次 `/sidebar/api` → loader 报 "duplicate prefix route" → 整棵插件树启动失败。守卫让本行在"前面已有另一个启用中的同名 entry"时退让。注释同时承认限制:loader 只看得见**排在它前面**的行,所以聚合包必须排在前面;反序无解,也没有运行时单例守卫(`cordis.patch.yml:26-38`)。

### 插件接口(宿主半,`src/index.ts`)

| 符号 | 值/位置 |
|---|---|
| `name` | `'dsh-better-sidebar'`(:100) |
| `inject` | `['webServer','sessions','connection','tools']`(:116) |
| `apply(ctx, config)` | :1438 |
| `Config` | `src/config.ts:168`,= 部署限额 + 全部 volatile 的用户偏好 |
| 路由 | 8 条 HTTP:`/sidebar/api`、`/sidebar/file`、`/sidebar/html`、`/sidebar/bundle`、`/sidebar/write`、`/sidebar/upload`、`/sidebar/archive`、`/sidebar/sidechat-image`;3 条 WS:`/sidebar/ws/agent-opens`、`/sidebar/ws/fs-watch`、`/sidebar/ws/sidechat` |
| 工具 | `ctx.tools.register(defineTool({ name: 'sidebar_open', … }))`(`src/agent-opens.ts:209-218`) |

注意一处**声明与行为的错位**:manifest 的 `contributes.tools` 是空数组,但运行期会在 `agentOpenTools` 偏好打开时注册 `sidebar_open`(`src/index.ts:1526` 的 `syncOpenToolsGate`,默认关)。市场页读到的能力清单与真实能力不一致。

设置面按**Loader 行 entry id** 寻址:`ownEntryId(ctx)` 用包名 + fiber 身份自发现(聚合包会用别的 id 挂同一包),再 `settings.configure({ auto: false }, ctx.fiber)` 让位给插件自绘的设置页(`src/index.ts:1455-1480`)。客户端不直接读 settings,而是走自己的 `settings.get / settings.update` 两条路由(带 revision 冲突 → 409)。

### 插件接口(客户端半,`src/client/index.tsx`)

- `inject = ['slots','sessions','locale','modules','connection','remote','remote.session']`(:54)。注释记录:少写 `remote.session` 会在渲染路径抛 `cannot get property "remote.session" without inject`,整块面板变白。
- `ctx.provide('betterSidebar', service)`(:176)。
- slot 注册:`settings.section.icon`(:480)、`settings.section`(:492)、`conversation.session.header.utilities`(`src/client/sidebar/bottom-toggle.tsx:23`)、`sidebar.right.tab.guide`(接管开始页)、`sidebar.right.pane.tab` / `sidebar.right.pane.tab.title`(每个 tab 一个,`src/client/native/index.ts:422` 起)。
- 原生类型注册:`tabs.register({ id, kind: descriptor.id, keepMounted: true, priority: 'extension', guide: [...] })`(`src/client/native/index.ts:470-497`)。

### 第三方接入的最小路径(源码可验证)

1. 客户端插件 `inject: ['betterSidebar']`(Cordis 保证服务就绪后才激活);
2. `ctx.betterSidebar.registerTab({ id: 'x:y', title, component, … })`;
3. 把返回的 disposer 交给 `ctx.effect`,HMR/禁用时自动注销。

第三方**完全不需要**碰 `sidebarRightTabs`、slot key、`keepMounted`、guide 条目——这些全在 `native/index.ts` 里被翻译掉。这就是它作为平台的核心价值:接一个 Tab 的成本 = 写一个 React 组件。

## 关键实现

### 文件结构(按职责)

- 传输:`wire.ts`(JSON 包/错误码)、`file-stream.ts`(Range 流)、`bundle-route.ts`、`html-route.ts`、`open-external.ts`
- 文件系统:`fs-tree.ts`、`fs-operations.ts`、`fs-search.ts`、`fs-batch.ts`、`fs-watch.ts`、`path-security.ts`、`text-encoding.ts`、`editor-limits.ts`
- Git:`git.ts`(1198 行)、`git-graph.ts`、`commit-message.ts`
- 会话:`session-path.ts`、`active-worktree.ts`、`changes-ops.ts`、`subagent-live-route.ts`、`team-routes.ts`、`workflow-routes.ts`、`sidechat-core.ts`(1728 行)+ `sidechat-routes.ts`(1137 行)
- 客户端:`state.ts`(1268 行)、`service.ts`(1759 行)、`native/*`(适配层)、`builtins/*`、`chunks/*`、19 份词典

### 核心模块逐个

**`wire.ts` + dispatch(`src/index.ts:1608` 的 `buildApi`)** — `POST /sidebar/api/<method>` 一个窄入口,44 个顶层方法(fs.* 9、git.* 23、archive/changes/settings/session/teams/workflows/subagents/open 共 12)+ `sidechat.*` 9 个。入口先过 `fence = ctx.connection.requestRejection(req) === undefined`(:1442)。派发用 `Object.hasOwn(api, method)` 而非裸查找——注释记录了一个真实漏洞:`POST /sidebar/api/constructor` 曾回 200 `{}`,`toString` 回 `"[object Undefined]"`。

**`path-security.ts`** — `resolveTarget(cwd, target)` 是唯一解析原语:相对路径挂到会话 cwd、绝对路径保留、`~` 展开、`..` 词法折叠。模块头明确写着 **"This module no longer enforces workspace containment"**(:1-16):原有 `realpath` + 越界拒绝被用户要求移除,现在能到达"宿主用户能到达的任何路径",只受 OS 权限和路由层的浏览器信任围栏约束。

**`fs-operations.ts`** — 同样的声明("No workspace containment any more",:1-16),保留的是**形状**校验:上传相对路径拒绝绝对路径/`.`/`..`/空段;rename/mkdir 必须是单段名;新文件名额外检查 Windows 非法字符与保留设备名;目标已存在则拒绝而非覆盖;workspace 根不可改名/删除;上传先写唯一临时兄弟再 `rename` 就位,失败不留半文件;符号链接按词法行路径处理(改的是链接不是目标)。

**`service.ts`** — Map + listener 集合,`useSyncExternalStore` 友好;重复 id **直接 throw**(`:1116-1122`),disposer 幂等且按对象身份校验。`SIDEBAR_SERVICE_VERSION = '0.32.1'`(:1014,`tests/service.spec.ts` 钉住与 package.json 同步);`SIDEBAR_FEATURES` 16 项能力位(:1050-1075),注释承诺 "features are never removed",并自己记录了 v0.19.0 移除 `floatWindows` 这个反例。

**`native/index.ts`(适配层,291 行起)** — 一个描述符 → 一个原生类型 + 两个 slot,全部成组注册、成组回滚(部分成功也要能退)。`editor` 用 `priority: 'extension'` 认领 `dsh-resource://file/**`,压过宿主 `text` 预览;但 `HOST_OWNED_EXTS`(`:72-84`)主动**拒收** xlsx/pdf/图片/Office,交回宿主的文档预览;`files` 这个内置 page kind 被同名接管。`keepMounted: true` 让宿主的"隐藏"不再销毁插件侧 React 状态。

**`state.ts`** — 每会话一份:分栏树(leaf / split 递归)+ 打开页签 + 展开集,持久化在 `localStorage` 的 `dsh-sidebar:v1:<sessionId>`;`SidebarTab.meta` 是插件私有可序列化状态;`line` 故意排除在持久化白名单外(一次性导航目标,刷新不该把读者拉回几天前的那一行)。

**`agent-opens.ts`** — 模型面工具 `sidebar_open` + 每会话队列 + `/sidebar/ws/agent-opens` 推送;返回值带 `delivered`,告诉模型"现在可见"还是"排队等该会话侧栏上屏"。工具执行前会先查 `prefs.tabsEnabled`,目标类型被用户关了就直接报错而不是静默成功。

**`sidechat-*`** — 侧聊不是 UI 彩蛋:它经 `sidechat.start/prompt/cancel/dispose/info/events/dequeue/models/model` 九个方法创建**子会话**、按 `seq` 增量取事件、单独做图片准入(metadata 字节阈值后才放开大 body)。

**`bundle-route.ts` + `chunk-loader.ts`** — `CHUNK_NAMES = ['editor','mermaid','locale','terminal']`(`bundle-route.ts:25`);CodeMirror/mermaid/xterm 首次用到才拉,页面启动不背这几个重库。

### 数据流

```text
React tab(第三方或内置)
  → src/client/api.ts        POST /sidebar/api/<method>  { sessionId, cwd? }
  → src/index.ts  fence()    → buildApi()[method]
  → fs-* / git / sidechat / changes 模块（宿主进程身份执行）
  → JSON 回包（错误统一 SidebarError → { code, message }）

宿主主动推（三条 WS 分工明确）:
  /sidebar/ws/fs-watch      客户端上报已展开目录 → 仅失效该层缓存并重列
  /sidebar/ws/agent-opens   sidebar_open 队列 → 客户端开对应 tab
  /sidebar/ws/sidechat      只推"哪条线程脏了"，正文仍走 sidechat.events 增量

客户端状态:
  state.ts(每会话) ←→ localStorage[dsh-sidebar:v1:<sid>]
  service.ts 注册表 → native/index.ts 翻译 → 宿主 sidebarRightTabs
```

编辑器保存路径是个例外:不走 JSON API,走 `/sidebar/write?sessionId&path&expectedMtimeMs`,文档即 body(避免 JSON 转义与 1 MiB 信封上限),并带 mtime 乐观并发。

## 为什么它突出

**63 是"提及"数,不是"接入"数**——必须说清楚,否则会高估。2026-11-18 抽样浅克隆 3 个提及者,三种强度都出现了:

| 样本 | 强度 | 证据 |
|---|---|---|
| `Lzh3070/dsh-file-review-tab` | 硬依赖 | `package.json` 写 `peerDependencies: {"dsh-better-sidebar": ">=0.19.1"}`;`src/client/index.tsx:267` 调 `ctx.betterSidebar.registerTab(...)`,`FileReviewTab.tsx:571` 调 `openFile` |
| `fuhefei/dsh-sentinel` | 软依赖 | 不 value-import,`src/client/index.tsx:55` 本地重述最小契约,`inject: ['betterSidebar']` 拿不到就静默跳过——正是 `docs/external-plugin-guide.md` §15 记录的做法 |
| `Max-Null/dsh-chat-rail` | 只提不用 | 只有 README/设计文档里说按 `--dsh-sidebar-height` 变量避让,仓内 grep 不到任何 `registerTab`/`betterSidebar` 调用 |

也就是说 63 是**上限**,"平台"这个判断不该只靠它。真正的机制性证据是下面四条:

1. **它把宿主内部 API 藏起来了**。想给 DSH 原生右列加一个 tab,原本要 inject `sidebarRightTabs`、懂 `keepMounted`/`priority`/guide 条目、自己注册两个 slot;现在只要 `registerTab` 一个 React 组件。平台的定义就是"把复杂度吃进自己肚子里"。
2. **接口有版本承诺**。`SIDEBAR_SERVICE_VERSION` + 16 项单调 `SIDEBAR_FEATURES`,消费方按能力位 gate;`package.json:15-35` 专门导出 `./client/service`、`./client/api` 两个子路径给消费方 import 类型。这不是随手开的口子。
3. **它替生态写了接入文档**。`docs/external-plugin-guide.md` 单文件 155 KB:§4.1 `TabDescriptor` 完整字段、§4.4 内置 tab 清单、§5.4 viewer 匹配算法、§7 服务方法清单、§15 真实接入案例。平台型插件的标志之一是它承担了上游文档的职责。
4. **它愿意为宿主让路**。`HOST_OWNED_EXTS` 主动放弃宿主已经做得更好的格式,自绘右侧面板与自由窗口整体删除,插件自带终端/浏览器类型也删了。一个只想抢地盘的插件不会这么干。

需要强调的是:这四条**不是**"它功能多"。功能多只解释星标;解释扩散的是"别人能往它身上加东西,而且加得便宜、加得稳定、加完不会被它下一次重构打碎"。

## 代价与边界

**权限与安全**

- **无权限清单**。`dsh.plugin.json` 只有 id/version/main/description/engines/contributes/client,没有 permissions 字段;准入完全交给宿主:`fence` 调 `ctx.connection.requestRejection(req)`,裁决 Host/Origin 与浏览器认证(`docs/host-contracts.md` 首段)。
- **它不经过 DSH 的沙箱策略链**。`src/` 内 grep 不到 `dsh-sandbox` / `sandbox-policy` / `user-approval` 的 import,也没有 `ctx.get('sandbox')`。文件写入、`git commit/push`、`open.external`(spawn 平台 opener)、归档(`zip`/`tar`)全部以宿主进程身份直接执行。沙箱约束的是模型工具调用,不是这个插件的 HTTP 路由——能过 fence 的请求就能读写宿主用户可读写的一切。
- 剩下的边界都在**内容侧**:HTML 预览的 CSP `sandbox`(`src/index.ts:1880-1890`)、媒体路由的 nosniff/no-referrer、`htmlViewerNoSandbox` 这个用户可开的逃生阀、explorer 排除 glob。没有一条限制路径。
- 8 HTTP + 3 WS 的准入都要自己守。`Object.hasOwn` 那条注释说明这类手写 dispatch 已经踩过一次原型链坑,靠测试兜住。

**外部依赖**

- 系统二进制:git(含 WSL 转发 `wsl.exe -d … -e git`,`git.ts:469-474`)、`zip`/`tar`(归档)、平台 opener。缺一个就退化成错误条,不崩。
- 运行库:15 个 `@codemirror/lang-*` + `@codemirror/view/state`、xterm、mermaid、dompurify、ws、yaml、rxjs。重库进 lazy chunk,`lib/` 因此是 6 个客户端产物 + ESM 宿主产物。
- **DSH 版本耦合**:14 条 `@deepseek-ai/*` peer 钉在 `^0.2.2-rc.2`,`engines.dsh >= 0.2.2-rc.2`。每个宿主 RC 都要跟:`docs/plans/` 里有 0.1.5 / 0.1.6 / 0.1.7 / 0.2.0 / 0.2.1 / 0.2.2 的逐版适配记录,`docs/host-contracts.md`(36 KB)把这些约束固化成"第 N 条"。这不是可选维护,是订阅了宿主的发布节奏。

**失败模式**

- **双挂载即整树失败**:`/sidebar/api` 注册两次 → "duplicate prefix route"。守卫靠 `!!js` 表达式 + bundle 顺序,反序无解(见上)。
- **设置写入静默失效**:必须用 DSH 自己的 `@deepseek-ai/schemastery`;用公开包写 volatile 字段会"报告成功、revision 也涨、有效值永远不变"(`src/config.ts:1-13`)。
- **服务缺失即降级**:`settings` 不在组合 → 表单面缺席、客户端退回 schema 默认;`webTerminals` 不在 → 底部终端置灰;`llm` 不在 → 提交信息建议 503;`sidebarRightTabs` 不在 → 什么原生类型都注册不上。
- **卸载顺序**:`noServer` 的 `WebSocketServer.close()` 不终止已升级的 socket,必须逐个 `client.close()`,否则每个 fs-watch 的 `fs.watch` 句柄活到浏览器断开(`src/index.ts` teardown 注释)。

**维护成本**

- 81.5k 行源码 + 87.8k 行测试;300 个 spec + 15 个 e2e(含真宿主 + Chromium 挂载冒烟);CI 双平台(ubuntu + windows,Windows 用 `--maxWorkers=1` 全量跑)。
- `CHANGELOG.md` 271 KB / `CHANGELOG_EN.md` 185 KB,按版本逐条写"改了什么 + 补了哪些测试"。
- 发布链严格:tag 必须等于 package.json version,`typecheck → lint → test → build → check:consumer-types → npm publish`(`.github/workflows/release.yml`)。

**被三方依赖后的兼容负担**

- `SIDEBAR_FEATURES` 承诺只增不减,但确实删过 `floatWindows`;gate 过它的消费者会静默降级。承诺 + 例外是平台税的固定项。
- 第三方把 peer 写成 `>=0.19.1` 这种宽区间,意味着 0.19→0.32 之间的签名变化全由平台方吸收;`TabDescriptor` 已经长到 19 个字段(`service.ts:184-310`),每加一个字段就多一处兼容面。
- **双层承载的语义裂缝**:宿主原生面按 `(kind, 地址)` 去重,插件的 `dedupeKey` 不参与;用户点原生 tab 的 × 不触发 `onClose`。这些只能靠一张长表解释"哪些行为只在底部工作台成立"(`docs/external-plugin-guide.md` §0)。

## 可信度与复现

**证据等级 ★★★**:manifest、入口(`src/index.ts`)、服务(`src/client/service.ts`)、适配层(`src/client/native/index.ts`)、patch、构建配置、`docs/host-contracts.md` / `external-plugin-guide.md` 的关键段都读了原文。星标/下载只读边车,一律标 ⚠。

```sh
git clone --depth 1 https://github.com/omdsh-dev/DSH-better-sidebar.git /tmp/an-sidebar
git -C /tmp/an-sidebar rev-parse HEAD        # 2811573c9c0bad51d77db6c3c94d78f5aed8d38a
git -C /tmp/an-sidebar log -1 --date=iso     # 2026-11-13 16:25:50 +0800

# 规模
find /tmp/an-sidebar/src -name '*.ts*' | wc -l                  # 250
find /tmp/an-sidebar/src -name '*.ts*' -exec cat {} + | wc -l   # 81551
find /tmp/an-sidebar/tests -type f | wc -l                      # 328

# 机制锚点
grep -n "provide('betterSidebar'" /tmp/an-sidebar/src/client/index.tsx   # 176
grep -n "export const inject" /tmp/an-sidebar/src/*.ts /tmp/an-sidebar/src/client/index.tsx
grep -n "priority: 'extension'" /tmp/an-sidebar/src/client/native/index.ts  # 495 / 555
```

复现扩散数 63(口径同 `_digested/ecosystem/delta.py` 的 `imitation_signals`;注意 census 把 YAML 键拍平成 `description.en` / `description.zh`,直接读嵌套字典会得到 0):

```python
import importlib.util, glob
from pathlib import Path
spec = importlib.util.spec_from_file_location("census", "_digested/ecosystem/census.py")
census = importlib.util.module_from_spec(spec); spec.loader.exec_module(census)
tok = "better-sidebar"; hits = self_ = 0
for p in glob.glob("data/plugins/*.yml"):
    d = census.parse_yml(Path(p)) or {}
    text = " ".join([str(d.get("name", "")), str(d.get("description.en") or ""),
                     str(d.get("description.zh") or "")]).lower()
    if tok in text:
        hits += 1
        self_ += tok in str(d.get("url", "")).lower().split("github.com/")[-1]
print(hits, self_, hits - self_)     # 65 2 63
```

**未跑**:`pnpm install` / `pnpm build` / `pnpm test` / `pnpm test:mount` / `pnpm test:mount:aggregate` 全部没执行(要装 14 条 DSH peer 与真宿主)。因此"包形态"来自 `tsdown.config.ts` 与 `package.json#files` 的**声明**,不是实测 tarball;patch 的 `!!js` 守卫行为来自注释与自测脚本,不是跑出来的。

**未读**:`src/client/SideChatView.tsx`(2443 行)、`FileTree.tsx`(2646)、`GitLens.tsx`(1390)、`TextEditor.tsx`(1264)、`EditorHost.tsx`(1071)、`tasks-*` / `TeamBoard.tsx`、19 份词典、`tests/` 全部、`scripts/e2e-*.sh`、`build-mermaid-frame-asset.mjs`、119 篇 markdown 中的绝大多数(只读了 `external-plugin-guide.md` §0/§1/§15、`host-contracts.md` §A 头部、`detail/DETAIL.md`)。

## 待验证

1. **63 里到底多少真接 API**。本次只抽样 3 个(硬/软/仅提及各一),不足以给比例。要确认:按 63 条 URL 逐个浅克隆,`grep -rn "betterSidebar\|registerTab"`,并统计 `package.json` 里 `dsh-better-sidebar` 是否进 peerDependencies。
2. **npm tarball 实际内容**。`files` 声明含 `src`、`detail`、`locale`、`cordis.patch.yml`(即发布包含完整源码),但没跑 `npm pack`。要确认:`npm view dsh-better-sidebar dist.tarball` 后解包比对,并看 `detail/*.svg` 是否真的随包(插件页图文详情依赖它)。
3. **聚合包双挂载守卫在真实 loader 上的行为**。`!!js` 表达式依赖 `ctx.loader.entries()` 的可见性与顺序,仓内只有 `scripts/e2e-aggregate-mount.sh` 自证(未跑)。要确认:该脚本 + 一个真实聚合 profile 的 `dsh.profile.bundles` 顺序。
4. **与宿主 `ui-sidebar-*` 类型的仲裁规则**。`editor` 用 `priority: 'extension'` 认领 `dsh-resource://file/**`,文档说卸载即复位;多插件同时认领同一 glob 时谁赢,不在本仓代码里。要确认:读 `@deepseek-ai/dsh-client-ui-sidebar-right` 的注册表实现(本机 DSH checkout 里有源码)。
5. **8 条路由是否都过了 fence**。本次只逐条看了 5 条;`/sidebar/bundle` 走的是 `registerBundleRoute(ctx, fence)`,内部是否每条分支都调用需要复核。要确认:`src/bundle-route.ts` 全文 + 各 handler 的 `if (!fence(req))`。
6. **`contributes.tools: []` 与运行期工具的错位是否有实际后果**。要确认:DSH 插件页 / 注册表是否用 `contributes` 渲染"提供哪些工具";若是,则该插件在市场页永远显示"无工具",而模型实际能用 `sidebar_open`。
7. **同作者 44 条是否构成套件**。`omdsh-dev` 在本仓名单里有 44 条(ui/notify/browser/tools/security),本次只分析了 1 条。要确认:它们是否共享同一套 service/协议、是否互为依赖。
