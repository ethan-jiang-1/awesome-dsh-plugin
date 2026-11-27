---
kind: card
domain: personal_agent
subcategory: im-personal-hubs
repo: roost-qq/dsh-roost
commit: 04af08228d1cfdfde2af094221ec7d8972cfff5c
evidence: 3
status: active
asof: 2026-11-27
---

# dsh-roost — 把 QQ 变成带“说话人分级围栏 + 三层夜间整理记忆”的个人常驻 Agent

> 证据等级 ★★★(源码级;`roost-qq/dsh-roost@04af0822`)。未执行 `node --test` 与真实 QQ 开放平台联调,未读外部内核仓 `roost-qq/qq-bot-roost`;权限隔离、三层记忆、主动唤醒与官方 QQ 约束均经源码逐文件核验。
> 星标 55★ / 3 forks 为 2026-11-27 GitHub API 实时值;npm `dsh-roost` 近 30 天下载 **22,012**(`2026-10-28`~`2026-11-26`,radar 同日稍早快照为 24,702,属滚动窗口差异)。

## 它替谁解决什么问题

**想把本机 DSH 变成 24/7 常驻 QQ(私聊 + 亲友/同事群 + 频道)的个人数字助手、但既怕群里外人顺手指挥电脑跑 `bash`,又怕长期聊天把上下文和 Token 撑爆的个人主机使用者。** 常见的笨办法有三个痛点:

- **直接挂裸 IM 桥**:大多 IM 插件只有粗粒度白名单,要么完全拒收群聊,要么进了群就人人都能触达本机工具与记忆写入,一旦被群友调戏或提示注入就可能改写记忆或执行命令。
- **靠提示词要求“只听主人的话”**:提示词挡不住模型在群聊上下文里误调本地工具或泄露跨群隐私事实。
- **白天实时调模型总结记忆**:每轮聊天都多跑一次总结既拖慢回复又烧 Token,旧对话久了还会把历史塞满。

`dsh-roost` 用宿主侧逐回合 `tools.restrict` 减法把群内说话人分成 6 级,只在夜间离线跑单次 JSON 记忆整理(facts + SQLite FTS5 日记 + 双时态知识图谱),并用首次引导自动拉起独立 QQ 官方开放平台内核。

## 适用面:谁该用、谁别用

- **适合**:以 QQ(单聊/群聊/频道)为日常高频入口的个人开发者或小群主;能按 QQ 开放平台流程申请 `AppID`/`AppSecret` 并在手机 QQ 手动开启群内“接收所有消息”与拉机器人进群的人;运行 Node ≥22 与 DSH `>=0.2.0` 的长期开机主机。
- **不适合**:需要 OS/容器级沙箱硬隔离的强安全场景(README L137 明确声明它跑在宿主 OS 用户权限下,不是沙箱);不能接受 `AGPL-3.0-only` 传染性许可的二次商业托管方;需要免审群主动推送或不受 QQ 官方 30 天 4 窗召回限制的海外用户(应看 WhatsApp/Telegram 路线)。
- **前置条件**:Node ≥22(依赖内置 `node:sqlite`,旧版 22.0–22.4 退化为线性扫描 JSONL 且停用知识图谱)、DSH `>=0.2.0`;需 QQ 开放平台 `AppID`/`AppSecret` 及额外运行独立进程 `qq-bot-roost`(默认装到 `~/.dsh/dsh-roost/roost`)。

## 业务价值

- **能算清的**:
  - **高真实下载转化**:仅 55★ / 3 forks,但 npm `dsh-roost` 近 30 天下载达 **22,012**(`2026-10-28`~`2026-11-26`),证明 QQ 个人常驻入口的真实安装需求远大于星标表现。
  - **零白天记忆整理模型调用**:白天仅做规则分类(`critical`/`important`/`normal`)写本地 SQLite,批量 LLM 蒸馏与三元组更新全部收口到夜间单次批处理(每次最多 5 群 / 80 行 / 6,000 字)。
  - **1 步 npm 安装 + 向导拉内核**:零 npm 运行时依赖,支持 `dsh plugin add dsh-roost`,但 QQ 开放平台建应用、手机端开“接收所有消息”与拉群这 3 步平台限制不可自动化(`src/setup.js:7-11`)。
