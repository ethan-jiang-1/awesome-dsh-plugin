# registry-data · 数据模型

> 状态:**0005 无对应 diff**(`lib/entries.mjs`、schema 白名单、`CAT_IDS` 全部零 diff)。结构统计重跑到 **7924 条**;本轮新增 URL 1281、删除 61、改名 11、同 URL 修改 182。新增里 2 条把 JSON 写进 `.yml`(`pixelligue/mcpbids-plugins`、`pixelligue/mcptender-plugins`):上游用 js-yaml,JSON 是合法 YAML 1.2,门禁照收——**条目文件不是严格 YAML 子集**。`data/capabilities.json` 仍是 2026-09-24 旧扫描,按当前 URL join 只剩 **3764/7924(47.5%)**。最近核验:`efe602e7b`,2026-10-31。

## 定位

`data/` 是全仓库唯一人工编辑层:`data/plugins/*.yml` 一个插件一个文件(实测 **7924 个**,2026-10-31,来自 **5114 个不同 owner**;0004 为 6704/4298,0003 时 4489 条 / 2821 owner,0002 基线 4392,初问快照 2286;全部满足 `<owner>__<repo>.yml` 命名,monorepo 子包形如 `owner__repo--packages-my-plugin.yml`,sub 用单 `-` 连接)。除 `plugins/` 外的 data 文件全部是机器写或冻结的派生物(拓扑见下)。为什么一文件一插件:以前所有人往 README 同一分类的同一位置追加,合并一个 PR 就撞掉下一个——独立文件永不冲突(contributing.md:47)。投稿者也不必再 regenerate README(合并后由 main 重生成,见 [readme-pipeline](../readme-pipeline/00-map.md))。

## 条目 schema(validateEntries 白名单,scripts/lib/entries.mjs:169-256)

