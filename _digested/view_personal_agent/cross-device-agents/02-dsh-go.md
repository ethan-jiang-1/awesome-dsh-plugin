---
kind: card
domain: personal_agent
subcategory: cross-device-agents
repo: ccch1mneyyy/dsh-Go
commit: 3b9fbbbb5953ad1afc383ddec16bd63bc02c3442
evidence: 3
status: active
asof: 2026-11-27
---

# dsh-Go — 33,066★ 口袋里的真 DSH 引擎 + 原生 Kotlin SafetyGate + Noise_IK 远控双模标杆

> 证据等级 ★★★(源码级;`ccch1mneyyy/dsh-Go@3b9fbbbb`)。未在真机运行或编译 266 份补丁;本地 Ubuntu/PRoot/Node 打包流程、`dsh-go-bridge`、SSH/Noise_IK 双远控、Kotlin `SafetyGate` 硬拒表与默认遥测行为均经源码逐文件核验。
> **未收录于 `awesome-dsh-plugin` 注册表**(独立移动 App 分发,同作者的 `dsh-TUI` 在 `view_ui`,本仓为移动端真 DSH 宿主)。星标 **33,066★ / 1,599 forks** 与单版 APK 下载近 10 万(`v1.3.0`:98,436)均为 2026-11-27 GitHub API 实测值。

## 它替谁解决什么问题

**想在一部随身手机上同时拥有“免 Root 免 Termux 本地跑真 DSH(可真装 npm 插件、跑 Python/Node、控手机 App)+ 随时端到端加密遥控家里电脑/服务器 DSH”全套个人随身 Agent 的移动端用户。** 现有移动方案的痛点很明显:

- **纯远程控制 App 断网或关电脑就废**:离了家里主机既查不了笔记也跑不了脚本,更操控不了手机本机应用。
- **纯套壳聊天 App 丢失完整 DSH 插件生态**:不能跑真实 `dsh plugin add`、`AGENTS.md`、本地文件系统技能与定时任务。
- **手机端操控 App 极怕提示注入刷银行卡或点确认键**:如果审批逻辑放在 LLM 或同一沙箱里,网页/聊天里的恶意文案能诱导 Agent 自己点“允许”甚至打开支付宝/网银。

`ccch1mneyyy/dsh-Go` 在安卓端把完整 Ubuntu 24.04 + Node 24.22.1 + pnpm 11.28.5 + Python 3.12 + 经 266 份补丁适配的 `@deepseek-ai/dsh@0.2.2-rc.1` 塞进单 APK,在原生 Kotlin 层(LLM 与 PRoot 之外)架起硬拒 29 款金融 App 与自身界面的 `SafetyGate`,同时支持免装本地 1 GB 运行时直接经 SSH(TOFU)或 `ds-harness-remote`(真 `Noise_IK` E2EE)遥控电脑。

## 适用面:谁该用、谁别用

- **适合**:希望一部手机通吃「随身本地完整 DSH(能装 npm 插件/跑脚本/语音 VAD/控手机)+ 端到端加密遥控 PC/VPS」的 Android 用户(可侧载 233 MB APK 并接受 ~1 GB 解压空间);只用纯远控模式(不装本地 1 GB 运行时)的用户;以及想用 MIT 协议 `sdk/plugin-kit` 为 DSH 插件提供原生移动卡片界面的插件作者。
- **不适合**:**对遥测零容忍的绝对隐私用户**——源码实锤 `UsageStatsState.enabled` 默认为 **`true`**,且**即便在安卓端关闭“发送匿名使用统计”,v4 日账本仍会继续向 `https://go.dshtui.com/api/usage/v1` 发送不含内容的匿名日活心跳**(`app/lib/usage/usage_stats.dart:4-6,129-134,152-154`, `docs/guide/zh/11-faq.md:115`),外加默认启用的 Google ML Kit OCR 自带 Google SDK 遥测;**iOS / 鸿蒙开箱即用用户**(均只有未签名 `.ipa`/`.hap` 需自签,iOS 默认无真 Linux,鸿蒙不能 exec 二进制且无读屏控手机);以及想低成本魔改分发的商业团队(**`AGPL-3.0`** 主许可 + 品牌/吉祥物资产全权保留不开源,`ASSETS.md:1-25`)。
- **前置条件**:Android 侧载(非 Google Play),本地模式需约 1 GB 存储 + OEM 后台电池白名单;远控 `ds-harness-remote` 模式需电脑侧安装对应插件(且该模式下仅支持图片附件、不支持远程装插件或 DS Bot)。

