---
kind: card
domain: personal_agent
subcategory: cross-device-agents
repo: chenkezhen480/dsh-world
commit: aab873ab110a7050b32055f760d79bb6c021968c
evidence: 3
status: active
asof: 2026-11-27
---

# dsh-world — 单依赖纯 DSH 插件搭建“自唤醒时间线 + 无工具压缩 + 微信/QQ + 独立浏览器/桌面”常驻个人世界

> 证据等级 ★★★(源码级;`chenkezhen480/dsh-world@aab873ab`)。未在 Windows 实机跑测试、未验证 C++ 微信 DLL 注入与 SnowLuma 联调;生命线、无工具压缩、记忆存储、QQ/微信适配器与浏览器/桌面操控均经源码逐文件核验。
> **未收录于 `awesome-dsh-plugin` 注册表**(GitHub + npm `dsh-world@0.8.5` 独立分发)。星标 454★ / 21 forks 为 2026-11-27 GitHub API 实时值。

## 它替谁解决什么问题

**想把一台常开 Windows 个人电脑里的 DSH 变成一个真正“24/7 活着、自己定闹钟、每天 23:00 写日记并复盘自我、能在微信/QQ 找你、又能用独立浏览器和后台桌面替你办事”的单一常驻伙伴,但不想部署 Docker/Postgres/向量库重型基础设施的个人用户。** 现有方案的痛点很具体:

- **会话不说话就彻底死掉**:普通 DSH 必须人发消息才动,定个简单 cron 又容易因为重启丢状态或忘掉上次干了什么。
- **工具调用记录把上下文和压缩质量全毁了**:长周期生活对话混入大量工具输出,标准压缩要么把对话情绪压没,要么中途改系统提示打穿前缀缓存。
- **桌面操控一动鼠标就抢焦点、关不掉**:普通 CUA 工具一跑就抢走用户正在用的键盘鼠标,也没有紧急停机开关。

`chenkezhen480/dsh-world` 用极轻的依赖(运行时仅 `ws` 一个 npm 包 + Node 内置 `node:sqlite`)实现了可复现的持久化闹钟、无工具压缩引擎、夜间日记与自我演化(`我.md`)、自学习浏览器步骤与带双按 `Esc` 急停的 Windows 后台/前台桌面操控。

## 适用面:谁该用、谁别用

- **适合**:个人常开 **Windows x64** 电脑、跑 DSH `0.2.1-rc.2`~`0.2.2-rc.1` + Node ≥22.16.0 的个人极客;看重“低依赖(无外部 DB/向量库)+ 夜间复盘 + 后台不抢鼠标桌面操控 + 多世界实例”的个人常驻体验。
- **不适合**:**macOS / Linux 主力用户**(虽核心记忆与闹钟跨平台,但微信适配器、桌面操控、任务栏监控、Toast 通知甚至**浏览器路径探测 `edge.ts:9-15` 全是 Windows 专属**,在 macOS/Linux 上开浏览器会直接报找不到 Edge/Chrome);**任何商业/SaaS/收费机器人场景**(仓库顶层挂 MIT,但 `src/ecosystem/wechat/windows/engine/LICENSE` 是**非商用许可 `LicenseRef-helper-noncommercial-1.0`**);对微信封号风险零容忍、或无法接受本机无 token 控制台 HTTP 路由及非 owner 共享主会话权限的多人/团队环境。
- **前置条件**:Node ≥22.16.0、DSH `0.2.1-rc.2`~`0.2.2-rc.1`(安装必须用 DSH 自带 `pnpm`);启用 QQ 需额外运行非官方本地网关 SnowLuma;启用 Windows 微信需 Visual Studio C++ x64 构建工具且微信版本精确命中 `profiles.json` 支持的 8 个 `4.1.15`–`4.2.1.9` 构建号。

## 业务价值

