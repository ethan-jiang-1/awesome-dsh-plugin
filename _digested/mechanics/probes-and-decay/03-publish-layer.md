# 03 · 发布层:npm 双包、legacy 截图清退、评论线程收编与 0007 的静态历史分片

> 基线:`upstream@8f1a1800e`(0007 复核,2026-11-25;build-site.yml 314→**318** 行,+4 是 job 级 fork 门 :78)。**0007 给发布层加了第三个面**:`build-site.mjs` +27 行,把 Release 历史拆成 `docs/release-history/v1/<owner>/<repo>.json` 的**每仓分片**(`publishReleaseHistory()`,lib/release-history.mjs:111-144,调用点 build-site.mjs:1237),`docs/updates.json` 只标 `releaseHistory: true` 不内嵌历史,同一段代码顺手把 `docs/updates.json` 压成单行 JSON。**两个 npm 发布器本轮零 diff**(publish-catalog 仍 **169** 行、publish-updates 仍 **134** 行),prune-legacy-screenshots 114 行、adopt-discussions 脚本零 diff(它的 workflow 只加 fork 门 :49)。**0006 的结论原样成立**(downloads 缓存拆 restore/save、#14322);0004 的结论(catalog 包顺带装 `docs/index.json`、684KB 实测代价、拆包无排期)也原样成立,只是行号按当前 checkout 校正。
>
> 最近核验:`8f1a1800e`。

## 为什么发 npm(注释里有真实测量)

- Pages 就是 GitHub(响应头 `server: GitHub.com`),大陆访问慢;公共 GitHub 反代一律拒非 github.com 的 hostname(实测该域名 403)。发到 registry.npmjs.org 就**复用了插件生态本来就在用的镜像体系**(publish-catalog.mjs:3-14)。
- 单独成包而非塞进 `awesome-dsh-plugin` 包:npm 强制携带 README(两个 README 各 ~500KB),`npm pack --dry-run` 测得 772KB vs 独立 ~250KB;独立包还让目录获得版本号、可回滚(:19-25)。
- updates 与 catalog 拆成两包:catalog tarball 被每个 market 每次升级都拉,update notes 只被打开对话框的那一个用户读;合并会让全体消费者的每日下载翻倍(publish-updates.mjs:9-15)。
- **0004 的新理由不是"大小"而是"权限"**:索引本来要单独发一个 `dsh-plugin-catalog-index`,第一次发布直接 404——npm 的 trusted publishing 是**按包**配置的,一个还不存在的包没法从 CI 里建立这层关系。于是索引先塞进发布链已经跑通的那个包里(:40-48)。代价是 0004 实测的:**每次 catalog 下载多扛 684KB gzip(约 2.3MB JSON)**。这条债有明确终点(拆包),但没有排期。

## 两个发布器的同构机制

| | dsh-plugin-catalog | dsh-plugin-updates |
|---|---|---|
| 内容 | `docs/plugins.json`(原字节)**+ `docs/index.json`** | `docs/updates.json`(**0007 起内含各仓 `releaseHistory: true` 标记,不含历史本体**)|
| 幂等键 | packument 自定义字段 `catalogSha`=sha256(**两个文件拼接**,:133)| `updatesSha`(:48)|
| 版本 | `YYYY.MDD.RUN`(月份不补零——semver 禁前置零;日期部分跨年可比)| 同 |
| 凭据 | trusted publishing(OIDC),需 `id-token: write` + npm ≥11.5 | 同 |
| stage | os.tmpdir() 随机目录,**绝不写仓库内文件** | 同 |
| dry-run | `DRY_RUN=1` → 追加 `--dry-run` | 同 |

共享的两个决策:

1. **registry 打不通时照常尝试发布**:"重复版本的错误 < 静默跳过真更新"——npm 会拒绝重复版本兜底(:69-81)。
2. **执行顺序在 Pages deploy 之后**(build-site.yml:**301-307** 与 **314-318**;deploy 现于 :257-258):"站点才是大家看的,registry 故障没资格拖住它。" deploy 那一步对探针运行挂 `continue-on-error: schedule||workflow_dispatch`(:276):"deploy 失败也没资格拖住 registry 发布与 cache-save"(2026-09-05 的 403 曾把 36 分钟探针成果全部带走)。

0004 给 catalog 这一个发布器加的三处细节(历史,文件未变):

- **哈希口径变了**:`sha256(Buffer.concat([built, index]))`(:133)而不是只哈希 plugins.json,所以"只动索引的一天"也会挣到一个版本。
- **文件清单与导出同步**:`exports` 加 `'./index.json'`、`files: ['plugins.json', 'index.json']`(:160-161),README 里给出可直接粘的地址 `https://cdn.jsdelivr.net/npm/dsh-plugin-catalog/index.json`(:112-117)。
- **多了一条硬前置**:脚本无条件读 `docs/index.json`(:130),而 build-site 只在索引至少收录一条插件时才写这个文件(build-site.mjs:**184-194**,`indexBuilt` 判在 :190,写在 :194——缓存里没有 `publishedAt` 的老条目会让索引为空,此时面板不显示、文件也不落盘)。也就是说发布步骤的前置条件从"plugins.json 存在"变成了"这次 run 的 npm-map 足以产出一份非空索引"。nightly 走 `PROBE_ALL` 全量探针所以恒成立;真正的漏洞在手工 dispatch:带 `skip_probes` 且恢复到的 cache 还是 0004 之前那份时,探针被跳过、索引为空、`docs/index.json` 不存在,而 `publish-catalog.mjs` 没有"没有索引就不发"的分支——它会直接在 `readFileSync` 上抛错(build-site 侧只是"少写一个文件",发布侧是硬失败,两个文件的容错口径不一致)。

## 0007 新增:Release 历史分片——第三个发布面

它既不是 npm 包也不是 `data/*.json`,而是**站点上的静态 JSON 树**:每仓一个文件,由同一份 `updates.json` 里的缓存派生。链路一行:

```text
probe-updates.mjs ─┬─ data/updates.json(entries, cache-only)
                   └─ collectReleaseHistory(...) ──► data/updates.json[$releaseHistoryV1]
                                                        │
build-site.mjs ── publishReleaseHistory(ordered, history, 'docs', 900MB − docs 现值)
                   ├─ docs/release-history/v1/<owner>/<repo>.json   (每仓一片)
                   └─ docs/updates.json  { ..., releaseHistory: true }(只标开关)
```

- **分片形状**:`{repo, complete, releases[]}` + 换行;`releases[]` 的每一项就是 GraphQL 页解析后的 `{tag, name, publishedAt, url, body(≤4KB), commit}`(lib/release-history.mjs:54-59)。文件名与目录名都被 `catalogRepo()` **强制小写**,所以 `Owner/Repo` 与 `owner/repo/tree/main/packages/x` 落到同一个 `release-history/v1/owner/repo.json`。
- **两道闸**:单文件 ≤ **1 MB**(`MAX_FILE_BYTES = 1_048_576`,:10)且条数 ≤ **256**;信封先预留 `128 + repo 名长度` 字节再逐条累加(:122-127),所以"刚好 1 MB"不会被对象分隔符挤爆。
- **总预算**:`900_000_000 − docs 目录现值`(build-site.mjs:1237)。现值只在**缓存里真的有历史**时才去递归统计 `docs/` 大小(:1234-1236),否则按 0 算——第一次跑不会被一棵空树骗成"还有 900MB 可用"。超预算的仓 `skipped++`(:132-135),**不写文件、也不算进 `repositories`**,于是 `docs/updates.json` 不会给它标 `releaseHistory`——"发出去的标记"与"真的存在的文件"永远一致(测试第 ⑦ 例钉死这条)。
- **`complete` 的含义**:`无 fallback && next === null && 发布条数 == 源长度`(:129)。带 `complete: false` 的分片有两种情形:有 `fallback`(7 天到点、重扫进行中,发布的是 `fallback` 那份完整旧列表,:118——**站点不会看到变短的历史**)或 `next` 还没走完(发布已扫到的部分)。代价是这些状态只由一个布尔位表达,前端分不清"旧的完整版"和"新的半份"。
- **updates.json 的两个出口**(build-site.mjs:1245-1256):有 `updates` 行的条目在标了 `releaseHistory: true` 后原样透传;只有分片、没有 `updates` 行的名单条目则补一条 `{releaseHistory: true}`——后者是防御分支(`collectReleaseHistory` 已把历史裁到 `updates` 的仓集合内,正常不会出现)。
- **`docs/updates.json` 改成单行 JSON**(:1257):真正的动机是体积,但连带效果是**这个文件不再好 diff**——它是构建产物、本来也不进 git(`docs/` 整目录被 .gitignore:9 忽略)。
- **不进 npm**:`publish-updates.mjs` 只 `files: ['updates.json']`(:126)、只读 `docs/updates.json`(:29、:98),所以**开关上了 npm 包、分片没有**。一个只装 `dsh-plugin-updates` 的消费方拿到 `releaseHistory: true` 之后,除了回站点抓 JSON 没有第二条路。
- **吃的是 Pages 的 1 GB,不是 npm 的带宽**。这也是为什么预算要减"站点现值"而不是减"上次发布的历史体积":Pages 上限算的是整棵 `docs/`,包括 catalog 页、readmes/screenshots 等 payload。
- **消费方在当前 checkout 里不存在**:在源码目录(`site/`、`.github/`、`data/`、`contributing.md`)里 `releaseHistory` / `release-history` **零命中**——`site/` 里没有任何页面或脚本读这棵树。它与 0006 的 `data/releases.json` 正好互为镜像——那边"有消费者、无生产者"(probe-releases 无 CI 接线),这边"有生产者、有产物、无消费者"。

## 持久化拓扑(与 build-site.yml 的耦合)

```text
nightly(UTC 02:23)                       push / workflow_run on sync-readme
─────────────────────                     ────────────────────────────────
probe-npm → downloads → stars             五个探针全跳过
          → readmes → updates             (缓存命中时)
→ tarballs → screenshots                  → tarballs + screenshots + capabilities
→ probe-capabilities(不在 PROBE_ALL 门控里)  → build-site.mjs
→ build-site.mjs(写 index.json / updates.json / release-history)   → deploy pages
→ deploy pages                            (不做 npm 发布)
→ publish catalog(plugins.json + index.json)+ updates(OIDC)
```

- **0007 的拓扑变化只有一处**:`build-site.mjs` 这一步多写了一棵树(`docs/release-history/v1/`);`updates.json` 的缓存内容多了一个键,**cache 条目数不变**(probe-data-v2、downloads-v1、updates-v1 三条,见 build-site.yml:112-120、143-147、152-156)。
- 结果三路持久化:**git 提交的快照**(stars/downloads/added-dates/screenshots/**capabilities**)+ **Actions cache**(共享条目 `probe-data-v2` 一条含 npm-map/stars/readmes/tarballs 四个 path,另有 downloads-v1 与 updates-v1 两条独立 entry)+ 与快照合并;workflow 永不写回 git(`contents: read`,build-site.yml:49)。
  - **0006 修正 downloads-v1 的第三路语义(#14322)**:旧式 `actions/cache@v4` 的 post-step 在每次 run 结束都 save,push 构建(跳过探针)把 restore 到的旧 downloads.json 用新 key 存回去;restore-keys 前缀恢复按创建时间排序,这份"旧数据、新 key"的副本排在 nightly 刚存的新副本之前,**遮住 nightly 的成果,站点落后一天**。修法:restore 用 `actions/cache/restore@v4`(:143-147),save 拆成独立步 `actions/cache/save@v4`、条件 `steps.build.outputs.probed == '1'`(:248-253;`probed=1` 由 Build 步在探针分支末尾写入 output,:223)。probe-data-v2 与 updates-v1 仍是老式 `actions/cache@v4`(save 无条件,:112-120/:152-156)——同样的"旧值存新 key"结构在它们身上理论上也存在,上游只修了 downloads。
  - **0006 的第四路缺席者**:`data/releases.json`(probe-releases 写)不在 git、不在 cache、不在任何 workflow——cache-only 边车从 updates.json 的四个变成五个,而这个连 cache 条目都没有(见 [01](./01-probe-family.md) probe-releases 一节)。**0007 复核:仍无接线。**
  - **0007 的第五路**:`docs/release-history/v1/` 既不是快照也不是缓存,而是**构建产物**(和 `docs/index.json` 同类:只存在于那天的 Pages 部署里,仓库中找不到)。
- **0004 补充第四种东西:构建产物**。`docs/index.json` 每次构建从 `data/npm-map.json` 重算(build-site.mjs:184-194),`docs/` 整个目录在 .gitignore:9 被忽略,所以它唯一的副本就是那天的 Pages 部署和 npm 包——**索引比任何一份 data 边车都新鲜,却也是唯一一个仓库里找不到的**;0007 的 `release-history/` 树继承了这条性质,而且比索引更彻底(它连 npm 包里都没有)。
- **0001 勘误(0002 更正)**:快照清单里的 `updates.json` **不是** git 提交物——它从未进过 git 历史,只活在 updates-v1 cache。真正第五个提交快照是 **capabilities.json**。
- **push 构建的兜底分支(0002 改写)**:条件是 `case schedule|workflow_dispatch → full_probe=1` 的白名单(build-site.yml:189-199),所以 workflow_run 触发的构建**不会**再临时跑全套探针。0004 给这条兜底加的一处是 2026-10-18 的 `skip_probes`(ac02c4e5d,build-site.yml:12 输入定义、:196 分支):deploy-only 路径必须存在。
- push 冷缓存且 `data/npm-map.json` 为空的兜底仍会临时跑 probes(:199:"Probing is slow; that is cheaper than a wrong plugins.json")。
- **0007 的新前提(对本仓库)**:`build-site.yml` 的 build job 加了 job 级门 `if: github.repository_owner == 'awesome-dsh-plugin' || github.event_name == 'workflow_dispatch'`(:75-78,注释原话 "skipped there to spare the fork owner's Actions minutes on a deploy nothing consumes")。**本仓库是 fork,合并后不再自动构建、不再部署 Pages、不再发 npm**;工作区里看到的 `README.md`/`docs/`/边车都是上游产物随 merge 带进来的。想验证构建只能手动 dispatch。

## prune-legacy-screenshots.mjs:maintainer-run 的清退器(未变)

背景:截图约定已迁到作者仓库(contributing.md §Screenshots),`data/screenshots.json` 是有终点的 fallback——41/773 张已发布截图烂成 404 正是当初动机。本脚本对 legacy 文件里现存的每个 key 探测作者仓库是否已有**可用**声明("a key is only pruned if the declaration would actually be used"),是则删 key;键序显式保留不重排——重排会把几百行无关行染进 diff,破坏 maint-rebase.sh 依赖的 diff 信号。清空即提示可删除整个文件与 build-site 的 fallback 分支。

**0004 期间这个文件确实变小了,但不是它干的**:`data/screenshots.json` 从 289 键降到 288——两次作者要求移除(`b1ebf11a1`、`b039938b9`,2026-10-21)加一条新条目的截图(`f0baef2aa`,2026-10-17)。区间里没有 prune 的运行痕迹,这也符合它的定位:维护者手动跑,不是 CI 步骤。**0007 复核**:现文件 **289** 键(0006 基线是 **290**,本轮 290→289,`git diff --numstat` 0 新增 / 3 删除行 = 一个条目),仍无 prune 运行痕迹;这个文件"新鲜度"依旧没有时间字段可读,age 只能靠 diff 推。

## 0002 新增:adopt-discussions(评论线程的收编层)

它不是探针也不是发布器,而是**同一类"外部世界的数据与我们的 join key 不一致"问题**的第三个受害者(前两个是 npm 包名归属、截图声明)。

- **问题**:giscus 只在"帖子位于 `Plugins` 类目**且**正文含 `<!-- sha1: <sha1(term)> -->`"时才认这个线程;手工在 GitHub UI 建的帖子两个条件都不满足 → 三个界面各显示一个空框,而 giscus **静默开第二条线程**。
- **做法**:补上 marker、移进类目——"never deletes, merges or retitles";幂等。
- **触发**:`discussion: created` 事件(唯一能当场抓住手工帖的时机)+ 每周二 04:17 全量扫(adopt-discussions.yml:20-25,顺带把**仓库改名**后的线程重新接上——改名会动 catalog 的 slug,也就动了 widget 要的 term)。
- **权限**:`contents: read` + `discussions: write`(:32-34)——**仓库里第一条写非仓库资源的 workflow**;注释还承认 GitHub 把 discussion webhook 标为 "public preview, subject to change",失效时的兜底是那条每周扫,所以失败模式是延迟而不是劈成两半。
- **配套**:`lib/terms.mjs` 把 `slugOf/termOf` 收成 build-site 与 adopt 共用的单点(此前 catalog 小写化 term,凡是 owner/repo 含大写的条目都被劈成两个线程,2026-09-24 才修)。
- **0004 的唯一改动是安装方式**:`npm ci` 加上 `npm_config_registry: https://registry.npmjs.org/` 与 `npm_config_replace_registry_host: always`(:56-62)。这个 job 本身不碰 npm 生态,但它的脚本经 `lib/entries.mjs` 依赖 `js-yaml`,而 lockfile 里 7 个 `resolved` 指向 registry.npmmirror.com——所以这不是可有可无的优化。
- **0007 只加门**:job 级 `if`(:46-49,同 build-site/decay-scan 那句 "a fork … has no upstream discussions to adopt")。权限、触发、cron、`npm ci` 全未动——**这个 job 在本 fork 上同样只能手动 dispatch**。

## 待复核

- [ ] cache key 版本(v2/v1/v1)升级流程:改 path 列表 = 全体冷启动,历史上如何操作过
- [ ] updates 包的消费端(dsh-market 对话框)实际拉哪个 URL
- [x] ~~**0002**:capabilities.json 既无回写 workflow、也不在 cache path——夜间的重扫结果是否只活在那次运行的 `docs/plugins.json` 里~~ → **0004 已解**(`contents: read` + 无 cache + 每次构建都跑;棘手的部分变成了"线上那份是新的、仓库那份是旧的",见 [00-map](./00-map.md))
- [ ] **0004 新增**:索引什么时候拆成独立包。现在它让每次 catalog 下载多 684KB,而拆包需要一个只有人才能做的动作(在 npmjs.com 上建包并配 trusted publishing);在那之前,`publish-catalog.mjs` 里那句"这是权宜之计"就是准确的现状。
- [ ] **0007 新增**:`docs/release-history/v1/` 没有站点消费方(`site/` 零命中),也没有 contributing.md 说明。分片形状(`complete` 布尔 + 4KB 正文)是否够前端渲染"历史版本"列表、是否需要索引文件(现在前端得先读 `docs/updates.json` 才能知道哪个仓有分片),要等站点侧接线才能定。
- [ ] **0007 新增**:`900_000_000 − docs 现值` 的余量与 Pages 1 GB 硬限之间的真实距离**未实测**;分片总量随"有 release 的仓数 × 每仓 256 条 × 4KB 正文"增长,单仓上限 1 MB,按这个上限算约 900 个仓就吃满 900 MB 预算——而名单有 13136 条、有 release 的仓数未知。当前没有 CI 日志可查(本 fork 不跑 build)。
- [ ] **0007 新增**:`updates.json` 压成单行后,**同一个文件既是 cache 又是 payload 源**的耦合没有变;`$releaseHistoryV1` 靠 build-site 主动剥掉(build-site.mjs:1231、1245-1256),任何新消费者直接透传都会把整份缓存发出去。
- [ ] **0007 新增**:fork 门之后,本 fork 的 `docs/`、边车、README 全部是上游产物;要验证 Release 历史这条链路只能 `workflow_dispatch`,而 dispatch 需要上游组织下的仓库(见 [site-surface/01](../site-surface/01-build-site.md) §部署链)。
