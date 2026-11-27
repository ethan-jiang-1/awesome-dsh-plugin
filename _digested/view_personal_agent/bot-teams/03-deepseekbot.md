---
kind: card
domain: personal_agent
subcategory: bot-teams
repo: BotHarness/DeepSeekBot
commit: b296cac78848cc9473317f7e34ba6fb8c3a4f3c6
evidence: 3
status: active
asof: 2026-11-27
---

# BotHarness/DeepSeekBot(Tobs 托布) — 85 万行代码的 DSH 多插件编排层,用 Git 记忆 + Noise XK 跨端中继复刻 Grok Bot

> 证据等级 ★★★(源码级;`BotHarness/DeepSeekBot@b296cac7`)。未执行 Vitest、Maestro 与实机 DSH `0.2.2-rc.1` 联调;架构、多 Bot 调度、Git 记忆、私有凭据与隔离边界均经源码逐文件核验。
> **未收录于 `awesome-dsh-plugin` 注册表**(GitHub 与 npm `@botharness/tobs` / `deepseekbot` 独立分发)。星标 1,076★ / 81 forks 为 2026-11-27 GitHub API 实时值;npm `latest`(`1.7.0`,2026-11-12)落后 `main`(11-27)15 天。

## 它替谁解决什么问题

**想在现有 DeepSeek Harness 生态里拥有一套完整对标 xAI Grok Bot 的“多 PersonaBot 个人工作台 + 手机端远程操控 + 跨渠道 IM 接入”、又希望把长期记忆纳入 Git 版本管理、并复用本机已有 Claude Code / Codex 订阅的个人重度用户与小团队。** 自己拼装 DSH 插件面临四个痛点:

- **每个 Bot 缺乏持久身份与可审计记忆**:普通会话切换工作区就断了上下文,改坏记忆也没法 diff 回滚。
- **多个 Bot 进群或后台定时干活容易死循环**:互相 `@` 会刷爆额度,或并发发言时忽略别人刚发的新消息。
- **给 Agent 填 API 密钥/登录凭据没有中间层**:直接贴进对话就会进上下文与日志。
- **离开电脑就失联**:需要同时配移动端、内网穿透、IM 桥与浏览器/桌面操控。

`BotHarness/DeepSeekBot`(品牌名 Tobs 托布)不是独立套壳 App,而是把一整套包含 `@botharness/{core,ui,browser,computer,im-provider}`、原生 Expo 移动端与 Cloudflare Workers 中继的超级 DSH 插件包挂进宿主。

## 适用面:谁该用、谁别用

- **适合**:运行 DSH `>=0.2.0-0`(实测围绕 `0.2.2-rc.1`/`rc.2`)的个人重度用户与 Linux 服务器小团队;需要为每个 Bot 配独立 Git 记忆仓(`SOUL.md`/`MEMORY.md`)、定时任务、托管 Chromium/桌面容器、Noise XK 加密手机端与飞书/微信/QQ/Slack/Discord(经 `dsh-im` 契约)入口的人。
- **不适合**:在 **Windows 或 macOS** 上依赖 OS 级强沙箱保护凭据或做多成员 Team 隔离的组织——ADR-0192 已删除 Docker 私有凭据围栏,`.credentials.yaml` 的 OS 级只读拦截仅覆盖 macOS `sandbox-exec` 与 Linux `bwrap`(Windows 与 Linux Landlock 退化为纯命令文本正则拦截,`store-guard.ts:77-100`, `mount.ts:89-95`),而 Team 成员 OS 隔离直接跳过非 Linux 平台(`if (platform !== 'linux') return;`, `member-confinement.ts:163-168`);也不能接受**单向不可逆 SQLite 迁移(199 个迁移)**、默认开启遥测(`telemetry: true`)及依赖作者域名(`media.botharness.ai`/`market.botharness.ai`)的离线/强内网环境。
- **前置条件**:Node ≥22(使用内置 `node:sqlite`)、DSH Desktop `>=0.2.0-0`(桌面缩放补丁严格按 `0.2.2-rc.1`/`rc.2` 校验 SHA256);接 IM 需换用 `cordis.im.patch.yml` 安装 `@botharness/im-provider`。

## 业务价值

