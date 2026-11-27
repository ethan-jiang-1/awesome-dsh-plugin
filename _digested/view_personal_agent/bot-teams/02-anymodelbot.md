---
kind: card
domain: personal_agent
subcategory: bot-teams
repo: modelflare-ai/AnyModelBot
commit: 06b05e2627675c2347735f4d477583301787ae08
evidence: 3
status: active
asof: 2026-11-27
---

# AnyModelBot — 5,006★ 本地优先 Grok Bot / Dots / Duet 复现,按“每 Bot 一独立 DSH 子进程”内嵌运行时

> 证据等级 ★★★(源码级;`modelflare-ai/AnyModelBot@06b05e26`)。未运行 Vitest、Electron 打包或 Docker 实机联调;`dsh-runtime` 打包、18 个内部 Cordis 插件、Linux `bwrap` 读围栏、应用 4 级分类门禁、Computer Use 默认配置与凭据存储均经源码逐文件核验。
> **未收录于 `awesome-dsh-plugin` 注册表**(私有 Electron/Docker 独立产品,`package.json` 为 `private: true`,未发 npm,底层直接打包 `@deepseek-ai/dsh@0.2.1-rc.4`)。星标 5,006★ / 124 forks 为 2026-11-27 GitHub API 实时值。

## 它替谁解决什么问题

**想在自己电脑或 NAS 上零门槛跑起对标 xAI Grok Bot / OpenAI Dots / Claude Duet 的多 Bot 个人助手——支持微信扫码/飞书/TG/Slack/Discord、直连飞书/腾讯文档/高德/语雀/Notion/GitHub、还能随意切换 70+ 模型(或自带官方 API Key)——但不愿手动配 DSH profile、不想让模型见到真实 API Key 的桌面与 NAS 个人用户。** 现有方案的痛点很具体:

- **直接用 DSH 插件生态门槛高**:用户得自己装 DSH、配多渠道 IM、配多模型路由、再装一堆不统一审批格式的应用连接器。
- **单进程跑多 Bot 容易串权或泄密钥**:所有 Bot 共享一个 DSH 进程和环境变量,上游模型 Key 与应用 OAuth 密钥难以彻底隔离在子进程之外。
- **开全权限(`danger-full-access`)怕误删文件**:一放开权限连 `rm -rf` 或外发消息都没刹把。

`modelflare-ai/AnyModelBot` 走的是与插件截然不同的**“独立宿主内嵌 DSH 子进程”**路线:把 `@deepseek-ai/dsh@0.2.1-rc.4` 打进 `resources/dsh/dsh.asar`,每激活一个 Bot 懒启动一个隔离 `DSH_HOME` 的独立 SDK 子进程,并用本地回环 `AgentBridge` + 托管 Go `magpie` 网关把所有真实密钥挡在子进程之外。

## 适用面:谁该用、谁别用

- **适合**:想用现成 Electron 安装包(macOS/Win/Linux)或 Docker 镜像在个人电脑/NAS 跑多 Bot + 微信/飞书/国内外应用连接器的非重度运维用户;以及研究「每 Bot 独立 DSH 子进程」「Linux `bwrap --tmpfs` 强读围栏」「4 级应用写/删/发门禁」「全权限递归删除拦截」的架构师。
- **不适合**:想在已有 DSH Web/Desktop 里通过 `dsh plugin add` 叠加使用的纯插件用户(它是独立宿主,不是插件);要求不登录 Modelflare 账号即可用全功能的纯 BYOK 用户——**Bot 互聊协作(`collab/service.ts:5-6,200-243`)、每 Bot 美元预算、文生图/视频与 Responses 服务端压缩全部硬锁 Modelflare 登录**;以及对默认配置敏感的强安全环境——**源码实测 Computer Use 默认 `enabled: true, approval: 'auto'`(点击/打字免审批,`bot-settings.ts:111`),官方 Docker 镜像默认开 `AMB_ALLOW_LANDLOCK=1` 削弱 `<dataDir>` 读隔离,且 macOS/Windows 下全部本地凭据均明文落盘且无 `bwrap`/`peer-guard`**。
- **前置条件**:下载 GitHub Releases 桌面安装包或拉取 `ghcr.io/modelflare-ai/anymodel-bot` Docker 镜像;每个活跃 Bot 占用约 160 MB 基线内存(外加 Go `magpie` 网关与 Electron 进程)。

## 业务价值

