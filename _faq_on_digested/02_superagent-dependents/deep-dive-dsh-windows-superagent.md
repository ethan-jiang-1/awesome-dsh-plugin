# HiSeax/dsh-windows-superagent — 16k 行的 Windows 分叉,给 Super-agent 补上微信与一块看板

> `repo@2f3dd46`(2026-11-20;138★ / 1 fork)。上游 `deepseek-ai/dsh-superagent-prototype@8c32a9dc`(24,565★ / 3,081 forks,2026-11-25)。注册表条目 [`HiSeax__dsh-windows-superagent--packages-dsh-windows-superagent.yml`](../../data/plugins/HiSeax__dsh-windows-superagent--packages-dsh-windows-superagent.yml),类目 workflow。证据等级 ★★★(读了 README、两个 `package.json`、`cordis.patch.yml`、源码树并与上游逐文件比对;**没有**在 Windows 上实装运行)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 / 类目 | HiSeax/dsh-windows-superagent#dsh-windows-superagent / workflow |
| 自述 | "DeepSeek Harness team 的 dsh-superagent 研究原型的桌面 bundle 分支"——实际是 Windows 发布快照,不是 GitHub fork 关系 |
| 声量 | **138★ / 1 fork**,pushed 2026-11-20(实时值,非冻结边车) |
| 包形态 | monorepo 两个 DSH 插件:`dsh-windows-superagent@0.2.6`(编排)+ `dsh-windows-superagent-board@0.2.6`(看板);均 `private: true`,MIT,不发 npm |
| 代码规模 | 编排包 `src/` **114 个 TS 文件 / 16,078 行**;看板包 **992 行**;测试 **65 个文件** |
| 宿主钉版 | 23 个 peer,`@deepseek-ai/dsh-* ^0.2.1-alpha.2`、`@deepseek-ai/cordis 4.0.5-alpha.1`;README 实测 DSH **0.2.2-rc.3** |
| 与上游关系 | 上游 `src/` **92 个文件全部存在、全部有改动**(抽样:`sources/github.ts` 920 行 diff、`limits.ts` 22 行、`kv.ts` 15 行),另加 **22 个新文件** |
| 复现 | `git clone https://github.com/HiSeax/dsh-windows-superagent && git checkout 2f3dd46`;`diff -rq` 对照上游 |

## 它到底是什么

**不是薄封装,是深分叉。** 上游 `dsh-superagent` 的 92 个源文件一个不少地搬了过来,而且每一个都有实质改动;新增的 22 个文件集中在 `app/`(看板、团队、本地会话、心跳)与 `sources/weixin*`。包名与 plugin id 全部改成 `dsh-windows-superagent-*`(上游是 `dsh-superagent-*`),所以两者理论上可以在同一宿主的不同 profile 里并存。

它继承的是上游的五段管线:

```text
Source(GitHub / 飞书 / 本地会话 / 微信 iLink)
  → Eval(gate + assessment:准入表 + accept mode + Mandate)
  → Ticket(原子创建 Ticket + Mandate + Subscription + Assignment + 回执)
  → Executor(每条 Ticket 一个 worker-<id> 会话与目录,可再派生 teammate)
  → Report/Reply(回执、回答、结果、求关注,各按规则回原对话)
```

在这条管线上,它加了四类东西(见 `README.en.md:173-190` 的对照表):

1. **Windows 适配**:盘符/UNC 路径、`PATHEXT`、`pwsh` 工具、`windowsHide`、大小写不敏感路径、`waitForStateLock()`、无 tmux/fcntl 的服务管理;
2. **新渠道**:微信(iLink 机器人,扫码绑定)、本地 DSH 会话(不用 GitHub 也能派活);
3. **人的界面**:侧栏看板(只读面板,按 `worker-*` 会话过滤)+ 主会话里的 grill 问题卡(复用官方 `ask_user_question`);
4. **授权与评估工具链**:版本化 Policy、准入表、`off/observe/auto` 三档、Mandate、决定记录与重排队。

