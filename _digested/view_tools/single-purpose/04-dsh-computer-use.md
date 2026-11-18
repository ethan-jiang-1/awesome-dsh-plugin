# dsh-computer-use — 把 macOS Accessibility 观测做成一次性快照，输入前再用 stateHash 重校验

> 证据等级:★★★(源码级;`Anionex/dsh-computer-use@90444cf18d994840cd1046ca1ec7b420cf7c4a59`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 22 为 2026-08-19 历史采样;下载 360 同为该日(边车无 `start/end`,统计窗口未知)。2026-11-18 实时星标 **106**。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `Anionex/dsh-computer-use`([registry](../../../data/plugins/Anionex__dsh-computer-use.yml)) |
| 类目 | tools(1639 条,[census](../../ecosystem/census.py)) |
| 子分类 | `single-purpose` |
| 自述 | 「Accessibility-first macOS computer use: fresh observations, stale-state rejection, scoped permissions, and safe input.」前三项在源码里各有落点;"safe input" 的审批是**模型声明式**的,host 不做语义分类(见「代价与边界」) |
| 星标 ⚠ | **22**(2026-08-19 冻结采样);2026-11-18 实时 **106** |
| 下载 ⚠ | **360**(2026-08-19 冻结采样)。补充:2026-11-18 查 npm last-month **6,570**(2026-10-18..11-16),只作实时参考,不替换 ⚠ 值 |
| 扩散 | **0**(口径见「为什么它突出」:`computer-use` 命中 38 条、`dsh-computer-use` 命中 18 条,逐条读 description 后,除自身外无一条引用本仓库或包名) |
| 仓库 commit | `90444cf`(2026-11-12,`main`);仓库创建 2026-08-13;78 个提交、13 个 tag、npm 13 个版本 |
| 包形态 | npm `@anionex/dsh-computer-use@0.3.9`;Cordis **bundle**(`dsh.bundle.patch`)+ Web client + 提交进仓库的 universal Swift helper;不走 MCP,无外部服务 |
| 代码规模 | `src/**/*.ts{,x}` **5,466 行**(TS 4,886 + `src/client/index.tsx` 580);Swift helper **2,695 行**(`native/macos/Sources/Helper/*.swift`);测试 **7,104 行 / 182 个 `it/test` 声明**(`tests/*.ts`,24 个文件);`lib/` 编译产物 4,155 行 |

## 它到底是什么

**一句话:一个自带原生二进制的 macOS 执行层。** 它不是配置包(有 5,466 行 TS)、不是 MCP 桥(没有 mcp-client 依赖)、也不是某个外部引擎的客户端——AX 遍历、截图、点击、键盘、光标全部在这个仓库里。四层结构:

1. `ComputerUseService`(`src/service.ts`,861 行)——provider 无关的观测存储、租约、确认令牌、动作流水线、settle 循环;通过 Cordis service key `ctx.computerUse` 暴露(`service.ts:334`)。
2. `MacOSBackend`(`src/providers/macos.ts`,309 行)——把 service 调用翻成固定的 JSON 命令(`resolve-app` / `list-apps` / `observe` / `act` / `activate-for-cursor` / `open-settings` / `health`,`main.swift:1253-1340`)。
3. `NativeHelperClient`(`src/providers/native-helper.ts`,761 行)——helper 完整性检查、`ctx.subprocess` 调用、持久光标进程、拖拽 START 屏障。
4. Swift helper(`native/macos/Sources/Helper/`,2,695 行)——Accessibility 树、ScreenCaptureKit 截图、SkyLight 定向指针、pid 定向键盘、`NSPanel` 光标。下文的 `main.swift` 均指 `native/macos/Sources/Helper/main.swift`。

**观测对象(不是 README 转述)。** 一次 `computer_observe` 返回:

- **observation** — `observationId`、精确 app `{bundleId,pid,name}`、`createdAt`/`expiresAt`、`frontmost`、`window{title,frame,id?}`、`tree{mode:'full'|'diff',text,truncated}`、`elements[]`、可选 `screenshot` Artifact、`permissions{accessibility,screenRecording}`(`src/service.ts:779-796`、`src/tools.ts:114-154`)。
- **element** — `index`(observation 局部)与不透明 `targetHandle`;公开元素**剥掉**了 `locator` 与 `nativeIdentifier`(`service.ts:54-66`)。句柄背后是 service 侧保存的 descriptor:`locator`、`nativeIdentifier`、`role/subrole`、accessible name、最近 4 层祖先指纹、窗口归一化 frame、排序后的 actions(`target-resolver.ts:122-160`)。
- **stateHash** — helper 对 `bundleId + pid + window(title,id,frame) + 每个元素的 hash 行` 做 SHA-256(`main.swift:520-539`)。secure 字段的 value 先被替换成 `[secure]` 再进 hash(`main.swift:465-471`)。
- **lease / confirmation** — 读租约按 Session、控制租约按当前 turn;敏感确认是一次性 token,绑定 app、observation 和**归一化后的** action 哈希(`confirmations.ts:32-35,78-84`;`service.ts:417-431`)。

**核心循环(AX 优先)。**

1. `resolveApp` 把 selector 解析成唯一 `bundleId+pid`;`list-apps` 只列 `activationPolicy == .regular` 的进程,同名/同 bundleId 多实例直接报 `COMPUTER_APP_NOT_FOUND`(`main.swift:172-229`)。
2. 取 `read` 租约 → 有界 DFS 遍历 AX 树(默认 `maxNodes 500`、`maxDepth 14`、`maxTextBytes 64,000`,`config.ts:92-94`),截断即 `truncated`;视觉信息才另拍窗口截图。
3. 选目标:语义元素(优先)、窗口/屏幕坐标、或截图坐标。
4. 取 `control` 租约 → (敏感动作)确认 token → **重新观测**并解析目标 → helper 再观测一次并校验 `stateHash` 或元素属性 → 输入。
5. 输入路由依次是:`AXPress`(含可按下后代重试,`main.swift:276-290`)、`AXValue`/`AXSelectedText`/元素声明的 action、pid 定向键盘、pid+`CGWindowID` 定向指针。指针**永不**走全局 HID,系统光标不动(`TargetedPointer.swift:39-41`;`docs/interaction-policy.md:44`)。Electron/Chromium 先写 `AXManualAccessibility` 并等最多 2.5 秒(`main.swift:403-415`)。
6. settle 循环按 `settleMs` 重观测,`stateHash` 变了就停;上限 `maxSettleMs`(`service.ts:637-649`)。
7. 无论动作成败,都返回一份**新的** full/diff observation,外加 `effect.observedStateChanged`(`service.ts:650-682`)。

**快照的新鲜度有三道,不是一道。**

- **默认 TTL 是关闭的**:bundle patch 与 schema 都把 `observationTtlMs` 设为 `0`(`cordis.patch.yml:7`、`config.ts:87,171`),此时 `expiresAt` 是哨兵值 `9999-12-31…`(`service.ts:783-785`)。所以"过期"默认不靠时间。
- **作用域拒绝**:observation 按 Agent 隔离;`requireObservation` 先 `prune` 掉过期项和旧 provider generation,查不到就 `COMPUTER_STALE_OBSERVATION`(`service.ts:714-733`)。每个 Agent 最多留 64 份(`service.ts:799-803`)。
- **动作前校验**:元素/句柄动作由 service 重新观测后跑 `resolveComputerTarget`(`service.ts:507-515`);helper 在真正输入前再观测一次,元素动作比对 locator+属性+窗口,坐标动作比对整棵 `stateHash`(`main.swift:913-929,1000-1019`)。窗口或进程变了直接 `COMPUTER_STALE_OBSERVATION`(`target-resolver.ts:169-174`)。

## 怎么接进 DSH

**manifest 是 bundle,不是字段集合。** `package.json:76-88` 只有 `dsh.bundle.patch → ./cordis.patch.yml` 和 `dsh.client`(5 个 client 包 + `platform: "web"`)。真正的挂载点是 16 行 patch:一条 `insert`、`id: computer-use`、`name: '@anionex/dsh-computer-use'`,并把仓库默认交互策略写死(`cordis.patch.yml:3-16`)。DSH 的兼容性判定读的是 `peerDependencies`(或 `engines.dsh`),不是 `dsh.compatibility`(本机 DSH `$DSH/node_modules/@deepseek-ai/dsh-app-boot/lib/index.js:279-298`)。`dsh plugin` 本身只是把参数转发给 pnpm(本机 DSH `$DSH/lib/bin.js:116-118`):

```sh
dsh plugin --profile web add @anionex/dsh-computer-use
dsh plugin --profile headless add @anionex/dsh-computer-use
```

**Service 注册。** `ComputerUseBundle extends MacOSComputerUseProvider extends ComputerUseService`,注入 7 个服务:`subprocess`、`approval`、`settings`、`sessions`、`agents`、`tools`、`skills`(`src/index.ts:49-51`)。`[Service.init]` 先做 helper 完整性与权限健康检查,**通过后**才发布 Skill 和工具(`index.ts:63-73`);非 macOS 只装 Web 设置页,不注册任何模型工具(`index.ts:66-71`)。

**模型工具面是渐进的。** 刚装好只有全局 `computer_use_activate`(`index.ts:28`、`exposure.ts:11`)。当前 Agent 的 Session 里出现"加载过本 Skill"的持久证据后,才为该 Agent 注册 11 个工具,再用 `tools.restrict({ deny: ['computer_use_activate'] })` 把引导工具藏掉(`exposure.ts:211-232`)。skill 证据同时认三种历史:`user/message` 的 `skill-invocation`、原生 `skill` 工具结果、以及 PTC `run_code` 的 `tool/ptc-dispatch`/旧名 `tool/code-dispatch`(`exposure.ts:92-127`)。

| 工具 | 通道 | 关键约束 |
|---|---|---|
| `computer_list_apps` | 只读 | 只列 regular 应用,带 TCC 状态 |
| `computer_observe` | 只读 | 必须带 `observationId` 语义;可 `full` 或 diff,可要截图 |
| `computer_click` | AX→坐标 | 默认 `AXPress`;`elementIndex` 精确或 `targetHandle` + `allowRebind`;坐标需显式 `allowCoordinateFallback` |
| `computer_set_value` | AX | 不碰剪贴板;可清空 |
| `computer_type_text` | AX→键盘 | `method:"keyboard"` 跳过 AX,逐字符发 Unicode;不回显文本 |
| `computer_press_key` | 键盘 | 60 个固定键名 + 4 个修饰键枚举 |
| `computer_scroll` | 坐标 | 只投递给选定 pid+window |
| `computer_drag` | 坐标 | 两点 + 三坐标空间 |
| `computer_perform_action` | AX | 只能执行元素自己声明的 action;`AXRaise` 需 `focusPolicy: activate` |
| `computer_wait` | 只读 | 单条件轮询,不修改应用 |
| `computer_confirm` | 审批 | 为"同一个 action"签发一次性 token |

**Skill 与命令。** 注册两个运行时 Skill:`dsh-computer-use` 与兼容名 `computer-use`(`skill.ts:6-12,160-172`),内容 143 行,写了观测协议、后台输入、视觉交接、敏感动作清单、拒绝后的行为(`skill.ts:15-157`)。`/dsh-computer-use` 就是 Skill 的 slash 入口;插件**没有**注册独立的 DSH command。旧包名 `@dsh-external/dsh-computer-use` 从未发布,README 明确要求改引用(`README.md:83-86`)。

**设置页与热更新。** 服务端 Settings namespace 是 `computer-use`,注册时带 `applies: 'live'` 和 `validate`(`providers/macos.ts:264-270`)。Web 路由是精确匹配的 `/_dsh/computer-use/settings`(`web.ts:15,197-209`),GET 返回 snapshot,POST 处理 `save`/`health`/`open-settings`;校验 `Content-Type`、128 KB 上限、同源(含 Desktop 的 Host Connection 签名回退)、`no-store` 与 CSP(`web.ts:48-96,156-193`)。客户端注册 `settings.section` slot,id `computer-use`,order 35(`src/client/index.tsx:558-580`)。保存成功后 `reconfigure` 换 backend、`generation += 1`、清空 observation 与 confirmation(`service.ts:364-373`)。

**存储与审批。** 读租约和"拒绝决定"落在插件自己的 storage-domain sidecar:`defineDomain({ name:'computer_use_state', version:0 })`,表 `sessions` 以 SessionId 为键,行里用 `createdAt+cwd` 围栏,复用 Session id 也不会串(`leases.ts:71-77,92-115,260-263`)。没有 `@deepseek-ai/dsh-storage-domain` 时,静态 grants 和"本 turn 控制批准"仍可用,但**交互式读租约与持久拒绝会明确失败**,不会静默降级(`leases.ts:219-221,311-320`)。审批走 `ctx.approval.request`:读租约批一次管整个 Session,控制租约批一次只管当前 turn;拒绝写入 sidecar,之后同一 app+scope 不再问(`leases.ts:197-257`)。`approval/policy: never`(如 `danger-full-access`)时连提示都不发,直接 `COMPUTER_PERMISSION_REQUIRED`,且不记为"用户拒绝"(`leases.ts:212-217`、`confirmations.ts:54-59`)。

**二进制与权限引导。** helper 是提交进仓库的 universal `arm64+x86_64` Mach-O(901,040 字节),`native/macos/manifest.json` 钉住二进制 SHA-256、Swift 源摘要、架构与最低 macOS 14.0。`prepare()` 拒绝符号链接、校验 hash、必要时只补 owner 执行位,然后才允许 spawn(`native-helper.ts:182-233`)。helper 启动时先要求"独立进程组 + 三个标准管道由直接父进程持有",普通 shell 重定向在解析命令前就失败(`main.swift:137-163`);这是纵深防御,README 自承挡不住同用户刻意构造的父进程(`README.md:154`)。设置页的 Accessibility / Screen Recording 卡片只显示状态和"打开系统设置"按钮;helper 的 `open-settings` 打开两个精确的隐私面板 URL(`main.swift:1278-1290`)。插件**不能**自己授予 TCC。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---:|---|---|
| `src/service.ts` | 861 | 观测存储、租约/确认接线、动作流水线、settle | `:409-444,480-522,592-612,637-682,714-733,779-803` |
| `src/target-resolver.ts` | 237 | 三层目标解析与 fail-closed | `:8-13,122-160,163-237` |
| `src/leases.ts` | 341 | 读/控制租约、sidecar、审批 | `:71-77,160-257,281-320` |
| `src/confirmations.ts` | 128 | 一次性敏感 token | `:32-35,47-84,88-117` |
| `src/exposure.ts` | 250 | 渐进工具面 + OCR guard | `:92-127,166-203,211-232` |
| `src/tools.ts` | 551 | 11 个工具的定义/输出 schema | `:197-207,333-551` |
| `src/providers/native-helper.ts` | 761 | helper 完整性、协议、光标进程、拖拽屏障 | `:182-233,236-278,280-414,561-689` |
| `src/client/index.tsx` | 580 | 设置页(中英)、健康/权限/grants | `:399-416,558-580` |
| `src/web.ts` | 210 | 同源设置路由 | `:48-96,132-209` |
| `src/skill.ts` | 172 | 143 行模型操作手册 | `:15-157` |
| `native/macos/Sources/Helper/main.swift` | 1,399 | AX/截图/输入主流程 | `:403-415,417-544,546-597,913-929,1000-1236` |
| `native/macos/Sources/Helper/TargetedPointer.swift` | 327 | SkyLight 定向指针 | `:39-49,147,202,246` |
| `native/macos/Sources/Helper/CursorOverlay.swift` | 840 | 独立光标进程的非激活 NSPanel | `:197-210,561-586` |
| `native/macos/Sources/Fixture/main.swift` | 451 | 从不激活的 AppKit 验收夹具 | 全文 |
| `tests/service.spec.ts` | 1,461 | 45 个服务契约用例 | 见下 |

**目标解析是确定性的三层,失败优先于猜测。** 先原始 locator(且稳定字段完全一致),再唯一 `AXIdentifier`,最后唯一语义匹配(role + 归一化 accessible name + 排序后的 actions + 最近 4 层祖先指纹)。重复候选 `COMPUTER_TARGET_AMBIGUOUS`,证据不足 `COMPUTER_TARGET_LOW_CONFIDENCE`;`truncated` 的新树不允许 rebind;`allowRebind` 必须同时给 `targetHandle`;descriptor 里**没有 value 字段**,secure 值也不会进指纹(`target-resolver.ts:83-96,190-226`;`tests/target-resolver.spec.ts:205-211`)。

**策略执行两遍,而且先后顺序有讲究。** service 在**拿控制租约和消费确认 token 之前**就拒绝已知的指针/前台需求(`service.ts:480-492`):`pointerInputPolicy: deny` 拦住坐标点击、滚动、拖拽;`AXRaise` 在 `focusPolicy: preserve` 下直接 `COMPUTER_ACTION_BLOCKED`。helper 在输入前按同一份 policy 再判一次,并补上只有运行时才知道的 fallback 决定(`main.swift:1052,1151,1185,1226-1228`)。敏感 token 在 `backend.act` 前一刻才消费(`service.ts:600-612`);若解析发生 rebind,旧 token 先失效再报 `COMPUTER_TARGET_REBIND_REQUIRES_CONFIRMATION`(`service.ts:516-522,542-548`)。

**观测裁剪与上下文成本。** `capture` 只保留每个 Agent 最近 64 份;第二次观测默认返回 diff,diff 以 `role|subrole|title|label|frame` 为身份,变化行用 `+/-/~` 前缀,超 `maxTextBytes` 截断(`service.ts:766-803`、`diff.ts:34-52`)。截图写到 workspace 下的 `.dsh-computer-use/artifacts/<sessionId>/`,`allocateScreenshotPath` 做 realpath、`..`、符号链接逐段检查,`describeScreenshot` 再查文件类型与大小上限(`artifacts.ts:41-97`)。截图只落在 Session workspace,不需要 `danger-full-access`。

**OCR 的"反向 guard"是个少见机制。** 当本 Skill 已加载、装了 vision 工具、且模型试图用 `bash` 跑 `tesseract`/`screencapture`/内联 Swift-Vision 时,`ctx.tools.guard` 直接拒绝这次 bash 调用并给出改走 `vision_*` 的指引(`exposure.ts:172-179`)。它不改 DSH 核心,只在自己加载后收紧一个相邻工具。

**测试能证明的契约(不是覆盖率)。** 182 个用例里,45 个在 `tests/service.spec.ts`,覆盖:TTL 过期与 Agent 隔离(`:843-867`)、读租约落 sidecar 且顺序是 `approval → session flush → sidecar`、Session 日志里**没有** `computer-use/*` 事件(`:906-931`)、`approval/policy: never` 不发提示(`:964-984`)、token 只能用一次且改一个字段就不匹配(`:1118-1150`)、敏感目标 rebind 后 token 失效(`:1150-1195`)、截图坐标空间换算(`:1345-1460`)。`tests/native-helper.spec.ts` 的 30 个用例里,有二进制 manifest/架构/签名、无 `CGEventPost`/`CGWarpMouseCursorPosition` 符号、直接 shell 调用 helper 被 transport guard 拒绝(`:188-216,329-357`)。`tests/action-surface.e2e.spec.ts:250-292` 用真实 helper 断言"过期观测不重试目标"和"全程不激活";`tests/native-fixture.e2e.spec.ts:865-903` 在后台应用里输入 `Background 深度🌿 42.` 并断言激活计数为 0。`tests/package-layout.spec.ts:122-181` 把 DSH peer 矩阵(6 个支持版本为真、5 个未测版本为假)和"不改官方 Session 事件词汇"写成可执行断言。

## 为什么它突出

**先拆星标归属:这里没有宿主项目可借。** 仓库是独立项目,时间线全部在发布之后:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-11 | 首个提交 `feat: add macOS computer use bundle` | `git log --reverse` |
| 2026-08-13 | GitHub 仓库创建 | API `created_at` |
| 2026-08-14 | npm `0.1.0` 发布 | npm registry `time` |
| **2026-08-19** | **⚠ 22 星 / 360 下载采样点** | 冻结边车 |
| 2026-09-01/02 | `0.2.0` / `0.3.0` | npm registry |
| 2026-11-12 | `0.3.9`,最后提交 `90444cf` | `git log -1` |
| **2026-11-18** | **实时 106 星;npm last-month 6,570** | GitHub API / npm API |

也就是说,22 星是上线 5 天内的全部家当,不是继承来的;106 星与 6,570 次/月下载是之后 3 个月长出来的。**绝对量很小**(类目 1,639 条,⚠ 榜头部是 477),按本册的两轴口径它**不是锚**:声量不高,扩散为零。它值得单独成卡的理由是机制密度:双遍策略执行、stateHash 重校验、secure 脱敏、transport guard、目标进程限定指针,以及 182 个测试——这些在源码里都能逐条指到,不靠自述。

**扩散为 0,但同名家族很大,必须人工筛。** 口径与结果:

```sh
grep -ril 'computer-use' data/plugins/ | wc -l        # 38(含自身)
grep -ril 'dsh-computer-use' data/plugins/ | wc -l    # 18(含自身)
grep -ril 'anionex' data/plugins/ | wc -l             # 3(全是同作者仓库:本插件 + vision-toolkit + turn-rewind)
grep -ril 'Anionex/dsh-computer-use' data/plugins/ | wc -l   # 1(自身)
```

38 条里逐条读 `description.en`:1 条自身;17 条是其他 owner 的 `dsh-computer-use*` 同名/近名条目;其余 20 条是 `computer-use` 家族里不含精确 `dsh-computer-use` 的名字或正文命中(Windows/Linux/cua-driver/桌面控制,以及一条明确写 "no computer-use" 的 handoff 插件)。**没有任何一条引用本仓库 URL、包名 `@anionex/dsh-computer-use`,或作者名。** 所以"零第三方"成立:这个名字在生态里被大量复用,但这套实现没有被点名、被 fork 或被称为基线。

**反向的机制扩散信号也弱。** `Accessibility-first` 在 registry 里只有 4 条命中(本插件 + 3 条其他 macOS 条目),而本插件独有的 `stale-state rejection`/`stale observation` 只有它自己 1 条。判断:问题域很热(macOS/Windows 都有人做 AX 优先、后台输入),但这套"快照 + 句柄 + 动作前重校验"的词汇没有被复制。它更像一份完成度很高的**参考实现**,而不是被追随的标准。

**它自己的突出点,按可验证程度排:**

- **原生层做到底**:提交进仓库的 universal 二进制 + source/binary 双 hash + CI 重建后 `git diff --exit-code`(`.github/workflows/blank-helper-path-macos.yml:81-84`),不是让用户首次运行时 `swiftc` 编译。
- **指针路线的硬约束**:源码/二进制都不含 `CGEventPost`、`CGWarpMouseCursorPosition`,`check:native` 把这条写成断言(`scripts/check-native.mjs:54-90`),e2e 用 1 ms 采样的监控器证明前台 pid 与系统光标坐标不变(`docs/interaction-policy.md:137`)。
- **请求与授权分离**:host policy 不能由 tool 参数覆盖;`allowCoordinateFallback` 只是"允许尝试",不是"开启指针"(`docs/interaction-policy.md:85-87`)。
- **发布纪律**:每加一个 DSH prerelease 就发一版(CHANGELOG 显示 `0.3.4`→`0.3.9` 的 25 天里为 rc.2/rc.3/rc.5/0.2.2-rc.1 各发一次),并把"支持/不支持"的版本写成测试。
- **规模与依赖**:运行时 npm 依赖只有 `zod` 一个;`src/` 没有出站网络调用(唯一 `fetch` 是浏览器端打同源设置路由,`src/client/index.tsx:251,271`)。

## 代价与边界

**失败模式,按发生顺序:**

1. **TCC 未授予** → helper 在 `observeSnapshot` 入口直接 `COMPUTER_PERMISSION_REQUIRED`(`main.swift:417-420`);截图另需 Screen Recording,只有 `screenshot:'required'` 才硬失败,`optional` 会退化成无截图(`main.swift:546-550`)。设置页只能显示状态并打开系统面板,不能代授。
2. **应用不存在 / 同名多实例** → `COMPUTER_APP_NOT_FOUND`,提示补 pid(`main.swift:193-229`)。
3. **应用重启或换进程** → `bundleId,pid` 对不上,service 直接 `COMPUTER_STALE_OBSERVATION`(`service.ts:756-758`);窗口换掉/关掉也在 resolver 第一道被拒(`target-resolver.ts:169-174`)。
4. **窗口消失/最小化/不在屏上** → 截图找不到窗口是 `COMPUTER_TARGET_UNAVAILABLE`(`main.swift:571-575`);坐标点落在所有窗口之外也是 `COMPUTER_TARGET_UNAVAILABLE`,不会退回全局指针(`main.swift:649-681`)。
5. **元素过期/歧义** → 精确 locator 不成立且没开 `allowRebind` 是 stale;开了但候选不唯一是 ambiguous / low-confidence。敏感动作遇到 rebind 必须重新观测再确认,旧 token 作废。
6. **多显示器** → 屏幕坐标按 Quartz 全局 point 解析"该点下最上层的、属于目标 app 的 on-screen 窗口";代码专门用 `.optionAll` 找回被 `.optionOnScreenOnly` 漏掉的多屏窗口,但仍然拒绝隐藏窗口(`main.swift:660-681`)。截图是**单窗口**、按 backing scale(`pixelScale`,Retina 通常 2)渲染,坐标必须声明 `coordinateSpace:'screenshot'`,否则按 point 解释会偏移(`service.ts:104-186`)。光标 overlay 只在一个 Space、且只在目标 app 前台时显示,`canJoinAllSpaces` 被测试明确禁止(`CursorOverlay.swift:197-210`;`tests/native-helper.spec.ts:217-228`)。
7. **输入法(IME)** → **没有专门的 IME 处理**。`type-text` 的键盘路径逐字符发 `keyboardSetUnicodeString` 的 down/up 并清空修饰键(`main.swift:853-871`),这会绕过输入法组合;`press-key` 走物理 keycode(`main.swift:742-783`),若目标应用挂着中文/日文输入法,按键可能被 IME 消费。判断:多语言输入需要实测,仓库的 e2e 只覆盖"直接注入 Unicode 字符串"(`tests/native-fixture.e2e.spec.ts:865-903`)。
8. **超时与取消** → helper 单次调用硬顶 `actionTimeoutMs`(默认 15s,范围 1–120s),超时映射 `COMPUTER_TIMEOUT`(`native-helper.ts:236-264`);拖拽一旦 native mouse-down,caller 取消不再接管,必须等 bounded mouse-up(`native-helper.ts:393-413`)。**没有全局 Esc 急停/热键**:`escape` 只是 `computer_press_key` 的 60 个键之一(`tools.ts:202-207`、`main.swift:742-749`),"中断"实际依赖 DSH 的 AbortSignal。
9. **光标 overlay 失败** → 预期可见却不可见时,前台目标的动作在输入前失败关闭(`service.ts:557-590`);后台目标是有意隐藏,不算失败。

**其它代价:**

- **敏感动作的判定在模型手里。** `computer_confirm` 只是把"用户批准了这一个 action"变成 token;`consume` 仅在 `action.sensitive === true` 时校验 token,否则直接返回(`confirmations.ts:88-94`)。host 不判断"发送/删除/付款"是否高危——那写在 Skill 文本里(`skill.ts:126-145`),由模型自愿传 `sensitive:true`。**这是"safe input"自述与实际执行之间最值得注意的缝。**
- **提示成本最高三次**。未配置 grants 时:一次 `computer_observe` 要读批准,一次 `computer_confirm` 要敏感批准,真正 `act` 还要控制批准;三者的生命周期不同(Session / 一次性 / turn),不能互相替代(`leases.ts:197-257`、`confirmations.ts:60-84`)。
- **默认不过期。** `observationTtlMs: 0` 让 observationId 永久有效,新鲜度完全依赖"动作前重观测";如果 helper 侧观测与输入之间仍有竞态,防线是 `stateHash`,不是 TTL。想收紧必须自己配 TTL。
- **`allowAllApps: true` 是总开关。** 打开后 `configuredAccess` 对任何 bundleId 都返回 true,精确 grants 被忽略,连 `approval/policy: never` 也直接放行(`leases.ts:117-120`;`tests/service.spec.ts:1081-1092`)。默认是 false,但这是设置页第一屏的复选框。
- **DSH prerelease 耦合很紧。** 18 个 `@deepseek-ai/dsh-*` peer(含 `dsh-util-values`)都把可支持的预发布逐个列进 range。DSH 在安装/boot 时确实会检查:`engines.dsh` 优先,否则逐个 `satisfies()` 每个 `@deepseek-ai/dsh*` peer,任一不满足就拒绝安装并要求 `dsh plugin allow-version` 例外(本机 DSH `$DSH/node_modules/@deepseek-ai/dsh-app-boot/lib/index.js:279-298,311-325`)。本包没写 `engines.dsh`,所以生效的是那 18 个 peer——每支持一个新 prerelease 就要扩 18 处 range,漏一个就从 profile 掉出(CHANGELOG 0.3.4 记录过这个故障)。`dsh.compatibility` 的 15 个 release 与 `profiles: ["web"]` 是另一层声明式元数据:本机 DSH 0.2.1-rc.5 的 `*/lib` 里搜不到读取 `dshReleases` 的代码(**判断**:消费方是 dsh-plugin-check/hub,不是运行时);而 README 又让 Web 和 Headless 都装,`profiles` 只写了 `web`,两者口径不完全一致。
- **私有 SPI。** 定向指针动态解析 `SLEventPostToPid`/`SLEventSetIntegerValueField`/`CGEventSetWindowLocation`(`TargetedPointer.swift:39-49`)。系统不给符号时,语义 AX 与 pid 键盘仍可用,指针 fallback 直接 `COMPUTER_ACTION_BLOCKED`,不会切换到全局注入(`docs/interaction-policy.md:119-121`)。
- **供应链与维护。** helper 是 ad-hoc 签名(README:232),只做 `codesign --verify --strict`;没有 notarization/stapling 检查。仓库同时提交 `lib/`、client bundle、Swift 源、二进制与 manifest,`AGENTS.md` 要求任何改动后全部重建——一次改动要同步 4 类产物。仓库 5.9 MB,其中二进制 ~880 KB。
- **隐私。** 截图内容可能含其它应用数据,Skill 明说按敏感材料处理(`README.md:207`);secure 字段只在读侧脱敏(`[secure]`),**不禁止**向密码框写入——只是输入结果不回显、后续观测也不回读(`main.swift:465-471`、`tools.ts:416-428`)。

## 可信度与复现

证据等级 ★★★:TS 侧读过 `src/` 的 20 个文件(其中 `backend.ts`/`types.ts` 只读头部,`client/index.tsx` 读设置页与 slot 注册的关键段);Swift 侧读了 helper 的 transport、observe、secure、截图、指针、键盘、activation、action dispatch、main,以及 `TargetedPointer.swift`/`CursorOverlay.swift` 的关键行;测试读了 11 个 spec 的用例名与关键断言;另外对照了本机 DSH 0.2.1-rc.5 的 `dsh-tools`、`dsh-skill`、`dsh-settings`、`dsh-storage-domain`、`dsh-user-approval`、`dsh-host-webserver`、`lib/bin.js`。**未读**:`lib/` 编译产物逐行、`CursorOverlay.swift` 的大部分几何代码、`Fixture`/`Monitor` 全文、`scripts/model-e2e.mjs` 的真实模型路径、CHANGELOG 的 0.1.x 段。

```sh
# 1) 提交与历史(本卡在已克隆的 .work/mine/cards/computer-use/repo 上补了完整历史)
git -C .work/mine/cards/computer-use/repo log -1 --format='%H %ad'
# → 90444cf18d994840cd1046ca1ec7b420cf7c4a59 2026-11-12
git -C .work/mine/cards/computer-use/repo rev-list --count HEAD      # → 78
git -C .work/mine/cards/computer-use/repo tag | wc -l                # → 13

# 2) 规模
find src -name '*.ts' -o -name '*.tsx' | xargs wc -l | tail -1        # → 5466
find native/macos/Sources/Helper -name '*.swift' | xargs wc -l | tail -1  # → 2695
wc -l tests/*.ts | tail -1                                           # → 7104
grep -h -E '^\s*(it|test)\(' tests/*.ts | wc -l                      # → 182

# 3) 扩散(在 awesome-dsh-plugin 仓库根)
grep -ril 'computer-use' data/plugins/ | wc -l        # → 38
grep -ril 'dsh-computer-use' data/plugins/ | wc -l    # → 18
grep -ril 'anionex' data/plugins/ | wc -l             # → 3(全是同作者)
grep -ril 'Accessibility-first' data/plugins/ | wc -l # → 4
grep -ril 'stale-state\|stale observation' data/plugins/ | wc -l  # → 1(自身)

# 4) 实时值(2026-11-18 查,不替换 ⚠ 值)
curl -s https://api.github.com/repos/Anionex/dsh-computer-use | grep -E 'created_at|stargazers_count|size'
curl -s https://api.npmjs.org/downloads/point/last-month/@anionex/dsh-computer-use
# → 106 星;6,570 次/月(2026-10-18..11-16)

# 5) DSH 侧机制核对(本机安装的 dsh 0.2.1-rc.5)
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh
grep -n 'requiredOption("--profile' $DSH/lib/bin.js
grep -n 'bundlePatchFiles\|bundle.patch' $DSH/node_modules/@deepseek-ai/dsh-app-boot/lib/index.js
grep -n 'restrict(filter)' $DSH/node_modules/@deepseek-ai/dsh-tools/lib/index.js
grep -n 'defineDomain' $DSH/node_modules/@deepseek-ai/dsh-storage-domain/lib/index.js
```

## 待验证

1. **helper 重建后 TCC 授权是否还认。** ad-hoc 签名没有 Team ID,每次重建的 cdhash 会变;macOS 的 Accessibility grant 很可能要求重新授权。仓库没有任何测试覆盖"升级后免重授",这决定 `dsh plugin` 升级的实际体验。
2. **敏感动作没有 host 侧分类器。** 需要确认 DSH 或 hub 是否在工具描述/schema 之外加了强制策略;就本仓库源码看,`sensitive` 完全由模型声明。若没有,`computer_confirm` 是"礼貌性"闸门而非强制闸门。
3. **IME 实测。** 在中文/日文输入法激活时,`press-key`(物理 keycode)与 `type-text`(Unicode 注入)分别会得到什么;仓库 e2e 只测了直接注入 `Background 深度🌿 42.`,没有测组合输入。
4. **双显示器 / 多 Space 实测。** 代码用 `.optionAll` + `.optionOnScreenOnly` 的组合处理多屏,但只有静态测试与文档;光标 overlay 的"单 Space、单前台 app"限制在真实双屏下是否可接受,未跑。
5. **`dsh.compatibility.profiles: ["web"]` 的消费方。** 本机 DSH 不读它;若是 dsh-plugin-check/hub 的字段,headless 安装是否会被判为不支持?需要看检查器源码或实跑 `dsh plugin --profile headless add`。
6. **升级/回滚路径。** `reconfigure` 会清空 observation 与 confirmation,但 sidecar 里的读授权会跨 generation 保留;0.2.x 的 `cursorMotionMs` 被接受但忽略。跨版本升级时旧 Settings 文档与旧 sidecar 行的兼容性,没有迁移测试。
7. **星标曲线。** 22(08-19)→ 106(11-18)只有两个点;GitHub API 的 stargazers 时间线未取(未授权会 401),无法判断增长是发布日脉冲还是持续。
