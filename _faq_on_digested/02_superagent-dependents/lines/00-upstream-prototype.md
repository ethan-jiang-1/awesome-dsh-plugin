# 00 · dsh-superagent 原型 — 被分叉的"领域模型"

> `deepseek-ai/dsh-superagent-prototype@8c32a9d`(2026-10-31;实时 24,565★ / 3,081 forks,2026-11-25)。上游仓库由 `deepseek-ai/dsh-superagent` 改名而来,包名 `dsh-superagent@0.1.0`,`private: true`,MIT。**不在**社区注册表 `data/plugins/` 里,也不发 npm。证据等级 ★★★(读了 README、SETUP、docs/000–008、`cordis.patch.yml`、`package.json` 与 `src/` 目录;没有实装运行)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 形态 | DSH **bundle**(带 `cordis.patch.yml`),client 侧注入 6 个 `@deepseek-ai/dsh-client-*` 包 |
| 职责 | 监听 GitHub(可选飞书)→ Policy 裁定 → Ticket → 独立 DSH 会话与目录执行 → 回原对话(评论/PR) |
| 代码 | `src/` **92 个 TS 文件 / 12,390 行**;`tests/` 53 个文件;`docs/` 9 篇(000–008,共 1,973 行) |
| 声量 | 24,565★ / 3,081 forks——**机构/团队背书**,不是社区采用 |
| 许可/分发 | MIT;`private: true`,无 npm 包,只能 clone/源码安装 |
| 自述边界 | "Research prototype for reference only, not an official DeepSeek product";文章里的部分设计**未实现** |

## 影响力

- **数字**:24,565★ / 3,081 forks / pushed 2026-11-03;无 npm 包(`private: true`),不在注册表 13,136 条里。
- **谁在用它**:注册表里 12 个条目与它有关——5 个整树 fork、1 个 vendor 内核、3 个契约插件、3 个设计衍生;其中 9 个是真依赖(见 [../answer.md](../answer.md))。这是一个**机构原型被一圈小分叉包围**的结构,不是一个有依赖生态的库。
- **判断**:定义权高、分发权低。它定义了 Source/Policy/Ticket/Mandate 这套语义,但没有 npm/版本契约,下游只能整树搬;24.5k★ 是 DeepSeek Harness 团队背书,不能读成社区采用。真正的"采用"发生在 fork 的部署面(Windows、本机、IM),不在上游本身。

## 它要解决什么问题

一个团队在一个 GitHub 仓库上协作时,瓶颈不是写代码,是**人的注意力**:

- 有人提 issue/PR 评论/飞书消息,得有人看见、判断、安排、回复;
- 让 agent 全自动接活,又会"浪费整个团队的注意力"——它可能乱开 PR、乱回评论、把半成品当完成;
- 现有 CI/机器人只能做规则触发,不能"读懂请求 → 开工作项 → 在隔离环境里执行 → 回原话题"。

上游的答案是**主动但受控**:只有当人明确要求,或团队写下的规则允许时才行动;只在"人必须拍板"或"结果可用"时说话。README 把它压成一句:"take as little human attention as possible, and give as much value as possible."

## 它的路径

五段管线 + 一套刻意很小的领域模型(`docs/001-domain.md`):

```text
Source → Trigger → Thread → Eval(gate + assessment) → Ticket(+Mandate)
       → Assignment → Executor(DSH Session + 目录) → Report/Reply → 回 Source
```

| 概念 | 职责 | 关键规则 |
|------|------|----------|
| **Source** | 事件流(一个 kind 可复用,一个实例是一份配置) | 自己记读取位置;丢弃机器人自己的消息;把事件翻译成 Thread 与回信地址 |
| **Trigger** | 一条不可变事件 | 同一 Trigger 被接受两次只建一个 Ticket |
| **Thread** | 按时间排序的 Trigger 序列 | 同一 Thread 同时只跑一个 Eval;可挂多个 Ticket |
| **Policy** | 版本化的裁定规则 + 每个 Source 的白名单/机器人名单 | 改规则会作废正在跑的 Eval;不撤销已发 Mandate |
| **Eval** | 对一批 Trigger 的两层判断(gate + assessment) | 无状态;输入是批次、Thread 快照、全部 Ticket、当前 Policy |
| **Mandate** | 一次 accept 授予的范围/强度/命中规则/发送者身份 | 不可变;扩大范围要新 Ticket;只有人喊停或 Policy 失效才撤销 |
| **Ticket** | 授权工作的单位 | 只由 Eval 创建;`open → ended`,人再来消息可恢复(除非被喊停) |
| **Assignment** | Ticket 与某个 Executor 实例的绑定 | 生命周期独立于 Ticket;只有最终报告能从 Executor 侧结束 Ticket |
| **Subscription** | Ticket 与 Thread 的多对多 | 订阅消息**绕过 gate**、只给上下文、不给新授权 |
| **Executor** | 域外:DSH Session + 目录 | 通过 Assignment 接入;每个 Ticket 一个 `worker-<id>` |

