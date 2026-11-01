---
title: "REFERENCE · 被 DSH 认可的那一条分发路径"
domain: lifecycle
kind: playbook
positioning: "一条能同时写进 web 与 Desktop 文档的装法：发 bundle、在应用内装，CLI 只作 web 面的自动化。"
takeaway: "应用内安装是当前 profile 相对的，所以两面同一句话；--profile 是面绑定的，所以必然要写两条、必然错一条。"
read_when: "要定一个产品的分发方式；或解释为什么只写 --profile web 会让 Desktop 用户装不上。"
status: living
updated: 2026-11-01
budget: 190
---
# 被认可的那一条路

> 这一篇只给一条路和它的边界，四阶段的细节在 [`INSTALL`](../install/README.md) / [`BOOT`](../boot/README.md) / [`CONFIG`](../config/README.md) / [`FIRST-RUN`](../first-run/README.md)。

## 0. 三个动作

1. **发一个 bundle**：包里声明 `dsh.bundle.patch`，patch 里放你的 loader 行。
2. **让用户在他正在跑的那个界面里装**：`dsh web` 和 Desktop 用的是**同一个**侧栏 Plugins 页。
3. **文档只写这一段安装说明**；CLI 命令作为"web 面自动化"附在后面，并标明它不覆盖 Desktop。

这条路的全部优越性来自一个事实：**动作 2 没有 profile 参数**。

## 1. 分发物长什么样

最小可用形态（照抄可跑，实测见 [`_证据/02`](../_证据/02_隔离实测记录.md) E4）：

```json
{
  "name": "your-product",
  "version": "0.1.0",
  "type": "module",
  "main": "lib/index.js",
  "exports": { ".": "./lib/index.js", "./client": "./lib/client.js" },
  "dsh": {
    "bundle": { "patch": "./cordis.patch.yml" },
    "client": { "platform": "web", "inject": ["@deepseek-ai/dsh-client-ui-slots"] }
  }
}
```

```yaml
# cordis.patch.yml
- insert:
    - id: your-product        # 稳定 id,发布后不改
      name: 'your-product'    # 解析到本包
```

**`dsh.client` 只有你带浏览器部分时才写**；`inject` 写你实际用到的客户端包，不要多写。

可选但建议的两个版本声明：`engines.dsh`（地板）与 `dsh.compatibility.dshReleases`（逐版本枚举）。两者在不同宿主线上各自是门禁，只写一个会在另一条线上失效 `[CARD]`。

## 2. 用户怎么装

| 面 | 应用内（推荐，唯一两句通用） | CLI（只覆盖 web） |
|---|---|---|
| `dsh web` | 侧栏 **Plugins** 页 → 搜索/填入 → 安装 | `dsh plugin --profile web add <pkg>` |
| Desktop | **同一个** Plugins 页 | **不可用**：`--profile desktop` 被 CLI 拒绝 |

- 两面的 Plugins 页来自同一个客户端包 `@deepseek-ai/dsh-client-ui-plugin-manager`，它挂在 `dsh-web-app` 层，而 web 与 Desktop 共用这一层 `[DSH]`（`dsh-web-app/cordis.patch.yml:315-319`）。
- 它背后是同一个宿主服务 `plugin-manager`，在 `dsh-base` 层、**有 profile 上下文就启用** `[DSH]`（`dsh-base/cordis.patch.yml:20-22`）。
- 这套服务自述为 *Current-profile plugin and bundle management shared by dsh CLI, Web and agent tools* `[DSH]`；`installBundle(spec, options)` 无 profile 参数 `[DSH]`（`dsh-plugin-manager/lib/types/index.js:540`）。

**给产品的 README 只需要一句**：

> 在 DSH 的 **Plugins** 页安装 `your-product`（`dsh web` 与 Desktop 通用）；或用命令行：`dsh plugin --profile web add your-product`（**仅 `dsh web`**）。

## 3. 三个必须

