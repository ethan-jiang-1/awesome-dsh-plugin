# site-surface · 站点

> 状态:**0005 无对应 diff**(基线 `upstream@efe602e7b`,2026-10-31;`build-site.mjs`、`site/`、locales 零 diff)。0003 把首页/分类页改成 24 张 SSR 回退卡 + JSON catalog 虚拟列表;0004 在此之上多出**第三个发布面**——把名单本身导出为 DSH 插件市场索引(`docs/index.json`,format 1),首页搜索条下多一行"索引源"地址;site-health 的取证点从窗口化首页挪到 `sitemap.xml`;卡片安装命令补回作者声明的 tarball 一级。最近核验:`efe602e7b`。

## 定位

`site/` + `scripts/build-site.mjs` 是注册表的第二个发布面:从同一份名单长出约 **1.59 万个 HTML 页面**(7924 条目 ×2 语言详情页 + 每 locale 的首页/23 分类页/隐私页;条目数取自 `git ls-tree HEAD data/plugins/` 的 7924 个 yml,按构建逻辑推算,非构建日志读数)+ 8 个全站数据产物,并额外为首页与各有条目的分类页生成语言/分类专属 `catalog.json`;共最多 **48 个 catalog 文件**(每语言 1 首页 + 23 个分类页,当前 23 类均有条目)。静态 HTML 与 JSON 部署到 GitHub Pages(`site/assets/CNAME` = awesome-dsh-plugin.com),前端由 Cloudflare 加速。首页/分类页只 SSR 下载排名前 24 张卡;JavaScript 加载 catalog 后按视口窗口化渲染全量列表,失败则退回这 24 张,`<noscript>` 明示仅有首屏内容。catalog URL 带内容 hash query 防 CDN 旧缓存。统计(Cloudflare Web Analytics)无 cookie,但站点**有条件地**携带两个第三方:Google AdSense(构建变量 `ADSENSE_CLIENT` 设定时进入每个首页/分类/详情页,隐私页除外,当前变量未设=字节级无广告)与 Giscus 评论(仅当访客把评论面板滚到视口附近)。

**第三个发布面是文档而不是页面。** `docs/index.json` 是 DSH 0.2.1 引入的 plugin market index(format 1):host 在官方 Plugins → Discover 与 `plugin_market` agent tool 里把它当 market source 读。构建用 `@deepseek-ai/dsh-plugin-market-index`(host 端同一个 parser)校验,注释里的目标是"从这里出去的文档不可能是 DSH 拒绝的那一份"。同一份字节走两条路:Pages 根(`awesome-dsh-plugin.com/index.json`)与 npm 包 `dsh-plugin-catalog`;首页和两份 README 给的是后者(`cdn.jsdelivr.net/npm/dsh-plugin-catalog/index.json`),理由是 host 的取数预算固定 15 s,而当时 3.1 MB 的 Pages 版从大陆网络实测要 22.7 s、同一份文件走 jsDelivr 约 1 s(提交信息实测,非本地复算)。**覆盖面只有 npm 条目**:需要包名、精确版本与该版本发布时间三件套;纯 GitHub 条目在 format 1 里没有表达式(每个 Git 版本要 commit SHA,本仓库不记录),upstream 自述约占名单一半。

0002 新增一条与"发布面"并列的**监督面**:`.github/workflows/site-health.yml` + `scripts/check-site-health.mjs`(168 行,0003 时 152)每天 07:23 取线上 `sitemap.xml`,数去重后的英文 `/p/<slug>` 页面,与 `data/plugins/` 的条目数比对,落后超过 tolerance(默认 300)即失败。注释交代了动机:dshmarket.com 曾在 2026-09-09 → 09-25 **静默冻结 18 天**(3,363 页对 4,347 条,1,082 个插件根本没有页面)而仓库里毫无痕迹;同一段注释还把"schedule 根本不再触发"(GitHub 对 60 天无活动的仓库会停掉定时任务)算进覆盖范围。它刻意**不**与已发布的 catalog 比对——"页与 catalog 出自同一次构建,拿站点比自己的 catalog 等于比自己"。取数失败一律 exit 1(检查不了 ≠ 全好)。

**0004 换掉了取证点**:0003 起的首页是窗口化的,数首页 `href="/p/<slug>/"` 数的是那个窗口——2026-10-19 报 48 页对 5,945 条目录,且从 2026-10-10 起每天误报(1ae7fd858)。改数 sitemap 后两侧都成了页面级量:预期值仍是 `data/plugins/` 的文件数(`--catalog-dir`),实际值来自 sitemap 里两语言的详情页 URL(去掉 `/zh/` 后按 slug 去重)。代价是它仍然只回答"页面在不在",不回答"内容是否冻结",也不看 `index.json`。

## 本专题最重要的一个架构事实

