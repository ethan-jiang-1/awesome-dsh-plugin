---
kind: card
domain: proactive_agent
subcategory: runtime-forks
repo: NelsonLongXiang/dsh-open-a2a-net
commit: 41517214ed7175caf88f5c190b78f976d8c9c513
evidence: 3
status: active
asof: 2026-11-25
---

# open-a2a-net — 只 vendor 2,088 行纯内核，把 A2A 的签名与结算套在外面

> ★★★ 源码级，`NelsonLongXiang/dsh-open-a2a-net@4151721`（2026-11-25 15:51 +0100，工作树干净）。
> 星标/npm 为 2026-11-26 实时读数；结构事实截止 2026-11-25。逐条深读见 [FAQ 06](../../../_faq_on_digested/02_superagent-dependents/lines/06-vendored-engine-a2a.md)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 / 类目 | `NelsonLongXiang/dsh-open-a2a-net` / **remote**（13,136 条里 365 条） |
| 自述 | "Open A2A network plugin for DeepSeek Harness: signed agent cards, decentralized peer/zone discovery, direct routing model tools, joinable session nodes"（`package.json:4`） |
| 声量 | **10★ / 3 forks / 44 open issues**（GitHub API 2026-11-26）；created 2026-08-19，pushed 2026-11-26T01:36Z，`fork: false`、`archived: false`、MIT |
| repo@commit | `41517214ed7175caf88f5c190b78f976d8c9c513`，2026-11-25，`Merge pull request #925 … docs/record-081-published` |
| 包形态 | npm `@nelsonlongxiang/dsh-open-a2a-net`：latest **0.8.2**（2026-11-25T17:03Z）、55 个版本、maintainer `yuanguang`、`dependencies` 为空；**卡针的 commit 里 `package.json:3` 仍写 `0.8.1`**——0.8.2 的发布提交晚于本 commit，未在本次克隆中读到 |
| vendor 了什么 | 上游 `src/core/` **15 个文件 / 2,088 行** + 上游自己的 **2 个测试 / 1,682 行**，落 `src/superagent/upstream/dsh-superagent/` |
| 是否逐字节相同 | 是：`cmp` 15/15 core + 2/2 测试全部 same；`node scripts/superagent-upstream.mjs` 输出 `{"ok":true,"files":17,"problems":[]}` |
| 锁定方式 | `UPSTREAM.json` 记上游 commit `8c32a9dc…` + 每个文件一条 sha256；校验脚本 88 行，同时查"目录里多出文件""sha 不符""内核 import 出界" |
| 适配层规模 | `src/superagent/` 去掉 `upstream/` 为 **52 个 TS / 13,723 行**，是内核 2,088 行的 **6.57 倍** |
| 依赖面 | **20 个 peer**（19 个 `@deepseek-ai/*` + `react`），运行时依赖 **0**；不依赖 `dsh-superagent` 包（上游 `private: true`，也没有包可依赖） |
| 整仓规模 | `src/` **173 TS/TSX / 43,960 行**；`*.spec.ts` **424** 个（`tests/` 下 366 个自有 + 2 个 vendored + `nexus-stage/tests` 56 个） |
| 署名 | `THIRD_PARTY_NOTICES.md:8` 自述 "vendored unchanged"；MIT 原文随包带在 `docs/licenses/` |

## 它到底是什么

**一句话：上游的领域引擎被当成库原样搬进来，"跨主机接活"这件事另做一套授权与结算面。**

它不是一个 fork，而是**两代并存**：

- **p2（外挂 Source）**：`src/superagent/a2a-watch.ts`（707 行）是写给上游 superagent 的 Source 插件，启用方式是往上游 `cordis.patch.yml` 插一行，**不改上游一行代码**。
- **v4（内嵌宿主）**：`src/superagent/host/`（46 个 TS）在自己的进程里组装 vendored 内核，自己实现上游的六个端口；p2 的 `a2a-watch` **原样复用**——`host/a2a-source.ts:1-16` 直说"这个文件是它期待的 `SourceHost`/`SourceContext`"。

**只搬 core，不搬 app。** 上游 `src/` 有 110 个 TS/TSX，这里只搬 15 个；剩下的 `app/`、`sources/`、`client/`、`executor/`、`infra/`、`policy.ts`、`admission.ts` 共 95 个全按端口重写。理由写在 vendored `README.md:15`："store、views、panel 与它自己的 app 缠在一起"。可搬的判据是**纯**：`ids.ts` 之外不 import 任何外部东西，`scripts/superagent-upstream.mjs:28-29` 把白名单收成 `node:crypto` 与 `vitest`。

