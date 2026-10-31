---
title: "薄基座 · dock"
domain: reshape-product
kind: sample
positioning: "`AKS1st/dock`：只给注册表、不给能力的工作台基座，六个 API + 六个兄弟包。"
takeaway: "服务面 + 零内部依赖 + 可选 peer；隐藏要留一条与被隐藏物无关的逃生口。"
read_when: "要做平台型外壳/注册表；或要接别人的布局又不想改它。"
status: observed
updated: 2026-10-31
---
# 薄基座 · dock:把「槽位」做成一个薄基座

> **状态**:`observed`(机制)/ `[OPEN]`(0.2.x 实测) · **基线**:DSH `0.2.1-rc.3` · **读于**:2026-10-31
> **类**:`1` 壳与工作台 · **层**: 3 → 6(平台化) · **★ 10 / npm 月下载 1,673**（2026-10-31）
> **一句话**:它只做一件事——**提供工作台外壳,不提供任何具体能力**。六个注册 API、六个兄弟包,契约放在仓库里。
> **借鉴价值**:**① "基座零内部依赖 + 一个服务面 + 安装顺序不敏感"是平台化的最小配方;② UI 依赖写成可选 peer,缺失时"不激活"而不是崩;③ 要碰别人的布局,先定义可测量的量,且只改位置不改尺寸;④ 私有 DOM 锚点消失时只能"不生效";⑤ 任何隐藏都要留一条与被隐藏对象无关的逃生入口。**

> **证据深度**:源码级（上游接缝 + 仓库 README；0.2.x 装上未实测）（2026-10-31）
> **影响力**：机制例外——唯一的"零依赖注册表基座"样本（门槛见 [`00-map` §7](../00-map.md)）。

