---
title: "横向协调：谁真能拦住写、锁缺什么、崩了谁收"
domain: agent-coordination
kind: index
positioning: "横向篇：原生唯一真拦截点、approval 与 inbox 语义、四个样本的拦截阶梯、三条判据与失效。"
read_when: "要判断一个协作方案的状态归属、写冲突与失败收敛，或评审它的拦截点。"
status: living
updated: 2026-11-01
budget: 130
---
# 横向协调：状态、冲突、失败收敛

> 本家族篇固定四段：**原生怎么做 → 样本怎么偏离 → 三条判据 → 失效与开放问题**。样本细节在卡，证据在 memo。

## 1. 原生怎么做（`@deepseek-ai/dsh@0.2.1-rc.3`）

**唯一能在写路径上「真拦住」的接缝是 `tools/pre-execute`**：它是 waterfall，默认返回 `{ kind: 'allow' }`，插件可返回 deny 或 ask；ask 会转成审批请求，deny 直接阻止分发 `[SRC-DSH]` `dsh-tools/lib/index.js:3321`。其后还有一层 monotonic guard（只收紧、不放宽）`:3008`。

**审批是 fail-closed 的**：服务 key 为 `approval` `[SRC-DSH]` `dsh-user-approval/lib/index.js:76`；`request()` 必须在 open turn 内调用，否则拒绝（`:128-130`）；没有可用 answerer 时**直接拒绝而不是放行**（`:26`）；每次询问落 `approval/asked` 与 `approval/decided` 审计对（`:139`）。

**状态面只有三个原语，没有锁**：

- `agent/status`：`idle` / `running`，由 agent loop 在相位切换时发出 `[SRC-DSH]` `dsh-agent-loop/lib/index.js:791,798`；
- inbox：`next-turn` / `next-step` 两个目标，读取侧折叠 `agent/inbox/spliced` `[SRC-DSH]` `dsh-experimental-agent-team/lib/index.js:772-775`；
- 会话日志：已知事件表之外的记录必须带 `ignorable` 与 `plugin:` 前缀 `[SRC-DSH]` `dsh-session/lib/index.js:1250-1268`、`:1517-1538`。

**原生没有：跨进程锁、租约/fencing、多文件事务、写冲突裁决。** 团队包只做 CAS（`expectedRevision`）与告警（`writeScopes`），不做互斥——见 [teams 家族篇](../teams/README.md)。

## 2. 样本怎么偏离

| 样本 | 分级 | 拦截点 | 缺口 |
|---|---|---|---|
| [`07-file-claim`](./samples/07-Nwflower-dsh-file-claim.md) | **典型** | 边车认领 + `pre-execute` 返回 deny——**本册唯一真拦写的样本** | 无 epoch；只覆盖内置写工具，`str_replace_editor` 启用即绕过 |
| [`01-agent-teams`](../teams/samples/01-NanmiCoder-dsh-agent-teams.md) | **典型** | 进程内锁 + 磁盘 `team.json` | 跨进程即覆盖写 |
| [`05-teams-x`](../teams/samples/05-Mlte0907-dsh-teams-x.md) | 变体 | 跨进程文件锁 | 只串行写、无归属；stale 30s |
| [`11-taskswarm`](../pipelines/samples/11-february2015-dsh-taskswarm.md) | **典型** | worktree 物理隔离，不做裁决 | 合并冲突推给 git；共享 `.git` |
| [`14-team-rooms`](../crossing/samples/14-PerryLink-dsh-team-rooms.md) | **典型** | 单写链排序 | 单进程内成立；投影在新宿主退化 |

**拦截阶梯（从弱到强）**：提示词约定 → 工具内检查 → 任务板 CAS/`writeScopes` → 文件锁 → **`pre-execute` deny** → worktree 物理隔离。前四层都只能减少概率，**只有后两层能改变结果**；而 worktree 改的是「写在哪」，不是「谁不许写」。

## 3. 三条判据

1. **拦截点必须写在写路径上。** 工具内检查与事后校验都不是拦截；`pre-execute` deny 才是。评审时只问一句：「拒绝发生在哪一行？拒绝之后有没有部分写入？」
2. **锁不够，要有归属与 fencing。** 锁 + 无 epoch ＝ 过期持有者仍能写；至少要有单调序号或租约 epoch，且被拒方要能读到「你为什么被拒」。
3. **收敛要有人负责。** 原生不释放 owner、不清 stale 记录；失败后是恢复、重跑还是留记录，必须显式设计。**能被查询的失败，才不会被误读成成功。**

## 4. 失效与开放问题

- **07 的覆盖缺口**：`WRITE_TOOLS` 之外的写工具（如 `str_replace_editor`）不在拦截集内；启用即绕过。
- **05 的锁无归属**：只串行写，不解决「谁持有、何时过期」。
- **14 的单写链只在单进程内成立**，且多表写入不是事务（目标仓自述）。
- `[OPEN]` 真实并发下的漏拦率、TOCTOU 触发条件、`pre-execute` 与 approval 叠加时的顺序。**下次核法**：B2 试验台并发两进程写同一文件，记录 deny 命中与部分写入。

## 5. 读法

[`06-when-not-multi-agent`](./06-when-not-multi-agent.md)（先决定要不要做）→ [`01-taxonomy`](./01-taxonomy.md)（边界与三笔税）→ [`02-mechanisms`](./02-mechanisms.md)（机制谱）→ [`03-state-ownership`](./03-state-ownership.md) → [`04-conflict-adjudication`](./04-conflict-adjudication.md) → [`05-failure-and-selection`](./05-failure-and-selection.md) → [`07-cost-and-observability`](./07-cost-and-observability.md)（成本与验收）。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| `pre-execute` 是 waterfall，默认 allow，可 deny/ask | `[SRC-DSH]` | `dsh-tools/lib/index.js:3321` | 只覆盖工具调用路径，shell 内部不经过 |
| 审批无 answerer 时 fail-closed | `[SRC-DSH]` | `dsh-user-approval/lib/index.js:26,128-130` | 只覆盖该服务版本 |
| `agent/status` 只有 idle/running | `[SRC-DSH]` | `dsh-agent-loop/lib/index.js:791,798` | 不表达「空闲多久」等语义 |
| 07 是唯一真拦写的样本 | `[OBS]` | 17 样本横向对照 + 07 memo | 归纳性判断，非穷尽 |
| 锁+无 epoch 会静默失锁 | `[OBS]` | 07 memo 的失效路径 | 待 B2 复现 |
