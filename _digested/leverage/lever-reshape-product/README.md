---
title: "lever-reshape-product：产品形态"
domain: reshape-product
kind: charter
positioning: "本域宪章：只收改变「人怎么用它」的 0.2.x 样本；一卡一插件，卡卡要交借鉴食谱。"
takeaway: "18 条可直接搬走的产品规则 + 11 个样本的七层坐标。"
read_when: "要改产品形态（壳/槽位/首启/分发/多端/身份）；或判断某插件算不算产品化。"
status: observed
updated: 2026-10-31
budget: 240
---
# lever-reshape-product · 不改上游，DSH 能被组装成什么产品

> **标语**:*What product can DSH become without forking it?* —— 产品的单位不是插件，是 profile。
> **状态**:`observed`(机制已核) · **基线**:DSH `0.2.1-rc.3` · 名单 @ `efe602e7b` · **快照**:2026-08-19
> **范围**:只收兼容 **DSH `0.2.x`** 的样本；0.1.x 时代的东西只作对照与反例。
> **视角**:**用户体验**，并且**只做借鉴用途**:一卡一插件，每张卡要交代"它好在哪、为什么好、**别人具体抄哪一行**"。
> **借阅入口**:想抄 → [18 条](#2-可以直接搬走的-18-条全卡片的公共产出) · 想选型 → [卡表](#4-卡表) · 想评审 → [边界](#5-边界) · 想回源 → [样本坐标](#41-样本坐标总表要精确复现再深挖从这里开始) · 跨域 → [BORROW](../BORROW.md)
> **规则源**:准入/分级以 [`horizon`](../horizon.md) 为准;本域的副本是摘要。
> **全量卡片**:本表是精选;全部文件(kind/定位/能拿走什么/何时读)见 [`catalog`](../catalog.md)。

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

---

## 2. 可以直接搬走的 18 条(全卡片的公共产出)

**如果你只读一节,读这一节。** 每条都在某张卡里被具体实现过,附"抄错的后果"。

| # | 规则 | 一句话说清 | 出处 | 抄错的后果 |
|---|---|---|---|---|
| 1 | **同源出数** | 凡是用户**已经见过**的数字(占用率、状态行、计费量),只允许上游那一份投影出数 | [`3-驾驶舱`](./3-驾驶舱-dsh-context.md) | 你显示 68.4%、输入框的环显示 67% → 整套面板永久失信 |
| 2 | **估算与真实并列** | 不二选一:估算值加 `≈`,旁边给 provider 上报的真值 | [`3-驾驶舱`](./3-驾驶舱-dsh-context.md) | 只给估算 → 用户拿它当账单,差一次就再也不看 |
| 3 | **兼容性写成可执行清单** | `Rule / Limitation / Check / Procedure` 四类,每条挂**上游源码路径**;接缝矩阵测试断言**退役接缝不存在** | [`3-驾驶舱`](./3-驾驶舱-dsh-context.md) | 只写"支持 0.2.x" → 上游一改靠用户报错 |
| 4 | **两个版本声明分工** | `engines.dsh` 是**地板**(粗门),`dsh.compatibility.dshReleases` 是**逐版本枚举**(安装证据);两者在不同宿主线上各自是唯一门禁,所以都要写 | [`3-驾驶舱`](./3-驾驶舱-dsh-context.md) · [`8-协作`](./8-协作-dsh-agent-teams.md) | 只写 peer → 在 `0.2.1-alpha.4+` 上不再生效 |
| 5 | **无服务 → 无能力** | 能力走**可选接缝**(延迟 `ctx.inject` / 一次性 `ctx.get`),缺服务时不挂 fiber、不抛错,面板入口自己消失 | [`3-驾驶舱`](./3-驾驶舱-dsh-context.md) | 硬 `inject` → 少一个包就白屏 |
| 6 | **能力探测式 UI** | 别人的插件在不在,决定我的入口显不显示("装它才有,没装不显示") | [`1-厚工作台`](./1-厚工作台-better-sidebar.md) · [`3-驾驶舱`](./3-驾驶舱-dsh-context.md) | 显示一个点了没反应的按钮 → 用户以为坏了 |
| 7 | **救生页活在启动之外** | "起不来"的兜底页必须由**不依赖插件栈**的东西提供,并且能选择**下一次启用哪些** | [`5-分发与救生页`](./5-分发与救生页-dsh-market.md) | 救生页也挂在坏掉的 profile 上 → 一起起不来 |
| 8 | **版本锁不到就跳过** | 装不上精确版本时**不装**,而不是装个近似的;并把"没做"说出来 | [`4-首启推荐`](./4-首启推荐-dsh-bootstrap.md) | 装了不兼容的版本 → 首启即崩,用户归因给整个产品 |
| 9 | **配置导出要能表达"保持现状"** | 环境码里**没包含**的项 = 不改变现状,不是"卸载" | [`4-首启推荐`](./4-首启推荐-dsh-bootstrap.md) | 用户导入一次配置,反而被删掉插件 |
| 10 | **计划先行 + 唯一授权点** | 先出将要发生的计划(不执行),聊就是改同一份草稿,**只有**一个按钮开跑;否掉之后**阻止自动重建** | [`8-协作`](./8-协作-dsh-agent-teams.md) | 一按就跑/否掉又复活 → 用户再也不点第二次 |
| 11 | **接管必须保守** | 不确定能不能接管时**放过**(回落到原生/文本),并说明"我没做" | [`7-感官接入`](./7-感官接入-modlens.md) | 强行接管 → 把本来能用的模型弄坏 |
| 12 | **多端是一台要配对的设备** | 有配对码、有效期、可撤销(撤销=删除哈希)、回环准入、锁屏不含正文 | [`6-多端与远程`](./6-多端与远程-dsh-mobile.md) | 当成响应式断点 → 等于把会话开放给整个局域网 |
| 13 | **注册表方法必须是原型方法** | 自建 `ctx.myService.registerX` 只能写成 prototype 方法,不能写成实例箭头属性 | [`1-厚工作台`](./1-厚工作台-better-sidebar.md) · [`1-薄基座`](./1-薄基座-dock.md) | Cordis 服务代理会把 effect 绑到服务自己的 root → 插件卸载时注册项不回收,且只在卸载时暴露 |
| 14 | **坏数据结构分两层校验** | schema 之外再加**引用完整性**(id 对 key、序号不越界、比例和为 1、无孤儿节点) | [`1-厚工作台`](./1-厚工作台-better-sidebar.md) | schema 过了不代表状态自洽 → 恢复出半个布局,点一下就崩 |
| 15 | **降级链的终点是"人还能读的原文"** | 节点坏就丢节点,块坏就退回原始 Markdown/代码块,插件缺席也要历史不破 | [`2-生成式界面`](./2-生成式界面-dsh-genui.md) | 坏数据变空白块 → 用户连复制出来自己看都做不到 |
| 16 | **每档能力都要一条"退化为 Y"** | 先列能力矩阵,再写每一档落点;最差档必须**不静默**(响铃 / 纯文本 / 不激活) | [`1-终端即产品`](./1-终端即产品-dsh-TUI.md) · [`1-薄基座`](./1-薄基座-dock.md) | 缺能力就什么都不做 → 用户当成 bug |
| 17 | **三层否定** | 用户否掉的东西要同时挡住:当前轮次 / 重建路径 / **模型侧记忆** | [`8-协作`](./8-协作-dsh-agent-teams.md) | 只挡一层 → 系统在另一层复活它,用户反复否同一件事 |
| 18 | **外部索引每次使用前再校验** | 规范形式、无凭据、无 fragment、不重复;并配超时/字节上限/`redirect:"error"`/同 URL 合并 | [`5-分发与救生页`](./5-分发与救生页-dsh-market.md) | 只在保存时校验 → settings / 环境变量绕过,schema 形同虚设 |

**三条"别抄"**:

- **[`9-冻结 fork`](./9-冻结fork-better-sidebar-N23.md)**:peer 上界钉死 (`< 0.2.0`) + 改到整个外壳 + 保留上游接口 → 分家是必然结局,而且用户会被推进"降级宿主 / 装回上游"的两难。**带显式上界的 peer 区间 = 主动设了一个死亡日期。**
- **`1-终端即产品`** 的教训:换表层不会让上面的层自动出现,**首启、分发、降级三件事从此归你**。
- **`1-薄基座` 的反面**:用私有 DOM 锚点(`data-turn-navigator`)去挪别人的布局,锚点在 `0.2.1-rc.3` 已 0 命中——**可以这么干,但必须先写"找不到就什么都不做",并且优先找上游已约定好的量(CSS 变量)。**

---

## 3. 怎么读这个目录

文件名是 `N-关键短语-插件名.md`。

**第一位数字就是类别**——不用记对照表，看见 `3-` 就知道是驾驶舱：

| 打头 | 类别 | 这一类的卡问的问题 |
|---|---|---|
| `0` | **本域的门**（口径、七层、命名法） | 什么算样本？七层怎么分？证据怎么标？ |
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

| 卡 | 插件 | ★ / 下载 | 一句话 | **能借鉴什么** |
|---|---|---|---|---|
| [`领域模型`](./0-领域模型-七层与命名约定.md) | — | — | 本域的门：四条口径、七层、编号法、证据级别 | **13 行上游接缝索引**：每层「改得动 / 改不动」以及该挂哪个服务 |
| **`1` 壳与工作台** | | | |
| [`薄基座`](./1-薄基座-dock.md) | `AKS1st/dock` | 未采到 | 只给注册表、不给能力：六个 API + 六个兄弟包 | **一个服务面 + 零内部依赖 + 安装顺序不敏感**；UI 依赖写成可选 peer，缺失时"不激活"；任何隐藏都留两条逃生通道 |
| [`厚工作台`](./1-厚工作台-better-sidebar.md) | `omdsh-dev/DSH-better-sidebar` | 2216 / 39,717 | 一个插件把自己做成 IDE，**自己就是第一个插件** | **一种扩展点形状 + 内置也走它**；原型方法注册表；`ns.v1.sessionId` 持久化 + 引用完整性；"先数扇出点再优化主路由" |
| [`终端即产品`](./1-终端即产品-dsh-TUI.md) | `ccch1mneyyy/dsh-TUI` | 2009 / 16,959 | 换表层 + 自带四步首启，把 DSH 变成另一个应用 | **每档能力一条"退化为 Y"**；输入解析的 hold 窗口(不被延长 + 超界原样重放)；恢复不确定就报错退出；更新只看退出码 |
| **`2` 内容形态** | | | |
| [`生成式界面`](./2-生成式界面-dsh-genui.md) | `omdsh-dev/dsh-genui` | 224 / — | 回复本身变成可操作界面：本地优先、"诚实 UI" | **内容协议当扩展面**；节点级丢弃 + 块级退回原文；同轮纠错；无 `action` 渲染成 disabled；主题只暴露一层变量 |
| **`3` 驾驶舱** | | | |
| [`驾驶舱`](./3-驾驶舱-dsh-context.md) | `bowenliang123/dsh-context` | 416 / 6,612 | 五块面回答"它吃了什么、为什么变笨、钱花在哪" | **同源出数**；估算与真实并列；兼容性写成 `Rule/Limitation/Check/Procedure`；"mirror, don't import" |
| **`4` 上手** | | | |
| [`首启推荐`](./4-首启推荐-dsh-bootstrap.md) | `why-sir/dsh-bootstrap` | 未收录 | 装完第一屏就答"我还该装什么"：计划 + 环境码 | **版本锁不到就跳过**；环境码能表达"保持现状"；读回磁盘自证收敛；失败只损失面板不损失宿主 |
| **`5` 分发** | | | |
| [`分发与救生页`](./5-分发与救生页-dsh-market.md) | `dsh-market/dsh-market` | 1100 / 82,491 | 把发现与安装搬进产品，并给"起不来"留救生页 | **救生页由进程外 helper 在原地址提供**；只给一个决定；外部索引每次使用前校验；自动重启先问"会不会杀死自己" |
| **`6` 多端** | | | |
| [`多端与远程`](./6-多端与远程-dsh-mobile.md) | `saya-ch/dsh-mobile` | — / 5,301 | 手机是**一台要配对的设备**，不是一个断点 | **配对码 + 可撤销(删哈希)+ 回环准入**；二进制供应链四项固定；`purge --yes` 式卸载清理 |
| **`7` 感官与模型** | | | |
| [`感官接入`](./7-感官接入-modlens.md) | `liustack/modlens` | 3152 / 63,829 | 给纯文本模型装上眼睛：粘贴即读、零配置 | **未确认就放过**("absent means unknown")；加元数据条目不换路由；`meta.attempts`/`warnings` 让回退不静默 |
| **`8` 协作** | | | |
| [`8-协作`](./8-协作-dsh-agent-teams.md) | `NanmiCoder/dsh-agent-teams` | 573 / 10,525 | 队长 + 任务 DAG + **执行前计划**，实时活动面板 | **计划先行 + 唯一授权点 + 三层否定**；完成时审计而非写入拦截；磁盘真相并坦白"不跨进程" |
| **`9` 反例** | | | |
| [`9-冻结 fork`](./9-冻结fork-better-sidebar-N23.md) | `All3nCN/dsh-better-sidebar-N23` | 未采到 | 0.1.x 冻结 fork：改得太深就只能分家 | **反食谱**：六条禁令 + 三条正确替代(只下界 + CI 矩阵 / 换接缝 / 别 fork) |

---

## 4.1 样本坐标总表(要精确复现/再深挖,从这里开始)

**每个样本都必须能被一句话定位**:repo 在哪、npm 叫什么、目录条目是哪个文件、装法是什么、本域已经挖到哪、还有哪里没挖。缺任何一列,这张卡就不算可复现。

| 卡 | repo | npm 包名 | 目录条目(`data/plugins/…`) | 装法(0.2.x) | 已挖 | 未挖/待深挖 |
|---|---|---|---|---|---|---|
| [`厚工作台`](./1-厚工作台-better-sidebar.md) | `omdsh-dev/DSH-better-sidebar` | `dsh-better-sidebar` | `omdsh-dev__DSH-better-sidebar.yml` (`ui`) | `dsh plugin --profile web add dsh-better-sidebar@latest` | `_证据/1-壳与工作台-原始挖掘.md` §一 | 版本对照表全表、`CHANGELOG`、`ctx.betterSidebar` 类型声明 |
| [`薄基座`](./1-薄基座-dock.md) | `AKS1st/dock` | `dock-base` + 兄弟包 `dock-files`/`dock-editor`/`dock-images`/`dock-markdown`/`dock-git`/`dock-spreadsheet` | `AKS1st__dock.yml` + `AKS1st__dock-*.yml` (`ui`) | `dsh plugin --profile web add dock-base` 后逐条装 | `_证据/1-壳与工作台-原始挖掘.md` §二 | 仓库 `src/client/contract.ts`、0.2.x 实测(本卡 `[OPEN]`) |
| [`终端即产品`](./1-终端即产品-dsh-TUI.md) | `ccch1mneyyy/dsh-TUI` | `@deepseek-harness-tui/dsh-tui`(全局 CLI) | `ccch1mneyyy__dsh-TUI.yml` (`ui`) | Windows 安装器;或 `npm i -g @deepseek-ai/dsh @deepseek-harness-tui/dsh-tui` 后 `dsh-tui`;**别用 git URL 装** | `_证据/1-壳与工作台-原始挖掘.md` §三 | `compatibility.json`、52 条降级里未展开的协议细节 |
| [`生成式界面`](./2-生成式界面-dsh-genui.md) | `omdsh-dev/dsh-genui`(npm scope 是 `@changfenhuang`) | `@changfenhuang/dsh-genui` | `omdsh-dev__dsh-genui.yml` (`ui`) | `dsh plugin --profile web add @changfenhuang/dsh-genui` | 本轮直接读 README 全文(429 行),行号已内联 | **`SKILL.md` 字段级 schema**、`docs/map.md`、action payload 信封 |
| [`驾驶舱`](./3-驾驶舱-dsh-context.md) | `bowenliang123/dsh-context` | `dsh-context` | `bowenliang123__dsh-context.yml` (`usage`) | GUI Add plugin,或 `dsh plugin --profile web add dsh-context` | 本轮直接读 README 全文(237 行)+ 上游 `dsh-token-meter` 源码 | git tag `v0.78.2` 快照、`docs/compatibility.md`、`docs/model-pricing-mapping.md` 与页脚两行 **0.2.2-alpha.2** 核实 |
| [`首启推荐`](./4-首启推荐-dsh-bootstrap.md) | `why-sir/dsh-bootstrap` | 未采到 | `why-sir__dsh-bootstrap.yml` (`market`;**无 ★/下载计量**) | 目录内名称 `why-sir/dsh-bootstrap` | `_证据/4-5-首启与分发-原始挖掘.md` §一 | npm 包名、其目录快照的生成时间锚(2026-10-16) |
| [`分发与救生页`](./5-分发与救生页-dsh-market.md) | `dsh-market/dsh-market` | `dshmarket`(商店内显示 **Plugin Market**) | `dsh-market__dsh-market.yml` (`market`) | Desktop:Settings→Plugins;web:`dsh plugin --profile web add dshmarket` | `_证据/4-5-首启与分发-原始挖掘.md` §二 + §四 | issue #227/#139 原文、救生页 HTML 的实际实现 |
| [`多端与远程`](./6-多端与远程-dsh-mobile.md) | `saya-ch/dsh-mobile` | `dsh-mobile`(+ Android App) | `saya-ch__dsh-mobile.yml` (`remote`) | 见卡 §3.1(Android App / 浏览器两条路) | `_证据/6-7-移动与视觉-原始挖掘.md` §一 | `compat.js` 的语法下限实测(Chromium 92 那档 `[OPEN]`) |
| [`感官接入`](./7-感官接入-modlens.md) | `liustack/modlens` | `@liustack/modlens` | `liustack__modlens.yml` (`vision`) | `npx -y @deepseek-ai/dsh plugin --profile web add @liustack/modlens@3.27.2` | `_证据/6-7-移动与视觉-原始挖掘.md` §二 | 六个引擎各自的质量差异、`docs/security.md` 全文 |
| [`协作`](./8-协作-dsh-agent-teams.md) | `NanmiCoder/dsh-agent-teams` | `@nanmicoder/dsh-agent-teams` | `NanmiCoder__dsh-agent-teams.yml` (`workflow`) | Plugins→Add plugin 填 `github:NanmiCoder/dsh-agent-teams` | 本轮直接读 README + `compatibility.json` + manifest | **三层否定的实现方式**(会话状态还是提示词)、`<workspace>/.agent-teams/` 实际文件格式 |
| [`冻结 fork`](./9-冻结fork-better-sidebar-N23.md) | `All3nCN/dsh-better-sidebar-N23` | `@all3cn/dsh-better-sidebar-n23` | `All3nCN__dsh-better-sidebar-N23.yml` (`ui`) | **0.2.x 上装不上**(安装期 `incompatible-version`) | 目录条目 + upstream README 对照 | 同作者 `dsh-qa-suite-N23`;强行 `allow-version` 豁免后的实际表现 |

**三条读这张表的规矩**:

1. **repo 与 npm 包名经常不同**(`omdsh-dev/dsh-genui` ↔ `@changfenhuang/dsh-genui`;`dsh-market/dsh-market` ↔ `dshmarket`)。只写一个,别人就装不上或 clone 不到。
2. **目录条目文件名是 `owner__repo.yml`**,可直接 `cat data/plugins/<该文件>` 取到官方 `url` / `name` / `category` / 双语描述 —— 这是**最省事的二次核实入口**。
3. **"已挖"那一列只写文件与节号**,不写人头结论;要复核任何 `[DSH]` / `[CAT]` 标注,先到这里找到原文,再去 `_证据/` 对行号。

---

## 5. 边界

**收**：兼容 `0.2.x`、改变了**人怎么用它**（入口 / 首屏 / 默认值 / 身份 / 界面 / 分发 / 上手路径）、有可复核的影响力证据。

**不收**：纯能力增强（多一个工具、多一个 provider）、只支持 `0.1.x` 的样本、目录里查不到也拿不到任何计量的条目（除非机制独特且写明理由）。

**不碰**：上游代码本身的建议（那属于 `lever-cross-boundary` / `lever-draw-limit` / `lever-prove-output` 三个域）；本域只写"下游用上游装出了什么"。

**共享文件只读**：`00-map.md`、`horizon.md`、`leverage/README.md`、`data/` 由别的会话维护，本域只调用、不写。

---

## 6. 计量口径

- ★ / npm 下载：`data/stars.json` / `data/downloads.json`，**快照 2026-08-19**；值形如 `{url: {stars|downloads, checkedAt}}`。
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
- [ ] `4` 类第二张：安装器 / 向导候选未探；`dsh-bootstrap` 是目录外样本，说明这类可能被目录系统性漏掉
- [ ] 口径外产品（桌面壳 `dataelement/dsh-desktop` 16,969★、`dsh-tauri` 3,379★）是否单独成 `5`/`6` 类卡
- [ ] `9` 类可能还有第二张：被证伪 / 停更的高星样本，统一成"证伪记录"格式