- **能算清的**:
  - **5,006★ / 124 forks / 3 open issues**(2026-11-27 实时值,2026-10-27 建仓仅 1 个月连发至 `v0.1.49`),是目前 GitHub 上明牌对标 Grok Bot / OpenAI Dots / Claude Duet 且实锤运行在 DSH 上的第二高星仓。
  - **密钥不出宿主进程 + 4 级应用硬门禁**:真实模型 Key 与 10 类连接器凭据(`app-secrets.json`)均不进 DSH 子进程环境变量;应用调用分为 `read`/`write`/`delete`/`send` 四级,其中 **`delete` 与 `send` 在包括 `full` 在内的所有权限档强制逐次询问且禁止“总是允许”**(`src/tools/apps/service.ts:1416-1425`)。
  - **工程与测试可核验**:核心非 i18n `src/` 193 文件 / 55,627 行 TS + `dsh-runtime/plugins/` 18 插件 2,512 行 + `ui/` 6.67 万行零构建 Preact + 135 个 Vitest 套件(35,922 行)。
- **只是预期(推断)**:
  - 独立打包 `dsh.asar` + 内置 4 套垂直 Bot 模板(`company-research`/`ppt-master`/`printfilm`/`us-stock-research`) + 微信 `y 1234`/`n 1234` 审批流可能大幅降低普通用户上手门槛,但官方无公开活跃用户数与下载总量统计。

## 一屏事实

| 项 | 值 |
|----|----|
| 仓库 / 注册状态 | `modelflare-ai/AnyModelBot`(**未收录于 `awesome-dsh-plugin`**,独立 Electron/Docker 宿主内嵌 DSH) |
| 子分类 | `bot-teams`(多 Bot 个人工作台,仿 Grok Bot / OpenAI Dots / Claude Duet) |
| 自述 | "Open-source, local-first alternative to Grok Bot, OpenAI dots and Claude Duet... Reach them in the app, WeChat or Feishu" |
| 星标 / fork(2026-11-27) | **5,006★ / 124 forks / 3 open issues**;创建 `2026-10-27`,最近 push `2026-11-26`(`v0.1.49`) |
| 包形态 / 许可 | `private: true`(npm 404);分发为 Electron 安装包(DMG/NSIS/AppImage)与 Docker 镜像;**MIT** |
| 代码规模 | `src/` 443 文件 / 69,507 行(核心非 i18n 55.6k)+ `dsh-runtime/plugins/` 18 插件 2,512 行 + `ui/` 66.7k + `test/` 135 套件 35.9k |
| 宿主钉版 | `dsh-runtime/package.json` 精确钉死 **`@deepseek-ai/dsh@0.2.1-rc.4`** + `@deepseek-ai/dsh-sdk-client@0.2.1-rc.4` + Go `magpie v0.1.1720` |
| repo@commit | `06b05e2627675c2347735f4d477583301787ae08`(2026-11-26 UTC) |
| 证据等级 | ★★★ |

## 它到底是什么

**一台把 DeepSeek Harness 当作“可回收无头引擎子进程”来驱动的多 Bot 桌面与 NAS 宿主。** 与把自身装进 DSH 的插件不同,AnyModelBot 自己承担 Web UI、SQLite 存储、IM 通道、应用连接器、统一审批中心与 Go 模型网关(`magpie`),每个 Bot 按需拉起一个独立 DSH SDK 子进程(`src/agent/host.ts:679-684`):

```text
Web/Electron UI(Preact) / 微信 iLink(QR) / 飞书卡片 / TG / Slack / Discord
  → AnyModelBot 宿主(SQLite 统一审批中心 + 10 应用连接器 + Go magpie 网关 + 本地 AgentBridge)
  → 每 Bot 1 个独立 DSH 0.2.1-rc.4 SDK 子进程(隔离 DSH_HOME,满 100 会话空闲自动回收)
     ├─ 动态生成 amb.patch.yml(0600):挂 18 个 amb-*.mjs 插件 + llm-pi-ai 指向本地 AgentBridge(假 Key)
     └─ 原生 Linux 下用 bwrap --tmpfs <dataDir> 隐藏宿主数据库与密钥(Docker 默认退化为 Landlock)
```

三层 Markdown 记忆(`src/agent/memory.ts:12-14`)在源码注释里明确致谢并借鉴了 `DS-Bot` 的设计与 `looksSecret` 正则,同时新增跨全部 Bot 共享的“关于我”个人档案(`about-me.json`,拦截身份证/卡号/密码、存邮箱电话前弹窗确认)。

