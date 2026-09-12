# readme-pipeline · README 生成

> 状态:**0001 已复核**(生成归属发生本专题立项以来最大变更:README 不再随 PR 提交,改由 main 合并后 bot 重生成;generate-readme.mjs 210→215 行,其余函数未动)。最近核验:`38976afd`,2026-09-12。

## 定位

根目录双语 README(各 3742 行,2026-09-12 实测)是 `data/plugins/*.yml` 的**投影**:marker 块(`<!-- BEGIN TOC -->…<!-- END TOC -->`、`<!-- BEGIN PLUGINS -->…<!-- END PLUGINS -->`)内由脚本再生,块外(badges、banner、intro、Contributing/Badge/Disclaimer)永远手工维护。

**0001 重构(核心变更)**:投稿改为 **yml-only**——"That one file is the whole submission"(contributing.md:22)。投稿者**不再需要**跑 `generate-readme`(也不再提交 README);PR 合并后由新增的 `.github/workflows/sync-readme.yml` 在 main 上重生成并以 bot 身份提交(`permissions: contents: write`,git push)。pr-check 的 `--check` 语义收窄:**仅当 PR 自己手改了 README 才要求与 yml 匹配**(:133-137);yml-only PR(新常态)由 runner 现场重新生成以保持树一致(:123-126)。动机:要求 PR 内 regenerate 曾使同分类的提交永远互相冲突——8-30 当天 296 个 open PR 里 218 个卡在生成行上,"none of them over anything a human had written"。

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

**已知未守卫点(0001 更新)**:.github/pull_request_template.md 的 category 列表这次**被人工同步到了 23 项**(含 wsl)——但它仍不在任何脚本看守范围内,与 contributing.md 的同步靠人记得。这个仓库的一致性哲学不变:**能被脚本看守的都被看守了;看不了的靠注释承认人工性**(build-site "2,143 entries" 等过期注释仍在,见各专题)。

## sync-readme.yml:bot 重生成(0001 新增,精读)

- **写权限的口子**:注释明说 "Unlike build-site.yml, this one DOES write to the repository — that is its entire job",刻意独立成窄权限 workflow,保住 "the build never writes" 在 build 侧为真。
- **排队不取消**:`concurrency: { group: sync-readme, cancel-in-progress: false }`——两个 merge 都会触发重生成,取消会让 main 留着 stale README 等下一次 merge 才修复,所以排队。
- **bot guard**:`if: github.actor != 'github-actions[bot]'`——bot 自己的提交会再触发一次 push,第二次运行 diff 为空即 exit 0,终止性靠 generate-readme 的确定性。
- **added-date 语义转移**(workflow 注释里自己交代了):新条目 README 行的"首个 added commit"现在是这个 bot commit 而非 merge commit——同日秒差,但读 build-site 日期推导的人要知道每个近期日期都指向 bot commit。

## 正文

- [01 · generate-readme 逐段机制](./01-generate-readme.md)
