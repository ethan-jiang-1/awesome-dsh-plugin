---
title: "桌面应用 · DSH Desktop（Dataelem）"
domain: reshape-product
kind: sample
positioning: "Dataelem 的桌面发行版：签名安装包、Safe Mode、六小时更新检查，把 Harness 装成普通桌面软件。"
takeaway: "闭环恢复：Safe Mode 只挂官方 bundle，`--safe-mode` 是最后一条入口。"
read_when: "要做桌面发行版/安装器/安全模式；或判断第三方壳能占用哪个 profile。"
status: observed
updated: 2026-10-31
budget: 186
---
# 桌面应用 · DSH Desktop（Dataelem）:把 Harness 装成普通桌面软件

> **状态**:`observed`(README 级核过) · **基线**:DSH `0.2.1-rc.3`(其 README 自述的预览基线) · **读于**:2026-10-31
> **类**:`1` 壳与工作台 · **层**:2(表层)+ 5(默认值)+ 6(首启)+ 7(分发) · **★ 16,975 / forks 586 / open issues 136**(GitHub API,2026-10-31)
> **一句话**:它不是"给 Web GUI 加个窗口",而是**把运行时、安装包、更新通道、恢复面、手机通道一起当产品做**:安装即用、数据在应用目录外、坏了进 Safe Mode。
> **借鉴价值**:**① "Safe Mode = 只挂官方 core bundle 的隔离 profile",把插件故障变成可退出的状态而不是白屏;② 安装包按**目标平台各自构建**,签名/公证是分发的一部分;③ 更新**先问再下、装完再重启**,并且允许"跳过这一版";④ 手机是**独立配对桥**,不是把 127.0.0.1 打个洞;⑤ 渲染器**无 Node + 上下文隔离 + 沙箱**,壳的安全基线不靠自觉。**

