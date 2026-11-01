---
title: "BOOT · 阶段②：重启、刷新、HMR 的语义分界"
domain: lifecycle
kind: playbook
positioning: "profile 由哪些文件构成、补丁怎么叠、启动失败坏在哪一层，以及三种“让它生效”的差别。"
takeaway: "CLI 装完不会通知正在运行的宿主：不重启就是没生效，而且没有任何提示；应用内装会告诉你。"
read_when: "要写“装完重启”这类提示；或排查“装上了但界面没变”。"
status: living
updated: 2026-11-01
budget: 160
---
# 阶段② · 起

## 1. 原生怎么做

**profile 就是四个文件加一个依赖树。** 实测抄录（`[RUN]` E1，全新 `DSH_HOME` 下 `dsh --profile web --dump-config`）：

| 文件 | 内容 |
|---|---|
| `package.json` | `name: dsh-profile-web`、`private: true`、`dependencies: {}`、`dsh.profile.bundles` |
| `cordis.yml` | 空的行列表 `[]`，注释写着 *Edit cordis.patch.yml, not this file* |
| `cordis.patch.yml` | 你的补丁层，出厂为 `[]` |
| `pnpm-workspace.yaml` | `packages: [.]`、`nodeLinker: hoisted`、`autoInstallPeers: false` |

**补丁叠加顺序**（从低到高）`[DSH]`（`lib/profile-boot-C14i-8IN.js:224-229`）：

```text
bundle 层（按 dsh.profile.bundles 的顺序）
→ profile 的 cordis.patch.yml
→ $DSH_HOME/cordis.patch.yml（机器级，压过 profile 层）
→ --patch 覆盖（按 argv 顺序）
→ telemetry 开关
```

**根 `cordis.yml` 每次启动都会被重写成 `[]`**：因为 Loader 可能把合成后的树写回根文件，留着会重复插入 `[DSH]`（`profile-boot-C14i-8IN.js:201-221`）。

**救援**：`--from-default-profile <出厂模板>` 用出厂模板重建一个**自定义** profile（staging 目录 + rename，失败可回滚）`[DSH]`。实测 `--profile rescue --from-default-profile web` 得到一个 `[dsh-base, dsh-web-app]` 的新 profile `[RUN]`。**但不能拿出厂同名 profile 当目标**：`--profile web --from-default-profile web` 直接报错 *names shipped profile "web" and cannot be a custom profile target* `[RUN]`。

**失败分三级**，别混为一谈：

| 级 | 表现 | 进程 |
|---|---|---|
| bundle 级 | `skipping profile bundle "<pkg>": <reason>` 后继续 | 活 `[DSH]` |
| **row 级（pending）** | `pending (waiting for service: <name>)`——依赖的服务没就绪，**既没激活也没失败** | **活** `[RUN]` |
| **row 级（import 失败）** | `warning: N entry did not activate` + 该行 import 错误 | **活** `[RUN]` |
| 整体 | 组合失败抛错，退出 | 死 |

> **pending 与失败要分开读。** 启动摘要是一句 `did not activate`，但 pending 说的是"等一下就好了"，失败说的是"这行根本起不来"。把 pending 当失败去改代码，是常见误判 `[RUN]`。

> 产品线 `horizon` 里"启动是全有或全无"这句 `[CARD]`，在本轮实测里**只对 bundle/组合级成立**；**单个 row 导入失败是被隔离的**。

## 2. 实测读到什么