- **能算清的**:
  - **454★ / 21 forks / 10 open issues**(2026-11-27 实时值,建仓 1 个月连发 15 个 npm 版本至 `0.8.5`,与 HEAD 同步),配 **97 个零框架测试文件(15,695 行)**。
  - **极低运行时依赖**:整个插件 `package.json` 只有 **`ws` 一个 runtime dependency**,记忆归档直接用 `node:sqlite`,桌面操控直接用内置 PowerShell(`win32.ps1`),浏览器直接用原生 CDP,大幅降低安装链复杂度。
  - **显式预算与防静默机制**:按人民币追踪每日 `assistant/message` 成本(`dailyBudget`),到额只提醒一次且停掉续问;闹钟落盘确认直到会话日志真正出现对应 `messageId`,5 分钟停滞自动重试。
- **只是预期(推断)**:
  - 无向量库纯子串检索 + 冷启动才注入历史(保前缀缓存)+ 去工具中文单段压缩,在个人长周期陪伴与轻量任务场景下可能兼顾省钱与连贯性,但缺少大规模真实用户留存与压缩保真度对比数据。

## 一屏事实

| 项 | 值 |
|----|----|
| 仓库 / 注册状态 | `chenkezhen480/dsh-world`(**未收录于 `awesome-dsh-plugin`**,GitHub + npm `dsh-world@0.8.5` 独立分发) |
| 子分类 | `cross-device-agents`(跨设备与常驻个人 Agent) |
| 自述 | DSH 跨会话记忆、人格与生活节律插件,带世界控制台、无工具压缩、原生 QQ/Windows 微信与自主浏览器/桌面 |
| 星标 / fork(2026-11-27) | **454★ / 21 forks / 10 open issues**;创建 `2026-10-24`,最近 push `2026-11-27` |
| 包形态 / 许可 | 单 DSH 插件包(`dsh-world@0.8.5`)+ 可选 2.5D 小屋包(`dsh-world-room@0.1.0`);顶层 MIT,**但内置微信 C++ 引擎为非商用 `LicenseRef-helper-noncommercial-1.0`** |
| 代码规模 | 非测试 **173 文件 / 24,835 行**(`src/` 20,202 行 + `dsh-world-room` 2,776 行 + 零构建 `client/index.js` 1,467 行);测试 **97 文件 / 15,695 行** |
| 宿主钉版 | `node >=22.16.0`, `dsh: ">=0.2.1-rc.2 <0.3.0-0 \|\| >=0.2.2-rc.1 <0.3.0-0"`;**仅 1 个 runtime dep(`ws`)** + 11 核心/4 可选 peerDeps |
| repo@commit | `aab873ab110a7050b32055f760d79bb6c021968c`(2026-11-25 +0800) |
| 证据等级 | ★★★ |

## 它到底是什么

**一套以“持续时间线 + 自我演化文档”为核心的纯 DSH 个人常驻世界插件,而非多 Bot 协作平台。** 它围绕一个规范主会话(`homeSessionId`)维持永不彻底沉睡的生活节律(`src/life/runtime.ts`),把对话、日记、维基与自主浏览器/桌面步骤全部落盘在 `<dshHome>/worlds/<worldId>/` 下(支持同 profile 挂载多个独立 `worldId` 实例):

```text
自唤醒闹钟(life.json 落盘确认) / 23:00 夜间复盘 / QQ(SnowLuma) / 微信(Win DLL) / Windows 任务栏通知
  → homeSessionId(仅首轮/压缩后/冷启动 24h 注入 dsh-world-history 保 KV 缓存)
  → 行动面:独立 user-data-dir Edge/Chrome CDP(含 procedure_* 自学习) + Win32 后台/UAC 前台桌面操控(双按 Esc 急停)
  → 沉淀:archive.sqlite(零向量纯子串查) + 无工具中文压缩 + 历史日记只读守卫 + 我.md 夜间备份自改
```

## 怎么接进 DSH

