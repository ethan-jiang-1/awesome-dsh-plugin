# dsh-superagent-trace — 只许读一张库:把黑箱摊成时序图,代价是钉死内部表结构

> `luckyxiang6688/dsh-superagent-trace@5d6feab`(0★,MIT,已发 npm `0.1.1`)。上游 `deepseek-ai/dsh-superagent-prototype@8c32a9dc`(24,565★)。注册表条目 [`luckyxiang6688__dsh-superagent-trace.yml`](../../../data/plugins/luckyxiang6688__dsh-superagent-trace.yml),类目 dev。证据等级 ★★★:读全 `src/`(41 个文件 / 8,978 行 TS/TSX)、26 个测试文件、`cordis.patch.yml` 与 README 全篇;**没有**拿一份真实 `orchestrator.sqlite` 装起来跑面板。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 / 类目 | luckyxiang6688/dsh-superagent-trace / **dev** |
| 自述 | "把 Super-agent 处理一条消息的全过程,展开成一张读得懂的时序图";明确"不是运维监控,也不是统计报表"(`README:3-7`) |
| 声量 | 0★(2026-11-25 实时值) |
| 包形态 | 单个 DSH 插件,宿主侧 `lib/index.js` + 客户端 `lib/client.js`;`cordis.patch.yml` 只有 `insert`,**不带任何 config**(包内 patch 不能写死绝对路径) |
| 宿主钉版 | `engines.dsh >=0.2.1-rc.0 <0.3.0`;Node `^22.19 \|\| >=24`(`package.json`);读库用 `node:sqlite` 的 `DatabaseSync` |
| 代码规模 | `src/` 41 文件 / 8,978 行;`domain`+`presenter` 不 import 任何 DSH 的东西(`README:142,212-218`) |
| 上游私有契约 | 只有 `src/adapter/superagent/db.ts`(481 行)含 SQL;其余代码只见 domain 类型(`db.ts:1-4`) |
| 读什么 | `orchestrator.sqlite`(**readOnly**)+ 会话日志 + `orchestrator` 服务的来源清单(`index.ts:30`) |
| 写什么 | 什么都不写:不改上游数据、不写宿主配置、不发遥测(`README:170`) |
| 对外接口 | `/agent-trace/*` 11 条路由,除 `translate` 外只允许 GET,同源校验(`routes.ts:57-92`) |
| 复现 | `git clone … && git checkout 5d6feab`;`node --test tests/*.test.ts`(作者记 269/269,`README:206`) |

## 影响力

- **0★ / 0 fork / 0 issue / 0 watcher**(GitHub API,2026-11-26 取);2026-11-09 建仓,最后一次 push **2026-11-13**——与 `0.1.1` 同日,之后再无提交。
- 注册表位置:[`data/plugins/luckyxiang6688__dsh-superagent-trace.yml`](../../../data/plugins/luckyxiang6688__dsh-superagent-trace.yml),类目 `dev`。
- npm **已发布**:`dsh-superagent-trace@0.1.1`(历史版本另有 `0.0.0-stage`、`0.1.0`),包创建于 2026-11-13;近 30 天窗口下载 **854** 次(npm downloads API;包只发布了 11 天,数字含镜像/CI,**不等于安装数**)。
- 判断:**社区影响力 = 小**。零 fork、零 issue 意味着没有公开反馈回路;但"已发 npm + bundle patch 自动挂载"让试装成本接近一条命令(`README:45-51`),854 次下载只说明它被**下载过**;是否真装进 profile,公开数据无法区分。
- **依赖面**:`package.json` 里没有任何 `@deepseek-ai/*` 依赖,只在运行时按服务名 `inject`(`index.ts:30`),也没有一行上游代码——与上游的关系是纯契约,不是分叉。
- 横向看:D1 的 HiSeax 138★、local 11★,D2 三条全是 0★。这一层的共同点是**没有分发叙事,只有功能**;它是三条里唯一把"解释"当成产品概念的。

## 一、要解决什么问题:上游只留"当前态",没留"因果链"

一条消息在 Super-agent 里的轨迹被劈成三处,而这三处**没有一处**是给人回看的(`README:17`):

