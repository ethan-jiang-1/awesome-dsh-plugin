---
title: "怎么借：从这套研究里拿走东西"
domain: layer
kind: guide
positioning: "跨域借用总入口：按需求路由到具体章节，并给出四域最小集、跨域法则与陷阱。"
takeaway: "8 条任务路由 + 6 条跨域法则 + 7 个必答问题 + 19 个陷阱 + 回源五步。"
read_when: "要写插件/做产品/做协作/做质量/做安全；或要评审、选型、回源、给官方提缺口。"
status: living
updated: 2026-10-31
budget: 420
---
# 怎么借：从这套研究里拿走东西

> **这一层不是插件导购。** 它挖的是「谁占了哪条缝、机制长什么样、代价是什么、什么时候坏」。所以你能拿走的不是结论，是**机制形状 + 失效条件**。
> **先记住四条引用规则**：① 引卡片，不引本文件（本文件的法则标 `[OBS]`，是综合判断）；② 每个数字带日期；③ 四域不是分类，一个插件可以同时在四个域里出现（重叠 41–44%）；④ 「稀缺 / 唯一」是人工判断，标 `[OBS]`，不写命中数。

## 0. 三条读法

| 你有多久 | 读什么 | 会拿到 |
|---|---|---|
| **30 秒** | §2 四域最小充分集里你关心的那一行 | 这个方向「只做一件事」是什么 |
| **30 分钟** | §1 找到你的需求 → §3 六条法则 → §4 七个问题 | 判断框架 + 该抄什么 + 该躲什么 |
| **半天** | 按 §1 的出处读一个域的宪章 + 2–3 张卡 + 坐标表 | 能动手的形状，以及哪里会塌 |

**不要这样用**：不要拿它当推荐榜（`[CAT]` 只是作者自述）；不要跳过「反面」只读结论；不要把它当完整分类（四域是四个并列提问）；不要在没有坐标的情况下声称「某插件做到了」。

## 1. 按需求路由：八种需求，八个入口

### 1.1 我要写一个插件，但不知道从哪下手

**答案**：先定接缝，再写机制。接缝决定它能改变什么，能力是次要的。

- **先读**：[00-map](./00-map.md) 的杠杆阶梯 → [RESHAPE-0](../leverage-reshape-product/horizon.md) §4 的 13 行接缝表。
- **再读**：§2 里选一个域的最小集；同类 `sample` 卡的「借用节」。
- **拿到**：7 级位置、13 行「上游保证 / 不保证」、一份可抄清单。
- **必问**：这条缝给不给我强制点？不给的话，我的保证上限是什么？
- **反例**：先写功能再找接缝 → 只能用提示词兜底（[PROVE-01](./lever-prove-output/01-quality-chain.md) §6 L1）。

### 1.2 我要改产品形态（壳 / 槽位 / 首启 / 分发 / 多端）

**答案**：产品化的单位是 profile，不是插件；**先分「插件侧 / 宿主侧」**，再决定改哪一层、要不要 fork。

- **先读**：[RESHAPE-plugin](../leverage-reshape-product/plugin/README.md)（装进别人的 profile）、[RESHAPE-profile](../leverage-reshape-product/profile/README.md)（发一套 bundle 在浏览器里交付）或 [RESHAPE-shell](../leverage-reshape-product/shell/README.md)（换掉表层自己当宿主），再看 [RESHAPE-0](../leverage-reshape-product/horizon.md) §2 的七层。
- **再读**：对应 `sample` 卡的「降级链」「救生页」「首启」三节；[RESHAPE-5](../leverage-reshape-product/plugin/51_分发与救生页-dsh-market.md) 与 [RESHAPE-1 终端](../leverage-reshape-product/shell/14_终端即产品-dsh-TUI.md)。
- **拿到**：改第 2 层必须自己补 5/6 层（规律 A）；救生页必须活在插件栈之外；每档能力一条「退化为 Y」。
- **必问**：起不来的时候，用户看到的是什么？那个东西依赖不依赖坏掉的 profile？
- **反例**：换表层却没补首启 → 用户第一次打开就卡住（RESHAPE-0 规律 A）。

### 1.3 我要做多 agent 协作 / 跨机

