# `view_proactive_agent/` 工作规则

主动式 agent 前沿专题。全册 12 个注册表成员 + 1 个上游根,0007 首立、0 卡。

> 通用纪律(底线、八段模板、立册/立卡门槛、同步七步)只在 [`../AGENTS.md`](../AGENTS.md);本文件只写本册特有的判断线索。

## 分层(本册的主轴)

| 层 | 判定 | 读什么 |
|----|------|--------|
| **D1 runtime-forks** | 同包名/同 id、整树分叉,或 vendor 上游 `core/` | 改了上游哪些文件、保留哪些语义;宿主钉版与安装路径 |
| **D2 contract-extensions** | 不搬代码,吃 `stateDir` / `orchestrator.sqlite` / Source 契约 / profile + `bridge.js` | 具体哪个服务/表/字段/协议;失败时是静默还是显式 |
| **D3 design-derivatives** | 只借领域模型,自有实现 | 保留哪几个概念(Ticket/Mandate/Subscription)、丢了哪几个、为什么 |

**分层决定证据标准**:D1 要给"上游 N 个文件里几个逐字节相同";D2 要给"读的是哪张表/哪个服务";D3 要给"代码/契约零依赖的反证"。

## 本册特有的判断线索

- **先问授权,再问执行。** 这条线的分界不在"能不能跑",在"谁让它跑、凭什么、做到哪一步":Source 名单、accept mode、Mandate 不可变、Policy 变更只投递、Subscription 绕过 gate 但不授权。执行层(session/目录/worktree)各家用各的,不是主要差异。
- **不要把"主动"写成"自动"。** 上游默认 `observe`,主动是"规则允许时才动";把 demo 的自动执行当默认行为,会写错整条线。
- **星标 ≠ 安装 ≠ 依赖。** 三种量纲分开:HiSeax 138★ 但不可 npm 装;desktop 1★ 但 npm 月下载 1,753;MYCF711 52★ 但 npm latest 停在 0.10.12。写"影响力"必须说明是哪一种。
- **跨册只登记一次。** 渠道(微信/飞书)寄在本册;会话生命周期归 `view_session`;工具型 Source 若只做渠道不建工单,归 `view_tools`。跨册用链接,不复制事实。
- **协议复用才算收敛。** 第三方读同一份 `orchestrator.sqlite`、复用同一套 Source 契约、或抄同一份 schema,才是"标准"信号;只是名字像、设计像,都不算。

## 刷新

- 每轮同步后:先跑 census 核分母,再看 `data/plugins/` 里新出现的 `superagent|super-agent|super_agent` 命中与上游是否发版;
- 成员表按 D1/D2/D3 重排;新增成员先归层,再决定是否立卡;
- **立卡后**才生成 `plugin-map.svg` 并把本册加入 `_digested/verify.mjs` 的领域列表;在此之前本册不占五领域导航位,也不进 `_data/` 卡表;
- 立册状态在 [`../_view/README.md`](../_view/README.md) 与 [`../00-index.md`](../00-index.md) 各留一行指针,不复制成员表。

## 完成判据

- 本册 Markdown 相对链接、UTF-8、LF 通过 `node _digested/verify.mjs`;
- 成员表的星标/日期与 `_faq_on_digested/02_superagent-dependents/` 一致;
- 0 卡阶段不写"全部 ★★★"、不挂空图、不把本册算进五领域统计。
