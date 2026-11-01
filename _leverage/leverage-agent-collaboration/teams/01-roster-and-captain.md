---
title: "编队与队长：roster 存在哪，谁有权改"
domain: agent-teams
kind: card
positioning: "团队的第一笔账：成员名单存在哪、谁是队长、roster 变更由谁执行；对照 01/04/05/10/12 五种做法。"
takeaway: "roster 的权威位置决定并发与恢复；成员是子代理还是根 Agent 决定上下文与权限边界。"
read_when: "要设计团队成员模型，或判断一个团队插件能不能撑住重启/并发时。"
status: observed
updated: 2026-11-01
---
# 01 · 编队与队长：roster 存在哪

> 团队不是“多开几个 agent”，而是**一份可写的成员名单 + 一个有权改它的角色**。名单的权威位置（会话内存 / 磁盘 / storageDomain / 配置行）决定了重启后剩什么、并发时谁覆盖谁。

## 1. 五种 roster 形态

| 样本 | roster 权威 | 成员是什么 | 队长/创建权 | 证据 |
|---|---|---|---|---|
| `NanmiCoder/dsh-agent-teams` | 磁盘 `<workspace>/.agent-teams/team.json` | 可续子代理 | captain 会话；成员由工具/审批后创建 | [`01 memo`](./_证据/01-agent-teams-源码复核.md) |
| `limuyang2/agent-team` | 宿主 `storageDomain` 5 表（`agent_team` v1） | **独立根 Agent**（`agents.create/resume`，无 `parentAgent`） | Leader 只分配任务；roster 变更在 Web transport，不在模型工具 | [`04 memo`](./_证据/04-agent-team-源码复核.md) |
| `Mlte0907/dsh-teams-x` | 磁盘 `.teams-x/<teamId>/` + 跨进程文件锁 | 持久子代理 | 队长搁浅回池 + 成员孤儿回池 | [`05 memo`](./_证据/05-teams-x-源码复核.md) |
| `Asher-2000/dsh-expert-mode` | 静态 `agent.cordis.yml` 的 17 条工具行 | **不是成员**：17 个委派工具别名 | 无 roster/无队长；prompt 约定 | [`10 memo`](./_证据/10-expert-mode-源码复核.md) |
| `2507483326/dsh-eteams` | SQLite + 进程内锁 | continuable 子代理 | 领队拆任务；成员由领队派发 | [`12 memo`](./_证据/12-eteams-源码复核.md) |

**读法**：先问“名单谁写”，再问“成员是谁”。同一份名单，成员从子代理换成根 Agent，权限、上下文、结果回传都会变。

## 2. 队长不是选举出来的

- `agent-teams`：调度每一步先解析活 captain；取不到就停派发，没有选举/接管协议。
- `agent-team`：Leader 是普通会话，roster 变更由面板/用户触发，leader 只分配任务。
- `teams-x`：队长失联后任务回池，但没有“新队长”角色。
- `expert-mode`：没有队长实体，协调官靠 prompt 让模型自己调 `expert_*`。

**共同点**：队长是“当前活着的那个会话”，不是可选举的席位；失败收敛靠任务回池/人工，不靠 leader election。

## 3. 成员模型的选择

| 选择 | 得到 | 付出 |
|---|---|---|
| 可续子代理（01/05/12） | 上下文连续、可追问 | 受宿主深度/容量/权限固定约束；结果常靠邮箱/通知回传 |
| 独立根 Agent（04） | 每成员异构模型/权限/技能 | 没有父子上下文；roster 与任务板要自建 |
| 配置行（10） | 零运行时 roster | 成员不可独立配置；宿主禁 `persona` 后路线失效 |

## 4. 借用与判定

1. 重启后 roster 从哪读？读不到时是空团队、stale 记录，还是自动重建？
2. 两个进程/两个面板同时改 roster，谁赢？有 CAS/锁/租约吗？
3. 成员创建失败/半创建，会不会留下“子会话存在、名单不认”的孤儿？
4. 队长会话死了，成员任务回池还是永久 claimed？

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 01 的 roster 是磁盘 team.json，锁只在进程内 | `[SRC-TARGET]` | `_证据/01-agent-teams-源码复核.md`（0.1.28/3331b90） | 跨进程会覆盖；具名失效为 `[OBS]` 命名 |
| 04 的成员是独立根 Agent，roster 在 storageDomain 5 表 | `[SRC-TARGET]` | `_证据/04-agent-team-源码复核.md`（0.1.4/a7f3046） | `leases` 空壳、`operations` 表未写；peer 范围不含 rc.3 |
| 05 用跨进程文件锁，但只串行写、无归属 | `[SRC-TARGET]` | `_证据/05-teams-x-源码复核.md`（9c56100） | 锁 stale 30s、获取超时 10s |
| 10 的 17 行是工具别名，不是 17 个成员 | `[SRC-TARGET]` | `_证据/10-expert-mode-源码复核.md`（HEAD ed9a19d） | rc.3 无 preset 声明，静默不挂载 |
| 12 的 persona/成员创建在 rc.3 失效 | `[SRC-TARGET]` | `_证据/12-eteams-源码复核.md`（0.2.21/0f8aa30） | 仅创建失效；既有团队唤醒路径仍在 |
| “队长不可选举”是跨样本归纳 | `[OBS]` | 上述 memo 横向对照 | 归纳性判断，不是宿主契约 |

**未验证**：真实重启后的 roster 竞争、成员半创建孤儿、跨进程同时改名单的实际顺序，均 `[OPEN]`。
