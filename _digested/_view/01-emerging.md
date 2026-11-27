# ① emerging — 什么冒出来了

> **本期区间**:`29b3ed46e`(2026-11-17,11744 条)→ `8f1a1800e`(2026-11-25,13136 条),8 天净 **+1392**(文件级新增 1440 / 删除 48)。
> **实时雷达**:2026-11-27 实采(`radar-29b3ed46e-to-8f1a1800e-2026-11-27.json`),覆盖本期新增 **1387/1395 个唯一仓(99.4%)**;对其中 ≥30★ 的 **16 个仓**补查 npm 月下载(11 个已发布、5 个未发 npm)。
> **复现**:`python3 _digested/ecosystem/delta.py 29b3ed46e 8f1a1800e` + `python3 _digested/ecosystem/radar_probe.py --delta 29b3ed46e 8f1a1800e --asof 2026-11-27`。

## 一屏答案

1. **新苗子(首次由分层雷达实测)**:本期 1395 个新增唯一仓中共有 **16 个 ≥30★**(4 个属 DSH 诞生前的老主项目背书,12 个为 2026-08-13 后创建的原生/子包仓)。**DSH 原生新苗子前三**为 `xiaoso456/dsh-workflow-lite`(308★ / 4,068 月下载,软工作流)、`dennisyang1986/polymarket-proxy`(160★ / 1,240 月下载,盘口面板)与 `HiSeax/dsh-windows-superagent`(138★ / 已立卡进 [view_proactive_agent](../view_proactive_agent/runtime-forks/01-hiseax.md));**下载黑马**是 `roost-qq/dsh-roost`(55★ 却有 **24,702 月下载**,QQ 官方机器人接入)。
2. **新作者群体**:本期 **819 个全新 owner**,其中 **22 个**一进来就 ≥2 条;头部是 `jyz48prsbr-netizen`(11 条,browser/ui/theme 三线)、`lwfjyjy`(9,tools/ui)与 `Lee2277-t`(8,tools/security/skill)。
3. **标签增速**:浏览器自动化(+357)连续两期增量第一,其次是任务/项目管理(+181)、桌面集成(+181)、安全/权限(+171)。

## 本期高星新苗子榜(2026-11-27 实时雷达,全部 ≥30★)

### A. DSH 原生新仓 / 生态子包(创建于 2026-08-13 之后,12 个)

| 仓库 | 类目 | 实时星标 | npm 月下载 | 创建日 | 定位(注册表自述摘要,★) |
|------|------|-------:|----------:|--------|------------------------|
| `xiaoso456/dsh-workflow-lite` | workflow | **308** | 4,068 | 2026-10-08 | 一句话生成软工作流,编译成提示词计划并支持自动触发与导出 Skill |
| `dennisyang1986/polymarket-proxy` | tools | **160** | 1,240 | 2026-11-16 | 本机 Polymarket 资产/盘口雷达与 CLOB 下注面板 |
| `HiSeax/dsh-windows-superagent` | workflow | **138** | —(未发 npm) | 2026-11-18 | Windows + 微信/飞书 + 看板的主动式多 agent 编排([已立卡 ★★★](../view_proactive_agent/runtime-forks/01-hiseax.md)) |
| `tianacloud/dsh-tiana` | tools | **89** | 1,218 | 2026-11-16 | 侧栏 Tiana 面板:一键部署会话产出的 Web/SQLite/API 到 TianaCloud |
| `Nimbus318/dsh-niuma-broker` | workflow | **76** | 1,417 | 2026-11-23 | 求职进度跟踪、岗位技能对比与多简历版本管理 |
| `yb-zhai/agent-memory` | memory | **61** | —(未发 npm) | 2026-11-21 | 零依赖 JSONL 本地记忆 + 可视化星云面板,可选叠加 Hindsight |
| `roost-qq/dsh-roost` | remote | **55** | **24,702** | 2026-10-26 | QQ 官方机器人接入 DSH,会话持久化映射 + 按说话人收放工具权限 |
| `cheso-ai-platform/dsh-cheso-design` | tools | **50** | 4,267 | 2026-11-17 | 接入腾讯 Cheso 创意平台生成 PPT/海报/视频(子包) |
| `YinkaiYu/chat-in-dsh` | ui | **48** | 4,813 | 2026-11-18 | 侧栏嵌入官方 DeepSeek 网页聊天,复用 DSH 账号免 API Key |
| `killher1/dsh-claude-preset` | identity | **35** | 1,008 | 2026-11-21 | 适配 Claude Code 行为提示词、Plan Mode 与 9 段式压缩预设 |
| `Wasabi2575/dsh-workflow-canvas` | workflow | **34** | 4,493 | 2026-11-20 | 侧栏可视化多代理工作流画布:并行子代理、条件分支与 Lead 暂停拍板 |
| `angel291592/dsh-submodel` | workflow | **31** | 1,833 | 2026-10-30 | 官方 subagent 的双向跨模型派活策略(强主脑下沉便宜执行 / 弱主脑升级专家) |

