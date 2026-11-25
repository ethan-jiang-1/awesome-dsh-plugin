# site-surface · 站点

> 状态:**0007 有实质 diff**(基线 `upstream@8f1a1800e`,2026-11-25)。行号 = `scripts/build-site.mjs`(**1296 → 1317 行**,除注明外)。三处性质变化:① **Release 历史成了站点上的第二类数据产物**——`data/updates.json` 的内部键 `$releaseHistoryV1` 被 `publishReleaseHistory()` 拆成每仓一片 `docs/release-history/v1/<owner>/<repo>.json`(单文件 ≤1 MB、每仓 ≤256 条、总预算 `900_000_000 − docs/ 现有字节`),`docs/updates.json` 不再内嵌历史,只给已发布分片的条目打 `releaseHistory: true`,并给"只有历史没有 update 行"的仓补一条;② **tarball 安装命令补 `-w`**(`releaseTarballCmd()`,`:449-452`)——DSH profile 本身是 pnpm workspace 根,不加 `-w` 在 workspace 根上装不进去;卡片、详情页、`plugins.json.install` 三处一起变;③ **`build-site.yml` 加 job 级 fork 门**(`:78`)——本仓库是 `ethan-jiang-1` fork,合并后本站**不再自动构建/部署**,push、nightly、`workflow_run` 全被跳过,只剩手动 dispatch。另有英文 `TITLE`/`DESC` 两行改词(`site/locales.mjs:33-34`),`site/` 其余零 diff(879 行首页模板、334 行详情页模板、32 个详情页 token、中文 locale 全部未动)。最近核验:`8f1a1800e`。
>
> 【历史 · 0006,基线 `29b3ed46e`,2026-11-18】三条主线:① `lib/terms.mjs` 新增 `slugHref()`——slug 里的 `%` 是数据不是转义,插进 href 前要二次编码,build-site 与 market-index 的全部详情页/卡片/目录/hreflang/`page` 字段改走它;② `lib/market-index.mjs` 新增 npm 名占用仲裁(monorepo 根与子包解析到同一 npm 包时,格式 1 只丢重复那一行,不再拒整份索引);③ build-site 读 `data/releases.json`(cache-only 新边车)给 GitHub-only 条目的 `version` 做 release-manifest 兜底,并给 registry 新增 `starsCheckedAt` / `githubReleaseDownloads(CheckedAt)` / `releaseManifest` 字段。`site/`(template、locales、privacy)当时零 diff。上述结论仍适用于 0006 基线,行号需按下方 0007 速查表重取。
>
> 【历史 · 0005 / 0004 / 0003】0005 无对应 diff(基线 `upstream@efe602e7b`,2026-10-31)。0003 把首页/分类页改成 24 张 SSR 回退卡 + JSON catalog 虚拟列表;0004 在此之上多出**第三个发布面**——把名单本身导出为 DSH 插件市场索引(`docs/index.json`,format 1),首页搜索条下多一行"索引源"地址;site-health 的取证点从窗口化首页挪到 `sitemap.xml`;卡片安装命令补回作者声明的 tarball 一级。

## 定位

`site/` + `scripts/build-site.mjs` 是注册表的第二个发布面:从同一份名单长出约 **2.63 万个 HTML 页面**(13136 条目 ×2 语言详情页 = 26272,加每 locale 的首页/23 分类页/隐私页共 25 页 ×2 = 50;条目数取自 0007 口径 `ls data/plugins/*.yml | wc -l`,按构建逻辑 ×2 推算,**非构建日志读数**)+ 十余个全站数据产物,并额外为首页与各有条目的分类页生成语言/分类专属 `catalog.json`;共最多 **48 个 catalog 文件**(每语言 1 首页 + 23 个分类页,当前 23 类均有条目)。静态 HTML 与 JSON 部署到 GitHub Pages(`site/assets/CNAME` = awesome-dsh-plugin.com),前端由 Cloudflare 加速。首页/分类页只 SSR 下载排名前 24 张卡;JavaScript 加载 catalog 后按视口窗口化渲染全量列表,失败则退回这 24 张,`<noscript>` 明示仅有首屏内容。catalog URL 带内容 hash query 防 CDN 旧缓存。统计(Cloudflare Web Analytics)无 cookie,但站点**有条件地**携带两个第三方:Google AdSense(构建变量 `ADSENSE_CLIENT` 设定时进入每个首页/分类/详情页,隐私页除外,当前变量未设=字节级无广告)与 Giscus 评论(仅当访客把评论面板滚到视口附近)。

