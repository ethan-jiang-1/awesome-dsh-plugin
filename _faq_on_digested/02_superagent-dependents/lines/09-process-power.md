# MingoYung/dsh-superagent-power — 输入栏一个 Sup 开关,管的是另一个 profile 的进程

> `MingoYung/dsh-superagent-power@be94341`(0★,MIT,`@local/superagent-power@0.1.1`)。上游 `deepseek-ai/dsh-superagent-prototype@8c32a9dc`(24,565★)。注册表条目 [`MingoYung__dsh-superagent-power.yml`](../../../data/plugins/MingoYung__dsh-superagent-power.yml),类目 **ui**。证据等级 ★★★:读全 6 个 JS/JSX(495 行)、`docs/{design,installation,verification}.md`、两个 example patch、`package.json` 与 CI 测试;**没有**在 Windows 上实机点过开关。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 / 类目 | MingoYung/dsh-superagent-power / **ui** |
| 自述 | "在 DSH 会话输入栏按需开启、关闭 Super-agent 后台,避免不使用时仍长期占用系统内存";"面向 **Windows / DSH NEXT** 的社区插件"(`README:1-10`) |
| 声量 | 0★(2026-11-25 实时值) |
| 包形态 | `@local/superagent-power@0.1.1`,**未发 npm**(`docs/installation.md:24`),走 GitHub Releases 的 `.tgz`;`exports` 同时给出 `./bridge`(`package.json`) |
| 两半 | 桌面 profile:`index.js`(宿主)+ `client.jsx`(输入栏);Super-agent profile:`bridge.js`(伴随模块,同进程) |
| 代码规模 | 6 个文件 / 495 行:controller 190、client 141、bridge 77、transport 41、index 35、remote 11;测试 3 个 / 181 行 |
| 宿主钉版 | `engines.dsh = 0.2.1-rc.4 \|\| 0.2.1-rc.5 \|\| 0.2.2-rc.1`;Node ≥24;peer `@deepseek-ai/dsh-typert-protocol` 同区间 |
| 平台 | 默认 `nodePath: C:/Program Files/nodejs/node.exe`、`port: 3082`;macOS/Linux 未验收(`README:102`) |
| 控制面 | 命名管道 `\\.\pipe\dsh-sa-<sha256(home\|profile)[0:24]>-{worker,owner}`;非 Windows 落 `<home>/sa-<id>-worker.sock`(`transport.js:5-9`) |
| 鉴权 | `DSH_HOME/plugins/superagent-power/control.key`:32 字节 hex(64 字符)、0600、`wx` 独占创建;恒定时间比较(`controller.js:33-46`,`transport.js:10-14`) |
| 状态 | `state.json` 只存 `{version:1,enabled}`,临时文件 + rename 原子替换(`controller.js:14-19,70`) |
| 观测量 | 单次本机验收:RSS ≈468 MB;启动 ≈7.3–13.2 s,关闭 ≈0.2 s(`docs/verification.md:9,36,39`) |

## 影响力

- **0★ / 0 fork / 0 issue / 0 watcher**(GitHub API,2026-11-26 取);2026-11-02 建仓,最后一次 push **2026-11-05**。本地浅克隆只能看到 1 个提交(`be94341`),完整历史未取。
- 注册表位置:[`data/plugins/MingoYung__dsh-superagent-power.yml`](../../../data/plugins/MingoYung__dsh-superagent-power.yml),类目 **ui**;条目里的 tarball 指向 `v0.1.0`,仓库已到 `0.1.1`。
- npm:**未发布**。`@local/superagent-power` 在 registry 返回 404(`docs/installation.md:24` 也自述"没有发布到 npm registry")。
- 分发证据只有 GitHub Releases:`v0.1.0` 的 `local-superagent-power-0.1.0.tgz` **743 次下载**、`v0.1.1` 的 **42 次**(API 实时值)。这是三条里唯一**发布物级**的下载计数(07/08 只有 npm 包计数),0★、0 fork 也有人取。
- 判断:**影响力 = 小,但"实际分发"最强**。代价是没有 issue 通道:兼容性问题只能靠作者自己的 `docs/verification.md` 记录,外部反馈进不来。
- 一个反向指标:743 次下载与 0 issue 并存,而 README 反复强调"只安装桌面包并不能完成整套安装"(`README:69`)——**下载量不能读成安装完成量**,它有两处必装、三处路径必须一致。

