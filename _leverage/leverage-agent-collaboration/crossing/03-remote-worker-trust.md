---
title: "远端 worker：把“跨机”降级为信任问题"
domain: agent-crossing
kind: card
positioning: "远端执行的三层：谁跑 loop、凭证怎么走、主机能对副机做什么；以 06 remote-agent 为例，划清“任务在副机”与“主机仍可执行”的边界。"
takeaway: "副机本地跑完整 loop 不等于主机碰不到它：hub 常有 exec/read 能力；凭证不过协议，但信任是不对称的。"
read_when: "要做跨机执行/远端 worker，或评审“凭证不出机”类宣传时。"
status: observed
updated: 2026-11-01
---
# 03 · 远端 worker

> 跨机方案最容易过度承诺的一句是“凭证永不出机”。协议层可能真的不带 key，但 hub 往往仍能在副机执行命令、读文件——这是**信任边界**问题，不是传输问题。

## 1. 谁在跑 agent loop

`dsh-remote-agent` 一个包两个角色：`hub | worker | both | auto`。worker 有两种后端：

- in-process：`agentLoop.createAgent` + `followup` + `whenIdle`（需要宿主 `agentLoop`/`sessions`）；
- spawn `dsh headless`：任务书走 stdin，**不能指定模型**。

两种都失败时任务不可用；卡片常省略这个二选一。

## 2. 凭证边界

- 协议里只有 `{provider, model}`，不传 key；全 lib 无 key 转发。
- 但 hub 有 `mode:exec` 可在副机跑 shell（继承全量 env），有 `remote_read` 读 roots 内文件；exec 默认 `approval:'manual'` 是缓解项，不是消除项。
- 作者自己写“不要把副机接到你不信任的主机”。

**准确说法**：“插件不要求凭证过线”，不是“凭证永不出机”。

## 3. 传输与配对

- hub 监听 19387（默认绑 Tailscale/私网/回环，永不通配）；worker 拨号；relay 模式走 8890。
- 配对串 `dshra1://` 是 7 字段配置打包，无过期/签名，但携带 token 与 hub 指纹（TOFU 唯一分发渠道）。
- 空 token 且未显式非回环 listenHost 时，强制绑 127.0.0.1。
- relay 是 X25519→HKDF→AES-GCM，但**可被恶意中继扣握手帧降级为明文**；direct 默认明文 `ws://`。

## 4. 借用与判定

1. 任务在副机执行，还是主机远程调用？前者断链不中断，后者会。
2. hub 对 worker 有哪些能力（exec/read/write）？凭证/密钥是否也受这些能力影响？
3. 配对串含什么？有无过期/签名/指纹？TOFU 绑在哪？
4. 传输是否可降级？direct 是否明文？

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| worker 有 in-process / headless 两种后端 | `[SRC-TARGET]` | [`06 memo`](./_证据/06-remote-agent-源码复核.md)（0.9.11/cc356e1） | headless 不能指定模型 |
| hub 有 exec/read 能力，凭证不过协议 | `[SRC-TARGET]` | 同上（exec.js/node-registry.js） | exec 默认 manual 审批 |
| 配对串 7 字段、无过期/签名、含 hub 指纹 | `[SRC-TARGET]` | 同上（pairing.js） | 空 token 强制回环 |
| relay 可降级明文、direct 默认明文 | `[SRC-TARGET]` | 同上（e2e.js/SECURITY） | 未做真实中间人测试 |
| “凭证永不出机”是过度承诺 | `[OBS]` | 上述对照 | 取决于 hub 能力配置 |

**未验证**：headless NDJSON 契约、relay 降级触发条件、0.9.12 发布动机，均 `[OPEN]`。