**最关键的边界**:Executor 不在领域模型里。模型只描述"谁被允许做什么、做到哪一步",不描述"用哪个进程跑"。所以换执行环境(本机/远程/多仓)不需要改授权模型。

## 技术思考(六条关键判断)

1. **授权与上下文分离。** 订阅(Subscription)让后续讨论自动到达 Ticket,但**不经过 gate、不授予新权限**;每条 Ticket 始终受自己的 Mandate 限制。这样"后来的人插话"不会变成"新工作",也不会丢掉上下文(`docs/002-authorization.md`)。
2. **Mandate 不可变,Policy 变更只投递。** 规则变了,活着的 Assignment 会收到通知,但不会撤销已发的 Mandate,更不会取消正在跑的 Ticket——避免"改规则把半成品撕了"。只有人喊停才停(`docs/001-domain.md` 的 rejected concepts 明确写了这条)。
3. **Ticket 状态独立于 Session。** Ticket 可以换 Executor、被恢复、由多个 Executor 依次跑;所以它有自己的一套阶段(`person/working/idle` 六阶段),不跟随 DSH 会话的生死(`docs/003-execution.md`)。
4. **Eval 无状态、Thread 串行、批量合并。** 同一 Thread 同时只跑一个 Eval,期间到达的 Trigger 合并进下一批;Eval 自己不留状态,重启不丢判断依据。这让"重复接受只建一个 Ticket"成为可实现的幂等。
5. **人的消息优先。** 并发有 worker slot 上限,但给人留**一个额外 slot**:人唤醒已有 Ticket 或问状态时,不会被新工作的队列堵住(`docs/003-execution.md`)。
6. **执行器要"能被打断"。** worker preset 把前台 shell 命令在 5 秒后转入后台,让 Executor 能收到新消息;后台工作每轮最多 30 分钟,到点杀 job(子代理可继续),报告里写清杀了什么。这是"长任务 + 人随时插话"的折中。

另外两个工程判断:**Source 自己记读取位置**(重启不重放事件);**prepare 命令**(通常是 `git worktree`)在第一次 Assignment 前跑一次、十分钟超时,失败即 Ticket 失败——隔离目录是部署的责任,不是模型的责任。

## 它如何被利用(四条缝)

上游把"可复用"与"属于部署"分得很清楚(`docs/001-domain.md` 的 "What is reusable"):

- **可复用**:领域概念与规则;
- **属于部署**:Source 实现、Policy 内容、Executor、Channel 实现。

实际发生的利用方式(详见 [分线册](README.md)):

| 方式 | 谁 | 复用了什么 |
|------|----|------------|
| 整树 fork | local / desktop / adapt / ctrl439 / HiSeax | 领域模型 + 全部 Source/Executor + 部署面改造 |
| vendor 内核 | open-a2a-net | `src/superagent/upstream/` 原样搬入,外层换 A2A |
| 吃运行契约 | trace / wechat-source / power | `orchestrator.sqlite`、`stateDir`、Source、profile/bridge |
| 只借设计 | mycf711 / nattocb / imperial | 分层与"人只在拍板时出现"的原则 |

## 界面体验

上游的界面不是"聊天窗",是 **DSH Web 侧栏里的 Superagent 面板**(`docs/005-panel.md`)。面板按三个问题排序:**现在有没有事需要我 → 系统健康吗 → 某件事从 Trigger 到 Ticket 的历史**。