## 业务价值

- **能算清的**:
  - **DSH 个人移动生态现象级声量与分发**:**33,066★ / 1,599 forks / 1,038 open issues**(2026-11-27 实时值,2026-10-25 建仓仅 1 个月);GitHub Releases 历史三版 APK 实测下载量分别为 `v1.1.0` **93,334**、`v1.2.0` **77,115**、`v1.3.0` **98,436**(`v1.4.1` 11-27 刚发,含 25.5 MB 增量差分包 `.dshdelta`)。
  - **最严手机操控硬件/原生层安全底线**:原生 Kotlin `SafetyGate` 硬拒绝自身 App(防自点确认)+ **29 款银行/支付/券商 App**(支付宝/云闪付/数字人民币/工农中建招/富途等,读写全禁)+ 系统设置/权限页禁写 + 密码/OTP/支付框禁写 + 微信每次写操作逐次确认,且**在任何手机任务执行期间禁止放宽规则**(`SafetyGate.kt:44-70,140-173`)。
  - **真客户端 E2EE 分享与远控**:`ds-harness-remote` 实现 `Noise_IK_25519_ChaChaPoly_SHA256` + 严格单调 nonce 防重放;云端分享链接采用 `AES-256-GCM(gzip)` 且密钥只放 URL `#k=` 片段(`hosted_crypto.dart:1-54`)。
- **只是预期(推断)**:
  - 实验性 `Direct glibc` / `tawcroot`(提速约 3 倍)与 2 次启动失败自动进安全救援模式可能大幅改善手机跑 PRoot Linux 的体验,但实机跨芯片/跨 ROM 崩溃率未做独立实测。

## 一屏事实

| 项 | 值 |
|----|----|
| 仓库 / 注册状态 | `ccch1mneyyy/dsh-Go`(**未收录于 `awesome-dsh-plugin`**,独立移动 App 宿主;同作者 `dsh-TUI` 在 `view_ui`) |
| 子分类 | `cross-device-agents`(跨设备与随身个人 Agent) |
| 自述 | 口袋里的真 DSH:安卓/iOS/鸿蒙本地运行完整 DSH 引擎 + 手机操控 + SSH/DSH Remote 端到端加密遥控电脑 |
| 星标 / 下载(2026-11-27) | **33,066★ / 1,599 forks**;单版 APK 下载近 10 万(`v1.3.0`:98,436;创建 `2026-10-25`,push `2026-11-27` `v1.4.1`) |
| 包形态 / 许可 | Android APK(233.4 MB)+ 未签名 iOS IPA(129.7 MB)/OHOS HAP(125.3 MB);主体 **`AGPL-3.0`**(`sdk/`/`dsh-go-bridge`/`dsh_remote` 为 MIT;品牌/吉祥物资产**全权保留**) |
| 代码规模 | `app/lib` 50.8 万行 Dart + `app/test` 2,638 套件 35.8 万行 + `android` 7.37 万 Kotlin + `dsh_client` 8.9 万 + `dsh_tavern` 25 万 + **266 份 `.diff` 补丁(23,488 行)** |
| 宿主钉版 | 精确 SHA-256 锁定 **`@deepseek-ai/dsh@0.2.2-rc.1`** + Ubuntu 24.04.5 + Node 24.22.1 + pnpm 11.28.5 + Python 3.12.15 |
| repo@commit | `3b9fbbbb5953ad1afc383ddec16bd63bc02c3442`(2026-11-27 +0800) |
| 证据等级 | ★★★ |

## 它到底是什么

**一台把完整 DSH Web 运行时与双模加密远控塞进 Flutter 三端外壳的“超级口袋宿主”。** 它既是手机上的本地个人 Agent 电脑,也是家里电脑的加密遥控器,底层共享同一个 `DshClient`:

```text
Flutter UI(50.8 万行 Dart / 语音 ONNX+Silero VAD / 原生插件卡片 / 酒馆引擎)
  ├─ 本地引擎(Android):PRoot / Direct glibc / tawcroot → Ubuntu 24.04 + Node 24.22 + pnpm + 真 DSH 0.2.2-rc.1(266 补丁)
  │    ├─ dsh-go-bridge(/dsh-go/v1/* + 路由守卫) + 本地插件市场安装(dshfind) + 2 次失败进 Safe Mode
  │    └─ phone MCP → relay.cjs → 抽象 Unix Socket → Kotlin McpServer + 原生 SafetyGate(硬拒 29 金融 App/自身/密码框)
  └─ 远程 PC/VPS(免装 1 GB 本地包):
       ├─ SSH(vendored dartssh2 + TOFU 主机指纹锁死 → 隧道直连远端 127.0.0.1 dsh web)
       └─ DSH Remote(Noise_IK_25519_ChaChaPoly_SHA256 E2EE over WebRTC DataChannel / Relay)
```