**答案**：协作是状态问题，不是 spawn 问题。先定权威状态在哪张纸上，再定冲突谁裁，最后定崩溃谁收敛；写冲突**只有** `tools/pre-execute` 返回 deny 真拦得住。

- **先读**：[CROSS README](./lever-cross-boundary/README.md) 的「能借鉴什么」→ [CROSS-01](./lever-cross-boundary/01-collab-topology.md) 的四道边界。
- **再读**：[CROSS-02](./lever-cross-boundary/02-coordination-mechanisms.md) §5.5 的三张配方；[CROSS-07](./lever-cross-boundary/samples/07-Nwflower-dsh-file-claim.md) 的写冲突样本。
- **拿到**：三笔税（状态 / 冲突 / 收敛）、配方 A/B/C、选型决策树、14 个样本坐标。
- **必问**：你的租约有没有 epoch / fencing token？被接管时原主怎么知道自己已经输了？
- **反例**：先写崩溃恢复，再发现状态存在两处 → 恢复逻辑重写一遍（CROSS-02 §5.5 的依赖顺序）。
- **额外**：跨机把「谁在执行」与「谁持有连接」解耦（CROSS-06）；跨实例投递没有幂等键就是重复执行（CROSS-08）。

### 1.4 我要做质量门禁 / 验收

**答案**：门禁位置决定它能改变什么。否决权按结论的确定性分配：能机械判的给 deny，要语义的只能 steer 或报告；必须有「等人」状态；模型侧不能有 `decide`。

- **先读**：[PROVE-01](./lever-prove-output/01-quality-chain.md) 的六环 → [PROVE-10](./lever-prove-output/10-quality-control-playbook.md) §7 的 64 条原则。
- **再读**：[PROVE-10](./lever-prove-output/10-quality-control-playbook.md) §8 的八问；按你挂的接缝读 02–09 里对应的一张。
- **拿到**：六环硬软表、Q/V/F/A/E/R/P/C 八组原则、七条「只想记七条」。
- **必问**：门禁自己会不会重跑判据？它采信的是自报的执行记录，还是自己看到的？
- **反例**：默认 `remind` → 装上 ≠ 生效（[PROVE-09](./lever-prove-output/09-discipline-loop.md)）；判文本想撤回 → 只能追赶（[PROVE-06](./lever-prove-output/06-judge-placement.md)）。

### 1.5 我要做安全 / 权限 / 审批 / 供应链

**答案**：最小充分集是三件事——一个不可绕过的沙箱、一处针对不可逆动作的确定性否决、一个失败即拒绝的默认方向。沙箱只覆盖文件，网络与进程不在它的策略词汇里。

- **先读**：[LIMIT README](./lever-draw-limit/README.md) 的「借法一览」→ [LIMIT-01](./lever-draw-limit/01-trust-layers.md) 的三层监管链。
- **再读**：[LIMIT-09](./lever-draw-limit/09-control-budget.md) §9 的八个决定；按场景读 02（审批）/ 03（第二模型）/ 05（网络）/ 08（安装面）。
- **拿到**：21 行「问题 → 抄哪条」、三层坐标、八个决定的施工图。
- **必问**：强制点在哪条缝上？失效时是 fail-closed、fail-open 还是转人工？这三者写清楚了吗？
- **反例**：把模型判定当授权（LIMIT-03）；判定器不可用就自动放行还不写出来（LIMIT-02）。

### 1.6 我要选一个插件装上

**答案**：先读默认值和失效方向，再读功能。星标 ≠ 使用量；npm 包名 ≠ 仓库名。

- **先读**：[catalog](./catalog.md) 里 `kind: sample` 或 `kind: card` 的行 → 目标卡的「失败模式 / 评估清单」。
- **再读**：该域 README 的样本坐标表；[PROVE-00](./lever-prove-output/00-sample-lineage.md)（要精确版本 / commit 时）。
- **拿到**：版本、安装串、证据级别、已知失效条件。
- **必问**：npm 上这个包名对应的是同一个仓库吗？（LIMIT README 记录了三个同名不同人的坑。）
- **反例**：按星标选 → 4★ 有 3,103 次月下载、0★ 根本没上 npm（CROSS README 的影响力段）。

