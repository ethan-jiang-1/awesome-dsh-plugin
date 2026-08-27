# registry-data · 数据模型

> 状态:**骨架,未消化。** 本页目前只划范围、列阅读入口,不承诺任何已验证结论。

## 定位

`data/` 是整个仓库的唯一事实源。摸清它,后续 README / 站点 / 门禁的一切行为才有依据。

## 范围承诺

- `data/plugins/*.yaml`:逐条插件的 schema(必填/可选字段、命名规则、約 2288 个文件的组织方式)
- `data/added-dates.json`、`downloads.json`、`screenshots.json`、`stars.json`:四个边车各记录什么、key 结构、由谁写入
- `scripts/migrate-to-yaml.mjs`、`scripts/reorder-categories.py`:历史数据是怎么变成现在这副样子的
- `scripts/lib/entries.mjs`:数据在脚本侧的统一加载形态

## 待回答的问题

- [ ] YAML 里 category 怎么表达?分类清单定义在哪一处?
- [ ] 边车 JSON 的 key 是 plugin 名还是 repo 全名?与 YAML 如何 join?
- [ ] 一条 PR 只加一个 `data/plugins/<name>.yaml`,文件名与 package name 的约束是什么?
- [ ] npm 包名(`@scope/dsh-xxx`)与 GitHub repo 的对应关系存在哪个字段?

## 阅读入口

- `scripts/lib/entries.mjs`(统一加载)
- 任意 2–3 个有代表性的 `data/plugins/*.yaml`(新条目 + 有 screenshots 的老条目)
- `.github/workflows/pr-check.yml`(schema 校验发生在哪一步)

编号正文规范:`01-yaml-schema.md` 起按问题编号。
