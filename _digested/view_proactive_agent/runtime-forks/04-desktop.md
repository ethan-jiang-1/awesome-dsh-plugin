---
kind: card
domain: proactive_agent
subcategory: runtime-forks
repo: jinghuaihuaxiang-star/dsh-superagent-desktop
commit: e2cee418f9549f1e006e4d2900c5a3f222946362
evidence: 3
status: active
asof: 2026-11-09
---

# dsh-superagent-desktop — 1★ 的薄分叉，把 super-agent 装进你正开着的那个 profile

> ★★★ 源码级，`jinghuaihuaxiang-star/dsh-superagent-desktop@e2cee41`（2026-11-09 20:12 +0800，`release 0.1.3`）。
> 星标与 npm 下载为 2026-11-26 实时读数；结构事实截止 2026-11-09。深读材料见 [FAQ 03](../../../_faq_on_digested/02_superagent-dependents/lines/03-desktop-fork.md)。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 / 类目 | `jinghuaihuaxiang-star/dsh-superagent-desktop` / **workflow** |
| 自述差异 | "desktop-bundle packaging, a default `stateDir`, peer ranges widened to `0.2.x`, Windows compatibility fixes in the host code"（`README.md:70`） |
| 声量 | **1★ / 0 forks / 0 open issues**（GitHub API 2026-11-26）；created 2026-11-09T05:21Z，pushed 2026-11-09T12:12Z，MIT，`fork: false` |
| 下载（最硬的采用信号） | npm `dsh-superagent-desktop`：**过去一月 1,753 / 过去一周 380 / 单日 59**（`api.npmjs.org`，2026-10-26–11-24） |
| 发版节奏 | **5 个版本全在 2026-11-09 一天内发完**（`0.0.0-stage`、`0.1.0`–`0.1.3`，05:57–12:14 UTC）；latest `0.1.3`，unpacked 1.33 MB，maintainer `jinghuaihuaxiang` |
| repo@commit | `e2cee418f9549f1e006e4d2900c5a3f222946362`，2026-11-09，提交信息 `release 0.1.3` |
| 包形态 | **`private: false`**、MIT、`dsh.bundle.patch` → `cordis.patch.yml`；23 个 peer |
| 宿主钉版 | 23 个 peer 里 **21 个** `@deepseek-ai/*` 放宽到 `^0.2.1-alpha.2 \|\| ^0.2.2-rc.1`；`@deepseek-ai/cordis` 精确钉 `4.0.5-alpha.1`、`schemastery` 精确钉 `3.18.5-alpha.1`；`engines.dsh` 同范围 |
| 改动面 | **7 个 `src` 文件（+78 / −19）+ `package.json` + `cordis.patch.yml`（7 行）**；另 `README.md` 重写、`tsdown.config.ts` 改 client bundle id 一行 |
| 一字未改 | `docs/`（9 个文件）、`tests/`（65 个）、`examples/`、`locale/`、`prompts/`、`SETUP.md` —— `diff -rq` 为空 |
| 代码规模 | `src/` **110 个 TS/TSX / 15,261 行**（与上游同量；这是薄分叉，不是重写） |
| 复现 | `git checkout e2cee41`；`diff -rq ../upstream/src src` 输出 7 行；`diff upstream/cordis.patch.yml cordis.patch.yml` 是 7 行改动 |

## 它到底是什么

**一句话：它不改"谁能派活、活落在哪"，只改"装在哪、默认值是多少、Windows 上能不能起"。**

上游的部署前提是"给这个 agent 单独一个宿主"：专用 profile、独立进程、必填的绝对 `stateDir`、POSIX 的 shim（`docs/006-deployment.md:7` 的"专用 profile"要求、`:95` 的 `stateDir | yes`）。桌面用户的前提正相反——DSH 已经开着，模型、插件、会话都在里面，他要的是侧栏多一个入口。这一支把四条前提逐条拆掉：

