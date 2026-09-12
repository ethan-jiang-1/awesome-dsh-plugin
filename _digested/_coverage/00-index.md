# Coverage · 覆盖矩阵

维护用索引：按源码组追踪消化覆盖状态。**未列出的源码文件不隐含任何覆盖承诺。**

状态含义：

- **骨架** — 只有 `00-map.md` 划了范围,无编号正文
- **进行中** — 有部分编号正文
- **已核验** — 结论核对过当前基线源码;「核验 commit」记录最后一次核对点

## 按专题

六个机制专题是**评估视角的辅助档案**,统一收纳在 [`mechanics/`](../mechanics/00-map.md)(其 [00-map](../mechanics/00-map.md) 是浓缩入口);ecosystem 是主轴。

| 专题 | 状态 | 已有正文 | 最近核验 commit |
|------|------|----------|-----------------|
| [`ecosystem`](../ecosystem/00-map.md) | **已核验**(0001:头条/23 类分布/标签表/演化曲线/盲区全部重算;新增 04 趋势、05→_method 方法档案) | 00-map · 01-scenario-taxonomy · 02-tech-landscape · 03-growth-maturity · 04-value-trend(+ _method/01) | `38976afd` |
| [`mechanics/system`](../mechanics/system/00-map.md) | **已核验**(0001:生命周期图并入五处机制变更,规模事实刷新) | 仅 map | `38976afd` |
| [`mechanics/registry-data`](../mechanics/registry-data/00-map.md) | **已核验**(0001:wsl 23 类、schema 白名单未变、3552 条、CRLF 11 个;行号刷新) | 仅 map | `38976afd` |
| [`mechanics/readme-pipeline`](../mechanics/readme-pipeline/00-map.md) | **已核验**(0001:yml-only 投稿 + sync-readme bot 重生成 + --check 语义收窄 + CRLF 归一化,已并入两篇) | 00-map · 01-generate-readme | `38976afd` |
| [`mechanics/site-surface`](../mechanics/site-surface/00-map.md) | **已核验**(0001:AdSense/Giscus/并发组拆分/1098 行/7160 页/隐私页重写已并入三篇) | 01-build-site · 02-templates-locales | `38976afd` |
| [`mechanics/submission-gates`](../mechanics/submission-gates/00-map.md) | 需复核(0001:四道门禁实质 diff、commit floor 删除、held-rescan 新增;复核中) | 01 · 02 · 03 | `5e7dc7eb` |
| [`mechanics/probes-and-decay`](../mechanics/probes-and-decay/00-map.md) | **已核验**(0001:仅 probe-npm +150 行/version 字段/新鲜度分层;九探针口径不变;六处修正已并入) | 01 · 02 · 03 | `38976afd` |

> 核验方式说明:`mechanics/submission-gates`、`system`、`registry-data`、`readme-pipeline` 由主笔逐行精读;`site-surface`、`probes-and-decay` 两专题由并行子代理逐行精读后主笔蒸馏,未做全文二次抽查——引用前如需强保证,按文中行号回源核对。`ecosystem` 的数字均可由 `_digested/ecosystem/census.py`(标准库,无第三方依赖)重跑复现;技术标签为描述正则判定,精度边界见其 02 文末方法注记。

## 按源码组(粗粒度)

| 源码组 | 归入专题 |
|--------|----------|
| `data/plugins/*.yaml`(≈2288 个) + `lib/entries.mjs` | registry-data |
| `data/*.json` 四个边车 | registry-data / probes-and-decay(写入方) |
| `scripts/generate-readme.mjs` | readme-pipeline |
| `scripts/build-site.mjs`、`site/*` | site-surface |
| `.github/workflows/pr-*.yml`、`regate.yml`、`check-submission`、`check-bleed` | submission-gates |
| `.github/workflows/build-site.yml`、`decay-scan.yml` | 分别归 site-surface / probes-and-decay 的调度视角 |
| `scripts/probe-*.mjs`、`scan-decay.mjs`、`publish-*.mjs` | probes-and-decay |
| `scripts/migrate-to-yaml.mjs`、`reorder-categories.py`、`prune-legacy-screenshots.mjs`、`maint-rebase.sh` | 历史/迁移工具,暂不单开专题,分别挂在相关专题下 |
| `contributing.md`、PR/Issue 模板 | submission-gates |

上游合入后,把受影响的专题标为「需复核」再逐个降回；流程见 [`_change_log/`](../_change_log/00-index.md)。
