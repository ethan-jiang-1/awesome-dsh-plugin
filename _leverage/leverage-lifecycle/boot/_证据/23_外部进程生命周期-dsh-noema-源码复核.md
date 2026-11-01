---
title: "证据 23 · noema 源码复核（0.1.0-rc.6）"
domain: lifecycle
kind: evidence
positioning: "固定版本（无 gitHead）、tarball 摘要、进程管理三条循环与默认值的原始定位。"
read_when: "复核 boot/23；或想抄外部进程的默认值与保活策略。"
status: observed
updated: 2026-11-01
budget: 120
---
# noema 源码复核

> **固定版本**：`@zseven-w/dsh-noema@0.1.0-rc.6`
> **gitHead**：**registry 未记录**
> **tarball**：`https://registry.npmjs.org/@zseven-w/dsh-noema/-/dsh-noema-0.1.0-rc.6.tgz`
> **sha256（前 24 位）**：`0c3f85c167f4e612da9412e7…` · **大小**：1,124,455 B · **文件数**：74
> **抽取位置**：`.work/mine/_zseven-w_dsh-noema/package/`

## 1. 包清单事实 `[PKG]`

| 字段 | 值 |
|---|---|
| version | `0.1.0-rc.6` |
| `dsh.bundle` | 有 |
| `dsh.client` | 有（`platform: web`） |
| `bin` | 无 |
| `gitHead` | **无** |

## 2. 符号命中（S3）

| 符号 | 命中 | 位置 |
|---|---|---|
| `workingDirectory` | 14 | `lib/client.js`(8)、`lib/settings.js`(3)、`lib/server-manager.js`(2)、`lib/status-route.js`(1) |
| `webServer.register` | 1 | `lib/status-route.js` |
| 其他 | 0 | — |

## 3. 关键原文

```js
// lib/server-manager.js:4-5 —— 模块自述
 * The manager spawns on first use (or at mount when autoStart is set), keeps
 * one connection, applies an idle timeout, backs off restarts after crashes,
```

```js
// lib/settings.js:10-15 —— 六个默认值
autoStart: true,
idleTimeoutMs: 0,
keepAlive: true,
keepAliveIntervalMs: 5_000,
callTimeoutMs: 30_000,
restartDelayMs: 1_000,
```

```js
// lib/server-manager.js:106-121 —— 保活 tick
async keepAliveTick() {
  const now = Date.now(); const config = this.resolveConfig();
  if (!config.enabled || !config.keepAlive) return;
  if (now - this.lastKeepAliveCheckAt < config.keepAliveIntervalMs) return;
  this.lastKeepAliveCheckAt = now;
  if (this.client?.state !== 'exited') return;
  const sinceExit = now - (this.client.exitAt ?? now);
  if (sinceExit < config.restartDelayMs) return;
  this.logger?.warn('dsh-noema keep-alive: memory server exited; restarting in the background');
  await this.ensureRunning();
  this.logger?.info('dsh-noema keep-alive: memory server restarted');
}
```

```js
// lib/server-manager.js:124-136 —— 并发共享一次 spawn
async ensureRunning() {
  if (this.disposed) throw new Error('Noema memory plugin is disposed');
  const state = this.client?.state;
  if (state === 'running') return;
  if (this.starting !== undefined) { await this.starting; return; }
  this.starting = this.start();
  try { await this.starting; } finally { this.starting = undefined; }
}

// lib/server-manager.js:173-181 —— 主动停：先清 client，再 dispose
async stop() {
  this.clearIdle();
  const client = this.client;
  this.client = undefined;
  this.lastStopAt = Date.now();
  if (client !== undefined) await client.dispose();
}

// lib/server-manager.js:225-233 —— 每次 start 都先等退避窗口（手动重启也付这 1s）
const sinceStop = Date.now() - this.lastStopAt;
if (sinceStop < config.restartDelayMs) await sleep(config.restartDelayMs - sinceStop);

// lib/server-manager.js:256-265 —— 空闲计时器；启动成功与每次成功调用后都会重置
armIdle(config) {
  this.clearIdle();
  if (config.idleTimeoutMs <= 0) return;
  this.idleTimer = setTimeout(() => { ... void this.stop(); }, config.idleTimeoutMs);
  this.idleTimer.unref?.();
}
```

**状态源** `[SRC-TARGET]`：`mcp-stdio.js:58`（`stopped`）、`:154`（`starting`）、`:95`（`running`）、`:160`（`exited`）。**主动停与崩溃的区分**：`stop()` 清空 `this.client`，而崩溃保留 client 且 state 为 `exited`；`keepAliveTick` 只重启后者（`:106-121`）。

**状态端点** `[SRC-TARGET]`：`status-route.js:146-160` 先判 loopback 与 same-origin（写操作再判 JSON content-type），`:100-133` 限制 body 大小；`server-manager.js:182-214` 在 `await` 之后重新核对 `this.client === client && client.state === 'running'`，避免把旧 client 的结果当成新状态。

**收尾** `[SRC-TARGET]`：`dispose()`（`:215-223`）= `stopKeepAlive()` + `stop()`，正常卸载会 `await client.dispose()`；宿主被强杀/崩溃时来不及，仍可能留下孤儿子进程。

## 4. 已核 / 未复核

- **已核**：正常卸载路径有收尾（`dispose → stop → client.dispose`）；强杀/崩溃来不及，孤儿风险仍在。
- **已核**：`idleTimeoutMs > 0` 时启动成功与每次成功调用都重置计时器，到点 `stop()` 并打日志（`:154`、`:242`、`:256-265`）。
- `[OPEN]` `bundled-binary.js` 的二进制探测与版本校验。
- `[OPEN]` **无 `gitHead`**，物证止于 tarball 摘要。
- `[OPEN]` 未实机拉起。
