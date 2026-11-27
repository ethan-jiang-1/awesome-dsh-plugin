---
kind: card
domain: personal_agent
subcategory: bot-teams
repo: Fei-Craft/DS-Bot
commit: 7963e66a74f40d23daa288a76cdca72b34e39561
evidence: 3
status: active
asof: 2026-11-27
---

# Fei-Craft/DS-Bot — 9,110★ / 7.5 万月下载的 DSH 原生多 Bot 锚点,已长出 7+ 库内第三方伴生契约插件

> 证据等级 ★★★(源码级;`Fei-Craft/DS-Bot@7963e66a`)。未运行 `npm test`、Electron 打包或 Docker 实机联调;宿主 72 模块管线、私密 Bot 围栏、Secrets 脱敏、8 渠道 IM、浏览器/CUA 门禁及 `data/plugins/` 内全部伴生插件均经源码与 YAML 逐文件核验。
> **未收录于 `awesome-dsh-plugin` 注册表**(GitHub + npm `ds-bot@0.4.0` + 独立桌面端/Docker 独立分发),但注册表内已合并多条直接依附其接口的第三方伴生插件。星标 9,110★ / 917 forks 与 npm 月下载 **75,869**(`2026-10-28`~`2026-11-26`)均为 2026-11-27 实测值。

## 它替谁解决什么问题

**想把 DeepSeek Harness 从“单会话编程工具”直接升级成对标 xAI Grok Bot 的“常驻多 Bot 个人团队”——每个 Bot 拥有长期身份、三层记忆、独立 Playwright 浏览器、桌面 CUA、8 渠道 IM 与 E2EE 手机配对,且支持用主 Bot 协调群聊与委派任务——但仍希望所有会话与工具原生留在 DSH 生态内的个人重度用户与插件开发者。** 常见笨办法有三个痛点:

- **在 DSH 里手开十几个会话假装团队**:会话彼此看不见、没法互发消息或建群,长任务写满上下文后只能手工切新窗口重喂背景。
- **把 IM 或手机接入多 Bot 后一团乱**:外部 IM 陌生消息直接进记忆回顾会被提示注入投毒;手机端远程审批若允许点“总是允许”会造成失控授权。
- **自己拼装多 Bot 外壳容易把插件生态割裂**:独立魔改宿主会导致第三方插件装不上去或换个界面就丢数据。

`Fei-Craft/DS-Bot` 把每个 Bot 直接映射成一个原生 DSH 根会话,不引入新会话事件类型,同时提供原生 DSH 插件(`ds-bot`)、独立 Electron 桌面端与 Docker NAS 版三种形态,并已在实际生态里长出一圈第三方伴生插件。

## 适用面:谁该用、谁别用

- **适合**:想直接用“多 Bot 个人工作台 + 8 渠道 IM(微信/飞书/钉钉/企微/QQ/TG/Slack/Discord)+ 手机 E2EE 遥控 + 独立浏览器 + 桌面 CUA”的个人与小团队;以及想基于现成多 Bot API 写看板/模型切换/反射弧/语音路由等 D2 伴生插件的作者。
- **不适合**:要求 OS 内核级强读隔离防止本地 Shell 越权读私密 Bot 文件的强安全环境——源码 `privacy.js:2-4,674-676` 诚实注明 DSH 沙箱不拦读取,Shell 侧保护仅靠词法检查(`ownerInText`);也不能把它的第三方 Bot 插件机制当成安全沙箱(`SECURITY_MODEL.md:75` 明写各安全层级目前**尚未真正沙箱化**,仍以宿主权限运行);Docker 版强制 `danger-full-access` + `approval: never`,不适合多租户共享宿主机。
- **前置条件**:原生插件模式依赖 12 个 `@deepseek-ai/dsh-*` peer(7 必填 + 5 可选),桌面端与 Docker 版均钉死 `@deepseek-ai/dsh@0.2.2-rc.5`;插件模式会禁用宿主原生 `ui-settings-general` 并改写 `web.searchProvider: auto`。

## 业务价值

