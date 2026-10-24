# 01 · build-site 主干与部署链

> 基线:`upstream@b4d0049a8`(0004 复核,2026-10-24)。行号 = scripts/build-site.mjs(**1291 行**,1174→1256→1291)除注明外。0001 核心变更:README 生成归属重构(sync-readme.yml)、AdSense/Giscus 注入、并发组拆分、added-date 双账本、plugins.json 新增 version。0002 核心变更:能力披露三字段进 plugins.json、下载窗口显式化、added-date 加"改写不算新增"守卫、slug/giscus term 大小写修复、site-health、`workflow_run` + 探针白名单。**0003(#6105):首页/分类页改为首 24 卡片 SSR,其余从带 hash URL 的 JSON catalog 虚拟窗口化加载,同时提供 no-JS 与 fetch-failure 回退。** **0004:新增市场索引产物(`docs/index.json`,用 host 端同一个 parser 校验)、卡片安装命令补上 tarball 一级(#7752)、`skip_probes` 手动部署路径、CI 用 npmjs 覆盖 lockfile 里的 npmmirror 源;条目数 4489 → 6704。**

## 阶段流水

1. **常量与资产**(:24-42):`ORIGIN='https://awesome-dsh-plugin.com'` 硬编码(:24);`site/assets/*` 平铺拷进 `docs/` 根(CNAME、robots.txt、badge.svg、logo.svg、双语 banner/og PNG、两个 woff2 字体子集、404.html);字体自托管的理由写在 template.html:28-32("a webfont request hands the visitor's IP to a third party on every page view")。0003 修改了 `site/template.html` 与 `site/locales.mjs`,加入 catalog preload / no-JS 提示与虚拟列表样式;0004 又在这两个文件里加了索引源一行与两条 `INDEX_*` 文案(见 02 · 模板契约);隐私页、ads.txt、Giscus 脚本、静态资产均无 diff。
2. **解析 README 花名册**(:106-167):en 要求分隔符 `-`、zh 要求 `—`(取自 loc.sep);五类 parity 失败全部置 `parityBroken` → exit 1,"refusing to build (a silent drop would delist and delete pages)":同 locale 内 URL 重复 / 分隔符不符 / 某语言缺 URL / 同 URL 两语言分类不同(#343)/ 只存在于另一语言。分类归属是**标题子串匹配**(`h[1].includes(loc.categories[id])`)。
3. **数据加载与派生**(:177-495):
   - `added-dates.json` 是人工拥有的**冻结基线**(2026-08-15 前固定);缺失日期改用**双账本推导**(README 账本 :240-293 + 条目 yml 账本 :294-314;`scripts/lib/added-dates.mjs:15` 抽出 `firstAddedDate`,走 `git log --diff-merges=first-parent --no-patch --diff-filter=A`,取最旧)。
     - **0002 新增守卫**:一个 commit 里同时 `-` 掉并 `+` 上同一 URL 视为**改写**,不再认领当天日期(逐 commit 维护 `addedHere`/`removedHere` 后 `flush()`)。动机是实测事故:2026-09-15 一次会话里两条目被改写到当天(siyuan-codex-bridge 09-11 → 09-15、thinking-token-stat 09-06 → 09-15)。
     - **0002 新增第二本账**:整仓一次 `--name-only` 的 yml 账本(:294-314),只用于被改写的 URL,"costs ~1.4s instead of minutes";**不回填历史**(约 120 条会被它提前一两天的旧目录刻意不重判)。
     - 抽出 `lib/added-dates.mjs` 的直接原因写在注释里:这条路径"had no test at all when it took the site down"(#4756,配 `scripts/added-dates.test.mjs`)。
   - **星数覆盖率地板** `STARS_MIN_COVERAGE = 0.66`(:229-234):未设 `SKIP_PUBLISH_CHECKS=1` 且覆盖率不足直接 throw(#1673 的 stars:{}×1362 教训;floor 判"磁盘已有",因为新条目合法地没有星数)。
   - **下载窗口显式化(0002 新增,`scripts/download-window.mjs`,16 行)**:月下载一律用显式 UTC 窗口(结束=昨天、起点=结束−29 天),并**拒收** `start/end` 与请求不符、或 downloads 不是非负安全整数的响应——相对时间端点会返回旧缓存窗口(#5309)。配套 `scripts/download-window.test.mjs` 进了 build-site.yml 的测试步骤(:95)。这是本仓库第一次把回归测试挂进构建。
   - 截图:host 白名单四个 GitHub 域(:374-379;key 必须 URL 精确匹配已列条目)、1–8 张、超限 exit 1。
   - 三方合并:`declared`(作者仓库的 screenshots.json)> legacy key;live verdict 仅剔除 ok:false(404/410),全死删整个字段而不是留空数组。
   - slug 规则(:480):`slugOf()` 移入 `scripts/lib/terms.mjs:22`(`repo--sub路径(/→-)`,无 sub 则 repo 本身),与 adopt-discussions 共用同一份实现。
   - **市场索引(0004 新增,`scripts/lib/market-index.mjs` 156 行 + `scripts/build-index.mjs` 55 行)**:`buildMarketIndex()` 用 `readEntries()`(yml,**不走 README**)、`data/npm-map.json` 与 `site/locales.mjs` 生成 format 1 文档,再用 host 端同一个 `parseMarketIndex` 校验。收录条件三条:有 npm 包名、有精确版本、该版本有整数 `publishedAt`(Unix 秒),缺一条就按 `noNpm/noVersion/noPublishTime` 计数跳过(:115-119);逐条先单独校验,一条坏只丢那一条并记 `refused`,末尾整份再校验一次(:142-154)。GitHub-only 条目在 format 1 里没有表达式(每个 Git 版本要 commit SHA,本仓库不记录),upstream 自述约占名单一半。描述按语言截到 160 字符(距词边界 24 字符内才回退到词边界,CJK 直接按字符切,末尾加 `…`),`keywords: []`/`engines: {}` 这类默认值一律省略;`engines.dsh` 仅在 `semver.validRange` 通过时写入(Discover 的兼容过滤)。`homepage` 指向 `${ORIGIN}/p/${slug}/`;`repository` 的 `tree/<branch>/<dir>` 子目录遇到百分号转义或空格就整段丢弃,而不是丢掉整个插件。构建在 :182-197 调一次并写盘:`indexBuilt = plugins.length > 0` 时才写 `docs/index.json`,并打印 listed / no-npm / no-version / 待回填发布时间的分项计数(:196)。注释两次点明动机:host 端取数预算是固定 15 s,所以压缩输出、不选 pretty-print。
4. **首页/分类与隐私页生成**:首页(:687-725)+ 分类页(:736-782,空分类跳过)+ 隐私页(:795-821,缺 privacyBody 文件 exit 1)。HTML 仅预渲染 download 排名前 24 张卡(`FALLBACK_CARDS` :525),`__CARD_COUNT__` 仍报全类目总数,`__FALLBACK_COUNT__` 显示当前 HTML 里确有的卡片数。两种结构产物并行生成:**HTML 首屏**与可客户端读取的 **JSON catalog**。`catalogPayload()`(:593-628)将 locale 文案、卡片元数据、描述、安装命令和详情 URL 串入 JSON;首页 catalog 包全量,分类 catalog 只包含该分类。`catalogHref()`(:625-626)基于 JSON SHA-256 前 8 位加 `?v=`,令 CDN URL 随内容变更。`<link rel=preload>` 预载 catalog。客户端在 `template.html` 过滤/排序并虚拟化可见卡片(约 3 行 overscan);`<noscript>` 提示只显示首屏。catalog 获取/渲染失败则保留首批烘焙卡片并在本地筛排——不是全量降级。详情页仍每插件每语言一页,孤儿详情页清理仍保留。

   **卡片安装命令(0004 修正)**:`cardCmd()`(:534-536)从 `npm ? npm : cmdGit` 改成 `npm ? npm : (cmdTarball ?? cmdGit)`——无 npm 但有作者声明 Release 包的条目不再退到 `github:` 源(#7752)。SSR 卡、分类卡与 catalog 的 `cmd` 字段共用这一个函数,首屏与虚拟列表因此不会分叉;`plugins.json.install`(:1165)本来就是这个优先级。配套 `scripts/card-install-command.test.mjs`(28 行)用 `runInNewContext` 直接抽 `build-site.mjs` 里的 `cardCmd` 函数体做纯函数测试,但**没有任何 workflow 跑它**(pr-check 逐个点名测试,:217-232 里没有它,也没有 `node --test` 通配)。

   **"索引源"那一行(0004)**:`INDEX_LINE`(:678-682)在 `.searchband` 末尾(template.html:323)输出一句话 + jsDelivr 地址 + 复制按钮;只有 `indexBuilt` 时替换成这段 HTML,否则整体替换为空串(:716),所以缓存缺 `publishedAt` 的构建不会指向一个 404。**但只有首页循环有这个 `replaceAll`**:分类页循环(:736-782)不替换 `__INDEX_LINE__`,于是每个分类页把字面 `__INDEX_LINE__` 印在搜索条下方——2026-10-24 直接在线上确认:抓 `https://awesome-dsh-plugin.com/tools/` 的 HTML,该 token 原样出现在 `.searchband` 内(同次抓首页无此字面)。
5. **README 渲染**(`renderReadme` :837):Marked + heading depth+1(cap 6)、相对链接基于 raw base 解析;`renderer.html` 返回空串——**详情页正文里裸 HTML 全部丢弃**;图片必须过 SCREENSHOT_HOSTS(允许 `data:`),丢图后清理空 `<a>`/`<p>`。多语言选择按 LOCALES 顺序回退,兼容旧的无 key 结构,命中非本页语言时提示 P_README_ONLY 并在包裹 div 标真实 lang。
6. **数据产物**:

| 产物 | 内容 | 关键点 |
|------|------|--------|
| `docs/plugins.json` | 完整注册表(name/owner/url/page/category/desc/npm/version/tarball/stars/downloads/install/added/screenshots + **0002 新增 downloadsStart/downloadsEnd/downloadsCheckedAt + capabilities/capabilityRedLines/capabilityCheckedAt** + **0004 新增 icon**)| tarball 键 absent 时省略而非 null;version 赋值 :475、registry 发射 :1119(`version: e.version` :1151,= npm dist-tags.latest,null=github-only 或无 latest,消费方 dsh-market#348);**能力三字段在未扫描时整个键省略**(:1157-1164)——注释明说"so a consumer cannot read 'absent' as 'empty'",市场侧渲染成"未检出 / not checked"(#401);下载三字段来自显式 UTC 窗口(:1154-1156);`icon` 同样缺省即省略(:1169,作者声明的门店图,站点页面不渲染,消费方回退作者头像);updates **故意不并入**(市场每次打开都拉这个文件,release body 会撑爆,:826-832)|
| `docs/index.json` | 名单作为 DSH 插件市场索引(format 1):`format/title/description/metadata.categories/plugins[]`,每条 `{name,title,description,homepage,repository,metadata.category,versions[1]}` | 只收 npm 且该版本有整数 `publishedAt` 的条目;`versions[0] = {version, publishTimestamp, source:{type:'npm'}}`;压缩输出(host 15 s 预算);两条发布路径:Pages 根 + `dsh-plugin-catalog` 包(jsDelivr),构建本身只写 `docs/` |
| `docs/count.json` | shields endpoint schema `{schemaVersion,message:N,color,cacheSeconds:300}` | README 徽章的消费端;cacheSeconds 取 shields 下限 300,因为徽章下面就是列表,数对不上会被当 bug |
| `docs/readmes.json` | 详情页正文源(locale→{md,base,blobBase})| MB 级 |
| `docs/updates.json` | 来自 `data/updates.json`(cache-only,见 [probes-and-decay/03](../probes-and-decay/03-publish-layer.md)),仅 listed | KB 级 |
| `docs/feed.xml` ×2 | 按 addedAt 倒序 newest 30 条 | |
| `docs/catalog.json` ×2 | 首页全量卡片 catalog(en/zh 各一份) | locale 文案与卡片数据随 JSON 下发;HTML 内 `?v=<sha256前8位>` 固定 CDN 版本 |
| `docs/<locale>/<category>/catalog.json` | 每个有条目的分类页一份分类专属 catalog | 不下载无关类别;部署必须与 HTML 一起发布,缺失时交互只剩首屏 24 张 fallback 卡 |
| `docs/sitemap.xml` | 四类 URL + 全套 hreflang alternates | 分类页 daily、详情页 weekly(lastmod=e.added)、隐私页 yearly,lastmod 取隐私源文件最后 commit 日期——"lastmod 每晚移动而内容没变会让爬虫不再相信全站的 lastmod";0004 起它同时是 site-health 的取证文件(见 00 · 地图) |

## 部署链(build-site.yml,298 行)

- **触发**:nightly cron `23 2 * * *` + workflow_dispatch(带 `probe_all` 与 **0004 新增 `skip_probes`** 两个布尔输入,:7-15)+ push 到 main(无 paths 过滤,刻意)+ **0002 新增 `workflow_run` on "Sync READMEs from data/plugins" completed**(:30-32)。理由写在注释里:bot 的 GITHUB_TOKEN 推送不触发 push 事件,"so the site stays exactly one merge behind";2026-09-20 实测 main 4,014 条 / 已发布 4,012,且 bot 的 sha 上没有任何 build-site 运行。选 workflow_run 而非 dispatch 是为了不加权限面。并发组仍在(:69-71):`build-site-push` / `build-site-probe`——push(含 workflow_run)只取代 push 构建,**永远不能取消 nightly**。
- **探针门(0002 白名单 + 0004 手动逃生口)**:旧逻辑 `event != 'push'` 导致每次 sync-readme 完成都跑全量探针,2026-09-22 有一次在这步坐了 40 分钟(纯部署构建约 12 分钟);0002 改为 `case schedule|workflow_dispatch → full_probe=1`(:177-186)。0004 把 dispatch 拆成两条语义:默认仍是全量重探,`skip_probes=true` 则只部署/发布(注释给的场景:2026-10-18 索引要赶在用户已经开始加的时候上线,:180-183)。冷缓存仍强制探针——`if [ -n "$full_probe" ] || [ ! -s data/npm-map.json ]`(:187):`skip_probes` 只省时间,不能在没数据时省探针。push/workflow_run 构建跳过 npm/downloads/stars/readmes/updates 五个探针,**始终跑 tarballs、screenshots 与 capabilities**(:214-232)——"Probing is slow; that is cheaper than a wrong plugins.json"。
- **不变量**:`permissions: contents: read`(:48-51);注释 "The build never writes to the repository." 仍在——**该不变量只对 build-site 链成立**;仓库里唯一向 main 写入的是 sync-readme.yml(bot 提交 README,:32-33)。
- **依赖安装(0004 新增覆盖)**(:88-94):lockfile 里有 7 条 `resolved` 指向 `registry.npmmirror.com` 的 tarball URL(新增的索引依赖树 + `semver` + `js-yaml@4`),该 CDN 在 GitHub runner 上反复 503/504 并把 `npm ci` 挂上几十分钟(2026-10-19);CI 因此设 `npm_config_registry=https://registry.npmjs.org/` 与 `npm_config_replace_registry_host=always` 两个变量。两者缺一不可:只改 registry 不会重写 lockfile 里显式记录的镜像 URL。
- **三层缓存**(probe-data-v2 共享条目 / downloads-v1 / updates-v1 刻意分离,#1673 后防版本连锁失效;#2797:downloads 不单独缓存时线上下载量比 npm 真实值低约 42%)。**0002 更正**:`data/updates.json` 是 **cache-only**,"NOT committed — unlike stars/downloads, there is no committed floor"(0001 曾误记为已提交边车)。
- **npm 发布(catalog/updates 双包)在 deploy 之后**(:281-298),且仅 nightly/manual。凭据 OIDC trusted publishing(`id-token: write`,npm ≥11.5);**deploy 失败对探针运行 continue-on-error**(:256),deploy 之败没资格拖住两个 publish 与 cache-save。0004 起 catalog 包里多了 `index.json`(`publish-catalog.mjs:55`、:130、:157-158),`catalogSha` 取 `plugins.json`+`index.json` 拼接的 sha256(:133),所以只动索引的一天也会发一个版本;索引没有自立包是因为 trusted publishing 按包配置、不存在的包无法从 CI 建立关系(首次尝试 404),理由与代价写在 `publish-catalog.mjs:40-55`:每次 catalog 下载 +684 KB gzip(约 2.3 MB JSON),"拆出去才是终态"。
- **新增测试步骤**(:95):`node --test scripts/download-window.test.mjs`。0004 的 `scripts/card-install-command.test.mjs` 未接入本 workflow,也未接入 pr-check。
- **`build-index.mjs` 是第二个入口**:用法注释自称 `--check` 是 "CI gate",但仓库里没有任何 workflow 调它;实际写索引的是 build-site.mjs:192。两处都调同一个 `buildMarketIndex`,逻辑不会分叉,守卫却没有落地。

## 已知文档漂移

- 详情页量随当前名单更新:0003 基线 4489 条目、0004 基线 6704 条目(`git ls-tree HEAD data/plugins/` 的 yml 数),按 ×2 推算约 1.34 万个静态详情页;首页与分类页现各多一个 JSON catalog 资源,另加一个全站 `index.json`。精确构建输出总数仍无 CI build log 留档。

- build-site.mjs:9 注释声称 "re-syncs the plugin-count figure inside every README"——build 全文写盘调用无一触及 README,计数徽章走 shields endpoint。**过期注释,行为是「build 从不碰源文件」**;0001 后这句话有了例外形态:写 README 的是 sync-readme.yml,不是 build。
- AdSense 头注入(`adHead()`,build-site.mjs:79,token 定义 :87,变量未设时返回空串,`__AD_HEAD__\n` 连换行一起替换——**未设变量时产物与无广告构建逐字节相同**;注入点 :719/:776/:1056,privacy-template 没有)与 Giscus 评论懒加载(`mapping:'specific'` 按 `plugin:<slug>` 映射 Discussion、IntersectionObserver 400px 触发才注入 script——**不滚动=不联系第三方**;enabled 时四 ID 强校验)。
- **0002 修复的静默漂移**:giscus 的 term 从"构建时小写化"改为 `termOf(e.slug)` 原样(:970)。自评论区上线到 2026-09-24,这条小写化让**所有 owner/repo 含大写的条目被劈成两个 Discussion**——市场问 `plugin:FeatherHunter/dsh-prompt`,catalog 答 `plugin:featherhunter/dsh-prompt`,"Two threads, neither wrong"。同一份 `slugOf/termOf` 现由 build-site 与 adopt-discussions 共用(`lib/terms.mjs`)。
- **0004 落地的两个未接线件**:`build-index.mjs` 的 `--check` 与 `card-install-command.test.mjs` 都没进 CI。前者意味着"已发布索引是否仍是合法 format 1"没有任何门禁;后者意味着 #7752 的回归保护只在本机跑 `node --test` 时才存在。

## 待复核

- [ ] checkout + Pages 上传的实际耗时分布(workflow 无计时输出;UNVERIFIED)
- [x] ~~会不会自动提交 README~~ → build-site 链不会;**0001 起 sync-readme.yml 会**(仓库唯一写 main 的 workflow),见上
- [ ] 0002:capabilities 三字段写进了 plugins.json,但**站内页面不渲染**(模板无对应 token)——确认消费方只有 dsh-market
- [ ] 0003:site-health 只比线上页面数与 `data/plugins/` 条目数;未见它校验生成 catalog 是否完整,应评估坏/缺 catalog 的部署能否被发现(0004 改成数 sitemap 后仍不覆盖)
- [ ] catalog JSON 的总输出字节及 Pages 实际部署/边缘缓存命中情况(当前只按构建逻辑确认,未从 production 下载测量)
- [ ] 0002:约 1.34 万个详情页是 6704×2 的推算值,没有构建日志佐证(UNVERIFIED)
- [ ] 0004:`docs/index.json` 的实际条目数与字节数无法本地复算——工作树里 `docs/` 与 `data/npm-map.json` 都被 .gitignore,只能引用提交信息里的实测(描述截断后 3.1 MB → 2.34 MB)**(UNVERIFIED)**
- [ ] 0004:`skip_probes` 碰到"有 npm/version 但无 `publishedAt`"的旧缓存会让 `indexBuilt=false`、不写 `docs/index.json`,而发布步骤无条件读它(`publish-catalog.mjs:130`)——推断,未实测
- [ ] 0004:索引每条 `homepage` 指向的 `/p/<slug>/` 可能还没生成(README 投影滞后窗口,见 00 · 地图),需一次真实构建或线上抓页面确认(分类页字面 `__INDEX_LINE__` 已由线上确认,见上)
