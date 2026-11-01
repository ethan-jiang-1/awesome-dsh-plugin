---
title: "团队：roster 存在哪、任务板怎么裁、消息怎么投"
domain: agent-teams
kind: index
positioning: "家族篇：原生 Team 的会话日志权威/CAS/writeScopes 真相、六个样本的偏离、三条判据与失效。"
read_when: "要建多 agent 团队，或判断一个团队插件的状态与冲突模型。"
status: living
updated: 2026-11-01
budget: 130
---
# 团队：多成员如何编队、调度、共享任务板

> 本家族篇固定四段：**原生怎么做 → 样本怎么偏离 → 三条判据 → 失效与开放问题**。样本细节在卡，证据在 memo。

## 1. 原生怎么做（`@deepseek-ai/dsh@0.2.1-rc.3`）

**权威状态在 Lead 的会话日志里，不在磁盘文件里。** Team 的 roster 与任务都是 Lead 会话的持久事件：`team/member`、`team/task`，写入走 `appendAndFlush(root, type, data)` → `root.session.append(...)` 后强制 flush `[SRC-DSH]` `dsh-experimental-agent-team/lib/index.js:156-157`；事件判别式见 `:534`，成员与任务的追加见 `:1025`、`:1234`。

**任务板是乐观并发，不是锁**：每次变更带 `expectedRevision`，不匹配直接抛 `TEAM_TASK_STALE_REVISION` `[SRC-DSH]` `dsh-experimental-agent-team/lib/index.js:1278`；revision 必须从 1 开始且连续（`:612-613`）。

**`writeScopes` 只是提示，不拦任何写入**：重叠只在投影里 `warnings.add("write scopes overlap with …")` `[SRC-DSH]` `dsh-experimental-agent-team/lib/index.js:371`。这是全册最容易误读的一条——**它不提供互斥**。

**消息走目标 agent 的 inbox，不额外保证顺序**：`sendMessage()` 校验调用方成员身份并投递（`:1516`），读取侧折叠 `agent/inbox/spliced` 的 `next-turn` / `next-step`（`:772-775`）；Team 不额外保证同目标发送顺序，投递顺序由目标 inbox 管理 `[SRC-DSH]` `dsh-experimental-agent-team/README.md:130`。

**原生自己写死的三条限制**：共享工作区（不支持独立工作目录）、单进程（不支持跨进程协调）、**不自动释放任务 owner** `[SRC-DSH]` `dsh-experimental-agent-team/README.md:32`；另有扁平不可变 roster（只有 Lead 可建直接 teammate、不支持嵌套/改名/复用）与「无发送重试保证」`:205-207`。

## 2. 样本怎么偏离

| 样本 | 分级 | 偏离点 | 代价 |
|---|---|---|---|
| [`01-agent-teams`](./samples/01-NanmiCoder-dsh-agent-teams.md) | **典型** | 把权威搬回磁盘 `<workspace>/.agent-teams/team.json`；idle 边沿调度；ack 在准入时 | 进程内锁，跨进程即覆盖写 |
| [`04-agent-team`](./samples/04-limuyang2-agent-team.md) | **典型** | 成员＝独立根 Agent（禁 `parentSession`），roster 落 `storageDomain` 5 表 | 无父子上下文；peer 不含 rc.3（blocked） |
| [`10-expert-mode`](./samples/10-Asher-2000-dsh-expert-mode.md) | **典型** | 不写插件：团队结构全在静态 composition 的 17 条工具行里 | rc.3 无 preset 声明 → 静默不挂载（blocked） |
| [`02-team-gui`](./samples/02-toolclub-dsh-agent-team-gui.md) | 变体 | 产品化 runtime：pre-step 派工 + Run Center | 无检查点，重启即 interrupted |
| [`05-teams-x`](./samples/05-Mlte0907-dsh-teams-x.md) | 变体 | 质量门自动派生返工；跨进程锁在未发布源码 | 发布物 0.2.0 只有进程内队列（R4b/R5）；0.11.5 从未发布 |
| [`12-eteams`](./samples/12-2507483326-dsh-eteams.md) | 变体 | SQLite + 领队拆任务；persona 走请求参数 | 该参数仅 0.1.x 成立（blocked） |

## 3. 三条判据

1. **权威状态只能有一个。** 放会话日志 → 可重放、可 fork、随会话走；放自有文件 → 可跨进程读，但要自己解决并发与崩溃恢复。**两个都当真源就是覆盖写的来源**（01 的磁盘 + 内存、05 的锁 + 文件）。
2. **`writeScopes` 不是锁，要拦写只有两条路。** 一是 `tools/pre-execute` 返回 deny（见 coordination 家族篇），二是 worktree 物理隔离。指望任务板字段互斥，会在第一次并发写时失效。
3. **owner 必须有人释放。** 原生明说不会自动释放；失败、退出、崩溃后都要插件自己回收，否则任务永久 `in_progress`，只能人工 `--force`。

## 4. 失效与开放问题

- **进程内锁跨进程即失效**：01 的锁只在同一进程；05 的跨进程文件锁只串行写、不解决归属。
- **孤儿与停驻**：成员创建半成功会留下「会话在、名单不认」；owner 不释放会留下永占任务。
- **假恢复**：记录还在不等于控制面还在（[`05-failure-modes`](./05-failure-modes.md)）。
- `[OPEN]` `agent/status` 的精确语义（`idle`/`running` 之外的空闲判定）、跨进程同时改 roster 的实际顺序、真实写入下 `writeScopes` 重叠的漏拦率。**下次核法**：用确定性试验台（B2）两进程同时 CAS 同一 task，记录谁先提交。

## 5. 读法

[`01-roster-and-captain`](./01-roster-and-captain.md) → [`02-scheduling`](./02-scheduling.md) → [`03-mailbox-and-ack`](./03-mailbox-and-ack.md) → [`04-taskboard-and-gates`](./04-taskboard-and-gates.md) → [`05-failure-modes`](./05-failure-modes.md)。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| roster/任务权威是 Lead 会话日志事件 | `[SRC-DSH]` | `dsh-experimental-agent-team/lib/index.js:156-157,534` | 只覆盖该包实现的 Team |
| 任务 CAS 用 `expectedRevision` | `[SRC-DSH]` | `dsh-experimental-agent-team/lib/index.js:1278` | 只保证单进程内 CAS |
| `writeScopes` 只告警不拦写 | `[SRC-DSH]` | `dsh-experimental-agent-team/lib/index.js:371` | 投影告警，不是强制执行 |
| 原生不自动释放 owner、不支持跨进程 | `[SRC-DSH]` | `dsh-experimental-agent-team/README.md:32,205-207` | 包自述限制，随版本可能变 |
