# import-export — 会话导入导出

> 把会话搬进来、带出去:聊天记录导入、会话导出。

## 定义

会话数据的出入口:导入历史聊天、导出会话记录。判定标准:数据跨越 DSH 边界(进出),而不是在会话内编辑。

## 成员(人工确认)

| 条目 | 星标 ⚠ | 说明 | 单卡 |
|------|--------|------|------|
| Nwflower/dsh-chat-import | 71 | 38 种来源格式 → 可续聊会话;反向导出 4 格式(registry 自称 13 家,落后代码两代) | [01](01-dsh-chat-import.md) ★★★ |
| whyihaveyou/dsh-suite#plugin-session-export | 42 | 458 行单文件,把 **live** session 日志投影成散文 MD/HTML;按事件类型分组,重启后导不出历史 | [02](02-dsh-session-export.md) ★★★ |

## 立卡条件

≥300 星,或被 ≥3 个条目引用其格式。

> 本轮破例:71/42 星、都被 0 个条目引用;按"chat-import 的下载量 session 类第一 + session-export 是类内 ⚠ 第三"立卡。门槛未变。

## 生长

源码确认这是**两种完全不同的东西**:

- **导入是兼容层**:37 个发现源 + 1 个显式 `local-jsonl`,42 个纯函数转换器,最终把各家存储契约翻译成 DSH 事件日志。跨插件面只有未标准化的 registry JSON 与可选 `chatImport` 服务。
- **导出是投影**:只走 `ctx.sessions` 的 live 会话,按事件类型 `switch` 挑 8/63 种事件渲染成散文;`user/message.source`、`surfaceOp`、附件、`event.time` 全部丢弃。HTML 自包含且转义完整,Markdown 完全不转义。README 说"按轨迹来源分组",代码里没有这个字段。

**所以零扩散是结构性的**:导入是"一次性迁移",导出产出的是散文而不是带 schema/版本/服务接口的"格式";`session-export` 簇有 6 个互不相干的实现,彼此零引用——用了也没法引用,不是没人用。
