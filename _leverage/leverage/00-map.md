---
title: "杠杆层总章：四个影响面领域"
domain: layer
kind: charter
positioning: "研究宪章：杠杆阶梯、命名约定、证据协议、文件约定与基线。"
read_when: "要判断一个插件占的是哪一级位置；或要新增卡/新域、改口径时。"
status: living
updated: 2026-10-31
budget: 170
---
# 杠杆层 · 四个影响面领域(总章)

> **这是什么**:围绕「DSH 里影响面大、强力扩充了 DSH 插件的机制」的深读层。目录前缀 `lever-` 是**第二轴**——`ecosystem/` 回答「有什么」,这里回答「改变了什么、改到多深、代价是什么、什么时候会坏」。
> **状态**:三域成稿(2026-10-31):5 份宪章 + 4 份索引 + 1 份借用指南 + 6 份横向手册 + 15 张机制卡 + **14 张样本卡** + 0 份原始证据,共 **45 篇**。**产品线另册**:[`../leverage-reshape-product/`](../leverage-reshape-product/README.md)(33 篇,19 张样本卡),不参与本层统计。本文件只做宪章,**不随卡片数量增长**;全量清单在 [catalog](./catalog.md),按任务借用看 [BORROW](./BORROW.md)。

## 为什么单独一层

DSH 的扩展面是有限的、可枚举的:seam(fs/shell/sandbox/llm/subagent/workflow…)、slot(sidebar/conversation/settings…)、layer(profile/bundle/patch)、policy(observation/checkpoint/permission)、preset、protocol。**插件的影响面,取决于它占的是哪一类位置,而不是它提供了多少个工具。** 所以评估应该问「它占了什么位置」,而不是「它属于哪一类」——前者是可比的,后者不可比。

现有 `ecosystem/` 的 23 类是收录容器(注册表货架),与此轴正交,不合并、不替换。

## 命名:前缀 `lever-` + 一句标语

`lever-`(杠杆点)是这一层的共同前缀:一个插件**占了哪个位置,就能撬动多大一片**。它和 `ecosystem/` 的「类目」正交——类目回答「是什么」,杠杆回答「改了多大、多深、留了什么代价」。四个域并列,没有先后,所以**不加数字**;阅读顺序由下表顺序固定。

| 目录 | 标语 | 见到它先问 |
|---|---|---|
| [lever-cross-boundary](./lever-cross-boundary/README.md) | *Which boundary does collaboration cross, and what does each crossing cost?*<br>协作跨到哪个边界,每跨一界多付什么 | 共享状态归谁?冲突谁裁决?崩溃后谁收敛? |
| [lever-prove-output](./lever-prove-output/README.md) | *Where is the gate that turns "looks done" into "proven"?*<br>门禁装在哪一环,产物凭什么算完成 | 门禁在哪一环?证据能否重放?产物是否原子? |
| [lever-draw-limit](./lever-draw-limit/README.md) | *Who can touch what, who enforces it, what evidence remains?*<br>谁能碰什么,由谁强制,留下什么证据 | 信任谁?边界由谁强制?留下了什么证据? |

**卡片编号**:`<域>/NN-<slug>.md`(一样本一篇时放 `<域>/samples/NN-<owner>-<repo>.md`)。编号**域内递增、不复用、不重排**,只表示写作顺序,不表示优先级,也不跨域比较。退役保留编号,改 `status` 并注明替代者;新增永远追加。**产品线有自己的一套编号法**（「首位 = 类别」+ 三个 lever），见 [`../leverage-reshape-product/`](../leverage-reshape-product/README.md)。

**为什么不用字母编号代号**:`L1–L4` 会让读者以为三域有强弱或先后,而它们实际是三种并列提问;`lift/link/lock/limit` 是为凑首字母造的近义词,彼此冗余。现在的后缀直接说动作,不需要额外解释。

## 杠杆阶梯:判断「为什么它影响面大」

| 级 | 形态 | 影响面 | 例子(DSH 原生) |
|---|---|---|---|
| 1 | tool | 一个 agent 的一个动作 | `present`、`web_fetch` |
| 2 | skill | 一类任务的做法 | agent-experience、cordis-plugin-development |
| 3 | slot | 一个产品体验 | sidebar、right rail、settings 页 |
| 4 | policy | 一条 seam 上的所有动作 | `fs-observation-policy`、`session-checkpoint-policy` |
| 5 | seam backend | 所有消费者 | `ctx.web` / `ctx.shell` 的提供方 |
| 6 | preset / bundle / profile | 一个 agent 或一个产品 | Agent Teams bundle、`dsh-web-app` |
| 7 | protocol / market | 谁能连、谁能被装 | ACP、SDK、MCP、插件市场索引 |

