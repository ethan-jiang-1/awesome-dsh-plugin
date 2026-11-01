---
title: "Noelune/dsh-agent-relay"
domain: agent-crossing
kind: sample
positioning: "`dsh-agent-relay`：HTTP broker 连 dsh/Codex/Claude；源码 0.8.1 有 wake，但 npm latest 0.5.0 没有，回环只是默认不是强制。"
takeaway: "broker 默认回环但无强制校验；0.6–0.8 均未发布到 npm，装着 0.5.0 就没有 wake/长轮询。"
read_when: "要让不是 DSH 的 agent 和 DSH 成员通信。"
status: observed
also_in: "pipelines"
updated: 2026-11-01
tier: 典型
life: unpublished
evidence: L1
answers: Q5
---
# 13 · `Noelune/dsh-agent-relay`

> **一句话**：一个 HTTP broker 当消息总线，把 dsh/Codex/Claude Code/Python 连成对等链路。**默认绑回环，但 broker 侧没有回环校验**；`wake_command` 与长轮询只存在于未发布的 0.6–0.8 源码，npm 最新 0.5.0 没有。
> **边界**:3 跨进程(跨**异构 agent 运行时**,不限于 DSH) · **定位**:**broker 流派**代表:本域唯一「跨生态」的样本 · **证据级别**:`observed`(源码逐文件读过)
> **影响力**(2026-10-31 实时采样):**4★** / npm **1,048 次/月**;星标低但月下载四位数
> **什么时候找它**:要让**不是 DSH 的** agent(Codex / Claude Code / Python)和 DSH 成员通信

> 导航:[样本索引](../../encyclopedia.md) · [域章程](../../00-map.md) · [三笔税机制谱](../../coordination/02-mechanisms.md) · [四道边界](../../coordination/01-taxonomy.md)
> **证据链**：源码 pin tag `v0.8.1`=`7e43c54`；npm latest 却是 **0.5.0**（无 wake/长轮询、仍含 v1）；回环是默认非强制，见[`13 源码复核`](../_证据/13-agent-relay-源码复核.md)。

## 设计思路

**它解决的是别人不解决的那个问题:异构运行时之间的对等通信。** 同一台机器上并行跑着 `dsh`、`Codex`、`Claude Code`、`Hermes`,它们各自有独立的会话与工具系统——`dsh-agent-teams` 管不了 Codex,`dsh-interconnect` 只管 DSH 实例。Relay 的办法是**把通信降级成 HTTP + HMAC**,谁都能当客户端。

**Broker 只做路由,不做编排。** README 反复强调「通信与编排解耦」:它不是 DAG 引擎,不驱动控制流,只保证消息投到。

**鉴权**：源码 0.8.1 的调用走 HMAC-SHA256 签名、300 秒时间戳窗口与常量时间比较；但 npm 0.5.0 还带 v1 整代（rate limit/锁定/旧 store）。签名串是 **canonical JSON**(v3 在第二段插入 `keyId`);rate limit 与鉴权失败锁定**属于已删除的 v1 世代,现在没有**——README 如实写了「边界由只绑回环承担」。

**投递语义是本域最完整的一套**:请求默认**留存 7 天**、SQLite 单一路径持久化、**租约投递 + 令牌化确认**、服务端**长轮询唤醒**(落库即达)、失败/过期由服务端定时扫描**自动回发未送达通知**,并以**幂等键去重**。

**`wake_command` 是源码 0.8.x 最独特的一招**（npm 0.5.0 没有）：轮询模型要求接收方一直有进程活着，这在个人机器上经常不成立。给成员声明 `wake_command` 后,消息落库时若它 **90 秒内没取过件**,broker 会**按需启动一次**工作进程。作者写得很清楚:「它**真的会跑一次该成员的 CLI 并产生 API 费用**」,所以开关单独成一条命令、**默认只预演**;而且唤醒是**兜底而非竞争**——成员 90 秒内取过件就不会另起进程,避免同一消息被处理两次。

**它注册 6 个模型工具**（README 自身 5/6 矛盾）：`agent_relay_send` / `status` / `history` / `peers` / `retry` 等；以固定 commit 的工具表为准。

**它删掉了自己的一半**(本域最值得学的一节):v1 世代(`X-Relay-*` 头、`/register`、`/messages` 游标轮询)**已于 2026-09-19 移除**,理由是审计显示 **v1 队列表自 2026-08-15 起再无任何消息,且没有任何现役客户端注册过**。协议规范只维护在 `docs/PROTOCOL-V2.md` 一处,README 明确写「此处不再复制一份等着漂移」;跨语言字节一致性由 `test/protocol_v2_golden.py` 与 `test/protocol-v2-python.test.mjs` **两个测试锁住**。

