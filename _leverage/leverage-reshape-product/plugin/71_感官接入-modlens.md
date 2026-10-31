---
title: "感官接入 · modlens"
domain: reshape-product
kind: sample
positioning: "`@liustack/modlens@3.27.2`：tool + provider wrapper + paste 路由 + 可选 pre-step hook；dsh 面丢弃 meta.attempts/warnings，回退静默。"
takeaway: "四条图像入口且 takeover 有严格/自动两套；dsh 面只取 result，attempts/warnings 被丢弃；零配置仍需引擎。"
read_when: "要补模型能力缺口（视觉/语音/搜索）；或要接管别人的路由而不改它。"
status: observed
updated: 2026-10-31
---
# 感官接入 · modlens:给纯文本模型装上眼睛

> **状态**:`observed` · **基线**:DSH `0.2.1-rc.3` · **读于**:2026-10-31
> **类**:`7` 感官与模型 · **层**:**4**(模型能力)→ 5 → 3 · MIT
> **★ 4,667 / npm 176,983**（2026-10-31 实时；本线第 4）
> **一句话**:它没有发明新技术,只解决一件极具体的事——**我用的是不能看图的模型,但我想直接 Ctrl+V 粘一张截图**,然后把这件事做到"一次都不用配置"。
> **借鉴价值**：① takeover verdict 对 unknown 保守，但默认 wrapper 对已知 family 的缺失模态仍接管；② 不只“加元数据条目”：源码注册 tool + provider adapter + web 路由 + 可选 pre-step hook；③ CLI 有 attempts/warnings，但 dsh 面只取 result，回退与配额归属静默；④ 复用登录逐项同意；⑤ 密钥轮换按错误族分流。**

