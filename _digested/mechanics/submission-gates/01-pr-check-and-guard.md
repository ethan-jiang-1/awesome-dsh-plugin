# 01 · pr-check 与 pr-guard:fork 安全层与元检查

> 基线:`upstream@c18ba4a0d`(0002 复核;pr-check 146→**233 行**,pr-guard 212 行未变)。行号对应该基线,段内引用为步骤序号。

## pr-check.yml(233 行,fork 可见的第一层)

触发 `pull_request`,权限 `contents: read`,无任何 secrets。**十个 step** 依次(pr-check.yml:24-233;0001 是六个):

1. **Stale-fork 守卫**(:24)。计数对象是**条目文件数**(`git diff -- data/plugins/`)——README 行数口径下,一个只带 `data/plugins/` 的 stale fork 会显示干净的对称 diff;本口径提示语为"单一投稿应为 +1/-0"。防的仍是落后 fork 静默吞条目(#502 案,删除在中英两侧对称自洽)。
2. **扩展名守卫**(:49)。`find data/plugins -type f ! -name '*.yml'`;丢失扩展名 = 沉默消失且全树自洽(#2495/#2140)。
3. **路径一层守卫**(:67,#3956)。条目必须匹配 `^data/plugins/[^/]+\.yml`——readEntries() 的 glob 不递归,放错层的文件"README 再生时静默消失、其余检查全绿"。真实案例:#3914(data/ 浅一层)、#3622(data/plugins/data/plugins/ 深层,全绿两周、文件还是非法 YAML——双重故障互相掩护)。报错给出可粘贴的 `git mv` 修正。
4. **"只改生成 README 行不算投稿"**(:105-151,**0002 新增**)。PR 若在 README.md/README.zh.md 里 diff 出生成区的插件行(`- [ … ](https://github.com/…)`)却**没有**任何 `data/plugins/` 变更 → 直接拒。注释写明 "The yml is the submission; README.md and README.zh.md are generated from data/plugins on main after the merge."。抓两种形态:
   - 作者写好了 yml 但没 stage——`git commit -a` 只记录改动与删除,**不记录新文件**(#5845,2026-09-25;其仓库其实 2026-08-27 就收录了,#3168);
   - 仓库早已收录,PR 里只有重生成的行在动。
   作用域仅限插件行,手写区(徽章/intro)不受影响。
5. **READMEs match data/plugins**(:152-207)。两种形态都接受——yml-only(新常态:runner 现场重生成,保持树一致)与 yml+再生 README(仍须 `--check` 匹配,手改被抓)。**0002 修正比对对象**:从 checkout 出来的 `refs/pull/N/merge` 改为 **PR 自己的 head commit**(`base.sha...head.sha`)。原因是 `pull_request` 事件的检出停在 merge ref 上,"as soon as main advanced past the PR's base, the merge tree's READMEs differed from base.sha's READMEs"——**#5796 实测(2026-09-24):96 个开放 PR 里有 18 个挂在这个假红上**。新增 `git fetch refs/pull/N/head` 兜底,并且 head SHA 解析不出来时显式报错。
6. **awesome-lint**(:208)。
7-9. **三个纯规则测试**(:210-221,**0002 新增**):`node --test scripts/added-dates.test.mjs`、`scripts/capabilities.test.mjs`、`scripts/adopt-discussions.test.mjs`。注释强调 "Pure rules only — no downloads, no scanner, no token"——这是升级成"有测试的仓库"的同时不破坏 fork 安全边界的做法(测试不许联网、不许要 token)。
10. **站点构建**(:222),带 `SKIP_PUBLISH_CHECKS=1`、探针数据缺失容忍——PR 检查必须免 token、fork 安全,发布前的 star 覆盖率门槛在这里关掉。

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
- [ ] **0002 新增**:三个 `node --test` 步骤在 fork PR 上确认真的不触网(注释是承诺,未见 CI 层面的网络隔离)
