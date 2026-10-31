---
title: "BACKLOG · 候选池（待深挖 / 快筛不过）"
domain: reshape-product
kind: index
positioning: "候选池：快筛过了门槛但还没深挖的，和没过门槛的，都记在这里，不占卡位。"
read_when: "要补新样本、或想知道某个产品为什么还没成卡。"
status: living
updated: 2026-10-31
budget: 64
---
# BACKLOG · 候选池

> **规则**：候选先过 [`00-map` §11.1](./00-map.md) 的 10 分钟快筛；**不过就不立卡，只在这里留一行**。
> 每行至少写清：类型（plugin / profile / shell）、硬指标（带日期）、**为什么还没成卡**、下次复核的条件。
> 候选池**不参与**篇数统计，也不进 catalog 的"全量文件"以外的地方。

## 1. 过了门槛、待深挖

| 候选 | URL | 类型 | 硬指标（2026-10-31） | 待办 / 风险 |
|---|---|---|---|---|
| `hust-open-atom-club/oh-dsh` | <https://github.com/hust-open-atom-club/oh-dsh> | shell | ★ 323 · forks 34 · issues 40 | 自带 Node + 安装包的三端发行版；要挖"分层安装"与 DSH Desktop 的差异，再判是否成卡 |
| `shaobeichen/dsh-pocket` | <https://github.com/shaobeichen/dsh-pocket> | plugin | ★ 2,601 · npm 月 18,308 | 远程/扫码同屏，与 `dsh-mobile` 同类；先判"是否需要第二张多端卡" |
| `sjh9714/dsh-win32` | <https://github.com/sjh9714/dsh-win32> | plugin | ★ 151 · npm 月 4,721 | 安装 + 实机验收 + 修 koffi，Windows-only；**5 类下一张**，先判"实机验收"是否算产品化 |
| `vshulcz/deja-vu` | <https://github.com/vshulcz/deja-vu> | plugin | ★ 1,342 · DSH 包 `dsh-deja` 月 6,089 | 跨 43 个 agent 就地索引、装完即"满"；先判归 4 类（首启）还是 7 类（记忆） |
| `weibaohui/skills-management` | <https://github.com/weibaohui/skills-management> | plugin | ★ 43 · npm 月 12,232 | 从 10+ agent 导入技能 + 6,600+ 技能市场；README 薄，需源码/实测才够卡 |
| `gezi-wen/sage-mem` | <https://github.com/gezi-wen/sage-mem> | plugin | ★ 23 · npm 月 8,955 | 记忆格式与 Claude Code 兼容，迁移角度的第二候选；先看有没有首启流程 |
| `yu-wenchao/dsh-free-models-hub` | <https://github.com/yu-wenchao/dsh-free-models-hub> | plugin | ★ 32 · npm 月 2,420 | 过 npm 门槛；"一键写入免费模型 provider"属首启配置，但机制偏薄 |
| `xiaoyuyu6420/dsh-backup` | <https://github.com/xiaoyuyu6420/dsh-backup> | plugin | ★ 36 · npm 月 3,841 | 备份/还原/迁移；与 `42_环境搬家` 同类，判是否值得第二张 |
| `xiaoxiao44443/dfy-dsh-plugins` | <https://github.com/xiaoxiao44443/dfy-dsh-plugins> | profile | ★ 3 · npm 月 4,766 | 原生组合包（8 个自研插件 + 2 个公共库，`Symbol.for` ABI 共享 provider）；过 npm 门槛，先判与 `13_组合包` 是否同形态 |
| `RevolutionLA/dsh-dream-skin` | <https://github.com/RevolutionLA/dsh-dream-skin> | plugin | ★ 297 · npm 月 41,441 | 皮肤资产包（8 套预设 + 主题包导入导出）；只换皮肤，暂按插件侧 1 类 |
| `benz-ai-x/dsh-24pa` | <https://www.npmjs.com/package/@benz-ai-x/dsh-24pa> | profile | ★ 未采 · npm 月 5,111 | 飞书个人助理套件（垂直产品包）；仓库 404（改名/私有），先找新地址再判 |
| `amplifthq/oh-my-dsh` | <https://github.com/amplifthq/oh-my-dsh> | shell/profile | ★ 16 · npm 月 481 | "overlay, not a fork" 发行版，装两个独立 profile；两条门槛都差一点，先判它算 profile 还是 shell |
| `@huaweidevtools/aishell-dsh-base` | <https://github.com/yusheng-g/aishell-dsh-plugins> | profile | ★ 未采 · npm 月 1,386 | 企业 profile base layer（Huawei scope，叠在 dsh-base 上）；README 缺失，待采语义 |
| `yhny1001/dsh-rp-distribution` | <https://github.com/yhny1001/dsh-rp-distribution> | profile | ★ 8 · 包未发布 | 垂直 RP 发行版（公共契约 + 包信任 + 组合发行）；npm 未发布，等可安装再判 |
| `magian1127/deepseek-harness-zh_pro` | <https://github.com/magian1127/deepseek-harness-zh_pro> | plugin | ★ 36 · npm 月 5,580 | "综合增强"是否算产品化有争议（改默认语言/提示词，但仍是单插件）；先看它有没有自己的分发/首启 |

