---
title: "15 · Garybot126/dsh-subagent-models 源码复核"
domain: agent-delegation
kind: evidence
positioning: "0.1.2 固定复核：用 agent/request 覆盖被委派子代理的 provider/model/effort；查优先级、校验与持久化偏差。"
read_when: "要引用“子代理模型统一设置”的机制，或核对它的优先级/校验是否符合 README 时。"
status: observed
updated: 2026-11-01
---
# 15 · `dsh-subagent-models` 源码复核

> 复核对象：[`samples/15-Garybot126-dsh-subagent-models.md`](../samples/15-Garybot126-dsh-subagent-models.md)。只读 GitHub raw / npm registry；**未安装、未构建、未运行**，未启动 DSH。`[RUN]` 仅 registry/API 读取。

## Provenance

| 项 | 值 | 核对方式 |
|---|---|---|
| 仓库 | `Garybot126/dsh-subagent-models`（MIT，默认分支 `main`，1★ @2026-11-01） | GitHub REST |
| npm | `dsh-subagent-models@0.1.2`（latest）；`gitHead = a10585581d4bac1df0b86227637e7258c0da0b8a` | registry |
| tag | **无 tag**（`/tags` 为空） | GitHub REST |
| 审计 pin | commit `a105855…`（npm gitHead） | raw 文件按 SHA 取 |
| 包形态 | 无 `main`/`files`；入口 `index.js`；`dsh.bundle.patch` → `cordis.patch.yml`；`dsh.client`（web） | package.json |
| 依赖 | 无 `dependencies`/`peerDependencies`；`engines.dsh >=0.2.1-rc.2` | package.json |
| 发布 | npm tarball 未下载比对；`index.js`/`client.js` 直接发布 | `[OPEN]` 字节一致性 |

## DOC（README 主张）

- 一个入口（输入框旁 chip）+ 两个范围（本对话/全局默认），设置 provider/model/reasoning effort。
- 生效于下一次委派；运行中的子代理在下一次模型请求生效；无路由时继承父会话。
- 优先级写为：本对话 override → 全局默认 → 无路由。
- 数据文件 `$DSH_HOME/plugin-data/subagent-models.json`，mtime 热加载。
- 局限：`subagent_fork` 也被覆盖，换模型会丢 KV cache；不支持的 effort 会让 adapter 校验失败，不静默降级。

## SRC-TARGET（`a105855`）

### 1. 接缝：`agent/request` waterfall，只改被委派 child

