# hindsight — 宿主项目的示例插件,却是 memory 领域的接口层标准

> 证据等级:★★★(源码级;`vectorize-io/hindsight@9fb28dbd724dc1ce4da7cb4c49008e601db76c5f`,2026-11-17)。
> 数据截止 `29b3ed46e`(2026-11-17)。⚠ 星标 20218 为宿主项目背书,且为 2026-08-19 历史采样。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `vectorize-io/hindsight#coding-agents`([registry](../../../data/plugins/vectorize-io__hindsight--hindsight-integrations-coding-agents.yml)) |
| 类目 | memory(504 条) |
| 自述 | 「会学习的 Agent 长期记忆:自动召回/保存、知识页、深度反思、按仓库隔离的记忆银行」——四项在适配层都能找到落点;但对模型暴露的工具面是**页中心**(搜页/读页/反思/记 initiative),没有 recall/remember 这类读写原语 |
| 星标 ⚠ | 20218(**宿主项目背书**,非插件热度;2026-08-19 冻结采样) |
| 扩散 | **9 个第三方衍生**(其中 **7** 个以 `dsh-hindsight-*` 命名,2 个仅在描述中提及;旧卡写的「8 个前缀」是错的,复现命令见末节) |
| 仓库 commit | `9fb28dbd`(2026-11-17,`main`),单条目目录 `hindsight-integrations/coding-agents/` |
| 包形态 | npm `@vectorize-io/hindsight-coding-agents@0.8.7`,**一个包覆盖 `hindsight-integrations/` 下 48 个目录**;DSH 的面 = 一条 Cordis plugin row + patch 层 + 一个 companion skill,不走 MCP |
| 适配层规模 | `src/dsh.ts` 458 行 + `src/core/transcript-dsh.ts` 109 行 = **567 行**;测试 449 行(`src/dsh.test.ts` 322 + `transcript-dsh.test.ts` 127);`cordis.patch.yml` 18 行;e2e 39 行 |

## 它到底是什么

不是"一个 DSH 插件",而是**一个记忆服务 + 一层薄客户端 + 一整个宿主适配器家族**(`hindsight-integrations/` 下 48 个目录)。DSH 适配器复用的核心只有三件事:配置解析、bank 解析、HTTP 客户端;其余全在服务端。

记忆的对象模型(从客户端代码可确证的形状,不是 README 转述):

