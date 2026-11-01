---
title: "catalog · 全量文件清单"
domain: layer
kind: index
positioning: "全部 Markdown 的 kind、定位、能拿走什么、什么时候读（本文件手工维护）。"
read_when: "想一次看全所有文件，或按关键词找入口。"
status: living
updated: 2026-10-31
---
# catalog · 全量文件清单

> **手工维护。** 新增 / 改名文件时补一行；数量不在这里统计（名单和卡片都还在长）。
> 用法：按 `read_when` 的任务词 grep，或按 `kind` 过滤。

**六列怎么用**：`定位`答「它是什么」，`能拿走什么`答「值不值得打开」，`什么时候读`用任务词写，能直接 grep。

## 层共享件 ｜ `layer`

| 文件 | kind | 定位 | 能拿走什么 | 什么时候读 | 状态 |
|---|---|---|---|---|---|
| [`README.md`](./README.md) | index | 本层唯一入口：说明这套研究回答什么、文件怎么分工、按目的怎么读。 | — | 第一次进这个目录；或不确定该读哪一篇时。 | living |
| [`BORROW.md`](./BORROW.md) | guide | 跨域借用总入口：按需求路由到具体章节，并给出四域最小集、跨域法则与陷阱。 | 8 条任务路由 + 6 条跨域法则 + 7 个必答问题 + 19 个陷阱 + 回源五步。 | 要写插件/做产品/做协作/做质量/做安全；或要评审、选型、回源、给官方提缺口。 | living |
| [`00-map.md`](./00-map.md) | charter | 研究宪章：杠杆阶梯、命名约定、证据协议、文件约定与基线。 | — | 要判断一个插件占的是哪一级位置；或要新增卡/新域、改口径时。 | living |
| [`horizon.md`](./horizon.md) | charter | 规则单一源：A/B/C/D/E/F/G 准入门、S/A/B/C 分级、每条必写的六项。 | — | 要把一个新样本立成卡；或质疑某条样本凭什么在场时。 | observed |
| [catalog.md（本文件）](./catalog.md) | index | 全部 Markdown 的 kind、定位、能拿走什么、什么时候读（本文件手工维护）。 | — | 想一次看全所有文件，或按关键词找入口。 | living |
| [`AUDIT.md`](./AUDIT.md) | guide | 审计基线与分批：46 篇的起始缺口、批次与完成标准。 | 接续证据化工作；查哪些样本/章节已升级。 | living |

## CROSS · 协作边界 ｜ `cross-boundary`

| 文件 | kind | 定位 | 能拿走什么 | 什么时候读 | 状态 |
|---|---|---|---|---|---|


## CROSS · 样本证据（固定版本）

| 文件 | kind | 定位 | 能拿走什么 | 什么时候读 | 状态 |
|---|---|---|---|---|---|

## PROVE · 质量门禁 ｜ `prove-output`

| 文件 | kind | 定位 | 能拿走什么 | 什么时候读 | 状态 |
|---|---|---|---|---|---|
| [`README.md`](./lever-prove-output/README.md) | charter | 本域宪章：六环质量链、六条设计律、12 个样本坐标与按用途的阅读导览。 | 64 条编号原则 + 八问评估 + 12 个样本的坐标与 commit。 | 要做质量/门禁/验收；或评审一个质量插件。 | observed |
| [`00-sample-lineage.md`](./lever-prove-output/00-sample-lineage.md) | index | 每个样本的 repo@commit、锚点文件、重抓命令与陷阱，是全部断言的回源入口。 | 17 个仓库的 HEAD 已锁；没绑 commit 的抓取等于没抓。 | 要复核某条断言；或三个月后重挖一个样本。 | observed |
| [`01-quality-chain.md`](./lever-prove-output/01-quality-chain.md) | playbook | 质量链底盘：六环里只有检查点与版本新鲜度是原生硬门禁，验收整环缺席。 | 六环骨架 + 六条设计律；生态几乎全挤在⑥验收。 | 要先知道上游到底保证了什么，再决定把门装在哪。 | observed |
| [`10-quality-control-playbook.md`](./lever-prove-output/10-quality-control-playbook.md) | playbook | 质量控制手册：十二个生态样本的横向结论与 64 条编号原则。 | Q/V/F/A/E/R/P/C 八组 64 条原则 + 八问评估顺序；只想记七条在 §7.9。 | 要写/评审质量插件；或要把原则贴进设计文档引用（「按 Q3 处理」）。 | observed |
| [`02-goal-gate-hard-floor.md`](./lever-prove-output/02-goal-gate-hard-floor.md) | card | 完成声明门禁：唯一能在副作用后说「不」的位置（tools/pre-execute）。 | 只拦 4 种完成声明、门禁自己重跑 AC、假完成 2 次冻结、契约改动即失效。 | 要让「做完了」变成可验证的声明；或要设计一个 deny 分支。 | observed |
| [`03-turn-end-reconciliation.md`](./lever-prove-output/03-turn-end-reconciliation.md) | card | 轮末对账：把「我说我读了」与「本轮真读过什么」摆在一起。 | 本轮工具输出做证据池；对账永不拦、动作可拦；否决权按确定性分配。 | 要防止模型声称读过/做过但实际没有；或要设计 turn-stopping 钩子。 | observed |
| [`04-evidence-index.md`](./lever-prove-output/04-evidence-index.md) | card | 证据索引：只判出处不判语义，并把防误杀做成五级阶梯。 | 五级反误杀阶梯 + converted/charity 反向指标；判决绑定输入。 | 要给回答加「有没有出处」的硬门；或你的门禁误杀太多。 | observed |
| [`05-custody-chain.md`](./lever-prove-output/05-custody-chain.md) | card | 保管链：用两个样本划出哈希链的能力边界。 | 证「没被改」不证「事是真的」；锚点必须在链外；只存哈希不存内容。 | 要做审计/回执/证据链；或有人拿「不可篡改」当卖点。 | observed |
| [`06-judge-placement.md`](./lever-prove-output/06-judge-placement.md) | card | 判官装在哪：五种位置，五种调解不了的风险。 | 判官能改什么取决于接缝；判动作能真拦，判文本只能追赶。 | 要给回答加第二模型评审；或要判断一个「AI 评审」是不是验收。 | observed |
| [`07-foreign-runtime-acceptance.md`](./lever-prove-output/07-foreign-runtime-acceptance.md) | card | 换运行时验收：判官不在会话里，是⑥环唯一真正独立的验收。 | 换进程/换运行时；退出码给门禁、结构化判决给诊断；规格仍可能由被判者写。 | 要做独立验收/真浏览器验收；或要设计外部进程判定。 | observed |
| [`08-delivery-receipt.md`](./lever-prove-output/08-delivery-receipt.md) | card | 交付回执：把「谁验收的」与「文件是什么」分开记。 | 回执=(文件版本,谁看见,谁说的)；模型侧无 decide；重检不替换基线。 | 要做交付确认/用户验收；或要防止「重检顺手改基线」。 | observed |
| [`09-discipline-loop.md`](./lever-prove-output/09-discipline-loop.md) | card | 纪律环：把六环串成流程，让默认值决定它是否真实存在。 | red 先于 green；默认 remind → 装上≠生效；对抗评审放进分叉子代理。 | 要做流程型质量插件（TDD/评审环）；或要设置门禁默认档。 | observed |

