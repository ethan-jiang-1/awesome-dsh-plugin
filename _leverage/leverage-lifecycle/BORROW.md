---
title: "BORROW · 按需求路由：我要做 X，抄哪一条"
domain: lifecycle
kind: guide
positioning: "不按文件罗列、按你要干的事路由：每个需求给一条判据、一个样本、一句代价。"
read_when: "手上有一个具体需求，不想通读全册。"
status: living
updated: 2026-11-01
budget: 80
---
# 按需求路由

> 与另外三册同名同职责：**先找你的需求，再顺着去**。规则源仍是 [`00-map`](./00-map.md)，本文件只做路由。

## 1. 要发东西

| 我要… | 去哪 | 一句话 |
|---|---|---|
| 定一条能同时写进 web 与 Desktop 的装法 | [`reference/REFERENCE.md`](./reference/REFERENCE.md) | 发 bundle，让用户在应用内装；CLI 只作 web 自动化；先分清两种 Desktop |
| 判断某个写法在另一面是否成立 | [`reference/SURFACES.md`](./reference/SURFACES.md) | 同一份 bundle、两个 profile 名；三处会静默失效 |
| 决定用哪种载体 | [`reference/CARRIERS.md`](./reference/CARRIERS.md) | 载体只从包清单或源码判，不从 README 判 |
| 发布前逐项自检 | [`practice/CHECKLIST.md`](./practice/CHECKLIST.md) | 十八项，每项都写"怎么核" |

## 2. 要做装

| 我要… | 去哪 | 一句话 |
|---|---|---|
| 装完能自证 | [`install/11`](./install/11_装后自证-cfbridge.md) | 三条自检命令；安装走原生；**别忘了 `files`** |
| 判断市场/安装器认不认我 | [`install/12`](./install/12_让安装器认你-dsh-origin-plugin.md) | host 的 loader/roster 是事实源；市场只是消费者，别急着加空行 |
| 判断“多路径安装”为什么不要做 | [`install/13`](./install/13_三条安装路径与空安装器-dsh-free-models-hub.md) | 反例：另造分发；只留“产物随包”的教训 |
| 用 patch 覆盖宿主已有行 | [`install/14`](./install/14_覆盖行的身份陷阱-dsh-tinyfish.md) | 只写 `id` + `config`；`name` 是断言 |
| 判"装上了没" | [`install/README.md`](./install/README.md) §2 | 三个成功分开核，只有进 roster 才算 |
| 离线/内网分发 | [`install/README.md`](./install/README.md) §2 | `.tgz` + `file:` 可用，来源签名自己保证 |

## 3. 要做起

| 我要… | 去哪 | 一句话 |
|---|---|---|
| 弄清重启/刷新/HMR 该写哪个词 | [`boot/README.md`](./boot/README.md) §2、§4 | CLI 装完宿主不知道；不重启就是没生效 |
| 仅自更新应用：确认新版接管 | [`boot/22`](./boot/22_重启取证-dsh-update-checker.md) | 结果文件 + 实例身份 + 端口探针；插件优先用宿主 `restart-required` |
| 在 React 之前改首屏 | [`boot/21`](./boot/21_启动期注入-dsh-rhine-splash.md) | `index-inject`，append 不 prepend，双转义 |
| 插件里拉起外部进程 | [`boot/23`](./boot/23_外部进程生命周期-dsh-noema.md) | 六个默认值：懒起/保活/退避/去重 |
| 做自愈、修复、回滚 | [`boot/24`](./boot/24_事务式修复-dsh-doctor.md) | 修前检查点硬前置；救生链一律人工 |
| 装完还差一步才生效 | [`boot/25`](./boot/25_装完还要一步-dsh-context-guardian.md) | 显式命令 + 默认 dry-run |

## 4. 要做配

| 我要… | 去哪 | 一句话 |
|---|---|---|
| 决定偏好放哪一层 | [`config/README.md`](./config/README.md) §1 | 四个家；home 层能覆盖不能供货 |
| 做权限/名单类配置 | [`config/31`](./config/31_全禁状态-dsh-isolation-gate.md) | 读不到就拒绝；坏文件不覆盖 |
| 替换宿主默认能力 | [`config/32`](./config/32_三档接管-dsh-free-search.md) | 只接出厂默认；被重置后补一次 |
| 把多个包收成一个组合包 | [`config/33`](./config/33_换壳保-id-dfy-bundle.md) | 复用同 id；退役留给用户层 |

## 5. 要做首启

| 我要… | 去哪 | 一句话 |
|---|---|---|
| 第一次打开该给什么 | [`first-run/README.md`](./first-run/README.md) §1、§6 | 原生只有令牌门；七种启动原语自己选 |
| 没有浏览器卡片也要有首启 | [`first-run/41`](./first-run/41_自检即首启-dsh-skill-cockpit.md) | doctor 退出码 + 文档对账测试 |
| 没有界面时用命令验收 | [`first-run/42`](./first-run/42_命令即验收面-dsh-tool-guardian.md) | `input` 决定命令还是提问 |
| 预置工作区与自有会话 | [`first-run/43`](./first-run/43_预置工作区与自有会话-dsh-24pa.md) | 身份可推导；冲突换 id 不覆盖 |

## 6. 要研究 / 要查

| 我要… | 去哪 | 一句话 |
|---|---|---|
| 加一张样本卡 | [`research/RESEARCH.md`](./research/RESEARCH.md) | 影响力门 → 机制门 → S1–S5 |
| 查某个包为何没进卡 | [`research/BACKLOG.md`](./research/BACKLOG.md) | 16 排期（15 已成卡）/ 12 备选 / 8 降级 / 8 被拒（去重 42） |

## 7. 七条“别抄”

1. **别抄“只发 CLI 一条命令”**——保留名 Desktop 装进 `profiles/web` 看不到；社区桌面壳的 home 是私有的，`--profile web` 也写不到（[`reference/SURFACES.md`](./reference/SURFACES.md) §3）。
2. **别抄"自带安装器"**——除非你的产品根本不是插件；那是 shell，代价见 [`INSTALL`](./install/README.md) §3。
3. **别抄"文档写得好就当机制对"**——`[DOC]` 不等于 `[SRC-TARGET]`，本册两张卡都是靠源码翻的案（`install/11`、`install/12`）。
4. **别在插件里重启宿主**——应用内装已经给 `restart-required`，让用户重启；[`boot/22`](./boot/22_重启取证-dsh-update-checker.md) 只解决“非做不可时怎么取证”。
5. **别在运行时抢别人行的所有权**——默认安装期 patch；reclaim 只在必须与宿主开关共存时（[`config/32`](./config/32_三档接管-dsh-free-search.md)）。
6. **别写死用户 home / 用“无 peer”绕版本门**——路径从 `DSH_HOME`/settings 派生，门写 `engines.dsh`/peer（[`config/31`](./config/31_全禁状态-dsh-isolation-gate.md)）。
7. **别把第三方市场当 DSH 语义标准**——host 的 `pluginManager`/loader 才是事实源（[`install/12`](./install/12_让安装器认你-dsh-origin-plugin.md)）。