**用法**:卡片里给每个标杆插件标一个级。**升级本身就是洞察**——同一个能力从 2 级升到 4 级(从 prompt 变成 policy)通常意味着它从「建议」变成了「保证」。

## 三域现在有什么

三个域是**三个并列的提问**,不是互斥分类,所以样本会重叠(41–44%)。它们的「分析单位」不同——这正是三个目录长得不一样的原因:

| 域 | 一句话问题 | 分析单位 |
|---|---|---|
| [CROSS](./lever-cross-boundary/README.md) | 协作跨到哪个边界,每跨一界多付什么 | 一个协作样本(一样本一文件)+ 横向卡 |
| [PROVE](./lever-prove-output/README.md) | 门禁装在哪一环,产物凭什么算完成 | 一个门禁位置(一环一卡) |
| [LIMIT](./lever-draw-limit/README.md) | 谁能碰什么,由谁强制,留下什么证据 | 一个控制点/预算(一卡一样本) |

**卡片数不随名单涨。** 全量文件清单见 [catalog](./catalog.md),按任务借用见 [BORROW](./BORROW.md)。

## 文件约定:frontmatter 与生长

**每一篇 Markdown 都有 frontmatter**,由 `verify.mjs` 校验。九个键:

| 键 | 必填 | 取值 |
|---|---|---|
| `title` | 是 | 短标题,不含编号 |
| `domain` | 是 | `layer` / `reshape-product`(产品线) / `cross-boundary` / `prove-output` / `draw-limit`(与路径绑定) |
| `kind` | 是 | `index` `charter` `guide` `playbook` `card` `sample` `evidence` |
| `positioning` | 是 | ≤120 字:它是什么、在整套研究里占哪一格 |
| `takeaway` | card/sample/playbook | ≤80 字:能拿走什么 |
| `read_when` | 是 | ≤80 字:任务词触发(冲突/审批/回滚/多端…) |
| `status` | 是 | `observed` / `inferred` / `open` / `living` |
| `updated` | 是 | `YYYY-MM-DD`,上次核对日期 |
| `budget` | 骨架类 | 行数上限;超了 `verify.mjs` 提醒 |

**三条铁律**:① **不放会漂的数字**(星标/下载/版本/基线日期),它们留在正文页头;② `card`/`sample` 必须有**借用节**(标题含 借鉴/搬走/借用/照抄/食谱/配方/移植);③ **规则只有一个源**——准入/分级看 [`horizon.md`](./horizon.md),四域 README 里的副本是摘要,冲突以源为准。

**生长方式**:新样本 → 过门 → 新卡(frontmatter + 借用节)→ catalog 补一行 → 域 README 只在「本域最佳取法变了」时改一行。**加的是叶子,宪章不跟着长。**

## 研究方法:先过门,再分级

**不是抓到一个插件就琢磨。** 对象不随名单膨胀——**卡片数不随收录量涨,只随「机制被验证」涨**。

| 组 | 证据(每条都要能回读) | 怎么判 |
|---|---|---|
| 影响力 | **A** 被目录内其他条目按名引用 · **B** 自述替换/接管官方对象 · **C** 自述具名接缝 · **F** 全库同类机制少见 | A/B/C 回读原文与被谁提到;**F 是人工判断,标 `[OBS]`,不计数** |
| 深度 | **D** 能力披露(空披露也算,须注明原因) · **E** 明指不可共存 / 同一接缝取反 · **G** 机制已核且有具名失效条件 | D 查 `capabilities.json`;**E/G 人工** |

**缺一不立卡**。过门之后分级:**S** 定义型(后来者的模板)· **A** 代表型(当前优解)· **B** 对照型(**不立卡**)· **C** 反例型(失败模式表一行)。

每条进入卡片的样本必须写齐六项:代表什么 / 为什么选它(过的是哪几条证据)/ **影响力证据(被谁提到、替换了哪个对象、或官方原文;不接受形容词,也不要求计数)** / 主要特点 / 代价与失效条件 / 证据级别。缺一项退回。

