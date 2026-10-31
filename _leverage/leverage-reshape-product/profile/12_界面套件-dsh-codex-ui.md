---
title: "界面套件 · dsh-codex-ui（月下载 11.9 万）"
domain: reshape-product
kind: sample
positioning: "dsh-codex-ui@2.0.9：六个 row 组成界面套件；源码有 theme/composer/sidebar 不同的激活与清理路径，部分 observer final dispose 未恢复全局样式。"
takeaway: "2.0.9 有六个独立 rows 与不同组件激活/清理路径；theme disable probe 有 token/root restore 分支，但最终 observer dispose 不做同样恢复，composer 还会先激活再异步探活。"
read_when: "要做整屏界面套件；或要避免主题/布局的「半降级」与僵尸设置卡。"
status: observed
updated: 2026-10-31
budget: 175
---
# 界面套件 · dsh-codex-ui：六个微内核，合成一个界面产品

> **研究范围**：`@michengai/dsh-codex-ui@2.0.9`，npm `gitHead` 与 fixed source commit [`29a999e`](https://github.com/MichengAI/dsh-codex-ui/commit/29a999ea8c41918e56a16542c669b258a5194e7a) / source manifest version 对齐。源码、测试与同 SHA CI 记录已读；未安装、构建或运行目标。详见[`10 源码复核`](./_证据/10_界面套件-dsh-codex-ui-源码复核.md)。
> **证据成熟度**：row composition、theme/composer/sidebar effect paths、settings null-render 与 Slot tests 为 `机制参考`；“禁用即全局彻底清理”不成立为普遍规则：theme observer final dispose 不执行探活失败分支的 root/style restore，composer async probe 前已 activate；无 `[RUN]`。
> **类**:`1` 壳与工作台 · **层**:2(表层)+ 3(槽位)+ 5(默认值) · npm 近 30 天 119,610 次下载（2026-09-30~10-29） · ★ 250 / forks 20 / issues 2（2026-10-31）
> **一句话**：0.2.9 用六个 bundle rows 组合设置皮肤、theme、composer、sidebar、session-title 与 dependencies；源码同时显示不同模块的探活、激活及清理路径并不完全相同。
> **借鉴价值**：**① 逐 row 设计激活/清理状态机，不能把统一“微内核可卸载”口号套给不同模块；② fail-closed probe 与最终 dispose 是不同路径，需分别恢复 DOM/token/root state；③ 设置卡片只在局部 branch 有 `return null`，不能扩大为所有禁用子插件全局 0 DOM；④ sidebar 使用宿主 DOM selector/CSS，settings skin 混用 slots 和 DOM，不是全量 primitive/slot；⑤ peer range 的声明不等于覆盖范围每版行为测试。**

> **样本档案**
> **repo**:[`MichengAI/dsh-codex-ui`](https://github.com/MichengAI/dsh-codex-ui) · **npm**:`@michengai/dsh-codex-ui@2.0.9` · **许可证**:Apache-2.0
> **目录条目**:`data/plugins/MichengAI__dsh-codex-ui.yml`(`ui`)
> **文档装法**:`dsh plugin --profile web add @michengai/dsh-codex-ui@latest --registry=https://registry.npmjs.org/` → 重启并硬刷新；本次未实测
> **版本要求**：Node `^22.19.0 || >=24.0.0`、pnpm `^11.0.0`；DSH/client peers `>=0.2.0-rc.1 <0.3.0-0`；声明范围不是每版本 runtime 证明。
> **证据链**：早期资料见[`01 产品聚合`](./_证据/01_产品聚合-原始挖掘.md) §三；固定源码、测试范围和同 SHA CI 引用见[`10 源码复核`](./_证据/10_界面套件-dsh-codex-ui-源码复核.md)。

---

## 它想干什么 · 为什么值得借鉴

**意图 [DOC]**：固定 README 将它定位为 Codex 风格的界面套件，列 settings skin/theme/sidebar/composer/session title 等模块及其可配置体验；这段描述不能证明各模块互相独立或完整可卸载。

**意义 [SRC-TARGET/OBS]**：2.0.9 bundle patch 插入六个 rows；不同插件 observer 各自定义探活、挂载和清理路径。theme 的探活失败分支能恢复 tracked tokens/root presentation，但最终 dispose 不执行同一恢复；composer 在异步探活完成前就 activate。故可迁移的工程点不是抽象“微内核”，而是逐模块检查 activate-before-probe、failure-after-probe、disable/final-dispose 三条路径。

**用户价值 [DOC/OBS]**：产品文档承诺禁用失效子插件后隐藏相关设置并回到宿主外观。源码只支持限定范围：theme settings card 在特定 disabled 状态 `return null`；不能据此声称所有模块、所有失活路径均 0 DOM/零残留。代价是 slot 与宿主 DOM selector/CSS 同时存在，仍需对宿主升级做回归。

**表达 [DOC]**：配色、布局、玻璃层级和 56px sidebar 体验是 README claims；代码显示 sidebar 混用宿主 DOM selectors，settings skin 同时使用 slots/DOM/CSS。本次未运行浏览器确认视觉效果或无闪烁。

## 0. 一页速览(想抄的人只看这 20 行)

| 主张/机制 | 固定版本证据 | 边界 |
|---|---|---|
| Bundle composition | 2.0.9 patch inserts six rows: session-title/settings-skin/composer/sidebar/theme/main | Package rows do not prove every microkernel is independently disableable or can work without others |
| Activation/cleanup | Theme probe failure branch restores tracked body tokens/surface/root presentation; composer activates before async probe; sidebar uses selectors + style overrides | Theme final observer dispose does not itself run root/token restore; no universal “disable = never installed” guarantee |
| Settings 0 DOM | Theme settings card `return null` in a particular disabled branch | Does not prove all settings/subplugins are 0 DOM for every unreachable/dispose case |
| Public extension contract | Composer/main register selected slots/settings section; sidebar/settings skin also use DOM/CSS techniques | Not a pure primitives/slots implementation; host DOM/theme contract remains a coupling |
| Version boundary | npm `2.0.9` gitHead matches commit; peers `>=0.2.0-rc.1 <0.3.0-0`, dev pin rc.3 | Declared range and Node 22/24 CI not proof for every peer baseline |
| Testing/CI | Slot/settings tests and same SHA Node 22/24 checks success | No local run; some tests mock cleanup instead of exercising full host observer/React integration |

## 1. 它在产品里的位置

**七层坐标**:**2**(表层:整屏设置、侧栏、主题)+ **3**(槽位:会话行菜单、伴侣插件面板)+ **5**(默认值:7 套主题与材质)。它不碰 6/7 层——不提供首启向导,也不自带分发;更新走 npm。

**和 `dsh-web` 的区别**:`dsh-web` 是「**功能全家桶 + 自家商店**」,它是「**界面重做 + 伴侣插件管理**」。一个横向铺能力,一个纵向改体验。两者都是 `profile` 级产品,但一个靠**广度**,一个靠**深度**。

**它证明的事**:profile 产品不一定非要 20 个包;**一个包、六个微内核、一套设计语言**,也能在浏览器里长成一个"看起来不是原生 DSH"的产品。

## 2. 机制(可照抄)

### 2.1 微内核:六个子插件,各自可禁用

## 2. 组件激活、清理与宿主耦合

### 2.1 六个 rows 不等于六个独立故障域

`[SRC-TARGET]` 2.0.9 bundle patch 插入六行：session-title、settings-skin、composer、sidebar、theme、main。主入口通过 Cordis effects 安装 observers，并注册 settings section；theme 的 Host probe 由 endpoint 反映 profile 子插件启用状态。Row/module 拆分是结构事实，但 module 间依赖与降级不完全独立。

> 洞察：模块化 UI 要逐个定义 mount dependencies、probe 时点、禁用传播和 cleanup owner；不能仅凭 package/row 个数声称用户可任意单独关闭且互不影响。

### 2.2 Theme failure branch 与 final dispose 是不同路径

`theme/index.ts` 中探活非 2xx、throw 或 disabled 的分支会移除 tracked body tokens/surface style、dispose glass，并在曾套用主题时恢复根 `data-ds-theme-source`、`colorScheme`、dark marker；另有 stock theme 恢复路径。**但 observer 最终 dispose 本身不做同一组 token/surface/root restore**，所以不能概括“任何卸载路径都彻底清到像没装过”。首次激活会先有同步效果，再异步 probe 回退，也非零闪烁 fail-closed。

`composer/index.tsx` 在 async probe 前先 activate，失败后再 return false/cleaners；sidebar 则探活成功才 mount React root、选 DOM selector 注入容器/隐藏原控件，dispose 时卸 root/style。三者的 fail timing/cleanup 不同。

> 洞察：对可见全局副作用，测试必须覆盖失败前后、手动 disable/unmount、root token 重复写、DOM observer 变化和 dispose；“probe fail cleans up”不能替代“所有 teardown 清理”。

### 2.3 官方 Slot/primitive 与 DOM hybrid

源码注册 `conversation.input.dock` 和 `settings.section` 等 Host slots，并使用宿主 Switch/SegmentedControl；sidebar 同时依赖宿主 button/class selectors 和 CSS，settings skin 混合 DOM decoration 与 CSS。不是全包“只吃官方 primitive + slot”，也不能保证内部无私有 DOM assumptions。

> 可迁移洞察：公开 Slot 可降低 fork 面积；对需要定位宿主 DOM 的局部增强，需额外版本检测/失配降级与 host-version contract，不要把“用了一部分 Slot”写成 zero-intrusion。

### 2.4 Settings card 的可见性范围

`ThemeSettingsCard.tsx` 在特定 `subPluginEnabled === false` 分支 `return null`；这证明该 card branch 是 0 DOM，不证明所有子插件不可用时整个设置根没有 DOM。已有设置测试包含 404/network failure 和 style/navigation assertions；部分测试手工安装/卸载，不是完整真实 host observer teardown。

### 2.5 Tests and compatibility limits

Same commit tests include real SlotCore contract and settings registration tests；composer portal cleanup test mock observer/cleanup helper，并未触发完整 observer/React integration。CI Node 22/24 jobs pass；独立 `test:compat` / `test:host` / `test:fallback-host` scripts 不能仅凭这些 job 宣称都通过。Peer range `>=0.2.0-rc.1 <0.3.0-0` 含多个 prereleases；dev pin rc.3 不是所有 peer version 实测。

## 3. 产品体验（README 描述，未运行验证）

- `[DOC]` README 要求安装后重启并硬刷新；描述主题/布局、输入历史、会话标题与依赖管理 UI。
- `[SRC-TARGET]` 源码确有六条 rows、UI slots、主题 token、composer history 和 sidebar injection，但这些机制并未在本轮浏览器中呈现。
- `[OPEN]` 子插件切换后的全部 effective UI、theme final dispose、异步探活期间首帧及与 ds-bot 同装冲突都未做 runtime 验证。

## 4. 证据与边界

- **采用信号**：npm 2.0.9 last-month 119,610（含 CI/镜像）；GitHub ★ 250 / forks 20 / issues 2（2026-10-31）。不可互证或解读为用户数。
- **固定源码**：npm `2.0.9` gitHead 与 source commit `29a999ea…` manifest 对齐；peer `>=0.2.0-rc.1 <0.3.0-0`；dev pin rc.3。细节见[`10 源码复核`](./_证据/10_界面套件-dsh-codex-ui-源码复核.md)。
- **[TEST]/[CI]** 读取了 pinned tests；same SHA Node 22/24 CI checks success。测试有真实 SlotCore contract，但 portal integration 部分用模拟；本次未本地执行。
- **[RUN]** 无安装/启动；没有验证浏览器实际体验、全 peer range、final dispose 的 root/theme cleanup 或 ds-bot conflict behavior。
- 旧 2026-08-19 快照对 npm 只记 1,141，已被 last-month 119,610 取代；使用时标明窗口。

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 一个界面套件拆成多个组件 | 当各 feature 的 state/dependency 可独立管理时用 rows/components 拆模块，但先定义跨模块 prerequisites 和 activation order。 | `[SRC-TARGET]` 2.0.9 六 rows；源码发现 composer 可先 activate 再 async probe，theme/sidebar 路径不同。 | 单项组合较灵活；代价是多条状态机、observer 和清理合同。 | 给每模块列 prerequisites、probe state、activate/disable/final-dispose actions 和故障矩阵。 | 行数不证明 module 可单独使用或 disable 不影响其他模块。 | 任意 disable 可能留下 toolbar/portal/theme state 或依赖不可用。 |
| 注入主题 token / root attrs / surface styles | 登记每次全局副作用，并在 probe-failure、user-disable、unmount、final dispose 各路径显式恢复 prior state。 | `[SRC-TARGET]` theme probe disabled branch 清 tracked values；final dispose 不做同等 root/token restore；`[TEST]` 部分手工 cleanup assertions。 | 可减少“关掉后留半套主题”；代价是要保存正确 prior state，处理多个主题插件相互覆盖。 | snapshot prior root state、owner token namespace、幂等 restore、dispose/order tests；针对外部 DOM mutation 再验。 | 此样本的清理并非所有 teardown 路径一致；没有 `[RUN]`。 | observer dispose 或异常卸载后残留全局颜色/样式污染其他插件。 |
| Slot 与宿主 DOM selector 并用 | 优先使用公开 slot/primitives；若不得不定位 host DOM，就记录 contract/version、mutation fallback 与无匹配时停用行为。 | `[SRC-TARGET]` composer/main 用 slots，但 sidebar 用 selectors/style hide native items，settings skin 混合 DOM/CSS。 | 在可用 seam 上降低 fork 面积；代价是 selectors 随宿主变动脆弱。 | 把 DOM hook 当显式兼容点，做 pinned host tests 与 runtime guard，不宣称 zero-intrusion。 | peer 范围 `>=0.2.0-rc.1 <0.3.0-0` 不是全版本已验。 | 宿主更新改 class/structure 后 sidebar 注入可能失效或隐藏错误控件。 |
| 子插件设置项应随功能消失 | 对每个设置 view 验证不可用时的 render policy；仅在具体 branch 测到 `return null` 时才称该卡 0 DOM。 | `[SRC-TARGET]` ThemeSettingsCard disabled branch `return null`；不能推广全设置/全部 modules。 | 降低不可用设置误导；代价是状态/设置根生命周期需一致。 | 分组件设置 card 断言 disabled, unreachable, unmounted 三状态及 portal/container presence。 | 局部 theme card 事实不证明整套 settings 0 DOM。 | 僵尸设置仍可点击，或隐藏整个设置而丢失其他功能配置。 |
| CI 看似通过但用户关注宿主集成 | 把 unit、real slot contract、browser/host mount、fallback-host、release checks 分开报告。 | `[TEST]` slot tests 真用 SlotCore；composer portal test mocks observer；`[CI]` Node 22/24 success；独立 scripts 不能据普通 job 推断都跑过。 | 质量声明可指向实际覆盖面；代价是维护 host matrix。 | 给每种测试标 fixture/fake/real host、版本和触达路径；失败恢复路径要有 adversarial tests。 | 本次未执行，peer range 未全跑，CI只属于固定 SHA。 | 将 mock test 或 Node matrix 误称为实际浏览器卸载/跨版本兼容验证。 |

## 6. 已知失效边界与下一步验证

| 风险 | 已知实现/限制 | 待验证 |
|---|---|---|
| Theme lifecycle final dispose | probe-failure branch恢复 tracked state；observer final dispose 不做同样的 root/token restore | 真实 disable/unmount/reload 后残留状态与多主题并存 |
| Async activation | composer 在 host probe 前已 activate | probe 慢/失败期间用户可见能力、后续关闭是否 clean |
| DOM coupling | sidebar selectors/CSS hide host controls；settings skin DOM/CSS + slots | DSH minor DOM changes、selector missing、host-side mutation |
| Settings visibility | theme settings component 的一个 disabled branch 返回 null | unreachable/unmount/各子组件是否仍留下其他设置节点 |
| Compatibility | peer `>=0.2.0-rc.1 <0.3.0-0`；dev pin rc.3 | 除固定 CI 的 Node 22/24 job 外，逐个 DSH peer baseline 的 Slot/theme behavior |
| Companion conflict | README warns against ds-bot; no runtime conflict auto-detection established here | same profile overlap of sidebar/session slots and diagnostics |

## 7. 下一步复核

- [ ] 在 disposable DSH profiles 对每个 module 分别 enabled→disabled→unmount→reload，观察 body tokens/root attributes/styles/portal/设置卡 DOM，并模拟 external mutation。
- [ ] 模拟 theme probe timeout、composer probe rejection、Slot unavailable，核对 activation visibility 和 cleanup 顺序。
- [ ] 对 sidebar selectors 做宿主版本矩阵；验证 `ds-bot` 同装时是否能检测而非静默竞争。
- [ ] 若要声称整个 peer range 兼容，按 DSH rc.1 至 rc.3 + 0.2.2 prereleases 分别验证；npm declaration/rc.3 dev pin 不能外推。
