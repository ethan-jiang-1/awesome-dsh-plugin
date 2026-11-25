# Q02 · 到底有多少 DSH 插件依赖 `dsh-superagent`?

## 问题

注册表里带 `superagent` 字样的条目有 16 个,但 `superagent` 是个被用滥的词:检索工具、子代理选档、会话唤醒都叫 superagent。真正的问题是:

1. **有多少条目真的依赖 `deepseek-ai/dsh-superagent` 这个上游原型**?依赖的是代码、运行契约,还是只借了"Router–Worker"这个设计?
2. 这些条目**各自利用了它的哪一面**——Source、Policy、Ticket、会话/worktree 隔离、`orchestrator.sqlite`、profile 进程,还是仅仅在同一个领域里另起炉灶?
3. 它们在**解决什么问题**?为什么有人宁可分叉/复刻,也不直接装上游?
4. 其中**有没有值得单独写一张卡的影响力条目**?

## 背景:上游是谁

`deepseek-ai/dsh-superagent`(仓库已改名 `deepseek-ai/dsh-superagent-prototype`)是 **DeepSeek Harness 团队**发布的研究原型,不是社区投稿:

- 包名 `dsh-superagent@0.1.0`,`private: true`,**不发 npm**——所以不存在"在 package.json 里写一条 npm 依赖"这种普通依赖形态;
- MIT,README 自述 "Research prototype for reference only, not an official DeepSeek product";
- 形态是 DSH **bundle**(自带 `cordis.patch.yml`),职责:监听 GitHub(可选飞书)→ Policy 裁定 → 开 Ticket → 在独立 DSH 会话与目录里执行 → 回原对话(评论/PR);
- 影响力:约 **24.5k★ / 3.1k forks**(2026-11-25 实时),但它**不在** `data/plugins/` 注册表里,所以"注册表内谁依赖它"不能靠读一条 upstream 条目回答。

## 口径:什么算"依赖"(四层,从严到宽)

| 层 | 定义 | 判定证据 |
|----|------|----------|
| **D1 代码级** | 同包名 `dsh-superagent`、同 plugin id、源码分叉、直接 import 其导出(含 `./github-watch`、`./feishu-watch` 子路径) | `package.json` 名字/deps、plugin id 比对、与 upstream 的 diff/致谢、源码痕迹 |
| **D2 契约级** | 不复制源码,但依赖它的运行契约:读 `orchestrator.sqlite` 或会话日志、注册进它的 profile、依赖其 Policy allow-list / Ticket / HTTP 路由 / panel slot / prompt/skill 目录、随包提供 `bridge.js` | 数据文件名、profile 配置、路由路径、slot 名、setup 文档 |
| **D3 设计级** | 实现同一 Router–Worker 思路(Source→Ticket→隔离会话/worktree→回原对话),但仓库里没有任何 upstream 代码/包/数据/契约引用;README 明确"实现该设计"也算 | 架构描述 + 空白证据(无依赖、无同名 id、无同名文件) |
| **D0 无关** | 只是名字含 superagent(检索工具、子代理选档、会话唤醒) | 功能与机制都不在同一层 |

**"依赖"只算 D1+D2;D3 是"同设计",单列,不能混进依赖数。**

## 影响力口径

- 上游自身:GitHub stars/forks(宿主/机构背书,与社区插件不可比);
- 依赖者:实时 stars/forks、注册表条目数、社区提及(README/描述)、是否有可用下载数(npm 私有,多数为 0);
- **不用**冻结边车(`data/stars.json` 停在 2026-08-19,对这批判条目几乎无覆盖)当"当前影响力"。

## 方法(可复现)

1. `grep -ril 'superagent\|super-agent\|super_agent' data/plugins` → 16 个候选(基线 `main@8f1a1800e`,13136 条);
2. 每个候选浅克隆到 `/tmp/sa-research/<slug>`,固定到当时 HEAD,读 `README`、`package.json`、`cordis.patch.yml`、`git log -5`,并 grep `dsh-superagent|orchestrator\.sqlite|bridge\.js|plugin id`;
3. 与上游 `deepseek-ai/dsh-superagent-prototype@8c32a9dc` 比对包名、plugin id、源码结构与数据契约;
4. 用 GitHub API 取实时 stars/forks/pushed_at(不复用冻结边车);
5. 按上表分层;边界案例(如"只借设计但名字相同")单列并写判定理由。

## 候选(16 个,按注册表类目)

| 仓库 | 类目 | 为什么被初筛命中 |
|------|------|------------------|
| 439436269-ctrl/dsh-superagent | workflow | 同名上游的 bundle,自述 GitHub+飞书/钉钉/企微 |
| DASHAN-0079/dsh-superagent-adapt | workflow | 自述"把 dsh-superagent 原型适配到 0.2.2-rc.3" |
| jinghuaihuaxiang-star/dsh-superagent-desktop | workflow | 自述"团队原型的桌面 bundle 分支" |
| mengzhongjie/dsh-superagent-local | workflow | 自述"dsh-superagent 的本地版",包名/id 与上游相同 |
| HiSeax/dsh-windows-superagent | workflow | 策略接收/工单/台账/微信飞书/看板,命名与机制同族 |
| NattoCB/dsh-plugin-superagent | workflow | 自述"项目控制台,持久工单、可替换 DSH 会话" |
| MingoYung/dsh-superagent-power | ui | 启停独立 Super-agent 进程 + `bridge.js` |
| luckyxiang6688/dsh-superagent-trace | dev | 只读 `orchestrator.sqlite` 与会话日志 |
| luckyxiang6688/dsh-superagent-wechat-source | remote | 把微信私聊做成 Super-agent 的 Source |
| shilaoban666/dsh-imperial-court | workflow | 自述"实现 DSH 的 super-agent(Router–Worker)设计" |
| NelsonLongXiang/dsh-open-a2a-net | remote | 0.8 预览含 "Superagent teams" |
| MYCF711/dsh-session-superagent | session | 会话级 superagent,盯 GitHub 唤醒会话 |
| wychmod/dsh-mini-superagent | agi | 任务派发 + 工作台,名字带 mini-superagent |
| Yukikaze-Ai/dsh-ladder-superagents | agi | "子代理选档阶梯",名字带 superagents |
| superagents-lab/dsh-s1 | browser | 组织名带 superagents,实为检索工具 |
| LittleChenLiya/dsh-superagent | workflow | 同名,自述并行子任务/合成报告 |

## 预期产出

- [answer.md](answer.md):分层计数、每个依赖者用了哪一面、解决什么问题、设计思路与代价;
- 若存在有影响力的依赖者,另写一张独立单卡(标题、事实、机制、代价、证据),并在 answer 里链接。
