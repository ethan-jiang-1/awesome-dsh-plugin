---
title: "源码复核：环境搬家 dsh-config-manager"
domain: reshape-product
kind: evidence
positioning: "对 dsh-config-manager 的导入流水线、快照与回滚边界、冲突裁决、外部来源翻译、密钥/压缩包安全作固定提交的一手源码复核；本文件为证据，不替代样本卡。"
read_when: "核对导入写入起点、快照回滚、冲突裁决、外部来源翻译与密钥/压缩包安全。"
status: observed
updated: 2026-11-01
---
# 源码复核：环境搬家 dsh-config-manager

> 取证时点：2026-11-01。只读 npm registry、GitHub API 与固定 commit 的 raw 源文件；**未安装、未构建、未运行目标代码**，未下载 tarball。下文 `[DOC]` = 上游 README/文档主张，`[SRC-TARGET]` = 目标仓库该 commit 的实现，`[SRC-DSH]` = DSH 宿主契约（本轮只经目标仓的类型声明间接观察），`[TEST]` = 测试源码存在性与覆盖意图，`[CI]` = workflow 声明与**该 commit 的 check-run 元数据**，`[RUN]` = 本次运行事实。目标固定为 commit [`babd759693bcbbd1da259a53d7d308728c0f0b8f`](https://github.com/xiajiajun516/dsh-config-manager/commit/babd759693bcbbd1da259a53d7d308728c0f0b8f)（tag `v0.2.3`，2026-10-31T14:02:04Z）；所有目标代码链接均 pin 此 commit。

## Provenance 与版本界限

- **npm 侧**：`registry.npmjs.org/dsh-config-manager` 的 `dist-tags.latest = 0.2.3`，该版本 `gitHead = babd759693bcbbd1da259a53d7d308728c0f0b8f`，发布时间 `2026-10-31T14:07:58Z`；`dist.attestations.provenance.predicateType = https://slsa.dev/provenance/v1`，`_npmUser.trustedPublisher = github/OIDC`。
- **GitHub 侧**：tag `v0.2.3` 指向 commit `babd7596…`，与 npm `gitHead` **逐字一致**。因此「npm 0.2.3 ↔ tag v0.2.3 ↔ 本文件审计的树」三者对齐；`publish.yml` 由 `tags: v*` 触发并用 `npm publish --access public --provenance`（[`publish.yml`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/.github/workflows/publish.yml#L1-L14) 与 [#L129](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/.github/workflows/publish.yml#L129)），与 registry 的 OIDC 发布者/attestation 相容。这是**声明与元数据一致**，不等于本次比对过 tarball 内容。
- **样本卡写的是 `0.2.2`**。核对同样成立：npm `0.2.2` 的 `gitHead = d39177950476ac1ff9ee948dfcbeaa059fcfa632`，tag `v0.2.2` 也指向 `d391779…`。所以卡片版本不是编造的，但它当时是 README 级证据，未读源码。
- **版本迁移不改变结论**：`compare v0.2.2...v0.2.3` = 6 commits / 17 files，全部落在 locale、文案、`package.json`/lock、CHANGELOG/DESIGN 与 `src/routes/messages.ts`（本地化消息路由），**没有** `src/core/`、`src/security/`、`src/foreign/`、`src/utils/zip.ts` 的改动。故本文对导入/安全/翻译路径的结论在两张版本上都成立；但「卡片作者读的是 0.2.2 的实现」仍不可回推——它只读过 README。
- **签名**：该 commit `verification = {verified:false, reason:"unsigned"}`。tag→commit 的绑定存在，但没有签名校验；本文不把 provenance 说成「已签名验证」。
- **未取**：npm tarball（`fileCount 1668` / `unpackedSize 24.7 MB`）未下载，`lib/*.js` 构建产物与仓库 `src/` 的一致性未比对 → `[OPEN]`。

## DOC

- README 的导入流程图把顺序写死为「选 ZIP → 校验 → 完整性 → schema → 兼容 → 扫描 → 计划 → consult → 选内容 → 逐项冲突 → 路径/密钥 → 确认 → 快照 → 应用 → 校验」，并写明「失败中途自动还原、可在确认页关闭」，见 pinned [`README.md`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/README.md#L145-L156)。
- README 明确「未勾选的条目既不被导入也不进快照」「冲突逐项保留当前/用备份，含批量按钮」「安全快照先于应用」：同文件 [#L267-L272](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/README.md#L267-L272)。
- `read failed 而不是 0` 的原文在**导出构成卡**一节：「unreadable sections say "loading / read failed" instead of a fake 0」，见 [#L290](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/README.md#L290)。样本卡把这条推广到导入报告，README 并未这样写。
- 「翻译成标准 bundle、复用同一条预览/冲突/快照/回滚」见 [#L74](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/README.md#L74)；「先剥密钥再打包」「默认不含密钥值」见 [#L42](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/README.md#L42) 与 [#L142](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/README.md#L142)。
- README 对「快照 Restore」写的是「整文件恢复 + 卸载新增插件」，见 [#L108](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/README.md#L108)。这是**Library 快照恢复**的动作，不是导入失败时的自动回滚——两者在源码里是两条路径（见下）。
- 作者自己的设计文档说明外部来源必须复用标准包而不是第二条写入通道，见 [`docs/design/2026-10-04-foreign-import-v1.md`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/docs/design/2026-10-04-foreign-import-v1.md)。文档存在只证明作者这样设计，不证明实现无分叉。

## SRC-TARGET

### 1. 流水线：读操作与写操作的分界

- 门面把流程写成 **14 步**（选 ZIP → 校验 → manifest → 完整性 → schema → 兼容 → 扫描 → 计划 → Preview → 确认 → 快照 → 执行 → 校验 → 结果），并声明「analyzeImport / createImportPlan 零写入（ZIP 全程内存解析，不进磁盘）」、`executeImportPlan` 必须显式 `confirm`，见 [`src/core/importer.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/importer.ts#L1-L10)。**样本卡说「十二步」、源码注释说 14 步、README 画的是 12 个箭头**——三者描述同一批阶段，只是切分粒度不同；引用步数时应说明口径。
- 只读阶段确实在 HTTP 层就分开：`/analyze` 只 `analyzeImport` 并回 200（[`src/index.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/index.ts#L3639-L3671)），`/plan` 只 `createImportPlan` + 计划期阻断（[#L3683-L3730](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/index.ts#L3683-L3730)）。`createImportPlan` 内部只读墓碑文件与设置、生成计划项，不调用任何 adapter 写入（[`src/core/analyzer.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L771-L846)）。`[SRC-TARGET]` 支持「计划阶段零写盘」。
- **写相位起点不在 `createSnapshot` 之后，而是更早**：`/execute` 先过 `withMutationGate('import-apply', …, { deferredSnapshot: true })`（[`src/routes/import.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/routes/import.ts#L179-L207)），journal 已在宿主侧落盘；进入引擎后 `executeImportPlan` 先用 `refresh` 重新读包（不复用跨请求缓存），再强制 `confirm === true`、再校验「加密备份必须已解密」（[`src/core/analyzer.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L889-L905)），随后 `createSnapshot` 把快照写入 `$DSH_HOME/dsh-config-manager/snapshots/…`（[#L921-L939](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L921-L939)），再做逐项 WAL 预登记（[#L941-L967](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L941-L967)），最后才 `applyOne`。
- 也就是说：**用户配置的第一笔写发生在「快照已落盘 + journal 已 APPLYING + 全部计划项已预登记 planned」之后**。这是卡片的「写入排在最后」在实现层的准确版本；把它说成「点确认前零写盘」不准确——确认后、动配置前仍会先写快照与 journal（这是有意的可回滚设计，不是泄漏）。
- 另有两条与配置无关的暂存写：`/upload`、`/decrypt-archive`（解出的明文 ZIP 用 0600 写进受控 tmpDir）、`/foreign-import` 产包，均不触碰 `$DSH_HOME` 配置（[`src/routes/import.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/routes/import.ts#L98-L177)、[`src/routes/foreign.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/routes/foreign.ts#L1-L30)）。

### 2. 快照覆盖的是「计划项的 target」，不是「盘上实际写的全部」

- `collectTargets(plan)` 只遍历 `plan.items`，且只收 `planItemWritesTarget(item) && item.target !== undefined` 的项（[`src/core/backup.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/backup.ts#L293-L306)）；`planItemWritesTarget` 把 `Skip`/`Warning`/`MissingDependency`/`Error` 与未采纳的 `Conflict` 全部排除（[#L58-L70](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/backup.ts#L58-L70)）。快照=「计划里会写的项」的集合，与执行侧同源（`analyzer.applyOne` 用同一谓词判断是否调用 adapter）。
- 快照内容 = adapter 自己的 `snapshot()`（若有）或引擎兜底条目；另加三份宿主整文件 `settings.yaml` / `settings.json` / `cordis.patch.yml`（[`HOST_FILE_CANDIDATES`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/backup.ts#L78-L82)、[#L505-L506](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/backup.ts#L505-L506)），以及导入前插件清单 `beforePlugins`（[#L509-L514](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/backup.ts#L509-L514)）。
- **两处真实缺口**，都可由代码直接读出，不需要实测：
  1. **分区收尾写入不在快照目标集**。`finalizeApply` / `finalizeImport` 在计划项之外产生写入（`executed.push({itemId: adapter+':finalize'…})`），但 `collectTargets` 只扫 `plan.items`（[`src/core/analyzer.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L1083-L1144) 与上引 `collectTargets`）。因此收尾阶段新写的文件（如会话登记相关落盘）没有对应快照条目，失败回滚不会还原它们。
  2. **自动回滚不卸载插件**。`rollback()` 逆序补偿的 entry 只有 `settingsNamespace` / `credential` / `patchLine` / `file` / `workspaceRecord`，没有插件卸载分支（[`src/core/rollback.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/rollback.ts#L26-L124)、[#L124-L156](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/rollback.ts#L124-L156)）。插件撤销只存在于**快照恢复**路径：拿 `beforePlugins` 与当前已装比对、生成 `pluginRemove`（[`src/core/restore.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/restore.ts#L675-L700)）。`[SRC-TARGET]` 结论：**「导入失败自动还原」= 还原文件/设置/凭据状态，不包含卸载这笔导入期间装上的插件**；要撤销插件得事后在 Library 用这笔快照做 Restore。样本卡 §5「回滚范围要含卸载新增插件」在自动回滚这条路径上**尚未实现**，实现的是「快照可恢复」这一半。
- 回滚本身是诚实的降级而非全等：`settings` 原 namespace 不存在时无法恢复「不存在」（DSH 无删除语义）→ 记 failed + manualHint（[#L33-L49](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/rollback.ts#L33-L49)）；`credential` 原已配置时**值不可回读**，一律 failed + 人工补录（[#L56-L70](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/rollback.ts#L56-L70)）。回滚报告 `full/partial` 由「失败条目数为 0」判定，不是「盘面已证等价」。

### 3. 部分失败：三种非致命与一种致命

- 每项结果只有 `ok` / `warning` / `failed` / `skipped`；只有 `failed` 计入 `anyFailed`，`warning` 是**非致命**（目标不可达等，不触发回滚），见 [`src/core/analyzer.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L1077-L1081)。`rollbackOnError` 缺省 **false**：单项失败如实记录并继续；显式打开才在项边界 `break` 并整笔回滚（同文件 [#L1112](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L1112)、[#L1216-L1218](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L1216-L1218)）。
- 收尾抛错被降级成 warning，且会把「终态部分保留」的语义留在报告里（[#L1086-L1096](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L1086-L1096)）；执行后校验失败也只进 warnings（[#L1220-L1234](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L1220-L1234)）。**「校验」是告警不是门禁**——卡片说「应用 → 校验」时不要读成校验失败会回滚。
- 用户终止只**在计划项边界**生效，绝不在项中途 abort（避免半装插件/半写文件）；安全点后询问「回滚 / 保留」，通道抛错或超时一律按回滚（[#L982-L1000](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L982-L1000)、[#L1017-L1021](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L1017-L1021)）。「保留」分支会补齐收尾、把未执行项写成 `skipped`、跑启动自洽审计，并**刻意不把快照标成 done**（[#L1152-L1213](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L1152-L1213)）——快照保持可用是「保留」的可撤销承诺。

### 4. 逐项冲突：UI 硬阻断，引擎只跳过

- 决策语义集中在零依赖纯函数：`keepCurrent → Skip`、`useImported → Update`、`review/未决策 + skipExisting → Skip`、`review/未决策 + replace → Update`，其余保持 `Conflict` 原样（[`src/core/conflict-decisions.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/conflict-decisions.ts#L17-L34)）。
- 界面上确有「不解决就不能走」：冲突阶段的主按钮 `disabled={collector.hasUnresolved}`（[`import-wizard-steps.tsx`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/client/import/import-wizard-steps.tsx#L264)），`hasUnresolved` = 决策为 `review` 或未决策的项（[`src/ui/conflict-view.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/ui/conflict-view.ts#L50-L58)）。这是产品判断，`[SRC-TARGET]` 支持。
- 但**服务端没有这条不变量**：`/execute` 只校验 `plan.items` 是数组、会话格式处置与加密态，不校验「计划里是否还有未决 Conflict」（[`src/routes/import.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/routes/import.ts#L194-L207)）；引擎对未采纳的 `Conflict` 直接不算写目标（`planItemWritesTarget` 返回 false），于是走 `applyOne` 的 skipped 分支（[`src/core/analyzer.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L1436-L1454)）。结论：**「未决冲突会卡住整个导入」是向导 UI 的保证，不是导入引擎的保证**。拿脚本直连 `/execute` 时，未决冲突在 `merge` 策略下被静默跳过（`replace` 策略下则被直接覆盖），而不是 409。风险受 loopback 围栏限制（[`src/routes/kit.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/routes/kit.ts#L156-L200)），但契约层面应写明。

### 5. 外部来源：翻译成标准 bundle v1，再进同一条流水线

- `[SRC-TARGET]` 与文档一致，不是第二套导入器：`/foreign-import` 只把来源译成标准包、写进受控 tmpDir 并返回 `zipPath`，注释把四条边界写死（只写 tmpDir、不做导入、凭据值不进响应、空结果不报成功），见 [`src/routes/foreign.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/routes/foreign.ts#L1-L30)。
- 翻译产物复用 `writeZip` + `buildManifest` + `buildChecksums`，并额外写一个**只含标识与计数**的 `manifest.foreign`（来源、位置、项目、插件元数据、`skipped` 码与计数、凭据引用名），见 [`src/foreign/bundle.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/foreign/bundle.ts#L1-L149)。`checksums.json` 不覆盖 `manifest.json`，所以「有/无 origin」两种包的内容摘要相同——作者自己写明这是刻意取舍。
- **源码自述的已知缺陷**：`source.dshVersion` 填的是**导入目标机**的版本，于是兼容性评分被构造性拉满（bundle.ts 头部注释，[#L8-L13](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/foreign/bundle.ts#L8-L13)）。这直接回答了样本卡「compatibility 评分怎么算」的一部分：外部来源包的评分对它没有信息量。
- 凭据不变量在翻译层就守住：外部 token/key 由导出侧同一个 `defaultSecretScanner` 剥离（命中字段值置空串），只留字段名与引用名，「值绝不进包」，见 [`src/foreign/types.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/foreign/types.ts#L11-L14)。这支持卡片「密钥只记键名」的说法，且不是靠导入侧再过滤一次。

### 6. read failed ≠ 0：导出构成卡做到了，导入计数没有同款通道

- 有独立的渲染状态机：`SectionCompositionState = 'ready' | 'loading' | 'failed'`，非 ready 时**不渲染 0 条目 / 0 B**，改渲染「loading / 读取失败」加 `—`，并注释说明「0 会被读成这一项没有内容，而引擎对清单缺失的分区按整体导出处理（语义相反）」，见 [`src/client/common/SectionComposition.tsx`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/client/common/SectionComposition.tsx#L15-L29) 与 [#L52-L70](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/client/common/SectionComposition.tsx#L52-L70)。`[SRC-TARGET]` 支持卡片这条，但适用面是**导出/总览**。
- 导入侧的同类诚实是另外两种形态：ZIP 读不出来时抛 `import.readFailed`（带路径与原因），不是「0 个分区」（[`src/core/analyzer.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L283-L287)）；会话格式探针用 `unreadable: {unitId, version}[]` 表达「本机读不了」，并逐项打 `formatUnsupported` 标记而不是折算成 0（[#L802-L815](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L802-L815)）。
- 但导入预览的**计数**没有 NULL 通道：`previewSummary` 里 `pluginsInstalled: analysis?.pluginSummary.installed ?? 0`、`conflicts: count([...])` 等一律落成数字（[`src/ui/import-wizard.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/ui/import-wizard.ts#L430-L456)）。所以卡片「所有汇总数都要允许 NULL」是它**建议你抄的规则**，不是这个样本在导入侧已做到的实现——样本只在导出构成卡与两类诊断字段上做到了。

### 7. 密钥与凭据：不复制值，失败如实

- 扫描器是第二道防线（第一道是 `settings.describe({redactSecrets:true})`），按字段名 + 值形状剥离，命中记录只含路径与字段名、**值永不外泄**，见 [`src/security/secret-scanner.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/security/secret-scanner.ts#L1-L31)；日志侧另有结构化字段 + 值形状 + URL userinfo + 高熵串的脱敏器，[`src/security/redaction.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/security/redaction.ts#L1-L30)。
- 导入时值只走内存：`secretInputs` 来自请求体、只经 adapter 写入；执行日志在宿主侧先 `redact()` 再落 run 账（[`src/routes/import.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/routes/import.ts#L241-L304)）。「值是否可用」只有一条判据 `usableSecretValue`（非空字符串），修掉了「空串也算已满足」的旧错（[`src/core/import-planning.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/import-planning.ts#L237-L246)）。
- 加密不变量是硬拒绝：manifest 标了 `encrypted` 但没注入解密结果 → 直接抛「需要密码」，不允许静默降级成「缺凭据照常导入」（[`src/core/analyzer.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/analyzer.ts#L900-L905)）。凭据回滚不可回读时如实失败（见 §2）。
- **一处残留窗口**：`/decrypt-archive` 解出的明文 ZIP 以 0600 写进 tmpDir，注释说「用完即清」，实现只在**导入成功**后立刻删；失败/取消时保留以便重试，靠 tmpDir 的 24h 保留期兜底（[`src/routes/import.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/routes/import.ts#L160-L163)、[#L305-L312](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/routes/import.ts#L305-L312)）。「用完即清」对失败路径不成立。

### 8. 压缩包安全：默认最严解析，解压函数无仓内调用方

- `parseZip` 默认即最严：条目名 `isPathSafe`（拒 `..`、绝对路径、盘符、UNC、NUL）、重复名、symlink 条目（central directory 的 `S_IFLNK`）、本地头越界、条目数/压缩总量上限，任一不满足**整体拒绝**（[`src/utils/zip.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/utils/zip.ts#L465-L521)，判定点 [#L503](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/utils/zip.ts#L503)、[#L506](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/utils/zip.ts#L506)、[#L508-L510](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/utils/zip.ts#L508-L510)）；条目名规则本身在 [`src/utils/paths.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/utils/paths.ts#L33-L42)。
- 读取阶段另有 CRC32 / 声明尺寸 / 解压总预算 / 压缩比四道校验（zip bomb 向量），见 [`ZipArchive.accept`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/utils/zip.ts#L428-L452)。
- 落盘侧 `safeExtractHardened` 逐条 `lstat` 复查「必须是普通文件」，异常即清空目标目录并抛出（[`src/security/zip-security.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/security/zip-security.ts#L60-L105)）。但 `safeExtract` / `safeExtractHardened` 在 pinned 树里**只有定义、没有仓内调用方**（`src/utils/zip.ts#L538` 与 security 层），导入路径从不把 ZIP 条目解压到磁盘——文件类分区由 adapter 读内存内容再经 fs 门面写目标。因此 Zip Slip 的实际风险点不在「解压」，而在「adapter 目标路径解析」，后者另有 reserved 前缀与 `isSameOrChild` 围栏（[`src/utils/paths.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/utils/paths.ts#L54-L66)）。另：本仓从不创建 symlink（只 `fs.writeFile`），`S_IFLNK` 拒绝属纵深防御而非唯一防线。

## SRC-DSH

- 本轮**没有重读 DSH 源码**，因此不更新样本卡「基线 DSH `0.2.1-rc.3`」的兼容性结论。宿主依赖只经目标仓的类型声明间接看到：`settings.describe(namespace,{redactSecrets})` 返回带乐观锁 `revision` 的命名空间、`settings.replace(…, expectedRevision)` 冲突即抛；`credentials.describe` **只返回状态、永不返回值**，只有 `set/unset`，见 [`src/core/types.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/types.ts#L203-L228)；`plugins.listInstalled` 见同文件 [#L250](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/types.ts#L250)。这些是**目标插件对宿主的假设**，不是 DSH 实现证据；DSH 是否真的不提供凭据值回读、`settings.replace` 的 revision 语义如何，需要按 DSH 固定版本另核 → `[OPEN]`。
- 作者注释称导入/导出/恢复等 **83 条路由**由 DSH webServer 注册（[`src/routes/index.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/routes/index.ts#L1-L9)）。本轮未在 DSH 侧核实注册/围栏语义，因此本文所有「零写入」判断只限**插件 HTTP 边界以内**，未覆盖宿主 `runJournaled` 的 journal/lock 写盘（那部分在 `src/index.ts`，未逐行读）。

## TEST

- 导入主链有逐语义测试：`I-01` 全流程、`I-02` merge 下未决策**不覆盖**、`I-03` replace、`I-05` useImported、`I-08` 未补录密钥**不落盘**、`I-09` 未确认 → 零写入，见 [`tests/core/importer.test.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/tests/core/importer.test.ts#L62-L314)。`I-02`/`I-09` 与 §3/§4 的结论互证。
- 安全侧有独立用例：畸形 ZIP、损坏中央目录、超条目数、checksum 不匹配/缺失、Zip Slip（`../` 与绝对路径），见 [`tests/security/import-security.test.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/tests/security/import-security.test.ts#L77-L175)（`S-01`…`S-06`）。这证明**测试作者认为**这些向量必须拒绝；本次未运行，不构成「已拒绝」的实测结论。
- 取消/保留路径有 `C-01`…`C-06`（含「决策通道抛错按安全侧回滚」「保留但未注入审计必须告警」），见 [`tests/core/import-cancel.test.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/tests/core/import-cancel.test.ts#L92-L213)。
- 目标侧 symlink 有专门回归：`B-1`…`B-4` 覆盖 `..` 越界、目标目录为 junction/symlink、目标文件本身是 symlink、home 位于链接祖先之下，见 [`src/core/restore-target-symlink.test.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/src/core/restore-target-symlink.test.ts#L114-L196)。注意这是**恢复**路径，不是导入路径。
- 脱敏有源码守卫（渲染 `analysis.warnings` 必须逐项 `redact()`），见 [`tests/client/import-wizard-redaction.test.ts`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/tests/client/import-wizard-redaction.test.ts#L51-L86)。
- 覆盖缺口：没有「回滚会卸载导入期间新增插件」的用例（因为实现不做，见 §2）；没有「服务端拒绝含未决 Conflict 的计划」的用例（因为不拒绝，见 §4）；没有「失败后明文解密副本被清理」的用例（因为只在成功路径删，见 §7）。

## CI

- `ci.yml` 声明 PR/主干门禁：三平台矩阵（ubuntu、windows 硬门禁；macOS 标记 `experimental: true` → `continue-on-error`），步骤为 `npm ci --legacy-peer-deps` → typecheck → typecheck:tests → `npm test` → build → bundle 自包含守卫 → 打包 dry-run，见 pinned [`.github/workflows/ci.yml`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/.github/workflows/ci.yml#L62-L124)。作者在注释里承认存在负载相关的间歇失败并建议先 rerun 再判缺陷——这降低「红灯=回归」的信噪比。
- 该 commit 的 check-run 元数据（GitHub API，2026-11-01 读取）：`Typecheck / Test / Build (ubuntu-latest)` success 2026-10-31T14:04:40Z、`(windows-latest)` success 14:06:23Z、`(macos-latest)` success 14:04:31Z、`publish` success 14:04:57Z，共 4 条全部 success。这是**该 commit 的 CI 结论**，比「workflow 存在」强；但它仍不是本地复跑，且 macOS 那条在配置上允许失败（本次恰好通过）。
- `publish.yml` 只在 `tags: v*` 触发、用 OIDC 信任发布并 `--provenance`（[`publish.yml`](https://github.com/xiajiajun516/dsh-config-manager/blob/babd759693bcbbd1da259a53d7d308728c0f0b8f/.github/workflows/publish.yml#L1-L14)）。这与 registry 的 attestation/trustedPublisher 元数据一致，支持「0.2.3 由该 tag 的 CI 产出」这一说法；仍未比对 tarball 内容。

## RUN

- 本轮只做只读 HTTP：`registry.npmjs.org`（dist-tags/versions/gitHead/time/attestations 元数据）、`api.github.com`（repo、tags、commit、check-runs、compare、tree）、`raw.githubusercontent.com`（pinned 源文件）。
- 未 `npm install`、未构建、未运行 `npm test`、未启动插件、未导入任何真实或构造的备份包。因此：未实测 `read failed` 的界面表现、未实测回滚后盘面、未验证 tarball 与仓库一致、未验证 DSH rc.3 上的安装/运行行为。

## 与样本卡的差异清单（供改卡时逐条取舍）

| 卡片主张 | 源码结论 | 处置建议 |
|---|---|---|
| 十二步流水线、写入排在最后 | 成立，但源码注释是 14 步；且「确认后」仍会先写快照与 journal，再写配置 | 保留结论，补一句「写前还有快照/journal 两笔可控写」 |
| 未决冲突会卡住整个导入 | 只在向导 UI 成立（按钮 disabled）；引擎对未决 Conflict 是跳过，服务端不校验 | 改成「UI 硬阻断 + 引擎跳过」，别写成系统不变量 |
| 失败自动还原 | 还原文件/设置/凭据状态；**不卸载**导入期间新增的插件；收尾写入不在快照范围 | 拆成「自动回滚」与「快照恢复（含插件卸载）」两件事 |
| 密钥只记键名、不复制值 | 成立（导出扫描器 + 外部来源翻译层双重剥离）；值只经内存；日志先 redact | 可直接引用 |
| 加密备份必须输密码 | 成立且是硬拒绝（engine 层抛错），不是 UI 提示 | 可直接引用 |
| 读不到写 read failed、不写假 0 | 导出构成卡成立；导入预览计数没有 NULL 通道 | 限定适用范围 |
| 外部来源翻译成标准包再走同一流水线 | 成立；但 `source.dshVersion` 填目标机版本 → 兼容性评分被拉满（源码自述缺陷） | 抄「翻译」时不要抄评分口径 |
| 自动快照 + 回滚可关 | 成立（`rollbackOnError` 缺省 false，确认页可开） | 可直接引用 |
| Zip Slip / symlink | 解析层默认最严；解压函数无仓内调用方；导入靠 adapter 路径围栏 | 卡片未写这条，可补「解析即拒绝」而非「解压时防御」 |
