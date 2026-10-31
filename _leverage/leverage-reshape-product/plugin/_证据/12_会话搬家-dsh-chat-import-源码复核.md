---
title: "源码复核：会话搬家 dsh-chat-import"
domain: reshape-product
kind: evidence
positioning: "对 dsh-chat-import 0.26.3 的发现面与格式探测、只读预览与真实写入的边界、重导幂等、cwd/工作区映射、撤回/删除与凭据暴露面作固定提交的一手源码复核；本文件为证据，不替代样本卡。"
read_when: "核对会话迁移的预览是否零副作用、解析失败为什么会被列出、重导/撤回的真实范围、cwd 归属与导入日志里的凭据风险。"
status: observed
updated: 2026-11-01
---
# 源码复核：会话搬家 dsh-chat-import

> 取证时点：2026-11-01。只读 npm registry、GitHub API，以及固定 commit 的源码归档（codeload tarball 解包后**静态阅读**）。**未安装、未构建、未运行 `npm test`、未启动宿主或插件、未执行任何导入**。下文 `[DOC]` = 目标仓 README/docs 主张，`[SRC-TARGET]` = 该 commit 的实现，`[SRC-DSH]` = 本机 DSH `0.2.1-rc.3` 发行包，`[TEST]` = 测试源码的存在与覆盖意图，`[CI]` = workflow 声明与**该 commit 的 check-run 元数据**，`[RUN]` = 本次运行事实。目标固定为 commit [`45745e5d459ed63ea07a9678313b74cc5e3df3a6`](https://github.com/Nwflower/dsh-chat-import/commit/45745e5d459ed63ea07a9678313b74cc5e3df3a6)（tag `v0.26.3`）；所有目标代码链接均 pin 此 commit。

## Provenance 与版本界限

- **npm 侧**：`registry.npmjs.org/dsh-chat-import` 的 `dist-tags.latest = 0.26.3`，该版本 `gitHead = 45745e5d459ed63ea07a9678313b74cc5e3df3a6`，发布时间 `2026-10-28T03:55:59.574Z`；`dist.attestations.provenance.predicateType = https://slsa.dev/provenance/v1`，`_npmUser = GitHub Actions / npm-oidc-no-reply@github.com`（trusted publishing）。
- **GitHub 侧**：`v0.26.3` 是**附注标签**（tag 对象 `b7f0a7d20b8ad8727f1fb3f43f4bc2c575629dae`，tagger `2026-10-28T03:53:13Z`），其 `object.type = commit`、`object.sha = 45745e5d…`。commit 时间 `2026-10-28T03:53:11Z`，message `chore(release): 0.26.3`，只改 3 个文件。
- **对齐结论**：npm `0.26.3` 的 `gitHead` 与 tag `v0.26.3` 指向的 commit **逐字一致**，也等于本文件审计的树；`package.json` 的 `version` 为 `0.26.3`。**未发现 registry/tag 不匹配**，无需推断。
- **签名**：该 commit `verification = {verified:false, reason:"unsigned"}`。tag→commit 绑定存在，但没有签名验证；本文不把 provenance 说成「已签名」。
- **样本卡版本核对**：卡片写 `0.26.3`，与本次 pin 一致；但卡片「13 家来源」已过时——`CHAT_FORMATS` 为 34 条（含 `dsh`/`dsh4`/`local-jsonl`，[`lib/toolkit.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/toolkit.mjs#L39-L74)），发现层 `SOURCES` 为 33 个（[`lib/discovery/registry.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/discovery/registry.mjs#L31-L37)），README 自称 25+。
- **未取**：npm tarball 未下载，`lib/client.js`（由 `src/client/` 片段逐字拼装的浏览器 bundle，`scripts/build-client.mjs --check` 在 CI 里守一致性）与 `src/client/` 的一致性未比对，`lib/*.mjs` 与 tarball 的逐字节一致性未验证 → `[OPEN]`。仓库是零构建纯 ESM：`prepack` 跑 `build-client --check` 与发布面自检 `.github/scripts/build-check.mjs`，没有 TS 编译步骤。

## DOC

- 预览的定义写死在 README：「double-click a row to preview the conversation (a read-only dry-run — **plugin injections skipped**, tool calls folded into one line)」，见 pinned [`README.md`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/README.md#L95-L95)。同一句里的「plugin injections」在 USAGE 里被解释为**本插件注入的消息**：「Messages injected by the plugin are skipped, consecutive tool calls collapse into one row…」，见 [`docs/USAGE.md`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/docs/USAGE.md#L267-L267)。
- 撤回有两条口径：`retract_import`「remove the registry record」，面板 History tab「delete plugin-created sessions (with confirmation)」，见 [`docs/USAGE.md`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/docs/USAGE.md#L10-L10)；README 功能表同口径，见 [`README.md`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/README.md#L131-L133)。
- 落点规则（cwd 缺失/主目录/本机不存在 → 专用导入工作区并**改写 cwd**；`per-project` 才宁可不分组）见 [`docs/USAGE.md`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/docs/USAGE.md#L259-L259)，与设计记录 [`docs/architecture.md` D16](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/docs/architecture.md#L218-L234) 一致。
- 重导三态（未变跳过 / 未被续聊续写 / 已续聊另铸副本）见 [`docs/USAGE.md`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/docs/USAGE.md#L106-L109) 与 [`docs/architecture.md` D13](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/docs/architecture.md#L149-L171)。
- 三级探测「explicit format > content marker > parser trial」「failures 记**每个**候选格式」见 [`docs/architecture.md` D20](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/docs/architecture.md#L287-L317)。
- 工具注入的文案是「tools … start out injected into context」，见 [`README.md`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/README.md#L119-L119)；实现默认档是 `minimal`（见 SRC-TARGET §8），文案没有写清「默认只常驻 `import_chat`」。
- 刷新行为：「只有目标代次 ≠ 宿主原生代次时」才需要刷新页面，见 [`docs/USAGE.md`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/docs/USAGE.md#L12-L12)。

## SRC-TARGET

### 1. 两个发现面，失败报告口径不同

- 发现列表（侧栏面板）按来源描述符扫默认根：每个来源声明 `roots(home,env)` 与 `scan(host,target,ctx)`，[`lib/discovery/registry.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/discovery/registry.mjs#L1-L9)；单目标失败只让该目标产出空数组，但进 `warnings: [{format,target,error}]`，[`lib/discovery/discover.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/discovery/discover.mjs#L13-L25)。**这是「按目标」的失败清单，不是「按解析器」。**
- 「Import from file」才是多解析器竞争：可识别后缀仅 `.jsonl/.jsonl.zstd/.zstd/.json/.dshbundle`，[`lib/file-import.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/file-import.mjs#L30-L34)；目录收集跳过 `node_modules/.git/.hg/.svn`，[同文件 #L37-L51](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/file-import.mjs#L37-L51)。**只递归 `type==='directory'`、只收 `type==='file'`**；DSH 的 `listDir` 条目类型是 `'file' | 'directory' | 'other'`（`@deepseek-ai/dsh-fs@0.2.1-rc.3` `lib/types/types.d.ts:93-97`，`[SRC-DSH]`），所以非普通文件/目录的条目（含后端不跟随后报告为 `other` 的链接）不会进入候选——但「不跟随 symlink」是这一实现的结果，不是它显式判断。
- 目录默认是否递归由调用方决定：面板先按当前层预览、弹窗确认后才 `recursive:true`，[`lib/panel.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/panel.mjs#L508-L537) 与 [`lib/file-import.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/file-import.mjs#L111-L119)。

### 2. 三级探测：`failures` 是「每个候选解析器为什么放弃」

- 顺序与短路：显式 `format` → 内容标记（`sniffInterchangeMarker`，bundle/generic 命中即权威）→ 候选试跑，[`lib/convert/local-jsonl.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/convert/local-jsonl.mjs#L88-L147)。
- 失败原因每条都是 `{format, reason}`：无结果 / `skipReason` / 无 meta / 0 轮；抛错另记为「解析抛错」（消息经 `sanitizeParseError` 净化、截断），[同文件 #L76-L82](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/convert/local-jsonl.mjs#L76-L82)。
- **一个容易抄错的细节**：候选顺序并不总是全量。`pathPriority` 对识别度高的路径只返回**单个**格式（如 `session.jsonl` → `dsh`、`rollout-*` → `codex`、`.claude/` → `claude`），此时 `detectedBy='path-hint'`；该格式试不出会话就直接失败，不再换格式猜，[同文件 #L53-L68](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/convert/local-jsonl.mjs#L53-L68) 与 [#L121-L141](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/convert/local-jsonl.mjs#L121-L141)。因此「逐个解析器试」只发生在路径特征不明确时。
- `failures` 只挂在**预览条目**上：`previewEntry` 与 `previewOneTarget` 才透出 `detectedFormat/detectedBy/failures`，[`lib/import-core.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-core.mjs#L669-L696)、[`lib/file-import.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/file-import.mjs#L143-L161)。正式导入走 `commitSingle`，无可导入内容时只回 `skipReason`，**不带 `failures` 数组**，[`lib/import-core.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-core.mjs#L499-L506)。所以「列出每个解析器放弃的原因」是**预览面**的保证（面板在此渲染清单 + 可复制的任务说明），不是导入结果 schema 的保证。
- 失败后的三个出口（强制格式 / generic / 报告本格式）在客户端渲染：失败清单、复制任务说明、指南链接，[`src/client/file-import.js`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/src/client/file-import.js#L462-L486)；`dsh-chat-import-convert` skill 的内容来自 `docs/INTERCHANGE-GUIDE.md`，[`lib/skill.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/skill.mjs#L1-L20)。

### 3. 预览确实零写入；「跳过插件注入」是**样张过滤器**，不是「不触发别的插件」

- 预览契约写在模块头：「绝不 create/append、绝不写 imports registry、绝不 attachToWorkspace」，并明确绕开 `loadImports/listPersistedIds/decideSingle/decideMulti/runDecision`，[`lib/import-core.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-core.mjs#L654-L709)。实际路径只有 `readText → convert → previewConverted`（预算标注 + cwd 重映射），[同文件 #L700-L709](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-core.mjs#L700-L709)。
- 两条预览路由都只读：`/api-import/preview`（发现行）与 `/api-import/file`（`preview:true`），[`lib/panel.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/panel.mjs#L625-L641)、[同文件 #L533-L537](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/panel.mjs#L533-L537)。发现行预览还显式传 `importSystemPrompt:false`，[`lib/toolkit.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/toolkit.mjs#L272-L278)。
- **「plugin injections skipped」的真实含义**：`previewSample` 把 `source.kind === 'plugin'` 的消息从样张里过滤掉，注释点名「the migration notice, the system prompt seat」，[`lib/preview-sample.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/preview-sample.mjs#L1-L24) 与 [#L52](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/preview-sample.mjs#L52-L52)。它过滤的是**本插件自己**在正式导入时会注入的那条「环境变更声明」；不是「别的插件被跳过」，也不是「预览不合成注入消息」。
- 正式导入**确实会注入**：合成器在首个 `step/start` 之后发一条 `user/message`，`source:{kind:'plugin',plugin:'chat-import'}`，正文是「环境变更声明」+（开关开启时）源系统提示词，[`lib/convert/events.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/convert/events.mjs#L239-L249)。`importSystemPrompt` 默认 **true**，[`lib/import-prefs.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-prefs.mjs#L90-L96)。同族的「注入识别」逻辑（`inject.mjs`）处理的是**源转录里**宿主/CLI 写下的注入块，与 DSH 插件注入是两件事，[`lib/convert/inject.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/convert/inject.mjs#L1-L31)。

### 4. 「可续聊」从哪来：原生 DSH 会话日志 + 真 agent，不是 shim

- 转换层把外部转录合成**完整 DSH 事件流**：`seq` 从 0 连续、surface 事件带 `surfaceOp`、工具调用与结果同 step 闭合、`sourceEventSeqs` 关联调用；还处理原生压缩事务、protected system head、V3/V4 双形状，[`lib/convert/events.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/convert/events.mjs#L1-L40) 与 [`lib/convert/validate.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/convert/validate.mjs#L1-L25)。
- 落盘走宿主原生日志面：`prepareHostMeta` 按宿主 header 白名单重建（`version/id/createdAt/isSeeded/delegationDepth/cwd/parentSession/origin/agentPreset`），`isSeeded=false`、`delegationDepth=0`，拒绝非绝对 `cwd` 时**只删 cwd、不拒绝整次导入**，[`lib/host-session.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/host-session.mjs#L145-L166)。事件按目标代次归一（V3 wrapper / V4 一级 tool 消息）后写入，[同文件 #L167-L290](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/host-session.mjs#L167-L290)。
- `createSession` 优先 `agents.create({sessionId, meta, seed, agentOptions, setup})`（挂默认 preset、绑默认模型），失败才回退 `sessionPersistence.create`；回退路径只落盘、不进宿主内存会话表，**需刷新页面才看得到**，[同文件 #L320-L398](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/host-session.mjs#L320-L398)。宿主侧确实有 `agents.create`，且 `meta/seed/agentOptions/setup` 是契约字段（`@deepseek-ai/dsh-agent@0.2.1-rc.3` `lib/types/index.d.ts:55-96`，`[SRC-DSH]`）；`agents.create` 公布 agent 后 `api-session-controller` 会发 `api-session/added`（`lib/index.js:2981-2990`，`[SRC-DSH]`），这解释了「原生代次导入后立刻出现在列表」。
- 会话 id 由源 sessionId 折成 `import-<slug>`，[`lib/convert/core.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/convert/core.mjs#L59-L65)。宿主 header **没有** `sourceId/provider/model` 的位置：这些字段只在 registry/导出协议里，落盘时被白名单裁掉（上引 `prepareHostMeta`）。会话里能看到的来源身份只有标题「来源 · 话题」，[`lib/sourced-title.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/sourced-title.mjs#L104-L137)。
- 0.8.3 起**不再写** `session/imported` 标记（宿主事件词汇表 fail-closed），归属以插件自己的 registry 为权威，[`lib/imports.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/imports.mjs#L24-L34)。这决定了下文撤回/删除的边界。

### 5. 重导与幂等：键是**源路径**，判据是「日志还是不是我写的」

- registry 落盘在 `$DSH_HOME/dsh-chat-import/imports.json`，形状 `{version, imports: {<源绝对路径>: record}}`；「幂等键 = 源文件路径（多个源文件可共享同一源 sessionId，按 sessionId 去重会静默丢历史）」，[`lib/imports.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/imports.mjs#L1-L34)。这与卡片「按最后一条 sessionId 认身份」是两件事：后者是**源内**身份判定，前者是**跨次导入**的去重键。
- 短路径：`force/replace/显式 id 变更` 之外，`version+size` 未变（目录/分页链用复合 stat）、参数指纹与预算未变 → 直接 `already-imported`，**不读源**；SQLite 源另加 `-wal` 边车签名，[`lib/import-state.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-state.mjs#L48-L89)。
- 源增长时用**实测**的 DSH 日志长度 `storedEvents` 分流：等于基线 → 只续写尾部；大于 → 用户已在 DSH 续聊 → 另铸副本（`continued-in-dsh`）；小于 → 跳过并报 `storedShrunk`；无基线 → 保守另铸副本（`baseline-missing`）；读不到长度 → 不写、报 `appendedSkipped`。分支在 [`lib/imports.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/imports.mjs#L493-L544)；`force`/显式 id 恒另铸副本，[同文件 #L477-L490](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/imports.mjs#L477-L490)；轮数变少 / 轮数相同但事件数变都只跳过上报，[同文件 #L546-L578](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/imports.mjs#L546-L578)。
- 基线是 create/replace 后实测回读、append 后按「追加前实测 + 尾部事件数」推算，[`lib/import-core.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-core.mjs#L236-L250)、[#L326-L352](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-core.mjs#L326-L352)、[`lib/imports.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/imports.mjs#L530-L539)。注意副作用：宿主若在 create 后自行追加事件（迁移/归一化），会被判成「已续聊」→ 多建一份副本，作者在 D13 里承认这个保守方向。
- id 撞车与幽灵：目标 id 被别的源占用、已归档、或「list 可见但日志读不回」的幽灵，都后缀另铸新 id（`staleGhost`），[同文件 #L579-L629](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/imports.mjs#L579-L629)；运行时 create 仍撞车时再兜底重试一次，[`lib/import-core.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-core.mjs#L326-L345)。
- 墓碑：归档 / 删除源 / 移除工作区自动登记，撤回写**永久**墓碑；命中即 `ignored` 并点名原因，`force` 可一次性越过但不解除墓碑，[`lib/imports.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/imports.mjs#L645-L696)、[`lib/ignore-watch.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/ignore-watch.mjs#L1-L10)。

### 6. 元数据与 cwd：源 cwd 只影响「落在哪个工作区」，默认会被改写

- 源 `cwd` 的来源按来源而异；Claude 缺 cwd 时先用 `~/.claude.json` 的 `projects` 键做权威映射，失败才 ASCII slug 解码（有损兜底），[`lib/import-core.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-core.mjs#L50-L61)、[`lib/cwd-map.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/cwd-map.mjs#L41-L95)。主目录 cwd 被显式跳过（沙箱 ACL 会拒绝 home 里的 temp/pwsh），[同文件 #L24-L28](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/cwd-map.mjs#L24-L28)。
- `cwdRemap` 是跨机器迁移的显式选项：长前缀优先、改写后仍要过宿主绝对性校验、余段含 `..` 时**拒绝改写并如实记录** `parent-traversal`，[`lib/import-core.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-core.mjs#L95-L156)。
- 归组必须在 create **之前**定：`planWorkspaceGroup` 默认 `auto`——cwd 命中已有工作区则沿用；cwd 是本机目录且非主目录则在 cwd 建工作区；否则落到专用导入工作区 `$DSH_HOME/dsh-chat-import-workspace` 并**改写 cwd**。`per-project` 只在最后一级不改写（宁可不分组），`dedicated` 恒落专用工作区，[`lib/workspace-group.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/workspace-group.mjs#L104-L153)。attach 只接受 cwd 与工作区路径相等，失败回 `reason` 不阻断导入，[同文件 #L155-L171](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/workspace-group.mjs#L155-L171)。
- 因此**「没有 cwd 就报跳过、不猜项目」在当前实现里不成立**：默认路径是「改写 cwd 到专用工作区并照常导入」，只有 `per-project` 会保留「未分组」；两者都不跳过会话。结果字段 `workspace/workspaceCreated/ungrouped/ungroupedReason` 把落点如实上报，[`lib/import-core.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-core.mjs#L437-L447)。
- 「拖到侧栏工作区」= `workspaceMode:'dedicated'` + `workspaceDir` + `restamp:'end'`，[`lib/panel.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/panel.mjs#L435-L440)。`restamp:'end'` 锚在本会话**最大**事件时间上，整体平移到「现在」，保留相对间隔，`createdAt` 一并平移且不得落到未来；时间戳缺失时不猜，[`lib/import-core.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-core.mjs#L173-L200)。这回答了卡片里「平移规则」的 `[OPEN]`。
- 模型绑定：`agents.create` 的 `agentOptions` 取宿主当前默认 provider/model/maxTokens，导入会话因此用**当前默认模型**续聊，而不是源模型，[`lib/host-session.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/host-session.mjs#L390-L398)；源 `model` 只出现在转换结果/registry，不写 header。

### 7. 撤回 / 删除 / 回滚：没有事务，只有「事后删」

- 上游缺面是前提：DSH `SessionPersistence` 的抽象面只有 `create/open/flush/stat/list`，**没有 delete/remove**（`@deepseek-ai/dsh-session-persistence@0.2.1-rc.3` `lib/types/index.d.ts:101-160`，`[SRC-DSH]`）；`lib/retract.mjs` 的模块头据此把工具面定为「识别 + 引导手删 + 移除 registry，绝不调用任何删除」，[`lib/retract.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/retract.mjs#L1-L16)。
- **工具面 `retract_import`**：按 sessionId（registry 反查优先，旧日志标记兜底）或 sourcePath 定位 → `removeImport` → 打 `retracted` 墓碑 → 返回 `manualDelete` 文案（含工件路径、幽灵会话说明），[同文件 #L154-L196](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/retract.mjs#L154-L196)。**它不删会话**。
- **面板面 `/api-import/purge`**：`all` / `sourcePath` / `sessionId` 三种，[`lib/panel.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/panel.mjs#L482-L500)；`deleteImportedSession` 先校验「在 imports registry 里」、拒绝 running agent，再停 fiber、detach 内存 store、detach 工作区、`rm` 工件目录（`locate` 优先，失败后扫 `$DSH_HOME/sessions/*/<id>`），最后修剪 registry 并打永久墓碑，[`lib/purge.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/purge.mjs#L212-L298)、[#L94-L142](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/purge.mjs#L94-L142)、[#L201-L233](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/purge.mjs#L201-L233)。这是 README「delete sessions this plugin created」对应的实现。
- 删除是**整条会话**：以会话 id 为单位 `rm` 整个工件目录，**不区分「导入段」与「导入后用户在 DSH 续聊的轮次」**；`storedEvents` 只在重导判定里用，删除路径不读它（`grep storedEvents` 只命中 imports/import-core）。唯一护栏是「agent 正在运行」与「不在 registry」。所以「撤回自己创建过的会话」在用户已续聊的会话上等价于「连带删掉用户后加的对话」。
- **没有事务式回滚**：`runDecision` 逐条 create/append，任一抛错只让该次调用失败，之前已建好的会话保留；registry 只在全部写完后 `rememberImport`，[`lib/import-core.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-core.mjs#L361-L428)。后果：多会话源（一个文件多条会话）若在中间某条 create 失败，前面已落盘的会话**没有 registry 记录**，而日志里又没有导入标记（上引 §4）→ 插件事后既列不出也删不掉它们。这是代码可读出的缺口，本次未实测。
- `replace`（面板「刷新已导入」）是另一条写路径：先 `clearSessionArtifactsForReplace` 删旧工件、保留 registry 与工作区挂接，[`lib/purge.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/purge.mjs#L212-L233)。它同样受「running 拒绝 / rm 后必须消失」约束。

### 8. 工具注入档位（顺带纠正卡片）

- 默认偏好是 `injectTools:'minimal'`（`importSystemPrompt:true`、`sidebarButton:true`），[`lib/import-prefs.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-prefs.mjs#L90-L98)。`minimal` = **只常驻 `import_chat`**，`full` 才是 12 个工具；启动时先 `register('full')` 兜底 settings 缺席的 CLI/headless，随后由 settings 对账，[`lib/tools.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/tools.mjs#L26-L87)。卡片「默认把工具注入上下文」应改成「默认 minimal，仅入口工具常驻」。

### 9. 路径处理与凭据内容

- 上传通道：文件名只取 basename、去控制字符、限长 120；`uploadId` 只接受 UUID；落点固定在 `<registryDir>/uploads/<uploadId>/`；配额 256MiB/文件、2GiB 暂存；未完成 24h 回收，[`lib/upload.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/upload.mjs#L1-L25)、[#L46-L70](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/upload.mjs#L46-L70)。整文件 sha256 校验通过才产出可导入路径。
- 直读路径：面板/工具给的是任意本机路径，经 `ctx.fs.resolve` + `stat`（宿主沙箱决定可读范围），[`lib/file-import.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/file-import.mjs#L96-L122)。目录收集只把 `type==='file'` 的条目当候选（见 §1 的限定）。`cwd` 只写绝对路径、`cwdRemap` 拒绝 `..`（见 §6）。
- **凭据只报告、不脱敏**：逐行 JSONL 解析对每行跑保守正则（api-key / token / password / secret / authorization），命中只记 `{line, kind}`，每行至多一条，[`lib/convert/core.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/convert/core.mjs#L134-L216)；结果只经 `secrets` 计数/位置透出，[`lib/import-core.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-core.mjs#L66-L79)。**凭据路径上没有任何替换或脱敏**——源转录里的密钥会原样进入 DSH 会话日志与模型上下文，插件只是把它标出来（预算裁剪 `budget` 会按 token 截断内容，但那是另一条与密钥无关的路径，见 §9 末条）。只有「报告文本」保证不含密钥内容（测试断言 `out.secrets` / 渲染文本不含 secret，[`test/secrets-reporting.test.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/test/secrets-reporting.test.mjs#L112-L121)），不是「导入内容已脱敏」。
- 超大体量：0.26.3 **没有** `maxTranscriptBytes` 符号；本地文件导入是整文件 `readText` 后转 IR，[`lib/import-core.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/import-core.mjs#L519-L519)；只有 codex 分页链/标题等少数路径用 `streamText`，[`lib/sources/codex.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/lib/sources/codex.mjs#L313-L320)；`budget` 做的是**上下文 token 裁剪**，不是内存分块。

## SRC-DSH

- 本机 DSH `0.2.1-rc.3`（与卡片基线一致）。`SessionPersistence` 抽象面只有 `create/open/flush/stat/list`，无删除面（`@deepseek-ai/dsh-session-persistence@0.2.1-rc.3` `lib/types/index.d.ts:101-160`）；jsonl 后端另有契约外的 `locate(meta)`（`dsh-session-persistence-jsonl@0.2.1-rc.3` `lib/index.js:2450`），插件对它是**可选**调用（`lib/retract.mjs#L59-L69`）。
- 两类写入错误的名字与文案与插件判定一致：`SessionAlreadyExistsError` / `SessionAlreadyOwnedError`（`dsh-session-persistence` `lib/index.js:33-48`）；插件按 `err.name` 优先、文案兜底（`lib/host-session.mjs#L396-L405`）。
- `attachSession` 要求 `realpath(header.cwd) === workspace.path`，否则抛错（`@deepseek-ai/dsh-workspace@0.2.1-rc.3` `lib/index.js:111-129`）；这正是 `workspace-group.mjs` 的「先定工作区再 create」与「不改写就未分组」的来源。
- `cwd` 必须绝对：`format v2 header cwd must be absolute`（`@deepseek-ai/dsh-session-format-v1-to-v2@0.2.1-rc.3` `lib/index.js:75`；v4 同规则在 `dsh-session-format-v3-to-v4` `lib/index.js:970`）。插件用 `node:path.isAbsolute` 先剔除非绝对 cwd（`lib/host-session.mjs#L152-L155`），与宿主口径一致。
- `agents.create` 接受 `meta`（whitelist 含 `cwd/agentPreset` 等）、`seed`、`agentOptions`、`setup`（`@deepseek-ai/dsh-agent@0.2.1-rc.3` `lib/types/index.d.ts:55-96`）；`agent/created` 后 `api-session-controller` 发 `api-session/added`（`dsh-api-session-controller` `lib/index.js:2981-2990`）。这支持「原生代次 + `agents.create` → 无需刷新即出现」。
- 本轮**没有**在 DSH 侧验证 `session/imported` 是否真的会被拒绝、`projectionCache.coldSnapshot` 的降级行为、`fs.streamText` 的签名；这些只按插件注释/探测逻辑记录 → `[OPEN]`。

## TEST

- 预览零副作用有端到端断言：预览后 `persistence.sessions.size === 0` 且 `imports.json` 不存在，[`test/file-import.test.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/test/file-import.test.mjs#L68-L84)；目录预览的「未识别条目带 failures 清单、强制格式失败不静默」在同文件 [#L101-L121](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/test/file-import.test.mjs#L101-L121)。这证明**测试作者认为**预览必须零写入；本次未运行。
- 重导语义逐条有测试：增长 append、未变短路径不读源、sourceShrunk、changedInPlace、force、共享 sessionId 避让、legacy 回填、`continued-in-dsh`、`storedShrunk`、`baseline-missing`，[`test/index-reimport.test.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/test/index-reimport.test.mjs#L59-L344)。
- 删除面：`deleteImportedSession` 删工件 + 清 registry、rm 后仍存在则中止且 registry 保留、拒绝非 registry 会话，[`test/purge.test.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/test/purge.test.mjs#L63-L158)。
- 工具撤回面：零删除保证（无 remove 调用、工件仍在）+ 手删引导 + 幂等 + 重导墓碑/幽灵，[`test/retract-import.test.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/test/retract-import.test.mjs#L191-L223)、[#L291-L393](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/test/retract-import.test.mjs#L291-L393)。
- cwd 映射与重映射有独立单测：slug 往返/中文路径/盘符、`resolveClaudeCwd` 三档匹配与缺失回退、贪心解码；`cwdRemap` 的畸形参数、前缀边界、`..` 拒绝、幂等，[`test/cwd-map.test.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/test/cwd-map.test.mjs#L10-L120)、[`test/cwd-remap.test.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/test/cwd-remap.test.mjs#L29-L110)。
- 凭据报告：`detectSecretKinds` 命中面、畸形行不把行内容写进错误消息、转换器只回 `{line,kind}`，[`test/secrets-reporting.test.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/test/secrets-reporting.test.mjs#L22-L134)。注意：它断言的是**报告**不含密钥，不是导入内容被清洗。
- 工具注入档位与常驻成本：`off/minimal/full` 三档、`minimal` 只注册 `import_chat`、描述长度上限，[`test/tools-injection.test.mjs`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/test/tools-injection.test.mjs#L12-L69)。
- 覆盖缺口（代码推导，非测试失败）：没有「多会话源中途 create 失败 → 已建会话无 registry」用例；没有「用户续聊后再删除」的护栏用例（因为实现不拦）；没有「导入内容中的密钥被清洗」用例（因为不清洗）。

## CI

- `ci.yml` 的 `test` job：`ubuntu-latest`，`npm ci` → `npm run check:coverage`（同一批测试 + 行覆盖阈值）→ `eslint` → `build-client.mjs --check` → `check:linux` → `check:leaks` → README 双语同步 → 文档链接 → 测试纪律 → lockfile 漂移 → `npm pack --dry-run`，[`.github/workflows/ci.yml`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/.github/workflows/ci.yml#L11-L59)。
- 另有 `smoke` job：装 npm latest 的 dsh CLI → link 装本仓 → headless boot + 插件激活审计 + 一次 mock LLM 回合，[同文件 #L72-L120](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/.github/workflows/ci.yml#L72-L120)。这是对宿主契约的回归网，不是单元测试的替代。
- `release.yml` 由 `tags: v*` 触发，校验 tag 与 `package.json` 版本一致、必须落在 `main`，重跑同一组门禁后 `npm publish --provenance`，[`.github/workflows/release.yml`](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/.github/workflows/release.yml#L11-L16)、[#L58-L92](https://github.com/Nwflower/dsh-chat-import/blob/45745e5d459ed63ea07a9678313b74cc5e3df3a6/.github/workflows/release.yml#L58-L92)。这与 registry 的 OIDC `_npmUser` / SLSA attestation 相容。
- 该 commit 的 check-run 元数据（GitHub API，2026-11-01 读取）：`test` success 2026-10-28T03:54:21Z、`release` success 03:54:50Z、`smoke` success 03:54:38Z，共 3 条全部 success。这是**该 commit 的 CI 结论**，仍不等于本地复跑。

## RUN

- 本轮只做只读 HTTP：`registry.npmjs.org`（dist-tags/gitHead/time/attestations）、`api.github.com`（repo、tags、tag 对象、commit、tree、check-runs）、`codeload.github.com`（该 commit 的源码归档，2.0 MB，解包到临时目录静态阅读）。源码归档解包在平台临时目录；仓库内只新增本文件。
- 未 `npm install`、未构建、未运行 `npm test`、未启动 DSH / 插件、未导入任何真实或构造的转录。因此：未实测预览在真实宿主中的零写入、未实测删除后的盘面、未验证 `lib/client.js` 与 `src/client/` 一致、未验证 tarball 与仓库一致。

## 与样本卡的差异清单（供改卡时逐条取舍）

| 卡片主张 | 源码结论 | 处置建议 |
|---|---|---|
| 支持 13+ 家来源 | `CHAT_FORMATS` 34 条、发现层 33 个；README 写 25+ | 改成「25+，以 `CHAT_FORMATS` 计」；「13」是旧快照 |
| 没有 `cwd` → 报「跳过」、不猜项目 | 默认 `auto` 把 cwd 改写到专用导入工作区并**照常导入**；`per-project` 才宁可不分组 | 删除「跳过」；改写成「落点三态 + 结果字段如实上报」 |
| 预览跳过「插件注入」= 不触发别的插件 | 预览确实零写入；但「跳过」是样张过滤 `source.kind==='plugin'`（本插件自己的环境变更声明） | 改成「预览不写盘、不建会话；样张隐藏本插件将注入的声明」，别写成「不触发其他插件」 |
| Retract Import 逐条删除本插件创建的会话 | 面板 `/purge` 会删工件；工具 `retract_import` **只删 registry + 手删指引**；删除按整条会话，不区分用户后续续聊 | 拆成「面板删除」与「工具撤回」两条；补「已续聊会话会被整条删掉」的边界 |
| 超大转录分块流式导入（`maxTranscriptBytes`） | 0.26.3 无此符号；本地文件整读 `readText`；`budget` 只裁上下文 token；上传上限 256MiB | 删除该句；改写成「无显式内存上限，整文件读入」 |
| 工具默认注入上下文 | 默认档 `minimal`，仅 `import_chat` 常驻；`full` 才 12 个 | 改成「默认 minimal，设置可切 off/minimal/full」 |
| 身份取最后一条 `sessionId` | 成立（Claude fork），但**跨次导入的幂等键是源路径** | 区分「源内身份」与「去重键」 |
| 解析失败列出每个解析器放弃的原因 | 成立，但只保证在**预览面**；导入结果只带 `skipReason` | 写明「预览列出，导入结果不带 failures」 |
| 保真 vs 去重：fork 保留父段 | 成立：主转录判据看文件两端、只导主转录、父段保留 | 可直接引用 |
| 预览是一次真解析的只读 dry-run | 成立（同源 `convert`，不写 registry/不建会话），且有测试断言 | 可直接引用 |
| 可续聊来自重建 DSH 会话 | 成立：合成完整原生事件流 → `agents.create`/`sessionPersistence.create`，挂 preset、绑默认模型 | 可直接引用；补「模型是当前默认模型、来源身份只在标题」 |
| 反向导出 / 忽略 | 本轮未复核（focus 之外） | 保持原卡，标注未复核 |