## 一、要解决什么问题:上游没有"不值守"这个状态

上游是**常驻主动代理**:等事件本身就是功能——Source 按订阅轮询、后台工作有 30 分钟上限、暂停只停派发不停进程(`上游 docs/003-execution.md:192-200`)。它没有"停机保状态"的档位,也不该有:一旦停了,等 GitHub/飞书事件这件事就断了。

真正的缺口是**运行形态**:

- Super-agent 必须跑在**自己的 profile 进程**里(独立 CLI);DSH 桌面端的 slot、Remote、权限模型都只覆盖自己这个进程,管不到另一个进程的生死。
- 而这个后台是**一个进程服务多个会话**。如果开关做成会话级,A 会话开、B 会话关,就会互相覆盖并给出误导状态(`README:24-28`)——所以键必须是 `DSH_HOME + profile`。
- 内存是唯一的量化理由:一次本机观测里,后台主进程 RSS 约 468 MB;关掉,进程真的退出(`docs/verification.md:39`)。作者特意写明"这不是所有机器都能省 468 MB 的承诺"(`README:22`)。

所以它补的不是"进程管理",而是**"要不要现在值守"这个显式选择**,并且放在每天都会经过的位置(输入栏)。

## 二、路径:为什么必须是插件,而不是一个脚本

这几乎是全部 D2 里"必须做成插件"最硬的一条,五个理由都能落到代码:

1. **入口只有插件有**。按钮挂在原生 slot `conversation.input.left`、order 71(`client.jsx:138`);脚本无法进入 composer 工具区。
2. **权限走宿主的通道**。状态通过 typert Remote 暴露:`TypertRemoteService` + `ctx.typert.register` 声明 `get/set` 两个方法(`index.js:10-33`,`remote.js:3-11`),浏览器经宿主 Gateway 调用。脚本要自建 HTTP 与鉴权,等于把宿主已有的权限模型复制一遍(`docs/design.md:60`)。
3. **优雅退出只能在进程内做**。`bridge.js` 先 `await runtime.stop()`,再 `ctx.appExit(0)`(`bridge.js:23-37`);`appExit` 是 CLI 提供的服务(本机 DSH 安装里 `@deepseek-ai/dsh-cmdline/lib/index.js:30` 的 `ctx.provide("appExit", host.exit)`)。外部脚本能做的只有 kill,拿不到"任务取消、会话落盘、SQLite 关闭、目录锁释放"这条路径。
4. **单控制者需要一个确定的生命周期钩子**。每个 `DSH_HOME/profile` 只能有一个控制者(owner 管道,第二个 `listen` 失败即拒绝加载,`controller.js:47-52`);插件的 `ctx.effect` 正好提供"卸载时释放"(`index.js:27`)。
5. **两半要一起发版**。桌面半与伴随半在同一个包里,靠两个 profile 的 patch 各自 mount;伴随半的 `name` 直接写 `bridge.js` 的绝对路径(`examples/superagent.patch.example.yml:3-9`)。

反过来,脚本方案还漏掉一件事:**活跃任务数**。判断"能不能关"要读 `executor.activeCount()` 与主控会话状态(`bridge.js:18-19`),这只有进程内的服务能给。

## 三、它如何利用 dsh-superagent(逐点对位)

| 触点 | 上游 / 宿主落点 | 本仓落点 |
|------|------------------|----------|
| `orchestrator` 服务 | `Runtime extends Service`,`super(ctx,'orchestrator')`(`上游 src/app/runtime.ts:88`) | `inject = ['orchestrator','agents','appExit']`(`bridge.js:7`) |
| `runtime.ready` | `readonly ready: Promise<void>`(`runtime.ts:73`) | `await runtime.ready` 后再开管道(`bridge.js:11`) |
| `runtime.masterId` | 主控会话 id(`runtime.ts:76`,赋值 `:104`) | 用来取主控 agent(`bridge.js:18`) |
| 活跃任务数 | `DshExecutor.activeCount()` = 打开的工单 ∩ running(`上游 src/executor/dsh.ts:404`) | `runtime.executor.activeCount()`(`bridge.js:19`) |
| 主控忙不忙 | `ctx.agents.get(id).status`(上游 `src/app/sessions.ts:115` 同款调用) | `master.status !== 'idle'` 计入 active(`bridge.js:18-19`) |
| 配置完成没 | `configured()`(`runtime.ts:179`) | `runtime.configured()` → 面板"业务配置仍需完成"(`bridge.js:21`,`client.jsx:124`) |
| 正常收尾 | `stop()`(`runtime.ts:229`;上游卸载时同一条路径 `src/index.ts:22`) | `await runtime.stop()`(`bridge.js:29`) |
| 退出 | CLI 提供的 `appExit` | `ctx.appExit(0)` + `process.disconnect()`(`bridge.js:34-35`) |
| profile 身份 | CLI `--profile <name>`(上游不认识"桌面") | `spawn(node, [cli,'--profile',name,'--no-open'])`(`controller.js:130`) |
| 双方一致的键 | 无 | `homePath` + `profileName` → 管道名(`transport.js:5-9`);`keyFile` 两端同读(`controller.js:34`,`bridge.js:12-13`) |
| 管理页 | 后台自己的 webserver 端口 | 只用于占用检查与"打开后台"链接(`controller.js:20-27,122`;`client.jsx:128`) |

