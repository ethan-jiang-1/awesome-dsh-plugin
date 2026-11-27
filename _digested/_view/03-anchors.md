# ③ anchors — 锚候选与明星

> **本期区间**:`29b3ed46e`(2026-11-17,11744 条)→ `8f1a1800e`(2026-11-25,13136 条)。
> **实时声量快照**:2026-11-27 全库纯 GraphQL 实采(`stars-2026-11-27.json`,覆盖 **12,501/12,636 唯一仓 = 98.9%**)+ 卡片级全量快照(`live-2026-11-27.json`,46/46 卡覆盖)+ 0007 增量雷达(`radar-29b3ed46e-to-8f1a1800e-2026-11-27.json`,1,387/1,395 = 99.4%)。旧的 2026-08-19 冻结边车仅保留作历史对照。
> **复现**:`python3 _digested/ecosystem/delta.py 29b3ed46e 8f1a1800e`(③b 候选分层)+ `python3 _digested/ecosystem/radar_probe.py --full --asof 2026-11-27` + `python3 _digested/ecosystem/live_probe.py --asof 2026-11-27`。口径见 [`_method/02`](../_method/02-anchor-metrics.md),证据等级见 [`../AGENTS.md`](../AGENTS.md) §一 底线 3。

## 两轴:声量 × 扩散(锚候选 / 明星)

星标是**声量**(且易受主项目背书或病毒传播稀释),第三方提及/衍生是**扩散**(每期名单现算)。两轴都高才是真锚;只有声量高的是"明星";想直接抄走经过源码验证的机制见 [④ leverage](04-leverage.md)。

| 对象 | 实时声量(2026-11-27) | 扩散(③b 候选 → 卡内判定) | 判定 | 单卡 |
|----|--------|------|------|------|
| `DSH-better-sidebar` | **5,357★** / 382,551 月下载 | 66 候选(1 同名 fork + 65 描述;0007 新增 `dsh-cove-task` 声明依赖与 `dsh-zen-remote` 桥接兼容) | **平台候选**:右栏原生 Tab 注册表;2026-11-18 抽样 3 家呈 1 硬 / 1 软 / 1 提及 | [enhance-shell/01](../view_ui/enhance-shell/01-better-sidebar.md) ★★★ |
| `hindsight` | 63,745★\* / 147,875 月下载 | 10 候选(7 同名 + 3 描述;0007 新增 `yb-zhai/agent-memory` 可选后端)→ 卡内判定 **4 个**真记忆工具 | **标准候选**:收敛在服务端 API + `~/.hindsight` 配置 + bank 命名 | [host-backed/01](../view_memory/host-backed/01-hindsight.md) ★★★ |
| `dsh-superagent`(上游) | 24,565★\*(不在注册表) | 15 候选(13 同名 + 2 描述)→ 卡内判定 **9 个真依赖**(6 D1 分叉 + 3 D2 契约扩展)+ 3 D3 衍生 | **品类定义者**:定义了 Source/Policy/Ticket 语义,尚无统一插件协议 | [view_proactive_agent](../view_proactive_agent/README.md) ★★★(6 卡) |
| `dsh-agent-teams` | **3,112★** / 62,898 月下载 | `agent-teams`/`agentteams` 并集 9 第三方 → 卡内判定 **6 条真衍生/硬依赖** | **workflow 最接近锚**:纯 DSH 原生,收敛在 `team.json` 与 patch 行 id | [multi-agent/01](../view_workflow/multi-agent/01-agent-teams.md) ★★★ |
| `dsh-genui` | **1,067★** / 67,561 月下载 | 26 候选(扣 `genuine` 假阳性)→ 卡内判定 **3 依赖/伴生** + 3 同类独立 + 4 互操作 | **协议栈候选**:声明式 JSON + 按需 Skill + 四表面渲染 | [inline-genui/01](../view_ui/inline-genui/01-genui.md) ★★★ |
| `dsh-TUI` | **8,333★** / 80,099 月下载 | 9 候选(5 同名 + 4 描述)→ 卡内判定 **2 条真对接**(其一需补丁) | **声量锚 / 扩散苗子**:换壳代表,自有插件 ABI 尚未免补丁收敛 | [replace-shell/01](../view_ui/replace-shell/01-dsh-tui.md) ★★★ |
| `billion-context` | 8,555★\* / 3,873,165 月下载 | 8 候选(2 同名 + 6 描述,多为清理/兼容工具) | **代理层高声量**:星标属主项目,靠本地 HTTP 代理绕过插件接口层 | [compression/01](../view_session/compression/01-billion-context.md) ★★★ |
| `OpenViking` | 42,892★\* / 48,817 月下载 | 4 候选(3 同名 + 1 描述) | **对接基线,未成标准**:宿主背书示例,衍生已跨出 memory | [host-backed/02](../view_memory/host-backed/02-openviking.md) ★★ |
| `modlens` | 5,096★\* | 4 候选(描述) | vision 参考实现,未逐条源码判定 | — ★ |
| `treg` | 9,642★\* / —(未发 npm) | 3 候选(全为 `RestRegular` 子串假阳性)→ 真实扩散 **0** | **明星,非锚**:150 行接入商业托管代理,高星归主产品 | [single-purpose/01](../view_tools/single-purpose/01-treg.md) ★★★ |
| `ouroboros` | 6,388★\* / —(未发 npm) | **0** | **明星,非锚**:24 行 YAML 纯配置挂 39 万行 Python 引擎 | [external-engine/01](../view_workflow/external-engine/01-ouroboros.md) ★★★ |

