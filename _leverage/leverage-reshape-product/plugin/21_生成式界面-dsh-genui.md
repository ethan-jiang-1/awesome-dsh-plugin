---
title: "生成式界面 · dsh-genui"
domain: reshape-product
kind: sample
positioning: "pinned 0.15.0 source renders `dsh-ui` fences via DOM; npm artifact provenance and action trust unverified."
takeaway: "在 pinned 0.15.0 source 中，DOM fence 是扩展机制而非 DSH native fence slot；但历史卡 npm artifact 未 pin 对齐。Schema/test 存在不构成安全、action 授权或恢复实测。"
read_when: "要让模型输出可交互组件；或要设计容错的内容协议。"
status: observed
updated: 2026-10-31
---
# 生成式界面 · dsh-genui:把回复本身变成产品界面

> **研究范围**：固定目标 source commit [`e00bdcf`](https://github.com/omdsh-dev/dsh-genui/commit/e00bdcfbf7d4492afc95d5e52af350d6b68882c6)（签名 verified；manifest package version `@changfenhuang/dsh-genui@0.15.0`），DSH 对照 `dsh-v0.2.1-rc.3` / commit `1f81c047…`。历史卡只给过宽 DSH version range，未给确切 npm version；因此本次 pin 只能归结论到仓库 source commit，npm 0.15.0 tarball 与该 commit 的 provenance 尚未证明。完整分源见[`07 源码复核`](./_证据/08_生成式界面-dsh-genui-源码复核.md)。
> **证据成熟度**：pinned `0.15.0` 源码/test declarations 可作有限机制参考；发布 artifact 对齐、性能/成本、安全隔离及 runtime 行为不作断言。无 `[RUN]`，CI 只记录 workflow 配置，未查询 same-SHA run 状态。
> **类**:`2` 内容形态 · **层**:3（槽位/内容）+ 4（身份/模型表达） · npm 近 30 天 48,798 / ★ 827（2026-10-31）
> **一句话**：pinned source 以 DOM assistant-fence observer 实现 `dsh-ui` JSON 渲染；它不是 DSH 提供的 fence-level native slot。发布包版本与这份源码的精确对应仍待证明。
> **借鉴价值（限 pinned source）**：**① 对 DOM fence 明确承认与 native slot 不同的耦合/清理合同；② strict schema 与节点级 fallback 可作为内容协议设计线索，但不能由 README 推安全或 node/action 上限；③ action payload 是模型事件，不等于用户授权、业务确认或幂等执行；④ unknown/invalid fence 保留可读 Markdown；⑤ Theme CSS/token ownership 需覆盖部分 surfaces 与不同失败/卸载路径。**

> **样本档案**
> **repo**:[`omdsh-dev/dsh-genui`](https://github.com/omdsh-dev/dsh-genui) · **npm**:`@changfenhuang/dsh-genui` · **审计 source version**:`0.15.0`（历史卡 npm pin 未对齐）
> **目录条目**:`data/plugins/omdsh-dev__dsh-genui.yml`(`ui`)
> **文档装法**:README 指示 `dsh plugin --profile web add @changfenhuang/dsh-genui`；旧 scope remove/reinstall 主张未复现
> **证据链**：协议/schema、stream/fallback、action、theme、tests/CI 定义及 DSH 接缝见[`07 源码复核`](./_证据/08_生成式界面-dsh-genui-源码复核.md)。

---

## 它想干什么 · 为什么值得借鉴

**意图 [DOC]**：README 将 GenUI 描述为 assistant message 中 `dsh-ui` fenced JSON 的呈现器，宣称可在回复中生成可操作组件；本次验证了仓库 source 对 DOM fence channel 的实现，但历史样本并无 npm/source tag 对齐证据。

**意义 [SRC-TARGET/OBS]**：pinned source 证明该实现观察 assistant DOM 内容并解析特定 fence；这不是“宿主给了正式内容协议扩展 API”，且与 DSH chat-node slot 的机制不同。它需要针对 MutationObserver/render ordering/fence fallback 承担 DOM lifecycle 与宿主 MarkDown renderer 的兼容成本。

**用户价值 [DOC/OPEN]**：README 描述排序/过滤/本地滑杆和 action feedback；测试目录包括 debounce/agentloop/fallback cases，但本次未执行。不得将模型收到 action payload 说成业务确认、权限授权或至少一次/至多一次执行保证。

**表达 [DOC/SRC-TARGET]**：README 描述无 action 控件 disabled、无效 fence 回退代码块；pinned source/tests 对部分 schema/fallback path 有支持。复杂引擎静态资源加载失败、异步资源完成后的卸载等不应推成“用户永远看到原文”的普遍保证。


## 0. 一页速览

| 主张/机制 | 固定 source / DOC 证据 | 边界 |
|---|---|---|
| 当前 source identity | repo `omdsh-dev/dsh-genui` commit `e00bdcf…`；manifest `@changfenhuang/dsh-genui@0.15.0` | 历史卡没有 npm exact version；tarball→commit provenance 未确认 |
| Extension point | README/代码用 assistant DOM `dsh-ui` fence observer | 不是 DSH native fence-level slot；有 DOM patch/lifecycle coupling |
| Schema/fallback | SKILL.md + schema/root/guard tests；invalid/unrecognized fences fallback markdown | 本次只读未跑；不由此推出 node count/byte/latency budgets |
| Actions | README/tests describe action payload, disabled controls, debounce/feedback | payload is model event, not authorization/confirmation/idempotency guarantee |
| Trust | whitelist nodes, no eval/script claims, trusted host-controlled map/style inputs | 未证明 CSP/origin isolation/sandbox 或所有 URL schemes 被拒绝 |
| Streaming/error recovery | Tests cover partial fence/render/repair/fallback and RAF cleanup | 测试源存在不是运行结果；异步 asset-load errors/全卸载无泄漏未证明 |
| Cost / performance | README estimates 200–800 tokens/fence and performance phrases | 作者估计/宣称；本轮未复算/测量 |
| Tests / CI / RUN | 测试与 workflow 配置存在；本次无运行 | same-SHA run 未确认成功，不宣称 CI green |

---

## 1. 它在产品里的位置

| 层 | 动作 | 说明 |
|---|---|---|
| 3 槽位 | 会话里的可交互块 + `/panel` 常驻面板 | 不注册新页,寄生在已有容器 |
| **4 身份** | 给模型一套**新的输出词汇** | 本线唯一一例真正改变"模型能说什么"的插件 |

### 1.1 为什么它是"内容形态"而不是"壳"

```
Host --streams Markdown prose & ```dsh-ui fence--> DOM --检测 fence 并按白名单规范化--> GenUI
```

它**没有**新窗口、没有新页面、没有新路由。它只做一件事:**把一种特殊格式的文本,在渲染时换成一个组件**。这条路的代价与收益:

| | 内容协议(它的选择) | 若改成 API(注册渲染器) |
|---|---|---|
| 宿主改动 | **零**(不 patch、不改 `node_modules`) | 需要槽位 |
| 模型侧成本 | 要教会模型一种格式 | 要教会模型调工具 |
| 失败表现 | 退化成代码块(**可读**) | 白屏或空块 |
| 流式支持 | 边到边解析边挂载 | 通常要等完整参数 |

---

## 2. 机制与信任边界

### 2.1 DOM fence 是本项目扩展层，不是 DSH native fence slot

`[DOC][SRC-TARGET]` 固定 source README/source 使用 assistant DOM 中严格标记为 `dsh-ui` 的 fence channel；DOM observer 扫描/挂载 fence，而不是注册一个 DSH fence-level renderer。DSH rc.3 的 `conversation.chat.node` slot 按 `ChatNodeKind` 替换整个节点，不提供围栏内部文本替换 API。两者不能混称“使用原生 GenUI slot”。

> **洞察**：若扩展依赖 DOM 观察，要记录宿主 Markdown renderer、节点 identity、streaming mutation、cleanup owner；DOM workaround 应明确与 native slot 的不同故障面。

### 2.2 Schema / node guards 与 fallback 层次

Pinned `SKILL.md` 定义字段形状；schema tests 存在 root shape/invalid input/node guards/ECharts/map guard 覆盖。README 描述节点错误局部丢弃、坏 fence 保留 Markdown、部分 Mermaid 修复；测试目录覆盖 partial render、repair/fallback。**本次没穷举 schema 所有预算**，不能声称有 node-count/byte-size/action-count 的通用上限，也不能因为 README 写 strict JSON 就声称完全拒绝所有外部 URL scheme。

> **洞察**：协议校验要定义节点级与块级失败原子性，并通过 tests 保证“坏节点不毁兄弟、坏块仍可读”；内容白名单不是浏览器 sandbox。

### 2.3 Action payload 不等于业务授权或幂等调用

README/tests 描述 action payload 回到模型 event loop，无 action 控件 disabled；有离散 dispatch 和滑杆 debounce 测试。Action 是交互意图/消息事件，不能据此声称已有业务 confirmation gate、CSRF protection、idempotency key、duplicate dispatch suppression 或权限授权。

> **洞察**：模型输出的 action 应先经服务侧权限/确认/幂等处理；渲染时 disabled 只消灭 dead-click，不建立业务授权。

### 2.4 Streaming lifecycle、主题和资源错误

DOM fence/partial rendering、fallback、RAF cleanup 有测试源；不等于所有 async asset load/unmount race 都无泄漏。CSS surface chain 区分 card/table surfaces；部分 settings/test 混用 CSS 与 DOM。ECharts/Mermaid/3D static route load 失败与 JSON/schema fallback 是不同错误面，未证明资源加载错误都会退 Markdown。

> **洞察**：对每一异步资源分别定义 loading/error/unmount cleanup UI；“坏 JSON 回退”不能替代 chunk/network failure fallback。

### 2.5 安全边界

README 的约束包括白名单节点、no `eval`/script injection、密码密钥不采集、外部 style 由 trusted host config 管理；README 没有声称 iframe/CSP/origin isolation 等 sandbox。复杂 ECharts options、Mermaid、链接/媒体属性仍需逐路径检查。

> **洞察**：把“受限内容协议”写成攻击面收窄，不叫安全隔离；如果将来允许外部资源、HTML 或 host actions，需要增设明确的 origin/permission/confirmation/URL policy。

---

## 3. 产品体验（README 主张，未实测）

- `[DOC]` README 给出 add → restart → hard refresh → 检查 console marker 的排障路径；marker、panel/fence 示例和导出形式属于文档 claim。
- `[SRC-TARGET]` 固定源码/测试对 DOM fence parsing、partial stream、fallback 与 action feedback 有一定实现/覆盖；本次没有启动宿主确认浏览器中内容、键盘/可访问性或模型消息往返。
- `[OPEN]` 资源 chunk 失败、旧会话回看、跨 session 状态 fingerprint、导出 HTML 在离线/受限网络运行的实际浏览器体验。

---

## 4. 证据与边界

| 证据类型 | 当前结论 |
|---|---|
| 采用信号 | npm 月下载 48,798 / ★827（2026-10-31），不代表用户数或运行质量 |
| Source pin | GitHub `e00bdcf…`, repository `package.json` 0.15.0；npm tarball/gitHead provenance 未对齐 |
| README claims | `dsh-ui` protocol、action/UI behavior、token/performance estimates；是文档主张，性能数字未测 |
| Source/tests | Schema/guard, DOM fence lifecycle, feedback/debounce/theme tests were read; no target tests run |
| CI/RUN | workflow has configured current/legacy Node+DSH lanes; same-SHA run 未查询或引用成功；本轮无 install/build/test/run |
| Security | No proven iframe/CSP isolation or complete external URL scheme policy; no CSRF/idempotency/confirmation guarantee for actions |
| Resource failures | Markdown fallback applies to invalid/unsupported fence paths; it does not prove ECharts/Mermaid/3D chunk failure renders a fallback placeholder |
| Provenance | This is pinned repo source mechanism at 0.15.0, but not proven identical to the historical npm artifact sampled by the card |


---

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 模型输出需要承载富 UI，但宿主没有匹配扩展 API | 当扩展必须嵌入 assistant 文本时，可设计独特 fence + 严格 schema；若改 DOM，必须明确这不是 native renderer API，并承担 host markup/lifecycle coupling。 | `[SRC-TARGET]` pinned 0.15.0 通过 DOM fence detection；`[SRC-DSH]` rc.3 chat-node slot 是整节点替换，不是 fence parser。 | 不改宿主 registry 即能渲染内容；代价是解析/stream/MutationObserver cleanup 与 host Markdown renderer 兼容工作。 | 固定协议 version、DOM ownership、partial fences、observer cleanup 和 invalid fallback。 | 卡片所针对 npm release 未与源码 provenance 对齐；当前 source facts 只归 0.15.0 commit。 | 将 DOM hack 当官方 seam，会在宿主 Markdown DOM/streaming 改动后破碎或重复挂载。 |
| 坏内容不应毁掉可读回复 | 将验证单位细到节点，同时为整块无效内容保留原始文本/代码块退化；记录哪些 repair 是自动修复，哪些是拒绝。 | `[SRC-TARGET][TEST]` schema/root-shape/invalid-fence/partial-render/fallback/repair test files 存在；未运行，完整分支未穷举。 | 单个坏节点影响面局部、用户仍能复制原文；代价是呈现部分内容可能藏掉重要数据，需可见诊断。 | 定义 fatal vs drop-node、原文 fallback 和用户可诊断的错误 summary。 | 不能据测试文件存在声称所有异常/过深输入/资源错误都覆盖。 | 过度丢弃使关键数据静默消失；整块白屏则用户无可恢复原文。 |
| JSON UI 控件可以触发 agent action | 将无 receiver 的控件渲染为 disabled；本地筛选/排序不需要回模型则留本地。业务层另实现权限/确认/幂等。 | `[DOC][TEST]` README/API 描述 action/debounce/local interactions，测试集有 action/debounce/fence feedback；没证据证明 CSRF、idempotency、confirmation 或 auth gate。 | 避免 dead-click 和不必要模型往返；代价是分清 view event 与带副作用业务命令。 | 为 action 设权限 owner、confirmation policy、request id/dedup、rate/size limits、error feedback。 | action payload 是模型事件，不是权限已确认；本轮无 runtime dispatch。 | 将 UI action 直接当授权命令会导致重复/越权副作用。 |
| UI 资源按需加载以减小首屏 | 懒加载重渲染引擎时，为 route/network/init failure 提供局部占位/重试；与 JSON fallback 分开。 | `[SRC-TARGET]` README/source 存在 ECharts/Mermaid/3D asset loading paths/tests；未验证加载失败后是否回 markdown。 | 缩短首屏；代价是引入 chunk/route/cache 生命周期与失败态。 | 测试网络失败、缓存失效、组件卸载中断、重试以及版本不匹配。 | 流式/invalid-fence fallback 不覆盖 engine chunk failure。 | 加载失败留下空白块却没有重试，用户误认为模型没回答。 |
| 内容 UI 需要接入宿主皮肤 | 只暴露 scoped plugin tokens，并把不同 surface（card/table）单独建模，避免写宿主全局 token。 | `[SRC-TARGET]` README/token chain 与 pinned CSS/source；其 owner/selector scope 未逐声明穷尽。 | 降低主题冲突并保留不同 surface 层次；代价是建立稳定 alias contract。 | 给 tokens 做 namespace、fallback、disable/reset test 与 host theme matrix。 | 不能声称“一变量控制所有表面”或所有 theme lifecycle 已清理。 | 全局 token 覆盖会污染宿主/兄弟插件，卸载后残留样式。 |
| 内容协议被宣传为“安全 UI” | 将白名单/无 eval 称为约束层；是否是 sandbox 要单独证明 origin、CSP、外部资源、action boundary。 | `[DOC]` README security promises；本次无源码证据证明 iframe/CSP/origin sandbox。 | 诚实披露信任范围；代价是有些节点类型需禁用或代理。 | 绘制模型输入→renderer→外链/host action 的信任边界，测试 URL schemes 和 CSP。 | 当前不能断言无外部请求、无 XSS 或隔离。 | 用户将“zero eval”误读为 sandbox，暴露 host/session 数据。 |

---

## 6. 已知失效边界与下一步验证

- `[OPEN]` 历史 npm artifact 对应 source 未 pin；需取得发布 provenance/tarball 内容映射后再把 `0.15.0` 实现推广到卡片原目标版本。
- `[OPEN]` 浏览器 observer 在 plugin disable/unmount/profile navigation 后是否完整 disconnect，需真实 host lifecycle test；DOM patch 不由 DSH slot registry 自动兜底。
- `[OPEN]` ECharts/Mermaid/3D static route / chunk load fail、service worker cache mismatch 的用户状态和 retry path。
- `[OPEN]` app action 重复点击、模型自动回馈、用户取消、host authorization、CSRF/URL validation 与 action dedupe/idempotency。
- `[OPEN]` LRU interaction state 的 fingerprint key 是否隔离 user/profile/session、storage corruption/eviction 语义与跨刷新恢复。
- `[OPEN]` `30+ Component Ecosystem` 与 schema preset 数量口径差异；须定义 component/preset/template 的计数单位。
- `[OPEN]` Node 22/24 CI success covers which lanes; independent host/compat scripts是否属于same commit checks需看实际run details。

## 7. 下一步验证

- [ ] 若获取准确 npm tarball provenance，在 scratch DSH rc.3 profile 对比实际 mounted module rows、profile overrides 和 hard refresh。
- [ ] 在 disposable browser profile 对 theme/composer/sidebar 分别 probe timeout、disable、effect dispose、navigation/unmount，检查 DOM/token/style/fiber/RAF 清理。
- [ ] 执行 real slot + DOM observer integration，测试 malformed/partial fence、chunk failure、重复 action、无action控件和 host gate。
- [ ] 如宣称 peer range 兼容，按 rc.1/rc.2/rc.3/0.2.2 alpha 分别核验 slot/theme APIs，不从 dev pin 外推。