1. `orchestrator.sqlite` —— 工单、裁定、去向、线程,全在 `value` 列的 JSON 里,表只负责主键与时间索引(`上游 src/app/store.ts:72-77`);
2. 按会话存放的日志 —— 模型请求、工具调用、想法,多帧 zstd,只能走宿主的 `sessionQuery` 读(`README:144`);
3. 宿主内存态 —— 正在跑什么、来源装没装、标题叫什么。

上游自己的面板(管理页)回答的是"现在怎么样":工单列表、健康、设置。用户要的是"我那句'修一下登录页'为什么没成单"——这需要把 Trigger→Disposition→Decision→Ticket→Assignment→Outbox 串成一条按真实时间排序的线。上游不存 stage(现算,`上游 src/core/stage.ts:9-21` 与 `docs/003-execution.md` 的阶段表)、不存评估开始时刻、按事件 id 去重时**直接返回不写行**,这三件事决定了"回看"必然有洞。

所以缺口不是"缺一个图表",而是:**域内只保证幂等与一致,不保证可解释**。

## 二、路径:当读者 —— 不改内核、不分叉、不回写

三条被放弃的路,理由都能从代码里读出来:

- **不分叉**:上游 92 个源文件、`private: true`、无 npm 包;为了一块面板扛一份整树,等于把 D1 分叉的同步债换一块 UI,不划算。
- **不给上游提补丁**:上游 issues/PR 关闭(adapt 的 README 自述,见 [../impact.md](../impact.md) 的"待验证"一节),且面板属"部署面",上游文档明确把 Channel/Executor/面板内容都归部署(`上游 docs/001-domain.md:64-71`)。
- **不自己采集**:不建索引、不埋点、不轮询(`README:31`),因为一旦采集就要和上游抢写权,也就不再是"只读"。

它选的是第四条:**把上游的运行事实当只读输入,把自己的解释层叠在上面**,并且把"解释"与"事实"在界面上分成两段(`README:22,110-117`)。这条路的前提只有一个:能拿到 `stateDir`。

于是 `stateDir` 的解析顺序被写成三档,**第二档不是兜底而是正确缺省**(`index.ts:34-58`):

```
显式 config.stateDir  →  orchestrator.machine.stateDir  →  都没有(origin: 'none')
```

理由写在注释里:bundle 自动挂载的用户不会读 README 第 3 步,而包内 patch 不能写死绝对路径;没有第二档,插件在默认安装下会"静默什么都不做"(`index.ts:38-43`)。

## 三、它如何利用 dsh-superagent(逐点对位)

| 用途 | 上游落点 | 本仓落点 |
|------|----------|----------|
| `orchestrator` 服务本身 | `Runtime extends Service`,`super(ctx,'orchestrator')`(`上游 src/app/runtime.ts:88`) | `inject = ['orchestrator','sessionQuery','webServer','llm']`(`index.ts:30`) |
| `machine.stateDir` | `Machine.stateDir`(`上游 src/deployment.ts:16-17`),库路径 `join(machine.stateDir,'orchestrator.sqlite')`(`runtime.ts:98`) | `resolveStateDir`(`index.ts:44-58`);**继承值不 trim**(`index.ts:52-56`) |
| 六张表 + kv | `trigger/disposition/thread/ticket/decision/outbox/kv`(`上游 store.ts:72-77`) | `SqliteStore`(`db.ts:267-324`) |
| `trigger.at` 真实列 | `trigger(id, value, at)`(`store.ts:72`) | 分页游标按 `at`+`id` 排序(`db.ts:380-391`) |
| 主控会话 id | `KV.runtime.masterId = 'master-id'`(`上游 src/kv.ts:33`) | `kv('master-id')`(`db.ts:26-27,444-450`) |
| 策略快照 | `KV.settings.version = 'settings-version:<rev>'`(`kv.ts:25-27`;结构 `SettingsVersion`,`store.ts:22-25`) | 按 revision 从新到旧读,坏行跳过(`db.ts:417-432`) |
| 线程显示名 | `KV.sources.labels = 'source-labels:<source>'`(`kv.ts:39-40`) | `sourceLabels`(`db.ts:434-442`) |
| 阶段派生 | `ticketStage` 首行命中(`上游 src/core/stage.ts:9-21`) | **复刻同一顺序**(`src/adapter/superagent/stage.ts:49-64`),连"人跟进过就不再算等人"也照抄(`:70-84`) |
| 理由码 | `REASONS` 表(`上游 src/core/reasons.ts:3-27`) | 一张中文译名表,查不到就写"不在解释表里"(`src/service/explain.ts:38-58`) |
| 执行器会话 id | `worker-<ticketId>`(`上游 src/executor/dsh.ts:23-24`) | `workerSessionId`(`src/domain/session.ts:8`) |
| 工具名(画箭头) | `orchestrator_ack`(`tools/executor.ts:29`)、`orchestrator_reply`(`tools/main.ts:224`)、`orchestrator_eval`/`_decide`(`tools/main.ts:203,215`) | `src/service/reader.ts:525-545`、`src/service/thoughts.ts:11` |
| 来源清单/标题 | `SourceRegistry.instances()/kind(id)`(`上游 src/sources/registry.ts:43,45-50`) | 通过服务读,失败返回 `[]` 不编造(`index.ts:76-99`) |
| 会话日志 | 宿主 `sessionQuery`;多帧 zstd,直读只解第一帧 | `events.ts:9-12,60-72`;自备切帧解码(`zstd.ts:1-68`) |

