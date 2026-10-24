# 03 · 发布层:npm 双包、legacy 截图清退与评论线程收编

> 基线:`upstream@b4d0049a8`(0004 复核,2026-10-24;build-site.yml 现 298 行)。两个发布器里只有 `publish-catalog.mjs` 变了(142→**169** 行):0004 起 catalog 包**顺带装一份市场索引** `docs/index.json`。`publish-updates.mjs`(134 行)与 prune-legacy-screenshots(114 行)零 diff;adopt-discussions 只多了一段 `npm ci` 的 registry 覆盖。

## 为什么发 npm(注释里有真实测量)

- Pages 就是 GitHub(响应头 `server: GitHub.com`),大陆访问慢;公共 GitHub 反代一律拒非 github.com 的 hostname(实测该域名 403)。发到 registry.npmjs.org 就**复用了插件生态本来就在用的镜像体系**(publish-catalog.mjs:3-14)。
- 单独成包而非塞进 `awesome-dsh-plugin` 包:npm 强制携带 README(两个 README 各 ~500KB),`npm pack --dry-run` 测得 772KB vs 独立 ~250KB;独立包还让目录获得版本号、可回滚(:19-25)。
- updates 与 catalog 拆成两包:catalog tarball 被每个 market 每次升级都拉,update notes 只被打开对话框的那一个用户读;合并会让全体消费者的每日下载翻倍(publish-updates.mjs:9-15)。
- **0004 的新理由不是"大小"而是"权限"**:索引本来要单独发一个 `dsh-plugin-catalog-index`,第一次发布直接 404——npm 的 trusted publishing 是**按包**配置的,一个还不存在的包没法从 CI 里建立这层关系,建它需要有人在 npmjs.com 上浏览器登录。于是索引先塞进发布链已经跑通的那个包里(:40-48)。代价是实测的:**每次 catalog 下载多扛 684KB gzip(约 2.3MB JSON)**。这条债有明确终点(拆包),但没有排期。

## 两个发布器的同构机制

| | dsh-plugin-catalog | dsh-plugin-updates |
|---|---|---|
| 内容 | `docs/plugins.json`(原字节)**+ `docs/index.json`** | `docs/updates.json` |
| 幂等键 | packument 自定义字段 `catalogSha`=sha256(**两个文件拼接**,:129-133)| `updatesSha` |
| 版本 | `YYYY.MDD.RUN`(月份不补零——semver 禁前置零;日期部分跨年可比)| 同 |
| 凭据 | trusted publishing(OIDC),需 `id-token: write` + npm ≥11.5 | 同 |
| stage | os.tmpdir() 随机目录,**绝不写仓库内文件** | 同 |
| dry-run | `DRY_RUN=1` → 追加 `--dry-run` | 同 |

共享的两个决策:

1. **registry 打不通时照常尝试发布**:"重复版本的错误 < 静默跳过真更新"——npm 会拒绝重复版本兜底(:69-81)。
2. **执行顺序在 Pages deploy 之后**(build-site.yml:281-298;deploy 现于 :238-256):"站点才是大家看的,registry 故障没资格拖住它。"deploy 那一步对探针运行挂 `continue-on-error: schedule||workflow_dispatch`(:256):"deploy 失败也没资格拖住 registry 发布与 cache-save"(2026-09-05 的 403 曾把 36 分钟探针成果全部带走)。

0004 给 catalog 这一个发布器加的三处细节:

- **哈希口径变了**:`sha256(Buffer.concat([built, index]))`(:133)而不是只哈希 plugins.json,所以"只动索引的一天"也会挣到一个版本;注释把理由写明了——哈希是告诉明天的 run "今天没新东西"的唯一信号。
- **文件清单与导出同步**:`files: ['plugins.json', 'index.json']`、`exports` 加 `'./index.json'`(:160-161),README 里给出可直接粘的地址 `https://cdn.jsdelivr.net/npm/dsh-plugin-catalog/index.json`(:112-117)。
- **多了一条硬前置**:脚本无条件读 `docs/index.json`(:130),而 build-site 只在索引至少收录一条插件时才写这个文件(build-site.mjs:182-192——缓存里没有 `publishedAt` 的老条目会让索引为空,此时面板不显示、文件也不落盘)。也就是说发布步骤的前置条件从"plugins.json 存在"变成了"这次 run 的 npm-map 足以产出一份非空索引"。nightly 走 `PROBE_ALL` 全量探针所以恒成立;真正的漏洞在手工 dispatch:带 `skip_probes` 且恢复到的 cache 还是 0004 之前那份(没有 `publishedAt`)时,探针被跳过、索引为空、`docs/index.json` 不存在,而 `publish-catalog.mjs` 没有"没有索引就不发"的分支——它会直接在 `readFileSync` 上抛错。build-site 侧对此是"少写一个文件、少显示一个面板",发布侧是硬失败,两个文件的容错口径不一致。

## prune-legacy-screenshots.mjs:maintainer-run 的清退器(未变)

背景:截图约定已迁到作者仓库(contributing.md §Screenshots),`data/screenshots.json` 是有终点的 fallback——41/773 张已发布截图烂成 404 正是当初动机。本脚本对 legacy 文件里现存的每个 key 探测作者仓库是否已有**可用**声明("a key is only pruned if the declaration would actually be used"),是则删 key;键序显式保留不重排——重排会把几百行无关行染进 diff,破坏 maint-rebase.sh 依赖的 diff 信号。清空即提示可删除整个文件与 build-site 的 fallback 分支。

**0004 期间这个文件确实变小了,但不是它干的**:`data/screenshots.json` 从 289 键降到 288——两次作者要求移除(`b1ebf11a1`、`b039938b9`,2026-10-21)加一条新条目的截图(`f0baef2aa`,2026-10-17)。区间里没有 prune 的运行痕迹,这也符合它的定位:维护者手动跑,不是 CI 步骤。顺带说明这个文件的"新鲜度"没有时间字段可读——它的 age 只能靠 diff 推(见 00-map 的三份边车对照)。

