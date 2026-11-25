# readme-pipeline · README 生成

> 状态:**0007 无对应 diff**(基线 `upstream@8f1a1800e`,2026-11-25):`scripts/generate-readme.mjs` 仍 215 行、**零 diff**;`.github/workflows/sync-readme.yml` 只加 fork 门(+4/−1,112→**115** 行),生成逻辑与触发面未动。README 从 11934/11933 涨到 **13326 / 13325** 行,全部由输入解释(条目 11744→13136),两处 marker 的起始偏移与 0006 相同(TOC 48-75、PLUGINS 起 79)。最近核验:`8f1a1800e`,2026-11-25;上一基线 `29b3ed46e`(2026-11-18)、再上一版 `efe602e7b`(2026-10-31)的结论保留作历史层级。(0001 曾记本专题立项以来最大变更:README 不再随 PR 提交,改由 main 合并后 bot 重生成。)

## 0007 变更

1. **生成器一行未改。** `generate-readme.mjs` 215 行零 diff,本专题的三个核心机制(模板替换 + 全文 URL 集合校验、GitHub 锚点复刻、`escapeRefs`)与双语配对的分工全部原样;本轮也没有给它加测试(13 个 `*.test.mjs` 里没有 generate-readme 的)。
2. **sync-readme 只多了一道 fork 门。** job 的 `if:` 从 `github.actor != 'github-actions[bot]'` 变成加上 `&& (github.repository_owner == 'awesome-dsh-plugin' || github.event_name == 'workflow_dispatch')`(:50-53,+4/−1)。**对本仓的直接影响**:这个 fork 上 bot 不再自动重生成 README——改完 `data/plugins/` 必须手动 `node scripts/generate-readme.mjs`,或 dispatch 一次;同步后看到的 README 是 merge 带进来的。
3. **README 高度仍可反推分母。** 13326 / 13325 行 = **条目数 + 190**:190 = 122 行 marker 与块外手写 chrome + 23 个 `###` 分类标题 + 45 个结构空行;0006 的 11934/11933 @11744 也是同一个 190。en 比 zh 多一行,是文件末尾的空行(en 以 `\n\n` 收尾、zh 以 `\n` 收尾),不在数据里。
4. **分母先对上的一轮。** census 在 13136 条上重跑**一次通过、0 解析失败**(此前六轮都靠修解析器兜底,本轮第一次不需要),所以"README 有多长"这个数这次可以直接对账,不用等解析器补丁。

## 定位

根目录双语 README(**13326 / 13325 行**,2026-11-25 实测;0006 时 11934 / 11933,0005 时 8114 / 8113,0004 时 6894 / 6893,0003 时 4676 / 4675,0001 时为各 3742 行)是 `data/plugins/*.yml` 的**投影**:marker 块(`<!-- BEGIN TOC -->…<!-- END TOC -->`、`<!-- BEGIN PLUGINS -->…<!-- END PLUGINS -->`)内由脚本再生,块外(badges、banner、intro、Contributing/Badge/Disclaimer)永远手工维护。两个 locale 的 marker 落在同一偏移(TOC 48-75、PLUGINS 79-13284,0006 时是 79-11892);PLUGINS 块 **13204 行** = **13136 条条目** + 23 个 `### ` 标题 + **45 个结构空行**,所以"README 有多长"这个数可以直接反推名单规模。**0007 的块外零改动**:635 个 diff hunk 全部落在 PLUGINS 块内(最小旧行 80、最大旧行 11884),前 79 行(到 `<!-- BEGIN PLUGINS -->` 为止,含 TOC)与 `<!-- END PLUGINS -->` 之后的行都与 0006 逐字节相同;0005 时也是这样(前 78 行与 0004 相同),0004 手写加入的市场索引 blockquote 仍在原位。

