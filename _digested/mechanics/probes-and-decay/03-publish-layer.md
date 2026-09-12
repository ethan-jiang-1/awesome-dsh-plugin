# 03 · 发布层:npm 双包与 legacy 截图清退

> 基线:`upstream@38976afd`(0001 复核;发布脚本未变,build-site.yml 行号已更新)。

## 为什么发 npm(注释里有真实测量)

- Pages 就是 GitHub(响应头 `server: GitHub.com`),大陆访问慢;公共 GitHub 反代一律拒非 github.com 的 hostname(实测该域名 403)。发到 registry.npmjs.org 就**复用了插件生态本来就在用的镜像体系**(publish-catalog.mjs:3-14)。
- 单独成包而非塞进 `awesome-dsh-plugin` 包:npm 强制携带 README(两个 README 各 ~500KB),`npm pack --dry-run` 测得 772KB vs 独立 ~250KB;独立包还让目录获得版本号、可回滚(:15-27)。
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

1. **registry 打不通时照常尝试发布**(:60-63):"重复版本的错误 < 静默跳过真更新"——npm 会拒绝重复版本兜底。
2. **执行顺序在 Pages deploy 之后**(build-site.yml:222-239;deploy 现于 :178-197):"站点才是大家看的,registry 故障没资格拖住它。"**0001 增量**:deploy 步骤对探针运行挂 `continue-on-error: schedule||workflow_dispatch`(:197)——镜像句同样成立:"deploy 失败也没资格拖住 registry 发布与 cache-save——run 存在的理由是探针+发布,不是部署"(2026-09-05 的 403 曾把 36 分钟探针成果全部带走)。

## prune-legacy-screenshots.mjs:maintainer-run 的清退器

背景:截图约定已迁到作者仓库(contributing.md §Screenshots),`data/screenshots.json` 是有终点的 fallback——41/773 张已发布截图烂成 404 正是当初动机。本脚本对 legacy 文件里现存的每个 key 探测作者仓库是否已有**可用**声明("a key is only pruned if the declaration would actually be used"),是则删 key;键序显式保留不重排(:106-112)——重排会把几百行无关行染进 diff,破坏 maint-rebase.sh 依赖的 diff 信号。清空即提示可删除整个文件与 build-site 的 fallback 分支。

## 数据持久化拓扑(与 build-site.yml 的耦合)

```
nightly(UTC 02:23)                       push 到 main
─────────────────────                     ─────────────
probe-npm → downloads → stars             五个 probe 全跳过
          → readmes → updates             (缓存命中时)
→ tarballs → screenshots                  → tarballs + screenshots
→ build-site.mjs                          → build-site.mjs
→ deploy pages                            → deploy pages
→ publish catalog + updates(OIDC)        (不做 npm 发布)
```

- 结果三路持久化:**git 提交的快照**(stars/downloads/updates/screenshots.json)+ **Actions cache**(共享 entry `probe-data-v2` 一条含 npm-map/stars/readmes/tarballs 四个 path(#1673 后按文件分组防版本连锁失效),另有 downloads-v1 与 updates-v1 两条独立 entry)+ 与快照合并;**唯独永不写回 git**(workflow `contents: read`)。push 构建靠 cache 把夜间成果带进当次 docs/(这正是 #2797 里 downloads 一度比 npm 真实值低 42% 的事故面)。**0001 增量**:并发组拆分(build-site.yml:48-50)后 push/nightly 分属 `build-site-push`/`build-site-probe` 两组、可同时在飞——push 不再能取消 nightly(动机链在 :32-47:#3512 catalog 冻结三天、#3417/#3698 READMEs 卡旧值,根源都是 nightly 被 push 中途取消)。
- push 冷缓存且 `data/npm-map.json` 为空的兜底分支也会临时跑 probes:"Probing is slow; that is cheaper than a wrong plugins.json"(build-site.yml 注释)。

## 待复核

- [ ] cache key 版本(v2/v1/v1)升级流程:改 path 列表 = 全体冷启动,历史上如何操作过(git log cache 相关键)
- [ ] updates 包的消费端(dsh-market 对话框)实际拉哪个 URL
