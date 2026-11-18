# dsh-annotation — 批注块本质是一段纯文本提示词,气泡里"看不见"是发完从 DOM 剪掉的

> 证据等级:★★★(源码级;`omdsh-dev/dsh-annotation@48eac63badf93641f2276b8b0068f6ebbe22ba9b`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 76 为 2026-08-19 冻结采样,下载边车无记录(同日采样缺口);2026-11-18 实时星标 **169**(GitHub API),两者不可混用。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `omdsh-dev/dsh-annotation`([registry](../../../data/plugins/omdsh-dev__dsh-annotation.yml)) |
| 类目 | ui(2351 条;[census](../../ecosystem/census.py));子分类 [enhance-shell](README.md) |
| 自述 | 「选中文字→批注→随消息发送,回复按批注逐条对照」。源码比自述多两件事:批注块发完要从**用户气泡**里剪掉,回复里的 `Annotation N` 要换成可悬浮芯片 |
| 星标 ⚠ | **76**(2026-08-19;仓库 2026-08-10 建,即建仓第 9 天);**实时 169**(2026-11-18 API `stargazers_count`);⚠ 值是建仓第 9 天的数,实时值已比它高 122% |
| 下载 ⚠ | 边车无记录(2026-08-19 采样缺口);npm 包存在但下载量未被采集,不能当"无使用" |
| 扩散 | **7 个同名独立实现**(口径:`grep -ril 'dsh-annotation' data/plugins/` 命中 8,减自身 = 7;逐条人工判定都不是本仓 fork);更宽的 `annotation` 口径命中 **84**(减自身 83) |
| 仓库 commit | `48eac63badf93641f2276b8b0068f6ebbe22ba9b`(2026-11-03,`Merge pull request #94 from omdsh-dev/codex/ci-efficiency-2026-11-03`) |
| 仓库 | 建仓 2026-08-10(API `created_at`),**152** 个提交、10 个 tag、**17 forks**、20 open issues、HTML、8471 KB;push 到 2026-11-03 |
| 包形态 | npm `@changfenhuang/dsh-annotation@1.4.11`(npm 侧 2026-08-24 首版、2026-10-01 最后发布、14 个版本);`dsh.bundle.patch` 一行 insert + `dsh.client` 声明;Node 半为空实现 |
| 代码规模 | `client.js` **2870** 行 + `src/index.ts` **9** 行 = 2879;测试 19 文件 2308 行(其中 `node --test` 单测 13 文件 1331 行);`site/` 1.9 MB 构建产物。口径:`wc -l client.js src/index.ts test/*` |

## 它到底是什么

**纯浏览器端插件**,不是适配层也不是配置包。Node 半只有 9 行空实现,唯一的正文是"真实功能在 client.js(浏览器 bundle)"(`src/index.ts:1-9`,编译产物 `lib/index.js:1-6` 逐字相同)。整张卡描述的机制全部发生在一个 2870 行的 DOM 脚本里。

核心循环五步,每一步都不经过 DSH 的任何结构化接口:

1. **选区**用浏览器 Selection API 抓,锚点用宿主渲染出来的 `data-chat-anchor-key` 属性 + 字符偏移。
2. **批注**攒在内存数组里,再镜像进 `localStorage`(按会话 id 分键)。
3. **发送**时把批注列表序列化成**一段纯文本**,`setDraft()` 写进宿主输入框草稿,和用户问题拼成同一条消息。
4. **发完**在微任务阶段把这段文本从用户气泡的 DOM 里剪掉,贴一个「批注 ×N」标签。
5. **回复**里只要模型写出 `Annotation N:`,就把这个标签换成芯片,内容回查"最近一条带标签的用户消息"。

第 3 步是关键判断:**批注不是字段,是提示词**。消息正文长这样(`client.js:1890-1903` 拼装,`client.js:200-207` 文案):

```
我批注了以下 2 处内容（编号与原文对应），请针对它们回答我的问题：

1. 原文A
   批注：note A

2. [docs/a.md]
   原文B

请用「Annotation 1：…」到「Annotation 2：…」的格式，逐条回应上面每一条批注，最后再回答我的问题。

提问：
<用户输入的问题>
```

`sourcePath` 存在时引文前加 `[路径]\n`(`client.js:478-480`)。拼稿是 `shell.setDraft(block + '\n' + draft)`(`client.js:1962-1963`)——所以模型收到的 prompt 第一条就是这句话,而用户在气泡里看到的只有问题。**模型是序列化器,也是反序列化器**。

数据模型只有一个数组(`client.js:1070-1081` 声明,`client.js:2016-2030` 构造),每条批注:

| 字段 | 含义 | 是否落盘 |
|---|---|---|
| `id` | `q-<base36 时间>-<4 位随机>` | 是 |
| `text` / `note` | 引文与批注正文(note 可为空 = 仅标记) | 是 |
| `sourceUrl` / `sourcePath` | 侧栏文件预览的来源(`dsh-resource://file/session/<sid>/<path>`) | 是 |
| `range` | 捕获时的 live `Range`(cloneRange) | **否**,`stringifyPendingQuotes` 直接丢弃(`client.js:957-969`) |
| `seqKey` | 宿主消息锚 `data-chat-anchor-key` / `data-focus-anchor-key` | 是 |
| `textOffset` | 该行 `textContent` 内的字符偏移 | 是 |
| `ctxBefore` / `ctxAfter` | 偏移前后各 24 字上下文 | 是 |
| `rowHead` | 行首 24 字(行锚后备) | 是 |

## 怎么接进 DSH

**① manifest 是"bundle patch + client 声明"两段**,没有自定义字段:`package.json:46-58` 里 `dsh.bundle.patch = ./cordis.patch.yml`,`dsh.client = { inject: [ui-session, ui-conversation, locale], platform: web }`;`exports["./client"] = ./client.js`(`package.json:13`)是浏览器半的入口。

**② 真正被 loader 读的是 3 行 patch**(`cordis.patch.yml:1-3`):

```yaml
- insert:
    - id: dsh-annotation
      name: '@changfenhuang/dsh-annotation'
```

`id` 与包名可以不同,但 `name` **必须是可解析的完整包名**——首版踩过:提交 `4289613` 的标题就是「bundle patch name 必须用完整包名(loader 靠它解析 client 路径)」。

**③ 浏览器半自己注册**:`window.__ModuleLoader__.load({ id: '@changfenhuang/dsh-annotation', factory })`(`client.js:48-52`)。`id` 必须与 `package.json` 的 `name` 逐字相同,否则宿主抛 `bundle ... loaded without registering "<id>"`(对照本机 DSH 0.2.1-rc.5:`node_modules/@deepseek-ai/dsh-client-modules/lib/client.js:874`)。`dsh.client.inject` 只保证这三个 ui 包**先到达**(`client-modules/lib/client.js:789-791` 按 `inject` 做 arrival 排序),不向 factory 注入任何东西——`factory: (require) => ...` 里 `require` 全程没用到。

**④ 服务依赖 4 个**(`client.js:2864-2866`):`exports.inject = ['sessions', 'conversation', 'locale', 'uiSession']`;`uiSession` 另有一层惰性探测 `ctx.get('uiSession')`(`client.js:996-1001`)。

**⑤ 实际用到的宿主 API 只有两类**:

| API | 调用点 | 用途 |
|---|---|---|
| `sessions.list` / `.subscribe` / `.scope(id)` | `client.js:1047`、`client.js:2805-2820` | 找当前会话、监听切换 |
| `ctx.conversation.input.for(scope)` → `.state.getSnapshot().draft` / `.setDraft()` / `.state.subscribe()` / `.submit('queue')` | `client.js:1962`、`client.js:1408`、`client.js:2315` | 读草稿、拼稿、纯批注直发、监听"草稿有→空" |
| `ctx.locale.getSnapshot()/subscribe()` | `client.js:2754-2779` | 三语文案实时切换 |

`setDraft(text: DraftInput)` / `submit(mode?)` 是宿主公开契约(`dsh-client-ui-conversation/lib/types/client/input/facade.d.ts:110,178`),不是模拟点击——这是它接入面里唯一"官方"的一段。

**⑥ 它明确不做什么**:不注册 slot、不注册工具、不加 HTTP 路由、不替换 provider、不改宿主文件。全仓 `grep -n 'ctx\.' client.js` 只命中 `ctx.sessions` / `ctx.conversation` / `ctx.locale` / `ctx.get`(其余 `ctx.before` / `ctx.after` 是打分函数的局部变量)。DSH 唯一的会话级扩展点是**整视图**注册(`ConversationViewRegistry.register()`,`dsh-client-ui-conversation/lib/types/client/conversation/view-registry.d.ts:1-15`),没有"给单条消息加装饰"的槽——所以消息级功能只能走 DOM。它依赖的宿主属性都能在本机 0.2.1-rc.5 里找到:`data-chat-flow-kind`(19 处)与 `data-chat-anchor-key`(5 处)在 `dsh-client-ui-chat/lib/client.js`,`data-textpreview-url` / `data-document-markdown` / `data-code-preview` / `data-textpreview-plain` 在 `dsh-client-ui-sidebar-documentpreview/lib/client.js`,`data-composer-input` 在 `dsh-client-ui-conversation/lib/client.js`。

**⑦ 安装与迁移**:`dsh plugin --profile web add @changfenhuang/dsh-annotation`;README 明令**不要**再往 profile 的 `cordis.patch.yml` 插同一个 id(`README.md:91-98`),自检是 `dsh --profile web --dump-config | rg "id: dsh-annotation"` 恰好 1 行。包名 1.4.2(2026-08-24)从 `@omdsh-dev/dsh-annotation` 改为 `@changfenhuang/dsh-annotation`(`CHANGELOG.md:91`),旧装法会在 profile 里留一条旧名条目,得手删。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `client.js` | 2870 | 全部功能:选区、工具条、编辑卡、标记层、胶囊、拼稿、剪气泡、回复芯片、i18n、清理 | 见下五个小节 |
| `src/index.ts` | 9 | Node 半空实现(只为 `dsh.bundle` 有个可加载入口) | `5-9` |
| `package.json` | 63 | `dsh.bundle` / `dsh.client` / `exports["./client"]` | `13,46-58` |
| `cordis.patch.yml` | 3 | 唯一一条 insert | `1-3` |
| `test/*.test.mjs` | 13 文件 1331 行 | `node --test` 单测:从 `client.js` 正则抽函数体、塞进 `Function` 沙箱跑 | `test/message-block.test.mjs:4-33` |
| `test/*-browser.mjs` | 5 文件 550 行 | Playwright + 假 `__ModuleLoader__` 加载真 `client.js` | `test/overlay-browser.mjs:1-20` |
| `test/host-enter.e2e.ts` | 427 | 真宿主 e2e:脚本化 LLM + 断言实际 RPC/JSONL | `test/host-enter.e2e.ts:330-380` |
| `docs/plans/`, `docs/testing.md` | 16 KB | 侧栏文件批注的验收记录与 CI 口径 | — |
| `site/` | 1.9 MB | GitHub Pages 产品页(Vite 构建产物),与插件运行无关 | — |

### 1. 选区捕获:只要"助手行内"或"文件预览内"的文本

- 监听 `selectionchange`,过滤掉输入框、工具层、浮层内的选区(`client.js:1201-1211`),再要求 `annotationRootOf()` 能解析出一个根:文件预览走 `documentSourceOf`,否则必须落在助手行(`client.js:434-455`)。
- **250 ms settle** 后才弹工具条,回调里重新校验选区键、根、来源、会话 id(`client.js:1171-1247`)。选区键是 `(同节点?1:0):startOffset:endOffset:长度`,不是哈希(`client.js:1171-1176`)。
- 助手行判别有三套并行:新版 `[data-chat-flow-kind="assistant-step"]`、旧版 `[data-time-hover-root]` 且不含 `[class*="bubble"]`、focus-chat 的 `[data-focus-flow]` + class 含 `assistant`(`client.js:362-432`)。
- 文件预览的来源只接受 `^dsh-resource://file/session/([^/]+)/(.+)$`,并校验会话 id 与当前会话一致、路径不含控制字符、URL 不含 `?#`(`client.js:434-450`),否则当普通会话选区处理。
- **多批注/重叠**:去重只按"文本完全相同且同一来源"(`client.js:1475`、`client.js:2016`),所以**重叠选区是各自独立的条目**——选第 1-20 字再选第 5-10 字会得到两条。

### 2. 发送:拼稿只发生在最后一个手势里

- `keydown` 用 **capture** 阶段挂,必须早于 React 容器层的提交(`client.js:1351-1394` 的注释与 `client.js:1391` 的 `addEventListener(..., true)`)。
- 修饰键策略:`Shift/Alt+Enter` 不接管;有文字时只接管裸 Enter;`Cmd/Ctrl+Enter` 仅在草稿为空时接管并 `submit('queue')`(`client.js:1358-1390`、`client.js:1905-1906`)。
- 斜杠命令草稿原样放行、批注留到下一句(`client.js:1952-1957`);草稿里已有批注块则不重复前置,靠三语头哨兵 `BLOCK_HEADS` 判断(`client.js:334-341`、`client.js:1960-1964`)。
- 空草稿的发送按钮被宿主禁用时,`pointerdown` 也能拼稿并直发(`client.js:1425-1439`);键盘激活按钮用 `detail === 0` 的 click 补齐(`client.js:1441-1443`)。
- IME 守卫三层:`isComposing` / `keyCode 229` / `compositionend` 后 50 ms latch(`client.js:1112-1149`),并且只拦"本来就会携带批注"的那次提交,不 `preventDefault`(`client.js:1917-1929`)。
- 发送完成的唯一权威是"草稿有→空"的订阅迁移,不是 DOM 观察(`client.js:2311-2344`);初始化早于会话加载时每 1 s 重试挂订阅(`client.js:2346-2367`)。清空时把条目转存给 `pendingDeco`,供气泡标签用(`client.js:2325-2336`)。

### 3. 气泡剪裁:按最后一个分隔标记切,再贴标签

- `decorateAll` 倒序扫消息行,跳过"已有标签"和 `data-pending-steering` 的行(`client.js:2694-2702`)。
- 纯批注块(没有提问)用"首行文案 + 尾行文案"双端匹配整块清空;有提问时找**最后一个**分隔标记,保留其后文本、删掉之前所有文本节点与空元素(`client.js:2369-2425`)。
- 分隔标记按语言列表 + 老格式:zh `\n提问：` / `提问：` / `\n问题：` / `问题：`,en `Ask:`,ru `Вопрос:`(`client.js:341-355`)。zh 故意用「提问：」而不是「问题：」,因为块首行"回答我的问题："里也含后者(`README.md:128`)。
- 条目数据的来源有两条:刚发送时用 `pendingDeco`;历史消息**从气泡文本反解析**——所以必须"在隐藏前"解析(`client.js:2706-2709`、`client.js:2432-2457`)。反解析按 `\n\n` 分段,靠 `buildBlock` 把引文换行缩进成 `\n   `(`client.js:1893`)来保证多段引文不会被 `\n\n` 切断。
- 标签是 `span[data-annotation-bubble-tag]`,条目挂在 DOM 节点属性 `tag.__annotationItems` 上(`client.js:2458-2525`)——不在任何 store 里。

### 4. 回复映射:纯提示词约定 + 正则 + 相邻行回溯

- 提示词侧只有一句格式指令(`client.js:203-206`),不传编号之外的任何标识。
- 装饰侧:只处理**已停流**的助手行(`data-streaming` 在行内也算,`client.js:2574-2575`),拿"最近一条带标签的用户消息"的条目数组(`client.js:2534-2549`),用 `Annotation[\s\u200b\u200c\u200d\u00ad]*(\d+)[\s\u200b\u200c\u200d\u00ad]*[:：]?` 匹配(`client.js:2589`),`items[num-1]` 取数据(`client.js:2609`)。
- **映射失败的三种降级**:编号越界(模型自己写 `Annotation 5:` 而只有 3 条)→ 保留原文不生成芯片(`client.js:2613-2621`);整行拿不到条目数据 → 整行不装饰(`client.js:2580-2582`);一个都没替换 → 完全不碰 DOM(否则 `replaceChild` 产生同内容新节点 → mutation → 再装饰,**自激死循环**,`client.js:2626-2635`)。
- 流式期间不做替换,原因写在注释里:与 React 正在更新的文本节点冲突会导致整条回复渲染异常(`client.js:2570-2573`)。

### 5. 锚定:文本偏移 + 消息锚,失败就隐藏

`captureAnchor`(`client.js:1807-1858`)在保存时同时抓 live `Range`、`seqKey`、`textOffset`、前后 24 字、行首 24 字;文本不完全一致时**也绝不返回空锚**,至少留行级锚点。

`locateQuote`(`client.js:702-857`)按固定顺序重定位:

1. 文件来源:同 `sourceUrl` 的正文 → live `range` → `textOffset` 精确 → 全文件**唯一**匹配(`client.js:703-720`)。
2. 会话:live `range` 仍连通且去空白后相等 → 直接用(`client.js:722-731`)。
3. `seqKey` 命中的行内:`textOffset` ±2 → `ctxBefore` 后紧邻 → 全行空白剥离扫描 + 上下文打分(`client.js:735-768`)。
4. 同消息内换"芯片差异变体"(`Annotation 1` vs `Annotation 1：`)与 token 级宽松匹配(`client.js:769-786`);**同消息内仍找不到就返回 null**(`client.js:784-786`,v1.3.6 的纪律:跨消息模糊搜索会跳到旧轮次)。
5. 没有 `seqKey`(或该行已不在 DOM)时:退到 `rowHead` 匹配行(`client.js:789-829`),再退到全行打分(`client.js:831-857`)。

标记层是 `position: fixed` 的独立图层,每次 rAF 用 `range.getClientRects()` 重算;滚出正文可视区、或与输入区/会话头部相交就**整条不画**,编号层与高亮层用同一条 `clipPath` 挖洞(`client.js:1698-1713`、`client.js:1752-1791`);多个编号重叠时向右让 18 px、最多 12 次(`client.js:1776-1791`)。

## 为什么它突出

**星标能归到自己头上。** `fork: false`、`parent: null`,仓库自身就是插件本体(无子目录、无宿主主项目),所以 76 / 169 都是这个插件自己的数。时间线:2026-08-10 建仓 → 08-11 首个提交(标题已经写着 **v1.3.2**,v0.9/v1.0 的更早历史不在本仓,README 的版本表是唯一线索)→ 08-19 采样 76 → 11-18 实时 169。三个月 +122%,增速平缓,不是爆款曲线。

**扩散不是代码复用,是交互被复制。** 这个区别必须拆开:

| 口径 | 命令 | 命中 | 判断 |
|---|---|---|---|
| 同名 | `grep -ril 'dsh-annotation' data/plugins/` | 8(含自身) | 7 条第三方,**全部是独立实现** |
| 同领域 | `grep -ril 'annotation' data/plugins/` | 84(含自身) | 83 条,含浏览器元素批注、文件批注、PDF/Zotero 笔记等不同交互 |
| 代码 fork | GitHub forks API(2026-11-18) | 17 | 这 7 个 owner **一个都不在** fork 列表里,即都不是本仓 fork |

7 条同名条目的逐条判定(只看 registry 自述,源码未读):

| 条目 | 判定 | 依据 |
|---|---|---|
| `ECNU/EduWork#dsh-annotation` | 独立实现 | monorepo 子包,自述明说复用"DSH 原生输入框引用、草稿保存和发送流程"——编码换成了官方引用 |
| `feifandiv/dsh-annotation` | 独立实现 | 自述是"输入框卡片 + 右侧栏列表",载体与本品不同 |
| `jin1254/dsh-annotations` | 独立实现 | 自述钉在 0.2.1-rc.2,发"紧凑批注标签" + 原文跳转 |
| `ruisenbai/dsh-annotation` | 独立实现 | 还覆盖文件与 diff 批注,registry 类目是 session |
| `stoner-byte/dsh-annotations` | 独立实现 | 英文自述与本品 registry 描述几乎同句(判断:抄了描述,不是 fork) |
| `swiftlc/dsh-annotation` | 独立实现 | "composer 里的标注工具与 chip" |
| `zengxiaolou/dsh-annotation` | 独立实现 | 自述明说依赖另一个插件 `dsh-paste-chip` 才有胶囊 |

所以:**0 条把本插件当依赖,0 个 fork 进 registry**。但 17 forks / 169 stars ≈ 10% 的 fork 率(且 fork 全 0 星)说明它被当底稿用,`Ryuu-64/dsh-annotation-upstream` 这种命名就是证据;CHANGELOG 里 #65/#66/#67/#68 的贡献者正好是 fork 所有者。

**为什么"批注"会被反复重写(判断,依据是本插件与宿主源码,不引别卡):** 三层都没有宿主原语。

1. **消息级装饰没有槽**。会话扩展点只有整视图注册(`view-registry.d.ts:1-15`),要动"某条消息里的某段文字"只能拿 DOM。于是行判别、锚点、裁剪全是猜属性——本仓为此维护了三套助手行判别、两套 composer 判别。
2. **草稿里没有"引用块"原语**。`DraftInput` 只有纯文本或引用 occurrence(`draft.d.ts:1-8`;`decorations.d.ts` 只认 `/`、`@` 触发词),没有"带出处的引文"这种实体。于是每条实现自选编码:纯文本块、原生引用、外部胶囊、JSON。本品选的是最退化的那种,**把 UI 状态写进消息正文,再回头把正文改回去**。
3. **回复与批注之间没有字段可挂**。协议只能靠模型自己写的 `Annotation N` 标签,映射是正则 + 相邻行回溯。

也就是说:接入点其实**很稳定**(选中文本 → `setDraft` → 消息日志 → 回复),不稳定的是**编码**。7 个实现落在同一个接缝上、各写一套格式,恰好说明缺的是"引文原语"和"装饰槽",不是 UI 细节没人规定。本仓 152 个提交里 58 个动 `client.js`、33 个以 `fix:` 开头,大半修的是锚定漂移、图层裁剪与装饰自激——同一件事反复重写的微观版本。

## 代价与边界

按发生顺序:

1. **会话 id 是四级回退**,每一级都是未公开形状:`uiSession.adapter.current` → `localStorage['dsh.sessions.current']` → `sessions.list` 快照的 `current` → `retainedBy.mainView > 0`(`client.js:975-1050`)。取不到就只 toast + 保留批注(`client.js:1932-1943`),不发送;这也是 CHANGELOG 里 0.1.7 上"批注在、回车没反应"的成因。
2. **选区跨块级元素**:选区文本会带出 DOM `textContent` 里没有的 `\n`。匹配靠"空白完全剥离 + 原始偏移映射"补救(`client.js:546-561`),但**发出去的引文仍是原样带换行**——匹配与发送用的是两套文本。
3. **剪气泡靠字符串标记**:`lastIndexOf` 取最后一个 `\n提问：`(`client.js:2394-2400`)。若用户问题本身在某行行首含「提问：」,切割点会落进用户文字里,批注块残留在气泡中。代码可证,未见防护。
4. **反解析依赖缩进约定**:引文里若真有连续空行,`buildBlock` 的 3 空格缩进(`client.js:1893`)能挡住 `\n\n` 分段,但这条契约只写在代码里,没有测试守着。
5. **锚定只认文本**:消息被编辑、重新生成、分叉后 `seqKey` 变或文本变 → 角标**静默消失**,没有"锚点丢失"提示(`client.js:784-786` 的纪律就是"找不到就不画")。流式期间文本增长会让 `textOffset` 漂移,±2 容差只挡小前缀插入,其余靠上下文打分救。
6. **代码块不豁免**:`decorateAnnotationLabels` 遍历行内全部文本节点,只判 `parentNode`(`client.js:2588-2636`),没有 `pre/code` 守卫——回复里贴一段含 `Annotation 1:` 的代码或协议原文,会被换成芯片。只有编号越界才保留原文(`client.js:2613-2621`)。
7. **长选区不截断**:发送路径原样拼全文(`client.js:1893`),只有显示层裁到 3 行(`client.js:113` 的 `-webkit-line-clamp: 3`)。选中 5000 字会整段进 prompt,也整段进 `localStorage`。
8. **装饰成本随会话长度线性增长**:`decorateAll` 是 `querySelectorAll` + 每行 `textContent`(`client.js:2694-2726`),已加 120 ms 合并(首拍仍立即执行,保住"绘制前隐藏",`client.js:2731-2743`)。1.4.11 修过一次自激死循环:越界编号在"不生成芯片"分支里仍无条件 `replaceChild`,mutation 不收敛,客户端整套卡死(`CHANGELOG.md:8`)。
9. **移动端/键盘**:工具条优先放选区**下方**,因为有原生选中菜单(z-index 无效,`client.js:864-882`);编号角标是 `div` + click,无 `tabindex`/`role`(`client.js:1773-1775`、`client.js:1794-1799`)→ 键盘不可达;`Esc` 只关工具条。
10. **发送按钮路径绑死文案**:按钮靠 `aria-label === '发送消息' || 'Send message'` 识别(`client.js:1418-1423`)。ru 界面(插件自己支持 ru)上这两个字符串都不匹配 → 空草稿点发送按钮不会拼批注,只剩 Enter 可用。
11. **隐私与出网**:零网络调用(`grep -n 'fetch(\|XMLHttpRequest\|WebSocket\|sendBeacon' client.js` 只命中 SVG 命名空间字符串)。批注全文以明文存 `localStorage['dsh.annotation.pending.v1.<encodeURIComponent(sessionId)>']`(`client.js:923-926`、`client.js:1094-1103`)。选区可来自任何**已打开**的工作区文件预览(只校验 URL 形态与会话归属,`client.js:434-450`,不判断文件敏感性),内容随后进入会话日志。
12. **卸载残留三条**:① `dispose` 移除了 host/overlay/numLayer/chipLayer/tipLayer 与全部监听(`client.js:2833-2861`),但 `<style id="annotation-for-dsh-style">` 不删(`client.js:59-61` 创建,清理段无对应);② `dsh.annotation.pending.v1.*` 不删、也没有按会话回收,每会话留一条;③ 最重的一条——**批注块已经是消息正文的一部分**,e2e 直接断言发给后端的 prompt 里含引文与批注(`test/host-enter.e2e.ts:354-355`),卸载后没人剪,用户气泡里会重新长出整段批注块。
13. **兼容成本**:三语协议块 + 反解析兼容老格式(zh 的「问题：」 legacy 仍在 `client.js:341-345`);助手行 3 种结构;composer 2 种结构(`client.js:1371-1376`,0.1.1 的 textarea 分支曾一度被删、1.4.11 又恢复);每次宿主改 DOM 属性都是 patch 级修复。

## 可信度与复现

★★★:`client.js` 全文通读(2870 行,分 6 段),`src/index.ts`、`lib/index.js`、`lib/types/index.d.ts`、`package.json`、`cordis.patch.yml`、`tsconfig.json`、`README.md`、`CHANGELOG.md`(1.4.11 段)、`docs/testing.md`、`docs/plans/2026-09-14-sidebar-annotation.md`、`test/` 的 19 个文件(`test/message-block.test.mjs` 全读,其余按用例名与关键段 grep)、`test/overlay-browser.mjs` / `test/sidebar-browser.mjs` / `test/host-enter.e2e.ts` 的驱动与断言段;对照本机 DSH **0.2.1-rc.5**(下凡以 `dsh-client-*` / `cordis/` 开头的路径均相对 `~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh/`)的 `dsh-client-modules`、`dsh-client-ui-conversation`(facade/view-registry/draft/decorations 类型)、`dsh-client-ui-chat`、`dsh-client-ui-sidebar-documentpreview` 的 bundle 属性。

```sh
git clone --depth 1 https://github.com/omdsh-dev/dsh-annotation.git .work/mine/cards/annotation/repo
cd .work/mine/cards/annotation/repo
git log -1 --format='%H %ad %s'          # 48eac63b… / 2026-11-03
git fetch --unshallow --filter=blob:none && git rev-list --count HEAD   # 152
git log --format='%s' | grep -c '^fix'   # 33
wc -l client.js src/index.ts test/*      # 2870 / 9 / 2308

# 扩散(在 awesome-dsh-plugin 仓库根)
grep -ril 'dsh-annotation' data/plugins/ | wc -l   # 8(含自身)
grep -ril 'annotation'     data/plugins/ | wc -l   # 84(含自身)
curl -s 'https://api.github.com/repos/omdsh-dev/dsh-annotation' | jq '.stargazers_count,.forks_count,.created_at'
#   169 / 17 / 2026-08-10T17:36:49Z
curl -s 'https://api.github.com/repos/omdsh-dev/dsh-annotation/forks?per_page=100' | jq -r '.[].full_name'
#   17 个 fork,与上面 7 个同名条目无交集 → 判定"独立实现"的依据

# 星标/下载边车
python3 -c "import json;print(json.load(open('data/stars.json'))['https://github.com/omdsh-dev/dsh-annotation'])"
#   {'stars': 76, 'checkedAt': '2026-08-19'};downloads.json 无该 URL
```

**未读**:`site/` 的 Vite 构建产物(581 KB JS)、`scripts/`(7 个文件,e2e/冒烟/打包校验的驱动)只看了 `scripts/plugin-client-url.mjs` 与 `scripts/resolve-dsh-tag.mjs`;5 个 `test/*-browser.mjs` 与 `test/host-enter.e2e.ts` **未实跑**(需 Playwright + 可解析的 `dsh-v*` tag);7 个同名实现的源码一个没读。

## 待验证

1. `exports.inject` 里含 `uiSession`(`client.js:2865`),而 cordis 的 inject 数组是**硬依赖**(`cordis/lib/types/registry.d.ts:13,105-111`:服务缺失时 fiber 不 apply);代码又在 `ctx.get('uiSession')` 做惰性探测(`client.js:996-1001`)。在 0.1.x 宿(该服务缺席)上到底是"等"还是"照常 apply",决定 README 声称的 0.1.1~0.2.0 覆盖是否成立——需在旧宿主实测一次启动日志。
2. **映射质量无数据**:`test/` 里没有 `decorateAnnotationLabels` / `findPrevAnnotationItems` / `locateQuote` / `captureAnchor` 的任何用例(grep 四个函数名在 `test/` 只命中一条注释)。真实模型按 `Annotation N:` 逐条回答的命中率、模型写 `**Annotation 1**` 这类变体的概率,都只能靠真实会话统计。
3. 代码块误换芯片(第 6 条失败模式)是静态可证,但没在真实宿主里构造复现;同理"用户问题行首含「提问：」导致气泡残留"。
4. 169 与 76 之间的增长来自哪里(registry 收录时间、Linux.do 导流、org 内互推)没有数据;`data/stars.json` 只有单点,画不出曲线。
5. 7 个同名条目只据 registry 自述判定"独立实现",其中 `stoner-byte/dsh-annotations` 的英文自述与本品几乎同句,是否照抄描述未核实;`ECNU/EduWork` 子包的"原生引用"编码是否真绕开了文本块,需读源码。
6. `localStorage` 里指向已删除会话的 `dsh.annotation.pending.v1.*` 永不回收(`client.js:2790-2810` 只读写当前会话),长时间使用后实际残留多少条未测。
7. 标记层的重绘频率:每次滚动/resize/mutation 都走 rAF 全量 `buildMarkers`(`client.js:1267-1309`、`client.js:1698-1713`),百条批注的长会话里主线程占用未量化。
