# 01 · probe 家族:十个采集器的机制参考(8 个 probe-* 脚本 + scan-decay + prune-legacy-screenshots)

> 基线:`upstream@b4d0049a8`(0004 复核,2026-10-24)。**这是 0002 之后第一次实质改动**:probe-capabilities 200→**230**(+`lib/capabilities.mjs` 144→**224**、新增 `capability-changes.mjs` 44、`capabilities.test.mjs` 111→**192**)、probe-npm 150→**181**;stars(142)/downloads(236)/readmes(310)/updates(331)/tarballs(125)/screenshots(239)六个探针与 scan-decay、prune、publish-updates 零 diff。行号为脚本内行号。

## 公共行为模式

- **花名册来源**:tarballs/screenshots/capabilities 三个直接 `readEntries()` 消费 YAML,其余解析 `README.md` 的条目行(`/^- \[.+?\]\((https:\/\/github\.com\/[^)]+)\) [—-] /`)——README 仍是多数探针眼里的注册表视图。
- **增量判据**:`fresh()` = 非 PROBE_ALL 且已有值且 checkedAt 在 `PROBE_RECHECK_DAYS`(默认 1,readmes 例外默认 7,capabilities 7)天内。probe-npm 的 `version` 字段只靠 nightly `PROBE_ALL` 全量刷新;unpublished 每天复查。**0004 新增三条通道**:probe-npm 现在是 full probe / version-backfill / publish-backfill 三条 pass 串行(probe-npm.mjs:78-80、170-172),后两条都是"键在即不再触发"的一次性回填——其中 publish-backfill 是 0004 才有的(:70-76)。
- **公平调度(0002 新增)**:`lib/probe-order.mjs` 的 `leastRecentlyChecked(urls, map)` 按 `checkedAt` 升序排、并列保持 README 顺序,已被 probe-updates 采用(:257)。动机是实测:2026-09-14 的 nightly `3632 listed … 2364 repo(s) kept their previous update data`,README 位置 40–80% 的条目最后检查时间停在 09-05——**预算被砍的一轮会把同一段列表饿死**(#5149)。
- **monorepo**:stars/updates/tarballs 取父 repo;npm/readmes/screenshots/**capabilities** 进入子目录。
- **写盘前**:按 key localeCompare 排序。**0004 更正**:旧版说"所有脚本都会清理不在列表中的 key"——实际只有 stars/npm/readmes/updates 四个有 `listed` 删除循环(probe-stars.mjs:101-102、probe-npm.mjs:174-175),**capabilities 只排序不删键**:`const next = { ...stored }`(probe-capabilities.mjs:115)之后没有任何名单过滤,`flush()` 直接对全部键排序写盘(:125-129)。现文件里仍有 51 个键指向已不在名单的 URL,就是这条的产物;已失效的记录只能人手工删——oauth-subs 那条就是 2026-10-20 手工删掉的(1a93fa18f,#8058)。

## 各采集器速览

| 脚本 | 目标 API | token | 输出 value 形状 | 特殊点 |
|------|----------|-------|-----------------|--------|
| probe-stars(142,未变)| `repos/{repo}` | 需 | `{stars, checkedAt}` | 无重试;失败保留旧值;有地板 |
| probe-npm(**181**)| raw package.json + registry.npmjs.org | 免 | `{npm: name\|null, version: latest\|null, **publishedAt, enginesDsh**, checkedAt}` | **repository 字段回链校验**防冒名;**version 三态**(键缺失/`version:null`/有键);弱值不覆盖强值;**0004 新增**:`publishedAt`(packument `time[latest]` → Unix 秒)+ `enginesDsh`(`versions[latest].engines.dsh`),取自它本来就已抓的同一份 packument,零额外请求;缺失一律写 `null`,"已知为空"与"尚未回填"因此可区分(:91-110、:130-135);下游不再只是 plugins.json,还有 `docs/index.json` |
| probe-downloads(**236**)| npm bulk `point/${start}:${end}` | 免 | `{downloads, checkedAt, **start, end**}` | **0002:相对时间窗 `last-month` 换成显式 UTC 30 天窗**(#5309),`downloadResult` 校验 package/start/end/downloads 四项,不符即抛"Missing, invalid, or stale npm download response";**批量成功但缺某个名字 → 保留旧计数,绝不写 0**;`fresh()` 也要求 start/end 匹配;unscoped 批量 128/scoped 单发+2s pacing;分 population 双层 66% 地板不变 |
| probe-readmes(**310**)| **raw.githubusercontent.com/HEAD** | **免(冷启动才要)** | `{en?, zh?}`(**`missing` 字段已删**)| **0002 整体重写**:contents API(≤4 次 REST/仓,夜间 `3334 repo(s) failed the first pass`、约九成页面陈旧)→ raw(完全不计 API 配额);批量 GraphQL 目录列举(50 仓/查询/1 点)一次拿到 README 与兄弟文件名,取正文只需 1–2 次请求(初版"猜文件名"跑了 40 分钟被取消);`MAIN_NAMES/pickMain/pickSibling`;语言嗅探 CJK>3%;`MAX_BYTES=48KB` 不变;并发 PROBE_ALL 4→**10**(旧 4 是给 REST 定的);raw() 重试 3 次(1500·2ⁿ ms);**404 也当失败保留旧值**,不再写 `missing:true`;token 现在只是"冷启动就退出"的闸门 |
| probe-updates(**331**)| **GraphQL 批量 releases+commits** + REST 兜底 | 需 | `{release{…}, commits[…], checkedAt}` | **0002 重写**:一条查询管 50 个仓的**两个事实**、只花 1 点(全列表 ~75 点 / 1000 每小时);动机是 2026-09-16 的夜间跑(`3727 listed … 2594 failed the first pass`,文件三分之一停在 09-05,#5275/#5317);REST `probe()` 保留为"两个字段的度量基准";`readEntries` 会拒绝 null/报错 alias 以及 `isDraft/isPrerelease` 的 latestRelease(端点没承诺这些语义),退回 REST(CONCURRENCY=8);限流等待抽成共享 `rateLimitDelayMs`,403/429 与 GraphQL HTTP-200-`data:null` 都等;重试按批(250ms/批);**冷缓存全失败改为 exit(0) 不写盘**(#5731) |
| probe-tarballs(125,未变)| release 资产 ranged GET(`bytes=0-0`)| 免 | `{tarball, ok(三值), status}` | 用 Range 不用 HEAD;URL 变更不继承旧 verdict;带版本号资产会打"下次发版就坏"预警 |
| probe-screenshots(239,未变)| raw screenshots.json + 图片存活 | 免 | declared/live 两文件 | host 白名单镜像 build-site;相对路径禁 `/` 开头与 `..` |
| **probe-capabilities(230,0002 新增)** | npm tarball / 作者预构建 release / codeload 归档 | 免 | `{version, spec, capabilities[], redLines[], scannedAt, tool, **provenance?**, **previous?**}` | **静态能力披露(#401/#209)**,见下 |

## probe-capabilities:把"碰了什么"变成可核对的事实

- **它做什么**:把**用户实际会装到的产物**下载下来(优先级:npm tarball > 作者预构建 tarball > codeload `github:<repo>@HEAD`,lib/capabilities.mjs:75-100),交给 `dsh-trust-check` 静态扫描;子路径条目**在子目录扫描**,因为那才是用户拿到的包(扫 monorepo 根会把兄弟包算进来)。
- **十种能力**:`fs-read / fs-write / env / network / shell / credentials / llm / dynamic-code / host-runtime / subagent`。这十个名字不是抄来的清单,而是现文件里实际出现的全部取值(3843 条统计):fs-read 2882、fs-write 2261、env 2206、network 2183、shell 1634、credentials 454、llm 348、dynamic-code 347、host-runtime 296、subagent 87。redLines 是**句子的列表**,如 "reads credentials/secrets AND has network access"、"runs code at install time (postinstall)"。
- **披露而非判决(#209 原话)**:脚本头写着 "The facts are DISCLOSURE, never a verdict";`lib/capabilities.mjs` 的 `factsFromScan` **刻意丢掉** `score`/`band`/`verdict`(:122-128 的注释与 :176-183 的白名单),好让"没有任何界面能把这个插件渲染成绿色,连意外都不行"。未扫到的条目**不在文件里**,界面渲染成"未检出"——"我们没能看"和"我们看了什么也没看到"是两句不同的话。
- **0004 新增 `provenance`:存在但未验签**。对 npm 来源且版本已知的条目,探针额外问一次 registry 的 attestation:先 `import('dsh-trust-check')` 拿 `readNpmProvenance`,再把扫描输出里声明的 `repository` 传进去做比对(probe-capabilities.mjs:84-93、167-170)。`lib/capabilities.mjs:215-224` 的 `copyProvenance` 只保留**一种形状**:`present` 必须是布尔、`signatureChecked` 必须是 `false`,输出固定写 `signatureChecked: false`,外加 `repository`/`commit`/`ref` 与 `repositoryMatches`。所以这条字段的准确读法是"**有来源证明,但我们没验签**",而不是"可信";如果将来扫描器开始验签(`signatureChecked: true`),这段代码会**整条丢掉**该字段——保守,但代价是"验过的"和"没问"在数据里长得一样。`repositoryMatches` 与 probe-npm 的 repository 回链是同一条纪律:attestation 指向的仓库要和条目声明的仓库对得上。
- **0004 新增 `previous`:一步记忆,不是历史**。`rememberPrevious`(:197-213)只在"存的版本与新扫的版本**都已知且不同**"时写入 `{version, capabilities, redLines}` 三样,同版本重扫保留原来的 `previous`(不指向自己),分支源(version 为 null)永远不会产生 `previous`。再换一版会**覆盖**上一份 `previous`——它是"上一版",不是时间线;而且它**不带 `scannedAt`**,所以下游无法回答"这个 before 是什么时候量的"。
- **0004 新增 `capability-changes.mjs`:一个没有生产者的仪表**。44 行,只读 `data/capabilities.json`(默认路径,见 :16),筛出带 `previous` 的记录,统计 `{records, withPrevious, capabilityChanged, redLineChanged, added}`(:38-43);`added` 只数**新增**的能力名,redLine 的变化不分方向。没有任何 workflow 调用它,`package.json` 连 `scripts` 字段都没有——它是给维护者手动跑的报告器。它的 docstring 写"让它在 catalog 构建上跑几周,再回来看这个比率,决定界面要不要大声说'这个版本新增了什么'"(:5-9),但 CI 里的重扫结果从不落盘(见下一条),所以在当前 checkout 上它只会打印 `withPrevious: 0`(实测 0/3843)。**仪器的前提是一条并不存在的数据流。**
- **0004 新增:compare-only 的字面 IP 不算外联**。scanner 0.2.1 的 `redLines` 里有一类 "uses literal IP <addr> for network access",由字符串匹配生成;而 SSRF 防护里 `host === '100.100.100.200' → throw` 这种**比较**读起来和真的外联一模一样。`dropCompareOnlyIpRedLines`(:149-165)用的是扫描器自己的分类:`destinations[]` 里 `kind === 'ip'` 且**每个** site 的 `usage` 都是 `compare` 才删这条 redLine,有任何一个 `assigned`/`called` 就保留(测试里正反两例都在,capabilities.test.mjs:126-161)。真实案例是 `MeteorNOX/DeepSeek-Balance-Whale-Widget`(#8140)。这条过滤只对 0.2.1 的输出生效——存量数据里仍有 32 条记录带着 "uses literal IP …" 的 redLine,其中只有一条被手工改过。
- **增量与失败**:按 release 版本失效,无版本的引用 7 天后过期(lib/capabilities.mjs:114-120;`RECHECK_DAYS` 默认 7,probe-capabilities.mjs:96);每 100 条 flush 一次(可续跑);子进程用异步 execFile(sync 版会阻塞事件循环,"silently made CONCURRENCY a lie");**失败什么都不写**,保留旧记录。但 provenance 走的是**进程内 import**,没有 `node_modules` 时它会静默缺席(:84-93 的 catch),扫描本身则退回 `npx`——所以同一个 checkout 在有/无依赖两种状态下产出的记录形状不同,日志里都不会有差别。
- **扫描器版本(0004 重写)**:`package.json:25` 是 `^0.2.1`(区间),`package-lock.json` 钉到 **0.2.1** 且 `resolved` 指向 registry.npmjs.org——CI 跑 `npm ci`,所以硬的是 lockfile,不是那条 caret。代码读的是 **schemaVersion**,而它已经不是一个数:`SCANNER_SCHEMA = 2`,`READABLE_SCHEMAS = {1, 2}`(lib/capabilities.mjs:25-26),schema 3 返回 null(capabilities.test.mjs:183)。注释说明了 2 多了什么(`facts[]` 与 `evidence[].rule`),而本文件只抄 `capabilities`/`redLines`,两个 schema 下这两个字段同形——**旧账因此还能读**。这也解释了一个容易看错的现象:现文件里 3843 条全写 `tool: dsh-trust-check@0.1.13`,而代码默认早就是 0.2.1(`TOOL` 常量,probe-capabilities.mjs:47)。`tool` 记的是这次 run **宣称**用了哪个扫描器(它的取值就是那个常量或 `CAPABILITY_SCANNER`),真实二进制来自 node_modules 或 npx——标签是意图,只有 lockfile 让它成真。(顺带:`SCANNER_SCHEMA` 在 probe-capabilities.mjs:42 已是未用导入,只被测试引用;常量从"唯一可读的形状"变成了"最新可读的形状"。)**可复现的边界也在这里**:六个 workflow 在 2026-10-19 之后让 `npm ci` 显式走 npmjs(`npm_config_replace_registry_host: always`),本地仍按 lockfile 里的 npmmirror 地址取——版本由 lockfile 加 integrity 固定,变的只是传输路径;真正会漂的是 `npx` 兜底,它跟着环境的 registry 走。而探针产出的**事实**本来就不可复现:它读的是外部世界的当前状态,能固定的只有"用哪个工具、读哪个版本"。
- **谁调用**:build-site.yml:232 **每次构建都跑**(不在 PROBE_ALL 门控里);产物 `data/capabilities.json` → `docs/plugins.json` 的 `capabilities/capabilityRedLines/capabilityCheckedAt`(build-site.mjs:465-467、1160-1163)。注意它**只**透传这三样:`provenance` 与 `previous` 在 build-site 里没有任何读者,也没有进 `docs/index.json`——0004 新加的两个字段目前只有 `capability-changes.mjs` 一个消费者,而它读的是仓库里那份冻结文件。
- **快照口径(0004 实测)**:3843 条记录、453 条带 redLine(11.8%)、353 条命中"既读凭据又有网络访问"。与 0002 的 454/354 各差 1,差的正是 2026-10-20 删掉的那条记录(oauth-subs 只带一条 credentials+network 的 redLine,1a93fa18f);另有一条记录在同日被手工删掉一行字面 IP 的 redLine(0355e74b5)。**这两处手工修改就是 0004 期间这份文件的全部变化**——没有一条记录被重扫,`scannedAt` 仍全是 2026-09-24,`provenance`/`previous` 仍各 0 条。

## gh() 封装与限流(0002 后)

- probe-readmes **不再有 gh()**(改走 raw,免配额)。
- probe-updates 保留一份 gh(),其限流算法抽进 `lib/probe-updates-graphql.mjs:rateLimitDelayMs`;15s 超时;403/429 时 `retry-after` 优先,否则按 `x-ratelimit-remaining==='0'` + reset 精确等待;单次等待上限 120000ms;等待后递归重试。更精的兄弟仍在 check-submission.mjs(区分权限型/限流型 403、双层预算 75s/150s)。
- **配额经济学(0002 的新知识点)**:`raw.githubusercontent.com` 不计 API 配额;GraphQL 一次查询 50 仓;REST 两查/仓是旧的失败模式(夜间 3334 仓首轮失败即此)。
- **0004 的一处反向依赖**:capability 探针不再只把扫描器当子进程,provenance 需要**同一个包被 import 进来**(probe-capabilities.mjs:86)。这把"扫描器版本"从"命令行字符串"变成了"依赖安装状态",而它的失败模式是静默的——见上节。

## 第二遍重试(readmes/updates 不再同构)

- readmes:首遍批量失败 → sleep 20000ms → 逐个串行重探(旧的行为,0002 保留在 raw 路径上,只是失败含义变成"保留旧值")。
- updates:重试**按批**进行(每批 50 仓、批间 250ms),不再逐仓串行(:280-286)。
- **0004 补一条边界**:probe-npm **没有重试**。它的失败语义是"返回 null,保留旧值"(probe-npm.mjs:136-138、156-164),三条 pass 各自 8 并发分批串行;唯一会把"未知"写下去的地方是首见即失败的那个兜底(:163)。

## 地板门的三种变体(0002 修正)

| 脚本 | 判定对象 | 不过的动作 |
|------|----------|-----------|
| probe-stars | 结果 map(磁盘已有数据)/ 全部条目 | exit(1),不写盘(#1673 的 1362×null 教训)|
| probe-downloads | 分 population + 总体,双 66% | 同上 |
| probe-updates | 无覆盖率地板 | **exit(0) 且不写盘**(0002 从 exit 1 改;cache-save 只在成功时跑,#5731)|
| probe-capabilities | 无地板 | 失败条目**保持缺席**(未检出),旧记录保留;整轮全失败 exit(0) 并保留旧文件(probe-capabilities.mjs:222-229)|
| probe-readmes | 无 | 只汇报失败 URL 及其中多少 NEW(会渲染空白页),列前 20 |

「判定对象是已有数据而非本次成功数」这个细节容易看漏:即使本轮全失败(ok===0),只要磁盘上存量仍 ≥66%,探针打印 "left as-is" 并 exit(0)——**保护的是数据的连续性,不是本轮的成就感**。

## 待复核

- [x] ~~probe-readmes 是否存在把 broken repo 写成 missing 的边缘~~ → **该字段已被删除**,问题消失(0002)
- [x] ~~capabilities.json 既不回写、也不进 cache——夜间的重扫结果是否只活在那次 run 的 plugins.json 里~~ → **代码路径已回答**(0004):是。build-site.yml:232 每次构建都跑,权限 `contents: read`(:49),cache path 不含它(:108-114),所以重扫只进那次 run 的 `docs/plugins.json`(部署 + npm catalog 包),永不回仓库。剩下的已经不是"是不是",而是"要不要"。
- [ ] **0004 新增**:`previous` 的仪器目前空转——没有 CI 生产者、没有第二个消费者、存在量 0/3843。要让"版本间能力变化"有意义,得先决定重扫结果落在哪里(回写仓库?单独 cache?还是只在维护者本地的受审 run 里跑)。
- [ ] **0004 新增**:32 条存量记录仍带 "uses literal IP …" 的 redLine,其中多少其实是 `usage: compare`(新过滤器会清掉)无法从冻结文件判断,要等一次全量重扫。
- [ ] `PROBE_RECHECK_DAYS` 在 push build 上实际等于永远 fresh(cache 保留了 checkedAt),确认无叠加效应
- [ ] **0002 新增**:downloads 的 start/end 迁移会让旧快照的 624 行全部失效、首轮重探全部已发布条目——尚未对 CI 日志确认
