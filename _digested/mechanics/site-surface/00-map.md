# site-surface · 站点

> 状态:**0003 已复核**(基线 `upstream@4693e5a83`,2026-10-11)。在 0002 既有能力披露/下载窗口/site-health 等机制之上,0003 将首页/分类页卡片改为 24 张 SSR 回退 + JSON catalog + 客户端虚拟列表;`site/` 不再是零 diff。最近核验:`4693e5a83`。

## 定位

`site/` + `scripts/build-site.mjs` 是注册表的第二个发布面:从同一份名单长出约 **9000+ 个 HTML 页面**(4489 条目 ×2 语言详情页 + 每 locale 的首页/23 分类页/隐私页;按构建逻辑推算,非构建日志读数)+ 7 个全站数据产物,并额外为首页与各有条目的分类页生成语言/分类专属 `catalog.json`;共最多 **48 个 catalog 文件**(每语言 1 首页 + 23 个分类页,当前 23 类均有条目)。静态 HTML 与 JSON 部署到 GitHub Pages(`site/assets/CNAME` = awesome-dsh-plugin.com),前端由 Cloudflare 加速。首页/分类页只 SSR 下载排名前 24 张卡;JavaScript 加载 catalog 后按视口窗口化渲染全量列表,失败则退回这 24 张,`<noscript>` 明示仅有首屏内容。catalog URL 带内容 hash query 防 CDN 旧缓存。统计(Cloudflare Web Analytics)无 cookie,但站点**有条件地**携带两个第三方:Google AdSense(构建变量 `ADSENSE_CLIENT` 设定时进入每个首页/分类/详情页,隐私页除外,当前变量未设=字节级无广告)与 Giscus 评论(仅当访客把评论面板滚到视口附近)。

0002 新增一条与"发布面"并列的**监督面**:`.github/workflows/site-health.yml` + `scripts/check-site-health.mjs`(152 行)每天 07:23 拉取**线上**首页,数 `/p/` 链接,与 `data/plugins/` 的条目数比对,落后超过 tolerance(默认 300)即失败。注释交代了动机:dshmarket.com 曾在 2026-09-09 → 09-25 **静默冻结 18 天**(3,363 页对 4,347 条,1,082 个插件根本没有页面)而仓库里毫无痕迹。它刻意**不**与已发布的 catalog 比对——"页与 catalog 出自同一次构建,拿站点比自己的 catalog 等于比自己"。取数失败一律 exit 1(检查不了 ≠ 全好)。

## 本专题最重要的一个架构事实

**build-site 的花名册来源是 README,不是 YAML;但 README 本身已降级为生成物。** 它逐行正则解析两份 README 得到条目集合(build-site.mjs:99 附近),YAML 只在 tarball 映射一处被读。0001 起投稿改为 **yml-only**(#3832/#4004):人工编辑点只有 data/plugins/*.yml;README 由 sync-readme.yml 在 merge 后由 bot 于 main 上重生成并提交(sync-readme.yml:32-33,`contents: write`——全仓库唯一向 main 写入的 workflow,0002 复核仍成立)。pr-check 的 `generate-readme --check` 守卫仍在但语义收窄:**只拦截"PR 自己手改 README 且与 yml 不符"**(pr-check.yml:171-210);yml-only PR(现在的常态)不经过它。完整因果链变为:

```text
data/plugins/*.yml ──(PR, yml-only)──▶ merge ──sync-readme.yml bot commit──▶ README.md/README.zh.md ──parseReadme──▶ site/docs/*
   (唯一人工编辑点)                                    (bot 生成的中间投影)                    (生成物 ×2:页面+数据)
```

0002 补上这条链上刚被发现的**断点**:bot 用默认 GITHUB_TOKEN 提交不会触发 `push`,所以站点会永远慢一个 merge(2026-09-20 实测 main 4,014 条、已发布 4,012,且 bot 那个 sha 上根本没有 build-site 运行)。修法是 build-site 增加 `workflow_run` 触发(build-site.yml:26-28),而不是让 bot 去 dispatch。同一次修复把探针开关从"排除 push"改成**事件白名单**(build-site.yml:158-171):旧写法让每次 sync-readme 完成都跑全量探针,2026-09-22 有一次在这一步坐了 40 分钟(纯部署构建约 12 分钟)。

一份数据、两次投影仍在,但第二次投影的守卫从"PR 时强制同步"变为"main 上确定性再生 + PR 侧仅防手改(+ 0002 起按线上字节兜底)"。docs 侧守卫不变(bilingual parity 五检 + 截图 host 白名单);「跳过 YAML 直接造数据」仍会被拦,「手编 README」则从"被拦"变为"被 sync-readme 的重生成覆盖"。

## 正文

- [01 · build-site 主干与部署链](./01-build-site.md)
- [02 · 模板契约与 locales 体系](./02-templates-locales.md)

## 待回答的问题

- [x] 详情页一插件一 HTML 还是 SPA → 每插件每语言一个静态 index.html(docs/p/{slug}/、docs/zh/p/{slug}/),模板见 [02](./02-templates-locales.md)
- [x] locales 支持几种语言 → 仅 en/zh;首元素为 default(x-default,serve at `/`)
- [x] build-site 在 CI 哪一步、产物推到哪 → 见 [01](./01-build-site.md) §部署链
- [ ] 第三种语言的最小接入成本(0001 后至少动五处:locales.mjs 含 `giscusLang`、TOC_SHELL、privacy.<code>.html、banner/og 两图,评估待做)
- [ ] **0002 新增**:`check-site-health.mjs` 的 tolerance=300 是否够兜住"catalog 日增 62.5 条、峰值 205 条"(注释给的实测),以及它能否认出"页面在、内容冻结"这种半冻结(现在只数链接数)
- [ ] **0003 新增**:site-health 目前只核线上 `/p/` 链接数,是否需要对 locale/category `catalog.json` 做完整性检查——catalog 缺失时单页仍可成功发布,但浏览器只剩 24 张回退卡
