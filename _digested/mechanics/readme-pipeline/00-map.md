# readme-pipeline · README 生成

> 状态:**进行中**(generate-readme.mjs 已逐行核验;边车数据与站点侧联动见姊妹专题)。最近核验:`5e7dc7eb`,2026-08-27。

## 定位

根目录双语 README 各约 600KB(2469 行),是 `data/plugins/*.yml` 的**投影**:marker 块(`<!-- BEGIN TOC -->…<!-- END TOC -->`、`<!-- BEGIN PLUGINS -->…<!-- END PLUGINS -->`)内由脚本再生,块外(badges、banner、intro、Contributing/Badge/Disclaimer)永远手工维护——`npm ci && node scripts/generate-readme.mjs` 是投稿者本地要跑的全部(:22-27 contributing.md)。CI 用 `--check` 模式验证同步(pr-check.yml:65)。

## 本专题的三个核心机制

1. **模板替换 + 全文集合校验**(双层):只保证 marker 块内的正确性是不够的——PR 可以在 `<!-- END PLUGINS -->` 之后再塞一个 `### UI Enhancements` 标题和几行条目,站点解析器(按标题正则切片)会照单全收而 YAML 无从对应。所以 generate-readme 有 `parsedUrls()`:把**整个文件**当站点会读的样子再解析一遍,URL 集合必须与 data/plugins 声明完全一致(generate-readme.mjs:59-79, :166-174)。"smuggled" 与 "missing" 都是失败。
2. **锚点算法复刻**:GitHub heading anchor 的实现逐字重写并注释两个「像 typo 但不是」的结果("Themes & Appearance"→`themes--appearance`;emoji 被删但它的空格留下 → `-ui-增强`)。TOC 与章节互链的正确性建立在这份复刻上。
3. **描述文本是贡献者散文,必须先防御 Markdown**:描述里 `[Shot N HH:mm]` 这类方括号会被 remark 当 link reference,让 awesome-lint 以 "expected corresponding definition" 全文爆红——作者无从知道为什么。escapeRefs 只在真正会成为 reference 的位置转义开括号,跳过 code span(那里反斜杠会渲染出来)与已有 inline link;注释声明对当时全部 4279 条描述验证为 no-op(此数字与当前条目数的差异待考,见下)。

## 双语配对是怎么被强制执行的

| 层 | 机制 | 出处 |
|----|------|------|
| 数据层 | validateEntries:description.en 必填单行;zh 可省但存在即非空非换行;未知 locale 拒绝 | lib/entries.mjs |
| 生成层 | 缺译不阻塞——zh 渲染英文原文并汇报清单("an honest gap a maintainer closes later") | generate-readme.mjs:140-143 |
| 站点层 | parity 五检(分隔符/互相缺失/分类一致)| build-site.mjs:56-117 |
| 守卫层 | contributing.md 的 category 清单由生成器核对(CAT_IDS 拼串比对,漂移过一次后改为脚本看守)| generate-readme.mjs:203-210 |

**已知未守卫点**:.github/pull_request_template.md 勾选框里的 category 列表仍是旧的 12 项(现为 22 项)——它不在任何脚本的看守范围内。同类问题还散布在注释里的过期数字(build-site "2,143 entries"、build-site.mjs:9 过期职责声明、probe-npm 头注释的 30 天)。这个仓库的一致性哲学是:**能被脚本看守的都被看守了;看不了的靠注释承认人工性。**

## 正文

- [01 · generate-readme 逐段机制](./01-generate-readme.md)
