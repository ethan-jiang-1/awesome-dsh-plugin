---
title: "团队失效谱：假成功、覆盖写、孤儿与停驻"
domain: agent-teams
kind: card
positioning: "把团队协作的失败按“谁以为自己成功了”分类：假成功、覆盖写、孤儿成员/任务、停驻与不收敛，并给可命名的失效条件。"
takeaway: "团队失败大多不是崩溃，而是某一层认为自己完成了；先写失败语义，再写恢复。"
read_when: "要设计团队恢复/对账，或评审一个团队插件的失败语义时。"
status: observed
updated: 2026-11-01
---
# 05 · 团队失效谱

> 多成员系统里最贵的 bug 不是“抛错”，而是“某一层认为成功、另一层没有”。下面五类都能在现有样本里找到具名证据。

## 1. 假成功

- **机制**：DSH `kick()` 是 `try { while (await this.turn()) } catch (_error) {}`，turn 内错误只走 `agent/error`；完成判据若只看超时/中断，就会把“报错 + 0 产物”标成完成。
- **样本**：`remote-agent` 的 `agent-false-success.test.js` 记录并修复了这条；`ok` 加上 `hadError` 才正确。
- **对策**：完成判据同时监听 `agent/error`，并要求产物清单非空。

## 2. 覆盖写

- **机制**：磁盘真相源 + 进程内锁；两个 DSH 进程写同一 `.agent-teams/`/`.teams-x/`，后写覆盖先写。
- **样本**：`agent-teams` 明确“不协调并发进程”；`teams-x` 加了跨进程文件锁，但只串行写，不提供归属。
- **对策**：要么单写者代理，要么跨进程锁 + 归属/fencing；只加文件锁不等于安全。

## 3. 孤儿成员 / 孤儿任务

- **机制**：spawn 成功、落盘失败（崩溃窗口）；或成员会话存在但 roster 不认。
- **样本**：`agent-teams` 正常失败有 retired-id + drain 补偿，只剩进程崩溃窗口；`agent-team` 的 `operations` 表从未被写，`leases` 空壳。
- **对策**：创建顺序（先预留 id → 再物化） + 启动对账 + 可枚举的孤儿清单。

## 4. 停驻（parked）不收敛

- **机制**：成员中断后任务仍 `claimed`；有的实现“停驻直到显式消息/转派/冷启动”，不是永久。
- **样本**：`agent-teams` 文档明说 parked until messaged/reassigned；`agent-team` 的 owner 不自动释放，只靠回池与提醒。
- **对策**：给停驻任务 TTL + 可见提醒；不要用“永久”描述实现。

## 5. 重启后的“假恢复”

- **机制**：任务记录还在，但控制面（内存 runs、pause/resume、句柄）已丢；记录变 stale `running`，需人工 `--force`。
- **样本**：`dsh_workflow` 的“可恢复=整体重跑+缓存回放”；`team-gui` 的 active→interrupted 且 interrupted 不可续；`taskswarm` 的批次 JSON 非原子写会让 `resume` 静默失效。
- **对策**：区分“记录存在”“控制面存在”“可继续执行”三件事，并在 UI 标清。

## 6. 借用与判定

1. 完成判据是否包含错误事件与产物校验？
2. 有没有跨进程写？锁保护的是读-改-写还是归属？
3. 创建/删除失败的补偿路径是什么？崩溃窗口留下什么？
4. 重启后哪些状态是“记录”、哪些是“可继续”？

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| `kick()` 吞 turn 内错误，`agent/error` 是暴露口 | `[SRC-DSH]` | `dsh-agent-loop/lib/index.js:887-890` | 只证明错误不返回 |
| 01 的跨进程覆盖写与 parked 语义 | `[SRC-TARGET]` | [`01 memo`](./_证据/01-agent-teams-源码复核.md) | 具名失效名是 `[OBS]` 命名 |
| 02 的重启 active→interrupted、不可续 | `[SRC-TARGET]` | [`02 memo`](./_证据/02-team-gui-源码复核.md) | 只 failed/partial 可续 1 次 |
| 05 的跨进程锁只串行写 | `[SRC-TARGET]` | [`05 memo`](./_证据/05-teams-x-源码复核.md) | 无归属/fencing |
| 11 的批次 JSON 非原子、`resume` 可能静默失败 | `[SRC-TARGET]` | [`11 memo`](../pipelines/_证据/11-taskswarm-源码复核.md) | 未跑真实崩溃恢复 |

**未验证**：五类失效在真实并发/崩溃下的触发率，`recv` 侧重复执行的实际后果，均 `[OPEN]`。
