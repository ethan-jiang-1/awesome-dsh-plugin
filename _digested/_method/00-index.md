# `_method` · 方法与纪律

> 横切目录(同 [`_change_log/`](../_change_log/00-index.md)、[`_coverage/`](../_coverage/00-index.md) 级别):收录**跨专题的方法论**——怎么拿到可信数据、怎么保证结论不烂。它们不描述 DSH 是什么,描述"我们的结论是怎么来的、何时会失效"。

## 为什么这个目录重要

`_digested/` 的所有数字都建立在**数据源选择**之上,而数据源本身会骗人:

- 仓库边车是冻结快照(0001 实测:15 天 3213 commits,下载榜数字纹丝不动);
- 上游 catalog 的 npm 发布会停(09-08 后停更);
- 公开 API 有网络可达性、限流、包名撞名三层坑,每层都能让结论**静默**出错
  (不是报错,是给你一个看似合理的错数字)。

这些对策不沉淀下来,下次同步就是重新踩一遍;更危险的是不知道要踩,直接引用了被污染的数字。所以方法档案与数据文档同级、且优先级更高。

## 目录

| 文件 | 内容 | 什么时候必读 |
|------|------|--------------|
| [01-fresh-probe](01-fresh-probe.md) | 自采管线:新鲜下载/星标怎么来,七(六+一)个坑与对策,运行方式与快照目录 | 引用任何下载/星标数字之前;跑 [`fresh_probe.py`](../ecosystem/fresh_probe.py) 之前 |

## 数据源层级(30 秒版)

| 层 | 可信度 | 用途 |
|----|--------|------|
| 仓库边车 `data/*.json` | 冻结快照(0002 复核:downloads 的 624 行 checkedAt 全停在 2026-08-19)| 历史锚点,不可用于趋势 |
| npm `dsh-plugin-catalog` 包 | 每夜但会停 | 备用基线(已转储于 `_snapshots/catalog-*.json`) |
| **自采管线 `fresh_probe.py`** | 实时 | 趋势主数据源 |

## 研究工具自身的修复(0002)

两份自研脚本本轮都修过——修的都是"会**静默**出错"的地方,不是崩掉的地方:

- [`census.py`](../ecosystem/census.py):(a) 行内注释污染——手写 YAML 子集解析器不剥 ` # 注释`,两条把 PR 模板注释粘进 `category:` 行的投稿会凭空造出两个类目(js-yaml 读作 tools/model,所以能合并进来);(b) 新增 ⑧ 节把「新队列 vs 存量」的类目漂移口径**落盘**(0001 时该表结论在 04,口径却不可复现)。
- [`fresh_probe.py`](../ecosystem/fresh_probe.py):长尾回源的四个连环坑(未捕获的 `RemoteDisconnected`/`IncompleteRead`、"未知"被写进缓存固化成"未发布"、缓存只在整轮跑完才落盘、DNS 卡死时 `urlopen` 的 timeout 不生效)。细节见 [01 §3 坑 7](01-fresh-probe.md)。

## 预留位

- census.py 的标签正则口径与已知误报史(暂记于 [ecosystem/02](../ecosystem/02-tech-landscape.md) 方法注记);
- 机制专题"逐行核验"的复核流程(暂记于 [`_coverage/`](../_coverage/00-index.md));
- 上游同步的取数通道对策(0002 已更新为"先 ls-remote 探活,再用带低速阈值的 https fetch",见 [`_change_log/00-index`](../_change_log/00-index.md));
- **0002 新增**:`data/capabilities.json` 的口径边界(静态扫描、不执行代码、不判意图)与它的"提交但无回写"持久化怪状(暂记于 [probes-and-decay/00](../mechanics/probes-and-decay/00-map.md))。

以上内容如果继续生长,提升为本目录正式条目。