**0007 起站点上多了第二类数据:每仓 Release 历史分片。** 它不是页面,也不是新的边车——入口仍是既有的 `data/updates.json`(cache-only),只是那个文件里多了一个内部键 `$releaseHistoryV1`;build-site 把它拆成一棵 `docs/release-history/v1/<owner>/<repo>.json` 树,再在 `docs/updates.json` 里用 `releaseHistory: true` 当指针。之所以拆:市场每次打开都要拉 `updates.json`,把每仓最多 256 条 release notes 内嵌进去会把这个聚合文件撑爆(0006 的注释已写过同一理由);拆完单个分片受 1 MB 与 Pages 全站 1 GB 两条上限约束。机制细节见下文 §0007 的改动,探针侧怎么填这个键见 [probes-and-decay/01](../probes-and-decay/01-probe-family.md)。

**第三个发布面是文档而不是页面。** `docs/index.json` 是 DSH 0.2.1 引入的 plugin market index(format 1):host 在官方 Plugins → Discover 与 `plugin_market` agent tool 里把它当 market source 读。构建用 `@deepseek-ai/dsh-plugin-market-index`(host 端同一个 parser)校验,注释里的目标是"从这里出去的文档不可能是 DSH 拒绝的那一份"。同一份字节走两条路:Pages 根(`awesome-dsh-plugin.com/index.json`)与 npm 包 `dsh-plugin-catalog`;首页和两份 README 给的是后者(`cdn.jsdelivr.net/npm/dsh-plugin-catalog/index.json`),理由是 host 的取数预算固定 15 s,而当时 3.1 MB 的 Pages 版从大陆网络实测要 22.7 s、同一份文件走 jsDelivr 约 1 s(提交信息实测,非本地复算)。**覆盖面只有 npm 条目**:需要包名、精确版本与该版本发布时间三件套;纯 GitHub 条目在 format 1 里没有表达式(每个 Git 版本要 commit SHA,本仓库不记录),upstream 自述约占名单一半。

0002 新增一条与"发布面"并列的**监督面**:`.github/workflows/site-health.yml` + `scripts/check-site-health.mjs`(168 行,0003 时 152)每天 07:23 取线上 `sitemap.xml`,数去重后的英文 `/p/<slug>` 页面,与 `data/plugins/` 的条目数比对,落后超过 tolerance(默认 300)即失败。注释交代了动机:dshmarket.com 曾在 2026-09-09 → 09-25 **静默冻结 18 天**(3,363 页对 4,347 条,1,082 个插件根本没有页面)而仓库里毫无痕迹;同一段注释还把"schedule 根本不再触发"(GitHub 对 60 天无活动的仓库会停掉定时任务)算进覆盖范围。它刻意**不**与已发布的 catalog 比对——"页与 catalog 出自同一次构建,拿站点比自己的 catalog 等于比自己"。取数失败一律 exit 1(检查不了 ≠ 全好)。

**0004 换掉了取证点**:0003 起的首页是窗口化的,数首页 `href="/p/<slug>/"` 数的是那个窗口——2026-10-19 报 48 页对 5,945 条目录,且从 2026-10-10 起每天误报(1ae7fd858)。改数 sitemap 后两侧都成了页面级量:预期值仍是 `data/plugins/` 的文件数(`--catalog-dir`),实际值来自 sitemap 里两语言的详情页 URL(去掉 `/zh/` 后按 slug 去重)。代价是它仍然只回答"页面在不在",不回答"内容是否冻结",也不看 `index.json`——**0007 之后它同样不看 `release-history/`**。

