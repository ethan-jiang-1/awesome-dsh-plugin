# 03 · `omdsh-dev/dsh_workflow`

> **一句话**:把一次性多 Agent 调度升级成可生成、可保存、可治理、可观察、可恢复的 **workflow 胶囊**。
> **边界**:1 同进程父子 · **过了哪些门**:C + D + G · **证据级别**:`observed`(源码逐文件读过)
> **影响力**(2026-10-31 实时采样):**153★ / 11 fork**;catalog 82★ → ×1.9
> **什么时候找它**:要一条**可复现**的多 agent 流水线,接受「不是断点续跑」

> 导航:[样本索引](../03-sample-encyclopedia.md) · [域章程](../README.md) · [三笔税机制谱](../02-coordination-mechanisms.md) · [四道边界](../01-collab-topology.md)

## 设计思路

**一句话设计思路**:把一次性多 Agent 调度升级成「可生成、可保存、可治理、可观察、可恢复」的 **workflow 胶囊** ——一个 JSON manifest + 一段受限 JS 的 `run(wf,args)`。

**它最反直觉的一条**:**没有 DAG、没有 step/node/edge**。JS 控制流本身就是编排;`wf.phase`/`parallel`/`pipeline`/`runAgent`/`spawnAgent`/`synthesize` 是编排词汇,每个「节点」就是一个**新的 DSH 子代理**。用代码表达控制流,而不是用数据结构表达控制流——这样并行/条件/循环都免费,代价是**图不可静态分析**。

**治理是它的重心**:三级信任(trusted-package / capability-generated / trusted-local);13 类 FORBIDDEN 静态正则 + QuickJS/WASM 独立堆双保险;胶囊字段精确白名单且**拒收 KodaX 格式**;全服务共享一个 `maxConcurrency` 部署信号量;token **开工前预留、结束后对账**。

**失败收敛**:`runAgent` 普通失败 → `null`;结构化输出最多 1 次同路由无工具修复;verification hard 模式同 actor 修复至多 3 轮,否则 `completed_unverified`/`failed`;无自动重试,幂等靠**结果缓存 + artifact 独占写**。

**必须准确表述的一点**:**「可恢复」= 从不可变快照整体重跑 + 按内容键回放结果缓存,不是断点续跑**;进程重启后活跃 run 丢失。而且它**明说不替换**原生 `ctx.workflows`——它是包在 `dsh-subagent` 之上的一层,不是替代。

**代价与失效**:`minDshVersion` 已存但全仓无比较逻辑;多进程共用绝对 runDirectory 无锁;嵌套 workflow 与父共享 maxAgents/token 配额;trusted-local 的 `.ts` 走 Node 模块缓存,不热更。

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | 不可变胶囊快照 `.dsh/workflow-runs/<runId>/` + 内容键结果缓存 | 进程重启后活跃 run 丢失 |
| 冲突裁决 | **不做**(每个 `runAgent` 是独立子代理,写同一工作区) | artifact 只做独占写,不裁决文件 |
| 失败收敛 | **整体重跑 + 缓存回放**,不是断点续跑 | 只保住「算出来的答案」,保不住「跑到一半的副作用」 |

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`omdsh-dev/dsh_workflow`](https://github.com/omdsh-dev/dsh_workflow) |
| **npm 包名** | `@dsh-external/workflow` |
| **版本(本次读)** | `0.1.2` |
| **License** | MIT |
| **npm 状态** | **未发布到公共 registry**(`@dsh-external/workflow` = 404) |
| **安装** | `dsh plugin --profile web add "github:dsh-external/dsh_workflow#main"` |
| **⚠ 仓库名与安装路径不一致** | 仓库在 `omdsh-dev/` 下,但上方安装命令用的是 **`github:dsh-external/dsh_workflow`**——两者不是同一 owner。**照着抄之前先去确认哪个是活的**;这就是为什么本文件同时给出仓库 URL 和安装串 |
| **接线方式** | 仅 `dsh.bundle.patch` → `cordis.patch.yml`(无 client 注入) |

## 借用指南

### 可借鉴(直接抄)

1. **用代码表达控制流,而不是用数据结构表达控制流** ——`run(wf,args)` 里 `phase/parallel/pipeline/runAgent`,并行、条件、循环全部免费,代价是图不可静态分析。先接受这个代价再选它,而不是选完才发现画不出图。
2. **不可变胶囊快照 + 内容键结果缓存**,得到的是「可复现」;诚实的话术是「整体重跑 + 回放已有答案」,不是断点续跑。
3. **治理三层**:静态禁用表(13 类正则)+ 隔离堆(QuickJS/WASM)双保险、字段精确白名单、三级信任。
4. **幂等靠结果缓存 + artifact 独占写**,而不是靠重试。

### 别照抄

- `minDshVersion` 存了却不比较——版本门形同注释;多进程共用一个绝对 runDirectory 却不加锁。
