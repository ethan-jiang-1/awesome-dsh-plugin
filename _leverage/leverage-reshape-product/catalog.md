---
title: "catalog · 产品线全量文件"
domain: reshape-product
kind: index
positioning: "产品线 Markdown 文件与指标快照的 kind、定位、能拿走什么、什么时候读（随文件手工维护）。"
read_when: "想一次看全产品线所有文件，或按关键词找入口。"
status: living
updated: 2026-10-31
---
# catalog · 产品线全量文件

> **手工维护。** 新增 / 改名文件时补一行；数量不在这里统计。
> **入口顺序**：[README](./README.md)（怎么读）→ [00-map](./00-map.md)（规矩）→ [horizon](./horizon.md)（门）→ 三个 lever 各自的 README；本文件是**全量清单**，找文件时用。

## 产品线的三个 lever

| lever | 收什么 | 卡数 | 入口 |
|---|---|---|---|
| `plugin/` | 装进任何 profile 的客人 | 11 | [README](./plugin/README.md) |
| `profile/` | 一套 bundle 装进 profile，浏览器启动 | 8 | [README](./profile/README.md) |
| `shell/` | 换表层 / 自带宿主 | 6 | [README](./shell/README.md) |

## 共用件

| 文件 | kind | 定位 | 能拿走什么 | 什么时候读 | 状态 |
|---|---|---|---|---|---|
| [`README.md`](./README.md) | index | 产品线入口：三个入口、三条路线怎么分工、文件和证据约定。 | 路线选择表 + 影响力门槛 + 读法。 | 第一次进产品线；或不确该看哪个 lever。 | living |
| [`RESEARCH.md`](./RESEARCH.md) | guide | 固定版本、主张分源、数据/状态/失败路径研究、七列表洞察与 BORROW 准入规程；规定逐卡流程并优先推进 profile 桶。 | 可复用的研究步骤、证据标记、洞察质量门与 profile 逐篇队列。 | 新增/复核样本卡，或判断一条洞察能否进 BORROW。 | living |
| [`00-map.md`](./00-map.md) | charter | **单一规则源**：目录、命名、frontmatter、证据、影响力口径、维护流程、反模式。 | 一张目录树 + 命名规则 + 维护动作表。 | 要新增/改名/合并文件；或口径冲突时。 | living |
| [`horizon.md`](./horizon.md) | charter | **三个 lever 共用**的门：C1–C4 口径、产品七层、卡片编号、13 行上游接缝索引。 | 13 行接缝表：每层上游保证什么、不保证什么。 | 判断改动落在第几层；抄任何卡之前先查接缝语义。 | living |
| [`BORROW.md`](./BORROW.md) | guide | 跨 lever 借用总入口：按需求路由 + 22 条可搬走规则 + 三条"别抄"。 | 22 条 + 每条出处 + 抄错后果；6 条需求路由。 | 只读一节就走；或评审方案时逐条对照。 | observed |
| [`BACKLOG.md`](./BACKLOG.md) | index | 候选池：过了门槛待深挖的、和没过门槛的，各留一行。 | 少走弯路：某产品为什么还没成卡。 | 要补新样本；或想知道某产品为什么没卡。 | living |
| [`catalog.md（本文件）`](./catalog.md) | index | 全量文件清单（手工维护）。 | — | 想一次看全，或按关键词找。 | living |
| [`_证据/指标快照-2026-10-31.json`](./_证据/指标快照-2026-10-31.json) | evidence | 25 张正式卡 + 1 个观察样本（26 个条目）的 ★ / forks / issues / npm 月下载原始响应（跨 lever 共用，可复算）。 | 复算卡片影响力数字；核对取数时点与口径。 | 引用或更新任何卡片指标前。 | observed |

### `plugin/` · 通用插件（11）

| 文件 | kind | 定位 | 能拿走什么 | 什么时候读 | 状态 |
|---|---|---|---|---|---|
| [`README.md`](./plugin/README.md) | charter | **插件侧宪章**：只收能 `dsh plugin --profile <任意> add` 的 0.2.x 样本；一卡一插件，卡卡要交借鉴食谱。 | 11 个插件样本的七层坐标 + 一张可照抄的接缝表。 | 要装配件；或判断一个插件是「厚客人」还是「宿主」。 | observed |
| [`11_薄基座-dock.md`](./plugin/11_薄基座-dock.md) | sample | `dock-base@0.2.4` 固定于 `AKS1st/dock` tag/commit；typed workbench service、registration disposal、browser-global localStorage stores、与 sibling dependency boundary。 | state 无 session/profile partition；invalid settings values may default-and-persist；optional React absence 和 dock-files sandbox 未验证；tarball byte equivalence/RUN 未做。 | 要设计 plugin family service contract、registry lifecycle、setting persistence scope 和 optional UI peers。 | observed |

