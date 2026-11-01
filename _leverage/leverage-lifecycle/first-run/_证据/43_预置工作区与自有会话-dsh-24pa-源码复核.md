---
title: "证据 43 · 24pa 源码复核（0.2.1-rc.5.1）"
domain: lifecycle
kind: evidence
positioning: "固定版本（无 gitHead）、tarball 摘要、预置工作区与会话冲突分支的原始定位。"
read_when: "复核 first-run/43；或想抄“冲突换 id 不覆盖”的做法。"
status: observed
updated: 2026-11-01
budget: 95
---
# 24pa 源码复核

> **固定版本**：`@benz-ai-x/dsh-24pa@0.2.1-rc.5.1`
> **gitHead**：**registry 未记录**
> **tarball**：`https://registry.npmjs.org/@benz-ai-x/dsh-24pa/-/dsh-24pa-0.2.1-rc.5.1.tgz`
> **sha256（前 24 位）**：`e28d5a022bdcbe9224ee0d45…` · **大小**：632,497 B · **文件数**：140
> **抽取位置**：`.work/mine/_benz-ai-x_dsh-24pa/package/`

## 1. 包清单事实 `[PKG]`

| 字段 | 值 |
|---|---|
| version | `0.2.1-rc.5.1`（版本号里嵌了宿主基线 `0.2.1`） |
| `dsh.bundle` | 有 |
| `dsh.client` | 有（`platform: web`） |
| `bin` | 无 |
| `gitHead` | **无** |

## 2. 符号命中（S3）

| 符号 | 命中 | 位置 |
|---|---|---|
| `!!js` | 7 | `cordis.patch.yml:43`、`:46`（平台门控）、`:167-171`（路径与覆盖） |
| `workspaceRegistry` | 2 | `lib/runtime.js:1248`（create）、`:4471`（list） |
| 其他 | 0 | — |

**注意**：会话创建走的是 `ctx.sessionController.create(...)`（`:1588`），**不是** `agents.create`——本卡写作时据此修正了初判。

## 3. 关键原文

```js
// lib/runtime.js:1246-1257
const saved = await repos.workspaceState.get(real);
next = {
  workspace: { ...await this.ctx.workspaceRegistry.create(real, '24私助'), statePath: real },
  accessSessionId: saved?.feishu_session_id ?? `pa24-${hash(real).slice(0, 12)}-feishu`,
  localSessionId:  saved?.local_session_id  ?? `pa24-${hash(real).slice(0, 12)}-local`,
};
next.accessSessionId = await this.prepareOwnedSession('feishu', next);
next.localSessionId  = await this.prepareOwnedSession('local', next);
await repos.workspaceState.save(real, { feishuSessionId: next.accessSessionId, localSessionId: next.localSessionId });
```

```js
// lib/runtime.js:1586-1598
async prepareOwnedSession(kind, target) {
  const key = kind === 'feishu' ? 'accessSessionId' : 'localSessionId';
  const create = () => this.ctx.sessionController.create({ sessionId: target[key], workspaceId: target.workspace.id, agentPreset: 'pa24' });
  try { await create(); }
  catch (error) {
    if (error.code !== 'agent-preset/conflict') throw error;
    const previous = target[key];
    target[key] = `pa24-${hash(target.workspace.statePath).slice(0, 12)}-${kind}-${randomUUID().slice(0, 8)}`;
    await create();
    target.sessionNotices.push({ dedupKey: `notice:session-rebound:${target[key]}`, text: `旧会话 ${previous} 已选择其他预设，历史保留；…` });
  }
}
```

```js
// lib/runtime.js:4471
availableWorkspaces: this.ctx.workspaceRegistry.list().map(w => ({ id: w.id, title: w.title, path: w.path })),
```

```yaml
# cordis.patch.yml
:43   disabled: !!js process.platform === 'win32'
:46   disabled: !!js process.platform !== 'win32'
:167  stateDirectory: !!js dshHomePath('24pa')
:171  workspacePath: !!js process.env.PA24_WORKSPACE || ''
```

## 4. 写作时的修正

- 初判：以为它用 `agents.create` 预置会话（依据是 `agents` 服务契约）。
- 实读：用的是 **`sessionController.create({ sessionId, workspaceId, agentPreset })`**，走会话控制器而不是 agent 工厂。
- 这属于本册 `[SRC-TARGET]` 的常规纠错：**服务契约能做什么 ≠ 这个包实际用了什么**。

## 5. 未复核

- `workspaceRegistry.create` 对已存在路径的行为。
- 除 `agent-preset/conflict` 外的冲突码。
- `sessionNotices` 的呈现路径。
- **无 `gitHead`**，物证止于 tarball 摘要。
- 未实机启动。
