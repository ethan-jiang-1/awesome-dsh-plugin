---
title: "源码复核：视觉资产 dsh-wallpaper-engine"
domain: reshape-product
kind: evidence
positioning: "固定 npm dsh-plugin-wallpaper-engine@1.4.0 与 v1.4.0 release commit，核验包/行、渲染降级、预设资产、零模型侧注册、生命周期与 CI。"
read_when: "复核 profile/18 的玻璃拆包、格式/Scene 降级、视频负载、预设 schema、安装顺序和 better-sidebar 前置主张。"
status: observed
updated: 2026-10-31
---
# 源码复核：视觉资产 dsh-wallpaper-engine

> 只读第一方 npm registry、上游固定 release source、固定 DSH `dsh-v0.2.1-rc.3` 契约与远端 CI。未下载/解包 tarball、安装、构建、运行或执行测试。`[DOC]` 是发布文档主张；`[SRC-TARGET]` 是 release tag 指向源码；`[SRC-DSH]` 仅说明该版本声明依赖的宿主契约；`[TEST]` / `[CI]` 分别是测试定义和该 SHA 的远端结果；`[RUN]` 无。

## 版本与发布身份

- **[SRC-TARGET: exact release pin]** npm 精确记录 [`dsh-plugin-wallpaper-engine@1.4.0`](https://registry.npmjs.org/dsh-plugin-wallpaper-engine/1.4.0) 的 `version` 为 1.4.0，tarball 为 [`dsh-plugin-wallpaper-engine-1.4.0.tgz`](https://registry.npmjs.org/dsh-plugin-wallpaper-engine/-/dsh-plugin-wallpaper-engine-1.4.0.tgz)，SHA-1 `4b1e609b5485533526fe48c4eda0d79c11dd062f`，SHA-512 `sha512-9vZN7nTdVu3pQlUd3F9vitKonkrxqyiePe0fpme8xyRWJhZTdio3SBMyB1dqOkbKhus3Rc/8hIw1urhLg2UysQ==`，144 files / 7,267,063 unpacked bytes，`engines.dsh: ^0.2.0-rc.1`、Node `>=22.12.0`。该精确 metadata 未提供 `gitHead`，npm provenance endpoint 对此包/版本返回 404，不用 provenance 推 source。
- **[SRC-TARGET: tag to commit]** GitHub 的 [`v1.4.0` annotated tag object](https://api.github.com/repos/elysia395/dsh-wallpaper-engine/git/tags/2a4870b4015ab20ad46a99194d6dbff0dcb74fb4) 指向 commit **`3b0103bc1d5431840208966ce67155f392c4095c`**。固定的 [package.json](https://github.com/elysia395/dsh-wallpaper-engine/blob/3b0103bc1d5431840208966ce67155f392c4095c/package.json) 与 registry 一致：name/version/engines 与 `dsh.bundle.patch`、client web inject。故源码推读限定于此 commit；可复核的 pinned commit links 均使用完整 SHA，而非 `main` / `HEAD`。
- **[SRC-TARGET: tarball identity caveat]** GitHub [v1.4.0 Release](https://github.com/elysia395/dsh-wallpaper-engine/releases/tag/v1.4.0) 的正文自述附件和 npm 是同一构建，并列出主包及七个子包 tarball、`release-set.json`、`SHA256SUMS.txt`；主包附件摘要 SHA-256 `81567ee656fe5a1f1a4131c3389cb16d92868113f5d7d536c499ed3b6de39d57`，但该 release API 标 `immutable:false`。npm 记录与 tag 对版本和声明相符；本轮未取附件计算摘要或逐字节比对 npm tarball，不能称已独立验证两份 tarball 字节相同。
- **[SRC-TARGET: version-specific correction]** 1.4.0 根包有**主包 + 七个子包**共八包。子包为 `about-notice`、`fonts`、`fx`、`mascot-avatar`、`media-bridge`、`parallax`、`pet-link`；主包 `dependencies` 只有 `webwallgl: ^3.0.0`、`x11: ^4.3.1`，子包在发布形态另由精确 1.4.0 运行依赖组装。固定 tag 的 [cordis.patch.yml](https://github.com/elysia395/dsh-wallpaper-engine/blob/3b0103bc1d5431840208966ce67155f392c4095c/cordis.patch.yml) 有八个主包拥有/管理的行：主壁纸、about、mascot/avatar、media bridge、pet link、fx、parallax、fonts。**没有 `wallpaper-engine-glass` 行或 glass 子包**：卡片所称独立玻璃行属于其他版本/后续代码，不能用于 v1.4.0 结论。更正：该版描述称 `dsh-better-sidebar` 无版本要求，并非硬依赖；不是目录 YAML 里旧版的 `>=0.19.0`。

## DOC

- **[DOC]** 固定 [README.md](https://github.com/elysia395/dsh-wallpaper-engine/blob/3b0103bc1d5431840208966ce67155f392c4095c/README.md) 将 Scene / Web 归实时 WebWallGL 渲染，Video 浏览器播放；Application 不支持且不进入库/轮播；自定义 JPG/PNG/MP4 上传；ffmpeg 不可用时转码/FPS 限制不可用、视频仍原片播放。macOS 没有 Wallpaper Engine 客户端时可上传或指向项目目录。
- **[DOC]** README 声明配置在宿主 `~/.dsh-wallpaper-engine/config.json`、上传目录默认 `~/.dsh-wallpaper-engine/uploads`，缓存可配；旧 localStorage 设置首次启动自动迁移。导入导出预设可选择携带字体、吉祥物、头像资产；README 同时说明有些设置/运行时状态并不在预设中。实现 schema 和迁移边界见 SRC-TARGET，避免把 README 营销简述当完整规格。
- **[DOC]** README 明确称“不向模型注册工具或注入提示文本，不增加模型 token 开销”。源码包 metadata 清单属于技术验证，见下文；不是对所有未来修改的永久保证。

## SRC-TARGET

### 包、行与模型侧边界

- **[SRC-TARGET]** 固定根 [manifest](https://github.com/elysia395/dsh-wallpaper-engine/blob/3b0103bc1d5431840208966ce67155f392c4095c/package.json) 的 `dsh.client` 声明 `platform: web`、`immediately: true`、注入 `@deepseek-ai/dsh-client-runtime`；peer 声明 Cordis、client runtime/UI slots、host webserver 和 React。Client 插件由客户端加载，宿主入口 `lib/index.js` 依赖 `webServer`，声明 `inject=['webServer']`：无该服务的 profile 不加载，而非缺失时跳过路由。
- **[SRC-TARGET]** [host entry](https://github.com/elysia395/dsh-wallpaper-engine/blob/3b0103bc1d5431840208966ce67155f392c4095c/lib/index.js) 的文件头明确 no model-visible tool / no prompt text。Host 侧提供 HTTP 路由和文件/配置服务；client inject 是浏览器模块装载，不是 model tool。该 release 的 token 合同有 [verify-token-contract.mjs](https://github.com/elysia395/dsh-wallpaper-engine/blob/3b0103bc1d5431840208966ce67155f392c4095c/test/verify-token-contract.mjs) 静态守卫；这是代码结构证据，不代表本轮调用模型验证。
- **[SRC-TARGET]** 主 patch 注释表明插件行开关需要重新加载/重启对应宿主，不是即时切换；整组 client 半边来自主包 metadata。子包被分成独立 host rows，可单行停用；不过“停用后整个行的 UI 一起退出”要按组件实现及测试理解，不应推广成每行所有资源都绝不加载。

### 格式、Scene 与 Web 沙箱

- **[SRC-TARGET]** 固定 [HOW-IT-WORKS.md](https://github.com/elysia395/dsh-wallpaper-engine/blob/3b0103bc1d5431840208966ce67155f392c4095c/docs/HOW-IT-WORKS.md)：Scene/松散 `scene.json` 与 Web 默认走 npm `webwallgl` 实时渲染；本仓 `lib/webwallgl/` 是适配页，不等于引擎源码。Scene 文件通过 `/scene-files`，入口 `/scene-live`。场景实时失败后唯一出图顺序是 **live iframe → 场景内嵌 MP4 → 实时抓帧缓存 → 用户自定义画面 → 明确空态**；首帧前的占位顺序则是实时抓帧 → 作者预览图 → 主题色。Application 可列出但不渲染、不进入产品库/轮播候选（README 口径）。
- **[SRC-TARGET]** Web 壁纸由 `/scene-files` 提供 HTML/子资源，并向入口注入 WE API shim 和 `project.json` 属性 seed；iframe `sandbox="allow-scripts"`，跨源控制/指针消息通过 `postMessage`。载入失败或运行失联会退回兼容裸 HTML iframe（不保证 WE API 等价）。桌面形态用独立 loopback media origin，网页内容不带宿主 origin；文档明确 `Origin: null` 下作者 `fetch`/XHR 有边界，CSS hover 等浏览器 hit-test 交互不受外部 pointer 注入影响。
- **[SRC-TARGET]** 失败记忆区分会话内传输软失败与持久渲染失败；首帧预算随载荷大小计算，载荷仍增长时续计。隐藏/未播放实例不载入大载荷以免抢带宽/解码器。文档描述 Scene WebGL2、驱动与复杂工坊项目兼容性限制；它不承诺任意 Wallpaper Engine 工程等同原生表现。

### Video 转换与资源限制

- **[SRC-TARGET]** 固定 [transcode.js](https://github.com/elysia395/dsh-wallpaper-engine/blob/3b0103bc1d5431840208966ce67155f392c4095c/lib/media/transcode.js) 实现抽帧降帧，不改变播放时间线：转码输出按源路径/mtime/FPS 建缓存，源已不高于上限则不需抽帧；client 可先用缓存产物作为 src，失败回退原文件。编码器顺序为 AV1 NVENC → H.264 NVENC → libx264；软件档 CRF 20。缺 ffmpeg 时运行期依次考虑显式 env、本地文件、按平台懒下载且 SHA256 校验、PATH；CI 工作流不会执行下载，见 TEST/CI。
- **[SRC-TARGET]** 并发编码上限 2，排队不计入单任务硬期限；默认单任务 15 分钟，可由 `DSH_WE_TRANSCODE_TIMEOUT_MS` 覆盖。用户断开后若所有等待者离开会 abort 子进程并清临时输出；卸载时杀活跃 ffmpeg 子进程。下载二进制流写盘计算 SHA256、最低体积与 magic 校验；环境不支持下载时最终回退 PATH/原视频。文档不提供通用 GPU/CPU/内存上限或跨硬件性能保证；帧率上限不是整体动画帧率承诺。
- **[SRC-TARGET]** `test/verify-transcode-state.mjs`、`verify-playback-controls.mjs`、`verify-media-probe.mjs` 等静态/夹具守卫定义逻辑边界；未运行，不据此宣称实际设备上的画质、时延或 FPS。

### 预设、资产与迁移

- **[SRC-TARGET]** 固定 [presets.js](https://github.com/elysia395/dsh-wallpaper-engine/blob/3b0103bc1d5431840208966ce67155f392c4095c/lib/routes/presets.js) 定义预设 JSON：`{$schema, id, name, values, assets?}`。`values` 是 `PROFILE_PRESET_KEYS` 的**完整快照**，读/写时经 settings schema 清洗、缺键补默认；`assets` 是可选字体/吉祥物/头像段。预设不是一组局部 delta，也没有 active pointer。内置预设在随包只读目录，用户层在数据目录 `glass-presets/`，用户层优先；写用户层原子落盘。
- **[SRC-TARGET]** 资产段四态语义：段缺席=保持接收方现值；`null`=显式清除/回内置默认；mascot 字符串=指向内置形态；对象=携带资产。预设 GET 只回 metadata，不传图片字节；导出通过普通 JSON attachment 携带选择的资产段；导入只保存不自动应用，点击应用时由 client 合并 `values` 并调用 settings 写入，再调用 `install-assets` 安装图像文件。图片支持 png/jpg/webp；宿主按文件白名单、尺寸形状清洗、单图 8 MiB 限制，总请求体按三项 base64 预算设限，并在任何删除/写入前整体预检超限项。
- **[SRC-TARGET]** 版本兼容是明确的作废策略：schema tag 不匹配的旧预设返回 `version-obsolete`，**不迁移、不容忍旧 schema**；这是“格式版本升级后要求重存”，不是跨版本保留承诺。删除内置预设用用户层墓碑持久遮蔽，不能恢复；用户存档原子写，包内预设不修改。
- **[SRC-TARGET]** 上传壁纸由独立 upload 路由和本地目录存储，不等同预设 `assets`：预设携带字体/立绘/头像，不包含 Wallpaper Engine 媒体库整体。固定 [UPGRADING.md](https://github.com/elysia395/dsh-wallpaper-engine/blob/3b0103bc1d5431840208966ce67155f392c4095c/docs/UPGRADING.md) 记录 v0.4+ 从浏览器 localStorage 到宿主 `config.json` 的旧设置迁移；缓存帧会按管线 key 失效重建。不要把这条设置迁移误读为预设 schema 自动迁移。

### 安装排序与卸载

- **[SRC-TARGET]** 固定 [RELEASING.md](https://github.com/elysia395/dsh-wallpaper-engine/blob/3b0103bc1d5431840208966ce67155f392c4095c/docs/RELEASING.md) 和根 manifest 定义发布依赖：主包要引用七个精确同版子包；子包先发布、主包最后，缺任一子包会造成解析失败。GitHub release 的排序清单是七子包后主包。普通 npm 单命令安装主包依赖会解析全套；不要单独激活子包 bundle（主 patch 负责插行）。安装指引要求完全退出目标 DSH，安装/更新后重启宿主；不是已证实“必须先更新 better-sidebar”的顺序。
- **[SRC-TARGET]** 组件宿主通过 `wallpaperEngineHost` Cordis service 取得冻结键面；主包 provide 服务，并把 teardown disposer 交入 `ctx.effect`。固定 [subpackage-boot.js](https://github.com/elysia395/dsh-wallpaper-engine/blob/3b0103bc1d5431840208966ce67155f392c4095c/lib/subpackage-boot.js) 注释说明注入依赖形成级联：主包卸载后其服务撤销，依赖它的子包 fiber park。主包也会检查 patch 声明的子包能否在仓库和 profile roots 解析，解析不到就抛错，避免行级失败静默导致部分 UI。
- **[SRC-TARGET]** 固定 [host-boot.js](https://github.com/elysia395/dsh-wallpaper-engine/blob/3b0103bc1d5431840208966ce67155f392c4095c/lib/host-boot.js) 的 `handOffTeardown` 将幂等 disposer 注册至 `ctx.effect`；单靠返回 disposer 不足以保证 Cordis 类式 apply 卸载。主入口在注册路由前登记 teardown，覆盖中途失败的回滚；具体行为是源码和守卫定义，不是本轮 live profile 实验。better-sidebar 在当前 README 及 manifest 描述为**可选配套**，没有依赖声明或版本下限。

## SRC-DSH

- **[SRC-DSH]** 用户指定的精确宿主 baseline 是 DSH tag [`dsh-v0.2.1-rc.3`](https://github.com/deepseek-ai/deepseek-harness/tree/1f81c047fc48fa190a683e469daa699857e9afe8) → commit `1f81c047fc48fa190a683e469daa699857e9afe8`。只用来理解插件声明的 `webServer` 注入/服务，以及 `@deepseek-ai/dsh-client-ui-slots` 中 slots/overlay 的消费契约；不把较新 Host API 当 v1.4.0 前置，也不推测 better-sidebar 的实际组合。
- **[SRC-DSH]** release manifest peer 要求 `@deepseek-ai/dsh-client-ui-slots >=0.1.5-rc.1`、host webserver/client runtime `>=0.1.5-rc.1`，DSH engine range 则是 `^0.2.0-rc.1`。Peer semver 下限不是全部 overlay/slot 行为等同保证；本节 host 引用应限为固定 commit 的契约链接，具体客户 profile 是否挂载仍需目标运行时验证。

## TEST

- **[TEST]** 固定 [package.json scripts](https://github.com/elysia395/dsh-wallpaper-engine/blob/3b0103bc1d5431840208966ce67155f392c4095c/package.json) 有 `verify`、`verify:docs`、`smoke`、`verify:all`、static lint/typecheck 等入口；[run-guards.mjs](https://github.com/elysia395/dsh-wallpaper-engine/blob/3b0103bc1d5431840208966ce67155f392c4095c/test/run-guards.mjs) 是 verify/docs/smoke 有序清单。硬档包含 client/token contract、scene/live、transcode/playback、settings schema、presets、upload/store、package/release-set、subpackage boot/purity/toggle-roundtrip/teardown 等守卫；docs 类布局/死码/可达性检查列软档。测试名与静态断言反映意图，不等于 UI 全流程实测。
- **[TEST]** CI 的 `full` 作业会在 Node 22 的 Windows 与 Ubuntu 跑 verify/static/smoke 和 bridge 检查；CI 依赖安装为 `npm ci --omit=peer --ignore-scripts`，随后显式 build。该事实不是本次执行安装。

## CI

- **[CI]** 对固定 release commit `3b0103bc1d5431840208966ce67155f392c4095c` 的 [GitHub check runs](https://api.github.com/repos/elysia395/dsh-wallpaper-engine/commits/3b0103bc1d5431840208966ce67155f392c4095c/check-runs) 显示 `full (ubuntu-latest)` 与 `full (windows-latest)` 均 completed/success；同 run 的 `ci/result` 成功。此为远端状态快照，不代表每个检查子项可从聚合 API 全量复核，亦不是本地重跑。
- **[CI]** 固定 [verify.yml](https://github.com/elysia395/dsh-wallpaper-engine/blob/3b0103bc1d5431840208966ce67155f392c4095c/.github/workflows/verify.yml) 变更分类为 fail-closed：代码走 Windows+Ubuntu full；docs/notice 快通道各有判定；`ci/result` 汇总。`verify:docs` 是软档并 `continue-on-error`；不应写成整个 workflow 所有门禁皆硬阻断。

## RUN

无。本轮未下载或解包 tarball，未安装、构建、运行插件/测试，未改卡片、catalog 或 BORROW。

## 结论与边界

npm `1.4.0` 与 `v1.4.0` → commit `3b0103bc…` 的版本来源足够固定，可对该 release 作源码复核。复核推翻 profile 卡里“玻璃独立子包行可停用”“必须 better-sidebar >=0.19.0”两项对 1.4.0 的陈述：该版本八包里无 glass 子包/行，better-sidebar 是可选配套。可保留的机制是 host/client 双半边、无模型工具/提示注册、Web sandbox、Scene 多级失败处理、受闸的转码、完整快照预设及分段资产语义；其中预设旧 schema 明确作废而非自动迁移。源码、文档和 CI 均不替代目标机器 WebGL/ffmpeg、实际插件行 teardown、玻璃视觉效果及具体 DSH profile 的运行验收。
