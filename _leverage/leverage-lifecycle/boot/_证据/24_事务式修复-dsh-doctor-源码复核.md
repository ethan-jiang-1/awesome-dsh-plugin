---
title: "证据 24 · dsh-doctor 源码复核（0.4.3）"
domain: lifecycle
kind: evidence
positioning: "固定版本、tarball 摘要、检查点两级严格度与受保护集合的原始定位。"
read_when: "复核 boot/24；或想抄“修之前先备份、救生链不许碰”。"
status: observed
updated: 2026-11-01
budget: 95
---
# dsh-doctor 源码复核

> **固定版本**：`dsh-doctor@0.4.3`
> **gitHead**：`a13a5ab4a73806475acd2be638585937a9f15932`
> **tarball**：`https://registry.npmjs.org/dsh-doctor/-/dsh-doctor-0.4.3.tgz`
> **sha256（前 24 位）**：`c8b04c367459de744c5cff9b…` · **大小**：130,514 B · **文件数**：61
> **抽取位置**：`.work/mine/dsh-doctor/package/`

## 1. 包清单事实 `[PKG]`

| 字段 | 值 |
|---|---|
| version | `0.4.3` |
| `bin` | `dsh-doctor` → `lib/cli.js` |
| `dsh.bundle` | 有 |
| `dsh.client` | 有 |

## 2. 符号命中（S3）

九类载体符号**零命中**——它是独立 CLI，不改宿主行、不注册路由、不挂槽位。按 `CARRIERS` §3.1 兜底：以 `bin` 为准。

## 3. 关键原文

```js
// lib/cli.js:783 —— 检查点创建
async function createCheckpoint(dshHome, profile, kind, valid) { ... }
// :761 —— 检查点目录
function checkpointDirectory(dshHome, profile, id) { ... }
// :854 —— 回滚
async function rollbackCheckpoint(dshHome, checkpointId) { ... }
```

```js
// lib/cli.js:2270 —— 修复前：硬前置
const checkpoint = await createCheckpoint(stored.dshHome, profile, "pre-repair", false);
// lib/cli.js:2308 —— 验证通过后：尽力而为
if (verification.blocking === 0) await createCheckpoint(stored.dshHome, profile, "healthy", true).catch(() => {});
```

```js
// lib/cli.js:2032-2038 —— 受保护集合（Web 救生链）
const PROTECTED_IDS = new Set(["modules", "connection", "client-runtime", "ui-layout", "ui-sidebar", "ui-settings", ...]);
```

```js
// lib/cli.js:2193-2198 —— 命中受保护集合时降级为人工
kind: PROTECTED_IDS.has(target ?? "") ? "manual" : "disable-plugin",
title: PROTECTED_IDS.has(target ?? "") ? "Repair the failed core plugin manually" : "Disable the failed plugin",
description: ... `${target ?? "A required plugin"} is part of the Web rescue path and cannot be disabled safely.` ...
risk: PROTECTED_IDS.has(target ?? "") ? "manual" : "confirmation",
```

```js
// lib/cli.js:2417 / :2425 —— 兜底拒绝
if (PROTECTED_IDS.has(target)) throw new Error(`Doctor refuses to disable required plugin ${target}`);
if (PROTECTED_IDS.has(target)) throw new Error(`Doctor refuses to re-enable required plugin ${target}`);
```

```js
// lib/cli.js:3213-3214 —— 回滚命令
program.command("rollback").description("Restore every file from a Doctor checkpoint").argument("<checkpoint-id>")...
```

## 4. 未复核

- 检查点的保留与清理策略。
- 宿主完全起不来时 doctor 仍可运行的前提（未实测）。
- `verification.blocking` 的具体判定项。
- 未实机修复。
