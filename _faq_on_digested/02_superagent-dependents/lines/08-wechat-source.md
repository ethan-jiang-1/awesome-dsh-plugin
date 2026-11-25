# dsh-superagent-wechat-source — 真写一个 `SourceKind`:入口插进去了,执行还是上游的

> `luckyxiang6688/dsh-superagent-wechat-source@486f817`(0★,MIT,`0.1.0`)。上游 `deepseek-ai/dsh-superagent-prototype@8c32a9dc`(24,565★)。注册表条目 [`luckyxiang6688__dsh-superagent-wechat-source.yml`](../../../data/plugins/luckyxiang6688__dsh-superagent-wechat-source.yml),类目 **remote**。证据等级 ★★★:读全 `src/`(15 个自有文件 / 1,491 行,另有 vendor 二维码 1,801 行)、10 个测试文件、`cordis.patch.yml`、README 与 NOTICE;上游 `src/sources/*` 全读;**没有**扫码绑定过真实微信号。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 / 类目 | luckyxiang6688/dsh-superagent-wechat-source / **remote** |
| 自述 | "把**个人微信私聊**接进 dsh-superagent 作为来源(Source)";面向"独立开发者自用:不需要组织账号、不需要企业微信/飞书"(`README:1-5`) |
| 声量 | 0★(2026-11-25 实时值) |
| 包形态 | 单个 DSH 插件,宿主侧 `lib/index.js` + 设置页 `lib/client.js`;`cordis.patch.yml` 只 `insert` 不写 config(`stateDir` 由用户在 profile 覆盖) |
| 宿主钉版 | `engines.dsh >=0.2.1-rc.0 <0.3.0`;Node `^22.19 \|\| >=24` |
| 运行时依赖 | **只有 `zod`**;不 import 任何 `@deepseek-ai/*`,契约在本地声明成结构镜像(`src/contract.ts:1-7`) |
| 注入 | `inject = ['orchestrator']`(`index.ts:16`)+ 条件 `webServer`(`index.ts:64-67`) |
| 规模 | `src/` 15 文件 / 1,491 行;10 个测试文件 / 825 行 |
| 契约面 | 实现 `kind/title/description/schema/fields/health/scope/channel/threadContext/policy`(`kind.ts:19-101`);**不实现** `rows/find/repliesTo/refreshLabels/environment/image` |
| 状态目录 | `<stateDir>/sources/wechat/{auth/token.json,sync-buf.json,messages.json,outbound.json}`,0600 原子写(`store.ts:32-41,60`) |
| 默认 `stateDir` | `~/.dsh-superagent-wechat`(`index.ts:34`)——**不继承** orchestrator 的 `stateDir`(与 [07](07-observability-trace.md) 相反) |
| 传输 | 微信 iLink / ClawBot:`https://ilinkai.weixin.qq.com`(`ilink/api.ts:11`),长轮询 + `get_updates_buf` 游标 |
| 限制 | 纯文本、一对一;10 条连发上限;24 小时主动消息窗口(`README:79-87`) |

## 影响力

- **0★ / 0 fork / 0 issue / 0 watcher**(GitHub API,2026-11-26 取);2026-11-09 建仓,最后一次 push **2026-11-13**(与 `0.1.0` 同日)。
- 注册表位置:[`data/plugins/luckyxiang6688__dsh-superagent-wechat-source.yml`](../../../data/plugins/luckyxiang6688__dsh-superagent-wechat-source.yml),类目 **remote**。
- npm **已发布**:`dsh-superagent-wechat-source@0.1.0`(另有 `0.0.0-stage`),包创建于 2026-11-13;近 30 天窗口下载 **712** 次(npm downloads API;包只发布了 11 天,含镜像/CI,**不等于安装数**)。
- 是否被其他 superagent 用户实际安装:**未见证据**。0 issue、0 fork、无第三方 README/issue 引用;唯一可核的是作者自述"传输、来源契约、登录、设置页、单测与实机端到端均已验证"(`README:7`)。
- **依赖面**:上游 `SourceKind` / `SourceRegistry` 一行未改,插件只调用 `register`(`上游 src/sources/registry.ts:20-39`);它是三条里唯一**既不搬上游代码、也不读 `orchestrator.sqlite`** 就能扩展上游能力的形态。
- 判断:**影响力 = 小**;但三条里它**分发路径最顺**:同名 npm 包 + 自带 patch 自动挂载,一条 `dsh plugin --profile superagent add` 即可(`README:22-25`),不需要 clone。
- 需要打折的地方:下载数不能区分"装上了"与"只是下载了";而它的前置条件(白名单 + 上游 GitHub 仓库)比 07/09 都长,放弃点更多。

