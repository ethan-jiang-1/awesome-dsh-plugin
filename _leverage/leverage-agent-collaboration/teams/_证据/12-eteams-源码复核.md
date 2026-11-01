---
title: "12 · 2507483326/dsh-eteams 源码复核"
domain: agent-teams
kind: evidence
positioning: "复核 dsh-eteams 0.2.21/HEAD：persona 走 startContinuable 请求参数在 rc.3 已不成立——该方法改名 startActivation，persona 也不再是启动参数。"
read_when: "核对 12 卡「persona 走请求参数」在 rc.3 是否成立、成员如何 spawn/重启恢复、版本坐标时。"
status: observed
updated: 2026-11-01
---

# 12 · `2507483326/dsh-eteams` 源码复核

> 复核对象：样本卡 [`12-2507483326-dsh-eteams.md`](../samples/12-2507483326-dsh-eteams.md)。
> 取证时点 2026-11-01。只读 GitHub（`git ls-remote` / `git clone` / `git show`）、npm registry（metadata + tarball 下载解包比对）与本机 `@deepseek-ai/dsh 0.2.1-rc.3` 安装树；**未安装、未构建、未运行插件、未跑测试、未启动宿主、未执行任何 `dsh` 命令**。
> 标签沿用 [`EVIDENCE.md`](../../EVIDENCE.md)：`[DOC]` 目标仓 README/docs 主张，`[SRC-TARGET]` 固定 commit 实现，`[SRC-DSH]` 本机 rc.3 发行包，`[TEST]` 测试源码，`[CI]` 同 SHA check-run，`[RUN]` 本轮实跑，`[OBS]` 判断。
> **主 pin（卡片坐标）**：卡片写「版本(本次读) `0.2.21`」→ npm `dsh-eteams@0.2.21` 的 `gitHead` = [`0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9`](https://github.com/2507483326/dsh-eteams/commit/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9)（2026-09-18T13:32:38+08:00，树内 `package.json` = `0.2.21`）。**下文未特别标注的目标仓行号均指这一 pin。**
> **现行 pin（今天装到的是什么）**：npm `latest = 0.2.22`，`gitHead` = [`cd6bc01ae511901e26c2b47d0a71e471dce262fd`](https://github.com/2507483326/dsh-eteams/commit/cd6bc01ae511901e26c2b47d0a71e471dce262fd) = `master` HEAD（2026-09-22T21:21:49+08:00），但该树 `package.json` 仍写 `0.2.21`。
> **一句话结论**：卡片读到的 `startContinuable({request:{persona, toolFilter}})` 这行**真在源码里**（0.2.21 与 HEAD 都在），但它**在 DSH 0.2.1-rc.3 上不成立**：rc.3 的 `ctx.subagents` 服务**没有 `startContinuable` 方法**（整棵安装树 0 命中），改名 `startActivation`；且 rc.3 的启动请求类型里**根本没有 `persona`/`toolFilter`**——两者只在「冷恢复时从持久化 descriptor v3 还原」这一条路上还活着。所以「persona 的合法路径是请求参数」是**面向 harness 0.1.x 的结论**（插件自己声明 `dsh-subagent: ^0.1.0-rc.6`、注释写死「harness 0.1.2」），不是 rc.3 的事实；卡片把它当成 rc.3 的机制，是**版本坐标错误**，不是摘录错误。
> **审计快照（重要）**：本 memo 审的是 **2026-11-01T04:49 读到的卡片**，即 git HEAD 里那一版（`updated: 2026-10-31`，与 `git diff` 的 `-` 侧一致）。**同日 05:04:30 该卡被并发改写**（不是本 memo 所为；本次会话只写了本文件）：positioning/takeaway/「一句话」/「设计思路」首段/版本行被改，其中版本行已补 `0f8aa30` 与「最新 0.2.22」，中心主张已改成「只对 0.1.x 成立」。因此下表**行号与引文一律按改写前版本**，第 1、4 行**已被那次改写覆盖**，其余行（尤其带 `childId` 的那段代码块）在改写后仍在。**引用前请对当前卡复核。**

## Provenance

| 项 | 值 | 核对方式 |
|---|---|---|
| 仓库 | [`2507483326/dsh-eteams`](https://github.com/2507483326/dsh-eteams)（MIT，作者「流川枫」）；**npm 0.2.16–0.2.21 的 `repository` 字段仍写 `.../eTeam.git`**，改名提交是 [`2114e78`](https://github.com/2507483326/dsh-eteams/commit/2114e78ed827900b5bb7d4b15e4598fb629a8c83)（2026-09-18T15:12:43+08:00，`修改地址`，把 `eTeam` 改成 `dsh-eteams`），晚于 0.2.21 发布 | `git clone` + `git log`、registry `repository`/`homepage` 字段逐版本对照 |
| npm 包 | `dsh-eteams`，**7 个版本** `0.2.16`–`0.2.22`；`latest = 0.2.22`，发布 `2026-09-22T13:33:54.196Z` | `registry.npmjs.org/dsh-eteams` |
| npm 近 30 天 | **1,251 次**（`2026-09-30:2026-10-29`，与卡片同窗口） | `api.npmjs.org/downloads/point/...` 返回 `{"downloads":1251}` |
| Stars | **2**（与卡片一致） | `img.shields.io/github/stars/2507483326/dsh-eteams.json` |
| **tag** | **一个都没有**：`git tag -l` 为空，`git ls-remote` 只有 `refs/heads/master` 与 `HEAD` | `git ls-remote`、clone 后 `git tag -l` |
| **npm 0.2.21 的 commit** | `gitHead = 0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9`；tarball 的 `package.json`、`cordis.patch.yml` 与 `git show 0f8aa30:<file>` **逐字节一致**；`README.md` 仅行尾差异（tarball 是 CRLF，树是 LF），内容相同 | 下载 `dsh-eteams-0.2.21.tgz` 解包后 `diff` |
| **npm 0.2.22 的 commit** | `gitHead = cd6bc01ae5…` = `master` HEAD；tarball 内 `package.json` 写 `0.2.22`，而**该 commit 树里的 `package.json` 写 `0.2.21`** | registry `dist.gitHead` + `git show cd6bc01:package.json` + 解包 0.2.22 tarball |
| 版本/`gitHead` 漂移 | `0.2.16`→`fabb667`（树 `0.2.16`，对齐）；`0.2.17`→`57c97d0`（树 `0.2.16`）；**`0.2.18`→同一个 `57c97d0`**（两版一个 commit，tarball 体积不同）；`0.2.19`→`398c1ce`（树 `0.2.18`）；`0.2.20`→`d17bda5`（树 `0.2.19`）；`0.2.21`→`0f8aa30`（树 `0.2.21`，对齐）；`0.2.22`→`cd6bc01`（树 `0.2.21`） | 七个版本的 `dist.gitHead` vs `git show <sha>:package.json` 版本逐行对照 |
| README 自述版本 | badge 写 **`0.2.18`**（[`README.md:10`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/README.md#L10)），0.2.21 与 HEAD 两棵树都是；与 `package.json` 的 `0.2.21`、npm 的 `0.2.22` **三处三个版本**（README 的 badge 自 0.2.18 起没再更新） | 两棵树 README 对读 |
| 卡片坐标 | 卡 L47 写「版本(本次读) `0.2.21`」，**全卡无 commit/tag pin**；`0.2.21` 确实是 npm 一个真版本，但截至卡片 `updated: 2026-10-31` 已**落后 latest 五周**（0.2.22 发布于 2026-09-22） | 卡 L47 vs registry 时间线 |

**错位结论**：

1. **「0.2.21」是真实且可复现的坐标**——这点比 10 卡（expert-mode）干净：npm 0.2.21 = `0f8aa30`，tarball 与树一致。缺的只是卡片没写 commit，读者无法知道 0.2.21 对应哪棵树。
2. **但卡片把 0.2.21 当成了「本次读」的现状**：npm 上已有 0.2.22（`cd6bc01`，5 周前），仓库 HEAD 也是它。按卡片坐标能复现「用 `startContinuable` 传 `persona`」这个动作，但**复现不出卡片那段引文**（0.2.21 的成员调用没有 `childId`，见 SRC-TARGET §1）；而「这个插件是什么」的版本陈述已经过期。
3. **`gitHead` 在这个仓库不可当版本锚**：7 个版本里只有 2 个（0.2.16、0.2.21）的树内版本号与 npm 版本一致；0.2.17/0.2.18 还共用一个 commit。发布时显然是在工作树里改了 `version` 就 `publish`，没有回提交。**任何「按 commit 复现 npm 版本」的做法在这里都会差一版。**
4. **没有 tag，所以「pin tag」这条路不存在**；唯一可复现锚是 `dist.gitHead`（也就是发布那棵树）——但它对 0.2.22 又偏一版。要严格复现 0.2.22 的**字节**，只能用 tarball；要读**源码**，只能读 `cd6bc01` 并接受「tarball 是从版本号被临时改过的树打出来的」。

## DOC

`[DOC]` 只证明作者主张，不证明实现如此。

- 「**自包含**：构建产物已内联全部依赖，无运行时安装负担；状态存本机 SQLite（内置 `node:sqlite`），不联网、不上传」：[`README.md:26`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/README.md#L26)。tarball 只有 `lib/`（`index.js`、`client.js`、`tailwind.gen.css`、`types/`）+ `package.json`/`README`/`LICENSE`/`cordis.patch.yml`，**不发布 `src/`**——所以源码复核只能对仓库，不能对发布物逐行。
- 「不是『一个大模型假装多个人』，而是真实的多会话协作……每个成员在自己的子会话里独立干活」：[`README.md:23`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/README.md#L23)。
- 「通过角色中的 **system** 来定制你的所有会话」：[`README.md:36-42`](https://github.com/2507483326/dsh-eteams/blob/cd6bc01ae511901e26c2b47d0a71e471dce262fd/README.md#L36-L42)——这是 `persona` 主张的 DOC 侧表述（角色 → system 段）。**注意：这句在 0.2.21 的 README 里还没有**，是 `95be3fd`（`更新 read.me`，2026-09-22）加进去的——**引它就必须标 HEAD**，不能挂在 0.2.21 坐标下（本行 `[DOC]` 行号按 HEAD `cd6bc01`）。
- **作者自己写的宿主版本基线**：「harness 0.1.2 起 `registerContinuableSetup` 被宿主移除」：[`CLAUDE.md:65`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/CLAUDE.md#L65)；同理 [`members.ts:6`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/members.ts#L6)、[`:168`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/members.ts#L168)、[`notifier.ts:310-311`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/notifier.ts#L310-L311) 都以 `0.1.2` 为界。**仓库里没有任何一行提到 0.2.x 或 `startActivation`**（`grep startActivation src/` = 0 命中）。
- 设计文档把同一行 `startContinuable` 抄在方案里：[`docs/panelTaskCommission.md:22`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/docs/panelTaskCommission.md#L22)（`request: { prompt, parent, persona, toolFilter: {...}, agentOptions }`）。DOC 与 SRC 在这里一致——**但因为是一致的旧契约，两边一起错**。
- 安装自述：`dsh plugin --profile desktop add dsh-eteams`（[`README.md:51`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/README.md#L51)；同节 `:59` 还有一条旧名残留 `dsh plugin --profile desktop add C:\eTeam`）、`dsh --profile desktop --dump-config`（[`README.md:65`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/README.md#L65)）。**这两条在 rc.3 的 CLI 形状上是合法的**（`plugin` 子命令有 `requiredOption("--profile")` 且只转发 pnpm；`--dump-config` 是顶层选项，`dsh/lib/bin.js:105`/`:116-118`）——**是命令形状正确的一类**，不是 10 卡那种缺 `--profile` 的错误。
- 角色 → 会话人设的注入面另有一处自述：[`docs/development.md:15`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/docs/development.md#L15)（「面板选人写 `session-persona`」）。

## SRC-TARGET

本节所有目标仓链接 pin 到 commit。**A 组 = `0f8aa30`（卡片坐标 0.2.21）；B 组 = `cd6bc01`（HEAD/0.2.22）**，标 B 的行号只在该组内有效。

### 1. 成员 spawn：`persona` 确实在 `request` 里，但 `provider` 不是字面量 `'spawn'`

卡片引的「本域最值得逐字读的一行」在 **0.2.21** 树里实际是（注意：**没有 `childId`**）：

```ts
// src/host/runtime/members.ts:185-205 （pin 0f8aa30，即 npm 0.2.21）
const start = await env.ctx.subagents.startContinuable({
  provider: env.config.memberProvider,
  // 标签 = 显示名（宿主会话头部读 label）：名字在前，工牌后缀带 (任务, 工号)
  label: buildMemberLabel(row.mainTaskId ?? 0, row.employeeId ?? 0, row.name),
  request: {
    prompt: [
      { type: 'text', text: memberWelcome(team, row.name, template, taskBriefing(env, team, task)) },
    ],
    parent: captain,
    persona: personaText,
    toolFilter: { deny: [...MEMBER_DENIED_TOOLS] },
    ...(agentOptions !== undefined ? { agentOptions } : {}),
  },
  // 0.1.2 的入口对 signal 无保护调用 throwIfAborted()
  signal: env.signal ?? new AbortController().signal,
});
```

- [`members.ts:185-205`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/members.ts#L185-L205)；`persona: personaText` 在 [`members.ts:198`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/members.ts#L198)，`toolFilter` 在 [`members.ts:199`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/members.ts#L199)。
- **`childId` 是 0.2.22 才加进成员路径的**：`git diff 0f8aa30..cd6bc01 -- src/host/runtime/members.ts` 里 `+const childId = randomUUID()`、`+childId,`、`+registerMemberSession(childId, identity)`、`+unregisterMemberSession(childId)`、`+if (String(start.childId) !== childId) …` 全是新增行；0.2.21 的 `spawnMember` 只在 spawn **之后**用 [`:206`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/members.ts#L206) `registerMemberSession(String(start.childId), …)` 登记。HEAD 对应块是 [`members.ts:202-223`](https://github.com/2507483326/dsh-eteams/blob/cd6bc01ae511901e26c2b47d0a71e471dce262fd/src/host/runtime/members.ts#L202-L223)（`childId` 预留 `:192`、预登记 `:199`、`persona` `:216`）。
- **由此得出一条比卡片更要紧的坐标结论**：卡片片段带 `childId`，**在 0.2.21 的成员路径里不存在**。它更贴的是同树里的**领队**调用（[`captainAgent.ts:422-435`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/captainAgent.ts#L422-L435)，那里 0.2.21 就有 `childId: spawnChildId`），或者 0.2.22 的成员调用。**卡片自称「0.2.21」但引的是领队形状/HEAD 形状**——版本坐标与引文自相矛盾。
- **其余与卡片片段的差异**：① `provider` 是 `env.config.memberProvider`，不是字面量 `'spawn'`——默认值才是 `'spawn'`（[`config.ts:52`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/config.ts#L52) `raw?.memberProvider ?? 'spawn'`，schema 默认 `:39`；bundle patch 也显式写 `memberProvider: spawn`）；② 卡片省略了 `signal`；③ `label` 走 `buildMemberLabel(主任务号, 工号, 名字)`；④ `prompt` 是内容块数组。**方向（persona 在 request 里）对，逐字引文对不上它自己标的版本。**
- `persona` 文本不是裸的 `template.persona`，而是「`personaMd` 全文 → `executionPrompt` → 兜底人设」三级回退、再 `neutralizeInterpolation(...)` 转义（[`members.ts:161-166`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/members.ts#L161-L166)）。转义的原因写在注释里：**「宿主对系统提示段做严格 `{{变量}}` 插值，用户 md 里的花括号引用会让整段装配抛错」**——这其实是对 rc.3 同款严格插值的防御，说明作者踩过宿主的插值契约，却没踩到「方法改名」这一层。
- 成员的工具面只靠 `toolFilter.deny` 收窄：`MEMBER_DENIED_TOOLS`（[`members.ts:68-`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/members.ts#L68)）把 `eteams_create_team`/`eteams_add_member`/`eteams_create_task`/`eteams_update_task` 等管理工具拒之门外。

### 2. 领队派发：同一条路径 + 一道**前置能力门**

- 领队 spawn 是同一个调用：[`captainAgent.ts:422-435`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/captainAgent.ts#L422-L435)（`persona` 在 `:430`，`toolFilter: { deny: [...CAPTAIN_CHILD_DENIED_TOOLS] }` 在 `:431`，`childId: spawnChildId` 在 `:426`）。
- **唯一一处能力探测**就在它前面：[`captainAgent.ts:297-301`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/captainAgent.ts#L297-L301)

  ```ts
  if (
    subagents?.startContinuable === undefined ||
    (subagents?.sendMessage === undefined && subagents?.followup === undefined)
  ) {
    throw new ETeamsError('子代理服务不可用，无法派发领队子代理');
  }
  ```

  **注意这条守卫的判定对象是「方法存在性」。** 在 rc.3 上 `startContinuable` 恰好不存在，所以领队路径会走这条例外——错误文案说「服务不可用」，而实际是「服务在、方法改名了」。**误导性诊断**，不是缺失诊断。
- **成员路径没有这道门**：`spawnMember` 直接调（[`members.ts:185`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/members.ts#L185)），没有 `=== undefined` 检查。构建子代理有（[`builderPhases.ts:114-120`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/builderPhases.ts#L114-L120)，缺能力返回 false）。**同一个宿主缺口，三条路径三种表现。**

### 3. 成员何时被 spawn（不是建团队时，是首次指派时）

- 调用点只有一处：[`assignment.ts:1152`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/assignment.ts#L1152) `row.sessionId = await spawnMember(env, team, row, captain, task)`。成员**行在指派前就存在**（`task_members` 副本行），子会话是派发帧内才建。
- 失败包装成工具级错误并带提示：[`assignment.ts:1153-1158`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/assignment.ts#L1153-L1158)（`成员「x」启动失败` + `检查成员模型路线/子代理配置后重试`）。在 rc.3 上这条提示会指向「配置」，而根因是宿主方法改名——**又一次误导性归因**。
- 原子性意图写在注释里：「start 失败直接抛，调用方尚未改任何状态」（[`members.ts:138`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/members.ts#L138)，`spawnMember` 在 `:146`）。**0.2.21 的实现只是「spawn 成功后再登记」**（`:206`），没有预留 id、没有回滚；「先登记后 spawn → 失败撤销预登记」那套是 **0.2.22 才加的**（HEAD `members.ts:192`/`:199`/`:225`/`:229-230`，来源 commit message：「领队的文本出现在了子成员中」）。卡片没提这个版本差异，本节按 0.2.21 写。

### 4. 状态归属、锁、重启恢复

- **写事务**：`withTeamTx` 在一个同步 `BEGIN IMMEDIATE … COMMIT` 里跑，事务内禁止 `await`（[`store.ts:118-140`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/state/store.ts#L118-L140)，`db.exec('BEGIN IMMEDIATE')` 在 [`store.ts:129`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/state/store.ts#L129)）。卡片「SQLite `BEGIN IMMEDIATE` 做跨调用事务」成立。
- **锁**：进程内 promise 链互斥（[`lock.ts:1-46`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/state/lock.ts#L1-L46)），文件头明写 `no cross-process file locking (single-writer assumption, NFR-03)`（[`lock.ts:3`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/state/lock.ts#L3)）。卡片「进程内团队锁」成立，且它**只串行化状态写**，不串行化成员的文件写。
- **注册表是进程内的**：`const memberSessions = new Map(...)`（[`usage.ts:74`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/usage.ts#L74)）；领队侧 `captainChildren = new Map`（[`captainChildRegistry.ts:18`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/captainChildRegistry.ts#L18)）。**重启即空**，与卡片一致。
- **跨重启的持久面**是 SQLite 列：`task.session_id`（v5 迁移补列，[`db.ts:450-458`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/state/db.ts#L450-L458)）与 `task_members.session_id`（v6 把 `main_session_id`/`child_session_id` 合并，[`db.ts:484-495`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/state/db.ts#L484-L495)）。卡片「按任务行 `session_id` 快照冷恢复」**方向对**，更准确说是「任务行 + 成员行两处 session 快照」。
- **唤醒/冷恢复链**：`wakeMember` 先按「成员登记表 → 本任务主会话快照 → 全队主会话快照 → 面板心跳 `presence.json`」解析活父锚（[`notifier.ts:297-328`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/notifier.ts#L297-L328)，心跳文件在 [`roleBuilder.ts:221-228`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/roleBuilder.ts#L221-L228)），全离线时用 `agents.resume` 按持久化会话 id 复活主会话（[`assignment.ts:161-178`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/assignment.ts#L161-L178)），再 `deliverToChild` 投给成员实例行的 `sessionId`。
- `deliverToChild` 是能力探测分发：有 `sendMessage` 走 `sendMessage(parent, childId, content, {signal})`，否则退回 `followup`（[`base.ts:410-437`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/base.ts#L410-L437)）。**这两个方法 rc.3 都还在**（见 SRC-DSH §4），所以「重启后把邮件投给已存在的成员会话」这条链在 rc.3 上**原理上仍可用**；断的是「新建成员」。
- **边车**：`<stateRoot>/captain-turn/<taskId>.json`（[`captainAgent.ts:121-142`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/captainAgent.ts#L121-L142)），派发前 `await markCaptainTurn(...)`（[`captainAgent.ts:387`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/captainAgent.ts#L387)）——「先落盘再投递」**成立**。但**边车里装的是领队的回合任务（`kind` + `message`），不是「要投给成员的内容」**；成员投递走的是邮箱表 + `wakeMember`（[`members.ts:255-285`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/members.ts#L255-L285) `sendAssignmentInTx` 事务内落库、`:285` 返回的唤醒动作在 COMMIT 后执行）。
- `atomicWriteText`：同目录临时文件 + `rename`；遇到 `EPERM/EACCES/EBUSY/EEXIST/ENOTEMPTY` 重试（`attempt < 3` 时 50ms 后再来），**第 4 次仍失败就 `writeFile(file, content)` 直接覆盖**（[`store.ts:50-77`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/state/store.ts#L50-L77)）。卡片「重试 3 次后退化为直接写」**成立**（4 次尝试 = 3 次重试）。它作用于边车/心跳/父锚文件，**不作用于团队状态**（后者已全走 SQLite）。
- **`stateDir` 硬编码**：bundle patch 里写死 `stateDir: C:/Users/epat/.eteams`（[`cordis.patch.yml:20`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/cordis.patch.yml#L20)）。解析器 `stateRootFor` 用 `^[a-zA-Z]:[\\/]` **在任意平台**把它当绝对路径放行（[`base.ts:147-156`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/base.ts#L147-L156)）。**源码级推论**：在 macOS/Linux 上这个字符串不是 POSIX 绝对路径，会被 `node:fs` 按进程 cwd 解析成 `<cwd>/C:/Users/epat/.eteams/`——即在工作区里凭空出现一个名为 `C:` 的目录，**与注释宣称的「全局单库、所有工作区共用」正好相反**（未实跑，见 [OPEN]）。
- **`workRoot` 配置没接线**：[`docs.ts:30`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/docs.ts#L30) 注释直说「与既有硬编码一致，`config.workRoot` 未接」。patch 里暴露的 `workRoot: teams` 是**装饰性配置**。
- **冲突裁决**：成员 spawn 时不传 `cwd`（`members.ts:185-205` 的 spec 里没有 `cwd`），所以子会话 cwd 由宿主继承父级；成员看到的任务目录是**简报文本里的绝对路径**（`taskBriefing`，[`members.ts:121-142`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/src/host/runtime/members.ts#L121-L142)）。**没有 per-member worktree、没有文件租约、没有 claim**；同一主任务下的成员共享那个任务目录。卡片「冲突裁决 **不做**；成员共享同一工作区」成立（严格说是「共享同一任务目录」，且所有子会话继承同一进程 cwd）。

## SRC-DSH

以下均指本机 `@deepseek-ai/dsh 0.2.1-rc.3` 安装树（`/Users/bowhead/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai/`）。**只读源码，未执行。**

### 1. `startContinuable` 在 rc.3 **不存在**——这是本卡最关键的一条

- 对整棵安装树（含 `.js`/`.ts`/`.d.ts`/`.md`）grep `startContinuable`：**0 命中**。`ctx.subagents` 的服务面是 `SubagentRuntime`（模块增广：`dsh-subagent/lib/types/index.d.ts:62-65`），它暴露的两个启动重载都叫 `startActivation`（`dsh-subagent/lib/types/index.d.ts:135`、`:145`；实现 `dsh-subagent/lib/index.js:3036`）。
- 服务文档也换了名字：`dsh-subagent/README.md:61` 写 `startActivation({ provider, label, request, signal, delivery })`；`:89` 写「**Fulfillment is publication.** `startActivation()` returns only after the child is accepted…」。全树**没有 deprecated 别名、没有 shim、没有 fallback**。
- 因此 `env.ctx.subagents.startContinuable(...)` 在 rc.3 里就是 `undefined is not a function`（TypeError）。eteams 自己那道守卫会先命中领队路径，成员路径则直接撞 TypeError。
- **`startActivation` 的 spec 与 eteams 声明的 `startContinuable` spec 也不同**：`SubagentActivationSpec` = `{ provider, label, childId?, request, signal, delivery }`（`dsh-subagent/lib/types/types.d.ts:25-39`），其中 **`signal` 与 `delivery` 都是必填**，`childId` 是 branded `SessionId`。eteams 的本地声明（`base.ts:38-54`，**是它自己的 `RuntimeContext` 子集，不是宿主类型**）里 `signal?:`，也没有 `delivery`。所以就算只把方法名改掉，参数形状也不完整对齐。

### 2. `persona` / `toolFilter` 已经**不是启动参数**了

- rc.3 的启动请求类型 `SubagentStartRequest`（`dsh-subagent/lib/types/types.d.ts:127-172`）字段是：`cwd`、`agentPreset`、`label`、`prompt`、`parent`、`signal`、`agentOptions`、`outputSchema`、`maxDepth`。**没有 `persona`，没有 `toolFilter`。**
- 运行时也不读：`startLocal` 组装 descriptor 时只取 `mode/provider/label/agentProvider/agentModel/agentReasoningEffort`（`dsh-subagent/lib/index.js:1399-1408`），传给 materialize 的组合是 **`composition: { agentPreset: request.agentPreset }`**（`lib/index.js:1452`）——`persona`/`toolFilter` 根本没进组合。
- 能力校验也不会拦：`assertCapabilities`（`lib/index.js:3311-3330`）只检查 `agentPreset`/`agentOptions`/`outputSchema`/`maxDepth` 四项 capability，**未知键既不报错也不生效**。⇒ 在 rc.3 上把 `persona` 塞进 request 是**静默无效**（这比抛错更难查）。
- 唯一还在读 `persona`/`toolFilter` 的地方是**冷恢复**：descriptor v3 白名单含这两个键（`lib/index.js:579-587`），重挂时 `composition: { agentPreset, persona: descriptor.persona, toolFilter: descriptor.toolFilter }`（`lib/index.js:2174-2181`），再由 `applyChildOverrides` 落成 `deployment:persona-prefix` 系统段与 `tools.restrict`（`lib/index.js:384-396`）。**这是「还原历史 descriptor」，不是「接受启动参数」。** 而且新宿主创建的子代理**不会**把 persona 写进 descriptor（见上面 `index.js:1399-1408`），所以这条还原路只对旧宿主留下的会话有意义。
- 结论：rc.3 上 persona 的**唯一合法创建路径是 agent preset**（`agentPreset` 选择 + preset 里的 `dsh-persona`）。`dsh-tool-subagent` 的 config 守卫也把话说死了：`for (const field of ["persona", "toolFilter"]) if (Object.hasOwn(config, field)) throw new Error("tool-subagent: ${field} is no longer supported; configure persona and tool plugins in an Agent Preset and select it with agentPreset (spawn only)")`（`dsh-tool-subagent/lib/index.js:355`）。**config 抛错、request 静默忽略——两条都不是「合法路径」。**

### 3. 其余 seam 在 rc.3 的现状（决定「重启后还能做什么」）

| eteams 期望 | rc.3 实际 | 证据 | 判断 |
|---|---|---|---|
| `subagents.startContinuable(spec)` | **没有** | 全树 0 命中；`startActivation` 在 `lib/types/index.d.ts:135/145` | **断（硬失败）** |
| `request.persona` / `request.toolFilter` | 不在类型、不被消费 | `types.d.ts:127-172`；`lib/index.js:1452` | **断（静默无效）** |
| `subagents.sendMessage(sender,target,content,{signal})` | 有，同形 | `lib/types/index.d.ts:167` | 通 |
| `subagents.followup(...)` | 无（被 `sendMessage` 取代；eteams 已双探测） | `base.ts:419-436` 双分支 | 通（走 sendMessage） |
| `subagents.interrupt(target,{kind:'ancestor',agent})` | 有 | `lib/types/index.d.ts:196` | 通 |
| `subagents.drainContinuableChildren` | 无 | 0 命中 | 通（eteams 探测缺省即跳过，`members.ts:243`） |
| `subagents.listChildren(...)` | 有（返回 `SubagentCatalogEntry[]`，eteams 声明的是 `SubagentChildEntry[]`，仅类型名不同） | `lib/types/index.d.ts:228` | 通 |
| `agents.resume({resumeSessionId,…})` | 有 | `dsh-agent/lib/types/index.d.ts:111`、`:184`、`:286` | 通 |

⇒ **重启恢复链（投递/冷恢复）在 rc.3 上仍可用；被掐断的是「新建成员/新建领队」这一层。** 一个在 0.1.x 上跑过、`task_members.session_id` 已有值的团队，在 rc.3 上理论上还能被唤醒续跑；一个**新团队**则在第一次指派就失败。

### 4. 依赖声明自己就排除了 rc.3

- `peerDependencies` 写 `"@deepseek-ai/dsh-subagent": "^0.1.0-rc.6"`（[`package.json:86`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/package.json#L86)），devDeps 固定 `0.1.0-rc.8`（[`package.json:163`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/package.json#L163)）。`^0.1.0-rc.6` 的语义是 `>=0.1.0-rc.6 <0.2.0`——**0.2.1-rc.3 落在声明范围之外**。
- 但所有 dsh peer 都是 `optional: true`（[`package.json:130-132`](https://github.com/2507483326/dsh-eteams/blob/0f8aa3055dd5a41bb899f1895f2e5d91c01da8d9/package.json#L130-L132)），所以 pnpm/npm **不会**因版本不符报错，插件照样装得上、照样激活——**失败推迟到第一次派发**。这解释了为什么「装得起来」不等于「跑得起来」。

## TEST

`[TEST]` 只核对存在性，不证明通过：

- 测试**存在且规模不小**：`tests/` 下 **52 个 `*.test.ts`** + `tests/support/`，`vitest.config.ts` 用 `pool: 'threads'`、`include: ['tests/**/*.test.ts']`；`package.json` 有 `test: "vitest run"`、`verify: "node scripts/verifyM0.mjs && vitest run"`、`prepublishOnly` 串了 build/typecheck/lint/test。
- **但宿主被整体 fake 掉了**。`startContinuable` 在 4 个测试文件里被手写成假方法：`tests/captainDispatch.test.ts:73-86`、`tests/lifecycle.test.ts:100-`、`tests/webui.test.ts:117/229/2869/2974`、`tests/buildWait.test.ts:130`（行号按 HEAD `cd6bc01`）。这些 fake 的 spec 类型宽窄不一——`lifecycle` 的只声明 `{provider,label,childId,request:{parent,toolFilter}}`（`persona` 没进类型），`captainDispatch` 的才带上并断言 `persona`——但**没有一处把「宿主真的认这个方法/这个参数」当契约**，测试**编码了同一个假设**，因此**永远发现不了 rc.3 的方法改名**。
- 唯一直接验证「persona 走请求参数」的断言在 `tests/captainDispatch.test.ts:277-278`：`expect(spec.request.persona).toBe(captainChildPersona('{{eteams_leader_handbook}}'))`。**这是对插件自己调用形状的单元断言，不是对宿主契约的验证**——它证明「我们这样调」，不证明「宿主认这个参数」。
- 重启/快照相关意图有覆盖（`tests/lifecycle.test.ts:1468`、`:1537-1538` 讨论 `registerCaptainChild → startContinuable` 与预留 id 的先后），仍是 fake 层。
- **没有任何集成测试或 contract test 跑真实 DSH**；没有针对 peer 版本范围变化的门。`[OPEN]`：测试套件本轮未执行（禁止跑），因此「是否通过」未验证。

## CI

- 仓库**没有 `.github/`**，也没有 `.gitlab-ci.yml`/`Jenkinsfile`/`.circleci/`/`.travis.yml`。全树 `*.yml|*.yaml` 只有 `pnpm-lock.yaml`、`pnpm-workspace.yaml`、`cordis.patch.yml` 三个**非 CI** 文件。
- 因此没有同 SHA 的 check-run 可引；`[CI]` 在本 memo 里只能是「不存在」。`prepublishOnly` 里的 build/typecheck/lint/test 是**本地发布前脚本**，不是 CI，也没有证据表明 0.2.21/0.2.22 发布时真的通过（`[OPEN]`）。

## RUN

`[RUN] None`。

本轮只做了只读操作：`git ls-remote`、`git clone`、`git show/diff/log`、`npm registry GET`、`curl` 下载 0.2.21/0.2.22 tarball 并解包比对、`grep/read` 本机 rc.3 源码、`curl` 取 shields/npm downloads。**没有** `npm install`、**没有** `pnpm build`、**没有** `vitest`、**没有**运行 `dsh`、**没有**挂载/激活插件、**没有**启动 Web GUI。

因此本 memo 里「rc.3 上派发会抛 ETeamsError / 成员 spawn 会 TypeError」「POSIX 上 `C:/…` 会落成工作区里的 `C:` 目录」都是**源码契约推断**，不是运行时观察；要升级为 `[RUN]` 必须实装实跑。

## 卡片偏差表（card-deviation table）

> **行号口径**：下表「卡片断言（行）」的 L 编号指向 **git HEAD 版卡片（2026-11-01T04:49 快照）**；05:04:30 的并发改写插入了一行「证据链」并改写了若干段，编号整体后移约 1 行。第 1、4 行**已被那次改写覆盖**（版本行已补 pin、中心主张已限定为 0.1.x），保留在此是为了记录「改写前它错在哪」。

| # | 卡片断言（行） | 证据 | 判定 |
|---|---|---|---|
| 1 | 「版本(本次读) `0.2.21`」（L47），全卡无 commit pin | npm 0.2.21 = `0f8aa30`（tarball 与树一致）；但 `latest = 0.2.22` = `cd6bc01`，早于卡片 `2026-10-31` 五周；仓库 **0 tag** | **可复现但已过期**：版本真、pin 缺、现状陈述落后一版（**05:04 改写已补 pin 与 latest**） |
| 2 | 仓库 `2507483326/dsh-eteams`（L45） | 当前名正确；但 0.2.21 的 npm metadata 仍写 `eTeam`，改名提交 `2114e78` 晚于 0.2.21 发布 | **成立**（名字对；版本与仓名跨了一次改名，卡片未记） |
| 3 | `startContinuable({provider: 'spawn', childId, label, request:{prompt,parent,persona,toolFilter,agentOptions}})`（L27-31、L66，注明「成员创建调用」） | `members.ts:185-205`（0f8aa30）**没有 `childId`**；`provider` 是 `env.config.memberProvider`、有 `signal`、`label` 走 `buildMemberLabel`、`prompt` 是内容块数组。`childId` 在 0.2.21 只出现在**领队**调用（`captainAgent.ts:426`），成员路径要 0.2.22（`cd6bc01`）才加 | **半成立、且引文与自报版本不符**：persona 在 request 里 ✅；`childId`+字面量 `'spawn'` 的写法既不是 0.2.21 的成员调用（无 childId），也不是领队调用（provider 是 config） |
| 4 | 「这证明了 `persona` 的合法路径是请求参数」（L13、L22，卡片的**中心主张**） | rc.3：`startContinuable` 不存在（全树 0 命中），`SubagentStartRequest` 无 `persona`，`startLocal` 只传 `{agentPreset}`；config 侧 `dsh-tool-subagent:355` 也抛错 | **在 rc.3 不成立**；只在 harness 0.1.x 语义下成立（插件 peer 声明 `^0.1.0-rc.6`、注释写死 0.1.2）。**05:04 改写已把这条限定为 0.1.x** |
| 5 | 「这解释了 `dsh-expert-mode` 的 `persona` 配置会挂载失败而它不会」（L22、L33） | rc.3 上**两者都失败**：expert-mode 是 config 命中守卫**抛错**；eteams 是方法不存在/参数被忽略 | **对照失效**：同一宿主版本上，两条路都到不了「persona 生效」 |
| 6 | 「成员=真 continuable 子代理」「同进程父子」（L14、L5） | `provider: spawn` 默认 + 子会话持久化，形态确实是 continuable 子代理；但 rc.3 上无法建立 | **条件成立**：形态描述对，前提（宿主 0.1.x）没写 |
| 7 | 「投递用 `deliverToChild` + 预落盘 `captain-turn/<taskId>.json` 边车，所以队长回合开始前该投给成员的内容已落地」（L35、L60） | 边车确实 `await` 在投递前（`captainAgent.ts:387`），但装的是**领队回合任务**；成员投递是邮箱表 + `wakeMember`（`members.ts:255-285`） | **机制对、对象错**：边车≠成员内容边车 |
| 8 | 「注册表是进程内的、重启即空，另有一层按任务行 `session_id` 快照冷恢复」（L22、L37） | `memberSessions`/`captainChildren` 都是 `Map`；`task.session_id` + `task_members.session_id` 持久；`wakeMember` → 锚点链 → `agents.resume` | **成立**（补充：是「任务行 + 成员行」两处快照） |
| 9 | 「SQLite `BEGIN IMMEDIATE` 做跨调用事务；进程内团队锁」（L35、L58、L68） | `store.ts:129` 同步事务；`lock.ts:3` 明写无跨进程文件锁、单写者假设 | **成立**（补充：锁只保护状态写，不保护成员文件写） |
| 10 | 「冲突裁决 **不做**；成员共享同一工作区」（L59、L6） | 不传 `cwd`、无 per-member worktree、无 claim/租约；简报只把任务目录当文本给出 | **成立**（严格说共享的是「同一任务目录 + 同一继承 cwd」） |
| 11 | 「`atomicWriteText` 重试 3 次后退化为直接写」（L39、L60、L74） | `store.ts:50-77`：4 次尝试、第 4 次失败直写 | **成立**（补充：只作用于边车/心跳，团队状态已走 SQLite） |
| 12 | 「patch 里写死作者 `stateDir: C:/Users/epat/.eteams`」（L39、L73） | `cordis.patch.yml:20` 逐字存在；`stateRootFor` 用正则把盘符当绝对路径放行 | **成立**；补充：POSIX 上会落成进程 cwd 下的 `C:` 目录，与「全局单库」意图相反 |
| 13 | 「构建产物内联全部依赖 + `node:sqlite` 内置；不联网/不上传」（L52、L69） | tarball 只发 `lib/`；`node:sqlite` 经 `createRequire` 晚加载（`db.ts:146`）；「不联网/不上传」只有 README 自述 | **部分成立**：内联与 `node:sqlite` ✅；网络行为**未做全量审计** → `[OPEN]` |
| 14 | 「市场搜 ETeams 一键装；或 `dsh plugin --profile desktop add`」（L50） | rc.3 `plugin` 子命令确实 `requiredOption("--profile")` 并转发 pnpm；`--dump-config` 存在 | **命令形状合法**（不是本册另一张卡那种缺 `--profile` 的错误）；`desktop` profile 是否存在、能否装上未跑 → `[OPEN]` |
| 15 | 「2★ / 1,251 次/月」（L15、L49） | shields `2`；npm point `1251`（2026-09-30..2026-10-29） | **成立**；「本域第四高」未复采样域内其它包 → `[OPEN]` |
| 16 | 卡头自称「版本(本次读) `0.2.21`」+「源码逐文件读过」（L9、L14、L47） | 卡片引文里的 `childId` **在 0.2.21 的成员调用里不存在**（0.2.21 只在领队调用带 `childId`；成员路径 0.2.22 才加）。所以那句「成员创建调用」要么抄的是**领队**调用，要么读的是 `cd6bc01`/HEAD | **自报版本与引文形状不符**：不能据此断定作者读了哪棵树，但**「0.2.21 的成员调用」这个说法不成立** |

## [OPEN]

1. **harness 0.1.x 是否真的消费 `request.persona`**：这是卡片中心主张成立与否的另一半。插件 peer 基线是 `0.1.0-rc.6`/`0.1.0-rc.8`，本机只装了 rc.3；**不安装旧宿主就无法验证** 0.1.x 的 `startContinuable` 是否读 `request.persona`。rc.3 的 descriptor v3 仍保留 `persona`/`toolFilter` 键，可作旁证（说明历史上它们进过子代理组合），但**不是证据**。`[OPEN]`
2. **改名的确切版本**：`startContinuable` → `startActivation` 发生在 0.2.0 还是某个 rc？rc.3 树里已无任何旧名痕迹，也没有 changelog/migration 段落可引。`[OPEN]`
3. **eteams 在 rc.3 上的真实运行表现**：静态推断是「领队派发抛 `ETeamsError('子代理服务不可用…')`、成员 spawn 抛 TypeError、构建子代理静默跳过」；未实跑。`[OPEN]`
4. **`eTeam` → `dsh-eteams` 的 HTTP 跳转**：`git ls-remote https://github.com/2507483326/dsh-eteams` 成功且 HEAD 与 `master` 一致，说明旧地址可达；但 `curl -I` 本轮返回 `000`（网络超时）、GitHub API `403`（限流），**没有观测到 301 的 Location**。`[OPEN]`
5. **npm 0.2.22 的 tarball 是否真由 `cd6bc01` 构建**：tarball 只发 `lib/`，无法与 `src/` 逐行对；`gitHead` 指向树内版本号为 `0.2.21` 的 commit，说明发布前改过 `version`。`[OPEN]`
6. **「本域第四高下载」的排序**：只复核了 eteams 自己的 `1251`，没有在同一窗口重采本域其它 13 个包。`[OPEN]`
7. **客户端半边与 rc.3 的兼容性**：插件声明 5 个 `dsh-client-*` 注入（`package.json` 的 `dsh.client.inject`），本 memo 只审宿主端 `subagents` seam，**没有审客户端 slot/props 是否仍对齐**。`[OPEN]`
8. **测试是否通过**：52 个测试文件本轮未执行（禁止 `pnpm`/`vitest`），「有测试」不等于「测试绿」。`[OPEN]`
9. **「不联网/不上传」**：未对 `src/` 做全量网络调用审计（`fetch`/`http`/`net`/`ws` 逐点核对）。`[OPEN]`
10. **`stateDir` 在 POSIX 上的实际落点**：`<cwd>/C:/Users/epat/.eteams/` 是源码推断（`stateRootFor` 正则放行 + `node:fs` 相对解析），未实跑确认目录是否真被创建。`[OPEN]`
