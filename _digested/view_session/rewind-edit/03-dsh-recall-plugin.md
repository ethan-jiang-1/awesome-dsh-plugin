# recall-plugin — 每条用户消息落一个影子 git 标签，撤回 = 还原文件 + 官方 fork 到该消息之前的 turn 边界

> 证据等级:★★★(源码级;`limbo947/dsh-recall-plugin@d00321ec6322b7eb77fed3a27bff93d80b33803a`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 **21** 为 2026-08-19 历史采样(2026-11-18 实时 **55**);⚠ 下载 **1105** 同为该日。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `limbo947/dsh-recall-plugin`([registry](../../../data/plugins/limbo947__dsh-recall-plugin.yml)) |
| 类目/子分类 | session([census](../../ecosystem/census.py) 914 条 / 全表 11 744 条)· `rewind-edit`(回退与编辑);⚠ 星标属本插件自身,仓库只有一个包 |
| 自述 | 「消息撤回:在用户消息旁加撤回按钮,把对话历史(官方会话 fork)与项目文件(逐消息影子 git 快照)一并回退到该消息发送之前,带差异预览确认面板」 |
| 星标 ⚠ | **21**(2026-08-19 冻结采样,仓库出生第 5 天);2026-11-18 实时 **55** |
| 下载 ⚠ | **1105**(2026-08-19 采样;边车未记来源,是否 npm 周下载待验证) |
| 扩散 | **0**(口径:`grep -ril 'recall-plugin' data/plugins/` 命中 1 条 = 自身;`dsh-recall` 的另 3 条是别的仓库自己的名字,逐条判断见「为什么它突出」) |
| 仓库 commit | `d00321ec6322b7eb77fed3a27bff93d80b33803a`,2026-11-17 21:59 +0800,`fix(host): ensureGit 按 store.git 做 in-flight 去重（issue #37）`;首提交 2026-08-15,325 个提交、19 个 tag、最新 `v2.6.8` |
| 包形态 | npm `dsh-recall-plugin@2.6.8`(裸名);**Profile Bundle + 浏览器半边双面包**:`dsh.bundle.patch` + `dsh.client.platform: "web"`,`cordis.patch.yml` 一条 `insert`,`lib/` 预构建随包提交 |
| 代码规模 | `src/` **14 364 行 / 51 文件**(host 18 文件 7 580 / client 24 文件 5 480 / types 9 文件 1 304);`tests/unit`+`tests/client` 63 文件、710 个 `it(`;工作树 4.5 MB(`du -sh .` 7.3 MB 含 `.git` 2.8 MB) |

## 它到底是什么

**是一个真插件,不是配置包,也不是外部系统的适配层。** 它自带 1.4 万行代码、自造磁盘布局、自己拼 git 命令,对外部世界只要求三样东西:一个 `git` 可执行文件、一个能写的 `$DSH_HOME`、DSH 的 `sessions.fork`(以及可缺的 `workspaces.archiveSession`,缺了就少一步归档)。`package.json` 没有 `dependencies`,只有 DSH 各包的 `peerDependencies` 与可选 `react`。

**它有两个互相独立的状态权威,理解这一点才能理解它的边界:**

1. **文件侧权威在插件自己的影子 git 仓库。** 每条用户消息对应一个轻量标签 `snap-<messageId>`,指向一次孤儿提交,内容是那一刻工作区的树(`src/host/scripts.posix.ts:414-451`:清 gitlink → 同步排除表 → 容量/预算护栏 → 超大文件剔除 → 一次性 renormalize → `add -A --ignore-errors` → `write-tree` → `commit-tree` → `tag -f`)。没有 delta 记录、没有「这条消息改了哪几个文件」——**每条消息就是一棵完整的树**,去重与增量压缩交给 git 自己。
2. **会话侧权威仍在 DSH 的 append-only 日志里。插件从不改日志。** 撤回时它找「这条消息之前最近一个 `turn/end` 的 `seq`」当切点(`src/host/snapshots.ts:210-224`),把这个值作为 `atSeq` 交给官方 `sessions.fork`(`src/client/recall-node.ts:825-845`)。切点之前的 turn 被原样 seed 进子会话,这条消息及之后的一律不进;原会话随后归档(可关)。撤回不是「删历史」,是「从前缀长出新分支,把旧分支收起来」。

**粒度是消息,不是轮次。** 快照在 `user/message` 事件到达时拍(`src/host/index.ts:441-466`),即**用户按下发送之后、agent 碰文件之前**。所以「撤回第 N 条」的目标 = 那条消息发出前一刻的字节;被丢掉的是该条之后整轮 agent 的全部文件改动,而不是「上一轮结束时」——agent 中途改过文件时这两个点并不相同。反过来一轮之内没有任何中间锚点,回不到「agent 做到第 3 步」的现场。标签在回退后**故意保留**(`recall-node.ts:908-909`),所以同一条消息可反复回退到同一点(`tag -f` 让重复 messageId 取最新快照)。

**磁盘上的数据模型只有三类东西**(`src/host/store.ts:764-780`):

```
<homeBase>/dsh-recall-snapshots/<sha256(工作区绝对路径)>/
├── git/                  # 影子仓库(git init 出来的普通仓库,只当裸库用)
│   ├── .git/             # 所有 git 调用都走 --git-dir 指到这里
│   └── .git/info/        # attributes(字节保真) + exclude(基础排除表 + 用户 exclude.txt)
├── index.json / root.txt # messageId → {root, time, sessionId, files?} / 工作区权威路径
├── recall-intent.json    # 回退意图日志(崩溃续做)
└── lineage.json          # fork 父子对(版本家族)
```

容器根(`<homeBase>/dsh-recall-snapshots/`)还共享一份 `exclude.txt`;`homeBase` 按 `$DSH_HOME` → 进程 env → `os.homedir()` 三档回退(`store.ts:59-72`),写不进时降级到 `<工作区>/.dsh-recall-snapshots`,`storeRoot` 可显式改根。安全快照 `snap-pre-rollback-<毫秒>` 用独立前缀,`isSafetySnapshotId` 把它们排除在索引外(`snapshots.ts:341-343`),但孤儿重建能捡回来。

## 怎么接进 DSH

**① manifest 三层,浏览器半边没有 `inject` 字段。** `dsh.bundle.patch: "./cordis.patch.yml"`(`package.json:42-45`);`dsh.client: { platform: "web" }`(`:46-48`)——`grep -n inject package.json` 无命中,这个包不声明预读元数据;`dsh.compatibility.dshReleases` 是 **32 个逐版本** `compatible` 枚举(`:49-81`),peer 范围同样逐段枚举 `dsh-host-webserver`/`dsh-sandbox-policy`/`dsh-session`/`dsh-session-query`/`dsh-settings`/`dsh-shell`/`cordis`/`schemastery`。

`cordis.patch.yml` 全文只有一条 `insert`,行 id 是 **`recall`**(`cordis.patch.yml:9-11`),不是包名;默认值随层下发(`:15-22`:gcSnaps 50、gcHours 24、maxFileBytes 8 MiB、maxWorkspaceBytes 256 MiB、scanBudgetMs 10 s、refillDraft true)。注释明说 patch **按行替换** `config`、不做深合并——用户要覆盖就得重述整张表。

**② host 半:3 个硬依赖 + 1 个可选通道 + 1 个事件钩子。**

| 注册点 | 位置 | 说明 |
|---|---|---|
| `inject = ['shell','sessions','agents']` | `src/host/index.ts:49` | `shell` 跑 PowerShell/bash;`sessions` 列会话;`agents` 查运行中 agent(不声明会 `cannot get property ... without inject`,拦截静默 fail-open) |
| `ctx.inject(['connection'], …)` | `:425-435` | **13 个** `POST /api/recall/<name>` exact fetch 路由;刻意不硬依赖——桌面端 composition 禁用 webserver row,硬依赖会让 fiber 永久 pending |
| `ctx.on('session/event', …)` | `:441-466` | 只认 `event.type === 'user/message'`、`data.source.kind === 'user'`、`header.origin !== 'subagent'` |
| 启动预热 | `:468-527` | 轮询等待 shell 就绪(20×500 ms),再按工作区两路并发 `ensureRootReady`;从没建过库的工作区直接剪掉 |

13 个端点全 POST,同一个 `handleRecall` 分发,请求体上限 1 MB(`index.ts:402-418`);`preview`/`execute` 会跑 `git add -A`,因此按工作区串行排队,与快照、gc 共用同一条锁(`routes-core.ts:1-7`)。端点:`init`/`snapshot-info`/`preview`/`execute`/`status`/`lineage-record`/`notify`(`routes-core.ts:59,93,115,135,261,279,300`),`exclude-get`/`exclude-set`/`config-get`/`config-set`/`manage`/`config-reset`(`routes-manage.ts:311,342,362,414,493,759`)。

**③ client 半:工厂入口 + 5 个 slot 键、6 条注册(chat.node 的 `user`/`steering` 各一条)。** `window.__ModuleLoader__.load({id, factory})`(`src/client/entry.ts:37-52`),`inject: ['slots','sessions','workspaces','uiWorkspace','timer']`(`:43`)——`conversation` 故意不在列表里(0.1.1-rc.2 无此服务,静态声明会让 fiber 永久 pending),改 `ctx.get('conversation')` 探测降级。**它没有工具,也没有斜杠命令**(`grep -rln 'ctx.tools' src/` 为零,`commands.register` 也没有),模型无法自己撤回,入口只有人点按钮——这既是产品决定,也是扩散为零的直接原因。

| slot | 写法 | 位置 | 作用 |
|---|---|---|---|
| `conversation.chat.node` | keyed,key `user`/`steering`,priority 取「当前最低值 − 1」 | `src/client/app.ts:74-90` | **覆盖用户消息节点渲染器**,按钮与面板长在这里 |
| `conversation.chat.assistant-actions` | list,`id: recall-version-pager` | `:95-107` | 版本翻页器 `‹ X/N ›` |
| `conversation.session.header.actions` | list,`id: recall-version-header` | `:112-122` | 消息区渲染失败时的兜底翻页 |
| `settings.plugin.item` | keyed,`key: 'dsh-recall'` | `:134-145` | 旧设置页插件卡片 |
| `plugins.bundle.config` | keyed,`key: 'dsh-recall-plugin'` | `:149-160` | 0.1.6-alpha.2 起的 bundle 配置页 |

## 关键实现

`src/` 51 个文件,按层分:

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `src/host/snapshots.ts` | 1132 | 快照/预览/回退/切点/反馈编排 | `:839-935` 拍;`:1000-1014` diff;`:1016-1045` 回退;`:1053-1090` 切点 |
| `src/host/scripts.posix.ts` / `scripts.pwsh.ts` | 878 / 1193 | bash 与 PowerShell 两套同语义模板 | `:414-451` 快照;`:536-598` 回退;`:55` 属性固化 |
| `src/host/store.ts` | 1134 | 存储发现、路径哈希、索引读写、原子写、降级 | `:144-146`;`:661-780`;`:899-930` |
| `src/host/index.ts` | 527 | 装配:配置/存储/路由/事件/预热 | `:49`,`:425`,`:441` |
| `src/host/routes-core.ts` | 368 | 7 个核心端点(含 preview/execute 主链) | `:115-260` |
| `src/host/maintenance.ts` | 433 | gc 节流、按条数/天数清理、会话删除联动 | `:114-148`,`:166-186`,`:196-230` |
| `src/host/intent-journal.ts` | 182 | 回退意图日志,phase `rollback|rescue` | `:40`,`:61`,`:124-133` |
| `src/client/recall-node.ts` / `app.ts` | 1085 / 161 | 按钮、确认面板、执行链、fork/归档/回填;slot 装配 | `:105-210`,`:639-930`;`app.ts:74-160` |

**四条数据流:**

```text
① 拍(每条用户消息一次,fire-and-forget)
   session/event{user/message, source.kind=user} → 解析 root → 该 root 串行队列
     └─ captureSnapshot: 熔断/护栏/构建产物根早退 → resolveStore → ensureGit
        → add -A → write-tree → commit-tree(孤儿) → tag -f snap-<messageId> → 写 index.json

② 看(只读预览,但会顺手 add -A)
   preview → diffFor: 影子索引 vs snap 树 → modified(两侧都有、sha 不同) / restored(目标有、当前无)
     / added(当前有、目标无);同时回传 treeId(add 后树指纹)与全量 counts

③ 撤(写工作区,队列内复核)
   execute → agentBusy? → 格式守卫 → 安全快照 snap-pre-rollback-<ms>
     → treeId 与预览指纹比对(不等 → STALE,不再动盘) → intent.begin(rollback) → rollbackScript
         · 恢复集 = 目标有、当前无或 sha 不同 → git archive | tar -x -m(过半整树,否则 100/批)
         · 删除集 = 当前有、目标无 → 逐条 rm -f(失败即整条失败)
     → ROLLBACK_OK deleted restored → intent.clear;失败 → intent.advance(rescue) → reset --hard

④ 切会话 + 回填(纯客户端编排)
   cutSeq → sessions.fork({sessionId, atSeq}) → uiWorkspace.openSession(childId)
     → removeStaleQueueItems(childId, 被 seed 的排队项) → lineage-record
     → workspaces.archiveSession(parentId, {stopActivity: true}) → fillDraft(childId, 原文, 附件)
```

**隔离是怎么做到的(不动用户 refs/index 的关键)。** 影子仓库是 `git init <store>/git`,`--git-dir` 指向 `<store>/git/.git`,每条命令都显式带 `--work-tree=<root>`(裸 `--git-dir` 下 `update-index` 会 fatal;`tests/unit/scripts-contract.test.js:352` 把这条写成断言)。项目自己的 `.git` 从头到尾没被指过,用户的 HEAD、branch、index、stash、reflog 都不会被读或写。唯一被**读**的项目侧配置是 `.gitignore` 与 `core.excludesFile`——`add -A --exclude-standard` 就是这么工作的(`scripts.pwsh.ts:268-276` 的注释按这个口径修正过统计)。

**字节保真靠一行属性。** 影子仓库的 `info/attributes` 每次 `ensureGit` 重写为 `* -text -filter -ident -export-ignore -export-subst -working-tree-encoding`(`scripts.posix.ts:55`),优先级高于树里的 `.gitattributes`,所以 `text=auto`、`core.eol` 不会在拍/还原两侧改变换行;存量索引靠一次 `add --renormalize ':(top)'` 迁移(`:400-410`)。

**确认/取消的真实语义。** 面板是纯客户端状态机:清单逐行带 `modified/restored/added` 徽标,`both` 与 `session-only` 二选一原生 radio;「取消」只调 `closePanel`,**不发任何请求**;「确认」才发 execute(`recall-node.ts:105-210`;`tests/client/recall-node.test.ts:195`)。首条消息(`cutSeq === null`)仍可只回文件,但「无文件树 + 首条」会禁用提交(`:236`)。回退后标签不删,按钮会再次出现,再点就是「再回退到同一点」。

**测试钉住的契约**(710 例,挑与本卡论点直接相关的):

- `tests/unit/scripts-contract.test.js:352`「bare 影子仓库:update-index 一律显式 `--work-tree`」;`:439`「diff/snapshot 脚本输出 TREE 行(index 树指纹,execute STALE 比对依据)」;`:169`「issue #22 变更集恢复:rollback 恢复侧只处理 diff 出的变更项(双侧)」。
- `tests/unit/snapshots-persist.test.js:209`「rebuild 输入含 `snap-pre-rollback-123` 与 `snap-abc` → 索引只收 abc」;`:281`「truncated(读截断)→ rebuild 整体跳过且不写盘」。
- `tests/unit/store-format.test.js:256`「execute:守卫拒写 → FORMAT_BLOCKED 响应,且不跑安全快照/回退」。
- `tests/client/recall-node.test.ts:252`「确认 → execute 携带 previewTreeId/previewTotal/scope;成功后 fork/导航/归档/队列清理全链发生」;`:303`「STALE → 自动重新 preview 回到确认面板」;`:345`「fork 失败 → 降级为仅文件回退:不导航、不清理队列、不归档」。

## 为什么它突出

**先拆星标归属:仓库级 = 插件级,没有宿主可借。** 单包结构(`package.json` 在根,`repository.url` 指向自己),325 个提交全属这一个包。时间线:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-14 | 仓库创建 | 编排者给定 |
| 2026-08-15 00:16 | 首提交 `a16e4ec feat: 消息撤回插件（影子 git 快照 + 对话整段回退）` | `git log --reverse` |
| **2026-08-19** | **⚠ 21 星采样点**(仓库第 5 天) | registry ⚠ |
| 2026-11-17 | v2.6.8、325 提交、19 tag | `git log -1` |
| 2026-11-18 | 实时 55 星 | 编排者 GitHub API |

**21 → 55(+34)发生在三个月的高频发布期**,而 21 星是最初 5 天拿到的——发布即被看见,之后靠迭代慢涨,不是宿主事件带上来的。55 星放在生态里不算高,**所以本卡不称它「类内头部」,而是「同类需求里少数把文件与对话两侧都做全的实现」。** 1105 下载对 55 星约 20:1,说明装的人明显多于点星的人(工具型插件的典型形状);但下载来源边车没记,**待验证**,不能当「1105 个活跃用户」。

**零扩散,而且是最严口径的零。**

```sh
# 在 awesome-dsh-plugin 仓库根执行
grep -ril 'recall-plugin'       data/plugins/ | wc -l   # 1  ← 只有它自己
grep -ril 'limbo947'            data/plugins/ | wc -l   # 1  ← 只有它自己
grep -ril 'dsh-recall'          data/plugins/ | wc -l   # 4  ← 自身 + 3 个同名不同仓库
grep -ril 'dsh-recall/complete' data/plugins/ | wc -l   # 0
grep -ril 'dsh-recall/failed'   data/plugins/ | wc -l   # 0
```

`dsh-recall` 那 4 条逐条判断:除去自身,`imtwa/dsh-recall-sessions`、`hg1048596-pixel/dsh-recall-unread`、`Relistencode/dsh-recall` 都是**各自仓库名里带 recall**,既没写本仓库 URL、包名,也没写 `limbo947` 或本插件的服务/事件名——不是引用,不计扩散。它确实对外发两个终态事件 `dsh-recall/complete` 与 `dsh-recall/failed`(`routes-core.ts:28-29`),但全表无人监听。

**为什么零扩散?我的判断是两条:**

1. **它是给人点的按钮,不是给插件用的接口。** 没有 service key、没有工具、没有命令;唯一的横向面是两个 fire-and-forget 事件,消费方得先知道名字。`manage`/`config-*` 是「本插件的设置页」而非公共 API。
2. **格式不可复用,价值也不在抽象。** 想读它的快照就得理解 `snap-<messageId>` 命名、`snap-pre-rollback-*` 安全标签、`index.json` 的 feedback 清洗、`recall-intent.json` 的两 phase 恢复——全是私有语义;两侧状态权威不同源,中间靠 `cutSeq` 与 `treeId` 缝合,这套缝合没有第三方可插入的缝。

**「逐消息」相对「整轮回退」的差异,只就它自己说:** 一条用户消息 = 一个标签 = 一棵树,回退目标精确到「那条消息发出前的字节」,并把该消息之后整轮 agent 的全部改动一起丢掉;代价是每条消息付一次 `add -A`(全工作区遍历 + 对象写入),收益是「撤回第 7 条」与「撤回第 12 条」互不依赖、可任意顺序、可反复执行。整轮粒度省快照次数,丢的是消息级定位与同一消息的多次回退——它选了前者,也正因此必须自造限流/熔断/预算:成本按消息数线性长。

## 代价与边界

- **权限边界等于宿主用户,且每条消息一次全树扫描。** host 半在 DSH 进程里拼 shell 跑 `git`/`tar`/`rm`,不借会话沙箱(README 明确「以宿主身份执行」),`git` 取自 PATH——拿到的是这个用户的全部文件权限。默认 `maxFileBytes` 8 MiB、`maxWorkspaceBytes` 256 MiB、`scanBudgetMs` 10 s、`snapshotBudgetMs` 180 s、`maxSnapshotsPerWorkspace` 500(`src/host/config.ts:44-75`)。超总量/超预算的处置是**整体停用该工作区快照**而非截断——截断会让「目标没有、当前有」的文件在回退时被当新增删掉(`scripts.pwsh.ts:262-268`),这个取舍是对的。
- **拍快照与 agent 起跑之间没有栅栏。** 事件回调 fire-and-forget,快照排进该工作区串行队列(`index.ts:441-466`);若队列正被上一次快照/回退/gc 占用,`add -A` 可能晚于本轮 agent 的第一次写文件。**判断:** 这是「快照不等于发送时刻」的唯一窗口,代码路径上成立,但我没有找到覆盖它的用例(见待验证)。
- **不还原的东西(按代码顺序):** `.git` 与被排除目录;被 `.gitignore`/`core.excludesFile` 忽略的文件(不进 `add -A`,回退也不删);超过 `maxFileBytes` 的文件(显式从索引剔除、回退不碰);嵌套仓库/子模块(160000 gitlink 在 add 前后各清一次,内容完全不进快照,`scripts.posix.ts:66-78`);特殊文件(fifo/socket,`add` 报 `unable to index` 后走 `SNAP_SKIP`);xattr/ACL/属主;mtime(`tar -x -m` 故意不恢复,防 stat 缓存误判,`scripts.posix.ts:554-558`);以及**空目录**——删除侧只 `rm -f` 文件,新建目录树在删完后会留空壳。
- **符号链接**:以 120000 条目记录、以链接本身还原;POSIX 下 git 不跟随指向目录的符号链接,Windows 侧另有 junction 爆炸防护(`scripts-contract.test.js:115`)。**判断:** 指向工作区外的文件链接会原样还原成链接,不会写穿到外部——但这依赖 git 语义而非插件自己的路径闸,未见专门用例。
- **失败模式,按发生顺序:**

  1. **没有 `git`** → `gitExe === ''`,init 下发 `notice.gitMissing`,撤回按钮根本不出现(`routes-core.ts:74-77`)。
  2. **工作区是构建产物根 / 超限 / 扫描失败** → 该工作区快照停用,按消息写 `failed` 反馈;`messageOnly` 模式下仍可只回退对话。
  3. **目标工作区有 agent 在跑** → `RECALL_AGENT_BUSY`,预览与执行都拦(执行时队列内二次检查,检查后紧接执行)。
  4. **预览后文件变了** → `STALE`(拿安全快照的 treeId 比对),客户端自动重新 preview,不写盘。
  5. **安全快照失败** → 记错误、继续回退(用户已确认),但此后无救援点。
  6. **回退脚本没打出 `ROLLBACK_OK` / 抛错** → 视为「可能半回退」,`reset --hard` 到安全快照;救援也失败 → 面板给可复制的手动命令,`recall-intent.json` 留痕。
  7. **fork 失败/返空** → 文件已回退、对话未回退;界面降级为「仅文件回退」,不导航、不清理队列、不归档,并上报 `failed(fork)` 事件。
  8. **归档失败** → 只 warn,原会话留在列表且可能继续跑(`archiveSession(..., {stopActivity:true})` 会先拒掉有活动的会话)。
  9. **磁盘格式高版本/损坏** → `RECALL_FORMAT_BLOCKED` 拒写(fail-closed),读路径不受影响。
  10. **同一工作区连续失败 3 次** → 指数退避熔断(5 min 起,上限 60 min);并发实例用心跳(900 s TTL)互让。
  11. **磁盘满/只读** → 索引写失败、快照不落盘,该条消息无快照;不产生半条索引。

- **维护成本是真实门槛。** 三个月 325 个提交、19 个版本 tag,`CHANGELOG.md` 通篇是「跟 DSH 版本 + 修 issue」;兼容表 32 个 release 逐条手写,两套 shell 模板(878 + 1193 行)靠契约测试对齐。**跨平台成本高于纯 JS 实现**:Windows 侧要处理长路径、junction、device name、`.NET` 解压 API(`CHANGELOG.md` 里 issue #12/#32/#34 全属此类)。
- **快照库自身会被算进工作区**——工作区根是 `$HOME` 且排除表漏掉 `dsh-recall-snapshots/` 时,影子库会把自己吞进快照。作者用两条默认排除 + 一次实测(issue #6)堵住,但这是**配置依赖的安全**:用户改 `baseExcludes` 时若只写半张表,仍可能再次踩中。

## 可信度与复现

- **★★★**:`src/host/` 的 `index.ts`、`config.ts`、`routes-core.ts`、`snapshots.ts`(捕获/预览/回退/切点段)、`scripts.posix.ts`(快照/回退/diff/排除/护栏段)、`store.ts`(路径/存储/索引段)、`maintenance.ts`(清理段)、`intent-journal.ts` 关键段;`src/client/` 的 `entry.ts`、`app.ts`、`recall-node.ts`(面板与执行链);`package.json`、`cordis.patch.yml`、`README.md`、`CHANGELOG.md` 头部;`tests/unit` 与 `tests/client` 的用例名与关键断言。
- **对照本机 DSH**(`~/.nvm/.../@deepseek-ai/dsh`):`conversation.chat.node`/`assistant-actions`/`user.content`/`session.header.actions` 四个 slot 键在对应 client bundle 里存在;`atSeq` 是「inclusive cut,缺省取最近一个已完成 turn 的边界」(`dsh-api-session-controller/lib/index.js:844-870`),与插件的 `turn/end.seq` 切点语义一致;`archiveSession` 吃 `{stopActivity:true}`(`dsh-api-workspace-controller/lib/index.js:297-299`)。
- **未读**:`routes-manage.ts` 全文(只读端点签名)、`store.ts` 的迁移/blobs 清理分支、`scripts.pwsh.ts` 的脚本实现(只读注释与同名签名)、`src/client/edit-node.ts`/`version-pager.ts`/`snapshot-manager.ts`/`draft-fill.ts` 的实现细节、`tests/probe/*`。所以「编辑并重发」与「版本翻页」两条支路只到入口与用例名的程度。

```sh
# 1) 提交与历史(仓库已在 .work/mine/cards/recall-plugin/repo,非浅克隆)
git -C .work/mine/cards/recall-plugin/repo log -1 --format='%H %ad %s'
# → d00321ec6322b7eb77fed3a27bff93d80b33803a  Tue Nov 17 21:59:01 2026 +0800  fix(host): ensureGit …
git -C .work/mine/cards/recall-plugin/repo rev-list --count HEAD   # 325
git -C .work/mine/cards/recall-plugin/repo tag | wc -l             # 19
git -C .work/mine/cards/recall-plugin/repo log --reverse --format='%h %ad %s' | head -1
# → a16e4ec Sat Aug 15 00:16:34 2026 +0800 feat: 消息撤回插件（影子 git 快照 + 对话整段回退）

# 2) 规模
cd .work/mine/cards/recall-plugin/repo
wc -l $(find src -name '*.ts') | tail -1                         # 14364
ls tests/unit/*.js tests/client/*.ts | wc -l                     # 63
grep -rhcE "^\s*it\(" tests/unit/*.js tests/client/*.ts | awk '{s+=$1} END {print s}'   # 710

# 3) 扩散(在 awesome-dsh-plugin 仓库根)
grep -ril 'recall-plugin' data/plugins/ | wc -l                  # 1
grep -ril 'limbo947'      data/plugins/ | wc -l                  # 1
grep -ril 'dsh-recall'    data/plugins/ | wc -l                  # 4(自身 + 3 个同名不同仓库)
grep -ril 'dsh-recall/complete' data/plugins/ | wc -l            # 0

# 4) 类目分母
python3 _digested/ecosystem/census.py | head -6                  # 总数 11744;session 914
```

## 待验证

1. **`1105` 下载从哪来。** 边车只记数值与日期,没记来源(README 徽章用 `npm/dm`)。npm 公开 API 只给最近一周,回填不了 2026-08-19;要判断真实采用量得看 tarball 安装数或 release 下载数,本仓都没采集。
2. **快照延迟窗口有多大。** 事件回调不 await(`index.ts:441-466`),快照排在该 root 的串行队列里。若队列正跑一次大仓库 `add -A`(上限 180 s)或 gc(上限 30 min),本轮 agent 早已改完文件——此时撤回会退回到一棵被污染的树。需要构造用例量化「队列忙时拍下的快照」与「发送时刻」的差。
3. **全局 `core.excludesFile` 与系统级 gitconfig 会参与 `add -A`。** 影子仓库没设 `GIT_CONFIG_NOSYSTEM`,也没覆盖 `core.excludesFile`,用户全局 ignore 会影响快照内容——影响面多大、会不会把本该能回退的文件排除在外,未验证。
4. **子模块边界。** gitlink 被清出索引、子模块目录不进快照;但**子模块工作区里的未提交改动**、以及 `.gitmodules` 本身是否随快照还原,我只核到「gitlink 被过滤」这一层,没读到子模块路径在删除侧的行为。
5. **32 个 DSH release 的兼容矩阵有没有自动化。** 表是手写的,`scripts/check-dsh-version.mjs` 存在但本次未读;CI 是否真在多个 DSH 版本上跑,未核。
6. **子会话里再次撤回的边界。** `resolveCutSeq` 对 seeded 会话走 `observeSession` 降级(`snapshots.ts:1053-1090`,注释提到 `readSession` 对 seeded 会话恒抛),但「子会话与父会话的消息 id 是否重合」「重复撤回会不会让 lineage 图成环」没有用例可引。
