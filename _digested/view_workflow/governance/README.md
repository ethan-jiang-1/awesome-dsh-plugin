# governance — profile 级治理与路由

> 不只编排 agent,而是给整个 profile 装一层"目标/事实/授权/风险/验收"的治理:提示注入、职责路由、证据账本、Control Center。

## 定义

插件在 profile 层而不是单次任务层工作:把治理正文注入 system prompt,把职责/能力路由成可执行状态,把过程证据落成独立账本,并提供检查界面。判定标准:去掉它,单个 agent 仍能跑,但整个 profile 失去准入、路由或验收约束。

## 成员(人工确认)

| 条目 | 星标 ⚠ | 说明 | 单卡 |
|------|--------|------|------|
| orziz/odai#odai-dsh-plugin | 89(仓库级) | 13 个 `odai_*` 工具 + 独立 JSONL 证据账本 + 中文 Web Control Center;仅承诺 DSH 0.2.2-rc.1 | [01](01-odai.md) ★★★ |

## 立卡条件

出现第二个 profile 级治理实现,或被 ≥3 个条目复用其证据/职责协议。

> 本轮立卡:它把治理做成运行时(8 个 systemPrompt section + 职责状态机 + JSONL 证据),不是提示词模板;⚠89 星属仓库、下载 1,951。门槛未变。

## 生长

**odai 不是配置包,也不是单个 skill**:`dsh/plugin` 只是 profile 打包壳,机制在打包进来的 `dsh/runtime/src`(52 文件 13,942 行)。

- **治理正文**:8 个 systemPrompt section(从 `-20` 起)注入"事/实/法/成/界"五问与操作标准。
- **职责路由**:`pending→active` 状态机,职责可 `same-turn`/`child`/`inline`;API 走 `subagents.startActivation`,包内零模型映射。
- **证据账本**:按 `sha256(session)` 命名的 JSONL,hash 去重、循环写、`fsync`、短写回滚;权限只由认证 scope/child 身份/风险保护决定,模型映射不产生权限。
- **压缩/记忆/安全连续性**:压缩走 `llm/stream` 拦截;本地语义记忆与安全连续性各自独立文件,拒绝符号链接与凭据。
- **Control Center**:中文 Web 界面,用于职责与证据检查。

**归属与兼容**:仓库 2026-03-19 创建、首个 `dsh/` 提交 2026-08-14,采样 2026-08-19 仅隔 5 天 → ⚠89 星主体属 odai 项目;真正属于该包的是 1,951 下载与 3 个月 60 个 npm 版本。registry 自述"兼容 0.1.5-rc.1"已过期;当前包精确 pin DSH 0.2.2-rc.1,本机 0.2.1-rc.5 的 `register(definition)` 只收一个参数,`{ when }` 会被静默丢弃、条件准入退化。

**判断**:这是目前唯一一个把"治理"做成 profile 运行时的样本;它的可复用面不是某条规则,而是"证据账本 + 职责状态机"这套结构。下一个同类出现之前,它仍是单点。
