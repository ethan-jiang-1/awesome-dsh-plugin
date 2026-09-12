# system · 全局运转图

> 状态:**0001 已复核**(全景数据流按 `upstream@38976afd` 重核,五处机制变更已并入下图;细节判定见各专题 map)。最近核验:`38976afd`,2026-09-12。

## 定位

awesome-dsh-plugin 是一台**把人工编辑压缩到最小、其余全部机器再生产**的注册表:约 3552 个人工维护的小 YAML 投影成双语 README(**0001 起 README 由 main 合并后自动重生成,投稿者不再提交**),再投影成数千页静态站点与 npm 目录包;收录由三道 fork-安全门禁把关(提交门槛放宽:commit floor 已删);外部事实(stars/下载量/存活)由探针家族夜间保鲜,失联条目进单一人审 issue。**站点已接入 AdSense(变量门控)与 Giscus 评论**——"零第三方、无变现"的时代结束。

## 一条 PR 的完整生命周期(0001 复核修订)

```text
贡献者                data/plugins/<owner>__<repo>.yml(唯一投稿物,README 不再随 PR 提交)
   │
   ├─ pr-check.yml(pull_request,fork 安全,零 token)
   │    stale-fork 守卫(计数改为条目文件数)→ .yml 扩展名守卫
   │    → 新增:条目必须在 data/plugins/ 一层(否则静默不收录的自洽漏洞)
   │    → generate-readme --check(接受"只带 yml"与"带重生成 README"两种形态)
   │    → awesome-lint → build-site 试跑(SKIP_PUBLISH_CHECKS=1)
   │
   ├─ pr-guard.yml(hourly,'37 * * * *',从 main 调度、处在 PR 爆炸半径外)
   │    抓"没有检查会运行"的两态:删 workflow 文件的 PR / 动 .github 的 stale fork
   │
   ├─ pr-gate.yml(workflow_run 于 PR check 完成后,基础仓库上下文,有 token)
   │    解析 PR → merge-base 提取 AR 类条目文件(git archive 只取数据不执行)
   │    → check-submission:dsh.bundle / 仓库≥1天(⭐ commit floor ≥10 提交已删,
   │      #4196:"时间不可伪造,提交数可以 pad")/ 每 PR≤3 条
   │    → check-run 判决 success | neutral(fail-open 放行)| failure
   │
   └─ regate.yml(every 6h)+ 人评(contributing 八维度,CI 只是前置条件)
        四理由重跑:never/stale/aged-in/neutral;绿灯满 48h 重访(passStale)

merge → push main
   ├─ sync-readme.yml(⭐ 0001 新增):在 main 上重生成双语 README 并提交;
   │    动机:投稿者各自 regenerate 曾使 296 个 open PR 中 218 个互相冲突(8-30)
   │    终止性:第二次运行发现无 diff 即不提交,确定性由 generate-readme 保证
   └─ build-site.yml:
        push 构建:并发组 build-site-push(⭐ 与 nightly 拆分,#3512/#3417/#3698 同根因)
        nightly('23 2 * * *',并发组 build-site-probe):PROBE_ALL 全量探针 → build-site
          → deploy pages(deploy 失败 continue-on-error,不拖垮发布)
          → 发布 dsh-plugin-catalog / dsh-plugin-updates 到 npm(OIDC)
        nightly 还会把 probe-npm 的 version 字段刷进 plugins.json(dsh-market 消费)
held-rescan.yml(⭐ 0001 新增,每日 06:19):重扫 `held: author` 已修好的 PR,
    只维护一个 tracking issue(2026-09-07 救回 11 个积压),不自动摘标签
decay-scan.yml(Mon 03:41):GraphQL 批扫全列表 → 单一 tracking issue,gone/archived/
    dormant/unbundled 四类 flag-only,不确定率>5% 熔断不发,永不自动删除
```

## 贯穿全局的五个设计决策

1. **README 是投影但也是枢纽。** YAML→README(generate-readme)、README→站点(build-site parseReadme)、README→探针花名册。一份数据两次投影,每次投影各配守卫(marker 替换 + 全文 URL 集合校验;bilingual parity 五检)。改数据只有一个入口,读数据却认 README——这是理解全仓库行为的钥匙。
2. **判决必须自我声明其局限。** gate 分不清「通过」与「没查过」时宁可显式失败;配额紧张放行的条目标 neutral 并留给 regate 重访;scan-decay 不确定率超 5% 整份报告不发。"a stale red gets noticed by its author, a stale green gets merged."
3. **workflow 永不写仓库(0001 出现唯一例外)。** 部署链 `contents: read`;探针成果活在 git 快照(stars/downloads/updates)+ Actions cache(共享 entry probe-data-v2 四 path + downloads-v1/updates-v1)+"与快照合并";唯一动 committed 文件的是维护者手动工具(prune-legacy-screenshots / maint-rebase)**和新 bot sync-readme.yml(代投稿者做 README 重生成提交)——这是"永不写仓库"原则为消灭 218/296 冲突开的唯一口子**。
4. **错误信息承担教学职责,并按"谁该动"分向(0001 深化)。** 该作者动手的:子路径写错给出候选目录与可粘贴修正、stale-fork 给出三行恢复命令、"127 submissions wearing a coat" 的拆分劝告;时间能解决的(仓库太新):明说 "nothing to do, no need to resubmit"——regate 每 6 小时自动翻绿,不再驱使人关-重开。整个贡献体验被当作产品来写。
5. **常量即事故刻度。** 每个阈值注释都指名一次翻车(#1348/#1554/#1608/#1619/#1635/#1673/#1701/#1794/#2797、2026-08-18 配额挤兑、2026-08-25 三义 403、0001 新增 #3512 catalog 冻结三天/#3417/#3698 READMEs 卡旧值/#4196 commit floor 误拦/8-30 218 个 README 冲突 PR/9-07 held 积压 11 件)。读这份源码约等于读它的故障史——这正是它适合消化学习的原因。

## 规模事实(2026-09-12 实测)

条目 3552 · 分类 23(ui 最大 592,agi 最小 6)· monorepo 子路径条目 383(来自 259 仓)· 上游节奏 0001 单次 3213 commits/15 天(squash-style,PR 号入题)· workflows 八条(pr-check/pr-guard/pr-gate/regate/build-site/decay-scan/sync-readme/held-rescan)· scripts 约 4400 行(js-yaml 唯一运行时依赖;marked 仅详情页正文渲染用)· 站点自定义域 awesome-dsh-plugin.com(Pages + Cloudflare;0001 起含 AdSense 变量门控 + Giscus 评论,privacy 页已如实改写)。

## 各专题导航

| 想搞懂 | 去 |
|--------|-----|
| 门禁五件套逐行机制 | [submission-gates](../submission-gates/00-map.md) |
| YAML↔README 双向管线 | [readme-pipeline](../readme-pipeline/00-map.md) |
| 数据 schema 与边车拓扑 | [registry-data](../registry-data/00-map.md) |
| 站点构建、模板契约、部署链 | [site-surface](../site-surface/00-map.md) |
| 探针家族与腐坏检测 | [probes-and-decay](../probes-and-decay/00-map.md) |