## 一、要解决什么问题:上游只有两个 Source,且都面向"组织"

上游的 Source 只有 GitHub 与飞书(`上游 docs/001-domain.md:68`):一个要仓库 + `gh` 登录,一个要企业自建应用与 `lark-cli`。对独立开发者,这两条都先要求"你有一家公司"。而"在微信里随口说一句要做什么"是最低摩擦的入口,上游没有、也不打算有(它把 Source 实现明确列为**部署面**,`docs/001-domain.md:64`)。

更具体地,上游缺的不是"一个渠道抽象"——`SourceKind` 就是为这个准备的——而是两样东西:

1. **一条不需要公网回调的传输**。个人微信没有 webhook,只能主动长轮询;上游只提供 `receive(trigger)`(`上游 src/sources/host.ts:41-42`),取事件的那一段完全由 Source 自己负责。
2. **一种"私聊即点名"的授权语义**。上游的准入默认"未点名 = 候选/忽略"(`ADMISSION_DEFAULTS`,`上游 src/admission.ts:12-13`),而私聊天然指向机器人本身;插件把它翻成 `addressed: 'direct'`(`trigger.ts:56`),才让"名单内的人私聊"落进 `explicit`(`上游 src/policy.ts:197`)。

所以问题被切成两半:**入口(微信私聊 → Trigger)是插件补的;接单、建单、执行、回帖仍是上游的**。

## 二、路径:实现契约,而不是搬代码

三条被放弃的路:

- **整树分叉**:上游 92 个源文件、`private: true`、无 npm 包;为加一个渠道扛整树,是把"加渠道"变成"跟上游"(见 [answer.md](../answer.md) 的"他们到底利用了哪一面"一节)。
- **改用飞书/企业微信**:需要组织主体,与"自用"目标相反(`README:5`)。
- **做成聊天客户端**:`dsh-wechat` 已经做了实时对话,定位不同(`README:13`);而且**一个微信号只能连一个 bot 客户端**(`README:70-77`),两个都装就是互相抢绑定。

它选的是第四条:**只实现 `SourceKind`,把 iLink 客户端当作 Source 自己的"读位置 + 身份"**。这与上游对 Source 的定义正好对齐——"Holds its read position and its own bot identity"(`上游 docs/001-domain.md:27`)。

代价是它必须自己承担三件上游不管的事:扫码登录(PIN/过期/重定向状态机)、长轮询与游标、回帖的 `context_token` 与配额。这三件事的代码占了近四成(`login.ts` 180 行、`account.ts` 241 行、`ilink/api.ts` 189 行)。

## 三、它如何利用 dsh-superagent(逐点对位)

| 契约成员 | 上游声明 | 本仓实现 |
|----------|----------|----------|
| 注册 kind | `SourceRegistry.register` 返回注销器,重名直接抛(`src/sources/registry.ts:20-39`) | `ctx.effect(() => orchestrator.sources.register(wechatKind))`(`index.ts:56`) |
| 健康条目 | `health: string[]` 由注册表 claim;`report` 只接受本 kind 声明过的名字,否则抛(`source-context.ts:67-70`) | `health: ['wechat']`(`kind.ts:35`)+ `report('wechat', …)`(`index.ts:50`) |
| 收事件 | `SourceContext.receive(trigger)`(`host.ts:41-42`) | `ctx.orchestrator.context(source).receive(trigger)`(`index.ts:48`),在轮询循环里调用(`account.ts:238`) |
| 监听范围 | `scope(input, config) → ScopeResult`(`src/sources/kind.ts:98`) | 恒 `{listened:true, observed:false, row:'direct'}`(`kind.ts:42-44`) |
| 策略 | `policy.schema/fields/explicit/unnamed`(`kind.ts:28-41`),`allowed` 被 `allowedSender` 读取(`上游 src/policy.ts:119-121`) | `allowed` 默认 `[]`、去重校验(`kind.ts:81-101`) |
| 回帖通道 | `channel.allowed/send/link`;`send` 必须按 id 幂等,`'gone'` 表示永远送不到(`kind.ts:46-56`) | `allowed` 只查地址有 `user`(`kind.ts:47`);`send` 落 `account.sendText`(`kind.ts:48-53`) |
| 线程上下文 | `threadContext.messageId/read/images`(`kind.ts:65-75`) | 分页读本地环形,`root/parent` 直接回 `no_root/no_parent`(`kind.ts:61-79`) |
| 设置页 | 宿主按 `fields` 生成 Source 配置卡 | 插件另有自己的设置页 section + 5 条路由(`routes.ts:41-…`) |
| 未用到的能力 | `context.state/threads/tickets/notify/config`(`host.ts:43-63`) | 全部不用:游标与消息环走自家文件(`store.ts`),不写 `kv` |

