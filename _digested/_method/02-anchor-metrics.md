# 方法 02 · 锚的两轴:提及、扩散与实时快照

> **为什么有这份文档**:2026-11-19 复核发现,③b 的旧口径把"URL 里含 token"当成锚自身,
> 导致 `dsh-hindsight-*` / `dsh-openviking-*` 这类同名衍生被误排除——`openviking` 报 0(实际 3)、
> `hindsight` 报 2(实际 9)、`better-sidebar` 报 63(实际 64)。这不是数字小错,是把最强的
> 扩散信号静默压掉了。本文固定新口径,并说明"提及"与"采纳"的边界。

## 1. 三层候选,不是三个结论

`delta.py` ③b 现在按**仓库身份**排除锚自身,再把第三方命中分成两层:

| 层 | 判定 | 例子 | 能说明什么 |
|----|------|------|------------|
| 锚自身 | `repo_key == 锚仓库` | `omdsh-dev/DSH-better-sidebar` | 必须排除;monorepo 的多个子条目都算自身 |
| 同名候选 | 第三方仓库名的最后一段含 token | `All3nCN/dsh-better-sidebar-N23`、`yffo/dsh-engramory-recall` | 最像 fork / 同名衍生,但仍可能是无关项目 |
| 描述候选 | 只有 name 字段或描述含 token | `Lzh3070/dsh-file-review-tab` 描述里提 better-sidebar | 只是"提到",不等于依赖 |

**这三层都是候选,不是采纳。** 同名可能是撞名(如 `auto-memory` 撞 Claude Code 的同名特性),
描述可能只是"清理 X 的缓存"或"类似 X"。最终数字必须回到卡内逐条判定,并在卡里写清
`grep` 命令与排除理由。

`delta.py` 的输出只负责**给出候选和分层**,不再直接印一个"第三方提及 N"让人引用。
复现:

```sh
python3 _digested/ecosystem/delta.py 29b3ed46e 8f1a1800e
python3 -m unittest _digested/ecosystem/test_delta.py
```

`repo_key()` 处理这些 URL 形态:`/owner/repo`、`/owner/repo#sub`、`/owner/repo/tree/<branch>/sub`、
`repo.git`、大小写差异;非 GitHub URL 返回 `None`。回归测试覆盖了这些形态与
"同名衍生不得算自身"的用例。

## 2. 提及 → 采纳:卡片负责最后一公里

`_view/03-anchors.md` 与领域册引用扩散数时,必须带三层限定:

1. **口径**:是 `grep -ril` 的命中,还是 `delta.py` 候选分层?
2. **性质**:同名 fork、描述提及、还是代码级依赖/`peerDependencies`?
3. **抽样**:如果只浅克隆了 3 个,就只能说"抽样中 1 个硬依赖",不能说"63 个接入"。

已修正的典型:

- better-sidebar:**64 个第三方条目提及**(1 个同名 fork + 63 个描述);
  2026-11-18 抽样 3 个 → 1 硬依赖、1 软依赖、1 只提不用。结论是"平台候选",不是"平台型"。
- hindsight:**9 个第三方条目**(7 个同名 + 2 个提及);卡内判定只有 4 个真实现记忆工具,
  其余是控制台/生命周期工具。结论是"标准候选",不是"9 个衍生都接入了"。
- session:message-edit 3 个第三方引用(2 fork + 1 vendor 集成)、billion-context 6 个;
  七个方向仍然**没有可被复用的协议面**。"零协议复用"不等于"零提及"。

## 3. 实时快照与三层分层雷达(`live-*.json` / `radar-*.json` / `stars-*.json`)

过去全量 `fresh_probe.py` 连续五轮未跑,根本瓶颈不是查星标,而是对约 9,000 个未缓存包名的仓逐个调 GitHub REST `contents` API 读 `package.json`,直接撞穿 5,000/hr 限额。2026-11-27 起改为**三层分层采集**:

