# Coverage · 覆盖矩阵

维护用索引：按源码组追踪消化覆盖状态。**未列出的源码文件不隐含任何覆盖承诺。**

状态含义：

- **骨架** — 只有 `00-map.md` 划了范围,无编号正文
- **进行中** — 有部分编号正文
- **已核验** — 结论核对过当前基线源码;「核验 commit」记录最后一次核对点

> **0005 复核方式**:`census.py` 在 **7924 条**上重跑(并修了 JSON-in-.yml 解析,见末节);上游本轮**源码零 diff**——`scripts/`、`site/`、`.github/workflows/`(仍 10 条)、`package.json` 全部未动,六个机制专题按「无对应 diff」核验,唯一实质 diff 是 `contributing.md` 的 held 文档段。ecosystem 五篇正文的**全部结构数字**换到新基线;下载/星标仍未自采(连续三轮),故仍标为部分核验。

## 按专题

六个机制专题是**评估视角的辅助档案**,统一收纳在 [`mechanics/`](../mechanics/00-map.md)(其 [00-map](../mechanics/00-map.md) 是浓缩入口);ecosystem 是主轴。

| 专题 | 状态 | 已有正文 | 最近核验 commit |
|------|------|----------|-----------------|
| [`ecosystem`](../ecosystem/00-map.md) | **部分已核验**(0005:census 已覆盖 7924 条;00/01/02/03 的分类、作者、标签、首录与新队列漂移更新;04 的时效边界与删撤侧观察更新;能力披露 join 重算为 3764(47.5%);历史下载/星标仅按采样日期引用,本轮仍未自采) | 00-map · 01-scenario-taxonomy · 02-tech-landscape · 03-growth-maturity · 04-value-trend(+ _method/01) | `efe602e7b` |
| [`mechanics/system`](../mechanics/system/00-map.md) | **无对应 diff**(0005:scripts 6952 行/38 个 mjs、10 条 workflow、site/、package.json 全部零 diff;仅名单 6704→7924) | 仅 map | `efe602e7b` |
| [`mechanics/registry-data`](../mechanics/registry-data/00-map.md) | **无对应 diff**(0005:entries.mjs/schema 零 diff;新增 2 条 JSON-in-.yml 被 js-yaml 接收,属数据形态;边车只减不增) | 仅 map | `efe602e7b` |
| [`mechanics/readme-pipeline`](../mechanics/readme-pipeline/00-map.md) | **无对应 diff**(0005:generate-readme 与 sync-readme 均零 diff;README 8114/8113 行、PLUGINS 块 7992 行可完全由 7924 条输入解释) | 00-map · 01-generate-readme | `efe602e7b` |
| [`mechanics/site-surface`](../mechanics/site-surface/00-map.md) | **无对应 diff**(0005:build-site.mjs、site/、locales 零 diff;详情页规模随名单变,约 1.59 万个) | 01-build-site · 02-templates-locales | `efe602e7b` |
| [`mechanics/submission-gates`](../mechanics/submission-gates/00-map.md) | **已核验**(0005:10 条 workflow 与校验脚本零 diff;`contributing.md` 新增 held/After review 一节,把标签语义、tracking issue 与 gate 列 `—` 写清楚) | 01 · 02 · 03 | `efe602e7b` |
| [`mechanics/probes-and-decay`](../mechanics/probes-and-decay/00-map.md) | **无对应 diff**(0005:probe/scan 脚本与 cache path 零 diff;能力披露 join 因分母扩大降到 47.5%,边车回写通道仍未新增) | 01 · 02 · 03 | `efe602e7b` |

> 核验方式说明:0004 六个机制专题都有真实 diff,均由子代理逐行读 diff 后改写档案,主代理另核对 market-index/capabilities/entries/check-site-health 的关键实现。`ecosystem` 的当前结构总数可由 [`census.py`](../ecosystem/census.py)(标准库,无第三方依赖)重跑;生态 03/04 中仍有按历史日期标注的 4392/3552 名单口径,只作为各次星标/下载采样的历史分母,不可视为当前基线。仓库下载/星标边车冻结于 2026-08-19,能力边车冻结于 2026-09-24(`dsh-trust-check@0.1.13`),均未用于更新趋势判断。

