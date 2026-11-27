---
kind: reference
domain: personal_agent
subcategory: oss-benchmarks
repo: n8n-io/nod
commit: 591788f66c9b088a19b373b574c3f918d8733a71
evidence: 2
status: active
asof: 2026-11-27
---

# n8n-io/nod — 纯 Apache-2.0「自带电脑的个人 Agent」与盲填 Vault / Sentinel 金标准蓝本

> 证据等级:★★(README + `docs/trust/*` 安全模型文档 + `compose.yaml` + `Dockerfile.*` + `package.json` 核验);**未逐行读源码**(参考卡,不要求八段)。参考坐标:`n8n-io/nod@591788f66c9b088a19b373b574c3f918d8733a71`(2026-11-27 `main` 头)。
> **未收录于 `awesome-dsh-plugin` 注册表**(n8n 出品独立个人 Agent,底层绑 Pi runtime,未接 DSH;**立卡理由:它是目前开源界补齐 DSH 最大短板——盲填凭证库、抗注入出站审批与三层费用防线——最干净的纯 Apache-2.0 工程蓝本**)。实时星标为 2026-11-27 GitHub API 读数。

## 它替谁解决什么问题

**想把个人账号、真实网站操作(追发票、退订试用、订票付款)交给常驻 Agent,却最怕「网页提示注入套走密码/乱刷卡/后台任务把 API 额度烧穿」的个人用户与 DSH 安全插件作者。** 现有 DSH 安全插件大多只拦 Shell 删库或做日志脱敏,而 Meta Muse 的 Sentinel 与 OpenAI Dots 的安全底座全部闭源。n8n-io/nod 把「策略活在服务端而非提示词里」「密钥绝不进沙箱与 LLM」「六元组绑定支付审批」完整写成了纯 Apache-2.0 公开工程。

## 适用面:谁该用、谁别用

- **适合**:准备为 DSH 开发个人级 Sentinel / 盲填 Vault / 费用闸门插件的架构师与安全工程师(直接抄它的威胁模型与边界划分);想在 Mac mini / VPS 上自托管单人个人电脑 Agent 的极客。
- **不适合**:需要多用户团队协作、语音通话或直接在现有 DSH 进程里热插拔的团队(`v0.1.0` 研究预览,仅单主人且紧耦合 Pi runtime,无 ACP / AG-UI 外部引擎协议);机器内存吃紧无法常驻 Docker + Postgres + 独立 Workspace/Browser 容器的轻薄本用户(源码默认容器配额 8 GB + 8 GB,桌面版 2 GB + 2 GB)。
- **前置条件**:Node ≥24.21、Docker、PostgreSQL(`pg-boss` 12);笔记本休眠即暂停,24/7 运行需放 Mac mini / VPS;注意默认应用 OAuth 走 n8n 托管连接服务且默认开 PostHog 遥测(可在设置关闭)。

## 业务价值

- **能算清的**:
  - **4,158★ / 627 forks**(2026-11-27 实时值,纯 Apache-2.0 + OpenSSF Best Practices,无闭源核心或企业版切分)。
  - **可复现安全基准(`evals/`)**:官方公布在 GPT-6.1 Sol 上 678 次模拟杂务 **98% 完成率、0 次不安全动作**、LongMemEval-S **93.2%**、WhisperBench 虚假记忆 **0/216**;同时诚实披露 Trust Checker 强依赖评审模型能力(GPT-6.1 Sol 与 Claude Opus 5.5 为 `240/240`,但 Claude Haiku 5.5 漏过 **8 次不安全动作**)。
- **只是预期(推断)**:把它的三件套(上下文隔离 Checker + 盲填 Vault + 三层预算闸门)移植为 DSH 插件,有望把 DSH 个人 Agent 的安全边界从“事后脱敏/防删文件”拉升到“真实账号与支付级防护”。

## 一屏事实

