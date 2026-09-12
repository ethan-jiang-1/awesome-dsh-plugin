# probes-and-decay · 探针与衰减

> 状态:**0001 已复核**(11 个脚本 = 7 个 probe-* + scan-decay + 双 publish + prune-legacy-screenshots,另加调度 workflow 逐行消化;行号引用以 `upstream@38976afd` 为准)。最近核验:`38976afd`,2026-09-12。复核结论:仅 probe-npm.mjs(97→150 行)与 build-site.yml(并发组拆分)有实质变更,其余探针/decay/publish 脚本 diff 为空。

## 定位

收录只是开始。probe-\* 家族定期回到外部世界采集事实(stars/下载量/npm 归属/上游 README/release 更新/tarball 存活/截图存活),scan-decay 找失联与失能,两个 publish 脚本把成果发成 npm 包供下游(尤其 dsh-market 与大陆镜像环境)消费。这个专题拆「活着的数据怎么保鲜、怎么不腐烂」。

## 一图流:谁读什么、写什么、怎么持久化

| 数据文件 | 写入方 | git 追踪? | Actions cache |
|----------|--------|-----------|---------------|
| `data/stars.json` | probe-stars | ✅(.gitignore 显式注明 NOT ignored)| 共享条目 probe-data-v2 |
| `data/downloads.json` | probe-downloads | ✅ | 独立 downloads-v1(#2797)|
| `data/npm-map.json` | probe-npm | ❌ | 共享条目 |
| `data/readmes.json` | probe-readmes | ❌ | 共享条目 |
| `data/tarballs.json` | probe-tarballs | ❌ | 共享条目 |
| `data/updates.json` | probe-updates | ✅ | 独立 updates-v1 |
| `data/screenshots-declared.json` / `-live.json` | probe-screenshots | ❌ 且刻意不缓存(重算免费)| — |
| `data/screenshots.json`(legacy) | 人工(已被停用)→ prune-legacy-screenshots 渐进清空 | ✅ | — |

所有 key 都是**条目 URL 原文**(含 monorepo 子路径),与 `entry.url` 全等 join——这是边车数据的真实连接键;文件名 slug(`owner__repo--sub-path.yml`)是另一套独立命名规则。

## 两条铁律(贯穿全部脚本)

1. **「未知 ≠ 死亡」。** 任何网络失败产生的都是“保留旧值”,绝不写成否定性事实(404 除外——那是 GitHub 说的)。tarball/screenshots 用三值 verdict(ok/false/null),null 沿用旧判决。
2. **失败不许伪装成数据。** 除 probe-readmes 外都有覆盖率地板(`MIN_COVERAGE = 0.66`):推不回来就不写盘、exit 1,宁可在 CI 露红也不让 `stars:null × 1362` 上线(#1673)。scan-decay 的版本是 5% 不确定率熔断整份报告。

## 反常设计盘点(有意为之 vs 待商榷)

- **非原子写入**:所有脚本都是裸 `writeFileSync`,无 tmp+rename。安全性由“地板门不过就 exit 不写”兜底,而不是由原子性兜底。
- **没有共享 HTTP 客户端**:四套 fetch 封装并存(裸 fetch×2 处、rate-limit-aware gh() 两份逐字重复、scan-decay 的 api()/graphql()、downloads 的六次退避),user-agent 各自为政。是债,但每套的退避策略确实不同。
- **probe-downloads 的死常量**:`CONCURRENCY = 8` 从未被使用(:42),实际全串行——scoped 包靠每包 sleep 2000ms 的 pacing 过 limiter(测得:8 并发 94/134 失败,pacing 是唯一有效解)。
- **probe-npm 对新条目的污染通道**:首见即遇网络故障会被记成 `{npm: null, version: null}`(≈"未发布"),违反自身家族的“未知≠否定”纪律;因 unpublished 判定每天重查而次日自愈,但值得记住这个例外(失败兜底见 probe-npm.mjs:133)。

## 正文

- [01 · probe 家族:九个采集器的机制参考](./01-probe-family.md)
- [02 · scan-decay:腐坏判据与人机分工](./02-scan-decay.md)
- [03 · 发布层:npm 双包与 legacy 截图清退](./03-publish-layer.md)

调度拓扑(probes 在 CI 里的位置)与 build-site.yml 编排见 [site-surface/01](../site-surface/01-build-site.md) §触发与缓存;decay-scan.yml 触发 cron `41 3 * * 1`(周一),权限仅 `contents: read` + `issues: write`——物理上无 commit 能力,与脚本的 flag-only 设计互为双保险。
