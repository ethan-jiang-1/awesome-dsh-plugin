# DASHAN-0079/dsh-superagent-adapt — 五个源文件、1213 个用例:把原型抬到 0.2.2-rc.3

> `repo@34c21ff`(2026-11-18 11:39 +0800,提交信息 "Document the prebuilt tarball install";0★ / 0 forks,pushed 2026-11-20)。上游 `deepseek-ai/dsh-superagent-prototype@8c32a9dc`(24,570★ / 3,081 forks,API 2026-11-25)。注册表条目 [`DASHAN-0079__dsh-superagent-adapt.yml`](../../../data/plugins/DASHAN-0079__dsh-superagent-adapt.yml),类目 workflow。证据等级 ★★★(`ADAPTATION.md`、`README.md`、`package.json`、`cordis.patch.yml`、5 个改动文件的逐行 diff、测试文件、`docs/adaptation/` 全部读过;**没有**重跑测试或安装)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 / 类目 | DASHAN-0079/dsh-superagent-adapt / workflow |
| 声量 | 0★ / 0 forks;pushed 2026-11-20 |
| repo@commit | `34c21ff`;创建于 2026-11-10 前后(`docs/adaptation/` 的日期) |
| 包形态 | `dsh-superagent@0.1.1`,`private: true`,MIT;bundle;提交了构建产物 `lib/`(约 1.0 MB);release tarball 与社区 plugin index 都可用 |
| 宿主钉版 | 24 个 peer 全部 `^0.2.2-rc.3`,新增 `@deepseek-ai/dsh-error`;`cordis 4.1.0`、`schemastery 3.19.0` 精确钉;`engines.dsh ^0.2.2-rc.3`(`package.json:56-89`) |
| 与上游的差异 | **5 个源文件**(`http.ts`、`resources.ts`、新增 `session-history.ts`、`client/deployment.tsx`、`deployment.ts`)+ 9 个测试文件(新增 1 个、就地迁移 8 个);`cordis.patch.yml`、工具与 store 键、导出面一字未改 |
| 自述定位 | "same bundle with five source changes, ten added tests, and the delivery declarations pinned to the target host"(`ADAPTATION.md:3-5`) |
| 复现 | `git clone https://github.com/DASHAN-0079/dsh-superagent-adapt && git checkout 34c21ff`;`diff -rq ../upstream/src src` 输出 5 行 |

## 影响力

- 数字(GitHub API,2026-11-25):**0★ / 0 fork / 0 watcher**;2026-11-10T16:00Z 创建,最后 push 2026-11-20T02:51Z;topics 为 `deepseek-harness`、`dsh-bundle`、`dsh-plugin`。
- 分发:**没有 npm**——`dsh-superagent`(它的包名)与 `dsh-superagent-adapt` 在 registry 都是 404;可装的是 release tarball(HTTP 200)、`git+…#v0.1.1`(`README.md:39`),以及作者自建的 plugin index(`DASHAN-0079/dsh-plugin-market` 的 `index.json` 里确有 `dsh-superagent` 条目)。
- **采用信号:没有外部采用**。0 fork、没有第三方 PR;唯一的 issue/PR 是作者自己的 #1 "Adapt SuperAgent to the public DSH 0.2.2-rc.5 release"(2026-11-19,open,未合并),报告 rc.5 上 1170/1213、剩余 43 条失败"present on the base revision",并称 typecheck、build、59 个定向测试、安装与 profile 组合均通过。
- 一个间接信号:被本仓注册表收录(`data/plugins/DASHAN-0079__dsh-superagent-adapt.yml`),但那是策展,不是采用。
- 活跃度:HEAD 提交是 2026-11-18,`pushed_at` 是 2026-11-20,差的两天与 rc.5 PR(2026-11-19)吻合——形态是"一次性交付 + 一条后续",不是持续维护。
- 判断:**没有影响**;它的价值不能按星标读。它是这批分叉里唯一把"改了什么、凭什么说没改坏"做成可复核交付物的一个——影响力应记在**方法**上(逐用例等价性 + 环境失败归因),而不是采用量上。也正因如此,它连"被官方接收"这条理论路径都没有:上游 `has_issues: false`,自己的后续也只开到 rc.5 的 PR。

## 1. 它要解决什么问题

上游声明 `engines.dsh: ^0.2.1-alpha.2`(上游 `package.json:55`),而 DSH 在 0.2.2 上把几个上游依赖的接口删了改了。`docs/adaptation/compatibility-checklist.md:8-14` 把 11 个 typecheck 错误归成 7 个根因,其中真正致命的四个:

