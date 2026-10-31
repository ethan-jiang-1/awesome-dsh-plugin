# 样本溯源卡：精确到 repo@commit 的重新挖掘入口

> **状态**:`observed` · **抓取时间**:2026-10-31 14:00 CST · **基线**:DSH `0.2.1-rc.3` · 名单 7924 条 @ `efe602e7b`
> **用途**:本域所有卡片的断言都指向具体代码或 README。这张卡回答一个问题——**「三个月后我想再核一次,去哪儿挖?」**
> **纪律**:断言不附出处等于传闻。凡本卡标 `observed` 的机制,下面都给了 **repo + commit + 文件路径**;凡是**没有** commit 的,是当时没记、不可追回的(`[OPEN]`)。
> **一句话**:**没绑 commit 的抓取等于没抓。** 本域已经付出过两次代价(§2 的两条自曝)。

## 0. 怎么用

三种情况:

| 我想做什么 | 用哪一列 |
|---|---|
| 核对我记得的那段代码 | `锚点` 列:直接打开 `repo@commit:path` |
| 三个月后看它变了没 | `重抓` 列:一条 `curl` 命令拿最新 head 和本卡对比 |
| 自己装来试 | `安装` 列:目录里的**确切引用名**(⚠️ 有两个是 monorepo 子包,`#` 后面那段不能省) |
| 确认它是什么版本 | §6:`package.json` 实测的 npm 包名 / 版本 / 入口(`lib/index.js` 还是 `dsh/plugin.mjs`)/ 运行时约束 |

**提交被锁定是有意的**:一个浮动在 `main` 上的断言语义等于没有断言。所有 `@<sha>` 都是 **2026-10-31 抓到的 HEAD**,用它打开保证看到的是我读过的那一份。

**为什么不用 GitHub API**:本次抓取时 API 配额已耗尽(`60/60`,403)。提交 SHA 从 `https://github.com/<owner>/<repo>/commits/main.atom` 的 `Grit::Commit/<sha>` 提取,不需要 token。**下面的重抓命令都只用 atom / raw,可无限次复跑。**

---

## 1. 十二个主样本(立卡的)

### 1.1 `samirliu/dsh-goalloop-agentteams` — 完成声明硬门禁 → [02](./02-goal-gate-hard-floor.md)

| 项 | 值 |
|---|---|
| **repo** | https://github.com/samirliu/dsh-goalloop-agentteams |
| **commit** | `6b4b1fad8cd61f98e6eedbb4f12ed10b5dc93f17`(2026-10-19) |
| **目录引用名** | `samirliu/dsh-goalloop-agentteams` · category `agi` |
| **版本** | v0.9.2 · tarball `releases/download/v0.9.2/dsh-goalloop-agentteams-0.9.2.tgz` |
| **安装** | `dsh plugin add samirliu/dsh-goalloop-agentteams` |
| **锚点** | 实现逻辑在打包产物 `lib/index.js`(本卡读的是这一份,已抓存 `/tmp/prove-src/goalloop-lib-index.js`);源码布局 `package.json` 声明的 `main`/`exports` 决定 |
| **重抓** | `curl -sS https://raw.githubusercontent.com/samirliu/dsh-goalloop-agentteams/6b4b1fa/README.md`<br>`curl -sS https://github.com/samirliu/dsh-goalloop-agentteams/commits/main.atom \| grep -oE 'Grit::Commit/[0-9a-f]{40}' \| head -1` |
| **已核的关键符号** | `NO_PROGRESS_TURNS = 4`、`time-budget` / `rounds-exhausted` 两种退出、`contract-revised` deny、`false-completes=2 ≥ 2`、`treeDigest` 绑定、7 种 deny code |
| **注意** | 名字里的 `agentteams` 容易让人以为它只服务多 agent;实测它有 `strict` / `goal-only` 两种作用域模式,**单 agent 也能用** |

### 1.2 `rootsbymenda/dsh-second-angle` — 轮末对账 → [03](./03-turn-end-reconciliation.md)

