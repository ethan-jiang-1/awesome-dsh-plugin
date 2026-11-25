# 06 · NelsonLongXiang/dsh-open-a2a-net — 只 vendor 2,088 行内核,把 A2A 网络套在外面

> `NelsonLongXiang/dsh-open-a2a-net@4151721`(2026-11-25 15:51 +0100;10★),包 `@nelsonlongxiang/dsh-open-a2a-net@0.8.1`。上游 `deepseek-ai/dsh-superagent-prototype@8c32a9dc`。证据等级 ★★★:读了 `THIRD_PARTY_NOTICES.md`、`src/superagent/` 的完整目录与主要文件、`cordis.patch.yml`、`docs/design/{114-task-authorization,assignment-card-lifecycle,superagent-a2a-spec,superagent-a2a-watch}.md`,并把 vendored 目录与上游逐个 `cmp`;**没有**在真实 A2A 节点上跑,没有跑它的 366 个 spec。

## 一屏事实

| 项 | 值 |
|----|-----|
| 自述 | "Open A2A network plugin for DeepSeek Harness: signed agent cards, decentralized peer/zone discovery, direct routing model tools, joinable session nodes"(`package.json:4`) |
| 声量 / 规模 | **10★**;HEAD `4151721`(2026-11-25);0.8.1、MIT;`src/` **173 个 TS/TSX / 43,960 行**,**366 个 spec**;`verify:core` 串起 9 道门禁(含 doc-drift、布局、架构锚点、变异测试) |
| superagent 子系统 | **52 个文件 / 13,723 行**(不含 vendored);是内核行数的 **6.6 倍** |
| vendor 了什么 | 上游 `src/core/` **15 个文件 / 2,088 行**,加**上游自己的 2 个测试**(1,682 行),落 `src/superagent/upstream/dsh-superagent/` |
| 没 vendor 什么 | 上游的 `app/`、`sources/`、`client/`、`executor/`、`infra/`、`policy.ts`、`admission.ts` —— 即上游 110 个 TS/TSX 里剩下的 95 个 |
| 是否原文 | `THIRD_PARTY_NOTICES.md:6` 自述 "vendored unchanged";我 `cmp` 了 **15/15 个 core 文件与 2/2 个测试,全部逐字节相同** |
| 锁定方式 | `UPSTREAM.json` 记 `8c32a9dc5d72c033816c6a8110b37f40cf94fba4` + **每个文件一条 sha256**;`scripts/superagent-upstream.mjs`(88 行)在单测里跑 |
| 依赖 | 只有 peer(`@deepseek-ai/* ≥0.1.7-alpha.2`),**运行时依赖为 0**;不依赖 `dsh-superagent` 包(上游 `private`,也没有包可依赖) |

## 影响力

| 项 | 数字 / 事实 |
|----|-------------|
| GitHub | **10★ / 3 forks / 10 watchers / 38 open issues**;created 2026-08-19,pushed_at **2026-11-25T16:58:52Z**;`fork: false`;topics `a2a, a2a-protocol, agent-network, deepseek-harness, dsh-plugin, p2p` |
| npm | **已发布且持续发版**:`latest = 0.8.2`、`preview = 0.8.1-preview.29`,可见版本自 0.5.13 起;maintainer `yuanguang`,homepage 直接指向 npm 包页 |
| 注册表 | `data/plugins/NelsonLongXiang__dsh-open-a2a-net.yml`,类目 **remote**(13,136 条里 365 条),条目描述自己写"0.8 预览版" |

10★/3 fork 是**小**;它也不是"机构背书"——上游 `deepseek-ai` 的 2.4 万★(实时 24,570)与它无关,它是一条独立开发的网络协议实现。38 个 open issue 至少说明它在被持续开发(是否全为作者自己的记录,未核)。
被谁用:注册表里 `NelsonLongXiang` 只出现 2 次,都是同一作者的仓;`a2a-net` 这个 CLI 名没有被任何第三方条目引用。**未见**第三方依赖它的 vendor 目录或 superagent host;3 个 fork 的内容未核。
判断:真正有影响的地方只有一处——它是这批依赖里**唯一把上游领域引擎当库用、且把"不变"做成可校验不变量**的样本。影响在方法,不在采用。

