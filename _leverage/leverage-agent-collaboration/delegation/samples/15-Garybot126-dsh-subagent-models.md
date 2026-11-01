---
title: "Garybot126/dsh-subagent-models"
domain: agent-delegation
kind: sample
positioning: "`dsh-subagent-models@0.1.2`：在 agent/request 上给被委派子代理统一 provider/model/effort，本对话覆盖优先于全局默认。"
takeaway: "不改子代理工具/preset，在下层改 frozen call config；但 README 的 preset 优先级与模型校验在实现里不存在。"
read_when: "要统一子代理模型，或判断“委派路由”该挂哪条缝时。"
status: observed
updated: 2026-11-01
---
# 15 · `Garybot126/dsh-subagent-models`

> **一句话**：子代理用哪个模型，不应由每个委派工具各配一套；它在 `agent/request` 上统一覆盖**被委派 child** 的 provider/model/effort，顶层会话保持用户选择。
> **边界**：1 同进程父子 · **过了哪些门**：C + G · **证据成熟度**：固定 commit 复核，无运行。

> 导航：[delegation README](../README.md) · [宿主契约](../01-host-contract.md) · [样本百科](../../encyclopedia.md)
> **证据链**：[`15 源码复核`](../_证据/15-subagent-models-源码复核.md)（npm 0.1.2 / commit `a105855`）。

## 设计思路

**一句话设计思路**：委派工具（`subagent`）在 agent-plane preset 里，插件改不了它的 `agentOptions`；所以路由下沉一层——`agent/request` 是“替换 frozen call config”的 waterfall，正好能在每次模型请求前改写 child 的 provider/model/effort。

**为什么不是 provider 包装**：包装 provider 会替换 provider 身份，影响计量/目录；`agent/request` 只改这次调用的配置，保留原 provider 与流。

**怎么识别 child**：`agents.roots()` + `agents.list()` + `agents.isOwnedBy(child, owner)`；只改“有活 owner 的 Agent”，顶层会话 `owners=[]` 直接放过。

**优先级（实现）**：本对话 owner 的 `sessions[id].default` → `global.default` → 无路由（继承）。README 写的 `presets` 层在 state 里存在但**从不读取**。

## 机制与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | `$DSH_HOME/plugin-data/subagent-models.json`，mtime 热加载 | 全 profile 共享一个文件；会话条目无淘汰；写失败仅 warn，内存先更新 |
| 冲突裁决 | 后写覆盖；串行 promise + tmp+rename | 多进程同时写仍可能互相覆盖（无锁） |
| 失败收敛 | 读坏回空 state；无 route 继承 | 路由模型不存在时不会回退——adapter 可能直接报错 |

**额外边界**：
- `routeApplies` 注释说“模型仍被广告才生效”，实现没有校验；目录只用于 UI 选项。
- 无 effort 时显式 `reasoningEffort: undefined`，可能清掉 preset 原来的 effort。
- `subagent_fork` 也会被覆盖；fork 共享父前缀，换模型会丢 KV cache。
- HTTP handler 无 token，依赖宿主对 `/plugin/*` 的防线（`[OPEN]`）。

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`Garybot126/dsh-subagent-models`](https://github.com/Garybot126/dsh-subagent-models) |
| **npm** | `dsh-subagent-models@0.1.2`（latest） |
| **版本(本次读)** | `0.1.2` @ commit `a105855`（无 tag；npm `gitHead` 同 SHA） |
| **License** | MIT |
| **安装** | `dsh plugin --profile <profile> add dsh-subagent-models`（README） |
| **接线** | `dsh.bundle.patch` → 一条 `insert: subagent-models`；`dsh.client`（web） |
| **依赖** | 无 `dependencies`/`peerDependencies`；`engines.dsh >=0.2.1-rc.2` |
| **数据** | `$DSH_HOME/plugin-data/subagent-models.json` |

## 借用指南

### 可借鉴

1. **改“调用配置”而不是改工具 schema**：`agent/request` 让同一个委派工具支持多模型，不用给工具加参数。
2. **只改被委派 child**：用 `isOwnedBy` 判归属，避免把顶层用户选择也覆盖。
3. **层级优先级**：本对话 → 全局 → 继承；对“按会话试模型”很自然。

### 别照抄

- 别把 README 的 `presets` 优先级当真：实现只读 `default`。
- 别省模型存在性校验：目录是 UI 的，不是 apply 时的 guard。
- 别把“写文件成功”当保证：写失败只 warn，刷新后可能回退。

## 证据与边界

| 主张 | 标签 | 来源/核对方式 | 边界 |
|---|---|---|---|
| 用 `agent/request` 覆盖 child 的 provider/model/effort | `[SRC-TARGET]` | [`15 memo`](../_证据/15-subagent-models-源码复核.md)（`index.js:247-255`） | 只改 config；不改消息/工具 |
| 只改被委派 child，顶层不动 | `[SRC-TARGET]` | 同上（`ownersOf/routeFor`） | `isOwnedBy` 运行时语义未逐行核 |
| 优先级实现为 session→global，presets 未用 | `[SRC-TARGET]` | 同上（`resolveRoute/routeFor`） | 与 README 不一致 |
| 状态文件与写入语义 | `[SRC-TARGET]` | 同上（`saveState`） | 无锁；写失败仅 warn |
| 无测试/无 CI/未运行 | `[TEST]`/`[CI]`/`[RUN]` | 仓库无 `.github`；未安装运行 | 行为未实测 |

**未验证**：`/plugin/*` 的宿主鉴权、真实 child 上 effort 不支持时的错误、fork 的 KV cache 影响，均 `[OPEN]`。
