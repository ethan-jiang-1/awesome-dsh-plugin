---
title: "闭环装配 · better-session"
domain: reshape-product
kind: sample
positioning: "`@morlay/better-session@0.1.10`：npm tarball 的五个精确依赖、patch rows 和 SQLite default 可查；会话闭环仍是 README 主张，源码 provenance 未对齐。"
takeaway: "npm 0.1.10 tarball 可确认 five-package exact dependency graph 与发布 patch rows/SQLite default；session lifecycle 与 rollback 保持 DOC-only，仓库源码未能 pin 到该版本。"
read_when: "要把多个自己的包装成一个产品；或要设计「一套闭环」的 bundle 边界与 preset 归属。"
status: observed
updated: 2026-10-31
---
# 闭环装配 · better-session:一个 bundle 就是一条闭环

> **研究范围**：目标 `@morlay/better-session@0.1.10` 第一方 npm tarball SHA-1 `e357b772…` / SHA-512 见[`07 源码复核`](./_证据/07_闭环装配-better-session-源码复核.md)；GitHub 无 tag、npm metadata 无 `gitHead`，可见源码只匹配后续 `0.1.11-alpha.0`，因此不把后续源码当本版实现。DSH 上游机制对照 pin 为 rc.3 commit `1f81c047…`。未安装、构建或运行目标。
> **证据成熟度**：发布 tarball 的 dependencies/patch rows/SQLite default 属 `发布物清单证据`；edit/retry/rewind/fork 状态机、DB schema、事务/恢复、slot 使用正确性仍是 `[DOC]` / `[OPEN]`，不是目标源码机制或行为实测。
> **类**:`1` 壳与工作台 · **层**:**3**（槽位）→ 5（默认值）→ 4（身份/preset）
> **采用信号**：★ 9 / forks 4 / issues 0；npm 月下载 8,561（2026-10-31，含 CI/镜像，目录外样本）
> **一句话**：npm 发布 patch 将五个精确版本依赖的 rows 组合成 better-session bundle，并给 `session-rdb` 行写入 SQLite path default；README 将它定位为 edit/retry/rewind/fork 闭环，后者实现语义本次未核。
> **借鉴价值**：**① 可借鉴“发布 manifest/patch 显式列出闭环依赖行”；② bundle 默认值不等于用户 effective config；③ README 中的“编辑不重放/重试重放”必须落实为不同状态转换并测试幂等、并发与副作用；④ preset 行清单不能归到本 bundle 0.1.10，需独立验证 sibling bundle。**

