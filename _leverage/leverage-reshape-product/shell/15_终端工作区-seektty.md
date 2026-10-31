---
title: "终端工作区 · SeekTTY"
domain: reshape-product
kind: sample
positioning: "把 Harness 的表层换成终端：自带 profile 与更新器，运行时状态仍归 Harness。"
takeaway: "`--update` self-first：每次最多装一个兼容组件，绝不跨未验证版本。"
read_when: "要做终端表层；或要设计 profile 自带更新器与包管理器布局适配。"
status: observed
updated: 2026-10-31
budget: 191
---
# 终端工作区 · SeekTTY:表层是自己的,状态是别人的

> **状态**:`observed`(README 级核过) · **基线**:DSH `0.2.0-rc.2`(其声明的**已测宿主**;声明下限也是 `0.2.0-rc.2`) · **读于**:2026-10-31
> **类**:`1` 壳与工作台 · **层**:2(表层)+ 6(首启)+ 7(分发/更新) · **★ 194 / forks 22 / open issues 8**(GitHub API,2026-10-31)/ **npm 月下载 1,296**(2026-09-30 ~ 10-29)
> **一句话**:它是本 lever 里**分寸感最好**的一张:换掉整个表层、自带 profile 与更新器,但明确宣布"**Harness remains the owner of runtime state**"——不抢运行时的所有权,只抢交互的所有权。
> **借鉴价值**:**① "表层归我、状态归你"是一条可以写进合同的边界;② 更新器 **self-first**:先检查自己,再检查宿主,一次只装一个兼容组件,绝不跨过未验证版本;③ pnpm 11 的 Global Virtual Store 会**在应用启动前**把 loader 弄挂,适配只作用于"自己发起的变更";④ 双渲染模式:全屏模式与**终端原生 scrollback** 模式,后者把历史交给终端,自己不重绘;⑤ 首启 API key **不回读、不付费校验、Escape 可推迟且不丢草稿**。**