- **只是预期(推断)**:
  - 说话人 6 级权限与三层记忆可能让同一个 DSH 既能安全待在亲友/工作群里答疑、又能在私聊替主人管电脑与主动提醒,但缺少真实生产留存与误触发统计。

## 一屏事实

| 项 | 值 |
|----|----|
| 条目 / 类目 | `roost-qq/dsh-roost` / `remote`([registry](../../../data/plugins/roost-qq__dsh-roost.yml)) |
| 子分类 | `im-personal-hubs`(注册表实装个人管家) |
| 自述 | 官方 QQ 机器人接入 DSH,1:1 持久会话映射、按说话人收放工具权限、三层记忆与主动定时消息 |
| 星标 / 下载(2026-11-27) | **55★ / 3 forks**;npm `dsh-roost@1.4.7` 月下载 **22,012**(创建 `2026-10-26`,push `2026-11-27`) |
| 包形态 / 许可 | 纯 ESM JS,零 npm `dependencies`;**`AGPL-3.0-only`**;附带独立进程内核 `qq-bot-roost` |
| 代码规模 | `src/` **237 文件 / 99,954 行**(其中 `src/host.js` 单文件 18,489 行);`client/client.js` 27,320 行;`test/` **292 套件 / 79,029 行** |
| 宿主钉版 | `engines.dsh: ">=0.2.0"`, `node >=22`;`@deepseek-ai/dsh-tools` 动态导入带三级兜底 |
| repo@commit | `04af08228d1cfdfde2af094221ec7d8972cfff5c`(2026-11-27 +0800) |
| 证据等级 | ★★★ |

## 它到底是什么

**一套以 QQ 官方开放平台为个人常驻壳、把“多角色群聊防越权”和“离线记忆蒸馏”做进宿主层的重型纯 JS 插件系统。** 2026-11-12 起它移除了 `ai-chat` 中间层(`docs/接入说明.md:3-6`),采用双进程结构:

```text
QQ(单聊 c2c / 群 group / 频道 guild / 频道私信 dm)
  ⇄ qq-bot-roost 独立内核(QQ Official OpenAPI)
  ⇄ roost-host/1(WS 或 HTTP+SSE 断线带 seq gap 检测 + POST /rpc)
  ⇄ dsh-roost(src/host.js: 6级说话人工具剪枝 + 12 槽 systemPrompt + 危险命令确认门)
  ⇄ DSH 会话(1:1 sessions.json 持久映射 + 夜间 consolidate 三层记忆)
```

两套内置 preset(`roost-private` / `roost-social`)在 `cordis.patch.yml:20-101` 里挂载了完全相同的本地工具(`dsh-tool-fs` + `bash`/`pwsh`),并给 `@deepseek-ai/dsh-persona` 设 `complete: true` 剥离编程助手基底提示词;真正的权限分界不是靠静态两套工具表,而是在**每回合入站时按当前说话人身份动态收缩工具集、回合结束在 `finally` 里无条件恢复**(`src/host.js:9264-9274, 9838-9843`)。

## 怎么接进 DSH