| 层 | 脚本与命令 | 覆盖与成本 | 落盘产物 |
|---|---|---|---|
| **Tier 1 · 卡片与存量锚全量** | `python3 _digested/ecosystem/live_probe.py --asof YYYY-MM-DD` | 全部已立卡仓库(当前 46 卡) + 星标边车 Top 80 + 下载边车 Top 40;REST + npm 下载 | `_snapshots/live-YYYY-MM-DD.json` |
| **Tier 2 · 增量/全库纯 GraphQL 星标** | `python3 _digested/ecosystem/radar_probe.py --delta <old> <new> --asof YYYY-MM-DD` 或 `--full` | 80 仓/批仅取 `stargazerCount/forkCount/createdAt/pushedAt/isArchived/isFork`;扫一期新增(~1,400 仓)仅 ~17 次请求(~15 秒),扫全库(~12,600 仓)仅 ~158 次请求(~3 分钟) | `_snapshots/radar-<old>-to-<new>-YYYY-MM-DD.json` · `_snapshots/stars-YYYY-MM-DD.json` |
| **Tier 3 · 过线新苗子补 npm 下载** | 随 `radar_probe.py --delta` 自动执行(`--star-threshold 30`) | 仅对星标 ≥30 的新增仓回源 `package.json` + `api.npmjs.org` 月下载,把 REST 配额集中在真冒头候选 | 同 `radar-*.json` 内的 `packages` / `ranked` |

**来源启发式打标(`origin`)**:`radar_probe.py` 按仓库 `createdAt` 与 URL 形态自动标记四类来源,防止把老主项目误读为原生新苗子:

- `pre-dsh-host`:仓库创建于 DSH 诞生日(`2026-08-13`)之前,高星大概率属主项目背书;
- `monorepo-subpath`:条目指向仓库子目录(`#` 或 `/tree/`),星标属整个 monorepo;
- `github-fork`:仓库为 GitHub fork;
- `dsh-native`:2026-08-13 后创建的非 fork 独立仓库(仍需读源码核实是否仅包外部服务)。

**引用规则**:

- `view_data.py` 自动选取 `_snapshots/live-*.json` 中最新一份(可用 `--snap` 显式覆盖),且 `stale-candidate(>90d)` 相对快照 `asof` 日期计算,不随本地时钟漂移;
- 历史边车值一律带 ⚠ 与 `2026-08-19`;实时值必须标明对应快照的 `asof` 日期与覆盖率;
- 快照未覆盖或 npm 返回 404(`unpublished`)一律记 `—` 或缺口,**不写 0**;
- 单次快照只证明某日截面,趋势仍需两次以上同口径快照对照。

## 4. 时效口径(与 `_method/01` 对齐)

| 数据 | 最后完整快照 | 引用时必须写 |
|------|--------------|--------------|
| 结构(条数/类目/owner/标签) | 当前 checkout(`census.py`) | commit + 运行日期 |
| 仓库边车 stars/downloads | 2026-08-19 | ⚠ + 日期;覆盖率(1408/596) |
| 卡片与存量锚实时值(Tier 1) | 最新 `live-YYYY-MM-DD.json` | `asof` + 覆盖率(见 `_data/health.md`) |
| 增量新苗子雷达(Tier 2+3) | `radar-29b3ed46e-to-8f1a1800e-2026-11-27.json` | `asof` + 覆盖率(1387/1395) + `origin` 口径 |
| 全库纯 GraphQL 星标(Tier 2 full) | `stars-2026-11-27.json` | `asof` + 覆盖率 |
| 全量自采 downloads | 2026-09-12 | ⚠ + 日期;覆盖 3552 名单 |
| capabilities | 2026-09-24 | ⚠ + 日期;覆盖率 28.5%(3745/13136) |

**禁止**:把不同日期的两个数放进同一个"增量"句子;把 `pre-dsh-host` 的老主项目高星写成“DSH 原生爆发”;把 `delta.py` 的候选数直接写成"接入数"。

## 5. 什么时候重跑

- 每次 `_change_log` 同步后:① `census.py` 核分母 → ② `live_probe.py --asof <today>` 刷全部卡片 → ③ `radar_probe.py --delta <old> <new> --asof <today>` 扫本期新增苗子 → ④ `view_data.py` 更新 `_data/`;
- 按需(每隔 2–3 轮或需要重排全库星标时):`radar_probe.py --full --asof <today>` 刷全库纯 GraphQL 星标;
- 只改文案、不动数据的轮次:不重跑,但要在页面顶部保留 `asof`;
- 网络失败:保留旧快照,把失败写进 `coverage.errors`;不要把失败写成 0。
