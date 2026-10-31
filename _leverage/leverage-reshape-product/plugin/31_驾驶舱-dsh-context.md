---
title: "驾驶舱 · dsh-context"
domain: reshape-product
kind: sample
positioning: "`bowenliang123/dsh-context`：把上下文、成本、编队做成可读可归因的五块面。"
takeaway: "读宿主投影（useProjection）而非 tokenMeter 服务；估算与实测并列；但头部占用率有未标注的四级回退，成本本地估算且价格来自第三方库。"
read_when: "要做用量/成本/上下文面板；或要避免面板数字与用户已知数字打架。"
status: observed
updated: 2026-10-31
---
# 驾驶舱 · dsh-context:给「智能体在扛什么」造一间驾驶舱

> **研究范围**：npm `dsh-context@0.78.2`，registry `gitHead` 与 tag `v0.78.2` → commit [`32982aa`](https://github.com/bowenliang123/dsh-context/commit/32982aa6aa2c70fbda6b81281de98a72ea625001) 同一 SHA（轻量 tag）。DSH 对照 `dsh-v0.2.1-rc.3`。源码、测试与 workflow 已读；未安装、构建、运行，也未下载 tarball 做字节比对。完整来源见[`09 源码复核`](./_证据/09_驾驶舱-dsh-context-源码复核.md)。
> **类**:`3` 驾驶舱 · **层**: 3(槽位)+ 4(提示词前后缀) · Apache-2.0 · ★ 3,909 / npm 264,177（2026-10-31 实时）
> **一句话**:它把"上下文"从一个**进度条**变成一间**可读、可追、可归因**的驾驶舱。
> **借鉴价值**:**① 数字应与用户已相信的宿主数字同源（但同源≠同精度：本插件占用率保留一位小数且有四级回退，可能显示 67.4% 而输入框环显示 67%）**,否则整套面板一次失信、永久失信;② **估算与真实并列**,而不是二选一;③ 一份**把"上游每个接缝"写成可执行断言清单**的兼容文档(`docs/compatibility.md`),这是本线最可直接抄的交付物。

> **证据成熟度**：投影读取、占用率回退/精度差、分类锚定、客户端成本与价格书刷新为固定 0.78.2 源码 `机制参考`；tarball 字节一致性、真实 UI 与账单对账未验证，无 `[RUN]`。
> **样本档案**
> **repo**:[`bowenliang123/dsh-context`](https://github.com/bowenliang123/dsh-context) · **npm**:`dsh-context` · **版本**:`0.78.2`
> **目录条目**:`data/plugins/bowenliang123__dsh-context.yml`(`usage`)
> **装法**:GUI Add plugin 搜 `dsh-context`;或 `dsh plugin --profile web add dsh-context`
> **已在本地挖掘**:本轮挖掘直接读 README 全文(237 行);上游投影口径由 `dsh-token-meter` 源码核对
> **再深挖去哪**:仓库 `docs/compatibility.md`(Rule/Limitation/Check/Procedure 四类)与 `docs/model-pricing-mapping.md`(**外链,本地未读**)

---

## 它想干什么 · 为什么值得借鉴

**意图。** 作者要让“智能体在扛什么”从输入框旁一个百分比，变成能追到每一行、每个子代理的驾驶舱——上下文、成本、编队分五块面（Insights 页、Context Tab、Fleet Tab、右栏面板、`/context` 弹窗）。它不调用 `ctx.tokenMeter` 服务，而是读会话 props 上的 `useProjection('tokenUsage' | 'contextPressure' | 'contextBreakdown')` 三份宿主投影；官方没有导出的公式/字段才镜像实现。它也不接管模型，唯一进模型的是 System Prompt 的 Prefix/Suffix。

**意义。** 它补的是“可解释性”的空缺：生态里不缺图表，缺的是敢写进界面的诚实——分类环在锚定后已按实测计费输入等比缩放；只有锚定前的估算分类才与 `projectedTokens` 不等，差额来自四字符一 token 启发式（CJK 与 JSON schema 被低估）。它读的是宿主投影而不是自算一套，但占用率镜像保留一位小数、且有四级回退，可能与输入框环的整数百分比差一格。更硬的一层是 `docs/compatibility.md` 把每个上游接缝写成 Rule/Limitation/Check/Procedure，连“已退役接缝不存在”都要断言。

**用户价值。** 装之前，用户看到上下文快满只能猜“是不是工具结果太多”；装之后，六色条指出工具结果占 62%、压缩保留区只剩一条缝，Trend 的柱子能跳到那一步的真实工具输出，Insights 按天看推理 41%、工具 schema 9% 与峰谷价。被“面板数字和输入框对不上”坑过的人最知道值。代价由作者背：镜像 6 处官方实现（占用率公式在内核包内无导出），上游一改就要重拟合；用户则要接受估算与账单本来不等。

**表达（界面与交互）。** 第一屏是一排卡片加一张柱状图，默认只给结论；想深究则悬停 → 钉住 → 展开 → DNA 逐层下钻，全量摊平在卡片内滚动而不刷屏。装完无构建、无重启，顶栏多一个 Context Tab、右栏多一个面板入口，不改原有布局，不要面板可在偏好里关。缺服务时“无服务 → 无能力”：不挂 pending fiber、不抛错；`tab.visible` 为假时不挂卡片、暂停订阅；`contextWindow − reservedOutput − headroomTokens ≤ 0` 时不画斜纹——这些不显示、不打扰、可回退的设计本身就是体验。

## 0. 一页速览(想抄的人只看这 20 行)

| 问题 | 它的答案 | 你能直接抄吗 |
|---|---|---|
| 数字从哪来 | **不调服务**:读会话 props 的 `useProjection` 三份宿主投影 `tokenUsage`/`contextPressure`/`contextBreakdown`；投影缺失字段时逐字段判空，形态不对按无数据处理 | ✅ 抄"投影读取 + 逐字段重证 + 镜像清单" |
| 分类数字与总量对不上怎么办 | 官方三分类先定段、messageTokens 按折叠五类比拆分；再按实测 prompt 总量**等比缩放**（anchoredParts），环上没有"不对齐"。只有锚定前的原始分类才与 `projectedTokens` 不等 | ⚠️ 两个口径要分开讲，别笼统说"绝不强行对齐" |
| 估算准不准 | 钉住视图里**并列** provider 上报的 Actual Prompt / Output / Cache | ✅ 直接抄交互 |
| 为什么可信 | 它自带 `docs/compatibility.md`:**规则 + 局限 + 检查方式 + 操作步骤**四类条目,每条挂证据路径 | ✅✅ **本卡最值得抄的东西** |
| 能点到多细 | 每个 token 元素能展开成**真实内容**(系统提示、每个工具的 JSON schema、消息、推理、工具输出),并标出**引入它的 step** | ✅ 但如果只做一层分类,别自称驾驶舱 |
| 失败时怎么办 | 每个能力都走**可选接缝**(`ctx.inject` 延迟注入),没有该服务就没有该能力:**不挂起、不抛错** | ✅ 抄"无服务→无能力"的写法,别抄"硬依赖" |
| 最贵的一课 | 它镜子了 6 处官方实现;**其中一处是内核包内部函数,官方没有导出** → 上游一改,它必须跟着改 | ⚠️ 镜子要付维护税,清单里写清"镜子了哪几行" |

---

## 1. 它在产品里的位置

| 七层 | 它的动作 | 证据 |
|---|---|---|
| 3 槽位 | 一次注册塞进**五个面**:一级侧栏页 `Context Insights`、会话内 Tab `Context`、会话内 Tab `Fleet`、右栏面板、`/context` 弹窗 | `[OBS]` README §五个面 |
| 3 槽位(细) | 官方槽 `conversation.*` 之外,它自己**在右栏占一个 tab**;`tab.visible` 为假时**不挂卡片、暂停订阅** | `[OBS]` compatibility §5 rule 15 |
| 4 身份 | 偏好卡 **System Prompt · Prefix / Suffix** 拼进**每个会话(含子代理)**系统提示首尾;只加不改 | `[OBS]` README §Settings |
| 5 默认值 | 面板入口四选一、Insights 默认 30 天、趋势粒度、diff 基线、自动 Overview 阈值 | `[OBS]` 同上 |

**为什么算"产品"而不是"监控工具"**:它把"信任模型"的动作成本压到**一次悬停**——`[OBS]` 用户在柱状图上悬停即预览那一步,Browser 同步联动。

---

## 2. 机制(可照抄的部分)

### 2.1 计量链路:谁算、算哪一段

| 数字 | 谁算 | 抄的时候注意 |
|---|---|---|
| 头部占用率 % | 优先读 `contextPressure`；缺失时四级回退 `projectedTokens → pressureTokens → derived → 折叠 current.total`；百分比镜像 `occupancyPercent`（一位小数），而宿主 `contextOccupancy()` 是整数 % | `[SRC-TARGET]` 回退链无来源标记，界面无法区分“官方投影”与“自推值”；精度差可造成 67.4% vs 67% |
| 六色条的各类占比 | **复用官方** `contextBreakdown`(`systemTokens` / `toolsTokens` / `messageTokens`)+ 自己补齐细类 | 官方只有三类;它拆到六类(系统提示 / 工具 schema / 用户消息 / 注入上下文 / 助手回复 / 工具结果) |
| 计费 token | **复用官方** `tokenUsage`(`uncachedInputTokens` / `outputTokens` / `cacheReadTokens` / `cacheWriteTokens`) | `[DSH]` 重试时 `llm/retry-started` 会结束替换域,**同一步的重试算另一次计费尝试** |
| 每类估算 | **镜像**官方 `estimate.ts`(`estimateSystemMessage`、`estimateContent` 的 reasoning / text / tool-call 三条分支) | `[OBS]` compatibility §4 逐行列出镜像点 |
| 文件 token | **镜像** `fileHandleText`:一个 `file` 块按**请求里的 handle 文本**计价,**永不按其字节数** | ✅ 这条最容易抄错,抄错会高估几十倍 |
| 压缩保留区(斜纹) | **镜像** `compaction-basic` 的两个默认值:`thresholdRatio` **0.8**、`headroomTokens` **65536** | ⚠️ 它明说"预设域让部署策略不可读",所以只能读**出厂默认**;`[OBS]` `contextWindow − reservedOutput − headroomTokens ≤ 0` 时后端直接拒绝,此时**不画斜纹** |
| 成本 | 价格来自第三方 `@opencode-ai/models`（devDependency；运行期是内置快照还是联网未核）；成本在客户端按 `cacheRead/cacheWrite/uncached/output` 四桶单价求和，DeepSeek 峰时 ×2，CNY 用固定 0.15 汇率 | ⚠️ 是本地估算，不是账单；未定价 route 从总和中跳过 |
| 首 token 时间 | **镜像** `assistantStreamFirstTokenTime` | 同上,镜子之一 |

**规则(可直接抄)**:凡是"用户已经见过的数字",**只允许一员出数**;自己补的那部分,必须能一句话说清"我补的是哪一段、从哪算起"。

### 2.2 为什么它敢显示"估算 + 真实"两列

`[OBS]` compatibility §4 的三条 Limitation 是全卡最硬的工程文字,原文逻辑如下:

| 局限 | 它怎么处理 |
|---|---|
| 没有任何受支持路由上报 thinking / answer / tool-call 三个桶(`llm-deepseek` 只映射 input/output/cache) | 三个切片按 token-meter 自己的块单价算,**provider 若给 `reasoningTokens` 则以它为准** |
| 分类之和 ≠ `projectedTokens` | **不强行对齐**;分类数字带 `≈` 前缀,总量另给 provider 精确值 |
| 峰谷按北京时间的周几判定,**不维护法定节假日日历**(明确决定) | 节假日工作日会**按峰时计价而平台按谷时计费**;tooltip 里直接写"周几/周末"规则 |

> **这就是"可解释性"的可执行定义**:不是给出更多数字,而是**每个数字都带上它的边界条件**。三行局限胜过三十个图表。

### 2.3 顺手把"报告完整性"做成机制

| 情形 | 它的做法 |
|---|---|
| 压缩前的 step | 从**被移除消息的归档**重建,并**在卡上标注"仅为近似"** |
| 旧历史 / 被裁剪的片段 | **明确披露**,不静默截断 |
| 某个工具的 schema 行 | 标来源芯片:`tool-*` 一方包 / `dsh-*` 能力包 / `mcp:<server>` / 具体插件名(从 `tools.register()` 活捉) |
| 技能注入 | 单独一类,原文理由:"一个偷偷加载的技能,它的上下文开销无法藏在注入或工具结果里" |
| 全量摊平(DNA 模式) | 卡片内滚动,不刷屏;每行带 `#12` 提示词位置 |

### 2.4 兼容性:本线**最值得抄的一份交付物**

`[OBS]` `docs/compatibility.md`(0.78.2，最后核验日 2026-10-30，基线为 rc.2 两条 tag；不是 rc.3 实测)的结构本身就是方法论:

```
支持集合 → 准入 → 折叠(fold) → 计量一致性 → 客户端面 → 投影缓存 → 打包 → 验证
```

四类条目,**每条都必须挂证据路径**(`src/...` 或 `dsh:` 前缀的上游包路径):

| 条目 | 含义 | 例子(原文摘) |
|---|---|---|
| **Rule** | 不变量,加粗即是结论 | "**Every capability rides an OPTIONAL seam**"——延迟 `ctx.inject`,用前复查面,注册加保护;**无服务 → 无能力:不挂 pending fiber、不抛异常** |
| **Limitation** | **已接受的缺口** | "节假日不维护日历(按决定上线)" |
| **Check** | 这条宣称**怎么被证明** | 接缝矩阵:按基线 tag 拉上游**真实源码**,把构建好的插件装进 tag 的真实注册表,**探测宿主与客户端接缝**、**断言已退役接缝不存在**(`settings.register`、`sessions.open(id)`) |
| **Procedure** | 任务怎么做 | "强制重折一个会话:`rm ~/.dsh/storages/session_projcache/sessions/<id>.json`" |

**它宣称的兼容范围与真实判定器一致**:

```jsonc
// package.json [OBS 读于 2026-10-31]
"engines": { "node": "^22.19.0 || >=24.0.0",
             "dsh": ">=0.2.0-rc.2 || >=0.2.1-rc.2" },     // 运行时地板
"dsh": { "compatibility": { "dshReleases": {               // 安装证据(逐版本枚举)
           "0.2.0-rc.2": "compatible", "0.2.1-rc.2": "compatible" } } }
```

`[DSH]` 上游确实按这两个字段分头判定:**`0.2.1-alpha.4` 起只看 `engines.dsh`**,`0.2.0` 线、带门禁的 `0.1.7` 与 `0.2.1` alpha.4 之前**只看 `@deepseek-ai/dsh*` peers**。所以:

> **抄这条**:两个声明**都要写**,因为它们各自是**不同宿主线上的唯一门禁**;而"我支持哪些"另有一份**逐版本枚举**给市场与用户看。

### 2.5 镜像税:它自己写出来的代价

`[OBS]` §4 rule 1 标题就是 **"Mirror, don't import"**,并附一张 6 行对照表(插件文件 ↔ 上游文件)。逐条代价:

| 镜子对象 | 上游一改会怎样 |
|---|---|
| `token-meter/src/estimate.ts` | 估算数字与宿主**悄悄分叉**;用户发现"装了这个插件,数字变了" |
| `llm/src/content.ts` `fileHandleText` | 文件成本整体算错 |
| `ui-conversation` 占用率公式 | 头部百分比与输入框的环**对不上**——本卡最怕的事 |
| `compaction-basic` 默认阈值 | 斜纹画错位置 |
| `assistant-stream` 首 token 锚 | TTFT 数字漂移 |

**它的对策**:每次支持线移动实现,就**重新拟合**;并用 §8 的**差分检查**(把插件算的数与宿主自己的投影在真实会话日志上逐一比等)来发现漂移。

---

## 3. 体验

### 3.1 四个真实问题,四条路径

| 用户问题 | 走法 | 看到 |
|---|---|---|
| 它怎么突然变笨了 | Context Tab → **Current Context** | 六色条里"工具结果"占 62%,压缩保留区只剩一条缝 |
| 这一轮到底发了什么 | Trend 某根柱 → **Step brief** 的 `In` | 跳到该条工具结果,原文一字不差 |
| 钱花哪了 | Insights → Token Stats + 7 日图 | 推理 41%、工具 schema 9%;按天看峰谷 |
| 哪个子代理卡住了 | **Fleet** | 网络图上那条边还在绿脉冲;点进去看实时上下文 |

### 3.2 首次使用

| 时刻 | 看到 | 设计 |
|---|---|---|
| 装 | `dsh plugin --profile web add dsh-context`,**无构建、无重启** | 门槛压到最低 |
| 打开会话 | 顶栏多一个 Context Tab,右栏多一个面板入口 | 不改原有布局;不要面板可在偏好里关 |
| 第一眼 | 一排卡片 + 一张柱状图 | **默认只给结论** |
| 想深究 | 悬停 → 钉住 → 展开 → DNA | 逐层下钻 |
| 用久了 | Insights 成了**个人账本** | 从工具变资产 |

### 3.3 模型看到的

**几乎为零**。`[OBS]` compatibility 明说客户端面全是人侧;唯一进模型的是 **Prefix/Suffix**。

> 取舍值得抄:**观察者不改变被观察者**。好处是测量无扰动;代价是**模型不会因为"上下文快满了"而主动收敛**。

---

## 4. 证据与边界

| 口径 | 值 / 说明 |
|---|---|
| ★ / npm | **3,909 / 264,177**（2026-10-31 实时） |
| 名单内被引 | **6** |
| 官方背书 | README 自述被 DSH 官方 **@tianyicui、@turtle1999** 推荐 |
| 下游联动 | `12_厚工作台` 在任务页 agent 节点、后台任务输出窗、会话头**三处**做"跳到该会话 Context 页",**装它才有、没装不显示**(能力探测) |
| 兼容 | `engines.dsh` 地板 `0.2.0-rc.2`;`dshReleases` 逐版本枚举 `0.2.0-rc.2` / `0.2.1-rc.2` |
| **已知偏差** | ① 分类数字是估算,**与计费总量不等是设计**;② CJK / JSON schema 被低估(四字符一 token);③ 节假日按工作日计价;④ 成本按列表价,第三方网关可能差很远;⑤ 镜像 6 处官方实现,上游移动即需重拟合 |


---

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 面板数字必须与宿主 UI 一致 | 优先读取宿主公开投影/字段，不复制总量算法；镜像仅限未导出的公式，并登记镜像清单与上游版本。 | `[SRC-TARGET]` 0.78.2 `useProjection(contextPressure/contextBreakdown/tokenUsage)` + 逐字段判空；`[DOC]` compatibility “Mirror, don't import” 6 行镜像表。 | 同源减少“68.4% vs 67%”式失信；代价是上游投影形态变化时逐字段重证、镜像点要跟版。 | 列出投影 key/owner/字段、缺字段语义、镜像文件与拟合检查。 | 镜像点含内核未导出占用率公式；上游改实现时需重拟合。 | 自己另算总量 → 与宿主显示差一格，用户永久不信面板。 |
| 估算值与供应商实测值容易混用 | 同屏并列 Estimated 与 Actual，并明确估算密度/误差与供应商上报口径；不要给单一“精确”数字。 | `[SRC-TARGET]` `Estimated ≈` 与 `Actual` 标签，页脚说明 4 字符≈1 token、Actual 来自供应商用量。 | 让用户知道何时可拿它对账；代价是要维护两套数据与文案。 | 定义 estimate 函数来源、provider usage 字段、口径脚注与取整规则。 | 四字符密度对 CJK/JSON schema 等严重低估，只能标 approx。 | 只显示估算并标成精确 → 用户拿去当账单，失真即失信。 |
| 分类合计与总量不相等 | 把“官方分类定段 + 折叠占比拆分 + 按实测总量等比锚定”写成流水线；向用户解释锚定前后两个口径。 | `[SRC-TARGET]` `officialParts`/`anchoredParts`/`billedParts`：先把 messageTokens 按内容比拆分，再缩放到目标总量；环用 billed 输入锚。 | 环与输入总量一致，细分仍保留相对比例；代价是细分数字不再是独立测量。 | 明确哪一层是测量、哪一层是按比例分摊，UI 标注“按比例”。 | 锚定后“分类≠总量”不再成立；把旧的“绝不强行对齐”当通则就错了。 | 声称每类都是实测 → 用户拿分类做审计时对不上账。 |
| 成本展示与真实账单混淆 | 把成本做成客户端估算：记录币种、单价来源、峰谷倍率、汇率与未定价 route 跳过策略，并声明不代表账单。 | `[SRC-TARGET]` 四桶单价求和、DeepSeek peak ×2、固定 USD_PER_CNY=0.15、misses 仅 tooltip；价格来自 `@opencode-ai/models`。 | 给用户相对量级与优化方向；代价是价目源第三方、汇率固定、未定价 route 静默跳过。 | 让价目源 owner/刷新语义可审计，UI 标“部分合计”与估算币种。 | 运行期是内置快照还是联网取价未核（devDependency + 构建产物）；本卡未验证账单一致性。 | 把本地估算当账单 → 与供应商对账差异被当成 bug。 |
| 宿主缺服务/缺投影时面板崩或空转 | 每个能力走可选接缝：缺服务→无能力，缺投影→逐字段判空并走无数据 UI；不挂 pending fiber、不抛错。 | `[SRC-TARGET]` `tab.visible=false` 不挂卡片/暂停订阅；投影形状不对整体 null；冷读限流跳过走无数据路径。 | 部署裁剪能力强时面板仍可用或安静消失；代价是多条降级路径要测。 | 给每个 optional seam 写 present/missing/degraded 三态与 UI。 | 本卡未见全部可选接缝的运行验证；`contextPressure` 缺失时头部会回退到自算值且未标注。 | 硬 inject/假定投影齐全 → 缺服务时白屏或假数据。 |
| 上游升级后兼容性靠口头声明 | 用 Rule/Limitation/Check/Procedure 写兼容文档，每条挂证据；并把接缝矩阵测试固定到基线 tag。 | `[DOC]` docs/compatibility.md 结构 + `dshReleases` 枚举与 engines 地板；`[SRC-TARGET]` package.json 双门禁字段。 | 使“支持哪些宿主”可审计；代价是文档与测试跟版维护。 | 给每基线列:检查命令、断言接口存在/不存在、失败处置。 | 文档自述 6 条 limitation；卡只摘了 3 条，不能称“全部”。 | 只写“支持 0.2.x” → 上游改接缝后靠用户报错。 |
| 高频读数导致重复计算与抖动 | 读数走缓存/投影，价格书懒加载单例 + 退避重试，最后一个订阅者离开后停摆。 | `[SRC-TARGET]` modelPrices 懒加载单例、30s×2^n（上限 240s）、reset 只清内存；价格不落盘。 | 减少重复请求；代价是同一账单刷新前后可能变化。 | 明确缓存 TTL、重试上限、离线 fail-closed 与“价格不可用”提示。 | 未定价 route 跳过且总价无“部分合计”标记，是本实现的可改进边界。 | 每次渲染重取价格 → 数字跳动且拖慢面板。 |
## 6. 失效条件与降级

| 触发条件 | 它会怎样 | 会不会说 |
|---|---|---|
| 宿主缺某个可选服务(如右栏) | **无服务 → 无能力**:不挂 pending fiber、不抛错 | 面板入口自动消失 |
| 宿主低于 `0.2.0-rc.2` | **双重门禁**:宿主侧装前拒绝;插件侧运行时再判,低于地板给**清零的回退单元 + 升级弹窗** | 是(升级弹窗) |
| 版本探测不出来 | **FAIL OPEN** 进真实单元(镜像一份兜底),理由:探测失灵不该把一个能用的部署变白板 | — |
| `contextWindow − reservedOutput − headroomTokens ≤ 0` | **不画斜纹掩码** | — |
| 会话投影缓存过期 | **从持久日志重折**(冷读走宿主全局限流:FIFO、一次一个、V8 堆低于上限 2/3) | 跳过时走"无数据"路径,不报错 |
| 事件畸形 | 折叠是**全函数**:未知事件原样返回,畸形事件**整体丢弃**(不留半截状态) | — |
| 单次冷读被限流跳过 | 走调用方设计的**无数据路径** | 是,不是"失败" |

---

## 7. 开放问题

- [ ] `[OPEN]` 它镜像了 6 处官方实现,其中**占用率公式在内核包里没有导出**。上游若把 `context-occupancy.ts` 导出,这镜子税能砍掉一半——但上游为什么要为一个插件导出内部函数?
- [ ] `[OPEN]` 观察不改行为:模型不知道上下文快满了。**要不要让驾驶舱反向通知模型**("还剩 12%,建议先压缩")?
- [ ] `[OPEN]` 它在 `0.2.1` 线上用到了 `job/*` 事件,在 `0.2.0` 线上只能从结果文本的**标记**反推(`derived: true`)。这类"文本标记契约"是否该由上游提供?
- [ ] `[OPEN]` 成本按 `models.dev` 列表价。第三方网关普遍打折 → **要不要支持导入账单对账**?
- [ ] `[OPEN]` 官方点名背书,**★ 仍只有 3,909**。"值得信任"的产品为什么传播不如"更好用"的?
