# 05 · ctrl439/dsh-superagent — 整树分叉,把"一个仓、一种聊天工具"改成多仓多机器人

> `439436269-ctrl/dsh-superagent@9dea493`(2026-11-25;0★)。上游 `deepseek-ai/dsh-superagent-prototype@8c32a9dc`(24,565★ / 3,081 forks,2026-11-25)。注册表条目 `439436269-ctrl__dsh-superagent`。证据等级 ★★★:读了 `README.md`/`README.en.md`、`package.json`、`cordis.patch.yml`、`docs/{009,010,011,012,013,014}`(前三篇读关键节)、`examples/im-bridges/*`,并把 `src/` 与上游 110 个 TS/TSX 文件逐个 `cmp`;**没有**实机安装,没有真实钉钉/企业微信凭据。

## 一屏事实

| 项 | 值 |
|----|-----|
| 自述 | "本仓库从 DeepSeek Harness 的原型起步,之后长出了多仓库与多源能力,均已在真实实例上验证"(`README.md:59-61`) |
| 声量 | **0★**;HEAD `9dea493`(2026-11-25 13:45 +0800);作者 `vfvrpq`、工作副本 `E:\codes\dsh-superagent-prototype`(`docs/014-progress.md:7-10`) |
| 包形态 | `@vfvrpq/dsh-superagent@0.3.0`;**未标 `private`**(上游是 `private: true`),MIT,`author` 仍写 DeepSeek Harness Team(`package.json:2-5`) |
| 入口 | 10 个 export:`index`、`client`、4 个 watch(`github`/`feishu`/**`im`**/**`session`**)、**`kind`**、**`claim`**、`package.json`、`locale/*.json`(`package.json:12-27`) |
| plugin id | 仍是 `dsh-superagent` / `-github` / `-feishu`,新增 `-im`、`-session`、`-claim`,外加三个 preset(`cordis.patch.yml:4-33,214-222`) |
| 宿主钉版 | 23 个 peer `^0.2.1-alpha.2`、`cordis 4.0.5-alpha.1`、node ^22.19 \|\| ≥24(`package.json:62-65`),与上游同档 |
| 代码规模 | `src/` **121 个 TS/TSX / 17,523 行**;上游 **110 个 / 15,205 行**;测试 **60 个 spec** |
| 与上游关系 | 110 个上游文件**一个不少**(0 缺失):**58 个逐字节相同、52 个被改**;另加 **11 个新文件** |
| 新文件 | `sources/im.ts`、`sources/im-bridge.ts`、`sources/session.ts`、`sessions/bus.ts`、`app/tools/session-bus.ts`、`app/tools/reviewer.ts`、`executor/review.ts`、`claim.ts`、`workers.ts`、`kind.ts`、`client/dispatcher.tsx` |
| 复现 | `git clone … && git checkout 9dea493`;对上游 `src/` 逐个 `cmp`;`find src \( -name '*.ts' -o -name '*.tsx' \) \| xargs wc -l` |

## 影响力

| 项 | 数字 / 事实 |
|----|-------------|
| GitHub | **0★ / 0 fork / 0 watcher**,1 个 open issue;created 2026-11-04,pushed_at **2026-11-25T12:31:41Z**;`fork: true`,parent 与 source 都是 `deepseek-ai/dsh-superagent-prototype` |
| npm | **已发布**:`@vfvrpq/dsh-superagent@0.3.0`,59 文件 / 1,587,678 B 解包,maintainer `vfvrpq`,`repository` 指回本仓 |
| 注册表 | `data/plugins/439436269-ctrl__dsh-superagent.yml`,类目 **workflow**(13,136 条里 793 条) |

它是**真的 GitHub fork**(不是"搬了代码的独立仓"),而且把包发上了 npm(上游本身是 `private: true`)——这两件事都说明作者想让人装,不只是给自己用。但采用是零:0★/0 fork/0 watcher 意味着没有传播;另有 1 个 open issue,内容未读。
被抄/被引用:**未见**。注册表里另有 11 条提到 `im-bridge`/`IM bridge`/`im-watch` 的条目(如 `BiBoyang__dsh-im-bridge.yml`、`caoxiaohu7745-bot__kongmu-im-bridge.yml`),是**同题不同源**;`439436269`/`vfvrpq` 出现在 19 条注册表里,全是同一作者的其它插件,没有一条引用它的多仓或 IM 桥。
结论:**影响 = 0**,既不是机构背书也不是社区采用;这页的价值在"它验证了哪条假设可以这样破",不在"它被谁用"。

