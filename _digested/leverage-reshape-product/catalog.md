---
title: "catalog · 产品线全量文件"
domain: reshape-product
kind: index
positioning: "产品线 32 份文件的 kind、定位、能拿走什么、什么时候读（随文件手工维护）。"
read_when: "想一次看全产品线所有文件，或按关键词找入口。"
status: living
updated: 2026-10-31
---
# catalog · 产品线全量文件

> **手工维护。** 新增 / 改名文件时补一行；数量不在这里统计。
> **入口顺序**：[README](./README.md)（怎么读）→ [00_map](./00_map.md)（规矩）→ [01_领域模型](./01_领域模型-七层与命名约定.md)（门）→ 三个 lever 各自的 README；本文件是**全量清单**，找文件时用。

## 产品线的三个 lever

| lever | 收什么 | 卡数 | 入口 |
|---|---|---|---|
| `plugin/` | 装进任何 profile 的客人 | 9 | [README](./plugin/README.md) |
| `profile/` | 一套 bundle 装进 profile，浏览器启动 | 4 | [README](./profile/README.md) |
| `shell/` | 换表层 / 自带宿主 | 6 | [README](./shell/README.md) |

## 共用件

| 文件 | kind | 定位 | 能拿走什么 | 什么时候读 | 状态 |
|---|---|---|---|---|---|
| [`00_map.md`](./00_map.md) | charter | **单一规则源**：目录、命名、frontmatter、证据、影响力口径、维护流程、反模式。 | 一张目录树 + 命名规则 + 维护动作表。 | 要新增/改名/合并文件；或口径冲突时。 | living |
| [`01_领域模型-七层与命名约定.md`](./01_领域模型-七层与命名约定.md) | charter | **三个 lever 共用**的门：C1–C4 口径、产品七层、编号法、13 行上游接缝索引。 | 13 行接缝表：每层上游保证什么、不保证什么。 | 判断改动落在第几层；抄任何卡之前先查接缝语义。 | living |
| [`02_公共产出-18条.md`](./02_公共产出-18条.md) | guide | 三个 lever 的公共产出：18 条可搬走的产品规则 + 三条"别抄"。 | 18 条 + 每条出处 + 抄错后果。 | 只读一节就走；或评审方案时逐条对照。 | observed |
| [`README.md`](./README.md) | index | 产品线入口：三条路线怎么分工、为什么和 leverage 平级。 | 路线选择表 + 影响力门槛 + 读法。 | 第一次进产品线；或不确该看哪个 lever。 | living |
| [`catalog.md（本文件）`](./catalog.md) | index | 全量文件清单（手工维护）。 | — | 想一次看全，或按关键词找。 | living |

### `plugin/` · 通用插件（9）