| 项 | 值 |
|---|---|
| **repo** | https://github.com/rootsbymenda/dsh-second-angle |
| **commit** | `9ac01ed3ebe3e6f0e2ebf6dcf5ab773cbdbd2fdd`(2026-10-27) |
| **目录引用名** | `rootsbymenda/dsh-second-angle` · category `agi` |
| **版本** | v0.1.0 · tarball `releases/download/v0.1.0/dsh-second-angle-0.1.0.tgz` |
| **安装** | `dsh plugin add rootsbymenda/dsh-second-angle` |
| **锚点** | `README.md`(抓存为 `/tmp/prove-src/rootsbymenda_dsh-second-angle.md`);源码曾另抓一份 `/tmp/prove-src/second-angle-src.mjs`,**该文件未与 commit 绑定,视为 `[OPEN]`** |
| **重抓** | `curl -sS https://raw.githubusercontent.com/rootsbymenda/dsh-second-angle/9ac01ed/README.md` |
| **已核的关键符号** | `requireQuoteForSteer`(默认 true)、`sync` / `block` / `async` 三模式、`maxLatencyMs`、`CONTRADICTED` / `OVERSTATED` / `UNSUPPORTED` / `CLEAN` 四判决、24 例评测表(7/8·8/8·8/8·0/8·3.6 s;`auditorReasoningEffort: low` → 8/8·5.85 s) |
| **注意** | 版本号 `0.1.0` 说明它很年轻;**24 例评测是作者自建,不是第三方复现**(作者自己列了四条局限) |

### 1.3 `AaronandWork/dsh-evidence-gate` — 证据索引防误杀阶梯 → [04](./04-evidence-index.md)

| 项 | 值 |
|---|---|
| **repo** | https://github.com/AaronandWork/dsh-evidence-gate |
| **commit** | `845ddf415e045eb6b2a014bca97a9c63aee1befa`(2026-09-12) |
| **目录引用名** | `AaronandWork/dsh-evidence-gate` · category `dev` |
| **版本** | tarball 为 `releases/latest/download/dsh-evidence-gate.tgz`(**浮动标签,无固定版本号**) |
| **安装** | `dsh plugin add AaronandWork/dsh-evidence-gate` |
| **锚点** | `README.md`(抓存 `/tmp/prove-src/AaronandWork_dsh-evidence-gate__main__README.md`) |
| **重抓** | `curl -sS https://raw.githubusercontent.com/AaronandWork/dsh-evidence-gate/845ddf4/README.md` |
| **已核的关键符号** | 五级阶梯(本会话 → 输出关键词 → 跨会话 → 存在性兜底 → block)、三个指标 `blocked` / `converted` / `charity`、`systemPrompt.section` order `550`、400 条索引上限、top-50 会话、`store.json` 落 `DSH_HOME`、64KB 同源 JSON 桥 |
| **注意** | 台账样例 `blocked 5 · converted 3` 是 README 里的示例,**不是可复现的基准**;`--probe "evidence.?gate\|实证"` 全库仅 **11/7924** |

### 1.4 `030611/qiushi-dsh-evidence-audit` — 哈希链保管 → [05](./05-custody-chain.md)

| 项 | 值 |
|---|---|
| **repo** | https://github.com/030611/qiushi-dsh-evidence-audit |
| **commit** | `94fae130b2845309e1dcabac14696fddb18f8f3a`(2026-08-14) |
| **目录引用名** | `030611/qiushi-dsh-evidence-audit` · category `security` |
| **下载量** | 163(名单快照 2026-08-19) |
| **安装** | `dsh plugin add 030611/qiushi-dsh-evidence-audit` |
| **锚点** | `README.md`(抓存 `/tmp/prove-src/030611_qiushi-dsh-evidence-audit__main__README.md`);`src/` 下有实现,`tests/` 下是那张工程诚实度清单对应的测试 |
| **重抓** | `curl -sS https://raw.githubusercontent.com/030611/qiushi-dsh-evidence-audit/94fae13/README.md` |
| **已核的关键符号** | `Integrity detection boundaries` 表(删整个文件 No / 删尾部 No / 重链 No)、`0700/0600`、`$DSH_HOME/evidence-audit/evidence-receipts.jsonl`、**只存哈希不存正文**、测试清单 17 项 |
| **注意** | 提交日期 08-14 是全部样本里**最老的**;README 明确说恢复依赖 `@deepseek-ai/dsh-session-checkpoint-policy` 的 all-or-nothing 恢复 |

### 1.5 `zhengqiuyang/dsh-attest-chain` — 签名链对照 → [05](./05-custody-chain.md) §6

