---
title: "toolclub/dsh-agent-team-gui"
domain: agent-teams
kind: sample
positioning: "`toolclub/dsh-agent-team-gui`：它自己就是 team runtime（8 表 + 2 工具 + pre-step 调度），Web 面只加 4 个槽；on-demand 是可选项，不是运行时默认。"
takeaway: "on-demand 靠 systemPrompt + pre-step 早退，但 shipped/legacy 默认 guaranteed；成本借宿主 tokenUsage；无检查点，重启即 interrupted。"
read_when: "想省掉「先起一个规划器」的调用成本，并逐成员配模型/工具。"
status: observed
updated: 2026-10-31
---
# 02 · `toolclub/dsh-agent-team-gui`

> **一句话**:小队是**用户预先存好的配置**,默认**由主 Agent 按需决定**用不用;派工跑一条有界 DAG,结果进 Run Center。
> **边界**:1 同进程父子 + 2 同工作区多成员 · **过了哪些门**:C + G · **证据级别**:`observed`(源码逐文件读过)
> **影响力**(2026-10-31 实时采样):**285★ / 5 fork**;catalog 84★ → ×3.4
> **什么时候找它**:想省掉「先起一个规划器」的调用成本,并且要逐成员配模型/工具

> 导航:[样本索引](../../encyclopedia.md) · [域章程](../../00-map.md) · [三笔税机制谱](../../coordination/02-mechanisms.md) · [四道边界](../../coordination/01-taxonomy.md)
> **证据链**：固定 release `v1.3.0 → 14ea1196` 的实现、默认值、槽位与 CI 见[`02 源码复核`](../_证据/02-team-gui-源码复核.md)。

## 设计思路

**一句话设计思路**:小队是**用户预先存好的配置**(成员 + 逐成员模型与工具策略),默认**由主 Agent 按需决定**用不用它;派工执行一条**有界 DAG**,结果进 Run Center。

**它真正的创新在一句提示词里**,不在代码里。`agent/pre-step` 在 `triggerMode: 'model-tool'` 下读到 squad 就**直接 return** ——不启规划器、不启成员、不建 run。判定写在 systemPrompt section `agent-team:squad-mode` 里:

> This team is AVAILABLE ON DEMAND, not mandatory. Decide within your normal reasoning whether delegation adds value. Do not start a planner or workers just to decide whether this team is needed.

**为什么这是设计而不是偷懒**:作者明确拒绝再加一个 router Agent(「没有额外的路由 Agent」)。反向对照是它的 `activationMode='smart'`——那个跳过发生在**规划之后**,规划调用已经花掉了,且同一消息不能再派工。on-demand 把决策前移到**零成本位置**。这是本域最便宜的一次成本优化:**把判断塞进本来就一定会发生的那次推理里**。

**成员是什么**:真子代理,`ctx.subagents.start(provider, {parent, agentOptions, toolFilter, maxDepth:1})`,逐成员 provider/model/maxTokens/toolScope。它不是"另一个 runtime 的 GUI":宿主侧自带 8 张存储表、2 个模型工具、tool guard 与 pre-step 调度；Web 面只加 4 个 additive 槽（settings.section / conversation.input.right / input.dock / conversation.view），没有侧栏。

**它的成本计量值得单独抄**:适配器读官方 session 的 `tokenUsage` projection 四桶(uncachedInput/cacheRead/cacheWrite/output),**0 样本返回 `undefined` 而不是伪造 0**,并附 full/partial/none 覆盖度。**不自己记账,借宿主账本。**

**代价与失效**:判断是提示词引导,不是数学保证(作者自认「不能证明所有模型都永远不把简单任务派给小队」);lead 自身推理 token 不计入统计,省下的成本在 Run Center 里**不可观测**;派工失败会注入可见提示要求 lead 披露，不是静默降级;**无执行级检查点** ——重启后所有活动 run → interrupted,pending/running 成员 → interrupted,且 interrupted 被排除在可续跑之外;`contextMode: 'chain'` 只向依赖节点传 handoff,非依赖的前序结果不会传递。有界 DAG 限节点 ≤32、每节点依赖 ≤32、并发 ≤32、重试 1 次、质量返工 ≤2 轮、续跑 1 次——**但不限深度**。

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | 宿主 `storageDomain` 8 表（`agent_team_gui`, version 0），有官方持久化后端 | 只能读自己域；无跨进程锁，跨进程并发 `[OPEN]` |
| 冲突裁决 | **不做**,连建议性写范围都没有 | 共享 checkout 完全裸露 |
| 失败收敛 | **不收敛**:启动时 active→interrupted，interrupted 不可续跑（只 failed/partial 可续 1 次） | 有持久运行记录 ≠ 可恢复 |

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`toolclub/dsh-agent-team-gui`](https://github.com/toolclub/dsh-agent-team-gui) |
| **npm 包名** | `dsh-agent-team-gui` |
| **版本(本次读)** | `1.3.0`(本域唯一 1.x) |
| **License** | MIT |
| **npm 状态** | **未发布到公共 registry**(`registry.npmjs.org/dsh-agent-team-gui` = 404)。只能走 Git/GitHub release 包 |
| **安装** | 编译产物 release 包(推荐,免跑 `prepare` 构建、免配 `allowBuilds`);或直接 Git 安装 |
| **接线方式** | `dsh.bundle.patch` → `cordis.patch.yml` + `dsh.client`(**`platform: web`**,是 Web 端插件) |
| **复现要点** | 装完/升级完**必须重启已在跑的 DSH Web 进程**,再去 **Settings → Teams**；v1.3.0 的 peer range 只覆盖 0.1.5 线，`0.1.7-rc.2` 与本书基线 `0.2.1-rc.3` 都不在内——后者安装行为 `[OPEN]`（作者对 0.1.7 的拒绝说明仅在 main，不在 tag） |

## 借用指南

### 可借鉴(直接抄)

1. **「要不要派活」写进 systemPrompt 的 on-demand 段 + `agent/pre-step` 早退** ——决策发生在本来就要发生的那次推理里,额外成本为零。凡是要先起一个 router agent 才知道该不该派活的方案,都已经先花掉了一次调用。
2. **成本计量借宿主账本**:读 session 的 `tokenUsage` 四桶,`0 样本返回 undefined 而不是伪造 0`,并标 full/partial/none 覆盖度。自己另记一套账,迟早和宿主对不上。
3. **成员配置在「小队」里预设** ——逐成员 provider/model/maxTokens/toolScope,派工时不再讨论用什么模型。

### 别照抄

- 「默认不派活」是**提示词引导**,作者自己写明「不能证明所有模型都永远不把简单任务派给小队」——别在文档里写成保证。
- 也别把「有持久运行记录」当「可恢复」:重启后活动 run 全部 interrupted,而且 interrupted 被显式排除在可续跑之外。
