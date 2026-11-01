---
title: "预置工作区与自有会话 · 24pa：打开就是我的东西"
domain: lifecycle
kind: sample
positioning: "在 boot 时创建工作区、预置两个确定性会话，并在预设被占用时换 id 而不是覆盖。"
takeaway: "“开箱即用”可以完全用宿主服务做出来：工作区 + 会话 + 预设，不需要自带启动器；关键是身份要可推导、冲突要可让位。"
read_when: "要让产品打开就落在自己的工作面；或要预置会话又怕抢了用户的预设。"
status: observed
updated: 2026-11-01
budget: 140
---
# 预置工作区与自有会话 · 24pa

> **阶段**：首启 · **载体**：boot-hook（`workspaceRegistry` + `sessionController`） · **兼看**：装
> **影响力**：npm 近 30 天 **5,111**（2026-11-01，42 个过影响力门的 bundle 之一）
> **研究范围**：`@benz-ai-x/dsh-24pa@0.2.1-rc.5.1`（**registry 无 `gitHead`**，按版本 + tarball 摘要钉），sha256 `e28d5a02…`（632,497 B，140 文件）；DSH 对照 `0.2.1-rc.3`
> **证据成熟度**：源码级（工作区与会话创建、冲突分支实读；未实机启动）
> **一句话**：它不造启动器，**用宿主自己的工作区与会话服务，把"打开就该是这样"做出来**。
> **借鉴价值**：**① 首启体验可以只用 host 服务实现；② 身份要可推导（路径哈希），不是随机；③ 预设冲突时换 id + 通知，绝不覆盖历史。**

## 它想干什么 · 为什么值得借鉴

**意图。** 把 DSH 变成一个"24 小时私人助理"：一个专属工作区、两条常驻会话（飞书中继 + 本地助理），一打开就在那儿 `[SRC-TARGET]`（`lib/runtime.js:1248-1256`）。

**意义。** 这正是"插件当产品"最省力的形态——**不换表层、不造 launcher**，只在 boot 时消费 `workspaceRegistry` 与 `sessionController` 把产品该有的东西摆好。前面 [`FIRST-RUN`](./README.md) §6 讲的原语，这里是一次完整落地。

**用户价值。** 装之前，用户要自己建工作区、自己开两个会话、自己记得哪个是飞书哪个是本地；装之后，工作区叫「24私助」，两条会话已经在那儿，**重启也不会多出来一堆** `[SRC-TARGET]`（`:1246-1251` 的 saved-state 复用与确定性 id）。代价是它替用户做了命名与摆放的决定，用户不喜欢就得自己删。

**表达。** 冲突时的处理最能说明取舍 `[SRC-TARGET]`（`:1592-1598`）：不是覆盖，而是**换一个新 id 再建**，并推一条通知——"旧会话 `<previous>` 已选择其他预设，历史保留；24私助已建立新的…会话"。

## 1. 阶段与载体

- **阶段**：首启。它决定"第一次打开看到什么"。
- **载体**：`boot-hook`——`workspaceRegistry.create(...)` 与 `sessionController.create(...)`，都在宿主服务层 `[SRC-TARGET]`。
- **兼看**：装。patch 里用 `!!js` 按平台门控行、按 `dshHomePath()` 定状态目录（见 §4）。

## 2. 机制

### 三段式首启

```js
// lib/runtime.js:1246-1257（节选）
const saved = await repos.workspaceState.get(real);
next = {
  workspace: { ...await this.ctx.workspaceRegistry.create(real, '24私助'), statePath: real },
  accessSessionId: saved?.feishu_session_id ?? `pa24-${hash(real).slice(0, 12)}-feishu`,
  localSessionId:  saved?.local_session_id  ?? `pa24-${hash(real).slice(0, 12)}-local`,
};
next.accessSessionId = await this.prepareOwnedSession('feishu', next);
next.localSessionId  = await this.prepareOwnedSession('local', next);
await repos.workspaceState.save(real, { feishuSessionId: next.accessSessionId, localSessionId: next.localSessionId });
```

1. **以真实路径为键**：`workspaceState.get(real)` 决定是否复用；工作区在宿主里按路径建。
2. **会话 id 可推导**：`pa24-<hash(real) 前 12 位>-feishu/local`。**同一个路径得到同一组 id**，所以重启不会制造新会话。
3. **会话带预设**：`agentPreset: 'pa24'` `[SRC-TARGET]`（`:1588`）。

### 冲突：换 id，不覆盖

```js
// lib/runtime.js:1586-1598（节选）
const create = () => this.ctx.sessionController.create({
  sessionId: target[key], workspaceId: target.workspace.id, agentPreset: 'pa24' });
try { await create(); }
catch (error) {
  if (error.code !== 'agent-preset/conflict') throw error;
  target[key] = `pa24-${hash(...)}-${kind}-${randomUUID().slice(0, 8)}`;   // 换 id
  await create();
  target.sessionNotices.push({ dedupKey: `notice:session-rebound:${target[key]}`,
    text: `旧会话 ${previous} 已选择其他预设，历史保留；…已建立新的…会话。` });
}
```

**它只为自己那一种冲突写分支**（`agent-preset/conflict`），其余照常抛出——不是"什么都兼容"，而是"知道这一种会发生"。

### 三条失败态

