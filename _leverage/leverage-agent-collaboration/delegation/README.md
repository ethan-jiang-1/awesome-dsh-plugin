---
title: "主-子委派：一条委派怎么发生、能不能续、结果怎么回"
domain: agent-delegation
kind: index
positioning: "家族篇：原生三形态与三条回传通道、三个样本的偏离、三条判据、失效边界。"
read_when: "要设计主-子委派，或判断一个委派插件改的是哪条接缝。"
status: living
updated: 2026-11-01
budget: 125
---
# 主-子委派：一条委派怎么发生

> 本家族篇固定四段：**原生怎么做 → 样本怎么偏离 → 三条判据 → 失效与开放问题**。样本细节在卡，证据在 memo。

## 1. 原生怎么做（`@deepseek-ai/dsh@0.2.1-rc.3`）

**三种「子代理」，由一次 `startActivation` 分流**：

| 形态 | 入口 | 能否继续 | 关键约束 |
|---|---|---|---|
| 本地 spawn | in-process provider | 可续：接受后续消息、可冷恢复 | 预留 `childId` 只对本地有效 |
| 本地 fork | fork 后端 + 预留 `childId` | 可续（继承父上下文） | 与 spawn 同一 dispatch 分支 |
| 外部执行 | external provider（ACP/SDK 等） | **一次性**：只暴露一次执行 | 不返回 `messageId` |

分流点是一行：`provider.prepareContinuable === void 0 ? manager.startExternal(spec) : manager.startLocal(spec)` `[SRC-DSH]` `dsh-subagent/lib/index.js:3047`。**有 `prepareContinuable` 就走本地**——这正是样本 16 在 rc.3 能生效的原因。

**深度与容量是宿主池，不是插件 roster**：

- `maxDepth` 默认 **1**、`maxActiveSubagents` 默认 **8**（zod `.default(1)` / `.default(8)`）`[SRC-DSH]` `dsh-subagent/lib/index.js:2979-2980`；超深抛 `SubagentDepthError`（`:279-282`）。
- 容量按 activation 树共享；耗尽不排队。

**启动请求面比 README 窄**：`SubagentStartRequest` 有 `agentOptions`（且要求 provider 声明 `capabilities.agentOptions`），**没有 `persona` / `toolFilter`** `[SRC-DSH]` `dsh-subagent/lib/types/types.d.ts:127,160`。persona 的合法路径是 agent preset。

**结果回传有三条通道，但不是一条邮箱**：

1. `activation.result`（调用方 await）；
2. `delivery:'parent'` 的完成通知（可能重复，插件常去重）；
3. 目标 agent 的 inbox（`sendMessage` 走相邻性校验）。

**没有持久 parent mailbox**：child→parent 投递要求直接 parent 在线，父不在时**拒绝而不排队** `[SRC-DSH]` `dsh-subagent/README.md:207,212`。

## 2. 样本怎么偏离

| 样本 | 分级 | 偏离点 | 代价 |
|---|---|---|---|
| [`16-route-pin`](./samples/16-tkaiz0406-dsh-subagent-route-pin.md) | **典型** | 包装 provider + 在 `startActivation` 钩子写 `agentOptions`，按 label 开例外 | 钩子是唯一生效点；`teamInjection:false` 会同时关掉单发与团队注入 |
| [`15-subagent-models`](./samples/15-Garybot126-dsh-subagent-models.md) | 变体 | 在 `agent/request` 上覆写 child 的 provider/model/effort | README 声称的 preset 优先级与模型校验在实现里不存在 |
| [`17-fork-lite`](./samples/17-aleskxyz-dsh-subagent-fork-lite.md) | **典型** | 截断 fork：只 seed 最近 N 个完成 turn，再重编号 | 截断后不能复用父 KV cache；peer 与 capabilities 均不含 rc.3（blocked） |

**分水岭**：15 与 16 做的是同一件事（子代理模型路由），但 15 改请求、16 改 dispatch 前的钩子。**rc.3 上真正稳定的是 16 那条**；15 的价值是说明「同一诉求有两个挂载点，选错就静默失效」。

## 3. 三条判据

1. **先判可续性，再选形态。** 要追问、要冷恢复 → 本地；只要一次结果 → 外部。`childId` 预留与 `messageId` 只在本地分支存在。
2. **路由与覆盖钉在 `startActivation`。** 不要假设 `provider.start` 会跑：rc.3 在 `prepareContinuable` 存在时走 `startLocal`（`3047`）。写路由前先回答「我的 provider 声明了哪个方法」。
3. **结果回传选通道，别假设邮箱。** await 拿最终值、`delivery:'parent'` 拿通知、`sendMessage` 拿 inbox——三条通道的可靠性不同；父不在线时第三条会拒绝。

## 4. 失效与开放问题

- **深度默认 1**：想要「子代理再派子代理」必须显式抬 `maxDepth`，抬了就是自己的容量治理责任。
- **权限启动时固定**：会话内不能扩权；需要审批的操作在子代理里自动拒绝（[`01` §3](./01-host-contract.md)）。
- **无 durable parent mailbox**：把「结果自动回到父」当保证会丢消息。
- `[OPEN]` 外部 provider 的真实中断语义、冷恢复时 persona 的实际注入、容量耗尽后的用户可见错误。**下次核法**：用 ACP 外部 provider 跑一次中断，再读 `subagent/catalog` 投影。

## 5. 读法

[`01-host-contract`](./01-host-contract.md)（契约）→ [`02-fork-and-resume`](./02-fork-and-resume.md)（创建语义）→ 样本 16 → 17 → 15（变体）。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| `maxDepth` 默认 1、`maxActiveSubagents` 默认 8 | `[SRC-DSH]` | `dsh-subagent/lib/index.js:2979-2980` | zod 默认值，可被配置覆盖 |
| 本地/外部由 `prepareContinuable` 分流 | `[SRC-DSH]` | `dsh-subagent/lib/index.js:3047` | 只覆盖 in-process provider |
| 启动请求无 persona/toolFilter | `[SRC-DSH]` | `dsh-subagent/lib/types/types.d.ts:127,160` | 冷恢复 descriptor 可还原 persona |
| 无持久 parent mailbox | `[SRC-DSH]` | `dsh-subagent/README.md:207,212` | 只覆盖可续 child 与在线父 |
| 16 生效的是钩子而非 `provider.start` | `[SRC-DSH]` | `3047` + 16 memo | 未实跑，L1 |