| [`12_厚工作台-better-sidebar.md`](./plugin/12_厚工作台-better-sidebar.md) | sample | `omdsh-dev/DSH-better-sidebar`：一个插件把自己做成 IDE，且提供显式 disposer 的扩展注册表。 | 注册生命周期由调用方持有；每会话布局隔离与局部 sanitize；按 session 合并冷元数据读取。 | 要做厚工作台/多面板 IDE；或要设计可注销的第三方注册表。 | observed |
| [`21_生成式界面-dsh-genui.md`](./plugin/21_生成式界面-dsh-genui.md) | sample | Pinned source `omdsh-dev/dsh-genui@0.15.0`：DOM `dsh-ui` fence observer renders assistant content; historical npm artifact provenance remains unresolved. | Bounded source reference for schema/partial fallback; DOM observer is not native fence slot; action is not authorization; no sandbox/CSP proven. | 要设计生成式内容协议、流式 renderer lifecycle、action trust boundary 与异步资源 fallback。 | observed |
| [`08_生成式界面-dsh-genui-源码复核.md`](./plugin/_证据/08_生成式界面-dsh-genui-源码复核.md) | evidence | 固定仓库提交 `e00bdcf…`，区分目标 source version `0.15.0`、未对齐的 npm artifact、DSH rc.3 contract、schema/DOM/action tests、CI workflow 与无 RUN。 | 防止 README/测试名称被升格为安全、权限、幂等、通用fallback或兼容保证；点明 DOM observer 非 host native fence slot。 | 复核 plugin `dsh-genui` 协议、渲染生命周期与 action trust boundary。 | observed |
| [`07_薄基座-dock-源码复核.md`](./plugin/_证据/07_薄基座-dock-源码复核.md) | evidence | 固定 `dock-base@0.2.4` 到 tag/source commit/npm gitHead；复核 workbench API/disposal、global store scope/failure behavior、optional peer discrepancy 与 DSH rc.3 layout contract。 | SRI metadata 已记录但 tarball 未字节比对；sibling filesystem auth、React absence、real host cleanup 均 OPEN；无 CI/RUN。 | 复核 plugin/11；设计 service ownership, store scope, and disposable registration lifecycle。 | observed |


