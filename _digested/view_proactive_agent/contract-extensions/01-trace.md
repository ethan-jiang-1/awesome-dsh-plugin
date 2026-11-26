---
kind: card
domain: proactive_agent
subcategory: contract-extensions
repo: luckyxiang6688/dsh-superagent-trace
commit: 5d6feab72868eb9caa6c93b7fd28f9721033424c
evidence: 3
status: active
asof: 2026-11-25
---

# superagent-trace — 只读一张库，把 Super-agent 的黑箱摊成泳道图

> 证据等级 ★★★：`luckyxiang6688/dsh-superagent-trace@5d6feab72868eb9caa6c93b7fd28f9721033424c`(2026-11-13，`0.1.1`)。读了 `README.md`、`package.json`、`cordis.patch.yml`，以及 `src/` 的 `index.ts`、`adapter/superagent/{db,stage}.ts`、`service/{routes,explain,reader,health,thoughts}.ts`、`adapter/session/zstd.ts`、`presenter/swimlane.ts`（头部）、`client/mount.tsx`；其余文件只按目录与行数统计。并与上游 `deepseek-ai/dsh-superagent-prototype@8c32a9dc` 的 `src/app/store.ts`、`src/kv.ts`、`src/core/stage.ts`、`src/deployment.ts` 逐点对位。**没有**装进 profile 跑，也没有拿一份真实 `orchestrator.sqlite` 验过面板。

## 它替谁解决什么问题

**角色**：已经装了一个 `superagent` profile 的维护者或值班者——不是插件作者,而是那个被问「这条消息怎么没接」的人;也包括要给团队写接入说明、需要一个能直接指给人看的界面的人。

**场景**：某条 GitHub / 飞书消息进来后结果不对——没成单、成了单没人干、干到一半停住。要回答的是三个具体问题:为什么没接这条、为什么建了这张工单、现在卡在谁那里。

**现有笨办法**：三处各看一半。`orchestrator.sqlite` 只有主键、`value` 的 JSON 和时间索引;会话日志是多帧 zstd,得走 `sessionQuery`;来源装没装、标题叫什么只在宿主内存里。手上同时有 `sqlite3` 和日志,也拼不出时间线。

**为什么拼不出**：stage 不落库、每次现算;评估开始时刻压根没记录;按事件 id 去重时直接返回、不写行。这三件事决定了手工回看必然有洞,而且洞的位置不固定。

**为什么现在需要**：上游把「当前态」保证得很严(幂等、一致、拒绝未知 schema),但没有一处是给人回看的;管理页回答「现在怎么样」,不回答「为什么」。这套东西一旦跑起来,「能跑,但说不清」就会变成日常问题。

**判断**：对这条线来说,「能解释」不是锦上添花——没有它,值班只能靠重放一遍或猜。

## 适用面:谁该用、谁别用

- **适合**：已经跑着 `dsh-superagent`、并且能拿到 `stateDir` 的 profile;DSH `>=0.2.1-rc.0 <0.3.0`、Node 22.19/24。
- **适合**：想「回看」而不是「操作」的人——维护者、值班者、写接入文档的人。
- **不适合**：想取消/重试/改工单/补数据的人。全插件只读,唯一非 GET 入口是显示层翻译;要动工单去上游面板,或回原渠道说一句话。
- **不适合**：要实时告警或监控的人。页面打开时取一次快照,不轮询、不推送;「现在有没有卡住」仍要看上游管理页。
- **不适合**：想读别的来源数据的人。它只认 `orchestrator.sqlite` 的 6 张表与 3 个 kv 键族,换个库名或表名就读不到。
- **前置**：`stateDir` 能解析(显式 `config.stateDir` 或 `orchestrator.machine.stateDir`);库在 `stateDir/orchestrator.sqlite`;同用户可读(WAL 还要能读 `-wal`/`-shm`)。
- **注意**：web 端已验证,桌面端未验证;装过改名前的 `dsh-agent-trace` 会多出一个面板。
- **一句话**：它把「回看」做成一屏,但不接管「操作」——两者的边界就是只读。

