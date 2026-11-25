# 分线册 · 每条"明显依赖或衍生"各一页

> 入册标准:**必须能指出对 `dsh-superagent` 的明显依赖,或是它的一种衍生**。只靠名字里有 superagent、但代码/契约/设计上都对不上的,不入册(排除名单见文末)。数据基线:注册表 `main@8f1a1800e`(13136 条,2026-11-25),候选各自 HEAD,星标 2026-11-25 实时值。

## 怎么读

先看 [../answer.md](../answer.md) 的计数与判定表,再看 [../impact.md](../impact.md) 的影响面分析;这里是**逐线展开**。每条线一页,页内固定回答五问:

1. **它要解决什么问题**——谁在什么场景下疼?为什么上游不够用?
2. **它的路径是什么**——选了什么做法,放弃了哪些替代(比如"为什么不直接装上游""为什么不分叉").
3. **它如何利用 `dsh-superagent`**——具体用了哪一层:领域模型、源码、`stateDir`/`orchestrator.sqlite`、profile/`bridge.js`、Source 契约;哪些改了、哪些原样保留.
4. **技术思考是什么**——隔离/并发/状态/鉴权/失败收敛/兼容,哪一条是它的关键判断;代价换来了什么.
5. **代价与边界**——升级、权限、维护、不可用的场景.

每页 80–150 行,证据给 `file:line` 或文件路径;没读到的写"未验证",不用"应该/大概"补齐.

层级沿用 answer 的 D1/D2/D3:

- **D1 代码级**:整树分叉、或把上游 domain engine vendor 进自己的仓;
- **D2 契约级**:不搬代码,但读它的数据/挂它的 profile/实现它的 Source 契约;
- **D3 设计衍生**:以它的领域模型为起点另写实现,仓库里没有上游代码或运行契约。

## 目录

| 页 | 线 | 层 | 关系 | ★ |
|----|----|----|------|--:|
| [00-upstream-prototype](00-upstream-prototype.md) | `deepseek-ai/dsh-superagent` | 根 | 被依赖/被衍生的原型 | 24,565 |
| [01-windows-hiseax](01-windows-hiseax.md) | HiSeax/dsh-windows-superagent | D1 | 整树 fork + Windows/微信/看板 | 138 |
| [02-local-fork](02-local-fork.md) | mengzhongjie/dsh-superagent-local | D1 | 整树 fork,改成"本机工作区"版 | 11 |
| [03-desktop-fork](03-desktop-fork.md) | jinghuaihuaxiang-star/dsh-superagent-desktop | D1 | 整树 fork,桌面 bundle;npm 月下载 1,753 | 1 |
| [04-adapt-fork](04-adapt-fork.md) | DASHAN-0079/dsh-superagent-adapt | D1 | 整树 fork,适配 DSH 0.2.2-rc.3 | 0 |
| [05-multi-repo-im-fork](05-multi-repo-im-fork.md) | 439436269-ctrl/dsh-superagent | D1 | GitHub 真 fork;多仓 + IM 桥;npm 0.3.0 | 0 |
| [06-vendored-engine-a2a](06-vendored-engine-a2a.md) | NelsonLongXiang/dsh-open-a2a-net | D1 | vendor 上游 domain engine,套 A2A 壳 | 10 |
| [07-observability-trace](07-observability-trace.md) | luckyxiang6688/dsh-superagent-trace | D2 | 只读 `orchestrator.sqlite` + 会话日志 | 0 |
| [08-wechat-source](08-wechat-source.md) | luckyxiang6688/dsh-superagent-wechat-source | D2 | 实现上游的 Source 契约 | 0 |
| [09-process-power](09-process-power.md) | MingoYung/dsh-superagent-power | D2 | 管独立 profile 的进程 + `bridge.js` | 0 |
| [10-session-level](10-session-level.md) | MYCF711/dsh-session-superagent | D3 | 以原型为起点的会话级重写 | 52 |

共 **11 页**:上游原型 1 页 + 依赖/衍生 10 页。**退册两页**:`11-project-console`(NattoCB,0★,持久工单/会话边界与上游自身重叠,无独立机制)与 `12-imperial-court`(shilaoban666,2★,是独立的多 CLI 产品,既无代码/契约依赖,也无采用证据);两者仍保留在 [../answer.md](../answer.md) 的 16 行判定表里,只是不单开页。

> **硬信号补充**:03 的 npm 月下载 **1,753**、09 的 Release tgz **743+42** 次、02 有一条真实用户 issue **#1**。星标低不等于没人用;但下载/试用也不等于"依赖"——三层要分开读。

## 不入册(名字相近但无依赖/衍生关系)

| 仓库 | 为什么不收 | ★ |
|------|------------|--:|
| LittleChenLiya/dsh-superagent | 并行子任务编排/合成报告,仓库无上游引用、无同名 id、无数据契约 | 22 |
| wychmod/dsh-mini-superagent | 任务派发 + 工作台,"能力模型参考"但不实现 Source→Ticket 管线 | 4 |
| Yukikaze-Ai/dsh-ladder-superagents | 子代理模型选档,与 Router–Worker 无关 | 1 |
| superagents-lab/dsh-s1 | Search1API 检索工具,组织名带 superagents | 2 |

> 这 4 个在 [../answer.md](../answer.md) 里记为 D0;它们不计入"9 个真依赖",也不进分线册。星标最高的两个社区条目(MYCF711 52★、LittleChenLiya 22★)一个在册(D3)、一个不在册(D0)——这个反差本身就是"名字 ≠ 依赖"的证据。

## 共同口径

- **载体**:全部是 **GitHub 公开仓**(上游 `deepseek-ai/dsh-superagent-prototype` 也在 GitHub,且 `private: true` 不发 npm)。npm 上能装到 03/05/06/07/08/10(各自包名见页内);02/04 走 GitHub tarball,09 走 Release tgz。
- 星标/forks/watchers 为 2026-11-25/26 GitHub API 实时值,不引用冻结边车;
- 每页的 `repo@commit` 是该仓库被读时的 HEAD,源码证据给 `file:line` 或文件路径;
- "代价"只写能从代码/文档读到的,不推断作者意图;
- 未读部分逐页列在末尾,不用"应该/大概"补齐。
