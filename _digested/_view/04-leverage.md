# ④ leverage — 干货与借鉴总索引

> **这是什么**:看完 ① 冒出来的、② 哪里热闹、③ 谁是锚 之后,回答**「不用回原 repo 翻,哪些经过源码验证的机制可以直接拿走,哪些坑绝对别踩」**。
> **数据口径**:汇总自 [`_digested/view_*`](README.md) 46 张源码级/参考单卡(`main@8f1a1800e`)与同级 [`_leverage/`](../../_leverage/README.md) 四册(226 篇,各自独立校验);**本页零原创**,每一条均可直达原卡或 `_leverage/` 原始论证。实时健康与活跃度见 [`_data/health.md`](../_data/health.md)。

## 一屏路由:按你要做的事直接找干货

| 你想解决什么问题 | 先看哪本领域册 / 源码卡 | 深入机制去 `_leverage/` 哪册 |
|---|---|---|
| **给 Web 壳加侧栏/面板/Tab,或做成可扩展工作台** | [view_ui](../view_ui/README.md) · [better-sidebar](../view_ui/enhance-shell/01-better-sidebar.md) | [产品线 BORROW](../../_leverage/leverage-reshape-product/BORROW.md) |
| **让模型在回复流里输出交互式组件 / 图表 / HTML** | [dsh-genui](../view_ui/inline-genui/01-genui.md) · [dsh-visualize](../view_ui/inline-genui/02-dsh-visualize.md) | [产品线 BORROW](../../_leverage/leverage-reshape-product/BORROW.md) §2 第 15 条 |
| **把 DSH 换成独立终端/桌面产品(换壳)** | [dsh-TUI](../view_ui/replace-shell/01-dsh-tui.md) · [tianshu-tui](../view_ui/replace-shell/02-dsh-tianshu-tui.md) | [产品线 horizon](../../_leverage/leverage-reshape-product/horizon.md) 七层 |
| **给 Agent 做跨会话长期记忆 / RAG / 知识页** | [view_memory](../view_memory/README.md) · [hindsight](../view_memory/host-backed/01-hindsight.md) · [dsh-memento](../view_memory/local-store/02-dsh-memento.md) | —(存储与隐私边界见 [view_memory](../view_memory/README.md)) |
| **会话上下文压缩 / 回退 / 跨工具导入导出** | [view_session](../view_session/README.md) · [billion-context](../view_session/compression/01-billion-context.md) · [dsh-chat-import](../view_session/import-export/01-dsh-chat-import.md) | [产品线 BORROW](../../_leverage/leverage-reshape-product/BORROW.md) §2 第 19–20 条 |
| **挂外部大引擎 / 商业 API / 本地 CLI 工具** | [view_tools](../view_tools/README.md) · [ouroboros](../view_workflow/external-engine/01-ouroboros.md) · [treg](../view_tools/single-purpose/01-treg.md) · [dsh-data-agent](../view_tools/integration-bridge/01-dsh-data-agent.md) | [生命周期 BORROW](../../_leverage/leverage-lifecycle/BORROW.md) |
| **多 Agent 团队编排 / 任务板 / DAG / 跨实例协作** | [view_workflow](../view_workflow/README.md) · [agent-teams](../view_workflow/multi-agent/01-agent-teams.md) · [dsh-taskboard](../view_workflow/multi-agent/02-dsh-taskboard.md) | [协作册 BORROW](../../_leverage/leverage-agent-collaboration/BORROW.md) |
| **让 Agent 从外部源主动接单 → 授权 → 隔离执行 → 回原对话** | [view_proactive_agent](../view_proactive_agent/README.md) · [hiseax](../view_proactive_agent/runtime-forks/01-hiseax.md) · [mycf711](../view_proactive_agent/design-derivatives/01-mycf711.md) | [协作册 BORROW](../../_leverage/leverage-agent-collaboration/BORROW.md) |
| **给 Agent 输出装硬门禁 / 验收闭环 / 审计账本** | [odai](../view_workflow/governance/01-odai.md) · [dsh-taskboard](../view_workflow/multi-agent/02-dsh-taskboard.md) | [门禁与权限 BORROW](../../_leverage/leverage/BORROW.md) · [PROVE 六环](../../_leverage/leverage/lever-prove-output/01-quality-chain.md) |
| **做权限边界 / 工具拦截 / 审批管道 / 隔离** | [gating-hub](../view_tools/toolchain-meta/01-gating-hub.md) · [dsh-computer-use](../view_tools/single-purpose/04-dsh-computer-use.md) | [LIMIT 三层](../../_leverage/leverage/lever-draw-limit/01-trust-layers.md) · [控制预算](../../_leverage/leverage/lever-draw-limit/09-control-budget.md) |
| **发一个在 Web 和 Desktop 都能一次装上、起得来、能自愈的包** | [dsh-TUI](../view_ui/replace-shell/01-dsh-tui.md) · [treg](../view_tools/single-purpose/01-treg.md) | [生命周期 REFERENCE](../../_leverage/leverage-lifecycle/reference/REFERENCE.md) · [发布 18 项自检](../../_leverage/leverage-lifecycle/practice/CHECKLIST.md) |

