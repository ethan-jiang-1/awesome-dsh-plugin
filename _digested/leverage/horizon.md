# 研究对象怎么选:准入与分级

> **状态**:`observed`(门禁已用 7924 条跑过) · **更新**:2026-10-31 · **基线**:名单 `main@efe602e7b` · DSH `0.2.1-rc.3`
> **一句话**:**不是抓到一个插件就琢磨。**能进这份研究的条目必须先证明自己「有影响力」,再证明自己「有深度」,然后才排等级;排不进 S/A 的,只配当反面教材或旁支脚注。

## 0. 纪律:为什么要有这道门

7924 条里,**过了门的是 51 条(0.6%)**。

```
$ python3 _digested/leverage/census.py   # §9
── 9 准入门(影响力 A/B/C ≥1 且 深度 D/E ≥1)──
通过 51/7924 (0.6%)
分域:RESHAPE 23 · CROSS 10 · PROVE 18 · LIMIT 16
```

这个比例是刻意的。让研究对象随收录量增长,是这类仓库最常见的腐坏方式:写的人越多、卡片越多、单条越轻,最后变成另一份目录。所以这里反向做:**卡片数不随名单涨,只随「机制被验证」涨**。

**三条硬规矩**:

1. **无影响力证据 = 不进研究**(可以出现在脚注,不许有卡)。
2. **无深度证据 = 不进研究**;只有功能描述、说不出它动的是哪条缝的,一律算「工具」,归 `ecosystem/`。
3. **进不了 S/A 的不写卡**。B 级只做对照表的一行,C 级只做一句话脚注。**拒绝写的条目远比写下的条目多,这是设计,不是遗漏。**

## 1. 入口条件(两组,缺一不立卡)

| 组 | 代号 | 条件 | 机器可判 | 判定方式 |
|---|---|---|---|---|
| 影响力 | **A 引用** | 仓库名被目录中其他条目按名提到 ≥3 次 | ✅ | 目录内 in-degree |
| 影响力 | **B 替代** | 自述**替换/接管官方对象**:profile、启动器、官方页面、官方默认行为 | ✅ | 描述正则 + 回读原文 |
| 影响力 | **C 接缝** | 点名**具名接缝**:`ctx.*`、`waterfall`、`/pre-step`、`/pre-execute`、`/post-execute` | ✅ | 描述正则 + 回读原文 |
| 影响力 | **F 稀缺** | **全库同类机制 ≤3 条**,而原生支持缺失或只是实验层 | 半 | 附一条可重跑检索式 |
| 深度 | **D 能力** | `capabilities.json` 披露 ≥2 个高杠杆能力;**空披露的已收录条目同样算** | ✅ | 能力边车 |
| 深度 | **E 反面** | 被同类插件**明指不可共存**,或同一接缝的**两种相反取法** | ❌ | **只能人工认定** |
| 深度 | **G 已核** | 机制已读官方包 README,且能指出它的失效条件 | ❌ | 人工,写进卡片第 3、7 节 |

**机器只判 A/B/C/D。** E、F、G 一律由人写,脚本不敢代劳——写了「稀缺」却不附检索式,等于拍脑袋。

### 门槛参数

| 参数 | 取值 | 依据 |
|---|---|---|
| A 的 in-degree 阈值 | ≥3 | 低于 3 基本是撞词或单次提及,不足以称影响力 |
| D 的高杠杆能力集 | `subagent` `workflow` `sandbox` `network` `credentials` `host-runtime` `dynamic-code` `shell` | 与 `lever-draw-limit` 的能力披露口径一致 |
| D 的空披露处理 | 算通过 | 已收录但披露为空,多半是零依赖库或纯前端;**但也可能是扫描器没跑**,卡里必须写明是哪一种 |

## 2. 分级:S / A / B / C

| 级 | 名称 | 条件(在入口条件之上) | 在研究里的位置 |
|---|---|---|---|
| **S** | 定义型 | 影响力 ≥2 条(A+B+C+F 任二)**且**深度 G 成立,**且**它**定义了一个机制或一类做法**——后来者照着它的形状写 | 单独一张卡,进域宪章的「骨架」表 |
| **A** | 代表型 | 影响力 ≥1 条 **且** 深度 D+G 成立 **且** 它是所在边界/层上**目前最好的一个取法** | 卡片「标杆」表的正例 |
| **B** | 对照型 | 影响力 ≥1 条 **且** 深度 D 或 E 成立,但**只在某个维度上与 A 不同**(更省、更狠、更偏) | 卡片内一行对照,**不单独立卡** |
| **C** | 反例型 | E 成立:明指不可共存,或同一接缝取反 | 失败模式表里的一行 |
| ✗ | 不收录 | 影响力与深度都没过门 | 最多一句话脚注 |