**0001 重构(仍生效)**:投稿改为 **yml-only**——"That one file is the whole submission"(contributing.md:26)。投稿者**不再需要**跑 `generate-readme`(也不再提交 README);PR 合并后由 `.github/workflows/sync-readme.yml` 在 main 上重生成并以 bot 身份提交(`permissions: contents: write`,sync-readme.yml:32-33)。pr-check 的 `--check` 语义收窄:**仅当 PR 自己手改了 README 才要求与 yml 匹配**(pr-check.yml:158-213;0002 起判定对象从 merge ref 改为 PR head,见 [submission-gates/01](../submission-gates/01-pr-check-and-guard.md));yml-only PR(新常态)由 runner 现场重新生成以保持树一致。动机:要求 PR 内 regenerate 曾使同分类的提交永远互相冲突——8-30 当天 296 个 open PR 里 218 个卡在生成行上,"none of them over anything a human had written"。

## 本专题的三个核心机制(0007 三个都零改动)

1. **模板替换 + 全文集合校验**(双层):只保证 marker 块内的正确性是不够的——PR 可以在 `<!-- END PLUGINS -->` 之后再塞一个 `### UI Enhancements` 标题和几行条目,站点解析器(按标题正则切片)会照单全收而 YAML 无从对应。所以 generate-readme 有 `parsedUrls()`:把**整个文件**当站点会读的样子再解析一遍,URL 集合必须与 data/plugins 声明完全一致(generate-readme.mjs:71-84, :171-179)。"smuggled" 与 "missing" 都是失败。
2. **锚点算法复刻**:GitHub heading anchor 的实现逐字重写并注释两个「像 typo 但不是」的结果("Themes & Appearance"→`themes--appearance`;emoji 被删但它的空格留下 → `-ui-增强`,generate-readme.mjs:27-32)。TOC 与章节互链的正确性建立在这份复刻上。
3. **描述文本是贡献者散文,必须先防御 Markdown**:描述里 `[Shot N HH:mm]` 这类方括号会被 remark 当 link reference,让 awesome-lint 以 "expected corresponding definition" 全文爆红——作者无从知道为什么。escapeRefs(:117-121)只在真正会成为 reference 的位置转义开括号,跳过 code span(那里反斜杠会渲染出来)与已有 inline link(`(?![^\]]*\]\()`)。源码注释(:115)仍写着 0001 的"对全部 4,279 条描述验证为 no-op";**0004 实测两个 README 各有 5 条条目行的描述里带 inline link**(0001 时注释说三条),这个豁免面在变大,注释自己没跟上——好在判据是正则而不是计数,多出来的两条不需要改代码。**0007 按同一判据重数:双语各 7 条**(描述里出现 `](`),继续缓慢增长;`generate-readme.mjs` 零 diff,所以这条注释依旧是 0001 的口径。

## 双语配对是怎么被强制执行的

| 层 | 机制 | 出处 |
|----|------|------|
| 数据层 | validateEntries:description.en 必填单行;zh 可省但存在即非空非换行;未知 locale 拒绝 | lib/entries.mjs:212-237 |
| 生成层 | 缺译不阻塞——zh 渲染英文原文并汇报清单("an honest gap a maintainer closes later") | generate-readme.mjs:147-148, :182-186 |
| 站点层 | parity 五检(同文件重复 URL / 分隔符 / 译文缺条目 / 分类不一致 / 译文多条目)| build-site.mjs:125-166 |
| 守卫层 | contributing.md 的 category 清单由生成器核对(CAT_IDS 拼串比对,漂移过一次后改为脚本看守)| generate-readme.mjs:204-215 |

**已知未守卫点(0004 复核不变;0007 数据层判据同样不变)**:`.github/pull_request_template.md` 的 category 列表仍是人工同步的 23 项(:6),不在任何脚本看守范围内。这个仓库的一致性哲学不变:**能被脚本看守的都被看守了;看不了的靠注释承认人工性**。0004 新增的 `icon` 也遵守同一条:形状由 `validateEntries` 看守,而"图还活着吗"没人看守(见 [registry-data](../registry-data/00-map.md))。0007 `lib/entries.mjs` 零 diff,所以上表"数据层"那一行与 0004 逐字相同。