`Trigger` 的形状也是本地镜像(`contract.ts:30-41`),实际值在 `trigger.ts:50-66`:

- `id`:`wechat:<from_user_id>:<messageKey>`,messageKey 依次取 `message_id → client_id → seq → create_time_ms-seq`(`trigger.ts:24-30,51`)——**稳定 id 是上游幂等的前提**("Accepting a Trigger twice creates one Ticket",`docs/001-domain.md:28`);
- `threads`:`wechat:<user>`,一条私聊一条线程(`trigger.ts:14,53`);
- `addressed: 'direct'`、`channel.address = { user }`(`trigger.ts:56-59`);
- 群消息、机器人自己、无发送者、纯媒体一律在进域前丢掉(`trigger.ts:37-43`)。

## 四、技术思考

### 4.1 Source 契约:哪一段真可插拔,哪一段不是

**可插拔的是"声明"**:kind、配置 schema、字段、策略片段、渠道适配器、上下文读取器。上游据此生成设置卡、策略卡、回复通道、评估上下文,并让 `SourceRegistry` 把 kind 的 health 条目 claim 掉(`registry.ts:20-39`);换渠道不需要改 Router,这与上游文档一致。

**不可插拔的是三段**:

1. **取事件**。长轮询、退避、`-14` 会话失效后暂停一小时、游标持久化,全在插件里(`account.ts:179-220`)。上游只在 `receive` 那一端接住。
2. **装配方式**。插件不是被 superagent 加载的,而是同 profile 的兄弟插件,硬 `inject: ['orchestrator']`(`index.ts:16`)。所以"没装插件"在上游看来是**来源未安装**,`scope` 直接返回 `source_not_installed`(`registry.ts:124-131`),而不是启动报错。
3. **读位置的归属**。契约要求 Source 自己持有读位置(`docs/001-domain.md:27`),但 API 层面只有 `context.state` 这个 KV(`host.ts:44-45`)。本插件绕开它,把游标写进 `sync-buf.json`(`store.ts:86-92`)——契约允许,但副作用是**只有插件自己知道读到哪了**:trace 之类只读 `orchestrator.sqlite` 的工具看不到微信游标。

### 4.2 两套配置平面,以及"到底碰不碰 stateDir"

| 平面 | 存在哪 | 谁读 | 例子 |
|------|--------|------|------|
| 插件级 config | profile 的 `cordis.patch.yml` | 插件 `apply(ctx, config)`(`index.ts:42-47`) | `stateDir`、`historyLimit`(本地环形大小) |
| Source 实例 config | superagent 的 settings(`orchestrator.sqlite` 的 `settings-version:*`) | 上游 `kind.schema.parse` 后作为参数传给 `scope/channel/threadContext`(`registry.ts:134-138,109-119`) | `historyLimit`、`readPageSize`(评估能回看多远) |

两张表里都有 `historyLimit`,**不是同一个数**:本地环形按插件级取值截断(`index.ts:47`),评估读的时候按实例级取值再切一页(`kind.ts:68`)。默认都是 200,所以平时看不出来;在 superagent 面板里把它调到 1000 并不会让本地留下更多消息,只会让评估"想要更多"却拿不到——静默,不报错。

**它不读 orchestrator 的 `stateDir`**:默认落在 `~/.dsh-superagent-wechat`(`index.ts:34`)。如果用户按 README 把它指到 superagent 的 state 目录,写入点是 `<stateDir>/sources/wechat/`(`store.ts:60`),与 `orchestrator.sqlite` 并列。上游对该目录持有一把 proper-lockfile 锁(`上游 src/app/runtime.ts:93`),插件只动自己的子目录,因此能共存;但备份、权限、清理的边界从此混在一起。

还有一处**只能靠人**的边界:白名单住在 superagent 的策略里(`policy.ts:119-121`),插件没有写策略的 API;设置页只把 `ilink_user_id` 显示出来,让用户复制到 superagent 的策略卡(`README:46-49`)。

### 4.3 失败时的表现