| 项 | 值 |
|---|---|
| **repo** | https://github.com/zhengqiuyang/dsh-attest-chain |
| **commit** | `bf837787c304f73c03b4bdd2fd331d8796ffd02f`(2026-10-19) |
| **目录引用名** | `zhengqiuyang/dsh-attest-chain` · category `security` |
| **安装** | `dsh plugin add zhengqiuyang/dsh-attest-chain` |
| **锚点** | `README.md`(抓存 `/tmp/prove-src/zhengqiuyang_dsh-attest-chain.md`) |
| **重抓** | `curl -sS https://raw.githubusercontent.com/zhengqiuyang/dsh-attest-chain/bf83778/README.md` |
| **已核的关键符号** | sha256 + ed25519、`.dsh-attest-chain/keys/` 须 gitignore、`sign: false` 退化、从 shell 输出提取 commit SHA、`verifyChain()` 返回首个坏点 `{seq, reason}`、**Kill criteria** 一节 |
| **注意** | 它是本域**唯一自带退役条件**的样本;同作者的 UI 侧调用方未在本域考察 |

### 1.6 `bycall/dsh-answer-reviewer` — 判官位置主样本 → [06](./06-judge-placement.md)

| 项 | 值 |
|---|---|
| **repo** | https://github.com/bycall/dsh-answer-reviewer |
| **commit** | `8c6186acb2246dbf3bbea27fd01643a8170141b0`(2026-09-29) |
| **目录引用名** | **`dsh-answer-reviewer`**(⚠️ 目录里 `name` 字段没有 owner 前缀,与 `url` 不一致——按 `url` 走) |
| **星标** | ★10 |
| **安装** | `dsh plugin add bycall/dsh-answer-reviewer` |
| **锚点** | `README.md`(抓存 `/tmp/prove-src/bycall_dsh-answer-reviewer__main__README.md`) |
| **重抓** | `curl -sS https://raw.githubusercontent.com/bycall/dsh-answer-reviewer/8c6186a/README.md` |
| **已核的关键符号** | `source.kind === 'plugin'` 过滤、绑 `assistant/message → data.message.id`、chip `● 评分 92` / `第2次` / `capped`、`threshold` 80(1–100)、`maxChallenges` 5(硬上限 8)、解析失败 fail-closed、sidecar 刻意不开跨源读、`.dark` CSS 事故 |
| **注意** | `[CAT]` 里的 `name` 字段缺 owner,`--probe` 按描述文本匹配,**不会**用 `name` 匹配——所以检索时用「评分 / reviewer / 挑战」而不是仓库名 |

### 1.7 `CAI-MH/dsh-quality-review` — 多维评审 + SOP 目录 → [06](./06-judge-placement.md) §6

| 项 | 值 |
|---|---|
| **repo** | https://github.com/CAI-MH/dsh-quality-review |
| **commit** | `7c5a67ddc76e91d2a87725fabb23a04b80370f3b`(2026-09-10) |
| **目录引用名** | `CAI-MH/dsh-quality-review` · category `agi` |
| **星标** | ★2 · fork 1 |
| **安装** | `dsh plugin add CAI-MH/dsh-quality-review` |
| **锚点** | `README.zh.md`(抓存 `/tmp/prove-src/CAI-MH_dsh-quality-review__main__README.zh.md`,4805 B) |
| **重抓** | `curl -sS https://raw.githubusercontent.com/CAI-MH/dsh-quality-review/7c5a67d/README.zh.md` |
| **已核的关键符号** | 四维(事实准确/完整/逻辑一致/指令遵循)、SOP 目录(文件名即关键词、命中即加载**整个目录**、每轮重扫)、`maxRounds` 2(上限 5)、`exemptPatterns`、嵌入 token |
| **注意** | README **只有中文版有细节**(英文版 3.4 KB,中文版 4.8 KB);用 `--probe` 搜英文关键词会漏 |

### 1.8 `XiaoOu2024/dsh-self-review` — 唯一能改用户所见文本 → [06](./06-judge-placement.md) §6(反例格)

| 项 | 值 |
|---|---|
| **repo** | https://github.com/XiaoOu2024/dsh-self-review |
| **commit** | `a903dffb60f7bede646063a1c0fa5dc883de842a`(2026-10-25) |
| **目录引用名** | `XiaoOu2024/dsh-self-review` · category `usage` |
| **安装** | `dsh plugin add XiaoOu2024/dsh-self-review` |
| **锚点** | `README.md`(抓存 `/tmp/prove-src/XiaoOu2024_dsh-self-review.md`) |
| **重抓** | `curl -sS https://raw.githubusercontent.com/XiaoOu2024/dsh-self-review/a903dff/README.md` |
| **已核的关键符号** | `llm/stream` 扣留重写、任何错误 **fail-open**、`minChars` 120 / `maxChars` 30000 / `timeoutMs` 60000、2–12 s、`turn-stopping` payload 只有 `{agent, turn, signal}`(反证引文) |
| **注意** | 这是本域**唯一一个能动用户所见文本**的样本;`llm/stream` 全库只有 **7/7924** 条 |

