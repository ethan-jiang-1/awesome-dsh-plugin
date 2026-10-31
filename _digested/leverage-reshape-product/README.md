---
title: "leverage-reshape-product · 产品线：从插件到 profile 到独立壳"
domain: reshape-product
kind: index
positioning: "产品线入口：三条路线怎么分工、怎么读、影响力门槛是什么。"
read_when: "要判断一个产品该发插件、发 profile 还是发应用；或第一次进产品线。"
status: living
updated: 2026-10-31
budget: 115
---
# leverage-reshape-product · 产品线

> **标语**:*From a plugin to a profile to an app.* —— 产品的单位，从插件到 profile 到应用。
> **和 `leverage/` 平级**：`leverage/` 回答"对上游的杠杆有多大"（协作 / 质量 / 安全三域）；本目录只回答"**怎么把 DSH 装成产品**"。
> **规模**：三个 lever，**19 张样本卡** + 1 个共用的门 + 5 份原始证据。
> **状态**：`living`（随样本增长） · 基线 DSH `0.2.1-rc.3` · 名单 @ `efe602e7b` · 快照 2026-08-19

---

## 0. 定调：这里产出什么

**不是插件导购，是"消化后的可借鉴结论 + 回源坐标"。**

一张产品卡必须能回答四个问题，答不出就不算写完：

| 问题 | 交付物 | 答不出的后果 |
|---|---|---|
| **抄哪一行？** | 可照抄的机制（字段、算法、阈值、顺序） | 只是转述 README |
| **为什么这么设计？** | 一个可证伪的取舍（放弃什么、换来什么、谁承担代价） | "好"与"说不清为什么好"分不清 |
| **抄错会怎样？** | 一张食谱表：问题 → 照它做 → 要改的地方 → 后果 | 读者只会说"哦，挺好" |
| **什么时候失效？** | 输入/版本/规模边界 + 退化形态 | 把信仰当工程 |

**不能借鉴的样本只进对照表，不立卡**（B 级不立卡、C 级一行）。每张卡都带 `[DSH]`/`[CAT]`/`[OBS]`/`[OPEN]` 与日期，随时能回源到 repo、issue 或上游行号；找新样本的入口见 [`00_map`](./00_map.md) §11。

---

## 1. 这条线回答的三个递进问题

| 问题 | 改到哪一层 | 交付物 | 去 |
|---|---|---|---|
| 不改宿主，只装**一个插件**，能改出什么？ | 3 层（槽位）为主 | 一个 npm 包 | [`plugin/`](./plugin/README.md) |
| 不改宿主，装**一整套 bundle**，浏览器里能长出什么产品？ | 2/3/5/6/7 层 | 一套 bundle / 一个 profile | [`profile/`](./profile/README.md) |
| **换掉表层 / 自带宿主**，DSH 能变成什么独立产品？ | 2 层起，连运行时都可能带 | 一个应用 | [`shell/`](./shell/README.md) |

**判断顺序**（一句话版）：

```
能 `dsh plugin --profile <任意> add` 吗？
  ├─ 能，但只是加一块能力 ──────────────→ plugin
  ├─ 能，而且一整套（聚合/单包多内核/组合补丁）+ ≥2 项产品化，浏览器交付 → profile
  └─ 不能（全局 CLI / 安装包 / 自带运行时 / 换表层）────→ shell
```

## 2. 目录

| 文件 / 目录 | 是什么 | 什么时候读 |
|---|---|---|
| [`00_map.md`](./00_map.md) | **单一规则源**：目录、命名、frontmatter、证据、维护流程 | 新增/改名文件；或口径冲突时 |
| [`01_领域模型-七层与命名约定.md`](./01_领域模型-七层与命名约定.md) | **三个 lever 共用**的门：C1–C4 口径、产品七层、编号法、13 行上游接缝索引 | 判断改动落在第几层；抄任何卡之前 |
| [`02_公共产出-18条.md`](./02_公共产出-18条.md) | 跨 lever 的 18 条可搬走规则 | 只读一节就走 |
| [`plugin/`](./plugin/README.md) | 通用插件（9 卡） | 装配件；判断厚客人 vs 宿主 |
| [`profile/`](./profile/README.md) | profile 级产品（4 卡） | 做发行版/全家桶 |
| [`shell/`](./shell/README.md) | 自带宿主（6 卡） | 换表层做独立应用 |
| [`catalog.md`](./catalog.md) | 全量文件清单（手工维护） | 想一次看全 |

## 3. 影响力门槛（摘要，规则源见 [`00_map` §7](./00_map.md)）

**所有卡都要有可复核的影响力证据，且带日期。** 三套数不同源、不可互证：

- **★**：GitHub API，引用时写 `2026-10-31` 这样的时点；
- **npm 下载**：`api.npmjs.org/downloads/point/last-month`，含 CI 与镜像，**≠ 用户数**；
- **仓库快照**：`data/stars.json` / `downloads.json`，**2026-08-19**，只代表当时；已有样本两个月内涨了一个数量级。

**杠杆自己的门槛**：

- `plugin` / `shell`：能过本线 C1–C4（见门的 §1）；
- `profile`：额外要求 **npm 近 30 天 ≥ 3,000 或 ★ ≥ 200**——聚合包星标普遍虚低，只能用下载说话。

## 4. 公共产出在哪

- **18 条可直接搬走的规则** → [`02_公共产出-18条.md`](./02_公共产出-18条.md)（跨三个 lever，第 16 条出自 shell 侧）；
- **七层 + 规律 A**（换表层 ⇒ 自己补 5/6/7）→ [门的 §2](./01_领域模型-七层与命名约定.md)；
- **宿主侧必抄 9 条** → [shell README §4](./shell/README.md)；
- **profile 侧必抄 6 条** → [profile README §4](./profile/README.md)。

## 5. 怎么读

| 我要… | 先读 |
|---|---|
| 写一个插件，不知道挂哪个接缝 | [门的 §4 接缝表](./01_领域模型-七层与命名约定.md) → [plugin README](./plugin/README.md) |
| 把自己的东西做成"全家桶 / 发行版" | [profile README](./profile/README.md) → 四张卡挑一个形态 |
| 换表层做独立应用 | [shell README](./shell/README.md) → 先看 `desktop` profile 那条接缝 |
| 判断一个东西该发什么 | 本文件 §1 的判断顺序 |
| 找某个产品/插件的坐标 | [`catalog.md`](./catalog.md) → 对应 lever 的坐标表 |

## 6. 和 `leverage/` 的关系

- **独立成册**：本目录的文件不计入 `leverage/` 的三域篇数与统计，`leverage/` 的 `catalog.md` 也不再列这里的卡。
- **交叉只在结论层**：`lever-cross-boundary` 看协作插件跨的边界，`lever-prove-output` 看门禁，`lever-draw-limit` 看权限；本线只回答"**怎么把它装成一个产品**"，不重复它们的机制分析。
- **共享文件只读**：`../leverage/00-map.md`、`horizon.md`、`README.md`、`data/` 由别的会话维护，本线只调用。

## 7. 验证

```sh
node _digested/verify.mjs
```

`verify.mjs` 同时校验 `_digested/leverage/` 与 `_digested/leverage-reshape-product/` 两棵树：严格 UTF-8、LF、相对链接与锚点、frontmatter 契约（domain 固定 `reshape-product`）、`sample` 必须有借鉴节。
