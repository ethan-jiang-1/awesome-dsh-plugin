---
title: "rig · 确定性试验台（R0–R7 的可复跑源码）"
domain: agent-collab
kind: guide
positioning: "把 R0–R7 变成别人能复跑的脚本：只读发布物 + 临时目录 + git，不起 DSH、不调模型。"
read_when: "要复核本册的 L2 结论，或改一条 R 记录前想先跑一遍基线。"
status: living
updated: 2026-11-01
budget: 70
---
# 确定性试验台

> 这是 [`_证据/00` 实测账本](../../_证据/00_实测环境与账本.md) 里 R0–R7 的源码。**它不启动 DSH、不调模型、不写用户 profile**；只解包发布物、起临时目录、跑 `git`。
> 产物全部落在 `<repo>/.work/collab-rig/`（已 gitignore），仓库里只留脚本。

## 1. 怎么跑

```sh
cd _leverage/leverage-agent-collaboration/research/rig
node setup.mjs     # npm pack 四个固定版本 → 校验 sha256 → 解包到 .work/collab-rig/pkgs
node run-all.mjs   # 跑 R1–R7，写 .work/collab-rig/out/results.json
```

**固定版本**（sha256 全值见账本 §0）：

| 目录 | 包 | 版本 |
|---|---|---|
| `fc` | `dsh-file-claim` | `0.2.0` |
| `tx` | `dsh-teams-x` | `0.2.0` |
| `at` | `@nanmicoder/dsh-agent-teams` | `0.1.28` |
| `ts` | `dsh-taskswarm2` | `0.2.38` |

`setup.mjs` 会拒收 sha256 不匹配的包——发布物被重发或镜像不一致时，它不会悄悄跑出另一组结论。

## 2. 跑出来的东西

| 记录 | 测什么 | 稳定判据 |
|---|---|---|
| R1 | 认领路径作用域（07） | `a.ts` 与 `a.ts.bak` 不重叠；越界归一化为 `null` |
| R2 | stale / 损坏 / 孤儿边车（07） | 只有新鲜边车命中；损坏边车 fail-open；`readClaim` 抛错 |
| R3 | deny 是否接在 `tools/pre-execute`（07） | write/edit/bash 重定向 → `deny`；read → 放行 |
| R4a/R4b | 两进程读改写（01/05） | 最终 `members` 只剩 `beta`，两侧退出码 `0` |
| R5 | 05 发布物有无跨进程锁 | `hasCrossProcessLock: false`；npm 只有 0.1.0/0.2.0 |
| R6 | 分波（11） | 正常依赖三波；环退化成同波；缺失依赖进 `unresolvedDeps` |
| R7 | worktree 隔离范围（11 的机制底座） | 未跟踪/被忽略不在；`.git` 是 `gitdir:` 指针；移除后分支仍在 |

## 3. 它不能证明什么

- 不是端到端：没有 DSH 事件顺序、审批、profile、模型。
- R7 是 `git` 语义，不是 11 的编排语义。
- 结论只对账本 §0 记录的 Node/平台/版本成立；换平台要重跑并在账本里记新一行。

## 4. 改它的时候

- 新增一条 R：在 `run-all.mjs` 里加一段，写进账本，并给出**负向判据**（什么结果算推翻）。
- 改固定版本：先改 `setup.mjs` 的 `sha256`，再跑一遍，最后同步账本与样本卡。
- 不要把它扩成「装 DSH 跑插件」——那是 L3，另开一次授权。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 本目录可复跑 R0–R7 | `[RUN]` | `node setup.mjs && node run-all.mjs` | 需网络取 npm 包 |
| 固定版本经 sha256 校验 | `[RUN]` | `setup.mjs` 的 `ARTIFACTS` | 只覆盖四个包 |
| 不碰用户环境 | `[OBS]` | 全部写 `.work/`；无 DSH 调用 | 依赖 npm 与 tar |
