---
title: "10 · Asher-2000/dsh-expert-mode 源码复核"
domain: cross-boundary
kind: evidence
positioning: "复核 dsh-expert-mode 0.9.2/HEAD：17 条静态子代理行只是 17 个工具别名，不是 17 个成员；preset 未声明，组合也已对不上 DSH 0.2.1-rc.3。"
read_when: "核对 10 卡「17 行=17 成员」、preset 路线能否在 rc.3 落地、taskboard 原子性与 bus 唤醒时。"
status: observed
updated: 2026-11-01
---

# 10 · `Asher-2000/dsh-expert-mode` 源码复核

> 复核对象：样本卡 [`10-Asher-2000-dsh-expert-mode.md`](../samples/10-Asher-2000-dsh-expert-mode.md)。
> 取证时点 2026-11-01。只读 GitHub（`git ls-remote` / `git clone` / codeload）、npm registry 与本机 `@deepseek-ai/dsh 0.2.1-rc.3` 安装树；**未安装、未构建、未运行插件、未执行 `taskboard.py`/`bus.py`、未启动宿主、未执行任何 `dsh` 命令**。
> 标签沿用 [`EVIDENCE.md`](../../EVIDENCE.md)：`[DOC]` 目标仓 README/CHANGELOG 主张，`[SRC-TARGET]` 固定 commit 实现，`[SRC-DSH]` 本机 rc.3 发行包，`[TEST]` 测试源码，`[CI]` 同 SHA check-run，`[RUN]` 本轮实跑，`[OBS]` 判断。
> **主 pin（工作树）**：commit [`ed9a19d64bb0fc1889ebcb1a998ca3716c56d299`](https://github.com/Asher-2000/dsh-expert-mode/commit/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299)（`main` HEAD，2026-09-07T14:26:38+08:00，`package.json` 0.9.2）。
> **发布物 pin（npm 0.9.2）**：commit [`d61da21aa12340fa05c908b7a5a4625841ea427a`](https://github.com/Asher-2000/dsh-expert-mode/commit/d61da21aa12340fa05c908b7a5a4625841ea427a)（npm `gitHead`，tarball 与该树逐文件一致）。
> **卡片版本**：取证开始时卡为 69 行；取证期间被并发修订为 **70 行**（新增 L19 证据链、L23 的 16/17 说明，L43/L47/L48 改为显式 pin HEAD 并区分 npm/tag/HEAD）。本 memo 的行号按 **70 行版（2026-11-01 04:50）**；对已修断言在偏差表标「已修」。
> **一句话结论**：**17 条 `dsh-tool-subagent` 工具行是真的，17 个「成员」不是**——每行只是一个委派工具别名；子代理没有 `agentPreset`，按宿主规则加入父代理当前 preset，于是 17 个孩子共享同一个协调官人格。卡片「装不起来」的**结论对，机制表述仍不完整**（坐标已在卡片的并发修订中改正，见偏差表「已修」）：当前发布物根本没有声明任何 agent preset，rc.3 也不再读取它写入的目录；即便手工迁移成 preset，组合里还有宿主已改名的 `persona.text`、17 个被禁的 `config.persona`、一个 rc.3 不存在的 `dsh-workflow-worker-thread` 三处独立硬失败。

## Provenance

| 项 | 值 | 核对方式 |
|---|---|---|
| 仓库 | [`Asher-2000/dsh-expert-mode`](https://github.com/Asher-2000/dsh-expert-mode)（MIT；13★ @2026-11-01） | `img.shields.io/github/stars/...json` → `13`；`LICENSE` 与 `package.json` |
| npm 包 | `dsh-expert-mode`，仅 `0.9.0` / `0.9.1` / `0.9.2` 三个版本；`latest = 0.9.2`，发布 `2026-08-27T06:49:03.433Z` | `registry.npmjs.org/dsh-expert-mode` |
| npm 近 30 天 | **374 次**（`2026-09-30..2026-10-29`，与卡片同窗口）；近 7 天 162 次 | `api.npmjs.org/downloads/point/...` |
| **npm 0.9.2 的 commit** | `gitHead = d61da21aa12340fa05c908b7a5a4625841ea427a`（2026-08-27T14:49:01+08:00，`chore: bump to 0.9.2`）；`dsh-expert-mode-0.9.2.tgz` 与 `git archive d61da21` **逐文件 diff 干净**（仅 npm 的 `files` 白名单排除了 `.gitignore`/`assets`/`docs`） | registry `dist.gitHead`、tarball vs `git archive` |
| **tag `v0.9.2`** | 轻量 tag → `b524f7b7e761a8083f76ddd1a2f16221c7f24ee2`（2026-08-27T14:48:49+08:00，比 npm 的 bump 提交早 12 秒）；该树 `package.json` = **`0.9.1`**、`preset.yml` = **`0.8.1`** | `git ls-remote`、`git cat-file -t v0.9.2` = `commit`、`git show v0.9.2:package.json` |
| **HEAD 工作树** | `ed9a19d`（2026-09-07，`feat: 同步 VPS 09-03 方法论更新 — 17专家架构 + router 路由层…`）；距 npm 的 `d61da21` **7 个提交**，但 `package.json` 仍是 **`0.9.2`**；`main` 已改 `lib/index.js`，新增 `lib/`、`dsh.plugin.json`、`.expert-mode/router/` | `git log d61da21..HEAD`、`git show HEAD:package.json` |
| 版本/标签规律 | tag 系统性晚一个提交：`v0.9.1` → `2cf9a86`（树内 `0.9.0`）、`v0.9.2` → `b524f7b`（树内 `0.9.1`）；npm 的 `gitHead` 才指向 bump 提交（`0.9.1`→`3a5d0e1`，`0.9.2`→`d61da21`） | 三个 tag 的 `package.json` 对照 |
| 卡片修订 | 取证开始时 69 行；取证期间被并发改为 **70 行**：新增 L19 证据链、L23 的 16/17 说明，L43/L47/L48 改为显式 pin HEAD 并区分 npm/tag/HEAD。**本 memo 行号按 70 行版（2026-11-01 04:50）**；已修的坐标断言在偏差表标「已修」 | `cat -n` 前后对照；卡 L19/L23/L43/L47/L48 |

**错位结论（本卡最实的坐标问题）**：

1. **npm 0.9.2 = `d61da21`**，不是 tag。该树的 `main` 是 [`index.js:15`](https://github.com/Asher-2000/dsh-expert-mode/blob/d61da21aa12340fa05c908b7a5a4625841ea427a/package.json#L15)（`index.js`），入口是 [`index.js:14-17`](https://github.com/Asher-2000/dsh-expert-mode/blob/d61da21aa12340fa05c908b7a5a4625841ea427a/index.js#L14-L17) 的 `apply() {}` 空实现；**没有 `lib/`，也不会拷贝任何文件**。`preset.yml` 仍自称 `专家模式 v0.8.1`、只有 16 位专家（[`preset.yml:1-6`](https://github.com/Asher-2000/dsh-expert-mode/blob/d61da21aa12340fa05c908b7a5a4625841ea427a/preset.yml#L1-L6)）。
2. **tag `v0.9.2` = `b524f7b`**，树内版本是 `0.9.1`；tag 打在了 bump 提交的父提交上。任何「按 tag 复现」都会拿到 0.9.1 的元数据。
3. **HEAD = `ed9a19d`**，版本串仍是 0.9.2，但 `main` 改成 [`lib/index.js`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/package.json#L15)，`apply()` 变成**真拷贝**（[`lib/index.js:51-82`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/lib/index.js#L51-L82)），并新增 `dsh.plugin.json` 与 router；**这部分从未发布到 npm**。

因此「0.9.2」不能单独当坐标：本 memo 的每条目标仓断言都标明是 `d61da21`（npm 0.9.2）还是 `ed9a19d`（HEAD）。卡片在取证期间已把 L43/L47/L48 改成显式 pin HEAD 并区分三棵树；这是并发修订后的写法，原始 69 行版曾把三棵树混写（见偏差表「已修」）。**无论哪版，不 pin commit 就无法复现 npm 的空壳与 HEAD 的拷贝。**

另有两处名称不一致，先记下不展开：

- HEAD 的 [`dsh.plugin.json:2`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/dsh.plugin.json#L2) 把包名写成 `@asherliner/dsh-expert-mode`，而 [`package.json:2`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/package.json#L2) 是 `dsh-expert-mode`；rc.3 安装树里**没有找到读 `dsh.plugin.json` 的代码**（见 [OPEN]）。
- 组合文件自己的注释写「16 expert subagent tools」与「16 位领域专家」（[`cordis.patch.yml:2`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/cordis.patch.yml#L2)、[`agent.cordis.yml:28`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/agent.cordis.yml#L28)、[`agent.cordis.yml:367`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/agent.cordis.yml#L367)），而 HEAD 的 README/preset.yml 写 17（[`README.md:5`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/README.md#L5)、[`preset.yml:1-3`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/preset.yml#L1-L3)）。**行数是 17，但仓库自己的提示词和注释仍说 16**（现卡 L23 已注明这一点）——下文的「17」都按行数计。

## DOC

`[DOC]` 只证明作者主张，不证明实现如此。

- 「首席协调官 + **17 位**领域专家」：[`README.md:5`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/README.md#L5)；`preset.yml` 同样写 17（[`preset.yml:3`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/preset.yml#L3)）。
- 「Inter-Expert Bus … zero coordinator relay, **P2P capable**」「Taskboard … crash recovery — real scheduling」：[`README.md:107-108`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/README.md#L107-L108)。
- 「Progressive Disclosure … **28% token savings**」：[`README.md:111`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/README.md#L111)（全仓 `28%` 仅此一处与 [`README.zh.md:111`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/README.zh.md#L111) 两行）。
- 安装自述：`dsh plugin add dsh-expert-mode`（[`README.md:124`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/README.md#L124)），随后把 preset 拷进 `~/.dsh/.agent-presets/expert-mode/` 并称该目录是「DSH's preset discovery directory」（[`README.md:130`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/README.md#L130)、[`README.md:140-153`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/README.md#L140-L153)）。**这是 0.2.1-rc.3 已废弃的目录**（见 SRC-DSH）。
- README 自己承认跨会话记忆是 **HOST-PLANE**、放进 preset 会挂载失败：[`README.md:180`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/README.md#L180)、[`README.md:199`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/README.md#L199)。这说明作者知道 preset 平面与 host 平面的区别，但没有把同一判断用到 `persona`/`workflow` 上。
- `PROTOCOL.md` 开头写「**✅ 已实现并验证**」（[`PROTOCOL.md:3`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/PROTOCOL.md#L3)），结尾 7 项验收里第 7 项 **未勾**：「端到端：真实双专家走总线接力（待测）」（[`PROTOCOL.md:155-161`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/PROTOCOL.md#L155-L161)）。
- `PROTOCOL.md` 对唤醒的表述是「协调官只在需要时通过 `send_message` 或任务提示告诉接收方『你的邮箱有消息』」（[`PROTOCOL.md:21`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/PROTOCOL.md#L21)）——这本身就是「文件事件不会唤醒子代理」的承认，只是它把这写成协调官的职责，而不是总线的缺陷。
- 「P2P 直接委派」定义为「专家持有 subagent 工具时，可直接创建另一位专家作为自己的孙代理」（[`PROTOCOL.md:121-125`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/PROTOCOL.md#L121-L125)）。这要求递归深度 ≥2；本组合没有设置 `maxDepth`，rc.3 默认 1（见 SRC-DSH §6），**孙代理默认会被宿主拒绝**。
- `preset.yml` 在 npm 0.9.2/tag 树里是 `v0.8.1` / 16 位（[`preset.yml:1-6`](https://github.com/Asher-2000/dsh-expert-mode/blob/d61da21aa12340fa05c908b7a5a4625841ea427a/preset.yml#L1-L6)），HEAD 才改成 `v0.9.2` / 17 位（[`preset.yml:1-7`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/preset.yml#L1-L7)）。**发布物自述版本比包版本落后一个 minor**。

## SRC-TARGET

本节所有目标仓链接都 pin 到 commit（HEAD `ed9a19d` 或 npm 0.9.2 的 `d61da21`），行号为该 commit 下的行号；除特别注明外，文件默认指 **HEAD `ed9a19d`**。

### 1. 「17 行」是真的；「17 个成员」不是

按固定 commit 逐行计数：

| 计数项 | 值 | 依据 |
|---|---|---|
| `dsh-tool-subagent` 插件行总数 | **21** | 2 条通用（`subagent`/`subagent_fork`）+ **17 条 `expert_*`** + 2 条外部 provider（`codex`/`claude-code`，均 `disabled: true`） |
| `expert_*` 工具行 | **17** | `id: tool-subagent-expert-*`，首行 [`agent.cordis.yml:317-325`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/agent.cordis.yml#L317-L325)，末行 [`agent.cordis.yml:556-565`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/agent.cordis.yml#L556-L565) |
| `persona:` 配置 | **17** | 每条专家行一份；例 [`agent.cordis.yml:320-325`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/agent.cordis.yml#L320-L325) |
| `provider: spawn` + `backgroundMode: continuable` | 17 条专家行全有 | 同上；`backgroundMode` 在 rc.3 已不是配置键（见 SRC-DSH §6） |
| `agentPreset` | **0** | 全文件无 `agentPreset` / `allowedAgentPresets` |
| roster / `spawn`/`remove` 工具 | **无** | 组合只有委派工具与 `list-agents`；没有成员状态机 |

**所以「17 条各自独立注册的工具行」成立，但把它等同于「17 个成员」不成立。** 差别不在数量，在**成员身份的载体**：

- 每行 `name: '@deepseek-ai/dsh-tool-subagent'` 是一个**独立插件实例**，注册的是**一个模型可调用的工具**（`toolName` 唯一：`expert_backend_dev`…`expert_media_creator`）。组合里没有任何东西在启动时创建 17 个 agent；**成员只在模型调用某个 `expert_*` 工具时才存在**，由 `provider: spawn` 起一个子代理。
- 子代理的**组合与人格从哪里来**？这 17 行都没有 `agentPreset`。rc.3 的规则是：两个选择字段都不配时，工具不要求 preset 服务；模型不指定时，子代理 **加入父代理当前的 preset revision**（`[SRC-DSH]` `dsh-tool-subagent/README.md:68-70`）。父代理就是「专家模式」这个 preset，于是**每个专家孩子拿到的都是同一份协调官 prompt + 同一套 17 个工具**，不是该专家的人格。
- 唯一可能区分成员的字段就是 `config.persona`；它在 rc.3 **加载即抛错**（`[SRC-DSH]` `dsh-tool-subagent/lib/index.js:355`）。抛错后这 17 行全部不可用。**所以不但「17 个成员」没有实现，连「17 个不同 prompt 的工具」都没有实现**：17 个工具的描述来自同一个 `providerWording()`，只在名字上不同。
- 更直接的证据：协调官 prompt 让模型「用 **`expert_delegate`** 工具委派」（[`agent.cordis.yml:44`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/agent.cordis.yml#L44)），但组合里**根本没有 `expert_delegate`**；实际注册的是 17 个各自命名的 `expert_*`。同一条 prompt 还说「你手下有 **16** 位领域专家」（[`agent.cordis.yml:28`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/agent.cordis.yml#L28)）。**即使挂载成功，协调官也会按一条不存在的工具名去委派。**
- 「成员边界 = 工具边界，模型看得见、叫得出」只在**名字**层面成立；模型看到的是 17 个同名描述、只差名字的工具，且没有成员状态、没有花名册、没有成员生命周期。**这不是「把成员写成配置」，而是「把 17 个委派入口写成配置」。**

用一张表回答「成员到底怎么创建」：

| 候选机制 | 本仓库用法 | 结论 |
|---|---|---|
| preset composition | `agent.cordis.yml` 是静态组合，但**没有被任何 `@deepseek-ai/dsh-agent-preset` 声明引用**（见 §2） | 有组合文件，没有 preset 声明 |
| `agentPreset` | **0 次** | 未使用；孩子继承父 preset |
| 重复工具行 | **17 条**同包不同 `toolName`（+ 2 条通用） | 实际机制：17 个委派别名 |
| roster / 状态机 | 无 | 没有成员持久状态 |
| 每次调用 spawn | 有（`provider: spawn`） | 成员是**调用时**产生的子会话 |

**结论**：卡片所谓「成员从运行时数据变成了配置」应改写为「**委派入口**从运行时工具变成了配置；成员身份仍需要一个 per-child preset，而本仓库没有配」。在 rc.3 里，唯一能把 `expert_backend_dev` 变成「后端专家」的合法路径是给它配 `agentPreset: <某个已声明的 preset>`，并为每个专家声明独立 preset（含自己的 `persona.prefix` 与工具表）。本仓库两条都没做。

**关于「不用写插件运行时」这半句**：在**协作机制**上成立——组合里没有 roster 服务、没有协调器进程、没有 spawn/remove 工具；`taskboard.py`/`bus.py` 只是被模型用 bash 调用的 Python CLI，不是 Cordis 服务。缺的不是「协作引擎」，而是「成员身份」：17 个工具别名共享一个父 preset。换句话说，卡片的**路线判断（预设式协作可行）成立，但本仓库的实例化停在「工具别名」层**。分发上也仍要一个 Cordis 插件/bundle 来部署 preset，所以「不用写插件」只对协作运行时成立，对分发不成立。

### 2. 安装/部署路径：plugin 是空壳，preset 从未声明

- **npm 0.9.2 的入口是空壳**：`main: index.js`（[`package.json:15`](https://github.com/Asher-2000/dsh-expert-mode/blob/d61da21aa12340fa05c908b7a5a4625841ea427a/package.json#L15)），`index.js` 只 `export default { name, inject: [], apply() {} }`（[`index.js:14-17`](https://github.com/Asher-2000/dsh-expert-mode/blob/d61da21aa12340fa05c908b7a5a4625841ea427a/index.js#L14-L17)）。安装它**不会部署任何 preset**。
- **HEAD 的入口会拷贝，但拷进死目录**：`main: lib/index.js`，`apply()` 把 `targetDir` 清空（仅保留 `.git`）后，把包根的 `agent.cordis.yml`/`preset.yml`/`cordis.patch.yml` 和 `.expert-mode/` 拷进去（[`lib/index.js:51-82`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/lib/index.js#L51-L82)）。默认目标就是 `~/.dsh/.agent-presets/expert-mode`（[`lib/index.js:52-55`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/lib/index.js#L52-L55)）。
- **bundle patch 只注册插件，不声明 preset**：

  ```yaml
  - insert:
    - id: dsh-expert-mode
      name: dsh-expert-mode
  ```

  （[`cordis.patch.yml:5-7`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/cordis.patch.yml#L5-L7)）。**没有** `name: '@deepseek-ai/dsh-agent-preset'` 的行，也没有 `config.id/plugins`。因此宿主里不会出现 `preset-expert-mode` 这个 Loader 行，preset 选择器里也没有「专家模式」。
- `dsh.plugin.json` 里虽然写了 `preset.targetDir/files/bundles`（[`dsh.plugin.json:12-21`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/dsh.plugin.json#L12-L21)），但 rc.3 安装树里没有读这个文件的代码；它更像是对外 registry（dsh.so）的元数据。**不能把它当作 rc.3 的部署机制**（见 [OPEN]）。
- **`apply()` 的副作用**：每次宿主启动、该插件行激活时，它都会先 `rmSync` 整个 `targetDir`（[`lib/index.js:57-66`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/lib/index.js#L57-L66)）再拷入新树（[`lib/index.js:68-80`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/lib/index.js#L68-L80)）。如果这个目录真是活的状态目录，`tasks/`、`mailboxes/`、`logs/` 会在每次重启时被清空——**与 `PROTOCOL.md:157` 的「持久化（重启不丢）」直接冲突**。

**结论**：**当前发布物是「空壳 + 死目录」，HEAD 是「真拷贝 + 死目录 + 启动清空」；两条路都到不了「可用 preset」。** 卡片的原始 69 行版曾把这两版混成一句（「`apply()` 是空实现」+「只把文件拷到…」）；现卡 L48 已区分两棵树，但「死目录」与「没有 preset 声明」仍未被合并成同一个结论。

### 3. Taskboard：`claim` 不是原子的，`stale` 回滚没有存活探测

`[SRC-TARGET]` 全部指 HEAD：

- `claim` 的实际顺序是 `_load_task` → 依赖检查 → `_set_status` 校验 → `_save_task` 整份覆盖（[`taskboard.py:273-292`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/taskboard.py#L273-L292)），写文件是 `open(p, "w")`（[`taskboard.py:97-100`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/taskboard.py#L97-L100)）。全仓 `*.py`/`*.mjs`/`*.js` 没有 `flock`、`fcntl`、`O_EXCL`、`os.replace`、`portalocker`、`filelock`（grep 0 命中）。**「原子认领」只存在于 docstring**（[`taskboard.py:274`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/taskboard.py#L274)）。
- 两个专家同时 `claim` 同一 `ready` 任务时，双方都先读到 `ready`，`_set_status` 的 `ready -> running` 都合法（迁移表 [`taskboard.py:50-56`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/taskboard.py#L50-L56)），后写者覆盖先写者的 `agent`/`history`。**lost update，不是互斥。**
- `_next_id()` 也是「读目录求最大 + 1」再写（[`taskboard.py:68-81`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/taskboard.py#L68-L81)），并发 `create` 可以拿到同一个 `task-NNN`，后写覆盖先写。
- `stale > 300s -> ready` 属实：`TASKBOARD_STALE_AFTER` 默认 `300`（[`taskboard.py:159`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/taskboard.py#L159)），`age > stale_after` 就把 `running` 直接写成 `ready`（[`taskboard.py:171-178`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/taskboard.py#L171-L178)），**只比较 `updated_at`，不查 PID、不查心跳、不查会话存活**。`updated_at` 只在状态迁移时更新（[`taskboard.py:118-119`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/taskboard.py#L118-L119)），所以任何跑超过 5 分钟的正常任务都会被判定为 stale。
- `recover` 是**手动命令**（[`taskboard.py:364-373`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/taskboard.py#L364-L373)、[`quality-gates.md:93`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/methods/quality-gates.md#L93)）；没有守护进程、没有定时器。卡片写「手动 `recover` + `stale > 300s` 直接回 `ready`」是准确的。

**卡片没写的两个后果**：

1. `_recover_stale` 直接赋值 `t["status"] = "ready"`（[`taskboard.py:172`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/taskboard.py#L172)），**绕过了 `ALLOWED_TRANSITIONS`**。原专家干完回来调 `done` 时，当前状态已是 `ready`，`ready -> done` 非法（[`taskboard.py:50-56`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/taskboard.py#L50-L56)），命令返回 1，成果无法入库；与此同时另一个专家可以 claim 同一任务，**同一任务被执行两次**。
2. 因为 `updated_at` 没有心跳刷新，「运行超过 300 秒」与「已经崩溃」在代码里**不可区分**。卡片说「跑得久的专家会被当崩溃回滚」——完全成立，而且回滚后的收尾会失败，不只是「被回滚」。

### 4. 文件总线：只有写/读，没有投递或唤醒

- `bus.py` 的 `send` 只是 `_write_message` 把 `.msg` 文件写进 `mailboxes/<to>/`（[`bus.py:103-123`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/bus.py#L103-L123)、[`bus.py:150-164`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/bus.py#L150-L164)）；`read` 只是 `os.listdir` + `open`（[`bus.py:126-147`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/bus.py#L126-L147)）。**没有 socket、没有 inotify、没有 FIFO、没有宿主事件、没有任何把文件变化推给子代理的路径。** 子代理是模型回合驱动的，文件事件不会叫醒它——卡片的判断正确。
- `PROTOCOL.md:21` 自己把唤醒责任交给协调官的 `send_message`/任务提示；`PROTOCOL.md:161` 的端到端接力仍未勾；`PROTOCOL.md:3` 却写「已实现并验证」。**同一份文档里的状态自相矛盾。**
- 并发副作用（卡片未列）：消息序号 `_next_seq()` 是「读 `.seq` → truncate → 写回」，无锁（[`bus.py:90-100`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/bus.py#L90-L100)）；两个专家同一秒发送可能拿到同一个 `seq`，而 `message_id` 是 `<epoch秒>_<from>_<seq>`（[`bus.py:103-107`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/bus.py#L103-L107)），同发送者同秒同 seq 会**覆盖同一条 `.msg`**。
- `read` 不标记已读；只有 `ack` 把文件 `shutil.move` 到 `archive/`（[`bus.py:221-237`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/bus.py#L221-L237)）。`_read_messages(agent, include_read=False)` 的 `include_read` 参数**从未使用**，所以 `read --all` 与 `read` 行为相同——所谓「默认只显示未读」是靠「已读即被 ack 移走」实现的，不是读状态。

### 5. 「省 28% token」：无来源，且仓库自己的度量是 71%

- 全仓 `28%` 只命中 README 两行（[`README.md:111`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/README.md#L111)、[`README.zh.md:111`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/README.zh.md#L111)），没有测试、日志或脚本产出这个数。
- 唯一的度量文档 [`docs/internal/test-progressive-disclosure.md`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/docs/internal/test-progressive-disclosure.md) 统计的是**字符数**：`~3230字` → `~930字`，结论写 **约 71%**（[`test-progressive-disclosure.md:48`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/docs/internal/test-progressive-disclosure.md#L48)、[`:64`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/docs/internal/test-progressive-disclosure.md#L64)、[`:69`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/docs/internal/test-progressive-disclosure.md#L69)）。卡片说「3230 字 → 930 字、71%」是准确的；它与 README 的 28% **不是同一个口径**，也没有互相引用。

### 6. 数据指标复核

- 13★：shields.io 的 GitHub stars 端点返回 `13`（2026-11-01）。
- 374 次/月：npm point API 对 `2026-09-30:2026-10-29` 返回 `{"downloads":374}`，与卡片窗口一致。
- catalog 2026-08-19 快照 5★：本仓 [`data/stars.json`](../../../../data/stars.json) 中该 repo 记录为 `{"stars": 5, "checkedAt": "2026-08-19"}`；13/5 = 2.6，与卡片「×2.6」一致。

### 7. 状态归属：一个全局目录，两套路径假设

- 状态根是**部署目录**，不是会话/工作区：`bus.py` 用 `BASE = dirname(__file__)`（[`bus.py:33-36`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/bus.py#L33-L36)），`taskboard.py` 同样（[`taskboard.py:43-45`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/comm/taskboard.py#L43-L45)），任务与邮箱都落在脚本旁边。按 HEAD 的 `apply()`，这个目录是 `~/.dsh/.agent-presets/expert-mode/`（[`lib/index.js:52-55`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/lib/index.js#L52-L55)）——**所有会话、所有项目共享一份看板/邮箱**；任务/消息记录里没有 session id、workspace id 或租约字段。
- 但协调官 prompt 和协议用的是**工作区相对路径**：`.expert-mode/methods/{expert}.md`（[`agent.cordis.yml:32`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/agent.cordis.yml#L32)、[`:43`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/agent.cordis.yml#L43)）、`.expert-mode/comm/taskboard.py`（[`:100`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/agent.cordis.yml#L100)）、`python3 .expert-mode/comm/bus.py`（[`:125`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/agent.cordis.yml#L125)）。部署却只写全局 preset 目录，**没有任何步骤把 `.expert-mode` 放进工作区**（[`lib/index.js:68-80`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/lib/index.js#L68-L80) 只写 `targetDir`；README 的 Option B/C 也只拷到 preset 目录，[`README.md:140-153`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/README.md#L140-L153)）。除非用户恰好在含 `.expert-mode/` 的 checkout 里工作，否则 prompt 里的相对路径解析不到脚本与方法论文档。
- 这两套假设还互相排斥：若把 `.expert-mode` 放进工作区以获得相对路径，状态就变成**每项目一份**，与全局 preset 目录那份分叉；若只用全局目录，prompt 的路径又失效。卡片把「状态归属」写成「`~/.dsh/.agent-presets/expert-mode/` 下的文件总线 + taskboard JSON」，只覆盖了前一套。
- 额外的所有权风险：HEAD 的 `apply()` 每次启动清空 `targetDir`（§2），所以只要插件行在，**全局那份状态每重启一次就归零**；`.gitignore` 忽略 `mailboxes/`/`archive/`/`logs/`/`.seq`，却**没有忽略 `tasks/` 与 `tasks_done/`**（`.gitignore` 全文），所以工作区那份看板反而可能被提交。

## SRC-DSH

以下均指本机 `@deepseek-ai/dsh 0.2.1-rc.3` 安装树（`/Users/bowhead/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai/`）。**只读源码，未执行。**

1. **`persona` 已被移除**：`dsh-tool-subagent/lib/index.js:355` 的 `apply()` 第一行就是
   `for (const field of ["persona", "toolFilter"]) if (Object.hasOwn(config, field)) throw new Error("tool-subagent: ${field} is no longer supported; configure persona and tool plugins in an Agent Preset and select it with agentPreset (spawn only)")`。
   Config schema 只有 `provider`/`toolName`/`modelSelectionSettings`/`agentOptions`/`agentPreset`/`allowedAgentPresets`/`maxDepth`（`lib/index.js:311-324`），**没有 `persona`，也没有 `backgroundMode`**。卡片的行号 355 精确。
2. **`~/.dsh/.agent-presets/` 已无人读取**：DSH 自带的 preset 编辑技能明写「Before declaration rows, a user preset was a directory `$DSH_HOME/.agent-presets/<id>/` … **Nothing reads that directory any more.**」（`dsh-agent-preset/skills/editing-cordis-compositions/SKILL.md:70`）。对 rc.3 安装树里 `@deepseek-ai` 包的 `lib/*.js` 做 `rg "\.agent-presets"` **0 命中**；本机 `~/.dsh/.agent-presets` 也确实不存在。卡片 #2 成立。
3. **现行 preset 机制是「bundle patch 里插一行 `@deepseek-ai/dsh-agent-preset`」**：`dsh-agent-preset/lib/index.js:13-19` 的 Config 是 `{ id: required, name, description, order, plugins: required }`；`Service.init` 直接 `ctx.agentPresets.register(config)`（`lib/index.js:24-26`）。卡片 #2 末尾的「现行做法」描述准确（`name` 其实是可选的）。
4. **preset 挂载是「一行失败、整体拒绝」**：`dsh-agent-preset-registry/lib/index.js:154-176` 的 `auditRows()` 收集 import/activation 失败；`mountPreset()` 在 `failed.length > 0` 时直接 `throw`（`lib/index.js:229`）。`register()` 是 eager 的（`lib/index.js:491-497`）。所以只要组合里有一行坏，整个 preset 就不可用；错误里会列出每一行。
5. **preset 里的 `dsh-persona` 要 `prefix`，不是 `text`**：`dsh-persona/lib/index.js:23-24` 是 `z.object({ prefix: z.string().required(), ... })`，`apply()` 用 `config.prefix`（`:39`）。目标组合的 persona 行用的是 `config.text`（[`agent.cordis.yml:24-27`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/agent.cordis.yml#L24-L27)）。**即使把 17 个 `persona` 全删掉，preset 的第一行也会因缺 `prefix` 挂载失败。** 这是卡片完全没提的硬伤。
6. **`dsh-workflow-worker-thread` 在 rc.3 安装树里不存在**：本机安装的是 `dsh-workflow`/`dsh-workflow-ptc`/`dsh-tool-workflow`；shipped `standard` preset 用的是 `@deepseek-ai/dsh-workflow-ptc`（`dsh-web-app/presets/standard.patch.yml:104-107`），dsh 的依赖里也是 `dsh-workflow-ptc`（`dsh/package.json:89`）。目标组合却引用 `@deepseek-ai/dsh-workflow-worker-thread`（[`agent.cordis.yml:594-598`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/agent.cordis.yml#L594-L598)）。registry 上该包 `latest` 是 `0.0.1-rc.3`（另一个版本线），**不在 0.2.1-rc.3 的安装树里**；除非 profile 单独安装它，否则这一行 import 失败。卡片也没提。
7. **`backgroundMode` 已不是键**：`dsh-tool-subagent` 的 Config（`:311-324`）与 README 配置表（`README.md:51-52`）都没有它；`grep backgroundMode` 在 `dsh-tool-subagent`/`dsh-subagent` 源码里 0 命中。由于 `persona` 守卫用 `Object.hasOwn(config, ...)` 判断，说明未知键会保留到 `config` 而不是被 schema 剥掉；因此 `backgroundMode` 大概率被**静默忽略**，不是致命错误。**[OPEN]**：未实跑验证 schemastery 对未知键的确切行为。
8. **递归与并发默认值**：`dsh-subagent/lib/index.js:2979` 的 `maxDepth` 默认 **1**，`resolveChildDepth()` 在 `childDepth > maxDepth` 时抛 `SubagentDepthError`（`:279-283`）。子代理深度为 1，所以**默认不能再创建孙代理**；`PROTOCOL.md:121-125` 的「P2P 直接委派」默认走不通。`:2980` 的 `maxActiveSubagents` 默认 **8**，`:1677` 每个 root parent 用 `pool.reserve(...)` 限流；**17 个专家不可能同时活跃**（除非宿主改设置，而 preset 改不了宿主设置）。
9. **子代理默认继承父 preset**：`dsh-tool-subagent/README.md:68-70` 明写「Without either selection field … An omitted model choice uses the configured `agentPreset`, or **joins the parent's current preset revision** when no default is configured」。`:72` 明写「Tool configuration containing `persona` or `toolFilter` fails at load with a migration error」。这两句同时判了本组合的「17 个不同专家」和 `config.persona` 的死刑。
10. **`dsh plugin` 不是「安装 bundle」**：`dsh/lib/bin.js:117-118` 的 `plugin` 子命令是「manage a profile's plugins by **forwarding the remaining arguments to pnpm** in the profile directory」，且 `requiredOption("--profile <name>")`。所以卡片/README 的 `dsh plugin add dsh-expert-mode` **缺 `--profile` 会直接被 Commander 拒绝**；补上 `--profile web` 也只是 `pnpm add`，**不会**把包加进 `dsh.profile.bundles`。bundle 层只来自 profile `package.json` 的 `dsh.profile.bundles` 顺序（`dsh/lib/profile-boot-C14i-8IN.js:122`、`:224-226`），未列入的包不会被当作 bundle 加载；`reportSkippedBundles` 只报告「声明了但装不上」的 bundle（`dsh-app-boot/lib/index.js:537`）。真正会写 `bundles` 的是 plugin manager 的 `installBundle`（`dsh-plugin-manager/lib/index.js:322-347`，在 `:340` push 新 bundle）。
11. **当前 profile 的旁证**：本机 `~/.dsh/profiles/web/package.json` 的 `dsh.profile.bundles` 是一份显式列表（`@deepseek-ai/dsh-base`、`@deepseek-ai/dsh-web-app`、第三方 bundle…），没有任何「扫描 node_modules 自动挂载」的机制。**装包 ≠ 挂 bundle。**

## TEST

`[TEST]` 只核对存在性，不证明通过：

- 仓库**没有测试目录、没有测试框架、没有 `package.json` 的 `scripts`**（`package.json` 无 `scripts` 字段）。
- 只有一份**人工测试报告** [`docs/internal/test-progressive-disclosure.md`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/docs/internal/test-progressive-disclosure.md)（自评、数字符，见 SRC-TARGET §5），不是可执行测试。
- HEAD 多一个 [`router-bootstrap-v34.selftest.mjs`](https://github.com/Asher-2000/dsh-expert-mode/blob/ed9a19d64bb0fc1889ebcb1a998ca3716c56d299/.expert-mode/router/router-bootstrap-v34.selftest.mjs)（router 自测脚本，HEAD 新增，未接入任何 runner）；它测的是 router，不是 17 个专家行或 taskboard/bus。
- **没有覆盖 `taskboard.py` 的 claim、`bus.py` 的 send/read、或 preset 挂载的测试。** 卡片里的「原子认领」「真通信」都没有测试背书。

## CI

- 仓库**没有 `.github/`**，也没有 `.gitlab-ci.yml`/`.circleci`/`.travis.yml`/`Jenkinsfile`（HEAD 根目录与全树 `find` 均无）。**没有任何 CI workflow。**
- 因此没有同 SHA 的 check-run 可引；`[CI]` 在本 memo 里只能是「不存在」。
- [OPEN]：GitHub API 本轮被限流（`403 rate limit exceeded`），无法读取 check-runs / commit 签名 / tag 签名；但从仓库文件结构看，没有可运行的 CI 配置。

## RUN

`[RUN] None`。

本轮只做了只读操作：`git ls-remote`、`git clone`、`git archive`、`git show`、`npm registry GET`、`curl` 下载 npm tarball 做 diff、`read` 本机 rc.3 源码、`ls` 本机 `~/.dsh`。**没有** `npm install`、**没有** `npm pack`/build、**没有**运行 `dsh`、**没有**挂载/激活任何插件、**没有**执行 `taskboard.py`/`bus.py`、**没有**启动 Web GUI。因此本 memo 里关于「挂载会失败」「子代理会继承父 preset」「claim 会互相覆盖」的结论都是**源码契约推断**，不是运行时观察；需要实跑才能升级为 `[RUN]`。

## 卡片偏差表（card-deviation table）

| # | 卡片断言（行） | 证据 | 判定 |
|---|---|---|---|
| 1 | 「版本(本次读) `0.9.2`」（原 69 行版 L42） | 现卡 L43 已改为 `HEAD ed9a19d`，并注明 npm 0.9.2=`d61da21` 空 `apply()`、tag `v0.9.2` 自述 0.9.1 | **已修**；坐标细节以 Provenance 的三棵树为准 |
| 2 | 「`main: lib/index.js`」（原 L46） | 现卡 L47 已区分 HEAD（`lib/index.js` + `dsh.plugin.json`）与 npm 0.9.2（`index.js`，无 `lib/`） | **已修** |
| 3 | 「`apply()` 是空实现……只把文件拷到…」（原 L47） | 现卡 L48 已区分：npm 0.9.2 空实现且不拷；HEAD 才拷贝到已失效目录 | **已修**；「死目录」结论仍成立（见第 7 行） |
| 4 | 「17 条各自独立注册的工具行」（L25/L63） | HEAD 与 npm 树均有 17 条 `expert_*` + 2 条通用 + 2 条 disabled 外部 | **成立**（行数 17） |
| 5 | 「17 条 = 17 个成员；成员=配置出来的可续子代理」（L13/L14/L25/L62-63） | 17 行是 17 个委派**工具别名**；`agentPreset` 0 次，孩子继承父 preset；唯一个体化字段 `persona` 被禁；`maxDepth` 默认 1、`maxActive` 默认 8 | **不成立**：成员身份未实现，只有 17 个入口 |
| 6 | 「17 行全部带 `persona`，所以 17 行全部挂载失败」（L29） | 条件成立（若挂载）；但当前**根本没有 preset 声明**，目录也无人读，所以「加载即抛错」不会发生；另外还有 `persona.text` 与 `workflow-worker-thread` 两处更早的硬失败 | **方向对、机制不全**：失败点更多，且当前是「静默不挂载」而非「报错」 |
| 7 | 「部署目录已失效；现行做法是 bundle 里挂 `dsh-agent-preset` + `config.id/name/plugins`」（L30） | `[SRC-DSH]` skill:70、rc.3 无 reader、本机目录不存在；agent-preset Config `{id, name?, plugins}` | **成立**（`name` 可选） |
| 8 | 「`dsh plugin add dsh-expert-mode`」（L46，转述 README） | rc.3 `plugin` 子命令 `requiredOption("--profile")`，且只转发 pnpm；bundle 需在 `dsh.profile.bundles` | **命令在 rc.3 不可用**；补 `--profile` 也只装包不挂 bundle |
| 9 | 「taskboard `claim` 是读→校验→整份覆写，两专家同时 claim 都会通过」（L31/L55） | `taskboard.py:273-292`、`:97-100`；无 `flock`/`fcntl`/`O_EXCL`/`os.replace`；lost update | **成立**；补充 `_next_id` 也会并发撞号 |
| 10 | 「手动 `recover` + `stale > 300s` 直接回 `ready`；无存活探测」（L56） | `taskboard.py:156-180`；默认 300、只比 `updated_at`、无 PID/心跳；`recover` 手动 | **成立**；补充：回滚绕过迁移表，活专家后续 `done` 会被判非法，任务可被重复认领 |
| 11 | 「文件总线是黑板不是 P2P；没有任何投递/唤醒；PROTOCOL 自己承认；第 7 项未勾」（L32） | `bus.py:103-164`、`:126-147`；`PROTOCOL.md:21`、`:3`、`:161` | **成立**；补充 `_next_seq` 非原子、`--all` 参数无效 |
| 12 | 「省 28% token 无来源；全仓只两行 README；度量文档是 3230→930 字、71%」（L33） | README 两行；`test-progressive-disclosure.md:48/64/69` | **成立** |
| 13 | 「13★ / 374 次/月；catalog 5★ → ×2.6」（L15） | shields `13`；npm point `374`（09-30..10-29）；`data/stars.json` 5★@2026-08-19 | **成立** |
| 14 | 「不需要 roster / spawn/remove 工具；没有官方 Team 的 Flat immutable roster 限制」（L25） | 组合无 roster/无 spawn-remove；但也没有成员身份与成员生命周期；`maxDepth`/`maxActive` 由宿主限制 | **半成立**：形式无 roster，代价是成员不可区分、不可递归、并发上限 8 |
| 15 | 「成员边界就是工具边界，模型看得见、叫得出」（L63） | 17 个工具描述来自同一个 `providerWording()`，只差 `toolName`；prompt 还叫模型用不存在的 `expert_delegate` | **弱成立/有缺陷**：看得见名字，叫不出不同的「人」 |
| 16 | 「它在本机 DSH 0.2.1-rc.3 上装不起来」（L14/L23） | 结论对：无 preset 声明 + 死目录；若迁移则 `persona.text` / 17×`persona` / `workflow-worker-thread` 三处失败 | **结论成立**，但卡片给出的**五条原因不完整且顺序不对**（真正首要的是「没有声明」，不是 `persona`） |

## [OPEN]

1. **`backgroundMode` 的确切行为**：rc.3 的 Config 没有这个键；`Object.hasOwn` 守卫暗示未知键不会被 schema 剥掉，但这只是推断。未实跑，无法确定它是被忽略还是被别的校验拒绝。`[OPEN]`
2. **`dsh.plugin.json` 是否被 rc.3 任何路径读取**：安装树 `lib/*.js` 与 plugin-manager 里没找到 `dsh.plugin.json`/`targetDir` 的 reader；它可能是 dsh.so registry 的元数据。没有实装验证。`[OPEN]`
3. **迁移到 `@deepseek-ai/dsh-agent-preset` 后的完整失败清单**：本 memo 只验证了三处（`persona.text`、17×`persona`、`workflow-worker-thread`）和两处默认值（`maxDepth`/`maxActive`）；没有逐键核对整份 600 行组合，可能还有别的 rc.3 已改名的键。`[OPEN]`
4. **实际挂载/运行行为**：未执行，所有「会失败」都是按 Config schema、`mountPreset` 审计和 apply 守卫的静态推断。若要在 `[RUN]` 级别确认，需要在隔离 profile 里装 bundle、声明 preset、观察 `preset-expert-mode` 的 diagnostic。`[OPEN]`
5. **GitHub 侧签名/check-runs**：API 本轮 403（rate limit），未能读取 commit verification、tag 对象签名或 check-runs；tag 已用 `git cat-file -t` 确认是轻量 tag（commit 对象）。`[OPEN]`
6. **旧宿主是否真的读过 `~/.dsh/.agent-presets/`**：只验证了 rc.3 不读；rc.3 的 skill 只说明「Before declaration rows」它曾经是用户 preset 目录，没有给出具体版本；没有追溯 0.1.x/0.2.0 的历史行为。`[OPEN]`
7. **`.expert-mode/router/` 是否构成第二条组合**：HEAD 新增的 router 目录含 `agent.cordis.yml` 与两个 `.mjs`，本 memo 未展开；卡片也没提。`[OPEN]`
