---
kind: card
domain: proactive_agent
subcategory: runtime-forks
repo: HiSeax/dsh-windows-superagent
commit: 2f3dd46ee30ff7994f36c7c46410b29d453d5bae
evidence: 3
status: active
asof: 2026-11-25
---

# dsh-windows-superagent — 上游 111 个文件一个不落地搬走、又全部改过,把部署面重写成 Windows + 微信 + 看板

> 证据等级 ★★★(源码级;`HiSeax/dsh-windows-superagent@2f3dd46`)。Windows 上的实际运行**未做**,平台结论只到代码、作者实测声明与 `WINDOWS-ADAPT.md`。
> 星标/forks 是 2026-11-25 GitHub API 实时值。上游基线 `deepseek-ai/dsh-superagent-prototype@8c32a9dc`(0.1.0,schema 11)。

## 它替谁解决什么问题

**一个 Windows 工作站上、只有一个 GitHub 仓库的团队**(README 的 good fit 只承诺 "one repository and one team")。需求本来就长在 issue / PR 评论或群里,他们想让 agent 接单、在自己的目录里干、把 PR 与答复送回原对话——但没人愿意为此维护一台 Linux 机器或 WSL。

现在有三种笨办法,疼点都很具体:

- **上 WSL 或第二台机器**:上游服务脚本是 Python + `fcntl` + `tmux`,worker shim 是 `#!/bin/sh`,`deployment.ts` 只认 `/…` 绝对路径;在 Windows 上装得上、一跑就废(`WINDOWS-ADAPT.md:10-18`)。
- **人肉转述**:issue 里的话由人抄进 DSH 会话,干完再抄回 PR。转述丢上下文,长任务期间也没人知道进行到哪一步。
- **只看终端**:上游的可见面是终端与日志;不坐在那台机器前的人,等于没有可见面。

最疼的通常是**既写代码又要派活的那个人**:他得在 issue、终端、PR 三处来回切,而 agent 卡住时只有他能拍板。

为什么是现在:DSH 0.2 的 profile / bundle patch / client 插槽让第三方插件能只挂自己的行、不改宿主,官方也提供了 `pwsh` 工具与 `dsh plugin … add link:` 的 profile 安装路径——这是它能"打完补丁就挂上去"的前提;剩下的 Windows 路径、进程与服务管理,才由这个仓库自己补。

## 适用面:谁该用、谁别用

**适合**:Windows 工作站、单 GitHub 仓库、一个团队;渠道是 issue/PR、飞书或微信私聊之一;愿意先跑几天 `observe`(只记录"本来会接受什么")再切 `auto`;身边有人能维护 clone + `pnpm build` + 一份 profile patch。

**不适合**:要跨多个仓库编排(README 自己把 multi-repo 列进 not a good fit);需要 OS 级隔离或强合规——worker 以你的 OS 用户执行、无审批,Windows 上 `blockedCommands` 还不生效;要求 `npm install` 一条命令搞定,或不能接受看板 fail-open(宿主升级后 worker 行重新出现,而不是报错)。

**前置条件**:

- DSH 0.2+(作者只在 `0.2.2-rc.3` 实测;`install-windows.ps1` 拒绝 0.1.x),Node ≥18、pnpm、git;
- 一个**专用** profile + 绝对 `stateDir`(没有默认值,漏写不启动);
- 一个 GitHub 机器人账号与 repo scope token;
- 微信渠道要一部手机扫码,且 iLink 只在对方最后一条消息后 24 小时内允许主动推送。

## 业务价值

**能算清的**(动作数或数据可核对):