- `SessionController.inspect` 被删——上游读 executor 会话记录全靠它(`src/app/resources.ts` 的 `transcript()`),删了之后 transcript 资源直接编译不过;
- `ConfigFormSnapshot.mode` 被删——面板"只读/可写"的判断依据没了(`src/client/deployment.tsx`);
- `webServer.port` 从 `number` 变成 `number | undefined`——同源检查拿不到端口;
- `WebRoute.auth` 变成默认 `'required'`,而没有 `authorize` responder 时直接 **503**——`/orchestrator` 的所有路由会整体不可达。

再加一条只在 Windows 上致命的:`stateDir` 的校验是 `/^\//`(上游 `src/deployment.ts:13-16`),`C:/…` 与 UNC 路径一律被拒,插件连激活都做不到(`docs/adaptation/stage4-install-and-run.md:5,55`)。

所以痛点不是"功能不够",而是**当前宿主上装不上、跑不起来**。而且这类修补没有回流通道:上游仓 `has_issues: false`、`has_discussions: false`(GitHub API,2026-11-25),issue 与 PR 共用同一个开关,等于两条路都关着——这正是 README 那句"the upstream repository has issues and pull requests disabled, so it cannot take this adaptation directly; this fork-like checkout carries it instead"(`README.md:7`)的事实基础。

## 2. 它的路径

它选了最窄的一条:**不换设计、不换领域模型,只把与宿主 API 接触的五个点改掉,再用测试证明"除此之外没变"**。

| 文件 | 改法 | 为什么必须改 |
|---|---|---|
| `src/app/session-history.ts`(新增,104 行) | 用 `sessionController.events` 分页读取整条会话日志:首屏钉 `throughSeq`,后续页用排他的 `beforeSeq`,校验不通过就抛 `HistoryIncomplete` | `inspect` 没了;transcript 的下标是"第几条消息",读短了会把编号整体挪位 |
| `src/app/resources.ts:114-115` | `transcript()` 改走 `sessionHistory()`,并把请求的 `signal` 传下去 | 同上;取消仍要生效 |
| `src/app/http.ts:238-249` | 路由声明 `auth: 'anonymous'`;`port === undefined` 时回 500 并记日志,已绑定但异源仍回 403 | 默认 `'required'` 会让路由 503;同源检查自己已经做了 |
| `src/client/deployment.tsx:36,49-54` | 只读 = `status === 'ready' && !writable`,不再读 `mode` | `mode` 字段被删 |
| `src/deployment.ts:13-15,19` | `absolute()` 接受 `/x`、`C:\x`、`C:/x`、`\\host\share`,拒绝相对与 `C:state` | Windows 上插件原本无法激活 |

**放弃了什么**:放弃"钉在旧宿主上"(那就永远用不了 rc.3 的新 API);放弃"在宿主侧打补丁"(没有渠道,也影响别人);放弃"vendor 内核 + 自己的壳"(`06-vendored-engine-a2a` 那条线的做法,会丢掉"同一份 bundle"这个前提)。也放弃"把差异藏起来":它把五处改动、10 个测试、等价性数据全部写进 `ADAPTATION.md`,并把审核过程留在 `docs/adaptation/`。

**分发上也做了取舍**:源码树的 `devDependencies` 是 `workspace:*`(`package.json:92+`),离开 DSH workspace 根本装不上;而 npm 上的 `@deepseek-ai/*@0.2.2-rc.3` 类型还落后于打标签的宿主(webserver 类型缺 `auth` 字段,`ADAPTATION.md:10-14`)。于是它把构建产物 `lib/` 提交进仓库、去掉 `prepare` 脚本、补 `icon`/`exports`/`files`,并靠一个钉死 commit 的社区 plugin index 分发(`ADAPTATION.md:62-75`、`README.md:26-54`)。**结论是:能装的是产物,不是源码。**

## 3. 它如何利用 dsh-superagent

**利用方式是"原样继承"。** `diff -rq` 显示 `src/` 只有 5 个文件不同;`cordis.patch.yml` 的 5 个 entry(id、preset、顺序)与上游一致;`tests/` 的差异只有 1 个新增文件和 8 个既有测试文件。领域模型(Ticket/Mandate/Assignment/Subscription/Executor)与 `orchestrator.sqlite` 的 schema 都没有被碰。

