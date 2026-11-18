# dsh-smooth-stream — 它替换的不只是文字节奏:一个字符揭示时钟 + 一个用合成层 transform 表达的跟随弹簧

> 证据等级:★★★(源码级;`Laplace-bit/dsh-smooth-stream@b93579a01c7c646761a360831b46e91f49114622`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 33 为 2026-08-19 历史采样;下载 937 同为该日。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `Laplace-bit/dsh-smooth-stream`([registry](../../../data/plugins/Laplace-bit__dsh-smooth-stream.yml)) |
| 类目 | ui(2351 条;[census](../../ecosystem/census.py));子分类 [enhance-shell](README.md) |
| 自述 | 「Fluid streaming rendering and smooth scrolling for the DeepSeek Harness Web UI / 流畅流式渲染和丝滑滚动」。源码比自述多三块:markdown 重渲染节流、滚动反压回写揭示速率、无障碍播报与三态动效偏好 |
| 星标 ⚠ | **33**(2026-08-19 冻结采样,建仓第 4 天);**实时 98**(2026-11-18,GitHub API) |
| 下载 ⚠ | **937**(2026-08-19;边车 `data/downloads.json`,npm `last-month` 口径;包首版发布日期未核,见「待验证」) |
| 扩散 | **0**(命令与逐条人工判定见「为什么它突出」) |
| 仓库 commit | `b93579a01c7c646761a360831b46e91f49114622`(2026-11-09,`chore: 发布 0.8.0`);建仓 2026-08-15、默认分支 main、API `size` 44.7 MB(编排者 2026-11-18 取数);本地浅克隆含 `.git` 26 MB |
| 包形态 | npm `dsh-smooth-stream@0.8.0`;`package.json:65-80` 同时声明 `dsh.bundle.patch` 与 `dsh.client`(`platform: 'web'` + 6 个 inject);host 入口 `lib/index.js`、client 入口 `lib/client.js`(`:41-53`) |
| 代码规模 | `src/` **11482** 行 / 42 文件(其中 `src/client/` 10238 行);测试 **8338** 行 / 19 个 `.spec.tsx`。口径:`find src -type f \( -name '*.ts' -o -name '*.tsx' \) \| xargs wc -l \| tail -1`,`tests` 同理 |

## 它到底是什么

**它是一个以浏览器为主战场的双半插件:host 半只有配置与设置通路,渲染与滚动 100% 在 client。** 不是配置包,也不是外部系统适配层。host 入口只有一行 re-export(`src/index.ts:2`),真正的 host 逻辑是 `src/plugin.ts`(355 行)里的三件事:把校验后的 config 注入 index HTML、把用户设置投影成可写文档、提供一个 npm profile 升级端点。没有任何渲染代码在 host 侧。

**它做的事不是 `scroll-behavior: smooth`,是两个独立的自研引擎,而且节拍不同源。**

1. **揭示引擎(字符时钟)**:模型已到达的全文是 `target`,屏幕上是 `displayed`,每帧放出 `target − displayed` 的一部分。核心状态全在 `useSmoothStreamContent.ts`:`displayedContent` 是 React state,`targetCharsRef` 是**按码点切分的字符串数组**,另有 `queueDebtRef` 浮点欠账与三个 EMA(`emaCps`/`arrivalCpsEma`/`chunkSizeEma`)(`useSmoothStreamContent.ts:337-355`)。
2. **跟随引擎(位移时钟)**:真实 scrollport 被压在底部,剩余视觉滞后由一个 `transform` 的位移表达,位移量由半隐式弹簧积分推进(`teleprompterGlide.ts:382-409`,`FOLLOW_SPRING_STIFFNESS=130`/`DAMPING=24`/`SUBSTEPS=4`/`MAX_STEP_MS=32` 在 `:41-45`)。

**三个 preset 是一张常量表,不是形容词**(`useSmoothStreamContent.ts:38-84`):

| preset | defaultCps | maxFlushCps | targetBufferMs | settleAfterMs | settleDrain(ms) |
|---|---|---|---|---|---|
| `realtime` | 120 | 640 | 24 | 200 | 100–280 |
| `balanced` | 80 | 480 | 40 | 280 | 120–420 |
| `silky` | 64 | 400 | 56 | 360 | 160–520 |

**揭示量是三个纯函数算的,不是"每帧固定几个字"**:

- **实时段**:压力曲线 `cps = min(tuning.maxRevealCps, 90 + backlog^1.25 × queuePressure)`,默认上限 600 cps(`:87-90`、`:117-133`);浮点欠账保证 120Hz 下每帧小数部分不丢。
- **稳态(生成长度超出目标滞后)**:`computeRevealStep` 走"跟踪到达率 + 硬追 32 字上限"——`LIVE_LAG_CHAR_CEILING = 32`,超出的部分按 0.15s 追平(`:92-93`、`:243-274`)。
- **收尾段(producer complete)**:换成**有界恒定速度**,由 `computeCompletionDrain` 按 `backlog × 8ms` 估一个截止期,再按 `τ=0.09s` 斜坡爬上去(`:177-195`、`:201-203`),并硬限 400 字/帧防长任务(`:204-210`)。源码注释明确说了为什么不在完成时一把同步:那一次 setState 就是"快流结束时整屏跳一下"的成因(`:408-417`)。

**一个容易看错的点:它并没有把所有动画收进同一个时钟。** `FrameCoordinator` 的文档写着"one document owns exactly one live animation frame"(`FrameCoordinator.ts:1-26`),确实是单例单帧(`:58-65`),但它服务的消费者是跟随弹簧、fps 监控、对数淡出、DOM 文本揭示(`useFpsGuard.ts:63-64`、`useProgressiveDomText.ts:124-190`)。**字符揭示自己另起一条 rAF**(`useSmoothStreamContent.ts:419-554`,`requestAnimationFrame(tick)` 在 `:550`)。所以"统一帧时钟"只覆盖了后三类,揭示仍是独立循环——这是读代码才能发现的边界。

**码点支持是局部的,不是复用的。** 仓库里有一个 145 行的 append-only rope 缓冲,带增量码点→UTF-16 偏移映射(`StreamBuffer.ts:1-7`、`:25-58`、`:97-134`),但 `grep -rn 'StreamBuffer' src tests`**除自身外零命中**;实际路径用 `[...content]` 把文本拆成码点数组再 `slice().join('')`(`useSmoothStreamContent.ts:342`、`:538`、`:587-597`)。判断:这是被保留但未接入的优化件,读卡时不要把它算作生效机制。

## 怎么接进 DSH

**manifest 三处,全是声明式的:**

1. `package.json:65-80`:`dsh.bundle.patch → ./cordis.patch.yml`;`dsh.client.platform: 'web'` + 6 个 inject(`dsh-client-runtime`、`ui-conversation`、`locale`、`connection`、`ui-settings`、`ui-settings-plugins`)。
2. `cordis.patch.yml:2-12`:唯一一条 `insert`,`id: smooth-stream`、`name: dsh-smooth-stream`,config 里给了 `mode/preset: balanced/revealCharsPerSec: 80/scrollSpeedPxPerSec: 48/maxScrollSpeedPxPerSec: 1000/controlScroll: false`。
3. 安装:`pnpm dsh plugin --profile web add dsh-smooth-stream`(`README.md:92`,PATH 里有 dsh 时 `:98`);仓库根另附 `smooth-stream-off.yml`(同一个 `id` + `disabled: true`)作为 A/B 开关。

**host→client 的配置通道只有一条,而且是 HTML 注入。** `apply` 里 `ctx.inject(['webServer'])` 后 `webServer.tapIndex(html => injectStreamConfig(html, …))`(`src/plugin.ts:85-90`),把 schema 校验过的 config 写成一个内联 `<script>window.__DSH_SMOOTH_STREAM_CONFIG__=…</script>`,插在 `<body>` 开标签之后(`boot-config.ts:11-25`;全局名在 `config.ts:55`)。注释解释了为什么必须这样:Web 的 boot 图不带 per-entry config(`config.ts:50-54`)。客户端读不到就走默认值,读到但畸形则**抛错**而不是半配置渲染(`client/index.ts:164-181`)。

**设置是双代适配 + 自建 RPC 通道:**

- 0.1.6 及以前是 settings **registry**(`register(ns, schema, {base})`),0.1.7 换成 **projection**(`describe()`/`update()`,`register` 消失),`settings-bridge.ts:1-33` 头注把这次断裂与"直接调用会让整个 Web 半死掉"的后果写清楚了。适配点在 `createStreamSettingsScope`(`:251-303`):现代 seam 的读必须每帧从 `describe()` 投影,不能缓存 apply 时拿到的 config(`:286-292` 注释)。
- 用户偏好与组合期配置**分成两套类型**:`StreamConfig`(boot global,组合期)与 `StreamSettings`(持久文档,可热改),理由写在 `settings.ts:68-77`。
- 因为核心 settings RPC 会过滤第三方命名空间,插件**自建**一个 loopback RPC 通道 `/smooth-stream`(`settings-api.ts:4-12`),5 个端点 `settings.read/write`、`debug.read/write`、`plugin.upgrade`(`:8-14`)。通道偏好 `connection.rpc.handle()`,拿不到再回退到 webServer 路由,并且回退**只监听 loopback**(`settings-channel.ts:1-16`)。

**客户端注册点(`client/index.ts`,inject 只有 `['slots']`,`:35`):**

| 槽位 / 事件 | 用法 | 位置 |
|---|---|---|
| `conversation.chat.node` | **原地替换**内置 `assistant-step` entry 的 `component`,而非新注册;低优先级影注册只作"宿主还没注册内置行"的回退(`priority: -100`) | `:568-582`、`:584-595` |
| 同上(其它行) | 遍历 `slots.entries`,把 7 个 `SKIP_WRAP` 之外的 Agent 行包一层 `wrapFollowNodeView` | `:123-131`、`:196-227` |
| `settings.plugin.item` | 旧设置卡(keyed slot 形态) | `:430-442` |
| `plugins.bundle.config` | 0.1.7+ 侧栏插件页配置卡 | `:450-455` |
| `conversation.session.header.utilities` | 诊断面板入口 | `:456-462` |
| `conversation.chat.reasoning.body` | 只**探测**是否被第三方替换,被替换就把展开正文交回槽位 | `:341-348`、`:488-500` |
| `slots/changed` | 三处订阅:重扫待包裹行、同步 slot 事实、影注册后升级为原地替换 | `:220`、`:344`、`:607-616` |

**是否 patch:** 不打宿主源码补丁;`cordis.patch.yml` 只是 bundle 插入。真正的接管是**运行时改写 slot entry 的 `component`**(`:579`),并在禁用/卸载时还原(`:597-601`、`:620-626`)。这条还原契约有测试兜底:`renderer-lifecycle.client.spec.tsx:55`/`:62` 分别断言"卸载后"和"关开关后"组件身份恢复。

## 关键实现

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `src/client/teleprompterGlide.ts` | 3360 | 跟随引擎:弹簧、预测 runway、反压、手势释放、scrollport 所有权 | `:41-45` 弹簧常数;`:187-199` reserve;`:345` 反压;`:382` 弹簧步;`:1413` 读者意图;`:1794` hook 入口 |
| `src/client/TypewriterAssistantNodeView.tsx` | 1130 | 接管后的 assistant 行:折叠、块路由、预测换行、播报 | `:60-67` 三态减动;`:94-101` 宽度近似;`:309-318` hooks 串联;`:911-912` 行归属;`:1112` FollowHost |
| `src/client/useSmoothStreamContent.ts` | 630 | 字符揭示时钟与全部纯函数 | `:38-84` preset;`:117`/`:243`/`:177` 三个速率函数;`:419-554` 帧循环 |
| `src/client/useLogarithmicFade.ts` | 690 | 逐字素的对数淡出尾(`FADE_TAIL_SIZE=24`,速度自适应到尾长 160) | `:5-10` 常数;`:23` 曲线;`:15` 排除表 |
| `src/client/TypewriterToolNodeView.tsx` | 237 | 通用行包裹器:透明 renderer 只提速 DOM 文本 | `:122-160` wrap;`:223` 传 controlScroll |
| `src/client/useProgressiveDomText.ts` | 307 | 直接写 `Text.data` 的渐进揭示(MutationObserver + 共享帧) | `:141-162` 写入;`:265-287` 观察;`:289-305` 卸载还原 |
| `src/client/FrameCoordinator.ts` | 183 | 每文档单帧时钟,read/simulate/write 三段 | `:38-65` 单例;`:108-146` tick |
| `src/client/useFpsGuard.ts` | 105 | EMA 帧率守卫 + 离屏判定 | `:15-18` 阈值 30fps;`:100-102` veto |
| `src/client/useDecoupledMarkdown.ts` | 243 | 未闭合代码块内把 markdown 降频到 30Hz | `:112-147` 增量 fence 扫描;`:162-243` 节流 |
| `src/plugin.ts` / `settings-bridge.ts` / `settings-channel.ts` | 355+303+279 | host 半:boot 注入、双代设置投影、loopback RPC | `plugin.ts:85-90`/`:96-354` |
| `tests/*.spec.tsx` | 8338 / 19 文件 | 见「可信度」 | `stream.client.spec.tsx` 4495 行独占一半 |

**一次流式提交的完整链路:**

```
assistant-step 渲染 → configured → TypewriterAssistantNodeView(:899)
  └─ AnimatedMarkdownText(:281)
       useSmoothStreamContent(text, {enabled: typing && !reduced, inputComplete: !streaming})   :309
         └─ 每帧: backlog = target − displayed(:425)
              revealChars = 压力曲线 / 稳态 / 收尾三选一(:461-508)
              targetCharsRef.slice(d, d+n).join('')(:538) → setState → React commit
              useLayoutEffect → onRevealCommit → notifyFollowCommit(:558-563)
       useDecoupledMarkdown(shown, live)(:316) → 未闭合 fence 内 30Hz
       useLogarithmicFade(rootRef, …)(:318)
  └─ FollowHost(:1112) → useConversationFollow(teleprompterGlide:1794)
       弹簧推进 → 写 transform 位移 + 必要时写 scrollTop
       FrameCoordinator 里与 fps/淡出/DOM 文本共享一帧
```

**平滑滚动策略,逐条对账:**

- **粘底**:scrollport 停在 `floor − min(requestedLag, reserve)`,滞后的其余部分由 message row 的 transform 表达,所以"看起来贴着底、实际没到底"(`teleprompterGlide.ts:1557-1572` 注释与实现)。写 `scrollTop` 前用 ledger 比对,发现别人写过就记 `external-scroll` 并让位(`:1365-1373`)。
- **用户上滚**:`wheel`/`touchstart|move|end|cancel`/`pointerdown`/`keydown` 七类事件作为方向性意图,一旦检测到上滚**立即 unpin**(`:24-31` 头注、`:176-186`)。指针/键盘这类没有明确方向的输入退回"用引擎自己写下的 scrollTop 与当前值之差"判断(`:1413`,`FOLLOW_UNPIN_GESTURE_PX=8`,`:80`)。**重新吸附比释放更严格**:读者回到真 floor 才重新接管(`FOLLOW_REPIN_PX=1`、`FOLLOW_HOST_RELEASE_PX=26`,`:82-86`),测试 `stream.client.spec.tsx:2040` 断言"拉到上面后只在回到 floor 才恢复"。
- **高度变化**:一个 `ResizeObserver` 在 layout 后、paint 前把 `animatedH` 复位,避免闪一帧被吸附的画面(`:1-31` 头注);预测性 runway 默认 72px(`FOLLOW_STATUS_RUNWAY_PX`),按揭示速度开合(`computeFollowReserve`,`:187-199`),响应时间 180ms(`:58-60`)。大行(Edit diff、宽工具卡)超出可掩蔽空间时,改用**包裹层真实高度**做 entrance clamp,让 floor 逐渐长(`:1861-1889` 区段注释)。
- **CJK 宽度**:没有文本测量,只有一张近似表——空白 0.33em、ASCII 0.56em、**其它字符按 1em 全宽**(`TypewriterAssistantNodeView.tsx:94-101`),用来判断"缓冲区里的字会不会提前换行",从而决定要不要先开 runway(`:104-123`)。所以中文流式会走"提前开跑道"的分支,但代价是**近似值**,不是实测宽度。
- **反压(两边互相咬合)**:滚动侧算出安全余量占用比,超过 10% 开始、75% 到顶,把揭示速率乘到最低 0.55(`computeFollowRevealScale`,`:345-361`;阈值 `:158-162`),结果通过 `revealScaleRef` 回喂揭示引擎(`useSmoothStreamContent.ts:121-132`、`:502`)。于是"文本越快 → 余量越满 → 揭示越慢",闭环在两处代码之间。

**markdown 与可访问性:**

- markdown 不是逐帧全量重排:只有**未闭合代码围栏**期间才把 markdown 重渲染节流到 33ms/30Hz,闭合或结束时立刻同步(`useDecoupledMarkdown.ts:149-167`、`:222-242`);围栏检测是增量扫描,只走新到的行(`:106-147`)。
- 屏幕阅读器不与视觉揭示共用节拍:独立的 `StreamAnnouncement` 活在 `aria-live` 区域,按最多 320 字符、间隔 800ms 播报,且在标点处切块(`TypewriterAssistantNodeView.tsx:103-107`、`:126-140`);测试 `:1671`/`:1681` 断言"只发一次节点级播报、按节奏增量"。

## 为什么它突出

**星标归属干净,没有主项目可借。** 仓库整个就是这一个插件:没有 monorepo 子目录、没有 `packages/`、host 入口只有一行 re-export。时间线:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-15 | 仓库创建 | 编排者 2026-11-18 取数 |
| **2026-08-19** | **33 星采样点(建仓第 4 天)** | 边车 ⚠ |
| 2026-11-09 | `0.8.0`(当前 HEAD) | `git log -1` |
| 2026-11-18 | **98 星(实时)** | GitHub API |

33 → 98 是 3 倍,且发生在建仓三个月的窗口里;937 下载同样只能记在它自己名下(⚠ 2026-08-19 月窗口值)。

**扩散是 0,而这个 0 有具体形状:**

```sh
grep -ril 'dsh-smooth-stream' data/plugins/ | wc -l   # → 2
grep -ril 'Laplace-bit'      data/plugins/ | wc -l   # → 3
grep -ril 'smooth'           data/plugins/ | wc -l   # → 20
```

逐条看过:

- **自己 1 条**;`dsh-smooth-stream` 的第 2 条是 **同名不同作者** `SpookySandwich/dsh-plugin-smooth-stream`(描述只说"更好的流式文字动画",没有提及本仓库、作者或包名)。
- `Laplace-bit` 的另外 2 条是**同作者兄弟插件**(`dsh-bell-notify`、`dsh-pianist`),属于 owner 级署名,不是第三方引用。
- `smooth` 的另外 18 条按机制分三类:**近义实现 4 家**(`TheGoodMorty/chat-pace` 做定速自动滚动、`TWFU-wcy/dsh-scroll-boost` 做行虚拟化、`ThinkofRain1213/dsh-smooth-cursor-patched` 做光标、`gitByteFree/dsh-mermaid-smooth` 做图表缩放),**反向需求 1 家**(`azazo1/dsh-reduce-effects` 专门**关掉**平滑滚动),其余是描述里出现 smooth 一词的误命中。

结论:**没有一条提到本仓库、作者或包名,也没有 fork。** 形态是"需求被独立复现了 4 次,实现没被引用一次"——说明这一层的可复制性在**手感参数与几何校正**,而那恰好是抄不走的:3360 行跟随引擎里大半在处理"宿主的 floor 什么时候动、动了谁该赔"。

**支撑判断的自身证据(不用星标):**

- **测试比适配层薄不了多少**:8338 行测试对 11482 行 `src/`;单个 `stream.client.spec.tsx` 4495 行。用例名本身即规格:`stream.client.spec.tsx:2040` 读者拉上后只在 floor 恢复、`:2145` 节点 settle 后轻滚轮不被拉回、`:1961` 外部写入多次后交出 scrollport、`:685` 安全间隙变窄前先加反压、`:781` 掉帧时首个恢复帧不许传送、`:269` 120Hz 每帧积分、`:307` 收尾有界排空、`:879-909` 三种减动偏好。
- **单时钟契约有专门的测试文件**:`frame-coordinator.client.spec.tsx:72` 四个任务只arm 一帧、`:83` read/simulate/write 顺序、`:112` 空闲自动停车、`:130` 每文档复用、`:151` 最后一个任务注销即停。
- **几何回归用台架而不是感觉**:仓库自带 `repro/`(1.3 MB 独立复现)、`benchmarks/` 与 40 个 `scripts/`(340 KB),`package.json:89-96` 里 `test:rebound`、`probe:tailbob`、`verify-overflow`、`probe:overlap`、`probe:stability` 都是可执行闸门。
- **机制上不是顺手写的**:收尾排空用"恒定速度 + 指数斜坡"而不是压力曲线,理由写在 `:461-465`(压力曲线在队列变短时会变速,肉眼是"最后几行被踹了一下");揭示速率的增长被 `REVEAL_MAX_GROWTH_MS=32` 夹住,因为"长帧 → 放更多字 → 下一帧更长"是正反馈(`:212-224`);fps 守卫只在**降级且离屏**时才否决提交(`useFpsGuard.ts:100-102`),不是一掉帧就停。

## 代价与边界

- **失败模式(按发生顺序):**
  1. 宿主的 markdown primitive 不可用 → **主动放弃接管**,保留内核渲染,只打一行 warn(`client/index.ts:547-549`)。这是它唯一"优雅退出"的路径。
  2. 设置还在 loading → 不接管(`settings.takeoverEnabled()` 要求 `!pending && enabled`,`:281-284`、`:551-556`);此时界面是原生的,用户看不到"插件已装但没生效"的任何提示。
  3. 无 host 半(单独装 client)→ 读不到 boot global,直接用 client 默认值,默认 preset 是 **`silky`**(`config.ts:43`),比安装态的 `balanced` 更慢(`:164-181`、console.info)。
  4. `slots/changed` 每次触发全量重扫 agent 行,靠 `wrapped` WeakSet 防重复包裹(`:200-217`);slot 频繁变更时有 O(entries) 的重扫成本。
  5. RPC 通道不可写(profile 无编辑文档 / 非 npm 安装)→ 设置卡退化成只读,更新按钮只在 `installation.kind === 'npm'` 时出现(`plugin.ts:117`、`:325-341`)。
  6. `prefers-reduced-motion` 命中(`auto` 模式)或 `force-reduced` → 揭示引擎整体关掉,直接显示原始文本(`TypewriterAssistantNodeView.tsx:38-67`、`:308-310`),`FollowHost` 的 `active` 也置 false(`:1116`)。这是唯一同时关掉文字与滚动的开关。
  7. 帧率 EMA < 30fps **且**回复离屏 → 跳过 DOM 提交,backlog 继续累积,回屏后一次性排(`useFpsGuard.ts:100-102`、`useSmoothStreamContent.ts:519-525`)。
  8. **后台标签页没有专门处理**:`grep -rn 'visibilitychange\|document.hidden' src/` → **0 命中**。切后台再切回,靠的是同一套 rAF 停摆 + `REVEAL_MAX_GROWTH_MS` 夹逼(`:448`),不是 page-visibility 暂停。判断:后台期间 rAF 本来就停,回来首帧的 dt 被夹到 32ms,所以不会有"一次喷完";但也没有"回来时跳到底部"的补偿逻辑,待验证。
- **真实成本在三处:**
  1. **每帧 setState + markdown 重渲染**。揭示是 `setState` 驱动的(`:543`),React 每帧提交一次;`useDecoupledMarkdown` 只压住"未闭合代码块"这一种最坏情况,闭合围栏和表格仍按帧同步。长回复的中段是这台机器最重的时刻。
  2. **码点数组的内存**:`targetCharsRef` 一个码点一个数组元素(`:342`、`:587-597`),长回复是文本长度的 4–8 倍量级(判断:V8 短字符串数组),而不是 `StreamBuffer` 那种按 chunk 的 rope。
  3. **直接写 DOM 文本绕过 React**(`useProgressiveDomText.ts:141-162`):它用 `internalWrites` 弱表识别自己的写入,卸载时只在 `node.data === 自己写过的值` 才还原(`:293-300`)——这是必要的保守,但意味着**任何在它之后同步改同一 Text 节点的代码都会赢**,且它不再尝试覆盖。
- **默认值有三处不一致,装之前要看:**
  - preset:代码默认 `silky`(`config.ts:43`),`cordis.patch.yml:7` 写 `balanced`,README 也说默认 `balanced`(`README.md:131`)。走 bundle patch 安装时以 patch 为准,单独引用 client 时才暴露出 `silky`。
  - `controlScroll`:**legacy settings registry 的 schema 默认 true**(`settings-bridge.ts:94` → `DEFAULT_STREAM_SETTINGS.controlScroll`,`settings.ts:141`),**modern 投影 seam 的 volatile 字段默认 false**(`settings-bridge.ts:139` → `DEFAULT_STREAM_CONFIG.controlScroll`,`config.ts:47`)。两代内核上"插件是否接管滚动"的默认行为相反,而 bundle patch 又显式写了 `false`(`cordis.patch.yml:11`)。判断:0.1.7+ 上默认不接管滚动是刻意收敛的方向(`config.ts:31-37` 注释),但 0.1.6 及更早仍是接管。
  - 三个 `*PxPerSec`/`revealCharsPerSec` 字段**在运行时无人读**:类型注释直接写 "Unused at runtime; kept so existing overlays load"(`config.ts:19-30`),渲染侧只把它们列进 props 且参数名带 `_` 前缀(`TypewriterAssistantNodeView.tsx:841-845`)。改这些数不会改变手感。
- **冲突面**:它假设自己是 `conversation.chat.node` 的最终 owner。原地替换是 last-writer-wins(`client/index.ts:579`),与另一个也做原地替换的插件同时安装时,后挂载的赢且不会报错(判断;它只对 `reasoning.body` 做了"被占就让位"的探测,`:341-348`,对 `chat.node` 没有)。滚动侧同理:它靠 ledger 发现"别人写过 scrollTop"然后交棒(`teleprompterGlide.ts:1365-1373`),但两个插件都写 transform 时没有仲裁。
- **维护成本**:`peerDependencies` 声明了 12 个 `@deepseek-ai/*` 包、全部带 `>=0.1.7-rc.1 <0.2.0 || >=0.2.0-rc.0` 的双区间(`package.json:98-113`);`tsdown.config.ts` 有宿主/client 边界纯净性检查;`lib/` 是构建产物但要一起发(`files` 含 `lib/**/*.js`,`:54-64`)。

## 可信度与复现

- **★★★**:在浅克隆里读了 `src/` 的 14 个文件(全文 12 个):`plugin.ts`、`client/index.ts`、`config.ts`、`settings.ts`、`settings-bridge.ts`、`client/StreamBuffer.ts`、`client/FrameCoordinator.ts`、`client/FollowHost.tsx`、`client/useFpsGuard.ts`、`client/useSmoothStreamContent.ts`、`client/useDecoupledMarkdown.ts`、`client/useProgressiveDomText.ts`、`src/index.ts`、`boot-config.ts`;部分读:`teleprompterGlide.ts`(1-40、176-200、339-410、1794-1900)、`TypewriterAssistantNodeView.tsx`(1-90、280-335、820-960、1100-1130)、`settings-api.ts`、`settings-channel.ts`(头注 + 关键函数)。另读 `cordis.patch.yml`、`package.json`、`smooth-stream-off.yml`、`README.md:73-135`、`tests/frame-coordinator.client.spec.tsx:58-158`。测试只完整读了 1 个文件,其余用 `grep -n 'describe(\|it('` 取用例名。
- **未读**:`docs/`(11 MB,站点与媒体,`size` 的主要来源)、`repro/`、`scripts/`(40 个)、`benchmarks/`、`lib/` 产物、`SmoothStreamCard.tsx`/`SmoothStreamPluginsPage.tsx`/`DebugPanel.tsx`/`locales.ts`/`debugRuntime.ts`/`AnimatedDisclosure.tsx`/`primitives-compat.tsx`/`harnessIcons.ts`/`fold-policy.ts`、`tests/` 其余 18 个文件(仅用例名)。**未运行** `pnpm test`、`pnpm typecheck`、`pnpm build` 与 `repro/` 台架。

```sh
# 1) 提交(浅克隆即可,本卡只用一个 commit)
git -C .work/mine/cards/smooth-stream/repo log -1 --format='%H %ad %s' --date=iso
# → b93579a01c7c646761a360831b46e91f49114622 2026-11-09 10:13:50 +0800 chore: 发布 0.8.0

# 2) 代码规模
find src -type f \( -name '*.ts' -o -name '*.tsx' \) | xargs wc -l | tail -1   # → 11482
find tests -name '*.spec.tsx' | xargs wc -l | tail -1                          # → 8338（19 文件）

# 3) 扩散（在 awesome-dsh-plugin 仓库根执行）
grep -ril 'dsh-smooth-stream' data/plugins/ | wc -l   # → 2（自身 + 同名不同作者）
grep -ril 'Laplace-bit'      data/plugins/ | wc -l   # → 3（自身 + 同作者 2 个兄弟插件）
grep -ril 'smooth'           data/plugins/ | wc -l   # → 20（人工筛:近义 4 + 反向需求 1 + 误命中 13）

# 4) 两个"没人用"的验证
grep -rn 'StreamBuffer' src/ tests/ | grep -v '^src/client/StreamBuffer.ts'   # → 0 命中
grep -rn 'visibilitychange\|document.hidden' src/                             # → 0 命中
```

## 待验证

1. **npm 首版日期**:937 下载是 2026-08-19 的 `last-month` 窗口值,但包首版是 2026-08-1x 还是更早没核(`registry.npmjs.org/dsh-smooth-stream` 的 `time.created`)。若首版晚于 8-19,这 937 也只是"几天"的量。
2. **`controlScroll` 在两代内核上的真实默认**:legacy 默认 true、modern 默认 false(`settings-bridge.ts:94`/`:139`)。需要在 0.1.6 与 0.2.x 各起一次真实 profile,看装完不动机器时滚动到底由谁写 `scrollTop`。
3. **后台标签切回的行为**:代码没有 page-visibility 分支,`REVEAL_MAX_GROWTH_MS=32` 只是夹住单帧。切后台 30 秒再回来,是否会出现一次性大 backlog 排空或视口跳位,需要真机录屏。
4. **两个同样接管 `conversation.chat.node` 的插件同时装**:原地替换是 last-writer-wins,谁的 `component` 最后写进去就是谁。构造一次"两个接管插件 + 先后挂载"的 profile,确认是否有可见的双重包裹或滚动争夺。
5. **CJK 近似宽度在窄栏/等宽字体下的误差**:`approximateInlineWidth` 把非 ASCII 一律按 1em(`TypewriterAssistantNodeView.tsx:94-101`),但中文标点、全角空格、emoji 的实际宽度不同。用 320px 窄栏 + 长中文回复测预测换行是否会误判(该开 runway 没开 / 不该开却开了)。
6. **`pnpm test` 是否真的全绿**:8338 行测试只读了用例名,没跑。尤其 `stream.client.spec.tsx` 依赖 jsdom 里的 `ResizeObserver`/`IntersectionObserver`/帧时钟打桩,这些桩与真实浏览器行为不一致的地方会有假绿。
