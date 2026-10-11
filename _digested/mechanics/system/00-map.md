# system · 全局运转图

> 状态:**0003 已复核**(源头、门禁、探针与部署 workflow 无 diff;站点投影新增 locale/category JSON catalog 与客户端虚拟卡片列表,详见 [site-surface](../site-surface/00-map.md))。最近核验:`4693e5a83`,2026-10-11。

## 定位

awesome-dsh-plugin 是一台**把人工编辑压缩到最小、其余全部机器再生产**的注册表:约 4489 个人工维护的小 YAML 投影成双语 README(由 main 合并后自动重生成,投稿者不再提交),再投影成数千页静态站点与 npm 目录包;收录由三道 fork-安全门禁把关;外部事实(stars/下载量/npm 归属/能力披露/存活)由探针家族夜间保鲜,失联条目进单一人审 issue。**0002 新增的两条外部防线**:一条盯**线上字节**(site-health,治"站点静默冻结"),一条盯**评论线程**(adopt-discussions,治"手工建的帖子 widget 读不到")。

## 一条 PR 的完整生命周期(0002 复核修订)

```text
贡献者                data/plugins/<owner>__<repo>.yml(唯一投稿物,README 不再随 PR 提交)
   │
   ├─ pr-check.yml(233 行,pull_request,fork 安全,零 token,**十步**)
   │    stale-fork 守卫(计数=条目文件数)→ .yml 扩展名守卫
   │    → 条目必须在 data/plugins/ 一层(否则静默不收录的自洽漏洞)
   │    → ⭐0002:改了生成 README 行却没有任何 data/plugins/ 变更 → 拒(#5845/#3168)
   │    → generate-readme --check(仅当 PR 自己动了 README;比对 base.sha...head.sha,
   │      ⭐0002 修:此前比 merge ref,主分支前进后被判假红——96 个开放 PR 里 18 个中招,#5796)
   │    → awesome-lint → ⭐0002:3 个纯规则 node --test(不联网/不要 token)
   │    → build-site 试跑(SKIP_PUBLISH_CHECKS=1)
   │
   ├─ pr-guard.yml(212 行,hourly '37 * * * *',从 main 调度、处在 PR 爆炸半径外)
   │    抓"没有检查会运行"的两态:删 workflow 文件的 PR / 动 .github 的 stale fork
   │
   ├─ pr-gate.yml(369 行,workflow_run 于 PR check 完成后,基础仓库上下文,有 token)
   │    解析 PR → merge-base 提取 AR 类条目文件(git archive 只取数据不执行)
   │    → check-submission:dsh.bundle / 仓库≥1天 / 每 PR≤3 条 / 已收录仓库豁免
   │    → ⭐0002:每个变更的 .yml 必须能被 js-yaml 解析,否则报 文件:行号(#4680 挂 5 天)
   │    → check-run 判决 success | neutral(fail-open 放行)| failure
   │
   └─ regate.yml(369 行,every 6h)+ 人评(contributing 八维度,CI 只是前置条件)
        ⭐0002 七类理由:never / stale / aged / unverified / faulted(gate 自己跑挂,1h 冷却)
          / checkStaleRed(红 check 比 check 自己的代码还旧)/ passStale;绿灯满 48h 重访
        ⭐0002:红 check 只在"新鲜"时否决;aged/unverified/faulted 三类照常重问(#5533)

   ⭐0002 新增旁路:held-rescan.yml(258 行,每日 06:19)
        held: author 已修好 → tracking issue;0002 起 **gate 从未运行**(分支与 main 冲突、
        无 merge ref,#2202)也入列,新增 gate 列 ✅/—,补救是维护者 rebase;绝不自动摘标签

merge → push main
   ├─ sync-readme.yml(106 行,escalated):在 main 上重生成双语 README 并提交
   │    ⭐0002:检出 ref: main(排队等到的 sha 早不是 main)+ 三轮
   │      fetch/reset --hard origin/main/regenerate/push,三轮都输就显式红
   │      (2026-09-19 README 陈旧了八小时);仍是全仓唯一 contents: write
   └─ build-site.yml(282 行):
        ⭐0002 新增触发 workflow_run on "Sync READMEs from data/plugins"
          ——bot 的 GITHUB_TOKEN 推送不触发 push,站点会永远慢一个 merge
        ⭐0002 探针门改事件白名单(schedule|workflow_dispatch):此前每次 README 同步
          都跑全量探针,有一次坐了 40 分钟(纯部署构建 ~12 分钟)
        push 构建:并发组 build-site-push(与 nightly 拆分)
        nightly('23 2 * * *',并发组 build-site-probe):PROBE_ALL 全量探针 → build-site
          → deploy pages(deploy 失败 continue-on-error,不拖垮发布)
          → 发布 dsh-plugin-catalog / dsh-plugin-updates 到 npm(OIDC)
        探针清单(0002):+probe-capabilities(dsh-trust-check 静态扫描 → data/capabilities.json,
          永远在跑,不进 PROBE_ALL 门控)
        nightly 还会把 probe-npm 的 version 字段刷进 plugins.json(dsh-market 消费)
         ⭐0003(#6105):首页/分类页只 SSR 前 24 张;构建另写 locale 全量与分类专属 catalog.json(均 hash-versioned),客户端虚拟化完整卡片列表;catalog 失败仅回退 24 张

⭐0002 新增:site-health.yml(46 行,每日 07:23)→ check-site-health.mjs(152 行)
     拉线上首页数 /p/ 链接,与 data/plugins 条目数比,落后 >tolerance(300)即红
     (dshmarket.com 曾静默冻结 18 天:3,363 页对 4,347 条,1,082 个插件没有页面)

⭐0002 新增:adopt-discussions.yml(65 行,discussion:created + 每周二 04:17 扫全量)
     把手工建的评论帖补上 giscus 的 sha1 marker 并移进 plugin 类目(不删/不并/不改标题)

decay-scan.yml(Mon 03:41):GraphQL 批扫全列表 → 单一 tracking issue,gone/archived/
    dormant/unbundled 四类 flag-only,不确定率>5% 熔断不发,永不自动删除
```

