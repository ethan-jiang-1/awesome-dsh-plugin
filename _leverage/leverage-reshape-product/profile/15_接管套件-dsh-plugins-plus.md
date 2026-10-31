---
title: "接管套件 · dsh-plugins-plus"
domain: reshape-product
kind: sample
positioning: "`sidleo/dsh-plugins-plus`：一个 bundle 装两个「-plus」组件，按 preset 接管宿主自带的插件行。"
takeaway: "README 描述按 preset 接管 built-in rows；npm 0.2.0 源码 pin 尚未对齐，接管与回滚行为暂列概念参考。"
read_when: "要替换宿主自带实现；或要设计「按 preset 生效」的默认值管线。"
status: observed
updated: 2026-10-31
---
# 接管套件 · dsh-plugins-plus:不叠加能力，换掉宿主自带的那一行

> **研究范围**：npm `@sidleo3/dsh-plugins-plus@0.2.0` 的 registry tarball metadata、integrity 和版本化 README 已核；**尚未找到与该 tarball 对齐的目标仓库 commit/tag**。metadata `gitHead=b0f2337…` 实际 GitHub manifest 标 `0.1.8`，另一个 `0.2.0` 发布提交也不是 metadata `gitHead`，故本卡不引用目标 checkout 源码为 npm 0.2.0 的实现。DSH 通用接缝对照为 `@deepseek-ai/dsh@0.2.1-rc.3`。细节见[`06 源码复核`](./_证据/06_接管套件-dsh-plugins-plus-源码复核.md)。
> **证据成熟度**：产品概念为 `概念参考`；目标接管 planner、回滚、迁移和 HMR 只能按 `[DOC]`，不是目标包的机制参考；无 `[RUN]`，不能称行为参考。
> **类**:`1` 壳与工作台 · **层**:**4**（身份/preset）→ 5（默认值）→ 3（设置槽位）
> **采用信号**：★ 0 / npm 月下载 6,094（2026-10-31；npm 下载≠用户数；无目录收录）
> **一句话 [DOC]**：README 将其描述为一个 bundle，为两个 built-in discovery components 提供按 agent preset 的接管开关、preset 配置和 legacy import。
> **借鉴价值（概念级）**：**① takeover 应明确替换目标和作用域；② 默认不开启破坏性替换；③“恢复默认”、旧配置导入、已有 session 的生效时点都必须在文档中说明。以上是设计问题清单，不代表目标包 0.2.0 的实现已核。**

