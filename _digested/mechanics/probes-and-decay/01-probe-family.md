# 01 · probe 家族:十二个采集器的机制参考(10 个 probe-* 脚本 + scan-decay + prune-legacy-screenshots)

> 基线:`upstream@8f1a1800e`(0007 复核,2026-11-25;行号为当前 checkout)。**0007 加的是一个采集器,不是一次重构**:新增 `scripts/probe-release-history.mjs`(90 行)与 `scripts/lib/release-history.mjs`(144 行),前者**没有自己的入口**——它被 `probe-updates.mjs` 尾部调用(`:52-53` 导入、`:334-339` 调用),`.github/` 里没有一行提到它。同轮 `probe-updates.mjs` 331→**343**(内部键 `$releaseHistoryV1` 进出、原子写、压成单行 JSON)、`probe-npm.mjs` 181→**183**(`publishedNpmName()` 身份例外)、`probe-readmes.mjs` 310 行 +1(`docs/i18n/README.zh-CN.md` 候选)。**其余全部零 diff**:probe-stars 133、probe-downloads 236、probe-tarballs 125、probe-screenshots 239、probe-capabilities 230、probe-releases 55、scan-decay 388、capability-changes 44、prune-legacy-screenshots 114、`lib/github-statistics.mjs` 69、`lib/release-manifest.mjs` 37。测试 13 个(0007 新增 `release-history.test.mjs` 118 行 7 例、`npm-name.test.mjs`)。
>
> **0006 结论保留(标历史,基线 `29b3ed46e`,2026-11-18)**:probe-stars 整体重写(REST 单仓 fetch → 批量 GraphQL,142→**133** 行,`checkedAt` 从 ISO date 变完整 ISO timestamp);新增 `probe-releases.mjs`(55 行)、`lib/github-statistics.mjs`(69 行)、`lib/release-manifest.mjs`(37 行)与两个测试;capability 与 npm 探针未动(0004 复核:probe-capabilities **230**、`lib/capabilities.mjs` **224**、`capability-changes.mjs` 44、`capabilities.test.mjs` **192**、probe-npm 181→现 183);downloads/readmes/updates/tarballs/screenshots 与 scan-decay、prune、publish-updates 当时零 diff。
> 最近核验:`8f1a1800e`。

## 公共行为模式