- **能算清的**:
  - **DSH 个人 Agent 赛道第一实证声量与采用**:**9,110★ / 917 forks / 335 open issues**(2026-11-27 实时值,建仓仅 7 周),npm `ds-bot@0.4.0` 近 30 天下载 **75,869**(26 个已发版本,当日刚发 0.4.0)。
  - **已形成真实的第三方 D2 契约复用环**:尽管本体不在 `awesome-dsh-plugin`,实测 `data/plugins/` 里已有 **4 个纯伴生 D2 扩展**(`onesmash/dsh-reflex`、`DamonKoy/dsh-bot-model-switch`、`JackWoods-code/dsh-bot-toggle`、`coii08o0o/dsh-bot-board`)、**3 个可选集成插件**(`dsh-pocket-glide`、`dsh-siri`、`ds-kanban`)、**2 套适配主题**与 **1 个下游分叉**(`automagik-si/automagik#bots-dsh`),是除 `dsh-superagent` 外全生态唯一形成协议吸附力的个人 Agent 根。
  - **可核验工程厚度**:`ds-bot/` 含 823 个代码文件(44.8 万行,含 371 个测试文件 18.7 万行),另含 Electron `app/`(7.2 万行)、`mobile/`(2.4 万行)、`link/` E2EE 中继与 `docker/`。
- **只是预期(推断)**:
  - 其「浏览器硬拒 `payment` 强制交人 + CUA 硬保护名单禁点钥匙串/设置 + 外部 IM 消息剔出记忆整理」的组合安全设计可能显著压低个人日常自动化翻车率,但尚缺公开红队或生产事故率统计。

## 一屏事实

| 项 | 值 |
|----|----|
| 仓库 / 注册状态 | `Fei-Craft/DS-Bot`(**未收录于 `awesome-dsh-plugin`**,但库内已有 **10 条** D2 伴生/集成/主题/分叉条目) |
| 子分类 | `bot-teams`(多 Bot 个人工作台,仿 Grok Bot / OpenAI Dots) |
| 自述 | "A team of long-lived bots for DeepSeek Harness, with main bots, bot-to-bot messages and group chats." |
| 星标 / 下载(2026-11-27) | **9,110★ / 917 forks**;npm `ds-bot@0.4.0` 月下载 **75,869**(创建 `2026-10-07`,push `2026-11-27`) |
| 包形态 / 许可 | 三形态:原生 DSH bundle(`ds-bot`) + Electron 44 桌面端(`app/`) + Docker(`docker/`);**Apache-2.0** |
| 代码规模 | `ds-bot/` 823 文件 / 448,607 行(`src/host` 93.5k、`src/client` 70.3k、`test` 371 套件 186.9k)+ `app/` 72.3k + `mobile/` 24k |
| 宿主钉版 | 插件 peer 写 `*`(7 必填 + 5 可选);桌面端(`app/`)、Docker(`docker/`)与 dev harness 均精确钉 **`@deepseek-ai/dsh@0.2.2-rc.5`** |
| repo@commit | `7963e66a74f40d23daa288a76cdca72b34e39561`(2026-11-27 -0800) |
| 证据等级 | ★★★ |

## 它到底是什么

**以“1 Bot = 1 原生 DSH 根会话”为核心抽象的长期多 Bot 个人运行环境。** 全部状态集中在 `<DSH_HOME>/bot/state.json`(`ds-bot/index.js:102,108`),由 72 个有序宿主模块驱动:

```text
桌面 / Web / 手机 E2EE Relay(wss://relay.dsbot.app) / 8 渠道 IM / Local API(:17830)
  → Main Bot(专权 create/update/stop Bot、建/删群) + 专职 Bots + 群聊(每成员隐藏群会话 + 防空转停机)
  → 72 宿主模块:
     ├─ 记忆:bots/groups/team 三层 Markdown(首读冻结保缓存) + 离线回顾(强丢 im:/api: 外部会话防投毒)
     ├─ 行动:每 Bot 独立 Playwright 浏览器(payment 硬拒交人) + CUA 桌面(禁点自身/系统设置/钥匙串) + 本地 CLI(Claude/Codex/ACP)
     └─ 防线:approval/request(prepend,辅助评审全异常 fail-closed 退人工) + Private Bot 围栏 + Secrets 双端脱敏
```

它不发明私有会话日志格式,因此可以同时作为插件放进用户已有 DSH Web,也能在 `app/` 里直接用 `@deepseek-ai/dsh/profile-boot` 启独立桌面应用。

