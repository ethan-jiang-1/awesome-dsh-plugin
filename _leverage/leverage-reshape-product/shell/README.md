---
title: "shell · 自带宿主"
domain: reshape-product
kind: charter
positioning: "宿主侧宪章：换掉表层之后，首启/分发/降级为什么必须自己补，以及六条样本的四条路线。"
takeaway: "规律 A 的代价清单 + 宿主侧必抄 9 条。"
read_when: "要换表层做独立应用；或判断一个插件该不该分家。"
status: observed
updated: 2026-10-31
budget: 170
---
# shell · 自带宿主：它自己就是那个产品

> **标语**:*If you replace the surface, you own the product.* —— 换掉表层，首启、分发、降级就没人替你回答。
> **分工**:本 lever 收**换表层/自带宿主**的样本；能 `dsh plugin --profile <任意> add` 装进别人 profile 的客人在 [`plugin` 侧](../plugin/README.md)，**装进 web profile 在浏览器里成套出产品**的在 [`profile` 侧](../profile/README.md)。**先分 lever，再看编号。**
> **状态**:`observed`(机制已核) · **基线**:DSH `0.2.1-rc.3` · 名单 @ `efe602e7b` · **指标**:2026-10-31 重采
> **范围**:兼容 **DSH `0.2.x`**；`0.1.x` 的冻结 fork 只作反例。
> **借阅入口**:想判归属 → [§2 判据](#2-入桶判据) · 想抄 → [§4 必抄 9 条](#4-宿主侧必抄-9-条) · 想回源 → [§3 坐标](#3-六张卡)

---

## 1. 为什么要单开一个 lever

**因为改第 2 层，5/6/7 层就归你。** 这是本线的门（[`horizon`](../horizon.md)）里那条**规律 A**：

| 层 | 名字 | 插件侧 | 宿主侧 |
|---|---|---|---|
| 1 | 运行时 | 上游 | 上游 |
| 2 | **表层** | 在别人的界面上加东西 | **换掉它**（终端壳 / 桌面框 / 另一块屏） |
| 3 | 槽位 | 可加 | 自己定 |
| 4 | 身份 | 可加 | 自己定 |
| 5 | 默认值 | 宿主给 | **自己给**（规律 A） |
| 6 | 首启 | 宿主给 | **自己给**：第一次打开看到什么 |
| 7 | 分发 | 宿主给 | **自己给**：从哪装、怎么更新、坏了怎么回 |

**一句话**：插件侧抄的是**接缝**，宿主侧抄的是**整机**。混在一起读，最容易把 `14_终端即产品` 当成"又一个工作台"——它不是，它把 DSH 变成了另一个应用。

## 1.1 先看那条接缝:`desktop` 是被独占的名字

**这是本 lever 一切路线选择的前提。** 上游把 `desktop` 这个 profile 判给了官方 Electron 应用:

- `lib/bin.js:35-37`:`error: profile "desktop" is managed exclusively by the Electron application`
- `lib/plugin-BiveYA7h.js:10-12`:必须先打开官方桌面应用初始化,并**完全退出**才能 `dsh plugin --profile desktop`
- `lib/profile-boot-C14i-8IN.js:154`:`--from-default-profile` 只接受**出厂模板名**,自定义 profile 不能冒用

于是第三方宿主只有三条路,本 lever 的六张卡正好各占一条:

| 路线 | 做法 | 样本 |
|---|---|---|
| **复用 `web`** | 只补壳,profile 仍走 `web`(与用户自跑 `dsh web` 共数据) | `windowos` |
| **自有 DSH_HOME + `web`** | 自带一套数据根(如 Electron userData 下),正常只开 `web` profile | `DSH Desktop`(已核) |
| **换一块屏** | 用终端,profile 取自己的名字(`tui` / `dsh-tui`,不碰 `desktop`) | `SeekTTY`、`dsh-TUI` |
| **自带运行时 + 借 `desktop` 名** | 内置 Node + dsh;**绕开 CLI** 用内部 API 建 `desktop` profile——与官方应用同名同目录 | `tauriapp`(已实测) |

**抄之前先回答**:你打算用哪个 profile 名?这个名字会不会和官方桌面应用、或用户自己跑的 `dsh web` 撞车?

## 2. 入桶判据

**与 [`00-map` §8](../00-map.md) 是同一套三步判定。** 本桶 = 三步判定的 **Q1「非浏览器表层 / 自带运行时 / 安装包」** 分支。

- **主问**：用户必须启动终端、桌面应用或安装包，才能用到它？
- **门槛**：★ ≥ 100 或 npm 近 30 天 ≥ 1,000；机制例外每 lever ≤ 2 张（见 [`00-map` §7](../00-map.md)）。
- **边界**：能不能 `dsh plugin add` **不作数**（`14_终端即产品` / `15_终端工作区` 都能 add）；**插件半区不改变归属**（`12_单文件桌面壳` 的插件只是安装器）。

> **三张边界样本为什么不在这一桶**：`12_厚工作台` 没换表层（还是 `web` profile）、`51_分发与救生页` 的救生页是替宿主兜底、`61_多端与远程` 把 `dsh web` 当回环上游——它们都是**厚客人**。逐条理由见 [plugin 侧 §1.1](../plugin/README.md)。

> **怎么加卡**：过 00-map §11.1 快筛且门槛达标 → 确认它怎么补 5/6/7 层 → 按 00-map §5 建卡 → catalog 与本表各补一行 → `node _leverage/verify.mjs`。

## 3. 六张卡

按"接管了什么"排：**终端**（2）→ **桌面**（3）→ **反例**（1）。

| 路线 | 卡 | 一句话 | 抄什么 | ★ / npm 月下载（2026-10-31） |
|---|---|---|---|---|
| 终端 | [`终端即产品`](./14_终端即产品-dsh-TUI.md) | 换表层 + 自带四步首启，把 DSH 变成另一个应用 | 每档能力一条"退化为 Y"；hold 窗口；恢复不确定就报错；更新只看退出码 | 6,381 / 56,569 |
| 终端 | [`终端工作区`](./15_终端工作区-seektty.md) | 表层归我、状态归你；自带 profile 与 self-first 更新器 | 三档兼容 + 未知 fail closed；pnpm 布局适配只作用于自己发起的变更；原生 scrollback 模式 | 194 / 1,296 |
| 桌面 | [`桌面应用`](./11_桌面应用-dsh-desktop.md) | 签名安装包 + Safe Mode + 六小时更新检查，万级 ★ 的发行版 | Safe Mode（只挂官方 bundle）/ `--safe-mode`；更新先问再装；随机回环端口 + 独立配对桥 | 16,975 / — |
| 桌面 | [`单文件桌面壳`](./12_单文件桌面壳-windowos.md) | 4.5 MB 裸 exe：候选链 + 监护自愈 + 升级回滚 | 五跳候选链（每跳独立就绪窗口）；进程三态所有权；AUMID；熔断 | 26 / 1,168 |
| 桌面 | [`内置运行时`](./13_内置运行时-tauriapp.md) | 把 Node sidecar 与 dsh 依赖树打进安装包 | 连接级健康探测；自愈 3 次封顶 + 2 分钟重置；局部注入 chrome 不禁用 stock 布局 | 1 / — |
| 反例 | [`冻结 fork`](./91_冻结分叉-better-sidebar-N23.md) | 0.1.x 冻结 fork：改得太深就只能分家 | **反食谱**：peer 上界 = 死亡日期；只写下界 + CI 矩阵，或换接缝，别 fork | 0 / 1,350 |

**四条路线，一句话**：`dsh-TUI` 把插件做成应用；`SeekTTY` 只做表层、把状态留给宿主；`DSH Desktop` 把**运行时 + 安装包 + 恢复面**一起做；`windowos` / `tauriapp` 在"运行时从哪来"上各走一端（借用 vs 内置）。**反例**说明第四条路的失败形态：换了表层却把 peer 上界钉死。

**对着读**：`dsh-TUI` 与 `SeekTTY` 都是终端表层——前者在把自己从插件改成应用，后者明确"状态归 Harness"。**同一块屏，两种所有权。**

### 坐标（复现入口）

| 卡 | repo | npm 包名 | 目录条目 | 装法(0.2.x) | 已挖 | 未挖 |
|---|---|---|---|---|---|---|
| `终端即产品` | `ccch1mneyyy/dsh-TUI` | `@deepseek-harness-tui/dsh-tui`（全局 CLI） | `ccch1mneyyy__dsh-TUI.yml` (`ui`) | Windows 安装器；或 `npm i -g @deepseek-ai/dsh @deepseek-harness-tui/dsh-tui` 后 `dsh-tui`；**别用 git URL 装** | `../plugin/_证据/01_壳与工作台-原始挖掘.md` §三 | `compatibility.json`、52 条降级里未展开的协议细节 |
| `终端工作区` | `Hilbert-beinghappy/seektty` | `seektty`（+ 全局 `deepseek` launcher） | `Hilbert-beinghappy__seektty.yml` (`ui`) | `dsh plugin --profile tui add --config.enable-global-virtual-store=false seektty@1.3.0` 后 `dsh --profile tui` | `_证据/01_桌面与终端-原始挖掘.md` §二.4 | `0.2.1-rc.3` 实测；与 `dsh-TUI` 的 `tui` profile 共存 |
| `桌面应用` | `dataelement/dsh-desktop` | 无（桌面发行版） | **无**（口径外） | 官网 / Releases 下载 dmg·msi；**不走 `dsh plugin add`** | `_证据/01_桌面与终端-原始挖掘.md` §二.1 | 它用哪个 profile；Safe Mode 的插件指认证据 |
| `单文件桌面壳` | `RAFOLIE/dsh-desktop-windowos` | `dsh-desktop-plugin`（插件半区） | `RAFOLIE__dsh-desktop-windowos.yml` (`ui`) | 插件装（自动放 exe + 快捷方式）或直接下裸 exe | `_证据/01_桌面与终端-原始挖掘.md` §二.2 | 无登录态时的通知；双版本线回滚 |
| `内置运行时` | `hyperion2144/dsh-desktop-tauriapp` | `dsh-desktop-tauriapp`（插件半区） | `hyperion2144__dsh-desktop-tauriapp.yml` (`ui`) | 插件装；**应用本体**从 Releases 下 dmg/msi | `_证据/01_桌面与终端-原始挖掘.md` §二.3 | `desktop` profile 在当前上游能否创建；包体与内置版本 |
| `冻结 fork` | `All3nCN/dsh-better-sidebar-N23` | `@all3cn/dsh-better-sidebar-n23` | `All3nCN__dsh-better-sidebar-N23.yml` (`ui`) | **0.2.x 上装不上**（安装期 `incompatible-version`） | 目录条目 + upstream README 对照 | 同作者 `dsh-qa-suite-N23`；强行 `allow-version` 豁免后的实际表现 |

> **口径**：★ / issue 为 **GitHub API 2026-10-31** 实测；npm 下载为 **2026-09-30 ~ 10-29** 的近 30 天（含 CI 与镜像）。两者**不同源、不可互证**；`—` 表示该口径没有值（不是 0）。

## 4. 宿主侧必抄 9 条

**1–5 来自终端表层，6–8 来自桌面壳，9 是反例的唯一正确用法。** 这九条只在"你换了表层"时成立——插件侧抄它们会抄成过度设计。

**终端表层**

1. **每档能力一条"退化为 Y"**：终端不支持通知 → 响铃；没有图片协议 → 纯文本；最差档必须**不静默**。
2. **输入解析的 hold 窗口不被延长，超界原样重放**：别为了等一个可能的组合键，吞掉用户已经敲下的字符。
3. **恢复不确定就报错退出**，不要猜着往下恢复。
4. **更新只看退出码**，不看输出文本；首启向导要能在**没有网络**时走完。
5. **自带更新器要 self-first，一次一个组件**：先检查自己，再检查宿主；绝不跨未验证区间；失败不阻塞启动（`SeekTTY`）。

**桌面壳**

6. **总要有一条"进不去界面也能起来"的路**：`--safe-mode` / 命令行 flag / 只挂官方 bundle 的隔离 profile（`DSH Desktop`）。
7. **进程所有权显式建模**：附加 / 拉起 / 隐藏三态；退出只杀自己拉起的树；自愈要**封顶 + 冷却**（`windowos` / `tauriapp`）。
8. **健康判据贴近用户感知**：连接级探测（连不上才算异常），不是"进程还在"；依赖不一致**只提示、不自动重建**（`tauriapp`）。

**反例**

9. **peer 上界 = 死亡日期**：只写下界 + CI 矩阵，或换接缝；真要 fork，就承认分家，别假装还能装回上游（`91_冻结分叉`）。

## 5. 已补与待补

**2026-10-31 这一轮补了 4 张**（桌面 3 + 终端 1），桶从 2 张到 6 张。补法：从注册表 `data/plugins` 按 `ui`/`remote` + 描述里的 "desktop / shell / Tauri / Electron / installer / standalone" 召回，再逐仓读 README，用 §2 的 H1–H3 过筛。

- [x] **桌面壳**：`dataelement/dsh-desktop`（16,975★，口径外）、`RAFOLIE/dsh-desktop-windowos`（npm 月 1,168）、`hyperion2144/dsh-desktop-tauriapp`（1★，机制例外）
- [x] **终端表层第二张**：`Hilbert-beinghappy/seektty`（194★ / npm 月 1,296）
- [ ] **官方桌面客户端**（`DeepSeek Harness Desktop`）：它是上游还是样本？`desktop` profile 由它独占（`lib/bin.js:36`）——本 lever 目前只把它当**接缝**，未成卡
- [ ] **手机 App 侧**：`dsh-mobile` 的 App、`tauriapp` 的 `mobile/`、`DSH Desktop` 的手机桥——"客户端"与"另一个宿主"的边界还没定
- [ ] **Linux 桌面壳**：本轮的三个桌面样本都只覆盖 macOS/Windows（`windowos` 甚至只有 Windows）
- [x] **`dsh-pocket`**（10,411 下载 / 179★）**已判：不是宿主**。它一个包 + 设置页 + 扫码，把电脑上的**同一个界面**投到手机（自带隧道/配对），属于"另一块屏的传输"，归 [`plugin` 侧](../plugin/README.md) 的 `61_多端与远程` 邻域，不进本 lever

**搜索口径**：`category` 是 `ui`/`remote`，且描述里出现 **desktop / shell / Tauri / Electron / installer / standalone / launcher / 免安装**；再按 §2 的 H1–H3 过一遍。只加能力的不成卡（见 [`horizon`](../../leverage/horizon.md)）。

**搜索口径**：`category` 是 `ui`/`remote` 但**需要全局安装、独立启动命令、或声明 fork** 的条目；再按 §2 的 H1–H3 过一遍。只加能力的不成卡（见 [`horizon`](../../leverage/horizon.md)）。

## 6. 与 plugin 侧的取舍

| | [`plugin` 侧](../plugin/README.md) | 本 lever |
|---|---|---|
| 你得到 | 装进任何产品的**零件**，宿主替你兜首启/分发/降级 | **整个产品**，包括第一次打开、装坏了怎么回 |
| 你付出 | 受上游接缝约束，能改的只有槽位与内容 | 首启、分发、降级、救生页**全归你**（规律 A） |
| 抄错的样子 | 硬依赖一个不存在的服务 → 白屏 | 换了表层没补 5/6/7 → 首启即崩，用户归因给整个产品 |

## 7. 边界

**收**：换表层 / 自带宿主 / 自带装-坏-回链路，且有可复核的影响力证据。

**不收**：能 `dsh plugin add` 装进别人 profile 的插件（去 [`plugin` 侧](../plugin/README.md)）；只加能力的工具类插件。

**共享文件只读**：`00-map.md`、`horizon.md`、`leverage/README.md`、`data/` 由别的会话维护，本 lever 只调用、不写。
