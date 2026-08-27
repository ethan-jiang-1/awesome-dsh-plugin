# ecosystem 03 · 演化节奏、作者结构与成熟度金字塔

> 数据:`census.py` ②③⑤⑥ 节,`main@5e7dc7eb`,2026-08-27。首录日期来自 `git log --diff-filter=A` 单趟遍历(58 条早期批量导入无日期,不进时间统计)。

## 1. 演化:一天 land-grab,然后进入稳态

```
2026-08-13   init(仓库创建)
2026-08-16   963 条单日入库 ← 42% 的存量在这天落地
2026-08-17~21  199 / 189 / 151 / 159 / 113
2026-08-22     4(周六谷值)
2026-08-23~27 106 / 190 / 54 / 42 / 58(今日未完)
```

- 近 7 天日均新增 **81 条**,较开局明显降温——生态已完成从"首批搬运"到"增量投递"的换挡;
- 有周末节律(8-22 只进 4 条),说明投稿者是真人开发者而非脚本灌库;
- **新增构成高度稳定**:近 7 天 ui 类每天占当日新增的 15–23%,从未掉出第一;notify 则在前半周 25% 之后归零——UI 军备竞赛仍在持续,而"推 IM"这波已经过峰。

## 2. 作者结构:78% 单件作者 + 一撮工作室

1522 个 owner:

| 条目数 | 作者数 |
|--------|-------:|
| 1 件 | 1182 (77.6%) |
| 2–4 | 297 |
| 5–9 | 33 |
| 10–29 | 9 |
| ≥30 | 1 |

Top owner 即可读出两种典型:

- **omdsh-dev(37 条)= 系列工作室**:`dsh-tool-{csv,diff,json,markdown,regex,schema,stat,time,calculator}` 微工具全家桶、sandbox-micro/mxc/nono 三连、deep-research、甚至附 `plugin-template` 脚手架——把"给 DSH 做插件"当作产品线经营;
- **damonkoy / zhu1090093659(dsh-web-ui)= monorepo 大户**:一个仓拆 12 个子包条目收录;
- johnxu22786(29)、perrylink(22)等其余头部待抽样定性(见 [00-map 待答](00-map.md))。

对生态健康的含义:长尾极碎但存在职业化生产者,且头部作者的插件之间开始互相引用(census ⑥ 显示 sub 包命名已互相兼容)。

## 3. 成熟度金字塔:冷长尾 + 外部巨头接入

stars 覆盖 1494 条:**中位 2,75% ≤5 星,≥100 星仅 49 条**;均值 73 完全被头部拉走。

Top by stars(节选):

| stars | 条目 | 注 |
|------:|------|----|
| 29567 | volcengine/OpenViking#examples/dsh-memory-plugin | 字节跳动项目,**以示例目录身份接入** memory 类 |
| 20218 | vectorize-io/hindsight#coding-agents | 外部 memory 项目 |
| 14283 | tt-a1i/archify#integrations/deepseek-harness | 外部 docs 项目 |
| 5565 | Q00/ouroboros#integrations/dsh-plugin | 外部 workflow |
| 4661 | zhu1090093659/dsh-web-ui#packages/dsh-web-ui-all | 原生 UI 头名 |
| 3152/2216/2009 | modlens / DSH-better-sidebar / dsh-TUI | 原生 vision/ui 头部 |
| 1100 | dsh-market/dsh-market | 官方市场本体 |

两个结构性结论:

1. **星标 Top3 全是外部成熟大项目"顺手接进来"**——它们的 star 是多年存量,不是在这个两周生态里挣的。大厂与知名开源项目正把 DSH 当作一个值得挂一条 integration 的分发渠道,这是 harness 打开度的最硬证据。
2. **原生头部集中在 ui/vision 层且被下载量独立印证**:npm 月下载 top8(dsh-market 82491、modlens 63829、web-ui-all 59648、better-sidebar 39717、vision-router/vision-toolkit/TUI…)与原生星标名单几乎重合。npm 覆盖 624 条、中位月下载仅 514——同样是极端金字塔,但塔尖一致说明头部是真的有人在用。

## 4. 给追踪者的启示

- 判断"生态在往哪走",盯三条曲线即可:每日新增总量(降温→饱和?)、ui 占比(壳的军备竞赛何时到顶)、外部大项目接入条数(平台合法性的滞后指标);
- 成熟度评估别看星标中位数——本生态里它几乎无判别力,头部用 npm 下载 × 是否外部接入双指标更有效;
- 下次 upstream 同步后重跑 `python3 _digested/ecosystem/census.py`,把 ③ 节日表与本文件对照追加新行,即可看到趋势拐点。
