# host-backed — 外部记忆系统适配

> 记忆存在外部系统里,插件只做 DSH 侧的接入层:召回、注入、工具。

## 定义

后台是一个独立项目或服务(OpenViking、hindsight、flowix、Mnemon),插件负责把它接进 DSH 的会话与工具面。判定标准:去掉外部项目,插件本身不能独立工作。

## 成员(人工确认)

| 条目 | 星标 ⚠ | 说明 | 衍生 |
|------|--------|------|------|
| volcengine/OpenViking#examples/dsh-memory-plugin | 29567(宿主背书) | 预注入 + 会话捕获 + `viking://` 防护 | 3 |
| vectorize-io/hindsight#coding-agents | 20218(宿主背书) | 长期项目记忆,自动 recall/retain | 9 |
| text2future/flowix#dsh-flowix-memory | 320 | 注册 flowix-cli MCP server | — |
| tinqiao-oss/engramory#plugin | 160 | markdown 落盘的长期记忆 | — |
| omdsh-dev/dsh-mnemon | 109 | 本地优先的跨 agent 持久记忆 | — |

## 立卡条件

≥3 个第三方衍生,或被 ≥5 个条目点名。

## 生长

**宿主背书是本分支的核心陷阱**:星标属于主项目。判断"是否被用"只能靠衍生数、下载量、衍生实现的活跃度。hindsight 已形成标准的形态(9 个衍生),OpenViking 还在对接基线阶段(3 个)。
