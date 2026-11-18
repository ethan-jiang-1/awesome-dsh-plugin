# enhance-shell — 增强现有壳

> 在 DSH 现有界面上加东西:侧栏、Tab、注记、导航条、状态标签。不替换宿主界面。

## 定义

插件挂进已有 UI 的扩展点(slot / Tab 注册 / 装饰),用户的界面骨架不变。判定标准:卸载后原界面仍可用,只是少了一块。

## 成员(人工确认的头部例子,非全量归类)

| 条目 | 星标 ⚠ | 说明 |
|------|--------|------|
| omdsh-dev/DSH-better-sidebar | 2216 | 侧栏工作台,63 个第三方插件往它的 Tab 注册(平台级) |
| ZSeven-W/dsh-openpencil | 119 | 设计预览与编辑 |
| omdsh-dev/dsh-annotation | 76 | 选区批注 |
| whiteguo233/dsh-openbiliclaw | 45 | 右侧抽屉面板 |
| vlln/dsh-navbar | 41 | 会话节点导航条 |
| alingalingling/ui-status-label | 38 | 状态标签自定义 |

## 立卡条件

≥500 星,或被 ≥5 个第三方条目点名(扩散信号)。

## 生长

这是 ui 里**最容易长出平台**的分支(better-sidebar 已证明):插件越多地往同一扩展点注册,那个扩展点就越接近标准。新卡优先看"被多少人接入",不是星标。
