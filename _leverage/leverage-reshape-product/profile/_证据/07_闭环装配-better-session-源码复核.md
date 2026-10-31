---
title: "源码复核：闭环装配 better-session"
domain: reshape-product
kind: evidence
positioning: "核验 profile/17 的 npm 发布坐标、bundle rows/config 与会话生命周期；发布源码不能与 0.1.10 对齐时，不将后续源码或文档主张推成实现事实。"
read_when: "核对 better-session 发布物、数据 owner、会话动作和恢复边界。"
status: observed
updated: 2026-10-31
---
# 源码复核：闭环装配 better-session

> 本轮只读第一方 npm 发布元数据/CDN 发布文件、GitHub 源码 API 与 DSH 上游固定源码；未安装、构建或运行目标代码。`[DOC]` 是发布 README 主张；`[SRC-TARGET]` 仅用于与 npm 精确版本匹配的源码，不能把该包内生成的 patch 自动等同于完整源码实现；`[SRC-DSH]` 是 DSH 固定版本契约；`[TEST]` 是测试定义/CI 文本，不是本轮测试结果；`[CI]` 记录可否绑定远端检查；本轮无 `[RUN]`。

## 坐标与来源边界

- **[DOC]** 目标是 `morlay/dsh-plugin` 的 npm `@morlay/better-session@0.1.10`。第一方 [npm 0.1.10 metadata](https://registry.npmjs.org/@morlay%2fbetter-session/0.1.10) 指向 [不可变 tarball](https://registry.npmjs.org/@morlay/better-session/-/better-session-0.1.10.tgz)，SHA-1 `e357b7727d6310e0d42e1de6e91b39dc5cb13a39`，SHA-512 integrity `sha512-KndeyOFl3l5s1mqPF4SB73ATBdnSygLFW2QqdlgCH6ItlcCWpEDUD+zLxJTWooDlLe6uIiFjqMyJA7agNo3E8w==`。metadata 没有 `gitHead`。版本化 [package.json](https://cdn.jsdelivr.net/npm/@morlay/better-session@0.1.10/package.json) 声明 exact dependencies：`session-branch@0.1.9`、`session-rdb@0.1.9`、`ui-conversation-manager@0.1.10`、`ui-conversation-message-actions@0.1.10`、`dsh-reference@0.0.10`；Cordis peer `^4.0.5`；DSH engine `>= 0.2.1-rc.1 < 0.2.2`。这是发布身份和依赖图，不是源码 commit pin。
- **目标源码 provenance gap。** 第一方 [GitHub tags API](https://api.github.com/repos/morlay/dsh-plugin/tags) 返回空列表。GitHub [better-session package.json path history](https://api.github.com/repos/morlay/dsh-plugin/commits?path=packages/bundles/better-session/package.json&per_page=100) 可见后来 commit `3f3edd432e892b35fb0c1e7e1d9ae66e3bc58e9`，但其 [固定 commit manifest](https://github.com/morlay/dsh-plugin/blob/3f3edd432e892b35fb0c1e7e1d9ae66e3bc58e9/packages/bundles/better-session/package.json) 是 `0.1.11-alpha.0`、DSH `>=0.2.2-alpha.2 <0.2.3`，依赖仍是 workspace ranges；既不是 0.1.10，也不能对应上述发布产物。该 SHA 不能作 0.1.10 的 `[SRC-TARGET]`。本 memo 不从默认分支/HEAD、后续 alpha、生成 patch 或发布 README 推断 0.1.10 的包源码、schema、生命周期实现、测试及 CI。
- **[SRC-DSH]** DSH 对照版本固定为 tag `dsh-v0.2.1-rc.3`，commit [`1f81c047fc48fa190a683e469daa699857e9afe8`](https://github.com/deepseek-ai/deepseek-harness/commit/1f81c047fc48fa190a683e469daa699857e9afe8)。只核对 bundle patch/config 和 session 语义所需宿主契约，不把宿主能力当成目标功能已验证。

## 发布文档与发布 patch 可直接确认的内容

- **[DOC]** 版本化 [README](https://cdn.jsdelivr.net/npm/@morlay/better-session@0.1.10/README.md) 将包描述为一次装配五个依赖，官方 `ui-conversation` shell 保留，扩展注册在 `conversation.chat.node` / `conversation.composer.dock`。它称 edit 将 user 消息及后续内容 rewind 回输入框而不重放；retry 对闭合回合重放并可 truncate 后续；fork 从闭合边界建新会话。README 示例列 `ctx.sessionEditor.retry({ action:"retry", sessionId, turn, cascade:"truncate" })`、`ctx.sessionBranch.rewind(sessionId, seq)`、`forkFrom(sourceId,{atSeq,childSessionId})`。这些是 DOC 行为意图，不能证明 UI 实际调用参数、权限/确认、持久化原子性、重启后结果或副作用恰好一次。
- **[SRC-TARGET:发布物内清单，非包源码]** 第一方 [0.1.10 cordis.patch.yml](https://cdn.jsdelivr.net/npm/@morlay/better-session@0.1.10/cordis.patch.yml) 明示由生成器产生。patch 禁用 `session-persistence-jsonl`、`session-projection-cache`、`session-query-sqlite`、`storage-json`；将 `storage-domain` config.backend 设为 `rdb`；插入 `session-branch`、`session-rdb`、`ui-conversation-message-actions`、`ui-conversation-manager`、`reference`。`session-rdb` 行 config 显式 `{type: sqlite, path: !!js dshHomePath('sessions','sessions.sqlite')}`。由此能确认发布 patch 的 rows 和该行配置值，不足以确认其他 row 在所有 lower-layer/profile 组合中的最终 effective config，也不足以断言所有 session 数据都归单一数据库。
- **[SRC-TARGET:发布包图]** 包发布 metadata 的 dependencies 固定上述五个版本；patch 插入的五行名称与五个依赖名称对应（`reference` 对应 `@morlay/dsh-reference`）。这是发布物可见的实现装配图。由于没有匹配的 0.1.10 源码 commit，生成器如何计算 rows、是否校验依赖对齐、不同 patch 顺序如何合并仍为 `[OPEN]`。
- **配置 ownership / preset line list。** 本发布 patch 仅能证明对 `session-rdb` 行写入 SQLite type/path，并关闭五个其他 rows、插入五行。它不含 agent preset 行清单。`mydsh-profile` 或仓库 HEAD 的 preset patch/测试不能归属到本版本 `better-session`；其复制和更新义务不在此包证据范围内。profile/home/CLI 是否再覆盖这些 values，需结合宿主层序解释，不能把 bundle 默认值写成用户最终配置。

## DSH rc.3 对照（最小必要范围）

- **[SRC-DSH]** Pin 为 `dsh-v0.2.1-rc.3` → [`1f81c047fc48fa190a683e469daa699857e9afe8`](https://github.com/deepseek-ai/deepseek-harness/commit/1f81c047fc48fa190a683e469daa699857e9afe8)。样本 package metadata 的 engines 区间包含 rc.3，但这只是声明的兼容范围，不是兼容测试结果。
- rc.3 profile patch layering 与新 session generation 仅在判断“bundle patch 默认值是否等于最终配置”“profile 改动是否追溯既有 session”时相关。已有 pinned rc.3 核对记录指向 [app-boot merge](https://github.com/deepseek-ai/deepseek-harness/blob/1f81c047fc48fa190a683e469daa699857e9afe8/packages/boot/app-boot/lib/index.js#L61-L109)、[profile boot order](https://github.com/deepseek-ai/deepseek-harness/blob/1f81c047fc48fa190a683e469daa699857e9afe8/packages/boot/profile-boot/lib/index.js#L223-L246) 及 [New Session generations guide](https://github.com/deepseek-ai/deepseek-harness/blob/1f81c047fc48fa190a683e469daa699857e9afe8/docs/upgrade-guide/v0.2.1-alpha.1/new-session-generations/guide.md)。因此 patch 中的 `session-rdb` SQLite config 是 bundle 层默认值，不足以证明 profile 最终 effective config 或 target retry/rewind/fork 实现服从/如何使用该 session contract。宿主契约不填补目标源码缺口。

## 会话数据账本与生命周期

- **持久化位置（[SRC-TARGET:发布清单]）**：默认 target path 为 `$DSH_HOME/sessions/sessions.sqlite`，`type: sqlite`。这证明 bundle 对 `session-rdb` 行的发布默认值，不证明当前 profile 最终值、目录创建/权限、并发锁、连接池、加密、备份、schema migration 或多进程写入行为。
- **schema / IDs / owner（[OPEN]）**：session、event、projection、revision、turn 和 branch 的表结构、字段约束、主外键、seq/revision 分配、幂等键、迁移版本均无法归于 0.1.10 的匹配源码。不能从 README 的 `sessionId`、`turn`、`atSeq` 参数或卡片摘述反推 schema。RDB backend 具体实现 owner 与 `storage-domain` 的事务边界亦未确认。
- **Edit / retry / retract（[DOC]）**：edit 是回填输入框而不自动重发；retry 是按 turn 重放且 `cascade: truncate`；rewind 会把指定消息及之后内容从可见会话推进撤回到输入框。目标实现是否先校验闭合边界、截断谁的 durable events/projections、是否存在确认取消、动作中断后可否重试、已发出的外部 tool side effect 是否可撤销均 `[OPEN]`。对已产生外部副作用的回合，“truncate”不等于撤销工具副作用。
- **Fork（[DOC]）**：README 声称从 `atSeq` 创建新会话且保留原会话。复制的是事件前缀、投影、元数据还是共享引用，child ID 冲突如何处理，源会话在读取与写入之间并发变化时的 snapshot 语义，均无 pinned target source。
- **Workspace scope（[OPEN]）**：发布 patch 的 home path 可见，但 session 是否按 workspace/project/profile/user 分区、workspace 切换是否过滤已有行、跨 workspace fork/rewind 是否受阻无法确认。不能将 `$DSH_HOME` 路径等同于 workspace scoping。
- **preset line list（[OPEN/不适用本 bundle]）**：`better-session@0.1.10` 自身 patch 未声明 preset rows。不能借用其他 sibling bundle 的 preset 行清单或其 drift tests 支撑本卡主张。

## 安全、兼容与恢复边界

- **Mutation/replay safety [OPEN]**：关键需核的对抗场景包括同 session 两个编辑/重试并发、durable event head 超过 UI projection、重试期间取消/进程退出、写事件成功而 projection 更新失败、部分数据库事务完成、fork 写入到一半、重启后再次点击动作，以及 retry 重跑有外部副作用的 tool call。没有 matching source/test 依据，不能称这些路径幂等、原子或可恢复。
- **版本兼容 [DOC]**：0.1.10 声明 DSH 范围 `>=0.2.1-rc.1 <0.2.2`，故 rc.3 落在声明区间内；这只代表 metadata 约束兼容，不代表已在 rc.3 运行通过。依赖为 exact 五包版本，Cordis peer 是 `^4.0.5`。依赖安装解析、rc.3 实际兼容、旧 session DB upgrade/downgrade 均未实测。
- **Failure/recovery [OPEN]**：坏 schema/坏 event、SQLite 文件只读/损坏/磁盘满、目录缺失、迁移失败、profile row missing/disabled、patch parse fail、workspace scope 错配、版本回滚，以及部分提交后的 UI 状态一致性均没有目标版本源码支撑。不得把目标 README 的确认弹窗或 bundle“一次装齐”解释为故障恢复保证。

## TEST / CI / RUN

- **[TEST]** 没有匹配 0.1.10 源码 commit，故本 memo 不归属具体测试源码/覆盖给该发布版本。发布 metadata 仅暴露 `build` script；测试文件、兼容矩阵、坏数据/重试/恢复测试没有版本对应证据。
- **[CI]** 未找到可与 npm tarball digest 或 `0.1.10` git commit 对齐的第一方 workflow run/check。README、CI workflow 配置、后来 commit message 中的测试数字都不证明 0.1.10 CI 通过。
- **[RUN]** None。本轮按要求未安装、构建、执行或修改目标/DSH；未打开 DB、改 profile、创建/编辑/重试/撤回/fork session，也未运行任何测试。

## 结论与可迁移边界

发布物本身可确认依赖图、DSH engine 声明及 bundle patch rows/config，README 可确认产品意图；但 GitHub 没有 tag，npm metadata 没有 `gitHead`，可见 path-history commit 对应的是后续 `0.1.11-alpha.0`。因此本次没有可 pin 的 `[SRC-TARGET]` 源码版本。最稳妥的结论是：**“rows 与默认 config 同包发布”在 npm 0.1.10 的 patch 产物层可直接观察；session schema、状态 owner、edit/retry/retract/fork 的状态迁移、workspace scope 和失败恢复仍为文档级/开放项。** 不要据此将 profile/17 中的闭环状态机和安全性写成源码已核，也不要把 sqlite path 误当 workspace 隔离或把 replay 当副作用撤销。

升级源码级复核需先取得作者提供的 0.1.10 build commit/source provenance 或可逐文件校验的 tarball 源码映射；然后固定五个依赖的各自 tarball integrity 和源码坐标，跟进 schema/migrations、事件序与 projection、并发/幂等、UI 确认入口、DB 错误恢复、workspace 过滤、fork snapshot，以及相同 SHA 的测试和 CI 记录。
