# `view_memory/` 工作规则

memory 领域册。504 条、本期新增 164、owners 470(单件 94%)。上层纪律见 [`../AGENTS.md`](../AGENTS.md)。

## 册内结构(三级)

| 层 | 文件 | 作用 |
|----|------|------|
| 册 | `README.md` | 快照 + 子分类索引 + 稳定性判读 |
| 子分类 | `<子分类>/README.md` | 定义 + 已确认成员 + 立卡条件 |
| 单卡 | `<子分类>/NN-<slug>.md` | 源码级分析(八段模板,同 [`../view_ui/AGENTS.md`](../view_ui/AGENTS.md)) |

子分类:`host-backed`(外部系统适配)/ `local-store`(本地存储)/ `context-shaping`(上下文整形)。

## 本册特有注意

**宿主背书是这张册最重要的陷阱**:OpenViking 29567、hindsight 20218 的星标属于主项目,不代表插件本身被用。写卡与读数时必须把「宿主项目火」与「插件被用」分开,可用的替代证据是:

- 扩散数(`delta.py` ③b:第三方提及/衍生);
- npm 下载边车(仅少数条目有);
- 衍生实现的活跃度(需逐个看,不能只看条数)。

**这个领域已出现收敛信号**:hindsight 一圈 9 个第三方衍生(7 个以 `dsh-hindsight-*` 命名,2 个仅提及),而 session 类零衍生。记忆的标准形态正在形成,写卡时留意"谁是标准、谁是分叉"。

## 刷新

数字随 `census.py`/`delta.py`;衍生清单用 `grep -il hindsight data/plugins/*.yml` 复核。新卡优先看:扩散数上升者、从"适配"转"产品"的衍生(如 A2chitect 落在 ui 而非 memory)。