血缘上它是**分叉的分叉**:README 把 Windows 基线指向 `vHao11/dsh-windows-superagent@windows-adapt`,而该仓库在 2026-11-25 已 **404**;能直接核对的只有它与 `deepseek-ai/dsh-superagent` 的 92/92 文件重叠与"derived from the upstream research prototype"的自述。

## 怎么接进 DSH

它**不改任何官方 DSH 文件**,只通过三条边挂进去(`README.en.md` 的 "Dependency boundary"):

1. **独立 profile**:建一个 `superagent` profile,在它的 `cordis.patch.yml` 里 `insert` 两个包的行;
2. **junction**:`dsh plugin --profile superagent add "link:<本仓库路径>"` 在 profile 的 `node_modules` 下建目录联接(Windows 上是 junction);
3. **配置**:profile 里给 `config.stateDir` 一个绝对路径(Windows 路径);worker preset 由包内 `cordis.patch.yml` 提供;看板作为第二个包单独 mount。

安装前置写在 `README.en.md:212-248`:clone → 构建 → 建 profile → mount orchestrator → 设 `stateDir` → mount board → 启动检查。`scripts/install-windows.ps1` 会拒绝低于 0.2 的 `dsh`(0.1.x 没有 `--profile`)。

## 关键实现

### 1. Source 层:渠道是可插拔的

`sources/kind.ts` 定义 `SourceKind`(配置、scope、policy、channel、threadContext),`sources/registry.ts` 负责注册;每个渠道拆成 `*-read`(读事件)、`*-trigger`(翻译成 Trigger)、`*-channel`(回写)。GitHub、飞书、本地会话、微信四套并列,微信又拆成 `weixin-api/bot/config/media/qr` 五个文件。**换渠道不需要改 Router**——这是上游领域模型真正的复用点。

### 2. Eval 与 Policy:授权留在域内

`admission.ts` + `policy.ts` + `app/assessment.ts`:准入表按"接收 scope"决定一条人类消息是 explicit 还是 candidate;`off/observe/auto` 三档决定"记录 / 只判定 / 按规则执行";accept 时原子创建 Ticket、Mandate、Subscription、Assignment 与回执。**Mandate 不可变**,Policy 变更只投递给活着的 Assignment,不撤销已发 Mandate——这条与上游 `docs/001-domain.md` 一致,是它没有改坏的部分。

### 3. Ticket 与 Executor:一 Ticket 一会话一目录

`core/tickets.ts` 与 `executor/dsh.ts`:每条 Ticket 建 `worker-<ticketId>` 会话与一个以短名命名的目录;首次执行前跑一次 prepare 命令(通常是 `git worktree`),超时十分钟;并发有 worker slot 上限,但给人留一个额外 slot,所以人不会被自己的队列堵住。Ticket 状态不跟随 DSH 会话(`person/working/idle` 六阶段),会话可换、工单不丢。

### 4. Windows 适配:不是换壳,是改运行时

`infra/paths.ts`、`infra/environment.ts`、`infra/commands.ts`、`infra/health.ts`、`deployment.ts` 承担了盘符/UNC、`PATHEXT`、`pwsh`、`windowsHide`、路径大小写与服务生命周期;服务停止前先按 PID 身份校验再 `taskkill /T /F`(fail-closed),避免杀错进程。README 的 "not a good fit" 也承认:**worker 以你的 OS 用户执行命令,Windows 上 `blockedCommands` 对 worker 不生效**。

### 5. 看板:独立 client 插件

`packages/dsh-windows-superagent-board`(992 行)是第二个 DSH 插件:注册自己的侧栏入口与主面板,通过宿主 client 模块(`@deepseek-ai/dsh-client-*`)读会话列表,并把 `worker-*` 行过滤掉。README 明确它的失败模式是 **fail-open**:宿主改了 `sessions` 服务的 store 形状,worker 行会重新出现,而不是把列表打挂。

### 6. 微信与 grill 卡

微信走 iLink 机器人:设置页扫码绑定,私聊消息由 `weixin-trigger.ts` 翻译成 Trigger,结果回到同一聊天;只支持纯文本一对一。grill 卡不是自绘 UI,而是复用官方 `ask_user_question`,把"需要你拍板"变成主会话里的一张点选卡。