**S 与 A 的唯一区别**:S 是「后来者的模板」,A 是「当前的优解」。一个插件可以在某个域里是 A、在另一个域里是 S——分级是**按域**的,不是按插件。

## 3. 每条必须交代的六件事

这是这一层最容易轻飘飘的地方,所以规定死:**任何进入卡片的样本,都要写齐六项,缺一项就退回不放**。

| # | 必写 | 具体要求 | 反例(会被退回的写法) |
|---|---|---|---|
| 1 | **它代表什么** | 一句话说清它是哪一类的样板,以及这一类在 DSH 里的边界 | 「一个很强大的团队插件」 |
| 2 | **为什么选它** | 指名它过的哪几条门(A/B/C/D/E/F/G 的具体值),而不是「因为看着不错」 | 「社区口碑好」 |
| 3 | **影响力多大** | 给**可复核的量**:被引次数 / 替代了哪个官方对象 / 稀缺检索式与命中数 / 能力披露 | 「很流行」「很多人用」 |
| 4 | **主要特点** | 机制层面的特点:占了哪条缝、失败时往哪倒、代价是什么 | 「功能丰富」「体验好」 |
| 5 | **代价 / 失效条件** | 至少一条**具名**的失效路径(升级断裂、优先级暗战、绕过通道、依赖漂移) | 「有一定风险」 |
| 6 | **证据级别** | `[DSH]` 官方包 README / `[CAT]` catalog 原文 / `[OBS]` 判断 **+ 状态** `observed`\|`inferred` | 不标来源,或把自述当事实 |

**第 3 项是关键**。这一层拒绝形容词式的影响力。要么给数,要么给检索式,要么给官方原文——三者都给不出,就不写。

## 4. 影响力怎么量:四个可复现的口径

### 口径一 · 目录内被引用(A)

```sh
python3 _digested/leverage/census.py    # §9b 输出前 12 名 + 被谁提到
```

实测结果里**有噪声,必须先看被谁提到**:

| 仓库 | 被引 | 真伪 |
|---|---|---|
| `giiiiiithub/terminal` | 110 | **部分为真**——`terminal` 是通用词,大量命中是撞词 |
| `DeepseekHarnessPlugins/Notification` | 66 | 同上 |
| `mzzsfy/dsh-plugin/*` | 21 | **真引用**:同仓多包互相提及 + 同类插件指路 |
| `omdsh-dev/DSH-better-sidebar` | 31 | **真引用**:一批插件自述「基于 dsh-better-sidebar」 |
| `vlln/whale-girl` | 23 | 真:衍生的 whale 系列插件成批命名 |
| `limuyang2/agent-team` | 3 | 真,但量小——只够 A 级下限 |

**纪律**:A 只能在**回读 `citers` 之后**才写进卡片。撞词的高分不是影响力,是噪声。

### 口径二 · 替代了哪个官方对象(B)

最强的信号,因为它指得出具体被替换掉的东西:

- `GDWhisper/dsh-web-startup-auth`:「Replaces the dsh web startup」→ 替换**启动器**
- `HiSeax/dsh-better-model-setting`:「Replaces the official Models settings page」→ 替换**官方设置页**
- `All3nCN/dsh-better-sidebar-N23`:自述为上游的**完整 fork**,并明写与同类共享 `/git` 路由前缀而互斥 → 同时构成 B 与 **E**

### 口径三 · 稀缺性(F)

原生没有、生态也很少有人做,才是真洞察。用 `--probe` 复核:

```sh
python3 _digested/leverage/census.py --probe "ctx\.workflowEngine"     # 0/7924
python3 _digested/leverage/census.py --probe "worktree"                # 45/7924
python3 _digested/leverage/census.py --probe "hash.?chain|哈希链"       # 3/7924
```

三个实测结果直接支撑三条判断:workflow 引擎**无人自述使用**、worktree 已有 45 条供给、哈希链回执全库只有 3 条。**F 级结论必须附这样一行检索式。**

### 口径四 · 能力披露(D)

`data/capabilities.json`(2026-09-24 静态扫描,URL join 3787/7922)。它说的是「会碰什么」,**不是「安不安全」,也不是「强不强」**。空披露要分两种情况写明:零依赖库/纯前端,还是扫描器没覆盖到。

