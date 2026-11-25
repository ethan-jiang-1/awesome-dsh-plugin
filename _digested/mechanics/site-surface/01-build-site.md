# 01 · build-site 主干与部署链

`0005 零 diff;0006 有实质改动;0007 有实质改动`;基线:`upstream@8f1a1800e`(2026-11-25)。行号 = scripts/build-site.mjs(**1317 行**,1174→1256→1291→1296→1317)除注明外。0007 相对 0006 是 +21 净行,新代码集中在三处——`:24` 的 import、`:449-452` 的 tarball 助手、`:1231-1259` 的分片发布——它们之后的段落整体下移 5–9 行;下文标出的都是本轮在 checkout 上核过的当前行号,0006 时期的旧数字只在需要说明"这里曾经是什么样"时保留。最近核验:`8f1a1800e`。

0001 核心变更:README 生成归属重构(sync-readme.yml)、AdSense/Giscus 注入、并发组拆分、added-date 双账本、plugins.json 新增 version。0002 核心变更:能力披露三字段进 plugins.json、下载窗口显式化、added-date 加"改写不算新增"守卫、slug/giscus term 大小写修复、site-health、`workflow_run` + 探针白名单。**0003(#6105):首页/分类页改为首 24 卡片 SSR,其余从带 hash URL 的 JSON catalog 虚拟窗口化加载,同时提供 no-JS 与 fetch-failure 回退。** **0004:新增市场索引产物(`docs/index.json`,用 host 端同一个 parser 校验)、卡片安装命令补上 tarball 一级(#7752)、`skip_probes` 手动部署路径、CI 用 npmjs 覆盖 lockfile 里的 npmmirror 源。** **0006(+31/−9):全站 href 改走 `slugOf` 之后的 `slugHref()`(见 [00 · 地图](./00-map.md));读 cache-only 边车 `data/releases.json`,GitHub-only 条目的 `version` 用 release-manifest 兜底;registry 新增 `starsCheckedAt` 与 release 元数据四字段;配套改动在 `lib/market-index.mjs`(npm 名占用仲裁)与 `lib/terms.mjs`。** **0007(+24/−3):① Release 历史从"聚合文件里的一个键"变成"每仓一个静态分片"(`docs/release-history/v1/<owner>/<repo>.json`),`docs/updates.json` 只留 `releaseHistory: true` 指针;② tarball 安装命令补 `-w`(`releaseTarballCmd()`),卡片/详情页/registry 三处同源;③ `build-site.yml` 加 job 级 fork 门,本 fork 合并后不再自动构建/部署。** 另:`site/locales.mjs` 英文 `TITLE`/`DESC` 两行改词,`site/` 其余零 diff;模板与 token 契约不变(见 [02](./02-templates-locales.md))。

## 阶段流水

1. **常量与资产**(`:24-89`):`ORIGIN='https://awesome-dsh-plugin.com'` 硬编码(:26);`site/assets/*` 平铺拷进 `docs/` 根(:32-33;CNAME、robots.txt、badge.svg、logo.svg、双语 banner/og PNG、两个 woff2 字体子集、404.html);字体自托管的理由写在 template.html:28-32("a webfont request hands the visitor's IP to a third party on every page view")。广告块 :80-89:`ADSENSE_CLIENT` 取 `process.env`、`adHead()` 返回空串或一段 head 标签、token 是 `'__AD_HEAD__\n'`(连换行一起替换,所以未设变量的构建与无广告构建逐字节相同)。0007 在这里只多了一行 import(`:24`,`catalogRepo / HISTORY_CACHE_KEY / publishReleaseHistory`)。
2. **解析 README 花名册**(`:108-170`):en 要求分隔符 `-`、zh 要求 `—`(取自 loc.sep);五类 parity 失败全部置 `parityBroken` → exit 1,"refusing to build (a silent drop would delist and delete pages)":同 locale 内 URL 重复 / 分隔符不符 / 某语言缺 URL / 同 URL 两语言分类不同(#343)/ 只存在于另一语言。分类归属是**标题子串匹配**(`h[1].includes(loc.categories[id])`)。`ordered` 在 :172 按 `CAT_IDS`(23 类)重排,`N = ordered.length`(:173)。
3. **数据加载与派生**(`:181-490`):
   - `added-dates.json` 是人工拥有的**冻结基线**(2026-08-15 前固定),读入在 :181;缺失日期改用**两本账 + 一条兜底**(README 账本 :243-294 → 整仓 yml 账本 :295-317 → 逐条 `firstAddedDate` :318-358;`scripts/lib/added-dates.mjs:15` 抽出 `firstAddedDate`,走 `git log --diff-merges=first-parent --no-patch --diff-filter=A`,取最旧)。三者都拿不到就 exit 1,拒绝盖章"今天"(:359-365)。
     - **0002 新增守卫**:一个 commit 里同时 `-` 掉并 `+` 上同一 URL 视为**改写**,不再认领当天日期(逐 commit 维护 `addedHere`/`removedHere` 后 `flush()`)。动机是实测事故:2026-09-15 一次会话里两条目被改写到当天(siyuan-codex-bridge 09-11 → 09-15、thinking-token-stat 09-06 → 09-15)。
     - **0002 新增第二本账**:整仓一次 `--name-only` 的 yml 账本(:295-317),只用于被改写的 URL,"costs ~1.4s instead of minutes";**不回填历史**(约 120 条会被它提前一两天的旧目录刻意不重判)。
     - 抽出 `lib/added-dates.mjs` 的直接原因写在注释里:这条路径"had no test at all when it took the site down"(#4756,配 `scripts/added-dates.test.mjs`);逐条兜底那段就是它(:318-358)。
   - **星数覆盖率地板** `STARS_MIN_COVERAGE = 0.66`(:232-242,`starsMap` 读入在 :200):未设 `SKIP_PUBLISH_CHECKS=1` 且覆盖率不足直接 throw(#1673 的 stars:{}×1362 教训;floor 判"磁盘已有",因为新条目合法地没有星数)。
   - **Release 元数据边车(`:201`)**:`const releasesMap = fs.existsSync('data/releases.json') …`——与 stars 同样的"缺文件即空 map"姿势,但**没有对应的发布地板**:注释明说 missing(尚未 bootstrap,或条目无 npm 包)对多数条目是"正常的永久状态",不像 stars.json 那样需要阻塞发布的 floor。`data/releases.json` 是 cache-only 边车(.gitignore:17,probe-releases 写,机制见 [probes-and-decay/01](../probes-and-decay/01-probe-family.md))。每条目 `e.releaseMetadata = releaseMetadataFor(e, releasesMap[e.url])`(:469),registry 发射时 `...e.releaseMetadata` 展开(:1163)——条件不满足时一个键都不产生,与 capabilities 的"缺席≠空"同一纪律。
   - **下载窗口显式化(0002 新增,`scripts/download-window.mjs`,16 行)**:月下载一律用显式 UTC 窗口(结束=昨天、起点=结束−29 天),并**拒收** `start/end` 与请求不符、或 downloads 不是非负安全整数的响应——相对时间端点会返回旧缓存窗口(#5309)。配套 `scripts/download-window.test.mjs` 进了 build-site.yml 的测试步骤(:99)。这是本仓库第一次把回归测试挂进构建。
   - 截图(:377 起,`SCREENSHOT_HOSTS`):host 白名单四个 GitHub 域;key 必须 URL 精确匹配已列条目、1–8 张、超限 exit 1。三方合并:`declared`(作者仓库的 screenshots.json)> legacy key;live verdict 仅剔除 ok:false(404/410),全死删整个字段而不是留空数组。
   - **slug 规则(:489)**:`slugOf()` 在 `scripts/lib/terms.mjs:22`(`repo--sub路径(/→-)`,无 sub 则 repo 本身),与 adopt-discussions 共用同一份实现。**0006 新增 `slugHref()`(terms.mjs:37-39)**:slug 含 `%` 时把 `%` 二次编码为 `%25`(monorepo 子目录带空格 → `%20` 在这里是数据不是转义,否则浏览器再解码一次会请求不存在的路径);CJK slug 与无 `%` 的 slug 逐字节原样。所有**详情页/卡片/目录 hreflang href** 改走它(:569/:573/:626/:906-910/:971/:1063/:1146/:1299/:1302),discussion term 走的 `termOf`(terms.mjs:42-44,调用点 :979)不变。
   - **市场索引(0004 新增,`scripts/lib/market-index.mjs` 171 行 + `scripts/build-index.mjs` 55 行)**:`buildMarketIndex()` 用 `readEntries()`(yml,**不走 README**)、`data/npm-map.json` 与 `site/locales.mjs` 生成 format 1 文档,再用 host 端同一个 `parseMarketIndex` 校验。构建在 :189-190 调一次,`indexBuilt = plugins.length > 0` 时才写 `docs/index.json`(:194)。收录条件三条:有 npm 包名、有精确版本、该版本有整数 `publishedAt`(Unix 秒),缺一条按 `noNpm/noVersion/noPublishTime` 计数跳过;逐条先单独校验,一条坏只丢那一条并记 `refused`。GitHub-only 条目在 format 1 里没有表达式(每个 Git 版本要 commit SHA,本仓库不记录),upstream 自述约占名单一半。`homepage` 指向 `${ORIGIN}/p/${slugHref(slugOf(entry.url))}/`(`lib/market-index.mjs:133`)。注释两次点明动机:host 端取数预算是固定 15 s,所以压缩输出、不选 pretty-print。0007 **未动**这个模块(零 diff)。
     - **0006 新增 npm 名占用仲裁(`lib/market-index.mjs:147-155`)**:monorepo 根与其子包可以解析到同一个 npm 包(真实案例:名单同时收 `Tests4gptplay/dsh-dots` 与 `Tests4gptplay/dsh-dots#dsh-dot-mcp`,两边 package.json 都写 `name: dsh-dot-mcp`,2026-11-15 nightly 被它绊倒),而格式 1 **按插件名键控**——parser 拒绝的是整份文档,不是第二行。修法是在逐条校验前维护 `claimed` Map:名字已被占即 `skipped.refused += 1` 并 `continue`;先到先得,列表顺序在前的条目保住名字。**丢行不丢索引**。被自家原因(如非精确版本)拒掉的行**不占用**名字,所以第二条同名的合法行仍可上榜。配套 `scripts/market-index-collisions.test.mjs`(68 行)。
   - **Release 历史缓存(0007 新增输入,`:1231`)**:`const history = updates[HISTORY_CACHE_KEY] ?? {}`——历史不在独立文件里,而在 `data/updates.json` 的内部键 `$releaseHistoryV1` 下。`updates` 本身在 :842 读入。详见下方 §0007。
4. **首页/分类与隐私页生成**:首页(:696-733)+ 分类页(:745-802,空分类跳过)+ 隐私页(:805-827,缺 privacyBody 文件 exit 1)。HTML 仅预渲染 download 排名前 24 张卡(`FALLBACK_CARDS` :534),`__CARD_COUNT__` 仍报全类目总数(:726/:783),`__FALLBACK_COUNT__` 显示当前 HTML 里确有的卡片数(:727/:784)。两种结构产物并行生成:**HTML 首屏**与可客户端读取的 **JSON catalog**。`catalogPayload()`(:602-632)将 locale 文案、卡片元数据、描述、安装命令与详情 URL 串入 JSON(:625/:626);首页 catalog 包全量,分类 catalog 只包含该分类。`catalogHref()`(:634-637)基于 JSON SHA-256 前 8 位加 `?v=`,令 CDN URL 随内容变更。`<link rel=preload>` 预载 catalog。客户端在 `template.html` 过滤/排序并虚拟化可见卡片(约 3 行 overscan);`<noscript>` 提示只显示首屏。catalog 获取/渲染失败则保留首批烘焙卡片并在本地筛排——不是全量降级。详情页仍每插件每语言一页(:834-1080),孤儿详情页清理仍保留(:1082-1102)。

   **卡片安装命令(0004 修正,0007 补 `-w`)**:`cardCmd()`(:543-545)从 `npm ? npm : cmdGit` 改成 `npm ? npm : (cmdTarball ?? cmdGit)`——无 npm 但有作者声明 Release 包的条目不再退到 `github:` 源(#7752)。0007 起 `cmdTarball` 由 `releaseTarballCmd()`(:449-452)产出,多一个 `-w`;SSR 卡、分类卡与 catalog 的 `cmd` 字段共用 `cardCmd`,首屏与虚拟列表不会分叉;`plugins.json.install`(:1176)本轮也从内联三元改成直接调 `cardCmd(e)`,与卡片逐字同源。配套 `scripts/card-install-command.test.mjs`(0007 后按函数名抽 `cardCmd` 与 `releaseTarballCmd` 并复算 `-w` 形态),但**仍然没有任何 workflow 跑它**(pr-check 逐个点名测试,:217-234 里没有它,也没有 `node --test` 通配)。

   **"索引源"那一行(0004)**:`INDEX_LINE`(:687-692)在 `.searchband` 末尾输出一句话 + jsDelivr 地址 + 复制按钮;只有 `indexBuilt` 时替换成这段 HTML,否则整体替换为空串(:725),所以缓存缺 `publishedAt` 的构建不会指向一个 404。**但只有首页循环有这个 `replaceAll`**:分类页循环(:745-802)的链式替换里没有 `__INDEX_LINE__`,于是每个分类页把字面 token 印在搜索条下方——2026-10-24 直接在线上确认(抓 `https://awesome-dsh-plugin.com/tools/` 的 HTML,该 token 原样出现在 `.searchband` 内;同次抓首页无此字面)。**0007 复核仍未修。**
5. **README 渲染**(`renderReadme` :846):Marked + heading depth+1(cap 6)、相对链接基于 raw base 解析;`renderer.html` 返回空串——**详情页正文里裸 HTML 全部丢弃**;图片必须过 SCREENSHOT_HOSTS(允许 `data:`),丢图后清理空 `<a>`/`<p>`。多语言选择按 LOCALES 顺序回退,兼容旧的无 key 结构,命中非本页语言时提示 P_README_ONLY 并在包裹 div 标真实 lang。
6. **数据产物**:

| 产物 | 内容 | 关键点 |
|------|------|--------|
| `docs/plugins.json` | 完整注册表(name/owner/url/page/category/desc/npm/version/tarball/stars/downloads/install/added/screenshots + downloadsStart/downloadsEnd/downloadsCheckedAt + capabilities/capabilityRedLines/capabilityCheckedAt + icon + starsCheckedAt、githubReleaseDownloads/githubReleaseDownloadsCheckedAt、releaseManifest)| tarball 键 absent 时省略而非 null(`:1157`);version 赋值 :484(`e.npm ? (npmMap[e.url]?.version ?? null) : (e.releaseMetadata.releaseManifest?.version ?? null)`);registry 对象 :1128-1188,写盘 :1188;`page` :1146、`version` :1160、`starsCheckedAt` :1162、`...e.releaseMetadata` :1163、能力三字段 `:1171-1175`、`install: cardCmd(e)` :1176、`icon` :1180、`screenshots` :1184。**能力三字段在未扫描时整个键省略**——注释明说"so a consumer cannot read 'absent' as 'empty'"(#401);`icon` 同样缺省即省略。updates **故意不并入**(市场每次打开都拉这个文件,release body 会撑爆);release 四字段来自 `releaseMetadataFor` 的条件展开——`releaseManifest.tarball` 与当前安装地址不一致时整键缺席。 |
| `docs/index.json` | 名单作为 DSH 插件市场索引(format 1):`format/title/description/metadata.categories/plugins[]`,每条 `{name,title,description,homepage,repository,metadata.category,versions[1]}` | 只收 npm 且该版本有整数 `publishedAt` 的条目;`versions[0] = {version, publishTimestamp, source:{type:'npm'}}`;压缩输出(host 15 s 预算);两条发布路径:Pages 根 + `dsh-plugin-catalog` 包(jsDelivr),构建本身只写 `docs/`(:194) |
| `docs/count.json` | shields endpoint schema `{schemaVersion,message:N,color,cacheSeconds:300}` | README 徽章的消费端;cacheSeconds 取 shields 下限 300,因为徽章下面就是列表,数对不上会被当 bug(:1313) |
| `docs/readmes.json` | 详情页正文源(locale→{md,base,blobBase})| MB 级(:1199-1221) |
| `docs/updates.json` | 来自 `data/updates.json`(cache-only,见 [probes-and-decay/03](../probes-and-decay/03-publish-layer.md)),仅 listed;**0007 起只带指针**:已发布分片的条目加 `releaseHistory: true`,只有历史没有 update 行的仓补 `{releaseHistory: true}` 一条;`$releaseHistoryV1` 缓存键永不出现 | KB 级;压缩 JSON(一处 `JSON.stringify`,:1257,0006 起就是这个形态);条目集合 = 有 update 行的仓 ∪ 有分片的仓 |
| `docs/release-history/v1/<owner>/<repo>.json` | **0007 新增**:每仓的 Release 历史分片,`{repo, complete, releases[]}`,`releases` 每条含 tag/name/publishedAt/url/body/commit | 单文件 ≤1 MB、每仓 ≤256 条、总预算 `900 MB − docs 现有字节`;只对 `catalogRepo()` 能规范化的 github.com URL 发布;`complete` 三条件见 §0007;只写不删(:1237 调用,实现 `lib/release-history.mjs:111-144`)|
| `docs/feed.xml` ×2 | 按 addedAt 倒序 newest 30 条 | :1105-1124 |
| `docs/catalog.json` ×2 | 首页全量卡片 catalog(en/zh 各一份) | locale 文案与卡片数据随 JSON 下发;HTML 内 `?v=<sha256前8位>` 固定 CDN 版本 |
| `docs/<locale>/<category>/catalog.json` | 每个有条目的分类页一份分类专属 catalog | 不下载无关类别;部署必须与 HTML 一起发布,缺失时交互只剩首屏 24 张 fallback 卡 |
| `docs/sitemap.xml` | 四类 URL + 全套 hreflang alternates | 分类页 daily、详情页 weekly(lastmod=e.added)、隐私页 yearly(:1278 起;`<loc>` :1299、alternates :1302),隐私页 lastmod 取隐私源文件最后 commit 日期——"lastmod 每晚移动而内容没变会让爬虫不再相信全站的 lastmod";0004 起它同时是 site-health 的取证文件(见 [00 · 地图](./00-map.md)) |

## 0007:Release 历史分片、tarball `-w`、fork 门

三件事彼此无关,共同点是都不动页面模板——所以 [02](./02-templates-locales.md) 的 token 契约照旧。

### 一、分片发布(`:1229-1260` + `lib/release-history.mjs`)

这一段在 `docs/plugins.json`(:1188)与 `docs/readmes.json`(:1199-1221)之后、`docs/sitemap.xml`(:1278)之前跑,四步:

1. `const history = updates[HISTORY_CACHE_KEY] ?? {}`(:1231)。键名常量在 `lib/release-history.mjs:7`(`'$releaseHistoryV1'`)。
2. 量站点现有字节(:1234-1236):`Object.keys(history).length === 0` 时直接记 0,否则 `fs.readdirSync('docs', { recursive: true, withFileTypes: true })` 递归 `statSync(...).size` 求和。注释动机:Pages 全站 1 GB,要给 updates manifest、sitemap 与 artifact 元数据留空间(:1232-1233)。因为测量点在 sitemap/count/updates 三个写盘之前,**它们不计入**;`docs/` 在构建开始时也不 wipe(只清理孤儿详情页),所以本地增量构建会把上一轮的旧分片算进去(推断,未实测)。
3. `publishReleaseHistory(ordered, history, 'docs', 900_000_000 - currentBytes)`(:1237),返回 `{ repositories, publishedBytes, skipped }`。
4. 一行日志:`release history: <N> repository fragments, <bytes> bytes, <skipped> over the Pages budget`(:1259)。

`publishReleaseHistory`(`lib/release-history.mjs:111-144`)逐条语义:

- 遍历 `new Set(entries.map(entry => catalogRepo(entry.url)))`(:115)——**只发布 listed 条目**,且 URL 必须过 `catalogRepo`(:14-18:owner/repo 全小写、`^[a-z0-9-]+/[a-z0-9_.-]+$`、不以 `/.` 或 `/..` 结尾),否则 `null` 跳过。
- `const source = history?.fallback ?? history?.releases`(:118):`fallback` 是重扫期间保留的上一版已发布内容,优先于 `releases`,避免扫描中途把线上分片清空。source 非数组或空 → 跳过(:119)。
- 逐条攒字节(:120-127):起点 `128 + byteLength(repo)`(给 `{repo, complete, releases}` 外壳留量),每条累加 `byteLength(JSON.stringify(release)) + 1`;超 `MAX_FILE_BYTES = 1_048_576` 或已 256 条(`MAX_RELEASES`,:9)就停。一条都放不下 → 整仓跳过(:128)。
- `complete = history.fallback === undefined && history.next === null && releases.length === source.length`(:129):"没有保留的上版、没有下一页、没被截断"三条同时成立才为 true。
- 总预算判定(:132-135):`publishedBytes + length > budget` 则 `skipped++` 并 continue;否则写 `docs/release-history/v1/<owner>/<name>.json`(:136-139),内容 `JSON.stringify({ repo, complete, releases }) + '\n'`。
- **没有删除分支**:分片树只增不减。CI 每次是干净 checkout + 整目录上传(:254),所以线上不会积累;只有本地增量构建会。

历史从哪来(`probe-release-history.mjs`,90 行;由 `probe-updates.mjs` 尾调,同一轮才写 `$releaseHistoryV1`):`BATCH = 30` 仓/查询、`QUERY_BUDGET = 240`、近期页预算 `RECENT_QUERY_BUDGET = 210`(:7-9),只对"update 行里有 release tag"的仓发起查询——没有 release 的仓连空分片都不会有。`refreshHistory`/`extendHistory`/`7 天 REVALIDATE_MS` 的游标语义归 [probes-and-decay/01](../probes-and-decay/01-probe-family.md),这里只记一个后果:**历史缓存只在跑全量探针的构建里前进**,而 `probe-updates.mjs` 位于 `if [ -n "$full_probe" ] || [ ! -s data/npm-map.json ]` 块内(build-site.yml:199-223),所以 push 构建永远不会刷新它。

### 二、`docs/updates.json` 的条目集合(`:1245-1257`)

- 第一轮:遍历 `Object.entries(updates)`,`!listed.has(url)` 直接跳过(:1246)——`$releaseHistoryV1` 不是 listed 里的 URL,所以缓存键**天然不可能**漏进公开文件;有分片的条目写 `{ ...entry, releaseHistory: true }`(:1247-1249),没有分片的写原 `entry`;`payload.count++`(:1250)。
- 第二轮:`for (const url of [...listed].sort())`(:1252),条件是"还没写进 payload"且"有对应分片",补一条 `{ releaseHistory: true }`(:1253-1255)。于是只有历史、没有 update 行的仓也会在聚合文件里占一个键。
- 写盘:`JSON.stringify(payload) + '\n'`(:1257)。**这一行 0007 未改**——`docs/updates.json` 从 0006 起就是压缩 JSON;本轮去掉了 pretty-print 的是探针写 `data/updates.json`(`probe-updates.mjs:340-342`:先写 `data/updates.json.tmp` 再 `renameSync`,内容是 `JSON.stringify(sorted)`,0006 时是 `JSON.stringify(sorted, null, 1)`)。
- 发布路径的连带事实:`publish-updates.mjs`(零 diff)只把 `docs/updates.json` 装进 npm 包 `dsh-plugin-updates`(`:29` `BUILT = 'docs/updates.json'`,`:108` 只写这一个文件),**分片树不上 npm**——所以 npm 侧的消费方只拿得到 `releaseHistory: true` 指针,历史本体要回 Pages 取。是否有人依赖这一点,待验证。

### 三、tarball 命令的 `-w`

```js
function releaseTarballCmd(tarball) {
  // The DSH profile is itself a pnpm workspace root.
  return tarball ? `dsh plugin --profile web add -w "${tarball}"` : null
}
```

(`:449-452`;0006 基线里这条还是 `:461` 的内联三元 `e.tarball ? … : null`,字符串里没有 `-w`)。理由只有注释那一句:DSH profile 是 pnpm workspace 根,不加 `-w` 会被当成往 workspace 子包装。消费点三处:`e.cmdTarball = releaseTarballCmd(e.tarball)`(:467)、详情页 `cmds` 第二档(:951)、registry `install: cardCmd(e)`(:1176,函数本身逐字等价于旧内联三元,属消重;但 `cmdTarball` 变了,`plugins.json.install` 里 tarball 条目随之带上 `-w`)。

### 四、fork 门(`build-site.yml:78`)

```yaml
jobs:
  build:
    # A fork mirrors the catalog but does not publish the site, so the job is
    # skipped there to spare the fork owner's Actions minutes on a deploy
    # nothing consumes. A manual dispatch still runs, for debugging.
    if: github.repository_owner == 'awesome-dsh-plugin' || github.event_name == 'workflow_dispatch'
```

**本文件只有一个 job**(`build`),所以这条 `if` 一跳过,deploy、cache save、双 publish 全部不跑——它们都是这个 job 的 step(:248-250 / :254 / :258-276 / :301-307 / :314-318)。本仓库 `github.repository_owner == 'ethan-jiang-1'`,因此合并后:**push、nightly cron、`workflow_run` 三条路径都不再构建/部署,唯一入口是手动 workflow_dispatch。** 部署链其余部分(下面一节)描述的是上游组织下的行为,在本 fork 上处于"仅在手动 dispatch 时成立"的状态。同轮另外 7 条 workflow 也加了同一条门,归属别处;`pr-check.yml` / `pr-gate.yml` 不加,PR 事件在 fork 上照跑。

## 部署链(build-site.yml,0007 起 318 行)

- **触发**:nightly cron `23 2 * * *`(:5)+ workflow_dispatch(带 `probe_all` 与 `skip_probes` 两个布尔输入,:6-16)+ push 到 main(无 paths 过滤,刻意)+ **0002 新增 `workflow_run` on "Sync READMEs from data/plugins" completed**(:30-31)。理由写在注释里:bot 的 GITHUB_TOKEN 推送不触发 push 事件,"so the site stays exactly one merge behind";2026-09-20 实测 main 4,014 条 / 已发布 4,012,且 bot 的 sha 上没有任何 build-site 运行。选 workflow_run 而非 dispatch 是为了不加权限面。**0007 的 job 级 `if`(:78)把这四条触发在 fork 上统一挡掉**,其中 `workflow_dispatch` 是白名单例外。并发组仍在(:69-70):`build-site-push` / `build-site-probe`——push(含 workflow_run)只取代 push 构建,**永远不能取消 nightly**。
- **downloads 缓存回写修复(0006,#14322,+16/−2)**:restore 步从 `actions/cache@v4` 改 **`actions/cache/restore@v4`**(:143-150),save 拆成独立一步 "Save downloads cache"(`actions/cache/save@v4`,:248-250),条件 `steps.build.outputs.probed == '1'`——Build 步 `id: build`(:158),只在真正跑了探针的分支末尾 `echo "probed=1" >> "$GITHUB_OUTPUT"`(:223)。要修的病:cache action 的 post-step 在**每次** run 结束都会 save,push 构建(跳过探针)把 restore 到的旧 downloads.json 用新 key(`downloads-v1-<本次 run_id>`)存回去;restore-keys 前缀恢复按创建时间排序,这份"旧数据、新 key"的副本排在 nightly 刚存的新副本前面,把 nightly 的成果遮住——站点落后一天,直到下一个 nightly 才翻过来。注释里保留了 #2797 的旧教训(#2797:downloads 不单独缓存时线上下载量比 npm 真实值低约 42%)。updates-v1 与 probe-data-v2 的缓存仍是老式 `actions/cache@v4`(save 仍无条件,但它们的写入只随探针 run 变化,病征不同)。**0007 注意:`data/updates.json` 现在同时装着 release 历史缓存**,所以 updates-v1 这个缓存条目里多了一棵树;缓存策略本身没改。
- **探针门(0002 白名单 + 0004 手动逃生口)**:旧逻辑 `event != 'push'` 导致每次 sync-readme 完成都跑全量探针,2026-09-22 有一次在这步坐了 40 分钟(纯部署构建约 12 分钟);0002 改为 `case schedule|workflow_dispatch → full_probe=1`(:189-198)。0004 把 dispatch 拆成两条语义:默认仍是全量重探,`skip_probes=true` 则只部署/发布(注释给的场景:2026-10-18 索引要赶在用户已经开始加的时候上线)。冷缓存仍强制探针——`if [ -n "$full_probe" ] || [ ! -s data/npm-map.json ]`(:199):`skip_probes` 只省时间,不能在没数据时省探针。push/workflow_run 构建跳过 npm/downloads/stars/readmes/updates 五个探针(:200-222),**始终跑 tarballs、screenshots 与 capabilities**(:230/:237/:245)——"Probing is slow; that is cheaper than a wrong plugins.json"。**0007 注意:probe-release-history 没有独立 workflow**,它挂在 probe-updates 尾部,于是一并继承"只在全量探针构建里跑"的性质。
- **不变量**:`permissions: contents: read`(:48-49);注释 "The build never writes to the repository." 仍在——**该不变量只对 build-site 链成立**;仓库里唯一向 main 写入的是 sync-readme.yml(bot 提交 README,`contents: write` :33、提交 :99-101;0007 给它也加了 fork 门,并因此在本 fork 上同样停摆)。
- **依赖安装(0004 新增覆盖)**(:92-98):lockfile 里有 7 条 `resolved` 指向 `registry.npmmirror.com` 的 tarball URL(新增的索引依赖树 + `semver` + `js-yaml@4`),该 CDN 在 GitHub runner 上反复 503/504 并把 `npm ci` 挂上几十分钟(2026-10-19);CI 因此设 `npm_config_registry=https://registry.npmjs.org/` 与 `npm_config_replace_registry_host=always` 两个变量。两者缺一不可:只改 registry 不会重写 lockfile 里显式记录的镜像 URL。
- **三层缓存**(probe-data-v2 共享条目(:112-118)/ downloads-v1(:143-150)/ updates-v1(:152-156)刻意分离,#1673 后防版本连锁失效;#2797:downloads 不单独缓存时线上下载量比 npm 真实值低约 42%;0006 起 downloads-v1 的 save 有条件)。**0002 更正**:`data/updates.json` 是 **cache-only**,"NOT committed — unlike stars/downloads, there is no committed floor"。**0006 再添一个 cache-only 文件**:`data/releases.json`,但它连 cache 条目都没有(.gitignore:17 + 无 workflow 调用方),当前只活在维护者本机。
- **npm 发布(catalog/updates 双包)在 deploy 之后**(:301-318),且仅 nightly/manual。凭据 OIDC trusted publishing(`id-token: write`,npm ≥11.5);**deploy 失败对探针运行 continue-on-error**(:276),deploy 之败没资格拖住两个 publish 与 cache-save。0004 起 catalog 包里多了 `index.json`(`publish-catalog.mjs:55`、:130、:157-158),`catalogSha` 取 `plugins.json`+`index.json` 拼接的 sha256,所以只动索引的一天也会发一个版本;索引没有自立包是因为 trusted publishing 按包配置、不存在的包无法从 CI 建立关系(首次尝试 404),理由与代价写在 `publish-catalog.mjs:40-55`:每次 catalog 下载 +684 KB gzip(约 2.3 MB JSON),"拆出去才是终态"。**0007 的 release-history 树不在任何一个 npm 包里**,`publish-updates.mjs:108` 只写 `docs/updates.json`。
- **测试步骤**(`:99`):`node --test scripts/download-window.test.mjs`。0004 的 `card-install-command.test.mjs` 与 0007 的 `release-history.test.mjs`(118 行)都未接入本 workflow,也未接入 pr-check(pr-check:217-234 是五个点名测试:added-dates / capabilities / adopt-discussions / entries-path / npm-name,**0007 新增的只有 npm-name**)。
- **`build-index.mjs` 是第二个入口**:用法注释自称 `--check` 是 "CI gate",但仓库里没有任何 workflow 调它;实际写索引的是 build-site.mjs:194。两处都调同一个 `buildMarketIndex`,逻辑不会分叉,守卫却没有落地。

## 已知文档漂移

- 详情页量随当前名单更新:0003 基线 4489 条目、0004 基线 6704、0005 基线 7924、0006 基线 11744、0007 基线 **13136**(`ls data/plugins/*.yml | wc -l`,census 口径),按 ×2 推算约 **2.63 万个**静态详情页;首页与分类页现各多一个 JSON catalog 资源,另加一个全站 `index.json`、一棵 `docs/release-history/v1/` 分片树。精确构建输出总数仍无 CI build log 留档。
- build-site.mjs 头部注释(:2/:9)声称读 README 为 "the source of truth" 且 "re-syncs the plugin-count figure inside every README"——build 全文写盘调用无一触及 README,计数徽章走 shields endpoint。**两处过期注释都在 0007 后仍存在**;0001 后这句话有了例外形态:写 README 的是 sync-readme.yml,不是 build。
- AdSense 头注入(`adHead()`,build-site.mjs:81;token 定义 :89,变量未设时返回空串,`__AD_HEAD__\n` 连换行一起替换——**未设变量时产物与无广告构建逐字节相同**;注入点 :728/:785/:1065,privacy-template 没有)与 Giscus 评论懒加载(`mapping:'specific'` 按 `plugin:<slug>` 映射 Discussion、IntersectionObserver 400px 触发才注入 script——**不滚动=不联系第三方**;enabled 时四 ID 强校验)。
- **0002 修复的静默漂移**:giscus 的 term 从"构建时小写化"改为 `termOf(e.slug)` 原样(:979)。自评论区上线到 2026-09-24,这条小写化让**所有 owner/repo 含大写的条目被劈成两个 Discussion**——市场问 `plugin:FeatherHunter/dsh-prompt`,catalog 答 `plugin:featherhunter/dsh-prompt`,"Two threads, neither wrong"。同一份 `slugOf/termOf` 现由 build-site 与 adopt-discussions 共用(`lib/terms.mjs`)。
- **0004 落地的两个未接线件**:`build-index.mjs` 的 `--check` 与 `card-install-command.test.mjs` 都没进 CI。前者意味着"已发布索引是否仍是合法 format 1"没有任何门禁;后者意味着 #7752 的回归保护只在本机跑 `node --test` 时才存在。**0007 让后者更值得注意**:同一条测试现在也覆盖 `-w` 的形态,而 `release-history.test.mjs` 覆盖的分片预算/截断逻辑同样无门禁——三个未接线件。
- **0007 新增的静默面**:`docs/updates.json` 的 `count` 现在数的是"有 update 行 ∪ 有分片"的仓数,而历史分片本身没有任何发布侧校验(不校验 JSON 能否被消费方解析、不校验分片树与聚合文件的指针是否一一对应)。`publishReleaseHistory` 的返回值只有日志,失败不 exit。

## 待复核

- [ ] checkout + Pages 上传的实际耗时分布(workflow 无计时输出;UNVERIFIED)
- [x] ~~会不会自动提交 README~~ → build-site 链不会;**0001 起 sync-readme.yml 会**(仓库唯一写 main 的 workflow),见上;**0007 起在 fork 上也不会**(同一道 repository_owner 门)
- [ ] 0002:capabilities 三字段写进了 plugins.json,但**站内页面不渲染**(模板无对应 token)——确认消费方只有 dsh-market
- [ ] 0003:site-health 只比线上页面数与 `data/plugins/` 条目数;未见它校验生成 catalog 是否完整,应评估坏/缺 catalog 的部署能否被发现(0004 改成数 sitemap 后仍不覆盖)
- [ ] catalog JSON 的总输出字节及 Pages 实际部署/边缘缓存命中情况(当前只按构建逻辑确认,未从 production 下载测量)
- [ ] 0002:约 1.59 万个详情页是 7924×2 的推算值,没有构建日志佐证(UNVERIFIED);**0007 口径应为 13136×2 ≈ 2.63 万**,同样无日志佐证
- [ ] 0004:`docs/index.json` 的实际条目数与字节数无法本地复算——工作树里 `docs/` 与 `data/npm-map.json` 都被 .gitignore,只能引用提交信息里的实测(描述截断后 3.1 MB → 2.34 MB)**(UNVERIFIED)**
- [ ] 0004:`skip_probes` 碰到"有 npm/version 但无 `publishedAt`"的旧缓存会让 `indexBuilt=false`、不写 `docs/index.json`,而发布步骤无条件读它(`publish-catalog.mjs:130`)——推断,未实测
- [ ] 0004:索引每条 `homepage` 指向的 `/p/<slug>/` 可能还没生成(README 投影滞后窗口,见 [00 · 地图](./00-map.md)),需一次真实构建或线上抓页面确认(分类页字面 `__INDEX_LINE__` 已由线上确认,见上)
- [ ] 0006:含 `%` 的 slug 现在在 sitemap/hreflang 里以 `%25` 形态发布;`check-site-health` 按 sitemap URL 去重数页,两侧同源应自洽,但未实测一条含空格子目录的条目从投稿到详情页 200 的全链路(UNVERIFIED)
- [ ] 0006:`probe-releases` 没有任何 workflow 调用方,`data/releases.json` 既不提交也不进 cache——contributing.md 说"counts refresh daily through a separate cache",与当前工作区代码不符;GitHub-only 条目的 version 兜底因此在 CI 构建里恒缺席,待上游补接线后复核
- [ ] **0007 新增**:`docs/release-history/` 没有 prune 路径,`currentBytes` 又按现存文件统计——本地增量构建会重复计数,若把预算吃光,新仓的分片会被静默 `skipped`(只出现在日志里)。未实测
- [ ] **0007 新增**:预算减到负数(站点 >900 MB)时全部 `skipped`;当前 `docs/` 体积无法本地测量,余量未知
- [ ] **0007 新增**:分片契约只有 `{repo, complete, releases}`,没有 `updatedAt`/条目 URL/版本;消费方要靠 `docs/updates.json` 的 `releaseHistory: true` 自行拼 `release-history/v1/<owner>/<repo>.json`(小写)。这个约定没有任何文档或类型声明,是否已被 dsh-market 采用、路径大小写是否对齐,待验证
- [ ] **0007 新增**:本 fork 上构建链完全停摆后,`docs/`、边车与 README 只能靠 merge 从上游带进来;一次手动 dispatch 在这类 fork 上能否跑到 deploy(而非卡在 `environment: github-pages` 的审批/权限)未实测
- [ ] **0007 新增**:`release-history.test.mjs` 与 `card-install-command.test.mjs` 都未接线,分片字节上限/截断/`complete` 三条件的回归只靠本机 `node --test`