**0006 给详情页 URL 加了一条编码规则(`slugHref`,`lib/terms.mjs:37-39`)**:slug 是条目 URL 的原文投影,所以源路径里一个百分号编码的字节(monorepo 子目录带空格 → `%20`)在这里是**数据,不是转义**——直接插值进 href,浏览器会再解码一次,请求一个没有文件对应过的路径。修法只做一件事:`slug.replaceAll('%', '%25')`,把 `%` 二次编码;其余字符逐字节保留,所以 CJK slug(浏览器 URL 合法)与不含 `%` 的 slug 发出的 URL 与今天发布的逐字节相同。0007 后这些调用点的当前行号:卡片(:569/:573)、catalog `href`(:626)、详情页 canonical/hreflang(:906-910)、相关插件(:971)、语言切换按钮(:1063)、registry `page`(:1146)、sitemap `<loc>` 与 alternates(:1299/:1302);market-index 的 `homepage`(`lib/market-index.mjs:133`)**未随本轮改动**。giscus term(`termOf`,`lib/terms.mjs:42-44`)**不改**——giscus 要的是 slug 原文,不是路径段。

## 0007 的改动

本轮 `scripts/` 侧的真实 diff 只落在 `build-site.mjs`(+24/−3)、新增的 `lib/release-history.mjs`(144 行)与 `site/locales.mjs`(+2/−2);`site/` 目录的 `git diff --stat` 只有 locales 一个文件。

### 一、Release 历史:从"一个键"到"一棵分片树"

缓存侧(`probe-updates.mjs` 尾部调 `probe-release-history.mjs`)把采集结果写进 `data/updates.json` 的内部键 `$releaseHistoryV1`(键名常量在 `lib/release-history.mjs:7`,数据文件里带前导 `$`,所以永远不会和条目 URL 键撞车)。发布侧在 `build-site.mjs:1229-1260` 一个块里做四件事:

1. 取历史:`const history = updates[HISTORY_CACHE_KEY] ?? {}`(:1231)。
2. 量现有体积:`fs.readdirSync('docs', { recursive: true, withFileTypes: true })` 递归累加现存文件字节(:1234-1236),**只在 history 非空时计算**,空则记 0;注释写明的动机是 Pages 全站 1 GB,要给 updates manifest、sitemap 与 artifact 元数据留空间(:1232-1233)。这个测量点位于 `plugins.json`(:1188)与 `readmes.json`(:1219 写盘)之后、`sitemap.xml`(:1278)与 `count.json`(:1313)之前,所以它统计的是"页面 + site/assets + catalog + registry + readmes + feeds",不含随后写的那三个文件。
3. 写分片:`publishReleaseHistory(ordered, history, 'docs', 900_000_000 - currentBytes)`(:1237),返回 `{repositories, publishedBytes, skipped}`。
4. 打标记:见下一条。

`publishReleaseHistory`(`lib/release-history.mjs:111-144`)的语义,逐条读出来的:

- **发布范围**是 `ordered` 里 `catalogRepo()` 能规范化的 URL(`:115`)。`catalogRepo`(:14-18)把 owner/repo 全小写,要求匹配 `^[a-z0-9-]+/[a-z0-9_.-]+$` 且不以 `/.`、`/..` 结尾,否则返回 `null` 直接跳过——所以非 github.com 的条目、解析不出 owner/repo 的 URL 都没有分片。
- **数据源**优先 `history.fallback ?? history.releases`(:118)。`fallback` 是 7 天重扫期间保留的上一版已发布内容(见 `refreshHistory`,`:68-95`),避免边扫边把线上分片掏空。source 不是数组或为空则跳过(:119)。
- **单文件字节上限 1,048,576**:从 `128 + byteLength(repo)` 起算(给对象外壳留量),逐条累加 `byteLength(JSON.stringify(release)) + 1`;累加超过 1 MB 或已攒满 `MAX_RELEASES = 256` 条就停(:120-127)。一条都放不下则整个仓跳过(:128)。
- **`complete` 三条件**:`history.fallback === undefined && history.next === null && releases.length === source.length`(:129)。任何一条不满足就是"还能更新/正被截断",消费方据此知道这份不是终态。
- **总预算**:每片写完前判 `publishedBytes + length > budget` 则 `skipped++` 并 continue(:132-135)。预算由 build-site 传入,所以"900 MB 减现有站点字节"这个口径只写在调用点一处。
- **落点**:`docs/release-history/v1/<owner>/<name>.json`,`mkdirSync` 递归建目录,内容 `JSON.stringify({ repo, complete, releases }) + '\n'`(:136-139)。
- **只写不删**:函数里没有任何 prune 分支。CI 是干净 checkout + `upload-pages-artifact` 整目录上传(:254),所以不留残骸;**本地增量构建**(docs/ 不 wipe,只在 :1082-1102 清孤儿详情页)会留下已下架仓的旧分片,并被下一次的 `currentBytes` 计入(推断,未实测)。

