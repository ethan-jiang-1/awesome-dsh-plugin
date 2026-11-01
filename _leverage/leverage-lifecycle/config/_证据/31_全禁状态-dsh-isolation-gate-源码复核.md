---
title: "证据 31 · isolation-gate 源码复核（1.13.7）"
domain: lifecycle
kind: evidence
positioning: "固定版本、tarball 摘要、状态读取五分支与判定开关的原始定位。"
read_when: "复核 config/31；或想知道 fail-closed 具体写在哪几行。"
status: observed
updated: 2026-11-01
budget: 95
---
# isolation-gate 源码复核

> **固定版本**：`dsh-isolation-gate@1.13.7`
> **gitHead**：`70b4b6fbaf7e9b80fec9b284c1e2544090b8c191`
> **tarball**：`https://registry.npmjs.org/dsh-isolation-gate/-/dsh-isolation-gate-1.13.7.tgz`
> **sha256（前 24 位）**：`119832a283b0a80bd14d11ca…` · **大小**：120,862 B · **文件数**：30
> **抽取位置**：`.work/mine/dsh-isolation-gate/package/`

## 1. 包清单事实 `[PKG]`

| 字段 | 值 |
|---|---|
| version | `1.13.7` |
| `dsh.bundle` | 有 |
| `dsh.client` | 有（`platform: web`，inject 1 个：`@deepseek-ai/dsh-client-runtime`） |
| `bin` | **6 个**：`gate`、`gate-hook-claude`、`gate-hook-gemini`、`gate-mcp`、`gate-hook-generic`、`gate-ui` |
| peer 依赖 | **无 `@deepseek-ai/dsh*`** |

## 2. 符号命中（S3）

```text
grep -rnoE 'tapIndex|index-inject|webServer\.register|commands\.register|agents\.create|
            workspaceRegistry|workingDirectory|installBundle|failOnStartupError|!!js'
```

**零命中。** 它的机制不在符号表里——判定与读写都走自建 HTTP 路由（`/__dsh-isolation-gate/*`，在 `lib/index.js` 里用字面量拼出来，未命中 `webServer.register` 的正则形态）。这是本册第一次遇到"符号表失效"，说明 `CARRIERS` 的判定规则需要一条兜底：**路由可用字符串常量 + 自建 handler 注册，grep 不到时以 patch 声明的路由清单为准**。

## 3. 关键原文

```js
// lib/store.js:62 —— 默认值
export const DEFAULT_LEVEL = 'deny';

// lib/store.js:69 —— 写进状态文件的自述行
'未在本文件列出的键一律按 deny；本文件缺省也不代表授权，恰恰等于全禁。';

// lib/store.js:76 —— 空状态
/** 空状态：全禁。 */
export function emptyState(now) { ... }
```

```js
// lib/store.js:270-309 —— 五分支读取
export function readState(filePath) {
  if (typeof filePath !== 'string' || filePath.trim() === '')
    return { ok: false, exists: false, state: emptyState(), error: '未配置状态文件路径（按全禁处理）' };
  if (!existsSync(filePath))
    return { ok: true, exists: false, state: emptyState(), error: null };
  try { text = readFileSync(filePath, 'utf8'); }
  catch (error) { return { ok: false, exists: true, state: emptyState(), error: `状态文件读取失败：…` }; }
  if (text.charCodeAt(0) === 0xfeff) text = text.slice(1);            // BOM
  if (text.trim() === '') return { ok: true, exists: true, state: emptyState(), error: null };
  try { ... return { ok: true, exists: true, state, ... }; }
  catch (error) {
    return { ok: false, exists: true, state: emptyState(),
             error: `状态文件不是合法 JSON（按全禁处理，且不覆盖它）：…` };
  }
}
```

```js
// lib/service.js:221-224 —— 判定侧压成一个开关 + 一句原因
// ⚠️ fail-closed 生效中：名单不可用 ⇒ 通道对一切受管对象一律拒绝。
gateClosed: rosterRead.ok === false,
rosterGateMessage: rosterRead.ok ? null : `名单不可用（…）⇒ 按"一律拒绝"处理，请先恢复名单文件`,
```

## 4. 写作时的修正

- 起初以为它只是"配置插件"；实际带 **6 个 bin**，说明它把同一套判定卖给了多个宿主（Claude / Gemini / generic / MCP / UI）。
- `CARRIERS` §3 的符号表对它是**失效**的，已在卡内标注并给出兜底规则。

## 5. 未复核

- `normalizeState` 的逐版本迁移语义。
- 六个 bin 与宿主半的职责划分。
- "无 peer 依赖 ⇒ 绕开安装期兼容闸门"的实际后果。
- 门禁行为未实机演练。
