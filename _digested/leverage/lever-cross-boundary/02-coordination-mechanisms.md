---
title: "三笔税的机制谱"
domain: cross-boundary
kind: playbook
positioning: "九家协作样本在三笔税上各选了什么机制，以及 §5.5 的三张可落地配方。"
takeaway: "配方 A/B/C：状态归属、冲突裁决（含 epoch）、失败收敛的三层。"
read_when: "要动手写协作机制；或要比较两种协作实现的失效条件。"
status: observed
updated: 2026-10-31
---
# 02 · 三笔税的机制谱：状态归谁、冲突谁裁、崩了谁收敛

> **状态**:`observed` · **基线**:DSH `0.2.1-rc.3` · 名单 7924 条 @ `efe602e7b` · **样本**:9 个协作插件逐条回读源码(见 [03](./03-sample-encyclopedia.md))
> **一句话**:同一笔税，生态里存在**互不兼容的几种交法**。看懂一个协作插件,只要问它三句话:权威状态写在哪张纸上、冲突靠什么裁决、崩溃后靠什么收敛。

## 1. 命题

> 协作插件的差异不在功能清单,而在**为三笔税各选了一种机制**。机制一旦选定,它的失效条件就被写死了——不是实现不够仔细,是那种机制本身的上限。

可证伪点:若存在一个插件,在**不选任何机制**（不持状态、不裁决、不收敛）的情况下仍能稳定协作,命题不成立。

## 2. 杠杆点

| 税 | 可选机制 | 阶梯级 | 供给(`census.py --probe`,基线 7924) |
|---|---|---|---|
| **状态归属** | 会话日志 / 磁盘自有真相源 / 宿主 storageDomain / 独立 broker | 4(policy)+5(backend) | `team` 102 · `captain` 5 · `邮件/邮箱` 13 · `mailbox` 8 |
| **冲突裁决** | 不做（共享 checkout）/ 建议性写范围 / 租约 / CAS / 三路合并 / 独立检出目录 | 4(policy)+5(backend) | `认领` 14 · `claim` 76 · `worktree` 45 |
| **失败收敛** | 不收敛 / 人工改派 / 对账器 / 心跳+租约过期 / 不可变快照重跑 / 链路自愈 | 4–6 | `handoff` 73 · `relay` 81 · `takeover` 14 |

## 3. 机制：三笔税各自的谱

### 3.1 第一笔 · 状态归属：权威写在哪张纸上 `[OBS]`

这是三笔税里分化最彻底的一笔。**九家样本用了五种互不相同的答案**：

| 机制 | 权威在哪 | 代表 | 它换来了什么 | 它付出的代价 |
|---|---|---|---|---|
| 宿主日志派生 | 会话事件流 | 官方 `dsh-experimental-agent-team` | 只凭日志即可重建,重放安全 | 单进程;跨进程读不到 |
| 磁盘自有真相源 | `<workspace>/.<plugin>/<teamId>/*.json` | `NanmiCoder/dsh-agent-teams`(`team.json`)、`Mlte0907/dsh-teams-x`(`.teams-x/`) | 面板可以直读、可与会话日志解耦 | **绕过了宿主日志**,并发进程直接覆盖写 |
| 宿主存储域 | `ctx.storageDomain` 的表 | `limuyang2/agent-team`(`agent_team` 5 表)、`toolclub/dsh-agent-team-gui`(`agent_team_gui` 8 表) | 有官方持久化后端、有 schema | 只能读自己域内的表,团队状态依然不可移植 |
| 独立 broker | 进程外的中继/端口 | `Noelune/dsh-agent-relay`(HMAC broker)、`zbzbhs/dsh-remote-agent`(WS + relay) | 真跨进程 | 多一个常驻进程与一套认证 |
| 文件总线 | 同步盘上的目录 | `IKEASven69/dsh-takeover`(`~/.handoff/`) | 零基础设施 | 没有实时性,冲突由同步盘决定 |

