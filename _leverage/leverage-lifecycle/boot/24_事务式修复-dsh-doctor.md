---
title: "事务式修复 · dsh-doctor：先备份，再动手，碰不得的转人工"
domain: lifecycle
kind: sample
positioning: "修复类工具的三条纪律：pre-repair 检查点必须是硬前置、验证通过才落 healthy、救生链上的行一律不自动改。"
takeaway: "自动修复的价值不在“能改”，在“改坏了能退”；而救生链上的行，自动工具必须学会说“我不碰”。"
read_when: "要写自愈/修复/一键排障；或排查“修完更糟了”。"
status: observed
updated: 2026-11-01
budget: 140
---
# 事务式修复 · dsh-doctor

> **阶段**：起 · **载体**：own-cli（`bin: dsh-doctor` → `lib/cli.js`） · **兼看**：装
> **影响力**：npm 近 30 天 **3,264**（2026-11-01，42 个过影响力门的 bundle 之一）
> **研究范围**：`dsh-doctor@0.4.3`，gitHead `a13a5ab4…`，tarball sha256 `c8b04c36…`（130,514 B，61 文件）；DSH 对照 `0.2.1-rc.3`
> **证据成熟度**：源码级（检查点、回滚、受保护集合实读；未实机修复）
> **一句话**：它在动手之前先存一份，**并且明确列出"哪些行我绝不自动关"**。
> **借鉴价值**：**① 修复前检查点必须是硬前置（失败就中止）；② 验证通过才落"健康"检查点，且是尽力而为；③ 救生链上的行一律降级为"人工处理"。**

## 它想干什么 · 为什么值得借鉴

**意图。** 给 DSH 一套体检与修复 CLI：诊断、修、必要时回滚 `[SRC-TARGET]`（`lib/cli.js:783` 的 `createCheckpoint`、`:3213` 的 `rollback` 命令）。

**意义。** 生命周期里"起"这一层最危险的动作是**自动修复**——它能一次把"某个插件坏了"变成"整个 Web 起不来"。这个样本把两件事写死在代码里：**修之前必须有检查点**，**救生链上的行不许自动关**。

**用户价值。** 装之前，用户遇到起不来只能重装；装之后，一条 `dsh-doctor` 给出诊断与可回滚的修复动作，`dsh-doctor rollback <id>` 退回去 `[SRC-TARGET]`（`:3213-3214`）。代价是"能自动修的范围"被刻意压小——**很多情况它只会告诉你"这个我建议你手动来"**。

**表达。** 对受保护的目标，它把动作从 `disable-plugin` 改成 `manual`，文案是 *Repair the failed core plugin manually*，理由写进描述：*is part of the Web rescue path and cannot be disabled safely* `[SRC-TARGET]`（`:2193-2198`）。

## 1. 阶段与载体

- **阶段**：起。它修的是"起不来"。
- **载体**：`own-cli`（单 bin），**没有任何 host 侧符号命中**——它是纯独立进程，所以宿主挂了也能跑。
- **兼看**：装。检查点与回滚会动 profile 文件。

## 2. 机制

### 两次检查点，两种严格度

```js
// lib/cli.js:2270 —— 修复前：硬前置（没有 catch，失败即中止）
const checkpoint = await createCheckpoint(stored.dshHome, profile, "pre-repair", false);

// lib/cli.js:2308 —— 验证通过后：尽力而为（有 catch）
if (verification.blocking === 0) await createCheckpoint(stored.dshHome, profile, "healthy", true).catch(() => {});
```

**不对称是刻意的**：修复前的检查点失败 → 不许改；修复后的"健康"检查点失败 → 只记一笔。**前者是安全边界，后者是便利。**

### 受保护集合

```js
// lib/cli.js:2032-2038（节选）
const PROTECTED_IDS = new Set(["modules", "connection", "client-runtime", "ui-layout", "ui-sidebar", "ui-settings", ...]);
```

这些正是 **Web 的救生链**。判定落在动作生成处 `[SRC-TARGET]`（`:2193-2198`）：

