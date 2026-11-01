---
title: "lever-prove-output：质量门禁"
domain: prove-output
kind: charter
positioning: "本域宪章：六环质量链、六条设计律、12 个样本坐标与按用途的阅读导览。"
takeaway: "64 条编号原则 + 八问评估 + 12 个样本的坐标与 commit。"
read_when: "要做质量/门禁/验收；或评审一个质量插件。"
status: observed
updated: 2026-10-31
budget: 320
---
# lever-prove-output · 门禁装在哪一环，产物凭什么算完成

> **标语**:*Where is the gate that turns "looks done" into "proven"?* —— 质量是门禁位置，不是评审力度。
> **状态**:`observed`(机制已核) · **基线**:DSH `0.2.1-rc.3` · 名单 @ `efe602e7b`
> **作业区**:**本目录自足、可独立开工**。只读共享件,不写共享件;不引用其他域的结论,不等待其他域的进度。四域并行契约见 [`../README.md`](../README.md#两域并行作业契约)。
> **借阅入口**:想抄 → [64 条原则](./10-quality-control-playbook.md#7-可借鉴可搬走的原则总表本域的核心产出) · 想选型 → [选择要求](#选择要求) · 想评审 → [八问检查顺序](./10-quality-control-playbook.md#8-一份可执行的检查顺序) · 想回源 → [精确坐标](#精确坐标重新挖掘的入口) · 跨域 → [BORROW](../BORROW.md)
> **规则源**:准入/分级以 [`horizon`](../horizon.md) 为准;本域的准入副本是摘要。
> **全量卡片**:本表是精选;全部文件(kind/定位/能拿走什么/何时读)见 [`catalog`](../catalog.md)。

## 怎么用这份材料(先读这里)

**这不是一份插件评测合集。** 每个样本都按同一个骨架写:**它解决什么真问题 → 机制怎么落(到源码行)→ 影响力证据(可回读) → 哪里会坏(具名条件)→ 你能搬走什么(做法 + 为什么有效 + 怎么搬 + 反面)**。

每张卡都有一个 **「可借鉴」** 节,那是主体,不是附录。九张卡的「可借鉴」合计 **69 条**,编号后汇总在 [`10`](./10-quality-control-playbook.md) §7,可以贴进你自己的设计评审里引用(「这里按 Q3 处理」)。

四条读法,按你的目的选:

| 你的目的 | 从哪读 | 会拿到什么 |
|---|---|---|
| **我要自己写一个质量插件** | [`01`](./01-quality-chain.md) §6 六条设计律 → [`10`](./10-quality-control-playbook.md) §7 总表 → 你那个接缝对应的卡 | 一张设计契约:门装哪、判什么、错了怎么办、默认档怎么设 |
| **我要选一个装在自己身上** | [`10`](./10-quality-control-playbook.md) §8 八个问题 → 各卡「评估清单」 | 八句话筛掉 90% 的「提示词冒充门禁」 |
| **我要评审别人的质量方案** | [`10`](./10-quality-control-playbook.md) §1 接缝表 + §4 权限阶梯 | 两个坐标轴,定位任何方案的硬度和可信度 |
| **我要给官方提缺口** | 各卡「开放问题」+ [`10`](./10-quality-control-playbook.md) §6 共同失败 | 七条结构性失败,每条都能对应到一个原生能力缺失 |

**一条阅读纪律**:本域反复出现「**看着对、其实反了**」的结论(默认软 ≠ 没做、对账 fail-open 才对、哈希正确 ≠ 内容正确、more stars ≠ deeper mechanism)。**只读摘要会读反**,所以每条结论后面都跟着它的代价与反面——**别跳过「反面」那一行**。

## 这个域问什么

一个 agent 说“做完了”。这句话什么时候可以被当作事实？答案不取决于评审多么严格，而取决于**门禁装在哪一环**——装得越靠近副作用，越硬；装在文字层，就只是建议。

**判断标准**：一个质量插件是**建议**还是**保证**，看它落在 prompt 层、工具层，还是持久化/副作用层。

## 收录 / 不收录

收录：

- 在**动作发生前**拦截或放行的（执行门禁、预检、危险操作拦截）
- 在**动作发生后**留存可复核痕迹的（回执、审计链、证据定位符）
- 定义**产物如何持续存在**的（检查点、原子写、回滚、快照、交付声明）
- 定义**独立验收**的（第三方浏览器验收、阈值门禁、结构化判定）

不收录：

- “请仔细检查”类提示词技能 → 除非它改了工具或持久化行为
- 代码风格、lint 配置 → 属普通工具
- 纯成本统计面板 → 归 `lever-reshape-product` 的槽位层，除非它触发了拦截

## 准入(本域自带副本,不依赖任何其他文档)

**不是抓到一个就琢磨。** 研究对象不随名单膨胀:**卡片数不随收录量涨,只随「机制被验证」涨**。

| 组 | 证据 | 怎么判 |
|---|---|---|
| 影响力 | **A** 被目录内其他条目按名提到 · **B** 自述替换/接管官方对象 · **C** 自述具名接缝 · **F** 全库同类机制少见 | A/B/C 回读原文;**F 人工判断,标 `[OBS]`,不计数** |
| 深度 | **D** 能力披露 · **E** 明指不可共存 / 同缝取反 · **G** 机制已核且有具名失效条件 | D 查 capabilities;**E/G 人工** |

**缺一不立卡。** 分级:**S** 定义型(后来者的模板)→ 单独卡片 · **A** 代表型(当前优解)→ 卡片「标杆」正例 · **B** 对照型 → **不立卡**,只作一行对照 · **C** 反例型 → 失败模式表一行。

每条进入卡片的样本必须写齐六项:**代表什么典型 / 为什么选它(过的哪几条证据)/ 影响力证据(被谁提到、替换了哪个官方对象、或官方原文;不要求计数)/ 主要特点(机制层)/ 代价与失效条件(具名)/ 证据级别**。缺一项退回。

### 本域专项加分项

- **门禁位置可命名**:必须指到 **六环**中的一环,且指出它挂在哪条缝——`tools/pre-execute`、`tools/post-execute`、`agent/pre-step`、持久化 flush、还是独立验收器。
- **可复核性可验证**:它留下的东西,别人能独立重放(重放输入)或定位(重放日志某几行)。

### 本域明确不收

- 提示词里写「请仔细检查」「务必验证」的技能包 → 2 级,官方 `dsh-plan-mode` 自己都说「引导而非强制」
- 只统计不拦截的成本/用量面板 → 槽位层
- 自查冒充验收(同一个 agent 写测试自己判过)→ 判定与执行未分离,直接出局

### 本域研究对象(主读,单一归属)

原生机制(S 级,定义型):

| 级 | 样本 | 过了哪些门 | 影响力证据(可复核) | 一句话特点 |
|---|---|---|---|---|
| **S** | 官方 `dsh-session-checkpoint-policy` | G | 三处屏障写自官方 README;全库唯一 fail-closed 的**副作用前**屏障 | 保证「至少知道发生了什么」,不保证「只发生一次」 |
| **S** | 官方 `dsh-fs-observation-policy` | G | 唯一把「读过」变成**版本约束**的机制 | 策略只做决策不做 I/O 的范式 |
| **S** | 官方 `dsh-plan-mode` | G | `exit_plan_mode` 评审式退出;官方自述「引导而非强制」 | ② 环唯一的官方接缝,**明说是软的** |
| **S** | 官方 `dsh-atomic-write` / `dsh-tool-present` / `dsh-workspace-changes` | G | present 明说「交付版本持久化与写时复制存储延期实现」;atomic-write 明说不 `fsync` | ⑤ 环原生只给**指针 + 本轮摘要** |
| **S** | 官方 `dsh-tool-goal` | G | 唯一处「模型不能自宣终止」的硬约束(`blocked` 需连续 3 轮,机械拒绝) | 原生的硬约束全部朝向**「不许放弃」**,没有一条朝向**「不许自宣成功」** |

生态样本(每条都已回读来源 README 或源码,不再只依赖 catalog 简介):

| 级 | 样本 | 过门 | 影响力证据(可复核) | 门禁位置 | 一句话特点 | 卡片 |
|---|---|---|---|---|---|---|
| **S** | `samirliu/dsh-goalloop-agentteams` | C·D·F·G | `update_goal` **很少** · `假完成` **很少** · ★1 | `tools/pre-execute` | **源码级**:只拦 4 种完成声明、门禁自己重跑 AC、假完成 2 次冻结、契约改动即批准失效 | [02](./02-goal-gate-hard-floor.md) |
| **S** | `rootsbymenda/dsh-second-angle` | C·D·F·G | `agent/turn-stopping` **很少** · ★0 · 24 例公开评测 | `agent/turn-stopping` | 本轮工具输出做**证据池**,矛盾才 steer;对账永不拦,动作可拦 | [03](./03-turn-end-reconciliation.md) |
| **S** | `bycall/dsh-answer-reviewer` | C·D·G | ★10 / fork5 · 本域最高 fork | `agent/turn-stopping` | 判官只读**真实用户提示**;分数绑 `message.id`;解析 fail-closed | [06](./06-judge-placement.md) |
| **A** | `AaronandWork/dsh-evidence-gate` | C·D·G | ★8 · `证据\|evidence` 很多 | `systemPrompt.section` + `tools/result` | 五级**反误杀阶梯** + `converted`/`charity` 反向指标 | [04](./04-evidence-index.md) |
| **A** | `030611/qiushi-dsh-evidence-audit` | F·C·D·G | `hash.?chain\|哈希链` **很少** · ★3 | `tools/result`(只观察) | 最小留存:只存哈希,`0700/0600`,并列出**检测不到的三种情形** | [05](./05-custody-chain.md) |
| **A** | `zhengqiuyang/dsh-attest-chain` | F·C·D·G | `ed25519` **很少** · ★0 | `tools/result`(只观察) | 每条签名 + 绑 git SHA + `verifyChain()` 返回**第一个坏点**;自带 kill criteria | [05](./05-custody-chain.md) |
| **A** | `263311487-ux/dsh-verify` | C·D·F·G | `真浏览器\|chromium` 不少 · ★2 | 外部进程 | 真浏览器执行 JSON 规格;三入口三种独立性;四个「不证明」 | [07](./07-foreign-runtime-acceptance.md) |
| **A** | `4444wjt/dsh-plugin-veriscope` | F·C·D·G | `永不转` **很少** · 三值组合 **很少** | 外部进程(纯 Node) | 不重新评测、不调模型;**REVIEW 永不转 PASS** | [07](./07-foreign-runtime-acceptance.md) |
| **A** | `oxmumu3/dsh-workproof` | C·D·F·G | `用户验收\|user acceptance` **很少** · ★0 | `conversation.view` + 工具 | 交付回执:**没有 `decide` 动作**;重检永不替换基线 | [08](./08-delivery-receipt.md) |
| **A** | `PerryLink/dsh-doublecheck` | C·D·F·G | ★**59**(本域最高)· `test evidence` 不少 | 多接缝 + fork 子代理 | 六阶段纪律环;**red 必须先于实现**;默认 `remind` | [09](./09-discipline-loop.md) |
| **A** | `CAI-MH/dsh-quality-review` | C·D·G | ★2 / fork1 | `agent/turn-stopping` | 四维 + **团队 SOP 目录**(文件名当关键词,整目录当标准) | [06](./06-judge-placement.md) |
| **A** | `Jonah-Wu23/dsh-gungnir` | C·D·F | ★6 · `假完成` 很少 之一 | `tools/pre-execute` | 目标锁定 + 自适应轮次;给出 **54 runs** 分臂实验数据 | [02](./02-goal-gate-hard-floor.md) |

**B 级(不立卡,只作对照行)**:`JayYuen666/dsh-quality-gate` @ `abb6266`(轮末命令白名单 + `agent.followup` 修复轮;脆在版本耦合)、`1052326311/dsh-plan-lattice` @ `ea4d4f7`(② 环自建网格,★3,v0.3.0)、`Jonah-Wu23/dsh-gungnir#dsh-plugin` @ `4038c3e`(**monorepo 子包** `packages/dsh-plugin`)、`1687210989/agent-clinic` @ `e88d6ec`(22 项诊断 + `#L<a>-L<b>` 定位符)。

**未进卡但记了坐标**:`863683348/dsh-plugin-gate` @ `b75c3a1`(60 条静态签名规则 + 12 种危险命令;归属偏 [`draw-limit`](../lever-draw-limit/README.md))、`guo6x/dsh-shipcheck`(**无 commit,不可追溯** `[OPEN]`)。完整表见 [`00`](./00-sample-lineage.md) §2。

**C 级(反例格,只在失败模式表里出现一行)**:`XiaoOu2024/dsh-self-review`(`llm/stream` 扣留,同时提供「`turn-stopping` 有没有 modelOutput」的否定式机制证据)。

**借用但非主读**(只可一句引用,不深读、不立卡):`dsh-sandbox-policy`、`dsh-experimental-auto-review`(主读均在 `lever-draw-limit`,本域仅在 [06](./06-judge-placement.md) §3.4 引一句「判动作可以真拦,判文本只能追赶」)、`dsh-experimental-agent-team`(主读在 `lever-cross-boundary`,本域仅在 [02](./02-goal-gate-hard-floor.md) 引一句 `writeScopes` 只是提示)。

### 精确坐标(重新挖掘的入口)

**每条断言都要能回到具体的一份代码上。** 全表在 [`00`](./00-sample-lineage.md):`repo` · **commit SHA** · 目录引用名 · 版本/星标/下载 · 锚点文件 · 一条 `curl` 重抓命令 · 已核的关键符号。

抓取时间 **2026-10-31 14:00 CST**,全部 HEAD 已锁。**不是 `main`,是短 SHA** —— 用 `main` 打开的代码会在三个月后变成另一份,而你以为还是那一份。

| 样本 | 锁定 commit | 目录引用名(装的时候用这个) | ⚠️ 陷阱 |
|---|---|---|---|
| [`samirliu/dsh-goalloop-agentteams`](https://github.com/samirliu/dsh-goalloop-agentteams) | `6b4b1fa` | `samirliu/dsh-goalloop-agentteams` | 逻辑在打包产物 `lib/index.js`;名字里的 `agentteams` 会让人以为只服务多 agent |
| [`rootsbymenda/dsh-second-angle`](https://github.com/rootsbymenda/dsh-second-angle) | `9ac01ed` | `rootsbymenda/dsh-second-angle` | v0.1.0;源码那份**未绑 commit**,`[OPEN]` |
| [`AaronandWork/dsh-evidence-gate`](https://github.com/AaronandWork/dsh-evidence-gate) | `845ddf4` | `AaronandWork/dsh-evidence-gate` | tarball 是浮动的 `latest`,没有固定版本号 |
| [`030611/qiushi-dsh-evidence-audit`](https://github.com/030611/qiushi-dsh-evidence-audit) | `94fae13` | `030611/qiushi-dsh-evidence-audit` | 本域**最老**的提交(08-14) |
| [`zhengqiuyang/dsh-attest-chain`](https://github.com/zhengqiuyang/dsh-attest-chain) | `bf83778` | `zhengqiuyang/dsh-attest-chain` | 密钥 `.dsh-attest-chain/keys/` 在仓库目录内 |
| [`bycall/dsh-answer-reviewer`](https://github.com/bycall/dsh-answer-reviewer) | `8c6186a` | `bycall/dsh-answer-reviewer` | **目录 `name` 字段缺 owner**(`dsh-answer-reviewer`),按名字搜不到 |
| [`CAI-MH/dsh-quality-review`](https://github.com/CAI-MH/dsh-quality-review) | `7c5a67d` | `CAI-MH/dsh-quality-review` | **只有 `README.zh.md` 有细节**,英文版会漏机制 |
| [`XiaoOu2024/dsh-self-review`](https://github.com/XiaoOu2024/dsh-self-review) | `a903dff` | `XiaoOu2024/dsh-self-review` | 唯一能动用户所见文本的那个 |
| [`263311487-ux/dsh-verify`](https://github.com/263311487-ux/dsh-verify) | `e7ce637` | `263311487-ux/dsh-verify` | 2088 dl 本域最高,但**不证明规格写对** |
| [`4444wjt/dsh-plugin-veriscope`](https://github.com/4444wjt/dsh-plugin-veriscope) | `5299b64` | `4444wjt/dsh-plugin-veriscope` | 三值判决全库只此一条 |
| [`oxmumu3/dsh-workproof`](https://github.com/oxmumu3/dsh-workproof) | `7096ead` | **`oxmumu3/dsh-workproof#dsh-delivery-receipts`** | **monorepo**:代码在 `packages/dsh-delivery-receipts/`,根目录只有 README + lockfile;根 README 与子包 README **内容不同** |
| [`PerryLink/dsh-doublecheck`](https://github.com/PerryLink/dsh-doublecheck) | `22fe2e0` | `PerryLink/dsh-doublecheck` | **它自己 README 里的路径是错的**:写 `plugins/dsh-doublecheck/src/...,` 公开仓库实为 `src/guard/prose.ts`(照抄 404) |

**两条不可让步的纪律**:

1. **抓完立刻记 commit。** 本域已经有两个文件(`second-angle` 源码、`guo6x/dsh-shipcheck` README)因为没记 commit 变成 `[OPEN]`,现在追不回来。
2. **注了出处,就必须验证出处能打开。** `doublecheck` 的案例说明:一个打不开的出处比没有出处更糟,因为它**看起来**可验证。

**官方包不在这份名单里**, 搜不到。原生侧断言只能读本机安装目录:`$(npm root -g)/@deepseek-ai/dsh/node_modules/@deepseek-ai/`,清单见 [`00`](./00-sample-lineage.md) §3。

> **本轮的证据级别升级**:上一轮所有样本的证据级别停在「catalog 自述 + 官方包 README」。本轮 **12 个生态样本的来源 README 已逐条回读**,其中 `goalloop` 另读了 `lib/index.js` 源码(四条 deny 分支、假完成计数器、`treeDigest` 重判逻辑),因此它标 `observed` 而不是 `inferred`。仍标 `inferred` 的样本在各自卡片「证据级别」栏注明原因。

## 选择要求

1. **门禁位置可指认**：它挂在哪一环——`tools/pre-execute` / `tools/post-execute` / `agent/pre-step` / `llm/stream` / 持久化 flush / 验收器？说不出位置的，只能算建议。
2. **可复核性可验证**：它留下的东西，另一个人（或另一个 agent）能不能**独立重放**？只留“我说我检查了”的不算证据。
3. **失败语义明确**：门禁拒绝时会发生什么？是 fail-closed（阻止副作用）、fail-open（放行并记录）、还是转人工？三者混用的样本必须点明。

## 领域骨架：六环质量链

| 环 | 问题 | 原生支撑 | 硬/软 |
|---|---|---|---|
| ① 意图 | 目标说清了吗 | 无原生机制 | 软 |
| ② 计划 | 行动前先审计划 | `dsh-plan-mode` | **软**（官方原话：“引导而非强制”） |
| ③ 动作 | 危险动作拦截 | `tools/execute` waterfall + 沙箱/审批 | **硬** |
| ④ 证据 | 留下的痕迹可否重放 | checkpoint policy + 会话日志 | **硬**（有明确边界） |
| ⑤ 产物 | 产物是否原子、能否找回 | `atomic-write`、present | **半硬** |
| ⑥ 验收 | 独立第三方判定 | 无原生机制 | 全生态 |

**核心洞察(待验证)**:②④⑤ 有原生支撑但都不是全硬，①⑥ 完全空白。**生态几乎全挤在 ⑥**（门禁/验收类样本很多 `[CAT]`），而 ① 和 ② 才是“返工”的真正来源。

## 卡片索引

| 编号 | 标题 | 状态 | 一句话结论 |
|---|---|---|---|
| [00](./00-sample-lineage.md) | **样本溯源卡**:精确到 `repo@commit` 的重新挖掘入口 | `observed` | 17 个仓库的 HEAD 已锁 + 锚点文件 + 可复跑 `curl` + 陷阱清单;**没绑 commit 的抓取等于没抓** |
| [01](./01-quality-chain.md) | 质量链：六环里只有两环是硬的 | `observed` | 原生保证集中在"动作前持久化"和"版本新鲜度"；验收整环缺席，全靠生态 |
| [02](./02-goal-gate-hard-floor.md) | 完成声明门禁：唯一能在副作用后说「不」的位置 | `observed` | `tools/pre-execute` 能拦住**完成声明**这个调用；门禁自己重跑 AC、假完成 2 次冻结、契约改动即批准失效 |
| [03](./03-turn-end-reconciliation.md) | 轮末对账：把「我说我读了」与「本轮真读过什么」摆一起 | `observed` | 本轮工具输出做证据池；**对账永不拦、动作可拦**——否决权按结论确定性分配 |
| [04](./04-evidence-index.md) | 证据索引：把「防误杀」做成阶梯，而不是阈值 | `observed` | 五级反误杀阶梯 + `converted`/`charity` 反向指标；**只判出处，不判语义** |
| [05](./05-custody-chain.md) | 保管链：哈希链能证什么、不能证什么 | `observed` | 证「没被改」不证「事是真的」；**连「文件被整个删掉」都证不了**——锚点必须在链外 |
| [06](./06-judge-placement.md) | 判官装在哪：五种位置，五种调解不了的风险 | `observed` | 判官能改什么取决于**站在哪个接缝上**，不是它多聪明；判动作能真拦，判文本只能追赶 |
| [07](./07-foreign-runtime-acceptance.md) | 换运行时验收：判官不在会话里 | `observed` | 换运行时是唯一的真独立；代价是规格必须事先写成可执行形式，而规格仍可能由被判者写 |
| [08](./08-delivery-receipt.md) | 交付回执：把「谁验收的」与「文件是什么」分开记 | `observed` | 回执 = (文件版本, 谁看见的, 谁说的)；**模型侧没有 `decide`**；重检永不替换基线 |
| [09](./09-discipline-loop.md) | 纪律环：把质量写成流程，让默认值决定它是否真实存在 | `observed` | 六阶段只有 red/green 可机械判定；**默认 `remind` 意味着装上 ≠ 生效** |
| [10](./10-quality-control-playbook.md) | 质量控制手册：十二个生态样本的横向结论 | `observed` | 横切 02–09：四个问题 + **64 条编号原则总表(Q/V/F/A/E/R/P/C)** + 七条共同失败 |

每张卡的 **「可借鉴」** 节条数:01 → 6 条设计律 · 02 → 7 · 03 → 8 · 04 → 6 · 05 → 8 · 06 → 9 · 07 → 9 · 08 → 8 · 09 → 8 · 10 → 汇总去重成 64 条编号原则。

每张卡还带一条**精确坐标行**(`repo@commit · 目录引用名 · 锚点文件`),见样本表下方的「精确坐标」行与各样本标题下的引用行;完整入口在 [`00`](./00-sample-lineage.md)。

**建议阅读顺序**:[01](./01-quality-chain.md)(原生底盘)→ [10](./10-quality-control-playbook.md)(横向结论)→ 按「最硬的先读」:[02](./02-goal-gate-hard-floor.md) → [05](./05-custody-chain.md) → [03](./03-turn-end-reconciliation.md) → [04](./04-evidence-index.md) → [06](./06-judge-placement.md) → [07](./07-foreign-runtime-acceptance.md) → [08](./08-delivery-receipt.md) → [09](./09-discipline-loop.md)。

## 边界契约(声明式,不依赖他域进度)

四域并行研究时,**归属是事先划定的,不是商量出来的**。本域遇到下列情形只写划给自己的那一半,另一半留给它的归属域;若那一边尚未产出,本域照写,不等待、不代笔。

| 情形 | 归属 | 本域只写到哪 |
|---|---|---|
| **拦截**危险命令、沙箱与审批策略 | `lever-draw-limit` | 只写「这里有个门禁」,不写权限词汇与强制点 |
| 成员之间的消息、任务归属、失败收敛 | `lever-cross-boundary` | 不写 |
| 证据用于**追责 / 合规** | 本域只写「存在性与可复核」 | 强制性、监管链归 `lever-draw-limit` |
| 成本/用量面板 | `lever-reshape-product` | 除非它触发了拦截 |
| 权限档作为产品默认值 | `lever-reshape-product` | 不写 |

**契约的两条硬约束**:① 本域结论不得把其他域的结论当作前提;② 需要外部事实时写进本域卡片并自带 `[DSH]`/`[CAT]`,不写「见某域」。

## 本域基线(冻结)

> 快照 **2026-10-31** · 名单 @ `efe602e7b` · DSH `0.2.1-rc.3`。**本域只引用这份快照读到的事实,不维护统计口径。**

四域重叠是正常的:本域与 RESHAPE / CROSS / LIMIT 都有样本交集。四域是**四个并列的提问**,不是互斥分类——独立性靠「编辑权 + 主读归属 + 不依赖他域结论」保证,不靠样本不重叠。

## 复核方式

**不设计数门。** 影响力看每张卡的实时采样(带日期);「少见 / 唯一」是人工回读判断,标 `[OBS]`,不附命中数。

## 复核触发条件

**原生侧**:

- `dsh-fs-observation-policy` 的"已观察状态不跨会话保留"若被修复（持久化观测），③④ 两环结论都要改
- `dsh-session-checkpoint-policy` 的检查点位置或 fail-closed 语义变化
- `dsh-plan-mode` 从"引导"变成有强制手段（目前 `:32` 明说「不限制 agent:每个工具都仍可调用」）
- `atomic-write` 加上 `fsync`（目前明确不保证崩溃持久性）
- `dsh-tool-present` 补上"交付版本持久化与写时复制存储"（目前明说延期实现）
- **出现官方「拦截最终文本」的机制**——本域 [01](./01-quality-chain.md) [03](./03-turn-end-reconciliation.md) [06](./06-judge-placement.md) 的核心结论（只能追赶、不能撤回）全部要改
- `agent/turn-stopping` 的载荷若加上本轮草稿（`dsh-agent/README.md:67` 目前只说 can steer），`llm/stream` 派系的存在理由消失、[06](./06-judge-placement.md) 的判官位置表要重建
- `dsh-tool-goal` 若增加「完成必须过验证」的原生语义，[02](./02-goal-gate-hard-floor.md) 整张卡的生态缺口被官方补上

**生态侧**:

- `goalloop` 的六道门（完成声明/契约/临界区/证据/进度/预算）任一被拆或默认值变化;或 `samirliu` 归档
- 任一 `observed` 样本归档、改名、或 README 撤回其自我限制（尤其 `qiushi` 的检测边界表、`dsh-verify` 的四个「不」、`evidence-gate` 的「harness 拦不住最终文本」）
- `doublecheck` 若把默认 `intensity` 改成 `block`，[09](./09-discipline-loop.md) 的「装上 ≠ 生效」结论要改
- `workproof` 若新增 `decide` 动作，[08](./08-delivery-receipt.md) 的权限结论作废
- 出现**把便宜索引与贵语义对账串起来**的样本（[04](./04-evidence-index.md) §10 第一条开放问题），本域需新增卡片

## 待答问题

- [ ] ⑥ 环没有原生机制，是设计选择还是缺口？生态里真正做"独立验收"的（而非自查）有多少？**本轮进展**:按「谁有权说过了」的五级阶梯([10](./10-quality-control-playbook.md) §4)分了层，但**停在 ③④ 两级的具体条目仍未统计**——只能逐个回读。
- [ ] 证据环的"可重放"有两类：**重放输入**（同一次执行再跑一遍）与**重放定位**（回到日志某几行看当时发生了什么）。生态偏哪一类？两者不能互相替代。**本轮进展**:[05](./05-custody-chain.md) 证明 `attest-chain` 走的是「定位」（第一个坏点的 `{seq, reason}`），`veriscope`/`dsh-verify` 走的是「重放输入」；两类各有代表，**但没有样本同时提供**。
- [ ] 产物环里，`present` 声明了交付物却不复制内容——"交付版本持久化与写时复制存储延期实现" `[DSH]`。这算质量闭环的缺口吗？**本轮进展**:[08](./08-delivery-receipt.md) 给出更便宜的近似（版本化基线 + `stale` 判定），但**内容丢失仍无解**；且原生层无 `fsync` 是同一环的另一个洞。
- [ ] **新增** 规格独立性问题：所有样本的验收契约（JSON spec / AC 命令 / SOP 目录）都可能由被判定者自己写。生态只有 `dsh-verify` 明说「review the spec separately」。**这是本域唯一一个「所有人都知道、没人真正解决」的问题。**
- [ ] **新增** 多门禁共存：`goalloop` 源码注释已提到「一律 `{kind:'deny'}` 绝不 throw，避免与其他 quality-gate 的异常路径混淆」。但生态没有统一的 deny 协议——同时装 3 个门禁时，谁先判、被判者能否看见全部 deny 理由？
- [ ] **新增** 本域 `observed` 与 `inferred` 混排。若把「每个 `observed` 断言必须注源码行号」（借用 `doublecheck` 的 `Observed from <file:line>` 写法）升级为硬要求，本域有几条会掉级？
