---
title: "研究对象怎么选：准入与分级"
domain: layer
kind: charter
positioning: "规则单一源：A/B/C/D/E/F/G 证据类型、S/A/B/C 分级、每条必写的六项。"
read_when: "要把一个新样本立成卡；或质疑某条样本凭什么在场时。"
status: observed
updated: 2026-10-31
budget: 230
---
# 研究对象怎么选:准入与分级

> **状态**:`observed`(规则已经被四域成稿检验过) · **更新**:2026-10-31 · **基线**:名单 `main@efe602e7b` · DSH `0.2.1-rc.3`
> **一句话**:**不是抓到一个插件就琢磨。** 能进这份研究的条目,先要证明自己「有影响力」,再证明自己「有深度」,然后才分级;排不进 S/A 的,只配当反面教材或旁支脚注。

## 0. 纪律:没有「通过率」

名单一直在涨。任何 `N / 总数` 的通过率都不是稳定真值,它只会让研究跟着名单一起膨胀。所以这一层**不设机器门、不设通过率、不设计数**;只设**证据类型**与**人工判断**。

三条硬规矩:

1. **无影响力证据 = 不进研究**(可以出现在脚注,不许有卡)。
2. **无深度证据 = 不进研究**;只有功能描述、说不出它动的是哪条缝的,一律算「工具」,归 `ecosystem/`。
3. **进不了 S/A 的不写卡**。B 级只做对照表的一行,C 级只做一句话脚注。**拒绝写的条目远比写下的条目多,这是设计,不是遗漏。**

**计数不是证据。** 「全库只有 3 条」这类断言会随名单涨而失真;真要用,只能写成「截至 `<日期>`,人工回读所见」并标 `[OBS]`。

## 1. 入口条件(两组,缺一不立卡)

| 组 | 代号 | 证据 | 怎么判 |
|---|---|---|---|
| 影响力 | **A 引用** | 被目录内其他条目按名提到 | 回读被谁提到;撞词不算 |
| 影响力 | **B 替代** | 自述**替换/接管官方对象**:profile、启动器、官方页面、官方默认行为 | 回读原文 |
| 影响力 | **C 接缝** | 点名**具名接缝**:`ctx.*`、`waterfall`、`/pre-step`、`/pre-execute`、`/post-execute` | 回读原文 |
| 影响力 | **F 少见** | 全库同类机制少见 | **人工判断**,标 `[OBS]`;不写命中数 |
| 深度 | **D 能力** | `capabilities.json` 有披露;空披露也算,但必须注明是「零依赖/纯前端」还是「扫描器没跑」 | 查能力边车 |
| 深度 | **E 反面** | 被同类插件**明指不可共存**,或同一接缝的**两种相反取法** | **人工认定** |
| 深度 | **G 已核** | 机制已读官方包 README 或源码,且能指出它的失效条件 | **人工**,写进卡的「机制」「失败模式」两节 |

**没有「四选一 / 三选一」的配方。** A/B/C/F 是四种可回读的影响力证据,D/E/G 是三种深度证据;**两组各至少一条**,且每条都要写清是哪一种。

## 2. 分级:S / A / B / C

| 级 | 名称 | 条件(在入口条件之上) | 在研究里的位置 |
|---|---|---|---|
| **S** | 定义型 | 影响力**至少两种**,**且**深度 G 成立,**且**它**定义了一个机制或一类做法**——后来者照着它的形状写 | 单独一张卡,进域宪章的「骨架」表 |
| **A** | 代表型 | 影响力**至少一种** **且** 深度 D+G 成立 **且** 它是所在边界/层上**目前最好的一个取法** | 卡片「标杆」表的正例 |
| **B** | 对照型 | 影响力**至少一种** **且** 深度 D 或 E 成立,但**只在某个维度上与 A 不同**(更省、更狠、更偏) | 卡片内一行对照,**不单独立卡** |
| **C** | 反例型 | E 成立:明指不可共存,或同一接缝取反 | 失败模式表里的一行 |
| ✗ | 不收录 | 影响力与深度都没过门 | 最多一句话脚注 |

**S 与 A 的唯一区别**:S 是「后来者的模板」,A 是「当前的优解」。一个插件可以在某个域里是 A、在另一个域里是 S——分级是**按域**的,不是按插件。

## 3. 每条必须交代的六件事

这是这一层最容易轻飘飘的地方,所以规定死:**任何进入卡片的样本,都要写齐六项,缺一项就退回不放**。