## 影响面层(leverage,2026-10-31 新建;同日出册到 `_leverage/`)

**这一层已搬出 `_digested/`**:两册(`leverage/` 三域与 `leverage-reshape-product/` 产品线)连同各自的 `_证据/` 一起移到仓库根同级目录 [`_leverage/`](../../_leverage/README.md),统一入口见该目录的 README。下表保留覆盖状态,路径指到新位置。

第二轴,不与 `ecosystem/` 的 23 类合并。四域成稿:宪章/索引、横向手册、机制卡、样本卡、原始证据各有其位。入口是 [`leverage/README.md`](../../_leverage/leverage/README.md);按任务借用看 [`BORROW.md`](../../_leverage/leverage/BORROW.md);全量清单见 [`catalog.md`](../../_leverage/leverage/catalog.md)。

| 域 | 状态 | 已有正文 | 证据来源 |
|----|------|----------|----------|
| [`leverage-reshape-product`](../../_leverage/leverage-reshape-product/README.md)(另册,与 leverage 平级) | **成稿**;核心卡已读到源码/实测,其余 README 级;三个 lever(通用插件 / profile 级产品 / 自带宿主)+ 独立规则源 | 1 规则源 + 3 lever 宪章(11 / 7 / 6 卡)+ 1 门 + 1 借用指南 + 1 候选池 + 8 证据 = 41 篇 + 1 指标快照 | catalog + 插件 README + 2026-10-31 指标快照 |
| [`lever-cross-boundary`](../../_leverage/leverage/lever-cross-boundary/README.md) | **成稿**;14 样本源码逐文件读过,影响力用 2026-10-31 实时数据 | 1 宪章 + 3 横向卡 + 14 样本 | 2026-10-31 实时 GitHub/npm |
| [`lever-prove-output`](../../_leverage/leverage/lever-prove-output/README.md) | **成稿**;12 样本,17 个仓库锁 `repo@commit` | 1 宪章 + 10 卡(含溯源卡/手册) | `repo@commit` + 实时抓取 |
| [`lever-draw-limit`](../../_leverage/leverage/lever-draw-limit/README.md) | **成稿**;10 样本,多卡读过 src,坐标只锁版本 | 1 宪章 + 8 卡 + 1 手册 | npm 近 30 天 + `capabilities.json` |

**准入是人工判断,不是脚本**:证据类型 A/B/C/D/E/F/G 与 S/A/B/C 分级见 [`leverage/horizon.md`](../../_leverage/leverage/horizon.md)。**不设通过率、不跑全库计数**——名单在涨,任何 `N / 总数` 都会过期。

> **未做/已知缺口**:证据强度分域——PROVE 锁 `repo@commit`,CROSS/LIMIT 读源码但只锁版本,RESHAPE 证据深度逐卡标注(部分源码级/实测,部分 README 级)、未锁 `repo@commit`;E 级(反面教材)只有 2 条真判;规格独立性、多门禁共存、租约 epoch 仍未解决。完整清单在 [`BORROW.md`](../../_leverage/leverage/BORROW.md) §6;各域「待答问题」与 [horizon](../../_leverage/leverage/horizon.md) §7 是下一轮入口。

## 按源码组(粗粒度)