## 一、它要解决什么问题:上游有五个假设,在 A2A 网络里全不成立

| 上游假设 | 上游锚点 | A2A 网络里的事实 |
|----------|----------|------------------|
| **单进程单节点**:主 Session 与 `worker-<id>` 都在同一个 DSH 实例里 | `docs/001-domain.md:41`(Executor 在域外,靠 Assignment 连接) | 要从**别的宿主机**上接活;节点身份、准入、投递、回执、账本都得在域外解决 |
| **发起者是人** | `docs/002-authorization.md:11-16`(名单内的人 @ 机器人 = explicit) | A2A 调用方是 agent,上游按 `human: false` 处理,只能走 Policy 的 bot 名单,永远拿不到 explicit 强度(`superagent-a2a-watch.md:28`) |
| **一单一会话一目录** | `docs/001-domain.md:98`,上游 `executor/dsh.ts` | 属主明令**不许再开新会话**(设计里的 S39),执行器必须是"固定成员池"(`host/executor.ts:1-18`) |
| **setup 必须先绑一个 GitHub 仓 + agent 账号** | 上游 `app/setup.ts:77-79` 无条件 `resolveDeployment`、`deployment.ts:87-105` | A2A 接活与 GitHub 无关;影子阶段只能在**未完成 setup** 的实例上读信(`superagent-a2a-watch.md:44-56` 有实测记录) |
| **代码可以整树搬** | 上游 `private: true`、无 npm、无版本化 API | 搬得动,但跟不动;而它要跟的是一个每周都在变的网络协议实现 |

真正的痛点写在 `114-task-authorization.md:19-22`:**谁发来一句 `[A2A receipt] task <id> …`,谁就能结算 `<id>`**。入站不记"凭什么接下这条任务",出站不记"是谁发的",结算不问"是谁结的"——在一个多主机、互不信任的网络里,这是授权模型的空洞,不是 bug。

## 二、它的路径:先做外挂 Source,再把内核搬进宿主

它走了两步,两步的产物今天**同时存在**:

1. **p2(外挂)**:`src/superagent/a2a-watch.ts`(707 行)是一个**给上游 superagent 写的 Source 插件**,读一个专用 A2A CLI 身份的信箱,把每条消息翻成 Trigger。启用方式是往上游的 `cordis.patch.yml` 插一行(`superagent-a2a-watch.md:12-22`)。这一代不改上游一行代码。
2. **v4(内嵌)**:`src/superagent/host/`(52 个文件)把 vendored 内核**在自己的进程里组装起来**,自己实现上游的六个端口;而 p2 的 `a2a-watch` **原样复用**——`host/a2a-source.ts:1-16` 明确写:"#402 的 a2a-watch runs unchanged;这个文件是它期待的上游 `SourceHost`/`SourceContext`,在 a2a 宿主上实现"。

放弃了三条替代路,而放弃的理由是**在文档里明写的**:

| 放弃 | 理由 | 锚点 |
|------|------|------|
| fork 整个 superagent | 属主 2026-11-06 裁定:"做成独立导出的插件包(`a2a-watch`),**不 fork superagent**" | `superagent-a2a-spec.md:181-186` |
| 把上游 `app/` 一起 vendor | "上游的 store、views、panel 与它自己的 app(sources、migrations、settings)缠在一起",所以只 vendor 纯内核,其余按端口自己实现 | vendored `README.md:15` |
| 用 A2A 把工单派给远端席位(原" A2A Executor") | S38 收窄:superagent 用**本地**执行器干活,A2A 外发只剩回执、送审、上报三种 | `superagent-a2a-spec.md:161-171` |

## 三、它如何利用 `dsh-superagent`:三层复用,一层比一层薄