| # | 必写 | 具体要求 | 反例(会被退回的写法) |
|---|---|---|---|
| 1 | **它代表什么** | 一句话说清它是哪一类的样板,以及这一类在 DSH 里的边界 | 「一个很强大的团队插件」 |
| 2 | **为什么选它** | 指名它过的哪几条证据(A/B/C/D/E/F/G 的具体哪种),而不是「因为看着不错」 | 「社区口碑好」 |
| 3 | **影响力证据** | 给**可回读的事实**:被谁提到 / 替代了哪个官方对象 / 哪条具名接缝 / 能力披露。**不要求计数** | 「很流行」「很多人用」 |
| 4 | **主要特点** | 机制层面的特点:占了哪条缝、失败时往哪倒、代价是什么 | 「功能丰富」「体验好」 |
| 5 | **代价 / 失效条件** | 至少一条**具名**的失效路径(升级断裂、优先级暗战、绕过通道、依赖漂移) | 「有一定风险」 |
| 6 | **证据级别** | `[DSH]` 官方包 README / `[CAT]` catalog 原文 / `[OBS]` 判断 **+ 状态** `observed`\|`inferred` | 不标来源,或把自述当事实 |

**第 3 项是关键**。这一层拒绝形容词式的影响力,但**不要求你数数**:要么给原文,要么给被谁引用,要么给官方对象;三者都给不出,就不写。

## 4. 影响力怎么判:四种可回读的证据

### 口径一 · 被谁提到(A)

在 `data/plugins/*.yml` 里按名检索,然后**回读被谁提到**:

```sh
grep -rl "owner/repo" data/plugins | head
```

**纪律**:A 只能在**回读 `citers` 之后**才写进卡片。撞词的高分不是影响力,是噪声——通用词(`terminal`/`notification`/`schedule`/`calendar`)尤其如此。

**已记录的域级修正(2026-10-31)**:`lever-cross-boundary` 复核九个样本,只有 `limuyang2/agent-team` 被其他条目按名提到;其余为 0——目录 `description` 极少互相点名,样本之间是**功能竞争**而非引用关系。该域因此改用**实时 GitHub + npm 数据**论证影响力,以 C/F/G 立卡。

**层的裁定**:A 只适用于「目录内确实互引」的域。任何域要换替代口径,必须①在域 README 写明原因与采样日;②结论只在本域成立;③不得写成层规则。CROSS 符合这三条,记为**域级口径修正**,不是层规则变更。

### 口径二 · 替代了哪个官方对象(B)

最强的信号,因为它指得出具体被替换掉的东西:

- `GDWhisper/dsh-web-startup-auth`:「Replaces the dsh web startup」→ 替换**启动器**
- `HiSeax/dsh-better-model-setting`:「Replaces the official Models settings page」→ 替换**官方设置页**
- `All3nCN/dsh-better-sidebar-N23`:自述为上游的**完整 fork**,并明写与同类共享 `/git` 路由前缀而互斥 → 同时构成 B 与 **E**

### 口径三 · 少见/唯一(F)

原生没有、生态也很少有人做,才是真洞察。**但这是人工判断,不是计数**:读同域与相邻域的样本表、看有没有同类机制,找不到才写「少见」,并标 `[OBS]` 与日期。

**不要写「N / 总数」。** 名单在涨,这个数明天就变;把它写进卡片,等于给读者一个会过期的保证。

### 口径四 · 能力披露(D)

`data/capabilities.json`(2026-09-24 静态扫描)。它说的是「会碰什么」,**不是「安不安全」,也不是「强不强」**。空披露要分两种情况写明:零依赖库/纯前端,还是扫描器没覆盖到。

## 5a. 并行作业:主读单一归属

四域曾由四个独立会话分头研究,因此**每份官方包、每个 S/A 级样本只能有一个主读域**。其他域可以「借用一句」写进自己的卡片,但不得深读、不得立卡。

| 官方包 / 样本 | 主读域 | 借用方(只许一句) |
|---|---|---|
| `dsh-experimental-agent-team` | `lever-cross-boundary` | PROVE(完成标准)、LIMIT(成员权限) |
| `dsh-subagent` / `dsh-subagents` | `lever-cross-boundary` | RESHAPE(产品形态里怎么呈现) |
| `dsh-sandbox-policy` | `lever-draw-limit` | RESHAPE(默认档)、CROSS(远端是否仍生效)、PROVE(拦截) |
| `dsh-experimental-auto-review` | `lever-draw-limit` | PROVE(判定器与验收器之别) |
| `dsh-session-checkpoint-policy` | `lever-prove-output` | CROSS(崩了谁收敛)、LIMIT(留下了什么痕迹) |
| `dsh-fs-observation-policy` | `lever-prove-output` | LIMIT(首次编辑守卫) |
| `dsh-plan-mode` | `lever-prove-output` | — |
| `dsh-atomic-write` / `dsh-present` | `lever-prove-output` | — |
| `dsh-web` 启动与 profile / bundle / patch | `lever-reshape-product` | LIMIT(启动器鉴权那一半) |
| `AKS1st/dock` · `All3nCN/dsh-better-sidebar-N23` · `HiSeax/dsh-better-model-setting` | `lever-reshape-product` | CROSS(团队面板是否承载状态) |
| `GDWhisper/dsh-web-startup-auth` | `lever-reshape-product` | LIMIT(当 HTTP 网关旁证) |
| `Mlte0907/dsh-teams-x` · `zbzbhs/dsh-remote-agent` · `IKEASven69/dsh-takeover` | `lever-cross-boundary` | LIMIT(跨机鉴权) |
| `qiushi-dsh-evidence-audit` · `dsh-plugin-veriscope` | `lever-prove-output` | LIMIT(证据链的强制性) |
| `PerryLink/dsh-defend` · `IamNewHands/dsh-approval-gate` | `lever-draw-limit` | PROVE(拒绝消息的写法) |