三点值得单独记住:

- **所有 SQL 只在一个文件里**。这是作者对"内部形状会变"的工程回答:把爆炸半径收进 481 行,上层只见 `domain/*`(465 行纯类型)。
- **它复刻的不只是表,还有规则**。`stage.ts` 是上游 `core/stage.ts` 的逐行移植;`explain.ts` 是 `reasons.ts` 的译名表。表可以加列,规则一改就是**语义漂移**,而且不报错。
- **服务只用来补"库外事实"**:来源标题、装没装(`installed`)、启没启(`enabled`)只有注册表知道,库里只有 source id(`index.ts:74-75`)。

## 四、技术思考

### 4.1 只读的三道闸

1. **连接级**:`new DatabaseSync(path, { readOnly: true })`(`db.ts:267`),打开失败返回 `undefined` 由调用方降级(`db.ts:8-14`)——注意这条路径**没有异常出口**,读错目录与读不到库都表现为"没有数据"。
2. **查询级**:分页 SQL 用 `json_valid()` 兜底,因为 `json_extract` 碰到坏 JSON 会抛,一行坏数据能让整次查询失败(`db.ts:277-286`);`rows()` 逐行 `JSON.parse` 失败即跳过(`db.ts:466-474`)。
3. **宿主级**:路由只 `register` 前缀 handler,同源校验 + GET-only + 未配置时统一 503 并带 `hint`(`routes.ts:68-81`);异常只回 `error.message` 前 200 字(`routes.ts:163-166`);诊断日志**默认不写**,要显式 `DSH_AGENT_TRACE_LOG`(`index.ts:21-27`)。

一个细节见功力:**继承来的 `stateDir` 不 trim**(`index.ts:52-56`,单测 `tests/state-dir.test.ts:47-54`)。上游用 `join(machine.stateDir,'orchestrator.sqlite')` 拼路径,若插件 trim 掉尾随空格,两边指向不同目录,而只读打开失败只会显示"没有数据"——"读错目录"比"读不到"更危险。

### 4.2 内部形状:绑死的到底是什么

不是"表名"这一层。真正绑死的是四样东西:

1. 表的**存在与列**(`trigger.at`、`disposition.id = trigger.id`);
2. `value` 里的 **JSON 路径**(`$.origin.triggerId`;`assignments[#-1].state` 上游用生成列算,插件在 JS 里重算同一件事,`上游 store.ts:36-42`);
3. **kv 键的命名族**(`settings-version:`、`source-labels:`、`master-id`);
4. **派生规则**(stage 顺序、理由码集合)。

