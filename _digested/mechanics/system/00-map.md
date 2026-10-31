# system · 全局运转图

> 状态:**0004 已复核**(workflow 数不变,**十条**;但六个带 `npm ci` 的 workflow 统一加了 npmjs registry 覆盖,`build-site` 多了 `skip_probes` 手动输入,`pr-check` 多了一步 entry-path 测试。源码侧新增一个对外产物——DSH 市场索引 `docs/index.json`,由 `@deepseek-ai/dsh-plugin-market-index`(锁在 `0.2.1-alpha.4`)校验后随 catalog 发布——外加 `build-index.mjs` / `lib/market-index.mjs` / `capability-changes.mjs` 三个新脚本与两个新测试;`dsh-trust-check` 升到 0.2.1)。最近核验:`b4d0049a8`,2026-10-24。

## 定位

awesome-dsh-plugin 是一台**把人工编辑压缩到最小、其余全部机器再生产**的注册表:约 **7924** 个人工维护的小 YAML 投影成双语 README(由 main 合并后自动重生成,投稿者不再提交),再投影成数千页静态站点、一个 npm 目录包,以及(0004 起)一份 **format-1 插件市场索引**;收录由三道 fork-安全门禁把关;外部事实(stars/下载量/npm 归属/能力披露/存活)由探针家族夜间保鲜,失联条目进单一人审 issue。**0002 新增的两条外部防线**:一条盯**线上字节**(site-health,治"站点静默冻结"),一条盯**评论线程**(adopt-discussions,治"手工建的帖子 widget 读不到")。

## 一条 PR 的完整生命周期(0004 复核修订)

