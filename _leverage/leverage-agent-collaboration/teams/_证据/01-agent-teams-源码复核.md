---
title: "源码复核：NanmiCoder/dsh-agent-teams 0.1.28（跨边界样本 01）"
domain: agent-teams
kind: evidence
positioning: "钉 npm 0.1.28 ↔ tag v0.1.28 ↔ commit 3331b90：成员启动签名、邮箱 60s 租约与准入 ack、attempt 代际、8 人上限、idle 边沿与四个具名失效。"
read_when: "核对本册 01 号样本的源码依据，或要改它的机制断言时。"
status: observed
updated: 2026-11-01
---
# 源码复核：`NanmiCoder/dsh-agent-teams` 0.1.28

> 取证时点 2026-11-01（Asia/Shanghai）。只读 `registry.npmjs.org`（packument + attestation）、GitHub codeload 归档与 check-runs API、本机 DSH `0.2.1-rc.3` 发行包，以及 `/tmp` 内的解包与 `shasum` 比对；**未安装、未构建、未运行目标插件，未执行其任何 `scripts/*.mjs`，未启动 DSH，未写任何真实 profile 或 `.agent-teams/`**。
> 坐标：`[SRC-TARGET]` = tag `v0.1.28` → commit [`3331b903f0e954d59ac69be1a75fd4fd7e1de20e`](https://github.com/NanmiCoder/dsh-agent-teams/commit/3331b903f0e954d59ac69be1a75fd4fd7e1de20e) 的 `src/`；本文所有 `src/` 行号都钉在该 commit。`[SRC-DSH]` = 本机 `@deepseek-ai/dsh@0.2.1-rc.3`。`[DOC]` 只证作者主张，`[TEST]` 只证覆盖意图，`[CI]` 只引同 SHA 的 check-runs 与 provenance，`[OBS]` 是推断。
> 阅读范围：`src/{members,harness-compat,state,mailbox,scheduler,tools,index,types,profiles}.ts` 中与本卡机制相关的段落，`README.md`、`docs/usage.md`、`docs/quality-gates.md`、相关 `scripts/*.mjs`；**没有逐行读完 12,185 行 `src/`**，所以“源码逐文件读过”这一自述不是本文能背书的范围。

## Provenance

- `[RUN]` npm `@nanmicoder/dsh-agent-teams@0.1.28` 是 `dist-tags.latest`（另两个 tag：`next = 0.1.24-rc.1`、`alpha = 0.1.15-alpha.1`），发布时间 `2026-10-30T06:36:55.107Z`，共 34 个版本；0.1.28 的 manifest **没有 `gitHead`**，`dist.attestations` 给出 SLSA v1 provenance。
- `[RUN]` 2026-11-01 重取 attestation：`buildType = github-actions workflow v1`、`externalParameters.workflow = { repository: https://github.com/NanmiCoder/dsh-agent-teams, path: .github/workflows/publish.yml, ref: refs/tags/v0.1.28 }`、`resolvedDependencies[0].digest.gitCommit = 3331b903f0e954d59ac69be1a75fd4fd7e1de20e`、`runDetails.metadata.invocationId = …/actions/runs/41014297086/attempts/1`。**npm 0.1.28 ↔ tag `v0.1.28` ↔ commit `3331b90` 的绑定由 provenance 给出，不依赖 `gitHead`。**
- `[SRC-TARGET]` 内容比对（tag 归档 vs npm tarball，`shasum -a 256`）：`README.md` 逐字节相同（`c325d34f…`）；`lib/scheduler.js`、`members.js`、`state.js`、`mailbox.js`、`tools.js`、`index.js`、`harness-compat.js` 七个模块逐字节相同；`lib/client.js` 不同（差在构建期 CSS module 类名前缀与 `\0dsh-css:` 路径）。→ **服务端产物与 tag 同源；npm 0.1.28 是同一 tag 源码的 CI 重建物，不是 tag 提交物 `lib/` 的字节副本。**
- `[SRC-TARGET]` **npm 包里没有 `src/`**：只有 `lib/`（构建产物）、`README*`、`cordis.patch.yml`、`compatibility.json`、`assets/`、`release-notes/` 与 3 个脚本（`compatibility.mjs`、`doctor.mjs`、`legacy-session-source-repair.mjs`）。因此“源码逐文件读过”只能指仓库/tag 的 `src/`，不可能指装到本机的 npm 包；本 memo 的源码行号一律指 tag 树。
- `[SRC-TARGET]` `package.json`：`version 0.1.28`、MIT、`bin.dsh-agent-teams-doctor`、`dsh.bundle.patch = ./cordis.patch.yml`、`dsh.client.platform = web`（`inject` 8 个客户端包）、`engines.dsh = ">=0.1.2-alpha.2"`、`engines.node = "^22.19.0 || >=24"`。
- `[RUN]` 本机 `git ls-remote` 未返回结果，**没有独立读 tag 对象**；tag → commit 只有 provenance 一侧的证据。
- `[DOC]` 本卡没有声明宿主基线；`compatibility.json` 推荐 `0.2.1-rc.2`、把 `0.2.1-rc.3` 列为 preview，而该 commit 的 CI 矩阵含 rc.3（ubuntu + windows，均 success）。本文用 rc.3 只为核对宿主默认值与事件契约，不外推其它版本。

## DOC（目标 README/中文文档的主张）

- `[DOC]` 定位与工具面：`14 coordination tools`、`persistent state`、`an automatic shared-task scheduler`、`without requiring a separate workflow engine`（[`README.md:31`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/README.md#L31-L31)）。
- `[DOC]` 成员与消息：`Durable members … continuable DSH sub-agents that can be woken for focused follow-up turns`（[:46](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/README.md#L46-L46)）；`Direct messaging … durable mailbox messages`（[:49](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/README.md#L49-L49)）。
- `[DOC]` 调度与 attempt：`uses real running / idle / ready state to atomically claim one ready task per idle member and wake it. An interrupted resident attempt stays parked … after a cold process restart, the scheduler retries stranded open work with a fresh attempt`（[:141](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/README.md#L141-L141)）；`reassignment or captain takeover revokes the old attempt and waits for the old worker to quiesce`（[:142](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/README.md#L142-L142)）。
- `[DOC]` 磁盘真相：`Team state is stored under <workspace>/.agent-teams/`（[:145](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/README.md#L145-L145)）。
- `[DOC]` 边界：`An idle member that still owns an open attempt is parked until messaged or explicitly reassigned; messages that cannot be delivered live remain durable and are retried at a later status boundary`（[:214](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/README.md#L214-L214)）；`State is file-backed and serialized within one DSH process; concurrent processes editing the same team are not coordinated`（[:215](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/README.md#L215-L215)）；`The activity panel reports persisted state as-is`（[:216](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/README.md#L216-L216)）。
- `[DOC]` 配置与安装：示例写 `maxMembers: 8`（[:186](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/README.md#L186-L186)）；桌面端 pnpm 11 的 24 h 最小发布年龄只在裸名/`@latest` 时生效（[:87](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/README.md#L87-L87)）；精确命令是 `dsh plugin --profile web add --save-exact @nanmicoder/dsh-agent-teams@0.1.28`（[:107](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/README.md#L107-L107)）。
- `[DOC]` 中文文档把 parked 说全了：驻留成员中断或正常结束一轮后若仍持 `claimed/in_progress`，该 attempt 停驻，**只有显式重试/转派/接管才撤销**；本进程已观察过的停驻 attempt 在 Harness 回收 AgentHandle 后仍保持原 attempt；只有冷启动或从未观察过的开放任务才自动恢复一次，恢复投递失败会回到原 capability（[`docs/usage.md:97`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/docs/usage.md#L97-L97)）。

## SRC-TARGET

### 1. `spawnMember` / `startMember` 签名：卡片少写了两个必填字段

- `[SRC-TARGET]` `spawnMember` 的真实签名有 12 个参数：`spawnMember(ctx, config, selections, llmSelection, captain, team, member, stateDir, signal, initialPrompt?, resolvedFilter?, relaxableDeny?)`（[`src/members.ts:900-L914`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/members.ts#L900-L914)）。
- `[SRC-TARGET]` 它不直接调 `startMember`，而是 `startMemberWithLenientFilter(toolFilter => … startMember(ctx.subagents, spec) …, requestedFilter, relaxableDeny)`；后者在宿主以 `tools.restrict() names unknown global tool` 拒绝时，逐轮删掉可放宽的 deny 名重试（[`src/harness-compat.ts:477-L497`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/harness-compat.ts#L477-L497)、[`src/members.ts:941-L966`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/members.ts#L941-L966)）。
- `[SRC-TARGET]` `startMember(runtime, spec: MemberStartSpec)` 的 spec 是 `{ provider, label, request: { parent, prompt, agentOptions?, persona?, toolFilter? }, signal }`——**`prompt` 与 `signal` 都是必填**（[`src/harness-compat.ts:47-L58`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/harness-compat.ts#L47-L58)、[`:71-L83`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/harness-compat.ts#L71-L83)）。卡片写的 `{provider, label, request:{parent, persona, toolFilter, agentOptions}}` 把这两个字段漏掉了。
- `[SRC-TARGET]` rc.3 走 managed-activation 分支：`startActivation` 存在时，`startMember` 先把 `persona` 与 `toolFilter` 从 `request` 里剥掉，再传 `{...spec, request, delivery:'parent'}`，并只对 `activation.result` 挂 `.catch`；persona/filter 由 `member.runtimeSetup` 在续聊/冷恢复时重新装回（[`src/harness-compat.ts:71-L82`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/harness-compat.ts#L71-L82)、[`src/members.ts:975-L983`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/members.ts#L975-L983)、[`:660-L686`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/members.ts#L660-L686)）。
- `[SRC-TARGET]` 成员创建发生在 `dispatchMember` 的 team 锁内，`spawnMember` 成功后才 `writeTeam`；`member.id = start.childId` 只在成功后赋值（[`src/tools.ts:691-L706`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/tools.ts#L691-L706)、[`src/members.ts:975`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/members.ts#L975-L975)）；doc 注释写 `On failure nothing is persisted`（[`src/members.ts:881`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/members.ts#L881-L881)）。

### 2. “persist + mailbox”的因果：模块注释是真的，卡片把宿主事实说满了

- `[SRC-TARGET]` 因果链原文在 `members.ts` 模块注释：成员是 captain 的 durable continuable 子代理，跨轮/跨宿主重启保留对话；`Its final assistant message is not readable programmatically, so the member persists its report into the captain's mailbox and the task records, which the captain reads through agent_teams_status`（[`src/members.ts:1-L12`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/members.ts#L1-L12)，引文在 :9-:11）。
- `[SRC-DSH]` 但宿主的结算通知**确实带着最终文本**：`subagent-settled` notice 里有 `Its closing message:` + closing text，有结构化结果时还附 `Structured result:`（`@deepseek-ai/dsh-subagent@0.2.1-rc.3` `lib/index.js:515-L526`）；`activation.result` 也是真的 promise，会 resolve 执行结果（同文件 `:2043`、`:2073-L2077`）。插件在 `startMember` 里主动忽略它，只留 `.catch` 作失败兜底（[`src/harness-compat.ts:76-L79`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/harness-compat.ts#L76-L79)）。
- `[OBS]` 所以“最终文本不可程序化读取”应读成“**没有调用帧去取结果**”：派发由 idle 边沿/任务图变更从后台触发（§6），captain 并不在等待某个调用；通知是散文，同一结算还可能重复，插件要专门去重（[`src/mailbox.ts:80-L99`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/mailbox.ts#L80-L99)）。结论（成员把报告写进邮箱与任务记录）成立，但“只能作为父通知投递一次”不成立——通知可能重复，`activation.result` 也不是不可读。
- `[SRC-DSH]` 因此“必须让成员活着”也偏强：宿主对**缺席的 continuable 子会话**在投递时会从持久化冷恢复（`dsh-subagent/lib/index.js:3060-L3063`）。成员设计的硬要求是“会话持久 + setup 可恢复”，不是“Agent 常驻”。

### 3. 邮箱三态、60 s 租约与准入 ack

- `[SRC-TARGET]` 字段与语义：`deliveryClaimedAt`（投递在途）、`deliveredAt`（Harness 已接受）、`readAt`（模型 step 已消费），另有 `discardedAt`（过期代际，见 §4）（[`src/types.ts:315-L335`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/types.ts#L315-L335)、[`src/state.ts:566-L598`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/state.ts#L566-L598)）。
- `[SRC-TARGET]` `MAILBOX_DELIVERY_LEASE_MS = 60_000`（[`src/state.ts:54`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/state.ts#L54-L54)），但它只在 `readPendingMailbox` 里生效：`deliveredAt === undefined` 且（未 claim 或 claim 已过 60 s）才算待投（[`:506-L512`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/state.ts#L506-L512)）。claim 在派发批次的 team 锁内整批写入（[`src/scheduler.ts:326-L334`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L326-L334)、[`src/state.ts:546-L557`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/state.ts#L546-L557)），投递失败则整批释放（[`src/state.ts:560-L568`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/state.ts#L560-L568)、[`src/scheduler.ts:338-L346`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L338-L346)）。
- `[SRC-TARGET]` 两条“消费”入口：
  1. `agent/pre-step` 收到 receipt 批次，在锁内重读、按 `isCurrentMail` 丢弃过期、把当前消息 `acknowledgeMailbox`（同时写 `deliveredAt` 与 `readAt`）（[`src/mailbox.ts:63-L140`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/mailbox.ts#L63-L140)）；
  2. `agent_teams_status` 把读到的 captain/member inbox 一并 ack（[`src/tools.ts:2442-L2450`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/tools.ts#L2442-L2450)）。
  所以卡片的“只有被 `agent/pre-step` 准入的消息才 ack”**是过强的**；“被 reject 的 step 不算消费”倒是对的（[`src/mailbox.ts:147-L171`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/mailbox.ts#L147-L171)）。
- `[SRC-TARGET]` 卡片引的注释就在函数上方：`Acceptance by Harness is not evidence that a model step consumed input`（[`src/state.ts:593`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/state.ts#L593-L593)），指的正是 `markMailboxDelivered` 只写 `deliveredAt`（[`:594-L598`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/state.ts#L594-L598)）。
- `[SRC-TARGET]` 60 s 租约的用途是“崩溃后让在途 claim 过期可重投”，不是投递时限；**没有测试覆盖过期重投**（见 TEST）。

### 4. `attemptId` / `sourceAttemptId` 代际过滤

- `[SRC-TARGET]` `isCurrentMail`（[`src/mailbox.ts:11-L19`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/mailbox.ts#L11-L19)）：
  - 带 `sourceAttemptId` 的成员报告：要求源任务 `id === sourceTaskId`、`attemptId === sourceAttemptId`、`assignee === message.from`，且任务已在终态时记录状态必须与之一致；
  - 带 `attemptId` 的指令：要求目标任务 `attemptId` 匹配、`assignee === message.to`、状态仍是 `claimed|in_progress`；
  - 两个字段都没有的消息**一律放行**——过滤只对“带代际”的邮件成立。
- `[SRC-TARGET]` 过期消息在准入时被 `discardMailboxMessages`（写 `discardedAt`，不写 `readAt`），当前消息才 ack（[`src/mailbox.ts:128-L138`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/mailbox.ts#L128-L138)、[`:34-L41`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/mailbox.ts#L34-L41)）。`send_message` 也强制 `source_task_id`/`source_attempt_id` 成对出现，并拒绝“别人的/过期的源 attempt”（[`src/tools.ts:2216-L2229`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/tools.ts#L2216-L2229)）。
- `[TEST]` 有专门用例：32 条消息一次准入恰好消费一次、被 reject 的 step 不消费；旧代际被丢弃而当前代际保留（[`scripts/stability-tdd.mjs:36-L56`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/scripts/stability-tdd.mjs#L36-L56)、[`:58-L69`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/scripts/stability-tdd.mjs#L58-L69)）。
- `[OBS]` 卡片“上一代 attempt 留下的指令不会污染下一代成员”成立，但只覆盖带代际的邮件；captain 发的、不带 attemptId 的邮件不会被清。

### 5. `maxMembers` 8 与宿主 `maxActiveSubagents` 8：相等为真，因果是卡片加的

- `[SRC-TARGET]` 默认 8：`maxMembers: z.natural().min(1).default(8)`（[`src/index.ts:173`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/index.ts#L173-L173)），运行配置 `maxMembers: config.maxMembers ?? 8`（[`:203`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/index.ts#L203-L203)），注释 `Team size cap in members (default 8)`（[`:90`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/index.ts#L90-L90)）；文档示例同为 8（[`README.md:186`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/README.md#L186-L186)、[`docs/usage.md:77`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/docs/usage.md#L77-L77)）。
- `[SRC-TARGET]` 它是**可配参数**：`z.natural().min(1)` 接受任意正整数；只在 `add_member` 时按“非 removed 成员数 ≥ cap”拒绝（[`src/tools.ts:1360-L1361`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/tools.ts#L1360-L1361)），profile 解析另有越界报错（[`src/profiles.ts:312-L314`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/profiles.ts#L312-L314)）。
- `[SRC-DSH]` 宿主默认值确为 8：`maxActiveSubagents … .default(8)`（`dsh-subagent/lib/index.js:2980`），每次 materialize 前 `pool.reserve(this.maxActiveSubagents())`（同文件 `:1677`），池满抛 `SubagentError(…, "ACTIVATION_LIMIT_REACHED")`（`:1046-L1049`）；池是**进程内、沿 continuable 父链共享**的 slots（`:1038-L1052`、`:1216-L1218`）。
- `[OBS]` 因此：两个 8 的**数值相等**属实；但（a）`maxMembers` 是花名册上限，不是并发上限——空闲成员不占激活槽；（b）插件源码从未提到 `maxActiveSubagents` 或 `ACTIVATION_LIMIT_REACHED`（全仓 grep 0 命中），所以“不是巧合”“硬天花板”“不可调”三条都没有源码支持。准确表述是“默认值相同；满编 8 人同时开工恰好占满父会话默认槽位，会与 captain 自己的子代理调用争夺同一池；是否蓄意对齐无法由源码证明”。

### 6. idle 边沿调度

- `[SRC-TARGET]` 模块注释把设计说得很直：Claude Code teammates 靠轮询，DSH continuable agent 暴露 idle/running 边沿，所以**每个 idle 边沿和每次任务图变更都尝试一次原子认领并唤醒成员**，不保留轮询 turn（[`src/scheduler.ts:1-L13`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L1-L13)）。
- `[SRC-TARGET]` 触发链：`ctx.on('agent/status', …)`（[`:547-L551`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L547-L551)）→ `syncMemberStatus` 在 team 锁内把成员标成 working/idle（[`:489-L543`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L489-L543)）→ 仅 idle 时 `runtime.kickMember`（[`:544`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L544-L544)）。`kickMember` 按 `stateRoot\0teamId\0member` 串行（[`:313-L315`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L313-L315)）。
- `[SRC-TARGET]` 锁内先邮箱后任务：有待投邮件就整批 claim 并 `steer`，接受后 `markMailboxDelivered`、失败则释放（[`:326-L347`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L326-L347)）；没有邮件才在锁内挑 ready 任务、`beginTaskAttempt` 铸新 attempt、标 working 并落盘（[`:353-L401`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L353-L401)）；**真正的唤醒 `deliverToMember(…, 'queue')` 在锁外**（[`:446-L450`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L446-L450)）。ready 的判据是 `pending` + 非 reassigning + 依赖全部 completed，先本成员、后无主（[`:202-L209`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L202-L209)）。
- `[SRC-TARGET]` 停驻：本进程观察到“成员 idle 但仍持有开放 attempt”就把该 attempt 记进 `parkedAttempts`（[`:279-L281`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L279-L281)、[`:365-L372`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L365-L372)、[`:397`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L397-L397)），后续 kick 只标 idle、不再派新 attempt；冷进程（map 为空）才允许恢复一次，恢复投递失败会回滚旧代际并重新 park（[`:359-L381`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L359-L381)、[`:455-L484`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L455-L484)）。captain 自己名下的开放任务则在 captain idle 边沿直接 `invalidateTaskAttempt` 回池（[`:497-L521`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/scheduler.ts#L497-L521)）。
- `[SRC-DSH]` 宿主事件契约：`agent/status` 只有 `idle|running`，`idle` 表示没有 driver 在跑（`@deepseek-ai/dsh-agent/lib/types/runtime-types.d.ts:84-L90`、`:252-L255`）。
- `[OBS]` 卡片这句基本准确，只差两点：idle 边沿**先投邮箱再领任务**；唤醒在锁外，锁内原子的是“认领 + 铸 attempt id”。另外它不是只把 `agent/status` 当时钟，任务图变更也会 kick。

### 7. 四个具名失效：机制各有出处，名字都不是上游的

全仓（`src/`、`README*`、`docs/`、`scripts/`）grep 四个名字均 **0 命中**——它们是卡片自造的分类，引用时必须标 `[OBS]`，不能写成上游术语。

- `second-process-lost-update`：真实风险，且比“丢更新”更糟。锁是进程内 Promise 链（[`src/state.ts:67-L85`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/state.ts#L67-L85)），全仓无跨进程的 pid 文件/锁文件/租约（只有临时文件名用 `process.pid`，`:703-L715`）；邮箱追加是“读全量 + 整文件重写”（[`:430-L450`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/state.ts#L430-L450)），两个进程同时写会吞掉对方的消息行。README 自陈不协调（[:215](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/README.md#L215-L215)）。
- `parked-attempt-orphan`：机制真实，但“永久 parked”与本版文档矛盾——README 说 `parked until messaged or explicitly reassigned`（[:214](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/README.md#L214-L214)），中文文档说只有显式重试/转派/接管才撤销、冷启动恢复一次（`docs/usage.md:97`）；`remove_member` 会把该成员所有非 completed 任务 `invalidateTaskAttempt` 回池（[`src/tools.ts:1435-L1466`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/tools.ts#L1435-L1466)）。准确说法是“本进程内停驻，需显式动作或冷启动”。
- `spawn-in-flight-race`：正常失败路径**有补偿**：`dispatchMember` 在 `spawnMember` 后先留 `orphan = {...member}`，`writeTeam` 抛错时把该 id 写进 retired 名单并 drain 掉这个 activation（[`src/tools.ts:701-L718`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/tools.ts#L701-L718)、[`src/state.ts:326-L337`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/state.ts#L326-L337)、[`src/members.ts:1048-L1053`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/members.ts#L1048-L1053)），还会记 `spawnError` 供面板诊断（[`src/tools.ts:676-L690`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/tools.ts#L676-L690)）。**残留窗口只有“spawn 成功 → `writeTeam` 之间进程被杀”**；没有测试覆盖这个崩溃窗口。
- `halt-non-anchor`：真实。`haltTeamWork` 先落盘 `halted`、逐任务 cancel、逐成员置 idle，再 `captain.cancel`，drain 后再次 cancel；若记录的 captain 会话不活，`stopTeamMemberActivations` 被跳过并 warn：`captain session … is not live; member activations of "…" were not drained from this session`（[`src/tools.ts:557-L627`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/tools.ts#L557-L627)，warn 在 `:607-L613`）。此时 halted 已持久，但子代理可能继续跑到自己结算。

## SRC-DSH（0.2.1-rc.3，只列本卡用到的契约）

- `[SRC-DSH]` `agent/status` = `idle|running`，`idle` 表示无 active driver（`@deepseek-ai/dsh-agent/lib/types/runtime-types.d.ts:84-L90`、`:252-L255`）。
- `[SRC-DSH]` 子代理容量默认 8，槽位在 materialize 前 reserve，池满为 `ACTIVATION_LIMIT_REACHED`，池为进程内、沿 continuable 父链共享（`dsh-subagent/lib/index.js:2980`、`:1677`、`:1046-L1049`、`:1038-L1052`、`:1216-L1218`）。
- `[SRC-DSH]` rc.3 提供 `startActivation(spec)`（`dsh-subagent/lib/index.js:3036-L3047`），没有 `startContinuable`；插件的 `startContinuable` 分支是给旧宿主的（[`src/harness-compat.ts:81-L82`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/src/harness-compat.ts#L81-L82)）。
- `[SRC-DSH]` 结算通知带 closing message 与可选 structured result（`:515-L526`），`activation.result` 可 resolve 结果（`:2043`、`:2073-L2077`）。
- `[SRC-DSH]` 对缺席 continuable 子会话的投递会从持久化冷恢复（`:3060-L3063`）。

## TEST / CI / RUN

- `[TEST]` 与卡片机制直接相关的：
  - 邮箱准入：32 条消息一次准入恰好消费一次；reject 不算消费；已读邮件不打断 tool-result 续跑（[`scripts/stability-tdd.mjs:36-L56`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/scripts/stability-tdd.mjs#L36-L56)）；
  - 代际：旧 attempt 的 guidance 被 discard、同批当前消息存活（[`:58-L69`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/scripts/stability-tdd.mjs#L58-L69)）；
  - mailbox fallback：投递失败保留一条 durable 未读、status kick 不伪造消费（[`scripts/lifecycle-verify.mjs:1213-L1218`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/scripts/lifecycle-verify.mjs#L1213-L1218)）；未读邮件阻止同一 kick 再派任务（[`:521`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/scripts/lifecycle-verify.mjs#L521-L521)）；
  - 坏 `team.json` 时 `agent/pre-step` 降级为 pass-through 而不是卡住宿主（[`scripts/corrupt-teamjson.test.mjs:75-L98`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/scripts/corrupt-teamjson.test.mjs#L75-L98)）。
- `[TEST]` 覆盖缺口：① 60 s 租约过期重投无用例；② 两进程同 workspace 无用例；③ spawn→write 崩溃窗口无用例；④ `maxMembers` 与宿主容量关系无断言；⑤ 测试脚本**不随 npm 包发布**（包里只有 3 个脚本），[TEST] 只能指 tag 树。
- `[CI]` tag 内有 `.github/workflows/verify.yml` 与 `publish.yml`。`[RUN]` 2026-11-01 读 commit `3331b90` 的 check-runs：**39 条全部 success**，其中含 `Real Harness (ubuntu-latest, 0.2.1-rc.3)`、`(windows-latest, 0.2.1-rc.3)` 与 `publish`/`release`。provenance 记该次发布为 run 41014297086 attempt 1、ref `refs/tags/v0.1.28`。workflow 存在与 check-run 通过是两件事，这里两者都只对应这个 SHA，不外推其它 commit。
- `[RUN]` 本轮做过：`registry.npmjs.org` packument + attestation；GitHub check-runs/repo API；`api.npmjs.org` 下载量；`codeload.github.com` 的 `refs/tags/v0.1.28` 归档；npm tarball；`/tmp` 内解包与 `shasum -a 256` 比对；读本机 rc.3 包源码。外部指标复核：`2610★ / 223 fork`（2026-11-01，卡片写 2026-10-31 的 2592/222，属采样漂移）、npm `last-month = 50,995`（窗口 2026-09-30–2026-10-29，与卡片数字一致）。
- `[RUN] None`：**未做** `npm/pnpm install`、构建、`pnpm verify`、跑 `scripts/*.mjs`、启动 DSH、安装/启用插件、写 profile、创建 `.agent-teams/`；也没有独立读 tag 对象（`git ls-remote` 无返回）。

## 与卡片的偏差表

| 卡片主张 | 源码/宿主实际 | 处置 |
|---|---|---|
| 版本 `0.1.28`，“源码逐文件读过” | npm 0.1.28 ↔ tag v0.1.28 ↔ commit 3331b90（provenance）；npm 包无 `src/`；七个服务端 `lib` 模块与 tag 逐字节相同，`lib/client.js` 不同 | 卡上写“读的是 tag 3331b90 的源码”；npm 只作发布物绑定 |
| `startMember(ctx.subagents,{provider,label,request:{parent,persona,toolFilter,agentOptions}})` | 真实 spec 还必填 `prompt`、`signal`；调用被 `startMemberWithLenientFilter` 包一层；rc.3 上 persona/toolFilter 被剥离、经 `runtimeSetup` 装回 | 按 §1 补全签名与调用链 |
| “最终文本不可程序化读取，只能作为父通知投递一次” | 宿主 notice 带 closing message + structured result，`activation.result` 可读；插件主动忽略；通知可重复且插件去重 | 改成“没有调用帧拿结果；通知是散文且会重复，所以用邮箱持久化结构化报告” |
| “必须让成员活着” | 宿主对缺席 continuable 子会话可冷恢复投递 | 改成“会话必须持久、setup 必须可恢复” |
| “只有被 `agent/pre-step` 准入的消息才 ack” | pre-step 与 `agent_teams_status` 两条 ack 入口；reject 不算消费 | 改成“ack 只发生在 pre-step 准入或 status 读取” |
| `deliveryClaimedAt` 60 s 租约 | 常量属实；只用于让 stale claim 在 fallback 重新可投，无测试 | 保留，补“过期只在 `readPendingMailbox` 生效” |
| `isCurrentMail` 判过期 | 属实，但对不带 `attemptId/sourceAttemptId` 的邮件不生效 | 保留，补“只对带代际的邮件” |
| `maxMembers` 默认 8“不是巧合”“硬天花板，不是可调参数” | 默认 8 属实；可配 `z.natural().min(1)`；源码从不提宿主容量/`ACTIVATION_LIMIT_REACHED`；宿主默认 8 与错误码属实 | 改成“默认值相同；对齐无源码证据；`maxMembers` 可调，不是并发上限” |
| idle 边沿“在锁内原子认领 ready 任务并唤醒” | 认领与铸 attempt 在锁内；**先投邮箱**，唤醒在锁外；任务图变更也 kick | 保留结论，补两句边界 |
| parked “永久” | README/usage 明说 parked until messaged or explicitly reassigned；冷启动恢复一次；remove_member 回池 | 改成“本进程内停驻，需显式动作或冷启动” |
| `spawn-in-flight-race`：spawn 成功但落盘失败 → 花名册不认 | 正常失败路径有 retired-id + drain 补偿；只剩进程崩溃窗口 | 改成“崩溃窗口内的孤儿”，并标 `[OBS]` |
| `halt-non-anchor`：captain 不驻留时 halt 不收敛成员 | 属实；halted 先落盘，drain 被跳过并 warn，captain 仍被 cancel 两次 | 保留，补“不驻留”条件 |
| `second-process-lost-update` | 属实且更重：无跨进程锁、邮箱整文件重写 | 保留名字但标 `[OBS]`（上游无此术语） |
| npm 包名“唯一带 scope 的样本” | 同册 03 `@dsh-external/workflow`、04 `@limuyang2/dsh-agent-team` 也带 scope | 删“唯一” |
| “作者明说不做 worktree” | 源码无 worktree；唯一相关句是 [`docs/quality-gates.md:83`](https://github.com/NanmiCoder/dsh-agent-teams/blob/3331b903f0e954d59ac69be1a75fd4fd7e1de20e/docs/quality-gates.md#L83-L83) 的一条任务约束（“不要一次做独立 git worktree 隔离”），不是 README 设计边界 | 降级为“源码没有 worktree 支持” |
| 安装 `dsh plugin add …@0.1.28` | README 的精确命令是 `dsh plugin --profile web add --save-exact …@0.1.28` | 按 README 改，或注明 profile 可换 |
| 卡头“证据级别 observed（源码逐文件读过）”，无证据链行/本 memo 链接 | EVIDENCE §2.2 要求卡头有“证据链”行并链到本 memo | 卡头补“证据链：[`01-agent-teams-源码复核.md`](01-agent-teams-源码复核.md)” |
| 2592★ / 222 fork / npm 50,995 次/月 | 2026-11-01 重取：2610★ / 223 fork；npm last-month 50,995（窗口 2026-09-30–10-29） | 数字可留，但标采样日与窗口；这是外部指标，不是 `[SRC-TARGET]` |

## 未运行与 [OPEN]

- `[OPEN]` 未比对 `lib/git-artifact-stamp.json` 的 `source`/`output` 哈希（兄弟复核做过，见 [`17_协作-dsh-agent-teams-源码复核.md`](../../../leverage-reshape-product/plugin/_证据/17_协作-dsh-agent-teams-源码复核.md)）；npm↔tag 的同源判断只由七个服务端模块的字节相同 + `README.md` 逐字节相同支撑。
- `[OPEN]` 60 s 租约在真实崩溃后的重投行为、以及两个 DSH 进程同 workspace 的覆盖顺序，本轮只有静态代码路径，未实测。
- `[OPEN]` `maxMembers` 是否蓄意对齐宿主 8：源码与注释均无表述；只有版本历史能证明时才可写成设计意图。
- `[OPEN]` 卡片对 `limuyang2/agent-team` 的对比（独立根 Agent、架构守卫禁止 `parentSession`/`delegationDepth`）不在本 memo 范围，未复核。
- `[OPEN]` 卡片的“过了 C+D+G”属本册门分类，不是目标源码事实，本 memo 不评。
- `[RUN] None`：未安装、未构建、未运行目标插件或其测试；未启动 DSH；未写任何真实 profile / `.agent-teams/`。本文全部结论来自固定 commit 的静态阅读 + rc.3 宿主包阅读 + 只读网络元数据。
