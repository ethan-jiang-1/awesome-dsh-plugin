---
title: "FIRST-RUN · 阶段④：第一次打开看到什么"
domain: lifecycle
kind: playbook
positioning: "原生首启只有令牌门与一个单步账本；四家样本怎么补，以及补在法律上归谁。"
takeaway: "原生不提供“装完第一屏”：令牌门之后直接是空界面，首启必须由产品自己回答。"
read_when: "要设计首次体验；或判断能不能复用 DSH 的原生首启账本。"
status: living
updated: 2026-11-01
budget: 160
---
# 阶段④ · 首启

## 1. 原生怎么做

**原生首启 = 一道令牌门，然后是空界面。** 没有欢迎页、没有向导、没有"装什么"的推荐。

**令牌门**（实测 `[RUN]` E9–E11）：

| 步骤 | 观察 |
|---|---|
| `dsh --profile web` 启动 | 打印 `dsh web: http://127.0.0.1:<port>/?token=<...>` |
| 无 token 直接访问 | `401`，纯文本："dsh web authentication required; reopen the URL printed by dsh web." |
| 带 token 访问 | `303` + `set-cookie: dsh-auth-…`（30 天、HttpOnly、SameSite=Strict）→ 重定向 `./` |
| 带 cookie | `200`，SPA 外壳（实测 37,907 字节），含 `globalThis["__DSH_BOOT__"]` 与若干 `__DSH_*__` 页面全局 |

首屏注入的页面全局里有 `__DSH_MODELS_ONBOARDING__ = {"credentialOnboarding":true}`——**它是一个标记，不是界面**。

**握手会留下一条持久授权**：跑完一次 token 换取后，隔离 home 下出现 `.credentials.yaml`，内含 `client-connection/browser-session` 的 `kind: grant` 记录 `[RUN]`。所以"每次都重新点 URL"并不是必需的——30 天 cookie 与这条 grant 是配套的。这也解释了为什么救生页/中转进程只需要在握手前介入。

**首启账本**（`settings.onboarding`）能力与边界 `[DSH]`：

- 列表槽，按 `order` **升序**投影，**一次只挂一个 step**（`dsh-client-ui-settings-general/lib/client.js:1169-1183`、`:489-496`）；
- **宿主自带两个**：`welcome-notice`（`order: -100`，**Desktop 里不注册**）与 `deepseek-official`（`order: 0`，模型登录）（`dsh-client-ui-settings-models/lib/client.js:4502-4515`）；
- 它只是"设置面板里的一串步骤"，**不保证抢到首屏**；完成或跳过把所有权交给下一个 `[CARD]`。

**另有 `OPTIONAL_BUNDLES`**：12 个出厂自带但默认关闭的实验 bundle，由插件管理器以"关着"的形式提供 `[DSH]`（`dsh-app-boot/lib/index.js:575-590`）。这是原生离"再装点什么"最近的东西，但它是开关，不是推荐。

## 2. 实测读到什么

- 全新 profile 的第一次启动**没有任何引导**：URL → cookie → 空会话界面 `[RUN]`。
- 首屏 HTML 里与首启有关的只有 `__DSH_MODELS_ONBOARDING__` 这一个标记 `[RUN]`。
- 因此"第一次看到什么"完全由**已安装的 bundle 与客户端插件**决定——即由产品自己决定。

## 3. 样本怎么偏离

25 张卡里，真正做了首启的只有四家 `[CARD]`：

| 样本 | 做法 | 能否推迟 |
|---|---|---|
| `shell/14` 终端即产品 | 四步向导（凭据 / 语言主题 / 模型+工作区 / 快捷键）+ 落地页 + `/setup` 重跑 | 可重跑 |
| `shell/15` 终端工作区 | 欢迎页 + 无 Provider 时三个出口 + Esc 推迟且保留草稿 | **可推迟，且不丢已输入内容** |
| `shell/12` 单文件桌面壳 | 启动页五跳候选链 + 全空时五个出口 | 可选择 |
| `61` 多端与远程 | 网卡确认 → 自动证书 → 重启 → 配对码（43 位、带有效期） | 可关掉网关 |

**没有一家用原生账本。** 唯一深挖过它的是产品线的观察样本 `04_首启观察-dsh-bootstrap`，结论是**故意绕开**，理由是账本是"设置面板里的步骤"，扛不住"装完第一屏" `[CARD]`。

**四种可抄的形态，代价各不同**：

