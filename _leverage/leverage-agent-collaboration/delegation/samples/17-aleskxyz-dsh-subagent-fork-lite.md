---
title: "aleskxyz/dsh-subagent-fork-lite"
domain: agent-delegation
kind: sample
positioning: "`dsh-subagent-fork-lite@0.1.1`：进程内 fork，只 seed 最近 N 个完成 turn；面向 0.1.x，peer 与 capabilities 均不含 rc.3。"
takeaway: "截断 fork 用 seed 窗口换上下文成本；但截断后不能复用父 KV cache，且 0.2.x 上类型/peer 不匹配。"
read_when: "要控制 fork 继承多少上下文，或判断“fork-lite”能否在 0.2.x 使用时。"
status: observed
updated: 2026-11-01
---
# 17 · `aleskxyz/dsh-subagent-fork-lite`

> **一句话**：官方 fork 会带全部父上下文；它只带最近 N 个**完成的** turn，把 seed 窗口截断后重编号，再交给 in-process driver。
> **边界**：0.1.x 线（peer `<0.2.0`）；**0.2.1-rc.3 上类型与 peer 都不匹配** · **证据成熟度**：固定 tag 复核，无运行。

> 导航：[delegation README](../README.md) · [宿主契约](../01-host-contract.md) · [样本百科](../../encyclopedia.md)
> **证据链**：[`17 源码复核`](../_证据/17-fork-lite-源码复核.md)（v0.1.1 / commit `57262a0`）。

## 设计思路

**问题**：官方 fork 继承全部父历史，长会话的孩子一出生就背着巨大前缀；很多委派只需要“最近几轮”的上下文。

**做法**：`completedTurnPrefix` 取最后一个 `turn/end` 之前的完整前缀 → `windowLastCompletedTurns` 保留最后 N 个完成 turn → `renumberSeed` 把 `seq` 从 0 重排、按偏移映射 `sourceEventSeqs` → `startInProcessRun(request, {seed})`。`maxCompletedTurns` 默认 2，0 等于空 seed（spawn-like）。

**它不做的**：不改变父会话、不写父日志；只影响 child 的 seed。

## 机制与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | seed 来自父会话快照；child 自己持久化 | 截断窗口与父前缀不同，**不能复用父 KV cache**（`[OBS]`） |
| 冲突裁决 | 不涉及（只创建 child） | 与官方 fork 的语义差异要写清 |
| 失败收敛 | seed 为空则退回 spawn-like；越界 `sourceEventSeq` 抛错 | 目标宿主 0.2.x 上 provider capability/peer 不匹配 |

**额外边界**：
- `capabilities` 声明 5 键（含 `toolFilter`/`persona`），rc.3 只有 4 键；peer 全为 0.1.x。
- `dependencies` 把 `tsdown`/`typescript` 放进运行时依赖，体积/供应链需注意。
- 无 `gitHead`，只能按 tag/commit 复现。

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`aleskxyz/dsh-subagent-fork-lite`](https://github.com/aleskxyz/dsh-subagent-fork-lite) |
| **npm** | `dsh-subagent-fork-lite@0.1.1` |
| **版本(本次读)** | `0.1.1` @ tag `v0.1.1` → commit `57262a0`（2026-09-16） |
| **License** | Apache-2.0 |
| **安装** | `dsh plugin --profile <profile> add dsh-subagent-fork-lite`（peer 期望 0.1.x） |
| **接线** | `dsh.bundle.patch`；注册 provider `fork-lite` |
| **配置** | `providerName` 默认 `fork-lite`；`maxCompletedTurns` 默认 2，0=空 seed |

## 借用指南

### 可借鉴

1. **按完成 turn 截断，而不是按事件条数**：`turn/end` 是语义边界，截在中间会产生坏 seed。
2. **重编号 + 源 seq 映射**：窗口不从 0 开始时，必须把 `seq` 连续化并重映射 `sourceEventSeqs`，否则 seed 不合法。
3. **0 = spawn-like**：一个参数同时表达“fork 多少轮”和“退化成 spawn”，语义干净。

### 别照抄

- 别承诺“截断 fork 仍复用父 KV cache”：前缀不同，缓存不共享。
- 别在 0.2.x 上直接引用它的 capabilities：rc.3 只认 4 键，peer 也不含 0.2.x。
- 别把它当“官方 fork 的等价替代”：它只覆盖 seed 截断，不覆盖 fork 的其它语义。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| seed = 最后 N 个完成 turn，截断后重编号 | `[SRC-TARGET]` | [`17 memo`](../_证据/17-fork-lite-源码复核.md)（`seed.ts:14-105`） | 重编号细节未跑测试 |
| `maxCompletedTurns` 默认 2，0=空 seed | `[SRC-TARGET]` | 同上（`index.ts:38-52`） | 参数校验为自然数 |
| 面向 0.1.x，rc.3 peer 不满足 | `[SRC-TARGET]`/registry | 同上（package.json peer） | 真实安装未试 |
| capabilities 5 键 vs rc.3 4 键 | `[SRC-DSH]` | `dsh-subagent/lib/types/types.d.ts:115-121` | 运行期是否被忽略未验证 |
| 截断后不能复用父 KV cache | `[OBS]` | 前缀不同 + 推理 | 未实测 |

**未验证**：rc.3 实际加载、seed 与持久化 descriptor 的兼容、KV cache 实测、tarball 一致性，均 `[OPEN]`。
