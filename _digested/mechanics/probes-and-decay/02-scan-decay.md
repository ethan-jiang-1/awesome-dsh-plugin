# 02 · scan-decay:腐坏判据与人机分工

> 基线:`upstream@b4d0049a8`(0004 复核,2026-10-24)。`scan-decay.mjs` 仍 **388 行**,自 0002 基线 `c18ba4a0d` 起逐字节未变;`decay-scan.yml` 在 0004 唯一的 diff 是 `npm ci` 的 registry 覆盖(6 行,:28-34),触发、权限、并发语义都没动。所以本专题在 0004 没有"新判据",只有两件事:旧判据在真实世界里闭合了一次,以及它的运行环境换了个安装源。

## 职责边界

flag-only,从不删除(scan-decay.mjs:1-12):每周扫全部条目产出 findings,汇总进**单个 tracking issue**(标题固定 `Decay scan: entries that need review`,:36),每项一条 `- [ ]`,首行写着 "**Nothing has been removed** — each item below needs a human decision…"(:355)。删除动作属于维护者人工环节(contributing.md:76)。workflow 权限只有 `issues: write`,物理上不可能动 `data/plugins/*`——机器发现与人判断之间的墙砌了两层。

**0004 期间这条链路至少闭合了一次,而且留下了完整的账**:2026-10-19 的 `2a274d92b` 以 "#2976 decay, 2026-10-19 re-verification" 为名 delist 了 16 条,一个 commit 里删掉两份 README 各 16 行、16 个 `data/plugins/*.yml`、`data/added-dates.json` 1 行、`data/stars.json` 16 个键(32 行);2026-10-21 又有两条按作者要求移除(`b1ebf11a1`、`b039938b9`)。这正是 flag-only 想要的样子——机器只开清单,删除永远发生在人的 commit 里。但同一份账也量出了人工环节的宽度:清一个条目要同时动四处(两份 README、added-dates、yml、stars 键),而 **capabilities 记录不在其中**——那条是第二天单独手工删的(`1a93fa18f`,#8058),因为 probe-capabilities 从不清理名单外的键(见 01-probe-family 的"写盘前")。也就是说,删一条实际上要记住五个地方。

## 0002 新增第五类:`subpath-gone`

0002 把 `hasBundle` 从三值改成**四值**:子路径条目的 `package.json` **不存在** → `'subpath-gone'`(目录搬走了);存在但没有 `dsh.bundle` → `false`(不再打包成插件)。注释解释了为什么必须分开:

> "A missing package.json at the subpath means the DIRECTORY is gone … Reporting the first as 'dsh.bundle no longer found' sends the maintainer to open a deadline when the actual fix is a one-line repoint"

真实案例:baosfeng 的条目把 `plugins/dsh-notify` 改成了 `plugins/dsh-my-notify`——一个一行的重指,旧文案却把它报成"插件坏了"。issue 正文也为此新增了一段(:357),那段顺带写明了两条人工注意事项:改条目文件名会重置派生的 added-date(要去 `data/added-dates.json` 里钉新 URL),以及要顺手检查 `data/screenshots.json` / `data/stars.json` 里还带着旧 URL 的键——**遗留的截图键会直接把构建打挂**。

## 五类判据(更新后)

| kind | 判据 | 关键实现细节 |
|------|------|--------------|
| gone | GraphQL NOT_FOUND **且 REST 复核也 404** | GraphQL 对 rename 未必像 REST 那样 301,所以 NOT_FOUND 只是一票怀疑,必须二次确认才可判死 |
| archived | `repository.isArchived` | detail 附最后 push 日期 |
| **subpath-gone(0002 新增)** | 子包路径下没有 package.json | 与 unbundled 分开:前者是"目录搬了",后者是"不再打包" |
| unbundled | hasBundle 得 `false`(manifest 在、但清单没了)| |
| dormant | `(now − pushedAt)/(30.44×86400s) ≥ DORMANT_MONTHS(6)` | 30.44 = 月均天数 |

KINDS 顺序(issue 内分节顺序,`gone → archived → subpath-gone → unbundled → dormant`,:313-322);`scan()` 的判定优先级仍是 `gone → archived → dormant → subpath-gone/unbundled`(先判死、再判睡,最后才判"装不上")。`subpath-gone` 刻意排在 `unbundled` 之前,注释给的理由是维护负担:前者通常当天就能清掉,后者要开 deadline 等一周。

第五状态 **INCONCLUSIVE**:显式 sentinel,区别于 healthy(null)。总闸门:不确定率 > `ceil(N×0.05)` → stderr 报错 exit(1),**整份报告不发**。"A scan that could not look at a meaningful share of the list has not produced a decay report; it has produced a shorter one."(--dry-run 在此闸门之后 exit)

## hasBundle 四值探测

- 有 sub(monorepo 子包)→ **只看该子包的 manifest**,不关兄弟包的事(注释给了 dsh-desktop-base 反例);该路径缺 package.json ⇒ `'subpath-gone'`(:212-213);
- 否则先零成本读根 manifest;
- 根没有才走 tree 枚举:`truncated` → inconclusive;读到任何 `dsh.bundle` → true;超 MAX_TREE_PKGS(40)或有 unreadable → inconclusive,**绝不因没读完而下否定结论**——和 check-submission.mjs 的同款纪律完全一致(两处独立实现,同一哲学);
- manifest 抓取走 raw.githubusercontent.com(不计 API 配额);BOM 剥离曾救回 3 个健康的 Windows 编辑器保存的条目;JSON 解析失败 → null(broken repository ≠ removed bundle)。

## 成本工程

- 元数据用 GraphQL 别名批量:50 repo/查询,~34 个请求替代 ~1650 次 REST;
- 每 repo 至多:1 GraphQL 点 + (可疑时)1 REST 复核 + ≤40 次 raw manifest(免费)。
- **0004 的运行环境改动**:这个 job 里唯一的依赖安装是 `npm ci`(脚本经 `lib/entries.mjs` 才用到 `js-yaml`,scan-decay.mjs:24),而 lockfile 里 7 个 `resolved` 指向 registry.npmmirror.com;那个 CDN 在 GitHub runner 上反复 503/504,把 `npm ci` 挂住几十分钟(注释日期 2026-10-19)。于是 `decay-scan.yml:28-34` 显式加上 `npm_config_registry: https://registry.npmjs.org/` 与 `npm_config_replace_registry_host: always`。这条**只改变工具从哪装下来**:扫描自己发的所有请求仍是脚本里的硬编码 URL,不读 npm 配置;它影响的是"这个 job 能不能开始跑",不是"它看到什么"。同一枚覆盖也加在 adopt-discussions/build-site/pr-check/pr-gate/sync-readme 上(13dcda271),六个 workflow 一致。

## issue 发布协议

search/issues 按**精确 title**(固定字符串,:377)+ open 状态找既有 issue:找到就 PATCH 原地更新 body(一个长期滚动清单,不开新 issue);没有且有 findings 才新建(label `['list']`,与 ISSUE_TEMPLATE 的标签同一枚,:384);没有且零 findings 就什么都不做。支持 `--dry-run` 与 `--limit=N`。0004 期间那份清单被真的执行了:delist commit 的消息写着 "#2976 decay, 2026-10-19 re-verification"——它引用的是一份长期存在的公告板,而不是一次性的 PR。

## 与 pr-check / contributing 口径的对齐

contributing.md 把周期扫描描述为"标记消失、归档或长期停更的条目"。对照本实现的五类:gone/archived/dormant 与文案一一对应;`unbundled` 与新增的 `subpath-gone` 是文案没提但最实用的两类——它们抓的不是死链而是**装不上了**(上游重构导致 dsh.bundle 搬家或丢失),恰是"能安装"这条收录底线本身。0004 的 delist 集中在最粗的那一档:commit message 的原话是 "16 entries whose repositories are gone",说明 gone 仍是实际工作量的大头。

## 待复核

- [ ] **0002 遗留**:`subpath-gone` 是否会与"子路径写错但仓库仍在"混淆——两者的修正动作不同(重指 vs 删除),但判据都是"这里没有 package.json",需要抽样看 issue 正文的措辞是否够分辨。0004 期间没有出现 `subpath-gone` 样本(delist 全是 gone),这一项仍然只靠注释里的 baosfeng 案例支撑;本次复核没有读线上 issue 正文,措辞是否够用**未核验**。
- [ ] **0004 新增**:delist 之后 capabilities 记录需要手工清(1a93fa18f),因为 writer 没有名单清理。要不要把 `listed` 删除循环加进 probe-capabilities(代价是要先决定"名单"以 YAML 还是 README 为准),待商榷——见 01-probe-family 的"写盘前"。