- **游标先走一步**。`saveCursor()` 在 `for (…msgs) ingest()` **之前**(`account.ts:205-206`),而 `ingest` 调 `receive` 不 await(`account.ts:238`)。上游明确要求"推进游标前先 await receive"(`上游 host.ts:41-42`);这里崩溃窗口内的消息只会靠 Trigger id 幂等在上游侧去重,不会被重放。这是本插件最实的一处契约松动。
- **回帖失败就抛**。未登录、缺 `context_token`、超出 10 连发都会抛(`account.ts:144-152`);上游 Outbox 按 5s 起、翻倍到 300s 重试(`docs/003-execution.md:177-183`)。插件从不返回 `'gone'`,所以一个永久打不通的会话会一直重试并计为 system problem,而不是被丢弃。
- **轮询失败**:5s→60s 退避并 `report('error')`;`-14` 视为服务端会话失效,暂停一小时再重连(`account.ts:191-197,208-215`)。
- **登录**:扫码状态机 5 分钟超时、最多 3 次刷新,PIN 在设置页输入(`login.ts:30-31,64-80`)。
- **白名单为空 = 谁都不能建单**:上游 gate 对未列名者给 `not_a_member`,整批都不可准入时直接记 ignore、根本不发起 Eval(`上游 policy.ts:193-210`,`src/core/evals.ts:96-106`),所以不会花模型调用。这是 fail-closed,方向正确。
- **设置页 API** 要求 `x-agent-wechat-request: 1` 且 `Origin` 与 `Host` 一致(`routes.ts:10-17`),body 上限 4 KB(`routes.ts:26-39`)。

## 界面体验

- **入口**:**设置 → 微信任务**(`client/index.tsx:14-17`;`settings.section`、id `agent-wechat`、order 41)。只有这一个入口,没有侧栏页、没有会话页。
- **未登录**:一张卡——标题"微信私聊 · superagent 来源" + 状态徽章,下面是 220×220 的二维码 SVG(`client/Settings.tsx:65,141`);出现数字校验时给输入框 + "提交"(`:145-150`);过期/出错/已绑他处 → "重新获取二维码"(`:155`)。
- **已登录**:显示机器人 ID、扫码用户 ID(旁边直接写"填到策略的 allowed 里")、长轮询在跑还是停了、最近一次轮询时间,以及"重新登录/退出登录"(`Settings.tsx:164-172`)。
- **冲突提示**:检测到本机 `dsh-wechat` 已登录时红字提示"一个微信号只能连一个 bot 客户端,请二选一"(`Settings.tsx:128-134`)。
- **第二张卡是"怎么用"五条**:扫码位置、直接发消息、回执+结果两步、上游 GitHub 前置、10 条连发上限(`Settings.tsx:181-190`)——扫码入口、GitHub 前置与 10 条上限这三处最容易踩的坑都写在界面上。
- **信息密度**:低。一个设置页承载"绑定 + 状态 + 用法",没有事件流、没有工单列表;真正的执行细节要去 superagent 面板或 [07](07-observability-trace.md) 看。
- **失败时看到什么**:八种登录相位各有中文文案(`Settings.tsx:41-50`);登录错误显示 `qr.error`;轮询错误显示在已登录卡的 `status.error`;而未登录时每 2 秒、已登录每 5 秒刷新一次(`Settings.tsx:86`)——三条里 07 不轮询、09 轮询进程状态,只有它为**登录状态**在登录前就开轮询。
- **回帖失败看不到**:那属于上游 Outbox 的 system problem,显示在 superagent 面板,不在这个设置页。

## 用户交互的思路

- **谁发起**:用户在**微信里**发一条私聊。入口不在 DSH——这是它与 07/09 最根本的差别:DSH 只负责"把机器人绑上",之后人一直在微信里。
- **在哪确认**:两处。绑定在设置页确认(扫码 + 可能的数字校验);"这条算不算工作"由上游主控裁定,**用户看不到裁定过程**,只能从"有没有回执"推断(`README:57-58`)。
- **怎么观察**:接单确认 + 最终结果两条消息回到同一对话,不做逐段流式(`README:62`);中间过程要看 superagent 面板。
- **怎么打断**:没有逐条取消。只能关掉这个来源或暂停编排(`README:64`),或者干脆不再发消息;已建的单仍在跑。
- **沉默的失败**:回帖失败由上游 Outbox 退避重试(`docs/003-execution.md:177-183`),用户在微信里只感到"迟迟没有回执";插件无法告诉用户"消息收到了但排不上"——这条回路里没有"已读"这一档。
- **需要人拍板时**:上游由主控用 `orchestrator_reply` 的 `purpose: 'attention'` 把提问发回原对话(`上游 src/app/tools/main.ts:224-230`),在微信里就是一条普通消息;用户回一条私聊,即成为该线程的新 Trigger(`上游 docs/001-domain.md:37` 的 Subscription/fan-out 路径)。
- **与上游回路的差异**:上游默认"渠道是 IM 的一个适配器",本页把**整个入口**搬到 IM——发起、回执、结果、追问都在微信闭环,DSH 只剩设置页。代价是上游的确认粒度(准入表、Mandate、提问 Attention)在这里全部退化成"发不发这条私聊"。