- **能算清的**:
  - **1,076★ / 81 forks / 572 open issues**(2026-11-27 实时值,建仓 2 个多月持续日更至 PR #5554),是 GitHub 上未入库 `awesome-dsh-plugin` 的 DSH 原生 Grok Bot 替代品中的头部重工程仓。
  - **可核验工程体量**:非测试源码 **4,429 文件 / 851,962 行**,配 **2,563 个测试文件(590,237 行)**,核心发布包 `@botharness/{tobs,core,ui,browser,computer,im-provider}` 均已上架 npm(`1.7.0`)。
  - **记忆与凭据机制可数**:每个 Bot 独立 Git 仓管理 `SOUL.md`(默认 5,000 字)与 `MEMORY.md`(默认 3,000 字),每 Bot 最多 20 条启用的定时任务,并内置 `ask_secret` + `secret_http`/`secret_cli` 凭据代填掩码。
- **只是预期(推断)**:
  - Orchestrator(单主脑排收件箱)+ 并发 Assignment(按授权工作区隔离派活)+ 复用本地 Codex/Claude 订阅的设计可能大幅扩展单人跨项目并发能力,但缺少真实生产稳定性与 Token 消耗统计。

## 一屏事实

| 项 | 值 |
|----|----|
| 仓库 / 注册状态 | `BotHarness/DeepSeekBot`(**未收录于 `awesome-dsh-plugin`**,GitHub + npm 独立分发) |
| 子分类 | `bot-teams`(多 Bot 个人工作台,仿 Grok Bot / OpenAI Dots) |
| 自述 | "BotHarness — a DeepSeek Harness plugin layer that gives agents a persistent identity (PersonaBots)"(`tobs.app`) |
| 星标 / fork(2026-11-27) | **1,076★ / 81 forks / 572 open issues**;创建 `2026-09-16`,最近 push `2026-11-27` |
| 包形态 / 许可 | 多包 DSH bundle(`@botharness/tobs`、`deepseekbot`、`@botharness/{core,ui,browser,computer,im-provider}`均发 npm `1.7.0`)+ Expo 移动端 + Cloudflare Relay;**MIT** |
| 代码规模 | 非测试 **4,429 文件 / 851,962 行**(`core` 26.4 万行、`client` 22.6 万行、`mobile` 13.3 万行、`scripts` 11.2 万行);测试 **2,563 文件 / 590,237 行** |
| 宿主钉版 | `engines.dsh: ">=0.2.0-0"`,devDeps 钉 44 个 `@deepseek-ai/dsh-*@0.2.2-rc.1`;仓库含 5 个针对 `@deepseek-ai/*` 的 pnpm patch 与 27 处宿主类型强转基线 |
| repo@commit | `b296cac78848cc9473317f7e34ba6fb8c3a4f3c6`(2026-11-27 +0900) |
| 证据等级 | ★★★ |

## 它到底是什么

**一套把 DSH 宿主升级成“多 PersonaBot 操作系统 + 跨机移动网络”的超大规模 Cordis 插件矩阵。** 核心调度模型把每个 PersonaBot 拆成两类会话(`docs/architecture/botharness-architecture.md:106`, `packages/core/src/runtime/bot-runtime.ts:128-250`):

```text
私聊 / 群消息 / Bot 互聊 / IM 渠道(dsh-im v1) / 定时任务(≤20/Bot) / 子任务回报
  → Bot Inbox(botharness.db 199 迁移 SQLite)
  → 1 个 Orchestrator 会话(cwd = Bot 专属 Git 记忆目录,持有快照版 SOUL.md + MEMORY.md)
  → 并发派生 N 个 Assignment 会话(各绑 1 个 workspace_grants 授权目录;或切到本机 Codex/Claude 订阅引擎)
  → 通过 @botharness/browser / @botharness/computer / secret_http / secret_cli 执行外部动作
```

内置元 Bot **Tob**(`core.ts:352-360`)负责用受控 `tobCli` 管理其他 Bot 与设置;前端 `@botharness/ui` 借助 `dockview-core` 在 DSH Web 内接管多面板布局,并配独立 Expo React Native App 经 Noise XK 端到端加密(LAN / Tailscale / Cloudflare Workers 中继)远程连回家中电脑。

## 怎么接进 DSH

1. **Bundle 注入 4 插件 + 4 Preset(`packages/deepseekbot/cordis.patch.yml:1-340`)**:挂入 `botharness-core`、`botharness-client`、`botharness-browser`(`headless: true`)、`botharness-computer`(`target: local`),并同步生成 `preset-deepseekbot`(Tobs 主预设,禁用原生 `dsh-tool-subagent` 改用自研 `bot_subagent`,禁用内置插件管理器/市场,把 `tool-ask-user` 改为 45 秒定时模式)及 `调研 / 编程 / 脚本` 3 套窄权限子预设。IM 版 `cordis.im.patch.yml` 在最前插入 `xmanrui-dsh-im`(`@botharness/im-provider`)。
2. **宿主服务与前缀注入(`packages/core/src/plugin.ts:93-103, 407-443, 737-873`)**:强注入 7 个核心服务(`tools/systemPrompt/sessions/agents/agentDefaultModel/llm/credentials`),按需注入 `workspaceRegistry/connection/storageDomain/sandbox`,对外 `ctx.provide('botharness', core)`,在 `order: 10400` 挂入 `botharness:persona` 并接管 HTTP/RPC 路由。
3. **前端包避坑与桌面缩放补丁**:因 DSH RC2 会把包名尾部 `/client` 误判为导出子路径,前端包特意命名为 `@botharness/ui`(ADR-0066,`botharness-architecture.md:122`);可选工具 `desktop-zoom-setup.mjs:80-194` 会改写桌面 profile 的 `package.json` 符号链接 `@deepseek-ai/dsh-client-ui-theme` 到精确版本补丁(`0.2.2-rc.1`/`rc.2`),不匹配直接拒装。

## 关键实现

| 模块 | 位置 | 作用与源码实证 |
|---|---|---|
| SQLite 状态与单向迁移 | `packages/core/src/database/{owner,schema-plan}.ts` | Node 内置 `node:sqlite`(`botharness.db`),含 **199 个命名迁移**,采用副本预迁移 + 页完整性/外键孤儿检查 + profile 写租约锁 |
| Git 记忆与前缀缓存保活 | `packages/core/src/memory/{managed-git,soul,standing-limits,service}.ts` | 每 Bot 独立 Git 仓(缺系统 git 时从 `media.botharness.ai` 校验 SHA256 下载 `dugite-native`);`personaForSession` 首读冻结快照,仅在压缩后 `refreshPersonaAfterCompaction` 刷新以保 KV 缓存;每轮变更走 `prepareTurn/reconcileTurn/abortTurn` 提交可回滚 |
| 防环派活与订阅引擎 | `packages/core/src/runtime/bot-runtime.ts`, `schedules/bot-schedules.ts`, `engines/engine-host.ts` | `botHopLimit` 防 Bot 互聊死循环;群发送复核在同伴插入新消息时暂缓回复(最多 2 轮);每 Bot 最多 20 条 `dsh-schedule` 定时任务;支持挂载本机 Codex 与 Claude Code(`@anthropic-ai/claude-agent-sdk`)订阅引擎 |
| 私有凭据与代填工具 | `packages/core/src/credentials/{mount,protected-execution,store-guard}.ts` | `ask_secret` 仅允许 Owner Web 端录入并绑 Bot 代次 UUID(15 分钟超时);模型只见不透明句柄,经 `secret_http`(禁重定向、响应 ≤32KB 掩码含 base64/URL 编码)与 `secret_cli`(无 shell、净环境变量、2 分钟限)使用 |
| IM 契约与配对围栏 | `packages/core/src/messaging/{dsh-im,pairing}.ts`, `platforms/{weixin,qq}.ts`, `team-policy/permissions.ts` | 经 `dsh-im` 契约 v1 接 5 渠道(微信扫码仅私聊、QQ 官方群/私聊);陌生 IM 发送者须 Owner 配对(`PairingRequest` 10 分钟过期、限 5 次尝试)授予细粒度权限;Team 模式含 20 项 RBAC 权限(`privateContent.view` 等仅限 Owner) |
| 浏览器、桌面与跨端中继 | `packages/browser/src/index.ts`, `packages/computer/src/index.ts`, `packages/connect-relay/` | Playwright 托管 Chromium 5 种目标(含 `selkies-webrtc` 接管);桌面操控支持本机/容器 VNC(`/botharness-computer/viewer`);移动与跨机走 Noise XK(`@noble/*`)加密经 LAN/Tailscale/Cloudflare Workers 中继 |

## 为什么它突出

只用本仓库自身证据:

- **DSH 生态目前工程深度最全的插件式个人 Bot 平台**:超过 85 万行非测试代码 + 59 万行测试 + 27 处宿主强转棘轮门禁(`scripts/check-host-casts.mjs`),同时把多 Bot 编排、Git 记忆、托管浏览器/桌面、IM 渠道与 Noise XK 移动端打通在原生 DSH 体系下。
- **真正做了“对 LLM 不可见”的凭据代填原语**:`ask_secret` + `secret_http` + `secret_cli` 在 DSH 原生插件里实现了接近 Muse `hatch-authd` 的代理注入与响应掩码思路。
- **兼顾缓存与审计的 Git 记忆设计**:把 `SOUL.md`/`MEMORY.md` 纳入每 Bot 独立 Git 仓,并用冻结快照避免回合内编辑记忆打穿 LLM 前缀缓存。

## 代价与边界

1. **OS 级隔离存在严重跨平台断层(源码实锤)**:
   - Docker 私有凭据沙箱已在 ADR-0192 中**删除**(`plugin.ts:141-145`);保护 `.credentials.yaml` 的 OS 级只读拦截只支持 macOS `sandbox-exec` 与 Linux `bwrap`,**Windows 与 Linux Landlock 下仅剩命令字符串静态正则检查**(`store-guard.ts:77-100`, `mount.ts:89-95`),可被脚本/环境变量间接读取绕过。
   - Team 成员 OS 隔离 `installMemberConfinement`(`member-confinement.ts:163-168`)**仅在 Linux 生效**(`if (platform !== 'linux') return;`),macOS 与 Windows 下多 Bot 成员无 `bwrap` 隔离。
2. **体量与宿主耦合极重**:85 万行代码、44 个 DSH `0.2.2-rc.1` 开发依赖、5 份 `@deepseek-ai/*` 工作区补丁、199 个**单向不可逆** SQLite 迁移(`README.md:118`),桌面缩放补丁硬绑定精确 RC 版本。
3. **默认外部依赖与遥测**:默认 `telemetry: true`(`plugin.ts:131,175-179`),并连接 `market.botharness.ai`、`media.botharness.ai`(托管 Git 下载)与 Cloudflare 中继。
4. **npm 发布滞后**:2026-11-27 核查时 npm `1.7.0`(11-12)落后 GitHub `main` 15 天。

## 可信度与复现

**读过**:根与 7 个子包 `package.json`、`cordis.patch.yml`、`cordis.im.patch.yml`、`docs/architecture/botharness-architecture.md`、`packages/deepseekbot/src/{deepseekbot,desktop-zoom-setup}.mjs`、`packages/core/src/{plugin,core}.ts`、`database/{owner,schema-plan}.ts`、`bots/registry.ts`、`memory/{managed-git,soul,standing-limits,service}.ts`、`runtime/bot-runtime.ts`、`schedules/bot-schedules.ts`、`credentials/{protected-execution,store-guard,mount}.ts`、`execution/member-confinement.ts`、`team-policy/permissions.ts`、`workspaces/grants.ts`、`messaging/{dsh-im,pairing,platforms/weixin,platforms/qq}.ts`、`engines/engine-host.ts`、`packages/{browser,computer}/src/index.ts`、`scripts/check-host-casts.mjs`。**未读**:`voice/` WebRTC、`devices/` Noise XK 握手与 `apps/mobile/` 正文,未跑实测。

```sh
git clone --depth 1 https://github.com/BotHarness/DeepSeekBot && cd DeepSeekBot
git rev-parse HEAD   # b296cac78848cc9473317f7e34ba6fb8c3a4f3c6
npm view @botharness/tobs version
```

## 待验证

- 未实测 npm `1.7.0` 在干净 DSH `0.2.2-rc.5` 上不打工作区 pnpm patch 能否顺利启动。
- 未读 `packages/core/src/devices/` 与 `packages/connect-relay/` 核验 Noise XK 密钥固定与重放防护细节。
- 未核验 `@botharness/tobs` 与 `deepseekbot` 的真实 npm 月下载走势。