- **派活少两次转述**:需求从 issue/群进工单、结果再回原对话,中间不需要人抄进抄出;按一天 3 次派活算,省下的是 6 次复制与上下文重建——这是可数的动作数,不是工时。
- **状态可见**:每条工单有自己的 `worker-<id>` 会话与目录,看板一屏给出团队成员与工单分组(含需要人处理的那一栏),长任务不再需要有人守着终端。
- **安装成本**:README 是 6 步(clone/构建 → 建 profile → 挂编排器 → 填 `stateDir` → 挂看板 → 启停检查);tarball 路线因看板缺 `dsh.bundle` 仍要手写一行,不能算"1 步"。
- **采用信号(2026-11-25 读数)**:138★ / 1 fork、0 open issue;6 个 release 集中在 2026-11-18→19 的 34 小时里——证明有人看、有人试,不证明有人在生产里跑。

**只是预期**(推断,没有数据支撑):

- 微信入口可能把"群里随口一句"变成可追踪工单,减少需求漏掉;没有工单量或留存数据。
- 看板可能减少"现在到底在干什么"的追问;README 截图是 fabricated demo,不是使用统计。

**明确不算**:没有 token 成本、没有工时节省、没有并发上限下的真实吞吐——这些不做 ROI 推算。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 / 类目 | `HiSeax/dsh-windows-superagent#dsh-windows-superagent` / workflow([registry](../../../data/plugins/HiSeax__dsh-windows-superagent--packages-dsh-windows-superagent.yml)) |
| 子分类 | `runtime-forks`(D1:整树分叉,同领域模型换部署面) |
| 自述 | GitHub 描述:"Windows-friendly multi-agent orchestration for DSH: WeChat channel, ticket board, policy-driven accept, eval toolchain";`fork: false`——与上游没有 GitHub fork 关系,是**发布快照**式分叉 |
| 星标 / fork | **138★ / 1 fork**;创建 2026-11-18T05:12Z,同日 06:57Z 发 v0.2.1,pushed 2026-11-19T17:37Z |
| 包形态 | monorepo 两个 DSH **bundle**:`dsh-windows-superagent@0.2.6` + `dsh-windows-superagent-board@0.2.6`;都 `private: true`、MIT;**npm 404**,只发 GitHub release tarball |
| 代码规模 | 编排 `src/` **133 文件 / 19,286 行**(`.ts` 114 / 16,078,`.tsx` 18 / 2,826,css 382);看板 `src/` 9 文件 / 3,125 行(TS 992 + web 2,133);spec **78 个**(71 + 7) |
| 宿主钉版 | **23 peer**:21 个 `@deepseek-ai/dsh-* ^0.2.1-alpha.2`、`cordis 4.0.5-alpha.1`、`schemastery 3.18.5-alpha.1`;README 实测 **DSH 0.2.2-rc.3**,安装器拒绝 <0.2 |
| 与上游关系 | 上游 `src/` **111 个文件全部存在**(92 `.ts` + 18 `.tsx` + 1 css),**逐字节相同 0 个**;**+22 个新文件**;schema 停在 **11**(`src/app/migration.ts:20`),不跟多仓迁移 |
| repo@commit | `2f3dd46ee30ff7994f36c7c46410b29d453d5bae`(2026-11-20,+0800) |
| 证据等级 | ★★★ |

## 它到底是什么

**整树分叉,不是薄封装。** 判断不看 README,看文件:上游 `src/` 的 **92 个 `.ts` 源文件 92/92 全在且全部被改**(放大到全部文件类型是 111/111);`diff` 上游 `src/` 与 `packages/dsh-windows-superagent/src/` 得到 111 个同名文件、0 个字节相同、22 个新增(`sources/weixin*` 8 个、`app/board*` 4 个、`app/{team,heartbeat,boot-notice,local-sessions}.ts`、`app/tools/team.ts`、`sources/local*.ts` 5 个)。包名与主 entry id 全部改成 `dsh-windows-superagent-*`(`cordis.patch.yml:5,7,10,14,18`)。

