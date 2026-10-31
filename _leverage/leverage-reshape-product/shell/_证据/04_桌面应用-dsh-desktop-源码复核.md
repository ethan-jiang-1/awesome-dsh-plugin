---
title: "源码复核：dataelement/dsh-desktop（DSH Desktop）"
domain: reshape-product
kind: evidence
positioning: "钉住 HEAD 1a6212e 与 v0.13.0，分清壳的进程/恢复/更新面与 CLI 的 profile 保留名契约，并记录版本对不上。"
read_when: "核对 desktop 版坐标、profile 归属、Safe Mode 组成与恢复面，或判断第三方壳能占哪个 profile。"
status: observed
updated: 2026-11-01
---
# dsh-desktop 源码复核

> **固定快照**：只读一手仓库与 npm 元数据，**未安装、未构建、未运行**目标应用或其 Harness 子进程。目标固定到 `main` HEAD [`1a6212edb321509c3ee00e5d857fadfce13a7790`](https://github.com/dataelement/dsh-desktop/commit/1a6212edb321509c3ee00e5d857fadfce13a7790)（2026-10-30T17:39:45+08:00，"fix(permissions): align microphone authorization and macOS signing with upstream (#822)"），最近 tag [`v0.13.0` → `2c197a55`](https://github.com/dataelement/dsh-desktop/commit/2c197a55f389e463d3fab0821ef2cf0daeb52be5)（2026-10-27T22:27:45+08:00，比 HEAD 早 **10** 个提交）。宿主固定为本机安装的 `@deepseek-ai/dsh@0.2.1-rc.3`。
>
> **方法**：`git clone --filter=blob:none --no-checkout` 后按需 `git cat-file -p HEAD:<path>` 读取单文件；树级统计用 `git ls-tree -r`。只读，不写目标仓库。
>
> **标记**：`[DOC]` 目标仓库文档/清单/注释；`[SRC-TARGET]` 目标仓库固定提交源码；`[SRC-DSH]` 本机 `0.2.1-rc.3` 发行包源码；`[TEST]` 测试源码（存在≠通过）；`[CI]` workflow 配置（存在≠通过）；`[RUN]` 本轮只读的 git/目录检查（**不含**安装、构建、运行目标代码）。
>
> **网络中断说明**：GitHub REST 元数据于 2026-11-01T01:28+08:00 读到一次后触发 60 次/时限流；`raw.githubusercontent.com` 随后 0 字节超时；最后 git promisor 拉取报 `curl 28 … Couldn't connect to server`。**未读到的文件在 §8 逐条列出**，不以推测补齐。

**证据分类（本文只按这六类说话）**

| 类 | 本文用到的具体材料 |
|---|---|
| `[DOC]` | `docs/architecture.md`（全文 127 行，逐行核过卡片引用的 :29 / :35 / :42 / :72）、`build/dsh-desktop*.patch.yml` 注释、`package.json` |
| `[SRC-TARGET]` | `src/main/runtime/harness-runtime.ts`、`src/main/index.ts`、`src/main/state/{safe-mode-profile,profile-store,plugin-disable}.ts`、`src/main/{safe-mode,desktop-protocol,process-recovery,close-to-tray}.ts`、`src/main/update/*`、`src/main/runtime/profile-plugin-command.ts`、`build/harness-node-entry.mjs`、`patches/@deepseek-ai+dsh+0.2.1-rc.3.patch` |
| `[SRC-DSH]` | 本机 `@deepseek-ai/dsh@0.2.1-rc.3`：`lib/bin.js`、`lib/plugin-BiveYA7h.js`、`lib/types/{bin,args}.d.ts`、`node_modules/@deepseek-ai/dsh-app-boot/lib/index.js` |
| `[TEST]` | 只到"`test/` 有 287 个文件"这一层；**未读用例、未跑** |
| `[CI]` | 只到"`.github/workflows/` 有 4 个、`release.yml` 在其中"这一层；**未读内容、未看 run** |
| `[RUN]` | 本轮只读的 `git log/show/ls-tree/cat-file`、目录与 npm 元数据检查；**不含**安装、构建、启动 |

## 0. 坐标

| 项 | 值 | 来源 |
|---|---|---|
| 仓库 | `dataelement/dsh-desktop`，MIT，`fork: false`，创建 `2026-08-13T13:45:50Z` | GitHub REST（2026-11-01T01:28+08:00） |
| 描述 / 主页 | "DSHDesktop：DeepSeek Harness Desktop / DeepSeek Harness 桌面版" / `https://dshdesktop.com` | 同上 |
| 影响力 | `stargazers_count=17,001`、`forks=586`、`open_issues=136`、`pushed_at=2026-10-31T15:12:32Z` | 同上（**时点值**，与卡片 2026-10-31 的 16,975 差 26，属正常漂移） |
| `package.json` 版本 | `dsh-desktop` **0.12.1**（`private: true`，`main: ./out/main/index.js`） | `[DOC]` [`package.json`](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/package.json#L1-L8) |
| tag 与 manifest | `v0.13.0` 的树里 `package.json` **仍是 0.12.1**；两个 tag 名与 manifest 版本不一一对应 | `[RUN]` `git show v0.13.0:package.json` |
| 宿主依赖 | `"@deepseek-ai/dsh": "0.2.1-rc.3"`（**精确 pin，无 `^`/`~`**），另有 30+ 个 `@deepseek-ai/*` 同为 `0.2.1-rc.3` | `[DOC]` `package.json` `dependencies` |
| 宿主补丁 | 仓库自带 **36** 个 `patches/*.patch`，其中 `patches/@deepseek-ai+dsh+0.2.1-rc.3.patch` 直接改宿主 CLI | `[RUN]` `git ls-tree -r HEAD patches/ \| wc -l` |
| 测试 / CI 工件 | `test/` **287** 个文件；`.github/workflows/` **4** 个（`release.yml`、`issue-feedback.yml`、`backfill-archive.yml`、`ppt-font-layout.yml`） | `[RUN]` `git ls-tree -r`（**存在不等于通过**） |
| 本地宿主 | `@deepseek-ai/dsh@0.2.1-rc.3`（`lib/bin.js`、`lib/plugin-BiveYA7h.js`） | `[SRC-DSH]` 本机安装目录 |

**三点关系**：目标仓库 pin 的宿主版本 = 本机安装版本（`0.2.1-rc.3`），所以下文 `[SRC-DSH]` 行号对"该仓库依赖的那一版"成立；但仓库同时用 patch-package 改了宿主（§1.2），所以**不能把发行版里的 CLI 等同于 npm 上的 rc.3**。

## 1. 血缘与版本：三处对不上，逐条记下来

### 1.1 tag 名 ≠ manifest 版本

`v0.13.0`（`2c197a55`）与 HEAD（`1a6212e`）的 `package.json` 都写 `"version": "0.12.1"`；`v0.12.1` tag 指向 `a170609b`。也就是说 tag 序列里 `v0.12.1` 与 `v0.13.0` 的 manifest 版本相同。`[RUN]` 只读比对。

**可以怎么说**：仓库的 *tag 名*是发布通道的标签，*manifest 版本*由发布流水线另行注入（`index.ts` 里仍残留 `V0.13.0 维修演示` 的硬编码窗口标题，[index.ts:3953](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L3953)）。**不能**据 tag 反推安装包 `CFBundleShortVersionString` / NSIS 版本——`electron-builder` 的实际注入步骤在 `release.yml` 与 `electron-builder.dev.cjs` 里，本轮**未读到**，故 `[OPEN]`。

### 1.2 发行版里的 CLI 是"rc.3 + 补丁"

`patches/@deepseek-ai+dsh+0.2.1-rc.3.patch` 只做两件事：

1. 把 `runCli` 捕获 `StartupError` 后的 `process.exit(1)` 改成 `process.exitCode = 1; throw error;`（[L7-L16](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/patches/@deepseek-ai+dsh+0.2.1-rc.3.patch#L7-L16)）——因为壳是在**子进程里直接调 `runCli()`**，需要拿到异常而不是被 CLI 抢先退出（见 §2.1）。
2. 往 `@deepseek-ai/dsh/package.json` 的 `dependencies` 里追加 11 个 Desktop 自有包与 `dsh-ppt-composer`、`react-dom`（[L17-L39](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/patches/@deepseek-ai+dsh+0.2.1-rc.3.patch#L17-L39)）——让 profile 解析能在应用的 hoisted 树里找到这些包。

`[SRC-TARGET]` 同目录还有 30 个针对 `dsh-client-ui-*`、`dsh-app-boot`、`dsh-plugin-manager`、`dsh-web-frontend` 等的 rc.3 补丁。**结论**：该产品交付的是**打过补丁的运行时**，"验证于 rc.3" 只能按"验证于 rc.3 + 本仓库 36 个补丁"读；宿主升级时这 36 个补丁就是迁移负债。

### 1.3 它是不是上游说的"the Electron application"

`[SRC-DSH]` 里 `desktop` 这个名字的全部契约只有 7 行，且**没有任何产品名、URL 或包名**：

| 位置 | 原文 |
|---|---|
| `dsh/lib/bin.js:35-37` | `rejectElectronProfile`：`profile "desktop" is managed exclusively by the Electron application` |
| `dsh/lib/bin.js:112` | 启动路径 `rejectElectronProfile(program, profile)` |
| `dsh/lib/bin.js:119` | `plugin` 路径 `if (!manageDesktopProfile) rejectElectronProfile(plugin, options.profile)` |
| `dsh/lib/bin.js:123` | 解析后把 `DESKTOP` 归一成 `desktop` |
| `dsh/lib/plugin-BiveYA7h.js:10-12` | `requireDesktopProfile`：`Open DeepSeek Harness Desktop once … then fully quit it before running dsh plugin --profile desktop.` |
| `dsh/lib/plugin-BiveYA7h.js:38-40` | `if (profile !== "desktop") await mkdir(dir, …)`，随后 `requireDesktopProfile(dir)` |
| `dsh/lib/plugin-BiveYA7h.js:64-65, 90-91` | `runPlugin` 前与写锁内各查一次 profile 是否已存在 |

`[SRC-DSH]` `@deepseek-ai/dsh-app-boot@0.2.1-rc.3` `lib/index.js`：`PROFILE_TEMPLATES` 只有 `acp / web / headless / sdk / sdk-minimal`（`:551-557`），**没有 `desktop`**；`DEFAULT_PROFILE_BUNDLES = ["@deepseek-ai/dsh-base"]`（`:570`）；`resolveProfileDir`（`:546-550`）只校验名字合法性，不校验归属。

**结论（重要）**：上游守的是一个**名字**，而且守的是一个**匿名的** "the Electron application"。本仓库**没有任何一手证据表明它就是那个 carrier**；反过来，它自己的补丁注释与架构文档写的是另一件事。`[DOC]` 两处直接自述用 `web`：

- "Open the startup surface, then start loading the packaged Harness shell at `dsh-desktop://harness/` while **inspecting the web Profile**"（[architecture.md:29](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/docs/architecture.md#L29)）
- "The **normal web profile** may contain community plugins and their transitive packages"（[architecture.md:72](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/docs/architecture.md#L72)）；同文 :42 的目录树把 `harness/` 标为 `DSH_HOME`、`profiles/` 标注为 "Normal and Safe Mode profiles"，:35 写 "Safe Mode starts a **separate profile**"。

因此：

- 卡片把这条缝当作"官方桌面应用占名"的**协议事实**引用，成立；
- 但把这个仓库当作被占名的那一方，**不成立**——它是**绕开**的一方（第三方/社区发行版，owner `dataelement`、author `DataElement`、MIT、独立站点 `dshdesktop.com`，仓库与 `deepseek-ai` 组织无一手关联）。按用户要求的口径：**官方 host 行为（保留名 + 只允许安装态 carrier 程序化通过）** 与 **第三方壳行为（自建 DSH_HOME + `web` profile，入口只调 `runCli({ packageManager })`）** 必须分开写。

## 2. 壳拥有什么、CLI 拥有什么

`[SRC-TARGET]` 的 ownership 边界很清楚：壳写一个自有 `DSH_HOME`，把 `dsh` 当**子进程**拉起，自己只碰"进程、端口、日志、更新、恢复页"，profile 内部的插件树交给 CLI/pnpm。

### 2.1 生命周期：壳 spawn 一个嵌入了 `runCli()` 的 Node 子进程

| 环节 | 事实 | 位置 |
|---|---|---|
| DSH_HOME | `join(app.getPath('userData'), 'harness')`——Electron per-user 数据目录下的 `harness/` | [index.ts:1567](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L1567)、[L1662](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L1662) |
| profile | **`web`**（默认参数），不是 `desktop` | [harness-runtime.ts:256](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L256)、[L316](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L316)、[L394](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L394)、[L493](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L493) |
| 参数 | `web --patch … --no-open --host 127.0.0.1 --port <n>`；`--no-open` 是为了不让 Harness 自己把 URL 交给系统浏览器 | [harness-runtime.ts:253-270](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L253-L270) |
| Node 入口 | `build/harness-node-entry.mjs`（打包后 `process.resourcesPath`）`import()` 宿主 `lib/bin.js` 后调 **`runCli({ packageManager })`**——**不传** `manageDesktopProfile`；CLI 本体是 `node_modules/@deepseek-ai/dsh/lib/bin.js` | [index.ts:659-661](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L659-L661)、[L688-692](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L688-L692)、[harness-node-entry.mjs:105-132](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/build/harness-node-entry.mjs#L105-L132) |
| 就绪判据 | **stdout 上的 launch token**（`dsh web: <url>?token=`）+ 回环 HTTP 探针（`401` 也算健康）；先见到 token 才追加 30s 宽限 | [L242-251](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L242-L251)、[L445-450](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L445-L450)、[L1113-1152](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L1113-L1152) |
| 超时 | 45s（POSIX）/ 180s（Windows） | [L590-591](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L590-L591) |
| 停止 | `SIGTERM` → 等 4s → `SIGKILL` | [L730-741](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L730-L741) |
| 意外退出 | 记为 `failed` 并把 stderr 的归因写进消息；**不自动重启** | [L668-683](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L668-L683) |
| 日志 | 单文件 `harness.log`（`app.getPath('logs')`），每行带 ISO 时间与本次启动 `+ms`；内存只留最近 200 行 | [index.ts:3532](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L3532)、[harness-runtime.ts:818-836](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L818-L836) |

**"不自动重启"是可复核的设计选择**：与 `12_单文件桌面壳`（自动重拉 + 3 次封顶）不同，这里的 Harness 崩溃直接变成可操作状态，交给恢复面。`[SRC-TARGET]` 只证明状态机，不证明用户体验。

### 2.2 端口：代码是"优先固定"，文档写"随机"

`DEFAULT_HARNESS_PORT = 43129`，**优先**占用 43129（为了 Chromium 前端缓存跨启动复用），只有该端口被占时才退到临时端口。`[SRC-TARGET]` [L56](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L56)、[L580-582](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L580-L582)、[L1103-1111](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L1103-L1111)，注释写明取舍。

**这里有一处 DOC 与 SRC 对不上**：`docs/architecture.md` 的拓扑图与手机章节都写 "Harness Web UI on 127.0.0.1 **random port**" / "Harness itself stays on a random loopback port"（[architecture.md:10](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/docs/architecture.md#L10)、[:102](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/docs/architecture.md#L102)），而代码优先固定 43129。卡片的"随机端口"**继承自文档措辞**，不是作者的运行观察；引用时应写"文档称随机，代码固定优先"。安全结论不变：无论是 43129 还是临时端口，都只绑 `127.0.0.1`。

### 2.3 单实例与"深链"

- `[SRC-TARGET]` `app.requestSingleInstanceLock()`；没有锁就 `app.quit()`（[index.ts:3976-3979](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L3976-L3979)）。
- 第二实例**不进主流程**：只把 argv 当指令——带 `--safe-mode` 就开恢复面，否则在就绪时把已有窗口拉到前台（[L3992-4002](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L3992-L4002)）。
- **没有**外部深链协议：已读文件里没有 `setAsDefaultProtocolClient`、没有 `open-url` 监听；`dsh-desktop://` 是**内部页面协议**（把 `build/*.html` 挂到可被 http 页面 iframe 的真实 origin 上，另有 `dsh-desktop://harness/` 代理），不是给浏览器/系统用的深链（[desktop-protocol.ts:1-10](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/desktop-protocol.ts#L1-L10)、[L55-74](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/desktop-protocol.ts#L55-L74)、[architecture.md:29](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/docs/architecture.md#L29)）。`[RUN]` grep 在**已读**文件中 0 命中；未读文件见 §8，故为"未发现"而非"确证没有"。
- `launchd` 拉起的实例在取锁**之前**就 `app.exit(0)`，避免一次后台启动把用户窗口顶到前台（[L3965-3970](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L3965-L3970)）。

### 2.4 关窗 ≠ 退出：**Windows 才 hide-to-tray**，macOS 靠另一条规则

`[SRC-TARGET]` `shouldKeepRunningInBackground(platform, quitting)` 的实现只有一行：`platform === 'win32' && !quitting`（[close-to-tray.ts:1-6](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/close-to-tray.ts#L1-L6)）。于是两条不同的路径：

- **Windows**：`window.on('close')` 里 `preventDefault()` + `window.hide()`，进程留在托盘（[index.ts:1176-1179](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L1176-L1179)）；
- **macOS**：允许关窗，随后 `window-all-closed` 因 `process.platform !== 'darwin'` 不成立而**不退出**（[L4022-4024](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L4022-L4024)）。

真正退出走 `before-quit`：先 `preventDefault()`，flush 存储、停更新器、销毁托盘、dispose 维修 Agent，再 `runtime.stop()` + `mobileBridge.stop()`（[L4026-4040](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L4026-L4040)）。**注意**：它没有"关闭即最小化到托盘"的统一策略，两个平台的机制不同，卡片写"菜单栏/托盘常驻，关窗口不等于退出"对 mac/win 都成立，但**原因不同**，别移植成一条规则。

### 2.5 进程监督：壳盯自己，不盯 Harness

`[SRC-TARGET]` `ProcessRecovery`（[process-recovery.ts:21-24](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/process-recovery.ts#L21-L24)）负责的是 **Electron 自己**的三类失败：

| 失败 | 行为 | 位置 |
|---|---|---|
| GPU 连续 3 次退出（120s 窗口内） | 探针确认真实失联才降级；软件渲染重启 | [L71-97](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/process-recovery.ts#L71-L97) |
| OOM | 先停 Harness、释放页面，再弹窗（重试/退出） | [L118-131](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/process-recovery.ts#L118-L131) |
| 主窗口渲染进程崩溃 | 走 `RendererNavigationRecovery`，与 GPU/内存策略互不覆盖 | [L21-24](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/process-recovery.ts#L21-L24)（注释） |

GPU 侧另有 `app.on('child-process-gone')` 只认 `type === 'GPU'`，且把 TDR（`exitCode 34`）当 Chromium 自愈、不计入降级（[index.ts:938-948](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L938-L948)）。

### 2.6 更新与安装包

| 断言 | 代码事实 | 位置 |
|---|---|---|
| 6 小时一次 | `UPDATE_CHECK_INTERVAL_MS = 6h` | [update-policy.ts:1](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/update/update-policy.ts#L1) |
| 启动后"不久" | `15s` 延迟 + `0–15s` 抖动 | [update-policy.ts:2-3](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/update/update-policy.ts#L2-L3) |
| 先问 | `autoUpdater.autoDownload = false`；`update-available` 只进状态，下载要显式触发 | [update-manager.ts:418](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/update/update-manager.ts#L418)、[L434-448](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/update/update-manager.ts#L434-L448) |
| 装完要点按钮 | `autoInstallOnAppQuit = false`；只有用户动作后 `autoUpdater.quitAndInstall(false, true)` | [update-policy.ts:4](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/update/update-policy.ts#L4)、[update-manager.ts:391](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/update/update-manager.ts#L391) |
| 跳过这一版 | `update-skip.json` 存单版本；**手动检查忽略 skip**，因此跳过可撤回；后续版本照常询问 | [skipped-version.ts:1-13](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/update/skipped-version.ts#L1-L13)、[L23-27](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/update/skipped-version.ts#L23-L27) |
| 平台 | 仅 `darwin` / `win32` 且 `isPackaged` 才开自动更新 | [update-policy.ts:6-8](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/update/update-policy.ts#L6-L8) |
| 休眠回来补检 | `powerMonitor.on('resume')` → 超过 6h 才查 | [update-manager.ts:195-196](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/update/update-manager.ts#L195-L196) |
| 源 | `electron-updater` + `provider: 'generic'` feed，pre-release 才 `allowPrerelease` | [update-manager.ts:253-256](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/update/update-manager.ts#L253-L256) |

`[SRC-TARGET]`（树级）签名/公证的**管线存在**：`scripts/notarize-macos.mjs`、`scripts/jsign-windows-hook.mjs`、`build/entitlements.mac.plist`、`.github/workflows/release.yml`、`scripts/verify-target.mjs` 都在该提交的树里。**"产物已签名/已公证"本轮无法验证**——没有下载任何 Release 资产，也没读 `release.yml` 内容。

## 3. 上游 `desktop` 契约：为什么外部 CLI 会被拒

四个层次，全部 `[SRC-DSH]` `@deepseek-ai/dsh@0.2.1-rc.3`：

1. **参数层就拒，且大小写不敏感。** `rejectElectronProfile` 用 `profile.toLowerCase() === "desktop"`（`lib/bin.js:35-37`），在 `--profile` 的 action 里先于任何文件操作执行（`:112`）。所以 `dsh --profile desktop --dump-config`、`dsh plugin --profile desktop add …`、`--from-default-profile web` 三条都在解析期死掉，**profile 目录一个字节都不会被创建**。
2. **唯一放行口是程序化选项，不是 flag。** `parseDshArgs(argv, version, manageDesktopProfile = false)`（`:101`），只有 `runCli({ manageDesktopProfile: true })` 能打开 `plugin` 分支的闸门（`:119`）；类型注释写"reserved for its installed carrier"（`lib/types/bin.d.ts:6-10`）。CLI 本身**没有** `--manage-desktop-profile` 之类的参数。
3. **即使放行，profile 必须"已初始化"。** `requireDesktopProfile` 只在 `$DSH_HOME/profiles/desktop/package.json` 存在时放行，否则报 "Open DeepSeek Harness Desktop once…"（`lib/plugin-BiveYA7h.js:10-12`）；`plugin` 分支还**故意不为 `desktop` 建目录**（`:38-40`），并在写锁（120s）内外各查一次（`:64-65`、`:90-91`）。
4. **`desktop` 不是出厂模板。** `PROFILE_TEMPLATES` 里没有它（`dsh-app-boot/lib/index.js:551-557`），默认 bundle 只有 `@deepseek-ai/dsh-base`（`:570`）。也就是说这个名字**只能由一个外部 Electron 进程先创建**，CLI 侧永远无法自举。

**对第三方壳的含义**：`desktop` 是上游的**保留名 + 安装态 carrier 协议**，不是可用资源；想复用它只能伪造一个"已初始化"的 profile，而那恰好是所有契约想阻止的状态。第三方发行版因此只有两条干净路：**自有 DSH_HOME + 非保留 profile**（本仓库：`web`），或**换一块屏**（TUI/手机）。

`[RUN]` 本机复现（临时 `DSH_HOME`，只跑 CLI 参数解析，不安装、不启动 Harness）：

```console
$ DSH_HOME=$(mktemp -d) dsh --profile desktop --dump-config
error: profile "desktop" is managed exclusively by the Electron application
$ DSH_HOME=$(mktemp -d) dsh plugin --profile desktop add left-pad
error: profile "desktop" is managed exclusively by the Electron application
$ DSH_HOME=$(mktemp -d) dsh --profile DESKTOP --dump-config      # 大小写不敏感
error: profile "desktop" is managed exclusively by the Electron application
$ DSH_HOME=$(mktemp -d) dsh --profile desktop --from-default-profile web --dump-config
error: profile "desktop" is managed exclusively by the Electron application
$ DSH_HOME=$(mktemp -d) dsh --profile web --dump-config | head -2
# == @deepseek-ai/dsh-base
- id: tool-plugin-manager
```

四次拒绝后临时 `DSH_HOME` **仍然是空目录**（`ls -A` 无输出）——与 §3 第 1 条"解析期就死、不建目录"一致；同一次会话里 `--profile web` 正常输出配置树，说明被拒的是**名字**，不是环境。

## 4. 本仓库怎么绕开：`web` profile + 自建 patch 栈

`[DOC]` patch 注释明确写着：

> `# Desktop keeps the existing web Profile; upstream only enables this for a Profile named desktop.`
> —— [build/dsh-desktop.patch.yml:25-28](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/build/dsh-desktop.patch.yml#L25-L28)

即：上游把 `ui-sidebar-browser` 只对名为 `desktop` 的 profile 打开，Desktop 在自己的 overlay 里手动打开它。`payload` 是三条 `--patch` 叠加层，**都晚于 profile 自己的层**（CLI 帮助文本："extra patch-list overlay applied after the profile layer"）：

| 顺序 | 文件 | 内容 | 位置 |
|---|---|---|---|
| 1 | `dsh-desktop.patch.yml` | 插入 log bridge、client-ui、workbenches、onboarding、market-installer、image-generation、ppt-composer、hmr-fallback、preset-transfer、office；关掉 `ui-brand-official`、`ui-settings-account`；打开 `ui-sidebar-browser` | [L1-L6](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/build/dsh-desktop.patch.yml#L1-L6)、[L18-L28](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/build/dsh-desktop.patch.yml#L18-L28)、[L30-L83](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/build/dsh-desktop.patch.yml#L30-L83) |
| 2 | `dsh-desktop-market.patch.yml` | **仅当** profile 的 `dsh.profile.bundles` 含 `dshmarket` 时才加 | [harness-runtime.ts:405-420](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L405-L420)、[L561-567](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L561-L567) |
| 3 | 由 Desktop 状态派生的 disabled overlay | `prepareHostDisabledPluginsPatch()` 按壳的插件状态再叠一层；正常 profile 才叠，Safe Mode 不叠 | [L568-571](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L568-L571) |

**"谁拥有插件开关"要分三处，别混成一句。** `[DOC]` 的三条自述合起来才是完整答案：

1. **开关的唯一权威**：`profiles/web/.dsh-market/state.json#disabled`（[architecture.md:82](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/docs/architecture.md#L82)）；
2. **`dsh.profile.bundles` 是派生的**：launch projection / bundle healing 可能把已安装 bundle 重新列出来，但**不等于重新启用**（同段）；
3. **显式开关会同步用户 patch 层，但只同步矛盾行**："treats `cordis.patch.yml` as structured user configuration … matches only direct top-level row IDs and boolean `disabled` overrides that contradict the requested package switch"，歧义 YAML **拒绝**而不是修补（[architecture.md:96](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/docs/architecture.md#L96)）。

所以"Desktop 只叠加、不改写 profile"是**错的**：它**不改 `dsh.profile.bundles` 来表达开关**，但会在用户 patch 层里按结构做最小同步。这条区分很重要——抄成"壳从不写用户配置"会在一次批量开关后把用户的 `cordis.patch.yml` 删成两行（文档 :96 正是在讲这个故障）。`[SRC-TARGET]` 侧对应的是 `plugin-disable.ts` 的"与 dsh-market 同一套写路径"（[L14-17](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/state/plugin-disable.ts#L14-L17)）。

## 5. Safe Mode：名字、组成、共享面

**卡片 §7 的第一个 `[OPEN]` 可以关掉。** `[SRC-TARGET]`：

| 问题 | 事实 | 位置 |
|---|---|---|
| profile 叫什么 | **`desktop-safe-mode`**（不是保留名 `desktop`，所以不需要任何豁免） | [safe-mode-profile.ts:6](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/state/safe-mode-profile.ts#L6) |
| 挂什么 | **`@deepseek-ai/dsh-base` + `@deepseek-ai/dsh-web-app`** 两个安装态 core bundle | [L7-10](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/state/safe-mode-profile.ts#L7-L10) |
| 自带文件 | 托管写 `package.json`、`cordis.patch.yml`、`pnpm-workspace.yaml`（`nodeLinker: hoisted`），内容不变就不重写 | [L12-22](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/state/safe-mode-profile.ts#L12-L22)、[L72-79](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/state/safe-mode-profile.ts#L72-L79) |
| 与正常 profile 共享什么 | **共享 DSH_HOME**（settings / credentials / sessions / workspaces）；**继承模型配置行**（`llm-*`、`agent-default-model` 等白名单），并删掉非法的 `baseURL`；**不**带第三方 bundle、不带非模型用户 patch | [L24-32](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/state/safe-mode-profile.ts#L24-L32)、[L34-70](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/state/safe-mode-profile.ts#L34-L70)、[L81-87](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/state/safe-mode-profile.ts#L81-L87) |
| 用谁的 `node_modules` | **不用 profile 的**：Safe Mode 启动时注入 `DSH_DESKTOP_HOST_RESOLVED=1`，注释写明"从补丁自身的安装树解析，不碰共享的 `profiles/node_modules`"（Windows junction 问题） | [harness-runtime.ts:369-372](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L369-L372) |
| 用哪套 patch | 换用 `dsh-desktop-safe.patch.yml`：只保留 brand 关闭、account 关闭、client-ui、hmr-fallback；**不引入** PPT / market / preset-transfer | `[SRC-TARGET]` `build/dsh-desktop-safe.patch.yml`（§8 未逐行核） |

**卡片 §2.3 的流程要补一条入口。** 代码里有**第三条**：preflight/维护判定需要恢复时**自动进** Safe Mode，不需要用户点菜单——

`maintenance.outcome === 'safe-recovery'` → `enterMigrationSafeRecovery()` → `ensureSafeModeProfile()` → `runtime.start(launchDirectory, SAFE_MODE_PROFILE)`（[index.ts:1637-1645](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L1637-L1645)、[L1516-1542](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L1516-L1542)），并且在 `runtime.stop()` 之后、启动之前把可疑 bundle 塞进"疑似插件"列表（`repairTarget`，[L1527-1531](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L1527-L1531)）。

而卡片说的"命令行 `--safe-mode`"是**应用自己的 argv**：`shouldStartInSafeMode(argv)` 只做 `argv.includes('--safe-mode')`（[safe-mode.ts:116-118](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/safe-mode.ts#L116-L118)），第二实例的同名参数也走这条路（[index.ts:3994-3996](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L3994-L3996)）。`dsh --safe-mode` 在 CLI 侧**不存在**。

**"指认插件"的证据是什么（卡片 §7 第二个 `[OPEN]`，基本关闭）**：有**两条**证据通道，都不是"异常栈分析"。

1. **结构化通道**：壳的入口在宿主抛出错误后遍历 `cause` / `AggregateError`，只取插件失败对象里的 `dshPluginFailure` 字段，序列化成**一行** `[harness-node] plugin failures {"version":1,"failures":[{stage,entryId,packageName,owner,chain,message}]}`——注释明确写"不要序列化任意 Error 属性、插件配置或整个 context/fiber 图"（[harness-node-entry.mjs:34-56](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/build/harness-node-entry.mjs#L34-L56)）。这是**上游 loader 主动标注的归属信息**，不是猜。
2. **日志行模式**：`extractPluginReferences` 认 `failed to (apply|import) loader entry (…)`、`cannot resolve profile bundle "X"`、`profile bundle "X" declares no dsh.bundle`、`plugin(s) failed to load: X`、`X: pending (waiting for service: …)`、`Failed to load plugins` 之后的行；只有出现 `duplicate prefix route` 时才额外从 `profiles/<name>/node_modules/<pkg>` 栈帧取 owner（[harness-runtime.ts:947-1017](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L947-L1017)），且 `@deepseek-ai/*` 与 `dsh-base`/`dsh-web-app`/`dshmarket` 被**排除**在可操作列表外（[L929-945](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L929-L945)）。

前端证据是第三条通路，在 `applyPendingFrontendEvidence()` / `takePendingFrontendPluginRecovery()` 里与运行时证据合并（[index.ts:2604-2620](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/index.ts#L2604-L2620)）。`[DOC]` 把它总结为"collects log and renderer evidence, resolves ownership through the profile manifest, lockfile, bundles, loader entry IDs, slot conflicts, dependencies, and Cordis patch rows"（[architecture.md:74](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/docs/architecture.md#L74)）——注意这一句说的是"**归属解析**"，不是"故障判定"；`plugin-recovery-detection.ts` 本轮未读，前端证据的判定条件仍 `[OPEN]`。

## 6. 应用内插件管理：一条权威 + 三条硬约束

`[DOC]` + `[SRC-TARGET]` 合起来能确定"插件到底开没开"由谁说了算——这一点卡片完全没有，但它是宿主型产品最该抄的部分：

> **唯一权威是 `profiles/web/.dsh-market/state.json#disabled`**；Harness 启动时在解析前就跳过被关掉的包；`dsh-market`、官方 Plugin Manager（经 `profileBundlePackageBackend` 的 `switched`/`removed` 钩子）、workbench、Recovery、Safe Mode 全部写同一处；`dsh.profile.bundles` 只是**派生的可组合性**，重新列出已安装 bundle 不等于重新启用它；卸载路径会忘掉这个开关，所以重装默认是开的。
> —— [architecture.md:82](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/docs/architecture.md#L82)

配套的**包归属**是两条腿：**generation registry** 拥有"按代安装"的插件，**pnpm** 拥有共享树与 Profile 自有包；两套互斥，generation 后端对后者返回 declines（同段）。`[SRC-TARGET]` `plugin-disable.ts` 的写路径与 dsh-market 自己的开关一致（读 `.dsh-market/state.json#disabled`，[L14-17](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/state/plugin-disable.ts#L14-L17)、[L196-215](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/state/plugin-disable.ts#L196-L215)），并对用户 patch 层按**结构化 YAML** 处理（只认顶层 row id + 布尔 `disabled`，歧义 YAML 直接拒绝，[architecture.md:96](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/docs/architecture.md#L96)）。

三条硬约束：

1. **pnpm 由壳提供，不由用户 PATH 提供。** 拉起 Harness 时从环境里**剥掉** `DSH_DESKTOP_PNPM_ENTRY/RUNNER/HIDE_CONSOLE_BOOTSTRAP`，再按打包路径重新注入（[harness-runtime.ts:319-327](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L319-L327)、[L373-379](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/harness-runtime.ts#L373-L379)）；入口把打包的 pnpm 交给 `runCli({ packageManager })`（[harness-node-entry.mjs:112-132](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/build/harness-node-entry.mjs#L112-L132)）。用户装的 `pnpm` 版本不影响应用内安装。
2. **store 必须被钉住，否则插件系统整体锁死。** pnpm 把 store 记在 `.modules.yaml`，换了 store 就 `ERR_PNPM_UNEXPECTED_STORE`，"not just installs, but uninstalls, updates and repairs"；壳在启动维护阶段把**pnpm 自己记录过的** store 写进 profile 的 `.npmrc`，只陈述既有事实、不新选 store（[profile-store.ts:5-19](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/state/profile-store.ts#L5-L19)、[L89-112](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/state/profile-store.ts#L89-L112)），另有只读一致性检查给出可读诊断（[L119-138](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/state/profile-store.ts#L119-L138)）。
3. **插件安装是"应用内的一个插件"，且每次写操作都受时长约束。** `dsh-desktop.patch.yml` 插入 `dsh-desktop-market-installer`（固定 target 的 `dsh-market` 安装器）作为设置入口（[build/dsh-desktop.patch.yml:38-44](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/build/dsh-desktop.patch.yml#L38-L44)）；壳侧的 profile 包命令**硬编码 `PROFILE = 'web'`**，并给每个操作设 15 分钟上限、30 分钟修复上限、2 分钟无进展即判停滞、5 秒轮询进度（[profile-plugin-command.ts:12-30](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/src/main/runtime/profile-plugin-command.ts#L12-L30)）。**壳不暴露 `dsh plugin` 的任意参数入口**——这条是 `[OBS]`（读 patch、设置入口与命令封装得出），未经 UI 实测。

## 7. 对卡片的校正

| 卡片说法 | 一手证据 | 可以怎么说 |
|---|---|---|
| "官方 Electron 桌面应用（Dataelem）"、"DSH 把 `desktop` 判给了官方应用（本卡）" | 上游守卫**不含产品名**（7 行，§1.3）；本仓库自己的补丁说"Desktop keeps the existing **web** Profile" | 上游的 `desktop` 保留名是**匿名契约**；本仓库是**绕开**它的第三方发行版。两件事分开写，不能互为证据 |
| "Harness 只在**随机** 127.0.0.1 端口" | 代码优先 `43129`，冲突才临时端口；**文档**也写 "random port"，所以卡片是在抄文档 | 改为"**代码优先固定 43129（复用前端缓存），冲突退临时端口**；文档措辞是 random，两者不一致处要标注" |
| "Safe Mode 用的 profile **叫什么** `[OPEN]`" | `desktop-safe-mode`，core bundle 仅 `dsh-base` + `dsh-web-app` | 关掉该 `[OPEN]`；顺带写明它**共享 DSH_HOME**、**继承模型行** |
| "是否与正常 `web` profile 共享 `node_modules` `[OPEN]`" | `[DOC]` "Safe Mode uses the installation anchor … **without requiring `profiles/node_modules`**"（[architecture.md:92](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/docs/architecture.md#L92)）+ `DSH_DESKTOP_HOST_RESOLVED=1` | 关掉该 `[OPEN]`；"隔离"指**插件集合与解析根**，不是数据根 |
| "两条入口：菜单 + 命令行" | 还有**自动**入口：preflight/维护判定 `safe-recovery` 直接进 | 改为"三条入口（菜单 / `--safe-mode` / 自动），命令行是逃生死锁" |
| "命令行 `--safe-mode`" | 应用 argv 的开关；CLI 无此参数 | 写成"**DSH Desktop 自己的** `--safe-mode`"，避免读者以为 `dsh --safe-mode` 有效 |
| "不碰用户的 `~/.dsh`" | 正常启动每次都调 `maybeImportWebHome(dshHome)`；`[DOC]` 只承诺"upgrades do not replace profile/plugin/workspace/session/model data"（[architecture.md:54](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/docs/architecture.md#L54)） | **不能**再写"不碰"；改为"**默认 DSH_HOME 在 Electron userData 下**，另有一次从旧 web home 的导入步骤（实现未读，读/写边界 `[OPEN]`）" |
| "启动/前端插件故障会被识别；指认具体插件" | 两条通道：入口序列化的 `dshPluginFailure`（stage/entryId/packageName/owner/chain）+ 日志行模式；core 包被排除 | 成立，但要写清"**上游标注的归属 + 日志行匹配**"；前端判定那一半 `[OPEN]` |
| "6 小时 / 先问 / Restart and install / 跳过这一版" | 全部命中；补 15s+抖动、resume 补检、`autoInstallOnAppQuit=false`、仅 darwin/win32 | 成立且可加强；"跳过"**可撤回**（手动检查忽略 skip） |
| 卡片未写"插件开关谁说了算" | `[DOC]` 唯一权威 = `.dsh-market/state.json#disabled`；`dsh.profile.bundles` 是派生；generation registry 与 pnpm 分属两套归属 | 值得单列一条机制：**开关状态与包归属分离**，否则"重新列出 bundle"会被误当"重新启用" |
| "渲染器无 Node + context isolation + sandbox；外链交系统浏览器" | `[DOC]` 逐条列出（[architecture.md:58-68](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/docs/architecture.md#L58-L68)），但 `security.ts`/`desktop-navigation.ts`/`window-permissions.ts` 本轮未读 | 可保留 `[DOC]` 级；**代码级未核**，不要写"已验证" |
| "签名 + 公证 + 每平台各构建一次" | 树里有 `notarize-macos.mjs`、`jsign-windows-hook.mjs`、`entitlements.mac.plist`、`verify-target.mjs`、`release.yml`；`[DOC]` 说 Windows 安装包**签名后重生成 blockmap 与元数据**、mac 双架构元数据合并（[architecture.md:117](https://github.com/dataelement/dsh-desktop/blob/1a6212edb321509c3ee00e5d857fadfce13a7790/docs/architecture.md#L117)） | 说"**管线在**"即可；"产物已签名"需资产级证据，本轮没有 |

## 8. 未核实（`[OPEN]`，含本轮读失败清单）

- **未安装、未构建、未运行**：不验证签名/公证、不验证 Safe Mode 真能起、不验证 `web` profile 与外部 `dsh plugin` 共存、不验证 GPU/OOM 恢复路径。
- **本轮读失败的目标文件**（GitHub 连接中断）：`src/main/state/web-home-import.ts`（`maybeImportWebHome` 的实现）、`src/main/security.ts`、`src/main/desktop-navigation.ts`、`src/main/window-permissions.ts`、`src/main/plugin-recovery-detection.ts`、`README.md`、`.github/workflows/release.yml`、`docs/patch-plugin-contract.md`、`docs/release-runbook.md`。**已读并可用于本 memo 的**：`docs/architecture.md`、`build/harness-node-entry.mjs`、`src/main/close-to-tray.ts`、`src/main/state/plugin-disable.ts`、`src/main/runtime/profile-plugin-command.ts`。
- `maybeImportWebHome` 对 `~/.dsh` 是**只读导入**还是**双向写入**：实现未读，卡片"不碰 `~/.dsh`"因此**不能成立为事实**。
- `DSH_DESKTOP_HOST_RESOLVED` 的**消费端**在 `dsh-app-boot` / `dsh-client-modules` 的两个补丁里（`[DOC]` architecture.md:92 自述 `Symbol.for("dsh.desktop.host-module-base-url")`），补丁本体本轮未读。
- **tag → 安装包版本**的注入步骤（`release.yml` / `electron-builder` 配置）：manifest 停在 `0.12.1` 而 tag 到 `v0.13.0`，两者谁进 `CFBundleShortVersionString` 未验证。
- 36 个 rc.3 补丁的**语义**只核了 `@deepseek-ai/dsh` 那一个；其余 35 个只按文件名归类，未逐个读 diff。
- `desktop` 保留名对应的真实 carrier 是谁：上游一手来源**没有**任何产品指向，本仓库也不自称（它的入口只调 `runCli({ packageManager })`，从不申请该豁免）；"官方 Electron 应用"在证据上仍是**未命名主体**。
- preview/stable 通道与社区插件的兼容矩阵：仍只有 `[DOC]` 一句 "may be incompatible"。

## 9. 复现命令（只读）

```sh
git clone --filter=blob:none --no-checkout https://github.com/dataelement/dsh-desktop dshdesk
git -C dshdesk log -1 --format='%H %cI' main
git -C dshdesk tag --sort=-creatordate | head -3
git -C dshdesk show v0.13.0:package.json | head -3      # 0.12.1 ≠ v0.13.0
git -C dshdesk ls-tree -r --name-only HEAD patches/ | wc -l
git -C dshdesk cat-file -p HEAD:src/main/runtime/harness-runtime.ts | sed -n '253,270p'
git -C dshdesk cat-file -p HEAD:build/dsh-desktop.patch.yml | sed -n '25,28p'
git -C dshdesk cat-file -p HEAD:docs/architecture.md | sed -n '10p;29p;35p;42p;72p;82p;92p;102p'
git -C dshdesk cat-file -p HEAD:build/harness-node-entry.mjs | sed -n '34,56p;112,132p'
git -C dshdesk cat-file -p HEAD:src/main/close-to-tray.ts

# 宿主侧（本机 0.2.1-rc.3）
cd "$(npm root -g)/@deepseek-ai/dsh"
grep -n 'managed exclusively' lib/bin.js
grep -n 'manageDesktopProfile' lib/bin.js lib/types/bin.d.ts
grep -n 'profile !== "desktop"' lib/plugin-BiveYA7h.js
grep -n 'const PROFILE_TEMPLATES' node_modules/@deepseek-ai/dsh-app-boot/lib/index.js

# 参数层拒绝（临时 DSH_HOME，不安装/不启动）
H=$(mktemp -d); DSH_HOME="$H" dsh --profile desktop --dump-config
DSH_HOME="$H" dsh plugin --profile desktop add left-pad
DSH_HOME="$H" dsh --profile DESKTOP --dump-config
ls -A "$H"          # 期望：空
```

> **给下一轮的三步**（按性价比排序）：① 读 `src/main/state/web-home-import.ts`，判定"不碰 `~/.dsh`"能否保留；② 读 `src/main/security.ts` + `desktop-navigation.ts` + `window-permissions.ts`，把渲染器安全从 `[DOC]` 升到 `[SRC-TARGET]`；③ 读 `release.yml`，确认 tag 与安装包版本的注入关系，再决定卡片是否继续引用 `v0.13.0` 这个坐标。
