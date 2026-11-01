---
title: "SEAMS · 接缝选择表与被认可的协作路线"
domain: agent-collab
kind: guide
positioning: "跨家族参照系：优先用宿主协作接缝的六条立场、四道边界的接缝矩阵、三问判定与偏离登记。"
read_when: "要在「用原生接缝」和「自建总线/协议/调度」之间选，或评审一个方案的偏离代价。"
status: living
updated: 2026-11-01
budget: 150
---
# 接缝选择表

> 本册的立场只有一句：**协作优先落在宿主已有的接缝上；要自建，先认领代价。**
> 家族细节在各自 README；兼容性在 [`COMPAT`](./COMPAT.md)；本文件只回答「该用哪条缝、自建要付什么」。

## 0. 六条立场

| # | 立场 | 合格 | 不合格 |
|---|---|---|---|
| P1 | 委派走 `startActivation`，不自造子代理池 | 本地 spawn/fork、外部 provider 两条分支 | 自己起进程/线程当子代理 |
| P2 | 团队状态优先放会话日志或宿主 storage | `team/member`、`team/task` 事件；CAS | 自建第二真相源却不认领同步代价 |
| P3 | 拦截写在 `tools/pre-execute`，不写在提示词里 | 返回 deny / ask | 「请在写之前先检查」当保证 |
| P4 | 文件隔离用 worktree，不用自研锁 | `ctx.worktrees.create` | 用锁保护共享 checkout |
| P5 | 远程控制用 gateway / ACP，不自造协议 | Peer + 资源级 policy；ACP 受信控制器 | 自开端口 + 共享 token 当鉴权 |
| P6 | 状态诚实 | 失败落成可读状态（denied / stale / blocked） | 静默缺失、假成功 |

**为什么是这六条**：它们分别对应本册四道边界上唯一被宿主验证过的接缝（`dsh-subagent`、`dsh-experimental-agent-team`、`dsh-tools`、`dsh-experimental-worktree`、`dsh-api-gateway`/`dsh-acp`）。**不是「官方推荐」，是「唯一有源码背书的路径」**。

## 1. 接缝矩阵

| 边界 | 原生接缝 | 给什么 | 不给什么 | 什么时候才自建 |
|---|---|---|---|---|
| 1 同进程父子 | `dsh-subagent.startActivation` | 可续/一次性、深度与容量、三条回传通道 | durable parent mailbox | 需要「父不在也能收」→ 自建并认领投递语义 |
| 2 同工作区多成员 | `dsh-experimental-agent-team` | roster/任务日志、CAS、inbox | 跨进程、owner 自动释放、写互斥 | 需要跨进程 → 自建并认领锁与归属 |
| 2 写冲突 | `tools/pre-execute` | deny / ask、审批审计 | 文件级租约、fencing、多文件事务 | 需要 epoch → 自建并认领过期语义 |
| 2 文件隔离 | `dsh-experimental-worktree` | 分支 + 检出、沙箱内 | lane 管理、合并、清理 | 需要自动合并 → 自建集成树 |
| 3 远程控制 | `api-gateway` + `api-remote-access` | RPC/流、Peer、资源级 policy | 实例间消息、离线队列 | 需要消息总线 → 自建并认领幂等 |
| 3 外部运行时 | `dsh-acp` | 持久会话、单在途提示词 | fork、回放、附加目录 | 需要回放 → 自建记录层 |
| 3 编排 | `dsh-tool-workflow` | 脚本扇出、后台 job | DAG、重放、断点 | 需要图/断点 → 自建控制面 |

## 2. 三问判定

```text
① 原生接缝能不能直接满足？      → 查 §1；能就到此为止
② 不能的话，插件层能不能补？    → bundle 里的插件 + pre-execute / workflow / worktree
③ 还不能，才新造进程 / 协议 / 总线 → 认领安装、鉴权、幂等、清理的全部代价
```

**第 ③ 步的代价清单**（答不全就不要自建）：谁装、谁升级、谁鉴权、谁去重、谁清理、坏了谁收敛、跨版本怎么活。

## 3. 偏离登记

未登记的偏离视为不允许。每条都要写**代价**与**退出条件**。

| 样本 | 偏离 | 代价 | 退出条件 |
|---|---|---|---|
| 01 `agent-teams` | 团队状态搬回磁盘 `team.json` | 跨进程覆盖写 | 需要跨进程时改用 CAS 存储 |
| 04 `agent-team` | 成员＝独立根 Agent | 无父子上下文；roster 自建 | 成员需要异构权限/模型时才用 |
| 06 `remote-agent` | hub/worker 自建远端 loop | 信任边界扩大（hub 可 exec） | 无（这就是它的定位） |
| 08 `interconnect` | 每对端一条 WS 的实例间总线 | 无幂等、无离线队列 | 补消息 id + 去重后才承诺投递 |
| 09 `takeover` | 文件总线 + 同步盘 | 无实时性、无回执 | 需要实时才换通道 |
| 13 `agent-relay` | HTTP broker | 机制未发布（0.6–0.8 源码） | 发布后再评估 |
| 14 `team-rooms` | 房间存储为权威 | 新宿主上投影为空 fold | 宿主恢复 fact 事件 |
| 03 `dsh_workflow` | 胶囊 + 内容键缓存 | 无断点，整脚本重跑 | 需要断点才自建控制面 |
| 11 `taskswarm` | 每 lane 一个 worktree + `_orch` | 无自动合并/清理 | 需要自动合并才自建 |
| 10 `expert-mode` | 无插件，全静态 composition | rc.3 不挂载（preset 目录无人读） | 宿主恢复该目录才成立 |
| 18 `agent-dag-workflow` | 自建声明式 DAG 引擎（模板 + journal + 重放） | 模板/引擎/恢复三套语义自己维护；适配器依赖 `workflow*` 服务 | 只需要「跑完就算」时回原生 `workflow` 工具 |

## 4. 判据：什么时候值得自建

自建只有在三种情况下划算，且必须写进 `BACKLOG`：

1. **原生接缝的空白是产品核心**（例如跨实例消息就是 interconnect 的全部价值）；
2. **你能承受「自建件比宿主活得短」**——宿主一次改事件表就能让它失效（14 就是先例）；
3. **你有可复现证据证明原生不够**（L2 以上），而不是「原生没文档」。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 六条立场对应唯一有源码背书的接缝 | `[SRC-DSH]` | 各家族篇的首节行号 | 随 rc 版本复核 |
| 偏离代价取自样本卡与 memo | `[SRC-TARGET]`/`[OBS]` | 18 张卡 + 分诊表 | 代价是观察判断，非定量 |
| 「自建件比宿主活得短」 | `[OBS]` | 14 的宿主事件表变更 | 单一样本归纳，可争论 |
