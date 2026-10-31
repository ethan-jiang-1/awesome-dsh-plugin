# 杠杆层 · 四个影响面领域(总章)

> **这是什么**:围绕「DSH 里影响面大、强力扩充了 DSH 插件的机制」的深读层。目录前缀 `lever-` 是**第二轴**——`ecosystem/` 回答「有什么」,这里回答「改变了什么、改到多深、代价是什么、什么时候会坏」。
> **状态**:骨架立成(2026-10-31)。四个域各有 1 张旗舰卡;卡片与数字随上游同步增量更新,本文件只做宪章与索引,不随内容膨胀。

## 为什么单独一层

DSH 的扩展面是有限的、可枚举的:seam(fs/shell/sandbox/llm/subagent/workflow…)、slot(sidebar/conversation/settings…)、layer(profile/bundle/patch)、policy(observation/checkpoint/permission)、preset、protocol。**插件的影响面,取决于它占的是哪一类位置,而不是它提供了多少个工具。** 所以评估应该问「它占了什么位置」,而不是「它属于哪一类」——前者是可比的,后者不可比。

现有 `ecosystem/` 的 23 类是收录容器(注册表货架),与此轴正交,不合并、不替换。

## 命名:前缀 `lever-` + 一句标语

`lever-`(杠杆点)是这一层的共同前缀:一个插件**占了哪个位置,就能撬动多大一片**。它和 `ecosystem/` 的「类目」正交——类目回答「是什么」,杠杆回答「改了多大、多深、留了什么代价」。四个域并列,没有先后,所以**不加数字**;阅读顺序由下表顺序固定。

| 目录 | 标语 | 见到它先问 |
|---|---|---|
| [lever-reshape-product](./lever-reshape-product/README.md) | *What product can DSH become without forking it?*<br>不改上游,DSH 能被组装成什么产品 | 产品栈是哪几层?哪些是配置,哪些必须 fork? |
| [lever-cross-boundary](./lever-cross-boundary/README.md) | *Which boundary does collaboration cross, and what does each crossing cost?*<br>协作跨到哪个边界,每跨一界多付什么 | 共享状态归谁?冲突谁裁决?崩溃后谁收敛? |
| [lever-prove-output](./lever-prove-output/README.md) | *Where is the gate that turns "looks done" into "proven"?*<br>门禁装在哪一环,产物凭什么算完成 | 门禁在哪一环?证据能否重放?产物是否原子? |
| [lever-draw-limit](./lever-draw-limit/README.md) | *Who can touch what, who enforces it, what evidence remains?*<br>谁能碰什么,由谁强制,留下什么证据 | 信任谁?边界由谁强制?留下了什么证据? |

**卡片编号**:`<域>/NN-<slug>.md`。序号只在一个域内表示「先立骨、后加样本」的写作顺序,不表示优先级,也不跨域比较。题目变了就新开号,旧号改状态 `superseded` 并指向新号。

**为什么不用字母编号代号**:`L1–L4` 会让读者以为四域有强弱或先后,而它们实际是四种并列提问;`lift/link/lock/limit` 是为凑首字母造的近义词,彼此冗余。现在的后缀直接说动作,不需要额外解释。

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

## 四域的第一刀:各一张旗舰卡

| 卡 | 命题(本层最想验证的一句话) | 供给(条目,多标) | 新队列漂移 | 首选样本 |
|---|---|---|---|---|
| [01 · 产品栈](./lever-reshape-product/01-product-stack.md) | 产品化的单位不是插件,是 profile | 3104 (39.2%) | **+9.8pp**(最大) | `AKS1st/dock`、`hyperion2144/dsh-desktop-tauriapp`、`GDWhisper/dsh-web-startup-auth`、`All3nCN/dsh-better-sidebar-N23` |
| [01 · 拓扑谱](./lever-cross-boundary/01-collab-topology.md) | 协作是状态问题,不是 spawn 问题 | 1865 (23.5%) | +1.3pp | `Mlte0907/dsh-teams-x`、`zbzbhs/dsh-remote-agent`、`IKEASven69/dsh-takeover`、`ANetResearch/ANet#dsh-anet` |
| [01 · 质量链](./lever-prove-output/01-quality-chain.md) | 质量是门禁位置,不是评审力度 | 2888 (36.4%) | −0.7pp | `030611/qiushi-dsh-evidence-audit`、`4444wjt/dsh-plugin-veriscope`、`263311487-ux/dsh-verify`、`1687210989/agent-clinic` |
| [01 · 信任三层](./lever-draw-limit/01-trust-layers.md) | 安全是从安装到动作的监管链 | 2798 (35.3%) | +0.9pp | `PerryLink/dsh-defend`、`IamNewHands/dsh-approval-gate`、`BotonJ/dsh-plugin-sentinel`、`DevilSpiderX/dsh-workspace-only-plugin` |

