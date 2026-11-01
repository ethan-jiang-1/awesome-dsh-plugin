---
title: "CONFIG · 阶段③：配置的四个家与它们的优先级"
domain: lifecycle
kind: playbook
positioning: "DSH settings、自己的文件、localStorage、profile 补丁层四个配置归属，以及 home 层能覆盖不能供货。"
takeaway: "home 层是唯一跨 profile 的配置层，但它只能覆盖行、不能提供包；选错家就等于选错覆盖面。"
read_when: "要决定某个偏好放哪；或排查“配置在这儿改了、另一个面没变”。"
status: living
updated: 2026-11-01
budget: 150
---
# 阶段③ · 配

## 1. 原生怎么做

**配置有四层，从低到高**（与 [`BOOT`](../boot/README.md) §1 同一套叠加序）：

| 层 | 位置 | 覆盖面 | 谁写 |
|---|---|---|---|
| bundle 默认值 | 每个 bundle 的 `cordis.patch.yml` | 所有用它的 profile | 包作者 |
| profile 用户层 | `$DSH_HOME/profiles/<p>/cordis.patch.yml` | 这一个 profile | 用户 / 你的插件 |
| **home 层** | `$DSH_HOME/cordis.patch.yml` | **所有 profile** | 用户 |
| 临时覆盖 | `--patch <file>` | 这一次启动 | 调用方 |

另有**设置域**（settings）：按命名空间读写、每次写带 `revision`、并发写被拒为 `settings/conflict` `[CARD]`（产品线接缝表口径，本册未复核）。

**读配置的三种视图** `[DSH]`（`lib/bin.js` 的 launcher 选项）：

| 命令 | 给出什么 |
|---|---|
| `--dump-config` | 合成后的完整树（含 home 层与 `--patch`） |
| `--dump-default-config` | 去掉用户层与 `--patch` 的树 |
| `--dump-config-schema` | 不挂载，只给条目与补丁的 JSON Schema |

## 2. 实测读到什么

| 实验 | 观察 |
|---|---|
| E6 | 在 `$DSH_HOME/cordis.patch.yml` 写 `- id: hmr / disabled: true`，**`bundlep` 与 `web` 两个 profile 的合成配置里同时变红** |
| E7 | 往 home 层插一行新包（`dsh-feas-probe`），`--dump-config` **照常显示这行** |
| E8 | 真启动同一个 profile：`ERR_MODULE_NOT_FOUND … imported from profiles/web/`，报 `1 entry did not activate`，**服务照常起** |

**结论要拆成两句**：

1. **home 层能覆盖**：禁用、改 config、对已存在的行做任何 patch 操作，跨 profile 生效 `[RUN]`。
2. **home 层不能供货**：它不改变任何 profile 的 `dependencies`，所以插入一个该 profile 没装的包，只在 dump 里好看、启动时 import 失败 `[RUN]`。

**这对分发意味着什么**：想让"所有面都默认启用我的功能"，靠 home 层做不到。正确做法是**各自装进各自的 profile**，或者让用户在他的面上用应用内装。

## 3. 样本怎么偏离

产品线 25 张卡里，配置落在四个**归属** `[CARD]`——**注意：§1 的"四层"是补丁叠加序，这里的"四家"是配置归属，两组维度不同，不要混用**：

| 家 | 样本 | 代价 |
|---|---|---|
| DSH settings 命名空间 | `43`、`71`、`31`、`18`；`42` 还会写宿主 settings | 跟随 profile；跨 profile 不共享 |
| 自己的文件 | `shell/14`（`~/.dsh-tui/settings.json`）、`shell/12`（`settings.json`）、`shell/13`（`desktop-keybindings.json`）、`61`（`$DSH_HOME/mobile-access/`）、`52`（`.plugin-health`） | 用户要记第二个位置；不跟随宿主备份 |
| **localStorage** | `11`（`dock:layout`）、`12`（`dsh-sidebar:v1:<sessionId>`） | 换浏览器即丢；跨面不共享 |
| profile 补丁行 | `profile/` 全桶，尤其 `15`（`unset` 恢复默认） | 只能表达"行级"配置 |

**一处卡内冲突**：`31` 把 `settings.register` 当作"已退役、应不存在"的接缝来断言，而 `71` 正在注册 settings 命名空间 `[CARD]`。两者版本不同、观测面不同，本册不裁决，只记：**引用"某接缝已退役"必须带版本**。

**本册样本补充**：

[`31`](./31_全禁状态-dsh-isolation-gate.md) 读不到就拒绝 ·
[`32`](./32_三档接管-dsh-free-search.md) 只接出厂默认、显式选择让路 ·
[`33`](./33_换壳保-id-dfy-bundle.md) 换包装保 id。

三张都在回答同一件事：**"没配置时是什么"必须由产品自己定义，而不能交给默认值**。

## 4. 三条判据

1. 你的配置项**要不要跨 profile**？要 → home 层或自有文件；不要 → profile 补丁或 settings。
2. 你的默认值**是不是 bundle 层**（可被更高层覆盖）？是 → 写进 bundle 的 patch，不要写死在代码里。
3. 你有没有在文档里说清"这个开关改的是哪一层"？没说 = 用户会改错层然后以为没生效。

## 5. 失效与开放问题

- `[OPEN]` settings 写入的 `revision` 冲突在插件侧的真实表现（本册未复核 `dsh-client-ui-settings` 实现）。
- `[OPEN]` localStorage 状态在 Desktop 与 web 之间是否共享（同一浏览器内核但不同 origin/端口，理论上不共享，未实测）。
- `[OPEN]` `--dump-default-config` 与 `--dump-config` 的差异是否等价于"少了 home 层"（本册只验证了后者）。

## 样本

| 文件 | 一句话 |
|---|---|
| [`31_全禁状态-dsh-isolation-gate.md`](./31_全禁状态-dsh-isolation-gate.md) | 五种“读不到”分开报，然后全部落到拒绝。 |
| [`32_三档接管-dsh-free-search.md`](./32_三档接管-dsh-free-search.md) | 只抢“没人设过”的位置；被重置后补一次。 |
| [`33_换壳保-id-dfy-bundle.md`](./33_换壳保-id-dfy-bundle.md) | 换包装不换 id，用户配置才活得下来。 |