| 源码组 | 归入专题 |
|--------|----------|
| `data/plugins/*.yml`(**7924 个**) + `scripts/lib/entries.mjs` | registry-data |
| `data/*.json` **五个**提交边车(stars/downloads/added-dates/screenshots/capabilities)+ cache-only 四个(npm-map/readmes/tarballs/updates) | registry-data / probes-and-decay(写入方) |
| `scripts/generate-readme.mjs`、`.github/workflows/sync-readme.yml` | readme-pipeline |
| `scripts/build-site.mjs`、`site/*`、`scripts/lib/terms.mjs`、`scripts/download-window.mjs`、`.github/workflows/site-health.yml`、`scripts/check-site-health.mjs` | site-surface |
| `.github/workflows/pr-*.yml`、`regate.yml`、`held-rescan.yml`、`check-submission.mjs`、`check-bleed.mjs` | submission-gates |
| `.github/workflows/build-site.yml`、`decay-scan.yml`、`adopt-discussions.yml` | 分别归 site-surface / probes-and-decay / probes-and-decay 的调度视角 |
| `scripts/probe-*.mjs`、`scripts/lib/capabilities.mjs`、`probe-order.mjs`、`probe-updates-graphql.mjs`、`adopt.mjs`、`added-dates.mjs`、`scan-decay.mjs`、`publish-*.mjs`、`adopt-discussions.mjs` | probes-and-decay |
| `scripts/*.test.mjs`(8 个;0002 首批 6 个,0004 增 `entries-path` 与 `card-install-command`) | 随被测模块所属专题 |
| `scripts/migrate-to-yaml.mjs`、`reorder-categories.py`、`prune-legacy-screenshots.mjs`、`maint-rebase.sh` | 历史/迁移工具,分别挂在相关专题下 |
| `contributing.md`、PR/Issue 模板 | submission-gates |

## 研究工具自身的变更(0002–0005)

消化材料的数字来自两个自研脚本,它们本轮也被修过——修的是"会静默出错"的地方:

| 脚本 | 0002 修复 |
|------|-----------|
| [`census.py`](../ecosystem/census.py) | 行内注释污染(2 条投稿把模板注释粘进 `category:` 行 → 凭空两个类目);新增 ⑧ 节「新队列 vs 存量」(把 04 §4 的口径落盘,此前不可复现) |
| [`fresh_probe.py`](../ecosystem/fresh_probe.py) | 长尾回源被 `RemoteDisconnected` 整轮打死(未捕获的非 URLError 异常);`IncompleteRead` 同类;失败条目被写进包名缓存 → 一次网络抖动永久固化成「未发布」;缓存只在整轮跑完后落盘 → 一次失败全部重来。现:重试 + 失败不入缓存 + 每 200 条增量落盘 |

0004:研究工具本身(`census.py`、`fresh_probe.py`、`verify.mjs`)没有改动——上游仍未携带 `_digested/`,合并不会碰这些文件;数字口径的变化只体现为输入数据从 4489 条变成 6704 条。

**0005:`census.py` 修了一处会静默少算分母的地方**——两份新条目把 JSON 直接写进 `.yml`(js-yaml 接受,门禁也放行),而 `parse_yml` 只认 YAML 行,两条因此被跳过、只留一行 stderr。现在遇到 `{` 开头就回退到 `json.loads`,并对 `description` 做展平;修后总数 7922 → **7924**。`fresh_probe.py` 与 `verify.mjs` 未动。

**2026-10-31(整理轮)**:[`verify.mjs`](../verify.mjs) 负责 `_digested/` 两棵树的编码/链接/锚点;`_leverage/` 出册后自带独立校验器(`_leverage/verify.mjs`,对两册强制 frontmatter / 借用节 / catalog 与卡表一致);[`catalog.md`](../../_leverage/leverage/catalog.md) 改为**手工维护**的全量清单(不生成、不校验计数)。这两处把「每篇的定位与借用节」变成可校验的契约,而不是靠人记。

**2026-10-31(另册对齐)**:产品线顶层改为与 `leverage/` 同构的骨架——`README` / `00-map` / `horizon` / `BORROW` / `BACKLOG` / `catalog`,**固定名、不编号**;卡片仍用 `NN_`。`verify.mjs` 同时增两条契约:产品线 `catalog.md` 与目录 Markdown 集合**双向一致**、三个 lever README 卡表覆盖本 lever 全部编号卡。

上游合入后,把受影响的专题标为「需复核」再逐个降回；流程见 [`_change_log/`](../_change_log/00-index.md)。
