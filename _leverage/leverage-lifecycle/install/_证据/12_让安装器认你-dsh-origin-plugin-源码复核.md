---
title: "证据 12 · origin-plugin 源码复核（2.7.3）"
domain: lifecycle
kind: evidence
positioning: "固定版本、tarball 摘要、自挂载行与 apply 返回值的原始定位，用于复核两个隐形判定。"
read_when: "复核 install/12；或想知道“市场认不认我”到底查了什么。"
status: observed
updated: 2026-11-01
budget: 135
---
# origin-plugin 源码复核

> **固定版本**：`dsh-origin-plugin@2.7.3`
> **gitHead**：`4010683f252380a644a6da9a08963690530a87cd`
> **tarball**：`https://registry.npmjs.org/dsh-origin-plugin/-/dsh-origin-plugin-2.7.3.tgz`
> **sha256（前 24 位）**：`8312f0f853c2773c67c8955b…` · **大小**：1,283,990 B · **文件数**：117
> **抽取位置**：`.work/mine/dsh-origin-plugin/package/`（`.work/` 已 gitignore）

## 1. 包清单事实 `[PKG]`

| 字段 | 值 |
|---|---|
| version | `2.7.3` |
| `main` | `./index.js`（`package.json:7`） |
| `bin` | `dsh-origin-mcp` → `./bin/dsh-origin-mcp.mjs`（`package.json:8-9`） |
| `dsh.bundle` | 有（`./cordis.patch.yml`） |
| `dsh.client` | **无** |
| `files` | 含 `index.js`、`bin/`、`cordis.patch.yml`、`scripts`、`.py` 全量 |

## 2. 符号命中（S3）

```text
grep -rnoE 'tapIndex|index-inject|webServer\.register|commands\.register|agents\.create|
            workspaceRegistry|workingDirectory|installBundle|failOnStartupError|!!js'
```

| 符号 | 命中 | 位置 |
|---|---|---|
| `failOnStartupError` | 3 | `cordis.patch.yml:14`（注释）、`:52`（覆盖示例注释）、`:76`（实际行） |
| `!!js` | 3 | `cordis.patch.yml:9`（注释）、`:71`、`:72`（实际表达式） |
| 其他载体符号 | 0 | — |

**说明**：没有 `webServer.register` / `commands.register` / `agents.create` 命中。载体是纯 `host-row`，唯一入口是 `mcp-origin` 这条 insert。

## 3. 关键原文

```yaml
# cordis.patch.yml:61-76
- id: mcp-origin
  name: '@deepseek-ai/dsh-mcp-client'
  config:
    transport: stdio
    command: python
    args: ['-u', '-X', utf8,
      !!js (process.env.DSH_HOME || (String(process.env.USERPROFILE) + '/.dsh')) + '/profiles/web/node_modules/dsh-origin-plugin/origin_mcp_server.py']   # :71
    cwd: !!js (process.env.DSH_HOME || ...) + '/profiles/web/node_modules/dsh-origin-plugin'                                                              # :72
    failOnStartupError: false                                                                                                                             # :76
```

```yaml
# cordis.patch.yml:78-85 —— 自挂载
# Self-mount: a no-op fiber so the plugin market reads this bundle as
# "live/active" (verify.js liveIncludes checks for the package name in the
# loader entry-name set). Without this row the only entry name is
# @deepseek-ai/dsh-mcp-client, so liveIncludes('dsh-origin-plugin')=false
# and the market perpetually shows "restart to apply" even after restart.
- id: dsh-origin-plugin
  name: dsh-origin-plugin
```

```js
// index.js:60-81
export default {
  ...plugin,
  apply(ctx) {
    if (ctx && typeof ctx.effect === 'function') {
      ctx.effect(() => { /* 通知 Python 引擎优雅退出，失败不抛 */ })   // :63-75
    }
    return void 0                                                    // :80
  },
}
```

## 4. 两条隐形判定的原始依据

