---
title: "薄基座 · dock"
domain: reshape-product
kind: sample
positioning: "dock-base@0.2.4：六类主要注册 API 只是 service surface 摘要；布局/设置存储为全局 localStorage，service dispose 不清所有外部 listeners。"
takeaway: "0.2.4 pins dock-base to source; registration disposers are identity-checked; layout/settings/floating geometry are activation stores on browser-global keys. Optional React has no proven missing-peer runtime fallback."
read_when: "要做平台型外壳/注册表；或要接别人的布局又不想改它。"
status: observed
updated: 2026-10-31
---
# 薄基座 · dock:把「槽位」做成一个薄基座

> **研究范围**：目标 `dock-base@0.2.4`，tag `v0.2.4` → commit [`8535f6e`](https://github.com/AKS1st/dock/commit/8535f6e24670931d9e93fb087ab474e38aa01856)，npm metadata `gitHead` 匹配；tarball SRI 已核 metadata、未下载作字节比对。DSH host 对照固定为 `0.2.1-rc.3`。源码/测试已读，未安装、构建、运行。详见[`07 源码复核`](./_证据/07_薄基座-dock-源码复核.md)。
> **证据成熟度**：服务 contract、disposer、store owner/recovery 与 UI effect 为固定 commit `机制参考`；optional React absence、实际浏览器 teardown、文件 sibling sandbox 和 0.2.x compatibility 仍 `[OPEN]`。
> **类**:`1` 壳与工作台 · **层**:3→6(平台化) · **采用信号**：★10 / npm 月下载1,673（2026-10-31）；本卡按“机制例外”收录（门槛见 [`00-map` §7](../00-map.md)）。
> **一句话**：dock-base 是一个无自身 dock-sibling dependency 的 workbench service/provider，功能由 sibling packages 注入；这次读到的 layout/settings state 是 browser-global，不是 session-scoped。
> **借鉴价值**：**① typed service contract + disposer per registration；② duplicate ID 明确失败、stale disposer 不删后来的 registration；③ memory fallback 与 storage persistence 区分；④ optional peer 声明不等于缺失时动态加载安全；⑤ escape hatch 与 host-layout hook 必须按有效 DOM selector / 上游公开 contract 验证。**

> **样本档案**
> **repo**:[`AKS1st/dock`](https://github.com/AKS1st/dock) · **npm**:`dock-base@0.2.4`（六个功能 sibling）
> **目录条目**:`data/plugins/AKS1st__dock.yml` 及 sibling 条目
> **装法**：README 指向 `dsh plugin --profile web add dock-base` 后按需安装 sibling；未实测。
> **证据链**：早期 README 摘录见[`01 壳与工作台`](./_证据/01_壳与工作台-原始挖掘.md) §二；固定源码、store/lifecycle、peer 和未验证边界见[`07 源码复核`](./_证据/07_薄基座-dock-源码复核.md)。

---

## 它想干什么 · 为什么值得借鉴

**意图 [DOC/SRC-TARGET]**：dock-base 0.2.4 自述为 workbench shell/provider，源码提供一组 `ctx.workbench` registry/service；功能文件树、编辑器等由 sibling packages 提供。不能据此说 package “没有任何具体能力”时忽略其自有 layout/settings/host UI。

**意义 [SRC-TARGET/OBS]**：fixed source 展示服务面、typed registrations 和 disposer；注册 ID 冲突显式 throw，disposer identity-check 防止旧 disposer 删除新 registration。对平台型生态，这比每个插件直接依赖具体 UI 实现形成更窄合作边界；代价是契约 schema 需版本治理且手工 vendored types 会漂移。

**用户价值 [DOC/OPEN]**：README 描述用户可只装基座或按需组合 sibling。代码显示部分 sibling 通过 `inject: ['workbench']`，workbench 缺席时不注册 file feature；但 React 被写作 optional peer、入口又静态 import React，缺 React 是否真能加载/只不激活 UI 尚未实测。

**表达 [DOC/SRC-TARGET]**：README 描述空 workbench、注册设置与可隐藏入口。持久状态在 global localStorage keys，不按 session/profile 隔离；坏 JSON/read exception 回 defaults、原 key 保留，写失败只 memory operation。布局碰 `data-turn-navigator` 之外还有 fallback selector，0.2.x grep 零命中不能单独证明偏移完全不生效。

## 0. 一页速览(想抄的人只看这 20 行)

| 主张/机制 | 固定版本证据 | 边界 |
|---|---|---|
| Target release | `dock-base@0.2.4`; npm gitHead matches tag `v0.2.4` / commit `8535f6e…` | Tarball SRI metadata read; bytes not downloaded/compared |
| Base service | Typed `ctx.workbench` registry, maps, snapshots/subscriptions, identity-checking disposers; duplicate IDs throw | Service `dispose()` itself does not clear every external listener; consumers still own their returned disposers/fibers |
| State owner/scope | layout=`dock:layout`, settings=`dock:settings`, geometry=`dock:floating-geometry:<viewId>` in browser localStorage | Global browser keys; not session/profile scoped. Corrupt/read failures default in memory, source key retained; writes can fail silently after in-memory update |
| `validate` | schema-invalid candidate is replaced/persisted as default; non-JSON/cyclic value rejected | Not a uniform “throw before write” gate |
| Optional UI peer | React/React DOM optional in manifest | client statically imports modules; missing-peer non-crash activation behavior remains OPEN, not runtime verified |
| Host layout | CSS keeps `data-turn-navigator` plus fallback selector for `nav[style*="--turn-natural-height"]`; DSH rc.3 also exposes `shell.leading` clearance variable | zero-hit grep for one selector alone does not prove no effect; no live DOM test |
| Filesystem sibling | `dock-base` itself has no filesystem route; `dock-files` `inject:['workbench']` and absent service returns early | dock-files route containment/sandbox was not inspected; don't infer security from “working directory” UI |

---

## 1. 它在产品里的位置

```
dock-base 0.2.4 (web UI shell + workbench provider)
├── dock-files       sibling consumer of workbench service
├── dock-editor      sibling package (README dependency)
├── dock-images      sibling package
├── dock-markdown    sibling package
├── dock-git         sibling package
└── dock-spreadsheet sibling package
```

| 层 | 动作 | 证据层级 |
|---|---|---|
| 3 槽位 | 自建 `ctx.workbench` service contract，由 sibling 插件注册 dock regions | `[SRC-TARGET]` |
| 6 平台化 | base 与功能包分开；base 无 dock-sibling dependency，dock-files 通过 `inject:['workbench']` 消费 | `[SRC-TARGET]` base + dock-files；其他 sibling 关系部分仍为 DOC |

“零内部依赖”只适用于不依赖 dock-sibling 包，不等于零 runtime/peer dependency；React 虽 optional peer，client entry 有 static import，缺失时能否不崩仍是 `[OPEN]`。上游 rc.3 同时有 `AppFrame/shell.leading` contract；目标 CSS 仍含私有选择器和 fallback selector，拓扑相似不等于 selector 必匹配。

---

## 2. 机制与可迁移洞察

### 2.1 Service registry contract 与 disposer ownership

`dock-base@0.2.4` 对外 `ctx.workbench` 不止 README 所列六个注册入口；另含 plugin metadata、layout/views/floating windows、open-path handler、queries/subscriptions。各 registration 由 Map/单槽保存，返回 identity-aware disposer；重复 ID 一般抛错，单槽 handler 仅在 disposer 仍拥有当前值时清除。Base client apply 先 provide service，后 mount UI effect；effect cleanup 卸 React root/style 并调 service.dispose，mount 异常 catch 后 cleanup。

**可迁移洞察**：当插件家族需要扩展注册表时，用稳定 contract、唯一 identity 和 disposer return，且让调用方 fiber 拥有 cleanup。需写明重复注册策略、slot replacement 与 service-wide dispose 是否连带清 subscriber。

> 本版 `service.dispose()` 不清所有外部 listeners；consumer 仍应自行释放返回的 disposer。测试源码覆盖部分注册/dispose 场景，但本次未运行。

### 2.2 Stores 的 owner/scope 与恢复

布局、设置与浮窗 geometry 三个状态放 browser `localStorage` 全局 keys；每 client activation 创建 store，无 session/profile partition。坏 JSON/read throw 回 defaults/empty memory view、原 key 保留；写时先更新内存，storage failure 被吞。设置候选 validation 与 mutation semantics 也不同：JSON-safe clone/schema failure 可替 default；non-JSON/cyclic set 会拒绝；未知 setting key 保留供未来注册恢复。

**可迁移洞察**：对每类状态分别标 owner/scope/lifetime，并区分腐坏读取、schema-invalid、不可持久化写入的可见反馈和修复方式。用户说“保存”时，memory mutation 不能冒充 durable success。

### 2.3 Optional peer 与 renderer entry

Manifest 将 React/ReactDOM 声明 optional peers；然而 v0.2.4 client entry 是静态 import。README 说“React 不在时 workbench UI 不激活”，但 package metadata/source 未证明 module resolution 在缺 peer 时能先进入该 fallback。

**可迁移洞察**：optional peer 用静态 import 时要测试 host loader 如何 materialize missing modules；如需 graceful no-UI,动态 import 或 host capability guard 必须位于触发该 import 之前。peer metadata 本身不是运行保证。

### 2.4 Layout integration / filesystem ownership

Target 0.2.4 style 对 dock clearance 匹配 `data-turn-navigator` 与 fallback `nav[style*="--turn-natural-height"]`。DSH rc.3 有 `shell.leading` clearance API，但此 source 未证实 dock 消费它；旧卡据单个属性 0-hit 断言“偏移失效”过强。File access 不在 base service：`dock-files` 有 `inject:['workbench']` 并在 provider 缺失时 return，但其 filesystem routes/auth/containment 本 memo 未审。

**可迁移洞察**：用 host-published layout contract 优先，若需 selector fallback就按每个 pinned host DOM 验证；security/path authority应归真正执行 filesystem route 的 sibling，不要从工作目录 UI 或 `openPath` 名称推断 sandbox。

### 2.2 契约怎么发给别人(没有 workspace 依赖时的土办法)

`src/client/contract.ts` 是工作台对外契约(`WorkbenchService`、`ViewProps`、`EditorOpenSeed` 等)。功能插件**只做类型导入**(编译期擦除),运行时全部走 `ctx.workbench`。而每个功能插件里有**一份 vendored 副本**,"改动本文件时需同步更新"。

代价被作者写明:改契约要**手动同步 5 份**。

> **抄这条判断**:跨包共享类型,在"没有 monorepo 依赖"的前提下只有三条路——① 发一个 `-types` 包;② vendor 副本 + 注明同步;③ 用 `import type` 从主包拿(需要依赖)。它选了 ②,因为 ② 不引入运行期与版本耦合。**选哪条不重要,重要的是把"要手动同步"写进 README**。

### 2.3 状态 owner、scope 和损坏/写失败恢复

`[SRC-TARGET]` `createLayoutStore` / `createSettingsStore` 各在一次 client activation 建立；layout/settings 分别落 browser-global `localStorage` keys `dock:layout` / `dock:settings`，closed floating geometry 另用 `dock:floating-geometry:<viewId>`。没有 session/profile key，所以 editor 的 `sessionId` prop 不会自动隔离这些 store。

- invalid JSON/read exception 会用 defaults 或空值继续，原 key 保留；
- writes 先更新内存后 best-effort localStorage，storage quota/availability error 被吞，刷新后可能丢失刚写入值；
- 未注册 setting 的值保留，后续 plugin registration 可读回；registration 时 raw candidate 经 JSON-safe clone/validate，失效值替换 default；普通 schema-invalid value 不一定 throw，而是可能 default + persist；
- `service.dispose()` 清除自身声明的 registries/subscriptions，但不无条件清空所有外部 `listeners`；consumer 仍须持有并调用 disposer。

> **洞察**：明确持久化 store 的 owner/scope，并分别定义 corrupt read、invalid field、storage unavailable 与 unload cleanup；“内存继续运行”不等于“写入已持久化”。这几个失败路径不可合并成笼统的 graceful fallback。

### 2.4 Host layout integration and fallback selector

`[SRC-TARGET]` v0.2.4 CSS includes the documented `data-turn-navigator` selector plus fallback selector `nav[style*="--turn-natural-height"]`; previous rc.3 full-tree grep returning zero hits only falsifies the first selector, not the fallback. `dock-base` adjusts position based on measured dock width + 24px and intends not to change page width/scrollbar; no live DOM measured this round.

`[SRC-DSH]` rc.3 exposes `shell.leading` and `--dsh-frame-leading-clearance`. That is an available upstream contract, but no evidence that dock 0.2.4 consumes it; do not describe dock as migrated to the official contract.

> **洞察**：prefer host-published clearance APIs over selectors; if a compatibility fallback is needed, test each selector against pinned host DOM, define zero-match behavior, and report that path separately.

### 2.5 Sibling activation and filesystem boundary

`dock-files@0.4.0` requires/injects `workbench`; if absent it returns without publishing file UI/service. Other siblings' precise manifests/source versions were not all pinned. `dock-base` has no filesystem route or workspace authorization; `openPath` only forwards a path to registered handler/view seed. File access is owned by sibling packages and must be audited there; the workbench API and “working directory” UI do not imply path containment or sandbox.

> **洞察**：shared UI base should define provider-absent behavior; security authority remains in the sibling that owns file/network routes, not in the navigation service.

---

## 3. 用户体验（README 描述，未实测）

### 3.1 安装与首次打开

README 指示先安装 dock-base，再按需 add siblings；描述初始空壳、dock settings、右键/设置逃生入口。此次未在 DSH profile 安装、mount 或验证插件管理面板。

### 3.2 几何与状态（文档值 vs 源码范围）

README 给出悬浮倍数、自动隐藏和预留空间规则；目标 v0.2.4 源码提供几何 clamps、localStorage stores 与 fallback selector。此处写清版本/来源，不把 README 默认值当本轮测量或把一个 selector grep 当实机布局结果。

### 3.3 逃生入口（README 主张）

隐藏 dock entry 后从设置或右键重开是 README 的交互承诺；源码/测试应逐路径核对。基座源码未证明真实 UI 下所有隐藏状态一定能访问，两条入口的宿主集成未运行验证。

---

## 4. 证据与边界

| 证据类型 | 当前结论 |
|---|---|
| Fixed target | `dock-base@0.2.4`, tag/commit `8535f6e…`; npm `gitHead` matches, SRI recorded but tarball bytes not downloaded |
| Host baseline | DSH `0.2.1-rc.3`, source commit `1f81c047…`; target declares DSH >=0.1.3-alpha.2 |
| Peers | Cordis required; React/React DOM optional in metadata, yet statically imported in client entry; absent-peer runtime outcome unknown |
| Tests/CI/RUN | Tests read, no workflow found at pinned tree, no local tests/run |
| Siblings | `dock-files@0.4.0` manifest/client pin read; other sibling release versions/provenance not exhaustively audited |
| Security | dock-base contains no filesystem route; dock-files routes not reviewed, so no filesystem sandbox claim |
| Host geometry | target 0.2.4 CSS retains `data-turn-navigator` plus fallback selector; rc.3 source exposes `shell.leading` clearance, but consumption/live DOM not tested |

---

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 一组独立功能需要共用工作台容器 | 建 service contract + typed registries；注册返回 disposer，调用方用自己的 lifecycle effect 托管。 | `[SRC-TARGET]` 0.2.4 `WorkbenchService`, map registries, identity-checked disposers; `[TEST]` duplicate/dispose cases only. | 减少基座依赖方向；代价是明确 registry id uniqueness/replacement policy 和 external listener ownership。 | 写清 API/add/update/remove/query/subscription、scope、dispose/order/duplicate behavior。 | 本仓 store/UI is activation-scoped; `service.dispose` 不会清外部 listeners set，consumer 仍需 disposer。 | 错误的 disposer 可删新注册项或留下 listener memory leak。 |
| 插件依赖可选 UI runtime | optional peer metadata 要和 import/activation path 一起验证；不能单靠 peer optional 推出缺失时不会 crash。 | `[SRC-TARGET]` manifest optional React peer but client entry static imports React/ReactDOM; README promises no-React no activation；没有 `[RUN]`。 | 可让非 UI consumers 少装 peers；代价是 bundler/loader module resolution 需兼容 optional peer absence。 | 动态 import/isolation, manifest optionality tests, actual peer-absent mount test。 | 本样本 runtime missing React behavior remains `[OPEN]`。 | 装在无 React profile 后 import-time crash，而非静默 UI inactive。 |
| 用户需要持久设置与布局 | 为 layout/settings/floating geometry 定义独立 keys、scope、schema version、read/write recovery与 reset policy。 | `[SRC-TARGET]` 0.2.4 stores: `dock:layout`, `dock:settings`, `dock:floating-geometry:<viewId>`; global localStorage, memory fallback. | 简单/跨 session preference 易用；代价是 profile/user/project boundaries不可混淆。 | 决定不同数据是否随 profile/session/workspace隔离，写失败反馈与 migration quarantine。 | 当前键是 browser-global，不是 per-session; storage write can silently fail after in-memory update。 | 路径/打开 tab跨 session 暴露或 UI显示“已保存”但刷新丢失。 |
| Settings values 要验证 | 把 schema validation 放在 mutation boundary，但明确 invalid candidate 是 reject、default-substitute 还是 retain，不要用一个 `validate` 字描述所有语义。 | `[SRC-TARGET]` register candidate invalid -> fallback default; `set` non-JSON/cyclic rejects, schema-invalid may default and persist. | 保证下游拿到合理值；代价是用户需知道数据为何被替换。 | 对每种 invalid class 返回诊断，设计恢复/修正 source of truth。 | 读损坏不会删 raw key；set failures may be swallowed. | 错误设置被静默重置，或坏原值持续回流。 |
| 需调整 host layout 几何 | 优先消费 host published CSS/slot contract；若保留 DOM fallback，为每个 selector 编写版本化匹配和 no-match behavior。 | `[SRC-TARGET]` dock 0.2.4 has `data-turn-navigator` + fallback selector; `[SRC-DSH]` rc.3 shell.leading clearance exists; no live match. | 约定接口降低结构耦合；代价是兼容测试和多路径维护。 | 对固定宿主 DOM integration test，检测匹配计数并提供安全 no-op。 | 单个 selector grep zero 不证明所有 fallback 不匹配；未运行浏览器。 | 偏移失效或命中错误元素，遮挡/挤压主 UI。 |
| Workbench file service 需要安全边界 | 把 path authorization/containment 放在真正拥有 filesystem route 的 sibling；base `openPath` registry 只负责路由，不是权限检查。 | `[SRC-TARGET]` dock-base no fs server route; dock-files implementation not audited here. | 明确 security owner；代价是用户需要审查 member route implementation。 | 每个操作做 canonical containment, symlink policy, auth, audit and recovery tests。 | 本 memo 未审计 dock-files sandbox；不得声称文件树限于 workspace。 | 不受信任的 sibling 可访问宿主用户可达路径。 |

---

## 6. 已知失效边界与下一步验证

- Missing React: metadata says optional peer, but static imports exist; run in disposable profile without React to observe loader behavior.
- Storage read corruption falls back to defaults/memory without deleting raw key; storage write errors are swallowed after memory updates, so refresh can lose unsaved state.
- Registry duplicate IDs throw; replacement requires old registration disposal first. External service listeners must unregister themselves.
- `data-turn-navigator` is absent in rc.3 grep, but dock 0.2.4 includes another nav style selector; only live DOM/runtime can establish whether clearance adjustment matches.
- `dock-files@0.4.0` returns early without `workbench`; its actual filesystem routes/security were outside this memo. Do not infer workspace sandbox.
- No CI workflow was found at dock-base pinned tree; tests exist but were not run; npm tarball bytes not compared to the source tree.

## 7. 下一步复核

- [ ] In a disposable DSH rc.3 profile, test with/without React peers, mount/unmount/restart and verify cleanup and UI recovery.
- [ ] Inspect all sibling package manifests/releases before generalizing installation order; specifically audit dock-files filesystem routes and DSH authorization/sandbox boundary.
- [ ] Download/verify dock-base@0.2.4 and dock-files@0.4.0 tarball SRI, compare packaged files to pins.
- [ ] On actual rc.3 DOM, check both host clearance selectors and right/left dock dimensions; keep fallback-to-no-op behavior documented.
- [ ] Run existing tests only in a disposable checkout; there is no repository CI evidence at pinned base commit.