## LIMIT · 安全监管链 ｜ `draw-limit`

| 文件 | kind | 定位 | 能拿走什么 | 什么时候读 | 状态 |
|---|---|---|---|---|---|
| [`README.md`](./lever-draw-limit/README.md) | charter | 本域宪章：信任三层、强制点与失效方向、10 个样本坐标与 21 行借法一览。 | 21 行借法一览（问题→抄哪条）+ 三层监管链 + 名字会骗人的三个坑。 | 要做安全/权限/审批/供应链；或评审一个安全插件。 | observed |
| [`01-trust-layers.md`](./lever-draw-limit/01-trust-layers.md) | playbook | 安装面/运行面/数据面三层监管链，逐层指出原生强制点在哪、缺在哪。 | 披露≠策略≠强制≠判决；沙箱只覆盖文件，网络与进程无策略词汇。 | 要判断一个安全插件属于哪一层；或要说明原生到底保证了什么。 | observed |
| [`09-control-budget.md`](./lever-draw-limit/09-control-budget.md) | playbook | 控制预算：七个样本为什么收敛到三个动词，以及从零搭控制点的八个决定。 | 最小充分集=沙箱+一处不可推翻的否决+fail-closed；八个决定是施工图。 | 要从零做一个安全控制点；或要解释为什么不需要第四套机制。 | observed |
| [`02-approval-budget.md`](./lever-draw-limit/02-approval-budget.md) | card | 审批预算：把「问几次」当成可耗尽的资源，硬拒免费、确认有额度。 | 八层管道模板 + 额度折算四前提 + 三条验收测试。 | 要做审批/放行/免打扰；或你的审批已经让人开始无脑点同意。 | observed |
| [`03-second-model.md`](./lever-draw-limit/03-second-model.md) | card | 第二模型：权威放在哪一侧，决定它是优化还是边界。 | 五条硬约束 + 3×2 决策矩阵 + 六个真实漏洞与修法；unavailable 即拒绝。 | 要接一个模型做判定；或要判断「AI 审批」能不能当授权。 | observed |
| [`04-guard-vs-pump.md`](./lever-draw-limit/04-guard-vs-pump.md) | card | 守卫与泵：同步谓词只能回答一次，复杂策略必须搬去别处。 | 同步守卫四铁律 + 沙箱让位五道闸 + 边界表模板。 | 要挂 ctx.tools.guard；或发现守卫里塞了重活。 | observed |
| [`05-network-gate.md`](./lever-draw-limit/05-network-gate.md) | card | 网络门：沙箱没有网络词汇，只能在沙箱外再造一道进程出口闸。 | 四步定位法 + 出口门三规则 + 一键放行四件套；明确写下代理管不到谁。 | 要拦外联/做网络策略；或要给 shell 子进程加出口门。 | observed |
| [`06-injection-seam.md`](./lever-draw-limit/06-injection-seam.md) | card | 缝的位置：挂 pre-step 才能看见「模型已经被说服」。 | 接缝选型表；能拦≠能解释≠能协商；范围×默认值×装得上。 | 要做注入防护/提示词防线；或要在两条缝之间选一条。 | observed |
| [`07-beyond-sandbox.md`](./lever-draw-limit/07-beyond-sandbox.md) | card | 沙箱之外：同一个缺口的收紧与放松，两者成本不对称。 | 重新围栏四规则 + 放绿灯五匹配 + 状态存放决策表。 | 要在沙箱外再围一道，或要自动批准某类操作。 | observed |
| [`08-install-face.md`](./lever-draw-limit/08-install-face.md) | card | 安装面：事前看「组合形状」，事后只做可回滚的隔离。 | 组合形状四规则 + 五步自救 + 判据选择法；可逆性优于预测。 | 要做装前审计/升级回滚；或要判断一个扫描器是不是装后才跑。 | observed |