一行构建日志收尾:`release history: <分片数> repository fragments, <字节> bytes, <skipped> over the Pages budget`(:1259)。

### 二、`docs/updates.json`:标记、补行、不内嵌

同一个块的后半段(:1245-1257)重写了聚合文件的条目集合:

- 第一轮遍历 `data/updates.json` 的条目,只保留 listed(:1246)。`$releaseHistoryV1` 不在 listed 里,所以**缓存键天然不会漏进公开文件**。有对应分片的条目写成 `{ ...entry, releaseHistory: true }`(:1247-1249)——原字段(release/commits/checkedAt)全部保留,只多一个布尔;没有分片的照旧 `entry`。
- 第二轮按 url 排序补齐:凡是 listed 里"有分片但第一轮没写进去"的仓(即只有历史、没有 update 行),补一条 `{ releaseHistory: true }`(:1252-1256)。于是 `docs/updates.json` 的条目集合 = 有 update 行的仓 ∪ 有分片的仓,`count` 两轮都加(:1250/:1255)。
- 序列化:`JSON.stringify(payload) + '\n'`(:1257)。**这一行本轮未变**——`docs/updates.json` 从 0006 起就是压缩 JSON。本轮去掉 pretty-print 的是探针侧的 `data/updates.json`(`probe-updates.mjs:341-342`,`tmp + rename` 原子写;0006 时是 `JSON.stringify(sorted, null, 1)`),两者不要混为一谈。

缓存里并不内嵌历史:`docs/updates.json` 只带指针,历史在 `docs/release-history/` 树里。消费方要拿历史,得先读聚合文件的 `releaseHistory: true`,再按 `https://github.com/<owner>/<repo>` 推出 `release-history/v1/<owner>/<repo>.json`(小写)。

### 三、tarball 安装命令补 `-w`

新增 `releaseTarballCmd(tarball)`(:449-452):falsy → `null`,否则 `dsh plugin --profile web add -w "<tarball>"`。注释只有一句:"The DSH profile is itself a pnpm workspace root."——不加 `-w`,pnpm 会把它当 workspace 子包安装,在 workspace 根上直接失败(本轮提交族 `tarball -w` 的动机)。

三个消费点同源:

- `e.cmdTarball = releaseTarballCmd(e.tarball)`(:467),每条目派生一次;
- 详情页 `cmds` 的第二档仍用 `e.cmdTarball`(:951),自动带上 `-w`;
- registry `install: cardCmd(e)`(:1176)——0006 时这里是内联三元 `e.npm ? npm : (e.cmdTarball ?? e.cmdGit)`,与 `cardCmd()`(:543-545)逐字等价,本轮改成直接复用函数、消掉重复;但因为 `cmdTarball` 本身变了,`plugins.json.install` 里 tarball 条目的字符串也随之带上 `-w`。

测试同步:`scripts/card-install-command.test.mjs` 从"只抽 `cardCmd`"改成按函数名抽取的 `commandHelper(name)`,并在断言里复算 `dsh plugin --profile web add -w "…"` 形态。**它仍然没有任何 workflow 运行**:`build-site.yml:99` 只跑 `download-window.test.mjs`,`pr-check.yml:217-234` 是五个点名测试(added-dates / capabilities / adopt-discussions / entries-path / npm-name),两处都没有 `node --test` 通配。

### 四、fork 安全门:本仓库不再自动部署

`build-site.yml` 本轮 +4 行,全部是 job 级守卫:

```yaml
jobs:
  build:
    # A fork mirrors the catalog but does not publish the site, so the job is
    # skipped there to spare the fork owner's Actions minutes on a deploy
    # nothing consumes. A manual dispatch still runs, for debugging.
    if: github.repository_owner == 'awesome-dsh-plugin' || github.event_name == 'workflow_dispatch'
```

(`:75-78`;本文件 0006 起 314 行 → 本轮 **318 行**。)

