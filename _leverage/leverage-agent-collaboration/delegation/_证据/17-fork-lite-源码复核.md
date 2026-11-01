---
title: "17 · aleskxyz/dsh-subagent-fork-lite 源码复核"
domain: agent-delegation
kind: evidence
positioning: "0.1.1 固定复核：在进程内 fork 一个只带最近 N 个完成 turn 的 child；查 seed 构造与 0.2.x 兼容边界。"
read_when: "要引用“截断 fork/最近 N 轮”的做法，或判断它能否在 0.2.1-rc.3 上安装时。"
status: observed
updated: 2026-11-01
---
# 17 · `dsh-subagent-fork-lite` 源码复核

> 复核对象：[`samples/17-aleskxyz-dsh-subagent-fork-lite.md`](../samples/17-aleskxyz-dsh-subagent-fork-lite.md)。只读 GitHub raw / npm registry；未安装/构建/运行。`[RUN]` 仅 API/registry 读取。

## Provenance

| 项 | 值 | 核对方式 |
|---|---|---|
| 仓库 | `aleskxyz/dsh-subagent-fork-lite`（Apache-2.0，默认 `main`，0★ @2026-11-01） | GitHub REST |
| npm | `dsh-subagent-fork-lite@0.1.1`（latest）；**无 `gitHead`** | registry |
| tag | 附注 tag `v0.1.1`（对象 `8fd2a42`）→ commit `57262a04a61baefd52ba6e51313cc7ab309a53b9`（2026-09-16） | tag API |
| 审计 pin | commit `57262a0`（tag 树；main 当前树未比对） | raw 按 tag |
| 包形态 | `main ./lib/index.js`；`dsh.bundle.patch`；无 client | package.json |
| 依赖 | `dependencies` 含 `tsdown`/`typescript`（构建期也在运行时依赖里）；peer 为 0.1.x 线 | package.json |
| 兼容 | `engines.dsh` **不存在**；peer 全部 `>=0.1.x <0.2.0` | package.json |

**关键坐标结论**：这是**面向 0.1.x** 的 provider；peer 范围不含 `0.2.1-rc.3`，且声明的 `capabilities` 键集与 rc.3 不一致（见下）。能否在基线安装/运行未执行，标 `[OPEN]`，但按 peer 门预期会被拒。

## DOC（README/CHANGELOG 主张）

- 进程内 subagent backend，类似 harness `fork`，但只 seed 最近 N 个**完成的**父 turn（默认 2）。
- 配置 `maxCompletedTurns`：0 = 空 seed（spawn-like）。
- 声称与官方 fork 同 capabilities，只是 seed 截断。

## SRC-TARGET（`57262a0`）

### 1. seed 构造：完成 turn 前缀 → 最近 N 轮 → 重编号

- `completedTurnPrefix`：找最后一个 `turn/end`，取 `[0, lastEnd.seq]`；无完成 turn 返回 `[]`（[`seed.ts:14-22`](https://github.com/aleskxyz/dsh-subagent-fork-lite/blob/57262a04a61baefd52ba6e51313cc7ab309a53b9/src/seed.ts#L14-L22)）。
- `windowLastCompletedTurns`：按 `turn/end` 切，保留最后 N 个完成 turn；参数必须非负安全整数（[:24-55](https://github.com/aleskxyz/dsh-subagent-fork-lite/blob/57262a04a61baefd52ba6e51313cc7ab309a53b9/src/seed.ts#L24-L55)）。
- `renumberSeed`：把窗口的 `seq` 从 0 重排，并按偏移重映射 `sourceEventSeqs`；越界抛错（[:57-90](https://github.com/aleskxyz/dsh-subagent-fork-lite/blob/57262a04a61baefd52ba6e51313cc7ab309a53b9/src/seed.ts#L57-L90)）。
- `buildForkLiteSeed`：`parent.session.snapshotEvents()` → prefix → window → renumber（[:92-105](https://github.com/aleskxyz/dsh-subagent-fork-lite/blob/57262a04a61baefd52ba6e51313cc7ab309a53b9/src/seed.ts#L92-L105)）。

### 2. provider 注册与 capabilities

- `capabilities` 声明 **5 键**：`agentOptions/outputSchema/depthLimit/toolFilter/persona`（[`index.ts:55-64`](https://github.com/aleskxyz/dsh-subagent-fork-lite/blob/57262a04a61baefd52ba6e51313cc7ab309a53b9/src/index.ts#L55-L64)）。
- rc.3 的 `SubagentCapabilities` 只有 **4 键**：`agentOptions/agentPreset/outputSchema/depthLimit`（`dsh-subagent/lib/types/types.d.ts:115-121`）。多出的 `toolFilter/persona` 在 rc.3 不再是 capability 字段；该 provider 的声明与基线类型不匹配。
- `start` 调 `startInProcessRun(request, seed.length ? {seed} : {})`；`prepareContinuable` 返回 seed spec（[:68-78](https://github.com/aleskxyz/dsh-subagent-fork-lite/blob/57262a04a61baefd52ba6e51313cc7ab309a53b9/src/index.ts#L68-L78)）。
- `apply` 只做 `ctx.subagents.registerProvider(new ...)`（[:80-85](https://github.com/aleskxyz/dsh-subagent-fork-lite/blob/57262a04a61baefd52ba6e51313cc7ab309a53b9/src/index.ts#L80-L85)）。

### 3. 与官方 fork 的差别

- 官方 fork 共享父前缀；fork-lite **截断窗口**后重编号。窗口起点不是父 seq 0，因此 child 的 seed 内容与父前缀不同——**不能复用父的 KV cache**（`[OBS]`，基于“同前缀才可复用”的推断；未实测）。
- `inheritsParentContext = true` 只是描述；真正决定上下文的是 seed 内容。

## SRC-DSH（0.2.1-rc.3）

- `SubagentProvider` 的 capabilities 4 键；`startActivation`/`prepareContinuable` 是当前契约。
- `requires persistence`：`prepareContinuable` 生成的 continuable spec 需要持久化会话；fork-lite 的 seed 是否满足 rc.3 的 descriptor/持久化要求未核，`[OPEN]`。
- peer 门：0.1.x 范围在 rc.3 上不满足；即使 `--ignore-scripts` 强行装，`capabilities` 键集与 rc.3 不一致，运行期可能被忽略/拒绝，`[OPEN]`。

## TEST / CI / RUN

- `test/seed.spec.ts` 覆盖 seed 窗口/重编号（存在，未跑）。
- `.github/workflows/` 有 ci/compat/publish 等；同 SHA check-run 未取，`[CI]` 不写“绿”。
- `[RUN] None`：未安装、未构建、未跑测试。

## 与卡片的偏差

（本卡为新建，无旧卡偏差；以下为写作约束）

| 主张 | 实际 | 处置 |
|---|---|---|
| “与官方 fork 同 capabilities” | 键集多了 toolFilter/persona，rc.3 只有 4 键 | 卡片写“面向 0.1.x，rc.3 类型不匹配” |
| “可复用父 KV cache” | 截断+重编号后前缀不同 | 卡片写“不保证复用”，标 `[OBS]` |
| “可直接在 rc.3 装” | peer 不含 0.2.x | 卡片写“预计被 peer 门拒绝，未实测” |

## `[OPEN]`

- rc.3 上真实安装/加载结果（peer 门 + capability 键集）。
- seed 与 child 持久化 descriptor 的兼容性。
- KV cache 是否真的不可复用（需运行时观测）。
- npm tarball 与 tag 树字节一致性（无 gitHead，未比对）。
