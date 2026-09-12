# `_digested` — awesome-dsh-plugin 消化

> 站位声明:我是**评估者**,不是贡献者。关心的是这东西有什么用、生态长什么样、数据可不可信——不学怎么投稿、不复刻它的门禁。本目录的结构就按这个视角组织。

**产品**:DSH = DeepSeek Harness(`deepseek-ai/deepseek-harness`,官方开源 agent 框架,"一切皆插件");本仓库是它的社区插件目录,`dsh plugin add` 安装制。
**审计基线**:`main@38976afdb5f70d1bcd1dfd5ed0e50e5a3a559fd4`(2026-09-11;0001 次同步,见 [`_change_log/`](./_change_log/00-index.md)。ecosystem 正文数字仍为旧基线 5e7dc7eb 的快照,复核前引用需注意)。

## 读法(只有两站)

### 第一站 · [`ecosystem/`](./ecosystem/00-map.md) — 生态全景(主轴)

回答"这里头有什么、正在发生什么":

| 文件 | 回答什么 |
|------|----------|
| [00-map](./ecosystem/00-map.md) | 全景导读 + 头条事实(14 天长出 2286 条)+ 方法精度声明 |
| [01-scenario-taxonomy](./ecosystem/01-scenario-taxonomy.md) | **按场景分**:22 类逐类透视 → 重聚十个场景带("做壳" vs "做增强") |
| [02-tech-landscape](./ecosystem/02-tech-landscape.md) | **按技术分**:34 个技术标签、模型阵营、多模态外挂、成本品类 |
| [03-growth-maturity](./ecosystem/03-growth-maturity.md) | 演化节奏、作者结构、成熟度金字塔与外部巨头接入 |
| [04-value-trend](./ecosystem/04-value-trend.md) | **价值定位与趋势**(catalog 双快照):头部在哪、增量流向、优秀插件特征 |

数字全部可重跑复现:`python3 _digested/ecosystem/census.py`(仅标准库)。

### 第二站 · [`mechanics/00-map.md`](./mechanics/00-map.md) — 机制速览(一页)

只回答评估要用的三个问题:名单数据可信吗 / 会不会烂 / 什么量级。**到此为止即可**;其下六个子目录(`system`、`registry-data`、`submission-gates`、`readme-pipeline`、`site-surface`、`probes-and-decay`)是逐行机制档案,投稿者或复现构建时才需要。

## 横切目录

| 目录 | 用途 |
|------|------|
| [`_coverage/`](./_coverage/00-index.md) | 覆盖矩阵:各专题消化到什么程度 |
| [`_change_log/`](./_change_log/00-index.md) | 上游同步记录:每次合入后哪些结论要复核 |

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
