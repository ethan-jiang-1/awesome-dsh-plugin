# view_proactive_agent — 主动式 agent(前沿专题)

> 状态:**前沿专题,0007 首立,未计入五领域;0 张卡待立**。数据截止 `main@8f1a1800e`(2026-11-25,13136 条);上游原型 `deepseek-ai/dsh-superagent-prototype@8c32a9dc`(24,565★ / 3,081 forks,实时值)。逐条证据与深读见 [`_faq_on_digested/02_superagent-dependents/`](../../_faq_on_digested/02_superagent-dependents/question.md)。

## 为什么单独一册

不是因为它条目多——16 个名字命中、9 个真依赖,体量远低于五领域(最小 546 条)。是因为**读者问题不同**:

- 五领域问"这个插件是什么、怎么接、值不值得装";
- 这里问"**谁能让 agent 自己开始干活、凭什么、在哪执行、干完回哪里**"。

这个问题横跨 workflow(编排)、session(会话)、remote(渠道)、dev(可观测)、ui(面板)。放在 `view_workflow` 下会把 session/remote/dev 的成员硬塞进 workflow;单独成册才能按**依赖层**组织,而不是按官方类目。

## 定义(三条同时成立)

1. 有**外部输入源**(GitHub / 飞书 / 微信 / 本地会话),不是只由当前会话手动派活;
2. 有**准入/裁定**环节(名单、规则、accept mode、Mandate),不是每条消息都执行;
3. 接受后生成**可追踪的工作项**(Ticket/工单),在**独立会话或目录**里执行,结果**回到原对话**。

与相邻概念的分界:

| 容易混的 | 不是本册 | 区别 |
|----------|----------|------|
| multi-agent | 团队协作 | 那边问"多个 agent 怎么分工";这里问"谁让 agent 开始、凭什么" |
| external-engine | 挂外部引擎 | 那边把活交给外部引擎;这里引擎仍是 DSH,变的是入口与授权 |
| session 自动化 | 定时/唤醒 | 那边是"什么时候叫醒会话";这里是"外部请求如何变成受权工作项" |
| 桌宠/陪伴 | 人格化交互 | 那边是"像谁";这里是"能替谁做什么、做到哪一步" |

## 成员地图(按依赖层)

| 子分类 | 定义 | 成员 | 代表 |
|--------|------|-----:|------|
| [runtime-forks](runtime-forks/README.md) | 整树分叉或 vendor 上游内核 | 6 | HiSeax(138★)、local(11★)、nelson(10★) |
| [contract-extensions](contract-extensions/README.md) | 不搬代码,吃 `stateDir`/`orchestrator.sqlite`/Source/profile 契约 | 3 | trace、wechat-source、power |
| [design-derivatives](design-derivatives/README.md) | 以领域模型为起点另写实现 | 3 | MYCF711(52★)、NattoCB、imperial |

上游根:`deepseek-ai/dsh-superagent`(仓库现名 `...-prototype`)——不在注册表,`private: true` 不发 npm;它定义 Source / Policy / Ticket / Mandate / Assignment / Subscription 的语义。

## 本册的判断线索

- **先看层,再看星**:D1 看"改了多少上游代码"(HiSeax 92/92 文件全改 vs desktop 7 个文件);D2 看"吃了哪条事实契约";D3 看"保留了哪几个概念、丢了哪几个"。
- **星标不是唯一量纲**:desktop 1★ 但 npm 月下载 1,753;HiSeax 138★ 但只能 clone/`link:` 装;MYCF711 52★ 但 npm latest 停在 0.10.12(2.0.0 未发)。
- **授权面比执行面更值得读**:Source 名单、accept mode、Mandate 不可变、Policy 变更只投递——这些是上游与分叉真正的分界;执行层(session/目录/worktree)各家用各的。
- **跨册成员只在本册登记一次**:渠道类暂时没有独立册(remote 未立),故 wechat-source 只在这里;session 侧 MYCF711 与 [view_session](../view_session/README.md) 互链,不重复计数。

## 立册与立卡门槛

- **立册**:默认门槛是"领域体量 ≥400 条 + 本期新增 ≥100"(见 [`../AGENTS.md`](../AGENTS.md) §二)。本册**远未达标**,是按"前沿机制 + 跨域读者问题 + 上游机构背书"破例先立;体量涨上来之前,不占五领域的可视化导航位。
- **立卡**:默认 ≥500★ 或被 ≥5 个条目引用其协议。**本轮无人达标**;按机制例外,下一轮优先 HiSeax(138★)、MYCF711(52★)两张。两页的源码级材料已在 FAQ 备好:[HiSeax](../../_faq_on_digested/02_superagent-dependents/lines/01-windows-hiseax.md)、[MYCF711](../../_faq_on_digested/02_superagent-dependents/lines/10-session-level.md)。
- **图谱**:立卡后再生成 `plugin-map.svg`;在此之前不挂图,避免空图。

## 与五领域的关系

| 册 | 关系 |
|----|------|
| [view_workflow](../view_workflow/README.md) | 本册从它的 `proactive-agent` 子分类升级而来;workflow 里只留一句指针 |
| [view_session](../view_session/README.md) | MYCF711 的"会话级唤醒"是 D3 成员;session 册负责会话生命周期,不重复本册的授权分析 |
| [view_tools](../view_tools/README.md) | 渠道/桥接类工具若只做 Source 不建工单,仍归 tools |
| `view_remote`(未立) | 微信/飞书渠道目前寄在本册;remote 立册后再交叉登记 |

## 数据与复现

```sh
grep -ril 'superagent\|super-agent\|super_agent' data/plugins | wc -l   # 16
git ls-remote https://github.com/deepseek-ai/dsh-superagent HEAD       # 8c32a9dc…
python3 _digested/ecosystem/census.py                                  # 13136 条
```

星标/forks 为 2026-11-25/26 GitHub API 实时值;注册表计数来自 `main@8f1a1800e`。本册 0 卡,`_data/` 不含本册条目。
