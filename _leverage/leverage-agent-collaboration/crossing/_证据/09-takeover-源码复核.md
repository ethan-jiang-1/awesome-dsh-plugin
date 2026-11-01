---
title: "09 · IKEASven69/dsh-takeover 源码复核"
domain: agent-crossing
kind: evidence
positioning: "对 dsh-takeover 0.4.3 工作树的固定提交复核：takeover 只新建宿主会话并投递 /resume-*，不夺进程、端口、profile 或 UI；npm 404 且 tag 与版本错位。"
read_when: "核对 09 卡 takeover 的替换对象、回滚与权限边界，或复核版本 pin 与 npm 状态。"
status: observed
updated: 2026-11-01
---

# 09 · `IKEASven69/dsh-takeover` 源码复核

> 复核对象：样本卡 [`09-IKEASven69-dsh-takeover.md`](../samples/09-IKEASven69-dsh-takeover.md)。
> 取证时点 2026-11-01。只读 GitHub REST、npm registry 与 codeload tarball；**未安装、未构建、未运行 `npm test`、未启动宿主或插件**。标签沿用 [`EVIDENCE.md`](../../EVIDENCE.md)：`[DOC]` 目标仓 README/CHANGELOG/THREAT-MODEL 主张，`[SRC-TARGET]` 固定 commit 实现，`[SRC-DSH]` 本机 `@deepseek-ai/dsh 0.2.1-rc.3` 发行包，`[TEST]` 测试源码，`[CI]` 同 SHA check-run，`[RUN]` 本轮实跑，`[OBS]` 判断。
> **主 pin**：commit [`afbc55cb4e076d885a50c2037515f16d008cac59`](https://github.com/IKEASven69/dsh-takeover/commit/afbc55cb4e076d885a50c2037515f16d008cac59)（`main` HEAD，2026-10-31T04:44:32Z，`package.json` 0.4.3）。**tag `v0.4.3` 不是这棵树**（→ `cf391a0`，自述 0.4.2，见 Provenance）。下文目标代码链接全部 pin `afbc55c`。
> 一句话结论：**「takeover」替换的是「会话」，不是进程、端口、profile 或 UI**——它在同一宿主进程里新建一个会话、改名、queue 一条 `/resume-<provider> <id>`（或 `/inbox`）指令；外部 agent 的会话只被只读读取，原进程与端口从未被碰过。卡片把这套机制写成「跨进程/跨机」的接力总线，方向对，但**全卡没有一句定义替换对象**，版本坐标也未 pin。

## Provenance

| 项 | 值 | 核对方式 |
|---|---|---|
| 仓库 | [`IKEASven69/dsh-takeover`](https://github.com/IKEASven69/dsh-takeover)（repo id `1399099937`，创建 2026-10-01，MIT，0★ / 0 fork / 0 open issue @2026-11-01） | `/repos` |
| **主 pin** | `main` @ [`afbc55c`](https://github.com/IKEASven69/dsh-takeover/commit/afbc55cb4e076d885a50c2037515f16d008cac59)（2026-10-31T04:44:32Z，`fix: .gitattributes 豁免二进制 sqlite 语料…`）；tarball 解包只读复核 | `/commits`、codeload |
| package.json 版本 | **`0.4.3`**（[package.json:3](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/package.json#L3)）；`main: ./lib/index.js`（[package.json:6](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/package.json#L6)） | 同上 |
| **npm 发布状态** | **不存在**：`registry.npmjs.org/dsh-takeover` → **404**，`registry.npmmirror.com/dsh-takeover` → **404**（2026-11-01 实取）；无 npm 侧 `gitHead` 可比 | registry HTTP |
| tag 列表 | `v0.4.3`→`cf391a0`、`v0.4.2`→`9d56515`、`v0.4.1`→`2e53639`、`v0.4.0`→`0627fdc`、`v0.2.1`→`df44c8d`、`v0.2.0`→`6b61f95`；`v0.4.3` 是**轻量 tag**（ref 直接指向 commit） | `/tags`、`/git/ref/tags/v0.4.3` |
| **tag `v0.4.3` 的树** | `package.json` = **`0.4.2`**、CHANGELOG 顶条 = `[0.4.2]`、`src/` 无 `signing.ts`；**下一个提交** `47b3b48`（2026-10-28T13:28:25Z，`0.4.3 居中模态版`）才把 version 改成 `0.4.3` | tag tarball vs `47b3b48` 的 package.json |
| **HEAD 的树** | `package.json` = `0.4.3`，但已含 **`0.4.4 功能批`** 提交 `3a6404f`（2026-10-29，`src/signing.ts` 等）；tag 之后共 11 个提交，`0.4.3` 的 version 串从 `47b3b48` 起；CHANGELOG 顶条仍是 `[0.4.3]`，**没有 0.4.4 条目、也没有 0.4.4 版本号** | CHANGELOG 顶条、`diff -rq` 两棵树 |
| 签名 | commit `verification = {verified:false, reason:"unsigned"}`；tag 是轻量 tag，无 tag 对象签名 | `/commits/afbc55c` |
| 卡片版本核对 | 卡片 L46 写 `0.4.3`，与 **HEAD 树**一致；**不指向任何 tag**。`PANEL_VERSION = 'v0.4.3'` 是客户端手写常量（[src/client.ts:2452](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/client.ts#L2452)），不是构建期注入 | 源码 |

**错位结论（这是本卡最实的坐标问题）**：npm 侧根本没有发布物，所以 `npm ↔ tag ↔ commit` 三坐标**无法对齐**；能对齐的只有「工作树自述版本」与 commit。tag `v0.4.3` 指向的是 **0.4.2 的树**（version 串在下一个提交 `47b3b48` 才变成 `0.4.3`），HEAD 树自述 0.4.3 却已装进 0.4.4 的功能提交。因此卡片写「版本(本次读) 0.4.3」时，读到的既不是 npm 版本（不存在），也不是 tag（0.4.2），而是 `47b3b48..afbc55c` 这段工作树；**不 pin commit 就无法复现**。

## DOC

`[DOC]` 只证明作者主张，不证明实现。

- 名字的来源写得明确：「**为什么叫 takeover？** takeover = 接管：别的 agent 干到一半的会话，你随时接管接着掌控」——[README.md:7](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/README.md#L7)。同一句把「接管」限定在**会话**层，不是进程层。
- 一键接管的产品描述：「点「接管」**直接新建会话投递指令并自动切换过去**看模型接手；失败自动退回复制指令」——[README.md:15](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/README.md#L15)。
- 权限范围自述：「写 `~/.handoff/`（可用 `HANDOFF_HOME` 覆盖）、读 git 状态、**只读**九家 agent 的本地会话库（zcode 与 cursor store 走 sqlite readonly）……**不访问网络，不复活外部进程，不回放历史工具调用，原文不进卡片**」——[README.md:118](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/README.md#L118)。
- UI 位置：「**每个会话输入框的工具行里**有一枚「接力」按钮……点开向上浮出双栏工作台」——[README.md:114](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/README.md#L114)。
- 安装串：`dsh plugin --profile web add github:IKEASven69/dsh-takeover`——[README.md:78](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/README.md#L78)；`lib/` 产物已入库、无需构建（[README.md:77](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/README.md#L77)）。
- 信任边界自述：「本机用户态进程与盘上文件**默认可信**；跨机场景的信任 = 同步盘的信任」；T6「端口与网络面」的防线是「连接级回环闸 + Host 回环校验 + 同源守卫；**插件不发起任何网络请求**」——[THREAT-MODEL.md:16](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/THREAT-MODEL.md#L16)、[THREAT-MODEL.md:90-96](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/THREAT-MODEL.md#L90-L96)。
- `[DOC]` **没有**任何一句声称接管进程、端口或 profile；卡片也没写。「跨进程/跨机」是卡片的域框架，不是作者原话。

## SRC-TARGET

### 1. 「接管」到底替换什么

| 候选 | 是否被替换 | 实际行为 | 依据 |
|---|---|---|---|
| 宿主进程 | **否** | 不 spawn、不 signal、不 kill；新会话跑在**同一个**宿主进程里 | `src` 无 `child_process`/`spawn`/`kill`（grep 仅 `process.pid` 用于临时文件名） |
| 端口 / listener | **否** | 不 `listen`；只在宿主已有 listener 上登记 `/dsh-takeover` 前缀路由 | [server.ts:332-338](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L332-L338) |
| profile | **否** | 不改 profile/bundle；安装是用户的 `dsh plugin` 动作 | [cordis.yml:1-6](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/cordis.yml#L1-L6) |
| UI | **否（叠加）** | 在 composer 工具行登记一枚 chip、设置页登记一张卡；打开时覆盖全屏遮罩；成功后调宿主 `openSession` **切到**新会话 | [client.ts:2716](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/client.ts#L2716-L2722)、[client.ts:2739-2746](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/client.ts#L2739-L2746)、[client.ts:2511](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/client.ts#L2511) |
| **会话** | **是（新建，不替换旧的）** | `create({})` → `rename` → `prompt(queue)` | [server.ts:256-269](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L256-L269) |
| 外部 agent 会话 | **否** | 只读适配器读元数据/正文；原文不进 POST；不写对方存储 | [README.md:118](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/README.md#L118)、[foreign.ts:445-476](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/foreign.ts#L445-L476) |

### 2. 接管的三个宿主调用（投递核心）

- `admitTakeover(controller, args)` 是纯函数化核心（可脱离 cordis 单测）：先按 mode 生成**指令字符串**与标题（`take`/`take_deposit` 走 `foreignResolveOne` 解析引用，`inbox` 只需要卡 id）——[server.ts:226-253](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L226-L253)。
- ① `controller.create({})`，**不传 cwd / workspaceId / preset**（[server.ts:256](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L256)）；缺 `sessionId` 回规范错误（L257-260）。
- ② `controller.rename({ sessionId, title })`，标题 `接管：<原标题>（MM-DD HH:mm）` 截到 48 字（[server.ts:262](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L262)、[server.ts:199](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L199)）。
- ③ `controller.prompt({ requestId, sessionId, mode:'queue', content:[{type:'text',text:instruction}] }, new AbortController().signal)`（[server.ts:264-269](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L264-L269)）。**投递的是一条 slash 指令**，不是会话正文：`/resume-${provider} ${id}`（[browser-view.ts:66-69](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/browser-view.ts#L66-L69)）或 `/inbox`（[server.ts:231-234](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L231-L234)）。
- 正文读取发生在**新会话里**：`/resume-*` 技能调 `foreign_session_read`，经只读适配器读外部库；`admitTakeover` 只解析引用（元数据层），不把外部正文放进 POST/指令。
- **cwd 不继承**：`create({})` 不给 cwd，所以新会话落在宿主默认工作区；技能自己要求「确认当前 DSH 工作目录与仓库根」，cwd 为空时先问用户（[resume.ts:155-157](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/skills/resume.ts#L155-L157)）。**「接管」传的是上下文，不是工作目录**——卡片未提这一点。
- 投递后：`writeRelayProvenance` 写 `<HANDOFF_HOME>/relay/<sessionId>.json`（[server.ts:282](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L282)），再后台尽力追加宿主 plugin record（[server.ts:285-295](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L285-L295)）。

### 3. 原进程/端口是怎么「取得」的：没有取得

- `src/` 里没有 `listen`、`createServer`、`net`/`http` 服务端代码，也没有读 pid/端口、探测占用、发信号的路径；唯一与进程相关的是 `process.pid` 用于临时文件名（[settings.ts:54](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/settings.ts#L54)）。
- 它「取得」的是**宿主能力**，不是进程/端口：① `ctx.inject(['webServer'])` + `host.effect(() => host.webServer.register({kind:'prefix', path:'/dsh-takeover', handler}))`（[server.ts:332-338](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L332-L338)）；② 从 root `ctx` 防御式取 `sessionController`（`create/rename/prompt` 三方法齐备才用，[server.ts:174-191](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L174-L191)）；③ 只读九家本地会话库。
- 前缀下挂 **10 个子路径**：`state`、`sessions`、`session-preview`、`takeover`、`send`、`memory-scan`、`memory-push`、`provider`、`clear-archived`、`dismiss-pending`（404 文案只列了 7 个，[server.ts:631](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L631)）。
- **前一个 listener 会怎样**：不存在「接管/顶掉」路径。宿主 `webServer.register` 对重复 `(kind,path)` **直接抛错**（[SRC-DSH] `dsh-host-webserver/lib/index.js:328`），所以同前缀冲突的真实后果是**后加载的插件 apply 失败**，原 listener 与已注册路由原样保留。宿主端口由宿主 `listen(config.port, config.host)` 绑定（`dsh-host-webserver/lib/index.js:468-474`）；插件从不触碰。
- **UI 也不是替换**：`inject = ['slots','locale']`（[client.ts:189](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/client.ts#L189)），登记 `conversation.input.activity` chip 与 `settings.section` 卡；打开面板时是 fixed 遮罩 `zIndex 9998/9999`（[client.ts:2511](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/client.ts#L2511-L2528)），关掉即还原；「自动切过去」是 `uiWorkspace.openSession(sessionId)`（[browser-view.ts:232-245](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/browser-view.ts#L232-L245)、[client.ts:1774](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/client.ts#L1774)），属于宿主 UI 导航，不是接管 UI。

### 4. 回滚 / 恢复：没有自动回滚

- `create` 成功、`rename`/`prompt` 失败时，**已建会话不会被删**：错误值带上孤儿 `sessionId` 并明说「可在会话树删除」（[server.ts:297-303](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L297-L303)）。整个 `server.ts` 没有删除会话的调用，`SessionControllerLike` 也只声明了 `create/rename/prompt` 三方法（[server.ts:159-169](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L159-L169)）。
- 客户端失败路径 = **把同一份指令复制到剪贴板** + 原因横幅（[client.ts:1780-1790](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/client.ts#L1780-L1790)），语义不降级（按钮与手动粘贴同源）；这是 fallback，不是 rollback。
- 卸载/停用时只有路由被 dispose（`host.effect` 的 disposer，[server.ts:333](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L333-L338)）；**已建会话、已写 relay 记录都不撤销**。
- 外部侧无需恢复：只读读取，原进程与对方存储从未被写（README:118）。
- 文件侧不可逆点：取件即 `pending → archived`（消费即弃），archived 只滚动保留 **50** 份，超出按 mtime 删除（[core dist:476](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L476)、[core dist:631-650](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L631-L650)）。

### 5. 权限 / 授权边界

- **传输面**：连接级回环闸先行——`socket.remoteAddress` 非 `127.0.0.1`/`::1` 一律 403（[server.ts:81-85](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L81-L85)、[server.ts:341-344](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L341-L344)）；写路由过 `sameOrigin`（Host 必须回环 + Origin 与 Host 同值，[server.ts:93-103](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L93-L103)、[server.ts:415-418](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L415-L418)）；读路由过 `readGuard`（`Sec-Fetch-Site` 非 cross-site，[server.ts:108-113](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L108-L113)）；JSON body 上限 4 KiB（[server.ts:116-146](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L116-L146)）。
- **没有 token / 会话凭据**：路由是裸 handler，宿主 webServer 不提供鉴权层（[SRC-DSH] `dsh-host-webserver/lib/index.js:321-334`）。Host/Origin 都是客户端可写的头，**本机任意进程**（curl 之类）可以伪造两者通过守卫——这与作者自述的信任边界（本机用户态进程可信）一致，但意味着「同源守卫」防的是浏览器跨站/DNS rebinding，不是本机进程。
- **文件面**：写只落 `<HANDOFF_HOME>`——`config.json`（[settings.ts:26-27](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/settings.ts#L26-L27)、原子 tmp+rename [settings.ts:49-64](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/settings.ts#L49-L64)）、`relay/<sessionId>.json`（[relay-records.ts:35-45](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/relay-records.ts#L35-L45)）、`lifecycle.jsonl`（[lifecycle.ts:56-57](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/lifecycle.ts#L56-L57)）；外部库只读（sqlite `{readOnly:true}`，[readers dist:424](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/readers/dist/index.mjs#L424)、[readers dist:624](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/readers/dist/index.mjs#L624)、[readers dist:1246](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/readers/dist/index.mjs#L1246)），`foreign.ts` 无写调用。路径可被 `HANDOFF_ROOT_<家>` 覆盖（README:118）。
- **宿主能力面**：`sessionController` 是宿主 root 服务，插件**不经工具审批面**直接建会话 + 投递 prompt；宿主把这次 prompt 记为 `source.kind='user'` 的用户消息（[SRC-DSH] `dsh-api-session-controller/lib/index.js:3218-3231`）。也就是说，**注入指令与会话日志里的用户手打消息同源**，只有插件自己写的溯源（relay 文件 + 会话日志里的 plugin record）能区分来源。这是上游契约（任何同 profile 插件都能拿到该服务），不是本插件私开的洞。
- 停用闸：provider 在设置里被停用时，`takeover` 与读路由同口径拒绝（[server.ts:328](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L328)、[server.ts:442](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L442)）。

### 6. 崩溃 / 断连行为

- **浏览器中途断连**：handler 没有 `request.on('close')` 中止逻辑；`create/rename/prompt` 一旦发出就继续完成，响应写失败被忽略。断连不会回滚已建会话。
- **宿主在 create 与 rename/prompt 之间崩溃**：留下一个默认标题的会话；relay 溯源未必写（写盘在 prompt 之后），下次启动**没有清理**逻辑。
- **溯源写盘不是原子写**：`writeFileSync` 直写 JSON（[relay-records.ts:40-48](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/relay-records.ts#L40-L48)），崩溃可能留半截文件；对比 `config.json` 走 tmp+rename（settings.ts:49-64）。溯源失败不影响投递（best-effort）。
- **后台 plugin-record 追加**：最多 **24 × 5s ≈ 120s** 轮询 `sessions.get(sessionId)`，拿不到就静默放弃（[server.ts:285-295](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L285-L295)）；该 `setTimeout` 未 `unref`，最长 120s 内持续持有定时器（宿主本就长活，只在关停时可见）。
- **重试/幂等**：只有 5 秒同键去重（`mode|provider|reference`，[server.ts:331](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L331)、[server.ts:436-451](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/server.ts#L436-L451)）；超过 5 秒的重复点击会**再建一个会话**。
- **收件箱取件崩溃**：认领文件 `.claim` 在 `finally` 删（[core dist:576-628](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L576-L628)）；认领到 rename 之间崩溃会留 claim，卡留在 pending，后续取件报「正在被另一个进程取件」，直到某次**列目录**触发清扫且 mtime > 60s（[core dist:500-519](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L500-L519)）。
- **实时性**：面板 30s 轮询 `/dsh-takeover/state`（[client.ts:2124-2132](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/src/client.ts#L2124-L2132)），无推送/无回执通道。

### 7. 状态归属

| 状态 | 所有者 | 位置 | 生命周期 / 依据 |
|---|---|---|---|
| 交接卡 pending/archived | 插件（任何本地写者都能投递） | `$HANDOFF_HOME/{pending,archived}` | 消费即弃；archived 滚动 50 |
| provider 开关 | 插件 | `$HANDOFF_HOME/config.json` | tmp+rename 原子写（settings.ts:26-27, 49-64） |
| 生命周期事件 | 插件 | `$HANDOFF_HOME/lifecycle.jsonl` | append-only，尾 500（lifecycle.ts:56-57） |
| 接力溯源 | 插件 | `$HANDOFF_HOME/relay/<sessionId>.json` | 整文件覆盖，best-effort（relay-records.ts:35-48） |
| **新会话 / 标题 / 消息日志** | **宿主** | 宿主 session store | 插件只经 `sessionController` 改；删也由用户在会话树删 |
| 会话日志内的 relay record | 宿主（plugin record） | 宿主会话日志 | 增益层，尽力追加（server.ts:285-295） |
| 外部 agent 会话库 | 外部 agent | 九家各自目录 | 只读，不写、不复活进程 |
| HTTP 端口 / 路由表 | 宿主 webServer | 宿主 listener | 插件只登记前缀，重复即抛（SRC-DSH） |
| UI seat | 宿主 renderer | 客户端 slot 表 | 插件登记 `conversation.input.activity` / `settings.section` |

### 8. 卡片「恰好一次」逐条复核（对象是 vendored dist，不是 core 源码）

卡片 L26/L57 的顺序与三条性质**成立**，但证据等级要降一档：本仓库**没有 `@agent-handoff/core` 的源码**，只有 `vendor/@agent-handoff/core/dist/index.mjs`（package.json 声明 0.1.0）与 `.d.mts`；因此下列行号是**已编译产物**的行号，不能证明与 core 源仓一致（[OPEN]）。

- 顺序 `assertSafeId → 8 MiB 尺寸闸 → open(claim,'wx') → render → rename → finally rm(claim)`：逐行成立（[core dist:576-628](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L576-L628)）；`wx` 在 [core dist:584](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L584)，`finally` 在 [core dist:624-628](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L624-L628)。
- 「同名归档内容相同 = 幂等吸收」：成立（[core dist:600-609](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L600-L609)）；不同则先写 `.conflict-HHMMSS[-n].md` 再 rename（[core dist:611-617](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L611-L617)）。
- **精度 1**：claim 打开失败**不区分 errno**，`catch` 一律报「正在被另一个进程取件」（[core dist:583-587](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L583-L587)）——EACCES/ENOSPC 也会被说成并发。
- **精度 2**：60s 是 `CLAIM_STALE_MS = 6e4`（[core dist:502](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L502)）与 mtime 判据（[core dist:516](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L516)）；清扫只在 `listDirCards` 列目录时触发（[core dist:526](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L526)、[core dist:505-519](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L505-L519)），**不是 60s 定时器**。
- **精度 3**：8 MiB 闸只在**读侧**（`loadCard` / `listDirCards`：[core dist:478](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L478)、[core dist:530-536](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L530-L536)、[core dist:581](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L581)）；`writeCard` 自身无尺寸上限（[core dist:490-499](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/vendor/@agent-handoff/core/dist/index.mjs#L490-L499)）。

## SRC-DSH

`[SRC-DSH]` = 本机 `@deepseek-ai/dsh 0.2.1-rc.3` 发行包。它证明宿主契约，不证明目标插件在其上的实际运行结果。

| 契约 | 宿主事实 | 目标插件的依赖点 |
|---|---|---|
| `webServer.register(route)` | 登记命名路由并返回 disposer；handler 拥有完整响应生命周期（`dsh-host-webserver/lib/types/index.d.ts:31-42`） | server.ts:332-338 |
| 重复 `(kind,path)` | **直接抛错**：`duplicate ${kind} route`（`dsh-host-webserver/lib/index.js:321-334`，抛在 L328）；不覆盖、不顶替 | 前缀 `/dsh-takeover` 唯一 |
| 端口所有权 | 宿主自建 `http(s).createServer` 并 `listen(config.port, config.host)`（`dsh-host-webserver/lib/index.js:468-474`）；`port` getter 是宿主自己的（L292-296） | 插件从不 listen |
| 绑定地址 | 配置 schema 拒绝 unspecified/wildcard 地址（`dsh-host-webserver/lib/index.js:255`），只允许一个具体本地接口 | 插件额外做连接级回环闸，覆盖「绑了 LAN 接口」的情况 |
| 前缀匹配 | `pathname === prefix` 或 `pathname` 以 `prefix + '/'` 开头（`dsh-host-webserver/lib/index.js:494-502`） | 注册时**不带尾斜杠**（server.ts:336 注释） |
| `sessionController` 服务 | `Context` 上声明（`dsh-api-session-controller/lib/types/index.d.ts:18`） | 从 root 防御式取（server.ts:174-191） |
| `create` / `rename` / `prompt` 形状 | `create(SessionCreateRequest)`（index.d.ts:101）、`rename`（:156）、`prompt(request, signal)`（:171）；请求字段见 `types.d.ts:284-341` | 三方法形态与插件 `SessionControllerLike` 一致（server.ts:159-169） |
| prompt 的来源归属 | 实现自造 `source = {kind:'user', rpcId, …}` 后交 `commands.prompt`（`dsh-api-session-controller/lib/index.js:3218-3231`） | 注入指令与用户消息在日志中同源 |
| plugin record | `appendPluginRecord(session,type,data)` 存在于 0.2.1-rc.3（`dsh-session/lib/types/index.d.ts:117`） | 动态 import，best-effort（server.ts:285-295） |
| 客户端 seat | `conversation.input.activity` 由 ui-conversation 渲染/声明（`dsh-client-ui-conversation/lib/client.js:19267`、`:20109`）；`settings.section` 由 settings-general 渲染（`:337`） | client.ts:2716 / 2739 |
| 客户端导航 | `ctx.uiWorkspace.openSession(...)`（`dsh-client-ui-chat/lib/client.js:13281`） | browser-view.ts:232-245 |

**目标行为 vs 上游契约的分界**：① 「接管」能成立，靠的是上游 `sessionController` 暴露给插件的能力；② 插件的 HTTP 面没有任何上游鉴权，安全性全由插件自己的 loopback/Origin 守卫承担；③ 同前缀冲突的后果（抛错、插件加载失败）是上游语义，不是插件「礼让」；④ 注入 prompt 在宿主日志里等同用户消息，是上游的 source 归属策略，不是插件伪造。

## TEST

`[TEST]` 只证明覆盖意图，**不证明测试通过**（本轮未跑）。

- 投递核心：`tests/takeover-route.spec.ts:45-73`（take / take_deposit 的 create→rename→queue 顺序与载荷同源）、`:79-85`（inbox 裸 `/inbox`）、`:86-103`（解析失败/create 缺 id/prompt 抛错三连降级）、`:122-138`（停用闸贯通）、`:139-149`（**create 后 rename/prompt 失败 → 错误带孤儿 sessionId**）。
- 路由：`:213-232`（null 体不崩、无 Origin 403、缺控制器规范降级）、`:242-262`（5s 同键去重，只真实投递一次）、`:264-286`（`sessionControllerOf` 形态兼容）。
- 边界：`tests/adversarial.spec.ts:774-781`（连接级回环闸：非回环 403，含 `::ffff:127.0.0.1` 放行）、`:298`（`Sec-Fetch-Site: cross-site` 读 403）。
- 取件语义：`tests/takeover.spec.ts:162-227`（list 只读、load 消费即弃、二次取件报错、核心层直调也报错）。
- **没覆盖**：宿主崩溃/断连后的孤儿清理、回滚、重复前缀冲突、真实宿主上的端到端接管、`lib/` 与 `src/` 一致性。仓库自述测试数 300（CHANGELOG 0.4.2）为 `[DOC]`，本轮未复算。

## CI

`[CI]`：同 SHA 才有意义。`.github/workflows/ci.yml` 在 `push: main` 与 PR 上跑 `npm ci --legacy-peer-deps` + `npm run check`（= `typecheck && test && build`，[ci.yml:22-23](https://github.com/IKEASven69/dsh-takeover/blob/afbc55cb4e076d885a50c2037515f16d008cac59/.github/workflows/ci.yml#L22-L23)）。

- pin commit `afbc55c` 的 check-runs：1 条，`CI` / `completed` / **`success`**，完成于 2026-10-31T04:47:08Z；对应 Actions run 名为 `CI`、`conclusion=success`（2026-10-31T04:44:40Z 触发）。
- 这只是「该 SHA 上 CI 绿」的记录，**不等于我跑过**；也没有核对测试数量或覆盖率。

## RUN

`[RUN] None`。本轮只做了只读网络取数（GitHub REST、`registry.npmjs.org`、`registry.npmmirror.com`、codeload tarball）与本地静态阅读；未安装、未构建、未执行 `npm test`、未启动宿主或插件、未调用任何 `/dsh-takeover/*` 路由。

## 与卡片的偏差

对照版本：`git show HEAD:_leverage/leverage/lever-cross-boundary/samples/09-IKEASven69-dsh-takeover.md`（卡内 `updated: 2026-10-31`）。下表按**审计时的 HEAD 版本**逐条列出；审计期间工作树里的卡片已被维护者并发更新（证据链、`afbc55c` pin、替换对象、入站路由、失败路径等均已补入），逐条现状以工作树为准——**本文件未改卡**。

| 卡片位置 / 主张 | 复核结论 | 标签 | 依据 |
|---|---|---|---|
| L46 「版本(本次读) `0.4.3`」 | 审计时**坐标不可复现**：npm 无发布物；tag `v0.4.3` 的树自述 `0.4.2`；HEAD 自述 `0.4.3` 但含 `0.4.4` 功能提交，且未 pin tag/commit。**工作树已改**：现为 `main afbc55c` pin + 错位说明 | `[SRC-TARGET]`+API | Provenance |
| 全卡未定义「takeover 替换什么」 | **只替换会话**：同进程新建会话并投递 `/resume-*`；不夺进程/端口/profile，UI 是叠加 | `[SRC-TARGET]` | server.ts:256-269；client.ts:2716/2739 |
| L13 / L22 「插件零网络」 | 方向对（无出站请求）但**省略入站 HTTP 面**：宿主 listener 上挂 10 个子路由 | `[SRC-TARGET]` | server.ts:332-338, 631 |
| L14 「边界:3 跨进程/跨机」 | 接管**本体在同进程内**；跨进程只发生在文件总线与只读外部库；跨机靠同步盘 | `[SRC-TARGET]` | server.ts:256-269；README:118 |
| L26 / L57 恰好一次顺序 | **成立**（`wx` 认领 → render → rename → finally 删） | `[SRC-TARGET]`（vendored dist） | core dist:576-628 |
| L26 / L57 「认领残留 60s 后 sweepClaims 清」 | 阈值成立，但**不是定时器**：仅列目录时触发；且 claim 打开的任何失败都被报成「另一进程」 | `[SRC-TARGET]` | core dist:502, 516, 526, 583-587 |
| L28 四态账本 | 成立；是**标记约定 + 覆盖率统计**，不是强制校验 | `[SRC-TARGET]` | tools.ts:89-90 |
| L30 「密钥与卡片同盘（T1-T6 自列）」 | 成立；T2 与信任边界段落都明写 | `[DOC]` | THREAT-MODEL:16, 36-47 |
| L50 「`@deepseek-ai/*` 走 registry」 | 不精确：它们是 **peerDependencies + devDependencies**，`dependencies` 为空；`@agent-handoff/*` 走 `file:` 正确 | `[SRC-TARGET]` | package.json:65-83 |
| L59 「>512KB 拒 / 未跟踪 ≤20 / `git apply` 三级」 | 成立（524288、20、`--check → apply → -3`） | `[SRC-TARGET]` | core dist:740, 742；tools.ts:385 |
| L60 「首末条各 400 / 最近 3 轮各 300 / top 15 / ≤10 命令」 | 大体成立，但「3 轮」实为**最近 3 条 assistant 文本**；15 是「额外关键文件」名额 | `[SRC-TARGET]` | foreign.ts:230, 258-259；tools.ts:485；collect.ts:173 |
| L48 「404 + 0★ 是几乎无人使用的最直接解释」 | 404/0★ 是事实；**因果是判断**，无法从仓库证明 | `[OBS]` | `/repos`、registry |
| 卡头缺「证据链」行、无 memo 链接 | 审计时与 `EVIDENCE.md` §2.1/§2.2 不符；**工作树已改**：卡头现补了指向本 memo 的证据链行（非本文件改动） | `[DOC]`（本册规程） | EVIDENCE.md:29-38 |
| 卡片未写接管失败路径 | 无自动回滚：孤儿会话 id 回传、手动删；外部侧不受影响 | `[SRC-TARGET]` | server.ts:297-303 |

## `[OPEN]`

- **core 只有 dist**：`@agent-handoff/core`/`readers` 在本仓库只有已编译 `dist`（声明的版本 0.1.0），claim/rename/archived 逻辑的「作者源码」不在 pin 内；dist 与 core 源仓的一致性未验证。
- **`lib/` 与 `src/` 一致性**：`lib/` 产物已入库，本轮未比对构建产物是否逐字对应 `afbc55c` 的 `src/`。
- **未在真实宿主跑过 takeover**：`/resume-*` 技能是否真能在 DSH 0.2.1-rc.3 上把外部会话读进新会话、`uiWorkspace.openSession` 是否切得动，均只做了契约层比对。
- **孤儿会话清理**：宿主会话树里删除孤儿后的 relay 记录是否残留、是否影响后续接管，未验证。
- **活跃外部库并发**：外部 CLI 正在写（sqlite WAL / JSONL 半行）时的读取一致性未验证；只确认适配器用 `readOnly:true` 打开。
- **同步盘冲突语义**：跨机 rename/冲突由同步盘决定，SMB/NFS/iCloud 下的实际表现未验证（CHANGELOG 0.4.0 只声称修过 Windows 并发 rename 双成功）。
- **0.4.4 未复核**：HEAD 已有 `src/signing.ts`（HMAC 信封）等 0.4.4 提交，但无 0.4.4 版本号/CHANGELOG/tag；本 memo 不评价其签名行为。
- **0.2.0-rc.2 宿主**：`engines.dsh` 同时允许 `0.2.0-rc.2` 分支，未核该代 `sessionController`/`webServer` 是否同形。