### 1.9 `263311487-ux/dsh-verify` — 换运行时验收 → [07](./07-foreign-runtime-acceptance.md)

| 项 | 值 |
|---|---|
| **repo** | https://github.com/263311487-ux/dsh-verify |
| **commit** | `e7ce6376fec8cf94f41ce46264baeb348911693b`(2026-10-28,**全部样本里最新**) |
| **目录引用名** | `263311487-ux/dsh-verify` · category `browser` |
| **星标 / 下载** | ★2 · 2088 dl(名单快照 2026-08-19) |
| **安装** | `dsh plugin add 263311487-ux/dsh-verify` |
| **锚点** | `README.md`(抓存 `/tmp/prove-src/263311487-ux_dsh-verify__main__README.md`);`tests/` 有实现测试;另有 `server.json` / `glama.json`(MCP 与目录元数据) |
| **重抓** | `curl -sS https://raw.githubusercontent.com/263311487-ux/dsh-verify/e7ce637/README.md` |
| **已核的关键符号** | JSON spec 顶层 `title`/`serve`/`base`/`browser`/`steps`、退出码 `0`/`1`、`--json`、`--update-baselines`、Playwright Chromium/Firefox/WebKit、`expect_text #total: got "0" want "99"`、`generate_and_verify`(「AI drafts; it never judges」)、四条「不」 |
| **注意** | 2088 下载是本域最高,但**它不证明规格写对**;README 自述「review the spec separately」 |

### 1.10 `4444wjt/dsh-plugin-veriscope` — 三值判决 → [07](./07-foreign-runtime-acceptance.md) §6

| 项 | 值 |
|---|---|
| **repo** | https://github.com/4444wjt/dsh-plugin-veriscope |
| **commit** | `5299b64087bbfa5beef6ae2e336045468f1af01d`(2026-10-18) |
| **目录引用名** | `4444wjt/dsh-plugin-veriscope` · category `tools` |
| **安装** | `dsh plugin add 4444wjt/dsh-plugin-veriscope` |
| **锚点** | `README.md`(抓存 `/tmp/prove-src/4444wjt_dsh-plugin-veriscope__main__README.md`,22 KB) |
| **重抓** | `curl -sS https://raw.githubusercontent.com/4444wjt/dsh-plugin-veriscope/5299b64/README.md` |
| **已核的关键符号** | `PASS`/`FAIL`/`REVIEW`、**REVIEW 永不转 PASS**、`row_threshold`、精确十进制比较、`gate_complete` 只在当前有效 PASS 时返回、回执随 GatePolicy/输入/环境失效、纯 Node 不启浏览器不调模型 |
| **注意** | `--probe "通过／失败／待复核\|PASS.{0,10}FAIL.{0,10}REVIEW"` 全库仅 **1/7924**——就是它自己 |

### 1.11 `oxmumu3/dsh-workproof` — 交付回执 → [08](./08-delivery-receipt.md)

| 项 | 值 |
|---|---|
| **repo(真身)** | https://github.com/oxmumu3/dsh-workproof —— **monorepo**,插件在子包 |
| **commit** | `7096ead2ca6a6f8ae611889b21749babd85b031d`(2026-10-27) |
| **目录引用名** | `oxmumu3/dsh-workproof#dsh-delivery-receipts`(⚠️ URL 带 `/tree/main/packages/dsh-delivery-receipts`) |
| **子包路径** | `packages/dsh-delivery-receipts/` —— **要挖代码必须进这个目录,根目录只有 README + lockfile** |
| **同仓其他子包** | `packages/dsh-evidence-ledger/`(目录里也单独列了一条,**本域未考察**,`[OPEN]`) |
| **安装** | `dsh plugin add oxmumu3/dsh-workproof#dsh-delivery-receipts` |
| **锚点** | 根 `README.md`(抓存 `/tmp/prove-src/oxmumu3_dsh-workproof__main__README.md`)+ 子包 README(抓存 `/tmp/prove-src/wp-receipts.md`,148 行) |
| **重抓** | `curl -sS https://raw.githubusercontent.com/oxmumu3/dsh-workproof/7096ead/packages/dsh-delivery-receipts/README.md` |
| **已核的关键符号** | 三层分离(代理声称/文件观测/用户决定)、`record→inspect→review_required→accepted\|changes_requested`、`stale`/`missing`/`unverifiable`、**无 `decide` 动作**、重检不替换基线、20 路径/100 回执/100 审计事件/64 MiB/64 KiB、`/tmp`→`/private/tmp` 规范化、peer `(0.2.0-rc.2 \|\| 0.2.1-rc.3)`、仅 macOS e2e |
| **注意** | 根 README 与子包 README 内容**不同**;本卡断言以子包那份为准。`--probe "回执\|receipt"` **28/7924** 噪声大 |

