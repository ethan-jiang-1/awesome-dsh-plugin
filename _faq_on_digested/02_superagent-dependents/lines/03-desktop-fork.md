# jinghuaihuaxiang-star/dsh-superagent-desktop — 把 Super-agent 装进你现在开着的那个 profile

> `repo@e2cee41`(2026-11-09 20:12 +0800,提交信息 `release 0.1.3`;1★ / 0 forks,pushed 2026-11-09T12:12Z)。上游 `deepseek-ai/dsh-superagent-prototype@8c32a9dc`(24,570★ / 3,081 forks,API 2026-11-25)。注册表条目 [`jinghuaihuaxiang-star__dsh-superagent-desktop.yml`](../../../data/plugins/jinghuaihuaxiang-star__dsh-superagent-desktop.yml),类目 workflow。证据等级 ★★★(README、`package.json`、`cordis.patch.yml`、与上游的 7 个源文件逐行 diff、npm registry 元数据都读过;**没有**实装运行)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 / 类目 | jinghuaihuaxiang-star/dsh-superagent-desktop / workflow |
| 声量 | 1★ / 0 forks;npm 上 5 个版本,全部发布于 2026-11-09 05:57–12:14 UTC |
| repo@commit | `e2cee41`,HEAD 即 `release 0.1.3` |
| 包形态 | `dsh-superagent-desktop@0.1.3`,**`private: false`**,MIT;npm 可装,latest = 0.1.3,unpacked 1.33 MB,maintainer `jinghuaihuaxiang` |
| 宿主钉版 | 23 个 peer,`^0.2.1-alpha.2 \|\| ^0.2.2-rc.1`;`cordis 4.0.5-alpha.1` 精确钉;`engines.dsh` 同范围(`package.json:56-88`) |
| 与上游的关系 | 整树 D1,但**只动部署面**:7 个 `src` 文件 + `package.json` + `cordis.patch.yml`(14 行)+ README;`docs/`、`SETUP.md`、`examples/`、`locale/`、`tests/` 一字未改 |
| 自述差异 | "desktop-bundle packaging, a default `stateDir`, peer ranges widened to `0.2.x`, Windows compatibility fixes in the host code"(`README.md:68-70`) |
| 复现 | `git clone https://github.com/jinghuaihuaxiang-star/dsh-superagent-desktop && git checkout e2cee41`;`diff -rq ../upstream/src src` 输出 7 行 |

## 影响力

- 数字(GitHub API,2026-11-25):**1★ / 0 fork**,`has_issues: true`,MIT;pushed 2026-11-09T12:12Z,HEAD 就是 `release 0.1.3`;`created_at`、watchers、topics 因 API 限流未读到(未验证)。
- **npm 是这个生态里最硬的采用信号**。`dsh-superagent-desktop` 在 2026-11-09 一天内发了 5 个版本(`0.0.0-stage`、`0.1.0`–`0.1.3`,05:57–12:14 UTC),latest 0.1.3;npm downloads **过去一月 1,753 次、过去一周 380 次**(`api.npmjs.org`,2026-10-26–11-24)。同批的 02 与 04 都是 0。
- 注册表收录:本仓 `data/plugins/jinghuaihuaxiang-star__dsh-superagent-desktop.yml`;条目**不带 tarball 字段**(装的是 npm 包),描述里也只讲功能与依赖(git 2.32+、gh)、**没写 npm 安装方式**——策展与分发是脱节的。
- 被引用/被抄/被讨论:**未见**其它仓库引用、下游依赖或第三方 issue/PR。
- 节奏:5 个版本集中在一天内发完,之后没有更新;0.1.3 之后没有 patch,仓库也没有 CHANGELOG。这是"一次性打包发布",不是持续维护。
- 量纲对比:上游 24,570★ 却不在注册表、不发 npm;它 1★ 却是这批里唯一发了 npm 的。**同一个生态里,"影响力"有星标和下载两种量纲,这一页正好撞上。**
- 判断:**星标几乎为零,安装量是这批里最高的**。1★ 说明它没有社区叙事;1,753 次下载说明确实有人在装——下载含 CI、镜像与重复安装,不能当用户数,但足以否定"1★ = 没人用"。这也是它值得保留的理由:它证明的是**分发路径**,不是设计。

## 1. 它要解决什么问题

