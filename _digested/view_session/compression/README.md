# compression — 上下文压缩

> 把长会话压进有限窗口:摘要、折叠、可逆恢复。判定标准:改变历史/上下文在模型请求里的**表示**,而不是只做检索、注入或存储。

## 定义

在宿主与模型 API 之间压缩会话历史:把已消费的轮次折成摘要、可逆地覆盖渲染、或按策略丢弃;目标是长会话不撞窗口、少花 token,同时尽量不破坏前缀缓存。与 `context-shaping` 的区别是:这里改的是"请求里历史的表示",那边改的是"这一轮额外注入什么"。

## 成员(人工确认)

| 条目 | 星标 ⚠ | 说明 | 单卡 |
|------|--------|------|------|
| ranxianglei/billion-context | **无记录(采样缺口)** | 本地压缩代理 + `acp-kernel`;DSH 侧用两行 bundle 条目抢压缩车道并关掉宿主原生自动压缩;可逆 decompress | [01](01-billion-context.md) ★★★ |

> ⚠ 该条目在 2026-08-19 星标边车里没有记录,**不是 0**;2026-11-18 实时 7,806 属主项目(22 个宿主),不是 DSH 适配层热度。npm 周下载约 93.5 万(2026-11-10~16,卡内实测)。

## 立卡条件

≥300 星,或被 ≥3 个条目引用其压缩协议。

> 本轮破例:边车无星标记录;按"实时 7,806(主项目)+ 6 条 registry 衍生 + 93.5 万/周下载"立卡。门槛未变。

## 生长

**它不是"一个压缩插件",是"代理 + 内核 + 每宿主薄适配"**:

- **代理**:插件自己 spawn 的本地 HTTP 代理进程,监听 ephemeral 端口,带 parent-pid watchdog;夹在宿主与模型 API 之间改写请求/流。
- **内核**:同仓 `kernel/` 的 `acp-kernel`(26,229 行);模型写摘要、内核只编排;三层 LSM block,原文不删只覆盖渲染,`decompress` 可逆。
- **DSH 适配**:`dsh.bundle.patch.yml` 55 行 + 宿主侧 4,694 行 TS;`bili-native` 管 plan/fetch、WS 拦截、工具注册与 `/acp`;`bili-compaction-gate` 是 `inject=[]` 的独立常驻 entry,只提供 `biliBasicCompactionPolicy`,并用 cordis INTERNAL 的 `internal/config` waterfall 把预设里嵌套的 compaction 行改成 `disabled`。**独立常驻是为了禁用 `bili-native` 时预设回落到宿主原生压缩,而不是永久 pending 把新会话砖掉**(#3662 事故复盘)。

**归属要拆清**:采样日(2026-08-19)比首个 DSH 提交(2026-09-18)早 30 天,星标在结构上不可能包含 DSH 增量;它的 7,806 星与周下载都属于主项目。

**跨类边界**:DSH 原生 ACP 曾有一个实现(`billion-context-dsh`),2026-10-24 已停维护并指向上游 `ranxianglei/billion-context`,因此不立卡;本子分类只收仍在维护、真正"改写请求表示"的实现。
