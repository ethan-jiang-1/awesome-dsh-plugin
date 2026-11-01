---
title: "Asher-2000/dsh-expert-mode"
domain: agent-teams
kind: sample
positioning: "`Asher-2000/dsh-expert-mode`：不用写插件也能写协作——团队落在静态 composition 的 17 条工具行里。"
takeaway: "不用插件写协作（preset 路线）；证明 persona 配置键已被宿主移除。"
read_when: "想用 preset/配置而不是运行时插件做多 agent。"
status: observed
also_in: "delegation"
updated: 2026-11-01
tier: 典型
life: blocked
evidence: L1
answers: Q3
---
# 10 · `Asher-2000/dsh-expert-mode`

> **一句话**:**不用写插件也能写协作**——团队结构全部落在静态 composition 的 17 条 `dsh-tool-subagent` 工具行里。
> **边界**:1 同进程父子(成员=配置出来的可续子代理) · **定位**:**反证型**旁支:路线成立,但在当前宿主上装不起来 · **证据级别**:`observed`(源码逐文件读过)
> **影响力**(2026-10-31 实时采样):**13★** / npm **374 次/月**;catalog 2026-08-19 快照 5★ → ×2.6
> **什么时候找它**:想用 preset/配置而不是运行时插件来做多 agent;或者想搞清楚 `persona` 为什么在这里会挂

> 导航:[样本索引](../../encyclopedia.md) · [域章程](../../00-map.md) · [三笔税机制谱](../../coordination/02-mechanisms.md) · [四道边界](../../coordination/01-taxonomy.md)
> **证据链**：三棵树的坐标（npm 0.9.2=`d61da21` 空壳 / tag `v0.9.2` 自述 0.9.1 / HEAD `ed9a19d` 含 lib+router）见[`10 源码复核`](../_证据/10-expert-mode-源码复核.md)。

## 设计思路

**它是本域唯一一条「不用插件写协作」的路线**——而它在当前宿主上装不起来；且**仓库内 17 行，提示词/注释多写 16**（行数按 17 计）。

它的形态**部分成立**：`preset.yml` 只有元数据，团队结构写在 `agent.cordis.yml` 的静态 composition 里——17 条 `@deepseek-ai/dsh-tool-subagent` 工具行，每条带自己的 `toolName` 与 `persona` 段，`provider: spawn`。但**“17 行 = 17 成员”不成立**：`agentPreset` 出现 0 次，rc.3 下孩子默认继承父代理当前 preset，`persona` 又被宿主禁用，所以它们只是**17 个委派工具别名 + 调用时 spawn**，不是 17 个可配置个体；协调官 prompt 还让模型调不存在的 `expert_delegate`。

**但它在本机 DSH `0.2.1-rc.3` 上有五处硬伤**（按“能不能装上→能不能跑”重排）：

1. **首先不是 persona，而是没有 preset 声明 + 死目录**。`cordis.patch.yml` 只 insert 一个 no-op 插件行，没有 `@deepseek-ai/dsh-agent-preset`；`apply()` 把树拷到 `~/.dsh/.agent-presets/expert-mode/`，而 rc.3 已无人读该目录（本机不存在）。结果是**静默不挂载**，还没轮到 persona 抛错。
2. **若手工迁移成 preset，还有三处更早的硬失败**：17 行 `config.persona` 在 rc.3 被拒（`dsh-tool-subagent/lib/index.js:355`）；`persona.text` 字段名也过时（rc.3 的 `dsh-persona` 要 `prefix`）；`@deepseek-ai/dsh-workflow-worker-thread` 不在 rc.3 安装树（standard preset 已换 `workflow-ptc`）。
3. **任务板不是原子的**。`taskboard.py` 的 `claim` 实序是「读文件 → 校验 → 整体覆写」，全仓无 `flock`/`fcntl`/`O_EXCL`/`os.replace`；两个专家同时 claim 同一任务，双方都会通过迁移校验，后写覆盖先写；`_next_id` 也并发撞号。stale 回滚直接赋值 `ready` 绕过迁移表，活专家随后的 `done` 会因非法迁移失败，任务可被再次 claim 重复执行。**「原子认领」是文档承诺，不是实现。**
4. **文件总线是黑板，不是 P2P**。总线只有「写文件/读文件」，没有任何投递或唤醒机制；`_next_seq` 也非原子。子代理一个回合一把唤醒，不会被文件事件叫醒。所以 B 的邮箱里躺一百条消息,B 也不会有反应——**得由协调官再调一次 `expert_*` 把它唤起,它才会去 `read`**。`PROTOCOL.md` 自己承认这一点。而且第七项验收「端到端:真实双专家走总线接力」**至今未勾**。
5. **「省 28% token」无来源**。全仓 grep `28%` 只命中两行 README;唯一的度量文档测的是**数字符**(3230 字 → 930 字),且由协调官自评,结论写的是 71%。

