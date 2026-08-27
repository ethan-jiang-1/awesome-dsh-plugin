# 01 · build-site 主干与部署链

> 基线:`main@5e7dc7eb`。行号 = scripts/build-site.mjs(943 行,末行无换行)除注明外。

## 阶段流水

1. **常量与资产**(:19-53):`ORIGIN='https://awesome-dsh-plugin.com'` 硬编码;`site/assets/*` 平铺拷进 `docs/` 根(CNAME、robots.txt、badge.svg、logo.svg、双语 banner/og PNG、两个 woff2 字体子集、404.html);字体自托管的理由写在 template.html:27-31("a webfont request hands the visitor's IP to a third party on every page view")。
2. **解析 README 花名册**(:56-117):en 要求分隔符 `-`、zh 要求 `—`(取自 loc.sep);五类 parity 失败全部置 `parityBroken` → exit 1,"refusing to build (a silent drop would delist and delete pages)":同 locale 内 URL 重复 / 分隔符不符 / 某语言缺 URL / 同 URL 两语言分类不同(#343)/ 只存在于另一语言。分类归属是**标题子串匹配**(`h[1].includes(loc.categories[id])`)。
3. **数据加载与派生**(:119-291):
   - `added-dates.json` 是人工拥有的**冻结基线**(2026-08-15 前固定);缺失的从 git 历史推导——对 en README 跑 `git log --reverse -p`,`maxBuffer: 256MiB`,首个新增条目行即收录日;推不出就报错(要求 CI `fetch-depth: 0`);
   - **星数覆盖率地板** `STARS_MIN_COVERAGE = 0.66`:未设 `SKIP_PUBLISH_CHECKS=1` 且覆盖率不足直接 throw(#1673 的 stars:{}×1362 教训;floor 判"磁盘已有",因为新条目合法地没有星数);
   - 截图:host 白名单四个 GitHub 域(key 必须 URL 精确匹配已列条目)、1–8 张、超限 exit 1;
   - 三方合并:`declared`(作者仓库的 screenshots.json)> legacy key;live verdict 仅剔除 ok:false(404/410),全死删整个字段而不是留空数组;
   - slug 规则:`repo--sub路径(/→-)`,无 sub 则 repo 本身。
4. **页面生成**(四轮循环):首页 + 分类页(空分类跳过)+ 隐私页(缺 privacyBody 文件 exit 1)+ 详情页 ×4572。替换实现分两类:**结构块用 regex+回调函数**(避免 `$&` 类特殊序列被展开),标量 token 用 `replaceAll('__X__', () => v)` 同样带回调(:433-449)。孤儿详情页清理:重建 live slug 集合后 rmSync 不匹配者(:743-761)。
5. **README 渲染**(:545-602):Marked + heading depth+1(cap 6)、相对链接基于 raw base 解析;`renderer.html` 返回空串——**详情页正文里裸 HTML 全部丢弃**;图片必须过 SCREENSHOT_HOSTS(允许 `data:`),丢图后清理空 `<a>`/`<p>`。多语言选择按 LOCALES 顺序回退,兼容旧的无 key 结构,命中非本页语言时提示 P_README_ONLY 并在包裹 div 标真实 lang。
6. **数据产物**:

| 产物 | 内容 | 关键点 |
|------|------|--------|
| `docs/plugins.json` | 完整注册表(name/owner/url/page/category/desc/npm/tarball/stars/downloads/install/added/screenshots)| tarball 键 absent 时省略而非 null;updates **故意不并入**(市场每次打开都拉这个文件,1300 条 release body 会撑爆,:539-541)|
| `docs/count.json` | shields endpoint schema `{schemaVersion,message:N,color,cacheSeconds:300}` | README 徽章的消费端;cacheSeconds 取 shields 下限 300,因为徽章下面就是列表,数对不上会被当 bug |
| `docs/readmes.json` | 详情页正文源(locale→{md,base,blobBase})| MB 级 |
| `docs/updates.json` | 来自 data/updates.json,仅 listed | KB 级 |
| `docs/feed.xml` ×2 | 按 addedAt 倒序 newest 30 条 | |
| `docs/sitemap.xml` | 四类 URL + 全套 hreflang alternates | 分类页 daily、详情页 weekly(lastmod=e.added)、隐私页 yearly,lastmod 取隐私源文件最后 commit 日期——"lastmod 每晚移动而内容没变会让爬虫不再相信全站的 lastmod" |

## 部署链(build-site.yml)

- **触发**:nightly cron `23 2 * * *` + workflow_dispatch(带 probe_all input)+ push 到 main(**无 paths 过滤,刻意**:每次 push 要么取消在跑的构建要么取代它,无关 push 只是重复部署相同字节)。
- **不变量**:`permissions: contents: read`;注释明示 "The build never writes to the repository."——**整个部署链没有任何自动 commit/push**(grep workflows 全目录仅 pr-guard 给贡献者的说明性评论文本含 git push 字样)。"docs/ is a pure function of main's tip" 由 concurrency `build-site` + cancel-in-progress 表达。
- **三层缓存**(probe-data-v2 共享条目 / downloads-v1 / updates-v1 刻意分离,#1673 后防版本连锁失效;#2797:downloads 不单独缓存时线上下载量比 npm 真实值低约 42%):改缓存 path 列表 = restore-keys 匹配不到 = 全体冷启动。
- **push 构建基本不做 probe**(五个全跳,只留 tarballs/screenshots);冷缓存且 npm-map 为空的兜底分支会临时跑全套——"Probing is slow; that is cheaper than a wrong plugins.json"。PROBE_ALL=1 仅 nightly/manual 强制时置位。
- **npm 发布(catalog/updates 双包)在 deploy 之后**,且仅 nightly/manual——曾两天合入 46 个 release,每次 merge 都给维护者发一条 npm 通知(build-site.yml:168-180)。凭据 OIDC trusted publishing(`id-token: write`,npm ≥11.5),无需 NPM_TOKEN。

## 已知文档漂移

- build-site.mjs:9 注释声称 "re-syncs the plugin-count figure inside every README"——全文写盘调用无一触及 README(grep writeFileSync 落点仅在 docs/),计数徽章走 shields endpoint。**过期注释,行为是「build 从不碰源文件」**。

## 待复核

- [ ] checkout + Pages 上传的实际耗时分布(workflow 无计时输出;UNVERIFIED)
- [x] ~~会不会自动提交 README~~ → 不会,见上
