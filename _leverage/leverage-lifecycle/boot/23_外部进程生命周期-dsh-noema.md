---
title: "外部进程生命周期 · noema：懒起、保活、退避"
domain: lifecycle
kind: sample
positioning: "把外部进程的四条策略写进配置默认值：何时起、空闲是否退、崩了怎么重启、并发怎么只起一个。"
takeaway: "外部进程不是“起一次就完”：默认值决定它是常驻还是常死，而 single-flight 与退避决定它不会把宿主拖垮。"
read_when: "要在插件里拉起外部进程（Python/二进制/本地服务）；或排查“功能时有时无”。"
status: observed
updated: 2026-11-01
budget: 140
---
# 外部进程生命周期 · noema

> **阶段**：起 · **载体**：host-row（+ web-route：状态页；+ client-slot） · **兼看**：配
> **影响力**：npm 近 30 天 **2,101**（2026-11-01，42 个过影响力门的 bundle 之一）
> **研究范围**：`@zseven-w/dsh-noema@0.1.0-rc.6`（**registry 无 `gitHead`**，按版本 + tarball 摘要钉），sha256 `0c3f85c1…`（1,124,455 B，74 文件）；DSH 对照 `0.2.1-rc.3`
> **证据成熟度**：源码级（进程管理与配置默认值实读；未实机拉起）
> **一句话**：它把"外部进程活得怎么样"写成了六个默认值，而不是散在代码里的 if。
> **借鉴价值**：**① 空闲退出默认关、保活默认开；② 重启要退避且只认 `exited`；③ 并发调用共享同一次 spawn。**

## 它想干什么 · 为什么值得借鉴

**意图。** 给 DSH 挂一套长期记忆：本地跑一个 memory server 进程，插件负责它的生死 `[SRC-TARGET]`（`lib/server-manager.js:4-5` 的模块注释）。

**意义。** 生命周期里"起"这一层最常见的坑是**外部进程**：起不来、起多个、崩了没人管、空闲被误杀。多数插件只写"首次调用时 spawn"，然后靠运气。这个样本把策略收敛成配置项与两条循环（保活 tick、空闲计时器）。

**用户价值。** 装之前，用户要自己跑一个服务、自己保证它不死；装之后，`autoStart: true` 让它在挂载时就起来，`keepAlive: true` 每 5 秒看一眼，崩了 1 秒后自动重启 `[SRC-TARGET]`（`lib/settings.js:10-15`）。代价是它默认**不让进程闲时退出**——对省资源的用户，这是一个要改的默认值。

**表达。** 默认值本身就是设计主张：

| 配置 | 默认 | 含义 |
|---|---|---|
| `autoStart` | `true` | 挂载即起，不等第一次调用 |
| `idleTimeoutMs` | **`0`（关）** | 空闲**不**自动退出 |
| `keepAlive` | `true` | 开着后台看护 |
| `keepAliveIntervalMs` | `5000` | 每 5 秒一次 |
| `restartDelayMs` | `1000` | 崩了 1 秒后才允许重启 |
| `callTimeoutMs` | `30000` | 单次调用上限 |

## 1. 阶段与载体

- **阶段**：起。它管的是"进程在不在"，不是"装没装"。
- **载体**：`host-row`（管理器）+ `web-route`（状态页）+ `client-slot`。
- **兼看**：配。六个默认值全是配置。

## 2. 机制

### 三条循环

1. **懒起 / 预起**：`autoStart` 决定挂载即起还是首次使用才起 `[SRC-TARGET]`（`settings.js:10`；`server-manager.js:4`）。
2. **保活**：`keepAliveTick` 每 `keepAliveIntervalMs` 检查一次，**只在 `state === 'exited'` 且距退出超过 `restartDelayMs` 时**才重启 `[SRC-TARGET]`（`:106-121`）。
3. **空闲退**：`idleTimeoutMs > 0` 时才挂 `setTimeout`，否则永不退 `[SRC-TARGET]`（`:260`）。

### 并发：只起一个