**它对本域的真正价值是反证**:它把「成员=配置 + 可续子代理 + 文件黑板」这条路走到了能想到的最远处,然后撞在宿主的三个硬约束上——`persona` 已不可配、preset 目录已失效、子代理只能被父唤醒。**这三条正好解释了为什么生态最终都去写运行时插件。**

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`Asher-2000/dsh-expert-mode`](https://github.com/Asher-2000/dsh-expert-mode) |
| **npm 包名** | `dsh-expert-mode` |
| **版本(本次读)** | **HEAD `ed9a19d`**（清单仍 0.9.2；npm 0.9.2=`d61da21` 是空 `apply()`、无 `lib/`；tag `v0.9.2` 树内自述 0.9.1） |
| **License** | MIT |
| **npm 近 30 天** | **374 次**(2026-09-30 ~ 10-29) |
| **安装** | rc.3 上 `dsh plugin add dsh-expert-mode` 缺 `--profile` 会被 CLI 拒绝；补上也只是 pnpm，不会写 `dsh.profile.bundles`。npm 0.9.2 是空壳，17 行 composition 只在未发布 HEAD |
| **接线方式** | HEAD：`main: lib/index.js` + `dsh.plugin.json` + `dsh.bundle.patch`（纯宿主侧）；npm 0.9.2：`main: index.js`，无 `lib/` |
| **复现要点** | **必须 pin commit**：npm 0.9.2 的 `apply()` 是空实现且无 `lib/`，不拷贝任何文件；HEAD `ed9a19d` 才把 preset 拷到 `~/.dsh/.agent-presets/expert-mode/`（该目录官方已不读）。验证要看的仍是 preset 是否被宿主加载 |

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | `~/.dsh/.agent-presets/expert-mode/` 下的文件总线 + taskboard JSON | 部署目录在当前宿主已失效;taskboard 非原子 |
| 冲突裁决 | 无。taskboard `claim` 是「读 → 校验 → 整份覆写」 | 两专家同时 claim 都会通过,后写覆盖先写 |
| 失败收敛 | 手动 `recover` + `stale > 300s` 直接回 `ready` | **无存活探测**,跑得久的专家会被当崩溃回滚 |

## 借用指南

### 可借鉴(直接抄)

1. **把「成员」写成配置行而不是运行时数据** —— 不需要 roster 状态机、不需要 spawn/remove 工具,也就没有官方 Team「Flat immutable roster」那条限制,因为它根本没有 roster。**如果你的团队是固定的,这是最省事的一条路。**
2. **每个成员一条独立的 `dsh-tool-subagent` 工具行** —— 17 个 `expert_*` 工具各自有 `toolName`、`persona`、`provider: spawn`、`backgroundMode: continuable`。**成员边界就是工具边界**,模型看得见、叫得出。
3. **`PROTOCOL.md` 这种「先写协议再写实现」的工艺** —— 它自己列了七项验收,并且**如实留着没勾完的那一项**。这种「把没做完的公开标出来」的习惯本身值得抄,比功能更值钱。

### 别照抄

- **别用 config 里的 `persona`** —— `dsh-tool-subagent/lib/index.js:355` 加载即抛错。合法的路径是把它作为 `startContinuable` 的**请求参数**传(见 [12 dsh-eteams](12-2507483326-dsh-eteams.md))。
- 别把「文件总线」当消息队列 —— 它没有任何唤醒机制,B 的邮箱里躺一百条消息也不会有反应。
- 别信没有测量口径的百分比 —— 「省 28% token」在全仓只出现在两行 README 里。
