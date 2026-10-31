---
title: "profile · profile 即产品"
domain: reshape-product
kind: charter
positioning: "profile 侧宪章：一套 bundle + 默认值 + 首启 + 分发，用 dsh web 在浏览器里启动。"
takeaway: "发货单位是 bundle；装成功 ≠ 挂载成功，必须读回 dsh.profile.bundles。"
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
> **借阅入口**:想判归属 → [§2 判据](#2-入桶判据) · 想抄 → [§4 必抄 6 条](#4-profile-侧必抄-6-条) · 想回源 → [§3 坐标](#3-卡表)

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

- **主问**：它自己定义默认体验（导航 / 首页 / 皮肤 / 设置），或自带分发与更新，或聚合整套 bundle？
- **门槛**：★ ≥ 200 或 npm 近 30 天 ≥ 3,000；机制例外每 lever ≤ 2 张（见 [`00-map` §7](../00-map.md)）。
- **三条边界**：
  - **单包也能进**——`12_界面套件` 是一个包，但重定义了整套界面与默认值；
  - **聚合要"策展 + 共享默认 + 自有更新"**——`13_组合包` / `14_聚合补丁` 算，纯打包不算；
  - **自带运行时不算**——`oh-dsh` 的 Web 只是三种界面之一 → [`shell` 侧](../shell/README.md)。

> **怎么加卡**：过 00-map §11.1 快筛且门槛达标 → 读 patch/bundle 形态 → 按 00-map §5 建卡 → catalog 与本表各补一行 → `node _leverage/verify.mjs`。

## 3. 卡表

**按 npm 近 30 天下载排序。** 四张卡是四种"聚合形态",不是四个同类产品。

| 卡 | 产品 | npm 月下载 | ★(2026-10-31) | 判据 | 形态 | **能借鉴什么** |
|---|---|---|---|---|---|---|
| [`界面套件`](./12_界面套件-dsh-codex-ui.md) | `MichengAI/dsh-codex-ui` | **119,610** | 250 | F1(单包多内核)·F2·F3(默认值/共存) | 单包六微内核,重做整套界面 | 子插件独立启停;fail-closed 清理(0 DOM);只吃官方 primitive/slot |
| [`全家桶`](./11_全家桶-dsh-web.md) | `zhu1090093659/dsh-web` | **99,694** | 9,865 | F1·F2·F3(四项全中) | 20+ 自研 bundle + 自家商店 | 发货单位是 bundle;`exit 0` 但 bundles 为空 = 静默半挂载;默认皮肤即身份 |
| [`组合包`](./13_组合包-dsh-suite.md) | `STARDUSTLC666/dsh-suite` | **8,230** | 3 | F1·F2·F3(默认值/更新) | 18 个独立插件 + 共享默认配置 | 固定组件版本;整包更新;扁平化无 git 子依赖 |
| [`聚合补丁`](./14_聚合补丁-dsh-all.md) | `hyzyn/dsh-plugin-kit` | **3,558** | 59 | F1·F2·F3(默认值/更新/管理) | 一条 bundle patch 挂 11 个插件 | 聚合包应是纯数据;共享库不进 bundles;Profile 管理卡片 |

**影响力门槛以 [`00-map` §7](../00-map.md) 为准**：本桶额外要求 npm 近 30 天 **≥ 3,000** 或 ★ **≥ 200**（聚合包星标普遍虚低）。低于门槛的只进 §5 普查表,不单独成卡。

**口径摘要**（详见 `00-map` §7）:npm 月下载取 `api.npmjs.org/downloads/point/last-month`(2026-09-30 ~ 10-29),**含 CI 与镜像**;★ 取 GitHub API(2026-10-31);仓库 `downloads.json`/`stars.json` 是 **2026-08-19 快照**,常与实时值差一倍(见 `全家桶` 卡)。三者**不可互证**。


### 坐标(复现入口)

| 卡 | repo | npm 包名 | 目录条目 | 装法(0.2.x) | 已挖 | 未挖 |
|---|---|---|---|---|---|---|
| `界面套件` | `MichengAI/dsh-codex-ui` | `@michengai/dsh-codex-ui` | `MichengAI__dsh-codex-ui.yml` (`ui`) | `dsh plugin --profile web add @michengai/dsh-codex-ui@latest --registry=https://registry.npmjs.org/` → 重启 → **硬刷新** | `_证据/01_产品聚合-原始挖掘.md` §三 | 六个子插件是否独立分包;与 ds-bot 的冲突检测 |
| `全家桶` | `zhu1090093659/dsh-web` | `@linxin666/dsh-web-all`(聚合)+ 20 个 `@linxin666/dsh-*` | `zhu1090093659__dsh-web-ui--packages-dsh-web-ui-all.yml` (`ui`) | `dsh plugin --profile web add @linxin666/dsh-web-all@latest` → **重启** `dsh web`;或 GitHub 源(二选一) | `_证据/01_产品聚合-原始挖掘.md` §二 | 聚合包最终 bundle 数;patch 是追加还是改 `dsh-web-app` 的行 |
| `组合包` | `STARDUSTLC666/dsh-suite` | `@stardustlc/dsh-suite` | `STARDUSTLC666__dsh-suite.yml` (`workflow`) | `dsh plugin --profile desktop add @stardustlc/dsh-suite`(web 换 profile 名)→ 重启 | `_证据/01_产品聚合-原始挖掘.md` §三 | 组合补丁的默认值清单;共同加载检查方式 |
| `聚合补丁` | `hyzyn/dsh-plugin-kit` | `@hyzyn/dsh-all`(+ 11 个插件 + 1 库) | `hyzyn__dsh-plugin-kit--packages-*.yml`(逐包) | `dsh plugin --profile web add @hyzyn/dsh-all` → 重启 | `_证据/01_产品聚合-原始挖掘.md` §三 | patch 形态;Profile 卡片与上游模板的关系 |

## 4. profile 侧必抄 6 条

**这六条只在"你发的是 profile 级产品"时成立**;发单插件抄它们会抄成过度设计。

1. **发货单位是 bundle,不是插件**:包里带 `dsh.bundle.patch`,让用户把它加进 `dsh.profile.bundles`——**不要**教用户手改 cordis 配置。
2. **装成功 ≠ 挂载成功**:给一条读回命令(`dsh --profile <name> --dump-config`);**`exit 0` 不算数**——半挂载(包在 `node_modules`,bundles 里没那行)是这类产品最典型的静默失败。
3. **顺序敏感的事写进前置条件**:构建脚本审批(`allowBuilds`)必须在**首次 add 之前**;写错顺序时"重跑一次"修不回来。
4. **吞并了别人的插件,就要处理共存**:列出被内置的原插件,说明"不要同装",并给迁移与备份——**只隐藏入口不够**,会留下重复路由/服务/监听器。
5. **默认值就是身份**:默认皮肤、默认预设、默认语言、默认导航——用户第一眼看到的是它们,不是你的功能列表。
6. **`desktop` 不是你的名字**:官方 Electron 应用独占它(CLI 拒绝 boot/config-dump);桌面入口要按"应用内安装"单独写。

## 5. 普查记录:这一桶为什么薄

**方法**:对 7,924 条注册表描述做正则召回(`全家桶|整套|开箱即用|一键装齐|发行版|distribution|all-in-one|suite|一整套`),再按 F1–F3 逐条过。

| 候选 | 命中什么 | 判定 |
|---|---|---|
| `MichengAI/dsh-codex-ui` | 六微内核子插件重做整套界面;npm 月下载 **119,610** | **收**(界面套件) |
| `zhu1090093659/dsh-web` | 聚合包 + 自带商店/皮肤/更新 + profile 安装 + 浏览器;月下载 **99,694** | **收**(全家桶) |
| `STARDUSTLC666/dsh-suite` | 18 个独立插件 + 共享默认配置 + 固定版本;月下载 **8,230** | **收**(组合包) |
| `hyzyn/dsh-plugin-kit` | 一条 bundle patch 挂 11 个插件 + Profile 管理卡片;月下载 **3,558** | **收**(聚合补丁) |
| `hust-open-atom-club/oh-dsh` | "社区发行版:TUI、桌面端与 Web UI 统一体验" | **不收**:自带运行时与安装包 → `shell` 侧 |
| `magian1127/deepseek-harness-zh_pro` | 综合性增强插件,2,360 下载 | **不收**:单插件增强 |
| `whyihaveyou/dsh-suite` | 活目录 + 内置商店 + 脚手架 + 工作台(开发中) | **不收**:产品是目录/商店(插件侧) |
| `Fayelin12/dsh-office` | 办公室工作台面板 | **不收**:单面板 |
| `Yurzi/dsh-tool-web-enhanced` | 包名里带 `profile` | **不收**:组合包解决 search/fetch 后端 |

**待补**(下一步值得从生态与 GitHub 搜的):

- [ ] 其他"**改 web 默认形态**"的发行版:自建导航/首页/皮肤 + 自带更新通道的组合
- [ ] `dsh-web` 之外的**企业内部分发**:把 profile 当交付物(环境码/模板/锁定 bundle 列表)的实践
- [ ] 官方 `desktop` profile 的**包结构**(它是唯一由上游自己交付的 profile 产品,可当"官方怎么做"的参照)
- [ ] 皮肤/预设/宠物这类**产品资产**是否也在 profile 里(还是在 `~/.dsh` 的数据区)

**搜索口径**:`category` 是 `ui` + 描述出现**聚合包 / 全家桶 / 商店 / 皮肤中心 / 预设中心**;再看它是否同时改 3 层以上并自带更新。只加能力的不成卡(见 [`horizon`](../../leverage/horizon.md))。

## 6. 三个 lever 的取舍

| | [`plugin` 侧](../plugin/README.md) | 本 lever | [`shell` 侧](../shell/README.md) |
|---|---|---|---|
| 你交付什么 | 一个插件 | **一套 bundle / 一个 profile** | 一个应用(或换掉表层) |
| 用户怎么启动 | 装进他现有的 profile | `dsh web --profile <name>` | 双击/命令行启动 |
| 你负责到哪层 | 3 层(槽位)为主 | 5/6/7(默认值/首启/分发) | 2 层起,连运行时都可能要带 |
| 抄错的样子 | 硬依赖不存在的服务 → 白屏 | 装上了但 bundles 没那行 → 用户以为装好 | 换了表层没补 5/6/7 → 首启即崩 |

## 7. 边界

**收**:一套 bundle + 浏览器启动 + 自带默认值/首启/分发,且有可复核的影响力证据。

**不收**:单插件增强(→ [`plugin`](../plugin/README.md));终端表层 / 自带运行时 / 安装包(→ [`shell`](../shell/README.md));只支持 `0.1.x` 的样本。

**共享文件只读**:`00-map.md`、`horizon.md`、`leverage/README.md`、`data/` 由别的会话维护,本 lever 只调用、不写。
