# replace-shell — 换壳

> 替换 DSH 的完整界面:把 web UI 换成终端全屏 TUI 或其他形态。

## 定义

插件接管整个呈现层,DSH 变成另一个界面。判定标准:卸载后界面消失,不是"少一块"而是"换一套"。

## 成员(人工确认)

| 条目 | 星标 ⚠ | 说明 |
|------|--------|------|
| ccch1mneyyy/dsh-TUI | 2009 | Claude Code 风格全屏终端 UI([01-dsh-tui](01-dsh-tui.md) ★★★) |
| huiliyi37/dsh-tianshu-tui | 217 | **宿主进程内换壳**:ANSI 引擎接管终端,自己管 live 区/scrollback、零 IPC([02-dsh-tianshu-tui](02-dsh-tianshu-tui.md) ★★★) |

**成员横向对照**:dsh-TUI 下载/星 ≈ 8.4(16959/2009),tianshu-tui ≈ 8.1(1763/217)——两条都"装机相对围观偏低",量级几乎一样。

## 立卡条件

≥1000 星,或成为某类用户的事实入口。

> 本轮破例:tianshu-tui 217 星未达 1000;按"第二套实现 + 另一条换壳架构(进程内 vs 独立进程)"立卡。门槛未变。

## 生长

换壳是一条**独立路线**,与 enhance-shell 不可比:换壳的代价是接管全部渲染与交互(更新跟随宿主 API 断裂),收益是完全控制体验。两条路线的优劣判断要分开写,不要混在一张表里排名。

**换壳内部也分两条实现路线**:

- **dsh-TUI**:自己起进程、自己组 profile;依赖宿主的**装载语义**(profile / bundle patch / 行 id / loader 行为 / `session/event`)。
- **tianshu-tui**:宿主进程内的 profile bundle,拿到的是同一个 Cordis `Context`;没有 IPC、没有重连,复用宿主 session/agent,自己写 ANSI 引擎接管终端——**live 区增量重绘 + 行级 diff + CPR 自愈 + 稳定前缀 append 进 scrollback**。代价换成进程内耦合:宿主 API 一断,界面直接起不来。

前者是"在外面再包一层",后者是"在进程里换掉呈现层";两者都能换壳,但失效面不同。

## 路线对照(换壳 vs 增强壳)

| | 增强现有壳([enhance-shell](../enhance-shell/README.md)) | 换壳(dsh-TUI) |
|---|---|---|
| 做法 | web UI 里加侧栏 / Tab | 自己起进程、自己组 profile |
| 依赖宿主的什么 | 一个注册点(Tab API) | **装载语义**:profile / bundle patch / 行 id / loader 行为 / `session/event` |
| 失效时的表现 | 少一块面板 | 整个界面起不来 |
| 兼容成本 | 跟随 web 客户端 API | 跟随 ~40 个官方包的版本线(peerDependencies 逐版本枚举) |