**但 id 并非全改干净。** patch 末尾还插两条 **legacy 别名 preset**(`dsh-superagent-worker` / `dsh-superagent-router`,`cordis.patch.yml:208-383`,代码见 `src/app/sessions.ts:58,281-282`),专门接管改名前的会话;而这两行与上游的 preset entry / config id 同名。所以"与上游并存"只在**不同 profile** 成立,同 profile 会在这两行撞 id(未实测失败形态)。

它保留的是上游的五段管线(`README.en.md:155-171`):

```text
Source(GitHub / 飞书 / 本地会话 / 微信 iLink)
  → Eval(gate:准入表 + accept mode + Mandate)
  → Ticket(原子创建 Ticket + Mandate + Subscription + Assignment + 回执)
  → Executor(一 Ticket 一 worker-<id> 会话与目录,可派生 teammate)
  → Report/Reply(回执/回答/结果/求关注,各按规则回原对话)
```

改的是这条管线的**外部条件**,分四类(`README.en.md:173-192` 的自述,已逐项在代码里找到落点):

1. **OS 层**:盘符/UNC、`PATHEXT`、`pwsh`、`windowsHide`、大小写不敏感、无 tmux/fcntl 的服务管理;
2. **渠道**:微信 iLink 机器人(扫码登录)、本地 DSH 会话;
3. **可见面**:侧栏看板(独立第二个包)+ 主会话里的 grill 卡;
4. **授权工具链**:版本化 Policy、准入表、`off/observe/auto`、Mandate、决定记录与重排队。

**血缘是"分叉的分叉",而且中间那层已经消失。** `README.en.md:177` 把基线写成 `vHao11/dsh-windows-superagent@windows-adapt`(2026-11-05,`b0ca277`);`WINDOWS-ADAPT.md:1-8` 说只取那一支的 Windows 适配、不带它的功能分支。实测该 GitHub 地址 **404**,所以能核对的只有:111/111 文件重叠 + "derived from the upstream research prototype" 的自述 + `WINDOWS-ADAPT.md` 的逐文件改动表。中间层的许可证与改动范围**无法从当前仓库确认**。

## 怎么接进 DSH

**不改任何官方 DSH 文件**,只走三条边(`README.en.md:68-80`):

1. **profile 的 `cordis.patch.yml`**:`insert` 两个插件包的行;bundle 自带的 `cordis.patch.yml` 已经写好 5 条 entry——编排器、GitHub Source、飞书(disabled)、本地会话(disabled)、微信(disabled)(`:5-18`),外加 worker/router 两套 preset 与两条 legacy 别名(`:28-383`);
2. **junction**:`dsh plugin --profile superagent add "link:<repo>/packages/dsh-windows-superagent"`,在 profile 的 `node_modules` 下建目录联接(Windows 上是 junction);
3. **配置**:`config.stateDir` 必须是**绝对路径且必填**(`src/deployment.ts:50`),没有默认值;worker preset 由 bundle 提供,看板是第二个包,要单独 `add` 一次。

安装顺序写在 `README.en.md:212-247`:clone → `pnpm install` → `pnpm --filter … check` → 建 `superagent` profile → 挂编排器 → 填 `stateDir` → 挂看板 → `scripts/dsh-windows-superagent.mjs status`。`scripts/install-windows.ps1:86-92` 会跳过并拒绝低于 0.2 的 `dsh`(0.1.x 没有 `--profile`)。

**看板要单独处理。** v0.2.6 的 release tarball 里,编排包有 `dsh.bundle`,**看板包没有**(只有 `dsh.client`),所以 tarball 安装必须手写一行 `id: superagent-board` 的 insert;HEAD 提交信息正是"board bundle mount until a fixed release ships"。条目的 `tarball` 字段指的是编排包。

## 关键实现