| [`31_驾驶舱-dsh-context.md`](./plugin/31_驾驶舱-dsh-context.md) | sample | `bowenliang123/dsh-context@0.78.2` 固定到 tag/commit：不调 tokenMeter 服务，读三份宿主投影；四段占用率回退；分类按实测锚定；成本本地估算；价格书第三方。 | 同源≠同精度；锚定后分类不再“不等”；价格书不落盘且部分 route 静默跳过；兼容文档基线是 rc.2 而非 rc.3。 | 设计用量/成本面板的数据 provenance、估算与降级。 | observed |
| [`09_驾驶舱-dsh-context-源码复核.md`](./plugin/_证据/09_驾驶舱-dsh-context-源码复核.md) | evidence | 固定 npm 0.78.2 与 tag/commit 同 SHA；复核投影读取、四级占用率回退与精度差、分类锚定、客户端成本估算与第三方价格书、缺数据降级、兼容文档结构与测试/CI 缺口。 | “同源”不等于同精度/同回退；锚定后分类不再不等；成本是本地估算非账单；价格表第三方且未落盘。 | 复核 plugin/31；设计计量面板的数据 provenance 与降级。 | observed |
| [`42_环境搬家-dsh-config-manager.md`](./plugin/42_环境搬家-dsh-config-manager.md) | sample | `dsh-config-manager` 0.2.x（源码审计 v0.2.3）：计划阶段零配置写入，确认后快照+journal 再逐项 apply；外部来源翻译成标准 bundle v1。 | 自动回滚不含卸载新装插件、收尾写入不在快照；未决冲突只是 UI 门；外部包兼容分被目标机版本拉满；read-failed≠0 仅导出侧成立。 | 设计批量导入的计划/快照/补偿回滚与冲突不变量。 | observed |
| [`10_环境搬家-dsh-config-manager-源码复核.md`](./plugin/_证据/10_环境搬家-dsh-config-manager-源码复核.md) | evidence | 固定 commit `babd759…`（tag v0.2.3）；复核计划/写入边界、快照覆盖、冲突卡点、来源翻译、密钥与 Zip Slip/Symlink、测试与 CI 元数据。 | 版本从卡上 0.2.2 前移；明确哪些回滚是补偿而非原子；密钥/路径安全以源码为准。 | 复核 plugin/42；设计批量写前的计划、快照与回滚。 | observed |
| [`43_会话搬家-dsh-chat-import.md`](./plugin/43_会话搬家-dsh-chat-import.md) | sample | `dsh-chat-import@0.26.3`：33 源/34 格式转成原生 DSH 事件流；预览零写入但只过滤本插件注入。 | failures 仅预览面；path-hint 短路；撤回两条路径且无事务；cwd auto 改写；密钥不脱敏。 | 设计迁移的发现/保真/可撤销。 | observed |
| [`12_会话搬家-dsh-chat-import-源码复核.md`](./plugin/_证据/12_会话搬家-dsh-chat-import-源码复核.md) | evidence | 固定 0.26.3 tag/commit：33 源/34 格式、三级探测与 path-hint 短路、预览零写入与“跳过注入”的真实含义、原生事件流+agents.create、撤回两条路径与无事务回滚。 | cwd auto 改写而非跳过；failures 仅预览面；密钥不脱敏；无 maxTranscriptBytes。 | 复核 plugin/43；设计迁移的预览/撤回/幂等与凭据边界。 | observed |
| [`04_首启观察-dsh-bootstrap.md`](./plugin/_证据/04_首启观察-dsh-bootstrap.md) | evidence | 观察样本：★1 / npm 763 的社区首启插件；保留“推荐+计划+环境码”机制分析，不占卡位。2026-11-01 评估：未过门槛且缺固定版本源码链，保留观察、不升卡。 | 机制参考；升卡条件与不升卡理由。 | 要核对首启机制；或问“它为什么没卡”。 | open |
| [`51_分发与救生页-dsh-market.md`](./plugin/51_分发与救生页-dsh-market.md) | sample | `dshmarket@1.73.6`：恢复页由独立 recovery 进程在回环原端口接管；外部目录无快照。 | supervisor 只认 systemd、显式覆盖优先；写回复用 patch/bundles 且失败不重启；loopback-only。 | 设计分发/崩坏恢复与外部索引信任。 | observed |
| [`13_分发与救生页-dsh-market-源码复核.md`](./plugin/_证据/13_分发与救生页-dsh-market-源码复核.md) | evidence | 固定 `dshmarket@1.73.6`：恢复进程/端口、supervisor 闸门、外部目录无快照、写回 patch/bundles、日志脱敏与 CI 缺口。 | 恢复面是独立进程而非 helper 本身；显式 allowRestart 可覆盖检测；顶层配置被忽略；隧道端口/真实崩溃未测。 | 复核 plugin/51；设计崩溃恢复与索引信任边界。 | observed |
| [`52_装坏自愈-dsh-plugin-health.md`](./plugin/52_装坏自愈-dsh-plugin-health.md) | sample | `dsh-plugin-health@1.1.0`：一次性 home + base-only profile 真启动，再写单条可撤销豁免。 | 预演非沙箱且非真实 profile；base 无 webServer 会误判；runs 默认保留；体外 safe 只加 disabled overlay。 | 设计预演/豁免/回滚与体外救生。 | observed |
| [`14_装坏自愈-dsh-plugin-health-源码复核.md`](./plugin/_证据/14_装坏自愈-dsh-plugin-health-源码复核.md) | evidence | 固定 1.1.0 的 gitHead/tag 父子关系与文档差异；复核一次性 home、base-only `health-smoke`、`runProfile` boot、激活判据、allow-version/install 顺序、回滚与 runs 保留。 | “能启动”仅指 base-only loader 激活；预演非沙箱、runs 默认不清理、Windows 孤儿检测缺口。 | 复核 plugin/52；设计预演/豁免/回滚与体外救生。 | observed |
| [`61_多端与远程-dsh-mobile.md`](./plugin/61_多端与远程-dsh-mobile.md) | sample | `saya-ch/dsh-mobile`：把手机当一台要配对的设备，用回环上游 + 独立 HTTPS 网关。 | 配对码 + 可撤销（删哈希）+ 回环准入；撤销与显示解耦。 | 要做多端/远程访问；或要给会话开一个网络入口。 | observed |
| [`15_多端与远程-dsh-mobile-源码复核.md`](./plugin/_证据/15_多端与远程-dsh-mobile-源码复核.md) | evidence | 固定 0.8.0 provenance/tag/commit 与内容比对；核配对码/限流/撤销、TLS 网关与回环上游、共享 upstream cookie、第三方与自产供应链、purge/health 与测试工件。 | 无按设备分区；APK 只校验大小不校验摘要；health 恒 200；instanceId 随 state 路径变；WS 允许查询串。 | 复核 plugin/61；设计远程配对/网关信任边界。 | observed |
| [`71_感官接入-modlens.md`](./plugin/71_感官接入-modlens.md) | sample | `liustack/modlens`：给纯文本模型装上眼睛，粘贴即读、零配置。 | 未确认就放过；加元数据条目而不换路由；attempts/warnings 让回退不静默。 | 要补模型能力缺口（视觉/语音/搜索）；或要接管别人的路由而不改它。 | observed |
| [`16_感官接入-modlens-源码复核.md`](./plugin/_证据/16_感官接入-modlens-源码复核.md) | evidence | 固定 3.27.2 tarball/commit 一致；核四条图像入口、wrapper takeover 的未知语义、CLI attempts 在 dsh 被丢弃、限额/凭据/测试与 CI 工件。 | README “No hooks/no wrappers” 与源码矛盾；回退在 dsh 面静默；零配置仍需引擎；via 计量未验证。 | 复核 plugin/71；设计感官接入的 metadata-only/回退边界。 | observed |
| [`81_协作-dsh-agent-teams.md`](./plugin/81_协作-dsh-agent-teams.md) | sample | `NanmiCoder/dsh-agent-teams`：把多代理变成一张可批准的计划，队长 + 任务 DAG + 磁盘真相。 | 计划先行 + 唯一授权点 + 三层否定；完成时审计而非写入拦截。 | 要做团队/编排 UI；或要设计「人批准后才开跑」的交互。 | observed |
| [`17_协作-dsh-agent-teams-源码复核.md`](./plugin/_证据/17_协作-dsh-agent-teams-源码复核.md) | evidence | 固定 0.1.28：provenance 绑定 tag/commit、npm 是 CI 重建物；核计划存储/审批、tool 策略、DAG、面板、并发与跨进程边界。 | “三层否定”是可见性/策略不是授权；compatibility.json 是 CI 矩阵非 OS 沙箱；预览通道过时。 | 复核 plugin/81；设计审批/DAG/团队状态并发。 | observed |
| [`01_壳与工作台-原始挖掘.md`](./plugin/_证据/01_壳与工作台-原始挖掘.md) | evidence | 三张壳卡（better-sidebar / dock / dsh-TUI）的原始摘录与上游行号，只作溯源。 | — | 要核对壳类卡片的 [DSH]/[CAT] 原文；或重挖这三个样本。 | observed |
| [`05_上手与修复-原始挖掘.md`](./plugin/_证据/05_上手与修复-原始挖掘.md) | evidence | 三张“装完之后”样本（环境搬家 / 会话搬家 / 装坏自愈）的 README 原文摘录与取数时点。 | — | 要核对 42/43/52 三张卡的原文；或重挖这三个样本。 | observed |
| [`02_首启与分发-原始挖掘.md`](./plugin/_证据/02_首启与分发-原始挖掘.md) | evidence | dsh-bootstrap 与 dsh-market 的原始摘录，含 A/B 两档证据强度标注。 | — | 要核对首启/分发卡片的原文与行号。 | observed |
| [`03_移动与视觉-原始挖掘.md`](./plugin/_证据/03_移动与视觉-原始挖掘.md) | evidence | dsh-mobile 与 modlens 的原始摘录与上游行号。 | — | 要核对多端/感官卡片的原文与行号。 | observed |

