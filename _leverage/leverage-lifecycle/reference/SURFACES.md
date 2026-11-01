---
title: "SURFACES · web 与 Desktop：同一份 bundle，两个 profile"
domain: lifecycle
kind: charter
positioning: "证明 dsh web 与 Electron Desktop 共用同一套 bundle、只差 profile 名，并列出三处会静默失效的分叉。"
read_when: "要判断某个装法/配置/首启逻辑在两个面上是否等价；或排查 Desktop 上装完看不到。"
status: living
updated: 2026-11-01
budget: 150
---
# web 与 Desktop

> **页头证据级别**：web 面 `[RUN]` + `[DSH]`；**Desktop 面仅 `[DSH]`**——本机没有 `desktop` profile，也没有 Electron 应用，未做实机验证。任何"Desktop 上会怎样"的句子都不得读成实测。

## 1. 它们是什么关系

**同一个浏览器界面，两个 profile 名。**

- `dsh-web-app` 这层 bundle 里，三处行按 profile 名分叉：`ctx.get('profileContext')?.name !== 'desktop'` `[DSH]`（`dsh-web-app/cordis.patch.yml:47`、`:59`、`:298`）。
- `dsh-base` 里还有一处 `desktopPlatform`，同样按 `name === 'desktop'` 取平台 `[DSH]`（`dsh-base/cordis.patch.yml:123`）。
- 出厂的 profile 模板只有 `acp` / `web` / `headless` / `sdk` / `sdk-minimal`，**没有 `desktop`** `[DSH]`（`dsh-app-boot/lib/index.js:551-559`）。

**推论**：`desktop` 不是"另一个界面"，是**同一个界面换了 profile 名**；它不由 CLI 创建，由 Electron 应用创建。

## 2. 三道闸：普通 CLI 进不去 `desktop`

| 动作 | 结果 | 证据 |
|---|---|---|
| `dsh --profile desktop` | `error: profile "desktop" is managed exclusively by the Electron application` | `[DSH]` `lib/bin.js:36`；`[RUN]` exit 1 |
| `dsh plugin --profile desktop add <pkg>` | 同一条错误 | `[DSH]` `lib/bin.js:119`；`[RUN]` |
| Electron carrier 自己调用 | 允许，用程序化开关 `manageDesktopProfile` 放行 | `[DSH]` `lib/bin.js:98-101`、`:209-210` |

注意第三行：**`manageDesktopProfile` 不是命令行参数**，是 `runCli` 的程序化选项。所以第三方安装器、脚本、agent 都拿不到这个口子。

## 3. 三处会"静默失效"的分叉

1. **装错 profile**：在 Desktop 机器上执行 `dsh plugin --profile web add X`，包进了 `profiles/web`，App 用的是 `profiles/desktop`——报告成功但界面没有 `[CARD]`（产品线 `51` 卡已量到）。
2. **home 层供货**：往 `~/.dsh/cordis.patch.yml` 插一个只装在某个 profile 的包，另一个 profile 启动时报 `did not activate`，**服务照常起来**，用户只看到功能缺失 `[RUN]`（[`_证据/02`](../_证据/02_隔离实测记录.md) E8）。
3. **首启文案**：`welcome-notice` 这一步在 Desktop 里**不注册**（代码里 `if (!('dshDesktop' in globalThis))`）`[DSH]`（`dsh-client-ui-settings-models/lib/client.js:4502`）。依赖它做首屏的产品，在 Desktop 上会少一段而没有任何报错。

## 4. 两个面真正共享的东西

| 共享 | 含义 |
|---|---|
| 同一份 `dsh-base` + `dsh-web-app` | 你的 bundle 只写一次，两面都能加载 |
| 同一个 Plugins 页 | 安装动作两句合一（[`REFERENCE`](./REFERENCE.md) §2） |
| 同一套 patch 方言 | profile / home / `--patch` 三层在两面语义一致 |
| 同一套 settings 命名空间 | 你的配置在两面同名同构 |
| 同一套首启账本 | 但 Desktop 会跳过 `welcome-notice` |

## 5. 两个面真正不同的东西

| 不同 | web | Desktop |
|---|---|---|
| profile 名 | `web` | `desktop` |
| 谁创建 profile | CLI（首次 `dsh plugin` 或出厂模板） | Electron 应用 |
| CLI 可否管理 | 可以 | 不可以（见 §2） |
| 第三方桌面壳可能另设 `DSH_HOME` | 不涉及 | 官方 App 与第三方壳行为不同，**各自记录**；第三方壳若自带 `DSH_HOME`，`--profile web` 更不可能命中 `[CARD]` |

## 6. 给产品作者的三条判据

1. **你的安装说明是否只需要一句？** 若必须分两段，说明你写的是 CLI，不是应用内装。
2. **你的首屏是否依赖 `welcome-notice`？** 依赖就必须给 Desktop 留替代路径。
3. **你有没有在任何地方假设 profile 名？** 一旦假设 `web`，Desktop 上就是错的。

## 7. 开放问题

- `[OPEN]` Desktop 实机行为（尤其应用内装的 `restart-required` 提示与 `profiles/desktop` 的目录结构）。复核条件：一台装过官方 Desktop 的机器，读出 `~/.dsh/profiles/desktop/package.json` 与 `cordis.patch.yml`。
- `[OPEN]` 官方 Desktop 是否固定 `DSH_HOME`（是否与 CLI 共用 `~/.dsh`）。复核条件：同上，看 `profiles/desktop` 落在哪个 home 下。
- `[OPEN]` 两面 `dsh.client` 的模块下发差异（`rev` 计算是否一致）。