**注意它完全不碰 `stateDir`、`orchestrator.sqlite`**。这是 D2 里另一种吃法:吃的是 **profile 身份 + 进程内服务**,不是数据。它与 Super-agent 之间唯一的"协议"是自己造的那条本地管道。

## 四、技术思考

### 4.1 进程状态与 UI 状态怎么对齐

唯一的真相是**进程 + bridge 探测**,不是前端 store:

- 每次 `get()` 都 probe 一次管道(`controller.js:81-91`),相位由探测结果推:有应答 → `adopt(live)`(pid/RSS/active/configured);无应答但 PID 还活着 → `error`("仍在,但控制接口已断开"),**绝不显示为已关闭**;PID 也没了 → `enabled ? error : off`。
- `revision` 在每次状态变化时 +1(`controller.js:40`);`set` 必须带当前 `revision`,过期即拒(`controller.js:103`)。这把"两个窗口/两个会话同时点"的竞态变成显式失败,而不是静默覆盖——比加锁更符合"状态是共享的"这个事实。
- 过渡态由 `begin()` 统一接管:`busy = true` + `starting/stopping`,失败落 `error`,finally 清 `busy`(`controller.js:92-98`);UI 在过渡态把轮询从 5 s 降到 600 ms(`client.jsx:59`)。
- 前端每个渲染进程一份 store,会话切换不产生独立偏好(`client.jsx:41-43`);隐藏窗口不发轮询(`client.jsx:47`)。

一句话:**它把"UI 状态"降级成"进程状态的一次投影"**,所以关掉桌面再开,看到的仍是真状态,而不是上次存的选择。

### 4.2 生命周期:三条收尾路径,一条被绕过

- **启动**:probe → 端口占用检查 → `spawn(node,[cli,'--profile',name,'--no-open'],{windowsHide:true, stdio:[…,'ipc'], env:{DSH_HOME, DSH_SUPERAGENT_MANAGED:'1'}})`(`controller.js:118-134`);必须等 bridge 应答才算"已开启"(默认 60 s,`:146-154`)。
- **路径一(用户点关闭)**:管道 `stop` → bridge 判 `active > 0 && !allowBusy` 则回 `BUSY`(`bridge.js:56-58`)→ 否则 `runtime.stop()` → `appExit(0)`;控制端轮询 PID,确认消失才落 `off`(`controller.js:161-169`)。
- **路径二(桌面退出)**:`ctx.effect` 释放 → `controller.close()` → `stop(true)`(`index.js:27`,`controller.js:180-188`)。注意这里 **`allowBusy = true`**:关桌面时"忙碌二次确认"被绕过,正在跑的任务会被中断——`docs/design.md:46` 把这写成设计("桌面退出会请求后台收尾")。
- **路径三(父进程消失)**:托管启动带 IPC,子进程监听 `disconnect`;若启动时发现 `DSH_SUPERAGENT_MANAGED=1` 却没有 IPC,直接自退(`bridge.js:68-76`)。手工启动后被"接管"的实例没有这条保证(`docs/design.md:47`)。

### 4.3 权限与"不杀"

