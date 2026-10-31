---
title: "00-map · 产品线宪章"
domain: reshape-product
kind: charter
positioning: "产品线单一规则源：目录、命名、frontmatter、证据、影响力口径与维护流程。"
read_when: "要新增/改名/合并产品线文件；或怀疑某条口径与别处冲突。"
status: living
updated: 2026-10-31
budget: 280
---
# 产品线宪章

> **单一规则源。** [`README.md`](./README.md) 只做入口，[`horizon`](./horizon.md) 只做七层与接缝；**三条口径冲突时，以本文件为准**。
> 与 [`../leverage/`](../leverage/README.md) 平级：那边回答"对上游的杠杆有多大"，这边只回答"**怎么把 DSH 装成产品**"；本目录不参与三域统计。

---

## 1. 范围

**收**：能改变"人怎么用它"的产品化样本——新入口、新首屏、新默认值、新身份、新分发/上手路径。

**不收**：纯能力增强（多一个工具/provider）；只支持 `0.1.x` 的；上游代码本身的建议（去 `lever-draw-limit` / `lever-prove-output` / `lever-cross-boundary`）。

**不重复**：名单与生态统计在 `ecosystem/`；上游机制在 `mechanics/`；本目录只写"下游怎么把上游装成产品"。

## 2. 目录结构（固定，不再加层级）

```text
leverage-reshape-product/
├── README.md                          ← 入口（固定名，不编号）
├── catalog.md                         ← 全量清单（固定名，不编号）
├── 00-map.md                          ← 规则源（固定名，不编号）
├── horizon.md                         ← 门：七层 + 准入 + 接缝
├── BORROW.md                          ← 跨 lever 的公共产出
├── BACKLOG.md                         ← 快筛不过 / 待深挖的候选
├── _证据/指标快照-2026-10-31.json  ← 跨 lever 的 19 卡指标快照（可复现）
├── plugin/                            ← lever 1
│   ├── README.md
│   ├── 11_薄基座-dock.md … 81_协作-dsh-agent-teams.md
│   └── _证据/01_壳与工作台-原始挖掘.md …
├── profile/                           ← lever 2
│   ├── README.md
│   ├── 11_全家桶-dsh-web.md … 14_聚合补丁-dsh-all.md
│   └── _证据/01_产品聚合-原始挖掘.md
└── shell/                             ← lever 3
    ├── README.md
    ├── 11_桌面应用-dsh-desktop.md … 15_终端工作区-seektty.md、91_冻结分叉-better-sidebar-N23.md
    └── _证据/01_桌面与终端-原始挖掘.md
```

**只有一层 lever。** 除 `_证据/` 外，**不允许在 lever 里再切子目录**；文件多到装不下时，先问"是不是该拆 lever"（§8），不是加目录层级。

## 3. 命名：骨架用固定名，卡片用 `NN_`

| 对象 | 规则 | 例 |
|---|---|---|
| 根：骨架 | **固定名、不编号**，按"回答什么问题"命名 | `README.md`、`00-map.md`、`horizon.md`、`BORROW.md`、`BACKLOG.md`、`catalog.md` |
| lever 目录 | 小写单词，**不带父目录前缀** | `plugin/`、`profile/`、`shell/` |
| 卡片 | `NN_关键短语-插件名.md`；**十位 = 类别，个位 = 该类第几张** | `plugin/11_薄基座-dock.md`、`shell/14_终端即产品-dsh-TUI.md` |
| 证据 | `_证据/NN_主题-原始挖掘.md`；NN 是该 lever 内的序号 | `shell/_证据/01_桌面与终端-原始挖掘.md` |
| 根 `_证据/` | 只放**跨 lever**的可复现数据（如指标快照），不放单卡摘录 | `_证据/指标快照-2026-10-31.json` |

**四条硬规矩**：

1. **骨架不编号**：根目录这六个文件是固定槽位，不再新增 `04_`、`05_`；要加新角色，先问能不能并进 `README` / `00-map` / `horizon` / `BORROW` / `BACKLOG`，不能才改本表。
2. **卡片一种前缀**：`NN_`。十位是类别（§4），个位是槽位；每类预留 10 个位（1–9 有效，0 保留不用），超过 9 张就是"这一类太挤"，**先拆类，不扩位数**。
3. **卡片文件名发布后不改**（外链稳定）；退役把十位改成 `9`（如 `91_`），`status` 改 `open`，并在 README 留一行。
4. **不要重复父目录**（禁止 `leverage-reshape-product/lever-reshape-product-plugin/`）；**关键短语取机制**（`薄基座`、`全家桶`、`终端工作区`），插件名放最后。

## 4. 类别：十位数字

**读文件名先看十位**；它回答"这一类卡在问什么"，不表示先后。