### 1.7 我要评审别人的方案

**答案**：问四件事——门装在哪、判什么、错了怎么办、谁有权说「过了」；再问一句：它收到的是观察还是报告？

- **先读**：§4 的七个问题 → 对应域的「评估清单」。
- **再读**：卡的「失败模式」表；§5 的陷阱总表。
- **拿到**：一张能在 20 分钟内过完的审查表。
- **必问**：它的判决绑定了哪一次具体输入？输入变了，判决会不会自动作废？
- **反例**：只看功能列表和 star；把「AI 评审」当验收（PROVE-06）；把披露当强制（LIMIT-01）。

### 1.8 我要继续挖 / 回源 / 给官方提缺口

**答案**：一切断言都要能回到 `repo@commit` 或官方包 README；回不去的必须标 `[OPEN]`。缺口在 §6。

- **先读**：§6；[PROVE-00](./lever-prove-output/00-sample-lineage.md) 的坐标格式；[horizon](./horizon.md) §8。
- **再读**：目标卡的「精确坐标」节；该域 README 的「自用检索式」。
- **拿到**：repo / npm / 版本 / commit / 锚点文件 / 一条可复跑的 `curl`。
- **必问**：你用 `main` 还是短 SHA？用 `main` 打开的代码三个月后是另一份（PROVE-00 的纪律）。
- **反例**：没记 commit 的抓取 = 没抓（PROVE-00 §2 的两条自曝）。
- **本册证据链**：14 张样本卡头部都有“证据链”指向 `_证据/NN-*-源码复核.md`（固定 npm/tag/commit 与偏差表）；15 张机制卡与 6 篇 playbook 末尾有“证据与边界”（`[DOC]/[SRC-TARGET]/[SRC-DSH]/[OBS]/[OPEN]`）。**引用任何机制断言前先读对应 memo/证据节**；README 主张不等于实现（见 [`EVIDENCE.md`](./EVIDENCE.md)）。

## 2. 四个方向各自的最小充分集

> 每域只列「如果只记几件事」。完整论证在各域宪章，这里只给指针与一句话。

### 2.1 [RESHAPE-plugin](../leverage-reshape-product/plugin/README.md) / [RESHAPE-shell](../leverage-reshape-product/shell/README.md) · 产品形态

**只做一件事**：先分「插件侧 / profile 侧 / 宿主侧」，再定「改的是哪一层」，最后才决定要不要 fork。

1. **profile 是产品单位**，插件只是零件；不改上游也能组装产品（[RESHAPE-plugin](../leverage-reshape-product/plugin/README.md)）。
2. **换表层 ⇒ 自己补首启 / 分发 / 降级**（RESHAPE-0 规律 A）。
3. **救生页必须活在插件栈之外**，否则它和坏掉的 profile 一起起不来（RESHAPE-5）。
4. **降级链的终点是人能读的原文**，不是空白块（RESHAPE-2）。
5. **同源出数**：用户已经见过的数字只允许上游那一份投影出数（RESHAPE-3）。
6. **版本锁不到就跳过**，不装近似版本；环境码「未包含 = 保持现状」（RESHAPE-4）。
7. **宿主侧没有"宿主兜底"**：换成独立产品后，首启 / 分发 / 降级全归你（[RESHAPE-shell](../leverage-reshape-product/shell/README.md) §4）。

### 2.2 [CROSS](./lever-cross-boundary/README.md) · 协作边界

**只做一件事**：先定权威状态在哪张纸上。

1. **三笔税**：状态归属 → 冲突裁决 → 失败收敛，顺序不能反（CROSS-02 §5.5）。
2. **写冲突只有 `tools/pre-execute` 的 deny 真拦**；提示词里的 writeScopes 永远是建议（CROSS-07）。
3. **「完成」判据要看错误事件**，不能只看没超时（CROSS-06）。
4. **消息 ack 放在「被 step 准入」那一刻**，不是投递成功那一刻（CROSS-01）。
5. **租约必须有 epoch / fencing**，否则被接管方静默失锁（CROSS-02 配方 B）。
6. **跨机把「谁在执行」与「谁持有连接」解耦**（CROSS-06）。
7. **四态证据账本**：`CURRENT_OBSERVED / HISTORY_REPORTED / MISMATCH / UNAVAILABLE`（CROSS README）。

