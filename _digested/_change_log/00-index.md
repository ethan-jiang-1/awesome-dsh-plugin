# Change Log · 上游同步记录

这个目录是整套消化的**核心纪律所在**：每次从 `upstream`(`awesome-dsh-plugin/awesome-dsh-plugin`)同步到本地 `ethan` 分支,都写一条记录,并据此判定哪些既有结论已过期。没有这里,_digested/ 会随上游漂移悄悄烂掉。

## 为什么它是核心

- 它把「研究基线」变成可执行的动作:合入 → 记录 → 判定影响 → 逐专题复核 → 更新覆盖矩阵。
- 「对消化材料的影响」判定表是强制项:**每个专题都要给一句理由**,不许含糊地说"可能有影响"。
- 复核完成后要回写日期与核对点,形成闭环。

```text
_change_log/
├── 00-index.md
├── 0000-baseline.md                    # 研究起点，不是一次同步
├── 0001-5e7dc7eb-to-38976afd.md        # 15 天 / 3213 commits / 2286→3552 条
├── 0002-38976afd-to-c18ba4a0d.md       # 18 天 / 1436 commits / 3552→4392 条
├── 0003-c18ba4a0d-to-4693e5a83.md       # 18 天 / 216 commits / 4392→4489 条
├── 0004-4693e5a83-to-b4d0049a8.md       # 13 天 / 3450 commits / 4489→6704 条 (+2215)
└── 0005-b4d0049a8-to-efe602e7b.md       # 7 天 / 2149 commits / 6704→7924 条 (+1220)
```

编号递增。`0000` 只记录开始消化时的 checkout；同步记录从 `0001` 起。本仓库没有版本号，所以文件名用短 hash 对：`0004-4693e5a83-to-<new>.md`。

> **取数通道(截至 0004)**:每次先 `ls-remote` 探活再 fetch,但**哪个协议当天能用是浮动的**。0004 实测:SSH `ls-remote`(git@github.com)挂死 45 s 以上;https `ls-remote` **秒回**;https fetch 默认 lowSpeed 阈值会因低速失败,tune 后成功:
> ```sh
> git ls-remote https://github.com/awesome-dsh-plugin/awesome-dsh-plugin.git main
> git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=60 fetch --no-tags \
>   https://github.com/awesome-dsh-plugin/awesome-dsh-plugin.git main:refs/remotes/upstream/main
> ```
> 该 fetch 用了约 5 分钟(经 tail 管道时不刷新进度,容易误判成卡死;用 `job_output` 等它结束)。macOS 没有 `timeout` 命令,别指望用它兜底。
>
> **0005 实测**:同一套 https `ls-remote` + 调优参数 `fetch` 一次成功(7 天 2149 提交、1535 文件)。这一轮**源码零 diff**——`scripts/`、`site/`、`.github/workflows/`、`package.json` 全未动,变化只有名单(+1281/−61)与 `contributing.md` 一节文档;因此六个机制专题按「无对应 diff」处理,唯一例外是 submission-gates 的文档段。另:`census.py` 增加了 JSON-in-.yml 回退(本轮 2 条新条目实际是 JSON),否则分母会静默少 2。

## 每条 sync 记录的固定结构

```markdown
# 同步 NNNN:`<from-short>` → `<to-short>`

**日期**:YYYY-MM-DD
**upstream**:`awesome-dsh-plugin/awesome-dsh-plugin` `main`
**from**:<full-hash>(合并前 ethan 所对齐的 upstream tip)
**to**:<full-hash>(本次合入后的 upstream tip)
**提交数量**:N(git rev-list --count from..to,能数清时)
**工作树**:files / +行 / −行(git diff --stat 汇总)
**合入方式**:merge 命令、merge commit、有无冲突、研究目录是否保留完好

## 核心变更
一段叙述 + 按主题归类表(| 主题 | PR | 落点 |),末尾给源码侧主要落点清单。

## 对消化材料的影响
| 专题 | 判定 | 原因 |
判定只许取值:「需复核」/「已核验」/「无对应 diff」,必须每专题一行。
```

## 每次 sync 的维护动作(缺一不可)

1. 在本目录新增一条记录,按上面结构写全。
2. 更新 [`../00-index.md`](../00-index.md) 顶部的产品源码审计基线。
3. 按「对消化材料的影响」表,在 [`../_coverage/00-index.md`](../_coverage/00-index.md) 将受影响专题改回「需复核」;完成源码复核后再更新其最近核验 commit。若上游同步删除研究目录,先从合并前研究分支恢复本地材料,不得把它当作 upstream 内容接受。
4. 复核 `_faq_on_digested/` 中受波及的答案。
5. 运行 `node _digested/verify.mjs`。

复核完成后,在当条记录末尾回写一行:复核日期 + 核对到的短 hash。
