# host-backed — 外部记忆系统适配

> 记忆存在外部系统里,插件只做 DSH 侧的接入层:召回、注入、工具。

## 定义

后台是一个独立项目或服务(OpenViking、hindsight、flowix、Mnemon),插件负责把它接进 DSH 的会话与工具面。判定标准:去掉外部项目,插件本身不能独立工作。

## 成员(人工确认)

| 条目 | 星标 ⚠ | 说明 | 衍生 |
|------|--------|------|------|
| volcengine/OpenViking#examples/dsh-memory-plugin | 29567(宿主背书) | 预注入 + 会话捕获 + `viking://` 防护 | 3 | [02-openviking](02-openviking.md) ★★ |
| vectorize-io/hindsight#coding-agents | 20218(宿主背书) | 长期项目记忆,自动 recall/retain | 9 | [01-hindsight](01-hindsight.md) ★★★ |
| text2future/flowix#dsh-flowix-memory | 320 | 注册 flowix-cli MCP server | — |
| tinqiao-oss/engramory#plugin | 160 | markdown 落盘的长期记忆 | — |
| omdsh-dev/dsh-mnemon | 109 | 本地优先的跨 agent 持久记忆 | — |

## 立卡条件

≥3 个第三方衍生,或被 ≥5 个条目点名。

## 生长

**宿主背书是本分支的核心陷阱**:星标属于主项目。判断"是否被用"只能靠衍生数、下载量、衍生实现的活跃度。hindsight 已形成标准的形态(9 个第三方衍生,7 个同名),OpenViking 还在对接基线阶段(3 个)。

**读源代码后修正的判据**(见 [01-hindsight](01-hindsight.md)):hindsight 的收敛**不在插件接口层,而在服务端/配置层**——固定 `~/.hindsight/coding-agent.json` 与固定 bank 命名。9 个衍生里只有 4 个真实现记忆工具,3 个只做控制台/本地生命周期,靠"读同一个库"成立。**"同名衍生数"是弱证据,"共用同一份配置/存储"才是强证据**。

⚠ **隐私**:hindsight 默认后端是 Cloud(`config.ts`),装完即上传;只有 daemon 模式才本地。写卡与推荐时必须说明这一点。

## 横向对照(成员之间)

| | OpenViking | hindsight |
|---|---|---|
| 星标 ⚠ | 29567(宿主背书) | 20218(宿主背书) |
| 第三方衍生 | 3 | 9 |
| 衍生命名 | `dsh-openviking-` | `dsh-hindsight-` 为主 |
| 衍生接手的层 | 重新实现 / 管理工具 / UI 增强,彼此不共享配置契约 | 共享一个服务端 + 一份约定俗成的配置(bank 名与配置路径就是接口) |
| 结论 | 有对接基线,未成标准 | 已成事实标准 |

**判据**:能被别人对着抄的**接口**才算标准;只能被对着抄 UI 的,只是参照物。
