---
title: "让安装器认你 · origin-plugin：市场判“活着”的三级证据"
domain: lifecycle
kind: sample
positioning: "一个只有 patch 的 bundle，如何被市场认成“可安装、活着”——以及 1.73.6 为什么已经不需要那条自挂载空行。"
takeaway: "市场只是消费者：它先看 loader 里有没有你的条目（或你插入的条目），再看 profile manifest，最后才看你的 patch；host 的 loader/roster 才是事实源。"
read_when: "要发一个以 patch 为主、自己不写运行时逻辑的 bundle；或装完在市场里一直显示未生效。"
status: observed
updated: 2026-11-01
budget: 170
---
# 让安装器认你 · origin-plugin

> **阶段**：装 · **载体**：host-row + `!!js`（兼 own-cli：另给 npx 用户一个 `bin`） · **兼看**：起
> **影响力**：npm 近 30 天 **2,485**（2026-11-01，42 个过影响力门的 bundle 之一）
> **研究范围**：`dsh-origin-plugin@2.7.3`，gitHead `4010683f…`，tarball sha256 `8312f0f8…`（1,283,990 B，117 文件）；**市场侧对照** `dshmarket@1.73.6`，sha256 `8790a060…`（860 KB，122 文件）；DSH 对照 `0.2.1-rc.3`
> **证据成熟度**：**实测级**（隔离 profile 真装 + 直接调用市场 `verifyActivation`，[`_证据/03`](../_证据/03_样本实测记录.md) E28）+ 源码级（sample 与市场实现实读；未跑市场 UI）
> **DSH 立场**：**有条件偏离**——carrier 走 bundle patch 是原生路径；两处越界：patch 里写死 `profiles/web`、把第三方市场判定当“活着的标准”。市场只是消费者，host 的 loader/roster 才是事实源。
> **一句话**：作者用一条空 fiber 换来的“活着”，在 1.73.6 已被市场用“你插入的行”兜住——值得抄的是**判断顺序**，不是那条空行。
> **借鉴价值**：**① 先读 host 的 loader/roster，再读市场（市场只是消费者）；② carrier 用“自己 patch 插入的 entry id”证明活着；③ 入口工件是可枚举形状；④ 判 `broken` 可能被市场卸载，退出码不会告诉你。**

> **不要抄**：把第三方市场（`dshmarket`）的状态判定当 DSH 语义标准；在 patch 里写死 `profiles/web`。host 的事实源是 `pluginManager`/loader，市场只是消费者；路径从 `DSH_HOME`/`profileContext` 派生。

## 它想干什么 · 为什么值得借鉴

**意图。** 把一个 Python MCP server（Origin 绘图，28 个工具）挂进 DSH。它自己**不实现任何工具**——`index.js` 顶部原话：*the actual server is origin_mcp_server.py, launched by DSH through the mcp-origin loader entry* `[DOC]`（`index.js:3-5`）。

**意义。** 这是 bundle 边界最极端的一种：**包里没有运行时逻辑，只有一行 insert**。作者因此撞上两个平时看不见的判定：安装器认不认“入口”，市场认不认“活着”。**这两个判定在 1.73.6 已经演化**——市场新增了 `carriedRowLive`（#156）专门兜住这种只有 patch 的 carrier bundle。这张卡因此有两层价值：作者的解法值得看，市场的修正更值得看。

**用户价值。** 装之前，用户面对的是“一个连 Python 都没有的机器”和“相对路径解析到 DSH 可执行目录”两个坑；作者的答案是 `!!js` 按 `DSH_HOME` 自定位 `[SRC-TARGET]`（`cordis.patch.yml:71-72`），外加一句“server 连不上只记日志、不注册工具，绝不让 DSH 启动失败” `[DOC]`（`:14-16`）。

**表达。** 注释写得像事故复盘：v2.0.2 修了路径、v2.0.4 修了 60 秒启动挂起——后者是 anyio 的 `_make_self_pipe` 用 socketpair 走回环，被防火墙阻塞导致永不响应 `initialize` `[DOC]`（`:29-35`）。**把失败史直接写在 patch 顶部的样本很少见**，这让后来者能判断“我要不要抄”。

## 1. 阶段与载体

- **阶段**：装。它回答的是“装完怎么被认到”，不是“界面长什么样”。
- **载体**：`host-row`（`mcp-origin` 一条 insert）+ `!!js` 表达式；另外有 `bin`（`dsh-origin-mcp`）给**没有 DSH 的用户**用 npx 直起 `[PKG]`。
- **兼看**：起。`failOnStartupError: false` 决定它装坏时不拖垮启动。