> **样本档案**
> **repo**:[`sidleo/dsh-plugins-plus`](https://github.com/sidleo/dsh-plugins-plus) · **npm**:`@sidleo3/dsh-plugins-plus` · **版本**:`0.2.0`
> **目录条目**:**无**（npm/repo 有发布声明，但本仓 `data/plugins/` 未收录）
> **装法**:`dsh plugin --profile <profile> add @sidleo3/dsh-plugins-plus` → 重启（README；本次未实测）
> **证据链**：README 摘录见[`02 产品形态`](./_证据/02_产品形态-原始挖掘.md) §一；npm tarball、`gitHead` 冲突、可确认的 DSH 通用契约及待补 provenance 见[`06 源码复核`](./_证据/06_接管套件-dsh-plugins-plus-源码复核.md)。

---

## 它想干什么 · 为什么值得借鉴

**意图。** 把宿主自带的 `agent-instructions` 与 `skill-filesystem` 两行换成**可配置版本**：AGENTS.md 扫哪几层、技能从哪些父目录找、顺序与预算——按 agent preset 分别生效。它不新增能力，只想让“默认值”变成“可调的产品”。

**意义 [DOC/OPEN]**：README 将产品定位为替换 discovery rules，而非新增工具能力。由于 npm `0.2.0` 的 `gitHead` 与 GitHub manifest 版本不一致，当前无法把仓库中任一 planner/HMR/rollback 实现认作该发布包源码；因此不能据当前 source claim“takeover 可逆机制已核”。

**用户价值 [DOC]**：README 称多项目、多 preset 用户可调整 AGENTS.md 与 skill search roots；本轮只能把它作为产品假设。其真实作用域、是否影响现有 session、失败/部分写入如何处理均待对齐版本源码或隔离复现。

**表达 [DOC]**：README 描述两个 component toggles 默认 disabled、通过 DSH Plus settings/log UI 操作。该项可以说明作者预期的保守启用体验，不能推断真实发布包中 default rows 与 UI 完全一致，待比对 npm tarball。

## 0. 一页速览(想抄的人只看这 20 行)

| 主张/实现面 | 可确认内容 | 证据边界 |
|---|---|---|
| 0.2.0 发布源码 | npm metadata 的 tarball `gitHead=b0f2337…`，GitHub 该 commit manifest 却是 `0.1.8`；`d85af4c` 发布 commit 是 `0.2.0` 但不是 tarball gitHead，源码对应关系未解决 | 不能将 d85af4c checkout / tests / CI 当作 npm 0.2.0 的源码事实。见[`06 源码复核`](./_证据/06_接管套件-dsh-plugins-plus-源码复核.md) |
| 接管算法/默认状态 | README 描述 core row + 两个 disabled component activators、preset takeover 和回退 | 均是 `[DOC]`，未取得与 tarball 对齐的 `[SRC-TARGET]` |
| 配置、unset、迁移 | README 声称 preset inheritance、`unset`、legacy marker 和逐字段导入 | schema/merge/idempotency 实现未知；不要改写为源码已核 |
| DSH 一般接缝 | rc.3 支持有序 patch layering、config editor edit/reconcile、session 使用创建时 preset composition | `[SRC-DSH]` 不证明目标插件正确调用或实际 UI 行为 |
| 测试/CI/运行 | npm metadata 有 smoke/build scripts；目标 gitHead 对应源码与 test 尚未找到；无 `[RUN]` | 只作概念参考，接管/回滚不能作机制或行为承诺 |

---

## 1. 它在产品里的位置

| 七层 | 动作 | 说明 |
|---|---|---|
| **4 身份** | 按 **agent preset** 决定哪套发现规则生效 | 同一个产品在不同 preset 里可以是不同行为 |
| 5 默认值 | AGENTS.md 的扫描层、技能的父目录清单与顺序 | 改的是"不配置时是什么" |
| 3 槽位 | 设置里的 `DSH Plus` 页 + 插件卡片 + 行配置三入口 | 同一份状态三种入口 |

### 1.1 它是 profile 侧的第 5 种形态:**接管型**

现有四张卡是四种"聚合"形态（全家桶 / 界面套件 / 组合包 / 聚合补丁）——**它们都在往里加东西**。这一张换了方向：

| 形态 | 动作 | 代表 |
|---|---|---|
| 全家桶 / 组合包 / 聚合补丁 | 把**多个插件**装成一件 | `dsh-web` / `dsh-suite` / `dsh-plugin-kit` |
| 界面套件 | 把**整套界面**换掉 | `codex-ui` |
| **接管型** | 把**宿主自带的实现**换掉，按 preset 生效 | **本卡** |

> **为什么算产品而不是"一个增强"**：它没有新增能力，而是重定义了 `agent-instructions` 与 `skill-filesystem` 这两行的**行为契约**（扫描层、父目录、预算），并把这套契约暴露成设置页。**改契约的是产品,加能力的是插件。**

### 1.2 它和 `14_聚合补丁` 的分工

`14_聚合补丁`（`hyzyn/dsh-plugin-kit`）用**一条 patch 挂 11 个插件**——那是"加法"的极致；这一张用**一条 patch 换 2 个内置行**——是"减法"。两者都在 `cordis.patch.yml` 上做文章，但一个增、一个替：

| | `14_聚合补丁` | 本卡 |
|---|---|---|
| 对内置行 | 不碰 | **停掉**并替换 |
| 配置落点 | 各自插件 | 核心行下的一个 schema |
| 回退 | 摘掉 patch 行 | **删掉覆写行**,让出厂层回来 |

---

## 2. 文档描述的接管设计与待核实现

**目标发布源码仍未对齐**：以下均为 `[DOC]` 产品承诺，DSH 通用行为另标 `[SRC-DSH]`。不要引用同仓 `0.1.8` checkout 推导 npm `0.2.0` 实现。

### 2.1 接管单位与 preset 作用域

`[DOC]` README 描述一个 bundle 含 core 与两个可独立启停组件；组件分别替换 `agent-instructions` 与 `skill-filesystem` 的发现行为，并按 agent preset 选择。README 声称组件 id 沿用 built-in row id 加 `-plus`，扩组件不增包。发布 tarball 是否确实只插入 activator、planner 是否按目标 preset row owner 写入，目前为 `[OPEN]`。

> **概念洞察**：替换型产品要让“替换谁、在哪个 scope、谁拥有覆盖值”在模型和 UI 中可见。命名成 `builtin-id-plus` 只是文档惯例，不能当 host id 稳定契约。

### 2.2 Config layering 与 unset

`[DOC]` README 称配置通过 profile `cordis.patch.yml` 和 DSH configForms/editor 管线，global/component preset 有继承关系，恢复默认用 `unset`。`[SRC-DSH]` rc.3 确有有序 bundle/profile/home/CLI patch layering、带 lock/reconcile 的 ConfigEditor；该契约只说明 host 支持这种写法，不证明目标包使用正确或 schema 中所有字段可 unset。

> **概念洞察**：覆盖值和继承态需要不同表示；移植时逐字段定义 owner、scope、inherit/reset 语义和 home/CLI overlay 冲突，而不是只给一个“默认值”按钮。

### 2.3 生效时间、回退与外部修改

`[DOC]` README 称关闭组件会移除 takeover、session 创建时固定 preset composition；两者的实际恢复范围、当前 session 是否刷新与 HMR transaction 顺序，没有可对齐 npm 0.2.0 的 target source。本卡不写“精确可逆”或“只影响新会话”为已验证事实。DSH rc.3 ConfigEditor 在候选值等于 lower layer 时可清理 override，且对 overlay 冲突/写失败有自己的拒绝和恢复规则；不能代替 target planner 验证。

> **待核洞察**：接管只能在能识别其所有权的配置行上回滚；若一个 preset override 同时含用户/其它插件字段，整体删除可能丢状态。确认前须做 foreign-edit 冲突与 rollback 测试。

### 2.4 Legacy import

`[DOC]` README 称会把旧独立包中的“尚未声明”字段导入新 schema，并用 `legacyImport` timestamp 控制一次迁移；旧文件留存。字段 allowlist、marker 与写入是否原子、失败重试、同一 home 多 profile ownership，以及旧 pipeline row adoption 均未能由目标发布源码确认，保留 `[OPEN]`。

> **概念洞察**：迁移规则需同时声明字段优先级、scope、重复执行语义和旧数据所有权；“导入一次”必须测试 partial failure 后重试是否幂等。

---

## 3. 产品体验（npm 0.2.0 README 主张，未实测）

### 3.1 首次使用文档流程

| README 描述的步骤 | 用户预期 | 当前证据界限 |
|---|---|---|
| 安装 bundle 后重启 | 安装本身不做 takeover | npm 0.2.0 README；未核对 tarball patch content |
| 打开插件页 | core row 存在；两个 component activators 显示开关 | README 声称；没有对齐源码确认 effective default rows |
| 开组件/配置 preset | 停用内置行、写 replacement；global/component selection 可继承 | README 声称；planner/inheritance implementation 暂不可与 0.2.0 对齐 |
| 查看日志 | 页内浮层/API 提供 pass/failure 记录 | README 声称；route/auth/redaction 未验证 |
| 关闭/回退 | 移除替换效果并让 built-in 恢复 | README 声称；只撤销 owner edits、保留 foreign config 等关键语义未知 |

### 3.2 可读性上的设计意图

`[DOC]` 安装默认不触发接管、设置里显示 preset/component 状态、将日志留在页内而非新窗口。可作为交互意图参考：先让用户看清作用对象和当前 owner，再允许替换宿主行为。实际 UI、桌面壳 `window.open` 限制、失败日志质量均未运行验证。

### 3.3 模型可见行为

`[DOC]` 产品文档称它改的是 discovery context（AGENTS.md / skill search roots），不是新增 tool。真实 session 中哪些 prompt/skill 变化、旧 session 是否保持快照，目标 `0.2.0` 源码未对齐，当前只能作概念定位。

---

## 4. 证据与边界

| 口径 | 值/范围 |
|---|---|
| GitHub | ★ 0 / forks 0 / issues 0（API 快照 2026-10-31；repo 较新） |
| npm | `@sidleo3/dsh-plugins-plus@0.2.0`；月下载 6,094（last-month，含 CI/镜像） |
| 目录 | 未收录于 `data/plugins/`；来自直接 npm/repo 发现 |
| release source pin | registry `gitHead=b0f2337…` 对应仓库 manifest v0.1.8；GitHub `d85af4c` 提交写 v0.2.0，但不是 `gitHead`，且没有 tag 与 tarball provenance 证明二者内容相同 |

**证据结论**：产品定位与交互为概念参考；npm `0.2.0` 的 takeover planner、migration、rollback 不能标机制参考，直到目标 tarball 源码与源码 pin 对齐。DSH rc.3 的 patch/config-editor/session 通用契约可独立引用，但不得代替目标实现证据。

**采用信号限制**：npm 6,094 不等于用户数；★ 0 / 下载倒挂无法仅凭公开指标解释，不能据此推断是发行版内置或 CI 来源。

---

## 5. 可迁移洞察

npm `0.2.0` 发布源码尚未与 GitHub source commit 对齐。以下表只提炼版本化 README 的**设计问题**，不把实现表述当作源码已证或直接进入 `BORROW.md`。精确 provenance 与缺口见[`06 源码复核`](./_证据/06_接管套件-dsh-plugins-plus-源码复核.md)。

| 触发问题 | 可迁移洞察（概念） | 文档依据 | 为什么可能有效 / 代价 | 移植时改什么 | 成立边界 / 待核 | 抄错后果 |
|---|---|---|---|---|---|---|
| 替换 host behavior 容易被误认为额外功能 | 命名和 UI 应同时说明“替换哪个能力、在什么 scope”；README 的 `builtin id + -plus` 只能作命名假设。 | `[DOC]` 0.2.0 README；源码版本未对齐。 | 让替换对象可发现；代价是依赖 host row identity 稳定。 | 对自家系统使用稳定 contract id，而非短期实现行名；显示 disable/enable 影响。 | 不能把该后缀当作 DSH 协议约定。 | host id 演进会令替换落空，或误替换不相干 row。 |
| takeover 有丢用户 config 风险 | 先展示 target/scope/diff，再执行有 ownership 的计划；绝不默认重写整份用户 preset。 | `[DOC]` README 对预览/接管的说明；target planner 未由 npm pin 证明。 | 透明的变更面降低恐惧；成本是实现 diff、冲突和 rollback。 | 定义目标字段 owner、foreign edit 策略与并发写保护。 | rollback 是否仅反转自有 edits 仍待 target source/运行核实。 | 全量写回会覆盖用户/其他插件的 preset 定制。 |
| 配置要支持恢复继承 | UI 将“恢复默认”语义设计为回到 inherited/default 层，而不是写一份静态默认值。 | `[DOC]` README 声称用 `unset`；具体 schema/persistence 未核。 | 上游默认可演进；代价是配置模型要区分 unset 与显式值。 | 为每个字段定义 inherit/empty/default 和迁移语义。 | 不是每个字段都必然支持 unset，须查 schema。 | 无法区分“继承”与“显式等于当前默认”，后续升级行为错误。 |
| 旧配置要合并进新 bundle | 迁移需要字段级 precedence、一次性 marker、可重试/幂等和保留原文件策略。 | `[DOC]` README migration notes；marker 原子性、字段 map 未核。 | 降低重复导入/覆盖；代价是处理 partial failure 和多 profile shared home。 | 定义 owner/scope、冲突处理、marker 写入顺序、恢复方式。 | npm `0.2.0` migration implementation 未验证。 | partial import 后重试重复覆盖，或多 profile 互相争夺一次性 marker。 |
| 配置改动有不同生效时点 | 在设置页和预览里明确区分 HMR/reconcile、当前 session state 与新 session snapshot。 | `[DOC]` README 声称只影响之后创建的 session；target + DSH call chain 未全核。 | 用户能判断何时看到效果；代价是说明/支持 session refresh semantics。 | 为每种状态定义何时读取、何时固化、能否重建。 | 当前 session 行为仍需 source trace / runtime test。 | 用户重复切换开关，以为没有生效或误以为旧 session 已更新。 |

---

## 6. 已知失效条件与验证缺口

目前目标 npm `0.2.0` 的内部行为仍属 `[DOC]`，以下为 README 主张/须核项，不表述为已观测 runtime：

| 情形 | 文档主张 | 尚缺证据 |
|---|---|---|
| 任一组件未选中 | 接管不生效 | target package 的有效默认 rows 未与 tarball 解包比对 |
| 已存在 session | 使用创建时 preset composition，新 session 才受改变 | DSH Agent 创建 preset snapshot 的准确调用点与目标端到端行为 |
| 关闭组件/恢复默认 | 移除 takeover，必要时清 preset override | foreign rows/自定义 override 是否被保留；npm 对应 planner 源未 pin |
| 旧 config 未存在或已导入 | migration 按 marker/已声明字段跳过 | marker 原子性、partial failure retry、多 profile 共享 home owner |
| 桌面 `window.open` 受限 | README 称使用页内 log overlay/API | route auth/scope、脱敏、桌面运行体验未核实 |
| 内置 row id / preset schema 演进 | 命名惯例要求 built-in identity 稳定 | ID 变更检测和 schema migration 未证 |

## 7. 下一步验证

- [ ] 取得能与 npm `0.2.0` tarball 对齐的 source provenance（当前 registry `gitHead` 指向仓库 0.1.8 manifest）。在此之前不把邻近 commit 的源码、测试或 CI 归给 0.2.0。
- [ ] 若取得匹配源码：核验 component defaults、planner diff ownership、ConfigEditor conflict/rollback、preset inheritance/unset、legacy marker/idempotency、多 profile migration、HMR/session snapshot 和 log API auth/redaction。
- [ ] 若要行为参考：在一次性 scratch profile 对两组件逐个启停、foreign row edits、保存失败/reconcile retry、legacy partial import、已有/新建 session 与桌面 log UI 做隔离实测。
- [ ] 采用量 6,094 与 ★0 的成因未知，不能据此推断 bundled installs 或实际用户数。
