---
title: "源码复核：RAFOLIE/dsh-desktop-windowos 单文件桌面壳"
domain: reshape-product
kind: evidence
positioning: "固定复核 4.8 MiB 裸 exe 的真实打包形态、iframe 托管方式、进程归属与 blast radius、注册表/凭据写入面、更新与回滚，以及卡片版本与通道错位。"
read_when: "核对 shell/12_单文件桌面壳-windowos.md 的「单文件」「五跳候选链」「附加不动别人」「自愈熔断」「升级回滚」「三段式发布」与离线边界。"
status: observed
updated: 2026-11-01
---
# dsh-desktop-windowos 单文件桌面壳源码复核

> **固定快照**：只读一手仓库，不安装、不构建、不执行目标代码。`main` HEAD = tag [`v1.6.72`](https://github.com/RAFOLIE/dsh-desktop-windowos/releases/tag/v1.6.72) = [`5419e676622fccdf1983d1cfdf61625a3460a0ee`](https://github.com/RAFOLIE/dsh-desktop-windowos/commit/5419e676622fccdf1983d1cfdf61625a3460a0ee)（2026-10-15T17:27:44+08:00，`git describe` = `v1.6.72`，157 个提交，首提交 2026-08-14）；按 CHANGELOG 与发布说明它是**预发布版**，稳定 Latest 当时为 [`v1.6.69`](https://github.com/RAFOLIE/dsh-desktop-windowos/releases/tag/v1.6.69) = [`9fc2d5f2ef0ca5a97dcd8c4fd778f9bdecefccf5`](https://github.com/RAFOLIE/dsh-desktop-windowos/commit/9fc2d5f2ef0ca5a97dcd8c4fd778f9bdecefccf5)（2026-09-28）。卡片写的应用版本 `v1.6.63` 是更早的 tag [`4a86af566ed9f15760fba7c79cb60376a3158985`](https://github.com/RAFOLIE/dsh-desktop-windowos/commit/4a86af566ed9f15760fba7c79cb60376a3158985)（2026-09-14T21:51:50+08:00）。本文行号默认取 HEAD；凡结论依赖版本差异，另标 `v1.6.63`。
>
> **四个版本位在 HEAD 并不自洽**：根 `package.json`（插件半区）`1.5.13`、`plugin/package.json` `1.5.13`、`src-tauri/Cargo.toml` `1.6.72`、`src-tauri/tauri.conf.json` `1.6.72`；README 仍写「npm 现 1.5.12,应用现 v1.6.63」。本轮查到 npm registry 的 `latest` 确实是 **1.5.12**（发布于 2026-09-11），`1.5.13` **从未发布**——所以 README 的版本号与源码 manifest 互不对应，只能拿 tag 对齐。[根 manifest](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/package.json#L1-L5) [Cargo](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/Cargo.toml#L1-L5) [tauri.conf](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/tauri.conf.json#L1-L6) [README 版本行](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/README.md#L85-L85)
>
> **样本从不 pin DSH**：全仓没有 `@deepseek-ai/dsh` 依赖、没有版本常量，只有 0.1.2（BrowserAuth 分界）、0.1.7-alpha.1（settingsScope 分界）两处协议分界，以及「已验证连接」清单 `["0.1.6-alpha.2","0.1.7-alpha.2"]`。[分界](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src/backendUpdateModel.ts#L34-L37) 卡片里的「基线 DSH `0.2.1-rc.3`」是复核者本机 CLI，不是样本坐标；0.2.x 不在样本自报的验证矩阵里。
>
> **标记**：`[DOC]` 仓库文档/README/发布说明与 manifest；`[SRC-TARGET]` 目标固定提交源码；`[SRC-DSH]` DSH 上游包 `@deepseek-ai/dsh@0.2.1-rc.3`（本机安装）；`[TEST]` 测试源码/手工验收清单；`[CI]` workflow 登记——**本仓库没有 CI**；`[RUN]` 本轮只读网络与工件元数据核对，**未执行任何目标代码**。

## 对旧卡的校正

| 旧卡主张 | 固定树能证明什么 | 不能据此声称什么 |
|---|---|---|
| 「基线 DSH `0.2.1-rc.3`，README 自述兼容 0.1.6–0.1.7」 | `[SRC-TARGET]` 样本不 pin DSH；兼容性靠运行时协议探测 + 手工连接矩阵，矩阵只列 `0.1.6-alpha.2`/`0.1.7-alpha.2` 两个 alpha 版本。[矩阵](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/docs/backend-compatibility.md#L1-L12) | 不能把 0.2.1-rc.3 记成样本基线，也不能说样本对 0.2.x 做过「兼容验证」；0.2.x 只落在探测梯子的「活着」判定里。 |
| 「应用 v1.6.63 / npm 1.5.12，两条独立版本线」 | `[SRC-TARGET]` 该组合在 tag `v1.6.63` 成立；但 HEAD 的 manifest 是 1.6.72/1.5.13，npm 上 1.5.12 仍是 latest（1.5.13 未发布）。 | 不能把 v1.6.63 的版本号与 HEAD README 的机制描述当同一棵树：卡片里的 `remote.mux`/cookie/`api-session/status` 属于 v1.6.70+，`v1.6.63` 还在用无鉴权的 `events.host`（[v1.6.63 monitor](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/4a86af566ed9f15760fba7c79cb60376a3158985/src-tauri/src/monitor.rs#L18-L21)）。 |
| 「就绪判据 = `POST /api/host.describe` 返回 `result.ok === true`」 | `[SRC-TARGET]` 真实判据是**端点梯子**：`host.describe` 200+ok 才过；404 再试 `session/list`，200 + `server-response` 信封即算活着；401 也算活着（BrowserAuth 围栏）。[探测](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L736-L754) | 「ok===true」只在 ≤0.1.1 成立；0.1.2+ 已删 `host.describe`（本机 0.2.1-rc.3 全树无该字符串）。照抄成「ok true 才算就绪」会对新版永远判死。 |
| 「单文件 4.5 MB」 | `[SRC-TARGET]` `bundle.active: false`，`tauri build` 只出裸 exe，不出安装器；`[RUN]` Releases 只挂 `.exe` + `.exe.sha256`，v1.6.69 为 5,078,016 B（4.84 MiB / 5.08 MB）。[bundle](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/tauri.conf.json#L18-L24) | 「4.5 MB」是低估（本轮抽样的 v1.6.52–v1.6.72 都没低于 5.04 MB）；「单文件」只指**壳**，Node、DSH、WebView2 都不在文件里。 |
| 「不打包运行时，只接管窗口与生命周期」 | `[SRC-TARGET]` 属实：窗口加载的是 `WebviewUrl::App("index.html")`，页面里用 iframe 打开 `http://127.0.0.1:3080/`；DSH 是外部 `dsh web` 进程，不是内嵌服务器。[窗口](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/lib.rs#L682-L700) [iframe](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src/App.tsx#L42-L44) [挂载](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src/App.tsx#L329-L329) | 不能把「零前置」写成这家的属性——正好相反：它把 Node/DSH 前置显式留给用户，并用候选链去**发现**它们。 |
| 「附加后退出不动别人的进程」 | `[SRC-TARGET]` 只对**退出**成立：`teardown` 只杀自己记录的 pid 树（`taskkill /T /F`），附加态是 no-op。 | 「重启」路径不是：托盘「重启后端」「前后端重启」和自我更新后的重启都走 `stop_backend` → `kill_port_listeners`，会 `taskkill /T /F` **任何**监听 3080 的进程（含附加实例与无关程序）。[stop_backend](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L1975-L2028) |
| 「连续快速崩溃熔断」 | `[SRC-TARGET]` 触发条件精确为「存活 <30s」的连续 3 次（进程内全局计数），第 3 次后停止自愈并报错；没有冷却期、没有退避，也没有重启次数的时间衰减。[熔断](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L1760-L1774) | 不能称「熔断=有冷却」：存活 ≥30s 的进程一退出就把计数清零，慢性崩溃（每 31s 死一次）会无限重拉。 |
| 「升级前记版本 → 失败给一键回滚」 | `[SRC-TARGET]` 只对**内核 npm 全局安装**成立：升级前写 `%USERPROFILE%\.dsh\.previous_dsh_version`，回滚执行 `npm install -g @deepseek-ai/dsh@<ver>`。[保存](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/backend_update.rs#L343-L343) [回滚](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L2571-L2586) | 不是通用回滚：①壳自身没有回滚；②回滚命令丢掉了升级时的 `--prefix`，自定义全局前缀会装回默认前缀；③回滚后不回读版本；④错误页按钮无条件显示，没有保存版本时点了只会得到「没有保存的回滚版本」；后台失败只写日志，前端 `.catch(()=>{})` 连即时错误也不提示。 |
| 「settings.yaml 备份+修复+round-trip 校验」 | `[SRC-TARGET]` 属实但范围窄：只看 `%USERPROFILE%\.dsh\settings.yaml`（无视 `DSH_HOME`/profile），每次进程只尝试一次，备份固定覆盖 `.yaml.dshbak`，只修「冒号后缺空格」，修完必须整文件 YAML 可解析才写回。[自修复](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L1262-L1310) | 不能称「配置写坏都能自愈」；改坏成结构性 YAML 错误时只保留备份并报错，不修。 |
| 「通知靠 webchat 登录态 cookie」 | `[SRC-TARGET]` cookie 来自**壳自己**用启动 token 换的浏览器会话 cookie（`GET /?token=` → 303 Set-Cookie），并与登录态无关；无 token 时才回退 `~/.dsh/.credentials.yaml` 的持久 token。[兑换](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L2466-L2530) | 依赖条件要改写：自拉起的 BrowserAuth 后端（stdout 有 token）或 credentials.yaml 有可解析 token；**附加**一个无 token 的新版后端时通知会静默停摆。 |
| 「主窗口隐藏才弹通知」 | `[SRC-TARGET]` 抑制条件是 `visible && !minimized && focused`，即**隐藏、最小化、失焦都会弹**。[抑制](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/monitor.rs#L307-L318) | 不是「只在隐藏时」；后台但可见也会打扰。 |
| 「三段式发布是产品功能」 | `[SRC-TARGET]` 稳定通道就是 GitHub `releases/latest`，预发布排除由 GitHub 语义完成，代码没有额外闸门；`[RUN]` 核对当天 latest 指向 v1.6.69，而 HEAD 的 tag v1.6.72 是预发布。[通道](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/update.rs#L337-L362) | 「转正」是作者在 GitHub 上的手工动作，没有 CI 规则、没有观察期校验；且 v1.6.72 的资产改名后自动更新**解析不到**，转正即断更新。 |

## [DOC] 作者声明

- `[DOC]` 「交付物是**单个免安装裸 exe**（约 4.5 MB）」；「窗口内嵌原生 webchat（常驻壳）」；「关闭窗口(X)只是隐藏到托盘」；「单文件、无安装器、无 DLL 依赖，数据/日志写在 `%LOCALAPPDATA%\dsh-desktop\`」。[README](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/README.md#L14-L16) [托盘](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/README.md#L37-L37) [便携](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/README.md#L60-L60)
- `[DOC]` 三段式发布：开发期一律预发布（「自动更新不触碰（latest 天然排除）」），检查版仍预发布，「仅当作者确认稳定使用后才转正」；稳定/预发布两通道可在更新中心切换。[README](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/README.md#L21-L35)
- `[DOC]` 候选链与窗口：`DSH_CMD` → 自定义路径 → PATH 全局 `dsh web` → 本地 `node_modules\.bin\dsh.cmd` → 已确认的 npx；已安装候选 120s、npx 300s；「不会静默下载任何东西」。[README](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/README.md#L37-L39) [快速开始](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/README.md#L87-L99)
- `[DOC]` 前置：目标机必须有 Node `^22.19` 或 `>=24`；DSH 可选；WebView2「Windows 11 自带」。[README](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/README.md#L63-L73)
- `[DOC]` 自述机制：`host.describe` 就绪探测、`api/remote.mux` 的 `$events` + `api-session/status` `running` true→false 边沿、AUMID 注册（`HKCU\Software\Classes\AppUserModelId\com.dsh.desktop`）。[工作原理](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/README.md#L106-L112)
- `[DOC]` 自述回滚：「dsh 后端升级前自动保存当前版本号；升级后如果启动失败，错误界面提供「回滚之前版本」按钮」「回滚过程后台执行不卡界面」。[README](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/README.md#L55-L55)
- `[DOC]` 构建方式只有一句手工命令：`pnpm tauri build` → `src-tauri\target\release\dsh-desktop-windowos.exe`，并要求「重建前先退出正在运行的应用」。[README](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/README.md#L97-L106)
- `[DOC]` 发布说明把 v1.6.72 标为「预发布版」、稳定 Latest 保持 v1.6.69，并要求「下载 exe，退出旧桌面后替换并重开」；npm 插件不改。[v1.6.72 说明](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/docs/releases/v1.6.72.md#L1-L14) [CHANGELOG](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/CHANGELOG.md#L1-L8)
- `[DOC]` 插件半区自述与桌面**版本线解耦**：「仓库 manifest 现 1.5.13，本版仅新增 DSH Store 兼容矩阵声明、未发 npm；npm 仍为 1.5.12」。[plugin/README](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/plugin/README.md#L3-L3)

## [SRC-TARGET] 机制复核

### 1. 「单文件桌面壳」到底是什么

`[SRC-TARGET]` 它是**一个 Tauri v2 的 Windows 可执行文件**，不是「一个可执行文件里带 Web 运行时 + 服务器」：

1. **壳的前端资产嵌进 exe**：`frontendDist: "../dist"`，窗口用 `WebviewUrl::App("index.html")` 从 Tauri 自定义协议加载；React 常驻壳（标题栏/启动页/设置面板）没有 CDN、没有远程字体，`withGlobalTauri: true`、`csp: null`。[tauri.conf](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/tauri.conf.json#L7-L17) [窗口](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/lib.rs#L682-L686)
2. **不产出安装器**：`bundle.active: false`，所以 `tauri build` 只编译二进制，Release 里也只挂 exe 与其 `.sha256`——这正是「裸 exe」的实现来源。[bundle](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/tauri.conf.json#L18-L24)
3. **发布构建依赖一个隐式 feature**：Cargo 里自定义 `custom-protocol = ["tauri/custom-protocol"]` 并注释说明「直接 `cargo build --release` 会回退 devUrl」；即裸 `cargo build` 出来的产物不是发布形态，必须由 `tauri build` 注入该 feature。[Cargo](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/Cargo.toml#L14-L22)
4. **体积按「体积优先」profile 换来的**：`opt-level="s"`、`lto=true`、`codegen-units=1`、`panic="abort"`、`strip=true`。[Cargo](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/Cargo.toml#L61-L67)
5. **没有构建可复现性证据**：仓库无 `.github/`、无构建脚本、无 lock 之外的产物清单；README 只有手工命令。`[RUN]` 只能核到 GitHub 上挂的成品（见「[RUN]」）。

`[SRC-TARGET]` 因此「单文件」的准确含义是：**窗口 + 壳 UI + 全部 Rust 逻辑打成 1 个 exe；运行时（WebView2）、Node、DSH 三件都不在里面**。它不是「自带一切的单文件应用」，而是「无需安装器的单文件**外壳**」。

`[SRC-TARGET]` 「无 DLL 依赖」在树里找不到支撑：没有 `.cargo/config.toml`、没有 `crt-static` 设置，release profile 也不动链接方式；MSVC 默认动态 CRT 下产物通常仍依赖 VC 运行时 DLL。本轮未能完成 PE 导入表核对（见「[RUN]」与「未核实与下一步」），所以这条只能保留为作者声明。

### 2. 它怎么托管 DSH：远程 URL + iframe，不是内嵌服务器

`[SRC-TARGET]` 宿主关系是「壳页面（`tauri.localhost`）里嵌一个跨源 iframe（`http://127.0.0.1:3080/`）」，DSH 是**外部进程**：

- 窗口 URL 是壳自己的 `index.html`；webchat 由 `<iframe src="http://127.0.0.1:3080/">` 承载，首次 ready 后挂载并常驻，重启只换 key 重新加载。[窗口](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/lib.rs#L682-L700) [iframe 常量](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src/App.tsx#L42-L44) [挂载](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src/App.tsx#L329-L329) [重载 key](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src/App.tsx#L73-L96)
- 后端只有两种来源：**附加**（探测到 3080 上已有 DSH 就 `emit_ready(attached=true)`，不 spawn）或**拉起**（候选链里按顺序 `cmd /S /C` 启动一个 `dsh web`，`CREATE_NO_WINDOW`，cwd 固定 `%USERPROFILE%\.dsh` 或 `DSH_CWD`）。[附加](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L838-L847) [cwd/候选](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L95-L170) [spawn](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L2053-L2085)
- 就绪不是「进程起来了」：`rpc_probe` 带 `Origin` 与 `client-request` 信封打 `/api/<endpoint>`，3s 超时；`probe_ready_once` 先 `host.describe`（200+`result.ok`），404 再 `session/list`（200 + `type=server-response` 信封），401 视为活着。每秒一次直到候选窗口到期。[探测](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L682-L754) [轮询](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L886-L905)
- 跨源鉴权是**壳代做**的：先 `GET /`，200 → 明文 URL（pre-0.1.2）；401 → 抓子进程 stdout 的 `dsh web: http://127.0.0.1:3080/?token=`，用 Rust 换 `?token=`（期望 303 + `Set-Cookie: dsh-auth-…`），再把同一 cookie 以 `SameSite=None; Secure` 写进 WebView2 jar，最后 iframe 仍加载明文 URL；失败则退回 `~/.dsh/.credentials.yaml` 的持久 token 或给 `webchat-auth-hint`。[auth flow](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L2466-L2530) [plant](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L2376-L2464) [token 抓取](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L1081-L1113)
- 前端对这次兑换设了 **12 秒兜底**：超时/异常一律退回明文 URL，绝不把 iframe 扣在 401 上。[race cap](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src/App.tsx#L118-L126)

`[SRC-TARGET]` 结论：**这不是「内嵌服务器」，而是「iframe 一个本机 HTTP 服务 + 一个由壳托管的进程生命周期」**。壳崩溃/退出时 DSH 可能继续活着（附加态必然如此；自拉起态取决于退出路径），反过来 DSH 死了界面只是一个 401/连接失败的 iframe。

### 3. 进程与窗口生命周期

- `[SRC-TARGET]` **单实例**：`tauri-plugin-single-instance` 最先注册；二次启动只 `show_main_window`（带 `--open-web` 时走浏览器登录入口）。[单实例](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/lib.rs#L658-L663)
- `[SRC-TARGET]` **窗口先隐藏后显示**：`visible(false)` + `decorations(false)` 创建；壳页面 `shell-ready` 或 5s 兜底后 `show()`，保证前端坏了也不会留一个看不见的进程。[创建](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/lib.rs#L682-L700) [兜底](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/lib.rs#L793-L799) [reveal](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/lib.rs#L20-L33)
- `[SRC-TARGET]` **X 的行为可配**：`CloseRequested` 一律 `prevent_close`，默认 `hide()`；设置成 `exit` 时走 `quit_dsh`（teardown + `app.exit(0)`）。托盘 `quit` 永远退出。[关闭](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/lib.rs#L872-L886) [设置](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L305-L318)
- `[SRC-TARGET]` **三态所有权只覆盖「谁拉起」**：`DshState.inner` 只存自己 spawn 的 pid；`teardown` 只对它有动作（`taskkill /PID <pid> /T /F`）；附加态 `inner=None`，退出是 no-op。[状态](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L52-L75) [teardown](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L2030-L2041) [kill_tree](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L2162-L2168)
- `[SRC-TARGET]` **blast radius 比卡片大**：`stop_backend` = teardown + `kill_port_listeners`；后者解析 `netstat -ano -p tcp`，对**所有**本地地址以 `:3080` 结尾且 pid≠0 的行执行 `kill_tree`。调用方有三处：托盘「重启后端」、托盘「前后端重启」/自我更新后的重启、崩溃自愈。[kill_port](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L2005-L2028) [restart](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L1980-L2003) [restart_app](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/update.rs#L247-L264) [自愈调用](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L1776-L1790)
- `[SRC-TARGET]` **监护器只管自己拉起的 child**：独立线程每 500ms `try_wait`，退出且非「故意停止」才自愈；先 2.5s 等 dshmarket 的替身落地，再清端口、最多等 10s、重跑整条候选链。附加的后端没有任何守护；壳自身与 WebView 进程也没有看门狗。[supervise](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L1738-L1790)

### 4. 文件系统范围、注册表与权限面

`[SRC-TARGET]` 壳**没有** `fs:*`/`shell:*`/`http:*` 插件权限，主窗 capability 只有 core + 窗口拖拽/最小化/最大化/关闭；文件与进程操作全部在 Rust 侧手写。[capability](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/capabilities/default.json#L1-L15)

写入面（全部用户级、无提权）：

| 目标 | 内容 | 依据 |
|---|---|---|
| `%LOCALAPPDATA%\dsh-desktop\` | `dsh.log`（每次启动轮转，保留 20 份）、`settings.json`、`webauth-session.cookie`、`webauth-cookie.marker` | [log_path](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L2153-L2160) [rotate](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L2090-L2130) [cookie 落盘](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L1025-L1058) |
| `%USERPROFILE%\.dsh\` | `.previous_dsh_version`；`settings.yaml` 及其 `.yaml.dshbak` | [版本标记](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L2589-L2605) [自修复](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L1262-L1290) |
| 桌面 | `DeepSeek Harness Web.url` 迁移到 `dsh-desktop-web://open`，并有 3s 轮询的「修复」线程 | [repair](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/web_shortcut.rs#L92-L115) |
| `%USERPROFILE%\Downloads` | iframe 内触发的下载统一落此，重名加 ` (n)` | [download_target](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/lib.rs#L517-L556) |
| 自身 exe 与 `%TEMP%` | 自我更新：下载到 temp → `rename` 旧 exe 为 `.exe.old` → 覆盖 → 3s 后重启 | [swap](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/update.rs#L428-L472) |
| WebView2 用户数据目录 | 通过 COM `ICoreWebView2CookieManager` 写入 `dsh-auth-*` cookie | [plant](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L2376-L2464) |

`[SRC-TARGET]` 注册表写入三处 + 一个 URI 协议：

1. `HKCU\Software\Classes\AppUserModelId\com.dsh.desktop`（`DisplayName`/`IconUri`）——裸 exe 的 Toast 身份。[AUMID](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/lib.rs#L594-L620)
2. `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` 的 `DeepSeek Harness`——开机自启（开关即时增删）。[autostart](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L613-L652)
3. `HKCU\Control Panel\NotifyIconSettings\*` 的 `IsPromoted=1`——把托盘图标钉出溢出区。[tray](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/lib.rs#L631-L652)
4. `HKCU\Software\Classes\dsh-desktop-web`：注册 `dsh-desktop-web://` 处理器，命令固定为 `"<exe>" --open-web`，**故意不带 `%1`**，因此网页无法借协议传路径/参数/凭据。[协议](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/web_shortcut.rs#L68-L92)

`[SRC-TARGET]` **凭据面**：`dsh-auth-*` 会话 cookie 会明文写到 `%LOCALAPPDATA%\dsh-desktop\webauth-session.cookie`（`name=value` + 过期时间戳），代码注释自认与 `~/.dsh/.credentials.yaml` 同一信任域；没有 DPAPI/凭据管理器封装，也没有文件 ACL 收紧。[落盘](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L1025-L1058) [信任域注释](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L1012-L1023)

`[SRC-TARGET]` **iframe 侧不授予通用 IPC**：远程页只拿到两个「按 origin/父窗校验」的桥——目录选择器走 `postMessage` 给壳，由壳调 `pick_workspace_directory`；链接右键菜单只用 `window.open` 交给 `on_new_window`（系统浏览器）。capability 里也没有 `remote.urls` 项。[bridge](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/directory-picker.js#L1-L23) [前端桥](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src/directoryPickerBridge.ts#L1-L26) [菜单脚本](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/menu.rs#L1-L16)
`[OPEN]` `withGlobalTauri: true` + `csp: null` 下，远程 iframe 里的脚本能否直接触达 `__TAURI_INTERNALS__`、以及 Tauri v2 对无 `remote` capability 的来源是否一律拒绝，本轮未运行验证；只能说该仓库**没有主动开放**远程 IPC。

### 5. 更新与回滚

`[SRC-TARGET]` **壳自更新**（README 的「检查应用更新」）：

- 目录来自 GitHub API：稳定通道只取 `releases/latest`（预发布天然被 GitHub 排除），尝鲜通道取 `releases?per_page=10` 的第一条非 draft。[通道](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/update.rs#L337-L362)
- 资产必须匹配 `dsh-desktop-windowos-v<数字.数字.数字>.exe`；不匹配就报 `target release has no versioned exe asset` 并放弃。[解析](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/update.rs#L48-L59) [失败分支](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/update.rs#L366-L383)
- 下载链：直连 → 环境代理变量 → 探活的常见本机代理端口（7890/7891/7897/7898/10808/10809）→ **3 个硬编码公共镜像**（ghproxy/gh-proxy/ghfast）。[routes](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/update.rs#L61-L120)
- 完整性：**字节数必查；`sha256` 只在 API 提供 `digest` 时查**，没有 digest 就只靠大小；没有 Authenticode/签名公钥校验，也**没有使用**发布附带的 `.exe.sha256` 文件。[verify](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/update.rs#L189-L232)
- 安装：`rename` 旧 exe → 覆盖；覆盖失败会 `rename` 回来（防「无 exe」）；随后 3s 后由 detached helper 重启到新 exe，旧进程 `exit(0)`；`.old` 文件不清理。[swap](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/update.rs#L428-L472) [relaunch](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/update.rs#L266-L300)
- **壳没有回滚**：只有「升级」方向（`compare_versions(to,current) > 0` 才装），装坏后只能手动换回旧 exe；README 的「回滚之前版本」是内核的，不是壳的。

`[SRC-TARGET]` **内核更新**（更新中心）：

- 只对**可核验的托管安装**开口：`source.managed` 且 pid/path/version 与用户看到的快照一致；外部实例必须显式确认才允许停；降级要 `allow_downgrade`；先 `npm view` 确认 registry 有目标版本，再重新核验一次来源，才停进程。[门槛](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/backend_update.rs#L213-L238) [perform](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/backend_update.rs#L298-L345)
- 升级前 `save_previous_version`；装完必须验证「新 pid + 同 path + 目标版本 + 就绪」，否则报「安装完成但无法验证，可回滚」。[保存](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/backend_update.rs#L343-L343) [验证](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/backend_update.rs#L388-L392)
- 回滚命令 `npm install -g @deepseek-ai/dsh@<ver>` **不带 `--prefix`**，且 `run_bounded` 只看退出码、不回读版本；错误页按钮无条件出现，失败被前端 `catch(() => {})` 吞掉。[回滚](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L2571-L2586) [按钮](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src/App.tsx#L489-L503)
- 插件半区同步：npm `latest`（8s 超时）→ 只对**已安装**该插件的 profile 执行 `dsh plugin add … --config.minimumReleaseAge=0` → 回读 `node_modules/<pkg>/package.json` 验证，失败重试一次。[同步](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/update.rs#L580-L640)

`[SRC-TARGET]` **三段式的机制真相**：切通道=改 GitHub Release 的 prerelease/latest 标记，代码只消费结果；没有观察期、没有自动转正、没有「latest 回退保护」。预发布可被「尝鲜」通道安装（且 v1.6.72 因资产改名会直接失败）。

### 6. 服务或界面失败时的恢复

| 失败点 | 代码路径 | 用户可见结果 |
|---|---|---|
| 候选全部失败 | 逐个候选记录失败原因 → `error` 事件带全部失败摘要 | 启动页错误视图 + 重试/npx/回滚/日志 |
| 一个 DSH 都没有 | 空链 → `notfound` 事件 | 启动页给一键全局安装、npx、手填路径、重新检测、退出五个出口；不做静默下载。[notfound](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L838-L884) [面板](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src/App.tsx#L405-L475) |
| 候选提前退出且是 profile 写锁 | 识别 `timed out waiting for the writer lock at …`，**保留**锁文件并报占用者 pid | `Blocked`，提示等待或人工处理，不删锁。[锁](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L917-L931) [解析](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/startup_policy.rs#L167-L180) |
| 候选退出且缺 profile bundle | 从子进程输出识别缺失包 → 冷却期旁路 `pnpm add --save-exact … --config.minimumReleaseAge=0` → 同候选重试一次 | 成功则继续；失败给出手动命令 |
| `settings.yaml` 写坏 | 备份 → 只修冒号空格 → 整文件 YAML 解析通过才写回；解析不过则保留备份并报错 | 启动页错误 + 日志（一次性修复） |
| 自拉起后端运行中崩溃 | 监护线程 500ms 轮询 → 2.5s 等替身 → 清 3080 → 10s 等待 → 重跑候选链 | 自动恢复并刷新 iframe；3 次「存活<30s」后停止并报错 |
| 附加后端崩溃 | **无守护**；只有事件流 monitor 断线重连（指数退避 0.5→1→2→4→8s，指数封顶 4 次，代码另有 10s 上限），无 cookie 时 15s 静默轮询 | 界面停在 iframe 错误页；托盘「重启后端」是唯一出路 |
| 前端/iframe 鉴权失败 | 12s 兜底 + `webchat-auth-hint` → iframe 上方细条解释 | 仍显示 DSH 的 401 页，不白屏 |
| 壳页面崩溃/白屏 | 窗口 5s 兜底显示；`on_page_load` 重新广播状态；托盘「重新加载界面」只 reload 不重启后端（v1.6.72 新增） | 可自行恢复，但「重新加载」会丢未发送草稿 |
| Toast 失败 | `Toast::show()` 出错只写 `Warn`；AUMID 注册失败只 `eprintln!` | 通知静默不可用，界面无感 |
| 更新下载失败 | 多路由逐条失败 → `failed` 状态 + 日志；不阻断启动 | 顶部版本胶囊显示失败，可重试 |

`[SRC-TARGET]` **没有的恢复机制**：壳自身崩溃重启（单实例只保证不双开，没有 supervisor 拉起壳）、iframe 内 DSH 前端资源损坏的自检、`dsh.log` 之外的远程诊断上传、后端「树有效但启动即崩」的自动回退（自愈 3 次后停在错误页）。

## [SRC-DSH] 上游接缝（`@deepseek-ai/dsh@0.2.1-rc.3`，本机安装）

- `[SRC-DSH]` `remote.mux` 是真实端点：`@deepseek-ai/dsh-api-gateway` 的 `REMOTE_STREAM_MUX_PATH = "/api/remote.mux"`（`lib/index.js:133`）。壳监听 `ws://127.0.0.1:3080/api/remote.mux` 的 `$events` 逻辑流与这一代一致。[monitor](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/monitor.rs#L25-L30)
- `[SRC-DSH]` 会话 cookie 前缀 `dsh-auth-` 来自 `@deepseek-ai/dsh-client-connection`（`lib/index.js:277`，`COOKIE_PREFIX`）。壳按该前缀解析 `Set-Cookie` 并在本地校验值长度，属于对该实现的软耦合。
- `[SRC-DSH]` **`host.describe` 在 0.2.1-rc.3 已不存在**（对 `@deepseek-ai/*` 全树检索无命中），而 `session/list` 存在（`@deepseek-ai/dsh-api-session-controller/lib/typert.host.js`）。这解释了壳的端点梯子为什么必须保留 `session/list` 回退；也说明卡片把判据写成 `host.describe ok` 对当前上游是失效的。
- `[SRC-DSH]` `--no-open` 仍是 `dsh-web-app` 的合法选项：`lib/startup.js:24-25` 的 `webCommand()` 声明了 `--no-open`/`--port`。壳的**只读**能力探测正是解析 `dsh.cmd` → `@deepseek-ai/dsh/lib/bin.js` → `@deepseek-ai/dsh-web-app/lib/startup.js` 的文本后判定，不执行 CLI。[探测](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/startup_policy.rs#L25-L120)
- `[SRC-DSH]` `~/.dsh/.credentials.yaml` 的 `client-connection.browser-session` 是壳的回退 token 来源；壳只读该文件、拒绝可疑 `USERPROFILE`。[读取](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L2250-L2277)
- **边界**：以上只证明 0.2.1-rc.3 存在这些端点/字段，不证明壳与 0.2.x 端到端可用；样本自己的验证矩阵停在 `0.1.6-alpha.2`/`0.1.7-alpha.2`。

## [TEST]

- `[TEST]` 前端模型测试：`node --test` + TS strip，覆盖外观模型与后端更新模型（版本比较、阶段 busy、命令构造）。[脚本](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/package.json#L44-L50) [外观](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/tests/appearance-model.test.mjs#L1-L10) [更新模型](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/tests/backend-update-model.test.mjs#L1-L12)
- `[TEST]` UI 测试是**注入假 `__TAURI_INTERNALS__` 的 Playwright + msedge** 脚本（启动页、boot 对账、外观、托盘设置、标题栏、目录选择器、链接只开一次），需要本机 Vite 1420 或页面夹具，且多数未挂进 `package.json` scripts。[启动页](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/tests/startup-ui.cjs#L1-L25) [boot 对账](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/tests/boot-reconcile-ui.cjs#L1-L20)
- `[TEST]` 真实后端连接矩阵是**opt-in**：需要 `DSH_COMPAT_INSTALLS`（两个精确版本的包目录）、`DSH_COMPAT_TEST_BIN`（编译出的 Rust 测试程序）、可选 `PLAYWRIGHT_MODULE`；每次用临时 `DSH_HOME` 与随机端口，脚本只结束自己启动的进程。[脚本](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/tests/backend-compatibility.cjs#L1-L15) [重跑说明](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/docs/backend-compatibility.md#L33-L45)
- `[TEST]` Rust 单测共 **48** 个 `#[test]`：dsh.rs 17、monitor.rs 10、startup_policy.rs 6、backend_update.rs 5、window_geometry 3、npm_operation 3、web_shortcut 2、lib.rs 2；其中 **5 个 `#[ignore]`**（假 CLI、真实后端矩阵入口、需要隔离窗口的原生窗口用例、只读能力探测/宿主检查），默认 `cargo test` 只跑 43 个。[统计来自各文件 `#[test]`]（逐文件：[dsh](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/dsh.rs#L2543-L2695) [startup_policy](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/startup_policy.rs#L182-L326) [backend_update](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/backend_update.rs#L395-L457)）
- `[TEST]` **更新器零单测**：`src-tauri/src/update.rs` 没有 `#[test]`（0 个），资产名解析、摘要校验、rename-aside 换装、relaunch helper 全部只靠人眼/手测；后端更新的「是否算成功」倒是有 5 个单测（含「安装+重启≠完成」）。
- `[TEST]` 托盘烟雾测试是 PowerShell 脚本 `tests/tray-native-smoke.ps1` + `native-smoke` feature，不在自动流程内。
- `[TEST]` 其余 `docs/*-checks.md` 是**手工验收清单**（启动、更新、托盘、外观、issue 13/18/19/20/21），记录的是作者当次手测范围，不是可重跑断言。测试源码只证明覆盖意图；本轮**未运行任何测试**。

## [CI]

- `[CI]` **没有 CI**：仓库无 `.github/` 目录，`git ls-files` 中没有任何 workflow；README、CHANGELOG、`docs/` 也从未提 CI。发布是作者在 Windows 上手工 `pnpm tauri build` 后上传 exe + `.sha256`。
- `[CI]` 因此不存在「该 commit 已通过测试/构建」的证明，也没有构建环境、工具链、feature 组合（见 `custom-protocol`）的可审计记录；npm 包的 1.5.13 同样只存在于仓库、未发布。
- `[CI]` 结论边界：**workflow 不存在**，谈不上「CI 通过」；发布产物的可信度目前只来自作者的机器与 GitHub Release 页面。

## [RUN]

**范围**：本轮**没有**安装、构建、启动目标应用，也没有执行任何目标代码或测试；只做了只读的发布/registry 查询与 HTTP 元数据读取。以下事实仅证明「2026-11-01 这些 URL 返回了什么」。

- `[RUN]` `https://github.com/RAFOLIE/dsh-desktop-windowos/releases/latest` 302 到 `releases/tag/v1.6.69`——稳定通道当时确实是 v1.6.69，与 HEAD（v1.6.72 预发布）分离。
- `[RUN]` Releases 资产清单：v1.6.63/v1.6.65/v1.6.69/v1.6.70/v1.6.71 均为 `dsh-desktop-windowos-v<ver>.exe` + 同名 `.exe.sha256`；**v1.6.72 改名为 `dsh-desktop-windowos.exe`**（无版本段）+ `.exe.sha256`，无 msi/nsis/zip 等其他资产。
- `[RUN]` 资产字节数（HTTP `Content-Length`）：v1.6.63 = 5,061,120；v1.6.65 = 5,067,776；v1.6.69 = 5,078,016；v1.6.71 = 5,106,176；v1.6.72 = 5,108,736。即 4.83–4.87 MiB（5.06–5.11 MB），不是 4.5 MB。
- `[RUN]` 发布的 `.exe.sha256` 内容：v1.6.69 = `9d6abe4d37ff843cdd13ab8f963abd84c44c6707fcd5a793da82aa740bb10760`；v1.6.72 = `ed21cc39afe3604d5823d1d6400354003c5374e11ff11787c15e2db2ef387531`。**壳的更新器不读这个文件**（只读 API `digest`）。
- `[RUN]` npm registry：`dsh-desktop-plugin` 的 `dist-tags.latest = 1.5.12`（`time.latest = 2026-09-11T01:24:29Z`），版本列表中**没有 1.5.13**。
- `[RUN]` 试图下载 v1.6.69 exe 做 PE 导入/签名核对，两次均被本机到 GitHub CDN 的网络截断（只拿到部分字节），**已放弃**；因此「无 DLL 依赖」「未签名」「PE 元数据」均未核实，二进制未执行。
- `[RUN]` GitHub REST API 触发未认证限流（403），未能复核 ★/forks/issues 与资产 `digest` 字段；卡片的 ★26、下载量数字保持旧快照口径。

## 未核实与下一步

- `[OPEN]` **v1.6.72 资产改名是 bug 还是有意**：`parse_asset_version` 只认带版本段的名字，`run_check` 会以 `target release has no versioned exe asset` 失败；插件的 `ensureUpdated` 则因 `asset.version === ''` 静默跳过。若作者把 v1.6.72 转正，稳定通道用户将永远收不到它。需对照作者后续提交或 issue。
- `[OPEN]` 发布资产是否带 GitHub API `digest`：限流未查到；若没有，更新器只校验大小，公共镜像路由（ghproxy 等）的投毒门槛就是「同大小」。
- `[OPEN]` 壳的 Authenticode 签名状态与 PE 导入表（VC 运行时 DLL、WebView2Loader）：未下载完整二进制、未用 `signtool`/`dumpbin` 核对。
- `[OPEN]` 远程 iframe 是否能绕过 capability 调 IPC（`withGlobalTauri` + `csp: null` + 无 `remote` 条目）：需在 Windows 上实机验证，不能从配置推定。
- `[OPEN]` `kill_port_listeners` 在「3080 被无关程序占用」时误杀的影响面：代码会 `taskkill /T /F` 该 pid 树，未实测；同理，附加模式下点「前后端重启」会杀掉用户自己的 DSH。
- `[OPEN]` 回滚在自定义 npm 前缀（`--prefix`）安装下的行为：升级用了 `--prefix`，回滚没用，预计装到默认前缀；未实机验证。
- `[OPEN]` `settings.yaml` 自修复在 `DSH_HOME` 非默认时的目标错位：代码只读 `%USERPROFILE%\.dsh`，未实测。
- `[OPEN]` 0.2.x 兼容：壳的探测梯子能认出 0.2.1-rc.3，但 cookie 兑换/`$events` 帧格式/`session/list` 参数是否全兼容未验证；样本自报矩阵没有 0.2.x。
- `[OPEN]` 仓库把 `.mimosa/hook-state/*.json`（AI 会话钩子状态）提交进了版本库，而 `.gitignore` 又忽略 `.mimosa/`；属仓库卫生问题，未影响机制结论。

## 对卡片的净结论

1. **「单文件」成立，但要限定为「单文件外壳」**：`bundle.active: false` + 内嵌前端 + 体积优先 profile，Release 只有 1 个 exe（+ 校验文件）。Node、DSH、WebView2 都不在文件里；「约 4.5 MB」应改为「约 4.8–4.9 MiB / 5.1 MB」，且**没有 CI/构建脚本**证明发布 exe 与 tag 同源。
2. **它不是「内嵌服务器」**：窗口是壳页面，DSH 是外部 `dsh web`，界面靠跨源 iframe；跨源鉴权由壳用启动 token 换 cookie 再注入 WebView2。卡片 §2「常驻 webchat 窗口」容易被读成内嵌运行时，应写明这层 iframe + 本机 HTTP 的缝。
3. **版本坐标要重钉**：卡片写 v1.6.63/1.5.12，但机制描述（`remote.mux`、cookie、`api-session/status`）属于 v1.6.70+；HEAD 是 v1.6.72（预发布），稳定 Latest 是 v1.6.69；npm `latest` 仍是 1.5.12，仓库里的 1.5.13 从未发布。建议卡片改标「读于 HEAD v1.6.72 / 稳定 v1.6.69」，并把 v1.6.63 的旧 `events.host` 通知路径写成历史（[v1.6.63](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/4a86af566ed9f15760fba7c79cb60376a3158985/src-tauri/src/monitor.rs#L18-L21) vs [HEAD](https://github.com/RAFOLIE/dsh-desktop-windowos/blob/5419e676622fccdf1983d1cfdf61625a3460a0ee/src-tauri/src/monitor.rs#L25-L30)）。
4. **就绪判据要改写**：不是 `host.describe.ok === true`，而是端点梯子（`host.describe` → `session/list`，401 亦算活着）；这也是「照抄点」成立的前提，否则移植到 0.2.x 会永远判死。
5. **进程所有权只对「退出」成立**：`taskkill /T` 只杀自己拉起的树（真实），但「重启后端/前后端重启/自愈」都会清掉 3080 上的**任何**监听者，包括用户的附加实例与无关程序。卡片 §2.2 的三态表必须补一列「重启路径」。
6. **熔断是「3 次、存活<30s」的进程内计数**，没有冷却与退避；自愈也只覆盖自己拉起的 child，附加实例没有任何守护——卡片「监护自愈」的适用范围要收窄。
7. **回滚是内核专用的、且不完整**：只有 `%USERPROFILE%\.dsh\.previous_dsh_version` 一个标记、回滚命令丢 `--prefix`、不回读验证、按钮无条件显示、失败被吞；壳自身没有回滚。卡片「升级失败一键回滚」应降级为「内核 npm 全局安装的单点回滚，带上述缺口」。
8. **权限面不是「有 fs 权限」而是「Rust 侧全权 + 用户级写入」**：capability 很窄（无 fs/shell/http），但壳自己写 `%LOCALAPPDATA%`、`~/.dsh`、桌面 `.url`、HKCU 四处注册表与一个 URI 协议，并把 `dsh-auth-*` 会话 cookie 明文落盘——审计这一面比看 capability 更有意义。
9. **三段式发布是 GitHub 语义 + 人的纪律**：代码只读 `releases/latest`，没有任何自动转正/观察期；而 v1.6.72 的资产改名会让「转正」直接断掉自动更新。卡片的 `[OPEN]`「靠人维护」应当升级为**已知机制缺口**：发布纪律与资产命名必须一起维护。
10. **离线/前置边界**：壳 UI 与 DSH 页面都在本机，装了 Node+DSH 后可以离线启动；但每次启动都会在后台打 `api.github.com`（更新检查）；该检查成功且无新版时再打 `registry.npmjs.org` 取插件 latest（8s 超时）。两处失败都只记日志、不阻断启动；首次安装/一键全局安装/npx 兜底都必须联网。所以「单文件离线可用」只在「机器已具备 Node+DSH」这一前提下成立。
