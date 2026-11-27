---
kind: card
domain: personal_agent
subcategory: im-personal-hubs
repo: MJ-CJM/DSH-Bot
commit: 4f08cf12d2fb7d046b7637ba8e848643eba1104e
evidence: 3
status: active
asof: 2026-11-27
---

# MJ-CJM/DSH-Bot(`dsh-botgroup`) — 注册表最高星多 Bot 个人工作台,用信息流控制 + TLA+ 锁死私密记忆外泄

> 证据等级 ★★★(源码级;`MJ-CJM/DSH-Bot@4f08cf12`)。未运行 Vitest / TLA+ TLC / 实机 DSH `0.2.1-rc.2` 联调;信息流控制(IFC)、审批链、Supergroup 防注入与 TLA+ 规格均经源码逐文件核验。
> 星标 100★ / 8 forks 为 2026-11-27 GitHub API 实时值(`stars-2026-11-27.json` 为 99★);npm 真实包名为 **`dsh-botgroup`**(近 30 天下载 **1,854**,切勿错装无关包 `dsh-bot`)。

## 它替谁解决什么问题

**想在 DSH Web 原生界面里养一批长期分角色的个人 Bot(各自有独立人设、技能目录、私有记忆与定时任务),还能拉进群聊自动组队协作、同时绝不允许某个 Bot 把私聊记忆偷偷带出群聊或发给外部的个人重度用户与安全洁癖型开发者。** 现有多 Bot 插件常见三个痛点:

- **私密记忆裸奔**:把私有记忆塞进共享群聊或子 Agent 提示词后,根本不知道哪条私人信息被带出去了,删记忆也挡不住旧会话继续引用。
- **跨 Bot 协作容易被间接提示注入劫持**:允许模型自由编造任务文本派给别的 Bot,网页/文档里的恶意指令就能借壳传话。
- **热重载与宿主升级悄悄坏掉**:插件更新后 ESM 缓存混装旧模块,或宿主缺沙箱能力时静默降级成裸奔。

`MJ-CJM/DSH-Bot` 用三层信息流控制(会话污点追踪 + 精确内容一次性 `OnceGrant` + 群外发人工审查)与 TLA+ 形式化模型把记忆越界做成硬门禁,对宿主 `rc.2` 做不到的两项能力宁可显式关闭(`effectiveAutoShare: false` / `workspaceExecutionAvailable = false`)也不假装安全。

## 适用面:谁该用、谁别用

- **适合**:在 DSH `0.2.1-rc.2`~`<0.3.0` 原生 Web 端内使用多 Bot 个人工作台、重视私有记忆边界与群外发精确内容审核的个人用户;研究 Agent 信息流控制(IFC)、`forgetEpoch` 强遗忘与 TLA+ 规约建模的插件架构师。
- **不适合**:高度依赖第三方任意 MCP 工具或 `run_code`(PTC)的团队——它的 `protectDataFlow()` 为保数据流闭环会**硬拦未审计的外部 MCP 与 `run_code`**(`tool-guard.ts:75-84`, `native-policy.ts:8-16`);需要各 Bot 文件系统强隔离的场景(所有 Bot 共享 `'Bots'` 工作区根目录,`bot-context.ts:176`);停留在 DSH `<0.2.1-rc.2` 或已升 `0.3.0` 的宿主环境。
- **前置条件**:DSH `>=0.2.1-rc.2 <0.3.0`(14 条 peer 严格钉在该区间);安装务必核对 npm 包名 **`dsh-botgroup`** 或 GitHub Release `dsh-bot.tgz`,更新后因 SHA-256 模块清单校验需完整重启 DSH(`src/index.ts:12-54`)。

## 业务价值

- **能算清的**:
  - **注册表 `awesome-dsh-plugin` 内星标最高的端到端个人 Agent 壳**:100★ / 8 forks(2026-11-27 实时值),npm `dsh-botgroup@0.7.4` 近 30 天下载 **1,854**,Release `v0.7.4` `dsh-bot.tgz` 下载 54 次。
  - **可核验工程密度**:`packages/dsh-bot/src/` 491 文件 / 64,195 行 TS,配 **262 个 Vitest 测试套件(73,448 行)**、TLA+ 6 条不变量模型(含故意关闭 epoch 校验的负对照 `stale_grant_negative.cfg`)与 319 条离线/红队合成评测用例。
  - **零虚报能力边界**:因宿主 `rc.2` 缺不可伪造用户输入证明与读+网沙箱,代码层直接锁死自动共享与主动工作区子进程,避免给用户制造虚假安全感。
- **只是预期(推断)**:
  - 其三层 IFC 审查与群根零模型守卫可能大幅压低多 Bot 群聊下的私密信息外泄风险,但仓库自身的真实大模型连续 Agent 评测集与 `rc.3` 实机传输测试目前均标为 `NOT_RUN` / `FAIL(environment)`。

## 一屏事实

