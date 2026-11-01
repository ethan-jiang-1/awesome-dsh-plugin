---
title: "zbzbhs/dsh-remote-agent"
domain: agent-crossing
kind: sample
positioning: "`zbzbhs/dsh-remote-agent`：一个包双角色（hub/worker），副机跑完整 loop；凭证不走协议，但 hub 有 exec/read 能力。"
takeaway: "副机跑完整 loop（in-process 或 spawn headless）；插件不要求凭证过线，但 hub 可 exec/read；跨机最终是信任问题。"
read_when: "要跨机，且不能被网络拖死——链路断了工作照常继续。"
status: observed
also_in: "delegation"
updated: 2026-11-01
tier: 典型
life: active
evidence: L1
answers: Q5
---
# 06 · `zbzbhs/dsh-remote-agent`

> **一句话**：一个包双角色，副机**本地跑完整 loop**（优先 in-process，否则 spawn `dsh headless`）；**凭证不过协议**，但 hub 可 `exec`/`remote_read`——最终是信任边界，不是“永不出机”的绝对保证。
> **边界**:3 跨进程/跨机 · **过了哪些门**:F + G · **证据级别**:`observed`(源码逐文件读过)
> **影响力**(2026-10-31 实时采样):**4★**
> **什么时候找它**:要跨机,且**不能被网络拖死** ——链路断了工作照常继续

> 导航:[样本索引](../../encyclopedia.md) · [域章程](../../00-map.md) · [三笔税机制谱](../../coordination/02-mechanisms.md) · [四道边界](../../coordination/01-taxonomy.md)
> **证据链**：pin `main@cc356e1`（0.9.11，无 tag）；双角色、两种 worker 后端、配对/鉴权与偏差见[`06 源码复核`](../_证据/06-remote-agent-源码复核.md)。

## 设计思路

**一句话设计思路**:一个包双角色(`hub|worker|both|auto`),副机**本地跑完整 loop**（两种后端之一），模型凭证**不经协议传输**；主机只收回 handoff 摘要与产物清单，但可按权限执行 shell/读 roots。

**为什么它把跨机从传输问题降级为信任问题**:工作的所有者本来就是副机,所以**链路断了不丢工作**。这是本域最重要的一条架构判断——只要把「谁在执行」和「谁在持有连接」解耦,跨机的可靠性就不再依赖网络。

**子代理的具体做法(它其实不派子代理)**:`subagent-provider.js` 让主机侧的委派工具把任务投到远端,但 provider 的 `capabilities` **全部为 false** ——不投工具集、不传模型 key,只传 `{provider, model}` 选择。副机把 goal 包成**自带上下文的「任务书」**再 `followup()`,因为「副机的 agent 是独立 Agent,它不知道自己在被远程派单」。**跨机委派不是子代理的一种,是另一种东西。**

**传输**:direct = 自研 WS 拨 `19387`;relay = VPS 纯转发 + 业务帧 X25519→HKDF→AES-256-GCM(信封明文供路由);心跳 15s/超时 45s,退避 1s→30s+抖动。配对码 `dshra1://` 是 **7 字段配置打包串,不过期、不核验** ——真正的长期凭证是 `nodeToken` 与 hub 的 ed25519 身份 + TOFU pin(`hubfp1-`)。

**它贡献了本域最值钱的一条失败语义**:见 [02 §3.3](../../coordination/02-mechanisms.md)——DSH 的 `kick()` 吞掉 turn 内错误导致「假成功」,修法三步并用**源码静态断言**钉住。

**产物协议也值得抄**:产物三分(final/intermediate/other),**intermediate 优先** ——「如果 final 优先,一条宽松的 `dist/**` 会把 `dist/*.log` 也捞进去」;按需拉取只回 manifest,字节显式 pull;hub 落 `.part` **边收边算 sha256**,通过才 rename;断点续传用旁车记 `startOffset`。

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | **副机本地 DSH**,主机只收摘要与产物清单 | 副机要独立管凭据、独立升级 |
| 冲突裁决 | 不适用(工作不共享工作区) | — |
| 失败收敛 | 心跳 15s / 超时 45s / 退避 1s→30s;**链路断不影响正在跑的工作** | 副机失联后 hub 侧无独立完成验证 |

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`zbzbhs/dsh-remote-agent`](https://github.com/zbzbhs/dsh-remote-agent) |
| **npm 包名** | `dsh-remote-agent` |
| **版本(本次读)** | `0.9.11` @ `main cc356e1`（仓库无 `v0.9.11` tag；npm latest 已是 0.9.12，同树） |
| **License** | MIT |
| **npm 近 30 天** | **3,103 次**(2026-09-30 ~ 10-29)——**是 4★ 完全看不出来的体量** |
| **安装** | `dsh plugin add github:zbzbhs/dsh-remote-agent`;或 `npm install -g dsh-remote-agent`(增强/worker 端可独立装) |
| **接线方式** | `main: ./lib/index.js`；**无第三方运行时依赖**（`dependencies` 只有宿主提供的 `@deepseek-ai/schemastery`；README 的 “零外部依赖/验 lockfile” 说法被 CI 注释否定：仓库 `.npmrc` 无 package-lock） |
| **复现要点** | hub 与 worker 是**同一个包的两个角色**;worker 端必须在**它自己的机器**上装好完整 DSH |

## 借用指南

### 可借鉴(直接抄)

1. **假成功检测** ——DSH 的 `kick()` 是 `try { while (await this.turn()) } catch (_e) {}`,**turn 内错误被完全吞掉,只经 `agent/error` 事件暴露**;判据必须加 `hadError`,`ok = !timedOut && !aborted && !hadError`,并把 stderr 塞进 `task/end.error`。更值得抄的是它的**测试手法**:agent 分支在单测里跑不起来,于是用**源码正则静态断言**钉死这三条。
2. **产物三分 final/intermediate/other 且 intermediate 优先** ——「如果 final 优先,一条宽松的 `dist/**` 会把 `dist/*.log` 也捞进去」。
3. **`.part` 边收边算 sha256,通过才 rename**;续传用 sidecar 记 `startOffset`。
4. **协议只传 `{provider, model}`,永不传 key**。

### 别照抄

- 把配对码当安全边界——`dshra1://` 只是**不过期、不核验**的配置打包串（但它携带 hub 指纹，是 TOFU 的分发渠道），真正的凭证是长活 `nodeToken` 与 hub 的 ed25519 身份 + TOFU pin；`nt_` 泄漏即长期访问。
- 也别抄 `ok = !timedOut && !aborted` 这种「没超时就算成功」的判据。
