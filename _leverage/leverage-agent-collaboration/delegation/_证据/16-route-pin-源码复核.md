---
title: "16 · tkaiz0406/dsh-subagent-route-pin 源码复核"
domain: agent-delegation
kind: evidence
positioning: "0.8.22 固定复核：包装 provider + startActivation 钩子钉 child 路由；核 rc.3 可达性、默认值与 README 偏差。"
read_when: "要引用子代理路由钉住的机制，或核对 provider 包装/团队注入在 rc.3 的实际可达性时。"
status: observed
updated: 2026-11-01
---
# 16 · `dsh-subagent-route-pin` 源码复核

> 复核对象：[`samples/16-tkaiz0406-dsh-subagent-route-pin.md`](../samples/16-tkaiz0406-dsh-subagent-route-pin.md)。只读 GitHub REST/raw 与 npm registry；**未安装、未构建、未跑测试、未启动 DSH**。`[RUN]` 仅 API/registry 读取与 `node --check` 语法解析。

## Provenance

| 项 | 值 | 核对方式 |
|---|---|---|
| 仓库 | `tkaiz0406/dsh-subagent-route-pin`（MIT，默认 `main`，2★/1 fork @2026-11-01，34 个提交） | GitHub REST |
| 改名 | 旧 owner `xywr8884156-tech` 的 URL 301 到本仓（repo id `1424052069`）；`homepage` 仍写旧路径，`repository.url` 已指 `tkaiz0406` | REST 301 + `package.json:35-42` |
| npm | **无**：`registry.npmjs.org/dsh-subagent-route-pin`、`@tkaiz0406/dsh-subagent-route-pin` 均 404；npm 搜索无同名包 | registry |
| tag / release | **无**：`/tags` 空、`/releases` 空 | REST |
| 审计 pin | commit `643519c541ac1a46287c827f8b7935024a3be278`（2026-10-29T14:56:50Z，HEAD） | `/commits/main` |
| 版本 | `package.json` `0.8.22`；README 安装示例仍写 `0.8.21.tgz`，ready 示例写 `0.8.13` | `package.json:3`、README:27/154 |
| 形态 | `index.js`(1390 行) + `client.js`(630) + `cordis.patch.yml`(35) + `bin/team-status.mjs`；`dsh.bundle.patch`、`dsh.client`(web, `inject: []`) | `package.json:60-68` |
| 依赖 | 无 `dependencies`；peer `@deepseek-ai/dsh`、`-tool-subagent`、`schemastery`(optional)，范围 `>=0.2.0-rc.1 <0.4.0` 的 rc 分支式；`engines.dsh` 同串 | `package.json:43-56` |
| CI | **无**：0 workflow、0 check-run、HEAD status `pending` | REST actions/check-runs/status |
| 发布 | 无 npm tarball，字节一致性无从比对 | `[OPEN]` |

## DOC（README 主张）

被复核的 README 固定链接：[`README.md@643519c`](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/README.md)。

- 主 agent 不动，单独给被委派 child 指定路由；**按 provider 生效，不按专家名单**（README:3-7）。
- 单发子代理走 `provider.start()`；团队成员不经过它，改钩 `startActivation` / 旧名 `startContinuable`（README:12-13）。
- `overrideMemberRoute` 默认开，覆盖 Teams 自带 `memberLlmProvider`（README:14）；README:95 又写「插件不会覆盖它」——**自相矛盾**。
- 零配置可用：路由没填、或 provider/model 不存在 → 打警告、继承（README:16,70）；另一处又说 `onPinFailure` 默认 `fail`、召唤直接报错（README:17）。
- `autoWireAgency` 默认开，挂载时改 profile 的 agency 行并留 `.bak-autowire-*`（README:18）。
- 每次委派写 `~/.dsh/subagent-route-pin.last-run.json`（README:19）。
- 失败回退表：`fallback:true` 时单发用调用方原路由重试、团队还原 `agentOptions` 重试；只在启动期可观测（README:185-195）。
- 兼容矩阵：`0.2.1-rc.3` 已验证，`seams:["startActivation"]`；peer 范围 `>=0.2.0-rc.1 <0.4.0`（README:203-208）。
- 174 项断言（README:249）；同一 README 的「升级回归」又写 128（README:263）。
- 发布：包名未被占用，两条 `--registry` 命令；「从 npm（发布后）」（README:272-280）。

