---
title: "RESEARCH · 怎么找、怎么分类、怎么挖（规程）"
domain: lifecycle
kind: guide
positioning: "本册唯一研究规程：影响力漏斗、三轴分类、S1–S5 流水线、七列质量门与结论归属。"
read_when: "要新增一张样本卡；或复核别人的挖掘是否达标。"
status: living
updated: 2026-11-01
budget: 160
---
# 研究规程

> 规则源仍是 [`00-map`](../00-map.md)。本文件只回答"**怎么做**"，不重复定义口径。

## 1. 找：影响力优先的三层漏斗

| 层 | 手段 | 规模 | 产出 | 纪律 |
|---|---|---|---|---|
| L1 分母 | `bundle_sweep`（`dsh-bundle` 关键词扫出的 bundle，带下载量） | 322 | 候选总体 | **不用关键词描述当分类** |
| L2 影响力门 | ★ ≥ 200 或 npm 近 30 天 ≥ 2,000 | 30（bundle 扫描）+ 12（关键词普查）= 42（去重后） | 待分诊名单 | 数字带日期；快照只作历史对照 |
| L3 分诊 | 读 registry 清单 + README，判定阶段/载体/深度 | 42 → 15 | `[PKG]` + `[DOC]` 结论 | README 只能让人进入下一层 |
| L4 取证 | 抽 tarball，grep 符号表 | 15 | `[SRC-TARGET]` 文件:行号 | **没有这一层，不许成卡** |

**为什么不用"关键词召回"当分母**：`onboarding_census` 撞过这个坑——671 个命中，大半是"零配置""开箱即用"这类营销词。关键词只配做召回，不配做分类。

## 2. 分类：三轴，只有 A 进文件名

| 轴 | 取值 | 落点 |
|---|---|---|
| **A 阶段** | 装 / 起 / 配 / 首启 / 反例 | **子目录**：`{install,boot,config,first-run,negative}/` |
| **B 载体** | 9 类，见 [`CARRIERS`](../reference/CARRIERS.md) | 卡内一行 + 矩阵一格 |
| **C 机制主题** | 通道与坑 · 装后自证 · 首启引导与可推迟 · 凭据与连接 · 默认值与分层 · 生效边界 · 迁移与导入 · 自愈与回滚 · 工作区·会话预置 | `BACKLOG` 分组、选题 |

**分类即目录**：阶段只由子目录表达，文件名不再重复编码十位；载体与主题写进卡内，不参与路径。

## 3. 挖：每样本五步

| 步 | 动作 | 判据 |
|---|---|---|
| **S1 钉版本** | `npm view <pkg> dist-tags version gitHead dist.tarball`；有 tag 则对 commit | memo 页头写"固定版本" |
| **S2 抽包** | 下载 tarball → **记录 sha256** → 解包 → 数文件 | memo 写 tarball 摘要 |
| **S3 符号取证** | 按载体符号表 grep，**只记命中** | 每条 `[SRC-TARGET]` 都带文件:行号 |
| **S4 机制还原** | 读命中文件 → 走状态机 → README 主张逐条对源码 | 产出**矛盾清单**（README 说 A、源码做 B） |
| **S5 成卡** | 卡 + memo + `catalog` + 矩阵 + `verify` | 过 §5 的四条硬检 |

**S3 的符号表**：`tapIndex` · `index-inject` · `webServer.register` · `commands.register` · `agents.create` · `workspaceRegistry` · `workingDirectory` · `installBundle` · `failOnStartupError` · `!!js` · `disabled:`。

## 4. 谁写结论

**子代理只交原始证据**：命令原文、文件:行号、代码片段。**不交结论。**

理由：上一轮 fanout 里已经有 evidence 被改写过的（把 registry 字段描述成一句话）。那样的东西进卡就是污染。

**主代理做 S4/S5**：机制还原、七列表、失效条件、矛盾清单。

## 5. 质量门（四条硬检 + 三条结构门）

| # | 硬检 |
|---|---|
| 1 | `## 5. 可迁移洞察` 七列表 ≥ 3 行，表头逐字照抄产品册 |
| 2 | 每条 `[SRC-TARGET]` 能 `sed -n 'Np'` 出来 |
| 3 | 失效与开放问题非空，且每条 `[OPEN]` 带可执行的复核动作 |
| 4 | `_证据/NN_源码复核.md` 存在，且页头写固定版本与 tarball 摘要 |
| 5 | （结构）样本卡的 `## 它想干什么 · 为什么值得借鉴` 四段齐 |
| 6 | （结构）`verify.mjs` 通过 |
| 7 | （结构）样本卡有 `DSH 立场` 行，且取值 ∈ 符合 / 有条件偏离 / 反例 |

**七列逐字照抄产品册**：触发问题 · 可迁移洞察 · 机制依据 · `为什么有效 / 代价`（一列，表头内含斜杠）· 移植时改什么 · 成立边界 · 抄错后果。照抄的代价是"载体"没有专属列，写进"机制依据"与"移植时改什么"。

## 6. 证据词表（样本卡、memo 与横切篇共用）

| 标签 | 含义 |
|---|---|
| `[PKG]` | 包清单事实：包名 + 版本 + 字段 |
| `[DOC]` | README/文档主张 |
| `[SRC-TARGET]` | 第三方源码：文件:行号 |
| `[DSH]` | 上游 DSH：包 + 文件:行号 |
| `[RUN]` | 本轮隔离实测 |
| `[OPEN]` | 未复核 + 复核动作 |

**`[DOC]` 不许冒充 `[SRC-TARGET]`。** 两者矛盾时，两条都写，矛盾本身进七列表。

## 7. 排期

| 批 | 卡 | 状态 |
|---|---|---|
| 1 | `cfbridge` · `origin-plugin` · `rhine-splash` · `update-checker` | 已成卡 |
| 2 | `isolation-gate` · `free-search` · `tool-guardian` · `skill-cockpit` | 已成卡 |
| 3 | `free-models-hub` · `noema` · `dsh-doctor` · `24pa` | 已成卡 |
| 4 | `tinyfish` · `dfy-bundle` | 已成卡 |
| 补 | `context-guardian` | 已成卡 |

**批 1 先跑通流水线**（当时的纪律）：如果 4 张里有一张挖不出 `[SRC-TARGET]`，先改流水线，不要硬写。`sage-mem` 仍在 `BACKLOG` 待办，状态以该文件为准。
