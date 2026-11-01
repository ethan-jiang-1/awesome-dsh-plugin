---
title: "命令即验收面 · tool-guardian：没有卡片时的首启"
domain: lifecycle
kind: sample
positioning: "用一条会话内命令当唯一验收面：input 决定路由、未就绪与起失败要分开说、临时放行要能撤。"
takeaway: "命令不是界面的替代品，是首启的验收面；而 `input` 不是装饰——不写它，带参数的命令会被当成提问发给模型。"
read_when: "产品没有浏览器卡片；或要设计“装完怎么确认它在跑”。"
status: observed
updated: 2026-11-01
budget: 135
---
# 命令即验收面 · tool-guardian

> **阶段**：首启 · **载体**：command（+ host-row） · **兼看**：起
> **影响力**：npm 近 30 天 **2,701**（2026-11-01，42 个过影响力门的 bundle 之一）
> **研究范围**：`dsh-tool-guardian@0.9.1-beta.1`，gitHead `ec61be43…`，tarball sha256 `0b7f2987…`（189,410 B，27 文件）；DSH 对照 `0.2.1-rc.3`
> **证据成熟度**：源码级（命令注册、自检与返回形态实读；未实机运行）
> **一句话**：它没有客户端、没有面板，**唯一的用户面就是 `/toolguardian` 这一条命令**。
> **借鉴价值**：**① `input` 决定命令是给人还是给模型；② “还在启动”与“起失败了”必须分开说；③ 命令注册要放进可选的 `ctx.inject`。**

## 它想干什么 · 为什么值得借鉴

**意图。** 在工具调用离开宿主之前做一道守卫（后端路由、token 节省、更新检查），并给人一条随时能问"你现在什么状态"的命令 `[SRC-TARGET]`（`index.js:1045` 的 `USAGE`、`:1049` 的 `selftestReport`）。

**意义。** 生命周期里"首启"最尴尬的情形是：**产品没有界面**。它不能像面板那样"你自己看"，也不能像 doctor 那样另起一个进程。剩下的唯一入口是**会话里的斜杠命令**——而且这条命令必须同时回答"能不能用""为什么不能用""怎么临时放过"。

**用户价值。** 装之前，用户面对的是一个静默生效的守卫，出了问题只看到工具被拦；装之后，`/toolguardian selftest` 直接给出后端、token、更新的三元结论，`/toolguardian bypass 24h` 临时放行，`/toolguardian restore` 撤回 `[SRC-TARGET]`（`:1122-1124`）。

**表达。** 没就绪时的文案分两种 `[SRC-TARGET]`（`:1051-1053`）：

```js
'still starting -- try again in a few seconds'          // 还在起
`failed to start: ${bootError}`                          // 起失败了
```

**同一个 `kind: 'error'`，但用户能一眼看出该等还是该查。**

## 1. 阶段与载体

- **阶段**：首启。它回答"装完以后它在不在、能不能用"。
- **载体**：`command`（唯一用户面）+ `host-row`（守卫本体）。
- **兼看**：起。没就绪的两种状态是启动期的事。

## 2. 机制

```js
// index.js:1129-1137
ctx.inject(['commands'], (inner) => {
  inner.commands.register({
    name: 'toolguardian',
    description: 'Tool Guardian: selftest (backends, token saving, update) · bypass [last|24h] · restore',
    // Without `input` DSH treats a command as argument-free and sends "/toolguardian bypass" to the MODEL.
    input: { hint: '[selftest | bypass | bypass last | restore]' },
    handler: toolguardianCommand,
  })
})
```

三个点：

1. **`input` 决定路由，不是装饰**。注释写明：**没有 `input` 时，DSH 把命令当作"无参数"处理，于是 `/toolguardian bypass` 会被当成提问发给模型** `[SRC-TARGET]`（`:1134-1135`）。
2. **命令注册是可选能力**：`ctx.inject(['commands'], …)`，注释是 *a host without the command registry still gets the tools* `[SRC-TARGET]`（`:1127-1129`）。没有命令注册表的宿主照样能用工具，只是没法自检。
3. **注册是 effect**：插件卸载或热替换时命令自动注销 `[SRC-TARGET]`（`:1140` 注释）。

### 三条失败态