### 1.12 `PerryLink/dsh-doublecheck` — 纪律环 → [09](./09-discipline-loop.md)

| 项 | 值 |
|---|---|
| **repo** | https://github.com/PerryLink/dsh-doublecheck |
| **commit** | `22fe2e0d58336f7c5dbe5fac8666d73206e71a57`(2026-10-26) |
| **目录引用名** | `PerryLink/dsh-doublecheck` · category `workflow` |
| **星标 / 下载** | ★59 · 611 dl(**本域影响力最高**) |
| **安装** | `dsh plugin add PerryLink/dsh-doublecheck` |
| **锚点(最重要的一行)** | `src/guard/prose.ts:191-192`、`src/guard/command.ts:156`、`tests/command.spec.ts:201-208`(三处**已在 22fe2e0 上逐一核对通过**) |
| **⚠️ 路径陷阱** | doublecheck 自己的 README 写的是 `Observed from plugins/dsh-doublecheck/src/guard/prose.ts:191-192`——**这个 `plugins/` 前缀是它作者内部 monorepo 的布局,公开仓库里没有这一层**。按 README 抄路径会 404。实测:`plugins/...` 版返回 **404**,`src/guard/prose.ts` 版返回 **200** |
| **其他文件** | `src/` · `lib/` · `tests/` · `scripts/` · `strict.patch.yml` · `capture.json` · `screenshots.json` · `README-zh.md`(仓库根**同时**有 `src/` 与 `plugins/` 之外的其他目录,但代码在根 `src/`) |
| **重抓** | `curl -sS https://raw.githubusercontent.com/PerryLink/dsh-doublecheck/22fe2e0/README.md`<br>`curl -sS https://raw.githubusercontent.com/PerryLink/dsh-doublecheck/22fe2e0/src/guard/prose.ts \| sed -n '188,194p'` |
| **已核的关键符号** | 六阶段 grill→design→red→green→review→verify、`testToolNames`/`testCommandPatterns`/`testFilePatterns`/`guardTools`/`vagueTaskMaxChars 200`/`remindOnce`、`verifyProvider: 'fork'`、`verifyMode: 'all'`、`intensity` 默认 `remind` + `strict.patch.yml`、`Verdict: rework required — 2 red item(s)` |
| **注意** | `--probe "纪律\|discipline\|grill\|审讯"` **25/7924**;★59 是本域最高,但它的机制深度与星数**不成正比**(最深的 goalloop 只有 ★1) |

---

## 2. 只作一行引用的样本(不立卡,但要能挖回去)

| 样本 | repo@commit | 目录引用名 | 用于 | 重抓 |
|---|---|---|---|---|
| `1052326311/dsh-plan-lattice` | `ea4d4f7d726681466e86d11f93e4cc38a6c0d3f3`(08-31) | `1052326311/dsh-plan-lattice` · `workflow` · v0.3.0 · ★3 | [09](./09-discipline-loop.md) B 级对照(计划环自建合同) | `curl -sS https://raw.githubusercontent.com/1052326311/dsh-plan-lattice/ea4d4f7/README.md` |
| `Jonah-Wu23/dsh-gungnir` | `4038c3e3d8fcb2532c59242f39a3419a9c9a36e9`(10-27) | `Jonah-Wu23/dsh-gungnir#dsh-plugin`(⚠️ 子包 `packages/dsh-plugin`)· `agi` · ★6 | [02](./02-goal-gate-hard-floor.md) §6 对照(`/ultragoal` 锁目标) | `curl -sS https://raw.githubusercontent.com/Jonah-Wu23/dsh-gungnir/4038c3e/packages/dsh-plugin/README.md` |
| `JayYuen666/dsh-quality-gate` | `abb6266df1876d8f8fea4752bd0404e53a1e4c42`(10-29) | `JayYuen666/dsh-quality-gate` · `dev` | [01](./01-quality-chain.md)/[02](./02-goal-gate-hard-floor.md) 的异常路径对照 | `curl -sS https://raw.githubusercontent.com/JayYuen666/dsh-quality-gate/abb6266/README.md` |
| `1687210989/agent-clinic` | `e88d6ec63d7a67277bf3c6c86f38a43ee97527c4`(10-15) | `1687210989/agent-clinic` · `usage` · ★1 | [01](./01-quality-chain.md) 做法 B(22 项诊断 + `#L<a>-L<b>` 定位符 + 处方) | `curl -sS https://raw.githubusercontent.com/1687210989/agent-clinic/e88d6ec/README.md` |
| `863683348/dsh-plugin-gate` | `b75c3a1b768448ee84a6fa07735206e6f8945411`(09-11) | `863683348/dsh-plugin-gate` · `security` · ★1 f2 · MIT · npm `dsh-plugin-gate` | 未进卡;[`draw-limit`](../lever-draw-limit/README.md) 边界参考 | `curl -sS https://raw.githubusercontent.com/863683348/dsh-plugin-gate/b75c3a1/README.md` |
| `guo6x/dsh-shipcheck` | 未绑定 `[OPEN]`(仅 README 抓存) | 目录内 | 未进卡(交付前检查,与 [09](./09-discipline-loop.md) 重叠) | 无 commit,不可追溯 |