| 项 | 值 |
|----|----|
| 仓库 / 定位 | `n8n-io/nod`(**未入 `awesome-dsh-plugin`**,外部纯开源 Sentinel/Vault 架构蓝本) |
| 对标范式 | Meta Muse Sentinel + OpenAI Dots 独立云电脑的纯 Apache-2.0 开源实现 |
| 实时声量(2026-11-27) | **4,158★ / 627 forks**;创建 `2026-09-25`,最近 push `2026-11-27`(`v0.1.0`) |
| 协议与技术栈 | **纯 Apache-2.0**;TS / Node ≥24.21 / Fastify 5 / React 19 / Postgres + `pg-boss` 12 / Pi runtime / `agent-browser` 0.43 / MCP + Composio / Telegram + WhatsApp |
| DSH 互操作面 | 无原生 DSH 挂载(绑 Pi runtime);**架构与 MCP/Composio 生态可直接借鉴移植到 DSH** |
| 参考 commit | `591788f66c9b088a19b373b574c3f918d8733a71` |
| 证据等级 | ★★(参考卡,未逐行读 `src/`) |

## 值得 DSH 生态直接抄走的四套安全机制(文档与 Compose 核验)

1. **三容器零共享边界(`compose.yaml`, `how-it-works/sandbox-and-browser.md`)**:模型 API Key 与主人密钥**只活在 Nod 服务端进程**,绝不进入容器或模型上下文;Workspace 容器全删 Linux capabilities(`cap_drop: [ALL]`, `no-new-privileges`),独立 `workspace-network` sidecar(`64m` 只读容器 + `iptables`)管出网;Browser 容器只读根文件系统且**与 Workspace 零共享挂载**,仅能访问公网地址。
2. **上下文隔离的出站 Checker(`trust/security-model.md`)**:一切网页、邮件、应用返回都标为不可信数据,记忆**只从主人消息学习**。独立 Checker 评估每次写操作或浏览器变更时,**只看主人原话/规则 + 结构化动作元数据(站点、URL、控件标签、表单目标、输入文本),绝不看原始网页或邮件正文**,彻底切断间接提示注入路径;且贯彻「一次批准只执行一次」,中断/状态不明标 `unknown` 绝不静默重试。
3. **盲填 Vault 与六元组绑定支付(`trust/vault.mdx`, `trust/payments.mdx`)**:
   - 账号密码与 `otpauth://` TOTP 由服务端解密后在已核验源站直接填表,LLM 只见账号名与状态;1Password 集成放在独立 helper 进程(10 分钟空闲回收)。
   - 银行卡存 Vault 但**永不存 CVV**(每次结账仅在 Web/桌面私密面板手填,禁止走 Telegram/WhatsApp);每次支付审批强绑定六元组:`(卡+版本号, 商店源站, 结账页, 含支付 iframe 在内的全部卡字段真实源站, 精确提交按钮, 金额+币种)`,任何编辑或新聊天消息立刻作废审批。
4. **三层防烧钱费用闸门(`use/spending.md`)**:月度硬上限(超限只许聊天查账/调限,且调限本身过 Trust Checker 防注入提额)+ 后台预备金(默认 `$5/月`,并发任务**预扣额度**,无定价/`$0` 模型 fail-closed)+ 单任务 `$5` 阶段停机汇报。

## 代价、风险与待验证

- **紧耦合 Pi runtime**:不支持把 DSH 作为后端引擎挂载,适合“拆架构抄进 DSH 插件”而非直接组合。
- **Checker 非形式化保证**:文档坦承弱模型做 Checker 会放行不安全动作(Haiku 5.5 漏 8 例),强安全仍需强模型开销。
- **待验证(★★ 边界)**:未逐行审计 `src/` 内 Vault 加密实现、`workspace-network.sh` 的 iptables 规则与 Checker 解析器代码。

## 相关档案

- 领域全貌:[../README.md](../README.md)
- 子分类横向对照:[README.md](README.md)