| 态 | 表现 | 用户看到什么 |
|---|---|---|
| **还在启动** | `ready === false` 且 `bootError === ''` | `still starting -- try again in a few seconds` `[SRC-TARGET]`（`:1052`） |
| **起失败了** | `bootError !== ''` | `failed to start: <原因>` + 建议去 DSH 日志搜 `tool-guardian` `[SRC-TARGET]`（`:1053`） |
| **命令没注册上** | 宿主没有 `commands` 服务 | 命令不可用，工具仍可用——**但用户不知道去哪自检** |

## 3. 设计取舍

| 取舍 | 选择 | 代价 |
|---|---|---|
| 用户面放哪 | 会话内命令，不做客户端 | 用户得记得命令名；换来零界面成本 |
| 自检与守卫的关系 | 同一进程、走同一个 bridge，而不是另起 doctor | 起不来时命令本身也起不来——所以文案必须说清"还没起" |
| 临时放行 | 命令式 `bypass [last\|24h]` + `restore` | 需要状态与到期逻辑 |
| 错误返回 | 统一 `{ kind, text }`，不抛异常 | 异常与"预期内的失败"混在一起时不好处理 |

## 4. 与宿主既有行的边界

它**不改宿主的工具列表**，只在调用链前后做判断；`restore` 还需要宿主侧 `allowRuntimeActivation: true` 才放行 `[SRC-TARGET]`（`:1120`）。这意味着"能临时放行"本身也是一个受控能力——**守卫自己也要被守卫**。

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 产品没有界面，首启怎么验收 | 用**一条会话内命令**当唯一验收面：自检 + 状态 + 临时放行三合一 | `[SRC-TARGET]` `index.js:1045`（USAGE）、`:1049`（selftest）、`:1122-1124`（bypass/restore） | 零界面成本、随时可问；代价是用户得记住命令 | 定义命令名、子命令与每种子命令的输出 | 只对"活在会话里"的产品成立 | 不给自检命令 → 用户只能猜它有没有生效 |
| 带参数的命令行为诡异 | 注册时写 `input.hint`；**不写 `input` 会被当成无参数命令发给模型** | `[SRC-TARGET]` `index.js:1134-1135`（注释与 `input` 字段） | 参数被当命令处理；代价是多一个字段要维护 | 每个带子命令的命令都写 `input` | 只对"把命令与提问分流"的宿主成立 | 不写 `input` → `/x bypass` 被当成提问发出去，用户以为命令坏了 |
| “起不来”与“还没起”混为一谈 | 同一种 `kind: 'error'`，但文本必须区分"还在起"与"起失败了+去哪儿看日志" | `[SRC-TARGET]` `index.js:1051-1053` | 用户知道该等还是该查；代价是文案要多写 | 给每个未就绪分支定义一句可执行提示 | 只对"有启动窗口"的产品成立 | 一律回 "not ready" → 用户反复重试，或直接卸载 |
| 宿主可能没有某个能力（如命令注册表） | 用 `ctx.inject(['commands'], …)` 注册，而不是静态 `inject` | `[SRC-TARGET]` `index.js:1127-1129`（注释：*a host without the command registry still gets the tools*） | 缺能力时降级而不是整行 pending；代价是自检面消失 | 把"锦上添花"的能力都走 `ctx.inject` | 只对支持 `ctx.inject` 的 loader 成立 | 静态 `inject` → 没有命令注册表的宿主整行 pending（`TRAPS` §11） |

## 6. 失效与开放问题

- `[OPEN]` `bypass 24h` 的到期实现与跨会话持久化（本卡只读到子命令与文案）。
- `[OPEN]` `restore` 依赖的 `allowRuntimeActivation` 默认值与风险（未读配置默认）。
- `[OPEN]` 命令未注册时插件是否有别的方式告知"你没有自检面"。
- `[OPEN]` 未实机运行（本机不装）。

## 7. 兼看

- 首启：与 [`first-run/41`](./41_自检即首启-dsh-skill-cockpit.md) 是一对——**41 用独立进程自检（宿主挂了也能跑），42 用会话内命令自检（活在同一进程里）**。选哪种取决于"你最需要诊断的是宿主还是插件"。
- 起：未就绪两态与 [`boot/README.md`](../boot/README.md) §1 的失败分级同源。