## 贯穿全局的五个设计决策

1. **README 是投影但也是枢纽。** YAML→README(generate-readme)、README→站点(build-site parseReadme)、README→探针花名册。一份数据两次投影,每次投影各配守卫(marker 替换 + 全文 URL 集合校验;bilingual parity 五检)。改数据只有一个入口,读数据却认 README——这是理解全仓库行为的钥匙。
2. **判决必须自我声明其局限。** gate 分不清「通过」与「没查过」时宁可显式失败;配额紧张放行的条目标 neutral 并留给 regate 重访;scan-decay 不确定率超 5% 整份报告不发;`check-site-health` 取数失败一律 exit 1。"a stale red gets noticed by its author, a stale green gets merged." **0002 把这句话推广成一条通则**:不仅 gate 判决会过期,**红 check 本身**也会过期(它可能是在门禁代码还旧的时候红的)。
3. **workflow 永不写仓库(唯一例外仍是 README bot)。** 部署链 `contents: read`;探针成果活在 git 快照(stars/downloads/capabilities)+ Actions cache + "与快照合并";唯一动 committed 文件的是维护者手动工具(prune-legacy-screenshots / maint-rebase)与 sync-readme.yml(bot 提交 README)。0002 新增的两条 workflow 都只读仓库(adopt-discussions 写 Discussions,site-health 只读网页)。
4. **错误信息承担教学职责,并按"谁该动"分向。** 该作者动手的:子路径写错给出候选目录与可粘贴修正、stale-fork 给三行恢复命令、"127 submissions wearing a coat" 的拆分劝告、**0002:非法 YAML 给文件:行号与复现命令**;时间能解决的:明说 "nothing to do, no need to resubmit";**0002 新增第三类——只有维护者能动的**:分支冲突导致 CI 从未运行 → held-rescan 入列并写明补救是 rebase。
5. **常量即事故刻度。** 每个阈值注释都指名一次翻车(#1348/#1554/#1608/#1619/#1635/#1673/#1701/#1794/#2797、2026-08-18 配额挤兑、2026-08-25 三义 403、#3512 catalog 冻结三天/#3417/#3698 READMEs 卡旧值/#4196 commit floor 误拦/8-30 218 个 README 冲突 PR/9-07 held 积压 11 件),0002 又添一批:**#4680 乱码挂 5 天、#5083 fault 挂 9 天、#932 超龄 run 打死 7/8 轮、#5533 被跳过 9 次、#5796 18/96 假红、#5845 README-only 投稿、#2202 分支冲突无人管、2026-09-15 两条目被改写到当天、2026-09-19 README 陈旧八小时、2026-09-22 探针误跑 40 分钟、dshmarket.com 冻结 18 天、2026-09-24 giscus 大小写劈线程**。读这份源码约等于读它的故障史——这正是它适合消化学习的原因。

## 规模事实(2026-10-11 实测)

条目 **4489** · 分类 23(ui 最大 781,agi 最小 17)· monorepo 子路径条目 **472**(来自 **316** 仓)· 上游节奏 0003 单次 **216 commits/18 天**(其中 172 个文件变化,主要是 registry 数据与 README;无 workflow 变更)· workflows **十条**(pr-check/pr-guard/pr-gate/regate/build-site/decay-scan/sync-readme/held-rescan/**site-health/adopt-discussions**)· scripts 约 **6184 行**(devDependencies:`js-yaml`、`marked`、**`dsh-trust-check@^0.1.13`**;0001 时"js-yaml 唯一运行时依赖"的表述已不再准确)· 站点自定义域 awesome-dsh-plugin.com(Pages + Cloudflare;含 AdSense 变量门控 + Giscus 评论,privacy 页已如实改写)· 0002 起仓库**首次有测试**(6 个 `*.test.mjs`)。

## 各专题导航

| 想搞懂 | 去 |
|--------|-----|
| 门禁五件套逐行机制 | [submission-gates](../submission-gates/00-map.md) |
| YAML↔README 双向管线 | [readme-pipeline](../readme-pipeline/00-map.md) |
| 数据 schema 与边车拓扑 | [registry-data](../registry-data/00-map.md) |
| 站点构建、模板契约、部署链、线上体检 | [site-surface](../site-surface/00-map.md) |
| 探针家族、能力披露、腐坏检测、评论线程 | [probes-and-decay](../probes-and-decay/00-map.md) |