---

## 一、核心干货模式库(可直接拿走的架构做法)

> 原则:**每条只摘源码已验证的机制形状 + 它的代价/失效边界**。没有失效条件的做法不算干货。

### 1. 界面、交互与产品形态

| 模式 | 代表项目 | 可直接拿走的做法 | 代价与失效边界 | 出处 |
|---|---|---|---|---|
| **把宿主复杂 API 翻译成薄注册表** | `DSH-better-sidebar` | 用 `ctx.provide('betterSidebar', service)` 暴露 `registerTab/Viewer/Action`,内置功能走同一张表(dogfooding);加 `SIDEBAR_SERVICE_VERSION` + 单调 `FEATURES` 能力位,消费方按能力位探测显隐;聚合包重复挂载用 `cordis.patch.yml` 的 `!!js` 守卫退让 | 必须订阅每个宿主 RC 节奏(14 条 peer 钉版);HTTP/WS 路由不经过 DSH 沙箱,只受 `requestRejection` 围栏约束 | [01-better-sidebar](../view_ui/enhance-shell/01-better-sidebar.md) · [产品线 BORROW](../../_leverage/leverage-reshape-product/BORROW.md) |
| **协议 + 按需 Skill + 分级修复的 GenUI** | `dsh-genui` | 系统提示只塞 ≤1.6 KB 围栏语法,64 KB 组件字典放 `SKILL.md` 按需加载;流式 partial parser 闭合首节点即出 UI;guard 先归一化再 `partialRepair` 丢单个坏节点,绝不拖垮整块;交互「本地优先」,只有 `action` 才回传模型 | 跑在宿主同源 DOM(无 iframe 隔离),依赖库(mermaid/ECharts)漏洞即同源风险;依赖代码块 DOM 选择器,宿主改版即静默退回源码 | [01-genui](../view_ui/inline-genui/01-genui.md) |
| **不可信 HTML 关进不透明来源 iframe** | `dsh-visualize` | 模型把整段 HTML 当工具参数交出,渲染端用不透明来源 iframe + 帧内 CSP 硬隔离,牺牲同源交互换取安全边界 | 无法直接共享宿主 React 上下文或本地状态,适合展示型图表/可视化 | [02-dsh-visualize](../view_ui/inline-genui/02-dsh-visualize.md) |
| **宿主侧单实例状态机做「自动继续」** | `dsh-auto-continue` | 用显式收尾判据表 + 九道重复防护闸门 + 32 条冷读预算控制续跑,不靠提示词赌模型自觉 | 紧耦合宿主回合事件与状态定义,宿主行为变化需同步回归 | [05-auto-continue](../view_ui/enhance-shell/05-auto-continue.md) |
| **独立启动器 + 零依赖救援模式** | `dsh-TUI` / `dsh-market` | 换壳产品自带 `doctor` / `safe` 救援 profile;救生页必须活在坏掉的插件栈之外;非 TTY 环境下静默跳过让位给 Web 共存 | 换表层 = 自己接管首启、分发、降级和全部宿主包版本矩阵(40 条 peer) | [01-dsh-tui](../view_ui/replace-shell/01-dsh-tui.md) · [救生页样本](../../_leverage/leverage-reshape-product/plugin/51_分发与救生页-dsh-market.md) |

