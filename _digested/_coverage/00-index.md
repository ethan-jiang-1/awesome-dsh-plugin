# Coverage · 覆盖矩阵

维护用索引：按源码组追踪消化覆盖状态。**未列出的源码文件不隐含任何覆盖承诺。**

状态含义：

- **骨架** — 只有 `00-map.md` 划了范围,无编号正文
- **进行中** — 有部分编号正文
- **已核验** — 结论核对过当前基线源码;「核验 commit」记录最后一次核对点

> **0003 复核方式**:`census.py` 重跑了分类/作者/标签/首录结构;site-surface 由并行子代理逐行审阅 build/template/locales diff。其他机制组按源码 diff 确认无对应变更。未自采下载/星标;ecosystem 正文已更新结构与历史指标的采样边界,故仍标为部分核验。

## 按专题

六个机制专题是**评估视角的辅助档案**,统一收纳在 [`mechanics/`](../mechanics/00-map.md)(其 [00-map](../mechanics/00-map.md) 是浓缩入口);ecosystem 是主轴。

| 专题 | 状态 | 已有正文 | 最近核验 commit |
|------|------|----------|-----------------|
| [`ecosystem`](../ecosystem/00-map.md) | **部分已核验**(0003:census 结构普查已覆盖 4489 条;00-map/01/02/03 的分类、作者、标签与首录结构更新;04 的漂移与外部信号时效更新,历史下载/星标仅按采样日期引用,本轮未自采) | 00-map · 01-scenario-taxonomy · 02-tech-landscape · 03-growth-maturity · 04-value-trend(+ _method/01) | `4693e5a83` |
| [`mechanics/system`](../mechanics/system/00-map.md) | **已核验**(0003:门禁/探针/发布 topology 无 diff;规模基数更新,站点投影增加 catalog/windowing) | 仅 map | `4693e5a83` |
| [`mechanics/registry-data`](../mechanics/registry-data/00-map.md) | **已核验**(0003:schema 与 sidecar 拓扑无 diff;条目/分类/作者与 wsl 计数更新) | 仅 map | `4693e5a83` |
| [`mechanics/readme-pipeline`](../mechanics/readme-pipeline/00-map.md) | **已核验**(0003:generate-readme 与 sync-readme workflow 无 diff;README 仍为生成投影) | 00-map · 01-generate-readme | `4693e5a83` |
| [`mechanics/site-surface`](../mechanics/site-surface/00-map.md) | **已核验**(0003:24 卡片 SSR/no-JS fallback、locale/category catalogs、hash cache bust、客户端虚拟列表与失败回退) | 01-build-site · 02-templates-locales | `4693e5a83` |
| [`mechanics/submission-gates`](../mechanics/submission-gates/00-map.md) | **已核验**(0003:pr-check/pr-gate/regate/held-rescan 与门禁脚本无 diff) | 01 · 02 · 03 | `4693e5a83` |
| [`mechanics/probes-and-decay`](../mechanics/probes-and-decay/00-map.md) | **已核验**(0003:探针、decay、publish 源码与调度无 diff;冻结 stars 边车仅随条目删除而删键) | 01 · 02 · 03 | `4693e5a83` |

> 核验方式说明:0003 的机制专题按上游 diff 范围判断;site-surface 另外逐读了核心模板/构建变化。`ecosystem` 的当前结构总数可由 [`census.py`](../ecosystem/census.py)(标准库,无第三方依赖)重跑;生态 03/04 中仍有按历史日期标注的 4392/3552 名单口径,只作为各次星标/下载采样的历史分母,不可视为当前基线。仓库下载/星标边车冻结于 2026-08-19,未用于更新趋势判断。

## 按源码组(粗粒度)

| 源码组 | 归入专题 |
|--------|----------|
| `data/plugins/*.yml`(**4489 个**) + `scripts/lib/entries.mjs` | registry-data |
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
