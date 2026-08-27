# readme-pipeline · README 生成

> 状态:**骨架,未消化。** 本页目前只划范围、列阅读入口,不承诺任何已验证结论。

## 定位

根目录 `README.md` / `README.zh.md` 各 600KB+,不可能手编。这个专题搞清生成器怎么把 `data/plugins/*.yaml` 渲染成中英双语列表,以及双语不一致时谁来拦截。

## 范围承诺

- `scripts/generate-readme.mjs`:渲染流程、分节顺序、条目字段到 Markdown 的映射
- 双语配对机制:两份 README 如何保证同构(en ⇄ zh),漂移如何被发现
- `data/added-dates.json` 在列表里的呈现方式("New" 标记之类,待验证)
- 生成物的 diff 纪律:哪些改动该出现在 PR diff 里,哪些算意外
- 本仓库消化材料本身不用 `README.md` 命名的原因(避免混入生成/校验视野)

## 待回答的问题

- [ ] generate-readme 是幂等重建还是增量改写?会动 README 之外的东西吗?
- [ ] 星标数、下载量这类会过期数字以什么策略进 README,还是根本不进?
- [ ] screenshots.json 与 README 中图片的关系;图片宿主在哪
- [ ] en/zh 两份是同一次运行产出,还是各自模板渲染?

## 阅读入口

- `scripts/generate-readme.mjs`
- `.github/workflows/build-site.yml` 里负责 README 的 step
- 根目录双语 README 的目录结构(只当生成产物读)

编号正文规范:`01-generate-readme.md` 起。
