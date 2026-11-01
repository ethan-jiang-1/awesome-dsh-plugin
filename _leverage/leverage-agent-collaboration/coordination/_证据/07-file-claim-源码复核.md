---
title: "07 · Nwflower/dsh-file-claim 源码复核"
domain: agent-coordination
kind: evidence
positioning: "对 dsh-file-claim 0.2.0（commit 42f07e2，无 tag）的固定提交复核：边车 + pre-execute deny 成立，但只拦四工具、无 epoch，pid 判活是宿主进程粒度，跨机即误杀。"
read_when: "核对 07 卡的写路径硬拦截、租约/孤儿语义与 npm↔commit 坐标时读。"
status: observed
updated: 2026-11-01
---

# 07 · `Nwflower/dsh-file-claim` 源码复核

> 复核对象：样本卡 [`07-Nwflower-dsh-file-claim.md`](../samples/07-Nwflower-dsh-file-claim.md)。
> 取证时点 2026-11-01。只读 GitHub REST（`/repos`、`/commits`、`/tags`、`/branches`、`/check-runs`）、`registry.npmjs.org`（metadata + 0.2.0 tarball）、codeload 固定 commit tarball、本机 `@deepseek-ai/dsh 0.2.1-rc.3` 发行包；**未安装、未构建、未执行 `npm test`、未启动宿主或插件**。
> 标签沿用 [`EVIDENCE.md`](../../EVIDENCE.md)：`[DOC]` 目标仓 README/AGENTS 主张，`[SRC-TARGET]` 固定 commit 实现，`[SRC-DSH]` 本机 DSH 发行包，`[TEST]` 测试源码，`[CI]` 同 SHA check-run，`[RUN]` 本轮实跑，`[OBS]` 判断。
> **主 pin**：commit [`42f07e2171d3781edd932732d243646635f4c1a0`](https://github.com/Nwflower/dsh-file-claim/commit/42f07e2171d3781edd932732d243646635f4c1a0)（`main` = `dev` HEAD，2026-09-02T07:27:34Z，`package.json` 0.2.0）；npm `0.2.0` 的 `gitHead` 即此 SHA。**仓库没有任何 tag 或 release**。
> 一句话结论：**「同目录边车 + `tools/pre-execute` deny」是真的；但它是「四个工具名 + 可解析写目标」的协作护栏，不是写路径上的锁。** 「唯一」在现卡里已降为跨样本观察；机制本身仍受限于：只认 `write`/`edit`/`bash`/`pwsh`、shell 解析漏 `&&`/双竖线/多行/紧贴重定向、无 epoch、pid 判活是**宿主进程**粒度（同宿主内所有会话同 pid）、跨机/NFS 必误杀。

## Provenance

| 项 | 值 | 核对方式 |
|---|---|---|
| 仓库 | [`Nwflower/dsh-file-claim`](https://github.com/Nwflower/dsh-file-claim)（repo id `1333745051`，创建 2026-08-14T03:18:14Z，MIT，**7★ / 0 fork / 1 open issue** @2026-11-01；默认分支 `main`，`pushed_at` 2026-09-02T07:38:46Z，共 **29** 个提交） | `/repos`、`/commits` |
| **npm 包** | `dsh-file-claim`，`dist-tags.latest = 0.2.0`；registry 共 9 个版本（0.1.0 … 0.1.7、0.2.0） | `registry.npmjs.org/dsh-file-claim` |
| **npm 0.2.0 发布** | 2026-09-02T07:41:25.423Z（`time.modified` 07:41:25.587Z）；`gitHead = 42f07e2…`；`shasum 345a58e7…`、`integrity sha512-bq+u…`、`fileCount 7`、`unpackedSize 110626` | registry metadata |
| **主 pin（commit）** | `42f07e2…`，提交信息 `feat: 存储改为工作区边车文件模式（*.dshclaim / *.dshpending）`，committer 2026-09-02T07:27:34Z；`verification = {verified:false, reason:"unsigned"}` | `/commits/42f07e2` |
| package.json | `version 0.2.0`、`main ./index.mjs`、`type module`、`engines.node >=18`、`license MIT`、**无 dependencies / peerDependencies**（[package.json:1-56](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/package.json#L1-L56)） | tarball |
| **tag / release** | **不存在**：`/tags` 为空数组、`/releases` 为空数组（2026-11-01 实取）；`main` 与 `dev` 都指向 `42f07e2` | `/tags`、`/releases`、`/branches` |
| **npm 发布物 vs commit 树** | 7 个文件：`LICENSE` 字节相同；其余 6 个（`index.mjs`、`claim.mjs`、`README.md`、`README.zh-CN.md`、`package.json`、`cordis.patch.yml`）**仅行尾 CRLF 不同**——`tr -d '\r'` 后逐文件 diff 无差异；`test/`、`.github/`、`AGENTS.md`、`package-lock.json` 不在发布面（[package.json:13-20](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/package.json#L13-L20)） | codeload tarball vs npm tarball，`diff` + `shasum` |
| **CI** | pin commit 上 1 条 check-run：`test` / `completed` / **`success`**，2026-09-02T07:38:57Z 完成（run `33604608032`），在 npm 发布前约 3 分钟 | `/commits/42f07e2/check-runs` |
| 下载量 | `last-month`（2026-09-30 → 2026-10-29）= **1064**；`last-week`（10-23 → 10-29）= 233 | `api.npmjs.org/downloads/point/…` |
| 卡片版本核对 | 现卡 L45 已写「`0.2.0` @ `main 42f07e2`（仓库无 tag/release）」——与复核一致；HEAD 版只写 `0.2.0`，没有 commit pin | 源码 + registry |

**坐标对齐与错位（本卡最实的坐标问题）**：`npm@0.2.0`（`gitHead`）↔ commit `42f07e2` ↔ `main`/`dev` HEAD **在内容上可对齐**；但 **tag↔commit 无法对齐——仓库从未打 tag**，也没有 GitHub Release。因此「0.2.0」不能作为可复现坐标（无法 `git checkout v0.2.0`），只能 pin 到 `42f07e2`。第二处错位是字节层：npm 发布物是 CRLF 版本，与 commit 树并非逐字节相同（内容等价）。第三处：发布面不含 `test/` 与 `.github/`，所以 npm 包本身无法自证 CI/测试。

## DOC

`[DOC]` 只证明作者声称什么，不证明实现如此。

- **写守卫覆盖与 fail-open**：「`tools/pre-execute` denies `write` / `edit` / `bash` / `pwsh` calls whose target path is actively claimed by **another** session … `read` is **not** intercepted … Quoted literals are **never** treated as write targets … and commands that yield no parseable target pass through (fail-open)」——[README.md:175-186](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L175-L186)。同段列出 shell 解析白名单（pwsh `Set-Content`/`Add-Content`/`Out-File`/`New-Item`/`Copy-Item`/`Move-Item`/`Remove-Item`/`Rename-Item`；bash `tee`/`dd of=`/`cp`/`mv`/`rm`）——[README.md:181-185](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L181-L185)。
- **commit 级守卫（opt-in）**：`guardCommit: true` 时 `git commit -- <path>` / `git commit <path>` 被拦；message 不检查、裸 `git commit` 放行——[README.md:188-190](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L188-L190)。
- **默认值**：`staleMs 7200000`、`guard true`、`guardCommit false`、`heartbeatMs 600000`——[README.md:196-201](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L196-L201)。
- **边车布局**：`README.md.dshclaim`（JSON：`version, path, tag, note, startedAt, lastSeenAt, pid`）、`README.md.dshpending/`（`content` / `base` / `meta.json`）、根 `.dsh-file-claim.audit.jsonl`、根 `.dsh-file-claim.lock`——[README.md:212-221](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L212-L221)。迁移：≤0.1.7 的 `.dsh-file-claim/` 与未发布的 `.dsh/dsh-file-claim/` 在第一次调用时迁移，旧目录保留，`registry.json` 改名 `.migrated` 作幂等标记——[README.md:232-236](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L232-L236)。
- **pending 语义**：「`git merge-file` over `current × base × pending` … Conflicts → the merged output (with conflict markers) lands on disk and the entry is **kept** … Missing base → refused, never a blind merge. Active claim by any session → refused until released.」——[README.md:262-266](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L262-L266)；`release` 自动尝试合并的失败原因（占用/缺 base/冲突/文件缺失）——[README.md:268-272](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L268-L272)。
- **心跳/孤儿**：「heartbeats refresh automatically via agent lifecycle events; a crashed / hard-killed session's claims are **cleared immediately on the next activity** (per-process pid check) and swept by the heartbeat interval; `staleMs` expiry (2h, for records without a pid) …」——[README.md:50-53](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L50-L53)；FAQ 复述——[README.md:288-292](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L288-L292)。
- **拦截边界自述**：「The guard is **advisory / cooperative**, not a mandatory lock: arbitrary shell commands (`echo > file`, `git checkout`, scripts), external editors, and IDE/git operations bypass the tool stack entirely.」——[README.md:274-279](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L274-L279)；FAQ——[README.md:283-286](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L283-L286)。
- **工具/命令/CLI**：8 个模型工具——[README.md:144-157](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L144-L157)；3 个斜杠命令——[README.md:159-170](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L159-L170)；CLI `node claim.mjs status | audit [n] | claim ...`「same semantics, no DSH required」——[README.md:172-173](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L172-L173)。
- **安装**：`dsh plugin add dsh-file-claim`——[README.md:90](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L90-L90)（中文版在同段：[README.zh-CN.md:84](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.zh-CN.md#L84-L84)）；`git` 在 PATH 中仅三路合并用——[README.md:99](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L99-L99)。
- **无源的品类断言**：「a full scan of **505** `dsh-plugin` topic repositories found **zero** …」——[README.md:69-72](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L69-L72)；「Checked against **11** Claude Code / Codex file-lock … tools」——[README.md:76-77](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L76-L77)。两者都没有附清单、版本或可复现脚本，是纯 `[DOC]`。
- **作者设计文档（非 README）**：`AGENTS.md` 声称 `fs/write-intent` / `fs/edit-intent`「是单槽 waterfall 且被 `dsh-fs-observation-policy` 占用——第三方认领守卫**只能走 `tools/pre-execute`**」——[AGENTS.md:70](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/AGENTS.md#L70-L70)。这条**与本机 DSH 0.2.1-rc.3 不符**（见 SRC-DSH §9）：`fs/write-intent` 是 waterfall，且已有至少两个监听者；「没有 fs 钩子」是**设计选择**，不是宿主硬禁令。

## SRC-TARGET

以下行号全部 pin 到 commit `42f07e2`。先给九条最强主张的裁决，再逐条展开。

### 0. 主张裁决（先看这张表）

| # | 卡片主张 | 裁决 | 关键依据 |
|---|---|---|---|
| 1 | 边车 claim 文件贴在被保护文件旁 | **成立**（认领/待合并是边车；审计与锁在仓库根，是全局文件） | [claim.mjs:113-149](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L113-L149) |
| 2 | `tools/pre-execute` deny 只覆盖 `write`/`edit`/`bash`/`pwsh`；shell 不可解析即 fail-open | **成立，但 fail-open 面比卡片写的宽**：漏 `&&` / 双竖线链、多行脚本、紧贴重定向（`>file`）、`mv`/`Move-Item` 的源路径；且守卫是**无锁预检（TOCTOU）** | [index.mjs:33](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L33-L33)、[index.mjs:386-501](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L386-L501) |
| 3 | 心跳事件 + 10 分钟兜底定时器 | **成立（有条件）**：`timer` 服务在 apply 时不可用则静默没有兜底；定时器只在有 ≥1 live agent 时才真正 prune | [index.mjs:29-30](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L29-L30)、[index.mjs:550-574](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L550-L574) |
| 4 | 三种冲突出口（active / stale / orphan） | **成立**：active → 拒绝；stale → 需 `--force`；orphan（pid 死）→ 自动清后继续 | [claim.mjs:601-646](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L601-L646) |
| 5 | pending 走 `git merge-file` 三路合并 | **成立**：`git merge-file -p cur base other`，0 落盘清条目、1 写冲突标记留条目、>1 失败 | [claim.mjs:938-959](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L938-L959) |
| 6 | 无 fencing / epoch | **成立**：边车字段没有 epoch/generation；被接管方 `sync` 静默刷新不到自己 → 静默失锁 | [claim.mjs:651-659](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L651-L659)、[claim.mjs:556-585](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L556-L585) |
| 7 | pid 判活是「进程粒度」 | **成立，且这是本插件最重要的限制**：`pid = process.pid` 是宿主进程；同一宿主内的多个会话共享同一 pid，会话崩溃 ≠ 进程崩溃 | [claim.mjs:233-248](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L233-L248)、[claim.mjs:658](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L658-L658) |
| 8 | 宿主重启后扫孤儿 | **有条件成立**：没有 startup hook，靠「新宿主 pid ≠ 旧 pid」+ 首次活动（或 10 分钟定时器）触发；容器 PID 1 / pid 复用会失效；无 live agent 时定时器不 prune | [claim.mjs:562-568](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L562-L568)、[index.mjs:566-572](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L566-L572) |
| 9 | NFS / 多机 pid 判活会误杀 | **成立**：边车里没有 hostname / boot id，`process.kill(pid,0)` 只查本机；远端 pid 在本机必然「已死」→ 立刻被当孤儿删掉 | [claim.mjs:233-248](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L233-L248)、[claim.mjs:604-608](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L604-L608) |

### 1. 边车：认领文件确实贴在被保护文件旁

- 路径是**字符串拼接**而非目录：`rel === '.' ? join(repoRoot, '.dshclaim') : join(repoRoot, rel + '.dshclaim')`——[claim.mjs:113-115](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L113-L115)；待合并是目录 `<rel>.dshpending/`——[claim.mjs:117-119](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L117-L119)。`'.'`（整仓库）落到 `<root>/.dshclaim`；目录认领 `src` 落到 `<root>/src.dshclaim`（不是 `src/` 里面）。
- 写入是**原子替换**：先写 `file + '.tmp-' + randomBytes(4)`，再 `rename`——[claim.mjs:143-149](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L143-L149)；读取对损坏 JSON 直接抛「认领边车损坏」——[claim.mjs:122-141](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L122-L141)。
- 覆盖探测 = 精确 + 逐级祖先 + 目录目标的子树扫描——[claim.mjs:202-228](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L202-L228)；枚举跳过 `.git`/`node_modules`/`*.dshpending`——[claim.mjs:65](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L65-L65)、[claim.mjs:187-189](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L187-L189)。删除边车后还会 `rmdir` 空的父目录——[claim.mjs:151-173](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L151-L173)。
- **不是「无中央状态」**：认领和待合并是边车，但审计 `.dsh-file-claim.audit.jsonl` 与跨进程锁 `.dsh-file-claim.lock` 在仓库根，仍是**工作区全局**文件——[claim.mjs:58-59](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L58-L59)；锁是 `open(...,'wx')` + 10s 超时 + 60s 残留回收——[claim.mjs:54-56](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L54-L56)、[claim.mjs:278-305](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L278-L305)。
- 读写全部走 `node:fs/promises`，**不经过宿主 `ctx.fs`**（[index.mjs:23-27](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L23-L27)、[claim.mjs:43-49](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L43-L49)）；因此边车写入不触发宿主的 `fs/write-intent` / 观察策略，也不被 workspace-changes 记录（见 SRC-DSH §9）。
- 迁移：`legacyRegistryDirs` 只认仍含 `registry.json` 的旧目录——[claim.mjs:338-340](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L338-L340)；`migrateLegacyDir` 持根锁、写边车、迁移 pending/audit、最后把 `registry.json` 改名 `.migrated`——[claim.mjs:344-371](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L344-L371)。

### 2. 写守卫：`tools/pre-execute` 的 deny 与它拦不住的东西

**注册与裁决形状**：

- 监听器注册为 `ctx.on('tools/pre-execute', async (exec, next) => …)`，命中时 `return { kind: 'deny', reason }`，否则 `return next()`——[index.mjs:577-585](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L577-L585)。守卫自身异常被 `catch` 吞掉并放行（fail-open）——[index.mjs:581-583](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L581-L583)。
- 覆盖面是**名字白名单**：`const WRITE_TOOLS = new Set(['write', 'edit', 'bash', 'pwsh'])`——[index.mjs:33](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L33-L33)；`name` 不在集合 / `guard === false` / 无 `agent.id` 一律放行——[index.mjs:477-483](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L477-L483)。
- `write`/`edit` 只取 `arguments.file_path`；`bash`/`pwsh` 只取 `arguments.command`——[index.mjs:465-474](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L465-L474)。
- 目标解析：`normPath` 以 `repoRoot`（会话 cwd 解析出的工作区根）为基准，绝对路径可用，越界返回 null 被跳过——[claim.mjs:78-86](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L78-L86)、[index.mjs:477-478](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L477-L478)。
- 命中判定用 `guardHits`：**只读、不加锁、不迁移**，遍历边车 + 未迁移旧 registry；只把 `data.tag !== tag && blocksAsActive(...)` 记为持有者——[claim.mjs:474-501](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L474-L501)。拒绝文案带持有者与三条建议——[index.mjs:497-501](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L497-L501)。

**shell 解析（`bash`/`pwsh`）**：

- 白名单：pwsh 8 个写 cmdlet、bash `tee`/`cp`/`mv`/`rm`——[index.mjs:355-365](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L355-L365)；重定向 `>`/`>>`/`1>`/`2>`/`<>`——[index.mjs:366-368](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L366-L368)；位置参数规则（`cp`/`mv` 取最后、`rm` 全取、其余取第一个）——[index.mjs:376-382](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L376-L382)。
- **具体漏法（都能从代码读出，未运行验证）**：
  1. `CMD_BOUNDARY = /^[|;&]$/` 只认单字符 `|`、`;`、`&`；**`&&` / `||` 不是边界**——[index.mjs:368](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L368-L368)。例：`cp a b && echo x` 会把 `cp` 的位置参数读成 `[a,b,&&,echo,x]`，取最后 = `x`，于是**漏掉真实目标 `b`**。
  2. 分词只按空白切（`splitCommandArgs`），**换行不是命令边界**——[index.mjs:274-295](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L274-L295)；多行脚本里的第一条 `cp` 会把后续命令的参数算进自己的位置参数，取最后一项可能取错。
  3. 重定向必须是**独立 token**：`echo hi>file` 的分词结果是 `hi>file`，不匹配 `REDIRECT` → 放行；`2>&1` 同理。
  4. `mv` / `Move-Item` 只检查**目标**（`positionalTargets` 取最后），源路径被移走/删掉不检查；`mv README.md /tmp/x` 若 `/tmp/x` 不在仓库根内则直接放行。
  5. 未覆盖的写路径：`sed -i`、`perl -i`、`truncate`、`touch`、`install`、`ln`、`git checkout/restore/apply`、`python -c`、`node -e`、`xargs`、编辑器/IDE；README 已自认「arbitrary shell … bypass」——[README.md:274-279](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L274-L279)。
  6. `guardCommit` 也只在 opt-in 时启用，且 `-a`/`-am` 这类无值/带值选项用 `j += 2` 跳过，可能跳过真实路径（注释自己写了 fail-open）——[index.mjs:441-463](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L441-L463)、[index.mjs:485-488](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L485-L488)。
- **引号**：`splitCommandArgs` 直接剥引号，引号内 token 与裸 token 同等参与白名单命令的位置参数匹配——[index.mjs:274-295](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L274-L295)。所以 README 的「Quoted literals are never treated as write targets」并不是一个独立判定；真正起作用的是「只认白名单写命令与重定向」。`rm "README.md"` 仍然会被拦（这合理），`grep -n "README.md" log` 不会被拦（因为 `grep` 不在白名单）。

**其它 fail-open / 边界**：

- 无 `file_path` / `command`、无 `cwd`、工作区根不可用（跨系统路径或目录不存在）→ 全部放行——[index.mjs:489-493](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L489-L493)、[index.mjs:66-82](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L66-L82)。
- **损坏边车的非对称**：守卫读边车出错时按「不可读 → 该目标放行」处理——[claim.mjs:480-486](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L480-L486)；但 `claim`/`status`/`sync` 走 `readClaim` 会抛「认领边车损坏」——[claim.mjs:132-139](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L132-L139)、[claim.mjs:192-193](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L192-L193)。结果：一个坏边车让**认领侧失败关闭、写守卫失败开放**。
- **TOCTOU**：`guardHits` 是**无锁只读预检**，检查与真正的 `write` 之间没有原子性——[claim.mjs:471-473](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L471-L473)、[index.mjs:495](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L495-L495)。这是「护栏」而非「锁」的直接后果。
- **相对路径基准可能错位**（`[SRC-TARGET]`+`[SRC-DSH]`）：插件用**不可变的** `agent.session.header.cwd` 推 `repoRoot`——[index.mjs:118-132](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L118-L132)、[index.mjs:490-493](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L490-L493)；但 DSH 的 `write`/`edit` 是相对**当前会话工作目录**解析（`ctx.workingDirectory.ensure`），该目录可变——见 SRC-DSH §7。若会话 cwd 是工作区子目录，或 agent 用 `working_directory` 改过 cwd，守卫会把 `file_path` 映射到错的根上，可能漏拦。
- **未覆盖的写工具**：DSH 0.2.1-rc.3 发行包还带 `str_replace_editor`（`@deepseek-ai/dsh-tool-str-replace-editor/lib/index.js:267`），它同样经 `fs/write-intent`/`fs/edit-intent` 写文件，但**不在** `WRITE_TOOLS` 里；默认组合未启用它（见 SRC-DSH §3），一旦部署启用即整条绕过。`read` 明确不拦——[index.mjs:32-33](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L32-L33)。

### 3. 心跳：生命周期事件 + 10 分钟兜底定时器

- 默认值：`DEFAULT_STALE_MS = 2h`、`DEFAULT_HEARTBEAT_MS = 10min`——[index.mjs:29-30](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L29-L30)；配置合并——[index.mjs:535-541](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L535-L541)。
- 事件挂接：`agent/created` → `sync`；`agent/status` → `sync`；`agent/disposed` → `release --all`——[index.mjs:550-558](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L550-L558)。`sync` 只刷新**自己还持有**的边车（`data.tag === ctx.tag`），并写入 `lastSeenAt: now` 与 `pid: process.pid`——[claim.mjs:556-585](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L556-L585)。没有认领的会话不登记——[claim.mjs:574](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L574-L574)。
- 定时器：`const timer = ctx.get('timer')`，存在才 `ctx.effect(() => timer.interval(async () => { … }, cfg.heartbeatMs))`——[index.mjs:563-574](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L563-L574)。回调内对 `agents.list()` 先逐个 `sync`、再逐个 `prune`——[index.mjs:566-572](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L566-L572)。注释说明了顺序理由（避免 prune 把即将刷新的活跃会话误判为 stale）——[index.mjs:560-562](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L560-L562)。
- **条件**：`timer` 在 apply 时不存在 → 没有兜底心跳，且没有任何警告（静默）；`agents` 服务不存在 → 回调直接 return——[index.mjs:567-568](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L567-L568)。`agents.list()` 为空（宿主刚起、还没会话）时，两个 `for` 都不执行 → **不会 prune**。
- **成本**：`agent/status` 是 idle ⇄ running 的状态翻转事件（DSH 每个 turn 至少两次），每次触发 `sync`：持根锁 + 全工作区递归扫 `*.dshclaim`——[claim.mjs:561](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L561-L561)、[claim.mjs:176-199](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L176-L199)。`autoRun` 的返回值被丢弃（`void autoRun`）——[index.mjs:550-558](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L550-L558)、[index.mjs:506-516](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L506-L516)，所以 sync 的 status 文本不会展示给任何人。
- `DSH_SESSION_STALE_MS` 只在 CLI 路径生效：`staleMsOf(env)` 读环境变量——[claim.mjs:67-70](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L67-L70)、[claim.mjs:1112](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L1112-L1112)；插件路径始终传 `config.staleMs`（默认 2h）——[index.mjs:129](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L129-L129)。

### 4. 三种冲突出口：active / stale / orphan

`cmdClaim` 在 `withLock` 内先扫重叠边车，分三类——[claim.mjs:601-646](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L601-L646)：

1. **orphan**（有合法 pid 且进程已死）：`isOrphan(data)` → `removeClaim` → 记入 `orphanSwept` → `continue`；随后审计 `orphan-sweep`——[claim.mjs:604-619](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L604-L619)。**不需要 `--force`**。
2. **active**（非 orphan 且 `now - lastSeenAt <= staleMs`）：`code 1`，文案「正被活跃会话占用」——[claim.mjs:620-631](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L620-L631)。
3. **stale**（过期但无死 pid，或根本没有 pid）：没有 `--force` → `code 1`「被 stale 会话占用」——[claim.mjs:632-641](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L632-L641)；有 `--force` → 删掉 stale 边车、记 `[接管]`、继续写自己的边车——[claim.mjs:643-646](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L643-L646)、[claim.mjs:648-660](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L648-L660)。

判定函数：`isPidAlive`（`process.kill(pid,0)`，`EPERM` 也算存活）——[claim.mjs:233-241](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L233-L241)；`isOrphan`——[claim.mjs:246-248](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L246-L248)；`isActive` 只看 `lastSeenAt`——[claim.mjs:251-253](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L251-L253)；`blocksAsActive = !isOrphan && isActive`——[claim.mjs:256-258](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L256-L258)。

**不一致点**：旧 registry 兼容路径（`guardHits` 里）只判 `now - lastSeenAt <= staleMs`，**没有 orphan 判定**——[claim.mjs:487-496](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L487-L496)。也就是说迁移前的旧 registry 记录即使 pid 已死，仍会挡写最多 2h。

### 5. pending：`git merge-file` 三路合并

- **写入条件**：目标必须被**其他活跃会话**占用；否则拒绝并提示「直接 claim 后修改」——[claim.mjs:1037-1050](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L1037-L1050)。内容读自文件或 stdin，写到 `<rel>.dshpending/content`；`base` 来自 `git show HEAD:<rel>`，`HEAD` 取 `git rev-parse HEAD`——[claim.mjs:961-972](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L961-L972)、[claim.mjs:1057-1063](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L1057-L1063)。
- **单槽覆盖**：`meta = { pender, claimedBy: active[0], at, baseSha }`，直接覆盖 `content`/`base`/`meta.json`，没有「已有条目」检查——[claim.mjs:1062-1063](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L1062-L1063)。多个持有者时只记第一个（`active[0]`）。
- **apply 前置条件**：无活跃持有者（`blocksAsActive`）、当前文件存在、`base` 文件存在，否则返回 `occupied` / `no-file` / `no-base`——[claim.mjs:886-908](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L886-L908)。缺 base **拒绝盲合**。
- **合并**：把 current/base/pending 落临时目录，调 `spawnSync('git', ['merge-file', '-p', cur, base, other])`——[claim.mjs:938-959](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L938-L959)。`status === 0` → 写回真实文件并 `rmSync` 条目——[claim.mjs:921-925](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L921-L925)；`status === 1` → **带冲突标记的合并结果写回真实工作树**、条目保留——[claim.mjs:927-930](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L927-L930)；`>1` → `merge-failed`，条目保留——[claim.mjs:931](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L931-L931)。
- **release 自动尝试**：`pendingUnlockCheck` 对「指向被释放路径」或「`claimedBy` 是释放者」的条目逐条 `mergePendingEntry`；成功清条目，失败按原因提示 `pending_apply`/`show`/`drop`——[claim.mjs:844-880](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L844-L880)。
- **纹理限制**：current/base/pending 都按 UTF-8 `readFile`/`writeFile`——[claim.mjs:896-920](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L896-L920)；二进制文件会被当文本处理。`spawnSync` 是**同步阻塞**——[claim.mjs:948](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L948-L948)。
- **测试只覆盖注入版**：测试全部用 `mergeFile: async () => …` 注入（[test/claim.test.mjs:256](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/claim.test.mjs#L256-L256)、`:262`、`:272`、`:278`），**`gitMergeFile` 默认实现没有测试**，本轮也未运行（见 TEST / `[OPEN]`）。

### 6. 无 fencing / epoch：被接管方静默失锁

- 边车字段固定为 `{ version, path, tag, note, startedAt, lastSeenAt, pid }`——[claim.mjs:651-659](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L651-L659)；**没有 epoch / generation / fencing token / owner incarnation**。
- 接管是「删掉旧边车 + 写新边车」——[claim.mjs:643-646](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L643-L646)；旧持有者没有任何被通知的通道。
- 旧持有者下次 `sync`：遍历全部边车，只把 `data.tag === ctx.tag` 的放进 `mine`——[claim.mjs:561-567](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L561-L567)；被接管后 `mine = []`，既不报错也不提示——[claim.mjs:574-583](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L574-L583)。`release` 也只会说「本会话没有认领可释放」——[claim.mjs:695-697](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L695-L697)。
- 自动 `sync` 的返回值被 `void` 丢弃——[index.mjs:550-558](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L550-L558)、[index.mjs:506-516](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L506-L516)，所以连 `claim_status` 的输出都不会自动出现。**失锁是静默的**。
- 但「静默失锁」≠「静默覆盖」：旧持有者之后的写会因 `data.tag !== tag` 被 deny（[claim.mjs:481-483](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L481-L483)），所以最坏结果是**被拒绝**，不是丢数据；代价是它不知道自己已被接管，会把拒绝理解为「别人占着」。
- 另一个竞态：锁只在同一工作区的**变更操作**间互斥（`withLock`）——[claim.mjs:311-318](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L311-L318)；跨机（NFS）时 `open(...,'wx')` 的互斥性未验证。

### 7. pid 判活：进程粒度，不是会话粒度

- 写边车时 `pid: process.pid`——[claim.mjs:658](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L658-L658)；`sync` 刷新时也重写 `pid: process.pid`——[claim.mjs:579](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L579-L579)。在 DSH 里，`process.pid` 是**宿主进程**的 pid；`ctx.agents` 是进程内注册表（[SRC-DSH] §4-5），同一宿主里的多个会话共享同一个 pid。
- 直接后果（按部署拓扑分）：
  - **一个 `dsh web` 宿主跑多个会话**（本 GUI 这类单进程 Web 宿主；`ctx.agents` 在进程内）：所有会话的边车 pid 相同。某个**会话**崩溃/被强杀（宿主还活着）→ `isPidAlive` 为真 → **不算 orphan**；它的认领只能等 `staleMs`（2h）被 `prune` 清掉，或等宿主正常 `agent/disposed`（只覆盖正常离开）。README 的「crashed session 立即清除」在这个拓扑下**不成立**。
  - **一会话一进程**（多个 `dsh` CLI 各自跑）：pid 近似会话 id，README 的承诺成立。
  - **CLI 写认领**：`node claim.mjs claim …` 用的是 CLI 进程自己的 pid，CLI 退出即「死」——下一次任何活动（sync/claim/release/prune）都会把它当 orphan 清掉。README 把 CLI `claim` 描述为「same semantics」——[README.md:172-173](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L172-L173)，但实际上 CLI 写的持久认领在插件侧**几乎立刻失效**。
  - **pid 复用**：宿主重启后新宿主拿到旧 pid（容器里常见，PID 1 永远复用）→ 旧边车被判「活着」→ 不能立即扫，最多挡 2h。
- 边车里**没有** hostname / boot id / machine id 字段（字段见 [claim.mjs:651-659](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L651-L659)、README 布局 [README.md:217](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L217-L217)），所以无法区分「同机另一个进程」与「另一台机器」。

### 8. 宿主重启后的孤儿清扫：没有 startup hook，靠 pid 变化 + 首次活动

- 代码里**没有**插件启动时扫一遍的逻辑；清扫只发生在四条路径：`sync` 全量扫（[claim.mjs:561-568](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L561-L568)）、`claim` 对冲突路径就地扫（[claim.mjs:601-608](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L601-L608)）、`release` 全量扫（[claim.mjs:683-690](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L683-L690)）、`prune` 全量扫（[claim.mjs:748-756](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L748-L756)）。
- 宿主重启后：新宿主的新 pid ≠ 旧边车里的 pid → 第一次 `agent/created`（恢复会话时触发 `sync`）或第一次工具/命令调用就会清掉；若一直没有会话，10 分钟定时器也**不会** prune（`agents.list()` 为空时循环不执行）——[index.mjs:566-572](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L566-L572)。
- `agent/disposed` 是「agent 离开注册表」的事件，不是宿主关停钩子（[SRC-DSH] §4）；宿主直接退出时释放不一定执行完。因此「重启后清扫」实际依赖 pid 变化，而不是一个显式的 shutdown/recovery 协议。
- 失败场景见 §7：容器 PID 1、pid 复用、宿主未重启但会话崩溃、无 live agent 的冷工作区。

### 9. NFS / 多机：pid 判活必然误杀

- `isPidAlive` 只看**本机** pid 命名空间——[claim.mjs:233-241](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L233-L241)；边车没有机器标识（§7）。共享盘上，机器 B 的会话写了 pid=B 的边车，机器 A 的任何活动都会 `process.kill(B, 0)` → `ESRCH` → `isOrphan` → `removeClaim`——[claim.mjs:246-248](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L246-L248)、[claim.mjs:604-608](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L604-L608)。随后两边都可以写同一文件。
- 更糟的是**认领侧**：A 的 `claim` 会直接删掉 B 的活跃边车（`orphanSwept`），并审计成「孤儿会话（进程已退出）」——[claim.mjs:604-619](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L604-L619)。B 的 `sync` 只能静默失锁（§6）。
- `open(...,'wx')` 锁在 NFS 上的语义未验证（`[OPEN]`）；即便锁可靠，也只在同一挂载、同一 NFS 语义下有效。

### 10. README-only：哪些话只有文档、没有 pin 内证据

| README/AGENTS 主张 | 性质 |
|---|---|
| 「505 个 `dsh-plugin` 仓库全量扫描，零命中」（[README.md:69-72](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L69-L72)） | `[DOC]`：无扫描脚本、无清单、无日期；本轮未复扫 |
| 「对照 11 个 Claude Code / Codex 文件锁工具」（[README.md:76-77](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L76-L77)） | `[DOC]`：没列出 11 个的名字/版本/结论来源 |
| 「pending 三路合并区在品类内独有」（[README.md:71-72](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L71-L72)） | `[DOC]`+`[OBS]`：无法从单一仓库证明「独有」；机制本身成立 |
| 「Windows-friendly」（[README.md:62-63](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L62-L63)、[README.md:83](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L83-L83)） | `[DOC]`：CI 只跑 `ubuntu-latest`（[ci.yml:10](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/.github/workflows/ci.yml#L10-L10)）；代码有 win32 分支（[index.mjs:79](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L79-L79)）但无 Windows 运行证据 |
| 「crashed/hard-killed session 的认领在下一次活动**立即**清除」（[README.md:50-53](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L50-L53)、[README.md:288-292](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L288-L292)） | `[DOC]`：只在「会话独占一个进程」时成立；同宿主多会话共享 pid（§7） |
| 「stale 边车在心跳间隔被自动清理」（[README.md:311-313](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L311-L313)） | 半 `[DOC]`：定时器只在有 ≥1 live agent 时真正执行 prune（§3） |
| 「quoted literals 绝不视为写目标」（[README.md:184-185](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L184-L185)） | 误导性 `[DOC]`：解析器直接剥引号；真正的规则是「只认白名单写命令 + 重定向」（§2） |
| 「`fs/*-intent` 单槽且被占用，第三方只能走 pre-execute」（[AGENTS.md:70](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/AGENTS.md#L70-L70)） | `[DOC]`，且与本机 DSH 0.2.1-rc.3 不符（SRC-DSH §9） |
| 「zero dependencies / no build step」（[README.md:62-63](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L62-L63)、[README.md:322-324](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L322-L324)） | 成立且可核：`package.json` 无 `dependencies`，纯 ESM 源码（[package.json:5-6](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/package.json#L5-L6)） |
| 「33 个测试（20 + 13）」（[README.md:317-318](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L317-L318)） | 可核：源码里正好 20 + 13 个 `test()`（见 TEST）；未运行，故只证明「存在」不证明「通过」 |

## SRC-DSH

`[SRC-DSH]` = 本机 `@deepseek-ai/dsh 0.2.1-rc.3` 发行包。它证明宿主契约与默认组合，不证明插件在该宿主上的实际运行结果。

| # | 宿主契约 | 事实 | 目标插件的依赖点 |
|---|---|---|---|
| 1 | `tools/pre-execute` 的形状 | waterfall：`(exec, next) => Promise<PreToolDecision>`；`next()` = allow；`deny` 必须带 `reason`；返回 `{kind:'deny',reason}` 后宿主把它变成模型可见的 `Error: <reason>` 结果（`@deepseek-ai/dsh-tools/lib/index.js:3321`、`:3327-3345`；类型 `lib/types/index.d.ts:38-47`、`:437-450`） | [index.mjs:577-585](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L577-L585) 的 `{kind:'deny', reason}` 形状**正确** |
| 2 | 工具名与参数 | 默认组合注册 `write`/`edit`/`read`/`read_image`（`@deepseek-ai/dsh-tool-fs/lib/index.js:251`、`:549`、`:690`、`:986`）、`bash`（`dsh-tool-bash/lib/index.js:493`）、`pwsh`（`dsh-tool-pwsh/lib/index.js:466`）；`write`/`edit` 的参数名确为 `file_path`（`dsh-tool-fs/lib/types/write.d.ts:17`、`edit.d.ts:24`）；`bash`/`pwsh` 为 `command` | [index.mjs:33](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L33-L33)、[index.mjs:465-474](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L465-L474) 与宿主一致 |
| 3 | 另一个写文件的工具 | 发行包还带 `str_replace_editor`（`dsh-tool-str-replace-editor/lib/index.js:267`），它经 `fs/write-intent`/`fs/edit-intent` 写文件；**默认组合未加载它**（`@deepseek-ai/dsh-base/cordis.patch.yml` 无该行），但 profile 可启用 | 不在 `WRITE_TOOLS` 内 → 启用即绕过；见 `[OPEN]` |
| 4 | agent 生命周期事件 | `agent/created` 是 **serial**（创建时 await）；`agent/status`（idle ⇄ running）与 `agent/disposed` 都是 **emit**（不 await）（`@deepseek-ai/dsh-agent/lib/types/runtime-types.d.ts:227-259`）；`agent/disposed` 在 agent 离开注册表时发出（`lib/index.js:549-565`），**不是宿主关停钩子**；监听器返回的 Promise 只记日志、不等待（`:552-561`） | [index.mjs:550-558](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L550-L558) 事件名正确；release/sync 是后台尽力而为 |
| 5 | `agents.list()` | `ctx.agents: AgentRegistry`，`list(): Agent[]` 返回进程内所有 live agent（`dsh-agent/lib/types/index.d.ts:354-360`）；`Agent.id` 即 `SessionId`（`dsh-agent/lib/types/types.d.ts:12-16`） | 定时器遍历 live agents（[index.mjs:567-571](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L567-L571)）；**同一宿主多会话同 pid** 的根据 |
| 6 | `timer` 服务 | `timer.interval(cb, delay)` 返回 disposer，且默认组合加载 `@deepseek-ai/cordis-plugin-timer`（`dsh-base/cordis.patch.yml:24-25`；实现 `cordis-plugin-timer/lib/index.js:48-55`；类型 `lib/types/index.d.ts:19`） | 10 分钟兜底在默认组合下**存在**（[index.mjs:563-574](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L563-L574)） |
| 7 | 相对路径的基准 | `write`/`edit` 用 `ctx.fs.resolve(path, await sessionResolveOptions(...))`，而该 options 的 `cwd` 来自 `ctx.workingDirectory.ensure(agent)`（`dsh-tool-fs/lib/index.js:171-177`、`:606`、`:750`）；`workingDirectory` 是**可变**的会话目录，session header 保留的是**原始** project cwd（`dsh-working-directory/lib/types/index.d.ts:27`、`:64`、`:73`） | 插件用不可变的 `session.header.cwd` 推 `repoRoot`（[index.mjs:118-121](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L118-L121)）——两者在 `cd` 后会分叉（§2 末尾） |
| 8 | `workspaceRegistry` | `resolveByPath(path): Promise<Workspace \| undefined>`，只解析**已存在**的目录，不创建（`dsh-workspace/lib/types/index.d.ts:259-265`） | [index.mjs:66-82](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L66-L82) 的 fallback 与「不存在则返回 null」一致 |
| 9 | `fs/*-intent` 不是单槽 | `fs/write-intent` 是 waterfall（`dsh-fs/lib/types/index.d.ts:28`），已有至少两个监听者：`dsh-fs-observation-policy/lib/index.js:90-91`、`dsh-workspace-changes/lib/index.js:1076-1081`；`fs/edit-intent` 文档写「Single-slot decision」但同样已有两个监听者。`write-intent` 的返回值只有 `createIfAbsent`/`replaceIfVersion` 两个 arm，**没有 deny arm**；`edit-intent` 可抛 `FsError` 阻断（observation-policy 的 `editIntent` 就这么做） | [AGENTS.md:70](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/AGENTS.md#L70-L70) 的「单槽被占用 → 只能走 pre-execute」**不准确**；没有 fs 钩子是设计选择，且 `write` 的意图钩子本来也不表达 deny |
| 10 | 服务就绪 | 插件只 `inject: ['tools']`，其余 `timer`/`agents`/`commands`/`systemPrompt`/`workspaceRegistry` 全是 apply 时 `ctx.get(...)` 的**当下快照**（Cordis `Context.get`：`cordis/lib/types/reflect.d.ts:14`） | [index.mjs:533](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L533-L533)；默认组合里 timer/commands/systemPrompt 都在插件行之前，但组合顺序不是契约；若顺序相反则命令/心跳/提示词静默缺失 |
| 11 | 插件写入不走 `ctx.fs` | 宿主 fs 工具的写入会经过 `fs/write-intent`；插件直接用 `node:fs/promises` 写边车与审计 | 边车/审计对 workspace-changes、观察策略不可见；这也是「无 fs 钩子」的另一面 |

**目标行为 vs 上游契约的分界**：① `deny` 能拦住工具调用，是宿主 `pre-execute` 的语义，不是插件私开的洞；② `deny` 只发生在**工具调用被派发前**——宿主没有给插件一个通用的「写盘前 allow/deny」门（`write-intent` 只有 create/replace 两个 arm，`edit-intent` 只返回版本守卫或抛错），`tools/pre-execute` 是唯一的 allow/deny 决策点，所以「工具面内硬拒绝、工具面外君子协定」是宿主结构决定的；③ 同宿主多会话共享 pid 是宿主进程模型，不是插件 bug——插件只是没有记录 host/boot 身份；④ 路径基准差异（§2）是插件读取了不可变的 header cwd 造成的，宿主本身能给出可变 cwd。

## TEST

`[TEST]` 只证明覆盖意图，**不证明测试通过**（本轮未跑）。源码里正好 20 个 `test()`（claim）+ 13 个（index），与 README:318 一致。

**覆盖到主张的用例**：

- 三种冲突出口：active 拒绝（[test/claim.test.mjs:59-71](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/claim.test.mjs#L59-L71)）、stale/`--force`（[test/claim.test.mjs:103-120](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/claim.test.mjs#L103-L120)）、**死 pid 立即清孤儿**（[test/claim.test.mjs:361-396](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/claim.test.mjs#L361-L396)，动态找一个 `ESRCH` 的 pid，心跳故意未过期以证明靠 pid 而非 stale）。
- 写守卫：`write`/`edit` deny、自己/未认领/`read` 放行、`guard:false` 全放行（[test/index.test.mjs:185-237](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/index.test.mjs#L185-L237)）；`pwsh` 写 cmdlet、bash `rm`/`tee`/重定向 deny，只读/引号/`cp`/`mv` 源路径放行（[test/index.test.mjs:239-275](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/index.test.mjs#L239-L275)）；`guardCommit` 开关与语义（[test/index.test.mjs:277-306](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/index.test.mjs#L277-L306)）。
- 心跳/生命周期：定时器清理 stale（[test/index.test.mjs:308-331](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/index.test.mjs#L308-L331)）、`agent/disposed` 释放全部认领（[test/index.test.mjs:333-350](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/index.test.mjs#L333-L350)）。
- pending：写入/查询/丢弃（[test/claim.test.mjs:181-203](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/claim.test.mjs#L181-L203)）、release 自动合并（[test/claim.test.mjs:221-245](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/claim.test.mjs#L221-L245)）、apply 成功/冲突/失败/占用（注入 `mergeFile`，[test/claim.test.mjs:247-283](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/claim.test.mjs#L247-L283)）、缺 base 拒绝（[test/claim.test.mjs:285-299](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/claim.test.mjs#L285-L299)）。
- 其它：8 个工具形状（[test/index.test.mjs:129-140](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/index.test.mjs#L129-L140)）、3 个命令注册与执行（[test/index.test.mjs:384-439](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/index.test.mjs#L384-L439)）、迁移与旧 registry 只读兼容（[test/index.test.mjs:441-521](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/index.test.mjs#L441-L521)）。

**没覆盖（[OPEN] 的直接来源）**：

- **真实 `git merge-file` 没测**：`gitMergeFile` 只导出、从不被测试调用；所有 apply 测试注入 `ctx.mergeFile`（[claim.mjs:910](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L910-L910)）。
- **`agent/created` / `agent/status` 没测**：没有任何测试触发这两个事件；只有 `agent/disposed` 与定时器测试。
- **同宿主多会话同 pid / 会话崩溃** 没测；测试用的 `agent(id, cwd)` 是纯对象，不模拟 `process.pid` 共享。
- **NFS / 多机 / pid 复用 / 容器 PID 1** 没测；`[TEST]` 里没有任何 host 身份字段。
- **`str_replace_editor` / `sed -i` / `&&` / 多行脚本 / `>file` 紧贴重定向** 没测；现有 `mv` 用例只测「源路径放行」，没有测「源被移走」。
- **路径基准**（`workingDirectory` 变化）没测；测试的 `workspaceRegistry.resolveByPath` 恒返回 `undefined`（[test/index.test.mjs:78](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/test/index.test.mjs#L78-L78)），所以永远走 cwd fallback，永远不触发「workspace 根 ≠ header cwd」。
- **Windows** 没测；CI 只有 ubuntu。

## CI

`[CI]`：同 SHA 才有意义。

- 工作流：`.github/workflows/ci.yml`，`push: main` + `pull_request`，`ubuntu-latest`、Node 22：`npm ci` → `git diff --exit-code -- package-lock.json` → `npm test` → `node .github/scripts/check-readme-sync.mjs` → `npm pack --dry-run`——[ci.yml:1-24](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/.github/workflows/ci.yml#L1-L24)。
- pin commit `42f07e2` 的 check-runs：**1 条**，`test` / `completed` / **`success`**，2026-09-02T07:38:57Z 完成，对应 Actions run `33604608032`（`html_url` 指向 job `100165643736`）。提交 07:27:34Z、push 07:38:46Z、CI 07:38:49Z 开始、07:38:57Z 绿、npm 07:41:25Z 发布。
- 这只说明「该 SHA 上 CI 绿」，**不等于我跑过**，也不覆盖 Windows / 真实 DSH 宿主 / `git merge-file` 默认实现。

## RUN

`[RUN] None`。本轮只做了只读取数与静态阅读：

- GitHub REST：`/repos`、`/commits`、`/commits/42f07e2`、`/commits/42f07e2/check-runs`、`/tags`、`/branches`、`/releases`；
- `registry.npmjs.org/dsh-file-claim` 与 `api.npmjs.org/downloads/point/…`；
- codeload 的 `42f07e2` tarball 与 npm 0.2.0 tarball（解包到临时目录，仅 `tar`/`diff`/`shasum` 只读比对）；
- 本机 DSH 0.2.1-rc.3 发行包的 `.d.ts` 与 `lib/*.js` 静态阅读。

未安装、未构建、未执行 `npm test`、未启动宿主或插件、未调用任何 claim 工具或 `/claim` 命令。

## 与卡片的偏差

> 口径：本轮起草期间卡片工作树被更新（`git diff` 可见；HEAD 版为 2026-10-31、工作树版为 2026-11-01）。下表按**当前工作树**的 65 行卡片核对；HEAD 版（当时行号 L13/L35/L48）的「全生态唯一」与「其余都是 `.js`」已在工作树修正，故不再算偏差，但仍保留在「结论」列里说明证据强度。按指令**未改卡**。

| 卡片位置 / 主张 | 复核结论 | 标签 | 依据 |
|---|---|---|---|
| L5 / L13「在写路径上返回 deny 的样本；『唯一』是跨样本观察，仅覆盖四个工具」 | **成立**（已按四个工具名收窄）；「唯一」本身仍是 `[OBS]`，本 memo 只核 07，不能证明其他 13 个样本都不拦写 | `[SRC-TARGET]`+`[OBS]` | [index.mjs:33](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L33-L33)、§2 |
| L19「证据链：pin `main@42f07e2`（0.2.0）」 | **成立**；`main` 是移动 ref，durable pin 是 SHA `42f07e2`；本 memo 的 Provenance 补了 npm `gitHead` 对齐与「无 tag」 | `[SRC-TARGET]`+API | Provenance |
| L25「`tag` = `exec.agent.id`」 | **成立**：`agentId(exec.agent)` 即工具/守卫/命令的身份；`sync` 也用它——[index.mjs:57-59](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L57-L59)、[index.mjs:146-159](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L146-L159)。注意：同宿主多会话**同 pid 但不同 tag** | `[SRC-TARGET]` | [index.mjs:57-59](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L57-L59) |
| L27「pending 三路合并…每路径只有一个槽，第二次写覆盖」 | **成立**；补充：`pending_write` **必须有**活跃持有者；`base` 只在 HEAD 含该路径时记录；`meta.claimedBy` 只记 `active[0]`；真实 `git merge-file` 未被测试覆盖 | `[SRC-TARGET]` | [claim.mjs:1037-1063](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L1037-L1063)、[claim.mjs:921-931](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L921-L931) |
| L29「至今没有一个样本同时握有两端」 | `[OBS]`：跨样本判断，不在本 memo 证据范围；本 memo 只确认「07 没有成员模型、只有会话/路径」 | `[OBS]` | [index.mjs:45-53](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L45-L53) |
| L35「工作区边车 `<目标>.dshclaim`，无中央注册表；多机/NFS 误杀」 | **半成立**：认领/待合并确实是边车；但审计 `.dsh-file-claim.audit.jsonl` 与锁 `.dsh-file-claim.lock` 是**工作区根全局文件**——卡片 L56 已补这一点；NFS 误杀**成立** | `[SRC-TARGET]` | [claim.mjs:58-59](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L58-L59)、§9 |
| L36「仅 write/edit/bash/pwsh；shell fail-open 面更宽（`&&`/双竖线、多行、重定向、mv 源）；无 fs 钩子；路径基准可能错位」 | **成立**（与代码一致）；本 memo 另补：`str_replace_editor` 是发行包里的**第五个写工具**（默认组合未启用，profile 可加），以及守卫的无锁 TOCTOU | `[SRC-TARGET]`+`[SRC-DSH]` | [index.mjs:368](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L368-L368)、§2、SRC-DSH §3 |
| L37「stale 2h + pid 判活即刻清孤儿；无 epoch；pid 是宿主进程粒度，同宿主多会话崩溃不触发；后续写会被 deny」 | **成立**，且是本 memo 最核心的复核结论；补充两个未写的场景：CLI `claim.mjs claim` 写的认领会被立刻当孤儿；宿主重启若复用 pid（容器 PID 1）则不清 | `[SRC-TARGET]`+`[SRC-DSH]` | [claim.mjs:233-248](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L233-L248)、§7、§8 |
| L45「`0.2.0` @ `main 42f07e2`（仓库无 tag/release，版本号本身不可定位）」 | **成立**：`/tags`、`/releases` 都为空；npm `gitHead` 与 `42f07e2` 一致；发布物与 commit 树仅 CRLF 差异 | `[SRC-TARGET]`+API | Provenance |
| L47「npm 近 30 天 1,064 次」 | 数字**成立**（`last-month` = 1064）；精度：npm API 的窗口是 2026-09-30→10-29，未覆盖到卡片采样日 10-31；`last-week` 233 | API | Provenance |
| L48「安装 `dsh plugin add dsh-file-claim`（README:90）」 | **成立**：README.md:90 与 zh:84 都是这条命令 | `[DOC]` | [README.md:90](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L90-L90) |
| L49「`main: ./index.mjs`；仓库只有 `index.mjs` 与 `claim.mjs`，没有 `.js`」 | **成立**：codeload 树 14 个文件里没有 `.js`；发布面 7 个文件 | `[SRC-TARGET]` | [package.json:6](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/package.json#L6-L6)、codeload 树 |
| L56「认领随仓库走；但审计与跨进程锁在工作区根」 | **成立** | `[SRC-TARGET]` | [claim.mjs:58-59](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L58-L59) |
| L58「pid 判活 + 2h stale，比纯 TTL 快、比纯心跳省；代价是进程活着但会话死了/跨机会误判」 | **成立**；「比纯 TTL 快」只对**进程已死**成立——同宿主内会话崩溃仍要等 2h，不能算「快」；卡片同句已写代价，故不构成新偏差 | `[SRC-TARGET]`+`[SRC-DSH]` | §7 |
| L59「8 个工具 + 3 个命令共用一个 `run(argv)`」 | **成立**：工具与命令都构造 argv 后调用 `run`，没有第二套语义 | `[SRC-TARGET]` | [index.mjs:136-174](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L136-L174)、[index.mjs:297-348](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L297-L348) |
| L64「无 epoch/fencing；`inject` 只有 `['tools']`，没有 fs 钩子；工具面内硬拒绝、工具面外君子协定」 | **成立**；但「只能走 pre-execute」的**理由**（AGENTS.md:70 说 `fs/*-intent` 是单槽且被占用）与本机 DSH 0.2.1-rc.3 不符——见 SRC-DSH §9；没有 fs 钩子是设计选择 | `[SRC-TARGET]`+`[SRC-DSH]` | [index.mjs:533](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/index.mjs#L533-L533)、SRC-DSH §9 |
| 卡片「唯一」所依赖的 README 数字（505 仓扫描 / 11 个同类工具） | `[DOC]` only：卡片本身没引用这两个数字，但 L5/L13 的「唯一」叙述与 README 的这两条同源；两者都无可复现清单 | `[DOC]` | [README.md:69-77](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/README.md#L69-L77)、§10 |

## `[OPEN]`

- **真实 `git merge-file` 未运行**：测试全部注入 `mergeFile`，默认实现（[claim.mjs:938-959](https://github.com/Nwflower/dsh-file-claim/blob/42f07e2171d3781edd932732d243646635f4c1a0/claim.mjs#L938-L959)）在本仓库没有任何执行证据；`git` 缺失/版本差异/二进制文件的行为未验证。
- **`agent/created` / `agent/status` 心跳链路未测**：事件名与宿主契约正确，但「每次状态翻转都 sync」的实际时序、锁争用与性能未验证。
- **宿主关停时 `agent/disposed` 是否触发**：`emitDisposed` 只在 agent 从注册表 detach 时调用（`dsh-agent/lib/index.js:549-565`），没有看到宿主退出时遍历 detach 的代码；因此「关停时自动 release 全部认领」不保证，重启后的清扫实际靠 pid 变化。
- **同宿主多会话的会话崩溃**：没有测试；按代码只能等 `staleMs`（2h）或正常 `agent/disposed`。宿主是否会在 agent loop 崩溃时移除 agent，未验证。
- **`str_replace_editor` 是否在真实 profile 中启用**：默认 base 组合没有它，但 profile 可加；一旦启用，claim 守卫完全不覆盖。
- **路径基准错位**：插件用不可变的 `session.header.cwd`，宿主写工具用可变的 `workingDirectory.ensure`；实际会话是否会在工作区子目录、或使用 `working_directory` 工具改变 cwd，未在真实宿主上验证（见 SRC-DSH §7）。
- **NFS/SMB 语义**：`open(...,'wx')` 锁、`rename` 原子性、属性缓存在 NFS 上的表现未验证；跨机 pid 误杀本身可由代码推出，但「多久发生、是否造成双写」未做运行验证。
- **pid 复用 / 容器 PID 1**：宿主重启后新进程拿到旧 pid 时，孤儿判定失效；容器里 DSH 作为 PID 1 时必然如此。未在容器内验证。
- **0.1.x 迁移路径**：`migrateLegacyDir` 只读代码，未用真实旧工作区验证 `registry.json` → `.migrated`、pending/audit 迁移与幂等性。
- **性能**：每个 `agent/status` 一次全工作区递归扫描 + 根锁；大仓库/多会话下的开销未测量。
- **npm 发布物行尾**：已逐文件核过——`LICENSE` 与 commit 树字节相同，其余 6 个仅 CRLF 不同；未验证 npm 客户端在不同平台解包/校验时的行为。
- **`engines` 只约束 node>=18**，没有 `engines.dsh` / peerDependency；本 memo 的宿主结论只对 `0.2.1-rc.3` 成立，`0.2.0-rc.*` 分支未核。
- **卡片「唯一」与「至今没有一个样本同时握有两端」**：属于跨样本判断，不在本 memo 的证据范围（`[OBS]`）。