**两层正交授权**——这是它最值得读的机制，它没有把两套授权缝成一套：

| 层 | 回答什么 | 载体 | 锚点 |
|----|----------|------|------|
| Ticket / Mandate（上游） | 谁**可以让这个 agent 干活**、能干到哪 | 不可变 Mandate，记 policyVersion / scope / strength / actor | upstream `src/core/tickets.ts`、`model.ts` |
| A2A 任务授权（本仓） | 谁**可以结算这条任务** | 入站行出生时冻结的 `auth`，结算前比对 `chain_role` | `docs/design/114-task-authorization.md:128,292-301` |

那层的样子：`auth = { caller, proof, ingress, via, admission_rule, basis, allowlist_version, target, receipt_target, received_at }`，**出生即冻结**、台账不提供修改方法（`:128`）；`allowlist_version = "al1:" + sha256(canonicalJSON(inputs)).slice(0,16)`，输入只取"本机运营者可控、准入代码真读到"的记录，**故意不含**名片缓存里的 `canvasOrg` 和在线节点集合（`:196-199`，理由是同缓存冷热抖动）。结算资格是一张封闭表 `target` / `target-member` / `host-face` / `legacy`，其余一律 `off-chain`（`:294-301`），被拒时记 `settler-off-chain`（`:356`）。

签名节点在另一侧：`src/card.ts:1-16` 是"带过期时间的签名名片"，Ed25519 签身份/团队/能力/过期，TTL 2 天（`:14`）；但它证明的只是**密钥持有**，不是人的同意——这句被写进 router 的人格文本："A CLI signature proves an agent key, not human consent"（`cordis.patch.yml:56`）。

## 怎么接进 DSH

1. **分发**：`package.json` 的 `dsh.bundle.patch` 指向 `cordis.patch.yml`，是标准 bundle 层；`dsh plugin --profile <name> add @nelsonlongxiang/dsh-open-a2a-net`（`cordis.patch.yml:10-13`），该命令 pnpm 装包并 reconcile 进 profile 的 `dsh.profile.bundles`。
2. **挂载点**：patch 插入两件——`- id: a2a`（`:19`，插件本体）与 `superagent-router-preset`（`:27`，router 会话的 preset，含 persona、agent-instructions、time-context、tool-*）。插件**不自带 listener**，要与一个 `webserver` 行同组装（`:4-8`）；标准 web profile 已经有。
3. **客户端**：`package.json` 的 `client.inject` 声明 `dsh-client-locale`、`dsh-client-ui-slots`、`dsh-client-ui-sidebar`；入口有两处——侧栏 footer 的 A2A 控制（`sidebar.footer.action`，把本机会话列为可 join 节点、逐行 join/leave，`src/client/index.ts:54-55`）与右栏两个 tab（`sidebar.right.pane.tab`：团队请求 / 决策，`src/client/team-request.ts:45,50`）。
4. **运行前提**：节点上能跑 `a2a-net`，进程环境里有 `A2A_CLI_HOME` 指向这个 Source 专用身份目录；该身份的家宿主须 ≥ next/0.8——信箱行的 `proof`、`receipt_for`、`admission` 字段是 0.8 才有，老宿主缺字段按 unverified/unlinked 处理（`superagent-a2a-watch.md:26-28`）。
5. **接单还要名单**：A2A 调用方都是 agent（`human: false`），只按 Source policy 的 `bots` 名单接收，名单外一律 `not_human`；宿主链接集与 bots 名单**两层都要满足**（同上 `:28`）。
6. **依赖面**：20 个 peer、0 运行时依赖，等于把宿主版本风险全放在 peer 范围上；包内同时导出 `./a2a-watch` 与 `./superagent-ptc`，两代并存也体现在 exports 上。
7. **状态**：团队级一份 `<a2a home>/superagent/`（JSON 仓储）、绑定在 `executor.json`、`auth` 与账本在 a2a 自己的 `tasks.json`；隔离只到 home 一级。

## 关键实现

