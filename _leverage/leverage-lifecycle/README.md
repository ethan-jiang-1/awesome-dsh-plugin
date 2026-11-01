---
title: "leverage-lifecycle · 分发与首启：装一次，两个面都能用"
domain: lifecycle
kind: index
positioning: "第四册入口：DSH 原生分发链路怎么走、web 与 Desktop 为何必须同一句话、四阶段各自判据。"
read_when: "要发一个能被 dsh web 和 Desktop 同时用起来的插件或 bundle；或判断某个装法为何在另一面失效。"
status: living
updated: 2026-11-01
budget: 170
---
# `leverage-lifecycle/` · 分发与首启(第四册)

> **标语**:*Ship a bundle; install where you already are.* —— 发一个 bundle，在"你正在跑的那个界面"里装。
> **和前三册平级**：`leverage/` 问接缝，`leverage-agent-collaboration/` 问协作，`leverage-reshape-product/` 问产品形态；本册只问一件事——**从拿到它到第一次成功，中间那几步走哪条路才不会被用户当成"奇怪"。**

## 0. 一句话结论

> **定调（宪章 §0）**：分发、安装、启动**一律走 DSH 给出的那条路**；需要特别的东西，用 bundle 里的插件、流程和配置去实现，**不靠改宿主、也不靠另造一套分发**。本册每条判据都是这条的推论。

> **发一个声明了 `dsh.bundle.patch` 的包；让用户在应用内装（侧栏 Plugins 页）；`dsh plugin --profile web add` 只是 web 面的自动化等价物。**

> **DSH 立场**：本册每条做法都标了 `符合 / 有条件偏离 / 反例`；偏离的代价与退出条件集中在 [`REFERENCE` §4](./reference/REFERENCE.md)。

理由是一条机制事实，不是一个偏好：**应用内安装天生是"当前 profile 相对"的**，所以 `dsh web` 和 Desktop 是同一句话；而 `--profile <name>` 天生是"面绑定"的，写到文档里必然要写两条、也就必然错一条。证据与反例见 [`REFERENCE`](./reference/REFERENCE.md) §6。

## 1. 为什么单开一册

产品线那册回答"**装成什么形态**"（plugin / profile / shell）。它把安装、启动、配置、首启拆在 25 张样本卡的页头里，每张各写一句。够用来看单个样本，不够用来**发东西**：真到分发时，问题是横向的——同一道题，别人怎么答、DSH 原生怎么答、答错会坏成什么样。

**分析单位不同，所以独立成册**：这里的单位是**一个生命周期阶段**，不是产品样本、不是接缝、不是协作家族。和 2026-11-01 协作册从 `leverage/` 独立出来是同一个理由。

## 2. 四阶段

| 阶段 | 问什么 | 读哪篇 |
|---|---|---|
| ① 装 | 用户拿到你时，谁碰包管理器、装进哪个 profile、什么算"装上了" | [`install/`](./install/README.md) |
| ② 起 | 装完要不要重启、重启和刷新和 HMR 差在哪、起不来时坏在哪一层 | [`boot/`](./boot/README.md) |
| ③ 配 | 你的默认值和用户的覆盖分别住在哪、优先级怎么叠 | [`config/`](./config/README.md) |
| ④ 首启 | 第一次打开看到什么、原生给不给、不给的话你补哪一段 | [`first-run/`](./first-run/README.md) |

横切两篇：[`SURFACES`](./reference/SURFACES.md)（web 与 Desktop 的同一性与分叉点）、[`REFERENCE`](./reference/REFERENCE.md)（被认可的那一条路）。

## 3. 八条硬结论

每条都挂了标签，标注方式见 §5。

