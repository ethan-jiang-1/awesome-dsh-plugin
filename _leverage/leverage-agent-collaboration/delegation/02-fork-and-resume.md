---
title: "fork 与冷恢复：共享前缀、一次性与可续"
domain: agent-delegation
kind: card
positioning: "三种创建语义的差别：spawn（新会话）、fork（共享父前缀）、外部执行（一次性）；以及冷恢复能还原什么、不能还原什么。"
takeaway: "fork 省上下文但共享前缀；外部执行不能续；冷恢复只还原持久化 descriptor 能表达的东西。"
read_when: "要在委派时复用父上下文，或判断一个 child 重启后还能不能继续时。"
status: observed
updated: 2026-11-01
---
# 02 · fork 与冷恢复

## 1. 三种创建语义

| 语义 | 上下文 | 可续 | 备注 |
|---|---|---|---|
| spawn（本地） | 新 child 会话，继承父的 origin/lineage/depth | 是（本地 child 接受后续消息、可冷恢复） | `startActivation` + 本地 provider |
| fork | 共享父前缀（同前缀） | 是 | `agentPreset` 对 fork 被拒；换模型会丢 KV cache |
| 外部执行（ACP/SDK/Codex/CC） | 独立运行时 | **否**：只暴露一次执行 | 只能拿一次 `result`，不能追问 |

来源：`dsh-subagent/README.md:59-65`；三者在 `startActivation` 的 `provider`/`request` 上分叉。

## 2. 冷恢复还原什么

- 本地 child 的 descriptor 是 log-only 事件（不进模型历史、跨压缩保留）；记录 provider/model/reasoningEffort 与 persona/toolFilter（README:65,137）。
- 冷恢复依赖持久化会话与 descriptor；**外部执行没有可恢复的本地 AgentHandle**。
- `maxDepth`/容量在冷恢复时同样走“先预留再物化”；根父不占槽。

## 3. 常见误判

- “成员可续”不是容器属性，而是 **provider 能力**：只有本地 provider 支持 `prepareContinuable`/continuable child；外部 provider 只给一次性。
- “fork 省 token”只省输入前缀，不保证输出/计量归父；换模型还会丢 KV cache。
- “冷恢复 = 恢复进程内状态”：不，它只恢复持久化描述；内存里的 pause/resume/句柄不在。

## 4. 借用与判定

1. 你要复用父上下文吗？要→fork；不要→spawn。
2. child 需要被追问吗？要→本地 continuable；不要→外部一次性也可。
3. 重启后要继续吗？要→确认 descriptor 持久化 + provider 支持冷恢复。
4. 换模型/换 preset 会影响什么？fork 的 KV cache、外部执行的不可续。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 本地 child 可续、外部执行一次性 | `[DOC]`/`[SRC-DSH]` | `dsh-subagent/README.md:59-65` | 外部 provider 具体行为随实现 |
| fork 拒绝 `agentPreset`，共享父前缀 | `[DOC]` | README:65 | 未在真实 fork 上验证 KV 影响 |
| 冷恢复依赖 descriptor，还原 persona/toolFilter | `[DOC]` | README:65,137 | descriptor 是 log-only，不保证模型可见 |
| 容量/深度在冷恢复同样预留 | `[SRC-DSH]` | `dsh-subagent/lib/index.js:2979-2980`；README:53 | 只证明默认值与语义 |

**未验证**：真实 fork 的 KV cache 代价、冷恢复后 persona 的实际注入、外部 provider 的重连语义，均 `[OPEN]`。
