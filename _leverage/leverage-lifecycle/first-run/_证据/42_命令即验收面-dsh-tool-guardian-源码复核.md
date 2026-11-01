---
title: "证据 42 · tool-guardian 源码复核（0.9.1-beta.1）"
domain: lifecycle
kind: evidence
positioning: "固定版本、tarball 摘要、命令注册与自检返回形态的原始定位。"
read_when: "复核 first-run/42；或想知道 input 字段到底改了什么行为。"
status: observed
updated: 2026-11-01
budget: 90
---
# tool-guardian 源码复核

> **固定版本**：`dsh-tool-guardian@0.9.1-beta.1`
> **gitHead**：`ec61be43f7d8e950d4a9a342ccf06ca02c8297c9`
> **tarball**：`https://registry.npmjs.org/dsh-tool-guardian/-/dsh-tool-guardian-0.9.1-beta.1.tgz`
> **sha256（前 24 位）**：`0b7f29875106e0ab82e2eb19…` · **大小**：189,410 B · **文件数**：27
> **抽取位置**：`.work/mine/dsh-tool-guardian/package/`

## 1. 包清单事实 `[PKG]`

| 字段 | 值 |
|---|---|
| version | `0.9.1-beta.1`（**预发布**，选它是因为它是唯一命令式自检样本） |
| `dsh.bundle` | 有 |
| `dsh.client` | **无**（所以没有浏览器卡片） |
| `bin` | 无 |

## 2. 符号命中（S3）

| 符号 | 命中 | 位置 |
|---|---|---|
| `commands.register` | 2 | `index.js:1131`（注册）、注释 `:29-30` |
| 其他 | 0 | — |

## 3. 关键原文

```js
// index.js:1127-1138
// Optional like settings: a host without the command registry still gets the tools.
ctx.inject(['commands'], (inner) => {
  inner.commands.register({
    name: 'toolguardian',
    description: 'Tool Guardian: selftest (backends, token saving, update) · bypass [last|24h] · restore',
    // Without `input` DSH treats a command as argument-free and sends "/toolguardian bypass" to the MODEL.
    input: { hint: '[selftest | bypass | bypass last | restore]' },
    handler: toolguardianCommand,
  })
})
// Registrations are effects: unloading or hot-replacing the plugin unregisters
```

```js
// index.js:1045 —— 用法
const USAGE = 'usage: /toolguardian [selftest] | /toolguardian bypass [last | 24h] | /toolguardian restore'
```

```js
// index.js:1050-1053 —— 未就绪的两种状态
if (live === null || !ready) {
  const why = bootError === '' ? 'still starting -- try again in a few seconds' : `failed to start: ${bootError}`
  return { kind: 'error', text: `tool-guardian ${PKG_VERSION}: ${why}.\nThe DSH log has the detail (search "tool-guardian").` }
}
```

```js
// index.js:1103 / :1107 / :1120 — 返回形态
return { kind: 'success', text: lines.join('\n') }
return { kind: 'error', text: 'tool-guardian is not ready yet -- /toolguardian shows why.' }
if (!resolveOptions(source()).allowRuntimeActivation) return { kind: 'error', text: 'restore needs allowRuntimeActivation: true.' }
```

## 4. 未复核

- `bypass 24h` 的到期与持久化实现。
- `allowRuntimeActivation` 的默认值。
- 命令未注册时的用户告知路径。
- 未实机运行（本机不装）。
