---
kind: reference
domain: personal_agent
subcategory: oss-benchmarks
repo: milind-soni/OpenMausBot
commit: b2286fcc7aa3a28aee730ce88ac8fae4ca405c4b
evidence: 2
status: active
asof: 2026-11-27
---

# OpenMausBot — GitHub 最高星 Grok Bot / Muse / Dots 开源复现与零代码 ACP 挂载靶标

> 证据等级:★★(README + 官方文档 `docs/` + `compose.yaml` + `package.json` 核验);**未逐行读源码**(参考卡,不要求八段)。参考坐标:`milind-soni/OpenMausBot@b2286fcc7aa3a28aee730ce88ac8fae4ca405c4b`(2026-11-27 `main` 头)。
> **未收录于 `awesome-dsh-plugin` 注册表**(外部开源独立产品,但原生支持通过 `customAcp` 零代码挂载 DSH 为工作引擎,也可通过 `openmausbot mcp` 被 DSH 编排)。实时星标为 2026-11-27 GitHub API 读数。

## 它替谁解决什么问题

**想在本地或自托管服务器上复刻 Grok Bot / Meta Muse / OpenAI Dots 多 Bot 联系人体验、但又想自带订阅/执行引擎(包括 DSH)的个人重度用户与插件架构师。** 闭源商业个人 Agent 面临地区封锁、订阅上限和平台锁死;而社区现存的轻量 DSH 插件大多只做单个切面(只做 IM 或只做浏览器)。OpenMausBot 把“多 Bot 联系人侧栏 + 每 Bot 独立沙箱/浏览器 + 定时/Webhook 触发 + 凭证库 + 可移植 Playbook”做成了一个完整的本地优先宿主壳。

## 适用面:谁该用、谁别用

- **适合**:想直接体验或对照当前社区最高星个人 Agent 形态的评估者;想零代码把 `dsh` 经 ACP 挂进多 Bot 桌面/移动端外壳的开发者;以及在研究「per-turn Bubblewrap 沙箱」「allowlist 团队预设导入」「Bitwarden/1Password 密码掩码」的 DSH 插件作者。
- **不适合**:只需要在现有 DSH Web/Desktop 里装一个小插件就能用的纯 DSH 用户(它本身是独立的 Electron + Node ≥24 全栈应用);不能接受 CLI/服务端模式下明文保存 `config.json` API Key 或个人默认 `Full access` 权限的强合规环境;需要纯无限制开源的企业功能使用者(`enterprise/` 目录采用专有 `OpenMausBot Enterprise License`,删去该目录可构建纯 Apache-2.0 OSS 版)。
- **前置条件**:Node ≥24(或 Electron 桌面包 / Docker Compose);挂载 DSH 需通过 `~/.openmausbot/config.json` 配置 `customAcp` 指向 DSH ACP 启动命令,或用 `openmausbot mcp` 暴露受限 stdio MCP 控制面。

## 业务价值

- **能算清的**:
  - **28,403★ / 4,035 forks**(2026-11-27 实时值,建仓仅 3.5 个月,当日仍有提交 `v0.1.184`),是目前 GitHub 上直指 Grok Bot / Muse / Dots 范式声量最大的开源复现。
  - **零代码接 DSH 路径明确**:官方文档 `docs/custom-engines.md` 写清了 `customAcp` 配置协议——剥离无关供应商 Key、通过临时 ACP 会话自动发现模型与思考档位、并将 ACP `session/request_permission` 直接路由到原生聊天审批卡;反向 `docs/mcp-server.md` 提供受限控制面 MCP(明确禁止远程授予审批、删 Bot、改凭证或启停 VM)。
- **只是预期(推断)**:借鉴其 `bot-box` 每轮 Bubblewrap 隔离、Bitwarden 最小 `PATH` 隔离与 Playbook 白名单导入安全模型,有望缩短 DSH 生态补齐个人安全边界的试错周期,但落地成本取决于各实现方。

