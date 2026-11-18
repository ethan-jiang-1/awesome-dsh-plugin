# host-backed — 外部记忆系统适配

> 记忆存在外部系统里,插件只做 DSH 侧的接入层:召回、注入、工具。

## 定义

后台是一个独立项目或服务(OpenViking、hindsight、flowix、misakanet.org),插件负责把它接进 DSH 的会话与工具面。判定标准:去掉外部项目,插件本身不能独立工作。**"默认安装是否需要外部端点"是这条判据的关键**——本地回退只改变安装形态,不改变默认依赖。(`mnemon` 是 local-store 分支插件的可选存储引擎,不归这里。)

## 成员(人工确认)

| 条目 | 星标 ⚠ | 说明 | 衍生 | 单卡 |
|------|--------|------|------|------|
| volcengine/OpenViking#examples/dsh-memory-plugin | 29567(宿主背书) | 预注入 + 会话捕获 + `viking://` 防护 | 3 | [02-openviking](02-openviking.md) ★★ |
| vectorize-io/hindsight#coding-agents | 20218(宿主背书) | 长期项目记忆,自动 recall/retain | 9 | [01-hindsight](01-hindsight.md) ★★★ |
| Ikalus1988/MisakaNet | 407 | 失败恢复知识库;默认一行 MCP 指向 misakanet.org,clone 才可本地 stdio | 0 | [03-misakanet](03-misakanet.md) ★★★ |
| text2future/flowix#dsh-flowix-memory | 320 | 注册 flowix-cli MCP server | — | — |
| tinqiao-oss/engramory#plugin | 160 | markdown 落盘的长期记忆 | — | — |

## 立卡条件

≥3 个第三方衍生,或被 ≥5 个条目点名。

> 本轮破例:MisakaNet 的第三方衍生为 0,按"声量 + 形态独特性"立卡;它的 407 ⚠ 星(实时读数更高)属于跨 13 宿主的主项目,不算这层适配的扩散。门槛未变。

## 生长

**宿主背书是本分支的核心陷阱**:星标属于主项目。判断"是否被用"只能靠衍生数、下载量、衍生实现的活跃度。hindsight 已形成标准的形态(9 个第三方衍生,7 个同名),OpenViking 还在对接基线阶段(3 个)。

**读源代码后修正的判据**(见 [01-hindsight](01-hindsight.md)):hindsight 的收敛**不在插件接口层,而在服务端/配置层**——固定 `~/.hindsight/coding-agent.json` 与固定 bank 命名。9 个衍生里只有 4 个真实现记忆工具,3 个只做控制台/本地生命周期,靠"读同一个库"成立。**"同名衍生数"是弱证据,"共用同一份配置/存储"才是强证据**。

**第三种形态:整条产品托管**(见 [03-misakanet](03-misakanet.md))。MisakaNet 把语料(1 057 篇 lesson)与检索(托管 Worker)都放在外部,DSH 侧真正自研的只有 3 005 行网页半身 + 一行 MCP 行;默认 npm 安装不包含本地 Python 服务。它的零扩散与"可抄的只有一行指向同一端点的配置"一致,不能读成"没人用"——npm 侧有可观的月下载量(卡内 2026-11-18 实测)。

⚠ **隐私**:hindsight 默认后端是 Cloud(`config.ts`),装完即上传;只有 daemon 模式才本地。MisakaNet 默认也会把查询前 80 字符写入托管端的 `search_signals`。写卡与推荐时必须说明这一点。

## 横向对照(成员之间)

| | OpenViking | hindsight | MisakaNet |
|---|---|---|---|
| 星标 ⚠ | 29567(宿主背书) | 20218(宿主背书) | 407(主项目背书) |
| 第三方衍生 | 3 | 9 | 0 |
| DSH 侧自研规模 | 重新实现/管理工具/UI 增强 | 服务端客户端 + 事件绑定 | 一行 MCP 行 + 3 005 行面板 |
| 数据默认在哪 | `viking://` 服务端 | Cloud 或 self-hosted/daemon | misakanet.org 托管端点 |
| 结论 | 有对接基线,未成标准 | 已成事实标准 | 明星,非锚 |

**判据**:能被别人对着抄的**接口**才算标准;只能被对着抄 UI 的,只是参照物。
