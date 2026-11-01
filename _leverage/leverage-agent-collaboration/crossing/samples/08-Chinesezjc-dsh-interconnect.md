---
title: "Chinesezjc/dsh-interconnect"
domain: agent-crossing
kind: sample
positioning: "`Chinesezjc/dsh-interconnect@0.13.0`：每个已配置对端一条拨号 WS（互配两条），投递到对端 session inbox；无幂等/无离线队列。"
takeaway: "每对端一条持久 WS + inbox；跨 DSH 实例，无幂等、无离线队列。"
read_when: "要跨实例投消息或同步事件，且能接受无幂等、无离线队列。"
status: observed
updated: 2026-10-31
also_in: "teams"
---
# 08 · `Chinesezjc/dsh-interconnect`

> **一句话**：每个已配置对端一条拨号 WebSocket（互配的一对实例之间有两条），把文本投进对端某个 session 的 inbox，并把本实例生命周期事件 fan-out；无幂等、无离线队列。
> **边界**:3 跨进程/跨机(跨 **DSH 实例**) · **过了哪些门**:F + G · **证据级别**:`observed`(源码逐文件读过)
> **影响力**(2026-10-31 实时采样):**38★ / 3 fork**
> **什么时候找它**:要跨实例投递消息或同步事件,且能接受无幂等、无离线队列

> 导航:[样本索引](../../encyclopedia.md) · [域章程](../../00-map.md) · [三笔税机制谱](../../coordination/02-mechanisms.md) · [四道边界](../../coordination/01-taxonomy.md)
> **证据链**：npm 0.13.0 ↔ tag `v0.13.0` ↔ commit `5547b03`；投递/鉴权/退避与“对齐闸已退役”见[`08 源码复核`](../_证据/08-interconnect-源码复核.md)。

## 设计思路

**一句话设计思路**:每个已配置对端一条持久 WebSocket(挂在宿主 webserver 上,不自建进程;一对互配实例各拨一条，共两条),把一段文本投进对端**某个 session 的 inbox**,并把本实例的生命周期事件 fan-out。

**边界精度**(它常被误解为跨机派活,其实不是):它跨的是**DSH 实例**,寻址两级——peers 键是**操作者配置的键**（不自动回写 `hello.sender`，不一致只 warn 一次）,实际拨号 origin 才是线上寻址,再落到对端 `sessionId`。**子代理拥有的会话被显式过滤掉**;没有任务、没有租约、没有 worktree。

**语义值得逐条区分**:`send` = 投 inbox 并调 `agent.followup/steer/inject`;`event` = 只做本地 `ctx.parallel('interconnect/event')` 分发,**不进会话**;`source` 与 `sender` 都**不进模型上下文**。

**它的两个空洞是设计级的**：**无消息级幂等**（`reqId` 只做关联，超时即删 pending，重试可能重复投递）、**无离线队列**（链路断即 `unreachable`，不缓存；事件也不补发）。要区分“离线”的两种含义：链路断一定丢；session 不 live 可被 `resume` 唤醒。本机还有一张内存 `senders` 表，是 `reply` 的唯一依据，**重启即丢**（回信变 `no-sender-known`）。

**工程策略是历史工具，不是现状**：它确有 `check-upstream-alignment.mjs` 双遍闸与 `port-upstream-change.mjs` 搬运脚本，但仓库 `RELEASING.md` 写明该流程 **2026-09-16 已作废**、**2026-09-25 起与上游分叉**，对齐闸此后“必然判红”（报的是分叉本身，不是漂移）。可抄的是工具链方法，**不能抄“与上游等价”的结论**；脚本需要私有上游 worktree，CI 里也跑不了。

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | 对端实例的 session inbox（经 `agent.followup/steer/inject` 投递） | 无离线队列，链路断即 `unreachable`；本机 `senders` 内存表重启即丢 |
| 冲突裁决 | 不适用(投递消息,不共享工作区) | — |
| 失败收敛 | 30s 心跳 + `min(30s, 1s·2^n)` 退避;**无消息级幂等** | 重试可能重复投递 |

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`Chinesezjc/dsh-interconnect`](https://github.com/Chinesezjc/dsh-interconnect) |
| **npm 包名** | `dsh-interconnect` |
| **版本(本次读)** | `0.13.0` @ tag `v0.13.0` = commit `5547b03`（npm gitHead 同 SHA） |
| **License** | MIT |
| **npm 近 30 天** | **1,017 次**(38★) |
| **安装** | `dsh plugin --profile <name> add dsh-interconnect`;或 `dsh plugin --profile <name> add file:/path/to/dsh-interconnect` |
| **接线方式** | profile bundle:`cordis.patch.yml` 里 `insert` **三个插件行** |
| **复现要点** | tarball 自带 `lib/*.js` 与 `.d.ts`,**安装时不跑构建**;**代码更新必须重启实例**(hmr 只重算 manifest,不重建 `lib/`) |
| **自检法** | 作者实测:装前 `GET /interconnect/link` → 404;装后 6 秒内同一请求 → **403**(插件 fail-closed 的应答)。这是判断「装没装上」最干脆的办法 |

## 借用指南

### 可借鉴(直接抄)

1. **寻址两级分离** ——peers 键是**操作者配置的键**（不自动回写 `hello.sender`，不一致只 warn 一次）,实际拨号 origin 才是线上寻址,再落到对端 `sessionId`;身份与地址不混用一个字段。
2. **`event` 与 `send` 分流** ——生命周期事件只做本地 fan-out,**永不进会话**,不污染模型上下文。
3. **token 校验 fail-closed 403,先 sha256 归一再用 `timingSafeEqual`**。
4. **退避 `min(30s, 1s·2^n)`**。
5. **双遍对齐闸 + 机械 diff 搬运（历史方法）** ——工具链可抄；但该闸已随分叉退役（2026-09-16 作废，上游 ref 冻结），只能当“如何做对齐闸”的参考，不能当“与上游等价”的保证。

### 别照抄

- 没有 message-id 幂等就不要重试;没有离线队列就不要承诺「消息不会丢」;更别把「跨实例投递到某个 session」说成「跨机派活」——它没有任务、没有租约、没有 worktree。