前两样坏了会读空,第三样坏了会少一列解释,第四样坏了**会画错**——页面照常渲染,只是状态带与"为什么没接"变成另一套意思。这是本插件最脆的一环,而它对上游的版本信号**一个都没用**:全仓没有读 `kv['schema']`(`上游 src/kv.ts:23`),也没有读 `SCHEMA_VERSION`。上游自己会拒绝未知版本(`上游 store.ts:67-69`)、迁移 10→11(`migration.ts`),插件不会。

### 4.3 失败时的表现:把"不知道"画在屏幕上

这是它最像"给人看"而不是"给机器看"的地方:

- 取不到 `stateDir` → 页面说明原因并给下一步,而不是空数据(`index.ts:130-133`,`README:89`);
- 上游没记的 → 单列"没记录的事实",逐条声明:去重不留痕、`filtered` 只落原因码不落设置快照、评估开始时刻未落库(`README:187-189`);
- 解释表里没有的码 → 不推测,写"不在解释表里"(`explain.ts:1-5`);
- 采集侧吞异常、展示侧三层错误边界(面板根、覆盖层、抽屉),一处画不出不影响其它(`README:146`);
- 健康接口只记计数与耗时,不记路径参数与正文(`service/health.ts:10`),且**每次探测都在 `finally` 里关句柄**——`/health` 是故障时被高频轮询的接口,漏一个句柄就会攒满 fd(`health.ts:33-54`)。

性能上它做的是"点开才算":打开面板 3 个请求,点开工单只多 1 个,列表响应实测 618 B 且服务端不为列表读会话日志(`README:145`)。

## 界面体验

- **入口**:侧栏一个条目"来源与工单"(`client/mount.tsx:13-14,61-66`;`sidebar.panellist`、order 10、16×16 SVG 图标),主区一个面板(`main` slot,`mount.tsx:58-59`)。
- **落地页**:左右分栏,分隔条比例存 localStorage(`client/split.ts:7`,`SourcePage.tsx:40,201`)。左栏"来源(按最近活跃排序,空来源置灰)+ 工单",主区"去向比例带(图例可点筛选)+ 事件流(倒序、游标分页)"(`README:95-106`)。
- **点事件**:右侧抽屉固定四段——事实 / 为什么这样去(明确标注"解释")/ 没记录的事实 / 原文与关联工单(`README:110-117`,`client/EventDrawer.tsx`)。
- **点工单**:覆盖层泳道图,来源、主控(Router)、执行器(Worker)各一列,评估块、派工块、状态背景带、知会/回复箭头、子代理按需加列;顶部"← 返回来源"+面包屑(`README:119-128`,`TicketOverlay.tsx`、`TicketView.tsx`、`presenter/swimlane.ts`)。
- **信息密度**:一屏能读完一条工单的来龙去脉;但 1200 px 内 500 节点会压成一列、标签互相压住(`README:186`),暗色主题未做。
- **失败时看到什么**:未配置 → 一句原因 + 下一步(加 `config.stateDir`)(`index.ts:130-133`);渲染抛错 → 面板级兜底"页面渲染出错"+`error.message` 前 200 字 + "切走再切回可重试"(`client/mount.tsx:49-55`);采集侧吞异常,一层崩不影响其它层(`README:146`)。
- **键盘**:Esc 只挂一个监听器、一个栈,"最后打开的先关",并在 capture 阶段 `stopPropagation`,避免顺带关掉宿主面板(`client/escape.ts:1-26`)。

## 用户交互的思路

- **谁发起**:这条线不向 Super-agent 发起任何工作——它是**纯回看**,所有动作都发生在上游完成之后(`README:29-31`)。
- **在哪确认**:确认的不是"要不要做",而是"到底发生了什么"。抽屉把库里的事实与查表得到的解释分开,让用户自己判断解释是否成立(`README:22`)。
- **怎么观察**:打开面板取一次快照(3 个请求),点开工单只多 1 个;不轮询、不推送(`README:145,191`)。要看"现在"仍回上游管理页。
- **怎么打断**:不打断。它是只读视图,没有取消/重试/停止入口;要动工单只能去上游面板,或在原渠道回一句话。
- **它唯一的写操作**:可选的 `POST /agent-trace/translate`(`routes.ts:82-91`),只影响显示文本,不落库、不改上游状态。
- **与上游回路的差异**:上游的用户回路是"消息 → 回执 → 结果回原对话"的闭环;本页把这个闭环**摊平成可审计的时间线**,但不参与它。代价是永远慢一拍,且上游没记的部分(去重、过滤快照、评估起点)只能声明"没记录"(`README:187-189`)。

