---
title: "源码复核：装坏自愈 dsh-plugin-health 1.1.0"
domain: reshape-product
kind: evidence
positioning: "固定 1.1.0 的源码复核：一次性 home 预演、base-only profile、激活判据、豁免写入/回滚、体外 CLI 与运行产物保留。"
read_when: "要核对隔离预演的隔离强度、runs/broken 判据、豁免写入与回滚、boot safe 的真实覆盖面、临时目录清理与并发写入。"
status: observed
updated: 2026-11-01
---
# 源码复核：装坏自愈 dsh-plugin-health 1.1.0

> 取证时点：2026-11-01（Asia/Shanghai）。只读 npm registry、GitHub API/源码归档、本机安装的 DSH `0.2.1-rc.3` 发行包；**未安装、未构建、未运行目标包**，未下载/解包 npm tarball，未执行其测试，未写入任何真实 profile。`[DOC]` = 目标仓库文档主张；`[SRC-TARGET]` = 目标仓库固定提交实现；`[SRC-DSH]` = DSH 上游包实现/契约；`[TEST]` = 测试源码，只证覆盖意图；`[CI]` = workflow 声明与该 commit 的 check-run 元数据；`[RUN]` = 本轮只读 HTTP/磁盘读取事实。
> 目标固定为 tag `v1.1.0` → commit [`db3ad66305b8271667db60b2cc642db6685739b9`](https://github.com/EasonMWS/dsh-plugin-health/commit/db3ad66305b8271667db60b2cc642db6685739b9)（2026-10-31T05:04:17Z，**未签名**）；npm `1.1.0` 的 `gitHead` 却是它的父提交 [`1c4b67d1e8be749f832bda70c938f8d97ea1eb4d`](https://github.com/EasonMWS/dsh-plugin-health/commit/1c4b67d1e8be749f832bda70c938f8d97ea1eb4d)（见下）。DSH 对照 = 本机 `@deepseek-ai/dsh@0.2.1-rc.3`。

## Provenance 与版本界限

- `[RUN]` npm `dsh-plugin-health@1.1.0` 是 `dist-tags.latest`，发布时间 `2026-10-31T04:51:18.427Z`；`gitHead = 1c4b67d1e8be749f832bda70c938f8d97ea1eb4d`，tarball `fileCount 39`、`unpackedSize 862799`，带 `attestations.provenance.predicateType = https://slsa.dev/provenance/v1` 与 `trustedPublisher = github/OIDC`。
- `[RUN]` GitHub tag `v1.1.0` 指向 `db3ad66305b8271667db60b2cc642db6685739b9`（`2026-10-31T05:04:17Z`），是 `1c4b67d` 的**子提交**；`main` 为 `05728e74ec3287db25130dba62141dce02a9e69e`（`05:12:28Z`），又是 `db3ad66` 的子提交。**没有任何 tag/branch 指向 npm 的 `gitHead`**。
- `[SRC-TARGET]` 内容核对（本次把两个 commit 的源码归档解开后 `diff -rq`）：`db3ad66` 与 `1c4b67d` 的差异**只有** `README.md`（+7 行）、`README.zh.md`（+7 行）、`SECURITY.md`（+29/−2 行）；`src/`、`bin/`、`test/`、`scripts/`、`.github/`、`package.json`、`cordis.patch.yml` 全部逐字相同。因此下文的代码/测试/CI 结论对**已发布的 1c4b67d** 同样成立；文档结论只在 tag 上成立。
- `[DOC]` tag 相对 npm `gitHead` 新增的 7 行是 README 的 GHSA 安全段，`SECURITY.md` 新增的是 advisory 表与 “Trust boundaries, stated plainly”。由于 `publish-npm.yml` 在 `1c4b67d` 上于 04:49:43Z 成功执行、npm 于 04:51:18Z 发布，**npm 1.1.0 包内（由 `files` 可见含 README/SECURITY）应当是 tag 之前的文档**：不含 advisory 表、不含回环信任边界段。本轮未下载 tarball 核对字节 → `[OPEN]`。
- `[DOC]` `main` 的 `05728e7` 又把 “external review” 改成 “a security test of 1.0.2”、删掉 “Thanks to the reviewer…”（`SECURITY.md`、`CHANGELOG.md`、`README.md`/`README.zh.md` 各一处），代码未变。引用 tag 的“外部评审/致谢”措辞时要知道它 8 分钟后就被作者自己改写。
- `[RUN]` 版本史：`1.0.3` 的 `gitHead = 9c332674…`（正是 `1c4b67d` 的父提交）；`v1.0.2`、`v1.0.3` **没有 tag**。即该仓库的常态是“先 publish、后打 tag/甚至不打 tag”，`npm version ↔ tag` 不能当作可复现坐标，必须同时记 `gitHead` 与 tag，并比对内容。
- `[RUN]` 提交 `db3ad66` 的 GitHub `verification = {verified:false, reason:"unsigned"}`；tag→commit 的绑定存在，但没有签名校验。本文不把 provenance attestation 说成“已签名验证”。
- `[SRC-TARGET]` `package.json`：`version 1.1.0`、`engines.node >=20`、`engines.dsh >=0.1.0-rc.6 <0.3.0-0`、`peerDependencies` 为 `@deepseek-ai/dsh-app-boot` / `@deepseek-ai/dsh-tools`（均 optional）、`dsh.bundle.patch = ./cordis.patch.yml`、`dsh.client.platform = web`，见 [`package.json:3`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/package.json#L3-L3)、[`:17-L58`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/package.json#L17-L58)。样本卡的版本、范围、安装形态与这里一致。
- `[SRC-TARGET]` README 自述 “Built against the official DSH `0.2.1-rc.2` compatibility rules”（[`README.md:15-L17`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/README.md#L15-L17)），smoke 文档写 “tested with `0.2.1-rc.2` and `0.2.1-rc.3`”（[`:371-L372`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/README.md#L371-L372)）。样本卡基线 rc.3 成立；rc.4 的实测例子本轮无法复核 → `[OPEN]`。

## DOC

- 四层与“第 2 层是存在理由”写在 README 的层表与下一行：[`README.md:30-L37`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/README.md#L30-L37)。第 2 层原文是 “grants the exemption *there*, installs it, boots it, checks every entry activated”（[`:33`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/README.md#L33-L33)）。
- 流程图把顺序写成 “rehearse … ← your profile is untouched”，随后 “confirm, then write one exemption”，并给出反例，见 [`README.md:54-L71`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/README.md#L54-L71)。
- UI 承诺：按钮一次预演 “(30–60 s), changing nothing”；失败时 “no exemption button at all”；豁免“listed with an undo button”；`compatibility.json` 里“single entry”，undo “restores exactly the value that was there before”，见 [`README.md:77-L85`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/README.md#L77-L85)。
- “We never grant an exemption when the rehearsal failed” 在 never-do 表，[`README.md:96-L102`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/README.md#L96-L102)；“临时豁免只证明能启动、不是官方支持” 在 [`:104-L106`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/README.md#L104-L106)。
- 宿主体外路径：三个命令 `boot diagnose/safe/restore`，`safe` “Disable every third-party entry so DSH starts again”，`diagnose` 读 `%APPDATA%\@deepseek-ai\dsh-desktop\logs\crash-*.log`，`safe` 只追加 `disabled: true` overlay、不删文件、不碰宿主条目、不禁自己，两个写命令默认 dry-run，见 [`README.md:136-L160`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/README.md#L136-L160)。
- smoke 的时间和保留语义：安装 120 s、boot/calls/shutdown 合计 30 s；超时停整个进程树；POSIX 上父进程退出零但留下后台子孙也判失败；Windows 无法在父进程退出后探测子孙；**Every run retains its home, smoke.json, runtime.json … There is no automatic cleanup**；临时 home 不是安全沙箱，插件以用户 OS 权限运行，见 [`README.md:359-L376`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/README.md#L359-L376)。
- SECURITY 把 smoke 的作用域写清：opt-in、会执行被测插件与安装、全新但**保留**的 `DSH_HOME`、继承进程环境、不是沙箱、日志保留，见 [`SECURITY.md:40-L43`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/SECURITY.md#L40-L43)；回环信任边界见 [`:45-L52`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/SECURITY.md#L45-L52)。
- 文档自相矛盾：README 的 “A real UI” 段说装成 bundle 就有 Settings → Plugin health（[`README.md:220-L228`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/README.md#L220-L228)），而 “Install inside DSH (bundle mode)” 末尾说 “The bundle declares `engines.dsh`, **adds no UI**”（[`:289-L300`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/README.md#L289-L300)）。`package.json` 的 `dsh.client` 与 `src/plugin.js` 的 `registerRepairRoute`/`registerRescueRoute` 都证明 UI 会注册；后一句是陈旧文案。
- “30–60 s” 是 UI 文案，不是代码上限；实际边界见 §2。

## SRC-TARGET

### 1. 预演的坐标：一次性 home 里到底有什么

- `[SRC-TARGET]` `runRuntimeSmoke` 自己创建运行目录与 home：`parent = out ?? os.tmpdir()`、`directory = mkdtempSync(parent/'dsh-health-smoke-')`、`home = directory/home`、`profile = 'health-smoke'`，并把 `DSH_HOME=home`、`DSH_TELEMETRY_DISABLED=1` 放进子进程环境，见 [`src/runtime/smoke.js:182-L190`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/smoke.js#L182-L190)。`home` 本身是空路径，由宿主 CLI 首次创建。
- `[SRC-TARGET]` **没有任何复制/软链接**：`smoke.js` 只 import `existsSync/mkdirSync/mkdtempSync/readFileSync/statSync/writeFileSync`（[`:3`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/smoke.js#L3-L3)），没有 `cp`/`symlink`/`copyFile`；真实 profile 的 settings、credentials、sessions、cordis.patch.yml 都不会进入这份 home。pnpm 可能把包硬链/软链到它自己的全局 store，但代码没有创建“指向真实 profile”的链接。
- `[SRC-DSH]` 临时的 `health-smoke` profile 由 `dsh plugin` 初始化：`initProfile(dir, PROFILE_TEMPLATES[profile]?.bundles ?? DEFAULT_PROFILE_BUNDLES)`（本机 rc.3 `lib/plugin-BiveYA7h.js:37-L41`）；`DEFAULT_PROFILE_BUNDLES = ['@deepseek-ai/dsh-base']`（`node_modules/@deepseek-ai/dsh-app-boot/lib/index.js:570`）；`web` 模板才是 `['@deepseek-ai/dsh-base','@deepseek-ai/dsh-web-app']`（同文件 `:553`）。因此**预演跑的是 base 单层 + 被测插件，不是用户的 web/desktop bundle 列表**。
- `[SRC-DSH]` base 不提供 `webServer`：`dsh-base/cordis.patch.yml` 的 96 个条目中没有 webServer，`dsh-web-app/cordis.patch.yml:179-L180` 才 insert `id: webserver, name: '@deepseek-ai/dsh-host-webserver'`。对在真实 web profile 里 `inject: ['webServer']` 的插件，base-only 预演会因服务缺失停在 pending，从而被 §3 判成 `broken`；反过来，一个与 web/desktop 其它插件冲突的插件在 base-only 里也看不到冲突。**“在隔离里能启动” 不等于 “在你的 profile 里能启动”。**
- `[SRC-TARGET]` 被测插件来自 `name@version` 的 registry spec（rescue 路由把 UI 的 `plugin`+`version` 拼成 `name@version`，见 [`src/ui/rescue-route.js:154-L167`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/ui/rescue-route.js#L154-L167)），`dsh plugin add` 安装的是 registry 上的那个版本，不是用户 profile 里可能已被本地修改的目录。只有 CLI `smoke --plugin <dir|tgz>` 才是本地包；`rescue` 路径不吃单个 tarball（`resolvePluginIdentity` 对单文件直接抛错，见 [`src/runtime/smoke.js:113-L120`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/smoke.js#L113-L120)）。
- `[SRC-TARGET]` 宿主本身**不会复制进临时 home**：`discoverDshDirectory` 依次找 `<home>/.plugin-health/host`、profile、home、`cwd` 下的 `@deepseek-ai/dsh`（[`src/rescue/environment.js:70-L84`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/rescue/environment.js#L70-L84)）；找不到时 `prepareRehearsalHost` 把 `@deepseek-ai/dsh@<exact>` 用 `npm install --prefix root --ignore-scripts` 装进**真实 home** 的 `.plugin-health/host`（[`:126-L151`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/rescue/environment.js#L126-L151)）。这一步发生在任何 verdict 之前，属于 §4 的“真实 home 被写”。

### 2. 宿主如何真正启动、如何被限时

- `[SRC-TARGET]` 启动前先跑两次官方 CLI：`allow-version <name>@<version> --dsh-version <host.version> --accept-risk`（在临时 home 里先开豁免），再 `plugin --profile health-smoke add <spec>`，两者都用同一个 `DSH_HOME`/cwd，见 [`src/runtime/smoke.js:199-L215`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/smoke.js#L199-L215)。注意 `--accept-risk` 由工具代填——只在这份临时 home 里。
- `[SRC-TARGET]` 真正的“启动”不是 `dsh web`，而是父进程 spawn `node --expose-internals worker.js <config>`（[`:217`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/smoke.js#L217-L217)），worker 通过 `createRequire(hostDir/package.json)` 解析宿主自己的 `@deepseek-ai/dsh/profile-boot` 与 `dsh-app-boot`，调用 `runProfile({ environment: loadLayeredEnv('dsh-health-smoke'), profile: 'health-smoke', patchFiles: [], args: [] })`，见 [`src/runtime/worker.js:66-L71`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/worker.js#L66-L71)。没有浏览器、没有 web server、没有 `cmdlineArgs`；它验证的是 Cordis loader 能否把这份 profile 组合并激活。
- `[SRC-TARGET]` 健康判读在 worker 内分三段：`verifyActivation` 遍历 `loader.entries()`，跳过 `disabled` 与 `state === 2`（ACTIVE）之外的条目一律记为 inactive，并把缺少的 inject 服务列出来（[`src/runtime/worker.js:8-L20`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/worker.js#L8-L20)）；boot-only 时用 `describeActivation` 记录实际 active 的条目（[`:47-L55`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/worker.js#L47-L55)）；再 `ctx.fiber.dispose()`、`shutdown.shutdown(code)`，最后才把 `report.ok = code === 0` 写进 `runtime.json`（[`:84-L99`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/worker.js#L84-L99)）。`runtime.json` 在 boot/assertions/shutdown/complete 各阶段多次落盘，所以超时也能保住最后一个阶段。
- `[SRC-TARGET]` 父进程的“健康”= `runtime.ok && details.ok`：`runtime.ok` 来自 `runBoundedProcess`（exitCode 0 且未 timedOut/未 orphaned），`details.ok` 来自 `runtime.json`；缺报告或读不动都记 error，见 [`src/runtime/smoke.js:216-L227`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/smoke.js#L216-L227)。
- `[SRC-TARGET]` 限时是两层：安装/allow-version 用 `installTimeoutMs`（默认 120000），boot+calls+dispose+shutdown 共用 `timeoutMs`（默认 30000），见 [`src/runtime/smoke.js:150-L160`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/smoke.js#L150-L160)；超时先 SIGTERM 整个进程组，1 s 后 SIGKILL（[`:32-L55`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/smoke.js#L32-L55)）；POSIX 用 `detached` 进程组，Windows 用 `taskkill /T /F`（[`:14-L42`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/smoke.js#L14-L42)）；父进程 close 后还会 `process.kill(-pid, 0)` 探测“父进程已退出但子孙还活着”，POSIX 上判 orphaned 并继续杀（[`:66-L82`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/smoke.js#L66-L82)）；Windows 不做退出后探测（README `:364-L366`）。
- `[SRC-TARGET]` CLI 的默认值不同：`rescue` 是 boot 120 s / install 300 s（[`src/cli.js:424-L425`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/cli.js#L424-L425)），`smoke` 是 30 s / 120 s（[`:308-L309`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/cli.js#L308-L309)）。UI 不传 timeout → 走 smoke 默认 30 s/120 s，所以一次“Check whether it can be saved”最坏约 150 s，而不是 README 的 30–60 s；`apply` 还会再跑一次（见 §5），所以“先 Check 再 apply”整条流程最坏约 300 s。
- `[SRC-TARGET]` 首次没有可发现宿主时，`prepareRehearsalHost` 的 `runNpmInstall` 只给 300 s（[`src/rescue/environment.js:154-L167`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/rescue/environment.js#L154-L167)），且这段时间不计入上面 30 s/120 s；在 desktop（app.asar）或全局安装的常见形态下，第一次预演会先下载一份宿主。
- `[SRC-TARGET]` 一个健壮性缺口：`finish()` 在 `closed === undefined` 时直接返回（[`src/runtime/smoke.js:56-L60`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/smoke.js#L56-L60)），即使 SIGKILL 后的 `forceComplete` 也不能越过它；若子进程/`taskkill` 始终不产生 close（Windows 上 taskkill 失败是现实路径），Promise 可能永远不 resolve，HTTP 请求也就一直挂着。没有观察到，标 `[OBS]` 级风险。

### 3. 健康怎么读：runs / broken / inconclusive

- `[SRC-TARGET]` `rehearse` 的判据只有四条分支：allow-version 阶段失败且整体不 ok → `inconclusive`；install 不 ok → `inconclusive`；`runtime.details.ok === true` → `runs`；否则 `broken`，见 [`src/rescue/rescue.js:103-L118`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/rescue/rescue.js#L103-L118)。
- `[SRC-TARGET]` **`runs` 只看 `runtime.details.ok`，不看 `runtime.ok`**（同文件 `:116`）：后者还包含 timedOut/orphaned/exitCode。于是“worker 写好 ok 之后被父进程按超时杀掉”或“父进程干净退出但留下后台子孙被判 orphaned”这两种情况，smoke 自己的验收是失败（`smoke.js:225`），rescue 却会报 `runs`。这是“读健康”与“读退出”分叉的精确位置。
- `[SRC-TARGET]` `broken` 的覆盖面比 UI 文案大：worker 超时、worker 崩溃/缺 runtime report、宿主缺失 `profile-boot` 导出、spawn 失败、宿主侧异常，都会落到 `broken`；只有 allow-version/install 失败被归为 `inconclusive`。UI 把 `broken` 翻译成 “Even with the exemption this plugin fails to start”（[`src/ui/client.js:379-L379`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/ui/client.js#L379-L379)），会把宿主侧故障误记到插件头上。
- `[SRC-TARGET]` **“every entry activated” 只覆盖“已组合且启用”的条目**：`verifyActivation` 明确 `continue` 掉 `entry.disabled`（[`src/runtime/worker.js:13-L15`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/worker.js#L13-L15)）。DSH 的兼容性 preflight 对不兼容行是 `row.disabled = true` 后继续启动（`dsh-app-boot/lib/index.js:2295-L2345`），被跳过/未组合的 bundle 则根本没有 entry。两种情况下**目标插件自己没加载，激活审计也看不见**；代码没有断言“存在一个 name/id 等于被测插件的 ACTIVE entry”，`describeActivation` 只是把跑过的列出来。
- `[SRC-TARGET]` **宿主版本没有和 `runtimeVersion` 对齐**：smoke 把 `hostVersion: manifest.version` 写进报告（[`src/runtime/smoke.js:191-L195`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/runtime/smoke.js#L191-L195)），而 `discoverDshDirectory` 对已存在的 `.plugin-health/host`（[`src/rescue/environment.js:131`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/rescue/environment.js#L131-L131)）只查 `package.json` 存在、不查版本；`rehearse` 的 `runtimeVersion` 参数甚至没有传给 `runRuntimeSmoke`（后者没有这个参数），预演宿主完全由 `dshDirectory` 决定，`report.hostVersion` 与 `runtimeVersion` 之间没有任何比较。后果：宿主升级后，缓存里上一次下载的旧宿主仍会被启动，豁免却按新的 `runtimeVersion` 写；预演证明的是旧宿主。UI 的确认页显示的是**预演宿主**版本（`rescue.verdict?.hostVersion`，[`src/ui/client.js:661`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/ui/client.js#L661-L661)、[`:769-L770`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/ui/client.js#L769-L770)），但写入的 `runtimeVersion` 是另一个值（§5），两者无相等校验。
- `[OBS]` 结合 §1 的 base-only 组合，这三个缺口叠起来的现实含义是：`runs` 证明的是“被测版本在 base-only 组合、某个（可能是缓存的）宿主上，所有已组合且启用的条目都 ACTIVE”，不证明“在你的 web/desktop profile、当前宿主上，插件会加载”。

### 4. 决策前，真实 profile 与真实 home 的写入边界

- `[SRC-TARGET]` **profile 目录在 rehearse 阶段没有被写**：`rehearse({dshDirectory, plugin, runtimeVersion, …})` 的签名里根本没有 `profileDir`（[`src/rescue/rescue.js:103`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/rescue/rescue.js#L103-L103)）；`runRuntimeSmoke` 只写 `directory/home` 下的内容。路由的 `rehearse` 也只读 `context()` 与宿主发现（`rescue-route.js:103-L167`），不读也不写 profile 配置。
- `[SRC-TARGET]` **真实 home 会被写**：没有可发现宿主时，`prepareRehearsalHost` 在 `<real home>/.plugin-health/host` 做一次 npm install（`environment.js:126-L151`），并在后续运行中复用。README 的 “your profile is untouched”（`README.md:59`）对 **profile 目录**成立，对 **DSH home** 不成立。
- `[SRC-TARGET]` 运行目录默认在 `os.tmpdir()`（`smoke.js:182`），CLI 可用 `--out` 改到任意目录（`cli.js:195`）；UI 不传 `--out`。所以 UI 路径的运行目录不在 profile 内。
- `[SRC-TARGET]` 子进程环境是 `{...process.env, DSH_HOME: home, DSH_TELEMETRY_DISABLED: '1'}`（`smoke.js:190`）：**真实进程环境（代理、API key、PATH、npm token 配置等）被继承**；`loadLayeredEnv` 只从运行目录和临时 home 读 `.env`，不读真实 home 的 `.env`（本机 rc.3 `dsh-app-boot/lib/index.js:3736-L3760`）。插件在安装/启动时仍以用户 OS 权限执行，能读到这些环境变量和用户文件。
- `[SRC-TARGET]` 写入前没有再次确认真实 profile 仍然是那个 `name@version`：`rescuePlugin` 用请求开始时的 `resolvePluginIdentity`（`rescue.js:182`）贯穿预演与写入；若用户在扫描后升级/卸载了插件，仍会为旧版本写豁免。

### 5. 写一条可撤销豁免：文件、字段、顺序、回滚

- `[SRC-TARGET]` 文件与字段：profile 目录下的 `compatibility.json`（`EXEMPTION_FILE`，`rescue.js:28`），顶层对象；键是精确的 `"<name>@<version>"`；值是该键允许的 DSH 版本字符串数组。`grantExemption` 读现有 map、`next = [...new Set([...previous, runtimeVersion])]`、整文件 `writeFileSync`，并返回 `{key, previous}` 供回滚，见 [`src/rescue/rescue.js:126-L139`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/rescue/rescue.js#L126-L139)。
- `[SRC-TARGET]` 第二份状态：`plugin-health-rescue.json`（`RESCUE_STATE_FILE`，`:31`），`{version:1, entries:[…]}`；每条含 `key/name/version/runtimeVersion/profile/appliedAt/previous/granted/rehearsal{verdict,runDirectory}`，写前把旧账本复制成 `.bak`，见 [`src/rescue/rescue.js:59-L81`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/rescue/rescue.js#L59-L81) 与 `:194-L202`。所以“一条豁免”在磁盘上是**两个文件**：宿主文件 + 本工具账本（外加账本 `.bak`）。
- `[SRC-TARGET]` **写入顺序成立**：`rescuePlugin` 先 `rehearse`，只有 `verdict === 'runs'` 才 `grantExemption`，再写账本，见 [`src/rescue/rescue.js:173-L204`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/rescue/rescue.js#L173-L204)；`test/rescue.test.js:104-L117` 断言失败预演后 `compatibility.json` 仍为空。CLI `rescue` 默认 dry-run，`--apply` 才写（`cli.js:416-L417`）。
- `[SRC-TARGET]` **但 apply 路由的写入由“第二次预演”授权**：`POST /rescue/apply` 调 `rescuePlugin`，后者在写之前又跑一次 `rehearse`（`rescue.js:183-L186`），而不是复用用户刚看到的 verdict。用户确认页上的 `hostVersion` 是第一次预演的（`client.js:661`），账本记录的是第二次预演的 `runDirectory`（`rescue.js:198`）。两次都是同一 `name@version`，安全上更强（写前必测），但“用户看到的证据”与“授权写入的证据”不是同一次运行；如果两次之间环境变了，账本留下的不是用户批准的那份。
- `[SRC-TARGET]` **写后没有验证**：`grantExemption` 之后没有重新读 `compatibility.json`、没有用新豁免再 `evaluatePluginCompatibility`、也没有在真实 profile 里做一次 dry boot；头注释声称的第 3 步 “re-verify in the real profile state”（`rescue.js:1-L9`）在代码里不存在。UI 只是 `reload()` 重读 status（`client.js:508-L519`）。
- `[SRC-TARGET]` **回滚语义**：`undoRescue` 遍历账本（可按 `key` 过滤），逐条 `revokeExemption`，再写回剩余账本（`rescue.js:211-L223`）。`revokeExemption` 分两种：`previous === null`（本工具创建了这个键）→ 从数组里删掉该 runtimeVersion，删空就 `delete` 整个键；`previous` 是数组（用户/宿主原本已有）→ **把该键的值整体恢复成 `previous`**，见 [`src/rescue/rescue.js:147-L161`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/src/rescue/rescue.js#L147-L161)。所以样本卡“撤销恢复原来的值（不是删掉整条）”只对第二种成立；第一种会删键。
- `[SRC-TARGET]` 回滚的两个边界：① `previous` 是 grant 时的快照，若之后宿主 CLI/用户又给同一个键加了别的版本，undo 会把它们一起覆盖掉；② `previous === []` 时 undo 会把键恢复成空数组而不是删除，留下一个空记录（宿主可接受，但账本语义略脏）。
- `[SRC-TARGET]` **崩溃窗口**：`grantExemption` 先写 `compatibility.json`，再写账本；两步之间崩溃/磁盘满 → 豁免已生效但账本没有记录，`status` 不显示、undo 找不到，用户只能手改文件。反过来 undo 是先逐条改豁免、最后写账本；中途崩溃后重跑 undo 基本幂等（`revokeExemption` 对缺失键返回 `changed:false`，但 `undoRescue` 仍会把它从账本删掉），不会重复破坏。

### 6. 覆盖式写入、校验与并发

- `[SRC-TARGET]` 与 DSH 自己的写入器相比，`grantExemption`/`revokeExemption` 缺四层保护：**没有文件锁**（全仓无 lock 实现，grep 只命中注释与 `.lock` 残留检测）、**没有原子 rename**（直接 `writeFileSync`）、**没有 0600 权限**（宿主用 `mode 384`）、**没有备份 `compatibility.json`**（只有账本里的 `previous` 值）。DSH 侧的 `setProfileVersionExemption` 是 `withFileLock(filename)` + `writeFileAtomic(..., {mode:384})`，并且对不可重写的文件直接抛错，见本机 rc.3 `node_modules/@deepseek-ai/dsh-app-boot/lib/index.js:424-L470`。
- `[SRC-TARGET]` 校验也不对等：DSH 只接受精确 `name@version` 键与精确 semver 值，`runtimeVersion` 必须等于当前 `getDshRuntimeVersion()`（app-boot 版本，`dsh-app-boot/lib/index.js:271-L275`、`:437`）；`grantExemption` 只拒绝空 runtimeVersion（`rescue.js:131-L133`），不校验 name/version 形状，也不校验 `runtimeVersion` 是否等于当前宿主。预演里的 `allow-version` 会用 DSH 的校验拒绝非精确的 `name@version` 和非精确的宿主版本，但它校验的是**预演宿主目录**的版本，不校验它等于调用方传入的 `runtimeVersion`；所以缓存宿主与运行宿主不一致时仍会放行，CLI `rescue --runtime` 也能把另一个版本写进豁免。
- `[SRC-TARGET]` `readExemptions` 对坏文件是“读成空 map”（`rescue.js:39-L52`），`grantExemption` 再把过滤后的 map 整体写回（`:136-L137`）：**DSH 会保留并警告的非法记录，这里会被静默丢掉**。DSH 的 reader 对不可解析文件返回 `{exemptions:{}, warnings, rewritable:false}`（`dsh-app-boot/lib/index.js:365-L423`），此后 `allow-version` 会拒绝写入直到人工修复；本工具没有这个“不可重写”概念。
- `[SRC-TARGET]` **截断风险**：`writeFileSync` 直接覆盖，崩溃/断电可能留下半截 JSON。DSH 读不动时把整个 profile 视为“没有任何豁免”，并在启动时按不兼容禁用相应行（`dsh-app-boot/lib/index.js:365-L423`、`:2295-L2345`）——也就是说，工具的一次坏写可以把**该 profile 里所有既有豁免一起失效**，直到文件被修复。这是“可撤销”叙事里没有覆盖的失败模式。
- `[SRC-TARGET]` **并发丢更新**：两个 `apply`（两个标签页、UI+CLI、或本工具+宿主 CLI）都读同一份 map、各自整文件写回，后写者覆盖前者；账本仍记两条，`status` 里会有一条 `active:false`。宿主自己的锁只能约束宿主写入器，约束不了这个不取锁的写入者。宿主的 `withFileLock`/`writeFileAtomic` 见 `dsh-app-boot/lib/index.js:424-L470`。
- `[SRC-TARGET]` 宿主缓存也没有锁：两个首次预演会同时对 `<home>/.plugin-health/host` 做 `npm install --prefix`（`environment.js:129-L142`），没有临时目录/原子切换；是否互相破坏取决于 npm 自身，代码层没有保护。

### 7. 宿主自己坏了：宿主体外的救生路径

- `[SRC-TARGET]` `boot` 三个动作在 `src/rescue/boot.js`，CLI 入口 `cmdBoot`（`cli.js:611-L681`）：`diagnose` 读 patch、pnpm 日志、崩溃日志；`safe` 追加 `disabled: true` overlay；`restore` 按注释前缀 `dsh-plugin-health-safe-mode` 删除自己加的条目；`safe`/`restore` 默认 dry-run（`cli.js:655`、`:672`）。写 patch 前备份 `.bak-plugin-health`，临时文件 + rename（`boot.js:69-L77`），并拒绝非 YAML 序列（`boot.js:37-L59`）。
- `[SRC-TARGET]` `safe` 的“第三方入口”只来自 **profile 自己的 `cordis.patch.yml`**：`readProfilePatch(profileDir)` → `thirdPartyEntries(entries)`（`boot.js:343-L354`）。若 profile 的 patch 是默认的 `[]`，目标列表为空，函数直接返回 `changed:false`；CLI 打印 “nothing to disable: 0 entry(ies) already disabled” 并以 0 退出（`cli.js:658-L658`）。
- `[SRC-DSH]` 而按 DSH 的 profile 模型，bundle 的条目由**各 bundle 自己的 patch 层**提供，profile 的 `cordis.patch.yml` 是“用户自己的 patch 层”（`dsh-app-boot/lib/index.js:488-L503`），新 profile 的该文件模板就是 `[]`（同文件 `:593-L596`）；`dsh plugin add` 只改 `dsh.profile.bundles`，只有 enable/disable 才会写 profile patch 行（`node_modules/@deepseek-ai/dsh-plugin-manager/lib/index.js:2280-L2312`、`:1032-L1060`）。**因此最常见的“插件都通过 `dsh plugin add` 装成 bundle、patch 还是 `[]`”的 profile 上，`boot safe` 什么也不会禁用，README 的 “Disable every third-party entry so DSH starts again” 不成立。** 这是静态可读的路径结论，本轮未在真实 profile 上复现。
- `[SRC-TARGET]` 同一盲区也打穿 “switch it off” 这个替代选项：`disablePlugin` 在 patch 里找不到匹配行时，anchor 为空，overlay 只有 `{name, disabled:true, comment}`，**没有 `id`**（`boot.js:397-L416`，注释说“falling back to the name keeps the overlay valid”）。DSH 的 patch 语义是：非 insert patch **必须**有 id，否则 `warn("patch: id is required for non-insert patches")` 并跳过（本机 rc.3 `node_modules/@deepseek-ai/cordis-plugin-include/lib/index.js:66-L90`）。于是路由仍返回 `disabled:true`（`rescue-route.js:211-L215`），UI 显示已禁用（`client.js:565-L575`），宿主却会把那条 patch 当无效行忽略，插件继续加载。
- `[SRC-TARGET]` `safe` 的其余承诺成立：只追加 overlay、保留用户条目、排除 `@deepseek-ai/*` 与自身（`isSelf` 匹配 `dsh-plugin-health` 及 `plugin-health` id，见 `boot.js:90-L114`）、`restore` 只删带 marker 的行（`:376-L386`）。测试覆盖了这些（§TEST），但**没有“bundle-only、profile patch 为空”的用例**。
- `[SRC-TARGET]` `diagnose` 的崩溃日志只在 `APPDATA` 存在时读（`boot.js:125-L130`，目录 `%APPDATA%\@deepseek-ai\dsh-desktop\logs`），在 macOS/Linux/WSL（无 APPDATA）返回空，随后退回 pnpm/`dsh.log` 证据（`:201-L248`）。README 只承诺了 Windows 桌面路径（`README.md:152-L154`），但 “优先读宿主崩溃日志” 在非 Windows 上实际不成立。
- `[SRC-TARGET]` 宿主体外工具的**可运行性依赖安装形态**：`bin` 只有全局/`npx` 才在 PATH 上；README 的 “Install inside DSH (bundle mode)” 只把包装进 profile（`README.md:289-L300`），不产生 PATH 命令，而 DSH 起不来时 `dsh plugin` 也不能用。`boot` 命令本身确实不 import UI/host（`cli.js:605-L610` 的注释），但 `cli.js` 的静态 import 图包含 `yaml`（经 `repair/apply.js`）、`semver`（经 `compat/evaluate.js`）与 `./index/build.js`，后者 import `@deepseek-ai/dsh-plugin-market-index`（`src/index/build.js:1-L10`）。所以 “dependency-free” 只意味着“不依赖 DSH 宿主”，不是“零依赖”；全局包损坏/不完整时 boot 也起不来。
- `[SRC-TARGET]` `safe`/`restore` 写完不验证 profile 能否启动，也不验证 overlay 是否命中；`diagnose` 的 “next: boot safe” 在 `thirdParty=0` 时仍会打印（`cli.js:650-L650`），把“没有可用目标”说成“下一步就能救”。

### 8. 清理：成功、失败、崩溃、并发

- `[SRC-TARGET]` **没有清理**：`smoke.js` 只有 `mkdtempSync`，全文件没有 `rmSync`/`rm`；README 也明说 “There is no automatic cleanup”（`README.md:368-L370`）。成功、失败、超时、崩溃都留下 `dsh-health-smoke-*`，里面可能有完整 home、`node_modules`、`smoke.json`、`runtime.json` 与 64 KiB 上限的 stdout/stderr（`smoke.js:9`、`:187-L196`）。
- `[SRC-TARGET]` 每次“Check”留一份；每次“临时放行”再跑一次预演（`rescue.js:183-L186`），又留一份；宿主缓存 `<home>/.plugin-health/host` 永久保留且不按版本清理。没有配额、没有保留期、没有 `--keep`/`--cleanup` 开关。
- `[SRC-TARGET]` **崩溃**：POSIX 上子进程 `detached: true`（`smoke.js:15`），父进程（DSH）被杀时没有 parent-death 信号，worker/安装进程可能继续跑；worker 自身没有超时（超时只在父进程），所以一个卡住的插件在宿主崩溃后可以无限期存活。临时目录也不会被回收。
- `[SRC-TARGET]` **并发**：每个 run 的 `mkdtempSync` 目录唯一，home 互不重叠；但 §6 的豁免/账本没有锁，宿主缓存没有锁，UI 只在单个页面内用 `busy` 禁按钮（`client.js:630`），跨标签页/CLI 没有 single-flight。两个并发 apply 的典型结果是一个键丢失（账本仍两条）。

## SRC-DSH

- `[SRC-DSH]` 豁免文件契约（本机 `@deepseek-ai/dsh@0.2.1-rc.3`，`node_modules/@deepseek-ai/dsh-app-boot/lib/index.js`）：文件名 `compatibility.json`（`:341`）；reader 只接受“精确 `name@version` 键 + 精确 semver 数组”，不可读/不可解析 → `exemptions:{}` + warning + `rewritable:false`（`:365-L423`）；writer `setProfileVersionExemption` 在 `withFileLock(filename)` 内复读、校验 `acceptRisk`、校验 `runtimeVersion === getDshRuntimeVersion()`、`writeFileAtomic(..., {mode:384})`，文件不可重写时直接抛错（`:424-L470`）。`getDshRuntimeVersion()` 取的是 **`@deepseek-ai/dsh-app-boot` 自己的 package.json version**（`:271-L275`），与目标插件 `hostRuntimeVersion()` 读 app-boot 的做法一致（`src/plugin.js:31-L57`）。
- `[SRC-DSH]` `dsh plugin allow-version` 走同一个 writer：先 `resolveProfileDir`，非 desktop 时 `mkdir` 并在缺 `package.json` 时 `initProfile(..., PROFILE_TEMPLATES[profile]?.bundles ?? DEFAULT_PROFILE_BUNDLES)`，再 `setProfileVersionExemption`（`lib/plugin-BiveYA7h.js:30-L50`）。这解释了临时 profile 的组成（base-only）与 `--accept-risk` 的来源。
- `[SRC-DSH]` profile 模型：`cordis.patch.yml` 是“用户自己的 patch 层，在全部 bundle 层之后应用”；bundle 条目由各 bundle 的 `dsh.bundle.patch` 提供（`dsh-app-boot/lib/index.js:488-L503`）；`initProfile` 写 `PROFILE_PATCH_TEMPLATE`，内容为注释 + `[]`（`:593-L596`）；`DEFAULT_PROFILE_BUNDLES=['@deepseek-ai/dsh-base']`（`:570`），web 模板 = base + web-app（`:553`）；web-app 的 patch 才 insert `webserver`（`node_modules/@deepseek-ai/dsh-web-app/cordis.patch.yml:179-L190`）。
- `[SRC-DSH]` patch 语义：`applyEntryPatches` 对非 insert patch 要求 `id`，没有 id 就 warn 并跳过；有 id 但 name 不匹配也跳过（`node_modules/@deepseek-ai/cordis-plugin-include/lib/index.js:40-L95`）。这直接决定 `disablePlugin` 的 name-only 回退无效。
- `[SRC-DSH]` 兼容性 preflight：不兼容行被置 `row.disabled = true` 后继续启动，并写 stderr “disabling profile plugin …”（`dsh-app-boot/lib/index.js:2295-L2345`）。这既是 `verifyActivation` 跳过 disabled 条目的背景，也是“被拒插件在预演里可能根本没加载”的机制来源。
- `[SRC-DSH]` `runProfile` 只做 profile 组合与 loader 启动，不启动 web server/浏览器；`loadLayeredEnv` 读“继承环境 + 调用目录 `.env` + `$DSH_HOME/.env`”（`lib/profile-boot-C14i-8IN.js:255-L330`、`dsh-app-boot/lib/index.js:3736-L3760`）。目标插件用 `args: []`、`patchFiles: []` 调它，所以预演是 loader 级，不是产品级。
- `[OBS]` 以上都是 rc.3 的实现；目标声明的支持范围到 `<0.3.0-0`，但 `fiber.state === 2` 是 Cordis 内部枚举（`worker.js:8-L9` 的注释也承认），宿主改枚举/激活语义时预演会整体失真。未在 rc.4 复核 → `[OPEN]`。

## TEST

- `[TEST]` `test/runtime.test.js:20-L40`：install 与 boot 用同一个隔离 home，`DSH_HOME === report.home` 且 `report.home !== process.env.DSH_HOME`；`smoke.json` 落盘。`[TEST]` `:42-L51`：安装失败不再 boot、不声称 runtime 兼容。`:53-L64`：超时保留最后阶段且 `ok:false`，即使 shutdown 以 0 退出。`:66-L71`：worker 零退出但没有 runtime report 不算成功。`:86-L113`：launcher 在 shutdown 强制 `process.exit(0)` 仍不能完成验收。`:154-L185`：SIGTERM 被忽略时强杀；父进程成功退出但留下后台子孙判 orphaned 并杀进程组。`:224-L237`：boot-only + tarball 不解析 identity（回归）。
- `[TEST]` `test/rescue.test.js:104-L117`：`verdict:'broken'` 时 `compatibility.json` 仍为空——这是“先测后写”的直接断言。`:119-L133`：`runs` 后才写，且 `previous` 记录原值。`:135-L149`：dry-run 预演但不写。`:33-L61`：grant 追加/幂等、revoke 删键或恢复原列表。`:63-L89`：undo 全量/单键。`:331-L350`：无 host version 拒绝写入（防止 `[null]`）。
- `[TEST]` `test/rescue-route.test.js:23-L47`：rehearse 返回 verdict/canApply，失败时 `canApply:false`。`:49-L83`：没有宿主时下载一个，且下载版本 = 运行版本；下载失败抛出。`:90-L105`：apply 恒为非 dry-run。`:107-L133`：undo 转发 key / 全量。
- `[TEST]` `test/boot.test.js:13-L31`：fixture 的 profile patch **直接写了** `@deepseek-ai/dsh-client-ui-settings`、`dsh-session-recall`、`dsh-winbox` 三条 entry；`:58-L69`：safe 只禁用第三方、保留原条目；`:71-L78`：dry-run 不写；`:80-L89`：restore 逐字保留原条目；`:161-L174`：safe 不禁自己；`:183-L215`：单插件 disable/enable。**没有 bundle-only（patch=`[]`）的用例**。
- `[TEST]` `test/coverage.test.js:32-L40` 证明“只列在 `dsh.profile.bundles`、不在 patch 里”是作者承认的 profile 形态；`listInstalledPlugins` 会把它算进扫描。但 `boot safe` 没有对应覆盖，正好落在 §7 的盲区。
- `[TEST]` `test/security.test.js:33-L60`：status 不再把 key 放 body、改 HttpOnly/SameSite=Strict cookie；`:68-L90`：handoff 的 name/version 路径穿越被围住；`:92-L101`：非精确 semver 的宿主版本被拒；`:103-L120`：宿主安装无 shell、`--ignore-scripts`；`:121-L155`：非序列 patch 被拒、写前备份。它们支撑 1.1.0 的安全修复声明，但不覆盖本 memo 的预演/写入缺口。
- `[TEST]` `scripts/runtime-acceptance.js:1-L73` 用 healthy/pending/throwing/hanging 四个 fixture 跑真实宿主：healthy 断言工具执行值，pending/throwing 断言 `stage:'boot'`，hanging 断言 `timedOut`。它**不覆盖** `bypassGate`/`allow-version`/`rehearse`/豁免写入；fixture 的 `engines.dsh` 都覆盖 rc.2/rc.3，所以 GATE 路径根本没被走到。
- 覆盖缺口（按本卡关注点）：没有“bundle-only profile 上 safe 会禁用谁”的测试；没有“目标插件被 preflight 禁用/未组合时 verdict 不能是 runs”的测试；没有“`report.hostVersion !== runtimeVersion` 必须拒绝/降级”的测试；没有并发 apply/宿主 CLI 的丢更新测试；没有临时目录清理/崩溃回收测试；没有 `apply` 第二次预演失败时不写盘的集成测试（单测只测 `rescuePlugin` 的 fake rehearse）。

## CI

- `[CI]` `ci.yml` 三个 job：`test`（ubuntu/windows × node 20/22，`npm ci` + `npm test`）、`pack`（`npm pack --dry-run`）、`runtime`（ubuntu、node 26、pnpm 11.7.0，host 矩阵 `0.2.1-rc.2`/`0.2.1-rc.3`，`npm install --prefix` 官方宿主后跑 `npm run test:runtime`，并 `upload-artifact` 收集 `smoke.json`/`runtime.json`），见 [`.github/workflows/ci.yml:1-L60`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/.github/workflows/ci.yml#L1-L60)。
- `[CI]` `publish-npm.yml` 是 `workflow_dispatch`，`id-token: write`，先 `npm ci` + `npm test`，再 `npm publish --provenance --access public`（[`.github/workflows/publish-npm.yml:1-L33`](https://github.com/EasonMWS/dsh-plugin-health/blob/db3ad66305b8271667db60b2cc642db6685739b9/.github/workflows/publish-npm.yml#L1-L33)）。这与 registry 的 GitHub OIDC trusted publisher + SLSA provenance 元数据一致。
- `[CI]` 该 commit 的 check-run 元数据（GitHub API，2026-11-01 读取）：`1c4b67d` 共 8 条全部 success，含 `publish to npm via trusted publishing`（04:49:43Z）与两套 `runtime acceptance`（04:48:40Z/04:49:01Z）；`db3ad66` 共 14 条（7 个名字 × push/PR 两轮）全部 success，含两套 runtime acceptance（05:05Z 左右）。这是**该 commit 的 CI 结论**，不是本地复跑。
- `[CI]` 缺口：runtime acceptance 只在 ubuntu 跑；`test` 在 Windows 只跑单测，**Windows 的 taskkill/进程树/orphan 路径没有真实宿主验收**（README 明说 Windows 不支持退出后探测子孙）。也没有任何 job 跑 `boot safe/restore`、`rescue --apply`、或对真实 profile 的 rehearsal。
- `[CI]` 时间线可对上发布：`1c4b67d` 的 publish check 04:49:43Z → npm time 04:51:18Z → tag 05:04:17Z → main 05:12:28Z。发布发生在 tag 之前，解释了 §Provenance 的 `gitHead ≠ tag`。
- `[CI]` 测试源码存在 ≠ 通过；上一条的 success 只说明 GitHub 上该 commit 的 job 成功，不代表本机环境（macOS、Windows 桌面、rc.4）能复现。

## RUN

- 本轮只做只读操作：`registry.npmjs.org`（dist-tags/versions/gitHead/time/attestations）、`api.github.com`（repo、tags、commits、compare、check-runs、rate_limit）、`codeload.github.com`（`db3ad66`/`1c4b67d`/`05728e7` 三个源码归档，解开在 `/tmp` 后 `diff -rq`），以及本机安装的 DSH `0.2.1-rc.3` 包内源码。未 `npm install`、未构建、未跑 `npm test`/`test:runtime`、未启动目标插件、未启动任何 DSH profile、未写 `~/.dsh`。
- 因此**未实测**：真实宿主上的 rehearsal、`allow-version` 在临时 home 的效果、`boot safe` 在 bundle-only profile 的 no-op、并发丢更新、缓存宿主导致的版本错配、Windows 的 taskkill/orphan、临时目录的实际体积与清理行为。相关结论均为固定 commit 的静态代码路径 + rc.3 宿主契约推导，已在正文用 `[SRC-TARGET]`/`[SRC-DSH]` 标出。
- 未下载 npm tarball；`npm 1.1.0` 包内 README/SECURITY 的字节内容、`lib/` 与 `src/` 的一致性未核对 → `[OPEN]`。

## 与样本卡的差异清单（供改卡时逐条取舍）

| 卡片主张 | 源码结论 | 处置建议 |
|---|---|---|
| 版本 `1.1.0`，基线 DSH rc.3 | npm/源码都成立；但 npm `gitHead=1c4b67d`，tag `v1.1.0=db3ad66`，两者只差 3 个文档文件 | 卡上同时写 `npm 1.1.0` 与 tag/commit，注明 `gitHead ≠ tag`；不要把 tag 文档当成已发布包文档 |
| 一次性 home 里预演，你的 profile 完全没动 | profile 目录确实没写；但真实 **home** 会写 `.plugin-health/host`（无宿主时 npm install），运行目录在 OS temp 且**永不清理**；环境变量/OS 权限不隔离 | 改成“profile 未动、home 有宿主缓存、临时目录保留”；补一条“不是安全沙箱，继承真实环境” |
| 预演 30–60 秒 | UI 文案；代码是 boot 30 s + install 120 s（CLI rescue 120/300 s），apply 再跑一次；首次可能先下载宿主（300 s） | 改成“单次最坏约 150 s，首次更久；apply 会跑两次” |
| “在你的 profile 上试” | 预演 profile 是 `@deepseek-ai/dsh-base` 单层 + 被测插件，**不是**用户的 web/desktop bundle 列表，没有其它插件、没有 webServer | 明确写“预演是 base-only 的最小组合”，`runs` 不等于在你的 profile 能跑 |
| 检查每个入口都激活 | 只审计“已组合且启用”的 entry；被 preflight 禁用/未组合的目标插件不会被发现；不校验目标插件自己的 entry | 改成“检查所有已组合且启用的入口”，并补“为什么不等于目标插件已加载” |
| 先测试，后写入 | 成立，且 apply 会用**第二次**预演授权写入；但确认页显示的是第一次的 `hostVersion`，账本记的是第二次 | 保留“先测后写”，补“确认页证据与授权证据是两次运行” |
| 写一条官方 `allow-version` 豁免 | 数据格式是官方的（同一 `compatibility.json`、同一键/值形状），但**写入器不是**：无宿主文件锁、无原子 rename、无 0600、无 `rewritable` 校验、无备份 | 改成“写官方格式，但不是官方 writer”；补锁/原子/截断风险 |
| 撤销恢复原来的值，不是删掉整条 | `previous === null` 时**会删掉整个键**；`previous` 为数组时整体恢复，会覆盖之后新增的版本 | 改成“工具创建的键会被删；用户原有列表按快照恢复” |
| `boot safe` 把所有第三方入口禁用 | `safe` 只枚举 profile 自己的 `cordis.patch.yml`；默认 profile 该文件是 `[]`，bundle 条目不在里面 → **什么也不禁用**，CLI 仍以 0 退出 | 改成“只覆盖 patch 层里已有行的入口”；补 bundle-only 的 no-op 风险；或先修发现逻辑 |
| 失败时“关掉它”是一个诚实选项 | `disablePlugin` 在无匹配行时写一条**没有 id** 的 overlay；DSH 对非 insert patch 要求 id，会 warn 后跳过；UI 仍显示已禁用 | 不要把这个选项写成已实现；补“无 id overlay 无效”的边界 |
| 宿主起不来时 CLI 在宿主体外可用 | 代码确实不 import UI/宿主；但只有全局安装才有 PATH 命令，装进 profile 的 bundle 模式没有；`cli.js` 还静态依赖 `yaml`/`market-index` | 写明“需要全局安装/`npx`”；bundle 模式 + DSH 起不来时这条路径不可用 |
| 预演起不来 = 真的不兼容 | `broken` 也覆盖超时、worker 崩溃、缺 `profile-boot`、宿主侧故障；只有 install/allow-version 失败是 `inconclusive` | 把“broken”拆成“插件失败”与“无法判定/宿主故障”，或在文案里限定 |
| 预演结论只证明能启动、不证明功能 | README 已自述；代码也只做 loader 激活 + 可选工具调用 | 保留；补“还不证明你的 profile 组合、真实 UI、当前宿主版本” |
| 没问题时什么都不显示 | 未在本 memo 范围；UI 代码存在，但安装形态/文档有 “adds no UI” 的矛盾 | 改卡前先修 README 的 `adds no UI` 矛盾，避免引用错 |
| 临时目录/并发行为 | 无清理；无锁；`apply` 与宿主 CLI 并发会丢更新；宿主缓存并发安装无锁 | 卡上补“保留证据、无清理、并发无 single-flight”三条边界 |

## 对样本卡 [OPEN] 的直接回答

- “一次性 home 隔离到什么程度”：独立的 `DSH_HOME` + 独立 `health-smoke` profile，**不复制**真实 settings/credentials/sessions/patch；但 profile 组成是 base-only（不是用户的 bundle 列表），环境变量与 OS 权限不隔离，宿主可能来自缓存/下载而非运行中的宿主，目录不清理。
- “`compatibility.json` 一条豁免的键结构”：顶层对象，键 = 精确 `"<name>@<version>"`，值 = 精确 DSH 版本字符串数组；宿主 reader/writer 的校验、锁、原子写与 0600 见 §6/§SRC-DSH。本工具另外写 `plugin-health-rescue.json` 账本（含 `previous` 快照与 `rehearsal.runDirectory`）。
- “top 120 的扫描口径 / 5 → 1”：不在本 memo 范围，未复核。
- “与 dsh-doctor / dsh-plugin-doctor / dsh-plugin-clinic 的关系”：不在本 memo 范围，未复核；本 memo 只回答“它自己的预演与写入是否成立”。
- “4★ / 4,377 npm 的倒挂”：未在本轮重取；不影响本 memo 对机制与失败边界的结论。

## 复核后的 [OPEN]

- [ ] `[OPEN]` 未下载 npm tarball：`1.1.0` 包内 README/SECURITY 是否确实停在 `1c4b67d`（推断是），以及 `lib/` 构建产物与 `src/` 是否一致。
- [ ] `[OPEN]` `boot safe` 在 bundle-only profile 的 no-op、`disablePlugin` 无 id overlay 被跳过，都是 rc.3 代码路径推导；需要在一次性 home 上跑一次真实 `boot safe --apply` + 启动验证（本轮按约束未运行）。
- [ ] `[OPEN]` 缓存宿主（`.plugin-health/host`）与运行宿主的版本错配是否会在真实升级后产生 `runs` 假阳性；需要构造“旧缓存 + 新 runtimeVersion”的隔离实验。
- [ ] `[OPEN]` 两个并发 apply（或 UI + `dsh plugin allow-version`）是否稳定丢键；需要并发写 `compatibility.json` 的实验。
- [ ] `[OPEN]` `verifyActivation` 的 `fiber.state === 2` 与 DSH rc.4/0.3 的枚举是否仍一致；本轮只有 rc.3。
- [ ] `[OPEN]` Windows 的 `taskkill /T /F` 失败/不产生 close 时，`runBoundedProcess` 是否会永久挂起；只有代码路径，没有 Windows 实测。
- [ ] `[OPEN]` 真实用户 profile（web/desktop）里插件的 `webServer` 依赖是否足以让 base-only 预演产生假 `broken`；需要至少一个 UI 插件样本。
- [ ] `[OPEN]` 样本卡的 npm 月下载 4,377 与 ★4 未在本轮重取；不影响本 memo 的机制结论。