## 2. 机制

### 作者的做法：两个“隐形判定”与两条补丁

```yaml
# cordis.patch.yml:61-76（节选）
- insert:
    - id: mcp-origin
      name: '@deepseek-ai/dsh-mcp-client'
      config:
        transport: stdio
        command: python
        args: [ ... ]           # !!js 按 DSH_HOME 自定位，:71-72
        failOnStartupError: false
    # Self-mount: a no-op fiber so the plugin market reads this bundle as
    # "live/active" ... — :78-85
    - id: dsh-origin-plugin
      name: dsh-origin-plugin
```

```js
// index.js:60-81 —— 空 apply，但必须 return void 0
export default {
  ...plugin,
  apply(ctx) {
    if (ctx && typeof ctx.effect === 'function') ctx.effect(() => { /* :63-75 */ })
    return void 0                                                            // :80
  },
}
```

作者注释把两个判定写成：**入口工件**决定“能不能装”，**loader fiber** 决定“市场认不认你活着” `[DOC]`（`index.js:6-19`）。下面用市场源码逐条对。

### 市场怎么判：七态、三级证据

**先把 DSH 侧事实源摆前面**：`pluginManager`/loader 是 host，`dsh.profile.bundles` 是 host 的 roster；市场只是第三方消费者，它的七态会随版本变。

市场（`dshmarket@1.73.6`）的 `verifyActivation()` 把“装上了”拆成 **7 种状态** `[SRC-TARGET]`（`lib/verify.js:17-28`）：

| 状态 | 含义 | 谁给出 |
|---|---|---|
| `live` | 当前组合里活着（热挂载或 loader 条目） | 观察 |
| `restart` | 已装、下次启动会加载，但现在不活着 | manifest 推断 |
| `incompatible` | 宿主的启动门每次都跳过它——重启永远没用 | manifest 推断 |
| `inert` | 装了但不是 profile 层插件（普通依赖 / 纯客户端 shim） | manifest 推断 |
| `broken` | 会加载失败：声明了 bundle 却没有可加载面，或入口产物缺失 | 推断 |
| `missing` | `node_modules` 里没有 | 观察 |
| `disabled` | 用户/补丁层明确关掉，重启后保持关闭 | 开关状态 |

**证据按严格优先级使用** `[SRC-TARGET]`（`lib/verify.js:1-16`）：

1. **loader inventory（观察）**：loader 正在跑的条目就是活的，**任何 manifest 事实都不能推翻它**（连没有 `dsh` 字段的普通库也可能被别人的 patch 加载）；
2. **profile manifest（推断）**：`dsh.profile.bundles` 预测下次启动会加载什么，是非运行包的唯一证据；
3. **profile patch（补充）**：用户自己的 `cordis.patch.yml` 里按名引用了它，可把 `broken` 升级为已装（`patchLoads`，`:150-163`）。

**对 carrier bundle 的关键修正（#156）**：`loaderLive = liveIncludes(live, name) || carriedRowLive(live, activeProfileDir, name)` `[SRC-TARGET]`（`lib/verify.js:400`）。

- `liveIncludes` 只看 loader 条目的 `name:`，允许 subpath（`pkg/subpath`），但要求 `/` 边界，避免 `@scope/pkg2` 命中 `@scope/pkg`（`:91-105`）；
- `carriedRowLive` 检查**你自己的 bundle patch 插入了哪些 entry id**，再看这些 id（`#id`）是否活着（`:108-128`）。作者那条 `mcp-origin` 的 id 就是证据——**因此 1.73.6 里，自挂载空行已经不再是“活着”的必要条件**；它只在没有 `carriedRowLive` 的旧市场/其他市场里才有意义。
- 旧市场正是用“包名在不在 live 集合”这一条判，才出现作者注释里的 *"restart to apply" forever*（作者引的 L149/L162 已随版本漂移，符号仍在）。

**已实测（E28）**：真装 `dsh-origin-plugin@2.7.3` 后直接调 `verifyActivation`：

| live 集合 | 判定 |
|---|---|
| `∅` | `restart`（入口在，没判 `broken`） |
| `#mcp-origin` | **`live`**（carriedRowLive） |
| `dsh-origin-plugin` | `live`（liveIncludes） |
| `@deepseek-ai/dsh-mcp-client` | `restart`（只看到别人的条目名） |

