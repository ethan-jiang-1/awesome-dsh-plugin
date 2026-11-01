---
title: "INSTALL · 阶段①：谁碰包管理器，什么算装上了"
domain: lifecycle
kind: playbook
positioning: "三条安装通道、三种“成功”状态、版本门与离线安装；以及 25 张产品卡里 24 张的装法通道分布。"
takeaway: "安装有三个独立的成功：pnpm 成功、依赖写入、成为 profile 层；只有第三个才让功能存在。"
read_when: "要定安装说明；或排查“装完了但功能不在”。"
status: living
updated: 2026-11-01
budget: 150
---
# 阶段① · 装

## 1. 原生怎么做

**三条通道，只有一条跨面。**

| 通道 | 谁执行 | profile 从哪来 |
|---|---|---|
| 应用内（侧栏 Plugins 页 / `plugin_manager` 工具） | 正在运行的宿主 | 当前 profile，**无参数** `[DSH]` |
| `dsh plugin --profile <p> <pnpm 参数>` | 命令行，转发给 pnpm | 显式指定；**首次使用时自动初始化** `[DSH]` |
| Electron carrier（程序化） | 桌面应用 | 只能它碰 `desktop` `[DSH]` |

- CLI 通道的实质是**在 profile 目录里跑 pnpm**，外加一步 `reconcile()` `[DSH]`（`dsh-plugin-manager/lib/types/operations.js:95-122`）。
- 首次使用会 `initProfile()`，用出厂模板的 bundle 列表；没有同名模板就用 `["@deepseek-ai/dsh-base"]` `[DSH]`（`operations.js:597`；`dsh-app-boot/lib/index.js:570`）。
- 兼容门在安装时判：不满足会列出 `incompatible` 并提示精确豁免命令 `dsh plugin --profile <p> allow-version <pkg>@<ver> --dsh-version <exact> --accept-risk` `[DSH]`（`lib/plugin-BiveYA7h.js:95`）。
- git 来源的包会跑 `prepare`，被 pnpm 拦下时需要往 profile 的 `pnpm-workspace.yaml` 加 `allowBuilds` `[DSH]`（`lib/plugin-BiveYA7h.js:97`）。
- **`file:` 相对路径按 profile 目录解析，不是当前工作目录**：`add file:./x.tgz` 会去找 `profiles/<p>/x.tgz`，报 `ERR_PNPM_LINKED_PKG_DIR_NOT_FOUND`；离线安装用绝对路径 `file:$PWD/x.tgz` `[RUN]`（E28 复现）。

## 2. 实测读到什么

| 实验 | 命令 | 结果 |
|---|---|---|
| E3 非 bundle 包 | `dsh plugin --profile plainp add file:…/probe-plain` | **exit 0**；依赖写入；`bundles` 仍只有 `dsh-base`；stderr：`declares no dsh.bundle — installed as a plain dependency, not a profile layer` |
| E4 bundle 包 | `dsh plugin --profile bundlep add file:…/probe-bundle` | exit 0；`bundles: [dsh-base, dsh-feas-probe]`；无警告 |
| E5 读回 | `dsh --profile bundlep --dump-config` | 行真的在，带层来源横幅 `# == dsh-feas-probe` |
| E13 离线 tarball | `dsh plugin --profile web add file:…/dsh-feas-client-0.0.1.tgz` | exit 0；依赖写的是 `file:…tgz`；roster 增一项 |
| E14 删除 | `dsh plugin --profile bundlep remove dsh-feas-probe` | exit 0；**roster 自动回收**回 `[dsh-base]`；依赖键被整个移除 |

**所以状态有三个，必须分开核**：

| 状态 | 怎么核 |
|---|---|
| ① pnpm 成功 | 退出码 0 + 输出里的 `+ <pkg>` |
| ② 依赖写入 | profile 的 `package.json.dependencies` |
| ③ 成为 profile 层 | profile 的 `package.json.dsh.profile.bundles` |

**只有 ③ 让功能存在。** 而 ①②成功、③失败时，退出码是 0。

## 3. 样本怎么偏离

25 张产品卡里 24 张写了装法（仅 `18_视觉资产` 未写）`[CARD]`。通道分布：

