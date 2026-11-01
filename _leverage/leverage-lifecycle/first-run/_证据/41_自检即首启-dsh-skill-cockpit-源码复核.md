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

同文件另有两项文档门：平台套件数一致（`:31-39`）、公开文档不含本机绝对路径（`:52-60`）。

**状态与退出码** `[SRC-TARGET]`：状态共六个——`ok` / `skip` / `wanted` / `bad` / `warn` / `fixed`（`fixed` 只在 `--fix` 成功创建后出现，`:136`）；退出码只有三档——`bad` 集合算 `bad`/`warn`/`wanted`（`:242`），所以 `fixed` 不改变退出码；`2` 只用于“起始读不了 home”（`:55-59`）或“报告写出失败”（`:263-267`）。

**文档对账的盲区** `[SRC-TARGET]`：`ids` 正则只认单引号、小写开头的 `add('id')`（`:44`），文档表只认首列反引号 id（`:46`）；写成双引号/模板串/大写开头的新检查不会被对账，测试仍绿。

**`--fix` 的写入范围** `[SRC-TARGET]`：只建状态目录（`:117`）与 user-dsh 技能根（`:135`），失败时把该条标 `bad` 而不是抛出；没有通用回滚，因为它只做 `mkdir`。

## 4. 已核 / 未复核

- **已核**：`--fix` 只做状态目录与技能根的创建，失败标 `bad`；`fixed` 不参与退出码；退出码 2 只来自起始 home 不可读或报告写出失败。
- **已核**：文档对账只覆盖单引号小写 id + 反引号首列，存在格式盲区。
- `[OPEN]` `test/run-docs.mjs` 是否真的在 CI 里跑（只看到测试文件）。
- 面板在侧栏的位置是否只由 slot `order` 决定。
- doctor 未实机运行。
