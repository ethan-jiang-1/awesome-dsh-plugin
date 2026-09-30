# 03 · 发布层:npm 双包、legacy 截图清退与评论线程收编

> 基线:`upstream@c18ba4a0d`(0002 复核;两个 publish 脚本与 prune 未变,build-site.yml 行号已更新为 282 行版)。

## 为什么发 npm(注释里有真实测量)

- Pages 就是 GitHub(响应头 `server: GitHub.com`),大陆访问慢;公共 GitHub 反代一律拒非 github.com 的 hostname(实测该域名 403)。发到 registry.npmjs.org 就**复用了插件生态本来就在用的镜像体系**(publish-catalog.mjs:3-14)。
- 单独成包而非塞进 `awesome-dsh-plugin` 包:npm 强制携带 README(两个 README 各 ~500KB),`npm pack --dry-run` 测得 772KB vs 独立 ~250KB;独立包还让目录获得版本号、可回滚。
- updates 与 catalog 拆成两包:catalog tarball 被每个 market 每次升级都拉,update notes 只被打开对话框的那一个用户读;合并会让全体消费者的每日下载翻倍(publish-updates.mjs:9-15)。

## 两个发布器的同构机制

| | dsh-plugin-catalog | dsh-plugin-updates |
|---|---|---|
| 内容 | `docs/plugins.json`(原字节)| `docs/updates.json` |
| 幂等键 | packument 自定义字段 `catalogSha`=sha256 | `updatesSha` |
| 版本 | `YYYY.MDD.RUN`(月份不补零——semver 禁前置零;日期部分跨年可比)| 同 |
| 凭据 | trusted publishing(OIDC),需 `id-token: write` + npm ≥11.5 | 同 |
| stage | os.tmpdir() 随机目录,**绝不写仓库内文件** | 同 |
| dry-run | `DRY_RUN=1` → 追加 `--dry-run` | 同 |

共享的两个决策:

1. **registry 打不通时照常尝试发布**:"重复版本的错误 < 静默跳过真更新"——npm 会拒绝重复版本兜底。
2. **执行顺序在 Pages deploy 之后**(build-site.yml:265-282;deploy 现于 :178-240):"站点才是大家看的,registry 故障没资格拖住它。"deploy 步骤对探针运行挂 `continue-on-error: schedule||workflow_dispatch`(:240)——"deploy 失败也没资格拖住 registry 发布与 cache-save"(2026-09-05 的 403 曾把 36 分钟探针成果全部带走)。

## prune-legacy-screenshots.mjs:maintainer-run 的清退器(未变)

背景:截图约定已迁到作者仓库(contributing.md §Screenshots),`data/screenshots.json` 是有终点的 fallback——41/773 张已发布截图烂成 404 正是当初动机。本脚本对 legacy 文件里现存的每个 key 探测作者仓库是否已有**可用**声明("a key is only pruned if the declaration would actually be used"),是则删 key;键序显式保留不重排——重排会把几百行无关行染进 diff,破坏 maint-rebase.sh 依赖的 diff 信号。清空即提示可删除整个文件与 build-site 的 fallback 分支。

## 0002 新增:adopt-discussions(评论线程的收编层)

它不是探针也不是发布器,而是**同一类"外部世界的数据与我们的 join key 不一致"问题**的第三个受害者(前两个是 npm 包名归属、截图声明)。

- **问题**:giscus 只在"帖子位于 `Plugins` 类目**且**正文含 `<!-- sha1: <sha1(term)> -->`"时才认这个线程;手工在 GitHub UI 建的帖子两个条件都不满足 → 三个界面各显示一个空框,而 giscus **静默开第二条线程**(标题搜索不可用:`plugin:zhu1090093659/dsh-web` 会命中 `--packages-dsh-web-all` 那条)。
- **做法**:补上 marker、移进类目——"never deletes, merges or retitles";幂等。
- **触发**:`discussion: created` 事件(唯一能当场抓住手工帖的时机)+ 每周二 04:17 全量扫(顺带把**仓库改名**后的线程重新接上——改名会动 catalog 的 slug,也就动了 widget 要的 term)。
- **权限**:`contents: read` + `discussions: write`——**仓库里第一条写非仓库资源的 workflow**;注释还承认 GitHub 把 discussion webhook 标为 "public preview, subject to change",失效时的兜底是那条每周扫,所以失败模式是延迟而不是劈成两半。
- **配套**:`lib/terms.mjs` 把 `slugOf/termOf` 收成 build-site 与 adopt 共用的单点(此前 catalog 小写化 term,凡是 owner/repo 含大写的条目都被劈成两个线程,2026-09-24 才修)。

## 数据持久化拓扑(与 build-site.yml 的耦合)

```text
nightly(UTC 02:23)                       push / workflow_run on sync-readme
─────────────────────                     ────────────────────────────────
probe-npm → downloads → stars             五个探针全跳过
          → readmes → updates             (缓存命中时)
→ tarballs → screenshots                  → tarballs + screenshots + capabilities
→ probe-capabilities(不在 PROBE_ALL 门控里)  → build-site.mjs
→ build-site.mjs                          → deploy pages
→ deploy pages                            (不做 npm 发布)
→ publish catalog + updates(OIDC)
```

- 结果三路持久化:**git 提交的快照**(stars/downloads/added-dates/screenshots/**capabilities**)+ **Actions cache**(共享条目 `probe-data-v2` 一条含 npm-map/stars/readmes/tarballs 四个 path,另有 downloads-v1 与 updates-v1 两条独立 entry)+ 与快照合并;workflow 永不写回 git(`contents: read`)。
- **0001 勘误(0002 更正)**:快照清单里的 `updates.json` **不是** git 提交物——它从未进过 git 历史,只活在 updates-v1 cache(注释现在也明说 "NOT committed — unlike stars/downloads, there is no committed floor")。真正第五个提交快照是 **capabilities.json**。
- **push 构建的兜底分支(0002 改写)**:条件是 `case schedule|workflow_dispatch → full_probe=1` 的白名单,所以 workflow_run 触发的构建**不会**再临时跑全套探针(旧写法 2026-09-22 让一次 README 同步后的构建在探针里坐了 40 分钟)。
- push 冷缓存且 `data/npm-map.json` 为空的兜底仍会临时跑 probes:"Probing is slow; that is cheaper than a wrong plugins.json"。

## 待复核

- [ ] cache key 版本(v2/v1/v1)升级流程:改 path 列表 = 全体冷启动,历史上如何操作过
- [ ] updates 包的消费端(dsh-market 对话框)实际拉哪个 URL
- [ ] **0002 新增**:capabilities.json 既无回写 workflow、也不在 cache path——夜间的重扫结果是否只活在那次运行的 `docs/plugins.json` 里(UNVERIFIED,见 [00-map](./00-map.md))