## 一屏事实

| 项 | 值 |
|----|----|
| 仓库 / 定位 | `milind-soni/OpenMausBot`(**未入 `awesome-dsh-plugin`**,外部开源标杆参考) |
| 对标范式 | xAI Grok Bot / Meta Muse / OpenAI Dots / Manus Cue 开源本地优先复现 |
| 实时声量(2026-11-27) | **28,403★ / 4,035 forks**;创建 `2026-08-11`,最近 push `2026-11-27`(`v0.1.184`) |
| 协议与技术栈 | Apache-2.0(含专有 `enterprise/` 例外);TypeScript / Node ≥24 / React 19 / Electron / SQLite + NDJSON / `agent-browser` / CUA Rust driver |
| DSH 互操作面 | 双向:**`customAcp` 挂载 DSH 为引擎**(`docs/custom-engines.md`) + **`openmausbot mcp` 供 DSH 调用**(`docs/mcp-server.md`) |
| 参考 commit | `b2286fcc7aa3a28aee730ce88ac8fae4ca405c4b` |
| 证据等级 | ★★(参考卡,未逐行读源码) |

## 值得 DSH 生态直接借鉴的关键机制(文档与配置核验)

1. **Per-Turn Bubblewrap 沙箱(`docs/bot-box.md`)**:云主机环境下,每轮 Bot 执行(引擎 CLI + Shell + MCP)跑在非特权 `bubblewrap` 沙箱内,隐藏 `~/.openmausbot` 下的 `messages.db`、`config.json` 与其他 Bot 目录,仅按当前激活引擎绑定对应登录凭据(`sign-in-masks.ts`)并暴露单轮权限 socket。
2. **Playbook 团队预设白名单导入(`docs/presets.md`)**:一键导入 Markdown + YAML 团队包时采用严格白名单解析——只接收角色说明、Playbook、纯文本 `SKILL.md`(剥离脚本)与起始笔记,**绝不导入模型、电脑配置、审批等级、凭证、MCP 或激活态定时任务**(导入的定时任务默认暂停,文件导入的 Skill 默认关闭)。
3. **浏览器与桌面分层操控(`docs/browser-packaging.md`, `docs/computer-use-integration.md`)**:Electron 侧按 Bot 分区维护 `persist:` `WebContentsView` 并经 CDP 驱动,支持人机同屏接管;本机桌面操控强制经 CUA Rust driver 私有 socket,Wayland 下 fail-closed。
4. **凭证掩码、用量上限与只读 Sentinel(`docs/bitwarden.md`, `docs/usage-caps.md`, `docs/sentinel.md`)**:Bitwarden/1Password CLI 仅给最小 `PATH`、值在进入对话与模型前掩码并密封进 `logins.json.enc`;支持全局与单 Bot 日/月美元与 Token 上限(`stops: "unattended"` vs `"everything"`);Sentinel 以 `SQLITE_OPEN_READONLY` 监控 WAL 与 NDJSON 费用/异常,只存归一化哈希不存正文。

## 代价、风险与待验证

- **默认权限偏宽**:文档明确独立个人 Bot 默认权限为 **`Full access`**,仅托管公司工作区默认 `Ask`。
- **CLI/服务端明文配置**:`openmausbot setup` / 服务端模式把 API Key 与 MCP 请求头明文存在 `config.json`(`0600`),仅桌面端对供应商 Key 做 OS 级加密。
- **外部商业依赖**:云桌面(`boat.dev`)、内置 Composio App Events 与 `enterprise/` 属商业或外部托管能力。
- **待验证(★★ 边界)**:未逐行审计 `server/bot-box/` 隔离实现、`logins.json.enc` 加密细节与 `customAcp` 挂载真实 `dsh --profile acp` 的端到端兼容性。

## 相关档案

- 领域全貌:[../README.md](../README.md)
- 子分类横向对照:[README.md](README.md)
