# `_leverage` — 杠杆层(两册)

> **这一层回答同一个问题**:*同样是不改上游,谁撬得更深?*
> 2026-10-31 从 `_digested/` 出册独立:两册同源、同一套证据纪律,只是**分析单位**不同。

## 两册分工

| 册 | 标语 | 分析单位 | 回答什么 |
|---|---|---|---|
| [`leverage/`](./leverage/README.md) | *Who can touch what; where is the gate; which boundary does it cross?* | **一个机制位置**(接缝 / 门禁 / 控制点) | 对上游的杠杆有多大:协作跨哪条边界、门禁装在哪一环、谁强制权限 |
| [`leverage-reshape-product/`](./leverage-reshape-product/README.md) | *From a plugin to a profile to an app.* | **一个产品样本**(插件 / profile / 应用) | 怎么把 DSH 装成产品:发插件、发一整套 bundle,还是自带宿主 |

**两册平级,不合并。** `leverage/` 问「改到多深、付什么代价」;`leverage-reshape-product/` 问「用户从哪进来、看到什么默认值、坏了谁负责」。同一份 DSH,前者看机制,后者看交付物。

## 怎么读(只挑一条)

| 你要… | 去哪 |
|---|---|
| 判断一个插件占了哪个位置、影响面多大 | [`leverage/horizon.md`](./leverage/horizon.md) → 对应三域 README |
| 抄一条协作 / 门禁 / 权限的现成做法 | [`leverage/BORROW.md`](./leverage/BORROW.md) |
| 判断一个东西该发插件、发 profile 还是发应用 | [`leverage-reshape-product/README.md`](./leverage-reshape-product/README.md) §4 的三步判定 |
| 找某个产品/插件的坐标 | [`leverage-reshape-product/catalog.md`](./leverage-reshape-product/catalog.md) |
| 查「它为什么还没成卡」 | 两册各自的 `BACKLOG.md` |

**不要从目录树开始通读。** 两册都有 BORROW(按需求路由)与 catalog(全量清单)。

## 目录

```text
_leverage/
├── README.md                        ← 本文件(两册共同入口,固定名)
├── verify.mjs                       ← 自包含校验器(只读本目录)
├── leverage/                        ← 三域:协作 / 门禁 / 权限
│   ├── README.md  00-map.md  horizon.md  BORROW.md  catalog.md
│   ├── lever-cross-boundary/  lever-prove-output/  lever-draw-limit/
│   └── _证据/
└── leverage-reshape-product/        ← 产品线:plugin / profile / shell
    ├── README.md  00-map.md  horizon.md  BORROW.md  BACKLOG.md  catalog.md
    ├── plugin/  profile/  shell/
    └── _证据/
```

## 共同纪律(两册一致)

1. **证据四标签**:`[DSH]`(上游包与版本)/ `[CAT]`(`data/plugins/*.yml` 原文)/ `[OBS]`(观察者判断,带反例)/ `[OPEN]`(待核)。每条断言都要挂一个。
2. **三种数不可互证**:★(GitHub API,带时点)/ npm 近 30 天下载(含 CI 与镜像)/ 仓库边车快照(只作历史对照)。卡片页头必须写时点。
3. **先过门,再立卡**:卡片数随「机制被验证」涨,不随名单涨。两册的准入分开写——`leverage/horizon.md` 管三域,`leverage-reshape-product/00-map.md` §7 管三个 lever 的影响力门槛。
4. **骨架不随样本长**:固定名(`README` / `00-map` / `horizon` / `BORROW` / `BACKLOG` / `catalog`)+ 卡片 `NN_` 编号;新增的是叶子。

## 自包含边界

**这一层是自包含的**:两册的骨架(`README` / `00-map` / `horizon` / `BORROW` / `catalog` / `BACKLOG`)、规则源、证据与校验器全部在这棵树里。唯一的运行入口是 `node _leverage/verify.mjs`,它只读 `_leverage/` 内的 Markdown——**不 import 外部脚本,不读外部数据文件**。

它与仓库同级的 `_digested/` 是两层并列的研究,不是上下游:

- `_digested/` 收**生态事实**(有什么、结构怎么变)与**上游机制**(名单数据、投稿门禁、探针衰减);`_leverage/` 收**影响面判断**。
- 两册都**不重复分类计数**:引用外部数字时带日期与口径,不重算。
- 跨目录只写文档链接;链接失效不会影响本层的校验与阅读。

## 验证

```sh
node _leverage/verify.mjs
```

**自包含的一支校验器**,只读 `_leverage/` 这一棵树:严格 UTF-8 / LF、相对链接与锚点、两册的 frontmatter 契约(路径绑定 `domain`)、产品线 `catalog.md` 与目录 Markdown 集合双向一致、三个 lever README 卡表覆盖本 lever 全部编号卡、门槛数字与 `00-map` §7 同数、卡片页头影响力过门槛(或标"机制例外")。不读 `_digested/` 的脚本,也不依赖任何外部数据文件。
