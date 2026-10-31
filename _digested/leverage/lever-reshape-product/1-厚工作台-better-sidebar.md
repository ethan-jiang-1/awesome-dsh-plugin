---
title: "厚工作台 · better-sidebar"
domain: reshape-product
kind: sample
positioning: "`omdsh-dev/DSH-better-sidebar`：一个插件把自己做成 IDE，且内置功能也走自己的扩展点。"
takeaway: "一种扩展点形状 + 内置也走它；原型方法注册表；版本前缀 key + 引用完整性。"
read_when: "要做厚工作台/多面板 IDE；或要设计第三方可扩展的注册表。"
status: observed
updated: 2026-10-31
---
# 1-厚工作台 · better-sidebar:一个插件,把自己做成了 IDE

> **状态**:`observed` · **基线**:DSH `0.2.1-rc.3`(本卡主要引用 `0.28.x` 线,要求宿主 `0.2.1-rc.1+`)· **读于**:2026-10-31
> **类**:`1` 壳与工作台 · **层**: 3(槽位)→ 3+5 · **★ 2,216 / npm 39,717**(本域第 2)
> **一句话**:不换表层、不碰官方布局,只在右侧栏"旁边"和"下面"各加一层,然后把文件、编辑器、终端、Git、任务、侧聊全塞进去。
> **借鉴价值**:**① 扩展点只留一种形状 `registerX(descriptor) => disposer`,且内置功能走同一条路;② 自建注册表的方法必须是原型方法,否则插件卸载不回收;③ 持久化的"版本前缀 key + 三道回落 + 引用完整性校验";④ 让第三方能力"装它才有、没装不显示";⑤ 把 40 MB 会话的冷读从 6 次全读压到 1 次 header 读的那套扇出修复。**

> **样本档案**
> **repo**:`omdsh-dev/DSH-better-sidebar` · **npm**:`dsh-better-sidebar` · **版本**:`0.28.2`(本卡引用线)
> **目录条目**:`data/plugins/omdsh-dev__DSH-better-sidebar.yml`(`ui`)
> **装法**:`dsh plugin --profile web add dsh-better-sidebar@latest`;或 `bash scripts/install.sh 0.28.2`;或把三行提示词粘给 DSH 让它自己装
> **已在本地挖掘**:`_证据/1-壳与工作台-原始挖掘.md` §一(better-sidebar 的 8 小节,含 19 条降级清单)
> **再深挖去哪**:README 里那张**宿主→插件版本对照表**(§Pick the plugin version)和 `CHANGELOG`;性能数字全部出自 README §v0.28.2 的修复说明

---

## 0. 一页速览(想抄的人只看这 20 行)

| 问题 | 它的答案 | 支撑 |
|---|---|---|
| 扩展点形状 | 自建 `ctx.betterSidebar`,只有两个方法 `registerTab` / `registerFileViewer`,**都返回反注册函数,都要 `ctx.effect` 包住** | `[CAT]` README §Plugin Ecosystem |
| 为什么可信 | **内置 6 个 tab + 4 个 viewer 走同一条 API**;这套 API 长出 **30+ 生态插件** | 同上 |
| 状态存哪 | **每会话** localStorage(不是全局 blob),key 形如 `dsh.sidebar-right.v1.${sessionId}` | `[DSH]` `dsh-client-ui-sidebar-right/lib/client.js:846-896` |
| 坏了怎么办 | `localStorage` 不存在 → return;读抛 → return;schema 失败 → **主动删 key**;写抛(配额满)→ **只 console** | 同上 |
| 还有什么校验 | 除 schema 外一层 **`validateReferences()`**:id 与 key 一致、序号 ≤ `minted`、split 恰 2 子、`sizes` 和≈1、全节点可达 | 同上 `:821-844` |
| 首屏体积 | **~325 KB core**,重 chunk 按需加载 | `[CAT]` README §Features |
| 最有说服力的数字 | 40.2 MB 会话 + 12 路由 + 36 次 bypass:修复后 **1 header read / 0 full / 3 ms / +0.3 MB RSS**;修复前 **6 次 = 6 次 full read / +1.0 GB**(36 次外推 ≈6 GB) | `[CAT]` README §v0.28.2 |
| 那次没修好的原因 | single-flight 只覆盖 `/sidebar/api`,真实扇出是"**每个被 watch 的目录一帧 fs-watch + 每个 file/html 资源一次 cwd 解析**" | 同上 §v0.28.2 |
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