| 文件 | kind | 定位 | 能拿走什么 | 什么时候读 | 状态 |
|---|---|---|---|---|---|
| [`README.md`](./plugin/README.md) | charter | **插件侧宪章**：只收能 `dsh plugin --profile <任意> add` 的 0.2.x 样本；一卡一插件，卡卡要交借鉴食谱。 | 9 个插件样本的七层坐标 + 一张可照抄的接缝表。 | 要装配件；或判断一个插件是「厚客人」还是「宿主」。 | observed |
| [`11_薄基座-dock.md`](./plugin/11_薄基座-dock.md) | sample | `AKS1st/dock`：只给注册表、不给能力的工作台基座，六个 API + 六个兄弟包。 | 服务面 + 零内部依赖 + 可选 peer；隐藏要留一条与被隐藏物无关的逃生口。 | 要做平台型外壳/注册表；或要接别人的布局又不想改它。 | observed |
| [`12_厚工作台-better-sidebar.md`](./plugin/12_厚工作台-better-sidebar.md) | sample | `omdsh-dev/DSH-better-sidebar`：一个插件把自己做成 IDE，且内置功能也走自己的扩展点。 | 一种扩展点形状 + 内置也走它；原型方法注册表；版本前缀 key + 引用完整性。 | 要做厚工作台/多面板 IDE；或要设计第三方可扩展的注册表。 | observed |
| [`21_生成式界面-dsh-genui.md`](./plugin/21_生成式界面-dsh-genui.md) | sample | `omdsh-dev/dsh-genui`：把回复本身变成可操作界面，用内容协议当扩展面。 | 内容协议当扩展面；节点级丢弃 + 块级退回原文；无 action 渲染成 disabled。 | 要让模型输出可交互组件；或要设计容错的内容协议。 | observed |
| [`31_驾驶舱-dsh-context.md`](./plugin/31_驾驶舱-dsh-context.md) | sample | `bowenliang123/dsh-context`：把上下文、成本、编队做成可读可归因的五块面。 | 同源出数；估算与真实并列；兼容性写成 Rule/Limitation/Check/Procedure。 | 要做用量/成本/上下文面板；或要避免面板数字与用户已知数字打架。 | observed |
| [`41_首启推荐-dsh-bootstrap.md`](./plugin/41_首启推荐-dsh-bootstrap.md) | sample | `why-sir/dsh-bootstrap`：装完第一屏回答「我还该装什么」，用计划 + 环境码。 | 版本锁不到就跳过；环境码未包含 = 保持现状；写完读回磁盘自证。 | 要做首启/推荐/一键配置；或要设计可导入导出的环境配置。 | observed |
| [`51_分发与救生页-dsh-market.md`](./plugin/51_分发与救生页-dsh-market.md) | sample | `dsh-market/dsh-market`：把发现与安装搬进产品，并给「起不来」留救生页。 | 救生页活在插件栈外；界面只做一个决定；外部索引每次使用前再校验。 | 要做分发/市场/安装器；或要设计「装坏了怎么回」。 | observed |
| [`61_多端与远程-dsh-mobile.md`](./plugin/61_多端与远程-dsh-mobile.md) | sample | `saya-ch/dsh-mobile`：把手机当一台要配对的设备，用回环上游 + 独立 HTTPS 网关。 | 配对码 + 可撤销（删哈希）+ 回环准入；撤销与显示解耦。 | 要做多端/远程访问；或要给会话开一个网络入口。 | observed |
| [`71_感官接入-modlens.md`](./plugin/71_感官接入-modlens.md) | sample | `liustack/modlens`：给纯文本模型装上眼睛，粘贴即读、零配置。 | 未确认就放过；加元数据条目而不换路由；attempts/warnings 让回退不静默。 | 要补模型能力缺口（视觉/语音/搜索）；或要接管别人的路由而不改它。 | observed |
| [`81_协作-dsh-agent-teams.md`](./plugin/81_协作-dsh-agent-teams.md) | sample | `NanmiCoder/dsh-agent-teams`：把多代理变成一张可批准的计划，队长 + 任务 DAG + 磁盘真相。 | 计划先行 + 唯一授权点 + 三层否定；完成时审计而非写入拦截。 | 要做团队/编排 UI；或要设计「人批准后才开跑」的交互。 | observed |
| [`1-01_壳与工作台-原始挖掘.md`](./plugin/_证据/01_壳与工作台-原始挖掘.md) | evidence | 三张壳卡（better-sidebar / dock / dsh-TUI）的原始摘录与上游行号，只作溯源。 | — | 要核对壳类卡片的 [DSH]/[CAT] 原文；或重挖这三个样本。 | observed |
| [`4-5-02_首启与分发-原始挖掘.md`](./plugin/_证据/02_首启与分发-原始挖掘.md) | evidence | dsh-bootstrap 与 dsh-market 的原始摘录，含 A/B 两档证据强度标注。 | — | 要核对首启/分发卡片的原文与行号。 | observed |
| [`6-7-03_移动与视觉-原始挖掘.md`](./plugin/_证据/03_移动与视觉-原始挖掘.md) | evidence | dsh-mobile 与 modlens 的原始摘录与上游行号。 | — | 要核对多端/感官卡片的原文与行号。 | observed |

### `profile/` · profile 即产品（4）

| 文件 | kind | 定位 | 能拿走什么 | 什么时候读 | 状态 |
|---|---|---|---|---|---|
| [`README.md`](./profile/README.md) | charter | **profile 侧宪章**：发货单位是 bundle；装成功 ≠ 挂载成功；四种聚合形态与影响力门槛。 | 必抄 6 条 + 四种形态对照 + 为什么这一桶天然薄。 | 要做发行版/全家桶；或判断该发插件、发 profile 还是发应用。 | observed |
| [`11_全家桶-dsh-web.md`](./profile/11_全家桶-dsh-web.md) | sample | `zhu1090093659/dsh-web`（★ 9,865 / npm 月下载 99,694）：20+ bundle 装进 web profile 的浏览器级产品。 | 聚合包 id 前缀；静默半挂载；共存治理；默认皮肤即身份。 | 要做 profile 级产品；或要设计聚合包与安装自证。 | observed |
| [`12_界面套件-dsh-codex-ui.md`](./profile/12_界面套件-dsh-codex-ui.md) | sample | `MichengAI/dsh-codex-ui`（npm 月下载 119,610 / ★ 250）：六个微内核子插件重做整套 Web 界面。 | fail-closed 清理（0 DOM）；只吃官方 primitive/slot；1.x 覆盖式美化的三条死因。 | 要做整屏界面套件；或要避免主题/布局的半降级。 | observed |
| [`13_组合包-dsh-suite.md`](./profile/13_组合包-dsh-suite.md) | sample | `STARDUSTLC666/dsh-suite`（npm 月下载 8,230）：18 个独立插件 + 共享默认配置 + 固定版本。 | 组合包卖的是策展；固定组件版本；扁平化无 git 子依赖；整包更新。 | 要把自己的多个插件打包成一件交付。 | observed |
| [`14_聚合补丁-dsh-all.md`](./profile/14_聚合补丁-dsh-all.md) | sample | `hyzyn/dsh-plugin-kit`（npm 月下载 3,558 / ★ 59）：一条 bundle patch 挂 11 个插件，自带 Profile 管理卡片。 | 聚合包应是纯数据；共享库不进 bundles；分面表回答「装完会变什么」。 | 要做聚合包/全家桶；或要理解 bundle patch 怎么落地。 | observed |
| [`_证据/01_产品聚合-原始挖掘.md`](./profile/_证据/01_产品聚合-原始挖掘.md) | evidence | profile/bundle 的上游语义、dsh-web 原文、7,924 条普查的召回与剔除。 | — | 要核对 profile 侧卡片的原文；或重跑「谁是 profile 级产品」的普查。 | observed |

