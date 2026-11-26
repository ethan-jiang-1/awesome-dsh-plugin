# design-derivatives — 只借领域模型,另写实现

> D3 层:仓库里没有上游代码、没有 `stateDir`/`orchestrator.sqlite`/Source 契约,但在文档、结构或提示词层面明确以 `dsh-superagent` 的领域模型为起点。**本子分类 3 个成员,已立 1 张(MYCF711);NattoCB、imperial 留待观察。**

## 定义

同时满足:

1. 自述或代码注释点名上游设计(不是只叫 superagent);
2. 保留上游至少两个核心概念(如 Router/Worker、Ticket、人只在拍板时出现);
3. 反证:无同名包/id、无 vendored 目录、不读上游数据、不注册 `bridge.js`。

**为什么单列**:设计衍生能说明"这套语义能不能脱离原实现成立",但它们对上游没有依赖边——不能算进"9 个真依赖"。

## 成员

| 条目 | 星标 | 保留了什么 | 丢了什么 | 页 |
|------|-----:|------------|----------|----|
| MYCF711/dsh-session-superagent | 52 | 会话级唤醒 + 单 Ticket 的"守";`worker` 模式才建独立 Session | Ticket 作为可移交主体、Mandate 版本、Subscription 扇出、结构化 Report 四态 | [FAQ](../../../_faq_on_digested/02_superagent-dependents/lines/10-session-level.md) |
| NattoCB/dsh-plugin-superagent | 0 | 持久工单 + 可替换 DSH 会话 + 项目矩阵 | 上游的 Eval/Policy/Mandate;工单状态部分跟随会话 | 未单开页(低影响) |
| shilaoban666/dsh-imperial-court | 2 | Router–Worker、人只在拍板时出现、隔离 worktree/分支 | 上游的 Source/Channel;执行体是自己的多 CLI + 三省六部审查 | 未单开页(独立产品) |

## 读法

- **保留/丢弃表比功能列表有用**:D3 的价值在"哪条语义被证明可省"。MYCF711 的 `official-decomp` 明写 v0.9"不复制完整 Ticket 状态机",v2.0 又补回五个房间——这是被文档记录下来的设计漂移。
- **确认点在哪**:imperial 把"批红"做成唯一合并闸;MYCF711 把确认前移到"装守"和 "ack";NattoCB 的中间态由 DSH 会话事件改写。三种交互,对应三种授权粒度。
- **不拿星标当依赖证据**:52★ 的 MYCF711 也不在同批任何一条依赖边上。

## 立卡条件

默认 ≥500★;本层最高 52★,不达标。已按机制例外立 **MYCF711**:唯一有社区量纲的 D3(52★ / 12 forks),"降级取舍"写得最清楚。另两个不立卡——NattoCB 与上游 Ticket 语义重叠,imperial 是独立产品,放进本册只为记录"设计可脱离实现"。
