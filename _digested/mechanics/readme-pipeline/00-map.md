# readme-pipeline · README 生成

> 状态:**0002 已复核**。本窗口 `generate-readme.mjs` **零 diff**(仍 215 行)——README 投影逻辑没动;**变的是"什么时候、以哪个 sha 来重生成"**:sync-readme.yml 从 69 行扩到 **106 行**,加了 `ref: main` 检出与三轮 fetch/reset/regenerate/push 重试。最近核验:`c18ba4a0d`,2026-09-30。(0001 曾记本专题立项以来最大变更:README 不再随 PR 提交,改由 main 合并后 bot 重生成。)

## 定位

根目录双语 README(**4579 / 4578 行**,2026-09-30 实测;0001 时为各 3742 行)是 `data/plugins/*.yml` 的**投影**:marker 块(`<!-- BEGIN TOC -->…<!-- END TOC -->`、`<!-- BEGIN PLUGINS -->…<!-- END PLUGINS -->`)内由脚本再生,块外(badges、banner、intro、Contributing/Badge/Disclaimer)永远手工维护。

**0001 重构(仍生效)**:投稿改为 **yml-only**——"That one file is the whole submission"(contributing.md:22)。投稿者**不再需要**跑 `generate-readme`(也不再提交 README);PR 合并后由 `.github/workflows/sync-readme.yml` 在 main 上重生成并以 bot 身份提交(`permissions: contents: write`,sync-readme.yml:32-33)。pr-check 的 `--check` 语义收窄:**仅当 PR 自己手改了 README 才要求与 yml 匹配**(pr-check.yml:171-210;0002 起判定对象从 merge ref 改为 PR head,见 [submission-gates/01](../submission-gates/01-pr-check-and-guard.md));yml-only PR(新常态)由 runner 现场重新生成以保持树一致。动机:要求 PR 内 regenerate 曾使同分类的提交永远互相冲突——8-30 当天 296 个 open PR 里 218 个卡在生成行上,"none of them over anything a human had written"。

## 本专题的三个核心机制

1. **模板替换 + 全文集合校验**(双层):只保证 marker 块内的正确性是不够的——PR 可以在 `<!-- END PLUGINS -->` 之后再塞一个 `### UI Enhancements` 标题和几行条目,站点解析器(按标题正则切片)会照单全收而 YAML 无从对应。所以 generate-readme 有 `parsedUrls()`:把**整个文件**当站点会读的样子再解析一遍,URL 集合必须与 data/plugins 声明完全一致(generate-readme.mjs:59-79, :166-174)。"smuggled" 与 "missing" 都是失败。
2. **锚点算法复刻**:GitHub heading anchor 的实现逐字重写并注释两个「像 typo 但不是」的结果("Themes & Appearance"→`themes--appearance`;emoji 被删但它的空格留下 → `-ui-增强`)。TOC 与章节互链的正确性建立在这份复刻上。
3. **描述文本是贡献者散文,必须先防御 Markdown**:描述里 `[Shot N HH:mm]` 这类方括号会被 remark 当 link reference,让 awesome-lint 以 "expected corresponding definition" 全文爆红——作者无从知道为什么。escapeRefs 只在真正会成为 reference 的位置转义开括号,跳过 code span(那里反斜杠会渲染出来)与已有 inline link;注释声明对当时全部 4279 条描述验证为 no-op。

## 双语配对是怎么被强制执行的

| 层 | 机制 | 出处 |
|----|------|------|
| 数据层 | validateEntries:description.en 必填单行;zh 可省但存在即非空非换行;未知 locale 拒绝 | lib/entries.mjs |
| 生成层 | 缺译不阻塞——zh 渲染英文原文并汇报清单("an honest gap a maintainer closes later") | generate-readme.mjs:140-143 |
| 站点层 | parity 五检(分隔符/互相缺失/分类一致)| build-site.mjs:99-160 |
| 守卫层 | contributing.md 的 category 清单由生成器核对(CAT_IDS 拼串比对,漂移过一次后改为脚本看守)| generate-readme.mjs:203-210 |

**已知未守卫点(0002 复核不变)**:`.github/pull_request_template.md` 的 category 列表仍是人工同步的 23 项,不在任何脚本看守范围内。这个仓库的一致性哲学不变:**能被脚本看守的都被看守了;看不了的靠注释承认人工性**。

## sync-readme.yml:bot 重生成(0001 新增,0002 加固)

- **写权限的口子**:注释明说 "Unlike build-site.yml, this one DOES write to the repository — that is its entire job",刻意独立成窄权限 workflow,保住 "the build never writes" 在 build 侧为真。0002 复核:**它仍是全仓库唯一 `contents: write` 的 workflow**。
- **排队不取消**:`concurrency: { group: sync-readme, cancel-in-progress: false }`——两个 merge 都会触发重生成,取消会让 main 留着 stale README 等下一次 merge 才修复,所以排队。
- **0002 修的三件事**:
  1. **检出 `ref: main`**(:57-59):"a queued run still holds the sha it was triggered on, which by then is an ancestor of main"——排队等到的运行手里那个 sha 早就不是 main 了。
  2. **三轮重试循环**(:74-96):`git fetch origin main` → `git reset --hard origin/main` → 重新生成 → 有 diff 才提交 → push;push 被拒说明 main 又动了,就在新的 tip 上重做。
  3. **三轮都输就显式红**(:98-106):`::error::` + exit 1,不再静默留下过期 README。动机是实测事故:2026-09-19 README 陈旧了**八小时**("Eight hours of that on 2026-09-19 is why this loop exists"),注释也顺势改成 "Queueing alone is not enough"。
- **bot guard**:`if: github.actor != 'github-actions[bot]'`——bot 自己的提交会再触发一次 push,第二次运行 diff 为空即 exit 0,终止性靠 generate-readme 的确定性。
- **added-date 语义转移**(workflow 注释里自己交代了):新条目 README 行的"首个 added commit"现在是这个 bot commit 而非 merge commit——同日秒差,0002 新增的 yml 账本(`lib/added-dates.mjs`)正是为了在有改写/迁移时给回一个可信日期,见 [site-surface/01 §阶段流水](../site-surface/01-build-site.md)。

## 正文

- [01 · generate-readme 逐段机制](./01-generate-readme.md)