**关键结构判断**:上游的 `sidebar` / `rightbar` 都是 **single 槽**——注册即**替换**而非叠加(注释原文 "OCCUPIED"、"registering here replaces the navigation column outright")。所以"厚工作台"要装下文件树 + Git + 编辑器 + 终端,只能**绕过 single 槽、自建一层注册表**。这不是品味问题,是槽位粒度倒逼的结果。

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
// [CAT] README §Plugin Ecosystem —— 官方给出的第三方样例形状
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

**自证**:内置 6 tab + 4 viewer **用同一条 API**。这一条是"扩展点可信"的唯一证明——**如果你的内置功能走了后门,第三方永远不知道自己是不是二等公民**。

### 2.2 自建注册表最重要的一个技术细节(几乎人人会踩)

`[DSH]` `dsh-client-ui-renderer/lib/types/client/registry.d.ts:70-84` 的注释:registry 的 `register` **必须是原型方法**。原因是 Cordis 的服务代理在调用时把 `this.ctx` 绑到**调用方** context;如果写成实例箭头属性,effect 会被冻结到**服务自己**的 root ctx,于是"**silently break per-plugin disposal**"(插件卸载时注册项不会被回收)。

> 抄这条:凡是你要 `ctx.reflect.provide('myService', obj)` 出去、让别人 `ctx.myService.registerX(...)`,**`registerX` 必须是 prototype 上的方法**。写成 `registerX = () => ...` 会静默泄漏,而且只在"卸载插件"时暴露。

`ctx.reflect.provide(name, value) => () => void`(`@deepseek-ai/cordis/lib/types/reflect.d.ts:41`);上游实例把两条 disposer 塞进同一个 `ctx.effect`(`dsh-client-ui-sidebar-right/lib/client.js:4965-4971`)。

### 2.3 持久化:三道回落 + 一层引用完整性

`[DSH]` `dsh-client-ui-sidebar-right/lib/client.js:846-896`(本卡最值得整段抄的代码):

| 情形 | 处理 | 为什么 |
|---|---|---|
| `typeof localStorage === 'undefined'` | 直接 `return` | SSR / 受限环境**无痕降级** |
| `getItem` 抛 | `catch { return }` | 存储不可用不是错误 |
| JSON 或 schema 失败 | `clearSidebarLayout(sessionId)` 后 `return` | **主动删坏 key**,下次从默认布局起——否则每次启动都读坏数据 |
| `setItem` 抛(配额满) | `console.error` 后继续 | 布局存不下不该让界面崩 |

**key 设计**:`dsh.sidebar-right.v1.${sessionId}`——**命名空间 + 版本号 + 会话身份**,三者都要。落盘只写 `{ layout, minted }`,**不写** `history`。

**第二层校验 `validateReferences()`**(`:821-844`)——"schema 过了不代表引用自洽":

1. `id` 必须与它在 map 里的 key 一致
2. 序号不得大于 `minted`
3. split 必须**恰好 2 个**子节点
4. `sizes` 之和与 1 的差 **≤ 1e-9**
5. pane 的 `host` 必须与遍历来源一致(来自 dock root / 来自 float)
6. float 必须带 `rect` 且**只有一个 tab**
7. 所有 node / tab **必须被访问到**(无孤儿)

> 第 5–7 条是"恢复半个布局"和"恢复崩溃"的分界。抄的时候别省略——**schema 校验器天然不检查跨引用**。

### 2.4 性能:一次"只修了一半"的修复,比修复本身更有教学价值