> **样本档案**
> **repo**:[`AKS1st/dock`](https://github.com/AKS1st/dock) · **npm**:`dock-base`(基座);兄弟包 `dock-files` / `dock-editor` / `dock-images` / `dock-markdown` / `dock-git` / `dock-spreadsheet` · **版本**:未取版本号
> **目录条目**:`data/plugins/AKS1st__dock.yml`(`ui`),兄弟包各有 `AKS1st__dock-*.yml`
> **装法**:`dsh plugin --profile web add dock-base`,再逐条装兄弟包
> **已在本地挖掘**:`_证据/01_壳与工作台-原始挖掘.md` §二(dock 的 8 小节,含 9 条降级清单)
> **再深挖去哪**:README §设置 API 给了 `registerSetting` 的完整字段;契约文件在仓库 `src/client/contract.ts`(功能插件内各有 vendored 副本)

---

## 0. 一页速览(想抄的人只看这 20 行)

| 问题 | 它的答案 | 支撑 |
|---|---|---|
| 它提供什么 | 一个**空工作台外壳**:左活动栏、侧边栏、编辑器区、底部状态栏 | `[CAT]` README §功能 |
| 它不提供什么 | 文件树 / 编辑器 / 图片 / Markdown / Git **全是兄弟包** | 同上 |
| 扩展点 | `ctx.workbench` 六个注册方法 `registerActivityBarItem` / `registerPanel` / `registerEditorView` / `registerStatusBarItem` / `registerCommand` / `registerSetting`,**全返 disposer、全配 `ctx.effect`** | `[CAT]` README §功能 |
| 安装顺序 | **不敏感**(Cordis 按依赖激活) | `[CAT]` README §插件契约 |
| UI 依赖 | `react` / `react-dom` 写成 **peer(可选)**:"未提供时**工作台 UI 不激活**" | `[CAT]` README §依赖 |
| 设置项 | `id` 用 `<pluginId>:<name>`,**另有 `pluginId` 决定归属**——身份与归属分离 | `[CAT]` README §设置 API |
| 文案多语言 | `title` **同时接受 string 与 `(locale) => string`**,切换语言不必重注册 | 同上 |
| 值怎么校验 | `validate: (value): value is boolean`——**TS 类型谓词**,校验发生在**写入前** | 同上 |
| 状态存哪 | 布局与设置都在 **localStorage**,设置是**一个全局 key** `dock:settings`(无 sessionId) | `[CAT]` README §设置 API |
| 坏了怎么办 | "存储不可用或数据损坏时,**使用内存值和默认值继续运行**"(不删 key、不报错) | 同上 |
| 怎么碰别人的布局 | 定位 `data-turn-navigator`,右停靠时把它左移 **实测 dock 宽度 + 24px**,且"**不改变页面宽度或滚动条位置**";关掉开关偏移**归零** | `[CAT]` README §通用设置 |
| 那个锚点还在吗 | **`data-turn-navigator` 在 0.2.1-rc.3 整个安装目录 0 命中**——软锚点,消失只是"偏移不生效" | `[DSH]` 全树 grep |
| 上游正规解 | `shell.leading` 挂载期间 frame 发布 CSS 变量 `--dsh-frame-leading-clearance`,内容按它 padding | `[DSH]` `dsh-client-ui-layout/lib/types/client/index.d.ts:112-124` |
| 逃生入口 | 入口隐藏后**仍可从设置打开**;**隐藏后仍可右键 dock 栏**打开设置 | `[CAT]` README |
| 最该抄的一句 | "只装 `dock` 本身也完全没问题——它就是一个干净的工作台外壳" | `[CAT]` README §推荐搭配 |

---

## 1. 它在产品里的位置

```
dock(基座)                    ← 平台层:只有外壳 + 注册服务,零内部依赖
├── dock-files    文件树
├── dock-editor   编辑器
├── dock-images   图片
├── dock-markdown Markdown
└── dock-git      Git
```

| 层 | 动作 |
|---|---|
| 3 槽位 | **不往宿主槽位注册多个功能**,而是自建 `ctx.workbench` 一层 |
| 6 平台化 | 一个插件变成**一个系列**,基座负责"形状",兄弟包负责"内容" |

**为什么自建而不用 `ctx.slots`**:上游 `sidebar` / `rightbar` 都是 **single 槽**(注释 "OCCUPIED"、注册即"replaces the navigation column outright")——一个要同时挂文件树 + Git + 编辑器的"复合面板/编辑器视图"结构,**single 槽装不下,list/keyed 槽又表达不了**。所以基座层是自己发明的,但它与上游 `AppFrame` 的拓扑同构(活动栏≈`sidebar`、编辑器区≈`main` keyed、状态栏/面板≈`shell.bottom` / `shell.overlay`、命令≈`ctx.shortcuts`)。

---

## 2. 机制(可照抄的部分)

### 2.1 注册面:一个方法一个语义

| 方法 | 语义 | 抄的时候注意 |
|---|---|---|
| `registerActivityBarItem` | 左侧图标项 | 需要 icon 回落 |
| `registerPanel` | 侧边栏面板 | 与编辑器视图是**两种**容器 |
| `registerEditorView` | 编辑器区视图 | 需要 `EditorOpenSeed`(怎么打开) |
| `registerStatusBarItem` | 底部状态条 | 极窄空间,别塞可点元素 |
| `registerCommand` | 命令面板条目 | 与快捷键绑定分离 |
| `registerSetting` | 设置项 | 见下 |
| `registerPlugin({id,title,description,icon,hasEntry})` | 让设置窗口**列出插件** | 没有 icon 用通用图标 |

`registerSetting` 的完整形状(唯一给了全套字段的):

```ts
ctx.effect(() => ctx.workbench.registerSetting({
  id: 'my-plugin:compact',                     // 命名空间 id
  pluginId: 'my-plugin',                       // 归属:设置页按它分组
  title: (locale) => locale === 'zh' ? '紧凑模式' : 'Compact mode',  // 字符串 or 工厂
  defaultValue: false,
  component: CompactToggle,                    // 只接收 { 当前值, onChange, 语言 },不持有状态
  validate: (value): value is boolean => typeof value === 'boolean',  // 写入前校验
}))
```

读侧三个:`getSetting` / `setSetting` / `onDidChangeSetting`。排序:`order`,再 `id`。

> **两处细节值得单独抄**:① **身份与归属分离**(`id` 管唯一性,`pluginId` 管"归到哪个插件的设置页")——否则一个插件想提供"属于别人的设置项"就没法表达;② **`validate` 是写入前的一道闸**,不是"存了再纠正";后者会让坏值先落盘。

### 2.2 契约怎么发给别人(没有 workspace 依赖时的土办法)

`src/client/contract.ts` 是工作台对外契约(`WorkbenchService`、`ViewProps`、`EditorOpenSeed` 等)。功能插件**只做类型导入**(编译期擦除),运行时全部走 `ctx.workbench`。而每个功能插件里有**一份 vendored 副本**,"改动本文件时需同步更新"。

代价被作者写明:改契约要**手动同步 5 份**。

> **抄这条判断**:跨包共享类型,在"没有 monorepo 依赖"的前提下只有三条路——① 发一个 `-types` 包;② vendor 副本 + 注明同步;③ 用 `import type` 从主包拿(需要依赖)。它选了 ②,因为 ② 不引入运行期与版本耦合。**选哪条不重要,重要的是把"要手动同步"写进 README**。

### 2.3 状态:一个命名空间 key,坏了就"内存值继续"

| 决定 | 它的做法 | 对比 better-sidebar |
|---|---|---|
| 作用域 | **全局**(`dock:settings` 无 sessionId) | 每会话 `…v1.${sessionId}` |
| 损坏 | **不删 key、不报错**,用内存值 + 默认值继续 | 删坏 key 回默认 |
| 写入前 | `validate` 谓词校验 | schema + 引用完整性双验 |

> **两种做法都对,取决于"坏数据的来源"**:如果坏数据来自"版本升级导致格式变了",删掉是对的(旧格式没救);如果来自"用户手改/迁移出错",**保留是慈悲**——用户下次修好还能用。dock 选保守是对的,因为它的设置项少、格式稳定。

### 2.4 侵入别人:先定义可测量的量

| 规则 | 它的做法 |
|---|---|
| 定位 | `data-turn-navigator`(宿主会话进度导航栏) |
| 动作 | 右停靠时把它**左移"实测 dock 宽度 + 24px"** |
| 不做 | **不改变页面宽度或滚动条位置** |
| 重算时机 | dock 栏尺寸变化 / 窗口缩放 / 开关切换 |
| 可逆 | **关闭开关时偏移归零** |

**而上游的正规解是"约定一个量"**:`shell.leading` 挂载期间,frame 发布 CSS 自定义属性 `--dsh-frame-leading-clearance`,主面板内容贴左上角时按它 padding。

> `+24px` 是它的手工近似版。抄的时候优先找**上游有没有已经约定好的量**;没有就自己定义一个**能被对方读取**的量(自定义属性/DOM 事件),而不是"我算你的宽度然后改你位置"。

### 2.5 软锚点的纪律

`data-turn-navigator` 在 `0.2.1-rc.3` 整个安装目录里 **0 命中**(全树 `grep -rn turn-navigator` 无输出;现有的是 `data-conversation-scroll` / `data-conversation-region` / `data-conversation-header-*` / `data-composer-*`)。

它没有崩,因为:**找不到元素 → 什么都不做**。这就是"敢用私有 DOM 标记"的代价与对策。

> 抄这条:**用私有锚点前先写好"找不到时怎么办"**。允许"不生效",禁止"抛错"或"改错节点"。

---

## 3. 体验

### 3.1 首次使用:装基座 → 加零件

| 步 | 做什么 | 看到 |
|---|---|---|
| 1 | `dsh plugin --profile web add dock-base`,再逐条装 `dock-files` / `dock-editor` / `dock-images` / `dock-markdown` / `dock-git` | — |
| 2 | 打开 | **一个空工作台外壳**:左活动栏、侧边栏、编辑器区、底部状态栏,只有 dock 图标与设置入口 |
| 3 | 点 dock 栏末尾的 **dock 图标** | 设置窗口 |
| 4 | 在"通用设置"里调位置 / 自动隐藏 / 预留空间 / 放大倍数;在"插件 → 入口 → Dock"管理显隐 | — |

### 3.2 交互细节:几何量即预算

| 项 | 值 |
|---|---|
| 悬浮放大 | 悬停 **1.6×**、相邻 **1.2×**(默认) |
| 倍数范围 | 悬停 **1.0–2.5×** / 相邻 **1.0–2.0×**,步进 **0.05** |
| 不变式 | **相邻倍数不超过悬停倍数** |
| 预留空间 | **实测 dock 宽度 + 24px** |
| 关掉自动隐藏 | 即使正在隐藏也**立刻强制展开**(幂等强制态,不是"下次生效") |

> 这个插件**没有任何体积/耗时/RSS 数字**——它把"性能"表达成**重算边界**(哪三种情况要重算)而不是毫秒数。这也是一种诚实的写法:**说清什么时候算,比给一个测不准的数字更有用**。

### 3.3 逃生:永不把自己锁死

- 入口隐藏后**仍可从设置里打开**。
- 隐藏后**仍可右键 dock 栏**打开设置。

> 这是"可隐藏 UI"的硬要求:**任何隐藏都要留一条与被隐藏对象无关的通道**。dock 留了两条。

---

## 4. 证据与边界

| 口径 | 值 |
|---|---|
| 目录指标 | **★ 10 / npm 1,673**（GitHub API / npm，2026-10-31） |
| 宿主最低版本 | `>=0.1.3-alpha.2` |
| peer | `cordis ^4.0.0-rc.7`;`react` / `react-dom ^18.2.0` **可选** |
| **已知偏差** | ① **无版本对照表**,只有一条最低版本,也没写不匹配会怎样;② 依赖 `data-turn-navigator` 私有锚点,0.2.x 已 0 命中 → 该偏移功能在 0.2.x 上**实际不生效**;③ 契约靠 5 份手工同步副本,不同步 = 类型漂移(编译期可见,运行时无感) |


---

## 5. 借鉴食谱表(本卡的产出物)

| 要解决的问题 | 照它的做法 | 你要改的地方 | 抄错的后果 |
|---|---|---|---|
| 想让一个插件变成"一个系列" | 基座**零内部依赖** + 一个服务面 + 兄弟包只依赖服务 | 你的服务面要有"增删改查"里的"增"和"读"两类 | 基座依赖兄弟包 → 装一个就拖一串;反向依赖 → 基座升级牵动全部 |
| 想让安装顺序无关 | 用**依赖注入声明**(`inject: ['workbench']`),不要 `import` 具体实现 | — | 手动 `import` → 顺序错了就白屏 |
| UI 依赖可能不存在 | React 写成**可选 peer**,缺失时"**UI 不激活**" | 你的可选依赖可能是图表库/编辑器 | 写成硬依赖 → 无 React 环境下加载即炸;写成 `require` 后 try/catch → 半初始化状态 |
| 插件设置要归组 | `id` 管唯一、**另一个字段管归属**(`pluginId`) | — | 只有 id → 一个插件没法替别人贡献设置项 |
| 文案要多语言 | `title` 接受 **string 或 `(locale) => string`** | — | 存字符串 → 切语言要重注册/重载页面 |
| 设置值要防手改 | 写入前 `validate` 谓词,**用 TS 类型谓词**让编译期与运行期同一份判断 | — | 存了再纠正 → 坏值先落盘,别处已读到 |
| 存储坏了要不要删 | 先问"坏数据是格式演进还是人为损坏":格式演进**删**,人为损坏**留**(内存值继续) | — | 一律删 → 用户手改一次配置就丢全部;一律留 → 格式升级后永远读不出 |
| 要碰别人的布局 | **先找一个已经被约定好的量**;没有就定义一个**对方能读**的量(CSS 变量/事件),**只改位置不改尺寸** | 你的宿主可能有 `--dsh-frame-*` 之类 | 直接改宽高 → 挤压对话区;改别人的 transform → 与动画打架 |
| 必须用私有 DOM 锚点 | 先写"**找不到就什么都不做**",并接受它某天会消失 | — | 找不到就抛错/回退到 `document.body` → 改错节点,页面错位 |
| 可隐藏的 UI | 隐藏后留**两条**通道(设置里能找到、右键能打开) | — | 只留一条 → 那条正好坏了 = 用户永久失去功能 |
| 开关语义 | "关掉自动隐藏"要**立即**强制展开(幂等强制态) | — | 写成"下次生效" → 用户以为开关坏了 |
| 几何交互 | 把倍数/步进/上下界**全部写死成常数**,并规定不变式(相邻 ≤ 悬停) | — | 只给默认值不给范围 → 用户调出难看且不可复现的形态 |
| 跨包共享类型(无 monorepo) | vendor 契约副本 + **README 写明"要手动同步 N 份"** | 份数写出来 | 不说 → 别人改契约后到处类型漂移 |
| 性能怎么表述 | 说清**"什么时候重算"**,而不是给测不准的毫秒数 | — | 编一个"50ms" → 一旦不达标就没人信你其他数字 |
| 平台化第一步 | 先只做基座并保证"**只装基座也完全没问题**" | — | 基座自带半成品功能 → 用户不知道该装哪一个 |

---

## 6. 失效条件与降级

| 触发 | 行为 |
|---|---|
| 没有 React | **工作台 UI 不激活**(不崩) |
| 存储不可用 / 数据损坏 | 内存值 + 默认值继续,**不删数据** |
| 插件没给 icon | 用 dock 自带通用图标 |
| 入口被隐藏 | 设置里仍可打开;**右键 dock 栏**仍可打开设置 |
| 关闭"预留空间" | 偏移**归零**,无残留 |
| 关闭自动隐藏 | **立即**强制展开 |
| 私有锚点 `data-turn-navigator` 不存在(0.2.x 现状) | **偏移不生效**,其余功能正常 |
| 契约副本没同步 | 编译期类型漂移;运行时走 `ctx.workbench` 不受影响 |
| 只装基座不装功能包 | 完全正常:一个空工作台外壳 |

---

## 7. 开放问题

- [ ] `[OPEN]` 它的 `data-turn-navigator` 在 0.2.1-rc.3 已不存在,说明**这个基座还没在 0.2.x 上真正跑通过那条偏移逻辑**。它是否已升级到用 `--dsh-frame-leading-clearance`?
- [ ] `[OPEN]` 基座 + 5 个兄弟包的模式,和 better-sidebar 的"一个厚包"模式,哪个在生态里更有生命力?证据:better-sidebar 30+ 插件基于其 API,而 dock 系列只有自家 5 个。
- [ ] `[OPEN]` 它把设置作用域定成**全局**,better-sidebar 定成**每会话**。**"哪些偏好该跟会话走"有没有一条判断规则**?(比如:改变"看到什么"的跟会话,改变"怎么用"的跟全局?)
- [ ] `[OPEN]` 契约靠 5 份手抄副本同步。**有没有一种"零依赖但不易漂移"的类型共享方式**(比如生成 `.d.ts` 并校验哈希)?
- [ ] `[OPEN]` 它自建的工作台外壳与上游 `AppFrame` 拓扑同构。**这是巧合还是必然**?如果上游把 `AppFrame` 的可组合性补齐,自建层会消失吗?
