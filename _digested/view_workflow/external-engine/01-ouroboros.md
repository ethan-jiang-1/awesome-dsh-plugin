# ouroboros — 24 行 YAML 的接线器，替一台 39 万行 Python 引擎在 DSH 里开门

> 证据等级:★★★(源码级;`Q00/ouroboros@c0a64b7d1b3fd792a2ffe13aedcb3e65c96fbc8b`,2026-11-18)。
> 数据截止 `29b3ed46e`(2026-11-17)。⚠ 星标 5565 为 2026-08-19 历史采样。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `Q00/ouroboros#integrations/dsh-plugin`（[registry](../../../data/plugins/Q00__ouroboros--integrations-dsh-plugin.yml)） |
| 类目 | workflow（[census](../../ecosystem/census.py) 703 条 / 全表 11 744 条） |
| 子分类 | `external-engine`（挂外部引擎）——本册中该形态最纯的样本 |
| 自述 | 纯配置包，经 DSH MCP 客户端挂载 Ouroboros，暴露 36 个访谈/Seed/执行/评估/演化工具 |
| 星标 ⚠ | **5565**（2026-08-19 采样；2026-11-18 实时 6375）；类内第一，第二名 tong-io/tongflow 860（6.5 倍） |
| 扩散 | **0**（全表 11 744 条中仅 1 条提及 ouroboros，即它自己） |
| 仓库 commit | `c0a64b7`，2026-11-18，`chore(release): prepare v0.61.1 (#3038)`；仓库创建于 2026-01-14 |
| 包形态 | pnpm/Cordis **bundle**：`package.json` 的 `dsh.bundle.patch` 指向 `cordis.patch.yml`，只声明一行 `@deepseek-ai/dsh-mcp-client`。npm 无 `dsh-ouroboros`（404），只能从 GitHub 子目录装 |
| 适配层代码规模 | **DSH 方向 0 行代码**：`cordis.patch.yml` 97 行（其中有效配置 24 行）+ `package.json` 28 行 + `README.md` 128 行 = 253 行。反向的 DSH 后端另有 ~457 行 Python（`dsh_acp_client.py` 152 + `dsh_llm_adapter.py` 305）+ 370 行测试 |
| 主项目体量 | `src/` 811 个 Python 文件 / **391 478 行**；全仓 2431 个 git 文件；PyPI `ouroboros-ai` 0.61.1 |

## 它到底是什么

**一句话：它不是一个插件，是一条"从 DSH 指向 PyPI 包"的指针。**

`integrations/dsh-plugin/README.md:10` 自己说得很清楚："This is a **config-only bundle**: it contains no custom plugin code, just one row that mounts dsh's existing `@deepseek-ai/dsh-mcp-client` against `ouroboros mcp serve`." 源码核对成立：整个目录只有三个文件，没有 `.ts`、没有 `src/`、没有 build 产物，`package.json:19` 的 `files` 只列 `cordis.patch.yml` 和 `README.md`。

**"纯配置"配置了什么**（`cordis.patch.yml:43-97`，全文唯一的 `insert`）：

- `id: mcp-ouroboros`、`name: '@deepseek-ai/dsh-mcp-client'`——用的是 DSH 自带插件，不是自研插件（:44-45）；
- `serverName: ouroboros`、`transport: stdio`（:47-48）；
- `command: uvx` + `args: [--from, 'ouroboros-ai[mcp]', --with, 'mcp==2.3.0', ouroboros, mcp, serve]`（:49-57）——**除这行 args 外没有一行逻辑**，子进程拉起来就是全部"集成"；
- `env`：6 个变量，全部是 `!!js process.env.X ?? ''` 形式的显式转发（:80-86）；
- `toolCallTimeoutMs: 1800000`（30 分钟，:90）、`failOnStartupError: false`（:97）。

