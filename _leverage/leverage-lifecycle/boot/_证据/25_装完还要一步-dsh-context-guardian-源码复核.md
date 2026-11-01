---
title: "证据 25 · context-guardian 源码复核（0.3.0-beta.1）"
domain: lifecycle
kind: evidence
positioning: "固定版本、tarball 摘要、setup 的 dry-run 开关与三条命令注册的原始定位。"
read_when: "复核 boot/25；或想确认 input 陷阱的第二次独立复现。"
status: observed
updated: 2026-11-01
budget: 90
---
# context-guardian 源码复核

> **固定版本**：`dsh-context-guardian@0.3.0-beta.1`
> **gitHead**：`bfdfda22186f6be45d51d892cce1f4cc6fcdc730`
> **tarball**：`https://registry.npmjs.org/dsh-context-guardian/-/dsh-context-guardian-0.3.0-beta.1.tgz`
> **sha256（前 24 位）**：`8045814f62895bd8fbca9ec0…` · **大小**：266,648 B · **文件数**：35
> **抽取位置**：`.work/mine/dsh-context-guardian/package/`

## 1. 包清单事实 `[PKG]`

| 字段 | 值 |
|---|---|
| version | `0.3.0-beta.1` |
| `dsh.bundle` | 有 |
| `dsh.client` | **无** |
| `bin` | **无**（生效入口是 `scripts.setup: node setup.mjs`） |

## 2. 符号命中（S3）

| 符号 | 命中 | 位置 |
|---|---|---|
| `commands.register` | 3 | `engine.js:1362`（`recall`）、`:1381`（`guardian`）、`:1386`（`context`） |
| 其他 | 0 | — |

## 3. 关键原文

```js
// setup.mjs:363
if (arg === '--apply') { flags.apply = true; continue }
// setup.mjs:610
say('dry run -- nothing written; re-run with --apply')
```

```js
// engine.js:1362-1370 —— recall 带 input
inner.commands.register({
  name: 'recall',
  description: 'Show original history: /recall 3-7 · …',
  // Without `input` DSH treats a command as argument-free: the web UI runs it bare on
  // select and sends "/recall result 42" typed in full to the MODEL (seen live 2026-09-20).
  input: { hint: '<3-7 | result 3 | checkpoint 1 | find text | digest>' },
  handler: …,
})
```

```js
// engine.js:1381-1392 —— guardian / context 不带 input（无参命令，正确用法）
commands.register({ name: 'guardian', description: 'Context Guardian status: …', handler: … })
commands.register({ name: 'context', description: 'Context pressure, cache hits and what compacting now would cost', handler: … })
```

```json
// package.json scripts
"setup": "node setup.mjs",
"selftest": "python modules/cg_bridge.py --selftest"
```

## 4. 交叉验证

**宿主侧复核** `[DSH]`：`dsh-client-ui-commands/lib/client.js:1661-1665`——有 `input` 才返回 claim；没有 `input` 且带参数时 `return void 0`，该行不再走命令通道。这条把本卡的 `[DOC]` 推论升级为宿主事实。

`input` 陷阱在本册出现两次，且互相独立：

| 样本 | 位置 | 证据强度 |
|---|---|---|
| `dsh-tool-guardian@0.9.1-beta.1` | `index.js:1134-1135` 注释 | `[DOC]` |
| `dsh-context-guardian@0.3.0-beta.1` | `engine.js:1365-1366` 注释，含**实机观察日期 2026-09-20** | `[DOC]` + 观察记录 |

两处都独立指向同一条宿主行为，可信度高于单点注释。

## 5. 未复核

- `setup.mjs` 写入 preset 的确切位置与幂等性。
- `setup.mjs` 随包发布（`files` 含它），但用户要先找到包目录；等价入口是否存在，按"包目录里 `npm run setup`"复核。
- 无数据时三条命令的表现。
- 未实机 setup。
