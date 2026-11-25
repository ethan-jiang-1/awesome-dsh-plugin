# Coverage · 覆盖矩阵

维护用索引：按源码组追踪消化覆盖状态。**未列出的源码文件不隐含任何覆盖承诺。**

状态含义：

- **骨架** — 只有 `00-map.md` 划了范围,无编号正文
- **进行中** — 有部分编号正文
- **已核验** — 结论核对过当前基线源码;「核验 commit」记录最后一次核对点

> **0007 复核方式**:`census.py` 在 **13136 条**上重跑(**一次通过、0 解析失败**,连续六轮以来第一次不需要修解析器);上游本轮**源码有实质 diff**——Release 历史成为第三个发布面(`probe-release-history.mjs` + `docs/release-history/v1/` 分片)、tarball 安装命令加 `-w`、npm 身份例外(`publishedNpmName`)、**8 条 workflow 加 fork 安全门(本 fork 不再自动构建/部署)**、`contributing.md` 补发布时效、英文首页标题改用 "DSH Plugins"。mechanics 六专题中 site-surface / probes-and-decay / submission-gates 有真实 diff(档案改写),system / registry-data 为计数与边车变化,readme-pipeline 零 diff。ecosystem 五篇正文的全部结构数字换到新基线;下载/星标仍未自采(连续五轮),故仍标为部分核验。

## 按专题

> **视图层(2026-11-18 新增;2026-11-19 加契约)**:`_view/`(三块板)+ `view_<领域>/`(领域册 → 子分类 → 单卡)不在下表按源码组追踪——它们的结构数字由 `census.py`/`delta.py` 可再生,卡片级实时值由 `_snapshots/live-*.json` 归档,纪律见 [`../AGENTS.md`](../AGENTS.md) §一/§二;**卡片数量与分型不在此记账**,避免每轮改这里。2026-11-19 起卡片 frontmatter 是元数据单一源,`verify.mjs` 校验 frontmatter/八段/SVG 证据级;`_data/` 由脚本生成。下表仍按七专题追踪档案层。


六个机制专题是**评估视角的辅助档案**,统一收纳在 [`mechanics/`](../mechanics/00-map.md)(其 [00-map](../mechanics/00-map.md) 是浓缩入口);ecosystem 是主轴。

| 专题 | 状态 | 已有正文 | 最近核验 commit |
|------|------|----------|-----------------|
| [`ecosystem`](../ecosystem/00-map.md) | **部分已核验**(0007:census 已覆盖 13136 条;00/01/02/03/04 的分类、作者、标签、首录与新队列换到新基线;历史下载/星标仅按采样日期引用,本轮仍未自采) | 00-map · 01-scenario-taxonomy · 02-tech-landscape · 03-growth-maturity · 04-value-trend(+ _method/01) | `8f1a1800e` |
| [`mechanics/system`](../mechanics/system/00-map.md) | **已核验**(0007:scripts 44→49 个 mjs、测试 11→13、lib 10→12,拓扑仍是 probe→lib→build;新增文件落在既有专题归组) | 仅 map | `8f1a1800e` |
| [`mechanics/registry-data`](../mechanics/registry-data/00-map.md) | **已核验**(0007:entries.mjs/schema 零 diff;边车 capabilities 3813→3805、stars 1447→1445、screenshots 290→289、downloads 624、added-dates 625→645;npm 身份例外在探针侧) | 仅 map | `8f1a1800e` |
| [`mechanics/readme-pipeline`](../mechanics/readme-pipeline/00-map.md) | **无对应 diff**(0007:generate-readme 零 diff;sync-readme 只加 fork 门;README 13326/13325 行可由 13136 条输入解释) | 00-map · 01-generate-readme | `8f1a1800e` |
| [`mechanics/site-surface`](../mechanics/site-surface/00-map.md) | **已核验**(0007:build-site +24/−3——Release 历史分片发布、tarball `-w`、updates.json 压缩 + `releaseHistory` 标记;locales 英文标题;build-site 的 fork 门使本 fork 不再自动部署) | 01-build-site · 02-templates-locales | `8f1a1800e` |
| [`mechanics/submission-gates`](../mechanics/submission-gates/00-map.md) | **已核验**(0007:8 条 workflow 加 repository_owner 门;pr-check 增 `npm-name.test.mjs`;pr-gate/check-submission 零 diff;contributing +8 是发布时效说明) | 01 · 02 · 03 | `8f1a1800e` |
| [`mechanics/probes-and-decay`](../mechanics/probes-and-decay/00-map.md) | **已核验**(0007:新增 release-history 探针族(30 仓/查询、240 查询预算、7 天重扫);probe-updates 原子写 + `$releaseHistoryV1` 缓存;probe-npm 身份例外;probe-readmes 补 zh 候选。**新发现:Release 历史有生产者、有产物、无消费者**——`releaseHistory` 在 `site/`、`.github/`、`data/`、contributing 零命中,`publish-updates.mjs` 只发 `updates.json`,分片不进 npm;与 0006 的 `data/releases.json`(有消费者、无生产者)互为镜像) | 01 · 02 · 03 | `8f1a1800e` |

