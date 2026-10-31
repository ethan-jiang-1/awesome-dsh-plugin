---
title: "厚工作台 · better-sidebar"
domain: reshape-product
kind: sample
positioning: "`omdsh-dev/DSH-better-sidebar`：一个插件把自己做成 IDE，且内置功能也走自己的扩展点。"
takeaway: "显式 disposer 的扩展注册表；按会话隔离的布局状态；按 session 合并跨路由冷 cwd 读取。"
read_when: "要做厚工作台/多面板 IDE；或要设计第三方可扩展的注册表。"
status: observed
updated: 2026-10-31
---
# 厚工作台 · better-sidebar:一个插件,把自己做成了 IDE

> **状态**:`observed` · **DSH 兼容声明**:`0.2.1-rc.1+`（目标仓库声明；CI mount lane 固定 rc.1；本机安装产物为 rc.3）· **样本版本**:`dsh-better-sidebar@0.28.2`
> **类**:`1` 壳与工作台 · **层**: 3(槽位)→ 3+5 · **★ 4,765 / npm 245,373**（2026-10-31 实时；本线第 3）
> **一句话**:不换表层、不碰官方布局，在右侧栏与底部增加组合工作台，把文件、编辑器、终端、Git、任务与侧聊放进同一个插件。
> **借鉴价值**:**① 扩展注册显式返回 disposer，注销由调用方生命周期持有；② 每会话布局独立存储，结构修复采取局部 sanitize，而非假定全局约束；③ 当多个路由争用冷数据时，按 session 缓存并合并 in-flight 请求，同时把性能数字与测量来源分开。**

