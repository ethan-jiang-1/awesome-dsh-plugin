# `_digested/` 工作纪律

本目录消化 awesome-dsh-plugin 上游(**评估者视角**:看清生态分布与趋势 → 识别真锚与新苗子 → 直接拿走经过源码验证的干货借鉴,不用反复回原 repo 翻)。上游每周涨几千条、源码每轮都可能变,所以这里定的不是僵化模板,是**不可动摇的底线 + 长期生长约束 + 裁量空间**。

---

## 一、三条底线(不可动摇)

任何一条破了,产出就是错的——不是"不够好",是**误导读者**。

### 底线 1:数字必须可复现,且分母先对上

- 所有结构数字来自 `census.py`(全量)或 `delta.py <old> <new>`(两期),不许手算、不许估。
- 跑完先核对:`census` 总数 == `ls data/plugins/*.yml | wc -l`,且 **0 解析失败**。不符就**先修解析器再落任何数字**——手写解析器对 js-yaml 合法形态的漏收已发生六次(行内注释、JSON-in-.yml、折叠标量、整文件缩进、缩进支持引入的 en/zh 回归),每次都静默少分母。
- 标签命中数与中文描述数要抽查一眼:突然塌缩 = description 解析坏了。

### 底线 2:时效与来源永远标在数字旁边

- 仓库自带星标/下载边车冻结于 `2026-08-19`,引用历史边车**必须**带 ⚠ 与日期;实时声量统一走三层分层雷达(`live_probe.py` 卡片全量 + `radar_probe.py --delta/--full` 纯 GraphQL 星标与过线补 npm,详见 [`_method/02`](_method/02-anchor-metrics.md))。
- 每页顶部写清:本期区间、基线 hash、数据截止日与快照覆盖率;快照未覆盖或 npm 404 记 `—` / 缺口,**绝不写 0**。
- 区分 `pre-dsh-host`(2026-08-13 前建仓的宿主/母项目背书)与 `dsh-native`(原生新仓),禁止把宿主高星写成“DSH 插件采用量”,禁止把不同采样日期的数字混进同一个增量句。

### 底线 3:单卡只研究自己,必须读过源码,且读者优先

- 一张卡只回答"它替谁解决什么、值不值得用、到底是什么、怎么实现、代价是什么"。**不与其他卡对比、不搬另一张卡的事实**——对比放子分类 `README.md` 或 `_view/03-anchors.md`,跨卡可借鉴模式收口到 [`_view/04-leverage.md`](_view/04-leverage.md)。
- 卡片头必须写证据等级(★ 注册表自述 / ★★ 读过 README 或文档 / ★★★ 源码级)与日期;**★★★ 必须带 `repo@commit <hash>`**,★★ 尽量记参考坐标(`git ls-remote` 也算),但不得冒充读过源码。
- 每条机制性断言指向具体文件/行号;没读到就写「待验证」,**不许由自述推断**。
- 与本机 DSH 源码、官方包的对照属于证据,允许。
- **新卡与升级卡(`asof >= 2026-11-25`)强制遵循 [`_view/WRITING.md`](_view/WRITING.md)**:先写「它替谁解决什么问题 / 适用面:谁该用、谁别用 / 业务价值」三节,再进八段(`verify.mjs` 自动校验顺序与存在性)。

---

## 二、三棵树分工与长期生长规则(增长时必守)

本仓库的研究材料分为三棵互补目录,新增内容前先落位,不混放、不重复抄写:

| 目录 | 定位 | 维护节奏 | 校验器 |
|---|---|---|---|
| **`_digested/`** | 主入口与常态跟踪:生态结构(`ecosystem/`)、上游机制(`mechanics/`)、四块板(`_view/01~04`)、领域册与源码单卡(`view_*/`) | 随上游同步持续刷新 | `node _digested/verify.mjs` + `ecosystem/test_*.py` |
| **`_leverage/`** | 横向深度杠杆四册(门禁权限 / 多 Agent 协作 / 产品形态 / 分发首启),物理自包含 | 按机制被验证增量增长 | `node _leverage/verify.mjs` |
| **`_faq_on_digested/`** | ad-hoc 跨领域深挖工坊:回答一次性综合困惑,不背每轮同步重算负担 | 按需新增;若某题长成持续赛道(如 `02_superagent-dependents`),升级为 `_digested/view_<topic>/` | `node _digested/verify.mjs` |

### 双轨 `view_*` 领域册(类目大册 + 跨域专题册)

