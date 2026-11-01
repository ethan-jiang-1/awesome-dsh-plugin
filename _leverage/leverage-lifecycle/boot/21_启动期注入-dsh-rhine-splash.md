---
title: "启动期注入 · rhine-splash：在页面生成的那一刻动手"
domain: lifecycle
kind: sample
positioning: "唯一用 webserver/index-inject 的样本：注入顺序、转义与“开屏频率”三件必须自己想清的事。"
takeaway: "index-inject 能改到 React 之前的首屏，但顺序（append 不 prepend）和转义（JSON/CSS）都得自己负责。"
read_when: "要做品牌首屏、主题注入或开屏动画；或排查“页面闪一下才变主题”。"
status: observed
updated: 2026-11-01
budget: 130
---
# 启动期注入 · rhine-splash

> **阶段**：起 · **载体**：index-inject（+ client-slot） · **兼看**：配
> **影响力**：npm 近 30 天 **2,243**（2026-11-01，42 个过影响力门的 bundle 之一）
> **研究范围**：`dsh-rhine-splash@0.2.8`，gitHead `8aa0961…`，tarball sha256 `bfae5708…`（588,189 B，24 文件）；DSH 对照 `0.2.1-rc.3`
> **证据成熟度**：源码级（host 注入与客户端配置实读；开屏组件的运行表现未实测）
> **一句话**：它不抢槽位，而是**在 HTML 生成的那一刻**把品牌、主题和开屏塞进去——代价是顺序与转义全归自己。
> **借鉴价值**：**① 首屏注入要 append，不能 prepend；② 往 HTML 里写用户配置必须双转义；③ 开屏频率是配置项，不是硬编码；④ 用 `ctx.inject` 而不是静态 `inject` 接可选服务。**

## 它想干什么 · 为什么值得借鉴

**意图。** 把 DSH 的默认外观换成一整套"Rhine"品牌：主题色、图集、logo、开屏动画、账单面板 `[SRC-TARGET]`（`lib/index.js:439-445`，`lib/client.js:10`）。

**意义。** 42 个过影响力门的 bundle 里，**只有它用 `index-inject`**——大多数换肤走客户端槽位（React 挂上去再改），而它选择在**页面字符串生成期**动手。这是两条完全不同的路：一条是"渲染后改"，一条是"渲染前就是"。

**用户价值。** 装之前，换肤类插件普遍会在首次加载时闪一下默认配色；装之后，主题属性在首屏 HTML 执行时就已经落在 `<html>` 上 `[SRC-TARGET]`（`lib/index.js:328` 的同步脚本）。代价是它必须自己处理"注入内容里出现 `</script>`"这类事。

**表达。** 注入体是一个内联脚本，先把 `globalThis.__RHINE_BRAND__` 与 `__RHINE_SPLASH__` 赋值，再**同步**改 `document.documentElement` 的属性 `[SRC-TARGET]`（`lib/index.js:326-328`）。顺序不是随意的：先数据、后 DOM。

## 1. 阶段与载体

- **阶段**：起。它改的是"页面怎么生成"，不是"装不装得上"。
- **载体**：`index-inject`——通过 `ctx.on('webserver/index-inject', table => table.push(...))` 往宿主生成的 HTML 里追加条目 `[SRC-TARGET]`（`lib/index.js:439-445`）。
- **兼看**：配。`splashWhen` 是配置项（见 §3），属于默认值那一层。

## 2. 机制

```js
// lib/index.js:438-445
// Append after theme bootstrap rows: do not pass Cordis's prepend option.
ctx.on('webserver/index-inject', (table) => {
  const resolved = readConfig(config);
  const { logo } = resolved;
  const brand = { mark: marks[logo], hero: heroes[logo] || marks[logo], name, marks, heroes: {...} };
  table.push(...buildInjections(resolved, { ...assets, brand }));
});
```

`buildInjections` 返回三类条目 `[SRC-TARGET]`（`lib/index.js:312-330`）：

1. `{ kind: 'style' }`：主题 CSS、图片 CSS、主 CSS；
2. `{ kind: 'script', placement: 'body' }`：赋值 `__RHINE_BRAND__` / `__RHINE_SPLASH__`，并**同步**写 root 属性；
3. 全部字符串先过 `safeJson` / `safeStyle`（见 §4）。

### 三条失败态

| 态 | 表现 | 用户看到什么 |
|---|---|---|
| **注入没进** | 事件回调注册失败或 `table.push` 在别的行之后 | 页面完全正常，只是没有品牌——**最难发现的一种** |
| **顺序错了** | 用 prepend 抢在主题引导行之前 | 先白一下再变色（FOUC），或主题被后到的行覆盖 |
| **转义漏了** | 用户配置里带 `</script>` 或 `</style>` | 页面被截断，白屏；错误出现在浏览器控制台，不在宿主日志 |

## 3. 设计取舍