| 通道 | 样本 |
|---|---|
| `dsh plugin --profile <p> add`（主流） | 多数；含 `31`、`42`、`43`、`51`、`71`、`profile/11`–`17` |
| 应用内 Plugins 页 | `51`、`61`、`81`（**都额外注明 Desktop 走 App 内**） |
| `github:` 规格 | `81`、`profile/11`（均记录 `allowBuilds` 坑） |
| npx 包一层 | `71`（`npx -y @deepseek-ai/dsh plugin … add`；仍是 CLI，必须标“仅 web”） |
| 仓库脚本 | `12_厚工作台`（`bash scripts/install.sh`；只对克隆者成立，不是分发路径） |
| OS 安装器 / 裸 exe / dmg-msi | `shell/11`、`shell/12`、`shell/13`、`shell/14` |
| 装不上 | `shell/91`（peer 上界 `<0.2.0`，安装期 `incompatible-version`） |

**三类偏离的判读**：

- **仅 shell 允许**：自带安装器（那四张 shell 卡的产品本来就不是插件；插件不要）。
- **插件可用，但要自己保证来源**：`.tgz` / `file:`（内网、离线 `[RUN]`）。
- 两类都登记在 [`REFERENCE` §4](../reference/REFERENCE.md)。
- **允许但要写明**：只给 CLI 命令（含 `npx dsh plugin`）——必须标“仅 `dsh web`”；仓库脚本只对克隆者成立，不能当用户安装说明。
- **坑**：把 `--profile desktop` 写进说明（`profile/13` 卡头即如此，而 CLI 实测拒绝）；把非 bundle 包当插件发；版本范围只写在 README 里（manifest 既无 `engines.dsh` 也无 DSH peer，宿主没有门可判，坏版本也会装进来 `[DSH]`）。

**本册样本补充**（15 张阶段样本落地后）：

- [`11_装后自证-cfbridge`](./11_装后自证-cfbridge.md)：五条 npm scripts（validate/dump/repair 可作自证；install/uninstall 应走 `dsh plugin`），`files` 漏掉 `scripts/` → 全 404。
- [`12_让安装器认你-dsh-origin-plugin`](./12_让安装器认你-dsh-origin-plugin.md)：市场按“观察 > manifest > patch”判七态；carrier 用自己的 patch 行证明活着（1.73.6 已不需要自挂载空行）。
- [`13_三条安装路径与空安装器-dsh-free-models-hub`](./13_三条安装路径与空安装器-dsh-free-models-hub.md)：**反例**——三条路径依赖的脚本全不在包里；插件只应发 bundle。
- [`14_覆盖行的身份陷阱-dsh-tinyfish`](./14_覆盖行的身份陷阱-dsh-tinyfish.md)：覆盖宿主行只写 `id`；`name` 是断言不是重命名。

四条里有两条（11、13）是同一种**"说明与包体不一致"**——装阶段的结构性风险，不是个案（见 [`practice/TRAPS`](../practice/TRAPS.md) §14）；14 是 patch 语义、12 是分发入口，不是同一个错。

## 4. 三条判据

1. 包声明了 `dsh.bundle.patch`，且装完能在 `dsh --profile <p> --dump-config` 里看到自己的行。
2. 安装说明的那句"在 Plugins 页装"**不需要区分 web 与 Desktop**。
3. 给了 CLI 命令的，后面跟了"仅 `dsh web`"。

## 5. 失效与开放问题

- `[OPEN]` 应用内装在 Desktop 上的完整结果（`application`/`warnings`/`nextStep` 三字段的实际取值）。复核条件：一台官方 Desktop 机器，装一个我们自己的 bundle，读回结果。
- `[OPEN]` 换 registry 后的 `ERR_PNPM_TARBALL_URL_MISMATCH`（产品线卡里提过，本册未复现）。
- **已关**：`remove` 之后 roster 会被 `reconcile` 自动回收，无需手工清理 `[RUN]`（E14）。但"运行中删除"仍受 [`BOOT`](../boot/README.md) §1 的 HMR 限制。

## 样本

| 文件 | 一句话 |
|---|---|
| [`11_装后自证-cfbridge.md`](./11_装后自证-cfbridge.md) | 五条 npm scripts，`files` 漏了 `scripts/`；安装/卸载不该用脚本。 |
| [`12_让安装器认你-dsh-origin-plugin.md`](./12_让安装器认你-dsh-origin-plugin.md) | 市场七态与三级证据；carrier 的 patch 行就能证明活着。 |
| [`13_三条安装路径与空安装器-dsh-free-models-hub.md`](./13_三条安装路径与空安装器-dsh-free-models-hub.md) | 反例：三条安装路径，靠的脚本全不在包里。 |
| [`14_覆盖行的身份陷阱-dsh-tinyfish.md`](./14_覆盖行的身份陷阱-dsh-tinyfish.md) | 覆盖只写 id+config；`name` 是断言，失配会被整条跳过。 |
