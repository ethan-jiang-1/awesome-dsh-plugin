# probes-and-decay · 探针与衰减

> 状态:**0004 已复核**(2026-10-24,行号以 `upstream@b4d0049a8` 为准;diff 区间 `4693e5a83..b4d0049a8`)。0003 判本专题"无对应 diff",这条判断只对 0003 那一段成立;0004 是本专题自 0002 以来第一次实质改动,且只落在两处——capability 探针(probe-capabilities 200→**230**、`lib/capabilities.mjs` 144→**224**、新增 `capability-changes.mjs` 44、`capabilities.test.mjs` 111→**192**)与 probe-npm(150→**181**)。`scan-decay.mjs` 仍 388 行,stars/downloads/readmes/updates/tarballs/screenshots 六个探针、prune-legacy-screenshots 与 publish-updates 全部零 diff。脚本清点:13 个(8 个 probe-* + scan-decay + capability-changes + 双 publish + prune-legacy-screenshots),另加 8 个 `lib/` 模块。

## 定位

收录只是开始。probe-\* 家族定期回到外部世界采集事实(stars/下载量/npm 归属/上游 README/release 更新/tarball 存活/截图存活/**安装产物碰了什么**),scan-decay 找失联与失能,两个 publish 脚本把成果发成 npm 包供下游(尤其 dsh-market 与大陆镜像环境)消费,adopt-discussions 收拾评论线程。这个专题拆「活着的数据怎么保鲜、怎么不腐烂」。**0004 新增一条主线**:探针开始记录"与上一版相比变了什么"(capabilities 的 `previous`)和"这个包有没有来源证明"(npm provenance),而市场索引 `index.json` 让 npm 探针多了一个必须按时写到的字段——三件事都卡在同一个瓶颈上:这些结果的落点。

## 一图流:谁读什么、写什么、怎么持久化

| 数据文件 | 写入方 | git 追踪? | Actions cache |
|----------|--------|-----------|---------------|
| `data/stars.json` | probe-stars | ✅(.gitignore 显式注明 NOT ignored)| 共享条目 probe-data-v2 |
| `data/downloads.json` | probe-downloads | ✅ | 独立 downloads-v1(#2797)|
| `data/added-dates.json` | 人工冻结基线(非探针)| ✅ | — |
| `data/screenshots.json`(legacy) | 人工(已被停用)→ prune-legacy-screenshots 渐进清空 | ✅ | — |
| `data/capabilities.json`(0002 新增) | probe-capabilities | ✅ | **无**,也**没有回写通道**(0004 复核仍是纯地板)|
| `docs/index.json`(**0004 新增**,构建产物) | build-site.mjs(消费 `data/npm-map.json`)| ❌(`docs/` 被 .gitignore 忽略)| 无,每次构建重算,随 catalog 包发布 |
| `data/npm-map.json` | probe-npm | ❌ | 共享条目 |
| `data/readmes.json` | probe-readmes | ❌ | 共享条目 |
| `data/tarballs.json` | probe-tarballs | ❌ | 共享条目 |
| `data/updates.json` | probe-updates | ❌ **从未提交过** | 独立 updates-v1 |
| `data/screenshots-declared.json` / `-live.json` | probe-screenshots | ❌ 且刻意不缓存(重算免费)| — |

> **0001 勘误(0002 更正)**:`updates.json` 在 0001 的表里被标成"✅ 已提交",实际它**从未进过 git 历史**(`git log --all -- data/updates.json` 为空),只在 updates-v1 cache 里。它也是唯一一个既不在 .gitignore、又从不被提交的 data 文件——本地跑一次探针就会在 `git status` 里冒出来。

**三份提交边车在 2026-10-24 的真实年龄(读文件自己写的字段,不看 mtime)**:

- `data/capabilities.json`:3843 条记录**全部** `scannedAt=2026-09-24`、**全部** `tool=dsh-trust-check@0.1.13`(而 HEAD 的默认扫描器已是 0.2.1),`provenance`/`previous` 各 0 条;
- `data/stars.json`:1464 个键里 1463 条 `checkedAt=2026-08-19`、1 条 `2026-09-04`;
- `data/screenshots.json`:288 个键,**没有任何时间字段**——它的年龄只能靠 diff 推。

三份文件在 0004 区间的改动加起来是:删键、改键、补一条截图、手工删掉一条 redLine——**没有出现任何一个新的时间戳**,也就是没有一次重扫或重探落进仓库。这才是"冻结"的可核对含义。

**capabilities.json 的定位很特殊,而 0004 把它变成了一个可证明的结论**:它仍是**提交进仓库的地板**,却不由任何 workflow 回写(build-site.yml:232 每次都跑 probe-capabilities,但 build-site 的权限是 `contents: read`,build-site.yml:49),也不在任何 actions/cache path 里(build-site.yml:108-114 只列 npm-map/stars/readmes/tarballs)。于是每夜的重扫结果只活在那次 run 的 `docs/plugins.json` 里,而那份文件会部署、会被打进 npm catalog 包——**线上可以很新,仓库地板只会更旧**。这份旧是会算出来的:名单在 0004 区间从 4489 条涨到 6704 条(`data/plugins/*.yml` 净增 2255 个),按当前 `data/plugins/*.yml` 的 url join,只有 **3792/6704(56.6%)** 的条目还有记录(0003 时 3826/4489 = 85.2%),另有 51 个键指向已经不在名单里的 URL——删掉的记录探针不会清理,只能人手工删(oauth-subs 那条就是 2026-10-20 手工删的,1a93fa18f,#8058)。

## 两条铁律(贯穿全部脚本)——0002 修正

1. **「未知 ≠ 死亡」。** 任何网络失败产生的都是"保留旧值",绝不写成否定性事实。**0002 修订**:0001 版写的例外"(404 除外——那是 GitHub 说的)"**在 readmes 上已被撤销**——probe-readmes 现在把 404 也当失败,保留旧值(它删掉了 `missing:true` 这个字段);probe-downloads 对"批量成功但该包不在返回里"也改为**保留旧计数,绝不写 0**。规则的**精神**没变(未知不许伪装成事实),变的是"什么算已知"。**0004 又多了两个实例**:扫描器的 schema 从"只认一个版本"变成"认一个可读集合"(`READABLE_SCHEMAS = {1, 2}`,lib/capabilities.mjs:25-26),所以 0.1.13 写下的旧账仍然可读;provenance 查询失败返回 `undefined` 而不是 `present:false`,注释原话是 "we could not ask" 不等于 "this version has no attestation"(probe-capabilities.mjs:80-93)。
2. **失败不许伪装成数据。** **0002 修订**:0001 版说"除 probe-readmes 外都有覆盖率地板(MIN_COVERAGE = 0.66),推不回来就 exit 1"——**现在只有 probe-stars 与 probe-downloads 有地板**(后者是分 population 的双 66%);probe-updates 与 probe-capabilities 改为 **exit 0 且不写盘**。理由是同一件事的另一面:cache 的 save post-step 只在 run 成功时执行,`exit 1` 会把 updates cache 打成**永久 miss**(#5731)。"失败不写盘"仍在,只是不再用红 exit 表达。0004 对这条没有改动,capabilities 的全失败分支仍是"保留旧文件 + 一行日志"(probe-capabilities.mjs:222-229)。

## 反常设计盘点(有意为之 vs 待商榷)

- **非原子写入**:所有脚本都是裸 `writeFileSync`,无 tmp+rename。安全性由天花板规则兜底,而非由原子性兜底。capabilities 每 100 条整文件重写一次(FLUSH_EVERY,probe-capabilities.mjs:101、125-129),中断时留下的是"已扫到的最新完整快照",不是半行——这是它唯一的原子性近似。
- **fetch/限流封装仍不统一,但开始收敛**:0002 抽出共享的 `rateLimitDelayMs`(`lib/probe-updates-graphql.mjs`),`lib/terms.mjs`、`lib/capabilities.mjs`、`lib/probe-order.mjs`、`lib/added-dates.mjs` 也各自把一份曾经复制粘贴的逻辑收成单点。仍存的重复:stars/npm/tarballs/screenshots 各自为政的 fetch。**0004 新增一种不对称**:capability 探针除了 spawn 扫描器,还第一次把同一个包 `import('dsh-trust-check')` 进来直接调用它的 `readNpmProvenance`(probe-capabilities.mjs:86-89);没有 `node_modules` 时这个 import 直接抛、provenance 被静默略过,扫描本身照旧走 `npx`(:59-62)。也就是说"记录里没有 provenance"可能是"没问",而日志里不会有任何一行说明——符合披露纪律(缺席=未检出),但不符合"失败要计数"的口味。
- **probe-downloads 的死常量仍在**:`CONCURRENCY = 8` 未使用(:42),实际全串行——scoped 包靠每包 sleep 2000ms 的 pacing 过 limiter(实测 8 并发 94/134 失败)。
- **probe-npm 对新条目的污染通道仍在**:首见即遇网络故障会被记成 `{npm: null, version: null, checkedAt}`(≈"未发布"),因 unpublished 判定每天重查而次日自愈,但仍是家族里唯一的"未知写成否定"例外。0004 的新字段没有加宽这个洞:那种失败行不带 `publishedAt` 键,而回填通道要求 `entry.npm` 为真(probe-npm.mjs:76),所以它要等下一次成功的 full probe 才被补齐(:130-135)。
- **0004 的新债:capabilities 的"固定资产"没有维护回路。** 它不回写、不进 cache、**也不清理名单外的键**(`next = { ...stored }` 之后没有任何 roster 过滤,probe-capabilities.mjs:115、125-129;对照 probe-stars.mjs:101-102 与 probe-npm.mjs:174-175 都有 `listed` 删除循环)。后果是两件可观察的事:49 个孤儿键要人手工删;2026-10-20 那条 compare-only 误报的修复落在**两处**——代码里加过滤器(lib/capabilities.mjs:149-165)、以及手工从 `data/capabilities.json` 里删掉一行 redLine(0355e74b5,记录是 `MeteorNOX/DeepSeek-Balance-Whale-Widget`,#8140)。当一次修复必须手抄进数据文件,说明数据文件的再生路径事实上不存在。

## 正文

- [01 · probe 家族:十个采集器的机制参考](./01-probe-family.md)
- [02 · scan-decay:腐坏判据与人机分工](./02-scan-decay.md)
- [03 · 发布层:npm 双包与 legacy 截图清退](./03-publish-layer.md)

调度拓扑(probes 在 CI 里的位置)与 build-site.yml 编排见 [site-surface/01](../site-surface/01-build-site.md) §部署链;decay-scan.yml 触发 cron `41 3 * * 1`(周一),权限仅 `contents: read` + `issues: write`(:12-14)——物理上无 commit 能力,与脚本的 flag-only 设计互为双保险。**0002 新增调度线**:adopt-discussions.yml(`discussion: created` 事件 + 每周二 04:17 全量扫,:20-25,权限 `contents: read` + `discussions: write`,:32-34——**仓库里第一条写非仓库资源的 workflow**)。**0004 没有任何 cron 或 permissions 改动;唯一与调度有关的变更在安装源**:六个 workflow 的 `npm ci` 全部加上 `npm_config_registry: https://registry.npmjs.org/` 与 `npm_config_replace_registry_host: always`(13dcda271,2026-10-19),因为 lockfile 里有 7 个 `resolved` 指向 registry.npmmirror.com,而那个 CDN 在 GitHub runner 上反复 503/504 把 `npm ci` 挂住几十分钟。它只决定**工具从哪装下来**,不改变探针抓的外部事实——探针里所有外部 URL 都是硬编码的(如 registry.npmjs.org、codeload.github.com),不读 npm 配置(细节分别见 01 与 03)。
