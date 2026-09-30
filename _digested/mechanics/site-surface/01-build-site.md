# 01 · build-site 主干与部署链

> 基线:`upstream@c18ba4a0d`(0002 复核)。行号 = scripts/build-site.mjs(**1174 行**,1098→1174)除注明外。0001 核心变更:README 生成归属重构(sync-readme.yml)、AdSense/Giscus 注入、并发组拆分、added-date 双账本、plugins.json 新增 version。**0002 核心变更:能力披露三字段进 plugins.json、下载窗口显式化(含 start/end/checkedAt)、added-date 加"改写不算新增"守卫、slug/giscus term 不再小写化、site-health 看门狗、build-site 增加 `workflow_run` 触发 + 探针事件白名单。**

## 阶段流水

1. **常量与资产**(:19-53):`ORIGIN='https://awesome-dsh-plugin.com'` 硬编码;`site/assets/*` 平铺拷进 `docs/` 根(CNAME、robots.txt、badge.svg、logo.svg、双语 banner/og PNG、两个 woff2 字体子集、404.html);字体自托管的理由写在 template.html:27-31("a webfont request hands the visitor's IP to a third party on every page view")。**0002:`site/` 目录零 diff**——模板、locales、隐私页、ads.txt、Giscus 脚本全部未动。
2. **解析 README 花名册**(:99-160):en 要求分隔符 `-`、zh 要求 `—`(取自 loc.sep);五类 parity 失败全部置 `parityBroken` → exit 1,"refusing to build (a silent drop would delist and delete pages)":同 locale 内 URL 重复 / 分隔符不符 / 某语言缺 URL / 同 URL 两语言分类不同(#343)/ 只存在于另一语言。分类归属是**标题子串匹配**(`h[1].includes(loc.categories[id])`)。
3. **数据加载与派生**(:170-471):
   - `added-dates.json` 是人工拥有的**冻结基线**(2026-08-15 前固定);缺失日期改用**双账本推导**(README 账本 :216-269 + 条目 yml 账本 :270-290;`scripts/lib/added-dates.mjs:15` 抽出 `firstAddedDate`,走 `git log --diff-merges=first-parent --no-patch --diff-filter=A`,取最旧)。
     - **0002 新增守卫**:一个 commit 里同时 `-` 掉并 `+` 上同一 URL 视为**改写**,不再认领当天日期(逐 commit 维护 `addedHere`/`removedHere` 后 `flush()`)。动机是实测事故:2026-09-15 一次会话里两条目被改写到当天(siyuan-codex-bridge 09-11 → 09-15、thinking-token-stat 09-06 → 09-15)。
     - **0002 新增第二本账**:整仓一次 `--name-only` 的 yml 账本(:270-290),只用于被改写的 URL,"costs ~1.4s instead of minutes";**不回填历史**(约 120 条会被它提前一两天的旧目录刻意不重判)。
     - 抽出 `lib/added-dates.mjs` 的直接原因写在注释里:这条路径"had no test at all when it took the site down"(#4756,配 `scripts/added-dates.test.mjs`)。
   - **星数覆盖率地板** `STARS_MIN_COVERAGE = 0.66`(:205-210):未设 `SKIP_PUBLISH_CHECKS=1` 且覆盖率不足直接 throw(#1673 的 stars:{}×1362 教训;floor 判"磁盘已有",因为新条目合法地没有星数)。
   - **下载窗口显式化(0002 新增,`scripts/download-window.mjs`,16 行)**:月下载一律用显式 UTC 窗口(结束=昨天、起点=结束−29 天),并**拒收** `start/end` 与请求不符、或 downloads 不是非负安全整数的响应——相对时间端点会返回旧缓存窗口(#5309)。配套 `scripts/download-window.test.mjs` 进了 build-site.yml 的测试步骤(:85)。这是本仓库第一次把回归测试挂进构建。
   - 截图:host 白名单四个 GitHub 域(:350-371;key 必须 URL 精确匹配已列条目)、1–8 张、超限 exit 1。
   - 三方合并:`declared`(作者仓库的 screenshots.json)> legacy key;live verdict 仅剔除 ok:false(404/410),全死删整个字段而不是留空数组。
   - slug 规则(:456):`slugOf()` 移入 `scripts/lib/terms.mjs:22`(`repo--sub路径(/→-)`,无 sub 则 repo 本身),与 adopt-discussions 共用同一份实现。
4. **页面生成**(四轮循环):首页(:597)+ 分类页(:636,空分类跳过)+ 隐私页(:681-707,缺 privacyBody 文件 exit 1,检查在 :683-684)+ 详情页 ×约 8784。替换实现分两类:**结构块用 regex+回调函数**(避免 `$&` 类特殊序列被展开),标量 token 用 `replaceAll('__X__', () => v)` 同样带回调。index/category 两轮新增 `__CARD_COUNT__`(:620/:668,服务端渲染计数,消除 #count CLS)与 `AD_HEAD_TOKEN`(:621/:669)。孤儿详情页清理:重建 live slug 集合后 rmSync 不匹配者(:961-976)。
5. **README 渲染**(`renderReadme` :723):Marked + heading depth+1(cap 6)、相对链接基于 raw base 解析;`renderer.html` 返回空串——**详情页正文里裸 HTML 全部丢弃**;图片必须过 SCREENSHOT_HOSTS(允许 `data:`),丢图后清理空 `<a>`/`<p>`。多语言选择按 LOCALES 顺序回退,兼容旧的无 key 结构,命中非本页语言时提示 P_README_ONLY 并在包裹 div 标真实 lang。
6. **数据产物**:

| 产物 | 内容 | 关键点 |
|------|------|--------|
| `docs/plugins.json` | 完整注册表(name/owner/url/page/category/desc/npm/version/tarball/stars/downloads/install/added/screenshots + **0002 新增 downloadsStart/downloadsEnd/downloadsCheckedAt + capabilities/capabilityRedLines/capabilityCheckedAt**)| tarball 键 absent 时省略而非 null;version 赋值 :451、registry 发射 :1037(= npm dist-tags.latest,null=github-only 或无 latest,消费方 dsh-market#348);**能力三字段在未扫描时整个键省略**(:1042-1050)——注释明说"so a consumer cannot read 'absent' as 'empty'",市场侧渲染成"未检出 / not checked"(#401);下载三字段来自显式 UTC 窗口(:1039-1041);updates **故意不并入**(市场每次打开都拉这个文件,release body 会撑爆,:712-718)|
| `docs/count.json` | shields endpoint schema `{schemaVersion,message:N,color,cacheSeconds:300}` | README 徽章的消费端;cacheSeconds 取 shields 下限 300,因为徽章下面就是列表,数对不上会被当 bug |
| `docs/readmes.json` | 详情页正文源(locale→{md,base,blobBase})| MB 级 |
| `docs/updates.json` | 来自 `data/updates.json`(cache-only,见 [probes-and-decay/03](../probes-and-decay/03-publish-layer.md)),仅 listed | KB 级 |
| `docs/feed.xml` ×2 | 按 addedAt 倒序 newest 30 条 | |
| `docs/sitemap.xml` | 四类 URL + 全套 hreflang alternates | 分类页 daily、详情页 weekly(lastmod=e.added)、隐私页 yearly,lastmod 取隐私源文件最后 commit 日期——"lastmod 每晚移动而内容没变会让爬虫不再相信全站的 lastmod" |

## 部署链(build-site.yml,282 行)

- **触发**:nightly cron `23 2 * * *` + workflow_dispatch(带 probe_all input)+ push 到 main(无 paths 过滤,刻意)+ **0002 新增 `workflow_run` on "Sync READMEs from data/plugins" completed**(:26-28)。理由写在注释里:bot 的 GITHUB_TOKEN 推送不触发 push 事件,"so the site stays exactly one merge behind";2026-09-20 实测 main 4,014 条 / 已发布 4,012,且 bot 的 sha 上没有任何 build-site 运行。选 workflow_run 而非 dispatch 是为了不加权限面。并发组仍在(:65-67):`build-site-push` / `build-site-probe`——push(含 workflow_run)只取代 push 构建,**永远不能取消 nightly**。
- **探针门从黑名单改白名单(0002)**:旧逻辑 `event != 'push'` 导致每次 sync-readme 完成都跑全量探针,2026-09-22 有一次在这步坐了 40 分钟(纯部署构建约 12 分钟);现为 `case schedule|workflow_dispatch → full_probe=1`(:158-171)。push/workflow_run 构建跳过 npm/downloads/stars/readmes/updates 五个探针,**始终跑 tarballs、screenshots 与 capabilities**(:198-216)——"Probing is slow; that is cheaper than a wrong plugins.json"。
- **不变量**:`permissions: contents: read`(build-site.yml:41);注释 "The build never writes to the repository." 仍在——**该不变量只对 build-site 链成立**;仓库里唯一向 main 写入的是 sync-readme.yml(bot 提交 README,:32-33)。
- **三层缓存**(probe-data-v2 共享条目 / downloads-v1 / updates-v1 刻意分离,#1673 后防版本连锁失效;#2797:downloads 不单独缓存时线上下载量比 npm 真实值低约 42%)。**0002 更正**:`data/updates.json` 是 **cache-only**,"NOT committed — unlike stars/downloads, there is no committed floor"(0001 曾误记为已提交边车)。
- **npm 发布(catalog/updates 双包)在 deploy 之后**(:265-282),且仅 nightly/manual。凭据 OIDC trusted publishing(`id-token: write`,npm ≥11.5);**deploy 失败对探针运行 continue-on-error**(:240),deploy 之败没资格拖住两个 publish 与 cache-save。
- **新增测试步骤**(:85):`node --test scripts/download-window.test.mjs`。

## 已知文档漂移

- build-site.mjs:9 注释声称 "re-syncs the plugin-count figure inside every README"——build 全文写盘调用无一触及 README,计数徽章走 shields endpoint。**过期注释,行为是「build 从不碰源文件」**;0001 后这句话有了例外形态:写 README 的是 sync-readme.yml,不是 build。
- AdSense 头注入(`adHead()`,build-site.mjs:72,变量未设时返回空串,`__AD_HEAD__\n` 连换行一起替换——**未设变量时产物与无广告构建逐字节相同**;注入点 :621/:669/:942,privacy-template 没有)与 Giscus 评论懒加载(`mapping:'specific'` 按 `plugin:<slug>` 映射 Discussion、IntersectionObserver 400px 触发才注入 script——**不滚动=不联系第三方**;enabled 时四 ID 强校验)。
- **0002 修复的静默漂移**:giscus 的 term 从"构建时小写化"改为 `termOf(e.slug)` 原样(:856)。自评论区上线到 2026-09-24,这条小写化让**所有 owner/repo 含大写的条目被劈成两个 Discussion**——市场问 `plugin:FeatherHunter/dsh-prompt`,catalog 答 `plugin:featherhunter/dsh-prompt`,"Two threads, neither wrong"。同一份 `slugOf/termOf` 现由 build-site 与 adopt-discussions 共用(`lib/terms.mjs`)。

## 待复核

- [ ] checkout + Pages 上传的实际耗时分布(workflow 无计时输出;UNVERIFIED)
- [x] ~~会不会自动提交 README~~ → build-site 链不会;**0001 起 sync-readme.yml 会**(仓库唯一写 main 的 workflow),见上
- [ ] 0002:capabilities 三字段写进了 plugins.json,但**站内页面不渲染**(site/ 零 diff 且模板无对应 token)——确认消费方只有 dsh-market
- [ ] 0002:约 8800+ 页是 4392×2+2×25 的推算值,没有构建日志佐证(UNVERIFIED)
