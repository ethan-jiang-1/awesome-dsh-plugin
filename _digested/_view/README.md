# `_view` — 生态动向呈现层(可再生视图)

> **这是什么**:对外的生态动向与干货入口。回答外部读者的四个问题——①什么冒出来了、②哪里热闹、③热闹领域里谁说了算、④**有哪些干货可直接借鉴**。结构数字由 `census.py`/`delta.py` 复现,卡片级与新苗子实时指标由 `_snapshots/` 归档,每轮 upstream 同步后覆盖式重建前三块板,`04-leverage.md` 按新机制增量更新。

**数据截止**:`main@8f1a1800e`(2026-11-25);本期区间 `29b3ed46e` → `8f1a1800e`(2026-11-17 → 11-25,8 天)。实时指标快照见 [`_data/health.md`](../_data/health.md)。
**写作规范**:卡片与领域册的读者顺序、适用面/价值要求、反模式与存量回填策略见 [`WRITING.md`](WRITING.md)。
**复现**:`python3 _digested/ecosystem/census.py`(全量)+ `python3 _digested/ecosystem/delta.py 29b3ed46e 8f1a1800e`(本期 diff)+ `python3 _digested/ecosystem/radar_probe.py --delta 29b3ed46e 8f1a1800e`(新增雷达)+ `python3 _digested/ecosystem/view_data.py`(卡片/健康表)。
**⚠ 数据边界**:仓库自带星标/下载边车冻结在 2026-08-19,趋势与新苗子统一以 `_snapshots/` 带日期实时采样为准;各页顶部均标明采样日期与覆盖率。

## 四块板

| 板 | 回答 | 文件 |
|----|------|------|
| ① 冒出来的 | 新 owner 群体、实时高星新苗子、标签增长 | [01-emerging.md](01-emerging.md) |
| ② 哪里热闹 | 23 类热度排名、真/假热闹判别 | [02-heat-map.md](02-heat-map.md) |
| ③ 锚 | 热闹领域的有影响力之物(扩散 × 声量) | [03-anchors.md](03-anchors.md) |
| ④ 干货借鉴 | 不用回原 repo 翻:可抄走的架构模式、反模式与 `_leverage/` 四册总路由 | [04-leverage.md](04-leverage.md) |

## 领域专册(`_digested/view_<领域>/`)

对**已经稳定且有突出条目**的领域单独立册,每个领域是 `_digested/` 下一级子目录、入口 `README.md`,其下再分子分类与单卡。**立册门槛是默认值,不是硬规定**:数值见 [`../AGENTS.md`](../AGENTS.md) §二,生态涨了可以抬,某个领域突然热了可以破例先立。

| 专册 | 类型 | 领域 | 状态 |
|------|------|------|------|
| [view_ui](../view_ui/README.md) | 类目大册 | 界面与交互 | 已立 |
| [view_tools](../view_tools/README.md) | 类目大册 | 工具箱 | 已立 |
| [view_session](../view_session/README.md) | 类目大册 | 会话管理 | 已立 |
| [view_workflow](../view_workflow/README.md) | 类目大册 | 工作流 | 已立 |
| [view_memory](../view_memory/README.md) | 类目大册 | 记忆与知识库 | 已立 |
| [view_proactive_agent](../view_proactive_agent/README.md) | 跨域专题 | 主动式 agent | **已立·前沿专题**(0007 首立,6 卡) |
| [view_personal_agent](../view_personal_agent/README.md) | 跨域专题 | 个人 Agent(Muse/Dots/Grok Bot) | **已立·前沿专题**(2026-11-27 首立,9 张 DSH ★★★ + 3 张外部 ★★ 参考卡) |
| — | 候补 | dev/usage/model/docs/vision… | 候补:dev/usage/model 已过体量门槛,但按“头部沉淀 + 读者问题”判断暂不立册(dev 的 3520 星 mirage 是宿主项目;usage 的 416 星锚 dsh-context 尚未做源码级卡;model 头部仅 62 星);docs/vision 头部锚已在 03 板。下次复核。 |

### 候补专题(未立册)

不是领域册,只是"可能长成专题"的观察项;每轮同步后重估,达标才立。

| 候选 | 证据(0007 基线) | 判断 |
|------|------------------|------|
| **dev / usage / model** | 见上一行体量判断 | 仍候补(原候选 `personal agent` 经突破注册表收录盲区、实查 GitHub DSH 原生高星仓与 `DS-Bot` 伴生契约环后已升级为 [view_personal_agent](../view_personal_agent/README.md)) |


**册内结构(三级)**:领域册 `README.md` 是入口(快照 + 子分类索引 + 稳定性判读)→ 子分类 `<子分类>/README.md`(定义 + 成员 + 立卡条件)→ 单卡 `<子分类>/NN-<slug>.md`(源码级八段)。子分类从头部条目的自述里归纳,分型会随生态重划;单卡编号在每个子分类内从 01 起。立册门槛是**默认值**,按 [`AGENTS.md`](../AGENTS.md) §二 可调。

每个领域册顶部另有一张 `plugin-map.svg`:按子分类排列单卡,卡上标注机制/价值、⚠ 边车星标、实时快照星标、下载与第三方提及,并用底部横条表示声量(log 尺度);点击卡片可打开对应 MD。图谱的证据级必须与卡片 frontmatter 一致(`verify.mjs` 会查)。

## 纪律

- **视图零原创**:`_view/` 汇总板与领域册 README 的结构数字必须可由 `census.py`/`delta.py` 复现,实时值必须能对到最新 `_snapshots/live-*.json` 或增量雷达快照,机制与借鉴结论必须指向 `view_*` 源码级单卡、`_leverage/` 或 `_digested/mechanics/`;而 `view_*` 下的 ★★★ 源码卡本身就是第一手源码证据源(锁 `repo@commit` 与文件行号)。
- **候选 ≠ 采纳**:扩散数先按 `delta.py` ③b 的同名/描述分层,再由卡片逐条判定;不得把候选数写成“接入数”,也不得把“零协议复用”写成“零提及”。
- **覆盖式重建**:每轮同步后本目录三块板(01/02/03)整页重写,不追加历史;历史在 `_change_log/` 与 ecosystem 档案里。
- **一屏契约**:读者只读各页顶部一屏,即可得到该板答案与数据新鲜度。
