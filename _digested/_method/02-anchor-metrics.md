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

## 3. 实时快照(`live-2026-11-19.json`)

卡片里的"实时星标/下载"过去是逐条查、逐条写,没有落盘。现在统一归档:

```text
_digested/ecosystem/_snapshots/live-2026-11-19.json
```

结构:

```json
{
  "asof": "2026-11-19",
  "generated_at": "2026-11-19T...Z",
  "method": "gh api repos/{repo} + api.npmjs.org downloads/point/last-month/{pkg}",
  "repos": {
    "owner/repo": {"stars": 0, "pushed_at": "...", "archived": false, "default_branch": "main"}
  },
  "repo_packages": {"owner/repo": "pkg"},
  "packages": {
    "pkg": {"downloads": 0, "start": "...", "end": "..."}
  },
  "coverage": {"repos": "N/M", "packages": "N/M", "unpublished": [], "errors": []}
}
```

**引用规则**:

- 卡片正文里的 2026-11-18 读数保留其原始日期,不冒充 11-19;最新统一快照以 `live-2026-11-19.json` 为准,差异见 `_data/health.md`。
- 历史值一律带 ⚠ 与 `2026-08-19`;实时值必须能对应到本快照的 `asof`。
- 快照没有覆盖到的条目,写"缺口",不写 0。
- 快照只证明"某天的读数",不证明趋势;趋势仍需两次以上同口径快照。

复现命令(需要 `gh auth login`;npm 端点无鉴权):

```sh
python3 _digested/ecosystem/live_probe.py --asof 2026-11-19
```

脚本默认覆盖:全部卡片仓库 + `data/stars.json` 里星标最高的 80 个仓库 + 下载边车
前 40 个仓库;去重后逐仓请求 REST。包名先取 `raw-name-cache.json`,卡片仓库缺失时
回源 `package.json`。任何单仓/单包失败只记入 `coverage.errors`,404 的 npm 包记入
`coverage.unpublished`,不写 0,不中断整轮。

2026-11-19 实跑:**repos 107/108**(1 个 404:`revolutionla/dsh-dream-skin`)、
**packages 39/52 已发布 + 13 unpublished**;`unpublished` 不等于“没人用”,只说明
该包名在 npm 上不存在或解析错了。

## 4. 时效口径(与 `_method/01` 对齐)

| 数据 | 最后完整快照 | 引用时必须写 |
|------|--------------|--------------|
| 结构(条数/类目/owner/标签) | 当前 checkout(`census.py`) | commit + 运行日期 |
| 仓库边车 stars/downloads | 2026-08-19 | ⚠ + 日期;覆盖率(1410/596) |
| 自采 stars | 2026-09-30 | ⚠ + 日期;覆盖 4385/4392 |
| 自采 downloads | 2026-09-12 | ⚠ + 日期;覆盖 3552 名单 |
| 卡片逐条实时值 | `live-2026-11-19.json` | `asof` + 覆盖状态 |
| capabilities | 2026-09-24 | ⚠ + 日期;覆盖率 47.5%(旧基线) |

**禁止**:把不同日期的两个数放进同一个"增量"句子;把"新增头部为空"写成"无影响力";
把 `delta.py` 的候选数直接写成"接入数"。

## 5. 什么时候重跑

- 每次 `_change_log` 同步后:先 `census.py` 核分母,再 `live_probe.py` 刷卡片/锚快照;
- 只改文案、不动数据的轮次:不重跑,但要在页面顶部保留 `asof`;
- 网络失败:保留旧快照,把失败写进 `coverage.errors`;不要把失败写成 0。
