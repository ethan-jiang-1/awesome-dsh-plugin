# system · 全局运转图

> 状态:**进行中**(全景数据流已核验;各环节细节见姊妹专题,行号引用以 `main@5e7dc7eb` 为基线)。最近核验:`5e7dc7eb`,2026-08-27。

## 定位

awesome-dsh-plugin 是一台**把人工编辑压缩到最小、其余全部机器再生产**的注册表:约 2286 个人工维护的小 YAML 投影成 600KB 双语 README,再投影成约 4600 页静态站点与 npm 目录包;收录由三道 fork-安全门禁把关;外部事实(stars/下载量/存活)由九个探针每周夜间保鲜,失联条目进单一人审 issue。

## 一条 PR 的完整生命周期(已核验主干)

```text
贡献者                data/plugins/<owner>__<repo>.yml(+再生双语 README)
   │
   ├─ pr-check.yml(pull_request,fork 安全,零 token)
   │    stale-fork 守卫 → .yml 扩展名守卫 → generate-readme --check
   │    → awesome-lint → build-site 试跑(SKIP_PUBLISH_CHECKS=1)
   │
   ├─ pr-guard.yml(hourly,'37 * * * *',从 main 调度、处在 PR 爆炸半径外)
   │    抓"没有检查会运行"的两态:删 workflow 文件的 PR / 动 .github 的 stale fork
   │
   ├─ pr-gate.yml(workflow_run 于 PR check 完成后,基础仓库上下文,有 token)
   │    解析 PR → merge-base 提取 AR 类条目文件(git archive 只取数据不执行)
   │    → check-submission:dsh.bundle / 仓库≥1天 / ≥10提交 / 每 PR≤3 条
   │    → check-run 判决 success | neutral(fail-open 放行)| failure
   │
   └─ regate.yml(every 6h)+ 人评(contributing 六维度,CI 只是前置条件)
        四理由重跑:never/stale/aged-in/neutral;绿灯满 48h 重访(passStale)

merge → push main
   └─ build-site.yml:
        push 构建:缓存命中则跳过五个 probe,只跑 tarballs+screenshots+build-site
        nightly('23 2 * * *'):PROBE_ALL 全量探针 → build-site → deploy pages
          → deploy 后发布 dsh-plugin-catalog / dsh-plugin-updates 到 npm(OIDC)
decay-scan.yml(Mon 03:41):GraphQL 批扫全列表 → 单一 tracking issue,gone/archived/
   dormant/unbundled 四类 flag-only,不确定率>5% 熔断不发,永不自动删除
```

## 贯穿全局的五个设计决策

1. **README 是投影但也是枢纽。** YAML→README(generate-readme)、README→站点(build-site parseReadme)、README→探针花名册。一份数据两次投影,每次投影各配守卫(marker 替换 + 全文 URL 集合校验;bilingual parity 五检)。改数据只有一个入口,读数据却认 README——这是理解全仓库行为的钥匙。
2. **判决必须自我声明其局限。** gate 分不清「通过」与「没查过」时宁可显式失败;配额紧张放行的条目标 neutral 并留给 regate 重访;scan-decay 不确定率超 5% 整份报告不发。"a stale red gets noticed by its author, a stale green gets merged."
3. **workflow 永不写仓库。** 部署链 `contents: read`;探针成果活在 git 快照(stars/downloads/updates)+ Actions cache(npm-map/readmes/tarballs)+"与快照合并";唯一动 committed 文件的是维护者手动工具(prune-legacy-screenshots / maint-rebase)。
4. **错误信息承担教学职责。** 太新的仓库被告知几小时后重交;子路径写错给出候选目录与可粘贴修正;stale-fork 给出三行恢复命令;"127 submissions wearing a coat" 的拆分劝告。整个贡献体验被当作产品来写。
5. **常量即事故刻度。** 每个阈值注释都指名一次翻车(#1348/#1554/#1608/#1619/#1635/#1673/#1701/#1794/#2797、2026-08-18 配额挤兑、2026-08-25 三义 403)。读这份源码约等于读它的故障史——这正是它适合消化学习的原因。

## 规模事实(2026-08-27 实测)

条目 2286 · 分类 22(ui 最大 358,identity 最小 4)· monorepo 子路径条目 229 · 上游节奏近 30 天 ~2700 commits(squash-style,PR 号入题)· workflows 五条约 1000 行 · scripts 约 4300 行(js-yaml 唯一运行时依赖;marked 仅详情页正文渲染用)· 站点自定义域 awesome-dsh-plugin.com(Pages + Cloudflare,无 cookie 统计)。

## 各专题导航

| 想搞懂 | 去 |
|--------|-----|
| 门禁五件套逐行机制 | [submission-gates](../submission-gates/00-map.md) |
| YAML↔README 双向管线 | [readme-pipeline](../readme-pipeline/00-map.md) |
| 数据 schema 与边车拓扑 | [registry-data](../registry-data/00-map.md) |
| 站点构建、模板契约、部署链 | [site-surface](../site-surface/00-map.md) |
| 探针家族与腐坏检测 | [probes-and-decay](../probes-and-decay/00-map.md) |
