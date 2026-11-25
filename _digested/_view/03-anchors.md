# ③ anchors — 锚候选与明星

> **本期区间**:`29b3ed46e`(2026-11-17,11744 条)→ `8f1a1800e`(2026-11-25,13136 条)。⚠ 星标为 2026-08-19 前后的**历史采样**,不反映当前;锚的机制结论链接档案层。
> **复现**:扩散 = 卡内 `grep -ril` + 逐条判定;`delta.py 29b3ed46e 8f1a1800e` ③b 只输出**候选分层**(同名/描述),不把候选数直接当采纳数。方法见 [`_method/02`](../_method/02-anchor-metrics.md)。证据等级定义见 [`../AGENTS.md`](../AGENTS.md) §一 底线 3。

## 两轴:声量 × 扩散(锚候选 / 明星)

星标是**声量**(且边车过期),第三方提及/衍生是**扩散**(每期名单现算,不过期)。两轴都高才是真锚;只有声量高的是"明星"。

| 对象 | 声量 ⚠ | 扩散(候选 → 卡内采纳) | 判定 | 单卡 |
|----|--------|------|------|------|
| DSH-better-sidebar | 2216 | 66 候选(1 同名 fork + 65 描述)→ 卡内采纳 **64**(1 fork + 63 描述) | **平台候选**:有 Tab 注册服务;抽样 3 个中仅 1 个硬依赖 | [enhance-shell/01](../view_ui/enhance-shell/01-better-sidebar.md) ★★★ |
| hindsight | 20218(宿主背书) | 10 候选(7 同名 + 3 描述)→ 卡内判定 **4 个**真实现记忆工具 | **标准候选** | [host-backed/01](../view_memory/host-backed/01-hindsight.md) ★★★ |
| modlens | 3152 | 4 候选(描述) | vision 的参考实现,未逐条判定 | — ★ |
| OpenViking | 29567(宿主背书) | 4 候选(3 同名 + 1 描述) | 对接基线,未成标准 | [host-backed/02](../view_memory/host-backed/02-openviking.md) ★★ |
| ouroboros | 5565 | **0** | **明星,非锚**:高星零衍生 | [external-engine/01](../view_workflow/external-engine/01-ouroboros.md) ★★★ |

**可复现**:`delta.py` ③b 给出候选分层;采纳数必须回到卡内逐条判定。本期 better-sidebar 与 hindsight 各多出 2 / 1 条描述候选,**尚未逐条判定**,采纳数暂按卡内现值。

## 一屏答案

热闹领域的锚按扩散轴重排后**并不等于星标榜**:**平台候选**是 DSH-better-sidebar(66 个候选,卡内采纳 64:1 个同名 fork + 63 个描述提及;抽样 3 个中仅 1 个硬依赖),**标准候选**是 hindsight(10 个候选,卡内判定 4 个真实现记忆工具),而 workflow 星标第一的 ouroboros 零衍生。本期新增的约 1400 条**无法判断**是否进入锚位——不是没有好苗子,是星标采样连续五轮没跟上(边车冻结在 2026-08-19),列为缺口。

| 类目 | 存量锚(星标 ⚠) | 备注 |
|------|----------------|------|
| memory | volcengine/OpenViking 29567 · vectorize-io/hindsight 20218 · Ikalus1988/MisakaNet 407 | 头部是官方/机构仓库的示例插件;MisakaNet 407 星属跨 13 宿主的主项目,DSH 适配层扩散 0;社区侧真实头部见 [view_memory](../view_memory/README.md)(mnemon 6 条描述候选、engramory 1 条同名候选) |
| workflow | Q00/ouroboros 5565 · tong-io/tongflow 860 · NanmiCoder/dsh-agent-teams 573 | ouroboros 是 workflow 类唯一的千星级社区项目,但零衍生 |
| ui | omdsh-dev/DSH-better-sidebar 2216 · ccch1mneyyy/dsh-TUI 2009 · FSMargoo/dsh-at-file 394 | omdsh-dev 跨 ui/notify/browser/tools 多类目锚位(系列化生产者) |
| dev | strukto-ai/mirage 3520 · hust-open-atom-club/oh-dsh 252 | mirage 为 dev 类唯一千星 |
| vision | liustack/modlens 3152 · ysr666/dsh-vision-router 775 · Anionex/dsh-vision-toolkit 714 | 头部集中度最高的小类之一 |
| docs | tt-a1i/archify 14283 | 同为宿主背书型(archify 主项目) |
| skill | GanyuanRan/Aegis 1062 · superdesigndev/superdesign-skill 432 | skill 类唯一千星 |
| theme | Small-tailqwq/dsh-deep-whale#maid-atelier 1400 | theme 类唯一千星 |
| notify | OpenPetsHQ/openpets 1081 · shaobeichen/dsh-pocket 179 | |
| remote | liguobao/ds-harness-remote 1197 | remote 类唯一千星 |
| security | toby-bridges/api-relay-audit 791 | security 类头部 |
| tools | superdesigndev/treg 477 · zhaoolee/notes#dsh-plugin 147 | tools 已是第二大类(1918 条),千星锚仍缺位 |
| session | Anionex/dsh-turn-rewind 83 | session 类 1024 条,头部仅 83 星——**供给第二大、沉淀最弱** |
| usage | bowenliang123/dsh-context 416 · zh667/TokenLedger 103 | |
| browser | omdsh-dev/dsh-browser 302 · liustack/modsearch 153 | 标签增速第一,但锚位仍是旧面孔 |
| fun | Nagi-ovo/dsh-ads 501 · vlln/whale-girl 241 | |
| model | Mars-Sea/dsh-commandcode-provider 62 | model 类 665 条,头部仅 62 星——与 session 同病 |

## 本期缺口(下轮优先)

- **新增锚位全部空缺**:8 天 1440 条新增无一条有星标读数。下一轮若重采星标边车(`fresh_probe.py`),优先扫本期新增 ≥100 条类目(tools/ui/session/workflow)的前 50 条,把 ③ 表的"新增头部"填上。
- **两条候选待判**:better-sidebar +2 描述候选、hindsight +1 描述候选;不重判就不改采纳数。方法仍是回卡内 `grep -ril` + 逐条看安装/依赖证据。
- **单卡覆盖**:本表不逐张列卡;新卡分布在各领域册的子分类目录,扩散口径以卡内 `grep -ril` 命令为准。OpenViking 仍是 ★★(未读源码),下一轮可升到 ★★★。
