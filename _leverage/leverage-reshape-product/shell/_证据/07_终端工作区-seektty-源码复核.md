---
title: "源码复核：Hilbert-beinghappy/seektty 终端工作区"
domain: reshape-product
kind: evidence
positioning: "固定复核 SeekTTY 1.3.0 的表层归属、三档兼容与上游 peer 闸门、pnpm 11 GVS 适配、原生 scrollback、self-first 更新器与 teardown/Profile 边界。"
read_when: "核对 shell/15 的「表层归我、状态归你」「三档兼容」「pnpm 11 适配」「原生模式」「更新器」结论。"
status: observed
updated: 2026-11-01
---
# SeekTTY 终端工作区源码复核

> **固定快照**：只读一手仓库，不安装、不构建、不执行目标代码，未触碰本机 DSH profile。`main` HEAD = tag [`v1.3.0`](https://github.com/Hilbert-beinghappy/seektty/releases/tag/v1.3.0) = [`42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5`](https://github.com/Hilbert-beinghappy/seektty/commit/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5)（2026-10-13T14:04:00+08:00，`git describe --exact-match` = `v1.3.0`，290 个提交）；npm `seektty` 的 `latest` 也是 **1.3.0**（2026-10-13T06:10:31Z 发布），发布物与 tag 同版。本文行号默认取该 commit。
>
> **声明的宿主版本**：根 `package.json` 的 `dsh.compatibility` 为 `minimum = tested = 0.2.0-rc.2`，`engines` 只有 Node（无 `engines.dsh`），另有 **63 个** `@deepseek-ai/dsh*` peer 全部锁死为精确 `0.2.0-rc.2`（共 67 个 peer）。[manifest](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/package.json#L70-L79) [peers](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/package.json#L103-L171)
>
> **与当前基线的错位**：本机安装的 DSH 是 **0.2.1-rc.3**（2026-10-23 发布；`dsh --version` 与 `@deepseek-ai/dsh/package.json` 均为该版本），npm `latest` 已是 **0.2.1-rc.5**；0.2.0-rc.2 发布于 2026-09-29。中间隔着 0.2.1 的 5 个 alpha 与 5 个 rc（rc.1…rc.5），**不是「落后一个 rc」**。更关键的是：0.2.0-rc.2 已存在的 Host peer 闸门，63 个精确 peer 在 0.2.1-rc.3 上全部判为不满足，normal install 预期会被上游拒绝，而不是「启动后给提示」（代码路径推断、未执行，详见 §[SRC-DSH]）。
>
> **标记**：`[DOC]` 仓库 README / 发布说明 / 文档；`[SRC-TARGET]` 目标固定提交源码；`[SRC-DSH]` 本机安装的 DSH `0.2.1-rc.3`（及 npm 取回的 `dsh-app-boot@0.2.0-rc.2` 包）；`[TEST]` 测试源码；`[CI]` workflow 登记——均为**产物，不是运行证明**；`[RUN]` 本轮只读的 clone / registry / 包元数据核对，**未执行目标代码、未安装、未运行测试**。

## 对旧卡的校正

| 旧卡主张 | 固定树能证明什么 | 不能据此声称什么 |
|---|---|---|
| 「更新默认 `SEEKTTY_UPDATE=check`（跑完提示）」 | `[SRC-TARGET]` 默认是 **`auto`**：未设变量时返回 `auto`，只有显式 `check/notice` 才只提示，`0/off/false/manual` 才关闭。[updateMode](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L83-L91) `[TEST]` 单测直接断言 `updateMode({}) === 'auto'`。[version-scan.test](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/tests/version-scan.test.ts#L446-L451) | 不能说「默认只提示、不安装」：默认每次启动前都会打 npm `latest`，命中就**先安装再启动**（见 §6）。 |
| 「三档 + 未知档：高于已测可启动但提示」 | `[SRC-TARGET]` 这条只描述 SeekTTY **自己**的运行时检查：低于下限抛错退出，高于已测写 stderr 提示，读不到/无法解析版本抛错，`host.describe` 的 `0.0.1` 占位符被特判放行。[error](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/dsh-compat.ts#L129-L152) [notice](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/dsh-compat.ts#L154-L177) [gate](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/client-runtime.ts#L176-L193) | 在 0.2.1-rc.3 上，**上游先否决**（按该版本代码路径）：63 个精确 peer 触发 Host 的 `evaluatePluginCompatibility`，`dsh plugin add` 预检拒绝、profile 加载跳过、profile preflight 禁用该行；SeekTTY 的「提示」根本轮不到。要装只能按精确版本豁免。 |
| 「自动更新只装显式兼容区间」 | `[SRC-TARGET]` 所谓区间是**退化的**：`AUTO_PERMITTED_DSH_MINIMUM = 0.2.0-rc.2`、`LEGACY_MAXIMUM = 0.1.0-rc.8`（低于下限），因此区间分支永不命中，实际只允许**精确的 tested 版本**；代码注释也承认「floor above the legacy ceiling permits only the tested pin」。[constants](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/version-scan.ts#L19-L24) [permit](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/version-scan.ts#L126-L136) | 不能读成「0.2.x 有一个可自动升级的区间」：0.2.0-rc.2 之后任何版本（含 0.2.1-rc.3）都只会打印「超出许可范围，不会安装」。 |
| 「装法走原生 reconciliation，不在原生 reconciliation 之外改 profile 清单」 | `[SRC-TARGET]` launcher 确实只调 `dsh plugin --profile tui add` 并 `dsh --profile tui` 启动；但 TUI 内的 `/plugin` 由 **SeekTTY 自己**在 profile 目录跑 `pnpm`，再用 Host 的 `@deepseek-ai/dsh-app-boot` 写 manifest、重排 `dsh.profile.bundles`，还能创建/克隆/转换 profile。[launcher](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L307-L357) [pnpm](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/profile-plugin-manager.ts#L312-L324) [reconcile](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/profile-plugin-manager.ts#L699-L735) [create](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/profile-plugin-manager.ts#L590-L633) | 不能称「只读、从不改 profile」：写的是宿主**同一套 manifest 工具**，但「加哪些 bundle、谁排前面」的决策在 SeekTTY，不在 `dsh plugin` CLI。 |
| 「能力全从运行中 Harness 发现，不硬编码；第 5 层不抢」 | `[SRC-TARGET]` 服务/注册表/设置/凭据确实来自运行中的 Host；但 `cordis.patch.yml` **禁用 25 个宿主行**（tool-bash/fs/todo/subagent/workflow…），并由 bundle 自己 insert `preset-standard`/`preset-minimal`/`preset-ptc` 三套 Agent Preset（含完整工具表）与 `agent-preset-registry.default: standard`。[header](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/cordis.patch.yml#L1-L17) [preset](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/cordis.patch.yml#L185-L210) [default](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/cordis.patch.yml#L100-L108) | 不能说「预设归 Host、它只提供编辑入口」：默认预设与工具目录是 bundle 数据；上游新加的工具**不会自动出现**，除非它也进了 preset。默认模型与权限命令仍归 Host。 |
| 「原生模式：已写入历史不重着色不重排；Ctrl+L 只刷新尾部」 | `[SRC-TARGET]` 切换、Esc、退出 alt screen、关鼠标上报、冻结非动态块都是真的；但「提交历史 + 活动尾部」的增量机制（`NativeHistory` 账本、序列化 `NativeOutput`、`renderNativeTail`）由 **`SEEKTTY_NATIVE_TAIL=1`** 显式启用，未设时 `nativeOutput` 为 `undefined`。[gate](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/surface.ts#L202-L204) [tail](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/transcript.ts#L3297-L3312) [release](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/docs/release-v1.3.0.md#L22-L24) | 「不重着色/只刷尾部」只在 opt-in 路径有机制保证；默认原生模式仍走补丁版 pi-tui 的主屏渲染，实际重绘边界未在真实终端验证（`[OPEN]`）。 |

## [DOC] 作者声明

- `[DOC]` 所有权口号：「SeekTTY is the terminal surface; Harness remains the owner of runtime state.」[README](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/README.md#L39-L39)
- `[DOC]` 能力发现：models / providers / agent presets / permissions / commands / tools / settings / skills / MCP / marketplace 全部从运行中的 Harness 发现，「第三方 Bundle 新增的能力无需硬编码即出现」。[README](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/README.md#L41-L41)
- `[DOC]` 安装：`pnpm add --global --config.enable-global-virtual-store=false @deepseek-ai/dsh@0.2.0-rc.2` → `dsh plugin --profile tui add --config.enable-global-virtual-store=false seektty@1.3.0` → `dsh --profile tui`；称走原生 `dsh plugin` reconciliation。[README](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/README.md#L62-L72)
- `[DOC]` 更新：self-first、每次最多一个兼容组件、绝不装未测缺口或未来 Host、`DSH_BIN`/本地安装/`SEEKTTY_SPEC` 保持不变、失败不阻塞启动；`SEEKTTY_UPDATE=check` 只是**可选**的「事后提示」，`=0` 关闭。[README](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/README.md#L106-L106)
- `[DOC]` 兼容表：Minimum = Tested = `0.2.0-rc.2`；旧于下限拒绝、新于已测「可启动 + 提示」，自动更新只装显式兼容区间；附件适配器只处理确切的旧 imageLimits 形状，未知形状 fail closed。[README](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/README.md#L452-L465)
- `[DOC]` pnpm 11：`store/v11/links` 会在 SeekTTY 启动前让测试过的 dsh/Cordis loader 失败；只在**它发起的**变更（launcher provisioning、self-update、`/plugin` 的 install/update/remove/reconciliation）加 `--config.enable-global-virtual-store=false`；不 `pnpm config set`、不设 `NODE_PATH`、不复制 Host 包、不在原生 reconciliation 外改 profile 清单。[README](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/README.md#L469-L471)
- `[DOC]` 原生模式：F3 或 `/mouse` 在空闲时切换；退出 alternate screen、完整会话写入普通 scrollback、关闭鼠标上报；Esc 取消回填，Ctrl+L 只刷新活动尾部；Terminal.app 需按 Fn、iTerm2 需按 Option 拖选。[help 文本](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/help.ts#L28-L42)
- `[DOC]` Clarify 的 15 分钟过期是**可选 companion 插件**的行为（问答/草稿留在 Host 内存，主会话只收显式提交的 Draft），不是本 Bundle 的 TTL。[README](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/README.md#L151-L151)
- `[DOC]` 回滚是**手工**的：README 只给「回到 1.2.6 + dsh 0.1.5-rc.1」的命令，「1.3.0 不要装到旧 Host 上」。[README](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/README.md#L498-L506)

## [SRC-TARGET] 机制复核

### 1. 表层归属：插件 bundle 在宿主机进程内，不是自建服务、也不是 `dsh web` 的客户端

`[SRC-TARGET]` 三条入口链互相印证它不是「自带服务器」：

1. **launcher 只做 provision + exec**：解析 `--profile`（默认 `tui`），确保 profile 里装了 `seektty`（先移除遗留 `deepseek-tui`），然后 `spawnSync('dsh', ['--profile', profile, ...inner], { stdio: 'inherit' })`；没有 HTTP、没有端口。[launch](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L307-L357) [spawn](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L193-L195)
2. **profile 层没有 Web 服务器**：`cordis.patch.yml` 开头即写明「No Web server, browser loader, or React package is mounted」；bundle 的 `insert` 把 `tui-runner`（`seektty` 自己）挂进树。[patch header](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/cordis.patch.yml#L1-L4) [tui-runner](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/cordis.patch.yml#L180-L183)
3. **Client 走「无网络」载体**：`InProcessConnectionService` 在进程内注册 RPC/Fetch，文档说「Provide the Host half without a Web server or listening socket」；Client 侧 `createConnectionHandle` 明确省略 Browser/fixture 构造器，因为终端插件「always receives its API and RPC carriers in-process」。[in-process](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/in-process.ts#L1-L2) [no server](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/in-process.ts#L78-L82) [connection](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/compat/client-connection.ts#L1-L12)

`[SRC-TARGET]` 因此所有权是「**同一进程内的 Surface**」，不是窗口壳也不是远程客户端：

| 状态 | 权威 owner | 依据 |
|---|---|---|
| Agent / Session / 消息历史 / 工作区 | Harness（`ctx.sessions`、`ctx.workspaces`、`ctx.sessionController`） | 启动时通过 Runtime API 打开/恢复会话，SeekTTY 不建自己的会话库。[targetSession](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/client-runtime.ts#L132-L155) |
| Settings / 凭据 | Harness（`settings.mutate` revision 保护、`credentials.set`） | `/mouse` 切换写入 `seektty-behavior` 命名空间并带 revision；失败回滚。[mouse](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/actions.ts#L3196-L3225) |
| Profile 依赖与 bundle 顺序 | SeekTTY 调 pnpm + 宿主 manifest 工具写入 | 见 §2 |
| 终端呈现状态（草稿、选择、原生历史账本） | SeekTTY（仅显示态） | `NativeHistory` 自称「Display-only ledger」；`source offsets` 只用于去重投递。[native-history](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/native-history.ts#L14-L20) |
| 宿主版本读数 | SeekTTY 覆盖 `host.describe`，从 dsh 安装目录 `package.json` 读真实版本 | 规避官方 `0.0.1` 占位符。[describeHost](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/api-compat.ts#L123-L137) |

`[SRC-TARGET]` **at 0.2.1-rc.3 的运行前提**：这些 `insert`/`disabled` 覆盖与 3 套 preset 都是 SeekTTY 的 bundle patch 数据；它改变的是**进程级能力装配**（25 个宿主行被显式禁用、工具表移入 preset），不只是「画界面」。这解释了为什么它能与 Web 共存却不同于纯 UI 皮肤：它拿走的是 profile 层的组合权。

### 2. Profile 与两条入口

`[SRC-TARGET]` launcher 侧：

- 默认 profile 名硬编码 `tui`（不是 `desktop`）；`--profile` 可覆盖，空值报错。[launcherArgs](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L120-L156)
- 若 `~/.dsh/profiles/<name>/package.json` 仍有 `deepseek-tui`，先 `dsh plugin --profile <name> remove`，再按需 `add seektty@<DEFAULT_SPEC>`（`SEEKTTY_SPEC`/`DEEPSEEK_TUI_SPEC` 可覆盖 spec）。[migrate](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L342-L356)
- `DSH_HOME` 被尊重；版本探测时会**删掉** `DSH_HOME`，避免探测到另一套 home。[probe env](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L196-L205) [profile dir](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L44-L69)
- 进程内入口**拒绝没有 `--profile` 的启动**（`tui-startup` 抛「必须通过 dsh --profile 启动」），说明它假设自己由 dsh 的 profile loader 装载。[activeProfile](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/startup.ts#L62-L75)

`[SRC-TARGET]` TUI 侧（`/plugin`、profile 管理）：

- `ProfilePluginManager` 的持久状态只有 profile 现有 manifest/lockfile/依赖树/bundle 顺序；`ensureProfile()` 在缺失时用宿主 `initProfile` 建 profile。[class](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/profile-plugin-manager.ts#L252-L285)
- `run()` 在 profile 目录直接 `crossSpawn('pnpm', ...)`，成功后 `reconcile()`：按已安装包是否声明 `dsh.bundle.patch` 自动增删 `dsh.profile.bundles`，并 `writeProfileManifest`。[run](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/profile-plugin-manager.ts#L336-L384) [reconcile](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/profile-plugin-manager.ts#L699-L735)
- `reorderBundles()` 只允许「当前 multiset 的重新排列」，写 manifest。[reorder](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/profile-plugin-manager.ts#L444-L463)
- `createUsableProfile()` 可**从现有 profile 复制**、增删 bundle、改写依赖 spec、再 `pnpm install`；`/profile` 的 create 端口固定 `addBundles: ['seektty']`、`removeBundles: ['@deepseek-ai/dsh-web-app','@deepseek-ai/dsh-headless']`，即把 web/headless profile **转换成 TUI profile**。[create](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/profile-plugin-manager.ts#L590-L635) [bridge](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/management.ts#L58-L59) [port](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/management.ts#L684-L692)

`[SRC-TARGET]` 两条入口的一致性边界：launcher 与 TUI 写的是**同一个** `$DSH_HOME/profiles/<name>`，不存在第二套包树；但 launcher 只在**缺依赖**时安装，不保证版本等于自己的 `PACKAGE_VERSION`；默认 `auto` 更新则会在启动前改这个 profile。因此「launcher 会 provisioning 自己的包树」这一顾虑成立一半：树是共享的，**版本漂移**与**启动前变更**才是真实风险。

### 3. 三档兼容与未知契约

`[SRC-TARGET]` 运行时检查链（在 TUI Client 装配完成后）：

| 输入 | 结果 |
|---|---|
| 版本 < `0.2.0-rc.2` | `dshCompatibilityError` 返回文本 → `throw` → 客户端清理 fiber 后退出（拒绝启动） |
| 版本 > `0.2.0-rc.2` | `dshCompatibilityNotice` → 写 stderr，继续启动 |
| 版本无法解析，或读不到 | 返回错误文本 → 拒绝启动（fail closed） |
| 版本恰为 `host.describe` 占位符 `0.0.1` | **放行且不提示**（明确特判） |

- 依据：[compare/minimum](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/dsh-compat.ts#L140-L151)、[placeholder](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/dsh-compat.ts#L134-L139)、[throw 位置](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/client-runtime.ts#L182-L193)。
- `[SRC-TARGET]` 这个检查读的是**真实 dsh 包版本**，不是官方占位符：`describeHost` 用 `process.argv[1]` 找 dsh 入口，再读 `../package.json` 的 `version`。[describeHost](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/api-compat.ts#L123-L137) 所以在能装载的前提下，0.2.1-rc.3 会走「新于已测 → 提示」这一档。
- `[SRC-TARGET]` 「未知契约 fail closed」的实例是权限命令适配器：只有 `commands.execute` 的 wire 字段恰为 `agentId,line,submittedAttachments` / `agentId,line,images` / `agentId,line` 之一才调用，其他形状直接抛「Host 权限命令契约不兼容」，**不换参数重试**（注释明说不能重试可能已执行的命令）。[permission](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/capabilities.ts#L1279-L1295)
- `[SRC-TARGET]` 附件适配器只认 rc.6/rc.7 的精确旧形状：必须四个正整数 + `mediaTypes` 字符串数组 + **无** `maxImageDimension`；否则原对象原样返回。`apply()` 只在形状变化时替换并被 `ctx.effect` 还原。[shape](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/attachment-compat.ts#L36-L48) [apply](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/attachment-compat.ts#L80-L90)
- `[OPEN]` 被特判放行的 `0.0.1` 是唯一「未知但放行」的口子；如果未来某个 Host 仍上报该占位符，兼容闸门等于失效。README 没有提到它。

### 4. pnpm 11 Global Virtual Store：局部、可逆、只在自发起变更上

- `[SRC-TARGET]` 常量与动作：`--config.enable-global-virtual-store=false`；只对 `add/install/remove/rm/uninstall/update/up` 这类会改动包树的命令追加；已有的 GVS 参数会被过滤并**归一化**为安全值；`--global` 保持紧跟子命令。[pnpm-compat](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/pnpm-compat.ts#L10-L55)
- `[SRC-TARGET]` 应用面正好三类：launcher 的 `dsh plugin ... add/remove` 与 `pnpm add -g`；`--update`/auto 的 self-update 与 dsh 升级；TUI `/plugin` 的 pnpm run（`withPnpmGvsCompatibility(args)`）。[dshPluginArgs](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/pnpm-compat.ts#L57-L60) [update](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L378-L399) [plugin run](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/profile-plugin-manager.ts#L318-L324)
- `[SRC-TARGET]` 不碰全局配置：没有 `pnpm config set`、没有 `NODE_PATH` 写入、没有复制 Host 包（全仓检索无「config set」调用）。`doctor()` 发现插件位于 `store/v11/links` 时只给 warning，并说明后续操作会自动附加参数。[doctor](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/profile-plugin-manager.ts#L484-L494)
- `[SRC-TARGET]` 诊断有两个触发面：launcher 在 **dsh 退出码非 0** 且自身/`DSH_BIN`/`PNPM_HOME` 的 realpath 命中 `store/v11/links` 时，打印双语诊断 + 两条恢复命令（`pnpm add -g ...`、`dsh plugin ... add ...`）；profile 管理器另用「布局 + loader 症状」双条件识别已知失败。[launcher detector](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L264-L290) [advice](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/pnpm-compat.ts#L108-L141) [classifier](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/pnpm-compat.ts#L103-L115)
- `[SRC-TARGET]` 但恢复建议里的 `pluginSpec` 取 profile 现有 spec 或 `DEFAULT_SPEC`；若 profile 已被 GVS 弄坏到 manifest 不可读，走的是 launcher 抛错路径，不会进入建议分支。`[OPEN]` 该分支未实测。

### 5. 原生 scrollback 模式

- `[SRC-TARGET]` 模式是 Harness Settings 值 `seektty-behavior.mouseMode: 'full' | 'native'`，不是进程内临时开关；`/mouse [full|native|toggle]` 先读文档 revision，再 `mutate`，应用失败则用新 revision 回滚。[type](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/protocol.ts#L286-L288) [command](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/capabilities.ts#L317-L318) [rollback](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/actions.ts#L3219-L3245)
- `[SRC-TARGET]` 切换前置条件（真正「仅空闲」）：无正在切换、无进行中的历史补载、无打开的子 Agent、当前轮次未运行、无待审批/提问、无待发队列。[block reason](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/surface.ts#L1194-L1216)
- `[SRC-TARGET]` 切到 native 前**顺序**拉完历史：循环 `loadOlder()` 直到 `snapshot.hasMore === false`，每页上报节点数；不靠「可见节点数不变」推断结束，因为一页可能只有编辑/控制事件。[load](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/surface.ts#L1217-L1254)
- `[SRC-TARGET]` 取消语义：Esc `abort()` 只中止补载 Controller，提示「当前会话和 Agent 仍保持运行」；另有第二个 Esc 只停 native 历史输出（`cancelNativeReplay`），不动会话。[esc backfill](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/surface.ts#L2336-L2348)
- `[SRC-TARGET]` 模式切换本身：`terminalSession.setDisplayMode()` 决定 alt screen 与鼠标上报；`transcript.setNativeMode()` 冻结非动态块（`nativeFrozenBlocks`）；切回时若行列未变可复用 render state，否则重置重绘。[switch](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/surface.ts#L1256-L1284) [freeze](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/transcript.ts#L3306-L3327)
- `[SRC-TARGET]` 增量历史（真正「已写历史不再参与渲染」）需要 `SEEKTTY_NATIVE_TAIL=1`：`NativeOutput` 只在候选时创建，`renderNativeTail()` 与 `NativeHistory` 的提交/投递账本都在这条路径上；未设时 Ctrl+L 仍只 `invalidate()` 动态块 + 请求渲染，但走的是整帧渲染路径。[candidate](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/surface.ts#L202-L204) [ctrl+l](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/surface.ts#L2369-L2374) [invalidate](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/transcript.ts#L2824-L2832)
- `[SRC-TARGET]` 补丁版 pi-tui 提供两个私有钩子：`__seekttyManagedAlternateScreen` 与 `__seekttyNativeFrame`；native 模式下 `fullRender(clear=false)` 不再发 `2J/3J`，避免清掉终端 scrollback，并只从 `height` 起点重画。[patch](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/patches/%40mariozechner__pi-tui%400.73.1.patch#L2200-L2235)

### 6. 更新器：self-first、一次一个、失败不阻塞，但没有回滚

- `[SRC-TARGET]` 默认 `auto`：`maybeAutoUpdate()` 在 `launch()` **之前** await，命中就装。`updateMode` 优先级：`SEEKTTY_UPDATE` > 遗留 `SEEKTTY_UPDATE_CHECK=0` > 默认 `auto`。[mode](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L76-L91) [boot order](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L509-L525)
- `[SRC-TARGET]` self-first：`updatePlan()` 先看 SeekTTY（且未被 pin、npm latest 更新）→ 只给 seektty；否则才考虑 dsh。`exclusiveUpdatePlan()` 二次裁剪，保证**至多一个 spec**。[plan](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/version-scan.ts#L171-L182) [exclusive](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/version-scan.ts#L155-L163)
- `[SRC-TARGET]` 「绝不装未来/缺口 Host」成立：dsh 候选必须 `isAutoPermittedDshVersion`（实际只等于 tested）**且**严格新于已装版本；`dshLatest` 超出就打印「不会安装」。[installable](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/version-scan.ts#L138-L153) [advice](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/version-scan.ts#L190-L216)
- `[SRC-TARGET]` 不越权改 pin：`DSH_BIN` 非空 → 不升级 dsh；`SEEKTTY_SPEC` 或本地/link spec → 不升级 SeekTTY；`facts` 只读 PATH `dsh --version`（删 `DSH_HOME`），不看 profile/session 文件。[facts](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L103-L114)
- `[SRC-TARGET]` 失败语义：auto 全部包在 `try/catch` 里静默；`applyUpdatePlan` 非 0 只返回码，不抛；`--update` 返回非 0。**没有回滚**：升级前不记旧版本、不保留旧包树、失败后不自动降级；恢复只有 README 的手工命令。[auto](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L455-L478) [update](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L360-L414)
- `[SRC-TARGET]` `SEEKTTY_UPDATE=check` 只在启动后、且 **stderr 是 TTY** 时做 passive 提示；非 TTY 不提示。`=0` 则完全跳过网络检查。[notice](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L484-L497) [TTY gate](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L517-L519)
- `[SRC-TARGET]` 延迟代价：auto 的 registry 扫描每个请求 3s 超时（两路并行），但成功命中后的 `pnpm add`/`dsh plugin add` 是同步 spawn，可能长时间占用启动；「不阻塞」只对**失败**成立，不对**耗时**成立。[timeout](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/version-scan.ts#L15-L17) [sync run](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/bin.ts#L292-L305)

### 7. Teardown、崩溃与重启交接

`[SRC-TARGET]` 这块比卡片写得更完整：

- 同步恢复终端（私有模式 → raw → 光标）在任何异步清理之前；`SHOW_CURSOR` 兜底，异常全部吞掉不阻断。[restore](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/process-guards.ts#L23-L50)
- 清理有 **2s 上限**（`withCleanupTimeout`），避免挂住的 drain/dispose 卡死进程。[timeout](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/process-guards.ts#L52-L70)
- 一次性 fatal guard 覆盖 `uncaughtException`、`unhandledRejection`、`SIGTERM`（143）、`SIGHUP`（129）；顺序是 restore → 有界 cleanup → exit(1/143/129)。[guards](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/process-guards.ts#L92-L135)
- POSIX 挂起：`SIGTSTP` 恢复屏幕/协议后自停，`SIGCONT` 重新进入并重建后台同步；Ctrl+Z 仍是输入撤销，不是挂起快捷键。[suspend](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/process-guards.ts#L137-L172) [surface](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/surface.ts#L2593-L2610)
- 正常关闭路径：先把 native 输出排空（有 deadline）→ `restoreSurfaceTerminalSync` → 逐项 dispose（notices/overlay/mouse/transcript/agentTree/syntax）→ `drainInput` → `tui.stop()` → `ctx.fiber.dispose()`；最后 `detachFatalGuards()`，失败汇总成 exit code。[close](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/surface.ts#L1104-L1141) [tail](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/client/surface.ts#L2680-L2691)
- 受控重启：新进程用 `process.execPath` + dsh 入口 + 同 profile/args，继承 stdio；旧进程 `appExit(0)`。交接文件是 tmp 下私有目录、`wx` + `0600`、≤256 KiB、单次消费、24h 清扫；profile/cwd/resume 任一不符就降级为普通启动并给提示，绝不让坏交接阻塞启动。[restart](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/startup.ts#L88-L120) [handoff](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/app-handoff.ts#L93-L157) [reconcile](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/src/host/restart-handoff.ts#L43-L81)
- `[SRC-TARGET]` 进程退出后 Host 侧资源（会话、job、子进程）是否被 SDK 正确回收，本 Bundle 不负责；它只 dispose 自己注册的 fiber/service。`[OPEN]` 未在真实会话里验证。

## [SRC-DSH] 上游接缝（本机 `@deepseek-ai/dsh@0.2.1-rc.3`）

- `[SRC-DSH]` **上游有独立的插件兼容闸门**：`@deepseek-ai/dsh-app-boot@0.2.1-rc.3` 的 `evaluatePluginCompatibility(manifest)` 在插件没有 `engines.dsh` 时，逐个检查 `@deepseek-ai/dsh`/`@deepseek-ai/dsh-*` 的 `peerDependencies` 是否满足运行版本（`semver.satisfies(..., { includePrerelease: true })`）。`evaluator`（`dsh-app-boot@0.2.1-rc.3 lib/index.js:300-322`）
- `[SRC-DSH]` 该闸门在三个位置生效：① `loadProfileDirectory()` 对不满足且未豁免的 bundle **直接 throw**，结果进入 `skippedBundles`（静默跳过该 bundle）；② `prepareProfileEntries()` 把不满足的条目 `disabled = true` 并向 stderr 报「disabling profile plugin …」；③ `@deepseek-ai/dsh-plugin-manager` 在 `add` 前预检 named spec，命中即 **installation rejected / nothing was installed**。`load`（`dsh-app-boot@0.2.1-rc.3 lib/index.js:1019-1029`） `entries`（`dsh-app-boot@0.2.1-rc.3 lib/index.js:2306-2340`） `reject`（`dsh-plugin-manager@0.2.1-rc.3 lib/index.js:577-606`）
- `[SRC-DSH]` `semver.satisfies('0.2.1-rc.3', '0.2.0-rc.2', { includePrerelease: true }) === false`（本机 semver 实测）。SeekTTY 有 **63 个** 精确 `0.2.0-rc.2` peer，因此在 0.2.1-rc.3 上会被判为 63 项不满足；normal install 预期被拒绝，或已装 profile 加载时被 skip/disable。要运行只能执行 `dsh plugin --profile <p> allow-version seektty@1.3.0 --dsh-version 0.2.1-rc.3 --accept-risk`（写入 profile 的 `compatibility.json` 精确豁免）。`exemption cmd`（`dsh@0.2.1-rc.3 lib/plugin-BiveYA7h.js:14-48`）
- `[SRC-DSH]` 该闸门在 **0.2.0-rc.2** 就存在（同函数，peer-only 语义相同），只是 tested 宿主上 63 个 peer 恰好精确匹配；所以「0.2.0-rc.2 能装」不是 SeekTTY 兼容策略的胜利，而是精确 pin 的副作用。`0.2.0-rc.2 evaluator`（`dsh-app-boot@0.2.0-rc.2 lib/index.js:258-300`）
- `[SRC-DSH]` `dsh plugin --profile <p> <pnpm-args>` 把剩余参数**原样转发**给 profile 目录里的 pnpm，因此 `--config.enable-global-virtual-store=false` 是合法透传；`desktop` profile 被独占保护（「managed exclusively by the Electron application」），印证卡片 §1 关于 `tui` 命名的选择。`plugin`（`dsh@0.2.1-rc.3 lib/bin.js:115-129`） `desktop`（`dsh@0.2.1-rc.3 lib/bin.js:35-37`）
- `[SRC-DSH]` SeekTTY 依赖的 `@deepseek-ai/dsh-app-boot` 导出在 0.2.1-rc.3 仍存在（`initProfile`、`writeProfileManifest`、`resolveProfileDir`、`readProfileManifest`、`resolveBundleDir`、`PROFILE_TEMPLATES`、`PROFILES_DIR`、`DEFAULT_PROFILE_BUNDLES`、`PROFILE_PATCH_FILENAME`），所以「能不能装载」的分歧点是 peer 闸门，而不是 API 缺失。`exports`（`dsh-app-boot@0.2.1-rc.3 lib/index.js:4566`）
- `[SRC-DSH]` 边界：以上只证明 0.2.1-rc.3 的闸门语义与导出面；**未执行** `dsh plugin add`，也未在 0.2.1-rc.3 上启动过 SeekTTY，拒绝/跳过属于代码路径推断（`[OPEN]`）。

## [TEST]

- `[TEST]` 测试是 vitest，共 **242** 个 `tests/*.test.*` 文件；`pnpm test` = `vitest run`。[script](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/package.json#L79-L91)
- `[TEST]` 更新器：`tests/version-scan.test.ts` 断言默认 `auto`、check/off 语义、future/gap Host 不安装、至多一个组件；`tests/package-contract.test.ts` 断言 auto 常量与 `dsh.compatibility` 同源。**这些证明设计意图，不证明真实 registry 行为。** [default](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/tests/version-scan.test.ts#L446-L451) [contract](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/tests/package-contract.test.ts#L50-L58)
- `[TEST]` 原生模式/尾部：`native-tail.test.ts`、`native-tail-terminal.test.ts`、`native-tail-exit.test.ts`、`native-history-contract.test.ts`、`native-history-gap.test.ts` 覆盖尾部事务、取消、投递账本；`tests/native-tail-exit.test.ts` 明确使用 `SEEKTTY_NATIVE_TAIL`。**未见测试覆盖「默认原生模式」的整帧重绘边界。** [tail exit](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/tests/native-tail-exit.test.ts#L1-L20)
- `[TEST]` Profile/插件：`profile-create-usable.test.ts`、`profile-plugin-snapshot.test.ts`、`plugin-remove.test.ts`、`plugin-progress.test.ts`、`installer-output.test.ts` 覆盖 manifest 写回、bundle 顺序、输出脱敏；证明「SeekTTY 自己跑 pnpm 再 reconcile」是刻意设计，不是旁路。[create](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/tests/profile-create-usable.test.ts#L1-L15)
- `[TEST]` 终端清理：`tests/process-guards.test.ts`、`terminal-session.test.ts`、`mouse-*.test.ts`；覆盖同步恢复、2s 上限与协议字节，但都是单测/夹具，不证明真实 TTY 的 teardown。`[TEST]` 本轮**未运行任何测试**。

## [CI]

- `[CI]` 有 2 个 workflow。`ci.yml` 的 `check` job：pnpm 11.7.0 + Node 22.x → `pnpm install --frozen-lockfile` → `pnpm run check`（typecheck + vitest + build + pack-check）→ **`git diff --exit-code lib/`**（提交的构建产物必须与源码同步）→ 打包后用 stock dsh 跑一次 `stock-dsh-cycle`。[ci](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/.github/workflows/ci.yml#L8-L49)
- `[CI]` `pnpm11-layout` job 是 3 OS × Node 22/24 矩阵，pnpm 11.7.0；两步分别执行 `pnpm test:pnpm11-layout false`（GVS 关闭，要求完整 dsh 生命周期）与 `true`（**「positive boot or exact known-failure diagnosis」**——允许已知失败作为通过条件）。[matrix](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/.github/workflows/ci.yml#L55-L99)
- `[CI]` `launcher-windows` job 在 windows-latest 跑 `launcher.test.ts` + `package-contract.test.ts`、build、`node ./lib/bin.js --version`。[windows](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/.github/workflows/ci.yml#L101-L124)
- `[CI]` `scripts/stock-dsh-version.mjs` 把 CI 安装的官方 dsh 精确钉到 `package.json` 的 `dsh.compatibility.tested`，并要求 workspace overrides 全部等于该版本；即 **CI 只验证 0.2.0-rc.2**，0.2.1-rc.3 不在任何自动验收里。[pin](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/scripts/stock-dsh-version.mjs#L11-L26)
- `[CI]` `dsh-version-scan.yml` 每天 02:17 UTC 跑 `bump-dsh.mjs --check`，发现比 tested 新的 npm `latest` 就自动改依赖/基线、跑 `check`、在隔离 `DSH_HOME` 重跑契约，全过才开升级 PR。这是「moving tested pin」的唯一自动化路径，也是本快照仍停在 0.2.0-rc.2 的原因。[scan](https://github.com/Hilbert-beinghappy/seektty/blob/42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5/.github/workflows/dsh-version-scan.yml#L1-L91)
- `[CI]` 边界：workflow **存在**不等于该 commit 跑过、更不等于 0.2.1-rc.3 通过；本轮未查 Actions 运行记录。

## [RUN]

**范围**：只做只读 clone 与 registry/包元数据核对；未安装 seektty、未启动 dsh 目标 profile、未执行任何目标代码或测试。

- `[RUN]` `git clone https://github.com/Hilbert-beinghappy/seektty.git`；HEAD `42a2a7fa2a01b5a10a2e2ce368c151c8e0fdafc5`、`git rev-parse v1.3.0^{commit}` 同为该提交、`git describe --tags --exact-match HEAD` = `v1.3.0`、`git rev-list --count HEAD` = 290、工作区 clean。
- `[RUN]` npm registry：`seektty` 的 `dist-tags.latest = 1.3.0`，`time['1.3.0'] = 2026-10-13T06:10:31.520Z`，`modified = 2026-10-13T06:10:31.709Z`；版本列表尾部 `1.2.5, 1.2.6, 1.3.0`。
- `[RUN]` 取 `seektty-1.3.0.tgz` 核对发布物：`version 1.3.0`、`dsh.compatibility = {"minimum":"0.2.0-rc.2","tested":"0.2.0-rc.2"}`、`engines` 仅 Node、`peerDependencies` 67 项（其中 dsh 系 63 项全为精确 `0.2.0-rc.2`）、`files` 17 项。发布物与 tag 一致。
- `[RUN]` npm registry：`@deepseek-ai/dsh` 的 `latest = 0.2.1-rc.5`、`next = 0.2.1-rc.5`、`alpha = 0.2.2-alpha.2`；`0.2.0-rc.2` 发布于 2026-09-29T09:56:27Z，`0.2.1-rc.1/rc.2/rc.3` 分别发布于 2026-10-17/10-17/10-23。本机 `dsh --version` = `0.2.1-rc.3`。
- `[RUN]` 用 dsh 自带的 semver 计算：`satisfies('0.2.1-rc.3','0.2.0-rc.2',{includePrerelease:true}) === false`；`satisfies('0.2.0-rc.2','0.2.0-rc.2',...) === true`。
- `[RUN]` 从 npm 取 `@deepseek-ai/dsh-app-boot@0.2.0-rc.2` 的 tarball，确认 `evaluatePluginCompatibility` 以同样的 peer-only 语义存在（`lib/index.js:286` 起）——闸门不是 0.2.1 新增。
- `[RUN]` 本机安装的 `@deepseek-ai/dsh@0.2.1-rc.3` 中核对：`dsh-app-boot/lib/index.js` 导出表含 SeekTTY 用到的全部 profile helper；`dsh-plugin-manager/lib/index.js` 预检拒绝路径存在；`dsh/lib/bin.js` 的 `desktop` 独占与 `plugin` 透传存在。**未运行**这些命令。
- `[RUN]` GitHub REST（★/forks/issues）本轮未查询；卡片里的 194/22/8 与 npm 1,296 次下载保持旧快照口径，不作机制证据。

## 未核实与下一步

- `[OPEN]` **0.2.1-rc.3 上 `dsh plugin --profile tui add seektty@1.3.0` 的实际输出**：按代码应报 63 项 peer 不满足并 `nothing was installed`；需在一次性 `DSH_HOME` 里实测（不得碰现有 profile）。
- `[OPEN]` 已安装且豁免后，0.2.1-rc.3 上 `dsh --profile tui` 能否真正跑起 Surface：profile loader 只跳过/禁用不兼容行，但 0.2.1 的 `dropRetiredBundles`、Agent Preset schema、`commands/execute` wire 变化是否仍兼容，未实测。
- `[OPEN]` 未设 `SEEKTTY_NATIVE_TAIL=1` 时，原生模式在真实终端（尤其 tmux/screen）里的重绘边界：是否会整帧重放、是否会冲掉 scrollback，只能实机观察。
- `[OPEN]` `--update` 在「self 有新版本但 dsh 被 pin」与「pnpm 部分成功」两种情形下的用户可见结果；无回滚意味着坏包的恢复全靠手工。
- `[OPEN]` `default auto` 在每次启动前同步 spawn `pnpm add` 的最坏耗时，以及离线/registry 慢时的启动体感；3s 只是 fetch 超时，不含安装。
- `[OPEN]` `ProfilePluginManager.createUsableProfile()` 的「web → tui 转换」是否会留下 `@deepseek-ai/dsh-web-app` 的传递依赖或 preset 残留；代码只删直接依赖与 bundle 顺序项，未清理 lockfile。
- `[OPEN]` `host.describe` 占位符 `0.0.1` 的放行分支：SeekTTY 覆盖后一般拿不到该值，但若 dsh 入口解析失败会怎样（当前实现直接抛「Cannot locate the official dsh entry」），未实测。
- `[OPEN]` 卡片里的 ★/下载量与「npm 月下载 1,296」未复核；GitHub 未认证 API 易限流。

## 对卡片的净结论

1. **版本坐标要改**：样本 = SeekTTY `1.3.0`（tag `v1.3.0` = `42a2a7f…` = npm `latest`），声明宿主 `minimum = tested = 0.2.0-rc.2`；本线基线 `0.2.1-rc.3`，npm 最新 `0.2.1-rc.5`。不是「落后一个 rc」，而是跨了 0.2.1 整条预发布线。
2. **「高于已测可启动但提示」在本线不成立**：0.2.0-rc.2 已存在的 Host peer 闸门，63 个精确 `0.2.0-rc.2` peer 在 0.2.1-rc.3 上全部不满足 → 按代码路径安装会被拒绝 / bundle 被跳过 / 行被禁用。要么钉 0.2.0-rc.2，要么按精确版本 `allow-version` 豁免后自担风险；SeekTTY 自己的「新版本提示」只在豁免后才可能看到。
3. **更新器默认不是 `check`**：默认 `auto`，每次启动前检查并**安装**；`check` 是显式可选项，且只在 stderr 为 TTY 时事后提示。卡片 §0/§2.2/§3 都要改。
4. **「显式兼容区间」是退化区间**：实际只允许精确 tested 版本；`0.1.0-rc.8` 旧的 legacy 上界低于下限，是死代码。自动更新对 0.2.1-rc.3/rc.5 只会打印「不会安装」。
5. **没有回滚**：`--update` 与 auto 都不保存旧版本、不自动降级；「失败不阻塞启动」只对失败成立，成功但装坏只能手工回退（README 只给 1.2.6 的手工命令）。
6. **所有权口号要加限定**：「状态归 Harness」对 Agent/Session/Settings/凭据成立；但 bundle patch 禁用了 25 个宿主行、自带 3 套 Agent Preset 并设定 `default: standard`，所以**能力装配（尤其工具目录与默认预设）不归 Host 自动发现**。卡片「第 5 层不抢」应改为「不抢模型默认与权限状态，但抢预设/工具组合」。
7. **Profile 写入比卡片承认的多**：`/plugin` 直接跑 pnpm + 用宿主 manifest 工具写 `dsh.profile.bundles`，`/profile` 还能克隆/转换 profile。README 的「不在原生 reconciliation 外改 manifest」应细化为「用宿主同一套 manifest helper，但决策在 SeekTTY」。
8. **pnpm 11 适配的机制成立**：局部参数、只在自发起变更上、不改全局配置、双条件识别已知失败、launcher 在非 0 退出且自身处于 GVS 布局时给恢复命令；CI 对 GVS 开启态甚至接受「精确已知失败」。这是可抄的部分；代价是恢复建议依赖 profile spec 可读。
9. **原生 scrollback 要分两层写**：模式本身（F3/`/mouse`、settings 持久化、仅空闲、顺序补载 + 进度、Esc 只停补载、退出 alt screen、关鼠标上报、冻结非动态块）是实装；「已写历史绝不重绘/只刷尾部」的增量路径要 `SEEKTTY_NATIVE_TAIL=1`，属 opt-in。卡片应明确这条分界。
10. **teardown 是本卡漏掉的长处**：同步恢复 + 2s 有界清理 + fatal/suspend guard + 单次、0600、24h 清扫的重启交接，值得单独列为可抄机制；`[OPEN]` 只在真实终端与真实会话下验证。
11. **Clarify 15 分钟不是本 Bundle 的 TTL**：它是可选 companion 插件的 Host 内存状态，SeekTTY 只消费 `stale`/`ttl-expired` 状态并给出口。卡片的表述应注明归属。
12. **发布物可信度较高**：npm 1.3.0 与 tag/HEAD 同版，CI 有 `lib/` 与源码同步检查、stock dsh 生命周期、GVS 双态矩阵；但 CI 只钉 0.2.0-rc.2，242 个测试本轮未运行——所以只能说「有覆盖意图与发布纪律」，不能说「0.2.1 已验证」。