`ensureRunning()` 的注释是 *concurrent callers share one spawn* `[SRC-TARGET]`（`:123`），用 `this.starting` 做在途去重。**没有它，两个并发调用会拉起两个进程。**

### 三条失败态

| 态 | 表现 | 用户看到什么 |
|---|---|---|
| **进程崩了** | `keepAlive` 开 → 1 秒后重启并 `warn` | 短暂不可用，随后恢复 `[SRC-TARGET]`（`:117-121`） |
| **保活关掉** | 崩了没人管，直到下次调用 | "功能时有时无"，且没有日志 |
| **启动中被打断** | 在途 spawn 未被复用 | 两个进程抢同一个数据目录 |

## 3. 设计取舍

| 取舍 | 选择 | 代价 |
|---|---|---|
| 默认常驻还是省资源 | `idleTimeoutMs: 0` + `keepAlive: true`：**默认常驻** | 空闲也占内存；省资源的用户要自己改 |
| 崩溃恢复 | 后台 tick 重启，不阻塞调用方 | 有最多 `keepAliveIntervalMs` 的空窗 |
| 重启节流 | `restartDelayMs` 防抖 | 连续崩溃时要等一秒 |
| 超时 | 调用级 `callTimeoutMs` 与重启级 `restartDelayMs` 分开 | 两个时间语义要各自理解 |

## 4. 与宿主既有行的边界

它**不接管宿主的进程管理**，只拉起自己的子进程，并把状态通过一条 status 路由暴露 `[SRC-TARGET]`（`lib/status-route.js` 的 `webServer.register` 一处）。宿主退出时它必须自己收尾——否则会留下孤儿进程 `[OPEN]`。

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 外部进程该常驻还是闲时退出 | 把两个选择都做成配置，**默认选"常驻"**（`idleTimeoutMs: 0` + `keepAlive: true`） | `[SRC-TARGET]` `settings.js:11-12`（`idleTimeoutMs: 0`、`keepAlive: true`）；`server-manager.js:260`（空闲计时器） | 默认"一直在"，用户无需担心；代价是占资源 | 明确默认档，并给出"省资源"的开关 | 只对"功能价值在随时可用"的产品成立 | 默认闲时退出 → 每次冷启动都有延迟，用户以为坏了 |
| 崩了要不要自动拉起 | 后台 tick + **只认 `exited`** + `restartDelayMs` 退避 | `[SRC-TARGET]` `server-manager.js:106-121` | 自愈且不风暴；代价是有一段空窗 | 定义"什么算崩"、"多久后重启" | 只对"可重启且有状态恢复"的进程成立 | 无退避 → 崩溃循环把 CPU 打满 |
| 并发调用起多个进程 | 在途去重（`starting`），`ensureRunning` 被多处共享 | `[SRC-TARGET]` `server-manager.js:123`（注释与实现） | 一个进程；代价是要处理"启动中"的等待语义 | 给 spawn 加 single-flight 包装 | 只对"多入口触发启动"的产品成立 | 不去重 → 两个进程抢同一数据目录 |
| 超时用哪个 | 调用超时与重启节流**分开两个字段** | `[SRC-TARGET]` `settings.js:14-15` | 语义清晰；代价是多一个配置 | 调用级、重启级、启动级各一个 | 只对"有远程调用"的进程成立 | 共用一个 timeout → 调慢点就触发重启 |

## 6. 失效与开放问题

- `[OPEN]` 宿主退出时是否清理子进程（未见 shutdown hook；孤儿进程风险）。
- `[OPEN]` `idleTimeoutMs > 0` 时的实际行为（计时器在 `:260`，触发条件未逐行读）。
- `[OPEN]` `bundled-binary.js` 的二进制探测与版本校验（本卡未展开）。
- `[OPEN]` **无 `gitHead`**，物证止于 tarball 摘要。
- `[OPEN]` 未实机拉起。

## 7. 兼看

- 起：与 [`boot/22`](./22_重启取证-dsh-update-checker.md) 是一对——**22 管宿主自己的重启取证，23 管插件子进程的生死**。
- 配：六个默认值属于 [`config/README.md`](../config/README.md) §1 的"bundle 层默认值"。
