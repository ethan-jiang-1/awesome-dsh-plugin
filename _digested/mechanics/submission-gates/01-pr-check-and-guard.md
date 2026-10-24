# 01 · pr-check 与 pr-guard:fork 安全层与元检查

> 基线:`upstream@b4d0049a8`(0004 复核;pr-check 233→**244 行**,pr-guard 212 行未变)。行号对应该基线,段内引用为步骤序号。0003 对本专题零 diff,故 0002 的逐个结论原样带到 0004,只改有 diff 的部分。

## pr-check.yml(244 行,fork 可见的第一层)

触发 `pull_request`,权限 `contents: read`,无任何 secrets。**十一个 step** 依次(pr-check.yml:30-244;0001 六个、0002 十个):

1. **Stale-fork 守卫**(:30)。计数对象是**条目文件数**(`git diff -- data/plugins/`)——README 行数口径下,一个只带 `data/plugins/` 的 stale fork 会显示干净的对称 diff;本口径提示语为"单一投稿应为 +1/-0"。防的仍是落后 fork 静默吞条目(#502 案,删除在中英两侧对称自洽)。
2. **扩展名守卫**(:55)。`find data/plugins -type f ! -name '*.yml'`;丢失扩展名 = 沉默消失且全树自洽(#2495/#2140)。
3. **路径一层守卫**(:73,#3956)。条目必须匹配 `^data/plugins/[^/]+\.yml`——readEntries() 的 glob 不递归,放错层的文件"README 再生时静默消失、其余检查全绿"。真实案例:#3914(data/ 浅一层)、#3622(data/plugins/data/plugins/ 深层,全绿两周、文件还是非法 YAML——双重故障互相掩护)。报错给出可粘贴的 `git mv` 修正。
4. **"只改生成 README 行不算投稿"**(:111-157,**0002 新增**)。PR 若在 README.md/README.zh.md 里 diff 出生成区的插件行(`- [ … ](https://github.com/…)`)却**没有**任何 `data/plugins/` 变更 → 直接拒。注释写明 "The yml is the submission; README.md and README.zh.md are generated from data/plugins on main after the merge."。抓两种形态:
   - 作者写好了 yml 但没 stage——`git commit -a` 只记录改动与删除,**不记录新文件**(#5845,2026-09-25;其仓库其实 2026-08-27 就收录了,#3168);
   - 仓库早已收录,PR 里只有重生成的行在动。
   作用域仅限插件行,手写区(徽章/intro)不受影响。
5. **READMEs match data/plugins**(:158-213)。两种形态都接受——yml-only(新常态:runner 现场重生成,保持树一致)与 yml+再生 README(仍须 `--check` 匹配,手改被抓)。**0002 修正比对对象**:从 checkout 出来的 `refs/pull/N/merge` 改为 **PR 自己的 head commit**(`base.sha...head.sha`)。原因是 `pull_request` 事件的检出停在 merge ref 上,"as soon as main advanced past the PR's base, the merge tree's READMEs differed from base.sha's READMEs"——**#5796 实测(2026-09-24):96 个开放 PR 里有 18 个挂在这个假红上**。新增 `git fetch refs/pull/N/head` 兜底,并且 head SHA 解析不出来时显式报错。
6. **awesome-lint**(:214)。
7-10. **四个纯规则测试**(:216-232;0002 三个、**0004 加 entry-path**):`node --test scripts/added-dates.test.mjs`、`scripts/capabilities.test.mjs`、`scripts/adopt-discussions.test.mjs`、`scripts/entries-path.test.mjs`。注释强调 "Pure rules only — no downloads, no scanner, no token" 与 "Pure rules only, no token and no network"——这是升级成"有测试的仓库"的同时不破坏 fork 安全边界的做法(测试不许联网、不许要 token)。
11. **站点构建**(:233),带 `SKIP_PUBLISH_CHECKS=1`、探针数据缺失容忍——PR 检查必须免 token、fork 安全,发布前的 star 覆盖率门槛在这里关掉。

**0004 新增:`icon` 的准入判据在第 5 步生效,不在 pr-gate。** 这是本轮唯一新增的**内容判据**,却和"实质层"无关:`validateEntries()` 全仓只被 `scripts/generate-readme.mjs:95` 调用,失败就 `exit 1`("N problem(s) in data/plugins — refusing to generate.");第 5 步的两条分支都会跑到它——yml-only 走 `node scripts/generate-readme.mjs`(:206),改了 README 的走 `:210` 的 `--check`。所以非法 `icon` 让 `PR check` 红,而 `Submission gate` 那枚判决一动不动:`check-submission.mjs` 里没有任何一行读 `icon`。判据本身(`entries.mjs:116-134`,接在 `:247-253`)是四个条件的合取——非空字符串且能解析、`https`、`hostname` 精确等于四台之一(`raw.githubusercontent.com`、`user-images.githubusercontent.com`、`camo.githubusercontent.com`、`github.com`)、`pathname` 小写后以 `.png`/`.jpg`/`.jpeg`/`.webp` 结尾。**SVG 没有专门分支**,是被最后一条挡下的。与合同的两处差:`contributing.md:169-173` 只写"GitHub 托管",没列这四台,而报错只报作者用的那台(`entries.mjs:129`),所以 `avatars.githubusercontent.com` 这类"明明是 GitHub、却不在名单里"的主机会得到一句 "must be hosted on GitHub"——方向对、照做不了;模板里的 `icon:`(:21)是**活示例**,照抄能过检,但它指向的 `owner/repo/main/assets/icon-180.png` 九成不存在,而 404 在判据里合法。当前 13 条条目带 `icon:`,基线 0 条。

**0004 新增:entry-path 测试修的是"通过"与"没跑过"的本地版本,不是 CI 判决。** `readEntries()` 现在把 `file` 归一化成 POSIX(`entries.mjs:75` 的 `toPosix`,`:105` 应用)。原来的故障链在 Windows 上:`path.join` 给出 `data\plugins\x.yml`,而 `check-submission.mjs:495` 拿它去比 `git diff --name-only` 的集合,恒不命中 → `targets` 为空 → `:507` 打印 "no entry files added or changed — nothing to verify" → `:508` 写下 `{ok:true, checked:0}` → 退出码 0。**一个明显加了条目的 PR 得到一份自称通过的判决**,正是脚本自己在 `:501-505` 注释里点名要防的那种 gate。但别把影响说大:GitHub 的 runner 是 ubuntu-latest(`pr-check.yml:15`),而且 `pr-gate` 调校验器时带 `--only-list`(`pr-gate.yml:177-182`),过滤用的是 `path.basename`(`:491`),根本不走 `changedEntryFiles()`(`:415-417`)。所以**这条修复不改变任何 CI 判决**;它修的是"照 CI 的方式在本机复跑"这条路(维护者在 Windows 上手动跑)以及 `::error file=` 注解(`:570`)——注解要的本来就是仓库相对的 POSIX 路径。配套测试 `scripts/entries-path.test.mjs`(65 行、3 个 test)覆盖三种形状:绝对目录、`process.chdir` 进临时树后用默认的 `data/plugins`、以及 `icon` 的三条断言。诚实的边界写在覆盖面上:在 POSIX 主机上 `path.sep === '/'` 会短路 `toPosix`,这两条对"分隔符"这一项恒真——它们钉住的是**输出契约**,不是**那次回归**(只有在 Windows 上跑才会红);`icon` 也只测了"异地主机"和"SVG"两个拒绝分支,非字符串、非 https、其余三台主机、以及 `github.com` 的 blob 页都没测。

**0004 的前置改动:`npm ci` 改从 npmjs 取包**(:23-29)。这一步不是判据,是"别让门禁根本没跑起来":lockfile 里还有 7 条 `resolved` 指向 `registry.npmmirror.com`,而 2026-10-19 那家 CDN 对 tarball 返 503/504,`npm ci` 单个 job 能挂 20 分钟以上——挂住的 `PR check` 与"没有 verdict"在队列里不可区分,正是这条准入链反复要防的形态。所以 CI 用两个环境变量把自己钉死在 npmjs(`npm_config_registry` + `npm_config_replace_registry_host: always`,后者让 npm 忽略 lockfile 里记录的主机),注释明说"本机安装仍用自己的 registry"。同一改动落在全部六条跑 `npm ci` 的 workflow 上(`build-site`/`sync-readme`/`decay-scan`/`adopt-discussions` 另有专题),`regate`/`held-rescan`/`pr-guard` 不装包,所以本轮零 diff。

**0004 的另一个依赖变更:`dsh-trust-check` 0.1.13 → 0.2.1——升的不是这条准入链上的包。** 0004 把它从 `^0.1.13` 提到 **`^0.2.1`**(`package.json:25`,lockfile 解析到 `registry.npmjs.org` 的 0.2.1)。**它不在任何一条准入 workflow 里**:全仓唯一的运行面是 `scripts/probe-capabilities.mjs`,而那个脚本只由 `build-site.yml:232`(发布路径)调用。pr-check 的 `capabilities.test.mjs`(`:218-222`)只 import `scripts/lib/capabilities.mjs`,不 import 扫描器、不联网——所以 0.2.1 能让一个 PR 变红的唯一途径是 `npm ci` 装不上(包被撤或损坏),**不是它的判断**。

从本仓能核的三件事,以及核不了的:

- **能核·调用面**:`TOOL` 默认值改成 `dsh-trust-check@0.2.1`(`probe-capabilities.mjs:47`),`scannerCommand()` 仍优先用 `node_modules/.bin/dsh-trust-check`、否则 `npx`(`:61`),`scannerArgs()` 仍是 `--dir <pkgdir> --spec <npm:…> --json`(`:63-67`)——**参数与旗标零变化**,变的只有 spec 里的版本。新增的是 `lookupProvenance()`:`await import('dsh-trust-check')`,若导出里有 `readNpmProvenance` 就调它(`:84-89`),缺了或抛错就返回 `undefined`(注释:"we could not ask" ≠ "没有 attestation")。
- **能核·消费的字段**:`SCANNER_SCHEMA` 1 → 2,但 `READABLE_SCHEMAS = new Set([1, 2])` 让旧记录仍可读(`lib/capabilities.mjs:25-26`);本仓显式解析 `destinations[].sites[].usage`、`payload.provenance`;并新增 `rememberPrevious()` 保留上一版的能力与红线。
- **核不了**:0.2.1 的检测规则、它如何判定 `usage: compare`、红线文案在什么条件下出现——**这些都在 npm 包里,本仓没有副本**。也就是说"目录声称这个插件具备什么能力"这句话,我们能审计的只是装配线(取哪些字段、怎么合并、什么时候不写),审计不了判据。

对"什么会打回我的 PR"的结论是零影响;对"这个目录的披露可不可信"的结论是**一层不可约的不透明**——它是唯一一个"判断会变成目录对外披露、而我们只能核接口"的依赖。`dsh-trust-check` 自己又是已收录条目(`data/plugins/liuwenji007__dsh-trust-check.yml`)——同一份代码既是被审对象、又是审查工具,这条"自食其粮"仍无成文政策。

## 为什么需要 pr-guard.yml:两类「检查根本不会运行」的状态

pr-guard.yml:1-27 的注释是全文最关键的设计说明(0002 复核:文件本身零 diff):

- **状态一:PR 删掉了 pr-check.yml 本身。** GitHub 对 `pull_request` 事件取的是 PR merge ref 里的 workflow 文件——删文件的 PR 同时删掉了审判自己的法官。零 check run,和"CI 还没跑完"在队列里不可区分。#1635 真实发生:五个 workflow 文件被删,零检查运行。
- **状态二:PR 动了 `.github/` 下任何文件。** 投稿者不会故意这么干——这是 stale fork 的指纹:fork 的 `.github` 早于现行 CI,sync 回来会把旧 workflow 推回来,合并即静默回滚所有人的 CI(#1614、#1635)。

所以 pr-guard 从 default branch 的 schedule(cron `37 * * * *`)跑,**刻意处在它要审判的 PR 的爆炸半径之外**——这是它不能并进 pr-check.yml 的原因(pr-guard.yml:21-23)。

> **0002 补记**:held-rescan 后来补上了这类状态的第三种子情形——**分支与 main 冲突的 PR 没有 merge ref,GitHub 根本不会为它创建 `PR check` run**(#2202)。pr-guard 抓的是"检查被外力关掉",held-rescan 抓的是"检查从未有机会跑",两者合起来才覆盖"没有 check run"的全部成因。见 [02](./02-pr-gate-and-check-submission.md)。

## pr-guard.yml 运行机制

- **成本纪律**:一条 GraphQL 查询按 50 个 PR 分页,同时携带文件列表(first:100)与 head commit 的 checkSuites/checkRuns;REST 等价物约 350 次调用,会挤兑门禁依赖的 1000/h 仓库配额(:64-69,又见 :113-116:GraphQL 返回 SCREAMING_CASE 结论枚举,与 REST 小写直接比较永远为 false——第一版撤回逻辑因此从不触发)。
- **两分钟原则变成九十分钟原则**(:48-57):"没有检查"只对出生满 `MIN_AGE_MINUTES=90` 的 PR 标;首次贡献者的 fork PR 要等维护者批准才起跑,等待以小时计,20 分钟版会把正常投稿哭成狼。
- **判决每轮重算、只在变化时张贴**(:119-129):第一版贴了 failure 就永不复查,#1624 在检查变绿后仍挂着红 X。"过期的红"与"过期的绿"互为镜像,同属这个 guard 要防的事。**0002:这个"过期证据"的论证被 regate 推广到了红 check 本身**(见 [03](./03-regate-and-bleed.md))。
- files 超 100 时补一次 REST 全量分页(:131-143),不从残缺清单里得出"没动配置文件"。
- 对 `.github/` 触碰给出可直接粘贴的三行恢复命令,并解释 push 被 workflow scope 拒绝时是同一根因的另一面(:163-172)。

## 与上游冲突解决工具:maint-rebase.sh

232 行维护脚本(未变):把 stale PR rebase 到 main、再生 README、推回贡献者 fork(要求 maintainerCanModify;走 SSH 因为 gh OAuth token 缺 `workflow` scope,推不动含 `.github/workflows` 改动的分支)。

两个值得记录的策略(maint-rebase.sh):

- 开头拒绝脏工作树(:17-21):因为循环里全是 `git reset --hard`,而 bash 边执行边重读脚本文件——曾有一次对脚本本身的修改在运行中途被自己销毁,之后跟着一个磁盘上已不存在的文件继续跑。
- 冲突策略(:52 起):README.md/README.zh.md 永远取 main 版本(反正要重新生成),但重试 resolve 直到 rebase 真正结束或遇到脚本无权决定的冲突(guard 上限 50 轮);`data/screenshots.json` 单独做**以 merge-base 为底的三方 JSON 合并**——取 main 会丢掉投稿者的截图(PR 的全部意义),而简单 overlay 会复活 main 已删除、分支还带着的陈旧 key(build-site 会因 key 不匹配已收录条目而拒建)。
- **0002 关联**:held-rescan 现在把"分支冲突、CI 从未跑"的 PR 也列进 tracking issue,而补救手段正是这个脚本(rebase 到 main)。

## 待复核

- [ ] ISSUE_TEMPLATE/list-problem.yml 的字段与 decay scan 处置流的衔接(与 probes-and-decay 共同核验)
- [ ] **0002 新增**:四个 `node --test` 步骤在 fork PR 上确认真的不触网(注释是承诺,未见 CI 层面的网络隔离;`entries-path.test.mjs` 自己 `process.chdir`,更值得确认它不会读到工作树之外的东西)
- [ ] **0004 新增**:`entries-path.test.mjs` 的分隔符断言在 POSIX runner 上恒真——它测的是形状,不是那次 Windows 回归。要真回归,需要有人偶尔在 Windows 上跑一次这 65 行
- [ ] **0004 新增**:`icon` 的五个拒绝分支只测了两个(异地主机、SVG);`https` 强制、非字符串、以及 `github.com` 的 blob 页(能过检却取回 HTML)都无测试
- [ ] **0004 新增**:`npm_config_replace_registry_host` 只在 CI 生效,lockfile 里仍有 7 条 npmmirror 的 `resolved`——本机 `npm ci` 仍走镜像,一旦镜像再 504,贡献者的本地复现与 CI 会分叉