```text
贡献者                data/plugins/<owner>__<repo>.yml(唯一投稿物,README 不再随 PR 提交)
   │
   ├─ pr-check.yml(244 行,pull_request,fork 安全,零 token,**十一步**)
   │    stale-fork 守卫(计数=条目文件数)→ .yml 扩展名守卫
   │    → 条目必须在 data/plugins/ 一层(否则静默不收录的自洽漏洞)
   │    → ⭐0002:改了生成 README 行却没有任何 data/plugins/ 变更 → 拒(#5845/#3168)
   │    → generate-readme --check(仅当 PR 自己动了 README;比对 base.sha...head.sha,
   │      ⭐0002 修:此前比 merge ref,主分支前进后被判假红——96 个开放 PR 里 18 个中招,#5796)
   │    → awesome-lint
   │    → ⭐0004:4 个纯规则 node --test(added-date / capability / discussion / entry-path,
   │      不联网、不要 token;新增那个专治 Windows 上 `file` 与 git 输出比不中)
   │    → build-site 试跑(SKIP_PUBLISH_CHECKS=1)
   │    这些步骤的 npm ci 从 ⭐0004 起钉死 registry.npmjs.org(见"规模事实")
   │
   ├─ pr-guard.yml(212 行,hourly '37 * * * *',从 main 调度、处在 PR 爆炸半径外)
   │    抓"没有检查会运行"的两态:删 workflow 文件的 PR / 动 .github 的 stale fork
   │
   ├─ pr-gate.yml(375 行,workflow_run 于 PR check 完成后,基础仓库上下文,有 token)
   │    解析 PR → merge-base 提取 AR 类条目文件(git archive 只取数据不执行)
   │    → check-submission:dsh.bundle / 仓库≥1天 / 每 PR≤3 条 / 已收录仓库豁免
   │    → ⭐0002:每个变更的 .yml 必须能被 js-yaml 解析,否则报 文件:行号(#4680 挂 5 天)
   │    → check-run 判决 success | neutral(fail-open 放行)| failure
   │    ⭐0004:check-submission 拿到的 file 已是 POSIX 路径,"没跑"不再伪装成"通过"
   │      (此前的 Windows 路径 bug 会让它直接回 ok:true / checked:0 退出)
   │
   └─ regate.yml(369 行,every 6h)+ 人评(contributing 八维度,CI 只是前置条件)
        ⭐0002 七类理由:never / stale / aged / unverified / faulted(gate 自己跑挂,1h 冷却)
          / checkStaleRed(红 check 比 check 自己的代码还旧)/ passStale;绿灯满 48h 重访
        ⭐0002:红 check 只在"新鲜"时否决;aged/unverified/faulted 三类照常重问(#5533)

   ⭐0002 新增旁路:held-rescan.yml(258 行,每日 06:19)
        held: author 已修好 → tracking issue;0002 起 **gate 从未运行**(分支与 main 冲突、
        无 merge ref,#2202)也入列,新增 gate 列 ✅/—,补救是维护者 rebase;绝不自动摘标签

merge → push main
   ├─ sync-readme.yml(112 行,escalated):在 main 上重生成双语 README 并提交
   │    ⭐0002:检出 ref: main(排队等到的 sha 早不是 main)+ 三轮
   │      fetch/reset --hard origin/main/regenerate/push,三轮都输就显式红
   │      (2026-09-19 README 陈旧了八小时);仍是全仓唯一 contents: write
   │    ⭐0004:只多了 npm ci 的 registry env(+6 行),重生成逻辑未动
   └─ build-site.yml(298 行):
        ⭐0002 新增触发 workflow_run on "Sync READMEs from data/plugins"
          ——bot 的 GITHUB_TOKEN 推送不触发 push,站点会永远慢一个 merge
        ⭐0002 探针门改事件白名单(schedule|workflow_dispatch):此前每次 README 同步
          都跑全量探针,有一次坐了 40 分钟(纯部署构建 ~12 分钟)
        ⭐0004:workflow_dispatch 新增 skip_probes=true(部署修复不必等一小时探针;
          2026-10-18 索引要赶在用户已经在用的时候上线)
        push 构建:并发组 build-site-push(与 nightly 拆分)
        nightly('23 2 * * *',并发组 build-site-probe):PROBE_ALL 全量探针 → build-site
          → deploy pages(deploy 失败 continue-on-error,不拖垮发布)
          → 发布 dsh-plugin-catalog / dsh-plugin-updates 到 npm(OIDC)
        探针清单(0002):+probe-capabilities(dsh-trust-check 静态扫描 → data/capabilities.json,
          永远在跑,不进 PROBE_ALL 门控);0004 扫描器升到 0.2.1,但仓库里那份边车
          仍是 0.1.13 / 2026-09-24 的旧快照
        nightly 还会把 probe-npm 的 version 字段刷进 plugins.json(dsh-market 消费);
          ⭐0004 probe-npm 另记每个版本的发布时间与 engines.dsh(供 Discover 做兼容性过滤)
        ⭐0004:逐条写进 docs/plugins.json 的可选 icon;并产出 docs/index.json
          (format 1 市场索引,只收"有 npm 包 + 精确版本 + 发布时间"的条目,
           纯 GitHub 条目在 format 1 里无表达式),发布前用 host 端同一个 parser 校验
         ⭐0003(#6105):首页/分类页只 SSR 前 24 张;构建另写 locale 全量与分类专属 catalog.json(均 hash-versioned),客户端虚拟化完整卡片列表;catalog 失败仅回退 24 张

⭐0002 新增:site-health.yml(46 行,每日 07:23)→ check-site-health.mjs(168 行,0003 时 152)
     与 data/plugins 条目数比,落后 >tolerance(300)即红
     (dshmarket.com 曾静默冻结 18 天:3,363 页对 4,347 条,1,082 个插件没有页面)
     ⭐0004:页面数改从 /sitemap.xml 取,不再数首页的 /p/ 链接——首页从 0003 起只 SSR
       24 张 + 客户端虚拟化,数首页等于数窗口;2026-10-10 起该检查每天假红,
       10-19 报出 48 页对 5,945 条

⭐0002 新增:adopt-discussions.yml(71 行,discussion:created + 每周二 04:17 扫全量)
     把手工建的评论帖补上 giscus 的 sha1 marker 并移进 plugin 类目(不删/不并/不改标题)

decay-scan.yml(Mon 03:41):GraphQL 批扫全列表 → 单一 tracking issue,gone/archived/
    dormant/unbundled 四类 flag-only,不确定率>5% 熔断不发,永不自动删除
```

