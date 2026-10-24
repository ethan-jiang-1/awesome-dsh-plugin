# Coverage · 覆盖矩阵

维护用索引：按源码组追踪消化覆盖状态。**未列出的源码文件不隐含任何覆盖承诺。**

状态含义：

- **骨架** — 只有 `00-map.md` 划了范围,无编号正文
- **进行中** — 有部分编号正文
- **已核验** — 结论核对过当前基线源码;「核验 commit」记录最后一次核对点

> **0004 复核方式**:`census.py` 在 6704 条上重跑分类/作者/标签/首录/新队列与成熟度 join;六个机制专题都有对应 diff,由并行子代理分别逐行审阅(市场索引、能力扫描 0.2.1、icon schema、POSIX 路径、CI 换源、站点索引导出),再由主代理核对关键文件与数字。未自采下载/星标;ecosystem 正文已更新结构与历史指标的采样边界,故仍标为部分核验。

## 按专题

六个机制专题是**评估视角的辅助档案**,统一收纳在 [`mechanics/`](../mechanics/00-map.md)(其 [00-map](../mechanics/00-map.md) 是浓缩入口);ecosystem 是主轴。

| 专题 | 状态 | 已有正文 | 最近核验 commit |
|------|------|----------|-----------------|
| [`ecosystem`](../ecosystem/00-map.md) | **部分已核验**(0004:census 结构普查已覆盖 6704 条;00-map/01/02/03 的分类、作者、标签与首录结构更新;04 的漂移、市场索引分发面与外部信号时效更新;能力披露 join 重算为 3792,历史下载/星标仅按采样日期引用,本轮未自采) | 00-map · 01-scenario-taxonomy · 02-tech-landscape · 03-growth-maturity · 04-value-trend(+ _method/01) | `b4d0049a8` |
| [`mechanics/system`](../mechanics/system/00-map.md) | **已核验**(0004:新增市场索引产物与 `@deepseek-ai/dsh-plugin-market-index` 依赖,scripts 6952 行/8 个测试/10 条 workflow,CI 换 npm 源) | 仅 map | `b4d0049a8` |
| [`mechanics/registry-data`](../mechanics/registry-data/00-map.md) | **已核验**(0004:schema 新增可选 `icon`(GitHub 托管位图),`ENTRY_KEYS` 扩展,`readEntries` 返回 POSIX 路径;边车行数不变) | 仅 map | `b4d0049a8` |
| [`mechanics/readme-pipeline`](../mechanics/readme-pipeline/00-map.md) | **已核验**(0004:generate-readme 无 diff;sync-readme 只多了 CI npm 源设置;README 新增市场索引粘贴说明,仍是生成投影) | 00-map · 01-generate-readme | `b4d0049a8` |
| [`mechanics/site-surface`](../mechanics/site-surface/00-map.md) | **已核验**(0004:市场索引 `docs/index.json` 与首页面板、icon 渲染与头像回退、`skip_probes` 手动输入、健康检查改读 sitemap 因首页已窗口化) | 01-build-site · 02-templates-locales | `b4d0049a8` |
| [`mechanics/submission-gates`](../mechanics/submission-gates/00-map.md) | **已核验**(0004:icon 校验进 `validateEntries`、entry-path 测试进 pr-check;pr-gate 只改 npm 源;`dsh-trust-check` 依赖 0.1.13→0.2.1) | 01 · 02 · 03 | `b4d0049a8` |
| [`mechanics/probes-and-decay`](../mechanics/probes-and-decay/00-map.md) | **已核验**(0004:能力扫描升 0.2.1(schema 1/2 可读、保留上一版、provenance 声明)、`capability-changes.mjs`、`probe-npm` 记录发布时间与 `engines.dsh`、catalog 附带 index;边车回写通道仍未新增) | 01 · 02 · 03 | `b4d0049a8` |

> 核验方式说明:0004 六个机制专题都有真实 diff,均由子代理逐行读 diff 后改写档案,主代理另核对 market-index/capabilities/entries/check-site-health 的关键实现。`ecosystem` 的当前结构总数可由 [`census.py`](../ecosystem/census.py)(标准库,无第三方依赖)重跑;生态 03/04 中仍有按历史日期标注的 4392/3552 名单口径,只作为各次星标/下载采样的历史分母,不可视为当前基线。仓库下载/星标边车冻结于 2026-08-19,能力边车冻结于 2026-09-24(`dsh-trust-check@0.1.13`),均未用于更新趋势判断。

## 按源码组(粗粒度)

| 源码组 | 归入专题 |
|--------|----------|
| `data/plugins/*.yml`(**6704 个**) + `scripts/lib/entries.mjs` | registry-data |
| `data/*.json` **五个**提交边车(stars/downloads/added-dates/screenshots/capabilities)+ cache-only 四个(npm-map/readmes/tarballs/updates) | registry-data / probes-and-decay(写入方) |
| `scripts/generate-readme.mjs`、`.github/workflows/sync-readme.yml` | readme-pipeline |
| `scripts/build-site.mjs`、`site/*`、`scripts/lib/terms.mjs`、`scripts/download-window.mjs`、`.github/workflows/site-health.yml`、`scripts/check-site-health.mjs` | site-surface |
| `.github/workflows/pr-*.yml`、`regate.yml`、`held-rescan.yml`、`check-submission.mjs`、`check-bleed.mjs` | submission-gates |
| `.github/workflows/build-site.yml`、`decay-scan.yml`、`adopt-discussions.yml` | 分别归 site-surface / probes-and-decay / probes-and-decay 的调度视角 |
| `scripts/probe-*.mjs`、`scripts/lib/capabilities.mjs`、`probe-order.mjs`、`probe-updates-graphql.mjs`、`adopt.mjs`、`added-dates.mjs`、`scan-decay.mjs`、`publish-*.mjs`、`adopt-discussions.mjs` | probes-and-decay |
| `scripts/*.test.mjs`(8 个;0002 首批 6 个,0004 增 `entries-path` 与 `card-install-command`) | 随被测模块所属专题 |
| `scripts/migrate-to-yaml.mjs`、`reorder-categories.py`、`prune-legacy-screenshots.mjs`、`maint-rebase.sh` | 历史/迁移工具,分别挂在相关专题下 |
| `contributing.md`、PR/Issue 模板 | submission-gates |

## 研究工具自身的变更(0002)

消化材料的数字来自两个自研脚本,它们本轮也被修过——修的是"会静默出错"的地方:

| 脚本 | 0002 修复 |
|------|-----------|
| [`census.py`](../ecosystem/census.py) | 行内注释污染(2 条投稿把模板注释粘进 `category:` 行 → 凭空两个类目);新增 ⑧ 节「新队列 vs 存量」(把 04 §4 的口径落盘,此前不可复现) |
| [`fresh_probe.py`](../ecosystem/fresh_probe.py) | 长尾回源被 `RemoteDisconnected` 整轮打死(未捕获的非 URLError 异常);`IncompleteRead` 同类;失败条目被写进包名缓存 → 一次网络抖动永久固化成「未发布」;缓存只在整轮跑完后落盘 → 一次失败全部重来。现:重试 + 失败不入缓存 + 每 200 条增量落盘 |

0004:研究工具本身(`census.py`、`fresh_probe.py`、`verify.mjs`)没有改动——本轮上游仍未携带 `_digested/`,合并不会碰这些文件;数字口径的变化只体现为输入数据从 4489 条变成 6704 条。

上游合入后,把受影响的专题标为「需复核」再逐个降回；流程见 [`_change_log/`](../_change_log/00-index.md)。
