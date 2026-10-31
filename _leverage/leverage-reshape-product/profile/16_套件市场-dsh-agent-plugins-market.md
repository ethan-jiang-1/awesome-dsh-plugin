---
title: "套件市场 · dsh-agent-plugins-market"
domain: reshape-product
kind: sample
positioning: "`Sivan757/dsh-agent-plugins-market`：把别的 agent 的整套插件就地读进来，当成本地可安装的 suite。"
takeaway: "来源 checkout、suite 安装记录、workspace 过滤是不同状态层；逐 artifact validation 与 mount 不把坏声明扩散成整套件失败。"
read_when: "要做跨生态导入/套件分发；或要设计多来源、多标签页的资源管理面。"
status: observed
updated: 2026-10-31
---
# 套件市场 · dsh-agent-plugins-market:别人家的套件，就是你的分发单位

> **研究范围**：目标 tag `dsh-agent-plugins-market-v0.13.0` / commit [`d3364da`](https://github.com/Sivan757/dsh-agent-plugins-market/commit/d3364dabd05187eb3fd595b1cd854e83a45f5314)；DSH 上游对照为 tag `dsh-v0.2.1-rc.3` / commit [`1f81c04`](https://github.com/deepseek-ai/deepseek-harness/commit/1f81c047fc48fa190a683e469daa699857e9afe8)。目标源码、测试和同 SHA CI 记录已读，未安装、构建或执行目标代码。完整引用见[`05 源码复核`](./_证据/05_套件市场-dsh-agent-plugins-market-源码复核.md)。
> **类**:`1` 壳与工作台 · **层**:**7**（分发）→ 4（身份：persona/hook）→ 3（八标签页工作区）
> **采用信号**：★ 19 / forks 1 / issues 6（GitHub API，2026-10-31）；npm 月下载 4,752（近 30 天，含 CI/镜像；不代表用户数）
> **一句话**:`0.13.0` 将外部 source checkout 解析成 suite 视图，以 user-state 记录 install/enable，并由 runtime reconciler 把已启用 suite 的各资源面挂入宿主；workspace filter 与 suite install record 是不同 owner/scope。
> **借鉴价值**:**① 来源 checkout 更新不等于安装内容冻结，`lockCommit` 不保证 refresh 不变；② validation 要声明失败粒度（suite / MCP file / MCP server），不能概括为“坏声明一律整套跳过”；③ named credentials 缺失与 OAuth 授权失败是两种状态；无 credential store 时 OAuth token 只存进程内；④ hook dry-run 用 host shell 执行，`dry_run` 标志不是 sandbox；⑤ suite 卸载默认留 checkout，source removal 与物理删 checkout 是独立动作。**

> **证据成熟度**：source/store、parser/validation、suite install/reconcile、credential/OAuth record 和 hook adapter 可作 `机制参考`；行为参考不成立。本次没有真实 profile、OAuth browser callback 或 shell hook `[RUN]`。
> **样本档案**
> **repo**:[`Sivan757/dsh-agent-plugins-market`](https://github.com/Sivan757/dsh-agent-plugins-market) · **npm**:`dsh-agent-plugins-market` · **版本**:`0.13.0`
> **目录条目**:`data/plugins/Sivan757__dsh-agent-plugins-market.yml`（`market`）
> **装法**:`dsh plugin --profile <name> add dsh-agent-plugins-market` → 重启 → Settings → Agent Plugins；或 GUI 插件页装
> **证据链**：原 README 摘录见[`02 产品形态`](./_证据/02_产品形态-原始挖掘.md) §二；固定 tag 源码、schema/状态链、测试和同 commit CI run 见[`05 源码复核`](./_证据/05_套件市场-dsh-agent-plugins-market-源码复核.md)。
> **仍待验证**：目标 DSH host 下的实际 hook 决策、OAuth 浏览器授权、同机多个 workspace state 和跨 peer range 行为；源码 memo 有明确复现边界。

---

## 它想干什么 · 为什么值得借鉴

**意图 [DOC]**：README 将它定位为外部 agent 套件入口，列出多个 layouts 和八个资源管理 tab；文档中的可用范围不等于每种方言都语义保真。

**意义 [SRC-TARGET][OBS]**：目标实现将 source metadata/checkout、suite view、user-scoped installed suite、per-resource adapters 分层；本地 checkout 可就地扫描，远端 marketplace metadata 不是安装内容本身。它把“来源”从“安装单位”中分离，但自动 refresh 会改变受管 checkout，因此安装时 `lockCommit` 不能解读为冻结/可回滚版本。迁移意义来自架构事实，长期升级价值仍需边界说明。

**用户价值 [DOC/OBS]**：README 的价值主张是少做跨 agent 手工搬运；源码确认能以 suite 为单位安装和启用，但六个 surface 的 workspace filter 与 suite install 状态不是同一层。MCP missing env reference 会返回可见 missing-credential；远程 401 OAuth 是否跨重启保留取决于 DSH credential store 是否存在。

**表达 [DOC/SRC-TARGET]**：八 tab、先预览再装、来源删除确认是 README 交互描述；底层源码支持多面 mount 与按粒度诊断。Hooks dry-run 只以 host shell 执行 command 并传入 `dry_run:true`，不是隔离 sandbox；用户的实际界面和权限边界本次未运行验证。

## 0. 一页速览(想抄的人只看这 20 行)

| 主张 | 固定版本证据 | 结论边界 |
|---|---|---|
| 套件支持十种布局 | `[DOC]` README；`[SRC-TARGET]` layout registry 有顺序，逐个 manifest adapter 后有优先级 fallback | 兼容深浅不一；布局数量不是保真度指标 |
| source 与 suite | `[SRC-TARGET]` source checkout/refresh 与 user state installed suite 分离；suite key=`<sourceId>/<suiteId>`，install 时记录 `lockCommit`，但受管 source refresh 可变更 checkout | `lockCommit` 不是内容冻结/回滚；workspace filters 是另一状态层 |
| 读取和诊断 | `[SRC-TARGET]` v1 schemas runtime-vendored；MCP file invalid disable 一个面，单 server invalid 跳过该 server；其他 manifest errors 有 fatal/ignored 分级 | 不能把“任何坏声明都会跳过整 suite”概括成原子 fail-closed |
| credentials / OAuth | `[SRC-TARGET]` `${ENV}` missing 映为 missing-credential；401 OAuth flow 可有持久 grant record，但无 `ctx.credentials` store 时仅内存有效 | `needs-credentials` 不是所有 OAuth 失败的通用状态；真实 callback 本次未跑 |
| hooks / dry-run | `[SRC-TARGET]` command hook 通过 DSH shell adapter 返回 decision；dry-run 在用户 home 以 host shell 执行并传 `dry_run:true` | dry_run 是脚本标志，不是 sandbox；DSH 权限边界本次未实测 |
| uninstall / ownership | `[SRC-TARGET]` suite uninstall 删 install entry，不删 source checkout；source removal 默认也保留 checkout，外部 local path 不由工具删除 | README 确认框不能替代对 adopted checkout 归属和删除目标的说明 |
| 测试与运行 | `[TEST]` 有 source、validation、install/reconcile、OAuth、hooks、migration tests；`[CI]` 对该 commit 找到 success run `40302671805`；本次未运行目标代码 | 可作机制参考；不能声称本轮已现场 mount/OAuth/hook 测试 |

---

## 1. 它在产品里的位置

| 七层 | 动作 | 说明 |
|---|---|---|
| **7 分发** | 分发单位从"我的 bundle"变成"**别人的套件**" | 来源、镜像、刷新、安装、启停 |
| 4 身份 | persona、hooks、instructions 都属于"这个 agent 是谁" | 八页里三页在这层 |
| 3 槽位 | 一个八标签页的工作区 | 市场与资源管理同居一处 |

### 1.1 它是 profile 侧的第 6 种形态:**进口型**

前四种是"怎么把自己的东西装成一件"，第五种（`15_接管套件`）是"换掉宿主自带的"，这一种是"**把别人的整套东西变成你的可安装单位**"：

| 形态 | 谁的资产 | 例子 |
|---|---|---|
| 全家桶 / 组合包 / 聚合补丁 | 作者自己的插件 | `dsh-web` / `dsh-suite` / `dsh-plugin-kit` |
| 界面套件 | 作者自己的界面 | `codex-ui` |
| 接管型 | 宿主自带的实现 | `15_接管套件` |
| **进口型** | **别的 agent 生态的套件** | **本卡** |

> **定位 [DOC/OBS]**：README 将“market”描述为资源入口；目标代码把 source registry、suite installation 和多个 runtime adapters 组成产品工作流。可观察的产品边界不是货架，而是 source → suite → resource surface 的映射；这一定位不代表各布局行为等价或运行时 UX 已验证。

### 1.2 它和 `51_分发与救生页` 的分工

| | `51_分发与救生页`（plugin 侧） | 本卡 |
|---|---|---|
| 卖什么 | DSH 插件（npm / GitHub） | **别的 agent 的套件**（十种布局） |
| 关心的失败 | 宿主起不来 → 救生页 | 套件装上了但能力没挂 → **诊断后跳过 + 凭据提示** |
| 单位 | 包 | **suite**（可含技能/命令/persona/MCP/LSP/hooks） |

---

## 2. 机制（可照抄的部分）

### 2.1 布局解析是有顺序的 adapter registry

`[DOC]` README 宣称支持十种布局并提供 layout coverage/compatibility report。

`[SRC-TARGET]` v0.13.0 的 `layouts.ts` 定义 adapter priority；manifest discovery 按此顺序解析，同一 checkout 多 manifest 时候选失败会写 diagnostics 并继续下一个 adapter。`validate.ts` 的 runtime schema 实际只接受 Agent Plugins v1 的 1.0/1.1；Universal/Cursor/其他格式的描述不能一概说成同一 schema validator 已核。

**洞察**：当同一目录可能含多个格式声明时，用可审计优先级和候选级诊断处理 parser fallback；须同时标明哪个格式真的被完整 schema 校验、哪些只是兼容读取。布局数量不等于语义保真度。

### 2.2 Source、suite install 与 workspace filters 是不同 owner/scope

```text
source registry + checkout (.sources/<sourceId>, user state.json)
  ├─ scan snapshots/cache → suite metadata
  └─ install record (<sourceId>/<suiteId>, lockCommit, enabled)
       └─ runtime reconcile → command / MCP / hooks / LSP adapters

project-native layouts → <projectRoot>/.dsh/agent-plugins/ (separate scan root)
workspace surface filter → runtime service constructed for workspace cwd
```

`[SRC-TARGET]` 自管 Git/archive checkout 位于 `.sources`；local path 原地读。`SourceStore.refresh()` 会更新受管 branch checkout；installed record 保存安装时 Git HEAD/archive digest，但未发现 refresh 将 installed content pin 回 digest 或提供 rollback，因此 `lockCommit` 不能解释为冻结。suite install/enable 位于用户 `state.json`；project resources 是另一路扫描；workspace surface filter 由 runtime workspace service 管理，不代表 suite install record per-workspace。

**洞察**：设计“来源可刷新、suite 可安装、workspace 可过滤”时分开状态 owner 和更新语义。要做真正 reproducible install，必须额外 pin/拷贝不可变 snapshot，而不是只记录 install-time hash。

### 2.3 安装与 runtime reconcile 是可逆状态转换

`[SRC-TARGET]` suite identity 以 `<sourceId>/<suiteId>` 限定，避免同名 source 碰撞。`InstallStore.install()` 会从当前 source checkout 重新发现 suite，拒绝 remote reference，记录 Git HEAD/archive digest，并置 enabled；不复制资源文件。state change 触发 derived snapshot refresh，再由 reconciler 分别挂载 command、MCP、hooks、LSP adapters；surface filter 分支独立 gating，避免关一个面误卸载同 suite 的其他面。

suite uninstall 只删除 user install record，不删除 checkout；source removal 会删该 source 下的 installed entries，但默认保留受管 checkout；只有显式 deleteCheckout 才删除 `.sources/<id>`，外部 local path 永不由工具删除。

**洞察**：资源管理应把来源所有权、安装选择、每面启用和 workspace filter 分开建模；移除 UI 操作要明示是“卸载 suite”“删 source 记录”还是“物理删除 checkout”，并规定其依赖关系。

### 2.4 Credentials 与 OAuth 是两个状态机

`[SRC-TARGET]` `${NAME}` env reference 经可选 `ctx.credentials` 解析，credential service 不存在才 fallback 到 process env；缺值时 server 映射为 `missing-credential`，不把占位符替换为空值。此状态不同于远程 MCP 401 后尚未授权/授权失败。OAuth grant 以 folded server name 存 token/client metadata；PKCE verifier 仅在进程内。若 credential record store 存在则 record 可持久化；没有该 store 时 OAuth flow 仍可完成，但 token 只在当前进程内有效。重新授权删除 target-owned grant 并触发 mount；server declaration 仍归 source 管理。

> **洞察**：凭据产品要区分“配置引用缺值、未授权、授权失败、已授权但未持久化”。UI 状态可以共享一套语言，但底层 owner、保存条件与重授权动作必须按状态类型分开。

### 2.5 Hook dry-run 不是 sandbox

`[SRC-TARGET]` hook adapter 在 live agent 上通过 DSH shell executor 执行命令 hook；`PreToolUse` decision 映射 host allow/ask/deny，`continue:false` 请求 host hook-cancel。异常/超时/解码失败有 containment path。实现按事件 / matcher / timeout 提供声明卡；dry-run 在用户 home 通过 host shell 执行并设置 `dry_run:true`，默认 30 秒、上限 60 秒并限 stdout/stderr 大小。该标记只是传给脚本的输入，**不隔离文件/进程权限**；本轮未验证 shell executor sandbox 或具体 hook 决策 UI。

> **洞察**：给 hook 加预览能解释“要运行什么”，但不能替代权限边界；只有执行器隔离本身被验证后才能声称安全 dry-run。

---

## 3. 产品体验（README 主张，未实测）

### 3.1 首次使用（README 描述，未实测）

| 时刻 | 看到 | 设计 |
|---|---|---|
| 装 | 插件页装 + 重启；或 `dsh plugin add` | 两条路等价 |
| 打开 | **Settings → Agent Plugins**，已有**一个第一方来源** | 开箱就有货，不是空市场 |
| 刷新 | 拉取该来源的套件列表 | 拉取与安装分开 |
| 看套件 | 打开 → 看内容 → 安装 → 保持启用 | 先看后装 |
| 补凭据 | MCP 页回答凭据提示 | 缺口有名字 |
| 日常 | 八标签页：Market / Instructions / Skills / Commands / Personas / MCP / LSP / Hooks | 按问题分页 |
| 换项目 | 项目自带资源需开"Scan project Agent layouts"；每工作区可存"资源窗口"收藏 | 作用域显式 |

### 3.2 产品文档给用户的边界（`[DOC]`）

- README 宣称坏声明会诊断后跳过，并称“never half-mounted”；源码实际存在 manifest fatal/ignored、MCP file disable、MCP server skip 等不同粒度，不能把该句理解成所有失败都是整 suite fail-closed。
- README 说 source removal 默认保留文件、显式勾选才删受管市场目录；源码可确认 suite uninstall/source removal/checkout deletion 是不同操作，具体受管 checkout 的删除需注意 `deleteCheckout`。
- README 提醒一个 layout 可读取不代表其原平台所有行为都能用；这是合理兼容边界，但本卡尚未逐 layout 对比。

### 3.3 模型/运行时可见面（源码已追踪，未跑 host）

`[SRC-TARGET]` reconciler 将启用 suite 分送到 commands、MCP、hooks、LSP adapters；skills 经 provider/catalog，personas 经 agent-preset provider。资源是否进入实际模型上下文/工具表还取决于 DSH 当前 session/workspace、凭据和 capability gates；本次未启动 host 确认可见结果。

> 可借鉴的是让每个 resource adapter 有独立 install/enable/validation/status 边界；不应从安装记录直接推断模型一定看见或能调用该能力。

---

## 4. 证据与边界

| 口径 | 值（2026-10-31） |
|---|---|
| ★ / forks / issues | 19 / 1 / 6（GitHub API） |
| npm 近 30 天 | 4,752（含 CI 与镜像） |
| npm 版本 | `0.13.0` |
| 目录条目 | `data/plugins/Sivan757__dsh-agent-plugins-market.yml`（`market`） |

**为什么它过门槛**：npm 4,752 ≥ 3,000（★ 19 未过 200）。

**证据限制**：

- README 声称十种布局；代码追踪了 adapter 顺序与候选回退，但不是十种格式都由同一种完整 schema validator 检查。
- hook source/decision mapping 已读，测试包含 allow/ask/deny；未运行测试或挂载真实 host，因此 deny 对真实宿主权限的效果未作行为保证。
- README UI、第一方来源、桌面端/各 workspace 实际表现均未启动验证。
- ★ 19 与 npm 4,752 是不同来源的采用信号，下载含 CI/镜像，不能推断用户数或证明功能有效。

---

## 5. 可迁移洞察

| 触发问题 | 可迁移洞察 | 机制依据 | 为什么有效 / 代价 | 移植时改什么 | 成立边界 | 抄错后果 |
|---|---|---|---|---|---|---|
| 多来源、多方言的外部资产要成为商品 | 当目录可能并存多个 manifest 时，用有序 adapter registry 和候选级 diagnostics/fallback，不用散落的 `if/else`。 | `[SRC-TARGET]` `layouts.ts`、`manifests.ts`；runtime schema 只验证 Agent Plugins v1 1.0/1.1（memo §主链 4–5）。 | 优先级可审计，坏候选不必遮蔽低优先级格式；代价是维护 adapter order、schema version 和失败粒度。 | 定义方言清单、优先级、schema owner 与 `fatal/ignore/skip resource` 结果。 | README 的“十种布局”不等于十种都同等验证/保真。 | 把兼容宣传当统一 validator 证明，会高估跨生态语义保真。 |
| Source 会刷新，但用户期望安装内容稳定 | 分开 source checkout revision、suite install record 和启用状态；要承诺固定版本，必须把实际运行内容 pin 到不可变快照，而非只记录 `lockCommit`。 | `[SRC-TARGET]` refresh 更新受管 checkout；install 保存 Git HEAD/archive digest；未见 refresh 后 pin 或 rollback（memo §主链 2–3、6）。 | 及时跟上游；代价是已安装 suite 可能随 source refresh 改变。 | 选 immutable snapshot 或声明 live-follow；定义审计 hash 与回滚记录。 | 本次静态复核未运行 refresh。 | 把安装时 digest 当冻结，会产生虚假的供应链保证。 |
| 安装与 workspace 开关被混为同一作用域 | 分开建模 user-scoped suite install/enable、project discovery 与 workspace resource filters。 | `[SRC-TARGET]` user `state.json`、project `.dsh/agent-plugins`、`ResourceFilterService` workspace path（memo §主链 7–8）。 | 避免把“可见/过滤”误当安装所有权；代价是 UI 要展示多种 scope。 | 明确每状态 owner、key、默认值、跨项目持久性和切换动作。 | 安装记录本身是 user-dimension，并非 per-workspace。 | 把全局 install 状态当 workspace 隔离，会造成项目间意外暴露。 |
| 某套件的一项声明损坏 | 按 artifact 定义失败原子性：manifest、MCP file、MCP server 可有不同 fatal/ignore/disable/skip 行为，并展示诊断。 | `[SRC-TARGET]` validate/resolvers：manifest verdict、MCP file 级 disable、server 级 skip（memo §主链 4–5）。 | 无关资源可继续用；代价是规则更细且需说明部分可用状态。 | 按风险定义 artifact boundary、failure code、UI 汇总与恢复动作。 | 不能笼统声称“任何坏声明都整套件 fail-closed”。 | 过度原子失败会丢有效资源；过度继续会漏危险配置。 |
| MCP 远程凭据缺失或 401 | 区分 env reference missing、OAuth pending/denied、grant persisted 与 memory-only；状态指向对应 credential owner。 | `[SRC-TARGET]` `mcp-credentials.ts` / OAuth store；`[SRC-DSH]` rc.3 credential contract；无 `ctx.credentials` 时 OAuth 仅进程内（memo §Credentials）。 | 把“未配置”与“未授权”分开并给下一步；代价是记录 client/token、PKCE verifier 有不同生命周期。 | 定义 record key、写入原子性、撤销、重授权、外部删除后的 stale memory 行为。 | 本次没跑真实 OAuth；SDK `auth()` 内部未独立审计。 | 宣称 token 总持久化会令重启后授权丢失难排。 |
| Hook 既能观察又能控制代理 | 明确 hook event/decision mapping、timeout/error containment 与每次授权检查；dry-run 只能预览脚本，不得称 sandbox。 | `[SRC-TARGET]` `extension-hooks.ts` / `hook-dry-run.ts`；`[TEST]` ask/deny/halt/live authorization（memo §Hooks）。 | 决策有契约，坏返回可限域；代价是还受 host decision 支持范围约束。 | 按宿主定义决策映射、授权复核时点与真实隔离执行器。 | 本次未验证 shell executor 的文件/进程权限或真实 hook 交互。 | 把 dry-run 预览当隔离会允许脚本在用户权限下实际运行。 |
| 卸载 suite 或 source | 分别处理 install record、managed checkout 与 external local path；默认只删除本工具拥有的记录/资产，物理删 checkout 须明确选择。 | `[SRC-TARGET]` `InstallStore.uninstall()` / `SourceStore.remove()` ownership（memo §Credentials/hooks/ownership）。 | 降低误删用户 checkout 风险；代价是需说明卸载后的残留所有权。 | 明确 path owner、adopted checkout 删除提示、残留清理和恢复路径。 | 显式 `deleteCheckout` 可删除受管 `.sources`；不能写成“来源永不删除”。 | 无边界删除会删用户 clone；完全不清理则留下敏感/过期资产。 |

---

## 6. 失效条件与降级

| 触发 | 固定版本实现/边界 | 用户可见状态或剩余风险 |
|---|---|---|
| 多个 manifest / 某 adapter 不认识或失败 | 按 adapter priority 候选读取，失败写 diagnostics 后试下个；所有候选结束才形成 scan result。 | 低优先级格式可能接管解析；十种布局不等于都完整保真。 |
| v1 manifest schema/extension 不合约 | 某些 top-level/namespace 违规记 ignored；其他 manifest 违规 fatal。 | 错误类型会影响 suite 呈现，需展示具体 diagnostics。 |
| MCP file 有错 / 单 server 有错 | 文件级可关闭该 suite MCP 面；单 server 错可只跳过 server；URL/path 有独立边界验证。 | 不是“全 suite 原子失败”；部分功能可缺席。 |
| `${ENV}` credential 缺失 | server 状态为 `missing-credential`，不给空字符串冒充配置。 | OAuth authorization 状态另行跟踪；store 缺失时成功 token 不跨进程。 |
| OAuth deny/timeout/callback error | 明确错误状态、5 分钟窗口；connection supervisor 等待审批后重连。 | 本次未运行 callback；外部删除 persisted grant 后的 live in-memory state 是 `[OPEN]`。 |
| 自动刷新关闭 / checkout refresh | 6 小时刷新是 opt-in；refresh 更新受管 checkout，adopted checkout 和 external local path 有不同 ownership。 | `lockCommit` 不冻结 refresh；需要可重现版本时要额外 pin snapshot。 |
| suite uninstall / source removal | uninstall 删除 install entry；source removal 默认保留 checkout；只有显式 deleteCheckout 才删受管 `.sources`。 | 外部 local path 不删；用户仍需理解 install/source/files 的区别。 |
| hook dry-run | 在 user home host shell 执行，`dry_run` 是 script input，不是 sandbox。 | 运行外部 hook 的权限边界本次未实测，不能显示“安全预演”承诺。 |
| current `state.json` 损坏/版本异常 | `loadState()` 退回 empty state，后续 mutation 可能覆盖原状态；未发现 current-state backup/restore。 | 卡片要把数据损失风险标明，不能泛称“可恢复”。 |
| profile workspace 变化 | suite install state 是用户维度；project scan 与 workspace surface filter 另有 scope。 | profile/cwd 到 runtime workspace 的映射本次未在实机验证。 |

---

## 7. 开放问题

- [ ] `[OPEN]` 十种布局逐一的 fidelity、缺失字段行为和 version coverage 尚未与 layout report、parser tests 对照。
- [ ] `[OPEN]` hooks `deny/allow/ask` 如何与 DSH host gate 组合；unsupported deny event 在 rc.3 上的 UX/permission result 未测。
- [ ] `[OPEN]` 任意 Git source 的 signature/review/pin/update-before diff、malicious hooks 与 rollback；dry-run 只是执行输入标记，不是 isolation。
- [ ] `[OPEN]` 项目级 `.dsh/agent-plugins`、`~/.agents`、DSH profile skills 的覆盖优先级与 duplicate identity 未验证。
- [ ] `[OPEN]` `state.json` corruption/version mismatch fallback-empty 的数据恢复路径；外部 credential record 被删后 live OAuth provider 何时丢弃缓存。
- [ ] `[OBS]` 跨生态 suite 入口的长期价值，取决于来源更新是否改变已安装内容、workspace scope 和执行权限是否让用户能预测。