### 2.3 [PROVE](./lever-prove-output/README.md) · 质量门禁

**只做一件事**：先选接缝，再写判据。

1. **门禁位置决定它能改变什么**，能力是次要的（PROVE-01 L2）。
2. **否决权按确定性分配**：可机械判的 deny，语义判断只 steer（PROVE-10 Q3）。
3. **默认值决定门是否存在**；装上 ≠ 生效（PROVE-10 E1）。
4. **必须有「等人」状态**，且不可自动消解（PROVE-07 / F5）。
5. **模型侧不能有 `decide`**（PROVE-08 Q7）。
6. **门禁自己重跑判据**，不采信自报的执行记录（PROVE-02 C3）。
7. **默认软 + 一行严格模式**，把选择权交给用户（PROVE-09 E2）。

### 2.4 [LIMIT](./lever-draw-limit/README.md) · 安全监管链

**只做一件事**：填「撤掉它会发生什么」。

1. **沙箱只覆盖文件**；网络与进程没有策略词汇（LIMIT-01）。
2. **最小充分集**：沙箱 + 一处不可推翻的否决 + fail-closed（LIMIT-09）。
3. **八层审批管道，顺序即策略**；额度不得越过硬拒层（LIMIT-02）。
4. **同步守卫只做纯函数判断**，复杂策略搬去异步流水线（LIMIT-04）。
5. **装前看「组合形状」，装后只做可回滚的隔离**（LIMIT-08）。
6. **范围 × 默认值 × 装得上**：用户要的是「不必再想这件事」（LIMIT-06）。
7. **不自破边界**：声称保护边界的插件，自己不能用它要防的能力（LIMIT README 一票否决）。

## 3. 跨域收敛：六条法则

> 这一节是**综合判断**，全部标 `[OBS]`。入选标准：在 ≥2 个域里能找到独立出处，且能给出反例。单域强结论放在 §3.7。

### 3.1 位置 > 能力 `[OBS]`

同一个能力，挂在不同的接缝上，能改变的东西完全不同。**先问「它站在哪」，再问「它多聪明」。**

- 出处：PROVE-01 §6 L2（门禁位置决定能力）· LIMIT-09 决定二（强制点在哪条缝）· RESHAPE-0 §4（上游保证/不保证）· CROSS-01 §3（边界决定税）。
- 反例：在同步守卫里做需要读文件、问人、跨调用记忆的重活 → 退化成超时或无判定（LIMIT-04）。
- 用法：任何方案先让它回答「接缝 + 强制点 + 失效方向」，答不出就不是机制。

### 3.2 默认值就是策略 `[OBS]`

**不配置时它做什么**，比「它支持什么」更能定义它的性质。装上 ≠ 生效。

- 出处：PROVE-10 E1 · LIMIT-09 决定三（撤掉它会发生什么）· CROSS-02 的「默认不派活」· RESHAPE README 第 11/16 条（接管必须保守 / 每档一条退化为 Y）。
- 反例：`dsh-doublecheck` 默认 `remind`——门装了，但默认不拦（PROVE-09）。
- 用法：评审第一句问默认值，第二句问「关掉它是不是真的零成本」。

### 3.3 失败方向必须显式 `[OBS]`

每个门禁都要写清：出错时是 fail-closed、fail-open，还是转人工。**三者混用的方案，一定有一个洞没被说。**

- 出处：LIMIT-02（fail-open 的诚实样本）· PROVE-10 F4（按可判定性定失败方向）· CROSS-02 配方 C（判据 → 检测 → 动作）。
- 反例：判定器不可用时自动放行，却没在文档里写 → 用户以为有门（LIMIT-02）。
- 用法：把「解析失败时走哪条分支」逐格填上；解析不了必须落到拒绝，不是落到第 0 项。

### 3.4 你收到的是报告，不是观察 `[OBS]`

跨边界之后，你拿到的是「谁说的」，不是「你看到的」。所以状态要标来源，证据要分层，判决要绑定输入。

