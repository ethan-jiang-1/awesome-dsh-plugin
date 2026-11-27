---
kind: reference
domain: personal_agent
subcategory: oss-benchmarks
repo: CopilotKit/OpenBot
commit: 8b185ee1b7883c7f629ebd27fbaf37125737fdc9
evidence: 2
status: active
asof: 2026-11-27
---

# CopilotKit/OpenBot — 合并 OpenDots + openfuse 的企业级 BYO-Harness 与 CEL 策略网关标杆

> 证据等级:★★(README + `docs/` + `docker-compose.yml` + 顶层目录核验);**未逐行读源码**(且核心服务端为预构建镜像 `ghcr.io/copilotkit/openbot`,未开放全部后端源码)。参考坐标:`CopilotKit/OpenBot@8b185ee1b7883c7f629ebd27fbaf37125737fdc9`(2026-11-27 `main` 头)。
> **未收录于 `awesome-dsh-plugin` 注册表**(外部开源平台参考,原生提供 AG-UI + 受治理 MCP 接入任意 Agent 框架,仓库内已含 15 个框架适配器目录)。实时星标为 2026-11-27 GitHub API 读数。

## 它替谁解决什么问题

**想把 Grok Bot / OpenAI Dots / Claude Duet 的体验搬进可控的企业或个人容器工作台,同时把「浏览器容器隔离、策略审批、不可篡改审计、人机接管」沉在平台层、让底层 Agent 框架可自由替换(BYO Harness)的平台架构师。** 之前 CopilotKit 生态同时维护 `OpenDots`(6,786★)与 `openfuse`(6,599★)两套独立产品;现在两者都已正式归档为 OpenBot 的前端皮肤(`app/src/skins/`),共享同一套 `/api/v2` 与容器编排底座。

## 适用面:谁该用、谁别用

- **适合**:研究多皮肤 UI 解耦(OpenDots / openfuse / openduet 共用后端)、fail-closed CEL 策略网关、人机实时接管("Take the wheel")与 Teach-a-Bot 录屏建技能的 DSH 平台/插件设计者;需要企业 SSO + 审计 + K8s 部署的团队。
- **不适合**:要求 100% 源码可控无闭源依赖的纯开源使用者——仓库虽挂 MIT 协议,但实际运行的 `server` / `agent-computer` / `supervisor` 来自预构建镜像,且启动依赖 **CopilotKit Intelligence**(桌面端 30 天可续期免费许可,K8s 需商业/试用许可,默认带 1 分钟 mTLS 心跳的 `management-agent`);也不适合轻量化单机运行(需 Docker + Postgres `pgvector` + Bun 1.4+ + k3d/K8s)。
- **前置条件**:Docker Desktop(或 Kubernetes)、PostgreSQL(`pgvector:pg17`)、Bun 1.4+;接入外部 Harness 需暴露 AG-UI 端点并配置精确匹配的 `AGENT_ENDPOINT_ALLOWED_HOSTS` 白名单。

## 业务价值

- **能算清的**:
  - **13,733★ / 1,718 forks**(2026-11-27 实时值,原 `OpenDots` 6,786★ 与 `openfuse` 6,599★ 的 README 均已实测挂出 `now a skin in OpenBot` / `status: no longer maintained` 徽章),合计代表超 2.7 万星关注度的收敛形态。
  - **15 个框架适配器目录**与 **8 原语信息架构**(`Conversations / Routines / Memory / Skills / Apps / Computer / Approvals / Activity` × 3 层作用域)给出了清晰的产品抽象模板。
- **只是预期(推断)**:其「网关先评估 CEL 策略 + 先写审计行再执行」以及「人工接管时拒绝而非排队 Bot 动作」的设计,可直接作为 DSH 侧栏/托管网关插件的安全范本。

## 一屏事实

| 项 | 值 |
|----|----|
| 仓库 / 定位 | `CopilotKit/OpenBot`(**未入 `awesome-dsh-plugin`**,外部开源标杆参考) |
| 对标范式 | 统一 OpenAI Dots(`OpenDots`) + `openfuse` + Grok Bot 的 BYO-Harness 容器平台 |
| 实时声量(2026-11-27) | **13,733★ / 1,718 forks**;创建 `2026-08-17`,最近 push `2026-11-27`(`v1.2.1`) |
| 协议与技术栈 | 前端/模板 MIT + **服务端镜像与 CopilotKit Intelligence 专有许可**;TS / Bun 1.4+ / React+Vite / Hono / Tauri / Postgres(`pgvector`) / K8s / AG-UI |
| DSH 互操作面 | AG-UI 端点接入(`docs/agent-frameworks.md`) + 受治理 MCP 目录(未识别与自定义 MCP 工具默认判为写操作) |
| 参考 commit | `8b185ee1b7883c7f629ebd27fbaf37125737fdc9` |
| 证据等级 | ★★(参考卡,服务端为闭源镜像) |

## 值得 DSH 生态直接借鉴的关键机制(文档与配置核验)

1. **Fail-Closed CEL 策略网关与「先审计后执行」(`docs/architecture.md`, `docs/approvals.md`)**:所有浏览器、文件、Shell 与 MCP 调用必须经过服务端网关:先从服务端持有的快照解析目标 → 用 CEL 规则按 `tool.name`、`intent`、`page.host`、`element.*`、`command` 与 **`initiator.*`(区分定时 Routine 与真人触发)**做 fail-closed 判定 → 写入只追加 PostgreSQL 审计行 → 最后才放行执行。
2. **四级审批优先级与防权限爬坡(`docs/approvals.md`)**:动作类别(支付/删除/发送/分享/发帖/改密/2FA 永远询问,点击类"总是允许"绝不能升级覆盖支付或外发) > 规则(最严优先:Admin > User > Conversation) > Auto-review > 高度警惕开关;巡检类 Routine 修改前一律询问。
3. **人机接管「拒绝而非排队」+ Teach-a-Bot 录制**:遇到登录/2FA 墙时,用户点击"Take the wheel"接管容器浏览器(`help_requested` → `control_taken` → `control_released`),接管期间 Bot 动作**直接被拒绝而非排队**避免交接竞态;内置实时浏览器录制器把用户操作转成可复用 Skill。
4. **网络与容器隔离(`docker-compose.yml`)**:`postgres` 置于独立 `data` 网络,`agent-computer` 容器完全不可达数据库且不注入服务端环境变量/密钥,仅绑定回环地址并配每容器独立 `COMPUTER_TOKEN`(可选 gVisor `runsc`)。

## 代价、风险与待验证

- **并非纯开源**:核心服务端镜像与 CopilotKit Intelligence 闭源且带许可与心跳机制,不能当作纯开源底座直接分叉。
- **运维较重**:全套需 Docker + Postgres + Intelligence(桌面端需 k3d;EKS 侧约需 3.55 vCPU;Intelligence 嵌入服务仅限 `amd64`)。
- **待验证(★★ 边界)**:闭源后端的 CEL 求值器与 Vault 加密细节不可直接审计;未实测 DSH 经 AG-UI 桥接接入 OpenBot 的工具权限映射。

## 相关档案

- 领域全貌:[../README.md](../README.md)
- 子分类横向对照:[README.md](README.md)
