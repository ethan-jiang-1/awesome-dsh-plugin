# turn-rewind — 每轮开头给整个工作树拍一张内容寻址快照，回退 = 状态还原 + 借宿主 fork 造新会话

> 证据等级:★★★(源码级;`Anionex/dsh-turn-rewind@f357dad58c8f42b705c009a4ff352ec33a034e3c`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 **83** 为 2026-08-19 历史采样(2026-11-18 实时 **150**);⚠ 下载 2373 同为该日。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `Anionex/dsh-turn-rewind`([registry](../../../data/plugins/Anionex__dsh-turn-rewind.yml)) |
| 类目 | session([census](../../ecosystem/census.py) 914 条 / 全表 11 744 条) |
| 子分类 | `rewind-edit`(回退与编辑);⚠ 星标为**整个 session 类目第一**,且属本插件自身,不是宿主背书 |
| 自述 | 「对话回退：基于持久 Change Ledger 回滚会话与工作区状态」——两个维度在源码里确实是分开的:文件还原走自己的引擎,会话「回退」走宿主的 fork |
| 星标 ⚠ | **83**(2026-08-19 冻结采样);2026-11-18 实时 **150**、fork 16、开放 issue 5。仓库只有这一个插件,**星标属于本插件,不是宿主背书** |
| 下载 ⚠ | **2373**(2026-08-19 采样;边车未记录该数的来源,是否 npm 周下载待验证) |
| 扩散 | **0**(口径:`grep -ril 'turn-rewind' data/plugins/` 命中 1 条 = 自身;详见「为什么它突出」) |
| 仓库 commit | `f357dad58c8f42b705c009a4ff352ec33a034e3c`,2026-11-12,`chore(release): publish v0.3.13 (#37)`;仓库 `created_at` 2026-08-13,最早提交 author date 2026-08-09 |
| 包形态 | npm `@anionex/dsh-turn-rewind@0.3.13`(21 个版本);**DSH Profile Bundle + `dsh.client` 双面包**:`cordis.patch.yml` 4 行,`lib/` 预构建随包提交 |
| 代码规模 | `src/` **10 287 行**(服务端 `src/*.ts` 7 936 + 浏览器 `src/client/index.tsx` 2 324 + 客户端辅助 27);测试 5 033 行 / **149 例**;`lib/` 构建产物 8 271 行 |
| 历史 | 110 个提交、20 个 tag(v0.1.0 2026-08-14 → v0.3.13 2026-11-12);⚠ 采样点之后的提交 65 个 |

## 它到底是什么

**是一个真插件,不是配置包,也不是外部系统的适配层。** 它自带上万行代码、自造磁盘格式、自带恢复引擎(`src/engine.ts:68` `ChangeLedgerEngine`),对 DSH 只提出四类要求:两个事件钩子、4 条同源 HTTP 路由、一个设置命名空间、一组浏览器 slot。

**第一个要纠正的命名误会:`Change Ledger` 存的是「状态」,不是「变更」。** 一条 restore point 的持久内容是**整棵树的全量清单**:`entries: Record<path, {kind,blob,size,mode}>` + `treeHash`(`src/types.ts:75-106`)。没有 delta、没有反向 diff、没有「第 N 轮改了哪几个文件」的记录。所谓「变更」是**读取时现算的**:`inspect` 把清单和当前工作树各算一次树,再 `diffTrees`(`src/engine.ts:518-539`;`src/snapshot.ts:234-284`),产出 `added / deleted / modified / mode-changed / type-changed` 五种(`src/types.ts:139-144`)。去重发生在**内容层**而不是记录层:同一个 blob 哈希在存储里只存在一份。

对象模型只有四个真实实体(全部可用源码核对):

- **restore point** — `kind: 'user' | 'rescue' | 'turn'` 三选一(`src/types.ts:72`)。`user` 由服务 API 显式创建;`rescue` 是每次还原**之前**自动拍的备份(`src/engine.ts:651-658`);`turn` 是每轮第一个 step 之前的隐藏检查点。三种点的元数据字段完全一样,差别只在谁创建、谁可以删。
- **manifest(两种格式)** — v1 把每个文件写成自己 CAS 里的 sha256 blob;v2 走 Git 对象库,manifest 只剩 sidecar + 一个私有 ref `refs/dsh-turn-rewind/v2/<storeId>/<worktreeId>/<rp_id>`(`src/git-checkpoint.ts:253`;`src/types.ts:125-133`)。
- **restore plan** — 纯内存、带 TTL、带一个必须原样回传的 `confirmation: RESTORE-XXXXXXXX`(`src/types.ts:189-202`)。它就是「人在回路」的载体:预览、选中路径、HEAD 栅栏、每条路径的期望值都固定在 plan 里。
- **restore operation** — 持久化日志,状态机 `running → completed | rolled-back | recovery-required | interrupted`(`src/types.ts:205-218`;`docs/FORMAT.md:78-98`)。写在工作树被修改**之前**。

**磁盘布局**(`docs/FORMAT.md:5-17`,与 `src/store.ts:669-672`、`:715-717`、`:288` 一致):

```
<DSH_HOME or ~/.dsh>/change-ledger/v1/
├── store-id.json                     # 存储根身份,私有 ref 命名空间用
├── workspaces/<key>/
│   ├── lock.json                     # PID + hostId + nonce 独占锁
│   ├── manifests/rp_<time>_<rand>.json
│   ├── operations/op_<time>_<rand>.json
│   └── blobs/<前两位>/<sha256>        # v1 的内容寻址存储
└── worktree-claims/<worktreeId>.json # 防两个仓库共用同一 worktree 命名空间
```

`<key>` 的算法分两种:Git 工作树用 `git-<sha256(commonDir\0worktreeId)>`(`src/store.ts:1729-1731`),普通目录用 `sha256(绝对路径)`(`src/store.ts:669-672`)。JSON 一律「同目录临时文件 + fsync + rename」(`src/path-utils.ts:62-79`),blob 用「临时文件 + fsync + 硬链接 + 已存在则回读校验哈希」(`src/store.ts:277-318`)。

**它怎么与 turn / session 事件对齐**:turn 检查点只认一个三元组 `(sessionId, turn, turnStartSeq)`。`turnStartSeq` 是 `turn/start` 事件的 `seq`,在 Agent 进入第一个 step **之前**读取(`src/rewind-host.ts:232-238`),所以语义严格是「Agent 还没处理这条用户消息」。三元组重复时直接复用已有点(`src/engine.ts:299-313`);格式只允许一个边界,`turnEndSeq` 是旧实现遗留、只读不用于新入口(`docs/FORMAT.md:70`;`tests/validate.test.mjs:26-32`)。

**会话那一维不是「截断」,而是「分叉」。** DSH 的 session 日志是 append-only(`dsh-session/lib/index.js:1033,1317`),所以插件从不改历史:它调宿主的 `sessionController.fork({sessionId, atSeq: previousTurnEndSeq})` 或 `create({cwd})` 起一个新会话,再把原消息文字与附件放回输入框草稿(`src/rewind-host.ts:815-826,835-847`;`src/client/index.tsx:2136-2168`)。原会话完整保留。

## 怎么接进 DSH

**① manifest 是三层,不是一个字段。** `package.json` 里三块都要看:

- `dsh.bundle.patch: "./cordis.patch.yml"`(`package.json:51-54`);而 `cordis.patch.yml` 全文只有 4 行、一个 `insert`,**没有任何 DSH core patch 或 `config`**(`cordis.patch.yml:1-4`)。
- `dsh.client: { platform: "web", inject: [5 个 UI 包] }`(`package.json:55-64`)——双面包的浏览器半边声明;`inject` 只是**预读元数据**,不是 Cordis 服务注入,`tests/package-layout.test.mjs:16-36` 把这句话写成了断言。
- `dsh.compatibility.dsh` 是一串**逐版本枚举**的区间,16 个发布 + `profiles: ["web"]`(`package.json:65-88`)。

它在 `dsh.bundle.patch` 之外还额外声明 `dsh.client`,而 `dsh-client-modules` 正是按这个键把包识别成「双面包」并装配 `window.__DSH_BOOT__` 条目图的——它的校验器对 `platform` 强制要求字符串、对 `inject`/`external` 要求字符串数组(`dsh-client-modules/lib/index.js:66-67`),本包的声明正好落在合法形状内。

**② 一个服务 + 两组 inject。** `ctx.provide('changeLedger', this)`(`src/index.ts:61`)把引擎暴露成 Cordis 服务;`ctx.inject(['agents'])` 装检查点协调器,`ctx.inject(['webServer','sessions','sessionQuery','agents'])` 装路由(`src/index.ts:65-72`)。注释明确写了 `apiProxy` **故意**不出现在 inject 列表里:0.1.2-alpha 系载体(DSH Desktop 2.x)只提供 `sessionController`,路由必须在两种载体上都存在(`src/index.ts:66-67`)。启动对账是 fire-and-forget,失败只记日志、不阻断加载(`src/index.ts:74-82`)。

**③ 两个钩子,一进一出**(`src/rewind-host.ts:186-198`):

| DSH 事件 | 参数 | 做什么 | 位置 |
|---|---|---|---|
| `agent/pre-step`(`prepend: true`) | `({agent, turn, step, signal})` | 仅 `step === 1` 时**异步**发起一次检查点抓取,不 await,直接 `next()` | `:187-190` |
| `tools/execute`(`prepend: true`) | `(exec, next)` | 只对**根调用**(`exec.parent === undefined`)等这一轮抓取落定,再放行工具 | `:192-197` |

这两个形状都能在本机 DSH 里对上:`agent/pre-step` 是 waterfall,payload 由 `{messages, turn, step, signal}` 加派发时补的 `agent` 组成,且 `turn/start` 在第一次 pre-step **之前**就已 append(`dsh-agent-loop/lib/index.js:909,945`);官方 `dsh-session-checkpoint-policy` 用的正是 `async ({agent}, next)` 与 `exec.agent/exec.parent` 同一套写法(`dsh-session-checkpoint-policy/lib/index.js:66,72`)。

这个「pre-step 不等、tools/execute 才等」的组合是本插件最巧的一处:它把抓取从**模型响应路径**上挪走(不拖慢首 token),又保证**第一个副作用型工具**执行前状态已经落盘——所以「检查点」和「工具改文件」之间没有窗口期。`tests/rewind-host.test.mjs:61-108` 就是钉这个契约的:pre-step 立刻返回 `enter`、状态 `pending`,根工具调用挂住,抓取释放后工具才继续;嵌套调用(`parent: Symbol()`)完全不挂。第 110-151 行再钉住「等的时候被取消,要把取消原样交还给运行时」,否则 DSH 会丢掉它自己的 `ABORTED_BEFORE_DISPATCH` 结果。

**④ 同源 HTTP 路由(4 个注册路径、5 个处理分支)**,全部 `webServer.register({kind: 'exact', …})`(`dsh-host-webserver/lib/index.js:326`):

| 路径 | 方法 | 作用 |
|---|---|---|
| `/turn-rewind` | GET | 按 `messageSeq` 解析检查点 → `inspect` → 生成 plan,返回分页 diff 预览(`src/rewind-host.ts:546-609`) |
| `/turn-rewind` | POST | `mode: code \| both \| messages` 三选一,`code/both` 必须带 planId+confirmation(`:611-672`) |
| `/turn-rewind/turns` | GET | 只读:把每个 turn 映射到它的开篇用户消息 `seq`(`:418-435`) |
| `/turn-rewind/manage` | GET/POST | 存储管理:列 workspace、删点、GC(`:1077-1133`) |
| `/turn-rewind/attachment-bytes` | GET | 把历史消息里的附件字节回放给浏览器草稿(`:1015-1063`) |

注意这些路由**没有 DSH 鉴权包装**,安全性靠「同源 + 服务端重新解析边界」:POST 不信任客户端传来的 seq,自己再跑一遍 `messageTarget`(`:850-884`),边界不一致就 `PLAN_STALE`。

**⑤ 设置命名空间是个裸字面量。** `TURN_REWIND_SETTINGS_NAMESPACE = 'turn-rewind'`(`src/settings.ts:24`),因为 0.1.5 把 `settingsNamespace` 助手删了、命名空间退化成编译期品牌。安装函数按载体三分支:`provider.installSection`(0.1.5)→ `provider.register` + `watch`(旧宿主)→ 都没有就只吃 patch 层配置(`src/settings.ts:142-169`)。`storageDir` **故意不可在设置页改**(`src/settings.ts:119-128`)。

**⑥ 浏览器侧:一个官方 slot + 一次 DOM portal。** `apply()` 注册三处(`src/client/index.tsx:953-993`):`conversation.session.header.actions`(会话级 list slot,id `turn-rewind-portals`,order 100)、`settings.plugin.item`、`settings.plugins.tab`。第一个确实是 DSH 的官方 slot,而且是 `scope: "session"` 的 `list`(`dsh-client-ui-conversation/lib/client.js:20058`)。

但回退按钮要挂在**每条用户消息**下面,DSH 没有这个 slot。源码注释写得很直:「0.1.5 没有 user-message actions 的官方 slot,只有 `conversation.chat.assistant-actions`(给已完成的助手轮),所以这座桥只能留在 DOM 上」(`src/client/index.tsx:1968-1979`)。于是有了两层兜底:

- 0.1.x:宿主还注入 `useChat/useSession` 快照钩子 → 走 React 节点树;
- 0.2.x:钩子没了 → `MutationObserver(document.body)` 盯 `data-chat-turn` 属性,再用 `GET /turn-rewind/turns` 把渲染行号换成事件 seq(`src/client/index.tsx:1100-1189`)。

portal 的落点是 `[class*="actions"]`(CSS-module 类名 `<hash>_actions`),旧宿主再兼容 `[data-time-hover-root="true"]`(`:1953-1986`)。我核对了本机 0.2.1-rc.5:chat 行确实带 `data-chat-flow-kind`/`data-chat-turn`(`dsh-client-ui-chat/lib/client.js:3807-3812`),而 slot 清单里确实没有任何「用户消息动作」seat(`grep -o 'conversation\.chat\.[a-z.-]*'` 只有 assistant-actions 与 user.content/user.images)——**它的判断是对的,这是 DSH 侧的真实缺口,不是作者偷懒**。

**⑦ 它没有工具,也没有斜杠命令。** `src/` 里没有 `ctx.tools`、没有 `commands.register`。模型无法自己触发回退;入口只有人点按钮,或别的插件调 `ctx.changeLedger`。这是产品决定,也是安全边界的一半。

## 关键实现

`src/` 18 个文件,按职责分四层(Git 工作树 / 普通目录 / 恢复引擎 / 宿主适配):

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `engine.ts` | 1452 | 引擎:创建、比对、计划、应用、删除、对账 | `:53-65` 默认值;`:270-394` turn 检查点;`:618-768` 应用 |
| `store.ts` | 1796 | 持久层:锁、原子写、blob、manifest、迁移与 reclaim | `:104-159` 启动对账;`:216-263` 锁;`:277-318` blob |
| `client/index.tsx` | 2324 | 浏览器:按钮、弹窗、设置卡、草稿恢复 | `:953-993` slot;`:1100-1189` DOM 桥 |
| `rewind-host.ts` | 1133 | 宿主适配:hook、4 条路由、turn 锚点、血统解析 | `:186-198` hooks;`:727-780` 血统 |
| `git-checkpoint.ts` | 853 | v2 Git 原生检查点(私有 index / envelope / ref) | `:97-102` 隔离环境;`:219-240` 树与提交 |
| `git.ts` | 551 | Git 探针:根、worktree 身份、sparse/submodule 拒绝 | `:31-49` |
| `snapshot.ts` | 426 | 抓取、diff、treeHash | `:40-146`;`:294-309` |
| `validate.ts` | 359 | 持久格式校验(未知版本/畸形一律拒绝) | 全文 |
| `path-utils.ts` | 265 | 路径校验、原子替换、安全父目录、空目录剪枝 | `:13-38`;`:118-213` |
| `directory.ts` | 222 | 普通目录枚举 + `.dsh-rewindignore` | `:63-109` |
| `types.ts` | 303 | 持久与 API 类型 | `:75-136`;`:189-218` |
| `settings.ts` | 170 | 设置命名空间与三分支安装 | `:142-169` |
| `index.ts` | 155 | 服务定义与 inject | `:59-83` |
| `path-cache.ts` | 144 | 路径身份缓存(未变文件不重读) | 全文 |
| `workspace.ts` / `deadline.ts` / `errors.ts` / `client/platform.d.ts` | 66/18/23/27 | 工作区发现、超时、错误码、浏览器侧类型声明 | — |

**五条数据流,别混:**

```text
① 自动抓取(每轮 step 1 之前)
   agent/pre-step(step===1) ──不 await──▶ TurnCheckpointCoordinator.capture
     ├─ 从 session 事件取 turn/start 的 seq(找不到→failed,不影响本轮)
     ├─ 按 workspace 串行(serializeWorkspace)
     ├─ mode=auto + Git 工作树 → v2 Git 原生;否则 → v1 CAS
     └─ 失败/超时/关闭 → 写一条持久 skip 标记(下次仍可重试)

② 预览 + 计划(只读)
   GET /turn-rewind ──▶ inspect(清单 vs 当前树 → changes) ──▶ planRestore
     过期 15 min、绑 session、confirmation 随机、逐路径记 expected

③ 应用(写)
   POST mode=code|both ──▶ applyRestore
     锁工作区 → 重读清单 → verifyGitCheckpoint(v2)
     → 重算当前树 → 校验 HEAD/branch/操作栅栏 → 逐路径 PLAN_STALE 校验
     → 拍 rescue 点 → 写 operation(running)
     → 删(深→浅) → 还原(浅→深) → 双读验证
     → completed / 回滚 / recovery-required

④ 会话分叉
   mode=both|messages ──▶ messageTarget(重解析边界)
     → sessionController.fork({atSeq: 上一个 turn/end}) 或 create({cwd})
     → 浏览器 openSession + conversation.input.for(scope).setDraft(原文)

⑤ 崩溃对账(下次启动)
   store.initialize ──▶ 非终态 journal → interrupted(仅当无活锁持有者)
   reconcileGitCheckpointJournals ──▶ publish/delete 两个方向的 ref 与 manifest 对齐
```

**恢复为什么不是「删了重写」**。`restorePaths` 分两趟:删除按**最深优先**、还原按**最浅优先**,避免父子路径互相踩(`src/engine.ts:1044-1081`)。每一趟在真正落盘前,都拿 plan 里记的 `expected` 再算一次该路径的当前快照,不等就 `PLAN_STALE`(`src/engine.ts:1084-1104`)——所以「预览之后又被改过」在**单条路径**粒度上会失败,而不是整树重比一遍。写文件一律「同目录临时文件 + fsync + rename」,再 `chmod` 回落权限位(`src/path-utils.ts:144-160`)。写完做**双读验证**:连续读两次相同、且等于期望值才算成功,否则 `RESTORE_VERIFY_FAILED`(`src/engine.ts:1106-1125`)。

**防止越界的四道闸**(全部在 `path-utils.ts`,不依赖 Git):

1. 清单里的路径先过 `validateRelativePath`:非空、无 NUL、非绝对、非盘符、无空段/`.`/`..`(`:13-28`);
2. `resolveWorkspacePath` 再 `resolve` 一次并做 `isWithin` 复查(`:31-38`);
3. 落盘前 `lstat` **每一级父目录**,遇到 symlink 直接 `SYMLINK_PARENT`,遇到非目录 `PARENT_NOT_DIRECTORY`(`:118-141`)——防「检查后把父目录换成软链」;
4. 删除只删单项:目录用 `rmdir`,非空就 `DIRECTORY_NOT_EMPTY` 拒绝,`rm -r` 在工作树内容上**一次都没出现**(`src/path-utils.ts:175-195`;`SECURITY.md:35-36`)。

**普通目录模式**是 0.3.0 才有的:`.git`、`node_modules` 内置排除,**最后**才 add,所以用户 `.dsh-rewindignore` 的否定规则无法把它们重新纳入(`src/directory.ts:63-109`);软链只记录不跟随;特殊文件(socket/设备/管道)记为 skip。

**测试钉住了什么**(149 例,5 033 行)。它们不是在测 DSH,而是在测**这批契约**:

- 存储与格式:`tests/engine.test.mjs:1880-1897` 改一个字节的 manifest 必须被 treeHash 拒绝;`:1898-1907` blob 地址不匹配必须拒收。
- 恢复语义:`:1436-1468` 全量恢复 = 两步确认 + 自动 rescue + 验证 + 可逆;`:1504-1517` 选择性恢复只改被选路径;`:1518-1532` 预览后改文件 → 计划失效;`:1657-1686` 恢复失败回滚到 rescue。
- 冲突:`:1586-1601` 规划阶段拒绝覆盖被忽略文件;`:1602-1619` 应用阶段拒绝预览后新建的被忽略文件;`:1620-1656` HEAD 漂移默认阻断、显式审核后才放行、且不会放行「之后再漂一次」。
- 崩溃与并发:`:1687-1711` 非终态 journal 启动后变 `interrupted` 并给出 rescue;`:1769-1797` 不抢活进程的锁;`:1469-1503` 同一 plan 不能并发应用。
- 宿主血统(`tests/rewind-host.test.mjs:853-882`):子会话优先自己的点、兄弟不串、`seedLength` 拦住越界继承;`:884-902` 0.1.5 对**无父会话**报 `inheritedEventCount: 0`,不能把这个 0 当血统(否则每个根会话都被 `PLAN_STALE` 拒掉);`:904-931` 有父会话时沿 `inheritedEventCount` 找回父的点。
- 打包契约(`tests/package-layout.test.mjs:10-136`):`dsh.bundle.patch` 指向正确、`dsh.client` 只声明 web + 5 个 preload、兼容矩阵逐版本、`exports` 每个入口都有 `lib/types/` + `lib/`、`devDependencies` 不许出现绝对路径/`file:`/`link:`、`src` 与 `lib` 里都不许 import 0.1.5 删掉的两个助手函数。

这份 package-layout 测试值得单独说一句:它把「Profile Bundle 装得上」这件事变成了 137 行可执行断言(含「必须提交 `lib/`」这条 AGENTS.md 规则的实际后果),这也是它能同时支持 16 个 DSH 发布版本还敢发版的原因。

## 为什么它突出

**先拆星标归属,这次是干净的。** 这里没有宿主项目可以借用:仓库 `Anionex/dsh-turn-rewind` 只有这一个包,`package.json:6-7` 的 repository 指向自己,GitHub `stargazers_count` 就是插件的。时间线也支持:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-09 | 最早提交 `c6d8a97 feat: add persistent workspace change ledger` | `git log --reverse` |
| 2026-08-13 | 仓库 `created_at`(历史在创建时被重放,提交日期早于仓库 4 天) | GitHub API |
| 2026-08-14 | npm 0.1.0 / tag v0.1.0 | npm registry、tag 日期 |
| **2026-08-19** | **⚠ 83 星采样点**(仓库 6 天、首个 tag 5 天) | registry ⚠ |
| 2026-11-12 | v0.3.13、110 个提交、20 个 tag | `git log -1` |
| 2026-11-18 | 实时 150 星、16 fork、5 开放 issue | GitHub API |

**83 → 150 的增量(67 星)全部发生在产品成熟期,前 6 天拿了现在的 55%。** 这是一条「发布即头部、之后慢涨」的曲线,不是靠某个宿主事件带起来的。

**类内位置要用两把尺子量。** 一把量类目:session 914 条里只有 **83 个条目**有星标记录(其中 69 个非零),第一名 83、第十名 15——**类目本身很薄**。另一把量全表:83 星其实不低,边车覆盖的 1 447 个 URL 中只有 **51 个**高于它(约前 3.5%),ui 的 2 349 条里只有 **7 个**高于它。所以它的位置是「薄类目里的绝对头部,兼全表前 4%」,不是矮子里的高个。子分类 `rewind-edit` 只有 2 个成员(本卡 83,另一个 32)。

```sh
# 上面两组数字的口径(在仓库根执行;EOF 之间就是脚本本身)
python3 - <<'EOF'
import json,glob,re
s=json.load(open('data/stars.json')); buckets={}
for f in glob.glob('data/plugins/*.yml'):
    t=open(f,encoding='utf-8').read()
    u=re.search(r'^url:\s*(\S+)',t,re.M); c=re.search(r'^category:\s*(\S+)',t,re.M)
    if not (u and c): continue
    r=s.get(u.group(1).rstrip('/'))
    if r: buckets.setdefault(c.group(1),[]).append(r['stars'])
every=[x for v in buckets.values() for x in v]
print(len(s), sum(x>83 for x in buckets.get('ui',[])), sum(x>83 for x in every),
      len(buckets.get('session',[])), sum(x>0 for x in buckets.get('session',[])))
EOF
# → 1447 个被跟踪 URL / ui 内 >83 星 7 个 / 全表 >83 星 51 个 / session 有记录 83 个、非零 69 个
```

**零扩散,而且是最严口径的零。**

```sh
grep -ril 'turn-rewind'   data/plugins/ | wc -l   # 1  ← 只有它自己
grep -ril 'change-ledger' data/plugins/ | wc -l   # 0
grep -ril 'changeLedger'  data/plugins/ | wc -l   # 0  ← 它导出的服务键,无人使用
grep -ril '@anionex'      data/plugins/ | wc -l   # 0  ← 包名从未被别的条目写出
grep -ril 'rewind'        data/plugins/ | wc -l   # 24 ← 23 条是别的插件自己的名字
```

`rewind` 的 24 条必须逐条判断:去掉自身后 23 条,没有一条包含 `Anionex`、包名、服务键或本仓库 URL——它们只是**同类功能各自命名**,不是引用。所以第三方点名 **0**。
另有一处边界命中要如实记:`change ledger`(带空格)命中 2 条,除自身外是 `Ejinhouse__dsh-turn-timeline.yml:7`(自述「data reads from the session event log and the change ledger」)。它既没写仓库名也没写服务键,无法确认指的是本插件,故**不计入扩散**,列入待验证。

**怎么解释「类内头部 + 零扩散」?** 我的判断是三条,按解释力排序:

1. **它交付的是「正确性」,不是「接口」。** 回退这类东西没有可被调用的横向 ABI:别人要用,只能依赖 `@anionex/dsh-turn-rewind` 这个包本身(`ctx.changeLedger` 是**同一个包**提供的服务,`inject = ['changeLedger']` 的前提是先把整个引擎装进来,`README.md:190-207`)。**没有第二个实现能只对齐格式就互操作**,因为格式里全是本引擎的私有语义(锁、journal、rescue 链、`treeHash` 算法)。抄格式没用,抄引擎才是抄。
2. **要复制的是 10 260 行里最难的那 3 000 行。** 真正的工作量不在「按 turn 存快照」,而在这几件事同时成立:计划—确认—rescue—journal—回滚—启动对账的完整状态机(`engine.ts:618-768`)、Git 侧不碰用户 index/HEAD 的私有 index 手法(`git-checkpoint.ts:97-111,219-240`)、路径包含与「绝不递归删工作树」的闸(`path-utils.ts:118-213`)。少任何一条,做出来就是「能删错东西的回退按钮」。
3. **接入面是 DSH 版本形状的,不是存储格式形状的。** 这点很重要,也是本卡最想回答的问题:**回退并不需要与 DSH 的会话存储格式强绑定。** 插件从头到尾没读没写 DSH 的会话文件:它只读 `session.header`(`cwd`、`parentSession`、`seedLength`)、读事件数组(`turn/start.seq`、`user/message.source.kind`、`turn/end.seq`)、调 `sessionController.fork/create`。真正脆的是**事件与 DOM 的形状**:0.1.5 删 `seedLength` 换 `inheritedEventCount`、0.2.0 抽掉 chat 快照钩子、0.2.2 连 slot 参数都变——每一次都要改代码(见 `CHANGELOG.md` 各条)。**所以别人不复制它,不是因为 DSH 存储格式锁死了,而是因为:抄格式无收益(私有语义),抄引擎成本极高,而接入层每两个月就要跟着 DSH 改一次。**

它是**明星**,但不是本册意义上的**锚**:声量在类内是第一档,扩散为零。要给一个归档判断:它更像「session 类目里唯一把回退做到工程级的一份实现」,而不是「rewind-edit 已形成标准」。

## 代价与边界

- **权限边界等于宿主用户。** 插件跑在 DSH 进程里,拿到的是同一个用户的全部文件权限,不做任何沙箱(`SECURITY.md:3-5`)。它自己声明的非目标很干脆:不保护你免受同用户进程的并发修改,不提供机密性/防篡改,不恢复 Git index、refs、commit、stash、submodule、被忽略文件,不保留 xattr、ACL、属主、时间戳、硬链接拓扑(`SECURITY.md:45-51`)。
- **每轮抓取是有成本的,而且不止主会话。** 默认 `turnCheckpointTimeoutMs: 60000`、`maxFiles: 20000`、`maxSnapshotBytes: 512 MiB`、`maxFileBytes: 64 MiB`(`src/engine.ts:53-65`)。抓取按 workspace **串行**(`rewind-host.ts:320-333`),所以同一工作树上的并发会话会排队。`agent/pre-step` 对**每个** agent 都触发,包括 subagent 会话(DSH 里 subagent 会话 `header.origin === 'subagent'` 且有 `parentSession`,`dsh-tool-subagent/lib/index.js:545`),**判断:** 因此子代理的 turn 1 也会各拍一张快照并占各自的保留额度——按代码路径成立,但我没有在真机上跑过 subagent 场景的回退(见待验证)。
- **磁盘占用有两种形态。** v1 把整棵树的内容复制进 `change-ledger/blobs/`(按内容去重,但和 `.git` 是两份);v2 内容留在仓库对象库里,只多一个 sidecar manifest 和一堆私有 ref,磁盘回收交给 `git gc`(`README.md:182`)。保留额度:`maxRestorePoints: 50`(user+rescue)、`maxTurnCheckpointsPerSession: 30`;超限**报错而不是静默丢**(`engine.ts:965-970`、`README.md:178`)。
- **失败模式,按发生顺序:**

  1. **抓取失败/超时/关闭** → 这一轮没有可用点,UI 显示 skip 原因,`messages` 模式仍可用;`turnCheckpointMode: 'off'` 时每条 turn 写一条持久 skip(`engine.ts:396-431`)。**永不阻断用户这一轮**(`rewind-host.ts:218-220`)。
  2. **预览后文件变了** → `PLAN_STALE`,要重新打开弹窗(`engine.ts:1339-1348`、`:1084-1104`)。
  3. **HEAD/branch 漂移** → 默认 `HEAD_CHANGED` 阻断;预览里审核过则可放行(`rewind-host.ts:604` 把 `inspection.headChanged` 传成 `allowHeadChange`),放行也只对**这一次已审核的漂移**有效(`engine.ts:1274-1279`、`tests/engine.test.mjs:1637-1656`)。
  4. **Git 操作状态变了**(merge/rebase/cherry-pick 中) → **一律阻断**,无放行开关(`engine.ts:1268-1273`)。
  5. **目标是「当前快照没观察到、但磁盘上确实存在」的路径**(被忽略文件、submodule 边界) → `UNMANAGED_PATH_CONFLICT`,拒绝覆盖(`engine.ts:1350-1371`)。
  6. **父目录是软链 / 目标是非空目录** → `SYMLINK_PARENT` / `DIRECTORY_NOT_EMPTY`,拒绝(`path-utils.ts:129-131,186-190`)。
  7. **同一工作树有跑着的 Agent(含源会话自己)** → 预览和提交都 `WORKSPACE_IN_USE`;idle 不阻(`rewind-host.ts:567,630-636,922-941`)。
  8. **恢复中途失败** → 从 rescue 点回滚;回滚成功抛 `RESTORE_FAILED_ROLLED_BACK`,回滚失败标 `recovery-required` 并把 rescue 点留在日志里(`engine.ts:689-746`)。
  9. **崩在恢复中间** → 下次启动把非终态 journal 改 `interrupted`,但**只在没有活锁持有者时**;`listRecovery` 给出 rescue 点,人再走一次 plan/apply(`engine.ts:104-107`、`store.ts:138-145`、`SECURITY.md:41-43`)。
  10. **「恢复文件并重新开始」里 fork 失败** → 自动用本次的 rescue 点把文件补偿回去;补偿也失败 → `AggregateError`(`rewind-host.ts:648-672`)。
  11. **磁盘满 / 只读** → JSON 写入失败(`writeJsonAtomic` 的临时文件或 rename 抛),manifest 不落盘,不产生半成品条目;v2 发布失败会走 journal 回退并 `update-ref -d`(`engine.ts:180-221`)。

- **真正不可回退的东西**:网络请求、已 spawn 的进程、外部服务写入、git commit/refs/branch/index/stash、被 `.gitignore` 或 `.dsh-rewindignore` 排除的文件、submodule、xattr/ACL/时间戳,以及**会话日志本身**(append-only,只能 fork 出新会话)。还有一条容易忽略:被删文件里的附件——草稿恢复依赖 DSH 的附件存储仍在(`rewind-host.ts:1015-1063`)。
- **维护成本是真实门槛。** 三个月 110 个提交、65 个在采样点之后,`CHANGELOG.md` 的通篇主题就是「跟 DSH 版本」;兼容矩阵一篇篇手写(`package.json:65-88`),而 `tests/package-layout.test.mjs:37-58` 把这份矩阵抄成了断言——**每支持一个 DSH 发布,要同时改兼容声明、peer 范围、和那份测试**。
- **CI 只矩阵 Node,不矩阵 DSH。** `.github/workflows/ci.yml:9-26` 只跑 node 22.19/24;锁文件里 `@deepseek-ai/dsh-settings` 固定在 `0.1.5-rc.1`(`pnpm-lock.yaml:18-20`)。所以 README 那句「Compatibility is declared and exercised against DSH 0.2.2-rc.1」里的 "exercised" 指的是**人工**在 rc.1 上装了一遍(见 `CHANGELOG.md` 0.3.12 条),不是 CI 保证的。
- **UI 侧的脆弱点是明账。** portal 依赖 CSS-module 类名 `[class*="actions"]` 与 `data-chat-turn` 属性(`src/client/index.tsx:1953-1986`、`:1103`),0.2.x 路径还挂了一个 `MutationObserver(document.body)` + 1 s 重试(`:1174-1175`、`:1164-1167`)。DSH 换一次渲染类名或属性,按钮就会静默消失。

## 可信度与复现

- **★★★**:`src/` 18 个文件全部读过(逐行读的有 `engine.ts`、`rewind-host.ts`、`types.ts`、`path-utils.ts`、`index.ts`、`settings.ts`、`directory.ts` 前半、`git-checkpoint.ts` 捕获与校验段、`snapshot.ts` 抓取段、`store.ts` 初始化/锁/blob/manifest 段、`client/index.tsx` 的 slot、DOM 桥、portal、草稿恢复段);`docs/FORMAT.md`、`SECURITY.md`、`docs/IMPLEMENTATION_PLAN.md`、`AGENTS.md`、`README.md` 全读;6 个测试文件的用例清单与关键用例体;CI 与锁文件;`package.json`、`cordis.patch.yml`。
- **对照本机 DSH 0.2.1-rc.5**(`~/.nvm/.../@deepseek-ai/dsh`):`dsh-agent-loop` 的 pre-step waterfall 与 `turn/start` 顺序、`dsh-session-checkpoint-policy` 的同形钩子、`dsh-host-webserver.register`、`dsh-client-modules` 的 `dsh.client` 解析、`dsh-api-session-controller` 的 `create/fork`、`dsh-client-ui-conversation` 的 slot 清单、`dsh-client-ui-chat` 的 `data-chat-*` 属性——都是本卡允许的 DSH 侧对照证据,不是 README 转述。
- **未读**:`src/validate.ts` 全文(只读了行为与测试)、`store.ts` 的迁移/reclaim 分支(`:832-1190`)、`git-checkpoint.ts` 的 cache 与 attributes 段(`:432-810`)、`client/index.tsx` 的弹窗与设置卡渲染细节(`:1248-1940`)。所以「畸形持久状态能不能穿过校验」我只到测试覆盖的程度,没有逐条走 `validate.ts`。

```sh
# 1) 克隆与提交
git clone --depth 1 https://github.com/Anionex/dsh-turn-rewind.git /tmp/an-turn-rewind
cd /tmp/an-turn-rewind && git log -1 --format='%H %ad %s'
# → f357dad58c8f42b705c009a4ff352ec33a034e3c  Thu Nov 12 15:27:14 2026 +0800  chore(release): publish v0.3.13 (#37)

# 2) 全史(浅克隆只有 1 条;deepen 后 110 条)
git fetch --deepen=200 && git log --oneline | wc -l          # 110
git rev-list --max-parents=0 HEAD                            # c6d8a97… 2026-08-09

# 3) 代码规模
wc -l src/*.ts | tail -1                                     # 7936
wc -l src/client/index.tsx                                   # 2324
wc -l tests/*.mjs | tail -1                                  # 5033
grep -h '^test(' tests/*.mjs | wc -l                         # 149

# 4) 扩散(在 awesome-dsh-plugin 仓库根;11 744 个 yml 必须用目录形式,直接展开会 Argument list too long)
grep -ril 'turn-rewind'   data/plugins/ | wc -l              # 1(只有它自己)
grep -ril 'change-ledger' data/plugins/ | wc -l              # 0
grep -ril 'changeLedger'  data/plugins/ | wc -l              # 0
grep -ril '@anionex'      data/plugins/ | wc -l              # 0
grep -ril 'rewind'        data/plugins/ | wc -l              # 24(23 条为其他插件自身命名,逐条判断后不计)

# 5) 类目分母与类内位置
python3 _digested/ecosystem/census.py | head -6               # 总数 11744;session 914
# session 类目内按边车星标排序(912 个条目有 category: session;其中 83 个在 data/stars.json 有记录)
python3 - <<'PY'
import json,glob,re
s=json.load(open('data/stars.json')); rows=[]
for f in glob.glob('data/plugins/*.yml'):
    t=open(f,encoding='utf-8').read()
    u=re.search(r'^url:\s*(\S+)',t,re.M); c=re.search(r'^category:\s*(\S+)',t,re.M)
    if u and c and c.group(1)=='session':
        r=s.get(u.group(1).rstrip('/')); rows.append((r['stars'] if r else -1,u.group(1)))
rows.sort(reverse=True); print(len(rows), sum(1 for r in rows if r[0]>=0), rows[:3])
PY
# → 912 个对象、83 个有星标记录、[(83,'<本卡>'),(71,'…'),(42,…)]

# 6) 发布形态
curl -s https://registry.npmjs.org/@anionex/dsh-turn-rewind | python3 -c \
  "import json,sys;d=json.load(sys.stdin);print(len(d['versions']),d['dist-tags'])"   # 21 {'latest': '0.3.13'}
```

## 待验证

1. **`2373` 下载数从哪来。** 边车没记来源;npm 公开 API 只给「最近一周」,无法回填 2026-08-19。要判断真实采用量,得看 tarball 安装数或 GitHub release 下载数,本仓都没有采集。
2. **subagent / job 会话是否也各拍一份快照。** 代码路径上 `agent/pre-step` 对所有 agent 触发、`capture` 只按 `session.header.cwd` 判工作树(`rewind-host.ts:224-278`),所以应该会;但 DSH 里 subagent 会话的 `cwd`、`origin`、`inheritedEventCount` 组合是否让它们落进同一 workspace key,需要真机跑一次并数 `manifests/` 增量。
3. **`change ledger` 那条命中的性质。** `Ejinhouse/dsh-turn-timeline.yml:7` 自述读 "the change ledger",但没写仓库名、服务键或 URL。它读的是本插件的存储,还是它自己的某个账本,决定了扩散数是 0 还是 1。**它的源码本次未读。**
4. **20 000 文件 / 351 MB 的真实耗时。** 仓库内基准是 15 500 文件 / 380 928 000 字节(`docs/LARGE_REPOSITORY_CHECKPOINT_DESIGN.md:5`),README 的「237 s → 7 s」出自 0.3.5 的路径缓存。这两个数我没有复跑,也不知道在 APFS 之外的文件系统上的表现。
5. **`turnCheckpointTrust: 'fast'` 会不会漏掉内容变化。** fast 信任「索引 OID + stat + attributes + 配置栅栏」(`git-checkpoint.ts:158-177`),理论上一个既不改 mtime/size/inode 又改了内容的写入可以骗过它。这是设计上的取舍还是漏洞,要构造用例才说得清。
6. **v2 私有 ref 的清理语义。** 删除走 `update-ref -d` + 启动对账(`engine.ts:149-178`),但 ref 在 `git gc` 前会不会被 `git fsck`/备份工具当成悬空对象报出来,以及用户 `git push --mirror` 会不会把 `refs/dsh-turn-rewind/**` 推上去——未验证。
7. **16 个 DSH 版本的兼容矩阵有没有真跑。** CI 只矩阵 Node(`ci.yml:9-26`),锁文件钉在 `dsh-settings@0.1.5-rc.1`。矩阵里 0.2.0/0.2.1/0.2.2 各 rc 的「compatible」是人工验证的结论,不是可复现的自动化。
