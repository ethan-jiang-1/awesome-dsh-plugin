---
title: "冲突裁决：谁真的能拦住写"
domain: agent-coordination
kind: card
positioning: "横向比较写冲突的拦截点：提示词、建议性写范围、任务板、pre-execute deny、worktree；只有能在写路径说“不”的才算裁决。"
takeaway: "能声明写范围不等于能阻止；真裁决必须落在执行路径上，且要说明覆盖哪些工具、失败是否 fail-open。"
read_when: "要设计多 agent 写冲突方案，或评估“文件锁/写范围”宣传时。"
status: observed
updated: 2026-11-01
---
# 04 · 冲突裁决

> 协作里最常见的过度承诺：“我们有 writeScopes”。官方 Team 自己写的是 “never block anything”——声明不是裁决。

## 1. 拦截点阶梯

| 层 | 能拦住吗 | 样本/宿主 |
|---|---|---|
| 提示词约定 | 否 | 多数团队的“写范围”说明 |
| 任务板字段 | 否（只记录） | `agent-team` 的 `fileScopes` 只是文案 |
| 任务归属锁 | 只防任务重复，不防文件 | `agent-team` 的 revision CAS/`MEMBER_BUSY` |
| `tools/pre-execute` deny | **是**（覆盖范围内） | `file-claim`：只 write/edit/bash/pwsh |
| worktree 隔离 | 物理隔离，合并时冲突 | `taskswarm`：每 lane 一个 worktree |

## 2. 真裁决的代价

`file-claim` 是本册唯一在写路径返回 deny 的样本，但它：

- 只覆盖四个工具；`&&`/`||`、换行、紧贴重定向、`mv` 源、`str_replace_editor` 都有漏法；
- 守卫是无锁 TOCTOU 预检；相对路径基准与宿主写工具可能错位；
- pid 是宿主进程粒度，同宿主多会话崩溃不触发；NFS/多机必误杀；
- 无 epoch/fencing，被接管方静默失锁（后续写会被拒）。

## 3. 借用与判定

1. 拦截发生在哪条路径？提示词/任务板/工具前/文件系统/worktree？
2. 覆盖哪些工具与写形态？解析失败是 fail-open 还是 fail-closed？
3. 租约有没有 fencing/epoch？失锁方怎么知道？
4. 冲突后是阻塞、合并、还是保留现场人工处理？

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 07 用 pre-execute deny，只覆盖四工具 | `[SRC-TARGET]` | [`07 memo`](./_证据/07-file-claim-源码复核.md)（0.2.0/42f07e2） | shell 漏法更宽；无 fs 钩子 |
| 07 无 epoch、pid 进程粒度、NFS 误杀 | `[SRC-TARGET]` | 同上 | 后续写会被 deny，不是静默覆盖 |
| 04 的 `fileScopes` 只是文案、`leases` 空壳 | `[SRC-TARGET]` | [`04 memo`](../teams/_证据/04-agent-team-源码复核.md) | revision CAS 是单进程窄控制 |
| 11 用 worktree 物理隔离、合并串行 | `[SRC-TARGET]` | [`11 memo`](../pipelines/_证据/11-taskswarm-源码复核.md) | 共享 .git/任务目录；跨进程无锁 |
| “声明≠裁决” | `[OBS]` | 本章归纳 + 官方 writeScopes 自述 | 经验判断 |

**未验证**：真实并发写下的漏拦率、TOCTOU 触发条件、worktree 合并冲突处理，均 `[OPEN]`。
