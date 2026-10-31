---
title: "源码复核：hyperion2144/dsh-desktop-tauriapp 内置运行时"
domain: reshape-product
kind: evidence
positioning: "固定复核内置运行时的打包形态、进程归属、校验与回退边界；以一手源码校正 shell/13 卡片，不替代安装实测。"
read_when: "核对 shell/13_内置运行时-tauriapp.md 的零前置依赖、版本 pin、健康自愈、更新/回退与权限断言。"
status: observed
updated: 2026-11-01
---
# dsh-desktop-tauriapp 内置运行时源码复核

> **固定快照**：只读一手仓库，不安装、不构建、不运行目标代码。`main` HEAD 为 [`577a6d3ac95aeb956e7bb8134efb574294ea63d2`](https://github.com/hyperion2144/dsh-desktop-tauriapp/commit/577a6d3ac95aeb956e7bb8134efb574294ea63d2)（2026-10-10T21:33:02+08:00，`git describe` = `v0.12.0-4-g577a6d3`）；最近 tag [`v0.12.0`](https://github.com/hyperion2144/dsh-desktop-tauriapp/releases/tag/v0.12.0) = [`2c4ba10e29278184424ae56a1ec02d0f45de8ea3`](https://github.com/hyperion2144/dsh-desktop-tauriapp/commit/2c4ba10e29278184424ae56a1ec02d0f45de8ea3)（2026-10-05T14:49:27+08:00），相差 4 个提交。三个版本位（根 `package.json`、`desktop/src-tauri/tauri.conf.json`、`desktop/src-tauri/Cargo.toml`）均为 `0.12.0`；`desktop/package.json` 是内部工具包 `0.6.0`。本文所有行号取自 HEAD；tag 与本 HEAD 的运行时 pin 相同，但 `spawn` 路径有 4 处差异（新增 `DSH_CLIENT_VERSION` 注入与 `dsh` shim 重写），引用时按 HEAD。
>
> **内置运行时版本**：`BUILTIN_DSH_VERSION = "0.2.0-rc.2"`（HEAD 与 tag 一致），内置 pnpm 固定 `11.16.0`，Node sidecar 取 `latest-v24.x`（构建时浮动，非精确版本）。`resources/dsh/` 与 `binaries/` 在 `.gitignore` 内，因此仓库本身**不能证明安装包实际带的是哪棵树**；能读到的只有准备脚本的 pin 与 CI 调用。[准备脚本](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/scripts/prepare-builtin-runtime.mjs#L26-L33) [.gitignore](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/.gitignore#L9-L12)
>
> **标记**：`[DOC]` 仓库文档/README；`[SRC-TARGET]` 目标固定提交源码；`[SRC-DSH]` DSH 上游包 `@deepseek-ai/dsh@0.2.1-rc.3`（本机安装，非内置树）；`[TEST]` 测试源码；`[CI]` workflow 登记；`[RUN]` 实测——**本次没有 `[RUN]`**，未安装、未构建、未启动任何目标代码。

## 对旧卡的校正

| 旧卡主张 | 固定树能证明什么 | 不能据此声称什么 |
|---|---|---|
| 内置 Node 24 sidecar + dsh 依赖树随包分发 | `[SRC-TARGET]` 安装包资源映射 `resources/dsh/ → dsh/`，`externalBin: binaries/dsh-node`；运行期直接读资源目录，无解压步骤。[tauri.conf](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/tauri.conf.json#L62-L70) [builtin.rs](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin.rs#L80-L85) | 不能证明发布产物真的含这棵树，也不能证明 sidecar 的精确补丁版本——Node 只 pin 到 `latest-v24.x`。[脚本](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/scripts/prepare-builtin-runtime.mjs#L31-L31) |
| 基线 DSH `0.2.1-rc.3`，内置版本“由脚本 pin、README 未给号” | `[SRC-TARGET]` 脚本 pin 是 **`0.2.0-rc.2`**；本机 `@deepseek-ai/dsh` 才是 `0.2.1-rc.3`。二者不是同一棵树。 | 卡里引用的 `lib/bin.js:35-37`、`profile-boot-C14i-8IN.js:154` 属于本机 CLI 的 0.2.1-rc.3，**不属于安装包内置运行时**；不能把它们的行号/行为直接记到样本账上。 |
| 版本精确 pin，“本地与 CI 一致可复现” | `[SRC-TARGET]` 只有顶层版本 pin；`npm install --no-save` 不留 lock，transitive 依赖按 semver 在当时 registry 上重新解析；Node 取浮动 dist 索引。[脚本](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/scripts/prepare-builtin-runtime.mjs#L47-L67) [下载](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/scripts/prepare-builtin-runtime.mjs#L76-L95) | 不能声称“同一 commit 每次构建出同一棵依赖树”。可复现的只有 `@deepseek-ai/dsh@0.2.0-rc.2` 与 `pnpm@11.16.0` 两个直接坐标。 |
| 启动走内部 `runProfile` API，不经 CLI | `[SRC-TARGET]` launcher 定位 `lib/profile-boot*.js` 的 `runProfile`，传 `{environment, profile, fromDefaultProfile, patchFiles, args}`；`--init-from-default` 固定映射模板 `web`。[launcher](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin/launcher.mjs#L17-L74) | 这不是公开契约：依赖 `@deepseek-ai/dsh-app-boot` 根导出与 `profile-boot*.js` 的文件名/导出名，随 DSH 内部重构会断（有散列名回退，不等于契约保证）。 |
| 运行时源可配 GitHub / npm | `[SRC-TARGET]` 两者**只影响版本目录来源**；安装载荷统一 `pnpm add @deepseek-ai/dsh@<ver>`，注释明确 GitHub release 无 asset。[registry](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/registry.rs#L455-L486) | 不能声称“从 GitHub 下载运行时包并校验”；也没有任何应用级 hash/签名校验。 |
| 健康探测连接级；3 次封顶；健康 2 分钟才重置 | `[SRC-TARGET]` 单次 TCP 失败即请求重启；`epoch_failures` 累计 3 次后停自愈；24 个 5s tick（120s）连续健康才清零。[lib.rs](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/lib.rs#L564-L633) | 守护器只探测**主实例**端口或远程地址，不覆盖多开的次窗 profile；不是“每个 profile 的自愈器”。 |
| 其余 profile 端口散列分配并持久化 | `[SRC-TARGET]` 端口是确定式散列（FNV-1a % 512 + 3082）并做冲突避让；Rust 注释明确**不写** `settings.yaml`，分配只存在会话内存。[settings.rs](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/settings.rs#L290-L365) | “持久化”不准确：跨启动稳定靠散列的确定性；只有用户显式改端口才由 client→插件→settings 服务落盘。 |
| 零前置依赖：不需要外部 Node | `[SRC-TARGET]` 打包形态成立；但 `find_builtin_node` 的查找顺序是 `DSH_NODE_BIN` → 应用旁 sidecar → **PATH 上的 node**。[builtin.rs](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin.rs#L87-L118) | “无需外部 Node”是发布包属性，不是代码不变量；sidecar 缺失时内置树会静默跑在用户系统 node 上。 |
| 运行时下载 / 切换 / 卸载，含更新与回退 | `[SRC-TARGET]` 下载=用内置 node+pnpm 在 `app_data/runtimes/<ver>` 重建依赖树；切换写设置并重启；卸载 rename 进 `.trash`，下次启动清空。[registry](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/registry.rs#L29-L68) [commands](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/commands.rs#L951-L1005) | 没有自动回滚：树“结构有效但启动即崩”时，自愈 3 次后停手，设置仍指向同一坏版本；只有“树缺失/无效”才回退。 |
| 签名 / 更新 | `[SRC-TARGET]` macOS `signingIdentity: "-"`（ad-hoc）且无公证配置；无 `tauri-plugin-updater`、`tauri.conf` 无 updater 段。[tauri.conf](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/tauri.conf.json#L39-L49) [Cargo](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/Cargo.toml#L18-L37) | 应用没有自动更新通道；“更新”只有手动换安装包与手动换运行时两条，二者互不联动。 |

## [DOC] 作者声明

- `[DOC]` “内置运行时开箱即用（无需自己装 Node 和 dsh）”“Node sidecar + dsh 依赖树随安装包分发”“经内部 API 启动（不走 CLI）”“外部 dsh：`DSH_BIN` → PATH → npm 全局”“应用内下载/切换/卸载，目录源可配 github/npm”。[README](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/README.md#L6-L13) [运行时](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/README.md#L62-L65)
- `[DOC]` 发布链：提交 → 三处升版本 → tag → CI 双平台构建 → draft release。安装包体积“约 200 MB / 240 MB”。[构建](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/README.md#L39-L47) [体积](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/README.md#L152-L154)
- `[DOC]` 已知限制写明“macOS 非公证包需右键打开；Windows 网络下载的 exe 触发 SmartScreen”。[README](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/README.md#L150-L154)
- `[DOC]` CHANGELOG 自述内置运行时从 `0.1.7-rc.1` 升级到 `0.2.0-rc.2`，并称 `desktop` 名字在 0.2.0-rc.2 的 CLI 里同样被拦截（自报实测，非本次复核）。[CHANGELOG](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/CHANGELOG.md#L46-L46) [升级](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/CHANGELOG.md#L62-L63)

## [SRC-TARGET] 机制复核

### 1. “内置运行时”到底是什么

`[SRC-TARGET]` 它是**随安装包分发的三件套**，不是“首次运行下载”，也不是“解压后再跑”：

1. **dsh npm 安装树**：构建期 `npm install @deepseek-ai/dsh@0.2.0-rc.2 pnpm@11.16.0` 到暂存目录，把整个 `node_modules` 拷进 `resources/dsh/node_modules`；dsh 本体在 `node_modules/@deepseek-ai/dsh`，内置 pnpm 在 `node_modules/pnpm`。[准备](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/scripts/prepare-builtin-runtime.mjs#L47-L73) [布局](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin.rs#L1-L10)
2. **Node sidecar**：构建期从 `nodejs.org/dist/latest-v24.x/` 的正则匹配下载 `node-v*-<os>-<arch>.tar.gz|zip`，抽出 `bin/node` 或 `node.exe`，命名成 Tauri 要求的 `binaries/dsh-node-<triple>[.exe]`；运行期按“应用可执行文件旁 `dsh-node[.exe]`”定位。[下载](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/scripts/prepare-builtin-runtime.mjs#L76-L120) [定位](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin.rs#L87-L118)
3. **启动器与解析钩子**：两个 `.mjs` 以 `include_str!` 编译进 Rust，每次 spawn 前写到 `app_data/runtime/`（无 hash、直接覆盖）；启动器 `import` dsh 的 `runProfile`，参数固定 `["--no-open","--host","127.0.0.1","--port", port]`。[内嵌](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin.rs#L16-L19) [写出](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin.rs#L120-L134) [调用](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin/launcher.mjs#L67-L74)

`[SRC-TARGET]` 额外装了一层 **Node 模块解析钩子**：凡是内置 `node_modules` 里存在的裸说明符，一律解析到内置树，避免存量 profile 里的旧版 `@deepseek-ai/*` 副本遮蔽运行中的内置核心；profile 自有第三方依赖仍走默认链。[resolver-hooks](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin/resolver-hooks.mjs#L22-L39) [launcher](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin/launcher.mjs#L28-L40)

`[SRC-TARGET]` **首次运行**只做两件事：写 launcher/hooks、按默认 profile 初始化。全新安装（`settings.yaml` 不存在）默认 profile 是 `desktop`；目录落在 `$DSH_HOME/profiles/<name>`。[默认](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/settings.rs#L396-L419) [目录](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/profiles.rs#L17-L29) 首启**不下载运行时**；下载只由用户在设置页/托盘显式触发。

### 2. 进程归属：谁拉起、谁停、端口与健康

`[SRC-TARGET]` **一个 profile 一个 worker，worker 是进程句柄的唯一持有者**；全壳唯一 spawn 入口是 `DshWorker::spawn_now`，壳内其它模块不直接启停 dsh。启动采用 latest-wins：`begin_start` 递增 epoch、先杀旧进程、再在后台做端口清理与 spawn。[worker 契约](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/process/worker.rs#L1-L21) [stop](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/process/worker.rs#L107-L144) [start](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/process/worker.rs#L146-L207)

- `[SRC-TARGET]` **停**：worker 的 `child.kill()` + `wait()`；退出事件里主 worker 与所有次窗 worker 逐个 shutdown，并摘实例台账。次窗不可重启，只能关窗（关窗即销毁 worker）。[stop](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/process/worker.rs#L107-L124) [退出](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/lib.rs#L752-L773)
- `[SRC-TARGET]` **端口**：`web=3080`、`desktop=3081`，其余 `3082 + FNV-1a(name) % 512` 再向后避让；lane 端口 `web=3092`、`desktop=3093`、其余 `3094 + hash % 512`，3091 留给壳自有转发器。`DSH_DESKTOP_PORT` 可全局覆盖，显式 per-profile 覆盖优先。[公式](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/settings.rs#L290-L331) [取值](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/settings.rs#L333-L365) [显式改](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/commands.rs#L864-L885)
- `[SRC-TARGET]` **端口归属的爆炸半径**：启动/重启前调用 `stop_port_owner(port)`，它会枚举该端口的所有监听 PID，先温和终止、再强杀，直到端口释放。也就是说“重启”会杀掉**占用该端口的任何进程**，不限于自己拉起的 child；台账认领逻辑（Ours / ForeignWeb / ForeignUnknown）只约束“接入/复用”，不约束重启路径。[stop_port_owner](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/process/lifecycle.rs#L811-L845) [请求启动](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/process/worker.rs#L176-L188) [认领](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/instances.rs#L96-L129)
- `[SRC-TARGET]` **拉起**：`resolve_source` 两态（内置/外部）；内置优先“用户选中的已下载版本”，否则随包树；外部按 `DSH_BIN` → `PATH` → Homebrew/npm/nvm/npx 常见位置探测。spawn 时注入 lane/port、代理、`$DSH_HOME` 工作目录，stdout/stderr 逐行进日志与页面启动控制台，并登记实例台账（pid/port/lane/source）。[来源](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin.rs#L149-L217) [外部](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/process/lifecycle.rs#L136-L155) [spawn](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/process/lifecycle.rs#L653-L745)
- `[SRC-TARGET]` **健康**：5s 一跳；`probe_local` 以 2s 超时 TCP connect 成功为“健康”，HTTP 只写日志、绝不判死；远程地址只提示不重拉；复用外部实例（非本壳拉起）也只提示。本壳拉起的实例**首次失败即请求重启**，没有“连续 3 次才动手”的闸门；`epoch_failures` 是“自愈失败计数”，达到 3 后停止自愈并置状态“异常（已停止自愈，请手动重启）”；连续 24 个 tick（约 120s）健康才把计数清零。`.ready_once` 在启动时复位，保证守护器与启动流程不双重拉起。[探针](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/process/probing.rs#L11-L59) [守护器](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/lib.rs#L564-L633)
- `[SRC-TARGET]` **切换运行时=写设置+重启**：托盘点击已装版本保存 `dsh_runtime` 后 `restart_dsh`；“下载并切换”在下载成功后自动切；切到 external 时保留 `dsh_runtime` 以便切回。[切换](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/ui/tray.rs#L428-L454) [下载并切换](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/ui/tray.rs#L456-L480)

### 3. 资源校验、供应链与签名

- `[SRC-TARGET]` **Node 归档没有校验**：脚本按 dist 索引正则取 URL、`fetch` 后直接解压，未取 `SHASUMS256.txt`、未验签名。[下载与解压](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/scripts/prepare-builtin-runtime.mjs#L89-L112)
- `[SRC-TARGET]` **dsh 树没有构建锁**：暂存目录每次新建最小 `package.json`，`npm install --no-save` 安装固定版本；只把 `node_modules` 拷进资源目录，不拷 lock，也没有 `desktop-runtime.json` 之外的清单。安装脚本写出的 `desktop-runtime.json`（variant/dsh/node/staged_at）在运行期**没有被任何代码读取**（全树检索只命中写入点）。[安装](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/scripts/prepare-builtin-runtime.mjs#L56-L73)
- `[SRC-TARGET]` **运行期下载也没有应用级校验**：`download_and_install` 用内置 node 跑内置 pnpm，`pnpm add @deepseek-ai/dsh@<ver>`；完整性完全委托给 npm/pnpm 的 registry 元数据与缓存，应用不比对 hash，安装后只检查 `node_modules/@deepseek-ai/dsh/lib/bin.js` 是否存在。[安装](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/registry.rs#L314-L406) [有效性](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/registry.rs#L70-L78) [安装入口](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/registry.rs#L455-L512) 注：`Cargo.toml` 里的 `flate2`/`tar` 在 `src/` 中未找到使用点，与“统一走 pnpm、无 tarball 解包”的注释一致。
- `[SRC-TARGET]` **macOS 是 ad-hoc 签名**：`macOS.signingIdentity: "-"`，无公证配置；release workflow 无 Apple 证书/公证 secret。`Entitlements.plist` 为 sidecar 开了 JIT、未签名可执行内存、关闭库校验、允许 dyld 环境变量——注释说明这是 Node/V8 在 hardened runtime 下启动的必要条件，也意味着包内 `node_modules` 的原生模块不被逐个签名校验。[tauri.conf](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/tauri.conf.json#L45-L49) [entitlements](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/Entitlements.plist#L5-L18)
- `[SRC-TARGET]` **没有应用自动更新**：Cargo 依赖只有 log/notification/single-instance/window-state/dialog 等插件，没有 `tauri-plugin-updater`；`tauri.conf.json` 无 `plugins.updater`、无 pubkey/endpoints。`DISABLE_AUTO_UPDATE` 只出现在 macOS 注册环境的 shell 片段里，不是更新器。[Cargo](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/Cargo.toml#L18-L37) [tauri.conf](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/tauri.conf.json#L1-L72)

### 4. 运行时更新与应用更新 / 回退

- `[SRC-TARGET]` **应用更新**只有手动路径：从 Releases 下新安装包覆盖安装；应用内没有版本检查/下载/应用更新包的入口（全树无 updater 依赖与配置）。
- `[SRC-TARGET]` **运行时更新**：目录（GitHub releases 或 npm registry 版本表）→ 用户选版本 → pnpm 装到 `app_data/runtimes/<ver>` → 写 `installed.json` → 切换 `dsh_runtime` → 重启。安装是 single-flight（`DL_ACTIVE`），失败会 `discard_runtime_dir` 清掉半成品。[目录](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/registry.rs#L166-L253) [安装](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/registry.rs#L458-L502) [命令](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/commands.rs#L909-L1005)
- `[SRC-TARGET]` **卸载**：正在使用的版本与内置版本禁删；删除先 rename 到 `.trash`，下次启动、spawn 之前才真删（避免直接 unlink 改动与运行树共享 inode 的 ctime，触发插件 rebuilt/白屏）。[回收站](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/registry.rs#L44-L68) [删除保护](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/commands.rs#L983-L1005)
- `[SRC-TARGET]` **回退语义**只有三种：①选中版本树无效/缺失 → 静默改用随包树；②内置不可用 → 回退外部并通知；③外部不可用 → 回退随包树并通知。回退**只对本次运行生效，不改写设置**；没有“启动失败自动退回上一版”的逻辑，也没有对已安装树的健康快照/回滚点。[来源解析](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin.rs#L175-L217)
- `[SRC-TARGET]` 与版本相关的兼容补丁是**按设置值生成**的：`desktop_plugin_patch_path` 根据 `settings.dsh_runtime` 在两代 `connection.inject`（`webRuntime` vs `webStartup`，分界 0.2.1-alpha.2）之间选；未设置时按旧契约。若选中版本树失效而回退到随包 0.2.0-rc.2，补丁仍按设置里的新版本生成，存在契约错配风险（本次未运行验证）。[plugin.rs](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/process/plugin.rs#L82-L115)

### 5. 沙箱与权限

- `[SRC-TARGET]` **主窗/次窗** capability 只给 `core:default`、notification、dialog、window 拖拽与一组自定义命令；**没有** `shell:*`、`fs:*`、`http:*`、`process:*` 插件权限——进程与文件操作全部在 Rust 侧，WebView 不能直接执行 shell 或任意读写。[default.json](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/capabilities/default.json#L1-L83)
- `[SRC-TARGET]` **remote origin 是另一套更大的面**：因为 DSH 页面跑在 `http://127.0.0.1[:*]/localhost`（对 Tauri 属 remote），`remote-desktop.json` 对这个 origin 放行了约 80 个命令，包括 `restart-dsh-service`、`save-desktop-settings`、`set-dsh-source`、`download-runtime`/`remove-runtime`、`migrate-profile`、`browser-guest-*`、`open-external`、下载器全部命令。[remote-desktop.json](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/capabilities/remote-desktop.json#L1-L94)
- `[SRC-TARGET]` `tauri.conf.json` 设置 `withGlobalTauri: true`、`security.csp: null`；因此页面内任何能执行脚本的代码（含第三方插件 client）都能直接调用上述命令。capability 按**窗口/来源**授权，不区分“核心 UI”与“插件注入脚本”。[tauri.conf](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/tauri.conf.json#L9-L38)
- `[SRC-TARGET]` 子进程不被 OS 沙箱包裹：spawn 继承环境、代理与 `PATH`，cwd=`$DSH_HOME`；`DSH_MODE` 环境变量可越过设置强制 external。dsh 自身的 sandbox/permission 模型在本仓库之外，不能由壳的 capability 推断。[spawn](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/process/lifecycle.rs#L704-L745) [模式](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin.rs#L54-L64)
- `[SRC-TARGET]` macOS 包没有 App Sandbox entitlement（只有 hardened runtime 的 JIT/库校验豁免），Windows 侧无额外沙箱配置；这与“壳不限制 dsh 能力”的定位一致。[entitlements](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/Entitlements.plist#L1-L19)

### 6. sidecar 失败时的恢复

| 失败点 | 代码路径 | 用户可见结果 |
|---|---|---|
| `resources/dsh` 未打包/被删 | `try_bundled_builtin` 返回错误 → `resolve_source` 回退外部 dsh；外部也没有才 `Err`。[builtin.rs](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin.rs#L167-L217) | 通知“内置运行时不可用，已回退外部 dsh”；两者皆缺进错误页 |
| sidecar node 缺失 | 同上；外部模式还需系统 node，找不到就 `NotFound`。[lifecycle.rs](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/process/lifecycle.rs#L688-L693) | 提示安装 Node/设置 `DSH_NODE`（与外置路径共用） |
| 安装树存在但 `lib/bin.js` 缺失 | `is_valid_runtime` 为假 → 选中版本被跳过，静默用随包树。[registry.rs](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/registry.rs#L70-L78) | 无专门通知（用户只会发现版本“变回内置”） |
| spawn 失败 / 启动即退 | `show_error("spawn-failed"/"not-found"/"timeout")`，stderr 缓冲供错误页与日志。[worker.rs](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/process/worker.rs#L194-L200) | 错误页 + 启动控制台输出，可手动重启 |
| 运行中 crash（本壳拉起） | 首次探测失败即 `request_start`；`epoch_failures` 3 次封顶；120s 连续健康才清零。[lib.rs](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/lib.rs#L585-L633) | 前两次自动重启并通知次数，第三次后“已停止自愈，请手动重启” |
| 远程 / 复用外部实例不可达 | 只提示，不代拉；远程每 5 分钟一条通知。[lib.rs](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/lib.rs#L606-L621) | 状态“外部实例不可达（请手动重启）” |
| 运行时下载失败 | `install_via_pnpm` 捕获错误 → `discard_runtime_dir` 清半成品 → 错误经轮询状态返回。[registry.rs](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/registry.rs#L496-L502) | 设置页显示去噪后的 pnpm 错误尾部；无自动重试/续传 |

## [SRC-DSH] 上游接缝（`@deepseek-ai/dsh@0.2.1-rc.3`，非内置树）

- `[SRC-DSH]` CLI 在参数解析阶段硬拦 `desktop`：`if (profile.toLowerCase() === "desktop") program.error('error: profile "desktop" is managed exclusively by the Electron application')`。这解释了壳为什么绕过 CLI 直调内部 API。`@deepseek-ai/dsh@0.2.1-rc.3` `lib/bin.js:36`。
- `[SRC-DSH]` 稳定名 `lib/profile-boot.js` 只是再导出：`export { ..., runProfile } from "./profile-boot-C14i-8IN.js"`（`:1-2`）。launcher 的“稳定名优先、散列名回退”正是对这个布局的适配。[launcher](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin/launcher.mjs#L48-L65)
- `[SRC-DSH]` `initializeProfileFromDefault(name, template)` 只接受 `PROFILE_TEMPLATES` 的键，且目标名若命中出厂模板会拒绝；launcher 传 `fromDefaultProfile: "web"`，所以 `desktop` 能作为自定义 profile 建出来，但走的是 `web` 模板。[0.2.1-rc.3 `lib/profile-boot-C14i-8IN.js:146-154`]
- `[SRC-DSH]` `runProfile(options)` 读取 `options.environment`、`options.profile`、`options.patchFiles`、`options.fromDefaultProfile`；launcher 的调用形状与之一致，但这是内部函数，不是 CLI/公开 API 契约。[0.2.1-rc.3 `lib/profile-boot-C14i-8IN.js:255-272`]
- `[SRC-DSH]` `loadLayeredEnv` 由 `@deepseek-ai/dsh-app-boot` 根导出（0.2.1-rc.3 `lib/index.js:3736`、导出表 `:4566`），launcher 通过 `createRequire(<dsh_lib>/bin.js)` 解析到它。[launcher](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin/launcher.mjs#L43-L46)
- **重要边界**：以上是 0.2.1-rc.3 的契约；内置树是 0.2.0-rc.2，本次**没有**独立核对后者是否同样导出 `runProfile`/`loadLayeredEnv`，也没有核对 `fromDefaultProfile` 的行为。项目自述 0.2.0-rc.2 也有 `desktop` 拦截、launcher 已端到端跑通（CHANGELOG:46），属于 `[DOC]` 自报，不是本次复核结论。

## [TEST]

- `[TEST]` 单元测试覆盖启动参数形状、`--patch` 早于 `--no-open` 的顺序约束、`dsh_lib` 布局解析、worker 生命周期、端口认领判定、pnpm 进度/错误尾部归一、`pnpm-workspace.yaml` 的 pnpm 11 关键项、node 垫片、运行树有效性。[builtin tests](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/builtin.rs#L278-L338) [registry tests](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/registry.rs#L514-L646)
- `[TEST]` 真实安装 e2e 是 `#[ignore]`，需要网络与 `DSH_TEST_NODE`/`DSH_TEST_PNPM` 两个环境变量，且安装的是 `0.1.5-rc.2` 而不是内置 pin 的 `0.2.0-rc.2`；它证明“测试设计存在”，不等于本次跑过。[e2e](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/registry.rs#L618-L646)
- `[TEST]` 手工验收脚本 E 段用 staged 运行时直调 launcher：临时 `DSH_HOME`、`desktop` + `--init-from-default`、12s 后请求 `/`，HTTP 200/401 即判通过；无 staged 运行时则跳过。这是 launcher/内置启动路径最接近端到端的覆盖，但不在 CI 里自动执行。[acceptance.sh](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/scripts/acceptance.sh#L93-L117)
- `[TEST]` 没有任何测试校验 sidecar 哈希、运行时树清单、安装包内容或签名；`is_valid_runtime` 只断言 `lib/bin.js` 存在。[有效性测试](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/desktop/src-tauri/src/runtime/registry.rs#L606-L616)

## [CI]

- `[CI]` CI 与 release 都在构建前跑同一准备脚本：CI `node desktop/scripts/prepare-builtin-runtime.mjs --variant latest` 后 `cargo check --locked` / `cargo test --locked`；release 同脚本后 `tauri-action` 出包。[ci.yml](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/.github/workflows/ci.yml#L41-L64) [release.yml](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/.github/workflows/release.yml#L41-L52)
- `[CI]` release workflow 没有签名/公证步骤或 Apple 凭据注入，与 `signingIdentity: "-"` 的 ad-hoc 结论一致；构建机 Node 是 22，与 sidecar 的 Node 24 不是同一版本（不影响产物，但说明“构建时 Node”和“内置 Node”是两条线）。[release.yml](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/.github/workflows/release.yml#L41-L52)
- `[CI]` 仓内没有 pnpm-lock（CI 注释明说），与本卡“本地/CI 可复现”的边界相关：前端依赖如此，内置 dsh 树的安装同样无 lock。[ci.yml](https://github.com/hyperion2144/dsh-desktop-tauriapp/blob/577a6d3ac95aeb956e7bb8134efb574294ea63d2/.github/workflows/ci.yml#L42-L45)
- **本次未运行 CI，也未查看任何 run 结果**；workflow 存在只证明登记了这些步骤。

## [RUN]

无。本文所有结论来自固定提交的源码、仓库文档与 workflow 文本；未安装/构建/启动目标应用，未下载 release 产物，未在干净机器上验证“无 Node 也能启动”。

## 未核实与下一步

- `[OPEN]` 发布产物（v0.12.0 dmg/msi）里实际是哪棵 dsh 树：`resources/dsh` 被 gitignore，只能信 pin 与 CI 步骤；未下载 release asset 核对。
- `[OPEN]` `@deepseek-ai/dsh@0.2.0-rc.2` 是否导出同名 `runProfile`/`loadLayeredEnv`、是否接受 `fromDefaultProfile: "web"`：未装该版本核对；只有项目自述与手写验收脚本。
- `[OPEN]` “同机装官方 Electron 桌面应用后共用 `profiles/desktop`”的覆盖顺序与损坏面：本卡与旧卡都未实测。
- `[OPEN]` 选中版本树失效回退随包树时，按设置生成的 `connection.inject` 是否与 0.2.0-rc.2 冲突：代码路径存在，未运行验证。
- `[OPEN]` 已发布 dmg 的签名/公证状态、Windows 安装包签名：README 自述“非公证/未签名”，本次未用 `codesign`/`signtool` 验证。
- `[OPEN]` 运行时下载在离线/代理失败、磁盘不足、pnpm 半途被杀时的用户可见状态：代码有清理路径，未实测。

## 对卡片的净结论

1. **“内置运行时”成立，但含义要写准**：随包 Node sidecar + 随包 npm 依赖树，运行时**不解压、不首启下载**，launcher 用内部 `runProfile` 起进程；壳还装了解析钩子把裸说明符钉到内置树。
2. **卡片基线版本错了**：内置 pin 是 `0.2.0-rc.2`；卡片写的 `0.2.1-rc.3` 是本机 CLI，不是安装包。卡里引用上游 `lib/bin.js`、`profile-boot-*.js` 的行号应标注为“本机 CLI 版本”，不能当作内置运行时证据。
3. **“精确 pin + 可复现”只到直接坐标**：dsh/pnpm 版本精确，Node 浮动、无 lock、无 hash/签名；`desktop-runtime.json` 只写不读。
4. **进程归属是“per-profile worker + 端口强占 + 单守护器”**：重启会杀掉端口上的任何监听者；健康探测只管主实例/远程地址，多开次窗没有守护；自愈是“首次失败即重启、3 次失败封顶、120s 健康才清零”。
5. **恢复≠回滚**：回退只覆盖“树缺失/无效/来源不可用”，不覆盖“树有效但启动即崩”；没有应用自动更新，也没有运行时版本回滚点，换回内置要用户手动切。
6. **权限面不是 shell/fs 授权，而是 remote origin 的命令白名单**：`csp: null` + `withGlobalTauri` + 约 80 个对 loopback 页面开放的命令（含运行时下载/删除、服务重启、设置写入），是比“有没有 shell 权限”更值得写进卡片的风险边界。
