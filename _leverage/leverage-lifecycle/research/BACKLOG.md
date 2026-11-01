---
title: "BACKLOG · 候选池（分诊结果与缺口）"
domain: lifecycle
kind: index
positioning: "42 个过影响力门的 bundle 的分诊结果：15 张待成卡、12 个备选、8 条降级为 TRAPS、6 个被拒。"
read_when: "要补样本、或想知道某个包为什么没进卡。"
status: living
updated: 2026-11-01
budget: 90
---
# 候选池

> 分诊口径见 [`RESEARCH`](./RESEARCH.md) §1。**过影响力门 ≠ 入选**；第二道门是"载体事实来自包清单或源码"。
> 分诊日期 **2026-11-01**，下载量为 npm 近 30 天，★ 为 GitHub API 实时。

## 1. 已排期（15 张）

| 批 | 包 | 阶段 | 载体 | 机制主题 | 状态 |
|---|---|---|---|---|---|
| 1 | `@wenaixi/cfbridge` | 装 | own-cli | 装后自证 | 已成卡 |
| 1 | `dsh-origin-plugin` | 装 | host-row + `!!js` | 通道与坑 | 已成卡 |
| 1 | `dsh-rhine-splash` | 起 | index-inject | 首启引导与可推迟 | 已成卡 |
| 1 | `dsh-update-checker` | 起 | web-route | 生效边界 | 已成卡 |
| 2 | `dsh-isolation-gate` | 配 | host-row | 默认值与分层 | 已成卡 |
| 2 | `dsh-free-search` | 配 | host-row | 默认值与分层 | 已成卡 |
| 2 | `dsh-tool-guardian` | 首启 | command | 首启引导与可推迟 | 已成卡 |
| 2 | `dsh-skill-cockpit` | 首启 | own-cli | 装后自证 | 已成卡 |
| 3 | `dsh-free-models-hub` | 装 | host-row | 通道与坑 | 已成卡 |
| 3 | `@zseven-w/dsh-noema` | 起 | host-row | 生效边界 | 已成卡 |
| 3 | `dsh-doctor` | 起 | own-cli | 自愈与回滚 | 已成卡 |
| 3 | `@benz-ai-x/dsh-24pa` | 首启 | boot-hook | 工作区·会话预置 | 已成卡 |
| 4 | `sage-mem` | 首启 | client-slot | 首启引导与可推迟 | 待 |
| 4 | `dsh-tinyfish` | 装 | host-row | 通道与坑 | 已成卡（改判为装） |
| 4 | `@dfy-plugins/dsh-bundle` | 配 | host-row | 迁移与导入 | 已成卡 |
| 补 | `dsh-context-guardian` | 起 | own-cli + command | 生效边界 | 已成卡 |

## 2. 备选（12 个，分诊为 candidate）

分诊给了 `candidate` 但没排期的，**任一主选核完不成立就顶上来**：

`dsh-plugin-save-token` · `@morlay/better-session`（产品册 `profile/17` 已有一张，注意重复）· `@viztor/dsh-tinyfish`（与 `dsh-tinyfish` 同代码双名，**只取其一**）· `dsh-scnet` · `dsh-qqbot-lite` · `dsh-context-imports` · `@try-works/dsh-stt` · `rolebox` · `@jiesou/dsh-opencode-zen-free-provider` · `dsh-code-pill` · `dsh-web3`

## 3. 降级为 TRAPS（8 条，文档纪律而非载体）

这些"sample"讲的是**安装文档写得好**，不是用了什么载体——不占卡位，进 [`TRAPS`](../practice/TRAPS.md) 与 [`INSTALL`](../install/README.md)：

| 包 | 它教的纪律 |
|---|---|
| `dsh-dream-skin` | 四条通道各配一句坑；发版 24 小时内必须写死版本 |
| `dsh-ppt-master` | `@latest` 会因 `minimumReleaseAge` 回退到**最旧**版本 |
| `dsh-knowledge` | `allowBuilds` 要合并进已有键，别新开第二个 |
| `dsh-study-mode` | 裸地址被当 tarball，拉回 HTML 导致安装失败 |
| `dsh-context-imports` | 手拷 `node_modules` 会被 loader 静默丢弃 |
| `dsh-ui-harmonizer` | 装完要**硬刷新**，普通刷新不够 |
| `dsh-code-pill` | 刷新页面 ≠ 重新加载客户端模块 |
| `@tianbuyu-wwx/dsh-formatforge` | 四道自检：bundle 注册 / 启动日志行 / HTTP 面 / 冒烟 |

## 4. 被拒（6 个，非生命周期）

`dsh-chat-import`（已产品册卡）· `@perrylink/dsh-plugin-doctor` · `dsh-cool-theme` · `dsh-voice-scribe` · `@doitian/dsh-music` · `dsh-metaphysics`(部分) — 纯能力或界面，无生命周期机制。

## 5. 缺口（下一轮普查方向）

- **反例（`negative/`）**现有 **1 张**（`negative/91`，机制对但没人用）。还缺一类：**"装了却永远不生效"的失败样本**——需要在真实用户机器上取证，本册暂无条件。
- **自带安装器 / 自带运行时（载体 8、9）**在 42 个里各只出现极少，说明这类东西普遍不走 npm——**下一轮要从 Releases 与安装包方向召回**，而不是继续扫 npm。
- **`desktop` 面**零实测：本册所有 Desktop 结论都是 `[DSH]` 级（见 [`reference/SURFACES`](../reference/SURFACES.md) 页头）。
- **配**这一轴已从 0 补到 3 张，但"凭据与连接"主题仍薄——`dsh-scnet`、`dsh-qqbot-lite` 是下一批候选。