| 判定 | 原文位置 | 性质 |
|---|---|---|
| 入口工件（`entryArtifactExists`） | `index.js:6-13` 注释：*a carrier bundle … is indistinguishable from a checkout that still needs a build step, so it gets rejected with "nothing installable"* | `[DOC]`；市场侧已核实其真实形状见 §5 |
| loader 活性（`loaderLive`） | `index.js:49-53` 注释引 `verify.js L149`（live）与 `L162`（restart） | `[DOC]`；1.73.6 的 `verify.js` 仍有 `liveIncludes`，但已加 `carriedRowLive`（§5） |
| `apply` 返回值 | `index.js:76-79` 注释：返回对象 → `TypeError: Invalid effect` → 启动崩溃（issue #1，DSH ≥0.1.5） | `[DOC]`，但 `return void 0` 是 `[SRC-TARGET]` 的实际代码 |

## 5. 市场侧对照（`dshmarket@1.73.6`）

> 来源：`https://registry.npmjs.org/dshmarket/-/dshmarket-1.73.6.tgz` · sha256 `8790a060ba728e32a355ec40ec4228d12e46195a343e984dbcfcd7bc61909ddd` · 860 KB · 122 文件。

| 事实 | 位置 | 说明了什么 |
|---|---|---|
| 七态：`live` / `restart` / `incompatible` / `inert` / `broken` / `missing` / `disabled` | `lib/verify.js:17-28` | “装上了”不是布尔值；市场按可观测性分级 |
| 证据优先级：loader inventory（观察）> profile manifest（推断）> profile patch（补充） | `lib/verify.js:1-16`、`:150-163` | manifest 不能推翻运行中的观察 |
| `liveIncludes(live, name)`：匹配 loader 条目名，允许 subpath，要求 `/` 边界 | `lib/verify.js:91-105` | 旧市场只按条目名判活 |
| `carriedRowLive(live, profileDir, name)`：用包自己 patch 插入的 entry id（`#id`）判活 | `lib/verify.js:108-128`、`:400` | **#156：carrier bundle 不再需要自挂载空行** |
| `entryArtifactExists`：`main` / `exports`（字符串、`.`、对象值）/ 回退 `index.js` | `lib/profile.js:850-869` | “入口工件”是可枚举形状，不是“有 lib” |
| `hasLoadableEntry`：carrier 的目标可加载即可，含宿主安装树（#906） | `lib/profile.js:1396-1432` | 纯 patch 的 carrier 合法 |
| install 校验判 `broken` → `removedBroken` → `removeAndReconcile` | `lib/install.js:855-870` | 市场会卸载“刚装好”的包，退出码 0 |

**结论**：作者的两条判定在 1.73.6 仍成立一半——入口仍是硬检查（但口径不同），活性已由 `carriedRowLive` 兜住。照抄“必须加自挂载行”会多一条无功能行；照抄“只写 patch 就行”会在挂载目标不可加载时被市场卸载。

## 5.5 E28：真装后调用市场判定器

隔离 `DSH_HOME=.work/deep/home`，`dsh plugin --profile exp add <abs>/pkg.tgz`（exit 0）后：

| live 集合 | `verifyActivation` 结果 |
|---|---|
| `∅` | `restart` |
| `#mcp-origin` | `live` |
| `dsh-origin-plugin` | `live` |
| `@deepseek-ai/dsh-mcp-client` | `restart` |

手造 fake carrier（`dsh.bundle` + 空 patch + 无入口）：`entryArtifactExists=false`、`hasLoadableEntry=false`、`verifyActivation → broken`。

复现注意：市场包解包后需给 `js-yaml` / `undici` 建 `node_modules` 链接（本机从 DSH 安装树借用），否则 `profile.js` 直接 `ERR_MODULE_NOT_FOUND`。

## 6. 未复核

- **已关（版本下限）**：逐版本抽 `lib/verify.js` / `lib/profile.js` / `lib/install.js`：`hasLoadableEntry` 首见 `dshmarket@1.10.0`（2026-08-16；该版 `install.js` 已 3 处调用），`1.9.0` 无；`carriedRowLive` 首见 `@1.11.3`（2026-08-17），`1.11.2` 无。对照 tarball：1.10.0 sha256 `a8f45466adbdbd408f9283c4…`（444K）；1.11.3 `cb07f8d08b8373c91c67e33c…`（580K）。
- Python 侧同步 stdio 循环（`origin_mcp_server.py` 的 `_sync_stdio_server()`）是否真的消除 60s 挂起。
- `profiles/web` 硬编码在 `desktop` profile 下的行为。
- 未实机安装/启动。
