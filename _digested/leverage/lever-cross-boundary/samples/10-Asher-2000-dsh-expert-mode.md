# 10 · `Asher-2000/dsh-expert-mode`

> **一句话**:**不用写插件也能写协作**——团队结构全部落在静态 composition 的 17 条 `dsh-tool-subagent` 工具行里。
> **边界**:1 同进程父子(成员=配置出来的可续子代理) · **定位**:**反证型**旁支:路线成立,但在当前宿主上装不起来 · **证据级别**:`observed`(源码逐文件读过)
> **影响力**(2026-10-31 实时采样):**13★** / npm **374 次/月**;catalog 2026-08-19 快照 5★ → ×2.6
> **什么时候找它**:想用 preset/配置而不是运行时插件来做多 agent;或者想搞清楚 `persona` 为什么在这里会挂

> 导航:[样本索引](../03-sample-encyclopedia.md) · [域章程](../README.md) · [三笔税机制谱](../02-coordination-mechanisms.md) · [四道边界](../01-collab-topology.md)

## 设计思路

**它是本域唯一一条「不用插件写协作」的路线**——而它在当前宿主上装不起来。

它的形态确实成立:`preset.yml` 只有元数据,团队结构全部写在 `agent.cordis.yml` 的静态 composition 里——**17 条各自独立注册的 `@deepseek-ai/dsh-tool-subagent` 工具行**,每条带自己的 `toolName`(`expert_backend_dev`、`expert_devops`、`expert_database`、`expert_qa_engineer`、`expert_security`……)与 `persona` 段,`provider: spawn`、`backgroundMode: continuable`。**「成员」从运行时数据变成了配置**:不需要 roster 状态机、不需要 spawn/remove 工具,也没有官方 Team「Flat immutable roster」那条限制——因为它根本没有 roster。

**但它在本机 DSH `0.2.1-rc.3` 上有五处硬伤**,按严重程度排:

1. **`persona` 键已被宿主移除**。`dsh-tool-subagent/lib/index.js:355` 明文:`tool-subagent: persona is no longer supported; configure persona and tool plugins in an Agent Preset and select it with agentPreset (spawn only)`——加载即抛错。**17 行全部带 `persona`,所以 17 行全部挂载失败** `[DSH]`(我独立复核过这一行)。
2. **部署目录已失效**。`lib/index.js` 把 preset 拷进 `~/.dsh/.agent-presets/expert-mode/`,而官方 preset 编辑技能明写该目录 **「Nothing reads that directory any more.」** `[DSH]`(已复核);本机该目录也确实不存在。现行做法是在 bundle 里挂一行 `@deepseek-ai/dsh-agent-preset` 并给 `config.id/name/plugins`。
3. **任务板不是原子的**。`taskboard.py` 的 `claim` 实序是「读文件 → 校验 → 整体覆写」,全仓无 `flock`/`fcntl`/`O_EXCL`/`os.replace`;两个专家同时 claim 同一任务,双方都会通过迁移校验,后写覆盖先写。**「原子认领」是文档承诺,不是实现。**
4. **文件总线是黑板,不是 P2P**。总线只有「写文件/读文件」两个动作,**没有任何投递或唤醒机制**;子代理一个回合一把唤醒,不会被文件事件叫醒。所以 B 的邮箱里躺一百条消息,B 也不会有反应——**得由协调官再调一次 `expert_*` 把它唤起,它才会去 `read`**。`PROTOCOL.md` 自己承认这一点。而且第七项验收「端到端:真实双专家走总线接力」**至今未勾**。
5. **「省 28% token」无来源**。全仓 grep `28%` 只命中两行 README;唯一的度量文档测的是**数字符**(3230 字 → 930 字),且由协调官自评,结论写的是 71%。

**它对本域的真正价值是反证**:它把「成员=配置 + 可续子代理 + 文件黑板」这条路走到了能想到的最远处,然后撞在宿主的三个硬约束上——`persona` 已不可配、preset 目录已失效、子代理只能被父唤醒。**这三条正好解释了为什么生态最终都去写运行时插件。**

## 精确坐标

| 项 | 值 |
|---|---|
| **仓库** | [`Asher-2000/dsh-expert-mode`](https://github.com/Asher-2000/dsh-expert-mode) |
| **npm 包名** | `dsh-expert-mode` |
| **版本(本次读)** | `0.9.2` |
| **License** | MIT |
| **npm 近 30 天** | **374 次**(2026-09-30 ~ 10-29) |
| **安装** | `dsh plugin add dsh-expert-mode` |
| **接线方式** | `main: lib/index.js`;`dsh.bundle.patch` → **无 client 注入**(纯宿主侧) |
| **复现要点** | `apply()` 是空实现——**它不注册任何运行时能力**,只把 `agent.cordis.yml`/`preset.yml`/`.expert-mode/` 拷到 `~/.dsh/.agent-presets/expert-mode/`。所以要验证它,要看的是**preset 装没装上**,不是插件在不在 |

## 三笔税与代价

| 税 | 它的答案 | 代价 |
|---|---|---|
| 状态归属 | `~/.dsh/.agent-presets/expert-mode/` 下的文件总线 + taskboard JSON | 部署目录在当前宿主已失效;taskboard 非原子 |
| 冲突裁决 | 无。taskboard `claim` 是「读 → 校验 → 整份覆写」 | 两专家同时 claim 都会通过,后写覆盖先写 |
| 失败收敛 | 手动 `recover` + `stale > 300s` 直接回 `ready` | **无存活探测**,跑得久的专家会被当崩溃回滚 |

## 借用指南

### 可借鉴(直接抄)

1. **把「成员」写成配置行而不是运行时数据** —— 不需要 roster 状态机、不需要 spawn/remove 工具,也就没有官方 Team「Flat immutable roster」那条限制,因为它根本没有 roster。**如果你的团队是固定的,这是最省事的一条路。**
2. **每个成员一条独立的 `dsh-tool-subagent` 工具行** —— 17 个 `expert_*` 工具各自有 `toolName`、`persona`、`provider: spawn`、`backgroundMode: continuable`。**成员边界就是工具边界**,模型看得见、叫得出。
3. **`PROTOCOL.md` 这种「先写协议再写实现」的工艺** —— 它自己列了七项验收,并且**如实留着没勾完的那一项**。这种「把没做完的公开标出来」的习惯本身值得抄,比功能更值钱。

### 别照抄

- **别用 config 里的 `persona`** —— `dsh-tool-subagent/lib/index.js:355` 加载即抛错。合法的路径是把它作为 `startContinuable` 的**请求参数**传(见 [12 dsh-eteams](./12-2507483326-dsh-eteams.md))。
- 别把「文件总线」当消息队列 —— 它没有任何唤醒机制,B 的邮箱里躺一百条消息也不会有反应。
- 别信没有测量口径的百分比 —— 「省 28% token」在全仓只出现在两行 README 里。