1. **应用内安装是"当前 profile 相对"的。** 包自述就是 *Current-profile plugin and bundle management shared by dsh CLI, Web and agent tools*，`installBundle(spec, options)` 没有 profile 参数，模型侧工具也没有。`[DSH]`
2. **`desktop` 从普通 CLI 双门禁闭。** 启动被拒（`profile "desktop" is managed exclusively by the Electron application`），`dsh plugin --profile desktop` 同样被拒；只有 Electron carrier 用程序化开关才能管理它。`[DSH]` `[RUN]`
3. **"装成功"有三个成功。** pnpm 成功 ≠ 依赖写入 ≠ 成层。**没声明 `dsh.bundle` 的包：退出码 0、依赖写进、roster 不变、只给一句 stderr 警告。** `[RUN]`
4. **启动不是全有或全无。** 单个 row 导入失败被隔离成 `warning: N entry did not activate`，进程照常服务。**所以"应用能开、我的功能没有"是一种合法终态**，退出码还是好的。`[RUN]`
5. **home 层（`$DSH_HOME/cordis.patch.yml`）跨 profile 生效，但不能供货。** 它能覆盖/禁用任意 profile 的行；插入一个本 profile 没装的包，真启动时报 `ERR_MODULE_NOT_FOUND` 且不阻塞服务。`[DSH]` `[RUN]`
6. **原生首启只有一道令牌门，没有向导。** 一条带 token 的 URL → 303 + 30 天 HttpOnly cookie → SPA；无 token 401。首启账本只提供"设置面板里的一串步骤"，不是"装完第一屏"。`[RUN]` `[DSH]`
7. **启动体验不必另造 launcher。** 首屏注入、预置会话、工作区都在 host 服务层（`webServer.tapIndex`、`agents.create`、`workspaceRegistry.create`），写在 bundle 里的插件即可，天然跨面。`[RUN]`

8. **机制做得对，不等于产品成立。** 本册唯一「机制过门、影响力不过」的样本放在 [`negative/91`](./negative/91_机制对但没人用-dsh-bootstrap.md)——它的机制值得抄，但它回答了用户不会问的问题。**门槛的意义就是承受这种误伤。**

### 3.1 15 张阶段样本 + 1 张反例落地后的五个跨样本发现

1. **"说明与包体不一致"是装阶段的结构性风险。** 四张装阶段的卡里，两张（`install/11`、`install/13`）是同一种错——**安装说明依赖的脚本没随 `files` 发布**，已进 [`TRAPS` 第 14 条](./practice/TRAPS.md)。`install/14` 是另一类（patch 的 `name` 是断言，不是重命名），别把两类混成 n=3 的"规律"。
2. **`input` 陷阱有两个互不相关的样本独立复现。** [`first-run/42`](./first-run/42_命令即验收面-dsh-tool-guardian.md) 与 [`boot/25`](./boot/25_装完还要一步-dsh-context-guardian.md) 都写明：不写 `input`，带参命令会被当成提问发给模型；后者还带了实机观察日期。**宿主侧已可核**：`dsh-client-ui-commands/lib/client.js:1661-1665` 在没有 `input` 且带参数时直接 `return void 0`，该行不再走命令通道——两个样本只是独立复现，不再是推理。
3. **"生效"的判断必须分三级证据：运行时观察 > manifest > 声明。** 市场把"装上了"拆成七态，先看 loader 实际在跑什么，再看 `dsh.profile.bundles` 预测什么，最后才看你的 patch `[SRC-TARGET]`（`dshmarket@1.73.6` `lib/verify.js:1-28`）；宿主启动也只把"观察到的失败"分级（bundle / row / 整体），`--dump-config` 则连模块都不 import（[`TRAPS` §10](./practice/TRAPS.md)）。**同一原则的三处落地：能被观察到的才算数。**
4. **把失败做成可读状态，是这些样本的共同设计。** 隔离单行给 `warning: N entry did not activate`；应用内装给 `restart-required` + `restartReason`；看门狗给 `recovered:false` + `error`；doctor 给六值状态（`--fix` 后多一个 `fixed`）。区别只在"失败被谁看见"——**能被查询的失败，才不会被用户误读成"没装好"。**
5. **冲突处理的共同点是"不悄悄覆盖"，但冲突对象不同。** [`first-run/43`](./first-run/43_预置工作区与自有会话-dsh-24pa.md) 换 id + 通知（会话预设冲突，历史保留）；[`config/32`](./config/32_三档接管-dsh-free-search.md) 让路不碰（值的所有权冲突）；[`boot/24`](./boot/24_事务式修复-dsh-doctor.md) 降级为人工（故障行与救生链冲突）——**共同点是都拒绝悄悄覆盖；它们不是一个轴上的三档。**

## 4. 怎么读

