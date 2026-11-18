# ③ anchors — 热闹领域的锚

> **本期区间**:同 [01](01-emerging.md)。⚠ 星标为 2026-08-19 前后的**历史采样**,不反映当前;锚的机制结论链接档案层。
> **复现**:`delta.py` ③ 节。证据等级:★=README 级 · ★★=源码级 · ★★★=实测(逐卡标注,本轮多数仍为 ★)。

## 锚的两轴:声量 × 扩散

星标是**声量**(且边车过期),第三方提及/衍生是**扩散**(每期名单现算,不过期)。两轴都高才是真锚;只有声量高的是"明星"。证据等级:★ 注册表自述 · ★★ 读过源码/文档 · ★★★ 实测。

| 锚 | 声量 ⚠ | 扩散 | 类型 | 单卡 |
|----|--------|------|------|------|
| DSH-better-sidebar | 2216 | **63** | **平台型**:被接入(Tab 注册) | [view_ui/01](../view_ui/01-better-sidebar.md) ★★ |
| hindsight | 20218(宿主背书) | **9** | **标准型**:被仿制(8 个 `dsh-hindsight-*`) | [view_memory/01](../view_memory/01-hindsight.md) ★★ |
| modlens | 3152 | 4 | vision 的参考实现 | — ★ |
| OpenViking | 29567(宿主背书) | 3 | 对接基线,未成标准 | [view_memory/02](../view_memory/02-openviking.md) ★★ |
| ouroboros | 5565 | **0** | **明星,非锚**:高星零衍生 | [view_workflow/01](../view_workflow/01-ouroboros.md) ★★ |

**可复现**:`python3 _digested/ecosystem/delta.py <old> <new>` 的 ③b 节。

## 一屏答案

热闹领域的锚按扩散轴重排后<b>并不等于星标榜</b>:真正的平台是 DSH-better-sidebar(63 个第三方插件接入),真正的标准是 hindsight(9 个衍生),而 workflow 星标第一的 ouroboros 零衍生。原星标视图见下(**memory 的 OpenViking/hindsight 2.9 万/2 万星实为宿主项目背书**)。本期新增条目无一进入任何类目的锚位——不是没有好苗子,是采样没跟上,列为缺口。

| 类目 | 存量锚(星标 ⚠) | 备注 |
|------|----------------|------|
| memory | volcengine/OpenViking 29567 · vectorize-io/hindsight 20218 · Ikalus1988/MisakaNet 407 | 头部是官方/机构仓库的示例插件;社区侧 MisakaNet 为纯社区最高 |
| workflow | Q00/ouroboros 5565 · tong-io/tongflow 860 · NanmiCoder/dsh-agent-teams 573 | ouroboros 是 workflow 类唯一的千星级社区项目 |
| ui | omdsh-dev/DSH-better-sidebar 2216 · ccch1mneyyy/dsh-TUI 2009 · FSMargoo/dsh-at-file 394 | omdsh-dev 跨 ui/notify/browser/tools 多类目锚位(系列化生产者) |
| dev | strukto-ai/mirage 3520 · hust-open-atom-club/oh-dsh 252 | mirage 为 dev 类唯一千星 |
| vision | liustack/modlens 3152 · ysr666/dsh-vision-router 775 · Anionex/dsh-vision-toolkit 714 | 头部集中度最高的小类之一 |
| docs | tt-a1i/archify 14283 | 同为宿主背书型(archify 主项目) |
| skill | GanyuanRan/Aegis 1062 · superdesigndev/superdesign-skill 432 | skill 类唯一千星 |
| theme | Small-tailqwq/dsh-deep-whale#maid-atelier 1400 | theme 类唯一千星 |
| notify | OpenPetsHQ/openpets 1081 · shaobeichen/dsh-pocket 179 | |
| remote | liguobao/ds-harness-remote 1197 | remote 类唯一千星 |
| security | toby-bridges/api-relay-audit 791 | security 类头部 |
| tools | superdesigndev/treg 477 · zhaoolee/notes#dsh-plugin 147 | tools 虽是第二大类,千星锚缺位 |
| session | Anionex/dsh-turn-rewind 83 | session 类 914 条,头部仅 83 星——**供给最大、沉淀最弱的类** |
| usage | bowenliang123/dsh-context 416 · zh667/TokenLedger 103 | |
| browser | omdsh-dev/dsh-browser 302 · liustack/modsearch 153 | |
| fun | Nagi-ovo/dsh-ads 501 · vlln/whale-girl 241 | |
| model | Mars-Sea/dsh-commandcode-provider 62 | model 类 593 条,头部仅 62 星——与 session 同病 |

## 本期缺口(下轮优先)

- **新增锚位全部空缺**:18 天 3899 条新增无一条有星标读数。下一轮若重采星标边车(`fresh_probe.py`),优先扫本期新增 ≥100 条类目的前 50 条,把 ③ 表的"新增头部"填上。
- **锚证据等级**:上表全部 ★(边车读数),无一链接到源码级结论。按 AGENTS.md 预算,下轮从 memory/workflow/ui 各取 1 个锚升 ★★。