它继承得有多彻底,`docs/adaptation/gate-report-equivalence.md:8-21` 的 L1 表给了可核对的口径:patch 行 `numstat` 为空、19 个工具名与 schema 为空、store 键与 schema 为空、`package.json` 规范化版本后唯一差异键是 `engines`、`exports`/`dsh.bundle`/`dsh.client.inject`/`scripts`/`files` 四项深比较全等。也就是说:**它把"依赖"变成了"同一件东西的另一个宿主版本"**,而不是"基于它的二次开发"。

唯一的接口面变化在 HTTP:`auth: 'anonymous'` 是新增字段,但路由表、`sameOrigin`、`x-orchestrator-request` 都没动(`docs/adaptation/gate-report-equivalence.md:18`)。transcript 的读取路径换了实现,但对调用方(`resources.ts` 的 `ticket/<id>/transcript`)语义不变——仍是"整条日志,最新在前"。

## 4. 技术思考

**关键判断一:读不全就报错,不要返回短日志。** `session-history.ts` 把一整套不变量写进了注释与代码(注释里列了九条):后续页必须报告同一个 cursor(否则窗口在并发追加下漂移)、页内与页间 `seq` 必须连续、首屏必须够到钉住的 cursor、最旧事件必须是 `seq 0`、坏记录必须抛错、空日志只允许 `cursor = -1`、已 abort 的 signal 在请求前就拒绝(`src/app/session-history.ts:23-40`)。理由是 transcript 的编号是位置:少一条,后面所有"第 n 条消息"都会指错,而错得很安静。这是本页最值得记的一条工程判断——**宁可让一个只读资源失败,也不返回一个看起来正常的错数据**。

**关键判断二:把鉴权声明成 anonymous,但自己把门。** rc.3 的默认 `'required'` 会在没有 `authorize` responder 时回 503,插件等于整体下线;而 `/orchestrator` 本来就只绑 loopback、自己查同源与 `x-orchestrator-request`。声明 `anonymous` 保住了 rc.1 的行为,代价是**安全边界从宿主的统一鉴权退回到插件自己的检查**。注册表条目因此专门写了一句"its HTTP routes have no DSH access check, so a web page open in your browser could call them"——这句话是对的:任何能连到该端口的本机进程都能调管理 API。

**关键判断三:端口没绑定就 500,不猜。** `sameOrigin` 需要真实端口;`port` 变成可选后,代码选择"未绑定 → 500 + 固定日志"(`http.ts:243-248`),而不是从 Host 头或默认端口反推。这与第一条同源:不确定就失败,别把不确定性变成放行。