## 业务价值

**能算清的**：

- 三处散落信息收成一屏:来源页(收/丢/成单)+ 事件抽屉 + 工单泳道;打开面板 3 个请求,点开工单只多 1 个(`README:145`)。
- 只读零写入:除可选的显示层翻译外全是 GET;不改上游数据、不写宿主配置、不发遥测。
- 分发面:近 30 天(2026-10-26–11-24)下载 854(含镜像/CI);0★/0 fork/0 issue(2026-11-26 取)——有人下载,没人公开反馈。
- 爆炸半径:8,978 行里只有 481 行含 SQL(`db.ts`),上游换形状时改动面可控。

**只是预期(推断,无数据)**：

- 缩短「为什么没接」的排查时间:三次手工查询压成一次点开,但没有 before/after 计时。
- 降低新人读内部库的门槛:事实与解释分栏,但没做过用户测试。

不吹 ROI:没有团队采用数据,也没有节省工时的度量;854 次下载只证明它被下载过。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 / 类目 | `luckyxiang6688/dsh-superagent-trace` / **dev**([registry](../../../data/plugins/luckyxiang6688__dsh-superagent-trace.yml)) |
| 层 | **D2 contract-extensions**：零上游代码、零 `@deepseek-ai/*` 依赖，只按服务名 `inject` |
| 自述 | 「把 Super-agent 处理一条消息的全过程，展开成一张读得懂的时序图」；明确「不是运维监控，也不是统计报表」(`README:3-7`) |
| 声量 ⚠ | **0★ / 0 fork / 0 open issue / 0 watcher**(GitHub API，2026-11-26 取)；建仓 2026-11-09，最后 push 2026-11-13 |
| 包形态 | npm `dsh-superagent-trace@0.1.1`(2026-11-13)，历史版本 `0.0.0-stage`、`0.1.0`；单包：宿主侧 `lib/index.js`、客户端 `lib/client.js` |
| 下载 ⚠ | 近 30 天 **854**(npm downloads API，2026-10-26–11-24)；包只发布了 13 天，**含镜像/CI，不等于安装数** |
| 宿主钉版 | `engines.dsh >=0.2.1-rc.0 <0.3.0`、node `^22.19 \|\| >=24`；读库用 `node:sqlite` 的 `DatabaseSync`(`package.json`) |
| 代码规模 | `src/` **41 文件 / 8,978 行** TS/TSX；`tests/` 26 个 `*.test.ts`；`client/` 15 个文件 |
| 读什么 | `orchestrator.sqlite`(**readOnly**)+ `sessionQuery` 会话日志 + `orchestrator` 服务的来源清单(`src/index.ts:30,76-99`) |
| 写什么 | 什么都不写。唯一非 GET 入口是可选的 `POST /agent-trace/translate`，只影响显示文本(`src/service/routes.ts:82`) |
| 界面 / 交互 | 侧栏**「来源与工单」**+ 主区面板；点开工单是主控/执行器**泳道时间线**；纯事后回看，**不能打断**（没有取消/重试/停止入口） |
| 契约面 | **6 张表 + 3 个 kv 键族 + 2 套派生规则**(stage 顺序、理由码集合) |
| commit | `5d6feab72868eb9caa6c93b7fd28f9721033424c`，2026-11-13，`fix(sidebar): 图标改成 16×16 SVG…;发 0.1.1` |

## 它到底是什么

**是一层解释，不是监控，也不是采集器。** 上游只保证幂等与一致，**不保证可解释**：表里只有主键、`value` 与时间索引；阶段不落库、现算；按事件 id 去重时不写行。于是「我那句『修一下登录页』为什么没成单」在库里根本拼不出来。这个插件做的就是**把现有事实按真实时间重排一遍**，再把「查表得到的解释」叠在上面。