| 模块 | 位置 | 作用 |
|---|---|---|
| Source 契约 | `src/sources/kind.ts`、`registry.ts` | `SourceKind` 声明配置/scope/policy/channel/threadContext;渠道拆 `*-read`/`*-trigger`/`*-channel` |
| 准入/Policy | `src/admission.ts:9`、`src/policy.ts:84` | 准入矩阵(explicit/inferred/ignore);accept mode 默认 **`observe`** |
| 工单 | `src/core/tickets.ts:40,278` | accept 时原子建 Ticket+Mandate+Subscription+Assignment;结束的工单可按未变 Mandate 复活 |
| 执行器 | `src/executor/dsh.ts:25,28,166-169` | `worker-<id>` 会话;prepare 超时 10 分钟;并发满时**给人多留一个 slot** |
| 会话/preset | `src/app/sessions.ts:56,119-127,529-530` | 两套 preset;`SHELL_TOOL` 在 Windows 取 `pwsh`;主会话 `tools.restrict` 保留 `ask_user_question`,worker 没有 |
| Windows 运行时 | `src/deployment.ts:16,103`、`src/infra/commands.ts:72`、`src/app/runtime.ts:68` | `PATHEXT` 解析、`windowsHide`、`waitForStateLock()` 等强杀后的 30s 陈旧锁 |
| 看板 | `packages/dsh-windows-superagent-board/src/{index,server,aggregate,client}.ts` | `/superagent-board` 路由 + iframe 页面 + 两层 fail-open 过滤 |
| 微信 | `src/sources/weixin{,-api,-bot,-config,-media,-qr,-read,-trigger}.ts` | iLink 机器人:扫码登录、长轮询 `getUpdates`、私聊即 Trigger |
| grill | `skills/dsh-windows-superagent-grill/SKILL.md:3,10,33` | 复用官方 `ask_user_question`,把一轮问题做成一张点选卡 |

**数据流(以微信为例)**:`weixin-bot` 长轮询收到消息 → `weixin-trigger` 生成 Trigger(thread = `weixin:<wxid>`,ChannelRef 也指这个私聊,`weixin-trigger.ts:46,48`)→ `sources/registry` 交给 Eval → accept 时 `core/tickets` 原子落库并写回执 → `executor/dsh` 起 `worker-<id>` → 结果按 Source 的 Channel 回同一私聊;需要人拍板的候选卡由 `deliver` 投主会话(`src/app/runtime.ts:194`)。GitHub/飞书/本地会话走同一条管线,差别只在 `*-read` 与 `*-channel`。

**看板的过滤器有两层,都故意 fail-open**(`src/shared/internal-sessions.ts:26-110`、`src/client.ts:13-23`):

- 第一层把 `sessions.list` 的 store 包成代理,给 `worker-*` 行标 `origin: 'subagent'`——宿主侧栏与搜索本来就会隐藏这一类;服务缺失、属性不可重绑、实例被冻结,都只打一条 `console.info` 然后原样放过;
- 第二层是一张静态样式表,按 `[data-row-key^="session:worker-"]` 直接 `display:none`。作者把它写成静态表的原因是宿主侧栏的 FLIP 动画:事后写行内样式会让下方那组先弹一下(`src/client.ts:13-23`、看板 README)。

**服务停止是 fail-closed**:`scripts/dsh-windows-superagent.mjs:174,306` 先核对 PID 的镜像名与命令行,认不出就不 `taskkill /T /F`——Windows 会复用 PID,停错进程比停不掉更糟。

**授权语义没有被改坏**:Policy 变更只给**受影响的活工单**投一条 `policy-changed` Input,不立即撤销已发 Mandate;结束的工单按**未变的 Mandate** 复活而不是重新评估(`docs/002-authorization.md:111-119`、`src/core/tickets.ts:278`);`observe` 默认只记录"本来会接受什么"(`policy.ts:84`)。这三条与上游 `docs/001-domain.md` 的写法一致,是"依赖"与"复刻"的分界。

## 为什么它突出

只用本仓库能证明的东西:

- **分叉密度**:111/111 文件全在、0 个字节相同、+22 文件;同一目录从上游的 15,587 行(111 文件)变成 19,286 行(133 文件),还有 78 个 spec。这不是改两行路径就发版。
- **它补的是 OS 与可见面,不是提示词**。改动落在 `infra/`、`deployment.ts`、`executor/`、`app/sessions.ts`、看板包——这些位置按上游的 Source 契约根本碰不到(`docs/008-cookbook.md` 只开 Source 缝)。所以"整树分叉"在这里是**结构性必需**,不是图省事。
- **它有自证的验收记录**:看板 README 记录了在真实隔离实例(`dsh web --profile boardtest --port 18080`)上验证"真实 worker 会话存在、行不渲染、普通行仍在",脚本与证据跟着一个工单目录走;还记录了"重启后 1–2 分钟白屏"这个已知现象的排查过程(构建时间戳、双环境渲染、`/orchestrator/api/state` 的同源门 403 不是鉴权变化)。
- **声量的形状**:138★ 但只有 1 fork——关注度高,二次开发生态只有这 1 个 fork。6 个 release 集中在 2026-11-18 06:57Z 到 11-19 16:44Z 的 34 小时里(v0.2.1→v0.2.6),说明它是"发布快照"而不是持续发布的产品。
- **它把"人的注意力"当成可见面的一等约束**:人只被叫三次(被问/结果待审/失败),看板不推送"正在进行";动作面窄到只有 stop / retry / unfocus,且带确认(`packages/dsh-windows-superagent-board/src/web/app.js:19-22`、`packages/dsh-windows-superagent/src/app/board-actions.ts:30-40`);发起与授权仍在对话里。主会话另用 `ask_user_question` 把"要你拍板"做成一张点选卡,而不是另造一套 UI。

## 代价与边界

1. **宿主耦合硬**。23 个 peer 钉在 `^0.2.1-alpha.2`,只有 0.2.2-rc.3 被实测;README 自己列了三处升级会断的位置:看板 client bundle、bundle 的 client `inject` 名单、worker preset 的 id。看板还是 fail-open,**断了不报错,只是 worker 行重新出现**。
2. **不能 `npm install`**。两个包都 `private: true`,`npm` 上 404;README 给的安装是 clone+build+`link:`。registry 另给了 release tarball 入口,但看板包缺 `dsh.bundle`,tarball 安装要手写 patch 行。
3. **分叉的分叉 + 上游无版本契约**。中间基线 `vHao11/...@windows-adapt` 已 404,上游本身 `private`、不发 npm,所以"跟上游同步"只能人工 diff 111 个文件;仓库没有 upstream remote,也没有 sync 脚本。
4. **权限边界是明说的**:worker 以操作者 OS 用户执行命令、无审批;Windows 上 `blockedCommands` 不生效(拦截 shim 是 `#!/bin/sh` 脚本),`README.en.md:208-210` 把"不能接受这一点"写进 not a good fit。
5. **单仓单团队**:不支持多仓编排;看板的动作面只有 stop / retry / unfocus,不能改工单内容或 Policy。README.en.md 与看板 `package.json` 仍把面板写成 "read-only"/"skeleton",与 HEAD 的动作路由(`POST /superagent-board/action`)不一致。
6. **发布状态仍有缺口**:HEAD 提交就是"board bundle mount until a fixed release ships";tarball 与树的差异只核到看板缺 `dsh.bundle` 这一处,其它 release 未逐个比对。
7. **微信渠道的硬限制**:iLink 只允许在对方最后一条消息后 **24 小时**内主动推送(`src/sources/weixin.ts:57-61`),超时必须等对方再发;只做一对一私聊,群消息直接丢弃(iLink 发送没有群分支,`weixin-trigger.ts:125`)。图片可收可发(下载、解密、按内容哈希存进 `mediaDir`),媒体目录的清理责任在使用者;文件/视频/未转写语音若取不到内容就不成为 Trigger。
8. **`stateDir` 必填无默认**:profile 的 patch 里漏写就整块不启动——与它的 Windows 绝对路径要求叠加,换机器/换盘符要重填。