- 出处：CROSS README 的四态证据账本 · PROVE-10 C9（声称 / 观测 / 决定）· LIMIT-01（披露 ≠ 策略 ≠ 强制 ≠ 判决）。
- 反例：把成员自述的 `changedPaths` 当证据（CROSS README「六条别照抄」）。
- 用法：任何跨进程/跨会话的数据，加一列「观察 / 报告 / 不一致 / 不可得」。

### 3.5 可逆性 > 预测 `[OBS]`

插件的真实行为在安装前不可判定，所以「我会判断它安不安全」必然有假阴性；而「我能退回上一版」在失败时仍然成立。

- 出处：LIMIT-08（可逆性优于预测）· RESHAPE-5（救生页 / 回滚）· CROSS-03（不可变快照 + 重跑，卖可复现）· PROVE-08（重检永不替换基线）。
- 反例：`atomic-write` 不 `fsync`、`present` 的交付版本持久化延期 → 崩溃后产物可能不在（PROVE-01 §3.4）。
- 用法：先设计「坏了怎么回」，再设计「怎么不坏」。

### 3.6 否决权按确定性分配 `[OBS]`

确定性的判据给 deny，语义判断只能 steer / 报告；把不确定的东西放到能一票否决的位置，误杀是迟早的。

- 出处：PROVE-10 Q3 · LIMIT-04（同步谓词只能回答一次）· CROSS-07（只对真正会写的工具挂 deny）。
- 反例：拿模型打分去 deny（PROVE-06）；对 `bash` 里的只读命令也 deny（CROSS-02 配方 B 的误伤）。
- 用法：画一张「判据确定性 × 可用的否决权」表，只有左上角能 deny。

### 3.7 单域强结论（同样该抄，但只有一家证据）

- **租约必须带 epoch / fencing**（CROSS-02 配方 B）：没有它，原主要等到下一次写入被拒才知道自己输了。
- **哈希链证「没被改」，不证「事是真的」**；连「文件被整个删掉」都证不了（PROVE-05）。
- **沙箱是路径白名单，不提供原子性**；网络与进程不在它的词汇里（LIMIT-01 / LIMIT-04）。
- **幂等键不能省**：没有幂等的重试通道，重投就是重复执行（CROSS README 五问 #5）。

## 4. 抄之前必答的七个问题

> 这七问合起来，就是四域「评估清单」的交集。答不出的那一格，通常就是你以后会塌的那一格。

| # | 问题 | 好答案长什么样 | 去哪看四域的答案 |
|---|---|---|---|
| 1 | 它挂在哪条接缝 / 哪一层？ | 点名 `tools/pre-execute`、`agent/pre-step`、沙箱后端、HTTP 路由或安装流程 | RESHAPE-0 §4 · LIMIT README 强制点 · PROVE-01 六环 |
| 2 | 它替换 / 接管了谁？撤掉它会怎样？ | 说得出被替换的对象，以及「撤掉后变松还是变紧」 | RESHAPE-5 · LIMIT-09 决定三 |
| 3 | 它的判决能不能被推翻？谁有权推翻？ | 一票否决 / 可 steer / 只能报告，三选一并说明 | PROVE-10 Q3 · LIMIT-04 |
| 4 | 失败时往哪倒？ | fail-closed / fail-open / 转人工，点名；解析失败也有归宿 | LIMIT-02 · PROVE-10 F4 · CROSS-02 配方 C |
| 5 | 它凭什么算「完成」？证据能否被重放或定位？ | 绑定一次具体输入；别人能重放输入或定位日志某几行 | PROVE-01 · PROVE-05 · PROVE-08 |
| 6 | 它收到的是观察还是报告？谁的状态是权威？ | 标出 `CURRENT_OBSERVED` / `HISTORY_REPORTED`，并指定唯一权威 | CROSS README 四态账本 · PROVE-10 C9 |
| 7 | 什么条件下它会坏？坏了退化成什么？ | 具名失效路径（升级断裂、优先级暗战、绕过通道、依赖漂移） | 每张卡的「失败模式」节 |

## 5. 陷阱总表

> 这些都是「读起来像能力、实际是空壳」的地方。四域已逐个核过；抄之前先看这一列。

### 5.1 假能力