## 怎么接进 DSH

1. **反客为主的内嵌打包(`scripts/bundle-dsh.mjs:1-65`, `dsh-runtime/package.json:7-14`)**:把纯 JS 版 `@deepseek-ai/dsh@0.2.1-rc.4` 与 18 个 `dsh-runtime/plugins/amb-*.mjs` 压成单文件 `resources/dsh/dsh.asar`(剔除 `libreoffice-kit`、`sherpa-onnx` 与 DSH Web UI),原生二进制(`node-pty`/`ripgrep`/`landlock-run`/`koffi`)放旁侧 `node_modules`。
2. **启动期动态生成 0600 Patch(`src/agent/host.ts:815-895`)**:每次拉起 Bot 子进程时写 `<data>/dsh/<botId>/amb.patch.yml`,把 `llm-pi-ai` 指向本地回环 `AgentBridge` + 临时 `bridge.token`(真实 Key 不入子进程),挂载 `amb-bridge`(因 `0.2.1-rc.4` SDK 不转发审批/提问,用此插件回环补齐)、`amb-permission`、`amb-workfolder`、`amb-delete-gate`、`amb-connections`、`amb-cua-mcp`、`amb-computer-use-gate` 等 18 个插件。
3. **进程回收补偿(`host.ts:198-203`)**:因 DSH SDK 无法单独关闭会话(每会话增约 0.25–0.45 MB 内存),Bot 子进程累计 `RECYCLE_AFTER_SESSIONS = 100` 后在空闲期自动重启回收。

## 关键实现

| 模块 | 位置 | 作用与源码实证 |
|---|---|---|
| 原生 Linux 强读围栏与防自批 | `src/agent/host.ts:1022-1121`, `src/agent/peer-guard.ts:1-76`, `dsh-runtime/plugins/amb-bridge.mjs:48-106` | 原生 Linux 用 `bwrap --tmpfs <dataDir>` 盖住宿主数据库与密钥,仅回绑工作区与 `dshHome`,缺失时 fail-closed 拒跑;Web 控制台用 `/proc/net/tcp`+`/proc/<pid>/fd` 拒绝来自 DSH 子进程树的 403 自批请求;`amb-bridge.mjs` 另在进程内拦截 `ctx.fs` 读 `<dataDir>` |
| 统一 SQLite 审批中心 | `src/agent/approvals.ts:8-247`, `dsh-runtime/plugins/amb-bridge.mjs:111-141` | 所有审批落 SQLite 配 4 位数字码(对话 10m / 后台任务 12h / 规则 1h),超时/重启/回环故障全 fail-closed;支持微信回 `y 1234`/`n 1234` 或飞书交互卡片审批 |
| 4 级应用分类与防删门 | `src/tools/apps/{service.ts:1416-1425,classify.ts}`, `dsh-runtime/plugins/amb-delete-gate.mjs:1-250` | 10 类连接器 + 自定义 MCP 经 `app_tools`/`app_tool_schema`/`app_call` 三元工具暴露;`delete`/`send` 全档强制逐次询问,`write` 绑定工具定义哈希;`amb-delete-gate` 在 `full` 档仍强把 `approval.policy` 改 `ask`,拦截 `rm -rf`/`git clean`/Base64 命令及 ≤256 KB 脚本内的递归删除 |
| 透明服务端压缩代理 | `src/agent/server-compaction.ts:1-180`, `src/agent/bridge.ts:189-250` | 除本地 Steward 压缩外,桥接层自动探测并缓存模型对 OpenAI `/v1/responses/compact` 的支持,透明改写前缀并在 4xx/流失败时自动回退原请求 |
| 记忆、关于我与协作上限 | `src/agent/{memory,about-me}.ts`, `src/collab/service.ts:32-52,200-243` | 3 层 Markdown 记忆 + 跨 Bot 共享 `about-me.json`(30 天撤销/禁回生/敏感信息拦截);Bot 互聊限单跳、默认 `$1`/4h/30 次/日上限且走 `looksSecret` 脱敏 |
| IM 接入与访问控制 | `src/core/{access,routes,groups}.ts` | 5 渠道 IM 均默认仅限主人(不支持 IM 群聊,群聊仅限 Web 端);陌生人每小时最多 1 次拒绝并生成 4 位配对码发主人 |

