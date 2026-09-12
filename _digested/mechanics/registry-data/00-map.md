# registry-data · 数据模型

> 状态:**0001 已复核**(schema/命名/边车拓扑/普查已按 `38976afd` 重核;schema 白名单与全部机制性论断仍成立,过期点集中在数字与行号,已就地更新)。最近核验:`38976afd`,2026-09-12。

## 定位

`data/` 是全仓库唯一人工编辑层:`data/plugins/*.yml` 一个插件一个文件(实测 **3552 个**,2026-09-12;基线 5e7dc7eb 时为 2286;全部满足 `<owner>__<repo>.yml` 命名,monorepo 子包形如 `owner__repo--packages-my-plugin.yml`,sub 用单 `-` 连接)。其余 JSON 全部是机器写或冻结的派生物。为什么一文件一插件:以前所有人往 README 同一分类的同一位置追加,合并一个 PR 就撞掉下一个——独立文件永不冲突(contributing.md:43)。**0001 起投稿者连 regenerate README 都不用做了**(合并后由 main 重生成,见 [readme-pipeline](../readme-pipeline/00-map.md))。

## 条目 schema(validateEntries 白名单,scripts/lib/entries.mjs:136-204)

| 字段 | 规则 |
|------|------|
| `url` | 必须 `https://github.com/<owner>/<repo>[/tree/<branch>/<sub>]`;全列表唯一 |
| `name` | 显示文本,惯用 `owner/repo`(子包加 `#subname`)|
| `category` | ∈ CAT_IDS(23 个:`agi ui usage theme model identity session memory tools wsl browser vision voice docs skill workflow git notify dev security remote market fun`;**wsl 为 2026-09 新增**,#3664)|
| `description.en` | 必填,单行 |
| `description.zh` | 可省;存在即非空非换行;**未知 locale(如 ja)拒绝** |
| `tarball` | 可选;仅 GitHub 域 https `.tgz/.tar.gz`,github.com 路径必须含 `/releases/`(TARBALL_HOSTS 三域)|

- 显式禁项:**手写 `npm:` 键被校验拒绝**——npm 归属只能由 registry 的 package.json `repository` 字段回链自动采集,"防止某个包把自己挂到并未认领它的仓库上"(contributing.md:211-212)。
- YAML 手写高频错误已内建诊断:`description` 含 `": "` 未引号 → readEntries 定位肇事行并给出改写建议。
- dumpEntry 省略空翻译键("未译"≠"译成空"),lineWidth -1 超长单行、双引号风格。

## 分类体系(2026-09-12 普查)

共 23 类全部有脚本看守(generate-readme ↔ contributing.md ↔ reorder-categories.py 三处联动:改序重排要动 CAT_IDS 与 locales 两个 categories 块再再生 README;contributing.md:46 类目清单已同步含 wsl)。条目量分布(前八):ui 592、tools 477、dev 268、session 224、workflow 216、usage 196、memory 168、model 156;最末 agi 仅 6(identity 已长到 14)。taxonomy 是活的:usage/vision/security/browser/git/docs/remote/voice/wsl 都是长胖后新增或拆出来的(contributing.md:95;注:wsl 尚未写进 contributing 的"拆分名单"原文,上游文档滞后)。

**wsl 类抽查(0001)**:35 条 = 173787247/dsh-wsl-* 系列 29 条 + 其余 6 作者 6 条;schema 无任何新字段(抽查全部仍是 url/name/category/description,仅 1 条带 tarball);双语类目名 wsl: 'WSL & Windows Interop'/'WSL 与 Windows 互操作',CAT_EMOJI 🐧(entries.mjs:43)。

主题类特殊通道:**Themes & Appearance(theme)**下的条目自动进入 dsh-market 的 Themes Tab 一键安装。

## 边车 JSON 与 CRLF 现象

四个 committed 边车(stars/downloads/screenshots/added-dates)+ 四个 cache-only 文件(npm-map/readmes/tarballs/updates-declared 部分见 [probes-and-decay/00-map](../probes-and-decay/00-map.md))。join 键统一是**条目 URL 原文**。URL→repo/sub 的 decompose 在六处探针里各有一份实现且行为不一(stars/updates 丢 subdir,npm/readmes/screenshots/prune 保留)——已知重复债。

实测数据卫生事实:**11 个 yml 带 CRLF**(2026-09-12;基线时 5 个,4 个原样保留);validateEntries 不查换行风格,js-yaml 容忍之,照常收录。(这也解释了粗 grep 统计时的计数分裂。)但 **generate-readme 已对 CRLF 免疫**:0001 新增 `normalizeNewlines`,`parsedUrls` 改 `split(/\r?\n/)`,README 比对前归一换行——入口 yml 的 CRLF 仍不设防,管线比对不再受扰。

0001 边车 diff 观察:screenshots.json 被**整文件重写**(diff -1343/+1359),键集合仅 17 处增删、其余为键序重排——结构仍是 URL → 图片 URL 数组,无字段级变化;四个边车的变更全部是键值增删改(含改 URL、Dayi-Z→dsh-learn-wiki 改名),value 结构不变;added-dates.json 末尾现在有换行(基线时没有)。

## 待回答的问题

- [ ] added-dates.json 冻结基线的完整规则(build-site:169-188 已读,en README 推导+人工补录的边界)
- [x] 边车 key 结构与 join → 见 [probes-and-decay/00-map](../probes-and-decay/00-map.md)
- [ ] 同 URL 多语言/多分类冲突在 validateEntries 与 build-site parity 两层的分工细节

## 正文

- 01 · 从 PR 到收录的数据生命周期(待写:新条目落地→首夜探针→出现在站点/市场/README 各面的时序)
