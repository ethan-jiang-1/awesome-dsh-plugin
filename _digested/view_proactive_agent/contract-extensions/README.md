# contract-extensions — 吃运行契约,不搬代码

> D2 层:仓库里没有上游源码,但依赖它的事实契约——`stateDir`、`orchestrator.sqlite`、Source 接口、profile 进程与 `bridge.js`。**本子分类 3 个成员,已立 1 张(trace);wechat-source、power 留待下一轮。**

## 定义

满足任一条即可:

1. 读上游写下的数据(`orchestrator.sqlite`、会话日志、`stateDir` 下的文件);
2. 实现上游的扩展接口(`SourceKind`:配置/scope/policy/channel/threadContext);
3. 与上游的 profile/进程生命周期对接(同 `homePath`/`profileName`/密钥,注册 `bridge.js`)。

**共同风险**:这些契约没有版本号,上游改形状时不会报错,往往表现为"页面正常、数据为空"或"起不来"。

## 成员

| 条目 | 星标 | 吃哪条契约 | 机制 | 页 |
|------|-----:|------------|------|----|
| luckyxiang6688/dsh-superagent-trace | 0 | `orchestrator.machine.stateDir` + `orchestrator.sqlite` 6 张表 + 会话日志 | 只读回看:来源页、泳道时间线、裁定/派工/工具调用;还复刻了上游 stage/reason 规则 | [FAQ](../../../_faq_on_digested/02_superagent-dependents/lines/07-observability-trace.md) |
| luckyxiang6688/dsh-superagent-wechat-source | 0 | `SourceKind` + 自己的 `stateDir` | 微信私聊 → Trigger;扫码绑定、白名单默认空、纯文本一对一 | [FAQ](../../../_faq_on_digested/02_superagent-dependents/lines/08-wechat-source.md) |
| MingoYung/dsh-superagent-power | 0 | profile 身份 + 进程内服务 + `bridge.js` | 输入栏 Sup 开关:起停独立 Super-agent profile 进程,失联不误报关闭 | [FAQ](../../../_faq_on_digested/02_superagent-dependents/lines/09-process-power.md) |

## 读法

- **它读什么**:表名/字段/服务名要具体;只写"读数据库"不算证据。
- **失败模式**:读不到时是静默空、显式报错、还是降级?trace 的选择是"说明原因,不显示空数据";wechat-source 的失败是"没有回执";power 的失败是"进程探测不到"。
- **写不写**:只读插件(trace)与写插件(wechat-source 写事件/工单;power 写进程状态)风险不同;写操作是否绕过上游授权,是必查项。

## 立卡条件

默认 ≥500★ 或被 ≥5 个条目引用其契约;本层无人达标。已按机制例外立 **trace**:它是唯一把"黑箱变白盒"做成只读工具的样本,且把"内部表 → 对外视图"的代价暴露得最清楚。wechat-source 与 power 更像渠道/生命周期样本,下一轮再评估。
