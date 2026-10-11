# registry-data · 数据模型

> 状态:**0003 已复核**(schema/命名/边车拓扑无 diff;结构统计重跑到 4489 条。新增 URL 117、移除 20、同 URL 修改 35;`data/capabilities.json` 为旧扫描快照,当前 URL join 覆盖 3826 条)。最近核验:`4693e5a83`,2026-10-11。

## 定位

`data/` 是全仓库唯一人工编辑层:`data/plugins/*.yml` 一个插件一个文件(实测 **4489 个**,2026-10-11;0002 基线时 4392,初问快照 2286;全部满足 `<owner>__<repo>.yml` 命名,monorepo 子包形如 `owner__repo--packages-my-plugin.yml`,sub 用单 `-` 连接)。除 `plugins/` 外的 data 文件全部是机器写或冻结的派生物(拓扑见下)。为什么一文件一插件:以前所有人往 README 同一分类的同一位置追加,合并一个 PR 就撞掉下一个——独立文件永不冲突(contributing.md:43)。投稿者也不必再 regenerate README(合并后由 main 重生成,见 [readme-pipeline](../readme-pipeline/00-map.md))。

## 条目 schema(validateEntries 白名单,scripts/lib/entries.mjs:139-243)

| 字段 | 规则 |
|------|------|
| `url` | 必须 `https://github.com/<owner>/<repo>[/tree/<branch>/<sub>]`;全列表唯一 |
| `name` | 显示文本,惯用 `owner/repo`(子包加 `#subname`)。**0002 新增硬规则(:166-177)**:写成 owner/repo 形式的 name **必须等于 url 的 owner/repo**(大小写不敏感;`#` 之后自由;纯显示名如 "Session Lens" 不受查)。理由:#5756 查出 6 条"名字指着一个仓库、链接指向另一个",其中 5 条的名字仓库**根本不存在**——"the name is the link text, so it must name the repository the link goes to" |
| `category` | ∈ CAT_IDS(23 个:`agi ui usage theme model identity session memory tools wsl browser vision voice docs skill workflow git notify dev security remote market fun`;wsl 为 0001 新增,#3664;0002 窗口内未增删)|
| `description.en` | 必填,单行 |
| `description.zh` | 可省;存在即非空非换行;**未知 locale(如 ja)拒绝** |
| `tarball` | 可选;仅 GitHub 域 https `.tgz/.tar.gz`,github.com 路径必须含 `/releases/`(TARBALL_HOSTS 三域)|

- 显式禁项:**手写 `npm:` 键被校验拒绝**——npm 归属只能由 registry 的 package.json `repository` 字段回链自动采集,"防止某个包把自己挂到并未认领它的仓库上"(contributing.md:211-212)。
- YAML 手写高频错误已内建诊断:`description` 含 `": "` 未引号 → readEntries 定位肇事行并给出改写建议。**0002 起语法错误还有一道兜底**:pr-gate 会先解析每个变更的 `.yml`,不合法就报 `文件:行号`(#4680 的 `zh:` 行是 GBK 乱码,曾被静默丢弃五天)。
- dumpEntry 省略空翻译键("未译"≠"译成空"),lineWidth -1 超长单行、双引号风格。

## 分类体系(2026-10-11 census 普查)

共 23 类全部有脚本看守(generate-readme ↔ contributing.md ↔ reorder-categories.py 三处联动:改序重排要动 CAT_IDS 与 locales 两个 categories 块再再生 README)。条目量分布(全量):ui 781、tools 585、dev 321、session 294、workflow 267、usage 236、model 213、memory 209、skill 178、notify 173、theme 158、security 151、remote 138、fun 137、git 111、vision 109、browser 98、market 80、**wsl 77**、docs 67、voice 65、identity 24、agi 17。taxonomy 是活的:usage/vision/security/browser/git/docs/remote/voice/wsl 都是长胖后新增或拆出来的(注:wsl 尚未写进 contributing 的"拆分名单"原文,上游文档滞后)。

**wsl 类抽查(0003 更新)**:77 条,其中 **173787247 的系列 70 条**,较 0002 基线增加 11 条;本轮新增继续集中于 Windows/WSL 控制、性能/事件与防护工具。它依然是高度集中的单作者类目,但下载转化沿用的仍是旧数据,不能据此断言当前需求。schema 无任何新字段;双语类目名 wsl: 'WSL & Windows Interop'/'WSL 与 Windows 互操作',CAT_EMOJI 🐧(entries.mjs:43)。

**0002 勘误(普查脚本)**:census.py 的手写 YAML 解析器此前不剥行内注释,两条把 PR 模板注释一起粘进 `category:` 行的投稿(js-yaml 认为合法,读作 tools/model)会在 ① 表里凭空长出两个类目。已修(`strip_comment`,只切"前面是空白且不在引号内"的 `#`,URL 的 `#sub` 与描述里的 `#tag`/`#12B7F5` 都不受影响),tools 576 / model 213 是修正后的数。

主题类特殊通道:**Themes & Appearance(theme)**下的条目自动进入 dsh-market 的 Themes Tab 一键安装。

## 边车 JSON 与 CRLF 现象

| data 文件 | 写入方 | git 追踪? | 说明 |
|-----------|--------|-----------|------|
| `stars.json` | probe-stars | ✅(刻意不 ignore) | 提交的地板,保证"抓取失败保留旧值" |
| `downloads.json` | probe-downloads | ✅ | 独立 downloads-v1 |
| `added-dates.json` | 人工拥有的冻结基线 | ✅ | 2026-08-15 前固定,之后由 build-site 双账本推导 |
| `screenshots.json`(legacy)| 人工(已停用)→ prune 渐进清空 | ✅ | 有终点的 fallback |
| **`capabilities.json`(0002 新增)** | `scripts/probe-capabilities.mjs` | ✅ | 见下 |
| `npm-map.json` / `readmes.json` / `tarballs.json` | 各探针 | ❌(.gitignore 明列)| 只在 Actions cache |
| `updates.json` | probe-updates | ❌ **从未进过 git 历史** | 只在 updates-v1 cache;0001 误记为已提交,0002 更正 |
| `screenshots-declared.json` / `-live.json` | probe-screenshots | ❌(.gitignore)| 刻意不缓存,重算免费 |

**`capabilities.json` 的形状(0002 新增边车)**:`{url: {version, spec, capabilities[], redLines[], scannedAt, tool}}`,`capabilities` ∈ {shell, fs-write, fs-read, network, env, credentials, llm, dynamic-code, host-runtime, subagent},`tool` 恒为 `dsh-trust-check@0.1.13`(扫描器版本钉在 package.json 的 devDependency 里)。3844 行(4392 条目的 87.5%),快照时间 2026-09-24T17:02–17:41Z,即一次扫描快照;与当前名单 URL join 只有 3826/4489(85.2%),不是当前完整覆盖。语义见 [probes-and-decay/01](../probes-and-decay/01-probe-family.md);它被 build-site 透传进 `docs/plugins.json`,**站内页面不渲染**。

join 键统一是**条目 URL 原文**(含 monorepo 子路径)。URL→repo/sub 的 decompose 在探针里各有一份实现且行为不一(stars/updates 丢 subdir,npm/readmes/screenshots/prune 保留)——已知重复债。0002 新增一份**共享**实现:`scripts/lib/terms.mjs` 的 `slugOf/termOf`,由 build-site 与 adopt-discussions 共用(此前两处各自小写化,劈了评论线程)。

实测数据卫生事实:**15 个 yml 带 CRLF**(2026-09-30;0001 时 11 个,初问 5 个);validateEntries 不查换行风格,js-yaml 容忍之,照常收录。generate-readme 已对 CRLF 免疫(`normalizeNewlines`)。**0002 新增一条同类观察**:`data/updates.json` 既不在 .gitignore 里、也从未被提交——本地跑一次探针就会在 `git status` 里冒出来,和它的三个兄弟(npm-map/readmes/tarballs 都在 .gitignore)不一致。

0002 边车 diff 观察:`screenshots.json` 继续整文件轮转(2700 行级),stars/downloads 常规更新;prev 快照到本轮的键增删以新增条目为主。

## 待回答的问题

- [ ] added-dates.json 冻结基线的完整规则(build-site :216-290 已读,en README 推导 + yml 账本 + 人工补录的边界)
- [x] 边车 key 结构与 join → 见 [probes-and-decay/00-map](../probes-and-decay/00-map.md)
- [ ] 同 URL 多语言/多分类冲突在 validateEntries 与 build-site parity 两层的分工细节
- [ ] **0002 新增**:`updates.json` 是否该补进 .gitignore(现在靠"没人提交"维持不追踪)
- [ ] **0002 新增**:CRLF 从 5→11→15 单调增长,是否该在 pr-check 加一条归一化守卫(而非只让下游免疫)

## 正文

- 01 · 从 PR 到收录的数据生命周期(待写:新条目落地→首夜探针→出现在站点/市场/README 各面的时序)
