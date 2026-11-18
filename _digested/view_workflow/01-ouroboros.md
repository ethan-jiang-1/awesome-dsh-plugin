# ouroboros — 高星但零衍生的反例锚

> 证据等级:★★(注册表自述 + 衍生清点);未读源码。
> 数据截止 `29b3ed46e`。⚠ 星标为 2026-08-19 历史采样。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `Q00/ouroboros#integrations/dsh-plugin`([registry](../../data/plugins/Q00__ouroboros--integrations-dsh-plugin.yml)) |
| 类目 | workflow(703 条) |
| 自述 | 纯配置包,经 DSH MCP 客户端挂载 Ouroboros,提供 36 个访谈/Seed/执行/评估/演化流程工具 |
| 星标 ⚠ | **5565**(workflow 类第一,全表社区第三) |
| 第三方衍生 | **0** |
| 同类第二名 | tong-io/tongflow 860(差 6.5 倍) |

## 为什么值得单独立卡

它是**"高星 ≠ 被模仿"的干净反例**,正好用来校准锚的判据。

- 星标断层第一(5565 vs 第二 860);
- 但全表没有任何第三方条目提及它(`delta.py` ③b:合计 1 = 锚自身);
- 自述形态是"纯配置包",挂载外部 Ouroboros 引擎——**影响力可能在 Ouroboros 主项目,而不在 DSH 适配层**。

与 better-sidebar(63 次提及)、hindsight(9 个衍生)对照,可以看出三类完全不同的"有影响力":**平台型**(被接入)、**标准型**(被仿制)、**自带流量型**(被知道但不被复刻)。

## 对锚判据的贡献

本卡立了一个规则:**锚的"影响力"至少要拆成两轴**——声量(星标/下载)与扩散(第三方提及/衍生)。两轴都高才是真锚;只有声量高的是"明星",不是"锚"。

## 可复现

```sh
python3 _digested/ecosystem/delta.py efe602e7b 29b3ed46e   # ③b:ouroboros 合计 1(零衍生)
grep -il ouroboros data/plugins/*.yml | wc -l              # 1
```

## 看点 / 待验证

- 若 Ouroboros 主项目本身在涨(需实时星标,边车已过期),那"零衍生"就不等于"没影响",只是影响发生在 DSH 之外。
- 待验证:36 个工具的实际调用量与配置复杂度——纯配置包的门槛低,理论上更易模仿,零衍生反而更值得解释。

## 相关档案

- workflow 类全貌:[../README.md](README.md)
- 锚两轴口径:[../_view/03-anchors.md](../_view/03-anchors.md)