| [`06_厚工作台-better-sidebar-源码复核.md`](./plugin/_证据/06_厚工作台-better-sidebar-源码复核.md) | evidence | 对 v0.28.2 固定提交核查扩展注册、布局持久化、cwd 读取、权限边界、测试与 CI；指出旧卡多处机制版本错配。 | 固定版本的一手实现证据与应修正事项。 | 复核 12 号卡的布局状态、注册生命周期、性能结论与 fs 安全边界。 | observed |

### `profile/` · profile 即产品（8）

| 文件 | kind | 定位 | 能拿走什么 | 什么时候读 | 状态 |
|---|---|---|---|---|---|
| [`README.md`](./profile/README.md) | charter | **profile 侧宪章**：发货单位是 bundle；装成功 ≠ 挂载成功；八种形态与影响力门槛。 | 必抄 9 条 + 八种形态对照 + 为什么这一桶天然薄。 | 要做发行版/全家桶；或判断该发插件、发 profile 还是发应用。 | observed |
| [`11_全家桶-dsh-web.md`](./profile/11_全家桶-dsh-web.md) | sample | `zhu1090093659/dsh-web`（★ 9,865 / npm 月下载 99,694）：private root wrapper 汇入公开 aggregate bundle，生成家族 row 装配到 web profile。 | 单一 aggregate manifest、package/row identity 分离、disabled/roster/dependency 状态分层、tombstone family migration。 | 要设计 profile bundle 家族、row 命名空间、family 更新与 profile 自证。 | observed |
| [`12_界面套件-dsh-codex-ui.md`](./profile/12_界面套件-dsh-codex-ui.md) | sample | `@michengai/dsh-codex-ui@2.0.9`，gitHead/source commit 对齐；六个 bundle rows。 | theme probe failure 有局部恢复但 final dispose 不恢复同一 global state；composer probe async 前 activate；theme setting card 的一个 branch 为 null；sidebar/settings skin 仍依赖 DOM/CSS。 | 审查模块化界面生命周期、全局 token cleanup、host DOM coupling 与 DSH peer compatibility。 | observed |
| [`13_组合包-dsh-suite.md`](./profile/13_组合包-dsh-suite.md) | sample | `@stardustlc/dsh-suite@0.9.1`，npm provenance 固定到 `b904373…`：18 exact direct dependencies/patch rows、默认配置与 per-profile updater。 | Direct pins 不冻结 transitive tree；suite defaults 可被 higher patches 覆盖；member update suppression；opt-in stable patch auto-update；失败时补偿恢复有 crash window。 | 设计 curated bundle、profile-scoped updater state/policy 与 package-manager failure recovery。 | observed |
| [`14_聚合补丁-dsh-all.md`](./profile/14_聚合补丁-dsh-all.md) | sample | `@hyzyn/dsh-all@0.1.73`（tag/commit pinned）：12 insert rows 对应 11 exact member dependencies；Profile 管理是独立成员插件。 | 行为由 patch/dependencies 驱动但含 no-op runtime entry；shared kit 是普通传递依赖非 Loader row；Profile CRUD 有 filesystem/process side effects；same-SHA CI 成功但本轮未运行。 | 要做 aggregate package、shared plugin library 边界、安装前 impact matrix 或 profile manager UI。 | observed |
| [`15_接管套件-dsh-plugins-plus.md`](./profile/15_接管套件-dsh-plugins-plus.md) | sample | `sidleo/dsh-plugins-plus@0.2.0` README 描述按 preset 替换 built-in discovery rows；发布包源码 pin 与 GitHub manifest 不一致，暂按概念参考。 | 替换型产品应说明目标 row/scope、继承与恢复语义；具体 planner/rollback/migration 等源码主张保持 OPEN，直至获得匹配发布源码。 | 要设计 preset takeover；或审查不可逆配置合并与发布源码 provenance。 | observed |
| [`16_套件市场-dsh-agent-plugins-market.md`](./profile/16_套件市场-dsh-agent-plugins-market.md) | sample | `Sivan757/dsh-agent-plugins-market`：外部 source checkout 经 adapter/scanner 成为 suite 视图与可启用资源面。 | source refresh 不等于安装 pin；suite install 与 workspace filter 分 scope；credential/OAuth 状态分型；parser/MCP artifact 失败粒度明确；dry-run 非 sandbox。 | 要设计跨生态 catalog、suite 安装、OAuth/MCP credentials、hooks 或受管 checkout ownership。 | observed |
| [`17_闭环装配-better-session.md`](./profile/17_闭环装配-better-session.md) | sample | `@morlay/better-session@0.1.10`：npm tarball 的 exact dependency graph、generated patch rows 和 `session-rdb` SQLite default 可直接复核；GitHub source commit 未能 pin 到该产物。 | 可迁移的是把依赖/rows/default config 一起作为可审阅发布物；README 的 edit/retry/fork 状态机、schema、原子性/副作用安全仍为 DOC/OPEN。 | 设计会话类 bundle、发布行校验和 replay/rewind/fork 的数据事务。 | observed |
| [`18_视觉资产-dsh-wallpaper-engine.md`](./profile/18_视觉资产-dsh-wallpaper-engine.md) | sample | `dsh-plugin-wallpaper-engine@1.4.0` fixed to tag/commit：主包 + 7 个子包与 host/client rows；本版本没有 glass row，better-sidebar 为 optional。 | versioned preset full-snapshot/assets semantics；unsupported Application resources excluded；Scene/Web/WebGL、video transcode and cleanup constraints explicit；no model tool/prompt contract is source-guarded。 | 设计可分发视觉资产、host/render capability matrix、preset schema/assets 与多包渲染资源生命周期。 | observed |
| [`03_视觉资产-原始挖掘.md`](./profile/_证据/03_视觉资产-原始挖掘.md) | evidence | `dsh-wallpaper-engine` 的 README 摘录：壁纸分档、玻璃子包、预设、依赖顺序。 | — | 要核对 18 号卡的原文与出处。 | observed |
| [`02_产品形态-原始挖掘.md`](./profile/_证据/02_产品形态-原始挖掘.md) | evidence | 三张新 profile 样本的 README 原文摘录与取数时点。 | — | 要核对 15/16/17 三张卡的原文；或重挖这三个样本。 | observed |
| [`05_套件市场-dsh-agent-plugins-market-源码复核.md`](./profile/_证据/05_套件市场-dsh-agent-plugins-market-源码复核.md) | evidence | 对 v0.13.0 固定提交复核 source refresh/cache、layout adapters、install/reconcile scope、MCP credentials/OAuth、hooks 和 migration ownership；同 SHA CI run 成功，但本次未执行目标代码。 | 区分 DOC/SRC/TEST/CI/RUN，标出 OAuth 持久条件、validation 粒度、dry-run 非 sandbox 与 state recovery 缺口。 | 复核 profile/16；设计跨生态 suite import、credentials 生命周期与外部资源删除边界。 | observed |
| [`06_接管套件-dsh-plugins-plus-源码复核.md`](./profile/_证据/06_接管套件-dsh-plugins-plus-源码复核.md) | evidence | 对照 npm `0.2.0` registry tarball metadata 与 GitHub `gitHead`；发现其指向 manifest v0.1.8，未能固定匹配 target source。 | 发布 provenance mismatch 与可用 DOC / DSH 通用契约边界；避免误用邻近版本实现。 | 复核 profile/15 的版本身份、接管/回退主张及升级机制参考资格。 | observed |
| [`07_闭环装配-better-session-源码复核.md`](./profile/_证据/07_闭环装配-better-session-源码复核.md) | evidence | 核对 `@morlay/better-session@0.1.10` tarball integrity、exact dependency graph、published patch rows/SQLite config，并记录 GitHub source provenance gap 与 DSH rc.3 契约。 | 区分 release artifact manifest 与 source implementation；将 session schema/lifecycle/tests/CI/safety 保持 OPEN。 | 复核 profile/17；设计 bundle artifact checks 和 session event/replay transaction tests。 | observed |
| [`08_聚合补丁-dsh-all-源码复核.md`](./profile/_证据/08_聚合补丁-dsh-all-源码复核.md) | evidence | 固定 `@hyzyn/dsh-all@0.1.73` 到 tag/commit，复核 generated patch 与 11 成员 exact deps、kit 传递依赖、Profile manager side effects、test/CI/RUN 边界。 | 修正“字面纯数据”与 shared library ownership、insert-only conflict、Profile CRUD 安全断言；记录 same-SHA CI success 和本地 no-run。 | 复核 profile/14；设计 aggregate generator parity、duplicate install guard 与 Profile filesystem safety。 | observed |
| [`09_组合包-dsh-suite-源码复核.md`](./profile/_证据/09_组合包-dsh-suite-源码复核.md) | evidence | 通过 npm SLSA provenance 将 `@stardustlc/dsh-suite@0.9.1` tarball digest 绑定到 commit `b904373…`；核验 18 exact deps/rows/defaults、profile updater policy/state、补偿恢复、tests 与 same-SHA CI。 | 区分 direct pin 与完整 reproducibility；Updater 按 profile、需 consent/idle gates；rollback 非原子，crash 仍可能留 partial state。 | 复核 profile/13；实现 bundle updater ownership、profile-scoped prefs 与 package transaction recovery。 | observed |
| [`10_界面套件-dsh-codex-ui-源码复核.md`](./profile/_证据/10_界面套件-dsh-codex-ui-源码复核.md) | evidence | 固定 npm `2.0.9` 至 gitHead/source commit；追六个 rows、theme/composer/sidebar lifecycle、settings card branch、Slot/DOM mix、tests 与 Node 22/24 CI。 | 区分 failure-probe restore 与 final dispose；指出 async composer activation、局部 0 DOM 和未验证的真实 host cleanup。 | 复核 profile/12；审查界面插件副作用 owner、probe timing、final cleanup 与宿主 DOM selector 兼容。 | observed |
| [`11_视觉资产-dsh-wallpaper-engine-源码复核.md`](./profile/_证据/11_视觉资产-dsh-wallpaper-engine-源码复核.md) | evidence | 固定 npm `1.4.0` 与 GitHub v1.4.0 tag/commit；核主+7 packages/rows、无 glass row、optional sidebar、Scene/Web/video、preset assets/migration 与 zero-token contract；区分 tests、same-SHA CI 与无 RUN。 | 修正旧卡 glass 子包、better-sidebar hard-dep、预设跨版本迁移和“降级即不黑屏”过度断言。 | 复核 profile/18；设计视频/场景资源 budget、preset snapshot/assets ownership、profile teardown。 | observed |
| [`_证据/01_产品聚合-原始挖掘.md`](./profile/_证据/01_产品聚合-原始挖掘.md) | evidence | profile/bundle 的上游语义、dsh-web 原文、7,924 条普查的召回与剔除。 | — | 要核对 profile 侧卡片的原文；或重跑「谁是 profile 级产品」的普查。 | observed |
| [`04_全家桶-dsh-web-源码复核.md`](./profile/_证据/04_全家桶-dsh-web-源码复核.md) | evidence | 对 v0.4.13 固定提交复核聚合事实源、patch 生成、依赖/row 身份、启停/更新、迁移兼容与 CI。 | dsh-web 版本化的一手装配链与行为边界。 | 复核 11 号 profile 卡；或设计 bundle 聚合、行命名空间、停用默认与升级迁移。 | observed |