代码分成五段，依赖方向单向：`adapter`(SQL)→ `domain`（纯类型）→ `service`(reader/explain/coverage)→ `presenter`（纯函数坐标）→ `client`(React)。`domain` 与 `presenter` 不 import 任何 DSH 的东西——所以泳道布局能被单测完整覆盖(`src/presenter/swimlane.ts:1-5`)。

它守的三道闸都在「读」这一侧：

1. **连接级**：`new DatabaseSync(…, { readOnly: true })`(`db.ts:267`)，打开失败返回 `undefined` 由调用方降级(`db.ts:8-14`)；
2. **查询级**：分页用 `json_valid()` 兜底，`rows()` 逐行 `JSON.parse` 失败即跳过——一行坏数据不能毁掉整次查询(`db.ts:466-474`)；
3. **宿主级**：只注册前缀 handler，除 `translate` 外只允许 GET，未配置统一 503 带 `hint`(`routes.ts:57,92`；`index.ts:128-133`)。

**事实与解释在界面上是分开的两段**：抽屉段序固定——原文 → 事实 → 解释(明确标「解释」，不是记录)→ 没记录的事实 → 线程 → 关联工单(`EventDrawer.tsx:5-10`)。解释表里没有的码不推测，明写「不在解释表里」(`explain.ts:1-5,69,91-95`)。这是它最像「给人看」而不是「给机器看」的地方。

## 怎么接进 DSH

**① manifest 是三块，不是一个字段。** `dsh.bundle.patch: ./cordis.patch.yml`、`dsh.client: { platform: "web", inject: [ui-slots, locale] }`、`engines.dsh` 区间(`package.json:20-22,35-48`)。`inject` 在这里只是客户端模块的预读元数据，不是 Cordis 服务注入。

**② patch 只有 `insert`，不带任何 config。** 理由写在文件里：包内 patch 会跟着分发到每台机器，不能携带本机绝对路径(`cordis.patch.yml:1-10`)。这条约束直接决定了下一档。

**③ `stateDir` 三档解析，第二档不是兜底而是正确缺省**(`index.ts:44-58`)：

```
显式 config.stateDir  →  orchestrator.machine.stateDir  →  都没有(origin: 'none')
```

理由是 bundle 自动挂载的用户不会读 README 第 3 步；没有第二档，插件在默认安装下会「静默什么都不做」。一个容易忽略的细节：**继承来的值不 trim**(`index.ts:55-56`)——上游用 `join(machine.stateDir,'orchestrator.sqlite')` 拼路径，trim 掉尾随空格就指向另一个目录，而 readOnly 打开失败只表现成「没有数据」。

**④ 只按名字 inject 四个服务**：`['orchestrator','sessionQuery','webServer','llm']`(`index.ts:30`)。没有依赖包，也就没有版本冲突；代价是没有类型、没有启动期校验。

**⑤ 路由前缀 `/agent-trace`**：注册一次前缀 handler(`routes.ts:29,57`)，内部 12 个 GET 读点 + 1 个可选 POST，非读方法一律 405(`:92`)。未配置时**仍然注册**：页面必须能说出「为什么是空的」，而不是给 404。

**⑥ 客户端两个 slot**：主区 `main`，侧栏 `sidebar.panellist`(id `agent-trace`、`order: 10`、label **「来源与工单」**、16×16 SVG 图标)(`mount.tsx:57-66`)。

**⑦ 它不注册工具、不写宿主配置、不发遥测。** 装法就是 `dsh plugin --profile <name> add dsh-superagent-trace`(bundle 自动挂载)，或 `link:` 源码安装。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---:|---|---|
| `src/index.ts` | 163 | 服务注入、`stateDir` 解析、路由装配、来源目录降级为空数组 | `:30,44-58,76-99,128-133` |
| `src/adapter/superagent/db.ts` | 481 | **唯一含 SQL 的文件**：readOnly 句柄、6 表读、kv、分页 | `:267,270-323,408-412,419-447` |
| `src/adapter/superagent/stage.ts` | 96 | 复刻上游 stage 判据顺序 + `waitsForPerson` | `:49-64,70-84` |
| `src/service/explain.ts` | 99 | 理由码译名表；查不到 → `NOT_IN_TABLE` | `:38-69,91-95` |
| `src/service/reader.ts` | 820 | 组装 chain、分页、`master-id` 指针 | `:461` |
| `src/adapter/session/zstd.ts` | 73 | 多帧 zstd 切帧解码 | `:1-7` |
| `src/service/thoughts.ts` | 61 | 评估前最近一条 assistant 消息 | `:1-11` |
| `src/presenter/swimlane.ts` | 944 | 纯函数：泳道、节点、箭头坐标 | `:1-50` |
| `src/client/mount.tsx` | 66 | 面板壳、面板级错误边界、两个 slot | `:57-66` |