> **来源基线**：目标仓库 `v0.28.2` tag 指向 commit [`b0e0fab`](https://github.com/omdsh-dev/DSH-better-sidebar/commit/b0e0fab50e68f54b07a1fc1e7898030409c7d979)（tag 未签名）；源码/测试复核见 [`源码复核`](./_证据/06_厚工作台-better-sidebar-源码复核.md)。未运行目标代码。
> **证据成熟度**：注册和状态机制为 `机制参考`（固定目标源码已追踪、相关测试已读但未运行）；性能数值为作者报告、非本次复现；安全边界由目标源码与测试断言明确（测试未运行），不代表本次行为实测。各项证据不要合并成一个“全卡源码已验证”。
> **repo**:[`omdsh-dev/DSH-better-sidebar`](https://github.com/omdsh-dev/DSH-better-sidebar) · **npm**:`dsh-better-sidebar` · **目标版本**:`0.28.2`
> **目录条目**:`data/plugins/omdsh-dev__DSH-better-sidebar.yml`(`ui`)
> **装法**:`dsh plugin --profile web add dsh-better-sidebar@0.28.2`;或 `bash scripts/install.sh 0.28.2`;或把三行提示词粘给 DSH 让它自己装
> **证据记录**:`_证据/01_壳与工作台-原始挖掘.md` 保留早期 README/DSH 摘录；[`06 源码复核`](./_证据/06_厚工作台-better-sidebar-源码复核.md) 对准目标 tag `v0.28.2` 与 DSH `0.2.1-rc.1`。
> **需继续复核**：目标仓库当前 HEAD 是否已改变此卡所写的 `0.28.2` 行为；本卡不把 HEAD 结论回推到 `0.28.2`。

---

## 它想干什么 · 为什么值得借鉴

**意图。** 它要把右栏从“一个可替换的导航列”扩成一整套 IDE：文件树、编辑器、终端、Git、任务、侧聊都装进右栏与底部自绘工作台，同时给第三方一条与内置完全同形的扩展路径——`registerTab` / `registerFileViewer`，收 descriptor、返 disposer、由 `ctx.effect` 持有。它不换表层、不碰官方布局，也明确不做 push/pull/fetch。

**意义。** 它面对的是 single 槽无法容纳复合工作台的问题：DSH 把 `sidebar` / `rightbar` 声明为 single/root，注册是替换，不是多方并列；目标项目因此另建 `ctx.betterSidebar` 注册面。前半是 `[SRC-DSH]` 槽位契约与 `[SRC-TARGET]` 项目选择之间的对应，因果解释属 `[OBS]`。README 另称内置 tab/viewer 走同一 API，且已有 30+ 插件；本次没有逐个审计这些生态采用数据和内置 descriptor，分别保留为 `[DOC]` 主张。

**用户价值。** 装之前，右栏只能挂一个替代导航栏的页面；装之后，一个包带来六个原生 tab 加底部工作台，窄屏 `<768px` 自动收敛成右栏全宽抽屉。重度用户在一个窗口里看文件、改代码、跑终端、查 Git，“值”发生在不再切窗口的那一刻。代价分两层：用户升级后必须硬刷新；部署者要接受 `fs` 路由自 v0.23.0 起不做 workspace 包含检查——作者把这条写在明处，而不是暗示有沙箱。

**表达（界面与交互）。** README 描述第一屏为右栏 tabs 与底部工作台，三步安装、没有向导，装完/升级后必须硬刷新（页面保留自己的 module bootstrap）。布局数据见 §2.3，和上游另一套 sidebar-right surface state 不混同。README 还描述关 tab、删文件、刷新前确认未保存草稿，外部修改后拒绝静默覆盖；跨插件联动只在 dsh-context 的 Context 页注册时显示，一次跳转在飞时禁用所有入口，失败只报一次。这几项目前为 `[DOC]`，除 layout state 外未逐项源码核验。

## 0. 一页速览(想抄的人只看这 20 行)

| 问题 | 它的答案 | 支撑 |
|---|---|---|
| 扩展点形状 | 自建 `ctx.betterSidebar` 注册 tabs / viewers / file icons；注册返回 disposer，生命周期由调用者持有 | `[DOC]` README Plugin Ecosystem；`[SRC-TARGET]` `service.ts:898-974`；[`源码复核`](./_证据/06_厚工作台-better-sidebar-源码复核.md) |
| 注册表数据与注销 | 三个独立 Map；重复 id 抛错；disposer 仅在当前 descriptor 仍相同才删除并通知订阅者 | `[SRC-TARGET]` `service.ts:898-974`；`[TEST]` `service.spec.ts:26-77` |
| 为什么可信 | README 称内置 6 个 tab + 4 个 viewer 使用同一 API；目标源码 memo 未逐个审计内置 descriptor，不把这点写成已独立验证 | `[DOC]` README；核查范围见[`源码复核`](./_证据/06_厚工作台-better-sidebar-源码复核.md) |
| 布局存哪 | 每会话 localStorage key 为 `dsh-sidebar:v1:<sessionId>`；bottom workbench state 含 `bottomSplits`，不是旧卡所写的 `dsh.sidebar-right.v1` / `{layout,minted}` | `[SRC-TARGET]` `state.ts:644-708` |
| 坏布局如何恢复 | 缺失/读抛/JSON 或 sanitize 失败回默认；坏 key 不自动删除；显式 `?dsh-sidebar-reset` 尝试清理。写入 debounce 200ms，写失败吞掉并保留内存态 | `[SRC-TARGET]` `state.ts:644-708,1195-1216`；`[TEST]` `state.spec.ts:527-620` |
| 状态一致性 | `sanitizeState` / `sanitizeNode` 做结构修复、ID 重铸和 active pane 回落；没有旧卡所述七条 `validateReferences()`，不验证 sizes 总和≈1 | `[SRC-TARGET]` `state.ts:719-779,800-893`；`[TEST]` `state.spec.ts:640-681` |
| 存储作用域与上限 | per activation store；session map LRU 上限 32，淘汰前 flush pending persist；`reduceFor` 可定向更新后台 session 而不发布当前 UI | `[SRC-TARGET]` `state.ts:905-918,965-985,1117-1216,1246-1255`；`[TEST]` 见 memo |
| 首屏体积 | **~325 KB core**,重 chunk 按需加载 | `[DOC]` README Features；未重新构建 |
| 性能结果 | 作者报告 40.2 MB 会话下，v0.28.2 为 1 header read / 0 full / 3ms / +0.3MB RSS；这不是本次运行结果 | `[DOC]` README / CHANGELOG；`[SRC-TARGET]` cwd cache/in-flight 实现在 `index.ts:134-241`；`[TEST]` `smoke.spec.ts:791-855`（已读未运行）|
| 为什么 v0.28.1 不够 | README/CHANGELOG 归因 API-local single-flight 未覆盖 fs-watch、file/html、upload/write 路径；v0.28.2 增加按 session 的 header cache 与 in-flight stat | `[DOC]` README/CHANGELOG；`[SRC-TARGET]` `index.ts:134-241,699-727`；非本次复现 |
| 有界读的常数 | 每页 **200** commits、offset 上限 **10,000**、**1,000** branches;tag 保留 **5,000** 个,再被 **8 MiB** 截断,**省略但不让图失败** | `[CAT]` README §Git Graph |
| 版本策略 | README 里一张 **7 行"宿主版本 → 插件精确版本"表**,含一行"**无兼容版本,先升宿主**";旧版一律 pin exact | `[CAT]` README §Pick the plugin version |
| 不匹配时 | 市场只装 `latest`,老宿主得到 **version-rejection error**(拒绝安装,不是运行时警告) | `[CAT]` + `[DSH]` `dsh-app-boot` 判定 |
| 装完必须做什么 | **硬刷新浏览器**(Cmd/Ctrl+Shift+R),升级后同样 | `[CAT]` README §安装 |
| 窄屏 | `<768px` **没有底部面板**,tab 并入右栏全宽抽屉 | `[CAT]` README §Known Limitations |
| 最该抄的一句 | "**a deployment without it shows no control at all**"——第三方能力不在时**完全不显示控件**,不是灰按钮 | `[CAT]` README §dsh-context diagnostics |

---

## 1. 它在产品里的位置

| 层 | 动作 | 侵入方式 |
|---|---|---|
| 3 槽位 | 右栏**原生** tab(6 个)+ 底部**自绘**工作台 | 槽位层挂载,**不做 DOM 选择器级侵入** |
| 5 默认值 | 每个会话的 tab/面板布局 | 每会话 localStorage |
| 4 身份(边际) | 一个 `sidebar_open` 工具,让**模型自己**打开侧栏 | 模型唯一可见面 |

**关键结构判断**:`v0.28.2` 复核的 DSH `dsh-client-ui-layout` / sidebar 契约将 `sidebar` / `rightbar` 声明为 root single 槽，注册即替换而非叠加；上游调用与类型引用以 DSH `dsh-v0.2.1-rc.1` 为界。样本作者据此自建 `ctx.betterSidebar` registry，以容纳多个 tab/viewer。**产品归因是观察，槽位形态是 DSH 源码事实**；不是说所有宿主 single 槽都只能用自建 registry。

### 1.1 上游槽位的真实形状(写代码前必读)

```js
// [DSH] dsh-client-ui-sidebar/lib/client.js:611-649 —— 一次真实调用
ctx.slots.inject("sidebar", () => ctx.slots.register({
  name: "sidebar", locale: NS,
  children: { "sidebar.brand.mark": { kind: "single", scope: "root" }, ... },
  inject: injectProps,
}, SidebarRoot));
```

可挂钩的壳(全部在 `dsh-client-ui-layout/lib/types/client/index.d.ts`):

| 槽 | 位置 | 语义 |
|---|---|---|
| `sidebar` (`:44`) | 整条左栏 | single / root |
| `main` (`:53`) | 主区 | **keyed**,`conversation` 是保留键 |
| `rightbar` (`:70`) | 右栏 | single / root |
| `shell.bottom` (`:81`) | 全宽底部 | 高度会压缩三栏可用高度 |
| `shell.overlay` (`:95`) | 帧级浮层 | list,**在你 opt-in 指针事件前"点击穿透"** |
| `shell.leading` (`:112`) | 窗口左上角 chrome | **仅当左栏完全隐藏时**挂载 |

> **两个会硬崩的坑**:① 根槽 `root` 的注释直接写 **DO NOT register here**——single 槽里再注册不是并排,而是**遮蔽整个 AppFrame**;② `ctx.layout.selectPanel(<未注册 key>)` 会 **throw** 且保留原选择。

---

## 2. 机制(可照抄的部分)

### 2.1 扩展点:一种形状,内置也走它

```ts
// [DOC] README §Plugin Ecosystem —— 项目作者给出的第三方示例（非实现证据）
import type {} from 'dsh-better-sidebar'   // 触发 ctx.betterSidebar 的类型合并
export const inject = ['betterSidebar']
export function apply(ctx: Context) {
  ctx.effect(() => ctx.betterSidebar.registerTab({
    id: 'my-plugin:db',                    // 命名空间前缀,防碰撞
    title: 'Database',
    component: ({ scope }) => <DbView sessionId={scope.sessionId} />,  // scope 带会话身份
  }))
}
```

四个可照抄的字段:`id`(**带前缀**)、`title`(字符串,**不是 thunk**)、`component`(入参 `{ scope }`)、返回 disposer 并由 `ctx.effect` 持有。

**作者主张**：内置 6 tab + 4 viewer 使用同一 API（`[DOC]` README）。源码复核没有逐个追踪内置 descriptor，因此这里作为可核查主张保留，不写成已独立验证的“唯一证明”。若要把它抽成借鉴规则，应补查内置注册调用与测试。

### 2.2 注册 API 的 disposer 与 Cordis 生命周期

`[SRC-TARGET]` `v0.28.2` 的 `createBetterSidebarService` 用闭包维护 tabs / viewers / fileIcons 三个 Map；注册函数返回 disposer，调用者必须通过 Cordis 生命周期持有它。disposer 检查当前 id 仍指向同一个 descriptor 后才删除并通知订阅者，避免旧 disposer 删除后来替换的注册项。实现见 `service.ts:898-974`；登记/去重/通知有测试覆盖（`tests/service.spec.ts:26-77,741-820`）。

`[SRC-DSH]` 上游 `SlotRegistry.register` 另有 prototype-method 契约：Cordis proxy 以调用方 context 执行方法，从而让 `ctx.effect` disposer 归属插件 fiber（DSH `dsh-v0.2.1-rc.1` `registry.ts:145-164,610-627`）。这是理解 DSH slot/factory registry 的规则，**不是 better-sidebar 自建闭包 registry 的实现证据**；两种 registry 不应混为一谈。

> 可迁移洞察：若 API 让插件注册长期存在的扩展项，返回幂等/有归属的 disposer，并明确由谁持有其生命周期；采用 DSH `SlotRegistry` 时再遵守其 prototype 契约。不要把某一实现要求无条件推广给所有 registry。

### 2.3 会话布局持久化：局部 sanitize 与显式 reset

`[SRC-TARGET]` `v0.28.2` 的自建 sidebar store 按 session 分开 localStorage，布局键为 `dsh-sidebar:v1:<sessionId>`；状态含 `bottomSplits` 树。读取路径在 storage 缺失、读取抛错、JSON 无法解析或 sanitize 失败时回到默认状态；无效 key 不会自动删除。用户可用 `?dsh-sidebar-reset` 显式尝试删除该 session key。写入按 session debounce 200ms；写失败被吞掉，内存状态继续使用。见 `state.ts:644-708,1195-1216`。

`sanitizeState` / `sanitizeNode` 做局部结构修复：夹限 bottom height；异常树回空 leaf；重复 pane/split ID 重新铸造并重映射 active pane；split 至少需要两个 child 且 sizes 数量与 child 数匹配、值为有限正数；未知 tab type 保留，便于插件之后载入恢复；diff 状态在恢复时移除。**不**存在旧稿所述 `validateReferences()` 七点全树可达检查、`minted` 序号界限或 sizes 总和≈1 约束。见 `state.ts:719-779,800-893`；相关 sanitize/migration/unknown extension 情形由 `state.spec.ts:527-620,640-681,716-845` 覆盖（本次只读测试，未运行）。

状态归属不只一个 localStorage key：store 按插件激活实例创建，内存 session map 是 32 项 LRU；淘汰前 flush pending persistence，`reduceFor` 能对后台 session 定向修改且不通知当前 UI。见 `state.ts:905-918,965-985,1117-1216,1246-1255`。

> 可迁移洞察：恢复布局时先界定每个会话的状态边界，再对结构损坏做可解释的局部修复；只有在实际 schema 有跨引用不变量时，才增加对应完整性检查。不要把“坏值回默认”说成“坏记录已删除”，也不要借用别的 registry 实现中的校验规则。

### 2.4 性能：一次“只修了一半”的修复，比修复本身更有教学价值

`[DOC]` v0.28.2 README/CHANGELOG 报告本机 40.2 MB fixture 的测量；下表数字是作者报告，不是本次运行或独立复现。目标源码确认 v0.28.2 的实现增加 session-keyed header cache / in-flight stat（`src/index.ts:134-241`），相关并发与 fallback 由 `tests/smoke.spec.ts:791-855` 覆盖；测试本次未运行。


| 版本 | 做了什么 | 结果 |
|---|---|---|
| v0.28.1 | 把十二个 `/sidebar/*` 路由的冷 cwd 读取**按 session + client hint 合并** | 仍不够 |
| **为什么不够**(作者自述) | single-flight 只覆盖 `/sidebar/api`;真实启动扇出是"**每个被 watch 的目录一帧 fs-watch + 每个 `/sidebar/file|html` 资源一次 cwd 解析**" | 39 MB 会话仍被**并行全量解码几十次** |
| v0.28.2 | 只读 header 里存的 workspace 地址(**只解第一个 zstd frame,header-only**);**per session memoized + in-flight 请求共享**;`activeWorktreeRootOf` 不再为 detached session 折叠整份日志 | **1 header read / 0 full / 3 ms / +0.3 MB** |

> **抄这条方法论**:① memoize 的键要是**身份**(这里 session),不是调用点;② 合并 in-flight 请求(single-flight);③ **先找扇出点,再优化主路由**——把 N 个入口的最热路径数出来,而不是看哪个函数在 profile 里最靠前。
> 另有一处同样值得抄的"减法":病态 `git status` 输出加 **latch + 进程树 kill**,把"宿主死于 `RangeError`"降级成"一次失败的 SCM refresh"。

### 2.5 让第三方能力“装它才有，没装不显示”

| README 主张 `[DOC]` | 可迁移解释 `[OBS]` |
|---|---|
| dsh-context 的 `Context` 页注册后才出现入口；没装或隐藏则不显示控件。 | 探测**能力是否已注册**，不要只检查包是否安装。 |
| 一次跳转在飞时所有入口禁用；失败只报一次，空闲不轮询。 | 若多个入口共享同一操作，统一在途状态与失败通道可减少重复提交和噪声。 |

> 此处是文档级产品行为描述；目标源码复核未追踪该联动组件的实现。抽入通用规则前需补对应源码/测试证据。

### 2.6 版本:一张表代替一段说明

`[DOC]` README §Pick the plugin version for your DSH version（版本映射是作者文档声明，不等同于逐版本 CI 实测）：

| 宿主 DSH | 插件版本 |
|---|---|
| `0.2.1-rc.1+` | `0.28.2` |
| `0.2.1-alpha.5` | `0.28.0-alpha.0` |
| `0.2.0-rc.2` | `0.26.1` |
| `0.2.0-rc.1` | `0.24.1` |
| `0.1.7-rc.1 ~ 0.1.7 stable` | `0.22.1` |
| `0.1.7-alpha.x` | **无兼容版本,先升宿主** |
| `0.1.6 及更早` | `0.19.1` |

配套规则:旧版**一律 pin exact**,因为 `latest` 会往前走。不匹配时市场**不看宿主版本**就装 `latest`,于是老宿主收到 **version-rejection**(`[DSH]` 拒绝码 `incompatible-version`,可 `dsh plugin allow-version <pkg@ver> --dsh-version <runtime> --accept-risk` 豁免)。

**一份硬证据**:`0.2.1-alpha.5 → rc.1` 的全树 diff **355 个文件,全是 `package.json`,零源码改动**——这句话是"抬 peer floor 无风险"的最佳论证模板。

---

## 3. 体验

### 3.1 首次使用(三步,没有向导)

| 步 | 做什么 | 用户看到 |
|---|---|---|
| 1 | `dsh plugin --profile web add dsh-better-sidebar@latest`(或 `bash scripts/install.sh 0.28.2`,或把三行提示词粘给 DSH 让它自己装) | — |
| 2 | **硬刷新浏览器** | 右栏 6 个原生 tab;底部出现自绘工作台 |
| 3 | 窄屏时 | 底部面板消失,tab 并入右栏全宽抽屉 |

### 3.2 边界被写在明处(而不是等用户撞)

| 边界 | 原文要点 |
|---|---|
| 文件系统权限 | **自 v0.23.0 起 fs 路由不做 workspace 包含检查**——宿主用户能碰的路径都能读写(只剩 OS 权限) |
| HTML 预览 | 跑在 **opaque-origin sandbox iframe**;可按 feature 关掉 sandbox(默认关,带警告) |
| Git 能力 | **不做 push/pull/fetch**;文件树只 watch **展开**的目录;Markdown 预览渲染**已保存**的文件 |
| 只读格式 | xlsx/PDF/图片/Office 交给 **DSH 自己的文档预览**,行为随宿主版本走 |
| 草稿 | 关 tab / 删文件 / 刷新前**确认未保存草稿**;外部修改后再保存是**拒绝**,绝不静默覆盖 |
| 终端 | 不自带 PTY;无 terminal controller 时显示"host provides no terminal capability" |
| 重复挂载 | 以别的 id 聚合挂载本包时**自动让位**;页面出现两个 sidebar 时删掉 `cordis.patch.yml` 里的老式手动挂载行 |

### 3.3 模型看到的

一个 `sidebar_open` 工具——**模型可以自己把侧栏打开**。这是"模型动作 → 人侧界面"的正向联动里最克制的一个:**只开关,不替用户决定看什么**。

---

## 4. 证据与边界

| 口径 | 值 |
|---|---|
| ★ / npm | **4,765 / 245,373**（2026-10-31 实时） |
| 生态面 | GitHub topic 下 **30+ 插件**基于其 `ctx.betterSidebar` |
| peer 面 | **13 个 DSH peer floor 全部抬到 `^0.2.1-rc.1`** |
| **已知偏差** | ① 走槽位 → 宿主改布局最坏是"tab 不上",但两处例外会**硬崩**(未注册 panel key、`root` 槽重复注册);② 浏览器侧代码改动**必须硬刷新**——页面保留自己的 module bootstrap,替换必须整页重载;③ 不做 push/pull/fetch,不是完整 IDE |


---

## 5. 可迁移洞察（本卡产出）

每行都是一条带前提的设计决策；来源等级不能混读。完整来源与精确引用见[`06 源码复核`](./_证据/06_厚工作台-better-sidebar-源码复核.md)。

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 插件/模块要注册可扩展 UI | 当扩展项需要跨组件存活时，返回显式 disposer，并让**调用方生命周期**持有它。 | `[SRC-TARGET]` 三个 Map + identity-checked disposer：`service.ts:898-974`；`[TEST]` duplicate/dispose/subscription：`tests/service.spec.ts:26-77`。 | 生命周期归属明确，可注销且避免旧 disposer 删除新 descriptor；代价是调用方必须正确绑定 effect/fiber。 | 换成自己的 descriptor、owner scope、重名策略、替换语义与 disposer 幂等规则。 | 本仓服务用闭包注册表；DSH `SlotRegistry` 的 prototype-method 规则是**另一种实现**，不能误套。 | 忘传 disposer 会遗留入口；沿用错误的原型结论可能修错层或漏掉真正 owner。 |
| 某会话工作区布局需持久化 | 当状态只属于一个 session 时，用 session id 隔离存储，并明确恢复/淘汰策略，不写跨会话共享 blob。 | `[SRC-TARGET]` `dsh-sidebar:v1:<sessionId>`、`bottomSplits`、32-session LRU/evict flush：`state.ts:644-708,905-918,1117-1216`；`[TEST]` migration/LRU。 | 切会话不串状态，LRU 限制内存并先 flush；代价是 32 项上限与跨会话后台读写逻辑。 | 若身份实际是 workspace/user/device，改 key 与 owner；定义多设备同步和淘汰后的可恢复性。 | 该 key 只覆盖 sidebar state，不代表产品所有偏好都 per-session。 | 身份粒度选错会串数据或丢状态；忽略 flush 会在 LRU 淘汰时丢待写变更。 |
| 持久化布局可能损坏或来自旧版本 | 当布局 schema 可兼容修复时，对字段/树做局部 sanitize 并有默认回退；只有在产品确实需要取证/清理时才删除坏记录。 | `[SRC-TARGET]` sanitizer/recovery：`state.ts:719-779,800-893`；`[TEST]` malformed tree / unknown type / migration：`state.spec.ts:527-620,640-681`。该版本坏 key不自动删除，reset query 才尝试清理。 | 局部修复可保留可识别 tabs/状态；但静默回默认可能隐藏损坏原因，key 保留也可能反复触发 sanitize。 | 定义可恢复字段、不可恢复阈值、诊断可见性、何时迁移/隔离/删除；依据自家 schema 写不变量。 | v0.28.2 **没有**旧卡所述 `validateReferences()` 七项、`minted` 与总和校验。 | 抄不存在的校验会产生虚假安全感；把“回默认”写成“删坏数据”会让运维步骤无效。 |
| 多路由并发读取同一会话的冷元数据 | 当多个入口争用同一 session 的慢 I/O，先量扇出，再按 session 共享缓存与 in-flight 请求；不要只在一个路由局部 single-flight。 | `[SRC-TARGET]` `storedCwdCache` / `storedCwdInFlight` 与 `sessionPersistence.stat()`：`index.ts:134-241,699-727`；`[TEST]` 12 concurrent requests share one stat：`smoke.spec.ts:791-855`。 | 跨入口消掉重复解析；代价是缓存失效、并发、fallback 优先级与 stale client hint 都需定义。 | 按数据权威源选 cache key/TTL/invalidation；实现时定义当前值、header、用户 hint 的优先级。 | 40.2 MB / 3ms 等数字是作者报告，本次未运行；不得直接外推到其他文件大小和机器。 | 只优化主 API 会漏掉 watcher/资源路径的扇出；无效缓存会选错 workspace 或掩盖真实状态。 |
| 文件功能容易被误当成 workspace sandbox | 当插件以宿主用户权限读写文件，必须明确威胁边界；cwd/path normalization 不等于授权围栏。 | `[SRC-TARGET]` lexical `resolveTarget` 无 containment/realpath：`path-security.ts:1-76`；`[TEST]` workspace 外路径与外部 symlink 可 list/read/write：`smoke.spec.ts:1063-1116,1534-1584`。 | 清晰告知用户真实 OS 权限边界，避免虚假隔离承诺；代价是访问面宽，需要信任安装包/宿主授权策略。 | 若需 sandbox，加入真实路径 containment、symlink policy、拒绝码和测试；别只检查 `cwd`。 | 这是明确的产品安全边界，不是可照搬的安全设计；HTML sandbox/CSP 不改变文件系统授权。 | 宣称 workspace 受限会使用户在错误安全假设下开放敏感文件。 |
| 兼容范围需要帮助用户选版本 | 若同一插件需服务多条宿主线，给宿主版本到插件版本的明确映射，并写出无兼容版本时的下一步。 | `[DOC]` v0.28.2 README compatibility table；`[SRC-DSH]` install gate；详见卡§2.6与来源 memo。 | 用户可选精确版本，降低 `latest` 被拒的惊讶；代价是矩阵必须随 release 更新，README 声称仍需 CI/测试佐证。 | 映射按自己的宿主分支维护；区分“声明兼容”和“CI 实测”；给无匹配路径。 | 当前矩阵是文档指导，不能仅凭它证明每一行都运行通过。 | 过期矩阵会推荐不可装版本；把推荐配对写成已测试矩阵会误导兼容承诺。 |

---

## 6. 失效条件与降级

| 触发 | 行为 |
|---|---|
| 宿主缺 dsh-context 的 Context 页 | 相关联动控件**完全不显示** |
| 宿主没有 terminal controller | 显示"host provides no terminal capability" |
| 本包被聚合包以别的 id 挂载 | **自动让位**,无需动作 |
| 页面出现两个 sidebar | 删 `~/.dsh/profiles/web/cordis.patch.yml` 里的老式手动挂载行 |
| 宿主版本不在表里(`0.1.7-alpha.x`) | **没有兼容版本**,先升宿主 |
| 老宿主装 latest | 安装期 **version-rejection**,不下载、不跑 build script |
| `<768px` | 无底部面板,tab 并入右栏抽屉 |
| 插件布局存储不可用/损坏 | v0.28.2 读错/sanitize 失败回默认但不自动删 key；`?dsh-sidebar-reset` 显式尝试删除；写失败吞掉并继续内存态（见 §2.3） |
| 升级后界面没变 | **没硬刷新**(页面保留 module bootstrap) |
| pnpm 11 拦传递依赖 build script | `pnpm approve-builds`;24 小时 `minimumReleaseAge` → 等或加 exclude |
| `Profile directory not found` | 先跑一次 `dsh web` 初始化 `~/.dsh/profiles/web` |

---

## 7. 开放问题

- [ ] `[OPEN]` 它自建 `ctx.betterSidebar` 而不是用 `ctx.slots`。**上游会不会把"多 tab 工作台"变成一等槽位**,让 30+ 插件不必各自发明? 反过来说,自建注册表是生态活力的来源还是分叉的开始?
- [ ] `[OPEN]` `~325 KB core` 是全文唯一的前端体积数字。**这类"首屏预算"要不要成为本线所有壳插件的必填项?**
- [ ] `[OPEN]` 40 MB 会话的修复故事说明:**上游若能暴露"会话 header 里有 workspace 地址"这一事实**,几十个插件都不必去全量解码。这算上游的接口缺口吗?
- [ ] `[OPEN]` fs 路由自 v0.23.0 起不做 workspace 包含检查。它写明了,但**写明是否足够**?本线对"安全边界自述"要不要有硬要求?
- [ ] `[OPEN]` 它让模型能 `sidebar_open`。**模型还有哪些"人侧界面"的正当控制权**(滚动、聚焦、贴标签)?边界在哪?
