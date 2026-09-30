# Coverage · 覆盖矩阵

维护用索引：按源码组追踪消化覆盖状态。**未列出的源码文件不隐含任何覆盖承诺。**

状态含义：

- **骨架** — 只有 `00-map.md` 划了范围,无编号正文
- **进行中** — 有部分编号正文
- **已核验** — 结论核对过当前基线源码;「核验 commit」记录最后一次核对点

> **0002 复核方式**:七个专题按 0002 变更面重核。`ecosystem` 的全部数字由 [`census.py`](../ecosystem/census.py) 与 [`fresh_probe.py`](../ecosystem/fresh_probe.py) 在 `c18ba4a0d` 上现算;`submission-gates`、`site-surface`+`readme-pipeline`、`probes-and-decay` 三个变更面各由**并行子代理逐行精读 diff 后主笔蒸馏**(与 0001 相同的分工),`registry-data`、`system` 由主笔直接重核。子代理报告中标注 UNVERIFIED 的条目已原样保留在正文的「待复核」里。

## 按专题

六个机制专题是**评估视角的辅助档案**,统一收纳在 [`mechanics/`](../mechanics/00-map.md)(其 [00-map](../mechanics/00-map.md) 是浓缩入口);ecosystem 是主轴。

| 专题 | 状态 | 已有正文 | 最近核验 commit |
|------|------|----------|-----------------|
| [`ecosystem`](../ecosystem/00-map.md) | **已核验**(0002:头条/23 类分布/十一个场景带/标签表/演化曲线/漂移表/盲区全部重算;新增能力披露口径;census 修复注释污染与「新队列 vs 存量」口径落盘) | 00-map · 01-scenario-taxonomy · 02-tech-landscape · 03-growth-maturity · 04-value-trend(+ _method/01) | `c18ba4a0d` |
| [`mechanics/system`](../mechanics/system/00-map.md) | **已核验**(0002:生命周期图并入八处机制变更:README-row 守卫/YAML 解析门/七类 regate 理由/held-rescan never-ran/sync-readme 重试/workflow_run 触发/探针白名单/site-health+adopt-discussions;规模事实刷新) | 仅 map | `c18ba4a0d` |
| [`mechanics/registry-data`](../mechanics/registry-data/00-map.md) | **已核验**(0002:name↔url 硬规则、capabilities.json 新边车、updates.json 勘误、CRLF 15、wsl 58/66、census 注释污染勘误) | 仅 map | `c18ba4a0d` |
| [`mechanics/readme-pipeline`](../mechanics/readme-pipeline/00-map.md) | **已核验**(0002:sync-readme 加固=ref: main + 三轮重试 + 硬失败;README 4579/4578 行;generate-readme 零 diff) | 00-map · 01-generate-readme | `c18ba4a0d` |
| [`mechanics/site-surface`](../mechanics/site-surface/00-map.md) | **已核验**(0002:site-health 看门狗、workflow_run 触发、探针白名单、capabilities/download-window 字段、terms.mjs 大小写修复、token 数勘误 30→32;site/ 目录零 diff) | 01-build-site · 02-templates-locales | `c18ba4a0d` |
| [`mechanics/submission-gates`](../mechanics/submission-gates/00-map.md) | **已核验**(0002:README-row 守卫 #5845、YAML 可解析门 #4680、name↔url 规则 #5756、七类 regate 理由(含 faulted/checkStaleRed)、新鲜红才否决 #5533、403 三义重写 #932、held-rescan never-ran #2202、≤3 条口径重数;pr-guard/check-submission/check-bleed 零 diff) | 01 · 02 · 03 | `c18ba4a0d` |
| [`mechanics/probes-and-decay`](../mechanics/probes-and-decay/00-map.md) | **已核验**(0002:readmes/updates 重写、capabilities 与 adopt 两层全新、download-window、subpath-gone、两条铁律修正、sidecar 拓扑更正;stars/npm/tarballs/screenshots 与两个 publish 零 diff) | 01 · 02 · 03 | `c18ba4a0d` |

> 核验方式说明:`submission-gates`、`registry-data`、`system`、`readme-pipeline` 由主笔逐行精读;`site-surface`、`probes-and-decay` 两专题由并行子代理逐行精读后主笔蒸馏,未做全文二次抽查——引用前如需强保证,按文中行号回源核对。`ecosystem` 的数字均可由 [`census.py`](../ecosystem/census.py)(标准库,无第三方依赖)重跑复现;技术标签为描述正则判定,精度边界见其 [02](../ecosystem/02-tech-landscape.md) 文末方法注记。

## 按源码组(粗粒度)

| 源码组 | 归入专题 |
|--------|----------|
| `data/plugins/*.yml`(**4392 个**) + `scripts/lib/entries.mjs` | registry-data |
| `data/*.json` **五个**提交边车(stars/downloads/added-dates/screenshots/capabilities)+ cache-only 四个(npm-map/readmes/tarballs/updates) | registry-data / probes-and-decay(写入方) |
| `scripts/generate-readme.mjs`、`.github/workflows/sync-readme.yml` | readme-pipeline |
| `scripts/build-site.mjs`、`site/*`、`scripts/lib/terms.mjs`、`scripts/download-window.mjs`、`.github/workflows/site-health.yml`、`scripts/check-site-health.mjs` | site-surface |
| `.github/workflows/pr-*.yml`、`regate.yml`、`held-rescan.yml`、`check-submission.mjs`、`check-bleed.mjs` | submission-gates |
| `.github/workflows/build-site.yml`、`decay-scan.yml`、`adopt-discussions.yml` | 分别归 site-surface / probes-and-decay / probes-and-decay 的调度视角 |
| `scripts/probe-*.mjs`、`scripts/lib/capabilities.mjs`、`probe-order.mjs`、`probe-updates-graphql.mjs`、`adopt.mjs`、`added-dates.mjs`、`scan-decay.mjs`、`publish-*.mjs`、`adopt-discussions.mjs` | probes-and-decay |
| `scripts/*.test.mjs`(6 个,0002 首批) | 随被测模块所属专题 |
| `scripts/migrate-to-yaml.mjs`、`reorder-categories.py`、`prune-legacy-screenshots.mjs`、`maint-rebase.sh` | 历史/迁移工具,分别挂在相关专题下 |
| `contributing.md`、PR/Issue 模板 | submission-gates |

## 研究工具自身的变更(0002)

消化材料的数字来自两个自研脚本,它们本轮也被修过——修的是"会静默出错"的地方:

| 脚本 | 0002 修复 |
|------|-----------|
| [`census.py`](../ecosystem/census.py) | 行内注释污染(2 条投稿把模板注释粘进 `category:` 行 → 凭空两个类目);新增 ⑧ 节「新队列 vs 存量」(把 04 §4 的口径落盘,此前不可复现) |
| [`fresh_probe.py`](../ecosystem/fresh_probe.py) | 长尾回源被 `RemoteDisconnected` 整轮打死(未捕获的非 URLError 异常);`IncompleteRead` 同类;失败条目被写进包名缓存 → 一次网络抖动永久固化成「未发布」;缓存只在整轮跑完后落盘 → 一次失败全部重来。现:重试 + 失败不入缓存 + 每 200 条增量落盘 |

上游合入后,把受影响的专题标为「需复核」再逐个降回；流程见 [`_change_log/`](../_change_log/00-index.md)。
