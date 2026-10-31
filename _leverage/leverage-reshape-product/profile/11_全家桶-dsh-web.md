---
title: "全家桶 · dsh-web（9,865★）"
domain: reshape-product
kind: sample
positioning: "把 20+ 个 bundle 装进 web profile，重启 dsh web 后浏览器里就是一个新产品。"
takeaway: "声明式 aggregate manifest 生成 bundle patch；包安装、profile bundle roster 与 row 启用是不同状态，必须分别核验。"
read_when: "要做 profile 级产品/全家桶；或判断一个东西该发插件还是发发行版。"
status: observed
updated: 2026-10-31
budget: 190
---
# 全家桶 · dsh-web：一个 profile 就是一个产品

> **研究范围**：目标仓库 tag `v0.4.13` / commit [`88409fb`](https://github.com/zhu1090093659/dsh-web/commit/88409fb958e4b97e7c179b9e50d26f5359627710)；DSH 上游运行时依据为 `@deepseek-ai/dsh@0.2.1-rc.3`。目标源码/测试已读，未安装、构建或运行目标包。完整来源、测试范围和未验证项见[`04 源码复核`](./_证据/04_全家桶-dsh-web-源码复核.md)。
> **类**:`1` 壳与工作台 · **层**:2(表层)+ 3(槽位)+ 5(默认值)+ 6(首启)+ 7(分发) · **★ 9,865**(GitHub API,2026-10-31)/ **npm 月下载 99,694**(2026-09-30 ~ 10-29);仓库旧快照(2026-08-19)为 ★ 4,661 / 59,648
> **一句话**:`dsh-web` 以 private root repo、公开 aggregate 包、家族子包和外部 satellite 组成发布家族；生成器把描述性的 manifest 编译为 DSH bundle patch。商店、皮肤、预设和 updater 是该版本 README 描述的产品能力，本次对这些用户体验未做实测。
> **借鉴价值**:**① 用 declarative manifest 管理 patch 来源、依赖、external rows、disabled rows 与 retired identities；② 把安装依赖名和 Loader row id 分开，用 `web-ui-*` 命名空间并用生成测试防 standalone/aggregate collision；③ 把 disabled 理解成“包在依赖中、bundle row 已存在但默认不启用”，不能把它与未安装或未进入 profile bundle roster 混为一谈；④ updater 是家族依赖升级器，需处理 registry/version verification；⑤ row/package 迁移需 tombstone 和 retired registry，避免旧 profile 的过期子路径 import 硬失败；⑥ UI、商店、自更新是否成功仍需独立 runtime evidence。**

> **证据成熟度**：聚合 manifest、row 生成、patch 和更新目标为 `机制参考`；半挂载、restart UX、任意 profile 下的 pnpm resolution 和视觉体验仍主要是 `[DOC]` / `[OPEN]`，不是本次行为实测。
> **样本档案**
> **repo**:[`zhu1090093659/dsh-web`](https://github.com/zhu1090093659/dsh-web) · **仓库 root**:`dsh-web@0.4.13`(private wrapper) · **npm bundle**:`@linxin666/dsh-web-all@0.4.13` + 仓内 family packages / registry satellites · **许可证**:Apache-2.0
> **目录条目**:`data/plugins/zhu1090093659__dsh-web-ui--packages-dsh-web-ui-all.yml`(`ui`)
> **装法**:README 文档入口为 `dsh plugin --profile web add @linxin666/dsh-web-all@latest` 或 `github:zhu1090093659/dsh-web`，并要求二选一后重启 `dsh web`；本次源码复核未复现这两种安装方式。
> **自带分发面**:<https://dsh-market.com>(皮肤/宠物/插件/预设;Cloudflare Workers + D1 点赞)
> **证据链**：早期 profile/上游语义摘录见[`_证据/01_产品聚合-原始挖掘.md`](./_证据/01_产品聚合-原始挖掘.md)；固定 `v0.4.13` manifest/aggregate generator/CI 复核见[`_证据/04_全家桶-dsh-web-源码复核.md`](./_证据/04_全家桶-dsh-web-源码复核.md)。
> **下一步验证**：在隔离 profile 实测安装后 package dependency、`dsh.profile.bundles` roster、row disabled overrides 的生效、重启和升级/退役迁移；不得将 CI job 定义当成本次已通过。

---

## 它想干什么 · 为什么值得借鉴

**意图 [DOC]**：README 把产品描述为浏览器中的完整工作台（任务板、Git、远程、技能、皮肤、商店），而不是逐个安装功能包。本卡的“整张桌子”是产品定位摘要，不是源码推导出的功能完整性结论。

**意义 [SRC-TARGET][OBS]**：v0.4.13 目标源码证明它将多个实际 packages 和 rows 作为一个 DSH profile bundle family 生成与发布。它没有证明“一个 bundle 等于全部产品体验”；商店、皮肤、预设、更新器属于 `[DOC]` 描述且含独立资产/服务面。可迁移的判断是把“成员选择、默认启用、更新与身份迁移”视为发行版产品决策，而非把产品化等同于 package aggregation 技术。

**用户价值 [DOC/OBS]**：README 描述用户可通过 family bundle 获得多个入口、默认皮肤和扩展入口。由此可观察到“策展减少逐包选型成本”的产品假设；默认布局、实际首屏和升级过程没有启动验证。潜在代价包括 family 版本协同、disabled row 的状态理解，以及迁移已有 standalone 插件，这些须在目标 profile 实测。

**表达 [DOC/OBS]**：README 把 Blue Fantasy 暗色皮肤、带图标入口和皮肤/预设中心描述为初始体验。可提炼的观察是：对视觉/分发型 profile，第一屏默认值能承担产品身份；移植时仍需为用户提供关闭/恢复原生默认的路径。本轮没有启动 UI，故实际首屏和视觉连续性均未实测。

## 0. 一页速览(想抄的人只看这 20 行)

| 问题 | 当前可确认的答案 | 证据与状态 |
|---|---|---|
| 哪个包是 profile bundle | private root repo `dsh-web` 是 GitHub wrapper；实际 bundle 是 `@linxin666/dsh-web-all@0.4.13`，其 manifest 声明 patch 和 DSH floor | `[SRC-TARGET]` root/aggregate `package.json`；commit `88409fb`，见源码复核 §身份 |
| 聚合内容从哪来 | `aggregate.yml` 声明 patch 来源/顺序、依赖、外部行、固定 family ids、默认 disabled 与退休兼容；generator 产出 patch、exports、metadata 与 retired registry | `[SRC-TARGET]` `aggregate.yml` / `scripts/aggregate.mjs`；`[TEST]` aggregate consistency tests（已读未运行） |
| 安装时几种状态要分开 | 包依赖已安装、profile `dsh.profile.bundles` 已登记、row 最终 enabled 是三层不同状态；`inactive` 是有包有 row 但 `disabled: true` | `[SRC-TARGET]` generator；`[SRC-DSH]` `@deepseek-ai/dsh@0.2.1-rc.3` patch resolver；本次未运行 CLI |
| 半挂载如何表现 | README 报告曾出现 `exit 0` 但 bundle roster 无该项，并要求读回验证 | `[DOC]` README 排障；没有本次 `[RUN]` 复现 |
| standalone 与 aggregate 共存 | generator 使用不同 row namespace；仓库测试检查 standalone/aggregate id collision | `[SRC-TARGET]` `namespaceId` / `familyIds`；`[TEST]` `aggregate.test.mjs`；外部安装共存仍未实测 |
| 子包迁移/退役怎么办 | tombstone exports 与 `retiredPlugins` registry 为旧 package subpath 提供过渡 no-op；测试校验 tombstone 与 registry 一致 | `[SRC-TARGET]` generator/shell；`[TEST]` retirement tests；真实旧 profile 升级未实测 |
| 家族包怎样更新 | `dsh-update` 汇总 family dependencies，执行 profile 更新后回读验证版本 | `[SRC-TARGET]` `dsh-update/src/update.ts`；未运行更新 |
| UI、商店、默认皮肤、桌面入口呢 | README 描述完整产品体验和对应操作 | `[DOC]` README；本次未 boot UI，不能写成 runtime 观察 |
| 最可迁移的一点 | 把声明式装配事实源、package dependency、Loader row identity、profile roster、effective enabled state 分开建模 | `[OBS]` 由上述 `[SRC-TARGET]` / `[SRC-DSH]` 推导；适用条件与代价见 §5 |

## 1. 它在产品里的位置

**七层坐标 `[DOC/OBS]`**：2（导航轨/顶栏/对话布局）+ 3（任务看板、SSH、用量、Git 等槽位）+ 5（皮肤/预设/语言）+ 6（安装后的首次体验）+ 7（聚合交付/商店/更新）。这组坐标是基于 README 描述的分类，不是本次启动观察。

**DSH 上游接缝 `[SRC-DSH]`**：`@deepseek-ai/dsh@0.2.1-rc.3` profile resolver 将有序 `dsh.profile.bundles` 各 bundle patch 与用户 profile patch 按固定层次组合；细节引用见[`源码复核`](./_证据/04_全家桶-dsh-web-源码复核.md)。

**目标项目装配 `[SRC-TARGET]`**：v0.4.13 的 package dependencies 决定包可解析，aggregate patch 行决定注册/配置，profile bundle roster 决定哪些 bundle 进入 patch fold，用户 profile patch 再承载用户覆盖。它不是“所有产品内容都在 bundle patch 与 user patch 两处”；商店和可下载资产有独立组件/存储面，部分体验仍只有 DOC 证据。静态源码不能推出现场 add 成功或运行时更新已复现。

## 2. 机制与装配架构

### 2.1 发布边界：仓库 root 不是 npm bundle

`[SRC-TARGET]` v0.4.13 root `package.json` 标 `private: true`、包名 `dsh-web`，作为 GitHub 入口并依赖公开包 `@linxin666/dsh-web-all@^0.4.13`。真正进入 profile 的 aggregate package 是 `@linxin666/dsh-web-all@0.4.13`，声明 `dsh.bundle.patch` 和 `engines.dsh >=0.2.1-rc.3`。它依赖仓内功能包的 `workspace:*`，并 pin 四个拆仓 satellite 的 registry version。仓库根身份、profile 安装入口、bundle 身份是三个不同对象。详见固定版本[`源码复核`](./_证据/04_全家桶-dsh-web-源码复核.md#身份与发布边界)。

> **可迁移洞察**：当 monorepo 同时承担 GitHub 安装入口和 npm 发布物时，明确标注哪个 package 才是 profile bundle；别让仓库名、wrapper、可发布包名互相冒充。

### 2.2 `aggregate.yml` 是装配事实源，patch 是生成物

`[SRC-TARGET]` `packages/dsh-web-all/aggregate.yml` 集中表达 `patchFrom`（child patch 来源/顺序）、`deps`（要安装的包）、`self`、外部 `rows`、`familyIds`、`inactive`、`tombstones` 与 `retiredPlugins`。`scripts/aggregate.mjs` 据此生成 `cordis.patch.yml`、package export/依赖、shell metadata 和退休插件 registry；patch 文件标注为 generated。改动应落 manifest 并运行 generator，不应手修产物；`aggregate:check` / tests 负责抓 manifest 和产物漂移（测试已读，未运行）。

> **可迁移洞察**：当 bundle 同时描述依赖、装配行、默认启停和兼容迁移时，维护一份声明式事实源并从它生成多个发布面；否则 manifest、patch、exports 与旧包 tombstone 会独立漂移。

### 2.3 包依赖、row identity 与实际启用是不同层

`[SRC-TARGET]` 生成器把 child row `ui-foo` 映射成 aggregate row `web-ui-foo`，但 row 的 `name` 指向 child 的真实 package name；package.json `dependencies` 决定包能被解析，patch row id 决定 Loader 装载身份，`dsh.profile.bundles` 决定 profile bundle 被纳入装配。外部 satellite row 则保留独立 entry。`familyIds` 可钉住历史发布 id；tests 断言 aggregate/standalone ids 不冲突、family id override 生效和行引用真实包。

`inactive` 生成 `disabled: true` override：这些包仍在 aggregate dependencies 中，row 也在 patch；“包已安装”“bundle 在 roster”“row 当前启用”是三种状态，不能合称安装成功。DSH `0.2.1-rc.3` upstream resolver 顺序读取 `dsh.profile.bundles`、包的 `dsh.bundle.patch` 并再叠 profile/user patches；本轮静态复核未实际执行 add 以验证现场写入链。

> **可迁移洞察**：聚合安装要分别验证 dependency resolution、bundle roster、effective row state。构建/解析成功不等于产品能力已挂载；分别用 manifest/lockfile、`--dump-config`/patch fold、effective enabled state 做自证。

### 2.4 更新和退役是同一套家族生命周期

`[SRC-TARGET]` `dsh-update` 以 aggregate package 为 anchor 汇总 family registry dependencies，执行 profile 中的 `pnpm update --latest` 后重新读版本验证；link/file development overrides 被跳过。包名迁移则由 `tombstones` / `retiredPlugins` 生成兼容 exports/registry，旧 shell-subpath 遇到退休插件时可成为 no-op。若旧导出已移除且无 tombstone，残留旧 row 可能在 import 时硬失败。更新器、tombstone 与 user migration 文档应作为一个发布/迁移生命周期设计，而不是三个无关功能。

> **可迁移洞察**：改变 bundle row identity 或 package topology 时，定义旧 identity 的过渡期和退出条件；兼容出口要有测试校验，并与家族更新/用户迁移步骤一同发布。

### 2.5 产品体验、安装提示与共存仍是文档主张

以下保留为 `[DOC]`：README 描述 `exit 0` 但 bundle roster 为空的半挂载案例、pnpm build approvals 的先后顺序、与被内置插件共存、默认皮肤/预设、商店/一键升级、桌面 `desktop` profile 入口和重启要求。该实现复核没有安装 npm/GitHub package、运行 CLI、试 pnpm hoisting 或启动 UI；这些项目行为仍未得到本轮 `[RUN]` 证据。产品卡可提炼其设计意图，但不能把文档案例改写成“本次已复现”。
## 3. 产品体验（文档描述，未实测）

- `[DOC]` 首次路径：安装 aggregate package → 重启 `dsh web` → README 声称侧栏出现功能入口并应用 Blue Fantasy 主题。
- `[DOC]` 日常/扩展：README 描述任务看板 cron、SSH、Git/worktree、会话归档、Token bank 与 Creative Workshop 的皮肤/宠物/预设。
- `[DOC]` 更新：README 描述侧栏/设置内显示 changelog 并一键升级；本卡目标源码核了 update family selection/verification，未运行更新过程。

## 4. 证据与边界

- **影响力**:**★ 9,865 / forks 608 / issues 3**(GitHub API,2026-10-31);**npm 近 30 天 99,694 次下载**(2026-09-30 ~ 10-29)。仓库 `stars.json` 的 2026-08-19 快照只有 4,661★ / 59,648 下载——**同一产品在两个口径下差一倍**,引用时必须写清用的是哪一个。它是**唯一一个"以聚合包形态"进本线影响力前列**的产品。
- **机制/文档分账**：目标实现和测试设计见[`04 源码复核`](./_证据/04_全家桶-dsh-web-源码复核.md)；旧 README 原文摘录见 [`01 产品聚合`](./_证据/01_产品聚合-原始挖掘.md) §二。README 体验 claims 仍是 DOC 级。
- **源码已核（TARGET v0.4.13）**：root `dsh-web` manifest private，指向发布 bundle `@linxin666/dsh-web-all`；`aggregate.yml` 是 patch/deps/rows/disabled/retirement 声明源，生成的 patch 使用 namespaced `web-ui-*` row ids 并挂真实 child package names。完整 package graph、生成链和测试范围见[`源码复核`](./_证据/04_全家桶-dsh-web-源码复核.md)。

## 5. 可迁移洞察

证据引用集中在本卡 §2 和[`04 源码复核`](./_证据/04_全家桶-dsh-web-源码复核.md)。DOC-only 体验主张保留为待验证场景，不作为机制已复现。

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 多插件需整套安装又保留单装 | 当成员包仍要独立安装时，把 package dependency 与 aggregate row identity 分开，聚合 rows 用独立 namespace。 | `[SRC-TARGET]` manifest/generator `namespaceId`、`familyIds`；`[TEST]` aggregate ID tests（读过、未运行）。 | identity 与包名解耦；代价是需维护 generator 与已发布 row ID 稳定性。 | 定义 package/row 两种身份、namespace、external deps。 | `web-ui-*` 是样本约定，不是通用前缀。 | ID 共用会重复注册/覆盖；已发布 ID 漂移会破坏用户 profile patch。 |
| Patch、依赖和 metadata 多处同步 | 当多个发布面来自同一产品声明时，以 aggregate manifest 为事实源并生成 patch/exports/metadata；加 drift check。 | `[SRC-TARGET]` `aggregate.yml` + `aggregate.mjs`；`[TEST]` aggregate tests（未运行）。 | 降低手工清单漂移；代价是 generator 成为发布关键路径。 | 定义生成物、外部手写依赖、check command 和发布 gate。 | generator pass 不证明任意 profile 都能 resolve tarball。 | 手改产物造成 manifest、patch、exports 与锁文件不一致。 |
| “包已装”不等于“功能已启用” | 分别建模并核验 dependency、profile bundle roster、effective row enabled 三种状态。 | `[SRC-TARGET]` inactive row 仍有 dependency/patch 且为 `disabled:true`；`[SRC-DSH]` rc.3 resolver 合并 bundle/user patch；半挂载仍是 `[DOC]`，本次未运行。 | 区分解析、profile reconcile、启用三层故障；代价是诊断需读回 roster/effective patch。 | 定义读回命令、部分成功处理与幂等 repair。 | `exit 0` 半挂载不是本次 runtime 复现，只能作测试场景。 | 只信 CLI exit code 会把未入 roster 的包误报成功。 |
| 旧 aggregate row/package identity 要迁移或退役 | 当发布物改变 identity 时，为已知旧身份留有期限的 tombstone/no-op 映射，并测试旧 profile import。 | `[SRC-TARGET]` tombstone/retired registry generator；`[TEST]` retirement consistency tests（未运行）。 | 避免旧 profile 因 import path 消失而启动硬失败；代价是维护过渡出口和清理期限。 | 编写 migration map、提示/无操作策略及回滚步骤。 | tombstone 不代替数据迁移，也不解决未登记旧格式。 | 删除过快会启动硬失败；永久保留会掩盖未迁移用户。 |
| 一组 family packages 需协同更新 | 当一个产品由多个依赖包组成时，更新器枚举 family、更新后读回版本，并区分 npm 与 link/file 开发态。 | `[SRC-TARGET]` `dsh-update/src/update.ts` family target/verification；updater 未运行。 | 降低包间版本漂移；代价是处理部分更新、lock 与失败恢复。 | 明确更新原子性、锁、部分成功状态和回滚策略。 | 此处源码细节针对 npm profile install 分支。 | 只升级 wrapper 会留下混合版本。 |
| 半挂载、共存、皮肤和重启体验 | 把 README 行为主张列成隔离验证场景；复现前保持 DOC/OPEN 等级，不包装成机制事实。 | `[DOC]` README claims；本次无 `[RUN]`。 | 保留产品洞察但不透支可信度；代价是需保留待测项。 | 用 scratch profile 固定 OS/DSH/pnpm，执行 add/dump/boot/restart/remove。 | 结论只覆盖已记录版本与配置。 | 把作者说明当现场保证会误导安装与迁移决策。 |

## 6. 已知边界与失效条件

**目标源码已确认（v0.4.13）**：

- aggregate family 混合 workspace packages 与四个 registry satellites；satellite 发布/版本是独立外部变量。
- package name 与 Loader row identity 分离；改变 `namespaceId` / `familyIds` 会触及已发布 profile identity，需同步 generator、测试和迁移出口。
- `tombstones` / `retiredPlugins` 只覆盖 manifest 已声明的旧身份；未知历史 export 不会自动兼容。
- updater 会校验目标 family dependency 版本，但不因此证明各 package 的行为兼容，也未显示对用户数据执行事务式回滚。

**README 主张，未运行验证**：pnpm isolated/GVS resolution、`minimumReleaseAge`、`exit 0` 半挂载、standalone 冲突、桌面 `desktop` profile CLI 限制与应用内安装步骤。本轮没有运行目标 package，均不能标为行为已验证。

**本次源码范围外**：商店和皮肤/宠物/预设资产存储与迁移、task-board daemon restart recovery、Windows/Linux UI/installer 体验。若这些决定卡片结论，应另开固定版本证据点或隔离测试。

## 7. 下一步复核

- [ ] 在一次性 DSH `0.2.1-rc.3` scratch home 核验 `dsh plugin add` 后 dependency resolution、`dsh.profile.bundles` roster 和 `--dump-config` effective rows；对比 pnpm 11 build approval 前后的安装结果与重跑行为。
- [ ] 在同一 profile 安装 aggregate 与代表性 standalone child，核验实际 row ID 共存及 `disabled:true` 如何被用户层覆盖。
- [ ] 在隔离 profile 做 v0.4.13 add/update/remove，观察 restart 前后 loader/client module 与 family version；保存命令输出和 config dump。
- [ ] 读取或复现皮肤/宠物/预设的存储路径与生命周期，并确认备份/迁移归属。
- [ ] 追 task-board daemon 的 profile/process restart recovery；README 只写“错过触发点跳过”。
- [ ] 若要声称跨平台可安装/运行，分别记录 Windows/Linux 的 pnpm 布局、profile resolution 和 runtime 结果。
