# 01 · probe 家族:十个采集器的机制参考(8 个 probe-* 脚本 + scan-decay + prune-legacy-screenshots)

> 基线:`upstream@c18ba4a0d`(0002 复核)。**0002 是本专题立项以来最大的一次探针改动**:probe-readmes 214→**310**、probe-updates 199→**331**(+`lib/probe-updates-graphql.mjs` 160)、probe-downloads 227→**236**、新增 probe-capabilities **200**(+`lib/capabilities.mjs` 144);stars/npm/tarballs/screenshots 四个未变。行号为脚本内行号。

## 公共行为模式

- **花名册来源**:tarballs/screenshots/capabilities 三个直接 `readEntries()` 消费 YAML,其余解析 `README.md` 的条目行(`/^- \[.+?\]\((https:\/\/github\.com\/[^)]+)\) [—-] /`)——README 仍是多数探针眼里的注册表视图。
- **增量判据**:`fresh()` = 非 PROBE_ALL 且已有值且 checkedAt 在 `PROBE_RECHECK_DAYS`(默认 1,readmes 例外默认 7,capabilities 7)天内。probe-npm 的 `version` 字段只靠 nightly `PROBE_ALL` 全量刷新;unpublished 每天复查。
- **公平调度(0002 新增)**:`lib/probe-order.mjs` 的 `leastRecentlyChecked(urls, map)` 按 `checkedAt` 升序排、并列保持 README 顺序,已被 probe-updates 采用(:257)。动机是实测:2026-09-14 的 nightly `3632 listed … 2364 repo(s) kept their previous update data`,README 位置 40–80% 的条目最后检查时间停在 09-05——**预算被砍的一轮会把同一段列表饿死**(#5149)。
- **monorepo**:stars/updates/tarballs 取父 repo;npm/readmes/screenshots/**capabilities** 进入子目录。
- **写盘前**:按 key localeCompare 排序(readmes 例外:紧凑无缩进)、清理不在列表中的 key。

## 各采集器速览

| 脚本 | 目标 API | token | 输出 value 形状 | 特殊点 |
|------|----------|-------|-----------------|--------|
| probe-stars(142,未变)| `repos/{repo}` | 需 | `{stars, checkedAt}` | 无重试;失败保留旧值;有地板 |
| probe-npm(150,未变)| raw package.json + registry.npmjs.org | 免 | `{npm: name\|null, version: latest\|null, checkedAt}` | **repository 字段回链校验**防冒名;**version 三态**(键缺失/`version:null`/有键);弱值不覆盖强值;下游 build-site 透传进 plugins.json |
| probe-downloads(**236**)| npm bulk `point/${start}:${end}` | 免 | `{downloads, checkedAt, **start, end**}` | **0002:相对时间窗 `last-month` 换成显式 UTC 30 天窗**(#5309),`downloadResult` 校验 package/start/end/downloads 四项,不符即抛"Missing, invalid, or stale npm download response";**批量成功但缺某个名字 → 保留旧计数,绝不写 0**;`fresh()` 也要求 start/end 匹配;unscoped 批量 128/scoped 单发+2s pacing;分 population 双层 66% 地板不变 |
| probe-readmes(**310**)| **raw.githubusercontent.com/HEAD** | **免(冷启动才要)** | `{en?, zh?}`(**`missing` 字段已删**)| **0002 整体重写**:contents API(≤4 次 REST/仓,夜间 `3334 repo(s) failed the first pass`、约九成页面陈旧)→ raw(完全不计 API 配额);批量 GraphQL 目录列举(50 仓/查询/1 点)一次拿到 README 与兄弟文件名,取正文只需 1–2 次请求(初版"猜文件名"跑了 40 分钟被取消);`MAIN_NAMES/pickMain/pickSibling`;语言嗅探 CJK>3%;`MAX_BYTES=48KB` 不变;并发 PROBE_ALL 4→**10**(旧 4 是给 REST 定的);raw() 重试 3 次(1500·2ⁿ ms);**404 也当失败保留旧值**,不再写 `missing:true`;token 现在只是"冷启动就退出"的闸门 |
| probe-updates(**331**)| **GraphQL 批量 releases+commits** + REST 兜底 | 需 | `{release{…}, commits[…], checkedAt}` | **0002 重写**:一条查询管 50 个仓的**两个事实**、只花 1 点(全列表 ~75 点 / 1000 每小时);动机是 2026-09-16 的夜间跑(`3727 listed … 2594 failed the first pass`,文件三分之一停在 09-05,#5275/#5317);REST `probe()` 保留为"两个字段的度量基准";`readEntries` 会拒绝 null/报错 alias 以及 `isDraft/isPrerelease` 的 latestRelease(端点没承诺这些语义),退回 REST(CONCURRENCY=8);限流等待抽成共享 `rateLimitDelayMs`,403/429 与 GraphQL HTTP-200-`data:null` 都等;重试按批(250ms/批);**冷缓存全失败改为 exit(0) 不写盘**(#5731) |
| probe-tarballs(125,未变)| release 资产 ranged GET(`bytes=0-0`)| 免 | `{tarball, ok(三值), status}` | 用 Range 不用 HEAD;URL 变更不继承旧 verdict;带版本号资产会打"下次发版就坏"预警 |
| probe-screenshots(239,未变)| raw screenshots.json + 图片存活 | 免 | declared/live 两文件 | host 白名单镜像 build-site;相对路径禁 `/` 开头与 `..` |
| **probe-capabilities(200,0002 新增)** | npm tarball / 作者预构建 release / codeload 归档 | 免 | `{version, spec, capabilities[], redLines[], scannedAt, tool}` | **静态能力披露(#401/#209)**,见下 |

## probe-capabilities:把"碰了什么"变成可核对的事实

- **它做什么**:把**用户实际会装到的产物**下载下来(优先级:npm tarball > 作者预构建 tarball > codeload `github:<repo>@HEAD`),交给 `dsh-trust-check` 静态扫描;子路径条目**在子目录扫描**,因为那才是用户拿到的包(扫 monorepo 根会把兄弟包算进来)。
- **十种能力**:`fs-read / fs-write / env / network / shell / credentials / llm / dynamic-code / host-runtime / subagent`;**redLines 是句子的列表**,如 "reads credentials/secrets AND has network access"、"runs code at install time (postinstall)"。
- **披露而非判决(#209 原话)**:脚本头写着 "The facts are DISCLOSURE, never a verdict";`lib/capabilities.mjs` 的 `factsFromScan` **刻意丢掉** `score`/`band`/`verdict`,好让"没有任何界面能把这个插件渲染成绿色,连意外都不行"。未扫到的条目**不在文件里**,界面渲染成"未检出"——"我们没能看"和"我们看了什么也没看到"是两句不同的话。
- **增量与失败**:按 release 版本失效,无版本的引用 7 天后过期;每 100 条 flush 一次(可续跑);子进程用异步 execFile(sync 版会阻塞事件循环,"silently made CONCURRENCY a lie");**失败什么都不写**,保留旧记录。
- **扫描器版本钉在 devDependency**:`dsh-trust-check@0.1.13`(package.json),代码读的是它的 `schemaVersion` 而不是 npm 版本;升级 scanner 是一次受审的 diff。
- **谁调用**:build-site.yml:216 **每次构建都跑**(不在 PROBE_ALL 门控里);产物 `data/capabilities.json` → `docs/plugins.json` 的 `capabilities/capabilityRedLines/capabilityCheckedAt`。
- **首份快照口径(0002 实测)**:3844 行(=第一次全量扫描),未扫到 548 条;有 redLine 的 454 条(11.8%),其中 **354 条命中"既读凭据又有网络访问"**——这是本目录第一次能对"供给链攻击面"给出量化下界(0001 时只能声明测不了)。

## gh() 封装与限流(0002 后)

- probe-readmes **不再有 gh()**(改走 raw,免配额)。
- probe-updates 保留一份 gh(),其限流算法抽进 `lib/probe-updates-graphql.mjs:rateLimitDelayMs`;15s 超时;403/429 时 `retry-after` 优先,否则按 `x-ratelimit-remaining==='0'` + reset 精确等待;单次等待上限 120000ms;等待后递归重试。更精的兄弟仍在 check-submission.mjs(区分权限型/限流型 403、双层预算 75s/150s)。
- **配额经济学(0002 的新知识点)**:`raw.githubusercontent.com` 不计 API 配额;GraphQL 一次查询 50 仓;REST 两查/仓是旧的失败模式(夜间 3334 仓首轮失败即此)。

## 第二遍重试(readmes/updates 不再同构)

- readmes:首遍批量失败 → sleep 20000ms → 逐个串行重探(旧的行为,0002 保留在 raw 路径上,只是失败含义变成"保留旧值")。
- updates:重试**按批**进行(每批 50 仓、批间 250ms),不再逐仓串行(:280-286)。

## 地板门的三种变体(0002 修正)

| 脚本 | 判定对象 | 不过的动作 |
|------|----------|-----------|
| probe-stars | 结果 map(磁盘已有数据)/ 全部条目 | exit(1),不写盘(#1673 的 1362×null 教训)|
| probe-downloads | 分 population + 总体,双 66% | 同上 |
| probe-updates | 无覆盖率地板 | **exit(0) 且不写盘**(0002 从 exit 1 改;cache-save 只在成功时跑,#5731)|
| probe-capabilities | 无地板 | 失败条目**保持缺席**(未检出),旧记录保留;整轮不写空列表 |
| probe-readmes | 无 | 只汇报失败 URL 及其中多少 NEW(会渲染空白页),列前 20 |

「判定对象是已有数据而非本次成功数」这个细节容易看漏:即使本轮全失败(ok===0),只要磁盘上存量仍 ≥66%,探针打印 "left as-is" 并 exit(0)——**保护的是数据的连续性,不是本轮的成就感**。

## 待复核

- [x] ~~probe-readmes 是否存在把 broken repo 写成 missing 的边缘~~ → **该字段已被删除**,问题消失(0002)
- [ ] `PROBE_RECHECK_DAYS` 在 push build 上实际等于永远 fresh(cache 保留了 checkedAt),确认无叠加效应
- [ ] **0002 新增**:capabilities.json 既不回写、也不进 cache——夜间的重扫结果是否只活在那次 run 的 plugins.json 里(UNVERIFIED)
- [ ] **0002 新增**:downloads 的 start/end 迁移会让旧快照的 624 行全部失效、首轮重探全部已发布条目——尚未对 CI 日志确认