也就是说：**1.73.6 里作者的空行确实多余；但“市场只看到你挂的别人条目名”仍会判未生效**——作者当年看到的现象是真的，解法已经被市场收编。

### “入口工件”到底是什么

市场的 install 校验用 `hasLoadableEntry`，**不是** `entryArtifactExists` `[SRC-TARGET]`（`lib/install.js:855-870`、`lib/profile.js:1396-1430`）：

- `entryArtifactExists`：看 `main`、`exports`（字符串、`.`、或对象里的字符串值），都没有才回退 `index.js`（`lib/profile.js:850-869`）。**这是可枚举的形状，不是“有没有 lib/”**。
- `hasLoadableEntry`：carrier（自己没入口）**只要它 patch 挂载的目标里有可加载入口**就成立；目标按 hoisted、carrier 内、workspace 根、**宿主安装树**四种位置解析（#906，`lib/profile.js:1418-1432`）。
- 判 `broken` 的包会被 `validateAddedPlugins` **直接卸载**（`lib/install.js:855-870`）——这是比“显示未生效”更严重的失败态：**安装退出码 0，包随后消失**。

所以作者当年“必须发一个真实 `index.js`”的判断，准确说法是：**入口必须能被枚举到，或者你挂载的目标能被枚举到**；纯 patch 的 carrier 本身合法，但挂一个连入口都没有的包仍会被判 `broken`。

### 三条失败态

| 态 | 表现 | 用户看到什么 |
|---|---|---|
| **入口/挂载目标不可加载** | `hasLoadableEntry` 假 → 判 `broken` → 市场卸载 | 装完过一会儿包没了；退出码 0 `[SRC-TARGET]`（`install.js:855-870`）；E28 用手造 fake carrier 复现了 `broken` 谓词 |
| **市场不认“活着”** | 无 live 条目、无 carried row → `restart` | 卡片永远提示“重启后生效”，重启也不变 `[SRC-TARGET]`（`verify.js:400`） |
| **宿主门不兼容** | `incompatible` | 重启永远没用；只能换版本或豁免 `[SRC-TARGET]`（`verify.js:536-551`） |

## 3. 设计取舍

| 取舍 | 选择 | 代价 |
|---|---|---|
| 逻辑放 Python 还是 JS | 全放 Python，JS 只留空壳 | 跨语言依赖 Python 环境；空壳必须解释清楚，否则下一个人会删掉它 |
| 路径怎么定位 | `!!js` 在启动期按 `DSH_HOME` 拼绝对路径 | 硬编码 `profiles/web`，**换 profile 名就失效** `[SRC-TARGET]`（`:71-72`） |
| 空行还要不要写 | 1.73.6 不写也能被 `carriedRowLive` 认活；**旧市场仍需要** | 写了多一条无功能行；不写则对旧市场“永远未生效” |
| 入口工件 | 发一个真实 `index.js`（哪怕 `export {}`） | 免掉“source-only”误判；代价是包体多一个必须解释的文件 |
| 分发面 | patch 主力 + `bin` 给无 DSH 用户 | 两条入口要各自维护、各自文档 |
| 卸载时怎么收尾 | 注册 `ctx.effect` 通知 Python 引擎优雅退出，**不 kill `Origin64.exe`** | 只能尽力；残留进程交给 `DSH_ORIGIN_AUTOKILL` `[DOC]`（`index.js:55-59`） |

## 4. 与宿主既有行的边界

**只插一条 `mcp-origin`。** 作者写死了一条红线：在 profile 里再加一条完整同名 insert → `duplicate loader entry id: mcp-origin` → **直接启动失败** `[DOC]`（`:16-18`、`:58`）。