## 一、它要解决什么问题:上游三条假设同时不成立

上游的部署模型写得很直白:一个部署 = 一个仓库 + 一个主 Session + 少数几个 Source 实例。

| 上游假设 | 代码锚点 | ctrl439 面对的事实 |
|----------|----------|--------------------|
| **一个部署只服务一个仓库** | `deployment.ts:46` 的 `repository: z.string()`,启动时校验"账号能推到它"(`:86-105`) | 团队同时在多个仓干活;一张工单必须知道自己在哪个仓开分支、开 PR、回话 |
| **一个 kind 只能有一个实例** | `sources/registry.ts:45-49`:`instances()` 按 `kinds` 遍历,`settings.sources[kind]` 的键就是 kind | 两个钉钉机器人、第二个飞书应用、一个企业微信桥要同时在线,各有各的群和凭据(`docs/013-multi-repository.md:69`) |
| **聊天工具只有 GitHub 与飞书** | `sources/` 里只有 `github*`、`feishu*` 两套实现 | 团队实际在钉钉/企业微信/Telegram;而新增一个 kind 要改内核、重打包(`docs/011-extensions.md:14-16,27-30`) |

作者的自我诊断比外部观察更狠:多源"不是缺 UI",而是 `settings.sources` 的键就是 kind,存储层表达不了第二个飞书机器人(`013:71-80`);更要命的是 `SourceContext.config(kind)` 按 **kind 名**取配置,第二个实例拿到的是第一个实例的配置(`013:103-128`,`sources/host.ts:40`)。所以多仓与多源共享同一个前置条件:**配置从单值变集合**。

## 二、它的路径:整树分叉,但只动"部署面"

它没有换领域模型,五段管线原样保留,改动集中在四处:

1. **多仓**:`deployment.repositories: string[]` 与 `machine.repositories`(`deployment.ts:55-60,73-78`),`Ticket.repository`(`core/model.ts:285-289`,`core/tickets.ts:43-48`),按仓的游标与线程键(`sources/github.ts:224-233`),按仓的 worktree 根(`app/execution-environment.ts:19-29`)。
2. **多实例**:`SourceInstance.kind` 缺省 = 键名(`sources/kind.ts:116`),`instances()` 按 kind 归组(`sources/registry.ts:45-59`),`SourceContext` 绑定实例 id 且 `config()` 无参时取绑定实例(`app/source-context.ts:33-47`)。
3. **新 Source**:`im`(通用 IM 桥)与 `session`(别的会话派活),各自一个 bundle 入口。
4. **人的界面**:调度者 tab + `claim` 工具(`cordis.patch.yml:214-222`),独立只读评审会话(`README.md:11`,`executor/review.ts`、`app/tools/reviewer.ts`)。

放弃了三条替代路:不写第二个 `feishu` 式的一等 Source(改成桥进程)、不改 `settings.sources` 的文件版本号(用 `kind ?? id` 迁移)、不为多仓做独立状态库(仍是单 `stateDir`)。

**兼容锚点是"默认仓"**:非默认仓才改写线程键、游标键、worktree 路径与回复地址,默认仓保持 `github:5` 这种旧形态,于是单仓部署"行为与改造前逐字节一致"(`README.md:70`,`013:148`)。这是它能宣称"单仓零感知"的全部依据。

## 三、它如何利用 `dsh-superagent`

**原样保留的 58 个文件**以基础设施与读路径为主:准入与部署检查(`admission.ts`、`setup.ts`)、`limits.ts`、`navigation.ts`、`infra/health.ts`、`core/` 的 `ids`/`intake`/`memory`/`part`/`reasons`/`stage`/`index`、`app/` 的 `store.ts`/`passes.ts`/`cards.ts`/`delivery.ts`/`effects.ts`/`migration.ts`/`store-read.ts`、`sources/` 的 `github-trigger.ts`/`feishu-read.ts`/`feishu-image.ts`/`poll.ts`/`admission-context.ts`,以及大部分 `client/*.tsx`。

**但"规则没改"不等于"文件没改"**:承载领域规则的那几个文件都落在改动的 52 个里——`core/engine.ts`、`core/model.ts`、`core/tickets.ts`、`core/evals.ts`、`core/assignments.ts`(多为加 `repository`、按仓改动线程/游标)。**Mandate 不可变、Policy 变更只投递不撤销、Subscription 扇出不走 Eval** 这三条语义仍与上游 `docs/001-domain.md:34,37` 对齐。

