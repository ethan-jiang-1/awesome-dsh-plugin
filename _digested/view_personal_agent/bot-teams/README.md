# bot-teams — 多 Bot 个人工作台(仿 xAI Grok Bot / OpenAI Dots)

> 本子分类收纳**围绕“多个长期具名 Bot 组成个人团队、各自持有持久记忆/身份/工具并能互聊或进群协作”展开的 DSH 高影响项目**。目前立 **3 张 ★★★ 源码卡**,全部活跃至 2026-11-26/27 且均在千星以上;三者虽尚未收录进 `awesome-dsh-plugin`,但底层均已源码实锤运行在 `@deepseek-ai/dsh` 之上。

## 定义

同时满足三条:

1. 以**多个长期具名 Bot(Roster / PersonaBots)** 而非单个会话为交互与记忆单元;
2. 支持 Bot 间协作(委派、群聊、收件箱或主 Bot 编排)+ 长期持久化记忆 + 跨渠道触达(IM / 移动 / 浏览器或桌面);
3. 底层直接作为 DSH Cordis 插件包运行,或将 `@deepseek-ai/dsh` 作为核心引擎内嵌打包。

## 成员

| 条目 | 实时星标(11-27) | 注册状态 / 下载 | 形态与一句话 | 卡 |
|------|----------------:|----------------|--------------|----|
| `Fei-Craft/DS-Bot` | **9,110★** | 未入库 / npm `ds-bot` **75,869/月** | 1 Bot = 1 原生 DSH 会话;3 形态 + 8 渠道 IM + 浏览器禁支付 + **已长出 7+ 库内 D2 伴生插件** | [01-ds-bot](01-ds-bot.md) |
| `modelflare-ai/AnyModelBot` | **5,006★** | 未入库 / 桌面+Docker | 独立宿主把 `dsh@0.2.1-rc.4` 打成 `dsh.asar` 按**每 Bot 一子进程**运行;原生 Linux `bwrap` 读围栏 + 4 级应用硬门 | [02-anymodelbot](02-anymodelbot.md) |
| `BotHarness/DeepSeekBot`(Tobs) | **1,076★** | 未入库 / npm `@botharness/tobs` | 85 万行 DSH 多插件矩阵 + Expo 移动端 + Git 记忆 + Noise XK + `ask_secret`/`secret_http` 凭据代填 | [03-deepseekbot](03-deepseekbot.md) |
| `kadaliao/dsh-bots` | 65★ | 未入库 | `@kadaliao/dsh-bots` 轻量 Grok-style 多 Bot Cordis 包(观察中) | — |
| `aibot-fans/dsh-bot` | 48★ | 未入库 | Super-agent + 专家 Bot 群组 monorepo(观察中) | — |

> 已收录于 `awesome-dsh-plugin` 的多 Bot 个人工作台 `MJ-CJM/DSH-Bot`(100★ / `dsh-botgroup` 1,854 月下载)归入 [im-personal-hubs](../im-personal-hubs/02-dsh-bot-mjcjm.md) 以便与注册表内其他实装管家对照;外部非 DSH 高星复现 `OpenMausBot`(28.4k★)与 `CopilotKit/OpenBot`(13.7k★)见 [oss-benchmarks](../oss-benchmarks/README.md)。

## 读法

- **三家代表了把 DSH 变成多 Bot 个人平台的三条工程路线**:
  - **原生插件兼三形态 + 生态吸附**:看 [01-ds-bot](01-ds-bot.md)(同时核对它如何在 `data/plugins/` 里养出 7+ 第三方伴生插件);
  - **独立宿主内嵌每 Bot 独立 DSH 子进程**:看 [02-anymodelbot](02-anymodelbot.md)(重点看原生 Linux `bwrap` 读围栏与默认免审批 CUA / Docker Landlock 的反差);
  - **超重型插件矩阵 + Git 记忆 + 凭据代填**:看 [03-deepseekbot](03-deepseekbot.md)(重点看 `secret_http`/`secret_cli` 与非 Linux 平台 OS 隔离退化)。

## 立卡条件

本子分类只收影响面显著(**≥1,000★** 或形成真实第三方协议复用环)且近 30 天活跃的 DSH 原生/内嵌多 Bot 平台;低于百星的原型仅列成员表观察。
