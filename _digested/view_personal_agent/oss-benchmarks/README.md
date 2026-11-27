# oss-benchmarks — 外部开源复现标杆(非 DSH 本体,★★ 参考基线)

> 本子分类收纳 **3 个尚未以原生插件进入 DSH、但在 GitHub 影响面巨大且最能代表 Meta Muse / OpenAI Dots / xAI Grok Bot 开源前沿的独立项目**,全部为 `kind: reference`(★★ 文档与配置核验,未逐行读源码)。收录目的只有两个:**直接抄走 DSH 生态目前最缺的安全/隔离/交互机制**,以及**跟踪谁最先通过 ACP / AG-UI / MCP 与 DSH 汇合**。

## 定义

同时满足三条:

1. 非 DeepSeek Harness 原生实现(独立全栈产品或自研宿主);
2. 在 GitHub 上明确复现 Grok Bot / OpenAI Dots / Meta Muse 范式且星标过千、2026-11 持续活跃;
3. 要么具备**零代码挂载 DSH 的标准协议缝**(ACP / AG-UI / MCP),要么在 **Sentinel / 盲填 Vault / 沙箱隔离 / 费用防线**上明显领先现有 DSH 插件、值得直接借鉴。

## 成员

| 条目 | 实时星标(11-27) | 协议 | 一句话 | 卡 |
|------|----------------:|------|--------|----|
| `milind-soni/OpenMausBot` | **28,403★** | Apache-2.0(+专有 `enterprise/`) | GitHub 最高星 Grok Bot/Muse/Dots 复现;原生 `customAcp` 可零代码挂 DSH | [01-openmausbot](01-openmausbot.md) |
| `CopilotKit/OpenBot` | **13,733★** | MIT 模板(+专有后端镜像) | 正式合并 `OpenDots`+`openfuse` 为多皮肤;fail-closed CEL 网关 + 人机接管 | [02-openbot](02-openbot.md) |
| `n8n-io/nod` | **4,158★** | **纯 Apache-2.0** | 自带电脑的个人 Agent;上下文隔离 Checker + 盲填 Vault + 三层预算闸门蓝本 | [03-n8n-nod](03-n8n-nod.md) |

> 其余高星外部底座(如 `openclaw/openclaw` 395k★、`NousResearch/hermes-agent` 266k★、`HKUDS/nanobot` 50k★、`agentscope-ai/QwenPaw` 38k★、`nearai/ironclaw` 12.7k★、`elie222/rakazo` 10k★、`simplexai-labs/linger` 5k★、`najmuzzaman-mohammad/gawkbot` 1.6k★)在领域总入口 [../README.md](../README.md) 的生态对照表追踪,不在此重复立卡。

## 读法

- **想把 DSH 直接塞进现成多 Bot 外壳**:先看 [01-openmausbot](01-openmausbot.md) 的 `customAcp` 路径与 [02-openbot](02-openbot.md) 的 AG-UI 接入边界;
- **想给 DSH 写个人级安全/盲填密码/防烧钱插件**:直接抄 [03-n8n-nod](03-n8n-nod.md) 的三容器零共享、上下文隔离 Checker 与六元组支付绑定。

## 立卡条件

非 DSH 原生仓一律从严:须 **≥4,000★**、近 30 天有真实迭代,且具备明确的 DSH 互操作协议或补齐 DSH 关键范式缺口的架构价值;统一以 `kind: reference`(★★)立卡,绝不混算进本册的 DSH ★★★ 源码卡数。