上游的部署模型是"给这个 agent 单独一个宿主"。`docs/006-deployment.md:17` 把理由写得很清楚:专用 profile 要和工作的 profile 分开,因为插件会改进程级 `PATH` 与 git 配置,而且它自己的进程需要独立重启与升级。于是安装是一串有先后顺序的手工步骤:从 web 模板建 profile、`dsh plugin --profile superagent add "link:$PWD"`、复制 `examples/profile.cordis.patch.yml` 并替换占位符、给 `stateDir` 一个绝对路径、用 `scripts/dsh-superagent` 在 tmux 里起停(`docs/006-deployment.md:83-95,117`)。

桌面用户的场景恰好相反:DSH 已经开着,模型、插件、会话都在里面;他要的是"侧栏多一个入口",不是"再开一个应用实例"。这条路上有三块硬石头:

1. **`stateDir` 必填**。上游 `Config.stateDir` 是 `.required()`(`upstream src/deployment.ts:16`),漏写就整个插件 invalid config、面板显示没有响应;而 macOS/Linux 用户还得自己找一个绝对路径。
2. **独立 profile + 独立进程**。上游把"隔离"当成前提,代价是第二个端口、第二份凭据、第二个要记得重启的东西,以及一个手抄的 token URL。
3. **POSIX 假设**。`worker-bin` 里的 shim 是 `#!/bin/sh` + `0o755`(`upstream src/infra/environment.ts` 的 `shim()`),Windows 上根本起不来——而 README 说的目标平台正是 Windows 11 桌面(`README.md:9-11`)。

所以它不是"又一个分叉",而是把上游的**部署前提**逐条拆掉:不要独立 profile、不要必填路径、不要 POSIX。

## 2. 它的路径

四步,全部围绕"装进现有 profile":

1. **改名以便分发**。包名 `dsh-superagent-desktop`,`private: false`,`version 0.1.3`(`package.json:2,9-10`)。这是三个分叉里唯一真的发上 npm 的(同批的 local 在 npm 是 404),也正因如此,安装才能写成"Settings → Plugins → Add bundle,输入 `dsh-superagent-desktop`,启用,重启"(`README.md:15-17`)或 `dsh plugin --profile desktop add dsh-superagent-desktop`(`:19-23`)。
2. **保留 entry id,只换实现的包名**。`cordis.patch.yml:5-13` 仍然是 `id: dsh-superagent` / `-github` / `-feishu`,只是 `name:` 指向 `dsh-superagent-desktop`、`dsh-superagent-desktop/github-watch` 等。这个选择很关键:profile 里已有的 `- id: dsh-superagent` 配置块(`stateDir` 覆盖)继续有效,`docs/` 与 `examples/` 原样可用,面板自己的 `/orchestrator/*` 路由前缀也不用动。

   ```yaml
   # 上游                                  # 本仓
   - id: dsh-superagent                    - id: dsh-superagent
     name: dsh-superagent                    name: dsh-superagent-desktop
   - id: dsh-superagent-github             - id: dsh-superagent-github
     name: dsh-superagent/github-watch       name: dsh-superagent-desktop/github-watch
   - id: dsh-superagent-feishu             - id: dsh-superagent-feishu
     name: dsh-superagent/feishu-watch       name: dsh-superagent-desktop/feishu-watch
                                             disabled: true
   ```

   14 行 patch 差异里,实质内容就是这三组 `name` 加飞书默认关闭;preset 段(worker `:20`、router `:125`)与上游一字不差。
3. **`stateDir` 给默认值**。`.required()` 换成 `.default(defaultStateDir())`,默认 `<DSH_HOME>/state/superagent`(`src/deployment.ts:16-19,23`);配套把 `cordis.patch.yml:1-3` 的注释改成"profile 可以覆盖"。
4. **补 Windows 与首次使用**。7 个文件按职责分:平台适配 2 个(`infra/environment.ts` 的 shim/git 来源、`app/sessions.ts` 的 pwsh 与工具白名单)、打包连带 1 个(`infra/paths.ts` 的包根识别)、配置默认值 1 个(`deployment.ts`)、面板新增 1 个(`client/overview.tsx` 的"开始使用"卡),另 2 个是文案与样式(`client/locales.ts`、`client/client.css`)。