需要明确区分:**“手机本地跑”指的是 DSH 引擎、工具、Shell、技能、插件与记忆全部跑在手机上,模型推理仍调用远程 API 提供商**(`README.md:174,219`)。

## 怎么接进 DSH

1. **SHA-256 精确锁定的 266 份上游补丁(`runtime/build-runtime.sh:12-91`, `runtime/patches/{series,pins.json}`)**:对 `@deepseek-ai/dsh@0.2.2-rc.1` 逐文件校验 `before`/`after` SHA-256 打入 266 份 `.diff`(23,488 行),含全局回环路由守卫补丁 `route-guard.diff:42-67`(强制每个命名 HTTP/WS 路由过 `connection.requestRejection`,未就绪直接 503 fail-closed)。
2. **`dsh-go-bridge` 与本地 Phone MCP 叠加 Patch(`runtime/bridge/dsh-go-bridge/`, `PhoneGuest.kt:8-250`)**:启动 `dsh web` 时叠加 `/etc/dsh-app/dsh-web.patch.yml` 与 `/opt/dsh-app/phone/phone.patch.yml`,通过 `@deepseek-ai/dsh-mcp-client` 连向 Kotlin `McpServer`(凭据写 `0600` `bridge.json`,带会话/调用溯源元数据)。
3. **三端插件生态兼容**:自带 `pnpm 11.28.5` 可直接在手机上装标准 DSH npm 插件(带 `approvedBuilds` 构建脚本确认);未适配插件走内嵌 Web 视图,实现 `ctx.inject(['dshGo'])` + `sdk/plugin-kit` 的插件渲染原生 Flutter 卡片。

## 关键实现

| 模块 | 位置 | 作用与源码实证 |
|---|---|---|
| 原生 Kotlin `SafetyGate` 硬围栏 | `app/android/.../phone/SafetyGate.kt:8-350` | 运行在 LLM/PRoot 之外防屏幕提示注入;即便开“免确认(`ALWAYS`)”也硬拒自身包(`OWN_PACKAGE`)、29 款银行/支付/券商 App(`DEFAULT_DENY`)、系统设置/权限页禁写、密码/OTP 框禁写;微信每写必问;**任务运行期间禁止放宽任何规则**(`lifts() && busy()` 拒绝);`android_shell` 独立逐条确认不继承免确认 |
| 安卓三模本地启动与救援 | `app/android/.../runtime/DshProcess.kt:21-288` | 支持 PRoot(默认兼 Safe Mode)/Direct glibc(含 `L2sMigration` 伪硬链迁移)/`tawcroot`(提速约 3 倍);注入自定义 `NODE_OPTIONS` DNS 解析修补 PRoot glibc AAAA 拒答 bug;2 次启动失败自动进无三方插件的 Safe Mode |
| 真 E2EE 双远控通道 | `packages/dsh_remote/lib/src/{crypto/noise_ik.dart,channel/secure_channel.dart}`, `app/lib/remote/ssh/ssh_link.dart` | `Noise_IK_25519_ChaChaPoly_SHA256` + 12 位十六进制主机指纹固定(`RelayTrust.keyChanged` fail-closed)+ 严格递增 nonce 校验(乱序/重复即断连);SSH 隧道锁 TOFU 指纹并伪装 `Host: 127.0.0.1:<port>` 过远端 DSH 围栏 |
| 回环路由总闸 | `runtime/patches/route-guard.diff:42-67`, `dsh-go-bridge/lib/index.js:180-239` | 除精确 `/connect` 与 `/oauth/callback` 外,所有命名 HTTP/WS 路由必须通过 `connection.requestRejection`,并对未打补丁远端主机提供 monkey-patch 兜底 |
| 客户端 E2EE 分享与凭据库 | `app/lib/share_hosted/hosted_crypto.dart:1-54`, `app/lib/secrets/secure_storage.dart:25-33` | 分享链接客户端 `AES-256-GCM(gzip)` 加密(20 MB 上限、64 MB gzip 炸弹限),32 字节密钥仅放 `#k=` 片段服务端不可见;密钥存 `FlutterSecureStorage` |
| 遥测与安卓不可关 DAU 心跳 | `app/lib/usage/usage_stats.dart:1-7,34,129-154`, `usage_net.dart:21` | `UsageStatsState.enabled` 默认 `true` 发往 `go.dshtui.com`;**关掉开关后安卓端 `observesDaily` 仍为 `true`,v4 账本继续发不含内容的匿名日活 ping** |