| 字段 | 规则 |
|------|------|
| `url` | 必须 `https://github.com/<owner>/<repo>[/tree/<branch>/<sub>]`;全列表唯一 |
| `name` | 显示文本,惯用 `owner/repo`(子包加 `#subname`)。**0002 新增硬规则(:202-208)**:写成 owner/repo 形式的 name **必须等于 url 的 owner/repo**(大小写不敏感;`#` 之后自由;纯显示名如 "Session Lens" 不受查)。理由:#5756 查出 6 条"名字指着一个仓库、链接指向另一个",其中 5 条的名字仓库**根本不存在**——"the name is the link text, so it must name the repository the link goes to" |
| `category` | ∈ CAT_IDS(23 个:`agi ui usage theme model identity session memory tools wsl browser vision voice docs skill workflow git notify dev security remote market fun`;wsl 为 0001 新增,#3664;0002/0003/0004 窗口内未增删)|
| `description.en` | 必填,单行 |
| `description.zh` | 可省;存在即非空非换行;**未知 locale(如 ja)拒绝** |
| `icon` | **0004 新增,可省**(:120-134 `iconProblem`,:247-253 调用):必须是 https,host ∈ ICON_HOSTS 四域(`raw.githubusercontent.com`/`user-images.githubusercontent.com`/`camo.githubusercontent.com`/`github.com`),且 pathname 以 `.png/.jpg/.jpeg/.webp` 结尾(大小写不敏感)。SVG 与第三方图床一律拒。github.com 只校验 host+扩展名,不像 tarball 那样要求路径含 `/releases/` |
| `tarball` | 可选;仅 GitHub 域 https `.tgz/.tar.gz`,github.com 路径必须含 `/releases/`(TARBALL_HOSTS 三域)|

- 显式禁项:**手写 `npm:` 键被校验拒绝**——npm 归属只能由 registry 的 package.json `repository` 字段回链自动采集,"防止某个包把自己挂到并未认领它的仓库上"(contributing.md:220-222)。这靠白名单实现:`ENTRY_KEYS`(:166)现在是 `url name category description icon tarball`(加上 `readEntries` 注入的 `file`),报错文案会把允许的六个键**逐个列出**(:176-181),所以 0004 加了 `icon` 之后,这条报错也跟着变了口径。
- YAML 手写高频错误已内建诊断:`description` 含 `": "` 未引号 → readEntries 定位肇事行并给出改写建议。**0002 起语法错误还有一道兜底**:pr-gate 会先解析每个变更的 `.yml`,不合法就报 `文件:行号`(#4680 的 `zh:` 行是 GBK 乱码,曾被静默丢弃五天)。
- dumpEntry 省略空翻译键("未译"≠"译成空"),lineWidth -1 超长单行、双引号风格。
- **0004:`icon` 的信任边界是一次纯形状校验,不是一次拉取。** 判据只有"https + 四域 + 位图后缀";没有探测这个 URL 是否 200(与 tarball 有 `probe-tarballs` 兜底 404 不同),也没有尺寸/大小/去重检查。所以死图标不会被摘,只由消费端回退到作者头像——"不会让访客去不可担保的图床取图"这句承诺只保证**取图源是 GitHub**,不保证图还在。
- **0004:`icon` 的执行点集中在别处。** `validateEntries` 在全仓库只有 `generate-readme.mjs:95` 一个调用方,所以 `icon` 规则实际在 pr-check 的再生成步骤(pr-check.yml:206/210)和合并后的 sync-readme(sync-readme.yml:83)上生效;`build-site` 只 `readEntries()` 后把它透传进 `docs/plugins.json`(build-site.mjs:48-52, :1169,缺省即省略),不重校验,`README` 也不渲染它。本轮 13 条带 `icon` 的条目全部落在 `raw.githubusercontent.com`。
- **0004:`readEntries` 的 `file` 现在是 POSIX 路径**(:68-75 `toPosix`,:105 注入)。原因不是跨平台洁癖:`file` 会被 echo 进 `::error file=…` 注解,并与 `git diff --name-only` 的输出比对,两者在任何平台都是 POSIX;Windows 上 `path.join` 给出的 `data\plugins\x.yml` 与 git 的打印永不相等,`check-submission.mjs` 于是回"没有新增/修改的条目文件——nothing to verify"并以 `ok:true, checked:0` 退出(:506-509)——一个把"通过"与"根本没跑"混成同一结果的失败模式。这个洞的代价是:pr-gate 只能用 `checked === 0` 兜底,把它变成一条"gate examined no entries"的红 check(pr-gate.yml:269, :346-348),作者看到的是"重跑一遍/这是 gate 的 bug",而问题既不在他的条目、也不在重跑。CI 全在 `ubuntu-latest`,所以真实触发面是 Windows 本地跑 check-submission。
- **同类 bug 已出现过一次**:`lib/added-dates.mjs:18` 早就在自己的边界上做 `file.replaceAll('\\','/')`。同一类分隔符假设散落在两个模块里,0004 修的是更靠上游的那一处;回写方向还留着一个同类洞——`dumpEntry`(:265-274)只写 url/name/category/description/tarball,**不写 icon**,任何"读进来再写回去"的工具都会静默丢掉这个字段(目前唯一调用方是一次性的 migrate-to-yaml.mjs,所以还没人踩到)。

## 分类体系(2026-10-24 census 普查)

共 23 类全部有脚本看守(generate-readme ↔ contributing.md ↔ reorder-categories.py 三处联动:改序重排要动 CAT_IDS 与 locales 两个 categories 块再再生 README)。条目量分布(全量):ui **1558**(19.7%)、tools 1061、session 567、dev 474、workflow 442、model 419、usage 418、memory 344、theme 310、notify 287、skill 285、fun 261、remote 238、security 216、browser 165、git 161、vision 161、docs 127、market 112、voice 102、**wsl 82**、identity 80、agi 54;前五类合计 51.8%。taxonomy 是活的:usage/vision/security/browser/git/docs/remote/voice/wsl 都是长胖后新增或拆出来的(注:wsl 尚未写进 contributing 的"拆分名单"原文,上游文档滞后)。

**wsl 类抽查(0004 更新)**:80 条(0003:77,本轮 +3),其中 **68 条来自同一作者 173787247**——该 owner 在全表共 70 条(另 2 条落在别的类目),而且**它的条目数一分没动(70→70)**:wsl 的 +3 条全部来自其他作者。所以浓度从 88% 降到 85% 是"别人扩容 + 名单整体 +49.3%"的结果,不是这位作者在扩产。schema 侧 wsl 没有专属变化,全局新增的 `icon` 这 80 条一条也没用;双语类目名 wsl: 'WSL & Windows Interop'/'WSL 与 Windows 互操作',CAT_EMOJI 🐧(entries.mjs:43)。下载转化沿用的仍是旧数据,不能据此断言当前需求。

**0002 勘误(普查脚本)**:census.py 的手写 YAML 解析器此前不剥行内注释,两条把 PR 模板注释一起粘进 `category:` 行的投稿(js-yaml 认为合法,读作 tools/model)会在 ① 表里凭空长出两个类目。已修(`strip_comment`,只切"前面是空白且不在引号内"的 `#`,URL 的 `#sub` 与描述里的 `#tag`/`#12B7F5` 都不受影响),tools 576 / model 213 是 0002 口径下修正后的数(2026-10-24 已是 878 / 362)。

主题类特殊通道:**Themes & Appearance(theme)**下的条目自动进入 dsh-market 的 Themes Tab 一键安装。

## 边车 JSON 与 CRLF 现象

| data 文件 | 写入方 | git 追踪? | 说明 |
|-----------|--------|-----------|------|
| `stars.json` | probe-stars | ✅(刻意不 ignore) | 提交的地板,保证"抓取失败保留旧值" |
| `downloads.json` | probe-downloads | ✅ | 独立 downloads-v1 |
| `added-dates.json` | 人工(冻结基线 + 改名锚定) | ✅ | **键 = 条目 URL 原文**(含子路径),不是 slug;548 键,值 496 条纯日期 + 52 条 ISO 时间戳。2026-08-15 前的日期冻结于此,之后只做人工锚定,其余由 build-site 从 git 推导 |
| `screenshots.json`(legacy)| 人工(已停用)→ prune 渐进清空 | ✅ | 有终点的 fallback |
| **`capabilities.json`(0002 新增)** | `scripts/probe-capabilities.mjs` | ✅ | 见下 |
| `npm-map.json` / `readmes.json` / `tarballs.json` | 各探针 | ❌(.gitignore 明列)| 只在 Actions cache |
| `updates.json` | probe-updates | ❌ **从未进过 git 历史** | 只在 updates-v1 cache;0001 误记为已提交,0002 更正 |
| `screenshots-declared.json` / `-live.json` | probe-screenshots | ❌(.gitignore)| 刻意不缓存,重算免费 |

**`capabilities.json` 的形状(0002 新增边车)**:`{url: {version, spec, capabilities[], redLines[], scannedAt, tool}}`,`capabilities` ∈ {shell, fs-write, fs-read, network, env, credentials, llm, dynamic-code, host-runtime, subagent}。**0004 的扫描器升级没有落到这份文件上**:仓库里 3821 条记录的 `tool` 仍全部是 `dsh-trust-check@0.1.13`,而 package.json 的 devDependency 已经是 `^0.2.1`(新记录会多带可选的 `previous` 上一版能力与 npm build provenance,见 `lib/capabilities.mjs:36-37`,但这里一条都没有)。文件 47,464 行,`scannedAt` 全部落在 2026-09-24T17:02:46–17:41:52Z,即一次扫描快照;与当前名单 URL join 只有 **3764/7924(47.5%)**(57 行指向已删 URL)——分母 4489→6704→7924,是覆盖率被新条目稀释,不是旧扫描失效。语义见 [probes-and-decay/01](../probes-and-decay/01-probe-family.md);它被 build-site 透传进 `docs/plugins.json`,**站内页面不渲染**。

`added-dates.json` 的规则值得单独记一笔(0004 已核对):它是**唯一被人工改写的边车**,键是条目 URL 原文(含 monorepo 子路径),值是首个 added 日期。548 个键里只有 **531 个对得上当前名单**(7.9%),其余 17 个是被改名/换 URL 甩下的旧键,没人清理;也就是说 **6173 条完全靠推导**——build-site 先翻默认语言 README 的 `-p` 历史,再翻 `data/plugins/` 的 `--name-only` 账本,最后用 `lib/added-dates.mjs:15-21` 的 `--diff-merges=first-parent --diff-filter=A` 取最老一次新增;还推不出来就拒绝构建(build-site.mjs:173-176 注释, :240-362,失败分支 :356-362)。人工键的用途因此很窄:**改名/换 URL 时把原日期钉回来**(否则新文件名的首个 added commit 会把老条目重新算成当天),本轮 +25/−2 全是这个用途,活着的键**没有任何值被改动**。

join 键统一是**条目 URL 原文**(含 monorepo 子路径)。URL→repo/sub 的 decompose 在探针里各有一份实现且行为不一(stars/updates 丢 subdir,npm/readmes/screenshots/prune 保留)——已知重复债。0002 新增一份**共享**实现:`scripts/lib/terms.mjs` 的 `slugOf/termOf`,由 build-site 与 adopt-discussions 共用(此前两处各自小写化,劈了评论线程)。

实测数据卫生事实:**28 个 yml 带 CRLF**(2026-10-24;0003 时 15 个,0001 时 11 个,初问 5 个);validateEntries 不查换行风格,js-yaml 容忍之,照常收录。generate-readme 已对 CRLF 免疫(`normalizeNewlines`)。**0002 新增一条同类观察**:`data/updates.json` 既不在 .gitignore 里、也从未被提交——本地跑一次探针就会在 `git status` 里冒出来,和它的三个兄弟(npm-map/readmes/tarballs 都在 .gitignore)不一致。

0004 边车 diff 观察:`added-dates.json` 525→548 键(+25/−2,全是改名钉日期,值零改动);`stars.json` 1472→1464 键(删 9 加 1,只随条目删除减);`capabilities.json` 3844→3843 键(**只减 1、零新增**,仍是 2026-09-24 那次扫描);`downloads.json` 本轮文件未动(624 键);`screenshots.json` 继续整文件轮转。一句话:**边车随名单删除而缩小,从不随名单增长而扩大**——0004 新增 2255 条里能力披露覆盖 0 条;0005 新增 1281 条里同样 0 条,且边车又因删除缩了 22 行。

## 待回答的问题

- [x] added-dates.json 的键与层级(0004 已核:键=条目 URL 原文,548 键中 531 个命中当前名单;2026-08-15 前的日期冻结 + 改名人工补录,其余 6173 条由 build-site 三路推导)
- [x] 边车 key 结构与 join → 见 [probes-and-decay/00-map](../probes-and-decay/00-map.md)
- [ ] 同 URL 多语言/多分类冲突在 validateEntries 与 build-site parity 两层的分工细节
- [ ] **0002 新增**:`updates.json` 是否该补进 .gitignore(现在靠"没人提交"维持不追踪)
- [ ] **0002 新增,0004 加剧**:CRLF 从 5→11→15→28 单调增长,是否该在 pr-check 加一条归一化守卫(而非只让下游免疫)
- [ ] **0004 新增**:17 个已改名条目的旧 URL 仍留在 added-dates.json 里(死键),要不要随改名一起清;以及 `dumpEntry` 不写 `icon` 的回写洞,是否该在有人加"读改写"工具前补上

## 正文

- 01 · 从 PR 到收录的数据生命周期(待写:新条目落地→首夜探针→出现在站点/市场/README 各面的时序)
