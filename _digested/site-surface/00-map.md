# site-surface · 站点

> 状态:**骨架,未消化。** 本页目前只划范围、列阅读入口,不承诺任何已验证结论。

## 定位

`site/` 是注册表的第二个发布面:同一份 `data/plugins` 数据长出详情页。搞清它和 README 共享多少管线、差异部分在哪。

## 范围承诺

- `site/template.html`、`site/detail-template.html`:页面骨架与占位符约定
- `site/locales.mjs`:站点级 i18n 的组织方式,与双语 README 的关系
- `scripts/build-site.mjs`:构建输入输出、部署目标(packages.json 提到 awesome-dsh-plugin.com)
- `site/assets/`、`privacy.*.html`:静态资产与法务页的来源
- `prune-legacy-screenshots.mjs` 与站点的关联

## 待回答的问题

- [ ] 详情页一插件一 HTML 还是 SPA?路由怎么定?
- [ ] locales.mjs 支持几种语言?和 README.zh 的翻译是两套吗?
- [ ] build-site 在 CI 的哪一步跑、产物推到哪里?
- [ ] 探针更新的数据(下载量等)站点直接读 JSON 还是经构建内联?

## 阅读入口

- `scripts/build-site.mjs`
- `site/detail-template.html`
- `.github/workflows/build-site.yml`

编号正文规范:`01-build-site.md` 起。
