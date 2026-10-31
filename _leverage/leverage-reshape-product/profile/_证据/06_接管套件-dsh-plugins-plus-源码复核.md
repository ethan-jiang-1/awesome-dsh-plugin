---
title: "源码复核：接管套件 dsh-plugins-plus"
domain: reshape-product
kind: evidence
positioning: "核验 profile/15 的目标发布坐标、接管/回退、preset 配置与迁移主张；目标源码无法与 npm 0.2.0 的 gitHead 对齐时不推断。"
read_when: "复核 profile/15 的接管算法、配置 ownership、回滚、迁移幂等与旧 session/HMR 语义。"
status: observed
updated: 2026-10-31
---
# 源码复核：接管套件 dsh-plugins-plus

> 只读第一方 GitHub、npm registry/CDN 与 DSH 上游固定源码；**未安装、未构建、未运行目标或 DSH**。`[DOC]` 是目标发布文档所述；`[SRC-TARGET]` 只用于可与 npm 版本对齐的目标 commit；`[SRC-DSH]` 是固定 DSH 上游；`[TEST]` / `[CI]` 是测试定义/远端 CI 记录，不等于本轮通过；`[RUN]` 本轮无。npm `0.2.0` 的 `gitHead` 与其 GitHub commit 上的 manifest 版本不符，故本 memo 不把该 checkout 的实现、tests 或 CI 冒充 `0.2.0`。

## 坐标与版本 pin