| 十位 | 类别 | 问什么 | 本线现有（个位 0–9） |
|---|---|---|---|
| `0` | **保留**（骨架文档不占卡片编号） | — | — |
| `1` | 壳与工作台（2/3 层） | 人坐在哪张桌子前？ | plugin `11_`–`12_` · profile `11_`–`14_` · shell `11_`–`15_` |
| `2` | 内容形态（3/4 层） | 答案本身长什么样？ | plugin `21_` |
| `3` | 驾驶舱（3 层） | 看不见的东西怎么被看见？ | plugin `31_` |
| `4` | 上手（6 层） | 第一次打开看到什么？ | plugin `42_`–`43_`（`41_` 观察样本在 `_证据/`） |
| `5` | 分发（7 层） | 从哪装、坏了怎么回？ | plugin `51_` |
| `6` | 多端（2/7 层） | 同一份 DSH 怎么上另一块屏？ | plugin `61_` |
| `7` | 感官与模型（4 层） | 模型能感知什么？ | plugin `71_` |
| `8` | 协作（4 层） | 一个会话怎么变成团队？ | plugin `81_` |
| `9` | 反例与退役 | 什么路走不通？ | shell `91_` |

**一个插件只出一张卡**；跨类能力写在卡内，不另开卡。

## 5. frontmatter 契约

**七个必填**：`title` / `domain` / `kind` / `positioning` / `read_when` / `status` / `updated`。

- `domain` **固定 `reshape-product`**（路径绑定，`verify.mjs` 会查）；
- `kind` ∈ `index` / `charter` / `guide` / `playbook` / `card` / `sample` / `evidence`；
- `kind` 为 `sample` / `card` / `playbook` 时**必须**有 `takeaway`，且正文必须有**借鉴节**（标题含 借鉴/搬走/借用/照抄/食谱/配方/移植）——没有就不是产品卡；
- `positioning` ≤120 字、`read_when` ≤80 字、`title` ≤80 字；
- `budget` 写行数上限，超了 `verify` 会给提醒（不是失败）。

## 6. 各类文件的职责

| 文件 | kind | 回答什么 | 不该写什么 |
|---|---|---|---|
| `README.md` | index | 三入口、三条路线怎么选、怎么读 | 具体机制、样本细节 |
| `00-map.md` | charter | 规矩（本文件） | 样本结论 |
| `horizon.md` | charter | 七层、C1–C4、编号、13 行接缝 | 单个样本的机制 |
| `BORROW.md` | guide | 跨 lever 的可搬走规则 | 只适用于一个 lever 的清单 |
| `BACKLOG.md` | index | 候选池：待深挖 / 没过门槛，各留一行 | 结论、机制细节 |
| `catalog.md` | index | 全量文件的 kind/定位/何时读 | 版本号、数字 |
| `<lever>/README.md` | charter | 本 lever 收什么、卡表、坐标、必抄清单 | 别的 lever 的样本 |
| `<lever>/N-*.md` | sample | 一个样本：位置 / 机制 / 体验 / 证据 / 食谱 / 失效 / 开放问题 | 道听途说、无出处的数字 |
| `*/_证据/*.md` | evidence | 原文摘录 + 行号 + 取数时点 | 结论（结论在卡里） |

## 7. 证据与影响力

**四个标签**（每条断言都要挂）：

| 标签 | 含义 |
|---|---|
| `[DSH]` | 原生机制，写清 `@deepseek-ai/<pkg>@<version>` 与文件:行号 |
| `[CAT]` | 生态事实，写 `owner/repo` + `data/plugins/*.yml` 条目 |
| `[OBS]` | 观察者判断，必须给反例或失效条件 |
| `[OPEN]` | 未验证，留给下一轮 |

**三种数字，三种口径，不可互证**：

1. **★**：GitHub API，写时点（如 `2026-10-31`）；
2. **npm 月下载**：`api.npmjs.org/downloads/point/last-month`，含 CI 与镜像，**≠ 用户数**；
3. **仓库快照**：`data/stars.json` / `downloads.json`，**2026-08-19**，只代表当时——已有样本两个月内涨一个数量级。

**卡片页头必须写时点**；同一张卡里不许拿快照数字冒充实时。**本线 21 张卡已于 2026-10-31 统一重采**（★/forks/issues 取 GitHub API，npm 取近 30 天；另 1 个观察样本不占卡位），原始响应存 `_证据/指标快照-2026-10-31.json`；仓库自带的 2026-08-19 快照只作历史对照，不再作为卡片的主口径。

**证据深度（卡片页头写一句）**：

| 级别 | 含义 | 能支撑什么结论 |
|---|---|---|
| **README 级** | 只读 README / 文档 | 机制"声称"与产品形态；不能断言实现细节 |
| **源码级** | 读过上游或仓库源码、有文件:行号 | 接缝语义、默认值、失败路径 |
| **实测级** | 跑过安装 / 启动 / 失败路径 | 兼容性、半挂载、降级行为 |

