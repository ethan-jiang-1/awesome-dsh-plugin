---
title: "profile · profile 即产品"
domain: reshape-product
kind: charter
positioning: "profile 侧宪章：一套 bundle + 默认值 + 首启 + 分发，用 dsh web 在浏览器里启动。八种形态。"
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
> **借阅入口**:想判归属 → [§2 判据](#2-入桶判据) · 想抄 → [§4 设计检查清单](#4-profile-设计检查清单) · 想回源 → [§3 坐标](#3-卡表)

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

**按 npm 近 30 天下载排序。** 八张卡是**八种形态**——前四种是"怎么把自己的东西装成一件",后四种是"换宿主 / 进口别人的 / 装一条闭环 / 做视觉资产"。

| 卡 | 产品 | npm 月下载 | ★(2026-10-31) | 判据 | 形态 | **能借鉴什么** |
|---|---|---|---|---|---|---|
| [`界面套件`](./12_界面套件-dsh-codex-ui.md) | `MichengAI/dsh-codex-ui` | **119,610** | 250 | F1(单包多模块)·F2·F3(默认值/共存) | 2.0.9 inserts six rows; theme/composer/sidebar have different probe/activation/cleanup lifecycles | theme final dispose doesn't run probe-failure restore; composer activates before async probe; settings 0 DOM is local branch only; sidebar/settings skin retain DOM/CSS coupling |
| [`视觉资产`](./18_视觉资产-dsh-wallpaper-engine.md) | `elysia395/dsh-wallpaper-engine` | **109,268** | 4,189 | F1(外观层)·F2·F3(预设分发) | v1.4.0 main + 7 packages/rows; Scene/Web/Video/custom assets; versioned preset snapshots; zero tool/prompt contract | 1.4.0 has no glass row; better-sidebar optional; preset obsolete schema refuses migration; WebGL/ffmpeg behavior needs actual hardware runtime verification |
| [`全家桶`](./11_全家桶-dsh-web.md) | `zhu1090093659/dsh-web` | **99,694** | 9,865 | F1·F2·F3(四项全中) | private root wrapper + aggregate bundle + family/satellite packages | aggregate manifest 生成 patch/exports/metadata；package、bundle roster 与 row enabled 是不同状态；family 更新与退役出口协同 |
| [`闭环装配`](./17_闭环装配-better-session.md) | `morlay/dsh-plugin` | **8,561** | 9 | F1(闭环)·F2·F3(行+配置同居) | npm 0.1.10 tarball 将五个 exact deps/patch rows 与 SQLite default 组合；README 描述 edit/retry/rewind/fork | 发布 patch 可供 assembly review；session schema/状态迁移/事务和 side-effect safety 是 DOC/OPEN；preset sibling 不归本 bundle |
| [`组合包`](./13_组合包-dsh-suite.md) | `STARDUSTLC666/dsh-suite` | **8,230** | 3 | F1·F2·F3(默认值/更新) | 0.9.1: 18 exact direct deps + 18 patch rows/defaults; same-package updater with profile-scoped prefs and gated updates | direct pins ≠ transitive lock; owner-aware suite member suppression; compensating old-version restore has crash window; defaults remain overridable by higher patches |
| [`接管套件`](./15_接管套件-dsh-plugins-plus.md) | `sidleo/dsh-plugins-plus` | **6,094** | 0 | F1(按 preset)·F2·F3(默认值) | README 描述按 preset 接管内置 discovery behavior | npm 0.2.0 源码 pin 未与 GitHub manifest 对齐；接管算法、rollback、migration 暂列 DOC/OPEN，不作为机制结论 |
| [`套件市场`](./16_套件市场-dsh-agent-plugins-market.md) | `Sivan757/dsh-agent-plugins-market` | **4,752** | 19 | F1(多 adapter 布局)·F2·F3(分发/凭据) | 外部 source checkout 被发现为 source-qualified suites，并由 runtime adapters 挂载多类资源 | user-scoped install 与 workspace filter 分离；refresh 不冻结 installed content；OAuth persistence 条件化；parser validation 按 artifact 粒度；dry-run 非 sandbox |
| [`聚合补丁`](./14_聚合补丁-dsh-all.md) | `hyzyn/dsh-plugin-kit` | **3,558** | 59 | F1·F2·F3(默认值/更新/管理) | v0.1.73：12 insert rows + 11 exact member deps；aggregate 导出 no-op runtime entry；Profile manager 为独立 substantive member | distinguish patch-driven aggregation from literal zero code; shared kit is transitive member dependency, not a row; reject duplicate install; treat Profile CRUD as guarded filesystem/process surface |

**影响力门槛以 [`00-map` §7](../00-map.md) 为准**：本桶额外要求 npm 近 30 天 **≥ 3,000** 或 ★ **≥ 200**（聚合包星标普遍虚低）。低于门槛的只进 §5 普查表,不单独成卡。

**口径摘要**（详见 `00-map` §7）:npm 月下载取 `api.npmjs.org/downloads/point/last-month`(2026-09-30 ~ 10-29),**含 CI 与镜像**;★ 取 GitHub API(2026-10-31);仓库 `downloads.json`/`stars.json` 是 **2026-08-19 快照**,常与实时值差一倍(见 `全家桶` 卡)。三者**不可互证**。


### 坐标(复现入口)

| 卡 | repo | npm 包名 | 目录条目 | 装法(0.2.x) | 已挖 | 未挖 |
|---|---|---|---|---|---|---|
| `界面套件` | `MichengAI/dsh-codex-ui` | `@michengai/dsh-codex-ui@2.0.9` | `MichengAI__dsh-codex-ui.yml` (`ui`) | README: `dsh plugin --profile web add …` → 重启 → 硬刷新（未实测） | `_证据/01_产品聚合-原始挖掘.md` §三；`_证据/10_界面套件-dsh-codex-ui-源码复核.md` | theme dispose/root cleanup、composer probe timing、DOM selector compat、real browser disable/unmount、ds-bot conflict detection |
| `全家桶` | `zhu1090093659/dsh-web` | `@linxin666/dsh-web-all`(聚合)+ 20 个 `@linxin666/dsh-*` | `zhu1090093659__dsh-web-ui--packages-dsh-web-ui-all.yml` (`ui`) | `dsh plugin --profile web add @linxin666/dsh-web-all@latest` → **重启** `dsh web`;或 GitHub 源(二选一) | `_证据/01_产品聚合-原始挖掘.md` §二 | 聚合包最终 bundle 数;patch 是追加还是改 `dsh-web-app` 的行 |
| `组合包` | `STARDUSTLC666/dsh-suite` | `@stardustlc/dsh-suite@0.9.1` | `STARDUSTLC666__dsh-suite.yml` (`workflow`) | README: desktop/web profile add → 重启（未实测） | `_证据/01_产品聚合-原始挖掘.md` §三；`_证据/09_组合包-dsh-suite-源码复核.md` | consumer lock/transitive graph；manual/auto updater recovery 在真实 profile 中的实际恢复；18 package 的 runtime compat |
| `视觉资产` | `elysia395/dsh-wallpaper-engine` | `dsh-plugin-wallpaper-engine@1.4.0` | `elysia395__dsh-wallpaper-engine.yml` (`theme`) | README: web/desktop profile add；装前退出 DSH（未实测） | `_证据/03_视觉资产-原始挖掘.md`；`_证据/11_视觉资产-dsh-wallpaper-engine-源码复核.md` | WebGL/GPU/ffmpeg runtime；preset obsolete schema UX；eight-package teardown；与其它 skin/sidebar 的共存 |
| `闭环装配` | `morlay/dsh-plugin` | `@morlay/better-session@0.1.10` | **无**（目录外） | README: `dsh plugin --profile web add "@morlay/better-session"`（未实测） | `_证据/02_产品形态-原始挖掘.md` §三；`_证据/07_闭环装配-better-session-源码复核.md` | 0.1.10 source provenance；五个依赖的行为兼容；session schema/transactions/workspace ownership/recovery |
| `接管套件` | `sidleo/dsh-plugins-plus` | `@sidleo3/dsh-plugins-plus` | **无**（目录外） | `dsh plugin --profile <profile> add @sidleo3/dsh-plugins-plus` → 重启 | `_证据/02_产品形态-原始挖掘.md` §一 | 接管引擎的 pre-step 时序；`/api/…/log` 字段 |
| `套件市场` | `Sivan757/dsh-agent-plugins-market` | `dsh-agent-plugins-market` | `Sivan757__dsh-agent-plugins-market.yml` (`market`) | README: `dsh plugin --profile <name> add …` → 重启（未实测） | `_证据/02_产品形态-原始挖掘.md` §二；`_证据/05_套件市场-dsh-agent-plugins-market-源码复核.md` | 十种 layout 各自验证深度；OAuth provider lifecycle；hook executor trust boundary；用户 state 恢复 |
| `聚合补丁` | `hyzyn/dsh-plugin-kit` | `@hyzyn/dsh-all@0.1.73` + 11 pinned members + transitive `dsh-kit` | `hyzyn__dsh-plugin-kit--packages-*.yml`(成员逐包) | README: `dsh plugin --profile web add @hyzyn/dsh-all` → 重启（未实测） | `_证据/01_产品聚合-原始挖掘.md` §三；`_证据/08_聚合补丁-dsh-all-源码复核.md` | duplicate row behavior、部分依赖安装恢复、Profile UI error paths、README impact matrix 对实际成员权限的准确性 |

## 4. Profile 设计检查清单

**以下是复核过的设计问题，不是九条无条件通用规则。** 仅在目标形态需要时采用；每条依赖的机制与证据层级见对应样本卡/源码复核。尤其 README-only 主张和源码 provenance 不匹配的样本，不能单独成为实现保证。

1. **区分 bundle package、dependency rows 和 effective profile state**：`dsh-web`/`dsh-all` 的发布物显示 bundle patch/rows；DSH profile 还会叠更高层 config。安装成功、row 入 roster、最终 enabled/config 是不同状态，需按产品提供读回路径。
2. **声明式生成要验证多份产物一致**：当依赖清单、Loader rows、包 exports 来自同一聚合定义时，用 generator/check 维持 parity；样本 `dsh-web` 和 `dsh-all` 都有此类仓库机制，但它不证明 profile 安装原子成功。
3. **重复装配要有冲突政策**：若 aggregate rows 与 standalone rows 使用同 id，同 profile 混装可能冲突；明确禁止组合、提供检测，或设计不同 namespace。`dsh-all@0.1.73` 与 `dsh-web` 的 namespace 策略并不相同，不能拿一个前缀当通则。
4. **安装前展示实际影响面**：组合涉及 model tools、system prompt、UI、filesystem、network 或 process 时，按成员列 capability 与风险；`dsh-all` README 有分面表，Profile manager 源码也显示 CRUD 是真实 filesystem/process 行为。
5. **区分默认值和用户最终值**：bundle/package row config 是一层 defaults；profile/home/CLI patches 可覆盖。说明有效配置如何查看，并按明确 owner 保存 profile-scoped state（见 `dsh-suite` updater、`dsh-web` row state）。
6. **更新策略要同时声明 owner、consent 与恢复级别**：direct version pin 不等于 transitive lock；更新失败的 reinstall 是补偿恢复，不是原子回滚（`dsh-suite@0.9.1`）。标明 crash window、restart-required 和人工修复状态。
7. **来源、安装、启用与 workspace 过滤分层**：导入外部 suite 时，source refresh 可改 checkout，而 suite installation 和 workspace filters 有不同 owner（`dsh-agent-plugins-market@0.13.0`）。不可把记录的 `lockCommit` 宣称为内容冻结。
8. **替换宿主实现前先验证可逆范围**：`dsh-plugins-plus@0.2.0` 的 npm/source provenance 尚未对齐，因此“只撤销自己拥有的行”目前只是设计审查问题，不是该发布包已核机制。对自己的产品需实现 ownership-aware diff、foreign edit protection，并对整份 override 删除做失败测试。
9. **视觉资产要区分呈现能力、模型侧预算和资产格式**：`dsh-wallpaper-engine@1.4.0` 源码为不注册模型工具/提示提供静态依据，预设是 full values snapshot 加可选 assets，旧 schema 会作废而非自动迁移；该 release 没有独立 glass package。硬件渲染和真实 token 成本仍需按版本/运行环境验证。

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
| `elysia395/dsh-wallpaper-engine` | 本机 WE 壁纸 + 玻璃 + 字体/吉祥物 + 预设导入导出;★ **4,189** / 月下载 **109,268** | **收**(视觉资产) |
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
- [x] 皮肤/预设这类**产品资产**已收:`18_视觉资产`(★4,189 / 月 109,268)证明外观是独立的产品形态;第二候选 `RevolutionLA/dsh-dream-skin`(★297 / 月 41,441)、`WYH66666666/DSH-Transparent-UI`(★428)见 BACKLOG

**npm 反向普查(2026-10-31)**:`keywords:dsh-bundle` 有 322 个包;按月下载排前 20 后逐个人工判形态,过门槛且成卡的 3 个、进候选池的 4 个(见 [`BACKLOG`](../BACKLOG.md))。星标普遍 <20,说明**这类产品的"影响力"只能按下载看**。

**搜索口径**:`category` 是 `ui` + 描述出现**聚合包 / 全家桶 / 商店 / 皮肤中心 / 预设中心**;再看它是否同时改 3 层以上并自带更新。只加能力的不成卡(见 [`horizon`](../horizon.md))。

## 6. 三个 lever 的取舍

| | [`plugin` 侧](../plugin/README.md) | 本 lever | [`shell` 侧](../shell/README.md) |
|---|---|---|---|
| 你交付什么 | 一个插件 | **一套 bundle / 一个 profile** | 一个应用(或换掉表层) |
| 用户怎么启动 | 装进他现有的 profile | `dsh web --profile <name>` | 双击/命令行启动 |
| 你负责到哪层 | 3 层(槽位)为主 | 5/6/7(默认值/首启/分发) | 2 层起,连运行时都可能要带 |
| 抄错的样子 | 硬依赖不存在的服务 → 白屏 | 装上了但 bundles 没那行 → 用户以为装好 | 换了表层没补 5/6/7 → 首启即崩 |

## 7. 边界

**收**:一套 bundle(或等价的分发单位)+ 浏览器启动 + 自带默认值/首启/分发,且有可复核的影响力证据。**八种形态**:全家桶 / 界面套件 / 组合包 / 聚合补丁 / 接管套件 / 套件市场 / 闭环装配 / 视觉资产。

**不收**:单插件增强(→ [`plugin`](../plugin/README.md));终端表层 / 自带运行时 / 安装包(→ [`shell`](../shell/README.md));只支持 `0.1.x` 的样本。

**共享文件只读**:`00-map.md`、`horizon.md`、`leverage/README.md`、`data/` 由别的会话维护,本 lever 只调用、不写。