**最值得记的一条反例**:`NanmiCoder/dsh-agent-teams` 的 `docs/usage.md` 明写数据链路是「工具执行 → **磁盘状态（真相源）** → host 快照路由 → 浮层 1s 轮询渲染;会话日志同时写入 `agent-teams/*` 事件（审计/重放/复盘）」。**会话日志被降级为审计,磁盘升级为真相源。** 而它的锁是进程内 promise 链(`src/state.ts:59-88`),于是「多进程同时操作同一团队不保证一致」不是遗漏,而是这个选择的必然结果——**换掉真相源,就换掉了并发模型**。

> **洞察**:官方设计是「持久日志、派生状态」,即日志权威、状态可重算。凡是把真相源搬到磁盘的插件,都在**用可观察性换并发安全**。

### 3.2 第二笔 · 冲突裁决：六种交法,只有一种真的拦住了写 `[OBS]`

| 裁决机制 | 谁拦住写 | 代表 | 失效条件 |
|---|---|---|---|
| 不裁决 | 没人 | 官方 Team、`agent-teams`、`team-gui`、`dsh_workflow`、`eteams` | 后写覆盖先写,无人察觉 |
| 建议性写范围 | 提示词 | 官方 Team(`writeScopes` 只产生 warning:「they never block anything」) | Bash/formatter 绕过 |
| 完成时审计 | 事后的 | `NanmiCoder/dsh-agent-teams`(`changedPaths` 审计) | 发现得了,拦不住 |
| **租约 + 服务端拦截** | **`tools/pre-execute` 返回 deny** | **`Nwflower/dsh-file-claim`** | 只覆盖 `write`/`edit`/`bash`/`pwsh`;shell 解析失败 fail-open |
| CAS | 陈旧写入被拒 | 官方 Team(`expectedRevision` → `TEAM_TASK_STALE_REVISION`) | 只保护**任务元数据**,不保护文件 |
| 独立检出目录 | 物理隔离 | `worktree`(45 条样本) | 合并仍是人的活 |

**`Nwflower/dsh-file-claim` 是全生态唯一在文件写入路径上真拦住写的样本**——它注册 `ctx.on('tools/pre-execute')` 返回 `{kind:'deny'}`(`index.mjs:577-585`),认领存为与被保护文件同目录的边车 `<目标>.dshclaim`。稀缺性可复核:`--probe "\.dshclaim|文件认领|写冲突|file claim|claim_files"` 命中 **1/7924**。

但它**不是带 fencing 的强租约**,这一点比它做了什么更值得写:边车字段只有 `startedAt`/`lastSeenAt`/`pid`,**没有 epoch/generation**。被接管时原主的 `sync` 只刷新「自己还持有的边车」,`mine=[]` 时**不报错**——原主静默失锁,只能靠下一次写入被守卫拒绝才发现。**“锁”在这里的含义是“别人写你会被拦”,不是“你知道自己还拿着锁”。**

### 3.3 第三笔 · 失败收敛：从「人收拾」到「对账器」

| 机制 | 怎么发现 | 代表 | 收敛到什么 |
|---|---|---|---|
| 不收敛 | — | `agent-team`(无任务超时/看门狗)、`dsh_workflow`(进程重启活跃 run 丢失) | 停在原处 |
| 人工改派 | Lead 看见 | 官方 Team(「No automatic ownership release」) | Lead 手动重派 |
| 停驻 + 一次性冷恢复 | 进程内观测 | `agent-teams`(`parkedAttempts`) | 本进程没见过的 open attempt 才重试 |
| 对账器轮询 | 定时扫 | `teams-x`(60s 对账回收搁浅任务、5min 判 orphan 回池) | 任务回池 |
| 租约过期 | wall clock | `file-claim`(stale 2h,pid 判活即刻清孤儿) | 他人接管 |
| 不可变快照重跑 | 内容键 | `dsh_workflow`(`.dsh/workflow-runs/<runId>/` + `results/<cacheKey>`) | 整体重跑并回放缓存 |
| 链路自愈 | 心跳 | `remote-agent`(15s 心跳 / 45s 超时 / 退避 1s→30s) | 副机本地继续,重连后续传 |

