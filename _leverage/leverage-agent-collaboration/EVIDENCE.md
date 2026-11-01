---
title: "证据规程：Agent 协作册"
domain: agent-collab
kind: guide
positioning: "本册证据规程：四家族样本必须有固定版本 memo 并链接；机制卡必须有“证据与边界”；与产品册 RESEARCH 同级。"
read_when: "要新增/修订本册样本或机制卡；或质疑某条断言有没有来源时。"
status: living
updated: 2026-11-01
---

# 证据规程（本册）

产品册 [`../leverage-reshape-product/RESEARCH.md`](../leverage-reshape-product/RESEARCH.md) 的规则在这里适用；本册的分析单位是**样本卡**（一样本一篇，按主家族归位）与**机制卡**（一个协作机制一篇）。

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

## 2. 样本卡（按家族归位，14 张起）

每张 `lever-cross-boundary/samples/NN-*.md` 必须：

1. **固定坐标**：repo、npm 包、精确版本、tag/commit（或说明为何无法对齐），最近核对日期；
2. **链接 memo**：同家族 `_证据/NN-<slug>-源码复核.md`，并在卡头写“证据链”一行；
3. **改写主张**：卡的每条机制断言要么有 memo 里的 `[SRC-TARGET]` 行号，要么降级为 `[DOC]`/`[OBS]`；
4. **保留代价与失效**：无法验证的运行行为标 `[OPEN]`，不删。

memo 最少包含：Provenance（npm↔tag↔commit 对齐/不对齐）、DOC 主张、SRC-TARGET 机制核对、与卡片的偏差表、TEST/CI/RUN、`[OPEN]`。

## 3. 机制卡（四家族 + 横向卷）

每章必须新增 **`## 证据与边界`** 一节，至少 3 行，格式：

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|

要求：
- 涉及宿主 seam/默认值/事件名的，优先 `[SRC-DSH]` 并给包名+文件+行号；
- 涉及样本实现的，`[SRC-TARGET]` + memo 链接或固定版本；
- 纯推论/经验写 `[OBS]`，并写可证伪条件；
- 无源数字（百分比、次数、体积）要么补来源与日期，要么删除或改成定性表述。

## 4. 索引与门禁

- 样本索引 `03-sample-encyclopedia.md` 的每行必须能点到样本卡与 memo；
- 顶层 `README`/`00-map`/`catalog`/`BORROW` 的计数以 `verify.mjs` 为准，不手写猜测；
- `verify.mjs` 将强制：样本 memo 存在且被卡链接、章节含 `## 证据与边界` 且 ≥3 行、catalog 一行不多一行不少；
- 负向测试：故意删 memo、删章节证据节、改坏表格列数，校验必须报错。

## 5. 研究顺序

1. 四家族骨架与迁移（delegation/teams/pipelines/crossing/coordination）；
2. delegation 宿主契约与委派样本；
3. pipelines 声明式编排与重放；
4. crossing 远端执行与跨实例；
5. teams 现有样本与新增对照；
6. coordination 横向对照与选型矩阵。

每批完成后跑 `node _leverage/verify.mjs`，并把本批结论写回对应 memo/章节，不攒到最后。
