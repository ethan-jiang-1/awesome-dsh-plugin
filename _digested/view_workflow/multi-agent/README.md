# multi-agent — 多智能体编排

> 多个 agent 分工、共享任务板、按角色协作。

## 定义

插件提供多智能体的结构:团队、任务板、角色划分、仲裁。判定标准:存在"不止一个 agent"的实体与状态。

## 成员(人工确认)

| 条目 | 星标 ⚠ | 说明 |
|------|--------|------|
| NanmiCoder/dsh-agent-teams | 573 | 多智能体团队 |
| toolclub/dsh-agent-team-gui | 84 | 持久多模型小队,设置中选择,Composer 中调用 |
| omdsh-dev/dsh_workflow | 82 | 可生成/保存/治理/观测/恢复的多 agent 编排 |
| whyihaveyou/dsh-suite#plugin-team-board | 42 | Cordis service key 上的共享任务板 |
| shengsheng90/DSH-taskboard | 40 | SQLite 任务板原生覆盖页 |

## 立卡条件

≥500 星,或被 ≥5 个条目引用其任务板协议。

## 生长

这是 workflow 里**最可能长出标准协议**的分支(任务板 = 共享状态接口)。写卡时重点看:状态存在哪、冲突怎么裁决、失败怎么收敛——这正是 `_leverage/leverage-agent-collaboration` 的证据面。