| 版本 | 做了什么 | 结果 |
|---|---|---|
| v0.28.1 | 把十二个 `/sidebar/*` 路由的冷 cwd 读取**按 session + client hint 合并** | 仍不够 |
| **为什么不够**(作者自述) | single-flight 只覆盖 `/sidebar/api`;真实启动扇出是"**每个被 watch 的目录一帧 fs-watch + 每个 `/sidebar/file|html` 资源一次 cwd 解析**" | 39 MB 会话仍被**并行全量解码几十次** |
| v0.28.2 | 只读 header 里存的 workspace 地址(**只解第一个 zstd frame,header-only**);**per session memoized + in-flight 请求共享**;`activeWorktreeRootOf` 不再为 detached session 折叠整份日志 | **1 header read / 0 full / 3 ms / +0.3 MB** |

> **抄这条方法论**:① memoize 的键要是**身份**(这里 session),不是调用点;② 合并 in-flight 请求(single-flight);③ **先找扇出点,再优化主路由**——把 N 个入口的最热路径数出来,而不是看哪个函数在 profile 里最靠前。
> 另有一处同样值得抄的"减法":病态 `git status` 输出加 **latch + 进程树 kill**,把"宿主死于 `RangeError`"降级成"一次失败的 SCM refresh"。

### 2.5 让第三方能力"装它才有,没装不显示"

| 原文 | 机制含义 |
|---|---|
| "The entries **appear only** while dsh-context's `Context` page is actually registered: a deployment without it (or with that page hidden) shows **no control at all**" | 探测**能力**,不是探测包名 |
| "while one jump is in flight every entry point is disabled" | 一次在飞,全部禁用(不排队、不重入) |
| "A failed jump is reported **once**, in a dismissible alert at the frame's bottom edge; **nothing is polled while idle**" | 失败只报一次;空闲零轮询 |

> 抄这条:跨插件联动**不要**用"我依赖它"的方式写死;探测它注册了没有,没注册就**整个控件不渲染**。灰按钮是最差的中间态——用户会点,然后以为坏了。

### 2.6 版本:一张表代替一段说明

`[CAT]` README §Pick the plugin version for your DSH version:

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
| ★ / npm | **2,216 / 39,717**(快照 2026-08-19) |
| 生态面 | GitHub topic 下 **30+ 插件**基于其 `ctx.betterSidebar` |
| peer 面 | **13 个 DSH peer floor 全部抬到 `^0.2.1-rc.1`** |
| **已知偏差** | ① 走槽位 → 宿主改布局最坏是"tab 不上",但两处例外会**硬崩**(未注册 panel key、`root` 槽重复注册);② 浏览器侧代码改动**必须硬刷新**——页面保留自己的 module bootstrap,替换必须整页重载;③ 不做 push/pull/fetch,不是完整 IDE |

```sh
python3 _digested/leverage/census.py --probe "sidebar|workbench|workbench.?panel|侧边栏|工作台"
```

---

## 5. 借鉴食谱表(本卡的产出物)