## 怎么接进 DSH

1. **防炸降级入口(`ds-bot/plugin.js:1-42`)**:`apply()` 内懒加载 `./index.js`,即便宿主依赖失效也只令宿主侧激活失败而不拖垮前端 bundle,保住设置页与经典 DSH 模式回退;可选 `codeMode` 独立挂在子插件上不阻塞主团队运行时。
2. **Bundle Patch 侵入点(`ds-bot/cordis.patch.yml:1-28`)**:插入 `id: bot`(`ds-bot`)与 `id: web-search-auto`(`ds-bot/web-search`),将 `id: web` 改为 `searchProvider: auto`(L14-18 警告单独禁用 `web-search-auto` 会令所有 `web_search` 报废),并**禁用原生 `id: ui-settings-general`**(`L27-28`)以接管侧栏设置位。
3. **三形态差异**:插件版依赖宿主 profile(`inject` 8 项宿主服务 + 6 项前端服务);桌面版(`app/src/host.mjs:46-84`)以 39 个 `@deepseek-ai/dsh-*@0.2.2-rc.5` 包进程内启动独立 `ds-bot` profile;Docker 版(`docker/docker.patch.yml:7-12`)以 `gosu node` 强设 `danger-full-access` 与 `approval: never`。

## 关键实现

| 模块 | 位置 | 作用与源码实证 |
|---|---|---|
| 主 Bot 权威与防空转群聊 | `ds-bot/src/host/{tools,groups,roster}.js` | `rt.teamTools` 仅向 Bot 会话暴露 15 个团队工具;建/改/停 Bot 与建删群硬核 `rt.isMain(...)`;群聊维护 `IDLE_ACK_WORDS`/周期/零工作量熔断防死循环;`local-agents/` 可挂 Claude Code/Codex/ACP 作为 Bot 引擎 |
| 防投毒三层记忆与会话轮转 | `ds-bot/src/host/{memory,memory-review,parts,steward}.js` | `bots/groups/team` 三层 Markdown + `journal.jsonl`(私密 Bot 独立日记),首读冻结保前缀缓存;`memory-review.js:86-90,111-127,180-184` 将 `im:`/`api:` 来源及其整簇回复标 `trust: 'external'` 并**彻底丢弃出记忆回顾**;支持 14 天删后禁回生与停机点换新会话轮转 |
| 浏览器与 CUA 强门禁 | `ds-bot/src/host/browser-plugins.js:79-124`, `computer/index.js:47-67` | 浏览器动作门禁**硬拒 `payment`**(强制 `browser_handoff` 交人),`post/upload/download/delete` 须审批且无审批服务即 fail-closed;CUA 桌面维护硬编码 `PROTECTED_IDS`/`NAMES`/`EXES` 黑名单,禁点 DS Bot、DSH、系统设置、钥匙串与密码管理器 |
| Fail-Closed 审批与模型复核 | `ds-bot/src/host/{approvals,approval-review}.js` | `approval/request` `prepend` 拦截;`"review"` 预设用辅助模型(30 秒超时)预审,遇缺证据、非文本消息、命中密文脱敏、对话漂移或 JSON 异常**一律抛错退回人工卡片**;`alwaysAllow` 仅限直属文件 `extraDirs`,且手机远程卡剥离 `alwaysAllow`(`phone.js:155-158`) |
| Secrets 双端脱敏与私密围栏 | `ds-bot/src/host/{secrets,privacy}.js` | `request_secret` 卡片录入,按 `canUse(secret, botId)` 经 `shellEnv` 注入 `$DSH_SECRET_*`;在 **`tools/execute` 返回与 `llm/stream` 出站双端**扫描原文/JSON 转义/URL 编码/多行变体脱敏;`privacy.js:985-1362` 对所有 Bot 封锁 `api-tokens.json`/`mcp.json`/`secret-refs/` |
| 8 渠道 IM、手机中继与 Local API | `ds-bot/src/host/{im/index,phone,api/auth}.js` | 8 平台经配对门禁接入,IM 拒收密文卡与复杂视图;手机端经 `wss://relay.dsbot.app` + X25519 E2EE 通信并校公网 IP 防 DNS 重绑定;Local API(`127.0.0.1:17830`)默认关,Token 走 `scrypt`/`sha256`+`timingSafeEqual` + 6 级 scope |

