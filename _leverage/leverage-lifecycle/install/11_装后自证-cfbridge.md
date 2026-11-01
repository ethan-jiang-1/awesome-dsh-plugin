---
title: "装后自证 · cfbridge：安装器写好了，却没随包发出去"
domain: lifecycle
kind: sample
positioning: "把装完自证拆成五条可重跑命令的样本，以及 files 白名单如何把它们全部弄丢。"
takeaway: "安装器属于包的一部分：files 白名单漏掉 scripts/，五条命令对 npm 用户全部 404，而仓库里一切正常。"
read_when: "要发带安装/校验脚本的包；或想知道“装完怎么证明装上了”。"
status: observed
updated: 2026-11-01
budget: 130
---
# 装后自证 · cfbridge

> **阶段**：装 · **载体**：own-cli（npm scripts，不是 `bin`）+ host-row · **兼看**：起
> **影响力**：npm 近 30 天 **2,495**（2026-11-01，42 个过影响力门的 bundle 之一）
> **研究范围**：`@wenaixi/cfbridge@0.13.2`，gitHead `0e46aa20…`，tarball sha256 `64521a2d…`（200,864 B，32 文件）；DSH 对照 `0.2.1-rc.3`
> **证据成熟度**：**实测级**（隔离 profile 真装并执行命令，[`_证据/03`](../_证据/03_样本实测记录.md) E20）+ 源码级（tarball 实读）
> **一句话**：它把"装完怎么证明装上了"拆成五条可重跑命令——**但那五条脚本没有随包发布**。
> **借鉴价值**：**① `files` 白名单是安装器的头号杀手；② 启动安全的默认值该写在 patch 里，不是代码里；③ 外部凭据用 `!!js` 读环境，绝不落盘进 patch。**

## 它想干什么 · 为什么值得借鉴

**意图。** 让一个 DSH bundle 的安装变成**可验证、可回滚**的动作，而不是"装完祈祷"。它同时把外部 MCP server 挂进宿主：`mcp-cloudflare` 走 `dsh-mcp-client`，`cfbridge` 自己按包名挂载技能 Provider `[SRC-TARGET]`（`cordis.patch.yml:16-32`）。

**意义。** 生命周期里最缺的不是"能装"，是"**装完知道装成了**"。生态里多数包只给一条 `dsh plugin add`，装完靠肉眼。这个样本把 add、校验、导出配置、卸载拆成四个独立入口，是这条路线上少见的完整度。

**用户价值。** 装之前，用户没法回答"这条 bundle 到底进了没进 `dsh.profile.bundles`"；作者给出的答案是 `npm run dump:config` 与 `npm run validate:bundle` `[DOC]`。代价也清楚：这套东西只对**从仓库克隆**的人成立——见 §3。

**表达。** patch 顶部用五行注释交代"不重复声明宿主已有的 agent 栈行"、"token 只放被忽略的 `.dsh/.env`" `[DOC]`（`cordis.patch.yml:9-13`）。注释写得像给后来者看的交接单，不是营销。

## 1. 阶段与载体

- **阶段**：装。它不改变界面、不注册命令，价值全在"装完能不能自证"。
- **载体**：`own-cli`——但注意，它**没有 `bin`**（`[PKG]` `bin: false`）。所谓命令行入口是 **npm scripts**（`package.json:63-67`），只能 `npm run`，不能被 `dsh` 或 shell 直接调到。
- **兼看**：起。`failOnStartupError: false` 决定它装坏时**不拖垮启动**，那是启动侧的事。

## 2. 机制

patch 插入两行，都是 `dsh-mcp-client` 的实例 `[SRC-TARGET]`：

```yaml
# cordis.patch.yml:16-25
- id: mcp-cloudflare
  name: '@deepseek-ai/dsh-mcp-client'
  config:
    transport: streamable-http
    url: https://mcp.cloudflare.com/mcp
    headers:
      Authorization: !!js '`Bearer ${process.env.CLOUDFLARE_API_TOKEN}`'
    failOnStartupError: false
```

三个点值得抠：

1. **凭据在 patch 里是表达式，不是值。** `!!js` 在启动期求值，patch 文件因此可以进版本库 `[SRC-TARGET]`（`cordis.patch.yml:23`）。
2. **启动失败被降级为日志。** `failOnStartupError: false` `[SRC-TARGET]`（`cordis.patch.yml:25`），配 `reconnect` 退避（500ms → 30s，最多 10 次）。
3. **自证链在 package.json 里。** `install:bundle` / `validate:bundle` / `dump:config` / `repair:config` / `uninstall:bundle` 五条 `[SRC-TARGET]`（`package.json:63-67`），每条指向 `scripts/*.js`。

### 三条失败态

| 态 | 这一层怎么表现 | 用户看到什么 |
|---|---|---|
| **读不到 token** | `!!js` 求值成 `Bearer undefined`，请求 401 | 工具在，但一调就失败；启动正常 `[SRC-TARGET]` |
| **装不进 roster** | 包在 `dependencies`，但 `dsh.profile.bundles` 没有它 | 什么都不发生，**退出码 0**（见本册 `TRAPS` §1） |
| **起了不生效** | 行加载了，但 `dsh-mcp-client` 连不上 | 只有日志；工具不注册 `[SRC-TARGET]` |