- 密钥 32 字节、`timingSafeEqual`、长度 ≥32 才比较(`transport.js:10-14`);请求 4 KB 上限、响应 32 KB、2.5 s 超时、socket 3 s 空闲销毁(`transport.js:15-30`,`bridge.js:39-46`)。
- **从不 `taskkill /F`、不按进程名批量杀**;端口被占就拒绝启动第二个(`controller.js:122`);PID 在但接口失联 → 保留信息报 `error`(`controller.js:87,175-177`)。
- 第二个控制者拿不到 owner 管道 → `initialize()` 失败,**不会去关别人的后台**(`controller.js:47-52`,`docs/design.md:43`)。
- bridge 的 `stop` 只在同一进程内生效,授权边界与上游一致:它不改 Super-agent 的业务策略,只决定"进程在不在"(`docs/design.md:62`)。

### 4.4 失败时的表现

- 启动超时/失败 → `error`,**不自动重试**;下次桌面初始化只按保存的 `enabled` 再试一次(`controller.js:63,146-154`;`docs/installation.md:92`)。
- 子进程退出 → `error` + "点击重试"(`controller.js:138-144`)。
- 收尾抛错仍继续退出,但作者写明"不能把进程退出解释为所有业务动作都成功提交"(`docs/design.md:37`)——这句是对"优雅退出"承诺的自我限制,比大多数同类插件诚实。
- 启动日志每次覆盖写 `DSH_HOME/plugins/superagent-power/worker.log`,里面可能有本地登录链接,提 issue 前必须脱敏(`docs/installation.md:88`)。

## 界面体验

- **入口**:输入栏工具区一个按钮,短标签 `Sup`(`client.jsx:114-117`);slot 为 `conversation.input.left`、order 71(`client.jsx:138`)。窄于 1400 px 时隐藏状态字,只留状态点(`client.jsx:31,117`)。
- **面板**:点开是一个 300 px 浮层(portal 到 `document.body`,自动翻转位置、Esc 关闭、点外部关闭)(`client.jsx:93-107,118-129`)。
- **面板内容**:标题"Super-agent"+ 徽章"全局",一句"所有会话共用同一个开关",一行状态 + 主按钮,一行"后台约 N MB · 运行中 N 个任务",底部一句"关闭会停止监听与后台任务,保留配置和记录"(`client.jsx:119-125`)。
- **状态点**:灰=已关闭、绿=已开启、黄=启动中/关闭中(脉动)、红=异常(`client.jsx:10-14,33-34`);过渡态按钮禁用并显示"请稍候…"(`:122`)。
- **忙碌保护**:有活动任务时第一次点"关闭"只把按钮变成"中断任务并关闭"并出一行红字警示,再点一次才发请求(`client.jsx:108-111,126`)。
- **失败时看到什么**:红点 + 具体原因——控制接口失联、启动超时、端口被占、进程未退出;按钮文案变成"重试开启"(`client.jsx:122`,`controller.js:87,168,176`)。
- **可访问性**:按钮有 `aria-label`/`aria-haspopup`/`aria-expanded`,面板 `role="dialog"` 且有标签,状态区 `aria-live="polite"`,Esc 关闭后回焦按钮,`prefers-reduced-motion` 下关掉脉动(`client.jsx:15,114-119`)。
- **信息密度**:极低——一个开关、两个数字、一句边界说明。这是刻意的:短标签为了少占输入栏宽度(`README:32`)。

## 用户交互的思路

- **谁发起**:用户点 `Sup` 开启——这是十二条线里**唯一把"起停另一个 profile 的进程"做成开关**的;上游本身没有"启动/停止"这个动作。
- **在哪确认**:同一个浮层里确认两件事:进程在不在(点 + 文案),以及"关掉会不会打断活"(二次点击)。
- **怎么观察**:绿点 + RSS + 活动任务数,平时 5 s 刷新、过渡态 600 ms(`client.jsx:59`);换会话看到同一状态,其他可见窗口约 5 s 内收敛(`README:58`)。
- **怎么打断**:点"关闭" → 有任务则二次确认 → bridge 拒绝无确认的忙碌关闭(`bridge.js:56-58`)→ 正常收尾后进程退出。**粒度是整进程**,不能只停某张工单。
- **与上游回路的差异**:上游是"消息 → 回执 → 结果"的闭环,人只在回执/提问处介入;Sup 把介入点前移到**运行形态**——关掉之后不再监听、不再回执。它比上游的"暂停编排"更彻底,也更粗(`README:61`)。
- **跨会话一致性**:开关不属于任何会话,切会话不触发启停(`README:28`);这与 mengzhongjie-local 那条"每个工作区一个主会话"的分叉路线正好相反。
- **一个缺口**:关桌面时 `close()` 传 `allowBusy=true`(`controller.js:184`),这条路径没有二次确认。"人在回路里"只覆盖用户主动点击。