> **证据深度**:源码级（上游模型/附件接缝 + README）（2026-10-31）
> **样本档案**
> **repo**:[`liustack/modlens`](https://github.com/liustack/modlens) · **npm**:`@liustack/modlens` · **版本**:`3.27.2`(README 示例用的精确版本)
> **目录条目**:`data/plugins/liustack__modlens.yml`(`vision`)
> **装法**:`npx -y @deepseek-ai/dsh plugin --profile web add @liustack/modlens@3.27.2`;跨 harness 的 skill 走 `npx -y skills add liustack/modlens --skill modlens --global`
> **已在本地挖掘**:`_证据/03_移动与视觉-原始挖掘.md` §二(modlens:模态判定/双闸门/attempts/warnings)
> **再深挖去哪**:仓库 `docs/security.md`(图片当不可信输入);`Antigravity CLI` 免 key 兜底那条
> **证据链**：固定 3.27.2 的四条入口、adapter takeover、attempts 丢弃与限额见[`16 源码复核`](./_证据/16_感官接入-modlens-源码复核.md)。

---

## 它想干什么 · 为什么值得借鉴

**意图。** 它只解决一件极具体的事：我用的是不能看图的模型，但我想直接 Ctrl+V 粘一张截图。交付单位是模型选择器里多出的一个元数据条目 `<model> (modlens vision)`（每 route 一条），选一次就被记住。README 声称不换底层路由、不起代理、不拦 hook；源码实际有 provider adapter 与可选 pre-step hook，因此不能按 README 的“零介入”理解。

**意义。** 它补的是“模型能力缺口”这一格，但判断方式比能力本身更值得抄：只在 `inputModalities` **显式否定** image 时接管，缺失按 `absent means unknown` 一律放过，原生 vision 自动排除。它改的惯例是“接管 = 换路由或起代理”：只加一条 advisory 的目录条目，让“模型 + 前置处理”变成可选项，请求仍由同一条 route 回答。这让补丁可以薄到不复制凭据、不复制限额。

**用户价值。** 装前，粘图要么被投影成 `[image omitted …]`，要么在 prompt 入口就被 `MODEL_DOES_NOT_SUPPORT_IMAGES` 拒掉；装后，粘贴即读，缩略图留在消息里。觉得值的是用纯文本模型又习惯截图的开发者；回退也可见——`meta.attempts` 记录每一次尝试，`meta.warnings` 标出花的是谁的额度，表格列名直接叫 **Rides as**。代价是图被转成结构化证据必然有损，读取质量取决于背后引擎，复用别家登录还得逐项显式同意。

**表达（界面与交互）。** 第一屏几乎不存在：装完无需 modlens 配置，但至少需要一个可用引擎，模型选择器里多一条 `(modlens vision)`，选一次就够，之后唯一的主动作是粘贴。默认值全部偏向“不动”：模态未声明不接管、原生 vision 自动排除、没选包装条目时静默退回上游默认而不报错。诚实被做进交互：结果附“我不确定什么”，`config set provider` 是**偏好**（链仍兜底）、`-p` 是**钉死**（无回退），两个开关而不是一个。

## 0. 一页速览(想抄的人只看这 20 行)

| 问题 | 它的答案 | 支撑 |
|---|---|---|
| 它凭什么判断"这模型没眼睛" | 读上游 `inputModalities`,其注释就是判定语义的原文:"**absent means unknown, while an explicit omission is negative capability**" | `[DSH]` `dsh-llm/lib/types/index.d.ts:317-333` |
| 所以它接管谁 | takeover verdict 严格 unknown→false；但默认 wrapper 对 deepseek/glm/mimo family 在模态缺失时仍接管；`families:['*']` 才要求显式 text | `[SRC-TARGET]` |
| 怎么接管 | 模型选择器里**加一个 `<model> (modlens vision)` 条目**(每 route 一个);选择被记住,一次就够 | `[CAT]` + `[DSH]` `resolveModelInfo`:目录"advisory,不控制请求路由" |
| 它换底层路由吗 | **不换**。请求仍由**同一条底层 route** 回答 | `[CAT]` |
| 它拦 hook / 起代理吗 | README 说 “No hooks, no wrappers”；源码实际注册 tool + provider adapter + 两条 web route + 可选 pre-step hook + settings namespace | `[SRC-TARGET]` 与 README 矛盾 |
| 上游第二道闸(它必须知道) | adapter 派发前把图片块投影成 `[image omitted because this model accepts text only; attachment sha256:<8>]` | `[DSH]` `dsh-llm/lib/types/index.js:884-888`、`content.js:47-50` |
| prompt 入口硬拒 | 声明了 `inputModalities` 且不含 image → 抛 `session/attachment-invalid`,reason `MODEL_DOES_NOT_SUPPORT_IMAGES` | `[DSH]` `dsh-api-session-controller/lib/index.js:927-941` |
| 兜底链 | **一条 failover 链**:API 车道(5–10s)先跑,agent CLI 车道(15–45s)兜底,**第一个好结果胜出** | `[CAT]` |
| 回退怎么不静默 | CLI 产 `meta.attempts`/`warnings`，但 dsh 的 `parseCliResult` 只取 `result` → 插件面回退与配额归属静默 | `[SRC-TARGET]` |
| 配额可见 | CLI 有 warnings/Rides as；dsh 面丢弃 meta，看不到用了谁的配额 | `[SRC-TARGET]` |
| 偏好 vs 钉死 | `config set provider <name>` = **偏好**(链仍兜底);`-p <name>` = **钉死单一、无回退** | `[CAT]` |
| 密钥轮换 | 逗号分隔多 key;**认证/限流/配额 → 换下一个 key**;**网络/5xx/解析 → 跳过剩余 key 直接换 provider** | `[CAT]` |
| 复别家登录 | `reuse.codex / opencode / pi / grok`,**每项一次显式同意并记录在 config**;"asks before reusing any of them" | `[CAT]` |
| 内网例外 | `modlens config set openai.proxy ""`——**空字符串显式声明"不走代理"**,不靠 `NO_PROXY` 猜 | `[CAT]` |
| 输出的诚实 | 结果附带 "**honestly stated uncertainty**" | `[CAT]` |
| 跨 harness | 同一份能力两种封装:skill 一个文件夹 / dsh 一个插件 | `[CAT]` |
| 最该抄的一句 | "**Evidence, not imagination**" | `[CAT]` |

---

## 1. 它在产品里的位置

| 层 | 动作 | 机制 |
|---|---|---|
| **4 模型能力** | 让纯文本模型"看见"图 | **只加元数据条目**,路由不变 |
| 5 默认值 | 安装时问"要不要复用别家登录";`auto` 可复用本地 CLI | 逐项同意 |
| 3 槽位 | Plugins 页 ModLens 卡片(`dsh 0.1.7+`) | 切引擎、勾 `auto`、保存生效 |

### 1.1 接缝在哪(一张图)

```
用户 Ctrl+V 截图
   │
   ▼  (1) prompt 入口准入 —— [DSH] 本来就有:声明不含 image 就拒绝
模型选择器选中 "DeepSeek-V4-Flash (modlens vision)"   ← ModLens 唯一新增的东西(元数据)
   │
   ▼  (2) adapter 派发前 —— [DSH] 本来就有:text-only 模型收到图片块 → 投影成一行占位文本
请求仍走同一条底层 route
   │
   ▼  (3) ModLens 自己的驾驶室:failover 链把图变成**结构化证据**
正文 + meta.attempts + meta.warnings
```

**关键**:上游第 (1)(2) 两道闸本来就存在。ModLens 做的是让第 (1) 道**不触发**(给包装条目声明 `inputModalities` 含 `image`),然后在**自己的车道**里把图转成文本证据。**它不改路由、不拦流、不复制凭据。**

---

## 2. 机制(可照抄的部分)

### 2.1 "未确认就放过"的判定规则

| 上游元数据状态 | 上游语义 | 它的动作 |
|---|---|---|
| `inputModalities` **缺失** | `absent means unknown` | **不动** |
| 显式不含 `image` | negative capability | **接管**(加包装条目) |
| 显式含 `image` | 原生能看图 | **自动排除** |

> **抄这条纪律**:凡是"我要补别人的能力",先问"**我怎么知道它真的缺**"。用元数据的**缺失 / 否定**区分"未知"与"没有",是唯一不会误伤的写法。"我没看到 image 就当它不能看图"会把你自己的图路搞挂。

### 2.2 加一个条目,而不是换一条路由

| 要改的东西 | 它的做法 | 为什么可行 |
|---|---|---|
| 让选择器出现 `<model> (modlens vision)` | 每 route 一个包装条目(stock 安装得到 Flash / Pro 两条,opencode-go、zai 各自一条) | `[DSH]` "catalog membership remains advisory and does not control request routing" |
| 记住选择 | 选择器自己记("once is enough") | 不让用户每次挑 |
| 请求怎么走 | 仍由**同一条底层 route** 回答 | 不复制凭据、不复制限额 |
| 两个入口一致 | 选择器与设置共享同一份 `ModelDirectory` | `[DSH]` "A switch made in either entry updates this shared state" |
| 模态词表 | provider 可扩展 `ModelModalityMap` | 将来非 image 的模态也能这么包 |

> **本卡最可迁移的一招**:想给"任何模型 + 任何前置处理"造一个可选形态,**不要**改路由、不要起代理、不要拦流;**用一个元数据条目把"模型 + 处理策略"变成一个可选择的东西**。

### 2.3 失败链:两个字段解决"回退永不静默"

| 字段 | 保证 |
|---|---|
| `meta.attempts` | **每一次尝试**都记录 → 回退不可能静默 |
| `meta.warnings` | 每次复用他方额度都标出**花的是谁的** |

配套的**偏好 / 钉死分离**:

| 开关 | 语义 | 结果 |
|---|---|---|
| `config set provider <name>` | **偏好** | 链**仍兜底**——偏好失败会换别人 |
| `-p <name>` | **钉死** | **无回退**,宁可失败也不换 |

> **"我想要 X" 与 "我只要 X" 必须是两个开关**。合成一个,你就永远无法同时解释"为什么不回退"和"为什么回退了"。

### 2.4 密钥轮换:错误族决定动作

| 错误族 | 动作 | 理由 |
|---|---|---|
| 认证 / 限流 / 配额 | **换下一个 key**(同 provider) | 换个身份就能过 |
| 网络 / 5xx / 解析失败 | **跳过剩余 key,直接换 provider** | 换身份也没用,别烧额度 |

> 一个极小的判断,决定了"浪费多少个失败请求"。**任何多凭据轮换都该按这个分法写。**

### 2.5 复用他人登录:同意、记录、可见

| 环节 | 做法 |
|---|---|
| 发现 | `modlens doctor` **发现**可用登录 |
| 授权 | `config set reuse.codex true` 等**逐项显式同意**,记录在配置里;安装流程对"装进哪个 harness"问**同一个问题** |
| 并入 | "Granted logins **join the engine pool as equals**"(不是降级通道) |
| 可见 | 每次读标 `meta.warnings`;列名 **Rides as** |
| 例外 | 内网端点用 `config set openai.proxy ""` **显式关闭代理** |

> 任何"借用用户已有凭据 / 额度"的功能,**同意、记录、可见**三个环节缺一不可。少一个就会出现"我的 Codex 额度怎么少了"。

### 2.6 跨 harness:一份能力,两种封装

| 封装 | 形态 | 安装 | 触发 |
|---|---|---|---|
| skill | **一个 skill 文件夹** | `npx -y skills add liustack/modlens --skill modlens --global`(user level)+ **重启 harness** | "the skill triggers on its own" |
| dsh plugin | **一个插件** | `npx -y @deepseek-ai/dsh plugin --profile web add @liustack/modlens@3.27.2`(**精确版本**) | 选择器条目 |
| 二次自证 | skill 封装里还有一道守卫:"**guard confirms the model truly has no vision**" | — | 运行时再确认,而非静态配置 |

> 它**不是**给两端写 shim:能力做成宿主无关的一层,两端只是外壳。这也解释了"不写任何 harness 配置"。

---

## 3. 体验

### 3.1 首次使用

| 步 | 动作 | 用户感受 |
|---|---|---|
| 1 | 装(一条命令,**精确版本**) | 无配置 |
| 2 | (可选)`modlens doctor` 看有哪些现成登录 | 显式决定要不要借 |
| 3 | 模型选择器挑一次 `(modlens vision)` | 一次即够,以后被记住 |
| 4 | **直接 Ctrl+V 粘图** | 缩略图**留在消息里**;图在请求时被转成结构化证据 |
| 5 | 想换引擎 / 勾 `auto` | Plugins 页 ModLens 卡片 |

### 3.2 输出契约里罕见的诚实

- 结果附 **honestly stated uncertainty**(示例是"关于**被截断的文件名**的不确定")。
- 文档把图片内容当**不可信输入**(`docs/security.md` 的定位是 "image content as untrusted input")。

> **让模型在结果里写"我不确定的是什么"**,比让它在别处打高分更有用。

### 3.3 模型看到的

**一次真正的供给侧变化**:模型从"收到一行 `[image omitted …]`"变成"收到结构化证据"。而且这个变化**只在用户选中包装条目时发生**——不选,一切与上游默认行为完全一致。

---

## 4. 证据与边界

| 口径 | 值 |
|---|---|
| ★ / npm | **4,667 / 176,983**（2026-10-31 实时；本线第 4） |
| 名单内被引 | **5** |
| 引擎 | 六个视觉读取引擎,任一可用即可(含 Claude Code / Codex / OpenCode / Pi / Gemini CLI / Antigravity CLI 等 CLI 车道) |
| **已知偏差** | ① 图被转成**证据**而非原文——细节取决于上游引擎的读取质量;② **无逐版本矩阵**(只说"在真机上验证过 Claude Code/Codex/Pi/OpenCode");③ **不接受 PR**(单作者逐行 review,贡献方式是 issue 或 fork);④ 精确超时毫秒数、临时文件清理时机、脱敏字段清单**未披露** |


---

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 纯文本模型需要读图 | 不改宿主路由：用 tool + provider wrapper + paste 路由 + 可选 pre-step 四条入口。 | `[SRC-TARGET]` modlens_read_image、modlens-<upstream> adapter、/modlens/paste、autoRead。 | 不 fork 宿主 UI/route；代价是多入口语义与兼容面。 | 明确各入口的触发条件、能力差异与关闭方式。 | README 称“无 hooks/wrappers”，与源码矛盾。 | 以为只注册 tool → 实际还有 adapter/hook。 |
| 模态能力未知 | 对“未知”做保守判定：takeover verdict 严格 unknown→false；但 wrapper 自动发现对已知 family 缺失模态仍接管。 | `[SRC-TARGET]` verdict 与 wrapper 两套策略；`families:['*']` 才要求显式 text。 | 兼顾兼容与安全；代价是行为不一致、难以解释。 | 统一“未知”策略或明确分入口文档。 | 媒体类型缺失直接拒绝。 | 笼统宣传“absent=unknown” → 与 wrapper 行为不符。 |
| 多引擎回退要可解释 | 产出 attempts/warnings，并在 UI/日志显示；但消费端可能丢弃。 | `[SRC-TARGET]` CLI 产 meta.attempts/warnings；dsh parseCliResult 只取 result。 | 引擎可替换；代价是 dsh 面回退静默。 | 在消费端保留 meta 或写日志。 | 本版本 dsh 面看不到回退原因。 | 以为有 attempts 就一定可见 → 排障无门。 |
| 全引擎失败 | 定义明确降级：wrapper/autoRead 用占位文本继续，tool 抛带 exit code 的错误；不自动切回原生视觉。 | `[SRC-TARGET]` 60s 失败冷却与固定占位；tool 抛错。 | 不让请求卡死；代价是模型可能读到占位而非真图。 | 让占位可识别，并提供显式“回到原生”开关。 | 未验证真实宿主 E2E。 | 静默占位 → 模型基于假内容回答。 |
| 凭据与浏览器边界 | key 不进浏览器、不落副本；config 0600、隐藏回显、错误脱敏；但 spawn 继承 process.env。 | `[SRC-TARGET]` hasKey 检查、reuse grant、空 proxy 直连；env 继承。 | 减少泄漏面；代价是 env 仍是旁路。 | 清理子进程 env 白名单，限制 CLI 路径覆盖。 | `MODLENS_DSH_CLI` 可覆盖 CLI。 | 以为 key 隔离 → 子进程/覆盖路径泄露。 |
| 上传/附件限额 | 分入口定义大小/类型/魔数/归一化上限，并测试边界。 | `[SRC-TARGET]` paste 25MiB/6 类；宿主附件 20MiB/4 类/≤4MiB；HEIC 仅 paste。 | 防止资源滥用；代价是双套规则易混淆。 | 统一限额表并在 UI 显示；补 25MiB 边界测试。 | 25MiB 边界无测试。 | 大文件绕过或误拒。 |
| “零配置”宣传 | 区分“无需新配置”与“无需引擎”：至少一个引擎可用才成立。 | `[SRC-TARGET]` 无配置文件可跑，但链为空则全失败。 | 降低上手门槛；代价是仍需安装/授权引擎。 | 首启检测引擎并给安装/授权指引。 | 无引擎时全失败。 | 用户以为装上就能读图 → 首次使用失败。 |
## 6. 失效条件与降级

| 触发 | 行为 |
|---|---|
| 模型是原生 vision | **自动排除**,不接管 |
| 模型模态**未声明** | **不动**(unconfirmed → left alone) |
| 某引擎失败/超时 | 链条继续;`meta.attempts` 如实记录 |
| 用户 `-p` 钉死 | 该引擎失败 → **不回退**,直接失败 |
| 网络/5xx/解析错误 | 跳过剩余 key,**直接换 provider** |
| 本机没有任何视觉通道 | `Antigravity CLI` 作为**免 key** 兜底("Nothing installed locally? Antigravity CLI is a free no-key channel") |
| 代理不可用 | 内网端点可 `openai.proxy ""` 关闭代理 |
| 未选中包装条目 | 退回上游默认(图片被投影成占位文本),**不报错** |
| dsh 版本太旧没有 Plugins 卡片 | 走 CLI 配置;模态 API 最低版本未声明 |

---

## 7. 开放问题

- [ ] `[OPEN]` 它的接管依赖"给包装条目标注 `inputModalities` 含 image"从而绕过 prompt 入口的闸。**这是上游有意留的口子,还是一个可利用的语义缺口**?上游该不该给"前置处理器"一个正式声明?
- [ ] `[OPEN]` 图 → 结构化证据,**信息必然有损**。它用 `meta.attempts` 让损耗可追溯,但**用户能不能看到"原图 vs 证据"的对照**?
- [ ] `[OPEN]` 它借别家 CLI 的视觉能力。这条链的长期合法性(ToS、额度、封号)只有一句 "you are responsible for"。生态需要一条统一约定吗?
- [ ] `[OPEN]` 它**不接受 PR**。单作者逐行 review 换来质量,代价是生态无法贡献。**高信任插件该如何开放而不劣化**?
- [ ] `[OPEN]` 它没有逐版本矩阵(对照 [`多端与远程`](./61_多端与远程-dsh-mobile.md) 的逐版本表)。**"已验证"这个词要不要在本线强制带范围**?
