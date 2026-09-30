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
└── 0002-38976afd-to-c18ba4a0d.md       # 18 天 / 1436 commits / 3552→4392 条
```

编号递增。`0000` 只记录开始消化时的 checkout；同步记录从 `0001` 起。本仓库没有版本号，所以文件名用短 hash 对：`0002-38976afd-to-<new>.md`。

> **取数通道(截至 0002)**:`git fetch` 的长连接会挂死且换协议不保险——0001 是 https 挂死、SSH 可用;0002 连 SSH fetch 也挂死,而 `ssh -T` 与 `git ls-remote https://…` 都秒回。**先 `ls-remote` 探活,再**用带低速阈值的 https fetch:
> `git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=30 fetch upstream main:refs/remotes/upstream/main`

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
3. 按「对消化材料的影响」表,在 [`../_coverage/00-index.md`](../_coverage/00-index.md) 将受影响专题改回「需复核」;完成源码复核后再更新其最近核验 commit。
4. 复核 `_faq_on_digested/` 中受波及的答案。
5. 运行 `node _digested/verify.mjs`。

复核完成后,在当条记录末尾回写一行:复核日期 + 核对到的短 hash。