> **两条自曝**:`guo6x/dsh-shipcheck` 当时抓了 README 但没记 commit,现在**追不回来**;`second-angle` 的 `second-angle-src.mjs` 同理。**这就是为什么这张卡存在**——没绑 commit 的抓取,等于没抓。

---

## 3. 官方包(原生侧,来源是本机安装目录)

原生侧断言全部来自本机安装的 DSH 包 README,不是 GitHub:

| 包 | 路径(相对 `$DSH_NODE_MODULES/@deepseek-ai/`) | 已引用的行 |
|---|---|---|
| `dsh-agent` | `dsh-agent/README.md` | `:47` `:67` |
| `dsh-llm` | `dsh-llm/README.md` | `:127` |
| `dsh-tool-goal` | `dsh-tool-goal/README.md` | `:55` `:57` `:116` `:151` |
| `dsh-workspace-changes` | `dsh-workspace-changes/README.md` | `:58` |
| `dsh-agent-loop` | `dsh-agent-loop/README.md` | `:220` |
| `dsh-fs-observation-policy` | `dsh-fs-observation-policy/README.md` | `:105-113` |
| `dsh-tool-present` | `dsh-tool-present/README.md` | `:90-92` |
| `dsh-plan-mode` | `dsh-plan-mode/README.md` | `:32` `:167` |
| `dsh-session-checkpoint-policy` | `dsh-session-checkpoint-policy/README.md` | `:114` |
| `dsh-tool-call-timeout-policy` | `dsh-tool-call-timeout-policy/README.md` | `:121-122` |
| `dsh-experimental-agent-team` | `dsh-experimental-agent-team/README.md` | `:76` `:136` `:203-204` |
| `dsh-experimental-auto-review` | `dsh-experimental-auto-review/README.md` | 整份 |

`$DSH_NODE_MODULES` 本次实测为:

```
/Users/bowhead/.nvm/versions/node/v22.23.1/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai/
```

**重抓一行**:

```sh
ls "$(npm root -g)/@deepseek-ai/dsh/node_modules/@deepseek-ai/" | grep dsh-
```

**注意**:官方包**不在这份 7924 条名单里**——`census.py --probe` 搜不到它们。想核原生行为只能读本机安装目录或官方仓库。DSH 升级后行号会漂移,所以要带上版本(`0.2.1-rc.3`)。

---

## 4. 可复跑的抓取脚本

不想手抄上面的 URL 时,直接跑这一段(只需要 `curl`,不需要 GitHub token):

```sh
# 1) 取当前 HEAD(用 atom,不吃 API 配额)
for r in samirliu/dsh-goalloop-agentteams rootsbymenda/dsh-second-angle \
         zhengqiuyang/dsh-attest-chain bycall/dsh-answer-reviewer \
         XiaoOu2024/dsh-self-review oxmumu3/dsh-workproof \
         263311487-ux/dsh-verify 030611/qiushi-dsh-evidence-audit \
         4444wjt/dsh-plugin-veriscope CAI-MH/dsh-quality-review \
         Jonah-Wu23/dsh-gungnir PerryLink/dsh-doublecheck; do
  printf '%-46s %s\n' "$r" \
    "$(curl -sS "https://github.com/$r/commits/main.atom" \
       | grep -oE 'Grit::Commit/[0-9a-f]{40}' | head -1 | cut -d/ -f2)"
done

# 2) 抓某个 commit 下的文件到本地核查
curl -sS -o /tmp/x.ts \
  https://raw.githubusercontent.com/PerryLink/dsh-doublecheck/22fe2e0/plugins/dsh-doublecheck/src/guard/prose.ts
sed -n '185,200p' /tmp/x.ts

# 3) 与本卡对比:HEAD 变了就说明该复核(见 §5)
```