### 第 1 层:领域引擎,逐字节

vendored 的 15 个文件就是上游 `src/core/`:engine、evals、tickets、assignments、intake、model、ports、replies、reasons、stage、part、memory、errors、ids、index。`UPSTREAM.json` 给每个文件记一条 sha256,`scripts/superagent-upstream.mjs:70-87` 做三件事:

- 目录里出现清单与 `README.md` 之外的文件 → 失败;
- 任何文件 sha256 与清单不符(即被改过)→ 失败,报 "edited (sha256 differs from upstream …)";
- 引擎里出现**离开自身的 import** → 失败。白名单只有 `node:crypto` 与 `vitest`(`:28-29,78-86`)。

所以"unchanged"不是一句声明,是一条**会挂测试的不变量**。上游的 2 个测试也一并搬来跑(`tests/core-engine.spec.ts` 1,621 行、`tests/stage.spec.ts` 61 行),"它们是 vendored 引擎行为与上游一致的证据"(vendored `README.md:6`)。

### 第 2 层:端口,自己实现

`host/index.ts:1-14` 把这层说清楚了:引擎拥有领域(Trigger/Thread/Eval/Decision/Ticket+Mandate/Assignment/Subscription/Reply),宿主实现它的端口——

| 上游端口 | a2a 的实现 | 锚点 |
|----------|-----------|------|
| `Repositories` | `<a2a home>/superagent/` 下的 JSON 仓储 | `host/store.ts`(135 行) |
| `Policy` / `SourceScope` | 属主的团队设置 → `teamPolicy` / `teamScope` | `host/policy.ts`(665 行) |
| `Assessor` | 上游的"主 Session"位置换成一个本地 router 会话,候选以**卡片**送进去,只能通过 `superagent_route` 之类的工具决策,不许自由文本 | `host/index.ts:8-9`,`host/cards.ts` |
| `Executor` | **固定成员池**:一个成员一个槽,没有空槽就排队;交接/阻塞会 parking 并接下一单;绑定持久化在 `<a2a home>/superagent/executor.json` | `host/executor.ts:1-18` |
| `Outbox` | workbench 的回复存在 Thread 上;其余 Channel 走各 kind 自己的 channel | `host/index.ts:10-11` |
| `SourceHost`/`SourceContext` | 把 p2 的 `a2a-watch` 原样装进来;`commands` 直接跑**真的** `a2a-net` CLI,复用它的 JSON 契约而不是在进程内重写 | `host/a2a-source.ts:1-16` |

### 第 3 层:插件 API 的类型快照(与设计语汇)

`src/superagent/upstream/snapshot-8c32a9d.ts`(254 行)逐字摘录了 `SourceKind`、`SourceHost`、`SourceContext`、`Trigger`、`ChannelRef` 等结构,并**声明了三处刻意的偏离**(类型外置成 `Opaque`、`z.ZodType<T>` 换成 `SchemaLike`、未用成员省略;`:31-39`)。`contract.ts`(38 行)用类型断言把两侧钉死:`KindIsUpstream`、`HostFromUpstream`、`ContextFromUpstream`、`TriggerSame`、`TicketOutcomeSame`……编译不过就是契约破了。

**为什么需要第 3 层**:vendor 的 `core/` 里**没有** `SourceKind`(它在 `src/sources/kind.ts`)。所以它有两把锁:内核用 sha256 锁字节,插件 API 用快照+类型断言锁形状。

不复用代码、只复用**语汇**的地方也有一处:`114-task-authorization.md` 开头写"参照:`dsh-superagent-prototype docs/002-authorization.md`(Mandate / Policy version / observe)"(`:10-11`);第 5 节把上游的策略变更语义搬过来——"Policy 版本变化时只通知受影响的在跑工单、**不直接撤销**;撤销只在恢复前重新校验时发生"(`:380`)——但自己只做前半段:**只记录受影响任务清单,不取消任何任务**(`:405-406`)。

## 四、技术思考

