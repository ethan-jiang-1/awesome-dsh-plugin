---
title: "源码复核：Mlte0907/dsh-teams-x 0.11.5（未发布版本，跨边界样本 05）"
domain: cross-boundary
kind: evidence
positioning: "钉 master 9c56100（清单 0.11.5，无 tag/无 release）：npm 仍 0.2.0 且 postinstall 缺件；「官方三条限制」是册子的对照，不是样本自评。"
read_when: "核对 05 号样本的源码依据，或要改它的机制断言时。"
status: observed
updated: 2026-11-01
---
# 源码复核：`Mlte0907/dsh-teams-x` 0.11.5

> 取证时点 2026-11-01（Asia/Shanghai）。只读 `registry.npmjs.org`（packument、tarball、attestations）、GitHub API（repo/tags/releases/commits/contents/check-runs/workflow runs/job log）、`codeload` 归档、本机 DSH 发行包，以及 `/tmp` 内的解包与 `shasum -a 256` 比对；**未安装、未构建、未运行目标插件，未启动 DSH，未写任何真实 profile 或 `.teams-x/`**。
> 坐标：`[SRC-TARGET]` = commit [`9c56100810bdfbabb03477c882ad1612b8138668`](https://github.com/Mlte0907/dsh-teams-x/commit/9c56100810bdfbabb03477c882ad1612b8138668)（master HEAD，`package.json` 0.11.5）的 `src/`；本文所有行号钉在该 commit。**0.11.5 没有 tag、没有 release、从未上 npm**，所以坐标只能是「commit + 清单版本」。`[SRC-DSH]` = 本机 `@deepseek-ai/dsh@0.2.1-rc.3`（`dsh-subagent@0.2.1-rc.3`）。`[DOC]` 只证作者主张，`[TEST]` 只证覆盖意图，`[CI]` 只引同 SHA 的 check-runs，`[OBS]` 是推断。
> 阅读范围：`src/{index,quality,scheduler,state,tools,members,compat}.ts` 与 `src/client/live-activity.ts` 的机制段，`README.md`/`README_ZH.md`/`CHANGELOG.md`/`ACCEPTANCE.md`，`sdd/{spec,design}.md`，`scripts/full-functional-test.mjs`，`.github/workflows/verify.yml`；**没有逐行读完 11,671 行 `src/`**，所以卡片「源码逐文件读过」这一自述不是本文能背书的范围。

## Provenance

- `[RUN]` npm `dsh-teams-x` **只有两个版本**：`0.1.0`（2026-09-06T19:01:50Z，`gitHead 195c5a2…`）与 `0.2.0`（2026-09-07T14:19:15Z，`gitHead 1217ddf…`，`dist-tags.latest`）。没有任何 `0.3.0`–`0.11.x`。→ **卡片写的 `0.11.5` 不是 npm 上存在的版本。**
- `[RUN]` 仓库默认分支 `master`，HEAD = [`9c56100810bdfbabb03477c882ad1612b8138668`](https://github.com/Mlte0907/dsh-teams-x/commit/9c56100810bdfbabb03477c882ad1612b8138668)（2026-10-20T16:02:08Z），其 [`package.json:3`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/package.json#L3-L3) 为 `"version": "0.11.5"`。
- `[RUN]` tag 共 8 个，最高 `v0.11.2` = `c2a132ea72fbf77bca9f2f290d688e3d977825ef`（2026-09-29）；release 也 8 个，最高 `v0.11.2`。**`v0.11.3`/`v0.11.4`/`v0.11.5` 都既无 tag 也无 release。**
- `[RUN]` 0.11.5 来自 `1b4dd5bc1a`（2026-10-11，`refactor(client): make the version follow package.json…`）把 `package.json` 从 `0.11.4` 改成 `0.11.5`；这是重构提交，不是 release 提交，也没有补 tag。
- `[RUN]` 所以 **npm↔tag↔commit 三方对齐不存在**，能钉的只有「master HEAD commit ↔ 清单版本 0.11.5」。`CHANGELOG.md` 里有 `## 0.11.5 (2026-10-11)` 一节（[`CHANGELOG.md:3-L7`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/CHANGELOG.md#L3-L7)），但 changelog 不是发布物。
- `[RUN]` npm `0.2.0` ↔ tag `v0.2.0`（`1217ddf4ebbfda87931558a48b0a176a8358f1b5`）：`README.md`、`README_ZH.md`、`cordis.patch.yml`、`package.json` 四个文件 `shasum -a 256` **逐字节相同**（README 两文件均为 `0f68d448…`，`package.json` 为 `e0b0de43…`）。tag 树里**没有 `lib/`**（`lib/` 到 `77253f26`，2026-09-23 才纳入版本控制），npm 包里的 56 个 `lib` 文件是该 tag 的构建物。→ npm 0.2.0 是 tag v0.2.0 的重建物，绑定靠 `gitHead` + 四文件字节相同；**没有 SLSA provenance**（`/-/npm/v1/attestations/dsh-teams-x@0.2.0` 返回 404），只有 npm 注册表签名。
- `[RUN]` 文件事实：npm 0.2.0 声明 `"postinstall": "node scripts/postinstall-check.mjs"`，但 `files` 白名单是 `[lib, assets/icons, cordis.patch.yml, README.md, README_ZH.md]`，tarball 里 `package/scripts` **0 个文件**。`[OBS]` 因此 `npm i dsh-teams-x` 会在依赖的 postinstall 阶段 `Cannot find module …/scripts/postinstall-check.mjs` 并以 `ELIFECYCLE` 失败（**本轮未执行安装**，是静态判定）——这正是 0.11.2 修掉的问题（[`CHANGELOG.md:50-L53`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/CHANGELOG.md#L50-L53)），修复从未发布。
- `[RUN]` 仓库根还入库了一个 `dsh-teams-x-0.2.2.tgz`（内部 `package.json` 版本 **0.2.2**、`engines` 没有 `dsh` 字段），而 README 说它「与源码同步构建」（[`README.md:15-L18`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README.md#L15-L18)）。→ **README 的推荐安装路径 A 装的是 0.2.2。**
- `[RUN]` 0.2.0 的 `lib/members.js:478` 仍调 `ctx.subagents.startContinuable(…)`，而 rc.3 上该函数已不存在（见 SRC-DSH）。`[OBS]` 即便 `--ignore-scripts` 绕过 postinstall，approve 后派生成员也会按 `CHANGELOG.md:29-L33` 描述的方式抛 `TypeError`（本轮未运行验证）。
- `[RUN]` 外部指标（2026-11-01）：**3★ / 0 fork**；npm `last-month = 89`，窗口 `2026-09-30`–`2026-10-29`（与卡片的 89 一致，但这是 0.2.0 的下载量）。License MIT（[`package.json:28`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/package.json#L28-L28)）。

## DOC（样本自己说的）

- `[DOC]` 宿主基线自相矛盾：README 称「原生面向 **DeepSeek Harness 0.2.0-rc.1**（`peerDependencies` 已声明 `>=0.2.0-rc.1`）」（[`README.md:9`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README.md#L9-L9)），而 `package.json` 的 `engines.dsh` 是 `>=0.2.1-rc.1 <0.3.0-0`（[:31](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/package.json#L31-L31)）、14 个 peer 是 `>=0.2.1-alpha.2`。0.11.3 的 changelog 已承认旧范围「在 semver 下根本不接受 0.2.1-alpha.2」（[`CHANGELOG.md:34-L41`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/CHANGELOG.md#L34-L41)），README 没跟着改。
- `[DOC]` 安装与复现：方式 A 用仓库自带 tgz（[:15-L18](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README.md#L15-L18)）；README:21 写「装完**重启宿主**（`dsh plugin add` 不会热加载新 bundle）」（[:21](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README.md#L21-L21)）——**卡片引的复现要点原文属实**；方式 B 就是卡片抄的那条 `npm i dsh-teams-x && dsh plugin --profile web add …`（[:23-L27](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README.md#L23-L27)）；方式 C 明说构建期需要同机 harness 源码 checkout（[:31](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README.md#L31-L31)）。
- `[DOC]` 质量门与自动返工：「质量门（v0.1）：requirements/implementation/verification/review/repair/integration 契约校验、完成规则（verdict=pass 才可完成、verify 失败必须 fail、inScope 路径审计、默认排除密钥文件）」（[:103](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README.md#L103-L103)）；「自动修复循环 … round 上限默认 3，`autoDerive` 可关」（[:73](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README.md#L73-L73)）。
- `[DOC]` 规模自述：「173 用例」（[:77](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README.md#L77-L77)）、「13 个 `teamsx_*` 工具」（[:79](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README.md#L79-L79)）。工具数属实（`lib/index.js` 与 `src` 都是 13 个）。
- `[DOC]` 中文 README 把机制写得比英文多：「对账兜底」队长会话消亡后由后台对账器回收（[`README_ZH.md:14`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README_ZH.md#L14-L14)）；修复回路「上限 3 轮、同源去重、源任务通过后级联取消」（[:15](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README_ZH.md#L15-L15)）；「停滞检测 … 停车超 30 分钟 / 运行超 60 分钟无进度 → 邮箱提醒队长（每次尝试至多一次）」（[:16](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README_ZH.md#L16-L16)）；「`teamsx_update_task({ progress })` 长任务心跳」（[:18](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README_ZH.md#L18-L18)）；「per-team 锁 + 成员级串行队列 + **默认跨进程文件锁**（`DSH_TEAMSX_FILE_LOCK=0` 关闭）」（[:23](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README_ZH.md#L23-L23)）。
- `[DOC]` **全仓没有卡片说的那张表**：`README.md`/`README_ZH.md`/`CHANGELOG.md`/`ACCEPTANCE.md`/`docs/`/`sdd/` 都找不到「官方三条限制逐条对照」，也没有「共享 checkout 未解决」「单进程未解决」这类自认。检索 `限制`/`隔离`/`单进程`/`owner`/`worktree` 只命中无关段落。全仓 `agent-teams` 字样只有两处（见 SRC-TARGET §13）。
- `[DOC]` 它真正自认的是另外几件事：真实实例验证交给使用者（[`README.md:61`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README.md#L61-L61)）；0.11.4 自认本机无 harness 检出、`pnpm verify` 未跑、CI 的 Runtime verification 在上一提交就已红、改动未在真实窗口目视（[`CHANGELOG.md:25`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/CHANGELOG.md#L25-L25)）；0.11.3 自认 typecheck/build/functional 全没跑、`lib/` 是照着 `src/` 手工镜像（[:45-L46](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/CHANGELOG.md#L45-L46)）。
- `[DOC]` §七「已知限制」只有四条：会话内卡片未渲染、浅色主题仅结构验证、成员会话跳转异常路径未测、CI strict typecheck 为 informational（[`ACCEPTANCE.md:267-L276`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/ACCEPTANCE.md#L267-L276)）——**与卡片写的两条完全不是一回事**。同一文件还把 `src/state.ts` 描述成「进程内锁」（[:306](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/ACCEPTANCE.md#L306-L306)），与 0.11.5 的默认跨进程锁冲突。
- `[DOC]` `sdd/` 确如卡片所说是 `/teamsx` 空态提示这一特性的三件套：`spec.md` 抬头就是 `teamsx_empty_hint`、代码基线 HEAD `da7cb82`/0.2.0、宿主 0.1.3-alpha.1（[`sdd/spec.md:1-L6`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/sdd/spec.md#L1-L6)），EARS 语法 + 验收条件（[:66-L68](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/sdd/spec.md#L66-L68)），非目标 O-1…O-7（[:144-L150](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/sdd/spec.md#L144-L150)），design 里的备选对比 → 裁决 → 理由（[`sdd/design.md:590-L607`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/sdd/design.md#L590-L607)）。**这套文档与团队架构无关，且基线停在 0.2.0。**

## SRC-TARGET（commit `9c56100`）

### 1. 「官方三条限制」：样本没有做这张对照

- `[SRC-TARGET]` 三条限制的原始出处是**册子**：`01-collab-topology.md:61-68` 逐字引官方 `dsh-experimental-agent-team` README 的 7 条已知限制，其中三条是「One process and one shared checkout」「No automatic ownership release」「No send retry guarantee … concurrent processes over one Team are unsupported」。
- `[SRC-TARGET]` 样本侧没有任何对应物：`src/` 里 `worktree`/`git` 调用 0 命中，`agent-teams` 全仓只有 2 处（§13），README 两个语种都不提这几条限制。**卡片把册子的对照写成了样本的自评。**
- `[OBS]` 就实现验证这三条：① 共享 checkout——成员以 `parent: captain` 派生、不传 cwd（[`src/members.ts:676-L692`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/members.ts#L676-L692)），仓内无 worktree/合并/文件版本检查，**未解决**；② 单进程——宿主 registry 是进程内 `Map`（见 SRC-DSH），插件有默认开启的跨进程文件锁但只串行化状态写入，**没有跨进程归属/派工**，**未解决但理由与卡片不同**；③ owner 不自动释放——搁浅回池 + 孤儿回池 + 提醒（§6/§7），**部分缓解**，但缓解手段与卡片点名的 `drainChildren`/退役守卫不是同一件事。

### 2. 质量门（建任务侧）

- `[SRC-TARGET]` 六种 quality kind 与两种写类：[`src/quality.ts:20-L25`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/quality.ts#L20-L25)。
- `[SRC-TARGET]` `validateCreateTask`（[:160](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/quality.ts#L160-L160)）：六种 quality kind 必须有非空 `objective` 与非空 `acceptance`（[:172-L178](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/quality.ts#L172-L178)）；`implementation`/`repair` 还必须有非空 `inScope` 与 `verify`（[:180-L186](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/quality.ts#L180-L186)）；`review` 只要求 `description` 非空（字符串存在性，不校验被审任务 id，[:188-L193](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/quality.ts#L188-L193)，注释自述这是 v0.1 的声明式做法）。
- `[SRC-TARGET]` 依赖必须存在；`repair`/`review` 不得依赖 `failed`/`cancelled` 任务（[:196-L205](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/quality.ts#L196-L205)）。
- `[SRC-TARGET]` 写类任务的 `inScope` 与其它**未终结**写类任务重叠即拒绝，要求串行化；已声明依赖的跳过、有悬空依赖的任务跳过（[:207-L225](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/quality.ts#L207-L225)）。
- `[SRC-TARGET]` `implementation` 在有 requirements 任务但尚无 pass 时被挡，除非它依赖该 requirements 任务（[:227-L238](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/quality.ts#L227-L238)）。
- `[SRC-TARGET]` 门在工具里真的被调用：锁内 `validateCreateTask`（[`src/tools.ts:1257-L1275`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/tools.ts#L1257-L1275)），staged 与 running 都走这条。

### 3. 质量门（完成侧）

- `[SRC-TARGET]` `evaluateQualityCompletion`（[`src/quality.ts:294-L355`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/quality.ts#L294-L355)）：`work` 直接放行（[:307](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/quality.ts#L307-L307)）。
- `[SRC-TARGET]` `review`/`requirements` 完成必须 `verdict='pass'`，且没有未解决的 `high`/`blocker` finding（[:310-L317](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/quality.ts#L310-L317)）；以 `needs_revision`/`reject` 判失败时至少要有一条 finding（[:318-L323](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/quality.ts#L318-L323)）。
- `[SRC-TARGET]` `commandsRun` 里只要有 `failed` 就**禁止** `completed`（[:327-L330](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/quality.ts#L327-L330)）。
- `[SRC-TARGET]` `implementation`/`repair`/`verification`/`integration` 完成还要求：`acceptanceResults` 覆盖每条 acceptance、`commandsRun` 覆盖每条 verify；`implementation`/`repair` 另需 `changedPaths` 且每条都落在 `inScope`（[:332-L351](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/quality.ts#L332-L351)）。
- `[SRC-TARGET]` **插件一条命令都不执行**：`src/` 内 `child_process`/`spawn`/`exec` 0 命中；`verify` 只是字符串清单，与成员上报的 `commandsRun` 做名字匹配（`verifyCovered`，[:265-L274](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/quality.ts#L265-L274)）。`changedPaths` 也是成员工具入参（[`src/tools.ts:1612`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/tools.ts#L1612-L1612)、[:1827](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/tools.ts#L1827-L1827)），没有 git/文件系统复核。

### 4. 防自审：只有提示词

- `[SRC-TARGET]` 「Do not approve your own implementation」出现在三处提示词：派工提示（[`src/scheduler.ts:371`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L371-L371)）、成员 persona 第 10 条「Do not mark your own implementation as review pass」（[`src/members.ts:622`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/members.ts#L622-L622)）、模型侧使用策略第 7 条（[`src/index.ts:102`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/index.ts#L102-L102)）。
- `[SRC-TARGET]` 代码里没有任何「reviewer ≠ implementer」断言；review 任务只要 `description` 非空即可建（§2）。→ 卡片「唯一的结构性防自审是提示词里一句」结论成立，只是实际是三处、并非结构性的。

### 5. 自动返工：派生 / 去重 / 级联 / 上限

- `[SRC-TARGET]` 默认上限 3：`DEFAULT_REPAIR_MAX_ROUNDS = 3`（[`src/scheduler.ts:63`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L63-L63)）；`verdictRequiresRepair` = `needs_revision`/`reject`（[:68-L70](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L68-L70)）。
- `[SRC-TARGET]` 触发点在 `teamsx_update_task` 之后：quality kind 且 verdict 需要返工才调 `triggerRepairLoop`（[`src/tools.ts:1872-L1877`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/tools.ts#L1872-L1877)）——所以**不止 review，requirements 打回也会派生**。
- `[SRC-TARGET]` `triggerRepairLoop`（[`src/scheduler.ts:681-L745`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L681-L745)）：`autoDerive === false` 直接返回（[:683-L684](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L683-L684)）；已有同源未终结 repair 兄弟则不派生（[:691-L702](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L691-L702)；`openRepairSiblingFor` [:112-L123](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L112-L123)）；`round >= maxRounds` 时给队长邮箱写一封信并停止（[:705-L726](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L705-L726)）。
- `[SRC-TARGET]` 派生体（`deriveRepairTask`，[:83-L103](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L83-L103)）：`dependencies=[failed.id]`、`round = 源.round + 1`、**assignee 继承失败任务**，且**不带** `objective`/`acceptance`/`inScope`/`verify`——它绕过了建任务门，契约字段为空。
- `[SRC-TARGET]` 级联取消：源任务 `completed` 时把同源 open repair 全部取消（[`src/tools.ts:1832-L1845`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/tools.ts#L1832-L1845)；`cancelSupersededRepairSiblings` [`src/scheduler.ts:125-L141`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L125-L141)）。
- `[SRC-TARGET]` **配置不可达**：插件 `Config` 里没有 `repairLoop`（[`src/index.ts:54-L76`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/index.ts#L54-L76)、schema [:80-L90](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/index.ts#L80-L90)），`resolved` 也没带（[:115-L124](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/index.ts#L115-L124)）；只有内部 `ToolsConfig` 有这个字段（[`src/tools.ts:105-L107`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/tools.ts#L105-L107)）并往 scheduler 传（[:501-L505](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/tools.ts#L501-L505)）。→ **用户既不能调 `maxRounds` 也不能关 `autoDerive`；README 的「`autoDerive` 可关」只在内部/测试可达。**

### 6. 软收敛：阈值与分类

- `[SRC-TARGET]` 三个阈值（[`src/scheduler.ts:140-L144`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L140-L144)）：`STALL_ORPHAN_MS = 5 * 60_000`、`STALL_PARKED_NOTIFY_MS = 30 * 60_000`、`STALL_RUNNING_NOTIFY_MS = 60 * 60_000`。
- `[SRC-TARGET]` `classifyStall`（[:154-L172](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L154-L172)）只对 `claimed`/`in_progress` 生效；`lastActivity = max(updatedAt, attemptStartedAt)`；**owner 状态 undefined（本进程 registry 里没有这个 agent）且 ≥5 min → orphan**；idle ≥30 min → parked-stall；running ≥60 min → running-stall。
- `[SRC-TARGET]` 处置（`detectStalledMemberWork`，[:453-L508](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L453-L508)）：orphan → `invalidateTaskAttempt` 回池（清 attempt 与 assignee，[`src/state.ts:1212-L1220`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L1212-L1220)），**不通知**；parked/running → 每 `(taskId, attemptId, stall)` 只提醒一次（key 在 [:469](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L469-L469)、去重表在内存 [:445](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L445-L445)、判重 [:480-L481](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L480-L481)），提醒进队长邮箱并尝试 steer（[:492-L500](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L492-L500)）。
- `[SRC-TARGET]` **无硬超时属实**：全仓定时器只有 60 s 的 reconcile（[:524](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L524-L524)）与 state 的轮询 sleep；没有 `AbortSignal.timeout`，也没有任何「超时即 cancel/interrupt/判失败」的路径。→ 「无硬超时」可写；**「软收敛」是册子的词，样本不用**，须标 `[OBS]`。

### 7. 60 s 对账器与「搁浅任务」

- `[SRC-TARGET]` `setInterval(…, 60_000)` + `unref()`（[:510-L525](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L510-L525)）。60 s 是**扫描周期，不是停留阈值**。
- `[SRC-TARGET]` 只扫 `seenWorkspaces`（[:416-L419](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L416-L419)）——本进程任一调度入口碰过的工作区；**冷启动后没被工具调用碰过的工作区不会被扫**。
- `[SRC-TARGET]` 队长名下的未完成任务只要队长**不处于 running**（含 idle）就在下一次对账回池，**没有停留时间**；对账既在 60 s 定时器里跑，也在每次 `kickTeam` 里跑（[`src/scheduler.ts:422-L443`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L422-L443)、[:530](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L530-L530)；`isStrandedCaptainTask` [:176-L183](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L176-L183)）。成员名下的 attempt 才要 5 min + owner agent 已不在 registry。

### 8. 心跳 / TTL

- `[SRC-TARGET]` **没有存活心跳**：调度只看 `agent.status` 与任务时间戳（`classifyStall`、`ownedOpenTask` [:312-L315](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L312-L315)），宿主契约也只有 `idle`/`running`（见 SRC-DSH）。
- `[SRC-TARGET]` 但仓里确实有 TTL：邮箱投递租约 60 s（[`src/state.ts:46`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L46-L46)，用于 [`src/state.ts:1090-L1103`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L1090-L1103)）；跨进程锁 stale 30 s（[:146](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L146-L146)）；客户端脉搏 TTL 30 s + 15 s 清扫（[`src/client/live-activity.ts:34-L36`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/client/live-activity.ts#L34-L36)，只决定面板是订阅值还是轮询值权威）；对账周期 60 s。
- `[SRC-TARGET]` 中文 README 把 `teamsx_update_task({progress})` 叫「长任务心跳」（README_ZH:18），落到 `progressLog`（最多 20 条，[`src/state.ts:53`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L53-L53)、[:69-L77](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L69-L77)）——那是进度笔记，不是存活信号。→ 卡片「无心跳」要改成「**无存活心跳**」，并说明这三处 TTL。

### 9. 状态归属与锁

- `[SRC-TARGET]` 状态在 `<workspace>/<stateDir>`，默认 `.teams-x`（[`src/index.ts:55-L57`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/index.ts#L55-L57)、[:82](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/index.ts#L82-L82)；拼接点 [:173](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/index.ts#L173-L173)、[:225](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/index.ts#L225-L225)、[:285](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/index.ts#L285-L285)、[:361](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/index.ts#L361-L361)）。
- `[SRC-TARGET]` 目录内容：`team.json`、`inbox/<agentKey>.jsonl`（[`src/state.ts:1-L21`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L1-L21)）、`operations.jsonl`（[:89-L130](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L89-L130)）、`artifacts/`（[:62-L87](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L62-L87)）、`retired-members.json`（[:42](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L42-L42)）、`index.json`（[:44](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L44-L44)）。**没有 `homedir` 回退**（grep 0）——ACCEPTANCE 里的 `~/.teams-x` 是旧文，卡片写相对 `.teams-x/<teamId>/` 是对的。
- `[SRC-TARGET]` **跨进程文件锁默认开启**（v0.3 起）：`crossProcessLockEnabled()` 返回 `process.env['DSH_TEAMSX_FILE_LOCK'] !== '0'`（[`src/state.ts:153-L156`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L153-L156)）；锁文件在 `$TMPDIR/dsh-teams-x-locks/<sha8>.lock`，`wx` 创建、30 s 判 stale 抢占、10 s 获取超时、50 ms 轮询（[:140-L200](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L140-L200)）；同一批排队变更共享一次持锁（[:219-L262](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L219-L262)）。
- `[SRC-TARGET]` 边界：锁只包 `withTeamLock` 内的读改写（团队状态、退役名单、索引等），**不提供跨进程的归属、派工或接管**；30 s stale 阈值小于一次慢变更时，另一进程可以越过它；锁目录在系统临时目录，与工作区无关。→ 卡片「锁仍是进程内」**是错的**（它源自册子 `01-collab-topology.md:82-83` 与 `ACCEPTANCE.md:306` 的旧描述）。

### 10. 依赖图语义

- `[SRC-TARGET]` 依赖必须存在（[`src/quality.ts:196-L205`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/quality.ts#L196-L205)）；自依赖与**成环**只在 staged 计划校验里拒绝（[`src/tools.ts:332-L360`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/tools.ts#L332-L360)，调用点 [:584](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/tools.ts#L584-L584) 计划批量修改与 [:605](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/tools.ts#L605-L605) approve）。运行期 `create_task` 只查存在性；新任务只能依赖已存在任务，正常路径构造不出环。
- `[SRC-TARGET]` ready 判据：`pending` + 非 `reassigning` + 所有依赖 `completed`（[`src/scheduler.ts:317-L325`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L317-L325)；[`src/state.ts:1230-L1240`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L1230-L1240)）；悬空依赖视为未满足，任务永不 ready。
- `[SRC-TARGET]` 依赖输出：递归祖先、拓扑序、只取 `completed`、每项 2000 字/总 12000 字、从旧端截断（[`src/scheduler.ts:38-L41`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L38-L41)、[:223-L263](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L223-L263)），带运行期环守卫（warn 后断枝，[:229-L234](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L229-L234)）。
- `[SRC-TARGET]` **没有 revision/CAS**（`revision`/`expectedRevision` 在 `src/` 里 0 命中）——与官方团队任务板的 `expectedRevision` 不是同一类东西，卡片也没声称有。

### 11. 信箱、幂等与重试

- `[SRC-TARGET]` `appendMailbox` 是「读全量 + 原子重写整文件」（[`src/state.ts:1016-L1035`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L1016-L1035)）；消息 id = `randomUUID()`（`createMessage`），**没有去重键**。
- `[SRC-TARGET]` 重试 = 租约：`readUnreadMailbox` 过滤 `readAt === undefined && (未 claim || claim 已过 60 s)`（[:1090-L1103](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L1090-L1103)）；claim/release/ack 见 [:1135-L1175](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/state.ts#L1135-L1175)。投递**被 Harness 接受即 ack**（[`src/scheduler.ts:560-L575`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/scheduler.ts#L560-L575)），不等模型 step 消费。
- `[OBS]` 后果：claim 后进程崩溃、或接受后 ack 前崩溃，都会重投 → 接收方可能看到重复。→ 卡片「没有 message-id 幂等，却做了投递重试」成立，可补一句「ack 的是投递接受，不是模型已读」。

### 12. 成员派生与宿主接缝

- `[SRC-TARGET]` `startActivation` 前置：provider 必须支持 `prepareContinuable`/`persona`/`toolFilter`，否则直接抛（[`src/members.ts:660-L673`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/members.ts#L660-L673)）；spec 带 `parent`、persona、`toolFilter: { deny: … }`、`agentOptions`、`maxDepth`（[:676-L692](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/members.ts#L676-L692)），**不传 cwd** —— 成员继承父工作区。
- `[SRC-TARGET]` `drainChildren` 兼容层：先新面 `drainChildren`，再旧面 `drainContinuableChildren`，都没有返回 `'unavailable'`（[`src/compat.ts:110-L130`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/compat.ts#L110-L130)）。
- `[SRC-TARGET]` 退役成员守卫：monkey-patch `ctx.subagents.sendMessage`/`followup`，命中 retired 集合抛 `NOT_RESUMABLE`（[`src/members.ts:738-L770`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/members.ts#L738-L770)）。→ 这两个机制管的是**激活句柄与会话复活**，不是任务归属；卡片把它们算进「owner 不自动释放」的缓解里，分类错了。

### 13. 与 `agent-teams` 的关系证据

- `[SRC-TARGET]` 全仓 `agent-teams` 只有两处：`tsdown.config.ts` 注释点名「dsh-agent-teams' tsdown.config.ts」（[`tsdown.config.ts:4`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/tsdown.config.ts#L4-L4)）；`prepublish-guard.mjs` 在 `lib/*.js` 里匹配 `agent-teams` 并让发布失败，理由写作 "stale reference to the old reference implementation"（[`scripts/prepublish-guard.mjs:33`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/scripts/prepublish-guard.mjs#L33-L33)）。
- `[SRC-TARGET]` 历史里有一条 `feat: drop agent-teams references`（`7b26b51e4a`，2026-09-06）。→ 「同骨架」有源码侧线索；但样本从未声明与官方/`agent-teams` 的关系，卡片「它防的是被误认成别家」是 `[OBS]`。

## SRC-DSH（本机 `@deepseek-ai/dsh@0.2.1-rc.3`）

- `[SRC-DSH]` `startActivation(spec)` 存在于 rc.3：`dsh-subagent/lib/index.js:3036-L3048`（`expectProvider` → 校验 → `startLocal`/`startExternal`）；`drainChildren(parent, childIds)` 在 `:1372` 与 `:3133`；`sendMessage(sender, targetId, content, options)` 在 `:1538`、`:3072`。**rc.3 里 grep 不到 `startContinuable` 与 `drainContinuableChildren`** —— 与 `CHANGELOG.md:29-L33` 的叙述一致。
- `[SRC-DSH]` `AgentStatus = 'idle' | 'running'`（`dsh-agent/lib/types/runtime-types.d.ts:90`），`idle` 表示没有 driver（`:245-L252`），`Agent.status` 镜像每次转换（`:146`）；`ctx.agents.get(id)` 返回裸 `Agent`（`dsh-agent/lib/types/index.d.ts:138`）；registry 是进程内 `Map`（`dsh-agent/lib/index.js:323`）。→ 插件用「registry 里没有该 agent」当 orphan 判据，语义上是「本进程不再持有」，不是「磁盘上的会话消失」。
- `[SRC-DSH]` `dsh-agent`/`dsh-subagent`/`dsh-workspace` 里没有 `worktree` 字样 —— **共享 checkout 是宿主事实**，不只是插件没做隔离。
- `[SRC-DSH]` `assertSubagentMaxDepth` 在 `startActivation` 里生效（`dsh-subagent/lib/index.js:3026-L3030`）；插件默认 `memberMaxDepth = 1`（[`src/index.ts:85`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/src/index.ts#L85-L85)）。

## TEST

- `[TEST]` `scripts/full-functional-test.mjs` 共 1,381 行，**180 处 `check(` 调用点**；README 自述 173 用例（[`README.md:77`](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/README.md#L77-L77)）。两者都不是「通过数」——本轮没跑。
- `[TEST]` 测试 import 的是**构建产物 `lib/`**，不是 `src/`（[:13-L19](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/scripts/full-functional-test.mjs#L13-L19)）；`lib/` 自 `77253f26` 入库，而 0.11.3 自认 `lib/` 是手工镜像（`CHANGELOG.md:45-L46`）。→ 测试证明的是「入库产物」，与 `src/` 是否一致要另核（本轮只在关键机制上核过：`FILE_LOCK`/`STALL_*`/`startActivation`/`reconcileSeenRoots`/`BEAT_TTL` 在 `lib/` 均有命中）。
- `[TEST]` 与卡片机制直接相关的覆盖：
  - M 组：自动派生 repair、依赖指向失败任务、round=1、主题/findings 摘要、round 到 3 不再派生、`autoDerive=false` 不派生（[:899-L975](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/scripts/full-functional-test.mjs#L899-L975)）；
  - Q 组：同源 open repair 去重、源任务 pass 后级联取消、`operations.jsonl` 记录（[:1080-L1136](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/scripts/full-functional-test.mjs#L1080-L1136)）；
  - R 组：`isStrandedCaptainTask`、`openRepairSiblingFor`、`cancelSupersededRepairSiblings`、锁默认开/=0 关（[:1139-L1170](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/scripts/full-functional-test.mjs#L1139-L1170)）；
  - U 组：`classifyStall` 的 5/30/60 分钟边界与终结态（[:1272-L1285](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/scripts/full-functional-test.mjs#L1272-L1285)）。
- `[TEST]` 缺口：① 60 s 定时器真正触发一次无用例（只测了纯函数）；② 两进程争同一把文件锁无用例（R 组只测开关默认值）；③ 插件 `Config` 是否暴露 `repairLoop` 无用例——M 组直接构造内部 config，所以「可关」在测试里成立、在用户侧不成立；④ npm 0.2.0 在 rc.3 上能否派生成员无用例；⑤ 冷启动后 `seenWorkspaces` 为空导致不扫的无用例。

## CI

- `[CI]` 唯一 workflow `.github/workflows/verify.yml`：checkout 上游 `deepseek-ai/deepseek-harness@master` 到同级目录、构建 host libs（[:19-L39](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/.github/workflows/verify.yml#L19-L39)）；`tsc` 容错（[:47-L52](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/.github/workflows/verify.yml#L47-L52)）；Runtime 面跑 `verify:version` + smoke + flow + 功能套件 + icons（[:58-L64](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/.github/workflows/verify.yml#L58-L64)），最后一步 informational typecheck（[:66-L68](https://github.com/Mlte0907/dsh-teams-x/blob/9c56100810bdfbabb03477c882ad1612b8138668/.github/workflows/verify.yml#L66-L68)）。
- `[CI]` **pinned commit 的 CI 是红的**：`9c56100` 只有 1 条 check-run，`verify = failure`（2026-10-21T00:36:07Z–00:39:46Z，run [39522292743](https://github.com/Mlte0907/dsh-teams-x/actions/runs/39522292743)）。失败步是第 10 步 Runtime verification；日志：`TypeError: ctx.subagents.startActivation is not a function`，位置 `lib/members.js:542` ← `tools.js:968`，发生在 A 组建队/派生成员（smoke 与 verify-flow 在它之前已通过）。
- `[CI]` 时间线：`6da32472a7`（2026-10-11）起 master 每条提交都红；最后一次绿是 `c2a132ea72`（`v0.11.2`，2026-09-29）。→ **卡片钉的版本没有绿色 CI，且红点恰好是「成员派生 + 宿主对齐」这条缝**——与卡片「更贴官方包」的叙事相反。

## RUN

- `[RUN]` 本轮做过：npm packument / downloads / tarball / attestations 探测；GitHub API（repo、tags、releases、commits、contents、check-runs、workflow runs、job log）；`codeload` 归档（HEAD `9c56100`、`v0.2.0`）；npm 0.2.0 tarball；`/tmp` 内解包与 `shasum -a 256` 比对；只读本机 rc.3 包；`src/`、`scripts/`、workflow、文档的检索。
- `[RUN] None`：**没有** `npm`/`pnpm install`、构建、跑 `scripts/*.mjs`、跑 `pnpm verify`、启动 DSH、安装/启用插件、写 profile 或 `.teams-x/`；也没有重取官方 `dsh-experimental-agent-team` 的 README 原文。CI 结论来自仓库自己的 run，不是本轮执行。

## 与卡片的偏差表

| 卡片主张 | 源码/宿主/发布物实际 | 处置 |
|---|---|---|
| 精确坐标「版本 0.11.5」 | 0.11.5 只在 master HEAD 的 `package.json` 与 CHANGELOG；无 tag、无 release、npm 最高 0.2.0（2026-09-07） | 坐标改成「commit `9c56100` + 清单 0.11.5（未发布）」 |
| 安装「`npm i dsh-teams-x` …」 | 0.2.0 的 postinstall 指向未打包的 `scripts/postinstall-check.mjs`，tarball 无 `scripts/` → 静态判定安装会失败（未执行安装）；即便绕过，`lib/members.js` 仍调已删除的 `startContinuable` | 标 DOC-only，补「npm 路线当前不可用」；可复现路线是仓库 tgz（0.2.2）或源码构建 |
| 「与 agent-teams 同骨架但更贴官方」 | 同骨架有线索（tsdown 注释、prepublish guard、drop 提交）；「更贴」未被 CI 支持：对上游 master 的 CI 红在 `startActivation`；README 写的宿主基线（0.2.0-rc.1）比 `package.json` 更旧 | 「同骨架」保留并标 `[OBS]`；「更贴官方」删除或降级 |
| 「唯一主动做『官方三条限制逐条对照』的样本」 | 全仓无此表；三条限制出自册子 `01-collab-topology.md:61-68`（引官方 README） | 改成「册子替它做了对照；样本自己不提这三条」 |
| 「两条自认未解决」 | 样本自认的是：真实实例验证交给使用者、`pnpm verify` 未跑、CI runtime 已红、`lib` 手工镜像、ACCEPTANCE §七 四条 | 删「自认」；改为册子的判断 + 列出样本真正的自认 |
| 「锁仍是进程内」 | v0.3 起**默认开启**跨进程文件锁（`state.ts:153-L156`、`:221-L262`），README_ZH:23 明写；`ACCEPTANCE.md:306` 是旧文 | 改成「有跨进程文件锁，但只串行化写入，无跨进程归属」 |
| 「单进程：未解决」 | 结论可留（宿主 registry 进程内、无跨进程归属），但理由必须换成上一条 | 保留结论、换理由 |
| 「owner 不自动释放：部分缓解（`drainChildren` + 退役守卫 + 搁浅回池）」 | `drainChildren` 释放激活句柄、退役守卫拦冷复活，都与任务归属无关；真正缓解归属的是队长搁浅回池（无停留时间）+ 成员孤儿回池（5 min）+ 提醒 | 重列缓解手段 |
| 「60 s 对账回收搁浅任务」 | 60 s 是扫描周期；队长名下任务只要队长不 running 就回池，无停留；只扫本进程碰过的工作区 | 补「周期≠阈值」「只扫见过的工作区」 |
| 「会话消失 5 min 判 orphan 回池」 | 属实，但判据是「本进程 registry 里没有该 agent」且 5 min 无任务更新；回池会清 assignee | 补判据与后果 |
| 「停车 30 min / 运行 60 min 各提醒一次」 | 属实：按 `(task, attemptId, kind)` 去重，表在内存，重启清零；提醒走邮箱 + 尽力 steer | 补「每进程一次」「尽力投递」 |
| 「无心跳」 | 无**存活**心跳；但 README_ZH:18 把进度上报叫「长任务心跳」，另有 60 s 邮箱租约、30 s 锁 stale、30 s 客户端脉搏 TTL | 改成「无存活心跳」并列出 TTL |
| 「软收敛」 | 机制属实（只有提醒/回池，没有超时杀），但「软收敛」是册子的词 | 标 `[OBS]` |
| 「质量门在建任务与完成两处」 | 属实；但 objective/acceptance 对六种 quality kind，`inScope`/`verify` 只对 `implementation`/`repair`；重叠检查只对未终结写类任务 | 补 per-kind 边界 |
| 「review/requirements 必须 verdict=pass 且无 high/blocker」 | 属实（`quality.ts:310-L317`） | 保留 |
| 「commandsRun 有 failed 禁止 completed」 | 属实，且只在「完成」时禁止（判 failed 允许） | 保留并补条件 |
| 「review 打回自动派生 repair（上限 3、同源去重、级联取消）」 | 属实，且 requirements 打回也会派生；上限是默认值，`maxRounds`/`autoDerive` 在插件 Config 里不可达（README「可关」只在内部/测试成立）；派生体不带契约字段、继承 assignee | 保留机制，删「可关」，补可达性 |
| 「verify 是字符串清单，插件不执行命令；changedPaths 由成员自述」 | 属实：`src` 无 `child_process`/`spawn`/`exec`；完成门只比对成员上报值与声明路径 | 保留 |
| 「唯一结构性防自审是提示词一句」 | 结论成立；实际是三处提示词，且 review 任务只要 description 非空 | 补「三处」「非结构性」 |
| 「没有 message-id 幂等，却做了投递重试」 | 属实：id 是 uuid、无去重；重试靠 60 s 租约；ack 的是投递接受，不是模型已读 | 保留并补 ack 语义 |
| 「锁仍是进程内；成员正式路径要同机 harness 源码」 | 锁见上；harness 源码 checkout 是**构建期** `link:` 依赖（README:31、devDependencies），运行期靠 profile 的 peer 包 | 删后半句或改成「构建期需要同机 harness 源码」 |
| `sdd/` 是 `/teamsx` 空态提示的 spec/design/tasks，工艺可搬 | 属实：`teamsx_empty_hint`、EARS + 验收、O-1…O-7、A/B/C/D 裁决表；但基线停在 0.2.0/宿主 0.1.3-alpha.1 | 保留，补「基线过旧」 |
| 「全仓未点名 [agent-teams]，只有 tsdown 一处 + prepublish guard」 | 属实（2 处）；但 guard 的措辞是 "old reference implementation"，且有 `drop agent-teams references` 提交 → 血统线索 | 保留事实，把「防被误认成别家」标 `[OBS]` |
| 「3★ / npm 89 次/月」 | 3★/0 fork；npm last-month 89（2026-09-30–10-29） | 数字保留，注明是 0.2.0 的下载量与窗口 |
| 卡头无「证据链」行（EVIDENCE §2.2） | 卡片只写「证据级别 observed（源码逐文件读过）」 | 卡头补 `证据链：[05-teams-x-源码复核.md](./05-teams-x-源码复核.md)` |

## 未解决与 [OPEN]

- `[OPEN]` 0.11.5 在 rc.3 上能否真正派生成员并跑完：本轮未运行；仓库 CI 是对上游 master 红在 `startActivation`，本机 rc.3 有该函数，两者不能互相替代。
- `[OPEN]` 173（README）vs 180（`check(` 调用点）：未运行，无法判断哪个是「通过数」，也不排除有分支内调用。
- `[OPEN]` 文件锁 30 s stale 抢占：若一次变更持锁超过 30 s，另一进程会抢走锁文件——静态可推，未实测双持窗口。
- `[OPEN]` 仓库自带 `dsh-teams-x-0.2.2.tgz` 是否等于 `v0.2.2` release 产物：未比对字节。
- `[OPEN]` npm 0.2.0 的 56 个 `lib` 文件能否由 tag `v0.2.0` 重建：无 provenance，未重建。
- `[OPEN]` 官方 `dsh-experimental-agent-team` README 的 7 条限制原文：本文只引册子 `01-collab-topology.md:61-68`，本轮未重取上游。
- `[OPEN]` 卡片「9 项能力披露」「过了 D+G 门」属本册计数与门分类，不是目标源码事实，本 memo 不评。
- `[OPEN]` 卡片与 `agent-teams` 的逐项骨架对比（成员启动签名、attempt 代际等）不在本 memo 范围，见 `01-agent-teams-源码复核.md`。
- `[RUN] None`：未安装、未构建、未运行目标插件或其测试；未启动 DSH；未写任何真实 profile / `.teams-x/`。本文结论来自固定 commit 的静态阅读 + rc.3 宿主包阅读 + 只读网络元数据 + 仓库自身 CI 日志。
