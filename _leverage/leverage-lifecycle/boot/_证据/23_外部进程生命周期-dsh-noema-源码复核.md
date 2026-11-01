---
title: "证据 23 · noema 源码复核（0.1.0-rc.6）"
domain: lifecycle
kind: evidence
positioning: "固定版本（无 gitHead）、tarball 摘要、进程管理三条循环与默认值的原始定位。"
read_when: "复核 boot/23；或想抄外部进程的默认值与保活策略。"
status: observed
updated: 2026-11-01
budget: 95
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
// lib/server-manager.js:123 —— 并发共享一次 spawn
/** Bring the server up if it is down; concurrent callers share one spawn. */
async ensureRunning() { ... if (this.starting !== undefined) ... }

// :260 —— 空闲计时器（idleTimeoutMs > 0 时才挂）
this.idleTimer = setTimeout(() => { ... }, ...);
```

## 4. 未复核

- 宿主退出时的子进程清理（未见 shutdown hook）。
- `idleTimeoutMs > 0` 的完整触发路径。
- `bundled-binary.js` 的二进制探测与版本校验。
- **无 `gitHead`**，物证止于 tarball 摘要。
- 未实机拉起。