**36 个工具从哪来**：全部来自独立的 Python 进程，DSH 侧一个都没实现。`ouroboros mcp serve` 的组合根 `src/ouroboros/mcp/server/adapter.py:1487` `create_ouroboros_server()` 在 :2396 起组装 `tool_handlers` 列表，含 `execute_seed`、`start_execute_seed`、`auto`/`start_auto`、`interview`、`generate_seed`、`evaluate`/`start_evaluate`、`checklist_verify`、`lateral_think`、`evolve_step`/`start_evolve_step`、`ralph`/`start_ralph`、`lineage_status`、`evolve_rewind`、`job_*`、`query_events`、`query_projection`、`project_status`、`brownfield`、`record_conductor_decision`、`session_signal`/`session_signal_targets`、`cancel_*`、`ac_dashboard`、`ac_tree_hud` 等；`*create_qa_handlers(...)` 再展开 2 个（`qa_background.py:126,135` 返回 `(QAHandler, StartQAHandler)`）。

我按括号深度静态数出 34–36 个，与 README/registry 的 36 一致；**但这是静态计数，未跑 `list_tools` 实测**（见"待验证"）。另一条装配路径 `definitions.py:459` 的 `get_ouroboros_tools()` 在 `include_auto=True` 时只返回 32 个具名 handler——同一批工具在不同入口有不同子集，所以"36"是 server 组合根的数，不是引擎的常数。

工具命名也不是 Ouroboros 定的，是 DSH 的 `mcp__<serverName>__<rawName>` 规则（`dsh-mcp-client/lib/index.js:58,97`）拼出来的 `mcp__ouroboros__ouroboros_interview`。注意这是双层前缀：DSH 命名空间 + Ouroboros 自己的 `ouroboros_` 前缀。

## 怎么接进 DSH

**挂载路径只有一条，且全部是 DSH 原生机制，没有一处是为本插件开放的特例**：

1. **分发**：`dsh plugin --profile <p> add "github:Q00/ouroboros#main&path:integrations/dsh-plugin"`（`README.md:34`）。`dsh plugin` 不是插件市场，`lib/bin.js:117` 显示它把剩余参数**转发给 pnpm**，`--profile` 是 `requiredOption`。所以 `#main&path:` 是 pnpm 的 git 子目录语法，DSH 侧没有任何"子目录插件"特判。
2. **识别为 profile 层**：靠 `package.json:23-27` 的 `dsh.bundle.patch`。`dsh-app-boot/lib/index.js:517-520` 校验它必须是字符串或字符串数组（否则抛 `dsh.bundle.patch must be a file path or a list of file paths`）；`dsh-plugin-manager/lib/index.js:313` 用它判断"这是不是 bundle"，`:336` 则对没有 `dsh.bundle` 的包警告 "installed as a plain dependency, not a profile layer"。这个键就是全部 manifest 契约。
3. **进程**：mcp-client 以 stdio 起 `uvx`，**需要独立进程**（Python ≥3.12；首次运行时 uvx 联网下载 `ouroboros-ai[mcp]`），**不需要端口、不需要常驻服务**。
4. **凭据**：DSH 的 subprocess 层确实会剥离 `/KEY|PASSWORD|SECRET|TOKEN/i` 与全部 `DSH_*`（`dsh-subprocess/lib/index.js:32`，`scrubbedParentEnv()` 在 :50），插件的显式 `env` 在剥离**之后**合并——所以那 6 行不是装饰，是唯一通道。
5. **失败不阻塞启动**：`failOnStartupError: false` 是 mcp-client schema 的真实默认（`dsh-mcp-client/lib/index.js:789`），bundle 只是显式写出；而 `toolCallTimeoutMs` 默认是 60 秒（:766 的 `6e4`），bundle 把它抬到 30 分钟（:788 的 schema 允许任意 number）。

一步到位的最小代价是 `uv` + 一条 `dsh plugin add`。**但这只是 dsh→Ouroboros 方向**；反方向的 `dsh` LLM 后端另需三个前置（见"代价与边界"）。