| 实验 | 观察 |
|---|---|
| E8 启动一个含未安装包行的 profile | `warning: 1 entry did not activate` + `ERR_MODULE_NOT_FOUND`: *Cannot find package 'dsh-feas-probe' imported from …/profiles/web/*；**服务照常起来并打印 URL** |
| E13 运行中 CLI 装 bundle | 安装 exit 0；**同一进程再取首屏，`__DSH_BOOT__` 里没有新模块**；宿主 stderr **完全静默** |
| E13 重启后 | `__DSH_BOOT__` 出现 `"id":"dsh-feas-client"`，带 `rev` 与 `inject` |

**所以三种"生效"必须分开写**：

| 说法 | 谁做 | 宿主知道吗 |
|---|---|---|
| **重启** | 用户 | 重启后必然生效 |
| **页面刷新** | 用户 | 只换客户端模块，宿主侧行不重载 |
| **HMR** | 宿主自己 | 有 `hmr` 服务时 `reconcileProfile` 可能直接应用；否则返回 `restart-required` `[DSH]`（`dsh-plugin-manager/lib/types/index.js:944-953`） |

**关键差别**：应用内装是宿主自己动手，所以能给出 `restart-required` + `restartReason`（例如 `no-hmr`）；**CLI 装是另一个进程，宿主根本不知道**——所以 CLI 装完必须重启，而且没有任何提示。

## 3. 样本怎么偏离

25 张卡在这一点上各说各的 `[CARD]`：

| 说法 | 样本 |
|---|---|
| 明确**不用**重启 | `31_驾驶舱`（"无构建、无重启"） |
| 明确要**重启一次** | `42`、`43`、`51`、`61`；`profile/11`–`17` 多数 |
| 要**硬刷新** | `12_厚工作台`、`21_生成式界面` |
| **热停用**（不重启） | `51`（patch + HMR 约 1 秒） |
| 什么都不说 | `11`、`52`、`71`、`81`；`17`、`18` 连启动命令都没写 |

对照本轮结论：**说"不用重启"的，基本是只改客户端渲染或只加工具行的样本；说"要重启"的，都在改宿主侧行。** 这不是文风差异，是行加载位置的差异——描述时应该按"改了哪一侧"来写，而不是按习惯写。

**本册样本补充**：五张卡覆盖五种"怎么生效"——

[`21`](./21_启动期注入-dsh-rhine-splash.md) 首屏注入（append 不 prepend）·
[`22`](./22_重启取证-dsh-update-checker.md) 自重启取证（结果文件+实例身份+端口）·
[`23`](./23_外部进程生命周期-dsh-noema.md) 子进程生死（懒起/保活/退避）·
[`24`](./24_事务式修复-dsh-doctor.md) 修完可回滚 ·
[`25`](./25_装完还要一步-dsh-context-guardian.md) 生效是显式一步且默认 dry-run。

## 4. 三条判据

1. 文档里的动词对不对：**改宿主行 → 重启**；**只换客户端模块 → 刷新**；**宿主自己应用 → HMR**。
2. 每一个"装完即可用"的承诺，都问一句：宿主是怎么知道的？CLI 装的情况下答案是"它不知道"。
3. 不要用"全有或全无"描述启动；写成三级（bundle / row / 整体）。

## 5. 失效与开放问题

- `[OPEN]` 运行中的应用内安装，`restartReason` 在 `web` profile 上的实际取值分布（`no-hmr` 之外还有什么）。
- **已关**：页面刷新**不能**让新增的 `dsh.client` 模块出现。E13 在同一进程内重新取首屏，`__DSH_BOOT__` 里没有新模块；重启后才出现 `[RUN]`。
- **已关**：救援路径可用，且对出厂同名 profile 有硬闸 `[RUN]`（E15/E16，见 §1）。

## 样本

| 文件 | 一句话 |
|---|---|
| [`21_启动期注入-dsh-rhine-splash.md`](./21_启动期注入-dsh-rhine-splash.md) | `index-inject` 在 React 之前改首屏；append 不 prepend。 |
| [`22_重启取证-dsh-update-checker.md`](./22_重启取证-dsh-update-checker.md) | 重启没有返回值，所以要造三件证据。 |
| [`23_外部进程生命周期-dsh-noema.md`](./23_外部进程生命周期-dsh-noema.md) | 外部进程的懒起、保活、退避与并发去重。 |
| [`24_事务式修复-dsh-doctor.md`](./24_事务式修复-dsh-doctor.md) | 修之前先备份；救生链上的行一律不自动改。 |
| [`25_装完还要一步-dsh-context-guardian.md`](./25_装完还要一步-dsh-context-guardian.md) | 生效是显式一步，默认 dry-run。 |
