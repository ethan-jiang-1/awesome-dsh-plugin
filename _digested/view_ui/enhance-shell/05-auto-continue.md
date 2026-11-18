# dsh-auto-continue — 把「继续」做成宿主侧单实例状态机:一张收尾判据表、九道闸门、32 条冷读预算

> 证据等级:★★★(源码级;`HsiangNianian/dsh-auto-continue@dea916849980f2d65e09018589c7d6fed859f141`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 26、下载 3804 均为 2026-08-19 冻结采样;2026-11-18 实时星标 204(GitHub API;本卡复核时读到 205)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `HsiangNianian/dsh-auto-continue`([registry](../../../data/plugins/HsiangNianian__dsh-auto-continue.yml)) |
| 类目 | ui(2351 条;[census](../../ecosystem/census.py));子分类 [enhance-shell](README.md) |
| 自述 | 「DSH Web 请求中断自动续跑:网络、超时或宿主崩溃等非人为失败后自动发送「继续」,支持错误分类、自适应退避、模板化继续文本与浏览器通知」。源码比 registry 自述多的四块:重启后的冷读扫描、子会话交接、goal 重新武装、循环守卫 |
| 星标 ⚠ | **26**(2026-08-19 采样,建仓第 5 天);**实时 204**(2026-11-18) |
| 下载 ⚠ | **3804**(2026-08-19;边车 `data/downloads.json`,npm `last-month` 口径——包首版 2026-08-14T04:24Z 才发布,所以这 3804 是「首 5 天」的月窗口值) |
| 扩散 | **0**(命令与逐条人工判定见「为什么它突出」) |
| 仓库 commit | `dea916849980f2d65e09018589c7d6fed859f141`(2026-11-16,`chore: release v0.20.1`);API `created_at` 2026-08-14T03:08Z、`pushed_at` 2026-11-17、66 个 tag、25 forks、0 open issues、MIT、`size` 10892 KB、默认分支 main |
| 包形态 | npm `dsh-client-auto-continue@0.20.1`(66 个版本,首版 0.2.0 在 `created_at` 后 76 分钟发布);`package.json:35-46` 同时声明 `dsh.bundle.patch` 与 `dsh.client`(web 平台 + 4 个 inject);host 半 ESM bundle、client 半 CJS 模块封装(`build.mjs:64-98`) |
| 代码规模 | `src/` **6956** 行 / 19 文件(host 3005 / client 2523 / shared 1088 / 入口 340);测试 **8974** 行 / 32 个 `.mjs`。口径:`find src -type f \| xargs wc -l \| tail -1`,测试同理限 `tests -maxdepth 1 -name '*.mjs'` |

## 它到底是什么

**它是一个完整的双半插件,不是配置包,也不是某个外部系统的适配层。** host 半是引擎(`src/host/engine.ts`,2834 行),browser 半只是壳(`src/client/`,2523 行,其中 643 行是设置卡片)。引擎跑在 **DSH host 进程**里,源码开头就把这条设计说死了:整个 host 只有一个引擎,所以"多标签页重复发送"这类 bug 在构造上不存在(`src/host/engine.ts:1-14`);浏览器半侧在 0.8.0 之后只 re-export 共享 core(`src/client/engine.ts:3-5`)。

**核心数据模型只有四层:**

- `SessionState`——每会话一份**宿主内存态**(`src/shared/core.ts:944-1014`):连续次数、上次尝试时间戳、待回显消息 ID、待发定时器、`running`/`queued`、工具跟踪器、loop guard 信号、断网挂起令牌、自主循环轮数。`freshState()` 给出全量初值(`:1016-1048`)。
- `DayStats`——单实例今日统计,按本地日期滚动(`:911-941`;`engine.ts:596-599` 读时跨天自动换桶)。
- `RecoveryAttempt[20]`——最近 20 次"已发送"记录,只用于展示(`engine.ts:1964`)。
- 每会话模式 `sessionModes`——唯一**持久化**的会话级状态,写在设置命名空间里(`src/index.ts:88`,写入走路径变更 `:296`)。

**它认为哪些收尾算「中断」**——这是全插件最该先看懂的一张表,分实时与扫描两条路径:

| `turn/end` 收尾 | 实时路径 | 重启/扫描路径 | 结论 |
|---|---|---|---|
| `error`(临时性:网络/超时/5xx/429/上游) | `engine.ts:1339-1350` → `onTurnFailure:1375-1408` | `scanInterrupted:2217-2229` → 同一处理 | 续跑,记 `lastFailure` 供模板与分类 |
| `error`(永久:401/403、认证、余额、模型不存在、上下文超限、invalid_request) | `core.ts:343-363` 判永久后跳过 | 同 | **不续**,`skipped` 计数,`notify` 开着才通知(`engine.ts:1392-1406`) |
| `max-tokens` | `engine.ts:1351-1355` | `isNonHumanReason`(`core.ts:321-325`) | 续跑,用 `continueTextMaxTokens` |
| `no-visible-output`,或 `completed` 但只观察到推理/无可见输出 | `engine.ts:1255-1271` | `engine.ts:2206,2211` | 续跑,用 `continueTextSilent`;这是**失败**语义,不清零重试预算 |
| `interrupted` | 实时路径**不续**,只清零预算(`:1333-1338`) | 正常候选 | 只由扫描恢复(崩溃修复在冷读时合成,`core.ts:315-319` 注释) |
| `aborted` 且 cause ∈ {`user`,`parent`,`hook`} | `:1292-1330` 视为人为介入 | 不满足条件被跳过;子会话另有 `DECISION_CANCEL_CAUSES`(`engine.ts:169`) | **永不续跑** |
| `aborted` 且 cause ∈ {`disposed`,`legacy`}(宿主关闭/重启) | 不实时处理 | `:2202-2203` 改判成 `interrupted`;判定函数 `isHostCancel:361-366` + `RESTART_CANCEL_CAUSES:167` | 续跑,用 `continueTextInterrupted` |
| `blocked`(策略拒绝) | `:1331-1332` | — | **永不续跑** |
| 维护回合(`turn/start` 的 `reason === 'message-ops'`) | `:1243-1248` | `:2205` | 跳过,且不算成功也不算失败(`tests/maintenance-turns.mjs:62`) |

三个容易漏的口径:**①「网络」不是一种 `turn/end` 原因,而是 `error` 的一个子类**——由 `isNetworkFailure()` 按 code/消息识别(`core.ts:378-382`),用来决定是否先做连通性探测;**②「宿主崩溃」在实时流里看不到**,重启后靠日志尾部判定;**③ 主会话的「开着的回合」**(有 `turn/start` 没有 `turn/end`)在扫描里被直接跳过(`engine.ts:2211`),它依赖 DSH 修复管线把尾部合成为 `interrupted`;只有子会话自己覆盖这种形态(`classifyChildInterruption` 返回 `'open-turn'`,`engine.ts:382-390`)。

**续跑消息本身**由「模板 + 可选护栏」拼成(`buildContinueText`,`engine.ts:2090-2110`):模板按原因选(`templateFor:1605-1613`,顺序是 loop → 自主循环 → `:silent` → `max-tokens` → `interrupted` → 通用),占位符 `{code}/{message}/{status}/{tool}/{turn}/{errorCount}/{sessionTitle}/{elapsed}/{result}` 由 `fillTemplate` 填(`core.ts:427-438`)。护栏读"上一步工具调用的结局":无结果 → 追加「可能没完成,先核实再继续」;成功 → 追加「已完成,结果摘要 xxx,不要重跑」;失败 → **不追加**(重试本来就是目的)(`core.ts:754-762`、`engine.ts:2102-2108`)。

## 怎么接进 DSH

**分发与识别,两行 manifest 搞定:**

1. `package.json:35-46`:`dsh.bundle.patch` 指向 `./cordis.patch.yml`;`dsh.client` 声明 `platform: 'web'` 与四个 inject(`dsh-client-connection`、`dsh-client-locale`、`dsh-client-ui-settings`、`dsh-client-ui-settings-plugins`)。入口分离在主/子路径导出里:`main: lib/index.js`、`exports["./client"] → lib/client.js`(`:6-19`)。
2. `cordis.patch.yml:5-7`:全部机制就是一条 `insert`,id `auto-continue`、name `dsh-client-auto-continue`。
3. 安装:`dsh plugin --profile web add dsh-client-auto-continue@latest`(`README.md:64`;也支持 `github:HsiangNianian/dsh-auto-continue`,`:89`)。

**host 半的注册点(`src/index.ts:149-340`):**

- 配置:**Loader 自带 config**,不是老式 `settings.register` 命名空间。`apply(ctx, config)` 先判 `'get' in config`(`:151-154`),用 `Config` 的 `volatile()` 拿活引用(`:127-133`)。只有旧宿主才走 `ctx.inject(['settings'])` 注册命名空间(`:157-171`),且显式防御"桌面宿主两套 API 同时存在"导致读写分叉(`:162-164`)。
- 引擎:`ctx.inject(['agents','webServer'])` 内 new `AutoContinueRunner`(`:178-182`),依赖可重入时先 dispose 旧引擎(`:180`)。
- 子代理服务:**懒注入** `ctx.inject(['subagents'])`,只塞一个 provider 闭包,服务卸载就清空(`:188-193`)——因为 subagent 服务可能比本插件晚加载。
- 状态桥与动作端点:`ctx.webServer.register({kind:'exact', path:'/api/auto-continue-bridge'})` 输出 SSE(`:241-268`,20s 一次 `: ping` 心跳 `:255-259`);`/api/auto-continue-action` 收 POST(`:271-316`)。两条路由都注册在宿主端口上。
- 设置变更订阅:同一回调绑三个事件名 `settings/updated`、`settings/document-updated`、`app-boot/config-reload`(`:237-239`),因为不同代宿主发不同名字。
- 生命周期:`engineCtx.effect(() => dispose)` + 顶层 `ctx.effect` 双保险(`:317-339`),注释解释了为什么 dispose 必须挂顶层——挂派生 ctx 的 effect 在 config HMR 时不会跑,悬空定时器会撞 inactive context 炸进程(`:172-175`)。

**用到的 DSH 契约(我逐个在本机 0.2.1-rc.5 里核过):**

| 契约 | 本插件用法 | DSH 侧声明 |
|---|---|---|
| `session/event` | 全量事件火管 `engine.ts:539-549` | `dsh-session/lib/types/index.d.ts:61` |
| `Agent.followup(message)` | 唯一发送方式 `engine.ts:1937` | `dsh-agent/lib/types/runtime-types.d.ts:192` |
| `Agent.cancel(cause,{keepInbox})` | loop guard 打断 `engine.ts:1200` | 同上 `:157`(`CancelOptions` `:33-40`) |
| `agent.inbox.nextTurn` / `remove` / `prepend` | 把续跑消息提到队首 `engine.ts:552-580` | 同上 `:145` |
| `agent/inbox/inserted` | 同步插入钩子(唯一能"趁驱动还没认领"改序的时机) | 同上 `:263` |
| `settings.mutate(ns, ops)` | 写会话模式 `src/index.ts:296` | `dsh-settings/lib/types/index.d.ts:114` |
| `ctx.webServer.register` | 两条 HTTP 路由 | `dsh-host-webserver/lib/index.js:326` |
| slot `conversation.input.left` | 输入框左侧开关 | `dsh-client-ui-conversation/lib/client.js:20108` |
| slot `plugins.bundle.config` | 插件页主体 `client/index.ts:181-191` | `dsh-client-ui-plugin-manager/lib/client.js:4440` |
| slot `settings.plugin.item` | 旧设置卡 `client/index.ts:170-180` | **0.2.1-rc.5 未声明**(该版本只有 `settings.plugins.tab`) |

最后一行是个真实的接入事实:插件同时注册了新旧两个设置位,新宿主只认 `plugins.bundle.config`,旧注册静默不生效(`ctx.slots.inject` 会一直等声明)。同一份卡片代码被包进 `AutoContinueSettingsPage` 的 `<ul>` 里,因为 bundle 页不给列表容器(`settings-card.tsx:321-327`)。

## 关键实现

**文件结构(按角色):**

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `src/host/engine.ts` | 2834 | 引擎:事件→判定→闸门→发送→记账;启动扫描、存储扫描、子会话唤醒 | `481` 类;`539`/`552` 两个 hook;`1208` 事件状态机;`1531` 调度;`1873` 发送 |
| `src/shared/core.ts` | 1088 | 与 UI 共享的纯逻辑:配置、分类、模板、退避、工具跟踪器、回显识别 | `343` 分类;`602` 跟踪器;`879` 退避;`1080` 回显 |
| `src/index.ts` | 340 | host 入口:Loader 配置、引擎装配、SSE 桥、动作端点 | `149` apply;`241`/`271` 路由 |
| `src/host/connectivity.ts` | 54 | 连通性探测:网卡 + 3 个公网名 DNS | `PROBE_HOSTS:10` |
| `src/host/settings-migration.ts` | 117 | 桌面宿主旧设置文档导入(走 profile editor,不碰原文件) | `:30-45` |
| `src/client/settings-card.tsx` | 643 | 6 类设置表单 + 3 个实时面板 | `330-337` 分组;`454-585` 面板 |
| `src/client/bridge.ts` | 261 | SSE 订阅、断线重连、浏览器通知 | `148-189` 通知;`195-261` 重连 |
| `src/client/composer-toggle.tsx` | 97 | 输入框 28px ∞ 开关 + 模式菜单 | `60-97` |
| `src/client/settings-form.ts` | 313 | 暂存式表单模型(改完点保存才写) | `:1-13`,`canWriteSettings:18` |
| `src/client/locales.ts` + `locale/*.json` | 516 | zh/en/ru 三语设置卡文案 | `client/index.ts:86-87` 注册 |
| `tests/*.mjs` | 8974 / 32 文件 | 6 个宿主 cohort 夹具 + 契约测试 | 见「可信度」 |

**一次续跑的完整数据流(数字是闸门顺序):**

```
session/event ──▶ onHostEvent(921) ──▶ onSessionEvent(1208)
   turn/end
     ├─ 维护回合 / 畸形 reason ──▶ 直接 break
     ├─ completed + 可见输出 ──▶ consecutive=0（成功重算预算）
     └─ error / max-tokens / silent / (loop 模式的 completed)
          └─ onTurnFailure(1375)  [error 才做分类]
               └─ schedule(1531)
                    ① loop 开关 ② 全局 paused ③ 会话暂停(pauseUntil)
                    ④ 已有待发 ⑤ 断网挂起中 ⑥ 循环轮数上限
                    ⑦ consecutive >= maxConsecutive(默认 3)
                    ⑧ 冷却未到 ──▶ deferCooldownRetry(1587) 到点再调度
                    ⑨ graceMs(默认 3000)后 fireWhenOnline(2037)
                          └─ 网络类失败先探测在线;离线则挂起、不扣预算
                               └─ fire(1873) 重新校验全部开关
                                    ├─ 取模板 + 填占位符 + 追护栏(2090)
                                    ├─ 无 live agent ──▶ 跳过(子会话可冷恢复)
                                    ├─ trackPendingEcho(1934) ──▶ agent.followup(1937)
                                    └─ consecutive += 1 / 记账 / 通知 / 触顶提示
```

**退避与上限。** `effectiveCooldown = min(max(base, base·factor^consecutive), max(base, backoffMaxMs))`(`core.ts:879-888`),默认 base 20 000ms、factor 2、上限 300 000ms(`core.ts:190-200`)。注意指数用的是**已经发出的次数**:发过一次失败后续跑,冷却已是 40s,而不是 20s。`lastAttemptAt` 在发送**之前**写入(`engine.ts:1927`),loop guard 的打断也记这笔账(`:1192`),所以"打断"和"发送"共用一套预算。

**重复防护(五层,互不替代):**

1. **回显识别**:发消息前登记 message id(`engine.ts:1934`),自己的 `user/message` 回来时按 id 消费掉、当作没发生(`core.ts:1080-1088`;窗口 10 分钟、上限 64 个 id,`:1051-1054`)。这是最关键的一层:**不认自己的回显,每次续跑都会被当成"用户发了消息",`consecutive` 被清零,连续上限就永远不生效**。`usePluginSource` 打开后消息带 `plugin:dsh-client-auto-continue` 来源(`core.ts:9`),但回显匹配对两种来源都接受(`:1083`)。
2. **单飞定时器**:有 `pendingTimer` 就不再排(`engine.ts:1543`);冷却重排先清旧 timer(`:1589`);loop 重启另有 `loopRetryTimer` 并在新回合清掉(`:1229-1232`)。`cancelPending` 一次清四类定时器(`:1615-1643`),在新回合(`:1233`)、新 `turn/end`(`:1239`)、用户消息(`:1365`)、手动续跑(`:1512`)、通知按钮暂停(`:1430`)处调用。
3. **队列内提优先级**:若 `agent.inbox.nextTurn` 非空,先登记 id,再在同步的 `agent/inbox/inserted` 里 `remove` + `prepend`,失败则回滚 `append`(`engine.ts:1935-1943`、`:552-580`)——避免续跑排在用户已排队的消息后面(也避免那段时间里被取消)。
4. **扫描去重**:`bootScannedSessions`(WeakSet)让每个会话每次启动只裁决一次(`:501`、`:2213/:2225/:2252`);存储扫描与子会话各有独立台账(`:505/:507`);坏日志连续失败 3 次放弃(`:131`、`:517`);每轮最多 `scanLimit`=8 次恢复(`core.ts:194`、`:2247-2249`)。
5. **子会话交接限流**:同一子会话失败交给主会话最多 5 分钟一次(`HANDOFF_COOLDOWN_MS:175`)、主会话离线时进 `deferredHandoffs` 等待(`:1831-1871`)、冷恢复在途去重(`reviveInFlight`)、同一批子会话只唤醒 root 一次(签名比较,`:513`、`:2591-2620`)。

**启动/重启恢复是三种扫描叠起来的**(不是一条):

- 实时 agent 扫描:`bootScanLoop` 每 3s 一轮、只跑 `freshMs`(默认 15 分钟)窗口(`engine.ts:2121-2162`);候选按最近活动倒序、最多恢复 8 个(`:2246-2249`)。
- 存储会话扫描:对没有 live agent 的历史做冷读,**一次启动最多读 32 个日志**(`engine.ts:138`、`:2372-2380`),单次读超时 5s(`:129`),解释写在注释里:冷读要整份解码 zstd→逐行 JSON.parse,几百个会话连读足以把默认约 3.4GB 堆打满(`:132-137`)。
- 子会话扫描:每轮最多冷读 8 个子日志(`CHILD_SWEEP_LIMIT:171`),按 root 归组后只给 root 发一条清单,由 root 决定继续还是收尾(`:2518-2654`)。

## 为什么它突出

**先拆星标归属,这一次是干净的。** GitHub 只有仓库级星标,而这个仓库**整个就是插件**:没有 monorepo 子目录、没有主项目可借。时间线:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-14T03:08Z | 仓库创建 | GitHub API `created_at` |
| 2026-08-14T04:24Z | npm 首版 `0.2.0`(建仓 76 分钟后) | npm registry `time` |
| **2026-08-19** | **26 星采样点(建仓第 5 天)** | 边车 ⚠ |
| 2026-11-13 ~ 11-17 | 0.19.0 → 0.20.1(全仓共 66 个 tag) | CHANGELOG / API |
| 2026-11-18 | **204 星**(实时;我复核时 205) | GitHub API |

所以 26 → 204 是真的 7.8 倍增长,没有任何归属争议;下载 3804 同样只能记在它自己名下(且是首 5 天的月窗口值,不是三个月累积)。

**扩散是 0,而且这个 0 有信息量。** 口径:

```sh
grep -ril 'HsiangNianian' data/plugins/ | wc -l            # → 1（只有它自己的 registry）
grep -ril 'dsh-client-auto-continue' data/plugins/ | wc -l # → 0（包名在第三方条目里零出现）
grep -ril 'auto-continue' data/plugins/ | wc -l            # → 14
```

14 条我逐条看过内容:**它自己 1 条;同名不同作者 5 条**(`43aquarius/dsh-auto-continue` 走模型链切换、`haochi72/dsh-auto-continue-429` 只认 429/配额、`imcaibaicai/dsh-auto-continue-inturn` 做同轮内续写、`VergilYe/dsh-auto-continue` 做流式守卫、`zhou1736948757-cpu/dsh-auto-continue` 面向小输出上限);**近义机制 6 条**(`dsh-turn-continue`、`dsh-interrupted-resume`、`dsh-stall-guard`、`dsh-continue-on-limit`、`dsh-auto-retry`、`dsh-task-reliability`);**误命中 2 条**(`dsh-mic-input` 的"自动续听"、`dsh-compact-agents` 的"自动续写预算")。**没有一条提到本仓库、作者或包名**,也没有一条 fork 自它。

这是个值得记下的形态:**名字被抄了,代码没被引。** 另外五个作者各起了一个 `dsh-auto-continue*`(或同义词),说明"断了就补一句继续"在 DSH 里已经是共识需求;但零引用说明它没有成为被依赖的原语——它把复杂度都花在**判据**上(哪些收尾算中断、什么时候不该发、重启后怎么找回),而这部分恰恰是抄不走也看不出来的。26 星时它已经有完整分类器与扫描器,那时没人会为了"自动继续"去读 2834 行宿主引擎。

**支持这个判断的自身证据,不再是星标:**

- **测试比源码长**:32 个 `.mjs` / 8974 行,对 6956 行 `src/`。测试不是摆设——(`tests/failure-classification.mjs:10-33`)构造了一组"畸形响应里回显了 `api_key`/`quota exceeded`/`context limit` 等字样"的用例,要求它们**仍然可重试**,同时真的 401/403/余额/模型/上下文错误**必须跳过**(`:50` 断言 `sent=9`、其余 `skipped`);(`tests/offline-and-loop-cap.mjs:78-99`)证明断网挂起期间复检不消耗 `maxConsecutive`;`tests/manual-resume-pauses.mjs:29-51` 证明"立即续跑"只豁免一次、不解除暂停;`tests/echo-matching.mjs:11-30` 证明回显只消费一次。
- **CI 跑六个宿主 cohort**:`0.1.7 / 0.2.0 / 0.2.0-rc.2 / 0.2.1 / 0.2.1-rc.2 / 0.2.2-rc.1`(`package.json:54`,`tests/fixtures/*/package.json`),外加 typecheck、build、`git diff --exit-code -- lib`、以及一个**按 commit pin 的第三方插件检查器**(`.github/workflows/plugin-check.yml:46-58`)。
- **94 天 66 个 release、25 个 fork、0 open issue**;issue 号已经做到 #91,每个修复都带 PR 号和致谢(CHANGELOG 里 `@anthonyhann`、`@kesha4`、`@palxex`、`@xiuchuan666`、`@loyalchiiina`、`@fu050409` 等外部贡献者),说明它真的有人在用、有人在报。
- **机制上有几处不是"顺手写的"**:`MALFORMED_RESPONSE` 被强制视为可重试,理由是"畸形模型输出会回显工具参数,看起来像认证/配额错误"(`core.ts:353-354`);loop guard 用**专属 cancel cause** `{kind:'hook', reason:'dsh-auto-continue:loop-guard'}`(`engine.ts:107-111`),只有持久化的 `turn/end` 精确带回它才重启回合,借 DSH 的 first-cause 语义保证"用户点停止"永远优先(`:1178-1182`);存储扫描的 32 条配额、子会话 8 条配额、5 分钟交接冷却都是把"重试"换算成**宿主资源**之后的参数,不是拍脑袋的常量。

## 代价与边界

- **它替模型花的钱是真实的。** 每次续跑都是一次完整模型回合;默认 `maxConsecutive`=3 只约束**失败**,而"有可见输出就清零"意味着成功续跑不消耗预算(`engine.ts:1279-1284`、`:1952`)。打开自主循环后每个 `completed` 都续跑且 `force` 跳过冷却与上限(`:1278-1285`),`loopMaxIterations` 默认 **0 = 无限**(`core.ts:216`)。这是它最大的代价,也是默认关闭循环的原因。
- **失败模式,按发生顺序:**
  1. host 半没加载 → `/api/auto-continue-bridge` 404,设置卡与输入框开关退化成只读/不显示,但不会崩(README 的排障表已列出)。
  2. 会话无 live agent(没打开过、已物化失败)→ 直接跳过(`engine.ts:1914-1926`);只有子会话会尝试冷恢复。
  3. 永久错误 + `notify` 默认 `false` → **静默跳过**,用户只在 `[auto-continue]` 日志里能看到原因(`:1392-1406`)。
  4. 重启超过 `freshMs`(15 分钟)才回来看 → 不恢复(`:2211-2212`);这正是"隔夜再开就没动静"的成因。
  5. 存储会话超过 32 条配额 → 按最近活动排序,后面的**本次启动直接跳过**(`:2372-2380`),日志只有一行提示。
  6. 子会话在 grace 期结束前已被宿主 dispose → 走冷恢复;宿主没有该服务就退化成给主会话的一条交接消息(`:1884-1892`、`:1914-1926`,CHANGELOG 0.20.0 说明了这个时序)。
  7. 桥断流 → 输入框开关保留最后一次策略、变灰只读,500ms 后重连(之后 3s)(`bridge.ts:195-261`)。
  8. 引擎上下文失活 → 定时器回调都有 try/catch,但只写日志(`engine.ts:1567-1572`、`:2071-2079`)。
- **`/api/auto-continue-action` 没有授权层。** 我在本机 `dsh-host-webserver` 里读到的分发逻辑只做 exact/prefix 路由匹配(`lib/index.js:495-505`),没有 origin/CORS/鉴权中间件;插件自己只校验 `sessionId` 形状、长度与原型污染键名、以及 `isSessionMode`(`src/index.ts:285-288`),请求体**不看 Content-Type 直接 `JSON.parse`**(`:282`)。判断:能访问宿主端口的本机进程都能改会话模式、清统计、触发一次续跑;一个跨站页面用 `text/plain` 的简单请求也能触发同一路径(读不到响应,但副作用发生)。我没实测,列在「待验证」。
- **浏览器通知的按钮大概率不显示。** host 侧通知带 `actions`(`engine.ts:264-275`、`1411-1420`),browser 侧直接用 `new Notification(title, {actions})`(`bridge.ts:148-176`)。按 Web 平台现状,`actions` 只在 `ServiceWorkerRegistration.showNotification` 的持久通知上生效;普通 `new Notification` 会忽略它。所以「立即续跑 / 暂停 1 小时」很可能只剩标题和正文可点(点了只是聚焦窗口)。这是判断,未在浏览器里实测。
- **兼容成本集中在"宿主 API 漂移"**:同一语义要绑三个设置事件名(`src/index.ts:237-239`);两套设置 API 并存时要防读写分叉(`:157-171`);`settings.plugin.item` 在 0.2.1-rc.5 已无声明;`snapshotEvents()` 与 `events` 两种历史读法都要兼容(`engine.ts:287-294`)。六个 cohort 的 runtime 矩阵就是这笔账的账单。
- **数据与隐私**:引擎在宿主进程内读全部会话事件与历史;统计、暂停列表、重试计数全在内存,重启即失(`README`「Privacy」段与 `engine.ts:482-527` 一致);唯一持久的是设置(含 `sessionModes`);离线探测只做 `os.networkInterfaces()` + 三个域名的 DNS 解析,不建连接(`connectivity.ts:13-52`);`resumeGoals` 会替用户在重启后重新武装 goal,所以默认关(`src/index.ts:109-112`),`resumePausedGoals` 更默认关——"暂停是人做的决定"。
- **维护成本**:66 个 release / 94 天,意味着升级很频繁;`lib/` 是提交进仓库的构建产物(CI 会 `git diff --exit-code -- lib`),想改行为必须同时改 src 与产物,不能只 patch 安装目录。

## 可信度与复现

- **★★★**:`src/` 19 个文件里读了 `host/engine.ts`(逐段,约 900 行)、`shared/core.ts`(前 460 行 + 600-1088 行)、`index.ts` 全文、`client/index.ts`、`bridge.ts`、`composer-toggle.tsx` 全文,`connectivity.ts` 全文;`settings-card.tsx`、`settings-form.ts`、`styles.ts`、`settings-migration.ts` 只读结构与关键函数(非逐行)。测试读全 4 个文件,另 4 个读了大半或按断言行抽查,其余 grep。
- **DSH 对照**:本机 `@deepseek-ai/dsh@0.2.1-rc.5`,核了 `session/event`、`Agent.followup/cancel/inbox`、`agent/inbox/inserted`、`settings.mutate`、`webServer.register` 与三个 slot 声明。
- **未读**:`docs/` 的 svg/html/png 素材(仓库 `size` 10.9MB 的主要来源)、`README.ru.md`、`CHANGELOG` 0.16 以下、`locale/*.json`、`lib/` 产物、`tests/simulate-host.mjs`(3392 行,只 grep 了事件名)、`settings-card.tsx` 的渲染细节。**未运行** `npm test` 与 `npm run test:runtime`。

```sh
# 1) 克隆与提交（浅克隆即可，本卡只用一个 commit）
git clone --depth 1 https://github.com/HsiangNianian/dsh-auto-continue.git /tmp/ac
cd /tmp/ac && git log -1 --format='%H %ad %s' --date=short
# → dea916849980f2d65e09018589c7d6fed859f141 2026-11-16 chore: release v0.20.1

# 2) 代码规模
find src -type f | xargs wc -l | tail -1                      # → 6956
find tests -maxdepth 1 -name '*.mjs' | xargs wc -l | tail -1   # → 8974
grep -c '^## ' CHANGELOG.md                                    # → 12（0.16.0 起 + 一个 Earlier releases 指针）

# 3) 扩散（在 awesome-dsh-plugin 仓库根执行）
grep -ril 'HsiangNianian' data/plugins/ | wc -l             # → 1
grep -ril 'dsh-client-auto-continue' data/plugins/ | wc -l   # → 0
grep -ril 'auto-continue' data/plugins/ | wc -l              # → 14（人工筛:自身 1 + 同名 5 + 近义 6 + 误命中 2）

# 4) 星标/下载归属与时间线
curl -s https://api.github.com/repos/HsiangNianian/dsh-auto-continue \
  | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["created_at"],d["size"],d["stargazers_count"],d["forks_count"])'
curl -s https://registry.npmjs.org/dsh-client-auto-continue \
  | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["time"]["created"],len(d["versions"]))'

# 5) DSH 侧契约核实
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai
grep -n "session/event" $DSH/dsh-session/lib/types/index.d.ts
grep -n "followup(message" $DSH/dsh-agent/lib/types/runtime-types.d.ts
grep -n "plugins.bundle.config" $DSH/dsh-client-ui-plugin-manager/lib/client.js | head -2
grep -rn "settings.plugin.item" $DSH --include=*.js | head   # → 0 命中（0.2.1-rc.5）
```

## 待验证

1. **跑一遍测试**:`npm test`(32 文件)与 `npm run test:runtime`(需要 6 个 cohort 的 `npm ci`)。我只读了测试代码,没跑;尤其 `test:runtime` 依赖真实宿主 fixture,失败率未知。
2. **主会话"开着的回合"能不能恢复**:代码在 `engine.ts:2211` 跳过 `lastEnd === undefined` 的会话,依赖 DSH 修复管线把尾部合成为 `interrupted`(`core.ts:315-319` 注释)。用 `kill -9` + 冷启动真实 profile 验证:没有 `turn/end` 的主会话到底会不会被恢复。
3. **通知按钮到底能不能点**:在 Chrome/Safari 里打开 `notify`,观察 `new Notification(title,{actions})` 是否渲染「立即续跑/暂停 1 小时」;若不能,`onaction`(`bridge.ts:171-175`)就是死代码。
4. **动作端点是否可跨站触发**:构造一个 `Content-Type: text/plain` 的跨站 POST 打 `/api/auto-continue-action`,确认副作用是否发生(该 handler 不看 Content-Type,`src/index.ts:282`)。
5. **32 条冷读配额是否够用**:在 100+ 会话的 profile 上测启动耗时与堆峰值,并核对 `sessionProjectionCache` 的排序(`engine.ts:2479-2517`)在真实数据上是否真的近似最近活动。
6. **旧宿主(0.1.7)上的设置卡**:`settings.plugin.item` 是否真的被声明、卡片是否出现;`plugins.bundle.config` 那条在旧宿主上的行为是否如注释所说"一直等声明"(`client/index.ts:168-169`)。
7. **子会话冷恢复依赖的具体宿主 API**:`subagentPrompts()`(`engine.ts:1653-1675`)读的是哪个服务方法、哪些 DSH 版本注册了 `subagents` 服务、服务缺失时交接路径是否如 0.20.0 的 CHANGELOG 所述完整。