## 为什么它突出

- **它是依赖者里唯一过百星的**(138★;第二名的真依赖是 local 的 11★)。在一圈个位数分叉里,这个量级说明它至少被一部分人当成"能跑起来的 Windows 版"。
- **它补的是上游明确不覆盖的面**:上游 README 自己说 prototype 面向团队仓库、Unix 实践;HiSeax 把"Windows + 微信 + 看板"做成了发布快照。
- **分叉密度高**:92/92 文件全改、+22 文件、16k 行、65 个测试文件——不是改两行路径就发版的玩票。
- **它没有改设计**:五段管线、Mandate、Subscription 语义与上游一致;新增的是部署面(OS、渠道、面板)。这正是"依赖"与"复刻"的分界。

## 代价与边界

1. **宿主耦合硬**:23 个 peer 钉在 `^0.2.1-alpha.2`,README 只在 `0.2.2-rc.3` 上实测。DSH 升级后看板 client bundle、worker preset、client inject 三处都可能断;看板还是 fail-open,断了不报错、只是过滤失效。
2. **不能 `npm install`**:两个包都 `private: true`,没有 npm 发布;安装要 clone + build + `link:` junction。对普通用户,这是一条有门槛的路径。
3. **分叉的分叉**:Windows 基线 `vHao11/dsh-windows-superagent@windows-adapt` 已 404;上游本身没有版本契约(`private`,无 npm),所以"跟上游同步"只能人工 diff 92 个文件。
4. **权限边界**:worker 以 OS 用户跑命令、无审批;Windows 上 `blockedCommands` 不生效。README 自己把"不能接受这一点"列为不适合使用的条件。
5. **单仓单团队**:不支持多仓编排(ctrl439 才做多仓);看板只读,不能从面板改工单。
6. **发布状态**:最新提交还在说"board bundle mount until a fixed release ships",说明打包/挂载仍有已知缺口。

## 可信度与复现

- **读过**:`README.en.md` / `README.md`、两个 `package.json`、`packages/dsh-windows-superagent/cordis.patch.yml`、`src/` 目录与关键文件(`admission.ts`、`policy.ts`、`core/tickets.ts`、`executor/dsh.ts`、`sources/weixin*.ts`、`infra/environment.ts`)、看板 `src/` 清单、上游 `docs/001-003`。
- **比过**:上游 `src/` 92 个文件与 HiSeax 同名文件逐个 `cmp`,全部不同;抽样 diff 行数;新增 22 个文件;测试文件 65 个;peer 23 条。
- **没做**:Windows 实机安装/运行、看板 smoke、微信扫码链路、与上游同 profile 共存、`vHao11` 中间层的许可证与改动范围。
- **复现**:
  ```sh
  git clone https://github.com/HiSeax/dsh-windows-superagent && cd dsh-windows-superagent
  git checkout 2f3dd46
  cat packages/dsh-windows-superagent/package.json
  diff -rq ../dsh-superagent/src packages/dsh-windows-superagent/src | wc -l
  find packages/dsh-windows-superagent/src -name '*.ts' | wc -l
  ```

## 待验证

1. **Windows 实装**:`install-windows.ps1` 的 profile/junction/stateDir 三步在干净机器上能否一次跑通;失败时的回滚是什么。
2. **看板 smoke**:`pnpm --filter dsh-windows-superagent-board smoke` 在 0.2.2-rc.3 之外的宿主上是否仍能过滤 worker 行。
3. **与上游/其他契约插件共存**:trace 与 wechat-source 找的是 `orchestrator` 服务与 `stateDir`;HiSeax 的 id 已改成 `dsh-windows-superagent-*`,两者能否互操作未验证。
4. **上游同步策略**:作者如何跟 `deepseek-ai/dsh-superagent` 的后续提交?仓库没有 upstream remote、没有 sync 脚本说明。
5. **血缘合规**:`vHao11` 中间层已 404;MIT 版权声明是否覆盖那一层的改动,无法从当前仓库确认。
