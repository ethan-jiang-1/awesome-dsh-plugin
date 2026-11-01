---
title: "13 · Noelune/dsh-agent-relay 源码复核"
domain: agent-crossing
kind: evidence
positioning: "对 dsh-agent-relay 固定提交的复核：v0.8.1 树内 wake/长轮询/幂等成立；npm 只到 0.5.0，按卡安装拿到的是无这两项且仍含 v1 的旧代。"
read_when: "核对 13 卡的 loopback 拓扑、wake_command、离线语义与「删掉一半」时读。"
status: observed
updated: 2026-11-01
---

# 13 · `Noelune/dsh-agent-relay` 源码复核

> 复核对象：样本卡 [`13-Noelune-dsh-agent-relay.md`](../samples/13-Noelune-dsh-agent-relay.md)（当前工作树版 79 行，`updated: 2026-10-31`）。按指令**未改卡、未改索引**。
> 取证时点 2026-11-01。只读 GitHub `codeload` 固定提交 tarball、`git ls-remote`、blobless `git clone`（只为取历史与 diffstat）、`registry.npmjs.org`（metadata + 0.5.0 tarball）、`api.npmjs.org` 下载量、shields.io 星数、本机 `@deepseek-ai/dsh 0.2.1-rc.3` 发行包的类型与编译产物；**未安装、未构建、未跑 `node --test`、未起 broker、未加载插件、未跑宿主**。
> 标签沿用 [`EVIDENCE.md`](../../EVIDENCE.md)：`[DOC]` 目标仓 README/docs/CHANGELOG 主张，`[SRC-TARGET]` 固定 commit 实现，`[SRC-DSH]` 本机 DSH 发行包，`[TEST]` 测试源码，`[CI]` 同 SHA check-run，`[RUN]` 本轮实跑，`[OBS]` 判断。
> **主 pin**：commit [`7e43c5452e035c6de7b5376fde131d08f5a0926d`](https://github.com/Noelune/dsh-agent-relay/commit/7e43c5452e035c6de7b5376fde131d08f5a0926d) = 附注 tag `v0.8.1` 解引用后的 commit（tag 对象 `7d45b4b`），committer 2026-09-19T15:38:03+08:00，树内 `package.json` 为 `0.8.1`。`main` HEAD 是 `07d0d5b`（2026-10-13），**比 pin 多 6 个 commit**。
> 一句话结论：**站在 `v0.8.1` 的源码上，卡片描述的机制几乎逐条成立，而且实现比卡片更细**（唤醒的两段闸、租约令牌、未送达通知的 60 s 独立扫描、幂等唯一索引都能指到行）；**最重的偏差不在源码而在坐标**——`0.6.0` 起的四个版本**从未发布到 npm**，`npm dist-tags.latest` 还是 `0.5.0`（2026-08-22）。而卡片把「版本 0.8.1」与「`dsh plugin add dsh-agent-relay`」写在同一条安装路径上：按卡安装拿到的是 **0.5.0，它既没有 `wake_command`，也没有长轮询**，并且**仍然包含 v1 半代**。于是卡片的两个招牌机制（唤醒兜底、落库即达）与「删掉自己的一半」在**可安装路径上都不成立**。

## Provenance

| 项 | 值 | 核对方式 |
|---|---|---|
| 仓库 | [`Noelune/dsh-agent-relay`](https://github.com/Noelune/dsh-agent-relay)，非 fork，MIT，默认分支 `main`，**81 个 commit**，首 commit `5016f69`（2026-08-15T00:15:31+08:00，`feat: initial release v0.1.0`），`main` HEAD `07d0d5b`（2026-10-13T13:39:41+08:00，`fix(v4): relay 消息改用生产者自有 source kind`） | `git ls-remote` + blobless clone |
| 星标 | **4★**（2026-11-01 经 shields.io JSON 取到；GitHub REST 当日 403 限流） | `img.shields.io/github/stars/…json` |
| **npm 包** | `dsh-agent-relay`，`dist-tags.latest = 0.5.0`；registry 共 **5 个版本**：`0.1.0`/`0.1.1`/`0.2.0`/`0.3.0`/`0.5.0`（创建 2026-08-14T16:36:22Z，最后修改 2026-08-22T03:25:20Z） | `registry.npmjs.org/dsh-agent-relay` |
| npm `gitHead` | `0.1.0 → 5016f69`、`0.1.1 → 7901404`、`0.2.0 → 4aca86d`、`0.3.0 → 4558c07`、**`0.5.0 → 6d17ff49c3a59f85437cb061a4353b43198536b2`**（该 SHA 在 git 历史里存在，但**没有对应 tag**） | registry metadata + `git cat-file -t` |
| **tag（全部 4 个）** | `v0.6.0`（tag 对象 `82222dd` → commit `3ddaa81`）、`v0.7.0`（`3ab1e27` → `95a83bc`）、`v0.8.0`（`4792541` → `8407bb0`）、`v0.8.1`（`7d45b4b` → `7e43c54`）；四个 tag 的 commit 日期**都是 2026-09-19**（+08:00） | `git ls-remote --tags` + `git log -1 <tag>` |
| **主 pin** | `7e43c54…`，`chore(release): 0.8.1 — client errors that name themselves, and a measured long-poll latency`，2026-09-19 15:38:03 +08:00；树内 `package.json` = `0.8.1`、`type: module`、`main: lib/index.js`、`license MIT`、**无 `dependencies`/`peerDependencies`/`engines`/`scripts`** | commit tarball 内 `package.json` |
| pin 之后 | `main` = pin + **6 个 commit**，含 `fc4a003 fix(broker): a failed wake now says why…`、`57d407d test(wake): stop asserting a settled claim…`、`07d0d5b fix(v4): relay 消息改用生产者自有 source kind` | `git log v0.8.1..main` |
| 提交 tarball | 131 条目 / **111 个文件**（含 `broker/`、`lib/`、`mcp/`、`setup/`、`adapters/`、`docs/`、`test/`、`.github/workflows/ci.yml`） | `tar tzf` |
| **npm 0.5.0 tarball** | **52 个文件**，`gitHead 6d17ff4`；含 `broker/src/auth.js`、`broker/src/store.js`、`lib/client.js`、`lib/sign.js`、`docs/PROTOCOL.md`、`adapters/hermes/relay_client.py`、**`broker/data/relay.db` + `relay.db-shm` + `relay.db-wal`（WAL 28,872 B）**、`__pycache__/*.pyc` | 下载 tarball + `tar tzf` |
| 下载量 | `last-month`（**2026-09-30 → 2026-10-29**）= **1,048**；`last-week`（10-23 → 10-29）= 246 | `api.npmjs.org/downloads/point/…` |
| GitHub Release / topics / created_at | **未取**（REST 403 限流，`/releases` 未查） → `[OPEN]` | — |
| 版本序列 | `CHANGELOG.md` 有 10 节（0.1.0 → 0.8.1），npm 只有 5 个包；**0.4.0 与 0.6.0/0.7.0/0.8.0/0.8.1 共 5 个版本从未发布** | registry `versions` 对照 CHANGELOG 小节 |

**坐标对齐与错位**

1. **tag ↔ commit ↔ 树内版本三处对齐**：`v0.8.1^{}` = `7e43c54`，`git show v0.8.1:package.json` 的 `version` = `0.8.1`。所以「0.8.1」作为**源码坐标**是干净、可复现的；本 memo 全部 `[SRC-TARGET]` 行号都指向这个 commit。
2. **npm 与 git 脱节，这是本卡最重的问题**：`0.5.0` 发布于 2026-08-22，而 `0.6.0`（唤醒 + 长轮询 + presence）、`0.7.0`（删 v1）、`0.8.0`（SQLite 单一真相）、`0.8.1`（客户端错误码）全部发生在 **2026-09-19 一天之内**，一个都没上 npm。`CHANGELOG.md` 0.6.0 把唤醒/长轮询/presence 列为新增，正好证明它们**晚于** npm 上的最后一版。
3. **「按卡安装」装到的是旧代**。卡 L47 的安装命令 `dsh plugin --profile web add dsh-agent-relay` 与本仓 README 第 166 行一致，但它解析到 `0.5.0`。我按文件核对过 0.5.0 的 broker 源码（`broker/src/config.js` + `broker/src/server.js`）：`grep wake_command|wakeCommand|spawnWorker` 零命中、`grep wait_seconds|waitFor` 零命中，而 `lease_token` 与 `idempotency_key` 已存在。也就是说 **0.5.0 = 有租约/幂等、无唤醒/长轮询**，并且 v1 的 `auth.js`/`store.js`/`client.js`/`sign.js`/`PROTOCOL.md` 都还在包里。
4. **`main` 不是这个卡的对象**。pin 之后有 6 个 commit，其中一个改的是插件收到的消息 `source` 形状（`fix(v4)`）。任何「照着 GitHub 首页读」的复核会读到与 tag 不同的实现；本 memo 一律取 tag。
5. **没有发布 workflow**：唯一 workflow 是 `.github/workflows/ci.yml`（4 个 job，见 §CI），不含 publish。这**解释**了 npm 断代，但不证明作者的意图（`[OPEN]`：为何 0.6.0 之后一直不发布，仓库里没有记录）。

## DOC

`[DOC]` 只证明作者声称什么，不证明实现如此。

- **只绑回环自述**：「Broker 默认仅绑定本地回环地址 `127.0.0.1:19121`」——[README.md:34](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/README.md#L34-L34)；部署流程「启动 Broker 进程并绑定 `127.0.0.1:19121` 端口」——[README.md:171](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/README.md#L171-L171)；模板注释「loopback only — the broker is not a network service」——[config.example.yaml:6](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/config.example.yaml#L6-L6)。
- **鉴权自述**：HMAC-SHA256、300 秒重放窗口、常量时间比较、租约令牌；并且**主动写明**「速率限制与鉴权失败锁定属于已删除的 v1 世代，现在没有这两道闸，所以边界由『只绑回环』承担」——[README.md:35-36](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/README.md#L35-L36)。SECURITY.md 把「不存在的控制」单列一节，避免把配置键误当控制——[SECURITY.md:23-28](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/docs/SECURITY.md#L23-L28)。
- **投递自述**：7 天留存、SQLite 单一路径、租约 + 令牌化确认、服务端长轮询（落库即达）、失败/过期由服务端定时扫描回发未送达通知、幂等键去重——[README.md:37-38](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/README.md#L37-L38)；协议文档给了传输层事实（HTTP/1.1、默认 `127.0.0.1:19121`、1 MiB 请求体、body/context 各 48 000 码点、broker 不记消息内容、v1 形状的请求回 400）——[PROTOCOL-V2.md:1-31](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/docs/PROTOCOL-V2.md#L1-L31)。
- **异构接入自述**：「MCP（Codex / Claude Code / Qoder / 任意 MCP 宿主）」+ 工具表——[README.md:101-113](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/README.md#L101-L113)；同一 README 第 104 行写「工具面只有 5 个」，第 215 行写「6 个工具」，表里实际 6 行——**`[DOC]` 内部自相矛盾**（见 §2）。
- **`wake_command` 自述**：「消息落库时若它 90 秒内没取过件，broker 会按需启动一次工作进程（凭据走子进程环境变量，不进命令行）；它真的会跑一次该成员的 CLI 并产生 API 费用，所以开关单独成一条命令，默认只预演」——[README.md:134-147](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/README.md#L134-L147)；SECURITY.md 单列「`wake_command` 是最锋利的一边」，写明「命令模板来自配置、不来自请求」——[SECURITY.md:87-96](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/docs/SECURITY.md#L87-L96)。
- **doctor 自述**：README 列七类输出（可达性、谁真能收、积压、两处凭据漂移、明文密钥、WAL 膨胀、线上 adapter 与基线）与退出码 0/2/1——[README.md:149-156](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/README.md#L149-L156)。实现里的检查名是 **10 个**（`broker`/`members`/`queues`/`history`/`config`/`on-demand`/`secrets`/`plaintext`/`storage`/`adapter`），比 README 多出「失败/过期计数」「wake 可用性」「配置存在性」三类（[doctor.mjs:88-190](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/setup/doctor.mjs#L88-L190)）。
- **协议单一来源自述**：「签名串的字节级定义只在 docs/PROTOCOL-V2.md 维护，此处不再复制一份等着漂移」+ 两个跨语言 golden 测试——[README.md:202-205](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/README.md#L202-L205)。
- **v1 删除自述**：「v1 世代（`X-Relay-*` 头、`/register`、`/messages` 游标轮询）已于 2026-09-19 移除——审计显示 v1 队列表自 2026-08-15 起再无任何消息，且没有任何现役客户端注册过」——[README.md:196-197](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/README.md#L196-L197)；CHANGELOG 0.7.0 给出同口径的审计数字与删除清单——[CHANGELOG.md:124-162](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/CHANGELOG.md#L124-L162)；0.8.0 又补了「四个什么都没做的配置键被删掉」——[CHANGELOG.md:32-123](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/CHANGELOG.md#L32-L123)。
- **兼容性自述**：「Node ≥ 22.13（`node:sqlite`）」「dsh 0.1.0-rc.6（推荐测试版本）」——[README.md:227-229](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/README.md#L227-L229)；ARCHITECTURE 复述「Tested against dsh 0.1.0-rc.6」——[ARCHITECTURE.md:104-114](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/docs/ARCHITECTURE.md#L104-L114)。本机宿主是 `0.2.1-rc.3`——比自述版本高**一个 minor**（0.1 → 0.2），且 rc 号并不连续（rc.6 → rc.3），是否仍兼容未测（`[OPEN]`）。
- **文档内的矛盾（目标仓自身）**：`adapters/openclaw/README.md` 仍在教 v1 API（`client.register()`、`client.send()`、`relay.mjs send/recv`，并 import 已删除的 `relay_client.py`）——[openclaw/README.md:5-25](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/adapters/openclaw/README.md#L5-L25)。CHANGELOG 0.8.0 声称「文档合并、删掉假的部分」，这个文件漏了。

## SRC-TARGET

以下行号全部 pin 到 commit `7e43c54`。先给裁决表，再逐条展开。

### 0. 主张裁决（先看这张表）

| # | 核对项 | 裁决 | 关键依据 |
|---|---|---|---|
| 1 | loopback broker 拓扑 | **默认成立，「只绑」过强**：默认 `127.0.0.1:19121`，但 `broker.host` 接受任意字符串，**broker 侧没有任何 loopback 校验** | [config.js:73-74](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/config.js#L73-L74) |
| 2 | 单 broker 星形，非 P2P | **成立**：所有客户端只与 broker 说话；无发现、无联邦、无 leader、无 WS，纯 HTTP + 长轮询 | [server.js:227-291](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L227-L291) |
| 3 | 异构运行时桥接 | **成立，但方向要说准**：跨的是**宿主/客户端**（dsh 插件、MCP、CLI、Python、codex/claude CLI 包装），**线上只有一种协议**（v2/v3 HMAC JSON），broker 不做协议翻译 | §2 |
| 4 | `wake_command` 触发条件 | **成立但需精确化**：是**两段闸**——先看有没有挂起的长轮询（有就立即结算，不起进程），再看 90 s presence；卡只写了后半段 | [server.js:191-200](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L191-L200) |
| 5 | `wake_command` 安全面 | **成立且比卡更狠**：`shell: true`、继承全量 `process.env`、注入 `AGENT_RELAY_SECRET`；无 per-agent 密钥时**给的是共享密钥** | [server.js:144-157](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L144-L157) |
| 6 | 对端离线时会发生什么 | **成立**：发送仍然成功入库（7 天），回包带 `target_online`/`last_seen_at`/`will_wake`/`hint`；同步 `ask` 在「不在线且唤不醒」时立刻返回 `peer_offline` | [v2-routes.js:120-147](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/v2-routes.js#L120-L147)、[client-v2.js:194-206](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/client-v2.js#L194-L206) |
| 7 | 幂等 | **成立**：`idempotency_key` **必填**，`UNIQUE(origin, idempotency_key)`，重复投递回原 `message_id` + `created:false`；去重窗口 = 30 天保留期 | [v2-routes.js:62-63](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/v2-routes.js#L62-L63)、[store-v2.js:79](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L79-L79) |
| 8 | 队列/租约/失败收敛 | **成立**：状态机 queued→leased→completed/failed/expired，令牌化 ack、重投计次、到期归还、过期/失败→一次未送达通知 | §5 |
| 9 | 删掉自己的一半 | **在 `v0.8.1` 树内成立**：`eb5e16d` 51 文件 +521/−4399；**在发布物里不成立**（npm 0.5.0 仍含 v1） | §6 |
| 10 | 状态归属/重启 | **成立**：消息状态只在 SQLite；presence/waiters/在飞唤醒只在内存，重启变保守；插件托管 broker，随 dsh 起停 | §7 |
| 11 | 5 个模型工具 | **成立**：`agent_relay_send/status/history/peers/retry` | [relay-tools.js:99-136](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/relay-tools.js#L99-L136) |
| 12 | doctor 退出码 0/2/1 | **成立**：`fail→1 / warn→2 / ok→0` | [doctor.mjs:220](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/setup/doctor.mjs#L220-L220) |

### 1. 拓扑：一个环回 HTTP broker，`只绑`是默认而不是保证

broker 是 `node:http` 起的单进程（[server.js:8-19](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L8-L19)、[index.js:40-43](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/index.js#L40-L43)），拓扑是**单点星形**：

```
dsh plugin ─┐
MCP 宿主   ─┤   HTTP + HMAC（v2/v3）      ┌─ 长轮询挂起（≤120 s）
CLI/脚本   ─┼──────────────────────────▶ broker（127.0.0.1:19121 默认）
Python     ─┤   /v1/messages /v1/pull     ├─ wake_command 起短命 worker
codex/claude┘   /v1/ack /v1/status …      └─ SQLite relay-v2.db（唯一真相）
```

- **只有一种传输**：HTTP 请求/响应 + 可选的 hold 住的 pull。**没有 WebSocket**、没有 broker 间联邦、没有成员发现、没有注册步骤（[server.js:236-239](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L236-L239) 注释直说「membership 来自 config」，v1 的 `/register` 心跳「从未被 v2/v3 客户端调用过」）。
- **唯一免鉴权路由是 `GET /healthz`**（[server.js:234-269](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L234-L269)），它回 `agents` 名单、每成员队列计数、`last_pull_at`、版本与 held pulls。默认环回时这是本机信息；一旦把 `host` 改到非环回，它就是**未鉴权的成员与积压枚举面**。SECURITY.md 承认「无加密、`broker.tls` 直接报错」，但把「改 host」说成「本指南不推荐的操作」（[SECURITY.md:60-64](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/docs/SECURITY.md#L60-L64)）——**这是文档约束，不是代码约束**。
- **代码里的 loopback 校验只有一处，而且在插件侧**：`/api/dsh-agent-relay/status` 会检查 `req.socket.remoteAddress` 是否 `127.0.0.1`/`::1`/`::ffff:127.0.0.1`，否则 403（[lib/index.js:259-283](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/index.js#L259-L283)）。broker 侧对应的校验**不存在**：`host: String(b.host ?? '127.0.0.1')` 之后只校验了端口号（[config.js:73-94](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/config.js#L73-L94)）。
- **一处有意义的对照**：本机 DSH 自己的 webserver 会在加载期**拒绝** unspecified 地址（`dsh-host-webserver` 的 `Config.host` 注释与 `isWildcardHost`，见 SRC-DSH §5）；relay broker 没有这层。两边口径相反，卡片「只绑回环」因此应读作「默认 + 部署纪律」，而不是「实现保证」。

### 2. 异构桥接：跨的是运行时，不是协议

卡片说「跨异构 agent 运行时」，字面成立，但**机制是「把通信降级到一种最小协议」，不是「做协议适配层」**。清单如下：

| 运行时/入口 | 桥接方式 | 依据 |
|---|---|---|
| dsh | Cordis 插件，注册 5 个模型工具 + 系统提示 section + 侧栏状态路由；签名走 **v2**（不带 keyId） | [lib/index.js:37-38](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/index.js#L37-L38)、[ARCHITECTURE.md:111-114](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/docs/ARCHITECTURE.md#L111-L114) |
| Codex | MCP stdio（`mcp/relay-mcp.mjs`，6 个工具）+ 可选 `codex-backend.mjs`（`codex exec --json`，按 JSONL 事件流解析） | [codex-backend.mjs:1-12](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/adapters/backends/codex-backend.mjs#L1-L12)、[codex-backend.mjs:22-40](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/adapters/backends/codex-backend.mjs#L22-L40) |
| Claude Code | 同一个 MCP 入口 + `claude-backend.mjs`（`--output-format stream-json --permission-mode plan`） | [claude-backend.mjs:1-25](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/adapters/backends/claude-backend.mjs#L1-L25) |
| 任意 MCP 宿主（Qoder 等） | 同上，3 行配置 | [README.md:101-113](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/README.md#L101-L113) |
| Python（Hermes） | 纯标准库客户端 `relay_client_v2.py`，可走 v3（带 `X-Agent-Relay-Key-Id`） | [relay_client_v2.py:1-27](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/adapters/hermes/relay_client_v2.py#L1-L27) |
| 脚本/cron | `adapters/cli/relay.mjs`，`v2 ask/send/pull/reply/ack/status/…` | [relay.mjs:142-246](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/adapters/cli/relay.mjs#L142-L246) |
| OpenClaw | 只有一份说明文档，**仍是 v1 API，已过时** | [openclaw/README.md:5-25](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/adapters/openclaw/README.md#L5-L25) |

四点值得记：

1. **「对等」是逻辑的，物理是星形**。成员之间不直连；`peer` 只是「同一个 broker 上的另一个 agent 名」。卡片的「对等链路」在语义上没错（broker 不编排、不改写、不驱动控制流），但不要读成 P2P 组网。
2. **MCP 工具是 6 个不是 5 个**：`relay_ask/send/inbox/reply/status/agents`（`relay_reply` 是 0.8.1 才加的「回答动词」）。README 第 104 行说 5、第 215 行说 6，CHANGELOG 0.6.0 也说 5——**`[DOC]` 内部漂移**，代码是 6。
3. **DSH 工具面拿不到「对方的在线状态」**：`agent_relay_send` 走 `client.sendRequest()`，只返回 `message_id`，把 `target_online`/`will_wake`/`hint` 全丢了（[relay-tools.js:40-48](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/relay-tools.js#L40-L48) vs [client-v2.js:79-99](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/client-v2.js#L79-L99)）。所以「离线即刻知情」只在 MCP/CLI 的 `ask` 上成立；在 dsh 里面模型要么等 `agent_relay_status`，要么等未送达通知被投回会话。
4. **「不碰文件」只对 DSH 插件路径成立**：独立 worker（也就是 `wake_command` 默认跑的那个）对 **write 模式**有真隔离——能建干净 git worktree 就建，不能就退到「按工作区路径的一把文件锁」（PID 活性恢复、15 min 过期），防止 Codex 与 Claude 同时写一个目录（[workspace.js:1-9](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/workspace.js#L1-L9)、[lease.js:1-19](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/lease.js#L1-L19)）。这些代码**只被 `adapters/relay-agent.mjs` 引用**，DSH 插件不 import 它们（`lib/` 内 `grep prepareRelayWorkspace|WorkspaceLease` 零命中，只有 `relay-plugin-core.js` 的提示文案提到 workspace）。所以「不提供文件裁决」在插件侧成立，在 worker 侧是**有一个最小写闸**的。

### 3. `wake_command`：两段闸、一把可能过粗的钥匙、一条不回收的子进程

**触发条件（精确版）**，`wakeAgent(agent, info)`（[server.js:191-200](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L191-L200)）：

1. 若该 agent 有**挂起的长轮询**（`waiters`），立即结算这些请求并返回 `false`——**不起进程**；
2. 否则看 `storeV2.lastPullAt[agent]`：≤ 90 s（`PRESENCE_STALE_SECONDS`）→ 返回 `false`；
3. 否则 `spawnWorker()`：每个 agent **同一时刻最多一个在飞**（`waking` Set），成功启动则回包 `will_wake: true`。

所以卡片 L30「若它 90 秒内没取过件，broker 会按需启动一次」是**必要非充分**：还要求此刻没有人挂着 pull。两条闸合起来才是「兜底而非竞争」（[server.js:179-190](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L179-L190) 的注释把动机写得很清楚：0.6 之前的判据是「此刻有没有挂起的 pull」，而老式定时轮询客户端几乎不挂 pull，会导致**重复处理**）。

**它到底怎么跑**（[server.js:131-177](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L131-L177)）：

```js
const command = fillWakeTemplate(template, { ...info, agent: agentName }) // 只替换 {message_id}/{root_id}/{agent}
spawn(command, {
  shell: true,                 // 走 shell
  stdio: 'ignore',
  env: { ...process.env, AGENT_RELAY_AGENT: agentName,
         AGENT_RELAY_BROKER_URL: brokerUrl,
         AGENT_RELAY_SECRET: entry?.secret || config.secret },
})
child.unref()
setTimeout(() => waking.delete(agentName), 15 * 60 * 1000) // 防丢 exit 事件卡死
```

安全与行为上的六个事实：

1. **命令来自配置，不来自请求**——模板变量只有 broker 生成的 32 hex id 与 agent 名（[server.js:124-129](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L124-L129)），而 agent 名必须先命中 `config.agents[agentName]` 才会 spawn。**线上不可注入**。
2. **但配置一旦可写 = 代码执行**。`shell: true` 意味着 `wake_command` 是任意 shell 行，以 broker 用户身份运行；`wake_command` 长度上限 2000 字符，除此之外**没有任何白名单/前缀校验**（[config.js:163-171](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/config.js#L163-L171)）。SECURITY.md 自己把文件权限称作「the authorization check」（[SECURITY.md:89-96](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/docs/SECURITY.md#L89-L96)）。
3. **凭证只进环境，不进 argv**——这点卡与文档都说了，成立；但**给哪把钥匙取决于配置**：`entry.secret || config.secret`。在默认的共享密钥模式下，**被唤醒的 codex worker 拿到的是全圈共享密钥**，即可以以任何 agent 名签名。这不是 bug，但卡片「凭据走子进程环境变量」的乐观读法应当补一句「默认就是共享密钥」。
4. **继承全量父环境**（`...process.env`）：broker 自己的环境（包括任何 `DSH_*`、代理设置、云厂商密钥）都会进到被唤醒的 CLI 里。文档没提这一层。
5. **不回收**：`stdio: 'ignore'` + `unref()`，broker 的 `shutdown()` 只清定时器、释放长轮询、关库、关连接（[broker/src/index.js:69-77](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/index.js#L69-L77)），**不杀已 spawn 的 worker**。所以 broker 重启后 `waking` 归零，而旧 worker 可能还在跑 → 新 broker 会再起一个，两个 worker 同时在线抢队列（同一条消息仍由租约保证只被一个认领，但 **CLI 计费会翻倍**）。`[OPEN]`：未实跑验证残留时长。
6. **它对三类事件都会被调用**：新消息（`v2-routes.js:121`）、未送达通知（`server.js:75`）、`admin/requeue`（`v2-routes.js:362`）。所以「唤醒」不只是投递路径，也是**失败通知的投递路径**——这点卡片没写，但正是「发送方在收件人全死时也能收到坏消息」的关键。

**默认只预演**成立：`enable-wake.mjs` 的 `apply` 默认 `false`，只打印将写入的行，`--apply` 才写且先备份（[enable-wake.mjs:1-17](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/setup/enable-wake.mjs#L1-L17)、[enable-wake.mjs:29-44](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/setup/enable-wake.mjs#L29-L44)）。它生成的命令是 `relay-agent.mjs --once --max-tasks 4 --backend-cmd "<node> …/codex-backend.mjs" --cwd <home>`（[enable-wake.mjs:39-44](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/setup/enable-wake.mjs#L39-L44)），而 `relay-agent.mjs` 的定位就是「认领→交给 `--backend-cmd`→ack→队列空即退」的短命工作进程（[relay-agent.mjs:1-19](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/adapters/relay-agent.mjs#L1-L19)、[relay-agent.mjs:80-96](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/adapters/relay-agent.mjs#L80-L96)）。**真会跑一次成员的 CLI 并计费**，卡片的警告成立。

### 4. 对端离线：消息不丢，回执与通知分三层

- **发送永远先落库**：`POST /v1/messages` 先把行写进 SQLite 再回包（[v2-routes.js:104-132](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/v2-routes.js#L104-L132)），TTL 默认 7 天、`ttl_seconds` 夹在 60 s–30 天（[protocol.js:32-34](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/protocol.js#L32-L34)、[v2-routes.js:66-68](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/v2-routes.js#L66-L68)）。
- **回包里带三件真相**：`target_online`（90 s 内取过件）、`last_seen_at`、`will_wake`；当「不在线且是新消息」时再附一句人话 `hint`（唤醒了说「已按需唤醒」，没唤醒说「已留存 N 小时」）——[v2-routes.js:130-147](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/v2-routes.js#L130-L147)。注释解释了为什么把它做成**加性字段**而不是失败：2026-09-19 审计里 6 个成员有 4 个从重启起就没取过件，「没人听」是常态不是异常。
- **同步 `ask` 的短路**：`target_online=false` 且 `will_wake=false` 且没传 `waitOffline` → 立刻 `reason: 'peer_offline'`，不烧满 deadline；请求仍留存（[client-v2.js:194-206](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/client-v2.js#L194-L206)）。
- **失败通知**：`notifyFailedSenders()` 扫 `kind='request' AND status IN ('failed','expired') AND notified_at IS NULL`，每个请求**最多一次**（`markNotified` 以 `notified_at` 为准），通知本身是一条 `reply` 消息、TTL ≥ 7 天、并且**也会尝试唤醒发送方**（[server.js:46-77](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L46-L77)）。它由 broker 自己的 **60 s 定时扫描**驱动，不依赖任何客户端来取（[broker/src/index.js:50-65](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/index.js#L50-L65)）——这是卡片「失败/过期由服务端定时扫描自动回发」的准确机制。
- **DSH 侧收到通知会怎样**：它是一条 `kind='reply'`、`parent_id` 指向原请求的消息；`handleReply` 靠 `routes` 表找回原会话并 `agent.steer()`，**找不到就 ack 掉并丢弃**（[message-handlers.js:48-70](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/message-handlers.js#L48-L70)）。`routes` 是 `~/.dsh-agent-relay-routes-<hash>.json`、TTL 7 天（[lib/index.js:40-50](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/index.js#L40-L50)）。所以「发送方一定能看到坏消息」在 **broker 层**成立，在 **DSH 会话层**是 best-effort：原会话被回收/重启后，这条通知会被安静地 ack 掉。

### 5. 投递语义：租约 + 令牌 + 幂等，边界比卡片写的更清楚

**状态机**（[store-v2.js:1-19](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L1-L19)）：

```
queued ──pull──▶ leased ──ack completed──▶ completed
  ▲                 │
  └──ack retry──────┘（attempts+1，>= maxAttempts(3) → failed）
queued/leased ──expires_at 到──▶ expired
leased ──lease_until 到──▶ queued（reclaim）
failed/expired ──admin requeue──▶ queued（attempts 归零）
completed/expired/failed ──30 天后──▶ 删除（连带幂等键）
```

- **认领是单语句原子操作**：`UPDATE … SET status='leased', attempts=attempts+1, lease_until=?, lease_token=? WHERE message_id=(SELECT … LIMIT 1) RETURNING …`（[store-v2.js:125-133](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L125-L133)），索引 `(target, status, created_at)` 让领取顺序=投递顺序（[store-v2.js:50-55](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L50-L55)）。`lease_token` 是 32 字节随机 base64url（[store-v2.js:309](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L309-L309)）。
- **ack 有两条路径**：带 `lease_token` 走严格路径（必须 `leased` + token 相同 + 租约未过期，否则 409 `lease_mismatch`）；不带 token 走 v2 兼容路径，**只要求状态是 `leased`**（[store-v2.js:317-355](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L317-L355)）。精确说法：**租约到期是由 sweep 的 reclaim 生效的，不是由 ack 路径生效的**——在「已过期但还没扫到」的窗口里，不带 token 的迟到 ack 仍会被接受。带 token 的客户端不受影响。
- **重投**：`retry` 把状态放回 `queued`、清租约，`attempts` 已在认领时 +1；`attempts >= 3` 时直接 `failed`（[store-v2.js:344-354](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L344-L354)）。
- **幂等**：`idempotency_key` 缺失直接 400（[v2-routes.js:62-63](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/v2-routes.js#L62-L63)）；重复键回原 `message_id` 且 `created:false`（[store-v2.js:272-290](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L272-L290)）。**去重窗口不是永久**：终态行 30 天后被 `purge` 连同唯一索引条目一起删掉（[store-v2.js:43-44](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L43-L44)、[store-v2.js:146-148](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L146-L148)）。客户端的键：DSH send 用 `agent:epoch:random`（每次新键，**重试靠服务端 requeue 而不是重发**，[relay-tools.js:40-44](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/relay-tools.js#L40-L44)）；reply 用 `reply:<parent_id>`（**确定性**，重放同一父请求只会产生一条回复，[message-handlers.js:24-38](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/message-handlers.js#L24-L38)）。
- **长轮询**：`wait_seconds` 夹到 ≤120 s（[protocol.js:39](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/protocol.js#L39-L39)、[v2-routes.js:181-189](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/v2-routes.js#L181-L189)）；每个 agent 最多 16 个挂起请求，超了立即返回空（[server.js:85](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L85-L85)、[server.js:208-225](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L208-L225)）；客户端断开时用 `res.once('close')` 结算，避免泄漏（[server.js:223](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L223-L223)）——这就是「落库即达」的实现，CHANGELOG 自述实测 ~30 ms。
- **presence 是「问过」不是「收到」**：`pull()` 一进来就 `lastPullAt.set(target, now)`，**空拉也算在线**（[store-v2.js:296-298](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L296-L298)）。所以「90 s 内取过件」严格说是「90 s 内发过 pull」，一个只会空转的轮询器也能挡住唤醒。
- **两处 online 口径不一致**：broker `/healthz` 与 wake 闸用 **90 s**；插件 `agent_relay_peers` 硬编码 **15 s**（[relay-tools.js:74-80](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/relay-tools.js#L74-L80)）。同一个词在两个面上含义不同，卡片没写。

### 6. 「删掉自己的一半」：实测 `eb5e16d`

`[SRC-TARGET]` 历史证据（blobless clone）：

- commit [`eb5e16d`](https://github.com/Noelune/dsh-agent-relay/commit/eb5e16d4caae86e6b74d4ae90059ca3badd5d2e9) `refactor!: remove the v1 generation and every duplicated code path`，2026-09-19 11:21:13 +08:00。
- **51 个文件，+521 / −4399**。删除的整文件包括：`broker/src/store.js`（415）、`broker/src/auth.js`（129）、`lib/client.js`（154）、`lib/sign.js`（32）、`docs/PROTOCOL.md`（257）、`adapters/hermes/relay_client.py`（220）、`adapters/hermes/deployed-adapter.py`（1476）、`adapters/hermes/example_hermes_plugin.py`（86），以及 **6 个**只覆盖 v1 的测试文件（`acl`/`e2e`/`lease`/`python-client`/`sign`/`store`，共 750 行）。`server.js` 有 293 行增删（inline v1 路由被摘掉，同时补 v2 侧改动）。
- 注意：`lib/relay-tools.js`、`lib/broker-lifecycle.js`、`lib/inbox-worker.js` 这批拆分**不在这个 commit 里**——它们各自的文件头写着 2026-08-29 的稳定化拆分，早于 v1 删除。所以「−4399」几乎全是净删除，不是搬迁。

**判断：卡片 L34「它删掉了自己的一半」成立，而且是可核对的数量级**：净删 3878 行，删掉的是**整代**（store、auth、client、sign、协议文档、Python 客户端、6 个测试文件），commit 带 `!`，是 breaking 删除而不是重构。「一半」是否精确取决于按行数还是按模块数数，两种数法都指向同一结论。三个配套动作也成立：

1. **协议文档只留一处**：`docs/PROTOCOL.md` 删除，规范只维护 `docs/PROTOCOL-V2.md`；代码层面 `broker/src/protocol.js` 变成 `lib/protocol.js` 的 re-export（[broker/src/protocol.js:1-9](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/protocol.js#L1-L9)）。这是「不复制一份等着漂移」的字面实现。
2. **跨语言 golden 测试是真的**：`test/protocol_v2_golden.py` 有硬编码向量表；`test/protocol-v2-python.test.mjs` spawn 真 Python 跑它，跑不过就红（`assert.ok(python, 'Python 3.10+ is required…')` 意味着**没有 Python 时是失败而不是跳过**，[protocol-v2-python.test.mjs:18-31](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/test/protocol-v2-python.test.mjs#L18-L31)）。
3. **v1 配置键不炸老部署**：`broker.rateLimit*`/`security.lock*` 被 ignore 而不是报错，注释与 SECURITY 同步（[config.js:98-104](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/config.js#L98-L104)）。

**但「删干净」有三处残留，且都在可安装路径上被放大：**

| 残留 | 位置 | 性质 |
|---|---|---|
| 注释仍指向已删除的文件 | `broker/src/v2-auth.js` 头注释「The stateful v1.1 authenticator with rate limiting lives in auth.js」——`auth.js` 已不存在 | 死引用（[v2-auth.js:1-4](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/v2-auth.js#L1-L4)） |
| OpenClaw 文档仍教 v1 | `adapters/openclaw/README.md` 的 `client.register()` / `client.send()` / `relay.mjs send/recv` 全部是已删 API | 文档过期（[openclaw/README.md:5-25](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/adapters/openclaw/README.md#L5-L25)） |
| **npm 0.5.0 仍含整代 v1** | `broker/src/auth.js`、`broker/src/store.js`、`lib/client.js`、`lib/sign.js`、`docs/PROTOCOL.md`、`adapters/hermes/relay_client.py` 都在 52 个文件里；还多带了 `broker/data/relay.db{,-shm,-wal}`（WAL 28,872 B）与 `__pycache__` | **发布物与仓库脱节**（见 Provenance §2-3） |

最后一条是这张卡最需要补的一句：**「删掉自己的一半」发生在 git 里，没有发生在 npm 上**。任何按卡片安装的人拿到的是删除前的半代 + 一份随包 SQLite 队列文件。`[OPEN]`：那份 WAL 里有没有历史消息体，本轮按要求没有解包读取（只确认了文件非空）。

另外，CHANGELOG 0.8.0 说删了「the five test files」，diffstat 是 **6 个**——作者自己的删除记账少算了一个（不影响结论，但说明「删掉一半」的叙述本身也有人工漂移）。

### 7. 状态归属与重启

**归属**：

- **消息状态只在 broker 的 SQLite**：`relay-v2.db`，WAL 模式，`persist:false` 时退化为 `:memory:` 而**不是**第二条代码路径（[store-v2.js:83-114](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L83-L114)）。注释直说「进程保留的 per-message 内存为零」——0.8 之前是「内存 Map 为准 + SQLite 镜像」，0.8 改成单语句原子认领（[store-v2.js:9-18](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L9-L18)）。
- **三样东西只在内存**，且都是「指标/调度」不是「消息真相」：`lastPullAt`（presence）、`waiters`（挂起的长轮询）、`waking`（在飞唤醒）。重启后 presence 归零、挂起请求消失、在飞标记消失。
- **客户端侧**有两份 JSON：`~/.dsh-agent-relay-receipts-<hash>.json`（1 天 TTL，用于重放已完成的回复）与 `~/.dsh-agent-relay-routes-<hash>.json`（7 天 TTL，message_id→DSH session 的映射）。它们让「重复投递」可重放、让「回复」能找到原会话；**丢了不致命，但回复会被丢弃**（§4）。

**重启行为（按代码路径推演）**：

| 事件 | 结果 | 依据 |
|---|---|---|
| broker 正常退出（SIGINT/SIGTERM） | 释放所有挂起长轮询 → 客户端收到空响应后按退避重试；`store.close()` 做 `wal_checkpoint(TRUNCATE)`；`closeAllConnections()` | [broker/src/index.js:69-77](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/index.js#L69-L77)、[store-v2.js:454-463](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L454-L463) |
| broker 被 kill -9 | 未确认的消息在 `lease_until`（默认 600 s）后被 reclaim 回 `queued`；到期的转 `expired`；终态行 30 天后清理 | [store-v2.js:134-145](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L134-L145)、[store-v2.js:261-266](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L261-L266) |
| broker 重启 | 构造 store 时先跑一次 `cleanup()`（过期/回收/耗尽/清理四类语句）；**presence 归零会让唤醒更积极**（注释称之为「保守」：宁可多唤一次也不假设有人轮询） | [store-v2.js:465-472](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L465-L472) |
| dsh 重启 | 插件 `dispose` 里 `worker.stop()` + `broker.dispose()`；下一轮 `ensureBroker()` 先探活，不可达就 spawn 打包内的 broker（`manageBroker` 默认 true），最多等 15 s | [lib/index.js:222-232](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/index.js#L222-L232)、[broker-lifecycle.js:49-78](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/broker-lifecycle.js#L49-L78) |
| 插件挂起→唤醒失败 | inbox worker 指数退避 2 s → 30 s，日志限流（首败/每档变/每 20 次一条） | [inbox-worker.js:50-63](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/inbox-worker.js#L50-L63) |

**由此得到的真话**：卡片 L59「真相源在 broker，不在任何 agent 侧；broker 挂了链路就断」成立，但要补两点。(a) **托管模式下 broker 是 dsh 的子进程**，dsh 一退 broker 就退——「插件托管 broker」既是便利也是单点：`manageBroker` 一旦为 true，dsh 崩溃会连带把全圈的 broker 带走（消息不丢，链路断）。(b) 重启会让 **presence 归零**，于是所有「离线」成员在下一条消息时都可能触发一次 `wake_command`——如果配置了唤醒，一次 broker 重启可能带来一波真实的 CLI 计费调用。卡片没有这条运维提示。

## SRC-DSH

本机 `@deepseek-ai/dsh 0.2.1-rc.3`（`/Users/bowhead/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh`，依赖树在 `node_modules/@deepseek-ai/*`）。只读类型与编译产物，未运行宿主。目标仓自述只在 **dsh 0.1.0-rc.6** 上验证过（[README.md:229](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/README.md#L229-L229)），本机比它高**一个 minor**（0.1 → 0.2，rc 号不连续），所以下面只核「插件用到的 seam 在这个版本还在不在、形状对不对」，不核运行。

**1. 五个注入点在 0.2.1-rc.3 都存在，名字对得上**。`inject = ['tools','agents','systemPrompt','timer','webServer']`（[lib/index.js:38](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/index.js#L38-L38)）：

- `tools: ToolRuntime`（`dsh-tools/lib/types/index.d.ts:34`），`register(definition: ToolDefinition): () => void`（同文件 `:637`）——插件把返回值当 disposer 收进 `disposers`，形状正确。
- `systemPrompt: SystemPrompt`（`dsh-system-prompt/lib/types/index.d.ts:12`），`section(section: PromptSection): () => void`（`:250`）；`PromptSection` 的 `{name, order, text}` 与插件 `{name:'agent-relay-circle', order:150, text}` 逐字段对得上（`:47-60`）。
- `webServer: WebServer`（`dsh-host-webserver/lib/types/index.d.ts:18`），`register(route: WebRoute): () => void`（`:174`），`WebRoute{kind:'exact'|'prefix', path, handler}`（`:33-40`）——插件的 `{kind:'exact', path:'/api/dsh-agent-relay/status', handler}` 合法。
- `agents`/`timer` 是 core 服务（插件只用了 `ctx.agents.get(id)` 与自建 `setTimeout`；注意它在 inbox worker 里**故意不用 `ctx.timeout`**，注释说不信 effect 注册的递归链，[inbox-worker.js:78-80](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/inbox-worker.js#L78-L80)）。

**2. 凭据 seam 形状正确**。`ctx.credentials: CredentialProvider`（`dsh-credentials/lib/types/index.d.ts:99-100`），`resolve(ref: CredentialRef): Promise<ResolvedCredential | undefined>`（`:130`），`ResolvedCredential.value: string`（`:73`）。`CredentialRef` 是 **branded string**（`credentialRef(value)`，同包 `:18`），运行时就是字符串，所以插件直接把 `cfg.secretRef` 传进去可行；插件也确实判了 `resolved?.value` 非空（[lib/index.js:144-152](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/index.js#L144-L152)）。

**3. 子进程 seam 形状正确，但插件只用了一条路径**。`ctx.subprocess: SubprocessRuntime`，`spawn(spec: SubprocessSpawnSpec): SubprocessHandle`（`dsh-subprocess/lib/types/index.d.ts:102`）；spec 要求 `argv`（**never shell-interpreted**）、`cwd`、`stdio`、`graceMs`（`dsh-subprocess/lib/types/types.d.ts:69-96`）；`stdio.stdout` 可以是 `'pipe'` 或 collect 规格 `{maxBytes}`（`SubprocessStdio` `types.d.ts:56-64`、`SubprocessCollect` `:39-48`、`SubprocessOutputMode` `:54`）；`handle.done: Promise<SubprocessOutcome>`，`SubprocessOutcome.exitCode: number | null`（`types.d.ts:107-115`）。插件传的 `{argv:['python','-c',SCRIPT,vaultPath,ref], cwd, stdio:{stdin:'ignore',stdout:'pipe',stderr:{maxBytes:1024}}, graceMs:2000}` 与这套形状吻合，读 `handle.stdout` + `handle.done` 也合法（[lib/index.js:153-180](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/index.js#L153-L180)）。注意这是**宿主的 vault 路径**；CLI/MCP/worker 走的是自己 `execFile(python, …)`（[credentials.mjs:72-82](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/credentials.mjs#L72-L82)），两处脚本常量是复制的，不是 import。

**4. `dsh.client.inject` + `dsh.bundle.patch` 都是真字段，插件两侧都接上了**。宿主的 client 模块系统读取 `dsh.client.platform`（必填字符串）与 `dsh.client.inject`（字符串数组）（`dsh-client-modules/lib/index.js:63-70`），并把 `exports["./client"]` 解析成浏览器半边（`:171-181`）。目标仓 `package.json` 正是 `dsh.client:{platform:'web', inject:[client-runtime, client-ui-sidebar]}` + `exports["./client"]='./lib/client-ui.js'`，而 `lib/client-ui.js` 是 `window.__ModuleLoader__.load({id:'dsh-agent-relay',…})` 的浏览器模块（[client-ui.js:1-8](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/client-ui.js#L1-L8)）。`dsh.bundle.patch` 是 dsh-base 自己声明的约定（`dsh-base/lib/types/index.d.ts:2-3`），插件把 `./cordis.patch.yml` 指过去（[cordis.patch.yml:1-4](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/cordis.patch.yml#L1-L4)）。**这一条是「有 client 注入」的实证，不只是清单里写了个字段。**

**5. 一个宿主角色的反差点**：DSH 自己的 webserver 在类型文档里写明 unspecified 地址「在加载期被拒绝」，并提供 `isLoopbackHost`/`isWildcardHost` 两个判据；relay broker **没有用这套判断**（它甚至不依赖宿主）。所以「loopback 边界」在宿主里有代码，在目标插件里只有文档。

**6. 一处** `[OPEN]` **的版本风险**：插件 `inject` 里 `webServer` 是**硬依赖**（不是 `ctx.inject(['webServer'], …)` 的等待式可选注入）。在 headless/无 web 的 profile 里，这个插件不会 apply——与 08 卡里 `interconnect` 把 webserver 当 optional 的做法相反。本机是 web profile，未跑，故只记录形状差异。

**7. 目标仓自述的 dsh 版本（0.1.0-rc.6）与本机（0.2.1-rc.3）不一致**：类型层面没发现冲突（上面 1-4 全部命中），但 `ctx.agents.get()`、`agent.steer()`、`ctx.get('sandboxPolicy'/'workspaceRegistry'/'sessionPersistence'/'agentDefaultModel')` 这些**软查找**（try/catch + 可选）在 0.2.1-rc.3 上是否仍返回预期对象，未运行不证。

## TEST

只核**存在性与覆盖面**，未运行、不证明通过。

- `test/` 下 **34 个 `*.test.mjs`** + 2 个 Python 文件（`protocol_v2_golden.py`、`test_relay_client_v2.py`）+ `test/helpers/broker.mjs`；`node --test`（CHANGELOG 0.8.1 自述 **152 passing**，grep `test(` 计数 **151**，差 1 可能来自 `test.skip` 或注释，未跑不裁）。
- 覆盖面对得上本 memo 的核对项：

| 核对项 | 有无测试 | 位置（示例） |
|---|---|---|
| 唤醒闸（presence / 挂起 pull） | 有 | `test/presence-and-wakeup.test.mjs` |
| 租约/令牌/重投 | 有 | `test/v2-lifecycle.test.mjs`、`test/v2-messages.test.mjs`（v1 的 `lease.test.mjs` 已在 `eb5e16d` 删除） |
| 幂等去重 | 有 | `test/v2-messages.test.mjs:64` `duplicate idempotency_key returns the same message_id with created=false` |
| SQLite 单一真相 | 有，且用**第二个连接**校验 | `test/store-v2-sqlite.test.mjs` |
| 跨语言字节一致 | 有（真 Python 子进程） | `test/protocol-v2-python.test.mjs` + `test/protocol_v2_golden.py` |
| v1 数据库迁移 | 有 | `test/migrate-v2.test.mjs`（造一个 `relay_messages` 源库） |
| 插件在宿主契约下装载 | 有（stub 宿主） | `test/plugin-harness.test.mjs`、`test-fixtures/plugin-harness-run.mjs` |
| 唤醒开关默认预演 | 有 | `test/enable-wake.test.mjs` |
| doctor 十项检查 | 有 | `test/doctor.test.mjs` |

- 一个**时间线信号**：pin 之后第一个行为修复是 `fc4a003 fix(broker): a failed wake now says why, instead of only its exit code`，第二个是 `57d407d test(wake): stop asserting a settled claim the instant the answer arrives`。说明 `v0.8.1` 的唤醒**失败诊断**与**唤醒测试断言**在当时都不完整——卡片若把 0.8.1 当「已验证的稳定点」，应当知道这两处在 tag 之后立刻被改。`[TEST]` 只证明测试源码存在，不证明 152 个都过。

## CI

只核存在性；**未取同 SHA check-run，故本 memo 不产 `[CI]` 证据**（GitHub REST 本轮 403 限流）。

- 唯一 workflow：`.github/workflows/ci.yml`，59 行，`name: CI`；触发 `push: branches:[main]` 与 `pull_request`（[ci.yml:1-6](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/.github/workflows/ci.yml#L1-L6)）。
- **4 个 job**：
  1. `test`：矩阵 `ubuntu-latest / macos-latest / windows-latest`，Node 22 + Python 3.10，跑 `node --test`（[ci.yml:8-27](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/.github/workflows/ci.yml#L8-L27)）。
  2. `secrets`：gitleaks，`fetch-depth: 0`（[ci.yml:29-38](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/.github/workflows/ci.yml#L29-L38)）。
  3. `license`：LICENSE 存在且含 "MIT License"（[ci.yml:40-48](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/.github/workflows/ci.yml#L40-L48)）。
  4. `lockfile`：有依赖时必须有 lockfile（[ci.yml:50-58](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/.github/workflows/ci.yml#L50-L58)）。
- **没有**：发布/publish workflow、release 资产、tarball 校验、版本一致性检查（08 卡里那种「清单版本必须等于 package.json」的小测试，这个仓没有）。
- 因此 **npm 断代与 CI 是一致的**：CI 只跑测试与扫描，没有自动发布通道；四个 tag 怎么打的、为什么没上 npm，仓库里没有记录（`[OPEN]`）。`[OPEN]`：`7e43c54` 上 4 个 job 的实际结论未取。

## RUN

`[RUN] None`（按指令**没有**安装、构建、跑测试、起 broker、加载插件、跑宿主）。

本轮实际做的**读操作**，可复现：

1. `git ls-remote https://github.com/Noelune/dsh-agent-relay` → `main`/tag/PR refs 与 SHA。
2. `git clone --filter=blob:none --no-checkout` → 81 commit 历史；`git log v0.8.1..main`（6 个）、`git show --stat eb5e16d`（51 文件 +521/−4399）、`git cat-file -t 6d17ff4`。
3. `curl codeload…/tar.gz/7e43c54…` → 解包 111 文件，逐文件读 `broker/src/{config,server,store-v2,v2-auth,v2-routes,index,protocol}.js`、`lib/{index,relay-tools,inbox-worker,broker-lifecycle,client-v2,message-handlers,session-manager,protocol}.js`、`lib/credentials.mjs`、`setup/{doctor,enable-wake}.mjs`、`adapters/{relay-agent.mjs,backends/*,openclaw/README.md,hermes/relay_client_v2.py}`、`docs/{SECURITY,ARCHITECTURE,PROTOCOL-V2}.md`、`README.md`、`CHANGELOG.md`、`.github/workflows/ci.yml`。
4. `curl registry.npmjs.org/dsh-agent-relay`（5 个版本、`gitHead`、时间表）；`…/dsh-agent-relay/0.5.0`。
5. `curl registry.npmjs.org/dsh-agent-relay/-/dsh-agent-relay-0.5.0.tgz` → 52 文件清单；`grep` 该包内 `wake_command|wait_seconds|waitFor`（零命中）与 v1 文件（命中 5 个）。
6. `api.npmjs.org/downloads/point/{last-month,last-week}`。
7. `img.shields.io/github/stars/Noelune/dsh-agent-relay.json` → `"value":"4"`。
8. 只读本机 DSH 0.2.1-rc.3 的 `dsh-host-webserver`、`dsh-system-prompt`、`dsh-tools`、`dsh-subprocess`、`dsh-credentials`、`dsh-client-modules`、`dsh-base` 类型与编译产物。

**没有做**：`npm i`、`dsh plugin add`、`node --test`、`node broker/src/index.js`、打开发布包里的 `relay.db`、取 GitHub Release/check-runs。

## 与卡片的偏差

> 按指令**未改卡**。口径：按当前工作树版（79 行）核对；「成立」= 能在 `7e43c54` 指到行；「过强」= 方向对但缺条件；「错/失效」= 在**可安装路径**上不成立。

| 卡片位置 / 主张 | 裁决 | 复核结论 | 标签 | 依据 |
|---|---|---|---|---|
| **L47 / L44**「版本（本次读）= `0.8.1`」+「安装 `dsh plugin --profile web add dsh-agent-relay`」 | **失效（最重）** | 0.8.1 只存在于 **git tag**；npm `latest` 仍是 **0.5.0**（2026-08-22），`0.6.0`–`0.8.1` 四个版本从未发布。按卡安装拿到 0.5.0。坐标必须写成「tag `v0.8.1` = commit `7e43c54`（**未发布**）」，安装必须写「`git clone` + 本地 `dsh plugin add <path>`」 | `[SRC-TARGET]`+registry | Provenance §1-3 |
| **L28 / L67**「`wake_command`：90 秒内没取过件就按需起一次」 | **成立但过强** | 实际是**两段闸**：有挂起长轮询 → 立即结算、不起进程；否则 90 s presence 闸；再否则 spawn。卡只写了第二段 | `[SRC-TARGET]` | [server.js:191-200](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L191-L200) |
| **L30**「唤醒是兜底而非竞争…避免同一消息被处理两次」 | **成立（但漏两个代价）** | 一 agent 一在飞 + 先结算挂起 pull，机理正确。漏：①`shell:true` 且**继承全量父环境**；②per-agent 密钥未配时子进程拿**共享密钥**；③broker 退出**不杀**已 spawn 的 worker | `[SRC-TARGET]` | [server.js:131-177](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L131-L177) |
| **L5 / L13 / L22 / L26**「只绑回环的 HTTP Broker」「边界由只绑 127.0.0.1 承担」 | **过强** | 默认环回、模板写明「loopback only」，但 `broker.host` 无校验、broker 无 loopback 断言；唯一的远端地址检查在**插件的状态路由**里。安全边界 = 部署纪律 + 配置，不是实现保证 | `[SRC-TARGET]` | [config.js:73-94](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/config.js#L73-L94)、[lib/index.js:259-283](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/index.js#L259-L283) |
| **L15 / L46**「4★ / npm 1,048 次/月」 | **成立** | 星数 4（shields，2026-11-01）；`last-month`（2026-09-30→10-29）恰为 1,048 | registry + shields | Provenance |
| **L26**「HMAC-SHA256 + 300 s 重放窗口 + 常量时间 + canonical JSON（v3 第二段插 keyId）；rate limit 与锁定属于已删 v1」 | **成立** | 逐条命中：`MAX_CLOCK_SKEW_SECONDS=300`、`timingSafeEqual`、`payload` 排序紧凑序列化、v3 签名串 `agent\nkeyId\nts\nMETHOD\npath\nsha256(body)`；配置层明写 rateLimit/lock 键被忽略 | `[SRC-TARGET]` | [protocol.js:16-39](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/protocol.js#L16-L39)、[protocol.js:105-126](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/protocol.js#L105-L126)、[config.js:98-104](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/config.js#L98-L104) |
| **L28**「投递语义是本域最完整的一套：7 天留存、SQLite 单一路径、租约+令牌化确认、长轮询落库即达、服务端定时扫描回发未送达、幂等键去重」 | **成立（六项全中）** | 六项都能指到行；补两个边界：幂等窗口 = 终态行 30 天保留期；presence 记的是「pull 过」不是「收到过」 | `[SRC-TARGET]` | §5、[store-v2.js:272-315](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/store-v2.js#L272-L315) |
| **L28 隐含**「投递语义最完整」= 端到端不丢 | **过强（DSH 侧）** | broker 层不丢；但 DSH 侧 reply 找不到会话映射就 **ack 后丢弃**；请求重投期间重复副本被直接 `ack completed`。所以「最完整」是 **broker 内部**的完整，不是 **会话层**的 | `[SRC-TARGET]` | [message-handlers.js:28-32](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/message-handlers.js#L28-L32)、[message-handlers.js:48-70](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/message-handlers.js#L48-L70) |
| **L32**「注册 5 个模型工具」 | **成立** | 正是 `send/status/history/peers/retry`；**但 MCP 是 6 个**（多 `relay_reply`），且 README 自己 5/6 两说 | `[SRC-TARGET]` | [relay-tools.js:99-136](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/relay-tools.js#L99-L136)、[README.md:104](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/README.md#L104-L104)、[README.md:215](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/README.md#L215-L215) |
| **L34**「v1 已于 2026-09-19 移除…协议规范只维护一处…两个测试锁住」 | **成立（树内）** | `eb5e16d`（2026-09-19 11:21 +08:00）51 文件 +521/−4399；`PROTOCOL.md` 删除、只剩 `PROTOCOL-V2.md`；两个跨语言测试在 | `[SRC-TARGET]` | §6 |
| **L34 / L71**「删掉了自己的一半」 | **树内成立，发布物不成立** | npm 0.5.0 仍含 `auth.js`/`store.js`/`client.js`/`sign.js`/`PROTOCOL.md`；另有 `v2-auth.js` 头注释死引用 `auth.js`、OpenClaw 文档仍教 v1。另外 CHANGELOG 说删了「五个测试文件」，diffstat 是 **6 个** | `[SRC-TARGET]`+registry | Provenance §3、§6 |
| **L36**「doctor 报什么…退出码 0/2/1」 | **成立（比卡多三类）** | 实现有 10 个检查名：`broker`（可达）/`members`（谁真能收 + 挂起长轮询）/`queues`（待投/处理中）/`history`（失败/过期）/`config`/`on-demand`（有无 `wake_command`）/`secrets`（两处漂移）/`plaintext`/`storage`（WAL 膨胀）/`adapter`（线上副本 vs 基线哈希）；退出码 `fail→1, warn→2, ok→0` | `[SRC-TARGET]` | [doctor.mjs:88-190](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/setup/doctor.mjs#L88-L190)、[doctor.mjs:220](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/setup/doctor.mjs#L220-L220) |
| **L42-53** 坐标表：repo / npm 名 / License / 端口 / 接线 / 自检 / 接入方式 | **除版本一行外成立** | MIT ✓、`127.0.0.1:19121` ✓、`main: lib/index.js` + `dsh.bundle.patch` + `dsh.client.inject` ✓（宿主侧也真读这两个字段，见 SRC-DSH §4）、MCP/CLI/JS/Python 四种接入 ✓ | `[SRC-TARGET]`+`[SRC-DSH]` | Provenance、SRC-DSH §1-4 |
| **L47**「安装…另装 `npm i -g dsh1024` 之外的 CLI 见仓库 `adapters/cli/`」 | **错（串了包）** | `dsh1024` 与本项目无关：它是「1024 Store」市场 CLI（`git+https://github.com/imsai-sh/awesome-deepseek-harness-plugins.git`，`packages/dsh1024`）。本仓**没有任何** `npm i -g` 说明，CLI 是 `node adapters/cli/relay.mjs`。这一行应删 | registry（`dsh1024`） | Provenance |
| **L50**「`agent-relay.json` 只记 vault 条目名，不记明文密钥」 | **过强（是约定不是结构）** | 加载器明确接受 `fileCfg.secret` 明文（`config.secret ?? env… ?? fileCfg.secret`）；`add-member`/`doctor` 的规范是只写 `secret_ref`，doctor 会对疑似 32+ hex 明文报 `fail`——**检测有，禁止无** | `[SRC-TARGET]` | [lib/index.js:61](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/index.js#L61-L61)、[doctor.mjs:161-166](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/setup/doctor.mjs#L161-L166) |
| **L51**「凭据来源：环境变量 / 指向已有 dotenv / DPAPI 保管库」 | **成立但分入口** | 顺序是 inline → `secret_env` → `secret_env_file`（dotenv）→ `secret_ref`+`vault_module`。**DSH 插件没有 dotenv 那条**（它的解析顺序是 inline → env → 宿主 `credentials.resolve` → vault 子进程），dotenv 只在 CLI/MCP/worker 上成立 | `[SRC-TARGET]` | [credentials.mjs:55-83](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/credentials.mjs#L55-L83)、[lib/index.js:137-180](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/index.js#L137-L180) |
| **L59** 三笔税「状态归属：broker 侧 SQLite 单一路径，请求留存 7 天；broker 挂了链路就断」 | **成立（补两点）** | 补：托管模式下 broker 是 **dsh 的子进程**，dsh 退 broker 退；重启会让 presence 归零 → 可能触发**一波真实计费的唤醒** | `[SRC-TARGET]` | §7、[broker-lifecycle.js:49-78](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/broker-lifecycle.js#L49-L78) |
| **L61** 三笔税「失败收敛：租约+令牌+幂等+超期自动回发未送达；rate limit 与锁定已删，暴力破解只剩回环」 | **成立** | 未送达通知由 60 s 独立扫描驱动、每请求一次、TTL ≥7 天；「只剩回环」与 SECURITY.md 自述一致（**且回环是默认不是强制**） | `[SRC-TARGET]` | [server.js:46-77](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/server.js#L46-L77)、[broker/src/index.js:50-65](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/broker/src/index.js#L50-L65) |
| **L67**「wake_command 是本域唯一真正解决『对端离线』的设计」 | **成立（限定语要加）** | 在同域样本里确实唯一；但它解决的是「**没人轮询**」，不是「**对端进程死**」——被唤醒的是一次性 CLI worker，它跑完就退，不维持会话；且要求配置者愿意付 API 费 | `[SRC-TARGET]` | §3 |
| **L77-79「别照抄」** 三条 | **前两条成立，第三条半成立** | ①HMAC 不等于安全（无速率限制/无锁定，回环是唯一闸）✓；②wake 会真花钱 ✓；③「只跨进程不跨工作区、不提供任何文件裁决」——**对 DSH 插件路径成立，对 worker 路径不成立**：write 模式有 git worktree 隔离 + 按工作区路径的跨 agent 写锁（PID 活性、15 min 过期）。准确说法是「插件不裁决文件；worker 只对 write 模式做最小互斥，仍不提供成员状态」 | `[SRC-TARGET]` | §1、§3、[workspace.js:1-9](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/workspace.js#L1-L9)、[lease.js:1-19](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/lease.js#L1-L19) |
| **L14**「证据级别 `observed`（源码逐文件读过）」 | **可升级** | 本 memo 已把七组机制 pin 到固定 commit 行号，达到 `[SRC-TARGET]` 强度；但**坐标必须先修**（版本 vs npm），否则「读过」读的是不可安装的树 | — | 本 memo |
| **缺项（L47 附近）**：发布物与仓库的关系 | **卡未写** | npm 0.5.0 的 `package.json` 有 `peerDependencies`（`@deepseek-ai/cordis ^4.0.1`、`dsh-tools ^0.1.0-rc.6`）与 `engines.node >=20`；**0.8.1 的 `package.json` 三者全无**，却 `import '@deepseek-ai/dsh-tools'` 且依赖 `node:sqlite`（需 Node ≥22.13，只在 README 里写）。若将来发布，依赖声明需要补 | `[SRC-TARGET]`+registry | Provenance §1、[package.json](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/package.json#L1-L45) |

## `[OPEN]`

1. **npm 0.5.0 随包的 `relay.db-wal`（28,872 B）里有什么**：本轮只确认文件非空，**没有解包读取**。若它含历史消息体，那就是「隐私设计」叙事之外的一个发布卫生问题。
2. **`0.6.0`–`0.8.1` 为何一直不发布**：仓库无 publish workflow、CHANGELOG 只有 release 小节，没有解释。`[OBS]` 候选解释（未证）：0.6–0.8 全部发生在 2026-09-19 一天内，作者按 tag 记账但没走 npm。
3. **同 SHA 的 CI 结论**：`7e43c54` 上 4 个 job 的 success/failure 未取（REST 403）。本 memo 不产 `[CI]` 证据。
4. **152 个测试是否真过**：按要求未跑；且 tag 之后立刻有 `57d407d test(wake): …` 修唤醒断言，v0.8.1 的该条断言当时是否正确存疑。
5. **本机 dsh 0.2.1-rc.3 能否装载该插件**：目标自述只测到 **0.1.0-rc.6**；`webServer` 是硬注入，headless profile 不会 apply。类型层面无冲突，运行未证。
6. **broker 退出后 `wake_command` 子进程是否残留**：代码里无 kill 路径（`unref` + `stdio:'ignore'`），推断会残留；残留多久、会不会与重启后的新 worker 同时认领，未实跑。
7. **`wake_command` 的 `shell:true` 在 Windows 上的实际解释器**：`enable-wake.mjs` 生成的命令含带空格的绝对路径并自己加了引号，跨平台引号规则未验证。
8. **0.5.0 与 0.8.1 的线协议兼容边界**：0.5.0 有 `lease_token`/`idempotency_key` 但**无** `wait_seconds`/`wake_command`/presence 字段；0.8.1 客户端对旧 broker 的降级是「忽略 wait_seconds，退回 fast/idle 轮询」（[lib/index.js:92-95](https://github.com/Noelune/dsh-agent-relay/blob/7e43c5452e035c6de7b5376fde131d08f5a0926d/lib/index.js#L92-L95) 注释），反向（新 broker + 旧客户端）未做端到端。
9. **GitHub Release 是否存在**：`/releases` 未查（403）；若存在，发布说明可能解释 npm 断代。
10. **`GET /healthz` 在非环回绑定下的暴露面**：代码可读出「无鉴权、回成员名单与队列计数」，但真实部署是否有人改过 `host`，无从得知。
