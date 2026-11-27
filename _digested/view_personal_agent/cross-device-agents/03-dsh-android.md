---
kind: card
domain: personal_agent
subcategory: cross-device-agents
repo: jackwener/DSH-Android
commit: 283a6eafeba171f744951c0d4f3182e47f8f197f
evidence: 3
status: active
asof: 2026-11-27
---

# DSH-Android — 免 Root 免 Termux 把真 DSH 引擎塞进安卓手机,读屏操控微信/小红书并带后台虚拟屏

> 证据等级 ★★★(源码级;`jackwener/DSH-Android@283a6eaf`)。未在真机安卓设备实测安装或运行 `js/test`;双进程 JNI 嵌入、22 份上游补丁、无障碍+OCR 操控、后台 `VirtualDisplay`、10 类触发器与安全策略均经源码逐文件核验。
> **未收录于 `awesome-dsh-plugin` 注册表**(独立 Android APK 分发,底层直接打包未分叉的上游 `@deepseek-ai/dsh@0.2.2-rc.5`)。星标 1,097★ / 130 forks 为 2026-11-27 GitHub API 实时值。

## 它替谁解决什么问题

**想把个人 Agent 直接装在随身安卓手机里——不依赖家里的电脑开机、不折腾 Root/Termux/proot——就能替自己读屏操作微信、小红书、BOSS 直聘、抖音、飞书、改系统设置、按时间/地理围栏/通知自动触发办事的移动端个人用户。** 之前在手机上跑个人 Agent 有三种笨办法:

- **手机套壳连 PC 电脑**:电脑一休眠或断网就瘫痪,而且电脑端根本碰不到手机专属 App(微信移动端、小红书、本地短信/日历/蓝牙/Wi-Fi)。
- **在手机里装 Termux + proot Ubuntu**:配置链路长、极易被 Android 12+ 幽灵进程机制(Phantom Process Killer)杀掉,且与安卓无障碍/通知监听/输入法割裂。
- **纯云端手机 Agent**:需要把微信/社交账号登录态交给第三方云手机,隐私和风控风险高。

`jackwener/DSH-Android` 直接交叉编译 Bionic 版 Node 24.22.1 进独立 `:engine` 进程,通过 JNI 拉起未分叉的 `@deepseek-ai/dsh@0.2.2-rc.5`,用 `AF_UNIX` socketpair 把安卓无障碍、ML Kit 离线 OCR、后台虚拟屏(经 Shizuku)与 10 类系统触发器接成原生 DSH 工具。

## 适用面:谁该用、谁别用

- **适合**:使用 `arm64-v8a` Android 10+(API 29+)设备、愿意侧载 ~110 MB APK 并按需开启无障碍/通知监听(可选配 Shizuku 获得后台免打扰虚拟屏)的个人极客与中文生态移动端自动化用户;也附带 Remote SSH 模式可复用同一套界面连远程 Linux/macOS 的 `dsh --profile sdk`。
- **不适合**:iOS 用户、非 `arm64-v8a` 机型或存储紧张手机(需预留约 500 MB);对隐私读取审批有强要求的敏感用户——**源码实测默认权限预设为 `Full`(`danger-full-access`)且无生物识别门禁,即便切到 `Ask` 模式也会自动放行短信、通讯录、定位、剪贴板与通知等 `sensitive` 读取**(`plugin-guard/index.js:476-478`, `SessionStore.kt:972`,与自身文档声明存在偏差);也不能接受锁屏状态下无法执行任何 UI 操控工具的后台全自动场景。
- **前置条件**:Android 10+ `arm64-v8a`,允许绕过 Google Play Protect 侧载提示;国产 ROM 需手动放行自启动/后台保活/悬浮窗;启用“后台虚拟屏免打扰”需额外激活 Shizuku(APK 内置一键安装)。

## 业务价值

- **能算清的**:
  - **1,097★ / 130 forks / 29 open issues**(2026-11-27 实时值,建仓 1 个月即达千星,版本 `0.3.11`),是目前源码公开、直接在手机端驱动真实生活 App 的原生 DSH 代表作。
  - **18 份内置 App 视觉操作指南(`APP.md`) + 零 LLM 固定触发器**:覆盖微信、小红书、抖音、飞书、B站、知乎、微博、闲鱼、BOSS 直聘等,首次进入对应 App 自动注入指南;简单规则(`RuleAction.Steps`)不启动 Node、零 Token 消耗即可执行。
  - **包体与启动开销明确**:APK 约 110 MB、引擎冷启动约 5 秒、裁剪掉桌面重依赖后启动模块数约减半(~1002 → ~500)、V8 堆上限锁在 768 MB。