> 核验方式说明:0004 六个机制专题都有真实 diff,均由子代理逐行读 diff 后改写档案,主代理另核对 market-index/capabilities/entries/check-site-health 的关键实现。`ecosystem` 的当前结构总数可由 [`census.py`](../ecosystem/census.py)(标准库,无第三方依赖)重跑;生态 03/04 中仍有按历史日期标注的 4392/3552 名单口径,只作为各次星标/下载采样的历史分母,不可视为当前基线。仓库下载/星标边车冻结于 2026-08-19,能力边车冻结于 2026-09-24(`dsh-trust-check@0.1.13`),均未用于更新趋势判断。

## 影响面层(leverage,2026-10-31 新建;同日出册到 `_leverage/`)

**这一层已搬出 `_digested/`**:两册(`leverage/` 两域与 `leverage-reshape-product/` 产品线)连同各自的 `_证据/` 一起移到仓库根同级目录 [`_leverage/`](../../_leverage/README.md),统一入口见该目录的 README。**2026-11-01 协作域再独立为 [`leverage-agent-collaboration/`](../../_leverage/leverage-agent-collaboration/README.md),分发与首启成 [`leverage-lifecycle/`](../../_leverage/leverage-lifecycle/README.md)。** 下表保留覆盖状态,路径指到新位置。

第二轴,不与 `ecosystem/` 的 23 类合并。四个方向成稿（协作/产品另册，第四册 `leverage-lifecycle` 另行成册）:宪章/索引、横向手册、机制卡、样本卡、原始证据各有其位。入口是 [`leverage/README.md`](../../_leverage/leverage/README.md);按任务借用看 [`BORROW.md`](../../_leverage/leverage/BORROW.md);全量清单见 [`catalog.md`](../../_leverage/leverage/catalog.md)。

| 域 | 状态 | 已有正文 | 证据来源 |
|----|------|----------|----------|
| [`leverage-reshape-product`](../../_leverage/leverage-reshape-product/README.md)(另册,与 leverage 平级) | **成稿**;核心卡已读到源码/实测,其余 README 级;三个 lever(通用插件 / profile 级产品 / 自带宿主)+ 独立规则源 | 1 规则源 + 3 lever 宪章(11 / 8 / 6 卡)+ 1 门 + 1 借用指南 + 1 候选池 + 9 证据 = 43 篇（2026-10-31 快照；2026-11-01 已增至 69 篇）+ 1 指标快照 | catalog + 插件 README + 2026-10-31 指标快照 |
| [`leverage-agent-collaboration`](../../_leverage/leverage-agent-collaboration/README.md)(原 `lever-cross-boundary`,2026-11-01 另册) | **成稿**;四家族 17 样本源码逐文件读过,影响力用 2026-10-31 实时数据 | 1 规则源 + 5 家族(3/6/2/5/1 样本)+ 横向卷 | 2026-10-31 实时 GitHub/npm |
| [`lever-prove-output`](../../_leverage/leverage/lever-prove-output/README.md) | **成稿**;12 样本,17 个仓库锁 `repo@commit` | 1 宪章 + 10 卡(含溯源卡/手册) | `repo@commit` + 实时抓取 |
| [`lever-draw-limit`](../../_leverage/leverage/lever-draw-limit/README.md) | **成稿**;10 样本,多卡读过 src,坐标只锁版本 | 1 宪章 + 8 卡 + 1 手册 | npm 近 30 天 + `capabilities.json` |

**准入是人工判断,不是脚本**:证据类型 A/B/C/D/E/F/G 与 S/A/B/C 分级见 [`leverage/horizon.md`](../../_leverage/leverage/horizon.md)。**不设通过率、不跑全库计数**——名单在涨,任何 `N / 总数` 都会过期。

> **未做/已知缺口**:证据强度分域——PROVE 锁 `repo@commit`,LIMIT 读源码但只锁版本,协作册与产品线证据深度逐卡标注(部分源码级/实测,部分 README 级)、未锁 `repo@commit`;E 级(反面教材)只有 2 条真判;规格独立性、多门禁共存、租约 epoch 仍未解决。完整清单在 [`BORROW.md`](../../_leverage/leverage/BORROW.md) §6;各域「待答问题」与 [horizon](../../_leverage/leverage/horizon.md) §7 是下一轮入口。

## 按源码组(粗粒度)

