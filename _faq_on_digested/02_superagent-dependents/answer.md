# A02 · 16 个名字,9 个真依赖:superagent 插件的四种接法

> 数据基线:注册表 `main@8f1a1800e`(2026-11-25,13136 条);上游 `deepseek-ai/dsh-superagent-prototype@8c32a9dc`(实时 24,565★ / 3,081 forks,2026-11-25);16 个候选各自浅克隆到下表 HEAD。星标全部为 2026-11-25 实时 API 值,**不引用冻结边车**。方法见 [question.md](question.md)。

## 一句话答案

16 个名字命中里,**9 个真依赖**:6 个代码级(D1,整树分叉或 vendor 内核)、3 个契约级(D2,只吃 Source/stateDir/`orchestrator.sqlite`/profile 进程);另有 3 个"同设计"(D3)、4 个只是名字里有 superagent(D0)。**上游自己不在注册表**;而注册表里**星标最高的两个社区条目反而不是依赖者**(MYCF711 52★ = D3,LittleChenLiya 22★ = D0)——这个反差是答案的一半。依赖者里唯一过百星的是 [HiSeax/dsh-windows-superagent](lines/01-windows-hiseax.md)(138★);影响面见 [impact.md](impact.md),分线见 [lines/](lines/README.md)。

**它们都在 GitHub 上**;上游 `private: true` 不发 npm。npm 上能装到的是 03(`dsh-superagent-desktop`)、05(`@vfvrpq/dsh-superagent`)、06(`@nelsonlongxiang/dsh-open-a2a-net`)、07(`dsh-superagent-trace`)、08(`dsh-superagent-wechat-source`)、10(`dsh-session-superagent`);02/04 走 GitHub tarball,09 走 Release tgz。

## 计数

| 层 | 数量 | 仓库 |
|----|-----:|------|
| **D1 代码级** | **6** | ctrl439-superagent · dsh-superagent-adapt · dsh-superagent-desktop · dsh-superagent-local · dsh-windows-superagent · dsh-open-a2a-net(vendor) |
| **D2 契约级** | **3** | dsh-superagent-trace · dsh-superagent-wechat-source · dsh-superagent-power |
| D3 设计级 | 3 | dsh-session-superagent · dsh-plugin-superagent · dsh-imperial-court |
| D0 无关 | 4 | dsh-superagent(LittleChenLiya) · dsh-mini-superagent · dsh-ladder-superagents · dsh-s1 |

## 逐个判定(16 行,证据在代码里)

| 仓库 | 层 | 用了哪一面 / 凭什么这么判 | ★ | HEAD |
|------|----|---------------------------|--:|------|
| 439436269-ctrl/dsh-superagent | D1 | 同一套 bundle id(`dsh-superagent`、`-github`、`-feishu`、`-worker-preset`);自述"从 DeepSeek Harness 的原型起步",新增 `im-watch` 与多仓 | 0 | `9dea493` |
| DASHAN-0079/dsh-superagent-adapt | D1 | `ADAPTATION.md:3`:"upstream `dsh-superagent` source adapted to 0.2.2-rc.3";同包名、同 plugin id | 0 | `34c21ff` |
| jinghuaihuaxiang-star/dsh-superagent-desktop | D1 | `README.md:3,70` 明说 fork,改成 desktop bundle;同 id 族 | 1 | `e2cee41` |
| mengzhongjie/dsh-superagent-local | D1 | `README.md:11` "fork of dsh-superagent";同包名 + 同 id + `local-watch` | 11 | `fe5929a` |
| HiSeax/dsh-windows-superagent | D1 | 上游 `src/` **92 个文件全部存在、全部有实质改动**,另加 22 个文件;README 自述 derived | **138** | `2f3dd46` |
| NelsonLongXiang/dsh-open-a2a-net | D1 | `THIRD_PARTY_NOTICES.md`:"domain engine … **vendored unchanged**",落点 `src/superagent/upstream/` | 10 | `4151721` |
| luckyxiang6688/dsh-superagent-trace | D2 | 从 `orchestrator` 服务取 `stateDir`,**只读** `orchestrator.sqlite`;`README:72` | 0 | `5d6feab` |
| luckyxiang6688/dsh-superagent-wechat-source | D2 | 实现 Super-agent 的 `SourceKind`(配置/scope/policy/channel/threadContext);复用 `stateDir` | 0 | `486f817` |
| MingoYung/dsh-superagent-power | D2 | 管独立 Super-agent profile 的进程启停;双方注册 `bridge.js`、同一 `homePath`/`profileName`/密钥 | 0 | `be94341` |
| MYCF711/dsh-session-superagent | D3 | 自述"项目起点 = prototype",但落盘是自己的 `watchers.json`,无 upstream 代码/契约 | 52 | `fe1c356` |
| NattoCB/dsh-plugin-superagent | D3 | `README:102` "参考项目与执行分层思想";自己的 `stateDir`(`superagent-control`) | 0 | `fee0315` |
| shilaoban666/dsh-imperial-court | D3 | "思路同源"的 Router–Worker 本机实现,零 upstream 代码 | 2 | `3191c46` |
| LittleChenLiya/dsh-superagent | D0 | 并行子任务编排/合成报告;仓库无 upstream 引用、无同名 id、无其数据契约 | 22 | `60d2b21` |
| wychmod/dsh-mini-superagent | D0 | 任务派发 + 工作台;"能力模型参考",但不实现 Source→Ticket 管线 | 4 | `90e3857` |
| Yukikaze-Ai/dsh-ladder-superagents | D0 | 子代理模型选档,与 super-agent 只是词面相近 | 1 | `a808d46` |
| superagents-lab/dsh-s1 | D0 | Search1API 检索工具,组织名带 superagents | 2 | `6d6ce96` |

