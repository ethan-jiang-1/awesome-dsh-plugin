# 01 · probe 家族:九个采集器的机制参考(7 个 probe-* 脚本 + scan-decay + prune-legacy-screenshots)

> 基线:`upstream@38976afd`(0001 复核;probe-npm 自 97 行扩至 150 行,其余采集器未变)。行号为脚本内行号。

## 公共行为模式

- **花名册来源**:除 tarballs/screenshots(直接 `readEntries()` 消费 YAML)外,一律解析 `README.md` 的条目行(`/^- \[.+?\]\((https:\/\/github\.com\/[^)]+)\) [—-] /`)——README 是探针眼里的注册表视图。
- **增量判据**:`fresh()` = 非 PROBE_ALL 且已有值且 checkedAt 在 `PROBE_RECHECK_DAYS`(默认 1,readmes 例外默认 7)天内。**0001 修订**:published 的语义分层了——包名判定与成功 README 仍永久有效不重查;但 probe-npm 的 `version` 字段只靠 nightly `PROBE_ALL` 全量刷新(push 构建永不刷新);unpublished 每天复查。
- **monorepo**:stars/updates/tarballs 取父 repo;npm/readmes/screenshots 进入子目录。
- **写盘前**:按 key localeCompare 排序(readmes 例外:紧凑无缩进)、清理不在列表中的 key。

## 各采集器速览

| 脚本 | 目标 API | token | 输出 value 形状 | 特殊点 |
|------|----------|-------|-----------------|--------|
| probe-stars(142)| `repos/{repo}` | 需 | `{stars, checkedAt}` | 无重试;失败保留旧值 |
| probe-npm(150)| raw package.json + registry.npmjs.org | 免 | `{npm: name\|null, version: latest\|null, checkedAt}` | **repository 字段回链校验**防冒名:先 `dist-tags.latest` 再取该 version 的 repository(处理 registry 顶层陈旧 metadata),小写包含即认。**0001 新增 version 字段**(:14-21):三态区分——键缺失=未回填、`version:null`=探过但无 latest tag、有键必写(失败兜底 :133);弱值不覆盖强值(`latest ?? priorVersion`,:100-105);新鲜度分层:full 队列(PROBE_ALL/首见/unpublished 超 1 天)跑完整探针,backfill 队列(已发布无 version 键)只打一次 registry 一次性回填(:60-68,112-124);`hasOwnProperty` 兼容旧行(:58)。零额外请求(packument 本来就取了);下游 build-site.mjs:390 透传进 plugins.json(消费方 dsh-market#348) |
| probe-downloads(227)| npm bulk point/last-month | 免 | `{downloads, checkedAt}` | unscoped 批量 128 个/scoped 单发+2s pacing(npm bulk 混入一个 scoped 即整批 400);404 算 0 不算失败;**分 population 双层地板**(scoped/unscoped 分别 ≥66%)——2026-08-19 总体 85% 达标而 scoped 仅 30%,聚合数掩盖了病态的一半 |
| probe-readmes(214)| `/repos/{repo}/readme` | 需 | `{en?, zh?, missing?}` | 语言嗅探 CJK 占比>3% 定 zh;9 个候选中文文件名 + 5 个英文,经一次 contents listing 匹配省配额;<br>`MAX_BYTES=48KB` 截断;**404 → {missing:true}(是事实),其他错误 → null(保留旧值)**;替补语言必须过嗅探不信文件名("some 'zh' files are English stubs") |
| probe-updates(199)| releases/latest + commits?per_page=5 | 需 | `{release{tag,name,publishedAt,url,body}, commits[{sha,message,date}], checkedAt}` | body 截 4KB、message 取首行截 200 字;`!release && !commits.length` 才算失败;刻意无地板(update notes 缺失合法),但拒绝空 map 替换非空 |
| probe-tarballs(125)| release 资产 ranged GET(`bytes=0-0`) | 免 | `{tarball, ok(三值), status}` | 用 Range 不用 HEAD(GitHub 对 release asset 的 HEAD 重定向后行为不一致);URL 变更则不继承旧 verdict;`releases/latest/download/<带版本号.tgz>` 会打印"作者下次发版就坏"预警 |
| probe-screenshots(239)| raw screenshots.json + 图片存活 | 免 | declared:`{url:[imgs]}`;live:`{img:{ok三值}}` | 作者仓库声明(四种 JSON 形状容错)+ legacy 兜底并联;host 白名单刻意镜像 build-site 的 SCREENSHOT_HOSTS,**堵“作者声明绕规则”后门**;相对路径禁 `/` 开头与 `..`;legacyOnly 与新声明并集做存活检查,被 superseded 的 legacy 键不查 |

## gh() 封装(readmes 与 updates 两份逐字等价)

15s 超时;403/429 时:`retry-after` 头优先,否则用 `x-ratelimit-remaining === '0'` + reset 时间戳精确等到配额窗口;单次等待上限 **120000ms**,超限抛 HttpError;等待后递归重试同一 path。这套逻辑在 check-submission.mjs 里有一个更精的兄弟(区分权限型 403 与限流型 403、双层预算 75s/150s),见 [submission-gates/02](../submission-gates/02-pr-gate-and-check-submission.md)。

## 第二遍串行重试(readmes/updates 同构)

首遍批量失败的清单 → sleep 20000ms → 逐个串行重探,间隔 250ms(:156-171 动机):burst 失败不能被误读成"这仓库没东西",尤其新条目没有旧值可回退。

## 地板门的三种变体

| 脚本 | 判定对象 | 不过的动作 |
|------|----------|-----------|
| probe-stars | 结果 map(磁盘已有数据)/ 全部条目 | exit(1),不写盘(#1673 的 1362×null 教训)|
| probe-downloads | 分 population + 总体,双 66% | 同上 |
| probe-updates | 无覆盖率地板 | 但 `!have && urls.length` → exit(1)(拒空 map 替换非空)|
| probe-readmes | 无 | 只汇报失败 URL 及其中多少 NEW(会渲染空白页),列前 20 |

「判定对象是已有数据而非本次成功数」这个细节容易看漏:即使本轮全失败(ok===0),只要磁盘上存量仍 ≥66%,探针打印 "left as-is" 并 exit(0)——**保护的是数据的连续性,不是本轮的成就感**。

## 待复核

- [ ] probe-readmes 是否存在把 broken repo 写成 missing 的边缘(404 与 rename 中间态)
- [ ] `PROBE_RECHECK_DAYS` 在 push build 上实际等于永远 fresh(cache 保留了 checkedAt),确认无叠加效应