- **只是预期(推断)**:
  - 后台虚拟屏(`VirtualDisplay` + 应用静音)与 8–20 秒随机社媒外发节流(`OutwardPacing`)可能显著提升手机端无人值守自动化体验并降低 App 风控误伤,但缺乏跨国产 ROM 的真实成功率统计。

## 一屏事实

| 项 | 值 |
|----|----|
| 仓库 / 注册状态 | `jackwener/DSH-Android`(**未收录于 `awesome-dsh-plugin`**,独立 Android APK 分发) |
| 子分类 | `cross-device-agents`(跨设备与随身个人 Agent) |
| 自述 | 免 Root 免 Termux 将 DSH 引擎进程内嵌入安卓 APK,读屏操控手机 App、改系统设置与条件自动化 |
| 星标 / fork(2026-11-27) | **1,097★ / 130 forks / 29 open issues**;创建 `2026-10-27`,最近 push `2026-11-24`(`v0.3.11`) |
| 包形态 / 许可 | Android APK(`arm64-v8a`, `minSdk 29` / `targetSdk 36`,含交叉编译 Node 24.22.1 + `@deepseek-ai/dsh@0.2.2-rc.5`);**Apache-2.0** |
| 代码规模 | 共 801 文件 / 核心约 **49,084 行**(279 `.kt` + 67 `.js/.mjs/.cjs` + 2 `.cc` JNI + 22 JS 补丁 + 17 Node 补丁 + 18 份 `APP.md` + 218 `js/test`) |
| 宿主钉版 | 精确钉死上游 `@deepseek-ai/dsh@0.2.2-rc.5` + `Node 24.22.1`,构建期打 **22 个 JS 补丁**(含按内容哈希打 chunk 补丁)与 17 个 Node 补丁 |
| repo@commit | `283a6eafeba171f744951c0d4f3182e47f8f197f`(2026-11-24 UTC) |
| 证据等级 | ★★★ |

## 它到底是什么

**一台把完整 DeepSeek Harness 运行时无 Root 塞进安卓双进程架构的“口袋个人操作代理”。** 应用严格拆为两个 OS 进程(`AndroidManifest.xml:10,104,217-224`, `EngineService.kt:27-105`):

```text
:main 进程(Compose UI / 无障碍 / 通知监听 / 输入法 / 悬浮球 / CapabilityHub / TriggerHub)
  ⇄ stdin/stdout 管道:标准 DSH SDK JSON-RPC 2.0 + android/* 扩展方法(patch 10)
  ⇄ AF_UNIX socketpair(DSH_BRIDGE_FD,64MB 行上限):capability/list + capability/invoke(含 base64 截屏)
:engine 进程(FOREGROUND_SERVICE_TYPE_SPECIAL_USE,16MB 栈线程 JNI 启动 Bionic Node 24.22.1)
  → @deepseek-ai/dsh@0.2.2-rc.5 --profile android(裁剪 50% 桌面模块 + plugin-device + plugin-guard)
```

因为 `node::Start()` 在单进程内只能调用一次,Node 退出时 `:engine` 主动调用 `stopSelf()` + `Process.killProcess` 自杀(`EngineService.kt:91-92`),既把引擎崩溃与 UI 隔离,又借前台服务避开 Android 12+ 幽灵进程查杀。

## 怎么接进 DSH