## 五、代价与边界

1. **内部 DB 当 API**。上游改表/改 JSON 路径/改 kv 族名,trace 的表现是"页面正常、数据为空"或某列解释消失,而不是启动失败。作者的对策是**措辞**,不是检测。
2. **派生规则的第二重绑定**。`stage.ts` 与 `explain.ts` 是上游语义的副本;上游一改判据,错的是"状态带"和"为什么不接",而且**错得很安静**。
3. **日志协议也是私约**。多帧 zstd 直读只解第一帧(`zstd.ts:1-7`),箭头依赖 `orchestrator_ack`/`orchestrator_reply` 真的出现在日志里,且来源有回复通道,缺一就不画(`README:190`)。
4. **只读 = 不能补洞**。去重不留痕、过滤无设置快照、评估起止是近似——这些是上游不写,读者无权补(写了就破坏"事实/解释"分界)。
5. **只做事后快照**。打开时取一次,不轮询、不告警(`README:29-30,191`);"现在有没有卡住"仍要回上游面板。
6. **宿主门槛不低**:`<0.3.0` 的区间声明 + `node:sqlite`(Node 22.19/24);桌面端未验证(`README:193`)。
7. **画布边界**:1200 px 内 500 节点会纵向叠成一列(`README:186`);暗色主题未做。
8. **改名残留**:装过改名前的 `dsh-agent-trace` 会出现两个面板(`README:67-68`)——同一个插件 id 只挂一次,不同 id 就是两个。

## 可信度与复现

- **读过**:`README.md` 全篇、`src/` 41 个文件、`tests/state-dir.test.ts`、`tests/sources.test.ts` 等 26 个测试文件、`cordis.patch.yml`、`package.json`;上游 `docs/001-domain.md`、`docs/003-execution.md`、`src/app/store.ts`、`src/app/runtime.ts`、`src/core/stage.ts`、`src/core/reasons.ts`、`src/kv.ts`、`src/sources/kind.ts`、`src/sources/registry.ts`。
- **对位比过**:表名逐张、kv 键逐个、stage 判据逐行、工具名逐处。
- **没做**:真实 `orchestrator.sqlite` 上跑面板;500 节点性能;`node --test`;npm 安装链路。
- **复现**:
  ```sh
  git clone https://github.com/luckyxiang6688/dsh-superagent-trace && cd dsh-superagent-trace
  git checkout 5d6feab
  grep -rn "readOnly\|orchestrator.sqlite" src/adapter/superagent/db.ts
  diff <(sed -n '9,21p' ../dsh-superagent/src/core/stage.ts) <(sed -n '49,64p' src/adapter/superagent/stage.ts)
  ```

## 待验证

1. **上游换形状后的真实表现**:把 `trigger.at` 列改名、或把 `settings-version:` 换族,插件是否仍"页面正常、数据为空"?没有负向测试,只有 `json_valid` 兜底。
2. **WAL 下的只读共享**:上游开 `PRAGMA journal_mode=WAL`(`store.ts:64`),只读连接仍需访问 `-wal`/`-shm`;同用户下成立,跨用户或只读挂载是否可读未实测。
3. **与 D1 分叉共存**:HiSeax 把服务/id 改成 `dsh-windows-superagent-*`;trace 的 `inject: ['orchestrator']` 是否能挂到它上面,未验证。
4. **`translate` 的模型成本**:配了才调,每次 ≤5 条 ≤1200 字(`routes.ts:82-91`),但没有成本上限说明。
5. **同源校验的实际强度**:无 `Origin` 头或 `webServer.port` 未知时直接放行(`routes.ts:194-203`),本机任意进程可读该 API;因为只读,风险被"只读"吸收,但不是鉴权。