| 上游端口 | a2a 的实现 | 锚点 |
|----------|-----------|------|
| `Repositories` | `<a2a home>/superagent/` 下的 JSON 仓储，135 行 | `host/store.ts` |
| `Policy` / `SourceScope` | 属主团队设置 → `teamPolicy` / `teamScope`，665 行 | `host/policy.ts` |
| `Assessor` | 上游的"主 Session"换成本地 router 会话：候选以**卡片**送进去，只能经 `superagent_route` 决策，不许自由文本 | `host/index.ts:8-9`、`host/cards.ts`（217 行）、`cordis.patch.yml:39` |
| `Executor` | **固定成员池**：一成员一槽，无空槽就排队；交接/阻塞/失败 parking 后接下一单，859 行 | `host/executor.ts:1-18` |
| `Outbox` | workbench 回复挂在该 Thread 上；其余 Channel 待后续 PR | `host/index.ts:10-11` |
| `SourceHost` / `SourceContext` | p2 的 `a2a-watch` 原样跑；`commands` 直接调**真的** `a2a-net` CLI，复用其 JSON 契约而非进程内重写 | `host/a2a-source.ts:1-16` |

**一条入站任务的数据流**：`a2a-net` 信箱 → `a2a-watch` 翻成 `human: false` 的 Trigger → 引擎 intake/eval → 卡片进 router 会话 → `superagent_route` 决定 accept / attach / stop / ignore → Ticket + Mandate → Assignment → 成员池取槽执行 → 成员用 `a2a_ticket_report` 报 progress/waiting/ready/failed → 回执走固定 task id `receipt-<task_id>`，**一个任务只有一张正式回执**（`superagent-a2a-spec.md:124`），之后的外发是同一 context 下的新任务。

**三把锁，锁的东西不同：**

1. **字节锁**：`UPSTREAM.json` 的逐文件 sha256 + 88 行脚本；多一个未列文件、改一个字节、import 出界任一发生即失败（`scripts/superagent-upstream.mjs:70-87`）。
2. **形状锁**：`upstream/snapshot-8c32a9d.ts`（254 行）逐字摘录 `SourceKind`、`SourceHost`、`SourceContext`、`Trigger`、`ChannelRef`，并声明三处刻意偏离（`:31-39`，类型外置成 opaque、`z.ZodType<T>` 换 `SchemaLike`、未用成员省略）；`contract.ts`（38 行）用类型断言钉死 `KindIsUpstream`、`HostFromUpstream`、`TriggerSame`、`TicketOutcomeSame`——编译不过就是契约破了。为什么需要：vendor 的 core 里**没有** `SourceKind`（它在上游 `src/sources/kind.ts`），字节锁管不到。
3. **升级锁**：`--compare <checkout>` 看差异（并报上游新增但未 vendor 的 core 文件）→ `--sync --commit <sha>` 复制并重写清单 → 全量测试（`scripts/superagent-upstream.mjs:7-16`、vendored `README.md:11-14`）。升级是一次要评审的变更，不是 `npm update`。

## 为什么它突出

**只用本仓证据：**

- **唯一把"不变"做成可挂测试的样本。** 这批依赖里，别人说"基于上游"，它是 17 个文件 + 每文件 sha256 + 导入白名单，`{"ok":true,"files":17}` 是 CI 里的一句输出。
- **授权分层而不是缝合。** 上游管"让不让干"（不可变 Mandate），A2A 管"谁来结"（出生冻结的 `auth` + `chain_role`），两层各有载体、各有锚点，而不是把结算塞进 Mandate 或反过来。
- **一个真实事故决定了设计。** `#61`（`direct-bb27ec94`）里 `flushFinals` 把另一条工作线的 final 当成答复、发出一张内容无关的 `completed (auto)` 回执，事后答不出"凭哪条授权结的"（`114:106-122`；该节自注第 2 步"按代码推断，未对日志核实"）；设计上的缺口写在 `:19-22`——"谁发来一句 `[A2A receipt]`，谁就能结算"。解法因此是**两道**——授权链拦"别人替你结"，turn 归属拦"宿主替你结但拿错 turn"，归属锚点改成"steer 被消费后第一条 final"（`:320-340`）。只看身份拦不住这一例。
- **声量很小，且是自循环。** 10★ / 3 forks / 44 issues，3 个 fork 内容未核；注册表里 `NelsonLongXiang` 只出现 2 次、都是本人仓库，`a2a-net` 这个 CLI 名没有被第三方条目引用。影响在**方法**，不在采用。

## 代价与边界