| 形态 | 适合 | 代价 |
|---|---|---|
| 用原生账本 | 你的首启只是"配一个凭据/选一个模型" | 一次只挂一个 step；抢不到首屏；Desktop 少一步 |
| 自建设置页 + 引导 | 首启有多个决策 | 自己管完成状态、幂等、可重入 |
| 无感（默认值就够好） | 你的产品开箱即用 | 用户不知道你能干什么 |
| 阻塞式向导 | 不配就不能用 | 必须给"稍后再说"的出口，否则用户直接关掉 |

**本册样本补充**：三种"没有浏览器向导"的做法——

[`41`](./41_自检即首启-dsh-skill-cockpit.md) 独立进程自检（宿主挂了也能跑）·
[`42`](./42_命令即验收面-dsh-tool-guardian.md) 会话内命令（`input` 决定路由）·
[`43`](./43_预置工作区与自有会话-dsh-24pa.md) 直接摆好工作区与会话（冲突时换 id，不覆盖）。

## 4. 三条判据

1. 你有没有回答"第一次打开看到什么"？没回答就是交给用户猜。
2. 你的首启**能不能推迟**？不能推迟的首启，等于把未配置状态变成死路。
3. 你的首启**在 Desktop 上还成立吗**？依赖 `welcome-notice` 的必须给替代路径（见 [`SURFACES`](../reference/SURFACES.md) §3）。

## 5. 失效与开放问题

- `[OPEN]` 首启账本在真实 profile 中的渲染顺序与"跳过"后的持久化（本册只读源码，未在浏览器里点）。
- `[OPEN]` Desktop 上 `welcome-notice` 缺失后，`deepseek-official` 是否仍然成为第一步。
- `[OPEN]` 客户端能否感知"这是首次运行"（本册未找到原生 API；样本多是自建标志位）。

## 6. 启动体验的载体：不另造安装器

> 想要一个自己的"打开就是这样"的体验，除了自带 launcher，还有一条更便宜的路：**在 bundle 里放一个 host 插件**。launcher 是最后手段，不是第一手段。

| 想要的效果 | 原语（`ctx.*`，web profile 里都在） | 证据 |
|---|---|---|
| 首屏注入一段 | `webServer.tapIndex(html => …)` | `[RUN]` 探针注入的标记出现在真实首屏 |
| 自定义页 / 路由 | `webServer.register(route)`、`registerFallback(handler)` | `[DSH]` 契约 |
| **另起一个会话** | `agents.create({ sessionId, meta: { cwd, agentPreset }, seed })` | `[RUN]` 会话真的落盘到 `sessions/<cwd 编码>/<id>/` |
| 工作区 | `workspaceRegistry.create(path, title)`、`workspaceController.initializeDefault()` | `[RUN]` 目录不存在会 `ENOENT: realpath` |
| 会话目录 | `workingDirectory.set(agent, path)` | `[DSH]` 契约 |
| 命令入口 | `commands.register(...)` | `[DSH]` 契约 |
| 首启配凭据 | `credentials.set(...)`、`authorization.begin(...)` | `[DSH]` 契约 |

**升级顺序**（越往后越强，也越容易让用户不安）：命令 → 一块界面 → 首屏注入 → 启动时自动建会话。**用户什么都没点，桌上就多出一个会话**，比"少一个功能"更难解释。

**三条纪律**：一次（durable 完成标记）／可重入（留 `/setup` 或设置页入口）／可退出（不阻塞，Esc 或"稍后"）。

**一个实测出来的坑**：静态 `inject` **没有"可选依赖"写法**——数组或对象形式里的每个键都是**必需**服务。写成 `inject: { optional: ['webServer'] }`，宿主会去找一个叫 `optional` 的服务，行停在 `pending`，而启动摘要只说"did not activate"，很容易误判成代码坏了。要选择性依赖，用 `ctx.inject([...], callback)`，或者干脆不声明、运行时 `ctx.get()` 取。详见 [`TRAPS`](../practice/TRAPS.md) §11。

## 样本

| 文件 | 一句话 |
|---|---|
| [`41_自检即首启-dsh-skill-cockpit.md`](./41_自检即首启-dsh-skill-cockpit.md) | 用 doctor 退出码当首启验收面，用测试锁住文档。 |
| [`42_命令即验收面-dsh-tool-guardian.md`](./42_命令即验收面-dsh-tool-guardian.md) | 没有卡片时，一条会话内命令就是全部验收面。 |
| [`43_预置工作区与自有会话-dsh-24pa.md`](./43_预置工作区与自有会话-dsh-24pa.md) | boot 时把工作区与会话摆好，冲突时换 id。 |
