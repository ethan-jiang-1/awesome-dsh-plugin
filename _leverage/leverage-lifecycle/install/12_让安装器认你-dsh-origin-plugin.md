---
title: "让安装器认你 · origin-plugin：两个看不见的判定"
domain: lifecycle
kind: sample
positioning: "一个只有 patch、没有代码的 bundle，如何被市场认成“可安装”和“活着”——以及为此付出的两条空行。"
takeaway: "插件市场判你，靠的是入口工件与 loader 里的 fiber 两件事；只靠 patch 供货的 bundle 两者都没有，会永远显示“restart to apply”。"
read_when: "要发一个以 patch 为主、自己不写运行时逻辑的 bundle；或装完在市场里一直显示未生效。"
status: observed
updated: 2026-11-01
budget: 140
---
# 让安装器认你 · origin-plugin

> **阶段**：装 · **载体**：host-row + `!!js`（兼 own-cli：另给 npx 用户一个 `bin`） · **兼看**：起
> **影响力**：npm 近 30 天 **2,485**（2026-11-01，42 个过影响力门的 bundle 之一）
> **研究范围**：`dsh-origin-plugin@2.7.3`，gitHead `4010683f…`，tarball sha256 `8312f0f8…`（1,283,990 B，117 文件）；DSH 对照 `0.2.1-rc.3`
> **证据成熟度**：源码级（patch 与入口实读；Python 侧未运行）
> **一句话**：它 90% 的价值在 `cordis.patch.yml` 里，却必须额外写一条自挂载行和一个"不许有返回值"的 `apply`，否则市场永远当它没装好。
> **借鉴价值**：**① 市场判"可安装"看入口工件；② 判"活着"看 loader 里有没有你的 fiber；③ 外部进程的绝对路径必须 `!!js` 自定位；④ 覆盖同名条目只能 config-only。**

## 它想干什么 · 为什么值得借鉴

**意图。** 把一个 Python MCP server（Origin 绘图，28 个工具）挂进 DSH。它自己**不实现任何工具**——`index.js` 顶部原话：*the actual server is origin_mcp_server.py, launched by DSH through the mcp-origin loader entry* `[DOC]`（`index.js:3-5`）。

**意义。** 这正好是"bundle 的边界"最极端的一种：**包里没有运行时逻辑，只有一行 insert**。而生态里绝大多数 bundle 至少挂一个自己的插件。作者被迫去撞两个平时看不见的判定，并把撞法写进注释——这就是本卡的全部价值。

**用户价值。** 装之前，用户面对的是"一个连 Python 都没有的机器"和"相对路径解析到 DSH 可执行目录"两个坑；作者的答案是 `!!js` 按 `DSH_HOME` 自定位 `[SRC-TARGET]`（`cordis.patch.yml:71-72`），外加一句"server 连不上只记日志、不注册工具，绝不让 DSH 启动失败" `[DOC]`（`:14-16`）。

**表达。** 注释写得像事故复盘：v2.0.2 修了路径、v2.0.4 修了 60 秒启动挂起——后者是 anyio 的 `_make_self_pipe` 用 socketpair 走回环，被防火墙阻塞导致永不响应 `initialize` `[DOC]`（`:29-35`）。**把失败史直接写在 patch 顶部的样本很少见**，这让后来者能判断"我要不要抄"。

## 1. 阶段与载体

- **阶段**：装。它回答的是"装完怎么被认到"，不是"界面长什么样"。
- **载体**：`host-row`（`mcp-origin` 一条 insert）+ `!!js` 表达式；另外有 `bin`（`dsh-origin-mcp`）给**没有 DSH 的用户**用 npx 直起 `[PKG]`。
- **兼看**：起。`failOnStartupError: false` 决定它装坏时不拖垮启动。

## 2. 机制

`mcp-origin` 这条 insert 是本体的全部 `[SRC-TARGET]`（`cordis.patch.yml:61-76`）：

```yaml
- id: mcp-origin
  name: '@deepseek-ai/dsh-mcp-client'
  config:
    transport: stdio
    command: python
    args: ['-u', '-X', utf8,
      !!js (process.env.DSH_HOME || (String(process.env.USERPROFILE) + '/.dsh')) + '/profiles/web/node_modules/dsh-origin-plugin/origin_mcp_server.py']
    cwd: !!js (process.env.DSH_HOME || (String(process.env.USERPROFILE) + '/.dsh')) + '/profiles/web/node_modules/dsh-origin-plugin'
    failOnStartupError: false
```

