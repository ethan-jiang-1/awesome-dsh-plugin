---
title: "历史审计基线：四域时代 46 篇"
domain: layer
kind: guide
positioning: "2026-11-01 四域时代的审计基线（46 篇、14 样本）；协作域迁出后本册 29 篇，本文件作为历史记录保留。"
read_when: "接续本册证据化工作时；或核对哪些样本/章节已升级、哪些仍是旧证据。"
status: living
updated: 2026-11-01
---
# 历史审计基线（四域时代，2026-11-01）

> **2026-11-01 迁移说明**：协作域已迁至 [`../leverage-agent-collaboration/`](../leverage-agent-collaboration/README.md)。本文件冻结为历史记录，不再更新 CROSS 行。**迁移后本册 29 篇：0 样本卡、15 张机制卡、4 篇 playbook、其余为顶层索引/宪章/指南**；下面 46 篇是拆册前的口径。

## 规模

| 类型 | 数量 | 位置 |
|---|---|---|
| 样本 | 14 | 原 `lever-cross-boundary/samples/`（已迁协作册） |
| 机制卡 | 15 | 原 `lever-cross-boundary/02`（已迁）+ `lever-prove-output/02`–`09`、`lever-draw-limit/02`–`08` |
| 横向 playbook | 6（含 1 篇 index） | 原 `lever-cross-boundary/01`（已迁）+ 本册 4 篇 playbook + `lever-prove-output/00`（index） |
| 宪章/索引/指南 | 11 | 拆册前两本册顶层 + 三域 README/百科（CROSS 已迁） + EVIDENCE/BORROW/catalog/horizon |

## 起始缺口

- 14 张样本：0 份固定版本 memo；卡内只有 1 条仓库链接，无 commit/版本对齐；`[SRC-TARGET]` 级断言与 `[DOC]/[OBS]` 未分。
- 21 篇机制卡/playbook：0 个 `## 证据与边界` 节；引用宿主 seam/默认值时无包名+行号；少量数字无可核来源。
- 顶层：`00-map` 仍写“0 份原始证据”；`catalog` 未登记 memo；`BORROW` 部分规则引用样本但没有回源。
- `verify.mjs`：只做 frontmatter/链接/预算等通用检查，尚未强制样本 memo、章节证据节。

## 分批

| 批次 | 内容 | 完成标准 |
|---|---|---|
| A | 样本 01–04 | 4 份 memo + 卡链接 + 索引行 |
| B | 样本 05–09 | 同上 |
| C | 样本 10–14 | 同上 |
| D | cross-boundary 3 篇 + prove-output 10 篇 | 每篇 `## 证据与边界` ≥3 行；数字有源或删 |
| E | draw-limit 9 篇 | 同上 |
| F | 顶层索引/BORROW/catalog/00-map | 计数与路径一致；EVIDENCE 入口可发现 |
| G | verifier 扩展 + 负向测试 | 删 memo/删证据节会报错；全目录通过 |

## 完成记录

- 2026-11-01：建立 `EVIDENCE.md` 与 `AUDIT.md`。
- 2026-11-01：**14 张样本全部完成固定版本 memo 并回写卡片**（证据链、坐标、偏差纠正）；`verify.mjs` 已加样本 memo 存在+链接门。
- 2026-11-01：**15 张机制卡 + 4 篇 playbook 全部加“证据与边界”**（拆册前口径为 6 篇，含协作侧 2 篇）；`verify.mjs` 已加章节门（≥3 行）。
- 2026-11-01：协作域迁出后，本册 catalog 补齐 `EVIDENCE.md`；`verify.mjs` 扩到四册 catalog 双向核对。**本文件到此冻结。**
