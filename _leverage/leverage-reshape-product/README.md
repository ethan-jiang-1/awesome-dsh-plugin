---
title: "leverage-reshape-product · 产品线：从插件到 profile 到独立壳"
domain: reshape-product
kind: index
positioning: "产品线入口：三条路线怎么分工、怎么读、影响力门槛是什么。"
read_when: "要判断一个产品该发插件、发 profile 还是发应用；或第一次进产品线。"
status: living
updated: 2026-10-31
budget: 220
---
# `leverage-reshape-product/` · 产品线(另册)

> **标语**:*From a plugin to a profile to an app.* —— 产品的单位，从插件到 profile 到应用。
> **和 `leverage/` 平级**：`leverage/` 回答"对上游的杠杆有多大"（协作 / 质量 / 安全三域）；本目录只回答"**怎么把 DSH 装成产品**"。
> **规模**：三个 lever，**21 张样本卡** + 1 个门 + 7 份原始证据 + 1 份指标快照（另有 1 个观察样本，不占卡位）。
> **状态**：`living`（随样本增长） · 基线 DSH `0.2.1-rc.3` · 名单 @ `efe602e7b` · **指标 2026-10-31 重采**（快照见 [`_证据/指标快照-2026-10-31.json`](./_证据/指标快照-2026-10-31.json)）

## 0. 三个入口

| 你要什么 | 去哪 | 你会拿到 |
|---|---|---|
| **拿走东西**（做插件 / 发行版 / 独立应用） | [BORROW](./BORROW.md) | 按需求路由 + 18 条公共产出 + 三条"别抄" |
| **查某一篇** | [catalog](./catalog.md) | 全部文件的 kind / 定位 / 能拿走什么 / 什么时候读 |
| **知道凭什么** | [horizon](./horizon.md) | C1–C4 口径、产品七层、13 行上游接缝 |
| **问"它为什么没卡"** | [BACKLOG](./BACKLOG.md) | 过了门槛待深挖 / 没过门槛的候选，各一行 |

**只读一次的话**：打开 [BORROW](./BORROW.md) §1 找你那一行；或直接进三个 lever 的 README。**不要从目录树开始通读。**

## 1. 为什么有这一册

`ecosystem/` 回答"有什么"，`mechanics/` 回答"上游怎么运转"，`leverage/` 回答"一个插件能撬动多深"。还剩一个没人回答的问题：**同样是不改上游，为什么有的东西只是一个插件，有的能变成一套产品？**

答案不在插件数量，在**产品的单位**：一个插件 → 一套 bundle（profile）→ 自带宿主的应用。同一份 DSH，换的是"用户从哪进来、看到什么默认值、坏了谁负责"。本册把这条递进拆成三个 lever，逐卡写清"能抄哪一行、抄错会怎样、什么时候失效"。

**不是**：插件推荐榜、功能分类、安装教程。

## 2. 读之前:四个最容易读错的地方

