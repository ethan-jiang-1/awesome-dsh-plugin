---
title: "证据 21 · rhine-splash 源码复核（0.2.8）"
domain: lifecycle
kind: evidence
positioning: "固定版本、tarball 摘要、index-inject 注册点与转义函数的原始定位。"
read_when: "复核 boot/21；或想知道首屏注入的顺序与转义是怎么写的。"
status: observed
updated: 2026-11-01
budget: 100
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

## 4. 与产品册/本册其它结论的呼应

- `ctx.inject([...], cb)` 是可选依赖的正解——与 [`TRAPS`](../../practice/TRAPS.md) §11 互证。
- 注入体在 `placement: 'body'`，且**同步**改 `documentElement`，这是"不闪"的实现基础。

## 5. 未复核

- `splashWhen` 的消费点（"每天第一次 / 更新后"的判定实现）未定位；本卡只核到声明与文案（`lib/client.js:30`、`:311-312`）。
- fanout 提过的 `maxWait` 兜底在源码中未命中，**不写入结论**。
- 注入点失效时是否有告警（判断为静默降级，未实测）。