| 项 | 值 |
|----|----|
| 条目 / 类目 | `MJ-CJM/DSH-Bot#dsh-bot` / `workflow`([registry](../../../data/plugins/MJ-CJM__DSH-Bot--packages-dsh-bot.yml)) |
| 子分类 | `im-personal-hubs`(注册表实装个人管家) |
| 自述 | 带持久化记忆、多 Bot 群协作与原生后台任务的 DSH 个人 Agent 工作台 |
| 星标 / 下载(2026-11-27) | **100★ / 8 forks**;npm **`dsh-botgroup@0.7.4`** 月下载 **1,854**(创建 `2026-10-18`,push `2026-11-26`) |
| 包形态 / 许可 | TS Monorepo 子包 `packages/dsh-bot` + Release `dsh-bot.tgz`;**MIT** |
| 代码规模 | `packages/dsh-bot/src/` **491 文件 / 64,195 行 TS**;`tests/` 262 套件 / 73,448 行;`evals/` 159 文件;`formal/` TLA+ 5 文件 |
| 宿主钉版 | `engines.dsh: ">=0.2.1-rc.2 <0.3.0"`;**14 条 peer** + 6 条 runtime deps + 7 个前端 UI 插槽包 |
| repo@commit | `4f08cf12d2fb7d046b7637ba8e848643eba1104e`(2026-11-27 +0800) |
| 证据等级 | ★★★ |

## 它到底是什么

**一个把“多 Bot 个人工作台”按安全操作系统标准重写进 DSH 的重工程插件。** 每个 Bot 经 `composer.ts:47-113` 动态编译成原生 DSH Agent Preset(`bot-<botId>`),以 `{ botId, botCreatedAt }` 二元组标识代次(删后重建同名 Bot 绝不继承旧会话、定时任务或私有记忆,`registry.ts:78-94`)。记忆走只追加 op-log 内核(`dsh_bot_memory` v3),一切跨 Bot / 跨群 / 外部输出均受信息流控制(IFC)拦截:

```text
用户私聊 / 群消息
  → agent/pre-step 单调记录会话污点标签(flow_sessions) + 读记忆记 versionIds 血缘
  → tools.guard 放行 28 个已审计原生工具(硬拦未知外部 MCP 与 run_code)
  → 跨边界外发(私转共享 / 群回复 / 外部出口) → EgressChecker 核验标签、epoch、代次
     ├─ 需确认(直推/同步出口) → 原生 approval.request('allowed-once') → 内存不可序列化 OnceGrant(5m TTL) → 原子消费落账
     └─ 群工作器外发(异步) → holdForReview 挂起 'awaiting-approval' → 纯文本摘要+SHA256 UI 审核 → 先脱敏消费再发 OnceGrant
```

## 怎么接进 DSH

1. **极简 Patch(`packages/dsh-bot/cordis.patch.yml:1-13`)**:仅 13 行,插入单插件 `id: dsh-bot`, `name: dsh-botgroup`,数据目录 `$DSH_HOME/dsh-bot`,记忆注入上限 4,000 字符。
2. **启动期自校验(`src/index.ts:12-54`)**:`apply()` 前逐文件校验 `host/`、`shared/`、`typert*` 与 `module-manifest.json` 的 SHA-256 哈希,并核对所有动态导入命名空间的 `DSH_BOT_MODULE_VERSION`,防热重载混用旧模块。
3. **11 项宿主服务 + 10 组 Typert RPC + 7 类 UI 插槽(`src/host/index.ts:42-265`, `src/client/index.tsx:94, 522-677`)**:注入 `storageDomain`、`agentPresets`、`typert`、`subagents` 等 11 个原生服务,开启 7+ 存储域,接入原生 `@deepseek-ai/dsh-tool-schedule` 与 `subagents` spawn(不另造 cron 守护进程),并在主面板、侧栏、会话行、对话顶栏、输入框 dock 与右侧栏挂满原生 UI。

## 关键实现