## 五、代价与边界

1. **两处安装,一处路径写死**。Super-agent profile 的 patch 里 `name` 指向**桌面 profile 的 `node_modules` 里**的 `bridge.js`(`examples/superagent.patch.example.yml:5`)。桌面 profile 升级/搬迁 → bridge 加载失败,而症状是"控制接口不可用",不是"配置错了";`docs/installation.md:84` 把这条列进常见问题。
2. **依赖三处未文档化的内部接口**:`masterId`、`executor.activeCount()`、`agents.get(...).status`。任一改名,busy 保护会**静默变成 active = 0**——也就是"有任务时直接关掉"。这是本插件最危险的失效方向,而它没有自检能发现"我读到的是 0 还是拿不到"。
3. **版本钉死**:只声明三个 DSH 版本、Node ≥24、Windows 默认路径;`README:98-102` 明说其他版本要重新验证、macOS/Linux 未验收。
4. **端口探测把超时当占用**(`controller.js:20-27`):连不上但也不 RST 的端口会被判"被占用",拒绝启动。
5. **不是 npm 包**:`@local/` 命名空间 + tgz;注册表条目挂的 tarball 还是 `0.1.0`,仓库已到 `0.1.1`。
6. **改不了上游的恢复语义**:中断后能否从中断点继续由 Super-agent 决定,不保证(`README:63`)。
7. **没有自动闲置关闭**:作者明确保留手动开关,理由是"等待新事件正是主动代理的用途"(`docs/design.md:64-66`)。这是产品判断,不是遗漏。
8. **手工实例只能接管**:检测到已在跑就 adopt,并在"选择为关"时提示需要手动关,不会替你杀(`controller.js:63-67`)。

## 可信度与复现

- **读过**:`README.md`、`docs/design.md`、`docs/installation.md`、`docs/verification.md`、`package.json`、`cordis.patch.yml`、两个 example patch、6 个源文件、`test/` 3 个测试 + 1 个假 CLI 夹具与 `scripts/build.mjs`;上游 `src/app/runtime.ts`、`src/executor/dsh.ts`、`src/app/sessions.ts`、`src/index.ts`;本机 DSH 安装里的 `dsh-cmdline`(验 `appExit`)与 `dsh-client-ui-conversation`(验 slot 名)。
- **对位比过**:每个 `runtime.*` 调用都对到上游声明行;管道名、密钥、端口三处配置在两端一致。
- **没做**:Windows 实机启动/关闭;`npm run check`;真实业务 profile 的启停;macOS/Linux。
- **复现**:
  ```sh
  git clone https://github.com/MingoYung/dsh-superagent-power && cd dsh-superagent-power
  git checkout be94341
  grep -n "runtime\.\|agents\.get\|appExit" bridge.js
  grep -n "spawn\|pipeName\|control.key\|revision" controller.js transport.js
  ```

## 待验证

1. **`activeCount()` 的语义边界**:它数的是"打开的工单 ∩ running",不含排队中的 prepare 与刚结束的 turn(`上游 src/executor/dsh.ts:404`);关闭瞬间是否可能漏掉一个刚要启动的 Assignment,未实测。
2. **桌面退出中断任务的恢复**:`close()` 传 `allowBusy=true`(`controller.js:184`),上游重启后按 "host restarted" 处理(`docs/003-execution.md:146`)——但那是**同进程重启**的措辞,进程被杀是否走同一路径,未验证。
3. **bridge 加载顺序**:`bridge.js` 先 `await runtime.ready` 再开管道(`bridge.js:11`);若上游 setup 未完成(`configured()` 为 false),`ready` 是否 resolve、管道是否仍可用,只从代码看是"可用但 configured=false",未实机确认。
4. **端口黑洞**:防火墙 DROP 而非 REJECT 时,`portBusy` 1 s 超时即判占用(`controller.js:25-26`),会导致无法启动;换端口只能改配置。
5. **与 07/08 的共存**:power 只按 `homePath`+`profileName` 认进程,不读 `stateDir`;若同一 profile 里还装了 trace(读 `orchestrator`)与 wechat-source(自带 `stateDir`),三者互不感知,组合行为未验证。