## 0002 新增:adopt-discussions(评论线程的收编层)

它不是探针也不是发布器,而是**同一类"外部世界的数据与我们的 join key 不一致"问题**的第三个受害者(前两个是 npm 包名归属、截图声明)。

- **问题**:giscus 只在"帖子位于 `Plugins` 类目**且**正文含 `<!-- sha1: <sha1(term)> -->`"时才认这个线程;手工在 GitHub UI 建的帖子两个条件都不满足 → 三个界面各显示一个空框,而 giscus **静默开第二条线程**(标题搜索不可用:`plugin:zhu1090093659/dsh-web` 会命中 `--packages-dsh-web-all` 那条)。
- **做法**:补上 marker、移进类目——"never deletes, merges or retitles";幂等。
- **触发**:`discussion: created` 事件(唯一能当场抓住手工帖的时机)+ 每周二 04:17 全量扫(:23-24,顺带把**仓库改名**后的线程重新接上——改名会动 catalog 的 slug,也就动了 widget 要的 term)。
- **权限**:`contents: read` + `discussions: write`(:32-34)——**仓库里第一条写非仓库资源的 workflow**;注释还承认 GitHub 把 discussion webhook 标为 "public preview, subject to change",失效时的兜底是那条每周扫,所以失败模式是延迟而不是劈成两半。
- **配套**:`lib/terms.mjs` 把 `slugOf/termOf` 收成 build-site 与 adopt 共用的单点(此前 catalog 小写化 term,凡是 owner/repo 含大写的条目都被劈成两个线程,2026-09-24 才修)。
- **0004 的唯一改动是安装方式**:`npm ci` 加上 `npm_config_registry: https://registry.npmjs.org/` 与 `npm_config_replace_registry_host: always`(:52-58)。这个 job 本身不碰 npm 生态,但它的脚本经 `lib/entries.mjs` 依赖 `js-yaml`,而 lockfile 里 7 个 `resolved` 指向 registry.npmmirror.com——所以这不是可有可无的优化:`npm ci` 装不上,adopt 连一次都跑不起来。权限、触发、cron 都没变。

## 数据持久化拓扑(与 build-site.yml 的耦合)

```text
nightly(UTC 02:23)                       push / workflow_run on sync-readme
─────────────────────                     ────────────────────────────────
probe-npm → downloads → stars             五个探针全跳过
          → readmes → updates             (缓存命中时)
→ tarballs → screenshots                  → tarballs + screenshots + capabilities
→ probe-capabilities(不在 PROBE_ALL 门控里)  → build-site.mjs
→ build-site.mjs(同时写 docs/index.json)   → deploy pages
→ deploy pages                            (不做 npm 发布)
→ publish catalog(plugins.json + index.json)+ updates(OIDC)
```

- 结果三路持久化:**git 提交的快照**(stars/downloads/added-dates/screenshots/**capabilities**)+ **Actions cache**(共享条目 `probe-data-v2` 一条含 npm-map/stars/readmes/tarballs 四个 path,另有 downloads-v1 与 updates-v1 两条独立 entry)+ 与快照合并;workflow 永不写回 git(`contents: read`,build-site.yml:49)。
- **0004 补充第四种东西:构建产物**。`docs/index.json` 既不是快照也不是缓存——它每次构建从 `data/npm-map.json` 重算(build-site.mjs:182-192),`docs/` 整个目录在 .gitignore:9 被忽略,所以它唯一的副本就是那天的 Pages 部署和 npm 包。换句话说:**索引比任何一份 data 边车都新鲜,却也是唯一一个仓库里找不到的**。
- **0001 勘误(0002 更正)**:快照清单里的 `updates.json` **不是** git 提交物——它从未进过 git 历史,只活在 updates-v1 cache(注释现在也明说 "NOT committed — unlike stars/downloads, there is no committed floor")。真正第五个提交快照是 **capabilities.json**。
- **push 构建的兜底分支(0002 改写)**:条件是 `case schedule|workflow_dispatch → full_probe=1` 的白名单,所以 workflow_run 触发的构建**不会**再临时跑全套探针(旧写法 2026-09-22 让一次 README 同步后的构建在探针里坐了 40 分钟)。0004 给这条兜底加的一处是 2026-10-18 的 `skip_probes`(ac02c4e5d,build-site.yml:176-186):deploy-only 路径必须存在,否则注释里那个日子(索引要赶在用户开始添加它之前上线)只能干等一小时探针。
- push 冷缓存且 `data/npm-map.json` 为空的兜底仍会临时跑 probes:"Probing is slow; that is cheaper than a wrong plugins.json"。

## 待复核

- [ ] cache key 版本(v2/v1/v1)升级流程:改 path 列表 = 全体冷启动,历史上如何操作过
- [ ] updates 包的消费端(dsh-market 对话框)实际拉哪个 URL
- [x] ~~**0002**:capabilities.json 既无回写 workflow、也不在 cache path——夜间的重扫结果是否只活在那次运行的 `docs/plugins.json` 里~~ → **0004 已解**(`contents: read` + 无 cache + 每次构建都跑,已由代码路径回答;棘手的部分变成了"线上那份是新的、仓库那份是旧的",见 [00-map](./00-map.md))
- [ ] **0004 新增**:索引什么时候拆成独立包。现在它让每次 catalog 下载多 684KB,而拆包需要一个只有人才能做的动作(在 npmjs.com 上建包并配 trusted publishing);在那之前,`publish-catalog.mjs` 里那句"这是权宜之计"就是准确的现状。