*(\* = 仓库级高星属于跨宿主主项目或早于 DSH 的宿主仓,不代表 DSH 适配层独立热度。)*

## 一屏答案

1. **按扩散轴看真锚未变**:真正形成第三方依赖/衍生生态的仍是 `DSH-better-sidebar`(66 候选)、`dsh-superagent`(9 真依赖)、`hindsight`(4 真记忆工具)、`dsh-agent-teams`(6 真衍生)与 `dsh-genui`(3 伴生);`ouroboros` 与 `treg` 虽近万星但扩散归零,仍是明星而非锚。
2. **全库 12,501 仓实时星标彻底改写了“中尾部空心”的旧印象**:过去 08-19 边车停更导致 `model`(曾报 62★)、`session`(曾报 83★)、`dev`、`usage`、`market`、`identity` 等类目严重失真。2026-11-27 实测显示,**DSH 原生高星梯队已全面长出**:如 `Ebony-Vinyl/dsh-our-free-model`(88,499★)、`dsh-market/dsh-market`(13,611★)、`kingcharleslzy-ai/dsh-purge`(12,995★)、`yjh051108/dsh-routing-suite`(7,027★)、`T-Auto/dsh-ops`(6,032★)、`bowenliang123/dsh-context`(5,546★)、`Minglink/dsh-infinite-gen-5`(4,778★)。
3. **0007 本期新增高星苗子已首次浮出水面**:详见 [01-emerging](01-emerging.md),原生前三为 `xiaoso456/dsh-workflow-lite`(308★ / 4,068 月下载)、`dennisyang1986/polymarket-proxy`(160★)与 `HiSeax/dsh-windows-superagent`(138★),另有下载黑马 `roost-qq/dsh-roost`(55★ / 24,702 月下载)。

## 全 23 类实时头部总览(2026-11-27 全库 12,501/12,636 仓实采)

> `*` 标注仓库创建于 `2026-08-13` 之前(大概率属宿主主项目或早于目录的 monorepo 背书);其余为 `2026-08-13` 及以后建仓的 DSH 生态项目。仅列每类按唯一仓库去重后的 Top 3,未读源码项均为 ★ 级信号。

