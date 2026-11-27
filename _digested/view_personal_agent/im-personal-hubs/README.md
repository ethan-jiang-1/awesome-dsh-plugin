# im-personal-hubs — 注册表实装个人管家(已入 `awesome-dsh-plugin`)

> 本子分类收纳**已经正式收录在 `awesome-dsh-plugin/data/plugins/`、可用 `dsh plugin add` 或 Release tarball 直接安装、且在真实下载量或安全工程深度上具备代表性的端到端个人 Agent 插件**。目前立 **2 张 ★★★ 源码卡**,另有 3 个已入库观察样本留在成员表。

## 定义

同时满足三条:

1. 已注册在 `data/plugins/*.yml`,是原生 DSH 插件而非独立桌面/手机宿主;
2. 提供面向单个主人的完整个人 Agent 闭环(长期记忆 + 角色/群聊或生活任务 + 显式权限/审批边界),不是纯通道桥接或桌宠皮肤;
3. 具备突出实证指标(npm 月下载过万,或注册表内同品类最高星且具源码级安全机制)。

## 成员

| 条目 | 实时星标(11-27) | npm 月下载 | 一句话 | 卡 |
|------|----------------:|----------:|--------|----|
| `roost-qq/dsh-roost` | **55★** | **22,012** | 官方 QQ 1:1 持久会话 + 6 级说话人动态工具剪枝 + 零外部 DB 三层夜间整理记忆 | [01-dsh-roost](01-dsh-roost.md) |
| `MJ-CJM/DSH-Bot`(`dsh-botgroup`) | **100★** | **1,854** | 注册表最高星多 Bot 工作台;三层 IFC 防私密记忆外泄 + 零模型群根 + TLA+ 规约 | [02-dsh-bot-mjcjm](02-dsh-bot-mjcjm.md) |
| `hanshanyike/dsh-yolo` | 52★ | — | 对话抽承诺→跨会话看板与离线补发提醒(暂不自动执行外部动作;观察中) | — |
| `Dely0/dsh-personal-workbench` | 47★ | — | 本地日历+层级任务+AI 提请完成人验收+可选 `@xmanrui/dsh-im` 提醒(观察中) | — |
| `Kevinwu901113/dsh-dot` | 19★ | — | 藏在 `fun` 类的 Dots/独立设备原型:自带安卓机+可选 microVM+`/qq owner` 围栏(观察中) | — |

## 读法

- **要立刻接进日常 IM(QQ)并防群友越权**:看 [01-dsh-roost](01-dsh-roost.md),重点核对它群聊 `confirmGate` 未验回复者身份的实测边界;
- **要在 DSH Web 内做多 Bot 个人工作台并抄信息流控制(IFC)**:看 [02-dsh-bot-mjcjm](02-dsh-bot-mjcjm.md),注意 npm 包名是 `dsh-botgroup` 且 `rc.2` 宿主锁死。

## 立卡条件

已入库条目须满足「高真实下载(npm 月下载 ≥10,000)」或「注册表内品类头部(≥100★)且具备源码级可借鉴安全/记忆机制」;其余 19–52★ 原型记入成员表持续跟踪,达标或出现协议复用后再补卡。