这条门对整个站点的意义:**`build-site.yml` 只有一个 job**,deploy、cache-save、双 publish 都是这个 job 里的 step(`:248-250` save downloads cache、`:254` upload-pages-artifact、`:258` deploy-pages、`:301-307` catalog publish、`:314-318` updates publish),所以 job 一跳过,fork 上整条链一步都不跑。`github.repository_owner` 在本仓库是 `ethan-jiang-1`(upstream 是 `awesome-dsh-plugin`),四个触发里只有 `workflow_dispatch` 能穿过——push、`schedule`(`23 2 * * *`)、`workflow_run` 全部被门挡掉。

对本仓库的直接后果(需记住的运营事实):

- 同步后工作区里**没有** `docs/`(`.gitignore:9` 忽略);`data/updates.json` 也不在——它是 cache-only,只活在 CI 的 `updates-v1` 缓存里(`.gitignore:17` 列的是另一个 cache-only 文件 `data/releases.json`)——所以站点产物无法在本地核实,只能引用提交信息与代码。
- 从上游 merge 进来的 `docs/`、边车、README 都是**上游产物**,不是本 fork 跑出来的;想验证一次真实构建,只能在 Actions 里手动 dispatch(仍会跑,但仍会在本 fork 的 Pages 上尝试部署,受 fork 的 Pages 配置约束,未实测)。
- 同轮另有 7 条 workflow 加了同一条门(`sync-readme`、`decay-scan`、`pr-guard`、`regate`、`held-rescan`、`adopt-discussions`、`site-health`);`pr-check.yml` / `pr-gate.yml` 不加,PR 事件在 fork 上照跑。归属见 [submission-gates](../submission-gates/00-map.md) 与 [probes-and-decay](../probes-and-decay/00-map.md),这里只记 build-site 这一条。

### 五、英文标题两行

`site/locales.mjs` +2/−2,只有英文的 `TITLE`(:33)与 `DESC`(:34):

- `TITLE` → `Awesome DSH Plugin — Curated List of DSH Plugins for DeepSeek Harness`
- `DESC` → `A curated list of {N} DSH plugins for DeepSeek Harness (dsh): …`(其余短语原样)

中文 `TITLE`(:176)/`DESC`(:177)、`CAT_TITLE`/`CAT_DESC`/`P_TITLE` 模板、两语言各 64 条 `strings` 与 23 个分类译名全部零 diff,`site/template.html`(879 行)、`site/detail-template.html`(334 行,32 token)、`privacy-*.html` 也全部未动。也就是说这轮**没有 token 契约变化**,00→02 的接口仍是 0004/0006 那一套。

## 0007 行号速查(当前 checkout)

| 位置 | 行号 |
|---|---|
| `releaseTarballCmd()` | `build-site.mjs:449-452` |
| `e.cmdTarball` 派生 | `:467` |
| `cardCmd()` | `:543-545` |
| `FALLBACK_CARDS = 24` | `:534` |
| `catalogPayload()` / 卡片 `href` | `:602-632` / `:626` |
| `catalogHref()` | `:634-637` |
| `INDEX_LINE` 定义 / 首页替换 | `:687-692` / `:725` |
| 首页循环 | `:696-733` |
| 分类页循环(**无** `__INDEX_LINE__` 替换) | `:745-802` |
| 隐私页循环 | `:805-827` |
| 详情页循环 / token 填充链 | `:834-1080` / `:1040-1075` |
| registry 对象 / 写盘 | `:1128-1188` / `:1188` |
| readmes 块 | `:1199-1221` |
| updates + release-history 块 | `:1229-1260` |
| sitemap 写盘 / `<loc>` / alternates | `:1278` / `:1299` / `:1302` |
| `count.json` | `:1313` |
| `slugOf` / `slugHref` / `termOf` | `lib/terms.mjs:22` / `:37-39` / `:42-44` |
| `HISTORY_CACHE_KEY` / `catalogRepo()` | `lib/release-history.mjs:7` / `:14-18` |
| `publishReleaseHistory()` | `lib/release-history.mjs:111-144` |
| fork 门 | `build-site.yml:78` |

## 本专题最重要的一个架构事实