- **bank** — 记忆库,默认按 git 仓库动态派生,模板 `coding-agent::{gitProject}`(`src/core/bank.ts:47-53`)。worktree 共用主仓的 bank;探不到仓库时**跳过整个会话**而不是猜一个 bank(`bank.ts:60-70`、`host-client.ts:40-43`,issue #3950)。
- **document** — 写入单位。会话正文写成 `conversation:<sessionId>` 一个文档(`src/core/chat.ts:329`);ingest 进来的资料是另一份文档;git 历史是 `gitlog:<project>`。每份带 `tags` 与 `metadata`(`source:chat`、`harness:dsh` 由插件强制写入,见 `src/core/retain-stamp.ts:37-40`)。
- **memory / observation** — 服务端从文档抽取出来的条目。客户端只发 `POST /v1/default/banks/<bank>/memories`(`src/core/hindsight.ts:476,515-546`),**抽取逻辑在服务端,本次未读**。
- **page** — 服务端合成并持续维护的"知识页"(架构、约定、过往决策、在办 initiative)。工具面是 `searchPages` / `listPages` / `getPage`(`hindsight.ts:960-1035`),服务端做 BM25+向量的 RRF 融合,所以客户端**故意不返回 score**(`page-tools.ts:222-226`:满分也只有约 0.03,模型会误读成"3% 相关")。
- **reflect** — 对整库做一次 agentic 综合,回答"为什么",`POST /banks/<bank>/reflect`(`hindsight.ts:839-846`)。

三层分工是清楚的设计:**页给"是什么",reflect 给"为什么",recall 给"当时怎么说"**。

## 怎么接进 DSH

DSH 面只有三样东西,全部可从源码确证:

**① manifest 是 patch,不是 manifest 字段集合。** `package.json` 里只有 `"dsh": { "bundle": { "patch": "./cordis.patch.yml" } }`,外加 `exports["./dsh"] → ./dist/dsh.js`。真正被 DSH 读的是 18 行的 `cordis.patch.yml`:一条 `insert`、`id: hindsight`、`name: "@vectorize-io/hindsight-coding-agents/dsh"`(`cordis.patch.yml:15-18`)。安装器走另一条等价路径——直接改 `$DSH_HOME/cordis.patch.yml`(`~/.dsh`),把 `name` 写成 `file://` URL(`src/installer.ts:1770-1788`);注释里明说裸绝对路径不是合法的 ES specifier,会被静默跳过。

**② 绑四个 Cordis 生命周期事件 + 一个 tools 注入**(`src/dsh.ts:443-456`):

| DSH 事件 | 去向 | 干什么 |
|---|---|---|
| `agent/session-start` | `RuntimeCore.seedIfCold` | 冷仓后台播种(git log + 代码库 survey),**不 await** |
| `agent/pre-step`(`prepend: true`) | `RuntimeCore.onPrompt` | 触发召回,把记忆作为一条 message 追加进本轮 |
| `agent/turn-stopping` | `RuntimeCore.onSessionIdle` | 重新取 transcript,写回记忆库 |
| `agent/disposed` | `liveAgents.delete` | 释放 agent 引用,否则长跑 Web 服务会钉住所有历史会话 |
| `ctx.inject(["tools"])` | `ctx.tools.register` | 注册 8 个 `hindsight_*` 工具 |

**③ 零 dsh 依赖,靠结构化类型对齐。** `src/dsh.ts:20-23` 明说这个文件不从 dsh import 任何东西:host 形状全部手写 interface,工具的 `parameters` 也是手写 JSON Schema 投影(`toDshParameters`,`dsh.ts:352-376`)而不是 `defineTool`。代价是"只支持 string 参数";收益是 profile 里不需要 pnpm 解析 dsh 包,也没有版本要对齐——**任何事件名仍匹配的 dsh 都能加载**。

几个只有在 DSH 语义下才成立的细节:

- **注入的是 user 消息,不是 system prompt**。`source: { kind: "plugin:hindsight", form: "recall" }`(`dsh.ts:246-253`),用 DSH 自己的 `form: 'recall'` 词汇让 UI 渲染成"召回材料";`runtime.ts:229-240` 解释了原因:块每轮变化,放进 system prompt 会打断 provider 前缀缓存。
- **去重从历史里读,不用内存 map**。`lastInjectedText()` 倒扫 session 事件找上一条自己注入的块(`dsh.ts:264-273`),相同就不重复追加(#5026/#5940:fork 继承历史、进程重启都会让内存 map 失效)。
- **一个 dsh 进程服务多个仓库**。`RuntimeCore` 按 workspace root 建并缓存(`dsh.ts:127,173-197`),bank 按调用方 agent 的 `session.header.cwd` 解析,而不是进程 cwd;工具名仍是按启动目录解析出的那套(`dsh.ts:396-401`,注释自承这是唯一硬边界)。
- **fork 只写自己的新增轮次**。`ownEvents()` 用 `inheritedEventCount` 切掉继承前缀(`dsh.ts:154-158`),否则子会话第一次写回会把父会话的历史重抽一遍。
- **subagent 直接跳过**(`dsh.ts:210-216`):注入会为一次委派付第二次召回,写回会把父会话已经完整保存的片段再存一份。
- **兼容 DSH 的 API 断代**:`snapshotEvents()`(alpha.4+)优先、`events` 属性回退、两者都无则返回空日志(`dsh.ts:141-145`)——注释点明这正是 alpha.4 的真实故障形态。

另外还装一个 companion skill 到 `~/.agents/skills`(`core/skill-dirs.ts:25`,与 Codex 共根),`skill/SKILL.md` 742 行,内容从 README 生成(`scripts/build-skill.mjs`)。

## 关键实现

适配层文件结构(`hindsight-integrations/coding-agents/`):

```
cordis.patch.yml            # 18 行:DSH 唯一真正读的 manifest
package.json                # dsh.bundle.patch + exports["./dsh"]
src/dsh.ts                  # 458 行:事件绑定、注入消息、工具注册、per-workspace 缓存
src/core/transcript-dsh.ts  # 109 行:SessionEvent 日志 → TransportTurn[]
src/core/runtime.ts         # 400 行:跨宿主共享的生命周期(DSH 只提供事件)
src/core/host-client.ts     #  86 行:workspace → (cfg, bankId, client) 的唯一构建器
src/core/page-tools.ts      # 379 行:8 个工具的 spec(与 MCP 共用)
src/core/page-injection.ts  # 149 行:注入给模型的 preamble / 工具指南
src/core/bank.ts            # 394 行:动态 bank 解析(worktree 感知)
src/core/config.ts          # 960 行:分层配置,~/.hindsight/coding-agent.json
e2e/Dockerfile.dsh          # DSH 有独立 CI 镜像 + stub model composition
```

**写入路径**(`turn-stopping` → `chat.ts:273-360`):
`ownEvents(session)` → `readDshEvents`(只保留 `source.kind === "user"` 的用户消息、assistant 文本、`tool/call` 的紧凑 action 行;`tool/result` 故意丢弃)→ `onSessionIdle` 重新拉一遍完整 transcript → `retainedTurns` 比较长度,只有增长才写 → **fire-and-forget**(`runtime.ts:356-399`),`ensureDaemon` 后再 `retain`,失败只落 `retain_failed` 诊断。写回被 `retainSessions` 开关控制,默认开。

**召回路径**(`pre-step` → `runtime.ts:168-227`):
`promptOf` 只取 `source.kind === 'user'` 的文本(工具续跑没有新输入就直接返回,不重复召回)→ `buildHookOutput` 按 `cfg.autoInject` 选一路:**默认 `reflect`**(`config.ts:580-588`),可选 `pages` / `recall` / `none` → 结果缓存在 session cache 里,一个会话只跑一次 → 适配层把 `pages preamble` 与本次记忆块拼成一个字符串 → DSH 侧与历史里上一条注入块比对,不同才追加成 message。

**存储位置**:记忆本体**只在服务端**;本地只有 tmpdir 下的会话缓存、usage 与诊断文件(`session-cache.ts:24-25`、`diag.ts`)。三种后端同一个 HTTP API:`cloud`(默认 `https://api.hindsight.vectorize.io`)、`self-hosted`、`daemon`(本机 `hindsight-embed`,端口 9077,`config.ts:598-603`、`daemon.ts:1-38`)。

## 为什么它突出

**星标不能说明任何事,扩散能。** 但"扩散"要拆开看,9 条衍生的性质并不相同:

| 类型 | 衍生 | 依赖的是谁 |
|---|---|---|
| 换一套记忆工具(`dyrcjqlgcj` 自述注册 10 个 `hindsight_local_*`) | dyrcjqlgcj/dsh-hindsight-local、jackyytche/dsh-hindsight-memory、meisijiya/dsh-hindsight-memory、snakejohn/dsh-hindsight-local | **Hindsight 服务端** |
| 只做本地服务生命周期 | Hua1Q1nG/dsh-hindsight-local-optimize | `hindsight-embed` 守护进程 |
| 只做控制台 / 配置面板 | Apauto-to-all/dsh-hindsight-control-plane、KouzakiUmi/dsh-hindsight-gui | **Hindsight 服务端** |
| 仅提及 | SMPcosy/dsh-memnexus(可选云后端)、soberkeen/dsh-vault(把记忆目录纳入备份) | 数据目录 / API |

也就是说:**标准收敛发生在"服务端 API + 配置文件 + bank 命名"这一层,而不是在这个插件的接口层。** 证据是源码级可查的:配置固定单文件 `~/.hindsight/coding-agent.json`(`config.ts:42`),bank 固定 `coding-agent::{gitProject}`,bank 的注释明说这个默认值**故意 harness 中立**,让所有 coding agent 共享一个仓库一份记忆(`bank.ts:47-53`)。于是第三方只要照抄这份约定,就能和官方插件读写同一个库——`dyrcjqlgcj` 的条目自述"不要与官方 `@vectorize-io/hindsight-coding-agents` 同时启用,两者读同一个记忆库,会重复注入上下文",正是这条 ABI 存在的外部证据(该插件源码本次未读,属自述级证据)。

对照 **OpenViking**(3 个衍生、29567 ⚠):两者都是"宿主项目 + 示例插件",差别不在星标,在**衍生者接手的是哪一层**。OpenViking 的衍生落在"重新实现 / 管理工具 / UI 增强",彼此不共享一个可复用的配置与 bank 契约;hindsight 的衍生共享一个服务端 + 一份约定俗成的配置,bank 名和配置路径就是接口。**能被别人对着抄的接口,才算标准;只能被对着抄 UI 的,只是参照物。**

还有一条反向证据支持"官方实现是真的被当基线":`hindsight-integrations/` 下有 48 个目录,DSH 是其中一个有独立 e2e 镜像与 stub-model composition 的宿主(`e2e/Dockerfile.dsh`、`src/e2e/harnesses.ts:316-332`)——社区包装通常不会有 CI。

## 代价与边界

- **默认云**。不配置 `serverMode` 时 `apiUrl` 就是 `https://api.hindsight.vectorize.io`(`config.ts:600-603`)。会话正文、git 历史、代码库 survey 都会离开本机;想留本地必须显式开 `daemon` 或自建服务。这是"安装即上传"的默认值,也是这份集成最该被读者注意的一行。
- **本地模式不便宜**。daemon 走 `uvx --from hindsight-embed`,`daemon.ts:1-38` 自承冷启动要 uvx 下载 + 模型加载,"tens of seconds";衍生条目自述约 450 MB Python 依赖并需自备 LLM key(自述级,未验)。
- **失败一律 fail-open**。`RuntimeCore` 不抛(`dsh.ts:440-442`),每个请求 15s 硬顶(`hindsight.ts:483-487`),reflect 超时/5xx 降级到纯 recall(`hook.ts:316-345`),永久 4xx 不重试(#5207)。结果是**记忆坏掉时会话看起来完全正常**——代价是用户只能靠 `hindsight_diagnose` 或 diag 文件发现。
- **工具注册绑在启动目录**。`registerTools` 用 `process.cwd()` 解析工具名与 schema(`dsh.ts:400`),若启动目录恰好被 `banks.<id>` 关掉,整个进程后续服务其它仓库时**一个工具都不会出现**(代码注释自承)。召回与写回不受影响。
- **与官方插件并存会重复注入**。同一 bank 被两个插件各注入一次;官方没有互斥检测,靠用户读文档。
- **命名成本**。7 个 `dsh-hindsight-*` 里,至少 3 个不提供记忆工具(2 个控制台/面板 + 1 个本地服务生命周期;`KouzakiUmi` 的条目明说工具由官方集成提供),用户按名字选会选到壳;而 `Apauto-to-all` 的条目自述其 HTTP 路由**没有 DSH 访问检查**、控制台默认监听 `0.0.0.0:9999` —— 衍生的安全问题不该记在官方头上,但确实是这个家族的实际攻击面。

## 可信度与复现

证据等级 ★★★:DSH 适配层逐文件读过;`hindsight` 服务端引擎(文档 → 抽取 → observation → page 合成 → reflect)以及 Web/控制台**未读**,凡涉及服务端内部行为的句子都已在正文标注。

```sh
git clone --depth 1 --filter=blob:none https://github.com/vectorize-io/hindsight.git /tmp/an-hindsight
cd /tmp/an-hindsight && git log -1 --format='%H%n%ad'          # 9fb28dbd… / 2026-11-17
wc -l hindsight-integrations/coding-agents/src/dsh.ts \
      hindsight-integrations/coding-agents/src/core/transcript-dsh.ts   # 458 + 109
ls -d hindsight-integrations/*/ | wc -l                        # 48

# 扩散(在 awesome-dsh-plugin 仓库根)
grep -il hindsight data/plugins/*.yml | wc -l                  # 10(含锚自身)
grep -il hindsight data/plugins/*.yml | grep -c dsh-hindsight- # 7 ← 不是 8
```

**更正**:旧版本页与本任务说明都写"8 个直接以 `dsh-hindsight-*` 命名",现算为 **7**;第三方衍生总数 9 不变(`SMPcosy/dsh-memnexus`、`soberkeen/dsh-vault` 不在前缀之列)。旧页的"9 条"与本次一致,错的是前缀计数。

读过的文件:`cordis.patch.yml`、`package.json`、`plugin.json`、`index.js`、`tsup.config.ts`、`src/dsh.ts`、`src/dsh.test.ts`(用例清单)、`src/core/transcript-dsh.ts`、`src/core/runtime.ts`、`src/core/host-client.ts`、`src/core/page-tools.ts`、`src/core/page-injection.ts`、`src/core/config.ts`(关键段)、`src/core/bank.ts`(前 120 行)、`src/core/hindsight.ts`(retain/reflect/recall/pages 段)、`src/core/chat.ts`(retain 段)、`src/core/retain-stamp.ts`、`src/core/daemon.ts`(头注释)、`src/core/session-start.ts`(头注释)、`src/core/seed.ts`、`src/core/skill-dirs.ts`、`src/installer.ts`(dsh 段)、`src/harness/registry.ts`、`src/e2e/harnesses.ts`(dsh 段)、`e2e/Dockerfile.dsh`、`e2e/dsh-stub-model.cordis.yml`、`skill/SKILL.md`(头部)。

## 待验证

- 服务端抽取质量:文档进 bank 后如何变成 observation、page 什么时候重写、`reflect` 的 `budget: low`(自动路径)与 `high`(工具路径)差多少 —— 引擎未读,无法判断"记忆准不准"。
- 9 个衍生的源码均未读。它们与官方是否真共用 `~/.hindsight/coding-agent.json` 与 `coding-agent::{gitProject}`,只能从条目自述推断;尤其 `dyrcjqlgcj` / `snakejohn` 两份 `local` 是否各自实现了 bank 命名。
- DSH 版本跨度:`dsh.test.ts` 覆盖了 alpha.4 的 `snapshotEvents` 断代,但 0.2.x 之后是否还有事件/工具签名变化未验证;官方对此的承诺是"事件名匹配即可加载",没有版本矩阵。
- 一次召回的 token 成本:`page-injection.ts:38-46` 说故意不列页标题(避免模型直接抄 id、不搜索),但 preamble + 工具指南本身的长度、以及它每会话占用多少上下文,均未量化。
- 20218 ⚠ 星标的时点与归属:该值为宿主主仓 2026-08-19 采样,与本插件被使用程度无关;真正的使用量证据(下载数、衍生活跃度)本仓没有采集。