**放弃了什么**:放弃了上游"独立 profile"的隔离(见第 4 节),也放弃了"只写文档教你配"的路线——它选择把默认值和 Windows 兼容做进代码。没有证据表明作者考虑过"vendor 内核 + 自己的壳"或"另起进程管生命周期"这两条路;README 只陈述结果,不讨论替代方案。

## 3. 它如何利用 dsh-superagent

**几乎全盘保留。** 领域模型(Ticket/Mandate/Assignment/Subscription/Eval)、`orchestrator.sqlite`、主会话与 worker 会话、两套 preset、面板各页(只多一张"开始使用"卡)全部沿用;`tests/` 一个文件没动,`docs/001`~`008` 与上游逐字节相同。也就是说:这一页的"依赖"不是"用了哪个函数",而是**整棵树 + 同一套 entry id**。

改动可以逐处指出来:

- **路径根不再假设包名**:`packageRoot()` 原来只认 `package.json.name === 'dsh-superagent'`,改名后会在自己的仓库里找不到根;现在接受 `{dsh-superagent-desktop, dsh-superagent}` 两个名字(`src/infra/paths.ts:6,16-25`)。这是"改名"最容易被忽略的连锁反应。
- **shim 分平台**:Windows 只写 `<name>.cmd`,首行 `@REM` 而不是 `#`(cmd 会把 `#` 当语法错),内容 `@echo off` + 绝对路径调用 + `exit /b %ERRORLEVEL%`;marker 匹配时先剥掉 `@REM `/`:: `(`src/infra/environment.ts:16,62-66,84-105`)。git 配置来源比对也把反斜杠折成正斜杠,否则 `git config --show-origin` 的 `file:C:/…` 与 `join()` 出来的 `C:\…` 永远不相等,会误报 `gitTooOld`(`:145-150`)。
- **pwsh 与工具白名单**:主会话的 `noWait` 守卫加上 `pwsh`(`src/app/sessions.ts:79`);`tools.restrict` 的 allow 列表同时列 `bash` 与 `pwsh`,再按宿主实际注册的工具过滤,因为 restrict 拒绝未知名字(`sessions.ts:262-266`)。
- **面板**:侧栏入口走官方插槽 `sidebar.panellist`(`src/client/index.tsx:49-57`),不是 DOM 注入;概览加一张"开始使用"三步卡(打开主会话 / 去来源 / 去执行),只在"没有流量、没有待办、没有 setup 问题"时出现(`src/client/overview.tsx:61-83,104`)。

## 4. 技术思考

**分发是这一页真正的技术判断。** 上游自己 `private: true`、不在 npm,所以分叉们只能靠 `link:`、git 或 release tarball 安装;而 DSH 的"Add bundle"入口是按包名去 registry 取的。把 `private` 翻成 `false` 并起一个不撞车的包名,等于把"安装"从"读文档 + 敲六条命令"降成"填一个包名"。这是它 1★ 却值得单独一页的原因:它验证了 bundle 分发的另一条路。

**id 不变、包名变,是刻意的兼容层。** 因为 entry id 仍是 `dsh-superagent`,profile 里原来的配置块、`docs/006` 的示例、`/orchestrator/api/*` 的路径、`stateDir` 的键名全部继续成立;换掉的只有"这个 id 指向哪个包"。代价是它和上游、和 02-local **在同一个 profile 里互斥**:一个 loader 里不能有两个 `dsh-superagent` entry。这一点比包名冲突更硬——包名不同可以并存于 `node_modules`,id 相同不行。

**`stateDir` 默认值把隔离换成了方便。** 默认值是 `<DSH_HOME>/state/superagent`,**按 DSH_HOME 而不是按 profile**,所以同一台机器上所有 profile 共享一个状态目录。上游用 `proper-lockfile` 锁住这个目录(`src/app/runtime.ts:93`),第二个宿主拿不到锁;README 因此专门写了一句"两个宿主进程不能共用一个 state 目录"(`README.md:33-35`)。换句话说:默认值让首次安装零配置,但把"多开"变成了一种要人工改配置才能做的事。

**环境注入从"隔离进程"漏进了"你的进程"。** `applyEnvironment` 是把 worker 变量写进 `process.env` 的:`PATH` 前面插 `worker-bin`、`GIT_CONFIG_GLOBAL` 指向 worker gitconfig、清掉 `GH_TOKEN`/`GITHUB_TOKEN`。上游要求独立 profile,正是为了让这些改动只影响那个进程(`docs/006-deployment.md:17`)。装进你自己的 profile 之后,**你日常会话里的 `PATH` 与 git 配置也会被这套值覆盖**。同批的 02-local 在自己的 `docs/006` 里补了一节 "The worker environment",把这件事写明了,而 desktop 的 `docs/` 一字未改——这是它最实质的一处"没说的代价"。

