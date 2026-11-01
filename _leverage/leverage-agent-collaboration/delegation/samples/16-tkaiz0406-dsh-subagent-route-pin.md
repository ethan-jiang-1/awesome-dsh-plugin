---
title: "tkaiz0406/dsh-subagent-route-pin"
domain: agent-delegation
kind: sample
positioning: "`dsh-subagent-route-pin@0.8.22`（未上 npm）：包装 subagent provider，并在 startActivation 上补 agentOptions，给被委派 child 钉独立 LLM 路由。"
takeaway: "一条 row 管所有 child、按 label 开例外；rc.3 上真正生效的是 startActivation 钩子，不是 provider.start。"
read_when: "要给专家/团队成员单独分模型，或判断 provider 包装与 startActivation 钩子哪个才生效时。"
status: observed
updated: 2026-11-01
tier: 典型
life: active
evidence: L1
answers: Q2
---
# 16 · `tkaiz0406/dsh-subagent-route-pin`

> **一句话**：给被委派的专家/团队成员单独钉一条 LLM 路由；不改委派工具、不动主 agent，而是注册一个包装 provider，再在 `startActivation` 上补 `agentOptions`。
> **边界**：1 同进程父子 + 团队创建缝 · **过了哪些门**：C + G · **证据成熟度**：固定 commit 复核，未安装/未运行。

> 导航：[delegation README](../README.md) · [宿主契约](../01-host-contract.md) · [样本百科](../../encyclopedia.md) · [对照 15](./15-Garybot126-dsh-subagent-models.md)
> **证据链**：commit `643519c`（无 npm、无 tag）；机制、行号与 README 偏差见 [`16 源码复核`](../_证据/16-route-pin-源码复核.md)。

## 设计思路

**一句话设计思路**：「大脑 + 4 路子代理挤在同一个 provider 额度里」不是容量问题，是路由问题；它把子代理的路由从「继承父」改成「一条可配置的 row」，并且只改 child、不改主 agent。

**作者的选择**：不碰委派工具、不碰 `agent/request`，注册一个包装 provider（`pinned-account` → `spawn`），在 `provider.start(request)` 里填 `agentOptions`；团队成员的创建不经过 `provider.start`，就在 `ctx.subagents.startActivation` 上包一层补 `agentOptions`。

**一个必须点破的前提**（本卡与 README 分道的地方）：rc.3 的 `startActivation` 按方法存在性分流——provider 有 `prepareContinuable` 就走 `startLocal`，`provider.start` 只在 `startExternal` 分支被调；包装器恰好声明了 `prepareContinuable`，真实 `spawn` 又只有它。**所以 rc.3 上真正生效的是 `startActivation` 钩子，不是包装器的 `start()`。**（代码路径阅读，未实跑，见 memo 的 SRC-DSH。）

**钉的是路由，不是子代理**：一条 config row 管所有 child；settings 的 `experts` 只是按 label 文本开例外，而 label 来自原生工具的 `description` 或 Teams 的成员描述。想要「每个专家一套模型」，靠的是 label 命中，不是一个稳定身份。

## 机制

1. **注册**：`ctx.subagents.registerProvider` 注册名为 `pinned-account` 的包装 provider，委托 `spawn`；`base()` 每次现查，缺了就抛（index.js:1301、:399-409）。
2. **单发**：`start()` 合并 `request.agentOptions`，写入 provider/model/effort/maxTokens，再调 `base.start`，成功或失败都写 `last-run`（:695-713）。
3. **团队/continuable**：`TeamInjectionAdapter` 探测 `startActivation` / `startContinuable`，逐个 `defineProperty` 包住；调用时按 `overrideMemberRoute` 决定让位还是覆盖，失败还原 `agentOptions` 再重试一次（:876-1016）。
4. **能力标记**：`{teamInjection, enabled, seams, reason}` 发布在服务 symbol 上，也导出 `teamInjectionCapabilities()`；`seams` 是**实际包住的方法名**，挂错方法不能再冒充成功（:853-874、:1112-1125）。
5. **三件自检**：`load.json`（模块被 import）、`probe.json`（8s 未 apply → parked）、`ready.json`（apply 的挂载裁决），把「装了没生效」拆成三种可判定状态（:1188-1245）。
6. **自接线**：挂载时把 profile 里 agency 行的 `provider` 改成 `pinned-account`，改前留 `.bak-autowire-*`（:240-306）。

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | 真相源是 profile 的 config row（volatile，下一次委派生效）；`~/.dsh/subagent-route-pin.json` 的 `experts`/`default` 只作覆盖；ready/load/probe/last-run 另写 4 个文件 | 一条 row 管全体；settings 的 `default` 被 row 盖住只打 WARN；`last-run` 只覆盖包装器路径 |
| 冲突裁决 | `experts` → row → default；同一 row 用 `normalizeRoute` 统一两处注入；`overrideMemberRoute` 默认压过 Teams 自带路由；已同路由不重复注入 | 谁最后写 `request.agentOptions` 谁赢；钩子改的是共享服务对象，与别的包装者按定义顺序叠加；注入发生在委派工具的策略预检之后 |
| 失败收敛 | 默认 fail-loud（`onPinFailure:'fail'`）；单发重试要 `fallback` + `inherit` 两道闸；团队失败还原调用方原路由；能力标记供外部降级；三种落盘记录区分「没 import / 没 apply / apply 失败」 | 默认不重试（README 的回退表在默认配置下不成立）；`strict` 只管单发；base provider 缺失时直接抛；child 流内的 429 抓不到 |