### `shell/` · 自带宿主（6）

| 文件 | kind | 定位 | 能拿走什么 | 什么时候读 | 状态 |
|---|---|---|---|---|---|
| [`README.md`](./shell/README.md) | charter | **宿主侧宪章**：换掉表层后首启/分发/降级为什么必须自己补；六条样本、四条路线，以及 `desktop` profile 被独占那条接缝。 | 规律 A 的代价清单 + 宿主侧必抄 9 条。 | 要换表层做独立应用；或判断一个插件该不该分家。 | observed |
| [`14_终端即产品-dsh-TUI.md`](./shell/14_终端即产品-dsh-TUI.md) | sample | `ccch1mneyyy/dsh-TUI`：换表层并把首启、降级、更新一起接管的终端产品。 | 每档能力一条「退化为 Y」；hold 窗口不被延长；恢复不确定就报错退出。 | 要换表层做独立应用；或要设计降级链与首启向导。 | observed |
| [`15_终端工作区-seektty.md`](./shell/15_终端工作区-seektty.md) | sample | `Hilbert-beinghappy/seektty`：终端表层，Harness 仍拥有运行时状态；自带 profile 与 self-first 更新器。 | 三档兼容 + 未知 fail closed；pnpm GVS 局部适配；原生 scrollback 模式。 | 要做终端表层；或要设计壳自带更新器。 | observed |
| [`07_终端工作区-seektty-源码复核.md`](./shell/_证据/07_终端工作区-seektty-源码复核.md) | evidence | 固定 v1.3.0/`42a2a7f` 与 npm 1.3.0：核进程内表层（无 Web 服务/端口）、上游 peer 闸门、pnpm 11 局部适配、原生 tail opt-in、self-first 更新与无回滚、teardown。 | 默认 update 实为 auto；0.2.1-rc.3 上精确 peer 被拒；兼容区间退化为单 pin；预设与工具表由 bundle 自建；CI 只钉 0.2.0-rc.2。 | 复核 shell/15；设计终端表层的版本闸门/GVS/teardown。 | observed |
| [`11_桌面应用-dsh-desktop.md`](./shell/11_桌面应用-dsh-desktop.md) | sample | `dataelement/dsh-desktop`（16,975★）：签名安装包 + Safe Mode + 六小时更新检查的桌面发行版。 | Safe Mode 只挂官方 bundle；`--safe-mode` 逃生；更新先问再装；随机回环 + 独立配对桥。 | 要做桌面发行版/安装器/安全模式。 | observed |
| [`04_桌面应用-dsh-desktop-源码复核.md`](./shell/_证据/04_桌面应用-dsh-desktop-源码复核.md) | evidence | 固定 HEAD/tag 与宿主 rc.3+patch-package：核 DSH_HOME/profile 归属、`web` 启动参数、desktop 保留名闸门、Safe Mode profile、更新/恢复/进程面；记录 tag↔manifest 对不上与未读文件。 | “第三方壳占用 desktop”不成立（它自建 DSH_HOME+web）；发行版 CLI ≠ npm rc.3；签名/公证实态未核。 | 复核 shell/11；设计桌面壳的 profile/恢复/更新边界。 | observed |
| [`12_单文件桌面壳-windowos.md`](./shell/12_单文件桌面壳-windowos.md) | sample | `RAFOLIE/dsh-desktop-windowos`：约 4.8 MiB（5,078,016 B）裸 exe，五跳候选链 + 监护自愈 + 升级回滚。 | 每跳独立就绪窗口；进程三态所有权；AUMID；连续崩溃熔断。 | 要做便携壳/托盘应用；或要设计找不到 dsh 时的路径。 | observed |
| [`06_单文件桌面壳-windowos-源码复核.md`](./shell/_证据/06_单文件桌面壳-windowos-源码复核.md) | evidence | 固定 v1.6.72 HEAD：裸 exe 内嵌 WebView，iframe 外部 dsh web；核五跳探测、附加/重启杀端口、单实例、熔断、更新无签名与通知条件。 | 不 pin DSH、无 CI/CD 签名；就绪是端点梯子；重启会杀任意 3080 监听者；无自动回滚。 | 复核 shell/12；设计便携壳的探测/所有权/更新边界。 | observed |
| [`13_内置运行时-tauriapp.md`](./shell/13_内置运行时-tauriapp.md) | sample | `hyperion2144/dsh-desktop-tauriapp`：Node sidecar + dsh 依赖树随包分发，运行时可在应用内换版本。 | 连接级健康探测；自愈 3 次封顶 + 2 分钟重置；局部注入 chrome。 | 要做零前置依赖的桌面壳；或要设计运行时版本管理。 | observed |
| [`05_内置运行时-tauriapp-源码复核.md`](./shell/_证据/05_内置运行时-tauriapp-源码复核.md) | evidence | 固定 HEAD/tag 与内置 DSH `0.2.0-rc.2`（非本机 rc.3）；核资源映射、sidecar 回退、内部 runProfile、端口散列、自愈封顶、无 lock/校验/回滚/更新与权限面。 | 修正“零前置依赖是代码不变量”“端口持久化”“每个 profile 都有守护”“有自动回滚”等断言。 | 复核 shell/13；设计内置运行时/进程归属/自愈边界。 | observed |
| [`91_冻结分叉-better-sidebar-N23.md`](./shell/91_冻结分叉-better-sidebar-N23.md) | sample | `All3nCN/dsh-better-sidebar-N23`：0.1.x 冻结 fork，用一次失联证明「改得太深就只能分家」。 | 反食谱：peer 上界 = 死亡日期；只写下界 + CI 矩阵，或换接缝，别 fork。 | 想 fork 上游；或要判断一个深改插件的升级风险。 | observed |
| [`03_冻结分叉-better-sidebar-N23-源码复核.md`](./shell/_证据/03_冻结分叉-better-sidebar-N23-源码复核.md) | evidence | 固定 fork HEAD/tag/npm 0.1.0 与上游分叉基点 v0.12.3、最新 v0.28.2：按树比对 90/89/19 改动、上游 1,154 提交/27 tag；确认发布物=tag 树、活动栏未补。 | 修正“上游已补齐活动栏/终端/浏览器”的表述；HEAD≠已发布、根提交无父不可算 ahead/behind。 | 复核 shell/91；判断何时该 fork、peer 上界与追更成本。 | observed |
| [`_证据/01_桌面与终端-原始挖掘.md`](./shell/_证据/01_桌面与终端-原始挖掘.md) | evidence | 四份宿主侧样本的 README 摘录、上游 `desktop` profile 接缝行号、取数时点。 | — | 要核对桌面壳/终端工作区卡片的原文；或重挖这四个样本。 | observed |
| [`02_dsh-TUI-源码复核.md`](./shell/_证据/02_dsh-TUI-源码复核.md) | evidence | 对 `main` HEAD commit `83fcf89`（package 0.17.0）复核 settings/permission 状态、backend 生命周期、输入解析、updater 与测试设计。 | 区分源码机制、测试覆盖和未运行项；纠正通用 overflow replay 等过宽主张。 | 复核 `14_终端即产品` 的数据/权限边界、backend import 和超时/溢出主张。 | observed |
