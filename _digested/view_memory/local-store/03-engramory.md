# engramory — 索引上限是这层唯一的硬拒绝,其余全是纯 markdown 约定

> 证据等级:★★★(源码级;`tinqiao-oss/engramory@5ea1e2aae537c7f146a6a61f4ac047a39418a15f`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 160 为 2026-08-19 历史采样;下载 946 同为该日。
> 160 与 2026-11-18 实时 208 都是**仓库级**星标(主项目 + 4 个宿主适配器共用),拆解见「为什么它突出」。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `tinqiao-oss/engramory#plugin`([registry](../../../data/plugins/tinqiao-oss__engramory--adapters-dsh-plugin.yml))——monorepo 子目录 `adapters/dsh/plugin`(master) |
| 类目 | memory([census](../../ecosystem/census.py) 504 条) |
| 子分类 | `local-store`(普通 markdown,本地) |
| 自述 | 「长期记忆插件;AI 记住的事存成普通 markdown 文件;每次对话带上一份记忆目录;目录有大小上限(默认 200 行 / 25 KB),写超了会被拦下;侧栏有记忆页;同一份记忆 Claude Code、Codex 等也能用」 |
| 星标 ⚠ | **160**(2026-08-19 冻结采样,仓库级);2026-11-18 实时 **208**(同为仓库级) |
| 下载 ⚠ | **946**(2026-08-19;npm `dsh-engramory` 的当日累计下载) |
| 扩散 | **1**(口径:`grep -ril 'engramory' data/plugins/` 命中 2 条,减去自身 = 1;命中 `yffo__dsh-engramory-recall.yml`,无反例) |
| 仓库 commit | `5ea1e2aae537c7f146a6a61f4ac047a39418a15f`(2026-11-17,`master`),子目录 `adapters/dsh/plugin` 的最后一次提交(该路径累计 63 个提交) |
| 包形态 | npm `dsh-engramory@1.5.5`:Cordis **bundle**(`dsh.bundle.patch`)+ 一份运行时注册的 skill + 一个 web 客户端(设置页/记忆页)。**零依赖、零构建、纯 ESM、只 import `node:` 内置**(`adapters/dsh/plugin/index.js:24-34`);**不走 MCP**;**注册 0 个工具**(全文只有一处 `ctx.tools` 用法,是 `guard` 而非 `register`,`index.js:222`) |
| 适配层规模 | `index.js` 5064 行 + `client.js` 1715 行 = **6779 行**;测试 `index.test.js` 4976 + `client.test.js` 1544 = **6520 行**;`cordis.patch.yml` 16 行,`package.json` 84 行(命令见末节) |
| 主项目体量 | 仓库 101 个文件、master 164 个提交、36 个 release(最新 `v1.5.5`);协议本体是 `SKILL.md`(41 KB)+ `rules-snippet.md` + `PORTING.md` + `AGENT-SETUP.md`;另有 4 个宿主适配器、5 个 Python 工具、1 个 Claude Code hook |

## 它到底是什么

**它是一个多宿主「记忆协议」仓库里的 dsh 层,不是一个独立的 dsh 插件。**

仓库的结构说明了分工:根目录放协议(`SKILL.md`、`rules-snippet.md`、`PORTING.md`)与宿主无关的工具(`tools/engramory_{init,check,doctor,sync,trace}.py`),`adapters/` 下是 codex / dsh / kiro / openclaw / reader 五层,`hooks/` 下是 Claude Code 的写前 hook。DSH 这一层拿到的是仓库里最厚的一份代码(6779 行),但它的价值在于**把协议里唯一能被强制执行的那一条变成硬拒绝**,其余全部是文件约定。

### 存储模型:目录 + 索引 + 一事实一文件

```text
<记忆根>/
├── MEMORY.md          # 索引:一行一条指针,不是正文
├── 改完先跑测试.md      # 一个文件 = 一条事实
├── ...
└── archive/           # 折叠掉的旧笔记
```

- **索引不是生成的。** `tools/engramory_sync.py:1-12` 的模块 docstring 明说它「never writes MEMORY.md or any detail note」,`mark-synced` 只做确认。唯一的生成点是建库时从模板拷一份:`tools/engramory_init.py:269-276`(`_write_text_atomic(index, _read_text(template))`,注释解释为什么要原子写——拷贝中断会留下截断的索引,而后续运行会把它当「kept existing」永久接受)。所以索引**由模型按协议手写**,插件只负责注入与拦截。
- **索引的形状**由 `templates/MEMORY.md:1-29` 定义:`# Memory Index` + 一句「pointers only」+ 按类型分节(`## user` / `## feedback` / `## project` / `## reference`),每节一行一指针:标题方括号 + 相对文件名(如 `slug.md`)+ 一行钩子。`SKILL.md:326-355` 是同一份规范的正文,并明确「若某行开始承载正文,说明内容从笔记里漏出来了」。
- **每条笔记**是带 frontmatter 的 markdown,`name` / `description` / `type` / `created` / `updated`(`templates/example-feedback.md:1-19`)。`type` 七种:协议的四种 `user|feedback|project|reference`,加陪伴模式的 `moment|upcoming|self`(`index.js:795` 的 `NOTE_TYPES`)。
- **两个库**:全局库默认 `$DSH_HOME/.engramory-memory/`(`index.js:2517-2524` 解析 `$DSH_HOME`,含 `~` 展开),可整体搬到别处;项目库是 `<项目根>/.engramory-memory/`,项目根**只按 `.git` 认**(`index.js:1029-1070` 的 `projectStoreOf`),且索引必须落在真实根内、不能是符号链接(`projectIndexAsync`,`index.js:1084-1094`)。

### 注入:一条 `role: "user"` 的消息,不是 system prompt

索引进上下文的方式是 `agent/pre-step` 里追加一条消息(`index.js:408-434`),不是 runtime context。原因写在 `index.js:320-326`:dsh 把 runtime context 拼成一份快照,任何一部分变化就整份重发,而旧副本会一直留在对话里直到被压缩;注释给了实测数字——dsh 0.2.1-rc.5 上,13 步会话里出现过 6 份 20 KB 索引。消息的 `source.kind` 是 `'engramory'`(`index.js:2300-2311`),配上 `sessionProjections` 里的 `RECALL` unit 记录「最后送去的是哪一版(seq + sha256 digest)」(`index.js:2238-2256`),于是只有内容变了、或那条消息被压缩掉之后才重发(`recallFor`,`index.js:2276-2297`)。

读取本身带缓存:目录上溯结果记 10 秒,索引按 `dev:ino:size:mtimeNs:ctimeNs` 判断是否变化,且只读到上限为止(`indexRecall`,`index.js:2329-2401`;`readUpTo = min(maxBytes, readLimit)` 在 `:2332`)。

### 上限:唯一的硬拒绝

`ctx.tools.guard()` 是这层存在的理由。插件文件头 `index.js:6-12` 写明:guard 是同步的、单调的拒绝,**一旦某个 guard 返回理由,后面的 waterfall 监听器不能把它改回允许**,所以 200 行 / 25 KB 在这里能「被强制」,而不只是「被要求」。

判定规则只有一句(`verdict`,`index.js:4015-4043`):两个维度**各自**要求「既超上限、又比当前文件大」才拒。所以 210 行的索引可以用一次 205 行的整文件重写继续压缩,永远不会被锁死。行数不算尾部换行,正好卡在上限还能写。

## 怎么接进 DSH

**① 两份 manifest,一份给 dsh,一份给爬虫。**

- 插件自己的 `package.json`: `dsh.bundle.patch → ./cordis.patch.yml`,另加 `dsh.client`(`platform: "web"`,inject 两个客户端包 `@deepseek-ai/dsh-client-locale` 与 `dsh-client-ui-plugin-manager`),以及一份逐版本的 `dsh.compatibility.dshReleases` 白名单(17 个版本标 `compatible`)。
- 仓库根还有一份 `"private": true` 的同名 `package.json`,只是发现清单(`package.json:2-10` 的 `"//"` 字段自述,`:21-24` 是 `dsh.bundle.patch`):registry 爬虫会在**仓库根**找 `dsh.bundle`,所以根清单声明同一个 patch 文件。`tests/test_dsh_plugin.py:79-105` 把「两份清单的 name/version/patch 必须同步」钉成断言。

**② patch 只有一行,但注释比配置长。** `cordis.patch.yml:10-16`:`id: engramory`、`name: dsh-engramory`、`config: {indexName, maxLines: 200, maxBytes: 25600}`。文件头 `:1-8` 说了两件容易踩的事:patch 会**整体替换**目标行的 `config`,所以覆写时要列全想保留的键;200/25 KB 是协议的常量,不是移植者的意见,放在这里是为了让部署能改而上游不用改代码。

**③ 事件与注册点。** 逐条指到行:

| 接缝 | 位置 | 干什么 |
|---|---|---|
| `ctx.tools.guard()` | `index.js:222-234` | 上限闸门(外加社交模式的陌生人过滤、搬家期的写入冻结) |
| `fs/write-intent` / `fs/edit-intent`(`prepend`)| `index.js:240-251` | 搬家时再判一次;选这两个钩子是因为 dsh 的文件工具可能在调用内等用户批准沙箱,guard 通过之后才真正落盘(`index.js:235-239`)|
| `agent/pre-step`(`prepend`)| `index.js:410-422` | 把索引消息追加进本轮 `messages`;`decision.kind === 'reject'` 或信号已中止时不动 |
| `agent/request-error`(`prepend`)| `index.js:423-433` | 因超长被压缩后重试时,补回被压缩吃掉的那一份 |
| `system-prompt/assemble`(`prepend`)| `index.js:479-495` | 记录本轮装配是否真的收下了插件的 context(决定下一步能不能发索引消息),并修 dsh 0.1 丢掉 `interpolate: false` 后 `{{` 被当模板变量的问题 |
| `ctx.inject(['skills'])` → `skills.register` | `index.js:265-294` | 注册内置 skill(名字 `engramory`,`source: 'runtime'`),不依赖安装路径 |
| `ctx.inject(['systemPrompt'])` → `systemPrompt.context` | `index.js:496-516` | 注册 runtime context(`interpolate: false`,`order` 300) |
| `ctx.inject(['connection'])` → `connection.fetch.register` | `index.js:551-570` | 4 条 HTTP 路由:`/api/engramory/{settings,memory,store,store/pick}` |
| `ctx.inject(['sessionProjections'])` → `register` | `index.js:190-213` | 两个 host-only projection:`engramory:recall`(索引版本)、`engramory:speakers`(谁说过话) |

**④ 依赖是零,可选服务是全部。** `export const inject = ['tools']`(`index.js:45`)是唯一硬依赖,注释 `:38-44` 解释为什么不用 `{required, optional}` 形态:dsh vendored 的 Cordis 会把那个对象当成两个叫 `"required"`/`"optional"` 的服务,插件永远 pending(issue #8)。`skills` 故意不声明,因为「上限必须在一个没有 skill registry 的 profile 上也挂上」,所以 `apply()` 里用 `ctx.inject` 反应式探测。同样的写法用在 `workingDirectory`(`:148-167`)、`sessionProjections`、`agents`、`configEditor`、`workspaceRegistry`/`sessionController`/`directoryPicker`(`:530-542`)、`connection`、`tokenMeter`/`compaction`/`llm`。

**⑤ 客户端三个 slot。** `client.js:1693-1711`:`plugins.bundle.config`(插件页里的设置页)、`main` + `sidebar.panellist`(记忆页与侧栏入口,`order: 20`,注释说明排在 dsh 自己的 Plugins 0 / Automations 10 之后)。`client.js:1-14` 说清它为什么是 plain script:React 从页面的 module table 取,不加载任何 Harness 客户端包(「they change without notice」),颜色走宿主主题 token。

**不走 MCP。** 仓库 README 的「为什么这样做」直接写:对能读写文件、能加载常驻规则的宿主,MCP 会多出一条绕过写前上限的写入通道,还会把「每次都加载的索引」降级成「模型得记得去调用的工具」。源码层面一致:整个插件没有注册任何工具。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `adapters/dsh/plugin/index.js` | 5064 | 宿主半边:闸门、召回、skill、4 条路由、store 搬家 | `:98` `apply()`;`:222` guard;`:3888` 闸门主体;`:2329` 召回;`:2276` 发送决策 |
| `adapters/dsh/plugin/client.js` | 1715 | 浏览器半边:设置页、记忆页、侧栏图标 | `:1681-1713` slots;`:1577` 记忆页 |
| `adapters/dsh/plugin/index.test.js` | 4976 | 232 个 `node --test` 用例,把闸门判定表逐行钉住 | 决策表见下 |
| `adapters/dsh/plugin/client.test.js` | 1544 | 51 个用例,页面与路由契约 | — |
| `adapters/dsh/plugin/cordis.patch.yml` | 16 | 唯一 manifest | `:10-16` |
| `hooks/engramory_index_guard.py` | 389 | Claude Code 的同类闸门(`PreToolUse`);dsh 侧的规则镜像自它 | `:56-58` 四个上限环境变量;`:341` `deny` |
| `tools/engramory_init.py` | 1875 | 建库 + 给各宿主写规则文件;DSH 走 `dsh` 子命令 | `:269-276` 索引从模板原子落盘 |
| `tools/engramory_check.py` | 143 | 无 hook 宿主的降级:跑完自己查 | `:1-21` 三层降级说明 |
| `tools/engramory_doctor.py` | 816 | 结构 + schema 体检(坏指针、孤儿、重名、超限) | `:17-46` |
| `tests/dsh_e2e/run.py` | 650 | 真 dsh 上的 e2e(装 dsh → 装插件 → 假模型跑 7 步) | 见下 |

**写入路径(闸门)。**

```text
model 调 write/edit/str_replace_editor
  └─ ctx.tools.guard(exec)                       index.js:222
       ├─ 社交模式陌生人过滤(refuseStranger)      :1827  (仅 social)
       ├─ 搬家冻结(refuseMoving)                 :2797
       └─ refuseOversizedIndex                   :3888
            ├─ gatedWrite(tool,args)?            :3911  只认 write/edit/str_replace/insert/str_replace_editor 的写命令
            ├─ 每个被点名的路径都判(file_path + path):3903
            ├─ 是索引吗?按写入实际落到的文件身份判(跟随符号链接;有 indexPath 时按 inode 比较) :3928-3941
            └─ verdict(text, current)            :4023
                 ├─ 行数:> maxLines 且 > 当前行数 → 拒
                 └─ 字节:> maxBytes 且 > 当前字节 → 拒   (:4036-4042)
```

几个只有读代码才知道的细节:

- **局部编辑要先算出结果再判。** `edit` 的 `old_string`/`new_string` 与 `insert` 会被 `simulateEdit`/`simulateInsert` 重放(`index.js:4106-4245`),再按整文件规则判。注释 `:4097-4105` 解释为什么两种参数名都要读:dsh 的 `edit` 只认 `old_string`,而 `str_replace_editor` 认 `old_str`,只读一种就会让另一种当诱饵。
- **非 UTF-8 的当前文件不能伪装成「变小」。** 当前字节数取自原始 buffer 而不是解码后的字符串(`index.js:4026-4034`),否则坏字节被解成 3 字节 U+FFFD,一个真实增长的写入会看起来像收缩。
- **guard 意外异常一律放行**(`index.js:229-233`);社交模式的陌生人过滤是唯一 fail-closed 的分支(`:1870-1873`,catch 里也返回拒绝理由)。
- **读操作永不被拒。** `index.js:19-22` 的注释记录过一次真实教训:第一版把所有点名索引的调用都拦了,结果在**最需要压缩的时候**连读都读不了。

**召回路径。**

```text
step 组装 → system-prompt/assemble 记 assembled[session] = 本轮是否收下 memory context
        → agent/pre-step → recallFor(:2276)
             ├─ roleOf(agent) === 'owner'?          (social 下可能是 stranger)
             ├─ indexRecall(:2329): 全局库 + 项目库(或 pinned),各自 stat 判变化,只读到上限
             └─ digest 与 RECALL 里记的一致 → 不发;否则发一条 role:"user",source.kind:"engramory"
```

`renderIndex`(`index.js:3840-3861`)负责「超限不带上」的那一半:按整行切到上限内,再加一句告诉模型为什么被截、该压缩。注释 `:3851-3859` 区分了两种截断——行数触顶是「该压缩的越界」,读不到底则是「读的上限」,两者给的提示不同。

**搬家(store move)。** 这是插件里唯一的加锁逻辑,也是它最复杂的部分:`prepared → staged → published → committed → detached` 五步,每步先写 journal(`index.js:2556-2566`),下次 dsh 打开时按 journal 续做或回滚(`resumeMove`,`:3770`;启动后 3 秒第一次、之后每分钟,`:576-585`)。锁是 `wx` 创建的 `$DSH_HOME/.engramory-memory.lock`,`staleLock` 判定覆盖三种情况:超过 15 分钟、pid 已不存在、以及「锁文件写了一半」(30 秒内没有补全就算撕裂)(`:3697-3754`)。搬家期间对两个位置的写入都被拒,并在拒绝里告诉模型新位置(`refuseMoving`,`:2797-2812`)。

## 为什么它突出

**先把星标拆掉。** GitHub 星标是仓库级的,而 registry 把 `tinqiao-oss/engramory` 的 160 记在它的一个**子目录条目**上。时间线是决定性的:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-06-13 | 仓库创建 | GitHub API `created_at` |
| 2026-08-15 | `3542b7e6 feat(dsh): dsh-engramory — the index cap as a real refusal, not a request` —— `adapters/dsh/plugin` 的**第一个**提交 | `commits?path=adapters/dsh/plugin` |
| **2026-08-19** | **⚠ 160 星 / 946 下载的采样点** | 边车 |
| 2026-11-17 | `5ea1e2aa` 最后一个提交(`1.5.5` e2e,3/3 通过);`v1.5.5` release | clone + API |
| 2026-11-18 | 实时 **208** 星 | GitHub API |

采样点距 DSH 子目录的第一个提交只有 **4 天**,距建仓 **67 天**。所以 **160 星里能归给这一层的,至多是 4 天的增量**;协议本体、Python 工具、Claude Code hook、以及 2026-06-13 到 2026-08-15 之间积累的东西,都不在这层。**判断:160 应记在主项目名下。**

实时值 208 是另一个方向的证据,但只到「可能」为止:164 个提交里有 **63 个**碰 `adapters/dsh/plugin`(38%),2026-08-19 之后的 48 星大概率由 DSH 适配层带动。**但这只是推断**——没有 stargazers 时间戳就无法证明(见「待验证」)。

**再看扩散,1 条,拆开看性质。** `yffo/dsh-engramory-recall` 自述「本地 BM25 自动召回、写入闸门、静态体检与记忆面板」,README 明说「借鉴了 Engramory 协议(MIT)『一事一文 + 索引当小抄 + 索引有硬上限』的路子」,并且「检索、注入、账本、写入闸门、归档、体检、面板、MCP 全部自研,与上游没有共享代码」。它自己的 `docs/format.md` 更直接:

- 它维护一份**自己冻结的 Format v1**,并附一张「与上游规范的差异」表(`docs/format.md:107-113`):笔记文件名是 `<kind>-<slug>.md`(上游是 `<slug>.md`,type 只在 frontmatter)、`created`/`updated` 可选(上游必填)、索引上限的守卫**自研**、口径从上游的「只拒绝增长」改成「拒绝写入」。
- 它的默认库是 `~/memory/engramory`(`cordis.patch.yml:15`),不是 `~/.dsh/.engramory-memory`;README 与 `docs/*.md` 里**没有任何一处**提到 dsh 的库路径。
- 它只读库(`store.js:1-5` 的契约「本模块**绝不写入**记忆库」),读的时候扫目录里所有 `*.md`(`store.js:79`),所以能读任意 markdown 记忆库;但它的写入闸门按自己的命名规则拒(`guard.js:31` 的 `NOTE_FILE_RE`),上游那种 `改完先跑测试.md` 的名字会被它自己拒掉 —— **判断:读侧兼容,写侧不兼容,两者不能共用一个库同时还开着它的闸门**(这一点我没有实跑,属源码推断)。

**所以「存储约定」是不是接口?** 是**可读的范本,不是可链接的接口**。证据有三条:① 唯一衍生者的做法是「照文档重写一份」,不是引用、不是依赖、不是插件组合;② 它重写时立刻改了文件名约定并声明「不声称二进制兼容」——说明这套约定没有版本协商、没有 schema 校验、没有共享代码,只有一段被读懂的文字;③ 上游自己也没打算让它成为 ABI:`tools/engramory_sync.py` 直言不生成索引,`engramory_check.py:1-21` 把「没有写前 hook 的宿主」列为需要人工补的第三层。

**为什么它能被复用,却只被复用了一次。** 复用价值在**阅读成本**上:一个目录 + 一个索引文件 + 一行一指针,任何人打开文件管理器就能看懂,不需要协议栈、不需要 schema 迁移、不需要跑服务。这是它和「把记忆塞进 SQLite 或依赖某个框架运行时」的做法最根本的差别——后者的数据模型藏在代码里,前者写在文件名和 frontmatter 里。但**能被看懂**不等于**能被接上**:复用它的人要先读懂 41 KB 的 `SKILL.md`,再自己实现一遍闸门和召回,产出的是一个**新插件**而不是一个**集成**——门槛刚好高到只剩一个人做了。**判断:这是「约定强、接口弱」的典型形态,扩散数会长期停在个位数。**

还有一条它自己的证据说明这不是随手做的移植:`tests/dsh_e2e/` 是**真 dsh 上的 e2e**,README 开头 `:1-7` 解释了为什么必须有它——`node --test` 只能对着 mock 钉住判定,钉不住「某个 dsh 版本还把文件工具叫 `write`/`edit`、还经过 `ctx.tools.guard()`、还列出 skill」;这些一旦变了**不会报错,只会静默失去上限**。`results.json` 里累计 **460 次运行全部 pass**,最新一批是 1.5.5 在 0.1.5-rc.3 到 0.2.2-rc.3 上、`repo` 与 `npm` 两种来源各跑一遍。

## 代价与边界

- **上限只挡得住 dsh 的文件工具。** `gatedWrite`(`index.js:3911-3917`)是一个硬编码的工具名集合:`write`、`edit`、`str_replace`、`insert`,加 `str_replace_editor` 的三个写命令。shell 重定向、`node -e`、MCP 文件工具、外部编辑器、别的插件的写全部绕过。`SKILL.md:678-704` 把保证分成三层:Claude Code 的 `PreToolUse`、dsh 的 `ctx.tools.guard()`、Codex 的生命周期提醒,并明说 dsh 这一层「the same bypasses apply」、纪律层「best-effort guidance, not a hard-enforced contract」。
- **索引是模型手写的,没有重建通道。** 插件不生成也不修索引;写坏了只能靠 `tools/engramory_check.py`(写完自己查)或 `tools/engramory_doctor.py`(结构 + schema)。记忆页的体检只报告、不改文件,还自带四个「不做」的出口(索引已超限、要核对的太多、有文件读不了、只按文件名和链接判断)(`checkUp`,`index.js:1223-1300`)。
- **并发没有锁,这是设计上的。** `SKILL.md:702-705` 直说:hook 先读索引、预测、再决定,**没有加锁**,两个 agent 同时更新同一个索引会丢更新或撞上 check-then-write 的竞态;`adapters/reader/README.md:10-12` 把它上升成「单写者 / 多读者」的不变量。插件里唯一的锁(`.engramory-memory.lock`)只保护**搬家**,不保护写入。
- **失败模式,按发生顺序:**

  1. **索引名撞车。** 不设 `indexPath` 时,任何叫 `MEMORY.md` 的文件都会被判(`index.js:3936`);一个无关项目的 `MEMORY.md` 会被拒,而且用户看不出为什么。拒绝话术里带了出路(`notMyIndexHint`,`:4073-4079`),但仍然是「无关文件被拦」。
  2. **guard 自身出错 → 放行。** `index.js:229-233` 的 catch 返回 `undefined`。注释的理由是「宿主多半也执行不了这个编辑」,代价是上限在这一步不存在。
  3. **索引大到读不完 → 只按字节判。** 读取上限是 `min(16 MiB, max(1 MiB, 4 × maxBytes))`(`index.js:59-60,137`);超过就只按文件系统大小比字节,行数维度退化成 `Infinity`,局部编辑直接放行(`index.js:3957-3961`)。
  4. **局部编辑算不出结果 → 只拦「已经超限」的。** `index.js:3980-3992` 的逻辑是:索引已经超了就拒绝「盲目修改」,但拒绝话术必须同时给出出路(「用整文件重写压缩,收缩永远放行」),否则读者会以为死锁。
  5. **搬家期间写不进去。** 搬的那几秒所有对两个位置的写都被拒,只协调 dsh 自己的写入;shell、编辑器、别的 AI 同时写会漏(`refuseMoving` + README 的已知限制)。
  6. **搬家中断。** journal 逐步骤落盘,未切换就撤销、已切换就续做;切换后旧位置清理失败会让插件每分钟重试(`index.js:576-585`),记忆页会一直显示「已搬完、旧的还没清」。
  7. **社交模式 fail-closed。** 认不出说话人时一律当陌生人(`refuseStranger` 的 catch,`index.js:1870-1873`):宁可主人的会话拿不到记忆,也不漏给别人。代价是 dsh 以后新增的消息种类,在插件认识之前都会被当成外人。
- **数据/隐私。** 明文,带本机细节。全局库默认在 `~/.dsh`,项目库必须 git-ignore(README 明说放在项目的 git 仓库里必须忽略)。社交模式**不是安全边界**,README 自己写清:shell 照样能读任何文件,同一账户下的另一个 profile 也读得到;自定义的 `skill` 配置会原样发给所有会话,包括陌生人。
- **实验性功能不承诺小版本稳定。** 陪伴模式、社交模式、设置页、记忆页、搬家在 minor 版本里也可能改(README「已知限制」末条)。
- **维护成本集中在版本跨度上。** 一个 5064 行的单文件,要同时兼容 `0.1.5-rc.3` 到 `0.2.2-rc.3` 的行为差异(0.1 丢 `interpolate: false`、0.1 没有 `workingDirectory`、0.2 的 `cd`、0.2.2 的 fiber 形态),每一处都在注释里点名了具体版本。`dsh.compatibility.dshReleases` 白名单之外「未经验证」,但 `engines.dsh` 只写下限,新版本不会拒装 —— 装上去可能可用,也可能静默失去上限,这正是 e2e 存在的理由。

## 可信度与复现

证据等级 ★★★:DSH 适配层的全部代码读过(`index.js` 逐节、`client.js` 的注册与页面段、两个测试文件的方法名与断言清单、`cordis.patch.yml`、插件与仓库根两份 `package.json`、插件与仓库根两份中文 README),协议侧读了 `SKILL.md` 的关键章节(§0/§3/§8/§9)、`templates/MEMORY.md`、`example-feedback.md`、`tools/{init,sync,check,doctor}.py` 的 docstring 与关键函数、`adapters/reader/README.md`、衍生者的 `README.md`/`docs/format.md`/`store.js`/`guard.js`/`cordis.patch.yml`、`tests/dsh_e2e/README.md` 与 `results.json`。**未读**:`engramory_init.py` 1875 行里的宿主写入细节、`engramory_doctor.py` 的 schema 校验主体、`client.js` 的渲染实现、`hooks/engramory_index_guard.py` 的匹配逻辑主体、`README.en.md`。凡涉及这些的判断都在正文里标了「判断:」。

```sh
# 1) 克隆与提交
git clone --depth 1 --filter=blob:none https://github.com/tinqiao-oss/engramory.git \
  .work/mine/cards/engramory/repo
cd .work/mine/cards/engramory/repo
git log -1 --format='%H %ad %s'
# → 5ea1e2aae537c7f146a6a61f4ac047a39418a15f Tue Nov 17 19:05:01 2026 +0800
#   test(dsh): e2e of the published dsh-engramory@1.5.5 on 3 representative dsh releases, 3 of 3

# 2) 适配层规模
wc -l adapters/dsh/plugin/index.js adapters/dsh/plugin/client.js        # 5064 + 1715 = 6779
wc -l adapters/dsh/plugin/index.test.js adapters/dsh/plugin/client.test.js  # 4976 + 1544 = 6520
grep -c '^test(' adapters/dsh/plugin/index.test.js                      # 232
find . -path ./.git -prune -o -type f -print | wc -l                    # 101

# 3) 扩散(在 awesome-dsh-plugin 仓库根)
grep -ril 'engramory' data/plugins/ | wc -l                              # 2(含锚自身)
grep -ril 'engramory' data/plugins/                                      # 另一条是 yffo__dsh-engramory-recall.yml

# 4) 子目录历史与星标归属(2026-11-18 查)
curl -s "https://api.github.com/repos/tinqiao-oss/engramory" \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['created_at'],d['stargazers_count'])"
# → 2026-06-13T14:15:28Z 208
curl -s "https://api.github.com/repos/tinqiao-oss/engramory/commits?path=adapters/dsh/plugin&per_page=100" \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(len(d),d[-1]['commit']['author']['date'])"
# → 63 2026-08-15T10:56:52Z   ← 第一个 DSH 提交,距 2026-08-19 采样点 4 天

# 5) 边车(冻结 2026-08-19)
python3 -c "
import json
s=json.load(open('data/stars.json'));d=json.load(open('data/downloads.json'))
k='https://github.com/tinqiao-oss/engramory/tree/master/adapters/dsh/plugin'
print(s[k],d[k])"
# → {'stars': 160, 'checkedAt': '2026-08-19'} {'downloads': 946, 'checkedAt': '2026-08-19'}

# 6) DSH 侧机制核实(本机安装的 dsh)
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh
grep -n 'monotonic guard\|First monotonic denial' \
  $DSH/node_modules/@deepseek-ai/dsh-tools/lib/index.js            # :3008, :3023
grep -rn 'fs/write-intent' $DSH/node_modules/@deepseek-ai/dsh-tool-fs/lib/index.js  # :607
```

## 待验证

1. **160 → 208 的星标里有多少来自 DSH 层**:需要 `GET /repos/.../stargazers` 带 `Accept: application/vnd.github.star+json` 拿 `starred_at`(未授权 401,本次未取)。拿到曲线才能把「2026-08-15 之后新增」的部分和 DSH 适配层对上,否则只能是推断。
2. **946 下载的口径**:边车没有说明这是日/周/月下载。`dsh-engramory` 在 2026-08-19 时只发布了 4 天,946 这个数要么是累计、要么是窗口值,两种含义对「采用率」的判断差一个量级;需要用 npm registry 的 `downloads` 端点复算。
3. **衍生与上游能否真共用一个库**:`yffo/dsh-engramory-recall` 的读侧扫 `*.md`、写侧按自己的 `NOTE_FILE_RE` 拒。我没有实跑「把 `storePath` 指向 `~/.dsh/.engramory-memory` 再用它写一条」,所以「写侧不兼容」是源码推断。跑一次就能确认。
4. **社交模式的陌生人判定在真实 dsh 上的行为**:`speakerOf`/`companionRoles`/`commandWindow`(`index.js:1571-1780`)只读了结构,没有构造真实的多来源会话验证。这是插件里最容易出安全语义错误的一块。
5. **索引上限的判定表在 dsh 0.2.2 之后的版本是否仍成立**:e2e 覆盖到 `0.2.2-rc.3`(2026-11-17),`package.json` 的白名单也止于此。本机 dsh 已是更高版本,未对它跑过 e2e。
6. **`engramory_init.py dsh` 建出的库与插件自建库的差异**:插件用 `homeState()` 找 `$DSH_HOME/.engramory-memory`,init 工具按 `--project-root` 写规则文件;两者是否总落在同一个位置、`--install-skill` 路径下和插件内置 skill 会不会重复,未逐行核对。
7. **搬家在真实文件系统上的原子性**:五步 journal + 逐文件哈希比对 + 冲突留 `.old-<n>`(`index.js:3489-3601`)读起来是完整的,但 `publish`/`detach` 用 rename,跨设备时会退化成 copy+delete,这一分支未实跑。