**额外边界**：

- 包内 patch 出厂就带 `deepseek-account/deepseek-flash`，**装完即钉**，不是「零配置继承」。
- 包装 provider 的能力表不是 spawn 的逐字副本：多 `persona`/`toolFilter`、少 `agentPreset`；后者会让带 preset 的委派撞 `UNSUPPORTED_CAPABILITY`。
- 非 continuable 的 base 被包装后会在 `prepareContinuable` 抛，整条委派失败——「方法存在即能力」的双刃。
- 在 rc.3 的代码路径上，`teamInjection:false` 会同时关掉单发与团队注入——它是钩子里的唯一开关。

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`tkaiz0406/dsh-subagent-route-pin`](https://github.com/tkaiz0406/dsh-subagent-route-pin)（旧 owner `xywr8884156-tech` 已改名 301 到此） |
| **npm** | **无**（registry 404；无 tag、无 release） |
| **版本(本次读)** | `0.8.22` @ commit `643519c`（2026-10-29，HEAD） |
| **License** | MIT |
| **安装** | 无 npm：按 README 的 tarball / 本地目录安装（示例仍是 `0.8.21.tgz`）；装后重启 DSH |
| **接线** | `dsh.bundle.patch` → `cordis.patch.yml`（id `subagent-route-pin`）+ `dsh.client`(web) |
| **依赖** | peer `@deepseek-ai/dsh`、`-tool-subagent`；范围 `>=0.2.0-rc.1 <0.4.0`；`engines.dsh` 同串 |
| **数据** | 设置文件 `~/.dsh/subagent-route-pin.json`；另有 `ready` / `load` / `probe` / `last-run` 四个记录文件 |
| **测试** | `node test/run.mjs`（离线 harness）+ `node test/logs.mjs`（读真实 ready 记录）；**无 CI** |

## 借用指南

### 可借鉴

1. **用 provider 名当「路由开关」**：把「这个专家走哪条车道」收敛成一个 provider 名，委派方只改一行 YAML——比每个专家配置里散落 model 好审。
2. **能力标记带 `seams`**：不只报「装没装」，还报「包住了哪个方法」；方法名是契约，挂错方法在日志里看得出来。
3. **三种落盘记录**：load / probe / ready 把「没 import」「import 了没 apply」「apply 失败」分开；升级后先读文件，再怀疑额度。
4. **volatile 配置 + 每次 spawn 读访问器**：设置页保存后下一次委派生效，不用重挂载。
5. **注入前快照、失败还原**：覆盖调用方 `agentOptions` 前存原对象，失败时还原而不是整块删掉，别把 Teams 自己的成员路由一起丢掉。
6. **零配置时不阻断**：没有可用路由就原样委托、让 child 继承父。可选功能不该变成全机故障。

### 别照抄

- **别假设 `provider.start` 会为主-子委派执行**：rc.3 的 `startActivation` 见到 `prepareContinuable` 就走 `startLocal`；想钉路由就钉 `startActivation`，或者别声明 `prepareContinuable`。
- **别手抄 provider 能力表**：本例多写 persona/toolFilter、漏写 agentPreset；能力表是宿主的校验输入，抄错就撞 `UNSUPPORTED_CAPABILITY`。
- **别把「fallback 默认开」当「失败会回退」**：还要 `onPinFailure:'inherit'`；默认是 fail-loud。
- **别把 `teamInjection` 当团队专属开关**：钩子对全部 `startActivation` 生效；关掉它，单发也没人钉。
- **别用 label 当稳定身份**：原生工具的 label 是模型写的 `description`，`experts` 的键会漂。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| rc.3 上钉路由靠 `startActivation` 钩子，而非包装器 `start()` | `[SRC-TARGET]`/`[SRC-DSH]` | [`16 memo`](../_证据/16-route-pin-源码复核.md)（`index.js:876-1016`；`dsh-subagent/lib/index.js:3047`） | 代码路径阅读，未实跑；agency 是否直调 `provider.start` 未核 |
| 路由是「一条 row + label 例外」，不是 per-subagent | `[SRC-TARGET]` | 同上（`index.js:436-530`） | label 取自 description，稳定性未测 |
| 默认 fail-loud；fallback 要两道闸 | `[SRC-TARGET]` | 同上（`index.js:641-726`） | 与 README 回退表不符 |
| 能力表与 spawn 不一致（多 persona/toolFilter、少 agentPreset） | `[SRC-TARGET]`/`[SRC-DSH]` | `index.js:81-87`；`dsh-subagent-spawn-in-process/lib/index.js:21-26` | 只在带 preset 的委派上可见 |
| 包内 patch 自带具体路由 | `[SRC-TARGET]` | `cordis.patch.yml:10-35` | 安装即钉，README 的「零配置」不成立 |
| 无 npm / tag / CI | `[RUN]` | registry 404、`/tags` 空、0 workflow | 只能按 commit 固定 |

**未验证**：真实宿主上的注入生效、`autoWireAgency` 的实际 YAML diff、0.2.0-rc.x 的 `startContinuable`、`>0.4.0` 的降级、agency 的直接调用路径，均 `[OPEN]`。