### 1. 为什么只 vendor 内核:因为内核是纯的

判断标准不是"重要不重要",而是"**能不能在不改一个字节的前提下复用**"。上游 `src/core/` 满足:除了 `ids.ts` 里的 `node:crypto`,它不 import 任何外部东西(其余 import 都是同目录的 `./model.ts` 之类)。所以它可以被复制、被哈希锁定、被上游自己的测试验证。反过来,`app/`、`sources/`、`client/` 里全是 Cordis 上下文、DSH 服务与 settings 形状——搬过来就等于整树分叉,也就等于放弃"跟着上游走"的可能。这条边界划得很干净:**纯的搬,脏的按端口重写**。

### 2. A2A 的签名节点与 Ticket 授权,是两层正交的授权

它没有把两套授权缝成一套,而是明确分工:

| 层 | 回答什么问题 | 载体 | 锚点 |
|----|--------------|------|------|
| **Ticket / Mandate**(上游) | 谁**可以让这个智能体干活**,能干到哪 | `Mandate`(不可变、记 policyVersion/scope/strength/actor) | 上游 `docs/001-domain.md:34` |
| **任务授权记录**(a2a) | 谁**可以结算这条任务** | 入站行出生时冻结的 `auth`;结算时比对 `chain_role` | `114:130-158,292-300` |

a2a 那层的样子:`auth = { caller, proof, ingress, via, admission_rule, basis, allowlist_version, target, receipt_target, received_at }`,**出生即冻结**,台账不提供任何修改它的方法,归档原样复制,重放无法覆盖(`114:230-241`)。`allowlist_version = "al1:" + sha256(canonicalJSON(inputs)).slice(0,16)`,输入只取"本机运营者可控、且准入代码真读到"的记录(zone/scope/joined/roster/canvas/cli/links),故意**不含**名片缓存里的 `canvasOrg` 和在线节点集合——理由是它们随缓存冷热与节点上下线抖动(§2.3)。结算资格是一张封闭表:`target`、`target-member`、`host-face`、`legacy`,其余一律 `off-chain`(`§4.2`)。

签名节点在另一侧:`card.ts:1-16` 是"带过期时间的签名名片"(Ed25519 签身份/团队/能力/过期,GNUnet HELLO 语义,TTL 2 天);`OriginClaim` 证明的是**密钥持有**,不是人的同意——这条被写进 router 的人格文本里当禁令:"A CLI signature proves an agent key, not human consent"(`cordis.patch.yml:56`)。

### 3. 一个真实事故决定了这套设计

`#61`(`direct-bb27ec94`)的复盘很具体:目标会话当时在做另一条工作线,`flushFinals` 把**那条线的 final 文本**当成了这条任务的答复,宿主于是发出一张内容无关的 `completed (auto)` 回执;事后无法回答"这条结算凭的是什么授权"(`114:106-122`)。设计的解法因此是**两道**而不是一道:授权链拦"别人替你结",turn 归属拦"宿主替你结、但拿错了 turn"——归属锚点改成"steer 被消费的那条 `user/message` 事件之后的第一条 final",而不是"投递时目标忙不忙"(`114:320-340`)。只看身份是拦不住这一例的,因为结算方恰是目标所在主机的进程面。

### 4. 状态与隔离:引擎不碰 IO,一切状态都归宿主

引擎是纯计算,持久化全在 `Repositories` 端口后面(`host/store.ts`),绑定在 `executor.json`,`auth` 与账本在 a2a 自己的 `tasks.json`。这条边界的实际好处是**测试可以完全离线**:引擎带着上游 1,682 行测试,宿主端口可以被替换(`host/deps.ts:29-40` 把 home、`sessionLoaded`、`workspaceOf`、`runPrepare` 等做成注入项,测试替换)。

代价是"隔离"只到文件与 home 一级:团队的 `<a2a home>/superagent/` 是单份,团队内多个 member 共享一个引擎实例与一本账。

### 5. 冻结内核的升级代价,被做成了可审计的流程

