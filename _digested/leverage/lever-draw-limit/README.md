---
title: "lever-draw-limit：安全监管链"
domain: draw-limit
kind: charter
positioning: "本域宪章：信任三层、强制点与失效方向、10 个样本坐标与 21 行借法一览。"
takeaway: "21 行借法一览（问题→抄哪条）+ 三层监管链 + 名字会骗人的三个坑。"
read_when: "要做安全/权限/审批/供应链；或评审一个安全插件。"
status: observed
updated: 2026-10-31
budget: 320
---
# lever-draw-limit · 谁能碰什么，由谁强制，留下什么证据

> **标语**:*Who can touch what, who enforces it, what evidence remains?* —— 安全是从安装到动作的监管链，最弱的一环决定整体。
> **状态**:`observed`(机制已核) · **基线**:DSH `0.2.1-rc.3` · 名单 @ `efe602e7b`
> **作业区**:**本目录自足、可独立开工**。只读共享件,不写共享件;不引用其他域的结论,不等待其他域的进度。四域并行契约见 [`../README.md`](../README.md#三域并行作业契约)。
> **借阅入口**:想抄 → [借法一览](#借法一览八张卡各能抄走什么) · 想选型 → [样本坐标](#样本坐标要精确挖掘时去哪里) · 想评审 → [选择要求](#选择要求) · 想回源 → [名字坑](#三个名字会骗人的坑重挖前必读) · 跨域 → [BORROW](../BORROW.md)
> **规则源**:准入/分级以 [`horizon`](../horizon.md) 为准;本域的准入副本是摘要。
> **全量卡片**:本表是精选;全部文件(kind/定位/能拿走什么/何时读)见 [`catalog`](../catalog.md)。

## 这个域问什么

“安全”在插件生态里是三个不同的问题，混在一起谈就会得出错误结论：

| 问题 | 归属 | 谁能回答 |
|---|---|---|
| 这个插件**会碰什么** | 披露 | `capabilities.json` 静态扫描 |
| 这个插件**被允许碰什么** | 策略 | 沙箱模式、审批策略、Remote access |
| 这个插件**真的碰不到什么** | 强制 | 执行环境 |
| 它**是否安全** | 判决 | **没有人能自动回答** |

**判断标准**：任何安全结论，先问它在哪一层、有没有强制点、留下的证据能否被别人复核。

## 收录 / 不收录

收录：

- 改**安装面**的：安装前静态审计、供应链校验、构建脚本批准、版本豁免
- 改**运行面**的：沙箱策略、审批策略与预设、工具级守卫、降权运行
- 改**数据面**的：凭据存取、脱敏、注入防护、网络暴露面、远端访问控制

不收录：

- 只记录不拦截的遥测 → 除非它同时构成证据链（那时归 `lever-prove-output`）
- 纯密码管理器式工具（存密码给 agent 用）→ 只有当它改变了**授权边界**才收
- 泛泛的“安全技能包”（SKILL.md 里的检查清单）→ 属杠杆阶梯 2 级，仅作旁证

## 准入(本域自带副本,不依赖任何其他文档)

**不是抓到一个就琢磨。** 研究对象不随名单膨胀:**卡片数不随收录量涨,只随「机制被验证」涨**。

| 组 | 证据 | 怎么判 |
|---|---|---|
| 影响力 | **A** 被目录内其他条目按名提到 · **B** 自述替换/接管官方对象 · **C** 自述具名接缝 · **F** 全库同类机制少见 | A/B/C 回读原文;**F 人工判断,标 `[OBS]`,不计数** |
| 深度 | **D** 能力披露 · **E** 明指不可共存 / 同缝取反 · **G** 机制已核且有具名失效条件 | D 查 capabilities;**E/G 人工** |

**缺一不立卡。** 分级:**S** 定义型(后来者的模板)→ 单独卡片 · **A** 代表型(当前优解)→ 卡片「标杆」正例 · **B** 对照型 → **不立卡**,只作一行对照 · **C** 反例型 → 失败模式表一行。

每条进入卡片的样本必须写齐六项:**代表什么典型 / 为什么选它(过的哪几条证据)/ 影响力证据(被谁提到、替换了哪个官方对象、或官方原文;不要求计数)/ 主要特点(机制层)/ 代价与失效条件(具名)/ 证据级别**。缺一项退回。

### 本域专项加分项

- **强制点可命名**:它在哪里拒绝?`tools/pre-execute`、`agent/pre-step`、沙箱后端、HTTP 路由、还是安装流程?**没有强制点的只能当旁证,不许立卡。**
- **失效方向明确**:fail-closed / fail-open / 转人工,三者必须点名。
- **可借鉴性**:卡片必须回答「**别人能搬走什么**」——一段可照抄的模板、一张验收清单、或一条踩坑后的具体改法。**只夸不取 = 不合格。**

## 这个域是怎么读的(给读者)

**本域不是插件导购。** 每张卡 9–10 节,结构固定,读的时候按用途挑:

| 你想干什么 | 读哪几节 | 为什么 |
|---|---|---|
| 判断一个安全插件靠不靠谱 | §7 失败模式 + §8 评估清单 | 失效率与失效方向,不会被功能列表骗 |
| **自己做一个控制点** | 每卡 §9「能搬走的东西」+ [09 §9 移植清单](./09-control-budget.md) | 八张卡的 §9 合起来是一套可执行的施工图 |
| 理解为什么生态长成这样 | §1 命题 + §2 杠杆点 | 缝的位置决定一切,这是本域的底层解释 |
| 挑一个装上 | §5 标杆(影响力数字)+ §7 | 影响力靠安装量与迭代密度,**不靠互相引用** |
| 给别人解释这套思路 | [09 控制预算](./09-control-budget.md) | 一张卡讲完「防灾难而不复杂」的全部结论 |

### 三分钟版:如果只读三段

1. **[09 §9 决定三「撤掉它会发生什么」](./09-control-budget.md)** —— 默认值就是策略。本域所有事故都能归到这一格填错。
2. **[04 §9.3「沙箱让位必须过五道闸」](./04-guard-vs-pump.md)** —— 沙箱是路径白名单,**不提供原子性**;这条推翻了大多数「交给沙箱就好」的设计。
3. **[06 §9.4「不要做被替代的那个」](./06-injection-seam.md)** —— 能力更宽的实现被更窄的实现淘汰,因为用户要的是**不必再想这件事**。

### 本域最终结论(可证伪)

> **防灾难的最小充分集是三件事**:一个不可绕过的沙箱、一处针对不可逆动作的确定性否决、一个失败即拒绝的默认方向。
> 其余一切——规则语言、第二模型、额度、审计、网关、回滚——都是**在某一项预算上做优化**,不能替代上面三样。
>
> 推论:**没有一个样本是靠「第 4 样」防住灾难的**;七个互不引用的实现独立收敛到同一套词汇(`allow / ask / deny`、默认拒绝、单点不可推翻、判不了就拒绝),这是本域最强的证据。

### 借法一览:八张卡各能抄走什么

本域的产出不是「这些插件不错」,而是下面这张表。**每一条都对应某张卡里的模板、清单或踩坑记录。**

| 你要解决的问题 | 抄哪条 | 出处 |
|---|---|---|
| 我的插件到底该不该做成「安全强制」? | 四问判定尺(不可逆?有词汇?能点名强制点?撤掉会变松吗?) | [01 §9.1](./01-trust-layers.md) |
| 审批管道怎么分层才不乱? | 八层模板(硬拒 → 不可逆 → 危险词 → 自改 → 白名单 → 越界 → 判定器 → 学习),**顺序即策略** | [02 §9.1](./02-approval-budget.md) |
| 「问过 N 次就别问了」怎么才安全? | 额度折算四前提(键是三元组、只对中立类、带指纹、不得越过硬拒层) | [02 §9.2](./02-approval-budget.md) |
| 怎么防止规则被文案改动绕过? | 三条验收测试:改说明文案,命中数不得变化 | [02 §9.3](./02-approval-budget.md) |
| 我要接一个模型做判定,怎么写才不出洞? | 五条硬约束 + 3×2 决策矩阵(只接受三格合法组合) | [03 §9.1–9.2](./03-second-model.md) |
| **我的裁决协议为什么会把「解析失败」变成「放行」?** | 禁用整数索引枚举;辅助字段解析失败不得改变主裁决方向 | [03 §3.4](./03-second-model.md) |
| 同步守卫里能放什么? | 四条铁律:只做纯函数判断、三个「判不了」各有归宿、沙箱让位五道闸、反馈落在本次调用 | [04 §9](./04-guard-vs-pump.md) |
| 什么时候可以把判断交给沙箱? | 五道闸;**沙箱是路径白名单,不提供原子性** | [04 §9.3](./04-guard-vs-pump.md) |
| 环境没给我强制点,我要自己架一道门 | 四步定位法(谁在发起)+ 出口门三规则(看地址不看名字 / 不许静默回退 / 链式前自问判定是否还成立) | [05 §9](./05-network-gate.md) |
| 「一键放行」按钮怎么写才不危险? | 写生效位置(索引 0)+ 最小维度 + 写后复验 + 拒绝清单 | [05 §9.3](./05-network-gate.md) |
| 我该把防线挂在哪条缝? | 接缝选型表(文本进模型 / 动作要拦 / 绝不能被推翻 / 问人) | [06 §9.1](./06-injection-seam.md) |
| 检测类工具怎么证明自己有用? | 基准集进测试 + 报告不含原文 + 自陈不全 | [06 §9.3](./06-injection-seam.md) |
| **我的功能更强,为什么没人用?** | 范围 × 默认值 × 装得上:用户要的是「不必再想这件事」 | [06 §9.4](./06-injection-seam.md) |
| 我要在沙箱之外再围一道 | 四条规则(覆盖所有模式 / 默认拒绝含超时 / 敏感路径永远问 / **重复请求不许去重跳过**) | [07 §9.1](./07-beyond-sandbox.md) |
| 我要自动批准某类操作 | 放绿灯五匹配(调用 + agent + 工具 + 原因前缀 + 目标与模式),且**只放行能看清的那一种** | [07 §9.2](./07-beyond-sandbox.md) |
| 状态该存哪?坏了怎么办? | 三处存储决策表;**损坏时拒绝加载,绝不清空** | [07 §9.4](./07-beyond-sandbox.md) |
| 我怎么做装前审计? | 组合形状四规则(凭据+外发 / 解码+执行 / 子进程+外发 / 安装即执行)+ 绝对阈值 | [08 §9.1–9.2](./08-install-face.md) |
| 升级把环境搞坏了怎么办? | 五步顺序:预检 → **建退路** → 装 → 版本校验 → 自动回滚;自动禁用只认可核证据 | [08 §9.4–9.5](./08-install-face.md) |
| 我的「检测坏了」的工具误报太多 | 判据选择法:问「它对哪种失效形态免疫」(目录空 → 237 误报;闭包可解析 → 0) | [08 §9.6](./08-install-face.md) |
| 我要从零做一个安全控制点 | 八个决定(理由 → 缝 → 默认值 → 枚举表示 → 动作表 → 状态 → 文本 → 基准与边界表) | [09 §9](./09-control-budget.md) |

**最短路径**:如果你只做一件事,做 [09 §9 决定三「撤掉它会发生什么」](./09-control-budget.md)——把每个依赖缺席时的默认值逐格填上,并让「解析不了」落到拒绝而不是落到第 0 项。**本域七张卡里的真实事故,一大半死在这一点上。**

## 样本坐标:要精确挖掘时去哪里

**每一行都可以直接 `git clone` 后回读。** 版本是 2026-10-31 实测的 `package.json` / npm `dist-tags.latest`,不是写作时的印象值;重挖时若版本已前进,以卡片里引用的机制描述为准,必要时用 git 历史落到对应 tag。

| 卡片 | 仓库(GitHub) | npm 包名 | 版本(2026-10-31) | 克隆命令 |
|---|---|---|---|---|
| [02](./02-approval-budget.md) | `IamNewHands/dsh-approval-gate` | `dsh-approval-gate` | **0.9.14**(仓库)/ npm 上 `latest` 为 **0.5.0**(另有人持有该名,见下) | `git clone https://github.com/IamNewHands/dsh-approval-gate` |
| [03](./03-second-model.md) | `PerryLink/dsh-auto-review` | `dsh-auto-review` | **0.15.0** | `git clone https://github.com/PerryLink/dsh-auto-review` |
| [04](./04-guard-vs-pump.md) | `JayYuen666/dsh-danger-guard` | `@jayyuen66/dsh-danger-guard` | **0.1.10** | `git clone https://github.com/JayYuen666/dsh-danger-guard` |
| [05](./05-network-gate.md) | `PerryLink/dsh-permission-rules` | `dsh-permission-rules` | **0.7.20** | `git clone https://github.com/PerryLink/dsh-permission-rules` |
| [06](./06-injection-seam.md) | `PerryLink/dsh-defend` | `dsh-defend` | **0.3.25** | `git clone https://github.com/PerryLink/dsh-defend` |
| [07](./07-beyond-sandbox.md) | `DevilSpiderX/dsh-workspace-only-plugin` | **未发布**(仓库 `0.2.6`) | 0.2.6 | `git clone https://github.com/DevilSpiderX/dsh-workspace-only-plugin` |
| [07](./07-beyond-sandbox.md) | `Fleey/dsh-workspace-folders` | **未发布**(仓库 `0.1.0`) | 0.1.0 | `git clone https://github.com/Fleey/dsh-workspace-folders` |
| [08](./08-install-face.md) | `Noob-stupid/dsh-plugin-gating-hub` | `@noob-stupid/dsh-plugin-console` | **0.5.98** | `git clone https://github.com/Noob-stupid/dsh-plugin-gating-hub` |
| [08](./08-install-face.md) | `BotonJ/dsh-plugin-sentinel` | ⚠️ **同名不同人**(见下) | 仓库 `0.1.0` | `git clone https://github.com/BotonJ/dsh-plugin-sentinel` |
| [03](./03-second-model.md) | `PerryLink/dsh-auto-mode` 之外:`NanmiCoder/dsh-auto-mode`(已归档) | `@nanmicoder/dsh-auto-mode` | **0.2.0** | `git clone https://github.com/NanmiCoder/dsh-auto-mode` |
| [01](./01-trust-layers.md) / [05](./05-network-gate.md) | `0QwQ0/dsh-ui-auth` | `dsh-ui-auth` | **0.7.1** | `git clone https://github.com/0QwQ0/dsh-ui-auth` |

### 三个「名字会骗人」的坑(重挖前必读)

| 坑 | 事实 | 后果 |
|---|---|---|
| **`dsh-approval-gate` 有两个** | npm 上 `dsh-approval-gate` 的 `repository` 指向 **`moon09300731/dsh-approval-gate`**,`latest` = `0.5.0`;**本卡研究的是 `IamNewHands/dsh-approval-gate`(0.9.14)**,它与 npm 同名包**不是同一个仓库** | 直接 `npm i dsh-approval-gate` 装到的是**另一个实现**。要复现本卡结论,必须从 GitHub 克隆并按仓库的安装说明装 |
| **`dsh-plugin-sentinel` 同名不同人** | npm 上该名属于 **`dushaobindoudou`**(`github.com/dushaobindoudou/dsh-plugin`,目录 `packages/dsh-plugin-sentinel`),`latest` = `0.0.1`,自述「name reserved; first release in development」;**本卡研究的是 `BotonJ/dsh-plugin-sentinel`**(仓库 0.1.0,源自 `awesome-dsh-plugin#466`) | 同理:从 npm 装到的不是本卡的样本 |
| **两个 workspace 类样本没有 npm 包** | `dsh-workspace-only-plugin` / `dsh-workspace-folders` 在 registry 里**查无此包**(`versions` 为空) | 「月下载」一栏对它们只能标「无」,不能估。**但它们的「无记录」不代表影响小**——本卡对它们的准入靠 E(同缝反向)与 G(机制已核),不靠影响力 |

### 重挖时的四条提醒

1. **版本会漂移,机制不会**。卡片里的数字(阈值 0.45、`maxDenies` 2、120 s 超时、15,638 下载)都是 2026-10-31 的快照;若 HEAD 已前进,用 `git log` 找卡片引用时的 tag/commit 再读。**引用结论时带日期,不带日期就别引用。**
2. **两个已停更的样本不要当现行最佳实践**:`NanmiCoder/dsh-auto-mode`(README 首行:「Maintenance ended on 2026-09-29…正在归档」,因为官方已内置 Auto review)、`PerryLink/dsh-defend`(2026-10-05 冻结,自述推荐 `cc-safety-net`)。**它们是历史形态,不是当前优解。**
3. **npm 包名 ≠ 仓库名**,本域有两处踩坑(见上表),还有一处 scoped 包下载数不可查。**装之前先核对 `package.json` 的 `repository` 字段。**
4. **卡片引用的官方包在本机**:`/Users/bowhead/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai/dsh-<包名>/README.zh.md`(DSH `0.2.1-rc.3`)。官方语义(`tools/pre-execute` 流水线、`dsh-user-approval` 的 `next()` 契约、沙箱词汇边界)以**本地安装包**为准,不以网页文档为准——网页版可能对应别的版本。

### 影响力数字的取法(可复现)

```bash
# 月下载(区间 2026-09-30 → 2026-10-29)
curl -s "https://api.npmjs.org/downloads/point/last-month/<包名>"

# scoped 包必须用 %2F 而非 /,否则一定 404
curl -s "https://api.npmjs.org/downloads/point/last-month/@jayyuen66%2Fdsh-danger-guard"
```

**两条已知限制**:

1. **scoped 包的下载数查询会返回 `{"error":"package ... not found"}`**,即使包确实存在且能装(`@jayyuen66/dsh-danger-guard` 实测如此,registry 元数据正常、tarball 可下)。因此 04 卡写「不可得,不估」,**不是「下载量为 0」**。
2. 星标取 `_digested/ecosystem/_snapshots/stars-2026-09-30.json` 的 `['entries']`;快照下载取 `snap-2026-09-12.json`。**这两份快照早于冻结基线(2026-10-31),只作历史锚点。**

### 本域明确不收

- 纯披露类(只统计、只报告、只打分)→ 披露 ≠ 策略 ≠ 强制 ≠ 判决
- 泛泛的安全检查清单技能包 → 2 级,无强制点
- 密码保管类,除非它改变了授权边界
- 声称保护边界、却自身读凭据/联网/动态执行而不自陈的 → 一票否决

### 本域研究对象(主读,单一归属)

| 级 | 样本 | 过了哪些门 | 影响力证据(可复核) | 一句话特点 | 卡片 |
|---|---|---|---|---|---|
| **S** | 官方 `dsh-sandbox-policy` | G | 唯一有策略词汇的维度;原文「网络和进程策略不在其词汇中」 | 权限状态是**日志事实**,不是实时开关 | [01](./01-trust-layers.md) |
| **S** | 官方 `dsh-experimental-auto-review` | G | 唯一的「模型判模型」;默认关闭、明说会误放行、留有 `run_code` 绕过通道 | 智能审批是**体验优化**,不是安全边界 | [01](./01-trust-layers.md) / [03](./03-second-model.md) |
| **A** | `PerryLink/dsh-defend` | C + D(零披露) | 月下载 4,511;已冻结,自述被 `cc-safety-net`(周 13,087)替代 | 想防注入必须挂 `agent/pre-step`,挂 tools 层永远防不了「模型已被说服」 | [06](./06-injection-seam.md) |
| **A** | `IamNewHands/dsh-approval-gate` | D + **E** | ⚠️ npm 同名包属 `moon09300731`(月下载 3,709 是它的);IamNewHands 版未发布,无下载数。E:阈值已满 + 判定器不可用 → **fail-open** | 显式 fail-open 的诚实样本;核心是「审批预算」 | [02](./02-approval-budget.md) |
| **A** | `PerryLink/dsh-auto-review` | C + D + E(与官方版同缝) | 月下载 7,216;星标 218 | 第二模型只是**可缺席的应答者**,不是授权来源 | [03](./03-second-model.md) |
| **A** | `JayYuen666/dsh-danger-guard` | C + E(同步守卫) | 注册表 16 个版本 / 1 个月;月下载不可得(**不估**) | 同步谓词只能回答一次,复杂策略必须搬到别的缝 | [04](./04-guard-vs-pump.md) |
| **A** | `PerryLink/dsh-permission-rules` | C + D + E | 月下载 6,420;本族最高 | 网络不在沙箱词汇里,只能在沙箱外再造一道进程出口门 | [05](./05-network-gate.md) |
| **A** | `Noob-stupid/dsh-plugin-gating-hub` | B + C + D | 月下载 **15,638**;本域最高 | 安装面的防灾难 = 可逆性,不是预测 | [08](./08-install-face.md) |
| **B** | `DevilSpiderX/dsh-workspace-only-plugin` + `Fleey/dsh-workspace-folders` | **E**(同缝反向)+ C + G | 星标/下载快照与 npm 均无记录(新入库);按名引用几乎为零 | 同一缺口的两种利用:收紧 vs 放松 | [07](./07-beyond-sandbox.md) |
| **B** | `BotonJ/dsh-plugin-sentinel` | C + G | ⚠️ npm 同名包属 `dushaobindoudou`(月下载 423 是它的);`BotonJ` 版仓库 0.1.0,**未发布** | 安装前看**组合形状**,不看单个危险 API | [08](./08-install-face.md) |

> 七张新卡(02–08)+ 一张横切卡(09)覆盖 **10 个样本**。**月下载口径**:`curl -s api.npmjs.org/downloads/point/last-month/<包名>`,区间 2026-09-30→2026-10-29,包名以各仓 `package.json` 为准(`dsh-plugin-gating-hub` 的包名是 `@noob-stupid/dsh-plugin-console`)。

**准入自检(2026-10-31)**：本域样本按名互引基本为 0 或仅命中自身，反而竞品 `cc-safety-net` 被第三方条目提到。结论：**本域的「影响力」只能靠安装量与迭代密度论证，不能靠目录内互引**；A 门在本域不成立，准入主要靠 **C / D / E / G**。这本身是一条域级发现（见 [09](./09-control-budget.md) §9）。

**借用但非主读**(只可一句引用,不深读、不立卡):`GDWhisper/dsh-web-startup-auth`(主读在 `lever-reshape-product`,本域只当 HTTP 网关旁证)、`dsh-fs-observation-policy`(主读在 `lever-prove-output`)。

## 选择要求

1. **强制点可命名**：它在哪里拒绝？`tools/pre-execute`、`agent/pre-step`、沙箱后端、HTTP 路由、还是安装流程？没有强制点的，只能算披露。
2. **失效方向明确**：出错时是 fail-closed（拒绝）、fail-open（放行）、还是转人工？三者必须点名，不许含糊。
3. **不自破边界**：一个声称保护边界的插件，自己是否用了它要防的那些能力？（这条在本域尤其重要，见 §5）

## 领域骨架：三层监管链

| 层 | 问题 | 原生强制点 | 代表卡 |
|---|---|---|---|
| 安装面 | 谁能被装进来、装进来时跑了什么 | `plugin_manager` 的版本检查、构建脚本批准 | [01-trust-layers](./01-trust-layers.md) |
| 运行面 | agent 的动作被什么挡住 | 沙箱模式（**仅文件**）、审批策略 | 同上 |
| 数据面 | 密钥、网络、跨机访问的边界 | `ctx.credentials`、Remote access policy | 同上 |

**核心洞察(已由 02–09 验证)**:三层里最弱的是**运行面的网络与进程**——官方明说沙箱模式只覆盖文件操作。生态的两种反应都已经成形:在**数据面**造网关(01 / 05),或在**工具层**再造一道门(04 / 07)。**两者都只能在「自己控制的那一段」上生效**,谁都没有覆盖宿主自身发起的网络。而「防灾难而不把策略写复杂」的答案在 [09](./09-control-budget.md):最小充分集是**沙箱 + 一处不可推翻的否决 + 失败即拒绝的默认方向**,其余全部是某一项预算上的优化。

## 卡片索引

| 编号 | 标题 | 状态 | 一句话结论 | 能搬走什么 |
|---|---|---|---|---|
| [01](./01-trust-layers.md) | 信任三层：只有文件那一环是硬的 | `observed` | 安装面靠自觉，运行面只管文件，数据面靠生态自建；披露率 47.5% | 三层监管链的判定顺序 |
| [02](./02-approval-budget.md) | 审批预算：把「问几次」当成可耗尽的资源 | `observed` | 硬拒免费、围栏一次、确认有额度、判定器只是兜底；收紧匹配有价（提示 +21%） | **八层管道模板 + 额度折算四前提 + 三条验收测试** |
| [03](./03-second-model.md) | 第二模型：权威放在哪一侧 | `observed` | 模型只决定「要不要打扰人」，不决定「能不能执行」 | **五条硬约束 + 3×2 决策矩阵 + 六个真实漏洞与修法** |
| [04](./04-guard-vs-pump.md) | 守卫与泵：同步谓词只能回答一次 | `observed` | 不可推翻的位置只装得下最便宜的判断；判不了要换档，不许借档 | **同步守卫四铁律 + 沙箱让位五道闸 + 边界表模板** |
| [05](./05-network-gate.md) | 网络门：进程级出口闸门 | `observed` | 沙箱词汇里没有网络，只能在沙箱外再造一道门 | **四步定位法 + 出口门三规则 + 一键放行四件套** |
| [06](./06-injection-seam.md) | 缝的位置：挂在文本进模型之前 | `observed` | 能拦 ≠ 能解释 ≠ 能协商；被更窄但采用度高一个数量级的实现替代 | **接缝选型表 + 检测层怎么证明有效 + 为什么不选「更宽」** |
| [07](./07-beyond-sandbox.md) | 沙箱之外：同一个缺口的收紧与放松 | `observed` | 缺一块策略词汇，既让收紧变贵，也让放松极便宜 | **重新围栏四规则 + 放绿灯五匹配 + 状态存放决策表** |
| [08](./08-install-face.md) | 安装面：装前看形状，装后可回滚 | `observed` | 可逆性优于预测；只禁有确证证据的行，框架行永不禁用 | **组合形状四规则 + 五步自救顺序 + 判据选择法** |
| [09](./09-control-budget.md) | 控制预算：七个样本为什么收敛到三个动词 | `observed` | 防灾难的最小充分集是三件事；其余都是在某一项预算上做优化 | **从零搭控制点的八个决定（全域施工图）** |

## 边界契约(声明式,不依赖他域进度)

四域并行研究时,**归属是事先划定的,不是商量出来的**。本域遇到下列情形只写划给自己的那一半,另一半留给它的归属域;若那一边尚未产出,本域照写,不等待、不代笔。

| 情形 | 归属 | 本域只写到哪 |
|---|---|---|
| 证据链的**可重放性** | `lever-prove-output` | 只写「强制点留下了什么痕迹」 |
| 跨机**身份与配对流程** | `lever-cross-boundary` | 只写「鉴权与强制」这一半 |
| 分发通道、市场索引 | `lever-reshape-product` | 不写 |
| 权限档作为**产品默认值** | `lever-reshape-product` | 只写强制与失效方向 |
| 团队任务完成标准 | `lever-prove-output` | 不写 |

**契约的两条硬约束**:① 本域结论不得把其他域的结论当作前提;② 需要外部事实时写进本域卡片并自带 `[DSH]`/`[CAT]`,不写「见某域」。

## 本域基线(冻结)

> 快照 **2026-10-31** · 名单 @ `efe602e7b` · DSH `0.2.1-rc.3`。**本域只引用这份快照读到的事实,不维护统计口径。**

**本域另用一份「安装量」口径**(catalog 不含此数据,故单列):npm 月下载数,**区间 2026-09-30 → 2026-10-29**,取法 `curl -s api.npmjs.org/downloads/point/last-month/<包名>`,包名以各仓 `package.json` 的 `name` 为准。已入卡样本:`@noob-stupid/dsh-plugin-console` 15,638 · `dsh-auto-review` 7,216 · `dsh-permission-rules` 6,420 · `dsh-defend` 4,511 · `dsh-approval-gate` 3,709 · `dsh-plugin-sentinel` 423(**同名不同人**,见样本坐标表) · `@jayyuen66/dsh-danger-guard`(API 不返回,**不估**)。此口径只作历史锚点,与冻结的名单不是同一时间点,引用时必须带日期。

四域重叠是正常的:本域与 RESHAPE / CROSS / PROVE 都有样本交集。四域是**四个并列的提问**,不是互斥分类——独立性靠「编辑权 + 主读归属 + 不依赖他域结论」保证,不靠样本不重叠。

## 复核方式

**不设计数门。** 影响力看 npm 安装量、迭代密度与实时采样(带日期);「少见 / 唯一」是人工回读判断,标 `[OBS]`,不附命中数。

## 复核触发条件

- 沙箱模式扩展出网络/进程策略（这会直接改写本域主结论）
- 支持多工作区根（现为“每会话只有一个主要工作区根”）
- `plugin_manager` 的构建脚本批准从“不核实对话”变成有可验证授权
- Remote access 的 principal 种类或 `decide()` 时机变化

## 待答问题

- [ ] 生态里做「安装前扫描」的样本，有多少真的在**安装前**运行（能拿到 tarball），多少只是装后体检？**复核方式**：逐个回读 08 卡的 `sentinel` 与 `gating-hub`——前者是装前、后者偏装后；**不靠计数**。
- [ ] 网络出口完全无强制，是否意味着所有“防外传”插件都只能是启发式？
- [ ] 安全插件自身的能力披露（57% 用 shell、32% 联网）是必要成本还是设计懒？有没有“零能力”实现的可能？