**Windows 适配是补丁式的,不是重构。** 它没有动 `Commands`/`Deployment` 的结构,只在写 shim、找包根、注册工具、比对 git 来源这四处按平台分叉。好处是 diff 小、可对照;坏处是平台判断散落在各模块里(`process.platform === 'win32'` 出现在 `environment.ts`、`cordis.patch.yml` 的 `!!js` 表达式里),没有单一的"平台层"。

**peer 放宽是声明,不是验证。** 23 个 peer 从 `^0.2.1-alpha.2` 放宽到 `^0.2.1-alpha.2 || ^0.2.2-rc.1`,但 `cordis` 仍精确钉在 `4.0.5-alpha.1`、`schemastery` 精确钉在 `3.18.5-alpha.1`。所以"支持 0.2.x"实际是"支持两个 pre-release 世代,且宿主必须带这两个精确版本";README 也只在 desktop `0.2.2-rc.1` + Windows 11 上测过(`README.md:11`)。

**它没有碰的那些假设。** 仍然是"一个 GitHub 仓库"(README 第 5 行的产品描述与上游相同)、仍然是 GitHub/飞书两个 Source、仍然只有单团队单仓策略、worker 仍然以操作者身份无审批执行。它改的是**装在哪、默认值是多少、Windows 上能不能起**,不是**谁能派活、活落在哪**——后者是 02-local 与 05-multi-repo 各自去解的问题。这一点让它的 diff 只有 7 个文件,也让它的适用面止步于"上游本来就能用、只是装起来麻烦"的人。

## 界面体验

- **入口**:装进现有 profile 后,侧栏面板列表里多一个锤子图标(`src/client/index.tsx:55`——`sidebar.panellist` 插槽,与上游同一注册点,本仓未改),重启后出现(`README.md:31`),点开是整页管理面板。同一个注册还在插件管理里给一张配置卡(`:56-57`)。
- **首次打开**:概览顶部多一张"开始使用"三步卡——打开主会话 / 去来源 / 去执行(`src/client/overview.tsx:61-83`),只在"没有流量、没有待办、没有 setup 问题"时出现(`:104`),一有工单就消失。这是它**唯一新增**的界面元素。
- **会话**:不隐藏 `worker-*` 与 `orchestrator-*`(`src/client/index.tsx` 里没有收起逻辑)。装进自己的 profile 之后,主会话、执行器会话与你的工作会话共用一个侧栏——这是与 02-local 最直观的差别(后者把系统会话全收起,只留 M 气泡)。
- **面板**:上游六页——概览 / 来源 / 触发 / 评估 / 执行 / 设置(`docs/005-panel.md:15-24`),表格密集、详情在右栏;概览首屏是待人工决定、系统问题、24 小时流量、执行器负载(`:19`)。
- **实时性**:面板每 5 秒拉 `GET state`,重启中 1 秒(`src/client/provider.tsx:74,89`);侧栏没有额外注入,所以没有 02-local 那种"新入口要等 3 秒"的延迟。
- **失败时**:部署检查失败在概览显示问题行并链到设置;机器配置表单在宿主拒绝写入时只读(`src/client/deployment.tsx:36,49-54`);管理 API 只接受同源 + `x-orchestrator-request` 的请求,否则 403(`src/app/http.ts:74-78`)。终端侧 `scripts/dsh-superagent status` 仍是 POSIX-only(`docs/006-deployment.md:117`),Windows 用户实际只有面板可用(`README.md:66`)。

## 用户交互的思路