**改的 52 个文件里,值得点名的是**:

- `sources/registry.ts:45-59`:从"按 kind 遍历"改成"按实例 id 遍历",`stored.kind ?? id` 保证旧配置原样读;
- `sources/registry.ts:87-94`:`channelAllowed` 用 `channel.address.instance ?? channel.source` 解析实例——这是把"实例身份"塞进 Channel 地址换来的;
- `app/source-context.ts:33-47`:`sourceContextOf(…, instance)` + `config()` 默认取绑定实例,这是 `013` 里判定的"更硬的耦合"的正解;
- `sources/github.ts:227-233`:`stamped()` 只对非默认仓改写 `thread`、`address.repository`、`threads[].id`,游标名 `KV.github.stream(repository:id)`;
- `executor/dsh.ts:132-141`:worktree 从"部署根下"改成"仓目录下的 `worktrees/`",一个仓一个文件夹而不是一单一个。

**新增的两个 Source 才是这页的主角**:

- `im`:kind 定义 + 一套"外部进程说 JSONL"的协议,读写全在 `sources/im-bridge.ts`(192 行);
- `session`:纯构造器 `sessionThreadId` / `sessionChannel` / `sessionTrigger`(`sources/session.ts:19-42`),`kind` 的 `channel.send` 交给一个由 Runtime 注入的投递钩子(`:44-48,64-69`),`runtime.ts:301-306` 把它接到 Session 服务,`runtime.ts:115-135` 把 `request`/`delegate` 两种意图都塞进同一条 `receive(sessionTrigger(...))`。
  注意这里有一处**文档落后于代码**:`sources/session.ts:4-6` 仍写"Built but not yet registered",`docs/012-dispatcher.md:102-112` 仍把"注册 sessionKind、改 inbound 分支"列为待做,而 `cordis.patch.yml:18-19` 已插入 `-session` 条目、`runtime.ts` 已接线。

## 四、技术思考

### 1. 多仓怎么表示:三层 + 一个兼容锚点

```
deployment.repositories[]  ← 部署级:监听哪些仓(来源设置可增删)
trigger.meta.repository    ← 事件级:这条 Trigger 来自哪个仓
Ticket.repository          ← 工单级:这单在哪个仓开分支/开 PR/回话
默认仓(空值)               ← 兼容:读不到就回落到配置里的那一个
```

三层各自解决一个问题,但真正的判断题只有一个:**"编号当身份"的地方,多仓下都要带上仓库**。作者踩了两次同一个坑——线程键 `github:5`(`013:168-188`)、PR `follows` 存裸编号(`013:237-255`,至今未修,`README.md:80` 自认)。第一次用"只改 `stamped()` 一处、不动任何函数签名"的方式修掉(`013:190-201`)。

### 2. IM 桥为什么放在内核外

不是为了架构好看,是因为**放进内核的代价它付不起**:新增一个 kind 要动 `src/sources/`、加一个 tsdown 入口、加一行 `cordis.patch.yml`,并且第三方只能依赖包内部类型(`011:14-16,27-30`)。桥把这件事降级成"写一个子进程"(`template.mjs` 49 行,`telegram.mjs` 95 行):

| 设计选择 | 位置 | 换来了什么 |
|----------|------|------------|
| 收/发拆成两个进程:`receive` 长驻、`send <json>` 一次性 | `009:12-20` | 接收端重启时回话仍然能发;两条路径不共享状态 |
| Trigger id = `key('im', chat/messageId)` | `009:34-36`、`im-bridge.ts:63` | 重投递天然幂等,桥可以不持久化游标 |
| 退出码 `3` = 会话已不存在 | `009:57-61`、`im-bridge.ts:26-28,182-191` | 把"目标没了"和"暂时失败"分开,Outbox 不会对死群重试一整天 |
| 失败提示按网络/证书分类 | `im-bridge.ts:82-89` | 内网网关只解析不到时,health 说的是"连上公司网"而不是"机器人坏了" |
| 凭据留在桥的环境里 | `009:96-102` | 令牌不进设置、不进库、不进会话指令 |

代价写在同一篇文档里:内核只看见 chat id、名字、文本(`009:3-5`),企业微信的非文本消息只能"确认后丢弃"(`009:129-130`);桥是**可信代码**,以运营者身份运行并往 Trigger 里写什么都行(`009:99-100`)。

### 3. 多实例:实例身份要贯穿三处,少一处就出 bug

