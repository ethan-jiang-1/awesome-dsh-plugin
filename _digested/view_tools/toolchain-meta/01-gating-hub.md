# gating-hub — 拿 profile 补丁当控制面的升级保险:升级前改别人的源码,起不来就关行

> 证据等级:★★★(源码级;`Noob-stupid/dsh-plugin-gating-hub@3d25799572058813cb0c9eaceb992e231e142b98`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 54、下载无记录,均为 2026-08-19 冻结采样;实时星标 131 为 2026-11-18 另查。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `Noob-stupid/dsh-plugin-gating-hub`([registry](../../../data/plugins/Noob-stupid__dsh-plugin-gating-hub.yml)) |
| 类目 | tools(1639 条;全表 11 744,[census](../../ecosystem/census.py)) |
| 子分类 | [`toolchain-meta`](README.md)(工具链元层)——本册当前唯一成员 |
| 自述 | registry 中文自述:「升级前跑『会话格式契约预检』…升级失败自动回滚、把拖垮过启动的插件自动隔离;另有环境指纹与公开契约规则库…内置多源插件市场只作发现层」;npm 包名却是 `@noob-stupid/dsh-plugin-console`——仓库名、包名、`cordis.patch.yml` 里的行 id(`plugin-console`)三者不同名 |
| 星标 ⚠ | **54**(2026-08-19 采样);2026-11-18 实时 **131**,forks 7,仓库 `homepage` 仍指向旧名 `dsh-plugin-hub` |
| 下载 ⚠ | **边车无记录**(`data/downloads.json` 624 条里没有该 URL,属 2026-08-19 采样缺口,不是零下载);可核到的是包本身:126 个 npm 版本,2026-08-21 首发,latest `0.5.110`(2026-11-10 发布,npm registry 于 2026-11-18 查询) |
| 扩散 | **0**(口径:`grep -ril 'gating-hub' data/plugins/` 命中 1 条,减去自身;命中:仅它自己。另有三个易混 token,见「为什么它突出」) |
| 仓库 commit | `3d25799572058813cb0c9eaceb992e231e142b98`,2026-11-17 22:51:24 +0000,`chore: refresh marketplace index`;仓库创建 2026-08-14,共 **950** 个提交、**130** 个 tag,主分支 `main` |
| 包形态 | npm `@noob-stupid/dsh-plugin-console@0.5.110`,**bundle 插件**:`package.json` 的 `dsh.bundle.patch` 指向 5 行 `cordis.patch.yml`,另带 `dsh.client`(web,注入 3 个 client 包);**零运行时依赖**(`package.json` 无 `dependencies`,`pnpm-lock.yaml` 的 `importers` 只有空对象);装法 `dsh plugin --profile web add @noob-stupid/dsh-plugin-console` |
| 代码规模 | `lib/**/*.js` 153 文件 / **47 405 行**,其中 `lib/client.js` **9 018 行**、服务端 38 387 行;测试 148 个 `test-*.mjs` / **38 242 行**;`docs/` 850 行;369 个受控文件,GitHub 计 9 997 KB |

## 它到底是什么

**它不是适配层,也不挂任何外部系统;它是一个装在 DSH 进程里的控制台,控制对象是宿主自己的文件。**

- `~/.dsh/profiles/<p>/cordis.patch.yml` —— 组合层的用户补丁:`- id: X` + `disabled: true`(`lib/server/domain/patch.js:100-110` 追加停用块、`:155-183` 追加启用行,全部是它自己拼文本)。
- `~/.dsh/profiles/<p>/package.json` 的 `dsh.profile.bundles` —— 它自己往清单里写 bundle(`lib/server/domain/install.js:37-49`),注释说这与官方 `dsh plugin add` 的 reconcile 行为一致,但代码里**没有调用任何 DSH API**。
- `~/.dsh/.agent-presets/<name>/agent.cordis.yml` —— 升级前就地迁移旧字段(`lib/server/domain/presets.js:59-94`),隔离时直接改名成 `.broken-<ts>`(`lib/server/routes/framework-upgrade.js:589`)。
- DSH 安装树 —— 升级前做全树 checkpoint、升级后回滚/重链,以及往 `dsh-app-boot/lib/index.js` 里写一段 YAML 容错补丁(`lib/server/domain/framework.js:97-115`)。

它没有 `ctx.provide`,只 `export name / inject / apply`(`lib/index.js:69-83`):**它对别的插件没有可调用的接口,只有对文件的读写权。** 全部能力经宿主 `webServer` 上的一条 `/plugin-console` 前缀路由出去(`lib/index.js:102-131`),表驱动分发 76 条路由表项(`lib/server/routes/index.js:51` 起)。

内部可以切成四个环,彼此的耦合只有共享状态文件:

| 环 | 触发 | 落盘 | 主要模块 |
|---|---|---|---|
| 契约预检 | 用户点「升级前预检 / 适配」或升级脚本前置 | 只读扫描;`apply` 时写回源码 + `.bak-preflight-*` | `format-contract.js` / `format-scan.js` / `routes/framework-preflight.js` |
| 升级与回滚 | 用户点「一键升级 / 回滚上版」 | `framework-backups/<ver>/`、`framework-rollback.json` | `routes/framework-upgrade.js` + 生成的 PowerShell |
| 常驻门控 | 每次 `/compat-status` 查询(面板轮询)看到指纹变化 | `env-fingerprint.json`、`auto-preflight.json`、`compat-pending.json`、`safe-boot/snapshots/` | `compat-state.js` / `auto-preflight.js` / `auto-disable.js` / `safe-boot.js` |
| 市场与安装 | 用户浏览/搜索/安装 | 装进 profile,写补丁行 | `market.js` + `install*.js` + `sources.js` |

状态全部住 `~/.dsh/plugin-console/`(`lib/server/infra/paths.js:13-15` 定义 `dshHome`,其余模块各自拼子路径),不写用户 profile 以外的配置目录;**但 patch 与 preset 是原地改的**,没有副本目录。

## 怎么接进 DSH

- **manifest**:只有两个键起作用——`package.json:36-39` 的 `dsh.bundle.patch`(指向 `cordis.patch.yml`)与 `:40-47` 的 `dsh.client`(`platform: web` + 三个 `@deepseek-ai/dsh-client-*` 注入)。`cordis.patch.yml:3-5` 只有一条 `insert`:id `plugin-console`、name `@noob-stupid/dsh-plugin-console`。`exports["./client"]`(`package.json:14`)是面板入口。
- **宿主接线**:`apply(ctx)` 里 `inject = ['webServer','loader']`(`lib/index.js:70`),`ctx.effect(...)` 内 `ctx.webServer.register({ kind: 'prefix', path: '/plugin-console' })`(`:102-131`)。分发器把路由分成「405 守卫之前 / 之后」两张表,因为 GET 只被 `GET_COMPAT` 白名单放行(`lib/server/routes/index.js:1-10` 头注释、`:51-120`)。
- **本机限定**:先判 `isLoopback(remoteAddress)`,再校验 `Host` 必须是 `127.0.0.1:<port>` / `localhost:<port>` / `[::1]:<port>`;非 GET/HEAD 还要求同源(`Origin` / `Sec-Fetch-Site` 校验,`lib/index.js:107-122`)。这是它自己的护栏,不是宿主给的。
- **依赖**:运行时零依赖;对 DSH 的定位全靠 `createRequire().resolve('@deepseek-ai/dsh/package.json')` 反查安装树(`lib/server/domain/framework.js:19-33`、`lib/server/infra/fw-root-detect.js:45`),不 import 任何 `@deepseek-ai/*`。
- **安装后要重启** dsh 服务再刷新页面(README:30-34 的安装流程也这么要求)——组合树在启动时装配,插件路由只在进程内 `apply` 之后存在。

## 关键实现

### 文件结构

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `lib/client.js` | 9018 | 设置页里的整套面板(市场、插件、框架卡、门控、安全启动) | 单文件打包产物,`window.__ModuleLoader__.load` |
| `lib/server/routes/index.js` | 232 | 两张路由表 + `handle()`;启动自更新调度 | :51 前缀、:1-10 GET 表纪律 |
| `lib/server/routes/framework-upgrade.js` | 696 | 一键升级:备份 → 预禁用 → 生成 PowerShell → 隔离 → 判定 | :173-211、:362-398、:574-633 |
| `lib/server/routes/framework-preflight.js` | 227 | 契约预检的两个端点(只读预检 / 出 diff / apply) | :47-80 扫描面、:98-179、:182-225 |
| `lib/server/domain/format-contract.js` | 265 | 从 npm registry 抓目标版本的会话格式迁移边 + 从 README 抽规则 | :24 catalog、:98-125、:179-237 |
| `lib/server/domain/format-scan.js` | 437 | 本地生产方扫描与就地重写(V3 `kind: 'plugin'` → V4 producer-owned) | :112-136 注释掩码、:172-221 计划、:370-415 写盘 |
| `lib/server/domain/framework.js` | 577 | checkpoint、CLI 备份、宿主形态识别、升级前预禁用 | :97-115、:176-198、:449-462、:507-576 |
| `lib/server/domain/quarantine.js` | 224 | 启动失败日志分析 + 隔离方案 + 记录并入门控清单 | :63-87、:98-131、:137-190 |
| `lib/server/domain/compat-state.js` | 176 | 环境指纹、运行模式、回滚记录读取 | :116-129、:147-156、:158-174 |
| `lib/server/domain/auto-preflight.js` | 345 | 指纹变化 → 只读预检的判定/节流/超时/记录 | :97-105、:112-127、:236-285 |
| `lib/server/domain/safe-boot.js` | 520 | last-known-good 快照与「只禁点名行」的纯判定 | :152-179、:185-200、:207-280 |
| `scripts/safe-boot.mjs` / `fw-preflight.mjs` / `fw-watchdog.mjs` | 260 / 186 / 246 | 服务起不来时的进程外出路(零依赖、不联网、不 spawn dsh) | 三个文件头各有一段「为什么必须进程外」 |
| `lib/contracts/rules.json` | 72 | 5 条契约规则的数据包(随包发布) | :15-70 |

### 数据流一:契约预检(回答「检查什么、规则从哪来、怎么判不兼容」)

1. **远端契约**:问目标版本「带哪些会话格式迁移边」。先取 `@deepseek-ai/dsh-session-format-catalog@<target>` 的 dependencies(`format-contract.js:179-188`),取不到才退回 `@deepseek-ai/dsh` 的 dependencies;边包名匹配 `^@deepseek-ai/dsh-session-format-v(\d+)-to-v(\d+)$`(`:21`)。然后按 `to` 从高到低最多拉 3 条边的 README(jsDelivr → npmmirror files API 两条通道,`:27`、`:165-173`),用正则从 README 里抽四件事:`Producer attribution` 行是否要求 producer-owned kind、`Any other plugin name` 行里的 `plugin:` 前缀、`Message-source conversion` 小节里「旧名 → 新名」的重命名表、证据摘录(`:98-125`)。**只有「目标版本比当前版本多出一条迁移边」才算契约变更**(`:145-148`),摘要会明说「本次新增迁移边」(`:240-249`)。
2. **本地生产方扫描**:扫描面 = `~/.dsh/.agent-presets` + 已装且启用的每个插件包目录;框架自带包(`profile` 之外的路径,或包名以 `@deepseek-ai/` 开头)单独标成 `kind: 'framework'`(`routes/framework-preflight.js:47-80`)。目录名 `.agent-presets` 是 2026-09-27 修过的真 bug(少一个点 ⇒ 预设从来没被扫过,"0 blocker" 是假绿,`:35-45`)。
3. **判据**:只认三种 blocker —— `kind: 'plugin'` 且同一对象字面量里确有 `plugin:` 字段的可改命中、同一形状但无法安全内联的只报告不修改、以及带探针的 `.volatile()` 告警(见下)。重写规则极保守:改的是 `kind` 的字面量本身,保留 `plugin:` 字段,`plugin:` 是字符串就写 `'plugin:<值>'`、是标识符就写 `` `plugin:${expr}` ``(`format-scan.js:172-221`)。
4. **不误报的几道闸**:注释先被等长掩码掉(注释里的 `kind: 'plugin'` 不算代码,`format-scan.js:112-136`);框架自带包命中一律降级成 `warn` + `fixable:false`(改框架文件等于污染安装树,`:317-325`);控制台自身从扫描面剔除(`routes/framework-preflight.js:54-63`);`schemastery-volatile` 规则必须先用 `createRequire` 从该文件位置真的解析一份 `@deepseek-ai/schemastery`,确认那份副本确实没有 `.volatile()` 才报(`format-scan.js:61-85`)——否则依赖修好后会永久误报。
5. **写盘**:只写「本次上报名单内 + severity=blocker + fixable」的位置,写前 `copyFile` 出 `<file>.bak-preflight-<stamp>`,备份失败就放弃该文件(`format-scan.js:370-415`);`isInsideAllowed` 用路径前缀再挡一次(`:358-364`)。
6. **规则库的真相**:`lib/contracts/rules.json` 是**人读的登记册**,不是执行引擎。检测参数不在数据里(`detect`/`fix` 是中文散文),扫描器实际只消费 `rules.pluginPrefix` 与 `rules.renames`(`format-scan.js:173-174`);自动预检那条路径把整份 `rules` 数组传进去(`auto-preflight-run.js:96-99`),那两个字段读不到,静默回落到默认值。规则库的价值在**可测的诚实性**:测试断言「声称 `implementedBy` 的规则,代码里真有那个实现」(`tests/test-contract-rules.mjs:45-58`),读不到文件时回报 `source:'unavailable'` 而不是「零发现」(`contract-rules.js:50-68`)。5 条规则全部有 `implementedBy`,无一「仅登记」。

### 数据流二:升级、回滚、隔离(回答「备份什么、回滚到哪、隔离在哪」)

**备份三件,顺序固定:**

1. 配置快照 `~/.dsh/plugin-console/framework-backups/<current>/`:`cordis.patch.yml`、`profile-package.json`、`plugins.json`(行 id/包名/启用位/版本/安装日期)(`framework.js:449-462`,在 `routes/framework-upgrade.js:100` 调用)。
2. CLI 目录整树拷贝到 `backupDir/dsh-package-backup`(`framework-upgrade.js:173-183`);**强制校验**里面有 `lib/bin.js`,否则直接取消升级(历史上曾因备份缺失导致"回滚后框架目录为空",`:184-189`)。
3. 框架全树 checkpoint `framework-backups/<ver>/fw-tree/<ts>/`:镜像 `.pnpm/@deepseek-ai+*` 每个版本包的「自包内容」+ 顶层 `@deepseek-ai` scope + `lock.yaml` + `fw package.json`(`framework.js:176-198`)。**不跟随依赖 junction**,所以体积小;扁平安装(无 `.pnpm`)时 `storeSkipped:true`,只镜像顶层 scope 与 lock。

**回滚边界(关键)**:PowerShell 的 `Invoke-Rollback` 先停监听该端口的服务,然后优先走全树:`checkpoint/.pnpm` 存在就把每个 `@deepseek-ai+<name>@<ver>` 的实体 robocopy 回去、整目录替换顶层 scope、拷回 `lock.yaml`(`framework-upgrade.js:368-388`);checkpoint 缺 `.pnpm` 时退化成只恢复 `dshDir` 一个目录(`:389-393`)。**回滚不碰用户 profile、不碰非 `@deepseek-ai/*` 的包**,也不还原 `package.json` 之外的 profile 状态。

**自动回滚的触发条件比宣传窄**:安装退出码非 0(两个 registry 各试一次、再停服重试一次,`:400-410`)会回滚;拉起失败则先做隔离,**只有拉起失败原因里出现「框架树损坏」标记(`Cannot find package` / `ERR_MODULE_NOT_FOUND` / `找不到 dsh 的 bin.js` / `package.json 不存在` 等)才自动回滚**,其余一律「保留框架 + 手动命令 + 人工点回滚」(`framework-relaunch.js:56-64`、`:150-167`)。2026-10-28 用户定案如此,代码注释写明了。

**启动失败隔离**:升级脚本在服务起不来时循环最多 3 轮(`framework-upgrade.js:613-626`):用 `fw-analyze-boot.mjs` 调插件内的 `planQuarantine`(不把判据复制进 PowerShell),后者从最近 400 行日志里认三类信号——`preset "x" failed to mount`、`failed to apply loader entry <rowId> (<module>)`、`Cannot find module '<module>'`(`quarantine.js:63-87`),映射回候选行,剔除核心行/受保护行/自身(`:107-116`)。落到三处:

- 记录 `~/.dsh/plugin-console/fw-quarantine.json`(mode/时间/被改名预设/被禁用行/命中日志行)(`framework-upgrade.js:605-609`);
- 被禁用的行**直接追加进 profile 的 `cordis.patch.yml`**(`:591-596`);
- 预设文件改名 `agent.cordis.yml.broken-<ts>`(`:587-590`);
- 若一个明确肇事者都没有(`planQuarantine` 返回 `safeMode`),它会把**当时所有第三方行**一次性禁掉,先让服务起来(`:598-604`)。

下次启动时 `mergeQuarantineRecord` 把记录并进 `compat-pending.json`,**先写清单并读回校验成功、才允许归档删除原记录**(`quarantine.js:137-190`);写失败会留 `fw-merge-error.log`,绝不销毁证据(`:29-37`)。这就是「谁被自动关了、为什么」在面板上的唯一来源。

### 数据流三:环境指纹 → 自动预检 → 证据禁用

指纹只有三个字段:`frameworkVersion`、`pnpmEntities`(`.pnpm` 下 `@deepseek-ai+*` 目录个数)、`pnpmRoot`(框架树根,含不含 `.pnpm` 的那一层),外加 `at`(`compat-state.js:110-129`)。基线写 `~/.dsh/plugin-console/env-fingerprint.json`,每次 `/compat-status` 现场重算并比对,任一项变化就是「环境变更事件」——**不管是谁改的**(官方桌面端更新器、手动 pnpm、npx 缓存)(`routes/compat.js:286-304`)。

变化后跑一次**只读**预检:超时 4 秒、同一指纹只自动跑一次、失败/超时允许重试一次(`auto-preflight.js:27-33`、`:97-105`、`:112-127`、`:236-285`);扫描内容 = 补丁行可解析性 + 生产方源码 + 预设声明行 + `.dsh-boot.log` 点名(`auto-preflight-run.js:80-138`)。结论里只有两种 `code` 算「确证证据」:`package-unresolvable`(所有解析基准都解析不到)、`file-target-missing`(`file://` 目标不存在),外加启动日志点名(`auto-disable.js:61-115`);解析不确定时整批只报告。真禁之前先写一份 last-known-good 快照(`safe-boot.js:207-280`),所以每一次自动禁用都能用一条命令回滚。三个开关住 `compat-gate.json`,**默认全开**(`autoDisable` / `autoDetect` / `autoDisableOnEvidence`,只有显式写 `false` 才关,`compat.js:204-216`);面板上的「自动禁用」开关只动 `autoDisableOnEvidence` 一项(`routes/compat.js:427-437`)。

### 数据流四:市场(回答「是不是只作发现层」)

默认源(`sources.js:266-304`):2 个 npm registry(npmmirror 主 / npmjs 备)、GitHub + Gitee 两个搜索源、**5 个静态索引源**(jsDelivr 三入口 + ghproxy + raw,全部指向它自己仓库的 `marketplace/index.json@main`)、2 个 git 克隆源、2 个 archive 源。

「零 GitHub API 调用」只对**浏览索引**成立:索引走 CDN、10 分钟内存缓存(`routes/market.js:408-419`)。**搜索与富化照样打 api.github.com**,而且是 https 与 `gh` CLI **并行竞速**(`http.js:223-251`),`gh` 那条会用你的 GitHub 凭据(`GH_TOKEN` 走环境变量,不上命令行,`http.js:79-86`);装包仍走 pnpm/registry。所以它是「发现层 + 安装器」,不是纯展示;只是发现层不改变门控判定。

## 为什么它突出

**先看数字,再看结构。**

- 星标:⚠ 54(2026-08-19)→ 实时 131(2026-11-18),三个月 +77;forks 7。仓库 2026-08-14 创建,95 天里 950 个提交、130 个 tag、126 个 npm 版本——**单作者、日更级发版**。
- 扩散:**0**。可复现口径:`grep -ril 'gating-hub' data/plugins/` 只有它自己。三个易混 token 都是撞名,不是衍生:`dsh-plugin-hub` 命中 5 条全是 `wingsky-1/dsh-plugin-hub` 的子包条目;`dsh-plugin-console` 命中 1 条是 `AlexYin-Tongji/dsh-plugin-console`(另一个仓库);`noob-stupid` 命中 4 条,除自身外是同一作者的 `dsh-github-login`、`dsh-connection-card-host`、`dsh-breadboard`,三条都没引用它。
- 时间线决定了「门控」是后来长出来的:2026-08-14 首发是「插件控制台 + 市场」;契约预检与隔离在 **2026-09-24** 的 `8a0d99c feat(0.4.0): 分层架构转正 + 升级前会话格式契约预检` 才出现;指纹自动预检、证据禁用、safe-boot 快照在 **2026-09-29** 的 `1a2aa35 0.5.32` 才出现(`git log --reverse -- <path>` 可复现)。也就是说,「元层」只占它三个月寿命的后六周。

**它算不算「被别人依赖」的元层?源码给出的答案是否定的。**

它没有任何 `ctx.provide`、没有导出的服务键、没有供别的插件调用的 API(`lib/index.js:69-83` 只有 `name` / `inject` / `apply`)。别的插件即便想依赖它,也只有一个 HTTP 前缀可以打——那不是 cordis 的依赖关系,是「同一台机器上的另一个网页」。所以「工具链元层」这个定位在它身上是**权威意义上的**(它能改你的补丁、你的预设、你的框架树),不是**调用链意义上的**(没有人调用它)。

判断:**按本册两轴口径,它是「声量小、扩散零」的单点工具,不是锚。** 但它是这批条目里少见的「有明确状态机与回滚点的单点工具」——真正的观察价值不在它今天被谁依赖,而在于它把「升级前预检 / 失败回滚 / 启动隔离」写成了可被抄的格式(compat-pending 清单、safe-boot 快照、隔离记录)。目前没有任何第三方引用这些格式,所以「标准」二字还只是它自己的注释。

## 代价与边界

**权限面(最硬的一条)**:它对宿主的写入是**无 API 中介**的——直接改 `cordis.patch.yml`、profile `package.json`、`.agent-presets` 里的 YAML、框架安装树,还会给 `dsh-app-boot/lib/index.js` 打一段容错补丁(`framework.js:97-115`,留 `.bak-issue5`)。其中 patch 文件是 DSH 官方插件管理器与它**共同**的写目标(它自己的 `appendInsert` 注释就写了「用户先用官方插件管理启用,再在我们面板点启用 ⇒ 重复装配」的现场,`patch.js:143-154`),并发写没有跨进程锁,只有进程内 `queuedWrite`。

**平台边界**:一键升级/回滚整条通道依赖 Windows 计划任务 + PowerShell,**非 win32 一律 501 拒绝**(`framework.js:287-301`),桌面端 Electron 托管时 409 拒绝(`:267-274`,判据在 `:225-261`)。在 macOS/Linux 上能用的只有契约预检、证据禁用、快照与两个离线脚本。

**失败模式,按发生顺序:**

1. **契约拉取失败 → 降级但不阻断**:`discoverFormatContract` 不抛,返回 `contract:null` + error,扫描继续用默认规则(`format-contract.js:194-237`、`routes/framework-preflight.js:107-126`);`DSH_TEST_SKIP_NETWORK=1` 时直接跳过网络(`:93-96`)。
2. **规则库缺失 → 如实报 `unavailable`**,不伪装成零发现(`contract-rules.js:50-68`);但扫描器本来就不消费规则库,所以「零发现」的实际含义仍是「代码里的三条判据没命中」。
3. **预检误报**:注释掩码是个手写状态机,不认正则字面量。我实测:文件里先出现一个含单引号的正则(如 `/'/u`),后面的注释里写着 `kind: 'plugin'` 就会**被当成代码报成 blocker 并写回**(`maskComments` + `planSourceKindRewrites` 的合成结果,`format-scan.js:112-136`、`:179-203`)。改写落在注释里语义无害,但会污染 diff、并给出一个假的 blocker。
4. **改写不看目标版本**:`kind:'plugin'` 的重写是无条件的,`producerKindRequired` / `edgesAdded` 只用于展示(`routes/framework-preflight.js:125`、`format-scan.js:172-221`);只有 `.volatile()` 这类已知破坏才用 `since` 卡版本(`:252`)。对一个还不需要 V4 的目标版本跑 apply,理论上会改出宿主不认识的 kind —— **未在真机验证**(见末节)。
5. **写盘失败**逐个文件记 `skipped` + 原因,不会假装成功(`format-scan.js:388-410`);`apply` 端点返回同一批目标重扫后的 `remaining`(`routes/framework-preflight.js:210-223`)。
6. **升级前置失败**逐个前置拦:无回滚点 → 500 取消(`framework-upgrade.js:184-189`);框架根认不出 → 500(`:194-195`);CLI 解析不到 → 200 但 `upgraded:false` + 步骤文本(`:156-164`)。
7. **安装失败 → 回滚**;回滚自身异常会写 `failed` + 「框架可能处于混合状态」,并把出错行位置写进日志(`:365-397`)。
8. **拉起失败 → 隔离(最多 3 轮)→ 仍失败才判定**:只有树损坏证据才自动回滚,否则停在「保留 + 手动命令」(`framework-relaunch.js:150-167`、`framework-upgrade.js:627-633`)。
9. **隔离误伤的代价**:行被写进 `cordis.patch.yml` 后,面板再启用会吃 409(软锁,带 `confirmRisky:true` 可通过,`routes/plugins.js:77-107`),而启用前还有一道**不可覆盖**的硬门:子进程真 import 一次,失败就拒绝(`:109-123`、`compat.js:105-140`)。预设的恢复只能手工把 `.broken-<ts>` 改回原名(`quarantine.js:171-174` 自己写了这条出路)。`safeMode` 一轮就会关掉全部第三方行——救得回服务,但用户会看到"插件全没了"。
10. **指纹的已知盲区**:它自己的注释承认「目录壳还在、里面被掏空 ⇒ 计数不变 ⇒ 判定环境未变」(`fw-preflight.js:8-14`),所以另补了进程外的 `fw-preflight.mjs`;这类事故里「控制台里的按钮等于没有」,因为它跑在 dsh 里(`:16-18`)。
11. **回滚点可用性的两套判据**:状态接口只看 `framework-backups` 目录存不存在(`compat-state.js:158-174`),而回滚路由要求 `framework-rollback.json` + checkpoint 与 fwRoot **都含 `.pnpm`**(`routes/framework.js:407-412`)。扁平安装树升级时 checkpoint 会 `storeSkipped`(`framework.js:183`),于是「升级成功但一键回滚不可用」是可能的。

**数据与隐私**:指纹三字段 + 路径,只落本地 `env-fingerprint.json`;`grep -rni 'telemetry|analytics|上报' lib/ scripts/` 未见遥测代码,也没发现指纹被塞进任何出网请求体。实际出网点只有:npm registry(默认 npmmirror)、api.github.com / raw.githubusercontent.com(+ `gh` CLI)、它自己仓库的 5 个索引 URL、用户配置的 Gitee OAuth。Gitee 的 `clientSecret` / `token` 与自定义搜索源的 `Authorization` 头存在 `~/.dsh/plugin-console-sources.secrets.json`,权限 `0o600`(`sources.js:184`),`/sources` 响应里打码(`:139-160`)。

**信任模型**:索引是 `marketplace/index.json@main` 的**可变指针**,取回后直接进缓存、没有任何摘要/签名校验(`routes/market.js:408-498` 只有 `fetchJsonUrl` + 10 分钟缓存),所以能改那个仓库或 CDN 的人就能改面板推荐什么;但装什么仍要过 pnpm 与它自己的安装校验,索引本身不改门控判定。

**维护成本**:三个月 126 个 npm 版本、950 个提交,注释里带日期的事故复盘随处可见;单作者 + 单一测试栈(`node tests/run-all.mjs` 四组),对第三方贡献者不友好;`deploy.sh` 还写着旧的包名 `@deepseek-ai/dsh-plugin-console`(`deploy.sh:9-24`),与 `package.json` 不一致——它的升级脚本里专门有一段「自报名一致性校验」正是为这类错配写的(`framework-upgrade.js:541-560`)。

## 可信度与复现

- **★★★(本插件全部 DSH 侧机制)**:读过上表所有文件的关键段落 + `lib/index.js` / `routes/index.js` / `patch.js` / `presets.js` / `auto-disable.js` / `sources.js` / `http.js` / `scripts/*.mjs` 头部;对照了本机 DSH 的 `dsh-app-boot`(`evaluatePluginCompatibility` 在本机 0.2.x 里是 `node_modules/@deepseek-ai/dsh-app-boot/lib/index.js:311`,`preflight` 在 `:2311`;插件注释里写的 286-313 / 2063-2109 是旧行号,函数与语义对得上)。
- **跑过的**:契约/格式/隔离/快照/自动预检/指纹相关的 7 个离线测试全绿(237 个断言):`test-contract-rules` 23、`test-format-contract` 23、`test-format-preflight` 62、`test-quarantine-merge` 22、`test-safe-boot` 43、`test-auto-preflight` 44、`test-compat-state` 20。
- **没跑过的**:生成的 PowerShell(升级/回滚)只在 win32 有意义,本机是 macOS;`scripts/fw-watchdog.mjs` 依赖 Windows 进程名;`gh` 竞速通道未实测。
- **未读**:`lib/client.js` 9 018 行只扫了结构与门控相关片段;`install*.js` / `suite.js` / `link-*.js` / `repoland.js` / `selfupdate*.js` 只读了头注释与调用点——所以「市场/安装/自更新有多稳」不在本卡结论内。

```sh
# 1) 克隆与提交(BRIEF 要求重新克隆,不用旧克隆)
git clone --depth 1 --filter=blob:none https://github.com/Noob-stupid/dsh-plugin-gating-hub.git .work/mine/cards/gating-hub/repo
cd .work/mine/cards/gating-hub/repo && git fetch --unshallow --filter=blob:none -q
git log -1 --format='%H %ad %s' --date=iso
# → 3d25799572058813cb0c9eaceb992e231e142b98 2026-11-17 22:51:24 +0000 chore: refresh marketplace index
git rev-list --count HEAD; git tag | wc -l        # → 950 / 130
git log --reverse --format='%h %ad %s' --date=short | head -1
# → 860d1e3 2026-08-14 feat: DSH 插件控制台——一键启用/停用插件 + GitHub dsh-plugin 插件市场

# 2) 代码规模
find lib -type f -name '*.js' -exec wc -l {} + | tail -1     # → 47405 total(153 文件)
wc -l lib/client.js                                          # → 9018
find tests -maxdepth 1 -name 'test-*.mjs' -exec wc -l {} + | tail -1   # → 38242(148 文件)
python3 -c "print(47405-9018)"                                # → 38387(服务端)

# 3) 扩散(在 awesome-dsh-plugin 仓库根;data/plugins 有 11 744 个文件,必须用目录形式)
grep -ril 'gating-hub' data/plugins/ | wc -l                  # → 1(只有它自己)
grep -ril 'dsh-plugin-hub' data/plugins/ | wc -l              # → 5(全是 wingsky-1 的同名项目)
grep -ril 'dsh-plugin-console' data/plugins/ | wc -l          # → 1(AlexYin-Tongji 的同名仓库)
grep -ril 'noob-stupid' data/plugins/ | wc -l                 # → 4(自身 + 同作者 3 条,均无引用)

# 4) 类目分母
python3 _digested/ecosystem/census.py | head -6               # → 总数 11744 / tools 1639

# 5) 我跑过的那批测试(全离线,私有 DSH_HOME)
for t in test-contract-rules test-format-contract test-format-preflight test-quarantine-merge test-safe-boot test-auto-preflight test-compat-state; do
  DSH_TEST_SKIP_NETWORK=1 node tests/$t.mjs >/tmp/$t.log 2>&1; echo "$t exit=$? pass=$(grep -c '^PASS' /tmp/$t.log) fail=$(grep -c '^FAIL' /tmp/$t.log)"; done
```

## 待验证

1. **Windows 实机跑一次升级 + 失败回滚**:PowerShell 脚本只被字符串级测试覆盖(`test-upgrade-script-blocks` 抽块断言、`test-upgrade-script-syntax` 做语法树检查),真正的 `robocopy` 回滚、`schtasks` 拉起、15 分钟/5 分钟双阈值都没实测。
2. **扁平(hoisted)树上的回滚行为**:checkpoint 会跳过 store 镜像(`framework.js:183`),回滚脚本要求 checkpoint 含 `.pnpm`(`framework-upgrade.js:371`),一键回滚路由又要求两边都有 `.pnpm`(`routes/framework.js:409-412`)——扁平树上到底退化成什么,需要一台上游 npm 安装的机器验证。
3. **不带 `producerKindRequired` 的目标版本跑 `apply`**:是否会改出宿主不认识的 `kind`。代码上重写无条件(`format-scan.js:172-221`),但真实旧宿主已很难找。
4. **`gh` 竞速通道的凭据行为**:`githubViaGhReal` 把 `GH_TOKEN` 注入环境(`http.js:79-86`),但它是否会用到用户已登录的 `gh` 配置、限流算在谁头上,未实测。
5. **规则库与代码的一一对应**:5 条规则都有 `implementedBy`,但 `patch-overlay-toplevel-array` 指向的是写侧规范化 `sanitizePatchText`(`patch.js`),真正的读侧校验在 `patch-yaml-check.js`——「规则被预检读」这句话在数据层面成立几分,需要逐条对着判据核。
6. **真实环境下的自动预检节流**:同一指纹只跑一次、失败重试一次、4 秒超时,测试用的是桩扫描器(`tests/test-auto-preflight.mjs`),真实 profile(数千文件)下会不会稳定降级成 `timeout` 未量化。
7. **registry 之外的扩散**:GitHub 全站代码检索需要鉴权,本卡只统计了 `data/plugins/` 的 11 744 条;`dsh.so`、`awesome-dsh-plugin.com` 等站点是否有第三方引用未查。
