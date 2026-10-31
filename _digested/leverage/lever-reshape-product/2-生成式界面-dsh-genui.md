---
title: "生成式界面 · dsh-genui"
domain: reshape-product
kind: sample
positioning: "`omdsh-dev/dsh-genui`：把回复本身变成可操作界面，用内容协议当扩展面。"
takeaway: "内容协议当扩展面；节点级丢弃 + 块级退回原文；无 action 渲染成 disabled。"
read_when: "要让模型输出可交互组件；或要设计容错的内容协议。"
status: observed
updated: 2026-10-31
---
# 2-生成式界面 · dsh-genui:把回复本身变成产品界面

> **状态**:`observed`(机制已核) · **基线**:DSH `0.2.1-rc.3`(该包自述覆盖 `^0.2.0-rc.1 || ^0.2.1-rc.1 || ^0.2.2-alpha.2`)· **读于**:2026-10-31
> **类**:`2` 内容形态 · **层**: 3 + **4(唯一一例)** · **★ 224 / npm 未采到**
> **一句话**:`1` 类三张卡在改"壳",它改的是**壳里的内容由谁生产**——**模型说的每一句,都可能是一个可以直接操作的组件**。
> **借鉴价值**:**① 用"内容协议"而不是 API 当扩展面(` ```dsh-ui ` + 严格 JSON),换来零 patch、零 `node_modules` 改动;② 两级容错:坏节点单独丢弃、整块不可解析就退回原始 Markdown;③ 校验失败**同轮**把诊断回灌给模型自纠,并给关断阀;④ 无 `action` 的控件渲染成 disabled,用渲染态消灭死点击;⑤ 表面色只暴露一层可覆盖变量;⑥ 重型引擎按节点类型懒加载。**

> **样本档案**
> **repo**:`omdsh-dev/dsh-genui`(目录条目);npm scope 是 `@changfenhuang` · **npm**:`@changfenhuang/dsh-genui` · **版本**:自述覆盖 `^0.2.0-rc.1 || ^0.2.1-rc.1 || ^0.2.2-alpha.2`
> **目录条目**:`data/plugins/omdsh-dev__dsh-genui.yml`(`ui`)
> **装法**:`dsh plugin --profile web add @changfenhuang/dsh-genui`(旧 `@omdsh-dev/` 作用域需先 remove)
> **已在本地挖掘**:本轮挖掘直接读 README 全文(429 行);未单独存盘 —— 关键行号已内联在卡里
> **再深挖去哪**:仓库内 `SKILL.md`(字段级 schema,README 只外链不给)与 `docs/map.md`;还有 11 个场景模板与 `/embed` 三个导出

---

## 0. 一页速览(想抄的人只看这 20 行)

| 问题 | 它的答案 | 支撑 |
|---|---|---|
| 数据从哪来 | **唯一源**:assistant 回复正文里的 ` ```dsh-ui ` fence,块体必须是合法 JSON | `[CAT]` README §架构、§排查 |
| 怎么判定生效 | 语言标识**严格等于** `dsh-ui`(**别名/大小写都不放宽**)+ 块体合法 JSON | `[CAT]` 排查清单第 1 项 |
| 它读不读 session log / 计量 | **不读**。全文无 `tokenUsage` / `contextPressure` / `useProjection`(grep 0 命中) | `[CAT]` 全文 |
| 节点形态 | 顶层 `{title, items[]}`,节点用 `type` 区分:`row` / `stat` / `progress` / `echart` / `table` / `plot` / `quiz` / `map` / `timeline` / `filetree` … | `[CAT]` 示例 |
| `echart.preset` 枚举 | **正好 14 个**:bar, line, area, pie, scatter, radar, gauge, funnel, treemap, sankey, graph, heatmap, bigline, wordCloud | `[CAT]` |
| 但宣传口径写 | "**30+ Component Ecosystem**" —— 与 14 并存,**两个数字口径不一致** | `[CAT]` |
| 一个 fence 多贵 | "**A fence costs only 200–800 tokens**"(区间估计,非测量) | `[CAT]` |
| 有 `action` 才能点 | 无 `action` payload → **渲染为 disabled**,"eliminate dead clicks" | `[CAT]` "Honest UI Guarantee" |
| 事件怎么回传 | 带 `action` 的控件把用户事件**打包回模型**触发下一轮;离散点击**立即发**,连续滑杆用 **trailing-edge debounce** | `[CAT]` |
| 本地能算的 | 排序 / 过滤 / 折叠 / 滑杆重绘 / 切 tab **全 client-side**,不发生模型往返 | `[CAT]` |
| 状态存哪 | 交互态按 **session fingerprint** 存在本地,容量 **LRU 200 blocks**,跨刷新保留 | `[CAT]` |
| 坏节点怎么办 | **丢弃该节点,兄弟照常渲染**("single node errors never crash the fence");Mermaid 语法抖动**自动修复** | `[CAT]` |
| 整块坏了怎么办 | 校验失败 → 诊断**同轮回灌**模型自纠(`fenceFeedback: false` 可关);插件缺席 → **干净退回代码块**,历史不破 | `[CAT]` |
| 重型引擎 | ECharts **~1 MB**、Mermaid、three.js 都"**首现触发**"、走宿主静态路由异步拉 | `[CAT]` |
| 它不做什么 | 零 `eval`、零脚本注入、**禁止采集密码与密钥**;模型 JSON **不得**决定外部资源(地图默认是**离线空白坐标图**,底图样式属于宿主配置) | `[CAT]` 三条红线 |
| 表面色怎么给主题留口 | `--dsl-g-surface → --dsh-genui-surface → --dsw-alias-bg-layer-2 → #fff`,皮肤只钉第二层 | `[CAT]` |
| 对外复用面 | 三个导出:`GenuiBlock` / `GenuiActionContext` / `processGenuiSpec`(`/embed`);前提是宿主 React 支持 CSS Modules | `[CAT]` |
| 导出物 | 单文件 `.html`(内联渲染器 + CSS + 字体 + 图表引擎,**可离线**);`.genui.json`(规范化 spec + durable 交互态) | `[CAT]` |
| 装完要做什么 | **重启 + 硬刷新**;控制台出现 `[genui] client active; fence-channel=dom` 才算激活 | `[CAT]` |
| 最该抄的一句 | "**Malformed nodes are safely discarded while siblings render normally**" | `[CAT]` |

---

## 1. 它在产品里的位置

| 层 | 动作 | 说明 |
|---|---|---|
| 3 槽位 | 会话里的可交互块 + `/panel` 常驻面板 | 不注册新页,寄生在已有容器 |
| **4 身份** | 给模型一套**新的输出词汇** | 本域唯一一例真正改变"模型能说什么"的插件 |

### 1.1 为什么它是"内容形态"而不是"壳"

```
Host --streams Markdown prose & ```dsh-ui fence--> DOM --检测 fence 并按白名单规范化--> GenUI
```

它**没有**新窗口、没有新页面、没有新路由。它只做一件事:**把一种特殊格式的文本,在渲染时换成一个组件**。这条路的代价与收益:

| | 内容协议(它的选择) | 若改成 API(注册渲染器) |
|---|---|---|
| 宿主改动 | **零**(不 patch、不改 `node_modules`) | 需要槽位 |
| 模型侧成本 | 要教会模型一种格式 | 要教会模型调工具 |
| 失败表现 | 退化成代码块(**可读**) | 白屏或空块 |
| 流式支持 | 边到边解析边挂载 | 通常要等完整参数 |

---

## 2. 机制(可照抄的部分)

### 2.1 协议:一个 fence 就是一个界面

````markdown
```dsh-ui
{
  "title": "Q3 Overview",
  "items": [
    {"type":"row","items":[
      {"type":"stat","label":"Total Revenue","value":"¥128,430","delta":"+12.4%","spark":[40,55,60,85,120]},
      {"type":"progress","label":"Quarterly Target","value":82,"variant":"ring"}
    ]},
    {"type":"echart","title":"Monthly Performance","preset":"bar",
     "data":[{"label":"Jan","value":98},{"label":"Feb","value":112}]}
  ]
}
```
````

| 字段 | 约束 |
|---|---|
| 围栏 | ` ```dsh-ui `,**语言标识严格匹配** |
| 块体 | 合法 JSON(**不是 YAML、不是 JS**) |
| 顶层 | `title`(字符串)、`items`(数组) |
| 节点 | 必须有 `type`,按白名单取字段 |
| 图表 | `preset`(14 个枚举)与 `Full Option Mode`(原生 ECharts options)**二选一** |
| 表格列 | `bar`(行内进度条)/ `ring` / `spark` / badge / `filter`(客户端文本过滤) |
| 地图 | 模型只给**坐标或稳定 location ID**,**底图样式永不来自模型 JSON** |

> **为什么必须是严格 JSON**:它要能在**流式**下被增量解析,还要能被**同轮回灌校验错误**。任何"宽松格式"(YAML、模板串)都会让这两件事同时失效。

### 2.2 两级容错 + 一级自愈

| 级别 | 行为 | 原文 |
|---|---|---|
| **节点级** | 坏节点丢弃,兄弟继续 | "Malformed nodes are safely discarded while siblings render normally (single node errors never crash the fence)" |
| **语法级(局部)** | Mermaid 抖动**自动修复** | "Mermaid syntax glitches are automatically repaired." |
| **块级** | 整块不可解析 → **退回原始 Markdown 代码块** | "If the plugin is absent or disabled, fences degrade cleanly to standard Markdown code blocks without breaking the chat history." |
| **不动的** | 流式中的行、不支持或非法 fence **保持原始 Markdown** | "Streaming rows and unsupported or invalid fences keep their original Markdown." |

> 抄这条:**降级链的终点必须是"人还能读的原文"**。把坏数据变成空白块是最差的选择——用户连复制出来自己看都做不到。

### 2.3 同轮纠错:把校验错误当输入喂回去

| 环节 | 做法 |
|---|---|
| 触发 | 生成的 fence 校验失败 |
| 动作 | 把**诊断错误**在同**一轮**内回灌模型,让它自己改 |
| 关断阀 | `config: fenceFeedback: false` |
| 另一开关 | `config: renderUiTool: false` —— 只关 `render_ui` 工具卡片,**fence 与 panel 不受影响** |

> **两个开关只关一半** 是个好设计:它让"我不想让模型看到那个工具卡片"和"我不想要整个功能"分得开。抄的时候别把开关做成"全关"。

### 2.4 诚实 UI:用渲染态消灭死点击

| 情形 | 渲染 | 理由 |
|---|---|---|
| 控件有 `action` payload | 可点 | 有接收者 |
| 控件**无** `action` | **disabled** | "eliminate 'dead clicks'" |
| `carousel` / `image-group` 的导航 | **不调用模型** | 显式把纯浏览交互排除在 action 通道外 |

> **凡是"点了会发生什么取决于模型"的控件,就先在渲染期确认接收者存在**。这比点了再报"暂不支持"好一万倍。

### 2.5 事件投递:离散立即、连续整流

| 手势 | 策略 |
|---|---|
| 离散(点击、选择) | **立即发送** |
| 连续(滑杆) | **trailing-edge debounce**(只在停下时发一次) |

配合"本地优先":排序、过滤、折叠、滑杆重绘、切 tab **全在客户端完成**,不发生模型往返。

> 抄这条判断:**"这个交互需要模型知道吗?"** 不需要的一律本地做。滑杆每格都上行 = 模型轮次被 UI 拖死。

### 2.6 主题:只暴露一层可覆盖变量

```
--dsl-g-surface → --dsh-genui-surface → --dsw-alias-bg-layer-2 → … → #fff
```

| 变量 | 用途 |
|---|---|
| `--dsh-genui-surface` | **皮肤只需钉这一层**,不碰宿主 token |
| `--dsh-genui-surface-flat` | `card.flat`,默认 2.5% 印刷底 |
| `--dsh-genui-surface-table` | `table`,默认透明;指到 surface 则三者同底 |

> **"刻意无表面"的组件要单独开变量**。用一个变量统管所有表面,就再也画不出"卡片有底、表格透明"这种层次。

### 2.7 安全:三条红线,不是沙箱

| 红线 | 原文 |
|---|---|
| 白名单节点 | 只渲染声明过的组件 |
| **零脚本注入 / 零 `eval`** | "zero script injection or `eval`" |
| **禁止收集密码与密钥** | "strict prohibition of passwords or secret collection" |
| 外部资源不归模型 | "external styles belong to trusted host configuration, **never model JSON**" |

**但**:README 全文**没有** CSP / iframe / `sandbox` / origin 白名单 / 速率限制(grep 0 命中)。

> 抄的时候必须知道:**"不执行脚本 + 白名单节点"不等于隔离**。如果节点里允许图片 URL、允许 `data:`、允许外链 CSS,那风险面就还在。要么补隔离,要么像它一样把"不采集密钥"写成产品约束。

---

## 3. 体验

### 3.1 首次使用(60 秒验证)

| 步 | 动作 | 期望 |
|---|---|---|
| 1 | 确认宿主版本在三条 semver 区间内;`pnpm` 在 PATH | — |
| 2 | `dsh plugin --profile web add @changfenhuang/dsh-genui` | — |
| 3 | **重启 + 硬刷新** | 控制台出现 `[genui] client active; fence-channel=dom` |
| 4 | 新会话发:"Use dsh-ui to draw a stats dashboard with a sortable service table." | **原地**出现可交互面板,**不是**代码块 |
| 5 | 点表格列头过滤、拖滑杆、点按钮 | 过滤本地瞬时;按钮把事件打回模型 |

### 3.2 三种进入方式,一套渲染器

| 入口 | 打开方式 |
|---|---|
| 会话内联 | 模型直接输出 fence |
| 常驻面板 | `/panel` 或 `panel: true`,composer 上方 dock,可拖边框改宽;`append: true` 追加标签页 |
| 导出 | `.html`(可离线打开)/ `.genui.json`(保留 spec 与交互态) |

### 3.3 模型看到的

- 一个可选的 `render_ui` 工具卡片(`renderUiTool: false` 可关);
- **失败时是同轮反馈**,不是下一轮重试——模型在同一次生成里被纠正;
- 一个隐含约束:**它必须学会"什么时候该画"**。README 给了 11 个场景模板,本质是在教模型"这类问题值得画"。

### 3.4 这套 UI 的真实用户价值

| 场景 | 不用它 | 用它 |
|---|---|---|
| "帮我看下这个季度的服务稳定性" | 一段 Markdown 表格 | 可排序、可过滤、带 spark 的表 |
| "调一下这个函数的参数" | 改代码、重跑 | 滑杆实时重绘曲线 |
| "考我三道 SQL 题" | 文本问答 | quiz 节点,**单题即时评分 + 解析 + 重试**,多题 `groups` 批量评分与进度 |

---

## 4. 证据与边界

| 口径 | 值 |
|---|---|
| ★ | **224**(快照 2026-08-19);npm 下载未采到 |
| 组件口径 | 宣传 "30+",`echart.preset` 实测 **14**;模板 **11**、badge **12**、内置 UI 字符串 **6** |
| 成本口径 | "a fence costs only **200–800 tokens**"(区间估计) |
| 性能口径 | 滑杆"60 FPS 重绘"、本地交互"sub-millisecond"(**作者断言,无复算方法**) |
| **已知偏差** | ① `30+` 与 `14` 两个口径并存;② README **没有** CSP/iframe/sandbox/origin 白名单/速率限制;③ 字段级 schema 不在 README(外链 `./SKILL.md`);④ 重型引擎加载失败只能靠**硬刷新/重装**运维,没有降级占位;⑤ `echart` 失败即空白,没有"退回表格" |


---

## 5. 借鉴食谱表(本卡的产出物)

| 要解决的问题 | 照它的做法 | 你要改的地方 | 抄错的后果 |
|---|---|---|---|
| 想在别人的产品里加一种新内容形态 | 用**内容协议**(特定 fence + 严格 JSON),不用 API | 你的围栏标记要足够独特(它用 `dsh-ui`),并在文档第一屏写明 | 用通用标记(如 ```json)→ 与别家冲突,误渲染;宽松格式 → 流式解析失败 |
| 需要流式渲染 | 边到边解析边挂载,不等完整块 | — | 等完整 JSON → 长回复卡住几十秒才出图 |
| 模型会写错格式 | 校验错误**同轮回灌**自纠,并给关断阀 | 你的"同一轮"可能是下一请求 | 只报错给人 → 用户要手改模型的 JSON |
| 模型会写错节点 | **节点级丢弃**,兄弟照常 | 按你的 schema 定义"节点边界" | 整块回滚 → 一个坏字段毁掉整个面板 |
| 整块不可解析 | **退回原始 Markdown** | — | 退回空白 → 用户连原文都拿不到 |
| 插件没装/被停用 | fence **干净退化为代码块**,历史不破 | — | 历史里的块变成乱码或报错 → 用户回看旧会话就报 bug |
| 点了会不会有反应 | **渲染期就决定**:没有接收者 → disabled | 你的"接收者"可能是回调/端点/命令 | 允许点击后报错 → 用户点 3 次就不信这个界面了 |
| 连续手势 | **trailing-edge debounce**;离散立即 | 你的拖动可能是滚动/画笔 | 每格上行 → 模型轮次被 UI 拖死 |
| 哪些交互要上行 | 先问"**模型需要知道吗**";不需要的一律本地 | — | 过滤/排序都上行 → 一次点击一个 token |
| 本地状态 | 按**会话指纹**存,`LRU N` 有界 | N 按你的块大小定(它是 200) | 无界 → localStorage 撑爆;无键 → 切会话串味 |
| 重型依赖 | **按节点类型懒加载**,首现才拉 | 你的可能是图表库/地图/Markdown 渲染器 | 全部预加载 → 首屏多几 MB;只懒加载不给失败占位 → 图片位置空白 |
| 主题 | 只暴露**一层**可覆盖变量;对"刻意无表面"的组件**另开变量** | — | 一个变量统管 → 画不出层次;直接改宿主 token → 与宿主皮肤打架 |
| 安全自述 | 把红线写成三条可审计的产品约束(白名单/零 eval/不采集密钥) | 你还要不要补 CSP/iframe? | 只说"安全" → 用户以为是沙箱;允许模型指定外链 → 模型能改你页面的资源来源 |
| 地图/外部资源 | 默认**离线空白底图**,底图样式属于宿主配置 | — | 让模型给 style URL → 模型能给你加载任意瓦片源 |
| 对外复用 | 只暴露 3 个导出名 + 一个 `/embed` 入口 | 你的入口要写清前置条件(它要求宿主 React 支持 CSS Modules) | 暴露内部组件 → 版本一升全碎 |
| 导出产物 | 单文件 `.html`(内联一切,**可离线**)+ 状态 JSON | — | 导出成依赖 CDN 的 HTML → 断网打不开 |
| 装完没生效 | 给一条**可搜的日志标记**(`[genui] client active; fence-channel=dom`) | 你的标记要独特 | 无自证标记 → 排查全靠猜 |

---

## 6. 失效条件与降级

| 触发 | 行为 |
|---|---|
| 插件缺席/停用 | fence 退化为标准 Markdown 代码块,聊天历史不破 |
| 单个节点坏 | 丢弃该节点,兄弟正常 |
| Mermaid 语法错 | **自动修复** |
| fence 校验失败 | 诊断**同轮**回灌模型;`fenceFeedback: false` 关 |
| 流式中的行 / 不支持的 fence | 保持原始 Markdown |
| 语言标识不是 `dsh-ui` 或块体不是 JSON | 不渲染(排查清单第 1 项) |
| 控制台没有激活标记 | bundle 未被宿主激活 → `dsh plugin list` → 重启 → **硬刷新** |
| 重型引擎(3D/Mermaid/ECharts)不渲染 | 静态路由资源没加载 → 硬刷新,仍不行则 remove + add 重装 |
| 渲染 fence 时**整屏白** | 宿主版本太老(缺 React slot/context 能力)→ 升级 DSH |
| 用 `link:` 装刚 clone 的目录 | **不会**打包/解析 peer 资源(mermaid/three/React)→ 仅限本地开发 |
| 只 `npm install` | **不会注册插件** → 必须 `dsh plugin add` |
| 装错包名(漏 scope) | 宿主 peer 依赖闸门**直接拒绝安装** |
| 在 dsh-go 上 | **能力子集**:choices/switches/buttons/submissions/本地评分/tabs/accordions/copy/确认过的 HTTPS 链接;**高级图形与自由文本输入明确不支持** |

---

## 7. 开放问题

- [ ] `[OPEN]` 它靠"DOM 层检测 fence"实现,而上游**没有**给 assistant Markdown 的 fence 替换槽位(`conversation.chat.node` 是按 `ChatNodeKind` **整节点替换**,代码块只有 `[data-code-block-banner]` 这个样式钩子)。**上游该不该给 fence 一个正式接缝**?
- [ ] `[OPEN]` "30+ 组件"与 `echart.preset` 的 14 个并存。**能力宣传的口径要不要在本域立一条"可数"规则**?
- [ ] `[OPEN]` 它没有 iframe/sandbox,安全靠"不执行脚本 + 白名单 + 不采集密钥"。**如果将来节点里出现外部图片/字体,这三条还够吗**?
- [ ] `[OPEN]` 重型引擎加载失败**只能硬刷新/重装**。这是"一次网络抖动 = 需运维动作"。**懒加载的失败占位该不该是硬要求**?
- [ ] `[OPEN]` 它把 `renderUiTool` 与 `fenceFeedback` 做成两个独立开关。**"功能开关要不要按能力而非按入口拆"**?
- [ ] `[OPEN]` 它教模型"什么时候该画"靠 11 个模板 + 一个工具卡片。**有没有更省的教法**(比如系统提示里的一句话规则)?