## SRC-TARGET（`643519c`）

### 1. 注册的是一个包装 provider，但能力表不是宿主 spawn 的逐字拷贝

- `inject = ['subagents']`（[:64](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L64)）；注释写明只接受数组形式，对象形式会让 Cordis 等 `required`/`optional` 服务、插件静默挂起（[:57-63](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L57-L63)）。
- `RoutePinProvider.capabilities = {agentOptions, outputSchema, depthLimit, toolFilter, persona}`（[:81-87](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L81-L87)、[:390](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L390)），注释自称 spawn 的逐字副本；rc.3 的 spawn 实际是 `{agentOptions, agentPreset, outputSchema, depthLimit}`（SRC-DSH）。**多声明 `persona`/`toolFilter`，少声明 `agentPreset`。**
- provider 名取配置 `providerName`（[:396](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L396)）；挂载时 `ctx.subagents.registerProvider(provider)`（[:1301](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L1301)）；重名只 warn 并沿用旧实例（[:1306-1315](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L1306-L1315)）；disposer 绑本 fiber（[:1321](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L1321)）。
- `base()` 每次现查 `getProvider(baseProvider)`，缺失即抛（[:399-409](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L399-L409)）；`start()` 合并 `request.agentOptions` 后调 `base.start`（[:695-703](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L695-L703)）；`prepareContinuable` 委托 base，base 没有就抛（[:419-425](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L419-L425)）；`inheritsParentContext` 转发 base（[:411-417](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L411-L417)）。

### 2. 钉的是「一条路由」，按 label 开例外

- 路由 = provider/model（`routeKey`，[:351-353](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L351-L353)）；config row 只有一条，`configuredRoute()` 要求 provider+model 同时非空（[:436-467](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L436-L467)）。
- 例外只在 settings 文件 `experts`：key 取 `label.trim().toLowerCase()`，`exact` 或 `contains`（[:360-380](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L360-L380)、[:509-520](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L509-L520)）；优先级 `experts` → row → `settings.default`（[:522-523](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L522-L523)），都没有才抛 `routeMissing`（[:524-530](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L524-L530)）。
- label 由调用方给：原生 `subagent` 工具传 `label: args.description`（SRC-DSH，模型写的 3-5 词描述）；官方 Teams 传成员 description。**所以「按专家钉模型」依赖 label 文本，不是稳定 id。**
- 团队钩子与包装器共用同一个 `resolve()`（[:887-909](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L887-L909)、[:945](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L945)），没有按 provider/seam 再分层。

### 3. `startActivation` 钩子：本机 rc.3 上唯一会真正写路由的地方

- 接缝常量 `['startActivation','startContinuable']`（[:754](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L754)）；probe 返回**所有**存在的接缝（[:821-847](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L821-L847)），install 逐个 `defineProperty` 包住（[:1050-1070](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L1050-L1070)），只留一个 slot（[:1036-1048](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L1036-L1048)、[:1080](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L1080)）。
- 每次调用重读 `slot.resolve()` / `slot.options`（[:921-932](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L921-L932)）；`teamInjection` / `overrideMemberRoute` / `fallback` / `onPinFailure` 都在这里判（[:923-932](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L923-L932)）。
- 注入：调用方已有 `agentOptions` 且 `overrideMemberRoute:false` → 让位（[:939-941](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L939-L941)）；否则写 provider/model/effort/maxTokens（[:969-981](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L969-L981)），保留调用方其它字段、清掉旧 effort（[:974-978](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L974-L978)）；已是同一路由则不再注入（[:963-967](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L963-L967)）。
- 失败：只有 `fallback===true` 才重试（[:997](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L997)）；调用方原本没路由且 `onPinFailure!=='inherit'` → 直接抛，不退到父模型（[:999-1005](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L999-L1005)）；否则还原 `request.agentOptions`（[:1008-1009](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L1008-L1009)）再调一次。
- 能力标记：`{teamInjection:'installed'|'unavailable', enabled, seams, reason}` 挂两个 symbol（[:757-763](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L757-L763)、[:776-780](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L776-L780)），也导出 `teamInjectionCapabilities()`（[:1112-1125](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L1112-L1125)）；dispose 只在 descriptor 仍指向自己时还原（[:1093-1097](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L1093-L1097)）。
- 钩子**与 `teamInjection` 开关无关地安装**，开关只在调用内生效（[:923](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L923)）；关掉它，rc.3 上就没有别的注入点（见 SRC-DSH）。
- 注释自述 continuable child 不走 `provider.start`，`startLocal` 自己读 `request.agentOptions`（[:782-791](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L782-L791)）——与宿主实现一致。

