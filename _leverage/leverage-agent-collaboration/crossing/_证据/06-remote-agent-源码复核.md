---
title: "06 · zbzbhs/dsh-remote-agent 源码复核"
domain: agent-crossing
kind: evidence
positioning: "对 dsh-remote-agent 0.9.11（commit cc356e1）的固定提交复核：双角色与副机本地 agent 循环成立，凭证只在协议层不出机；npm 已到 0.9.12 且无 v0.9.11 tag。"
read_when: "核对 06 卡的双角色、凭证边界、拓扑、断链与版本 pin。"
status: observed
updated: 2026-11-01
---

# 06 · `zbzbhs/dsh-remote-agent` 源码复核

> 复核对象：样本卡 [`06-zbzbhs-dsh-remote-agent.md`](../samples/06-zbzbhs-dsh-remote-agent.md)。
> 取证时点 2026-11-01。只读 GitHub REST（部分被限流）、`registry.npmjs.org`、`codeload` tarball 与本机 `@deepseek-ai/dsh 0.2.1-rc.3` 发行包；**未安装、未构建、未跑 `npm test`、未启动 hub/worker/relay**。标签沿用 [`EVIDENCE.md`](../../EVIDENCE.md)：`[DOC]` 目标仓 README/SECURITY/CHANGELOG 主张，`[SRC-TARGET]` 固定 commit 实现，`[SRC-DSH]` 本机 DSH 发行包，`[TEST]` 测试源码，`[CI]` 同 SHA check-run，`[RUN]` 本轮实跑，`[OBS]` 判断。
> **主 pin**：commit [`cc356e11dfe435a755459e3e07420a49ea506317`](https://github.com/zbzbhs/dsh-remote-agent/commit/cc356e11dfe435a755459e3e07420a49ea506317)（2026-10-21T06:28:08Z，`fix: agent 任务假成功 —— ok 必须排除 hadError（0.9.11）`，父提交 `4bcdfa3`；`package.json` 自述 `0.9.11`）。该 commit 的树与 `main` HEAD 的树**逐字节相同**（两棵 codeload tarball `diff -rq` 无输出）。下文目标代码链接全部 pin `cc356e1`。
> 一句话结论：**「一个包双角色」与「副机本地跑完整 agent 循环」都成立，且实现比卡片写的更细（两种后端）**；但「凭证永不出机」只成立于**协议层**——hub 侧拿到的是副机 shell（`mode:exec`），能不能读到凭证取决于你信不信 hub，这正是作者自己在 SECURITY 里写的信任假设。版本侧：`0.9.11` 可复现（gitHead 对齐），但**没有任何 tag 钉它**，且 npm `latest` 已经是 `0.9.12`（同一棵树、只改了版本串）。

## Provenance

| 项 | 值 | 核对方式 |
|---|---|---|
| 仓库 | [`zbzbhs/dsh-remote-agent`](https://github.com/zbzbhs/dsh-remote-agent)（repo id `1416741285`，创建 2026-10-13，MIT，**4★** / 1 fork / 1 open issue @2026-11-01；`pushed_at` 2026-10-21T06:28:25Z） | `/repos` |
| **主 pin** | `main` @ [`cc356e1`](https://github.com/zbzbhs/dsh-remote-agent/commit/cc356e11dfe435a755459e3e07420a49ea506317)（2026-10-21T06:28:08Z，父 `4bcdfa3` = tag `v0.9.10`） | `/commits/cc356e1` |
| **HEAD 对齐** | `main` 树的 tarball 与 `cc356e1` 树的 tarball 解包后 `diff -rq` **无差异** → 主 pin 就是 HEAD，不存在「pin 落后于 HEAD」 | codeload ×2 |
| package.json 版本 | **`0.9.11`**（[package.json:3](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/package.json#L3-L3)）；`main: ./lib/index.js`（[:45](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/package.json#L45-L45)）；`type: module`，**无构建步骤** | tarball |
| **npm 发布物** | `0.9.11` 发布 2026-10-21T06:29:41Z，`gitHead = cc356e1…`；`0.9.12` 发布 2026-10-21T06:31:08Z（**87 秒后**），`gitHead` **完全相同**；`dist-tags.latest = 0.9.12`；共 23 个版本（含 `0.0.0-stage`） | registry |
| **tag 列表** | **17 个** tag，最高为 `v0.9.10` → `4bcdfa3`；**没有 `v0.9.11`、也没有 `v0.9.12`**（同样缺 `v0.4.1`、`v0.4.2`、`v0.4.3`、`v0.8.0`、`v0.9.8`——即并非每个 npm 版本都打 tag） | `/tags?per_page=100` |
| **npm 0.9.11 ≠ git 树？** | 共享 82 个文件，**4 个字节不同**：`lib/hub/ui-routes.js` 与 3 篇 `docs/verification-*.md`——差异**全部是 CRLF/LF 行尾**，`tr -d '\r'` 后 sha 一致 → **语义相同，仅换行归一** | tarball 逐文件 `cmp` |
| **0.9.12 是什么** | 与 0.9.11 的 tarball 逐文件比对，**只有 `package.json` 的 version 不同**（`0.9.11`→`0.9.12`）→ 从**未提交的工作树**重发的版本号，git 里没有任何 commit 的 `version` 是 `0.9.12` | tarball diff |
| 签名 | `verification = {verified:false, reason:"unsigned"}` | `/commits/cc356e1` |
| 卡片版本核对 | 卡片 L48 写 `0.9.11`：**能对上** commit 与 npm 0.9.11（gitHead 一致），但 **pin 不到 tag**（不存在），且**不是 npm `latest`** | 上述 |

**错位结论（这是本卡最实的坐标问题）**：`npm ↔ tag ↔ commit` 三坐标里只有两环成立。`0.9.11` 与 `cc356e1` 是同一棵树（gitHead 自证、内容仅 CRLF 差异），但**仓库从未给 0.9.11 打 tag**——最高 tag 停在 `v0.9.10`。同时 npm `latest` 已推进到 `0.9.12`，而 `0.9.12` 不是任何 commit：它等于 `cc356e1` 的树 + 一个未提交的版本号。因此：

- 想复现卡片的 `0.9.11`：**必须用 commit `cc356e1`，不能靠 tag，也不能靠 `npm i dsh-remote-agent`**（今天装到的是 0.9.12）；
- 0.9.12 与 0.9.11 **行为等价**（只差版本串），所以「装 latest 得到不同行为」的风险在这一对上是零——但这只是巧合，不构成 pin 纪律。

## DOC

`[DOC]` 只证明作者主张，不证明实现。

- 定位自述：「副机拥有自己的 DSH 与独立 Agent 循环，任务在它本地持久运行；主电脑只拿到 **handoff 结果卡**与**产物清单**，成品要显式拉取才过河」——[README.md:12-13](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/README.md#L12-L13)。**注意同页架构图把「DSH · 模型 · 会话日志 · 全部凭证」画在 hub 框里**（[README.md:17](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/README.md#L17-L17)）——即作者从未声称「只有副机有凭证」，声称的是「凭证不过线」。
- 凭证主张原文出现两次：「**凭证不离开副机** | 协议里不带任何模型 key；副机用自己的模型配置跑自己的循环」——[README.md:181](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/README.md#L181-L181)、[README.md:271](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/README.md#L271-L271)。
- **信任假设是作者自己写死的**（这是全仓最重要的一段，卡片没引）：「主机是可信的 — 主机能派任意任务给副机。**不要把副机接到你不信任的主机。**」「副机是可信的 — 副机上报的 handoff 会进主机的模型上下文。」「传输通道可能被窃听 — `direct` 模式的默认配置是**明文 ws://**」「中继机器是可信的（用 relay 时）……它可以扣下握手帧让链路退回明文」——[SECURITY.md:43-46](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/SECURITY.md#L43-L46)。
- 「可用性边界（**不是安全边界**）：中继挂了任务照跑……链路断不影响已派任务的完成，只影响『此刻能否派新的』」——[SECURITY.md:49](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/SECURITY.md#L49-L49)。这句话几乎就是卡片「降级为信任问题」的原文出处。
- 明列**不做**的三件事：「不隔离副机的文件系统 —— 安全边界是 `roots` 配置，不是沙箱」「**不限制副机能执行的命令 —— `mode: exec` 直接跑 shell**」「不校验副机的身份（默认 `nodeToken` 为空）」——[SECURITY.md:54-56](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/SECURITY.md#L54-L56)。
- 认证默认值：「`direct` 模式下，主机侧的 `nodeToken` 为空时**不校验任何凭证** —— 任何能连到 `hubUrl` 的人都能注册成节点并接收任务」——[SECURITY.md:64](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/SECURITY.md#L64-L64)。
- 配对码定位：「配对码 `dshra1://…` 内含 `nodeToken`。**它能注册一台新副机 —— 谁拿到它，谁就能接入你的主机。**」「面板『副机接入』生成的配对码有披露边界：**含 token 的完整码只回本机回环请求**」——[SECURITY.md:131-139](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/SECURITY.md#L131-L139)、[README.md:381](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/README.md#L381-L381)。
- 安装串：`dsh plugin add github:zbzbhs/dsh-remote-agent`（[README.md:286](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/README.md#L286-L286)）、`npm install -g dsh-remote-agent`（[README.md:289](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/README.md#L289-L289)）——与卡片 L51 一致。
- 「零外部运行时依赖」：「`npm install` # 只为验证 lockfile；本包零外部运行时依赖」——[README.md:629](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/README.md#L629-L629)。**这是 `[DOC]`，且与两处实现矛盾，见偏差表**。
- `[DOC]` 从未声称「副机能独立验证主机完成情况」，也没声称「链路断了 hub 能知道任务是否真成功」——卡片 L40 的代价是**卡片自己的判断**，不是作者原话。

## SRC-TARGET

### 1. 双角色：一个包，两个入口

| 主张 | 结论 | 依据（`cc356e1`） |
|---|---|---|
| 一个包承载两个角色 | **成立** | `exports` 同时暴露 `./hub` 与 `./worker`（[package.json:31-35](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/package.json#L31-L35)），入口按 `role` 分发 |
| 角色取值 | `hub` / `worker` / `both` / `auto` | `ROLE` 冻结对象（[lib/index.js:31](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/index.js#L31-L31)） |
| `both` 的含义 | **同一台机器同时当 hub 与 worker**（自测） | 两个分支都会执行（[lib/index.js:312](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/index.js#L312-L312)、[:334](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/index.js#L334-L334)） |
| `auto` 的判据 | **配了 `hubUrl` → worker；没配 → hub** | 只有这一条判据（[lib/index.js:86-93](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/index.js#L86-L93)） |
| 未配置/非法值 | **什么都不注册**，面板显示引导；不静默回退 hub | `unconfigured` 分支（[lib/index.js:68-101](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/index.js#L68-L101)、[lib/index.js:192-214](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/index.js#L192-L214)） |
| worker 分支的加载方式 | **动态 import**：hub 进程不加载任务引擎/进程管理/文件遍历，worker 进程不加载 hub 注册表 | 文件头注释（[lib/index.js:1-25](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/index.js#L1-L25)） |

**命名校正**：仓库的词汇是 **hub / worker**，代码里没有 `master`/`secondary` 标识符；卡片用的「主机/副机」与之一一对应，本轮任务描述里的「master/secondary」是同一对象的别名，不构成偏差。

**为什么 hub 不用模块级 `export const inject`**：声明式 inject 是模块级的，副机 profile 没有 `webServer`，整插件会被 hub 的依赖拖死；所以 hub 侧改用作用域 `ctx.inject([...], cb)`，worker 侧走动态 import（[lib/index.js:10-25](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/index.js#L10-L25)）。这是「一个包两角色」能成立的具体机关。

### 2. 副机的 agent 循环：不是「一条命令」，是两种真后端

卡片说「副机本地跑完整 DSH 与完整 Agent 循环」——**成立，但卡片省略了后端二选一**。

| 后端 | 触发条件 | 实际做什么 | 依据 |
|---|---|---|---|
| **in-process**（首选） | worker 插件跑在副机 DSH 进程里，且 `ctx.get('agentLoop')` 与 `ctx.get('sessions')` 都在 | `ctx.agentLoop.createAgent(ctx, { sessionId, meta:{cwd}, signal, agentOptions })` 起一个**新会话**（`session-remote-<taskId>`），`agent.followup({...})` 投任务书，`agent.whenIdle()` 等停稳，`handle.dispose()` 收尾 | [lib/node/runner.js:406-410](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/runner.js#L406-L410)、[:572](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/runner.js#L572-L572)、[:685-691](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/runner.js#L685-L691)、[:797](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/runner.js#L797-L797)、[:804](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/runner.js#L804-L804) |
| **headless**（回退） | 没有 DSH 上下文，或上述服务探测失败 | `spawn(dshBin, ['headless','--json', …, '-'])`，任务书写进 **stdin**，解析 NDJSON 事件流取最终回答 | [lib/node/runner.js:130-135](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/runner.js#L130-L135)、[:211](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/runner.js#L211-L211)、[:218-230](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/runner.js#L218-L230) |
| 选择器 | `selectRunner()` | `preferHeadless` / profile / dshBin 参与判断 | [lib/node/runner.js:916](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/runner.js#L916-L916) |

**三个卡片没写的边界**：

1. **in-process 的「完整」是有前提的**：探测不到 `agentLoop`/`sessions` 时返回 `unavailable: true`，不是报错，而是让上层退回 headless（[lib/node/runner.js:458-467](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/runner.js#L458-L467)）。worker profile 的注释也明说「缺 agentLoop 时自动降级到 headless 后端」——[profiles/worker.cordis.yml:13](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/profiles/worker.cordis.yml#L13-L13)。
2. **headless 不能指定模型**：`dsh headless` 固定用副机默认模型，host 指定 `{provider,model}` 时**派发前就报错**，不静默忽略（[lib/node/runner.js:155-171](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/runner.js#L155-L171)、[README.md:450](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/README.md#L450-L450)）。所以「副机能用主机指定的模型」只在 in-process 后端成立。
3. **任务书是副机自己包的**：`buildTaskBrief(rec)` 在 **worker 侧**生成多行 Markdown（「你正在一台独立机器上执行一条由远程同事派发的任务……成品留在工作区」），再由 `runner.run({ goal: buildTaskBrief(rec) })` 投递（[lib/node/task-engine.js:672-706](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/task-engine.js#L672-L706)、[:387](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/task-engine.js#L387-L387)）——卡片的「副机把 goal 包成自带上下文的任务书」逐字成立。

**「它其实不派子代理」**：`subagent-provider` 只让主机侧的委派工具把任务投到远端；`capabilities` 五项全 false、`inheritsParentContext: false`（[lib/hub/subagent-provider.js:218-225](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/subagent-provider.js#L218-L225)、[:10](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/subagent-provider.js#L10-L10)）。远端跑的是**副机自己的 agent**，不是主机的 DSH 子代理——卡片这句判断成立，但能力对象的**键名与宿主契约不一致**，见 §SRC-DSH。

### 3. 凭证边界：「不走协议」成立，「到达不了 hub」不成立

- **协议里确实没有密钥材料**：模型选择被收敛成 `{ provider?, model, reasoningEffort? }`，逐字段白名单、长度截断，**没有 key 字段**（[lib/protocol.js:367-403](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/protocol.js#L367-L403)）；`remote_task` 的 `model` 参数说明也写「只传**选择**、不传凭证」——[lib/hub/tools.js:524-526](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/tools.js#L524-L526)。全仓 `lib/` 内没有任何 API key / Authorization 的构造或转发。
- **副机侧凭证只在本机进程内使用**：headless 后端 `spawn(..., { env: { ...process.env } })`（[lib/node/exec.js:401](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/exec.js#L401-L401)），in-process 直接复用副机 DSH 的模型配置——两者都**不经过 ws 帧**。
- **但 hub 拿到了副机的 shell**：`remote_task` 的 `mode` 是 `agent|exec`（[lib/hub/tools.js:519-520](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/tools.js#L519-L520)），`exec` 路径直接跑 shell，`roots`/`denyPaths` 只约束**文件工具**，不约束命令能读什么（[lib/node/index.js:574-581](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/index.js#L574-L581)、[SECURITY.md:55](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/SECURITY.md#L55-L55)）。所以「凭证永不出机」在**被信任的 hub 不主动去取**的前提下成立。
- **唯一的软化是审批默认值**：`mode:exec` 缺省 `approval = 'manual'`（agent 缺省 `auto`），即 exec 任务默认挂起等面板批准、超时 fail-closed（[lib/protocol.js:436-438](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/protocol.js#L436-L438)）。这挡得住「普通 hub agent 顺手 exec」，**挡不住被攻陷的 hub**（审批是 hub 侧自己的闸）。
- **读文件面另有边界**：`remote_ls/read/grep/tree` 只读、限 `roots`、`denyPaths` 里**永远追加 stateDir**（[lib/node/index.js:574-577](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/index.js#L574-L577)）；默认 roots 是 `~/dsh-remote-work` 或 `~/work`（[lib/node/exec.js:524-536](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/exec.js#L524-L536)），凭证目录通常不在内——但 `mode:exec` 绕过这层。

**结论**：卡片的「凭证永不出机」应读作「**插件不要求凭证过线**」，不能读作「**hub 拿不到凭证**」。作者自己的措辞是前者（SECURITY:200-203），且把「不要把副机接到你不信任的主机」写成了硬前提（SECURITY:43）。

### 4. 传输与拓扑：谁监听、谁拨号、几条入站面

| 问题 | 事实 | 依据 |
|---|---|---|
| **谁监听** | **hub** 自己起一个 `node:http` server（不挂在 DSH webServer 上），默认端口 **19387**，只处理 `GET <healthPath>` 与精确匹配路径的 WS upgrade，其它一律 404 | [lib/listen-server.js:61](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/listen-server.js#L61-L61)、[:230-270](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/listen-server.js#L230-L270)、[:292](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/listen-server.js#L292-L292) |
| **绑哪个地址** | 用户 `listenHost` → Tailscale `100.64/10` → 私网 → 任意非回环 → 回环；**永不通配**，`0.0.0.0`/`::` 被忽略 | [lib/listen-server.js:149-172](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/listen-server.js#L149-L172) |
| **谁拨号** | **worker** 主动连 hub（direct）；relay 模式下 hub 与 worker **都拨中继**（默认 `8890`） | [lib/relay.js:1-18](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/relay.js#L1-L18)、[lib/relay.js:82](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/relay.js#L82-L82) |
| **第二条入站面** | hub **同时**在 DSH 的 `webServer` 上注册同路径 `registerUpgrade`（回退通道）；两条路径各自做 token 校验，「少一处就是无鉴权入口」 | [lib/hub/index.js:706-724](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/index.js#L706-L724)、[:618-634](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/index.js#L618-L634) |
| **第三条入站面** | hub 的 **Web 面板**路由（`kind:'exact'`，绕过 DSH 的 `/api` prefix 围栏，故自己重放 `connection.requestRejection` + 同源检查，失败关闭） | [lib/hub/ui-routes.js:195-241](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/ui-routes.js#L195-L241)、[:408-409](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/ui-routes.js#L408-L409) |
| **relay 的定位** | 纯转发：登记 hub / 登记 node / 按 `nodeId` 投递；**不缓冲离线消息、不解析业务帧、不持久化任务** | [lib/relay.js:1-18](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/relay.js#L1-L18) |
| **relay 加密** | X25519（一次性密钥）→ HKDF-SHA256 → **AES-256-GCM**；信封 `t/id/to/from` 保持明文供路由；ed25519 hub 身份签 X25519 公钥 | [lib/e2e.js:19-45](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/e2e.js#L19-L45)、[:83](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/e2e.js#L83-L83)、[:178](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/e2e.js#L178-L178)、[:258-272](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/e2e.js#L258-L272) |
| **哪些帧必须加密** | 下行 `task/start`、`task/cancel`、`artifact/*`、`fs/req`、`share/req` 在加密会话里明文出现 = **拒收**；`welcome`/`hub/identity`/`error`/`ping`/`hub/e2e` 永远明文 | [lib/node/transport.js:58-84](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/transport.js#L58-L84) |
| **已知降级漏洞** | **恶意中继扣下 node/e2e 握手帧可让链路退回明文**，副机只打警告；作者自己列为 v1 已知局限 | [lib/e2e.js:36-40](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/e2e.js#L36-L40)、[SECURITY.md:46](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/SECURITY.md#L46-L46) |

**卡片 L28 的「relay = VPS 纯转发 + 业务帧 X25519→HKDF→AES-256-GCM（信封明文供路由）」逐项成立**，但卡片**没写**这条：加密可被主动降级，direct 模式默认还是明文 `ws://`。

### 5. 配对与认证：`dshra1://` 是配置串，不是凭证校验器

- **格式**：`dshra1://` + `base64url(JSON)`；载荷白名单 **恰好 7 个字段** `v / transportMode / hubUrl / relayUrl / token / nodeId / hubFingerprint`（[lib/pairing.js:26](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/pairing.js#L26-L26)），`v` 固定 1，其余可选。**卡片说「7 字段配置打包串」，准确。**
- **不过期**：载荷里**没有时间戳/有效期字段**，也没有签名或 MAC——它就是一串可被任意伪造/改写的明文 base64。**卡片说「不过期、不核验」，准确**（`decodePairCode` 只校验结构、版本、白名单，不校验来源——[lib/pairing.js:96-130](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/pairing.js#L96-L130)）。
- **它里面确实有 token**：`token` 是白名单字段，作者明写「配对码里含 token，等同凭证」（[lib/pairing.js:14-22](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/pairing.js#L14-L22)）。
- **真正的认证是三层**：
  1. **`x-dsh-token` 共享口令**（`nodeToken`），两条入站通道都在 upgrade 时用**恒定时间比较**校验（[lib/hub/index.js:510](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/index.js#L510-L510)、[:624-628](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/index.js#L624-L628)、[:711-716](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/index.js#L711-L716)）。
  2. **空 token 的降险策略**：`nodeToken` 默认为空串（[lib/index.js:423-426](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/index.js#L423-L426)）；为空且**未显式指定非回环 `listenHost`** 时，强制绑 **`127.0.0.1`**（`source: 'loopback-no-token'`）——[lib/hub/index.js:578-586](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/index.js#L578-L586)。**所以「默认不校验」的真实暴露面是回环**；只有用户显式把 `listenHost` 写成非回环又留空 token 才会网络裸奔（此时代码会 warn）。**卡片与 SECURITY 都只写了「不校验」，没写这层回环兜底。**
  3. **hub → 副机的反向认证**：hub 持久 ed25519 身份，指纹 `hubfp1-` + base64url(sha256(SPKI)[0:16])（22 字符），签名绑 nonce + 时间戳（容差 5 分钟）；副机首连 TOFU 钉到 `<stateDir>/hub-pin.json`（0600 原子写），之后不匹配即拒绝（[lib/identity.js:1-45](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/identity.js#L1-L45)、[:45](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/identity.js#L45-L45)、[:55](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/identity.js#L55-L55)、[lib/node/hub-pin.js:4-11](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/hub-pin.js#L4-L11)）。指纹**经配对码分发**——这是配对码唯一的「安全用途」。
- **卡片 L28 的「真正的长期凭证是 `nodeToken` 与 hub 的 ed25519 身份 + TOFU pin」成立**；补一句：TOFU 防不了首连被截和，作者也这么写（SECURITY:46）。

### 6. 离线 / 断链：任务根本不知道链路状态

| 项 | 值 | 依据 |
|---|---|---|
| 心跳 | **15 s** 发 `conn.ping()` + 业务 `ping` | [lib/node/transport.js:36](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/transport.js#L36-L36)、[:715-722](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/transport.js#L715-L722) |
| 超时 | 最后 pong 超过 **45 s** → `heartbeat timeout`，强制重连 | [lib/node/transport.js:37](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/transport.js#L37-L37)、[:715-717](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/transport.js#L715-L717) |
| 握手超时 | 10 s | [lib/node/transport.js:46](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/transport.js#L46-L46) |
| 退避 | **1 s → 30 s** 指数，叠加 **0–20 % 抖动** | [lib/node/transport.js:34-35](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/transport.js#L34-L35)、[:736-738](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/transport.js#L736-L738) |
| 断链时任务 | **不中断**：执行路径一个字节都不读连接状态；`send()` 包成永不抛、失败即丢帧 | [lib/node/index.js:13-21](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/index.js#L13-L21) |
| 重连后 | worker 主动 `engine.syncAll()` 全量上报，hub 重建投影 | [lib/node/index.js:21](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/index.js#L21-L21)、[:881](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/index.js#L881-L881) |
| relay 断链 | 不缓冲；重连靠 node 自己 sync | [lib/relay.js:9-13](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/relay.js#L9-L13) |
| 启动是否被 hub 拖住 | **否**：`applyWorker` 全程同步，没有顶层 await 网络；定时器全 unref | [lib/node/index.js:10-12](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/index.js#L10-L12) |

**卡片「链路断不影响正在跑的工作」成立**，且比卡片更彻底：连「hub 侧能不能查状态」都被设计成可降级（查不到就走磁盘或 `task/query`）。

### 7. 状态归属与命令/幂等语义

| 状态 | 所有者 | 位置 | 语义 | 依据 |
|---|---|---|---|---|
| **任务状态真身** | **副机** | `<stateDir>/tasks/<taskId>.json`（默认 `~/.dsh-remote-agent`） | 状态转移**同步落盘**（终态必须耐久，否则崩溃后 reconcile 会把 completed 当 interrupted 重跑）；日志/进度 200 ms 批量写；原子 tmp+rename | [lib/node/task-store.js:1-22](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/task-store.js#L1-L22)、[:29-35](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/task-store.js#L29-L35) |
| **hub 的视图** | hub（投影） | 内存 `NodeRegistry` | 断连只置 `online=false`，**绝不清 tasks**；重连靠 `task/sync` 重建 | [lib/hub/node-registry.js:3-9](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/node-registry.js#L3-L9) |
| **重复 taskId** | 副机 | 同 store | **直接返回已有记录 + `duplicate: true`，不重跑** | [lib/node/task-engine.js:88-96](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/task-engine.js#L88-L96)、[lib/node/task-store.js:22](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/task-store.js#L22-L22) |
| **取消** | 副机执行、hub 发起 | `AbortController` + 杀进程树 | `ok` 必须排除 `aborted`，否则取消会被显示成 completed | [lib/node/task-engine.js:214-216](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/task-engine.js#L214-L216)、[lib/node/runner.js:830-838](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/node/runner.js#L830-L838) |
| **产物字节** | hub 拉取时落 hub 盘 | `<dest>/.dsh-remote-agent-<pullId>.part` | 边收边算 sha256，**校验通过才 rename**；续传旁车记 `startOffset`，7 天 TTL | [lib/hub/pull-manager.js:10-17](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/pull-manager.js#L10-L17)、[:176](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/pull-manager.js#L176-L176)、[:224](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/pull-manager.js#L224-L224)、[:301](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/pull-manager.js#L301-L301) |
| **产物分类** | 副机 | manifest | `final / intermediate / other`，**intermediate 规则先判**（否则 `dist/**` 会把 `dist/*.log` 捞成 final） | [lib/artifacts.js:6-15](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/artifacts.js#L6-L15)、[:105-108](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/artifacts.js#L105-L108) |
| **hub 收到什么** | — | — | handoff 摘要（summary ≤4000 字）+ 产物清单 + `progressTail`/`logTail` **各 ≤6 条、每条 ≤2000 字** | [lib/hub/views.js:319-371](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/lib/hub/views.js#L319-L371) |

**命令语义的精度点**：`task/completed` **不会**自动 push `task/sync`——只有 ① 节点上线重连 ② hub 主动 `task/query` 才发全量（[test/engine-e2e.test.js:15-22](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/test/engine-e2e.test.js#L15-L22) 把这条写成帧语义约定）。所以「hub 以为的成功」在断链窗口里只能是**摘要级**的，卡片 L40 的代价成立。

### 8. 「从传输问题降级为信任问题」复核

**方向成立，但要说清是哪一半降级了。**

- **成立的一半（正确性/可用性）**：工作的所有者是副机，任务状态真身在副机（§7），执行路径不读连接状态（§6），重连靠 `task/sync` 对账。所以**链路不再承担正确性**——这正是作者写「可用性边界（**不是安全边界**）」（SECURITY:49）的意思。
- **没降级的一半（安全/机密性）**：
  1. **relay 可主动降级加密**（§4 最后一行）：中继扣住 e2e 握手帧就能让链路退回明文，副机只警告——**传输层信任仍然存在**。
  2. **direct 默认明文 `ws://`**（SECURITY:45）：同网段可嗅探。
  3. **信任是强不对称的**：hub 能对副机 `mode:exec` 跑 shell（§3）。「信任问题」不是对等的「互相认识」，而是「副机把 shell 交给 hub」。
  4. **反向也没有独立验证**：hub 只有副机自报的 handoff，**无法独立证明任务真的做成了**（卡片 L40 的代价）。
- 所以更准确的说法是：**「正确性权威从连线搬到了副机；传输仍是信任依赖；而信任的代价是副机的 shell」**。卡片把「信任问题」写得像已经收敛，实际只是把风险**重新分配**了，没消除。

## SRC-DSH

`[SRC-DSH]` = 本机 `@deepseek-ai/dsh 0.2.1-rc.3`。它证明宿主契约，不证明目标插件在该宿主上的实际运行结果。

| 契约 | 宿主事实 | 目标插件的依赖点 |
|---|---|---|
| `agentLoop` 服务 | `Context` 上声明（`dsh-agent-loop/lib/types/index.d.ts:29`） | in-process 后端 `ctx.get('agentLoop')` |
| `createAgent(ownerCtx, options)` | 两参：调用方上下文 + `CreateAgentOptions`（`dsh-agent-loop/lib/types/index.d.ts:164`） | 插件按同一形态调用（runner.js:685-691） |
| `whenIdle()` | 循环等 `activityDone` 稳定（`dsh-agent-loop/lib/index.js:870-875`） | runner.js:804 |
| **`kick()` 吞 turn 错误** | `try { while (await this.turn()); } catch (_error) {} finally { … }`（`dsh-agent-loop/lib/index.js:887-897`）——**错误不进 driver，`whenIdle()` 照常 resolve** | 卡片 L30/L59 的核心前提 |
| `agent/error` 事件 | 由 `throwError()` 在 rethrow 前 emit（`dsh-agent-loop/lib/index.js:875-883`） | 插件唯一的错误观测面（runner.js:776-790） |
| `cordis-host-runner` 是合法来源 | `MessageSourceMap` 含 `'cordis-host-runner': { kind: 'cordis-host-runner' }`（`dsh-agent-preset-registry/lib/typert.host.js:637`）；**没有 `plugin`** | 插件常量 `PLUGIN_SOURCE`（runner.js:53）选择正确 |
| `subagents.registerProvider(provider)` | 注册面（`dsh-subagent/lib/types/index.d.ts:288`） | hub 侧注册 `remote-agent` provider（lib/hub/index.js:860-866） |
| `SubagentProvider` 形状 | `name` / `capabilities: SubagentCapabilities` / `inheritsParentContext: boolean`（`dsh-subagent/lib/types/types.d.ts:296-306`） | 插件三字段齐备 |
| **`SubagentCapabilities` 的键** | **只有 4 个**：`agentOptions`、`agentPreset`、`outputSchema`、`depthLimit`（`dsh-subagent/lib/types/types.d.ts:115-121`） | 插件声明了 **5 个**：`agentOptions`/`outputSchema`/`depthLimit`/**`toolFilter`**/**`persona`**，且**缺 `agentPreset`**（lib/hub/subagent-provider.js:218-224） |
| `webServer.registerUpgrade(route)` | 宿主提供（`dsh-host-webserver/lib/types/index.d.ts:181`） | hub 回退通道（lib/hub/index.js:707） |
| exact 优先于 prefix | `match()` 先查 exact 表再扫 prefix（`dsh-host-webserver/lib/index.js:495-504`） | 插件 UI 路由用 `kind:'exact'` 绕过 `/api` 围栏，故自己补围栏（ui-routes.js:195-241） |
| schemastery 由宿主提供 | 插件把它声明为 `peerDependencies` + `dependencies`（package.json:76-84） | 顶层 `import z from '@deepseek-ai/schemastery'` |

**目标行为 vs 上游契约的分界**：

1. **「假成功」是上游语义，不是插件 bug 的借口**：`kick()` 的 `catch {}` 在宿主里，插件唯一的正确做法就是监听 `agent/error` 并把它算进 `ok`——0.9.11 正是这么修的（runner.js:837 `ok: !timedOut && !aborted && !hadError`）。卡片把它写成「DSH 的 kick() 吞掉 turn 内错误导致假成功」，**归因准确**。
2. **`capabilities` 的键与宿主不一致**：`toolFilter`/`persona` 在 0.2.1-rc.3 的 `SubagentCapabilities` 里**不存在**，`agentPreset` 缺失。因为值全是 `false`/`undefined`，**运行时效果等价**（都不支持），但「声明形状」不是宿主契约的形状——这是一个「文档级正确、类型级不精确」的点。卡片说「capabilities 全部为 false」在**值**上成立。
3. **in-process 后端依赖的是宿主服务名与形状**：`ctx.get('agentLoop')`/`ctx.get('sessions')` 的探测方式（先 `ctx.get` 再回退 headless）是对 cordis「未声明 inject 访问属性会抛」的正确规避（runner.js:429-445 注释），与宿主 0.2.1-rc.3 行为一致。

## TEST

`[TEST]` 只证明覆盖意图，**不证明测试通过**（本轮未跑）。仓库共 **62 个** `test/*.test.js`。

- **假成功回归**：`test/agent-false-success.test.js` **5 条**，全部是**源码正则静态断言**（读 `lib/node/runner.js` 文本后 `assert.match`）——`agent/error` 必须置 `hadError`（:47-57）、`ok` 必须含 `!hadError`（:59-70）、`exitCode`/`stderr` 形态（:73-81）、状态映射 completed/failed（:96-99）、超时/取消仍判失败（:104-107）。**卡片「用源码正则静态断言钉死这三条」逐字成立**。
- **全链路**：`test/hub-worker-e2e.test.js` 用**真实实现**（真 http server + `applyHub` + `applyWorker` + 真 relay），但 agent 模式不走真实模型，全链路用 `mode:'exec'`（文件头 :1-30）。
- **拓扑/韧性**：`test/resilience.test.js`（7 条：心跳定时器、不误杀活跃节点、背压、relay 停滞断连、`ctx.get` 探测抛错不炸）、`test/relay-link.test.js`（29 条）、`test/listen-server.test.js`、`test/ws.test.js`。
- **认证**：`test/hub-pin.test.js`（11 条：TOFU 落盘、指纹不符拒绝、坏签名/重放 nonce/超时时间戳全拒）、`test/hub-identity.test.js`、`test/pairing.test.js`（17 条）。
- **产物/状态**：`test/engine-e2e.test.js`（20 条：exec、intermediate 不可 pull、**同 taskId 二次 accept = duplicate 且不重跑**、失败/超时/取消）、`test/artifact-resume.test.js`、`test/artifacts.test.js`、`test/task-store-batching.test.js`。
- **没覆盖的**：真实 DSH agent 循环（in-process 后端只能靠源码断言，作者在 `agent-false-success.test.js:34-37` 明说「依赖真实 DSH agent 上下文，无法在单测里跑起来」）；真实网络下的 NAT/中继部署；跨机时钟漂移下的 ed25519 时间戳判定。CI 注释自称「`npm test` 524 条」是 `[DOC]`，本轮未复算。

## CI

`[CI]`：**workflow 存在，同 SHA 的结果未取到**（GitHub REST 对本机 IP 限流，`/commits/cc356e1/check-runs` 返回 403 rate-limit，重试两次均失败）。按 `EVIDENCE.md` §1「workflow 存在不算」，本条记为 **[OPEN]**，不写「CI 绿」。

已知的 workflow 事实（`[CI]` 只到「配置存在」这一级）：

- `.github/workflows/ci.yml`（97 行），三个 job：`check`（matrix `ubuntu/windows/macos` × `node 22/24`，排除 macos+22 → **5 组**，跑 `npm install` + `npm run check`）、`packaging`（`node scripts/check-packaging.mjs`，校验 `files`/`exports` 路径存在）、`lint`（`eslint .`）——[ci.yml:22-37](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/.github/workflows/ci.yml#L22-L37)、[:56-63](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/.github/workflows/ci.yml#L56-L63)、[:72-80](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/.github/workflows/ci.yml#L72-L80)、[:86-97](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/.github/workflows/ci.yml#L86-L97)。
- `npm run check` = `check:packaging && check:docs && diag:inject && test`（[package.json:94](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/package.json#L94-L94)）。
- **CI 注释自己否掉了 README 的 lockfile 说法**：「这一步的真实价值**不是**『验证 lockfile 自洽』（本仓库 `.npmrc` 显式 `package-lock=false`，没有 npm lockfile 可校验）」——[ci.yml:52-55](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/.github/workflows/ci.yml#L52-L55)、[.npmrc:9](https://github.com/zbzbhs/dsh-remote-agent/blob/cc356e11dfe435a755459e3e07420a49ea506317/.npmrc#L9-L9)。见偏差表。

## RUN

`[RUN] None`。本轮只做只读网络取数（GitHub REST、`registry.npmjs.org`、`api.npmjs.org` 下载量、codeload tarball、npm tarball）与本地静态阅读 + 本机 DSH 发行包检索；**未安装、未构建、未执行 `npm test` / `npm run check`、未启动 hub/worker/relay、未建立任何 ws 连接**。

## 与卡片的偏差

| 卡片位置 / 主张 | 复核结论 | 标签 | 依据 |
|---|---|---|---|
| L48 「版本(本次读) `0.9.11`」 | **可复现但 pin 不完整**：gitHead 对齐 `cc356e1`，但仓库**没有 `v0.9.11` tag**（最高 `v0.9.10`），且 npm `latest` 已是 `0.9.12`（同树、仅版本串不同）。只写版本号会让读者装到 0.9.12 或无从定位 | `[SRC-TARGET]`+registry | Provenance |
| 全卡无「证据链」行与 memo 链接 | 与 `EVIDENCE.md` §2.2 不符（本条按要求未改卡） | `[DOC]`（本册规程） | EVIDENCE.md:1-68 |
| L5/L13/L22 「凭证永不出机」 | **只在协议层成立**：协议确实不带 key，但 hub 有 `mode:exec` 可跑 shell、`remote_read` 可读 roots 内文件；作者自己把「主机可信」写成硬前提。应改为「插件不要求凭证过线」 | `[SRC-TARGET]` | SECURITY:43-46, 54-56；lib/node/exec.js:401 |
| L22 「副机本地跑完整 DSH 与完整 Agent 循环」 | **成立，但有两种后端**：in-process（需 `agentLoop`+`sessions`）优先，否则 spawn `dsh headless`；**headless 不能指定模型**，且两者都失败时任务不可用。卡片未写 | `[SRC-TARGET]` | runner.js:406-467, 155-171 |
| L40 「副机要独立管凭据、独立升级」 | 成立；再补一条：**副机也要独立装 DSH 与 profile**，`inject` 必须清空否则永不激活 | `[SRC-TARGET]` | profiles/worker.cordis.yml:26-33；lib/index.js:10-25 |
| L40 「副机失联后 hub 侧无独立完成验证」 | **成立且是结构性的**：任务真身在副机，hub 只有自报 handoff；`task/sync` 只在重连/主动 query 时发 | `[SRC-TARGET]` | node-registry.js:3-9；engine-e2e.test.js:15-22 |
| L6/L24 「把跨机从传输问题降级为信任问题」 | **只对一半**：正确性权威确实搬到了副机（成立），但传输仍是信任依赖——relay 可被扣帧降级为明文、direct 默认明文 `ws://`；且信任不对等（副机把 shell 交给 hub）。准确说法是「**风险重新分配**，不是消除」 | `[SRC-TARGET]`+`[DOC]` | e2e.js:36-40；SECURITY:43-49；§8 |
| L28 「配对码…7 字段…不过期、不核验」 | **准确**（7 个白名单键、无时间戳、无签名/MAC）；但漏了它**携带 hub 指纹**、是 TOFU 的唯一分发渠道 | `[SRC-TARGET]` | pairing.js:26, 14-22 |
| L28/L66 「`nodeToken` 是真正的长期凭证」 | 成立；补两条卡片没有的：① 空 token 时**强制回环**（除非显式非回环 `listenHost`）② 校验在 **upgrade 头 `x-dsh-token`**、恒定时间比较 | `[SRC-TARGET]` | hub/index.js:578-586, 624-628, 711-716 |
| L28 「relay = 纯转发 + X25519→HKDF→AES-256-GCM」 | **逐项成立**；但漏了**可主动降级**（中继扣 e2e 握手帧→退回明文）与 direct 默认明文 `ws://` | `[SRC-TARGET]` | e2e.js:36-40；SECURITY:45-46 |
| L28 「心跳 15s/超时 45s，退避 1s→30s+抖动」 | **四个数全对**（另补握手超时 10s、抖动 0–20 %） | `[SRC-TARGET]` | transport.js:34-37, 736-738 |
| L26 「`capabilities` 全部为 false」 | **值上成立**；但键集与宿主不一致：`toolFilter`/`persona` 不是 `SubagentCapabilities` 的键，缺 `agentPreset`。运行时等价，类型不精确 | `[SRC-TARGET]`+`[SRC-DSH]` | subagent-provider.js:218-224；dsh-subagent types.d.ts:115-121 |
| L30/L59 「`kick()` 吞 turn 内错误 → 假成功；`ok` 必须加 `hadError`」 | **完全成立**：宿主 `kick` 的 `catch (_error) {}` 在 `dsh-agent-loop` 内，`whenIdle()` 照常 resolve；0.9.11 的 `ok` 已是 `!timedOut && !aborted && !hadError` | `[SRC-DSH]`+`[SRC-TARGET]` | dsh-agent-loop/lib/index.js:887-897；runner.js:837 |
| L59 「用源码正则静态断言钉死」 | **成立**：5 条测试全部 `readFileSync(runner.js)` + `assert.match` | `[TEST]` | agent-false-success.test.js:47-107 |
| L32 「产物三分、intermediate 优先、`.part` 边收边算 sha256、`startOffset` 续传」 | **全对**（续传 TTL 7 天、旁车 meta 校验全文 sha256） | `[SRC-TARGET]` | artifacts.js:6-15；pull-manager.js:10-17, 176, 224, 301 |
| L50 「npm 近 30 天 3,103 次（2026-09-30~10-29）」 | **数字精确**：`api.npmjs.org` 该区间合计 **3103** | `[RUN]`（只读取数） | api.npmjs.org/downloads/range |
| L52 「零外部运行时依赖(README:629)」 | **半错**：`README:629` 确有此句，但 `package.json` 有 1 个 `dependencies`（`@deepseek-ai/schemastery ^3.18.4`，宿主提供）；且 CI 注释自己说「这不是验证 lockfile」（`.npmrc` 无 package-lock）。准确说法是「**无第三方运行时依赖**」 | `[SRC-TARGET]` | package.json:83-84；ci.yml:52-55 |
| L52 「`main: ./lib/index.js`」 | 成立（另：`lib/**` 即产物，无构建步骤） | `[SRC-TARGET]` | package.json:45；README:633 |
| L15/L50 「4★、3,103 次」 | 4★ 与 3103 均复核一致；「4★ 看不出的体量」是判断 | `[RUN]`/`[OBS]` | `/repos`；api.npmjs.org |
| L14 「过了哪些门：F + G」 | 本册内部闸门，**目标仓无法证明** | `[OPEN]` | — |
| 卡头 `updated: 2026-10-31`、影响力采样日 | 复核日（2026-11-01）星数仍为 4；下载量为历史窗口，取值一致 | `[RUN]` | `/repos`；api.npmjs.org |

## `[OPEN]`

- **CI 同 SHA 结果未取到**：GitHub REST 限流（403 rate-limit），`cc356e1` 的 check-run 状态未知。workflow 存在≠CI 绿。
- **没有真实宿主上的运行证据**：in-process 后端在真实副机 DSH 上的行为（`agentLoop`/`sessions` 可用性、`followup` 的 `cordis-host-runner` 来源是否被接受、`whenIdle` 的时序）只做了契约层比对，未实跑。
- **headless 后端的 NDJSON 契约**：`extractFinalFromNdjson` 认的三种形态（`assistant/message`、`assistant.message`、`message`）是否覆盖本机 `dsh 0.2.1-rc.3 headless --json` 的真实输出，未验证（作者注释称 2026-10-15 核实过 `dsh-headless` 源码）。
- **relay 主动降级**：中继扣住 `node/e2e` 握手帧后退回明文的实际触发条件、警告是否可被用户看到，未验证。
- **跨机时钟与 TOFU 首次截和**：ed25519 身份帧 ±5 分钟容差在真实跨机时钟漂移下的表现、TOFU 首连被中间人的后果，未验证（作者已披露）。
- **`both` 模式与端口冲突**：同机同时 listen 19387 与拨入自身的实际行为、EADDRINUSE 重试（最多 4 次尝试，等待 200/400/600 ms）在热重载下的稳定性，未验证。
- **0.9.12 的来源**：从「未提交的版本号」重发意味着发布树不可从 git 复现（虽然内容与 0.9.11 等价）；0.9.12 的发布动机（是否修了什么）无从判断，`CHANGELOG` 顶条仍是 `0.9.11`。
- **`lib/` 与 npm tarball 的 CRLF 差异**：4 个文件在 npm 包里是 CRLF——是发布机的换行归一还是 `.gitattributes` 配置所致未查；语义无差，但「npm 产物字节 = commit 字节」严格说**不成立**。
- **测试通过性**：62 个测试文件、CI 注释自称 524 条，本轮一律未跑；`[TEST]` 只到覆盖意图。
