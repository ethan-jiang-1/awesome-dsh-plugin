# 08 · `Chinesezjc/dsh-interconnect`

> **一句话**:每个对端一条持久 WebSocket,把文本投进对端某个 session 的 inbox,并把本实例生命周期事件 fan-out。
> **边界**:3 跨进程/跨机(跨 **DSH 实例**) · **过了哪些门**:F + G · **证据级别**:`observed`(源码逐文件读过)
> **影响力**(2026-10-31 实时采样):**38★ / 3 fork**;F 探针 `interconnect` = **1/7924**
> **什么时候找它**:要跨实例投递消息或同步事件,且能接受无幂等、无离线队列

> 导航:[样本索引](../03-sample-encyclopedia.md) · [域章程](../README.md) · [三笔税机制谱](../02-coordination-mechanisms.md) · [四道边界](../01-collab-topology.md)

## 设计思路

**一句话设计思路**:每个对端一条持久 WebSocket(挂在宿主 webserver 上,不自建进程),把一段文本投进对端**某个 session 的 inbox**,并把本实例的生命周期事件 fan-out。

**边界精度**(它常被误解为跨机派活,其实不是):它跨的是**DSH 实例**,寻址两级——peers 键是对端自报的 `instanceId`,实际拨号 origin 才是线上寻址,再落到对端 `sessionId`。**子代理拥有的会话被显式过滤掉**;没有任务、没有租约、没有 worktree。

**语义值得逐条区分**:`send` = 投 inbox 并调 `agent.followup/steer/inject`;`event` = 只做本地 `ctx.parallel('interconnect/event')` 分发,**不进会话**;`source` 与 `sender` 都**不进模型上下文**。

**它的两个空洞是设计级的**:**无消息级幂等**(`reqId` 只做关联,超时即删 pending,重试可能重复投递)、**无离线队列**(down 即 `unreachable`,不缓存);但离线 session 可 resume 唤醒。

**工程策略是本域独一份**:它的 spec 与上游 monorepo **逐行同步**,并有 `check-upstream-alignment.mjs` 双遍闸(骨架比对 + 含注释原文比对,白名单外任何差异=漂移);`port-upstream-change.mjs` 按映射表机械搬运上游 diff 并自动跑闸。意义是**树外发布通道与上游行为等价性可机械验证** ——但 CI 不跑这道闸。

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | 对端实例的 session inbox(经 `agent.followup/steer/inject` 投递) | 无离线队列,down 即 `unreachable` |
| 冲突裁决 | 不适用(投递消息,不共享工作区) | — |
| 失败收敛 | 30s 心跳 + `min(30s, 1s·2^n)` 退避;**无消息级幂等** | 重试可能重复投递 |

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`Chinesezjc/dsh-interconnect`](https://github.com/Chinesezjc/dsh-interconnect) |
| **npm 包名** | `dsh-interconnect` |
| **版本(本次读)** | `0.13.0` |
| **License** | MIT |
| **npm 近 30 天** | **1,017 次**(38★) |
| **安装** | `dsh plugin --profile <name> add dsh-interconnect`;或 `dsh plugin --profile <name> add file:/path/to/dsh-interconnect` |
| **接线方式** | profile bundle:`cordis.patch.yml` 里 `insert` **三个插件行** |
| **复现要点** | tarball 自带 `lib/*.js` 与 `.d.ts`,**安装时不跑构建**;**代码更新必须重启实例**(hmr 只重算 manifest,不重建 `lib/`) |
| **自检法** | 作者实测:装前 `GET /interconnect/link` → 404;装后 6 秒内同一请求 → **403**(插件 fail-closed 的应答)。这是判断「装没装上」最干脆的办法 |

## 借用指南

### 可借鉴(直接抄)

1. **寻址两级分离** ——peers 键是对端自报的 `instanceId`,实际拨号 origin 才是线上寻址,再落到对端 `sessionId`;身份与地址不混用一个字段。
2. **`event` 与 `send` 分流** ——生命周期事件只做本地 fan-out,**永不进会话**,不污染模型上下文。
3. **token 校验 fail-closed 403,先 sha256 归一再用 `timingSafeEqual`**。
4. **退避 `min(30s, 1s·2^n)`**。
5. **spec 与上游逐行同步 + 双遍对齐闸 + 机械 diff 搬运** ——把「与上游行为等价」变成可机械检测的事。

### 别照抄

- 没有 message-id 幂等就不要重试;没有离线队列就不要承诺「消息不会丢」;更别把「跨实例投递到某个 session」说成「跨机派活」——它没有任务、没有租约、没有 worktree。
