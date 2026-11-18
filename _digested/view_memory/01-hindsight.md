# hindsight — 标准级锚

> 证据等级:★★(注册表自述 + 衍生条目清点);未读源码。
> 数据截止 `29b3ed46e`。⚠ 星标为 2026-08-19 历史采样。

## 一屏事实

| 项 | 值 |
|----|-----|
| 官方条目 | `vectorize-io/hindsight#coding-agents`([registry](../../data/plugins/vectorize-io__hindsight--hindsight-integrations-coding-agents.yml)) |
| 类目 | memory(504 条) |
| 星标 ⚠ | 20218(**宿主项目背书**,非插件热度) |
| 第三方衍生 | **9 条**(全表第二) |

## 为什么它是锚

扣除宿主背书后,它的星标不能说明插件被用,但**衍生实现数量能**:名单里有 9 个第三方条目围绕它做本地化、控制台、GUI 与优化,其中 8 个直接以 `dsh-hindsight-*` 命名。

**这是 memory 领域事实标准的形态**:一个上游实现 + 一圈下游适配。与 session 领域(914 条、头部仅 83 星、零衍生)对照,记忆的收敛已经发生,会话的还没有。

## 衍生清单(可复现)

```sh
grep -il hindsight data/plugins/*.yml | wc -l   # 10(含锚自身)
```

| 衍生条目 | 类目 | 方向 |
|----------|------|------|
| Apauto-to-all/dsh-hindsight-control-plane | memory | 控制台 |
| dyrcjqlgcj/dsh-hindsight-local | memory | 本地化 |
| Hua1Q1nG/dsh-hindsight-local-optimize | memory | 本地优化 |
| jackyytche/dsh-hindsight-memory | memory | 记忆接入 |
| KouzakiUmi/dsh-hindsight-gui | memory | GUI |
| meisijiya/dsh-hindsight-memory | memory | 记忆接入(第二实现) |
| snakejohn/dsh-hindsight-local | memory | 本地化(第二实现) |
| SMPcosy/dsh-memnexus | memory | 描述中提及 |
| soberkeen/dsh-vault | tools | 描述中提及 |

## 看点 / 待验证

- 同一方向出现两份 `local`、两份 `memory` —— 是分叉竞争还是各自对接不同后端?需读三份 src。
- 待验证:官方包与本仓插件的关系(是官方集成还是社区包装),决定"标准"的归属。

## 相关档案

- memory 类全貌:[../README.md](README.md)
- 宿主背书型读数的口径:[../../_method/00-index.md](../_method/00-index.md)
