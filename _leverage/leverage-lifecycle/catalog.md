---
title: "catalog · 第四册全量清单"
domain: lifecycle
kind: index
positioning: "本册全部文件的 kind、定位与阅读时机；新增文件必须在这里补一行。"
read_when: "想一次看全本册；或按关键词找某条判据。"
status: living
updated: 2026-11-01
budget: 90
---
# 全量清单

> **入口顺序**：[README](./README.md)（结论与读法）→ [REFERENCE](./reference/REFERENCE.md)（那条路）→ 四个阶段篇 → 五个阶段目录里的样本。本文件是**全量清单**，`verify.mjs` 会双向核对：**这里少一行或多一行都会失败**。

## 1. 骨架

| 文件 | kind | 定位 | 何时读 |
|---|---|---|---|
| [`README.md`](./README.md) | index | 第四册入口：七条硬结论、四阶段路由、证据口径与实测环境。 | 第一次进本册。 |
| [`00-map.md`](./00-map.md) | charter | 规则源：定位与边界、目录、命名、两道人选门、标签、不变量。 | 要新增/改名文件；或怀疑口径冲突。 |
| [`reference/REFERENCE.md`](./reference/REFERENCE.md) | playbook | 被认可的那一条路：发 bundle、应用内装、CLI 只作 web 自动化。 | 要定一个产品的分发方式。 |
| [`reference/SURFACES.md`](./reference/SURFACES.md) | charter | web 与 Desktop 的同一性与三道闸，含三处静默失效。 | 判断某个写法在另一面是否成立。 |
| [`reference/CARRIERS.md`](./reference/CARRIERS.md) | charter | 九类载体的判定依据与矩阵；分类只从包清单/源码来。 | 要判断一个插件属于哪类。 |
| [`install/README.md`](./install/README.md) | playbook | 阶段①：三条通道、三种“成功”、版本门、离线 tarball。 | 写安装说明；排查“装了但不在”。 |
| [`boot/README.md`](./boot/README.md) | playbook | 阶段②：profile 四件套、补丁叠加序、失败三级、重启/刷新/HMR。 | 写“装完重启”这类提示。 |
| [`config/README.md`](./config/README.md) | playbook | 阶段③：四个配置的家、home 层能覆盖不能供货。 | 决定偏好放哪一层。 |
| [`first-run/README.md`](./first-run/README.md) | playbook | 阶段④：令牌门、首启账本、启动体验的六种载体。 | 设计首次体验。 |
| [`practice/TRAPS.md`](./practice/TRAPS.md) | guide | 十二条照抄就中招，每条带反例。 | 发布前自查；排查怪状态。 |
| [`practice/CHECKLIST.md`](./practice/CHECKLIST.md) | guide | 十七项发布前检查，每项写“怎么核”。 | 要把 bundle 发出去之前。 |
| [`research/RESEARCH.md`](./research/RESEARCH.md) | guide | 影响力漏斗、三轴分类、S1–S5 流水线、质量门与结论归属。 | 要新增样本；或复核别人的挖掘。 |
| [`research/BACKLOG.md`](./research/BACKLOG.md) | index | 42 个过门 bundle 的分诊结果：15 张排期、12 备选、8 条降级、6 个被拒。 | 要补样本；或问某包为何没进卡。 |
| [`BORROW.md`](./BORROW.md) | guide | 按需求路由：我要做 X 抄哪一条；含三条“别抄”。 | 手上有具体需求，不想通读。 |
| [`catalog.md`](./catalog.md) | index | 全量文件清单（手工维护）。 | 想一次看全。 |

## 2. 样本（按阶段目录）