| 目标 | 动作 kind | 风险 |
|---|---|---|
| 普通插件 | `disable-plugin` | `confirmation` |
| **受保护行** | `manual`（"Repair the failed core plugin manually"） | `manual` |

### 三条失败态

| 态 | 表现 | 用户看到什么 |
|---|---|---|
| **检查点建不出来** | `pre-repair` 抛错，修复中止 | 什么都没改——这是正确行为 |
| **修完起不来** | 可用 `rollback <checkpoint-id>` 退回 `[SRC-TARGET]`（`:854`、`:3213`） | 一条命令回到修复前 |
| **想自动关救生链** | 动作降级为 `manual`，不会真的写 `disabled: true` | 提示"这个你得自己修" `[SRC-TARGET]`（`:2417`、`:2425` 亦直接抛错拒绝） |

## 3. 设计取舍

| 取舍 | 选择 | 代价 |
|---|---|---|
| 自动化的边界 | 只自动改"非救生链"的行 | 能自动解决的情况变少 |
| 备份粒度 | 每个 profile 一份检查点目录（`checkpointDirectory`，`:761`） | 磁盘占用；需要清理策略 |
| 备份时机 | 修复前强制、修复后尽力 | 两次语义不同，作者必须记住 |
| 回滚入口 | CLI 显式命令，不自动回滚 | 用户要知道有这回事 |

## 4. 与宿主既有行的边界

它**不接管宿主的启动**，只读 profile 与 patch、写 `disabled` 覆盖；**它把自己当成"宿主之外的最后一道"**——这也是它敢自动改的前提：宿主真起不来时，它仍然能跑 `[OPEN]`（未实测）。

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 自动修复会不会把事情搞得更糟 | 修复前检查点是**硬前置**（失败即中止），修复后的健康检查点可以尽力而为 | `[SRC-TARGET]` `lib/cli.js:2270`（无 catch）vs `:2308`（`.catch(() => {})`） | 安全边界与便利分开；代价是两套语义 | 明确"哪些备份是前置、哪些是记录" | 只对"改动可枚举、可回放"的修复成立 | 不分严格度 → 备份失败也照改，等于裸奔 |
| 有些行改了就是灾难 | 维护一份**受保护集合**，命中时把动作从"自动"降级为"人工" | `[SRC-TARGET]` `:2032-2038`（集合）、`:2193-2198`（降级） | 保住救生链；代价是自动修复覆盖率下降 | 列出你的"救生链"并写进动作生成 | 只对"有核心行概念"的宿主成立 | 一把梭 → 关掉 `ui-layout` 之类，Web 直接白屏且无 GUI 可救 |
| 修完怎么退 | 检查点带 id，回滚做成显式 CLI 命令 | `[SRC-TARGET]` `:761`（目录）、`:854`（回滚）、`:3213`（命令） | 用户可自助；代价是 id 要能被找到 | 规定检查点命名、保留数与查找方式 | 只对"有稳定文件布局"的宿主成立 | 只备份不暴露 → 用户不知道该退到哪 |
| 动作要不要分风险 | 每个动作带 `kind` 与 `risk`（`confirmation` / `manual`） | `[SRC-TARGET]` `:2193-2198` | 高风险动作要求人工确认；代价是 UI/CLI 要实现两档 | 给动作定义风险等级与确认路径 | 只对"批量动作"的产品成立 | 全部同级 → 用户点一次全改完 |

## 6. 失效与开放问题

- `[OPEN]` 检查点的保留与清理策略（未读）。
- `[OPEN]` 宿主完全起不来时 doctor 仍能跑的前提（它读 profile/patch，不连宿主——未实测）。
- `[OPEN]` `verification.blocking` 的判定项（未逐条读）。
- `[OPEN]` 与 `dsh-doctor` 的"安全模式"配合（本卡未涉及）。
- `[OPEN]` 未实机修复。

## 7. 兼看

- 起：与 [`boot/22`](./22_重启取证-dsh-update-checker.md) 同为"外部观测"路线——**22 观测更新，24 观测并修复**。
- 装：回滚会改 profile 文件，边界见 [`install/README.md`](../install/README.md) §2 的三态。