数字口径见 [`census.py`](./census.py) 与下文「证据协议」;漂移为「新队列(2026-09-12 起首录 4418 条)相对存量」的百分点差,**是供给构成差异,不是需求趋势**。

## 研究方法:先过门,再分级

**不是抓到一个插件就琢磨。** 7924 条里过了准入门的是 **51 条(0.6%)**,对象不随名单膨胀。

| 组 | 条件(四选一 / 三选一) | 谁判 |
|---|---|---|
| 影响力 | **A** 目录内被按名引用 ≥3 次 · **B** 自述替换/接管官方对象 · **C** 自述具名接缝 · **F** 全库同类机制 ≤3 条 | A/B/C 机器,**F 须附检索式** |
| 深度 | **D** 披露 ≥2 个高杠杆能力(空披露也算) · **E** 明指不可共存 / 同一接缝取反 · **G** 机制已核且有具名失效条件 | D 机器,**E/G 只能人工** |

**缺一不立卡**。过门之后分级:**S** 定义型(后来者的模板)· **A** 代表型(当前优解)· **B** 对照型(**不立卡**)· **C** 反例型(失败模式表一行)。

每条进入卡片的样本必须写齐六项:代表什么 / 为什么选它(过门的具体值)/ **影响力多大(给数、给检索式或给官方原文)** / 主要特点 / 代价与失效条件 / 证据级别。缺一项退回。

完整规则、门槛参数、四域专项条件、现役 S/A 清单与已知缺口 → [`horizon.md`](./horizon.md)。

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
4. **样本要回读。** `[CAT]` 的样本至少回读一条 catalog 描述原文;旗舰卡的首选样本要求能说明其接缝位置(自述 `ctx.*` / seam / preset / bundle 即可,不必读源码)。

## 当前基线与数据边界

| 项 | 值 | 时效 |
|---|---|---|
| 名单基线 | 7924 条,`main@efe602e7b`(2026-10-31,0005) | 当前 |
| DSH 运行时 | `@deepseek-ai/dsh@0.2.1-rc.3`,安装内 306 个 `@deepseek-ai/*` 包 | 本机 checkout |
| 能力披露 | `data/capabilities.json`,3821 行,扫描于 2026-09-24(`dsh-trust-check@0.1.13`);URL join 当前名单 **3766/7924 (47.5%)** | 旧扫描,非新采 |
| 下载/星标 | 未重采;最后完整下载采样 2026-09-12,星标 2026-09-30 | 只作历史锚点 |

DSH 包的事实来自本机安装目录(`dsh --version` 与各包 README),不是上游源码 checkout;包版本变化时,`[DSH]` 条目需复核。

## 维护规则(增量,不改本文件)

- **新增一张卡**:按 `<域>/<NN>-<slug>.md` 建文件 → 在域 `README.md` 的索引行加一行 → 需要新样本/新数字时跑 `python3 _digested/leverage/census.py`。
- **收窄/拆分域**:域 `README.md` 自己有准入标准;标准变了就改域 README,不动本文件。
- **同步上游后**:只复核卡片页头的 `基线` 与 `[DSH]` 包版本;`ecosystem/` 与 `_coverage/` 各自按原流程更新。
- **口径变化**:只有本文件的「证据协议」或「前缀图例」变化时才改本文件,并在 `_change_log/` 记一笔。
- **验证**:`node _digested/verify.mjs`(链接/锚点/编码)。

## 待回答问题

- [ ] 四域是否有足够的**反例样本**?目前每张卡的首选样本偏向「做对了的」,`[OBS]` 的失效条件有待真实事故/缺陷样本支撑。
- [ ] `lever-reshape-product` 的 +9.8pp 漂移是「真产品化」还是「工作台类描述词」的正则放大?下一轮抽 30 条人工复核。
- [ ] `[DSH]` 证据目前只有本机安装目录,是否需要一份上游 `deepseek-harness` 源码 checkout 做逐行核验?