| 模块 | 位置 | 作用与源码实证 |
|---|---|---|
| 动态 Preset 与代次隔离 | `src/host/composer.ts:47-113`, `src/host/registry.ts:71-123` | 克隆 `standard`/`minimal` 模板替换 `dsh-persona`、补齐 `dsh-tool-schedule`、按 Bot 设独立 `customSkillDirs`;所有记录绑定 `{ botId, botCreatedAt }` 防“借尸还魂” |
| Op-Log 记忆与强遗忘 | `src/host/memory/{domain-v2,context,tools}.ts` | 权威 `ops`+`payloads` 与投影分离;注入时按 `audience` 全员 `canReadLabel` 过滤(私密记忆永不自动进群)且 JSON 引用防注入;`bot_memory_forget` 递增 `forgetEpoch` 并挂起受影响会话直至清理核验 |
| 三层 IFC 与一次性授权 | `src/host/data-flow/{tool-guard,egress,grants,outlets,native-policy}.ts`, `src/host/memory/confirmation.ts` | 28 个 `rc.2` 原生工具白名单并在首轮 `pre-step` 锁 `ToolDefinition` 对象身份防影子替换;`OnceGrant` 仅存内存不走 JSON 序列化;外部出口硬判 `'Shared is not public'` |
| 群外发离回合审核 | `src/host/groups/export-review.ts:19-249`, `src/host/data-flow/outlets.ts:124-161` | 群子任务回复触碰私有记忆即停在 `awaiting-approval`(重启不放行);审核界面强制纯文本+SHA256 防 Markdown 隐藏图片外泄;`approveReview()` 先擦除审核行再发 `OnceGrant` 防崩溃重放 |
| 防注入 Supergroup 与零模型群根 | `src/host/supergroup/{tool,service}.ts`, `src/host/groups/root-guard.ts:1-56` | `bot_supergroup` **拒绝模型传入自由任务文本**(`tool.ts:16`),只校验并共享最新真实人类文本消息;`root-guard.ts:52-55` 禁止群根会话直接调 LLM,仅允许单次指纹匹配的 `SetupPermit` |
| 形式化与红队自证 | `formal/bot_message.tla:1-86`, `formal/stale_grant_negative.cfg`, `evals/` | TLA+ 验证 6 条不变量(`NoStaleGrant`/`NoCrossBirth`/`NoResurrection` 等)并附负对照;60 条红队用例 + 160 条记忆冲突 + 64 条回放用例 |

## 为什么它突出

只用本仓库自身证据:

- **DSH 生态里罕见的“安全工程级”个人 Agent**:把信息流污点追踪、精确内容 `OnceGrant`、群外发纯文本审核、`forgetEpoch` 强遗忘、TLA+ 形式化模型与 SHA-256 模块自检一次性做进了注册表可装插件。
- **高度诚实的 fail-closed 边界**:面对宿主 `rc.2` 的真实能力缺口(`auto-share.ts:32-35`、`proactive/workspace-process.ts:4-8`),直接显式关掉功能并写明原因,没有用提示词糊弄。
- **不另起炉灶的原生复用**:定时任务复用 `@deepseek-ai/dsh-tool-schedule`,委派复用原生 `subagents` spawn 与 `tools/pre-execute` 审批链,完全长在 DSH 原生对象模型上。

## 代价与边界

1. **严苛的宿主版本锁死**:14 条 peer 全部带 `<0.3.0` 上界并硬编码 28 个 `rc.2` 原生工具名(`NATIVE_TOOL_NAMES`),DSH 升级 `rc.3+` 或 `0.3.0` 极易触发不可装或白名单失配(仓库红队清单已记录 `rc.3 Host cannot listen`)。
2. **闭环工具集与开放生态冲突**:`protectDataFlow()` 硬拦任意未接入的第三方 MCP 工具与 `run_code`,安全换来的是与大量社区工具插件不兼容。
3. **两项承诺能力目前处于硬关闭态**:`effectiveAutoShare: false`(无自动私转共享)与 `workspaceExecutionAvailable = false`(无主动后台工作区子进程)。
4. **同工作区无 OS 文件隔离**:所有 Bot 共享 `'Bots'` 工作区根目录(`bot-context.ts:176`),且无独立浏览器/云 VM 沙箱。
5. **包名陷阱与评测未全跑**:npm 真名是 `dsh-botgroup` 而非 `dsh-bot`(后者是无关作者的旧包);24 条连续 Agent 真实模型评测目前 `NOT_RUN`。

## 可信度与复现

**读过**:`data/plugins/MJ-CJM__DSH-Bot--packages-dsh-bot.yml`、`packages/dsh-bot/{package.json,cordis.patch.yml,src/index.ts}`、`src/host/{index,registry,composer,bot-context}.ts`、`src/host/memory/{domain-v2,context,tools,confirmation,auto-share,quota}.ts`、`src/host/data-flow/{egress,grants,tool-guard,outlets,native-policy}.ts`、`src/host/groups/{export-review,root-guard}.ts`、`src/host/supergroup/{service,tool}.ts`、`src/host/native-schedule/service.ts`、`src/host/proactive/{lifecycle,workspace-process}.ts`、`src/host/delegate/tool.ts`、`src/client/index.tsx`、`formal/bot_message.tla` 与 3 份 `.cfg`、`evals/manifests/*`。**未读**:`tests/` 单测正文、React 组件正文、`connectors/` 与 `messaging/` 细节,未实跑测试或 TLC。

```sh
git clone --depth 1 https://github.com/MJ-CJM/DSH-Bot && cd DSH-Bot
git rev-parse HEAD   # 4f08cf12d2fb7d046b7637ba8e848643eba1104e
npm test
curl -s https://api.npmjs.org/downloads/point/last-month/dsh-botgroup
```

## 待验证

- 未在真实 DSH `0.2.2-rc.x` 上实测加载与 `NATIVE_TOOL_NAMES` 兼容度。
- 未实跑 `formal/bot_message.tla` 的 TLC 模型检验与 `evals/continuous-agent` 真实大模型评测。
- 未读 `src/host/connectors/` 核实已接入的受管外部连接器清单。
