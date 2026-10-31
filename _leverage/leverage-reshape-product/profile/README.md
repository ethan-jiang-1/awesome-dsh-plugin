---
title: "profile · profile 即产品"
domain: reshape-product
kind: charter
positioning: "profile 侧宪章：一套 bundle + 默认值 + 首启 + 分发，用 dsh web 在浏览器里启动。七种形态。"
takeaway: "发货单位是 bundle；装成功 ≠ 挂载成功；接管/进口型也要可逆、可诊断。"
read_when: "要做发行版/全家桶；或判断该发插件、发 profile，还是发独立应用。"
status: observed
updated: 2026-10-31
budget: 160
---
# profile · profile 即产品：换个 profile，浏览器里就是另一个产品

> **标语**:*The product is not a plugin — it's a profile.* —— 不发安装包，发一套 bundle;用户 `dsh web --profile <name>` 打开它。
> **分工**:本 lever 只收**浏览器启动的 profile 级产品**;[`plugin` 侧](../plugin/README.md) 收能装进任何 profile 的**客人**;[`shell` 侧](../shell/README.md) 收换表层/自带宿主的**独立应用**。**先分 lever,再看编号。**
> **状态**:`observed`(机制已核) · **基线**:DSH `0.2.1-rc.3` · 名单 @ `efe602e7b` · **指标**:2026-10-31 重采
> **范围**:兼容 **DSH `0.2.x`**;能把一整套 bundle 装进某个 profile,并在浏览器里交付完整体验。
> **借阅入口**:想判归属 → [§2 判据](#2-入桶判据) · 想抄 → [§4 必抄 8 条](#4-profile-侧必抄-8-条) · 想回源 → [§3 坐标](#3-卡表)

---

## 1. 为什么单开这一桶

**因为上游把"产品"的单位改成了 profile。** DSH `0.2` 的架构注记标题就是 *Everything becomes a profile*:

- 一个 **profile** = `$DSH_HOME/profiles/<name>` 目录:`package.json`(依赖 + `dsh.profile.bundles` **有序列表**)+ 用户自己的 `cordis.patch.yml`;
- 一个 **bundle** = 声明了 `"dsh": { "bundle": { "patch": "./cordis.patch.yml" } }` 的 npm 包;
- **组合顺序**:每个 bundle 的 patch 按 `dsh.profile.bundles` 顺序打在**空根**上 → 用户层 → `--patch` → flag patches,一次 `applyEntryPatches` 完成;
- 解析**双锚**:`bundles` 里点名的包先从 dsh 安装解析,再从 profile 的 `node_modules`;裸插件名走父级查找 + `$DSH_HOME/profiles/node_modules` 扁平兜底。

**所以"做一个产品"= 发一个 bundle(带 patch)+ 让用户把它加进 bundles 列表**,而不是做新 bin、也不是改上游。第 5/6/7 层(默认值/首启/分发)全部落在**你那个 patch 文件**与**你那个包里**。

> **名字的例外**:`desktop` 这个名字被保留给官方 Electron 应用(CLI 直接拒绝 boot 与 config-dump,`README.md:20`;`lib/bin.js:36`)。**做 profile 产品时,别碰这个名字。**

## 2. 入桶判据

**与 [`00-map` §8](../00-map.md) 是同一套三步判定。** 本桶 = 三步判定的 **Q1「浏览器」+ Q2「一整套」** 分支。

- **主问**：它自己定义默认体验（导航 / 首页 / 皮肤 / 设置），或自带分发与更新，或聚合整套 bundle，或**按 preset 换掉宿主自带实现**，或**把别人的套件当分发单位**？
- **门槛**：★ ≥ 200 或 npm 近 30 天 ≥ 3,000；机制例外每 lever ≤ 2 张（见 [`00-map` §7](../00-map.md)）。
- **三条边界**：
  - **单包也能进**——`12_界面套件` 是一个包，但重定义了整套界面与默认值；
  - **聚合要"策展 + 共享默认 + 自有更新"**——`13_组合包` / `14_聚合补丁` 算，纯打包不算；
  - **接管也要算**——按 preset 停掉宿主自带行、换成自己的实现（`15_接管套件`），比"再加一个能力"更接近产品；
  - **进口也要算**——把别的 agent 的套件就地读成可安装单位（`16_套件市场`），分发单位可以不是自己的 bundle；
  - **闭环也要算**——一个 bundle 正好装一条用户闭环（`17_闭环装配`），边界不是"功能组"而是"做完一件事"；
  - **自带运行时不算**——`oh-dsh` 的 Web 只是三种界面之一 → [`shell` 侧](../shell/README.md)。

> **怎么加卡**：过 00-map §11.1 快筛且门槛达标 → 读 patch/bundle 形态 → 按 00-map §5 建卡 → catalog 与本表各补一行 → `node _leverage/verify.mjs`。

> **每张卡开头都是「它想干什么 · 为什么值得借鉴」**：意图 / 意义 / 用户价值 / 表达（界面与交互）——先回答“为什么要看它”，再进机制。

## 3. 卡表

**按 npm 近 30 天下载排序。** 七张卡是**七种形态**——前四种是"怎么把自己的东西装成一件",后三种是"换宿主 / 进口别人的 / 装一条闭环"。

| 卡 | 产品 | npm 月下载 | ★(2026-10-31) | 判据 | 形态 | **能借鉴什么** |
|---|---|---|---|---|---|---|
| [`界面套件`](./12_界面套件-dsh-codex-ui.md) | `MichengAI/dsh-codex-ui` | **119,610** | 250 | F1(单包多内核)·F2·F3(默认值/共存) | 单包六微内核,重做整套界面 | 子插件独立启停;fail-closed 清理(0 DOM);只吃官方 primitive/slot |
| [`全家桶`](./11_全家桶-dsh-web.md) | `zhu1090093659/dsh-web` | **99,694** | 9,865 | F1·F2·F3(四项全中) | 20+ 自研 bundle + 自家商店 | 发货单位是 bundle;`exit 0` 但 bundles 为空 = 静默半挂载;默认皮肤即身份 |
| [`闭环装配`](./17_闭环装配-better-session.md) | `morlay/dsh-plugin` | **8,561** | 9 | F1(闭环)·F2·F3(行+配置同居) | 一个 bundle 装配一条闭环（改/重试/撤回/分支） | 装配数据（`rows`）是发布物;只挂官方槽位不 fork;preset 行清单可归包 |
| [`组合包`](./13_组合包-dsh-suite.md) | `STARDUSTLC666/dsh-suite` | **8,230** | 3 | F1·F2·F3(默认值/更新) | 18 个独立插件 + 共享默认配置 | 固定组件版本;整包更新;扁平化无 git 子依赖 |
| [`接管套件`](./15_接管套件-dsh-plugins-plus.md) | `sidleo/dsh-plugins-plus` | **6,094** | 0 | F1(按 preset)·F2·F3(默认值) | 按 preset 停掉宿主自带行，换成 `-plus` 行 | 接管 = 停原行+加己行;回退是删覆写行;`unset` 才是默认 |
| [`套件市场`](./16_套件市场-dsh-agent-plugins-market.md) | `Sivan757/dsh-agent-plugins-market` | **4,752** | 19 | F1(十种布局)·F2·F3(分发/凭据) | 把别的 agent 的套件就地读成可安装单位 | 套件是安装单位;就地读不转换;坏声明诊断后跳过;缺凭据显式化 |
| [`聚合补丁`](./14_聚合补丁-dsh-all.md) | `hyzyn/dsh-plugin-kit` | **3,558** | 59 | F1·F2·F3(默认值/更新/管理) | 一条 bundle patch 挂 11 个插件 | 聚合包应是纯数据;共享库不进 bundles;Profile 管理卡片 |

**影响力门槛以 [`00-map` §7](../00-map.md) 为准**：本桶额外要求 npm 近 30 天 **≥ 3,000** 或 ★ **≥ 200**（聚合包星标普遍虚低）。低于门槛的只进 §5 普查表,不单独成卡。

**口径摘要**（详见 `00-map` §7）:npm 月下载取 `api.npmjs.org/downloads/point/last-month`(2026-09-30 ~ 10-29),**含 CI 与镜像**;★ 取 GitHub API(2026-10-31);仓库 `downloads.json`/`stars.json` 是 **2026-08-19 快照**,常与实时值差一倍(见 `全家桶` 卡)。三者**不可互证**。


### 坐标(复现入口)

| 卡 | repo | npm 包名 | 目录条目 | 装法(0.2.x) | 已挖 | 未挖 |
|---|---|---|---|---|---|---|
| `界面套件` | `MichengAI/dsh-codex-ui` | `@michengai/dsh-codex-ui` | `MichengAI__dsh-codex-ui.yml` (`ui`) | `dsh plugin --profile web add @michengai/dsh-codex-ui@latest --registry=https://registry.npmjs.org/` → 重启 → **硬刷新** | `_证据/01_产品聚合-原始挖掘.md` §三 | 六个子插件是否独立分包;与 ds-bot 的冲突检测 |
| `全家桶` | `zhu1090093659/dsh-web` | `@linxin666/dsh-web-all`(聚合)+ 20 个 `@linxin666/dsh-*` | `zhu1090093659__dsh-web-ui--packages-dsh-web-ui-all.yml` (`ui`) | `dsh plugin --profile web add @linxin666/dsh-web-all@latest` → **重启** `dsh web`;或 GitHub 源(二选一) | `_证据/01_产品聚合-原始挖掘.md` §二 | 聚合包最终 bundle 数;patch 是追加还是改 `dsh-web-app` 的行 |
| `组合包` | `STARDUSTLC666/dsh-suite` | `@stardustlc/dsh-suite` | `STARDUSTLC666__dsh-suite.yml` (`workflow`) | `dsh plugin --profile desktop add @stardustlc/dsh-suite`(web 换 profile 名)→ 重启 | `_证据/01_产品聚合-原始挖掘.md` §三 | 组合补丁的默认值清单;共同加载检查方式 |
| `闭环装配` | `morlay/dsh-plugin` | `@morlay/better-session` | **无**（目录外） | `dsh plugin --profile web add "@morlay/better-session"` | `_证据/02_产品形态-原始挖掘.md` §三 | 五个 bundle 的下载分布；子包版本是否强制同版 |
| `接管套件` | `sidleo/dsh-plugins-plus` | `@sidleo3/dsh-plugins-plus` | **无**（目录外） | `dsh plugin --profile <profile> add @sidleo3/dsh-plugins-plus` → 重启 | `_证据/02_产品形态-原始挖掘.md` §一 | 接管引擎的 pre-step 时序；`/api/…/log` 字段 |
| `套件市场` | `Sivan757/dsh-agent-plugins-market` | `dsh-agent-plugins-market` | `Sivan757__dsh-agent-plugins-market.yml` (`market`) | `dsh plugin --profile <name> add dsh-agent-plugins-market` → 重启 | `_证据/02_产品形态-原始挖掘.md` §二 | 十种布局的兼容分级；hooks 与宿主门禁的优先级 |
| `聚合补丁` | `hyzyn/dsh-plugin-kit` | `@hyzyn/dsh-all`(+ 11 个插件 + 1 库) | `hyzyn__dsh-plugin-kit--packages-*.yml`(逐包) | `dsh plugin --profile web add @hyzyn/dsh-all` → 重启 | `_证据/01_产品聚合-原始挖掘.md` §三 | patch 形态;Profile 卡片与上游模板的关系 |

## 4. profile 侧必抄 8 条

**这八条只在"你发的是 profile 级产品"时成立**;发单插件抄它们会抄成过度设计。前 6 条来自聚合型样本,后 2 条来自接管型与进口型样本。

1. **发货单位是 bundle,不是插件**:包里带 `dsh.bundle.patch`,让用户把它加进 `dsh.profile.bundles`——**不要**教用户手改 cordis 配置。
2. **装成功 ≠ 挂载成功**:给一条读回命令(`dsh --profile <name> --dump-config`);**`exit 0` 不算数**——半挂载(包在 `node_modules`,bundles 里没那行)是这类产品最典型的静默失败。
3. **顺序敏感的事写进前置条件**:构建脚本审批(`allowBuilds`)必须在**首次 add 之前**;写错顺序时"重跑一次"修不回来。
4. **吞并了别人的插件,就要处理共存**:列出被内置的原插件,说明"不要同装",并给迁移与备份——**只隐藏入口不够**,会留下重复路由/服务/监听器。
5. **默认值就是身份**:默认皮肤、默认预设、默认语言、默认导航——用户第一眼看到的是它们,不是你的功能列表。
6. **`desktop` 不是你的名字**:官方 Electron 应用独占它(CLI 拒绝 boot/config-dump);桌面入口要按"应用内安装"单独写。

**后两条来自 2026-10-31 补的接管型与进口型样本:**

7. **替换宿主自带实现要可逆**:停原行 + 加己行 + 按 preset 生效;**回退 = 删掉覆写行**,不是写一份"等于出厂"的配置——后者的默认值永远跟不上上游。启用前后都要能一眼看出"现在是谁在生效"。
8. **分发的单位可以不是你的 bundle**:别的 agent 的套件也能当安装单位;**就地读、不转换**才能跟上游;坏声明要**诊断后跳过**,绝不半挂载。

## 5. 普查记录:这一桶为什么薄,以及 2026-10-31 补了什么

**结论先说**:这一桶天然薄——profile 级产品的作者通常有三条去路(DIY 一个桌面壳、发单个插件、或被上游收编),留下来的多是 npm 下载高、星标低的"打包型"产品。**2026-10-31 用 npm 反向普查**(见下表)补了 3 张:接管型 / 进口型 / 闭环型,三种都不是"再加一个聚合包"。


**方法**:对 7,924 条注册表描述做正则召回(`全家桶|整套|开箱即用|一键装齐|发行版|distribution|all-in-one|suite|一整套`),再按 F1–F3 逐条过。

| 候选 | 命中什么 | 判定 |
|---|---|---|
| `MichengAI/dsh-codex-ui` | 六微内核子插件重做整套界面;npm 月下载 **119,610** | **收**(界面套件) |
| `zhu1090093659/dsh-web` | 聚合包 + 自带商店/皮肤/更新 + profile 安装 + 浏览器;月下载 **99,694** | **收**(全家桶) |
| `STARDUSTLC666/dsh-suite` | 18 个独立插件 + 共享默认配置 + 固定版本;月下载 **8,230** | **收**(组合包) |
| `hyzyn/dsh-plugin-kit` | 一条 bundle patch 挂 11 个插件 + Profile 管理卡片;月下载 **3,558** | **收**(聚合补丁) |
| `morlay/dsh-plugin` | 一个 bundle 装配一条会话闭环(5 包);月下载 **8,561** | **收**(闭环装配) |
| `sidleo/dsh-plugins-plus` | 按 preset 停掉宿主自带行,换成 `-plus` 行;月下载 **6,094** | **收**(接管套件) |
| `Sivan757/dsh-agent-plugins-market` | 十种外部套件布局就地读成可安装单位;月下载 **4,752** | **收**(套件市场) |
| `hust-open-atom-club/oh-dsh` | "社区发行版:TUI、桌面端与 Web UI 统一体验" | **不收**:自带运行时与安装包 → `shell` 侧 |
| `magian1127/deepseek-harness-zh_pro` | 综合性增强插件,2,360 下载 | **不收**:单插件增强 |
| `whyihaveyou/dsh-suite` | 活目录 + 内置商店 + 脚手架 + 工作台(开发中) | **不收**:产品是目录/商店(插件侧) |
| `Fayelin12/dsh-office` | 办公室工作台面板 | **不收**:单面板 |
| `Yurzi/dsh-tool-web-enhanced` | 包名里带 `profile` | **不收**:组合包解决 search/fetch 后端 |

**待补**(下一步值得从生态与 GitHub 搜的):

- [ ] 其他"**改 web 默认形态**"的发行版:自建导航/首页/皮肤 + 自带更新通道的组合
- [ ] `dsh-web` 之外的**企业内部分发**:把 profile 当交付物(环境码/模板/锁定 bundle 列表)的实践——候选 `@huaweidevtools/aishell-dsh-base`(月 1,386,**未过门槛**,待看它的 base layer 语义)
- [ ] **发行版 overlay**:`amplifthq/oh-my-dsh`(★16 / 月 481)自称"overlay, not a fork"、装两个独立 profile——**两头都差一点**,先判它算 profile 还是 shell
- [ ] 官方 `desktop` profile 的**包结构**(它是唯一由上游自己交付的 profile 产品,可当"官方怎么做"的参照)
- [ ] 皮肤/预设/宠物这类**产品资产**是否也在 profile 里(还是在 `~/.dsh` 的数据区)——`RevolutionLA/dsh-dream-skin`(★297 / 月 41,441)是现成样本,但它只换皮肤,暂按插件侧看

**npm 反向普查(2026-10-31)**:`keywords:dsh-bundle` 有 322 个包;按月下载排前 20 后逐个人工判形态,过门槛且成卡的 3 个、进候选池的 4 个(见 [`BACKLOG`](../BACKLOG.md))。星标普遍 <20,说明**这类产品的"影响力"只能按下载看**。

**搜索口径**:`category` 是 `ui` + 描述出现**聚合包 / 全家桶 / 商店 / 皮肤中心 / 预设中心**;再看它是否同时改 3 层以上并自带更新。只加能力的不成卡(见 [`horizon`](../../leverage/horizon.md))。

## 6. 三个 lever 的取舍

| | [`plugin` 侧](../plugin/README.md) | 本 lever | [`shell` 侧](../shell/README.md) |
|---|---|---|---|
| 你交付什么 | 一个插件 | **一套 bundle / 一个 profile** | 一个应用(或换掉表层) |
| 用户怎么启动 | 装进他现有的 profile | `dsh web --profile <name>` | 双击/命令行启动 |
| 你负责到哪层 | 3 层(槽位)为主 | 5/6/7(默认值/首启/分发) | 2 层起,连运行时都可能要带 |
| 抄错的样子 | 硬依赖不存在的服务 → 白屏 | 装上了但 bundles 没那行 → 用户以为装好 | 换了表层没补 5/6/7 → 首启即崩 |

## 7. 边界

**收**:一套 bundle(或等价的分发单位)+ 浏览器启动 + 自带默认值/首启/分发,且有可复核的影响力证据。**七种形态**:全家桶 / 界面套件 / 组合包 / 聚合补丁 / 接管套件 / 套件市场 / 闭环装配。

**不收**:单插件增强(→ [`plugin`](../plugin/README.md));终端表层 / 自带运行时 / 安装包(→ [`shell`](../shell/README.md));只支持 `0.1.x` 的样本。

**共享文件只读**:`00-map.md`、`horizon.md`、`leverage/README.md`、`data/` 由别的会话维护,本 lever 只调用、不写。