1. **未分叉上游 + 构建期外科补丁(`js/engine/package.json:6-9`, `js/build-engine.sh:33-212`)**:直接拉取 `@deepseek-ai/dsh@0.2.2-rc.5`,应用 22 份 `js/patches/*.patch`(修 Android `flock`、`/system/bin/sh`、硬链接回退、`sharp-wasm`、`android` profile 模板、SDK 扩展方法与 `prompt steer` 等),并裁掉 `libreoffice-kit-wasm`、`dsh-web-frontend`、`sherpa-onnx*`、`otel`、`ptc-runtime` 等桌面包,打成无符号链接的 `engine.zip` 进 APK assets。
2. **自定义 `android` Profile(`js/packages/bundle-android/{cordis.patch.yml,main.mjs}`)**:以 `--profile android --patch $DSH_HOME/android/app-layer.patch.yml` 启动,配 2 次崩溃即进安全模式的启动归因保护(`plugin-extensions/boot.js`),并允许通过 `bundle-android` 挂接第三方 OpenAI 兼容模型提供方(`@snnh/dsh-llm-service-lite`)。
3. **静态能力描述保缓存(`CapabilityHub.kt:104-110`, `plugin-device/index.js:95-134, 141-331`)**:`plugin-device` 经 `capability/list` 注册静态工具描述(防止动态权限/Shizuku 切换打穿模型前缀缓存);当前模型路由不支持 `image` 输入时自动剥离截屏并附文字说明。

## 关键实现

| 模块 | 位置 | 作用与源码实证 |
|---|---|---|
| JNI 嵌入与 `AT_SECURE` 绕过 | `native/engine-jni/dshengine.cc:46-96`, `EngineService.kt:64-93`, `docs/ENGINE-CONTRACT.md:10-26` | 绕过安卓 zygote `AT_SECURE=1` 忽略 `NODE_OPTIONS`/`TMPDIR` 的限制:将 `--expose-internals`、`--max-old-space-size=768` 直接塞进 argv 并用 `--require android-env.cjs` 恢复环境语义 |
| 读屏、OCR 与安全页接管 | `DshAccessibilityService.kt:79-195`, `ScreenTools.kt:80-250`, `ScreenOcr.kt:19-41`, `TextInput.kt:18-45` | 多屏无障碍树(深度 40)+ 稳定 ID + 增量 `ScreenDiff`;可读节点 `<4` 自动跑内置 ML Kit 中英文 OCR 输出 `[t<n>]` 可点坐标;遇支付/密码 `FLAG_SECURE` 或全黑屏自动 `hand_to_user`;5 级校验文字输入防重复输入 |
| 后台虚拟屏免打扰 | `AgentScreen.kt:77-285`, `ShellUserService.kt:77-115, 164-204` | 配合 Shizuku(uid 2000)创建按会话隔离的 `VirtualDisplay("dsh-agent")`,用 `ImageReader` 抓帧、`appops` 静音、拉回溢出任务,空闲 10 分钟自动回收;内置 700 行零依赖无线自连 ADB(`LocalAdb`)可跑命令但不能建虚拟屏 |
| 防死循环与外发防风控 | `ActionGuard.kt:18-174` | `LoopGuard` 监控 `Repeat`/`NoEffect`/`Reread`/`Failure` 四项指标升级警告至硬停;`OutwardPacing` 在同 App 内发消息/发帖/关注间强插 **8–20 秒随机延迟**(30 分钟窗口最高延至 30 秒),并检测 `LimitNotice` 限流横幅 |
| 10 类自动化触发器 | `TriggerHub.kt:139-338`, `RuleValidation.kt:22-80` | 定时/地理围栏(无 GMS 回退 `LocationManager`)/Wi-Fi/蓝牙/充电/低电/耳机/亮灭屏/通知/打开 App;轻量 `RuleMonitorService` 监听不拉 Node;60 秒防抖 + 50 次/24h 上限;`Steps` 模式禁 `adb_shell`/`termux_run`(因 `hardline.js` 只在引擎内),`Agent` 模式硬锁 `allowedTools` |
| 硬底线拦截与权限分层 | `js/packages/plugin-guard/{hardline.js,index.js}`, `CapabilityHub.kt:197-269`, `SessionStore.kt:958-973` | Android 无 Linux OS 沙箱(`sandbox-policy.mode: danger-full-access`),靠 `hardline.js` 不可覆盖硬拦删根/系统目录、重启、格式化、`curl\|sh` 与卸载系统包;锁屏时 UI 工具暂停并推通知等待解锁 |

## 为什么它突出

只用本仓库自身证据:

- **极硬核的原生移动端 DSH 工程**:不靠 Termux、不靠云手机、不分叉 DSH 主树,用 Bionic Node 24 + 22 份外科补丁 + 双进程 socketpair 把真 DSH 引擎塞进了单 APK。
- **真正面向中文真实手机 App 做了深水区打磨**:ML Kit 稀疏节点 OCR、`FLAG_SECURE` 自动交人、Shizuku 后台虚拟屏静音、18 份微信/小红书/抖音等 `APP.md` 操作指南、8–20 秒外发防风控节流,每一项都直击手机操控的真实痛点。
- **零 LLM 监听层 + 熔断自愈**:触发器监听与固定步骤不拉起 Node;引擎崩溃走 1s/2s/4s 退避、10 分钟 3 崩熔断、反复原生崩自动切 V8 `--jitless`(`RestartPolicy.kt:14-37`, `SettingsRepository.kt:106-109`)。

## 代价与边界

1. **源码实测文档与代码不符(隐私读取未询问)**:`docs/ENGINE-CONTRACT.md:271-272` 写着 `sensitive` 读取每会话问一次,但实际运行代码 `plugin-guard/index.js:476-478` 与 `SessionStore.kt:972` 在人工交互会话中**即便处于 `Ask` 模式也会自动放行 `sensitive` 读取**(短信/通讯录/定位/剪贴板/通知/通话记录);且默认预设为 **`PermissionPreset.Full`**,除 `sms_send`/`notification_reply` 外全自动放行,Manifest 声明了 `USE_BIOMETRIC` 但实际**无生物识别确认**(`ARCHITECTURE.md:101`)。
2. **无 OS 沙箱且权限面极宽**:`danger-full-access` 模式 + Manifest 请求 `MANAGE_EXTERNAL_STORAGE`、`READ/SEND_SMS`、`WRITE_SECURE_SETTINGS` 等高危权限(虽为按需首次工具调用时申请),全靠软件层 `hardline.js` 与 `CapabilityHub` 守门。
3. **停止会话即杀整引擎 + 空闲 5 分钟休眠**:DSH SDK 缺单会话取消,点停止直接杀整个 `:engine` 进程(`ARCHITECTURE.md:53`);默认空闲 5 分钟关引擎(会停掉后台插件心跳),需手开 `engineKeepAlive`。
4. **重度上游补丁债**:维护 22 个 JS 补丁(含哈希 chunk 补丁)+ 17 个 Node 补丁钉死 `0.2.2-rc.5` 与 `Node 24.22.1`,`UPSTREAM.md:3` 记录向上游提 PR 数为 **0**。
5. **安卓生态摩擦**:仅 `arm64-v8a`、侧载触发 Play Protect 拦截、锁屏阻断全部 UI 工具、部分国产 ROM 拒绝给 `shell` 授 `ADD_TRUSTED_DISPLAY` 会导致虚拟屏输入法退化。

## 可信度与复现

**读过**:`README.md`、`docs/{ARCHITECTURE,ENGINE-CONTRACT}.md`、`app/build.gradle.kts`、`AndroidManifest.xml`、`native/engine-jni/dshengine.cc`、`core/engine/{EngineService,RestartPolicy}.kt`、`js/engine/package.json`、`js/build-engine.sh`、`js/patches/UPSTREAM.md`、`bundle-android/{cordis.patch.yml,main.mjs}`、`plugin-device/{index,bridge}.js`、`plugin-guard/{index,hardline}.js`、`core/capability/{CapabilityHub,ActionGuard,AgentScreen,ScreenOcr,TextInput,tools/ScreenTools}.kt`、`DshAccessibilityService.kt`、`core/trigger/{TriggerHub,RuleValidation}.kt`、`core/platform/{DeviceShell,ShellUserService}.kt`、`core/data/SettingsRepository.kt`、`core/session/SessionStore.kt` 及微信/小红书 `APP.md`。**未读**:各 `.patch` 逐行 diff、`core/platform/adb/*`、`core/remote/*` 与 Compose UI 屏幕,未做真机实测。

```sh
git clone --depth 1 https://github.com/jackwener/DSH-Android && cd DSH-Android
git rev-parse HEAD   # 283a6eafeba171f744951c0d4f3182e47f8f197f
```

## 待验证

- 未在主流国产安卓 ROM(小米/华为/OPPO/vivo)真机实测 Shizuku 后台虚拟屏与 18 份 `APP.md` 的端到端成功率。
- 未验证 `LocalAdb` 无线自连在手机重启或 Wi-Fi 切换后的重连稳定性。
- 未实测 Remote SSH 模式连接远程 `dsh --profile sdk` 的权限与断开恢复表现。