- **花名册来源**:tarballs/screenshots/capabilities/**releases(0006)** 四个直接 `readEntries()` 消费 YAML,其余解析 `README.md` 的条目行——README 与 YAML 各占一半。**0007 加了第五种**:**probe-release-history 吃的是上一轮的 `data/updates.json`**(`:15-18` 遍历 `Object.entries(updates)`,只留 `catalogRepo(url) !== null && entry.release?.tag` 的仓)——家族里第一个**探针吃探针**的采集器,名单 = 上一轮成功看到 release 的仓,不需要另读花名册。
- **增量判据**:`fresh()` = 非 PROBE_ALL 且已有值且 checkedAt 在 `PROBE_RECHECK_DAYS`(默认 1,readmes 例外默认 7,capabilities 7)天内。probe-npm 的 `version` 字段只靠 nightly `PROBE_ALL` 全量刷新;unpublished 每天复查。**0004 新增三条通道**:probe-npm 现在是 full probe / version-backfill / publish-backfill 三条 pass 串行(probe-npm.mjs:79-81、172-174),后两条都是"键在即不再触发"的一次性回填。**0007 新增一对双判据**(release-history):头页用 **stamp**(`tag:publishedAt` 变了才认为头页换了,`probe-release-history.mjs:17、:19`)决定排序,旧页用 **`REVALIDATE_MS = 7 天`**(lib/release-history.mjs:12)决定何时整段重扫——时间不再是唯一维度。
- **公平调度(0002 新增)**:`lib/probe-order.mjs` 的 `leastRecentlyChecked(urls, map)` 按 `checkedAt` 升序排、并列保持 README 顺序,已被 probe-updates 采用(:261)。动机是实测:2026-09-14 的 nightly `3632 listed … 2364 repo(s) kept their previous update data`,README 位置 40–80% 的条目最后检查时间停在 09-05——**预算被砍的一轮会把同一段列表饿死**(#5149)。**0007 是同一哲学的第二种实现**:`pending` 按 `checked(repo, stamp)`(stamp 不匹配记 0)升序推送——**换了最新 release 的仓插队**,其余按最久没查的排(probe-release-history.mjs:19-21);旧页 backlog 另按 `advancedAt` 升序(:66),每轮每仓只推一页。
- **monorepo**:stars/updates/tarballs/**releases** 取父 repo(0006 起 stars 经 `repoOf` 去重后批量);npm/readmes/screenshots/**capabilities** 进入子目录。**0007 的 release-history 取父仓并强制小写**(`catalogRepo` → `repoOf(...).toLowerCase()`,lib/release-history.mjs:14-18),同一仓的多条子路径条目因此合并成一个分片(测试第 ⑥ 例专门钉了大小写混写)。
- **写盘前**:按 key localeCompare 排序。**0004 更正**:旧版说"所有脚本都会清理不在列表中的 key"——实际只有 stars/npm/readmes/updates 四个有 `listed` 删除循环(probe-stars.mjs:**92-93**、probe-npm.mjs:**176-177**),**capabilities 只排序不删键**:`const next = { ...stored }`(probe-capabilities.mjs:115)之后没有任何名单过滤,`flush()` 直接对全部键排序写盘(:125-129)。**0006 起清单变五个**:probe-releases 在全量跑(`!selected`)时有删除循环(probe-releases.mjs:**50-53**)。**0007 变六个**:probe-release-history 也有(probe-release-history.mjs:84-87),且它的注释把边界写清了——"partial legacy probe 要保住数据,只有仓真的被下架才删"(:82-83)。

## 各采集器速览

| 脚本 | 目标 API | token | 输出 value 形状 | 特殊点 |
|------|----------|-------|-----------------|--------|
| probe-stars(**133,0006 重写**)| **GraphQL 批量 `repository(…)`(50 仓/查询)** | 需 | `{stars, checkedAt}` | 旧版 `repos/{repo}` REST 每仓一发 + CONCURRENCY=10 并发——**整个文件换芯**:probe 逻辑抽进共享 `repositoryStatistics`,自己只剩增量筛选、README 花名册、写盘与地板;`repoOf` 复用 `lib/probe-updates-graphql.mjs`(monorepo 子目录取父仓);**`checkedAt` 从 `.slice(0,10)` 的 ISO date 变完整 `toISOString()`**——GraphQL 是整仓批量刷新,同一仓里几十个条目共享一次观测,精确到秒才有意义;失败语义不变:该仓不在返回 map 里 → 保留旧值并计数;**66% 地板保留**(:41、:119-120,不写盘 exit);**无重试** |
| probe-npm(**183,0007 +4/−2**)| raw package.json + registry.npmjs.org | 免 | `{npm: name\|null, version: latest\|null, **publishedAt, enginesDsh**, checkedAt}` | **repository 字段回链校验**防冒名;**version 三态**(键缺失/`version:null`/有键);弱值不覆盖强值;**0004** 新增 `publishedAt`(packument `time[latest]` → Unix 秒)+ `enginesDsh`(`versions[latest].engines.dsh`),取自同一份 packument,零额外请求;缺失一律写 `null`(publishFields,:100-111);**0007 改成 `publishedNpmName(repoPath, declaredName)`**(:121)——唯一硬编码例外是 `tests4gptplay/dsh-dots` → `@tests4gptplay/dsh-dots`(lib/npm-name.mjs:4-12),比对的是**全路径**,所以只对仓库根那条生效;下游不再只是 plugins.json,还有 `docs/index.json` |
| probe-downloads(**236**)| npm bulk `point/${start}:${end}` | 免 | `{downloads, checkedAt, **start, end**}` | **0002:相对时间窗 `last-month` 换成显式 UTC 30 天窗**(#5309),`downloadResult` 校验 package/start/end/downloads 四项;批量成功但缺某个名字 → **保留旧计数,绝不写 0**;`fresh()` 也要求 start/end 匹配;unscoped 批量 128/scoped 单发+2s pacing;分 population 双层 66% 地板不变 |
| probe-readmes(**310,0007 +1/−1**)| **raw.githubusercontent.com/HEAD** | **免(冷启动才要)** | `{en?, zh?}`(**`missing` 字段已删**)| **0002 整体重写**:contents API → raw(完全不计 API 配额);批量 GraphQL 目录列举一次拿到 README 与兄弟文件名;`MAIN_NAMES/pickMain/pickSibling`;语言嗅探 CJK>3%;`MAX_BYTES=48KB`;并发 PROBE_ALL 4→**10**;raw() 重试 3 次;**404 也当失败保留旧值**;**0007 只在 `ZH_NAMES`(:54)里补了一个候选 `docs/i18n/README.zh-CN.md`**——那是一条只在"目录列举没给出答案"时才试的兜底路径(:218) |
| probe-updates(**343,0007 +14/−2**)| **GraphQL 批量 releases+commits** + REST 兜底 | 需 | `{release{…}, commits[…], checkedAt}`(**外加顶层内部键 `$releaseHistoryV1`**)| **0002 重写**:一条查询管 50 个仓的**两个事实**;REST `probe()` 保留为"两个字段的度量基准";`readEntries` 会拒绝 null/报错 alias 以及 `isDraft/isPrerelease` 的 latestRelease;限流等待抽成共享 `rateLimitDelayMs`;**冷缓存全失败改 exit(0) 不写盘**(#5731);**0007**:开头读 `map[HISTORY_CACHE_KEY]` 并从 map 里 `delete`(:80-81),写盘前 `sorted[HISTORY_CACHE_KEY] = await collectReleaseHistory(...)`(:335),catch 时回写旧缓存(:336-339),`tmp + rename` 原子写 + 单行 JSON(:340-342),日志计数改用 `have`(:343) |
| probe-tarballs(125,未变)| release 资产 ranged GET(`bytes=0-0`)| 免 | `{tarball, ok(三值), status}` | 用 Range 不用 HEAD;URL 变更不继承旧 verdict;带版本号资产会打"下次发版就坏"预警 |
| probe-screenshots(239,未变)| raw screenshots.json + 图片存活 | 免 | declared/live 两文件 | host 白名单镜像 build-site;相对路径禁 `/` 开头与 `..` |
| **probe-capabilities(230,0002 新增)** | npm tarball / 作者预构建 release / codeload 归档 | 免 | `{version, spec, capabilities[], redLines[], scannedAt, tool, **provenance?**, **previous?**}` | **静态能力披露(#401/#209)**,见下 |
| **probe-releases(55,0006 新增)** | GraphQL 批量 releases(共用 github-statistics)+ raw `package.json` | 需(GitQL);manifest 走 raw 免配额 | `{statistics:{downloads,checkedAt}, manifest:{version,enginesDsh,peerDependencies,tarball,checkedAt}}` | **Release 附件累计下载 + 安装 tag 清单**,写 `data/releases.json`(.gitignore:17);只扫 **GitHub-only 条目**;**0007 仍未接任何 workflow**(`grep -r probe-releases .github/` 为空)|
| **probe-release-history(90,0007 新增)** | GraphQL `releases(first:12, orderBy:{field:CREATED_AT, direction:DESC})` + `tagCommit{oid}` | 需(复用 probe-updates 的 token) | 每仓 `{releases[], next, fallback?, started, checkedAt, advancedAt, stamp, headCursor, headCount}` | **不新建 workflow**:probe-updates 尾部调用;**30 仓/查询、240 查询/轮**、每仓 ≤256 条、正文截 4 KB;失败**整仓作废**、配额见底**暂停整轮**;落 `updates.json` 的内部键,再由 build-site 拆成分片(见下节与 [03](./03-publish-layer.md))|

## probe-capabilities:把"碰了什么"变成可核对的事实

- **它做什么**:把**用户实际会装到的产物**下载下来(优先级:npm tarball > 作者预构建 tarball > codeload `github:<repo>@HEAD`,lib/capabilities.mjs:75-100),交给 `dsh-trust-check` 静态扫描;子路径条目**在子目录扫描**,因为那才是用户拿到的包(扫 monorepo 根会把兄弟包算进来)。
- **十种能力**:`fs-read / fs-write / env / network / shell / credentials / llm / dynamic-code / host-runtime / subagent`。这十个名字不是抄来的清单,而是现文件里实际出现的全部取值(3843 条时的统计):fs-read 2882、fs-write 2261、env 2206、network 2183、shell 1634、credentials 454、llm 348、dynamic-code 347、host-runtime 296、subagent 87。redLines 是**句子的列表**,如 "reads credentials/secrets AND has network access"、"runs code at install time (postinstall)"。
- **披露而非判决(#209 原话)**:脚本头写着 "The facts are DISCLOSURE, never a verdict";`lib/capabilities.mjs` 的 `factsFromScan` **刻意丢掉** `score`/`band`/`verdict`(:122-128 的注释与 :176-183 的白名单),好让"没有任何界面能把这个插件渲染成绿色,连意外都不行"。未扫到的条目**不在文件里**,界面渲染成"未检出"——"我们没能看"和"我们看了什么也没看到"是两句不同的话。
- **0004 新增 `provenance`:存在但未验签**。对 npm 来源且版本已知的条目,探针额外问一次 registry 的 attestation:先 `import('dsh-trust-check')` 拿 `readNpmProvenance`,再把扫描输出里声明的 `repository` 传进去做比对(probe-capabilities.mjs:84-93、167-170)。`lib/capabilities.mjs:215-224` 的 `copyProvenance` 只保留**一种形状**:`present` 必须是布尔、`signatureChecked` 必须是 `false`,输出固定写 `signatureChecked: false`,外加 `repository`/`commit`/`ref` 与 `repositoryMatches`。所以这条字段的准确读法是"**有来源证明,但我们没验签**";如果将来扫描器开始验签,这段代码会**整条丢掉**该字段——保守,但代价是"验过的"和"没问"在数据里长得一样。`repositoryMatches` 与 probe-npm 的 repository 回链是同一条纪律。
- **0004 新增 `previous`:一步记忆,不是历史**。`rememberPrevious`(:197-213)只在"存的版本与新扫的版本**都已知且不同**"时写入 `{version, capabilities, redLines}` 三样,同版本重扫保留原来的 `previous`(不指向自己),分支源永远不会产生 `previous`。再换一版会**覆盖**上一份;而且它**不带 `scannedAt`**。
- **0004 新增 `capability-changes.mjs`:一个没有生产者的仪表**。44 行,只读 `data/capabilities.json`,筛出带 `previous` 的记录统计 `{records, withPrevious, capabilityChanged, redLineChanged, added}`;没有任何 workflow 调用它,`package.json` 连 `scripts` 字段都没有。**仪器的前提是一条并不存在的数据流**——现文件 3805 条里 `previous` 仍 0 条。
- **0004 新增:compare-only 的字面 IP 不算外联**。scanner 0.2.1 的 `redLines` 里有一类 "uses literal IP <addr> for network access",由字符串匹配生成;而 SSRF 防护里 `host === '100.100.100.200' → throw` 这种**比较**读起来和真的外联一模一样。`dropCompareOnlyIpRedLines`(:149-165)用的是扫描器自己的分类:`destinations[]` 里 `kind === 'ip'` 且**每个** site 的 `usage` 都是 `compare` 才删这条 redLine。真实案例是 `MeteorNOX/DeepSeek-Balance-Whale-Widget`(#8140)。这条过滤只对 0.2.1 的输出生效——存量数据里仍有记录带着 "uses literal IP …" 的 redLine。
- **增量与失败**:按 release 版本失效,无版本的引用 7 天后过期(lib/capabilities.mjs:114-120;`RECHECK_DAYS` 默认 7,probe-capabilities.mjs:96);每 100 条 flush 一次(可续跑);子进程用异步 execFile(:106);**失败什么都不写**,保留旧记录。但 provenance 走的是**进程内 import**,没有 `node_modules` 时它会静默缺席(:84-93 的 catch),扫描本身则退回 `npx`(:61)——所以同一个 checkout 在有/无依赖两种状态下产出的记录形状不同,日志里都不会有差别。
- **扫描器版本(0004 重写)**:`package.json:25` 是 `^0.2.1`(区间),`package-lock.json` 钉到 **0.2.1**;代码读的是 **schemaVersion**,而它已经不是一个数:`SCANNER_SCHEMA = 2`、`READABLE_SCHEMAS = {1, 2}`(lib/capabilities.mjs:25-26),schema 3 返回 null。现文件里 3805 条仍全写 `tool: dsh-trust-check@0.1.13`,而代码默认早就是 0.2.1(`TOOL` 常量,probe-capabilities.mjs:47)——`tool` 记的是这次 run **宣称**用了哪个扫描器,真实二进制来自 node_modules 或 npx。(`SCANNER_SCHEMA` 在 probe-capabilities.mjs:42 已是未用导入,只被测试引用。)
- **谁调用**:build-site.yml:**245** 每次构建都跑(不在 PROBE_ALL 门控里);产物 `data/capabilities.json` → `docs/plugins.json` 的 `capabilities/capabilityRedLines/capabilityCheckedAt`(build-site.mjs:**475-476**、1173-1174)。注意它**只**透传这三样:`provenance` 与 `previous` 在 build-site 里没有任何读者,也没有进 `docs/index.json`。
- **快照口径(0004 实测,现文件已缩到 3805 条)**:3843 条记录、453 条带 redLine(11.8%)、353 条命中"既读凭据又有网络访问";与 0002 的 454/354 各差 1,差的正是 2026-10-20 删掉的那条记录(oauth-subs,1a93fa18f),另有一条记录在同日被手工删掉一行字面 IP 的 redLine(0355e74b5)。**这两处手工修改是 0004 期间这份文件的全部变化**——没有一条记录被重扫。

## 0006 新增(历史):Release 探针家族(github-statistics / probe-releases / release-manifest)

> 本节三个文件在 0007 全部零行 diff,结论原样有效;只把读到的行号按当前 checkout 校正(probe-releases 的删除循环 :50-53、build-site 的 `releaseMetadataFor` 调用 :469)。

### `lib/github-statistics.mjs`(69 行):批量 GraphQL 的共享库

- **常量与分页形状**:`REPOSITORIES_PER_QUERY = 50`(:3,与 probe-updates 同一个数);release 资产分页是**两级**的——releases 连接 `first: 10`(:4),每个 release 的 `releaseAssets` 连接 `first: 100`(:5)。`statisticsQuery(tasks, releases)`(:7-12)把一批任务拼成一条带别名(`r0..r49`)的查询。
- **`repositoryStatistics(repositories, request, {releases})`(:15-64)是唯一的执行体**:每仓状态 `{stars: null, downloads: 0, assets: Set, releases: Set, cursors: Set, failed: false}`;输入先 `[...new Set(repositories)]` 去重;每轮取 50 个未失败任务;`request` 抛错 → **该批 50 个全部标 failed**,continue——不是重试,是放弃这一批。
- **任何一页缺失/失败 → 整仓作废,不取部分和**(:41-63):GraphQL errors 命中本别名、value 缺失、`isPrivate !== false`(**私有仓直接作废**)、pageInfo 缺 hasNextPage、hasNextPage 而无 cursor、**cursor 重复**、资产缺 id / downloadCount 非负安全整数 / 资产 id 重复、累计和溢出安全整数、release 缺 id / isDraft 非布尔 / release id 重复——每一条都 throw 进同一个 catch。失败仓**根本不在返回 map 里**,让调用方沿用"不在 map = 保留旧值"的语义。
- `stars ??= value.stargazerCount`;`isDraft` 的 release **计入 release 去重但跳过资产**(:57-59);prerelease 不跳。零下载是合法事实。测试 `github-statistics.test.mjs`(55 行,**3 个 `test()`**,覆盖 9 类情形)。

### `scripts/probe-releases.mjs`(55 行):两个事实一个文件

- **花名册是 YAML 不是 README**:`readEntries().filter(entry => entry.tarball && !npm[entry.url]?.npm)`(:13)——只有"作者声明了 Release tarball 且没有 npm 包"的 GitHub-only 条目才进名单;支持 `--repo=owner/repo` 单仓复跑。
- **增量判据**:`stale()` = `PROBE_ALL=1`,或 `checkedAt` 解析不了,或距今 ≥86400000ms(24h,写死,无环境变量旋钮);**manifest 的增量判据是另一条**:`stored.manifest?.tarball === entry.tarball` 即跳过——作者换 tag 才触发重读,**与时间无关**。
- **统计侧**:token 缺失只打日志、`stats` 保持空 map——**没有 token 不算失败**;请求 30s 超时。fresh 值 `{downloads, checkedAt: now}` 是本次 run 的完整 ISO 时间戳。
- **manifest 侧**:解析出 raw 地址后 fetch(15s),**流式读 body 并在累计超过 1 MiB 时 throw**;任何一步失败只 `failed++` 并保留旧 manifest。并发 6。
- **失败纪律**:注释原话 "A failed probe preserves the last complete observation and its original time"——**时间戳跟着各自的值走**。
- **删撤**:`!selected` 时(全量跑)把不在当前名单的键删掉(**probe-releases.mjs:50-53**);`--repo=` 单仓复跑刻意不删。
- **写盘**:`JSON.stringify(…, null, 1)` + 按 key localeCompare 排序。
- **没有 CI 接线(0007 复核仍无)**:**当前 checkout 里没有任何 workflow 调用它**(`grep -r probe-releases .github/` 为空),`data/releases.json` 也不在任何 cache path 上——**它仍只活在维护者本机**,与 capability-changes 同属"有代码、有消费者、无生产调度"一族。contributing.md 那句 "counts refresh daily through a separate cache" 与工作区代码不符(上游私有环境或计划态,记为待复核)。

### `scripts/lib/release-manifest.mjs`(37 行):锁定声明 tag,绝不换 latest

- **`releaseManifestUrl(entry)`(:3-13)**:两条正则,一条解 `entry.url`,一条解 `entry.tarball`(**必须**是 `releases/download/<tag>/<file>.tgz|.tar.gz` 的固定 tag 形态)。仲裁:owner/repo 不一致 → null;`releases/latest/download/…` → null(**绝不替换成仓库 latest**);`%2E%2E` 解码出 `..`/反斜杠/超长 tag → null。monorepo 子目录条目读的是**子目录里的** `package.json`。
- **`releaseManifestFacts(value)`(:16-21)**:白名单提取。硬校验三条:name 是 string、version 非空 ≤256、**`dsh.bundle` 存在**。提取 `version`、`enginesDsh`(**两级回退** `engines.dsh ?? dsh.engines.dsh`)、`peerDependencies` **只留 `@deepseek-ai/*`**;`scripts.postinstall` 等一切可执行字段根本不进返回值——"never runs package code" 是结构保证。
- **`releaseMetadataFor(entry, stored)`(:24-34)**:build-site 每条目调用的仲裁口(**build-site.mjs:469**)。三重条件(有 tarball && 缓存清单的 tarball 与当前一致 && URL 现在仍解析得出)任一不满足,`releaseManifest` 键整个不产生。
- **测试 `release-manifest.test.mjs`(31 行)**。

### 消费口径(contributing.md 0006 新节,+10 行)

npm 30 天滚动 `downloads` 与 `githubReleaseDownloads`(公开仓库 Release 附件**累计**,含 prerelease 不含 draft;是下载事件,不是安装数/用户数)**必须分开标注、不得相加、不得放进同一窗口排序**;探测失败保留上次完整计数与原时间戳,**未知不写成零**;`starsCheckedAt`/`githubReleaseDownloadsCheckedAt` 标识观测时刻而非消费时刻;GitHub-only 条目的 `version`/`releaseManifest` 出自所选 tag 的 `package.json`,消费方必须核对 `releaseManifest.tarball` 与当前安装地址一致才可信;探针不执行包代码。

## 0007 新增:Release 历史(github 上没有第二个入口)

### `scripts/probe-release-history.mjs`(90 行):入口写在别人的文件里

- **不新建 workflow**:`probe-updates.mjs:52-53` 导入 `collectReleaseHistory`,并在写盘前调用(:334-339)。CI 里对应的仍只是 `node scripts/probe-updates.mjs`(build-site.yml:222)——**"挂尾巴"是这次唯一的接线方式**,没有新的 job、没有新的 cache 条目、没有新的 cache path。
- **名单 = 上一轮的 release 集合**:遍历 `updates`,只收 `catalogRepo(url) !== null && entry.release?.tag`(:15-18);键是**小写父仓**,值是 `tag:publishedAt` 的 **stamp**。
- **排序靠 stamp**:`checked(repo, stamp)` 只在缓存里的 stamp 与当前一致时返回 `checkedAt`,否则 0(:19)——换了头页 release 的仓自动排前,其余按最久没查的排;`pending` 全量排序后按 `BATCH` 切批(:20-21)。
- **两段预算**:常量 `BATCH = 30`、`QUERY_BUDGET = 240`、`RECENT_QUERY_BUDGET = 210`、`QUOTA_RESERVE = 50`(:7-10)。近期页循环最多 210 次查询(6300 仓-页,:52);旧页 backlog 吃剩余预算(`queries < QUERY_BUDGET`,正常最多 30 次;每次 30 仓,即最多约 900 个旧页/轮,:67-81)。
- **暂停语义**:`getPages` 先查预算,再查 `remaining < QUOTA_RESERVE`(:26);fetch 带 15s `AbortSignal.timeout`(:38),任何异常(超时/HTTP/`data:null`)**只 warn 一行并返回 null**(:46-49)→ 外层把 `paused` 置真并 **break**(:55、:72):不重试、不 exit,已拿到的留着。`x-ratelimit-remaining` 每查更新一次(:40-41)。
- **旧页推进**:`canAdvance` = 有 `next` 且条数未到 `MAX_RELEASES`(:64);backlog 按 `advancedAt` 升序(:66);每仓每轮只推一页,`page.next === after`(游标没动)视为无进展跳过(:75)——防服务端原地打转。
- **名单清理**:`listed` = **全部** `updates` 键的 catalogRepo,:84-87 删掉不在里面的仓;注释写明"partial legacy probe 要保住数据,只有仓真的被下架才删"(:82-83)。
- **只返回、不写盘**:落盘由 probe-updates 负责,所以它没有自己的文件、没有自己的地板、也没有自己的 cache。
- **日志一行**:`release history: X/Y repositories, Z queries`(:88)——X 是写回去的仓数,Y 是本轮有 release 的仓数。

### `scripts/lib/release-history.mjs`(144 行):每仓一个游标、一份分片

- **常量**:`HISTORY_CACHE_KEY = '$releaseHistoryV1'`(:7)、`RELEASES_PER_PAGE = 12`(:8)、`MAX_RELEASES = 256`(:9)、`MAX_FILE_BYTES = 1_048_576`(:10)、`MAX_BODY_BYTES = 4096`(:11)、`REVALIDATE_MS = 7 × 24h`(:12)。
- **`catalogRepo(url)`(:14-18)**:只认 `https://github.com/`,取 `repoOf` 后**转小写**,`/^[a-z0-9-]+\/[a-z0-9_.-]+$/` 校验,并显式排除以 `/.`、`/..` 结尾——**路径穿越闸**,与 `release-manifest.mjs` 的 `%2E%2E` 闸同族。小写化让分片名与"同一仓不同子路径条目"归一。
- **`historyQuery(batch)`(:21-33)**:一条查询、每仓一个 alias `r{i}`、**每仓独立 `after`**(`JSON.stringify` 生成字面量,首轮是 `null`);`orderBy: {field: CREATED_AT, direction: DESC}`;字段 `tagName name publishedAt url description isDraft isPrerelease tagCommit { oid }`。**注意是 CREATED_AT 而非 PUBLISHED_AT**:作者补发的旧 release 会插进头页,这正是"头页必须判重叠"的原因。
- **`boundedBody`(:35-43)**:先 `Buffer.byteLength`;超 4096 就从 4096 往回退,退到不是 UTF-8 续字节(`(bytes[end] & 0xc0) === 0x80`)为止,再 `subarray(0, end).toString('utf8') + '\n\n…'`——**截断后上限 4101 字节**(4096 + `\n\n…` 的 5 字节;测试断言 `<= 4101`),标记与 0006 的 latest-release 快照同一个。
- **`readHistoryPages(payload, batch)`(:45-63)**:先收 `payload.errors[].path[0]` 进 `failed`;逐 alias 取 `data[alias].releases`,四条验收(无 error、`nodes` 是数组、`pageInfo` 在、`hasNextPage` 是布尔且翻页必有 `endCursor`)任一失败就 **continue**;**失败只作废单仓**,不污染同批其他仓(与 0006 `github-statistics` 的"整批 50 个作废"相反);`filter` 只留 `isDraft === false && isPrerelease === false` 且 `tagName` 为 ≤256 字符串;`commit` 取 `tagCommit.oid`(可能为 null)。
- **`refreshHistory(previous, page, stamp, now)`(:68-95)** 是全库最绕的一段:
  - 重叠判定用 **`tag` 与 `commit` 双字段**(:70-71)——只对 tag 不算,作者可以强推同名 tag;`index < 0` 即"头页与旧尾接不上"。
  - `boundary`:旧 `headCursor === page.next`(头页没翻页)时用 `headCount`,否则 `index + 1`(:71)。
  - `appendOld` 三重条件:`page.next !== null`(还有旧页)、`boundary != null`(能续接)、`now - previous.started < REVALIDATE_MS`(:72)。满足就拼 `[...page.releases, ...previous.releases.slice(boundary)]`——**头页取新值,旧尾原样接上**(作者改过的旧 release 正文要等 7 天重扫才会更新)。
  - **7 天到点就整段重扫**:`appendOld` 为假 → 只用 `page.releases`,把旧列表存进 `fallback`(:79-83),条件是"头页还有下一页 && (旧缓存没有待续 next 或已顶到 256)"。`publishReleaseHistory` 优先读 `fallback`(:118),所以**重扫期间站点继续看到上一版完整历史**,不会突然缩短。
  - `headCursor/headCount` 记"头页翻到哪、几条"(:87-88);`started` 只在重扫时重置(:90);`checkedAt` 每轮更新、`advancedAt` 只由旧页推进改(:91-92);`stamp` 存本轮头页标识(:93)。返回前 `slice(0, MAX_RELEASES)`,`next === null` 或已满 256 时**主动清掉 fallback**(:89)。
- **`extendHistory(previous, page)`(:97-107)**:按 **tag** 去重追加(`filter` 掉已有 tag);满 `MAX_RELEASES` 时**保持旧游标**(:100)——停止前进,而不是悄悄丢溢出的页。
- **`publishReleaseHistory(entries, histories, directory, budget)`(:111-144)**:遍历 `entries`(build-site 传全名单 `ordered`)取 `catalogRepo`,同仓只写一次(`new Set`);源 = `history.fallback ?? history.releases`(:118);信封预算从 `128 + repo 名长度` 起算,逐条 `JSON.stringify` 累加,超 `MAX_FILE_BYTES` 或满 256 条就停(:121-127);`complete = 无 fallback && next === null && 条数等于源长度`(:129);写 `<dir>/release-history/v1/<owner>/<repo>.json`(:136-139);**总预算超了 `skipped++` 且不写文件、不计入 `repositories`**(:132-135)。
- **测试 `release-history.test.mjs`(118 行,7 例)**:①每仓独立游标 + 只收稳定 release + 4 KB 截断落在 UTF-8 边界(断言 ≤4101 字节);②新 release 出现后旧尾仍保留、7 天后过期重扫、`fallback` 生效与清空;③头页只有 prerelease 时不清空已有历史;④顶到 256 上限时保留已发布历史等重扫;⑤配额见底(`x-ratelimit-remaining: 49`)只发一次查询就停;⑥一个分片、大小写混写的子路径归并、<1 MB、`complete: false`;⑦总预算超限时不写第二份、`skipped = 1`、`publishedBytes ≤ budget`。
- **消费侧(0007 实测缺口)**:在源码目录(`site/`、`.github/`、`data/`、`contributing.md`)里 `releaseHistory` / `release-history` **零命中**——`site/` 里没有任何代码读 `docs/updates.json` 的 `releaseHistory` 标记或 `release-history/v1/` 下的分片,contributing.md 也没有对应段落。**产出链路完整、消费端尚不存在**(见 [03](./03-publish-layer.md) 与"待复核")。

## gh() 封装与限流(0002 后,0006/0007 部分被取代)

- probe-readmes **不再有 gh()**(改走 raw,免配额)。
- probe-updates 保留一份 gh(),其限流算法抽进 `lib/probe-updates-graphql.mjs:rateLimitDelayMs`;15s 超时;403/429 时 `retry-after` 优先,否则按 `x-ratelimit-remaining==='0'` + reset 精确等待;单次等待上限 120000ms;等待后递归重试。更精的兄弟仍在 check-submission.mjs(区分权限型/限流型 403、双层预算 75s/150s)。
- **配额经济学(0002;0006 重写其一)**:`raw.githubusercontent.com` 不计 API 配额;GraphQL 一次查询 50 仓;REST 两查/仓是旧的失败模式(夜间 3334 仓首轮失败即此)。**0006**:probe-stars 的 REST 单发也是同一个病——Actions token 每小时 ~1000 请求**与全部 workflow 共享**,全量探 ~1300 仓一次就打爆自己的预算;修法不是调参而是换协议:改走"50 仓/查询"的批量 GraphQL,注释压成一句 "One REST request per entry exceeds the Actions token's hourly budget"(probe-stars.mjs:63-64)。
- **0007 的配额账(第三种写法)**:release-history 一条查询 **30 仓 × 12 条 release**,1 个 GraphQL 点;240 次/轮 ≈ 7200 个"仓-页"。近期页上限 210 次(6300 仓)保最新,**剩下的 30 次留给等得最久的旧页**;`x-ratelimit-remaining < 50` 立刻暂停,把 50 点让给别的探针。它把预算写成**脚本内常量**,不受 `PROBE_BATCH`/`PROBE_RECHECK_DAYS` 之类环境变量影响——这既是保护(不会被一次误设放大十倍),也是硬伤(调参要改代码)。
- **0004 的一处反向依赖**:capability 探针不再只把扫描器当子进程,provenance 需要**同一个包被 import 进来**(probe-capabilities.mjs:86)。这把"扫描器版本"从"命令行字符串"变成了"依赖安装状态",而它的失败模式是静默的。

## 第二遍重试(readmes/updates 不再同构)

- readmes:首遍批量失败 → sleep 20000ms → 逐个串行重探(0002 起失败含义是"保留旧值")。
- updates:重试**按批**进行(每批 50 仓、批间 250ms),不再逐仓串行(:284-295)。
- **0004 补一条边界**:probe-npm **没有重试**。它的失败语义是"返回 null,保留旧值"(probe-npm.mjs:138-139),三条 pass 各自 8 并发分批串行;唯一会把"未知"写下去的地方是首见即失败的那个兜底(:165)。
- **0007 补一条边界**:release-history **也没有重试**。`getPages` 一次失败就暂停整轮(probe-release-history.mjs:46-49),下一轮靠 `checked`/`advancedAt` 排序自然轮到它——它用**轮转**代替重试。

## 地板门的三种变体(0002 修正)

| 脚本 | 判定对象 | 不过的动作 |
|------|----------|-----------|
| probe-stars | 结果 map(磁盘已有数据)/ 全部条目 | exit(1),不写盘(#1673 的 1362×null 教训;0006 重写后地板仍在 :41、:119-120)|
| probe-downloads | 分 population + 总体,双 66% | 同上 |
| probe-updates | 无覆盖率地板 | **exit(0) 且不写盘**(0002 从 exit 1 改;cache-save 只在成功时跑,#5731)|
| probe-capabilities | 无地板 | 失败条目**保持缺席**(未检出),旧记录保留;整轮全失败 exit(0) 并保留旧文件(probe-capabilities.mjs:222-229)|
| probe-readmes | 无 | 只汇报失败 URL 及其中多少 NEW(会渲染空白页),列前 20 |
| probe-releases(0006) | 无地板 | 无 token/无数据时照常写盘(保留上次观测);单条失败只计数;**删撤只发生在全量跑**(`!selected`)|
| **probe-release-history(0007)** | 无地板(它没有独立文件) | 配额见底/查询失败 → **暂停整轮**并保留已拿到的部分;`collectReleaseHistory` 抛错由 probe-updates catch 住并回写旧缓存(probe-updates.mjs:334-339);**单仓**失败只让该仓本轮不更新 |

「判定对象是已有数据而非本次成功数」这个细节容易看漏:即使本轮全失败(ok===0),只要磁盘上存量仍 ≥66%,探针打印 "left as-is" 并 exit(0)——**保护的是数据的连续性,不是本轮的成就感**。**0007 有一个新副作用值得记下**:release-history 的调用点在 probe-updates 的两条 `exit(0)` 之后(probe-updates.mjs:324-331),所以"整晚探针全失败"或"冷缓存且全失败"的那一夜,**连历史也不推进**——文件不写,缓存里的 `$releaseHistoryV1` 就还是上一版。

## 待复核

- [x] ~~probe-readmes 是否存在把 broken repo 写成 missing 的边缘~~ → **该字段已被删除**,问题消失(0002)
- [x] ~~capabilities.json 既不回写、也不进 cache——夜间的重扫结果是否只活在那次 run 的 plugins.json 里~~ → **代码路径已回答**(0004):是。build-site.yml:245 每次构建都跑,权限 `contents: read`(:49),cache path 不含它(:112-120),所以重扫只进那次 run 的 `docs/plugins.json`,永不回仓库。剩下的已经不是"是不是",而是"要不要"。
- [ ] **0004 新增**:`previous` 的仪器目前空转——没有 CI 生产者、没有第二个消费者、存在量 0/3805。要让"版本间能力变化"有意义,得先决定重扫结果落在哪里。
- [ ] **0004 新增**:存量记录里仍带 "uses literal IP …" 的 redLine,其中多少其实是 `usage: compare`(新过滤器会清掉)无法从冻结文件判断,要等一次全量重扫。
- [ ] `PROBE_RECHECK_DAYS` 在 push build 上实际等于永远 fresh(cache 保留了 checkedAt),确认无叠加效应
- [ ] **0006 新增**:probe-stars 的 `checkedAt` 已是完整 ISO timestamp,但仓库里 `data/stars.json` 存量值仍是旧格式(date 或旧 timestamp);`fresh()` 用 `Date.parse` 两种都能读,混存无害,但"仓库地板 vs cache 新副本"的时间跨度读数要等一次 nightly 全量重探才统一
- [ ] **0006 新增**:probe-releases 无 CI 接线(**0007 复核仍无**),`data/releases.json` 的生产/缓存路径待上游补;在此之前 build-site 的 GitHub-only version 兜底与 `githubReleaseDownloads` 字段在实际构建中恒缺席
- [ ] **0006 新增**:`github-statistics` 对 request 抛错整批(≤50 仓)作废、不重试;夜间一次配额抖动会作废多少仓、次日能否自愈,无 CI 日志可查(UNVERIFIED)
- [ ] **0002 新增**:downloads 的 start/end 迁移会让旧快照的 624 行全部失效、首轮重探全部已发布条目——尚未对 CI 日志确认
- [ ] **0007 新增**:`docs/release-history/v1/` 的**消费方不存在**(`site/` 里零命中)。这是"有生产者、有产物、无站点消费者",与 0006 的 probe-releases(有消费者、无生产者)刚好互为镜像;要等站点侧接线才能判断分片形状够不够用。
- [ ] **0007 新增**:256 条上限 + 7 天重扫叠加时,历史长于 256 条的仓每 7 天会把 `fallback` 重播一遍;而 `fallback` 只有 `started` 一个隐含时期,下游分不清"这一版是新的"还是"正在重扫"。
- [ ] **0007 新增**:Release 历史只收 `isPrerelease === false`,而 `githubReleaseDownloads` 是**含 prerelease** 的累计下载——两个数字出现在同一个详情页时口径不同,是否会被读者相加**未核验**(没有任何文档约束)。
- [ ] **0007 新增**:`collectReleaseHistory` 只在 probe-updates 真正写盘时被调;**配额耗尽夜的 historical 新鲜度没有 CI 日志可查**(该 job 在本 fork 上还被 fork 门挡掉,build-site.yml:78)。
