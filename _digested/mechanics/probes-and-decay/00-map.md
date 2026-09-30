# probes-and-decay · 探针与衰减

> 状态:**0002 已复核**(12 个脚本 = **8 个 probe-\*** + scan-decay + 双 publish + prune-legacy-screenshots,另加六个新 `lib/` 模块、adopt-discussions 与调度 workflow 逐行消化;行号以 `upstream@c18ba4a0d` 为准)。**0001 的结论"其余探针 diff 为空"在 0002 被推翻**:readmes/updates/downloads 三个被重写,capabilities 与 adopt 两层是全新的。最近核验:`c18ba4a0d`,2026-09-30。

## 定位

收录只是开始。probe-\* 家族定期回到外部世界采集事实(stars/下载量/npm 归属/上游 README/release 更新/tarball 存活/截图存活/**安装产物碰了什么**),scan-decay 找失联与失能,两个 publish 脚本把成果发成 npm 包供下游(尤其 dsh-market 与大陆镜像环境)消费,adopt-discussions 收拾评论线程。这个专题拆「活着的数据怎么保鲜、怎么不腐烂」。

## 一图流:谁读什么、写什么、怎么持久化

| 数据文件 | 写入方 | git 追踪? | Actions cache |
|----------|--------|-----------|---------------|
| `data/stars.json` | probe-stars | ✅(.gitignore 显式注明 NOT ignored)| 共享条目 probe-data-v2 |
| `data/downloads.json` | probe-downloads | ✅ | 独立 downloads-v1(#2797)|
| `data/added-dates.json` | 人工冻结基线(非探针)| ✅ | — |
| `data/screenshots.json`(legacy) | 人工(已被停用)→ prune-legacy-screenshots 渐进清空 | ✅ | — |
| **`data/capabilities.json`(0002 新增)** | probe-capabilities | ✅ | **无**(0002:提交即地板)|
| `data/npm-map.json` | probe-npm | ❌ | 共享条目 |
| `data/readmes.json` | probe-readmes | ❌ | 共享条目 |
| `data/tarballs.json` | probe-tarballs | ❌ | 共享条目 |
| `data/updates.json` | probe-updates | ❌ **从未提交过** | 独立 updates-v1 |
| `data/screenshots-declared.json` / `-live.json` | probe-screenshots | ❌ 且刻意不缓存(重算免费)| — |

> **0001 勘误(0002 更正)**:`updates.json` 在 0001 的表里被标成"✅ 已提交",实际它**从未进过 git 历史**(`git log --all -- data/updates.json` 为空),只在 updates-v1 cache 里。它也是唯一一个既不在 .gitignore、又从不被提交的 data 文件——本地跑一次探针就会在 `git status` 里冒出来。

**capabilities.json 的定位很特殊**:它是**提交进仓库的地板**,却不由任何 workflow 回写(build-site.yml:216 每次都跑 probe-capabilities,但 build-site 是 `contents: read`),也不在任何 actions/cache path 里。也就是说它是**维护者手动提交的快照**,夜间重扫的结果只活在那次运行产出的 `docs/plugins.json` 里——和 stars/downloads 的"提交地板 + cache 增量"是两种不同的持久化策略。

## 两条铁律(贯穿全部脚本)——0002 修正

1. **「未知 ≠ 死亡」。** 任何网络失败产生的都是"保留旧值",绝不写成否定性事实。**0002 修订**:0001 版写的例外"(404 除外——那是 GitHub 说的)"**在 readmes 上已被撤销**——probe-readmes 现在把 404 也当失败,保留旧值(它删掉了 `missing:true` 这个字段);probe-downloads 对"批量成功但该包不在返回里"也改为**保留旧计数,绝不写 0**。规则的**精神**没变(未知不许伪装成事实),变的是"什么算已知"。
2. **失败不许伪装成数据。** **0002 修订**:0001 版说"除 probe-readmes 外都有覆盖率地板(MIN_COVERAGE = 0.66),推不回来就 exit 1"——**现在只有 probe-stars 与 probe-downloads 有地板**(后者是分 population 的双 66%);probe-updates 与 probe-capabilities 改为 **exit 0 且不写盘**。理由是同一件事的另一面:cache 的 save post-step 只在 run 成功时执行,`exit 1` 会把 updates cache 打成**永久 miss**(#5731)。"失败不写盘"仍在,只是不再用红 exit 表达。

## 反常设计盘点(有意为之 vs 待商榷)

- **非原子写入**:所有脚本都是裸 `writeFileSync`,无 tmp+rename。安全性由天花板规则兜底,而非由原子性兜底。
- **fetch/限流封装仍不统一,但开始收敛**:0002 抽出共享的 `rateLimitDelayMs`(`lib/probe-updates-graphql.mjs`),`lib/terms.mjs`、`lib/capabilities.mjs`、`lib/probe-order.mjs`、`lib/added-dates.mjs` 也各自把一份曾经复制粘贴的逻辑收成单点。仍存的重复:stars/npm/tarballs/screenshots 各自为政的 fetch。
- **probe-downloads 的死常量仍在**:`CONCURRENCY = 8` 未使用(:42),实际全串行——scoped 包靠每包 sleep 2000ms 的 pacing 过 limiter(实测 8 并发 94/134 失败)。
- **probe-npm 对新条目的污染通道仍在**:首见即遇网络故障会被记成 `{npm: null, version: null}`(≈"未发布"),因 unpublished 判定每天重查而次日自愈,但仍是家族里唯一的"未知写成否定"例外。
- **0002 新增一条债**:`capabilities.json` 是提交物但没有回写通道、也不进 cache(见上),所以"扫过的 3844 条"会随分支 tarball 过期(7 天)而逐渐失真,而**没有任何自动机制让它重新变新**——它靠维护者手动跑一次并提交。

## 正文

- [01 · probe 家族:十个采集器的机制参考](./01-probe-family.md)
- [02 · scan-decay:腐坏判据与人机分工](./02-scan-decay.md)
- [03 · 发布层:npm 双包与 legacy 截图清退](./03-publish-layer.md)

调度拓扑(probes 在 CI 里的位置)与 build-site.yml 编排见 [site-surface/01](../site-surface/01-build-site.md) §部署链;decay-scan.yml 触发 cron `41 3 * * 1`(周一),权限仅 `contents: read` + `issues: write`——物理上无 commit 能力,与脚本的 flag-only 设计互为双保险。**0002 新增调度线**:adopt-discussions.yml(`discussion: created` 事件 + 每周二 04:17 全量扫,权限 `contents: read` + `discussions: write`——**仓库里第一条写非仓库资源的 workflow**)。
