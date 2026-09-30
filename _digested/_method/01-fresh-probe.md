# 方法 01 · fresh_probe 数据管线(新鲜下载/星标自采)

> **为什么有这份文档**:做"真实下载/热度趋势"时,仓库边车不可用、catalog 会停更、
> 公开 API 有各自的坑——下面每一条都是实际踩过并验证过的。脚本本体
> [`fresh_probe.py`](../ecosystem/fresh_probe.py) 已固化这些对策;本文记录"为什么必须这样"。
> 首次跑通:2026-09-12,基线 `main@38976afd`。总纲见 [`00-index.md`](00-index.md)。

## 1. 数据源层级(重要程度递增)

| 源 | 新鲜度 | 问题 | 用途 |
|----|--------|------|------|
| 仓库边车 `data/downloads.json` 等 | **冻结**(0001 实测:15 天 3213 commits 只变 6 行,下载榜数字与 08-26 完全一致;**0002 复核:提交版 624 行的 `checkedAt` 全部停在 2026-08-19,且没有 `start/end` 字段**——它连"这是哪 30 天"都答不出来) | 真实数据活在 Actions cache,仓库里的是快照的快照 | 只看历史锚点 |
| `dsh-plugin-catalog` npm 包 | 每夜 | **发布会停**(09-08 后停更,#3512 型故障同征);且"下载量"是包发布时刻快照 | 备用基线,取法 `npm pack dsh-plugin-catalog@<ver> --cache <自建目录>`(系统 npm cache 可能 root-owned 报 EPERM) |
| **自采:公开 API**(本管线) | 实时 | 无停更风险;坑见下文 | 趋势分析的唯一可靠源 |

## 2. 本机网络环境约束(2026-09-12 实测,换机器需重测)

| 通道 | 状态 | 对策 |
|------|------|------|
| `git fetch` https | **挂死**(60s/180s 双超时) | 走 SSH:`git fetch git@github.com:<org>/<repo>.git main:refs/remotes/upstream/main` |
| `raw.githubusercontent.com` | **完全不可达**(000) | npm 包名改经 `api.github.com/contents` 取 package.json |
| `api.github.com` / `gh api` | 通(gh CLI 已认证,5000/hr) | GraphQL 星标、contents API 都走它 |
| `api.npmjs.org` / `registry.npmjs.org` | 通,无鉴权 | 下载量、包名归属校验 |

## 3. 六个坑与对策(脚本内的不变量)

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
**实测 3552 条里有 npm 名 2780,其中 772 条(22%)未发布到 npm,另约 222 条因名字撞名被弃用——两者合计 994 条(28%)不可归因**——
这是生态真实属性(github/tarball 安装通道),不是 bug。但它们必须**退出增量
统计**,否则会制造 d0>0→d1=0 的假负增量污染类目流向。

> **0002 勘误**:本文旧版把 994 与 22% 写在一起(994/3552 实为 28%,22% 只属于
> 772 这个子集),03-growth-maturity §4 也已同步更正。

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

### 坑 7:长尾回源的两种"静默杀手",以及"未知被固化成否定"(0002 新增)
条目从 2286 涨到 4392 后,每轮首次回源的 `package.json` 从几百条涨到 **942 条**,
于是 0002 的第一次自采跑了三轮才成功——每轮都死在不同的异常上,而且**每轮都从零开始**:

- **(a) `http.client.RemoteDisconnected`**:连接被对端掐断,它是
  `ConnectionResetError`(OSError)的子类,**不是** `URLError`。旧代码只捕获
  `(URLError, HTTPError, JSONDecodeError, TimeoutError, ValueError)`,于是它直接
  掀掉整轮采集;
- **(b) `http.client.IncompleteRead`**:响应体读一半就断,它是 `HTTPException`
  **既不是 OSError 也不是 ValueError**——第二轮的杀手。两处现在都显式列出
  `http.client.HTTPException` 并做指数退避重试;
- **(c) "未知"被写进缓存**:旧代码把回源失败也 `cache[u] = None`,而
  `None` 在本脚本里的语义是"没有 npm 名"——于是一次网络抖动会把某条目**永久**
  固化成"未发布",下轮不再回源。这违反本目录的第一条铁律。现在失败**不写缓存**,
  下轮自动重试,并在日志里点名;
- **(d) 缓存只在整轮跑完后落盘**:前两条导致 900+ 次成功回源全部作废。现在每
  200 条增量落盘,单次失败的代价从"整轮"降到"一条";
- **(e) `urlopen(timeout=…)` 管不到 DNS 解析**:回源阶段与"逐包校验"阶段都在
  无输出状态下静默停摆过(最长 40 分钟),而同一时刻 `ls-remote`、单次 curl
  都秒回。对策是**给每个调用套一层硬期限**(在独立 daemon 线程里跑,超时就
  丢弃该线程继续),并且**把期限套在 worker 内部**——套在消费端
  (`f.result()`)是无效的:`as_completed` 要等某个 future 完成才会让出,
  12 个 worker 全卡住时消费循环一次都不执行,预算也就永远不触发;
- **(f) 校验阶段要有预算**:`registry.npmjs.org` 从本机实测单请求 1–20s 且
  间歇超时,1128 个唯一包名逐个问一遍可能要一小时。现在给它
  `VALIDATE_DEADLINE_S=60`(单条)+ `VALIDATE_BUDGET_S=1800`(整体)+
  并发 10;预算用尽后**退回"元数据不可用"那条分支**(名字含 `dsh` 或按
  owner 作用域命名则通过),而不是无条件丢弃——校验每轮重跑,下轮自动补。

**教训(可迁移)**:长尾采集的失败模式不是"某一条错了",而是"**整轮归零 + 把未知
写成否定 + 下次不再重试**"三件事叠在一起。修的时候要同时修三层:异常覆盖、语义
(未知 ≠ 否定)、持久化时机;而"卡住"这一层还要额外区分**请求超时**与
**解析/DNS 卡死**——后者只能用调用级硬期限兜,且期限必须落在 worker 上。

### 环境可用性本身是数据源的一部分(0002 新增)
本轮(2026-09-30)的采集**未能完整产出快照**:包名回源(942 条)在第一轮被
`RemoteDisconnected` 打死、第二轮被 `IncompleteRead` 打死(修完这两处后才通过),
随后的 `registry.npmjs.org` 校验与 npm 下载端点又大面积超时。结论不是"管线坏了",
而是**自采管线的产出依赖网络窗口**:引用自采数字时,必须连同"它是哪一天、跑通没跑通"
一起说明。本轮结构性数字(npm 可归因 3387/4392、星标覆盖 4385/4392)来自跑通的部分,
下载/星标区间数则仍停在 2026-09-12 快照。

## 4. 运行方式

```sh
python3 _digested/ecosystem/fresh_probe.py            # 采集 + 打印增量报告
python3 _digested/ecosystem/fresh_probe.py --quiet    # 只采集
```

- 时机:每次 `_change_log` 同步后跑一次;或想看趋势时随时跑(快照按日期落盘,可任意间隔对比)。
- 产出:`_digested/ecosystem/_snapshots/` 下的 `snap-<UTC 日期>.json`(url → npm 名/月下载/stars/pushedAt/archived)。
- 配额: contents API 只在首次/新条目时回源(缓存命中为 0),GraphQL 45 批,
  npmjs 无配额压力。
- 耗时(0002 修正):**不再是"约 5 分钟"**。条目涨到 4392 后,首次回源 942 条、
  包名校验 1128 个唯一名字、下载 2580 个非 scoped + 约 780 个 scoped。在网络
  正常时约 15–20 分钟;**网络抖动时任一阶段都可以是小时级**(见 §3 坑 7);
  缓存热之后重跑只需走下载+星标。
- 依赖:`gh auth login` 已完成;Python 3 标准库。

## 5. 快照目录

| 文件 | 是什么 |
|------|--------|
| `catalog-2026-08-25.json` / `catalog-2026-09-07.json` | npm catalog 转储(基线锚点,上游发布已停故存档) |
| `snap-2026-09-12.json` | **最后一个完整自采快照**(3552 条基线;0002 的下载采集未完成,见 §6) |
| `stars-2026-09-30.json` | **0002 星标快照**(仅星标/pushedAt/archived,无下载;4385/4392,99.8%) |
| `snap-<date>.json` | 本管线自采快照(趋势主数据,随时间累积) |
| `raw-name-cache.json` | 回源包名缓存(含 null,避免重复烧 contents 配额;0002 起**失败不写缓存**) |

## 6. 基线数据(0001 = 2026-09-12,0002 = 2026-09-30)

**0001(完整跑通,3552 条)**:覆盖 npm 可归因 2558/3552(72%);不可归因 994(28%,= 未发布 772 + 撞名弃用约 222,测过抽样属正确丢弃);stars 3540/3552;有下载 1778(50%),双无 349(10%)。09-07 → 09-12 五日增量(月窗口):总量 532 万 → 569 万(+7%);增量类目 ui 23.5% · remote 15.7% · usage 14.4% · market 14.2% · tools 13.5% · memory 12.4%;增量榜前段 dsh-market(+4.2万)、better-sidebar(+3.7万)、dsh-web 五子包(各 +2.1~2.4 万,7422★)、server-deck(402→1.8万)、token-usage-stats(1176→1.5万)。

**0002(2026-09-30,4392 条)部分跑通**:

- **结构层拿到了**:包名回源 942 条全部完成(修复 RemoteDisconnected/IncompleteRead 之后),
  最终**可归因 3387/4392(77.1%)**、不可归因 1005(两轮读数 3372 / 3387,**差异全部来自校验
  阶段对 registry.npmjs.org 的请求超时**,超时的名字退回"含 dsh 才通过"的保守规则);
- **星标拿到了**:`gh` GraphQL 重采,覆盖 **4385/4392(99.8%)**,中位 2、均值 89.4、
  ≥100★ 164 条、archived 17;
- **下载没拿到**:bulk 端点与 scoped 逐个请求在本轮窗口内大面积超时,快照未落盘。
  因此 [04](../ecosystem/04-value-trend.md) §2/§3/§5/§7 的下载比例与
  [03](../ecosystem/03-growth-maturity.md) §4 的下载覆盖**仍是 09-12 口径**,文中已逐处标注;
- **本轮的方法收益**(比数字更重要):七个坑全部是一次真跑出来的,见 §3;并且确立了
  "自采快照的可用性依赖网络窗口,引用时必须说明它是哪一天、跑通没跑通"这条纪律。
  另一个教训:**同一份代码、间隔几分钟的两轮采集,星标覆盖可以差 13 个点**
  (86.4% → 99.8%)——GraphQL 整批静默失败时会表现为"覆盖率掉了一截"。
  **覆盖率异常时,先用第二次运行排除采集本身,再下生态结论。**