## 关键实现

**DSH 侧文件，逐个说清**：

| 文件 | 行数 | 作用 | 关键位置 |
|---|---|---|---|
| `integrations/dsh-plugin/cordis.patch.yml` | 97 | 唯一的机制载体：1 个 `insert`、1 行插件、6 个 env、2 个超时/容错开关 | :43 起；有效配置 24 行 |
| `integrations/dsh-plugin/package.json` | 28 | 让它被识别成 bundle；`files` 只发两个文件，刻意不带代码 | :19-27 |
| `integrations/dsh-plugin/README.md` | 128 | 安装、四个 env 的语义、`dsh` 后端的三个前置、启动失败与恢复 | :59-82, :105-116 |
| `tests/unit/integrations/test_dsh_plugin_bundle.py` | 153 | **8 个契约测试**，钉住配置与 DSH 现实的一致性 | :66-153 |
| `docs/guides/deepseek-harness.md` | 179 | 两个方向的官方说明（dsh→Ouroboros 装插件；Ouroboros→dsh 配 LLM 后端） | :9-16 |
| `docs/research/deepseek-harness-adoption.md` | 164 | 2026-08-15 的调研底稿，解释"为什么是这两种接法" | :66-115 |
| `src/ouroboros/providers/dsh_acp_client.py` | 152 | 反向：spawn `dsh-acp-demo --config`，缺配置即 `invalid_config` 失败关闭 | :105-125 |
| `src/ouroboros/providers/dsh_llm_adapter.py` | 305 | 反向：把 interview/seed/qa/evaluate 的**补全**调用交给 dsh；明确不支持工具型 runtime | 模块 docstring |
| `src/ouroboros/orchestrator/host_dispatch.py` | 812 | `host` runtime：park 住 `execute_task`，发 `host_action=spawn_subagents`，等宿主回传 | :1-47, :351 |
| `src/ouroboros/cli/commands/mcp.py` | — | `serve` 的 `--runtime` 含 `host`；继承到 `claude` SDK 时用 standin 顶替并警告 | :1463-1471, :1528-1552 |

那份测试值得单独说：它断言的不是 Python 行为，而是**配置与 DSH 现实的三个接缝**（文件头 :1-16 自述）：`--profile` 必须出现在每条发布的安装命令里（:135）、凭据必须显式转发（:97）、`dsh` 后端的两个前置必须跟着选择器一起走（:108）。还有一个 :147 的测试，断言 README 里必须写着 "Recovery is not automatic in general."——**用测试禁止文档许诺自动恢复**。把"文档诚实度"写成可执行断言，在这批插件里我是第一次见。

**数据流（三条，别混）**：

```
① dsh → Ouroboros（本 bundle，24 行）
   dsh 模型 ──mcp__ouroboros__ouroboros_interview──▶ mcp-client ──JSON-RPC/stdio──▶
   `ouroboros mcp serve`（独立 Python 进程）──▶ handler ──▶ EventStore(SQLite) + LLM + agent runtime

② 执行步骤（OUROBOROS_AGENT_RUNTIME 决定）
   host        : execute_task park → host_action=spawn_subagents → dsh 自己开 subagent → submit_fanout_results 回传
   claude-cli / codex / opencode : 由那个 CLI 干活，dsh 只在旁边等

③ Ouroboros → dsh（不是本 bundle；配 OUROBOROS_LLM_BACKEND=dsh）
   Ouroboros ──spawn──▶ dsh-acp-demo --config <绝对路径 cordis.yml> ──ACP──▶ dsh 的 LLM 层
```