### 2. 记忆与会话工程

| 模式 | 代表项目 | 可直接拿走的做法 | 代价与失效边界 | 出处 |
|---|---|---|---|---|
| **零 DSH 依赖 + 前缀缓存友好注入** | `hindsight` | 不 import `@deepseek-ai/*`,手写结构化 interface 对齐事件;召回内容以 `form: 'recall'` 的 **user 消息**注入而非 system prompt(避免打断前缀缓存);去重倒扫 session 历史而非内存 map;fork 用 `inheritedEventCount` 切掉父历史、subagent 直接跳过 | 默认后端是 Cloud(装完即上传);fail-open 设计导致记忆坏掉时会话看似正常;工具名绑在启动目录 | [01-hindsight](../view_memory/host-backed/01-hindsight.md) |
| **本地 SQLite 双层记忆 + 写审批 + 会话快照冻结** | `dsh-memento` | 自建 `ctx.memory` 服务缝,零外部服务依赖;写路径经过审批与审计,读视图按会话冻结快照,协议 v1 配 22 例自证套件 | 自建协议尚未被第三方大规模复用,迁移需跟着它的 schema 走 | [02-dsh-memento](../view_memory/local-store/02-dsh-memento.md) |
| **宿主侧决定「何时想起」** | `dsh-auto-memory` | 把召回触发权从模型工具调用收归宿主侧本地判定核,命中后只在历史尾部追加固定边界引用块 | 判定核精度决定噪音上限,误召会挤占上下文预算 | [01-dsh-auto-memory](../view_memory/context-shaping/01-dsh-auto-memory.md) |
| **代理层接管上下文压缩** | `billion-context` | 夹在宿主与模型 API 之间做本地代理改写历史表示,DSH 侧只用两行 bundle 条目顶掉原生自动压缩 | 耦合在 HTTP/API 代理层而非插件接口层,多模型/新协议头需代理端跟进 | [01-billion-context](../view_session/compression/01-billion-context.md) |
| **纯函数 IR 迁移 + 可撤回导入** | `dsh-chat-import` | 42 个来源格式先转统一 IR,再用 host ABI 合成原生会话日志;预览真解析零副作用,导入历史可逐条撤回并保留反向导出 | 每增一种来源或宿主升级会话日志格式,都要补齐转换器测试 | [01-dsh-chat-import](../view_session/import-export/01-dsh-chat-import.md) · [产品线 BORROW](../../_leverage/leverage-reshape-product/BORROW.md) §2 第 20 条 |
| **内容寻址/影子 Git 快照 + 宿主 Fork 回退** | `dsh-turn-rewind` / `dsh-recall-plugin` | 每轮/每条消息拍工作树快照,回退 = 还原工作树 + 借宿主原生 `fork` 到目标 turn 边界建新会话(不破坏原历史) | 大仓库或未忽略大文件会放大快照成本;不同回退实现间无共享协议 | [01-dsh-turn-rewind](../view_session/rewind-edit/01-dsh-turn-rewind.md) · [03-dsh-recall-plugin](../view_session/rewind-edit/03-dsh-recall-plugin.md) |

### 3. 工具接入与外部引擎

