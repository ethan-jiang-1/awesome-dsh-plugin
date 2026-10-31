---
title: "plugin · 通用插件"
domain: reshape-product
kind: charter
positioning: "插件侧宪章：什么算「装进任何 profile 都成立的客人」，以及 11 张卡各抄哪一行。"
takeaway: "11 个插件样本的七层坐标 + 一张可照抄的接缝表。"
read_when: "要给现有 profile 加一块能力；或判断某插件算不算产品化、该不该分家。"
status: observed
updated: 2026-10-31
budget: 240
---
# plugin · 通用插件：不改上游，能装出什么产品

> **标语**:*What can a plugin add without forking?* —— 宿主是别人的，它只在接缝上加东西。
> **分工**:本 lever 只收**客人**（`dsh plugin --profile <任意> add` 装得上）；**成套装进一个 profile、浏览器里交付完整体验**的在 [`profile` 侧](../profile/README.md)，换表层/自带宿主的在 [`shell` 侧](../shell/README.md)。**先分 lever，再看编号。**
> **状态**:`observed`(机制已核) · **基线**:DSH `0.2.1-rc.3` · 名单 @ `efe602e7b` · **指标**:2026-10-31 重采
> **范围**:只收兼容 **DSH `0.2.x`** 的样本；0.1.x 时代的东西只作对照与反例。
> **视角**:**用户体验**，并且**只做借鉴用途**:一卡一插件，每张卡要交代"它好在哪、为什么好、**别人具体抄哪一行**"。
> **借阅入口**:想抄 → [18 条](../BORROW.md) · 想选型 → [卡表](#4-卡表) · 想评审 → [边界](#5-边界) · 想回源 → [样本坐标](#41-样本坐标总表要精确复现再深挖从这里开始) · 跨域 → [BORROW](../../leverage/BORROW.md)
> **规则源**:准入/分级以 [`horizon`](../../leverage/horizon.md) 为准;本线的副本是摘要。
> **全量卡片**:本表是精选;全部文件(kind/定位/能拿走什么/何时读)见 [`catalog`](../../leverage/catalog.md)。

---

## 1. 这份研究是干什么用的

**它不是插件导购。** 它回答的是:

> **别人凭什么能借鉴它?到底借鉴哪一行?**

所以每一张卡都必须交出四样东西,缺一样这张卡就不算写完:

| 要件 | 具体要求 | 写不出来意味着 |
|---|---|---|
| **① 机制到可照抄的粒度** | 不是"它做了上下文面板",而是"它读上游哪个投影字段、按什么公式算、在哪分叉、默认展开到第几层、数字对不上时怎么办" | 你只是转述了营销文案 |
| **② 为什么这么做** | 每个设计后面挂一个**可证伪的取舍**:它放弃了什么、换来了什么、代价由谁承担 | 这是"好"与"说不清为什么好"的分界 |
| **③ 怎么抄 / 别抄** | 每张卡结尾给一张**食谱表**:`要解决的问题 → 照它的做法 → 要改的地方 → 抄错的后果`。抄的人能直接照着做 | 读者看完只会说"哦,挺好" |
| **④ 失效条件** | 什么输入、什么宿主版本、什么规模下它会坏;坏了退化成什么 | 没有失效条件的方案不是工程,是信仰 |

**判据**:把一张卡给一个**没读过这个插件**的工程师,他能不能在半天内做出一个"形状对、细节抄对、知道哪里会塌"的实现。做不到就是深度不够,得重挖。

三条跨卡成立的规律(详细论证见各卡):

1. **主导权在下游,不在上游。** 谁定义格式谁定边界,谁做产品谁拿用户。
2. **"装坏了怎么回"比"一键装"更能定义一个分发产品。**
3. **体验的护城河是降级路径,不是功能数量。**

### 1.1 这个 lever 收什么（与 profile / shell 的分界）

**先过三步判定**（唯一协议见 [`00-map` §8](../00-map.md)）：**Q1 浏览器 → Q2「一块能力」**，才是本桶。

- **主问**：装进现有 profile 后，它只加一块能力，而默认体验 / 首启 / 分发仍由宿主或用户决定？
- **门槛**：★ ≥ 200 或 npm 近 30 天 ≥ 2,000；机制例外每 lever ≤ 2 张（见 [`00-map` §7](../00-map.md)）。
- **别拿"能不能 add"当判据**：终端 TUI 也能 add，但归 [`shell` 侧](../shell/README.md)。

**三张看着像宿主、其实不是**（都留在本 lever）：

- **`12_厚工作台`**：它"自己就是第一个插件"、把整套 IDE 塞进侧栏，但**没有换表层**——装的还是 `web` profile，首启/分发/降级仍由宿主回答。**厚客人，不是宿主。**
- **`51_分发与救生页`**：救生页由进程外 helper 提供，看着像"越过宿主"；但插件本体仍是宿主里的客人，救生页是它替宿主做的兜底。
- **`61_多端与远程`**：另起 3443 的 HTTPS 网关、还有 Android App；但宿主仍是 `dsh web`（被当回环上游），插件照样 `dsh plugin add` 进 profile。

反过来：**只要它开始要求"先卸宿主 / 换启动命令 / 自己发安装包"，就挪去 shell。**

---

## 2. 公共产出：18 条

**18 条已上移到产品线根目录**：[`BORROW.md`](../BORROW.md)。它跨三个 lever，不再挂在 plugin 侧。

---

> **怎么加卡**：过 00-map §11.1 的 10 分钟快筛 → 深挖 → 按 00-map §5 建卡 → catalog 与本表各补一行 → `node _leverage/verify.mjs`。

## 3. 怎么读这个目录

文件名是 `N-关键短语-插件名.md`。

**十位数字就是类别**——不用记对照表，看见 `3` 打头就知道是驾驶舱：

| 打头 | 类别 | 这一类的卡问的问题 |
|---|---|---|
| `0` | **本线的门**（口径、七层、命名法） | 什么算样本？七层怎么分？证据怎么标？ |
| `1` | **壳与工作台** | 人坐在哪张桌子前？桌子是薄基座还是厚工作台？ |
| `2` | **内容形态** | 答案本身长什么样？还是纯文本吗？ |
| `3` | **驾驶舱** | 看不见的东西（上下文、成本、编队）怎么被看见？ |
| `4` | **上手** | 第一次打开看到什么？该装什么？ |
| `5` | **分发** | 从哪装、能不能装、**装坏了怎么回**？ |
| `6` | **多端** | 同一份 DSH 怎么上另一块屏幕？ |
| `7` | **感官与模型** | 模型能感知什么？粘贴图片算不算？ |
| `8` | **协作** | 一个会话怎么变成一支团队？ |
| `9` | **反例与退役** | 什么路走不通？为什么？ |

一个插件只出一张卡；跨类能力写在卡内，不另开卡。新增卡不改老卡文件名（外链稳定）。

`_证据/` 是**挖掘期的原始记录**（逐条原文 + `上游 文件:行号`），只作引用溯源用，不是正文；卡里每个 `[DSH]` / `[CAT]` 标注都能在这里找到出处。

---

## 4. 卡表

| 卡 | 插件 | ★ / npm 月下载（2026-10-31） | 一句话 | **能借鉴什么** |
|---|---|---|---|---|
| [`领域模型`](../horizon.md) | — | — | **三个 lever 共用**的门：四条口径、七层、编号法、证据级别 | **13 行上游接缝索引**：每层「改得动 / 改不动」以及该挂哪个服务 |
| **`1` 壳与工作台** | | | |
| [`薄基座`](./11_薄基座-dock.md) | `AKS1st/dock` | 10 / 1,673 | 只给注册表、不给能力：六个 API + 六个兄弟包 | **一个服务面 + 零内部依赖 + 安装顺序不敏感**；UI 依赖写成可选 peer，缺失时"不激活"；任何隐藏都留两条逃生通道 |
| [`厚工作台`](./12_厚工作台-better-sidebar.md) | `omdsh-dev/DSH-better-sidebar` | 4,765 / 245,373 | 一个插件把自己做成 IDE，**自己就是第一个插件** | **一种扩展点形状 + 内置也走它**；原型方法注册表；`ns.v1.sessionId` 持久化 + 引用完整性；"先数扇出点再优化主路由" |
| **`2` 内容形态** | | | |
| [`生成式界面`](./21_生成式界面-dsh-genui.md) | `omdsh-dev/dsh-genui` | 827 / 48,798 | 回复本身变成可操作界面：本地优先、"诚实 UI" | **内容协议当扩展面**；节点级丢弃 + 块级退回原文；同轮纠错；无 `action` 渲染成 disabled；主题只暴露一层变量 |
| **`3` 驾驶舱** | | | |
| [`驾驶舱`](./31_驾驶舱-dsh-context.md) | `bowenliang123/dsh-context` | 3,909 / 264,177 | 五块面回答"它吃了什么、为什么变笨、钱花在哪" | **同源出数**；估算与真实并列；兼容性写成 `Rule/Limitation/Check/Procedure`；"mirror, don't import" |
| **`4` 上手** | | | |
| [`环境搬家`](./42_环境搬家-dsh-config-manager.md) | `xiajiajun516/dsh-config-manager` | 277 / 19,723 | 装完第一件事：把整套环境从旧机器/旧 agent 搬过来，先出计划再写 | **十二步导入流水线，写入放最后**；外部来源先翻译成标准包再走同一条路径；冲突必须逐条裁决；写前快照 + 失败回滚；读不到写"读失败"不写 0 |
| [`会话搬家`](./43_会话搬家-dsh-chat-import.md) | `Nwflower/dsh-chat-import` | 270 / 15,185 | 把 13+ 家 agent 的对话搬成**可续聊**的会话，能预览、能撤回、能搬回去 | **发现/保真/可撤销三件套**；预览=真解析的只读 dry-run（跳过插件注入）；解析失败列出每个解析器放弃的原因并给一条可发给 agent 的任务说明 |
| **`5` 分发** | | | |
| [`环境搬家`](./42_环境搬家-dsh-config-manager.md) | `xiajiajun516/dsh-config-manager` | `dsh-config-manager` | `xiajiajun516__dsh-config-manager.yml` (`tools`) | `dsh plugin --profile web add dsh-config-manager@latest` → 重启 | `_证据/05_上手与修复-原始挖掘.md` §一 | `dcm` CLI 子命令、migration consult 判决枚举、market 配置包校验 |
| [`会话搬家`](./43_会话搬家-dsh-chat-import.md) | `Nwflower/dsh-chat-import` | `dsh-chat-import` | `Nwflower__dsh-chat-import.yml` (`session`) | `dsh plugin --profile web add dsh-chat-import` → 重启 | `_证据/05_上手与修复-原始挖掘.md` §二 | `docs/USAGE.md` 行级规则、13+ 来源的保真分级 |
| [`分发与救生页`](./51_分发与救生页-dsh-market.md) | `dsh-market/dsh-market` | 9,902 / 813,066 | 把发现与安装搬进产品，并给"起不来"留救生页 | **救生页由进程外 helper 在原地址提供**；只给一个决定；外部索引每次使用前校验；自动重启先问"会不会杀死自己" |
| [`装坏自愈`](./52_装坏自愈-dsh-plugin-health.md) | `EasonMWS/dsh-plugin-health` | 4 / 4,377 | 升级后插件被静默拒载：先在一次性的 home 里真启动一次，再决定放不放行 | **静态检查只是第一层，隔离预演才是修复的前提**；只写一条可撤销的官方豁免；顺序即安全（先测后写）；宿主起不来时工具必须在宿主体外还能跑 |
| **`6` 多端** | | | |
| [`装坏自愈`](./52_装坏自愈-dsh-plugin-health.md) | `EasonMWS/dsh-plugin-health` | `dsh-plugin-health`（CLI）+ 同名 bundle | `EasonMWS__dsh-plugin-health.yml` (`dev`) | CLI `npm i -g dsh-plugin-health`；或 `dsh plugin --profile web add dsh-plugin-health` | `_证据/05_上手与修复-原始挖掘.md` §三 | `compatibility.json` 键结构、隔离预演的实现、top-120 扫描口径 |
| [`多端与远程`](./61_多端与远程-dsh-mobile.md) | `saya-ch/dsh-mobile` | 690 / 21,057 | 手机是**一台要配对的设备**，不是一个断点 | **配对码 + 可撤销(删哈希)+ 回环准入**；二进制供应链四项固定；`purge --yes` 式卸载清理 |
| **`7` 感官与模型** | | | |
| [`感官接入`](./71_感官接入-modlens.md) | `liustack/modlens` | 4,667 / 176,983 | 给纯文本模型装上眼睛：粘贴即读、零配置 | **未确认就放过**("absent means unknown")；加元数据条目不换路由；`meta.attempts`/`warnings` 让回退不静默 |
| **`8` 协作** | | | |
| [`81_协作`](./81_协作-dsh-agent-teams.md) | `NanmiCoder/dsh-agent-teams` | 2,597 / 50,995 | 队长 + 任务 DAG + **执行前计划**，实时活动面板 | **计划先行 + 唯一授权点 + 三层否定**；完成时审计而非写入拦截；磁盘真相并坦白"不跨进程" |

**shell 侧那 2 张不在这张表里**：[`终端即产品`](../shell/14_终端即产品-dsh-TUI.md) 与 [`冻结 fork`](../shell/91_冻结分叉-better-sidebar-N23.md)，见 [`shell`](../shell/README.md)。

---

## 4.1 样本坐标总表(要精确复现/再深挖,从这里开始)

**每个样本都必须能被一句话定位**:repo 在哪、npm 叫什么、目录条目是哪个文件、装法是什么、本 lever 已经挖到哪、还有哪里没挖。缺任何一列,这张卡就不算可复现。

| 卡 | repo | npm 包名 | 目录条目(`data/plugins/…`) | 装法(0.2.x) | 已挖 | 未挖/待深挖 |
|---|---|---|---|---|---|---|
| [`厚工作台`](./12_厚工作台-better-sidebar.md) | `omdsh-dev/DSH-better-sidebar` | `dsh-better-sidebar` | `omdsh-dev__DSH-better-sidebar.yml` (`ui`) | `dsh plugin --profile web add dsh-better-sidebar@latest` | `_证据/01_壳与工作台-原始挖掘.md` §一 | 版本对照表全表、`CHANGELOG`、`ctx.betterSidebar` 类型声明 |
| [`薄基座`](./11_薄基座-dock.md) | `AKS1st/dock` | `dock-base` + 兄弟包 `dock-files`/`dock-editor`/`dock-images`/`dock-markdown`/`dock-git`/`dock-spreadsheet` | `AKS1st__dock.yml` + `AKS1st__dock-*.yml` (`ui`) | `dsh plugin --profile web add dock-base` 后逐条装 | `_证据/01_壳与工作台-原始挖掘.md` §二 | 仓库 `src/client/contract.ts`、0.2.x 实测(本卡 `[OPEN]`) |
| [`生成式界面`](./21_生成式界面-dsh-genui.md) | `omdsh-dev/dsh-genui`(npm scope 是 `@changfenhuang`) | `@changfenhuang/dsh-genui` | `omdsh-dev__dsh-genui.yml` (`ui`) | `dsh plugin --profile web add @changfenhuang/dsh-genui` | 本轮直接读 README 全文(429 行),行号已内联 | **`SKILL.md` 字段级 schema**、`docs/map.md`、action payload 信封 |
| [`驾驶舱`](./31_驾驶舱-dsh-context.md) | `bowenliang123/dsh-context` | `dsh-context` | `bowenliang123__dsh-context.yml` (`usage`) | GUI Add plugin,或 `dsh plugin --profile web add dsh-context` | 本轮直接读 README 全文(237 行)+ 上游 `dsh-token-meter` 源码 | git tag `v0.78.2` 快照、`docs/compatibility.md`、`docs/model-pricing-mapping.md` 与页脚两行 **0.2.2-alpha.2** 核实 |
| [`分发与救生页`](./51_分发与救生页-dsh-market.md) | `dsh-market/dsh-market` | `dshmarket`(商店内显示 **Plugin Market**) | `dsh-market__dsh-market.yml` (`market`) | Desktop:Settings→Plugins;web:`dsh plugin --profile web add dshmarket` | `_证据/02_首启与分发-原始挖掘.md` §二 + §四 | issue #227/#139 原文、救生页 HTML 的实际实现 |
| [`多端与远程`](./61_多端与远程-dsh-mobile.md) | `saya-ch/dsh-mobile` | `dsh-mobile`(+ Android App) | `saya-ch__dsh-mobile.yml` (`remote`) | 见卡 §3.1(Android App / 浏览器两条路) | `_证据/03_移动与视觉-原始挖掘.md` §一 | `compat.js` 的语法下限实测(Chromium 92 那档 `[OPEN]`) |
| [`感官接入`](./71_感官接入-modlens.md) | `liustack/modlens` | `@liustack/modlens` | `liustack__modlens.yml` (`vision`) | `npx -y @deepseek-ai/dsh plugin --profile web add @liustack/modlens@3.27.2` | `_证据/03_移动与视觉-原始挖掘.md` §二 | 六个引擎各自的质量差异、`docs/security.md` 全文 |
| [`协作`](./81_协作-dsh-agent-teams.md) | `NanmiCoder/dsh-agent-teams` | `@nanmicoder/dsh-agent-teams` | `NanmiCoder__dsh-agent-teams.yml` (`workflow`) | Plugins→Add plugin 填 `github:NanmiCoder/dsh-agent-teams` | 本轮直接读 README + `compatibility.json` + manifest | **三层否定的实现方式**(会话状态还是提示词)、`<workspace>/.agent-teams/` 实际文件格式 |

**三条读这张表的规矩**:

1. **repo 与 npm 包名经常不同**(`omdsh-dev/dsh-genui` ↔ `@changfenhuang/dsh-genui`;`dsh-market/dsh-market` ↔ `dshmarket`)。只写一个,别人就装不上或 clone 不到。
2. **目录条目文件名是 `owner__repo.yml`**,可直接 `cat data/plugins/<该文件>` 取到官方 `url` / `name` / `category` / 双语描述 —— 这是**最省事的二次核实入口**。
3. **"已挖"那一列只写文件与节号**,不写人头结论;要复核任何 `[DSH]` / `[CAT]` 标注,先到这里找到原文,再去 `_证据/` 对行号。

**shell 侧 2 张的坐标**（repo / npm / 装法 / 已挖）在 [`../shell/README.md`](../shell/README.md) §3，不在这张表里。

---

## 5. 边界

**收**：兼容 `0.2.x`、能 `dsh plugin --profile <任意> add` 装进现有 profile、且改变了**人怎么用它**（入口 / 首屏 / 默认值 / 身份 / 界面 / 分发 / 上手路径）、有可复核的影响力证据。

**不收**：纯能力增强（多一个工具、多一个 provider）、只支持 `0.1.x` 的样本、目录里查不到也拿不到任何计量的条目（除非机制独特且写明理由）。

**不碰**：换表层 / 自带宿主的样本 → [`shell`](../shell/README.md)；上游代码本身的建议 → `lever-cross-boundary` / `lever-draw-limit` / `lever-prove-output` 三个域。本 lever 只写"下游把插件装进别人的产品里，装出了什么"。

**共享文件只读**：`00-map.md`、`horizon.md`、`leverage/README.md`、`data/` 由别的会话维护，本线只调用、不写。

---

## 6. 计量口径

- ★ / npm 下载：**2026-10-31 统一重采**（GitHub API / npm last-month，快照存 `../_证据/指标快照-2026-10-31.json`）；仓库自带 `data/*.json` 的 2026-08-19 快照只作历史对照。
- **两种口径不可互证**：★/下载按 GitHub URL 映射；GitHub API 是另一套时点。引用时写明用的是哪一种，并带日期。
- **不做全库计数**：名单在涨，`N / 总数` 没有稳定真值；「少见 / 唯一」只写人工回读判断，标 `[OBS]`。
- **已知偏差**：① 插件目录**只收能 `dsh plugin add` 的东西**，桌面壳 / 手机 App 不在其中 → 按目录看会系统性低估 2/7 层；② 短名召回差（`TUI`、`dock`）；③ 下载量含 CI 与镜像，不等于用户数。

---

## 7. 每张卡的固定骨架

```
0 一页速览        ← 想抄的人先读这 20 行
1 它在产品里的位置  ← 七层坐标 + 它到底改了什么
2 机制(可照抄)    ← 数据从哪来 / 关键属性的形状 / 算法 / 阈值
3 体验
4 证据与边界      ← 数字口径、明星引用、已知偏差
5 借鉴食谱表      ← 问题 → 照它做 → 要改的地方 → 抄错的后果
6 失效条件与降级
7 开放问题
```

**`5` 是这张卡的产出物**,其余各节都是为它服务的举证。若某卡没有 `5`,按本 README §1 的判据视为未完成。

---

## 8. 待办

- [ ] 第二梯队的 `6`/`7` 类候选：`shaobeichen/dsh-pocket`（10,411 下载）、`THEWOLFWALKER/dsh-notifier`（6,677）、`ysr666/dsh-vision-router`（21,679）、`Anionex/dsh-vision-toolkit`（17,248）——先判断它们是否**改变了交互契约**，只加能力的不成卡
- [ ] `3` 类第二张候选：`feibi-mochi/deepseek-harness-control-center`（2,066 下载）
- [ ] `4` 类已补两张（`42_环境搬家` / `43_会话搬家`）；**仍未成卡的两条支线**：①「就地索引」（`vshulcz/deja-vu`，★1,342 / DSH 包 `dsh-deja` 月 6,089，先判它算 4 类还是 7 类）；②「引导推荐」（`dsh-bootstrap` 仍是观察样本，★1/763 不过门槛）
- [ ] `5` 类已补第二张（`52_装坏自愈`）；下一个候选 `sjh9714/dsh-win32`（★151 / 月 4,721，安装 + 实机验收 + 修复，Windows-only）

**搬到 shell 侧的待办**（口径外产品、证伪样本）见 [`../shell/README.md`](../shell/README.md) §5。
