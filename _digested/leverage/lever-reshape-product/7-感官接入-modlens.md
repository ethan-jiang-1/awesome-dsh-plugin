# 7-感官接入 · modlens:给纯文本模型装上眼睛

> **状态**:`observed` · **基线**:DSH `0.2.1-rc.3` · **读于**:2026-10-31
> **类**:`7` 感官与模型 · **层**:**4**(模型能力)→ 5 → 3 · MIT
> **★ 3,152 / npm 63,829**(全名单下载第 2)
> **一句话**:它没有发明新技术,只解决一件极具体的事——**我用的是不能看图的模型,但我想直接 Ctrl+V 粘一张截图**,然后把这件事做到"一次都不用配置"。
> **借鉴价值**:**① 只在"上游以元数据正面确认"的能力缺位上动手,`absent means unknown` 一律放过;② 接管方式是"**加一个元数据包装条目**"——不换底层路由、不起代理、不拦 hook;③ `meta.attempts` + `meta.warnings`,回退永不静默、配额归属永远可见;④ 复用别家登录必须逐项显式同意并标出"花的是谁的额度";⑤ 密钥轮换按**错误族**分流。**

> **样本档案**
> **repo**:`liustack/modlens` · **npm**:`@liustack/modlens` · **版本**:`3.27.2`(README 示例用的精确版本)
> **目录条目**:`data/plugins/liustack__modlens.yml`(`vision`)
> **装法**:`npx -y @deepseek-ai/dsh plugin --profile web add @liustack/modlens@3.27.2`;跨 harness 的 skill 走 `npx -y skills add liustack/modlens --skill modlens --global`
> **已在本地挖掘**:`_证据/6-7-移动与视觉-原始挖掘.md` §二(modlens:模态判定/双闸门/attempts/warnings)
> **再深挖去哪**:仓库 `docs/security.md`(图片当不可信输入);`Antigravity CLI` 免 key 兜底那条

---

## 0. 一页速览(想抄的人只看这 20 行)

| 问题 | 它的答案 | 支撑 |
|---|---|---|
| 它凭什么判断"这模型没眼睛" | 读上游 `inputModalities`,其注释就是判定语义的原文:"**absent means unknown, while an explicit omission is negative capability**" | `[DSH]` `dsh-llm/lib/types/index.d.ts:317-333` |
| 所以它接管谁 | **只接管被正面确认 text-only 的 DeepSeek/GLM/MiMo Pro**;"anything unconfirmed is **left alone**";原生 vision 模型**自动排除** | `[CAT]` 原文 |
| 怎么接管 | 模型选择器里**加一个 `<model> (modlens vision)` 条目**(每 route 一个);选择被记住,一次就够 | `[CAT]` + `[DSH]` `resolveModelInfo`:目录"advisory,不控制请求路由" |
| 它换底层路由吗 | **不换**。请求仍由**同一条底层 route** 回答 | `[CAT]` |
| 它拦 hook / 起代理吗 | **不**:"No hooks, no wrappers, no local proxy daemon, **not a single line changed in any harness config**";卸载 = 删文件夹 | `[CAT]` |
| 上游第二道闸(它必须知道) | adapter 派发前把图片块投影成 `[image omitted because this model accepts text only; attachment sha256:<8>]` | `[DSH]` `dsh-llm/lib/types/index.js:884-888`、`content.js:47-50` |
| prompt 入口硬拒 | 声明了 `inputModalities` 且不含 image → 抛 `session/attachment-invalid`,reason `MODEL_DOES_NOT_SUPPORT_IMAGES` | `[DSH]` `dsh-api-session-controller/lib/index.js:927-941` |
| 兜底链 | **一条 failover 链**:API 车道(5–10s)先跑,agent CLI 车道(15–45s)兜底,**第一个好结果胜出** | `[CAT]` |
| 回退怎么不静默 | `meta.attempts` "records **every attempt** so a fallback is never silent" | `[CAT]` |
| 配额可见 | 每次复用标在 `meta.warnings` "**whose quota it spent, so nothing is ever silently billed**";表格列名直接叫 **Rides as** | `[CAT]` |
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
| ★ / npm | **3,152 / 63,829**(快照 2026-08-19;全名单下载第 2) |
| 名单内被引 | **5** |
| 引擎 | 六个视觉读取引擎,任一可用即可(含 Claude Code / Codex / OpenCode / Pi / Gemini CLI / Antigravity CLI 等 CLI 车道) |
| **已知偏差** | ① 图被转成**证据**而非原文——细节取决于上游引擎的读取质量;② **无逐版本矩阵**(只说"在真机上验证过 Claude Code/Codex/Pi/OpenCode");③ **不接受 PR**(单作者逐行 review,贡献方式是 issue 或 fork);④ 精确超时毫秒数、临时文件清理时机、脱敏字段清单**未披露** |