**`dsh_workflow` 的“可恢复”需要被准确表述**:它不是断点续跑,而是**从不可变胶囊快照整体重跑 + 按内容键回放已有结果**。这两者在故障语义上完全不同——前者能保住“跑到一半的副作用”,后者只能保住“已经算出来的答案”。

**`remote-agent` 贡献了本域最有价值的一条失败语义**:它的 `agent-false-success.test.js` 记录了一个真实缺陷——DSH 的 `kick()` 是 `try { while (await this.turn()) } catch (_error) {}`,**turn 内的错误被完全吞掉,只通过 `agent/error` 事件暴露**;而它的完成判据当时是 `ok = !timedOut && !aborted`,没看这个事件,于是「TRANSPORT 错误 + 成品 0 项」被标成 `completed`。作者的判断比缺陷本身更值得抄:「报错至少知道要重试;'假成功'会让人以为事情做完了」。

## 4. 三笔税的联合分布：九家各选了什么

| 样本 | 状态归属 | 冲突裁决 | 失败收敛 | 组合结论 |
|---|---|---|---|---|
| 官方 `dsh-experimental-agent-team` | 会话日志派生 | 建议性写范围 | 人工改派 | 元数据硬、工作区软 |
| `NanmiCoder/dsh-agent-teams` | 磁盘 `team.json` | 完成时审计 | 停驻 + 冷恢复 | 用可观察性换并发安全 |
| `Mlte0907/dsh-teams-x` | 磁盘 `.teams-x/` | 完成时审计 | 对账器 | 同上,粒度更粗 |
| `toolclub/dsh-agent-team-gui` | 宿主 storageDomain | 无 | 不收敛(重启全 interrupted) | 持久运行记录 ≠ 可恢复 |
| `limuyang2/agent-team` | 宿主 storageDomain | 无(`leases` 表是空的) | 启动恢复 + 重投 | schema 里有,代码里没有 |
| `omdsh-dev/dsh_workflow` | 不可变胶囊快照 | 无 | 快照重跑 | 可恢复的是**答案**不是**状态** |
| `Nwflower/dsh-file-claim` | 工作区边车 | **服务端 deny** | 租约过期 + pid 判活 | 唯一真裁决,但无 fencing |
| `Chinesezjc/dsh-interconnect` | 对端实例的会话 inbox | 不适用 | 无幂等、无离线队列 | 传输可靠 ≠ 语义可靠 |
| `zbzbhs/dsh-remote-agent` | 副机本地 DSH | 不适用 | 心跳 + 断点续传 | 工作与链路解耦 |

**这张表读出来的一句话**:没有任何一个样本在三笔税上都交得漂亮。**交得最狠的一笔,往往就是它其余两笔最弱的地方**——`file-claim` 把冲突裁决做到服务端拦截,代价是它根本没有成员模型;`agent-team` 把成员异构做到极致,代价是依赖图、租约、文件裁决三样都空着。

## 5. 标杆

**配额**:本卡深读 **2 个**机制标杆——各代表一笔税的极限交法。

### 标杆 A · `Nwflower/dsh-file-claim`(第二笔税的极限:真拦截)