`013` 记了一次真实的连环失败:两个探针实例各配自己的群,消息都到了引擎却全被判 `chat_not_allowed`——因为 `channelAllowed` 按 kind 解析,永远解析到默认实例(`013:316-346`)。修法就是上面那三处改动:存储按实例 id、上下文绑定实例、Channel 地址带 `instance`(`im-bridge.ts:91-96`)。

但**不是所有地方都贯穿了**,作者自己列了残留:health 条目按 kind 登记(`im.ts:56` 的 `health: ['im']`),同类型多实例显示成一行(`README.md:76`);`received` 计数也按 kind(`README.md:77`);策略部分的解析入口仍以 kind 名为键(`registry.ts:80-86`)。最后一条是否影响"每个实例一张准入表",我只读到 `im.ts:91-102` 按实例配置生成行、`settings.ts:230` 却把 `instance.id` 传给按 kind 取值的 `policyPart`,**未验证**。

### 4. 状态与隔离:分层在目录,不在数据库

`stateDir` 仍是单份,`orchestrator.sqlite` 仍是一个(`app/runtime.ts:172`)。多仓带来的隔离是**目录级**的:`<root>/<owner>/<name>/worktrees/<name>`(`execution-environment.ts:19-29`,`executor/dsh.ts:132-141`),外加按仓的游标键(`github.ts:232-233`)与线程键(`:227-231`)。所以多个仓共享一套工单、一个面板、一份 health、一个并发上限——隔离到"文件不串"为止,不隔离治理。

### 5. 长时空闲的 Stream 不会重建(已知缺口,可定位到代码)

钉钉 Stream 桥的接收回路只在两种信号下结束:收到 `SYSTEM` 的 `disconnect` 帧后主动 `close`,或 socket 的 `close` 事件(`dingtalk-stream.mjs:55-62`);子进程一旦退出,`runIm` 的循环会带退避重启它(`im-bridge.ts:99-126,144-153`)。问题在于**第三种情况没有信号**:网关静默丢掉连接、socket 不报 close,子进程就一直活着,`runIm` 的 `while` 等不到重启。没有 ping/keepalive 定时器,`README.md:79` 自认"keepalive 尚未实现"。这是"用长连接换掉公网回调"的必然账单,不是实现疏忽。

## 界面体验

- 入口是宿主侧栏的一个锤子图标:`PANEL_ID = 'dsh-superagent'`、`order: 10`,点开是主面板;Plugin Manager 里另有同一插件的配置页(`client/index.tsx:21-28,53-57`)。
- 面板七个 tab:`overview / source / trigger / eval / execution / dispatcher / settings`(`client/route.ts:7`),`settings` 再分 source/eval/execution/prompts/deployment 五组(`:9`)。
- 概览页自述是"待人工处理的 Ticket、系统问题、24 小时流量计数、执行器负载"(`client/overview.tsx:1`);README 的截图注释补了一句:红色块是**评估未能进行**的条目,带原因(`README.md:88`)。
- 信息密度靠"每一行都能点":问题行自带"去修"按钮与 `CheckSetupButton`(`overview.tsx:26-40`);工单以"工作区"呈现,每个有自己的目录(`README.md:89`)。
- 它不只是看板:面板能 `POST tickets/:id/stop`、`POST triggers/:id/requeue`、`POST executor/pause`(`app/api.ts:39,33,40`)——叫停、重排队、暂停执行器都在界面上。
- 失败时的可见性:问题按 `kind` 分成 setup / no-source / no-allowed / executor-paused / runtime-error / source-error,每种带定位链接与原因(`overview.tsx:26-40`);IM 桥的失败被翻成一句人话(内网 DNS、证书、连不上),写进来源健康(`im-bridge.ts:82-89`)。
- IM 这一侧**没有 UI**:人只在自己熟悉的聊天工具里看到消息与回复;桥的 stdout 是 JSONL,不面向人(`examples/im-bridges/template.mjs:8-23`)。

## 用户交互的思路

