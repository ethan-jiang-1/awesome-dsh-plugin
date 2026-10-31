# `_digested` — awesome-dsh-plugin 消化

> 站位声明:我是**评估者**,不是贡献者。关心的是这东西有什么用、生态长什么样、数据可不可信——不学怎么投稿、不复刻它的门禁。本目录的结构就按这个视角组织。

**产品**:DSH = DeepSeek Harness(`deepseek-ai/deepseek-harness`,官方开源 agent 框架,"一切皆插件");本仓库是它的社区插件目录,`dsh plugin add` 安装制。
**审计基线**:`main@efe602e7b`(2026-10-31;0005 同步记录见 [`_change_log/`](./_change_log/00-index.md))。生态结构统计已按 **7924 条**重算;本轮上游源码零 diff,六个机制专题按「无对应 diff」核验(submission-gates 另有 `contributing.md` 文档段);下载/星标尚未重采,仅保留带日期的历史值(仓库边车冻结于 2026-08-19)。

## 读法(三站)

### 第一站 · [`ecosystem/`](./ecosystem/00-map.md) — 生态全景(主轴)

回答"这里头有什么、结构如何变化":

| 文件 | 回答什么 |
|------|----------|
| [00-map](./ecosystem/00-map.md) | 全景导读 + 0005 更新后的 7924 条结构基线、分类/作者/标签画像及历史热度数据时效说明 |
| [01-scenario-taxonomy](./ecosystem/01-scenario-taxonomy.md) | **按场景分**:23 类逐类透视 → 重聚十一个场景带("做壳" vs "做增强")+ 新队列漂移 |
| [02-tech-landscape](./ecosystem/02-tech-landscape.md) | **按技术分**:34 个技术标签(7924 当前基线)、模型提及、多模态/成本特征、历史能力披露快照 |
| [03-growth-maturity](./ecosystem/03-growth-maturity.md) | 演化节奏与作者结构(7924 当前基线);成熟度/星标仍是带日期的历史快照 |
| [04-value-trend](./ecosystem/04-value-trend.md) | 当前结构与数据时效边界;头部/下载转化仍为 2026-09-12 或更早的历史观测,不可外推 |

数字全部可重跑复现:`python3 _digested/ecosystem/census.py`(仅标准库);新鲜下载/星标走 [`fresh_probe.py`](./ecosystem/fresh_probe.py)(方法见 [`_method/01`](./_method/01-fresh-probe.md))。

### 第二站 · [`mechanics/00-map.md`](./mechanics/00-map.md) — 机制速览(一页)

只回答评估要用的三个问题:名单数据可信吗 / 会不会烂 / 什么量级。**到此为止即可**;其下六个子目录(`system`、`registry-data`、`submission-gates`、`readme-pipeline`、`site-surface`、`probes-and-decay`)是逐行机制档案,投稿者或复现构建时才需要。

### 第三站 · [`leverage/`](./leverage/README.md) — 影响面与杠杆(第二轴)

`ecosystem/` 按「是什么」分类;这一层按「**改了多大、多深、留了什么代价**」提问,四个域并列、无先后:

| 目录 | 标语 | 回答什么 |
|------|------|----------|
| [lever-reshape-product](./leverage/lever-reshape-product/README.md) | 不改上游,DSH 能被组装成什么产品 | 产品栈七层;产品化的单位是 profile 不是插件 |
| [lever-cross-boundary](./leverage/lever-cross-boundary/README.md) | 协作跨到哪个边界,每跨一界多付什么 | 四道边界与其各自的税(状态归属/冲突裁决/失败收敛) |
| [lever-prove-output](./leverage/lever-prove-output/README.md) | 门禁装在哪一环,产物凭什么算完成 | 质量链六环;只有检查点与版本新鲜度是原生硬门禁 |
| [lever-draw-limit](./leverage/lever-draw-limit/README.md) | 谁能碰什么,由谁强制,留下什么证据 | 信任三层;沙箱只覆盖文件,网络与进程无策略词汇 |

**入口**:[`leverage/README.md`](./leverage/README.md) 首屏有三条路——拿走东西去 [BORROW.md](./leverage/BORROW.md),查某一篇去 [catalog.md](./leverage/catalog.md),知道凭什么去 [horizon.md](./leverage/horizon.md)。四域成稿;**先过门再立卡,卡片数不随名单涨**。准入/分级见 horizon,**不维护全库计数与命中率**。

## 横切目录

| 目录 | 用途 |
|------|------|
| [`_coverage/`](./_coverage/00-index.md) | 覆盖矩阵:各专题消化到什么程度 + 研究工具自身的修复记录 |
| [`_change_log/`](./_change_log/00-index.md) | 上游同步记录:每次合入后哪些结论要复核(含取数通道对策) |
| [`_method/`](./_method/00-index.md) | **方法与纪律**:数据从哪来、坑在哪(引用下载/星标数字前必读) |

## 分支纪律

| 分支 | 上面有什么 |
|------|------------|
| `main` | 干净的 upstream 镜像,不放研究材料 |
| `ethan` | 研究分支;非快进 merge `upstream/main` 同步 |

## 验证

```sh
node _digested/verify.mjs
```

检查严格 UTF-8、LF 与结尾换行、相对链接与锚点。二次研究见同级 [`_faq_on_digested/`](../_faq_on_digested/00-index.md)。
