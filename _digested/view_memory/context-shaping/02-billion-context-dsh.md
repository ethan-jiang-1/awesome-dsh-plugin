# billion-context-dsh — 把"何时压、压什么"交给模型：seam 层的三个自动摘要入口被显式置空，唯一自动动作是超窗后的一次持久化抢救

> 证据等级:★★★(源码级;`Tyan66666/billion-context-dsh@3b893134452810909f2b31fe1643b7c70cf77ea4`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 26 为 2026-08-19 历史采样;2026-11-18 实时星标 171;下载边车无记录(采样缺口,不是 0)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `Tyan66666/billion-context-dsh`([registry](../../../data/plugins/Tyan66666__billion-context-dsh.yml)) |
| 类目 | memory(504 条,[census](../../ecosystem/census.py) 全表 11 744 条;类目数取 `view_memory/README.md` 快照) |
| 子分类 | `context-shaping` —— 只改"什么进入当轮上下文",不新增长期存储 |
| 自述 | 「模型驱动的上下文压缩(Active Context Pruning):由模型决定何时压缩、压缩什么」;extended description 自认是 `CompactionEngine` 后端,已停止维护并指向上游统一版 |
| 星标 ⚠ | **26**(2026-08-19 边车);2026-11-18 实时 **171**(GitHub API,约 6.6×) |
| 下载 ⚠ | **边车无记录**(2026-08-19 采样缺口)。npm 包 `billion-context-dsh` 存在(`README.md:37`),但 `data/downloads.json` 无该键 |
| 扩散 | **0**(`grep -ril 'billion-context' data/plugins/` 命中 7 条,减自身 6 条,逐条人工判断后**全部指向另一作者的上游** `ranxianglei/billion-context`,不是对本插件的提及;命令与判定见「为什么它突出」) |
| 仓库 commit | `3b893134452810909f2b31fe1643b7c70cf77ea4`(2026-10-24,`docs: 标注项目已停止维护,指向上游统一版 billion-context (#229)`);仓库建于 2026-08-13,首提交同日;共 202 个提交 |
| 包形态 | npm `billion-context-dsh@0.2.27`,纯宿主面单包(`main: dist/index.js`,无 `dsh.client`);`dsh.bundle.patch` 一条 manifest 契约;`dist/` 1.7 MB(构建时把 `acp-kernel` 内联) |
| 代码规模 | `src/*.ts` **17 个文件 / 7 468 行**(口径:`wc -l src/*.ts \| tail -1`);测试 `tests/*.test.ts` 37 个文件 / 369 处 `test(`;/`scripts/e2e/scenarios/` 6 个 JSON 场景;受管文件 122 个,工作树 5.1 MiB(含 `.git` 1.6 MiB) |

## 它到底是什么

**形态判定:DSH 原生压缩 seam 的实现者 + 一个外部压缩内核的适配层。** 它不是配置包(`src/` 7 468 行),不是远端服务适配层(全仓 `src/` 无 `http`/`https`/`fetch`,只 import `node:crypto` 与 `@deepseek-ai/*`、`acp-kernel`),也不是"薄壳 + 大依赖"——它 `extends CompactionEngine`(`src/index.ts:375`),直接占据宿主 `ctx.compaction` 这个服务名,再把自己不做的压缩算法委托给第三方内核 `acp-kernel`(9 处 import,`package.json:70` 精确 pin `0.0.101`,构建时内联)。

所以它既不是"外部压缩器适配"里那种**通过 MCP/CLI 外挂**的形态,也不是 DSH 官方的摘要式 compaction:它注册在 DSH 自己的 `CompactionEngine` 基类上,但把基类的三个自动摘要入口**改成空实现或抛错**——

| seam 方法 | 行为 | 位置 |
|---|---|---|
| `compactIfNeeded()` | `return null`(永不自动摘要) | `src/index.ts:1052-1059` |
| `compactNow()` | `return null`(显式压缩也不做) | `src/index.ts:1062-1068` |
| `compactRegion()` | 抛 `ManualCompactionError`:"use the compress tool instead of automatic summarization" | `src/index.ts:1075-1086` |

**核心循环只有一条:内核判断"该提醒了"→ 宿主投一条建议消息 → 模型自己写摘要并调 `compress` → 宿主落一次持久化替换。**

1. **判定不在模型侧,在宿主侧的内核里。** `agent/pre-step` 里 `buildNudge()` 先 `processTurn` 喂**整份日志**(`allLogMessages`)和宿主测量的 token 数,内核返回 `nudge.shouldInject`(`src/nudge.ts:281-301`)。`compactIfNeeded` 的空实现只是"不自动动手",压力判断仍由内核在每次 pre-step 算。
2. **投递是一条 durable user 消息,不是 system prompt 补丁。** `createUserMessage({ source: { kind: 'plugin:acp-nudge' } })`(`src/nudge.ts:352-361`);正文里带一张 **seq 范围表**(最多 6 行,`src/nudge.ts:170`),每行给出 `seq start..end — N messages, ~T tokens [tool X% | text Y%]`(`src/prompts.ts:206`)。
3. **压缩由模型书写摘要,没有第二次 LLM 调用。** 工具描述明说摘要要自带路径/决策/数值(`src/tools.ts:158`),内核只负责 block 记账。

**数据模型:没有自己的存储文件。** 一次压缩 = 4 条追加事件(`compaction/start` → `compaction/summary` → 带 `surfaceOp` 的 `user/message` checkpoint → `compaction/end`,`src/region.ts:570-629`),原文留在 append-only 会话日志里;内核状态在内存里的 per-session LRU(`src/state.ts:111-146`),重启后从日志重建 block(`src/state.ts:27-88`、`src/region.ts:675-737`)。所以"摘要存在哪"的答案是:**存在 DSH 会话日志里,和宿主自己的 compaction 事件同一个命名空间**,不是 sidecar 数据库。

## 怎么接进 DSH

**① manifest 只有一条契约:profile 层 patch。** `package.json:34-38` 的 `dsh.bundle.patch` 指向 `cordis.patch.yml`,后者两段:

```yaml
- id: compaction-basic
  disabled: true

- insert:
    - id: compaction-acp
      name: 'billion-context-dsh'
```

(`cordis.patch.yml:27-32`)。第一段是**服务名互斥**处理:同一 realm 只能有一个 `ctx.compaction` 提供者(文件头注释 `:10-14` 说明了原因);第二段把它挂在 **host plane**,因此对该 profile 的所有模式生效。`README.md:68` 的 `dsh plugin --profile web add billion-context-dsh` 是唯一安装动作,装完重启即全局可用。

**② 服务与注册点(四类,全部带冷启动竞态兜底)。** 构造器里按 `ctx.get()` 探测,拿不到就监听 `ctx.on('internal/service')` 重试,且带 `done` 标志防重复注册:

| 注册点 | 内容 | 位置 |
|---|---|---|
| `ctx.tools.register` | `compress` / `decompress` / `search_context` / `acp_status` | `src/tools.ts:1196-1231`;`src/index.ts:639-654` |
| `ctx.commands.register` | `/acp-prune status\|compress\|decompress\|config` | `src/commands.ts:232-255`;`src/index.ts:655-670` |
| `ctx.systemPrompt.section` | 一次性 ACP 纪律,`order: 150`(`100–199` 是工具指导段) | `src/index.ts:812-835`;`src/system-prompt.ts:19` |
| `ctx.inject(['settings'])` | 六个标量旋钮的热更新接缝 | `src/index.ts:530-606` |

**③ 绑 4 个宿主事件。**

| 事件 | 位置 | 干什么 |
|---|---|---|
| `agent/pre-step` | `src/index.ts:710-743` | 先无条件清理孤儿 tool 消息 → 重读 settings → `next()` 放行后算 nudge → 以 `{ kind:'enter', messages:[...decision.messages, nudge] }` 追加 |
| `session/event` | `src/index.ts:676-709` | 成功 compress 的 call/result 对在微任务里隐藏(见「代价与边界」失败模式 2) |
| `agent/request-error` | `src/index.ts:761-804` | 唯一自动动作:provider 确认超窗时抢救一次 |
| `agent/status` | `src/index.ts:756-760` | 回到 idle 时清空抢救预算 |

**④ 依赖面。** `peerDependencies` 19 条(`package.json:49-68`),全部带**显式上下界**而非 caret,例如 `@deepseek-ai/dsh-compaction: ">=0.1.5-alpha.1 <0.2.1-0"`;`dependencies` 为空,`acp-kernel` 只在 `devDependencies`(`package.json:70`)里,靠 tsup 内联进 `dist`。判断:安装后没有外部运行时依赖,代价是内核版本只能在发版时换。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `src/index.ts` | 1 089 | 引擎本体:构造、服务注册、窗口解析、超窗抢救、seam 拒绝 | `:375` 类;`:857-911` 窗口;`:968-1049` 抢救;`:1052-1086` 三个空/抛 |
| `src/region.ts` | 1 702 | 持久化事务、边界求解、日志重建账本、守卫与范围表几何 | `:260-372` 边界;`:528-648` 事务;`:675-737` 账本;`:1145-1237` 守卫;`:1367` 范围表 |
| `src/tools.ts` | 1 236 | 四个工具的参数、守卫、事务调用与结果文案 | `:114-177` schema;`:558-894` compress;`:896-969` decompress;`:1196-1231` 注册 |
| `src/nudge.ts` | 594 | 压力判定、去重、seq 范围表、模板路径 | `:86-103` token;`:281-363` nudge;`:266` 每轮上限 3 |
| `src/messages.ts` | 769 | 事件日志 ↔ 内核 `CoreMessage` 投影、行分类、摘要框 | `:1-12` 桥;`:76-90` 提取;`:35-44` source kind |
| `src/state.ts` | 151 | per-session 内核状态 + LRU + 日志重建 | `:27-88`;`:111-146` |
| `src/prompts.ts` | 256 | 默认话术与系统提示模板、模板校验 | `:189-216`;`:217-250` |
| `src/settings.ts` | 398 | 六旋钮 + 两代 settings 接缝 | `src/index.ts:530-606` 可见调用面 |
| `src/config.ts` | 58 | 三个阈值合并进内核配置 | `:37-58` |
| `src/commands.ts` | 388 | `/acp-prune` 四个子命令 | `:232-255` |
| 其余 | — | `window.ts` 208、`presets.ts` 113、`block-ledger.ts` 130、`host-tokens.ts` 269、`lru.ts` 38、`session-events.ts` 50、`system-prompt.ts` 19 | — |

**A. 何时压:内核算,但只"说",不带手。**

- 分母:显式 `modelContextLimit` > 实时投影 `contextPressure.contextWindow` > `llm.resolveModelInfo` 探测 > 兜底 128 000(`src/index.ts:857-911`),探测失败会 `warn` 并缓存失败结果(`:899-903`)。
- 再减**输出预留**:`applyReservation` 从窗口里减去适配器每次请求的输出上限(`src/index.ts:953-955`),注释给出的例子是 96K 窗口 / 16K 上限 ⇒ 只有 80K 输入预算。
- 阈值:引擎默认 `max 0.70` / `emergency 0.85`(`src/index.ts:261-262`),注释说明为何**低于**内核默认 0.75/0.95 与宿主 compaction-basic 的 0.80 线:强制提醒必须抢在自动摘要之前。可用 `preset` 五档整包覆盖,优先级 显式值 > preset > 引擎默认(`src/index.ts:283-300`),阈值倒挂直接抛错(`:348-360`)。
- 节奏:普通提醒**每用户轮最多 1 次**;紧急提醒每轮最多 **3 次**(`EMERGENCY_NUDGE_MAX_PER_TURN`,`src/nudge.ts:266`),超了走日志解释而不是沉默(`src/index.ts:733-739`)。
- 话术:普通 nudge 只有一句效率提示(`src/prompts.ts:195`),紧急才说"compress now"(`:196`)。

**B. 压什么:范围表给候选,模型定取舍,宿主侧还有四道硬守卫。**

范围表的几何来自内核 `nudge.compressibleRanges`,引擎只做 seq 翻译 + 宿主守卫(`src/region.ts:1367`)。不可压的节点**切断区间**(而非跳过),注释写明理由:跨过它就会 shadow 它(`src/region.ts:1250-1260`):

1. 最近 5 条尾巴(`preserveRecent`,`src/region.ts:1209-1216`);
2. 最后一条**真**用户消息(`isRealUserTurn`,不认注入行,`:1224-1230`);
3. 每个 scope 最新的 AGENTS.md 指令行——宿主发现它消失会立刻重注,压了等于白压(`src/region.ts:1231`;机制解释 `src/tools.ts:355-373`);
4. 最新技能目录行——它的重发门是 digest 不是可见性,压了就永久没了(`src/region.ts:1232-1235`)。

`compress` 工具侧再做一次**硬拒**:用 `guardedSurfaceSeqsOf`(`src/region.ts:1145-1164`)与实际将被 shadow 的位置切片求交,而不是数值区间(`src/tools.ts:673-678`);拒信会点名 seq 并给出**剩下可压的分片**,让模型改刀而不是重试同一调用(`src/tools.ts:415-481`)。

**C. 一次 compress 落什么:4 条事件 + 1 个替换。**

`handleCompress` 依次:清孤儿 → 全量日志建 ref → `kernel.applyCompression` → 逐个范围 `runCompactionTransaction`(`src/tools.ts:748-757, 837-856`)。事务内部:

- 写前校验 span 必须**逐元素等于当前 surface 切片**(`isExactSurfaceSpan`,`src/region.ts:561-567`)——注释说明这不是洁癖:声明与实际不符会让**整份日志在加载时永久不可读**(issue #201);
- `compaction/summary` 里放模型摘要 + `shadowedSeqs` + 宿主口径的 `shadowedTokenCount`(`src/region.ts:599-608`);
- checkpoint 节点用 `surfaceOp: { op:'replace', startSeq, endSeq }` 三键方言(`src/region.ts:619-627`),peer 下界 0.1.5-alpha.1 就是被这三键锁死的;
- 任一步失败补写 `compaction/end`,不留悬挂 start 阻塞后续压缩(`src/region.ts:630-646`)。

摘要文本**只在创建时加一次框**,事件与 checkpoint 节点写同一份字节(`src/region.ts:588-598`),投影侧再做一次幂等兜底;引擎自己写的超窗标记摘要按内容豁免(`src/messages.ts:35-44` 的 kind 声明 + `prefixSummaryBlocks`)。

**D. 可逆性与存储:原文从不删除。**

`decompress` 只读地按 block 回放原文,分页 100 条 / 7 000 字符(`src/tools.ts:896-969`;`src/region.ts:1636-1647`),分页提示放在页首,避免被宿主裁剪时先丢掉"本页不完整"那行(`src/tools.ts:960-965`);`search_context` 在"摘要 + 所有被 shadow 的原文"上做混合检索(`src/tools.ts:1048`,`src/tools.ts` 的 `buildSearchDocs` 按日志快照缓存)。三级蒸馏:压一个 checkpoint 节点 = tier 2,再压 tier-2 = tier 3,`decompress` 会展开回最底层原文(`src/region.ts:1599`)。

**E. 唯一的自动动作:超窗抢救。**

`agent/request-error` 收到 `CONTEXT_WINDOW_EXCEEDED`:用与 nudge 表**完全相同**的几何选最大可压范围(`preserveRecent: 5` 显式钉死,`src/index.ts:1001-1008`)→ 写一条引擎生成的标记摘要(**不调用 LLM**)→ `{ kind:'retry' }`(`:1019-1047, 803`)。预算 `maxOverflowRetries` 默认 1,与宿主 compaction-basic 对齐;模型产出下一条 assistant 消息或回到 idle 时重置(`:676-690, 756-760`)。

**数据流**:

```text
① 建议(每 pre-step,宿主)  日志 ──processTurn──▶ kernel ──shouldInject?──▶ nudge(user 消息, plugin:acp-nudge)
   正文 = 上下文分解 + 最多 6 行 seq 范围表 + tier2/3 蒸馏行
② 压缩(模型)  compress(content[]) ──守卫/边界──▶ 4 条日志事件 + checkpoint(replace) ──▶ 隐藏 call/result 对
③ 取回(模型,只读)  decompress(bN) / search_context(q) ──账本──▶ 原文
④ 抢救(宿主,唯一自动)  400 CONTEXT_WINDOW_EXCEEDED ──▶ 最大可压范围 + 标记摘要 ──▶ retry
```

**测试:** 37 个 `tests/*.test.ts`、369 处 `test(`;`tests/kernel-upstream/search.test.ts` 单独镜像内核行为。与卡内四条结论直接对应的用例名:

| 契约 | 用例(只读名) |
|---|---|
| 自动摘要确实被关掉 + 抢救预算 | `overflow-recovery.test.ts`:`M5: context overflow emergency-compacts the largest eligible block and returns retry`、`M5: retry budget spent without progress → original error preserved (no infinite retry)` |
| 注入守卫不可绕过 | `injection-governance.test.ts`:`B1-1 prefix constant and idempotency`;`checkpoint-span.test.ts`:`a PLAIN range that crosses a live checkpoint carrier is rejected` |
| 前缀稳定 + 方言 + 挂载 | `byte-stability.test.ts`:`an append-only turn preserves every previously-sent byte (issue #111)`;`surfaceop-dialect.test.ts`:`compress lands on a real 0.1.5 session with the startSeq/endSeq dialect`;`bundle-patch.test.ts`:`bundle patch ships the root-realm collision guard` |

## 为什么它突出

**先拆星标归属,再谈"机制独特"。** 这个仓库**不是**上游项目的 monorepo 子目录:2026-08-13 建仓,首提交即引擎本体(`3e386d0 feat: billion-context-dsh — ACP CompactionEngine backend for DeepSeek Harness`,21 个文件 / 4 645 行),至今 202 个提交,无母项目。所以 **171 星属于这个包本身**,不存在"把主项目星标算给插件"的问题。

但机制归属必须说清——**它自述的上游有两层**:内核 `ranxianglei/acp-kernel`(MIT,pin `0.0.101`,原样复用、构建时内联;`AGENTS.md` 规则 11 要求内核缺陷回上游修),与适配范式 `ranxianglei/billion-context-pi`(README 自述"移植",`src/messages.ts:8`、`src/nudge.ts` 头部逐模块对照)。本仓只拥有 DSH 接入:事件形状、seq 作为 ref、durable 事务、日志重建。

时间线一句话:**08-13 建仓+首提交 → 08-19 ⚠ 26 星 → 10-24 HEAD `3b89313` 并标注停止维护 → 11-18 实时 171 星**(约 6.6×)。

**判断:这 6.6× 增长发生在"已弃用"公告前后,说明涨的是"想找 DSH 上 ACP 的人",不是"项目在演进"。** 弃用公告(`README.md:5-9`、`package.json:4` 的 description 也写了 `Unmaintained`)把维护成本转移给上游,评估时是**扣分项而非加分项**:任何新问题都没有本仓的修复路径。

**零扩散,而且是"真零"。** `billion-context` 是这个问题域的高频词,必须逐条排除:6 条命中里,`ranxianglei/billion-context` 是上游官方版,`No-ni/billion-context-patched` 是"上游的补丁构建",`light-cheng/dsh-strata` 提示"先卸载 … 或 billion-context",`wxzjss/dsh-whale-loli` 说"压缩交给 billion-context 插件",`FenrirCait/dsh-session-leftover-purge` 与 `kkkkk-tubu/dsh-deep-purge` 清的是上游留下的快照/索引——**没有一条指本插件**。

窄 token 复核:`grep -ril 'billion-context-dsh' data/plugins/` → 1(自身);`grep -ril 'Tyan66666'` → 1(自身);`grep -ril 'acp-kernel'` → **0**;`grep -ril 'Active Context Pruning'` → 2(自身 + `snow-The__dsh-session-handoff`,后者是**独立实现**的 `acp_*` 工具,描述里没有任何对本插件的引用)。

**判断:概念扩散了(有第二个条目独立做"模型自写摘要的 ACP"),插件没扩散。** 原因不是没人用,而是①它只活了 2.5 个月就弃用,②核心概念名属于上游 `billion-context`,第三方引用时自然指向上游,③DSH 侧的可替代入口(官方 `CompactionEngine`)让"换一个后端"比"提一个 issue"更省事。

**机制上真正值得记的一条:它把"自动压缩"从能力变成了可关闭的默认。** 宿主官方 compaction 是"到线就摘要";这里 `compactIfNeeded/compactNow/compactRegion` 三个入口全部空实现或抛错(`src/index.ts:1052-1086`),压力只以"建议"形式到达模型,压缩的边界、摘要的措辞、以及**是否真的压**都由模型决定。代价与收益都很直接(见下节)。

## 代价与边界

按发生顺序列失败模式,每条有源码位置:
1. **模型不理会建议 → 压力继续涨 → 直到 provider 400。** 这是"模型驱动"的结构性代价:唯一兜底是超窗抢救,且预算默认 **1 次**(`src/index.ts:764-773`)。第二次 400 就原样抛给用户(`:769-773`)。判断:对"听话"的模型是省 token,对"埋头干活"的模型是硬失败。
2. **compress 成功后的 call/result 对必须隐藏,而且不能同步隐藏。** 摘要节点写在 tool 结果之前,留下 `assistant(tool_calls) → user(summary) → tool(result)` 会被严格 provider 判 400(`src/index.ts:671-675`);但 `session.append` **不可重入**,在 `session/event` 里同步 append 会抛 "cannot reenter" 且被派发器吞掉,所以只能延迟到微任务(`src/index.ts:698-708`)。只隐藏"恰好只含这一个 call"的节点,多 call 节点隐藏会孤立兄弟结果。
3. **崩溃留下的孤儿 tool 消息。** 每个 `agent/pre-step` 无条件清理(`src/index.ts:718`),而不只是在 nudge 触发时清(`src/region.ts:919-1016`);`openToolCallIds` 保证本步在飞的兄弟 call 不被误删。
4. **过期 span。** 模型拿旧 nudge 表来压:边被更早的压缩 shadow → 重映射到仍然可见的余量;整段没了 → 报 "already compressed" 并给覆盖它的 block(`src/region.ts:208-258`、`src/tools.ts:650-661`)。写前还有 `isExactSurfaceSpan` 一票否决(`src/region.ts:561-567`)。
5. **宿主版本窗很窄。** peer 全部 `<0.2.1-0`,replace 方言只有三键一种写法(`src/region.ts:619-627`);低版本直接运行时拒压,高版本未验证。这是"精确 pin"换来的可复现性,也是升级成本。
6. **settings 接缝双方言,第三种就降级。** ≤0.1.6 用 `installSection`;≥0.1.7 用 `describe/update/replace`;两者都不是时**只 warn 一次,不注册**(`src/index.ts:594-604`),六旋钮保持组合值。热更新靠每个 pre-step 重读 volatile ref(`:719-722`)。
7. **内存是真实开销。** 构造时把内核文档缓存上限拉到 128 MB(`src/index.ts:449`),注释给出实测:保留堆是计费字符的 1.9×–48.9×,**最坏约 6.5 GB**(`:437-448`)。理由是单用户 profile 的语料常规超过内核默认 8 MB,不调则每次 `search_context` 重算(实测冷热都约 18 s/次,`:440-445`)。判断:这是"搜索可用性"换"进程内存",长会话重的用户要自己权衡。
8. **维护状态是最大的边界。** README 与 npm description 都写着停止维护(`README.md:5-9`、`package.json:4`),功能修复已转到上游统一版;`AGENTS.md` 也被改成同一口径。装它等于接受"不再有修复"。

- **隐私**:全部本地。`src/` 无网络调用;数据写在 DSH 会话日志里(明文,和宿主自身事件同权限面),不新增目录、不上传;`shadowedTokenCount` 走宿主 `tokenMeter` 口径而不是自有估算,避免把宿主的负值投影打穿(`src/host-tokens.ts`,卡内不展开)。
- **前缀缓存**:没有专门的缓存机制。它靠的是**只追加**(append-only)天然稳定;但一次 compress 必然是 `surfaceOp: replace`,从替换点起的出站消息序列会重写(判断,依据 `src/region.ts:624-627`)。字节级守卫只在单测层面钉住"无压缩的追加轮不改任何已发送字节"(`tests/byte-stability.test.ts:7,57`),端到端另有 wire 级断言(`README.md:319` 自述;场景见 `scripts/e2e/scenarios/`)。
- **可观察性**:四个工具 + `/acp-prune` 是全部人工面;`acp_status` 明确不显示窗口行(窗口只给人类命令),模型侧看到的是分解与块账本(`src/prompts.ts:215`)。

## 可信度与复现

- **★★★**:`src/index.ts`(构造、注册、窗口、抢救、三个 seam 拒绝)、`src/tools.ts`(四工具与守卫)、`src/region.ts`(边界、事务、账本、守卫、分页)、`src/nudge.ts`、`src/messages.ts` 头部、`src/prompts.ts`(默认话术)、`src/state.ts`、`src/config.ts`、`src/commands.ts`(命令面)、`src/system-prompt.ts`、`package.json`、`cordis.patch.yml`、`README.md` 头部与安装段、`tests/byte-stability.test.ts` 头部。
- **未读**:`docs/` 19 个设计文档(352 KB,含 `dsh-porting-verification.md`、`overflow-recovery-design.md`)、`dist/`(1.7 MB 构建产物)、37 个测试文件的函数体(只读用例名与 `byte-stability` 头部)、`scripts/e2e/*.mjs`、`settings.ts` / `window.ts` / `host-tokens.ts` / `block-ledger.ts` 的实现细节。体量口径:`.git` 1.6 MiB、工作树合计 5.1 MiB、受管文件 122 个;`src/` 396 KB、`tests/` 660 KB、`dist/` 1.7 MB、`docs/` 352 KB。

```sh
# 1) 提交与仓库时间线
git log -1 --format='%H %ad %s' --date=iso
# 3b893134452810909f2b31fe1643b7c70cf77ea4 2026-10-24 21:07:15 +0800
git rev-list --count HEAD          # 202
git log --reverse --format='%ad %s' --date=iso | head -1   # 2026-08-13 首提交

# 2) 规模
wc -l src/*.ts | tail -1           # 7468 total
ls src/*.ts | wc -l                # 17
ls tests/*.test.ts | wc -l         # 37
grep -rc "test('" tests/*.test.ts | awk -F: '{s+=$2} END {print s}'   # 369
git ls-files | wc -l               # 122

# 3) 形态:DSH 原生 seam + 三个自动入口被关
grep -n 'override async compact' src/index.ts       # 1052 / 1062 / 1075
grep -n "ctx.tools\|ctx.commands\|ctx.systemPrompt\|agent/pre-step\|agent/request-error" src/index.ts

# 4) 扩散(仓库根;11744 个文件必须用目录形式)
grep -ril 'billion-context' data/plugins/ | wc -l            # 7(含自身)
grep -ril 'billion-context-dsh' data/plugins/ | wc -l        # 1(仅自身)
grep -ril 'Tyan66666' data/plugins/ | wc -l                  # 1(仅自身)
grep -ril 'acp-kernel' data/plugins/ | wc -l                 # 0
grep -ril 'Active Context Pruning' data/plugins/ | wc -l     # 2(自身 + snow-The 的独立 ACP)
```

## 待验证

1. **171 星的采样后曲线**。只有 08-19 的 26 与 11-18 的 171 两点;中间是否有弃用公告带来的下跌/回弹,需要 `stargazers` 带时间戳的接口(本次未取)。
2. **`acp-kernel 0.0.101` 内联进 `dist` 后的实际体积与可控性**。`dist/` 1.7 MB 里内核占多少、内核升级是否必须重发本包,未逐文件核。
3. **369 处 `test(` 里内核镜像用例的占比**。`tests/kernel-upstream/search.test.ts` 单独镜像内核搜索行为,但只统计了总数、没有按文件拆分;评估覆盖率时应先剔除这一份。
4. **6 个 e2e 场景的具体断言强度**。只读了 `scenarios/` 文件名与 `README.md:319` 的自述,没有读 `harness.mjs` / `fake-llm.mjs`,因此"wire 级前缀稳定"到底断言到哪一层,待验证。
5. **`settings.ts` 六旋钮的读写路径**在真实 `~/.dsh/settings.yaml` 与 SettingsForms 两种宿主上的行为一致性。卡内只确认了探测分支与降级 warn,没有核 reset/conflict 的具体语义。
6. **官方统一版 `ranxianglei/billion-context` 与它的机制差**。README 说"同一套实现覆盖 20+ 宿主",但本卡未读上游源码,因此"弃用后该用哪个"只能给迁移建议,不能给能力对比。