②③ 才是真正的耦合点，而且都**不在** `integrations/dsh-plugin` 里：③ 在 `providers/`（457 行 Python），② 在 `orchestrator/host_dispatch.py`（812 行，注释 :13-14 明说 "Host-agnostic on purpose: nothing here names a concrete host. dsh is the first consumer, not the design target"）。**所以"DSH 集成"其实是三层：24 行 YAML（dsh→Ouroboros）+ 457 行 Python（Ouroboros→dsh）+ 812 行主机无关的 dispatch 协议（dsh 是首个消费者）。** 只读第一层会严重低估工作量；只读后两层会高估 DSH 的特殊性。

## 为什么它突出（以及为什么零衍生）

**先拆星标归属，这是本卡的核心。** GitHub 只有仓库级星标，registry 把 `Q00/ouroboros` 的 5565 记在它的一个**子目录条目**头上——这本身就是采样口径造成的错配。时间线是决定性的：

| 日期 | 事件 | 来源 |
|---|---|---|
| 2026-01-14 | 仓库创建 | GitHub API `created_at` |
| 2026-08-15 | #2143 `feat(providers): add DeepSeek Harness (dsh) ACP completion backend` | 该文件 commit 历史 |
| 2026-08-17 | #2158 `feat(integrations): add installable dsh plugin` | `integrations/dsh-plugin` 路径历史（共 4 个提交） |
| **2026-08-19** | **5565 星采样点** | registry ⚠ |
| 2026-08-24 | #2169 `host-driven execution runtime for MCP hosts` | `host_dispatch.py` 历史 |
| 2026-11-18 | 6375 星（实时）、0.61.1、3038 个 PR | GitHub API |

仓库在 DSH 相关代码出现前已经跑了 **7 个月**；三个 DSH 提交集中在 9 天内；采样点距第一个 DSH 提交 4 天、距插件提交 **2 天**。**5565 星里能归给 DSH 适配层的，最多是 2–4 天的增量。** 结论：这 5565 星属于主项目（一个支持 15 个 runtime 的 spec-first 工作流引擎，README:117-133 的 "Works with" 里 DSH 排在最后一位），不属于这层接线。

**再解释零衍生。四个理由，按解释力排序：**

1. **没有可仿制的代码。** 24 行有效 YAML，内容就是"调用 DSH 自带的 mcp-client，指向一个 PyPI 包"。仿制它 = 仿制一次 `insert`。它没有可扩展的 seam,也没有可复用的算法,24 行配置里没有被抄走的形状。第三方即便照抄，产出的也只是一行指向同一个 `ouroboros-ai` 的配置，**不构成新条目**。
2. **价值不在适配层，在引擎。** 要复现能力，得重写 391 478 行 Python，或依赖同一个 PyPI 包。于是衍生只剩两种形态：换个 harness 再包一次（无新意），或直接 fork 主项目（那不算插件衍生）。**适配层薄 → 抄了没用；引擎厚 → 抄不动。两头都堵死。**
3. **它是 vendor-published integration，不是 community primitive。** census ④ 显示 524/11 744（4.5%）命中 "MCP 协议"标签——"挂一个 stdio MCP server"是常规手法，不构成机制创新；`monorepo 子包条目` 也有 1205 条。第三方要提它，得先有理由讨论 Ouroboros 的**方法论**（访谈打分、Seed、隐藏 AC 判定），而那是产品讨论，不是插件生态讨论。
4. **门槛确实不低，但这只解释"没人用"，不解释"没人提"。** `uv` + Python 3.12 + 首次联网下载；想用 `dsh` LLM 后端还要从源码 build dsh（`README.md:66-70`，且明说 npm 上 `@deepseek-ai/dsh-acp-demo` 因 `dsh-tool-bash` 的 peer 依赖冲突装不上）。这个门槛压低采用率，但零**提及**是理由 1+3 的结果，不是理由 4。

**判断：明星，不是锚**（按本册两轴口径：声量极高、扩散为零），归属 `external-engine` 子分类，且**影响力应记在 Ouroboros 主项目名下，不记在 DSH 适配层**。它在 DSH 侧的位置，更接近**外来项目的官方接入点**，而不是本领域被认可的机制。