1. **Bundle 挂载(`cordis.patch.yml:16-101`)**:插入插件 `roost` 与 `roost-private`/`roost-social` 两套 preset(内含 `dsh-compaction-basic` + `dsh-compaction-tool-result-pruner` 独立组,阈值 8,192 字符)。
2. **宿主服务与双 HTTP 面(`src/host.js:499-504, 10541`, `src/server.js:62-225`)**:`inject = ['agents', 'sessions', 'systemPrompt', 'webServer']`,在宿主注册 `/roost/api/*`,并另起回环服务 `127.0.0.1:17321`(端口冲突经 `lease.js` 自动顺延)承载扩展 `/v1/*` 与 `/tts`;可选通过 `ctx.provide('aurabot', ...)` 暴露跨插件服务(默认关闭,`src/bridge.js:5, 21-48`)。
3. **12 槽有序系统提示注入(`src/host.js:8528-8944`)**:按 `895`~`910` 顺序挂载扩展上下文、表情包、场景、静态记忆(为保前缀缓存,动态召回默认塞进用户消息,`L8853-8865`)、情绪、人设(含关键词触发世界书)、权限说明与末尾安全边界 `roost-guard`(`910`)。
4. **前端面板与首启拉核(`client/client.js:27216-27226`, `src/setup.js:37-41, 853-871`)**:仅注入 `slots` 注册 `main` 与 `sidebar.panellist`;首次向导按 Gitee zip → npm `qq-bot-roost` → GitHub 顺序下载内核到 `~/.dsh/dsh-roost/roost` 并自动配对校验。

## 关键实现

