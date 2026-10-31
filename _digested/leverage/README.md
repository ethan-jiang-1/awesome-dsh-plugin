---
title: "leverage · 影响面与杠杆"
domain: layer
kind: index
positioning: "本层唯一入口：说明这套研究回答什么、文件怎么分工、按目的怎么读。"
read_when: "第一次进这个目录；或不确定该读哪一篇时。"
status: living
updated: 2026-10-31
budget: 260
---
# `leverage/` · 影响面与杠杆(第二轴)

> **一句话**:[`ecosystem/`](../ecosystem/00-map.md) 回答「有什么」;这一层回答「**它占了哪条缝、改到多深、代价是什么、什么时候会坏、别人能抄哪一行**」。
> **不是**:插件推荐榜、功能分类、安装教程。它是**深读层**——**不是每一条都值得研究**:先过门,再立卡。
> **状态**:三域成稿（产品线另册：[`../leverage-reshape-product/`](../leverage-reshape-product/README.md)） ｜ 篇数以 [catalog](./catalog.md) 为准 ｜ 基线:名单 `efe602e7b`(2026-10-31) · DSH `0.2.1-rc.3`

## 0. 三个入口

| 你要什么 | 去哪 | 你会拿到 |
|---|---|---|
| **拿走东西**(写插件/评审/选型) | **[BORROW](./BORROW.md)** | 8 条任务路由 + 三域最小集 + 6 条跨域法则 + 7 问 + 陷阱 |
| **查某一篇** | **[catalog](./catalog.md)** | 全部文件的 kind / 定位 / 能拿走什么 / 什么时候读,可直接 grep |
| **知道凭什么** | **[horizon](./horizon.md)** | 准入门 A–G、分级 S/A/B/C、每条必写的六项 |

**只读一次的话**:打开 [BORROW](./BORROW.md) §1,找到你那一行,按它给的出处读。**不要从目录树开始通读。**

## 1. 为什么有这一层

DSH 的扩展面是有限、可枚举的:seam(fs/shell/sandbox/llm/subagent/workflow…)、slot(sidebar/conversation/settings…)、layer(profile/bundle/patch)、policy、preset、protocol。**插件的影响面,取决于它占了哪类位置,而不取决于它提供了多少工具。**

所以评估要问「它占了什么位置」,分类回答不了这个问题:同属 UI 类的两个插件,一个只换配色,一个把产品形态改掉。

**本层的验收判据**:把任意一篇卡给一个没读过该插件的工程师,他能不能在半天内做出一个**形状对、细节对、知道哪里会塌**的实现。做不到就是深度不够。

## 2. 读之前:五个最容易读错的地方

1. **三域不是分类树。** 一个样本可以同时出现在多个域(重叠 41–44%);「属于哪个域」取决于你问哪个问题。
2. **计数不是证据。** 名单一直在涨,任何 `N / 总数` 明天就变;所以本层不写命中数,只写「谁被谁提到」「替代了哪个官方对象」「哪条缝」这类可回读的事实。**「稀缺 / 唯一」是人工判断,标 `[OBS]`。**
3. **能力披露缺失 ≠ 安全,空披露 ≠ 无能力。** `capabilities.json` 是 2026-09-24 的静态扫描;披露 / 策略 / 强制 / 判决是四件事。
4. **星标、下载、实时 API 是三套数。** 引用必须带日期;星标 ≠ 使用量;npm 包名 ≠ 仓库名。
5. **BORROW 的 `[OBS]` 法则是综合判断。** 引用请引一手卡片;`inferred` 的断言不要写成 `observed`。

## 3. 目录长什么样

目录里只有三种东西:

| 层 | 是什么 | 会长吗 | 约束 |
|---|---|---|---|
| **骨架** | 本文件、[00-map](./00-map.md)、[horizon](./horizon.md)、[BORROW](./BORROW.md)、三域 README | **不随样本长** | 行数预算(frontmatter `budget`),超了要删/移 |
| **叶子** | `card` / `sample` / `_证据/` | 随便长 | 每篇 frontmatter + 借用节 |
| **文档** | [catalog](./catalog.md) | 手工补 | 加卡时补一行;数量不在这里维护 |

七种角色(frontmatter `kind`):

| kind | 是什么 | 例子 |
|---|---|---|
| `index` | 目录/索引 | 本文件、catalog、[CROSS-03](./lever-cross-boundary/03-sample-encyclopedia.md)、[PROVE-00](./lever-prove-output/00-sample-lineage.md) |
| `charter` | 规则页:收什么、怎么判 | 00-map、horizon、三域 README |
| `guide` | 借用总入口 | [BORROW](./BORROW.md) |
| `playbook` | 横向框架/手册 | [CROSS-01](./lever-cross-boundary/01-collab-topology.md)、[PROVE-10](./lever-prove-output/10-quality-control-playbook.md)、[LIMIT-09](./lever-draw-limit/09-control-budget.md) |
| `card` | 一个机制/环节/控制点一篇 | [PROVE-05](./lever-prove-output/05-custody-chain.md)、[LIMIT-03](./lever-draw-limit/03-second-model.md) |
| `sample` | 一个样本一篇 | [CROSS-07](./lever-cross-boundary/samples/07-Nwflower-dsh-file-claim.md)、[PROVE-02](./lever-prove-output/02-goal-gate-hard-floor.md) |
| `evidence` | 原始摘录,只作溯源 | 各域 `_证据/`（产品线的证据在 [`../leverage-reshape-product/`](../leverage-reshape-product/README.md)） |