1. **改名以便分发。** 包名 `dsh-superagent-desktop`、`private: false`、`version 0.1.3`（`package.json:2,9-10`）。上游自己 `private: true`、不发 npm，所以别的分叉只能 `link:` / git / tarball 装。
2. **保留 entry id，只换实现的包名。** `cordis.patch.yml:5-13` 仍是 `id: dsh-superagent` / `-github` / `-feishu`，只把 `name:` 指向本包。profile 里已有的同名配置块、`docs/` 的示例、面板的 `/orchestrator/*` 前缀、`stateDir` 键名全部继续成立。
3. **`stateDir` 给默认值。** `.required()` 换成 `.default(defaultStateDir())`，默认 `<DSH_HOME>/state/superagent`（`src/deployment.ts:16-19,23`），并配一条注释"profile 可以覆盖"（`cordis.patch.yml:1-3`）。
4. **补 Windows 与首次使用。** `.cmd` shim、`pwsh` 工具、包根识别、面板"开始使用"卡——见下节。

**它没碰的假设**：仍只服务一个 GitHub 仓库、仍只有 GitHub/飞书两个 Source、仍是单团队单仓策略、worker 仍以操作者 OS 用户身份无审批执行。这既是它 diff 只有 7 个文件的原因，也是它适用面止步于"上游本来能用、只是装起来麻烦"的人。

## 怎么接进 DSH

1. **从 UI**：Settings → Plugins → **Add bundle**，输入 `dsh-superagent-desktop`，启用，重启应用（`README.md:17`）。这是 DSH 按包名去 registry 取的标准入口，也是它能"填一个包名就装完"的关键。
2. **从 CLI**：`dsh plugin --profile desktop add dsh-superagent-desktop`（`README.md:21`），然后把 `"dsh-superagent-desktop"` 加进该 profile `package.json` 的 `dsh.profile.bundles`，重启（`:25`）。本地检出可换 `link:/abs/path`。
3. **patch 插入三个 entry**：同 id、换 `name`；飞书 entry 仍是 `disabled: true`——**这一行上游本来就有**（上游 `cordis.patch.yml:12`），本仓没有新增默认关闭。
4. **不另起进程、不单独 profile**：装进现有 profile 就是全部卖点；面板注册走官方插槽 `sidebar.panellist`（`src/client/index.tsx:55`，与上游同一注册点、本仓未改），重启后侧栏出现锤子图标。
5. **`stateDir` 可覆盖**（`README.md:35-41`）：

   ```yaml
   - id: dsh-superagent
     config:
       stateDir: /absolute/path/to/state/superagent
   ```

6. **一个 state 目录只能一个宿主**：目录被 `proper-lockfile` 锁住（`src/app/runtime.ts:93`），第二个宿主拿不到锁；想并存必须显式改路径。

## 关键实现

| 文件 | 改动 | 作用 | 锚点 |
|------|-----:|------|------|
| `src/deployment.ts` | +16/−4 | `defaultStateDir()` 取 `$DSH_HOME` 否则 `~/.dsh`，拼 `state/superagent` 并把 `\` 折成 `/`；`stateDir` 由必填改默认；绝对路径 pattern 接受 `C:/` 盘符写法 | `:14,16-19,23` |
| `src/infra/paths.ts` | +8/−2 | `PACKAGE_NAMES = {dsh-superagent-desktop, dsh-superagent}`，`packageRoot()` 沿目录上溯匹配最近 `package.json` 的名字 | `:7,18,24` |
| `src/infra/environment.ts` | +15/−7 | Windows 只写 `<name>.cmd`：首行 `@REM`（`#` 会被 cmd 当语法错）、`@echo off`、按绝对路径调用、`exit /b %ERRORLEVEL%`；marker 比对先剥 `@REM `/`:: `；git origin 比对把 `\` 折 `/`，否则 `file:C:/…` 与 `join()` 出来的 `C:\…` 永不相等、误报 `gitTooOld` | `:16,92-96,104-105,149` |
| `src/app/sessions.ts` | +3/−2 | `noWait` 守卫加 `pwsh`；`tools.restrict` 的 allow 同时列 `bash`/`pwsh`，再按宿主**实际注册**的工具过滤（restrict 拒绝未知名字） | `:79,263-264` |
| `src/client/overview.tsx` | +26/−1 | 概览新增"开始使用"三步卡（打开主会话 / 去来源 / 去执行），只在无流量、无待办、无 setup 问题时出现 | `:61-83,104` |
| `src/client/locales.ts` | +7/−3 | 三步卡与面板文案 | — |
| `src/client/client.css` | +3/−0 | 三步卡的 `dt-steps` 样式 | — |

