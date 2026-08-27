# Coverage · 覆盖矩阵

维护用索引：按源码组追踪消化覆盖状态。**未列出的源码文件不隐含任何覆盖承诺。**

状态含义：

- **骨架** — 只有 `00-map.md` 划了范围,无编号正文
- **进行中** — 有部分编号正文
- **已核验** — 结论核对过当前基线源码;「核验 commit」记录最后一次核对点

## 按专题

| 专题 | 状态 | 已有正文 | 最近核验 commit |
|------|------|----------|-----------------|
| [`system`](../system/00-map.md) | 骨架 | 仅 map | — |
| [`registry-data`](../registry-data/00-map.md) | 骨架 | 仅 map | — |
| [`readme-pipeline`](../readme-pipeline/00-map.md) | 骨架 | 仅 map | — |
| [`site-surface`](../site-surface/00-map.md) | 骨架 | 仅 map | — |
| [`submission-gates`](../submission-gates/00-map.md) | 骨架 | 仅 map | — |
| [`probes-and-decay`](../probes-and-decay/00-map.md) | 骨架 | 仅 map | — |

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