只在 README 上下的结论，写"README 级核过"，不要写成"机制已核"；升级证据级别时同步改页头与 `_证据/`。

**影响力门槛（2026-10-31 定；任一硬指标达标即可）**：

| lever | 硬指标（任一） | 例外额度 |
|---|---|---|
| `plugin` | ★ ≥ 200 或 npm 近 30 天 ≥ 2,000 | 每 lever ≤ 2 张，标"机制例外" |
| `profile` | ★ ≥ 200 或 npm 近 30 天 ≥ 3,000（聚合包星标普遍虚低） | 同上 |
| `shell` | ★ ≥ 100 或 npm 近 30 天 ≥ 1,000 | 同上 |

**"有影响力"怎么证明**（缺一不立卡）：

| 类型 | 可用证据 | 记录方式 |
|---|---|---|
| **硬指标** | GitHub ★/forks/issues；npm 近 30 天下载；目录收录条目；Releases/安装包存在 | 卡头写 `★ N / npm M（YYYY-MM-DD）` + repo URL |
| **软证据** | 官方文档点名；被其他项目依赖或引用；issue/PR 活跃；稳定发布节奏 | 给可点 URL + 一句"它证明了什么"（不能只写"很火"） |

**例外（机制例外）**：机制独一无二、但等不到影响力时（如 `dock` 的注册表基座、`tauriapp` 的内置运行时）允许成卡，但必须：① 卡头写 `影响力：机制例外`；② 写清"为什么这条机制不可替代"；③ **每 lever ≤ 2 张**——例外超额度说明**门槛定错了，改门槛，不要加例外**。

## 8. 归属：三步判定（一个样本只进一个）

**别从"能不能 add"开始判**——终端 TUI 也能 `dsh plugin add`，但它换的是表层。按顺序问三步：

```text
Q1 用户为了用它，必须启动什么？
  ├─ 终端 / 桌面应用 / 自带运行时 / 安装包 ───────────────→ shell
  └─ 浏览器里的 dsh web（某个 profile） ───────────────→ Q2

Q2 它交付的是"一块能力"，还是"一整套产品形态"？
  ├─ 一块能力：装进现有 profile，默认值/首启/分发仍归宿主或用户 → plugin
  └─ 一整套：自己定默认体验（导航/首页/皮肤/设置）
             或自带分发/更新，或聚合整套 bundle ──────────────→ profile

Q3 有插件入口，但产品不是插件？（如桌面应用的 in-page 半区）
  └─ 看"用户实际运行的是什么"：
       exe / 终端 → shell；浏览器 profile → profile；现有界面里加功能 → plugin
```

**五条 tie-breaker**（争论时按序用）：

| # | 规则 | 例子 |
|---|---|---|
| 1 | **表层优先于安装方式**：能不能 `dsh plugin add` 不作数 | `dsh-TUI` / `seektty` 都能 add，但表层是终端 → shell |
| 2 | **交付物优先于技术栈**：Tauri / Electron 只是实现 | `windowos` 交付 exe → shell；`dsh-web` 交付 bundle → profile |
| 3 | **单包也能是 profile**：重定义了默认体验就算 | `codex-ui` 单包六内核 → profile |
| 4 | **聚合必须"策展 + 共享默认 + 自有更新"**，只堆包不算 | `dsh-suite` / `dsh-all` → profile；纯打包 → 不成卡 |
| 5 | **加一块屏 ≠ 换宿主**：不改宿主表层、只加通道 | `dsh-mobile` → plugin |

**边界回归表**（现有样本必须全部过这张表；新增有争议时先加一行再判）：

| 边界样本 | 判定 | 一句话理由 |
|---|---|---|
| `dsh-TUI` / `seektty` | shell | 表层是终端，不是浏览器 |
| `codex-ui` | profile | 单包，但重定义整套界面与默认值 |
| `better-sidebar` | plugin | 很厚，但只加侧栏工作台，未改默认体验 |
| `dsh-mobile` | plugin | 另起网关，但宿主仍是 `dsh web` |
| `windowos` | shell | 插件只是安装器，产品是 exe |
| `dsh-suite` | profile | 聚合 18 包 + 共享默认 + 整包更新 |
| `dsh-desktop` | shell | 自带 DSH_HOME 与安装包 |
| `dsh-bootstrap` | plugin | 首启面板装在现有 profile 里，不定义新产品 |

## 9. 公共产出放哪

- **跨 lever 的**规则清单 → 根目录 `BORROW.md`（唯一一份）；
- **单个 lever 的**"必抄 N 条" → 该 lever README 的 §4；
- 不要把跨 lever 的清单塞进某个 lever 的 README。

