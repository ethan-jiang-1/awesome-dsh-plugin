# 02 · pr-gate 与 check-submission:判决机

> 基线:`upstream@38976afd`(0001 复核;行数 check-submission 529→**584**、pr-gate.yml 275→**316**)。最大变更:**commit floor 删除**(#4196)+ 已收录仓库豁免 + 非法扩展名的显式归因。

## 分工

- `check-submission.mjs`(584 行):纯校验器。输入是条目清单,输出是 JSON 判决 `{ok, checked, failures[], incomplete[], tooMany?}`(`--json` 落盘),退出码只反映 failures。
- `pr-gate.yml`(316 行):调度与判决发布层。处理「PR 是谁、改了哪些文件、怎么把结果钉回 commit」,并把校验器产出翻译成 check-run(success / neutral / failure 三种结论 + 65000 字符 summary 上限)。

## 校验器(check-submission.mjs)

### 常量即历史

| 常量 | 值 | 出处 | 为什么是这个数 |
|------|-----|------|----------------|
| `MIN_AGE_DAYS` | 1 天 | :21 | 过滤"PR 前几分钟才建的仓库"。**0001:失败文案重写**——不再说"约 N 小时后重新提交",改为"nothing to do: this check re-runs by itself"(regate 的 aged 规则每 6 小时按 summary 里的 `/days old/` 字样自动翻转判决;旧文案曾驱使作者关 PR 重开或 force-push 空提交去"买"本就会到账的东西) |
| ~~`MIN_COMMITS`~~ | ~~10~~ | 已删(:23-31) | **0001 删除**(2026-09-03,#4196):提交数衡量的是开发**习惯**不是质量——squash-merge 仓的多年真改动 main 历史很短,而 `git commit --allow-empty` 十秒清线;"实践中它从未拒绝过任何东西,全部效果就是延迟 + 一枚让后续人审对干净历史带偏见的红 X"。age floor 保留:**时间不可伪造**。另注意 pr-gate.yml:309 的 success 文案仍残留 "enough commits" 字样——上游自己的过期字符串 |
| `CONCURRENCY` | 6 | :31 | 批间并发 |
| `MAX_TREE_PKGS` | 40 | :32 | 每个 package.json 要一次 contents API;DSH 本体树里 dsh-base 排在第 19 个 manifest(~248 个中),所以守得住 |
| `MAX_ENTRIES_PER_PR` | 3(env 可覆盖) | :78 | 最近 100 个已合并 PR:92×1 条、8×2 条、0×3 条。awesome-go 收 1 条、awesome-python 自动关多件套——3 是宽松端。唯一正当多件形态:monorepo 子包各自可安装 |
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

由此派生一整族行为:meta 请求失败 → 本条目"nothing checked";tree API 截断(truncated:true,HTTP 仍是 200)→ 视为 unknown 而非 absent(:219-225 附近);package.json 超 40 个读不完 → 同样 unknown。~~commit 数读不到记 unverified~~ 一条随 commitCount() 一并删除(0001)。

### 身份黑名单与 vendored 检测(:41/:50, vendored :244)

- `FIRST_PARTY_REPOS = {deepseek-ai/deepseek-harness}`:**按身份拒绝**。DSH 自己声明 dsh.bundle,合同检查它全过——"在插件的插件列表里收录产品本体"是每个访客都认得的错误,所以不按合同按身份拒。
- `FIRST_PARTY_PACKAGES = {@deepseek-ai/dsh-base, dsh-web-app, dsh-headless}`:**vendored 记录暂缓**。实测有五个仓库存着 harness 拷贝(fork:false 检不出来);它们可能只是在测试里合法地带了一份 harness,所以只有整棵树扫完仍无真实 bundle 时才报"这个仓库包含的是 harness 而非插件"。

### hasBundle() 的三层判定(:280 起;fuzzy 候选 :300-313、根指向修正 :316-356)

1. **直读**入口 URL 对应目录的 package.json(sub 先行;解析失败 → 明确失败而非"视为无清单",BOM 由 :189 剥除——Windows 编辑器写出的 U+FEFF 曾让 JSON.parse 抛错后被误报为"没有 dsh.bundle");
2. sub 404 → 用 `manifestDirs()` 做 leaf 名的双向 includes fuzzy 匹配给出候选(#1794 教训:旧提示会让作者照建议改成另一个插件名);
3. 根指向且根无 bundle → 全树扫描;找到子包 bundle 时**仍判失败**,并给出完整修正三件套(url/name/文件名,#1701 教训:site 从条目 URL 构造安装命令,装的是根,不是碰巧在某子目录里的清单。2026-08-18 审计 1302 个根指向条目,48 个实际不可安装)。

### API 成本工程(:95-171 → 0001 下移约 8-16 行)

- **403 三义性**:权限拒绝(无 retry-after/x-ratelimit-remaining 头,立即返回)、主配额(x-ratelimit-remaining:0,等到 reset)、次级滥用限制(retry-after,约一分钟)。第一版三者一律放弃 → 2026-08-25 八个投稿裸奔未核验。修复:只重试"重试有用"的两类,严格等 GitHub 要求的时长(:116-124 附近)。
- **memo 按 promise 不按结果**(:175-180 附近):monorepo N 个子包 → 同 repo 的 meta/commits/tree 只发一次;#1608 一个 PR 带 33 个子包曾产生 64 次纯重复调用(1000/h 配额,还要和其它 workflow 共享——这就是 2026-08-18 挤兑的成因,23 个开放 PR 因此挂着"无法完全检查")。
- ~~commitCount~~(0001 删除):曾从 Link header 的 rel="last" 页码取值,走同一套 api() 退避;commit floor 删除后整个函数移除,memo 只剩 meta/tree 两类。
- **已收录仓库豁免(0001 新增,listedReposAt)**:从 base commit 的 `git ls-tree` 按**文件名**解析已收录 owner/repo(名字 `owner__repo--sub.yml` 的第一个 `__` 必是 owner 边界,GitHub owner 名不含下划线);豁免的是**仓库**不是变更类型——改名落到已收录仓库直接跳过门槛(Tlyer233 案:插件在自己仓里上移一层目录,却被"7 commits (needs 10)"拒绝),落到未收录仓库仍受全量审查(#1554 原样保留)。豁免**以 base 为准**,PR 不能靠同一 push 里自加首条目给自己发豁免;base 读不到 → null = "谁都不豁免",fail-closed。

## pr-gate.yml 调度层

### 定位 PR:一次请求而非遍历(:43-60)

`workflow_run.pull_requests` 对 fork PR 为空;早期实现分页列出全部 ~150 个 open PR——这正是 2026-08-18 配额爆掉的源头之一。现改为用 `head_repository.owner:head_branch`(一个分支至多一个 open PR)+ head_sha 精确匹配一次命中。找不到时静默退出(PR 已关或已被新 push 取代)。

### 解析 PR 失败 = 显式红(:65-84)

在贴出判决前死掉的 gate 与"不需要跑的 gate"不可区分——绿色 check 旁读者只会觉得"没问题"。#2026-08-18 有两个低于提交门槛的投稿因此看起来可合并。现在 catch 里直接在对应 commit 上创建 conclusion:failure 的 check-run。

### 提取层(:99-153)

- checkout 停留在 main(信任的代码、信任的 lockfile);`git fetch refs/pull/N/head` 后 **merge-base 对比今天的 origin/main**——API 给的 base.sha 是开 PR 时的快照,fork 同步过的分支会因此把别人的条目算进本 PR(:104-111)。
- `--diff-filter=AR`:**R(改名)必须算进来**。#1554 通过改名条目文件、把 url 指向别的仓库绕过了"没有新增文件"的门;"R 时 --name-only 打印新路径",恰好是要检查的那份。
- `git archive … | tar -x`:blob 只作数据进 /tmp/prdata,不执行任何东西。0001 增量:extract 步骤显式输出 `base` 供 listedReposAt 使用(注释:必须从 base commit 读,从 checkout 读则 PR 加的每个仓都像"早已收录")。
- **非 yml 扩展名的显式归因(0001 新增)**:extract 收集 data/plugins/ 下全部变更路径,而校验器只读 `*.yml`——扩展名丢失的条目会被计数、永不解析、永远进 failure 分支,#1477 因此被"重跑 workflow"搪塞了 13 天。现在全数非 yml 时直接报 "N entry file(s) missing the .yml extension",不再让作者空转。
- modified.txt:本 PR 改写的既有条目单独列出,M 类不走年龄/提交门(存量条目按收录时的规则,周度 decay scan 盯它们的退化),但**每一份判决都要附上这份清单**让评审追问:#1348 案(两次混过所有机械检查)正是这类。

### 判决翻译表(约 :198-311)

| 情形 | 结论 | 标题语义 |
|------|------|----------|
| 无新增+无修改 | success | "No entries changed" |
| 无新增但有修改 | success + modifiedNote | 列出所有被改写的既有条目 |
| 结果文件缺失 | failure | "The gate could not run"( checker 崩溃=bug 不是投稿问题)|
| tooMany | failure | 附全文拆分劝告 + "pick as well as split"(提前拒在 :518-541) |
| changed 全部无 .yml 扩展名 | failure | "N entry file(s) missing the .yml extension" + 逐文件 git mv 命令(0001 新增,pr-gate:263-289;#1477 曾挂 13 天被反复告知重跑 workflow) |
| checked===0 但 extract 说有文件 | failure | 两个组件互相矛盾,不能 vouch |
| ok 且有 incomplete | **neutral** | "X pass;其余放行但 nothing here vouches for them;Re-run to check properly" —— neutral 就是留给 regate 重访的钩子 |
| ok 全绿 | success | "dsh.bundle declared, repo old enough, enough commits" + modifiedNote(**上游遗留**:commit floor 已删但这句没改,pr-gate.yml:309) |
| 有 failures | failure | 每条逐点列出 + 指向 contributing.md |

## 待复核

- [x] neutral 在 regate 侧的重访闭环 → 见 [03](./03-regate-and-bleed.md)(已核)
- [ ] `concurrency.group: pr-gate-<head_sha>` cancel-in-progress 的实际效果(同一 head_sha 连续完成两次会互相取消?)UNVERIFIED,值得跑一次观察