| 必答项 | 内容 |
|---|---|
| **代表什么典型** | 边界 2 的**冲突裁决**这一笔税,以及「只有服务端 deny 才算裁决」这条判断 |
| **为什么选它** | 过 **F**(`--probe "\.dshclaim|文件认领|写冲突|file claim|claim_files"` → **1/7924**)+ **C**(具名接缝 `tools/pre-execute`)+ **G**(机制已核,见下) |
| **影响力多大** | 星标 7、**npm 1,064 次/月**(实时采样 2026-10-31;catalog 2026-08-19 快照为 6★)——**影响力小,不可替代性高**。它是唯一把「写权」做成机制的样本 |
| **主要特点** | ① 认领与被保护文件同目录(边车),不建中央注册表 ② `tools/pre-execute` 返回 `deny`,仅覆盖 `write`/`edit`/`bash`/`pwsh`,shell 解析失败 fail-open ③ 心跳 = `agent/created`/`agent/status` 事件 + 10min 兜底定时器 ④ 冲突三条出路:活跃(force 也拒)、stale(提示接管)、孤儿(就地清扫) ⑤ 真正冲突时走 pending 三路合并(git merge-file),冲突标记直接写进工作树 |
| **代价 / 失效** | **无 fencing token** → 原主静默失锁;pid 是宿主进程粒度,同进程内死掉的会话不会被孤儿探测命中;**宿主重启后所有认领被当孤儿清**;NFS/多机远端活会话会被立即误清;guard 是 check-then-act,存在竞态;工具面外全是君子协定 |
| **证据级别** | `[OBS]` 源码全部读过(`claim.mjs` / `index.mjs`);`inject` 只有 `['tools']`,无 fs 钩子、无 `ctx.provide` |

### 标杆 B · `omdsh-dev/dsh_workflow`(第三笔税的极限:快照重跑)

| 必答项 | 内容 |
|---|---|
| **代表什么典型** | 边界 1(同进程父子)的**失败收敛**,以及「没有 DAG 也能编排」这条路 |
| **为什么选它** | 过 **C**(服务键 `dynamicWorkflows`,自报接缝)+ **D**(6 项能力披露)+ **G**(机制已核) |
| **影响力多大** | 星标 **153**(实时,2026-10-31),catalog 内 82(2026-08-19);`workflow` 类。两个半月涨了 1.9 倍——**本域里增长最快的非头部样本** |
| **主要特点** | ① **没有 DAG/step/node/edge**,JS 的 `run(wf,args)` 控制流就是编排,每个 `runAgent` = 一个新的 DSH 子代理 ② 治理三层:静态正则 13 类禁用 + QuickJS/WASM 独立堆双保险;胶囊字段精确白名单;三级信任 ③ 部署级共享并发信号量与 token 开工前预留后对账 ④ 明说不替换原生 `ctx.workflows` |
| **代价 / 失效** | 「可恢复」= 从不可变快照**整体重跑** + 内容键缓存回放,不是断点续跑;进程重启后活跃 run 丢失;`minDshVersion` 只存不比较;多进程共用绝对 runDirectory 无锁 |
| **证据级别** | `[OBS]` 源码读过(`engine.ts` / `store.ts` / `service.ts`);`[doc]` README 与 `KODAX_PARITY.md` |

## 5.5 实现配方：三笔税各自的最优交法(可直接落地)

前面是「有哪些交法」,这一节是「选哪一种、按什么顺序写」。每条配方都给出**在 DSH 上用什么接缝、必须补什么、不补会怎样**。

### 配方 A · 状态归属:会话日志权威 + 盘上视图(不是反过来)

```text
权威:会话事件流(宿主已持久化、可重放)
      └─ 派生:磁盘 <ws>/.<plugin>/<teamId>/state.json  ← 只读视图,给面板与跨会话查询用
锁    :单写者。同一 workspace 只允许一个宿主进程持有写权(用 workspace 级独占文件,不是进程内 promise)
```

**为什么这么选**:官方 `dsh-experimental-agent-team` 的设计前提是「持久日志、派生状态」——日志权威才换来重放与并发安全。生态里把磁盘升成真相源的(`agent-teams`/`teams-x`)都付出了同一笔代价:**锁只能做到进程内,多进程即覆盖写**(`second-process-lost-update`)。

**如果你偏要磁盘权威**(为了面板直读、为了不与会话日志耦合),那你必须同时做三件事,少一件都会出事:

1. **workspace 级独占**:不是一个进程内 promise 链,而是一个 `open(write.lock,'wx')` 或等价的跨进程互斥;
2. **整文件原子替换**:`tmp` 写入 + `rename`,只保证「不出现半截文件」,不保证「不丢更新」;
3. **不要声称多进程安全**。`agent-teams` 的 `docs/usage.md` 明写「多进程同时操作同一团队不保证一致」——这是诚实,不是缺陷。**把做不到的写出来,比假装有锁更可信。**

