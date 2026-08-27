# registry-data · 数据模型

> 状态:**进行中**(schema、命名规则、边车拓扑、普查数据已核验;文件级统计为 2026-08-27 实测)。最近核验:`5e7dc7eb`。

## 定位

`data/` 是全仓库唯一人工编辑层:`data/plugins/*.yml` 一个插件一个文件(实测 **2286 个**,全部满足 `<owner>__<repo>.yml` 命名;monorepo 子包形如 `owner__repo--packages-my-plugin.yml`,sub 用单 `-` 连接)。其余 JSON 全部是机器写或冻结的派生物。为什么一文件一插件:以前所有人往 README 同一分类的同一位置追加,合并一个 PR 就撞掉下一个——独立文件永不冲突(contributing.md:41)。

## 条目 schema(validateEntries 白名单,lib/entries.mjs:135-203)

| 字段 | 规则 |
|------|------|
| `url` | 必须 `https://github.com/<owner>/<repo>[/tree/<branch>/<sub>]`;全列表唯一 |
| `name` | 显示文本,惯用 `owner/repo`(子包加 `#subname`)|
| `category` | ∈ CAT_IDS(22 个:`agi ui usage theme model identity session memory tools browser vision voice docs skill workflow git notify dev security remote market fun`)|
| `description.en` | 必填,单行 |
| `description.zh` | 可省;存在即非空非换行;**未知 locale(如 ja)拒绝** |
| `tarball` | 可选;仅 GitHub 域 https `.tgz/.tar.gz`,github.com 路径必须含 `/releases/`(TARBALL_HOSTS 三域)|

- 显式禁项:**手写 `npm:` 键被校验拒绝**——npm 归属只能由 registry 的 package.json `repository` 字段回链自动采集,"防止某个包把自己挂到并未认领它的仓库上"(contributing.md:198-199)。
- YAML 手写高频错误已内建诊断:`description` 含 `": "` 未引号 → readEntries 定位肇事行并给出改写建议。
- dumpEntry 省略空翻译键("未译"≠"译成空"),lineWidth -1 超长单行、双引号风格。

## 分类体系(2026-08-27 普查)

共 22 类全部有脚本看守(generate-readme ↔ contributing.md ↔ reorder-categories.py 三处联动:改序重排要动 CAT_IDS 与 locales 两个 categories 块再再生 README)。条目量分布(前八):ui 358、tools 295、dev 193、session 156、workflow 131、usage 124、memory 112、notify 110;最末 identity 仅 4。taxonomy 是活的:usage/vision/security/browser/git/docs/remote/voice 都是长胖后从 tools/ui/dev 里拆出来的(contributing.md:93)。

主题类特殊通道:**Themes & Appearance(theme)**下的条目自动进入 dsh-market 的 Themes Tab 一键安装。

## 边车 JSON 与 CRLF 现象

四个 committed 边车(stars/downloads/screenshots/added-dates)+ 四个 cache-only 文件(npm-map/readmes/tarballs/updates-declared 部分见 [probes-and-decay/00-map](../probes-and-decay/00-map.md))。join 键统一是**条目 URL 原文**。URL→repo/sub 的 decompose 在六处探针里各有一份实现且行为不一(stars/updates 丢 subdir,npm/readmes/screenshots/prune 保留)——已知重复债。

实测数据卫生事实:5 个 yml 带 CRLF 换行(paicat1__dsh-screenshot.yml 等);validateEntries 不查换行风格,js-yaml 容忍之,照常收录。(这也解释了粗 grep 统计时的计数分裂。)

## 待回答的问题

- [ ] added-dates.json 冻结基线的完整规则(build-site:169-188 已读,en README 推导+人工补录的边界)
- [x] 边车 key 结构与 join → 见 [probes-and-decay/00-map](../probes-and-decay/00-map.md)
- [ ] 同 URL 多语言/多分类冲突在 validateEntries 与 build-site parity 两层的分工细节

## 正文

- 01 · 从 PR 到收录的数据生命周期(待写:新条目落地→首夜探针→出现在站点/市场/README 各面的时序)