> **样本档案**
> **repo**:[`morlay/dsh-plugin`](https://github.com/morlay/dsh-plugin) · **npm**:`@morlay/better-session` · **版本**:`0.1.10`
> **目录条目**:**无**（仓库不在 `data/plugins/`；同作者另有 4 个 bundle 未进目录）
> **装法**:`dsh plugin --profile web add "@morlay/better-session"`（README 指示；未实测）
> **证据链**：早期 README 摘录见[`02 产品形态`](./_证据/02_产品形态-原始挖掘.md) §三；npm tarball、发布 patch rows、来源 pin 缺口及 DSH rc.3 对照见[`07 源码复核`](./_证据/07_闭环装配-better-session-源码复核.md)。

---

## 它想干什么 · 为什么值得借鉴

**意图 [DOC]**：版本化 README 将 bundle 描述为组装 edit / rewind / retry / fork 会话闭环，保留官方对话 shell 并向两个 slot 增加动作入口。该描述尚未由 0.1.10 匹配源码或 runtime 验证。

**意义 [发布物观察]**：npm 0.1.10 tarball 的 generated patch 显式把五个 exact package dependencies 与相应 row ids 放在一个 bundle，并给 `session-rdb` 行配置 SQLite default。由此可得“装配映射本身是可审阅发布物”的设计观察；不能延伸为实现一定完整、所有 rows 的 config 都同包，或状态机正确。

**用户价值 [DOC/OPEN]**：README 的闭环价值是把复杂子包名藏在一个安装单元后面；真实 edit/retry/fork 的确认、回滚、并发、durability、side effects 语义都待源码 provenance 或隔离测试确认。代价至少包括五包 exact-version compatibility 和 DSH slot/engine range 约束。

**表达 [DOC]**：README 称编辑只 rewind 到输入框不重放，retry 才重放，并有确认弹窗。是否 UI 实际采用该动作区分、是否正确提示外部 tool side effects，本次没有对齐实现源码。

## 0. 一页速览(想抄的人只看这 20 行)

| 主张/产物 | npm 0.1.10 可确认内容 | 证据边界 |
|---|---|---|
| 装配单位 | 一个 bundle tarball，有五个 exact dependencies 与五个 inserted patch rows | 发布 package metadata + generated patch；闭环行为是 README claim |
| 会话动作 | README 说 edit/rewind 回填不重放、retry truncate/replay、fork 新 session | `[DOC]`；无 matched source/`[RUN]`，不能声称状态机已核 |
| UI slots | README 提到 `conversation.chat.node` / `conversation.composer.dock`；patch 装入两个 UI packages | `[DOC]` + row 清单；slot contract/内部实现未核 |
| Patch contents | 插入 branch/rdb/message-actions/conversation-manager/reference rows，禁用四个 storage rows | 发布 generated patch 可读；不揭示实现和运行时结果 |
| 存储默认 | `session-rdb` row config 为 SQLite `$DSH_HOME/sessions/sessions.sqlite` | `[SRC-TARGET:发布patch]`；不是最终 effective config、workspace isolation 或备份保证 |
| Target source | GitHub tags empty、npm metadata 无 `gitHead`；可见源码为后续 `0.1.11-alpha.0` | 无 matched target source/test/CI；不从后续 commit 推断 |
| Dependencies | five exact versions: session-branch@0.1.9, session-rdb@0.1.9, manager/actions@0.1.10, dsh-reference@0.0.10 | npm 0.1.10 package metadata；对应源码实现未 pin |
| Sibling bundles | 早期 monorepo README 摘录列同作者五个 bundles；`mydsh-profile` rows 不在本 artifact | `[DOC]` only；sibling source/version 未作为本卡证据 |
| 可迁移洞察 | 将 dependency/row/default config 显式放进可审阅发布物 | 此处仅确认为 patch artifact；需检查每行 owner 与最终 effective config |
| Update channel | npm package 发布版本可见；未核 auto-update mechanism | `[OPEN]`；不要据此宣称 family update 保证 |

---

## 1. 它在产品里的位置

| 七层 | 动作 | 说明 |
|---|---|---|
| **3 槽位** | README 声称沿用官方 conversation shell 并注册两个 slots | package rows 可见 UI action/manager dependencies；内部实现未核 |
| 5 默认值 | patch 给 `session-rdb` row 指定 SQLite path default | 用户 effective storage config 可能被更高层覆盖 |
| 4 身份 | 同仓 sibling `mydsh-profile` 据 README/早期摘录包含 preset rows | 不属于 `better-session@0.1.10`；不得归入本 bundle owner |

### 1.1 它是 profile 侧的第 7 种形态:**闭环装配**

| 形态 | 装配单位 | 代表 |
|---|---|---|
| 全家桶 | 20+ 个自研 bundle | `dsh-web` |
| 界面套件 | 一个包、六个微内核 | `codex-ui` |
| 组合包 | 18 个独立插件 + 共享默认 | `dsh-suite` |
| 聚合补丁 | 一条 patch 挂 11 个插件 | `dsh-plugin-kit` |
| 接管型 | 替换宿主自带的行 | `15_接管套件` |
| 进口型 | 别人的套件 | `16_套件市场` |
| **闭环装配** | npm 发布 patch 显式组合的会话相关 package rows/config default；README 以一条用户闭环描述 | **本卡** |

> **一句话区分**：目标 README 回答“这组包意图支持什么会话 workflow”；本文可确认发布物组合，实际是否闭环仍待实现版本与 runtime 证据。

### 1.2 它和 `13_组合包` 的分工

| | `13_组合包`（`dsh-suite`） | 本卡 |
|---|---|---|
| 边界 | 18 个**独立**插件共享默认配置 | npm 0.1.10 artifact 依赖五个 exact package versions；README 称其提供一条闭环 |
| 版本 | 固定组件版本、整包更新 | 五个 exact versions 由 npm 0.1.10 package manifest 固定；source release parity 未知 |
| 配置 | 共享默认 | published patch 给 `session-rdb` row 声明 SQLite default；其余最终 config 需读宿主有效层 |
| 前端 | 各自改 | README 声称仅挂官方槽位；目标源码/运行未验证 |

---

## 2. 发布物中能确认的装配面与文档设计

### 2.1 README 描述的用户闭环（DOC）

| 动作 | 文档所述行为 | 尚未由目标实现验证 |
|---|---|---|
| 编辑 user 消息 | rewind 后回填输入框，不重放 | durable event/projection 如何截断、取消与重启一致性 |
| 重试闭合回合 | 重放输入，可用 `cascade: "truncate"` | 幂等键、tool side effects、并发 retry 的处理 |
| Fork | 从 `atSeq` 派生新 session，保留原会话 | event 前缀/metadata 的复制策略与并发 snapshot |
| 服务 API | `sessionEditor.retry` / `sessionBranch.rewind` / `forkFrom` | 权限、确认入口和服务内部事务边界 |

> **概念洞察**：编辑与重试应是不同操作：编辑回填让用户修改意图，重试才重放既有请求。副作用已发生时，rewind/truncate 不等于撤销外部副作用；必须把两者区别写入 UI 和数据模型。

### 2.2 发布 patch rows 和默认配置（发布物清单证据）

npm `@morlay/better-session@0.1.10` tarball 可确认：五个 exact dependency versions；patch 关闭四个 legacy/storage rows、设置 `storage-domain.backend=rdb`、插入 branch/rdb/message-actions/conversation-manager/reference rows，并为 `session-rdb` 声明 SQLite `$DSH_HOME/sessions/sessions.sqlite` default。

这证明**发布 patch 是可审阅的装配清单**，不证明 generator 的实现、所有有效配置层的结果、数据库 schema/事务、session lifecycle 或故障恢复。`rows` 此处属于发布产物，不应称为已读目标源码。

> **可迁移洞察**：把 bundle 的依赖、row id、默认 config 与 target version 放入可审阅/可校验的发布物；为 build pipeline 加 dependency-row parity 和 tarball inspection。若用户 override 可遮蔽 bundle default，安装说明需区分 package default 与 effective profile config。

### 2.3 Slot extension 与 preset 家族范围

`[DOC]` 0.1.10 README 声称保留官方 `ui-conversation` shell，仅注册 `conversation.chat.node` 与 `conversation.composer.dock` slots。npm patch row/name 可确认安装清单中包含对应 UI packages，但不能验证组件内部没有私有 DOM 依赖、slot props 稳定或运行时无冲突。

仓库/早期摘录另描述 sibling bundle `mydsh-profile` 复制并修改官方 preset rows。**这不是 `@morlay/better-session@0.1.10` 自身 patch 的内容**；本卡不能将其作为 better-session 的 ownership 或更新责任证据。DSH rc.3 patch layering 可确认 higher layers 能覆盖 bundle defaults，不能推出 slot/preset compatibility 已验证。

> **概念洞察**：扩展官方 UI 时优先依赖公开 slot，并为所需 props/contracts 留版本检查；家族中另一个 bundle 拥有的 preset 行要单独归档 owner，不能把整个 monorepo 责任归给一个 npm bundle。

### 2.4 数据和状态所有权目前开放

发布 patch 只声明 `session-rdb` 默认 type/path。session/event/projection/revision/turn/branch schema、序号分配、profile/workspace partition、migration、事务和 concurrency owner 均无法 pin 到 0.1.10 target source。SQLite 路径是存储位置 default，不是 workspace isolation，也不是加密/备份/原子性保证。

---

## 3. 产品体验（README 主张，未实测）

### 3.1 README 描述路径

| 时刻 | 文档所述 | 证据边界 |
|---|---|---|
| 安装 | 一条 npm bundle 命令带入五个依赖 | registry dependency graph + README；未执行安装 |
| 编辑/重试 | 确认后分别 rewind-to-input 与 replay/truncate | README 行为主张；无 0.1.10 matched source / `[RUN]` |
| fork | 从闭合 seq 派生 child session | README 行为主张；数据复制和并发语义未知 |
| 更换 storage | 修改 `session-rdb` config，默认 SQLite | 发布 patch row default；最终 effective config 未验证 |

### 3.2 可观察到的发布意图

npm tarball patch 显示 bundle 将五个包 rows 与 SQLite storage default 一起分发；README 把入口放在消息/回合边界。前者是发布物清单，后者是交互文案，二者都不能证明 UI 确认实际覆盖正确、重试没有重复 side effects 或 fork 后原会话不变。

### 3.3 模型与状态影响（DOC）

README 将该产品描述为改变会话状态而非工具集合；branch 为新会话，编辑与重试分别回填/重放。sibling `mydsh-profile` 的 preset 行删除和模型工具可见性不归属本 bundle；本轮不把它混作 better-session 的效果。

---

## 4. 证据与边界

| 证据类型 | 当前可确认内容 |
|---|---|
| GitHub / npm 采用信号 | GitHub ★ 9 / forks 4 / issues 0（2026-10-31）；npm `@morlay/better-session@0.1.10` 近 30 天下载 8,561（含 CI/镜像） |
| npm 发布身份 | tarball integrity、exact five dependency versions、Cordis peer 与 DSH engine range 见[`07 源码复核`](./_证据/07_闭环装配-better-session-源码复核.md) |
| 发布 patch | 能读到 generated `cordis.patch.yml` rows/SQLite row config；不等于匹配源码实现或最终 effective profile config |
| 目标源码 | **未能 pin**：GitHub tags 为空、npm metadata 无 `gitHead`；可见 source path commit 是后续 `0.1.11-alpha.0` |
| README | edit/retry/rewind/fork、slot 扩展和用户体验均为 `[DOC]`；未在 DSH rc.3 运行 |
| tests / CI / RUN | 没有匹配 0.1.10 source/test/CI 证据；本次未执行目标代码 |

**采用信号限制**：8,561 是一个 bundle 的 npm 下载，包含 CI/镜像，不代表用户数；其余四个 bundle 的相对下载量未采。

---

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 一个闭环依赖多个 packages | 以用户可完成的一条任务闭环定义 bundle boundary，并在发布 patch 显式列出 dependency rows/config。 | `[SRC-TARGET:发布物]` 0.1.10 dependency manifest + generated patch；README 将这五个包命名为 edit/retry/rewind/fork bundle。没有 matched package source。 | 一条命令即可引入协同资源；代价是 exact versions、row parity 与集成兼容需 release gate。 | 用 tarball inspection/manifest check 确认所有依赖 row 都已发布，锁定发布依赖。 | 该 bundle 下载与依赖图不能证明五步都在 runtime work；套件安全与状态机待测。 | 漏 row 会“装了 bundle 但闭环缺能力”；漂移版本会产生未知组合。 |
| 需要在官方对话 UI 加交互 | 优先选公开 slot 而不是 fork shell，发布前把 slot contracts 与 peer range 锁定。 | `[DOC]` README 称使用 `conversation.chat.node` / `conversation.composer.dock`；patch package rows 对应两 UI package；无 matched source/运行观察。 | 降低对整块上游 UI 的复制；代价是依赖 slot 的 props/生命周期稳定。 | 验证 slot props/types、mount/unmount、keyboard/focus、宿主升级和无 DOM 私有依赖。 | 目前只达“有此设计意图/row”证据，不可声称实现仅使用公开 API。 | slot 变更或隐式 DOM 假设会令 UI 静默缺失/破版。 |
| Bundle default 与用户最终配置易混淆 | 显示“包默认行配置”与“profile effective config”两级；支持读取回实际值。 | `[SRC-TARGET:发布物]` patch 对 `session-rdb` 设置 SQLite path；`[SRC-DSH]` rc.3 多层 patch merge。 | 用户能理解默认值来源和 override；代价是诊断要解释多层来源。 | 用目标 profile config dump + fold tests 验证 bundle/profile/home/CLI precedence。 | 本次没有安装，不能确认最终 backend/path。 | 把默认值当 effective config 会误判数据落点或备份范围。 |
| edit/retry/fork 涉及用户数据与外部副作用 | 分开“回填修改意图”“重放请求”“派生分支”，逐个定义 closure、side effect、取消、幂等和 durable commit。 | `[DOC]` README 对 edit 不重放、retry 重放、fork 新 session 的描述；没有目标 0.1.10 source/tests。 | 减少误重放并让确认行为可懂；代价是实现多种事务和副作用恢复。 | 设计 event/projection model、seq/revision IDs、write-ahead/atomicity 和外部 tool side effect 限制。 | 该卡无法证明 rewind/truncate 恢复外部状态；所有 lifecycle claims 需独立实现审计。 | 重试重复外部副作用、partial write 后 UI/DB 分歧、fork 丢失上下文。 |
| 多个领域能力被同一作者发布 | 领域 bundle 可单独安装；应独立维护 each bundle dependency/version matrix，不把 sibling package facts 混入一个产品证据范围。 | `[DOC]` 早期 README 摘录列五个 bundles；本次核验仅 `better-session@0.1.10` registry artifact。 | 减少单一巨包的可选成本；代价是兼容矩阵和发布节奏增加。 | 为每个 bundle 独立记录 npm version、integrity、rows、tests、peer range。 | 同 repo sibling `mydsh-profile` 的 preset 行清单不属于本 bundle 证据。 | 把 sibling facts 当本包实现，导致错误 ownership 和升级责任。 |

---

## 6. 已知失效边界与开放问题

| 触发/风险 | 证据状态 | 要验证什么 |
|---|---|---|
| Bundle 层设 SQLite，但 profile/home/CLI 覆盖存储 config | `[SRC-TARGET:发布patch]` / `[SRC-DSH]` layering | 安装后 dump effective `session-rdb` backend/path；不能只检查 bundle row。 |
| session schema 与迁移变化 | `[OPEN]`，缺少 0.1.10 matched source | pin `session-rdb` 具体 tarball/integrity/source，再查 schema version、migration/rollback、坏 DB 恢复。 |
| edit/retry 的 concurrent/interrupted writes | `[DOC][OPEN]` | 同 session 并发动作、取消/进程退出、写 event 与更新 projection 分离失败、磁盘满。 |
| retry 重跑有副作用的 turn | `[DOC][OPEN]` | 明确外部 tool side effect 是否去重/可补偿；truncate DB events 不是 undo 外部动作。 |
| Fork 的 boundary/source mutation 并发 | `[DOC][OPEN]` | child id conflict、事件前缀/metadata ownership、copy snapshot 与源会话并发写入。 |
| UI slot / peer range compatibility | `[DOC][OPEN]` | 按 DSH rc.3 实际 mount，检查 props/lifecycle、session actions 和 target peer support。 |
| preset rows / Agent Teams conflict | sibling bundle only; not this npm artifact | 如复核 `mydsh-profile`，另 pin 该 bundle 版本与 rows；不得归到 better-session。 |
| 目标 package source & CI | provenance gap | 取得 0.1.10 build commit/source map；否则 tests、schema、runtime claims 不升为 target mechanism reference。 |

## 7. 下一步复核

- [ ] 获取作者提供的 0.1.10 build commit 或可校验 tarball→source map；目前 GitHub 无 tag、npm 无 `gitHead`。
- [ ] 分别 pin 五个 dependency tarballs/source，追 schema、event/projection sequence、transactions、workspace partition 和 migration。
- [ ] 在 scratch profile 验证 effective storage config、确认 UI、edit/retry/rewind/fork、concurrency/interruption/restart 和 tool side effects；记录 DB dump/日志，不能碰用户 session DB。
- [ ] 仅在 evidence 对齐后更新 profile README/catalog 与可能的 BORROW 规则。