- 六个 Tab:**Overview / Source / Trigger / Eval / Execution / Settings**;Overview 只放"需要人处理的 Ticket、系统问题、24 小时计数、Executor 负载",每块都能点进详情。
- **Quiet by default**:健康状态不占空间;需要人的行直接给动作(Retry / Evaluate again / 打开 Ticket);破坏性操作要确认;计数必须等于它链接的列表长度("honest state")。
- **失败时看到什么**:启动/配置问题在 Overview 与 Deployment 里给出"缺什么 + 去哪个设置",并提供 Check again;Source 页解释"对话消失了"还是"Source 不再监听";被 Source 过滤的消息也能在 Trigger 页找到。
- **搜索**:按文本/id/飞书 message id/GitHub 链接找 Trigger,按 `#12` 或 URL 找 Thread,按标题找 Ticket。

一句话:**它把"agent 在干什么"做成可审计的工作台,而不是日志窗口。**

## 用户交互的思路

- **入口是消息,不是命令**:人在 GitHub issue/PR 评论或飞书里说一句;Source 把它变成 Trigger,Eval 判断"这是不是新工作",接受才建 Ticket 并回执。
- **工作单位是 Ticket,不是会话**:每条 Ticket 有自己的 worker 会话与目录;人可以换会话、恢复、移交,工单不丢。人只在三种时刻被叫:**被问(Attention)、结果待审(ready)、失败/阻塞**。
- **面板是监督面**:人可以在 Execution 里 Pause processing、Retry、看 Assignment;在 Eval 里看"为什么接受/忽略"及命中的规则;在 Settings 里改 Policy/Execution/Prompts,每块有保存历史。
- **说话克制**:机器人只在"人必须行动"或"结果可用"时回话;后续讨论通过 Subscription 到达工单,不重新走授权。
- 与普通 coding chatbot 的差别:交互对象从"一段对话"变成"一条可授权的工单 + 一条可审计的决策链";面板回答"为什么它做了这件事",而不只是"它说了什么"。

## 代价与边界

1. **它自己说不要上生产。** README 明写 research prototype、可能仍有 bug、风格不一致;`docs/000-philosophy.md` 也把"操作者的责任"写得很重。
2. **Unix 假设。** 上游实践里依赖 `fcntl`、`tmux`、`#!/bin/sh`、`bash` 工具、`/…` 路径;Windows 上要另做适配(HiSeax 的全部工作由此而来)。
3. **单仓、单团队。** 一个实例服务一个 GitHub 仓库(可选飞书);多仓要另做(ctrl439 的 `docs/013`)。
4. **私有、无版本契约。** `private: true` + 不发 npm,意味着没有"依赖某个版本"这回事;所有下游只能 fork 或 vendor,升级靠人工 diff。
5. **权限模型是"信任操作者"。** worker 以 OS 用户执行命令、无审批;`blockedCommands` 这类限制在 Windows 上对 worker 不生效(HiSeax README 的 "not a good fit" 明确承认)。这是"能不能用"的边界,不是"好不好用"。

## 证据与复现

```sh
git clone https://github.com/deepseek-ai/dsh-superagent && cd dsh-superagent
git checkout 8c32a9d
cat package.json SETUP.md
ls docs && wc -l docs/*.md
find src -name '*.ts' | wc -l          # 92
find src -name '*.ts' -print0 | xargs -0 cat | wc -l   # 12390
find tests -name '*.ts' | wc -l        # 53
```

关键证据:`docs/001-domain.md`(概念与 rejected concepts)、`docs/002-authorization.md`(两条路径/强度)、`docs/003-execution.md`(阶段/Executor/并发)、`docs/008-cookbook.md`(加 Source)、`README.md`(定位与免责声明)。

## 未验证 / 待答

- **上游是否接受外部 Source 回流**:adapt 的 README 说上游 issues/PR 关闭;`docs/008` 又教人加 Source——"可扩展"是文档承诺还是维护者实践,未核。
- **文章与实现的差**:README 明说文章里部分设计未实现;具体哪几条未逐条对照。
- **为什么 `private: true`**:是"研究代码不承诺 API",还是"避免被当产品依赖",README 未解释。
- **领域模型之外**:`app/` 里的 panel/prompt/资源层未逐文件读,本文只覆盖 `docs/` 声明的模型与 `src/` 的目录职责。
