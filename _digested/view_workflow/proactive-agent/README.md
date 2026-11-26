# proactive-agent — 主动式 agent(Source → 工单 → 隔离执行 → 回原对话)

> 状态:**0007 新增观察,待立卡**(2026-11-25)。本子分类登记的是本轮突然成形的一族:**不是"多个 agent 互相协作",而是"一个常驻 agent 接外部请求、按规则裁定、开工单、在隔离会话里执行、把结果回原对话"**。成员全部来自 0007 同步窗口(`29b3ed46e` → `8f1a1800e`),溯源与逐条判定见 [`_faq_on_digested/02_superagent-dependents/`](../../../_faq_on_digested/02_superagent-dependents/question.md)。

## 定义

判定标准三条同时成立:

1. 有**外部输入源**(GitHub/飞书/微信/本地会话),不是只由当前会话手动派活;
2. 有**准入/裁定**环节,不是每条消息都直接执行;
3. 接受后生成**可追踪的工作项**(Ticket/工单),在**独立会话或目录**里执行,结果**回到原对话**。

与 [multi-agent](../multi-agent/README.md) 的分界:multi-agent 问"多个 agent 怎么分工";这里问"**谁让 agent 开始干活、凭什么、干完回哪**"。与 [external-engine](../external-engine/README.md) 的分界:external-engine 把活交给外部引擎;这里引擎仍是 DSH,变的是**入口与授权**。

## 成员(0007 窗口)

上游根:`deepseek-ai/dsh-superagent-prototype`(24,565★ / 3,081 forks,不在注册表,`private: true` 不发 npm)。注册表内 16 个名字命中里,**9 个真依赖、3 个同设计**;本子分类只登记 workflow 类目内的 7 个,跨域成员在其它册。

| 条目 | 星标(实时) | 关系 | 说明 |
|------|------------:|------|------|
| HiSeax/dsh-windows-superagent | **138** | D1 整树 fork | Windows + 微信 iLink + 看板;92/92 上游文件全改,+22 新文件([FAQ 单页](../../../_faq_on_digested/02_superagent-dependents/lines/01-windows-hiseax.md)) |
| mengzhongjie/dsh-superagent-local | 11 | D1 整树 fork | 改成"本机工作区"版:每个 workspace 一个主会话→工单→worker |
| DASHAN-0079/dsh-superagent-adapt | 0 | D1 整树 fork | 适配 DSH 0.2.2-rc.3;1213 例等价性测试,停在"能装" |
| 439436269-ctrl/dsh-superagent | 0 | D1 整树 fork | 多仓 + IM 桥(钉钉/企微);GitHub 上是真 fork,npm 0.3.0 |
| jinghuaihuaxiang-star/dsh-superagent-desktop | 1 | D1 整树 fork | 装进现有 profile;npm 月下载 1,753(这批唯一有安装量) |
| NattoCB/dsh-plugin-superagent | 0 | D3 设计衍生 | 持久工单 + 可替换会话的项目控制台 |
| shilaoban666/dsh-imperial-court | 2 | D3 设计衍生 | 本机 Router–Worker + 三省六部审查;独立多 CLI 产品 |

跨域成员(不在本册计数):MYCF711/dsh-session-superagent(52★,session)、NelsonLongXiang/dsh-open-a2a-net(10★,remote,vendor 内核)、luckyxiang6688/dsh-superagent-trace(dev,只读 `orchestrator.sqlite`)、dsh-superagent-wechat-source(remote,Source 契约)、MingoYung/dsh-superagent-power(ui,进程开关)。

## 为什么本轮才立

- **供给突然成形**:0007 窗口 workflow 新增 98 条,其中 7 条落在这个机制上;跨域再加 5 条,合计 12 条与上游有关。0006 时只有零星条目。
- **上游有机构背书但不在注册表**:24.5k★ 的 prototype 定义了 Source/Policy/Ticket/Mandate 的语义,而社区侧的分叉在 11 月集中出现。
- **机制与现有子分类都不同**:不是团队协作(multi-agent)、不是外部引擎(external-engine)、不是垂直预设(vertical-preset)。

## 立卡条件与候选

默认门槛不变(≥500 星,或被 ≥5 个条目引用其协议)。**按此门槛,本轮无人达标**;但按"机制例外"有两条值得先读:

1. **HiSeax/dsh-windows-superagent(138★)** — 唯一过百星的依赖者,且是 92/92 文件全改的深分叉;它把"上游的 Unix 假设"逐条拆掉,是这条线的机制样本。已写过源码级分析:[FAQ 单页](../../../_faq_on_digested/02_superagent-dependents/lines/01-windows-hiseax.md)。
2. **MYCF711/dsh-session-superagent(52★)** — 把 Router–Worker 降成"会话级唤醒",牺牲 Ticket/Mandate/Subscription 四项换轻量;它的 `official-decomp` 记录了设计漂移。属 session 册,但机制同族:[FAQ 单页](../../../_faq_on_digested/02_superagent-dependents/lines/10-session-level.md)。

**本轮先建子分类、不立卡**:成员、边界、候选已清楚,但两条候选的源码级证据在 FAQ 侧,搬成八段卡需要重写与 SVG 挂载;留到下一轮按"机制例外"立 1-2 张(HiSeax 优先)。

## 观察点

- **是否出现协议复用**:trace/wechat-source 吃的是 `stateDir`/`orchestrator.sqlite`/Source 契约,不是公开 API;谁能先把这层做成稳定接口,谁才可能成为标准。
- **Windows 与 IM 渠道是否继续分化**:HiSeax 已把微信/看板做进同一 fork;下一个分叉是复制它,还是回到上游写 Source,是这条线的分水岭。
- **星标与安装量的背离**:03-desktop 1★ 但 npm 月下载 1,753;HiSeax 138★ 但 npm 不可装。评价这条线不能只看星标。