### 4. 配置与默认值：包内 patch 自带一条具体路由

- `makeConfig` 默认（[:186-208](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L186-L208)）：providerName `pinned-account`、baseProvider `spawn`、strict `false`、fallback `true`、onPinFailure `fail`、autoWireAgency `true`、teamInjection `true`、overrideMemberRoute `true`；provider/model/effort/maxTokens 是 `volatile()` 无默认。
- apply 时再归一（[:1278-1296](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L1278-L1296)）：fallback `!== false`；onPinFailure 只有 `'inherit'` 才算 inherit，否则 fail。
- 包内 [`cordis.patch.yml:10-35`](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/cordis.patch.yml#L10-L35) **出厂就写了** `provider: deepseek-account` / `model: deepseek-flash`，另有 strict false、teamInjection true、fallback true；没有 onPinFailure/overrideMemberRoute。**安装即钉住，不是「零配置继承」。**
- 设置页只写 4 个字段（provider/model/reasoningEffort/teamInjection），带 revision 冲突检查（`client.js:344-359`）；effort 下拉写死 `low/medium/high`（`client.js:31`），与 open issue #1–#3（max 显示成 low）一致。

### 5. 失败面：包装 provider 缺失或不兼容

- 无可用路由：`pickRoute` 返回 undefined，`start()` 原样委托（[:686-693](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L686-L693)）。
- 目录不认路由：默认 `onPinFailure='fail'` → 抛 `routeFailure`（[:641-648](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L641-L648)），只有 `inherit` 才降级/回退 row（[:653-659](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L653-L659)）；`strict` 只是多一层，不是开关（[:646](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L646)、[:673](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L673)）。团队钩子则完全只 warn，不读 `strict`。
- `start()` 失败：`fallback !== false && onPinFailure === 'inherit' && !sameRoute` 才重试（[:712](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L712)），否则抛中文错误并给处置指引（[:721-726](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L721-L726)）。
- `baseProvider` 缺失：`start()` 在解析路由前就 `base()`（[:684](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L684)）→ 抛；`prepareContinuable` 同样抛（[:420-423](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L420-L423)）→ 经过该 provider 的委派全失败。
- **包装 provider 本身缺失**（插件没挂上，或 profile 行 `name` 解析不到）：`registerProvider` 没跑，消费者 `startActivation({provider:'pinned-account'})` 撞宿主 `NO_PROVIDER`；原生委派工具干脆不挂载，只打「not registered yet」等 `provider-added`（SRC-DSH）。
- **非 continuable 的 base**：包装器仍声明 `prepareContinuable`，宿主据此选 `startLocal`（SRC-DSH），随后包装器因 base 无该方法而抛——「方法存在即能力」的双刃。
- 记录：模块 import 写 `load.json`（[:1188-1200](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L1188-L1200)）、8s 未 apply 写 `probe.parked`（[:1202-1214](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L1202-L1214)）、apply 写 `applied|degraded|failed`（[:1215-1245](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L1215-L1245)）、ready 记录（[:1354-1375](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L1354-L1375)）；`last-run` 只在包装器 `start()` 的成功/失败写（[:704](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L704)、[:713](https://github.com/tkaiz0406/dsh-subagent-route-pin/blob/643519c541ac1a46287c827f8b7935024a3be278/index.js#L713)），**钩子路径不写**。

## SRC-DSH（0.2.1-rc.3）

- `SubagentRuntime.startActivation`（`dsh-subagent/lib/index.js:3036`）按**方法存在性**分流：`provider.prepareContinuable === void 0 ? manager.startExternal(spec) : manager.startLocal(spec)`（`:3047`）。
- `provider.start(request)` 只有一处调用：`host.startExternal` 闭包（`dsh-subagent/lib/index.js:2997-2998`），而它只服务 `startExternal` 分支（`:1483`、`:3047`）。
- `startLocal` 用 `resolveChildAgentOptions(parent, request.agentOptions, depth)`（`:1400`）定 child 路由；`agentOptions` 字段是 provider/model/reasoningEffort/**maxTokens**（`:315-331`；`dsh-agent/lib/types/runtime-types.d.ts:22-31`）。
- 内置 `spawn`（`dsh-subagent-spawn-in-process/lib/index.js`）能力 `{agentOptions, agentPreset, outputSchema, depthLimit}`（`:21-26`）、`inheritsParentContext=false`（`:27`）、**只有 `prepareContinuable()`（`:31-33`），没有 `start`**。
- `registerProvider` 要求 `start` 或 `prepareContinuable` 至少一个，重名 `DUPLICATE_PROVIDER`（`:3256-3272`）；`expectProvider` 缺失即 `NO_PROVIDER`（`:3293-3298`）；`assertCapabilities` 校验 agentOptions/outputSchema/depthLimit，`agentPreset` 另有检查（`:3312-3330`）。
- 原生 `subagent` 工具：`startActivation({provider, label: args.description, request, ...})`（`dsh-tool-subagent/lib/index.js:475-481`）；provider 不存在时工具不挂载、等 `subagent/provider-added`（`:498-508`）。
- 官方 `dsh-experimental-agent-team` 也用 `startActivation({provider, label, request})`，request 不带 `agentOptions`（`dsh-experimental-agent-team/lib/index.js:1032-1041`）。
- 本机全树**没有 `startContinuable`**（grep 0 命中）——插件探针报 `seams:["startActivation"]` 与此一致。
- **推论（代码路径阅读，未实跑）**：包装器声明了 `prepareContinuable` → 宿主走 `startLocal` → `provider.start` 不被调用；因此 rc.3 上「钉住」实际由 `startActivation` 钩子完成，`teamInjection:false` 会同时关掉单发与团队两条注入。

## TEST

- 离线 harness `test/run.mjs`（1756 行）+ `test/logs.mjs`（312）+ `test/client.mjs`（209）；`package.json` scripts `test`/`verify`/`ready`（`:69-76`）。
- 静态计数：`check(` 171 处、唯一标签 115 个；README 同时写 174 与 128 项断言，**未运行无法裁决**。
- harness 的 fake service 把 `startActivation` 放在原型上（`test/run.mjs:64-70`），但**从不调用它去分派 provider**；测试直接 `provider.start(request)`（`:8-10`、`:103-107`）。fake base 同时有 `start` 和 `prepareContinuable`（`:48-57`），而真实 spawn 只有后者（SRC-DSH）——测试固化的是包装器契约，**测不到「宿主不调 start」这条路径**。
- 覆盖点（节选）：路由/热读/优先级/半填 row、strict 与 no-route 降级、团队注入（override 三态、空 effort、maxTokens）、能力标记与双接缝、默认 fail 不静默换模型（第 25 节）、团队重试（第 26 节）、三行日志契约（第 27 节）、ready 记录（第 28 节）。
- `test/logs.mjs` 读 readiness/probe 文件校验身份、版本、seams、路由来源、龄期与损坏记录；`--strict` 只额外把 `teamInjection:'unavailable'` 判失败。

## CI

**无。** 仓库无 `.github/`（tree 内无 workflow），`/actions/workflows` = 0，HEAD 的 check-runs = 0、status = `pending`。README 的「174 项断言全绿」没有同 SHA CI 可核，`[CI] None`。

## RUN

- 读：GitHub REST（repo / tags / releases / commits / tree / contents / check-runs / status / issues）、`registry.npmjs.org`（两个名字均 404）、按 SHA 取 raw 文件。
- 解析：`node --check index.js`、`node --check client.js` 仅语法解析，不执行插件。
- **未做**：`npm install`、`pnpm pack`、`node test/run.mjs`、`node test/logs.mjs`、启动 DSH、真实委派。`[RUN]` 不能证明任何运行时行为。

## 卡片偏差表

| 卡片 / README 主张 | 源码实际 | 处置 |
|---|---|---|
| `provider.start()` 是 child 创建前唯一可改点（README:12，index.js:4-9） | rc.3 的 `startActivation` 在 provider 有 `prepareContinuable` 时走 `startLocal`，`provider.start` 只在 `startExternal` 分支被调；包装器自己声明了 `prepareContinuable` | 卡片改写：rc.3 的活注入点是 `startActivation` 钩子；`start()` 可达性取决于 provider 形态 |
| 单发走 `provider.start`、团队走钩子（README:12-13） | 两条路径在 rc.3 都经 `startActivation`；钩子不筛 provider，对全部调用生效 | 卡片写「钩子覆盖单发与团队」；`teamInjection:false` 等于关掉两处 |
| 零配置可用、路由不存在只警告并继承（README:16,70） | 默认 `onPinFailure='fail'`：目录不认路由即抛；包内 patch 还自带 `deepseek-account/deepseek-flash` | 卡片写「默认 fail-loud + 出厂自带路由」 |
| `fallback:true` 就会重试（README:185-193） | 单发还要求 `onPinFailure==='inherit'`；团队要求 `fallback===true` 且（调用方原路由存在或 inherit） | 卡片写两道闸，并标 README 表在默认配置下不成立 |
| `strict:true` 才变硬错误（README:70） | 默认 `onPinFailure='fail'` 已是硬错误；`strict` 只影响单发，团队钩子只 warn | 卡片写 `strict` 的有效范围 |
| Teams 路由「插件不会覆盖它」（README:95） | 与 README:14 自相矛盾；实现默认 `overrideMemberRoute:true` 覆盖 | 卡片写默认覆盖；README 矛盾列 `[OPEN]` |
| 自动接线不需手改 YAML（README:18） | 只改 profile `cordis.patch.yml` 的 agency 行并留 `.bak-autowire-*`；不补其它字段 | 卡片写副作用与备份 |
| 每次委派都写 last-run（README:19） | 只有包装器 `start()` 成功/失败写；钩子路径不写 | 卡片写范围 |
| 174 项断言 / 128 项断言（README:249,263） | 同一 README 两个数；静态 171 个 `check(` 调用 | 卡片不写具体数，memo 记 `[TEST]` 计数 |

## `[OPEN]`

- agency-agents 是否绕过 `startActivation` 直接调 `provider.start`（本轮未读其源码）。
- 真实宿主上 `ctx.subagents` 是否为消费方同一对象实例——钩子 `defineProperty` 的可见性未实跑。
- 0.2.0-rc.x 的 `startContinuable` 形态（本机无该版本，全树 0 命中）。
- >0.4.0 或宿主冻结服务对象后的降级行为（README 声称置 `unavailable`，未验）。
- 无 npm tarball，发布物与 commit 的字节一致性无法比对。
- `checkRoute` 不校验 `reasoningEffort`；设置页写死三档（issue #1–#3 仍开着），无效 effort 的错误形态未测。
- `experts` 以 label 匹配，而原生工具的 label 是模型写的 `description`，稳定性未测。
- 未跑测试、未装插件：实际断言数、真实注入效果、`autoWireAgency` 的实际 YAML diff 均未观测。
