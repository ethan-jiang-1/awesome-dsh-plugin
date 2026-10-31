---
title: "内置运行时 · dsh-desktop-tauriapp"
domain: reshape-product
kind: sample
positioning: "`dsh-desktop-tauriapp@0.12.0`：安装包带 Node sidecar 与 dsh 0.2.0-rc.2 依赖树；无 lock、无自动回滚、无自动更新，sidecar 缺失会回退 PATH node。"
takeaway: "内置运行时只是打包属性；依赖树无 lock 不可复现；健康探测单次 TCP 失败即重启、3 次封顶、120s 连续健康才清零。"
read_when: "要做零前置依赖的桌面壳；或要设计运行时版本管理与多 profile 多窗口。"
status: observed
updated: 2026-10-31
budget: 180
---
# 内置运行时 · dsh-desktop-tauriapp:把运行时一起打包

> **研究范围**：`dsh-desktop-tauriapp` tag `v0.12.0` → commit [`2c4ba10`](https://github.com/hyperion2144/dsh-desktop-tauriapp/commit/2c4ba10e29278184424ae56a1ec02d0f45de8ea3)，源码复核按 HEAD [`577a6d3`](https://github.com/hyperion2144/dsh-desktop-tauriapp/commit/577a6d3ac95aeb956e7bb8134efb574294ea63d2)（比 tag 多 4 个提交）。内置运行时 pin 为 **`0.2.0-rc.2`**，不是本机 CLI 的 0.2.1-rc.3。只读，未安装/构建/运行。详见[`05 源码复核`](./_证据/05_内置运行时-tauriapp-源码复核.md)。
> **类**:`1` 壳与工作台 · **层**:2(表层)+ 5(默认值)+ 6(首启)+ 7(分发) · **★ 1 / open issues 25**(GitHub API,2026-10-31)
> **一句话**:它是三条宿主路线里**最"自成一体"的一条**:Node sidecar + dsh 依赖树随包分发,**双击即用、零前置依赖**,并且把"运行时版本"做成应用内的可换件。
> **借鉴价值**:**① 内置运行时把"装 Node / 装 dsh / 配 PATH"三个失败点一次性消掉;② 健康探测是**连接级**的(TCP 连不上才算异常),不靠进程存在;③ 自愈要**封顶 + 冷却重置**(3 次封顶,持续健康 ≥2 分钟才重置);④ 桌面 chrome **局部注入**,不禁用 stock `ui-layout`;⑤ 依赖状态**只提示、不自动重建**(#124 的教训)。**

> **证据成熟度**：打包资源映射、内置版本 pin、启动路径、健康/自愈与运行时管理为固定源码 `机制参考`；发布产物是否含该树、sidecar 补丁版本、真实崩溃恢复与签名/更新均未验证，无 `[RUN]`。
> **影响力**：机制例外——唯一的"内置运行时"样本，证明这条路线可行（门槛见 [`00-map` §7](../00-map.md)）。

> **样本档案**
> **repo**:[`hyperion2144/dsh-desktop-tauriapp`](https://github.com/hyperion2144/dsh-desktop-tauriapp) · **npm**:`dsh-desktop-tauriapp`(插件半区) · **许可证**:GitHub API 报 `NOASSERTION`(仓库内有 LICENSE,读前先核)
> **目录条目**:`data/plugins/hyperion2144__dsh-desktop-tauriapp.yml`(`ui`)
> **装法**:`dsh plugin add dsh-desktop-tauriapp` / `dsh plugin add github:hyperion2144/dsh-desktop-tauriapp`(插件半区);**应用本体**从 Releases 下 dmg/msi
> **产物**:macOS `.app/.dmg`、Windows `.msi/.exe`;`desktop/` 是 Tauri 2 壳(Rust);`mobile/` 还有 Expo/鸿蒙手机壳
> **血缘**:fork 自 `happpsee/dsh-desktop-app`(后者 `downloads.json` 快照 352)
> **已在本地挖掘**:[`../_证据/01_桌面与终端-原始挖掘.md`](./_证据/01_桌面与终端-原始挖掘.md) §二.3
> **再深挖去哪**:`desktop/scripts/prepare-builtin-runtime.mjs`、`desktop/src-tauri/tauri.conf.json`、`docs/windows-audit-report.md`

---

## 它想干什么 · 为什么值得借鉴

**意图。** 把“装 Node / 装 dsh / 配 PATH”三个失败点一次性消掉：安装包里带 **Node 24 sidecar + dsh 依赖树**，启动走内部 API 代码路径而不是 shell out 到 CLI，内置版本由 `BUILTIN_DSH_VERSION` pin 到 `0.2.0-rc.2`。它交付的单位是**一个自带运行时的安装包**，并把“运行时版本”做成应用内可换件（下载 / 切换 / 卸载，源可选 github / npm）。有两件它明确不做：不自动重建依赖（#124 起只提示），也不接管 stock `ui-layout`；此外**没有自动回滚**（结构有效但启动即崩时只停自愈）与**没有自动更新通道**。

**意义。** 这是本线唯一的“内置运行时”样本，★ 只有 1，却证明这条路可行，也顺手回答了代价问题：macOS dmg ~200 MB、Windows msi ~240 MB。它改的边界是**兼容性责任**——钉死运行时等于承诺“这一版 dsh 与这一版壳一起验过”，把散落在用户机器上的版本不确定性收回产品侧。它同时是一根探针：`desktop` 这个 profile 名被上游判给官方 Electron 应用，CLI 三条路径全部拒绝，它能跑是靠 launcher 直调内部 `runProfile`、用自有参数 `--init-from-default` 从 `web` 模板初始化。

**用户价值。** 装之前，用户要自己解决 Node 版本、npm 全局权限、PATH 和 dsh 版本；装之后，双击 dmg/msi 直接是完整界面，插件需要另一个 dsh 时在托盘的“运行时版本”里切一下，不必重装应用。感到“值”的是拿不到安装权限的机器（受控环境、设计/运营同事）和装了很多插件的重度用户。代价由两边分担：包体积 200–240 MB、macOS 非公证包要右键打开、Windows 过 SmartScreen；更要紧的是它会在 `$DSH_HOME/profiles/desktop` 建 profile，与官方桌面应用同名同目录，上游一收紧就得改。

**表达（界面与交互）。** 第一屏是安装包→双击→完整界面，中间没有“请先安装 Node”这一步；等待被做成**可看的**：加载页实时显示子进程 stdout/stderr，可展开、收起、清空。日常是多窗多 profile，托盘按 profile 分组、可就地切换本窗口的 profile，而不是再开一个窗；关窗收托盘。克制的部分最见取舍：只在有会话在跑时持系统断言，**屏幕照常熄灭**，等审批/等输入不持有；依赖不一致只在启动时提示、不代修；macOS 用 `titleBarStyle: Overlay` 留住原生红绿灯，Windows 才自绘按钮，桌面 chrome 走插件式局部注入而不动 stock 布局。

## 0. 一页速览(想抄的人只看这 20 行)

| 问题 | 它的答案 | 支撑 |
|---|---|---|
| 前置依赖 | **零**:Node 24 sidecar + dsh 依赖树随安装包分发 | `[OBS]` §主要看点 |
| 怎么启动 dsh | 走**内部 API 代码路径**,不是 CLI;也可切外部 `DSH_BIN` → PATH → npm 全局 | `[OBS]` §特性 |
| 版本怎么钉 | `prepare-builtin-runtime.mjs` 顶部 `BUILTIN_DSH_VERSION` **精确 pin**;pnpm 也精确 pin | `[OBS]` §从源码构建 |
| 能在应用内换运行时吗 | 能:下载 / 切换 / 卸载;源可配 **github / npm**;托盘有「运行时版本」子菜单 | `[OBS]` §特性 |
| 健康判据 | **连接级**:TCP 连不上才判异常;异常 → 回启动页重建 | `[OBS]` |
| 自愈上限 | **3 次封顶**;持续健康 **≥2 分钟** 才重置计数;复用外部/远程实例**只提示不代拉** | `[OBS]` |
| 多 profile | per-profile 端口：web=3080、desktop=3081，其余用确定性散列（不写 settings；只有显式覆盖才持久化）；托盘按 profile 分组 | `[SRC-TARGET]` |
| 默认 profile | 全新安装默认 **`desktop`**;它**不是出厂模板**,经 `--from-default-profile` 初始化 | `[OBS]` |
| 桌面 chrome | **插件式局部注入**:在标准布局内加拖拽区/状态条,**不禁用 stock `ui-layout`** | `[OBS]` |
| 标题栏 | macOS `titleBarStyle: Overlay`(保留原生红绿灯);Windows `decorations:false` **自绘** | `[OBS]` |
| 快捷键 | 页面里装原生键盘桥 `dshDesktop.keyboard`,按官方 `desktop:<os>` 档派发 | `[OBS]` |
| 防休眠 | 有会话在跑才持系统断言(macOS `IOPMAssertion` / Windows `SetThreadExecutionState`);**屏幕照常熄灭** | `[OBS]` |
| 依赖对不上 | 面板列出各 profile 的 pnpm / 内置版本 / 是否需重建;**启动只提示,#124 起不自动重建** | `[OBS]` |
| 启动可见性 | 加载页实时显示子进程 stdout/stderr,可展开/收起/清空 | `[OBS]` |
| 最该抄的一句 | "**连接级健康探测(连不上才判异常)**" | `[OBS]` |

## 1. 它在产品里的位置

**七层坐标**:**2**(表层:独立窗口 + 托盘 + 自绘标题栏)+ **5**(默认值:全新安装默认走它自己的 `desktop` profile)+ **6**(首启:内置运行时,双击即用)+ **7**(分发:安装包 + 运行时下载/切换 + 更新)。

**它和上游的缝**:它**试图占用 `desktop` 这个 profile 名**,并声称"`desktop` 非 dsh 出厂模板,经 `--from-default-profile` 初始化"。但当前上游把 `desktop` 判给**官方 Electron 应用**(`lib/bin.js:35-37`),且 `--from-default-profile` 只接受**出厂模板名**(`lib/profile-boot-C14i-8IN.js:154`)。**这条冲突是本卡最重要的发现**——见 §4 与 §6。

## 2. 机制(可照抄)

### 2.1 内置运行时:把三个失败点一次消掉

- 安装包里带 **Node 24 sidecar + dsh 依赖树**,启动走**内部 API 路径**(不 shell out 到 CLI);
- 内置版本**精确 pin**(`BUILTIN_DSH_VERSION`),本地与 CI 用同一套准备脚本 → 可复现;
- 也可切**外部 dsh**:`DSH_BIN` → PATH → npm 全局;
- 应用内可**下载 / 切换 / 卸载**运行时版本(源 github / npm),托盘里"已装点击即切,未装点击 = 下载→自动切换",全程系统通知反馈。

> **照抄点**：内置运行时是把兼容性责任拿回来，但“零前置依赖”只是发布包属性：sidecar 缺失会回退 PATH 上的 node，依赖树用 `npm install --no-save` 无 lock、Node 取 `latest-v24.x` 浮动，因此不能声称同 commit 可复现。

### 2.2 进程守护:连接级健康 + 封顶自愈

```
每 tick:TCP 连不上 → 判异常 → 回启动页重建
                                   ├─ 连续 3 次 → 封顶(不再自愈)
                                   └─ 持续健康 ≥2 分钟 → 计数清零
复用外部 / 远程实例 → 只提示,不代拉
```

- 判据是**连接**而不是"进程还在"(僵尸进程会被识别);
- 自愈**计数 + 冷却**:既不会无限重拉,也不会一次偶发抖动就把额度用光;
- 对"不是自己拉起的"实例**只提示**。

> **照抄点**:健康检查的**观测点**要贴近用户感知(连不上),而不是贴近实现(进程存在)。

### 2.3 多 profile 多窗口:端口是确定性散列 + 显式覆盖

- `web=3080`、`desktop=3081`,其余**散列分配并持久化**;设置页可改;
- 托盘按 profile 分组:聚焦已有窗口 / 新窗打开 / **就地切换本窗口 profile** / 新建 / **全量迁移 A→B**;
- 迁移时要**排除锁与临时文件、符号链接感知、覆盖前备份**;
- 还有一个 **lane 反代**:3091 稳定入口指向**焦点窗口**,手机侧零改动。

> **照抄点**:多实例不是"多开窗口",是**端口 + profile + 窗口**三者的映射表。切换 profile 要能**就地**,否则用户会开出一堆窗。

### 2.4 桌面 chrome:局部注入,不接管布局

- 由内置插件的 client 在**标准布局内**注入拖拽区/状态条,**不禁用 stock `ui-layout`**;
- macOS 用 `titleBarStyle: Overlay` 保留原生红绿灯;Windows 用 `decorations:false` 自绘按钮;
- 配色走主题 token。

> **照抄点**:能"加一层"就不要"换一层"。**局部注入的失败模式是退化,整体替换的失败模式是白屏。**

### 2.5 键盘桥:壳不吞键

- 壳在页面里装 `dshDesktop.keyboard`,把原生键盘事件送给 dsh;
- dsh 按官方 `desktop:<os>` 档派发快捷键;
- 改绑偏好存 `$DSH_HOME/desktop-keybindings.json`,即时生效。

> **照抄点**:WebView 天然吞键。壳要么**把键还给页面**,要么承认自己吃掉了一部分交互。

### 2.6 防休眠:只在"真的在跑"时持有

- 任一窗口有会话在跑 → 持系统级断言;
- **等待审批/等待输入不持有**;会话结束 / 关窗 / 退出立即释放;
- **屏幕仍照常熄灭**。

> **照抄点**:区分"应用醒着"与"屏幕亮着"。持断言的范围要**精确到会话运行期**,不是应用生命周期。

### 2.7 依赖自检:只提示,不代修

- pnpm store 大版本必须与 profile 的 `node_modules` 一致;
- 面板列出每个 profile 的 pnpm / 内置版本 / 是否需重建;
- 启动时后台检查,**不一致只弹提示**;**#124 起不再自动重建**(运行中禁重建)。

> **照抄点**:自动修复依赖 = 在用户不知情时改他的环境。**提示 + 手动重建**是更慢但更安全的默认。

## 3. 体验

- **第一次**:装 dmg/msi → 双击 → 直接是完整界面(没有"先装 Node");托盘里可看"运行时版本"。
- **日常**:多 profile 多窗;关窗收托盘;会话跑着时系统不休眠,屏幕照常黑。
- **更新**:运行时与应用各自可换;换运行时走"下载 → 切换",有系统通知。
- **出错**:加载页能看子进程输出;依赖不一致会提示重建。

## 4. 证据与边界

- **影响力**:**★ 1 / open issues 25**(GitHub API 2026-10-31)——**本 lever 里影响力最弱的样本**,但它有**最独特的机制**(内置运行时 + 运行时版本管理),按本线"机制独特可例外"的口径成卡,并在标题里标明。
- **血缘**:fork 自 `happpsee/dsh-desktop-app`(下载快照 352),说明这条"内置运行时"路线至少有两代实现。
- **机制证据**:README 全文(2026-10-31 抓取);摘录见 [`../_证据/01_桌面与终端-原始挖掘.md`](./_证据/01_桌面与终端-原始挖掘.md) §二.3。
- **口径警告**:★ 1 只说明社区可见度极低，**本卡不足以证明"内置运行时"是主流选择**，只能证明它可行。
- **已实测（2026-10-31）**：上游 CLI **三条路都拒绝 `desktop`**——`dsh --profile desktop --dump-config`、`dsh plugin --profile desktop add …`、以及加 `--from-default-profile web`，全部返回 `error: profile "desktop" is managed exclusively by the Electron application`。它能跑，是因为 launcher **直调内部 `runProfile` API、不经 CLI**（`desktop/src-tauri/src/runtime/builtin/launcher.mjs:1`），并用自有参数 `--init-from-default` 从 `web` 模板初始化（同文件 :25）。**代价**：它会在 `$DSH_HOME/profiles/desktop` 建 profile——与官方 Electron 应用**同名同目录**。

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 用户机器缺 Node/DSH，装不起来 | 把运行时作为随包资源（依赖树+sidecar）分发，首次运行不下载、不解压。 | `[SRC-TARGET]` resources/dsh + externalBin dsh-node；builtin.rs 直接读资源目录。 | 消除前置安装失败点；代价是 200–240MB 体积与每版运行时同步。 | 定义资源映射、启动器写盘位置、sidecar 查找顺序与缺件回退。 | 仓库 gitignore resources/binaries，不能证明发布产物实际含该树。 | 假定“零依赖”是代码不变量 → sidecar 缺失时静默跑系统 node。 |
| 运行时要跟 DSH 版本走 | 把内置版本 pin 成常量，并在 UI 显示；升级应用=升级运行时。 | `[SRC-TARGET]` `BUILTIN_DSH_VERSION=0.2.0-rc.2`；launcher 传 profile/bundles。 | 版本可预期；代价是应用与插件生态版本耦合。 | 固定 dsh+pnpm+node 三个坐标，并保存构建产物清单。 | 依赖树用 `npm install --no-save` 无 lock；Node 取 `latest-v24.x` 浮动；不可复现。 | 声称“同一 commit 可复现” → 每次构建依赖树不同。 |
| 启动/health 失败要自愈 | 对主实例做连接级探测（TCP），失败重启并设累计上限与健康冷却，避免无限重启。 | `[SRC-TARGET]` 5s tick、TCP 2s timeout、单次失败即重启、3 次封顶、120s 连续健康清零。 | 快速恢复；代价是只覆盖主实例/远程地址，次窗无守护。 | 定义探测对象、失败阈值、封顶计数、冷却和“重启会杀谁”。 | 重启前 `stop_port_owner` 会杀占用端口的任何监听者。 | 把“3 次”当连续失败阈值 → 实际是累计自愈失败计数。 |
| 多个 profile/窗口需要稳定端口 | 用确定性散列分配端口，冲突避让；只有用户显式覆盖才持久化。 | `[SRC-TARGET]` FNV-1a%512+3082；Rust 注释明确不写 settings；显式改端口经 client→settings 落盘。 | 重启稳定、无需状态；代价是端口可能与其它服务冲突。 | 定义散列输入、冲突策略、显式覆盖的持久化 owner。 | 不是“端口持久化到设置”；跨启动稳定靠散列确定性。 | 以为端口写在配置里 → 手改/迁移后行为不符。 |
| 运行时下载/切换/卸载 | 用内置 node+pnpm 在 app_data 重建依赖树；切换写设置并重启；卸载 rename 到 .trash 后清理。 | `[SRC-TARGET]` registry/commands；下载失败清半成品。 | 无需外部工具；代价是无 lock、无 hash/签名、无自动回滚。 | 加校验（hash/签名）、lock、事务与回滚策略。 | 结构有效但启动即崩不会自动退回；无应用自动更新。 | 把“可换版本”当“可安全回滚” → 坏版本留在设置里。 |
| 桌面权限与签名 | 最小 capability + 明确信任边界；发布包签名/公证。 | `[SRC-TARGET]` default capability 无 shell/fs/http；remote capability 对 loopback 放行大量命令；withGlobalTauri+csp null；macOS ad-hoc、无公证。 | 功能可用；代价是攻击面与 Gatekeeper/SmartScreen 摩擦。 | 收紧 remote capability、恢复 CSP、配置签名与公证。 | 本卡未做渗透/签名验证。 | 把“没有 shell 插件权限”当无危险 → loopback 页面可调大量命令。 |
## 6. 失效条件与降级

- **profile 名冲突**(§4):若上游继续收紧 `desktop`,它必须改 profile 名或改走"自带 profile 向导"。
- **包体积**:内置运行时让安装包到 200–240 MB 量级,小水管用户下载成本高。
- **外部实例**:复用外部/远程实例时它"只提示不代拉",等于把健康责任交回用户。
- **依赖不一致**:只提示不自动重建 → 用户可能长期带着不一致的 store 跑。
- **签名**:README 提到 macOS 非公证包需右键打开、Windows SmartScreen——与"零前置依赖"的体验承诺有落差。

## 7. 开放问题

- [ ] `[OPEN]` 同机安装**官方桌面应用**后，两者对 `profiles/desktop` 的覆盖顺序与损坏面——本卡只证明"同名同目录"，未实测共存。
- [ ] `[OPEN]` 内置运行时与**外部插件**的兼容边界:插件按外部 dsh 的 peer 声明装,内置版本不同时谁负责?
- [ ] `[OPEN]` 它同时带 `mobile/` 手机壳,桌面 + 手机是否共享同一套配对/反代(lane 3091)在文档里只有一句。
- [ ] `[OPEN]` 迁移 profile(A→B)的"覆盖前备份"存在哪、怎么回滚,README 未写。