- **[DOC]** 样本目标是 `sidleo/dsh-plugins-plus`、npm `@sidleo3/dsh-plugins-plus@0.2.0`。npm 精确版本 metadata：[registry 0.2.0 metadata](https://registry.npmjs.org/@sidleo3%2fdsh-plugins-plus/0.2.0)。不可变 tarball：[dsh-plugins-plus-0.2.0.tgz](https://registry.npmjs.org/@sidleo3/dsh-plugins-plus/-/dsh-plugins-plus-0.2.0.tgz)，SHA-512 integrity `sha512-j0l9dHZfQ7wT4rtCijiZiTWsCVqyxFPsM5nWP2Qxc7nLlXXvvhC7RwNETmsnYRgT998XSgpcEtb32Rcv3iT5MQ==`，shasum `f6eeeb72d02605af173309f036642cda72dcaf83`。metadata 给出 `gitHead=b0f23374c733866e521e0008412c760f5ae7c8df`。
- **源码 pin 不一致，停止 SRC-TARGET 推论。** 第一方 [GitHub commit b0f2337](https://github.com/sidleo/dsh-plugins-plus/commit/b0f23374c733866e521e0008412c760f5ae7c8df) 的 commit message 是 0.1.8 修复；提交内 [package.json](https://github.com/sidleo/dsh-plugins-plus/blob/b0f23374c733866e521e0008412c760f5ae7c8df/package.json#L1-L5) 明确版本 `0.1.8`。GitHub [tags API](https://api.github.com/repos/sidleo/dsh-plugins-plus/tags) 返回空列表，`v0.2.0` 不存在。不能把 b0f2337 或默认分支代码当作 npm `0.2.0` 的可复核源码；未能逐文件对照 npm tarball。故本 memo **不提供 SRC-TARGET 结论或将该 commit 测试/CI 归于 0.2.0**。
- **[SRC-DSH]** 核对上游固定 DSH tag `dsh-v0.2.1-rc.3`，tag 指向 [`1f81c047fc48fa190a683e469daa699857e9afe8`](https://github.com/deepseek-ai/deepseek-harness/commit/1f81c047fc48fa190a683e469daa699857e9afe8)。仅用来确认 profile patch/config editor/session 所需宿主语义，不推导目标 bundle 实现。

## 能确认的文档主张

- **[DOC]** npm 0.2.0 的版本化 README 可从 [README.md](https://cdn.jsdelivr.net/npm/@sidleo3/dsh-plugins-plus@0.2.0/README.md) 和 [README.zh-CN.md](https://cdn.jsdelivr.net/npm/@sidleo3/dsh-plugins-plus@0.2.0/README.zh-CN.md) 读取。文档描述一个 bundle 有核心 `dsh-plugins-plus` 行和 `agent-instructions-plus`、`skill-filesystem-plus` 两个可独立切换组件；安装后要求重启，两个组件行默认 `disabled: true`。
- **[DOC]** README 称开启组件后，在选择的 agent preset 中禁用 built-in 行并追加替代发现行；关闭后撤销这两项，组合回到 shipped layer 时删除 override。文档不能证明实现是否保留其他插件/用户在相同 preset override 中的字段。
- **[DOC]** 配置写 profile `cordis.patch.yml`，在核心行下经 DSH `ctx.configForms` / config editor 管线；组件选择可继承 global 或自选；“恢复默认”用 `unset` 回 schema default；save 立即生效、核心行不 remount。此描述没有揭示每个字段实际 schema 是否可 unset，也没有实测 config layering。
- **[DOC]** README 明说 session 创建时固定 preset composition，接管变化影响之后创建的 session。另称旧 standalone 配置导入只补 profile 尚未声明字段、adopt 旧 wizard preset selections、重写旧 pipeline rows、记录 `legacyImport` timestamp；旧 JSON 留在共享 DSH home，不删除。没有源码 pin 时，这些只视作作者文档主张。
- **[DOC]** README 称日志由页内浮层展示，并有 `GET /api/dsh-plugins-plus/log`，内容包括 effective config/component state、迁移结果和最近 20 次 pass 的 reason/write/failure/note。未验证 route scope/鉴权、日志字段稳定性、敏感值脱敏与保留行为。

## DSH rc.3 契约（有限交叉核对）

- **[SRC-DSH] Profile patch layering：** rc.3 app-boot 按顺序合成 bundle、profile、home-level、CLI patches；相同 row id 的后层可覆写先前字段。[app-boot merge](https://github.com/deepseek-ai/deepseek-harness/blob/1f81c047fc48fa190a683e469daa699857e9afe8/packages/boot/app-boot/lib/index.js#L61-L109) [profile boot order](https://github.com/deepseek-ai/deepseek-harness/blob/1f81c047fc48fa190a683e469daa699857e9afe8/packages/boot/profile-boot/lib/index.js#L223-L246)。所以“设置落到 profile patch”可与宿主机制相容，但不证明 target takeover engine 的 planner 正确。
- **[SRC-DSH] Config editor：** rc.3 config editor 提供结构化 `edit()` 与 profile patch 的锁定读改写/校验/reconcile能力；当候选 config 与 lower layer 相等时可删除 override。引用 [config-editor README](https://github.com/deepseek-ai/deepseek-harness/blob/1f81c047fc48fa190a683e469daa699857e9afe8/packages/boot/config-editor/README.md)。这个宿主能力不等于插件“精确回滚”已证实。
- **[SRC-DSH] session：** DSH 新会话使用创建时解析的 preset composition；profile 后续改动不会自动重建已存在 session。见 rc.3 [New Session generations guide](https://github.com/deepseek-ai/deepseek-harness/blob/1f81c047fc48fa190a683e469daa699857e9afe8/docs/upgrade-guide/v0.2.1-alpha.1/new-session-generations/guide.md)。因此 README 的“只影响新 session”与上游模型一致；仍未验证目标插件配置变更后实际创建路径以及当前 session UI/上下文是否有额外刷新。

## 高风险主张与未知

- **精确回滚/override 删除：** 目前只能说 `[DOC]`。核心风险是关闭组件时，preset override 可能还包含用户或其他插件的改动；只有整个 composition 恢复到 lower/shipped layer 才适合删除 override。是否按 row ownership 只还原 built-in `disabled`、只删除本插件 pipeline rows、保留 foreign edits，以及最终删除是否会丢失同一 override 的其他字段，必须待 0.2.0 源码/隔离运行确认。不可把“删除覆写行”宣传为任何状态下都无损。
- **旧 session 与 HMR：** README 声明旧 session 不追溯；保存立即生效不等于重建当前 session。HMR 对已运行 Cordis app、mounted component 与 preset registry 的具体顺序、是否有短暂双停/双启窗口，目标源码未能 pin，均 `[OPEN]`。
- **启停与内置行接管：** 默认组件 disabled 和按 preset 接管均为 DOC。实际 enable/disable state scope、组件未 mount/broken preset 的处理、内置 row ID 变更时的诊断/失败策略无法源码确认。
- **preset schema/inheritance：** `unset`、global/component precedence 与显式 empty/none 区分均为 DOC；未知 preset、坏值 normalize、schema 默认值及每字段 unsetability未确认。
- **legacy import idempotency/ownership：** timestamp、只补未声明字段、adopt selection、旧文件不删除都是 DOC。是否 marker 与 row rewrite 原子、失败后重复是否安全、多 profile 共用 `~/.dsh` 的字段 owner/并行迁移无源码证据。保守上应视旧 JSON 为共享数据，不自行清理。
- **logs/status：** API 路由、scope/鉴权、20 条数量语义、敏感设置脱敏、状态字段 schema 都是 DOC，未运行核验。

## TEST / CI / RUN

- **[TEST] 未能对 npm `0.2.0` 的源码测试覆盖作断言。** npm metadata 有 `smoke`、`typecheck`、`build` scripts，只证明脚本名存在，不证明 0.2.0 的测试实现或通过结果。`b0f2337` 是 0.1.8 checkout，其 smoke 文本/断言不得移作 0.2.0 证据。
- **[CI] 未确认**与 npm 0.2.0 tarball 可绑定的 commit workflow run 或成功 check。不能将 CI 配置或 README 兼容性说明写成通过。
- **[RUN] None。** 没有安装、构建或执行目标；没有改 profile/旧 JSON、切换插件、比较旧新 session、验证 HMR/API/log，也没有运行测试。测试定义不是测试结果。

## 结论

本轮能够确认目标发布物的 npm 身份、tarball integrity、版本化 README 的产品承诺，以及 DSH rc.3 的通用 patch layering/config editor/session 原理。**未能 pin 与 `@sidleo3/dsh-plugins-plus@0.2.0` 匹配的 GitHub tag/commit**：发布 metadata 的 `gitHead` 指向 0.1.8 manifest。依用户要求，不从当前分支或邻近版本推断接管算法、enable/disable 状态、unset schema、迁移幂等、log/status、tests/CI。因此 profile/15 中这些机制目前仍是 DOC 级；特别是 overwrite rollback 和 old-session/HMR 行为是高风险未验证项。

升级为源码级复核前，需拿到与 tarball 对齐的发布 commit/tag 或发布源码 provenance，并逐项核对：row-level foreign edits 与整份 override 删除；profile/home patch 冲突和并发写；组件开关、broken preset 与 built-in ID 演进；legacy marker + selection adoption 的重试/多 profile ownership；新旧 session 与 HMR；日志 API 鉴权/脱敏/保留；对应测试源码及同 SHA CI 结果。
