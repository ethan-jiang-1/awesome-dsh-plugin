---
title: "00_map · 产品线宪章"
domain: reshape-product
kind: charter
positioning: "产品线单一规则源：目录、命名、frontmatter、证据、影响力口径与维护流程。"
read_when: "要新增/改名/合并产品线文件；或怀疑某条口径与别处冲突。"
status: living
updated: 2026-10-31
budget: 210
---
# 产品线宪章

> **单一规则源。** [`README.md`](./README.md) 只做入口，[`01_领域模型`](./01_领域模型-七层与命名约定.md) 只做七层与接缝；**三条口径冲突时，以本文件为准**。
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
├── 00_map.md                          ← 规则源（0N = 产品线级文档）
├── 01_领域模型-七层与命名约定.md
├── 02_公共产出-18条.md
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

## 3. 命名：`NN_` 一种前缀

| 对象 | 规则 | 例 |
|---|---|---|
| 根：结构件 | 固定名，**不编号** | `README.md`、`catalog.md` |
| 根：产品线文档 | `0N_`（0–9 共 10 个位） | `00_map.md`、`01_领域模型-七层与命名约定.md`、`02_公共产出-18条.md` |
| lever 目录 | 小写单词，**不带父目录前缀** | `plugin/`、`profile/`、`shell/` |
| 卡片 | `NN_关键短语-插件名.md`；**十位 = 类别，个位 = 该类第几张** | `plugin/11_薄基座-dock.md`、`shell/14_终端即产品-dsh-TUI.md` |
| 证据 | `_证据/NN_主题-原始挖掘.md`；NN 是该 lever 内的序号 | `shell/_证据/01_桌面与终端-原始挖掘.md` |

**四条硬规矩**：

1. **前缀只有一种形状**：`NN_`。十位是类别（§4），个位是槽位；`0N_` 只给产品线级文档。
2. **每类预留 10 个槽位（0–9）**。超过 9 张就是"这一类太挤"的信号：**先拆类，不扩位数**。
3. **文件名发布后不改**（外链稳定）；退役把十位改成 `9`（如 `91_`），`status` 改 `open`，并在 README 留一行。
4. **不要重复父目录**（禁止 `leverage-reshape-product/lever-reshape-product-plugin/`）；**关键短语取机制**（`薄基座`、`全家桶`、`终端工作区`），插件名放最后。

## 4. 类别：十位数字

**读文件名先看十位**；它回答"这一类卡在问什么"，不表示先后。

| 十位 | 类别 | 问什么 | 本线现有（个位 0–9） |
|---|---|---|---|
| `0` | **产品线级文档**（不进 lever） | 规矩、七层、公共产出 | `00_`–`02_` |
| `1` | 壳与工作台（2/3 层） | 人坐在哪张桌子前？ | plugin `11_`–`12_` · profile `11_`–`14_` · shell `11_`–`15_` |
| `2` | 内容形态（3/4 层） | 答案本身长什么样？ | plugin `21_` |
| `3` | 驾驶舱（3 层） | 看不见的东西怎么被看见？ | plugin `31_` |
| `4` | 上手（6 层） | 第一次打开看到什么？ | plugin `41_` |
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
| `README.md` | index | 三条路线怎么选、怎么读 | 具体机制、样本细节 |
| `00_map.md` | charter | 规矩（本文件） | 样本结论 |
| `01_领域模型` | charter | 七层、C1–C4、编号、13 行接缝 | 单个样本的机制 |
| `02_公共产出-*.md` | guide | 跨 lever 的可搬走规则 | 只适用于一个 lever 的清单 |
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

**卡片页头必须写时点**；同一张卡里不许拿快照数字冒充实时。注意：本线三个 lever 的取数时点**不一致**——`plugin` / `shell` 多数仍是 2026-08-19 快照，`profile` 是 2026-10-31 实时。**跨卡比较前先看页头日期**。

**证据深度（卡片页头写一句）**：

| 级别 | 含义 | 能支撑什么结论 |
|---|---|---|
| **README 级** | 只读 README / 文档 | 机制"声称"与产品形态；不能断言实现细节 |
| **源码级** | 读过上游或仓库源码、有文件:行号 | 接缝语义、默认值、失败路径 |
| **实测级** | 跑过安装 / 启动 / 失败路径 | 兼容性、半挂载、降级行为 |

只在 README 上下的结论，写"README 级核过"，不要写成"机制已核"；升级证据级别时同步改页头与 `_证据/`。

**门槛**：`plugin` / `shell` 过门的 C1–C4；**`profile` 额外要求 npm 近 30 天 ≥ 3,000 或 ★ ≥ 200**（聚合包星标普遍虚低）。

## 8. lever 归属（一个样本只进一个）

```text
能 `dsh plugin --profile <任意> add` 吗？
  ├─ 能，但只是加一块能力 ───────────────────→ plugin

  ├─ 能，一整套（聚合/单包多内核/组合补丁）+ ≥2 项产品化，浏览器交付 ─→ profile
  └─ 不能（全局 CLI / 安装包 / 自带运行时 / 换表层）→ shell
```

- **按交付物判，不按技术栈判**：同样用 Tauri，打包成 exe 的进 `shell`，装进 profile 的进 `profile`；
- **跨界能力写在卡里**，不复制卡；
- **两边都像时**，问"用户是把它当插件装，还是当产品用"。

## 9. 公共产出放哪

- **跨 lever 的**规则清单 → 根目录 `0N_*`（当前只有 `02_公共产出-18条.md`）；
- **单个 lever 的**"必抄 N 条" → 该 lever README 的 §4；
- 不要把跨 lever 的清单塞进某个 lever 的 README。

## 10. 维护流程

| 动作 | 步骤 |
|---|---|
| **新增样本** | 过门 → 判 lever（§8）→ 建卡（照抄同类的 frontmatter 与骨架）→ `catalog.md` 补一行 → lever README 卡表补一行 |
| **新增 lever** | 必须同时满足：交付物不同 + ≥2 个过门样本 + 现有三 lever 都装不下 → 加目录、README、本文件 §2/§4/§8、`catalog.md` |
| **退役/被替代** | 把十位改成 `9`（如 `91_...`），`status` 改 `open`，在 `takeaway` 写明被谁替代；**不删、不改名** |
| **改名** | 先全仓改链接，再改文件名；改完跑 `verify`；对外链接优先于内部整齐 |
| **改口径** | 只改本文件与 `01_领域模型`；各 lever README 是摘要，不重复定义 |
| **同步上游** | 只改受影响卡的 `updated` 与 `[DSH]` 断言；`ecosystem/`、`_coverage/` 走原流程 |
| **验证** | `node _digested/verify.mjs`（同时校验 `leverage/` 与 `leverage-reshape-product/`） |

## 11. 找样本、继续挖

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
