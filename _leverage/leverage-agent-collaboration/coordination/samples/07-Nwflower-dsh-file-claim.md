---
title: "Nwflower/dsh-file-claim"
domain: agent-coordination
kind: sample
positioning: "`Nwflower/dsh-file-claim`：认领与被保护文件同目录的边车，pre-execute 返回 deny——在写路径上返回 deny 的样本（“唯一”是跨样本观察，仅覆盖四个工具）。"
takeaway: "同目录边车 + pre-execute deny；租约必须自己加 epoch，否则静默失锁。"
read_when: "怕两个人改同一个文件（写冲突）——只有这条路真拦得住。"
status: observed
updated: 2026-10-31
---
# 07 · `Nwflower/dsh-file-claim`

> **一句话**:认领与被保护文件同目录的边车,`tools/pre-execute` 返回 deny——在写路径上返回 deny 的样本；“唯一”是跨样本观察，覆盖边界见下。
> **边界**:2 同工作区多成员(只管冲突裁决) · **过了哪些门**:C + F + G · **证据级别**:`observed`(源码逐文件读过)
> **影响力**(2026-10-31 实时采样):**7★ / npm 1,064 次/月**
> **什么时候找它**:怕两个人改同一个文件——**只有这条路真拦得住**

> 导航:[样本索引](../../encyclopedia.md) · [域章程](../../00-map.md) · [三笔税机制谱](../02-mechanisms.md) · [四道边界](../01-taxonomy.md)
> **证据链**：仓库无 tag，pin `main@42f07e2`（0.2.0）；deny 覆盖、pid 判活、无 epoch 与 TOCTOU 见[`07 源码复核`](../_证据/07-file-claim-源码复核.md)。

## 设计思路

详见 [02 §5 标杆 A](../02-mechanisms.md#5-标杆)。这里只补它与成员模型的关系:

**它根本没有成员模型**。它不知道谁是“团队”,只知道哪个**会话**(`tag` = `exec.agent.id`)认领了哪个**路径**。这是它能在写面做硬拦截的原因——**它站在比团队更下面的一层**。

**它的 pending 三路合并区值得一提**:冲突时允许 B 写(需 A 活跃占用)、以 git HEAD 为 base,持有人在 release 时自动 3-way,冲突标记**直接写进真实工作树**、条目保留待人工处置。每路径只有一个槽,第二次写覆盖。

**这就是「冲突裁决」与「成员模型」互补的证明**:[04 limuyang2/agent-team](../../teams/samples/04-limuyang2-agent-team.md) 有成员模型但文件裁决是空壳,[07](07-Nwflower-dsh-file-claim.md) 有文件裁决但没有成员模型。**至今没有一个样本同时握有两端。**

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | 工作区边车 `<目标>.dshclaim`,无中央注册表 | 多机/NFS 场景 pid 判活会误杀 |
| 冲突裁决 | **`tools/pre-execute` 返回 deny**（仅 write/edit/bash/pwsh） | shell fail-open 面比“解析失败”更宽（`&&`/`\|\|`、多行、重定向、mv 源等）；无 fs 钩子；路径基准可能与真实写路径错位 |
| 失败收敛 | stale 2h + `process.kill(pid,0)` 判活即刻清孤儿 | **租约无 epoch**；pid 是宿主进程粒度，同宿主多会话崩溃不触发；后续写会被 deny（不是静默覆盖） |

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`Nwflower/dsh-file-claim`](https://github.com/Nwflower/dsh-file-claim) |
| **npm 包名** | `dsh-file-claim` |
| **版本(本次读)** | `0.2.0` @ `main 42f07e2`（仓库无 tag/release，版本号本身不可定位） |
| **License** | MIT |
| **npm 近 30 天** | **1,064 次**——比 7★ 的星标暗示的高两个数量级 |
| **安装** | `dsh plugin add dsh-file-claim`(README:90,一条命令) |
| **接线方式** | `main: ./index.mjs`；仓库只有 `index.mjs` 与 `claim.mjs` 两个源文件，**没有 `.js`** |
| **复现要点** | 边车文件直接落在被保护文件旁边,试用前先 `git status` 看一眼脏不脏 |

## 借用指南

### 可借鉴(直接抄)

1. **边车与被保护文件同目录** ——认领天然随仓库/分支走；但审计与跨进程锁在**工作区根**，不是完全没有中央文件。
2. **裁决落在 `tools/pre-execute` 的 `{kind:'deny'}`**,而不是提示词。提示词里的写范围永远只是建议。
3. **pid 判活即刻清孤儿 + 2h stale 兜底**，比纯 TTL 快、比纯心跳省；代价是它对“进程活着但会话死了”与跨机场景会误判。
4. **8 个工具 + 3 个命令共用一个 `run(argv)`** ——模型面与 CLI 面同源,不会长出两套语义。
5. **冲突走 pending 三路合并**,冲突标记直接写回真实工作树,条目留待人工处置——不假装能自动解决。

### 别照抄

- 租约**没有 epoch/fencing** ——被接管时原主 `sync` 只刷新自己还持有的边车,`mine=[]` 也不报错,原主**静默失锁**（但下一次写会被 deny，不是静默覆盖）;`inject` 只有 `['tools']`,没有 fs 钩子,所以「工具面内硬拒绝、工具面外君子协定」。
- 这两条是它自己的天花板,抄之前先想清楚你是否能补上。