**`doctor.mjs` 自检报什么**:broker 是否可达、**谁真的能收消息**、队列积压、**两处凭据是否漂移**、明文密钥、WAL 是否膨胀、线上 adapter 与仓库基线是否一致。退出码 0/2/1。

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`Noelune/dsh-agent-relay`](https://github.com/Noelune/dsh-agent-relay) |
| **npm 包名** | `dsh-agent-relay` |
| **版本(本次读)** | 源码 tag `v0.8.1`=`7e43c54`；**npm latest 仍是 0.5.0**（0.6–0.8 未发布；0.5.0 无 wake/长轮询且仍含 v1） |
| **License** | MIT |
| **npm 近 30 天** | **1,048 次**(2026-09-30 ~ 10-29) |
| **安装** | `dsh plugin --profile web add dsh-agent-relay` 装到 npm 0.5.0（旧代）；要 0.8.1 只能 GitHub 安装。`dsh1024` 是无关包，别混 |
| **接线方式** | `main: lib/index.js`;`dsh.bundle.patch` + **有 client 注入** |
| **默认端口** | `127.0.0.1:19121`，**默认回环但 broker 侧无校验**；唯一的远端地址检查在插件状态路由 |
| **成员配置** | `~/.dsh/agent-relay.json`——**只记 vault 条目名,不记明文密钥** |
| **凭据来源** | 环境变量 `AGENT_RELAY_*` / `DSH_RELAY_*`,或指向已有 dotenv,或 DPAPI 保管库(`AGENT_RELAY_SECRET_REF` + `AGENT_RELAY_VAULT_MODULE`) |
| **自检** | `node setup/doctor.mjs`,或 `node adapters/cli/relay.mjs doctor` |
| **接入方式** | MCP(Codex / Claude Code / Qoder / 任意 MCP 宿主)、CLI、JS 客户端、Python 客户端 |

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | broker 侧 **SQLite 单一路径**持久化,请求留存 7 天 | 真相源在 broker,不在任何 agent 侧;broker 挂了链路就断 |
| 冲突裁决 | 不适用(只投消息,不动文件) | — |
| 失败收敛 | 租约投递 + 令牌确认 + 幂等键去重 + 超期通知；DSH 侧 reply 无会话映射时 ack 后丢弃 | v1 限流/锁定已删；回环是默认边界，不是代码强制 |

## 借用指南

### 可借鉴(直接抄)

1. **`wake_command`:把「收件人没在跑」从失败变成兜底** —— 消息落库时若成员 90 秒内没取过件,broker 按需启动一次工作进程;并且**兜底而非竞争**(取过件就不另起)。这是本域唯一真正解决「对端离线」的设计,DSH 侧的 `interconnect` 没有、`takeover` 靠同步盘绕开。
2. **危险开关默认只预演** —— `enable-wake.mjs --agent codex` 先只打印将写入的行,要 `--apply` 才真写(且自动备份),写清楚「真的会产生 API 费用」。**凡是会花钱或会改线上状态的开关,都该这样设计。**
3. **两处凭据漂移检测进 `doctor`** —— 「明文密钥、两处凭据是否漂移、WAL 是否膨胀」这些是运维型插件的必备自检项,大多数样本没有。
4. **凭据只存引用不存明文** —— `agent-relay.json` 只记 vault 条目名;让宿主 dotenv 别成为密钥的第二个明文副本。
5. **删掉自己的一半,并把理由写下来** —— v1 因「队列表自 2026-08-15 起再无消息、无现役客户端注册」被整体移除。**能删代码的项目才是活的项目。**
6. **协议文档只维护一处,并用跨语言 golden 测试锁死** —— README 明说不在两处各写一份等着漂移;字节级一致性由两个测试守。
7. **常量时间比较 + 300 秒重放窗口 + canonical JSON 签名** —— 三件套齐全,是跨语言协议的底线。

### 别照抄

- 别以为有 HMAC 就安全了:**rate limit 与鉴权失败锁定已被删除**,安全边界完全由「只绑 127.0.0.1」承担。一旦改成对外监听,需要自己补这两道闸。
- 别把 `wake_command` 当免费功能:它会**真的跑一次 CLI 并产生 API 费用**。
- 它跨的是**进程**,不是**工作区**——不提供任何文件裁决或成员状态,别指望它当团队插件用。
