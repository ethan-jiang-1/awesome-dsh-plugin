# 01 · pr-check 与 pr-guard:fork 安全层与元检查

> 基线:`main@5e7dc7eb`。所有行号对应该基线。

## pr-check.yml(82 行,fork 可见的第一层)

触发 `pull_request`,权限 `contents: read`,无任何 secrets。五个 step 依次(pr-check.yml:24-82):

1. **Stale-fork 守卫**(:24-41)。对 README.md 做 diff,数被删的条目行(`^-- \[.+\]\(https://github\.com/`)与新增行;当 `removed > 2 且 removed > added` 判失败,提示"Sync fork 后重推"。防的是落后 fork 一合并就静默吞掉新条目——#502 那种会删 32 条的 fork 曾在所有内容检查下全身而过,因为删除在中英两侧是对称的、自洽的。
2. **扩展名守卫**(:42-59)。`find data/plugins -type f ! -name '*.yml'`。readEntries() 只读 `*.yml`,一个丢失扩展名的文件会在沉默中消失——且其余检查全绿:再生的 README 同样少了它,自洽。#2495 修过一次,#2140 又从旧 main 基础上把它带回来。
3. **README 同步**:generate-readme.mjs --check(:60-68)。
4. **awesome-lint**(:69-70)。
5. **站点构建**,带 `SKIP_PUBLISH_CHECKS=1`、探针数据缺失容忍(:71-82)——PR 检查必须免 token、fork 安全,所以发布前的 star 覆盖率门槛在这里关掉。

## 为什么需要 pr-guard.yml:两类「检查根本不会运行」的状态

pr-guard.yml:1-27 的注释是全文最关键的设计说明:

- **状态一:PR 删掉了 pr-check.yml 本身。** GitHub 对 `pull_request` 事件取的是 PR merge ref 里的 workflow 文件——删文件的 PR 同时删掉了审判自己的法官。零 check run,和"CI 还没跑完"在队列里不可区分。#1635 真实发生:五个 workflow 文件被删,零检查运行。
- **状态二:PR 动了 `.github/` 下任何文件。** 投稿者不会故意这么干——这是 stale fork 的指纹:fork 的 `.github` 早于现行 CI,sync 回来会把旧 workflow 推回来,合并即静默回滚所有人的 CI(#1614、#1635)。

所以 pr-guard 从 default branch 的 schedule(cron `37 * * * *`)跑,**刻意处在它要审判的 PR 的爆炸半径之外**——这是它不能并进 pr-check.yml 的原因(pr-guard.yml:21-23)。

## pr-guard.yml 运行机制

- **成本纪律**:一条 GraphQL 查询按 50 个 PR 分页,同时携带文件列表(first:100)与 head commit 的 checkSuites/checkRuns;REST 等价物约 350 次调用,会挤兑门禁依赖的 1000/h 仓库配额(:64-69,又见 :113-116:GraphQL 返回 SCREAMING_CASE 结论枚举,与 REST 小写直接比较永远为 false——第一版撤回逻辑因此从不触发)。
- **两分钟原则变成九十分钟原则**(:48-57):"没有检查"只对出生满 `MIN_AGE_MINUTES=90` 的 PR 标;首次贡献者的 fork PR 要等维护者批准才起跑,等待以小时计,20 分钟版会把正常投稿哭成狼。
- **判决每轮重算、只在变化时张贴**(:119-129):第一版贴了 failure 就永不复查,#1624 在检查变绿后仍挂着红 X。"过期的红"与"过期的绿"互为镜像,同属这个 guard 要防的事。
- files 超 100 时补一次 REST 全量分页(:131-143),不从残缺清单里得出"没动配置文件"。
- 对 `.github/` 触碰给出可直接粘贴的三行恢复命令,并解释 push 被 workflow scope 拒绝时是同一根因的另一面(:163-172)。

## 与上游冲突解决工具:maint-rebase.sh

232 行维护脚本:把 stale PR rebase 到 main、再生 README、推回贡献者 fork(要求 maintainerCanModify;走 SSH 因为 gh OAuth token 缺 `workflow` scope,推不动含 `.github/workflows` 改动的分支)。

两个值得记录的策略(maint-rebase.sh):

- 开头拒绝脏工作树(:17-21):因为循环里全是 `git reset --hard`,而 bash 边执行边重读脚本文件——曾有一次对脚本本身的修改在运行中途被自己销毁,之后跟着一个磁盘上已不存在的文件继续跑。
- 冲突策略(:52 起):README.md/README.zh.md 永远取 main 版本(反正要重新生成),但重试 resolve 直到 rebase 真正结束或遇到脚本无权决定的冲突(guard 上限 50 轮);`data/screenshots.json` 单独做**以 merge-base 为底的三方 JSON 合并**——取 main 会丢掉投稿者的截图(PR 的全部意义),而简单 overlay 会复活 main 已删除、分支还带着的陈旧 key(build-site 会因 key 不匹配已收录条目而拒建)。

## 待复核

- [ ] ISSUE_TEMPLATE/list-problem.yml 的字段与 decay scan 处置流的衔接(与 probes-and-decay 共同核验)