### 配方 B · 冲突裁决:建议 → 审计 → 拦截,三段都要有对应产物

```text
第 1 段 建议 : 在任务/成员上声明 writeScopes。它只产生 warning,永不阻断。目的是让人和模型「先谈」
第 2 段 审计 : 任务完成时比 changedPaths 与 writeScopes,越界报警或打回。事后,但便宜
第 3 段 拦截 : ctx.on('tools/pre-execute') → 命中他人认领则返回 { kind: 'deny', ... }
              只对真正会写的工具挂:write / edit / bash / pwsh
              必须显式列出:哪些写路径不在你的钩子覆盖面内(shell 拼接、格式化器、外部写入)
```

**为什么必须是三段而不是一段**:第 1 段给模型一个不改错的机会(零成本);第 2 段保证事后可追;第 3 段才是兜底。只有第 3 段的设计会因为 `deny` 太硬而误伤(比如 `bash` 里的只读命令)。

**拦截段必须自带 fencing**,这是 `file-claim` 的未完成项。最小实现:

```text
认领边车 { path, holder, epoch, startedAt, lastSeenAt, pid }
取得 : epoch = 现存最大 epoch + 1;写边车(原子替换)
续租 : 心跳时**带自己的 epoch 去写**;写入失败/发现 epoch 变大 → 立即停止写并上报「我已失锁」
守卫 : 拦写时比对 epoch。epoch 不匹配 → deny,并告知当前持有者
```

差别在于:**没有 epoch,被接管的原主要等到下一次写入被拒才知道自己输了**(`file-claim` 就是这样);**有 epoch,原主在续租那一刻就知道**,能主动收敛。

### 配方 C · 失败收敛:判据 → 检测 → 动作,三层分开写

```text
判据(最重要):ok = 未超时 && 未中断 && !hadError
              hadError 来自监听 agent/error
              绝不用「没超时」当成功(D: dsh-remote-agent 的 agent-false-success)

检测:三档并存,各管一段
      ① 事件驱动:idle / created / status 边沿 —— 毫秒级,最省
      ② 对账器:定时扫盘,回收搁浅任务 —— 分钟级,兜网络与进程边界
      ③ TTL 兜底:wall-clock 过期 —— 小时级,兜一切漏网

动作:回池(可重试)/ 冷恢复(用保留的 childId 续聊)/ 交人(升级为一等公民)
```

**为什么三层都要有**:事件驱动最灵但跨不过进程边界;对账器能跨边界但有延迟;TTL 兜一切但会误杀长任务。`teams-x` 只做①+② 所以明写「无心跳、无硬超时」;**只做③就会误杀**(`dsh-expert-mode` 的 `stale > 300s → ready` 没有存活探测,跑得久的专家会被当崩溃回滚)。

**「交人」要当一等公民而不是异常**:`dsh-takeover` 在投递失败时把同一份指令复制到剪贴板 + 原因横幅。人是最可靠的后备,前提是你给了他足够的信息去做决定。

### 三笔税的依赖顺序(别搞反)

```
先定状态归属 ──→ 再定冲突裁决 ──→ 最后定失败收敛
```

理由:**裁决要有认领记录可依,收敛要有状态可回**。反过来做——先写一个漂亮的崩溃恢复,再发现状态存在两个地方——你会把恢复逻辑重写一遍。生态里 `agent-team` 就是这个顺序反了的结果:schema 先写了 `leases` 与 `dependencyIds`,代码却从没跟上,留下两张空表。

## 6. 体验

**人看到的**:三笔税在人这一侧几乎不可见,只在出事时暴露成不同形状——

- 状态归属选错 → 面板显示的和 agent 记忆的**不一样**(`agent-teams` 明写活动面板「读磁盘真相,与会话日志事件流相互独立」)
- 冲突裁决选错 → 文件被改坏,但没有一个人收到过提示
- 失败收敛选错 → 任务永远停在 `in_progress`,界面看起来一切正常

**模型看到的**:模型**看不到三笔税中的任何一笔**。它只看到工具返回值:

- 抢不到文件时看到一句 `认领失败：… 正被活跃会话占用`
- 消息没送到时看到**什么都没发生**
- 自己的 attempt 被废弃时,`agent-teams` 会在下一次 step 准入时把过期邮件丢弃——但模型只知道自己没收到邮件

> **这就是本域最不对称的地方**:三笔税全是给**宿主**交的,模型侧只承担「发现自己被拒」这一层。因此模型能配合的设计必须**把裁决结果做成工具返回值**,而 `file-claim` 的 `pre-execute` deny 恰好就是。

## 7. 失败模式

| 失败 | 表现 | 根因 | 具名条件 |
|---|---|---|---|
| 第二真相源失步 | 面板与模型记忆不一致 | 磁盘做真相源,会话日志降级为审计 | 任何多进程写同一状态目录(`second-process-lost-update`) |
| 丢失更新 | 后写覆盖先写 | 进程内锁 + 整文件 rename 写 | `agent-teams` / `file-claim` 的 `tmp+rename` 都只保证「不出现半截文件」 |
| 静默失锁 | 原主以为还持有 | 租约无 epoch/fencing | `file-claim` 被接管后原主 `mine=[]` |
| owner 永占 | 任务停在 in_progress | 模型忘调 `update_task` 即进入 parked | `parked-attempt-orphan`(`agent-teams`) |
| 空表 | schema 有租约/依赖,代码没有 | 设计先落地、实现未跟上 | `limuyang2/agent-team`:`leases` 表无代码、`dependencyIds` 硬写 `[]` |
| 假成功 | completed 但零产出 | 完成判据只看超时/中断 | `remote-agent` 的 `agent-false-success` |
| 重启归零 | 在跑的全 interrupted | 无执行级检查点 | `team-gui`(明说无自动续跑)、`dsh_workflow`(活跃 run 丢失) |
| 重复投递 | 同一条消息被处理两次 | 无消息级幂等 | `dsh-interconnect`(`reqId` 仅关联)、`teams-x`(无 message-id 幂等) |

## 8. 评估清单

1. **权威状态写在哪张纸上?** 会话日志、磁盘、storageDomain、broker、同步盘——五选一,说清“另一份是审计还是真相”。
2. **它的锁是哪种锁?** 进程内 / 文件锁 / 租约 / CAS / 检出目录。有没有 **fencing token（epoch）**?没有的话,它能保证什么、不能保证什么?
3. **冲突被拦在哪个位置?** 提示词、工具返回、`pre-execute` deny、还是物理隔离。只有后两者能阻止写入。
4. **崩溃后靠什么收敛?** 心跳、对账器、租约过期、快照重跑,还是人的手动操作。
5. **“可恢复”具体恢复的是什么?** 状态(断点)还是答案(缓存)?两者在副作用上完全不同。
6. **完成判据是自述还是证据?** 自述的判据一定会在某个版本上产出假成功。
7. **消息有没有幂等键?** 没有幂等的重试通道,重投就是重复执行。
8. **进程重启会发生什么?** 若答案是「全部 interrupted」,那它就只是有持久记录,不是可恢复。

## 9. 开放问题

- [ ] `[OPEN]` 磁盘自有真相源 vs 宿主日志派生:哪一个是长期正解?前者换来面板可观测性,后者换来重放与并发安全,目前没有插件同时拿到两者。
- [ ] `[OPEN]` 为什么生态里没有一个样本给自己的租约加 **epoch/fencing**?是成本问题,还是宿主没给「拒绝写」的通用钩子（只有 `tools/pre-execute`,而 shell 一绕就没）?
- [ ] `[OPEN]` `limuyang2/agent-team` 的「schema 有、代码无」(leases/dependencyIds)是个案,还是生态里“设计先行、实现未跟上”的普遍现象?需要更大样本的盘点。
- [ ] `[OPEN]` 若官方把 Agent Teams 的成员配置（每成员模型/权限/技能包）补上,三家自建 roster 的存在理由还剩几条?