**数据流**：面板每 5 秒拉 `GET state`（`src/client/provider.tsx:74,89`，重启中 1 秒） → 宿主读 `orchestrator.sqlite` 与 state 目录 → 主会话把人的话变成工单 → 该工单在 `stateDir/work` 下由 `worker-*` 会话执行 → 结果回原对话，面板的"执行"页显示进度与危险区（stop / retry）。

**环境注入是这一支最需要看清的一处**：`src/app/setup.ts:92` 调 `applyEnvironment(...)`，后者把 `PATH` 前面插入 `worker-bin`，并写入一整组 git 变量：`GIT_CONFIG_GLOBAL` 指向 worker gitconfig、`GIT_CONFIG_NOSYSTEM=1`、`GIT_ASKPASS=''`，同时把 `GH_TOKEN`/`GITHUB_TOKEN`、`GIT_DIR` 一类定位变量、`GIT_AUTHOR_*`/`GIT_COMMITTER_*` 身份变量清成 `undefined`（`src/infra/environment.ts:47-59`）。它**直接改 `process.env`**，返回一个 restore 回调（`:125-131`）。上游要求专用 profile，正是为了让这些改动只影响那个进程（`docs/006-deployment.md:7`）。

## 为什么它突出

- **它验证了一条分发路径。** 上游 24,589★（2026-11-26 读数）却不在 npm、不发包（`dsh-superagent` 在 registry 是 404）；它 1★ 却把安装从"读文档 + 六条命令 + 手抄占位符"降成"填一个包名"。`private: false` + 不撞车的包名 + 保留 entry id，三件事合起来才是"能装进现有 profile"。
- **星标与下载是两种量纲，这一页正好撞上。** 1★ 说明它没有社区叙事；月下载 1,753 说明确实有人在装。下载含 CI、镜像与重复安装，不能当用户数，但足以否定"1★ = 没人用"。同批的 `dsh-superagent-local` 在 npm 也是 404。
- **id 兼容层是刻意的。** 换掉的只有"这个 id 指向哪个包"，于是 profile 配置、`docs/` 示例、路由前缀全部不作废。代价是它与上游、与 02-local **在同一个 profile 里互斥**——包名不同可以并存于 `node_modules`，id 相同不行。
- **一次性打包，不是持续维护。** 5 个版本一天发完，之后无更新、无 CHANGELOG、无 upstream remote；`tests/` 一个文件没动。

## 代价与边界