- **谁发起**:装好之后,人在**自己的** profile 里打开主会话直接说任务;也可以照旧在 GitHub issue/飞书里 @ 机器人——"开始使用"的三步文案把这两条并列(`src/client/locales.ts:103-104`)。
- **在哪确认**:没有"提交"动作。主会话把话变成工单,人第一次看到它是在面板的"执行"页——第三步文案就是"任务跑起来后,在「执行」看进度"(`locales.ts:105`);这与上游"回执发回 issue"不同,**回执在你自己的会话里**。
- **怎么观察**:面板 5 秒轮询;或回主会话读 relay/notice(上游机制未改);worker 会话就在侧栏里,可以直接点进去插话。
- **怎么打断**:工单页的危险区有 stop 与 retry(`src/client/ticket.tsx:192-194`、`:131-133`),也可以在主会话里说停;worker 会话里直接插话同样有效。
- **与上游的差异**:上游要你切到一个独立 profile/进程,交互面在"另一个窗口 + 外部渠道";这里入口就在你正在用的侧栏里,发起、观察、打断同屏完成。代价是**没有隔离**:系统会话、worker 会话、系统提示与你的工作混在一个列表,进程级环境注入也落在同一个宿主。
- 一句话:**它把 Super-agent 从"另一个 app"变成"侧栏里的一个面板"**——交互本身没变,变的是距离。

## 5. 代价与边界

1. **与上游/02-local 互斥**:id `dsh-superagent`、`-github`、`-feishu` 相同(`cordis.patch.yml:5-13`)。想两个都试,只能开两个 profile,而两个 profile 又会在默认 `stateDir` 上抢锁。
2. **默认状态目录是全局的**:`<DSH_HOME>/state/superagent`,不区分 profile(`deployment.ts:16-19`)。桌面 app 与 CLI 同时跑、都用默认值时,第二个会因目录锁起不来;要并存必须显式改 `stateDir`。
3. **环境注入影响整个宿主进程**:`PATH`、`GIT_CONFIG_GLOBAL`、清空 token 变量;上游靠独立 profile 规避,这一支没有。
4. **文档没跟着改**:`docs/006-deployment.md:95` 仍写 `stateDir | yes`;`examples/profile.cordis.patch.yml` 仍是 `<absolute path>` 占位;`SETUP.md` 仍在问"哪个 github.com 仓库"、仍教建 `superagent` profile。bundle 自带的说明书和它的卖点互相矛盾,照着做会绕回上游那套部署。
5. **在最想要的平台上没有测试证据**:`tests/` 未改,README 自己说测试套件假设 POSIX(`sleep`/`ps`),Windows 上 `pnpm test` 的失败来自平台;验证方式是"跑起来的宿主里的面板与 API"(`README.md:58-66`)。
6. **权限边界没变**:worker 以操作者 OS 用户执行命令、无审批(`docs/003-execution.md:27`);`blockedCommands` 只是 `worker-bin` 里的同名 shim,按绝对路径可绕过(`docs/003-execution.md:80`)。装在你每天用的 profile 里,这条比以前更贴近人。
7. **维护面薄**:1★、0 fork,5 个 npm 版本集中在一天内发完(2026-11-09),维护者是个人邮箱;升级路径是"更新包 + 重启宿主"(`README.md:56`),没有 CHANGELOG、没有 upstream remote。
8. **只适配一个桌面世代**:目标写的是 desktop `0.2.2-rc.1`,cordis 精确钉死;宿主换 cordis 版本就得重新出包。

## 证据与未验证

**读过**:`README.md`、`package.json`(与 npm registry 的 0.1.3 元数据对齐)、`cordis.patch.yml`、与上游 `src/` 的逐文件 diff(`sessions.ts`、`deployment.ts`、`infra/paths.ts`、`infra/environment.ts`、`client/index.tsx`、`client/overview.tsx`、`client/locales.ts`、`client/client.css`)、上游 `docs/006-deployment.md`、上游与本仓的 `examples/`、`SETUP.md`。

**没做**:没有真的 `dsh plugin add dsh-superagent-desktop` 安装、没有启动面板、没有跑 worker;没有验证两个 profile 共用默认 `stateDir` 时的具体报错文案(只知道有目录锁);没有验证 `cordis 4.0.5-alpha.1` 与宿主实际版本的匹配;没有验证 peer 放宽后在 `0.2.2-rc.2+` 上是否真能加载。**未验证**项不替作者补理由。

**复现**:

```sh
git clone https://github.com/jinghuaihuaxiang-star/dsh-superagent-desktop && cd dsh-superagent-desktop
git checkout e2cee41
diff -rq /path/to/upstream/src src          # 7 个文件
diff /path/to/upstream/cordis.patch.yml cordis.patch.yml | wc -l   # 14
curl -s https://registry.npmjs.org/dsh-superagent-desktop | head -c 200
```
