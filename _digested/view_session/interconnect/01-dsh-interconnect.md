# dsh-interconnect — 一条共享密钥的 WebSocket,把文本投进对端 session 的 inbox

> 证据等级:★★★(源码级;`Chinesezjc/dsh-interconnect@59f89789a6ccd23b63953d1092778ead3ea3a56d`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 34 为 2026-08-19 历史采样,2026-11-18 实时 42;下载无记录,属该日采样缺口。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `Chinesezjc/dsh-interconnect`([registry](../../../data/plugins/Chinesezjc__dsh-interconnect.yml)) |
| 类目 | session([census](../../ecosystem/census.py) 914 条 / 全表 11 744 条) |
| 子分类 | `interconnect`(会话互连)——当前唯一成员 |
| 自述 | 「跨实例互联：经 interconnect 服务在多个 DSH 实例间转发消息与事件」。源码核对:转发的是**文本消息**与 **6 类生命周期事实**;assistant 流、tool call/result、审批都不在协议里 |
| 星标 ⚠ | **34**(2026-08-19 冻结采样);2026-11-18 实时 **42** |
| 下载 ⚠ | **边车无记录**(2026-08-19 采样缺口;`data/downloads.json` 无此 URL 键) |
| 扩散 | **0**(口径:`grep -ril 'interconnect' data/plugins/` 命中 **1** 条,即条目自身;`grep -ril 'chinesezjc' data/plugins/` 同为 1 条。对照词 `cross-session` 131 条、`multi-instance` 3 条是共享上下文/外部服务多实例语义,人工判断后不计入) |
| 仓库 commit | `59f89789a6ccd23b63953d1092778ead3ea3a56d`(2026-11-18,`main`,`Merge pull request #9 from Chinesezjc/docs/federation-protocol`);仓库创建 2026-08-13,124 个提交 |
| 包形态 | npm `dsh-interconnect`:源码 `0.17.0`,**npm 最新只到 `0.15.0`**(2026-11-06 发布);DSH profile bundle,`package.json:28-32` 的 `dsh.bundle.patch` → `cordis.patch.yml` 3 条 insert 行 |
| 代码规模 | `src/**/*.ts` **3 182 行**(6 文件,不含测试);测试 4 211 行 / 208 个 `it`;仓库 677 KB |
| 协议草案 | `docs/interconnect-federation.md` 635 行,**Draft 0.1、未实现**(`docs/interconnect-federation.md:3`):定义了跨管理域的 envelope/relay/回执,与现有代码没有对应实现 |

## 它到底是什么

**不是配置包,也不是外部系统的适配层,而是一组 DSH host 插件加一条新传输。** 仓库里没有第三方服务客户端:三个插件都挂在 host composition 上,核心是 1 894 行 TypeScript(`src/interconnect/index.ts`)。它也**没有独立 server 进程**——registry 自述里的「interconnect server」就是每台实例自己的宿主 webserver:有 webserver 的实例在它上面开一条 WebSocket 路由,并按 `Config.peers` 向对端拨同一条路由;没有 webserver 的 headless 组合只剩出站(`src/interconnect/index.ts:462-470`)。它做的事只有一件:把「本实例的一条文本」投进「对端某个 live session 的 inbox」。

对象模型只有四层,全部能从 `src/interconnect/types.ts` 确证,不是 README 转述:

- **link** — 每个配置对端一条持久 WebSocket(`src/interconnect/types.ts:250-256`)。寻址键是 `Config.peers` 的 `instanceId`,真正拨的 origin 是映射值(`src/interconnect/types.ts:410-440`);`instanceId` 不参与寻址,只出现在 `hello` 帧与回包里(`src/interconnect/index.ts:1504`、`src/interconnect/index.ts:1545-1554`)。`self` 是特殊值,拨向本实例自己的 webserver,端口每次拨号时现读(`src/interconnect/index.ts:1057-1063`、`src/interconnect/types.ts:410-424`)。
- **frame** — 6 种:`hello` / `event` / `msg` / `msg-result` / `query` / `query-result`(`src/interconnect/types.ts:250-256`)。`msg`/`query` 用 `reqId` 关联回复,`event` 是单向推流。**没有任何协议版本字段**,也没有能力协商。
- **message** — 一次 `send` 的载荷:`sessionId`(对端的)、`text`、可选 `sender`、可选 `delivery`、可选 `resume`(`src/interconnect/types.ts:43-72`)。`reply` 不是线上变体:它在本机查「本地 session → 最后发送方」的映射,再发一条普通 `send`(`src/interconnect/index.ts:606-626`、`src/interconnect/index.ts:1117-1121`)。
- **event** — 6 类生命周期事实的判别联合:`agent/created|disposed|status`、`session/created|disposed`、`subagent/end`(`src/interconnect/types.ts:223-229`)。订阅点正好 6 个,没有别的(`src/interconnect/index.ts:507-540`)。

**投递不是事件回放,是 inbox 拼接。** 接收侧 `deliver()` 先 `ctx.agents.get(sessionId)` 找 live agent,找不到才走 `wake()`(`src/interconnect/index.ts:1321-1338`);然后构造一条 DSH 原生 user 消息——`createUserMessage({ source: { kind: 'plugin:dsh-interconnect', form: 'notice', summary }, content: [{ type: 'text', text }] })`(`src/interconnect/index.ts:1365-1376`)——再按模式调 `agent.steer|inject|followup`(`src/interconnect/index.ts:1382-1396`)。写 session 日志的是**接收方的 Host**,发送方从不碰对端日志。

**事件通道是给别的插件用的钩子,不是消息通道。** 入站 `event` 帧只做两件事:一行 `logger.info`(`src/interconnect/index.ts:1161`),一次 `ctx.parallel('interconnect/event', notification, sender)`(`src/interconnect/index.ts:1164`)。该事件在 `Context.Events` 上声明(`src/interconnect/index.ts:99-110`),但**本仓库没有任何订阅者**——`grep -rn "interconnect/event" src/` 只命中声明与派发两处,其余命中全在 `tests/`。所以「事件转发」的落点是第三方插件,对端 session 收不到事件。

**状态归属:唯一权威源是接收方自己的 session 日志。**

- 两个实例**不共享** session 日志,也没有读写对端日志的代码路径。跨实例传递的只有一段文本;接收方 Host 把它记成 `role: user`、`source.kind: 'plugin:dsh-interconnect'`、`form: 'notice'`、`summary` 上限 120 字符(`src/interconnect/index.ts:1365-1376`;`boundContextSummary` 的截断在 `dsh-llm/lib/index.js:21-23`)。
- 因此不存在「同一 turn 两边同时写」:发送方只发帧,唯一写入者是接收方。两个发送方同时投同一个 session 时,裁决权在 Host 的 inbox——`next-turn` 排队与 `next-step` 插队的语义写在 `src/interconnect/types.ts:9-19`,插件不加序号、不加时间戳。
- 插件自己保留的跨实例状态只有两处:内存里的 `senders` 映射(每个本地 session 只记**最后一个**发送方,`src/interconnect/index.ts:392-393`、`src/interconnect/index.ts:1402-1406`)与磁盘上的 pairing sidecar(`src/interconnect/index.ts:851-857`)。两者都是本实例单写者。
- 没有幂等键、没有去重、没有序号:重发一段文本就是两条消息。`reqId` 只关联请求与结果,不落盘、不跨连接(`src/interconnect/index.ts:993-1022`)。

## 怎么接进 DSH

**① manifest 是 patch。** `package.json` 只有 `"dsh": { "bundle": { "patch": "./cordis.patch.yml" } }`(`package.json:28-32`),外加 4 个 `exports` 子路径(`package.json:8-27`);`dsh.plugin.json` 只是 9 行的重复声明,`entry.name` 指向 `dsh-interconnect/interconnect`、`inject: ["agents","credentials"]`(`dsh.plugin.json:5-8`)。真正被读的是 15 行的 `cordis.patch.yml`:三条 insert,id 分别是 `interconnect` / `tool-interconnect` / `skill-interconnect`,前者的 config 只写 `instanceId: dsh` 与 `requestTimeoutMs: 10000`(`cordis.patch.yml:4-15`)。

**② 三个插件各自注册一个面。**

| 插件 | 注册点 | 关键行 |
|---|---|---|
| `interconnect` | `class InterconnectService extends Service` → `ctx.interconnect`;`static inject = ['agents','credentials']`;`static Config` 6 个字段 | `src/interconnect/index.ts:365-373`、`src/interconnect/index.ts:400-401` |
| `tool-interconnect` | `inject: ['interconnect','tools']`,注册 **7** 个 `defineTool`:`interconnect_send/ping/list/peers/doctor/pair/reply` | `src/tool-interconnect/index.ts:25`;七个注册点在 `src/tool-interconnect/index.ts:98,209,247,321,381,468,558` |
| `skill-interconnect` | `inject: ['skills','interconnect']`;`ctx.skills.registerProvider(...)`,正文从 `assets/dsh-interconnect.md` 运行时读 | `src/skill-interconnect/index.ts:26,63-67` |

**③ 入站路由走宿主 webserver 的等待式 inject。** `ctx.inject(['webServer'], webCtx => webCtx.effect(() => webCtx.webServer.registerUpgrade(route)))`(`src/interconnect/index.ts:468-470`);path 是 `/interconnect/link`(`src/interconnect/index.ts:136`)。这样组合顺序不影响路由存在;没有 webserver 的 profile 只剩出站模式(`src/interconnect/index.ts:462-467`)。0.9 起**没有任何 HTTP 端点**,测试里也有一条断言「WS-only 时不注册 HTTP 前缀路由」(`tests/interconnect.host.spec.ts:419`)。

**④ 安装与配置。** `dsh plugin --profile <name> add dsh-interconnect`(或 `file:` 路径),`dsh plugin` 本身只是把剩余参数转给 pnpm(`dsh/lib/bin.js:115-122`)。profile patch 层按 `id` 覆盖时,**`config` 是整键替换而不是深合并**(`dsh-app-boot/lib/index.js:103-106`),未写的字段回落到 schema 默认值(`src/interconnect/index.ts:366-373`)——所以覆盖 `instanceId` 时必须把 `peers` 一起写上。

**⑤ 依赖与构建。** 13 个 peer 依赖(其中 `dsh-host-webserver` 可选,`package.json:47-66`),`ws` 是运行期 peer;esbuild 把 `@deepseek-ai/dsh-*`、cordis、`ws` 全部 external,类型另跑 `tsc`(`build.mjs:19-58`)。没有独立守护进程,也不需要单独开端口。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `src/interconnect/index.ts` | 1894 | 服务本体:升级鉴权、帧分发、投递、list/wake、pairing、诊断、`LinkState` | 结构见下 |
| `src/interconnect/types.ts` | 462 | 线上契约 + `Config` + 诊断类型 | `src/interconnect/types.ts:20,114,223,250,396-462` |
| `src/interconnect/pairing.ts` | 96 | pairing code 的 HMAC-SHA256 编解码 | `src/interconnect/pairing.ts:19,38-42,52-96` |
| `src/tool-interconnect/index.ts` | 649 | 7 个模型工具与渲染 | 见上表 |
| `src/skill-interconnect/index.ts` | 68 | 打包 skill provider | `src/skill-interconnect/index.ts:26,63-67` |
| `src/index.ts` | 13 | 包根 re-export(`.` 入口的类型与服务面) | 全文件 |
| `tests/interconnect.host.spec.ts` | 3172 | 149 个用例:链路、鉴权、投递、list 边界、pairing、self | — |
| `docs/interconnect-federation.md` | 635 | 跨域协议草案(未实现) | `docs/interconnect-federation.md:3,572-598` |
| `scripts/*` | 1169 | 发布/上游对齐/部署探针(仓库自带运维工具) | `scripts/check-upstream-alignment.mjs:1-20` |

**消息路径**(`send` 到投递完成):

```
A 的 agent ── interconnect_send ──▶ ctx.interconnect.send()            src/interconnect/index.ts:580-594
  └ msg 帧 {reqId, sessionId(B), text, sender{A, A-sess}, delivery?, resume?}   src/interconnect/index.ts:944-955
        ── WS /interconnect/link + Authorization: Bearer <token> ──▶ B 的升级处理器   src/interconnect/index.ts:1428-1461
              └ deliver(): agents.get(sessionId) 或 wake()          src/interconnect/index.ts:1321-1338
                    └ createUserMessage(source: plugin:dsh-interconnect, form: notice)  src/interconnect/index.ts:1365-1376
                          └ agent.followup | steer | inject          src/interconnect/index.ts:1382-1396
  ◀── msg-result {reqId, delivered, instance, delivery | reason} ──   src/interconnect/index.ts:1130
```

**事件路径**(单向,无回执):

```
A 的 6 个 Host 事件 ──ctx.on──▶ fanout() ──▶ broadcast()       src/interconnect/index.ts:507-540, 1066-1110
   broadcast 选一条 socket:有拨号链时跳过自报 id 被覆盖的入站 socket;hello 未到的窗口内会双发
        ── event 帧 ──▶ B ──▶ logger.info + ctx.parallel('interconnect/event')   src/interconnect/index.ts:1159-1174
```

逐个模块说清:

- **鉴权**。token 来自 credentials 的 `DSH_INTERCONNECT_TOKEN`(`src/interconnect/index.ts:93`、`src/interconnect/index.ts:1410-1413`);升级时先解析 token,未配置直接 403(`src/interconnect/index.ts:1441-1444`),读失败也 403(`src/interconnect/index.ts:1432-1439`);比较用 SHA-256 摘要后再 `timingSafeEqual`,把长度差也抹平(`src/interconnect/index.ts:1453-1458`、`src/interconnect/index.ts:1864-1866`)。出站把同一个 token 放进 `authorization` 头(`src/interconnect/index.ts:1752-1761`)。
- **握手**。只有 HTTP upgrade 的 bearer 校验加一帧 `hello`(双方 `attachSocket` 时立刻发,`src/interconnect/index.ts:1504`);收到 `hello` 记下对端自报 id(`src/interconnect/index.ts:1545-1554`)。没有 session id 交换,没有挑战-应答。
- **链路维护**。心跳 30 s、`pong` 续命、超时 `terminate`(`src/interconnect/index.ts:489-505`);拨号握手 10 s 上限(`src/interconnect/index.ts:134`、`src/interconnect/index.ts:1760`);断线重连指数退避 `min(30s, 1s·2^retry)`,无抖动(`src/interconnect/index.ts:1845-1855`);帧上限 1 MiB,双向 `maxPayload` 加显式长度检查(`src/interconnect/index.ts:128`、`src/interconnect/index.ts:381`、`src/interconnect/index.ts:1517-1520`)。
- **结果关联与超时**。每个请求建一条 pending,`requestTimeoutMs` 默认 10 s、schema 上限 60 s(`src/interconnect/index.ts:368`、`src/interconnect/index.ts:993-1022`);结果帧只按 `reqId` 认领,**不校验它来自哪条 socket**(`src/interconnect/index.ts:1563-1583`)。`ping`/`list` 的结果还要按请求 kind 过形状投影,形状不符按「无答复」处理(`src/interconnect/index.ts:970-990`)。
- **list 的双重上限**。只列 live agent、过滤 `origin === 'subagent'`(`src/interconnect/index.ts:1219-1220`),上限 100 行(`src/interconnect/index.ts:163`)与「帧上限减去应答信封」的字节预算(`src/interconnect/index.ts:1186-1193`);标题来自可选 projection,抛错只降级该行(`src/interconnect/index.ts:1248-1267`),装不下标题就先丢标题、再整行截断,保证结果是顺序前缀(`src/interconnect/index.ts:1226-1243`)。
- **唤醒**。不调 `ctx.agents.resume()`,而走 Host 的 `typert.lookups.get('agent')`(`src/interconnect/index.ts:1288`),理由是 `resume()` 的 handle 归调用方 context,插件 fiber 一卸载就把 session 拆了(`src/interconnect/index.ts:1269-1281` 的注释);`allowResume` 默认 true,拒绝时在 lookup 之前短路(`src/interconnect/index.ts:1284`);Host 的 `session/agent-busy` 映射成 `session-owned-by-subagent`(`src/interconnect/index.ts:1310-1312`)。
- **pairing**。code = `dshpair1.<base64url(JSON)>.<HMAC-SHA256>`(`src/interconnect/pairing.ts:38-42`),TTL 10 分钟(`src/interconnect/pairing.ts:19`),校验格式/签名/过期/`inReplyTo`(`src/interconnect/pairing.ts:52-96`);接受后 `addPeer` 写 sidecar,原子替换(tmp + rename,`src/interconnect/index.ts:904-923`),默认路径 `<profileDir>/interconnect-pairings.json`(`src/interconnect/index.ts:851-857`);静态 `peers` 同名时优先(`src/interconnect/index.ts:445-448`)。
- **诊断**。`diagnose()` 只读本地状态,返回 token 的 `configured|missing|error`(从不返回值)、webserver 端口、每个 peer 的 `fixed|self`、最后错误、重试次数与下次重试时间,再生成 `hints`(`src/interconnect/index.ts:672-724`);对应 `interconnect_doctor`(`src/tool-interconnect/index.ts:381-466`)。
- **卸载**。清心跳、断所有拨号状态与 socket、以 `unreachable` 结算所有 in-flight 请求,再置 `disposed` 挡住迟到的入站投递(`src/interconnect/index.ts:544-561`、`src/interconnect/index.ts:1321-1324`)。

**测试覆盖什么。** 208 个用例(`grep -h "  it(" tests/*.spec.ts | wc -l` = 208),大头在链路与投递:真实 WS 双向回环的 send/ping/list/reply、入站帧与畸形帧、鉴权边界(无 token、空 token、差一个字符、多字节头)、token 迟到后链路自愈、心跳清理、断线后重连调度、超时即 `unreachable`、list 的行数/字节双上限、subagent 封栏、self 路由的真 `--port 0` webserver 回环。**不覆盖**的正好是协议语义的三块:没有乱序用例、没有重复投递/幂等用例、没有版本不匹配用例(对 `tests/interconnect.host.spec.ts` 跑 `grep -nE 'order|twice|duplicate|concurren'` 只有 6 处命中,全是注释)。

## 为什么它突出

**星标归属没有陷阱:这是单包仓库,42 星就是插件的星。** 但曲线的形状比数字更有信息:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-13 | 仓库创建,当天 11 个提交(插件、MIT、README、bundle 化、CI) | `git log --reverse` |
| **2026-08-19** | **⚠ 34 星采样点(创建后第 6 天)** | registry 边车 |
| 2026-09-16 | 定位为「树外主源」;README 记录并入 monorepo 的 PR #3243 以「保持树外」关闭 | `README.md:6`、`RELEASING.md:3-7`(自述,私有仓不可核) |
| 2026-10-23 | `resume` 默认改为开(一次计费回合) | `CHANGELOG.md:169` |
| 2026-11-06 | 0.15.0 上 npm;0.16.0 的 `doctor` 与联邦协议草案同日落地 | npm registry、`CHANGELOG.md:43,76` |
| 2026-11-09 | 0.17.0(`pair`);npm 未发布 | `CHANGELOG.md:5`、npm `dist-tags` |
| **2026-11-18** | **实时 42 星(+8 / 91 天)、3 fork、0 watcher、4 个 issue(2 位外部作者)** | GitHub API |

34 星集中在创建后 6 天,之后 91 天只增 8——这是「发布周被看到」,不是「持续被采用」。npm 侧也能对上:42 个已发布版本、`latest` 停在 0.15.0,源码已经到 0.17.0,pair 与 doctor 没有进入任何安装路径。

**扩散为零,且是结构性零。** `grep -ril 'interconnect' data/plugins/` 只有它自己。四个理由,按解释力排序:

1. **使用场景要求「多实例」。** 同一台 DSH 上的多会话不需要它(subagent 在实例内解决);它解决的是「桌面 + 笔记本 + 服务器」或团队内多台机器。没有第二个实例,这条通道的价值为零——`self` 路由只是同实例两会话的补丁(`README.md:138-162`)。
2. **它是团队内部件,不是社区原语。** README 与 RELEASING 都写明:并入 DSH monorepo 的 PR 被关闭、仓库转为「树外主源」、团队内部插件集合仓以 git submodule 引用它(`README.md:6`、`RELEASING.md:3-7`)。这类仓库的维护目标是内部一致性,不是让别人复刻。注意这两条是**自述**,私有仓无法核对。
3. **没有可复用的规范面。** 线上格式只存在于 TypeScript 类型里(`src/interconnect/types.ts:250-356`),无版本字段、无 JSON Schema 文件、无客户端 SDK;跨域协议还是 `Draft 0.1、未实现`(`docs/interconnect-federation.md:3`),文中自己承认要新增 idempotency key 与三态应答(`docs/interconnect-federation.md:572-598`)。第三方要兼容,只能读 TS 源码。
4. **没有任何网络效应。** 一条链路的价值取决于对端也装;对端也装的前提是同一个 token 与一条可达 origin,跨机还要 SSH 隧道(`README.md:387-443`)。这是运维决定,不是插件决定。

**判断:机制上突出,生态上不突出。** 按本册两轴(声量 × 扩散),42 星 / 0 扩散都够不上锚;但它是 registry 里唯一被归到「会话到会话」的条目;机制上值得读的地方,是它怎么把跨进程消息压进 DSH 已有的 inbox 抽象,而不是它的采用量。

## 代价与边界

按发生顺序列失败模式:

1. **没配 token** → 入站 403,出站链路保持 down 并按退避无限重拨,模型拿到的只是 `unreachable`(`src/interconnect/index.ts:1441-1444`、`src/interconnect/index.ts:1737-1750`)。默认配置(无 token、无 peers)是**安全但不可用**:端点存在,一切请求被拒(`cordis.patch.yml:4-15`)。
2. **两端 token 不一致** → 401;两侧都显示 `down`,发送方只看到 `unreachable`(`src/interconnect/index.ts:1455-1458`;失败文案在 `unansweredText`,`src/tool-interconnect/index.ts:83-88`),要靠 `interconnect_doctor` 的 hints 才能定位到 token。
3. **对端离线** → `msgRequest` 见 `writable() === false` 直接返回 `undefined`,`send` 映射成 `unreachable`(`src/interconnect/index.ts:932-942`、`src/interconnect/index.ts:580-594`)。**没有队列、没有离线补投**:重试是调用方的事。
4. **超时** → 10 s 默认(上限 60 s)后 pending 被拒(`src/interconnect/index.ts:993-1002`),但此时 `msg` 可能已被对端投递。重试 = 可能重复投递;协议里没有幂等键,接收方也不去重。这是这套实现最实质的一致性缺口。
5. **重复事件** → 双向一对 socket 时,拨号链与入站链各发一次,`broadcast` 只跳过「已见过 hello 且 id 被拨号链覆盖」的入站 socket;hello 未到的窗口内必然双发(`src/interconnect/index.ts:1084-1088`、`src/interconnect/index.ts:1103-1109`)。peer 键与自报 id 不一致时该窗口永不关闭,每个事件都重复,只 warn 一次(`src/interconnect/index.ts:1548-1553`)。
6. **乱序** → 单条 socket 内 WebSocket 保序,两个方向各一条 socket;事件与消息是两条独立路径,没有序号或时间戳,所以「先收到 status 变化、后收到对应消息」是正常现象。跨发送方没有顺序概念。
7. **版本不匹配** → 帧里没有版本字段,也没有能力协商:新帧型会被联合 schema 拒绝,整帧丢弃并 warn `dropping malformed link frame`(`src/interconnect/index.ts:1531-1537`);既有帧里新增字段的去留取决于 schemastery,协议没有约定。表现是安静的 `unreachable` 或字段缺失,不是明确的「版本太旧」。
8. **帧超限** → 本地拒发并回 `message-too-large`,链路保持(`src/interconnect/index.ts:959-961`);入站超 1 MiB 直接丢(`src/interconnect/index.ts:1517-1520`)。
9. **上下文与日志成本** → 入站消息就是一条持久化的 user 消息,永久占该 session 的上下文;事件只写一行日志,不落 session 日志(`src/interconnect/index.ts:1161`),所以事件不会撑大日志。
10. **计费** → 两个工具的 `resume` 都默认 `true`(`src/tool-interconnect/index.ts:203,644`),服务端只有显式 `resume: true` 才唤醒(`src/interconnect/index.ts:1283`)——也就是说「对端模型一句话就能让你这台机器起一个带完整工具集的计费回合」,而接收方 `allowResume` 默认也是 true(`src/interconnect/index.ts:372`)。默认值把成本放在被投递方。
11. **安全边界**。默认只绑回环:DSH 的 webserver 默认 `127.0.0.1:3080`(`dsh-web-app/cordis.patch.yml:183-184`),且 schema 直接拒绝 `0.0.0.0` 之类通配绑定(`dsh-host-webserver/lib/index.js:252-259`);跨机按 README 走 SSH 隧道(`README.md:405-416`)。若显式绑具体网卡地址,upgrade 路由只按 pathname 分发、**DSH 自身的 GUI 认证不覆盖它**(`dsh-host-webserver/lib/index.js:432-455`),唯一的门是那把 bearer token;插件不终止 TLS,`wss` 只在宿主配了 `tls` 且 origin 写 `https://` 时才成立(`src/interconnect/index.ts:1880-1888`),且 `new WebSocket` 没有自定义 CA 选项(`src/interconnect/index.ts:1752-1761`),自签证书按 Node 默认策略会失败(判断)。
12. **一个 token 通吃整个 mesh**。没有 per-peer 密钥、没有 ACL、没有速率限制、没有审计:任何持 token 的对端可以列全部 live session、向任意 session 投递、唤醒持久 session(`src/interconnect/index.ts:1215-1245`、`src/interconnect/index.ts:1321-1408`)。`sender` 是自报字段,只用于 reply 归因,不构成鉴权(`src/interconnect/types.ts:22-37`)。pairing code 也用同一 token 做 HMAC,且接收方会去拨 code 里写的 origin(`src/interconnect/index.ts:794-804`)——把 code 交给你这边接受的对端,可以让本机去拨它指定的任意 `ws(s)://` 地址(判断,非漏洞主张)。
13. **分发缺口**。README 的 `dsh plugin add dsh-interconnect` 现在装到的是 **0.15.0**:没有 `pair`、没有 `doctor`(`CHANGELOG.md:5,43`、npm `dist-tags`)。要这两个工具只能 `file:` 装源码。
14. **维护成本**。3 182 行源码 + 4 211 行测试;两处 Host 内部逻辑是**手工镜像**(子代理归属判定 `src/interconnect/index.ts:64-78`、`assertNever`),Host 一改就得跟;CI 需要 checkout 并完整构建 `deepseek-harness`(`.github/workflows/ci.yml:15-51`)。

## 可信度与复现

★ ★ ★ 仅限本插件自身:服务、类型、pairing、工具、skill、测试清单逐文件读过;DSH 侧只对照了与本插件直接相关的四处(`dsh-host-webserver` 的 upgrade 与绑定约束、`dsh-web-app` 的默认 host/port、`dsh-app-boot` 的 patch 覆盖语义、`dsh-llm` 的 `createUserMessage`/`boundContextSummary`)。

正文里的 DSH 包路径相对 `$DSH/node_modules/@deepseek-ai/`;`dsh/lib/bin.js` 相对 `$DSH/`。

```sh
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh

# 1) 克隆与提交
git clone --depth 1 https://github.com/Chinesezjc/dsh-interconnect.git /tmp/an-interconnect
cd /tmp/an-interconnect && git log -1 --format='%H %ad %s'
# → 59f89789a6ccd23b63953d1092778ead3ea3a56d  Wed Nov 18 10:48:33 2026 +0800  Merge pull request #9 …

# 2) 规模
git fetch --unshallow -q && git rev-list --count HEAD          # 124
find src -name '*.ts' | sort | xargs wc -l                     # 3182 total
grep -h '  it(' tests/*.spec.ts | wc -l                        # 208

# 3) 扩散(在 awesome-dsh-plugin 仓库根)
grep -ril 'interconnect' data/plugins/ | wc -l                 # 1
grep -ril 'interconnect' data/plugins/                         # data/plugins/Chinesezjc__dsh-interconnect.yml
grep -ril 'chinesezjc' data/plugins/ | wc -l                   # 1

# 4) 元数据(2026-11-18 查)
curl -s https://api.github.com/repos/Chinesezjc/dsh-interconnect \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['created_at'],d['pushed_at'],d['stargazers_count'],d['forks_count'],d['size'])"
# → 2026-08-13T12:19:01Z 2026-11-18T02:48:33Z 42 3 677
curl -s https://registry.npmjs.org/dsh-interconnect | python3 -c "import json,sys;print(json.load(sys.stdin)['dist-tags'])"
# → {'latest': '0.15.0'}
```

**读过的文件**:`package.json`、`cordis.patch.yml`、`dsh.plugin.json`、`build.mjs`、`tsconfig.json`、`src/index.ts`、`src/interconnect/index.ts`(全文)、`src/interconnect/types.ts`(全文)、`src/interconnect/pairing.ts`(全文)、`src/tool-interconnect/index.ts`(全文)、`src/skill-interconnect/index.ts`、5 个 spec 的用例名与关键断言、`.github/workflows/ci.yml`、`README.md`(全文)、`CHANGELOG.md`(0.16–0.17 与 0.9 段)、`RELEASING.md`(前 40 行)、`docs/interconnect-federation.md`(头部 80 行、12–16 节)、`assets/dsh-interconnect.md`(前 50 行)。

**未读**:`docs/interconnect-federation.md` 的 5–11 节(传输/信封/签名细节)、`scripts/check-upstream-alignment.mjs` 与 `scripts/port-upstream-change.mjs` 的实现、`scripts/verify-deployment.*`、测试文件的绝大部分函数体(只读了 208 条用例名与少量断言行)、`pnpm-lock.yaml`。

## 待验证

1. **双机实测**:README 的 SSH 隧道流程(`README.md:387-455`)未实跑;`wss` 路径要宿主 webserver 配 `tls` 才能成立,`dsh web` 的 TLS 开关与自签证书下的握手未验证。
2. **wire 兼容性**:0.15.0(npm)与 0.17.0(源码)互通会怎样?帧里没有版本字段,理论上兼容帧可用,但 `senders`/`pair` 的行为差异没有测试矩阵。
3. **`interconnect/event` 的实际消费者**:本仓库零订阅;团队内部插件集合仓(不可见)是否订阅、订阅后做什么,无法从公开材料得知。
4. **PR #3243 与 submodule 引用**:只来自 README/RELEASING 自述,私有 monorepo 无法核对;公开仓库只有 5 个 PR、4 个 issue。
5. **并发投递顺序**:两个 peer 同时向同一 session 投 `followup`/`steer` 时的实际顺序与丢失概率——代码上由 Host inbox 决定,测试里没有对应用例。
6. **超时重试的重复率**:`msg` 已投递但 `msg-result` 丢失的窗口有多宽(默认 10 s),重复投递会不会被接收方 Host 合并——没有幂等键,也没有测量。
7. **42 星的构成**:2026-08-19 之后的 +8 落在哪几天;`stargazers` 的 `starred_at` 需鉴权,star-history 不可得。