```sh
python3 _digested/leverage/census.py --probe "vision|image|ocr|视觉|看图"
```

---

## 5. 借鉴食谱表(本卡的产出物)

| 要解决的问题 | 照它的做法 | 你要改的地方 | 抄错的后果 |
|---|---|---|---|
| 要给别人的能力打补丁 | 先分清 `缺失 = 未知` 与 `显式否定 = 没有`,**只动后者** | 你的元数据可能是 `capabilities.x` / `features[]` | 把"未知"当"没有" → 误接管本来就能看图的模型,把能用的搞坏 |
| 怎么接管 | **加一个元数据条目**把"能力 + 策略"变成可选项;路由不动 | 条目名要带可辨识后缀(如 `(myplugin vision)`) | 改路由 / 起代理 → 复制凭据、破坏限额、升级即碎 |
| 用户要不要每次选 | 选择器**记住选择**,一次即够 | — | 每次粘贴都要选 → 用户放弃 |
| 链路要有兜底 | **一条 failover 链**:快车道先、慢车道兜底、第一个好结果胜出 | 你的车道可能是"本地模型 → 云模型" | 只给一个引擎 → 它挂了你也不可用 |
| 回退不能静默 | 固定字段 `meta.attempts`(每次尝试)+ `meta.warnings`(配额归属) | 字段名固定下来,不要每次改名 | 静默回退 → 用户以为结果来自他选的引擎 |
| 偏好 vs 钉死 | **两个开关** | — | 合成一个 → 无法解释"为什么这次没回退" |
| 多凭据 | 按**错误族**分流:认证/限流/配额换 key;网络/5xx/解析换 provider | — | 全都换 key → 网络故障时把 key 全烧一轮 |
| 借用用户已有凭据 | **发现 → 逐项显式同意 → 记录 → 每次使用可见** | 你的"已有凭据"可能是 cookie / 本机 agent | 静默借用 → 用户看到别处额度少了,信任崩塌 |
| 并入的通道 | 借来的登录 **join the pool as equals** | — | 二等通道 → 质量差且用户不知为何 |
| 代理与内网 | 内网端点用**空字符串显式声明**不走代理 | 你的可能是自建 registry / 内网 API | 靠 `NO_PROXY` 猜 → 内网请求被代理吞掉 |
| 跨多个宿主 | 能力做成宿主无关的一层,**两端只做外壳** | — | 给每端写 shim → N 倍维护、N 种行为差异 |
| 结果的可信度 | 输出附"**我不确定什么**";输入(图)当**不可信**对待 | — | 只给结论 → 用户无法判断何时该复核 |
| 卸载 | **不写宿主配置,卸载 = 删文件夹** | 检查你有没有往全局层写 | 写了一堆配置 → 卸载后行为残留 |
| 兼容性声明 | 至少写清"在哪些真机上验证过";**没有矩阵就直说没有** | — | 写"已支持全部" → 一次失败毁掉全部可信度 |

---

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
- [ ] `[OPEN]` 它没有逐版本矩阵(对照 [`多端与远程`](./6-多端与远程-dsh-mobile.md) 的逐版本表)。**"已验证"这个词要不要在本域强制带范围**?
