---
title: "源码复核：All3nCN/dsh-better-sidebar-N23"
domain: reshape-product
kind: evidence
positioning: "钉住冻结 fork 的 HEAD / v0.1.0 / npm tarball 三点，按树差异而非血统量出它与上游 0.12.3、0.28.2 的距离，界定 shell/91 反例卡的证据强度。"
read_when: "核对 shell/91_冻结分叉-better-sidebar-N23.md 的分叉坐标、peer 闸门、持久化身份，以及『上游已补齐』类断言。"
status: observed
updated: 2026-11-01
---
# dsh-better-sidebar-N23 源码复核

> **固定快照**：只读一手仓库与 npm 元数据，**未安装、未构建、未运行**目标代码或宿主。fork 固定到 HEAD [`ca9694b4d232ff47eefec07e395b23eef0766831`](https://github.com/All3nCN/dsh-better-sidebar-N23/commit/ca9694b4d232ff47eefec07e395b23eef0766831)（2026-09-03T22:54:40+08:00）与 tag [`v0.1.0` → `8604e63`](https://github.com/All3nCN/dsh-better-sidebar-N23/commit/8604e63b36854fb937ec7bf86a5a0331ca590e51)；上游固定到分叉基点 [`v0.12.3` → `ab785d71`](https://github.com/omdsh-dev/DSH-better-sidebar/commit/ab785d71fb194ea9db4487461af8f5d40e67c216) 与最新 tag [`v0.28.2` → `b0e0fab5`](https://github.com/omdsh-dev/DSH-better-sidebar/commit/b0e0fab50e68f54b07a1fc1e7898030409c7d979)。宿主固定为本机 `@deepseek-ai/dsh@0.2.1-rc.3`。
>
> **方法**：fork 根提交**没有父提交**（不是 GitHub fork 关系），因此 ahead/behind 不能按祖先算；本文用 `git ls-tree -r` 比 blob SHA 得出增/删/改，用 npm tarball 与 git tree 逐文件哈希比对确定"发布物 = 哪个提交"。
>
> **标记**：`[DOC]` 仓库文档/清单；`[SRC-TARGET]` fork 固定提交源码；`[SRC-DSH]` `0.2.1-rc.3` 发行包源码；`[TEST]` 测试源码；`[CI]` workflow 配置（存在≠通过）；`[RUN]` 本机只读的 git/npm/目录检查（**不含**安装、构建、运行目标代码）。

## 0. 坐标

| 项 | 值 | 来源 |
|---|---|---|
| fork 仓库 | `All3nCN/dsh-better-sidebar-N23`，MIT，`fork: false`，创建 `2026-08-31T16:00:09Z`，最后 push `2026-09-03T14:55:01Z` | GitHub API |
| fork 历史 | 根提交 `1b83db4b`（无父）+ 9 个提交 = **总计 10**；`main` HEAD = `ca9694b4` | `git log` |
| fork 版本 | `package.json` `0.1.0`；npm 只有 **1** 个版本：`0.1.0`（`2026-08-31T17:21:40Z`，shasum `5e4c2576…`） | `[DOC]` [package.json](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/package.json#L1-L3) / npm registry |
| fork tag | 唯一 tag `v0.1.0` → `8604e63`（"rename marketplace fork to N23"，`2026-09-01T00:24:12+08:00`） | `git tag` / GitHub tag API |
| 分叉基点 | 根提交自述 `fork of dsh-better-sidebar@0.12.3`；上游 `v0.12.3` = `ab785d71`（2026-08-17） | `[DOC]` [根提交](https://github.com/All3nCN/dsh-better-sidebar-N23/commit/1b83db4be282d17f56ca33bc053f132b8625a860) / [UPSTREAM.md:6](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/UPSTREAM.md#L6) |
| 上游现状 | `v0.28.2` = `b0e0fab5`（2026-10-27）；`main` = `2d736f5`（2026-10-30，tag 后 2 个 README 提交）；4,780★ / 446 fork / 222 open issues | GitHub API |
| 上游 npm | 36 个版本，latest `0.28.2`，月下载 245,373 | npm registry |
| fork npm 下载 | 月 1,350 / 周 386（2026-09-30–10-29） | npm downloads API |

## 1. "分叉"是复制树，不是继承历史

- 根提交 `1b83db4b` 的 `parents` 为空，`git log --max-parents=0` 只有一个根；仓库 `fork: false`（**不是** GitHub 意义上的 fork），因此 GitHub compare 无共同祖先，`ahead_by/behind_by` 对本仓库无意义。`[SRC-TARGET]`
- 提交时间被重写：根提交 `2026-09-01T00:00:05+08:00`，`8604e63` 为 `2026-09-01T00:24:12+08:00`，其余 8 个全部落在 `2026-09-03T22:54:39–40+08:00`；而 npm 发布在 `2026-08-31T17:21:40Z`。git 时间线不能当发布史用，**npm 的 `time` 与 release 的 `published_at` 才是锚点**。
- 发布物对齐：把 npm tarball 解出 171 个文件，与 tag `v0.1.0` 树逐文件 SHA-256 比对 **171/171 全等**；tag 树共 174 个文件，差 3 个是 `files` 未包含的 `.github/workflows/release.yml`、`docs/RELEASE.md`、`.gitignore`。对根提交树则只有 162/171 相等（9 个文件在 rename 时改过）。`[RUN]` 本机只读比对。
- 由此：**npm 上的 0.1.0 = tag 树**；HEAD 比 tag 多 8 个提交（测试/CI/文档），`package.json` 仍是 `0.1.0`，`CHANGELOG` 把这批记为 `[Unreleased]`（[CHANGELOG.md](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/CHANGELOG.md#L7-L23)）。仓库 HEAD ≠ 已发布产物。

## 2. 差异规模（按树，不按血统）

`[RUN]` `git ls-tree -r v0.12.3`（180 个文件）对 fork HEAD（181 个文件）：

| 指标 | 值 |
|---|---|
| 新增 / 删除 / 内容改动 | **90 / 89 / 19**（触及 198 条路径） |
| 上游同期已走远 | `v0.12.3..v0.28.2` = **1,154 个提交**、**27 个版本 tag**，约 **72 天**（≈16 提交/天、约 2.7 天一个版本）；到 `main` 为 1,156 个提交 |
| 删除里的结构项 | `tests/` **60 → 2**（删 58 个文件，含全部 spec / e2e / helper）；`docs/plans/` **17 → 0**；构建工具链 `tsconfig*.json`、`tsdown.config.ts`、`vitest.config.ts`、`playwright.config.ts`、`pnpm-lock.yaml`、`pnpm-workspace.yaml`；`AGENTS.md`、`docs/external-plugin-guide.md`、`dsh.plugin.json` |
| 新增里的结构项 | `lib/` 6 个 bundle（`index/client/client-registry/client-editor/client-terminal/invariant`）+ 75 个 `.d.ts`（**基点树里 `lib/` 为 0 个文件**，是 CI 产出不提交）；`UPSTREAM.md`/`CONTRIBUTING.md`/`SECURITY.md`/`CHANGELOG.md`/`THIRD-PARTY-NOTICES.md`/`docs/RELEASE.md`；2 个零依赖测试 |
| 改动的源码 | 仅 **9 个** `src` 文件：`src/client/{Sidebar.tsx,TerminalView.tsx,chunk-loader.ts,index.tsx,layout.css,sidebar.module.css,split-pane.tsx,state.ts}` + `src/html-route.ts` |

**读法**：改动面很窄（9 个 src 文件），但**验收面被整体拆除**——上游 60 个测试、17 份设计档、类型检查与打包工具链都不在了；同时把上游不提交的 `lib/` 变成人工维护的运行时。

## 3. 它到底改了什么：五条声明与它们落在哪

`[DOC]` [UPSTREAM.md:16-36](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/UPSTREAM.md#L16-L36) 列出 5 条：① 拖拽面板期间不逐帧写 `--dsh-sidebar-width/height`，中央对话只在 pointer release 时重排一次；② composer 卡片改 8px 圆角；③ 面板宽度 ≤320px 时页签退化为纯图标；④（2026-08-22）适配删除 `window.__DSH_MODULES__` 的新内核，经 `ctx.get?.("modules")` 绑定 ClientModuleSystem；⑤（2026-08-31）外壳重构：全宽 48px 顶栏、VSCode 式活动栏、全局控制区，验证于 DSH `0.1.1-rc.2`。

源码对得上的是：`[SRC-TARGET]` [layout.css:54-59](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/src/client/layout.css#L54-L59)（`[data-composer-card]` 8px）；[layout.css:22-52](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/src/client/layout.css#L22-L52)（布局挤压 + 折叠/拖拽 body 属性；48px 带变量本身在 [sidebar.module.css:82-87](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/src/client/sidebar.module.css#L82-L87)）；[chunk-loader.ts](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/src/client/chunk-loader.ts)（modules 服务回退）。`split-pane.tsx`、`state.ts`、`Sidebar.tsx` 在改动清单里，与 ①③ 相符。

**但外壳的重心不在 `src` 里。** `[SRC-TARGET]` 活动栏类名 `.ssb-actrail` 在 **`lib/client.js`** 出现 **23** 次，而 `src/` 里只有一句注释提到它（[sidebar.module.css:2041-2055](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/src/client/sidebar.module.css#L2041-L2055)）；上游**全部 45 个 tag 都没有** `actrail`（逐 tag 检查 `src/client/sidebar.module.css` 命中数为 0，`v0.28.2` 整树 grep 亦为 0；`[RUN]` 只读 grep）。这与作者自述一致：`[DOC]` [UPSTREAM.md:46-58](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/UPSTREAM.md#L46-L58) 说 `src/` 已回补上游 0.17.1 的 A 类加固、`lib/` 保留"手工镜像进去的 shell CSS"，**运行时由 `lib/` 决定**，且"naive 全量重建会抹掉 shell（2026-09-01 回滚事故的根因）"。

也就是说：**招牌界面的一部分只存在于编译产物里，从仓库源码无法重建**；`src` 与 `lib` 是有意的双轨。

## 4. 它继承了哪些上游耦合

| 耦合面 | fork 的值 | 上游 0.12.3（基点） | 上游 0.28.2（现状） |
|---|---|---|---|
| peer 区间 | 15 个 `@deepseek-ai/dsh*` peer = `>=0.1.0-rc.6 <0.2.0`；另 `@deepseek-ai/cordis`、`cordis`、`react(-dom)` [package.json:76-95](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/package.json#L76-L95) | `^0.1.0-rc.6`（同一语义，semver 展开为 `>=0.1.0-rc.6 <0.2.0-0`） | `^0.2.1-rc.1`（展开 `>=0.2.1-rc.1 <0.3.0-0`），并增 `dsh-subagent`、`@huanlin/dsh-plugin-better-locale` |
| `dsh.client.inject` | 与基点**逐字相同**：`dsh-client-runtime`、`dsh-client-locale`、`dsh-client-ui-slots`、`dsh-client-ui-conversation` [package.json:44-52](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/package.json#L44-L52) | 同上 | 改为 `…-locale`、`…-ui-slots`、`…-ui-conversation`、**`ui-sidebar-right`**、**`dsh-client-modules`**，并加 `dsh.manifestVersion: 1` |
| 客户端 slot | `settings.section`（[index.tsx:240](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/src/client/index.tsx#L240)）、`conversation.chat.turnTail`（[intercept.tsx:75-76](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/src/client/intercept.tsx#L75-L76)） | 同 | 两个 slot 名在 `0.2.1-rc.3` 宿主里**仍在用**（`dsh-client-ui-settings-*`、`dsh-client-ui-chat` 等包注册到同名） |
| DOM 假设 | `#root > div[data-slot="root"] > div > div:nth-child(2)`、`body[data-dsh-sidebar-collapsed] [data-slot="conversation.session.header"] > header`，注释自称"DSH 0.1.x"结构 [layout.css:9-15,27-52](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/src/client/layout.css#L9-L52) | 同结构 | 宿主在 0.2.x 增加了原生 `ui-sidebar-right` / dock 包，上游 0.28.2 的 `sidebar/dock-fallback.tsx` 自述在与宿主 AppFrame 几何对齐 |
| 持久化身份 | localStorage `dsh-sidebar:v1:<sessionId>`（[state.ts:764](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/src/client/state.ts#L764)）、settings namespace `dsh-better-sidebar`（[prefs-shared.ts:10](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/src/prefs-shared.ts#L10)）、Loader 行 id `better-sidebar`（[cordis.patch.yml:22](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/cordis.patch.yml#L22)）、locale ns `betterSidebar`（[locales.ts:470](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/src/client/locales.ts#L470)） | 同名 | **四个 key 到 0.28.2 一字未改**（`state.ts`、`prefs-shared.ts`、`cordis.patch.yml` 同值） |
| 服务名 | `ctx.provide('betterSidebar', …)` [index.tsx:68](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/src/client/index.tsx#L68)，`registerTab` / `registerFileViewer` [service.ts:295-296](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/src/client/service.ts#L295-L296) | 同 | 同服务名，但改由宿主 `ui-sidebar-right` 承载 |

**结论**：它换的只是**包名与版本号**，没换接缝——行 id、服务名、settings ns、localStorage key 全部沿用上游；所以第三方插件的 `inject: ['betterSidebar']` 源码层面仍兼容，而本仓库快照里没有任何插件把 `@all3cn/...` 写进 peer（`[DOC]` 卡片所称"生态按包名选择"在此成立，机制依据是身份四件套未换）。

## 5. 宿主版本闸门（复核卡片 §2.2）

`[SRC-DSH]` `@deepseek-ai/dsh-app-boot@0.2.1-rc.3` `lib/index.js`：

| 位置 | 事实 |
|---|---|
| `:252-296` | `unmetRequirements(fields, runtimeVersion)`：**先看 `engines.dsh`**，有就只按它判（`:281-287`），没有才遍历 peerDependencies |
| `:291` | `if (name !== "@deepseek-ai/dsh" && !name.startsWith("@deepseek-ai/dsh-")) continue;` —— **前缀白名单**，不是通配展开 |
| `:276-278` | `semver.satisfies(version, range, { includePrerelease: true })` |
| `:311-322` | `evaluatePluginCompatibility(manifest, exemptions, runtimeVersion)`；`:306-309` 的注释写明入参是"parsed plugin package.json"，返回未满足项与豁免状态 |
| `:1758-1759`（`dsh-plugin-manager`） | `throw new ManagementFailure("incompatible-version", …)`；安装/更新路径另有 `:2041`、`:2075-2076`、`:2287-2288` |
| `:1625-1640`（`dsh-plugin-manager`） | `readProfileVersionExemptions` / `setProfileVersionExemption`：**按"包@精确版本 + 精确宿主版本"发放豁免**；`pluginCompatibilityWarning` 文案直接指向 `dsh plugin allow-version` |

对本包的可复核推论：15 个 `@deepseek-ai/dsh*` peer 全部不满足 `0.2.1-rc.3`；`@deepseek-ai/cordis`、`cordis`、`react`、`react-dom` 这 4 个 peer **不参与判定**（不匹配 `dsh` / `dsh-` 前缀）；字面量 `@deepseek-ai/*` 同样永远不匹配——效果确实是"写了等于没写"，但机制是白名单而非"通配特判"。

两处需要精确化的边界：

1. **闸门读的是 `package.json`。** 宿主发行包的 JS（`@deepseek-ai/*/lib/*.js` 与 `dsh/lib/*.js`）里没有读取 `dsh.plugin.json` 或 `dsh-plugin.json` 的代码（grep 0 命中）。所以上游 0.12.3 在 `dsh.plugin.json` 里写的 `engines.dsh: ">=0.0.1"` **救不了** fork（那份清单不是本代闸门的输入）；fork 自造的 `dsh-plugin.json` 只是给注册表/市场工具的自述（[dsh-plugin.json:16-19](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/dsh-plugin.json#L16-L19)）。
2. **"什么都没装"未被源码证明。** 源码证明的是抛错点，不证明 pnpm/文件系统已写入的部分会回滚；卡片该句应记为 `[OPEN]`。

一处语义差异：fork 把上游的 `^0.1.0-rc.6` 手写成 `>=0.1.0-rc.6 <0.2.0`，两者**并不完全等价**——caret 展开是 `<0.2.0-0`，会排除 `0.2.0-rc.*`；手写版在 `includePrerelease` 下**接受 `0.2.0-rc.1`**（`[RUN]` 用宿主自带 `semver` 计算，非运行目标代码）。即 fork 的抄写把上界**放宽**了一点点，但仍挡不住 `0.2.1-rc.3`。

## 6. 越过闸门之后还会撞什么（豁免也救不了的部分）

- **双挂载即路由冲突。** `[SRC-DSH]` `dsh-host-webserver` `:321-331`：`duplicate (kind, path)` 直接抛 `webserver: duplicate prefix route "…"`。fork 注册 `/sidebar/api`、`/sidebar/file`、`/sidebar/html`、`/sidebar/bundle`、`/sidebar/ws/terminal`、`/sidebar/ws/agent-terminals`（[index.ts:533-722](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/src/index.ts#L533-L722)），前三条与上游基点**同名同路径**，上游 0.28.2 也仍注册这三条（`[RUN]` 只读 grep 两版 `src/index.ts`）。为此上游 0.28.2 在 `cordis.patch.yml` 里加了 `disabled: !!js` 的聚合守卫并点名 "duplicate prefix route"，**冻结的 fork 没有这层守卫**，只有一句"先删掉旧挂载行"的注释。
- **双服务即抛错。** `[SRC-DSH]` `@deepseek-ai/cordis@4.0.5` `lib/index.js:800-823`：同名二次注册抛 `service "betterSidebar" has been registered at <fiber>`。行 id 相同（`better-sidebar`）再叠加同名服务，两条挂载无法共存。
- **客户端声明已过期。** `0.2.1-rc.3` 的安装目录里 `dsh-client-runtime`、`dsh-client-ui-slots`、`dsh-client-web-react`、`dsh-client-ui-primitives`、`dsh-invariants` **全部不存在**（`[RUN]` 只读目录检查）；而 fork 的 `dsh.client.inject` 里 `dsh-client-runtime`、`dsh-client-ui-slots` 正是其中两个（`dsh-client-locale`、`dsh-client-ui-conversation` 则仍在）。宿主把 `inject` 原样带进客户端模块图（`dsh-client-modules` `lib/index.js:67`、`:743`），对未知依赖是致命还是忽略本轮未验证 → `[OPEN]`；但"声明指向宿主已不存在的包"是事实。
- **持久化键是共享的。** fork 与上游写同一个 `dsh-sidebar:v1:<id>`、同一个 settings ns；上游 0.28.2 的 `sanitizeState` 会修剪/兼容旧 state（`state.ts` 的旧字段默认值，`[DOC]` CHANGELOG:544 记 split-leaf 修剪），fork 的版本冻结在 0.12.3 的 schema。双向切换会互相改写同一份布局状态，具体损坏形态未实测 → `[OPEN]`。
- **加固没有进运行时。** 作者自述 `src` 已吸收上游 0.17.1 的 A 类修复、`lib` 没有（[UPSTREAM.md:48-55](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/UPSTREAM.md#L48-L55)）；而运行时是 `lib`。这属于作者自述的**安全/健壮性缺口**，本次无法构建验证两轨差异。

## 7. 为什么值得维护一个冻结 fork（作者给的理由，及它剩下的东西）

`[DOC]` 理由只有一条真的不可上游化：**外壳方向**（48px 顶栏 + 活动栏）。其余三条是局部 UX/CSS，第四条是内核兼容补丁。`[OBS]` 判断：**"上游拒绝这个方向"并不成立**——上游从未实现活动栏，它走的是另一条路：把界面接缝交给宿主。

`[RUN]` 文件级对比显示上游 0.28.2 已经**主动砍掉**了 fork 赖以立身的另外两块：

| fork 独有 | 上游 0.28.2 |
|---|---|
| `src/agent-pty.ts`、`pty-manager.ts`、`pty-deps.ts`、`tools.ts`（`terminal_*` 工具） | 全部删除；改为驱动宿主 `ctx.webTerminals`（`[DOC]` CHANGELOG:248），`terminal_*` 工具不再由插件提供 |
| `src/browser-probe.ts`、`client/BrowserView.tsx`、`browser.ts`（内嵌浏览器） | 全部删除 |
| Git 真 diff / 暂存 / 提交 / 还原 | **已补齐**：`client/DiffTab.tsx`、`git.ts:1010-1112`（`diff/diffHead/stage/unstage/commit/discard`）、`editor-git-gutter.ts`；`[DOC]` CHANGELOG:433 明说"真 diff / 历史 / 暂存·提交·还原" |
| 活动栏 + 48px 顶栏 | **没有**；`sidebar.module.css` 无 `actrail`、无 `--dsh-global-header-bottom`；唯一相近的 `client/activity-icons.tsx` 是任务页的"合并活动行"图标 |

另外 `0.2.1-rc.3` 宿主自己就带了 `dsh-client-ui-sidebar-right`、`-files`、`-terminal`、`-browser`、`-documentpreview` 五个原生侧栏包（是否在默认 profile 挂载本轮未验证）——fork 的浏览器与终端能力在 0.2.x 上已属**宿主可提供**，不再是不可替代的差异点。

## 8. 维护者要承担、而插件不必承担（本样本的账）

| 项 | 上游 | fork |
|---|---|---|
| 发布节奏 | 72 天 27 个版本、1,154 提交；`v0.28.2` 之后仍有 2 个提交 | 10 个提交、1 个版本；2026-09-03 后停更；`CHANGELOG` 有 `[Unreleased]` 未发 |
| 兼容矩阵 | `[CI]` CI 明确"pin the exact 0.2.1-rc.1 host CLI; never use a dist-tag"（`ci.yml:174-181`），带 typecheck/lint/单测/挂载冒烟 | `[CI]` 单个 `ubuntu-latest` + Node 22，只跑 `npm test`（2 个测试）、`node --check` 与 manifest dry-run（[ci.yml:9-31](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/.github/workflows/ci.yml#L9-L31)）；**不安装宿主、无 typecheck（工具链已删）** |
| 安全修复 | 有 issue/PR 面（222 open）与成规模单测（`[DOC]` CHANGELOG:363 自述 124 files / 1,296 passed） | `SECURITY.md` 写"只支持最新发布版"，而最新版恰好是 0.2.x 拒装的那个；唯一 release 的 npm 元数据**无 provenance 证明**（`dist.attestations` 为空），尽管 `release.yml` 已配 OIDC Trusted Publishing |
| 构建可复现 | 提交 `pnpm-lock.yaml`，CI 构建 | `lib/` 手改、`src` 与 `lib` 双轨，作者自己写明"naive 重建会回滚 shell" |
| 迁移说明 | 逐版 CHANGELOG + 支持线下限 | README 只给"先删旧挂载行"与"降级宿主"两条路 |
| 同作者第二份 | — | `@all3cn/dsh-qa-suite-n23` 也只有 `0.1.0`（2026-09-01），peer 同样是 `^0.1.0-rc.6` / `^0.1.1-rc.2`，同样停在 0.1.x |

## 9. 对卡片的校正

| 卡片说法 | 一手证据 | 可以怎么说 |
|---|---|---|
| "peer 写上界是它主动设的死期" | fork 的 `>=0.1.0-rc.6 <0.2.0` 是上游 0.12.3 `^0.1.0-rc.6` 的手写展开，且比 caret 略宽（接受 `0.2.0-rc.*`） | 上界是**继承**的默认写法，不是 fork 的独立决策；真正的选择是"冻结在 0.1.x"。`0.x` 包的 caret 天然带上界，所以"排定退役"应归因于冻结，而非归因于写上界 |
| "有 `engines.dsh` 就独占判定，否则每个 peer 都要满足" | `app-boot:281-296` | 成立；补充：只判 `@deepseek-ai/dsh` 与 `@deepseek-ai/dsh-*`，`@deepseek-ai/cordis` 等不判 |
| "通配键 `@deepseek-ai/*` 被静默 continue，是上游该修的真陷阱" | `app-boot:291` 是前缀白名单 | 效果对（写了等于没写、无警告），但机制不是通配特判；把它描述为"白名单外的键一律忽略"更准确 |
| "0.2.x 上装不上，安装期抛 `incompatible-version`" | `dsh-plugin-manager:1759` 等 4 处 | 判定成立；**"什么都没装"未证明**（原子性 `[OPEN]`） |
| "验证只到 `0.1.1-rc.2`" | `[DOC]` [dsh-plugin.json:18](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/dsh-plugin.json#L18)、[README.md:28](https://github.com/All3nCN/dsh-better-sidebar-N23/blob/ca9694b4d232ff47eefec07e395b23eef0766831/README.md#L28)、UPSTREAM.md:36 | 三处一致 |
| "peer `>= 0.1.0-rc.6 < 0.2.0`、无 `engines.dsh`" | npm manifest、`package.json` | 成立（`engines` 只有 `node: >=20`） |
| "★0 / npm 1,350" | GitHub 0★；npm 月 1,350、周 386 | **精确命中** |
| "0.1.x 冻结" | npm 只有 1 个版本 | 更准确："只有 `0.1.0` 一个版本" |
| "同作者还发了 `dsh-qa-suite-N23`" | npm 有 `@all3cn/dsh-qa-suite-n23@0.1.0`（2026-09-01） | 包存在；**仓库本轮网络不可达**，仓库维度 `[OPEN]` |
| "上游 0.28.x 已把 diff、暂存、活动栏补齐" | diff/暂存 ✓（`DiffTab.tsx`、`git.ts:1010-1112`）；活动栏 ✗（45 个 tag 的 CSS 与 v0.28.2 整树均无 `actrail`） | 改为"diff 与暂存/提交/还原已补齐；**活动栏没有**；终端与浏览器是**宿主**补的，不是上游" |
| "名单内被引 1 条" | `data/plugins/` 1 条 yml + `data/capabilities.json` 1 行；根 README 2 次提及 | 按目录条目算是 1 条；"无人适配"只能说到"本仓库快照内无第二条依赖记录" |
| "强行 allow-version 豁免 `[OPEN]`" | `dsh-plugin-manager:1625-1640` 有按"包@版本+宿主版本"的豁免与 CLI | 机制**存在**；但客户端 `inject` 指向的包在 0.2.1-rc.3 不存在，豁免后能否跑起来仍需实测 → 保持 `[OPEN]` |

## 10. 未核实（`[OPEN]`）

- 未安装、未构建、未运行：fork 的 `lib/` 与 `src/` 是否行为等价、`lib` 里手改的 shell 是否真能跑，本轮都**没有验证**（且构建本身被任务禁止）。
- `dsh plugin add` 在 peer 拒绝时是否留下半装状态：源码只给抛错点。
- 客户端模块图对"inject 指向不存在包"的处理是致命还是忽略。
- DSH `0.1.1-rc.2` 上的真实行为：本机只有 `0.2.1-rc.3`，作者声称的验证点无法复现。
- `All3nCN/dsh-qa-suite-N23` 仓库本体的提交/版本（npm 侧证据在，GitHub 本轮连接失败）。
- 双挂载时 Loader 对重复行 id 的具体处置（源码只证明路由与服务会抛）。
- 上游是否接受过外壳方向的上游 PR：本轮未查 issue/PR 面，只有"从未实现活动栏"这一事实。

## 11. 复现命令（只读）

```sh
git clone --filter=blob:none --no-checkout https://github.com/omdsh-dev/DSH-better-sidebar up
git clone https://github.com/All3nCN/dsh-better-sidebar-N23 fork
git -C up fetch /path/to/fork main                  # 同一对象库内跨仓比树
git -C up diff --stat v0.12.3 FETCH_HEAD          # 需 blob；或直接比 ls-tree 的 SHA
git -C up ls-tree -r v0.12.3 > base.txt; git -C up ls-tree -r FETCH_HEAD > fork.txt
curl -sSL https://registry.npmjs.org/@all3cn/dsh-better-sidebar-n23/-/dsh-better-sidebar-n23-0.1.0.tgz | tar -xz
```
