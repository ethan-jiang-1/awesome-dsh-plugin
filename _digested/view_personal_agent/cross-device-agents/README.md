# cross-device-agents — 跨设备、口袋原生与常驻个人世界(仿 Meta Muse / 随身 DSH)

> 本子分类收纳**把个人 Agent 从桌面对话窗口解放到随身手机、跨设备网格或 24/7 自唤醒个人世界的 DSH 高影响项目**。目前立 **4 张 ★★★ 源码卡**,均在 2026-11-24~27 持续活跃且尚未收录于 `awesome-dsh-plugin`,覆盖从 33k★ 口袋真 DSH 到 3.7k★ Meta Muse 跨端复现的完整光谱。

## 定义

满足以下至少一条且以**单个主人的跨设备/全天候数字生活**为核心:

1. 将真实 `@deepseek-ai/dsh` 引擎装进移动设备(免 Root 免 Termux),直接操控手机真实 App 或加密远控桌面;
2. 以 DSH 作为跨设备网格节点(手机 + 电脑 + 中继),实现跨端派活与就近审批(Meta Muse 形态);
3. 在单主机内构建 24/7 自唤醒时间线、夜间自我复盘、IM 常驻与独立浏览器/桌面操控闭环。

## 成员

| 条目 | 实时星标(11-27) | 注册状态 / 分发 | 形态与一句话 | 卡 |
|------|----------------:|----------------|--------------|----|
| `nano-muse/nanoMuse` | **3,740★** | 未入库 / Release tarball + 安装包 | 明牌复刻 Meta Muse;桌面为 `dsh-nanomuse` Cordis 包 + HMAC Hands 审批 + 本地代理注 OAuth(注意中继非 E2EE) | [01-nanomuse](01-nanomuse.md) |
| `ccch1mneyyy/dsh-Go` | **33,066★** | 未入库 / APK 单版近 10 万下载 | 口袋真 DSH(266 补丁 + Ubuntu/Node/pnpm)+ Kotlin `SafetyGate` 硬拒 29 金融 App + SSH/`Noise_IK` 双远控 | [02-dsh-go](02-dsh-go.md) |
| `jackwener/DSH-Android` | **1,097★** | 未入库 / 110 MB APK | 双进程 Bionic Node 24 嵌入未分叉 `dsh@0.2.2-rc.5` + Shizuku 后台虚拟屏 + 18 份微信/小红书 `APP.md` | [03-dsh-android](03-dsh-android.md) |
| `chenkezhen480/dsh-world` | **454★** | 未入库 / npm `dsh-world@0.8.5` | 单依赖 `ws` 纯插件实现自唤醒时间线 + 无工具压缩 + 夜间日记 + Win32 后台/UAC 桌面(注意微信引擎非商用许可) | [04-dsh-world](04-dsh-world.md) |
| `DSH-APP/DSHA` | 3,738★ | 未入库 / APK | 免 Root 安卓 Ubuntu+proot DSH 运行时 + ADB 直控(与 `dsh-Go`/`DSH-Android` 同路线,留待下轮补源码审计) | — |
| `imsai-sh/fish-pocket` | 453★ | 未入库 / Swift iOS | 原生 iOS/iPadOS DSH 直连苹果日历/提醒/健康 + `iCTRL`(iOS 生态样本,留待下轮补源码审计) | — |

## 读法

- **比较手机端“怎么把真 DSH 装进口袋”的两条技术路线**:[02-dsh-go](02-dsh-go.md)(PRoot/Direct Ubuntu 完整生态 + 266 份补丁 + 外置 Kotlin `SafetyGate`) vs [03-dsh-android](03-dsh-android.md)(进程内 Bionic Node 24 + 22 份补丁 + Shizuku 后台虚拟屏与 18 份中文 App 指南);
- **看跨设备 Meta Muse 网格与安全取舍**:读 [01-nanomuse](01-nanomuse.md)(重点对比它的 HMAC 审批票据优势与非 E2EE 明文云同步代价);
- **看极简依赖的桌面 24/7 常驻范式**:读 [04-dsh-world](04-dsh-world.md)(重点看无工具压缩、双 `Esc` 急停与 Windows 强耦合/非商用微信引擎风险)。

## 立卡条件

本子分类只收影响面大(**≥400★** 且近期活跃)并具备鲜明架构代表性的跨设备/口袋/常驻个人 Agent 仓;其余同类高星仓(`DSHA`、`fish-pocket`)记入成员表待下轮补源码级核验。