1. **冻结内核也就冻结了上游修复。** 上游在 `core/` 修一个 bug，这里只能一次 `--sync` + 全量测试 + 重新评审；想临时打补丁，sha256 先拦住。
2. **适配层是内核的 6.57 倍**（13,723 vs 2,088）。这是"只 vendor 纯内核"的真实账单：复用越纯，适配越多；上游每加一个端口语义，这里就多一处要跟。
3. **两代并存要维护两套启用方式。** `a2a-watch` 与 `host/` 同时在包里、同时导出，文档要讲两遍；`a2a-source.ts` 靠"原样跑 p2"避免重复实现，也继承了 p2 的已知限制（毒行会让游标停住）。
4. **授权还没真正收紧。** `settlementAuth` 三档默认 `observe`（`src/config.ts:303`），S7 未开：`114:13` 自己写"唯一余项是把默认从 observe 改成 enforce，由 #125 跟踪"，判据与阻断条件在 `:451`。今天"结算方不在授权链上"只被记录，不被拒绝。
5. **类型钉的是快照，不是运行时。** `contract.ts` 是纯类型断言，编译通过不代表运行期两侧行为一致；快照落后于上游是常态（`snapshot-8c32a9d.ts:38-39` 要求新快照独立提交并写明新旧 commit）。
6. **执行体语义已经换了形状。** 上游"一单一会话一目录"，这里"固定成员池 + 排队 + parking + 交接"；Ticket 与 Mandate 的语义保住了，"这单在哪个执行体里跑"这条事实变了，投递不确定性要另写一整套规则（`sending`/`unknown`、重启不重发，`assignment-card-lifecycle.md:7,11,17`）。
7. **不可用的场景**：需要 A2A 网络、`A2A_CLI_HOME`、家宿主 ≥ next/0.8；单人单机自用属于过重装配。
8. **隔离只到 home 一级**：团队一份 `<a2a home>/superagent/`，团队内多个 member 共享一个引擎实例与一本账。

## 可信度与复现

- **★★★（本仓与 vendored 边界）**：读了 `THIRD_PARTY_NOTICES.md`、`UPSTREAM.json`、`scripts/superagent-upstream.mjs` 全文、`host/{index,executor,a2a-source}.ts` 头注释、`contract.ts`、`snapshot-8c32a9d.ts:28-42`、`card.ts:1-16`、`cordis.patch.yml:1-60`、`docs/design/114-task-authorization.md` 的授权链与结算章节，并对上游克隆逐个 `cmp`。
- **未做**：没在真实 A2A 节点上跑、没跑 424 个 spec、没核 3 个 fork 的内容、没对上游 HEAD 跑 `--compare`。

```sh
git clone https://github.com/NelsonLongXiang/dsh-open-a2a-net /tmp/nelson-a2a && cd /tmp/nelson-a2a && git checkout 4151721
node scripts/superagent-upstream.mjs        # {"ok":true,"files":17,"problems":[]}
UP=/tmp/sa-research/upstream                # 上游 8c32a9dc 的克隆
for f in src/superagent/upstream/dsh-superagent/src/core/*.ts; do cmp -s "$UP/${f#src/superagent/upstream/dsh-superagent/}" "$f" && echo same; done | wc -l   # 15
find src/superagent -name '*.ts' -not -path '*/upstream/*' | xargs wc -l | tail -1          # 13,723
curl -s https://registry.npmjs.org/@nelsonlongxiang%2Fdsh-open-a2a-net | python3 -c 'import json,sys;print(json.load(sys.stdin)["dist-tags"])'
```

## 待验证

1. **端口实现是否真的只经端口**：读的是 `host/index.ts` 的契约声明与 `deps.ts` 的注入面，没逐行核 46 个 host 文件里是否仍有直接读引擎内部字段的地方。
2. **成员池执行器与上游 Assignment 语义的等价性**：`executor.ts` 自述 parking/交接/重试规则，上游 `docs/003-execution.md` 里 Assignment 的约束是否逐条保住，未对照。
3. **`observe` → `enforce` 的现场数据**：#125 的判据要求"结算方不在授权链上的结算数 = 0"连续 7 天，仓库里只有设计文本与阻断条件，没有实测数字。
4. **npm `0.8.2` 与 `4151721` 的差异**：发布提交晚于本 commit（npm 时间 17:03Z，HEAD 的 `package.json` 仍是 0.8.1），tarball 内是否只多了版本号，未核。