> **证据深度**:README 级（未读源码）（2026-10-31）
> **样本档案**
> **repo**:[`Hilbert-beinghappy/seektty`](https://github.com/Hilbert-beinghappy/seektty) · **npm**:`seektty`(TUI 侧);全局 launcher 也叫 `seektty` · **许可证**:MIT
> **目录条目**:`data/plugins/Hilbert-beinghappy__seektty.yml`(`ui`)
> **装法**:`pnpm add -g @deepseek-ai/dsh@0.2.0-rc.2` → `dsh plugin --profile tui add --config.enable-global-virtual-store=false seektty@1.3.0` → `dsh --profile tui`;或全局装 + `deepseek` 直启
> **产物**:npm 包 + `deepseek` 全局 launcher;可选 companion bundles(Creator / Browser / Computer)
> **已在本地挖掘**:[`../_证据/01_桌面与终端-原始挖掘.md`](./_证据/01_桌面与终端-原始挖掘.md) §二.4
> **再深挖去哪**:`docs/release-v1.3.0.md`、`docs/pnpm11-layout-acceptance.md`、`docs/terminal-background-compatibility.md`
> **证据链**：固定 v1.3.0 的 peer 闸门、GVS、native tail opt-in 与 teardown 见[`07 源码复核`](./_证据/07_终端工作区-seektty-源码复核.md)。

---

## 它想干什么 · 为什么值得借鉴

**意图。** 把整个表层换成一个**终端工作区**,同时把所有权写进第一段:界面归它,Agent、会话、模型路由、权限、profile 与插件加载仍归 Harness("SeekTTY is the terminal surface; Harness remains the owner of runtime state.")。它要解决的麻烦是:想用终端,就得自己拼 profile、自己猜 pnpm 版本、自己盯着 dsh 升级,而现成的桌面壳又重到要装一个应用。它明确不做的,是替宿主做决定、动全局 pnpm 配置或复制宿主包。

**意义。** 它补的是"换表层但不换宿主"这条中间路线:能力全部从运行中的 Harness 发现(models / providers / presets / tools / skills / MCP),所以上游或第三方 bundle 加的功能会自动出现在终端里,不需要它发版。这让壳和宿主可以长期共存,而不是每次升级都打一次架。它还改了两条惯例:兼容性写成**三档 + 一个未知档**(低于下限拒、等于已测正常、高于已测提示但只自动装显式区间、未知契约 fail closed),更新器则 self-first 且"每次最多装一个兼容组件"。

**用户价值。** 装之前,终端用户面对的是 `dsh --profile`、被官方 Electron 应用独占的 `desktop` 名,以及 pnpm 11 的 Global Virtual Store 在**应用启动前**就把 loader 弄挂;装之后,`deepseek` 直接起一个工作区,`deepseek --update` 先查自己再查宿主,失败不挡启动。最觉得值的是 tmux/SSH 用户:按一次 **F3** 或 `/mouse native`,历史交给终端,滚动、搜索、选择全部恢复成终端原生的手感。代价由双方各担一点:用户得知道它只测到 `0.2.0-rc.2`、低于下限会被直接拒绝,作者则要长期维护"一次一个组件"的兼容矩阵,而且密钥**不回读、不预校验**,写错要到第一次真实请求才暴露。

**表达（界面与交互）。** 第一屏是像素鲸鱼欢迎页(可关),没有可用 Provider 时给三个出口——官方快速配置 / 共享 Provider 管理器 / 稍后配置;输入掩码、直接交给 `credentials.set`、不回读也不落 settings,Esc 推迟后仍能进 `/settings`、`/plugin`,**待发文本与附件保留**,配好自动继续。日常入口是 `/` 命令菜单,把 SeekTTY 命令、Host 命令与用户 Skill 合并成一个列表。切换原生模式时的纪律最像产品:顺序回填带进度,Esc **只停止回填、不停会话**,已写入 scrollback 的历史不重着色不重排,切回只用 Ctrl+L 刷新尾部;更新默认 `SEEKTTY_UPDATE=check`(跑完提示,`=0` 才关),Clarify 的草稿 **15 分钟**无交互即静默过期。

## 0. 一页速览(想抄的人只看这 20 行)

| 问题 | 它的答案 | 支撑 |
|---|---|---|
| 它是什么 | **终端表层**:`deepseek` 起一个工作区,Harness 拥有 Agent/Session/模型/权限/Profile/插件/持久化 | `[OBS]` §Overview |
| 能力从哪来 | 从**运行中的 Harness** 发现(models / providers / presets / tools / skills / MCP);上游或第三方 bundle 加的能力**自动出现**,不硬编码 | `[OBS]` 同上 |
| 装法 | `dsh plugin --profile tui add … seektty@1.3.0`;profile 是 **`tui`**,不是 `desktop` | `[OBS]` §Quick start |
| 更新器 | `deepseek --update`:**self-first**(先自己后 dsh)、**每次最多装一个兼容组件**、绝不装"未测的缺口"或未来宿主 | `[OBS]` |
| 更新失败 | **不阻塞启动**;`SEEKTTY_UPDATE=check` 改成"跑完提示",`=0` 关掉 | `[OBS]` |
| 宿主版本 | **低于下限直接拒**;高于已测版本可启动但**提示**;自动更新只装**显式兼容区间** | `[OBS]` §Compatibility |
| 未知契约 | 附件兼容适配器只处理**确切的老形状**,未知形状 **fail closed**,不重试 | `[OBS]` |
| pnpm 11 坑 | GVS 布局会让 Cordis loader **在应用启动前**就挂(`plugin tree failed to load`);适配器只对**自己发起的**变更加 `--config.enable-global-virtual-store=false` | `[OBS]` §pnpm 11 |
| 全局配置 | **不改** `pnpm config set`,不动 `NODE_PATH`,不复制宿主包,不在原生 reconciliation 之外改 profile 清单 | `[OBS]` |
| 渲染模式 | 全屏 alternate-screen;按 **F3** 或 `/mouse native` 切**终端原生模式**(退出 alt screen,把完整会话写入 scrollback,关鼠标上报,滚动/搜索/选择交给终端) | `[OBS]` §Interface |
| 全屏回填 | **顺序回填 + 进度**;Esc **只停止回填,不停会话**;已写入历史**不重着色、不重排** | `[OBS]` |
| 首启 API key | 无可用 Provider 时:官方快速配置 / 共享 Provider 管理器 / **稍后配置**;输入**掩码**,直接交 `credentials.set`,**不回读**;**不发付费校验请求** | `[OBS]` §First-run |
| 推迟首启 | Esc **不阻塞** `/settings`、`/plugin` 等本地面;**待发文本与附件保留**,配置成功后自动继续 | `[OBS]` |
| 撤销/过期 | Clarify 的问答与草稿默认 **15 分钟**无交互即过期;只有你显式提交的 Draft 进主会话 | `[OBS]` §Clarify |
| 迁移 | 老的全局 `deepseek-tui` 先卸再装;自定义 profile **首次启动独立迁移** | `[OBS]` §Migration |
| 最该抄的一句 | "**SeekTTY is the terminal surface; Harness remains the owner of runtime state.**" | `[OBS]` |

## 1. 它在产品里的位置

**七层坐标**:**2**(表层:整个终端界面)+ **6**(首启:首次 API key / 欢迎页)+ **7**(分发:profile bundle + 全局 launcher + 自带更新器)。第 5 层它**不抢**——默认模型、权限、预设仍由 Harness 的 settings 决定,它只提供编辑入口。

**它和上游的缝**:它用 **`tui`** 这个 profile 名(而不是 `desktop`——那被官方 Electron 应用独占,`lib/bin.js:35-37`)。安装走原生 reconciliation(`dsh plugin --profile tui add`),启动走 `dsh --profile tui` 或全局 `deepseek`。

**一句话**:它是"**换表层但不换宿主**"的最完整样本——比 `dsh-TUI` 更克制(不声称自己是应用),比桌面壳更轻(不要安装包)。

## 2. 机制(可照抄)

### 2.1 表层归我,状态归你

- 它**不**接管 Agent 运行时、会话存储、模型路由、权限模型、插件加载;
- 所有能力**从运行中的 Harness 发现**:`models`、`providers`、`agent presets`、`permissions`、`commands`、`tools`、`settings`、`skills`、`MCP`、`marketplace sources`;
- 因此上游或第三方 bundle 新增的能力**自动出现在终端**,不需要 SeekTTY 发版。

> **照抄点**:表层产品最大的诱惑是"顺手把状态也管了"。**明确写下"状态归宿主"这条边界**,是它能跟上游长期共存的原因。

### 2.2 自带更新器:self-first + 一次一个

```
deepseek --update
  ├─ 先检查 SeekTTY(自己)
  ├─ 再检查 dsh(宿主)
  ├─ 每次运行最多装一个兼容组件
  ├─ 绝不装:未测的版本缺口 / 未来宿主
  └─ 失败不阻塞启动
```

- `SEEKTTY_SPEC` 可把 profile reconciliation 钉到**确切 npm 版本**;
- `DSH_BIN`、本地安装、`SEEKTTY_SPEC` 覆盖**保持不动**;
- 默认 `SEEKTTY_UPDATE=check` 可改成跑完提示,`=0` 关闭。

> **照抄点**:壳自己的更新器要**先于宿主**检查,但**不能替宿主做大版本跳跃**。"一次一个组件"让失败可归因。

### 2.3 宿主版本:三档处理

| 宿主 | 行为 |
|---|---|
| **低于声明下限** | **拒绝**启动 |
| **等于已测版本** | 正常 |
| **高于已测版本** | 可启动,但**提示**;自动更新只装**显式兼容区间** |
| **未知契约** | 适配器 **fail closed**,不重试"可能已执行"的命令 |

> **照抄点**:兼容策略要写成**三档 + 一个未知档**,而不是"支持 0.2.x"。

### 2.4 pnpm 11 的 Global Virtual Store:在启动前就炸

- 症状:pnpm 11 把全局包放到 `store/v11/links`,Cordis loader 在**应用启动前**就报 `plugin tree failed to load` / `cordis:include`;
- 适配:只对**自己发起的**包树变更(launcher 供应、自更新、`/plugin` 安装/更新/删除/reconciliation)加 `--config.enable-global-virtual-store=false`;
- **不做**:不改全局 pnpm 配置、不设 `NODE_PATH`、不复制宿主包、不在原生 reconciliation 之外改 profile 清单;
- 诊断:如果在 `store/v11/links` 下看到失败的 launcher,给**双语诊断 + 逐条恢复命令**,而不是"缺依赖"。

> **照抄点**:**适配要局部、可逆、可解释。** 全局改包管理器配置是"修好一次、坑所有人"。

### 2.5 双渲染模式:把历史的所有权交出去

| 模式 | 谁拥有滚动/搜索/选择 | 关键约束 |
|---|---|---|
| 全屏(默认) | SeekTTY(alt screen) | 固定视口,composer/status 贴底 |
| **终端原生**(F3 / `/mouse native`) | **终端 / tmux** | 退出 alt screen;完整会话写入 scrollback;关鼠标上报 |

原生模式的纪律:

- **顺序回填 + 进度**;Esc **只停止回填,不停会话**;
- 已写入历史**不重着色、不重排**(终端拥有那段历史);
- 切回时用 Ctrl+L 只刷新**当前尾部**。

> **照抄点**:两套渲染模式不是"多一个开关",是**两套所有权**。切换时必须明确"谁负责重绘"。

### 2.6 首启:三步、可推迟、不偷看

- 无可用 Provider 时给三个出口:官方快速配置 / 共享 Provider 管理器 / **稍后配置**;
- 输入掩码,**直接传给 `credentials.set`**,SeekTTY **不回读**,也不写进 settings/日志/截图/会话;
- 保存**不发付费校验请求**(真正的鉴权发生在第一次真实请求);
- Esc 推迟,**不阻塞** `/settings`、`/plugin`;**待发文本与附件保留**,配置成功后自动继续;
- Provider 状态读不到时,指向 `/settings` 与 `/doctor`,**不显示一个用不了的表单**。

> **照抄点**:首启的错误处理不是"报错",是**保留用户已经输入的东西**并给出口。

### 2.7 过期与撤销:15 分钟

Clarify 的问答、选项、预览、refine 反馈留在 Host 内存,**默认 15 分钟无交互即过期**;主会话只收到**你显式提交的 Draft**;辅助用量记在官方 `storageDomain`,排除提示词/答案/凭据/路径。

> **照抄点**:临时交互必须有**过期**,而且过期要"静默变陈旧",不能"悄悄生效"。

## 3. 体验

- **第一次**:`deepseek` → 欢迎页(pixel whale,可关)→ 无 Provider 则三步配置(可 Esc)→ 直接开聊。
- **日常**:`/` 开命令菜单,合并 SeekTTY 命令 + Host 命令 + 用户 Skill;`/plugin`、`/settings`、`/theme` 都在终端里。
- **切模式**:F3 把历史交给终端,`/transcript` 浏览,`/transcript replay` 显式重写。
- **更新**:`deepseek --update` 先自己后宿主,失败不挡启动。

## 4. 证据与边界

- **影响力**:★ 194 / forks 22 / open issues 8(GitHub API 2026-10-31);npm 近 30 天 **1,296** 次下载（2026-09-30 ~ 10-29）。★ 与下载都**高于**同类的 `dsh-TUI Pro`（★ 1，旧快照下载 2,113）,说明"克制的终端表层"有真实用户。
- **机制证据**:README 全文(2026-10-31 抓取);摘录见 [`../_证据/01_桌面与终端-原始挖掘.md`](./_证据/01_桌面与终端-原始挖掘.md) §二.4。
- **口径警告**:npm 月下载含 CI 与镜像,≠ 用户数;与 ★ 不同源。
- **已核（2026-10-31）**：`dsh-TUI` 用的是 **`dsh-tui`** profile（其 README："`dsh plugin --profile dsh-tui add …`"、"`dsh --profile dsh-tui`"），与 SeekTTY 的 `tui` **不同名**，不存在 profile 撞车。真正的冲突面在 **patch 行 id**：两者都覆盖 `system-prompt`、`hmr`、`session-query-sqlite` 等宿主行（各自 `cordis.patch.yml` 开头即说明按 id 覆盖），所以**装进同一个 profile 才会打架**。
- `[OPEN]` 已测宿主是 `0.2.0-rc.2`,比本线基线 `0.2.1-rc.3` 落后一个 rc;`0.2.1-rc.3` 上未验证。

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 终端 UI 与宿主状态的边界 | 表层进程内渲染，状态/模型/权限仍归宿主；不要自建 Web 服务器。 | `[SRC-TARGET]` launcher spawn `dsh --profile tui`；无 createServer/listen；InProcessConnectionService。 | 少一层网络与生命周期；代价是进程内耦合与版本绑定。 | 定义进程内服务契约、启动参数与退出清理。 | 仍会通过 patch 改宿主行/预设。 | 自建端口 → 鉴权/清理/双开问题。 |
| 宿主版本兼容 | 用精确 tested pin + 兼容表 + 明确的 allow-version 逃生，而不是模糊 range。 | `[SRC-TARGET]` 63 精确 peers、minimum=tested=`0.2.0-rc.2`；无 `engines.dsh`。 | 测试矩阵可控；代价是新宿主直接被上游预检拒绝。 | 给每个宿主版本准备兼容证据与豁免流程。 | 在 0.2.1-rc.3 上需 `allow-version` 才能装。 | 宣传“高于已测可启动提示” → 实际安装期被拒。 |
| 自动更新 | self-first、最多一个组件、绝不装未测缺口；但默认模式与回滚要写清。 | `[SRC-TARGET]` updateMode 默认 auto；兼容区间退化为单 pin；无 previous 版本保存。 | 减少版本漂移；代价是启动前安装、失败无回滚。 | 默认改为 check 或显式 opt-in，加 previous pin 与回滚。 | 失败不阻塞启动，但成功装坏不会自动降级。 | 以为默认只提示 → 每次启动静默改环境。 |
| pnpm 11 GVS | 只在自身发起的 pnpm 变更加 `--config.enable-global-virtual-store=false`，不改全局配置。 | `[SRC-TARGET]` launcher/plugin/self-update 局部加参；不 pnpm config set/NODE_PATH。 | 避免全局副作用；代价是每次调用都要带参。 | 统一封装 pnpm 调用并测试 GVS 开/关。 | 上游 loader 在 GVS 下失败。 | 改全局配置 → 影响其他工具。 |
| 原生 scrollback | 切换/回填/关鼠标上报可做；增量“只刷尾部”应作为 opt-in 并有 terminal matrix。 | `[SRC-TARGET]` SEEKTTY_NATIVE_TAIL=1 门控 NativeHistory/NativeOutput。 | 兼容终端复制/滚动；代价是默认路径仍走主屏重绘。 | 定义终端矩阵与默认开关，测重绘边界。 | 默认未启用 tail 机制。 | 宣称默认“不重着色” → 与实现不符。 |
| Profile 管理 | 若在 TUI 内做 `/plugin`、`/profile`，要承认自己成为 profile 写入者，并用宿主 manifest helper。 | `[SRC-TARGET]` profile-plugin-manager 跑 pnpm、改 bundles、克隆/转换 profile。 | 一体化体验；代价是承担 profile 损坏/迁移责任。 | 加事务/备份/回滚与冲突检测。 | README “native reconciliation”仅是同一 helper。 | 认为从不改 profile → 出问题无法归因。 |
| Teardown/重启交接 | 同步恢复终端、fatal/suspend guard、限时清理、一次性 0600 交接文件并定期清扫。 | `[SRC-TARGET]` teardown/restart handoff。 | 崩溃后终端可用；代价是实现复杂。 | 定义信号处理、超时清理与交接文件生命周期。 | 未在真实终端验证全部路径。 | 崩溃后终端乱码/交接文件泄漏。 |
## 6. 失效条件与降级

- **宿主版本**:低于下限直接拒;高于已测只提示,自动更新停在显式区间。
- **pnpm 布局**:GVS 未修复前,所有"自己发起的"包树变更都要带局部开关;未知布局 fail closed。
- **终端能力**:`TERM=dumb`、`NO_COLOR`、tmux/screen 下主题与背景同步降级(不重着色,只给一次性提示)。
- **图片**:原生模式用**文本附件行**;只有终端支持时才内联渲染。
- **profile 冲突**(§4):与 `dsh-TUI` 共用 `tui` 名,共存未验证。

## 7. 开放问题

- [ ] `[OPEN]` `tui` profile 与 `dsh-TUI` 的共存边界(§4)。
- [ ] `[OPEN]` `0.2.1-rc.3` 上的实测(它自己只测到 `0.2.0-rc.2`)。
- [ ] `[OPEN]` 可选 companion bundles(Creator / Browser / Computer)是否会让"表层项目"变成"能力发行版"——那会把第 5 层也吃进来。
- [ ] `[OPEN]` 全局 `deepseek` launcher 与 `dsh --profile tui` 两条入口的**状态一致性**(launcher 会 provisioning 自己的包树)。
