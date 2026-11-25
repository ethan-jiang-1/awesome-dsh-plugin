# probes-and-decay · 探针与衰减

> 状态:**0007 给本专题加了一整条采集线(Release 历史),衰减侧逻辑一字节未动**(基线 `upstream@8f1a1800e`,2026-11-25,行号以当前 checkout 为准)。新增 `scripts/probe-release-history.mjs`(90 行)与 `scripts/lib/release-history.mjs`(144 行);**不新建 workflow**——挂在既有 `probe-updates.mjs` 尾部,该文件 331→**343** 行(开头取出内部键 `$releaseHistoryV1` 再从 map 里删掉、末尾 try/catch 调 `collectReleaseHistory`、写盘改 `tmp + rename` 原子写并压成单行 JSON、日志计数改用 `have` 以免把内部键算进仓数)。同轮 `probe-npm.mjs` 181→**183**(改用 `lib/npm-name.mjs` 的 `publishedNpmName()`,唯一硬编码例外 `tests4gptplay/dsh-dots` → `@tests4gptplay/dsh-dots`)、`probe-readmes.mjs` 310 行 +1(zh 候选补 `docs/i18n/README.zh-CN.md`,:54)。**衰减侧零逻辑 diff**:`scan-decay.mjs` 仍 **388 行**、逐字节未变,`decay-scan.yml` 只加 4 行 job 级 fork 门(:25)。脚本清点:全仓 `scripts/**/*.mjs` 44→**49**(含测试)、测试 11→**13**、`scripts/lib/` 10→**12**;`ls scripts/probe-*.mjs` 是 12 项,其中 `probe-order.test.mjs`、`probe-updates-graphql.test.mjs` 是测试,实际探针脚本 **10 个**(0006 是 9 个)。
>
> **0006 结论保留(标历史,基线 `29b3ed46e`,2026-11-18)**:新增 `lib/github-statistics.mjs`(批量 GraphQL 库)、`probe-releases.mjs`(Release 附件下载)、`lib/release-manifest.mjs`(清单 URL 锁定 tag);probe-stars 整体重写(REST 单仓 → 批量 GraphQL,142→133 行);`build-site.yml` 修 downloads 缓存回写(#14322)。这三个脚本本轮全部零 diff,结论继续成立,只是不再是"本轮新事"。
> 最近核验:`8f1a1800e`。

## 定位

收录只是开始。probe-\* 家族定期回到外部世界采集事实(stars/下载量/npm 归属/上游 README/release 更新/tarball 存活/截图存活/**安装产物碰了什么**),scan-decay 找失联与失能,两个 publish 脚本把成果发成 npm 包供下游(尤其 dsh-market 与大陆镜像环境)消费,adopt-discussions 收拾评论线程。这个专题拆「活着的数据怎么保鲜、怎么不腐烂」。**0004 新增一条主线**:探针开始记录"与上一版相比变了什么"(capabilities 的 `previous`)和"这个包有没有来源证明"(npm provenance)。**0007 新增的是另一回事**:探针第一次为**终端站点**生产历史数据——每仓一份 Release 历史分片,不进 `data/*.json`、不进 catalog 包、不发 npm,只落 `docs/release-history/v1/`;它复用 `updates.json` 的缓存与入口,所以"提交边车五个 / cache-only 五个"的口径不变,只是 `updates.json` 里多了一个 `$releaseHistoryV1` 键、`docs/` 下多了一棵树(细节见 [01](./01-probe-family.md) 与 [03](./03-publish-layer.md))。

## 一图流:谁读什么、写什么、怎么持久化

| 数据文件 | 写入方 | git 追踪? | Actions cache |
|----------|--------|-----------|---------------|
| `data/stars.json` | probe-stars | ✅(.gitignore 显式注明 NOT ignored)| 共享条目 probe-data-v2 |
| `data/downloads.json` | probe-downloads | ✅ | 独立 downloads-v1(#2797)|
| `data/added-dates.json` | 人工冻结基线(非探针)| ✅ | — |
| `data/screenshots.json`(legacy) | 人工(已被停用)→ prune-legacy-screenshots 渐进清空 | ✅ | — |
| `data/capabilities.json`(0002 新增) | probe-capabilities | ✅ | **无**,也**没有回写通道**(0004 复核仍是纯地板)|
| `docs/index.json`(**0004 新增**,构建产物) | build-site.mjs(消费 `data/npm-map.json`)| ❌(`docs/` 被 .gitignore:9 忽略)| 无,每次构建重算,随 catalog 包发布 |
| `data/npm-map.json` | probe-npm | ❌ | 共享条目 |
| `data/readmes.json` | probe-readmes | ❌ | 共享条目 |
| `data/tarballs.json` | probe-tarballs | ❌ | 共享条目 |
| `data/updates.json` | probe-updates(**0007 起尾部还会写入 Release 历史缓存**)| ❌ **从未提交过** | 独立 updates-v1 |
| `data/screenshots-declared.json` / `-live.json` | probe-screenshots | ❌ 且刻意不缓存(重算免费)| — |
| `data/releases.json`(**0006 新增**)| probe-releases | ❌(.gitignore:17)| **cache-only 第五个,且当前仍无 cache 条目、无 workflow 调用方**——只活在维护者本机;消费见 [01](./01-probe-family.md) |
| `data/updates.json` 的内部键 `$releaseHistoryV1`(**0007 新增**)| probe-release-history(由 probe-updates 尾部调用,:335)| ❌(随 `updates.json` 一起活在 updates-v1)| 与 `updates.json` 同一条,**没有新增 cache 条目** |
| `docs/release-history/v1/<owner>/<repo>.json`(**0007 新增**,构建产物)| build-site.mjs 的 `publishReleaseHistory()`(:1237)| ❌(`docs/` 整目录被忽略)| 无,每次构建重写;总预算 900 MB 减 `docs/` 现值 |

> **0001 勘误(0002 更正)**:`updates.json` 在 0001 的表里被标成"✅ 已提交",实际它**从未进过 git 历史**(`git log --all -- data/updates.json` 为空),只在 updates-v1 cache 里。它也是唯一一个既不在 .gitignore、又从不被提交的 data 文件——本地跑一次探针就会在 `git status` 里冒出来。

**三份提交边车在 2026-11-25 的真实年龄(读文件自己写的字段,不看 mtime)**:

- `data/capabilities.json`:**3805** 条记录(0006 基线 3813,本轮 −8,纯删除),`tool` **全部** `dsh-trust-check@0.1.13`(而 HEAD 的默认扫描器已是 0.2.1),`provenance`/`previous` 各 0 条;`scannedAt` 只有两个取值——`2026-09-24T17:02:46.730Z` **3097** 条、`2026-09-24T17:41:52.360Z` **708** 条(0006 基线是 3105/708)——0004/0006 写的"全部同一个 timestamp"不准确,同一天是对的,所以"没有一次重扫落进仓库"的结论不变;
- `data/stars.json`:**1445** 个键,`checkedAt` 为 1443 条 `2026-08-19`、1 条 `2026-09-04`、1 条 **`2026-11-02`**。**0006 的读数要更正**:那份档案写"1464 键 / 1463+1",而 0006 基线(`git show 29b3ed46e:data/stars.json`)实测是 **1447 键**(1445×08-19 + 1×09-04 + 1×11-02)——总数与分布两处都不对,`2026-11-02` 那条在 0006 之前就在,不是本轮新写的(本轮区间 `stars.json` 只有删除);
- `data/screenshots.json`:**289** 个键,**没有任何时间字段**——它的年龄只能靠 diff 推。

三份文件在 `29b3ed46e..8f1a1800e` 区间的 diff **都是纯删除**(`git diff --numstat`:`data/capabilities.json` 0/99、`data/stars.json` 0/8、`data/screenshots.json` 0/3,`+` 是新增行;分别对应 3813→3805、1447→1445、290→289 个键),也就是**没有出现任何一个新的时间戳**,没有一次重扫或重探落进仓库。这才是"冻结"的可核对含义。(同区间 `data/added-dates.json` 是 +24/−4,人工钉日期,不属于探针产物。)

**capabilities.json 的定位很特殊,而 0004 把它变成了一个可证明的结论**:它仍是**提交进仓库的地板**,却不由任何 workflow 回写(build-site.yml:245 每次都跑 probe-capabilities,但 build-site 的权限是 `contents: read`,build-site.yml:49),也不在任何 actions/cache path 里(build-site.yml:112-120 只列 npm-map/stars/readmes/tarballs,downloads 与 updates 各有独立条目 :143-147/:152-156)。于是每夜的重扫结果只活在那次 run 的 `docs/plugins.json` 里,而那份文件会部署、会被打进 npm catalog 包——**线上可以很新,仓库地板只会更旧**。这份旧在 0004 时算过一次:名单当时从 4489 条涨到 6704 条,按那天的 `data/plugins/*.yml` 的 url join,只有 **3764/7924(47.5%)** 的条目还有记录(0003:3826/4489 = 85.2%),另有 57 个键指向已经不在名单里的 URL(0004 实测,**本轮未重算**);删掉的记录探针不会清理,只能人手工删(oauth-subs 那条就是 2026-10-20 手工删的,1a93fa18f,#8058)。现文件已缩到 3805 条(本轮纯删除)。

## 两条铁律(贯穿全部脚本)——0002 修正

1. **「未知 ≠ 死亡」。** 任何网络失败产生的都是"保留旧值",绝不写成否定性事实。**0002 修订**:0001 版写的例外"(404 除外——那是 GitHub 说的)"**在 readmes 上已被撤销**——probe-readmes 现在把 404 也当失败,保留旧值(它删掉了 `missing:true` 这个字段);probe-downloads 对"批量成功但该包不在返回里"也改为**保留旧计数,绝不写 0**。规则的**精神**没变(未知不许伪装成事实),变的是"什么算已知"。**0004 又多了两个实例**:扫描器的 schema 从"只认一个版本"变成"认一个可读集合"(`READABLE_SCHEMAS = {1, 2}`,lib/capabilities.mjs:25-26);provenance 查询失败返回 `undefined` 而不是 `present:false`(probe-capabilities.mjs:80-93)。**0006 把这条纪律下沉进了共享库**:`lib/github-statistics.mjs` 对任何缺失/失败的页把**整仓作废**;contributing.md 写了"an unknown count is never zero",npm 30 天 `downloads` 与 `githubReleaseDownloads` 不得相加。**0007 的新落点整条都在这条纪律上**:`readHistoryPages()` 逐仓验收,alias 有 error、`nodes` 不是数组、`pageInfo` 缺失或 `hasNextPage` 非布尔、`hasNextPage` 却没 `endCursor` —— 任一条命中就 **continue,该仓这一轮什么都不写**(lib/release-history.mjs:45-63);`refreshHistory()` 只在拿到页时覆盖,旧值原样保留;`fallback` 让"正在重扫"期间**继续发布上一版已发布内容**(:79-83);`publishReleaseHistory()` 只在文件真的写成功后才把 repo 放进 `repositories`(:136-141)——预算超了的那一份**不算已发布**,`docs/updates.json` 也就不会标它。
2. **失败不许伪装成数据。** **0002 修订**:0001 版说"除 probe-readmes 外都有覆盖率地板(MIN_COVERAGE = 0.66),推不回来就 exit 1"——**现在只有 probe-stars 与 probe-downloads 有地板**(后者是分 population 的双 66%);probe-updates 与 probe-capabilities 改为 **exit 0 且不写盘**。理由是同一件事的另一面:cache 的 save post-step 只在 run 成功时执行,`exit 1` 会把 updates cache 打成**永久 miss**(#5731)。"失败不写盘"仍在,只是不再用红 exit 表达。0004 对这条没有改动,capabilities 的全失败分支仍是"保留旧文件 + 一行日志"(probe-capabilities.mjs:222-229)。**0007**:release-history 没有地板也没有 exit,配额见底就把整轮**暂停**并保留已拿到的那部分(probe-release-history.mjs:26、:46-49);`collectReleaseHistory` 自身抛错时 probe-updates 用 catch 兜住、回写旧缓存(probe-updates.mjs:334-339)——与"失败不写盘"同族,只是这里的"盘"是 cache 里的一个键。

## 反常设计盘点(有意为之 vs 待商榷)

- **非原子写入(0007 破例一次)**:除一个例外,所有脚本仍是裸 `writeFileSync`,无 tmp+rename。**例外是 `probe-updates.mjs`**:`OUT_FILE + '.tmp'` → `writeFileSync` → `renameSync`(:340-342),同时把 JSON 从缩进 1 压成单行——这条路径现在写的是"site payload 的源文件 + 一个内部缓存键",半行坏文件的代价比别的探针高。其余仍靠天花板规则兜底;capabilities 每 100 条整文件重写一次(FLUSH_EVERY,probe-capabilities.mjs:115、:125-129),中断时留下的是"已扫到的最新完整快照"。
- **fetch/限流封装仍不统一,0007 又多了一种**:`lib/github-statistics.mjs`(0006)管批量 GraphQL,`lib/probe-updates-graphql.mjs` 管 `rateLimitDelayMs`,stars/npm/tarballs/screenshots 各自为政。0007 的 release-history **自己写了一份 fetch**(probe-release-history.mjs:29-39,15s `AbortSignal.timeout`),只从家族里借了 `repoOf`(lib/release-history.mjs:3、:16),没有复用 0006 的批量库——报酬是它拿到了完全独立的预算旋钮(见 [01](./01-probe-family.md) 的配额一节),代价是 GraphQL 的错误与分页验收在 lib 里重写了一份(私有仓与 404 都表现为 `data[alias]` 取不到 `nodes`,靠同一条"`nodes` 必须是数组"的验收兜住,没有像 `github-statistics` 那样显式读 `isPrivate`)。
- **`$releaseHistoryV1` 是塞进站点 payload 源文件里的内部键**。同一个 `data/updates.json` 既是探针的 cache、又是 build-site 的输入,所以 build-site 必须显式知道这个键存在并且**剥掉**它(build-site.mjs:1231 读、:1245-1256 只吐 `releaseHistory: true` 标记);而 probe-updates 是在 `Object.fromEntries(...sort)` **之后**才把内部键追加进去(:333-335),文件因此不再全局键序(`$` 本应排最前)。这是本轮最容易被下一个消费者踩到的一处:谁把 `updates.json` 原样透传出去,谁就泄漏整份缓存。
- **probe-downloads 的死常量仍在**:`CONCURRENCY = 8` 未使用,实际全串行——scoped 包靠每包 sleep 2000ms 的 pacing 过 limiter(实测 8 并发 94/134 失败)。
- **probe-npm 对新条目的污染通道仍在**:首见即遇网络故障会被记成 `{npm: null, version: null, checkedAt}`(≈"未发布",:165),因 unpublished 判定每天重查而次日自愈,但仍是家族里唯一的"未知写成否定"例外。0007 改的是**身份**不是这个洞:`publishedNpmName()`(lib/npm-name.mjs:4-12)只为一行加硬编码例外——`tests4gptplay/dsh-dots` 的经典条目在主仓被 Dot MCP 占用后仍解析到已发布的 `@tests4gptplay/dsh-dots`;其余条目一律返回 `package.json` 声明的名字。注意它比对的是 `repoPath` **全串**(probe-npm.mjs:121),所以例外只对"仓库根那条"生效,子路径条目(`…/tree/main/packages/x`)不吃这个特判。
- **0004 的新债:capabilities 的"固定资产"没有维护回路。** 它不回写、不进 cache、**也不清理名单外的键**(`next = { ...stored }`,probe-capabilities.mjs:115、:125-129;对照 probe-stars.mjs:92-93 与 probe-npm.mjs:176-177 都有 `listed` 删除循环)。后果是两件可观察的事:孤儿键要人手工删;2026-10-20 那条 compare-only 误报的修复落在**两处**——代码里加过滤器(lib/capabilities.mjs:149-165)、以及手工从 `data/capabilities.json` 里删掉一行 redLine(0355e74b5,#8140)。当一次修复必须手抄进数据文件,说明数据文件的再生路径事实上不存在。**0007 把"有删除循环"的清单从五个扩到六个**(probe-release-history.mjs:84-87),capabilities 仍是那个例外。

## 正文

- [01 · probe 家族:十二个采集器的机制参考](./01-probe-family.md)
- [02 · scan-decay:腐坏判据与人机分工](./02-scan-decay.md)
- [03 · 发布层:npm 双包、legacy 截图清退、评论收编与 0007 的静态历史分片](./03-publish-layer.md)

调度拓扑(probes 在 CI 里的位置)与 build-site.yml 编排见 [site-surface/01](../site-surface/01-build-site.md) §部署链;decay-scan.yml 触发 cron `41 3 * * 1`(周一),权限仅 `contents: read` + `issues: write`(:12-14)——物理上无 commit 能力,与脚本的 flag-only 设计互为双保险。**0002 新增调度线**:adopt-discussions.yml(`discussion: created` 事件 + 每周二 04:17 全量扫,:20-25,权限 `contents: read` + `discussions: write`,:32-34——**仓库里第一条写非仓库资源的 workflow**)。**0004 唯一的调度改动在安装源**:六个 workflow 的 `npm ci` 全部加上 `npm_config_registry: https://registry.npmjs.org/` 与 `npm_config_replace_registry_host: always`(13dcda271,2026-10-19),因为 lockfile 里有 7 个 `resolved` 指向 registry.npmmirror.com。**0007 的调度改动是"减法"**:8 条 workflow 在 job 级加同一道 fork 门(`github.repository_owner == 'awesome-dsh-plugin' || github.event_name == 'workflow_dispatch'`;其中 7 条是裸门,`sync-readme.yml:53` 把它与既有的 `github.actor != 'github-actions[bot]'` 用 `&&` 串起来),本专题有两条——`decay-scan.yml:25` 与 `build-site.yml:78`(探针全在 build-site 的 build job 里,所以**本 fork 合并后不再自动跑任何探针、也不部署站点**;`docs/` 里带进来的产物是上游跑的)。脚本侧的触发逻辑一行未改。