### 两个看不见的判定

这两条是作者用注释和空函数"买"来的，也是本卡的核心：

| 判定 | 它查什么 | 只写 patch 会怎样 | 作者的对策 |
|---|---|---|---|
| **入口工件** | files / main 里有没有真入口 | 被判成"source-only"，要 `allowBuilds` 才能装，甚至报"没有可安装的内容" | 发一个 `index.js` `[PKG]`（`main: ./index.js`） |
| **loader 活性** | loader 的 entry-name 集合里有没有你的包名 | 只有 `@deepseek-ai/dsh-mcp-client` 一个名字 → 永远显示 "restart to apply" | 插一条 **no-op 自挂载行** + 一个不返回值的 `apply` |

原文与实现 `[SRC-TARGET]`：

```yaml
# cordis.patch.yml:78-85
# Self-mount: a no-op fiber so the plugin market reads this bundle as
# "live/active" (verify.js liveIncludes checks for the package name ...)
- id: dsh-origin-plugin
  name: dsh-origin-plugin
```

```js
// index.js:60-81 —— 注意它不是"空函数"
export default {
  ...plugin,
  apply(ctx) {
    if (ctx && typeof ctx.effect === 'function') {
      ctx.effect(() => { /* 卸载时通知 Python 引擎优雅退出，失败也不抛 */ })   // :63-75
    }
    return void 0                                                            // :80
  },
}
```

**`return void 0` 那一行是防御性的，不是随手写的**：作者注释写明 Cordis 会把 `apply()` 的返回值当 effect 处理，返回普通对象会抛 `TypeError: Invalid effect`，**DSH 启动直接崩溃**（`:76-79`，标注 issue #1 实证、DSH ≥0.1.5 必现）。

作者甚至在注释里引了对方的行号：*"restart to apply" (L162: if (inBundles && !loaderLive) → state='restart')* `[DOC]`（`index.js:52`）。

### 三条失败态

| 态 | 表现 | 用户看到什么 |
|---|---|---|
| **读不到 Python / venv** | `failOnStartupError: false` 让它只记日志、不注册工具 | 装了，但工具列表里没有；启动正常 |
| **装不进 roster** | 包在依赖里，`dsh.profile.bundles` 没它 | 什么都不发生，退出码 0 |
| **起了不生效** | loader 有 fiber，但 MCP server 握手失败 | 市场显示"活着"，工具却调不通——**比"没装"更难查** |

## 3. 设计取舍

| 取舍 | 选择 | 代价 |
|---|---|---|
| 逻辑放 Python 还是 JS | 全放 Python，JS 只留空壳 | 跨语言依赖 Python 环境；空壳必须解释清楚，否则下一个人会删掉它 |
| 路径怎么定位 | `!!js` 在启动期按 `DSH_HOME` 拼绝对路径 | 硬编码 `profiles/web`，**换 profile 名就失效** `[SRC-TARGET]`（`:71-72`） |
| stdio 怎么实现 | 弃 anyio 事件循环，改同步 JSON-RPC 循环 | 放弃异步；换来的是不再依赖回环 socketpair `[DOC]`（`:29-35`） |
| 分发面 | patch 主力 + `bin` 给无 DSH 用户 | 两条入口要各自维护、各自文档 |
| 卸载时怎么收尾 | 注册 `ctx.effect` 通知 Python 引擎优雅退出，**不 kill `Origin64.exe`** | 只能尽力；用户可能还在手动用 Origin，残留进程交给 `DSH_ORIGIN_AUTOKILL` `[DOC]`（`index.js:55-59`） |

## 4. 与宿主既有行的边界

**只插一条 `mcp-origin`。** 作者写死了一条红线：在 profile 里再加一条完整同名 insert → `duplicate loader entry id: mcp-origin` → **直接启动失败** `[DOC]`（`:16-18`、`:58`）。