| 文件 | kind | 定位 | 何时读 |
|---|---|---|---|
| [`install/11_装后自证-cfbridge.md`](./install/11_装后自证-cfbridge.md) | sample | 装后自证五件套，以及 `files` 白名单如何把它们全部漏掉。 | 要发带安装/校验脚本的包。 |
| [`install/12_让安装器认你-dsh-origin-plugin.md`](./install/12_让安装器认你-dsh-origin-plugin.md) | sample | 两个隐形判定：入口工件决定能否装，loader fiber 决定市场是否认你活着。 | 要发以 patch 为主、自己没有运行时的 bundle。 |
| [`install/13_三条安装路径与空安装器-dsh-free-models-hub.md`](./install/13_三条安装路径与空安装器-dsh-free-models-hub.md) | sample | 按用户类型分三条安装路径，而三条依赖的脚本都不在包里。 | 要写面向小白的多路径安装说明。 |
| [`install/14_覆盖行的身份陷阱-dsh-tinyfish.md`](./install/14_覆盖行的身份陷阱-dsh-tinyfish.md) | sample | 覆盖宿主行只写 `id`+`config`；`name` 是断言，写别人包名=冒名。 | 要用 patch 覆盖宿主已有行。 |
| [`boot/21_启动期注入-dsh-rhine-splash.md`](./boot/21_启动期注入-dsh-rhine-splash.md) | sample | 用 `index-inject` 在 React 之前改首屏；顺序、转义、开屏频率全归自己。 | 要做品牌首屏、主题注入或开屏动画。 |
| [`boot/22_重启取证-dsh-update-checker.md`](./boot/22_重启取证-dsh-update-checker.md) | sample | 自重启后如何证明新版接管：结果文件 + 实例身份 + 端口探针。 | 要做自更新/自重启；或排查“重启后还是旧版”。 |
| [`boot/23_外部进程生命周期-dsh-noema.md`](./boot/23_外部进程生命周期-dsh-noema.md) | sample | 懒起/保活/退避/并发去重四件事，靠六个默认值表达。 | 插件里要拉起外部进程。 |
| [`boot/24_事务式修复-dsh-doctor.md`](./boot/24_事务式修复-dsh-doctor.md) | sample | 修复前检查点硬前置、健康检查点尽力而为、救生链一律降级人工。 | 要写自愈/修复/一键排障。 |
| [`boot/25_装完还要一步-dsh-context-guardian.md`](./boot/25_装完还要一步-dsh-context-guardian.md) | sample | 生效做成显式一步且默认 dry-run；三条命令做会话内验收。 | 装完还需要额外一步才生效。 |
| [`config/31_全禁状态-dsh-isolation-gate.md`](./config/31_全禁状态-dsh-isolation-gate.md) | sample | 状态文件四态读取 + 一律 deny + 坏文件不覆盖；含“符号表失效”的兜底。 | 要做权限/名单/白名单类配置。 |
| [`config/32_三档接管-dsh-free-search.md`](./config/32_三档接管-dsh-free-search.md) | sample | 只接出厂默认、显式选择让路、被重置后补一次；含 apply 重入的日志去重。 | 要让插件替换宿主默认能力。 |
| [`config/33_换壳保-id-dfy-bundle.md`](./config/33_换壳保-id-dfy-bundle.md) | sample | 换包装时复用同 id 保配置；退役旧包留给用户层，不越权。 | 要把多个独立包收成一个组合包。 |
| [`first-run/41_自检即首启-dsh-skill-cockpit.md`](./first-run/41_自检即首启-dsh-skill-cockpit.md) | sample | 用 doctor 退出码当首启验收面，并用测试锁住检查项与排障文档。 | 产品没有浏览器卡片；或检查项越加越多。 |
| [`first-run/42_命令即验收面-dsh-tool-guardian.md`](./first-run/42_命令即验收面-dsh-tool-guardian.md) | sample | 会话内命令当唯一验收面；`input` 决定命令是给人还是给模型。 | 产品没有浏览器卡片；或要设计自检命令。 |
| [`first-run/43_预置工作区与自有会话-dsh-24pa.md`](./first-run/43_预置工作区与自有会话-dsh-24pa.md) | sample | boot 时建工作区 + 两个可推导的会话；预设冲突换 id 不覆盖。 | 要让产品打开就落在自己的工作面。 |

## 3. 证据