## sync-readme.yml:bot 重生成(0001 新增,0002 加固,0004 加 registry env,0007 加 fork 门)

- **写权限的口子**:注释明说 "Unlike build-site.yml, this one DOES write to the repository — that is its entire job",刻意独立成窄权限 workflow,保住 "the build never writes" 在 build 侧为真。0004 复核:**它仍是全仓库唯一 `contents: write` 的 workflow**(:33);其余九条都没有授予这个权限(build-site.yml:26 出现过这五个字,但它只是注释,`permissions:` 给的是 `contents: read`)。**0007 复核这条仍成立,但 fork 门上之后它在本仓不会触发**——静态权限没变,动态生效面变了。
- **触发面包含生成器本身**(:22-26):`data/plugins/**`、`scripts/generate-readme.mjs`、`scripts/lib/**`、`site/locales.mjs`。所以 0004 里 `lib/entries.mjs` 的两次改动(#7647、#7934)合并后各触发了一次 sync-readme 运行——改 schema 与改数据走同一条路,区别只是前者重生成后没有 diff,于是按设计 exit 0("READMEs already match data/plugins — nothing to do"),不留提交。0007 触发面零改动,但 fork 门上之后的路径是"触发 → job 判 `skip`",不再有 exit 0 那一步。
- **排队不取消**:`concurrency: { group: sync-readme, cancel-in-progress: false }`——两个 merge 都会触发重生成,取消会让 main 留着 stale README 等下一次 merge 才修复,所以排队。
- **0002 修的三件事**:
  1. **检出 `ref: main`**(:59-62):"a queued run still holds the sha it was triggered on, which by then is an ancestor of main"——排队等到的运行手里那个 sha 早就不是 main 了。
  2. **三轮重试循环**(:83-105):`git fetch origin main` → `git reset --hard origin/main` → 重新生成 → 有 diff 才提交 → push;push 被拒说明 main 又动了,就在新的 tip 上重做。
  3. **三轮都输就显式红**(:107-115):`::error::` + exit 1,不再静默留下过期 README。动机是实测事故:2026-09-19 README 陈旧了**八小时**("Eight hours of that on 2026-09-19 is why this loop exists"),注释也顺势改成 "Queueing alone is not enough"。
- **0004 唯一的 diff 是 `npm ci` 的 registry 覆盖**(:66-72):lockfile 钉的是 `registry.npmmirror.com`,该 CDN 在 GitHub runner 上 503/504 挂过几十分钟(2026-10-19),于是六个带 `npm ci` 的 workflow 统一加 `npm_config_registry=https://registry.npmjs.org/` + `npm_config_replace_registry_host=always`。重生成逻辑本身没动。
- **0007 唯一的 diff 是 job 级的 fork 门**(:50-53,+4/−1):`if: github.actor != 'github-actions[bot]' && (github.repository_owner == 'awesome-dsh-plugin' || github.event_name == 'workflow_dispatch')`。注释把理由写在门上面:"A fork mirrors the catalog but must not commit bot-generated READMEs, or its main drifts from upstream on a commit nobody reviewed." **对本仓的直接后果**:这个 fork 上 bot 不会自动重生成 README,合并后看到的 README 是随 merge 带进来的;改 `data/plugins/` 之后要么手动 `node scripts/generate-readme.mjs`,要么 `workflow_dispatch` 跑一次。原来那条 `github.actor != 'github-actions[bot]'` 的终止性论证(第二次运行 diff 为空即 exit 0)仍然成立,只是现在它排在一个更靠前的门后面。
- **added-date 语义转移**(workflow 注释里自己交代了,:94-98):新条目 README 行的"首个 added commit"现在是这个 bot commit 而非 merge commit——同日秒差,0002 新增的 yml 账本(`lib/added-dates.mjs`)正是为了在有改写/迁移时给回一个可信日期,见 [site-surface/01 §阶段流水](../site-surface/01-build-site.md)。

## 正文

- [01 · generate-readme 逐段机制](./01-generate-readme.md)