**「借用」的写法**:在自己卡片里直接引 `[DSH]`/`[CAT]` 原文,**不写「见某域」**。这样任何一域停更都不会让另一域的理由失效。

## 5. 四域的专项条件(概括性优先)

| 域 | 入口条件之上,还要求 | 明确不收 |
|---|---|---|
| `lever-reshape-product-plugin` | 必须能指到**身份/首启/分发**中的一层;只改槽位的,要能证明它把槽位变成了**注册表**(`ctx.workbench` 那一路);且**装进任何 profile 都不用改宿主** | 换皮主题、单页面板、只加设置项的、换表层的(去 shell) |
| `lever-reshape-product-shell` | 必须**换掉表层(第 2 层)**或**自带宿主**;并写清首启/分发/降级三条怎么补(规律 A) | 能 `dsh plugin add` 装进别人 profile 的客人(留在 plugin 侧) |
| `lever-cross-boundary` | 必须跨**边界 1/2/3** 中可命名的一道;能说出**状态归谁、冲突谁裁、崩了谁收敛** | 子代理模型路由(那是 policy 钩子,只做旁支)、纯看板/活动球 |
| `lever-prove-output` | 必须能指到**六环**中的一环,且**门禁位置可命名**(pre-execute / post-execute / pre-step / 持久化 flush / 独立验收器) | 提示词里写「请检查」的技能包、只统计不拦截的面板 |
| `lever-draw-limit` | 必须落在**安装面/运行面/数据面**,且**强制点可命名**;纯披露的只能当旁证 | 密码保管类工具(除非它改了授权边界)、安全检查清单 |

## 6. 现役研究对象(分级清单不在这里维护)

**分级清单随样本变,放在各域 README 与 [catalog](./catalog.md) 里。** 本文件只保留判据,避免两份清单漂移:

| 级 | 判据 | 落位 |
|---|---|---|
| **S** | 定义了一个机制/一类做法,后来者照它的形状写 | 单独卡 + 域 README「骨架」表 |
| **A** | 所在边界/层上目前最好的一个取法 | 域 README 表 + 卡的「标杆」节 |
| **B** | 只在某个维度上与 A 不同 | 卡的对照行,**不立卡** |
| **C** | 明指不可共存,或同一接缝取反 | 失败模式表一行 |

**域级入口**:[RESHAPE-plugin](./lever-reshape-product-plugin/README.md) · [RESHAPE-shell](./lever-reshape-product-shell/README.md) · [CROSS](./lever-cross-boundary/README.md) · [PROVE](./lever-prove-output/README.md) · [LIMIT](./lever-draw-limit/README.md)。**全量文件**(kind / status / 定位)见 [catalog](./catalog.md)。

## 7. 现役研究的已知缺口

**这一节是给自己上刑的,不许删。** 完整缺口清单(含给上游的)在 BORROW §6。

1. **E 级(反面教材)只有 2 条真判**:`All3nCN/dsh-better-sidebar-N23` 的路由互斥、`IamNewHands/dsh-approval-gate` 的 fail-open。其余「失败模式」多来自**官方限制文档的推演**,不是真实事故。
2. **A 的撞词噪声**未清除:通用词(`terminal`/`notification`/`schedule`/`calendar`)会在按名检索时命中一堆无关项。CROSS 已改用实时数据绕开;其余域引用 A 时必须先回读被谁提到。
3. **证据强度分域,不能互推**:PROVE 锁 `repo@commit`;CROSS/LIMIT 读过源码但只锁版本;RESHAPE 停在 catalog + 插件 README。引用任何断言前,先看该域 README 的坐标表与页头状态。
4. **「少见/唯一」没有可重跑的计数**——这是刻意的。它只能写成「截至 `<日期>`,人工回读所见」并标 `[OBS]`;它会过时,引用时带日期。

## 8. 怎么复核这份规则

```sh
node _digested/verify.mjs # frontmatter / 链接 / 锚点 / 编码
```

**每次上游同步后必做**:重读受影响样本的坐标与 `[DSH]` 断言;若某个 S/A 样本**掉了证据**(被引消失、描述改口、官方对象不再被替换),它不是「还能用」,而是**必须重审**——这正是分级表存在的意义。**不要重跑计数门**:没有计数门。
