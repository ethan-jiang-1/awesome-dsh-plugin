# view_memory — 记忆与知识库

> 已立册(504 条 / 新增 164 / owners 470、单件 94%)。⚠ 星标为历史采样。数据截止 `29b3ed46e`。

## 快照

中盘类目,本期占比 −0.0pp 匀速;owners 470、单件 94%,多样性尚可。

## 锚(存量头部,⚠ 星标历史采样)

| 条目 | 星标 | 说明 |
|------|------|------|
| volcengine/OpenViking#examples/dsh-memory-plugin | 29567 | ⚠ 宿主背书型:星标属于 OpenViking 主项目,非插件热度([02](host-backed/02-openviking.md) ★★) |
| vectorize-io/hindsight#coding-agents | 20218 | 同上,hindsight 主仓背书([01](host-backed/01-hindsight.md) ★★★) |
| Ikalus1988/MisakaNet | 407 | **主项目背书型**:跨 13 宿主失败知识库,DSH 是第 12 个;不是"纯社区最高"([03](host-backed/03-misakanet.md) ★★★) |
| text2future/flowix#dsh-flowix-memory | 320 | monorepo 子包 |
| tinqiao-oss/engramory#plugin | 160 | |

## 子分类(册内目录)

| 子分类 | 定义 | 成员数(已确认) |
|--------|------|----------------|
| [host-backed](host-backed/README.md) | 外部记忆系统适配(宿主背书陷阱) | 5 例,9 个第三方衍生(7 同名) |
| [local-store](local-store/README.md) | 本地存储与检索(SQLite/markdown) | 4 例 |
| [context-shaping](context-shaping/README.md) | 上下文整形与蒸馏 | 3 例 |

单卡落在子分类目录内:`<子分类>/NN-<slug>.md`;本册已有 5 张单卡(host-backed 3、local-store 2),全部 ★★★。

## ⚠ 隐私提示

本领域三个头部(hindsight、OpenViking、MisakaNet)都依赖**外部服务**。hindsight 默认后端为 Cloud,装完即上传会话内容;OpenViking 需 `viking://` 服务端;MisakaNet 默认 MCP 行指向 `misakanet.org`,并把查询前 80 字符写入托管端的 `search_signals`。引用"记忆能力"时,先确认数据存哪——这是选择记忆插件比选工具更要紧的一条。

## 稳定性判读

memory 的头部被三个机构级宿主项目占据,读数时要**把"宿主项目火"与"插件被用"分开**(数字口径见 [`_method/00-index.md`](../_method/00-index.md))。源码级卡片修正了一条旧判断:**MisakaNet 不是"纯社区侧最高"**——它的 407 ⚠ 星(实时读数更高)属于一个支持 13 个宿主的失败知识库,DSH 适配层只有一行 MCP 行 + 3005 行面板,扩散为 0。

扣除三个宿主背书型后,社区侧的真实头部是 `dsh-mnemon`(109 ⚠,实时读数显著更高;同一仓库、无宿主稀释)与 `dsh-memento`(58 ⚠,同样高于边车值);前者有硬衍生,后者有可分发协议套件但第三方采纳为 0。**社区侧记忆方案同样未收敛**,与 session 类似但供给量小一半。RAG/知识库标签本期 +308(见 [01-emerging](../_view/01-emerging.md)),供给端在加速,锚位竞争未定。