## 他们到底利用了哪一面

所有"真依赖"都绕不开同一个事实:**上游是 `private: true` 的源码仓库,不发 npm**。所以依赖只能长成四种形态:

1. **整树分叉**(5 个):把上游 `src/` 搬过来,改包名/id/平台,再补渠道或面板。HiSeax(Windows)、local(本机工作区)、desktop(桌面 bundle)、adapt(0.2.2-rc.3 适配)、ctrl439(多仓 + IM 桥)都是这一类。它们复用的是**整套领域模型**(Source → Eval → Ticket → Executor → Report),不是某一个函数。
2. **vendor 内核**(1 个):Nelson 把上游 domain engine 原样搬进 `src/superagent/upstream/`,外层换成 A2A 网络与 superagent team presets——代码不动,壳换掉。
3. **吃运行契约**(3 个):trace 只读 `orchestrator.sqlite` 与会话日志(可观测性);wechat-source 新写一个 Source,把微信私聊翻译成 Trigger(新渠道);power 管独立 profile 的进程与 `bridge.js`(生命周期)。
4. **只借设计**(3 个):mycf711 把 Router–Worker 降级成"会话级唤醒 + 单 Ticket";nattocb 做带持久工单的项目控制台;imperial 把 Router–Worker 搬到自己电脑上,再加三省六部式审查。它们读上游文档,但不搬代码。

## 解决什么问题(为什么有人宁可分叉)

| 缺口 | 谁在补 | 做法 |
|------|--------|------|
| **Windows 跑不起来** | HiSeax、power | 路径/PATHEXT/pwsh/`windowsHide`/PID 身份校验;power 只做进程开关 |
| **只服务 GitHub 仓库,不服务"坐在机器前的人"** | mengzhongjie-local | 每个工作区一个主会话,把需求转工单,Worker 在该工作区目录执行 |
| **只有 GitHub + 飞书两个 Source** | ctrl439、HiSeax、wechat-source | IM 桥(钉钉/企微/微信 iLink);Source 作为可插拔适配层 |
| **看不见它在干什么** | trace、HiSeax board | 只读 sqlite + 会话日志画泳道;侧栏看板列并发位/工单状态 |
| **独立 profile 的进程没人管** | power | 输入栏一个 Sup 开关,起停后台进程并释放内存 |
| **上游只适配某个 DSH rc** | adapt | 把 0.1.0 的源码改到 0.2.2-rc.3,并记录等价性测试 |
| **多仓/团队策略/审批** | ctrl439、nattocb、imperial | 多仓分支、准入表 + Mandate、面板决策卡 |

## 设计思路的共性

四个字:**把"谁让它做"留在域内,把"怎么做"放出去**。上游把授权(Source 的允许名单、Policy、Mandate)和内容(Trigger、Subscription)分开,Executor 只是域外的一个 Session;于是:

- 换渠道只需要新 Source,不需要改 Router;
- 换执行环境只需要换 Executor/目录准备命令(`git worktree`),不需要改授权;
- 换展示只需要读 `orchestrator.sqlite`,不需要进主循环。

这也解释了为什么分叉者大多**不改领域模型,只改部署与渠道**——模型是可复用的,Source/Channel/Executor 属于部署。

## 影响面与分线

本文只回答"有多少、用了什么、解决什么问题"。**谁有杠杆、什么值得盯、每条线各自怎么长**另开两页:

- [impact.md](impact.md):影响面分析(机构背书 vs 社区采用、四种杠杆、分叉经济学、风险与观察点);
- [lines/](lines/README.md):每条符合"明显依赖或衍生"标准的线各一页(上游原型 + 10 条依赖/衍生线,共 11 页;两条低价值线退册,原因见该页)。

单条线里影响力最大的 Windows 分叉见 [lines/01-windows-hiseax.md](lines/01-windows-hiseax.md)(138★)。

## 复现

```sh
grep -ril 'superagent\|super-agent\|super_agent' data/plugins | wc -l        # 16
git ls-remote https://github.com/deepseek-ai/dsh-superagent HEAD            # 8c32a9dc…
# 16 个仓库浅克隆到 /tmp/sa-research/<slug>,HEAD 见上表
```

判定全部基于克隆后的 `README`、`package.json`、`cordis.patch.yml`、`src/` 与 `THIRD_PARTY_NOTICES.md`;星标为 2026-11-25 GitHub API 实时值。未读部分与边界案例见下文。

## 边界与未验证

- **"依赖"不含设计借鉴**:D3 单列,不计入 9;否则数字会虚高到 12。
- **ctrl439 是否算独立 fork** 取决于"同 bundle id + 自述从原型起步"是否足够;它的包名换了 scope(`@vfvrpq/`),但 id 未换。
- **Nelson 的 vendor 是否原样**:`THIRD_PARTY_NOTICES.md` 自述 unchanged;未逐行 diff 整个 `src/superagent/upstream/`。
- **HiSeax 的血缘**:README 把 Windows 基线指向 `vHao11/dsh-windows-superagent@windows-adapt`,该仓库 2026-11-25 已 404;与 `deepseek-ai/dsh-superagent` 的代码重叠(92/92 文件)是直接证据,但中间那层无法复核。
- **生态兼容**:trace/wechat-source 找的是 `orchestrator` 服务与 `stateDir`;HiSeax 把 id 改成 `dsh-windows-superagent-*`,两者能否共用未验证。
