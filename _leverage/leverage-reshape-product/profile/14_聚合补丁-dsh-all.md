---
title: "聚合补丁 · dsh-all（12 条 insert rows 装配 11 个成员）"
domain: reshape-product
kind: sample
positioning: "@hyzyn/dsh-all@0.1.73：精确依赖 11 个成员包、生成 12 条 insert rows；Profile 管理是 substantive member plugin，不是聚合包逻辑。"
takeaway: "0.1.73 发布物是 insert-only member rows + exact dependencies，另带 no-op runtime entry；Profile manager 的业务逻辑属于独立成员包。"
read_when: "要做聚合包/全家桶；或要理解 profile 产品的 bundle patch 怎么落地。"
status: observed
updated: 2026-10-31
budget: 170
---
# 聚合补丁 · dsh-all：12 条 insert rows 装配 11 个成员

> **研究范围**：`@hyzyn/dsh-all@0.1.73`，tag `v0.1.73` → commit [`2c6b35b`](https://github.com/hyzyn/dsh-plugin-kit/commit/2c6b35bbb50730b9781039d52fd24763e45cbc2e)；npm tarball SHA-1/SHA-512、dependency map 与发布 patch 均已对齐。目标源码/测试/CI 记录已读，未本地安装、构建或运行。完整引用见[`08 源码复核`](./_证据/08_聚合补丁-dsh-all-源码复核.md)。
> **证据成熟度**：aggregate manifest/patch/generator、成员/共享库依赖边界和 Profile member routes 可作固定版本 `机制参考`；README 的逐档兼容、安装/启停恢复及 Profile UI 体验不是本轮 `[RUN]`。
> **类**:`1` 壳与工作台 · **层**:3(槽位)+ 5(默认值)+ 7(分发) · npm 近 30 天 3,558 次下载（2026-09-30~10-29） · ★ 59 / forks 6 / issues 1（2026-10-31）
> **一句话**：aggregate package 有 12 条 insert rows（自身 `all` + 11 个成员）并 exact-pin 11 个 package dependencies；其空 `apply()` 仍会导出 no-op runtime entry。共享 kit 不作为 row/direct aggregate dependency，但由 10 个成员插件作为普通依赖引入；Profile manager 是有路由/文件操作的成员插件。
> **借鉴价值**：**① 聚合行为可以由 patch/dependency data 驱动，但“纯数据”要区分 no-op entry 与字面零代码；② shared library 不作为 Loader row/direct aggregate dependency，却仍由成员 package 普通依赖消费；③ insert rows 不等于改写/禁用宿主行，且同 profile 重复装成员会冲突；④ Profile 管理具有文件系统副作用时，应按独立 member plugin 审计 loopback/Host/Origin、路径校验、copy/install 回滚；⑤ 分面表可作为安装前用户影响面，但文档分类仍要逐项验证。**

> **样本档案**
> **repo**:[`hyzyn/dsh-plugin-kit`](https://github.com/hyzyn/dsh-plugin-kit) · **npm**:`@hyzyn/dsh-all@0.1.73` + 11 个成员 + 普通共享库 `@hyzyn/dsh-kit@0.7.3` · **许可证**:Apache-2.0
> **目录条目**:`data/plugins/hyzyn__dsh-plugin-kit--packages-*.yml`（成员逐包收录）
> **文档装法**:`dsh plugin --profile web add @hyzyn/dsh-all` 后重启；README 另允许按需安装成员。本次未实测。
> **证据链**：早期 README 摘录见[`01 产品聚合`](./_证据/01_产品聚合-原始挖掘.md) §三；精确发布 patch、profile side-effect 边界、test/CI/RUN 分账见[`08 源码复核`](./_证据/08_聚合补丁-dsh-all-源码复核.md)。

---

## 它想干什么 · 为什么值得借鉴

**意图 [DOC]**：固定 tag README 将产品描述为聚合包一次装配 11 个插件、另可逐成员安装，并提供 Profile 管理卡片和能力分面表。

**意义 [SRC-TARGET/OBS]**：0.1.73 的发布 patch 只有 insert rows（aggregate `all` + 11 成员），无 disable/override；代码有一个 no-op runtime entry，所以准确说是“业务行为由 rows/dependencies 驱动”，不是字面上没有执行代码。共享 `dsh-kit` 不作为 Loader row/direct aggregate dependency，但由十个成员包作为普通依赖消费。

**用户价值 [DOC/OBS]**：README 旨在让用户一次引入一组工具并提前看清各插件影响面。Profile 管理实际由 `@hyzyn/dsh-profile@0.2.13` 这个成员包实现，会对 profile 目录做创建/复制/改名/删除/安装等 filesystem 操作；它是 side-effectful runtime surface，不是无代码的聚合层。

**表达 [DOC]**：README 的分面表与启动命令复制是文档/界面意图。本次读到源代码和同 SHA CI 记录但未实际装包或启动 UI；Profile 操作成功路径不等于用户端恢复/数据安全已在本轮验证。源码映射的专用 create templates 是 `web` / `headless`；默认 `base` 是缺省路径，不应列作第三个显式模板。

## 0. 一页速览(想抄的人只看这 20 行)

| 主张/机制 | 固定版本证据 | 边界 |
|---|---|---|
| Patch 覆盖什么 | 0.1.73 published `cordis.patch.yml` 有 12 insert rows：`all` + 11 member ids；没有 disable/override | `[SRC-TARGET:发布物]`；重复装 aggregate 与 member rows 可能冲突 |
| 聚合包是否完全没代码 | `packages/all/src/index.ts` 有 `apply()` no-op 与空 inject，发布包仍导出 runtime entry | 行为由 patch/dependencies 驱动，但不是字面零运行时代码 |
| Shared library boundary | `dsh-kit@0.7.3` 不在 aggregate rows/direct deps；十个插件普通依赖引用它，`kit-settings` 是例外 | 不进 Loader roster ≠ 不会安装/执行；避免单例重复版本 |
| Member dependency parity | all package exact-pins 11 plugins；generator 从成员 package manifests 与 patch rows 生成依赖/挂载 | `[SRC-TARGET]` + `[TEST/CI]` same-SHA aggregate check 成功；本轮未本地运行 |
| Profile manager | `dsh-profile@0.2.13` 有真实 Node routes/filesystem operations、profile-specific ports | 单独的 member side-effect surface；不能归为纯聚合 patch |
| 兼容/体验 | README 列 11 个基线、按需安装和分面表 | `[DOC]`/manifest range 不是本轮兼容或用户 UI 实测 |

## 1. 它在产品里的位置

**七层坐标 `[DOC/SRC-TARGET]`**：3（成员插件提供 slots/tools）+ 5（`kit-settings` 配置面）+ 7（aggregate 与按需分发）。这是基于 README 和固定 package graph 的分类，不是本轮 UI 观察。

**三种聚合形态对照**:

| 形态 | 代表 | 聚合包的内容 | 用户感知 |
|---|---|---|---|
| 功能全家桶 | `dsh-web` | 20+ 自研包 + 商店/皮肤 | "换了一个产品" |
| 界面套件 | `codex-ui` | 单包六微内核 | "换了一套皮和设置" |
| **纯聚合补丁** | **本卡** | **12 条 insert rows + 11 exact member dependencies** | **"一条命令挂成员,界面主干仍为 DSH"** |

**成员产品面 `[SRC-TARGET]`**：`@hyzyn/dsh-profile@0.2.13` 提供 profile 管理 routes；README 称 UI 可列出/创建/复制/改名/删除并设置端口。源码只确认可选 templates `web`/`headless`，不提供名为 `base` 的显式 template；无 template 时走默认 base bundle 路径。

## 2. 机制与发布边界

### 2.1 Aggregate patch 是 insert-only roster

`[SRC-TARGET]` 0.1.73 aggregate patch 有 12 个 `insert`：自身 `all` row + 11 个成员 rows；无 disabled/override。`packages/all/src/index.ts` 只导出空 `apply()` 和空 inject，故准确说其行为是 patch/dependency-driven，同时随包带一个 no-op runtime entry。成员功能逻辑仍由各 plugin packages 提供；聚合 package 并非“压缩进一个插件实现”。

README 允许同 profile 单装成员或装 aggregate，但仓库明确提示不要同时装 aggregate/root bundle/成员，否则同一 Loader row id 可能重复。Insert-only 也意味着它不关掉 host builtin；新增资源与替换资源是不同产品语义。

> **洞察**：aggregate manifest/patch 应明确是“新增 row”还是“覆盖/禁用 row”，并测试与单包装配的组合规则。写纯 insert 并不能自动避免成员重复安装冲突。

### 2.2 Shared kit 不挂 row，但仍在 runtime dependency graph

`@hyzyn/dsh-kit@0.7.3` 无 patch，不在 aggregate 11 dependencies；10 个 member packages 将其列为普通 dependency（`kit-settings` 例外）。固定版本仓库以 `kit-pins:check` 防止多份 kit 拆成多个模块级 singleton。

库实现回环 HTTP guards、托管块、`!!js` 表达式与 service reading。其含义是“不作为独立插件 Loader row/direct aggregate dependency”，不是“用户 profile 中完全不会安装 kit 代码”。

> **洞察**：将跨插件共享服务做成库可消除重复实现；同时把 singleton 依赖版本纳入发布一致性门，避免同一进程加载多个实例。

### 2.3 Member risk surfaces are separate

README 的分面表将成员分为 model tools、system prompt additions、UI cards。这是 `[DOC]` 的用户影响说明，不能单独证明每项权限/副作用边界。Profile member 是明确的 runtime side-effect package：创建/复制/改名/删除 profile、写端口及执行 `pnpm install`；源码含 loopback/Host/Origin/body/path guards，并对复制失败回滚本次新建目录。

> **洞察**：在聚合安装前列出每个成员的 capability surface；对 filesystem/process/network 管理类成员单独做 threat model 和恢复审查，不能因 aggregate patch 本身很薄而把整套产品标成低风险。

### 2.4 Version compatibility and checks

0.1.73 package metadata 显式声明 11 个 DSH 基线与 `engines.dsh >=0.1.7-rc.2`；这是 compatibility declaration，不是每档 runtime proof。`aggregate:check` 重新生成并对照构件，校验 generator/manifest/patch/dependency 同步。

Same-SHA remote CI reports passing build/typecheck/test, publishability, package contents, kit pins and mount/headless checks；本轮未执行这些检查。它不能证明所有 user profile组合、按需 install 或失败修复事务。

> **洞察**：把依赖与 rows 的生成一致性做成 CI gate；把静态包一致性、宿主 mount smoke、交互/恢复测试分开报告，不要用一个绿色 workflow 概括所有兼容层。

## 3. 产品体验（文档主张，未实测）

- `[DOC]` README 指引 add aggregate、重启后使用；也允许逐成员按需安装。
- `[DOC]` README 分面列工具、prompt additions 和 UI cards；实际端到端 model/UI effect 本轮未启动验证。
- `[SRC-TARGET]` Profile member 源码有创建/复制/改名/删除、端口设置、copy/install 流程与安全校验；此处不等于本次点击 UI 操作成功或跨平台兼容。

## 4. 证据与边界

- **固定目标**：`@hyzyn/dsh-all@0.1.73`, tag `v0.1.73`, commit `2c6b35b`; npm tarball hash、dependency list、patch parity 见[`08 源码复核`](./_证据/08_聚合补丁-dsh-all-源码复核.md)。
- **采用信号**：npm last-month 3,558（2026-09-30~10-29，含 CI/镜像）；GitHub ★ 59 / forks 6 / issues 1（2026-10-31）。不同来源，不可用 60:1 推断用户数量或质量。
- **[TEST]** same-source tests/workflow 已读；**[CI]** GitHub same-SHA checks 为 success；**[RUN]** 本次无本地安装/build/运行。
- **已确认边界**：patch 是 insert-only；不提供成员开关或聚合级 enable API；单包/聚合重复挂载有 row id 冲突风险。Profile manager 的删除会递归删除目标 profile，虽有保留 web 和校验/回滚保护，也属于明确破坏性操作。
- **待验证**：任意 profile 的 add/reconcile/partial dependency failure、用户 override 与真实按需组合、Profile UI error/recovery、跨 OS filesystem behavior。本卡的同 SHA CI 不覆盖本轮用户配置。

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 11 个功能包要一键装齐又要保留单装身份 | 当成员仍独立发布时，用一个 aggregate package 精确 pin 成员 versions 并生成 insert rows；同时声明禁止 aggregate+member 混装或给 rows 做可检测冲突。 | `[SRC-TARGET]` v0.1.73 package manifest + generated patch：11 exact dependencies、12 insert rows、无 override/disable；`[TEST/CI]` aggregate generation consistency 有同 SHA pass。 | 便利入口复用成员实现；成本是更新 aggregate 版本、保持 dependencies/rows/id 三方一致。 | 设计 member identity、版本策略、row conflict gate、卸载/升级事务与 profile readback。 | 该样本自身仍会在同 profile duplicate install 时 row-id 冲突；patch 不做自动 reconcile/rollback。 | 重复装可能导致加载失败或同项注册冲突；手工修改生成 patch 会漂移。 |
| 跨插件共享 host seam 逻辑 | 将共享服务放普通 library dependency 而不是 Loader row；对 singleton-sensitive library 增加全依赖图 pin/duplication check。 | `[SRC-TARGET]` dsh-kit 无 patch/aggregate direct dependency，被 10 个 member plugins 普通 dependency 使用；`kit-pins:check` 有固定 CI gate。 | 共享代码不多出插件生命周期；成本是 peer/runtime resolution 和单例版本一致性。 | 明确 host library 的插件身份、普通依赖传播、peer/runtime compat 与单例检查。 | “不进 bundle row”不等于最终依赖树不安装库；不是所有库都需单例。 | 把共享库当插件会重复 activate；不 pin 单例依赖会拆状态或注册表。 |
| 用户不知道一键安装会改变模型什么 | 在 install 前逐成员标注 tools/prompt/UI、外部网络/文件副作用及权限，而非只列 feature names。 | `[DOC]` 固定 README 分面表；`[SRC-TARGET]` actual member package set and profile manager side effects；本轮未跑 UI。 | 用户可在安装前判断模型/tool surface；代价是需要维护 per-member impact manifest。 | 尽量机器可读化，按 package version 校验影响声明和权限。 | README matrix 不自动等于代码静态审计或有效权限列表。 | 装“界面套件”却意外新增可调用工具或 filesystem/network operations。 |
| 插件需要 Profile 管理 UI | 把 profile CRUD 做成明确的 side-effectful member boundary：loopback/Host/Origin 校验、名字/path containment、copy/install rollback、保护保留 profile。 | `[SRC-TARGET]` `dsh-profile@0.2.13` route/source；`[TEST]` tests；same-SHA CI green；本轮未运行。 | UI 直接管理隔离配置有用；代价是高风险 filesystem/child process surface。 | 威胁建模、CSRF/Host、路径穿越、删除确认、copy failure cleanup 和 pnpm/install cancellation。 | 源码 guard 与 CI 不能证明部署代理、真实浏览器或所有 OS 下的安全行为。 | 路径/请求验证缺口可改删错误 profile；只回滚新建目标，不能笼统承诺全操作事务安全。 |
| 需要对多个 DSH 基线给兼容承诺 | 分开记录 package `peerDependencies`、`engines.dsh` 与每个基线的真实 mount/render/test 状态；声明范围不是验证矩阵。 | `[SRC-TARGET]` package 明列 11 DSH peer slots；`[DOC]` README 宣称版本支持；`[CI]` fixed commit有真实 DSH mount/headless job。 | 发布门槛可发现 peer mismatch；成本是维护可重复基线矩阵。 | 为每个基线区分 metadata、build、mount、headless/UI 与故障测试。 | CI 行为受其固定 workflow/config 限制，不代表本轮或任意用户 profile pass。 | 把“peer range includes”误读成“用户环境已验证兼容”。 |

## 6. 已知失效边界与下一步验证

- **重复安装**：aggregate 与 member 插入同一 ids；同 profile 混装会冲突。卡片/README 应提供检测与迁移命令，不假设 loader 幂等。
- **依赖/row drift**：bundle 的精确依赖与 patch rows 来自 generator；source check 通过只说明 repo artifacts 一致。外部 registry 缺包、安装失败/部分写入未由本次 CI 证明自动回滚。
- **共享 kit**：未纳入 bundle row，但 member manifests 普通依赖 `dsh-kit@0.7.3`；若 pin 检查缺失，多版本可能拆模块 singleton。
- **Profile delete/copy**：代码保护 web、不删除既有目标、校验 path/host/origin，copy install failure 会回滚新目录；真实 OS permission、symlink、恶意浏览器请求、磁盘故障和用户数据恢复均未运行验证。
- **权限影响**：`tty`/`docker`/`loglens`/`codegraph` 等会增加 model-visible tools；只想改界面的用户不应默认开启此聚合。
- **Compat range**：11 档 peer 声明与 same-SHA mount CI 是不同证据；用户另装成员、不同 pnpm layout 或 profile override 需独立测试。

## 7. 下一步验证

- [ ] 在 disposable profile 分别验证 aggregate-only、member-only、aggregate+member duplicate；dump roster/effective config 并检查失败后 profile state。
- [ ] 用坏 registry dependency / pnpm install failure 观察 profile package.json、lockfile、node_modules 与 bundle roster 是否部分提交及 repair 命令。
- [ ] 对 Profile manager 在隔离 home 测路径冲突、copy/install failure、permission denied、rename/remove、web protection 与跨平台行为。
- [ ] 将 README impact matrix 与各 member manifest/actual tools/prompt/slots 对齐，保持用户可见副作用声明版本化。