## 3. 设计取舍：**安装器没随包发布**

这是本卡最重要的一处，也是 fanout 的 README 判断修正后的结果。

- `package.json:37` 的 `files` 是：`cordis.patch.yml`、`lib/`、`skills/`、`locale/`、`icon.png`、`README.md`、`LICENSE`、`.env.example`、`README.zh.md` `[SRC-TARGET]`。
- **`scripts/` 不在其中**；tarball 解包后只有 32 个文件，`find . -name '*install-bundle*'` 为空 `[SRC-TARGET]`。
- 而 `package.json:63-67` 的五条命令全部指向 `scripts/*.js` `[SRC-TARGET]`。

**结论**：对从 **npm** 安装的人，`npm run install:bundle` 等五条命令会直接找不到文件；对**从仓库克隆**的人，一切正常。作者的自证工具只在自己机器上成立——这正是"装后自证"最容易翻车的地方。

**已实测（E20）**：在隔离 profile 里装完后执行同一条命令，得到 `Error: Cannot find module '…/@wenaixi/cfbridge/scripts/install-bundle.js'` `[RUN]`。安装本身 exit 0、roster 也写对了——**失败只发生在真正要用的时候**。

## 4. 与宿主既有行的边界

patch 顶部有一句自我约束：**不在 patch 里重复声明 `persona` / `agent-instructions` / `tool-fs` / `skill-filesystem` / `tool-skill` / `planning` 这些宿主已提供的 agent 栈行** `[DOC]`（`cordis.patch.yml:9-12`）。

这条值得单列，因为它是 bundle 作者最常见的越界：**"我也想要这些行"和"这些行已经在了"是两件事**，重复插入会得到重复注册或覆盖宿主默认值，而这两者的失败都很安静。

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 装完无法证明装上了 | 把安装拆成 add → validate → dump-config → repair → uninstall 五条**可单独重跑**的命令，而不是一条黑箱 | `[SRC-TARGET]` `package.json:63-67` 五个 scripts 各指一个 `scripts/*.js` | 每步可单独重跑、失败点可定位；代价是要维护五个脚本并保证它们随包发布 | 定义四件套语义（装/验/卸/修），并把 scripts 目录写进 `files` | 只对能执行 npm scripts 的安装者成立 | `files` 漏 `scripts/` → 五条命令全部 404（本卡实测） |
| 缺凭据不能拖垮启动 | 把"启动容错"写成 **patch 里的行配置**（`failOnStartupError: false` + 退避重连），不写进代码分支 | `[SRC-TARGET]` `cordis.patch.yml:25`（`failOnStartupError`）、`:26-31`（`reconnect`） | 用户可以按行覆盖；代价是容错策略对每个 MCP 行都要重复声明 | 给出每个外部依赖行的容错字段与默认值 | 只对"宿主支持按行配置"的接缝成立 | 写死在代码里 → 用户想收紧或放宽都得改包 |
| 凭据要进版本库又不想泄露 | patch 里只放 `!!js` 表达式读环境变量，真实值留在被忽略的 `.dsh/.env` | `[SRC-TARGET]` `cordis.patch.yml:23`；`[DOC]` `:11-12` 的说明 | 同一份 patch 可共享；代价是排错时看不见值，只能看"求值后是否为 undefined" | 规定表达式只读环境、不读文件；给出 `.env` 的忽略规则 | 表达式的求值时机在启动期，环境必须先就绪 | 把 token 写进 patch → 一旦提交就永久泄露 |
| 与宿主的 agent 栈抢行 | 只在 patch 里声明**宿主没有的**行，宿主已有的（人格、指令、技能文件系统）一律复用 | `[DOC]` `cordis.patch.yml:9-12` 的注释约定 | 避免重复注册与覆盖默认；代价是作者必须知道宿主到底提供了什么 | 列出"宿主已有行"白名单，patch 只写增量 | 只对同一宿主版本成立，升级要重核 | 重复插入 → 静默覆盖宿主默认值 |

## 6. 失效与开放问题

- `[OPEN]` `validate:bundle` 具体校验什么（tarball 里没有该脚本，本卡无法核）。复核动作：从仓库源码读 `scripts/validate-bundle.js`，记录它校验 roster 还是 patch 可解析性。
- `[OPEN]` `repair:config` 对损坏 YAML 的处理（README 提过 `.bak` 抢救 `[DOC]`，未在源码中核）。
- `[OPEN]` 在 Desktop 面是否同样适用（本机无 Electron 应用）。

## 7. 兼看

- 起：`failOnStartupError` 与 [`BOOT`](../boot/README.md) §1 的"三级失败"是同一件事的两端。
- 坑：`files` 漏发脚本已进 [`TRAPS`](../practice/TRAPS.md)。