- `ctx.on('agent/request', async (payload, next) => { const config = await next(); const route = await routeFor(payload?.agent); ... return {...config, ...overridden} })`（[`index.js:247-255`](https://github.com/Garybot126/dsh-subagent-models/blob/a10585581d4bac1df0b86227637e7258c0da0b8a/index.js#L247-L255)）。
- `routeFor` 先用 `ownersOf(agent)` 找“拥有该 child 的活 Agent”；`owners.length===0` 直接返回 null——**顶层会话永不被改**（[:207-245](https://github.com/Garybot126/dsh-subagent-models/blob/a10585581d4bac1df0b86227637e7258c0da0b8a/index.js#L207-L245)）。
- `ownersOf` 先 `agents.roots()` 再 `agents.list()`，用 `agents.isOwnedBy` 过滤；注释说 conversation root 优先。

### 2. 优先级与 README 不一致

- 实际解析：对每个 owner，读 `state.sessions[owner.id].default`；命中即返回；否则 `state.global.default`（[:233-245](https://github.com/Garybot126/dsh-subagent-models/blob/a10585581d4bac1df0b86227637e7258c0da0b8a/index.js#L233-L245)）。
- state 里保存了 `presets`，但 `routeFor` **从不读 presets**；README/注释里的 `S.presets[P] -> global.presets[P]` 路径未实现（[:58-70](https://github.com/Garybot126/dsh-subagent-models/blob/a10585581d4bac1df0b86227637e7258c0da0b8a/index.js#L58-L70)）。
- 未配置 route 时返回 null，child 保留 composition 的 `agentOptions`。

### 3. “模型仍被广告才生效”未实现

- `routeApplies` 注释写“wins only when its model is still advertised by a mounted provider”（[:85-92](https://github.com/Garybot126/dsh-subagent-models/blob/a10585581d4bac1df0b86227637e7258c0da0b8a/index.js#L85-L92)），但函数只拼 `{provider,model,reasoningEffort}`，**无 catalog/校验**；目录只用于 UI。
- 无 effort 时显式写 `reasoningEffort: undefined`（[:252-253](https://github.com/Garybot126/dsh-subagent-models/blob/a10585581d4bac1df0b86227637e7258c0da0b8a/index.js#L252-L253)），可能清掉 preset 原有 effort；README 未提。

### 4. 状态与写入

- 文件 `$DSH_HOME/plugin-data/subagent-models.json`，mtime 缓存；读坏/缺文件回默认空 state（[:95-118](https://github.com/Garybot126/dsh-subagent-models/blob/a10585581d4bac1df0b86227637e7258c0da0b8a/index.js#L95-L118)）。
- 写：串行 promise 链 + tmp 文件 + rename；失败只 `logger.warn`，**内存 cache 已先更新**（[:120-138](https://github.com/Garybot126/dsh-subagent-models/blob/a10585581d4bac1df0b86227637e7258c0da0b8a/index.js#L120-L138)）。
- `mutate` 只写 `sessions[sessionId].default` 或 `global.default`，`presets` 恒为空（[:140-157](https://github.com/Garybot126/dsh-subagent-models/blob/a10585581d4bac1df0b86227637e7258c0da0b8a/index.js#L140-L157)）；会话条目无淘汰。

### 5. HTTP 面

- 单前缀 `/plugin/subagent-models`，GET `state` / POST `route` / POST `hello`；body 上限 1MB（[:272-311](https://github.com/Garybot126/dsh-subagent-models/blob/a10585581d4bac1df0b86227637e7258c0da0b8a/index.js#L272-L311)）。
- `hello` 把 client 上报写 `subagent-models.client.json`（[:299-309](https://github.com/Garybot126/dsh-subagent-models/blob/a10585581d4bac1df0b86227637e7258c0da0b8a/index.js#L299-L309)）。
- 通过 `ctx.inject(['webServer'])` + `scope.webServer.register({kind:'prefix'})` 挂载（[:315-318](https://github.com/Garybot126/dsh-subagent-models/blob/a10585581d4bac1df0b86227637e7258c0da0b8a/index.js#L315-L318)）；**handler 内无鉴权**，依赖宿主对 `/plugin/*` 的防线——未核，标 `[OPEN]`。

## SRC-DSH（0.2.1-rc.3）

- `agent/request` 是 waterfall，可替换 frozen call config；不能修改消息（`dsh-agent/lib/types/runtime-types.d.ts:317-330`）。
- `agents.isOwnedBy(childId, ownerId)` 用于判断委派归属；未逐行核运行时语义。
- `ctx.llm.listProviders/listModels/resolveModelInfo` 用于目录与 effort 枚举。

## TEST / CI / RUN

- 仓库无测试、无 `.github/`、无 CI（`[TEST] None`、`[CI] None`）。
- `[RUN] None`：未安装、未运行、未执行 HTTP 路由。

## 与卡片的偏差

| 主张 | 实际 | 处置 |
|---|---|---|
| README 的 preset 优先级 | 未实现 presets 读取 | 卡片写“本对话→全局→继承”，不写 preset 层 |
| “模型仍被广告才生效” | 仅注释，未校验 | 标 `[OPEN]`；写“目录只用于 UI” |
| 无 effort 时保持 preset | 显式写 undefined | 卡片补“可能清空 preset effort” |
| 写失败可见性 | 内存先更新，仅 warn | 卡片写“UI 可能显示未持久化状态” |
| 无鉴权 | handler 无 token，依赖宿主 | 标 `[OPEN]`，不写“安全” |

## `[OPEN]`

- `/plugin/*` 前缀是否被宿主做连接级鉴权/回环限制。
- npm tarball 与 commit 字节一致性（无构建，风险低但未比对）。
- 真实 child 上 effort 不被支持时的 adapter 错误形态。
- `subagent_fork` 覆盖后 KV cache 的实际影响。