## 4. 三个域:三个并列的问题（+ 一条产品线另册）

**分析单位不同**——这正是各目录长得不一样的原因,不是混乱。**产品线已独立成册**：`../leverage-reshape-product/`，不参与本层的三域统计。

| 域 | 一句话问题 | 分析单位 |
|---|---|---|
| [**产品线（另册）**](../leverage-reshape-product/README.md) | 从插件到 profile 到独立壳，怎么把 DSH 装成产品 | 19 张样本卡（不参与本层统计） |
| [CROSS](./lever-cross-boundary/README.md) | 协作跨到哪个边界,每跨一界多付什么 | 一个协作样本(一样本一文件)+ 横向卡 |
| [PROVE](./lever-prove-output/README.md) | 门禁装在哪一环,产物凭什么算完成 | 一个门禁位置(一环一卡) |
| [LIMIT](./lever-draw-limit/README.md) | 谁能碰什么,由谁强制,留下什么证据 | 一个控制点/预算(一卡一样本) |

三域没有先后,学习顺序由这张表固定。**样本重叠是正常的**:独立性靠「主读单一归属 + 不引用他域结论」保证,不靠样本不重叠。

## 5. 怎么读

**按目的路由**(详细版在 [BORROW §1](./BORROW.md),这里只给入口):

| 你要干什么 | 先读 |
|---|---|
| 做产品（插件 / profile / 独立壳） | [产品线 README](../leverage-reshape-product/README.md)（另册） |
| 做多 agent / 跨机 | [CROSS README](./lever-cross-boundary/README.md)「能借鉴什么」 |
| 做质量门禁 | [PROVE-01](./lever-prove-output/01-quality-chain.md) 六环 → [PROVE-10](./lever-prove-output/10-quality-control-playbook.md) |
| 做安全/权限 | [LIMIT README](./lever-draw-limit/README.md)「借法一览」→ [LIMIT-09](./lever-draw-limit/09-control-budget.md) |
| 选一个装上 | catalog 的 `sample` 行 → 卡的失败模式/评估清单 |
| 评审别人的方案 | [BORROW §4](./BORROW.md) 七问 + 各卡评估清单 |
| 继续挖 / 回源 / 提缺口 | [BORROW §6](./BORROW.md) + [horizon](./horizon.md) §8 |

**给 agent 的五条检索式**(不用读全目录):

```sh
sed -n '1,80p' _digested/leverage/catalog.md # 全量菜单（手工维护）
grep -rl '^kind: sample' _digested/leverage --include='*.md' # 只要样本卡
grep -rn '^read_when:.*冲突' _digested/leverage --include='*.md'
grep -rn -E '^#{2,3} .*(借鉴|搬走|借用|照抄|食谱|配方|移植)' _digested/leverage
node _digested/verify.mjs # frontmatter / 链接 / 锚点
```

## 6. 文件约定

**每一篇都有 frontmatter**,`verify.mjs` 校验九个键(`title` / `domain` / `kind` / `positioning` / `takeaway` / `read_when` / `status` / `updated` / `budget`)。完整定义与写入规则在 [00-map §文件约定](./00-map.md),这里只留三条:

1. **不放会漂的数字**(星标/下载/版本/基线日期)——留在正文页头。
2. **`card` / `sample` 必须有借用节**(标题含 借鉴/搬走/借用/照抄/食谱/配方/移植),否则 verify 失败。
3. **规则只有一个源**:准入/分级看 [horizon](./horizon.md);三域 README 里的副本是摘要,冲突以源为准。

**新增文件命名**:`<域>/NN-<ascii-slug>.md`;一样本一篇放 `<域>/samples/NN-<owner>-<repo>.md`。编号域内递增、不复用、不重排;退役保留编号改 `status`。**老文件不改名**(外部引用与锚点稳定)。

## 7. 证据、坐标与深度

**四个标签**(每条结论都标):

| 标签 | 含义 |
|---|---|
| `[DSH]` | 原生机制,引用 `@deepseek-ai/<pkg>@<version>` 的 README/配置 |
| `[CAT]` | 生态事实,引用 `owner/repo`;注明是 catalog 描述还是能力披露 |
| `[OBS]` | 观察者判断(可争论),必须给反例或失效条件 |
| `[OPEN]` | 未验证,留给下一轮 |