1. **同 id 互斥**：`dsh-superagent` / `-github` / `-feishu` 三个 id 与上游完全相同（`cordis.patch.yml:5-13`），一个 loader 里不能有两份；想两个都试只能开两个 profile，而两个 profile 又会在默认 `stateDir` 上抢锁。
2. **默认状态目录是全局的**：`<DSH_HOME>/state/superagent` **按 `DSH_HOME` 而不按 profile**，同机所有 profile 共享；桌面 app 与 CLI 都用默认值时，第二个会因目录锁起不来。
3. **进程级环境注入落在日常宿主**：`PATH`、`GIT_CONFIG_GLOBAL` / `GIT_CONFIG_NOSYSTEM` / `GIT_ASKPASS`、被清空的 `GH_TOKEN`/`GITHUB_TOKEN` 与提交者身份变量，全部作用于你每天用的那个进程。上游用独立 profile 规避，这一支没有；它的 `docs/` 一字未改，等于这层代价没有写进随包说明书。
4. **worker 会话混进列表**：`src/client/index.tsx` 与上游逐字节相同，不收起 `worker-*` / `orchestrator-*`。装进自己的 profile 后，主会话、执行器会话与你的工作会话共用一个侧栏。
5. **宿主升级风险**：peer 放宽是**声明不是验证**——`cordis` 与 `schemastery` 仍精确钉死，宿主换 cordis 版本就得重出包；README 也只说在 desktop `0.2.2-rc.1` + Windows 11 上测过（`README.md:11`）。`0.2.2-rc.2+` 能否加载未验证。
6. **文档没跟着改**：`docs/006-deployment.md:95` 仍写 `stateDir | yes`，`SETUP.md` 仍教建 `superagent` profile，`examples/` 仍是 `<absolute path>` 占位。bundle 自带的说明书和它的卖点互相矛盾。
7. **测试仍假设 POSIX**：`tests/` 未改，README 自己说套件依赖 `sleep`/`ps`，Windows 上 `pnpm test` 的失败来自平台（`README.md:66`）；验证方式退化为"跑起来的宿主里的面板与 API"。
8. **权限边界没变**：worker 以操作者 OS 用户、`danger-full-access` 执行（`docs/006-deployment.md:19`），`blockedCommands` 只是同名 shim、按绝对路径可绕过。装进日常 profile 后，这条比以前更贴近人。

## 可信度与复现

- **★★★（本仓与其与上游的差异）**：读了 `README.md`、`package.json`（与 npm 0.1.3 元数据对齐）、`cordis.patch.yml` 全文与逐行 diff、7 个 `src` 文件的逐行 diff、`src/app/{setup,sessions}.ts` 的注入与工具面、上游 `docs/006-deployment.md` 的部署前提。
- **未做**：没有真的 `dsh plugin add` 安装、没有启动面板、没有跑 worker；没有验证两个 profile 共用默认 `stateDir` 时的具体报错文案；没有验证 peer 放宽后在 `0.2.2-rc.2+` 上是否真能加载。

```sh
git clone https://github.com/jinghuaihuaxiang-star/dsh-superagent-desktop /tmp/jh-desktop && cd /tmp/jh-desktop
git checkout e2cee41
diff -rq /tmp/sa-research/upstream/src src              # 7 行
diff /tmp/sa-research/upstream/cordis.patch.yml cordis.patch.yml   # 7 行改动（注释 2 + entry name 3 + preset 显示名 2）
diff -rq /tmp/sa-research/upstream/docs docs | wc -l   # 0
curl -s https://registry.npmjs.org/dsh-superagent-desktop | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["dist-tags"],len(d["versions"]))'
curl -s https://api.npmjs.org/downloads/point/last-month/dsh-superagent-desktop
```

## 待验证

1. **实装**：`dsh plugin add dsh-superagent-desktop` 装进一个已有 bundle 的非空 profile 后，是否真如 README 所说"重启即出现锤子图标"。这是它全部价值所在，也是唯一没验的一步。
2. **默认 `stateDir` 的冲突形态**：两个 profile 共用 `<DSH_HOME>/state/superagent` 时，第二个宿主是报错退出、还是静默降级，文案是什么——只知道有目录锁。
3. **peer 放宽的真实边界**：`0.2.2-rc.2+` / `0.2.3` 上能否加载；`cordis 4.0.5-alpha.1` 与宿主实际版本不一致时的失败形态。
4. **client bundle id 与 entry id 不一致是否有影响**：`tsdown.config.ts` 把 client 模块 id 改成 `dsh-superagent-desktop`，而 server 侧 entry id 仍是 `dsh-superagent`；这与 client 加载/去重路径的关系未验证。
5. **两处"未写明的代价"的实际影响面**：环境注入（`PATH`/git 配置/清 token）对日常会话里其它插件的影响，以及 worker 会话混排对会话列表/搜索的干扰，都只有代码证据、没有运行证据。
