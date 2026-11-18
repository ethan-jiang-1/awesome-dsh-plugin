# dsh-visualize — 模型把整段 HTML 当工具参数交出来，宿主只负责把它关进不透明来源的 iframe

> 证据等级:★★★(源码级;`Nagi-ovo/dsh-visualize@6a713a74795fc3043eaad86acf49ac23211ac238`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 180 / 下载无记录,均为 2026-08-19 边车采样;2026-11-18 实时星标 347。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `Nagi-ovo/dsh-visualize`([registry](../../../data/plugins/Nagi-ovo__dsh-visualize.yml)) |
| 类目 | ui([census](../../ecosystem/census.py) 2351 条 / 全表 11 744 条,本类占 20.0%,全表最大) |
| 子分类 | `inline-genui`(内联生成式 UI);⚠ 采样值在本子分类排第二 |
| 自述 | 「对话内生成式 UI:模型把交互式 HTML 卡片直接画进会话流,带流式预览与沙箱渲染」。三项都能落到代码:工具调用产卡、参数流预览、`<iframe sandbox>` + 帧内 CSP |
| 星标 ⚠ | 180(2026-08-19 采样);2026-11-18 实时 **347**(约 1.9 倍) |
| 下载 ⚠ | **无记录**(边车 `data/downloads.json` 没有该 URL,是采样缺口,不是 0) |
| 扩散 | **0**(全表 11 744 条中没有一条点名它;token 与三词筛选见末节) |
| 仓库 commit | `6a713a7`(2026-11-15,`chore: release 0.1.10`);仓库创建 2026-08-13(编排者 API),但**首提交 2026-08-08**,65 个提交全属这一个插件 |
| 包形态 | npm `@nagi-ovo/dsh-visualize@0.1.10`,Cordis **bundle**(`dsh.bundle.patch`)+ 一个 web 客户端半(`dsh.client.platform: "web"`);无任何 runtime 依赖,9 个 peer 依赖全是 `@deepseek-ai/*` 与 react |
| 代码规模 | `src/` **32 文件 9 521 行**(其中 `src/lint.ts` 1817 行);测试 27 个 spec / **5 307 行** / 329 个 `it`;产物 `lib/client.js` 162 033 B(gzip 49 068)、`lib/index.js` 170 924 B(gzip 56 185) |
| 仓库体量 | git 跟踪 **2 092 069 B**(assets/ 988 KB 是演示视频 525 KB + 预览图 247 KB);判断:编排者记录的约 1.3 MB 是打包压缩后的量级 |

## 它到底是什么

**不是适配层,是一个自带协议、自带检查器、自带客户端的完整插件**(node 半 + browser 半),把一个外部概念(Codex 的 `/visualize`)整套搬进了 DSH。核心只有一句话:模型输出的是**一段可以带 `<script>` 的 HTML 正文**,它从不被宿主解析,只被宿主**包进文档、塞进沙箱帧**。

**生成协议:工具调用 + 一个字符串参数,不是围栏,也不是组件 JSON schema。** 三条独立证据:

- 工具签名把整段 markup 声明成 `fragment` 字符串参数,`action` 只有 `create`/`update`,**没有**任何结构化 UI 字段(`src/tool.ts:102-153`)。工具名唯一,叫 `visualize`(`src/fragment.ts:23`)。
- 随包发的技能正文就是写作契约,明确要求「Pass the markup directly as the `fragment` argument」并要求 fragment **不带** `<!doctype>/<html>/<head>/<body>`(`assets/visualize-skill.md:38-42`);文档骨架由宿主补(`src/shell.ts:127-148`)。
- lint 规则表把「带骨架标签」「被 JSON 转义过的 markup」直接判成 error(`src/lint.ts:62-71`,VZ003/VZ004)——反过来说明通道就是字面 HTML 文本,不是 AST。

**一个 fragment 有三条命,别混:**

1. **参数态** — 还在模型输出流里,是不完整 JSON 的一个 `"fragment":"…` 前缀,被浏览器半边收边渲染(`src/fragment.ts:349-389`)。
2. **文件态** — 落定后写进会话级卡片库 `$DSH_HOME/visualize/sessions/<会话>/<slug>-<8hex>.<style>[.page].html`,内容寻址,出了工作区(`src/storage.ts:1-9`、`src/tool.ts:251-258`)。
3. **meta 态** — 同一段 markup 又被投影进 `tool/result` 的持久化 meta(`kind:'visualize'`),重放时只读 meta,不再读文件(`src/tool.ts:195-207`、`src/fragment.ts:50-76`)。

**两条动作,一个循环:**

- `create` 收全量 markup;`update` 收 `path` + 一击命中的 `old_str`/`new_str`,在**文件态**上打补丁(不是模型自己的历史),命中不唯一就直接拒绝并回引卡片真实文本(`src/fragment.ts:132-171`)。名字里记录风格与是否 page,所以补丁不必重述风格(`src/tool.ts:312-331`)。
- `mode` 有三个:`inline`/`wide` 是聊天列里的卡,`page` 在聊天里只放**启动卡**(标题 + 一行 summary + 实时缩略图 + 按钮),真页面在独立标签页里开(`src/tool.ts:125-132`、`src/client/VisualizeCard.tsx:540-569`)。

## 怎么接进 DSH

**manifest 只有两个键。** `package.json` 里 `dsh.bundle.patch → ./cordis.patch.yml` 与 `dsh.client.platform → "web"`(`package.json:46-52`);patch 本身 4 行,一条 `insert`(`cordis.patch.yml:1-4`)。客户端半不是 React 组件库导出,而是被包成 loader 模块:构建时加 `window.__ModuleLoader__.load({ id, factory })` 头尾(`tsdown.config.ts:56-61`),宿主侧 `@deepseek-ai/dsh-client-modules/lib/client.js:1` 正是这个入口,`:758/:874` 会拒绝「加载了却没有注册」的 bundle。

**node 半注册六个东西,全在一个 `apply` 里**(`src/index.ts:75-95`):

| 注册点 | 内容 | 位置 |
|---|---|---|
| `ctx.tools.register` | `visualize` 工具(风格变了就重新注册,因为工具描述里带风格名) | `src/index.ts:81-89` |
| `ctx.skills.registerProvider` | bundled `visualize` 技能,正文 `assets/visualize-skill.md`,末尾拼当前风格说明与用户风格文件 | `src/index.ts:90`、`src/skill.ts:63-82` |
| `webserver/index-inject` | 把 `{ style }` 塞进页面全局,给还在流式渲染的卡用 | `src/index.ts:115-121` |
| `connection.fetch.register` | 设置页的风格文件读写路由 | `src/index.ts:140-153` |
| `connection.fetch.register` | 图片字节路由 `/api/dsh-visualize/image` | `src/index.ts:164-185`、`src/fragment.ts:98` |
| `agent/turn-stopping` + `session/event` | 同回合自我修复(steer) | `src/index.ts:94`、`src/self-repair.ts:385-419` |

`inject = ['tools', 'skills', 'fs']`(`src/index.ts:34`),其余服务(`connection`/`settings`/`uiConversation`/`sessions`)一律**feature-detect 后可选**:缺了就不注册路由、不出设置页、卡片隐藏 prompt 按钮,而不是启动失败(`src/index.ts:142-151`、`src/client/prompt-bridge.ts:146-155`)。

**browser 半占四个坑**(`src/client/index.tsx:75-111`):

- `tool.call.toolview` 的 **keyed** 条目,key 就是 `visualize`——宿主文档写明了 keyed 命中会**替换**通用工具行(`@deepseek-ai/dsh-client-ui-tool/lib/client.js:92`)。
- `conversation.input.dock`(`id: visualize-stream`,order 30):输入框上方的流式预览。
- `conversation.chat.turnTail`(order/priority 100):回合折叠时把这一轮的卡片再贴到最终回答下面。
- 设置分区(风格选择器 + 风格文件编辑器)。

**安装**:`dsh plugin --profile web add @nagi-ovo/dsh-visualize`(README 同时给 GitHub 与本地目录两条);没有服务端、没有端口、没有外部进程,也不需要 API key。

## 关键实现

| 文件 | 行 | 作用 | 关键位置 |
|---|---|---|---|
| `src/index.ts` | 200 | node 入口:工具/skill/路由/自修复 | :34, :75-95 |
| `src/tool.ts` | 430 | `visualize` 工具定义与执行 | :102-153, :190-207, :214-294 |
| `src/fragment.ts` | 409 | 双端共享契约:meta 窄化、补丁、流式抽取 | :132-171, :349-389, :404-409 |
| `src/lint.ts` | 1817 | 静态规则表(11 条 error + 9 条 warn) | :51-155, :1242-1543 |
| `src/lint-gate.ts` | 173 | 闸门 + 每 code 重试熔断 | :32, :67-97, :104-115 |
| `src/shell.ts` | 292 | 帧文档组装、CSP、流式 DOM 同步 | :22-48, :120-149, :210-271 |
| `src/window-doc.ts` | 82 | 新标签页外壳(零脚本) | :20, :44-66 |
| `src/viz-helper.ts` | 492 | 帧内 `dshViz` 运行时 | :100-481, :245-267 |
| `src/storage.ts` | 464 | 会话级卡片库、图片路由 | :45, :108-146, :380 |
| `src/images.ts` | 581 | `data-viz-src` 解析 + SSRF 防护 | :59-67, :502-514, :529 |
| `src/self-repair.ts` | 491 | 回合停止边界的 steer | :89, :148-193, :385-419 |
| `src/skill.ts` | 83 | 技能提供者 | :24, :63-82 |
| `src/client/VisualizeCard.tsx` | 633 | 卡片与 iframe、三道事件桥 | :289-329, :341-372, :577-602 |
| `src/client/StreamingPreview.tsx` | 388 | 关参数流的折叠与预览 | :183-209, :279-334 |
| `src/client/prompt-bridge.ts` | 176 | 卡片→输入框的桥 | :62-109, :146-163 |
| `src/client/card-state.ts` | 294 | 卡片交互状态(宿主 localStorage) | :37, :44, :112 |
| `src/client/TurnCards.tsx` | 182 | 回合尾卡片 | :135-138 |

**数据流(按发生顺序):**

1. 模型先加载 `visualize` 技能,拿到 fragment 契约 + 当前风格说明(`src/skill.ts:70-80`)。
2. 模型发工具调用,fragment 作为参数逐 token 到来。
3. 浏览器半从参数流里扫出 fragment 前缀,**每 150ms 节流**一次推给一个常驻空壳帧(`src/client/StreamingPreview.tsx:219, 313-317`);空壳帧用 `innerHTML` 解析后按 child index 增量同步 DOM,并把已闭合的 `<script>` 克隆成可执行节点插入(`src/shell.ts:210-271`,关键是 :241、:266)。**这一步在 lint 之前发生**。
4. 调用落定 → `execute`:先补丁或取全量,再过大小/规则闸门(`src/tool.ts:246`、`src/lint-gate.ts:67-97`),再解析图片(`src/tool.ts:265-273`),再写内容寻址文件,返回**一行确认**+持久化 meta(`src/tool.ts:190-207, 360-369`)。
5. 卡片按 meta 重建帧文档:宿主 `--dsw-alias-*` 设计变量 → 帧内 `--dsh-viz-*`,风格变量覆盖其上,再拼 fragment 与 `CSP meta`,整体作为 `srcDoc`(`src/shell.ts:120-149`、`src/client/theme.ts:14-21`)。
6. 帧内 `postMessage` 三条通道回父页:高度(ResizeObserver 持续上报)、`dshViz.prompt`(写字),`dshViz.state`(存状态)。
7. 回合结束:宿主默认折叠过程行,于是 turnTail 再渲染一次同一批卡片;若 toolview 卡片当前可见,尾巴跳过它(`src/client/shown-cards.ts:1-40`、`src/client/TurnCards.tsx:135-138`)。

**lint 是这个插件的第二引擎**(1817 行,占源码 19%)。它没有 HTML/JS parser:一次线性扫描切出 markup/注释/`<script>`/`<style>`,再各自 tokenize 到「能分清代码与字符串、注释、正则字面量」为止(`src/lint.ts:1-22`)。规则表 11 条 error(VZ001-VZ011)+ 9 条 warn(VZ101+)——error 拒绝调用、什么都不写;warn 只随结果回给模型(`src/lint.ts:51-155`)。error 规则一旦「读不准」(变量遮蔽、属性链、两种解析)自动降级为同名 warn,注释里写明取舍:**误杀会挡掉合法卡片,漏放只是把一部分交给 CSP**(`src/lint.ts:6-12`、`:1464-1543`)。

**熔断有三层:** 同一 error code 连续 3 次拒绝就追加「STOP,别再调了,直接告诉用户」(`src/lint-gate.ts:32, 88-95`);`update` 时旧卡片本来就有的 finding 降级为 warn,避免一次补丁被迫修完全部旧账(`src/lint-gate.ts:127-162`);`selfRepair` 每回合最多 2 次 steer、同一指纹只触发一次(`src/self-repair.ts:89, 402-418`)。

**测试能证明契约**:329 个用例里,`lint-adversarial.spec.ts` 专门跑「接近 1 MB 的敌意输入不超时、不抛异常」并把预算写成可复现的 200ms(含 140k CSS 声明、64000 个 `/[`、300k 嵌套模板);`storage.spec.ts` 覆盖 `..`、符号链接逃逸、store 外文件拒读;`images.spec.ts` 覆盖 loopback/内网/metadata 目标与逐跳重定向检查;`prompt-bridge.spec.tsx` 覆盖 token/窗口/长度/忙闲/保留读者草稿;`frame-state.spec.tsx` 覆盖「状态烤进文档也不能闭合 script」。

## 为什么它突出

**星标归属没有争议,这在这批条目里少见。** 全仓 65 个提交、最早一条就是 `dsh-visualize v0.1: inline generative UI plugin for DSH`(2026-08-08),之后每一条都在这个插件上;没有主项目、没有 monorepo 子目录、没有第二个产品可以借星。所以 180 ⚠ 与 347 实时都记在插件本身。

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-08 | 首个提交(v0.1) | `git log --reverse` |
| 2026-08-13 | 仓库公开/创建 | 编排者 API;与首提交相差 5 天,判断为「先私有开发后公开」 |
| **2026-08-19** | **180 星采样点** | 边车 ⚠ |
| 2026-10-17 ~ 10-18 | v0.1.5 → v0.1.7,两天 20 个提交,是三个月里最密的一簇 | `refs/tags` |
| 2026-11-15 | v0.1.10 | `git log -1` |
| 2026-11-18 | 347 星(实时)、发布 3 个月 | GitHub API |

**扩散 0,而且不是 grep 漏。** 见末节的三个 token:点名 `dsh-visualize` 的只有它自己。为什么零:一是**没有可仿的接缝**——它不暴露 service key、不挂 MCP、不给其他插件留 API,能复用的只有导出的 `validateFragment`/`visualizeMetaFrom` 几个纯函数(`src/index.ts:24-29`),抄不走形状;二是**仿制成本等于重写 9.5k 行**——协议、CSP 帧、1817 行 lint、流式同步、SSRF 防护,少一样都跑不起来;三是它的价值在「装上去就有一整套体验」,用户没有理由再包一层。同类独立实现确实存在(registry 里另有一条自述同样强调"沙箱 HTML 卡片"的条目),但**没有一条点名它**,所以扩散按口径仍是 0——这两件事要分开写。

**路线差异(只讲机制)。** 生成式 UI 有两条根本不同的路:

- **任意 HTML + 不透明来源沙箱(本插件)**:模型产出的是一个**程序**(HTML/CSS/JS 文本),宿主不解释它,只负责包文档、上 CSP、塞 iframe。能力上限等于浏览器减去 CSP/沙箱:canvas、WebGL、WASM、任意 CDN 图表库都能用;代价是宿主**对画出来的东西一无所知**——没有元素树、没有事件 schema、没有可访问性映射,任何要回到宿主的信息都只能是**一段字符串**,靠 `postMessage` 隧道传,且每个通道都要自己重做鉴权、限长、限频。设计系统只能靠约定复用(CSS 变量桥 + 213 行基础样式表),不能靠类型。
- **声明式组件 JSON + 宿主 React(另一条路)**:模型产出的是**数据**,宿主按 schema 把节点映射到自己的组件,渲染在同源 DOM 里。宿主知道整棵树,因此可以结构化校验、可以用类型约束交互回调、可以天然复用主题与可访问性;代价是能力被组件集写死(想做模拟器就得有对应组件),每加一种表达力都要发一个组件 + 一个 schema 版本,而且一旦渲染层有 bug 就是同源失守。

两边的成本刚好互补:前者把成本放在**安全与策略层**(CSP、沙箱、lint、隧道协议、流式预览),后者放在**组件与 schema 演进**。本插件选了前者,所以它的源码里最厚的两个文件是 `lint.ts`(1817)和 `VisualizeCard.tsx`(633),而不是组件库。

**判断:是本子分类的机制样本,不是生态锚。** 声量中等(180 ⚠ / 347 实时)、扩散为零,但它的实现完整度与安全工程密度,在本子分类里属于少见的量级;它的可借鉴之处不在 UI,而在**把一个不可信执行体接进宿主时,需要补哪些层**。

## 代价与边界

**失败模式,按发生顺序:**

1. **客户端半没加载**(非 web 面、旧宿主、安装后没刷新):工具照常返回一行文本,卡片不出现——这是设计好的降级(`src/index.ts:1-7`、`src/client/VisualizeCard.tsx:592-596`)。
2. **生成中途被打断**:参数 JSON 不完整时不会落卡;流式预览随调用卸载(`src/fragment.ts:269-287`、`src/client/StreamingPreview.tsx:356-364`)。
3. **lint error**:调用直接失败、不写文件、不渲染;模型必须在同回合改。连续 3 次同 code 会被勒令停手(`src/lint-gate.ts:32, 88-95`)——用户看到的是"这次没有卡片,只有一句话"。
4. **补丁打不上**:`old_str` 不唯一或不匹配就抛错并回引真实字节,模型若继续错就会耗尽上下文(`src/fragment.ts:132-171`)。
5. **图片取不到**:占位框 + 结果里写原因(逐图失败不拖垮整卡);宿主没有 `/api` 通道时直接报"无法投递图片"而不是白存字节(`src/tool.ts:78-79, 265-280`)。
6. **状态存不下**(隐私模式/配额满):退回内存态,刷新即失(`src/client/card-state.ts:1-30`)。

**体积与存储。** 无 runtime 依赖,但代价转移到了两处:浏览器半 162 KB(gzip 49 KB)要单独下载并求值,且强依赖宿主冻结的模块表(React/Cordis/UI 包,`tsdown.config.ts:14-25`),宿主升级 UI 包就可能要重发版;卡片正文在 `$DSH_HOME/visualize` 下**只增不减**(README 明说不会自动清理),同时会话日志里还有两份(fragment 参数 + result meta),单卡上限默认 1 MB(`src/index.ts:63`)。

**版本兼容成本是真实的。** 代码里同时存在 dsh 0.1.1 / 0.1.2 / 0.1.5 / 0.1.6 / 0.1.7 / 0.2.1 六代分叉判断:折叠偏好在两代 settings 服务间切换(`src/client/folding.ts:1-15`)、turnTail 的 chain/list 两种注册形状(`src/client/index.tsx:44-52`)、流式片段的三种来源(`src/client/StreamingPreview.tsx:11-19`)、session 事件的两代 payload(`src/self-repair.ts:300-328`)。README 自述兼容 0.1.1-rc.2 → 0.2.2-rc.3,这些分支就是代价。

### 安全边界(本卡重点)

**三道隔离,缺一不可:**

1. **`<iframe sandbox="allow-scripts">`,没有 `allow-same-origin`**(`src/window-doc.ts:20`、`src/client/VisualizeCard.tsx:365`)。没有同源 ⇒ 帧是不透明来源,读不到宿主 DOM、cookie、`localStorage`;同时也没有 `allow-popups`/`allow-forms`/`allow-modals`/`allow-downloads`/`allow-top-navigation`,所以不能开窗、不能提交表单、不能导航顶层。
2. **帧文档自带 CSP**(写在 `srcdoc` 里,`src/shell.ts:35-48`、:133):`default-src 'none'`;`script-src` 允许 inline、`eval`、wasm 与 7 个 CDN;`style/img/font/media` 同样只允许 `blob: data:` + 7 个 CDN;`worker-src blob:`;**`connect-src blob: data:`(即 fetch/XHR/WebSocket 一律不可用)**;`frame-src/object-src/base-uri/form-action` 全 `'none'`。测试钉住了这几条(`tests/shell.spec.ts:15-19`)。
3. **fragment 从不进入宿主文档**。父页面这条路径上没有 `dangerouslySetInnerHTML`;fragment 只出现在两个地方:iframe 的 `srcDoc`(浏览器按文档解析,不参与宿主文档解析),以及"新标签页"外壳里**转义后的 `srcdoc` 属性**(`src/window-doc.ts:63, 75-82`)。而那个外壳页**零脚本、零模型文本**,只有一个全视口 iframe——因为 Blob URL 由宿主页面创建、天然带宿主来源,作者在注释里写明了这一点(`src/window-doc.ts:1-15`),`tests/window-doc.spec.ts:24-38` 断言外壳里 `script`/`img` 数量为 0。

**所以恶意卡片能做什么:** 在**自己的**不透明来源里跑任意 JS、画 canvas/WebGL、跑 WASM、从 7 个 CDN 拉静态资源(且 lint 要求版本 pin,VZ006)、用 `postMessage` 对父页说话。**不能做:** 读宿主 DOM 与凭据、读宿主 storage、发网络请求、嵌 frame、提交表单、跳顶层、开新窗口、下载文件。它也无法自己持久化状态——状态由父页收下并写进宿主的 `localStorage`,key 由父页决定,帧内 `localStorage` 只会抛 `SecurityError`(`src/lint.ts:1244-1248` 的 VZ108 注释就是这么写的)。

**回环:卡片无法自己触发模型。** 三条通道都在父侧设闸:

| 通道 | 父侧校验 | 后果 |
|---|---|---|
| 高度 | 只校验 `type` + token,写入 `HEIGHT_CAP`(inline 800/wide 1200/page 800) | 只改 frame 高度(`src/client/VisualizeCard.tsx:58, 346-357`) |
| `dshViz.prompt` | `event.source === 本帧 window` + token + **该帧持有焦点** + `navigator.userActivation` + 300ms 间隔 + 2000 字符 + 只写**空草稿或卡片自己上次写的草稿** + 永不代发 | 只能产出一条**用户可编辑的草稿**;发送仍由人点(`src/client/prompt-bridge.ts:26-32, 62-109`、`src/client/VisualizeCard.tsx:312-329`) |
| `dshViz.state` | `event.source` + token + 16 KB/卡、256 KB 总量 + key 由父页按 `session+path` 算 | 只能写自己那张卡的状态(`src/client/card-state.ts:37, 44, 112`、`src/client/VisualizeCard.tsx:289-301`) |

换句话说:**卡片造成的"新 turn"只可能由人产生**(点击 → 草稿 → 人按发送)。唯一的自动回环在宿主侧,是 `agent/turn-stopping` 上的一次 steer,与卡片运行时无关,且 subagent 跳过、每轮上限 2 次、指纹去重(`src/self-repair.ts:385-419`)。

**残余风险,按可利用性排序(都有源码位置):**

- **预览先于校验。** 生成过程中,已闭合的 `<script>` 会被克隆成可执行节点插入空壳帧(`src/shell.ts:225-235, 241`),而 lint 只在 `execute` 里跑(`src/tool.ts:246`)。所以 **CSP + 沙箱是唯一的安全边界,lint 只是质量闸门**。任何把 lint 当成安全措施的读法都是错的。
- **CDN 允许列表是一条单向外带通道。** `img-src`/`script-src` 允许 7 个 CDN(`src/shell.ts:22-40`),卡片可以把自带数据编码进 CDN 的路径/查询串发出去;`connect-src` 只挡了 fetch/XHR/WS,挡不住 `<img src>`。lint 的 `reportUrl` 只查字面量,拼接出来的 URL 读不准(`src/lint.ts:1117-1160`,JS 侧 `img.src = …` 仅 warn)。能外带的是**模型自己写的内容 + 已被烤进文档的已保存状态**(`src/viz-helper.ts:108`、`src/shell.ts:103, 138-141`),**不含**宿主凭据。这是"沙箱挡住宿主、挡不住模型把自己看到的东西送出去"。
- **`postMessage` 用 `'*'` 作目标源。** 两条帧→父消息都以 `'*'` 发出(`src/viz-helper.ts:250, 264`)。帧是不透明来源,确实无法指名父来源,但结果是**页面上任何脚本(宿主或其他插件的客户端半)都能收到**卡片状态与 prompt 文本。
- **高度通道不校验 `event.source`**,只校验 type + token(`src/client/VisualizeCard.tsx:346-357`),与 prompt/state 两条(:294、:318)不一致。token 就是 callId,虽然写进了每张卡自己的文档里(等于半公开),但要跨卡利用仍需知道另一个卡片帧的 callId,后果也仅限于把某帧高度改到 cap 以内。**判断:一致性缺陷,不是越权。**
- **CDN 脚本等于帧内任意代码。** `script-src` 放行 jsdelivr/unpkg/esm.sh,模型可以引任意第三方包——这只是把"模型写的代码"换成"模型挑的代码",仍在同一不透明来源里;真正的边界是"这个来源能不能碰到宿主",答案是不能。
- **工作区风格文件会进入技能正文。** `<workspace>/.dsh/visualize-style.md` 与 `<DSH_HOME>/visualize/style.md` 的文本被拼进模型加载的技能,单文件上限 4096 B(`src/style-guide.ts:28-35`)。这是一条**持久化的提示注入面**:往仓库里塞一个风格文件,就能影响之后每次画卡。它属于 token 级风险,不是代码级。
- **新标签页外壳与 DSH 同源。** 现在它零脚本、fragment 只在转义后的 `srcdoc` 里,是安全的设计;但这条边界靠"不要往外壳里加脚本"维持,一旦有人加了,就是同源失守(`src/window-doc.ts:5-13`)。
- **服务端侧的两处防护是加分的**:图片在 DNS 解析钩子里逐地址判公网、字面量 IP 先判、逐跳重定向都判(`src/images.ts:502-514, 529`);卡片库只按规范 id 打开文件、`update` 路径要过 `..`/`~`/符号链接三关(`src/storage.ts:108-146, 380`)。

## 可信度与复现

**★★★,只限这个插件自身**:node 半与 browser 半全部打开读过(`src/` 32 个文件;核心 20 个逐行读,含 1817 行的 `lint.ts` 主结构与全部规则定义);测试读的是用例清单与关键断言,**没有跑 vitest**;没有在真实浏览器里加载过恶意 fragment。与本机 DSH 官方包的对照只用于确认接缝:`dsh-client-ui-tool` 的 keyed toolview 语义、`dsh-client-modules` 的 loader 契约。

```sh
# 1) 克隆与提交
git clone --depth 1 https://github.com/Nagi-ovo/dsh-visualize.git /tmp/an-visualize
cd /tmp/an-visualize && git log -1 --format='%H %ad %s'
# → 6a713a74795fc3043eaad86acf49ac23211ac238 2026-11-15 23:07:54 +0000 chore: release 0.1.10
git fetch --unshallow --filter=blob:none && git rev-list --count HEAD   # → 65
git log --reverse --format='%h %ad %s' --date=short | head -1          # → 33f9238 2026-08-08 dsh-visualize v0.1…

# 2) 规模
cat src/*.ts src/client/*.ts src/client/*.tsx | wc -l                   # → 9521(32 文件,不含测试)
wc -l src/lint.ts                                                      # → 1817
ls tests/*.spec.* | wc -l                                              # → 27
grep -rE "^[[:space:]]*(it|it\.each)\(" tests/*.spec.* | wc -l          # → 329
gzip -c lib/client.js | wc -c                                          # → 49068(原始 162033)
git ls-files | xargs wc -c | tail -1                                   # → 2092069

# 3) 扩散(在 awesome-dsh-plugin 仓库根;data/plugins 有 11744 个文件,
#    必须用目录形式,展开文件名会 Argument list too long)
grep -ril 'dsh-visualize' data/plugins/ | wc -l                        # → 1(只有它自己)
grep -ril 'Nagi-ovo' data/plugins/ | wc -l                             # → 2(另一个是同作者的 dsh-ads,不是衍生)
grep -ril 'visualize' data/plugins/ | wc -l                            # → 17,逐条人工判读见下

# 4) 沙箱与 CSP
grep -n "allow-scripts\|FRAME_SANDBOX" src/window-doc.ts src/client/VisualizeCard.tsx
grep -n "connect-src\|frame-src\|default-src" src/shell.ts             # → :36, :43-44
grep -n "event.source !== frame.contentWindow" src/client/VisualizeCard.tsx  # → :294, :318
```

**`visualize` 的 17 个命中怎么筛。** 这个词本身是通用动词,不能直接报数。逐条读 `data/plugins/` 里的 `description` 后,17 = **自身 1** + 三类第三方:① **12 条**是别的插件在自述里用英文动词(「visualizes token usage」「audio visualizer」「memory nebula」),与本插件无关;② **3 条**是路径/包名里带 `visualize` 的独立项目(`zhangj1164/…openwiki-visualize` 是 OpenWiki 阅读器,`xuanyuanchumo/dsh-codegraph-visualizer`、`darkneu/dsh-finesse-visualizer` 名字里的 visualizer 说的是"画图工具"),不是本插件;③ **1 条**是同机制的独立实现(`tonebean/dsh-inline-visualizer` 自述"sandboxed HTML card in place inside the conversation"),**但它没有点名本插件,也没有引用它**。所以第三方提及 = **0**;`Nagi-ovo` 的第二条命中是同作者的另一个插件(`dsh-ads`),不算衍生。

**未读**:`assets/references/{charts,design}.md`、5 个 `assets/styles/*.md` 与两个示例 HTML 只看了目录与引用关系,没逐行读;`src/client/VisualizeSection.tsx`(559 行设置页)与 `settings.tsx`/`settings-locale.ts` 只看了入口;`frame-css.ts` 213 行只读了 token 段。**所以"卡片好不好看/图表默认值调得如何"这类判断不在本卡范围内。**

## 待验证

1. **真浏览器里的沙箱行为**:jsdom 能证明属性与文档结构,证明不了 Chrome 真的拦住了 `fetch`、`window.open`、`top.location`、表单提交。需要一个恶意 fragment 的实测矩阵(每项一条,期望"被拦")。
2. **CDN 外带通道是否真能打通**:构造一个把 `dshViz.state` 编码进 `cdn.jsdelivr.net/npm/<pkg>/<base64>` 的卡片,看请求是否发出、是否带 referer(帧已设 `no-referrer`)。目前结论只有 CSP 文本依据。
3. **`srcdoc` 里 CSP meta 的实际生效边界**:`worker-src blob:` 是否允许新起 worker、`base-uri 'none'` 是否覆盖 `document.write` 场景,均未实测。
4. **高度通道缺 `event.source` 的可利用性**:需要先知道另一个卡片帧的 callId;同页多卡时 callId 是否出现在 DOM 属性里(React props 不落地,但 React DevTools 可见),未验证。
5. **桌面端已知问题**:README 说桌面端"在新窗口打开"与"打开页面"无反应;代码只做了 `typeof window.open === 'function' && typeof URL.createObjectURL === 'function'` 的特性探测(`src/client/VisualizeCard.tsx:146-148`),真正的失效原因没在源码里找到。
6. **星标曲线**:180(08-19)→ 347(11-18)之间没有中间采样,分不清"发布日暴涨后平台期"还是"持续慢涨";需要 stargazers API 或 star-history。
7. **兼容矩阵**:README 自述 0.1.1-rc.2 → 0.2.2-rc.3,但代码里的六代分叉只做了静态阅读,没有在 0.1.1 / 0.1.7 / 0.2.1 三个真实宿主上装一遍验证降级路径。
