---
title: "装完还要一步 · context-guardian：setup 默认不写"
domain: lifecycle
kind: sample
positioning: "安装与生效之间隔一条命令的样本：setup 默认 dry-run、--apply 才落盘，并用三条命令做会话内验收。"
takeaway: "把“生效”做成一条显式命令、且默认不写，是防止用户被静默改配置的最省力办法。"
read_when: "装完还需要额外一步才生效；或要让用户先看后写。"
status: observed
updated: 2026-11-01
budget: 135
---
# 装完还要一步 · context-guardian

> **阶段**：起 · **载体**：own-cli（`npm run setup` → `node setup.mjs`）+ command（三条） · **兼看**：配
> **影响力**：npm 近 30 天 **2,863**（2026-11-01，42 个过影响力门的 bundle 之一）
> **研究范围**：`dsh-context-guardian@0.3.0-beta.1`，gitHead `bfdfda22…`，tarball sha256 `8045814f…`（266,648 B，35 文件）；DSH 对照 `0.2.1-rc.3`
> **证据成熟度**：源码级（setup 参数、三条命令注册实读；未实机 setup）
> **一句话**：装上不等于生效——它把生效做成一条命令，**而这条命令默认什么都不写**。
> **借鉴价值**：**① 生效步骤显式化且默认 dry-run；② 用会话内命令做验收面；③ `input` 缺失会把带参命令发给模型（本包独立复现）。**

## 它想干什么 · 为什么值得借鉴

**意图。** 管上下文压力：压缩时机、回忆（recall）、成本估算，并把引擎行写进 agent preset `[SRC-TARGET]`（`setup.mjs` 的写入逻辑 + `engine.js` 三条命令）。

**意义。** 生命周期里最容易被忽略的一段是**"装了但还没生效"**。这个包把它显式化：`npm run setup` 是必须的一步，**默认 dry-run**，加 `--apply` 才写 `[SRC-TARGET]`（`setup.mjs:363`、`:610`）。

**用户价值。** 装之前，用户不知道"这条 bundle 到底改了我 preset 的哪一行"；装之后，先跑一次看清单，确认了再 `--apply`。代价是**多一步操作**——不做就没效果，而且不会报错。

**表达。** dry-run 的收尾文案直白 `[SRC-TARGET]`（`:610`）：

> `dry run -- nothing written; re-run with --apply`

## 1. 阶段与载体

- **阶段**：起。它管"装完之后怎么算生效"。
- **载体**：`own-cli`（npm script，非 `bin`）+ `command`（`recall` / `guardian` / `context` 三条）。
- **兼看**：配。`--apply` 写的是 preset 行。

## 2. 机制

### 默认不写

```js
// setup.mjs:363
if (arg === '--apply') { flags.apply = true; continue }
// setup.mjs:610
say('dry run -- nothing written; re-run with --apply')
```

**默认是"只报告"**：想看就先看，写是显式动作。

### 三条会话内命令

```js
// engine.js:1362-1392 —— ctx.inject(['commands'], …) 内注册
commands.register({ name: 'recall',  input: { hint: '<3-7 | result 3 | checkpoint 1 | find text | digest>' }, … })
commands.register({ name: 'guardian', description: 'Context Guardian status: engine, window, pressure, last compaction, goal, memory, spans', … })
commands.register({ name: 'context', description: 'Context pressure, cache hits and what compacting now would cost', … })
```

`guardian` 与 `context` **不带 `input`**（它们不接受参数，这是正确的用法）；`recall` 带 `input`，并且注释写明了原因 `[DOC]`（`engine.js:1366-1367`）：

> Without `input` DSH treats a command as argument-free: the web UI runs it bare on select and sends "/recall result 42" typed in full to the MODEL (seen live 2026-09-20).

**这是本册第二次遇到同一个坑**（第一次是 [`first-run/42`](../first-run/42_命令即验收面-dsh-tool-guardian.md)），而且这次带了实机观察日期。

### 三条失败态

| 态 | 表现 | 用户看到什么 |
|---|---|---|
| **只装不 setup** | 引擎行没写进 preset | 功能"半生效"，命令可能已有但没数据 |
| **以为 dry-run 已经写了** | 没加 `--apply` | 清单打印完就结束，什么也没变 |
| **命令没写 `input`** | 带参命令被发给模型 | 用户以为命令坏了，其实是路由问题 |

## 3. 设计取舍

| 取舍 | 选择 | 代价 |
|---|---|---|
| 生效方式 | 显式一步，不自动改 preset | 用户可能跳过，且不报错 |
| 默认行为 | dry-run | 多一条命令要跑 |
| 验收面 | 三条会话内命令 | 命令名要记 |
| 命令参数 | `input.hint` 必填（带参者） | 少一个字段就换路由 |

## 4. 与宿主既有行的边界

它**改 agent preset 的行**，不改 bundle 的 patch。这意味着生效结果不在 `--dump-config` 里，而在 preset 文档里——**两种"配置"存在两个地方**，排查时要分开看 `[OPEN]`。

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 装完还不能用，要用户做一步 | 把这步做成**显式命令**，且**默认 dry-run**，写入要 `--apply` | `[SRC-TARGET]` `setup.mjs:363`（flag）、`:610`（dry-run 文案） | 用户先看后写；代价是可能被跳过 | 定义"生效"的确切含义与写入目标 | 只对"生效=改配置"的产品成立 | 自动写 → 用户不知道自己被改了什么；或只写不报告 → 出了问题查不到 |
| 装完怎么确认在跑 | 会话内命令做验收面：状态、成本、回忆各一条 | `[SRC-TARGET]` `engine.js:1362-1392` | 零界面成本；代价是命令名与语义要设计好 | 每条命令给一句话描述与是否带参 | 只对"活在会话里"的产品成立 | 不给命令 → 用户只能看日志 |
| 带参命令行为诡异 | 带参命令必须写 `input.hint`；不写会被当成无参命令发给模型 | `[SRC-TARGET]` `engine.js:1366-1367`（注释含实机观察 2026-09-20）；互证 [`first-run/42`](../first-run/42_命令即验收面-dsh-tool-guardian.md) | 参数被当命令处理；代价是多一个字段 | 把"是否带参"当成命令注册的必填项 | 只对"命令与提问分流"的宿主成立 | 不写 → 用户以为命令坏了 |
| 生效结果放在哪 | 明确它写的是 preset 行而非 bundle patch，两者要分别排查 | `[SRC-TARGET]` setup 写入目标；对比 [`boot/README.md`](./README.md) §1 的 profile 结构 | 排查路径清晰；代价是用户要知道两套配置 | 在文档里写清"生效改了哪个文件" | 只对"改的是宿主另一层"的产品成立 | 混为一谈 → 用户改 patch 没效果，以为插件坏了 |

## 6. 失效与开放问题

- `[OPEN]` `setup.mjs` 写入 preset 的确切位置与幂等性（未逐行读）。
- `[OPEN]` `npm run setup` 依赖 npm scripts——**只在源码/仓库安装时可用**；从 npm 包安装的用户是否有等价入口，本卡未确认。
- `[OPEN]` 三条命令在无数据时的表现。
- `[OPEN]` 未实机 setup。

## 7. 兼看

- 首启：与 [`first-run/42`](../first-run/42_命令即验收面-dsh-tool-guardian.md) 共享 `input` 那条坑，互为独立复现。
- 配：`--apply` 写 preset，属于 [`config/README.md`](../config/README.md) §1 的"profile 用户层"。