## 10. 维护流程

| 动作 | 步骤 |
|---|---|
| **新增样本** | 过门 → 判 lever（§8）→ 建卡（照抄同类的 frontmatter 与骨架）→ `catalog.md` 补一行 → lever README 卡表补一行 |
| **新增 lever** | 必须同时满足：交付物不同 + ≥2 个过门样本 + 现有三 lever 都装不下 → 加目录、README、本文件 §2/§4/§8、`catalog.md` |
| **退役/被替代** | 把十位改成 `9`（如 `91_...`），`status` 改 `open`，在 `takeaway` 写明被谁替代；**不删、不改名** |
| **改名** | 先全仓改链接，再改文件名；改完跑 `verify`；对外链接优先于内部整齐 |
| **改口径** | 只改本文件与 `horizon.md`；各 lever README 是摘要，不重复定义 |
| **同步上游** | 只改受影响卡的 `updated` 与 `[DSH]` 断言；`ecosystem/`、`_coverage/` 走原流程 |
| **验证** | `node _leverage/verify.mjs`（自包含：两册的 frontmatter/链接/锚点 + 产品线 catalog 与卡表一致） |

## 11. 找样本、继续挖

### 11.1 候选先过 10 分钟快筛

| # | 问题 | 过不了就 |
|---|---|---|
| 1 | 有一条**可复现的装法**（命令或安装包 URL）？ | 进候选池，注明缺什么 |
| 2 | 改动落在 **2/3/5/6/7 层**中的哪一层（用户可见）？ | 纯能力增强 → 不立卡 |
| 3 | **硬指标过 §7 门槛**，或够"机制例外"？ | 进候选池，写复核条件 |
| 4 | 能写出一条"**抄哪一行**"（不是"它很好"）？ | 退回深挖 |
| 5 | repo / npm / 目录条目 / Issue **至少三样能回源**？ | 补证据再判 |

五条全过 → 进入 30 分钟深挖 → 立卡；任何一条不过 → 记进 [`BACKLOG`](./BACKLOG.md)，**不立卡**。

**四个入口，按成本从低到高**：

| 入口 | 怎么用 | URL / 路径 |
|---|---|---|
| 本仓库注册表 | 7,924 条，一条一个 yml；`category` + 双语描述 | `data/plugins/*.yml`（文件名 `owner__repo.yml`）；热度在 `data/stars.json` / `data/downloads.json`（**2026-08-19 快照**） |
| npm | 按关键词搜包；查近 30 天下载 | `https://registry.npmjs.org/-/v1/search?text=dsh&size=250`；`https://api.npmjs.org/downloads/point/last-month/<pkg>` |
| GitHub topic | 生态的自定义标签 | <https://github.com/topics/dsh-plugin> |
| GitHub 搜索 | 按仓库找"整套产品"，或按代码找 bundle 形态 | `https://api.github.com/search/repositories?q=deepseek-harness&sort=stars`；代码搜索：`"dsh.bundle"` / `"dsh.profile"` / `"--profile web add"`（需登录） |

**召回词**（先粗筛"像不像产品级"）：`全家桶`、`整套`、`发行版`、`all-in-one`、`suite`、`bundle`、`launcher`、`installer`、`desktop`、`tauri`、`electron`。

**筛选顺序**：先过 §8 的 lever 判断树 → 再看 §7 的影响力门槛 → 最后只读 README 的 **Quick start / Installation / Requirements / Known limitations** 四节。只读这四节就能判断它是不是产品、能不能抄。

**深挖的标准动作**（一个样本半天）：

1. 装法跑一遍，或读 CI / Releases 确认它真的能装；
2. 找到 `dsh.bundle.patch` / `dsh.profile.bundles` 的实际形态（是追加还是改宿主行）；
3. 抓 2–3 条"坏了怎么回"的代码路径或文档段；
4. 原文 + 行号写进该 lever 的 `_证据/`；
5. 只写"可照抄的一行 + 抄错后果 + 失效条件"——这三样写不出，就退回对照表，不立卡。

**每张卡自带"再深挖去哪"**：样本档案里那一行给出具体文件/章节，下一轮直接从这里开始，不另开清单。

## 12. 反模式（今后最容易头疼的）

1. **一卡两 lever**：同一张卡出现在两个目录 → 两边都会漂。
2. **把"能一键装齐"当 profile 产品**：组合包不等于产品形态。
3. **拿 2026-08-19 的快照当今天**：★/下载都已翻倍甚至百倍。
4. **在 lever 里再开子目录**：层级一深，链接与心智负担同时爆炸。
5. **公共产出塞进 lever**：18 条已经在根目录，不要再复制一份。
6. **卡片没有借鉴节**：那是笔记，不是产品卡。
