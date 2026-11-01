---
title: "ACP/外部运行时：一次性执行怎么接"
domain: agent-crossing
kind: card
positioning: "跨运行时的另一条路：ACP/SDK 把外部 agent 当一次性执行接入；能拿到结果，不能追问，也没有父信箱。"
takeaway: "外部执行只承诺一次运行；要跨会话追问就得回到本地 continuable，或者自建 broker/relay。"
read_when: "要接 Codex/Claude Code/ACP 类外部 agent，或判断“跨运行时协作”能到什么程度时。"
status: observed
updated: 2026-11-01
---
# 04 · ACP / 外部运行时

> 08/13 解决“DSH 之间”的消息；ACP/SDK 解决“把非 DSH 的 agent 接进来”。后者的边界更硬：**只承诺一次执行**。

## 1. 一次性意味着什么

- 外部 provider 通过 `startActivation` 暴露一次执行；`result` 只结算一次，**拒绝 continue/follow-up**（`dsh-subagent/README.md:59-61`）。
- 没有本地 AgentHandle / inbox / idle 状态；`SubagentRun` 是外部执行句柄，不是会话。
- 父通知/调用方结果仍可用；但“再问一句”不在契约里。

## 2. 与 broker/relay 的分工

| 需求 | 选什么 |
|---|---|
| 把一次任务交给外部 agent，拿结果 | ACP/SDK 外部 provider |
| 跨 DSH 实例持续投消息 | `interconnect`（直连 WS）或 `relay`（broker + 长轮询） |
| 让外部 agent 像成员一样被反复追问 | 本地 continuable 子代理；外部运行时做不到 |
| 跨会话接管/接力 | `takeover`（会话层）或 `rooms`（共享房间） |

## 3. 接入时要问

1. 外部运行时是否支持中断/取消？取消后进程/容器谁清理？
2. 结果是一次性文本，还是结构化 `outputSchema`？失败怎么表达？
3. 权限/凭据在谁手里？外部运行时能否反过来访问宿主？
4. 断链/超时后是重试、丢弃，还是留孤儿进程？

## 4. 借用与判定

- 想要“跨运行时对等协作”→ 先接受一次性；需要持续对话就自建 broker，并自己解决幂等/离线队列。
- 别把“能调用 Codex/CC”写成“能和 Codex/CC 组队”：成员模型、任务板、追问都不在 ACP 契约里。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 外部执行一次性、拒绝继续 | `[DOC]`/`[SRC-DSH]` | `dsh-subagent/README.md:59-61` | 具体 provider 能力随实现 |
| 外部执行无本地 inbox/idle | `[SRC-DSH]` | `dsh-subagent/README.md:88,119` | 只覆盖 external variant |
| `dsh-acp` 有一次性权限决策/取消语义 | `[SRC-DSH]` | `dsh-acp/lib/types/index.d.ts` 注释 | 未核 ACP 协议细节 |
| ACP 不等于团队协作 | `[OBS]` | 本章归纳 | 经验判断 |

**未验证**：ACP 会话的真实取消/清理、结构化结果的边界、外部进程孤儿处理，均 `[OPEN]`。
