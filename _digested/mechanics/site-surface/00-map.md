# site-surface · 站点

> 状态:**0001 已复核**(build-site.mjs 现为 **1098 行**,行号已按 `upstream@38976afd` 刷新;本次核心变更——README 生成归属重构、AdSense、Giscus、并发组拆分——已并入下方架构事实)。

## 定位

`site/` + `scripts/build-site.mjs` 是注册表的第二个发布面:从同一份名单长出约 **7160 个 HTML 页面**(3555 详情页 ×2 语言 + 每 locale 的首页/23 分类页/隐私页)+ 5 个数据产物,部署到 GitHub Pages(`site/assets/CNAME` = awesome-dsh-plugin.com),前端由 Cloudflare 加速;统计(Cloudflare Web Analytics)无 cookie,但站点**有条件地**携带两个第三方:Google AdSense(构建变量 `ADSENSE_CLIENT` 设定时进入每个首页/分类/详情页,隐私页除外,当前变量未设=字节级无广告)与 Giscus 评论(仅当访客把评论面板滚到视口附近)。

## 本专题最重要的一个架构事实

**build-site 的花名册来源是 README,不是 YAML;但 README 本身已降级为生成物。** 它逐行正则解析两份 README 得到条目集合(build-site.mjs:97 附近),YAML 只在 tarball 映射一处被读。0001 起投稿改为 **yml-only**(#3832/#4004):人工编辑点只有 data/plugins/*.yml;README 由新增的 sync-readme.yml 在 merge 后由 bot 于 main 上重生成并提交(sync-readme.yml:69,`contents: write`——全仓库唯一向 main 写入的 workflow)。pr-check 的 `generate-readme --check`(pr-check.yml:129)守卫仍在但语义收窄:**只拦截"PR 自己手改 README 且与 yml 不符"**;yml-only PR(现在的常态)不经过它。完整因果链变为:

```text
data/plugins/*.yml ──(PR, yml-only)──▶ merge ──sync-readme.yml bot commit──▶ README.md/README.zh.md ──parseReadme──▶ site/docs/*
   (唯一人工编辑点)                                    (bot 生成的中间投影)                    (生成物 ×2:页面+数据)
```

一份数据、两次投影仍在,但第二次投影的守卫从"PR 时强制同步"变为"main 上确定性再生 + PR 侧仅防手改"。docs 侧守卫不变(bilingual parity 五检 + 截图 host 白名单);「跳过 YAML 直接造数据」仍会被拦,「手编 README」则从"被拦"变为"被 sync-readme 的重生成覆盖"。

## 正文

- [01 · build-site 主干与部署链](./01-build-site.md)
- [02 · 模板契约与 locales 体系](./02-templates-locales.md)

## 待回答的问题

- [x] 详情页一插件一 HTML 还是 SPA → 每插件每语言一个静态 index.html(docs/p/{slug}/、docs/zh/p/{slug}/),模板见 [02](./02-templates-locales.md)
- [x] locales 支持几种语言 → 仅 en/zh;首元素为 default(x-default,serve at `/`)
- [x] build-site 在 CI 哪一步、产物推到哪 → 见 [01](./01-build-site.md) §部署链
- [ ] 第三种语言的最小接入成本(0001 后至少动五处:locales.mjs 含 `giscusLang`、TOC_SHELL、privacy.<code>.html、banner/og 两图,评估待做)