1. **必须声明 `dsh.bundle.patch`。** 不声明也能装、也返回 0，但只算普通依赖、**不进 `dsh.profile.bundles`**，于是永不加载——只给一句 stderr `declares no dsh.bundle` `[RUN]`。
2. **必须用稳定的 row id + 自己的命名空间。** id 发布后不改；与"单装同款"并存时，同 id 会重复注册或互相覆盖 `[CARD]`。
3. **必须自己回答首启。** 原生只给一道令牌门，没有向导 `[RUN]`；不回答就等于把"第一次看到什么"交给用户猜。做法与代价见 [`FIRST-RUN`](../first-run/README.md)。

## 4. 允许的偏离（附代价）

| 偏离 | 什么时候可以 | 代价 |
|---|---|---|
| **自带安装器 / launcher**（shell 那条路） | 用户根本不用 `dsh web`，或要在他机器上装运行时 | 两面从此各维护一套更新与恢复；用户多一条升级线 `[CARD]` |
| **只发 CLI 一条命令** | 产品明确只面向 `dsh web` | **必须在文档里写"仅 web"**；否则 Desktop 用户会装进 `profiles/web` 然后看不到东西 `[CARD]` |
| **配置放自己的文件**而不是 DSH settings | 配置项与宿主无关，或需要跨 profile 共享 | 不跟随 profile 备份/迁移；用户要记第二个配置文件位置 |
| **自带更新器** | 你发的是应用而不是插件 | 与宿主升级竞态；必须自己定义"宿主版本不在区间时怎么办" `[CARD]` |
| **发 `.tgz` / 本地路径** | 内网、离线、审计环境 | 包的来源与签名要自己保证；`file:` 依赖写进了 profile 的 `package.json` `[RUN]` |
| **启动体验用 bundle 内的插件实现**（首屏注入、预置会话、工作区） | 要"打开就是这样"，但不想换入口 | **不构成偏离**：仍是应用内装、同一份 bundle，只是多一块 UI 或一次首启动作。载体见 [`FIRST-RUN`](../first-run/README.md) §6 |

**偏离不是错，不写明才是错。**

## 5. 四条禁止

1. **禁止把 `dsh plugin --profile desktop add ...` 当安装说明。** 普通 CLI 直接被拒（见 [`SURFACES`](./SURFACES.md) §2）。
2. **禁止在文档里只写 `--profile web` 且不提 Desktop。** 这正是本册存在的理由。
3. **禁止用 `$DSH_HOME/cordis.patch.yml` 给所有 profile 供货。** 它能覆盖行，不能提供包；插入未安装的包会 `ERR_MODULE_NOT_FOUND`，表现为"功能静默缺失"；只有该行不是 `required` 时才降为告警，`required` 行会启动失败 `[RUN]` `[DSH]`。
4. **禁止把"装完 exit 0"当安装成功。** 三态见 [`INSTALL`](../install/README.md) §2。

## 6. 为什么这条算"被认可"

不是因为它最方便，而是因为它是**唯一一条机制上对两个面同时成立的**：

1. 应用内安装的服务无 profile 参数 `[DSH]`；
2. 该服务在两面都由同一个 bundle 提供 `[DSH]`；
3. 两面的 profile 名不同（`web` / `desktop`），但服务不感知它 `[DSH]`；
4. CLI 侧相反：`--profile` 必填，且 `desktop` 被专门拒 `[DSH]` `[RUN]`；
5. 所以"CLI 一条通吃"在机制上不存在，文档里写它就必然对一面说谎。

> `[OBS]` **反例校验**：如果将来 DSH 支持"一次装到所有 profile"或 `--all-profiles`，这条结论就退化为"推荐"而不是"唯一"。目前 `dsh plugin --profile` 是单选（`selectProfile` 拒绝重复指定，`lib/bin.js:31-34`）。

## 7. 三条判据（可进 checklist）

1. 我的包声明了 `dsh.bundle.patch` 吗？
2. 我的安装说明里，那句"在 Plugins 页装"是否不需要区分 web 与 Desktop？
3. 我写 CLI 命令时，有没有标明它只覆盖 web？