覆盖时只能 config-only，且**必须带全字段**——因为 patch 是整体替换 `config`，不是合并 `[DOC]`（`:43-52` 给了完整示例）。这与 [`install/14`](./14_覆盖行的身份陷阱-dsh-tinyfish.md) 的 `name` 断言是同一条边界。

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 市场永远显示“未生效” | 先读 host 的 loader/roster，再读市场的状态机：**观察 > manifest > 你的 patch**；carrier 用“自己插入的 entry id”证明活着，不必先造空行 | `[SRC-TARGET]` `verify.js:17-28`（七态）、`:400`（loaderLive = liveIncludes ∨ carriedRowLive）、`:108-128`（#156） | 判定与市场实现同构，不会为一个已经不存在的 bug 加行；代价是要跟市场版本 | 把“我的包名是否在 live 集合”换成“我的 patch 插入了哪些 id、哪些活着” | 只对实现了 carried-row 判定的市场成立；旧市场仍只看包名；不要把市场判定当 DSH 语义 | 照抄旧解法 → 多一条无功能行，且误以为它是普遍规律 |
| 只发 patch 的 bundle 装不上 | 用 `hasLoadableEntry` 的口径自检：入口可枚举，或你挂的目标可枚举；carrier 是合法形态 | `[SRC-TARGET]` `profile.js:1396-1430`（#103/#906）、`:850-869`（入口形状）；`install.js:855-870` | 纯 patch 包能过安装校验；代价是挂载目标必须真实存在且可加载 | 发一个 `export {}` 的入口，或确认挂载目标在宿主安装树里可解析 | 只对实现了 carrier 豁免的市场成立 | 挂一个没有入口的包 → 判 `broken` 并被卸载 |
| 装完过一会儿包没了 | 把“市场卸载”当成一种失败态：安装退出码 0 不代表包还在；发布前在干净 profile 里装一次并复查 `node_modules` | `[SRC-TARGET]` `install.js:855-870`（`removedBroken` → `removeAndReconcile`） | 能提前发现“入口不可加载”这类静默失败；代价是多一步验收 | 发布检查加“装后 30 秒仍在 + 市场状态不是 broken” | 只对带安装后校验的市场成立 | 只看退出码 → 用户装完包消失，还以为是自己的网络问题 |
| 入口工件到底要什么 | 入口是**可枚举的形状**：`main` / `exports`（含 `.` 与对象值）/ 回退 `index.js`；不是“有 lib 目录” | `[SRC-TARGET]` `profile.js:850-869` | 最小真实入口即可；代价是空入口需要注释解释 | 发 `index.js` 并写明“composition only” | 只对按 manifest 判入口的安装器成立 | 发一个空目录或只有 README → 判 source-only / broken |
| 同名条目被覆盖两次 | 覆盖必须 **config-only 且带全字段**，并禁止第二条完整 insert | `[DOC]` `cordis.patch.yml:16-18`、`:43-52`、`:58`；`[DSH]` `dsh-app-boot/lib/index.js:100-101`（name 不符 → warn + skip） | 避免 `duplicate loader entry id`；代价是覆盖样板很长、易漏字段 | 发布“覆盖示例”而非“插入示例” | 只对整体替换语义的 patch 成立 | 写第二条 insert → 启动直接失败 |
| `apply` 顺手 `return {}` 想表明“我是谁” | cordis 把 `apply()` 的返回值当 effect 消费；返回普通对象抛 `TypeError: Invalid effect`，**启动直接崩溃** | `[SRC-TARGET]` `index.js:80` 显式 `return void 0`；`[DOC]` `index.js:76-79` 标注 issue #1、DSH ≥0.1.5 必现 | 显式返回 undefined；代价是“返回插件描述符”这种直觉写法被禁 | 规定 `apply` 只做副作用、不返回值，描述走单独 export | 只对“把返回值当 effect”的 loader 成立 | 返回对象 → 整个 profile 起不来，报错点离真正原因很远 |

## 6. 失效与开放问题

- `[OPEN]` `carriedRowLive` / `hasLoadableEntry` 在更早的市场版本里从哪个版本开始存在（本卡只核 1.73.6）。复核动作：取 1.70–1.73 的 `verify.js`/`profile.js` 做 diff。
- `[OPEN]` 其他市场实现（非 `dshmarket`）是否也做了 carrier 豁免。
- `[OPEN]` Python 侧同步 stdio 循环是否真的解决了 60s 挂起。复核动作：在隔离环境用 `--doctor` 与一次 `initialize` 握手计时。
- `[OPEN]` 路径硬编码 `profiles/web`：在 `desktop` profile 下是否可用。
- **已关**：自挂载空行对 1.73.6 不是“活着”的必要条件（`verify.js:108-128`、`:400`）；它在旧市场里仍然必要。

## 7. 兼看

- 起：`failOnStartupError` 与 [`BOOT`](../boot/README.md) §1 的失败分级同源；"同步循环修 60s 挂起"是 bundle 之外的启动事故。
- 装：入口工件那条与 [`INSTALL`](./README.md) §2 的三态检查互补——**三态查的是 roster，市场查的是入口、目标与 live 集合**；`name` 断言见 [`install/14`](./14_覆盖行的身份陷阱-dsh-tinyfish.md)。
- 产品册 [`51_分发与救生页`](../../leverage-reshape-product/plugin/51_分发与救生页-dsh-market.md)：同一个市场的分发/救生面。