vendored `README.md:11-14` 定了三步:先 `--compare <checkout>` 看差异(还会列出**上游新增但没 vendor 的 core 文件**),再 `--sync --commit <sha>` 复制并重写清单,最后跑全量。也就是说:

- 上游在 `core/` 里新增一个文件,`--compare` 会以 `notVendored` 报出来,**不升级也是一种可见状态**;
- 任何一个字节的本地修补都会让单测失败,想改内核就只能先改上游或先分叉;
- 升级是一次"独立的、要评审的变更",不是 `npm update`。

## 界面体验

- 入口三处,都在宿主 Web UI 里:①侧栏 footer 的 A2A 控制(活动流,`client/A2aControl.tsx:1-10`);②侧栏会话行,逐行 join/leave 网络(`client/index.ts:1-9`);③**右侧栏两个 tab**——团队请求与决策(`client/team-request.ts:1-13`)。
- 活动流是"这个面板的全部内容":在飞路由、欠回执、路由活动环;打开时轮询以跟上每一轮,收起时未读徽章走慢轮询(`A2aControl.tsx:2-9`)。
- 请求与决策在右栏:一个输入框发请求(`POST /__dsh_a2a/superagent { action: 'request' }`),下面列"团队等你决定的事"(`TeamRequestTab.tsx:1-5`);决策卡 P2/P3 可一键通过,P0/P1 必须选一个选项,宿主也强制(`TeamDecisionsTab.tsx:1-5`)。
- 纯观察面是工作台 `/__dsh_a2a_nexus/`:DOM 优先、无 WebGL,四区为目录(本机/远端/canvas/peers)、台账(pending/dead + abandon)、活动、规划;数据全部来自 `GET /__dsh_a2a/state`,服务端零改动(`docs/design/2026-10-19-a2a-workbench.md:11-17,23-27`)。
- 失败时看到什么:`/__dsh_a2a/superagent` 返回 **401** = 团队存在但这页没有 key,视图直接说;返回 **404** = 没有团队,视图根本不挂(`client/team-request.ts:35-39`)。另有健康横幅(`TeamHealthBanner.tsx`)与 `a2a`/`a2a-reply`/`a2a-deposit` 三类 error(`superagent-a2a-watch.md:79-84`)。
- 信息密度:右栏只放"要你决定的",过程在活动流与工作台。**人不在被服务的那条对话里**——这是它与 05 最本质的界面差异。

## 用户交互的思路

- 发起者通常不是人,是**另一个 agent**:它在自己会话里 `a2a_route` 一条任务,经对端 `/a2a/direct` 落到本机,被翻成 `human: false` 的 Trigger,只能走 Policy 的 bot 名单(`superagent-a2a-watch.md:28`)。
- 谁确认:**router 会话**。候选以卡片送进它的会话,它用 `superagent_route` 决定 accept / attach / stop / ignore(`cordis.patch.yml:39`);人**不**参与接单这一步。
- 人确认的是**决策**,不是工单:P0–P3 决策卡,一键或选一个选项,再由 host 执行(`TeamDecisionsTab.tsx:1-5`);出站还有独立的审批口径(`OUTBOUND_APPROVE`,`host/outbound.ts`)。
- 观察:右栏请求/决策 + 活动流(在飞、欠回执)+ 工作台台账;成员用 `a2a_ticket_report` 报 progress / waiting / ready / failed,问题以卡片回到人(`cordis.patch.yml:143`)。
- 打断:面板 stop 走 `superagent_*` 工具停 Ticket;执行器把 `stop` 当一种 Input 中继给成员(`host/executor.ts:8-13,43`);卡住的工单重启后要人先对账,再 retry 或 reassign(`assignment-card-lifecycle.md:19-21`)。
- 与上游的关键差异:上游把结果写回**原对话的 Channel**;这里只回给**触发它的调用方**,且每个任务**只有一张正式回执**(`receipt-<task_id>`),之后的外发是同一 context 下的新任务(`superagent-a2a-spec.md:100-107`)。人看到的是卡片与回执状态,不是一段对话。

