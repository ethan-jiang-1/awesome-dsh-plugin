---
title: "流水线：控制流用脚本还是图、重放靠什么、隔离用哪一层"
domain: agent-pipelines
kind: index
positioning: "家族篇：原生 workflow 只有脚本编排、无 DAG/重放，原生 worktree 只做检出隔离；两条样本路线与三条判据。"
read_when: "要搭多 agent 流水线，或判断该用图还是代码、要不要自建重放。"
status: living
updated: 2026-11-01
budget: 125
---
# 流水线：控制流、重放与隔离

> 本家族篇固定四段：**原生怎么做 → 样本怎么偏离 → 三条判据 → 失效与开放问题**。样本细节在卡，证据在 memo。

## 1. 原生怎么做（`@deepseek-ai/dsh@0.2.1-rc.3`）

**原生编排只有一个形态：模型写 JavaScript，脚本里扇出 subagent。** `workflow` 工具执行脚本并返回最终 JSON 值：前台等待全部工作结束，取消或异常完成返回错误，**部分输出绝不会被报告为成功** `[SRC-DSH]` `dsh-tool-workflow/README.md:12,34`；后台模式注册为自有 `ctx.jobs` 任务（`:42`，`lib/index.js:53`）。结果渲染受 `maxResultChars` 限制，默认 `5e4` `[SRC-DSH]` `dsh-tool-workflow/lib/index.js:68`。

**子代理的工作不进父对话**：模型只看到最终结果，中间消息与子代理自身上下文都留在子代理侧 `[SRC-DSH]` `dsh-tool-workflow/README.md:38`。这是原生编排最大的隐式约束——**并行很便宜，但「边跑边看」不免费**。

**原生没有：图、缓存键、暂停/恢复、断点续跑。** 包内检索不到 `resume` / `replay` / `checkpoint` 符号，README 也未承诺 `[OBS]`。要重放只能整脚本重跑。

**原生隔离是 worktree，但不是 lane 管理器**：`ctx.worktrees.create(agent, { name?, from? }, signal?)` 从本地提交建新分支与检出目录，并 `workingDirectory.set` 进入；只复制已提交内容（暂存、未暂存、未跟踪、被忽略都不带）；写入仍受沙箱约束；**离开会保留分支与文件，移除/清理/合并由消费方负责** `[SRC-DSH]` `dsh-experimental-worktree/README.md:30,85`。默认落在 `<checkout root>/.agents/worktrees/<name>`。

## 2. 样本怎么偏离

| 样本 | 分级 | 偏离点 | 代价 |
|---|---|---|---|
| [`18-agent-dag-workflow`](./samples/18-GM-HZ-agent-dag-workflow.md) | **典型** | 声明式模板 + ready 队列；checkpoint/`semanticHash` 管恢复、Artifact 管 recorded 重放；额度取 `min(模板, 宿主)` | 只收窄能力、不做文件互斥；`recorded` 要求源 run 完成且 Artifact 齐全 |
| [`03-dsh_workflow`](./samples/03-omdsh-dev-dsh_workflow.md) | **典型** | 不可变胶囊快照 + 内容键结果缓存；「可恢复」＝整体重跑 + 回放 | 不是断点续跑；多进程共用 runDirectory 无锁；npm 未发布 |
| [`11-taskswarm`](./samples/11-february2015-dsh-taskswarm.md) | **典型** | 每 lane 一个 worktree + 常驻 `_orch` 集成树；合并失败刻意不清理 | `updateLane()` 仍整份读改写（last-write-wins）；npm 已下架 |

**三条路线各补一块原生空白**：03 补「可复现」（内容键 + 回放），11 补「文件隔离 + 集成」（worktree + `_orch`），18 补「断点与重放」（checkpoint + `semanticHash` + 三档 replay）。**「进程重启后从断点继续」第一次有样本做到**——但它靠自建引擎与 SQLite journal，不是宿主白给。

## 3. 三条判据

1. **控制流：脚本换自由度，图换可分析性。** 代码即编排让并行、条件、循环都免费，代价是图不可静态分析、不能只跑一半。**先接受「不能只跑一半」，再选脚本。**
2. **重放：断点、内容键、记录输出是三件事。** 原生没有 checkpoint；03 用内容键换「可复现」，18 用 checkpoint + `semanticHash` 做恢复、用 Artifact 做 `recorded` 重放。**承诺「可复现」前先说是哪一档**，以及 Artifact 存多久。
3. **隔离：用 worktree，不用锁。** 原生 worktree 只隔离已提交文件，共享 `.git` 与未提交状态；文件级互斥仍要另想办法（见 coordination）。

## 4. 失效与开放问题

- **11 的发布物不可得**：npm 全量下架，只能源码装；它的价值是机制与故障档案，不是可安装件。
- **03 未发布到公共 registry**：安装走 GitHub；机制可学，版本门形同注释。
- **原生 worktree 的清理缺口**：检出目录会留下，需要消费方回收。这与 11「合并失败不清理」是同一取向——**保留现场优于自动清理**。
- `[OPEN]` 原生 worktree 与 11 的 `_orch` 合并语义差异、胶囊缓存在多进程下的正确性。**下次核法**：B2 试验台里用两个进程跑同一胶囊，比对缓存命中与副作用。

## 5. 读法

[`01-graph-vs-code`](./01-graph-vs-code.md)（控制流）→ [`02-native-workflow-engine`](./02-native-workflow-engine.md)（原生引擎）→ [`04-worktree-lanes`](./04-worktree-lanes.md)（隔离）→ 样本 18 → 03 → 11。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 原生 workflow 是脚本编排、无部分成功 | `[SRC-DSH]` | `dsh-tool-workflow/README.md:12,34` | 只覆盖该工具的前台/后台两态 |
| 结果渲染受 `maxResultChars`（默认 5e4）限制 | `[SRC-DSH]` | `dsh-tool-workflow/lib/index.js:68` | 只限渲染，不限执行 |
| 原生 worktree 只复制已提交内容、不负责清理 | `[SRC-DSH]` | `dsh-experimental-worktree/README.md:30,85` | 只覆盖该实验包 |
| 原生没有 DAG/重放/断点 | `[OBS]` | 包内符号检索无命中 + README 未承诺 | 未见不等于不存在，随版本复核 |
| 18 的恢复要过 semanticHash 闸 | `[SRC-TARGET]` | `@gm-hz/agent-dag-workflow@1.0.1` `lib/core/engine.js:173-184` | 只覆盖该发布物 |
| 18 的 `recorded` 重放要求源 run 完成且 Artifact 齐全 | `[SRC-TARGET]` | 同上 `lib/runtime/runtime.js:257-266` | 未实跑重放 |