**看点**:12 个原生新苗子里 **5 个落在 `workflow`**(`workflow-lite` / `windows-superagent` / `niuma-broker` / `workflow-canvas` / `submodel`),印证工作流编排与跨模型派活是当前最活跃的创新带;同时 `roost-qq/dsh-roost`(55★ / 24,702 下载)再次证明**IM 渠道接入的真实采用远大于星标表现**。

### B. 预存主项目背书(创建于 2026-08-13 之前,4 个)

| 仓库 | 类目 | 实时星标 | npm 月下载 | 创建日 | 说明(星标属主项目) |
|------|------|-------:|----------:|--------|--------------------|
| `zhoushoujianwork/easyeda-agent` | tools | 1,241 | — | 2026-06-25 | 嘉立创 EasyEDA Pro 自动化 MCP 桥接 + Skill |
| `ximizhou/convenient_window_free` | tools | 200 | 356 | 2026-07-31 | Windows 便捷窗口/触发角/手势工具的 DSH 适配 |
| `onlyLT/wow-gongwen-writing` | skill | 61 | — | 2026-07-04 | 中文公文写作技能(15 种法定公文 + GB/T 9704) |
| `kaust-ark/ARK` | workflow | 38 | — | 2026-03-24 | `Idea2Paper` 论文实验与独立评审子包 |

*(口径说明:以上仅作雷达发现,除已标 ★★★ 卡片外均为 ★ 自述 + 实时 API 读数,未读源码;8 个新增仓在 2026-11-27 采样时返回 404/不可达,记入快照 `coverage.errors`。)*

## 新 owner 榜(本期首见、新增 ≥2 条,Top 12)

| owner | 新增条目 | 主要落点类目 |
|-------|---------|--------------|
| jyz48prsbr-netizen | 11 | browser×3, ui×3, theme×2 |
| lwfjyjy | 9 | tools×4, ui×3, session×1 |
| Lee2277-t | 8 | tools×5, security×2, skill×1 |
| qinghuidaqzp | 6 | fun×2, usage×1, dev×1 |
| DaYangtuo247 | 4 | ui×2, usage/theme×1 |
| compilink | 4 | model×2, ui/notify×1 |
| wzvx | 4 | tools×3, market×1 |
| yanli-nyan | 4 | ui×3, security×1 |
| 0131kikimy / AmahaHanasaki / Beeasy-L / CHENJIAMIAN | 各 3 | tools×2 / tools×3 / ui×2+notify / ui×2+session |

(完整 22 名 ≥2 条;其余 797 个是单条新 owner——长尾仍是单件试水,不成群体。上期 18 天有 2565 个新 owner,本期 8 天 819 个,密度相近。)

## 标签增长(34 组中增量 Top 15)

| 标签 | 上期 → 本期 | 增量 |
|------|------------|------|
| 浏览器自动化 | 881 → 1238 | **+357(连续两期增量第一)** |
| 任务/项目管理 | 1388 → 1569 | +181 |
| 桌面集成 | 1608 → 1789 | +181 |
| 安全/权限 | 1513 → 1684 | +171 |
| 文档/写作输出 | 1235 → 1398 | +163 |
| 用量/成本监控 | 1134 → 1280 | +146 |
| RAG/知识库 | 898 → 994 | +96 |
| 上下文/会话工程 | 873 → 969 | +96 |
| 主题美化 | 785 → 877 | +92 |
| 数据/DB | 378 → 450 | +72 |
| 终端/命令行 | 618 → 685 | +67 |
| 模型聚合/路由 | 700 → 765 | +65 |
| MCP 协议 | 524 → 586 | +62 |
| DeepSeek | 555 → 613 | +58 |
| 视频 | 378 → 429 | +51 |

**读法**:浏览器自动化连续两期是增量最大的标签(上期 +450,本期 +357),仍在把插件从"文本工具"推向"操控真实环境";桌面集成、安全/权限、任务/项目管理三条老主线各 +170~180,体量继续膨胀。全表 34 组命中 **9753/13136(74.2%)**。

**口径提醒**:标签是描述文本的正则命中,不是技术采用的实测;标签表有已知误报史(见 [ecosystem/02](../ecosystem/02-tech-landscape.md) 方法注记),本轮未对 Top 标签做精度抽样。引用"某标签涨了多少"时,把它当"描述里这样写的条目变多了",不要当"采用该技术的插件变多了"。
