# dsh-tianshu-tui — 宿主进程内换壳:移植来的 ANSI 引擎直接接管终端,自己管 live 区与 scrollback

> 证据等级:★★★(源码级;`huiliyi37/dsh-tianshu-tui@fc6aa32b5c5b4f761db91c14eaf673ec8dba2b1b`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 217、下载 1763 为 2026-08-19 历史采样;2026-11-18 实时星标 313。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `huiliyi37/dsh-tianshu-tui`([registry](../../../data/plugins/huiliyi37__dsh-tianshu-tui.yml)) |
| 类目 | ui([census](../../ecosystem/census.py) 2351 条 / 全表 11 744 条) |
| 子分类 | `replace-shell`(换壳,见 [README](README.md)) |
| 自述 | registry 只有一句「A terminal UI (TUI) for DeepSeek Harness.」;`package.json:3` 的 description 才列了流式 markdown、工具卡、16+ 主题、slash 命令、会话 tabs、LSP、成本、自更新——其中「会话 tabs」在 `src/` 里找不到实现(见「代价与边界」) |
| 星标 ⚠ | **217**(2026-08-19 采样;建仓后第 6 天);2026-11-18 实时 **313**(+44%) |
| 下载 ⚠ | **1763**(2026-08-19,同为第 6 天) |
| 扩散 | **0**(口径:`grep -ril 'tianshu' data/plugins/` 命中 1 条,减去自身为 0,唯一命中 `data/plugins/huiliyi37__dsh-tianshu-tui.yml`;中文名 `grep -rl '天枢' data/plugins/` 命中 0) |
| 仓库 commit | `fc6aa32b5c5b4f761db91c14eaf673ec8dba2b1b`,2026-11-15,`docs(release): 记录 1.0.0-rc.6 已上线`;包版本 `1.0.0-rc.6`,Apache-2.0 |
| 包形态 | npm 包 + DSH bundle 双角色,但**没有 `bin`**:`package.json` 184 行里无 `bin` 字段,入口只能是 `dsh --profile tui`;`package.json:55-59` 的 `dsh.bundle.patch: ./cordis.patch.yml` 让它成为 profile 的呈现层;`files` 只发 `lib/index.js`(1 123 521 字节)、`lib/invariant.js`、`lib/types/**/*.d.ts`、`cordis.patch.yml`,以及 `CHANGELOG.md` / `NOTICE` / `SOURCE-MAP.md` 三份说明——`src/` 不进包 |
| 代码规模 | `src/**/*.ts` **181 文件 / 40 853 行**(含注释,不含测试);`tests/**/*.spec.ts` **160 文件 / 41 535 行**;`cordis.patch.yml` 596 行;跟踪文件合计 **8 408 925 字节**(≈8.0 MB,不含 `.git`)。命令见末节 |
| 仓库历史 | 2026-08-13 建仓,根提交 `2ee948d` 一次落 **207 个文件**(「独立基线仓初始化」);到 2026-11-15 共 **338** 提交、CHANGELOG **33** 个版本 |

## 它到底是什么

**一句话:它不是终端客户端,是宿主进程内的一个 profile bundle——把「DSH 长什么样」换掉,但一行 IPC 都没有。**

三条可以从源码确证的边界:

1. **同进程,不是同协议。** 它拿到的是宿主自己的 Cordis `Context`,不是 HTTP/WS 句柄:`src/index.ts:141-160` 把 `runtimeCtx` 直接交给 `TuiApp`,后者用 `ctx.sessions.get(...)`(`src/ui/app.ts:2381`)、`ctx.agents.resume(...)`(`app.ts:2439`)、`ctx.on('session/event', ...)`(`app.ts:2513`)。`src/` 全域没有 `node:http`、`node:net`、`createServer`、`WebSocket` 任一符号;本进程的出网点只有两个:自更新查 npm registry(`src/self-update.ts:1-6`)与 `/key` 供应商对话框列模型(`src/ui/key-dialog.ts:85`);唯一间接联网是 LSP 子进程(`cordis.patch.yml:41-54` 默认 `npx -y typescript-language-server` 懒启动时首次拉包)。**判断:所谓「断线重连」在这条实现里不存在,因为它没有可断的线;代价换成进程内耦合(宿主 API 一断,界面直接起不来)。**
2. **纯展示层,契约写进了文档也写进了代码。** `ADAPTER.md:9-20` 立了三条:不注册任何 prompt / 工具 / 上下文面、用户输入只作为普通日志消息、所有渲染状态派生自事件流。代码侧对得上:`grep -rn 'ctx.tools\|systemPrompt' src` 无命中;输入经 `followup`/`steer` 提交进宿主 inbox(`src/adapter/send.ts:1-10` 明说「不直接写任何会话事件」);`adapter/` 里的 fold 是纯函数(`src/adapter/live.ts:1-11`、`assistant-stream.ts:1-16`)。
3. **渲染核心不是为 DSH 写的,是移植来的。** `SOURCE-MAP.md:1-16` 记录:渲染核心移植自作者自己的天枢终端 UI(`huiliyi37/Tianshu-Tui` 的 `src/tui/` 子树,Apache-2.0),port 时点是本仓提交 `b26ebed`(2026-08-10)对上游 `bc2aa2a0c`。181 个 `src/` 文件的来源标注是 **17 ported + 57 modified + 107 new**(`grep -c '| ported'` 等,见末节);最核心的 `engine/live-engine.ts`、`engine/input-handler.ts`、`engine/input-line.ts`、`block-stream-writer.ts`、`format/markdown.ts` 都是 `modified`,而 `ui/app.ts` 是 `new`(「角色对应上游 engine/app.ts,为面向 dsh cordis 服务的独立装配实现,非逐行移植」)。**这解释了两件事:40 853 行不是 6 天写出来的;星标也不是从一个空项目长出来的。**

**核心循环只有一个,但分成两个完全不同的写屏面:**

- **scrollback(主屏上方)** — append-only,进了就不擦:`src/engine/commit-engine.ts:1-12` 明写「只做 append-only `stdout.write()`,进入 scrollback 的内容不可被擦除、不可被重绘」,替代 Ink 的 `<Static>` 语义。
- **live region(屏幕底部 N 行)** — 进行中的工具卡、推理头行、审批卡、输入轨、footer,由 `LiveEngine` 增量重绘,永远只占底部若干行。

数据从会话事件流进来,经 `adapter/transcript.ts` 折成 `Transcript` 视图,再由 `render/` 与 `format/` 生成行:已落定的走 commit,进行中的走 live。**这个「两表面」划分是整张卡的技术核心**,后面所有机制(行预算、行级 diff、CPR 自愈、稳定前缀提交)都是为了守住它。

## 怎么接进 DSH

- **安装/启动链路**(`README.md:64-70`):`pnpm dlx @deepseek-ai/dsh@next plugin --profile tui add @huiliyi37/dsh-tianshu-tui`,再 `pnpm dlx @deepseek-ai/dsh@next --profile tui`。`plugin add` 只是把包名转发给 pnpm(`dsh` 侧 `--profile` 是必填项);真正让它变成「一层」的是包里的 `dsh.bundle.patch`。宿主侧的判定点在 `@deepseek-ai/dsh-app-boot`:`bundlePatchFiles()` 校验该字段必须是字符串或字符串数组(`lib/index.js:517-521`);`@deepseek-ai/dsh-plugin-manager` 对没有 `dsh.bundle` 的包只当普通依赖并告警「installed as a plain dependency, not a profile layer」(`lib/index.js:336`),安装路径上还会以 `not-a-bundle` 直接拒绝(`:1866`、`:1917`)。装配结果是 profile 的 bundle 层 = `[@deepseek-ai/dsh-base, @huiliyi37/dsh-tianshu-tui]`(`docs/LOCAL-DEV.md:24`)。
- **patch 里到底插了什么**(`cordis.patch.yml`,596 行,一个顶层 `insert` 数组 + 一个 disable 列表):
  - `- id: tui-runner` / `name: '@huiliyi37/dsh-tianshu-tui'`(`:13-14`)——**这是唯一属于它自己的行**,插件名固定为 `tui-runner`(`src/index.ts:23`)。
  - 官方 `agent-preset-registry`(`:60-64`,`default: standard`)+ 四条预设声明行 `preset-standard` / `preset-ptc` / `preset-minimal` / `preset-cordis`(`:67`、`:191`、`:319`、`:394`),每条的 `plugins:` 是完整 agent 面清单。整个 `insert` 只有 12 行(其中 1 行是它自己);**agent 面从宿主搬进了 preset**,所以 patch 尾部有 22 条 `- id: ... disabled: true`(`:526-596`)把 host 上的工具行关掉。
  - 作者自己的 LSP 三件套:`@huiliyi37/dsh-lsp`、`dsh-lsp-local`(默认带一条 `npx -y typescript-language-server --stdio`)、`dsh-tool-lsp`(`:38-57`)。base 不含 LSP,这是它自带的模型工具面。
- **依赖三线**(`package.json:61-77` 与 `:148-183`):16 个 `@deepseek-ai/dsh-*` **peer 精确钉 `0.2.2-rc.3`**、`@deepseek-ai/cordis ~4.1.0`;另有 7 个官方包放在 `dependencies` 里(预设注册表、cordis host runner、market、PTC 执行器等,base 不提供);再加 **21 个 `@huiliyi37/*@0.8.0`** 直接依赖。`ADAPTER.md:101-105` 自己把这条写成纪律:「宿主版本漂移时先升级 peer 范围再发版,不静默容忍」。
- **注册点**:只 `inject` 三个必选服务 `sessions` / `agents` / `agentDefaultModel`(`src/index.ts:115`);其余 20 余个服务一律走 `ctx.reflect.get`(可选,缺了就面板降级,`ADAPTER.md:38-59` 有完整表)。**唯一对外提供的服务是 `tui.commands`**(`app.ts:1219`),让别的插件往 slash 注册表里加命令——这是它留给生态的唯一接缝,不是通用扩展协议。
- **订阅面**(`ADAPTER.md:61-75`):`session/event`(事件流)、`approval/request`(waterfall answerer,`app.ts:1442-1444`)、`user-questions/request`(全局注册,`app.ts:1537-1538`)、`workflow/*` 六事件、`subagent/start|end`;`sessionProjections` 走快照 + `onChanged`(`app.ts:2532-2575`)。全部只读,不发布。
- **生命周期**:`attach()` 接管终端、`dispose()` 恢复(`app.ts:1356`、`:4251`);`ctx.effect` 注册卸载清理,SIGINT 双注册(POSIX + stdin,`index.ts:166-182`),退出经宿主 `appExit` 而不是硬 `process.exit`(`index.ts:122-126`)。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `cordis.patch.yml` | 596 | 唯一 manifest 载体 | `:12-15` insert;`:38-57` LSP;`:60-64` preset;`:526-596` disable |
| `src/index.ts` | 250 | 装配入口、退出/重启、启动自更新 | `:23` name;`:81` apply;`:115` inject;`:186` attach;`:194` 自更新 |
| `src/ui/app.ts` | 4310 | 装配、事件订阅、键仲裁、渲染组合 | `:1356` attach;`:2513` feed;`:3326` 渐进重放;`:4251` dispose |
| `src/engine/live-engine.ts` | 669 | 底部 live 区增量重绘 + CPR 自愈 | `:341` render;`:528` 行预算;`:598` 行级 diff;`:202` noteCpr |
| `src/engine/write-batcher.ts` | 94 | 渲染帧合并(~60fps 封顶) | `:23` `MIN_FRAME_INTERVAL_MS=16`;`:52` schedule |
| `src/block-stream-writer.ts` | 175 | 流式文本按语义边界切块 | `:12-17` `minChars:100 / maxChars:200 / idleMs:180 / 64KB` |
| `src/engine/stream-renderer.ts` | 203 | 稳定前缀 commit、尾部留 live | `:1-20` 模型说明;`:37` `findStableBoundary` |
| `src/engine/commit-engine.ts` | 142 | scrollback append + 1000 行环形缓存 | `:20` `DEFAULT_SCROLLBACK_MAX_LINES` |
| `src/engine/input-handler.ts` | 740 | raw mode、CSI/kitty 解码、bracketed paste | `:99-113` 80ms/500ms 双超时;`:236` setRawMode |
| `src/engine/input-line.ts` | 1560 | 多行编辑、CJK 折行、粘贴折叠 | 头注释(10 万字符草稿 1.3s→10ms) |
| `src/width.ts` | 248 | 三档显示宽度 narrow/wide/full | `:1-20` 档位语义 |
| `src/controllers/approval-controller.ts` | 313 | 审批挂起状态机 | `:63` 60s 超时;`:242` 本地白名单 |
| `src/adapter/sessions.ts` | 342 | 列表/恢复/分叉/损坏降级 | `:131` list;`:213` fork;`:235` loadHistory |

**live 区:自己写的一套「光标常驻 + 行级 diff」。** `live-engine.ts:1-18` 直接点名与 Ink 的差别:Ink 在 live 区高度 ≥ 终端高度时会 `\x1B[2J` 全屏清屏,`LiveEngine` 永不触发全屏清屏,区域被严格限制在底部。三条不变量:

- **帧末光标常驻区域末行**(`:331-332` 的契约,尾行不写 `\n` 见 `buildAppend` `:560-568`),所以不会「贴底每帧滚屏」;
- **所有行数记账按 display rows**(wrapping-aware,`rowsForLine` `:251-259`),不按逻辑行——200 字符一行在 80 列终端占 3 行;
- **行级 diff 只在「结构未变 + 每行 wrap 高度未变」时启用**(`canDiff`,`:431-437`),否则回退全量重写(`buildFullRewrite` `:579-587`);diff 实现见 `:598-620`,不写任何 `\n`,靠 `cursorDown` 在底行被 clamp 来避免滚屏。

**CPR 自愈**(`:95-236`)是这个引擎最有意思的一段:别的进程往同一个 TTY 写字节会移动光标,`lastDisplayRows` 随即失同步,之后回顶量不足,旧帧顶部就永久残留进 scrollback。它的对策是渲染后发 DSR 探针(`\x1B[6n`)记录驻停基线,后续响应偏离就判「污染」,下一帧走恢复重铺;探针有 1s 节流、5s 超时、`rowsUp` 漂移丢弃三重阳止(`:209-217`),alt screen 期间整体 suppress(`:165-175`)。

**行预算按 display rows 而不是行数**(`:528-558`):整帧恒 ≤ `min(28, rows-1)` 行,超预算时**优先保尾部 chrome**(输入框 + footer),截断的是中段 dynamic。窄窗口下这是防止「正文泄露到输入框底下」的那道闸(`:513-527` 注释里有完整的故障史)。

**流式输出:切块 → 稳定前缀入 scrollback → 尾部留 live。** `BlockStreamWriter` 按段落 > 句末 > 空白的优先级切块(`block-stream-writer.ts:12-17`、`:99-129`),`StreamRenderer` 再在「最后一个稳定顶层 block 边界」切分(空行结束的段落、闭合的 ``` 围栏,`stream-renderer.ts:24-40`):稳定前缀立刻高亮并 commit,不完整尾部留在 live 区。**围栏代码块在未闭合期间不解析高亮**,避免闪烁。

**流式中断**:`handleAbort()`(`app.ts:2882-2903`)先释放 overlay,再 `cancel({kind:'user'}, {keepInbox:true})`,然后**先丢弃流式残文、再提交中止提示**——注释说明次序反了会把上一个 run 的残留画进那一帧(`:2895-2899`)。

**输入**:`raw mode` + 逐字节解析;孤立 ESC 80ms 刷新、不完整 CSI 兜底 500ms(分两个超时常量,`input-handler.ts:99-113`,注释解释了为何不能共用一个值:高延迟 SSH 下 80ms 会腰斩方向键序列);bracketed paste 走 `onPaste`(`:117-118`);kitty 键盘增强只在探测通过时推送 flag 1(`app.ts:1399`)。

**终端能力检测与降级**(`src/term-caps.ts`):legacy Windows conhost 用「win32 且无任何现代终端标记」判(`:22-30`),命中即无条件 ASCII 字形 + ASCII 边框 + 宽度 full 档;OSC52 剪贴板按 `TERM_PROGRAM` 白名单 + VTE/screen/linux VT 显式排除(`:45-56`);kitty 键盘白名单排除 tmux/screen(`:144-153`);`NO_COLOR` 按规范实现(`engine/ansi.ts:240-260`);`RIVET_ASCII_UI=0/1` 可强制覆盖。**宽度**是三档而非两档(`width.ts:1-20`):narrow(= string-width)/ wide(非 box 的 ambiguous +1)/ full(含 box-drawing,+1,legacy CJK conhost 默认)——因为 Windows 中文点阵字体连框线都按 2 列渲染。

**图片**:只走两种终端图形协议——kitty APC 与 iTerm2 OSC 1337(`engine/term-image.ts:1-25`),协议探测在 `engine/ansi.ts:406-442`;两种序列被不支持的终端静默忽略,所以「检测失误的最坏结果是图片不显示」。安全边界写得很实:data URL 载荷编码前必须过 RFC 4648 校验,否则载荷里的 BEL/ESC/ST 能提前终止 OSC 并注入控制序列(`term-image.ts:18-21`)。

**会话模型**(`src/adapter/sessions.ts`):列表走 `sessionPersistence.open(id,'read')` 的只读句柄封装(`:50-89`),`listSessions`(`:131`)、`loadHistory`(`:235`)、`forkSession`(`:213`,用 `agents.create({seed, meta})` 而不是 `sessions.fork` 后再 resume,`:170-172` 解释了原因);**损坏的持久化会话 catch 成空历史**(`:243-247`),列表行仍在,由 TUI 自己把失败显示出来。恢复不是一次性写完:历史按 **100 行一片** 经 `setImmediate` 链落底,首片同步写(首帧即有内容),重放期间新到的 `session/event` 进 backlog 排队,播完按序回放(`app.ts:3326-3356`)。`switchSession` 先 resume 再提交切换状态,目标不可恢复时停在原会话(`app.ts:2433-2440`)。`/rewind` 是「会话截断 + 文件快照回退」双模(`app.ts:2360-2424`),截断依赖宿主 `sessionPersistence.truncateStored` 与 `Session.truncate`,任一缺失就 fail loud。

**审批**:waterfall answerer(`app.ts:1442`),状态机在 `approval-controller.ts`;决策梯度 y/p/t/a/n/f/esc,其中 `p`(命令前缀白名单)与 `t`(本会话记住此工具)是**纯 TUI 本地短路态**,不落协议(`ADAPTER.md:72-74`);非当前会话的请求 `next()` 委托,已有挂起也委托(fail-closed);挂起超 60s 无应答自动结算 `cancelled`(`:63`、`:257-262`)。

**测试**(160 个 spec / 41 535 行,四个值得单独点):

- `tests/loader-composition.spec.ts:1-10` 是**真组装 lanes**:test-only `cordis.yml` 经真 Loader 进程内 boot,真 `dsh-session`/`dsh-agent`/`dsh-agent-loop`/审批/提问服务树,只在终端边界造假 TTY、用 `llm-replay` 顶掉真适配器;断言是行为判据(挂载后事件驱动渲染、dispose 后监听器全释放、raw-mode 对称恢复)。
- `tests/architecture-guards.spec.ts:1-30` 把设计约束变成红绿测试:禁止 `src/` 全域出现 `process.stdout.write`、子进程必须 `windowsHide: true`、`format/`+`render/` 禁 I/O import、`app.ts` 行数棘轮只降不升、README 哈希清单一致、键位投影必须在 README 登记。
- `tests/bundle-contract.spec.ts:1-6` 守发布形态:`lib/*.js` 不得 import 未发布的 `@deepseek-ai/dsh-root`(那是 issue #1 的真实爆炸)。
- `scripts/e2e-tui.sh:1-15` 是 pty 真机 e2e(expect 驱动官方 CLI + profile link 到本仓 `lib/`),独立 `DSH_HOME`,覆盖启动复用、`/session list` 分页、选择器翻页。

渲染与输入覆盖很实:`live-engine.spec.ts`、`render-invariants.spec.ts`、`input-handler-keys.spec.ts`、`input-line.spec.ts`、`vim-input.spec.ts`、`term-caps.spec.ts`、`term-width.spec.ts`、`write-batcher.spec.ts`;会话侧有 `sessions-fork-seed.spec.ts`、`session-reuse.spec.ts`、`restore-session.spec.ts`、`rewind-overlay.spec.ts`。

## 为什么它突出

**先拆星标归属。** 这里是单仓库、无子目录条目,仓库级星标与插件级热度重合,217 ⚠ / 313 实时**就是插件自己的数**,没有归属歧义。但「6 天 217 星」不是自然增长,证据在仓库自己的历史里:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-10 | 渲染核心自上游 `Tianshu-Tui@bc2aa2a0c` 移植 | `SOURCE-MAP.md:5` |
| 2026-08-13 | 建仓,根提交 `2ee948d` 一次落 207 个文件(「独立基线仓初始化」),当天 27 个提交 | `git show --stat 2ee948d` |
| 2026-08-15 | 0.1.2-rc.7 | `CHANGELOG.md:416` |
| **2026-08-19** | **217 星 / 1763 下载采样点**(建仓第 6 天,当时版本 0.1.2-rc.10) | registry ⚠ |
| 2026-11-15 | 1.0.0-rc.6(33 个版本、338 提交) | `git log -1` |
| 2026-11-18 | 313 星(实时) | GitHub API |

**判断:首波声量来自作者已有的天枢社区,不是 registry 的自然发现。** 依据是可见的三条:根提交直接是 207 文件的完整基线(不是从零起步);`README.md:170-176` 挂着官网 `tianshuharness.com`、上游 `Tianshu-harness`、论坛 `tianshu.club` 三个自有入口;`README.md:178-189` 有一张 7 行的「社区生态」互链表——**它是给别人导流的一方,不是被导流的一方**。这与下面第 0 扩散的事实是同一枚硬币的两面。

**零第三方提及,而且原因是结构性的。** 11 744 条里 `tianshu` 只命中它自己。可解释的部分:

1. **可复制的部分不在这一层。** 40 853 行里真正值钱的是移植来的渲染引擎,而引擎的上游是作者自己的 Apache-2.0 项目 `Tianshu-Tui`(`NOTICE` 明写再分发与 §4(b) 修改声明)。第三方要复用那套引擎,直接去上游更省事,不会来提这个 DSH 包。
2. **没有可对接的协议面。** 全文唯一的 outward seam 是 `ctx.provide('tui.commands')`(`app.ts:1219`),让别的插件加 slash 命令——是「往我这儿塞一条命令」,不是「按我的协议写一个 provider」。没有 MCP、没有 HTTP 路由、没有可与别的工具共用的配置文件格式(配置走 `~/.dsh-tui/prefs.json` 与 `themes/*.json`,自用)。
3. **换壳天然不可组合。** 它整屏接管 TTY,别的插件没法把它当一块面板嵌进去;能「提及」它的场景只剩两种——要么讨论 TUI 体验本身,要么抄它的实现。前者不是生态数据,后者会变成 fork 而不是新条目。

**那么「第二套 TUI」为什么值得一张卡?** 因为它代表换壳路线里的**另一个实现选择**,而且这个选择改变了代价的形状:

- **换壳可以「在宿主进程里换掉呈现层」,不必在外面再包一层客户端。** 复用宿主的 session / agent / 会话日志,拿到的是同一个 `Context`(`index.ts:115`、`app.ts:2513`),因此零 IPC、零重连逻辑、断线这一类失败模式整体消失。
- **换壳也可以不用 React/Ink 那套树。** 它自己写 ANSI 引擎:底部 live 区增量重绘 + 行级 diff + CPR 自愈 + 稳定前缀 append 进 scrollback(`live-engine.ts:341-463`、`stream-renderer.ts:24-40`)。**这一层的机制值得读,因为它解决的问题(Ink 全屏清屏、贴底滚屏、CJK 宽度误算、外来写入污染)在任何终端 UI 里都存在,而它给出的答案是可验证的、带故障史的。**
- **它把「换壳的代价」暴露得很直接**:peer 精确钉在一个宿主 rc 上,宿主一升级就 hard fail(下一节第 1 条);反过来,它也用 33 个版本 / 338 提交标出了跟随成本的量级。

**判断:这是一个「有真实使用量的产品型插件」,不是生态锚。** 217 ⚠ → 313 实时、1763 下载、33 个版本,说明有人在用;零扩散说明它不产出可被别人引用的机制标准。它在 `replace-shell` 里的位置是「另一种换壳实现」,而不是「被跟随的范式」。

## 代价与边界

按发生顺序列:

1. **宿主版本不匹配 = 启动即失败,不是降级。** peer 里 16 个 `@deepseek-ai/dsh-*` 精确钉 `0.2.2-rc.3`(`package.json:61-77`);宿主对 **bundle** 做的是硬校验——`dsh-app-boot/lib/index.js:1025-1026` 对未豁免的不匹配直接 `throw`,`:311-325` 的规则是「每个 `@deepseek-ai/dsh[-*]` peer 都必须匹配,预发布参与区间比较」。补救只有两条:升级插件,或对 `包名@版本 + 宿主版本` 做一次 `dsh plugin allow-version` 精确豁免。**这是全卡最硬的一条成本:换壳插件换来的自由,代价是钉死在宿主的一个 rc 上。**
2. **Node 版本同样是硬的。** `engines.node >= 24.9.0`(`package.json:42-44`);`scripts/e2e-tui.sh:20-24` 记录了更阴的形态——Node 过旧时宿主入口 `import.meta.main` 不存在,CLI 静默 no-op(exit 0 无输出),用户看到的是「装完了没反应」。
3. **安装路径本身要绕。** 官方 CLI 依赖树大,install 脚本注释明说 npm 11 会 heap OOM,一律走 pnpm(`scripts/install-tui.sh:11-13`);pnpm ≥ 11.7 对未裁决的原生构建 exit 1,脚本要先把 profile 里 `pnpm-workspace.yaml` 的 `allowBuilds` 占位填掉再重试(`:52-62`)。插件自身还带两个原生面:`sharp`(图片转码)与 `node-addon-require-builtin`。
4. **非 TTY 没有全局闸门。** `src/` 里 9 处 `isTTY` 判断全是局部降级,没有一处是启动前的拒绝——`input-handler.ts:236`、`:324` 只是 raw mode 开关,`index.ts:102` 是退出兜底,`theme-detect.ts:76` 让背景探测走 env 兜底,`ansi.ts:358`、`:436` 让 OSC 8 超链接与图片协议判「不支持」,`app.ts:1518` 决定要不要自动弹 key 引导。**判断:被重定向到管道时 ANSI 序列照常写出,只是没有 raw mode、没有超链接、没有图片——这是与「终端专用」自述不一致的一处。**
5. **终端太小只能硬裁,没有最小值门槛。** live 区上限 `Math.max(4, Math.min(28, rows-1))`(`engine/live-budget.ts:58-60`),chrome 本身超预算时「宁可超行也不能让输入框消失」(`live-engine.ts:526`)。rows 很小的终端上会看到 chrome 压掉正文,而不是报错。
6. **流式中断有专门的编舞,但只覆盖「用户主动打断」。** `handleAbort` 的次序敏感段见 `app.ts:2895-2903`;进程崩溃/被 kill 时靠的是 `index.ts:101-103` 的 `process.on('exit')` 兜底关 raw mode——**这条兜底只恢复 raw mode,不恢复光标可见性**(光标恢复在 `dispose()` 末尾,`app.ts:4298-4300`)。异常退出路径上残留隐藏光标是可能的。
7. **审批 60 秒超时会静默取消。** `DEFAULT_APPROVAL_TIMEOUT_MS = 60_000`(`approval-controller.ts:63`),超时 fail-closed 结算 `cancelled`。**离开座位一分钟,这一步就被拒了**,而终端里只看到卡片消失。这是「终端里没有推送通知、只能靠超时收敛」的直接后果(TUI 侧另有 `os-notify.ts` 做「后台完成」的系统通知,审批不在此列)。
8. **切主题会清屏 + 清 scrollback,再整段重放。** `rerenderHistory()` 写 `ERASE_SCREEN + \x1b[3J` 后从会话日志重放(`app.ts:3359-3367`)。日志是权威数据,内容不会丢,但长会话这一下要重放全部历史(见下一条的节流)。
9. **scrollback 的内存副本有上限。** `DEFAULT_SCROLLBACK_MAX_LINES = 1000`(`commit-engine.ts:20`),超出丢最旧条目;`/scroll` 看全文靠另一次从会话日志的读取,不是内存里的副本。
10. **两套版本线在同一个 profile 里。** 官方 16 peers + 21 个 `@huiliyi37/*@0.8.0` 直接依赖;`docs/LOCAL-DEV.md:96` 明确警告还有一条平行生态(`@huiliyi37/dsh-base` 0.2.x,「同源分叉,独立演进」),「两套生态 scope 不同,勿混装」。
11. **文档与实现有漂移,且守护测试只守一半。** `docs/interaction.en.md:13-14`、`:20` 描述了一个「会话标签条」(`Ctrl+X` 循环切换、`Alt+1~9` 跳第 N 个、输入轨上方显示短 id 列表);`src/` 里找不到对应实现——`input-handler.ts:81,159` 只定义了 `ctrl_x` 键名而无消费点,`app.ts:1914` 只剩一条引用已移除函数 `refreshSessionTabs` 的注释,中文手册(`docs/interaction.md`)对此一字未提、与代码一致。守护测试只做 **registry → README(中文)** 的单向检查(`architecture-guards.spec.ts:296-306`),`docs/*.md` 不在守护范围。**判断:英文手册先于实现(或实现已回滚),用户按英文手册按 Ctrl+X 不会有任何反应。**
12. **启动会改自己的 profile。** `runSelfUpdate` 对照 npm latest 直接改写 profile 依赖并可能在空会话时自动重启进程(`index.ts:191-210`、`self-update.ts:1-6`);关闭开关 `DSH_TUI_SKIP_UPDATE=1`,CI/VITEST 下自动 noop。**一个界面插件在启动路径上写安装目录并重启自己,是需要读者知道的默认行为。**
13. **许可证义务随移植而来。** Apache-2.0,`NOTICE` 声明再分发与 §4(b) 修改声明,`SOURCE-MAP.md` 逐文件标 `ported/modified/new`(210 行);`tests/source-map.spec.ts` 校验标注全覆盖。想 fork 它的人继承这套义务。
14. **可调面很宽。** `src/` 有 57 处 `process.env` 读取、12 个专属环境变量(`RIVET_*` 9 个 + `DSH_TUI_*` 3 个:如 `RIVET_ASCII_UI`、`RIVET_IMAGES`、`RIVET_KITTY_KEYBOARD`、`RIVET_AMBIGUOUS_WIDTH`、`DSH_TUI_SKIP_UPDATE`)+ `TuiRunnerConfig` 的 15 个顶层装配字段(`index.ts:26-74`)。灵活,但也意味着排障时状态空间大;**好消息是没有遥测上传**:`RIVET_DEBUG_TELEMETRY` 控制的是本地 `perf_hooks` 采样(`engine/perf-monitor.ts:1-6`),不是上报。
15. **一个进程一个 TTY。** 多会话在同一进程里活着(`ownedHandle` 可 `keepHandle` 让渡给 registry,`app.ts:4230-4232`),切换是 `/session`/`Ctrl+S`;多窗口只能是多个 `dsh --profile tui` 进程,共享同一个 `$DSH_HOME` 的并发行为**未验证**(见「待验证」)。

## 可信度与复现

证据等级 ★★★:DSH 适配层与渲染引擎逐文件读过;`src/pi/latex-to-unicode.ts`(2076 行)、`src/lsp/`(932 行)、`src/commands/registry.ts`(901 行)只读了头注释与调用点,未逐行读;上游 `Tianshu-Tui`(`bc2aa2a0c` 快照)**未读**——所以「哪些是移植、哪些是本仓原创」完全依赖 `SOURCE-MAP.md` 的标注,**没有做同一性核验**(它自己不主张字节同一性,`SOURCE-MAP.md:9-13`)。

```sh
# 1) 克隆与提交
git clone https://github.com/huiliyi37/dsh-tianshu-tui /tmp/an-tianshu
cd /tmp/an-tianshu && git log -1 --format='%H %ad %s'
# → fc6aa32b5c5b4f761db91c14eaf673ec8dba2b1b 2026-11-15 docs(release): 记录 1.0.0-rc.6 已上线

# 2) 规模
find src -name '*.ts' | wc -l                                  # → 181
find src -name '*.ts' -print0 | xargs -0 cat | wc -l           # → 40853
find tests -name '*.spec.ts' | wc -l                           # → 160
find tests -name '*.spec.ts' -print0 | xargs -0 cat | wc -l    # → 41535
wc -l cordis.patch.yml                                         # → 596
wc -c lib/index.js                                             # → 1123521
git ls-files | xargs wc -c | tail -1                            # → 8408925(不含 .git,≈8.0 MB)

# 3) 移植面(17 / 57 / 107)
grep -c '| ported' SOURCE-MAP.md && grep -c '| modified' SOURCE-MAP.md && grep -c '| new' SOURCE-MAP.md

# 4) 零扩散(在 awesome-dsh-plugin 仓库根)
grep -ril 'tianshu' data/plugins/ | wc -l     # → 1(只有它自己)
grep -ril 'tianshu' data/plugins/             # → data/plugins/huiliyi37__dsh-tianshu-tui.yml
grep -rl '天枢' data/plugins/ | wc -l          # → 0

# 5) 「同进程、零 IPC」
grep -rn "from 'node:http'\|from 'node:net'\|createServer\|WebSocket" src | wc -l   # → 0
grep -rn 'ctx.tools\|systemPrompt' src | wc -l                                      # → 0

# 6) 宿主侧硬校验(本机装 dsh)
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh
grep -n 'evaluatePluginCompatibility(bundleManifest\|throw new Error(pluginCompatibilityWarning' \
  $DSH/node_modules/@deepseek-ai/dsh-app-boot/lib/index.js    # → :1025-1026
grep -n 'declares no dsh.bundle' $DSH/node_modules/@deepseek-ai/dsh-plugin-manager/lib/index.js   # → :336(告警)、:1866/:1917(not-a-bundle 拒绝)

# 7) 文档漂移
grep -rn "ctrl_x" src | wc -l                  # → 2(仅键名定义,无消费点)
grep -rn 'refreshSessionTabs' src | wc -l      # → 1(仅注释)
```

**读过的文件**:`package.json`、`cordis.patch.yml`、`README.md`、`ADAPTER.md`、`NOTICE`、`SOURCE-MAP.md`、`docs/architecture.md`、`docs/themes.md`、`docs/interaction.md`、`docs/interaction.en.md`、`docs/LOCAL-DEV.md`(相关段)、`CHANGELOG.md`(版本清单)、`scripts/install-tui.sh`、`scripts/e2e-tui.sh`、`src/index.ts`、`src/ui/app.ts`(attach/dispose/switchSession/feed/重放/rewind/键路由段)、`src/engine/live-engine.ts`、`live-budget.ts`、`write-batcher.ts`、`input-handler.ts`(头与解析段)、`input-line.ts`(头)、`resize-handler.ts`、`commit-engine.ts`、`stream-renderer.ts`、`term-image.ts`、`perf-monitor.ts`、`src/block-stream-writer.ts`、`src/term-caps.ts`、`src/width.ts`、`src/theme-detect.ts`、`src/port.ts`、`src/adapter/{sessions,live,assistant-stream,send}.ts`、`src/controllers/approval-controller.ts`、`src/format/markdown.ts`(头与高亮段)、`tests/{architecture-guards,bundle-contract,loader-composition}.spec.ts`(头部)。

## 待验证

1. **`@huiliyi37/*@0.8.0` 这条线的真实作用面。** patch 只挂了其中 3 个 LSP 包(`cordis.patch.yml:38-57`),打包产物 `lib/index.js` 里也只 import 5 个官方包;其余 18 个 `@huiliyi37/*` 是 LSP 三件套的 peer 树、还是被别的 profile 层挂载,未验证——这决定了「两套版本线」到底有多深。
2. **`dsh.runtime: "host"` 是否真有消费方。** 在 `dsh-app-boot`、`dsh-plugin-manager`、`dsh-plugin-market` 的 `lib/*.js` 里 grep 不到读取点,**判断:可能是给市场/工具读的元数据**,未证实。
3. **版本不匹配的实际体验。** 上面引的是宿主规则与 throw 点,但没在真机跑过「peer 钉 rc.3 + 宿主 rc.5」的组合——是 boot 直接退出、还是 `dsh plugin add` 阶段就拒绝,以及 `allow-version` 后的实际行为,均未实测。
4. **大会话性能。** 历史重放 100 行/片(`app.ts:3330`)、切主题整段重放、CPR 探针 1s 节流,这些在 1 万行会话 + 200 列终端上的实际帧率与首屏延迟,未测;`engine/perf-monitor.ts` 提供了 `p50/p99` 采样点,是现成的测量入口。
5. **审批超时与宿主语义的交互。** TUI 60s 后结算 `cancelled`,宿主侧是重问、还是让该 turn 以失败告终,未验证;这决定「离开一分钟」的代价是一条被拒还是整轮失败。
6. **两个进程共享 `$DSH_HOME` 的并发行为。** 同一 profile 起两个 `dsh --profile tui`(不同终端)时,会话存储的并发写/加锁行为未读也未测;`adapter/sessions.ts` 只保证单进程内「只读日志、不追加事件」。
7. **发布产物与源码是否同步。** `lib/index.js` 跟仓(1 123 521 字节),`tests/bundle-contract.spec.ts` 只校验它的 import 面,不校验它与当前 `src/` 的构建一致性;`npm i` 拿到的 bundle 是否等于 `fc6aa32` 的源码,未验证。
8. **Windows legacy conhost 全链路。** 相关分支(`term-caps.ts:22-30`、宽度 full 档、ASCII 边框)只读了代码,没在真机跑过;这是它自称支持、也是降级逻辑最复杂的一块。