## 五、代价与边界

1. **冻结的是内核,也是上游的修复**。上游在 `core/` 里修一个 bug,这里只能靠一次 `--sync` + 全量测试 + 重新评审才拿到;想临时打补丁,`sha256` 检查会先拦住。
2. **端口实现是内核的 6.6 倍**(13,723 行 vs 2,088 行)。这是"只 vendor 纯内核"的真实账单:复用越纯,适配越多。上游每加一个端口语义,这里就多一处要跟。
3. **两代并存**。`a2a-watch`(外挂 Source)与 `host/`(内嵌引擎)同时在包里、同时导出(`package.json` 的 `./a2a-watch`、`./superagent-ptc`),文档要同时维护两套启用方式;`a2a-source.ts` 靠"原样跑 p2"来避免重复实现,但也意味着 p2 的已知限制被继承(毒行会让游标停住,`superagent-a2a-watch.md:103`)。
4. **授权还没真正收紧**。`settlementAuth` 三档默认 `observe`(`src/config.ts:303`),S7 未开:`114:13` 自己写"唯一余项是 S7:把 `settlementAuth` 默认从 observe 改成 enforce,由 #125 跟踪"。所以今天"结算方不在授权链上"只被记录,不被拒绝。
5. **类型钉的是快照,不是运行时**。`contract.ts` 是纯类型断言,编译期通过不代表运行期上游/宿主行为一致;快照落后于上游最新提交是常态,`snapshot-8c32a9d.ts:38-39` 要求"新快照是独立提交,PR 里写明旧、新 commit"。
6. **执行体语义已经和上游不同**:上游"一单一会话一目录",这里"固定成员池 + 排队 + parking + 交接";Ticket 的语义保住了,Mandate 的语义保住了,但"这个工单在哪个执行体里跑"这条事实换了形状。`assignment-card-lifecycle.md` 整篇都在处理这个新形状带来的投递不确定性:`sending`/`unknown`、重启后不重发、拒绝与异常必须区分(`:5-21`)。
7. **不可用的场景**:需要 A2A 网络、`A2A_CLI_HOME`、家宿主 ≥ next/0.8(信箱行的 `proof`/`admission` 字段是 0.8 才有,`superagent-a2a-watch.md:26-28`);单人单机的 super-agent 用法在这里是多余的重型装配。

## 六、可信度与复现

```sh
git clone https://github.com/NelsonLongXiang/dsh-open-a2a-net && cd dsh-open-a2a-net && git checkout 4151721
node scripts/superagent-upstream.mjs                 # {"ok":true,"files":17,"problems":[]}
# 以 $UP 指向上游 8c32a9dc 的克隆;15 个 core + 2 个测试逐个 cmp,全部 same
for f in src/superagent/upstream/dsh-superagent/src/core/*.ts; do cmp -s "$UP/$f" "$f" && echo same; done
```

## 待验证

1. **端口实现是否真的只经端口**:我读的是 `host/index.ts` 的注释与 `deps.ts` 的注入面,没有逐行核 52 个文件里是否有直接读引擎内部字段的地方。
2. **成员池执行器与上游 Assignment 语义的等价性**:`executor.ts` 自己声明了 parking/交接/重试规则,但上游 `docs/003-execution.md` 里 Assignment 的"只有终报能结单"等约束是否被完整保留,未逐条对照。
3. **`observe` 到 `enforce` 的现场数据**:`#125` 的判据要求"结算方不在授权链上的结算数 = 0"连续 7 天,仓库里只有设计文本,没有实测数字。
4. **`--compare` 与真实使用面**:我只核了 `UPSTREAM.json` 声明的 `8c32a9dc` 与本地上游克隆一致,没有对上游 HEAD 跑 `--compare`;366 个 spec 与 9 道门禁说明工程强度,但证明不了有第二方在真网络上跑过。
