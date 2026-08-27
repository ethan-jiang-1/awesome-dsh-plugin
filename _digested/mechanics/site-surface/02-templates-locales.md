# 02 · 模板契约与 locales 体系

> 基线:`main@5e7dc7eb`。

## locales.mjs:唯二语言的注册表

- 结构三层:顶层标量(URL 路径、文件指针、SEO 标题模板 `{N}{CAT}{TOP}{NAME}` 占位)+ `categories`(22 id→译名,同时服务 README 解析/chips/sitemap)+ `strings`(54 个 UI 短语,以 `__T_KEY__` 或代码引用消费)。
- **不是与 README 无关的第二体系**:locales.mjs 同时是 generate-readme 与 build-site 的输入(import LOCALES);两工具共享 `loc.readme / categories / sep`。但翻译版标题的 emoji 前缀不在 locales 里——`CAT_EMOJI` 硬编码在 lib/entries.mjs(generate-readme 用),`TOC_SHELL` 在 generate-readme.mjs(每种 locale 一份 TOC 外壳,缺失即 exit 1)。**加第三种语言至少动四处**:locales.mjs、generate-readme 的 TOC_SHELL、site/privacy.<code>.html、assets 里 banner/og 双图。
- 与其手工同步的副本:`entries.mjs` 的 `LOCALE_CODES/BASE_LOCALE`(注释自认 "in sync with site/locales.mjs",无代码强制)。
- dead strings:`FULLLIST`、`MARKET_LINK`、`MENU_CLI_HINT` 无任何消费者(可证)。

## template.html(500 行)vs detail-template.html(235 行)

| | 首页/分类页模板 | 详情页模板 |
|---|---|---|
| 交互脚本 | ~165 行:搜索/筛选/排序/URL 状态同步(`?cat=&q=&sort=&npm=1&new=1`) | ~11 行:复制按钮反馈 |
| 数据嵌入 | 预渲染卡片 `<li>` 带 dataset(data-cat/data-dl/data-stars/data-added/data-npm),JS 读 dataset 排筛 | 全静态文本 |
| SEO | ItemList JSON-LD 先放 `{}` 占位、构建时整体替换 | 直接放 `__JSONLD__` |
| 特有 | hero 动效、搜索栏、market CTA、chips/filters、install 下拉(details 元素)、back-to-top(scrollY>600) | breadcrumbs、specs 五段(缺项整段省略)、相关插件(同分类按 stars 前 6)、README panel |

- **排序比较器双份互锁**:服务端 byDownloads(null 沉底按 stars 内排;npm 缺席绝不写 `data-dl="0"`)与客户端 SORTS.dl 必须等价否则首屏重排——两处注释互相点名(build-site.mjs:320-323 ↔ template.html:360-363)。「近 7 天」过滤器 cutoff 注释里的 "2,143 entries" 是过期数字。
- 复制按钮反馈三处超时不一致(1500/900/1200ms);detail 页反馈是裸 '✓' 而 index 页走 locale 字符串(小不一致)。
- **CSS :root 变量块在三个模板各完整复制一份**,都有 "keep in sync" 注释——改主题色要改三处。

## detail-template.html 占位符契约

28 个 token,填充点集中在 build-site.mjs:709-734,要点:

- `__P_README_SECTION__`:整段 section 或空串,内部由 renderReadme 产物组装;
- `__TITLE__/__DESC__/__URL__/__HREFLANGS__/__OG_IMAGE__`:SEO 面;meta description ≤155 直用,否则在前 152 字符找 `. 。 ; ;` 边界(需 >90),退空格边界,再退硬切加 `…`;
- `__P_INSTALL__`:安装命令 npm > tarball > git;
- `__JSONLD__`:SoftwareApplication(applicationCategory DeveloperApplication,sameAs:[github,(npm)])+ BreadcrumbList;
- 所有机器标识(H1/specrow 数字/命令 pre)标 `translate="no"`。

三个模板尾部都直连 Cloudflare Web Analytics beacon(token 明文硬编码),与隐私页 "cookie-less analytics" 表述一致。

## 隐私页的三文件法

`privacy-template.html`(壳)+ `privacy.en.html` / `privacy.zh.html`(正文片段)。正文是 prose 不是 UI strings 所以不进 locales.mjs;但 registry 声明 `privacyBody` 路径——新增语言漏写正文会 exit(1) 而非悄悄发英文版(:505-507)。sitemap 对隐私页 lastmod 取源文件最后 commit 日期,为的是不稀释爬虫对全站 lastmod 的信任。

## 待复核

- [ ] 404.html 是独立静态 SPA(中英返回链接),与「无 JS 回退」策略的关系待读
- [ ] assets 中 banner/og 的生成方式(是否有脚本或纯人工导出)
