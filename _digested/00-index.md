# `_digested` — awesome-dsh-plugin 源码消化

这个目录是对 awesome-dsh-plugin 仓库的**消化分析**：理解一个插件注册表(awesome list)如何用数据、生成管线和 CI 门禁把自己维护下去。它不是使用指南，也不是给 upstream 的补丁。

> **产品源码审计基线**:awesome-dsh-plugin `main@5e7dc7ebdfe538e89be20c7a34879a91e5fd2c1e`(2026-08-27)。每次同步产品源码后，在 [`_change_log/`](./_change_log/00-index.md) 记录范围，并按 [`_coverage/`](./_coverage/00-index.md) 逐专题复核。

## 分支纪律

| 分支 | 上面有什么 |
|------|------------|
| `main` | 干净的 upstream 镜像。不放研究材料，不改产品代码。 |
| `ethan` | 研究分支。源码随 `upstream/main` merge 进来；研究材料位于 `_digested/` 和 `_faq_on_digested/`。 |

同步方式:在 `ethan` 上非快进 merge `upstream/main`,让产品源码对齐新基线并保留研究目录，再按 `_change_log/` 审计过期结论。

## 与同级目录的关系

| 目录 | 本质 | 受众 |
|------|------|------|
| **`_digested/`** | 源码消化，机制剖析 | 想彻底搞懂注册表背后发生了什么的人 |
| `_faq_on_digested/` | 跨消化材料的二次研究 | 我自己(产出者) |

本仓库不另做用户手册。怎么提交插件、怎么过门禁，仍读 `contributing.md` 和各 workflow 本身。

## 子目录

专题按 **这个仓库自己的主轴** 切：数据是唯一事实源，README / 站点都是生成物，质量靠 CI 门禁和探针维持。不按 `scripts/` 文件名平铺成货架。

| 目录 | 聚焦 | 一句话 |
|------|------|--------|
| `system/` | 全局运转图 | 一条 PR 从提交到出现在 README/站点要流经哪些环节 |
| `registry-data/` | 数据模型 | `data/plugins/*.yaml` 是事实源，四个 JSON 边车各自记录什么 |
| `readme-pipeline/` | README 生成 | `generate-readme.mjs` 怎么把 YAML 变成中英双语 README,双语配对怎么保证 |
| `site-surface/` | 站点 | `build-site.mjs`、模板、多语言资产怎么从同一份数据长出网站 |
| `submission-gates/` | 提交与门禁 | 五条 workflow、check-submission / check-bleed、PR/Issue 模板构成的准入机制 |
| `probes-and-decay/` | 探针与衰减 | probe-* 家族从外部采集什么遥测，scan-decay 怎么发现列表腐烂 |
| `_coverage/` | 覆盖矩阵 | 维护用索引，按源码组追踪 digest 覆盖状态 |
| `_change_log/` | 上游同步记录 | 每次 upstream 合入后的变更摘要与资料审计 |

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