- `_digested/view_*` 平铺容纳两类专册:**类目大册**(对应官方主类如 `ui/tools/session/workflow/memory`)与**跨域专题册**(按读者问题横跨多类,如 `view_proactive_agent`)。
- 新立任意 `view_<domain>/` 必须满足闭环(`verify.mjs` 自动发现并强制校验):
  1. 册内齐备 `README.md`(按 `WRITING.md` §二 含「读者与价值」)、`AGENTS.md`(写本册特有判断线索并指向 `../_view/WRITING.md`)、`plugin-map.svg`;
  2. 在 [`_view/README.md`](_view/README.md) 册表登记一行并显式标注类型(`类目大册` 或 `跨域专题`),在 [`00-index.md`](00-index.md) 导航表登记一行;
  3. 不建空子分类目录:尚无成员的分支只写进领域 `README.md` 的待孵列表。

### 新增单卡的五步生长闭环

每新增或升级一张 ★★★ 单卡,按以下闭环落盘,缺一步不算完成:

1. **写卡**:frontmatter 齐全(`kind/domain/subcategory/repo/commit/evidence/status/asof`),先写 `WRITING.md` 前三节(问题/适用面/业务价值),再写标准八段。
2. **挂图与子分类**:更新所在子分类 `README.md` 成员表与领域 `plugin-map.svg`(链接与证据级星数必须与 frontmatter 一致)。
3. **刷单一数据源**:如该仓不在最新 `live-*.json`,先跑 `live_probe.py --asof YYYY-MM-DD`,再跑 `python3 _digested/ecosystem/view_data.py` 更新 `_data/{cards.json,summary.json,health.md}`。
4. **沉淀干货到 `04-leverage.md`**:如果这张卡产出了值得复用的架构模式或真实翻车反模式,在 [`_view/04-leverage.md`](_view/04-leverage.md) 增补一行(带「做法 + 代价/失效边界 + 卡片出处」);如果是纯重复形态则不强塞。
5. **跑门禁**:`node _digested/verify.mjs` 与 `python3 -m unittest discover -s _digested/ecosystem -p 'test_*.py'` 全绿,且 `health.md` 无新增 `no-live-repo`。

---

## 三、裁量空间与卡片契约

上游在变、生态在长,下面这些**每轮都可以由判断调整**:

| 事项 | 说明 |
|------|------|
| 子分类怎么划 | 从头部条目的自述与源码里归纳真实分型;分型变了就重划,别守着旧目录。 |
| 立册/立卡时机 | 参考默认门槛(领域 ≥400 条且本期新增 ≥100、有 ≥100★ 或源码锚、owners ≥300 且单件 <95%;单卡 ≥500★ 或 ≥5 条第三方点名),但**跨域新范式或高借鉴价值机制可破例先立**。 |
| 每轮补几个锚 | 建议 1–5 个,删掉、重写、补证据、回填旧卡都算数;没有值得补的就不补。 |
| 每张卡的篇幅 | 八段是**骨架不是配额**,机制复杂的写长,纯配置包的写短;装不下时升级为 `NN-<slug>/` 子目录。 |

### 单卡标准结构(唯一模板,子目录不再重复)

新卡与升级卡按 [`_view/WRITING.md`](_view/WRITING.md) 顺序写 11 节(前 3 节给评估者,4–7 节给实现者,8–11 节给复核者):

- 前三节:`## 它替谁解决什么问题` → `## 适用面:谁该用、谁别用` → `## 业务价值`(能算清 / 只是预期两档分开)
- 核心八段:`1. 一屏事实` → `2. 它到底是什么` → `3. 怎么接进 DSH` → `4. 关键实现` → `5. 为什么它突出`(只用自身证据) → `6. 代价与边界` → `7. 可信度与复现` → `8. 待验证`

### 卡片 frontmatter(单一源)

```yaml
---
kind: card              # card | reference(reference 是没读源码的参考基线)
domain: ui
subcategory: enhance-shell
repo: omdsh-dev/DSH-better-sidebar
commit: 2811573c9c0bad51d77db6c3c94d78f5aed8d38a
evidence: 3             # 1/2/3;3 必须有 commit
status: active          # active | watch | stale | deprecated | frozen | archived
asof: 2026-11-27        # 本卡结构事实的截止日
---
```

- `kind: reference` 不要求八段,但必须写清“未读源码”和参考 commit;领域册不得把它算进“全部 ★★★”。
- `status` 是可复核状态词:`active`(近 90 天有 push 且无已知宿主断裂)/ `watch`(钉旧 peer 或需改造)/ `stale`(停更 >90 天)/ `deprecated`(被宿主内置取代)/ `frozen`(不可安装)/ `archived`(仓库归档)。
- `verify.mjs` 自动校验:frontmatter 必填字段、`★★★` commit、`kind: card` 八段、`asof >= 2026-11-25` 前三节顺序、`_data/cards.json` 与 `summary.json` 同步、自动发现的 `view_*` 闭环(四块板 + `README`/`AGENTS`/`plugin-map.svg` + 入口登记 + SVG 证据级与链接 + “全部 ★★★”声明)。