| 文件 | kind | 定位 | 何时读 |
|---|---|---|---|
| [`_证据/01_DSH-源码定位.md`](./_证据/01_DSH-源码定位.md) | evidence | 全部 `[DSH]` 断言的包 + 文件:行号 + 保证了什么。 | 复核某条 `[DSH]`。 |
| [`_证据/02_隔离实测记录.md`](./_证据/02_隔离实测记录.md) | evidence | E0–E19 的命令、输出与复现步骤。 | 复核某条 `[RUN]`。 |
| [`install/_证据/11_装后自证-cfbridge-源码复核.md`](./install/_证据/11_装后自证-cfbridge-源码复核.md) | evidence | cfbridge 0.13.2 的固定版本、tarball 摘要、符号命中与负向事实。 | 复核 `install/11`。 |
| [`install/_证据/12_让安装器认你-dsh-origin-plugin-源码复核.md`](./install/_证据/12_让安装器认你-dsh-origin-plugin-源码复核.md) | evidence | origin-plugin 2.7.3 的固定版本、自挂载行与 apply 返回值的原始定位。 | 复核 `install/12`。 |
| [`install/_证据/13_三条安装路径与空安装器-dsh-free-models-hub-源码复核.md`](./install/_证据/13_三条安装路径与空安装器-dsh-free-models-hub-源码复核.md) | evidence | free-models-hub 0.3.1 的七文件全量清单与 README 三条路径对照。 | 复核 `install/13`。 |
| [`install/_证据/14_覆盖行的身份陷阱-dsh-tinyfish-源码复核.md`](./install/_证据/14_覆盖行的身份陷阱-dsh-tinyfish-源码复核.md) | evidence | tinyfish 0.13.0 的覆盖行原文与“name 是断言”注释。 | 复核 `install/14`。 |
| [`boot/_证据/21_启动期注入-dsh-rhine-splash-源码复核.md`](./boot/_证据/21_启动期注入-dsh-rhine-splash-源码复核.md) | evidence | rhine-splash 0.2.8 的 index-inject 注册点、转义函数与配置声明。 | 复核 `boot/21`。 |
| [`boot/_证据/22_重启取证-dsh-update-checker-源码复核.md`](./boot/_证据/22_重启取证-dsh-update-checker-源码复核.md) | evidence | update-checker 1.7.3（无 gitHead）的三件重启证据原始定位。 | 复核 `boot/22`。 |
| [`boot/_证据/23_外部进程生命周期-dsh-noema-源码复核.md`](./boot/_证据/23_外部进程生命周期-dsh-noema-源码复核.md) | evidence | noema 0.1.0-rc.6 的六个默认值与保活/空闲/去重原文。 | 复核 `boot/23`。 |
| [`boot/_证据/24_事务式修复-dsh-doctor-源码复核.md`](./boot/_证据/24_事务式修复-dsh-doctor-源码复核.md) | evidence | dsh-doctor 0.4.3 的检查点两级严格度、受保护集合与回滚命令。 | 复核 `boot/24`。 |
| [`boot/_证据/25_装完还要一步-dsh-context-guardian-源码复核.md`](./boot/_证据/25_装完还要一步-dsh-context-guardian-源码复核.md) | evidence | context-guardian 0.3.0-beta.1 的 dry-run 开关与三条命令注册。 | 复核 `boot/25`。 |
| [`config/_证据/31_全禁状态-dsh-isolation-gate-源码复核.md`](./config/_证据/31_全禁状态-dsh-isolation-gate-源码复核.md) | evidence | isolation-gate 1.13.7 的状态读取五分支与判定开关原文。 | 复核 `config/31`。 |
| [`config/_证据/32_三档接管-dsh-free-search-源码复核.md`](./config/_证据/32_三档接管-dsh-free-search-源码复核.md) | evidence | free-search 0.9.26 的接管条件、reclaim 与日志去重原文。 | 复核 `config/32`。 |
| [`config/_证据/33_换壳保-id-dfy-bundle-源码复核.md`](./config/_证据/33_换壳保-id-dfy-bundle-源码复核.md) | evidence | dfy-bundle 0.1.3 的八文件清单、同 id patch 与 README 迁移段。 | 复核 `config/33`。 |
| [`first-run/_证据/41_自检即首启-dsh-skill-cockpit-源码复核.md`](./first-run/_证据/41_自检即首启-dsh-skill-cockpit-源码复核.md) | evidence | skill-cockpit 1.5.1 的 doctor 退出码、四值状态与文档对账测试。 | 复核 `first-run/41`。 |
| [`first-run/_证据/42_命令即验收面-dsh-tool-guardian-源码复核.md`](./first-run/_证据/42_命令即验收面-dsh-tool-guardian-源码复核.md) | evidence | tool-guardian 0.9.1-beta.1 的命令注册、input 路由与未就绪两态。 | 复核 `first-run/42`。 |
| [`first-run/_证据/43_预置工作区与自有会话-dsh-24pa-源码复核.md`](./first-run/_证据/43_预置工作区与自有会话-dsh-24pa-源码复核.md) | evidence | 24pa 0.2.1-rc.5.1 的工作区创建、会话身份与冲突换 id 原文。 | 复核 `first-run/43`。 |

## 4. 速查：四阶段一句话

| 阶段 | 一句话 |
|---|---|
| 装 | 三个成功要分开核，只有“进 roster”才算装上。 |
| 起 | CLI 装完宿主不知道；不重启就是没生效。 |
| 配 | 选哪一层等于选覆盖面；home 层能覆盖不能供货。 |
| 首启 | 原生只给令牌门，第一次看到什么由产品自己决定。 |