| 类目 | 实时星标头部 Top 3(2026-11-27) | 判读与领域册 |
|------|----------------------------------|--------------|
| `ui` | `zhu1090093659/dsh-web#packages/dsh-web-all` 10,660\* · `ccch1mneyyy/dsh-TUI` 8,333 · `MeteorNOX/DeepSeek-Balance-Whale-Widget` 7,485(另 `better-sidebar` 5,357\* 为扩散第一) | 最成熟盘子;见 [view_ui](../view_ui/README.md) |
| `tools` | `Tencent/WeKnora#dsh-weknora` 38,327\* · `DayuanJiang/next-ai-draw-io#dsh-plugin` 37,204\* · `superdesigndev/treg` 9,645\*(原生第一 `T-Auto/dsh-ops` 6,032) | 头部仍被跨宿主主项目占据,但原生 Windows/Blender 工具已破两千至六千星;见 [view_tools](../view_tools/README.md) |
| `session` | `ranxianglei/billion-context` 8,556\* · `Minglink/dsh-infinite-gen-4` 4,778 · `liangmianya/dsh-synapse` 781 | 破除 08-19 边车“最高 83★”假象,但标准协议仍未收敛;见 [view_session](../view_session/README.md) |
| `workflow` | `loopx-project/loopx#dsh-loopx-plugin` 6,767\* · `Q00/ouroboros#integrations/dsh-plugin` 6,388\* · `chuspeeism/dashi-taskboard#deepseek-harness` 3,539\*(原生第一 `dsh-agent-teams` 3,112\*) | 外部引擎星高零扩散,真扩散在 `agent-teams` 与 [view_proactive_agent](../view_proactive_agent/README.md);见 [view_workflow](../view_workflow/README.md) |
| `memory` | `vectorize-io/hindsight#coding-agents` 63,745\* · `volcengine/OpenViking#examples/dsh-memory-plugin` 42,893\* · `MemTensor/MemOS#memos-local-plugin` 12,521\*(原生第一 `dsh-mnemon` 1,139) | 三大机构宿主背书领跑;社区原生看 `mnemon`/`memento`/`engramory`,见 [view_memory](../view_memory/README.md) |
| `model` | `Ebony-Vinyl/dsh-our-free-model` **88,499** · `dingminhua/dsh-connect-workbuddy` 2,056 · `Alice-Marx/dsh-model-router` 1,021 | 免费模型车道引爆全库最高原生星标(2,502 forks),需后续源码核验 |
| `dev` | `yjh051108/dsh-routing-suite` 7,027 · `strukto-ai/mirage#dsh` 3,939\* · `first-fluke/oh-my-agent#dsh` 1,479\* | 原生热重载/注入套件 `dsh-routing-suite` 冲上 7 千星,已达候补立册观察线 |
| `usage` | `bowenliang123/dsh-context` 5,546 · `Han-1413141/dsh-cost-meter` 760 · `wssfk12138/dsh-damage-pulse` 291 | `dsh-context` 从 416★ 涨至 5,546★(在 `_leverage` 产品线有深度样本卡) |
| `market` | `dsh-market/dsh-market` 13,611 · `zhu1090093659/dsh-web#packages/dsh-plugin-manager` 10,660\* · `LivXue/dsh-plugin-shop#dsh-plugin-shop` 665 | 分发轨道本身就是超级流量入口 |
| `identity` | `kingcharleslzy-ai/dsh-purge` 12,995 · `aureth-labs/dsh-aurabot-qq` 749 · `ECNU/EduWork#dsh-oidc` 424 | `dsh-purge` 社区分支(4,873 forks)拉高整个类目声量 |
| `skill` | `tw93/Mole#mole` 76,368\* · `zhu1090093659/dsh-web#packages/dsh-skill-explorer` 10,660\* · `QingYunA/answer-me-with-html` 6,692 | 原生 HTML 可视化输出技能 `answer-me-with-html` 达 6,692★ |
| `theme` | `elysia395/dsh-wallpaper-engine` 8,260 · `Small-tailqwq/dsh-deep-whale#maid-atelier` 3,153 · `Nwflower/dsh-claude-style` 725 | 壁纸与皮肤类呈典型高星低衍生形态 |
| `fun` | `PC2005-cloud/dsh-pet#dsh-pet` 6,772 · `flizzywine/dsh-tavern#dsh-tavern` 1,779 · `Alterssss/dsh-bili-whale` 1,137 | 桌宠与娱乐交互头部均破千星 |
| `notify` | `xmanrui/dsh-im` 3,834 · `shaobeichen/dsh-pocket` 3,187 · `c1overzz/dsh-bili-scroll` 1,479 | IM 通道与手机访问稳定双三千星 |
| `remote` | `zhu1090093659/dsh-web#packages/dsh-ssh` 10,660\* · `liguobao/ds-harness-remote` 3,854 · `saya-ch/dsh-mobile` 1,011 | 远程访问已形成三强格局,另本期冒出 `dsh-roost`(24,702 月下载) |
| `browser` | `Tencent/BrowserSkill#dsh-plugin-browserskill` 10,766\* · `DDDMUC/dsh-free-search` 1,741 · `omdsh-dev/dsh-browser#packages/browser/bridge-browser` 1,148\* | 标签连续两期增速第一,值得下轮评估是否单独立册 |
| `docs` | `tt-a1i/archify#integrations/deepseek-harness` 100,694\* · `dream-num/dsh-univer-office` 763 · `ECNU/EduWork#dsh-knowledge-studio` 424 | `archify` 为十万星级宿主背书 |
| `vision` | `liustack/modlens` 5,096\* · `ysr666/dsh-vision-router` 1,306 · `Anionex/dsh-vision-toolkit` 951 | 视觉头部均已破千星 |
| `security` | `kenryu42/cc-safety-net` 2,109\* · `ADWMC/helm-d#helmd` 1,539 · `toby-bridges/api-relay-audit` 934\* | 机制与安全边界见 [`_leverage/leverage/lever-draw-limit`](../../_leverage/leverage/lever-draw-limit/README.md) |
| `git` | `zhu1090093659/dsh-web#packages/dsh-git-graph` 10,660\* · `Akimiya-z/codex-guard#dsh` 131 · `xbzbing/dsh-git-panel` 62 | 除 `dsh-web` 子包外普遍长尾 |
| `agi` | `FuRongJun-1999/dsh-memory` 757 · `Clearailhc/clearai-dsh` 700 · `oriliz/agent-crop` 332 | 小盘探索类目 |
| `voice` | `Yuuyuko-uu/dsh-tts-bridge` 270 · `Fishsb/dsh-voice-prompt-enhancer` 135 · `PolinniZhong/dsh-omi-voice` 75 | 小盘长尾 |
| `wsl` | `6Mikao9/dsh-wsl-workspace` 125 · `XINY11451/dsh-wsl` 21 · `stallenlu/dsh-wsl-suite` 4 | 零增长小类 |

*(异常星/fork 比提醒:全库扫描中个别高星原生仓存在星/fork 极高比值,如 `helloHub1212/dsh-windows-mcp` 2,674★ / 12 forks,比值 222.8;未经源码与下载交叉核验前,所有未立卡高星条目只视为 ★ 级线索。)*

## 本期缺口(下轮优先)

- **新冒出的千星级原生仓待源码深挖**:`dsh-our-free-model`(88k★)、`dsh-routing-suite`(7k★)、`T-Auto/dsh-ops`(6k★)、`dsh-context`(5.5k★)、`answer-me-with-html`(6.7k★)与 0007 新苗子 `dsh-workflow-lite`(308★)均尚无 `view_*` 源码级单卡;下轮按「有没有可借鉴机制」择优立卡。
- **OpenViking 仍为 ★★ 参考卡**:尚未读源码,下轮可按需升至 ★★★。
- **全量 npm 下载仍停在 2026-09-12**:当前分层雷达已覆盖全部 46 卡 + 0007 高星新苗子(≥30★)的实时月下载,但全库 13,136 条中低星黑马(类似 55★ 却 24.7k 月下载的 `dsh-roost`)仍可能存在盲区。