1. **6 行 Patch + 零构建客户端(`cordis.patch.yml:1-6`, `client/index.js:1427-1466`)**:仅插入 `id: dsh-world`,前端为无打包 IIFE React 模块,在设置页挂入单栏 `世界控制台`(`settings.section`, order 28),并注册 `/dsh-world/worlds/<worldId>/{console,qq,room,bridge,wechat/ask}` HTTP 路由。
2. **启动期主动修改宿主 profile 配置(强耦合细节)**:
   - 首启默认(`replaceCompaction: true`)自动备份并把 profile 里的 `@deepseek-ai/dsh-compaction-basic` 替换成自研 `dsh-world/compaction`,并顺手修补旧复制 preset 里 `0.2.2` 已废弃的 `list-agents`(`src/compactionSwap.ts:28-45, 102-156`)。
   - 控制台开关 QQ/小屋时,直接调用内部 `@deepseek-ai/dsh-plugin-manager/operations`(`runProfilePnpm`)在线执行 `pnpm add --ignore-scripts` 并带 `package.json`/`pnpm-lock.yaml` 原子回滚(`src/packageInstall.ts:49-98`);新增多世界直接往 `cordis.patch.yml` 追加文本(`src/worldAdd.ts:16-39`)。
   - 顶层显式 `import 'ws'` 绕过 `dsh-hmr` 热重载丢懒加载 CJS 的问题(`src/index.ts:3-7`)。
3. **严格作用域围栏(`src/runtime.ts:60-169, 441-460`)**:会话一旦切离世界工作区或世界停用,立即用空 `system/message` 替换撤回历史记忆块并以 `DSH_WORLD_SCOPE_CHANGED` 中止请求。

## 关键实现

| 模块 | 位置 | 作用与源码实证 |
|---|---|---|
| 持久闹钟与永不静默环 | `src/life/{runtime,alarm,alarmTurn}.ts` | `plan_next` 写盘 `state.delivering`,直到会话日志真出现对应 `messageId` 才算送达;5 分钟停滞重试;`turn-stopping` 无闹钟则催促一次,仍无则次日 09:00 兜底;附带客观工具活动账本 `didSince` 核对自述防幻觉 |
| 零向量记忆与无工具压缩 | `src/{store,memory,memoryTools,runtime,compaction}.ts` | `archive.sqlite`(WAL + `FULL`)镜像 JSONL;明确弃用实体图谱与向量索引,直接子串查(默认 8 条/200 字);`toolFreeMessages` 剥离全部 tool 角色与调用体,只留工具名清单,75% 窗口压成单段中文 |
| 夜间复盘与日记只读门 | `src/self.ts`, `src/life/diary.ts:14-40` | 23:00 先备份 `我.md` 到 `我.history/YYYY-MM-DD.md` 再允许自我改写(注入上限 5,000 字);拦截 `write`/`edit` 工具禁止篡改往日已封存日记及非主会话改 `wikiDir`(注:不拦 shell 工具) |
| 自主浏览器与自学习步骤 | `src/ecosystem/computer/{tools.ts,browser/edge.ts,README.md}` | 起独立 `--user-data-dir` Edge/Chrome(禁用扩展与同步),经原生 CDP 提供 9 个 `page_*` + 4 个 `procedure_*` 工具,支持 JSON 步骤失败自动 2 版本回滚及闹钟前只读预执行(`onAlarm: true`) |
| Win32 后台/UAC 前台桌面 | `src/ecosystem/computer/{index.ts,desktop/{desktop,driver}.ts}` | 后台模式 `PrintWindow`+`PostMessage` 不抢鼠标且拒碰提权窗口;前台模式**不持久化**,每会话须重新过 Windows **UAC(`RunAs`)**,提权进程回连随机命名管道 `\\.\pipe\dsh-world-<32hex>` + 24 字节一次性密钥;配蓝框视觉提示与 0.5 秒双按 `Esc` 急停锁 |
| QQ 与 Windows 微信通道 | `src/ecosystem/qq-native/index.ts`, `qq/supervisor.ts`, `wechat/{index.ts,windows/adapter.py}` | QQ 走 SnowLuma OneBot 11 WS + 30 秒看门狗自动拉起 + `roomFilesOnly` 防外传主机文件;微信通过**解密本地 `xwechat_files` SQLite 读消息 + 编译 C++ DLL 注入 `Weixin.exe` 调硬编码内存地址发消息**(含 `outbox` 与 `EXIT_NEEDS_HUMAN` 人工对账防重发) |

## 为什么它突出

只用本仓库自身证据:

- **极简依赖做出极完整的个人常驻闭环**:仅 1 个 runtime 依赖(`ws`),却覆盖了持久闹钟、防缓存穿透记忆、无工具压缩、夜间自我复盘、自学习浏览器与带双 `Esc` 急停的后台桌面操控。
- **工程细节克制且务实**:用实测否决了实体图谱/向量索引的复杂度;用 UAC 不落盘 + 一次性管道密钥 + 双 `Esc` 急停处理前台桌面高危权限;用 `messageId` 日志回执解决异步唤醒丢消息。
- **零构建客户端 + 原生多世界扩展**:不用打包器直接跑 1,467 行前端控制台,并在同 profile 内支持多 `worldId` 隔离并行与按需装 2.5D 小屋(`dsh-world-room`)。

## 代价与边界

1. **许可冲突与微信封号高风险(源码实锤)**:顶层仓库标 MIT,但 `src/ecosystem/wechat/windows/engine/LICENSE` 是**非商用 `LicenseRef-helper-noncommercial-1.0`**,明确禁止任何商用/SaaS/付费机器人集成;且微信发送机制为 C++ DLL 内存注入 `Weixin.exe`(仅匹配 8 个精确版本号),README 自身已警告 2026-01-29 微信安全中心整治带来的封号风险。
2. **重度绑死 Windows**:微信、桌面操控、任务栏通知、Windows Toast 乃至浏览器启动(`edge.ts:9-15`)全限 Windows;macOS/Linux 仅能跑核心记忆与闹钟。
3. **QQ 通道单点依赖非官方 SnowLuma**:强耦合 SnowLuma 专有事件与路径,若上游关停或腾讯封禁则 QQ 通道直接瘫痪。
4. **权限与本地 HTTP 安全缺口**:
   - `/console/*` 与 `/qq/*` 写路由**没有 Bearer Token**,仅靠 `knownHost` + `sec-fetch-site` + 自定义头 `x-dsh-world: 1`(`console/routes.ts:218-230`),本机其他进程可直接操控世界甚至拉起 UAC 申请。
   - **缺乏说话人分级隔离**:白名单内所有微信私聊及 `bindHomeSession: 'owner'` 下的所有 QQ 私聊均直接进入主会话,继承完整桌面/浏览器工具权限(`wechat/windows/README.md:110`, `index.ts:379,410-414`);日记/维基写守卫也不拦截 shell 命令(`diary.ts:14`)。
5. **主动改写宿主配置与默认联网检查**:首启修改 `cordis.patch.yml`,且默认每天请求 `registry.npmjs.org` 查更新(`updateCheck: true`)。

## 可信度与复现

**读过**:`package.json`、`cordis.patch.yml`、`CLAUDE.md`、`INSTALL.md`、`src/{index,runtime,compaction,compactionSwap,hostContract,workspacePermissions,self,promptSection,memory,memoryTools,store,http,worldAdd,packageInstall}.ts`、`src/life/{runtime,alarm,alarmTurn,diary}.ts`、`src/console/routes.ts`、`src/cottage/index.ts`、`src/ecosystem/qq-native/{index,snowluma}.ts`、`src/ecosystem/qq/supervisor.ts`、`src/ecosystem/wechat/{index.ts,windows/{adapter.py,README.md,engine/LICENSE}}`、`src/ecosystem/computer/{index.ts,tools.ts,README.md,browser/edge.ts,desktop/{desktop,driver}.ts}`、`client/index.js` 关键段。**未读**:`win32.ps1` 与微信 C++ `engine/` 源码正文,未做 Windows 实机测试。

```sh
git clone --depth 1 https://github.com/chenkezhen480/dsh-world && cd dsh-world
git rev-parse HEAD   # aab873ab110a7050b32055f760d79bb6c021968c
node --experimental-strip-types --test
```

## 待验证

- 未实测无工具压缩(`dsh-world/compaction`)在超长周期(数周)个人生活对话中的信息保留率。
- 未验证 `win32.ps1` 在高 DPI 多屏与 Windows 11 24H2 下的后台 `PrintWindow`/`PostMessage` 兼容性。
- 未核验 `dsh-world` 在 npm 上的月下载量。