**几套时间口径,不可互证**:

| 口径 | 值 | 谁维护 |
|---|---|---|
| 名单 | `efe602e7b`(2026-10-31 快照) | [`ecosystem/`](../ecosystem/00-map.md) |
| 能力披露 | `data/capabilities.json`,2026-09-24 静态扫描 | 旧扫描,非判决 |
| 星标/下载 | 星标 2026-09-30、下载 2026-09-12 | `data/*.json`(历史锚点) |
| 实时 GitHub / npm | CROSS / LIMIT 采样 2026-10-31 | 各域 README |
| commit | PROVE 2026-10-31 14:00 CST | [PROVE-00](./lever-prove-output/00-sample-lineage.md) |

**证据强度分域,不能互推**:

| 域 | 源码 | 坐标强度 | 影响力口径 |
|---|---|---|---|
| 产品线 | 插件 README + 官方包 README | 无 commit | 另册 catalog + ★/下载快照 |
| CROSS | 14 样本逐文件读过 | 版本 + 实时数据,无 commit | 2026-10-31 实时 |
| PROVE | 读过(含打包产物) | **repo@commit** | 2026-10-31 抓取 |
| LIMIT | 多卡读过 src | 版本(dist-tags),无 commit | npm 近 30 天 |

**深度阶梯**(每级一跳,回源路径不会断):

| 层 | 你要的 | 去哪 |
|---|---|---|
| L0 | 一句话结论 | [BORROW §2/§3](./BORROW.md);域 README 标语 |
| L1 | 判断框架 | 域 README 骨架表 + 卡的「评估清单」 |
| L2 | 机制怎么落 | 卡的机制节 / 样本的「设计思路」 |
| L3 | 我该抄哪一行 | 卡的借用节 |
| L4 | 凭什么信 | 页头 `[DSH]`/`[CAT]`/`[OBS]` + 坐标 + 原文 |
| L5 | 一手源 | `repo@commit` / npm / 官方包 |
| L6 | 还没解决什么 | [BORROW §6](./BORROW.md) + 各域「待答」 |

**回源五步**在 [BORROW §6.4](./BORROW.md)。

## 8. 生长协议:加的是叶子,宪章不跟着长

| 变化 | 写哪里 | 不要动 |
|---|---|---|
| 新样本过门,S/A | 新卡(frontmatter + 借用节);catalog 补一行 | 所有骨架 |
| 新样本只到 B | 不立卡;域表一行对照,或不写 | 所有骨架 |
| C 级反例 | 对应卡失败模式表一行 | 所有骨架 |
| 现有 S/A 掉门 / 退役 | 该卡 `status` + 域表一行;保留编号,不删不改名 | 所有骨架 |
| 某条跨域法则被推翻 | [BORROW §3](./BORROW.md) 改一行 | 其他 |
| 新域出现 | 必须满足:新位置 + 多个过门样本 + 三域都装不下;才加目录/枚举/README 一行/BORROW 一行（产品线是另册，不在此列） | 三域正文 |
| 上游同步 | 只改受影响卡的 `updated` 与 `[DSH]` 断言 + 层级基线 | 其他 |
| 数字口径变 | 该域 README 基线说明 + 相关卡数字 | 其他 |

**五条不变量**:① 骨架不随样本数增长(`budget` + 只列 S/A);② 全量清单只维护一张(catalog),不散在各处;③ 借用层按任务分,不按样本分(BORROW 不随样本改);④ 一个样本只在一处完整论证;⑤ 编号域内递增、不复用、不重排。

## 9. 校验

```sh
node _digested/verify.mjs # frontmatter / 链接 / 锚点 / 编码
```

**只校验文件自洽,不校验计数**——名单在涨,任何全局数字都不是稳定真值。

## 三域并行作业契约

> **已归档**:四个域已经收工,本节只解释「为什么四份宪章的写法不一样」,并保留给引用它的域 README。日常阅读不需要它。

三域曾由三个彼此独立的会话分头研究。独立性靠结构,不靠约定:

| # | 约束 | 具体做法 |
|---|---|---|
| 1 | **自足** | 每个域的 README 自带准入、分级、本域基线说明;不引用其他域的结论 |
| 2 | **不写共享件** | 域会话只写自己的 `lever-*/`;共享件只读 |
| 3 | **主读单一归属** | 每份官方包、每个 S/A 样本只指定一个主读域;其他域可借一句,不深读、不立卡 |
| 4 | **声明式分界** | 重叠情形由本层事先裁定;域内只写划给自己的那一半 |
| 5 | **冻结基线** | 每域只引用 2026-10-31 快照 |

**这条契约的代价**:四份宪章有重复的准入段、四种不同的卡片骨架。**消除它们不是目标**——正文已经带证据行号,重写只会掉信息。现在用「规则单一源(horizon)+ frontmatter + catalog」把差异收在检索层,而不是把内容抹平。