| 要解决的问题 | 照它的做法 | 你要改的地方 | 抄错的后果 |
|---|---|---|---|
| 想给别人留扩展点 | **只有一种形状**:`registerX(descriptor) => disposer`,调用方 `ctx.effect` 包住 | 你的 descriptor 字段换成你的域 | 留两套 API → 第三方不知道该用哪套;不留 disposer → 卸载后幽灵注册项 |
| 扩展点怎么让人信 | **内置功能走同一条 API**,并在 README 里明说 | — | 内置走后门 → 第三方默认自己是二等公民,不贡献 |
| 自建服务要 `provide` 出去 | `registerX` 写成**原型方法**,不要箭头属性 | 检查你的 service 类写法 | 箭头属性 → effect 冻结在服务 root,**插件卸载不回收**,且只在卸载时暴露 |
| 注册表槽位选错 | 先看上游槽是 single 还是 keyed:`single` 是**替换**,装不下多个功能插件 | 你的宿主若有 single 槽,就自建注册表 | 往 single 槽塞第二个 → 第一个被顶掉或整页被遮蔽 |
| 要按会话记状态 | `${ns}.v1.${sessionId}` 这种**三段 key**,不要一个全局 JSON blob | 你的身份可能是 workspace / 项目 | 全局 blob → 切会话后布局乱串;无版本号 → 格式一改全炸 |
| 持久化会坏 | 四道回落:环境不存在→return、读抛→return、**schema 失败→删 key**、写抛→只 console | — | 只 try/catch 不删坏 key → 每次启动都读坏数据,用户以为"设置不保存" |
| schema 通过但状态错乱 | 再加一层**引用完整性**:id 对 key、序号 ≤ minted、split 恰 2 子、比例和≈1、**所有节点可达** | 按你的数据结构改写这 7 条 | 只做 schema → 恢复出半个布局,点一下就崩 |
| 大对象被并发读爆 | memoize **按身份** + 共享 in-flight;**先数扇出点**再优化主路由 | 你的扇出可能在 watcher/静态资源 | 只给主路由加 single-flight → 仍被并行全量解码几十次 |
| 病态输入能杀宿主 | 给外部命令输出加 **latch + 进程树 kill**,降级成"一次失败的刷新" | — | 不设界 → 一次畸形 `git status` 让整个宿主 OOM |
| 资源有界读 | 把上限写成常数并公开;**超限显式报错**;对装饰性数据**省略不失败** | 200/10,000/1,000、5,000 tags/8 MiB | 静默截断 → 用户以为"只有 200 条提交";装饰数据报错 → 图整体画不出来 |
| 跨插件联动 | 探测对方**能力注册了没有**,没有就**整个控件不渲染** | — | 渲染灰按钮 → 用户点,然后以为坏了 |
| 一次操作在飞 | **所有入口一起禁用**;失败只报 **一次**;空闲**零轮询** | — | 每个入口各自 spun → 重复提交;失败弹三次 |
| 改了浏览器侧代码 | README **第一屏**就写"装完/升级后必须硬刷新",并说原因 | — | 等用户报"改了没用" → 你会查一整天 |
| 要给多版本宿主发版 | README 放一张**"宿主版本 → 插件精确版本"表**,并给"无兼容版本怎么办" | 你的矩阵行数按宿主线数定 | 只写"支持 0.2.x" → 老宿主装 latest 直接被拒,用户不知道该怎么办 |
| 想论证"抬版本无风险" | 贴**全树 diff 统计**("355 个文件,全是 package.json,零源码改动") | — | 只说"兼容" → 用户不敢升 |
| 权限边界 | 直接写"**fs 路由不做 workspace 包含检查**",别暗示有沙箱 | 你没有就是没有 | 暗示安全 → 用户以为读了也白读 |
| 外部修改冲突 | 保存时检测外部修改,**拒绝并告知**,绝不静默覆盖 | — | 静默覆盖 → 用户丢一次工作就再也不信这个编辑器 |

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
| 存储不可用/损坏 | 删坏 key,回默认布局;写失败只 console |
| 升级后界面没变 | **没硬刷新**(页面保留 module bootstrap) |
| pnpm 11 拦传递依赖 build script | `pnpm approve-builds`;24 小时 `minimumReleaseAge` → 等或加 exclude |
| `Profile directory not found` | 先跑一次 `dsh web` 初始化 `~/.dsh/profiles/web` |

---

## 7. 开放问题

- [ ] `[OPEN]` 它自建 `ctx.betterSidebar` 而不是用 `ctx.slots`。**上游会不会把"多 tab 工作台"变成一等槽位**,让 30+ 插件不必各自发明? 反过来说,自建注册表是生态活力的来源还是分叉的开始?
- [ ] `[OPEN]` `~325 KB core` 是全文唯一的前端体积数字。**这类"首屏预算"要不要成为本域所有壳插件的必填项?**
- [ ] `[OPEN]` 40 MB 会话的修复故事说明:**上游若能暴露"会话 header 里有 workspace 地址"这一事实**,几十个插件都不必去全量解码。这算上游的接口缺口吗?
- [ ] `[OPEN]` fs 路由自 v0.23.0 起不做 workspace 包含检查。它写明了,但**写明是否足够**?本域对"安全边界自述"要不要有硬要求?
- [ ] `[OPEN]` 它让模型能 `sidebar_open`。**模型还有哪些"人侧界面"的正当控制权**(滚动、聚焦、贴标签)?边界在哪?