补充一个反直觉的细节：DSH 拿到的待遇其实不低——`.claude-plugin/`、`.codex-plugin/` 是 marketplace 形态，而 DSH 拿到了**原生 `dsh.bundle` 包**，比只有 runtime guide 的 Gemini/Kiro 等更正式。作者是认真接的，只是这层再认真也只有 24 行。workflow 类"一超多弱、超的那一个还不参与生态互动"的格局，本身就是这册最该记下的结论。

## 代价与边界

- **外部引擎依赖（最硬）**：DSH 侧没有任何降级实现，`uv` 不在 PATH 上就是 36 个工具全部消失；且 `--from 'ouroboros-ai[mcp]'` **不 pin 版本**（只 pin 了 `mcp==2.3.0`），每次首装/升级拿到的可能是不同 Ouroboros。想固定得自己在 profile 里覆写 `args`。
- **两个方向要分开配，文档还互相打架**：`docs/guides/deepseek-harness.md:47-52` 说"要一个可执行的 agent runtime（claude-cli/codex/opencode）"，而 `cordis.patch.yml:82` 的默认是 `host`（并在 :25-34 解释为什么）。同一仓库两处说法冲突，读者会以为必须先装一个 CLI。
- **`dsh` LLM 后端是"三个前置"**：绝对路径 composition（相对路径被 `dsh_acp_client.py:119-123` 显式拒绝，理由是会被解析到不可信的项目 cwd）、`dsh-acp-demo` 可执行、以及该 composition 指名的凭据。而且它 spawn 的是**另一个 dsh 进程**，不复用你正在用的这个。
- **失败模式，按发生顺序**：
  1. 无 `uv` → 静默降级，工具列表里干脆没有 `mcp__ouroboros__*`，dsh 其余功能正常。**published rc 没有重连循环**（`README.md:110-116`），修好原因后要重载插件或重启。
  2. `--runtime` 继承到 `claude`（SDK 型，MCP 进程里跑不了）→ 用 standin 顶替并在 stderr 打黄字（`mcp.py:1528-1552`）。宿主若吞掉 stderr，用户会看到一个"能列但不知道背后是谁"的工具集。
  3. `dsh` 后端缺配置 → `invalid_config` **失败关闭**，但**工具注册和列表照常**：`README.md:80-82` 直说 "the first interview/Seed/QA call is what fails"。**这是最阴的失败模式——看着能用，第一次调用才炸。**
  4. `ouroboros_auto` 同步跑完整条流水线，30 分钟超时；模型侧可能早就放弃这一轮。
  5. bundle **没有设 `cwd`**（mcp-client schema 的 `cwd` 默认 `""`，`lib/index.js:787`），server 的 `project_dir` 退化为进程 cwd（`adapter.py:1692` 的 `_safe_cwd()`）。产物落在哪个目录取决于 dsh 从哪儿启动——**待验证**在 `dsh web` 下是否等于会话工作区。
- **数据/隐私**：访谈、Seed、事件落本地 SQLite `EventStore`（`mcp.py` 的 `--db` 可覆盖），不出本机；凭据只转发 `ANTHROPIC_API_KEY` 与 `DEEPSEEK_API_KEY` 两个，是有意的短名单。但 uvx 首次联网从 PyPI 拉包，供应链面转移到 `ouroboros-ai` 与 `uv`；仓库还有 `TELEMETRY.md`（20 KB），**默认是否上报我未核实**（见"待验证"）。

## 可信度与复现

