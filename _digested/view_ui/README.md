# view_ui — 界面与交互

> 已立册(2351 条 / 本期新增 812 / owners 2017、单件 88%;门槛为默认值,定义见 [`../AGENTS.md`](../AGENTS.md) §二)。
> ⚠ 星标为历史采样。数据截止 `29b3ed46e`(2026-11-18)。

## 快照

本期 2351 条(20.0%,全表最大类);上期 1558 → 净 +793,占比 +0.4pp,匀速扩张。owners 2017,单件作者 88%——多人真热闹。

## 锚(存量头部,⚠ 星标历史采样)

| 条目 | 星标 | 说明 |
|------|------|------|
| omdsh-dev/DSH-better-sidebar | 2216 | 类内唯一 2000+;作者系 omdsh-dev(跨 ui/notify/browser/tools 的系列化生产者,见 [03-anchors](../_view/03-anchors.md))([01](enhance-shell/01-better-sidebar.md) ★★★) |
| ccch1mneyyy/dsh-TUI | 2009 | 终端 UI 方向的代表([01](replace-shell/01-dsh-tui.md) ★★★) |
| FSMargoo/dsh-at-file | 394 | 输入框 `@` 文件引用;官方 0.2.1 已内置 `@file`,本插件被取代并疑似在 0.2.1-rc.5 上 Host 半加载失败([02](enhance-shell/02-at-file.md) ★★★) |
| omdsh-dev/dsh-genui | 224 | 同作者第二锚;模型写 `dsh-ui` JSON 围栏,宿主渲染 React 树([01](inline-genui/01-genui.md) ★★★) |
| huiliyi37/dsh-tianshu-tui | 217 | TUI 方向第二例 |

## 子分类(册内目录)

| 子分类 | 定义 | 成员数(已确认) |
|--------|------|----------------|
| [enhance-shell](enhance-shell/README.md) | 增强现有壳:侧栏、Tab、注记、导航 | 7 例,平台型已出现 |
| [replace-shell](replace-shell/README.md) | 换壳:接管整个界面(TUI) | 2 例 |
| [inline-genui](inline-genui/README.md) | 内联生成式 UI:模型在回复流渲染组件 | 3 例 |

单卡落在子分类目录内:`<子分类>/NN-<slug>.md`;本册已有 5 张单卡(enhance-shell 3、replace-shell 1、inline-genui 1),全部 ★★★。

## 本期动向

新增 812 条为全表之最;新增侧暂无星标读数(采样缺口)。新 owner 榜里 imcaibaicai(ui×3)、stallenlu、TLEWA、fujingzhai、AvenYQ(ui×4)都以 ui 为主落点——**ui 是新作者进场的第一落点**,与「做壳门槛最低」的档案结论([ecosystem/01](../ecosystem/01-scenario-taxonomy.md))一致。

## 稳定性判读

盘子大、头部锚成型(双 2000+ 星)、多 owner 供给——**ui 是当前生态最成熟的领域**;次级梯队(394 星以下)断层明显,中部空心。

**五张单卡读完后,"成熟"的含义要补一层**:头部仍然稳固,但**常见交互正在被宿主收编**——at-file 的 `@` 文件引用已被官方 `@file` 取代,并因 `ctx.settings.register` 在 0.2.1-rc.5 上消失而疑似 Host 半加载失败;genui 没有走"通用组件库"路线,而是自定 `dsh-ui` 围栏协议 + 60 个组件的渲染器,把成本压在维护面。判断:ui 的竞争重心正从"加一块面板"转向"协议/渲染器/外部工具适配";中部的空心,一部分是宿主内置能力填掉的。
