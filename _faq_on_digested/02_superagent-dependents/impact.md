# 影响面 · 一个大上游,一圈小分叉,四种杠杆

> 这一页不重复 [answer.md](answer.md) 的计数,只回答"这套依赖结构里谁有杠杆、什么被复用、什么会坏、值得盯什么"。数据同 answer:注册表 `main@8f1a1800e`(2026-11-25),上游 `deepseek-ai/dsh-superagent-prototype@8c32a9dc`,星标实时。

## 先纠正一个直觉:影响力 ≠ 星标

- 上游 **24,565★ / 3,081 forks** 是 DeepSeek Harness 团队的机构背书;它**不在注册表**里,也没有 npm 包(=`private: true`)。把它当"社区采用"读会高估一个数量级。
- 9 个真依赖里,只有 HiSeax 过百星(**138**);其余 ≤11,一半是 0★。
- 注册表里星标最高的两个社区 superagent 条目——MYCF711(52★)与 LittleChenLiya(22★)——**都不是依赖者**:前者是设计衍生(D3),后者只是同名(D0)。
- **星标不是唯一量纲**:03-desktop 只有 1★,但 npm 月下载 **1,753**(周 380);09-power 0★,Release tgz 743+42 次下载;02-local 11★,却有一条真实用户 issue(#1,报告 worker 环境遮蔽宿主 `gh`)。这些说明"被安装/被试用"和"被讨论"是两条线,而"被依赖"又是第三条线——三者不能互相替代。
- 所以这个生态的真实形状是:**一个机构原型 + 一圈补部署面的小分叉**。分叉的影响力不在"改设计",而在"让它在某种环境里真的能跑"。

## 影响面分三层

| 层 | 谁在控制 | 被复用什么 | 断的时候谁疼 |
|----|----------|------------|--------------|
| **领域模型** | 上游 | Source / Trigger / Thread / Policy / Mandate / Ticket / Assignment / Subscription 这套语义 | 所有 D1 分叉:模型一改,整树 diff |
| **运行契约** | 上游的 `stateDir`、`orchestrator.sqlite`、profile/`bridge.js` | `orchestrator.sqlite` 的表与字段、profile 的 `config.stateDir`、`bridge.js` 的握手 | D2 插件(trace / wechat-source / power):静默读空或起不来 |
| **用户界面** | 分叉与 D2 各自 | 侧栏看板、grill 卡、IM 渠道、面板 | 最终用户:升级宿主后"看板还在、数据不对" |

关键点:**只有第一层有文档**(上游 `docs/001-008`),第二层是**事实契约**——`orchestrator.sqlite` 不是公开 API,trace 却把它当数据库读;`bridge.js` 不是协议规范,power 却按它对接。第三层最靠近用户,也最不可复现。

## 四种杠杆

1. **上游:定义语义,但不发版。** 没有 npm、没有版本化 API、没有 changelog 契约;它一改,分叉只能整树 diff。上游的"影响力"是**定义权**,不是分发权——这解释了为什么 9 个依赖者全都自己扛一份代码。
2. **D1 分叉:控制部署面。** Windows(HiSeax)、本机工作区(local)、桌面 bundle(desktop)、DSH 版本适配(adapt)、多仓+IM(ctrl439)、A2A 壳(nelson)。它们真正卖的是"上游不覆盖的运行环境",不是新设计。代价是 92 个上游文件全部要跟。
3. **D2 插件:控制观测与生命周期。** trace 把黑箱变白盒,wechat-source 把微信变 Source,power 把独立 profile 变成输入栏一个开关。它们最轻,也最脆——吃的是**内部形状**,不是接口。
4. **D3 衍生:控制叙事。** mycf711 把 Router–Worker 降成"会话级唤醒",nattocb 做成持久工单控制台,imperial 做成本机"丞相府"。它们影响"人们怎么理解 super-agent",但不产生代码复用。

## 分叉经济学

- **成本**:一份 fork 要背 92 个源文件 / 约 1.6 万行(HiSeax 实测 114 文件 / 16,078 行,含新增),外加 23 个 peer 的宿主耦合;上游没有 npm 包,不能 `depend on` 一个版本,只能整树搬。
- **同步**:所有 D1 仓库都没有声明 upstream remote 或 sync 脚本(读到的 README/CHANGELOG 未提);上游一改,靠人工 diff。
- **血缘**:HiSeax 的 Windows 基线 `vHao11/dsh-windows-superagent@windows-adapt` 在 2026-11-25 已 404——**分叉链的中间层会消失**,只剩末端与上游的代码重叠可核。
- **许可**:上游 MIT,D1 分叉都保留 MIT;但中间层的版权声明是否完整,末端仓库无法自证。

## 风险与观察点(按可信度排序)

1. **内部 DB 当 API**:trace 读 `orchestrator.sqlite`;上游改表/改字段,trace 会"页面正常、数据为空"或直接报错。README 已把"取不到 stateDir 就说明原因"写进去,说明作者知道这是事实契约。
2. **profile/bridge 私约**:power 要求双方同一 `homePath`/`profileName`/密钥文件并注册 `bridge.js`;这类约定没有版本号,宿主或上游一改就断,且断在启动前。
3. **fork 同步债**:92 文件全改的 fork,一旦上游大改,合并成本接近重做;HiSeax 的 README 把"上游测试在 Windows 上环境受限"也写明了。
4. **权限边界**:上游 worker 以 OS 用户执行命令、无审批;HiSeax 明确说 Windows 上 `blockedCommands` 对 worker 不生效。这是"能不能用"的问题,不是"好不好用"。
5. **名字通胀**:注册表 16 个名字命中里 4 个完全无关(D0)。如果只看名字做生态统计,依赖数会虚高 44%;这也是 [answer.md](answer.md) 坚持分层的理由。

## 如果要做选择

| 你想要的 | 看哪条线 | 代价 |
|----------|----------|------|
| Windows 上跑起来 + 微信 + 看板 | [01-windows-hiseax](lines/01-windows-hiseax.md) | 23 peer 钉 0.2.1-alpha.2;clone + link 安装;分叉的分叉 |
| 本机工作区派活,不绑 GitHub | [02-local-fork](lines/02-local-fork.md) | 同包名/同 id,不能与上游并存 |
| 桌面 bundle,不另起 profile | [03-desktop-fork](lines/03-desktop-fork.md) | 与上游同 id 族,需二选一 |
| 钉在 DSH 0.2.2-rc.3 | [04-adapt-fork](lines/04-adapt-fork.md) | 只适配一个 rc,不跟上游 |
| 多仓 + 钉钉/企微 | [05-multi-repo-im-fork](lines/05-multi-repo-im-fork.md) | 包名换 scope,id 未换 |
| 把 super-agent 当 A2A 网络的一环 | [06-vendored-engine-a2a](lines/06-vendored-engine-a2a.md) | 内核冻结,靠外层适配 |
| 看清每条消息去了哪 | [07-observability-trace](lines/07-observability-trace.md) | 只读;依赖 sqlite 形状 |
| 微信私聊直接派活 | [08-wechat-source](lines/08-wechat-source.md) | 只支持纯文本一对一;白名单默认空 |
| 输入栏一键起停 Super-agent | [09-process-power](lines/09-process-power.md) | 仅 Windows;需独立 profile + bridge |
| 会话级、不另起执行体 | [10-session-level](lines/10-session-level.md) | 设计衍生,不共享代码 |

## 待验证

- **上游对分叉的实际态度**:issues/PR 关闭(adapt 的 README 提到),意味着分叉无法回流;是否有意维持 "prototype only" 不明。
- **`orchestrator.sqlite` 的稳定性**:没有 schema 版本号;trace 的兼容策略是"取不到就说明原因",不是迁移。
- **D1 分叉之间的兼容**:HiSeax 把 id 改成 `dsh-windows-superagent-*`,与 upstream 的 `dsh-superagent-*` 不同;trace/wechat-source 找 `orchestrator` 服务,是否能挂到 HiSeax 上未验证。
- **分叉链的许可完整性**:vHao11 中间层已 404,MIT 声明是否覆盖其改动无法从末端仓库确认。