| 模块 | 位置 | 作用与源码实证 |
|---|---|---|
| 6 级说话人与动态剪枝 | `src/permissions.js:26-53, 180-206`, `src/capabilities.js:321-495`, `src/host.js:715-907` | `owner(0) > admin(1) > manager(2) > helper(3) > member(9999) > unknown`;`bucketOfLevel()` 先拒空串防 `Number('')===0` 提权;先读实时 `tools.schemas()` 再算 `deny = pool \ allow`,规避 DSH `tools.restrict` 遇未知工具名整批抛错;普通成员默认只留 `memory_search`/`qq_send`/`qq_close`(显式排除 `qq_send_file`) |
| 工具内纵深防线 | `src/tools.js:165-172, 209-235, 286-293` | `memory_note` 执行期二次验 `caller().bucket === 'owner'` 防群友污染记忆;`memory_search` 非 owner/admin 禁止查 `global` 跨群记忆且隐藏发言人姓名 |
| 危险命令一次性确认门 | `src/safety.js:21-194`, `src/host.js:1394-1442, 9037-9056` | 挂 `tools.guard` 扫 shell 与 `mcp__*__(exec\|bash\|cmd\|pwsh)` 全参数(10 类破坏性正则);跳过非 Roost 编程会话(issue #73),无头会话 fail-closed;命后要求 QQ 回 `确认`(5 分钟 TTL + 归一化命令指纹绑定,拒收 `/v1/message` 来源) |
| 1:1 会话持久化 | `src/sessions.js:56-354`, `src/account.js:38-150` | `sessions.json` 写前合并防覆盖外部迁移、10 分钟删除墓碑防复活、PID+随机后缀原子替换、坏 JSON 隔离保留 3 份;支持 `openid`↔QQ 号别名跨 AppID 迁移 |
| 三层 + 自我叙事记忆 | `src/memory.js:1-319`, `src/journal.js:1-350`, `src/graph.js:1-320`, `src/consolidate.js:1-800` | L1 `memory.json`(global/chats 分层、衰减 `R=exp(-age/tau)`、低置信不覆高置信)+ L2 `journal.sqlite`(内置 `node:sqlite` FTS5 中文 bigram + 向量,只压不删)+ L3 `graph.sqlite`(双时态边 + `suppress` 墓碑防删除关系夜间回生)+ 夜间单次 JSON 蒸馏与自我叙事 |
| 主动外推与 QQ 限流治理 | `src/speakup.js:23-447`, `src/wakeup.js:1-151`, `src/outbound-policy.js:1-250`, `src/channel.js:52-70, 580-667` | SpeakUp(默认关,单聊 `8-23` 时、上限 3 次/日、未回复自动止骚扰、`<<skip>>`/`<<silence:2h>>`);QQ 官方 `is_wakeup` 4 窗(1d/3d/7d/30d 硬截断);`outbound-policy` 移植自 `aurabot-beta` 做 `admit→reserve→commit` 账本;编码了 QQ 1,500 字上限、100 张图池上限与 2 分钟撤回限制 |

## 为什么它突出

只用本仓库自身证据:

- **极罕见的“高下载/低星标”真实采用样本**:建仓仅 1 个月(2026-10-26),55★ 却跑出 **22,012** npm 月下载(发布至 `v1.4.7`,PR #100),配 **292 个测试文件(79,029 行)**。
- **把 QQ 群多说话人隔离做到了源码级 fail-closed**:显式修过 `Number('')===0` 提权、`tools.restrict` 未知工具名静默拒批、跨群记忆串味、工具内二次身份校验四类真实踩坑。
- **零外部 DB 的本地三层记忆 + 夜间整理**:仅靠 Node 22 内置 `node:sqlite` 实现事实衰减、FTS5 日记与带墓碑的双时态知识图谱,且零 npm 运行时依赖。

## 代价与边界

1. **源码实测安全缺口(群聊 `confirmGate` 未校验回复者身份)**:`src/host.js:9037-9056` 的 `confirmGate.onMessage(chat.chatId, said)` 虽校验了 `chatId` 与 `!fromApi`,但不同于 `profileConfirm`(L9080-9085),它**没有核对回复 `确认` 的发言人是否为 `owner`**——在群聊里主人触发危险命令的 5 分钟窗口内,其他群成员回复 `确认` 理论上可代为放行。
2. **不是 OS 沙箱**:README L137 明确声明跑在 DSH 宿主进程与操作者 OS 用户权限下,工具限制仅约束 LLM 侧调用;且未对凭证做盲填隔离。
3. **单文件复杂度极高**:`src/host.js` 单文件 **18,489 行**、`client/client.js` **27,320 行**,大量状态集中在巨型闭包内,维护与审计门槛高。
4. **双进程运维与 QQ 平台硬壁垒**:必须并跑外部 `qq-bot-roost` 进程(且其源码不在本仓);受 QQ 开放平台硬约束(无撤回超 2 分钟、无群流式、群主动推送需专门 `group_push` 授权、C2C 召回 30 天最多 4 窗、单条 1,500 字、图库上限 100 张)。
5. **`AGPL-3.0-only` 许可**:强传染性,不适合闭源托管改造。

## 可信度与复现

**读过**:`data/plugins/roost-qq__dsh-roost.yml`、`package.json`、`cordis.patch.yml`、`docs/接入说明.md`,以及 `src/` 下 `permissions.js`、`capabilities.js`、`sessions.js`、`roost-host.js`、`bridge.js`、`safety.js`、`wakeup.js`、`speakup.js`、`server.js` 全文,外加 `host.js`、`channel.js`、`consolidate.js`、`memory.js`、`journal.js`、`graph.js`、`tools.js`、`setup.js`、`outbound-policy.js`、`account.js`、`autotelic.js`、`client/client.js` 关键段。**未读**:外部仓 `roost-qq/qq-bot-roost`、`ext-*.js` 扩展市场与 `tts*.js`/`onnx*.js` 语音模块,未跑实测。

```sh
git clone --depth 1 https://github.com/roost-qq/dsh-roost && cd dsh-roost
git rev-parse HEAD   # 04af08228d1cfdfde2af094221ec7d8972cfff5c
node --test "test/**/*.test.js"
curl -s https://api.npmjs.org/downloads/point/last-month/dsh-roost
```

## 待验证

- 未验证外部 `qq-bot-roost` 内核的源码安全性、token 落盘权限与 QQ 开放平台回调签名校验。
- 未实测 `src/host.js:9037-9056` 群聊 `confirmGate` 非 owner 回复 `确认` 是否在前置分支被其他条件拦截。
- 未验证 `22,012` npm 月下载中自然用户安装 vs 自动化 CI/重装的比例。