| 我要… | 先读 |
|---|---|
| 手上有具体需求，不想通读 | [`BORROW`](./BORROW.md)（按需求路由 + 七条“别抄”） |
| 直接拿一条能写进 README 的装法 | [`REFERENCE`](./reference/REFERENCE.md) §2 |
| 搞清 Desktop 为什么和 web 不一样 | [`SURFACES`](./reference/SURFACES.md) |
| 给自己产品做发布前自检 | [`practice/CHECKLIST`](./practice/CHECKLIST.md) |
| 查"我这个写法为什么会坏" | [`practice/TRAPS`](./practice/TRAPS.md) |
| 看某条结论凭什么 | 各篇内的标签 → [`_证据/01`](./_证据/01_DSH-源码定位.md) · [`_证据/02`](./_证据/02_隔离实测记录.md) |

## 5. 证据与实测环境

| 标签 | 含义 |
|---|---|
| `[DSH]` | 上游发行物内可核，写到包 + 文件:行号（本册基线 `@deepseek-ai/dsh@0.2.1-rc.3`） |
| `[RUN]` | 本轮隔离实测，环境见下；只证明该环境下的行为 |
| `[PKG]` | npm 包清单事实：包名 + 版本 + 字段（如 `dsh.bundle` / `dsh.client`），不证明行为 |
| `[CARD]` | 引自产品线 25 张样本卡，按该卡页头标注的证据成熟度计，不升级 |
| `[SRC-TARGET]` | 样本卡 / memo 专用：第三方源码，包名 + 版本 + 文件:行号 |
| `[DOC]` | 样本卡 / memo 专用：README/文档主张，写清哪一节 |
| `[OBS]` | 观察者判断，必须带反例或失效条件 |
| `[OPEN]` | 未复核 |

**实测环境**：macOS · Node `v22.23.1` · pnpm `12.5.1` · `@deepseek-ai/dsh@0.2.1-rc.3` · **隔离 `DSH_HOME`**（`.work/feas/home`）。全过程未触碰真实 `~/.dsh` 的 profile、凭据与会话。

**样本卡的证据级别**：**5 张已到实测级**——[`install/11`](./install/11_装后自证-cfbridge.md)、[`install/12`](./install/12_让安装器认你-dsh-origin-plugin.md)、[`install/13`](./install/13_三条安装路径与空安装器-dsh-free-models-hub.md)、[`boot/21`](./boot/21_启动期注入-dsh-rhine-splash.md)、[`config/31`](./config/31_全禁状态-dsh-isolation-gate.md)；其余 10 张阶段样本为源码级；另有 [`negative/91`](./negative/91_机制对但没人用-dsh-bootstrap.md) 反例一张（源码级，不计入四阶段样本）。实测记录见 [`_证据/03`](./_证据/03_样本实测记录.md)。

**Desktop 面是源码级**：本机无 `desktop` profile、无 Electron 应用，Desktop 相关结论一律按 `[DSH]` 计，不冒充实测。这条边界写在 [`SURFACES`](./reference/SURFACES.md) 页头。

## 6. 与前三册的边界

- **与 `leverage-reshape-product/`**：那边按产品样本立卡，回答"该发插件、发 profile 还是发应用"；本册不重复样本机制，只把 25 张卡里散落的装卸配首**按阶段重排**，并补上它们共同缺的那一段——**DSH 自己的第一次安装**。
- **与 `leverage/`**：门禁与权限的机制深度归它；本册只引用结论，不重做机制分析。
- **与 `leverage-agent-collaboration/`**：无交叉。
- **共享文件只读**：`../leverage/README.md`、产品线各骨架由别的会话维护，本册只调用。

## 7. 校验

```sh
node _leverage/verify.mjs
```

`_leverage/verify.mjs` 是自包含校验器，只读 `_leverage/` 这棵树。本册纳入它的五件事：严格 UTF-8 / LF / 结尾换行、相对链接与页内锚点、frontmatter 契约（`domain` 固定 `lifecycle`、`kind` 合法、`playbook`/`sample` 必须有 `takeaway`）、样本卡的「它想干什么」节、第 5 节七列表头、DSH 立场行，以及同目录固定版本 memo 是否存在。它**不判断**结论是否成立——那是 [`_证据`](./_证据/02_隔离实测记录.md) 与人工复核的事。
