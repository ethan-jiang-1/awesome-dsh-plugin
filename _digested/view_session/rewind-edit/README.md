# rewind-edit — 回退与编辑

> 回到过去的某一步:轮次回退、消息编辑。

## 定义

对既有会话做时间轴操作:轮次回退、消息改写。判定标准:操作后会话历史发生变化,但记忆存储不新增条目。

## 成员(人工确认)

| 条目 | 星标 ⚠ | 说明 | 单卡 |
|------|--------|------|------|
| Anionex/dsh-turn-rewind | 83 | 整轮次:全树内容寻址快照 + 会话 fork(类内最高) | [01](01-dsh-turn-rewind.md) ★★★ |
| Moeblack/dsh-message-edit | 32 | 消息级:每次编辑分叉真实会话,版本树读时投影 | [02](02-dsh-message-edit.md) ★★★ |
| limbo947/dsh-recall-plugin | 21 | 逐消息:影子 git 标签 + 官方 fork,文件与对话一起退;下载 1,105 | [03](03-dsh-recall-plugin.md) ★★★ |

## 立卡条件

≥300 星,或与检查点/快照机制形成组合。

> 本轮破例:83/32/21 均未达 300;按"类内头部 + 三条互不相同的回退路线"立卡。门槛未变。

## 生长

**三条路线不可比**:

- **turn-rewind** 的状态权威在插件自己的 Change Ledger(全树快照),文件还原走自己的引擎、会话侧借宿主 fork;能还原工作树,但工具副作用/网络/进程/refs 不可回退。
- **message-edit** 的状态权威在宿主 session 日志(前缀 seed),版本树是 `parentSession` 的读时投影;保留源历史且不删分支,但没有测试、最后 push 停在 2026-08-16。
- **recall-plugin** 的状态权威在插件自己的**影子 git**:每条用户消息一个 `snap-<messageId>` 标签(孤儿提交 + 完整树),所有命令用 `--git-dir=<store>/git/.git --work-tree=<root>`,**不碰项目 `.git`/HEAD/index/refs**;会话侧从不改日志,撤回 = 官方 `sessions.fork({atSeq=该消息前最近 turn/end})` + `archiveSession`。它是三者里唯一"文件与对话一起退、且标签保留可反复回退到同一点"的实现。

三者的共同空白是**工具副作用**:文件能还原,网络请求、外部进程、git commit/refs 都不在回退范围。这也是"回退"在本领域无法成为安全边界的原因。
