---
title: "原生 workflow：脚本编排，不是声明式 DAG"
domain: agent-pipelines
kind: card
positioning: "DSH 0.2.1-rc.3 的 workflow 能力：模型写 JS 脚本 fan-out 子代理，前台/后台运行；没有内建声明式图原语。"
takeaway: "宿主给的是“脚本 + 引擎 + caps”，不是 DAG；要图就得在脚本/生态层自己建，并接受不可静态分析。"
read_when: "要判断该用宿主 workflow 还是自建 DAG/编排层时。"
status: observed
updated: 2026-11-01
---
# 02 · 原生 workflow

> 很多“DAG 引擎”在 DSH 上其实是**脚本编排**：模型写一段 JS，引擎负责解析/执行/限额/取消；控制流由代码表达，不是图。

## 1. 宿主的 workflow 面

- `dsh-tool-workflow` 注册模型工具 `workflow`：运行 JS orchestration script，fan-out 子代理，返回脚本最终值。
- 解析/执行/caps/cancellation 在 `ctx.workflowEngine`（`@deepseek-ai/dsh-workflow`）后面；换硬化引擎不影响模型看到的 schema。
- 前台：await `run.result`，总是 dispose；非 completed 变 tool error。
- 后台：`run_in_background: true` 注册为 `ctx.jobs` job，立即返回 id；输出 ring 流式进度，结果随 job completion notice 到达。
- 结果渲染有 `maxResultChars`（默认 50000），超长截断并提示。

来源：`dsh-tool-workflow/lib/types/index.d.ts:1-40`；`dsh-workflow/lib/types/index.d.ts` 的 engine 契约。

## 2. 这意味着什么

| 你想要的 | 宿主给不给 | 现实 |
|---|---|---|
| 声明式 DAG（节点/边） | **没有内建原语** | 只能用脚本/生态层自建；图不可静态分析 |
| 并行 fan-out | 给（脚本里并发） | 受引擎 caps/子代理容量限制 |
| 后台运行/进度 | 给（jobs + ring） | 需要 `ctx.jobs` 控制器；缺失则调用失败 |
| 暂停/恢复 | 不在工具面 | 引擎/生态各自实现；宿主管道是 dispose 或 job |
| 缓存/重放 | 不在工具面 | `dsh_workflow` 这类样本自己加内容键缓存 |

## 3. 与样本的关系

- `dsh_workflow` 的“代码即编排”与宿主 workflow 同构，但它自己加胶囊快照、缓存、暂停/恢复、治理。
- `taskswarm` 不是 workflow 引擎：它是 lane 调度器 + worktree；控制流是波次计划，不是 DAG。

## 4. 借用与判定

1. 你需要“图”本身（可视化/静态检查/按节点重放）吗？需要→自建，别宣称宿主有 DAG。
2. 你需要后台/进度吗？需要→用 jobs + ring，别自己写轮询。
3. 失败后要断点续跑还是重跑+回放？宿主工具面不提供前者。
4. caps 触发时脚本会 loudly kill，还是要安静截断？读引擎契约。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| `workflow` 工具运行 JS 脚本并 fan-out 子代理 | `[SRC-DSH]` | `dsh-tool-workflow/lib/types/index.d.ts:1-12` | 只证明工具面；脚本语言能力看引擎 |
| 前台 await result 并 dispose；后台注册 jobs | `[SRC-DSH]` | 同文件 `:13-20` | 后台需 jobs 控制器 |
| 解析/执行/caps 在 `ctx.workflowEngine` | `[SRC-DSH]` | 同文件 `:2-6`；`dsh-workflow` types | caps 细节未逐条核 |
| 无内建声明式 DAG 原语 | `[OBS]` | 本机安装树与工具类型 | 否定性判断；生态层可自建 |
| 03/11 都不是声明式 DAG | `[SRC-TARGET]` | 03/11 memo | 样本结论，不外推宿主 |

**未验证**：脚本引擎的 cap 具体阈值、后台 job 的持久化/重启语义、暂停/恢复是否有引擎级支持，均 `[OPEN]`。
