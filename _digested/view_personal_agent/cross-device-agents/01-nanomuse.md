---
kind: card
domain: personal_agent
subcategory: cross-device-agents
repo: nano-muse/nanoMuse
commit: f7d775243e04024a3f40231207bcb37845368143
evidence: 3
status: active
asof: 2026-11-27
---

# nanoMuse — 3,740★ 明牌复刻 Meta Muse 的跨设备个人 Agent,桌面端就是 DSH Cordis 插件包

> 证据等级 ★★★(源码级;`nano-muse/nanoMuse@f7d77524`)。未跑 `node --test`/pytest 或跨设备真机联调;`harness/dsh-nanomuse` Bundle、HMAC Hands 审批票据、中继 Hub 与同步库、Python Sentinel/Vault 与 IM 渠道分布均经源码逐文件核验。
> **未收录于 `awesome-dsh-plugin` 注册表**(npm `dsh-nanomuse` 404,仅发 GitHub Release tarball `dsh-nanomuse-1.0.10.tgz` 与桌面/安卓安装包)。星标 3,740★ / 468 forks 为 2026-11-27 GitHub API 实时值。

## 它替谁解决什么问题

**想要 Meta Muse 那种“一个人、一个跨手机/电脑/网页统一身份与记忆的个人 Agent,在手机上 `@Mac` 就能指挥家里的电脑干活,高危操作就近在手头设备上审批”的跨设备体验,但不想受限于 Meta 地区封锁与闭源云 VM 的个人用户。** 现有方案的痛点有三处:

- **桌面 Agent 离了电脑就失联,手机 Agent 算力与工具又太弱**:两者账号、记忆、面孔和审批流割裂,没法在通勤时用手机让家里 Mac 跑任务并在手机上点“同意”。
- **跨设备把电脑操控权暴露出去极危险**:如果靠提示词让模型传 `confirmed: true` 就能操作键鼠,一次网页提示注入就能控电脑。
- **电脑端接外部远程 MCP 服务时 OAuth 令牌容易落进会话日志**:直接写死在 DSH 配置里容易暴露给模型或工具输出。

`nano-muse/nanoMuse`(附技术报告 arXiv:2610.08699)把跨设备网格拆成三端协同:桌面端以原生 DSH Cordis bundle(`dsh-nanomuse`)承载 Agent、Hands(MCP + HMAC 审批)与 Reach 跨设备工具;手机端基于 OpenMinis 1.13(安卓 proot Alpine + iOS Swift);自托管或社区中继(`cloud/`)负责跨端路由与同步。

## 适用面:谁该用、谁别用

- **适合**:同时拥有手机(Android/iOS TestFlight)与电脑(macOS/Win/Linux)、看重跨设备 `@Mac` 派活、手机端审批定时任务与 Muse 式“同一张脸/同一份记忆”体验的个人用户;愿意自托管 `cloud/` 中继(`scripts/self-host.sh --local`)或接受社区中继的开发者。
- **不适合**:**误以为桌面 DSH 版自带飞书/钉钉/企微/Telegram 的用户**——源码实测 4 个 IM 渠道**仅存在于独立 Python 服务端(`nanomuse/channels/`)**,在 `harness/dsh-nanomuse/` 与 `android/` 中零命中;**要求跨设备数据端到端加密(E2EE)的隐私敏感用户**——中继服务器默认开启明文对话同步(`sync_messages` 存明文至中继 SQLite,`cloud/nanomuse_cloud/db.py:179-200`),Hub 转发的截屏与 ≤8 MiB 文件均为 TLS 到中继的明文 JSON(**非 E2EE**);以及不能接受 **`GPL-3.0-or-later`** 传染许可或需要把 `dsh-nanomuse` 装进最新 `0.2.2-rc.x` 宿主的团队(精确钉死旧版 `0.2.0-rc.2`)。
- **前置条件**:独立桌面包 252–503 MB(macOS 未公证、Windows 未签名,首次在 Win 启动因 Defender 扫描可能耗时数分钟,`harness/desktop/src/main.ts:60-62`);单独装 tarball 需精确兼容 `@deepseek-ai/dsh@0.2.0-rc.2`;iOS 端受系统限制无 GUI Hands 操控。

