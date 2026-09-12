# submission-gates · 提交与门禁

> 状态:**0001 已复核**(门禁逐行重核;行数 pr-check 82→146、check-submission 529→584、pr-gate 275→316、regate 197→218;新增 held-rescan.yml 233 行)。最近核验:`38976afd`,2026-09-12。

## 定位

一个日均约 90 个 commit 的注册表,人工 review 是瓶颈也是最后防线。机器门禁的职责因此非常明确:**把形式问题在合并前拦下,并保证「没有核验过」永远不会被读成「已核验」**。这个专题记录六条 workflow + 两个校验脚本如何构成这台防线(0001:结构从"五条门禁"改为 **3 道准入门 + 2 条保鲜线 + 1 条监督线**——held-rescan 不做判决,是队列保鲜线,与 regate 构成"stale green 会被合并"哲学的机器/人工两个半区)。

## 设计原则(从源码与注释中提炼)

1. **fork 安全优先于一切。** 面向 fork PR 的 `pull_request` job 没有 token(`pr-check.yml`),所有需要认证 API 的检查挪进 `workflow_run` 触发的 `pr-gate.yml`,在基础仓库上下文里跑;checkout 永远停在 main,PR 的 YAML 只作为数据被 `git archive` 抽出,**绝不执行来自 PR 的任何代码**(`pr-gate.yml:9-15` 有显式 SECURITY 注释)。
2. **判决是快照,会过期。** regate 用四类理由重跑:从未被判、判决早于当前门禁代码、"时间能解决"的失败(仓库太新;提交数门槛已删但 summary 正则仍留 `commit(s)` 兼容旧判决)、neutral(fail-open 放行的未核验);连绿灯满 48 小时也会被重查(`regate.yml`)。
3. **门槛过滤的是仓库,不是投稿动作。** 0001 新增已收录仓库豁免(`listedReposAt(base)`,从条目**文件名**解析 owner/repo,base 读不到一律视为"全部新仓库"fail-closed)——在自己仓里挪目录的插件不再被重新审判(#1554 的改名绕过检查原样保留:改名落到未收录仓库仍受全量审查)。
3. **fail-open 但必须自曝。** 配额挤兑时条目放行但标 neutral,"nothing here vouches for them";检查器自身崩溃明确写成 failure 而非静默绿。这条纪律源自 2026-08-18 六个不达标条目因 403 与正常通过不可区分而变绿的翻车。
4. **错误信息替作者写好下一步,并按"谁该动"分向(0001 深化)。** 该作者动手的:给可粘贴命令(路径/扩展名错 → `git mv`;子路径写错 → fuzzy 候选目录与修正 YAML,`check-submission.mjs:300-356`);时间能解决的:**明说什么都不用做**——age 文案改为 "nothing to do: this check re-runs by itself"(旧文案曾诱导关-重开/force-push 空提交),regate 按 `/days old/` 每 6 小时自动翻绿。
5. **每个常量都是事故刻度。** 见各正文中的事故索引。

## 3 道准入门 + 2 条保鲜线 + 1 条监督线

### 准入门

| workflow | 触发 | 权限面 | 职责 |
|----------|------|--------|------|
| [`pr-check.yml`](./01-pr-check-and-guard.md) | `pull_request`(含 fork) | 无 token | 形式层:stale-fork 守卫、`.yml` 扩展名守卫、README 同步、awesome-lint、站点构建(SkipPublishChecks) |
| [`pr-gate.yml`](./02-pr-gate-and-check-submission.md) | `workflow_run: PR check completed` | 有 token | 实质层:dsh.bundle 清单、仓库年龄≥1天(**提交数门槛已删**,#4196)、每 PR ≤3 条、**已收录仓库豁免**;产出 check-run 判决 |
| [`pr-guard.yml`](./01-pr-check-and-guard.md) | schedule `37 * * * *` + 手动 | 元检查 | 抓两类"其他检查根本不会运行"的状态:删掉 workflow 文件的 PR(#1635)、动了 `.github/` 的 stale fork(#1614/#1635) |
### 保鲜线

| [`regate.yml`](./03-regate-and-bleed.md) | schedule `19 */6 * * *` + 手动 | 重跑驱动 | 机器判决保鲜:理由不变(never/stale/aged/unverified + passStale),调度改三层 blocking→revalidate→speculative(0001),每轮 ≤20 次 |
| [`held-rescan.yml`](./02-pr-gate-and-check-submission.md)(0001 新增,233 行) | schedule `19 6 * * *` | issues:write | **人工 held 保鲜**:每日列出"已修好仍挂 `held: author`"的 PR 到单一 tracking issue(09-07 手动重扫救回 11 个积压,#2233 挂 17 天 ping 3 次);NEUTRAL 明确不算过;时钟取 label 最后施加事件;红 check 只展示不过滤(#3832 后 README 红多为分支陈旧伪影);**绝不自动摘 label** |

### 监督线
| `held-rescan.yml`(0001 新增) | schedule `19 6 * * *` | issues: write | 重扫 `held: author` 已修好的 PR,维护单个 tracking issue(2026-09-07 救回 11 个积压);**不自动摘标签**——held 是人工判断,只有重评审能摘 |
| `sync-readme.yml` | 归 [readme-pipeline](../readme-pipeline/00-map.md) | contents: write | 仓库唯一向 main 写入的 workflow(bot 提交 README) |
| `decay-scan.yml` | 归 [probes-and-decay](../probes-and-decay/00-map.md) | — | 收录后的持续监督,不属于准入 |

配套脚本:[`check-submission.mjs`](./02-pr-gate-and-check-submission.md)(584 行,实质校验)、[`check-bleed.mjs`](./03-regate-and-bleed.md)(94 行,描述串染检测,#1348,未变)。

## 评审哲学(contributing.md 是合同,CI 只是前置条件)

"CI 通过是前置条件,不是结论"(contributing.md:90)。**八个评审维度**(0001:+7 纯聚合包不单收,范例 hyzyn/dsh-plugin-kit、wingsky-1/dsh-plugin-hub;+8 依赖须指向原作者):描述与代码一致(写"46 个工具"就要数出 46 个)、分类合理(永不打回,维护者直接改)、真实可用代码、是否重复收录(规则不是先来后到,是谁更好)、源码无可疑行为(常识检查而非安全审计)、PR 不碰无关条目、聚合包、依赖归属。表述基调:「我们不是插件好坏的裁判」。

## 待回答的问题

- [x] check-bleed 查什么 → 见 [03](./03-regate-and-bleed.md):跨条目共享 40 字符以上描述文本即报,报而不拦
- [x] 哪些规则给出自动修正建议 → 子路径修正、根指向改子包、stale-fork 三行修复命令
- [x] ISSUE_TEMPLATE 关系 → 问题分流模板:市场 UI 问题去 dsh-market,dsh 本体问题去官方仓,插件 bug 去插件自己仓库;本仓库只收"清单本身坏了"
- [ ] decay scan 如何执行"经确认后移除"的人工环节(归 probes 专题,待补)

## 正文

- [01 · pr-check 与 pr-guard:fork 安全层与元检查](./01-pr-check-and-guard.md)
- [02 · pr-gate 与 check-submission:判决机](./02-pr-gate-and-check-submission.md)
- [03 · regate 与 check-bleed:判决保鲜与描述污染检测](./03-regate-and-bleed.md)
