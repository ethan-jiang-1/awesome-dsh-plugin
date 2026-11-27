# `view_personal_agent/` 工作规则

个人 Agent 前沿跨域专题(对标 Meta Muse / OpenAI Dots / xAI Grok Bot 范式)。首立共 12 张卡:**9 张 DSH ★★★ 源码卡**(7 个 GitHub 未入库高星仓 + 2 个 `awesome-dsh-plugin` 已入库实装锚)+ **3 张外部开源标杆 ★★ 参考卡(`kind: reference`)**。

> 写作顺序:新卡先写 `它替谁解决什么问题 / 适用面 / 业务价值`,再进八段;规范见 [`../_view/WRITING.md`](../_view/WRITING.md)。
>
> 通用纪律(底线、八段模板、立册/立卡门槛、同步七步)只在 [`../AGENTS.md`](../AGENTS.md);本文件只写本册特有的判断线索。

## 四条子分类主轴

| 子分类 | 定位 | 读源码必核点 |
|---|---|---|
| **`bot-teams`** | 多 Bot 个人工作台(仿 Grok Bot / Dots) | 是原生插件还是内嵌子进程;跨 Bot/群防环与私密记忆隔离;第三方伴生插件复用 |
| **`cross-device-agents`** | 跨设备、口袋真 DSH 与 24/7 个人世界(仿 Meta Muse) | 手机到底跑真引擎还是远控壳;中继是否真 E2EE;上游补丁数量与 OS 锁死 |
| **`im-personal-hubs`** | 已入 `data/plugins/` 的实装个人管家 | 多说话人权限剪枝、信息流控制(IFC)、npm 真实包名与月下载量 |
| **`oss-benchmarks`** | 外部高星开源复现(`kind: reference`, ★★) | 零代码挂 DSH 协议缝(ACP/AG-UI/MCP)或可直接抄走的 Sentinel/Vault 蓝本;不得混算进 DSH ★★★ 卡数 |

## 本册特有的判断线索

- **宁缺毋滥,只留影响面大且活跃的真例子。** 不收零星玩具原型(除非具备不可替代的协议复用);必须同时验近期 push 与真实代码体量/下载/衍生。
- **不把 Proactive Agent、桌宠或“名义支持 DSH”的壳混进本册。** 工程工单派活留在 `view_proactive_agent`;纯物理/Live2D 挂件(如 `GrokBot_in_DeepseekHerness`)留在 `fun`;像 `stablyai/orca` 这种源码实测 `BOT_AGENTS` 排除 `dsh` 的大宿主绝不凭 README 误收。
- **未入库必须显式标清。** 允许收录尚未出现在 `awesome-dsh-plugin/data/plugins/`、但源码实锤运行在 `@deepseek-ai/dsh` 上的高星 GitHub 仓,卡内首屏与 `README.md` 必须明确标注「未收录于注册表 / GitHub 独立分发」,绝不与注册表 13,136 条分母混淆。
- **先查出站安全,再看功能花活。** 个人 Agent 管的是用户的真实账号、聊天记录、屏幕与钱包,读源码必查六件事:① 默认权限档是否过宽(如 CUA `approval: 'auto'` 或 `PermissionPreset.Full`);② DSH 沙箱不拦读导致的跨平台隔离断层(Linux `bwrap` vs Win/macOS/Docker Landlock);③ 凭据是否明文落盘、是否进 LLM 上下文;④ 中继与云同步是否真 E2EE;⑤ 遥测/非商用子许可陷阱(如 `dsh-Go` 安卓不可关 DAU、`dsh-world` 微信引擎非商用许可);⑥ 文档与代码的真实偏差(如 `DSH-Android` `sensitive` 读取未询问、`dsh-roost` 群 `confirmGate` 未验回复者)。
- **绝对禁止写“全部 ★★★”。** 本册含 3 张 `oss-benchmarks/` `★★` 参考卡,领域 `README.md` 必须如实拆分 ★★★ 与 ★★ 计数。

## 刷新

- 每轮同步后:除扫描 `data/plugins/` 中新出现的 `ds-bot` 伴生插件、Dots/Muse/OpenClaw 桥与高下载 IM 管家外,另用 `gh api` 复查本册未入库高星仓的新发版、是否已入库 `data/plugins/` 及 `live_probe.py` 快照;
- 若某张 `oss-benchmarks/` 参考卡落地了原生 DSH 集成,重读源码后移入对应 DSH 子分类升为 ★★★;
- 本册由 `_digested/verify.mjs` 自动发现并校验;增删改卡必须同步 `plugin-map.svg`、`live_probe.py`、`view_data.py`,有新机制/反模式时补进 [`../_view/04-leverage.md`](../_view/04-leverage.md)。

## 完成判据

- 全部 Markdown 相对链接、UTF-8、LF、frontmatter、前三节顺序、SVG 证据级与 `_data/` 通过 `node _digested/verify.mjs`;
- `live_probe.py` 与 `view_data.py` 刷新后 `_data/health.md` 无新增 `no-live-repo`;
- 9 张 ★★★ 卡与 3 张 ★★ 参考卡在 `README.md`、子分类 `README.md` 与 `plugin-map.svg` 三处完全一致。
