# ecosystem 05 · 方法档案:fresh_probe 数据管线

> **为什么有这份文档**:做"真实下载/热度趋势"时,仓库边车不可用、catalog 会停更、
> 公开 API 有各自的坑——下面每一条都是实际踩过并验证过的。脚本本体
> [`fresh_probe.py`](fresh_probe.py) 已固化这些对策;本文记录"为什么必须这样"。
> 首次跑通:2026-09-12,基线 `main@38976afd`。

## 1. 数据源层级(重要程度递增)

| 源 | 新鲜度 | 问题 | 用途 |
|----|--------|------|------|
| 仓库边车 `data/downloads.json` 等 | **冻结**(0001 实测:15 天 3213 commits 只变 6 行,下载榜数字与 08-26 完全一致) | 真实数据活在 Actions cache,仓库里的是快照的快照 | 只看历史锚点 |
| `dsh-plugin-catalog` npm 包 | 每夜 | **发布会停**(09-08 后停更,#3512 型故障同征);且"下载量"是包发布时刻快照 | 备用基线,取法 `npm pack dsh-plugin-catalog@<ver> --cache <自建目录>`(系统 npm cache 可能 root-owned 报 EPERM) |
| **自采:公开 API**(本管线) | 实时 | 无停更风险;坑见下文 | 趋势分析的唯一可靠源 |

## 2. 本机网络环境约束(2026-09-12 实测,换机器需重测)

| 通道 | 状态 | 对策 |
|------|------|------|
| `git fetch` https | **挂死**(60s/180s 双超时) | 走 SSH:`git fetch git@github.com:<org>/<repo>.git main:refs/remotes/upstream/main` |
| `raw.githubusercontent.com` | **完全不可达**(000) | npm 包名改经 `api.github.com/contents` 取 package.json |
| `api.github.com` / `gh api` | 通(gh CLI 已认证,5000/hr) | GraphQL 星标、contents API 都走它 |
| `api.npmjs.org` / `registry.npmjs.org` | 通,无鉴权 | 下载量、包名归属校验 |

## 3. 五个坑与对策(脚本内的不变量)

### 坑 1:npm 包名不在注册表里
yml 只有 GitHub URL;npm 名要解析。层级:上一份快照的 npm 名(已验证)>
catalog 的 npm 字段(上游 probe 亲自解析,视为可信)>
repo 的 package.json `"name"`(monorepo 条目取子路径;URL 有 `#sub` 与
`/tree/<branch>/sub` 两种形态,**都要处理**)。
回源结果写 `_snapshots/raw-name-cache.json`(含 null),避免重复烧 contents 配额。

### 坑 2:包名撞名 → 别人的下载量记到我们头上
repo 叫 `Nicercz007-cloud/schedule` 的条目,package.json 里 name 是公共包
`schedule`(月下载 48 亿级)——不校验就凭空多出 16 万"下载"。
**对策**:`validate_names` 每轮对全部"回源/缓存来源"的名字跑 registry 元数据校验:
- 元数据 repository 指向同一 owner → 通过(注意 `github.com:` 冒号形态);
- 元数据没写 repository 但名字含 `dsh` → 通过(名字出自 repo 自己的 package.json,特异性足够);
- 其余(404 未发布、指向他人仓)→ 丢弃,标 npm 不可归因。

### 坑 3:未发布 ≠ 异常
**实测 2780/3552 有 npm 名,772 条(22%)未发布到 npm 或名字撞名弃用**——
这是生态真实属性(github/tarball 安装通道),不是 bug。但它们必须**退出增量
统计**,否则会制造 d0>0→d1=0 的假负增量污染类目流向。

### 坑 4:GraphQL 批量里混入坏 alias 会全军覆没
`repository(owner,name)` 的 name 带子路径(`/tree/...` 未剥净)→ 该 alias
NOT_FOUND → **gh 以 rc=1 退出,即使其余 79 个都成功**。对策:rc!=0 也解析
stdout 的 `data`(失败 alias 为 null,成功的照常取);repo 归一后按仓去重,
结果回填同仓全部条目。批量 80 alias/批。

### 坑 5:基线时序
"今天的快照"写盘后才出报告——若报告时才选基线,会选中刚写的自己(全 0 增量)。
对策:main() 一进来就把基线定死(上一份 snap-*.json,否则最近一份 catalog-*.json)。

### 坑 6:npmjs 限流的"静默零"(上游自己都栽过)
api.npmjs.org 约 40 个单独请求就限流,429 秒拒。若不重试,**scoped 包逐个并发
请求会大面积静默变 0**——上游 probe-downloads.mjs 注释记载 94/134 个 scoped 包
曾因此连续数天空返回。对策:`_get_json` 对 429/5xx 指数退避重试(1s 起,×2,
至多 6 次,尊重 retry-after),404 才视为"包不存在"(返回 None,语义上等于
未发布,不是失败);scoped 低并发(3)即可——对限流器而言并发只烧配额不提速。
同理,校验器里 registry 元数据 404 = 未发布,要显式判 None,不能当 dict 解析。

## 4. 运行方式

```sh
python3 _digested/ecosystem/fresh_probe.py            # 采集 + 打印增量报告
python3 _digested/ecosystem/fresh_probe.py --quiet    # 只采集
```

- 时机:每次 `_change_log` 同步后跑一次;或想看趋势时随时跑(快照按日期落盘,可任意间隔对比)。
- 产出:`_snapshots/snap-<UTC 日期>.json`(url → npm 名/月下载/stars/pushedAt/archived)。
- 配额: contents API 只在首次/新条目时回源(缓存命中为 0),GraphQL 45 批,
  npmjs 无配额压力。单次全程约 5 分钟。
- 依赖:`gh auth login` 已完成;Python 3 标准库。

## 5. 快照目录

| 文件 | 是什么 |
|------|--------|
| `catalog-2026-08-25.json` / `catalog-2026-09-07.json` | npm catalog 转储(基线锚点,上游发布已停故存档) |
| `snap-<date>.json` | 本管线自采快照(趋势主数据,随时间累积) |
| `raw-name-cache.json` | 回源包名缓存(含 null,避免重复烧 contents 配额) |

## 6. 首跑基线数据(2026-09-12,供后续对照)

- 覆盖:npm 可归因 2558/3552(72%);不可归因 994(22%,未发布/撞名弃用,测过
  抽样属正确丢弃);stars 3540/3552;有下载 1778(50%),双无 349(10%)。
- 09-07 → 09-12 五日增量(月窗口):总量 532 万 → 569 万(+7%)。
- 增量类目:ui 23.5% · remote 15.7% · usage 14.4% · market 14.2% · tools 13.5% · memory 12.4%。
- 增量榜前段:dsh-market(+4.2万)、better-sidebar(+3.7万)、dsh-web 五子包(各 +2.1~2.4 万,7422★)、
  server-deck(402→1.8万)、token-usage-stats(1176→1.5万)、dsh-context(+1.2万)、cost-meter(+9.7千)。