| 模式 | 代表项目 | 可直接拿走的做法 | 代价与失效边界 | 出处 |
|---|---|---|---|---|
| **24 行 YAML 纯配置包 + 显式凭据转发** | `ouroboros` | 零 JS 代码,用 `cordis.patch.yml` 挂自带 `dsh-mcp-client` 拉 `uvx` 进程;因 `dsh-subprocess` 默认剥离 `*KEY/*TOKEN/DSH_*`,用 `!!js process.env.X ?? ''` 显式白名单转发;配**契约测试**钉住文档诚实度(如禁止承诺自动恢复) | 依赖外部 `uv` 与 PyPI;未 pin 版本会漂;无 `cwd` 配置可能落错目录;缺凭据时工具照常列出、首调才炸 | [01-ouroboros](../view_workflow/external-engine/01-ouroboros.md) |
| **环境变量 `!!js` 门控 + 零构建纯 ESM** | `treg` | `disabled: !!js (process.env.TREG_TOKEN ?? '') === ''`(切忌 `!!js !` 触发 YAML 双 tag 语法错),缺 token 时隐藏远程 MCP 避免刷屏 401;git 直装包不写 `prepare` 与 `dependencies`,保持零构建纯 ESM | DSH `mcp-client` 默认超时 60s 而上游可跑 180s,客户端超时可能仍被服务端扣费;托管服务有数据出网与归档共享风险 | [01-treg](../view_tools/single-purpose/01-treg.md) |
| **不引驱动包,包 CLI + 版本化 Schema 目录** | `dsh-data-agent` | 把 9 种数据库客户端 CLI 统一包成 7 个窄工具,外加版本化 schema catalog 减少模型重复探库 | 依赖本机已装对应数据库 CLI 与凭据环境 | [01-dsh-data-agent](../view_tools/integration-bridge/01-dsh-data-agent.md) |
| **一次性观测快照 + `stateHash` 执行前复核** | `dsh-computer-use` | GUI 操控把观测做成快照,发输入前用 `stateHash` 校验界面未被篡改/漂移,防误点 | 强绑 macOS Accessibility 权限与窗口焦点 | [04-dsh-computer-use](../view_tools/single-purpose/04-dsh-computer-use.md) |
| **分段提炼 → 合并 + 预算与后台任务** | `dsh-deepread` | 长文档/多源精读统一走「切段提炼 → 归并」流水线,外层套 token 预算、结果缓存与后台执行 | 适合离线/长耗分析,不适合低延迟交互问答 | [05-dsh-deepread](../view_tools/single-purpose/05-dsh-deepread.md) |

### 4. 多 Agent 协作、主动式工作流与治理

| 模式 | 代表项目 | 可直接拿走的做法 | 代价与失效边界 | 出处 |
|---|---|---|---|---|
| **事件驱动推 + 磁盘 `team.json` + `attemptId` 代次防旧信** | `dsh-agent-teams` | 复用宿主 continuable subagent 当成员、当前会话当队长;`agent/status` idle 边推活无轮询;任务带单调 `attemptId`,`agent/pre-step` 信箱准入核对代次丢弃过期消息;冷重启每任务恰好恢复一次、进程内停放不自动死循环 | 锁只在进程内(双进程写同一工作区会静默覆盖);成员共享同目录无 OS 沙箱;关掉队长会话全队静默停摆;追宿主私有 symbol 维护极贵 | [01-agent-teams](../view_workflow/multi-agent/01-agent-teams.md) · [协作册 BORROW](../../_leverage/leverage-agent-collaboration/BORROW.md) |
| **写冲突硬拦截 + Worktree 并行隔离** | `dsh-file-claim` / `dsh-taskswarm` | 多写者改同仓库:要么用 `tools/pre-execute` 返回 **deny** 拦截具体写工具,要么每 lane 一个 git worktree + 集成树 | 提示词里的 `writeScopes` 永远不拦写入;worktree 只带已提交文件,未跟踪文件不会隔离 | [file-claim 样本](../../_leverage/leverage-agent-collaboration/coordination/samples/07-Nwflower-dsh-file-claim.md) · [taskswarm 样本](../../_leverage/leverage-agent-collaboration/pipelines/samples/11-february2015-dsh-taskswarm.md) |
| **外部源 → 准入策略(`observe`先行) → 原子工单 → 隔离执行** | `dsh-windows-superagent` / `session-superagent` | Source/Eval/Ticket/Executor/Report 五段管线;默认 `observe` 先跑几天再切 `auto`;接受时原子建 Ticket+Mandate+Assignment;并发满时**给人多留一个 slot**;保留人工验收权(grill/ack) | worker 以宿主 OS 用户执行无隔离;整树分叉维护成本高;D2 扩展(如 `trace`)吃私有 SQLite 形状而非公开 API,上游改表会静默空白 | [01-hiseax](../view_proactive_agent/runtime-forks/01-hiseax.md) · [01-trace](../view_proactive_agent/contract-extensions/01-trace.md) · [01-mycf711](../view_proactive_agent/design-derivatives/01-mycf711.md) |
| **职责状态机 + JSONL 证据账本 + 人手锁验收权** | `odai` / `dsh-taskboard` | 用 SQLite/JSONL 落不可篡改证据账本,把「人验收的那一步」从模型工具面移除(模型侧不能有 `decide`),强制留「等人」状态 | 规格仍可能由被判定者起草;多门禁共存尚无统一 deny 协议 | [01-odai](../view_workflow/governance/01-odai.md) · [02-dsh-taskboard](../view_workflow/multi-agent/02-dsh-taskboard.md) · [PROVE Playbook](../../_leverage/leverage/lever-prove-output/10-quality-control-playbook.md) |