**关键判断四:Windows 路径校验要覆盖三种绝对形式。** 新正则 `/^(\/|[A-Za-z]:[\\/]|\\\\)/u`(`deployment.ts:15`),测试给了 4 个接受(`/var/...`、`C:\state\...`、`C:/state/...`、`\\host\share\...`)与 5 个拒绝(`state/...`、`./state`、`../state`、`C:state`、`\`)(`tests/deployment.spec.ts:53-61`)。注意 `C:state` 是"盘符相对路径",不是绝对路径——这条区分很多插件会漏。

**关键判断五:等价性用"逐用例比对"而不是"总数看起来差不多"。** 原生侧 `8c32a9d` 零改动跑出 1197 例 / 1155 过 / 42 失败;适配到 rc.1 后 1206 例(1197 + 9)逐用例比较 **0 差异**;最终 rc.3 上 1213 例 / 1168 过 / 45 失败(`ADAPTATION.md:43-53`)。42 条失败按 `failureMessages` 逐条定性,总口径是 **41 条 Windows 环境族 + 1 条既有基线红、0 条回归**(`gate-report-equivalence.md:34-44`);分类明细列了符号链接 `EPERM`、POSIX 命令缺失、路径/引号语义、`relative()` 反斜杠等,但这些行相加是 37、与合计 42 差 5 条,报告没有解释差额。它还主动记录了"那条翻转"的归因:native rig 少拷了 `LICENSE`,不是适配侧的增益(`:46-51`)。这套记账比"我们跑通了"值钱得多。

**这套证据能证明什么、不能证明什么。** 它能证明:同一份源码在换宿主后,除五个适配点之外的代码路径与原生侧逐步一致——工具、store、导出、patch 都没动,失败集合逐条对得上。它不能证明**行为**等价:测试是单进程的单元/集成用例,没有覆盖真实模型调用、调度时序、GitHub 网络与面板交互;而这些恰恰是 Super-agent 的主要行为面。更微妙的是,测试套件在 Windows 上跑出 42 条环境失败,说明它无法覆盖 Windows 特有的那几条路径——真正验证 `stateDir` 与 shim 的是 `stage4` 的手工三项(监听、面板 200、`state` 200),不是测试。**等价性证据的边界,正好落在它想修的那个平台上。**

## 界面体验

- **入口**:侧栏面板列表里一个锤子图标(`src/client/index.tsx:55`,`HammerIcon`,`order: 10`),点开整页面板;同一份注册还在插件管理里给一张配置卡(`:56-57`)。
- **面板**:上游的六页——概览 / 来源 / 触发 / 评估 / 执行 / 设置(`docs/005-panel.md:15-24`),表格密度高、详情在右栏;概览首屏是"待人工决定 / 系统问题 / 24 小时流量 / 执行器负载"(`:19`)。
- **会话**:它**不隐藏** `worker-*` 与 `orchestrator-*` 会话——客户端里没有对应的收起逻辑(`src/client/` 搜不到 `worker-`),所以人打开侧栏会看到一串执行器会话。这是与 02-local 最直观的界面差异。
- **实时性**:面板每 5 秒拉一次 `GET state`,重启中 1 秒(`src/client/provider.tsx:74,89`);没有桌面通知,也没有 IM 推送——人被"原对话里的新消息"而不是"面板变化"驱动。
- **失败时看到什么**:工单阶段直接写 `Input undelivered` / `Awaiting answer` / `Awaiting review` / `Blocked` / `Failed`(`docs/003-execution.md:9-17`);管理 API 在端口未绑定时回 500 与固定文案 `Management is unavailable…`(`src/app/http.ts:244-248`);部署页在宿主拒绝写入时显示只读提示(`src/client/deployment.tsx:49-54`)。
- **终端**:文档给的运维面是 `scripts/dsh-superagent status/start`(`docs/006-deployment.md:117-121`),但它 `import fcntl`、依赖 tmux,Windows 上直接 `ModuleNotFoundError`(`docs/adaptation/stage4-install-and-run.md:73-76`)——对这批用户,可用的界面只剩面板与 HTTP。

## 用户交互的思路

- **谁发起**:名单内的人在 GitHub issue 里评论 @ 机器人,或在飞书群 @ / 私聊机器人;全程不打开 DSH(`docs/001-domain.md:27-29`)。
- **在哪确认**:没有"提交工单"的入口——Eval 的 gate 决定谁能发起、assessment 决定接不接;需要人拍板时用结构化的 `Attention` 挂在工单上等人回答(`docs/001-domain.md:101`、`src/client/ticket.tsx:144-145`)。
- **怎么观察**:原对话里收回执与结果,要看全貌再打开面板。追问不必重新 @:同一 Thread 上的新消息按 Subscription 扇出到同一工单,不再过 Eval(`docs/001-domain.md:37`)。
- **怎么打断**:人在原对话里说停——只有人的 stop 能撤回 Mandate(`docs/001-domain.md:34`);面板可以暂停处理;单张工单可重试或重启。
- **与上游的差异**:**没有差异**。它刻意不改交互面,连 UI 也只动了 `client/deployment.tsx` 的只读判断。它把"人不在 DSH 里"当常态——与 02-local 把整条回路搬进 DSH 正好相反。
- **代价**:异步、跨应用、能被 IM 通知拉动;但一旦 GitHub/飞书没配好(例如 `stage4` 里的 `repositoryUnset`),这套交互就**只有观察面、没有发起面**——面板能看到空队列,却没有任何入口开始第一张工单。

## 5. 代价与边界

1. **只对一个 rc 负责**。`engines.dsh` 与 24 个 peer 全部钉在 `^0.2.2-rc.3`(`package.json:56-89`)。注意 pre-release 的 caret:它不会自动接受 `0.3.x`,但下一个 rc 一旦改动同样的接口,这五个补丁就要重做一遍——而作者没有承诺跟进。
2. **源码不能在仓外构建**。`devDependencies` 是 `workspace:*`,`pnpm install` 离开 DSH workspace 就失败(`ADAPTATION.md:70-71`);npm 上的宿主包类型又落后(缺 `auth` 字段)。所以**想改一行代码,得先有一份那个 commit 的 DSH 工作区**。提交 `lib/` 解决了"装",没有解决"改"。
3. **`lib/` 与 `src/` 可能悄悄分叉**。`lib/` 仍在 `.gitignore` 里、靠 force-add 跟踪(`ADAPTATION.md:68-69`);作者用"force-add"保证 `pnpm build` 的输出与跟踪副本不漂移,但这只是约定,不是机制。本页没有核对两者的字节一致性。
4. **"能装"不等于"能用"**。唯一的实际运行证据在 rc.1:`stage4-install-and-run.md:49-70` 记录面板 200、`GET /orchestrator/api/state` 200,但 `setup.problem` 是 `repositoryUnset`、`load.running = 0`——**没有仓库、没有工单、没有 worker 启动**。rc.3 侧只有测试数据,没有实机启动记录;作者 2026-11-19 的 rc.5 PR 也只写到 "installation and profile composition passed",没有工单跑通的记录。作者自己也把"native 宿主在 Windows 上根本起不来"写成等价性的天花板:`ADAPTATION.md:55-58` 说 UI 与持久化的等价是**有条件的**(适配侧真机、原生侧只到测试层),不是双机对比。
5. **审核结论其实没出**。`gate-report-equivalence.md:6` 写的是"L1 完成;L2 等 `native.json`;L3/L4 受 Windows 边界限制。结论:尚无 P0/P1 判定,未出总结论"。而 README 说"Signed review artifacts are in `docs/adaptation`"(`README.md:73`),`ADR-001-test-adaptation.md:3` 的实际状态是"提议;…Chief 和判官尚未签字",且它写的是"适配目标:仅 dsh 0.2.2-rc.1"(`:4`)。**签字这件事没有证据**;这批文档是过程记录,不是批准记录。
6. **数字是新的,清单是旧的**。`ADAPTATION.md:31` 说 `session-history.spec.ts` 有 8 个用例,文件里实际有 15 个(`tests/session-history.spec.ts:23-117`);1213 = 1197 + 15 + 1 恰好对上,说明总数跟着测试增长更新了、那句描述没跟上。这类漂移不影响结论,但说明"证据文件"也需要维护。
7. **与上游同包名同 id**。`name: dsh-superagent`(`package.json:2`)、entry id 不变(`cordis.patch.yml:5-11`),所以它和上游、02-local、03-desktop 在同一 profile 里都互斥。
8. **运维脚本在 Windows 上不可用**。`scripts/dsh-superagent` `import fcntl` 且依赖 tmux,`status` 直接 `ModuleNotFoundError`(`stage4-install-and-run.md:73-76`)——而它适配 Windows 的主要理由之一就是路径。要运维只能走面板与 HTTP。
9. **它没变成产品,但作者在继续推**。上游 issue/PR 关闭,仓库自身 0★、无外部贡献,`private: true`、无 CHANGELOG;唯一的后续是一条**未合并**的 rc.5 PR(#1,2026-11-19,1170/1213、剩余 43 条失败归因于基点)。它更像一份"适配报告 + 可安装快照":快照会停在 rc.3,报告的方法比产物活得久。

## 证据与未验证

**读过**:`ADAPTATION.md`、`README.md`、`package.json`、`cordis.patch.yml`、`src/app/session-history.ts`、`src/app/resources.ts`、`src/app/http.ts`、`src/client/deployment.tsx`、`src/deployment.ts`、`tests/session-history.spec.ts`、`tests/deployment.spec.ts`,以及 `docs/adaptation/` 下 7 份文件(`ADR-001`、`compatibility-checklist`、`g0-native-baseline`、`gate-report-equivalence`、`stage3`、`stage4`、`adaptation.diff`)。与上游 `8c32a9dc` 做了 `diff -rq`(src 5 行、tests 9 行)并逐行读了 5 处 diff;查了 GitHub API(`has_issues: false`、`has_discussions: false`)与 release tarball(HTTP 200)。

**没做**:没有重跑测试或 `tsc`,1213/1168/45 与 42 条失败归因**全部来自作者文档**,未独立复核;没有安装 tarball、没有启动 rc.3 宿主;没有核对 `lib/` 与 `src/` 的字节一致性;没有验证 `auth: 'anonymous'` 在实际宿主上的路由可达性;没有验证 `scripts/dsh-superagent` 在非 Windows 上的行为。**未验证**项按上文标注,不用"应该/大概"补齐。

**复现**:

```sh
git clone https://github.com/DASHAN-0079/dsh-superagent-adapt && cd dsh-superagent-adapt
git checkout 34c21ff
diff -rq /path/to/upstream/src src                 # 5 个文件
diff -rq /path/to/upstream/tests tests             # 9 行
grep -c "  it('" tests/session-history.spec.ts     # 15,而 ADAPTATION.md:31 写 8
curl -s https://api.github.com/repos/deepseek-ai/dsh-superagent-prototype | grep has_issues
```