| 取舍 | 选择 | 代价 |
|---|---|---|
| 改外观的时机 | 注入 HTML，而不是 React 挂载后再改 | 必须自己负责顺序、转义、冷却；换来无闪烁 |
| 注入顺序 | **append（不传 prepend）**，让宿主主题引导行先落地 `[SRC-TARGET]`（`:438`） | 自己的样式只能覆盖，不能抢先 |
| 开屏频率 | 配置项 `splashWhen`：`launch`（每次启动）/ `daily`（每天第一次）/ `update`（更新后），且 `command: true` 可从命令面板改 `[SRC-TARGET]`（`lib/client.js:30`；文案 `:311-312`） | 三档语义要各自实现，且要存"上次播到哪" |
| 可选服务 | `ctx.inject(['workspaceRegistry','sessionPersistence'], child => …)` 延迟挂载 `[SRC-TARGET]`（`lib/host/archives.js:131`） | 比静态 `inject` 多一层回调 |

## 4. 与宿主既有行的边界

宿主已经决定"页面由谁生成"，本插件只**追加**条目，不替换渲染管线。它甚至没有自己的客户端入口 DOM——`dsh.client` 声明了 9 个 inject，但画面完全由那一段注入脚本与随后的客户端模块共同决定 `[PKG]`。

**这条边界的实际含义**：注入是"只读叠加"，一旦宿主换了 HTML 骨架，注入点就可能失效——而失效时**页面依然正常**，属于静默降级。

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 首屏换主题会闪一下 | 在 HTML 生成期注入：先赋值数据全局，再由**同步脚本**改 `documentElement` 属性 | `[SRC-TARGET]` `lib/index.js:326-328`（赋值 + 同步改 root）；`:439-445`（注册追加入口） | 样式在首帧前就位；代价是失去 React 的状态管理，只能靠属性与 CSS 变量 | 定义"注入体里只做同步副作用、不含异步等待" | 只对"允许追加 HTML 注入"的宿主成立 | 改成挂载后再改 → 用户看到闪白 |
| 注入顺序会决定谁生效 | 用 **append**，显式不传 prepend，让宿主的主题引导行先落地 | `[SRC-TARGET]` `lib/index.js:438` 的注释与实现 | 宿主默认值不被第三方抢；代价是自己只能覆盖、不能抢先 | 在文档里写清"本插件不 prepend"，并给出验证方法 | 只对存在"主题引导行"的宿主成立 | prepend → 闪白或被后到行覆盖，且难定位 |
| 往 HTML 写用户配置 | 双转义：JSON 的 `<` → `\u003c`、U+2028/29 转义；CSS 的 `</style` 转义 | `[SRC-TARGET]` `lib/index.js:313-317`（`safeJson` / `safeStyle`） | 防脚本/样式逃逸；代价是注入体不可读、排错要解转义 | 规定所有进 HTML 的字符串必须过同一对函数 | 只对"把配置塞进内联脚本/样式"的写法成立 | 漏转义 → `</script>` 截断页面，白屏 |
| 开屏频率不该写死 | 做成三档配置（每次/每天/更新后），并从命令面板可改 | `[SRC-TARGET]` `lib/client.js:30`（`splashWhen` 三选一 + `command: true`） | 用户可关、可降频；代价是要维护"上次播放"状态与三档语义 | 定义默认档，并给"关掉"的最短路径 | 只对"首屏有额外动画"的产品成立 | 写死成每次启动 → 高频用户第一件事就是卸载 |
| 需要可选服务时 | 用 `ctx.inject([...], child => …)` 延迟挂载，而不是把它写进静态 `inject` | `[SRC-TARGET]` `lib/host/archives.js:131` | 服务缺失只让那块功能不挂，不至于让整行 pending | 把可选依赖统一走 `ctx.inject`，必选才写静态 `inject` | 只对支持 `ctx.inject` 的 loader 成立 | 静态 `inject` 里写可选服务 → 行停在 pending（见 `TRAPS` §11） |

## 6. 失效与开放问题

- `[OPEN]` 开屏"每天第一次 / 更新后"的判定实现：本卡只核到配置项与文案（`client.js:30`、`:311-312`），**没定位到读取"上次播放"的代码**。复核动作：在 `client.js` 里追 `splashWhen` 的消费点。
- `[OPEN]` 注入失效时是否有任何告警（本卡判断为静默降级，未实测）。
- `[OPEN]` 宿主换 HTML 骨架后注入点是否仍存在（未实测）。
- `[OPEN]` `maxWait` 兜底是否存在（fanout 提过，源码未命中，暂不写入结论）。

## 7. 兼看

- 配：`splashWhen` 属于 [`CONFIG`](../config/README.md) 说的"bundle 层默认值 + 用户覆盖"。
- 坑：静态 `inject` 的问题已记在 [`TRAPS`](../practice/TRAPS.md) §11。
