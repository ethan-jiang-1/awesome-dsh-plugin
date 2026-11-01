---
title: "CARRIERS · 九类载体：它在旅程哪一步、用什么碰宿主"
domain: lifecycle
kind: charter
positioning: "按“阶段 × 载体”给插件分类；每类的判定依据都落在包清单或源码符号上，不落 README。"
read_when: "要判断一个插件属于哪类、或决定自己的产品用哪类载体。"
status: living
updated: 2026-11-01
budget: 140
---
# 九类载体

> 产品册按"它长什么样"分（壳 / 内容 / 驾驶舱…）。本册按**"它在旅程的哪一步、用什么载体介入"**分。`data/plugins` 的 `category`（ui / remote / tools）在这里没有用。

## 1. 阶段（轴 A）

| 十位 | 阶段 | 它回答 |
|---|---|---|
| `1` | 装 | 用户怎么把它弄进来 |
| `2` | 起 | 装完怎么让它生效 |
| `3` | 配 | 它的默认值与用户覆盖住在哪 |
| `4` | 首启 | 第一次打开看到什么 |
| `9` | 反例 | 以为能行、实际不行的 |

## 2. 载体（轴 B）

| # | 载体 | 判定依据（**只用包清单或源码**） | 强度 |
|---|---|---|---|
| 1 | 纯 host 行 | `dsh.bundle` 有、`dsh.client` 无 | 最弱，只加能力 |
| 2 | 客户端槽位 | `dsh.client` 有；源码无 `webServer.register` | 界面 |
| 3 | 首屏注入 | 源码有 `tapIndex` / `index-inject` | 强 |
| 4 | 自有路由/页 | 源码有 `webServer.register(` | 强 |
| 5 | 命令入口 | 源码有 `commands.register` | 中 |
| 6 | **boot hook** | 源码有 `agents.create` / `workspaceRegistry` / `workingDirectory` | **最强** |
| 7 | 自带 CLI | 包清单有 `bin` | 强，代价高 |
| 8 | 自带安装器 | 发行物有 dmg / msi / exe（**只能到 README/Releases，不进源码判定**） | 最强，代价最高 |
| 9 | 自带运行时 | 发行物含 Node / 运行时 | 最强，代价最高 |

**读法**：1–6 都在"宿主替我兜分发"这一侧；7–9 越往右，越是在说"分发也归我"。7 以上就该问一句：**是否真的需要**。

## 3. 派生规则（怎么从机器事实走到分类）

```text
拉 npm manifest
  ├─ 无 dsh.bundle → 不是 bundle，最多算"普通依赖"（装完不成层，见 TRAPS §1）
  ├─ 有 dsh.bundle + 无 dsh.client → 载体 1
  ├─ 有 dsh.client → 至少载体 2；再 grep 源码决定 3 / 4 / 6
  ├─ 有 bin → 叠加载体 7
  └─ README/Releases 有安装包 → 叠加载体 8；含运行时 → 9
```

**源码 grep 的符号表**（只认这些，其他一律不算）：

| 符号 | 说明 |
|---|---|
| `tapIndex` / `index-inject` | 首屏注入 |
| `webServer.register(` | 自有路由 |
| `commands.register` | 斜杠命令 |
| `agents.create` / `workspaceRegistry` / `workingDirectory` | boot hook |
| `pluginManager.installBundle` | 自带安装面 |
| `webserver/index-inject` | 行级注入（与 tapIndex 同族，标注区分） |

## 3.1 符号表不是穷尽的

`[SRC-TARGET]` `dsh-isolation-gate@1.13.7` 在 §3 的符号表上**零命中**：它的 HTTP 路由用字符串常量拼出（`lib/index.js` 里的 `/__dsh-isolation-gate/*`），没有走 `webServer.register` 的正则形态。

**兜底规则**：符号表 grep 不到时，**以 patch 顶部声明的路由/能力清单为准**，并在 memo 里写明"符号表失效"以及替代判据。不要因为 grep 为空就判"无载体"。

## 4. 矩阵（随样本增长）

> 格子里的数字是**已立样本数**。空格子就是下一轮选题；空格超过三个阶段说明普查方向偏了。

| 载体 \ 阶段 | 装 | 起 | 配 | 首启 |
|---|---|---|---|---|
| 1 纯 host 行 | 3（`install/12`、`install/13`、`install/14`） | 1（`boot/23`） | 3（`config/31`、`config/32`、`config/33`） | — |
| 2 客户端槽位 | — | — | — | — |
| 3 首屏注入 | — | 1（`boot/21`） | — | — |
| 4 自有路由 | — | 1（`boot/22`） | — | — |
| 5 命令 | — | 1（`boot/25`） | — | 1（`first-run/42`） |
| 6 boot hook | — | — | — | 1（`first-run/43`） |
| 7 自带 CLI | 1（`install/11`） | 1（`boot/24`） | — | 1（`first-run/41`） |
| 8 自带安装器 | — | — | — | — |
| 9 自带运行时 | — | — | — | — |

> **现状（15 张阶段样本落地后）**：9 类载体用了 **6/9** 类——host-row 7 张（装 3 / 起 1 / 配 3）、own-cli 3 张（装 1 / 起 1 / 首启 1）、command 2 张（起 1 / 首启 1）、首屏注入 1、自有路由 1、boot hook 1，合计 15 张。另有 `negative/91` 反例一张，不计入本矩阵。
> **空着的是 8「自带安装器」与 9「自带运行时」**——按本册 [`00-map`](../00-map.md) §0 的定调，这两格本来就该稀薄：它们是"分发也归自己"的形态，不是插件该走的路。

## 5. 两条使用纪律

1. **一个样本只填一格**：它最主要的介入点；其余写进卡内"兼看"。
2. **分类不许从描述推断**：`零配置`、`开箱即用`、`一键` 这类词只能让人进入候选，不能产出 class。