| 陷阱 | 真相 | 出处 |
|---|---|---|
| 「写范围 / 文件隔离」 | 官方 Team 的 `writeScopes` 自述「never block anything」；除 `file-claim` 外无人真拦 | CROSS-01 §3 · CROSS README |
| 「原子认领」 | `dsh-expert-mode` 的 taskboard 是「读 → 校验 → 整份覆写」，全仓无 `flock` / `O_EXCL` / `temp+rename` | CROSS-10 |
| 「可恢复」 | `dsh_workflow` 是快照重跑；`team-gui` 重启后全部 interrupted——都不是断点续跑 | CROSS-02 §3.3 |
| 「P2P 直连、零中转」 | 子代理只能被父唤醒；文件总线没有唤醒机制，投递仍要协调官再唤起一次 | CROSS-10 |

### 5.2 假安全

| 陷阱 | 真相 | 出处 |
|---|---|---|
| 「AI 审批 = 安全边界」 | 第二模型只替代人工点击，不替代强制点；没有应答者时是 `unavailable`，而 `unavailable` 是拒绝 | LIMIT-03 |
| 「装前扫描 = 安全」 | 真实行为安装前不可判定；正确判据是「组合形状」+ 可回滚 | LIMIT-08 |
| 「能力披露缺失 = 安全」 | 空披露可能是零依赖，也可能是扫描器没覆盖；披露 / 策略 / 强制 / 判决是四件事 | LIMIT-01 |
| 「沙箱 = 全覆盖」 | 沙箱只覆盖文件；网络与进程没有策略词汇，生态只能在沙箱外再造门 | LIMIT-01 · LIMIT-05 |

### 5.3 假恢复

| 陷阱 | 真相 | 出处 |
|---|---|---|
| 「重试 = 幂等」 | 没有幂等键的重试通道，重投就是重复执行 | CROSS-08 |
| 「atomic-write = 崩溃持久」 | 官方明说不 `fsync`，只保证不出现半截文件 | PROVE-01 §3.4 |
| 「present = 交付版本已持久化」 | 交付版本持久化与写时复制存储「延期实现」；present 只给指针 + 本轮摘要 | PROVE-01 §3.4 |
| 「哈希链 = 事是真的」 | 只证「发生过、顺序、未被篡改」；锚点必须在链外，否则可被一起重写 | PROVE-05 |

### 5.4 假数据

| 陷阱 | 真相 | 出处 |
|---|---|---|
| 「星标 = 使用量」 | 4★ 有 3,103 次月下载、0★ 根本没上 npm；星标是滞后指标 | CROSS README · LIMIT README |
| 「npm 包名 = 仓库名」 | 三个同名不同人的坑；装之前先核 `package.json` 的 `repository` | LIMIT README |
| 「目录内被引 = 影响力」 | A 门有撞词噪声（terminal / notification / schedule / calendar） | horizon §4 |
| 「全库只有 N 条 / 命中率 0.x%」 | 名单一直在涨，这个数明天就变；它只说明**当时的描述文本**，不证明能力 | [horizon](./horizon.md) §4 |

### 5.5 假门禁

| 陷阱 | 真相 | 出处 |
|---|---|---|
| 「提示词里写请检查」 | 2 级建议，不是门禁；官方 `dsh-plan-mode` 自己说「引导而非强制」 | PROVE-01 §3.3 |
| 「默认 remind 也是个门」 | 装上 ≠ 生效；默认档位决定门是不是真实存在 | PROVE-09 |
| 「判官能撤回文本」 | 判动作能真拦，判文本只能追赶；`turn-stopping` 不给草稿 | PROVE-06 |

## 6. 还没解决的事

> 这一节是给研究者和上游的入口。每条都能对应到一个具体缺口；引用时请带出处，不要把 `[OPEN]` 写成 `[OBS]`。

### 6.1 官方缺口

