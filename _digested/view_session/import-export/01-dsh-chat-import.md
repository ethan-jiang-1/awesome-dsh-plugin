# dsh-chat-import — 42 个纯函数转换器,加一层把 IR 合成为 DSH 原生会话日志的 host ABI 适配

> 证据等级:★★★(源码级;`Nwflower/dsh-chat-import@ba599183390164484d5f5894585ddb8f6abb2228`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 71 为 2026-08-19 历史采样;2026-11-18 实时 318(约 4.5 倍)。
> ⚠ 下载 4273 同为 2026-08-19 采样。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `Nwflower/dsh-chat-import`([registry](../../../data/plugins/Nwflower__dsh-chat-import.yml)) |
| 类目 | session([census](../../ecosystem/census.py) 914 条 / 全表 11 744 条) |
| 子分类 | `import-export`(数据跨越 DSH 边界:入边导入、出边导出) |
| 自述 | registry 写「13 家」;`package.json:3` 与 README 写「25+」;代码里是 **37 个可发现来源 + 1 个只能显式指定的 `local-jsonl` = 38 个 `import_chat` 格式**(`lib/discovery/registry.mjs:36-44`、`lib/tools/import-sources.mjs:520`)。自述数字落后代码两代 |
| 星标 ⚠ | **71**(2026-08-19 冻结采样);**2026-11-18 实时 318**(4.5 倍)。仓库级星标,单仓库非 monorepo,无归属争议 |
| 下载 ⚠ | **4273**(2026-08-19);session 类第一,同口径次高 3568 |
| 扩散 | **0**(`grep -ril 'chat-import' data/plugins/` 命中 **1** 条,即自身;命令见末节) |
| 仓库 commit | `ba599183390164484d5f5894585ddb8f6abb2228`(2026-11-15,`main`,`fix(cherrystudio): local-jsonl 路径提示与跨平台发现根`);仓库创建 2026-08-13 |
| 包形态 | npm `dsh-chat-import@0.26.7`;Cordis **bundle**(`package.json:46-55` 的 `dsh.bundle.patch` + `dsh.client.inject/platform`),`cordis.patch.yml` 全文 3 行、一条 `insert`;服务端插件 + 一个 398 KB 的浏览器 bundle(`lib/client.js` 4 872 行,由 `src/client/` 构建) |
| 代码规模 | `lib/**/*.mjs` **36 286 行**(不含生成的 `lib/client.js` 与 `lib/index.d.ts` 738 行);其中 `lib/convert/` 12 795 行/53 文件、`lib/sources/` 4 858 行、`lib/discovery/` 3 634 行、`lib/export/` 1 244 行、`lib/tools/` 2 312 行;测试 161 个 `test/*.test.mjs`(加 `_support/` 共 **40 270 行**)+ 43 个 fixture |

## 它到底是什么

**判断:它不是 MCP 适配器,也不是外部引擎的指针,而是「格式兼容层 + 宿主会话合成器」。** 三件事各自独立:

1. **发现层**:37 个来源描述符(`lib/discovery/registry.mjs:36-44`),每个声明数据根、扫描器、单文件路径特征;`defaultRoots()` 把 `{format: root}` 摊平成一张表(`lib/discovery/registry.mjs:50-54`)。读取一律经宿主 `fs`/SQLite 只读原语,不 import 任何 DSH 包(`lib/discovery.mjs:1-6`)。
2. **转换层**:42 个导出的 `convertXxx()` 纯函数(`grep -rho "export function convert[A-Za-z0-9]*" lib/convert/*.mjs | sort -u | wc -l` → 42),每个文件头写清该客户端的存储契约;统一产出 turns IR。`lib/index.mjs:7-8` 明说 `lib/convert/*` 与 `lib/export/*` 保持「零 DSH 依赖纯函数」。
3. **合成/落盘层**:`finishSession` 做预算裁剪 → tool-call 块序收尾 → 合成事件日志(`lib/convert/core.mjs:53-62`);`lib/host-session.mjs` 再把 IR 产物按宿主代次写成合法的 `SessionEvent[]`,经 `sessionPersistence`/`agents.create` 落盘。

**IR 的形状就是它的保真边界**(`lib/convert/events.mjs:8-13`):

```
turns: [{ prompt, promptBlocks?, promptSource?, time?, compaction?,
          steps: [{ content, toolCalls, toolResults, usage?, time?, model? }] }]
```

`content` 是 DSH 内容块数组(text / reasoning / tool-call / image);`compaction` 是「该轮之前有一次源工具上下文压缩」的标记;`usage` 是 provider 回报的 token 桶;`time` 是源时间戳(毫秒)。**凡是 IR 装不下的字段,就是这张卡里「必然丢失」的那一栏。**

**合成时必须同时满足的宿主硬不变量**(决定「导入后能不能续聊」):

- `seq` 从 0 连续、surface 事件带 `surfaceOp`(`lib/convert/events.mjs:5-8`);
- 首个 surface 事件必须是 system head,环境变更声明紧随其后(`lib/convert/validate.mjs:8-16`、`lib/convert/events.mjs:8`);
- 每个 tool-call 必须在被广告的同一 step 内闭合,且恰好一条结果(`lib/convert/events.mjs:6-8`);
- 同一条 assistant 消息里 `tool-call` 必须是最后一批块,否则宿主把 `tool_use` 与 `tool_result` 拆到不相邻的两条 provider 消息,续聊第一条消息就被接口以 `400 INVALID_REQUEST` 拒收(`lib/convert/ir.mjs:112-118`,0.26.7 修复记录 `CHANGELOG.md:22`);
- V3/V4 形状由宿主互斥校验,落盘前按目标代次分流(`lib/host-session.mjs:180-214`,见同文件 :234-245 的 V3/V4 生产者 kind 说明)。

**格式版本差异:每家都是「一套存储契约 + 若干代」,不是一份 JSON schema。** 源码里能点名的:

| 来源 | 版本差异 | 证据 |
|---|---|---|
| Claude Code | fork 转录开头是父会话的逐字拷贝,身份取**最后**一个 sessionId;`isMeta:true` 的 user 记录永不开新轮、内容前置进下一个 assistant step | `lib/convert/claude.mjs:5-25` |
| Codex | 0.167+ 压缩 rollout `rollout-*.jsonl.zst`(发现层只解到够用的文件头);子代理线程 `thread_source=subagent` 整份跳过;Desktop 外部 agent 会话要把展平的信封还原成 tool call | `lib/discovery/registry.mjs:62-68`、`lib/discovery/jsonl.mjs:24-25`、`lib/zstd.mjs:50-55`、`lib/convert/codex.mjs:15-22` |
| Reasonix | v1 `tool_calls:[{type:'function',function:{name,arguments}}]` vs v2 扁平 `{id,name,arguments}`;v2 才有 `createdAt` 与行级 `usage` | `lib/convert/reasonix.mjs:12-26` |
| Pi / oh-my-pi | v1 线性无 id,靠顺序成链;v2/v3 用 `id/parentId` 组成树,压缩边界 `firstKeptEntryId` 或 `retainedTail` | `lib/convert/pi.mjs:4-8` |
| Kimi | 旧 Kimi CLI `~/.kimi/sessions/<md5>/<id>/{wire.jsonl,context.jsonl,state.json}` vs 新 Kimi Code `~/.kimi-code/sessions/<ws>/<id>/agents/main/wire.jsonl`;旧 wire 首行是 `protocol_version` 元数据、事件 PascalCase,新 wire 每行 `{type,time,…}` | `lib/convert/kimi.mjs:3-13` |
| OpenCode | V1 三表 `session/message/part` vs V2 `session_v2/session_message`;V2 的压缩正文是 `summary + recent`,V1 只有 `summary` | `lib/convert/opencode.mjs:18-30` |
| Zed | `version === '0.3.0'` 走 `DbThread`;缺版本或旧值走 `legacy_thread` 升级分支 | `lib/convert/zed.mjs:22-42` |
| DSH 自身 | 只透传 `DURABLE` 白名单(含三类压缩事件),其余丢弃;V3 wrapper / V4 一级 tool 消息两种形状都认,落盘时再归一 | `lib/convert/dsh.mjs:15-40` |

**保真与丢失(逐字段,只写代码能证明的)**:

| 字段 | 处理 | 证据 / 丢失条件 |
|---|---|---|
| 正文、标题、cwd | 保留;标题钉成 `session/title`,cwd 走 header | `lib/import-core.mjs:167-175`、`lib/host-session.mjs:149-164` |
| reasoning | **保留**:thinking→`reasoning`、Reasonix `reasoning_content`、Kimi `ThinkPart`、Gemini `thoughts`;Codex 的加密推理无明文可导(降级规则 `reasoning-encrypted`) | `lib/convert/core.mjs:73-80`、`lib/convert/reasonix.mjs:18`、`lib/convert/interchange.mjs:32-37` |
| tool call / result | 保配对;源无结果(Cursor)补空结果占位;孤儿结果丢弃并计数 | `lib/convert/interchange.mjs:19-26`、`lib/convert/events.mjs:6-8` |
| 图片/附件 | V4 落成宿主附件引用(base64 **绝不**进日志);V3 或拿不到字节 → `[image]` 占位并计 `imagesDegraded`;单会话上限 500 张 | `lib/attachments.mjs:1-20`、`:22-28` |
| token 统计 | **只有少数转换器映射** `step.usage`(`grep -rl 'step\.usage' lib/convert/*.mjs` 命中 8 个文件,其中 1 个是合成器 `events.mjs`,余 7 个:claude / opencode / reasonix / buddy-family / codearts / copilot-vscode / generic);其余来源没有,宿主的 token-meter/统计折不出 | `lib/convert/events.mjs:37-40` |
| 逐条时间戳 | 源有则逐步透传,缺则用单调时钟补齐(不倒退) | `lib/convert/events.mjs:34-36` |
| 首 token 延迟 / 输出速度 | **必然丢失**:`stream` 恒 `[]`,注释明说「不虚构不存在的流」 | `lib/convert/events.mjs:294-298` |
| 上下文压缩 | 有摘要则发射原生 `compaction/start→summary→检查点→end` 事务,模型看到「摘要 + 边界之后」;只有边界无摘要则退化为可见文本或旧窗口切片 | `lib/convert/events.mjs:18-30` |
| 系统提示词 | 不是 system 角色:默认(开关 `importSystemPrompt` 开)以 `<system-reminder>` 包裹的环境变更声明 + 原文,作为**一条 plugin user 消息**注入 | `lib/convert/events.mjs:48-60`、`:67-83`、`lib/import-prefs.mjs:96` |
| 分支 | ChatGPT 默认只导 active branch,`branch:'all'` 才把每条 root→leaf 路径各建一条会话;DSH 单线程无分支概念 | `lib/convert/chatgpt.mjs:9-16`、`lib/convert/interchange.mjs:43-48` |
| 子代理转录 | **整份跳过**(Claude `subagents/`、Codex `thread_source=subagent`、Cherry Studio 同) | `lib/discovery/claude.mjs:414`、`lib/convert/codex.mjs:15-22` |
| 源会话身份 / fork 关系 | **必然丢失**:converters 的 `sourceId` 不进 header(白名单只有 9 个键);`parentSession` 字段允许但**没有任何转换器写它** | `lib/host-session.mjs:149-161`、`grep -rn 'parentSession:' lib/convert/` 无命中 |
| 单条超长内容 | 默认就裁:单文本 ≤16 000 字符、单工具结果 ≤40 000 字符(头 75% + 尾),并计入结果 `trimmed` | `lib/convert/trim.mjs:30-31`、`:150-170`、`lib/imports.mjs:428` |
| 疑似密钥 | **只报告不脱敏**:`{line, kind}`,原文照进会话日志与模型上下文 | `lib/convert/core.mjs:138-148`、`:184-220` |

## 怎么接进 DSH

- **manifest**:`package.json:46-55` 的 `dsh.bundle.patch` 指向 `cordis.patch.yml`;`dsh.client` 声明浏览器侧注入 `@deepseek-ai/dsh-client-locale`、`platform: web`。`cordis.patch.yml` 全文三行:`insert` 一条,`id: import-claude`,`name: dsh-chat-import`。注意 `lib/index.mjs:47` 的 `name` 仍是历史名 `import-claude`,profile 里看到的插件行就是它。
- **硬依赖只有三个服务**:`inject = ['sessionPersistence','fs','tools']`(`lib/index.mjs:51`),注释解释了为什么不把 `webServer/skills/commands/settings` 放进去——放进去会让 headless/CLI profile 整体无法激活。
- **可选服务全部延迟挂载**(`lib/index.mjs:71-108`):`webServer` 经 `ctx.inject` 注册 16 条 `POST /api-import/*` 路由(`lib/panel.mjs:281-299` 的注册壳、`:305-605` 的各路由;路由数用 `grep -c "jsonRoute('/api-import"` 数出;`lib/index.mjs:73-78` 的注释还写着 11 条,已过时),且必须经 `webCtx.effect` 登记 disposer,否则插件重载后旧路由绑在已 dispose 的 ctx 上;`skills` 注册两个运行时 skill;`commands` 注册 `/import`、`/import-all`、`/ignores`、`/resume-claude`、`/resume-codex` 等;`settings` 驱动注入档位。
- **12 个工具**:`import_chat`、`import_agents`、`import_mcp`、`import_settings`、`doctor`、`export_chat`、`export_bundle`、`restore_bundle`、`list_imported_sessions`、`retract_import`、`verify_session`、`scan_discover`(`lib/tools.mjs:43-47`,各文件 `name:` 枚举)。注入档位 `off|minimal|full`,**默认 `minimal`(只注入 `import_chat`)**(`lib/import-prefs.mjs:82,91,96`、`lib/tools.mjs:58`);`lib/tools.mjs:84` 在 settings 缺席时兜底 `register('full')`。README:126 写「tools start out injected」,与默认档位不一致,读者会以为 12 个工具都在上下文里。
- **第三方服务面**:`ctx.provide('chatImport', …)`(`lib/chat-import-service.mjs:122,162`),方法 `scanDiscover / importPath / importAll / resumeSummary`;不复刻解析逻辑,直接转 `IMPORT_SPECS` 与 `runChatImportAll`(`:137-160`)。
- **绑定的宿主事件**:`agent/session-start` 两处(新会话迁移提示 `lib/prompt-hint.mjs:53`;默认关闭的 Claude memory/CLAUDE.md 上下文桥 `lib/context-bridge.mjs:144`)、`domain/changed`(归档/删工作区 → 自动忽略墓碑 `lib/ignore-watch.mjs:145`)、`loader/volatile-update` 与 `settings/document-updated`(设置热更新 `lib/import-prefs.mjs:257-261`)。
- **依赖与门槛**:peer `@deepseek-ai/dsh >=0.1.5-rc.1`、`dsh-tools >=0.1.0-rc.6 <0.3.0`(`package.json:57-64`);`engines.node >= 22.13`(`:104-105`);运行时依赖只有 `fzstd`(`:126-128`,解 Codex `.jsonl.zst` 与 DSH `.zstd`);SQLite 走 Node 内置 `node:sqlite` 且只读(`lib/sources/sqlite.mjs:1-20`)。插件**自身零网络**:`lib/` 里唯一的 `fetch` 在浏览器侧 `src/client/utils.js:254`,打的是本机面板路由。
- **安装**:`dsh plugin --profile web add dsh-chat-import`(README:89);CI 里用 `link:${GITHUB_WORKSPACE}` 走同一条 bundle 路径(`.github/workflows/ci.yml:104-107`)。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `lib/convert/*.mjs` | 12 795 | 42 个纯函数转换器 + IR/合成/裁剪/校验共用件 | `lib/convert/core.mjs:20` 格式版本常量、`:53-62` `finishSession` |
| `lib/convert/events.mjs` | 418 | IR → 平衡的 DSH 事件日志(压缩事务、usage、注入、块序) | `:85-104` 合成器、`:120-160` 压缩检查点 |
| `lib/convert/ir.mjs` | 167 | 回合骨架、压缩边界、块序不变量 | `:24-60` `createTurns`、`:112-167` `toolCallsLast` |
| `lib/host-session.mjs` | 553 | 宿主契约面:代次探测、header 白名单、V3/V4 形状、create/append、两套持久化 ABI | `:149-170`、`:180-214`、`:329-390`、`:490-518` |
| `lib/import-core.mjs` | 774 | 导入状态机(单会话/多会话/批量/预览)、落盘决策、cwd 重映射、restamp | `:258-458` `runDecision`、`:527-547`、`:559-584` |
| `lib/import-state.mjs` | — | 「源未变」短路径与重导语义(不读源) | `:52-60`、`:69-88` |
| `lib/workspace-group.mjs` | — | 归组:创建前把 cwd 写进 header,create 后再 attach | `:1-27` 两条硬约束、`:17-23` 三种模式 |
| `lib/export/claude.mjs` | 304 | DSH 日志 → Claude Code JSONL(出边) | `:1-17` 布局、`:113-114`、`:134`、`:158`、`:171`、`:206-243` |
| `lib/export-tool.mjs` | 176 | 4 种出边的只读执行体 + 降级清单 | `:1-6`、`:39-56`、`:60-90` |
| `lib/tools/import-sources.mjs` | 522 | 38 条来源 spec(转换器/编排/派生/指纹键) | `:95-112` claude、`:520` local-jsonl |
| `lib/discovery/registry.mjs` | 88 | 37 个发现源描述符 + 单文件路径 → 候选格式 | `:36-44`、`:62-83` |
| `lib/budget.mjs` | — | 预算解析链(参数 > env > 模型窗口 > 静态 550k) | `:5-12`、`:72` |
| `lib/panel.mjs` | — | 面板路由(全部 POST) | `:281-299` |

**导入数据流**(一条会话):

1. 入口分发:`import_chat({format,path,…})` → `buildImportSources` 取 spec → `file`/`dir`/专属 `io`(`lib/tools/import-sources.mjs:86-92`、`lib/toolkit.mjs`)。
2. 状态机:`importTranscript` 先 `stat` → `loadKnownRecord` → `singleShortPath` 判「源未变」直接返回(不读文件)(`lib/import-core.mjs:527-536`、`lib/import-state.mjs:52-60`)。
3. 读取:超过 V8 单字符串上限(~512 MiB)直接抛 `TRANSCRIPT_TOO_LARGE`;否则整读成字符串(`lib/import-core.mjs:514-521`)。
4. 转换:`convertXxx(raw,args)` → turns IR;`finishSession` 依次 `applyBudgetTrim`(L1 裁块 + L2 截断)、`toolCallsLast`、`synthesizeSession`(`lib/convert/core.mjs:53-62`、`lib/convert/trim.mjs:286-295`)。
5. 收尾:cwdHint 权威映射 → 预算标注 → 来源标题 → restamp → cwdRemap(`lib/import-core.mjs:51-64`、`:167-213`)。
6. 决策:`decideSingle` 比对 registry 基线,得出 `create / replace / append / skip`(`lib/imports.mjs`)。
7. 落盘:`prepareHostMeta`(白名单裁字段 + 无损 JSON 清洗)→ `prepareHostEvents`(V3/V4 形状 + 降级告警)→ `createSession` → 结构校验 → 归组 attach → `warmProjection` → 写 registry(`lib/host-session.mjs:329-390`、`lib/import-core.mjs:258-458`)。

**session id / cwd / parent 怎么定**:

- id = `import-` + 源 sessionId 的字符清洗(去掉非 `[A-Za-z0-9_-]`、截 64 位),无源 id 时用时间戳(`lib/convert/core.mjs:64-69`)。撞「宿主已有同名会话」时另铸后缀副本 `import-<id>-1` 并重试一次(`lib/import-core.mjs:333-350`、`lib/host-session.mjs:409-416` 的错误判定)。
- header 只允许 9 个键:`version/id/createdAt/isSeeded/delegationDepth/cwd/parentSession/origin/agentPreset`;`isSeeded` 恒 false、`delegationDepth` 恒 0(`lib/host-session.mjs:149-157`)。
- cwd 必须是**绝对路径**且宿主校验时目录存在;相对/跨平台路径直接剔除,会话退化为未分组,**不因 cwd 拒绝整次导入**(`lib/host-session.mjs:160-163`)。`cwdRemap` 可把源机前缀改写到本机,但显式拒绝含 `..` 的余段,防转录指定任意工作区(`lib/import-core.mjs:111-165`)。
- 归组必须在**创建前**定:宿主只接受「cwd 与工作区路径逐字相等」的 attach,先把目标路径写进 `header.cwd`,create 后再 attach;`auto` 模式下 cwd 是主目录/本机不存在时改写进专用工作区 `$DSH_HOME/dsh-chat-import-workspace`(`lib/workspace-group.mjs:1-27`、`:17-23`)。
- **parent/fork 不写**:`parentSession` 在白名单里,但所有转换器都不产出它;源 fork 关系只剩「拷贝段的历史在日志里」这一事实(`lib/convert/claude.mjs:5-14`)。

**「导入后能否真的继续对话」的证据链**:

1. 落盘走 `agents.create({sessionId, meta, seed})`——把整份事件日志当 `seed` 种进一个**新宿主会话**,而不是自制只读历史(`lib/host-session.mjs:329-372`)。
2. 同时挂默认 preset scope(`setup: agentPresets.mount`)并绑定默认模型 `{provider, model, maxTokens}`,让导入会话与原生会话工具一致、自动压缩可触发(`lib/host-session.mjs:347-366`);`meta.agentPreset` 也补写,UI 才显示预设 chip(`:358`)。
3. `agents` 缺席时回退 `sessionPersistence.create+append`;注释明说这条路径只落盘、不进内存会话表,**要刷新页面才看得到**(`lib/host-session.mjs:340-343`、`:490-518`)。
4. 测试钉住这个契约:`test/index-tools.test.mjs:91-138` 断言 `agents.create` 收到非空 `seed`、`agentOptions` 为默认模型、`setup` 执行了 preset mount;`test/index-reimport.test.mjs:242-275` 先导入、再由测试**向同一会话 append 两条 DSH 消息**,然后验证重导检测到「用户已续聊」并另铸副本——即导入出来的就是一条活的、可被宿主追加的会话。
5. 最强证据是它自己修过的 bug:0.26.7 之前,opencode 的 `patch` part 让 assistant 消息「工具调用在前、正文在后」,宿主摊平后 `tool_use`/`tool_result` 不相邻,**用户在这种会话里发的第一条新消息被 400 拒收**——浏览历史一切正常,只有续聊暴露(`CHANGELOG.md:22`、`lib/convert/ir.mjs:112-118`)。这说明作者把「真的发一条新消息」当作验收面,也说明续聊正确性依赖事件块序,不是「写进日志就行」。
6. CI 有一条**真实宿主**冒烟:装 npm latest 的 dsh、link 本插件、起本地 mock LLM、跑 `dsh --profile headless "hi"`,断言插件行进 composition 且一次 LLM 回合成功(`.github/workflows/ci.yml:92-128`)。**但它不导入任何会话**,所以「真实宿主里导入 + 续聊」仍未被自动化覆盖(见待验证)。

**反向导出回 Claude Code(以及往返损失)**:

- 出边有 4 个目标:`claude / codex / kimi / opencode`(`lib/tools/export-tools.mjs:28-29`),另有事件级无损的 `export_bundle`(SHA-256 双层指纹)与 `restore_bundle`(`lib/export-tool.mjs:92-96`)。
- Claude 布局:首行 `mode`、次行 `permission-mode`,首个 user `parentUuid:null`,标题写成 `custom-title`(`/rename` 载体,而非会被改写的 `ai-title`),之后按 DSH `seq` 串成 `parentUuid` 链;`tool_result` 的 `parentUuid` 指向**声明该调用的** assistant(支持并行扇出与跨 step 延迟结果);有 call 无 result 时在文件末尾补空 `tool_result`(`lib/export/claude.mjs:1-17`、`:113-114`、`:158`、`:206-243`、`:253-270`)。
- 写入 `<outputDir>/<slug>/<uuid>.jsonl`,默认 `~/.claude/projects`;每次铸新 uuid v4 + `createIfAbsent`,绝不覆盖;只读会话日志,不写 registry(`lib/export-tool.mjs:1-6`、`:39-56`)。
- **往返不是恒等**:① 导出铸新 uuid,再导入会得到 `import-<新 uuid>`,源身份丢失;② 导出不写 `message.usage`,Claude 侧也不回填 → token 统计在往返中消失(导入侧本来读 `message.usage`,见 `lib/convert/claude.mjs:435-443`);③ 压缩事务不导出(`compaction/*` 落到 default 分支被跳过,检查点那条 user 消息 `source.kind≠user` 被计 `skippedInjections`,`lib/export/claude.mjs:134`),而原始被遮蔽轮次仍在日志里顺序导出 → 再导入时模型看到的是「压缩前的全量历史、没有摘要」;④ 注入(环境变更声明 + 源系统提示词)按设计跳过,往返不重复但也不再存在;⑤ 非文本块与拿不到字节的图片计入 `skippedBlocks`/`unavailableImages`(`lib/convert/interchange.mjs:92-104`)。
- 往返测试只覆盖 3 条边:Codex(`test/matrix.test.mjs:24-39`)、Kimi(`:40-57`)、OpenCode(`test/opencode-export.test.mjs:169-199`)。**Claude 导出只有结构单测**(`test/export.test.mjs` 18 个用例,全部只断言序列化结果,没有 `import(export())` 往返),所以「导出后 Claude Code 能 `--resume`」目前是代码意图 + README 自述,不是测试事实。

**测试面怎么守**:161 个 `test/*.test.mjs`、43 个 fixture(只覆盖 claude/codex/cursor/gemini/pi/omp/opencode/chatgpt/qoder/reasonix 等约 10 家,其余用内联字面量与临时 SQLite 夹具)。CI 另有三层护栏:覆盖率逐文件/逐目录下限(`.github/workflows/ci.yml:24-28`)、**每个来源格式至少被一个测试锚点引用**(`.github/scripts/check-test-discipline.mjs:33-46`,按转换器导出名或 `lib/sources/<fmt>.mjs` 导出名在测试语料里搜)、单测文件 ≤1200 行(`:12-15`)。

## 为什么它突出

**星标归属没有争议**:单仓库、非 monorepo 子目录,318 颗星全归这个插件。时间线是干净的:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-13 | 仓库创建 | GitHub API `created_at` |
| **2026-08-19** | **⚠ 71 星采样点**(建仓第 6 天) | `data/stars.json` |
| 2026-11-14 | 0.26.7 发布(修复续聊 400) | `CHANGELOG.md:17` |
| 2026-11-15 | HEAD `ba59918`,工作树停止 | `git log -1` |
| **2026-11-18** | **实时 318 星 / 49 fork / 7 open issues** | GitHub API |
| 2026-11-18 | npm `0.26.7`,⚠ 下载 4273(08-19) | `package.json:5`、`data/downloads.json` |

也就是说:采样点只有 71 星时它已经是 session 类**下载第一**;三个月后星标 4.5 倍、仍是下载第一。**这是本册「声量高、扩散零」最纯的样本**:`grep -ril 'chat-import' data/plugins/` 只有它自己,连作者另外两个插件也不提它。

**为什么「高下载、零衍生」——四条解释,按解释力排序:**

1. **可复制的不是代码,是逐家存储契约。** 42 个转换器各写一套「这个客户端把会话存在哪、字段怎么变代」,没有可被第三方直接 import 的 seam;抄一行 `insert` 只能得到一个指向同一个 npm 包的配置,不构成新条目。要抄就得把 38 家格式重写一遍。
2. **它不使用、也不定义任何可收敛的协议。** 入边是各家私有文件/SQLite,出边是四家各自的原生 JSONL;唯一的跨插件面是 `$DSH_HOME/dsh-chat-import/` 下未标准化的 registry JSON 与 `chatImport` 服务(可选、单向)(`lib/imports.mjs:47-50`、`lib/chat-import-service.mjs:122`)。对比「共用一份配置/存储」那类收敛,这里没有可共用的东西——第三方要用,只能装它本身。
3. **迁移是一次性动作。** 用户换 agent 时导一次,此后没有持续读写;衍生插件缺少可挂载的高频场景。下载量高(4273)但绝对盘面小(全表 top 是 82 491),正符合「一次性工具」的形状。
4. **DSH 原生能力没有替代它。** 本机 DSH 包里 `grep -ril 'session.*import' $DSH/lib` 无命中——宿主只提供 `sessionPersistence`/`agents.create` 这类通用原语,没有官方导入器。「被原生替代」这个解释在 2026-11-18 不成立;零衍生的原因是**没有可复用的形状**,不是需求消失。

**判断:是明星,也是这一细分目前唯一的事实标准**——但标准的载体是「38 家格式的支持清单 + 事件合成约束」,不是任何对外协议。它值得读的地方不在星标,而在它把「外部转录 → 宿主可续聊会话」的每一道宿主不变量都写成了代码与测试。

## 代价与边界

**权限与读取面(装一个插件,读 37 个 agent 的家目录)**:

- 默认根来自各源描述符:`~/.claude/projects`(+Windows `LOCALAPPDATA/Claude-3p/...`)、`~/.codex/{sessions,archived_sessions}`、`~/.cursor/projects`、`~/.gemini/history`、`~/.kimi`/`~/.kimi-code`、`~/.pi`、`~/.omp`、`~/.qoder(-cn)`、`~/.reasonix`、`~/.zcode/cli/db/db.sqlite`、`~/.local/share/{opencode,mimocode,kilo}`、VSCode/Cursor 系 `User/globalStorage`、豆包 IndexedDB 等(`lib/discovery/registry.mjs:50-54` 汇总;各源 `roots()` 见 `discovery/*.mjs`)。
- 认环境变量改写根:`CODEX_HOME`、`APPDATA`、`LOCALAPPDATA`、`CONTINUE_GLOBAL_DIR`、`GROK_HOME`/`CODEARTS_HOME` 等(`lib/discovery/jsonl.mjs:444-456`、`lib/discovery/claude.mjs:450-457`)。
- SQLite 一律 `{readOnly:true}` + `PRAGMA table_info` 自适应 + 必关句柄(`lib/sources/sqlite.mjs:1-58`)——只读是硬约束,不会改客户端库。
- 也接受**任意路径**:工具参数 `path` 由模型/用户给,`import_chat` 可读任意可访问文件/目录(`lib/file-import.mjs:1-16`);边界只有宿主 `fs` 的解析与用户自己的判断。显式防穿越只有两处:`cwdRemap` 拒绝含 `..` 的余段(`lib/import-core.mjs:143-151`),purge 用 `SESSION_ID_RE` 限定会话 id(`lib/purge.mjs:17`)。
- 写盘:`$DSH_HOME/dsh-chat-import`(registry/ignores/scan-cache,原子写 `lib/atomic-write.mjs:11-26`)、`$DSH_HOME/sessions` 经宿主服务、附件对象、导出文件(默认 `~/.claude/projects` 或 `~/.dsh/exports`)。

**隐私**:源转录里的密钥只被**报告**(`{line,kind}`),不脱敏、不阻断(`lib/convert/core.mjs:138-148`);原文进入 DSH 会话日志与模型上下文,也会被导出到别的 agent 目录。导入会话还会注入一条英文环境变更声明(默认附源系统提示词),让模型知道工具/权限以 DSH 为准(`lib/convert/events.mjs:67-83`)。这是「保真优先」的自觉取舍,但读者要按「导入 = 把旧 agent 的全部对话再落一份盘、并送进模型」来评估。

**失败模式(按发生顺序)**:

1. **格式不认识**:三级探测(显式 format > 内容标记 > 候选试跑);路径特征明确时只试一个解析器(报 `path-hint`),失败不再换格式猜;全失败时给**每个**候选的放弃原因 + 强制格式/generic/报格式三个出口(`lib/convert/local-jsonl.mjs:1-15`、`:58-80`)。
2. **坏 JSON / 畸形行**:逐行跳过并计数,`skippedLines` 最多留 200 条明细,不中断整份(`lib/convert/core.mjs:184-220`、`SKIPPED_LINES_CAP`)。
3. **超大文件**:超过 V8 单字符串上限(~512 MiB)直接失败并给出拆分建议;没超也要过 L1/L2 裁剪(默认预算 550k token),超长会话「全量落盘后恢复对话直接 400」正是预算层存在的原因(`lib/import-core.mjs:514-521`、`lib/budget.mjs:1-12`、`lib/convert/trim.mjs:1-10`)。
4. **重复导入**:同源按 `sourcePath` + 参数指纹 + stat(version/size,SQLite 还看 WAL 签名)判「源未变」,不读源直接 `already-imported`(`lib/import-state.mjs:52-88`);源增长则 append 尾部;用户已在 DSH 续聊过则**另铸副本**并报 `continued-in-dsh`,绝不把导入轮次追加进用户自己的对话(`test/index-reimport.test.mjs:242-275`)。
5. **部分失败**:批量逐项 `try/catch`,失败计 `failed` 不中断整批,registry 在批末一次原子提交(`lib/import-core.mjs:559-584`、`lib/imports.mjs:214-245`)。**没有事务回滚**:会话先落盘、registry 后写,中途崩在两者之间会留下「日志在、registry 无记录」的孤儿会话;已成功创建的前 N 条也不会被撤销。
6. **宿主会话 id 被占**:识别 `SessionAlreadyExistsError`/`SessionAlreadyOwnedError` 及其文案,另铸 `-1` 后缀重试(`lib/host-session.mjs:409-416`)。
7. **宿主格式代次未知(V5+)**:大声告警,但按已知最高版本(V3/V4)产出,导入很可能被新宿主拒载——这是「一版一支」的显式代价(`lib/host-session.mjs:190-201`、`:230-232`)。
8. **导出目标不可写 / 会话不存在 / 读不到日志**:在写入前抛错,不产出半截文件(`lib/export-tool.mjs:20-36`);`createIfAbsent` 保证绝不覆盖既有导出。

**撤回与删除**:平台 `sessionPersistence` **没有 delete 面**,所以 `retract_import` 只删 registry 记录 + 引导手删(`lib/retract.mjs:1-12`);面板 purge 才 out-of-band 停 agent、detach、`rm` 工件目录(`lib/purge.mjs:1-8`)。删会话是整条删,不区分你之后续聊的轮次。

**维护成本**:三个月 55 个 `##` 段(含 Unreleased,`grep -c '^## ' CHANGELOG.md` → 55),0.26.6 修 Codex 压缩 rollout 被整类漏扫,0.26.7 修块序导致的续聊 400;每加一家来源至少要动:描述符 + 转换器 + spec + 派生根因 + 测试锚点(CI 强制)。这是典型的「格式军备竞赛」成本,不会收敛。

## 可信度与复现

**★★★(源码级)**:上述每个机制点都读过对应文件;未安装、未导入真实会话、未跑测试(仓库依赖 `@deepseek-ai/dsh-tools`,本机无 node_modules,`npm test` 需先 `npm ci`)。

读过的文件:`package.json`、`cordis.patch.yml`、`README.md`(结构)、`CHANGELOG.md`(头部与 0.26.6/0.26.7)、`AGENTS.md`(仓库自带,仅确认目录约定)、`lib/index.mjs`、`lib/tools.mjs`、`lib/tools/import-sources.mjs`、`lib/tools/export-tools.mjs`、`lib/toolkit.mjs`(片段)、`lib/convert/{index,core,events,ir,validate,trim,interchange,local-jsonl,claude,codex,cursor,gemini,reasonix,pi,kimi,opencode,dsh,chatgpt,zed}.mjs`、`lib/host-session.mjs`、`lib/import-core.mjs`、`lib/import-state.mjs`、`lib/imports.mjs`(关键段)、`lib/import-batch.mjs`、`lib/workspace-group.mjs`、`lib/attachments.mjs`(头)、`lib/budget.mjs`、`lib/import-prefs.mjs`(关键段)、`lib/retract.mjs`(头)、`lib/purge.mjs`(头)、`lib/export/claude.mjs`、`lib/export/common.mjs`、`lib/export-tool.mjs`、`lib/discovery/registry.mjs`、`lib/discovery/{claude,jsonl}.mjs`(roots 段)、`lib/sources/sqlite.mjs`(头)、`lib/chat-import-service.mjs`、`lib/panel.mjs`(路由段)、`lib/file-import.mjs`、`lib/atomic-write.mjs`、`.github/workflows/ci.yml`、`.github/scripts/check-test-discipline.mjs`,测试:`test/index-tools.test.mjs`、`test/index-reimport.test.mjs`、`test/matrix.test.mjs`、`test/export.test.mjs`、`test/opencode-export.test.mjs`、`test/_support/fake-host.mjs`(头)。

```sh
# 1) 克隆与提交
git clone --depth 1 https://github.com/Nwflower/dsh-chat-import.git \
  .work/mine/cards/chat-import/repo
cd .work/mine/cards/chat-import/repo
git log -1 --format='%H %ad %s'
# → ba599183390164484d5f5894585ddb8f6abb2228 2026-11-15 fix(cherrystudio): ...

# 2) 规模
find lib -name '*.mjs' -exec cat {} + | wc -l          # → 36 286
find lib/convert -type f -exec cat {} + | wc -l        # → 12 795
find test -name '*.mjs' -exec cat {} + | wc -l         # → 40 270
grep -rho 'export function convert[A-Za-z0-9]*' lib/convert/*.mjs | sort -u | wc -l  # → 42
# 格式数:37 个发现源 + local-jsonl = 38 个 import_chat 格式
node -e "const t=require('fs').readFileSync('lib/discovery/registry.mjs','utf8');console.log(t.match(/SOURCES = Object\.freeze\(\[([\s\S]*?)\]\)/)[1].split(',').filter(Boolean).length)"  # → 37
grep -c "format: '" lib/tools/import-sources.mjs         # → 38

# 3) 扩散(在 awesome-dsh-plugin 仓库根;不能直接展开 11 744 个文件)
grep -ril 'chat-import' data/plugins/ | wc -l           # → 1
grep -ril 'chat-import' data/plugins/                   # → 只有 Nwflower__dsh-chat-import.yml
grep -ril 'Nwflower' data/plugins/ | wc -l              # → 3(作者自己的三个插件,互不提及)

# 4) 边车与实时值
node -e "const d=require('./data/downloads.json'),s=require('./data/stars.json');console.log(s['https://github.com/Nwflower/dsh-chat-import'],d['https://github.com/Nwflower/dsh-chat-import'])"
# → { stars: 71, checkedAt: '2026-08-19' } { downloads: 4273, checkedAt: '2026-08-19' }
curl -s https://api.github.com/repos/Nwflower/dsh-chat-import   # → stargazers_count 318 / forks 49 / created 2026-08-13

# 4b) session 类下载排名(边车 × 条目 category；简易解析只读 url/category 两行)
node -e 'const fs=require("fs"),d=require("./data/downloads.json");const r=fs.readdirSync("data/plugins").filter(f=>f.endsWith(".yml")).map(f=>{const t=fs.readFileSync("data/plugins/"+f,"utf8"),u=(t.match(/^url:\s*(\S+)/m)||[])[1],c=(t.match(/^category:\s*(\S+)/m)||[])[1];return{c,u,dl:u&&d[u]?d[u].downloads:0}}).filter(x=>x.c==="session"&&x.u).sort((a,b)=>b.dl-a.dl);console.log(r.slice(0,3).map(x=>x.dl+" "+x.u).join("\n"))'
# → 4273 Nwflower/dsh-chat-import / 3568 … / 2373 …(第一与次高)

# 5) 类目分母(权威)
python3 _digested/ecosystem/census.py 2>/dev/null | head -8   # → session 914 / 总计 11 744
```

**未读**:`lib/convert/` 里其余 ~30 个来源转换器(只读了 18 个)、`lib/sources/*`(SQLite 来源的 host 适配,只读了 `sqlite.mjs` 头)、`lib/discovery/*` 的各源扫描器(只读 registry 与 roots)、`lib/discovery-host.mjs`、`lib/verify.mjs`、`lib/handoff.mjs`/`resume-command.mjs`、`lib/upload.mjs`、`src/client/`(浏览器面板)、`docs/`(14 篇)。因此「某一家格式的解析细节是否正确」不在本卡保证范围内;本文只对**结构与契约**负责。

## 待验证

1. **真实宿主里的导入→续聊闭环**:CI 冒烟只证明插件能在真实 dsh 里 boot + 跑一轮 LLM(`.github/workflows/ci.yml:92-128`),没有导入任何会话。需要在 `dsh web` 里导入一份真实 Claude 转录,发一条新消息,确认无 400 且上下文接得上。
2. **318 星的增长曲线**:只有 71(08-19)与 318(11-18)两个点,无法区分一次性传播与持续增长;`stargazers` API 需认证,本次未取。
3. **42 个转换器里到底多少家真的产出 `usage`**:本卡按 `step.usage` 赋值点统计为 7 个转换器文件,但没逐家核对源记录是否真的带 usage 字段(尤其 Codex/Gemini/Kimi 是否另有回填路径)。
4. **Claude 导出的真实可加载性**:README 自称「可被 Claude Code `--resume` 加载」,但测试只有结构断言(`test/export.test.mjs`),没有真正启动 Claude Code 加载;需实测。
5. **压缩会话的往返**:代码上 Claude 导出会跳过压缩事务、只留被遮蔽的原始轮次;用一条真实压缩过的 DSH 会话走 `export_chat` → `import_chat` 验证模型看到的是否真的退回全量历史。
6. **孤儿会话的实际概率**:`create` 成功而 `endRegistryBatch` 失败会留下无 registry 记录的会话,`retract_import` 与 purge 都依赖 registry 归属(`lib/retract.mjs:1-12`);需要一个故障注入实验来确认用户是否还能在 History 页看到并删掉它。
7. **registry 的「13 家」何时更新**:`data/plugins/Nwflower__dsh-chat-import.yml` 的 description 与代码差两代(13 vs 25+ vs 38);需确认这是上游采样延迟还是条目自述未同步,否则下一轮刷新仍会重复这个数字。
