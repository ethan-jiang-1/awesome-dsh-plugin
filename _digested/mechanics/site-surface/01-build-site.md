# 01 · build-site 主干与部署链

> 基线:`upstream@38976afd`(0001 复核)。行号 = scripts/build-site.mjs(**1098 行**,+155,旧 942/943 基线的行号已整体后移)除注明外。核心变更:README 生成归属重构(sync-readme.yml)、AdSense/Giscus 注入、并发组拆分、added-date 双账本、plugins.json 新增 version。

## 阶段流水

1. **常量与资产**(:19-53):`ORIGIN='https://awesome-dsh-plugin.com'` 硬编码;`site/assets/*` 平铺拷进 `docs/` 根(CNAME、robots.txt、badge.svg、logo.svg、双语 banner/og PNG、两个 woff2 字体子集、404.html);字体自托管的理由写在 template.html:27-31("a webfont request hands the visitor's IP to a third party on every page view")。
2. **解析 README 花名册**(:56-117):en 要求分隔符 `-`、zh 要求 `—`(取自 loc.sep);五类 parity 失败全部置 `parityBroken` → exit 1,"refusing to build (a silent drop would delist and delete pages)":同 locale 内 URL 重复 / 分隔符不符 / 某语言缺 URL / 同 URL 两语言分类不同(#343)/ 只存在于另一语言。分类归属是**标题子串匹配**(`h[1].includes(loc.categories[id])`)。
3. **数据加载与派生**(:119-291):
   - `added-dates.json` 是人工拥有的**冻结基线**(2026-08-15 前固定);缺失日期改用**双账本推导**(build-site.mjs:228-272):先按 en README 账本(`git log --reverse -p`,`maxBuffer: 256MiB`,首个新增条目行即收录日,保护已发布日期不漂移);仍缺者改查**条目自己的 yml 文件**的 added commit(`git log --diff-filter=A --format=%cI -- <file>`,取最旧;若条目在 merge commit 中首次出现——默认 log 看不到 merge 的 diff,#2662 三次改名事故——再以 `--diff-merges=first-parent` 兜底重试一次,只对没有答案的条目重试);两账本皆空才 exit 1("shallow clone or genuinely uncommitted entry",要求 CI `fetch-depth: 0`);
   - **星数覆盖率地板** `STARS_MIN_COVERAGE = 0.66`:未设 `SKIP_PUBLISH_CHECKS=1` 且覆盖率不足直接 throw(#1673 的 stars:{}×1362 教训;floor 判"磁盘已有",因为新条目合法地没有星数);
   - 截图:host 白名单四个 GitHub 域(key 必须 URL 精确匹配已列条目)、1–8 张、超限 exit 1;
   - 三方合并:`declared`(作者仓库的 screenshots.json)> legacy key;live verdict 仅剔除 ok:false(404/410),全死删整个字段而不是留空数组;
   - slug 规则:`repo--sub路径(/→-)`,无 sub 则 repo 本身。
4. **页面生成**(四轮循环):首页(:532)+ 分类页(:571,空分类跳过)+ 隐私页(:617,缺 privacyBody 文件 exit 1,检查在 :618-619)+ 详情页 ×7110。替换实现分两类:**结构块用 regex+回调函数**(避免 `$&` 类特殊序列被展开),标量 token 用 `replaceAll('__X__', () => v)` 同样带回调。index/category 两轮新增 `__CARD_COUNT__`(服务端渲染计数,消除 #count CLS,:555/:603)与 `__AD_HEAD__`(:556/:604)。孤儿详情页清理:重建 live slug 集合后 rmSync 不匹配者(:895-910)。
5. **README 渲染**(:545-602):Marked + heading depth+1(cap 6)、相对链接基于 raw base 解析;`renderer.html` 返回空串——**详情页正文里裸 HTML 全部丢弃**;图片必须过 SCREENSHOT_HOSTS(允许 `data:`),丢图后清理空 `<a>`/`<p>`。多语言选择按 LOCALES 顺序回退,兼容旧的无 key 结构,命中非本页语言时提示 P_README_ONLY 并在包裹 div 标真实 lang。
6. **数据产物**:

| 产物 | 内容 | 关键点 |
|------|------|--------|
| `docs/plugins.json` | 完整注册表(name/owner/url/page/category/desc/npm/**version**/tarball/stars/downloads/install/added/screenshots)| tarball 键 absent 时省略而非 null;**version = npm dist-tags.latest,null=github-only 或无 latest**(build-site.mjs:389-390、:969-972,消费方 dsh-market#348;version 与 downloads 是不同信号,null 语义不同);updates **故意不并入**(市场每次打开都拉这个文件,release body 会撑爆,:647-653)|
| `docs/count.json` | shields endpoint schema `{schemaVersion,message:N,color,cacheSeconds:300}` | README 徽章的消费端;cacheSeconds 取 shields 下限 300,因为徽章下面就是列表,数对不上会被当 bug |
| `docs/readmes.json` | 详情页正文源(locale→{md,base,blobBase})| MB 级 |
| `docs/updates.json` | 来自 data/updates.json,仅 listed | KB 级 |
| `docs/feed.xml` ×2 | 按 addedAt 倒序 newest 30 条 | |
| `docs/sitemap.xml` | 四类 URL + 全套 hreflang alternates | 分类页 daily、详情页 weekly(lastmod=e.added)、隐私页 yearly,lastmod 取隐私源文件最后 commit 日期——"lastmod 每晚移动而内容没变会让爬虫不再相信全站的 lastmod" |

## 部署链(build-site.yml)

- **触发**:nightly cron `23 2 * * *` + workflow_dispatch(带 probe_all input)+ push 到 main(无 paths 过滤,刻意)。**0001:并发组一拆为二**(build-site.yml:49,#3789):`build-site-push` / `build-site-probe`——push 只取消/取代 push 构建,**永远不能取消 nightly**;nightly 是唯一 PROBE_ALL + npm 发布的运行,被取消连 cache-save post-steps 一起丢(病灶:cron 常推迟数小时进入繁忙时段,被下一次 merge mid-probe 取消;三个同根因症状 #3512 catalog 冻结三天、#3417/#3698 READMEs 卡旧值)。拆分引入 Pages 单部署竞态 → nightly 的 deploy 对失败 continue-on-error(:197;#4386:9-05 一次 dispatch 跑 36 分钟探针后死于 403,probe 从头重来)。
- **不变量(0001 修订)**:`permissions: contents: read`;注释 "The build never writes to the repository." 仍在(build-site.yml:24)——**该不变量现在只对 build-site 链成立**;仓库里唯一向 main 写入的是 sync-readme.yml(bot 提交 README,:69),刻意独立成窄权限 workflow 以保住 build 不写仓库这句话。"docs/ is a pure function of main's tip" 的并发表达已按并发组拆分改写(见上)。
- **三层缓存**(probe-data-v2 共享条目 / downloads-v1 / updates-v1 刻意分离,#1673 后防版本连锁失效;#2797:downloads 不单独缓存时线上下载量比 npm 真实值低约 42%):改缓存 path 列表 = restore-keys 匹配不到 = 全体冷启动。
- **push 构建基本不做 probe**(五个全跳,只留 tarballs/screenshots);冷缓存且 npm-map 为空的兜底分支会临时跑全套——"Probing is slow; that is cheaper than a wrong plugins.json"。PROBE_ALL=1 仅 nightly/manual 强制时置位。
- **npm 发布(catalog/updates 双包)在 deploy 之后**(build-site.yml:200-239),且仅 nightly/manual——曾两天合入 46 个 release,每次 merge 都给维护者发一条 npm 通知。凭据 OIDC trusted publishing(`id-token: write`,npm ≥11.5),无需 NPM_TOKEN;**deploy 失败对探针运行 continue-on-error**(:197),deploy 之败没资格拖住两个 publish 与 cache-save。

## 已知文档漂移

- build-site.mjs:9 注释声称 "re-syncs the plugin-count figure inside every README"——build 全文写盘调用无一触及 README,计数徽章走 shields endpoint。**过期注释,行为是「build 从不碰源文件」**;0001 后这句话有了例外形态:写 README 的是 sync-readme.yml,不是 build。
- 0001 新增:AdSense 头注入(`adHead()`,变量未设时返回空串,`__AD_HEAD__\n` 连换行一起替换——**未设变量时产物与无广告构建逐字节相同**;仅 template:264 与 detail:187 有注入点,privacy-template 没有)与 Giscus 评论懒加载(`mapping:'specific'` 按 `plugin:<slug>` 映射 Discussion、IntersectionObserver 400px 触发才注入 script——**不滚动=不联系第三方**;enabled 时四 ID 强校验,"半配置组件不得给每个访客发坏请求")。

## 待复核

- [ ] checkout + Pages 上传的实际耗时分布(workflow 无计时输出;UNVERIFIED)
- [x] ~~会不会自动提交 README~~ → build-site 链不会;**0001 起 sync-readme.yml 会**(仓库唯一写 main 的 workflow),见上