- **★★★（仅限本 bundle 与其 DSH 侧机制）**：253 行全读，逐条对照本机 DSH 安装包的实现（`dsh-app-boot` 的 `bundlePatchFiles`、`dsh-plugin-manager` 的 bundle 判定、`dsh-subprocess` 的 env 剥离、`dsh-mcp-client` 的命名/超时 schema）。
- **★★（36 这个数字）**：静态数出 34–36，与自述吻合，未跑运行时 `list_tools`。
- **未读**：Ouroboros 主引擎 391 478 行里的绝大部分——只读了 MCP 装配（`definitions.py`、`server/adapter.py` 局部）、`providers/dsh_*`、`cli/commands/mcp.py` 局部、`orchestrator/host_dispatch.py` 的 docstring 与关键行；`TELEMETRY.md`、`persistence/`、`interview/`、`evaluation/` 的判定逻辑均未读。**所以关于"引擎多强"的任何判断都只基于体量与装配层，不基于算法质量。**

```sh
# 1) 复现克隆与提交
git clone --depth 1 --filter=blob:none https://github.com/Q00/ouroboros.git /tmp/an-ouroboros
cd /tmp/an-ouroboros && git log -1 --format='%H %ad'
# → c0a64b7d1b3fd792a2ffe13aedcb3e65c96fbc8b 2026-11-18

# 2) 适配层就是三个文件、253 行
find integrations/dsh-plugin -type f | xargs wc -l
grep -vE '^\s*#|^\s*$' integrations/dsh-plugin/cordis.patch.yml | wc -l   # → 24

# 3) 零扩散（注意：data/plugins/*.yml 有 11 744 个文件，直接展开会
#    "Argument list too long"（我实测 exit 126）；必须用目录形式）
grep -ril ouroboros data/plugins/ | wc -l      # → 1（只有它自己）
grep -ril ouroboros data/plugins/ | head       # → data/plugins/Q00__ouroboros--integrations-dsh-plugin.yml

# 4) bundle 只有 4 个提交，DSH 相关工作集中在 2026-08-15 ~ 08-24
curl -s "https://api.github.com/repos/Q00/ouroboros/commits?path=integrations/dsh-plugin&per_page=20"

# 5) DSH 侧机制核实（本机安装的 dsh）
DSH=~/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh
grep -n 'SENSITIVE_ENV_PATTERN' $DSH/node_modules/@deepseek-ai/dsh-subprocess/lib/index.js
grep -n 'bundle.patch\|bundlePatchFiles' $DSH/node_modules/@deepseek-ai/dsh-app-boot/lib/index.js
grep -n 'requiredOption("--profile' $DSH/lib/bin.js
```

## 待验证

1. **36 的确切数字**：跑一次 `uvx --from 'ouroboros-ai[mcp]' --with 'mcp==2.3.0' ouroboros mcp serve` 后取 `tools/list`，或看 CLI 是否有 `ouroboros mcp tools --json`。静态计数在 34–36 之间，差的那 2 个可能就在 `create_qa_handlers` 的展开边界。
2. **5565 星在 2026-08-17 之前是多少**：需要 `stargazers` API 的 `starred_at`（未授权返回 401，我试过）或 star-history 曲线。拿到这个数，"星标与 DSH 无关"就从推断变成实测。
3. **uvx 首装体积与耗时**：`ouroboros-ai[mcp]` 的 wheel 大小、是否带 `crates/` 的产物。这决定"低门槛"的说法成立几分。
4. **产物落盘位置**：bundle 未设 `cwd`，需实测 `dsh web` 下 `project_dir` 是否等于会话工作区；否则 `ooo auto` 可能在错的目录里改文件。
5. **遥测默认值**：`TELEMETRY.md` 存在，是否 opt-in、上报什么，未读。
6. **`github:...#main&path:integrations/dsh-plugin` 的实际安装行为**：未实跑（会写入 profile）。pnpm 版本要求、`#main` 与 commit pin 的差异、升级后 `dsh.bundle` 是否被重新解析，都待验证。
7. **registry 之外的扩散**：GitHub 上搜 `dsh-ouroboros` fork/复刻，以及是否有第三方把 Ouroboros 的 MCP server 接进自己的插件。本卡的"0"只统计本 registry 的 11 744 条。
