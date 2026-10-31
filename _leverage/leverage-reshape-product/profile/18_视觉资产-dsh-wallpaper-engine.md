---
title: "视觉资产 · dsh-wallpaper-engine"
domain: reshape-product
kind: sample
positioning: "dsh-plugin-wallpaper-engine@1.4.0：八个包/rows 提供 wallpaper runtime 与可选资产插件；此版没有 glass 子包，better-sidebar 也不是硬依赖。"
takeaway: "1.4.0 把 wallpaper host/client 与七个子包发布成八行；预设是完整 values snapshot + 可选资产段，schema version mismatch 作废而不迁移；本版无 glass row。"
read_when: "要做皮肤/外观类产品；或要判断「视觉身份」该不该算 profile 级产品。"
status: observed
updated: 2026-10-31
budget: 210
---
# 视觉资产 · dsh-wallpaper-engine:外观本身就是产品

> **研究范围**：`dsh-plugin-wallpaper-engine@1.4.0`；tag `v1.4.0` 指向 commit [`3b0103b`](https://github.com/elysia395/dsh-wallpaper-engine/commit/3b0103bc1d5431840208966ce67155f392c4095c)。npm tarball/tag/manifest 版本相符；release 自述附件一致，但本轮未独立比对 tarball bytes。源码、测试和 same-SHA CI 已读，未安装/构建/运行。见[`11 源码复核`](./_证据/11_视觉资产-dsh-wallpaper-engine-源码复核.md)。
> **证据成熟度**：package rows、host/client service、video/preset/upload 实现为固定版本 `机制参考`；WebGL/ffmpeg/GPU 的真实表现和视觉回退为 `[OPEN]`。v1.4.0 无 glass 子包/row；`dsh-better-sidebar` 是 optional companion，不是 `>=0.19.0` 硬依赖。
> **类**:`1` 壳与工作台 · **层**:**5**（默认值：观感）+ 3（设置/壁纸库槽位）+ 7（预设分发） · DSH engine 声明 `^0.2.0-rc.1` · ★ 4,189 / npm 月下载 109,268（2026-10-31）
> **一句话**：1.4.0 由主 wallpaper host/client row 与 7 个子包组成；支持 Scene/Web/Video/custom assets、预设和运行时资源控制。目标代码有 no-tool/no-prompt contract；具体 WebGL/设备效果仍未本次实测。
> **借鉴价值**：**① 用进程能力界定 wallpaper format，并拒绝不可执行 Application 类型；② 把预设做成完整 `values` snapshot + optional asset states，明确缺席/null/对象等语义与版本作废策略；③ GPU/解码器/ffmpeg 用排队、取消、cache 和资源限额治理；④ 多包发布标明 order/version 与 dependencies；⑤ 大型视觉效果需分离资产数据与 playback/render state。**

## 它想干什么 · 为什么值得借鉴

**意图 [DOC]**：v1.4.0 README 将产品描述为本机 Wallpaper Engine 资产（Scene/Web/Video）与字体、吉祥物、预设；明确声明不注册模型工具、不注入 prompt。

**意义 [SRC-TARGET/OBS]**：固定 release 的 host/client 两端、7 个子包和主 row 结构清晰；可分享预设不是只存 asset refs，还包含完整 whitelisted values snapshot 与可选字体/mascot/avatar。其结构适合研究“观感是可版本化产品资产”，但不能从该版推导“玻璃是可独立子包”：v1.4.0 patch/package list 中不存在 glass row/package。

**用户价值 [DOC/OPEN]**：README 目标是让本机 Wallpaper Engine 素材和 web-renderable/custom assets 进入 DSH。源代码说明 Application 类不进入库/轮播、Scene 有 fallback；实际硬件上是否可播放、用户数据如何备份迁移仍需 runtime 验证。`dsh-better-sidebar` 是 optional companion，不是包级硬依赖。

**表达 [DOC]**：壁纸库双入口、暂停/清除语义、缩略图即时效果来自 README 描述；本次没 boot UI。预设导出可能携带有限资产，不包含整个 Wallpaper Engine media library；应用预设是否改变最终 UI 还受 schema/资产与更高配置层影响。

## 0. 一页速览(想抄的人只看这 20 行)

| 产物/主张 | 固定版本依据 | 证据边界 |
|---|---|---|
| Package family | npm `1.4.0` + GitHub v1.4.0 tag→commit `3b0103bc…`；主包 + 7 子包，共 8 packages/rows | Release 自述 tarball 与附件一致；本次未独立比较 bytes |
| Wallpaper formats | Scene/Web live paths、Video、custom assets；Application 不进产品库/轮播 | `[DOC][SRC-TARGET]`；具体硬件/浏览器表现没跑 |
| Scene/Web isolation | Web iframe sandbox allow-scripts + shim; Scene WebGL fallback tiers | 源码/文档有链路；不是“任何场景都不黑屏”保证 |
| Glass | 1.4.0 无 `wallpaper-engine-glass` row/package | 卡片旧 claim 不适用于该 release |
| Presets | Full allowlisted values snapshot + optional font/mascot/avatar asset semantics; schema mismatch obsolete/no migration | `[SRC-TARGET]` preset route/schema；没有实际做跨版本 import |
| Model side | Host entry comment + static token-contract guard: no tools/prompt injection | 不代表未来版本永久不变；未运行模型观察 |
| Sidebar dep/install | Better-sidebar is optional companion; README requests full DSH exit before install; engines Node >=22.12, DSH `^0.2.0-rc.1` | No hard `>=0.19.0` dependency; order/compat not runtime-tested |
| Tests/CI | Static guards/tests enumerated; fixed release SHA Ubuntu/Windows checks success | No local execution; hardware WebGL/ffmpeg/UI not CI-equivalent |

## 1. 它在产品里的位置

| 七层 | 动作 | 说明 |
|---|---|---|
| **5 默认值** | 背景、玻璃、字体、吉祥物、特效 | 用户第一眼看到的就是它 |
| 3 槽位 | 设置里的 `Wallpaper Engine` 页 + 壁纸库 + 吉祥物拉绳入口 | 两个入口，互相可达 |
| 7 分发 | **外观预设导入导出** | 一套观感可以整套传给别人 |

### 1.1 它是 profile 侧的第 8 种形态:**产品资产（视觉身份）**

前七种回答“装什么”（聚合、界面、组合、补丁、接管、进口、闭环），这一种回答“**它看起来是谁**”：

| 形态 | 交付物 | 代表 |
|---|---|---|
| 家族桶 / 组合包 / 聚合补丁 | 多个插件 | `dsh-web` / `dsh-suite` / `dsh-plugin-kit` |
| 界面套件 | 整套交互界面 | `codex-ui` |
| 接管 / 进口 / 闭环 | 内置行 / 外部套件 / 一条闭环 | `15` / `16` / `17` |
| **产品资产（视觉身份）** | **一整套观感 + 可分享预设** | **本卡** |

> **为什么它算 profile 而不是插件**：本 lever 的主问里就写着“**皮肤**”；它定义的正是“不配置时你看到什么”，而且带自己的分发单位（预设）。`12_界面套件` 已经开了“单包也能进”的先例——单包与否不是判据，**是否重定义整套体验**才是。

### 1.2 它和 `12_界面套件` 的分工

| | `12_界面套件` | 本卡 |
|---|---|---|
| 改什么 | **交互**：布局、侧栏、设置形态、会话标题 | **观感**：背景、玻璃、字体、吉祥物、特效 |
| 代价 | 学一套新布局 | 吃 GPU / 跨产品依赖 |
| 社区量级 | ★250 / 月 119,610 | **★4,189 / 月 109,268** |
| 共同点 | 都不碰模型侧 | 都不碰模型侧 |

> 两张卡拼起来是“界面产品”的两半：**一半管怎么用，一半管看起来像谁**。星标的差距（250 vs 4,189）说明用户先为“好看”买单。

---

## 2. 机制（可照抄的部分）

### 2.1 Format admission 与 Scene fallback

`[SRC-TARGET]` v1.4.0 将 wallpaper 划分 Scene/Web/Video/custom/Application。Scene 路径经外部 `webwallgl` 实时渲染，失败顺序为 live iframe → scene embedded MP4 → live capture cache → user custom image → empty state；首帧占位另有 poster/cache 顺序。Application 需要启动第三方程序，明确不渲染、不进入产品 library/rotation。Web iframe 使用 `sandbox="allow-scripts"` 并注入 WE API shim，通过 postMessage bridge；bridge 失败可退 compatibility bare HTML，不保证 API equivalence。

> **洞察**：按 host process 实际可执行能力决定资产是否入库；为“可渲染但降级”与“不可运行、直接拒绝”设不同状态与 UI 文案。不要把 fallback chain 写成无黑屏保证。

### 2.2 Video resource limits 与 cancellation

Video 转码限帧率而不改时间线；优先 NVENC、再软件 `libx264`；cache key 含 source path/mtime/FPS，client 可先用 cache，失败回原视频。并发上限 2，单 task 15min default；等待队列不计任务 deadline。断连且无等待者时 abort 子进程并清临时文件，unload 会终止活跃 ffmpeg；binary download 有 SHA256、size/magic checks。没有通用 GPU/CPU/memory cap 或硬件性能保证。

> **洞察**：重媒体处理应同时约束并发、期限、缓存、取消和下载完整性；单一 FPS cap 并不等于总体资源安全。

### 2.3 Preset snapshot 与 asset ownership

预设 schema 为 `{$schema, id, name, values, assets?}`：`values` 是 allowlisted profile settings 的完整 snapshot，读写经 schema sanitize、缺键补默认；`assets` 可选择携带 fonts/mascot/avatar。字段状态区分缺席（保持当前）、`null`（清除/默认）、内置 string id 与上传对象。GET 返回 metadata，不携带图片 bytes；导出是 JSON attachment，导入仅保存、不自动应用。应用时写 settings 并安装 asset files；壁纸媒体文件整体并不随 preset 打包。未知 schema tag 返回 `version-obsolete`，不自动 migrate。

> **洞察**：可分享预设需要定义 snapshot vs delta、unset/null、asset ownership 和兼容迁移；显式 obsolete 比默默把旧 preset 错套到新 schema 更安全，但会让用户必须重存。

### 2.4 Package family 与 teardown

v1.4.0 主包 + 7 子包共八 packages；主包精确引用同版子包，按子包先发、主包最后的 `publishOrder`。主服务在 Host 提供 routes/file/config，client 注入 Web runtime；子包依赖 host `wallpaperEngineHost` service，主 package teardown 触发依赖 fiber park。better-sidebar 标为 optional companion，不是硬版本依赖。该发布版无 glass row。

> **洞察**：多包视觉系统要把 release order、version parity、optional peer/companion 和 host service teardown 放进 manifest/CI；不要依旧版/后续版 README 推当前包结构。

### 2.5 模型侧零注册（固定版本约束）

主入口注释和静态 token contract test 指明不注册 model tool、不注入 prompt text；client inject 是浏览器代码装载而非模型能力注册。该 release 的源码结构可支持“当前版本零模型侧注册”结论，不能永久承诺未来版本零 token。

> **洞察**：外观产品应把 model-side budget 当显式设计约束，并在新增工具/提示的 CI 中作结构守卫。

---

## 3. 产品体验（README 主张，未实测）

- `[DOC]` README 要求安装前退出 DSH，列壁纸库/吉祥物入口、选择/暂停/清除、预设导入导出与平台说明；本次未启动 UI。
- `[SRC-TARGET]` package/patch 给出八行主子包结构及 host/client split；source guards/CI 不证明用户机器上的实际 WebGL、ffmpeg、audio/video device 或 filesystem permissions。
- `[OPEN]` 不同 DSH profile/OS 下的 first boot、错误提示、有效配置和玻璃/样式 teardown 均需 runtime verification；尤其此 release 不存在 card 所述 glass subpackage。

## 4. 证据与边界

| 证据类型 | 当前结论 |
|---|---|
| 固定发布 | npm `1.4.0`, tarball digest；tag `v1.4.0`→`3b0103bc…`，npm/git version 与 manifest 对齐；附件等同性未独立计算 |
| Release package graph | 主包 + 7 子包/rows；无 glass row/package；better-sidebar optional；DSH engine `^0.2.0-rc.1` |
| 实现机制 | host/client injection、Scene/Web fallback、video controls、preset schema/assets、settings migration、teardown 从固定源码读过；非 runtime 实测 |
| Tests / CI | source guards 与 same SHA Windows/Ubuntu check success 已读；本次未跑测试或本机 build |
| 采用信号 | ★ 4,189 / npm last-month 109,268（含 CI/镜像），不代表用户数或机制质量 |
| 未验证 | 实际 WebGL/GPU/ffmpeg 性能、复杂第三方 scene、预设跨版本导入、同其他 UI bundle 共存、安装顺序要求与真实 DSH unload teardown |

**旧卡偏差**：目录 YAML 及旧卡曾写 `0.1.5-rc.1`/静态 Scene；这是旧口径。本卡对机制限定于固定 1.4.0，不将旧描述套到当前版。

---

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 一种资产格式要求启动另一个桌面程序 | 按“当前宿主进程能否直接渲染”定义支持矩阵；不可执行的 Application 资源显式排除，仍可保留其它可用格式。 | `[SRC-TARGET]` 1.4.0 supported format/catalog code + README；Application 不进 library/rotation。 | 避免用户看到无法启动的资产；代价是削减兼容范围并解释格式边界。 | 按 host/browser capabilities 探测，不仅按文件扩展名；错误资源显示原因。 | Scene/Web fallback 对第三方项目不是完整 Wallpaper Engine 等价模拟。 | 静默展示黑屏/不可交互资源，用户误判产品故障。 |
| Scene/Web/Video 都消耗显卡/解码器 | 为每类资源定独立 budget/fallback：poster/placeholder、live timeout、transcode queue/concurrency/deadline/cache、cancel cleanup。 | `[SRC-TARGET]` v1.4.0 scene fallback + transcode limits 见[`11 源码复核`](./_证据/11_视觉资产-dsh-wallpaper-engine-源码复核.md)；未运行硬件。 | 控制资源竞争且可在失败后退到低成本视觉；代价是多级 cache/state 和体验质量降低。 | 给每个 fallback 定 timeout/状态/取消/缓存 invalidation，并在目标 GPU/OS 测样本资产。 | 并发/帧率限制不保证整体 CPU/GPU/RAM 或所有作品性能。 | 只限制 FPS 仍可能并发转码堆积、抢解码器或硬件卡死。 |
| 外观预设需分享多项设置和素材 | 用版本化 full-values snapshot 加 optional asset sections；明确 absent/null/default/embedded asset 语义，导入先存档、显式应用。 | `[SRC-TARGET]` preset schema/routes；schema mismatch 返回 obsolete，不自动 migrate；预设不含完整壁纸媒体库。 | 预设自包含且能保留用户覆盖选择；代价是 schema upgrade 会要求重存、asset size/validation。 | 定义 schema tag、sanitize、asset limits、import atomicity、trusted path 与版本失效 UX。 | 本实现对旧 schema 是废弃，不是自动迁移；不得宣传跨大版本无损兼容。 | 旧预设被静默错映射、丢资源或覆盖现有用户设置。 |
| 视觉模块含主包、renderer、字体、pet 等大依赖 | 拆成有版本纪律的 package family，同时明确哪些 row 由 host main 提供服务、依赖缺失如何 fail。 | `[SRC-TARGET]` v1.4.0 package graph/release order/teardown；八 package rows；better-sidebar 是 optional companion。 | 可单独停部分能力并控制发布顺序；代价是跨包 exact version、host service contract 与兼容测试。 | 固定 package versions、publish order、service deps 和 safe unload/failure path；确认用户可组合路径。 | 该版没有 glass 独立子包；旧版本或 README 叙述不能移植为当前 release 事实。 | 主包/子包版本错配或主服务先卸载，造成依赖插件 park/残留或整组不加载。 |
| “不增加 token”是纯视觉产品承诺 | 将 model-facing tool/prompt registration 设为可测试的 architecture contract，并在每次 release 做 static/host checks。 | `[SRC-TARGET]` host manifest/entry + `verify-token-contract.mjs`；source only。 | 让用户可区分外观开销与模型上下文成本；代价是新 feature 要过 contract gate。 | 列出允许的 client/host services，测试 prompt/tool surface 不变化。 | 仅对 1.4.0 可支持该结论，不永久约束未来产品版本。 | 后续便利功能悄悄注入工具/提示，打破零模型侧预算。 |

---

## 6. 已知失效边界与下一步验证

| 风险/触发 | 固定版本理解 | 仍待验证 |
|---|---|---|
| Scene/WebGL/WebWallGL failure | README/docs/source define multi-step fallback, includes poster/custom/empty states | GPU driver, live WebGL and complex third-party scene behavior on actual host |
| Web wallpaper trust boundary | iframe `sandbox="allow-scripts"`, injected shim, loopback-origin/bridge constraints | malicious payload threat model, browser CSP/cross-origin enforcement in supported browsers |
| Video / ffmpeg unavailable | transcode may be skipped and original video used; software encoder and concurrency/time caps exist | target codec support, process resource usage, real cancel/disconnect races |
| Preset schema mismatch | older schema returns obsolete; no automatic migrate | UX for obsolete preset, manual export/re-save, asset conflicts and actual import rollback |
| Subpackage unload | main provides host service; dependency lifecycle parks subpackage fiber; no glass row in this release | actual running profile unload and persisted DOM/storage cleanup; not measured here |
| Optional companion/UI overlap | better-sidebar optional, and different skin plugins may overlap | cross-plugin ownership/detection/conflict behavior |
| Install sequencing | docs ask full DSH exit before install; no hard better-sidebar semver dependency found | clean one-time scratch profile update/install vs running process across OS |

## 7. 下一步复核

- [ ] 在 disposable Web profile 和 GPU-capable browser 测 scene live fail chain、first-frame budget、Web sandbox bridge、video playback/transcode/cancel；记录 GPU/OS/browser/sample file。
- [ ] 测 preset absent/null/assets semantics、obsolete schema refusal、broken asset preflight 与 partial asset install recovery；不触碰用户 preset/壁纸库。
- [ ] 比较 plugin manager disable/remove 与 host/client `ctx.effect` teardown；确认 body/root/style、route、ffmpeg child process、cache 和 user media 是否清理/保留。
- [ ] 对 Steam/Wallpaper Engine、better-sidebar 与其他 skin packages 的可选/冲突关系在 profile 中单独验证，不因目录旧描述推断 hard peer。