## 2. 观察样本（未过门槛，机制独特）

| 候选 | URL | 类型 | 硬指标（2026-10-31） | 为什么留着 |
|---|---|---|---|---|
| `why-sir/dsh-bootstrap` | <https://github.com/why-sir/dsh-bootstrap> | plugin | ★ 1 · npm 月 763 · 仓库 14 天 | 唯一"首启推荐 + 计划 + 环境码"样本；分析见 [`plugin/_证据/04_首启观察`](./plugin/_证据/04_首启观察-dsh-bootstrap.md)，**未过门槛，不立卡** |
| `Dariandai/dsh-starter-pack` | <https://github.com/Dariandai/dsh-starter-pack> | plugin | ★ 1 · npm 月 385 | **唯一"批量装 15 个插件 + 配置"样本**；只有 `/setup` 与设置页，量太小，留着当机制参考 |
| `gongyijie85/dsh-repo-setup` | <https://github.com/gongyijie85/dsh-repo-setup> | plugin | ★ 2 · npm 月 1,481 | 只读扫描仓库（栈/测试/文档/DB）→ 推荐插件/MCP/卫生文件；"理解用户数据"的最小样本 |
| `woodfood111/dsh-subscription-login` | <https://github.com/woodfood111/dsh-subscription-login> | plugin | ★ 1 · npm 月 1,448 | 一页列出所有订阅登录并带你走完，列表从授权接缝读、不硬编码 provider |
| `PerryLink/dsh-claude-move` | <https://github.com/PerryLink/dsh-claude-move> | plugin | ★ 30 · npm 月 待采 | 四来源迁移向导（Claude Code / Codex / OpenCode / Hermes），dry-run；与 `42` 同赛道 |
| `liangl1985/work-personal-secretary` | <https://github.com/liangl1985/work-personal-secretary> | plugin | ★ 3 · 无 npm 计量 | 安装器 + 环境探测（Python / WPS / 工作区）→ 装兄弟插件 → 生成工作区基线；**profile 级首启的雏形** |
| `KERBALMans/dsh-modpack` | <https://github.com/KERBALMans/dsh-modpack> | plugin | ★ 4 · 无 npm 计量 | Minecraft 整合包式：勾插件 → 打包 → 别人导入即还原整套环境（`.dshmodpack.json`） |
| `ljh257110/dsh-local-installer` | <https://github.com/ljh257110/dsh-local-installer> | plugin | ★ 0 · npm 月 842 | 在设置页里选 `.tgz` 装插件、自动探测 profile、回显 CLI 输出；"不用终端"的安装面 |
| `objectivex666/dsh-settings-search` | <https://github.com/objectivex666/dsh-settings-search> | plugin | ★ 1 · 无 npm 计量 | 按关键词/拼音/意图/AI 找设置并直达；"让用户理解这个插件"的一条支线 |
| `sjh9714/dsh-movein` | <https://github.com/sjh9714/dsh-movein> | plugin | ★ 17 · npm 月 1,251 | 把 Claude Code 配置迁入 DSH（dry-run + 冲突保护）；接近门槛，先观察 |

## 3. 没过门槛（留档，避免重复搜）

| 候选 | URL | 类型 | 硬指标（2026-10-31） | 未过原因 |
|---|---|---|---|---|

## 4. 复核节奏

- 每次补新卡时，顺手把本表**已过门槛**的候选重新看一眼（星标/下载有没有变化、有没有新版本）；
- 候选成卡后，从本表**删行**，在卡片 `样本档案` 里写清"从候选池转正"的日期；
- 连续 6 个月无变化的"未过门槛"行可以删掉，保持表短。
