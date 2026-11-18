# dsh-genui — 模型写 `dsh-ui` JSON 围栏,宿主页面里挂 React 树

> 证据等级:★★★(源码级;`omdsh-dev/dsh-genui@382a4a6149c0f7c0926104d4e49d1d0805aa9e00`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-18)。⚠ 星标 224 为 2026-08-19 历史采样;下载边车无记录。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `omdsh-dev/dsh-genui`([registry](../../../data/plugins/omdsh-dev__dsh-genui.yml)) |
| 类目 | ui([census](../../ecosystem/census.py) 2351 条 / 全表 11 744 条) |
| 子分类 | `inline-genui`([本册](./README.md));成员表里另外两条 ⚠ 180 / 41,本卡按 2026-11-18 实时值是本子分类唯一已知千星 |
| 自述 | 回复内联的可交互 UI:布局、图表、表单、测验、mermaid、3D,以及动作回传模型的循环(registry `description`) |
| 星标 ⚠ | **224**(2026-08-19 冻结采样);**2026-11-18 实时 1014**(编排者当日 GitHub API;本卡复核为 1015,同一日波动) |
| 下载 ⚠ | 边车无记录(2026-08-19 采样缺口,不写成 0) |
| 扩散 | **3 个依赖/伴生 + 3 个同类独立实现 + 4 个互操作提及 = 10 个第三方条目**;原始 `grep -ril 'genui' data/plugins/` 22 条,其中 11 条是 `genuine/genuinely` 子串假阳性。逐条分类与命令见「为什么它突出」和末节 |
| 仓库 commit | `382a4a6149c0f7c0926104d4e49d1d0805aa9e00`(2026-11-18,`main`,merge PR #451);822 个提交 / 32 个 tag / v0.16.0 |
| 仓库时间线 | GitHub `created_at` 2026-08-13;最早提交 2026-08-09;首屏采样时仓库只有 6 天 |
| 包形态 | npm `@changfenhuang/dsh-genui@0.16.0`;`dsh.bundle.patch` → `cordis.patch.yml` + `dsh.client.platform=web`;一份包同时是 node 插件、浏览器渲染器、`SKILL.md` 与懒加载资产宿主 |
| 代码规模 | TypeScript `src/**/*.{ts,tsx}` **33 821 行**;测试 161 个 spec / 28 655 行;仓库 584 个文件、工作树 21 MB(GitHub API 23 956 KB ≈ 24 MB) |
| 依赖 | 运行时依赖只有 3 个:`katex`、`mdast-util-from-markdown`、`react`(`package.json:77-80`);另声明 19 个 DSH 包 + react 的 optional peer(`package.json:82-103`) |

## 它到底是什么

**不是一个"UI 组件库",也不是配置包,而是一套输出协议 + 一个浏览器渲染器 + 一个宿主侧教学插件。** 模型仍然只产出文本:回复正文里写一个 `dsh-ui` 围栏,围栏体是 JSON;浏览器半在 DSH 会话 DOM 里发现这个代码块,把它换成一棵 React 树。仓库同时带一个 `genui` skill、一个 `render_ui` 工具、一个面板通道和一个 dsh-go 原生桥,但主通道不需要任何工具调用——没有 tools 服务的宿主照样能渲染围栏(`src/plugin/index.ts:186-191`)。

协议的事实边界在三个文件里:

- **围栏语言**:`dsh-ui`(容忍大小写与尾部标点;`dsh-ui-dark` 不会被误认)——`src/shared/fence-language.ts:8-29`。
- **spec 根**:`{ title?, gap?, panel?, append?, computed?, items: GenuiNode[] }`——`src/client/spec.ts:142-162`;`panel:true` 走会话面板,`append:true` 追加,`computed` 是输入驱动的本地计算公式。
- **组件注册表**:手写的 `COMPONENT_SCHEMAS`,不是从 TypeScript interface 推断的 JSON Schema——`src/client/genui-runtime/schema.ts:325-475`;`COMPONENT_SCHEMAS` 在 `:478-483` 汇总。当前 **60 个 type**(统计命令见末节):布局 `row/col/grid/card/carousel/tabs/accordion`、文本与展示 `text/callout/table/list/keyvalue/steps/timeline/badge/stat/hero/progress/diff/json/code/file-tree/icon/blocks`、图表 `chart/plot/echart/map`、交互 `button/input/select/checkbox/radio/switch/slider/textarea/editor/date-picker/segmented-control/copy/link/submit/popover/choices`、高级 `svg/mermaid/diagram/scene3d/quiz/entity-card/audio/video` 等(`SKILL.md:42-50` 给了同一份分组)。

**模型怎么知道该写什么**:系统提示里只放一个约 1.6 KB 的 `genui:fence` 段,教围栏语法、规模和 MUST 规则,并要求模型先调 `skill` 工具加载 `genui`(`src/plugin/index.ts:131-161`);组件字段的正文在随包发布的 `SKILL.md`(429 行 / 64 KB),通过 `skills.registerProvider` 以 `source: 'bundled'`、rank 600 注册(`src/plugin/index.ts:252-281, 382-384`)。`genui:reference` 段在随包 skill 可用时通常为空(只有被同名 skill 遮蔽、缺章节时才补);宿主没有 skill 工具时退化为短版 `GENUI_QUICK_REFERENCE`(`src/plugin/index.ts:172-178, 344-357`);测试把 full 档钉在 1600 字符、minimal 档 300 字符、无 skill 回退总计 3400 字符以内(`tests/plugin-genui.spec.ts:141-170`)。所以它**不是把 60 个组件的 schema 塞进每轮系统提示**,而是按需加载一份 64 KB 的 skill。

**为什么 JSON 能稳定渲染**:模型输出的 JSON 默认不可信,渲染前统一走 `processGenuiSpec`(`src/client/guard.ts:2037-2100`):别名归一化 → `repairGenuiSpec` 确定性修复(丢坏节点、截断超长、夹紧数值)→ `validateCanonicalGenuiSpec` 校验字段类型/枚举/引用 → 计数与诊断。未知 type 在校验阶段报错、在修复阶段被丢弃(`src/client/guard.ts:1-17`);围栏通道随后调用 `partialRepairGenuiSpec`,按错误路径丢掉坏节点再跑一遍,**一个坏组件不会拖垮整块 UI**(`:2174-2220`)。如果根都修不好,保留原代码块并在上面挂一条可见诊断(`src/client/fence-render.tsx:186-189`);渲染分发器对漏网的未知 type 还有最后一层 `err.unknownType`(`src/client/blocks/render-node.tsx:649`)。

**第二条通道**:`render_ui` 工具,参数是 `{ spec: <object> }` 的宽松 JSON Schema——schema 故意不拒绝 guard 能修的东西,只挡住"把 spec 序列化成字符串"这类不可修的形态(`src/plugin/tool.ts:20-79`)。工具结果把修好的 spec 放进 `presentationMeta`,浏览器 `tool.call.toolview` 槽位按 `key: 'render_ui'` 取出来渲染(`src/plugin/tool.ts:205-256`;`src/client/index.tsx:186-199`)。第三条是面板:`panel:true` 的围栏或 `render_ui` 结果都会发布到会话面板 store,由输入框上方的 dock 渲染(`src/client/index.tsx:200-210`;`src/client/panel-store.ts:1-17`)。

## 怎么接进 DSH

**manifest 是标准的 bundle + client 双声明**,没有私有安装器:

| 接点 | 内容 | 证据 |
|---|---|---|
| bundle patch | 9 行 YAML,一条 `insert`:`id: genui`、`name: '@changfenhuang/dsh-genui'` | `cordis.patch.yml:7-9` |
| package 双声明 | `dsh.bundle.patch` 指 patch;`dsh.client = { inject: [], platform: 'web' }` | `package.json:203-210` |
| 浏览器入口 | `exports["./client"]` → `lib/client.js`;宿主 client-modules 只读 `dsh.client` 且要求存在 `./client` 导出 | `package.json:14-17`;宿主源码 `dsh-client-modules/lib/index.js:731-739` |
| node 入口 | `main: lib/index.js`,由 `src/index.ts` 转发 `src/plugin/index.ts` | `package.json:7`;`src/index.ts:1-9` |
| 版本门槛 | `engines.dsh` 允许 `0.2.0-rc.1 / 0.2.1-rc.1 / 0.2.2-alpha.2` 三条线;Node 22.19+ 或 24+ | `package.json:213-217` |

**宿主侧(node half)注册了七样东西**,全部是 Cordis 原生机制,没有改宿主源码:

1. **系统提示**:`ctx.systemPrompt.section` 两个段,order 取 `getSectionOrder('STRUCTURED_OUTPUT')`——`genui:reference` 与 `genui:fence`(`src/plugin/index.ts:313-325`);`system-prompt/assemble` 钩子再按 skill 可见性替换占位文本(`:326-366`)。
2. **bundled skill**:`skills.registerProvider`,把 `SKILL.md` 作为 `source: 'bundled'` 的 `genui` skill 暴露给模型;描述从 frontmatter 读,避免代码里维护第二份文案(`src/plugin/index.ts:218-281, 382-384`)。
3. **工具**:`ctx.inject(['tools'])` 依赖 fiber,注册 `render_ui` 与 `validate_dsh_ui`;`renderUiTool:false` 只关第一个(`src/plugin/index.ts:373-379`;`src/plugin/tool.ts:205, 369`)。
4. **懒加载资产路由**:可选 `webServer` 服务,注册前缀 `/plugins/@changfenhuang/dsh-genui/assets`,只接受扁平的 `*.js` 文件名,ETag + `?rev=` 缓存(`src/plugin/index.ts:43-100, 388-392`)。
5. **回合尾修正**:`installFenceFeedback`,默认开启,监听 `agent/turn-stopping`(`src/plugin/index.ts:369`;详见「事件回环」)。
6. **dsh-go 原生桥**:可选 `dshGo` 服务,注册原生面板与投影(`src/plugin/index.ts:308`;`src/plugin/dsh-go-native.ts:86-93`)。
7. **懒加载资产**:mermaid / three / echarts-core / echarts-full / maplibre / icons 六个独立 IIFE 资产,由 `tsdown` 单独构建(`tsdown.config.ts:286-292, 344-349`)。

**浏览器侧(client half)的注册点是 slots + 一个 DOM 观察器**:

- 硬注入 `['slots', 'sessions']`(`src/client/index.tsx:249`);缺任一服务则整个客户端树不启动,所以源码把 `inputTriggers` 改成可选注入,避免"声明了但宿主没提供"把渲染器一起挂死(`src/client/index.tsx:211-247`)。
- `tool.call.toolview` 按 `render_ui` 注册工具卡片(`:186-199`);`conversation.input.dock` 注册会话面板(`:200-210`);`inputTriggers` 可选注册 `/panel`(`:211-229`)。
- **围栏不是 slot**:它在 `installDomFenceRenderer` 里用 MutationObserver 找宿主 markdown 的代码块,自己 `createRoot` 挂一棵 React 树到代码块旁边,再把原块 `display:none`(`src/client/dom-fence.tsx:1304-1333`)。这就是"不改宿主"的代价:依赖 `.md-code-block`、`.code-block`、`data-code-block-content` 等 DOM 语义(`src/client/dom-fence.tsx:1-30, 80-100`)。

安装命令是普通 `dsh plugin`(`README.md:90`):

```sh
dsh plugin --profile web add @changfenhuang/dsh-genui
```

**包名陷阱**:registry 的仓库是 `omdsh-dev/dsh-genui`,实际 npm 包是 `@changfenhuang/dsh-genui`;README 明确警告 npm 上还有一个**无关的**非 scoped `dsh-genui`(Vue/OpenTiny 实现),装错会因 peer 依赖不兼容失败,并给了从旧 `@omdsh-dev` scope 迁移的命令(`README.md:109-119`)。这是本卡必须写清的第一使用成本。

## 关键实现

**文件结构**(行数为本次 clone 实测):

| 文件 | 行数 | 作用 | 关键位置 |
|---|---:|---|---|
| `src/plugin/index.ts` | 395 | node half 总装:提示词、skill、工具、资产路由、修正、原生桥 | `:307-395` |
| `src/plugin/tool.ts` | 470 | `render_ui` / `validate_dsh_ui` 定义与参数宽松策略 | `:47-79, 205-256, 369-459` |
| `src/plugin/fence-feedback.ts` | 730 | 回合尾围栏修正:提取、诊断、预算、steer | `:4-22, 49, 691-725` |
| `src/plugin/dsh-go-native.ts` | 238 | dsh-go 原生面板/视图与动作回传 | `:86-93, 180-231` |
| `src/shared/fence-repair.ts` | 749 | JSON 围栏修复(tier-1/tier-2、截断、括号补全) | 模块头 + `repairFenceJson/completeFenceJson` |
| `src/shared/fence-resolve.ts` | 88 | 浏览器与 node 侧共用的"围栏 → spec"流程 | `:53-85` |
| `src/client/genui-runtime/schema.ts` | 490 | 60 个组件的运行时字段/枚举/别名/嵌套规则 | `:306-313, 325-483` |
| `src/client/guard.ts` | 2763 | 限额、结构校验、确定性修复、部分修复、ECharts 清洗 | `:1-17, 1449-1517, 2037-2220` |
| `src/client/dom-fence.tsx` | 2166 | DOM 观察通道:发现、流式接管、挂载、动作 relay | `:1-30, 1304-1333` |
| `src/client/fence-render.tsx` | 264 | 围栏 → spec → React 节点;面板发布;失败诊断 | `:144-189, 191-240` |
| `src/client/GenuiBlock.tsx` | 339 | 组件树壳:本地状态、持久化、动作 debounce | `:46-96, 218, 248-255` |
| `src/client/panel-store.ts` | 579 | 会话面板的确定性折叠:sourceId 去重、顺序、预算 | `:1-39, 80-93, 287` |
| `src/client/spec.ts` | 1298 | spec 的 TypeScript 数据模型 | `:142-162` |
| `src/client/genui-runtime/limits.ts` | 77 | 全局资源上限 | `:4-40` |
| `SKILL.md` | 429(64 KB) | 模型侧组件字典与写法规范 | `:42-50` 组件词汇 |

**数据流(围栏,主路径)**:

1. 模型在 assistant 文本里输出 ```` ```dsh-ui ```` + JSON + 闭合围栏;宿主 markdown 先把它渲染成普通代码块。
2. DOM 通道按语言标签/结构找候选,流式期间用 partial parser,**只要有一个完整组件闭合就先渲染**;正文继续增长时重渲染(`src/client/dom-fence.tsx:20-30`;`src/client/parse-partial.ts`)。
3. `resolveFence` 先 tier-1 修复(引号/尾逗号),settled 后才允许 tier-2 补全缺失括号/引号;解析值走 `processGenuiSpec`(`src/shared/fence-resolve.ts:53-85`;`src/client/fence-render.tsx:186-189`)。
4. guard 归一化别名、修复字段、夹紧数值、按 200 节点 / 8 层 / 2 000 字符等上限截断,并把声明但未渲染的节点记成错误(`src/client/guard.ts:2037-2100`;`src/client/genui-runtime/limits.ts:4-40`)。
5. 校验失败时 `partialRepairGenuiSpec` 按错误路径丢坏节点再跑一次;仍失败则保留原代码块 + 诊断条(`src/client/guard.ts:2174-2220`;`src/client/fence-render.tsx:87-135`)。
6. 成功则 `block.after(container)` + `createRoot(container).render(...)`,再把原块隐藏;卸载/切分支时恢复原块(`src/client/dom-fence.tsx:1310-1333, 1579-1590`)。渲染层是插件自有的 React 18 根,不是 iframe,也不是 Web Component(`src/client/dom-fence.tsx:54, 643, 1310-1321`)。
7. 组件内的本地交互(排序、tab、折叠、判题)直接在前端完成;只有带 `action` 的控件才需要模型参与。

**事件回环(三种出口,别混)**:

| 出口 | 机制 | 证据 |
|---|---|---|
| 正文围栏 / 面板 | `conversation.send(t('action.inline' / 'action.panel', ...))`——把 `[genui-action] <name> <JSON payload>` 作为**新的用户消息**排进队列,模型下一轮看到 | `src/client/index.tsx:89-105, 140-150`;`src/client/i18n/en.ts:380-381` |
| `render_ui` 工具卡片 | 工具结果在 tool row 渲染;**同一 spec 同时发布到面板**,面板那棵树有 action provider | `src/client/toolview.tsx:47-62`;`src/client/panel.tsx:274-290` |
| dsh-go 原生 | `agent.followup()` 注入 `[genui-action] ...` 用户消息;要求 agent 处于 idle 且 inbox 为空 | `src/plugin/dsh-go-native.ts:215-216` |
| 同回合修正 | `agent.steer()` 把修正消息塞回**当前回合**,不是用户动作 | `src/plugin/fence-feedback.ts:691-725` |

**循环防护与幂等**:

- 修正循环有硬预算:每回合最多 2 条 correction,render failure 与 delivery reminder 共用;每个围栏 body 每回合最多修一次;子代理不触发;取消/缺 session 不触发;fingerprint 在 `steer` **之前**记账,防止重入边界重复投递(`src/plugin/fence-feedback.ts:4-22, 49, 310-328, 691-725`)。
- 面板操作按 `sourceId` 去重 + `replayBarrier`/`localBarrier` 挡住历史滚动重放;不同 source 都保留,后到的 replace 覆盖先到的(`src/client/panel-store.ts:1-17, 80-93, 281-300`)。
- 动作本身**没有幂等键**:连续点击会连续 `conversation.send`;只有 slider 拖拽按 action 名 + 字段 id 做 trailing debounce,离散控件立即发送(`src/client/GenuiBlock.tsx:46-72`)。dsh-go 侧有 idle/队列检查(`dsh-go-native.ts:215`),网页侧把排队交给宿主。
- 本地判定优先:quiz 的选项带 `correct` 时在原地判对错、显示解析,不发模型请求;只有带 `action` 才额外回传(`src/client/blocks/advanced.tsx:621-629, 640-690`)。这正是提示词里 "LOCAL-FIRST + actions" 的落点(`src/plugin/index.ts:156`)。

**测试**(能证明契约的部分):

- 161 个 `tests/**/*.spec.{ts,tsx}` / 28 655 行,jsdom 环境(`vitest.config.ts:17-25`)。覆盖 guard 限额与丢节点(`tests/genui-guard.spec.ts:101-340`)、ECharts XSS 过滤(`tests/genui-echart-guard.spec.ts:77-166`)、mermaid 输出拒绝(`tests/genui-mermaid-safe.spec.ts:13-24`)、工具卡片回退(`tests/genui-toolview.spec.tsx:38-77`)、提示词预算(`tests/plugin-genui.spec.ts:141-170`)、真实 AgentLoop 下的修正回环(`tests/fence-feedback-agentloop.spec.ts:1-30`)。
- **真机 e2e** `scripts/e2e.mjs`:真实 `dsh web` + 真实模型,装插件 → 模型输出围栏 → 点击 action → 只认"出现新的 assistant-step key 且新节点不再 streaming"作为模型响应,本地 chip 文案变化不算;超时 180 s 失败(`scripts/e2e.mjs:4-8, 743-767`)。
- **视觉 e2e** `scripts/e2e-visual.mts`:无需模型 key,注入 gallery 围栏后截图并跑交互断言,产出 `gallery.png` / `interactions.png`(`scripts/e2e-visual.mts:3-16, 313-327, 657-663`);另有 mermaid / map / 主题 / 交互状态 / 换行等独立 browser-check 脚本。**没有像素级 golden 基线**——截图是留档 + 断言,不是 diff 比对。

## 为什么它突出

**先拆星标归属。这个仓库就是插件本身,不是 monorepo 子目录,也没有宿主主项目可分账。** GitHub 星标是仓库级,因此 224 与 1014 都可以归给插件;需要解释的是增长节奏,不是归属:

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-08-09 | 仓库最早提交(`dsh-genui: interactive UI components inline in assistant replies`) | `git log --reverse` |
| 2026-08-13 | GitHub `created_at` | GitHub API |
| **2026-08-19** | **224 ⚠** | registry 边车 |
| 2026-11-18 | **1014 实时**;v0.16.0;822 commits;32 tags | 编排者/本卡 API + clone |

采样点时仓库只有 **6 天**;判断:224 星主要是首周传播的结果。此后约 3 个月涨到 1014,约 **4.5 倍**。224 不能当作深度采用证据——边车没有下载数,本轮也没有 npm 下载数据(见「待验证」)。

**扩散必须人工分类,因为 `genui` 会被 `genuine` 命中。** 原始 22 条里:

| 类型 | 计数 | 条目 | 判定依据 |
|---|---:|---|---|
| 依赖 / 伴生 | 3 | `SnakeDream/dsh-genui-scope`、`liqiming-whu/dsh-status-card`、`yushui6666/dsh-learning-mode` | 三者都需要 GenUI 的提示词/渲染:scope 明说按 `dsh-genui 0.3.3` 裁剪其系统提示词;status-card 与 learning-mode 的 README 都要求先装 `@changfenhuang/dsh-genui` |
| 同类独立实现 | 3 | `pengyue-polaron/deepseek-harness-genui`、`lhuans/dsh-genui`、`HwFee/HwFee-dsh#genui` | 各自有自己的渲染通道与 schema,不是本仓的 fork;`lhuans` 见下方更正 |
| 互操作 / 仅提及 | 4 | `zengxiaolou/dsh-github-link`、`Jason25417/dsh-composer-tweaks`、`kfirsch/dsh-hebrew-rtl`、`drscrewdriver/dsh-im-union` | 分别明说"不改 GenUI 本体只补链接行为"、加 GenUI 提示词开关、RTL 覆盖 GenUI 行、把 GenUI 围栏挡在纯文字 IM 外 |
| 假阳性 | 11 | `lzlrt/dsh-auto-wake`、`fightingFirefox/dsh-web-terminal` 等 | 命中的是 `genuine/genuinely`,与 GenUI 无关 |

**更正任务给的线索**:`lhuans/dsh-genui` 不是本仓衍生的代码 fork。GitHub API 返回 `fork: false`;其 README 明说组件来自 **OpenTiny GenUI SDK(Vue)**,围栏用 `schemaJson` 而不是 `dsh-ui`;本仓 README 也把它称为 "an unrelated, unscoped package named `dsh-genui` (a Vue/OpenTiny implementation by another maintainer)"(`README.md:113-114`)。它和本仓是**同名同题的两套实现**,计入"同类独立",不计"衍生"。同理,`SnakeDream` 是依赖提示词结构的伴生插件,不是 fork;把伴生/同名实现都算"真衍生"会虚增。

**开发强度是第二层证据**:822 个提交、32 个 tag、35 位贡献者、98 个 fork、7 个 open issue(均为 2026-11-18 API);但前两位贡献者合计 703 个提交,总线因子很集中。HEAD 就是一个社区 PR 的 merge(#451,提示词预算),最近批次还包含 mermaid 渲染文档(#457)、独立导出图片(#455)、mermaid 缩放(#452)——说明不是"发完就停"的样例仓。

**机制上的独特性(只用本仓证据)**:一套协议同时喂四种表面——正文围栏(DOM 接管)、工具卡片(slot)、会话面板(dock)、dsh-go 原生面板(bridge);60 个组件、27 种 diagram kind、14 个 ECharts preset(`src/client/genui-runtime/schema.ts:84-96`);流式 partial parser 在第一个组件闭合时就出 UI;再叠一个 64 KB 的按需 skill 和 `render_ui` / `validate_dsh_ui` 两个工具。它把"生成式 UI"做成了**协议 + 渲染器 + 教学层 + 资产层**的完整栈,而不是只加一个 React 组件。

## 代价与边界

### 安全边界:模型只能写 JSON,渲染器跑在宿主页面里

这是本卡最重要的一节。先给结论:**恶意 spec 不能执行 JS,也没有 iframe/sandbox 隔离;它跑在 DSH 页面同源环境里,能做的事由"白名单组件 + 清洗器 + 浏览器同源策略"共同限定。** 逐项证据:

| 恶意 spec 想做的事 | 能不能 | 源码证据 |
|---|---|---|
| 执行任意 JS / `eval` | **不能**。模型只能写 JSON;渲染器把 type 映射到插件自己的 React 组件,没有实际的 `eval` / `new Function` 调用;computed 用白名单函数求值 | `src/client/spec.ts:1-7`;`src/client/safe-math.ts:4`;`src/client/blocks/render-node.tsx:233-649` |
| 注入 HTML / 事件属性 | **不能**。行内富文本是自己写的 tokenizer,不做 HTML 解析;组件输出的是 React 节点,不走 `innerHTML` | `src/client/inline.ts:26-31`;`src/client/dom-fence.tsx:44-47` |
| 用 iframe 隔离 | **没有**。聊天内渲染器直接 `createRoot` 到宿主 DOM;唯一的 iframe 是 mermaid 的**同源测量文档**,没有 `sandbox` 属性,不是安全边界 | `src/client/dom-fence.tsx:1310-1333`;`src/client/asset-script.ts:20-28` |
| 用 SVG 注入脚本 | **不能**。`svg.code` 被解析成 XML 后转成 `data:image/svg+xml` 放进 `<img>`,不注入宿主 DOM | `src/client/blocks/svg.tsx:47-64` |
| 用 mermaid 注入脚本 | **受限**。mermaid 以 `securityLevel: 'strict'` 初始化,渲染后的 SVG 再被正则拒绝 `<script`、`on*=`、`javascript:` 才允许 `dangerouslySetInnerHTML` | `src/client/mermaid-core.ts:11-14, 47-49, 116`;`src/client/mermaid-safe.ts:15-24` |
| 用 ECharts option 做 XSS | **受限**。option 走深度/预算受限的清洗:字符串拒绝 `<script|img|iframe|...>`、`on*=`、`javascript:`、`url(`;tooltip 强制 `renderMode: 'richText'` | `src/client/guard.ts:1449-1517`;测试 `tests/genui-echart-guard.spec.ts:77-166` |
| 通过颜色/样式外传 | **受限**。颜色只接受 literal hex/rgb/hsl 或 `--dsw-*` token,`url()`/任意 CSS 被拒 | `src/client/genui-runtime/value-utils.ts:14-24` |
| 发起外网请求 | **能,但只能"打点"**。image/audio/video 的 `src` 接受 `http(s)` 或同源相对路径;浏览器会 GET 模型给的 URL,模型可把已知内容编码进 query 当信标。图片带 `referrerPolicy=no-referrer`,音视频没有 | `src/client/genui-runtime/value-utils.ts:35-44`;`src/client/blocks/image.tsx:87,120`;`src/client/blocks/basic.tsx:88,109` |
| 用地图加载任意外部瓦片 | **不能由 spec 指定**。地图样式是宿主配置,模型不能写 style/source URL;缺配置走无外源离线底图 | `src/client/map-config.ts:1`;`src/client/map-core.ts:42, 89`;`SKILL.md:428` |
| 用 3D 加载纹理/着色器/模型 | **不能**。只有 5 种 primitive、颜色与数值变换,没有 texture/shader/URL | `src/client/scene3d-core.ts:9-11, 30-70` |
| 读取宿主 storage/cookie 或调用工具 | **spec 本身不能**。动作只是 `[genui-action]` 用户消息,不是 tool call;但没有隔离,任何依赖库的同源 XSS 都等于宿主页面失守 | `src/client/index.tsx:140-150`;`src/plugin/dsh-go-native.ts:216` |
| 诱导用户填密码 | **部分能**。password 字段不进 submit 聚合、也不持久化,但源码明说“它自己的 action 仍会投递”;即 `inputType:password` + `action` 仍能把值发给模型。提示词禁令只是政策 | `src/client/blocks/forms.tsx:403-405, 467-477`;`src/client/GenuiBlock.tsx:218, 248-255`;`src/client/submission-registry.ts:135` |
| 耗尽资源 | **有上限**:200 节点 / 8 层 / 2 000 字符串 / 12 000 code / 8 000 mermaid / 60 图表点 / 50 表行 / 5 mesh 等 | `src/client/genui-runtime/limits.ts:4-40`;`src/client/guard.ts:2037-2100` |
| 导出独立 HTML | 单独文件带 CSP(`default-src 'none'`;`script-src 'unsafe-inline' blob:` 只给自带 runtime),不是聊天内渲染 | `src/client/artifact/html.ts:115-122` |

**判断**:它的安全模型是"**模型只能写声明式 JSON,渲染器是可信代码**",不是"把不可信 HTML 放进沙箱"。因此:

- 真正的代码执行面只有插件自己的 60 个组件与四个重引擎(mermaid / ECharts / MapLibre / three);这些库的 0-day 或一个渲染绕过,就是**宿主同源失守**——没有 iframe/CSP 兜底。mermaid 的正则复检是最后一道闸,不是解析器级 sanitizer(`src/client/mermaid-safe.ts:15-24`),这是最值得盯的残余风险。
- 模型可以做**钓鱼 UI**(假登录框、假"会话过期"提示)和**外链打点**(图片/音视频 URL);password 字段被排除出 submit 聚合与持久化,但**单独的 `action` 仍能带走它的值**,普通输入框的内容在提交时也会回到模型。提示词禁止索取密码/Key/Token(`src/plugin/index.ts:157`),那是政策,不是执行层强制。
- `link` 组件与行内 file 链接能把任意 http(s) 或本地路径变成可点击目标;本地文件路径打开后走宿主的文件服务,作用域是否被宿主限制在 workspace,**本轮未验证**(`src/client/file-link.ts:13-35`;`src/client/blocks/render-node.tsx:408-418`)。

### 失败模式(按发生顺序)

1. **宿主 DOM 改版** → 观察器找不到代码块,围栏静默退化回 JSON 代码块。它已经兼容 `.md-code-block` / `.code-block` / `.code-block-small` / `data-code-block-content` / 纯文本标签五类表面,但这仍是全仓最脆的耦合(`src/client/dom-fence.tsx:1-30, 80-100`)。
2. **JSON 坏了** → settled 后保留原代码块并显示诊断条;`fence-feedback` 会在回合尾请求一次修正,最多 2 条/回合,且消耗模型步数(`src/client/fence-render.tsx:87-135`;`src/plugin/fence-feedback.ts:4-22, 49`)。
3. **单个组件字段不合法** → 被 `partialRepairGenuiSpec` 丢掉,其余照常渲染;根不可修才整块回退(`src/client/guard.ts:2174-2220`)。
4. **资产路由不可用**(旧宿主/无 webServer 服务)→ mermaid 显示源码、scene3d 显示加载失败、echarts/map 走 fallback;主包仍能渲染静态组件(`src/client/asset-loader.ts:1-20`;`src/plugin/index.ts:43-48`)。
5. **`render_ui` 工具卡片里的 action 没有 relay**:toolview 注册时只套了 file-link context,没有装 `GenuiActionContext` provider;`GenuiBlock` 的 `onAction` 来自该 context,所以工具卡片上的按钮/表单动作不会回到模型。同一 spec 会被 toolview 发布到面板,面板侧有 provider,交互从面板走(`src/client/index.tsx:186-199`;`src/client/toolview.tsx:40-52`;`src/client/GenuiBlock.tsx:96`;`src/client/panel.tsx:274`)。判断:这是源码可证的边界,未在浏览器里点过。
6. **面板超限** → 折叠预算 200 节点/200 次 append,超出产生 overflow 诊断;模型应改发 replace(`src/client/panel-store.ts:34-39`;`src/plugin/index.ts:160`)。
7. **版本漂移** → 19 个 DSH peer 的范围覆盖三条 rc 线(`package.json:82-103, 213-217`);宿主 slots/事件名一变,客户端入口可能整棵不启动——源码已经用"可选注入"避免 `inputTriggers` 把渲染器拖死,但 `slots`/`sessions` 仍是硬注入(`src/client/index.tsx:232-249`)。
8. **装错包名** → npm 上无关的 `dsh-genui` 与本包同名;装错后 peer 依赖不兼容(`README.md:109-119`)。
9. **维护集中** → 822 个提交里前两人 703 个,核心是 33.8k 行源码 + 2.7k 行 guard + 2.1k 行 DOM 通道;这是高维护密度项目,不是"装完不管"的薄插件。

### 体积与提示词成本

- 主 `client.js` 在 v0.6.0 分包后是 **9.04 MB → 109 KB(gzip 28 KB)**(`CHANGELOG.md:601`);当前 0.16.0 未重新构建,数量级仅供参考。
- 重引擎全部按需: mermaid 3.4 MB、three 700 KB(v0.6.0 数据),echarts ~1 MB(`README.md:152`),icons ~1 MB 路径数据(`tsdown.config.ts:349`),maplibre 单独资产。**但首个围栏渲染后会 idle 预取 mermaid + three,两者合计约 1.25 MB gzip**——即使本轮没有图(`src/client/index.tsx:36-38, 56-83`)。
- 系统提示每轮只加 full 档 ≤1600 字符的围栏段;组件字典 64 KB 走 skill 按需加载,`validate_dsh_ui` 对 ≥3 节点/含 table 的 spec 是一次额外工具步(`src/plugin/index.ts:131-161`;`src/plugin/tool.ts:264-280`;`tests/plugin-genui.spec.ts:141-170`)。复杂 UI 的模型侧成本是"1 次 skill + 1 次验证 + 1 次正文",不是零成本。
- npm 包的 `files` 同时发布 `lib` 与 `src`(以及 `tsdown.config.ts`),安装体积会包含源码(`package.json:29-60`)。

## 可信度与复现

- **★★★(本仓)**:node half 全读;browser half 读了渲染主链、guard、spec/schema、面板、动作、资产、导出 CSP 与安全相关组件;测试读了关键 spec 与 e2e 脚本。**未跑** `pnpm install` / `pnpm test` / 浏览器 e2e / 构建,凡"运行时行为"均以源码与已有测试断言为据。
- **★(扩散分类)**:三条依赖/伴生与三条同类只读了 registry 描述 + 各自 README/package.json,未克隆源码;`lhuans` 的 fork 状态来自 GitHub API;`HwFee` 是 monorepo 子目录条目。
- **源码注释有陈旧处**:`src/client/spec.ts:8-9` 仍写着 “v1 interactivity is client-side only … events do NOT flow back”,与当前 v2 动作回传不符;判断以 `src/client/index.tsx:140-150` 与 `src/plugin/dsh-go-native.ts:216` 的实现为准。

```sh
# 1) 复现 clone 与提交
git clone --depth 1 --filter=blob:none https://github.com/omdsh-dev/dsh-genui.git .work/mine/cards/genui/repo
cd .work/mine/cards/genui/repo
git log -1 --format='%H %ad %s'        # 382a4a61… 2026-11-18
git rev-list --count HEAD              # 822
git tag | wc -l                        # 32

# 2) 规模与组件数
find src -name '*.ts' -o -name '*.tsx' | xargs wc -l | tail -1   # 33821
find tests -name '*.spec.ts' -o -name '*.spec.tsx' | wc -l       # 161
sed -n '/^const RAW_COMPONENT_SCHEMAS/,/^} as const/p' src/client/genui-runtime/schema.ts \
  | grep -cE "^  ('?[a-z0-9-]+'?): schema\("                   # 60

# 3) 扩散:22 条命中,11 条是 genuine/genuinely 子串
grep -ril 'genui' data/plugins/ | wc -l        # 22
grep -ril 'genuine' data/plugins/ | wc -l      # 11(全部为假阳性)
grep -rl 'GenUI' data/plugins/ | wc -l         # 7(区分大小写后仍会漏掉小写仓库名)
grep -rl 'dsh-ui' data/plugins/ | wc -l        # 51,但绝大多数是 dsh-ui-* 插件名前缀,不可当扩散口径

# 4) 外部事实(2026-11-18)
curl -s https://api.github.com/repos/omdsh-dev/dsh-genui        # created_at / stars / size
curl -s https://api.github.com/repos/lhuans/dsh-genui            # fork:false
```

**读过的文件**(逐项):`package.json`、`cordis.patch.yml`、`tsdown.config.ts`、`vitest.config.ts`、`src/plugin/{index,tool,fence-feedback,dsh-go-native}.ts`、`src/shared/{fence-repair,fence-resolve,fence-language}.ts`、`src/client/{spec,guard,dom-fence,fence-render,GenuiBlock,panel,panel-store,toolview,index,inline,submission-registry,asset-loader,asset-script}.ts(x)`、`src/client/genui-runtime/{schema,limits,normalize,diagnostics,value-utils}.ts`、`src/client/blocks/{render-node,svg,image,basic,forms,advanced,charts}.tsx`、`src/client/scene3d-core.ts`、`src/client/map-{config,core}.ts`、`src/client/artifact/html.ts`、`src/client/i18n/en.ts`(动作文案)、`SKILL.md`(分部)、`README.md`(安装/命名)、`docs/dsh-go.md`、`scripts/{e2e,e2e-visual}.mjs`、`tests/plugin-genui.spec.ts`、`tests/genui-guard.spec.ts`、`tests/genui-echart-guard.spec.ts`、`tests/genui-mermaid-safe.spec.ts`、`tests/genui-toolview.spec.tsx`、`tests/fence-feedback-agentloop.spec.ts`、`CHANGELOG.md`(分包段)。

**未读**:60 个组件的全部视觉细节(`charts.tsx` 51 KB、`advanced.tsx` 30 KB、`diagram/` 整目录)只读了契约与入口;`fence-repair.ts` 的完整修复算法、`panel-store` 的完整折叠算法、`artifact/` 导出运行时、dsh-go 原生面板的完整状态机均只读关键段;外部 10 个条目未克隆源码。**没有跑构建,所以 `lib/client.js` 的当前体积、实际首屏加载、以及 e2e 是否在本机通过都未实测。**

## 待验证

1. **工具卡片 action 是否真的不回传**:源码显示 toolview 没装 `GenuiActionContext` provider(`src/client/index.tsx:186-199`),但这是推断;需要在浏览器里对 `render_ui` 卡片点一次带 `action` 的 button,看是否出现 `[genui-action]` 用户消息。
2. **ECharts option 的远程资源面**:字符串过滤挡住了 `url(`/HTML/`javascript:`,但 `graphic` 的 `image` 之类若接受裸 `https:` URL 是否仍会被 ECharts 加载,未做运行时验证;这决定"外链打点"是否也能从图表走。
3. **mermaid 正则 sanitizer 的绕过面**:`assertSafeSvg` 是 `<script|on*=|javascript:` 的黑名单,不是 DOM 解析;需要拿已知 mermaid 输出向量做一次绕过测试,才能给残余风险定级。
4. **v0.16.0 的真实包体**:109 KB / 3.4 MB / 700 KB 都来自 v0.6.0 changelog;当前版本的 `lib/client.js`、六个资产、npm tarball 体积未构建测量。
5. **星标增长曲线**:224 是 2026-08-19 的单点,1014 是 2026-11-18 的实时;没有 stargazer 时间戳,无法判断增长是发布日冲高还是持续;下载边车缺失也让"采用"只有星标一个轴。
6. **本地文件链接的作用域**:`file-link.ts` 接受任意绝对/相对路径,点击后由 DSH 的文件服务处理;宿主是否限制在 workspace、是否会打开 workspace 外文件,未验证。
7. **dsh-go 原生面板**:只读了 `dsh-go-native.ts` 与 `docs/dsh-go.md`,没有 App/桥可跑;原生面板的 stale-click/重复投递保护只在文档、源码注释与 idle/inbox 入口检查里,未实测。