## 为什么它突出

只用本仓库自身证据:

- **DSH 生态目前唯一同时跑通“高星 + 7.5 万月下载 + 真实 D2 伴生插件环”的个人 Agent 底座**:`data/plugins/` 中 4 个纯伴生 D2 插件(如 `dsh-reflex` 无需改 `ds-bot` 源码、`dsh-bot-model-switch` 调其 `api/bot` 接口、`dsh-bot-toggle` 切面共存、`dsh-bot-board` 只读看板)证明其运行契约已开始被社区复用。
- **把“个人 Agent 真实安全边界”写进了 `SECURITY_MODEL.md` 与源码**:外部 IM 不进记忆整理、浏览器禁支付、CUA 禁点密码管理器、双端密文脱敏、手机剥离 `alwaysAllow`、辅助预审全异常退人工,工程成熟度显著高于常规多 Bot 壳。
- **不抛弃原生 DSH 对象模型**:1 Bot = 1 原生 DSH 会话,既能单独发桌面端与 Docker,也能随时作为普通插件装回官方 DSH。

## 代价与边界

1. **Shell 读围栏缺口(`privacy.js:2-4,674-676`)**:DSH 原生 `workspace-write` 沙箱只拦写不拦读,私密 Bot 与密文文件对 `bash`/`pwsh` 的防护依赖词法路径检查,动态拼路径或脚本内相对穿越无法在 OS 内核层拦住。
2. **第三方 Bot 插件沙箱尚未落地(`SECURITY_MODEL.md:75`)**:清单分级校验虽 fail-closed,但文档明写实际沙箱尚未实现,运行中插件仍享宿主同级权限。
3. **`secrets.json` 默认明文落盘(`secrets.js:221-224`)**:静态 AES-256-GCM 加密为可选项,且运行期解密值仍驻留宿主内存。
4. **公网中继与 IM 信任边界未完全闭环(`SECURITY_MODEL.md:13,41,88-93`)**:手机端默认依赖 `wss://relay.dsbot.app`(元数据与浏览器页面信任);已配对 IM 发送者虽不进记忆回顾,仍可直接驱动工具回合;主 Bot 对单 Bot 密文的可见性仍在开放讨论中。
5. **宿主侵入与 Docker 放权**:插件模式禁用原生 `ui-settings-general` 并改写 `web.searchProvider`;Docker 版强制 `danger-full-access` + `approval: never`。

## 可信度与复现

**读过**:`ds-bot/{package.json,cordis.patch.yml,plugin.js,index.js}`、`SECURITY_MODEL.md`、`app/{package.json,src/host.mjs,src/app-patch.mjs}`、`docker/{Dockerfile,docker.patch.yml,entrypoint.sh}`、`ds-bot/src/host/{entry,roster,privacy,secrets,permissions,approvals,approval-review,memory,memory-review,browser,browser-plugins,phone,groups,parts,tools,computer/index,api/auth,im/index,im/platforms/index,local-agents/index,plugins/tiers,plugins/env,plugins/kill-list}.js`,并核验 `data/plugins/` 内全部 13 个匹配 `.yml`。**未读**:`ds-bot/src/client/`、`mobile/`、`link/` 中继实现、`secrets-crypto.js` 与各 IM 平台底层 wire 适配器,未跑实测。

```sh
git clone --depth 1 https://github.com/Fei-Craft/DS-Bot && cd DS-Bot
git rev-parse HEAD   # 7963e66a74f40d23daa288a76cdca72b34e39561
curl -s https://api.npmjs.org/downloads/point/last-month/ds-bot
grep -rilE 'ds-bot|DS Bot|Fei-Craft|Fei2411' data/plugins/ | sort
```

## 待验证

- 未读 `link/` 与 `mobile/` 核验手机 E2EE 握手抗中间人与密钥轮换实现。
- 未读 `ds-bot/src/host/connectors/` 核验邮件(`imapflow`/`nodemailer`)与 OAuth 连接器的写前审批边界。
- 未实测 `ds-bot@0.4.0` 插件版与 4 个 `data/plugins/` 伴生插件在 DSH `0.2.2-rc.5` 上的联合兼容性。
