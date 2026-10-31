---
title: "BACKLOG · 候选池（待深挖 / 快筛不过）"
domain: reshape-product
kind: index
positioning: "候选池：快筛过了门槛但还没深挖的，和没过门槛的，都记在这里，不占卡位。"
read_when: "要补新样本、或想知道某个产品为什么还没成卡。"
status: living
updated: 2026-10-31
budget: 60
---
# BACKLOG · 候选池

> **规则**：候选先过 [`00-map` §11.1](./00-map.md) 的 10 分钟快筛；**不过就不立卡，只在这里留一行**。
> 每行至少写清：类型（plugin / profile / shell）、硬指标（带日期）、**为什么还没成卡**、下次复核的条件。
> 候选池**不参与**篇数统计，也不进 catalog 的"全量文件"以外的地方。

## 1. 过了门槛、待深挖

| 候选 | URL | 类型 | 硬指标（2026-10-31） | 待办 / 风险 |
|---|---|---|---|---|
| `hust-open-atom-club/oh-dsh` | <https://github.com/hust-open-atom-club/oh-dsh> | shell | ★ 323 · forks 34 · issues 40 | 自带 Node + 安装包的三端发行版；要挖"分层安装"与 DSH Desktop 的差异，再判是否成卡 |
| `shaobeichen/dsh-pocket` | <https://github.com/shaobeichen/dsh-pocket> | plugin | ★ 2,601 · npm 月 18,308 | 远程/扫码同屏，与 `dsh-mobile` 同类；先判"是否需要第二张多端卡" |
| `magian1127/deepseek-harness-zh_pro` | <https://github.com/magian1127/deepseek-harness-zh_pro> | plugin | ★ 36 · npm 月 5,580 | "综合增强"是否算产品化有争议（改默认语言/提示词，但仍是单插件）；先看它有没有自己的分发/首启 |
| `xiajiajun516/dsh-config-manager` | <https://github.com/xiajiajun516/dsh-config-manager> | plugin | ★ 277 · npm 月 19,723 | 配置备份/导出/导入/迁移 + 多变体 profile；与"首启/环境码"相邻，**已达门槛，优先立卡**（待判类别 4 还是 5） |

## 2. 观察样本（未过门槛，机制独特）

| 候选 | URL | 类型 | 硬指标（2026-10-31） | 为什么留着 |
|---|---|---|---|---|
| `why-sir/dsh-bootstrap` | <https://github.com/why-sir/dsh-bootstrap> | plugin | ★ 1 · npm 月 763 · 仓库 14 天 | 唯一"首启推荐 + 计划 + 环境码"样本；分析见 [`plugin/_证据/04_首启观察`](./plugin/_证据/04_首启观察-dsh-bootstrap.md)，**未过门槛，不立卡** |
| `sjh9714/dsh-movein` | <https://github.com/sjh9714/dsh-movein> | plugin | ★ 17 · npm 月 1,251 | 把 Claude Code 配置迁入 DSH（dry-run + 冲突保护）；接近门槛，先观察 |

## 3. 没过门槛（留档，避免重复搜）

| 候选 | URL | 类型 | 硬指标（2026-10-31） | 未过原因 |
|---|---|---|---|---|
| `Fayelin12/dsh-office` | <https://github.com/Fayelin12/dsh-office> | plugin | ★ 7 · 无 npm 计量 | 单面板，硬指标与产品形态都不够 |
| `whyihaveyou/dsh-suite` | <https://github.com/whyihaveyou/dsh-suite> | plugin | ★ 64 · `@dsh-suite/all` 月 141 | 产品是"目录 + 商店"，聚合包下载极低；没有统一产品形态 |
| `Yurzi/dsh-tool-web-enhanced` | <https://github.com/Yurzi/dsh-tool-web-enhanced> | plugin | 待采 | 组合包只换 search/fetch 后端，属能力增强 |

## 4. 复核节奏

- 每次补新卡时，顺手把本表**已过门槛**的候选重新看一眼（星标/下载有没有变化、有没有新版本）；
- 候选成卡后，从本表**删行**，在卡片 `样本档案` 里写清"从候选池转正"的日期；
- 连续 6 个月无变化的"未过门槛"行可以删掉，保持表短。