| 源码组 | 归入专题 |
|--------|----------|
| `data/plugins/*.yml`(**13136 个**) + `scripts/lib/entries.mjs` | registry-data |
| `data/*.json` **五个**提交边车(stars/downloads/added-dates/screenshots/capabilities)+ cache-only 五个(npm-map/readmes/tarballs/updates/**releases**;0007 起 `updates.json` 内部另有 `$releaseHistoryV1` 缓存键,仍不提交) | registry-data / probes-and-decay(写入方) |
| `scripts/generate-readme.mjs`、`.github/workflows/sync-readme.yml` | readme-pipeline |
| `scripts/build-site.mjs`、`site/*`、`scripts/lib/terms.mjs`、`scripts/lib/release-history.mjs`、`scripts/download-window.mjs`、`.github/workflows/site-health.yml`、`scripts/check-site-health.mjs` | site-surface |
| `.github/workflows/pr-*.yml`、`regate.yml`、`held-rescan.yml`、`check-submission.mjs`、`check-bleed.mjs` | submission-gates |
| `.github/workflows/build-site.yml`、`decay-scan.yml`、`adopt-discussions.yml` | 分别归 site-surface / probes-and-decay / probes-and-decay 的调度视角 |
| `scripts/probe-*.mjs`(含 0007 新增 `probe-release-history.mjs`)、`scripts/lib/capabilities.mjs`、`scripts/lib/npm-name.mjs`、`scripts/lib/release-history.mjs`(写入方)、`probe-order.mjs`、`probe-updates-graphql.mjs`、`adopt.mjs`、`added-dates.mjs`、`scan-decay.mjs`、`publish-*.mjs`、`adopt-discussions.mjs` | probes-and-decay |
| `scripts/*.test.mjs`(**13 个**;0002 首批 6 个,0004 增 2 个,0006 增 `github-statistics`、`release-manifest`、`market-index-collisions`,0007 增 `release-history`、`npm-name`) | 随被测模块所属专题 |
| `scripts/migrate-to-yaml.mjs`、`reorder-categories.py`、`prune-legacy-screenshots.mjs`、`maint-rebase.sh` | 历史/迁移工具,分别挂在相关专题下 |
| `contributing.md`、PR/Issue 模板 | submission-gates |

## 研究工具自身的变更(0002–2026-11-19)

消化材料的数字来自两个自研脚本,它们本轮也被修过——修的是"会静默出错"的地方:

| 脚本 | 0002 修复 |
|------|-----------|
| [`census.py`](../ecosystem/census.py) | 行内注释污染(2 条投稿把模板注释粘进 `category:` 行 → 凭空两个类目);新增 ⑧ 节「新队列 vs 存量」(把 04 §4 的口径落盘,此前不可复现) |
| [`fresh_probe.py`](../ecosystem/fresh_probe.py) | 长尾回源被 `RemoteDisconnected` 整轮打死(未捕获的非 URLError 异常);`IncompleteRead` 同类;失败条目被写进包名缓存 → 一次网络抖动永久固化成「未发布」;缓存只在整轮跑完后落盘 → 一次失败全部重来。现:重试 + 失败不入缓存 + 每 200 条增量落盘 |

0004:研究工具本身(`census.py`、`fresh_probe.py`、`verify.mjs`)没有改动——上游仍未携带 `_digested/`,合并不会碰这些文件;数字口径的变化只体现为输入数据从 4489 条变成 6704 条。

**0005:`census.py` 修了一处会静默少算分母的地方**——两份新条目把 JSON 直接写进 `.yml`(js-yaml 接受,门禁也放行),而 `parse_yml` 只认 YAML 行,两条因此被跳过、只留一行 stderr。现在遇到 `{` 开头就回退到 `json.loads`,并对 `description` 做展平;修后总数 7922 → **7924**。`fresh_probe.py` 与 `verify.mjs` 未动。

**0006:`census.py` 再修同类缺陷(共三处)**——(1) 折叠标量:一条新条目的 `description.en` 引号跨多行(YAML 折叠),按行匹配失败;(2) 整文件统一缩进:另一条新条目全文缩进 3 空格,顶层键正则不认;(3) 支持缩进时引入的回归(复核自查并当场修复):剥缩进后 `en:`/`zh:` 子键被通用键正则吞掉,`description.en/zh` 丢失、标签与中文统计塌缩,已改为子键先匹配。均属 js-yaml 接受而手写解析器拒绝/错读的序列(0002 行内注释、0005 JSON-in-.yml 以来第六次)。修后总数 11743 → **11744**(0 解析失败),标签命中 8686、中文描述 11218/11744(95%,0005 为 100%——本轮新进条目约 5% 缺中文)。`fresh_probe.py` 与 `verify.mjs` 未动。

**0007:解析器首次零修复通过**——`census.py` 在 13136 条上重跑即 0 解析失败(总数与 `ls data/plugins/*.yml | wc -l` 一致),说明 0006 补的三类形态已覆盖本轮数据。不过这不改变纪律:每轮同步后仍必须先跑 census 并核对分母与标签/中文命中数,突变即回头查解析。`fresh_probe.py` 与 `verify.mjs` 未动。

**2026-10-31(整理轮)**:[`verify.mjs`](../verify.mjs) 负责 `_digested/` 两棵树的编码/链接/锚点;`_leverage/` 出册后自带独立校验器(`_leverage/verify.mjs`,对两册强制 frontmatter / 借用节 / catalog 与卡表一致);[`catalog.md`](../../_leverage/leverage/catalog.md) 改为**手工维护**的全量清单(不生成、不校验计数)。这两处把「每篇的定位与借用节」变成可校验的契约,而不是靠人记。

**2026-10-31(另册对齐)**:产品线顶层改为与 `leverage/` 同构的骨架——`README` / `00-map` / `horizon` / `BORROW` / `BACKLOG` / `catalog`,**固定名、不编号**;卡片仍用 `NN_`。`verify.mjs` 同时增两条契约:产品线 `catalog.md` 与目录 Markdown 集合**双向一致**、三个 lever README 卡表覆盖本 lever 全部编号卡。

**2026-11-19(审查整改轮)**:这一轮不碰上游,只修“汇总层与证据层不一致”和“实时数字无落盘”两类问题。改动:

| 问题 | 修法 | 回归 |
|------|------|------|
| `delta.py` ③b 用“URL 含 token”当锚自身,把 `dsh-hindsight-*` / `dsh-openviking-*` / `dsh-better-sidebar-N23` 误排除 | 改为 `repo_key()` 精确仓库身份;输出 `锚自身 / 同名候选 / 描述候选` 三层;新增 `test_delta.py` 8 个用例 | `python3 -m unittest _digested/ecosystem/test_delta.py`;③b 现在 `better-sidebar 64`、`hindsight 9`、`openviking 3` |
| 卡片证据级/状态/commit 在卡、领域册、SVG 三处手抄 | 40 张卡加 frontmatter(单一源);`verify.mjs` 校验必填字段、★★★ commit、八段、SVG 证据级与链接 | `node _digested/verify.mjs` |
| “63 个插件接入”把 mentions 写成 adoption | better-sidebar 改 64(1 同名 fork + 63 描述),抽样 3 个只写 1 硬依赖;卡片补精确复现代码 | 卡片/README/SVG 同步 |
| session 册写“七者第三方提及全部为零”,但卡内是 3 / 6 | 改为“无协议级复用;message-edit 3、billion-context 6”;AGENTS 同步 | 卡内逐条命令 |
| memory 册写“全部 ★★★”,OpenViking 实为 ★★ | 改成 7 张 ★★★ + 1 张 ★★ 参考卡;SVG 证据级改 ★★;参考卡标题去“锚” | `verify` 的“全部 ★★★”检查 |
| `_view/03` 仍写 MisakaNet“纯社区最高” | 改成“主项目背书、DSH 适配层扩散 0,不是纯社区最高” | 与 memory 册一致 |
| 实时星标/下载无快照,37 张卡各写各的 | 新增 `live_probe.py` + `_snapshots/live-2026-11-19.json`(107/108 repo、39/52 已发布包;404 = unpublished)| `_data/health.md` |
| 无单一数据源/健康轴 | 新增 `cardmeta.py`、`view_data.py`、`_data/cards.json` / `summary.json` / `health.md` | 生成式,不再手抄 |

`_view/01` 的“没有任何苗子”改成“不能判断(采样缺口)”;`04` 的“连续两轮”改成“四轮”;`00-index` 的星标口径改为指向 live 快照。本轮没有重跑 `fresh_probe` 全量下载,历史下载数字仍按 2026-09-12 标注。

**后续(未做,已列缺口)**:

- 全量 npm 下载 + 星标重采(本轮只做了卡片/锚的 11-19 快照;全量下载仍是 09-12);
- repo 级去重统计(本轮只在 `_view/02` 加了口径提醒,未改 census/delta 输出);
- 领域选型矩阵(数据存哪/外部依赖/权限/宿主耦合/测试/健康) — `_data/cards.json` 已具备字段基础;
- 接缝图谱(seam atlas)与 50 条新条目质量抽样(模板化/账号年龄/README/测试);
- 全量 `fresh_probe` 的网络窗口与预算仍未验证。

上游合入后,把受影响的专题标为「需复核」再逐个降回；流程见 [`_change_log/`](../_change_log/00-index.md)。