- **⑥ 验收环没有原生机制**；`dsh-plan-mode` 只做引导（[PROVE-01](./lever-prove-output/01-quality-chain.md)）。
- **`present` 的交付版本持久化、写时复制存储延期实现；`atomic-write` 不 `fsync`**（[PROVE-01](./lever-prove-output/01-quality-chain.md) §3.4 / [PROVE-08](./lever-prove-output/08-delivery-receipt.md)）。
- **`agent/turn-stopping` 不携带本轮草稿**，所以判官永远只能拿到上一轮的成品（[PROVE-06](./lever-prove-output/06-judge-placement.md)）。
- **`dsh-tool-goal` 的硬约束全朝向「不许放弃」，没有一条朝向「不许自宣成功」**（[PROVE-02](./lever-prove-output/02-goal-gate-hard-floor.md)）。
- **沙箱没有网络 / 进程策略词汇**；官方 Team 的 `writeScopes` 不拦任何写入（[LIMIT-01](./lever-draw-limit/01-trust-layers.md) / [CROSS-01](./lever-cross-boundary/01-collab-topology.md)）。

### 6.2 生态缺口

- **E 级反例只有 2 条真判**，其余失败模式来自官方限制推演（[horizon](./horizon.md) §7）。
- **规格独立性问题**：所有验收契约（JSON spec / AC 命令 / SOP 目录）都可能由被判定者自己写；只有 `dsh-verify` 明说「review the spec separately」（[PROVE README](./lever-prove-output/README.md) 待答）。
- **多门禁共存没有统一 deny 协议**：同时装 3 个门禁时，谁先判、被判者能否看到全部 deny 理由（[PROVE README](./lever-prove-output/README.md) 待答）。
- **没有人给自己的租约加 epoch / fencing**：是成本问题，还是宿主没给可绕过的写面钩子？（[CROSS README](./lever-cross-boundary/README.md) 待答）
- **workflow 引擎的「可恢复」普遍是快照重跑**，不是断点续跑（[CROSS-03](./lever-cross-boundary/samples/03-omdsh-dev-dsh_workflow.md)）。

### 6.3 方法缺口

- **RESHAPE 没有 commit 锚点**：证据深度逐卡标注（源码级 / README 级），多数只锁版本、少数实测，未锁 `repo@commit`；要逐字复核得按版本找 tag（[RESHAPE README](../leverage-reshape-product/plugin/README.md) §4.1）。
- **A 门撞词噪声未清**：层级前 5 名至少 4 个是通用词（[horizon](./horizon.md) §4）。
- **「少见 / 唯一」没有可重跑的计数**——这是刻意的；引用时带日期、标 `[OBS]`，接受它会过时（[horizon](./horizon.md) §7）。
- **证据强度分域，不能互推**：PROVE 锁 commit；CROSS / LIMIT 读源码但只锁版本；RESHAPE 分卡标注、未锁 commit（[README](./README.md) §7 / [horizon](./horizon.md) §7）。

### 6.4 回源五步

1. **拿坐标**：在卡的「精确坐标」或域 README 的坐标表里取 `repo` + `npm` + `version`；PROVE 的样本取 **commit**。
2. **锁到那一份**：`git clone` 后按版本 tag 或短 SHA 打开；不要用 `main`。
3. **按符号读**：用卡里给出的函数名 / 常量 / 字段去 grep，不要按章节通读。
4. **人工判断唯一性**：回读同域与相邻域的样本表；找不到同类机制才写「少见 / 唯一」，标 `[OBS]` 与日期。**不要写命中数**——名单在涨，数字会过期。
5. **回报差异**：结论变了就改卡的 `status` / 数字，并在域 README 对应行标注；若推翻分级，按 [horizon](./horizon.md) §8 重审。

## 7. 借用记录模板

> 抄的时候填这张表。**填不出「失效条件」就是还没读懂**；填不出「复核点」就是抄了一个无法维护的东西。

| 我借的 | 借自（文件 §） | 我改了什么 | 为什么改 | 失效条件 | 复核点 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

三条纪律：

1. **先写失效条件，再写功能**。写不出失效条件的方案，不是工程，是信仰。
2. **一个机制只在一处有完整论证**。引用时给文件 + 节号，不复制论证。
3. **升级后重跑**：`node _leverage/verify.mjs`；catalog 手工补一行。若样本掉门，按 [horizon](./horizon.md) §8 重审。

---

**找不到对应行？** 用 [catalog](./catalog.md) 按 `read_when` 的任务词 grep；或从 [README](./README.md) 的「五个最容易读错的地方」重新进。