### `shell/` · 自带宿主（6）

| 文件 | kind | 定位 | 能拿走什么 | 什么时候读 | 状态 |
|---|---|---|---|---|---|
| [`README.md`](./shell/README.md) | charter | **宿主侧宪章**：换掉表层后首启/分发/降级为什么必须自己补；六条样本、四条路线，以及 `desktop` profile 被独占那条接缝。 | 规律 A 的代价清单 + 宿主侧必抄 9 条。 | 要换表层做独立应用；或判断一个插件该不该分家。 | observed |
| [`14_终端即产品-dsh-TUI.md`](./shell/14_终端即产品-dsh-TUI.md) | sample | `ccch1mneyyy/dsh-TUI`：换表层并把首启、降级、更新一起接管的终端产品。 | 每档能力一条「退化为 Y」；hold 窗口不被延长；恢复不确定就报错退出。 | 要换表层做独立应用；或要设计降级链与首启向导。 | observed |
| [`15_终端工作区-seektty.md`](./shell/15_终端工作区-seektty.md) | sample | `Hilbert-beinghappy/seektty`：终端表层，Harness 仍拥有运行时状态；自带 profile 与 self-first 更新器。 | 三档兼容 + 未知 fail closed；pnpm GVS 局部适配；原生 scrollback 模式。 | 要做终端表层；或要设计壳自带更新器。 | observed |
| [`11_桌面应用-dsh-desktop.md`](./shell/11_桌面应用-dsh-desktop.md) | sample | `dataelement/dsh-desktop`（16,975★）：签名安装包 + Safe Mode + 六小时更新检查的桌面发行版。 | Safe Mode 只挂官方 bundle；`--safe-mode` 逃生；更新先问再装；随机回环 + 独立配对桥。 | 要做桌面发行版/安装器/安全模式。 | observed |
| [`12_单文件桌面壳-windowos.md`](./shell/12_单文件桌面壳-windowos.md) | sample | `RAFOLIE/dsh-desktop-windowos`：4.5 MB 裸 exe，五跳候选链 + 监护自愈 + 升级回滚。 | 每跳独立就绪窗口；进程三态所有权；AUMID；连续崩溃熔断。 | 要做便携壳/托盘应用；或要设计找不到 dsh 时的路径。 | observed |
| [`13_内置运行时-tauriapp.md`](./shell/13_内置运行时-tauriapp.md) | sample | `hyperion2144/dsh-desktop-tauriapp`：Node sidecar + dsh 依赖树随包分发，运行时可在应用内换版本。 | 连接级健康探测；自愈 3 次封顶 + 2 分钟重置；局部注入 chrome。 | 要做零前置依赖的桌面壳；或要设计运行时版本管理。 | observed |
| [`91_冻结分叉-better-sidebar-N23.md`](./shell/91_冻结分叉-better-sidebar-N23.md) | sample | `All3nCN/dsh-better-sidebar-N23`：0.1.x 冻结 fork，用一次失联证明「改得太深就只能分家」。 | 反食谱：peer 上界 = 死亡日期；只写下界 + CI 矩阵，或换接缝，别 fork。 | 想 fork 上游；或要判断一个深改插件的升级风险。 | observed |
| [`_证据/01_桌面与终端-原始挖掘.md`](./shell/_证据/01_桌面与终端-原始挖掘.md) | evidence | 四份宿主侧样本的 README 摘录、上游 `desktop` profile 接缝行号、取数时点。 | — | 要核对桌面壳/终端工作区卡片的原文；或重挖这四个样本。 | observed |