### 5. 安全边界与发布生命周期

| 模式 | 代表项目 | 可直接拿走的做法 | 代价与失效边界 | 出处 |
|---|---|---|---|---|
| **最小安全三件套:沙箱 + 硬否决 + fail-closed** | `dsh-isolation-gate` 等 | 权限/名单类配置读不到或坏文件一律拒绝(绝不覆盖坏文件);同步守卫只做纯函数判断,重活放异步;明确标清失败方向(fail-closed / fail-open / 转人工) | DSH 原生沙箱**只覆盖文件**,网络与进程不在其策略词汇内,必须在沙箱外单独建门 | [LIMIT 预算](../../_leverage/leverage/lever-draw-limit/09-control-budget.md) · [全禁状态样本](../../_leverage/leverage-lifecycle/config/31_全禁状态-dsh-isolation-gate.md) |
| **双面分发 + 装后自证 + 外部进程六默认** | `cfbridge` / `dsh-noema` | 发标准 `dsh.bundle` 让用户在应用内装(CLI 仅作 web 自动化,Desktop profile 名与 home 路径有差异);`package.json` 别漏 `files`;自带 `doctor` 三条自检;拉外部进程配齐懒起/保活/退避/去重 | 没重启宿主新装 CLI 插件不会生效;用 patch 覆盖宿主已有行时 `name` 是断言,只改配置应只写 `id + config` | [生命周期 REFERENCE](../../_leverage/leverage-lifecycle/reference/REFERENCE.md) · [SURFACES](../../_leverage/leverage-lifecycle/reference/SURFACES.md) · [装后自证](../../_leverage/leverage-lifecycle/install/11_装后自证-cfbridge.md) · [外部进程](../../_leverage/leverage-lifecycle/boot/23_外部进程生命周期-dsh-noema.md) |

---

## 二、高频反模式 / 别抄清单(Top 10)

> 以下每一条都有真实源码翻车案例,做方案或评审时直接当一票否决项核对:

1. **别把「提示词约束 / 默认 `remind`」当门禁或写锁**:官方 Team 的 `writeScopes` 自述永不拦写入,`remind` 默认不拦等于没门;真拦只能挂 `tools/pre-execute` 返回 `deny`([协作册 BORROW](../../_leverage/leverage-agent-collaboration/BORROW.md) · [门禁 BORROW](../../_leverage/leverage/BORROW.md) §5)。
2. **别给 peerDependencies 写死显式上界(`< 0.2.0`)**:带显式上界的 peer 区间等于主动给插件设死亡日期,宿主一升级立刻冻结不可装([冻结分叉反例](../../_leverage/leverage-reshape-product/shell/91_冻结分叉-better-sidebar-N23.md) · [ai-novel-writer](../view_workflow/vertical-preset/01-ai-novel-writer.md))。
3. **别把「宿主主项目星标」当「DSH 插件被采用」**:OpenViking / hindsight / ouroboros / treg / billion-context / MisakaNet 的高星均属主项目,看插件真实热度必须拆星标归属 + 看 npm 月下载 + 第三方代码级依赖([03-anchors](03-anchors.md) · [_method/02](../_method/02-anchor-metrics.md))。
4. **别把「装前扫描 / 空能力披露 / AI 审批」当安全边界**:静态扫描不执行代码且 `capabilities.json` 覆盖率持续衰减;第二模型只替代点击,不替代强制点;真实安全靠最小权限 + fail-closed + 可回滚([LIMIT 三层](../../_leverage/leverage/lever-draw-limit/01-trust-layers.md))。
5. **别把「有 DAG / 快照重跑 / 无幂等重试」当断点可恢复**:没有 journal 的 DAG 不能暂停恢复;没有幂等键的重试通道会造成重复执行;跨进程写同一个 JSON 文件没有文件锁/revision 会静默丢更新([03-dsh-workflow](../view_workflow/multi-agent/03-dsh-workflow.md) · [01-agent-teams](../view_workflow/multi-agent/01-agent-teams.md))。
6. **别在 `cordis.patch.yml` 里写 `disabled: !!js !expr`**:第二个 `!` 会被 YAML 解析为重复 tag 属性导致整棵 profile 炸掉,必须改写为 `=== ''` 等无前导 `!` 表达式([01-treg](../view_tools/single-purpose/01-treg.md))。
7. **别让「救生页」或「安装后自检」依赖可能坏掉的插件栈**:profile 炸了的时候救生页一起起不来;救援模式必须零 lib 依赖独立运行([救生页样本](../../_leverage/leverage-reshape-product/plugin/51_分发与救生页-dsh-market.md) · [01-dsh-tui](../view_ui/replace-shell/01-dsh-tui.md))。
8. **别对第三方包「只看仓库名不核 npm 包名」**:同名不同人的 npm 包已出现多起(如 `omdsh-dev/dsh-genui` 实际发 `@changfenhuang/dsh-genui`,非 scoped `dsh-genui` 是无关 Vue 包);安装前必核 `package.json` 的 `repository`([01-genui](../view_ui/inline-genui/01-genui.md) · [门禁 BORROW](../../_leverage/leverage/BORROW.md) §5.4)。
9. **别用私有 DOM 锚点还不写降级**:宿主 DOM 改版后选择器 0 命中就会变白屏或无声失灵;优先用上游约定 CSS 变量/slot,必写「找不到就退回原文/不激活」([产品线 BORROW](../../_leverage/leverage-reshape-product/BORROW.md) §3)。
10. **别只写一条 CLI 命令就宣称支持双端**:`dsh plugin --profile web add` 装不进保留名 Desktop 或私有 home 的社区桌面壳;发布前按双面差异表逐项核对([生命周期 BORROW](../../_leverage/leverage-lifecycle/BORROW.md) §7)。

---

## 三、深度专题直达(`_leverage/` 四册,物理自包含)

当上面的索引不够用、需要抄施工图或完整证据链时,直接进入同级 [`_leverage/`](../../_leverage/README.md) 的对应册(四册共用 `node _leverage/verify.mjs`,共 226 篇):

| 册 | 解决什么深层问题 | 快捷入口 |
|---|---|---|
| **门禁与权限** | 质量链六环(PROVE)、安全三层监管链(LIMIT)、六条跨域法则、抄前七问 | [`leverage/BORROW.md`](../../_leverage/leverage/BORROW.md) |
| **多 Agent 协作** | 单 vs 多五步判、委派/编队/DAG/跨机八条配方、状态/冲突/收敛三笔税 | [`leverage-agent-collaboration/BORROW.md`](../../_leverage/leverage-agent-collaboration/BORROW.md) |
| **产品形态重塑** | 插件 / Profile / 独立宿主七层决策、可直接搬走的 22 条产品工程规则 | [`leverage-reshape-product/BORROW.md`](../../_leverage/leverage-reshape-product/BORROW.md) |
| **分发与生命周期** | Web + Desktop 双面安装/启动/配置/首启规范与发布前 18 项自检表 | [`leverage-lifecycle/BORROW.md`](../../_leverage/leverage-lifecycle/BORROW.md) |