**build-site 的花名册来源是 README,不是 YAML;但 README 本身已降级为生成物。** 它逐行正则解析两份 README 得到条目集合(`parseReadme`,build-site.mjs:108-129);YAML 只被读来补三样东西——条目文件路径(:49)、门店图 `icon`(:50-54)、tarball 映射(:55-65)——再加 0004 的市场索引(:189-190)。0001 起投稿改为 **yml-only**(#3832/#4004):人工编辑点只有 data/plugins/*.yml;README 由 sync-readme.yml 在 merge 后由 bot 于 main 上重生成并提交(sync-readme.yml 的 `contents: write`——全仓库唯一向 main 写入的 workflow,0002 复核仍成立;0007 只给它加了 fork 门,没动生成逻辑)。pr-check 的 `generate-readme --check` 守卫仍在但语义收窄:**只拦截"PR 自己手改 README 且与 yml 不符"**(pr-check.yml:210);yml-only PR(现在的常态)不经过它。完整因果链变为:

```text
data/plugins/*.yml ──(PR, yml-only)──▶ merge ──sync-readme.yml bot commit──▶ README.md/README.zh.md ──parseReadme──▶ site/docs/*
   (唯一人工编辑点)                                    (bot 生成的中间投影)                    (生成物 ×2:页面+数据)
```

0004 给这条链加了**第二条取数路径**:市场索引不经 `parseReadme`,直接 `readEntries()` 读 `data/plugins/*.yml`(:189)。于是索引是站上第一个"跳过 README 投影"的产物:yml-only PR 刚 merge、bot 还没再生 README 的窗口里,索引已经列出新条目,而每条记录的 `homepage` 指向 `${ORIGIN}/p/<slug>/`——那一页要等下一次构建才存在(推断,未实测;窗口通常被 `workflow_run` 触发的那次构建关掉)。0007 的 release-history 块走的是 `ordered`(README 投影),所以它**没有**跳过 README——这是它与索引的结构差别,不要混同。

0002 补上这条链上刚被发现的**断点**:bot 用默认 GITHUB_TOKEN 提交不会触发 `push`,所以站点会永远慢一个 merge(2026-09-20 实测 main 4,014 条、已发布 4,012,且 bot 那个 sha 上根本没有 build-site 运行)。修法是 build-site 增加 `workflow_run` 触发(build-site.yml:30-31),而不是让 bot 去 dispatch。同一次修复把探针开关从"排除 push"改成**事件白名单**(build-site.yml:189-198 的 `case`:schedule → 全量、dispatch 看 `skip_probes`、其余置空)。**0007 的 fork 门把这条修复在 fork 上一并废掉**:`workflow_run` 现在连 job 都进不去,所以 fork 上"慢一个 merge"不再是问题,因为根本不构建。

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
- [x] **0004 新增,线上已确认**:"索引源"那一行只在首页循环里被替换(build-site.mjs:725),分类页循环(:745-802)没有对应替换。2026-10-24 直接抓 https://awesome-dsh-plugin.com/tools/ ,搜索条下原样输出字面 `__INDEX_LINE__`(同次抓首页无此字面)——这是 0004 引入的用户可见缺陷,不是文档推断;**0007 复核仍未修**(分类页链式替换里没有 `__INDEX_LINE__`)
- [ ] **0007 新增**:`docs/release-history/` 树没有清理路径(`publishReleaseHistory` 只写不删);CI 干净 checkout 下无害,但本地增量构建或将来改成持久 `docs/` 时会留下已下架仓的分片,并被 `currentBytes` 重复计入。未实测
- [ ] **0007 新增**:预算 `900_000_000 − currentBytes` 在站点字符数超过 900 MB 时会变负数,所有分片都会被 `skipped`;当前 `docs/` 实际体积无法本地测量(工作区没有 `docs/`,gitignored),余量未知
- [ ] **0007 新增**:分片文件只有 `{repo, complete, releases}` 三字段,没有更新时间/条目 URL/版本;消费方要靠 `docs/updates.json` 的 `releaseHistory: true` 自己去推路径。这个契约没写进任何 README 或模板,是否会被 dsh-market 采用、路径大小写是否对齐,待验证
- [ ] **0007 新增**:`release-history.test.mjs`(118 行)与 `card-install-command.test.mjs` 都没有接进任何 workflow——新机制的核心预算/截断逻辑目前只有本机 `node --test` 才会跑到