**build-site 的花名册来源是 README,不是 YAML;但 README 本身已降级为生成物。** 它逐行正则解析两份 README 得到条目集合(build-site.mjs:106 附近);YAML 只被读来补三样东西——条目文件路径(:47)、门店图 `icon`(:48-52)、tarball 映射(:53-63)——再加 0004 的市场索引(:187)。0001 起投稿改为 **yml-only**(#3832/#4004):人工编辑点只有 data/plugins/*.yml;README 由 sync-readme.yml 在 merge 后由 bot 于 main 上重生成并提交(sync-readme.yml:32-33,`contents: write`——全仓库唯一向 main 写入的 workflow,0002 复核仍成立)。pr-check 的 `generate-readme --check` 守卫仍在但语义收窄:**只拦截"PR 自己手改 README 且与 yml 不符"**(pr-check.yml:210);yml-only PR(现在的常态)不经过它。完整因果链变为:

```text
data/plugins/*.yml ──(PR, yml-only)──▶ merge ──sync-readme.yml bot commit──▶ README.md/README.zh.md ──parseReadme──▶ site/docs/*
   (唯一人工编辑点)                                    (bot 生成的中间投影)                    (生成物 ×2:页面+数据)
```

0004 给这条链加了**第二条取数路径**:市场索引不经 `parseReadme`,直接 `readEntries()` 读 `data/plugins/*.yml`(build-site.mjs:187)。于是索引是站上第一个"跳过 README 投影"的产物:yml-only PR 刚 merge、bot 还没再生 README 的窗口里,索引已经列出新条目,而每条记录的 `homepage` 指向 `${ORIGIN}/p/<slug>/`——那一页要等下一次构建才存在(推断,未实测;窗口通常被 `workflow_run` 触发的那次构建关掉)。

0002 补上这条链上刚被发现的**断点**:bot 用默认 GITHUB_TOKEN 提交不会触发 `push`,所以站点会永远慢一个 merge(2026-09-20 实测 main 4,014 条、已发布 4,012,且 bot 那个 sha 上根本没有 build-site 运行)。修法是 build-site 增加 `workflow_run` 触发(build-site.yml:30-32),而不是让 bot 去 dispatch。同一次修复把探针开关从"排除 push"改成**事件白名单**(build-site.yml:177-186):旧写法让每次 sync-readme 完成都跑全量探针,2026-09-22 有一次在这一步坐了 40 分钟(纯部署构建约 12 分钟)。

一份数据、两次投影仍在,但第二次投影的守卫从"PR 时强制同步"变为"main 上确定性再生 + PR 侧仅防手改(+ 0002 起按线上字节兜底)"。docs 侧守卫不变(bilingual parity 五检 + 截图 host 白名单);「跳过 YAML 直接造数据」仍会被拦,「手编 README」则从"被拦"变为"被 sync-readme 的重生成覆盖"。0004 之后实际是三次投影(页面 / catalog / 索引),其中索引不经过 README,也就不受 sync-readme 那次 bot 提交的时延约束。

## 正文

- [01 · build-site 主干与部署链](./01-build-site.md)
- [02 · 模板契约与 locales 体系](./02-templates-locales.md)

## 待回答的问题

- [x] 详情页一插件一 HTML 还是 SPA → 每插件每语言一个静态 index.html(docs/p/{slug}/、docs/zh/p/{slug}/),模板见 [02](./02-templates-locales.md)
- [x] locales 支持几种语言 → 仅 en/zh;首元素为 default(x-default,serve at `/`)
- [x] build-site 在 CI 哪一步、产物推到哪 → 见 [01](./01-build-site.md) §部署链
- [ ] 第三种语言的最小接入成本(0001 后至少动五处:locales.mjs 含 `giscusLang`、TOC_SHELL、privacy.<code>.html、banner/og 两图,评估待做)
- [ ] **0002 新增**:tolerance=300 是否够兜住目录日增(注释给的实测 2026-09-03..09-25 日均 62.5 条、峰值 205 条),以及它能否认出"页面在、内容冻结"这种半冻结——0004 改成数 sitemap 后,窗口化不再是误报来源,但检查仍然只数页面数
- [ ] **0003 新增**:site-health 只核线上页面数,是否需要对 locale/category `catalog.json` 做完整性检查——catalog 缺失时单页仍可成功发布,但浏览器只剩 24 张回退卡
- [ ] **0004 新增**:索引的覆盖面天然只有 npm 那一半;剩下的一半要等 format 1 支持 Git 版本的 commit SHA(本仓库目前不记录),评估时不要把它当成"索引落后"
- [ ] **0004 新增**:`docs/index.json` 现在搭 `dsh-plugin-catalog` 的车(自立包需要先在 npmjs 上人工建包,trusted publishing 无法从 CI 给不存在的包建关系),代价是每次 catalog 下载多 +684 KB gzip(注释自认"拆出去才是终态");拆出去的收益/成本未评估
- [ ] **0004 新增**:site-health 不检查 `index.json`;若某次构建因缓存里没有 `publishedAt` 而没写索引,线上不会有任何东西报错(页面照旧)
- [x] **0004 新增,线上已确认**:"索引源"那一行只在首页循环里被替换(build-site.mjs:716),分类页循环(:736-782)没有对应替换。2026-10-24 直接抓 https://awesome-dsh-plugin.com/tools/ ,搜索条下原样输出字面 `__INDEX_LINE__`(同次抓首页无此字面)——这是 0004 引入的用户可见缺陷,不是文档推断
