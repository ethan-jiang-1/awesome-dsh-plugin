---
title: "证据 21 · rhine-splash 源码复核（0.2.8）"
domain: lifecycle
kind: evidence
positioning: "固定版本、tarball 摘要、index-inject 注册点与转义函数的原始定位。"
read_when: "复核 boot/21；或想知道首屏注入的顺序与转义是怎么写的。"
status: observed
updated: 2026-11-01
budget: 130
---
# rhine-splash 源码复核

> **固定版本**：`dsh-rhine-splash@0.2.8`
> **gitHead**：`8aa09619a58ec5e456eb4c358ed250767c74c1dc`
> **tarball**：`https://registry.npmjs.org/dsh-rhine-splash/-/dsh-rhine-splash-0.2.8.tgz`
> **sha256（前 24 位）**：`bfae5708f4741a3c21deb284…` · **大小**：588,189 B · **文件数**：24
> **抽取位置**：`.work/mine/dsh-rhine-splash/package/`（`.work/` 已 gitignore）

## 1. 包清单事实 `[PKG]`

| 字段 | 值 |
|---|---|
| version | `0.2.8` |
| `dsh.bundle` | 有（`./cordis.patch.yml`） |
| `dsh.client` | 有（`platform: web`，9 个 inject） |
| `bin` | 无 |
| `engines` | 无 |

## 2. 符号命中（S3）

```text
grep -rnoE 'tapIndex|index-inject|webServer\.register|commands\.register|agents\.create|
            workspaceRegistry|workingDirectory|installBundle|failOnStartupError|!!js'
```

| 符号 | 命中 | 位置 |
|---|---|---|
| `index-inject` | 1 | `lib/index.js:439` |
| `webServer.register` | 5 | `lib/host/{update,store,notify,billing,archives}.js` |
| `workspaceRegistry` | 7 | `lib/host/archives.js`（`:32`、`:64`、`:131`…） |
| 其他 | 0 | — |

**注意**：本卡取的是 `index-inject` 这条载体；`webServer.register` 出现在四个 host 模块里，属于账单/通知等旁支功能，不构成本卡骨架。

## 3. 关键原文

```js
// lib/index.js:438-445
// Append after theme bootstrap rows: do not pass Cordis's prepend option.
ctx.on('webserver/index-inject', (table) => {
  const resolved = readConfig(config);
  ...
  table.push(...buildInjections(resolved, { ...assets, brand }));
});
```

```js
// lib/index.js:312-330（节选）
export function buildInjections(config, assets) {
  const safeJson = (value) => JSON.stringify(value)
    .replace(/</g, '\\u003c')
    .replace(/\u2028/g, '\\u2028')
    .replace(/\u2029/g, '\\u2029');
  const safeStyle = (css) => css.replace(/<\/style/gi, '<\\/style');
  return [
    ...(assets.themeCss ? [{ kind: 'style', text: safeStyle(assets.themeCss) }] : []),
    ...
    { kind: 'script', placement: 'body',
      text: 'globalThis.__RHINE_BRAND__=...;globalThis.__RHINE_SPLASH__=...;\n'
          + '(function(c){const root=document.documentElement;...})(globalThis.__RHINE_SPLASH__);\n'
          + assets.js },
  ];
}
```

```js
// lib/client.js:30
splashWhen: { type: "choice", choices: ["launch", "daily", "update"], label: "sw_", section: "splash", command: true },
```

```js
// lib/host/archives.js:131
if (typeof ctx.inject === 'function') ctx.inject(['workspaceRegistry', 'sessionPersistence'], (child) => { ... });
```

```js
// lib/splash.js:69-85 —— 开屏频率的两套存储
if (!cfg.replayOnReload) {
  if (sessionStorage.getItem('rhine-splash:played')) return
  sessionStorage.setItem('rhine-splash:played', String(Date.now()))
}
if (!cfg.force) {
  const seen = JSON.parse(localStorage.getItem('rhine-splash:splash-seen'))  // { day, version }
  if (cfg.splashWhen === 'daily' && seen?.day === today) return
  if (cfg.splashWhen === 'update' && cfg.version && seen?.version === cfg.version) return
  localStorage.setItem('rhine-splash:splash-seen', JSON.stringify({ day: today, version: cfg.version }))
}

// lib/splash.js:99-105 —— 主题判断依赖“主题引导行已经跑过”
const dark = cfg.theme === 'dark' || (cfg.theme !== 'light' && (
  doc.documentElement.dataset.dsThemeSource !== undefined
    ? doc.body.hasAttribute('data-ds-dark-theme')
    : matchMedia('(prefers-color-scheme: dark)').matches
))

// lib/splash.js:121 / :640-641 —— maxWait 兜底
const maxWait = Math.max(num(cfg.maxWait, DEFAULTS.maxWait), exitAt)
later(leave, maxWait); later(destroy, maxWait + exitMs + 2000)
```

**宿主侧** `[DSH]`：`dsh-host-webserver/lib/index.js:517-535` 每次渲染 index.html 现场 `emit` 收表，订阅者按激活顺序 push；`:84-100` 按 head/body 分组、组内表序拼接；`:529-535` 先渲染表、再跑 `tapIndex`；`:23-60` 只转义属性值，`script`/`style` 文本原样输出。

## 4. 与产品册/本册其它结论的呼应

- `ctx.inject([...], cb)` 是可选依赖的正解——与 [`TRAPS`](../../practice/TRAPS.md) §11 互证。
- 注入体在 `placement: 'body'`，且**同步**改 `documentElement`，这是"不闪"的实现基础。

## 5. 已核 / 未复核

- **已核**：`splashWhen` 的消费点在 `lib/splash.js:69-85`（sessionStorage 每会话一次 + localStorage `{day, version}`；`replayOnReload`/`force` 绕过）。
- **已核**：`maxWait` 存在：默认 8000ms（`lib/index.js:109`、`:264-267`），客户端 `Math.max(cfg.maxWait, exitAt)`（`lib/splash.js:121`），到点强制离场（`:640-641`）。
- **已核**：注入表每次渲染现收、按激活序渲染（`dsh-host-webserver/lib/index.js:517-535`、`:84-100`）；主题判断读的是主题行写下的 `data-ds-theme-source` / `data-ds-dark-theme`（`lib/splash.js:99-105`），因此 append 是数据依赖而非风格。
- `[OPEN]` 注入点失效时是否有告警（判断为静默降级，未实测）。
- `[OPEN]` 宿主换 HTML 骨架后注入点是否仍存在（未实测）。