**两条硬规则**:

- **抓完立刻把 commit 记下来**。本域已经有两个文件因为没记 commit 变成 `[OPEN]`。
- **raw URL 用短 SHA(7 位)即可**;URL 里用 `main` 会让你三个月后看到别的代码,而你以为还是那一份。

---

## 5. 复核触发:commit 漂移检测

把本卡 §1 的 commit 与脚本 (1) 的输出对比。**任何一个变了,就该复核对应卡片**,因为本域的断言是绑定到具体实现语义的:

| 卡片 | 变了要复核什么 |
|---|---|
| [02](./02-goal-gate-hard-floor.md) | `NO_PROGRESS_TURNS`、7 种 deny code、`treeDigest` 作废逻辑是否还在 |
| [03](./03-turn-end-reconciliation.md) | `requireQuoteForSteer` 默认值、四判决是否合并、24 例评测表是否更新 |
| [04](./04-evidence-index.md) | 五级阶梯是否仍是五级、`charity`/`converted` 是否还在计数 |
| [05](./05-custody-chain.md) | 检测边界表是否新增了「能检测删整个文件」 |
| [06](./06-judge-placement.md) | `threshold` 80 / `maxChallenges` 5 是否改动 |
| [07](./07-foreign-runtime-acceptance.md) | 四条「不」是否被删、退出码语义是否变化 |
| [08](./08-delivery-receipt.md) | 是否新增了 `decide` 动作(**一加,权限结论作废**) |
| [09](./09-discipline-loop.md) | `intensity` 默认值是否从 `remind` 改成 `block` |

**特别提醒**:有三条断言的**失效信号最隐蔽**——

1. [08](./08-delivery-receipt.md) 的「模型侧没有 `decide`」:如果哪天 README 里多了一行动作名,**结论直接反转**。
2. [09](./09-discipline-loop.md) 的「默认软」:默认值一行改动,整张卡的实践意义就变了。
3. [05](./05-custody-chain.md) 的检测边界表:它若新增了「能检测删整个文件」,说明作者加了链外锚点,**那是本域最想看到的变化**。

---

## 6. 发布版本与入口(从 `package.json` 实测,`main` 分支)

目录里**没有版本字段**(`data/plugins/*.yml` 只有 `url`/`name`/`category`/`tarball`/`description`),所以版本要自己读。下表是 `raw.githubusercontent.com/<repo>/main/package.json` 在 2026-10-31 的原值:

| 仓库 | npm 包名 | 版本 | 入口(`main` / `exports`) | 运行时约束 |
|---|---|---|---|---|
| `samirliu/dsh-goalloop-agentteams` | `dsh-goalloop-agentteams` | **0.10.0**(`main`)/ **v0.9.2**(目录 tarball) | `lib/index.js` + `./core` 子入口 | node ≥22 |
| `rootsbymenda/dsh-second-angle` | — (Release tarball) | v0.1.0 | — | — |
| `AaronandWork/dsh-evidence-gate` | **`@aaronandwork/dsh-evidence-gate`** | 0.2.1 | `lib/index.js` · client `lib/client.mjs` | node ≥18 |
| `030611/qiushi-dsh-evidence-audit` | — | — | `dsh.plugin.json`(**唯一带此 manifest 的样本**) | — |
| `zhengqiuyang/dsh-attest-chain` | `dsh-attest-chain` | 0.1.0 | `lib/index.js` | node ≥20 · cordis ^4.0.0 |
| `bycall/dsh-answer-reviewer` | `dsh-answer-reviewer` | **0.7.6** | `lib/index.js` · 另有 `./review` 子入口 | node ≥18 · cordis ^4.0.1 |
| `CAI-MH/dsh-quality-review` | `dsh-quality-review` | 0.1.0 | `lib/index.js`(+ `.d.ts`) | node ≥22.18 |
| `XiaoOu2024/dsh-self-review` | `dsh-self-review` | 0.4.2 | `index.js` · client `client.js` | **`engines.dsh: =0.2.1-rc.2`(精确等号)** |
| `263311487-ux/dsh-verify` | `dsh-verify` | **0.9.6** | **`dsh/plugin.mjs`**(⚠️ 非 `lib/`)· 另有 `bin/` `mcp/` `templates/` `demo/` | node ≥20 |
| `4444wjt/dsh-plugin-veriscope` | `dsh-plugin-veriscope` | 0.6.0 | `index.js` · client `client.js` | node ≥22.19 · **peer 钉在 `0.2.1-alpha.2`** |
| `oxmumu3/dsh-workproof#dsh-delivery-receipts` | 子包 | — | 见 `packages/dsh-delivery-receipts/package.json` | peer `(0.2.0-rc.2 \|\| 0.2.1-rc.3)` |
| `PerryLink/dsh-doublecheck` | `dsh-doublecheck` | **0.9.29** | `lib/index.js` + `./grill` 等多个子入口 | node `^22.19.0 \|\| >=24` · **`engines.dsh` 写成三段区间** |

