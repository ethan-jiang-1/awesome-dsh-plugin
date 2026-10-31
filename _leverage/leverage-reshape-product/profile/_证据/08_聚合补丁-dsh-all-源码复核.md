---
title: "源码复核：聚合补丁 dsh-all"
domain: reshape-product
kind: evidence
positioning: "固定 @hyzyn/dsh-all 发布物与目标源码 commit，核验聚合 patch、依赖边界、Profile 管理与失败/测试证据。"
read_when: "复核 profile/14 的聚合包纯数据主张、共享库边界、安装/启停、Profile UI 与发布可靠性。"
status: observed
updated: 2026-10-31
---
# 源码复核：聚合补丁 dsh-all

> 只读第一方 npm metadata/CDN、GitHub 固定 commit 与 DSH 上游 `dsh-v0.2.1-rc.3`；未安装、构建或运行目标。`[DOC]` 为发布文档主张；`[SRC-TARGET]` 仅指精确匹配 npm 版本的目标源码；`[SRC-DSH]` 为宿主固定源码契约；`[TEST]` 为测试/检查定义，不是本轮执行结果；`[CI]` 为该 SHA 的远端 check 记录；本轮无 `[RUN]`。

## 身份与发布 pin

- **[SRC-TARGET:发布 metadata]** 样本是 `hyzyn/dsh-plugin-kit` 中 `packages/all` 的 npm 包 `@hyzyn/dsh-all@0.1.73`。精确 [npm metadata](https://registry.npmjs.org/@hyzyn%2fdsh-all/0.1.73) 给出 tarball [`dsh-all-0.1.73.tgz`](https://registry.npmjs.org/@hyzyn/dsh-all/-/dsh-all-0.1.73.tgz)、SHA-1 `7e0c76e09d0bde44579cfdeb8145517498d700df`、SHA-512 `sha512-LSs9HDip+oDqMciS+HakPLLZsuwAmpi3UK+MooIiOMIBmjJ56onTs79k7iY3hm9AFMK8O+CFwZZtLWNnL+RdJA==`；registry `repository.directory` 是 `packages/all`。
- **[SRC-TARGET:commit/tag]** GitHub tag `v0.1.73` 指向 [`2c6b35bbb50730b9781039d52fd24763e45cbc2e`](https://github.com/hyzyn/dsh-plugin-kit/commit/2c6b35bbb50730b9781039d52fd24763e45cbc2e)。固定 [tagged packages/all/package.json](https://github.com/hyzyn/dsh-plugin-kit/blob/2c6b35bbb50730b9781039d52fd24763e45cbc2e/packages/all/package.json) 标记 `@hyzyn/dsh-all@0.1.73`；其 dependency map 与 npm metadata 精确一致。npm tarball 内发布 patch [CDN copy](https://cdn.jsdelivr.net/npm/@hyzyn/dsh-all@0.1.73/cordis.patch.yml) 与 commit 的 [cordis.patch.yml](https://github.com/hyzyn/dsh-plugin-kit/blob/2c6b35bbb50730b9781039d52fd24763e45cbc2e/packages/all/cordis.patch.yml) 内容一致。该版本源码推论可继续；不把 `main` 或其他版本作依据。
- **[DOC]** 同一 commit 的 [README](https://github.com/hyzyn/dsh-plugin-kit/blob/2c6b35bbb50730b9781039d52fd24763e45cbc2e/README.md) 宣称面向 DSH Web GUI，并列出安装、按需单装、能力分面、重启要求和 11 个适配基线。该清单是作者声明，不等价于每一基线在本轮被验证。

## SRC-TARGET：聚合与依赖边界

- [发布 manifest](https://github.com/hyzyn/dsh-plugin-kit/blob/2c6b35bbb50730b9781039d52fd24763e45cbc2e/packages/all/package.json) 声明 `dsh.bundle.patch: ./cordis.patch.yml`，并精确依赖 11 个功能包：`codegraph@0.6.18`、`docker@0.13.7`、`env@0.3.15`、`kit-settings@0.2.9`、`loglens@0.1.6`、`mcp@0.3.11`、`profile@0.2.13`、`prompt@0.2.13`、`rss@0.4.13`、`search@0.4.15`、`tty@0.35.0`。Peer `@deepseek-ai/dsh` 为可选，范围显式列出 11 档，不是笼统 `0.2.x`；`engines.dsh` 声明 `>=0.1.7-rc.2`。目标 README 另称安装/启动兼容检查由 peer declaration 承担；本 memo 不把范围声明当作实测兼容。
- [发布 patch](https://github.com/hyzyn/dsh-plugin-kit/blob/2c6b35bbb50730b9781039d52fd24763e45cbc2e/packages/all/cordis.patch.yml) 是 12 个 `insert`：aggregate 自身 id `all` 加 11 个插件行（`env-manager`, `codegraph`, `docker`, `kit-settings`, `loglens`, `mcp-config`, `profile-manager`, `prompt-manager`, `rss-digest`, `global-search`, `tty`）。这些是各单包 patch 的 Loader row id，name 指包名。patch 不包含 `disabled` 或 `override`，因此它做的是添加挂载行，而非禁用或覆盖宿主/既有插件行。已单独装某些成员时，仍有重复 row ID 冲突风险；README 明确警告不要在同一 profile 同时添加聚合入口和根 bundle/单包。
- [aggregate generator](https://github.com/hyzyn/dsh-plugin-kit/blob/2c6b35bbb50730b9781039d52fd24763e45cbc2e/scripts/aggregate.mjs) 扫描有 `dsh.bundle.patch` 的包，从各自 patch 提取 `id`/`name`，依据 `aggregate-order.mjs` 排序后写 aggregate patch 与 dependencies；依赖版本取每个插件自身 `package.json` 精确版本，而非发布时才转换的 `workspace:*`。它还同步生成仓库根 bundle，两入口共用成员 rows，但 aggregate `all` 自身行与根 `dsh-plugin-kit` 行身份不同。脚本注释称手改生成文件会漂移；`aggregate:check` 通过重新生成和 git diff 作闸门。
- “聚合包纯数据”需精确说法：`packages/all/src/index.ts` 的 `apply()` 是空函数、`inject=[]`，没有聚合业务逻辑；然而包仍导出一个 no-op runtime plugin entry（`lib/index.js`），并非字面上完全没有运行时代码。真实功能逻辑属于成员包。这支持“聚合行为由 patch/dependency 数据表达”，不支持“所有 bundle 包都无需插件入口”。
- 共享库 `@hyzyn/dsh-kit@0.7.3` 没有 `cordis.patch.yml`，也不在 `@hyzyn/dsh-all` 的 11 个依赖中。根 [architecture.md](https://github.com/hyzyn/dsh-plugin-kit/blob/2c6b35bbb50730b9781039d52fd24763e45cbc2e/docs/architecture.md) 说明它是唯一非插件包，被 10 个功能插件作为普通 runtime dependency 引入；`kit-settings` 是唯一例外。目标 [kit manifest](https://github.com/hyzyn/dsh-plugin-kit/blob/2c6b35bbb50730b9781039d52fd24763e45cbc2e/packages/kit/package.json) 依赖 `js-yaml`。逐包 dependency manifests 固定 kit 为 `0.7.3`；仓库 CI 有 `kit-pins:check`，因为重复 kit 会分裂模块级单例。因而“共享库不进 bundles”确指不作为 Loader 行/聚合直接依赖；其代码仍随消费它的插件 dependency graph 安装。
- 挂载顺序是声明行顺序，不是启动先后保证。aggregate patch 把 env 放在前面；其 README 解释 env 启动期同步写入 `process.env`，而 DSH loader 并发 create，真实先后需 `dshEnvReady` 服务依赖表达。不可把 patch row 次序写成 runtime sequencing guarantee。

## SRC-TARGET：Profile 管理面与安装/恢复边界

- `@hyzyn/dsh-profile@0.2.13` 的固定 [manifest](https://github.com/hyzyn/dsh-plugin-kit/blob/2c6b35bbb50730b9781039d52fd24763e45cbc2e/packages/profile/package.json) 提供 `dsh.client` Web 半体；[`src/index.ts`](https://github.com/hyzyn/dsh-plugin-kit/blob/2c6b35bbb50730b9781039d52fd24763e45cbc2e/packages/profile/src/index.ts) 是实质宿主代码。创建、复制、重命名、删除和端口配置操作访问 `dshHome()/profiles/<name>`；profile 列表读取 `package.json` 中有序 `dsh.profile.bundles` 与 dependencies。配置属于各 profile 的 `package.json` / `cordis.patch.yml`；单 profile 端口另存该目录 `profile.runtime.json`，而不是 aggregate 全局状态。
- 创建模板只有 `web` / `headless` 两项映射，未提供 `base` 模板名时使用默认 base bundle；命名校验允许 ASCII 字母/数字/点/下划线/连字符，保留 `node_modules`, `.`, `..`，保护 `web` 不让删除。复制跳过 `node_modules` 和 `pnpm-lock.yaml`，复制完成后在新目录执行 `pnpm install`。对于创建/复制/改名/删除/端口接口，源码均有字段验证与错误响应；Profile 操作不是纯 UI 数据展示。
- 路由有 loopback remote address + Host 校验、拒绝 cross-site fetch、Origin host 匹配，并限制 JSON body 512 KiB。复制失败只删除本次请求创建的目标目录；源/目标存在性预检在创建前，避免旧缺陷中的误删既有 profile。`pnpm install` 失败会被捕获并返回错误，已创建的新目录由调用端回滚。删除 `web` 被拒绝，但删除其他 profile 是递归移除整个目录；无本轮运行验证。
- aggregate patch 本身没有 per-member enable/disable API，也没有 disable rows；独立组件启停应由 profile 用户 patch 的同 id `disabled` 值表达，具体 UI/API 未在 aggregate 中实现。若 patch 顺序/用户 override 冲突、成员包无法解析或部分安装失败，最终有效状态/恢复事务性不可从该 package patch 本身推出。用户应读回 profile roster/effective config，不把安装命令成功等同所有功能可用。
- README 推荐 `dsh plugin --profile web add @hyzyn/dsh-all`，重启 `dsh web` 后生效；按需安装可逐包 add，且同 profile 不应混搭 aggregate 与其成员或根 bundle。README 对“已安装卡片不出现”指向重启与 `dsh --profile web --dump-config` 检查；它未构成对 npm 安装失败恢复原子性或实际修复的运行证据。

## SRC-DSH：仅 bundle patch 语义

- 固定 DSH `dsh-v0.2.1-rc.3` 指向 commit [`1f81c047fc48fa190a683e469daa699857e9afe8`](https://github.com/deepseek-ai/deepseek-harness/commit/1f81c047fc48fa190a683e469daa699857e9afe8)。其 [profile bundle 文档](https://github.com/deepseek-ai/deepseek-harness/blob/1f81c047fc48fa190a683e469daa699857e9afe8/README.md) 将 profile 定义为有序 bundles + 用户 patch；bundle patch 按 `dsh.profile.bundles` 顺序参与组合，用户 patch 在 bundle 层之后。该宿主契约说明为什么 aggregate 是一个可插入 profile 的包；不证明 npm add 成功、依赖安装原子性或用户层任何特定 override 的最终结果。

## TEST / CI / RUN

- **[TEST]** 固定 commit 中的 root manifest 定义 `test: vitest run`，并有 `aggregate:check`、`publishable:check`、`package-contents:check`、`dsh-peers:check`、`kit-pins:check` 等发布一致性脚本。aggregate 检查调用 generator 再比较四个生成文件；它校验声明/生成物同步，不验证用户 profile 安装与启停恢复。当前检查本次只读源码，未执行任何脚本或测试。
- **[CI]** 固定 commit 的 [CI workflow](https://github.com/hyzyn/dsh-plugin-kit/blob/2c6b35bbb50730b9781039d52fd24763e45cbc2e/.github/workflows/ci.yml) 包含三平台 build/typecheck/test、aggregate 及 package contents/peer/kit pin 检查，并有真实 DSH mount/headless render job。GitHub [该 commit checks](https://api.github.com/repos/hyzyn/dsh-plugin-kit/commits/2c6b35bbb50730b9781039d52fd24763e45cbc2e/check-runs) 显示完成成功，包括 macOS/Ubuntu/Windows build、真实 DSH mount/headless render、publish 和 concurrent full-suite flake lane。远端 check 是该 SHA 的 CI 记录，不是本轮复跑；仓库里的 tests 也不等于测试覆盖了 npm 安装后的真实恢复路径。
- **[RUN]** None。本轮没有安装、构建、执行 CLI/插件或改动任何 profile；没有测试交互式启停、失败后修复、跨版本迁移或实际 UI。

## 可迁移结论与边界

当一组功能包仍要独立安装且可选择启用时，可将包解析依赖与 Loader row roster 分开：aggregate 只依赖精确版本的成员并生成有序 insert rows，成员功能仍由各自包实现；公共宿主工具作为普通共享 library dependency，而非 bundle row。收益是 one-command convenience 不吞掉单包身份；成本是发布时必须保持 dependency/patch/id 三方一致，重复安装会碰 ID，成员更新依赖 aggregate 发布。必须在自家环境明确同 profile 重复安装策略、profile override、依赖安装失败回滚和有效配置读回；本样本的 generator/check 只能证明仓库自洽，不能保证任意 profile 的安装原子性。若 aggregate 加入真正业务逻辑，它就已不再是“仅挂载”的包，卸载/启停也不再只影响数据层。
