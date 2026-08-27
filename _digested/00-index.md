# `_digested` — awesome-dsh-plugin 消化

这个目录消化两件事:**插件生态本身**(主轴——里面有什么、谁在做、往哪走),以及注册表的运转机制(辅助——数据和结论可信度的基础)。它不是使用指南,也不是给 upstream 的补丁。

> **审计基线**:awesome-dsh-plugin `main@5e7dc7ebdfe538e89be20c7a34879a91e5fd2c1e`(2026-08-27)。每次同步产品源码后,在 [`_change_log/`](./_change_log/00-index.md) 记录范围,并按 [`_coverage/`](./_coverage/00-index.md) 逐专题复核;ecosystem 各文档要求重跑 [`ecosystem/census.py`](./ecosystem/census.py) 刷新数字。

## 分支纪律

| 分支 | 上面有什么 |
|------|------------|
| `main` | 干净的 upstream 镜像。不放研究材料,不改产品代码。 |
| `ethan` | 研究分支。源码随 `upstream/main` merge 进来；研究材料位于 `_digested/` 和 `_faq_on_digested/`。 |

同步方式：在 `ethan` 上非快进 merge `upstream/main`，让产品源码对齐新基线并保留研究目录，再按 `_change_log/` 审计过期结论。

## 主轴:`ecosystem/` — 插件生态全景

回答"这个生态里有什么、正在发生什么":

- [ecosystem/00-map.md](./ecosystem/00-map.md) — 全景导读:DSH 是什么、头条事实(14 天长出 2286 条)、两套坐标系、方法精度声明
- [ecosystem/01-scenario-taxonomy.md](./ecosystem/01-scenario-taxonomy.md) — **按场景分**:官方 22 类逐类透视 + 重聚十个场景带
- [ecosystem/02-tech-landscape.md](./ecosystem/02-tech-landscape.md) — **按技术分**:34 个技术标签、模型阵营格局、多模态外挂模式
- [ecosystem/03-growth-maturity.md](./ecosystem/03-growth-maturity.md) — 演化节奏、作者结构(单件作者 vs 工作室)、成熟度金字塔

## 辅助参考:机制专题

理解收录数据的来源与可信度时再读(不是本消化的目标方向):

| 目录 | 聚焦 | 一句话 |
|------|------|--------|
| `system/` | 全局运转图 | 一条 PR 从提交到出现在 README/站点要流经哪些环节 |
| `registry-data/` | 数据模型 | `data/plugins/*.yml` 是事实源，各 JSON 边车各自记录什么 |
| `readme-pipeline/` | README 生成 | `generate-readme.mjs` 怎么把 YAML 变成中英双语 README |
| `site-surface/` | 站点 | 模板、多语言资产怎么从同一份数据长出网站 |
| `submission-gates/` | 提交与门禁 | 五条 workflow、check-submission / check-bleed 构成的准入机制 |
| `probes-and-decay/` | 探针与衰减 | probe-* 家族采集哪些遥测(stars/downloads 正是 ecosystem 的数据源)，列表腐烂怎么被发现 |

## 横切目录

| 目录 | 用途 |
|------|------|
| `ecosystem/census.py` | 生态普查脚本,每次同步后重跑刷新 ecosystem 数字 |
| `_coverage/` | 覆盖矩阵，按源码组追踪 digest 覆盖状态 |
| `_change_log/` | 上游同步记录，变更摘要与资料审计 |

## 每个专题内部的结构

- `00-map.md`:按主干顺序阅读的**概念导读**，只建立职责、关系和阅读入口；状态为「未消化」时只承诺范围。
- 编号正文(如 `01-xxx.md`):按问题查找的**机制参考**，记录数据结构、算法、失败行为和源码入口(标 commit hash)。
- 引用规范见各正文顶部；文件一律不叫 `README.md`,避免与产品文档语料混淆。

## 验证

修改本目录或 `_faq_on_digested/` 后运行：

```sh
node _digested/verify.mjs
```

该检查验证 Markdown 的严格 UTF-8、LF 换行与单个结尾换行，以及相对链接与锚点确实存在。
