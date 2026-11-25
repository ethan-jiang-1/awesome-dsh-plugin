# 02 · 模板契约与 locales 体系

> 基线:`upstream@8f1a1800e`(2026-11-25,0007 复核)。**0007 的 `site/` 变更只有一个文件、两行**:`locales.mjs:33-34` 的英文 `TITLE`/`DESC` 换词(`TITLE` → "Awesome DSH Plugin — Curated List of DSH Plugins for DeepSeek Harness",`DESC` → "A curated list of {N} DSH plugins for DeepSeek Harness (dsh): …")。**结构零变化**:两语言 `strings` 仍各 64 条、分类仍 23 个,`template.html`(879 行)、`detail-template.html`(334 行,**32 个 token**)、`privacy-template.html` / `privacy.en.html` / `privacy.zh.html`、`comments.mjs`、`ads.txt` 与静态资源全部未动;`git diff --stat 29b3ed46e 8f1a1800e -- site/` 只有 `site/locales.mjs` 一个文件(+2/−2)。0006 是 `site/` 整目录零 diff,当时的连带变化只有 href 取值改走 `slugHref()`(机制见 [00](./00-map.md) 与 [01](./01-build-site.md));0004 的"索引源"一行与两条 `INDEX_*` 仍是最近一次**结构**改动;0003 的 24 卡 SSR + catalog 虚拟列表仍是当前形态。最近核验:`8f1a1800e`。

## locales.mjs:唯二语言的注册表

- 结构三层:顶层标量(URL 路径、文件指针、SEO 标题模板 `{N}{CAT}{TOP}{NAME}` 占位、`giscusLang`)、`categories`(23 id→译名,含 wsl: 'WSL & Windows Interop'/'WSL 与 Windows 互操作',:73/:198)+ `strings`(**64** 个 UI 短语;0003 加 `NOJS`,0004 加 `INDEX_LEAD`/`INDEX_COPY`;英文 :88-156、中文 :213-278,`NOJS` 分别在 :96/:221,`INDEX_LEAD`/`INDEX_COPY` 在 :110-111 与 :235-236)。**0007 没有增删任何键**,只改了英文段两行的值(:33-34)。
- **0007 的文案变化是"英文 SEO 面"而不是"本地化"**:旧 `TITLE` 是 "Awesome DSH Plugin — Curated DeepSeek Harness (dsh) Plugin List",新句把 "DSH Plugins" 提到前面;旧 `DESC` 以 "DeepSeek Harness (dsh) plugins" 起句,新句改成 "{N} DSH plugins for DeepSeek Harness (dsh)"。中文 `TITLE`(:176)/`DESC`(:177)一字未动,所以两语言首页的 `<title>` 与 meta description 从这一轮起**不再对称**(中文仍是"插件精选列表");这是上游按英文搜索词做的取舍(提交信息自述该词 1,092 曝光、position 5.9,本轮未复核第三方数据),修不修是产品判断,不是 bug。
- **不是与 README 无关的第二体系**:locales.mjs 同时是 generate-readme 与 build-site 的输入(import LOCALES);两工具共享 `loc.readme / categories / sep`。但翻译版标题的 emoji 前缀不在 locales 里——`CAT_EMOJI` 硬编码在 lib/entries.mjs(generate-readme 用),`TOC_SHELL` 在 generate-readme.mjs(每种 locale 一份 TOC 外壳,缺失即 exit 1)。**加第三种语言至少动五处**:locales.mjs(新条目必须带 `giscusLang`,否则评论 lang 为 undefined)、generate-readme 的 TOC_SHELL、site/privacy.<code>.html、assets 里 banner/og 双图。
- 与其手工同步的副本:`entries.mjs` 的 `LOCALE_CODES`(:20)/`BASE_LOCALE`(:21)(注释自认 "in sync with site/locales.mjs",无代码强制)。
- 0004 的两条 `INDEX_*` 只经模板的 `__T_*` 替换,**不进 catalog JSON**——它们只出现在服务端渲染的那一行里。四处替换循环当前行号:首页 :729、分类页 :786、隐私页 :826、详情页 :1075,形态都是 `for (const [k, v] of Object.entries(loc.strings)) page = page.replaceAll('__T_' + k + '__', …)`。0007 改的是 `loc.TITLE`/`loc.DESC` 的值,而这两个走的是 `__TITLE__`/`__DESC__` 的**具名**替换(首页 :706-707,`__DESC__` 还额外 `.replace('{N}', N)`),不是 `__T_*` 通配,所以文案变化不经这条循环——这也是"只改两行值、不新增键"能生效的原因。
- dead strings:`FULLLIST`(:93/:218)、`MARKET_LINK`(:119/:244)、`MENU_CLI_HINT`(:126/:251)无任何消费者(可证:三个键在 `site/` 与 `scripts/` 里除定义处各出现两次——en 一次、zh 一次——没有第三处引用)。

## template.html(879 行)vs detail-template.html(334 行)