## 为什么它突出

只用本仓库自身证据:

- **DSH 生态绝对断层的移动端体量与工程完成度**:33,066★、单版 APK 近 10 万下载、50.8 万行 Flutter + 2,638 测试套件,还配齐了 25.5 MB `.dshdelta` 差分更新与 2 次崩溃 Safe Mode。
- **`SafetyGate` 是目前 DSH 生态手机操控最硬的原生外置安全门**:把金融 App 黑名单、禁点自身确认键、任务忙时锁死规则放宽全放在 LLM 触及不到的 Kotlin 层,直接可作为其他手机 Agent 的安全基准。
- **真正同时跑通“手机本地真插件生态 + 端到端加密远控电脑”**:既能在手机里跑真 `pnpm` 装 DSH 插件,也能在无本地运行时下经 `Noise_IK`/SSH 遥控电脑。

## 代价与边界

1. **源码实锤隐私边界(默认遥测 + 安卓不可完全关闭 DAU)**:`usage_stats.dart:4-6,129-154` 证实即便用户关闭统计开关,安卓端仍持续发送 v4 匿名日活 ping 至 `go.dshtui.com`,且默认启用的 ML Kit 中文 OCR 独立上报 Google SDK 遥测(`docs/guide/zh/11-faq.md:115,122-124`)。
2. **极重的上游补丁债**:维护 **266 份 `.diff` 补丁(23,488 行)** 按 SHA-256 精确钉死 `@deepseek-ai/dsh@0.2.2-rc.1`,每升一次宿主 RC 都是重度 rebase 工程。
3. **跨平台能力严重不对称与分发门槛**:仅安卓提供完整签名 APK(233 MB 侧载 + ~1 GB 解压空间 + 电池白名单);iOS/鸿蒙均未签名且缺失真 Linux 或屏幕操控;DSH Remote 远控不支持远程装插件或 DS Bot。
4. **复合许可约束**:核心为强传染 `AGPL-3.0`,且品牌与吉祥物资产全权保留(`ASSETS.md`),二次分发须剥离全部品牌素材并开源网络侧改动。

## 可信度与复现

**读过**:`README.md`、`SECURITY.md`、`ASSETS.md`、`docs/architecture.md`、`docs/guide/zh/11-faq.md`、`app/pubspec.yaml`、`runtime/build-runtime.sh`、`runtime/patches/{series,pins.json,route-guard.diff}`、`runtime/bridge/dsh-go-bridge/{package.json,cordis.patch.yml,lib/index.js}`、`app/android/.../runtime/DshProcess.kt`、`app/android/.../phone/{SafetyGate,PhoneGuest,McpServer}.kt`、`packages/dsh_remote/lib/src/{crypto/noise_ik,channel/secure_channel}.dart`、`app/lib/state/{connection_state,plugins_state}.dart`、`app/lib/remote/{ssh/ssh_link,ssh/local_forward,relay/relay_backend}.dart`、`app/lib/share_hosted/{hosted_client,hosted_crypto}.dart`、`app/lib/usage/{usage_stats,usage_net}.dart`。**未读**:其余 265 份 `.diff` 补丁、`DirectLaunch`/`TawcrootLaunch`、iOS/鸿蒙原生宿主与 `dsh_tavern`,未做真机实测。

```sh
git clone --depth 1 https://github.com/ccch1mneyyy/dsh-Go && cd dsh-Go
git rev-parse HEAD   # 3b9fbbbb5953ad1afc383ddec16bd63bc02c3442
gh release view v1.3.0 --repo ccch1mneyyy/dsh-Go --json assets --jq '.assets[] | [.name, .downloadCount]'
```

## 待验证

- 未实测 `Direct glibc` 与 `tawcroot` 模式在主流安卓 14/15 国产 ROM 上的兼容性与 `L2sMigration` 失败回退表现。
- 未读 `services/share-worker/` 核验其日志保留策略与 `dshfind` 插件索引校验机制。
- 未验证 iOS `PhoneRunner` XCTest 控手机与鸿蒙 TinyEMU 的真实可用度。