## 贯穿全局的五个设计决策

1. **README 是投影但也是枢纽。** YAML→README(generate-readme)、README→站点(build-site parseReadme)、README→探针花名册。一份数据两次投影,每次投影各配守卫(marker 替换 + 全文 URL 集合校验;bilingual parity 五检)。改数据只有一个入口,读数据却认 README——这是理解全仓库行为的钥匙。
2. **判决必须自我声明其局限。** gate 分不清「通过」与「没查过」时宁可显式失败;配额紧张放行的条目标 neutral 并留给 regate 重访;scan-decay 不确定率超 5% 整份报告不发;`check-site-health` 取数失败一律 exit 1。"a stale red gets noticed by its author, a stale green gets merged." **0002 把这句话推广成一条通则**:不仅 gate 判决会过期,**红 check 本身**也会过期(它可能是在门禁代码还旧的时候红的)。**0004 补了一个反面样本**:Windows 路径 bug 期间,check-submission 在"一条都没比对到"时写下 `ok:true, checked:0` 就退出——`ok` 为真而 `checked` 为零,两个字段各自都"对",合起来是一次假通过。这一层唯一的兜底在 pr-gate:它把 `checked === 0` 当真异常,报一条红 check 说 "The gate checked nothing"——说白了是**下一层替上一层擦屁股**,脚本自己并没有承认"我没跑"。**判决的正确性不能只由判决自己声明。**
3. **workflow 永不写仓库(唯一例外仍是 README bot)。** 部署链 `contents: read`;探针成果活在 git 快照(stars/downloads/capabilities)+ Actions cache + "与快照合并";唯一动 committed 文件的是维护者手动工具(prune-legacy-screenshots / maint-rebase)与 sync-readme.yml(bot 提交 README)。0002 新增的两条 workflow 都只读仓库(adopt-discussions 写 Discussions,site-health 只读网页)。**0004 的两个新产物也不破坏这条**:`docs/plugins.json` 的 `icon` 与 `docs/index.json` 都写在 `docs/` 下,而 `docs/` 在 `.gitignore` 里(:9),构建只把它交给 Pages/npm,从不提交。
4. **错误信息承担教学职责,并按"谁该动"分向。** 该作者动手的:子路径写错给出候选目录与可粘贴修正、stale-fork 给三行恢复命令、"127 submissions wearing a coat" 的拆分劝告、**0002:非法 YAML 给文件:行号与复现命令**;**0004:`icon` 报错点名违规值(如 "must be hosted on GitHub (got evil.example)"/"must point at a raster image"),但不列出允许的四台主机——方向对、照做不了,见 [submission-gates](../submission-gates/00-map.md)**;时间能解决的:明说 "nothing to do, no need to resubmit";**0002 新增第三类——只有维护者能动的**:分支冲突导致 CI 从未运行 → held-rescan 入列并写明补救是 rebase。**0004 的 registry 覆盖注释属于同一类**:它解释了为什么 CI 要绕过 lockfile 里的源(2026-10-19 的 503/504),让下一个人不必再猜一遍。
5. **常量即事故刻度。** 每个阈值注释都指名一次翻车(#1348/#1554/#1608/#1619/#1635/#1673/#1701/#1794/#2797、2026-08-18 配额挤兑、2026-08-25 三义 403、#3512 catalog 冻结三天/#3417/#3698 READMEs 卡旧值/#4196 commit floor 误拦/8-30 218 个 README 冲突 PR/9-07 held 积压 11 件),0002 又添一批:**#4680 乱码挂 5 天、#5083 fault 挂 9 天、#932 超龄 run 打死 7/8 轮、#5533 被跳过 9 次、#5796 18/96 假红、#5845 README-only 投稿、#2202 分支冲突无人管、2026-09-15 两条目被改写到当天、2026-09-19 README 陈旧八小时、2026-09-22 探针误跑 40 分钟、dshmarket.com 冻结 18 天、2026-09-24 giscus 大小写劈线程**,0004 再添三条:**2026-10-19 npmmirror 的 503/504 把 `npm ci` 挂住几十分钟、2026-10-10 起 site-health 因首页改虚拟化而每天假红(10-19 报 48 页对 5,945 条)、2026-10-18 索引修好却等不起一小时探针(才有了 `skip_probes`)**。读这份源码约等于读它的故障史——这正是它适合消化学习的原因。

## 规模事实(2026-10-31 实测)

条目 **7924**(7 天 6704→7924,+1220 / +18.2%)· owners **5114**(0004:4298)· 分类 23(ui 最大 **1558**,agi 最小 **54**;前五类占 51.8%)· monorepo 子路径条目 **797**(来自 **523** 仓;0004:689/461)· 上游节奏 0005 单次 **2149 commits / 7 天**(1535 个文件、+59254/−48989,其中 `data/plugins/` 1528 个文件;**workflow 数不变**)· workflows **十条**(pr-check/pr-guard/pr-gate/regate/build-site/decay-scan/sync-readme/held-rescan/**site-health/adopt-discussions**;0005 无增删,行数同 0004)· scripts **6952 行 / 38 个 `.mjs`**(与 0004 相同,0005 零 diff)· 站点自定义域 awesome-dsh-plugin.com(Pages + Cloudflare;含 AdSense 变量门控 + Giscus 评论,privacy 页已如实改写)· **8 个 `*.test.mjs`**。

**依赖(0004 动了两处,连带进来六个包;0005 未动)。** devDependencies 五条:`js-yaml`、`marked`、`semver@^7.8.5`、`@deepseek-ai/dsh-plugin-market-index@^0.2.1-alpha.4`、`dsh-trust-check@^0.2.1`(0003 时是 `^0.1.13`);锁文件的包条目 6→12。全部是构建期依赖,没有运行时依赖;`package.json` 没有 `scripts` 段,入口一律 `node scripts/*.mjs`,测试一律 `node --test`。唯一的**预发布**依赖是市场索引那个包(alpha.4),而它不在边缘:**它在站点构建的路径上**——`lib/market-index.mjs` 用它逐条校验(校验失败的条目只丢那一行并计数,:145)再整份校验(:154),整份不过就直接抛错。所以这颗 alpha 的 bug 同时能打掉"索引"和"站点构建"两件事,不是"装不上就跳过"。它自己又要求 `@deepseek-ai/dsh-package-manifest` **精确 0.2.1-alpha.4**(无 caret)与 peer `@deepseek-ai/cordis@~4.0.5-alpha.2`,这条 alpha 链被锁文件钉死,不会自己漂,但也意味着**升级要人工看一眼**。

**CI 可复现性(0004 变复杂了,值得记住;0005 无变化)。** 锁文件 12 个包条目里,带 `resolved` 的 11 个有 **7 个钉在 `registry.npmmirror.com`、4 个在 `registry.npmjs.org`**;而六个跑 `npm ci` 的 workflow 统一强制 `npm_config_registry=https://registry.npmjs.org/` + `npm_config_replace_registry_host=always`。也就是说 **lockfile 记的源 ≠ CI 实际取的源**,两者靠这条环境变量对齐,内容正确性只剩 `integrity` 哈希一道校验。本地安装没有这层覆盖,仍按 lockfile 走镜像——"本地能装"与"CI 能装"依赖两个不同的源,这是 0004 引入的新耦合,也是下一次装包挂住时第一个该看的地方。

## 各专题导航

| 想搞懂 | 去 |
|--------|-----|
| 门禁五件套逐行机制 | [submission-gates](../submission-gates/00-map.md) |
| YAML↔README 双向管线 | [readme-pipeline](../readme-pipeline/00-map.md) |
| 数据 schema 与边车拓扑 | [registry-data](../registry-data/00-map.md) |
| 站点构建、模板契约、部署链、线上体检 | [site-surface](../site-surface/00-map.md) |
| 探针家族、能力披露、腐坏检测、评论线程 | [probes-and-decay](../probes-and-decay/00-map.md) |