| 态 | 表现 | 用户看到什么 |
|---|---|---|
| **工作区建不出来** | 路径不可用（目录不存在/无权限） | 启动期报错，产品打不开——`workspaceRegistry.create` 需要真实路径 |
| **会话 id 被占** | `agent-preset/conflict` | **能自愈**：换 id 重建 + 一条通知，旧历史不动 |
| **状态没存上** | `workspaceState.save` 失败 | 下次启动会重建一组 id，出现"重复会话" |

## 3. 设计取舍

| 取舍 | 选择 | 代价 |
|---|---|---|
| 首启怎么摆 | 用宿主的工作区与会话服务，不造启动器 | 受宿主能力约束（`workspaceRegistry` / `sessionController` 必须存在） |
| 会话身份 | 路径哈希 + 保存的 id，而不是随机 | 同一个目录永远同一组 id；代价是换目录就换一组 |
| 冲突策略 | 换 id + 通知，历史保留 | 用户会多出一个会话，但不会丢数据 |
| 平台差异 | patch 里 `!!js process.platform === 'win32'` 门控行 `[SRC-TARGET]`（`cordis.patch.yml:43`、`:46`） | 两个平台的配置分叉写在补丁里，而不是代码里 |
| 状态目录 | `!!js dshHomePath('24pa')` 等 `[SRC-TARGET]`（`:167-171`） | 跟着 `DSH_HOME` 走，可被环境变量覆盖（`PA24_WORKSPACE`） |

## 4. 与宿主既有行的边界

它**不动宿主的默认工作区**，只**新建**一个并把自己的会话放进去。`availableWorkspaces` 是把 `workspaceRegistry.list()` 原样透出 `[SRC-TARGET]`（`:4471`）——读宿主的事实，不复制一份。

这条边界很重要：**产品可以有"自己的工作面"，但不该假设"用户只有我这一个工作面"。**

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 想让产品"打开就是自己的样子"，又不想造启动器 | 在 boot 时用宿主的 `workspaceRegistry` / `sessionController` 把工作区与会话摆好 | `[SRC-TARGET]` `lib/runtime.js:1248`（建工作区）、`:1588`（建会话带预设） | 复用宿主的持久化与 UI，零额外入口；代价是强依赖这两个服务存在 | 定义"我的工作面"由哪几个宿主对象组成 | 只对暴露这两个服务的宿主成立 | 自己再存一份工作区列表 → 与宿主不同步，用户看到两份 |
| 每次启动都预置，怕重复 | 身份**可推导**（路径哈希）+ 已保存 id 优先 | `[SRC-TARGET]` `:1250-1251`（`pa24-${hash(real).slice(0,12)}-…`）、`:1246`（saved 复用） | 重启幂等，不制造重复会话；代价是换目录就换身份 | 选一个稳定键（路径/项目 id）做哈希输入 | 只对"路径稳定"的场景成立 | 用随机 id → 每次启动多一组会话，用户被迫手工清理 |
| 预置的会话可能被别的预设占用 | 捕获**具体**错误码（`agent-preset/conflict`），换新 id 重建，并给用户一条通知 | `[SRC-TARGET]` `:1592-1598` | 历史保留、体验连续；代价是用户会多看到一个会话 | 明确"哪种冲突要自愈、哪种要抛" | 只对"会话预设归属"这类冲突成立 | 覆盖原会话 → 用户的历史被顶掉；或不处理 → 产品永久起不来 |
| 平台差异写在哪 | 写进 patch 的行门控（`!!js process.platform`），代码只认"这一行在不在" | `[SRC-TARGET]` `cordis.patch.yml:43`、`:46` | 一份代码两平台；代价是补丁可读性下降 | 把平台判断收敛到 patch，代码里不留 `platform` 分支 | 只对"行级可门控"的宿主成立 | 代码里到处 `if (win32)` → 补丁与代码两套事实 |
| 状态放哪 | 用宿主 home 的路径函数 + 环境变量覆盖 | `[SRC-TARGET]` `cordis.patch.yml:167-171`（`dshHomePath`）、`:171`（`PA24_WORKSPACE`） | 跟着 `DSH_HOME`；代价是启动时的 home 必须一致 | 所有路径都从 home 派生，不写死 | 只对"home 可注入"的宿主成立 | 写死 `~/.dsh` → 换 home 或隔离环境时全部错位 |

## 6. 失效与开放问题

- `[OPEN]` `workspaceRegistry.create` 对已存在路径的行为（复用还是报错）——本卡没在实机验证。
- `[OPEN]` `agent-preset/conflict` 之外还有哪些冲突码（只看到这一种被处理）。
- `[OPEN]` `sessionNotices` 如何呈现给用户（本卡只看到入队）。
- `[OPEN]` **无 `gitHead`**：物证只到 tarball 摘要，无法上溯 commit。
- `[OPEN]` 未实机启动（本机不装）。

## 7. 兼看

- 首启：与 [`first-run/41`](./41_自检即首启-dsh-skill-cockpit.md)、[`42`](./42_命令即验收面-dsh-tool-guardian.md) 构成三种做法——**独立进程自检 / 会话内命令 / 预置工作面**。
- 装：patch 的 `!!js` 平台门控与 [`install/12`](../install/12_让安装器认你-dsh-origin-plugin.md) 的自定位表达式同源。
