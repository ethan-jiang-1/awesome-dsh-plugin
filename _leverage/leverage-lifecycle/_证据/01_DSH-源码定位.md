---
title: "证据 01 · DSH 源码定位（0.2.1-rc.3）"
domain: lifecycle
kind: evidence
positioning: "本册全部 [DSH] 断言的原始定位：包 + 文件 + 行号 + 它到底保证了什么。"
read_when: "要复核某条 [DSH]；或基线升级时批量重扫引用。"
status: observed
updated: 2026-11-01
budget: 120
---
# DSH 源码定位

> **基线**：`@deepseek-ai/dsh@0.2.1-rc.3`，读取位置为全局安装目录 `…/lib/node_modules/@deepseek-ai/dsh/`（本机 `node v22.23.1`）。行号为该安装物内的行号，升级后可能平移。

## 1. CLI 与 profile 归属

| 断言 | 定位 | 保证了什么 |
|---|---|---|
| `desktop` 不可由 CLI 启动 | `dsh` · `lib/bin.js:35-37`（启动路径）、`:119`（`plugin` 路径） | 两处都调 `rejectElectronProfile`；除非 carrier 传入 `manageDesktopProfile` |
| carrier 才能管 | `dsh` · `lib/bin.js:98-101`、`:209-210` | 该开关是**程序化选项**，不是命令行参数 |
| profile 只能单选 | `dsh` · `lib/bin.js:31-34` | `selectProfile` 拒绝重复 `--profile` |
| 自定义 profile 不由启动创建 | `dsh-app-boot` · `lib/index.js:1068-1070` | 抛 `profile "X" does not exist; create it with 'dsh plugin --profile X add <package>'` |
| 出厂模板只有五个 | `dsh-app-boot` · `lib/index.js:551-559` | `acp` / `web` / `headless` / `sdk` / `sdk-minimal`，**无 `desktop`** |
| 无模板时的默认层 | `dsh-app-boot` · `lib/index.js:570` | `DEFAULT_PROFILE_BUNDLES = ["@deepseek-ai/dsh-base"]` |
| 出厂可选 bundle | `dsh-app-boot` · `lib/index.js:579-590` | 12 个实验 bundle，默认关闭，由插件管理器以"关着"提供 |

## 2. 安装

| 断言 | 定位 | 保证了什么 |
|---|---|---|
| CLI 安装转发 pnpm | `dsh` · `lib/plugin-BiveYA7h.js:63-98` | 在 profile 目录跑 pnpm，附 `outputBytes`、锁等待等 |
| 首次使用即初始化 | `dsh` · `lib/plugin-BiveYA7h.js:37-41` | 非 `desktop` 先 `initProfile(...)` |
| 不兼容时给豁免命令 | `dsh` · `lib/plugin-BiveYA7h.js:95` | 打印 `allow-version … --accept-risk` 精确版本命令 |
| git 包需 allowBuilds | `dsh` · `lib/plugin-BiveYA7h.js:97` | 指明写进 profile 的 `pnpm-workspace.yaml` |
| 安装后 reconcile | `dsh-plugin-manager` · `lib/types/operations.js:95-122`、`:559` | 新装且声明 `dsh.bundle` 的包被 `push` 进 `dsh.profile.bundles`；**不重新启用旧依赖** |
| 非 bundle 只警告 | `dsh-plugin-manager` · `lib/types/operations.js:111` | 输出 `declares no dsh.bundle — installed as a plain dependency, not a profile layer` |
| 安装语义是"当前 profile" | `dsh-plugin-manager` · `package.json` description；`lib/types/tools.js:1`；`lib/types/index.js:540` | 包自述 *Current-profile plugin and bundle management shared by dsh CLI, Web and agent tools*；`installBundle(spec, options)` 无 profile 参数 |
| 移除需要停宿主（无 HMR 时） | `dsh-plugin-manager` · `lib/types/tools.js:17` | 文案：*This profile runs without HMR; tell the user to stop DSH and run `dsh plugin --profile <profile> remove <bundle>`* |

## 3. 启动

| 断言 | 定位 | 保证了什么 |
|---|---|---|
| 补丁叠加顺序 | `dsh` · `lib/profile-boot-C14i-8IN.js:224-229` | bundle（按 roster 顺序）→ profile → home → `--patch` → telemetry |
| 根 `cordis.yml` 每次重写 | `dsh` · `lib/profile-boot-C14i-8IN.js:201-221` | 防 Loader 回写导致重复插入 |
| home 层路径 | `dsh` · `lib/profile-boot-C14i-8IN.js:115-117` | `$DSH_HOME/cordis.patch.yml`，压过 profile 层 |
| 整体失败与清理 | `dsh` · `lib/profile-boot-C14i-8IN.js:255-327` | 失败时先 dispose 再抛；信号处理与 5s 强退 |
| 救援：用出厂模板重建 | `dsh` · `lib/profile-boot-C14i-8IN.js:146-200` | staging 目录 + rename；失败可回滚；不能对出厂同名 profile 使用 |
| 只在 boot 成功后提交 ready | `dsh` · `lib/profile-boot-C14i-8IN.js:313-314` | `fiber.state === 2` 且有 `loader` |
| 重启原因 | `dsh-plugin-manager` · `lib/types/index.js:944-953` | `hmr.reconcileProfile` 给 `restartReason`；无 `hmr` 时 `application: 'restart-required'`, `restartReason: 'no-hmr'` |

## 4. 两个面

| 断言 | 定位 | 保证了什么 |
|---|---|---|
| 同一份 web 层 | `dsh-web-app` · `cordis.patch.yml:315-319` | 注释写明 *the sidebar Plugins page installs, enables, disables, and removes the profile's bundles through the `pluginManager` Remote*；`ui-plugin-manager` 在本层 |
| Desktop 靠 profile 名分叉 | `dsh-web-app` · `cordis.patch.yml:47`、`:59`、`:298` | `ctx.get('profileContext')?.name !== 'desktop'` |
| 平台相关行 | `dsh-base` · `cordis.patch.yml:123` | `desktopPlatform` 仅在 `name === 'desktop'` 时取平台 |
| 宿主服务在 base 层 | `dsh-base` · `cordis.patch.yml:16-22` | `plugin-manager` 在有 profile 上下文时启用；`tool-plugin-manager` 默认 `disabled: true` |

## 5. 首启

| 断言 | 定位 | 保证了什么 |
|---|---|---|
| 账本升序、一次一个 | `dsh-client-ui-settings-general` · `lib/client.js:1169-1183`、`:489-496` | 按 `order` 排序；只渲染 `onboardingStep.id` 一个 |
| 自带 `welcome-notice` | `dsh-client-ui-settings-models` · `lib/client.js:4502-4507` | `order: -100`，且 `if (!('dshDesktop' in globalThis))` 才注册 |
| 自带 `deepseek-official` | `dsh-client-ui-settings-models` · `lib/client.js:4508-4515` | `order: 0`，挂模型登录子槽 |

## 6. 复核方式

```sh
cd "$(npm root -g)/@deepseek-ai/dsh"
sed -n '35,37p' lib/bin.js
sed -n '95,122p' node_modules/@deepseek-ai/dsh-plugin-manager/lib/types/operations.js
sed -n '315,319p' node_modules/@deepseek-ai/dsh-web-app/cordis.patch.yml
```

升级基线时按上表逐行重读；行号平移就改行号，**不要改结论方向**。
