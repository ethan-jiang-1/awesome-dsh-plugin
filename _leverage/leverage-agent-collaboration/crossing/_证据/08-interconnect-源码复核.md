---
title: "08 · Chinesezjc/dsh-interconnect 源码复核"
domain: agent-crossing
kind: evidence
positioning: "对 dsh-interconnect 0.13.0（commit 5547b03 = tag v0.13.0 = npm gitHead）的固定提交复核：每对端持久 WS + inbox 投递成立；上游对齐闸已作废、必红。"
read_when: "核对 08 卡的 WS 拓扑、鉴权、退避、幂等/离线语义与「上游逐行同步」主张时读。"
status: observed
updated: 2026-11-01
---

# 08 · `Chinesezjc/dsh-interconnect` 源码复核

> 复核对象：样本卡 [`08-Chinesezjc-dsh-interconnect.md`](../samples/08-Chinesezjc-dsh-interconnect.md)。**注意**：复核开始时卡片为 66 行（`updated: 2026-10-31`），本轮进行中（2026-11-01T04:43）被并发修订为 **67 行**。修订内容与本 memo 的若干结论一致（是并发读取本 memo 还是独立复核，无法确证）；本 memo 的偏差表按**当前 67 行工作树版**核对，并单列「残留」。
> 取证时点 2026-11-01。只读 GitHub REST（`/repos`、`/commits`、`/tags`、`/branches`、`/releases`）、`registry.npmjs.org`（metadata + 0.13.0 tarball 目录清单）、`git clone` 后 checkout 固定 commit 的源码树、本机 `@deepseek-ai/dsh 0.2.1-rc.3` 发行包；**未安装、未构建、未跑 `pnpm test`、未启动宿主或插件、未跑对齐闸**。
> 标签沿用 [`EVIDENCE.md`](../../EVIDENCE.md)：`[DOC]` 目标仓 README/RELEASING/CHANGELOG 主张，`[SRC-TARGET]` 固定 commit 实现，`[SRC-DSH]` 本机 DSH 发行包，`[TEST]` 测试源码，`[CI]` 同 SHA check-run，`[RUN]` 本轮实跑，`[OBS]` 判断。
> **主 pin**：commit [`5547b03466a5db4a3d69e25fc48fa07611e8cff6`](https://github.com/Chinesezjc/dsh-interconnect/commit/5547b03466a5db4a3d69e25fc48fa07611e8cff6)（`main` HEAD，committer 2026-10-23T03:37:59Z，`package.json` 0.13.0）。**三处坐标完全对齐**：npm `0.13.0` 的 `gitHead` = 此 SHA，tag `v0.13.0` = 此 SHA，`main` = 此 SHA。
> 一句话结论：**传输/投递/鉴权/退避四条机制与卡片描述对得上**（含「无幂等」「无离线队列」两个空洞）。复核中发现的**最重问题**是「spec 与上游逐行同步、行为等价性可机械验证」——按仓库自己的 RELEASING.md，该流程 2026-09-16 已作废、2026-09-25 起本仓与上游分叉，对齐闸此后「必然判红」。**该问题在复核期间已被修订进卡片 L31；但 L63 仍保留旧说法，形成卡内自相矛盾，是本轮唯一未消解的重偏差。**

## Provenance

| 项 | 值 | 核对方式 |
|---|---|---|
| 仓库 | [`Chinesezjc/dsh-interconnect`](https://github.com/Chinesezjc/dsh-interconnect)（非 fork、`archived: false`、MIT、默认分支 `main`、创建 2026-08-13T12:19:01Z、`pushed_at` 2026-10-23T03:46:12Z、**38★ / 3 fork / 1 open issue** @2026-11-01、topics `deepseek-harness`/`dsh`/`dsh-plugin`/`interconnect`） | `/repos` |
| **npm 包** | `dsh-interconnect`，`dist-tags.latest = 0.13.0`；registry 共 41 个版本（0.1.0 … 0.11.24、**0.13.0**） | `registry.npmjs.org/dsh-interconnect` |
| **npm 0.13.0** | 发布 2026-10-23T03:47:38.930Z；`gitHead = 5547b03…`；`shasum 322d2a600fd0cb461dcc04e1925c19381926c90a`、`fileCount 35`、`unpackedSize 681654` | registry metadata |
| **主 pin（commit）** | `5547b03466a5db4a3d69e25fc48fa07611e8cff6`，subject `feat: wake a persisted session by default on send and reply`，committer 2026-10-23T03:37:59Z | `/commits/main` |
| **tag** | `v0.13.0` → `5547b03…`（40 个 tag；`v0.11.24 → v0.13.0` 之间**没有** `v0.12.0`） | `/tags` |
| **GitHub Release** | **不存在**（`/releases` 为空数组）；发布只走 npm + git tag | `/releases` |
| package.json | `version 0.13.0`、`main lib/index.js`、`type module`、`license MIT`、无 `engines`、无 `dependencies`、14 条 `peerDependencies`（`ws` 与 13 个 `@deepseek-ai/*`）+ 1 条 `peerDependenciesMeta`（webserver optional）、`files = [lib, assets, cordis.patch.yml, dsh.plugin.json, README.md, LICENSE]`、`scripts` **无 `prepare`/`postinstall`**（[package.json:1-95](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/package.json#L1-L95)） | 源码树 + tarball 内同一文件 |
| **tarball 内容** | 35 文件：`lib/*.js`（6 个入口 + 6 个 `.js.map`）、`lib/types/**/*.d.ts`（12 个）、`assets/dsh-interconnect.md`、`cordis.patch.yml`、`dsh.plugin.json`、`README.md`、`LICENSE`、`package.json`；**不含 `src/`、`tests/`、`.github/`、`scripts/`** | `curl` tarball + `tar tzf` |
| **tarball 与源码树一致性** | `dsh.plugin.json` 版本 0.13.0、`cordis.patch.yml` 与源码树**逐字节相同**（`diff` 无输出）、`package.json` 的 `version`/`scripts`/`files` 相同 | 抽取 3 个清单文件比对 |
| **CI** | 仅 `.github/workflows/ci.yml`（51 行），无发布 workflow | 源码树 |
| 下载量 | `last-month`（**2026-09-30 → 2026-10-29**）= **1017**；`last-week`（10-23 → 10-29）= 694 | `api.npmjs.org/downloads/point/…` |
| 卡片版本核对 | 卡片 L47 写 `0.13.0`，与本轮 pin 一致；复核期间补充的 L19「证据链」已带 `v0.13.0`/`5547b03` pin（见「与卡片的偏差」） | registry + `/tags` |

**坐标对齐与错位**

1. **三处对齐（本卡最好的一面）**：`npm@0.13.0` 的 `gitHead`、tag `v0.13.0`、`main` HEAD 指向同一个 SHA `5547b03`。这让「0.13.0」本身成为可复现坐标——`git checkout v0.13.0` 就是发布源码，不必另找 commit。
2. **没有 GitHub Release**：`/releases` 空。这不影响可复现性（tag 在），但意味着没有 release notes 面，变更说明只在 `CHANGELOG.md`。
3. **0.12.0 是「仓库版本、非发布版本」**：`CHANGELOG.md` 有 `## 0.12.0（2026-09-25）` 整节（[CHANGELOG.md:45](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/CHANGELOG.md#L45-L45)），commit `428df37` 的 subject 是 `docs: add the two-machine quickstart, release 0.12.0`，`package.json` 在 `428df37` 时确实写着 `"version": "0.12.0"`（`git log -S` 可证）；**但 npm 没有 0.12.0，也没有 `v0.12.0` tag**。所以 0.12.0 从未发布，0.13.0 的 CHANGELOG 仍以「与 0.12.0 的构建产物比对」为基线——版本号序列在 npm 上有一个洞，跳过原因未见记录（`[OPEN]`）。
4. **npm 元数据里没有 `repository` 字段**：`registry` 返回 `repository: undefined`，`package.json` 也没写。从 npm 页面无法跳到 GitHub，仓库坐标只能靠 README/搜索确认——这是溯源摩擦，不是错误。
5. **`gitHead` 只证明发布时工作树来自该 commit**，不证明 tarball 里的 `lib/*.js` 等于该 commit 的构建产物（构建需 esbuild，本轮按指令未跑）——字节级一致性 `[OPEN]`。

## DOC

`[DOC]` 只证明作者声称什么，不证明实现如此。

- **传输自述**：「全走持久 WebSocket 链接：跨实例、跨机器投递消息…（`send`/`reply`/`ping`/`list` 经 `/interconnect/link` 的 `msg`/`query` 帧）」；「`/interconnect/link` WebSocket 端点：双向实时事件推流，含心跳与指数退避重连；…**0.9 起没有 HTTP 端点，也没有 HTTP 回退**」——[README.md:12-14](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L12-L14)。「心跳与指数退避重连沿用既有实现」——[README.md:135](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L135-L135)。
- **鉴权自述**：「共享密钥鉴权（`DSH_INTERCONNECT_TOKEN`，bearer，fail-closed，timing-safe 比较）」——[README.md:16](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L16-L16)；「任一端没配 token 时端点 fail-closed，直接 403」——[README.md:327](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L327-L327)。
- **寻址自述**：「`instanceId` 是 `interconnect` 行 `peers` 映射里的键；真正用来拨号的 origin 由该映射的值给出…**`instanceId` 本身从不出现在线上**，也不参与路由——origin 才是唯一的拨号依据」——[README.md:47](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L47-L47)。
- **配置默认值自述**表：`instanceId 'dsh'`、`requestTimeoutMs 10000`（上限 60000）、`peers {}`、`delivery 'followup'`、`allowResume true`——[README.md:243-247](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L243-L247)。
- **不直投 subagent 自述**：「`interconnect_send` 不会往 subagent 拥有的 session 里投递，`interconnect_list` 也不会把它们列出来…判定逻辑镜像 Host 的 `hasApiSessionSubagentOwner`…所以这里**逐字复制一份**（`isSessionOwnedBySubagent`）」——[README.md:162-173](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L162-L173)。
- **resume 默认开自述**（2026-10-23 起）：不带 `resume` 时两个工具按 `true` 处理，传 `false` 才保持原样；「**默认开启是 2026-10-23 的决定**」——[README.md:175-193](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L175-L193)。CHANGELOG 同一决定带动机与实测：`session-not-live` 后改投别的 session 导致原会话永远收不到——[CHANGELOG.md:5-43](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/CHANGELOG.md#L5-L43)。
- **投递模式自述**：`followup` = `next-turn` + 唤醒；`steer` = `next-step` + 唤醒；`inject` = `next-step` 不唤醒——[README.md:223-231](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L223-L231)。
- **失败原因自述**：8 个 `reason` 的语义与「哪些只可能来自本机」——[README.md:142-160](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L142-L160)。
- **工程策略自述（关键）**：「本仓库是该插件的**树外（out-of-tree）主源**。并入 DSH monorepo 的计划（PR #3243）已按「保持树外」的评审意见关闭」——[README.md:5](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L5-L5)。更明确的作废声明在 RELEASING：「PR #3243 已关闭、未合并…**§一 的同步流程与 §六 的迁移预案均已作废**」——[RELEASING.md:3](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/RELEASING.md#L3-L3)；「**⚠️ 已作废（2026-09-16）**：上游分支 `feat/merge-dsh-interconnect` 随 #3243 关闭而不再前进。本节流程与 `scripts/check-upstream-alignment.mjs`、`scripts/port-upstream-change.mjs` 保留仅作历史工具——对齐门禁要比较的 ref 已冻结，不会再产生新结论」——[RELEASING.md:9](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/RELEASING.md#L9-L9)；「**2026-09-25 起本仓开始与上游分叉**（0.12.0 新增 `interconnect_peers`、失败原因 `peer-not-configured`…）。此后对齐门禁**必然判红**，报的是分叉本身而不是漂移」——[RELEASING.md:11](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/RELEASING.md#L11-L11)。
- **对齐闸自述**：七类不变量，第 1 条「四个源文件 + 三个 spec：剥掉注释与 import 行后的骨架必须逐行一致」，第 2 条「原始文本（注释计入）…除 `RAW_ADAPTATIONS` 记录在案的适配行以外，必须逐字一致」——[RELEASING.md:21-24](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/RELEASING.md#L21-L24)。
- **测试/CI 自述**：「179/179 单测通过」——[README.md:408](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L408-L408)；「CI（GitHub Actions）：clone 公开 DSH 仓库作为 sibling，跑 `pnpm run check`」——[README.md:412](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L412-L412)。注意 `[DOC]` 内部就不一致：README 说 179，CHANGELOG 0.13.0 说「4 files / 180 tests」，本仓 `it(` 计数 180——README 那一行是旧的。
- **安装后 403 自述**：「已实测：安装前 `GET /interconnect/link` 返回 404，安装后 6 秒内同一请求返回 403（插件 fail-closed 的应答）」——[README.md:281-283](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L281-L283)。这是作者实测（`[OBS]`），本轮未复现。
- **无损/幂等自述**：README 全文**没有**声称「消息不丢」或「恰好一次」；反而在失败表里把超时归到 `unreachable` 并写「重连成功后就可能通」——[README.md:132-140](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L132-L140)。作者对这两个空洞是诚实的。

## SRC-TARGET

以下行号全部 pin 到 commit `5547b03`。先给十项核对清单的裁决表，再逐条展开。

### 0. 主张裁决（先看这张表）

| # | 核对项 | 裁决 | 关键依据 |
|---|---|---|---|
| 1 | 每个对端一条持久 WebSocket | **成立但需精确化**：每个**已配置**对端一条**拨号**链；互配的一对实例之间有**两条** socket（各拨一条），单条 socket 本身双向（正文 L13/L23 已在复核期间按此修订；frontmatter L5/L6 未改） | [index.ts:407-411](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L407-L411)、[index.ts:766-800](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L766-L800) |
| 2 | 消息如何注入对端 session inbox | **成立**：`deliver()` → `ctx.agents.get(sessionId)` → `agent.followup/steer/inject(createUserMessage({source, content:[text]}))`；splice 由宿主完成 | [index.ts:1000-1088](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1000-L1088) |
| 3 | 认证/配对 | **只有一把共享密钥**：`DSH_INTERCONNECT_TOKEN` bearer，缺 token 403、错 token 401；**没有配对仪式、没有 per-peer 密钥、没有 id 白名单** | [index.ts:1107-1140](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1107-L1140) |
| 4 | 重连/退避 | **成立**：`min(30s, 1s·2^retry)`，`onOpen` 归零；**无 jitter**；握手 10s 上限；30s 心跳 | [index.ts:1455-1462](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1455-L1462)、[index.ts:455-469](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L455-L469) |
| 5 | 离线队列（卡说无） | **成立，无队列**：链路不 `writable()` 即 `undefined` → `unreachable`；断链期间事件同样丢弃不补发 | [index.ts:647](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L647-L647)、[index.ts:554-556](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L554-L556) |
| 6 | 幂等（卡说无） | **成立，无消息级幂等**：`reqId` 每次新生成、只做关联、超时即删 pending；重试＝重新投递 | [index.ts:648](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L648-L648)、[index.ts:703-707](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L703-L707) |
| 7 | 什么标识一个 peer | **三个不同的东西**：配置键（寻址）、origin（拨号）、`hello.sender`（自报、仅事件归因）；自报 id **不经认证绑定**，与配置键不一致只 warn 一次 | [index.ts:1224-1231](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1224-L1231)、[types.ts:307-350](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/types.ts#L307-L350) |
| 8 | 多实例拓扑 | **配置驱动的部分网状**：无发现、无注册中心、无 leader；可单向、可互配、可枢纽；事件按「自己拨的链优先」去重 | [index.ts:773-800](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L773-L800) |
| 9 | 状态归属 | 消息落到**接收方 session log**；本插件只有内存表 `senders`（重启即丢）与 `pendingMessages`；无租约、无工作区、无任务 | [index.ts:383](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L383-L383)、[index.ts:1082-1086](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1082-L1086) |
| 10 | 失败/降级；协议不匹配 | 8 个 `reason` 分支完备；**协议没有版本字段**，不匹配表现为「帧被丢 → 超时 → unreachable」，没有专门的版本错误码 | [index.ts:328-347](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L328-L347)、[index.ts:1214-1220](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1214-L1220) |

### 1. 传输：谁拨号、几条链、什么走链

构造器对 `Config.peers` 的每个条目建一个 `LinkState` 并立刻 `dial()`，因此**已配置对端数 = 拨号链数**（[index.ts:407-411](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L407-L411)、[index.ts:736-747](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L736-L747)）。接收侧对每个通过鉴权的 upgrade 建 socket 加入 `sockets` 池（[index.ts:1138-1141](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1138-L1141)、[index.ts:1150-1185](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1150-L1185)）。

**关键的结构事实**：`attachSocket` 同时服务拨号侧与被拨侧，装 message/pong/close/error 处理器，并向对端发一条 `hello` 自报 id（[index.ts:1183](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1183-L1183)）。所以**单条 socket 是双向的**：事件可以沿它双向推流。但 `msg`/`query` 请求只能沿**本实例配置的拨号链**发——`msgRequest`/`queryRequest` 只查 `linkStates`（[index.ts:637-647](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L637-L647)、[index.ts:678-682](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L678-L682)）。

于是拓扑分三种，代码都允许：

```
A 配了 B，B 没配 A     → 1 条 socket（A→B 拨）。事件双向；A→B 的 send/ping/list 通；
                          B→A 的 send/reply 得 peer-not-configured。
A 配了 B，B 也配了 A   → 2 条 socket（各拨一条）。两个方向都通；事件需去重（见 §8）。
A 配了 B、C；B 配 C    → 3 条 socket，非完全图。没有发现机制，谁配谁才有链。
```

这也解释了代码注释里那句「A bidirectional pair owns two sockets to the same peer」（[index.ts:766-772](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L766-L772)）。卡片 frontmatter（L5/L6）仍写「每个对端一条持久 WebSocket」，在**单向**时精确、在**互配**时是两条；正文 L13/L23 已在复核期间按本条修订为「已配置对端 / 互配两条」——frontmatter 是残留。

**为什么不用宿主的 Connection RPC 通道**：模块头写明理由——那个 registry 的 handler 只收到 `(endpoint, payload, signal)`，信任栅栏是 DNS-rebinding 的 `trustedHosts` 检查，两者都不携带本服务用来鉴权的共享密钥 `Authorization` 头；自持一条 upgrade 路由才能把 bearer 鉴权放在读得到 header 的边界上，并在 token 未配置时 fail-closed（[index.ts:1-14](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1-L14)）。这是一个可复用的设计判断。

webserver 是**可选**依赖：`ctx.inject(['webServer'], …)` 用等待式 fiber 注册 upgrade 路由，所以组合顺序不会造成路由漏注册；没有 webserver 的 profile（headless）仍拨号并投递，只是不接受入站（[index.ts:432-434](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L432-L434)、[package.json:67-71](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/package.json#L67-L71) 的 `peerDependenciesMeta`）。

### 2. 投递：inbox 注入的真实路径

一条入站 `msg` 帧的完整路径（[index.ts:802-815](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L802-L815) → [index.ts:1000-1088](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1000-L1088)）：

1. `handleFrame` 认出 `type: 'msg'`，异步调用 `handleMsgFrame`，异常兜成一条 `msg-result{unreachable}`（[index.ts:1265-1277](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1265-L1277)）。
2. `deliver()` 先查 `ctx.agents.get(sessionId)`；没有 live agent 则走 `wake()`（[index.ts:1000-1017](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1000-L1017)）。
3. 子代理封栏：`isSessionOwnedBySubagent` 命中即 `session-owned-by-subagent`，**不进 inbox**（[index.ts:1022-1024](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1022-L1024)）。
4. `createUserMessage({ source: { kind: 'plugin:dsh-interconnect', form: 'notice', summary: … }, content: [{ type: 'text', text: payload.text }] })`——**content 里只有对端发来的文本**，发送方身份只进 `source.summary`（[index.ts:1044-1053](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1044-L1053)）。
5. `DeliveryMode` 三选一，穷尽 switch：`steer` → `agent.steer`、`inject` → `agent.inject`、`followup` → `agent.followup`（[index.ts:1061-1071](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1061-L1071)）。
6. 投递成功后才记 `senders.set(localSessionId, sender)`；不带 sender 的入站消息会**清掉**旧记录，防止回信打到上一个发送方（[index.ts:1076-1086](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1076-L1086)）。

**所以「投进 inbox」是宿主的行为，不是本插件的行为**：插件只调 `Agent.followup/steer/inject`，真正的 inbox splice 与 `agent/inbox/spliced` 事件在 `@deepseek-ai/dsh-agent`（见 SRC-DSH）。这是卡片 L27「`send` = 投 inbox 并调 `agent.followup/steer/inject`」的准确读法。

**`event` 与 `send` 的分流是真的**：`receiveEvent` 只做 `ctx.logger.info` + `ctx.parallel('interconnect/event', notification, sender)`，**完全不碰任何 session**（[index.ts:842-863](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L842-L863)）。用 `parallel` 而非 `emit` 的理由写在注释里：`emit` 不 await，listener 返回 rejected promise 会变成 unhandled rejection；`parallel` 会 settle 全部并聚合失败。而且**入站事件不会被再广播**——没有回环放大。

fanout 只在本机生命周期事件上挂（`agent/status`、`agent/created`、`agent/disposed`、`session/created`、`session/disposed`、`subagent/end`），且 `subagent/end` 只发 `info.local` 的（[index.ts:471-514](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L471-L514)）。

### 3. 鉴权与「配对」：只有一把共享密钥

入站 upgrade 的四条拒绝路径（[index.ts:1107-1140](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1107-L1140)）：

| 情形 | 应答 | 行 |
|---|---|---|
| token 读取抛错 | `403 Forbidden` + socket 关闭 | [1117](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1117-L1117) |
| token 未配置 / 空 | `403 Forbidden`（fail-closed） | [1120-1123](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1120-L1123) |
| 服务已 dispose | `503 Service Unavailable` | [1129-1133](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1129-L1133) |
| `Authorization` 缺失或不等 | `401 Unauthorized` | [1134-1137](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1134-L1137) |

比较方式与卡片 L61 完全一致：**两侧先 `sha256` 归一成等长 digest，再 `timingSafeEqual`**——这样畸形的多字节 header 不会以长度不匹配的身份进到 crypto 层，比较也不泄漏长度（[index.ts:1466-1474](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1466-L1474)）。出站 `new WebSocket(url, { headers: { authorization: \`Bearer ${token}\` }, maxPayload: 1MiB, handshakeTimeout: 10s })`（[index.ts:1384-1393](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1384-L1393)）。

**「配对」这一层不存在**。逐项核对：

- **无 per-peer 密钥**：所有 peer 共用 `DSH_INTERCONNECT_TOKEN` 一个值（[index.ts:93](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L93-L93)）。
- **无 peer id 白名单**：入站 socket 的 `hello.sender` 只写进 `peerOf` 用于事件归因，不与 `Config.peers` 做准入比对；**任何持同一 token 的实例都能 upgrade 成功**，能收全量事件，也能 `send`（只要知道目标 `sessionId`）。
- **身份未经认证绑定**：`hello.sender` 是自报字符串，两个实例可以自称同一个 id；`Config.instanceId` 的文档明说「必须全网唯一」，否则事件重复或只走一条（[types.ts:307-316](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/types.ts#L307-L316)）。
- **无握手后的二次确认**：upgrade 通过即入池，`hello` 是**无条件**先发（[index.ts:1183](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1183-L1183)）。

结论：安全边界 = **整个 mesh 共用一把密钥**。卡片 L61 的技术细节全对，但没有写出「配对只到共享密钥这一级，没有 per-peer 授权」——这决定它能不能用在互不完全信任的几台机器之间。

### 4. 重连与退避

```
retry=0 ──失败──> 1s ──> 2s ──> 4s ──> 8s ──> 16s ──> 30s ──> 30s ──> …
                      (onOpen 时 retry 归零；open 之后掉线重新从 1s 开始)
```

- 公式就是卡片写的 `min(30s, 1s·2^n)`（[index.ts:1455-1462](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1455-L1462)），`n` 从 0 起、每次排程自增，`onOpen` 归零（[index.ts:1395](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1395-L1395)）。
- **没有 jitter**：所有 peer 在同一时刻掉线后会按同一张时刻表重连，多实例场景下是同步重连风暴。代码里没有 `Math.random()`，也没有注释承认这一点——是设计缺口，不是隐瞒。
- **握手窗口**：`handshakeTimeout: 10000`（[index.ts:1392](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1392-L1392)）。注释解释了为什么要有：只接受 TCP 但永不完成 upgrade 的对端会让 socket 永远停在 CONNECTING——既不 open（没有心跳）也不 close（不触发重连）；交握超时让 ws 自己 abort，error+close 随之到来，由 close handler 排下一次重连，且定时器归 ws 所有，拆卸时不泄漏。
- **心跳**：30s 一轮的 `setInterval`，对池里每个 socket 做 ping/pong 存活判定，上一轮没回 pong 的直接 `terminate()` 并出池（[index.ts:455-469](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L455-L469)）。检测窗 **30–60s**。心跳常量与退避常量都被注释声明为「协议常量，不是部署可调项」（[index.ts:450-452](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L450-L452)）。
- **token 后注入可自愈**：每次 `dial()` 都重新 `resolveToken()`；没有 token 时 warn 一次然后继续按退避重试，所以事后注入 credential 能把链拉起来，不用重启（[index.ts:1368-1381](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1368-L1381)）。
- **拆卸干净**：fiber 卸载时清心跳定时器、关每条 LinkState、terminate 全部 socket、关 acceptor，并把所有 in-flight 请求 settle 成 `unreachable`（[index.ts:517-533](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L517-L533)）。

### 5. 离线语义：没有队列，「离线」还有第二种含义

链路不 `writable()` 时 `msgRequest` 直接返回 `undefined`（[index.ts:647](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L647-L647)），`send()` 把 `undefined` 兜成 `{delivered:false, reason:'unreachable'}`（[index.ts:553-556](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L553-L556)）。**没有 outbox、没有重放、没有落盘缓冲**——`src/` 里没有任何 `queue`/`outbox`/`buffer` 形态的持久化（`grep -i` 无命中，只有 `pendingMessages` 这个内存 Map）。卡片 L29「无离线队列（链路断即 `unreachable`，不缓存）」**逐字成立**。

顺带两个同族事实：

- **事件也不补发**：`broadcast` 对非 OPEN 的 socket 直接删除并跳过（[index.ts:779-790](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L779-L790)）。断链期间的生命周期事件永久丢失，重连后不重放。卡片说的是「无离线队列」，事件侧同罪。
- **「离线」有两种**：原卡把两者混在一句里，复核期间已在卡片 L29 补齐；区分如下——**(a) 链路离线**：无队列，消息丢，`unreachable`；**(b) 链路在线但目标 session 没有 live agent**：0.13.0 起工具默认 `resume: true`，会把 session 唤醒再投递（[index.ts:961-994](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L961-L994)）。两者失败原因不同（`unreachable` vs `session-not-live`/`resume-refused`/`resume-failed`），处置也不同。把 (b) 也算成「离线可唤醒」，读起来像 (a) 有救——实际上 (a) 一定丢。

`wake()` 的四层判定：`resume !== true` → `session-not-live`（[962](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L962-L962)）；`allowResume` 为假 → `resume-refused`（[963](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L963-L963)）；没有 `typert.lookups.get('agent')` → `session-not-live`（[968](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L968-L968)，headless 部署的降级）；resolver 抛 `session/agent-busy` → `session-owned-by-subagent`，其余抛错 → `resume-failed`（[984-993](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L984-L993)）。注释里的理由值得记：**不用 `ctx.agents.resume()` 而走宿主 lookup，是因为 `resume()` 的 handle 由调用方 context 拥有**——插件 fiber dispose 时会把 agent 和 session 一起拆掉；宿主 resolver 拥有它，且会按 session 日志记录的 preset 重建工具集。

### 6. 幂等：`reqId` 只做关联

- 生成：`const reqId = \`m${++this.reqIdCounter}-${randomUUID()}\``（[index.ts:648](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L648-L648)）；query 用 `q` 前缀。每次调用都是新 id，**不复用**。
- 消费：`handleMsgFrame` 收到 `msg` 就直接 `deliver()`，**没有任何「这个 reqId 见过」的查表**（[index.ts:802-815](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L802-L815)）。
- 超时：`setTimeout` 到点 `pendingMessages.delete(reqId)` 并 reject（[index.ts:703-707](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L703-L707)），`send()` catch 成 `unreachable`。**此时对端可能已经投递成功、只是答复丢了**——这是「重试可能重复投递」的具体机制，卡片 L29 的表述准确。
- 结果帧按 kind 绑定，防止串号：`msg-result` 只结算 `kind==='msg'` 的 pending，`query-result` 只结算 `kind==='query'` 且必须过该 kind 的 projector（[index.ts:1244-1260](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1244-L1260)）。**这是「响应侧」的防串扰，不是「消息侧」的幂等**——两者不能混为一谈。
- 线缆词表收窄：`msgResultSchema` 只接受 5 个 reason（`session-not-live`/`unreachable`/`resume-refused`/`resume-failed`/`session-owned-by-subagent`）（[index.ts:328-337](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L328-L337)），所以 `message-too-large`/`peer-not-configured`/`no-sender-known` 这三个本机原因**对端伪造不出来**。这个设计值得抄：失败原因分「本机判定」与「对端可回答」两层，避免对端借失败码影响本机的路由判断。

### 7. 什么标识一个 peer：三个字段，别混用

| 字段 | 谁写 | 用途 | 是否可伪造 |
|---|---|---|---|
| `peers` 映射的**键** | 本实例操作者（config） | `send`/`reply`/`ping`/`list` 的寻址键，`linkStates` 的 key | 不适用（本地配置） |
| 映射的**值**（origin） | 本实例操作者（config） | **唯一的拨号依据**；`instanceId` 不参与拼地址 | 不适用（本地配置） |
| `hello.sender` / `sender.instanceId` | 对端自报 | 事件归因（`peerOf`）、回信寻址（`senders`）、`peer-status` 诊断 | **可以**：不经认证绑定 |

- `linkUrl(origin)` 只把 `http:`→`ws:`、`https:`→`wss:`，显式 `ws:`/`wss:` 保留（不会把 TLS 对端降级成明文），其它 scheme 抛 `TypeError`（[index.ts:1488-1499](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1488-L1499)）。构造器在 dial 任何对端之前**先把所有 origin 过一遍 `linkUrl`**，所以配置错在激活时就炸，而不是留下一个漏 socket/漏重连循环（[index.ts:402-405](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L402-L405)）。
- 配置键与自报 id 不一致时：**链路照常按配置键工作**（`send`/`ping`/`list` 都用键），只在 `hello` 到达时 warn 一次（[index.ts:1224-1231](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1224-L1231)）。后果不是断链，而是**事件重复**：那条自报别的名字的入站 socket 不被认作「已有拨号链覆盖的同一个 peer」，于是同一个事件从两条 socket 各到一次（见 §8）。
- 所以卡片 L25「peers 键**是**对端自报的 `instanceId`」应读作「键**应当**等于对端自报的 id；不一致只 warn，代价是事件重复」。方向对，强度过头。

### 8. 多实例拓扑：配置驱动的部分网状

- **没有发现机制**：没有注册中心、没有广播寻址、没有 leader/follower。拓扑 100% 由每个实例自己的 `peers` 映射决定，因此是**部分网状**，且**允许不对称**（A 有链到 B，B 没有到 A）。
- **事件去重规则**（[index.ts:773-800](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L773-L800)）：先收集「本实例有拨号链的对端 id」集合 `covered`；再遍历池，**拨号 socket 一律发**；**入站 socket 只在它自报的 id 不在 `covered` 里时才发**。规则用「本地所有权」而不是「对端自述」来决定，注释点明理由：这样自报 id 无法让另一个 peer 的链被静默。
- **已知的瞬时重复**：从拨号链 open 到对端 `hello` 抵达之间，入站 socket 还不可归因，这个窗口里发出的事件会走两条 socket，对端收到两份。注释明说「The duplicate is transient and never a dropped event」（[index.ts:764-772](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L764-L772)）。**宁可重复、不可丢**是明确取舍。
- **instanceId 必须全网唯一**：两个实例共用一个 id 时，只会走「本实例拨的那条」，另一个的入站被跳过——即事件只到一边（[types.ts:307-316](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/types.ts#L307-L316)）。
- **`peers` 变更不需要重启**（前提是 patch 层被真正应用）：构造器只在激活时读一次映射，profile 的 HMR 行重算 patch 层会重建 fiber 并按新映射建链（[types.ts:344-350](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/types.ts#L344-L350) 与 [README.md:62-68](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L62-L68) 的双向实测记录）。

### 9. 状态归属

| 状态 | 存在哪 | 生命周期 |
|---|---|---|
| 消息本体 | **接收方 session log**（`agent/inbox/spliced` 持久化）；归接收实例所有 | 随 session 日志；本插件不管 |
| `senders`（本地 sessionId → 发送方身份） | 插件内存 `Map`（[index.ts:383](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L383-L383)） | 进程重启即丢；`session/disposed` 时删（[index.ts:491](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L491-L491)） |
| `pendingMessages` / `peerOf` / `dialedPeerOf` / `linkStates` | 插件内存 | fiber 拆卸时清空 |
| 已投递结果 | 无 | 没有 spool、没有回执表 |

**没有任何共享可变状态**：没有租约、没有工作区、没有任务队列、没有共享文件。`src/` 全仓 `grep -iE '\b(task\|lease\|worktree)\b'` 零命中——卡片 L25 的「没有任务、没有租约、没有 worktree」是**可验证的结构事实**，不是修辞。

代价也说清楚：`senders` 是内存表，**实例重启后回信能力丢失**——一个本地 session 重启前收到过的消息，重启后 `reply` 会返回 `no-sender-known`（[index.ts:570-574](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L570-L574)）。卡片的三笔税表把它归到「状态归属：对端实例的 session inbox」是对的，但没有点出这张内存表——它才是 `reply` 的唯一来源。

### 10. 失败与降级；协议不匹配

**失败分支是完备的**，8 个 `reason` 各有出处，且本地/远程分层清晰：

| reason | 产生位置 | 含义 |
|---|---|---|
| `peer-not-configured` | 本机 [index.ts:646](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L646-L646) | `peers` 里没这个键，重试永不成功 |
| `unreachable` | 本机 [554](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L554-L554) / [586](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L586-L586) + 超时 + 拆卸 | 链路断、无答复、鉴权被拒、服务已 dispose |
| `message-too-large` | 本机 [index.ts:664-665](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L664-L665) | 编码后 >1 MiB；**什么都没写、链路没断** |
| `session-not-live` | 接收方 [962](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L962-L962)/[968](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L968-L968) | 没 live agent，且未请求唤醒或无唤醒能力 |
| `resume-refused` | 接收方 [963](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L963-L963) | `allowResume: false` |
| `resume-failed` | 接收方 [992](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L992-L992) | 唤醒尝试了但没得到 live agent |
| `session-owned-by-subagent` | 接收方 [990](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L990-L990)/[1023](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1023-L1023) | 归父 agent 投递 |
| `no-sender-known` | 本机 [573](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L573-L573) | 该本地 session 从未记过发送方 |

**协议不匹配：没有版本协商，这是真实缺口。** `hello` 帧只有 `sender` 一个字段（[index.ts:340-347](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L340-L347)、[types.ts:250-256](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/types.ts#L250-L256)），**全仓没有 `version`/`capabilities`/`negotiate` 字样**。不匹配的四种表现：

1. **未知 `type`** → 联合 schema 不匹配 → `warn('dropping malformed link frame')` 并丢弃（[index.ts:1214](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1214-L1214)）。
2. **字段形状变了**（例如新的 `reason`）→ 同上丢弃（[index.ts:1220](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1220-L1220)）。
3. **帧超 1 MiB** → 先按字节数拒绝，warn「dropping oversized link frame」，**不解析**（[index.ts:1189-1198](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1189-L1198)）；发送侧另有 `maxPayload: 1MiB`。
4. **二进制帧** → 直接丢，不解析（[index.ts:1169-1172](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1169-L1172)）。

四种的对外表现**统一是「帧消失 → 请求超时 → `unreachable`」**，调用方**分不出**「对端版本旧」和「对端挂了」。跨版本兼容因此只靠两条软约束：字段全可选（`sender`/`delivery`/`resume` 缺省即旧语义），以及结果帧按 kind 校验（[index.ts:1244-1260](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1244-L1260)）。0.13.0 的 commit 把这一点说得很明确：「The wire default stays 'do not wake', so old peers interoperate unchanged」——**兼容策略是「只加可选字段、不改缺省语义」，不是版本握手**。这是可用但脆的策略：一旦需要「这个 peer 支持 X 吗」，没有地方问。

**其它降级点**：webserver 缺失 → 仅出站模式；`typert` lookup 缺失 → `session-not-live` 而不是报错；title projection 抛错 → 该行降级成只有 id，整个 list 不失败（[index.ts:931-955](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L931-L955)）；list 有 100 行与字节双上限，超限就截断而不撑爆帧（[index.ts:156](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L156-L156)、[index.ts:869-884](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L869-L884)）。

### 11. 上游对齐闸：脚本在，流程已作废（本 memo 最重的一条）

**原卡 L30（复核期间被拆成 L31 与 L63 两处，L31 已改写、L63 未改）**的完整主张是：「它的 spec 与上游 monorepo **逐行同步**,并有 `check-upstream-alignment.mjs` 双遍闸（骨架比对 + 含注释原文比对,白名单外任何差异=漂移）;`port-upstream-change.mjs` 按映射表机械搬运上游 diff 并自动跑闸。意义是**树外发布通道与上游行为等价性可机械验证** ——但 CI 不跑这道闸。」下面按这段原文逐项裁决。

逐项裁决：

| 子主张 | 裁决 |
|---|---|
| `check-upstream-alignment.mjs` 是双遍闸（骨架 + 含注释原文 + 白名单） | **成立**：脚本头写明两遍与「comments are ported from upstream like code」；`RAW_ADAPTATIONS` 就是白名单；差异 exit 1（[check-upstream-alignment.mjs:1-20](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/scripts/check-upstream-alignment.mjs#L1-L20)、[scripts/check-upstream-alignment.mjs:645-648](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/scripts/check-upstream-alignment.mjs#L645-L648)）。而且实际是**七类不变量**，不止两遍（[RELEASING.md:21-30](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/RELEASING.md#L21-L30)）。 |
| `port-upstream-change.mjs` 按映射表搬运 diff | **成立**：文件在，125 行。 |
| **「spec 与上游逐行同步」**（L31 已改口，L63 仍如此主张） | **不成立（0.13.0）**：RELEASING.md 明写「2026-09-25 起本仓开始与上游分叉」——0.12.0 就新增了 `interconnect_peers` 与 `peer-not-configured`，0.13.0 又改了 `resume` 的工具默认值。分叉是**设计决定**（PR #3243 关闭、保持树外），不是疏忽。 |
| **「行为等价性可机械验证」** | **不成立（0.13.0）**：比较对象 `origin/feat/merge-dsh-interconnect` **已冻结、不再前进**；RELEASING.md 明写「此后对齐门禁**必然判红**，报的是分叉本身而不是漂移」，且「不要再按它的输出回补上游，也不要用它判断某一版是否发布」。对一条死 ref 验证等价性，证明不了当前行为。 |
| 「CI 不跑这道闸」 | **成立**：`ci.yml` 只有 clone DSH→构建→`pnpm run check` 五步（见 CI 节）。但真实原因是**它不可能在 CI 跑**：默认要 `~/dsh-wt-ic-merge` 这个本地 worktree + 私有上游分支，取不到 ref 就 exit 2，不给结论（[check-upstream-alignment.mjs:47-68](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/scripts/check-upstream-alignment.mjs#L47-L68)）。 |

**这条偏差的性质与现状**：原卡把一件「已退役的历史工具」写成了现在进行时的工程策略（「本域独一份」「可机械验证」）。机制描述没错，**时态错了**，而时态恰恰是这条卖点的全部价值。卡片原 `updated: 2026-10-31`，晚于作废声明 6 周，所以不是「当时为真」。**复核期间 L31 已按本节结论改写，但 L63 逐字保留了旧说法**——同一张卡现在既写「已作废、不能抄『与上游等价』的结论」（L31），又写「把『与上游行为等价』变成可机械检测的事」（L63）。L63 是本轮唯一未消解的重偏差。

**仍然成立的部分**值得保留：仓库确实有「把上游 diff 变成可机械搬运 + 可机械判定」的完整工具链，只是现在只能用于「核对某个旧 commit 是否与冻结 ref 逐字一致」（RELEASING.md 原话）。作为**方法**它是本仓最完整的一套工具链；作为**当前能力**它已经关掉。

### 12. subagent 封栏：谓词镜像与 Host 逐字相同

`isSessionOwnedBySubagent`（[index.ts:68-79](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L68-L79)）与宿主 `hasApiSessionSubagentOwner` 的实现**逐行相同**（见 SRC-DSH §3），两处使用：投递封栏（[index.ts:1022](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1022-L1022)）与列表过滤（[index.ts:903](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L903-L903)），两处口径一致——不会出现「list 列出来但 send 拒绝」的自相矛盾。

复制而非 import 的理由是**可验证的**：宿主 0.2.1-rc.3 的包根确实导出该函数（`dsh-api-session-controller/lib/types/agent.d.ts:76`），但插件注释说「the hosts this package is installed on still resolve the older root」，所以复制是跨版本兼容的选择。这是一个**已知的同步债**：Host 改规则时副本必须跟改，而没有任何机械检查会提醒——注释里自己写了「keep it in sync if the Host changes the rule, because this is a safety fence」。

## SRC-DSH

本机 `@deepseek-ai/dsh 0.2.1-rc.3`（`/Users/bowhead/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh`，依赖树内 `node_modules/@deepseek-ai/*`）。只读类型/编译产物，未运行宿主。

**1. inbox 三方法确实存在，且语义与卡片的投递模式表一一对应。** `Agent` 的 `send(message, target: InboxTarget, wakeup: boolean)` 加上三个特化：

- `followup(message)`：注释「Queue an ordinary follow-up turn and wake the driver. The item becomes the sole ordinary message of its own turn.」——`runtime-types.d.ts:187-192`。
- `steer(message)`：注释「Submit steering for the nearest step. An idle driver starts a turn; a running driver consumes it at its next step boundary.」——`runtime-types.d.ts:193-200`。
- `inject(message)`：注释「Queue model-facing context for the next pre-step **without waking the driver**… idle drivers leave it pending until follow-up or steering wakes them」——`runtime-types.d.ts:201-209`。

这与插件 README 的 `(inbox target, wakeup)` 三行表（`followup`=`next-turn`+wake、`steer`=`next-step`+wake、`inject`=`next-step`no-wake）完全一致。**插件对宿主契约的理解是准确的**，不是文档抄代码。

**2. 「inbox」是宿主的正式概念，splice 会持久化成 session 事件。** `dsh-agent` 的 `SessionEventMap` 有 `'agent/inbox/spliced'`，payload 是 `{ target: InboxTarget; start: number; removedCount?: number; inserted: UserMessage[]; outcome?: 'canceled' }`（`dsh-agent/lib/types/types.d.ts:86-94`）；该事件名同时登记在 `dsh-session/lib/types/known-event-types.js:23`。注释还写明「The session-projection registry applies the committed event before `Session.append()` returns」——**这就是「消息落到接收方 session log」的宿主机制**，也解释了 README 里「日志里只多一条 `agent/inbox/spliced`」的实测。

**3. `source` 不进模型上下文，在宿主类型层是明确的。** `MessageBase` 有两个并列字段：`content: readonly ContentBlock[]`（注释「**Exact model-facing blocks**」）与 `source: MessageSource`（注释「Required source fields supplied by the producer」+ `@persistenceSource user developer`）——`dsh-llm/lib/types/message.d.ts:126-134`。所以卡片 L26「`source` 与 `sender` 都不进模型上下文」**成立**：插件把对端文本放进 `content`、把发送方身份放进 `source.summary`，而宿主只把 `content` 当 model-facing。同理，接收方的**模型分辨不出**消息来自插件——README 自己把这一点写成了警告。

**4. 子代理归属谓词：插件副本与宿主逐字相同。** 宿主 `hasApiSessionSubagentOwner`（编译产物）：

```js
if (session.header.origin === "subagent") return true;
const parentId = session.header.parentSession;
if (parentId === void 0 || agent === void 0) return false;
const parent = ctx.agents.get(parentId);
return parent !== void 0 && ctx.agents.isOwnedBy(agent.id, parent);
```
（`dsh-api-session-controller/lib/index.js:128-134`；类型签名见同包 `lib/types/agent.d.ts:76`。`ctx.agents.isOwnedBy(id, owner)` 见 `dsh-agent/lib/types/index.d.ts:352`。）与插件 `index.ts:68-79` 逐行一致——**镜像没有漂移**（在本机这个宿主版本上）。

**5. `resume()` 的 owner 语义，插件说法成立。** 宿主同时提供 `sessionAgents.resume(ownerCtx: Context, options)` 与 `agent.resume(options)`（`dsh-agent/lib/types/index.d.ts:184`、`:286`）。「handle 由调用方 context 拥有」是该 API 形状的直接结果（第一个参数就是 `ownerCtx`），与插件注释「resume on the plugin fiber would tear the session down again the moment the plugin unloads」一致。

**6. 插件依赖的两个宿主 seam 都在。** `typert.lookups: TypertLookupRegistry`（`dsh-typert-protocol/lib/types/types.d.ts:781`）支持 `lookups.get('agent')`；`webServer.registerUpgrade(route: WebUpgradeRoute): () => void`（`dsh-host-webserver/lib/types/index.d.ts:181`）支持自持 upgrade 路由，且返回值可作 disposer——与插件 `ctx.effect(() => webCtx.webServer.registerUpgrade(upgrade), …)` 的用法吻合。

**7. 一处卡片表述需要宿主侧修正**：卡片 L52 的「装前 404、装后 6 秒内 403」是 README 的实测结论；从源码看 403 来自 token 未配置的 upgrade 拒绝（[index.ts:1120-1123](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1120-L1123)），**不是**「路由未挂载」。所以 403 恰好证明两件事同时成立：路由已注册 + token 未配。作为自检法是有效的，但把 403 当「装上了」的判据在**已配 token 的实例**上会变成 401——卡片没写这个前提。

## TEST

只核**存在性与覆盖面**，未运行、不证明通过。

4 个 spec 文件、`it(` 计数 **180**（`interconnect.host.spec.ts` 131、`tool-interconnect.spec.ts` 42、`skill-interconnect.spec.ts` 5、`release-consistency.spec.ts` 2）；README 写 179、CHANGELOG 0.13.0 写 180——`[DOC]` 内部不一致，实测数取 180（见 Provenance 注）。`vitest` 4.1.8，`pnpm test` = `vitest run`。

覆盖面对得上本 memo 的核对项：

| 核对项 | 有无测试 | 测试位置（示例） |
|---|---|---|
| 自动建链 + 投递 | 有 | `links a configured peer automatically and delivers a send over the link`（host spec:434） |
| 鉴权四路径 | 有 | `rejects an upgrade when no token is configured` / `…without an authorization header` / `…whose token differs only in one character` / `…multi-byte authorization header`（host spec:1269-1319） |
| token 后注入自愈 | 有 | `brings a token-less peer link up when the credential arrives later`（:1352） |
| 重连排程 | 有（弱） | `schedules reconnection when a peer link drops and answers sends unreachable`（:2252）——**只断言「排了」**，不断言 1/2/4/8/16/30s 序列，也测不到 jitter |
| 心跳 | 有 | `terminates sockets that stopped answering protocol pings and pings the rest`（:853） |
| 投递模式与 resume | 有 | `delivers with steer and inject modes…`（:896）、`refuses an inbound send to a not-live session unless resume is requested`（:931）、`refuses wake when the receiver does not allow it`（:942） |
| 失败原因分支 | 有 | `peer-not-configured`（:462）、`unreachable`（:475）、8 个 reason 的渲染（tool spec） |
| subagent 封栏 | 有 | `refuses delivery to a session reserved to subagent routing`（:1060）、`filters subagent-owned sessions`（:1190） |
| 事件去重 | 有 | `sends each lifecycle event once per peer, preferring the link this instance dials`（:797） |
| 配置键/自报 id 不一致 | 有 | `warns when a dialed peer announces an id other than its configured key`（:771） |
| 畸形/超大/二进制帧 | 有 | `warns and ignores malformed frames`（:1565）、`drops an oversized link frame before parsing it`（:1767）、`drops binary frames`（:1555） |
| 结果帧按 kind 绑定 | 有 | `answers undefined when a peer answers a list query with a ping-shaped result`（:2385）等 5 条 |
| 帧上限/行数上限 | 有 | `caps a list answer at the row limit`（:1576）、`bounds a list answer by the serialized bytes of its rows`（:1588） |
| 拆卸/生命周期 | 有 | `settles an in-flight send as unreachable when the service is disposed`（:2475） |
| **幂等** | **无（因为不存在）** | — |
| **离线队列** | **无（因为不存在）** | — |
| **跨版本互通 / 协议版本** | **无** | 只有「旧 peer 不带 sender 仍可投递」一条（:2338），没有版本协商测试 |

`release-consistency.spec.ts` 守的是发布记账：`dsh.plugin.json` 版本必须等于 `package.json`，`files` 必须含 `dsh.plugin.json` 与 `cordis.patch.yml`，`dsh.bundle.patch` 必须指向 `./cordis.patch.yml`。注释交代了来源：0.11.9 曾漏改 `dsh.plugin.json`，导致发布清单广告一个旧版本。**这是很值得抄的一条「发布一致性」小测试**——它把一次真实事故变成了回归。

测试的形态也值得记：大量用例跑在**真实 WS 回环**上（`describe('interconnect over real WS links')`），不是 mock；tool spec 有独立的 `describe` 覆盖渲染与取消（`raceSignal`）。README 声称「每个行为改动都配负例对照」，`v8 ignore` 注释在源码里也大量标注了不可达分支的理由——这种「解释为什么这段测不到」的纪律在插件仓里不常见。

## CI

只核存在性；**未取同 SHA check-run，故本 memo 不产 `[CI]` 证据**。

- 唯一 workflow：`.github/workflows/ci.yml`，51 行，`name: CI`；触发 `push: branches: [main]` 与 `pull_request`。
- 单 job `check`，`runs-on: ubuntu-latest`，6 步：checkout `deepseek-ai/deepseek-harness` 到 `dsh/`（sibling，因为 `link:../dsh/...` 的 devDependencies 必须在同一 workspace 内才能解析）→ checkout 本仓到 `plugin/` → Node 22 → pnpm 11 → 在 `dsh/` 里 `pnpm install --frozen-lockfile && pnpm run build:lib:host`（注释说明 DSH 的包未发布，必须先构建出可解析的类型与 `lib/index.js`）→ 在 `plugin/` 里 `pnpm install --config.auto-install-peers=false` → `pnpm run check`（[ci.yml:1-51](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/.github/workflows/ci.yml#L1-L51)）。
- **没有**：发布/publish workflow、release 资产、对齐闸步骤、矩阵、缓存、覆盖率上传。
- 所以卡片 L30 的「CI 不跑这道闸」**成立**；但更要紧的是它**跑不了**（需私有上游分支的本地 worktree，取不到 ref 就 exit 2）——见 §11。
- `[OPEN]`：pin commit `5547b03` 上的 CI 结论（success/failure）本轮未取。

## RUN

本轮实际执行过的、可复现的读操作：

1. `curl registry.npmjs.org/dsh-interconnect` → `dist-tags.latest`、41 个版本、0.13.0 的 `gitHead`/`shasum`/`fileCount`/`unpackedSize`、`time` 表。
2. `gh api`：`/repos`（★/fork/`pushed_at`/MIT/非 archive）、`/tags`（40 个，取 `v0.13.0` 与 `v0.11.24`）、`/branches`、`/commits/main`、`/releases`（**空**）。
3. `git clone` + `git checkout 5547b03466a5db4a3d69e25fc48fa07611e8cff6`，读 33 个文件的源码树；`git log`、`git log -S` 查 0.12.0 的存在。
4. `curl` npm 0.13.0 tarball（`sha256 ee2c9673…`），`tar tzf` 列 35 个文件；抽 `package.json`/`dsh.plugin.json`/`cordis.patch.yml` 三个清单与源码树 `diff`。
5. `api.npmjs.org/downloads/point/last-month` = 1017、`last-week` = 694。
6. 读本机 DSH 0.2.1-rc.3 发行包的类型与编译产物（`dsh-agent`、`dsh-llm`、`dsh-api-session-controller`、`dsh-typert-protocol`、`dsh-host-webserver`）。
7. 源码内 `grep`：`dedup|idempot|outbox|offline|queue|retry|replay`、`version|protocol|capabilit|negotiat`、`\b(task|lease|worktree)\b`（第三项零命中）。

**没有做**（按指令）：`pnpm install`/`build`/`test`、`dsh plugin add`、启动宿主、跑 `check-upstream-alignment.mjs`、取 CI check-runs。

## 与卡片的偏差

> 按指令**未改卡**。**口径**：复核期间卡片被并发修订（2026-11-01T04:43，66 行 → 67 行），修订涉及四处，与本 memo 的对应结论一致——拓扑「已配置对端 / 互配两条」、离线的两种含义 + `senders` 内存表、上游对齐闸「已退役」、以及新增 L19「证据链」pin（是否因读本 memo 而改，无法确证）。下表按**当前 67 行工作树版**核对，「修订状态」列标明哪些已对齐、哪些是残留。
> **修订自身引入的一个新问题**：L31 已改口为「历史工具，不是现状」，但 L63（可借鉴第 5 条）**仍写「把『与上游行为等价』变成可机械检测的事」**——同一张卡前后矛盾，L63 是未清理的残留。

| 卡片位置 / 主张 | 修订状态 | 复核结论 | 标签 | 依据 |
|---|---|---|---|---|
| **L63**（可借鉴第 5 条）「spec 与上游逐行同步 + 双遍对齐闸 + 机械 diff 搬运 —— 把『与上游行为等价』变成可机械检测的事」 | **残留，且与 L31 冲突** | **本轮最重的未消解偏差**。「逐行同步」与「等价性可机械检测」在 0.13.0 不成立：流程 2026-09-16 作废、上游 ref 冻结、2026-09-25 起本仓主动分叉，RELEASING.md 明写对齐闸此后「**必然判红**，报的是分叉本身而不是漂移」。L31 已正确改写，L63 未跟改，读者按「可借鉴」清单照抄会拿到一个已关闭的保证 | `[SRC-TARGET]`+`[DOC]` | [RELEASING.md:9-11](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/RELEASING.md#L9-L11)、[README.md:5](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L5-L5)、§11 |
| **L31**「工程策略是历史工具，不是现状…2026-09-16 已作废…2026-09-25 起与上游分叉…必然判红…CI 里也跑不了」 | **已对齐（本轮修订）** | **成立**，与 RELEASING.md 逐句对得上。补一处精度：脚本闸实为**七类**不变量（不止双遍）；「CI 跑不了」的真实机制是默认要 `~/dsh-wt-ic-merge` 这个本地 worktree + 私有上游分支，取不到 ref 就 exit 2 而不给结论 | `[SRC-TARGET]`+`[DOC]` | [RELEASING.md:9-11](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/RELEASING.md#L9-L11)、[RELEASING.md:21-30](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/RELEASING.md#L21-L30)、[check-upstream-alignment.mjs:47-68](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/scripts/check-upstream-alignment.mjs#L47-L68) |
| **L13 / L23**「每个**已配置**对端一条**拨号** WebSocket（互配的一对实例之间有两条）」 | **已对齐（本轮修订）** | **成立**，与源码完全一致：已配置对端数 = 拨号链数；互配一对 = 两条 socket（各拨一条）；单条 socket 双向，但 `send`/`ping`/`list` 只沿自己拨的链走 | `[SRC-TARGET]` | [index.ts:407-411](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L407-L411)、[index.ts:766-772](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L766-L772)、§1 |
| **L5 / L6** frontmatter「每个对端一条持久 WebSocket」「每对端一条持久 WS」 | **残留（未修订）** | 正文 L13/L23 已改成「已配置 / 两条」，但 frontmatter 的 `positioning` 与 `takeaway` 没跟改。这两行是索引与检索直接读到的口径，不一致最容易扩散——建议下次改卡时同步（本轮未改） | `[SRC-TARGET]` | §1、L13/L23 |
| **L25 / L59**「peers 键**是**对端自报的 `instanceId`」 | **残留（未修订）** | **半成立**：键是**操作者配置**的，服务从不把 `hello.sender` 写回键；不一致**只 warn 一次**，链路仍按配置键工作，代价是**事件重复**。应读作「键**应当**等于对端自报 id」 | `[SRC-TARGET]` | [index.ts:1224-1231](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1224-L1231)、§7 |
| **L25 / L59**「实际拨号 origin 才是线上寻址」「身份与地址不混用一个字段」 | 成立 | **成立**：`linkUrl(origin)` 是唯一拨号依据，`instanceId` 不参与拼地址；`types.ts` 明写「An origin is the ONLY routing authority」 | `[SRC-TARGET]` | [types.ts:344-350](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/types.ts#L344-L350)、[index.ts:1488-1499](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1488-L1499) |
| **L29**「无消息级幂等（`reqId` 只做关联，超时即删 pending，重试可能重复投递）」 | 成立 | **成立，逐字对得上**：每次新 `reqId`、无收端查重、超时 `delete` + reject → `unreachable`。补充：结果帧按 kind 绑定是**响应侧防串扰**，不是消息幂等 | `[SRC-TARGET]` | [index.ts:648](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L648-L648)、[index.ts:703-707](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L703-L707)、§6 |
| **L29**「无离线队列（链路断即 `unreachable`，不缓存；**事件也不补发**）；要区分『离线』的两种含义…本机还有一张内存 `senders` 表…重启即丢」 | **已对齐（本轮修订）** | **成立，且补齐了原卡两处漏写**：事件确实不补发（`broadcast` 跳过非 OPEN socket）；`senders` 确实是 `reply` 的唯一依据、重启即 `no-sender-known` | `[SRC-TARGET]` | [index.ts:647](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L647-L647)、[index.ts:779-790](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L779-L790)、[index.ts:570-574](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L570-L574)、§5、§9 |
| **L27**「`send` = 投 inbox 并调 `agent.followup/steer/inject`」 | 成立 | **成立**：`createUserMessage` + 三方法穷尽 switch；inbox splice 由宿主完成（`agent/inbox/spliced`） | `[SRC-TARGET]`+`[SRC-DSH]` | [index.ts:1044-1071](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1044-L1071)、SRC-DSH §1-2 |
| **L27**「`event` = 只做本地 `ctx.parallel('interconnect/event')` 分发，不进会话」 | 成立 | **成立**：`receiveEvent` 不碰 session；用 `parallel` 而非 `emit` 有注释说明理由；入站事件不再广播（不回环） | `[SRC-TARGET]` | [index.ts:842-863](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L842-L863) |
| **L27**「`source` 与 `sender` 都**不进模型上下文**」 | 成立 | **成立**：插件只把对端文本放进 `content`；宿主 `MessageBase` 把 `content` 标为「Exact model-facing blocks」、`source` 标为 `@persistenceSource`。后果是接收方**模型分辨不出**消息来自插件（README 自己也这么警告） | `[SRC-TARGET]`+`[SRC-DSH]` | [index.ts:1044-1053](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1044-L1053)、SRC-DSH §3 |
| **L25**「子代理拥有的会话被显式过滤掉」/「没有任务、没有租约、没有 worktree」 | 成立 | **成立**：投递封栏 + 列表过滤两处同口径；谓词与宿主 `hasApiSessionSubagentOwner` **逐行相同**（本机版本）。`src/` 全仓 `grep -iE '\b(task\|lease\|worktree)\b'` 零命中。代价是**同步债**：Host 改规则时副本必须跟改，无机械检查提醒 | `[SRC-TARGET]`+`[SRC-DSH]` | [index.ts:68-79](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L68-L79)、[index.ts:903](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L903-L903)、SRC-DSH §4 |
| **L37** 三笔税表「状态归属 = 对端实例的 session inbox…本机 `senders` 内存表重启即丢」 | **已对齐（本轮修订）** | **成立**：原表没提 `senders`，修订后已补 | `[SRC-TARGET]` | [index.ts:383](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L383-L383)、§9 |
| **L39**「30s 心跳 + `min(30s, 1s·2^n)` 退避」 | 成立 | **成立**：公式与 30s 心跳都对。补充三个没写的量：**无 jitter**（同时掉线会同步重连）、CONNECTING 有 **10s** 握手超时（否则永远不 open 也不 close）、心跳检测窗 **30–60s** | `[SRC-TARGET]` | [index.ts:1455-1462](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1455-L1462)、[index.ts:1392](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1392-L1392)、[index.ts:455-469](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L455-L469) |
| **L38**「冲突裁决 不适用」 | 成立 | **成立**：无共享工作区、无租约、无任务；冲突面只剩「同一 session 两个发送方」这类语义问题，由 `senders` 的后写覆盖处理（后到的不带 sender 会**清空**旧记录） | `[SRC-TARGET]` | §9、[index.ts:1076-1084](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1076-L1084) |
| **L61**「token 校验 fail-closed 403，先 sha256 归一再用 `timingSafeEqual`」 | 成立 | **成立，细节全对**；补：**401 vs 403 是两条不同的理由**（403 = token 未配置/读取失败，401 = header 缺失或不匹配），disposed 时是 503 | `[SRC-TARGET]` | [index.ts:1107-1140](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1107-L1140)、[index.ts:1466-1474](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1466-L1474) |
| **缺项（L13 / L25 之间）**：配对只到共享密钥 | **两轮修订后仍缺** | 一把密钥覆盖整个 mesh：**无 per-peer 密钥、无 peer id 白名单、自报 id 不经认证绑定**；任何持同一 token 的实例可收全量事件、可向任意已知 `sessionId` 投递。这是**部署决策级**信息（能不能用在互不完全信任的几台机器上），不是实现细节 | `[SRC-TARGET]` | §3 |
| **缺项（L13 / L27 之间）**：协议无版本 | **两轮修订后仍缺** | `hello` 只有 `sender`，全仓无 `version`/`capabilities`；不匹配统一表现为「帧被丢 → 超时 → `unreachable`」，调用方分不出「版本旧」与「对端挂」。兼容只靠「只加可选字段、缺省语义不变」 | `[SRC-TARGET]` | [index.ts:340-347](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L340-L347)、§10 |
| **L29**「session 不 live 可被 `resume` 唤醒」 | 成立（措辞偏弱） | **成立，但比卡片写的更强**：0.13.0 起**工具默认 `resume: true`**（`args.resume ?? true`），不再是 opt-in；代价是唤醒即起一个**计费回合**。卡片读起来像可选项，实为默认行为 | `[SRC-TARGET]` | [tool-interconnect/index.ts:203](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/tool-interconnect/index.ts#L203-L203)、[CHANGELOG.md:5-43](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/CHANGELOG.md#L5-L43) |
| **L19**「证据链：npm 0.13.0 ↔ tag `v0.13.0` ↔ commit `5547b03`…见 08 源码复核」 | **已补（本轮修订）** | **成立**：与 Provenance 三处对齐一致（`gitHead` / tag / `main` HEAD 同一 SHA）；memo 相对路径 `../_证据/08-interconnect-源码复核.md` 正确。这也补上了 `EVIDENCE.md` §2.2 要求的「证据链」一行 | API | Provenance |
| **L47**「版本（本次读）= `0.13.0`」 | **部分残留** | L19 已带 pin，但「精确坐标」**表内**仍只有版本号。`EVIDENCE.md` §2.1 要求坐标可复现，建议把 commit/tag 也写进这张表（本轮未改卡） | `[OBS]`（规程） | [`EVIDENCE.md:31-35`](../../EVIDENCE.md) |
| **L47-54** 版本/License/下载/安装/接线/复现要点 | 成立 | 全部核对通过：`0.13.0` ✓、MIT ✓、`last-month` 1017（窗口 2026-09-30→10-29，未覆盖到采样日 10-31）✓、`38★/3 fork` ✓、安装命令 ✓、`cordis.patch.yml` 三个 `insert` 行 ✓、tarball 35 文件含 `lib`+`lib/types` 且 `scripts` 无 `prepare`/`postinstall` ✓ | API+`[SRC-TARGET]` | Provenance、[cordis.patch.yml:1-15](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/cordis.patch.yml#L1-L15) |
| **L53**「装前 `GET /interconnect/link` → 404；装后 6 秒内 → 403」 | 成立但未复现 | 文档与源码一致：403 确是 token 未配置时的 upgrade 拒绝。**注意前提**：已配 token 的实例会回 **401** 而不是 403，卡片未写。「6 秒」「404」是作者实测，本轮未复现 | `[DOC]`+`[OBS]` | [index.ts:1120-1123](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/src/interconnect/index.ts#L1120-L1123)、[README.md:281-283](https://github.com/Chinesezjc/dsh-interconnect/blob/5547b03466a5db4a3d69e25fc48fa07611e8cff6/README.md#L281-L283) |
| **L67**「没有 message-id 幂等就不要重试；没有离线队列就不要承诺消息不会丢；更别说成跨机派活」 | 成立 | **成立且是最该保留的一条**：确无任务/租约/worktree；两条空洞经代码确认 | `[SRC-TARGET]` | §5-§6、§9 |
| **L14**「证据级别 `observed`（源码逐文件读过）」 | 可升级 | 本 memo 已把关键机制 pin 到固定 commit 的行号，达到 `[SRC-TARGET]` 强度；卡片的证据级别可以据此上调（本轮未改卡） | — | 本 memo 全文 |
| **L47** 版本序列 | 卡片未写 | `0.12.0` 存在于 CHANGELOG 与 git 历史（`package.json` 曾为 0.12.0），**从未发布到 npm、也没有 `v0.12.0` tag**；npm 上 `0.11.24 → 0.13.0` 有个洞 | `[SRC-TARGET]` | Provenance §3 |

## `[OPEN]`

1. **CI 在同一 SHA 上的结论**：按指令只核存在性，未取 `5547b03` 的 check-runs。`[CI]` 证据为空。
2. **对齐闸在 `5547b03` 的实际输出**：需私有上游仓的 `~/dsh-wt-ic-merge` worktree + 冻结 ref；本轮未运行。按 RELEASING.md 自述**预期判红**（分叉本身），但「红在哪几个文件」未取证。
3. **发布物字节一致性**：只比对了 tarball 的文件清单与 3 个清单文件；`lib/*.js` 是否等于该 commit 的 esbuild 产物**未验证**（构建需 esbuild，按指令未跑）。
4. **`resume` 唤醒的计费回合**：README/CHANGELOG 自述实测（`wakeDriver() → kick() → turn() → llm.stream()`），本轮未复现；「一次完整回合」的具体 token 成本未量化。
5. **共享 token 下的横向移动面**：代码可读出「任何持 token 者可收全量事件、可向任意已知 `sessionId` 投递」，但真实部署里 token 的分发范围、隧道暴露面未测。这是**性质已知、暴露程度未知**。
6. **无 jitter 的重连风暴**：代码可读出，多实例同时掉线时的行为未实测。
7. **0.12.0 为何从未发布**：CHANGELOG 有整节、git 历史有 `"version": "0.12.0"`，但 npm 无此版本、仓库无 `v0.12.0` tag，原因未见记录。
8. **跨版本对端兼容矩阵**：`msgResultSchema` 的 reason 词表与 `linkFrameSchema` 的帧词表各版本是否一致，未做跨版本比对（只有一条「旧 peer 不带 sender」测试）。
9. **两台机器实测双向互通**：README 自述已测（含真实 WS 事件推流与工具反向回发），本轮未复现，保留为 `[DOC]`。
