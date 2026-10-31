# 09 · `IKEASven69/dsh-takeover`

> **一句话**:`handoff: 1` 协议的拉/推/取闭环,`~/.handoff/` 是总线,跨机靠同步盘——**插件零网络**。
> **边界**:3 跨进程/跨机 · **过了哪些门**:F + G · **证据级别**:`observed`(源码逐文件读过)
> **影响力**(2026-10-31 实时采样):**0★**;F 探针 `接力` = **7/7924**
> **什么时候找它**:要跨机但**不想写任何协议**,且能接受没有实时性

> 导航:[样本索引](../03-sample-encyclopedia.md) · [域章程](../README.md) · [三笔税机制谱](../02-coordination-mechanisms.md) · [四道边界](../01-collab-topology.md)

## 设计思路

**一句话设计思路**:`handoff: 1` 协议的「拉/推/取」闭环,`~/.handoff/` 是总线,跨机靠 `HANDOFF_HOME` 指同步盘,**插件零网络**。

**它为什么可行**:协作状态被做成**可序列化的自包含单元** ——一张会话卡片(含六段上下文骨架、随卡补丁 `<id>.patch`、四态证据账本)。

**「恰好一次」的实现完全靠文件系统原语**,这是本域最漂亮的一段:顺序 = `assertSafeId` → 尺寸闸(8MiB) → `open(<id>.claim,'wx')` 独占认领(EEXIST 即「另一进程取件中」) → render → rename 到 archived → finally 删 claim。同名归档内容相同 = 幂等吸收,不同 = 先写 `.conflict-HHMMSS[-n].md` 再 rename。认领残留 60s 后 `sweepClaims` 清。CHANGELOG 明说这套来自「Windows 并发 rename 双成功」的真实缺陷。

**四态账本** `CURRENT_OBSERVED` / `HISTORY_REPORTED` / `MISMATCH` / `UNAVAILABLE` 是它的证据模型——**接力过来的上下文永远标注“这是报告,不是观察”**,原文才按需分页拉取。

**代价**:没有回执、没有实时性,冲突语义由同步盘决定;密钥与卡片同盘(威胁模型 T1-T6 里自列)。

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | `~/.handoff/` 目录即总线;跨机把 `HANDOFF_HOME` 指到同步盘 | 零回执,冲突语义由同步盘决定 |
| 冲突裁决 | `open(<id>.claim,'wx')` 独占认领 + 内容相同去重 + `.conflict-HHMMSS[-n].md` | 认领残留 60s 后才清扫 |
| 失败收敛 | 消费即弃卡片 + 四态证据账本 + 投递失败退回复制指令 | 没有实时性;密钥与卡片同盘 |

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`IKEASven69/dsh-takeover`](https://github.com/IKEASven69/dsh-takeover) |
| **npm 包名** | `dsh-takeover` |
| **版本(本次读)** | `0.4.3` |
| **License** | MIT |
| **npm 状态** | **未发布到公共 registry**(404)——0★ + 未发布,是它几乎无人使用的最直接解释 |
| **安装** | `dsh plugin --profile web add github:IKEASven69/dsh-takeover`(README:78) |
| **接线方式** | `main: ./lib/index.js`;依赖里 `@deepseek-ai/*` 走 registry,`@agent-handoff/*` 走 **`file:` 链接**(README:123) |
| **复现要点** | 跨机靠同步盘时,要把 `HANDOFF_HOME` 指向同步目录;否则只用本机 `~/.handoff/` |

## 借用指南

### 可借鉴(直接抄)

1. **恰好一次用文件系统原语实现**:`assertSafeId` → 8MiB 尺寸闸 → `open(<id>.claim,'wx')` 独占认领(EEXIST = 另一进程取件中) → render → rename 归档 → `finally` 删认领;同名归档内容相同 = 幂等吸收,不同 = 先写 `.conflict-HHMMSS[-n].md`;认领残留 60s 后清扫。**单机或同步盘场景下,`O_EXCL` 比任何自研锁都可靠,且零基础设施。** 这套顺序是从「Windows 并发 rename 双成功」这个真实缺陷里长出来的。
2. **四态证据账本** `CURRENT_OBSERVED / HISTORY_REPORTED / MISMATCH / UNAVAILABLE`——接力过来的上下文**永远标注「这是报告,不是观察」**,原文按需分页拉。这是本域最该被抄走的一个数据结构。
3. **补丁随卡走** + `git apply --check` → `apply` → `-3` 三级指引;>512KB 直接拒,未跟踪文件只给名字(≤20)。
4. **上下文摘要优先**:首末条用户消息各 400、最近 3 轮各 300、top 15 文件、≤10 条命令。
5. **投递失败把同一份指令复制到剪贴板 + 原因横幅** ——把「人」当成可靠后备,而不是报错了事。

### 别照抄

- 零回执却当可靠通道;密钥与卡片同盘;把同步盘的冲突语义当成你的冲突语义。