覆盖时只能 config-only，且**必须带全字段**——因为 patch 是整体替换 `config`，不是合并 `[DOC]`（`:43-52` 给了完整示例）。

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 只发 patch 的 bundle 装不上 | 包里必须有**真入口工件**（`main` + 实际文件），让安装器能判"这是预构建产物"而不是"源码待构建" | `[PKG]` `main: ./index.js`、`files` 含 `index.js`；`[DOC]` `index.js:6-13` 说明 source-only 会被拒 | 免掉 build approval；代价是包体多一个必须解释的空模块 | 给 bundle 加一个最小入口，并在文件头写清"它为什么存在" | 只对"以入口工件判可安装性"的安装器成立 | 删掉空壳 → 装不上，或被要求 `allowBuilds` |
| 市场永远显示"restart to apply" | 让 **loader 里出现你自己的包名**：插一条 no-op 自挂载行，配空 `apply` | `[SRC-TARGET]` `cordis.patch.yml:84-85`；`index.js:62` 空 `apply`；`[DOC]` `index.js:15-19` | 活性判定从"我挂了别人的行"变成"我有自己的 fiber"；代价是多一条没有功能的行 | 定义"bundle 自身是否需要在 loader 里有一条行"的规则并写进发布检查 | 只对"按 loader entry-name 判活"的市场成立 | 不挂 → 永远显示未生效，用户重复重启 |
| 插件目录在运行时不可知 | 用 `!!js` 在启动期按 `DSH_HOME` 拼绝对路径，**不依赖进程工作目录** | `[SRC-TARGET]` `cordis.patch.yml:71-72`；`[DOC]` `:9-13` 记录旧版相对路径导致工具永不注册 | 修复"相对路径解析到 DSH 可执行目录"；代价是路径里写死了 `profiles/web` | 用 profile 名变量替代硬编码，或从 `profileContext` 取 | 只在 web 面、且 `DSH_HOME` 有默认值时可回退 | 硬写 `profiles/web` → 换 profile 或 Desktop 就找不到文件 |
| 外部依赖挂了不该拖垮启动 | `failOnStartupError: false` + 工具调用时再报错 | `[SRC-TARGET]` `cordis.patch.yml:76`；`[DOC]` `:14-16` | 启动不失败、不挂起；代价是"装了但没工具"变成一种合法状态 | 给每个外部进程行定容错策略，并给用户一个自检入口 | 只对支持该字段的行类型成立 | 设成 true → 一个连不上，整个 profile 起不来 |
| 同名条目被覆盖两次 | 覆盖必须 **config-only 且带全字段**，并禁止第二条完整 insert | `[DOC]` `cordis.patch.yml:16-18`、`:43-52`、`:58` | 避免 `duplicate loader entry id`；代价是覆盖样板很长、易漏字段 | 发布"覆盖示例"而非"插入示例" | 只对整体替换语义的 patch 成立 | 写第二条 insert → 启动直接失败 |
| `apply` 顺手 `return {}` 想表明"我是谁" | cordis 把 `apply()` 的返回值当 effect 消费；返回普通对象抛 `TypeError: Invalid effect`，**启动直接崩溃** | `[SRC-TARGET]` `index.js:80` 显式 `return void 0`；`[DOC]` `index.js:76-79` 标注 issue #1、DSH ≥0.1.5 必现 | 显式返回 undefined；代价是"返回插件描述符"这种直觉写法被禁 | 规定 `apply` 只做副作用、不返回值，描述走单独 export | 只对"把返回值当 effect"的 loader 成立 | 返回对象 → 整个 profile 起不来，报错点离真正原因很远 |

## 6. 失效与开放问题

- `[OPEN]` Python 侧同步 stdio 循环是否真的解决了 60s 挂起。复核动作：在隔离环境用 `--doctor` 与一次 `initialize` 握手计时。
- `[OPEN]` 路径硬编码 `profiles/web`：在 `desktop` profile 下是否可用。复核动作：同一台机器读 `profiles/desktop` 的 patch 代入。
- `[OPEN]` 市场的 `liveIncludes` 判定是否对所有市场实现一致（本卡只引作者注释与 `index.js:52`）。
- `[OPEN]` `bin` 与 bundle 两条入口同时存在时，安装器会不会误判（未实测）。

## 7. 兼看

- 起：`failOnStartupError` 与 [`BOOT`](../boot/README.md) §1 的失败分级同源；"同步循环修 60s 挂起"是 bundle 之外的启动事故。
- 装：入口工件那条与 [`INSTALL`](./README.md) §2 的三态检查互补——**三态查的是 roster，市场查的是入口与 fiber**。
