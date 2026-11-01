---
title: "SURFACES · web 与 Desktop：同一份界面，两种壳"
domain: lifecycle
kind: charter
positioning: "先分清保留名 carrier 与社区桌面壳，再证明两者共用 dsh-web-app，并列出四个会静默失效的分叉。"
read_when: "要判断某个装法/配置/首启逻辑在 Desktop 上是否等价；或排查 Desktop 装完看不到。"
status: living
updated: 2026-11-01
budget: 165
---
# web 与 Desktop

> **页头证据级别**：web 面 `[RUN]` + `[DSH]`；**社区桌面壳**（`dataelement/dsh-desktop@1a6212e`）`[SRC-TARGET]`，只读源码、未装未跑；**保留名 carrier**（上游代码里那个匿名的 "the Electron application"）只有 `[DSH]` 契约，没有公开应用/源码。任何“Desktop 上会怎样”的句子都要先问是哪一种。
> 社区壳的来源核对见产品册 [`shell/11`](../../leverage-reshape-product/shell/11_桌面应用-dsh-desktop.md) 与 [`04 源码复核`](../../leverage-reshape-product/shell/_证据/04_桌面应用-dsh-desktop-源码复核.md)；本册只引用其 home / profile / 插件开关事实。

## 1. 先分清两个“Desktop”

上游只守一个**名字**，不认产品：`desktop` 是保留 profile，由安装态的 Electron carrier 通过程序化开关管理 `[DSH]`（`lib/bin.js:35-37`、`:98-101`、`:119`）。但这不等于“所有桌面应用都用 `desktop`”。

| | 保留名 carrier | 社区桌面壳（dsh-desktop） |
|---|---|---|
| profile | `desktop` | **`web`**（默认参数；`harness-runtime.ts:256`、`:316`、`:394`、`:493`） |
| `DSH_HOME` | 未知（DSH 只约束 profile 名，不约束 home） | **`app.getPath('userData')/harness`**（`index.ts:1567`、`:1662`） |
| 谁创建 profile | Electron 应用 | 壳的 main 进程（初始化 + 维护） |
| CLI 能否管理 | 不能：`--profile desktop` 解析期拒绝 | 能跑 `--profile web`，但写的是当前 home 的 `profiles/web`（默认 `~/.dsh`），**不是**壳的 `userData/harness/profiles/web` |
| 应用内 Plugins 页 | 同一个客户端包 | **同一个**客户端包，作用在它自己的 `web` profile |
| 证据 | `[DSH]` 契约 | `[SRC-TARGET]` 固定提交 |

> **一句话**：应用内装对两种 Desktop 都成立；**CLI 对两种 Desktop 都不成立**——保留名被拒，社区壳则因为 home 不同而写不到。

**官方 carrier 的三条公开契约** `[DSH]`（`@deepseek-ai/dsh/README.md:20`、`:60`、`:62`）：

1. `desktop` 是 **Electron-owned profile**，CLI 拒绝它的启动 / dump / 插件管理；
2. Desktop 安装态自带的命令可以用程序化开关管理**已初始化**的 `desktop` profile；
3. `@deepseek-ai/dsh/profile-boot` 把同一套 profile 生命周期交给 Desktop host；应用 profile 提供自己的 install anchor，但**保留 Harness home patch**、proxy、telemetry、patch reload 与有界关闭。

第 3 条意味着：`$DSH_HOME/cordis.patch.yml` 的语义对官方 carrier 仍成立；**但 home 放在哪、UI 怎么提示 `restart-required`，没有公开源码**。

## 2. 保留名的三道闸：普通 CLI 进不去 `desktop`

| 动作 | 结果 | 证据 |
|---|---|---|
| `dsh --profile desktop` | `error: profile "desktop" is managed exclusively by the Electron application` | `[DSH]` `lib/bin.js:36`；`[RUN]` exit 1 |
| `dsh plugin --profile desktop add <pkg>` | 同一条错误 | `[DSH]` `lib/bin.js:119`；`[RUN]` |
| Electron carrier 自己调用 | 允许，用程序化开关 `manageDesktopProfile` 放行；官方 carrier 的 bundled command 就是这条 | `[DSH]` `lib/bin.js:98-101`、`:209-210`；`README.md:20`、`:62` |

注意第三行：**`manageDesktopProfile` 不是命令行参数**，是 `runCli` 的程序化选项。所以第三方安装器、脚本、agent 都拿不到这个口子。`desktop` 是“保留名 + 安装态 carrier 协议”，不是可用资源。

## 3. 四个会“静默失效”的分叉

1. **拿 CLI 装 Desktop**：
   - 保留名 carrier：`--profile web` 写当前 home 的 `profiles/web`（默认 `~/.dsh`），App 用它自己 home 下的 `profiles/desktop`（默认 home 才是 `~/.dsh`；官方 home 未公开）——报告成功但界面没有 `[CARD]`。
   - 社区壳：`--profile web` 写当前 home 的 `profiles/web`（默认 `~/.dsh`），App 用 `userData/harness/profiles/web`——**连 profile 名都猜对了也写不到** `[SRC-TARGET]`（`index.ts:1567`、`:1662`；`profile-plugin-command.ts:12-30` 硬编码 `PROFILE='web'`）。
