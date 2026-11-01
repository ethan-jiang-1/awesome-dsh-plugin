---
title: "证据 41 · skill-cockpit 源码复核（1.5.1）"
domain: lifecycle
kind: evidence
positioning: "固定版本、tarball 摘要、doctor 退出码与文档同步测试的原始定位。"
read_when: "复核 first-run/41；或想抄“检查项与文档对账”那条测试。"
status: observed
updated: 2026-11-01
budget: 95
---
# skill-cockpit 源码复核

> **固定版本**：`dsh-skill-cockpit@1.5.1`
> **gitHead**：`77f527635495632aaa3c717b8dd4015dfe18d46f`
> **tarball**：`https://registry.npmjs.org/dsh-skill-cockpit/-/dsh-skill-cockpit-1.5.1.tgz`
> **sha256（前 24 位）**：`ed3ca5d6bae5dc04986d888f…` · **大小**：352,792 B · **文件数**：65
> **抽取位置**：`.work/mine/dsh-skill-cockpit/package/`

## 1. 包清单事实 `[PKG]`

| 字段 | 值 |
|---|---|
| version | `1.5.1` |
| `dsh.bundle` | 有 |
| `dsh.client` | 有（`platform: web`，inject `@deepseek-ai/dsh-client-runtime`） |
| `bin` | `dsh-skill-cockpit-doctor` → `bin/cockpit-doctor.mjs` |
| `manifestVersion` | 1 |

## 2. 符号命中（S3）

```text
grep -rnoE 'tapIndex|index-inject|webServer\.register|commands\.register|agents\.create|
            workspaceRegistry|workingDirectory|installBundle|failOnStartupError|!!js'
```

**零命中。** 与本册 `config/31` 同类：它的生命周期价值在 **bin + 客户端 bundle**，不在 host 侧符号。按 `CARRIERS` §3.1 的兜底规则，以包清单（`bin`）与 patch 声明为准。

## 3. 关键原文

```js
// bin/cockpit-doctor.mjs:12
 * 退出码：0 = 一切就绪 / 1 = 需要修（--fix 能补的） / 2 = 环境问题（读不了 home 等）
```

```js
// bin/cockpit-doctor.mjs:38-40 / :45
const asJson = flag('--json')
const doFix = flag('--fix')
const dryRun = flag('--dry-run')
const add = (id, label, status, detail) => checks.push({ id, label, status, detail: detail ?? null })
```

```js
// bin/cockpit-doctor.mjs:114-121（dry-run 与 fix 的分支）
if (dryRun) {
  add('state', '状态目录可写', existsSync(stateDir) ? 'ok' : 'wanted', stateDir)
}
```

```js
// bin/cockpit-doctor.mjs:281 —— 成功输出里写明“去哪儿看”
? (dryRun ? '一切就绪（dry-run 未落盘）。' : '一切就绪。面板没出现的话：重启 DSH，再确认左侧导航「插件」与「自动化任务」之间。')
```

```js
// test/run-docs.mjs:42-49 —— 检查项与排障文档对账
const ids = [...new Set([...doctor.matchAll(/add\(\s*'([a-z][a-z0-9-]*)'/g)].map((m) => m[1]))].sort()
const table = read('docs/troubleshooting.md')
const documented = new Set([...table.matchAll(/^\|\s*`([a-z][a-z0-9-]*)`\s*\|/gm)].map((m) => m[1]))
const missing = ids.filter((id) => !documented.has(id))
check('每个 doctor 检查项都在 troubleshooting 表里', missing.length === 0, missing.join(', '))
```

同文件另有两项文档门：平台套件数一致（`:31-39`）、公开文档不含本机绝对路径（`:51+`）。

## 4. 未复核

- `--fix` 的写入范围与失败回滚。
- `test/run-docs.mjs` 是否真的在 CI 里跑（只看到测试文件）。
- 面板在侧栏的位置是否只由 slot `order` 决定。
- doctor 未实机运行。