> **证据深度**:README 级 + `docs/architecture.md`（未读源码）（2026-10-31）
> **样本档案**
> **repo**:[`dataelement/dsh-desktop`](https://github.com/dataelement/dsh-desktop) · **npm**:无(桌面发行版,不走 `dsh plugin add`) · **许可证**:MIT
> **目录条目**:**无**(口径外样本:它不在插件目录里,这正是"宿主侧会被目录系统性漏掉"的实例)
> **装法**:官网 <https://www.dshdesktop.com/> 下载 stable;或 GitHub Releases 取 Pre-release
> **平台**:macOS(Apple Silicon / Intel,签名+公证) · Windows x64(代码签名 NSIS) · **不支持 Linux / Windows ARM64**
> **已在本地挖掘**:[`../_证据/01_桌面与终端-原始挖掘.md`](./_证据/01_桌面与终端-原始挖掘.md) §二.1(README 原文摘录 + API 数字)
> **再深挖去哪**:`docs/architecture.md`(runtime flow / security boundaries / recovery)、`docs/preset-packages.md`(`.dshpreset` 契约)、`docs/release-runbook.md`(签名与发布管控)

---

## 它想干什么 · 为什么值得借鉴

**意图。** 让“跑 DSH”从“先装 Node、敲 `dsh web`、自己记端口”变成**双击一个签过名的安装包**：运行时随应用拉起，就绪后就是完整界面。它交付的单位是**一件桌面软件**——安装包、更新通道、恢复面、手机通道一起算，而不是 `dsh plugin add` 进去的一个包；也明确不做的三件事：不支持 Linux / Windows ARM64，不碰用户的 `~/.dsh`，不在用户不知情时静默更新。

**意义。** 它补的是“宿主侧”的空缺：目录只收插件，而这个 ★ 16,975 的产品**根本不在 `data/plugins` 里**，按目录做的普查会系统性漏掉整条宿主路线。它改的惯例是“桌面版 = 给 Web GUI 套个窗口”——签名与公证、每个产物在匹配的 OS/架构上各构建一次、stable 与 preview 两条通道，都是把分发当产品的一部分。更实用的一点：它证明第三方壳可以不抢 `desktop` 这个 profile 名，用自有 `harness/` DSH_HOME 加 `web` profile 照样做成发行版。

**用户价值。** 装之前，用户要自己解决 Node、npm 全局权限、终端与端口；装之后，下载对应平台安装包、打开即用，profiles / plugins / sessions / 模型设置全在应用目录之外，覆盖安装、换版本、卸载重装都不搬家。感到“值”的是只想把活干完的人：PPT 用户、非开发同事、临时在客户机器上演示的人。代价分给两边——作者持续付 macOS 公证与 Windows 代码签名，用户要接受没有 Linux、preview 可能与社区插件不兼容，以及异地连手机得回电脑看一眼 6 位口令。

**表达（界面与交互）。** 第一屏没有安装向导：装完打开就是完整界面，菜单栏/托盘常驻，**关窗口不等于退出**。更新被拆成三个可分别拒绝的动作——启动后不久检查一次、之后每 6 小时一次，发现新版**先问**，下载完还要点 **Restart and install**，并给 **skip this version** 且不隐藏后续版本。出事的表达更克制：启动失败被归因到**具体哪个插件**，恢复面直接给升级/批量升级/移除的动作，诊断只写 `harness.log` 而不要求用户翻目录；再不行退到 **Safe Mode**（只挂官方 core bundle 的隔离 profile，数据不动），连界面都进不去还有 `--safe-mode`。手机侧它不显示端口、不暴露 127.0.0.1：扫码走局域网，公网隧道才要那 6 位、默认 5 分钟只存内存的口令。

## 0. 一页速览(想抄的人只看这 20 行)

| 问题 | 它的答案 | 支撑 |
|---|---|---|
| 它是不是"插件" | **不是**。它是独立安装的应用:启动本地 Harness 运行时,运行时就绪后打开完整界面 | `[OBS]` README §What DSH Desktop adds |
| 数据放哪 | profiles / plugins / workspaces / sessions / 模型设置**全部在应用目录之外**,升级不搬家 | `[OBS]` 同上 |
| 版本通道 | stable 与 **preview** 两条;preview "may be incompatible with community plugins",只给尝鲜者 | `[OBS]` §Download |
| 更新节奏 | 启动后**不久**检查一次 + **每 6 小时**一次;发现新版**先问**,用户点 **Restart and install** 才装 | `[OBS]` §Download |
| 能不能跳过 | 能,**跳过这一版**且不隐藏后续版本 | `[OBS]` 同上 |
| 坏在哪看得见吗 | 启动失败与前端插件故障会被识别,诊断留在 **`harness.log`**,并给出**引导式恢复动作** | `[OBS]` §What it adds |
| 最坏情况 | **Safe Mode**:只挂官方 core bundle 的**隔离 profile**;Agent/会话/模型/工作区照常可用 | `[OBS]` §Safe Mode and recovery |
| 连界面都进不去 | 命令行 `--safe-mode` 直接起 | `[OBS]` 同上 |
| 手机怎么办 | Harness 只在**随机 127.0.0.1 端口**;手机走**独立配对桥**,口令默认 **5 分钟、只存内存**,可选持久化 | `[OBS]` §Phone access |
| 隧道 | Cloudflare Quick Tunnel 为主;**Pinggy 兜底**(约 60 分钟过期,给 Cloudflare 不可达的地区) | `[OBS]` 同上 |
| 渲染器权限 | **没有 Node 权限** + context isolation + sandbox;webview / 非受信导航 / 意外权限请求一律拦 | `[OBS]` §Local data and security |
| 外链 | 全部交给系统浏览器 | 同上 |
| 平台边界 | macOS 双架构 + Windows x64;Linux 与 Windows ARM64 **明确不支持** | `[OBS]` §Platform support |
| 安装包怎么来 | **每个产物在匹配的 OS/架构上构建**(Harness 带目标原生依赖) | 同上 |
| 最该抄的一句 | "**non-destructive Safe Mode**":恢复不删你的东西 | `[OBS]` |

## 1. 它在产品里的位置

**七层坐标**:它同时占了 **2**(表层:独立应用的窗口与菜单)+ **5**(默认值:模型/预设/主题的一套默认)+ **6**(首启:装完即起的第一次)+ **7**(分发:签名安装包与更新通道)。DSH 的 Web GUI 仍在,只是从"用户打开的网页"变成"应用内嵌的运行时"。

**它和上游的那条缝**:DSH 把 `desktop` 这个 profile 名**判给了官方 Electron 应用**(`lib/bin.js:35-37`:`profile "desktop" is managed exclusively by the Electron application`;`lib/plugin-BiveYA7h.js:10-12` 要求先打开官方桌面应用初始化、并完全退出后才能 `dsh plugin --profile desktop`)。所以第三方桌面产品只有三条路:

1. **自有 DSH_HOME + `web` profile**(本卡;`harness/` 是应用自己的 DSH_HOME,正常启动只碰 `web` profile)
2. 复用 `web` profile,只补壳(见 [`12_单文件桌面壳-windowos`](./12_单文件桌面壳-windowos.md))
3. 换一块屏(终端/手机),不碰 profile 名(见 [`15_终端工作区-seektty`](./15_终端工作区-seektty.md))

**一句话**:`desktop` 这个名字是上游资产,不是公共资源。**抄它之前先决定:你要抢这个名字,还是绕开它。**

## 2. 机制(可照抄)

### 2.1 安装包即产品:签名、目标架构构建、双通道

- macOS 产物 **code-signed + notarized**(Apple Silicon 与 Intel 各一份),Windows x64 是 **代码签名 NSIS**。
- "**every release artifact is built on the matching operating system and architecture**"——因为 Harness 依赖目标原生包,不能交叉打包。
- **stable / preview 双通道**:preview 明说可能与社区插件不兼容,只给尝鲜者;stable 走官网。

> **照抄点**:分发不是"压个包",是**为每个平台各建一次 + 签名 + 公证**,并把不稳定版本隔离到另一条通道。

### 2.2 更新:先问、后下、再重启,且允许跳过

1. 启动后不久检查一次 → 之后**每 6 小时**一次;
2. 发现新版 → **询问**,用户同意才下载;
3. 下载完 → 用户点 **Restart and install** 才安装(不是静默替换);
4. 提供 **skip this version**,且不隐藏未来版本。

> **照抄点**:把"检查 / 下载 / 安装"拆成三个可分别拒绝的动作。**静默更新对宿主型产品是负债**——它会在用户最不想重启的时候重启。

### 2.3 Safe Mode:插件故障的第三层否定

```
正常启动
  └─ 启动/前端插件故障被识别(运行时证据 + 前端证据)
       ├─ 引导式恢复面:升级受影响的插件 / 批量升级 / 移除
       └─ 还是起不来 → Safe Mode:隔离 profile,只挂官方 core bundle
            ├─ Agent / 会话 / 模型 / 工作区仍然可用
            └─ 从横幅里移除插件,或返回正常启动
                 └─ 连界面都进不去 → 命令行 --safe-mode
```

三个关键性质:

- **non-destructive**:隔离的是插件,不是数据;
- **可归因**:从运行时 + 前端证据**指认**某个插件,而不是"某个插件有问题";
- **两条入口**:菜单里的 "Restart as Safe Mode…" 与命令行的 `--safe-mode`——后者是**逃生死锁**。

> **照抄点**:恢复面必须**比故障面更早可用**。插件的插件化恢复(第 4 条"三层否定"的宿主版)在这里是:当前启动 / 安全启动 / 命令行启动。

### 2.4 数据外置:升级不搬家

profiles / plugins / workspaces / sessions / 模型设置都放在 Electron 的 per-user 应用数据目录,**不在安装目录里**。于是:覆盖安装、换版本、卸载重装都不会碰到会话。

> **照抄点**:**"升级"与"迁移"必须是两件事。** 安装包只换二进制;数据目录只被应用按需写。

### 2.5 手机 = 一台要配对的设备(宿主版)

- Harness 本体只监听**随机 127.0.0.1 端口**——不暴露局域网;
- 手机访问走**独立配对桥**,不是把 Harness 端口转发出去;
- 扫码即连(Wi-Fi);走公网隧道时,手机还要输入**电脑上显示的 6 位配对口令**;
- 口令默认 **5 分钟、只存内存**;持久化要用户**显式选择**;
- 断开手机 → 移动会话**立即失效**;
- 隧道**两条腿**:Cloudflare Quick Tunnel 为主,Pinggy 兜底(约 60 分钟过期)。

> **照抄点**:**随机回环端口 + 独立桥 + 短时口令**三件套。把"能连"与"能一直连"分开,是宿主型产品对远程面的最低承诺。

### 2.6 渲染器安全基线

- renderer **无 Node 权限**;context isolation + sandbox;
- webview、非受信的应用内导航、意外权限请求**一律阻断**;
- 外链交给系统浏览器(应用内不开新窗)。

> **照抄点**:壳的权限模型要**先于功能**写死。宿主产品一旦拿到 Node,后面所有"沙箱"都是装饰。

### 2.7 诊断:一条日志 + 引导动作

- 启动/插件故障写 **`harness.log`**;
- 恢复面直接给**可执行动作**(升级、批量升级、移除、回正常启动);
- 不要求用户去翻目录找日志。

## 3. 体验

- **第一次打开**:下载对应平台安装包 → 安装 → 打开即自动拉起 Harness → 运行时就绪后直接是完整界面(没有"先装 Node 再装 dsh"这一步)。
- **日常**:菜单栏/托盘;窗口关掉不等于退出;更新在启动早期完成,不打断对话。
- **出事时**:看到的是"哪个插件 + 怎么办",而不是白屏;最坏进 Safe Mode,**会话还在**。
- **手机**:扫码 → 局域网直接进;异地则隧道 + 6 位口令,口令过期要重新在电脑上看。

## 4. 证据与边界

- **影响力**:GitHub API 2026-10-31:`stargazers_count=16,975`、`forks=586`、`open_issues=136`、`pushed_at=2026-10-30`。这是本 lever **唯一一个有万级 ★ 的样本**,也是"宿主侧被插件目录系统性漏掉"的最好证据(**它不在** `data/plugins`)。
- **机制证据**:README 全文(2026-10-31 抓取);上游接缝行号见 [`../_证据/01_桌面与终端-原始挖掘.md`](./_证据/01_桌面与终端-原始挖掘.md) §一。
- **口径警告**:★ 是 **GitHub API 时点值**,与仓库 `data/stars.json` 的 2026-08-19 快照**不同源**,不可互证,引用时必须带日期。
- **已核（2026-10-31）**：`docs/architecture.md` 写明 DSH_HOME 在 **Electron userData 下**（`harness/ DSH_HOME`，:42），启动时"**inspecting the web Profile**"（:29），正常状态是"the normal **web profile**"（:72）；Safe Mode 是**另一个只含官方 core bundle 的 profile**（:35）。所以它既不占 `desktop`，也不碰用户的 `~/.dsh`——**自带一套宿主数据根**。
- `[OPEN]` preview 通道与社区插件的兼容矩阵没有公开表,只有一句"may be incompatible"。

## 5. 借鉴食谱

| 要解决的问题 | 照它的做法 | 要改的地方 | 抄错的后果 |
|---|---|---|---|
| 装完就能用,别让用户先装 Node | 安装包内置/拉起运行时,首次启动只做"就绪探测" | 你要为每个目标平台各构建一次(原生依赖不可交叉) | 交叉打包 → 用户装完打不开,且错误发生在最不可诊断的时刻 |
| 更新别在对话中途把应用重启 | 检查 / 下载 / 安装三段分离,安装必须用户点按钮 | 加"跳过这一版"且不隐藏后续版本 | 静默更新 → 用户正在跑的长任务被杀,归因给整个产品 |
| 插件把应用弄崩了怎么办 | **Safe Mode**:隔离 profile,只挂官方 bundle,数据不动 | 需要一条**不依赖插件栈**的启动路径(命令行 flag) | 安全模式也挂在坏 profile 上 → 和坏应用一起起不来 |
| 失败要能指认 | 运行时 + 前端证据 → 指认具体插件 → 给升级/移除动作 | 证据采集要在启动早期就开着 | 只说"启动失败" → 用户只能全删重装 |
| 手机要能连,但不能把 Harness 暴露出去 | 随机回环端口 + 独立配对桥 + 短时口令 + 双隧道兜底 | 口令要能持久化,但必须显式选择 | 直接把 3080 转发到局域网/公网 → 整个会话对同网段开放 |
| 壳里能不能跑任意网页 | 无 Node + 上下文隔离 + 沙箱 + 拦非受信导航 | 外链要显式交系统浏览器 | 图省事给 renderer Node → 后面所有安全承诺失效 |

## 6. 失效条件与降级

- **平台**:Linux / Windows ARM64 不支持;每个产物只能在匹配 OS/架构上构建。
- **preview 通道**:与社区插件可能不兼容,官方自己不建议普通用户用。
- **Safe Mode 也不保证**:它隔离的是第三方插件,官方 core bundle 自身出问题就只剩 `--safe-mode` 与重装。
- **隧道**:Cloudflare 不可达地区靠 Pinggy 兜底,但 Pinggy 免费隧道约 60 分钟过期;口令过期后手机要回电脑重看。
- **签名成本**:macOS 公证 + Windows 代码签名是持续成本;没有签名就退回"右键打开 / SmartScreen"的体验(见 [`12_单文件桌面壳-windowos`](./12_单文件桌面壳-windowos.md))。

## 7. 开放问题

- [ ] `[OPEN]` Safe Mode 用的**那个 profile 叫什么名**、是否与正常 `web` profile 共享 `node_modules`——文档只写"separate profile"。
- [ ] `[OPEN]` Safe Mode 的"指认插件"用的是什么证据(启动日志?前端异常栈?)——README 只说 runtime + frontend evidence。
- [ ] `[OPEN]` 企业版与开源版的边界(README 提到 enterprise edition,未展开)。
- [ ] `[OPEN]` PPT 运行时(`16 templates / 192 layouts` + 内置 Python)是否算"宿主自带能力"的第三条腿——它已经不是界面,而是**随产品分发的能力包**。