## 五、代价与边界

1. **微信号独占**。一个微信号只能绑一个 bot 客户端,而目前没有自助解绑入口;残留绑定可能弄挂已有的 `dsh-wechat`(`README:70-77`)。插件会检测 `~/.dsh-wechat/auth/token.json` 并提示(`account.ts:33-41`),但只是提示。
2. **只解决了入口,没解决执行**。上游 `Setup.resolve` 无条件解析 GitHub 部署,`resolveDeployment` 在没配仓库时直接抛 `repositoryUnset`(`上游 src/deployment.ts:87-91`,`setup.ts:76-78`)。所以"没有组织账号也能用"只对**收消息**成立;要真的建单跑活,仍需一个可推送的仓库与 `gh` 登录(`README:17`)。
3. **接单模式管不了私聊**。私聊 + 名单内 = `addressed` 命中,直接 `explicit`(`上游 policy.ts:197`),根本不进准入表;`off/observe/auto` 对它无效(`README:83`)。想静音只能关来源或暂停编排。
4. **契约漂移没有编译期保护**。`contract.ts` 是手写镜像(`contract.ts:1-7`),测试用假 orchestrator(`tests/plugin.test.ts:37-44`)。上游给 `SourceChannel.send` 加参数、或改 `receive` 的返回类型,插件照旧编译通过,运行时才失效。
5. **`row: 'direct'` 是个没有表的行**。上游 `admissionOf` 取不到该行就落到默认值(`上游 policy.ts:138-140`),所以这个字段现在只是标注;若上游将来按 `row` 严格校验,它会变成错误来源。
6. **两套 `historyLimit` 会漂移**(见 4.2),且漂移是静默的。
7. **能力面窄**:纯文本、一对一、无媒体、无引用、无群聊(`README:81`);`threadContext.images` 恒空(`kind.ts:78`)。
8. **协议与合规风险**:iLink 是腾讯官方通道,但本项目是独立第三方客户端,协议随官方升级可能变(`README:87,121-123`)。

## 可信度与复现

- **读过**:`README.md`、`NOTICE.md`、`package.json`、`cordis.patch.yml`、`src/` 全部 15 个自有文件 + vendor 头、10 个测试文件;上游 `docs/001-domain.md`、`src/sources/kind.ts`、`src/sources/registry.ts`、`src/sources/host.ts`、`src/app/source-context.ts`、`src/policy.ts`、`src/deployment.ts`、`src/app/setup.ts`。
- **对位比过**:契约的每个成员逐个对到上游声明与插件实现;`policy.allowed` 在 gate 中的用法逐行读过。
- **没做**:扫码绑定真实微信号;实机走一遍"私聊→裁定→建单→回帖";iLink 协议字段与官方文档逐条核对。
- **复现**:
  ```sh
  git clone https://github.com/luckyxiang6688/dsh-superagent-wechat-source && cd dsh-superagent-wechat-source
  git checkout 486f817
  grep -rn "inject\|sources.register\|context(source)" src/index.ts
  grep -rn "allowed\|addressed" src/kind.ts src/trigger.ts
  ```

## 待验证

1. **`receive` 不 await 的真实后果**:`ingest` 里是 `try { receive(trigger) } catch`(`account.ts:238`),若上游 `receive` 返回 Promise 且在微任务里失败,这里的 catch 抓不到;丢消息概率取决于 `get_updates_buf` 的服务端语义。
2. **`source_not_installed` 的表现**:禁用/卸载插件后,库里已有的 `wechat` 事件与线程在上游面板如何显示,未实测。
3. **与 `dsh-wechat` 同时安装**:除绑定冲突外,两者的设置页 section、HTTP 前缀、本地目录是否真的互不干扰(`README:72` 自述,未验证)。
4. **10 连发与 24 小时窗口的边界**:`outbound.count` 只按"连续 bot 消息"计,入站清零(`store.ts:25-30,108-113`);分片发送时 `chunks.length` 计入同一配额(`account.ts:151`),切分策略与配额的关系未测。
5. **上游若把 `addressed` 语义收紧**(例如要求 `'direct'` 只能来自私聊类型),当前 `message_type === 1` 的判定是否仍成立。
