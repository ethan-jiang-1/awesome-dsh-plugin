---
title: "证据 91 · dsh-bootstrap 源码复核（0.1.0）"
domain: lifecycle
kind: evidence
positioning: "反例的固定版本、实时影响力、机制原文与仓库时间线。"
read_when: "复核 negative/91；或想理解本册影响力门为什么承受这类误伤。"
status: observed
updated: 2026-11-01
budget: 105
---
# dsh-bootstrap 源码复核

> **固定版本**：`dsh-bootstrap@0.1.0`
> **gitHead**：**registry 未记录**
> **tarball**：`https://registry.npmjs.org/dsh-bootstrap/-/dsh-bootstrap-0.1.0.tgz`
> **sha256（前 24 位）**：`33a1840882a15b754f941390…` · **大小**：87,589 B · **文件数**：24
> **抽取位置**：`.work/mine/dsh-bootstrap/package/`

## 1. 实时影响力（2026-11-01 采）

| 指标 | 值 | 口径 |
|---|---|---|
| GitHub ★ | **1** | GitHub API `/repos/why-sir/dsh-bootstrap` |
| forks | **0** | 同上 |
| created | `2026-10-17` | 同上 |
| pushed | `2026-10-17` | 同上——**发布当天之后无提交** |
| npm 近 30 天 | **763** | `api.npmjs.org`，区间 2026-09-30 ~ 2026-10-29 |

**对照本册门槛**（★≥200 或 npm≥2,000）：两项都不过。

## 2. 包清单事实 `[PKG]`

| 字段 | 值 |
|---|---|
| version | `0.1.0` |
| `dsh.bundle` | 有 |
| `dsh.client` | **无**（界面靠首屏注入 + 自有路由） |
| `bin` | 有 |

## 3. 符号命中（S3）

| 符号 | 命中 | 位置 |
|---|---|---|
| `webServer.register` | 2 | `lib/index.js`、`lib/routes.js` |
| `index-inject` | 1 | `lib/index.js` |

## 4. 关键原文

```js
// lib/install.js:2
 * 一键安装：先出计划（plan），确认后执行。

// :135 —— 锁不到精确版本就跳过
report.skipped.push({ npm: item.npm, version: null, status: 'skipped', error: '锁定不到精确版本' })

// :161 —— 幂等
report.skipped.push({ npm: item.npm, version: item.version, status: 'skipped', error: '已安装，跳过' })

// :213 —— 一行账
return `已安装 ${report.installed.length} 个，已启用 ${report.enabled.length} 个，跳过 ${report.skipped.length} 个，失败 ${report.failed.length} 个`
```

```js
// lib/envcode.js:5-6 / :18-19 —— 两档编码
 *   DSHB1.<base64url(JSON)>        —— 明文表示，便于人眼排查
 *   DSHB1z.<base64url(deflateRaw(JSON))> —— 压缩表示，长清单时自动选用更短的那个
export const ENV_CODE_PREFIX = 'DSHB1.'
export const ENV_CODE_PREFIX_DEFLATE = 'DSHB1z.'

// :52-59 —— 摘要
export function digestOf(envelope) {
  return createHash('sha256').update(stableStringify(payload), 'utf8').digest('hex').slice(0, 16)
}
// :262-263 —— 校验结果
integrity = digestOf(envelope) === envelope.digest ? 'ok' : 'mismatch'
```

```js
// lib/index.js:99-103 —— 缺能力降级
if (!webServer || typeof webServer.register !== 'function') {
  logger.warn('[dsh-bootstrap] 拿不到 webServer，跳过 HTTP 路由')
  return
}
```

## 5. 为什么放 negative 而不是 samples

它满足本册的**第二道门（机制门）**：载体事实来自源码、可写"抄哪一行"。
它不满足**第一道门（影响力门）**：★1 / 763。

按 [`00-map`](../../00-map.md) §4.1，**不能为它破门**；于是用一张反例卡承载它的机制价值，同时在卡里写明门槛的代价。这是本册唯一一次"机制过门、影响力不过"的公开裁决。

## 6. 未复核

- 未实机安装。
- 它引用的插件目录数据是否已过期。
- 作者只发一版是弃坑还是本意。
- 若挂到已有用户动作上是否会有不同结果（册内无法验证）。