1. **能 `dsh plugin add` ≠ 是插件。** 终端 TUI 也能 add，但它换的是表层 → 归 `shell`。判定从"用户为了用它必须启动什么"开始（[§4](#4-三个-lever三个递进的问题)）。
2. **"能一键装齐" ≠ profile 产品。** 组合包卖的是**策展 + 固定版本 + 共享默认**；只把包堆在一起不构成产品形态。
3. **★ / npm 下载 / 目录条目是三套数。** 不同源、不可互证；引用必须带日期。仓库自带的 `data/*.json` 是 2026-08-19 冻结快照，只作历史对照。
4. **"机制例外"不是补丁。** 每 lever ≤ 2 张；例外超额度说明门槛定错了——改门槛，不要加例外。

## 3. 目录长什么样

目录里只有三种东西：

| 层 | 是什么 | 会长吗 | 约束 |
|---|---|---|---|
| **骨架** | 本文件、[00-map](./00-map.md)、[horizon](./horizon.md)、[BORROW](./BORROW.md)、[BACKLOG](./BACKLOG.md)、[catalog](./catalog.md)、三个 lever 的 README | **不随样本长** | 固定名、不编号；frontmatter `budget` 超了要删/移 |
| **叶子** | `<lever>/NN_*.md`、`_证据/` | 随便长 | 每篇 frontmatter + 借用节 |
| **文档** | [catalog](./catalog.md) | 手工补 | 加卡时补一行；数量不在这里维护 |

七种角色（frontmatter `kind`）：

| kind | 是什么 | 例子 |
|---|---|---|
| `index` | 目录/索引 | 本文件、[catalog](./catalog.md)、[BACKLOG](./BACKLOG.md) |
| `charter` | 规则页：收什么、怎么判 | [00-map](./00-map.md)、[horizon](./horizon.md)、三个 lever README |
| `guide` | 借用总入口 | [BORROW](./BORROW.md) |
| `playbook` | 横向框架/手册 | 本册暂无 |
| `card` | 一个机制/环节一篇 | 本册暂无（单域，机制写在样本卡内） |
| `sample` | 一个样本一篇 | `plugin/11_薄基座-dock.md` … `shell/91_冻结分叉-better-sidebar-N23.md` |
| `evidence` | 原始摘录/原始响应，只作溯源 | 各 lever 的 `_证据/`；跨 lever 的指标快照在 `_证据/` |

## 4. 三个 lever:三个递进的问题

| 问题 | 改到哪一层 | 交付物 | 去 |
|---|---|---|---|
| 不改宿主，只装**一个插件**，能改出什么？ | 3 层（槽位）为主 | 一个 npm 包 | [`plugin/`](./plugin/README.md) |
| 不改宿主，装**一整套 bundle**，浏览器里能长出什么产品？ | 2/3/5/6/7 层 | 一套 bundle / 一个 profile | [`profile/`](./profile/README.md) |
| **换掉表层 / 自带宿主**，DSH 能变成什么独立产品？ | 2 层起，连运行时都可能带 | 一个应用 | [`shell/`](./shell/README.md) |

**归属不是三选一，是三步**（完整协议、5 条 tie-breaker 与回归表见 [`00-map` §8](./00-map.md)）：

```text
Q1 用户为了用它，必须启动什么？
  ├─ 终端 / 桌面应用 / 自带运行时 / 安装包 ───────────→ shell
  └─ 浏览器里的 dsh web（某个 profile） ───────────→ Q2
Q2 交付的是"一块能力"，还是"一整套产品形态"？
  ├─ 一块能力（默认值/首启/分发仍归宿主） ──────────→ plugin
  └─ 一整套（自定默认体验 / 自带分发 / 聚合整套） ────→ profile
```

| 容易判错的 | 判定 | 理由 |
|---|---|---|
| `dsh-TUI` / `seektty` | shell | 能 `dsh plugin add`，但表层是终端 |
| `codex-ui` | profile | 单包，但重定义整套界面与默认值 |
| `dsh-mobile` | plugin | 加一块屏，不改宿主表层 |

## 5. 怎么读

| 我要… | 先读 |
|---|---|
| 写一个插件，不知道挂哪个接缝 | [horizon §4 接缝表](./horizon.md) → [plugin README](./plugin/README.md) |
| 把自己的东西做成"全家桶 / 发行版" | [profile README](./profile/README.md) → 四张卡挑一个形态 |
| 换表层做独立应用 | [shell README](./shell/README.md) → 先看 `desktop` profile 那条接缝 |
| 判断一个东西该发什么 | 本文件 §4 的判断顺序 |
| 抄一条现成规则 | [BORROW](./BORROW.md) 的 18 条 |
| 找某个产品/插件的坐标 | [catalog](./catalog.md) → 对应 lever 的坐标表 |
| 问"它为什么还没成卡" | [BACKLOG](./BACKLOG.md) |

## 6. 文件约定

**每一篇都有 frontmatter**，`verify.mjs` 校验九个键（`title` / `domain` / `kind` / `positioning` / `takeaway` / `read_when` / `status` / `updated` / `budget`）。这里只留三条：

1. **`domain` 固定 `reshape-product`**，与路径绑定；`kind` 为 `sample` / `card` / `playbook` 时必须有 `takeaway` + 借用节。
2. **不放会漂的数字**（星标/下载/版本/基线日期）——留在正文页头，带时点。
3. **规则只有一个源**：目录/命名/证据看 [00-map](./00-map.md)；准入/七层看 [horizon](./horizon.md)；lever README 里的副本是摘要，冲突以源为准。

**新增文件命名**：骨架用固定名，不新增编号；卡片用 `<lever>/NN_关键短语-插件名.md`，编号域内递增、不复用、不重排；退役保留编号改十位为 `9`。**老文件不改名**（外部引用与锚点稳定）。

## 7. 证据、坐标与深度

**所有卡都要有可复核的影响力证据，且带日期。** 门槛（与 [00-map §7](./00-map.md) 同一组数字，摘要）：

| lever | 硬指标（任一） | 例外 |
|---|---|---|
| `plugin` | ★ ≥ 200 或 npm 近 30 天 ≥ 2,000 | 每 lever ≤ 2 张，标"机制例外" |
| `profile` | ★ ≥ 200 或 npm 近 30 天 ≥ 3,000 | 同上 |
| `shell` | ★ ≥ 100 或 npm 近 30 天 ≥ 1,000 | 同上 |

**三种数，三种口径**：★（GitHub API，写时点）/ npm 近 30 天下载（含 CI 与镜像，≠ 用户数）/ 仓库 2026-08-19 快照（只作历史对照）。**本线 21 张卡已于 2026-10-31 统一重采**（另有 1 个观察样本），原始响应存 [`_证据/指标快照-2026-10-31.json`](./_证据/指标快照-2026-10-31.json)。

**证据深度**（卡片页头写一句）：`README 级` < `源码级` < `实测级`。只在 README 上下的结论，不写"机制已核"。

## 8. 生长协议:加的是叶子,骨架不跟着长

| 变化 | 写哪里 | 不要动 |
|---|---|---|
| 新样本过门 | 新卡 + [catalog](./catalog.md) 补一行 + lever README 卡表补一行 | 所有骨架 |
| 新样本只到候选 | [BACKLOG](./BACKLOG.md) 一行（写清缺什么 / 复核条件） | 所有骨架 |
| 现有卡掉门 / 退役 | 卡 `status` + 十位改 `9`，保留编号 | 所有骨架 |
| 某条公共规则被推翻 | [BORROW](./BORROW.md) 改一行 | 其他 |
| 新 lever 出现 | 必须满足：交付物不同 + ≥2 个过门样本 + 现有三 lever 都装不下；才加目录/README/[00-map](./00-map.md) 枚举/[catalog](./catalog.md) | 三个 lever 正文 |
| 上游同步 | 只改受影响卡的 `updated` 与 `[DSH]` 断言 | 其他 |
| 数字口径变 | 卡头数字 + [00-map §7](./00-map.md) 一行 | 其他 |

**五条不变量**：① 骨架不随样本数增长（固定名 + `budget`）；② 全量清单只维护一张（catalog）；③ 借用层按需求分、不按样本分；④ 一个样本只在一处完整论证；⑤ 卡片编号域内递增、不复用、不重排。

## 9. 校验

```sh
node _leverage/verify.mjs
```

`_leverage/verify.mjs` 是**自包含**的校验器，只读 `_leverage/` 这一棵树（不依赖 `_digested/` 的脚本或数据）：严格 UTF-8、LF、相对链接与锚点、frontmatter 契约（domain 固定 `reshape-product`）、`sample` 必须有借鉴节；另外校验本册 `catalog.md` 与本目录 Markdown 集合双向一致、三个 lever README 卡表覆盖本 lever 全部编号卡、门槛数字与 `00-map` §7 同数、卡片页头影响力过门槛（或标"机制例外"）。`leverage/` 三域由同一支校验器一并覆盖。

## 与 `leverage/` 的边界

- **独立成册**：本目录的文件不计入 `leverage/` 的三域篇数与统计，`leverage/` 的 `catalog.md` 也不再列这里的卡。
- **交叉只在结论层**：`lever-cross-boundary` 看协作插件跨的边界，`lever-prove-output` 看门禁，`lever-draw-limit` 看权限；本线只回答"**怎么把它装成一个产品**"，不重复它们的机制分析。
- **共享文件只读**：`../leverage/00-map.md`、`horizon.md`、`README.md`、`data/` 由别的会话维护，本线只调用。
