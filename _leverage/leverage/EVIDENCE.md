---
title: "证据规程：本册的版本、分源与升级门"
domain: layer
kind: guide
positioning: "本册 29 篇的证据规程（原 46 篇，协作域 2026-11-01 迁出）：分源标签、机制卡/playbook 的证据节与固定版本要求。"
read_when: "要新增/修订本册样本或机制卡；或质疑某条断言有没有来源时。"
status: living
updated: 2026-11-01
---

# 证据规程（本册）

> **2026-11-01 迁移说明**：协作域已迁至 [`../leverage-agent-collaboration/`](../leverage-agent-collaboration/README.md)，并使用其自己的 `EVIDENCE.md`。本文件只覆盖 PROVE/DRAW 与父册骨架。

产品册 [`../leverage-reshape-product/RESEARCH.md`](../leverage-reshape-product/RESEARCH.md) 的规则在这里适用，但本册的分析单位不同：**样本卡**（一样本一篇）与**机制卡**（一个门禁/控制点一篇）。所以证据门分两类，不混用。

## 1. 分源标签

| 标签 | 含义 | 允许用它证明什么 |
|---|---|---|
| `[DOC]` | 目标仓库 README/docs/CHANGELOG 的主张 | 作者声称什么；**不**证明实现如此 |
| `[SRC-TARGET]` | 目标仓库固定 commit 的实现 | 该版本代码怎么走；不证明发布物字节一致 |
| `[SRC-DSH]` | 本机 DSH `0.2.1-rc.3` 发行包 | 宿主契约/默认值；不证明其它宿主版本 |
| `[TEST]` | 目标仓库测试源码 | 覆盖意图；**不**证明测试通过 |
| `[CI]` | workflow/check-run | 同 SHA 的 CI 结果才算；workflow 存在不算 |
| `[RUN]` | 本轮实际执行 | 只能写做过的事；未跑就写 `[RUN] None` |
| `[OBS]` | 作者观察/经验判断 | 只能作假设，不能写成宿主事实 |

**铁律**：`[DOC]` 不能升级成 `[SRC-TARGET]`；上游行为不能当成目标行为；未验证一律 `[OPEN]`，不写“已验证”。

## 2. 样本卡（0 张，已随协作域迁出）

本册不再驻留样本卡；原 14 张协作样本连同 memo 已迁至 [`../leverage-agent-collaboration/`](../leverage-agent-collaboration/README.md)，其迁移后的样本规程（固定坐标、同家族 memo、主张改写、保留失效）见 [`../leverage-agent-collaboration/EVIDENCE.md`](../leverage-agent-collaboration/EVIDENCE.md) §2。本册只保留机制卡与 playbook 的证据要求（§3）。

## 3. 机制卡与 playbook（15 卡 + 4 篇横向）

每章必须新增 **`## 证据与边界`** 一节，至少 3 行，格式：

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|

要求：
- 涉及宿主 seam/默认值/事件名的，优先 `[SRC-DSH]` 并给包名+文件+行号；
- 涉及样本实现的，`[SRC-TARGET]` + memo 链接或固定版本；
- 纯推论/经验写 `[OBS]`，并写可证伪条件；
- 无源数字（百分比、次数、体积）要么补来源与日期，要么删除或改成定性表述。

## 4. 索引与门禁

- 机制卡/playbook 的索引在 [`catalog.md`](./catalog.md)，一行一篇，与目录双向一致；
- 顶层 `README`/`00-map`/`catalog`/`BORROW` 的计数以 `verify.mjs` 为准，不手写猜测；
- `verify.mjs` 将强制：机制卡/playbook 含 `## 证据与边界` 且 ≥3 行、catalog 一行不多一行不少（四册同款）；
- 样本 memo 的门禁由协作册承担；负向测试：故意删章节证据节、删 catalog 行，校验必须报错。

## 5. 研究顺序

1. ~~14 张协作样本~~（2026-11-01 迁出，由协作册接管）；
2. prove-output 10 章（门禁链/硬地板/对账/回执…）——已完成；
3. draw-limit 9 章（信任层/审批预算/第二模型/注入缝…）——已完成；
4. 顶层索引、BORROW 与 catalog 收口——本轮完成；
5. 之后只做回源复核：数字过期、链接失效、结论被推翻时按 §3 改。

每批完成后跑 `node _leverage/verify.mjs`，并把本批结论写回对应 memo/章节，不攒到最后。