2. **home 层供货**：往 `~/.dsh/cordis.patch.yml` 插一个只装在某个 profile 的包，另一个 profile 启动时报 `warning: 1 entry did not activate` + `ERR_MODULE_NOT_FOUND`，**服务照常起来**（第三方行不在 required 名单里），用户只看到功能缺失 `[RUN]`（[`_证据/02`](../_证据/02_隔离实测记录.md) E8）。社区壳的 home 是它自己的 `userData/harness`，这条 home 层同样不跨过去。
3. **首启文案**：`welcome-notice` 这一步在带 `dshDesktop` 全局的壳里**不注册**（代码里 `if (!('dshDesktop' in globalThis))`）`[DSH]`（`dsh-client-ui-settings-models/lib/client.js:4502`）。依赖它做首屏的产品，会少一段而没有任何报错。
4. **社区壳的开关权威**（只在社区壳）：插件是否启用由 `profiles/web/.dsh-market/state.json#disabled` 决定，`dsh.profile.bundles` 只是派生；直接改 roster 不等于启用 `[SRC-TARGET]`（`architecture.md:82`；产品册 memo §6）。这是“装上了但 UI 仍是关的”的另一种来路。

## 4. 两个面真正共享的东西

| 共享 | 含义 |
|---|---|
| 同一份 `dsh-base` + `dsh-web-app` | 你的 bundle 只写一次，web 与两种 Desktop 都能加载 |
| 同一个 Plugins 页 | 安装动作在应用内是一句话；作用在“当前 home 的当前 profile” |
| 同一套 patch 方言 | profile / home / `--patch` 三层在两面语义一致（社区壳也靠 `--patch` 叠自己的层） |
| 同一套 settings 命名空间 | 你的配置在两面同名同构 |
| 同一套首启账本 | 但带 `dshDesktop` 的壳会跳过 `welcome-notice` |
| 同源 `rev` 函数 | rc.3 的 `comboRevision` 对“有序行集合的 (id, rev)”做 hash（`dsh-client-modules/lib/index.js:332-334`）；社区壳对 `dsh-client-modules` 有补丁（URL/host 解析），是否动到 rev 计算未读补丁，见 §7 |

## 5. 两个面真正不同的东西

| 不同 | web | 保留名 carrier | 社区桌面壳 |
|---|---|---|---|
| profile 名 | `web` | `desktop` | `web` |
| home | `~/.dsh`（或 `DSH_HOME`） | 未知（home patch 保留，位置未公开） | `userData/harness` |
| 谁创建 profile | CLI（首次 `dsh plugin` 或出厂模板） | Electron 应用 | 壳的 main 进程 |
| CLI 可否管理 | 可以 | 不可以（见 §2） | 可跑但 home 不对，等于不可以 |
| 崩溃恢复 | 由用户/宿主 | 未知 | 壳的恢复面（不自动重启 Harness；`harness-runtime.ts:668-683`） |
| 更新 | 宿主升级 | 壳自己的更新器（未知） | 应用更新器：先问、再下、再 `quitAndInstall`（产品册 memo §2.6） |

## 6. 给产品作者的四条判据

1. **先问“哪一个 Desktop”**：保留名 carrier 还是社区壳？两者的 profile 与 home 不同，不能共用一句“Desktop 用 `profiles/desktop`”。
2. **安装说明只写应用内装**：它对两种 Desktop 都成立。CLI 命令必须标“仅 `dsh web`”，并补一句“社区桌面壳的 `DSH_HOME` 是私有的，`--profile web` 不命中”。
3. **有没有假设 profile 名或 home**：假设 `web` 或 `desktop` 都可能错；假设 `~/.dsh` 一定错（社区壳是 `userData/harness`）。
4. **首屏是否依赖 `welcome-notice`**：依赖就必须给带 `dshDesktop` 的壳留替代路径。

## 7. 已关与仍开

- **已关（保留名 carrier 契约）**：`desktop` 是 Electron-owned profile；CLI 三条入口全拒；bundled command 可程序化管理已初始化 profile；`profile-boot` 共用；home patch 保留 `[DSH]`（`README.md:20`、`:60`、`:62`）。
- **已关（社区壳）**：`DSH_HOME` 固定为 `userData/harness`；profile 是 `web`；Safe Mode 是 `desktop-safe-mode`（`safe-mode-profile.ts:6-10`）；插件开关权威是 `.dsh-market/state.json#disabled`。
- **推断（保留名 carrier 结构）**：`profiles/desktop` 按 `profile-boot` 的共享生命周期，应同样是 `package.json` + `cordis.yml` + `cordis.patch.yml` + `pnpm-workspace.yaml`（E1 的四件套）`[OBS]`；home 路径与应用内 UI 仍未公开。
- **部分关闭（`rev`）**：rc.3 的 `comboRevision` 两面共用；具体 `rev` 值会因叠加层/行集不同而不同。社区壳对 `dsh-client-modules` 有补丁，补丁是否改 rev/URL 未读。
- `[OPEN]` **保留名 carrier 的 home 与 UI**：`profiles/desktop` 的结构可按 `profile-boot` 推为标准 profile 四件套，但 home 路径与应用内 `restart-required` 提示没有公开源码；复核条件：一台装过官方 carrier 的机器，或 carrier 源码。
- `[OPEN]` 官方 carrier 是否复用同一 `dsh.client` 下发/`rev` 实现（`profile-boot` 同源是 `[DSH]`，但不等于 UI 注入路径相同）。
- `[OPEN]` 社区壳应用内装的 `application` / `warnings` / `nextStep` 实际取值：源码级走同一 `pluginManager`，但未跑 UI；复核条件：一台装过 dsh-desktop 的机器。
- `[OPEN]` 社区壳 `maybeImportWebHome` 对 `~/.dsh` 的读写边界（产品册 memo 亦未读实现）；本册只据 `userData/harness` 判断主 home。
- `[OPEN]` 社区壳 36 个 rc.3 补丁是否改 `dsh-client-modules` 的 rev/URL 计算（补丁本体未读）。
