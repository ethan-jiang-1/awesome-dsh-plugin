---
title: "任务板与质量门：完成是谁说了算"
domain: agent-teams
kind: card
positioning: "团队的第四笔账：任务状态机归谁、完成判据由谁写、质量门在完成前还是完成后跑；对照 01/02/04/05。"
takeaway: "任务板必须是可并发写的权威；质量门是“完成判据”的一部分，放在写入后审计只能返工，不能阻止坏产物。"
read_when: "要设计团队任务板/完成判据，或判断质量门能否真的拦住坏交付时。"
status: observed
updated: 2026-11-01
---
# 04 · 任务板与质量门

> 协作里最容易被写错的一格：任务标成 `completed` 不等于产物合格；而质量门如果只做事后审计，它拦不住已经写坏的文件，只能派生返工。

## 1. 任务板的四种权威

| 样本 | 任务状态存哪 | 并发控制 | 完成判据 |
|---|---|---|---|
| `dsh-agent-teams` | 磁盘 `team.json` 的 tasks | 进程内 promise 链 | 成员 `update_task`；质量门默认关闭，可显式开 |
| `dsh-agent-team-gui` | `storageDomain` 8 表（任务/运行/消息…） | revision CAS + `ownership_conflict`/`MEMBER_BUSY` | run 状态 + 可选质量门；重启 active→interrupted |
| `dsh-agent-team` | `storageDomain` 5 表 | revision CAS；`leases` 空壳 | 成员任务工具 + 角色提示词 |
| `dsh-teams-x` | 磁盘 `.teams-x/` | 跨进程文件锁（只串行写） | 质量门自动派生返工（默认 3 轮），`maxRounds` 不可配 |

## 2. 质量门的位置

- **完成时审计**：`agent-teams` 的质量门在完成阶段检查；失败派生修复任务或标 `completed_unverified`。好处是不打断执行，坏处是副作用已发生。
- **自动返工**：`teams-x` 把审查失败转成新任务；默认 3 轮，同源去重，源完成可级联取消。
- **前置拦截**：真正能在写之前拦住的是 `tools/pre-execute`（见 [coordination/02](../coordination/02-mechanisms.md) 与 07 样本）；任务板本身不是拦截点。

**判定**：问“质量门失败时产物回滚吗？”——不回滚就只是审计，不是门禁。

## 3. 完成判据的三个陷阱

1. **把 `ok = !timedOut && !aborted` 当成功**：DSH `kick()` 吞 turn 内错误，只走 `agent/error`；不监听这个事件就会假成功（`remote-agent` 的真实缺陷）。
2. **只看任务状态、不看产物**：成员标 `completed` 但没写文件/写错文件，任务板无法发现。
3. **质量门不可配**：`teams-x` 的 `maxRounds`/`autoDerive` 在插件 Config 里不可达，README 的“可关”只在测试成立。

## 4. 借用与判定

1. 任务状态机有哪些状态？谁能迁移？非法迁移是抛错还是静默？
2. 完成判据包含产物校验吗？失败会回滚、返工，还是只记录？
3. 质量门默认开还是关？配置真的可达吗？
4. 重启后 active 任务是恢复、标 interrupted，还是留在 running？

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 01 的质量门默认关闭、完成时审计 | `[DOC]`/`[SRC-TARGET]` | [`01 memo`](./_证据/01-agent-teams-源码复核.md) | 具体门数/默认值需按版本重核 |
| 02 的 8 表与 `interrupted` 语义 | `[SRC-TARGET]` | [`02 memo`](./_证据/02-team-gui-源码复核.md)（v1.3.0） | 只 failed/partial 可续 1 次 |
| 04 的 revision CAS 与空壳 `leases` | `[SRC-TARGET]` | [`04 memo`](./_证据/04-agent-team-源码复核.md)（0.1.4） | 单进程窄控制；无跨进程锁 |
| 05 的自动返工默认 3 轮，配置不可达 | `[SRC-TARGET]` | [`05 memo`](./_证据/05-teams-x-源码复核.md)（9c56100） | `maxRounds`/`autoDerive` 不在插件 Config |
| `kick()` 吞错、`agent/error` 是唯一出口 | `[SRC-DSH]` | `dsh-agent-loop/lib/index.js:887-890` | 只证明错误不返回；调用方需自行监听 |

**未验证**：质量门在真实坏产物上的拦截率、返工轮数与成本、`interrupted` 后人工恢复流程，均 `[OPEN]`。
