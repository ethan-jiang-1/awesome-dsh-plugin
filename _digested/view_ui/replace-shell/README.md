# replace-shell — 换壳

> 替换 DSH 的完整界面:把 web UI 换成终端全屏 TUI 或其他形态。

## 定义

插件接管整个呈现层,DSH 变成另一个界面。判定标准:卸载后界面消失,不是"少一块"而是"换一套"。

## 成员(人工确认)

| 条目 | 星标 ⚠ | 说明 |
|------|--------|------|
| ccch1mneyyy/dsh-TUI | 2009 | Claude Code 风格全屏终端 UI([02-dsh-tui](02-dsh-tui.md) ★★★) |
| huiliyi37/dsh-tianshu-tui | 217 | 另一种 TUI 实现 |

**成员横向对照**:dsh-TUI 下载/星 ≈ 8.4(16959/2009),装机相对围观偏低;tianshu-tui 无下载边车数据。

## 立卡条件

≥1000 星,或成为某类用户的事实入口。

## 生长

换壳是一条**独立路线**,与 enhance-shell 不可比:换壳的代价是接管全部渲染与交互(更新跟随宿主 API 断裂),收益是完全控制体验。两条路线的优劣判断要分开写,不要混在一张表里排名。

## 路线对照(换壳 vs 增强壳)

| | 增强现有壳([enhance-shell](../enhance-shell/README.md)) | 换壳(dsh-TUI) |
|---|---|---|
| 做法 | web UI 里加侧栏 / Tab | 自己起进程、自己组 profile |
| 依赖宿主的什么 | 一个注册点(Tab API) | **装载语义**:profile / bundle patch / 行 id / loader 行为 / `session/event` |
| 失效时的表现 | 少一块面板 | 整个界面起不来 |
| 兼容成本 | 跟随 web 客户端 API | 跟随 ~40 个官方包的版本线(peerDependencies 逐版本枚举) |