## 5a. 并行作业:主读单一归属

四域将由四个独立会话分头研究,因此**每份官方包、每个 S/A 级样本只能有一个主读域**。其他域可以「借用一句」写进自己的卡片,但不得深读、不得立卡。

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
|  `PerryLink/dsh-defend` · `IamNewHands/dsh-approval-gate` | `lever-draw-limit` | PROVE(拒绝消息的写法) |

**「借用」的写法**:在自己卡片里直接引 `[DSH]`/`[CAT]` 原文,**不写「见某域」**。这样任何一域停更都不会让另一域的理由失效。

## 5. 四域的专项条件(概括性优先)

| 域 | 入口条件之上,还要求 | 明确不收 |
|---|---|---|
| `lever-reshape-product` | 必须能指到**表层/身份/首启/分发**中的一层;只改槽位的,要能证明它把槽位变成了**注册表**(`ctx.workbench` 那一路) | 换皮主题、单页面板、只加设置项的 |
| `lever-cross-boundary` | 必须跨**边界 1/2/3** 中可命名的一道;能说出**状态归谁、冲突谁裁、崩了谁收敛** | 子代理模型路由(那是 policy 钩子,只做旁支)、纯看板/活动球 |
| `lever-prove-output` | 必须能指到**六环**中的一环,且**门禁位置可命名**(pre-execute / post-execute / pre-step / 持久化 flush / 独立验收器) | 提示词里写「请检查」的技能包、只统计不拦截的面板 |
| `lever-draw-limit` | 必须落在**安装面/运行面/数据面**,且**强制点可命名**;纯披露的只能当旁证 | 密码保管类工具(除非它改了授权边界)、安全检查清单 |

## 6. 每域现役研究对象(按分级)

只列 S/A。**B 级以下是刻意不列的**——它们出现在卡片的对照行与失败模式里,不该有独立条目。

### `lever-reshape-product`

| 级 | 仓库 | 过了哪些门 | 影响力证据(可复核) | 一句话特点 |
|---|---|---|---|---|
| **S** | `AKS1st/dock` | C+D | 自述 `ctx.workbench` 注册表;零能力披露(纯前端);6 个 dock-* 兄弟包跟随 | 不提供界面而提供**注册表**,把 3 层槽位变成 6 层平台 |
| **S** | `hyperion2144/dsh-desktop-tauriapp` | F+G | **F**:桌面壳场景里少见的「页面内半区 + 宿主外壳」双段设计;壳在 DSH **之外** | 证明「真正的产品改造发生在插件系统外面」 |
| **A** | `GDWhisper/dsh-web-startup-auth` | B+D | B:自述替换 `dsh web` 启动器;D:7 项能力含 host-runtime | 2 层唯一一种**在 DSH 内部**改产品的办法 |
| **A** | `All3nCN/dsh-better-sidebar-N23` | B+D+**E** | B:完整 fork;E:明指与同类共享 `/git` 路由前缀而互斥 | fork 路线的成本样本,同时是**反面教材** |
| **A** | `HiSeax/dsh-better-model-setting` | B+D | B:替换官方 Models 设置页 | 「官方页面可整体替换」的实证 |

### `lever-cross-boundary`

| 级 | 仓库 | 过了哪些门 | 影响力证据 | 一句话特点 |
|---|---|---|---|---|
| **S** | 官方 `dsh-experimental-agent-team` | G | 不是生态条目,是全域的**约束源**;三条已知限制定义了边界 2 的税 | 变量不在它自己,而在它留下的三个空白 |
| **A** | `Mlte0907/dsh-teams-x` | D+G | 9 项能力含 `subagent`/`dynamic-code`;自述 captain + 依赖感知 DAG + 持久邮箱 | 生态自建 roster,与官方 Team 并存两套语义 |
| **A** | `zbzbhs/dsh-remote-agent` | F+G | **F**:「副机跑完整 DSH、断链继续」在 62 条 remote 类里罕见 | 把跨机从**传输问题**降级为**信任问题** |
| **A** | `IKEASven69/dsh-takeover` | F | **F**:同步盘 + 消费即弃卡片 + 四态账本,全库少见 | 最省事的跨机:**没有协议,只有文件** |

### `lever-prove-output`