- 发起:人在 GitHub issue/PR 评论、飞书话题或任意 IM 会话里说话;`im` 桥把它变成一条 Trigger(id = `chat/messageId`),`scope` 按**该实例**的会话配置决定这条会话是否被接收(`im.ts:57-62`)。
- 确认:**没有确认步骤**。谁能发起由 Policy 的 allow list 与准入表决定,`explicit` 由主 Session 用 `orchestrator_route` 接单,`inferred` 按 `off/observe/auto` 三档处理(上游 `002-authorization.md:91-101`);人要拦,只能事后 stop。
- 观察:三个 tab 分工——`trigger` 看事件、`eval` 看判定与理由、`execution` 看工单与它的目录;实时进展在工单自己的 `worker-<id>` 会话里。概览给 24 小时计数。
- 打断/接管:面板的 stop 是**命令**(直接改工单);在聊天里说"停"只是一条普通 Trigger,由 Eval 判定(上游语义,本 fork 未改)。本 fork 新增的接管是 `orchestrator_claim`(`claim.ts:1-7,21-30`):用 router preset 起的会话说"我要接手调度者"就成为做判定的会话,面板"调度者"tab 可换回。
- 结果回路:回原对话。GitHub 走 PR/评论,IM 走桥的 `send <json>`;桥退出码 3 表示会话已不存在,回复被丢弃而不是永远重试(`009:57-61`)。
- 与上游的差异是三条:**任意 IM 成为来源**(不必写一等 Source)、**人可以把调度者换成自己看得见的会话**、**面板能 stop/pause/requeue**。代价是"谁在决定"从固定变成可配置,也就更容易配错。

## 五、代价与边界

1. **110 个上游文件全要背**:58 个原样(升级时是纯 diff)、52 个要跟。上游没有 npm 包、没有版本化 API,同步只能人工 `diff`;`git remote` 只有 `origin`(GitHub fork 关系仍在),没有配好的 upstream 同步脚本(未读到)。
2. **自己的 test 基线不是绿的**:`docs/014-progress.md:51` 记"全量 62 failed / 1155 passed",作者注明"未用 git stash 对跑,其余组是推断不是结论"。60 个 spec 里有多少继承自上游未核。
3. **单仓单实例之外没人为它背书**:多仓端到端只在一个第二个仓 `439436269-ctrl/superagent-second` 上跑通过一次(`013:203-225`);多源里"第二个机器人真的收到过一条"始终缺一次人工 @(`013:257-272`);企业微信多实例"没有凭据连过真实群"(`013:375`)。
4. **凭据位置与自己的安全规则打架**:多实例要各自凭据,于是新增每实例 `config.env`(`im.ts:23-27`,`013:160`),而 `009:74-75` 的原规则是"凭据只放 DSH 进程的环境,绝不进这个设置表单,因为面板配置对智能体可见"。`env` 不在面板 `fields` 里(`im.ts:41-55`),但它与其它 config 一起落进 settings,和原规则的口径不一致。
5. **文档债**:`sources/session.ts:4-6` 与 `docs/012` 都还在说 session 源"未注册";`docs/011-extensions.md:14-15,19` 里 `→`/`—` 已损坏成 `鈥?`(UTF-8 被按 GBK 读过后再存盘)。这些是"由智能体生成的仓库"的典型残留,读文档时必须回代码核对。
6. **不可用的场景**:单实例钉钉/企微 + 单仓是它验证过的形状;多仓多实例的治理面(并发、health、计数、策略)仍是半成品;Windows 路径假设很重(`E:\codes\…`、`014:67-74` 的 PowerShell 坑清单),跨平台未验证。

## 六、可信度与复现

```sh
git clone https://github.com/439436269-ctrl/dsh-superagent && cd dsh-superagent && git checkout 9dea493
# 与上游逐文件比对:58 相同 / 52 不同 / 0 缺失
for f in $(cd ../upstream/src && find . -name '*.ts' -o -name '*.tsx'); do cmp -s "../upstream/src/$f" "src/$f" && echo same || echo diff; done | sort | uniq -c
cat package.json | head -30; cat cordis.patch.yml | sed -n '1,35p'
```

## 待验证

1. **`@vfvrpq/` 是否真的发到 npm**:`package.json` 没有 `private`,但 `README.md:15-21` 的安装路径是"读 SETUP.md 让智能体装",没说 `npm i`。
2. **策略层的实例穿透**:`policyPart(instance.id)` 与 `kinds.get(id)` 的取值口径,两个 `im` 实例是否共享一份 allow list。
3. **`session` 源的实际状态**:条目已插入、`inbound` 已改走 `receive`,但 `docs/012` 的步骤 2-4(面板准入表、`orchestrator_event` 工具)是否完成。
4. **PR `follows` 跨仓撞号**:`README.md:80` 与 `013:237-255` 都承认未修;两个仓有同号 PR 时的实际表现。
5. **与上游/其他契约插件的共存**:包名换了 scope 但 plugin id 未换,能否与 `trace`/`wechat-source` 这类按 `orchestrator` 服务与 `stateDir` 对接的插件同 profile 运行。
