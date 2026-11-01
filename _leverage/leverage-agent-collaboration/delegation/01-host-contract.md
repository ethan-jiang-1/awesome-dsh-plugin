---
title: "宿主契约：主-子代理能做什么、不能做什么"
domain: agent-delegation
kind: playbook
positioning: "dsh-subagent 0.2.1-rc.3 的委派契约：spawn/fork/外部执行、深度与容量、权限固定、结果回传与消息权威。"
takeaway: "先分清本地可续子代理与外部一次性执行；深度/容量是宿主池，权限在启动时固定，结果回传有三条不同通道。"
read_when: "要设计主-子委派，或判断一个委派插件到底改的是哪条接缝时。"
status: observed
updated: 2026-11-01
---
# 01 · 宿主契约：主-子代理

> 这一章只写 DSH `0.2.1-rc.3` 安装树里能核到的委派契约。生态样本的做法在 `samples/`；宿主没承诺的行为一律 `[OPEN]`。

## 1. 三种“子代理”

| 形态 | 入口 | 能否继续 | 典型用途 |
|---|---|---|---|
| 本地 spawn | `startActivation({provider, childId, ...})`（in-process provider） | 可续：本地 child 接受后续消息、可冷恢复 | 子任务、可追问成员 |
| 本地 fork | fork 后端 + 预留 `childId` | 可续（继承父会话） | 复制上下文继续 |
| 外部执行 | `startActivation` 的 external provider | **一次性**：只暴露一次执行，拒绝继续 | ACP/SDK/Codex/Claude Code |

`startActivation` 返回 `{childId, messageId?, result, dispose}`；只有本地 child 保证 `messageId`（[`dsh-subagent/README.md:59-61`]，实现 `lib/index.js:3036`）。

## 2. 深度与容量

| 约束 | 默认 | 语义 |
|---|---|---|
| `maxDepth` | **1** | 只允许直接子代理；显式 tool depth 可覆盖；0 关闭委派 |
| `maxActiveSubagents` | **8** | 每棵 activation 树共享池；根父不占槽；创建/冷恢复先预留再物化；耗尽不排队 |

来源：`dsh-subagent/lib/index.js:2979-2980`（zod `.default(1)` / `.default(8)`），README:49/53/55。**容量是宿主池，不是插件的 roster 上限**；两者相同只是默认值，不是同一约束。

## 3. 权限在启动时固定

- 子代理的权限范围在启动时固定，会话内不能扩大；需要审批的操作**自动拒绝**（`dsh-subagent/README.md:181,186`，注入的运行上下文声明）。
- `agentOptions` 可覆盖 provider/model/reasoningEffort/outputTokens，但需要 provider 声明 `capabilities.agentOptions`（`types.d.ts:127-175`）。
- `agentPreset` 可独立于父 composition；省略则加入父当前 preset；fork 与外部后端拒绝该选项（README:65）。

**常见误解**：把 `persona` 当启动参数。rc.3 的 `SubagentStartRequest` 没有 `persona`/`toolFilter` 字段（`types.d.ts:127-175`）；`dsh-tool-subagent` 对 config persona 直接抛错（`lib/index.js:355`）。persona 的合法路径是 agent preset，冷恢复时从 descriptor v3 还原。

## 4. 结果回传的三条通道

1. **`activation.result`**：调用方 await 的最终结果；teardown 失败只影响 `dispose()`，不替换已捕获结果（`types.d.ts:40-51`）。
2. **父通知（settlement notice）**：`delivery:'parent'` 时，模型收到完成通知；通知可能重复，插件常做去重。
3. **持久邮箱/会话事件**：本地 child 有 inbox，消息经 `agent/inbox/spliced` 持久化；但**不是**“结果自动进父邮箱”。

**没有 durable parent mailbox**：child→parent 消息要求 resident continuable child 且 direct parent 活着；父不在时拒绝，不排队（README:207,212）。

## 5. 消息权威

- 发送者身份来自日志里的 `source.senderSessionId` + 相邻性检查，不来自消息文本。
- `sendMessage(sender, targetId, ...)` 只允许 direct parent / direct continuable child；absent child 可冷恢复，running 目标在最近 step 边界接纳。
- 没有“冒充他人发送”的参数面；控制面工具把 `exec.agent` 同时作为 sender 与 authority。

## 6. 借用与判定

1. 你的“子代理”是本地可续还是外部一次性？后者不能追问、不能续聊。
2. 深度/容量是宿主池还是插件自己记账？有没有预留-物化顺序？
3. 权限/模型/preset 在启动时定死还是可中途改？改的代价是什么？
4. 结果走调用帧、父通知还是邮箱？父不在时消息丢还是排队？

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| `maxDepth` 默认 1、`maxActiveSubagents` 默认 8 | `[SRC-DSH]` | `dsh-subagent/lib/index.js:2979-2980` | zod 默认值；用户/配置可覆盖 |
| 本地 child 可续、外部执行一次性 | `[SRC-DSH]`/`[DOC]` | README:59-61；`types.d.ts:25-51` | 外部 provider 的具体行为随实现 |
| 权限启动时固定、需审批操作自动拒绝 | `[DOC]` | README:181,186（注入声明） | 未在真实审批场景实测 |
| `SubagentStartRequest` 无 persona/toolFilter | `[SRC-DSH]` | `types.d.ts:127-175` | 冷恢复 descriptor v3 可还原 persona |
| 无 durable parent mailbox，父不在即拒 | `[SRC-DSH]`/`[DOC]` | README:207,212 | 只覆盖 in-process continuable child |
| `agentPreset` 可独立，fork/外部拒绝 | `[DOC]` | README:65 | 具体 provider 能力需看 capabilities |

**未验证**：外部 provider 的真实中断语义、冷恢复时 persona 的实际注入效果、容量耗尽后的用户可见错误，均 `[OPEN]`。