| | 首页/分类页模板 | 详情页模板 |
|---|---|---|
| 交互脚本 | ~498 行:搜索/筛选/排序/URL 状态同步、catalog 拉取、虚拟窗口渲染(:379-876;180ms 搜索防抖);先显示 24 张烘焙卡,成功后仅挂载视口附近行(+3 行 overscan) | ~75 行:复制按钮反馈 + **Giscus 懒加载器**(:248-330,IntersectionObserver 400px 触发才注入 script;不滚动=不联系第三方) |
| 数据嵌入 | HTML 只预渲染前 24 张 `<li>`;完整首页或分类列表经 JSON catalog 载入,JS 从数据构造 DOM、按视口窗口化。catalog 失败/渲染异常时 `.legacy` 对已烘焙卡片筛排,不等于完整名单 | 全静态文本 |
| SEO | ItemList JSON-LD 先放 `{}` 占位、构建时整体替换 | 直接放 `__JSONLD__` |
| 特有 | hero 动效、搜索栏、market CTA、**索引源一行(0004)**、chips/filters、install 下拉(details 元素)、back-to-top(scrollY>600) | breadcrumbs、specs 五段(缺项整段省略)、相关插件(同分类按 stars 前 6)、README panel |

- **排序比较器双份互锁**:服务端 `byDownloads`(`build-site.mjs:523-528`)与客户端 catalog 模式下的 `SORTS.dl`(`site/template.html:470-480`)必须等价否则首屏顺序改变(源码注释自己点名了这条约束)。"近 7 天"过滤器 cutoff 注释里的旧条目数仍是过期数字。首屏 SSR 仅按下载排序取前 24 项;完整排序在 client catalog 上执行。
- **卡片只显示一条安装命令,详情页列三条(0004;0007 给 tarball 档补 `-w`)**:`cardCmd()`(`build-site.mjs:543-545`)按 npm > 作者声明的 tarball > git 取值,与详情页 `cmds`(:949-953)的顺序、以及 `plugins.json.install`(:1176)一致;0003 时无 npm 的条目直接落到 `github:` 源,丢掉作者声明的 Release 包(#7752)。0007 起 tarball 字符串由 `releaseTarballCmd()`(:449-452)产出,形如 `dsh plugin --profile web add -w "<tarball>"`。模板本身**没有因此改动一行**——变的只是填充进去的字符串,所以 token 契约不变。SSR 卡与 catalog 共用这一个函数,首屏与虚拟列表不会分叉。
- 复制按钮反馈超时四处不一致(1500/900/1200ms + 评论状态 2500ms 自清);detail 页反馈是裸 '✓' 而 index 页走 locale 字符串(小不一致)。0004 的索引行按钮进的是同一条 1200ms 路径(`e.target.closest('.cli .copy, .market .go, .indexline .copy')`,:548),并复用 `#live` 的 1500ms 播报(:535)。
- **CSS :root 变量块在三个模板各完整复制一份**,都有 "keep in sync" 注释——改主题色要改三处。

## detail-template.html 占位符契约

**32 个 token**(0002 勘误;0001 误记 30;**0007 复核仍是 32**,模板文件 334 行,与 0006 逐字节相同),填充链 `build-site.mjs:1040-1075`(`__P_COMMENTS_SECTION__` :1043、`AD_HEAD_TOKEN` :1065、`__P_INSTALL__` :1071),要点:

- `__P_README_SECTION__`:整段 section 或空串,内部由 renderReadme 产物组装(渲染器 :846);
- `__TITLE__/__DESC__/__URL__/__HREFLANGS__/__OG_IMAGE__`:SEO 面;`__TITLE__` 不直填——复合名按 e.name → short → '#' 后裸包名逐级回退取 ≤65 字符(:1051-1055);`__DESC__` 先对 <60 字符的短描述用 `P_META_SHORT` 包裹再走 155 截断(:929-935;`clampMeta` 本体 :917-925);长描述在前 152 字符找 `. 。 ; ;` 边界(需 >90),退空格边界,再退硬切加 `…`;
- `__P_INSTALL__`:安装命令**三条都列**——npm、声明式 tarball(0007 起带 `-w`)、git(`cmds` :949-953),缺项跳过,不是只取一条;
- `__JSONLD__`:SoftwareApplication(applicationCategory DeveloperApplication,sameAs:[github,(npm)])+ BreadcrumbList;
- 所有机器标识(H1/specrow 数字/命令 pre)标 `translate="no"`。

**0002/0004 未动但要注意**:模板里**没有**能力披露相关 token,`plugins.json` 的 capabilities/capabilityRedLines/capabilityCheckedAt 不在本站页面上出现——消费方是 dsh-market。0004 同理:**模板里也没有 `icon` token**,`data/plugins/*.yml` 的 `icon` 只进 `plugins.json`(build-site.mjs:1180),站点仍用站点自己的 `logo.svg` favicon,门店图与作者头像回退都发生在 dsh-market 一侧。`icon` 的准入规则(https、GitHub 图床、位图扩展名)写在 `lib/entries.mjs` 的 `validateEntries` 里,实际由 `generate-readme.mjs:95` 调用(PR 门禁走的正是这条),build 只透传字段。**0007 又添一例同类事实**:`docs/release-history/` 的分片树在 `site/` 里**零引用**(`grep -rn 'releaseHistory\|release-history' site/` 无命中)——它是纯数据产物,首页/分类页/详情页都不渲染 release 历史,模板因此一个 token 都没多。

三个模板尾部都直连 Cloudflare Web Analytics beacon(token 明文硬编码),与隐私页 **Analytics 一节**的 "cookie-less" 表述一致;但隐私页整体已不再宣称零第三方(广告 cookie + 按需评论)。另:三模板的 Archivo Fallback 度量匹配字体(size-adjust:111.1% 等,修 Windows Segoe UI 回退重排 CLS,#4422)——仍是本地字体,不违背"无第三方 webfont"。

## 隐私页的三文件法

`privacy-template.html`(127 行)+ `privacy.en.html` / `privacy.zh.html`(正文片段)。正文是 prose 不是 UI strings 所以不进 locales.mjs;但 registry 声明 `privacyBody` 路径——新增语言漏写正文会 exit(1) 而非悄悄发英文版(build-site.mjs:806-808)。sitemap 对隐私页 lastmod 取源文件最后 commit 日期,为的是不稀释爬虫对全站 lastmod 的信任。

**内容重写(2026-08-30,0001 已记)**:短版本从 "no cookies…no third party" 改为 "counts views…carries Google ads, which do use cookies",新增 Advertising(AdSense:cookie + IP,#advertising 锚点)与 Community comments(Giscus,"不滚动到评论区就不发请求")两节——**引用隐私页旧文案("本站不设任何 cookie""没有广告网络")的笔记表述全部作废**。

## 0003 列表 catalog 机制

- 构建在首页旁输出 `catalog.json`(全 locale 条目),在每个非空分类页旁输出仅该类的 `catalog.json`;序列化数据包含卡片需要的 locale 文案、分类、下载/星数/日期、名称/owner/slug、描述、安装命令与详情 href。HTML 的 `data-catalog` 与 preload 均指向加 `?v=<SHA-256前8位>` 的版本化 URL,避免边缘缓存跨构建复用旧 JSON。
- HTML 默认只有 24 卡,`<noscript>` 明示只显示首屏;catalog 成功则重建完整可筛选列表,按视口与滚动窗口只挂载可见项。fetch/校验/构造任一失败则 `.legacy` 回退,对 24 张 SSR 卡继续筛选与排序。此路径优先保证可用与轻量,但失败会把可浏览范围降到 24 条。
- `locales.mjs` 每种语言新加一条 `NOJS` 短语;其它交互按钮文案随 catalog JSON 传递,避免在脚本字面量插值时被引号打断。0004 未改 catalog 结构,只有卡片 `cmd` 随 `cardCmd()` 一起变(两处仍出自同一函数)——**0007 也是同一形态**:catalog 的 `cmd` 字段随 tarball 字符串带上 `-w`,JSON 结构、加载与回退逻辑、`?v=` 版本化都没变。

## 待复核

- [ ] 404.html 是独立静态 SPA(中英返回链接),与「无 JS 回退」策略的关系待读
- [ ] assets 中 banner/og 的生成方式(是否有脚本或纯人工导出)
- [x] 0004:分类页确实把字面 `__INDEX_LINE__` 印在搜索条下——首页循环替换它(build-site.mjs:725),分类页循环(:745-802)没有对应 `replaceAll`;2026-10-24 抓 `https://awesome-dsh-plugin.com/tools/` 已在线上确认,首页无此字面。**0007 复核仍未修**
- [ ] 0004:`INDEX_*` 两句文案只给 jsDelivr 一个地址;README 的开场块是"给出 jsDelivr 地址 + 说明 Pages 版与其镜像是 canonical mirror"的写法——站点要不要也给出 Pages 版,未定
- [ ] **0007 新增**:英文 `TITLE`/`DESC` 换词对 SERP 的实际影响无法本地评估(提交信息给的曝光/排名是上游自述,未复核);中文两行未跟随,是否要统一措辞是产品决定
- [ ] **0007 新增**:release 历史只有数据面、没有 UI——站点无任何入口浏览 `docs/release-history/`,消费方只能靠 `docs/updates.json` 的 `releaseHistory: true` 自行拼路径。若将来要在详情页加"更新历史"面板,至少需要新 token + 客户端 fetch + 按 `complete` 决定是否续拉,本轮没有做
- [ ] **0007 新增**:`site/detail-template.html` 的 32 个 token 与填充链本轮零 diff,但本轮没有任何测试或 `--check` 验证"模板 token 集合 == build-site 的 replaceAll 集合"——加 token 漏替换仍只能靠人工或构建时的字面残留发现