**这张表里最重要的两行**:

- **`dsh-self-review` 写 `engines.dsh: =0.2.1-rc.2`(精确等号)** —— 本域基线是 `0.2.1-rc.3`。按字面**它不该装在 rc.3 上**。这是一个真实的兼容性风险,而不是文档瑕疵:精确等号的 engines 会被宿主或包管理器用来拒绝安装。
- **`dsh-plugin-veriscope` 的 peer 钉在 `0.2.1-alpha.2`** —— 比本域基线的 rc.3 更老。这与 [`08`](./08-delivery-receipt.md) B8 提倡的「显式并集 + 实测范围」形成对照:**三家写法各不相同,没有一个是「宽到能装、窄到可信」的标准答案。**

> `package.json` 读的是 **`main` 分支**,而 §1 的 commit 是 10-31 的 HEAD ——对这几个仓库两者时间接近但**不保证同一提交**。要精确,用 `https://raw.githubusercontent.com/<repo>/<sha>/package.json`。

---

## 7. 本卡自身的缺口 `[OPEN]`

- [x] ~~五个样本没有绑定实现文件~~ → **本轮已解决**:`bycall` / `CAI-MH` / `zhengqiuyang` / `AaronandWork` 的入口都是 `lib/index.js`(**发布产物,不是源码**),`4444wjt` / `XiaoOu2024` 是根 `index.js`。**注意:它们仓库里没有 `src/` 目录**,只有编译后的 `lib/` 或打包后的 `index.js`(debug 只能读产物)。`rootsbymenda` 仍只有 README 可读。
- [ ] **`XiaoOu2024/dsh-self-review` 声明 `engines.dsh: =0.2.1-rc.2`(精确等号),而本域基线是 `0.2.1-rc.3`。两份版本的 seam 行为是否一致,本域未验证**——[`06`](./06-judge-placement.md) 关于「唯一能动已发送文本」的结论依赖这一点。
- [x] ~~`dsh-verify` 与 `doublecheck` 的版本号未取~~ → 已补:`dsh-verify` **0.9.6**,入口 **`dsh/plugin.mjs`**;`doublecheck` **0.9.29**,入口 `lib/index.js`。
- [ ] ⚠️ **`goalloop` 有一个版本落差**:目录 tarball 是 **v0.9.2**,而 `main` 的 `package.json` 已是 **0.10.0**。[`02`](./02-goal-gate-hard-floor.md) 的源码断言读的是 **`lib/index.js`(v0.9.2 产物)**——若 0.10.0 改了 deny code 或 `NO_PROGRESS_TURNS`,那张卡需要复核。
- [ ] 本卡 §6 的 `package.json` 读的是 `main` 分支,与 §1 的 commit **不保证同一提交**。若要严格,应改用 `raw.githubusercontent.com/<repo>/<sha>/package.json`。
- [ ] `oxmumu3/dsh-workproof` 的同仓子包 `packages/dsh-evidence-ledger/` **完全未考察**,但目录里单独列了它——它可能与本域 ④ 证据环直接相关。
- [ ] `bycall/dsh-answer-reviewer` 在目录里的 `name` 字段缺 owner(`dsh-answer-reviewer`),这会让按名字检索失败;**不确定是否还有别的条目有同样的字段缺陷**。
- [x] ~~没记录默认分支~~ → 抽查 5 个仓库,`main` 与 `master` **都返回 200**(GitHub 对不存在的分支会回落到默认分支,所以这个探测不可靠)。**结论:atom 抓取若返回空,必须当成失败处理,不能当成「没有提交」。**
