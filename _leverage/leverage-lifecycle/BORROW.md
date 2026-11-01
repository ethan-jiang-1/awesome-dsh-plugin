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
| 定一条能同时写进 web 与 Desktop 的装法 | [`reference/REFERENCE.md`](./reference/REFERENCE.md) | 发 bundle，让用户在应用内装；CLI 只作 web 自动化 |
| 判断某个写法在另一面是否成立 | [`reference/SURFACES.md`](./reference/SURFACES.md) | 同一份 bundle、两个 profile 名；三处会静默失效 |
| 决定用哪种载体 | [`reference/CARRIERS.md`](./reference/CARRIERS.md) | 载体只从包清单或源码判，不从 README 判 |
| 发布前逐项自检 | [`practice/CHECKLIST.md`](./practice/CHECKLIST.md) | 十七项，每项都写"怎么核" |

## 2. 要做装

| 我要… | 去哪 | 一句话 |
|---|---|---|
| 装完能自证 | [`install/11`](./install/11_装后自证-cfbridge.md) | 五条可重跑命令；**别忘了 `files` 要带上它们** |
| 让安装器/市场认得出我 | [`install/12`](./install/12_让安装器认你-dsh-origin-plugin.md) | 入口工件决定"能装"，loader fiber 决定"活着" |
| 判"装上了没" | [`install/README.md`](./install/README.md) §2 | 三个成功分开核，只有进 roster 才算 |
| 离线/内网分发 | [`install/README.md`](./install/README.md) §2 | `.tgz` + `file:` 可用，来源签名自己保证 |

## 3. 要做起

| 我要… | 去哪 | 一句话 |
|---|---|---|
| 弄清重启/刷新/HMR 该写哪个词 | [`boot/README.md`](./boot/README.md) §2、§4 | CLI 装完宿主不知道；不重启就是没生效 |
| 自更新后确认新版接管 | [`boot/22`](./boot/22_重启取证-dsh-update-checker.md) | 结果文件 + 实例身份 + 端口探针，三件套 |
| 在 React 之前改首屏 | [`boot/21`](./boot/21_启动期注入-dsh-rhine-splash.md) | `index-inject`，append 不 prepend，双转义 |

## 4. 要做配

| 我要… | 去哪 | 一句话 |
|---|---|---|
| 决定偏好放哪一层 | [`config/README.md`](./config/README.md) §1 | 四个家；home 层能覆盖不能供货 |
| 做权限/名单类配置 | [`config/31`](./config/31_全禁状态-dsh-isolation-gate.md) | 读不到就拒绝；坏文件不覆盖 |

## 5. 要做首启

| 我要… | 去哪 | 一句话 |
|---|---|---|
| 第一次打开该给什么 | [`first-run/README.md`](./first-run/README.md) §1、§6 | 原生只有令牌门；六种载体自己选 |
| 没有浏览器卡片也要有首启 | [`first-run/41`](./first-run/41_自检即首启-dsh-skill-cockpit.md) | doctor 退出码 + 文档对账测试 |

## 6. 要研究 / 要查

| 我要… | 去哪 | 一句话 |
|---|---|---|
| 加一张样本卡 | [`research/RESEARCH.md`](./research/RESEARCH.md) | 影响力门 → 机制门 → S1–S5 |
| 查某个包为何没进卡 | [`research/BACKLOG.md`](./research/BACKLOG.md) | 15 排期 / 12 备选 / 8 降级 / 6 被拒 |

## 7. 三条"别抄"

1. **别抄"只发 CLI 一条命令"**——Desktop 用户装完看不到东西（[`reference/SURFACES.md`](./reference/SURFACES.md) §3）。
2. **别抄"自带安装器"**——除非你的产品根本不是插件；那是 shell，代价见 [`INSTALL`](./install/README.md) §3。
3. **别抄"文档写得好就当机制对"**——`[DOC]` 不等于 `[SRC-TARGET]`，本册两张卡都是靠源码翻的案（`install/11`、`install/12`）。
