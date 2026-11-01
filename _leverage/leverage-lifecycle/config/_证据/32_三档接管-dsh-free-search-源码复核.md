---
title: "证据 32 · free-search 源码复核（0.9.26）"
domain: lifecycle
kind: evidence
positioning: "固定版本、tarball 摘要、接管判定与运行时 reclaim 的原始定位。"
read_when: "复核 config/32；或想抄“只接出厂默认、显式选择让路”的判定。"
status: observed
updated: 2026-11-01
budget: 95
---
# free-search 源码复核

> **固定版本**：`dsh-free-search@0.9.26`
> **gitHead**：`7c30dd059e1d9de4ffc8b779978b2152af84b0ec`
> **tarball**：`https://registry.npmjs.org/dsh-free-search/-/dsh-free-search-0.9.26.tgz`
> **sha256（前 24 位）**：`51d7e7425a6ffd1cf389bfba…` · **大小**：231,171 B · **文件数**：18
> **抽取位置**：`.work/mine/dsh-free-search/package/`（`.work/` 已 gitignore）

## 1. 包清单事实 `[PKG]`

| 字段 | 值 |
|---|---|
| version | `0.9.26` |
| `dsh.bundle` | 有 |
| `dsh.client` | 有（`platform: web`） |
| `bin` | 无 |

## 2. 符号命中（S3）

| 符号 | 命中 | 位置 |
|---|---|---|
| `webServer.register` | 1 | `lib/index.js`（设置桥 `/api/dsh-free-search-settings`） |
| 其他 | 0 | — |

**注意**：接管逻辑本身**不落在符号表里**——它是改另一行的 config，不是注册新能力。这是 `CARRIERS` §3.1 兜底规则的第三次适用场景。

## 3. 关键原文

```js
// lib/index.js:3713-3714 —— 接管开关与条件
// 是否在 web.fetchProvider 为空/出厂默认 http 时接管 fetch（#83：显式 pin http 的用户可关掉）。
fetchProviderTakeover: z.boolean().default(true).volatile(),
```

```js
// lib/index.js:241-248 —— 进程内日志去重（apply 会重入）
// 同一条接管/冲突日志在一个进程里只打一次：rc.2 的启动重入会把同样的 warn 刷到 65ms 一条，
// 日志噪音会盖住真正的问题（#82）。
const loggedOnce = new Set();
const logOnce = (log, level, message) => { if (loggedOnce.has(message)) return; loggedOnce.add(message); ... };
```

```js
// lib/index.js:4536-4552 —— 被重置后补一次接管
// #86：DSH 设置里的「DeepSeek 搜索 API」开关关掉时会把整行 `- id: web` 删掉，
// provider 回到出厂默认 `deepseek-official`（模型搜索，更慢更贵），而插件只在加载时接管过一次。
// 这里在 web 配置变化后补一次运行时接管；只认「出厂默认」，绝不抢显式选择的 `deepseek-search-api`。
let reclaimAttempted = false;
const reclaimOfficialDefaults = (next) => {
  if (reclaimAttempted) return;
  const config = next.config ?? {};
  const ops = [];
  if (config.searchProvider === "deepseek-official") takeOverOps(ctx.web, "searchProvider", provider.id, ops);
  if ((config.fetchProvider === "http" || config.fetchProvider === undefined) && current().fetchProviderTakeover !== false)
    ...
```

```js
// lib/client.js:391-392 —— 开关旁的人话说明
fetchTakeoverLabel: "自动接管 web_fetch",
fetchTakeoverHint: "开启时：web.fetchProvider 未设置或仍是出厂默认 http 会接管为 fs-quality-fetch。如果你刻意 pin 了 http（例如只想用内置抓取），关掉此项。",
```

## 4. 未复核

- "出厂默认值"清单的来源与跟版方式（只看到 `http` 与 `deepseek-official` 两处判定）。
- reclaim 与用户手动修改的竞态。
- `desktop` profile 下的一致性（无实机）。
- 接管后的实际搜索质量与回退链。
