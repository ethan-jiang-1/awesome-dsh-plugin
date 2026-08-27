# site-surface · 站点

> 状态:**初稿完成**(build-site.mjs 942 行 + 模板 + locales + 部署链已逐行消化;行号来自 `main@5e7dc7eb` 工作区)。

## 定位

`site/` + `scripts/build-site.mjs` 是注册表的第二个发布面:从同一份名单长出约 **4622 个 HTML 页面**(2286 详情页 ×2 语言 + 首页/分类页/隐私页)+ 5 个数据产物,部署到 GitHub Pages(`site/assets/CNAME` = awesome-dsh-plugin.com),前端由 Cloudflare 加速并做无 cookie 统计。

## 本专题最重要的一个架构事实

**build-site 的花名册来源是 README,不是 YAML。** 它逐行正则解析两份 README 得到条目集合(build-site.mjs:62-67),YAML 只在 tarball 映射一处被读(:39-49)。"README 必须是 YAML 的忠实投影"这件事不由 build-site 保证,而由 pr-check 的 `generate-readme --check` 保证(pr-check.yml:65)。所以完整因果链是:

```text
data/plugins/*.yml ──generate-readme──▶ README.md / README.zh.md ──parseReadme──▶ site/docs/*
        (唯一人工编辑点)              (强制同步的中间投影)         (生成物 ×2:页面+数据)
```

一份数据、两次投影,每次投影都有自己的守卫(README 侧:marker 块内替换 + 全文 URL 集合校验;docs 侧:bilingual parity 五检 + 截图 host 白名单)。「手编 README」或「跳过 YAML 直接造数据」都会被某道守卫拦下。

## 正文

- [01 · build-site 主干与部署链](./01-build-site.md)
- [02 · 模板契约与 locales 体系](./02-templates-locales.md)

## 待回答的问题

- [x] 详情页一插件一 HTML 还是 SPA → 每插件每语言一个静态 index.html(docs/p/{slug}/、docs/zh/p/{slug}/),模板见 [02](./02-templates-locales.md)
- [x] locales 支持几种语言 → 仅 en/zh;首元素为 default(x-default,serve at `/`)
- [x] build-site 在 CI 哪一步、产物推到哪 → 见 [01](./01-build-site.md) §部署链
- [ ] 第三种语言的最小接入成本(需动 locales.mjs + generate-readme TOC_SHELL + privacy.<code>.html + banner/og 两图,评估待做)