完整规则、三域专项条件、分级落位与已知缺口 → [`horizon.md`](./horizon.md)。产品线的准入条件在 [`../leverage-reshape-product/horizon.md`](../leverage-reshape-product/horizon.md)。

## 证据协议:所有卡片共同遵守

**标签**:每条结论标出处。

| 标签 | 含义 |
|---|---|
| `[DSH]` | 原生机制,引用 `@deepseek-ai/<pkg>@<version>` 的 README/配置,写清包名 |
| `[CAT]` | 生态事实,引用 `owner/repo`,并注明是「catalog 描述」还是「能力披露」 |
| `[OBS]` | 观察者判断(可争论),必须给出反例或失效条件 |
| `[OPEN]` | 未验证,留给下一轮 |

**状态**:`observed`(读过机制/实现、样本回读原文)· `inferred`(只有 catalog 描述)· `open`(待研究)。卡片页头统一写这三项。

**纪律**:
1. **披露 ≠ 策略 ≠ 强制 ≠ 判决。** 描述文本讲「作者声称」;`capabilities.json` 讲「会碰什么」;两者都不讲「安全吗」。四者混用是 `lever-draw-limit` 最常见的错误。
2. **不写必装/神器/推荐榜。** 只写「占了哪个位置、为什么有效、代价是什么、什么条件下失效」。
3. **不重复 ecosystem。** 分类计数、下载/星标、作者结构归 `ecosystem/`;这里只引用并使用带日期的口径,不自行重算。
4. **样本要回读。** `[CAT]` 的样本至少回读一条 catalog 描述原文;首选样本要求能说明其接缝位置(自述 `ctx.*` / seam / preset / bundle 即可,不必读源码)。

## 当前基线与数据边界

| 项 | 值 | 时效 |
|---|---|---|
| 名单基线 | `main@efe602e7b`(2026-10-31,0005) | 当前 |
| DSH 运行时 | `@deepseek-ai/dsh@0.2.1-rc.3`,安装内 306 个 `@deepseek-ai/*` 包 | 本机 checkout |
| 能力披露 | `data/capabilities.json`,扫描于 2026-09-24(`dsh-trust-check@0.1.13`) | 旧扫描,非新采 |
| 下载/星标 | 未重采;最后完整下载采样 2026-09-12,星标 2026-09-30 | 只作历史锚点 |

DSH 包的事实来自本机安装目录(`dsh --version` 与各包 README),不是上游源码 checkout;包版本变化时,`[DSH]` 条目需复核。

## 维护规则(增量,不改骨架)

- **新增一个样本**:过门 → 建卡(照抄同类 `card`/`sample` 的 frontmatter 与骨架,含借用节)→ catalog 补一行 → 域 README **只在「本域最佳取法变了」时**加一行。不要改本文件 / `horizon` / `BORROW`。
- **B 级不立卡、C 级只一行**:B 只出现在卡的对照行,C 只出现在失败模式表。
- **退役/被替代**:保留文件与编号,改 `status`,在 `takeaway` 里写明被谁替代;**不删、不改名**。
- **新域**:必须同时满足「新位置(seam/slot/layer)+ 多个过门样本 + 三域都装不下」;才加目录、`domain` 枚举、README 域表一行、BORROW 一行。**产品线是另册**,不适用本条。
- **同步上游**:只改受影响卡的 `updated` 与 `[DSH]` 断言 + 本文件「基线」行;`ecosystem/`、`_coverage/` 按原流程。
- **口径变化**:准入/分级只改 [`horizon.md`](./horizon.md)(单一源);三域 README 的副本是摘要,不必同步改。本文件的证据协议若变,在 `_change_log/` 记一笔。
- **验证**:`node _leverage/verify.mjs`(frontmatter/链接/锚点/编码)。**不做计数校验**。

## 待回答问题

完整清单(含给上游的)在 [BORROW §6](./BORROW.md#6-还没解决的事);这里只留三条层级问题:

- [ ] 四域的**反例样本**仍不足:E 级只有 2 条真判,其余失败模式多来自官方限制推演。
- [ ] RESHAPE 的「新队列更产品化」是真实趋势,还是「工作台类描述词」的放大?下一轮抽 30 条人工复核。
- [ ] `[DSH]` 证据来自本机安装目录;是否需要一份上游 `deepseek-harness` 源码 checkout 做逐行核验?