## 可信度与复现

**读过**:`README.en.md` / `README.md`、两个 `package.json`、两个 `cordis.patch.yml`、`WINDOWS-ADAPT.md`、看板 README、`docs/001`/`002`/`005`/`006`/`008` 的关键段,以及 `src/{deployment,admission,policy}.ts`、`src/core/tickets.ts`、`src/executor/dsh.ts`、`src/app/{runtime,sessions,migration}.ts`、`src/infra/commands.ts`、`src/sources/weixin{,-trigger}.ts`、看板 `src/{client,index,server,aggregate}.ts` 与 `src/shared/internal-sessions.ts` 的关键段。其余文件(`infra/{paths,environment,health}.ts`、`sources/kind.ts`、`core/intake.ts` 等)按 `WINDOWS-ADAPT.md` 的改动表与 grep 定位,**未逐行读**。
**比过**:与 `upstream/src` 做全量文件集与逐字节比较;数了 spec、peer、行数;拉了 v0.2.6 两个 tarball 核 `dsh` 字段。
**没做**:Windows 实机安装/运行、看板 smoke 在其它宿主版本、微信扫码与媒体解密链路、两个包同 profile 共存、`vHao11` 中间层的许可范围。

```sh
git clone https://github.com/HiSeax/dsh-windows-superagent && cd dsh-windows-superagent
git checkout 2f3dd46
find packages/dsh-windows-superagent/src -type f | wc -l            # → 133
find packages/dsh-windows-superagent/src -name '*.ts' | xargs wc -l | tail -1   # → 16078
find packages -name '*.spec.ts*' | wc -l                            # → 78
python3 -c "import json;print(len(json.load(open('packages/dsh-windows-superagent/package.json'))['peerDependencies']))"  # → 23
# 与上游比:111 个同名文件全在且全部不同(111 differ),另 22 个 Only in
diff -rq /path/to/upstream/src packages/dsh-windows-superagent/src | wc -l        # → 133
diff -rq /path/to/upstream/src packages/dsh-windows-superagent/src | grep -c differ  # → 111
curl -s -o /dev/null -w '%{http_code}\n' https://registry.npmjs.org/dsh-windows-superagent   # → 404
```

## 待验证

1. **Windows 实装**:`install-windows.ps1` 的 profile/junction/stateDir 三步在干净机器上能否一次跑通;失败回滚是什么;`status` 的 0/1/2/3 退出码是否覆盖真实的半启动状态。
2. **看板在其它宿主版本上的行为**:0.2.2-rc.3 之外的宿主改 `sessions.list` 形状时,两层 fail-open 是否真的只退化、不打挂列表;`betterSidebar` 服务缺席时看板 tab 是消失还是报错(看板包没有声明任何 peer)。
3. **与吃同一份 `stateDir`/服务契约的插件共存**:它们按 `orchestrator` 服务或 `stateDir` 找对象,这里 id 已改成 `dsh-windows-superagent-*`;能否互操作、还是会各看各的库,未验证。
4. **上游同步策略**:作者如何跟 `deepseek-ai/dsh-superagent` 的后续提交?没有 upstream remote、没有 sync 脚本,也没有版本映射表。
5. **血缘合规**:`vHao11` 中间层已 404,MIT 声明是否覆盖那一层的改动,无法从当前仓库确认。
6. **微信链路的真实边界**:扫码失败/过期换码、图片解密失败、24 小时窗口外的回复失败,面板上分别显示什么,未实测。

→ 同层其它成员与读法:[runtime-forks/README.md](README.md);逐行材料:[FAQ 深读](../../../_faq_on_digested/02_superagent-dependents/lines/01-windows-hiseax.md)。