| 级 | 仓库 | 过了哪些门 | 影响力证据 | 一句话特点 |
|---|---|---|---|---|
| **S** | 官方 `dsh-session-checkpoint-policy` | G | 全库唯一 fail-closed 的**副作用前**持久化屏障 | 保证「至少知道发生了什么」,不保证「只发生一次」 |
| **S** | 官方 `dsh-fs-observation-policy` | G | 唯一把「读过」变成**版本约束**的机制;生态里大量「首次编辑」守卫是它的回声 | 策略只做决策不做 I/O 的范式 |
| **A** | `030611/qiushi-dsh-evidence-audit` | F+C | **F**:`hash.?chain\|哈希链` 全库 **3/7924** | 只证「发生过、顺序、未被篡改」,不存内容 |
| **A** | `4444wjt/dsh-plugin-veriscope` | F+G | `REVIEW`/待复核检索式宽泛(756 条),需回读后择真;它的独特点是 **REVIEW 永不转 PASS** | 不确定性不允许被自动消解 |
| **A** | `263311487-ux/dsh-verify` | F | **F**:换运行时(真 Chromium)做验收,全库少见 | 判定与执行分离 |
| **A** | `1687210989/agent-clinic` | F | **F**:22 项具名诊断 + 稳定**证据定位符**(如 `session.v4.jsonl.zstd#L101-L110`) | 诊断与判决分离,可复核性来自定位符 |

### `lever-draw-limit`

| 级 | 仓库 | 过了哪些门 | 影响力证据 | 一句话特点 |
|---|---|---|---|---|
| **S** | 官方 `dsh-sandbox-policy` | G | 唯一有策略词汇的维度;原文「网络和进程策略不在其词汇中」 | 权限状态是**日志事实**,不是实时开关 |
| **S** | 官方 `dsh-experimental-auto-review` | G | 唯一的「模型判模型」;默认关闭、明说会误放行、留有 `run_code` 绕过通道 | 智能审批是**体验优化**,不是安全边界 |
| **A** | `PerryLink/dsh-defend` | C | 同时挂 `agent/pre-step` 与 `tools/pre|post-execute`;**零能力披露** | 想防注入必须挂 pre-step,挂 tools 层永远防不了「模型已被说服」 |
| **A** | `DevilSpiderX/dsh-workspace-only-plugin` | F | **F**:把**所有**沙箱模式的文件访问收进会话工作区,原生无此词汇 | 在策略之上再套一层自己的策略 |
| **A** | `IamNewHands/dsh-approval-gate` | D+**E** | D:含 network/llm;E:判定器不可用时**自动放行**(fail-open)——与本域其他样本相反 | 显式 fail-open 的诚实样本,同时是对照 |
| **A** | `BotonJ/dsh-plugin-sentinel` | F | **F**:安装前 tarball 内存解析、零落盘;仅 `fs-read`+`env` 两项能力 | 替官方补「安装面没有自动检查」这一格 |

## 7. 现役研究的已知缺口

**这一节是给自己上刑的,不许删。**

1. **E 级(反面教材)目前只有 2 条真判**:`All3nCN/dsh-better-sidebar-N23` 的路由互斥、`IamNewHands/dsh-approval-gate` 的 fail-open。其余「失败模式」表的行多数来自**官方限制文档的推演**,不是真实事故。
2. **F 级的检索式只覆盖了 4 条判断**,其余「稀缺」表述尚无可重跑证据。
3. **`hyperion2144/dsh-desktop-tauriapp` 过不了机器门**:它既无 in-degree、也不自述接缝、能力边车也没有它。它现在靠 **F+G 人工认定**进来——这是本表最弱的一格,若下一轮仍找不到可复核证据,应降级为 B 或删除。
4. **A 的撞词噪声**未清除:前 5 名里至少 4 个是通用词(`terminal`/`notification`/`schedule`/`calendar`)。要么加白名单,要么改口径,下一轮决定。
5. **所有样本的证据级别停在「catalog 自述 + 官方包 README」**,未读插件源码。任何「它真的做到了」的断言都是 `inferred`,不是 `observed`。

## 8. 怎么复核这份准入

```sh
python3 _digested/leverage/census.py              # 看 §9 通过数与证据分布
python3 _digested/leverage/census.py --probe "<正则>"   # 复核任何稀缺性断言
node _digested/verify.mjs                         # 文档本身的一致性
```

**每次上游同步后必做**:重跑 §9,若某个 A 级样本**掉了门**(被引跌到 3 以下、描述改了口径),它不是「还能用」,而是**必须重审**——这正是分级表存在的意义:它让「这条样本凭什么在这儿」变成一个每次都能重问的问题。