**6 张表**(`db.ts:270-323`)：`trigger(id,value,at)`、`disposition(id = trigger.id)`、`thread(key)`、`ticket`、`decision`、`outbox`。除 `disposition` 要多取 `id` 做主键关联外，只 `select value`，JSON 在应用层解；分页游标按 `at + id` 排(`:380-391`)，因为 `trigger.at` 是真实列。

**3 个 kv 键族**：

| 键族 | 用途 | 位置 |
|---|---|---|
| `master-id` | 主控会话 id | `reader.ts:461` |
| `settings-version:<rev>` | 策略快照，按 revision 从新到旧，坏行跳过 | `db.ts:419-432` |
| `source-labels:<source>` | 线程/会话显示名 | `db.ts:435-442` |

另有一处 `settings-block-revision:source:%` 前缀，**只**用来把「配置过但已从设置里删掉」的来源补进清单(`db.ts:408-412`)——它不是第四个展示维度。

**派生规则也是契约。** `stage.ts` 按上游 `core/stage.ts` 的首行命中顺序逐条对应：结束 → 投递失败 → 待回答 → 待验收 → 受阻/失败且等人 → 排队 → 空闲 → 执行中(`:49-64`)，连「人跟进过之后就不再算等人」也照抄(`:70-84`)。理由码则是一张中文译名表(`explain.ts:38-58`)。表可以加列，**规则一改就是语义漂移，而且不报错**。

**数据流**：`orchestrator.sqlite` → `db.ts`(列名 + JSON 路径)→ `domain` → `reader`(分页 + 详情)→ `presenter`（坐标）→ `client`；会话日志走 `sessionQuery`，只在点开工单/事件时读。打开面板 3 个请求，点开工单只多 1 个(`README:145`)。

## 为什么它突出

- **它把「解释」本身当产品概念。** 同一层的大多数条目在做渠道或开关，这条回答的是「刚才到底发生了什么」。
- **0★ 但试装成本接近一条命令。** 854 次下载 / 13 天，说明的是「下载过」，不是「用起来」；bundle 自动挂载把门槛压到一次 `dsh plugin add`。
- **把爆炸半径收进 481 行。** 所有 SQL、所有表名、所有 JSON 路径只在一个文件里，上层只见 `domain/*` 的纯类型。这是对「内部形状会变」最实际的工程回答。
- **「事实 / 解释」分界可复用。** 任何拿内部库当数据源的工具都该这样：库里有的、查表得到的、上游没记的，三段分开写，读者自己判断解释是否成立。
- **失败时把「不知道」画出来。** 取不到配置就说原因与下一步；上游没记的逐条声明(去重不留痕、`filtered` 只落原因码、评估起点未落库)，不补全(`README:187-189`)。

## 代价与边界