---

## 四、供应链与每轮同步(七步)

```text
upstream main (awesome-dsh-plugin/awesome-dsh-plugin)
  │ ① fetch → ② merge
  ▼
data/plugins/*.yml  ├─ ③ census.py ──────────────────────► ecosystem/(全量档案)
                    ├─ ④ delta.py <old> <new> ───────────► _view/01~03(覆盖式重建)
                    └─ ⑤ live_probe.py + radar_probe.py ─► _snapshots/ + _data/health.md
                                                               │
                                                               ▼
                           view_<领域>/README.md → <子分类>/README.md → NN-<slug>.md
                                                               │ (沉淀可抄机制/反模式)
                                                               ▼
                                                   _view/04-leverage.md ←── _leverage/(四册)
```

每轮上游同步七步:

1. **探规模**:`git rev-list --count`、`git diff --stat`;先看 `scripts/`、`.github/`、`package.json` 有无 diff。
2. **合入**:https 通道 + `-c http.lowSpeedLimit=1000 -c http.lowSpeedTime=60` fetch,`git merge --no-ff`;研究目录若被上游触及,先从合并前分支恢复。
3. **核分母**:跑 `census.py`,核对总数与 `ls data/plugins/*.yml | wc -l` 一致且 0 解析失败。
4. **写当期记录**:`_change_log/NNNN-<from>-to-<to>.md`,七个专题各一行判定(需复核 / 已核验 / 无对应 diff)+ 理由;有真实 diff 的逐行读 diff 并改写对应 `mechanics/` 档案与 `mechanics/00-map.md`。
5. **刷三层实时雷达**:
   - `python3 _digested/ecosystem/live_probe.py --asof YYYY-MM-DD`(全部已立卡 + 存量锚)
   - `python3 _digested/ecosystem/radar_probe.py --delta <old> <new> --asof YYYY-MM-DD`(本期新增仓 GraphQL 星标 + 过线补 npm;每 2–3 轮可另跑一次 `--full`)
   - `python3 _digested/ecosystem/view_data.py`(重建 `_data/cards.json` / `summary.json` / `health.md`)
6. **更新视图与状态**:`_view/01~03` 覆盖式整页重写;`_view/04-leverage.md` 按新机制增量更新;领域册快照与 `_coverage/00-index.md`、`00-index.md`、`_faq_on_digested/` 时效提示同步更新;单卡不无故重写,除非目标插件有新提交或扩散数变化。
7. **全套验证**:跑下方第六节全部命令并确认零报错,当期记录末尾回写「复核日期 + 短 hash」。

---

## 五、视图规则

1. **视图零原创**:`_view/01~04` 与领域册 README 的结构数字必须来自 `census.py`/`delta.py`,实时值来自 `_snapshots/`(标日期与覆盖率),机制与干货结论必须指向 `view_*` 源码级单卡、`_leverage/` 或 `mechanics/`;而 `view_*` 下的 ★★★ 源码卡本身就是第一手证据源。
2. **动静分离**:`01-emerging`、`02-heat-map`、`03-anchors` 每轮覆盖式重写(历史归 `_change_log/` 与 `ecosystem/`);`04-leverage.md` 为长期累积的干货与反模式索引,增量演进、不随每轮清空重写。
3. **候选 ≠ 采纳**:扩散先看 `delta.py` ③b 候选分层(锚自身 / 同名 / 描述),再由卡内逐条判定;不得把候选数写成“接入数”。
4. **分册规则不重复通则**:每个 `view_<领域>/AGENTS.md` 只写本册特有判断线索;通用底线与生长闭环只在本文件维护。

---

## 六、完成判据(缺一不可)

```sh
python3 _digested/ecosystem/census.py                                  # 分母与工作区一致、0 解析失败
python3 _digested/ecosystem/view_data.py                               # _data 与 frontmatter 及最新快照同步
python3 -m unittest discover -s _digested/ecosystem -p 'test_*.py'     # 全部研究工具单测通过
node _digested/verify.mjs                                              # _digested + _faq_on_digested 全部通过
node _leverage/verify.mjs                                              # _leverage 全部通过
```

- 四块板每页顶部一屏能回答该板问题 + 数据截止日与口径;
- `_data/health.md` 无未说明的 `no-live-repo`;
- 同步轮次在 `_change_log` 当期记录末尾回写复核日期与短 hash。

数字引用前必读 [`_method/00-index.md`](_method/00-index.md) 与 [`_method/02-anchor-metrics.md`](_method/02-anchor-metrics.md)。
