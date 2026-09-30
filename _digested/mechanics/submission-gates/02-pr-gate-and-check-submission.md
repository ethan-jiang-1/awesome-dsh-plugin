# 02 · pr-gate 与 check-submission:判决机

> 基线:`upstream@c18ba4a0d`(0002 复核;pr-gate.yml 316→**369 行**,`check-submission.mjs` **584 行未变**)。0001 最大变更:commit floor 删除(#4196)+ 已收录仓库豁免 + 非法扩展名的显式归因。**0002 最大变更:非法 YAML 的显式归因(#4680)+ held-rescan 收编"CI 从未运行"的 PR(#2202)。**

## 分工

- `check-submission.mjs`(584 行,**未变**):纯校验器。输入是条目清单,输出是 JSON 判决 `{ok, checked, failures[], incomplete[], tooMany?}`(`--json` 落盘),退出码只反映 failures。
- `pr-gate.yml`(**369 行**):调度与判决发布层。处理「PR 是谁、改了哪些文件、怎么把结果钉回 commit」,并把校验器产出翻译成 check-run(success / neutral / failure 三种结论 + 65000 字符 summary 上限)。

> 0002 观察:**这次的加固全部落在"调度/归因层",校验器一行没动**——也就是门禁的病不在判据,而在"判据没跑起来、或跑起来但说不清是哪份文件"。

## 校验器(check-submission.mjs)

### 常量即历史

| 常量 | 值 | 出处 | 为什么是这个数 |
|------|-----|------|----------------|
| `MIN_AGE_DAYS` | 1 天 | :21 | 过滤"PR 前几分钟才建的仓库"。失败文案是 "nothing to do: this check re-runs by itself"(regate 的 aged 规则每 6 小时按 summary 里的 `/days old/` 字样自动翻转判决;旧文案曾驱使作者关 PR 重开或 force-push 空提交) |
| ~~`MIN_COMMITS`~~ | ~~10~~ | 已删(:23-31) | **0001 删除**(2026-09-03,#4196):提交数衡量的是开发**习惯**不是质量;"实践中它从未拒绝过任何东西,全部效果就是延迟 + 一枚让后续人审对干净历史带偏见的红 X"。age floor 保留:**时间不可伪造** |
| `CONCURRENCY` | 6 | :31 | 批间并发 |
| `MAX_TREE_PKGS` | 40 | :32 | 每个 package.json 要一次 contents API;DSH 本体树里 dsh-base 排在第 19 个 manifest,所以守得住 |
| `MAX_ENTRIES_PER_PR` | 3(env 可覆盖) | :78 | 定值时的实测是 92×1 / 8×2 / 0×3;**2026-09-24 重数(最近 100 个"新增过条目"的 PR):88×1、3×2、9×3**——上限正在被真实使用,见 [00-map](./00-map.md) §评审哲学 |
| `MAX_WAIT_PER_CALL_MS` / `_TOTAL_MS` | 75s / 150s | :130-131 | 无界退避本身就是事故(runner 空转等配额重置不如报 unverified 让 regate 重来) |

### 两级准入日期(contributing 的「老条约老规则」)

- `GATE_EFFECTIVE_FROM`:2026-08-16T00:00:00Z(:58)之后开的 PR 才受年龄/门槛约束;
- `BULK_RULE_FROM`:2026-08-20T00:00:00Z(:79)之后才受 ≤3 条上限约束;
- workflow 侧(pr-gate.yml:152-153)用 `git log --diff-filter=A -- <pr-gate.yml>` 取 workflow 实际落地日作为 effective_from,**不让脚本默认值和现实漂移**。

### 判决的四种出口(:560-567 附近)

1. `problems` 非空 → failure(exit 1),逐条以 `::error file=…::` 注解到具体文件;
2. 仅 `unverified` → 放行但如实汇报("N pass;M could not be fully checked"),**incomplete 永不阻塞**(§ fail-open 纪律);
3. 全查过且全过 → "all checked entries pass";
4. 超 PR 条数上限 → 在发出任何网络请求**之前**就拒绝(:518-541),"先花配额再拒"是浪费。

### 反悔逻辑的核心:`unverified ≠ problems`

设计者反复强调的方向性问题(pr-check 里 ok:true 未检查、:365 附近 meta 非 200 返回 unverified):

> 一个 gate 若分不清「通过」和「从没跑过」,比没有 gate 更糟——因为它被信任着。

由此派生一整族行为:meta 请求失败 → 本条目"nothing checked";tree API 截断(truncated:true,HTTP 仍是 200)→ 视为 unknown 而非 absent(:219-225 附近);package.json 超 40 个读不完 → 同样 unknown。

### 身份黑名单与 vendored 检测(:41/:50, vendored :244)

- `FIRST_PARTY_REPOS = {deepseek-ai/deepseek-harness}`:**按身份拒绝**。DSH 自己声明 dsh.bundle,合同检查它全过——"在插件的插件列表里收录产品本体"是每个访客都认得的错误,所以不按合同按身份拒。
- `FIRST_PARTY_PACKAGES = {@deepseek-ai/dsh-base, dsh-web-app, dsh-headless}`:**vendored 记录暂缓**。实测有五个仓库存着 harness 拷贝(fork:false 检不出来);它们可能只是在测试里合法地带了一份 harness,所以只有整棵树扫完仍无真实 bundle 时才报"这个仓库包含的是 harness 而非插件"。

### hasBundle() 的三层判定(:280 起;fuzzy 候选 :300-313、根指向修正 :316-356)

1. **直读**入口 URL 对应目录的 package.json(sub 先行;解析失败 → 明确失败而非"视为无清单",BOM 由 :189 剥除——Windows 编辑器写出的 U+FEFF 曾让 JSON.parse 抛错后被误报为"没有 dsh.bundle");
2. sub 404 → 用 `manifestDirs()` 做 leaf 名的双向 includes fuzzy 匹配给出候选(#1794 教训:旧提示会让作者照建议改成另一个插件名);
3. 根指向且根无 bundle → 全树扫描;找到子包 bundle 时**仍判失败**,并给出完整修正三件套(url/name/文件名,#1701 教训:site 从条目 URL 构造安装命令,装的是根,不是碰巧在某子目录里的清单。2026-08-18 审计 1302 个根指向条目,48 个实际不可安装)。

### API 成本工程(:95-171)

- **403 三义性**:权限拒绝(无 retry-after/x-ratelimit-remaining 头,立即返回)、主配额(x-ratelimit-remaining:0,等到 reset)、次级滥用限制(retry-after,约一分钟)。第一版三者一律放弃 → 2026-08-25 八个投稿裸奔未核验。修复:只重试"重试有用"的两类,严格等 GitHub 要求的时长(:116-124 附近)。
- **memo 按 promise 不按结果**(:175-180 附近):monorepo N 个子包 → 同 repo 的 meta/commits/tree 只发一次;#1608 一个 PR 带 33 个子包曾产生 64 次纯重复调用(1000/h 配额,这就是 2026-08-18 挤兑的成因,23 个开放 PR 因此挂着"无法完全检查")。
- **已收录仓库豁免(`listedReposAt`)**:从 base commit 的 `git ls-tree` 按**文件名**解析已收录 owner/repo(名字 `owner__repo--sub.yml` 的第一个 `__` 必是 owner 边界,GitHub owner 名不含下划线);豁免的是**仓库**不是变更类型——改名落到已收录仓库直接跳过门槛(Tlyer233 案:插件在自己仓里上移一层目录,却被"7 commits (needs 10)"拒绝),落到未收录仓库仍受全量审查(#1554 原样保留)。豁免**以 base 为准**,PR 不能靠同一 push 里自加首条目给自己发豁免;base 读不到 → null = "谁都不豁免",fail-closed。

## pr-gate.yml 调度层(369 行)

### 定位 PR:一次请求而非遍历(:43-60)

`workflow_run.pull_requests` 对 fork PR 为空;早期实现分页列出全部 ~150 个 open PR——这正是 2026-08-18 配额爆掉的源头之一。现改为用 `head_repository.owner:head_branch`(一个分支至多一个 open PR)+ head_sha 精确匹配一次命中。找不到时静默退出(PR 已关或已被新 push 取代)。

### 解析 PR 失败 = 显式红(:65-84)

在贴出判决前死掉的 gate 与"不需要跑的 gate"不可区分——绿色 check 旁读者只会觉得"没问题"。现在 catch 里直接在对应 commit 上创建 conclusion:failure 的 check-run。**0002:这类"门禁自己跑挂"的判决现在会被 regate 认出来并 1 小时后自动重问**(见 [03](./03-regate-and-bleed.md) 的 `faulted`)。

### 提取层(:99-153)

- checkout 停留在 main(信任的代码、信任的 lockfile);`git fetch refs/pull/N/head` 后 **merge-base 对比今天的 origin/main**——API 给的 base.sha 是开 PR 时的快照,fork 同步过的分支会因此把别人的条目算进本 PR。
- `--diff-filter=AR`:**R(改名)必须算进来**。#1554 通过改名条目文件、把 url 指向别的仓库绕过了"没有新增文件"的门;"R 时 --name-only 打印新路径",恰好是要检查的那份。
- `git archive … | tar -x`:blob 只作数据进 /tmp/prdata,不执行任何东西。extract 步骤显式输出 `base` 供 listedReposAt 使用(必须从 base commit 读)。
- **非 yml 扩展名的显式归因**(:264-285):extract 收集 data/plugins/ 下全部变更路径,而校验器只读 `*.yml`——扩展名丢失的条目会被计数、永不解析、永远进 failure 分支,#1477 因此被"重跑 workflow"搪塞了 13 天。现在全数非 yml 时直接报 "N entry file(s) missing the .yml extension",附逐文件 `git mv` 命令。
- modified.txt:本 PR 改写的既有条目单独列出,M 类不走年龄/提交门(存量条目按收录时的规则,周度 decay scan 盯它们的退化),但**每一份判决都要附上这份清单**让评审追问:#1348 案(两次混过所有机械检查)正是这类。

### 0002 新增:非法 YAML 的显式归因(:286-337)

在非 .yml 分支之后,pr-gate 现在把**每一个变更的 `.yml`** 丢给 js-yaml 解析,失败则报 `N entry file(s) are not valid YAML`,附文件+行号与一行复现命令。动机写在注释里:"the file is named right but is not valid YAML, so readEntries() drops it and --only-list then matches nothing"——**#4680 在这里挂了五天**,根因是它的 `zh:` 行是 GBK 乱码(UTF-8 被当 GBK 读)。

实现细节值得记一笔:`require` 用的是**绝对路径** `${process.env.GITHUB_WORKSPACE}/node_modules/js-yaml`,因为 github-script 会把 `require` 解析到 action 自己的目录而不是工作树。js-yaml 加载不了时退回通用的"门禁什么都没查到"文案,不静默放行。

### 判决翻译表(约 :198-362)

| 情形 | 结论 | 标题语义 |
|------|------|----------|
| 无新增+无修改 | success | "No entries changed" |
| 无新增但有修改 | success + modifiedNote | 列出所有被改写的既有条目 |
| 结果文件缺失 | failure | "The gate could not run"( checker 崩溃=bug 不是投稿问题;**0002 起 regate 会对它 1 小时后重问**)|
| tooMany | failure | 附全文拆分劝告 + "pick as well as split" |
| changed 全部无 .yml 扩展名 | failure | "N entry file(s) missing the .yml extension" + 逐文件 git mv 命令 |
| **有 .yml 但解析不了(0002)** | failure | **"N entry file(s) are not valid YAML" + 文件:行号 + 复现命令(:316-337;#4680)** |
| checked===0 但 extract 说有文件 | failure | 两个组件互相矛盾,不能 vouch |
| ok 且有 incomplete | **neutral** | "X pass;其余放行但 nothing here vouches for them" —— neutral 就是留给 regate 重访的钩子 |
| ok 全绿 | success | "dsh.bundle declared, repo old enough, enough commits" + modifiedNote(**上游遗留**:commit floor 已删但这句没改,现位于 **pr-gate.yml:362**)|
| 有 failures | failure | 每条逐点列出 + 指向 contributing.md |

## held-rescan.yml(258 行):"从未运行"也是队列成员

0002 唯一改动(233→258 行):gate 过滤条件从 `gate !== 'SUCCESS'` 放宽为 `gate !== 'SUCCESS' && gate !== undefined`(:139),于是**根本没有 gate 判决**的 PR 也进队列。理由是:"A pull request whose branch conflicts with main has no merge ref, so GitHub never creates its `PR check` run"——**#2202 因此在作者四次追问下干等**。NEUTRAL 仍被排除(gate 跑过、只是配额耗尽 fail-open),两者不可混为一谈。

配套:issue 表格新增 `gate` 列(✅/—,:190/:225),表头改为"green **or has never had the chance to run**",并明确补救手段是**维护者 rebase 到 main**,不是让作者 push。

## 待复核

- [x] neutral 在 regate 侧的重访闭环 → 见 [03](./03-regate-and-bleed.md)(已核)
- [ ] `concurrency.group: pr-gate-<head_sha>` cancel-in-progress 的实际效果(同一 head_sha 连续完成两次会互相取消?)UNVERIFIED,值得跑一次观察
- [ ] **0002 新增**:`entries.mjs` 的 name↔url 规则(#5756)会不会误伤"顺手把 name 写成上游组织名"的合法条目——六条违规里五条指向不存在的仓库,可疑但未抽样全部