1. **内部 DB 当 API，且拿不到版本信号。** 全 `src/` **0 处**读 `kv['schema']` 或 `SCHEMA_VERSION`；上游自己会写 `KV.store.schema`(`src/kv.ts:22-23`)并对未知版本抛错(`src/app/store.ts:64-69`)，trace 一个都没用。上游改形状后的三种表现：① 库打不开/目录不对 → 页面说明原因（有出口）；② `value` 的 JSON 路径变 → **行还在、字段空**，也就是「页面正常、数据为空」；③ 列名/表名变 → 查询抛错转 500。三种都不告警，区别只是哪一种更难看出来。
2. **派生规则是第二重绑定。** `stage.ts` 与 `explain.ts` 是上游语义的副本；上游改判据，错的是「状态带」和「为什么不接」，错得很安静。
3. **日志协议也是私约。** 多帧 zstd 直读会静默丢帧，所以插件自备切帧解码(`zstd.ts:1-7`)；「知会 / 回复」箭头依赖 `orchestrator_ack`、`orchestrator_reply` 真的出现在日志里(`reader.ts:525,544-545`)，缺一就不画。
4. **只读 = 不能补洞。** 去重不留痕、过滤无设置快照、评估起止是近似——写了就破坏「事实/解释」分界，所以只能声明。
5. **只做事后快照。** 打开时取一次，不轮询、不告警；「现在有没有卡住」仍要回上游管理页(`README:29-31`)。
6. **宿主门槛不低。** `<0.3.0` 的区间声明 + `node:sqlite`(Node 22.19/24)；桌面端未验证(`README:193`)。
7. **画布边界。** 1200 px 内 500 节点会纵向叠成一列、标签互相压住；暗色主题未做(`README:186,192`)。
8. **改名残留。** 装过改名前的 `dsh-agent-trace` 会出现两个面板——同 id 只挂一次，不同 id 就是两个(`README:67-68`)。

## 可信度与复现

- **读过**：`README.md` 全篇、`package.json`、`cordis.patch.yml`、`src/index.ts`、`src/adapter/superagent/db.ts`（全）、`stage.ts`（全）、`service/{routes,explain,reader,health,thoughts}.ts`、`adapter/session/zstd.ts`、`presenter/swimlane.ts`（头部）、`client/mount.tsx`；上游 `src/app/store.ts`、`src/kv.ts`、`src/core/stage.ts`、`src/deployment.ts`。
- **对位比过**：6 张表逐张、3 个 kv 族逐个、stage 判据逐行、失败出口逐个；`0★/0 fork/0 issue`、`854` 下载、`0.1.1` 发布日均为 2026-11-26 实时查询。
- **没做**：真实 `orchestrator.sqlite` 上跑面板；`npm install` 链路；500 节点性能；`node --test`(作者自述 269/269，`README:206`，未复跑)。
- **复现**：
  ```sh
  git clone https://github.com/luckyxiang6688/dsh-superagent-trace && cd dsh-superagent-trace
  git checkout 5d6feab
  UPSTREAM=/tmp/sa-research/upstream    # 或自行 clone dsh-superagent-prototype@8c32a9d
  grep -rn "readOnly\|json_valid" src/adapter/superagent/db.ts        # 连接级 + 查询级
  grep -rn "kv(\|settings-version:\|source-labels:" src/ | head       # 3 个键族，没有 schema
  diff <(sed -n '9,21p' "$UPSTREAM/src/core/stage.ts") <(sed -n '49,64p' src/adapter/superagent/stage.ts)
  ```

## 待验证

1. **换形状后的真实表现**：把 `trigger.at` 改名、或把 `settings-version:` 换族，插件是空字段、还是 500？仓库里只有 `json_valid` 兜底，没有负向测试。
2. **WAL 下的只读共享**：上游开 `PRAGMA journal_mode=WAL`(`src/app/store.ts:64`)，只读连接仍需访问 `-wal`/`-shm`；同用户成立，跨用户或只读挂载未实测。
3. **与 D1 分叉共存**：HiSeax 把服务/id 改成 `dsh-windows-superagent-*`，这里的 `inject: ['orchestrator']` 能否挂上去，未验证。
4. **`translate` 的成本上限**：配了才调，每次 ≤5 条 ≤1200 字(`routes.ts:82`)，但没有费用上限说明。
5. **同源校验的实际强度**：无 `Origin` 头或 `webServer.port` 未知时直接放行(`routes.ts:194-203`)，本机任意进程可读该 API；因为只读，风险被「只读」吸收，但那不是鉴权。
