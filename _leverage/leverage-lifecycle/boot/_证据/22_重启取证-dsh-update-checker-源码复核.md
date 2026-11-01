---
title: "证据 22 · update-checker 源码复核（1.7.3）"
domain: lifecycle
kind: evidence
positioning: "固定版本（无 gitHead）、tarball 摘要、三件重启证据的原始定位。"
read_when: "复核 boot/22；或想知道“重启成功”在源码里是怎么被证明的。"
status: observed
updated: 2026-11-01
budget: 115
---
# update-checker 源码复核

> **固定版本**：`dsh-update-checker@1.7.3`
> **gitHead**：**registry 未记录**（`npm view` 返回空）——本卡无法把 npm 物证与源码 commit 对齐，这是它比另外三张弱的地方
> **tarball**：`https://registry.npmjs.org/dsh-update-checker/-/dsh-update-checker-1.7.3.tgz`
> **sha256（前 24 位）**：`e37656481d6b496640900e40…` · **大小**：174,086 B · **文件数**：63
> **抽取位置**：`.work/mine/dsh-update-checker/package/`（`.work/` 已 gitignore）

## 1. 包清单事实 `[PKG]`

| 字段 | 值 |
|---|---|
| version | `1.7.3` |
| `dsh.bundle` | 有 |
| `dsh.client` | 有 |
| `bin` | 无 |
| `gitHead` | **无** |

## 2. 符号命中（S3）

```text
grep -rnoE 'tapIndex|index-inject|webServer\.register|commands\.register|agents\.create|
            workspaceRegistry|workingDirectory|installBundle|failOnStartupError|!!js'
```

| 符号 | 命中 | 位置 |
|---|---|---|
| `webServer.register` | 22 | 全在 `lib/index.js`（`:5376`、`:5409`、`:5424`、`:5443`、`:5459`、`:5617`、`:5879`…） |
| 其他载体符号 | 0 | — |

**说明**：单文件、路由密集。载体是 `web-route`，没有槽位、没有命令、没有 boot hook。

## 3. 三件证据的原文

```js
// lib/index.js:195
const RESTART_RESULT = join(DSH_HOME, "dsh-update-checker-restart-result.json");

// lib/index.js:211-213
const INSTANCE_ID = `${process.pid}-${Date.now().toString(36)}`;
const INSTANCE_STARTED_AT = Date.now();
```

```js
// lib/index.js:5827 —— 父亲把结果文件路径交给新进程
DSH_RESTART_RESULT: RESTART_RESULT,
```

```js
// lib/index.js:2209-2214 —— 起一个完全脱离的进程
spawn(plan.file, plan.args, {
  cwd: plan.cwd || deployRoot,
  windowsHide: false,
  detached: true,
  stdio: "ignore",
}).unref();
```

```js
// lib/index.js:5879-5886 —— 读取结果，读不到就是"还没重启过"
webServer.register({
  kind: "exact",
  path: "/dsh-update-checker/restart-status.json",
  handler: async (req, res) => {
    try {
      const raw = await readFile(RESTART_RESULT, "utf8");
      return json(res, 200, JSON.parse(stripBom(raw)));
    } catch {
      return json(res, 404, { ok: false, error: "no restart recorded yet" });
    }
  },
});
```

```js
// lib/index.js:5402 —— 状态端点带上实例身份
json(res, 200, { ...status, instanceId: INSTANCE_ID, startedAt: INSTANCE_STARTED_AT, mount: lastMountReport });
```

```js
// lib/index.js:1950 —— 端口探针
function probePortOpen(port, host = "127.0.0.1", timeoutMs = 1200) { ... }
```

## 4. 本卡与其它卡的呼应

- 与 [`BOOT`](../README.md) §2 的"应用内装给 restart-required、CLI 装没有"互补：**这里补的是重启之后怎么取证**。
- 端口探针单独用会误判，与 [`TRAPS`](../../practice/TRAPS.md) §6「装完不重启以为已生效」是同一族问题。

## 5. 未复核

- `DSH_RESTART_RESULT` 的消费点（谁读它、何时写、写什么 schema）未定位。
- 旧进程让出端口的方式（主动退出？等待窗口？）未定位。
- 三个探针的判组合逻辑未定位。
- **无 `gitHead`**：本卡的物证只能到 tarball 摘要，无法上溯 commit。