## 为什么它突出

只用本仓库自身证据:

- **验证了“把 DSH 当无头嵌入式引擎”的另一条高星产品路线**:5,006★ 证明普通桌面/NAS 用户买单的是“一键装好 + 微信/飞书 + 多模型 + 现成应用连接器”,而不是手动拼装 Cordis patch。
- **原生 Linux 下补齐了 DSH 缺失的“读围栏 + 防自批”**:`bwrap --tmpfs <dataDir>` 隐藏宿主密钥文件 + `/proc` 进程树阻断子进程自调审批接口,是值得 DSH 生态直接参考的防御范式。
- **把高风险应用写/删/发从权限档里剥离出来硬锁**:即便用户开了 `full` 全权限,`delete`/`send` 应用调用与递归删除仍受独立拦截门约束。

## 代价与边界

1. **高危默认配置(源码实锤)**:
   - **Computer Use 默认开启且免审批**:`src/domain/bot-settings.ts:111` 设为 `{ enabled: true, backend: 'cua', approval: 'auto' }`,点击/打字默认不弹窗确认;且 `amb-computer-use-gate.mjs:16-33` 权限查询报错时 fail-open 返回 `{ ok: true }`,未见类似 `DS-Bot` 的钥匙串/设置黑名单。
   - **非微信 IM 先到先得认主人**:飞书/TG/Slack/Discord 以“第一个私聊发消息的人”自动成为 Owner(`src/core/access.ts:4-5,151-176`)。
2. **严重的跨平台与 Docker 安全落差**:
   - 官方 `Dockerfile:50` 默认设 **`ENV AMB_ALLOW_LANDLOCK=1`**,据其自身源码警告(`host.ts:1110-1113`),Landlock 下 `<dataDir>`(含 `ui-token`、`app-secrets.json`、SQLite 库)对沙箱命令**可读**,且 `peer-guard.ts` 对脱离进程失效。
   - **macOS / Windows 下无 `bwrap` 读围栏且 `peer-guard.ts` 恒返回 `false`(`peer-guard.ts:9`)**,本地凭据(`modelflare-account.json` 已刻意迁出 Electron `safeStorage` 改为明文 base64、`app-secrets.json`、`ui-token`、`magpie/keys.json`)全部无静态加密,仅靠 POSIX `0o600`(Windows 下无效,`secrets.ts:96`)。
3. **无出站 `tools/result` / `llm/stream` 密文脱敏器**:仅日志层有 `redactText`(`src/log.ts:14-60`),不扫描模型上下文里的用户密文。
4. **核心能力商业绑定与旧版 DSH 钉死**:Bot 互聊、每 Bot 预算、生图视频与服务端压缩硬锁 Modelflare 登录;钉在较旧的 `0.2.1-rc.4`;且无内置每 Bot Playwright 浏览器面板。

## 可信度与复现

**读过**:`package.json`、`dsh-runtime/package.json`、`Dockerfile`、`scripts/bundle-dsh.mjs`、`electron/main.ts`、`src/{main,app,log}.ts`、`src/account/vault.ts`、`src/agent/{host,manager,approvals,bridge,memory,about-me,server-compaction,peer-guard,settings}.ts`、`src/domain/bot-settings.ts`、`src/collab/service.ts`、`src/core/{access,routes,groups,types}.ts`、`src/magpie/supervisor.ts`、`src/web/server.ts`、`src/tools/apps/{secrets,classify,service}.ts`、`src/tools/computer-use/index.ts`、`src/providers/official.ts` 及 7 个核心 `dsh-runtime/plugins/amb-*.mjs`。**未读**:Go 子模块 `vendor/magpie`、`ui/` Preact 前端、`src/tasks/*` 与 `cua-driver.ts` 底层实现,未跑实测。

```sh
git clone --depth 1 https://github.com/modelflare-ai/AnyModelBot && cd AnyModelBot
git rev-parse HEAD   # 06b05e2627675c2347735f4d477583301787ae08
cat dsh-runtime/package.json
```

## 待验证

- 未读 `src/tools/computer-use/cua-driver.ts` 确认底层 CUA 驱动自身是否带有受保护应用过滤。
- 未读 `src/tasks/*` 核验定时任务与规则引擎的观察模式(observe-only)边界。
- 未实测 macOS/Windows 下多 Bot 同时开启时每 Bot ~160 MB 子进程的实际内存峰值与回收体验。
