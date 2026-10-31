---
title: "组合包 · dsh-suite（18 个插件一次装）"
domain: reshape-product
kind: sample
positioning: "@stardustlc/dsh-suite@0.9.1：18 个精确依赖/insert rows 与 defaults；同包 updater 按 profile 管理偏好和受控整包更新。"
takeaway: "0.9.1 精确 pin 18 个 direct deps/rows；updater 的偏好按 profile 存储、自动安装 opt-in，并以补偿恢复而非原子事务处理失败。"
read_when: "要把自己的多个插件打包成一件交付；或要判断聚合包和发行版的区别。"
status: observed
updated: 2026-10-31
budget: 165
---
# 组合包 · dsh-suite：策展、钉版本、注入默认值

> **研究范围**：npm `@stardustlc/dsh-suite@0.9.1` 的 SLSA provenance 将发布 artifact digest 绑定到 commit [`b904373`](https://github.com/STARDUSTLC666/dsh-suite/commit/b904373fb644d0d6aaa8f1b7bd7d5d3c9bf1464a)；没有 `v0.9.1` tag，采用 provenance commit 作为源码 pin。源码、测试与 same-SHA CI 记录已读；本次未安装、构建或运行。完整来源见[`09 源码复核`](./_证据/09_组合包-dsh-suite-源码复核.md)。
> **证据成熟度**：release dependency/rows/defaults、profile-scoped updater state/policy 与补偿式恢复可作 `机制参考`；测试未运行，真实升级、partial failure 与 UI 仍非本次行为观察。
> **类**:`1` 壳与工作台 · **层**:3(槽位)+ 5(默认值)+ 7(分发) · npm 月下载 8,230（2026-09-30~10-29） · ★ 3（2026-10-31）
> **一句话**：0.9.1 用 18 个 exact direct dependencies/insert rows 组合组件与默认 config；updater 按 profile 保存状态，只允许经门控的自动 stable patch 更新，并用旧版本 reinstall 做补偿恢复，不是事务式 atomic update。
> **借鉴价值**：**① exact direct deps 不等于 transitive lockfile/reproducible tree；② bundle defaults 是 lower layer，effective config 需合并 profile/home/CLI；③ updater 的 check/consent/idle gates 与 per-profile state 要同 owner；④ suite-member update 要抑制重复独立更新；⑤ install/update failure recovery 是 compensating workflow，会有 crash window；⑥“共同加载”声明不能从精确版本号单独推出。**

> **样本档案**
> **repo**:[`STARDUSTLC666/dsh-suite`](https://github.com/STARDUSTLC666/dsh-suite) · **npm**:`@stardustlc/dsh-suite@0.9.1` · **许可证**:MIT
> **目录条目**:`data/plugins/STARDUSTLC666__dsh-suite.yml`（`workflow`）
> **文档装法**:`dsh plugin --profile desktop add @stardustlc/dsh-suite` 或将 profile 换为 `web` → 重启；README 另列桌面插件面板安装（本次未实测）
> **组件**：18 个精确版本 direct deps；Review 与 Computer Use 独立提供（按该版本 README）
> **证据链**：README 摘录见[`01 产品聚合`](./_证据/01_产品聚合-原始挖掘.md) §三；固定 artifact/source/update recovery/CI 复核见[`09 源码复核`](./_证据/09_组合包-dsh-suite-源码复核.md)。

---

## 它想干什么 · 为什么值得借鉴

**意图 [DOC]**：固定 0.9.1 README 将它描述为 18 个组件的组合包，提供共享配置、整包更新；组件可单装，Review / Computer Use 另列。该 README 不证明用户环境已共同加载成功。

**意义 [SRC-TARGET/OBS]**：0.9.1 manifest exact-pins 18 个 direct packages；`cordis.patch.yml` 有 18 inserts，并为若干行写 defaults。Suite patch 是配置 owner，成员包仍拥有功能实现；额外 `ptc-minimal.patch.yml` 则是 preset composition。组件直接版本精确，不代表完整 transitive dependency tree 可复现（未提供 consumer lockfile）。

**用户价值 [DOC/OBS]**：一项可核的价值是将 18 个明确版本、rows 和默认 config 通过一个 bundle 发布；README 的“共同加载检查”未在本轮重现。updater 的机制另有 per-profile preferences、自动安装 opt-in、idle/consent gates 与补偿恢复；它不是无条件 background update。

**表达 [DOC]**：README 描述原生插件列表中展示 suite 与组件图标、按需安装、由用户选择何时重启。本轮源码复核覆盖 updater/profile logic，但没有执行 DSH UI 或 package install。

## 0. 一页速览(想抄的人只看这 20 行)

| 主张/机制 | 固定版本证据 | 边界 |
|---|---|---|
| Bundle contents | `package.json` exact-pins 18 direct members；`cordis.patch.yml` inserts 18 rows with selected defaults | `[SRC-TARGET]` 0.9.1 tag/source；generated artifact proves rows, not member internals |
| Version reproducibility | All 18 direct dependency strings are exact semver | No consumer lockfile/transitive freeze implied; exact direct pins alone do not reproduce all transitive deps |
| Defaults and ownership | Suite patch owns bundle-layer defaults; members own actual features. `ptc-minimal.patch.yml` contains a preset composition | DSH higher patches can override; effective values depend on full profile bundle order/user patches |
| Updater | Per-profile state/cache; checks opt-in per package; auto-install disabled by default; stable patch-only auto policy; Suite members suppressed as separate update targets | Exact version install + host compatibility checks; rollback is compensating, not atomic |
| Failure/recovery | Failed/cancelled update attempts reinstall previous exact version/enabled state; restore-failed/unknown block retry for manual repair | Crash between package-manager steps may leave partial state; no automatic restart; tests read, not run |
| Compatibility and UX | README enumerates supported DSH baselines, install/restart steps, per-profile plugin display | Manifest range and remote CI not this session's real compatibility/UI observation |

## 1. 它在产品里的位置

**七层坐标**:**3**(槽位:18 个组件各自的面板)+ **5**(默认值:共享配置补丁)+ **7**(分发:一条命令、整包更新)。

**它和 `dsh-web` / `codex-ui` 的区别**:

| | `dsh-web` | `codex-ui` | **本卡** |
|---|---|---|---|
| 卖什么 | 功能广度 + 自家商店 | 界面深度 + 伴侣管理 | **策展 + 默认值 + 版本钉死** |
| 界面是否统一 | 是(自有导航/主题) | 是(整屏重做) | **否**(18 个组件各长各的) |
| 组合方式 | 自研 20+ 包 | 单包六微内核 | **别人的 18 个包 + 一条组合补丁** |

**一句话**:它证明 profile 级产品还有第三种形态——**不重做界面,只做"装什么、默认怎么配、版本怎么锁"**。

## 2. 机制与状态生命周期

### 2.1 Bundle patch 和 defaults 的 owner

`[SRC-TARGET]` 0.9.1 `package.json` 列 18 个 exact direct dependencies；`cordis.patch.yml` 插入 18 个成员 row，并在若干成员 row 上设置 default config。patch comment 允许 profile user patch 以同 id 覆盖。这是 bundle lower-layer config，不等于 profile 最终 effective value。`ptc-minimal.patch.yml` 是独立 preset composition patch，不能与 18 个组件 patch 混作一个标量“共享默认”。

> **洞察**：聚合包可以策展成员版本并携带 defaults；同时应展示配置 owner 和覆盖顺序，避免用户把 package default 当最终 runtime state。

### 2.2 Direct pin 与完整复现不是一回事

18 个 direct dependency 字符串都是 exact version，没有 `^`/`~`；registry 组件 updater 从兼容 releases 中选 exact target 再调用 host package manager。npm metadata 无 consumer shrinkwrap/lock graph，因此 direct pins 未冻结每个 dependency 的 transitive graph。

> **洞察**：若产品声称可复现，应写清 pinned level：direct package versions、完整 transitive lock、registry integrity、Node/DSH peer range各是不同保证。

### 2.3 每 profile updater state、admission gates 和 restore flow

Updater coordinator 由 profile context 注册；preferences/cache 放目标 profile directory。每组件有 `checkEnabled`、`autoInstall`、`deferredUntil`、`ignoredVersion` 等 state，默认 check enabled、auto-install disabled；revision-checked lock + atomic temp-file rename 写偏好，坏 state fail-closed 并保留供 repair。

自动更新仅针对 enabled/healthy/registry package、非 suite-managed member、stable patch bump；还需用户 consent、host agents/jobs idle、client heartbeat/page clean/busy checks、quiet window/no pending restart。manual install 需明确确认。版本 metadata、digest/integrity、engine range 被核后才安装。Suite 内成员由 suite-managed status 抑制单独更新，避免同包两套入口。

更新优先走 host `updateBundle`; rc.3 fallback 保存原 exact version/enabled state，remove→install exact new，失败/取消则 reinstall old exact 版本。恢复失败标 `restore-failed`，未知操作标 `unknown`，需用户去官方 manager 核查并修复；进程 crash 位于 remove/install/restore 中间仍可能留下 partial state。该机制是 compensating workflow，不是 package manager + DSH config 的原子事务。

> **洞察**：多包组合更新要有 owner-aware update suppression、install 前再次验证 digest、记录旧状态并提供显式补偿流程；不能把“更新失败回滚”简化为原子事务保证。

### 2.4 DSH profile 层和冲突边界

DSH rc.3 bundle patch 按 profile 声明顺序叠加，用户 patch 在其后；Suite row defaults 可以被 higher layer 覆盖。Aggregate rows 都是 `insert`；若同 profile 还装独立成员/另一个聚合包并写同 ids/config，仍可能重复或由层序决定 effective config。没有 universal conflict checker。

> **洞察**：在 profile 安装 UX 中显式检测同 id/同 package 的重复来源；分别解释“包已安装”“row 入 roster”“row 是否 enabled / config 最终值”。

## 3. 用户体验（README 主张，未实测）

- `[DOC]` README 描述 add + restart 后看到 Suite/18 个成员、按需配置、Suite 级更新及用户决定 restart；本次未安装或打开 DSH UI。
- `[SRC-TARGET]` updater code 有 profile-specific state/UI routes 和手动/自动 update policy；不等于 README 所述每个组件面板的实际呈现已运行验证。

## 4. 证据与边界

- **目标 pin**：`@stardustlc/dsh-suite@0.9.1`；SLSA provenance ties tarball digest to `b904373fb644d0d6aaa8f1b7bd7d5d3c9bf1464a` / publish run `41022121732`；没有 `v0.9.1` tag。详见[`09 源码复核`](./_证据/09_组合包-dsh-suite-源码复核.md)。
- **采用信号**：npm last-month 8,230（2026-09-30~10-29，含 CI/镜像）；GitHub ★ 3（2026-10-31）。不同口径，不解释为“用户装了就走”。
- **[TEST]** 固定 commit tests 有 updater policy/state/restore cases；本轮未运行。
- **[CI]** same-SHA Node 22/24 tests/validate/release checks success；不是本轮 local reproduction。
- **[RUN]** 无；没有真实 profile/package-manager UI 和失败恢复的 end-to-end 行为。
- **风险边界**：exact direct dependency strings 不等于完整 transitive freeze；update compensation 不是 crash-atomic；insert rows 与其他包重复时没有全局 conflict checker；peer/engine declaration 不等于 11 档兼容实测。

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 多个独立插件要共享默认并成套交付 | 用一份 bundle manifest/patch pin direct dependency versions、rows 和 defaults；继续允许成员独立安装时要显式定义重复来源冲突。 | `[SRC-TARGET]` 0.9.1 `package.json` 18 exact deps + `cordis.patch.yml` 18 inserts/configs。 | 一次策展并保持 direct package compatibility；代价是每次成员升级都需重发 suite，且 direct pin 不锁 transitive graph。 | 同步 rows/dependency map、兼容条件、用户 override 与按需 install policy。 | target README 的“共同加载”并不等于当前组合实测；profile layers 仍可覆盖默认。 | 独立装与 aggregate 冲突，或成员间不兼容却被精确直依赖掩盖。 |
| 用户要“安全的自动更新”而不是静默漂移 | 按 profile 保存 updater preference；默认 auto install off；只对已授权、healthy、idle 的 stable patch change 自动更新，并提供人工确认路径。 | `[SRC-TARGET]` updater policy/store；`[TEST]` idle/dirty/stale/consent tests；`[CI]` same-SHA pass, not local run。 | 把无人值守风险限制在较窄范围；代价是 host activity signals 和 UI state 的持续维护。 | 定义 package source allowlist、fresh metadata recheck、profile owner、用户 consent 和 restart status。 | README general “整包更新”需与源码 updater 实际 target/admission 区分。 | 简单 `update --latest` 会破坏活动 session/本地包/需人工审批版本。 |
| Package manager 更新存在 remove/install partial failure | 记录原 exact version/enabled state，更新失败时做 compensating reinstall；恢复失败/未知状态阻止自动重试并引导人工修复。 | `[SRC-TARGET]` NativeInstaller fallback/coordinator restore states；`[TEST]` restore exact version/enabled / restore-failed tests。 | 相比盲重试，保留可诊断的旧状态目标；代价是多步操作不原子，crash window 仍存在。 | 为每一步定义 durable operation journal、取消语义、recover/resume/unknown、用户重启要求。 | 该逻辑依赖 DSH host `updateBundle` 与 plugin manager contracts；本次未真实触发错误。 | 把补偿恢复误称事务回滚，会忽略 remove 后 crash 导致的半安装。 |
| Updater 与 Suite/member 出现重复 ownership | suite-managed member 从独立 update target 中抑制，防止同一包被两条更新流程同时处理。 | `[SRC-TARGET]` `targets()` marks `bundledBy: Suite` / skip member update; `[TEST]` duplicate suppression. | 单一更新 owner 减少竞态；代价是 suite 更新器故障会阻挡 member 独立更新。 | 明确谁是版本协调 owner，以及解除套件管理的迁移流程。 | 同名/同 id 的第三方 aggregate 不一定能被识别。 | 两个 updater 竞态覆盖/回退对方刚装的版本。 |
| Suite defaults / peer range 被当作 compatibility guarantee | 区分 exact direct deps、`engines.dsh` minimum、peer declaration、CI mount matrix 和 consumer lockfile。 | `[SRC-TARGET]` package metadata; `[SRC-DSH]` rc.3 patch layering; `[CI]` Node 22/24 workflow runs。 | 让“兼容”的含义可审计；代价是维护每项基线和 transitive graph evidence。 | 发布实际验证矩阵，标注 metadata-only 与 test/mount passed，给 users effective config dump。 | same-SHA CI 不是本轮测试，也不覆盖任意 user profile composition。 | 把 peer range 当兼容证明会在未测 host/profile 中失败。 |

## 6. 已知边界与降级

- **外部 prerequisites**：README 称邮件/日历需 account、media packages 需本机环境；bundle 只能组合依赖，不能创造 credentials / OS executable。
- **Security/update lag**：exact direct pins 让组合版本一致，但上游 security fixes 不自动进入；须发布新 suite version。transitive dependencies 仍要看实际 installer lock/registry resolution。
- **Profile patch conflicts**：same-id user/home/CLI override 可以改变 bundle defaults；其他 aggregate 插相同 row ids 可能重复或覆盖，目标没有 universal conflict resolver。
- **Updater restore failure**：若 compensating reinstall 失败或操作状态不确定，更新阻塞在 `restore-failed` / `unknown`，需官方插件管理器检查并重启；不要把它写成无缝自动 rollback。
- **Restart**：source 明确不会强迫 DSH restart；pending restart 是 gate。用户可保留新包但仍运行旧加载态，须让 UI/doc 清楚显示。

## 7. 下一步验证

- [ ] 运行前固定一份 scratch `web` profile：安装 suite，dump bundle roster/effective defaults；单装其中一个 member 与 suite 同装，观察重复 row/collision handling。
- [ ] 注入 install fail/cancel/restart at each update stage，核对 preferences state、installed exact version/enabled、`restore-failed/unknown` repair instruction。
- [ ] 检查 manual vs auto update gates、pending restart、profile switch、active job/page changes；这是安全/一致性行为，源码测试不能替代 host run。
- [ ] 对 18 package transitive resolution 记录 lockfile/registry integrity；exact direct dependency pins 不够支撑完整 reproducible install。