## 业务价值

- **能算清的**:
  - **3,740★ / 468 forks / 185 open issues**(2026-11-27 实时值,当日仍在合并 PR #970);GitHub Release `v1.0.9` 单版安卓 APK 下载 **5,035**、`dsh-nanomuse` tarball 160(`v1.0.10` 11-25 刚发)。
  - **不可伪造的跨进程 GUI 审批防线**:用每次启动随机生成的 `NANOMUSE_MCP_CONFIRM` 做 `HMAC-SHA256(secret, canonical_json(args))[:32]`,彻底杜绝 LLM 伪造 `confirmed: true` 绕过敏感点击/按键审批(`nanomuse/bridge/mcp_server.py:167-183`)。
  - **三端代码体量完整**:`harness/dsh-nanomuse/src/` 4.66 万行 TS(+ 79 测试套件 1.68 万行)+ `nanomuse/` 6.09 万行 Python(+ 127 pytest)+ `cloud/` 4.37 万行 FastAPI + 手机端自有代码 10.2 万行(Kotlin 6.87 万 + Swift 3.32 万)。
- **只是预期(推断)**:
  - “定时任务在电脑跑、审批卡片广播到你手头的手机上先答即消(`phone-approvals.ts`)”的交互范式极贴合 Meta Muse 日常使用心智,但三套独立运行时(DSH/OpenMinis/Python)并存会持续放大跨端同步维护成本。

## 一屏事实

| 项 | 值 |
|----|----|
| 仓库 / 注册状态 | `nano-muse/nanoMuse`(**未收录于 `awesome-dsh-plugin`**,npm 404,GitHub Release 分发 tarball 与安装包) |
| 子分类 | `cross-device-agents`(跨设备与随身个人 Agent,仿 Meta Muse) |
| 自述 | "nanoMuse: an open-source personal agent for every device you own... your phone's screen and your computer as its hands" |
| 星标 / fork(2026-11-27) | **3,740★ / 468 forks / 185 open issues**;创建 `2026-09-23`,最近 push `2026-11-27`(`v1.0.10`) |
| 包形态 / 许可 | DSH bundle(`dsh-nanomuse-1.0.10.tgz`)+ Electron 桌面端(282–503 MB)+ Android APK(40.5 MB)+ iOS TestFlight + 自托管 Cloud;**`GPL-3.0-or-later`** |
| 代码规模 | `harness/` 75,273 行(`dsh-nanomuse/src` 46.6k)+ `nanomuse/` 60.9k Python + `cloud/` 43.7k + `android/` 自有 Kotlin/Swift 101.9k |
| 宿主钉版 | **精确钉死 `@deepseek-ai/dsh@0.2.0-rc.2`**(全部 18 条 `@deepseek-ai/dsh-*` peer 无范围符,`harness/dsh-nanomuse/package.json:98-117`) |
| repo@commit | `f7d775243e04024a3f40231207bcb37845368143`(2026-11-27 +0800) |
| 证据等级 | ★★★ |

## 它到底是什么

**一套用三套运行时拼出“Meta Muse 跨设备个人网格”的开源复现。** 它的真实分工并不对称:

```text
手机端(OpenMinis 1.13: Android Alpine proot / iOS Swift — 不跑 DSH!)
  ⇄ wss://<relay>/v1/hub (明文 JSON 帧转发,16MB/帧,非 E2EE) ⇄
桌面端(Electron + 独立 ~/.nanomuse/desktop + DSH 0.2.0-rc.2 + dsh-nanomuse bundle)
  ├─ Hands: stdio MCP 拉起打包版 Python `nanomuse mcp` → 本地 nut-js operator(带 HMAC 审批票据)
  ├─ Reach: 7 个跨设备工具(devices/screen/shell/files/open/notify/delegate) + 手机审批广播
  ├─ Connectors: 本地代理(127.0.0.1:38417)出站注入 OAuth/API Key,不进 DSH 配置与日志
  └─ Rooms: Feed / Ideas / Goals / Library(rooms.json)
(独立 Python Web 服务 nanomuse/ 才包含飞书/钉钉/企微/TG 渠道与 Sentinel/Fernet Vault)
```

## 怎么接进 DSH

1. **双 Patch 覆盖与 12 子路径导出(`harness/dsh-nanomuse/{package.json,cordis.patch.yml,presets/nanomuse.patch.yml}`)**:
   - `cordis.patch.yml:10-102` 禁用原生 `skill`、`ui-brand-official`、`ui-sidebar`、`ui-settings-general`、`pwsh-sandbox`,把默认 preset 切为 `nanomuse`,插 6 个宿主插件(`nanomuse-skills`/`windows-pwsh-sandbox`/`nanomuse`/`nanomuse-cloud`/`nanomuse-rooms`/`nanomuse-connectors`)。
   - `presets/nanomuse.patch.yml:12-199` 克隆 `standard` preset(禁用 `tool-plugin-manager`)并追加 `capability-skill`、`hands`、`reach`、`rooms-tools`、`connectors-tools` 五块插件。
2. **离线打包与桌面补丁(`harness/desktop/scripts/prepare-dsh.mjs:50-127`, `src/main.ts:32-201`)**:使用独立 `~/.nanomuse/desktop`(不碰 CLI `~/.dsh`),以 `ELECTRON_RUN_AS_NODE` 拉起 `0.2.0-rc.2`,打两处桌面补丁(`patchCapacityDefaults`/`patchClearedSessionAccess`),并在 Linux 把 `sharp` 换为 `@img/sharp-wasm32` 规避 Electron GLib 符号崩溃。
3. **回环路由围栏(`harness/dsh-nanomuse/src/admit.ts:26-38`)**:全部 `/nanomuse/*` 路由包裹 `mountGuarded()` 调用宿主 `connection.requestRejection(req)` 防 DNS 重绑定。

## 关键实现

| 模块 | 位置 | 作用与源码实证 |
|---|---|---|
| 不可伪造 HMAC Hands 审批 | `nanomuse/bridge/mcp_server.py:86-184`, `harness/dsh-nanomuse/src/cloud.ts:4035-4074` | `RiskLevel.SENSITIVE` 键鼠操作要求 `confirmed === HMAC-SHA256(NANOMUSE_MCP_CONFIRM, canonical_json(args))[:32]`;拒绝后 DSH 侧弹原生审批卡,点一次允许才现签票据重放(注:独立裸跑 `nanomuse mcp` 缺密钥时会退化接受模型传 `confirmed: true`) |
| 跨设备 `@Mac` 派活与接力 | `android/.../DeviceMention.kt:8-75`, `harness/dsh-nanomuse/src/{device-conversations,reach,cloud}.ts` | 安卓端截获开头 `@设备名` 注入单轮指令调 `nanomuse-pc task`;桌面端直发持久 Hub `task` RPC 并记日志经 `task.status` 恢复;`Reach` 注册 7 个跨设备工具,远程审批按 `{approvalId,deviceId,risk,sessionId,grantTarget}` 哈希隔离 |
| 跨设备定时审批与远控门 | `harness/dsh-nanomuse/src/{cloud.ts:3721-3766,actions.ts:7-11,phone-approvals.ts:1-118}` | 桌面端 `remoteControl` **默认关闭**(`false`),非信任设备来调 `shell/files/screen/task` 弹 110 秒 `AskDesk` 审批卡(但一旦打开或加信任,来单直接以 OS 用户静默执行);定时任务审批广播 `any_device: true` 至手机(600 秒),先答即全端消卡 |
| 本地代理注入远端 MCP 凭据 | `harness/dsh-nanomuse/src/connectors.ts:19-25,208-246` | OAuth/API Key 存 `$DSH_HOME/nanomuse/connectors.json`(`0600`),DSH MCP 客户端只连本地 `127.0.0.1:38417`(带进程随机 `x-nanomuse-proxy` 头),代理出站注入凭据,会话日志零明文 |
| Python Sentinel 污点与 Vault | `nanomuse/sentinel/policy.py:77-152`, `nanomuse/vault/vault.py:1-120` | Python 运行时实现 6 级策略与污点追踪(读私密数据后非白名单出网即便 `auto` 模式也强制升 `ASK`),Fernet 加密 Vault 以 `{{vault:NAME}}` 占位仅向 `accepts_secrets` 工具解析并脱敏输出 |

## 为什么它突出

只用本仓库自身证据:

- **唯一把 Meta Muse 跨设备体验真拆进 DSH Cordis Bundle 的高星开源实现**:3,740★ + 468 forks,不仅复现了桌面+手机跨设备派活与跨端审批,还保留了独立 `dsh-nanomuse.tgz` 插件形态。
- **两项高含金量安全原语值得直接抄进 DSH 插件**:`HMAC-SHA256` 绑定参数的 MCP Hands 审批票据(防模型自填 `confirmed: true`)与本地回环 MCP 凭据注入代理(凭据不进 DSH 配置与日志)。

## 代价与边界

1. **中继非 E2EE 且默认明文云同步(`cloud/nanomuse_cloud/db.py:179-200`, `sync.py:15`, `hub.py:33-34`)**:登录账号默认同步明文对话到中继 SQLite(每条截断 16 KB、上限 20,000 条),Hub 转发的截屏与 ≤8 MiB 文件均为中继可见明文 JSON;必须自托管中继才不暴露给社区服 `cloud.nanomuse.cn`。
2. **三运行时割裂(IM 渠道不在桌面 DSH 版里)**:飞书/钉钉/企微/Telegram 只活在 Python `nanomuse/` 服务器里,桌面 DSH App 并没有内置这些 IM 入口;手机端跑的是 OpenMinis(Alpine proot)而非 DSH,三套代码需手工对齐协议与目录清单。
3. **严格钉死旧版 DSH `0.2.0-rc.2`**:18 条 peer 无范围符,升级宿主须手工比对 `nanomuse.patch.yml` 与上游 `standard.patch.yml` 并重修 `prepare-dsh.mjs`。
4. **`GPL-3.0-or-later` 强传染许可 + 重体积未签名桌面包**:安装包 252–503 MB 且 macOS 未公证/Windows 未签名;开启 `remoteControl` 后远端文件/Shell 指令不再二次弹窗。

## 可信度与复现

**读过**:`README.md`、`AGENTS.md`、`harness/dsh-nanomuse/{package.json,cordis.patch.yml,presets/nanomuse.patch.yml}`、`harness/dsh-nanomuse/src/{index,reach,hub,hands-tools,admit,approval-grants,actions,phone-approvals,device-chat,device-conversations,connectors,desk}.ts`、`cloud.ts` 关键段、`harness/desktop/{package.json,src/main.ts,scripts/prepare-dsh.mjs}`、`nanomuse/{bridge/mcp_server.py,sentinel/policy.py,channels/manager.py,vault/vault.py}`、`cloud/nanomuse_cloud/{hub,db,sync}.py`、`android/.../DeviceMention.kt`。**未读**:React 客户端组件、桌面 `operator*.ts`、各 IM 适配器正文与测试套件,未跑实测。

```sh
git clone --depth 1 https://github.com/nano-muse/nanoMuse && cd nanoMuse
git rev-parse HEAD   # f7d775243e04024a3f40231207bcb37845368143
cat harness/dsh-nanomuse/package.json
```

## 待验证

- 未实测自托管 `cloud/` 中继在弱网与 16 MB 帧上限下的重连恢复表现。
- 未读 `harness/desktop/src/operator*.ts` 核验本地 `nut-js` 服务是否有类似受保护窗口黑名单。
- 未验证 `dsh-nanomuse-1.0.10.tgz` 直接装入独立 DSH `0.2.0-rc.2` CLI/Web(脱离 Electron 壳)时的完整可用性。
