# 02 · scan-decay:腐坏判据与人机分工

> 基线:`upstream@c18ba4a0d`(0002 复核;scan-decay 364→**388 行**,`decay-scan.yml` 未变)。

## 职责边界

flag-only,从不删除(scan-decay.mjs:1-12):每周扫全部条目产出 findings,汇总进**单个 tracking issue**,每项一条 `- [ ]`,首行写着 "**Nothing has been removed** — each item below needs a human decision…"。删除动作属于维护者人工环节(contributing.md:76)。workflow 权限只有 `issues: write`,物理上不可能动 `data/plugins/*`——机器发现与人判断之间的墙砌了两层。

## 0002 新增第五类:`subpath-gone`

0002 把 `hasBundle` 从三值改成**四值**:子路径条目的 `package.json` **不存在** → `'subpath-gone'`(目录搬走了);存在但没有 `dsh.bundle` → `false`(不再打包成插件)。注释解释了为什么必须分开:

> "A missing package.json at the subpath means the DIRECTORY is gone … Reporting the first as 'dsh.bundle no longer found' sends the maintainer to open a deadline when the actual fix is a one-line repoint"

真实案例:baosfeng 的条目把 `plugins/dsh-notify` 改成了 `plugins/dsh-my-notify`——一个一行的重指,旧文案却把它报成"插件坏了"。issue 正文也为此新增了一段。

## 五类判据(更新后)

| kind | 判据 | 关键实现细节 |
|------|------|--------------|
| gone | GraphQL NOT_FOUND **且 REST 复核也 404** | GraphQL 对 rename 未必像 REST 那样 301,所以 NOT_FOUND 只是一票怀疑,必须二次确认才可判死 |
| archived | `repository.isArchived` | detail 附最后 push 日期 |
| **subpath-gone(0002 新增)** | 子包路径下没有 package.json | 与 unbundled 分开:前者是"目录搬了",后者是"不再打包" |
| unbundled | hasBundle 得 `false`(manifest 在、但清单没了)| |
| dormant | `(now − pushedAt)/(30.44×86400s) ≥ DORMANT_MONTHS(6)` | 30.44 = 月均天数 |

KINDS 顺序(issue 内分节顺序)`gone → archived → subpath-gone → unbundled → dormant`(:313-319);`scan()` 的判定优先级仍是 `gone → archived → dormant → subpath-gone/unbundled`(先判死、再判睡,最后才判"装不上")。

第五状态 **INCONCLUSIVE**:显式 sentinel,区别于 healthy(null)。总闸门:不确定率 > `ceil(N×0.05)` → stderr 报错 exit(1),**整份报告不发**。"A scan that could not look at a meaningful share of the list has not produced a decay report; it has produced a shorter one."(--dry-run 在此闸门之后 exit)

## hasBundle 四值探测

- 有 sub(monorepo 子包)→ **只看该子包的 manifest**,不关兄弟包的事(注释给了 dsh-desktop-base 反例);该路径缺 package.json ⇒ `'subpath-gone'`(:212);
- 否则先零成本读根 manifest;
- 根没有才走 tree 枚举:`truncated` → inconclusive;读到任何 `dsh.bundle` → true;超 MAX_TREE_PKGS(40)或有 unreadable → inconclusive,**绝不因没读完而下否定结论**——和 check-submission.mjs 的同款纪律完全一致(两处独立实现,同一哲学);
- manifest 抓取走 raw.githubusercontent.com(不计 API 配额);BOM 剥离曾救回 3 个健康的 Windows 编辑器保存的条目;JSON 解析失败 → null(broken repository ≠ removed bundle)。

## 成本工程

- 元数据用 GraphQL 别名批量:50 repo/查询,~34 个请求替代 ~1650 次 REST;
- 每 repo 至多:1 GraphQL 点 + (可疑时)1 REST 复核 + ≤40 次 raw manifest(免费)。

## issue 发布协议

search/issues 按**精确 title**(固定字符串)+ open 状态找既有 issue:找到就 PATCH 原地更新 body(一个长期滚动清单,不开新 issue);没有且有 findings 才新建(label `['list']`,与 ISSUE_TEMPLATE 的标签同一枚);没有且零 findings 就什么都不做。支持 `--dry-run` 与 `--limit=N`。

## 与 pr-check / contributing 口径的对齐

contributing.md 把周期扫描描述为"标记消失、归档或长期停更的条目"。对照本实现的五类:gone/archived/dormant 与文案一一对应;`unbundled` 与新增的 `subpath-gone` 是文案没提但最实用的两类——它们抓的不是死链而是**装不上了**(上游重构导致 dsh.bundle 搬家或丢失),恰是"能安装"这条收录底线本身。

## 待复核

- [ ] **0002**:`subpath-gone` 是否会与"子路径写错但仓库仍在"混淆——两者的修正动作不同(重指 vs 删除),但判据都是"这里没有 package.json",需要抽样看 issue 正文的措辞是否够分辨
