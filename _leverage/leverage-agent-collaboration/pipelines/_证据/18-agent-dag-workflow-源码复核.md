---
title: "18 · `@gm-hz/agent-dag-workflow@1.0.1` 源码复核"
domain: agent-pipelines
kind: evidence
positioning: "18 的固定版本复核：npm/tag/commit/CI 对齐、模板/引擎/重放/限额/适配器的行号证据，与卡片主张的偏差表。"
read_when: "引用 18 的「声明式 DAG / 检查点恢复 / 记录重放 / 限额」结论前。"
status: observed
updated: 2026-11-01
budget: 130
---
# 18 · 源码复核

> 取证时点 2026-11-01（Asia/Shanghai）。标签沿用 [`EVIDENCE.md`](../../EVIDENCE.md)。
> **本轮没做的事**：未安装、未起 DSH、未跑它的测试或 CI、未执行任何 Workflow。**`[RUN]` 只覆盖** `npm pack`、解包、`sha256` 与只读静态阅读。
> 本 memo 的行号指 **npm tarball 内的 `lib/` 与 `spec/`、`README.md`**（1.0.1 发布物）。

## Provenance

| 项 | 值 | 核对方式 |
|---|---|---|
| 仓库 | [`GM-HZ/agent-dag-workflow`](https://github.com/GM-HZ/agent-dag-workflow)（MIT，7★，`pushed_at 2026-10-07`） | `/repos` |
| npm 包 | `@gm-hz/agent-dag-workflow@1.0.1` | registry |
| tag ↔ commit | `v1.0.1` = `9e9d006913e067a8bfcab18a063a8b5acd683518`；main HEAD 同 SHA | `/tags`、`/commits/main` |
| npm ↔ commit | `dist.gitHead` = `9e9d006…` | registry |
| tarball | `1bd5736eb9bb529515d73da9663b0ee022735b0810f52cf5fe178a2bc0740670`，808,178 B，379 文件 | `npm pack` + `shasum` |
| CI（同 SHA） | 4 个 check-run 全 `success`：`check`、`build`、`npm`、`deploy` | `/commits/<sha>/check-runs` |
| 发布物内容 | `lib/`、`docs/`、`spec/`、`examples/`、`skills/`、`cordis.patch.yml`；**不含 `src/` 与 `tests/`** | tarball 清单 |

**结论**：坐标三层对齐（tag = commit = npm gitHead），CI 同 SHA 全绿；源码只能从仓库读，发布物是构建物。

## DOC（作者主张，不证明实现）

- **定位**：轻量、Host-neutral 的 DAG Workflow Runtime；把 Tool/Skill/MCP 组织成可保存、校验、恢复、审计和重放的 `WorkflowTemplate` JSON（`README.md:3`）。
- **权限只收窄**：模板 `requires` ∩ 节点声明 ∩ Authority ∩ Host policy（`README.md:30`）。
- **可复现**：run 固化模板、发布修订、依赖闭包、Engine 版本与 NodeDefinition set hash；Journal 与 Checkpoint 原子提交（`README.md:36`）。
- **重放边界**：Recorded Replay 不声称重放模型隐藏思维链，只用显式输入、公开内容、结构化输出与按 Capture Policy 保存的 Artifact（`README.md:219`）。

## SRC-TARGET（发布物内可核）

| # | 事实 | 证据 |
|---|---|---|
| 1 | **声明式模板 v1**：Envelope / Node / Edge / Outputs / Policies / 发布校验；`requires` 是不可变依赖 allowlist | `spec/workflow-template-v1.md:1-230`（Policies 段 `:192-205`，Requires 段 `:38-57`） |
| 2 | **模板额度不能超过宿主**：模板/默认值与 deployment limits 取 `min`，Catalog 发布与恢复路径各校验一次 | `lib/core/limits.js:47-54`；`spec/workflow-template-v1.md:203` |
| 3 | **默认额度**：部署 `maxConcurrentNodes 16`、`maxNodeRuns 1000`、`maxDurationMs 1h`；模板默认 `4 / 100 / 10min`；并发硬顶 64 | `lib/core/limits.js:4-27`、`:29-31` |
| 4 | **DAG 调度**：start 节点进 ready 队列，`sortReady` 决定顺序；恢复时重建 ready | `lib/core/engine.js:55-56`、`:214` |
| 5 | **恢复要过三道闸**：run 存在、authority 一致、`semanticHash` 与存档一致（否则 `CHECKPOINT_TEMPLATE_MISMATCH`）；同一 `invocationId` 绑定不同输入 → `INVOCATION_CONFLICT` | `lib/core/engine.js:173-184`、`:112-117` |
| 6 | **重放有三种模式**：`inspect`（读历史）、`recorded`（用已提交外部输出重放）、`live`（重新执行）；`recorded` 要求 plan 可重放、源 run 已完成、外部输出齐全，否则报错 | `lib/runtime/runtime.js:250-300`、`:483-495` |
| 7 | **重试按幂等分级**：节点定义声明 `retry: never / safe / idempotent`；编译期若 `maxAttempts > 1` 而定义 `never`，报 `NODE_RETRY_UNSAFE` | `lib/core/types.d.ts:103`；`lib/core/compiler.js:71-74` |
| 8 | **子流程幂等是契约**：`WorkflowSubworkflowGateway.execute` 要求实现方让 `invocationId` 跨进程重启幂等 | `lib/core/types.d.ts:198-200` |
| 9 | **节点种类**：`core.start/end/condition/foreach/script` + `gateway.tool.execute / agent.execute / approval.request / workflow.call` | `lib/core/nodes.js:44`、`:311`、`:364`、`:392` |
| 10 | **DSH 接线**：适配器 `inject = ['tools','subagents','approval','skills']`；patch 只插一行，SQLite 库落在 `dshHomePath('agent-dag-workflow/workflows.db')` | `lib/adapters/dsh/index.js:3-5`；`cordis.patch.yml:1-5` |
| 11 | **外部结果两级校验**：`expects.schema` 编译成校验器；不合法即 `NODE_EXPECTATION_SCHEMA_INVALID` | `lib/core/compiler.js:103-108`、`:223-225` |

## 卡片主张 vs 证据

| 卡片主张 | 证据 | 判定 |
|---|---|---|
| 声明式 DAG（模板 JSON），不是代码即编排 | `spec:1-230`；节点/边/输出在模板里 | 成立 |
| 断点恢复靠 checkpoint + semanticHash，不是「重跑整段代码」 | `engine.js:173-184` | 成立（恢复 ≠ 重放，见下） |
| `recorded` 重放能复现外部调用结果 | `runtime.js:257-266` | 成立，但**要求源 run 已完成且 Artifact 齐全** |
| 额度是「模板 ≤ 宿主」的硬顶 | `limits.js:47-54`、`spec:203` | 成立 |
| 权限只会收窄 | `README:30`；`spec:52-57` | 成立（DOC + 编译期未声明检查） |
| 适配 DSH 的接缝只有一行 patch | `cordis.patch.yml:1-5` | 成立；但 adapter 需要宿主已装 `workflow*` 服务或自带内存实现 |

## TEST / CI / RUN

- **`[CI]`**：同 SHA 4 个 check-run 全成功；**这只证明该 SHA 上跑过什么，不证明发布物等价**。
- **`[TEST]`**：仓库有 `tests/`（core/dsh/sqlite/verification 等），发布物**不含**；本轮未运行。
- **`[RUN]`**：`npm pack`、解包、`sha256`、只读阅读。**没有启动任何 Workflow**。

## `[OPEN]`

1. **SQLite Journal 在多进程下的并发语义**：文档称原子提交，但未读实现（`lib/journal`）。复核动作：读 `lib/journal/index.js` 的提交路径，并起两个进程写同一库。
2. **`recorded` 重放在 Artifact 被裁剪后的失败面**：代码有 `missing replayable artifact` 错误，但未验证清理策略。
3. **DSH 内恢复**：`WorkflowRecoveryCoordinator` 在宿主重启时怎么扫未完成 run，未实跑。
4. **模板编译器的分支支配检查**：README 声称「某条激活路径必然缺数据」会被拒，未找到对应诊断码，待读 `compiler.js` 全文。
