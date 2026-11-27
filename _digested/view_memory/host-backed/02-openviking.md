---
kind: reference
domain: memory
subcategory: host-backed
repo: volcengine/OpenViking
commit: 2e643943d0abed02023defb9d3410a623272d292
evidence: 2
status: active
asof: 2026-11-27
---

# OpenViking — 宿主背书 + 轻衍生:对接基线,未成标准

> 证据等级:★★(注册表自述 + 衍生清点 + 生态观察);**未读源码**(参考卡,不要求八段)。参考坐标:`volcengine/OpenViking@2e643943d0abed02023defb9d3410a623272d292`(2026-11-18 `main` 头,仅记录未阅读)。
> 数据截止 `8f1a1800e`(2026-11-25)。⚠ 边车星标为 2026-08-19 历史采样;实时快照见 [`_data/health.md`](../../_data/health.md)。

## 它替谁解决什么问题

**已经在生产或测试环境里部署了火山引擎 OpenViking 记忆服务、想顺手把同一套知识库与用户画像接进 DSH 的团队。** 如果没有官方示例插件,团队得自己对着 `viking://` 协议手写 pre-step 召回、会话捕获和 URI 防护逻辑;这份 `examples/dsh-memory-plugin` 充当了官方提供的最小接线样板。

## 适用面:谁该用、谁别用

- **适合**:已选用 OpenViking 作为统一记忆/知识库后端的团队,以及想参考官方示例写增强面板或管理工具的插件作者。
- **不适合**:只需要轻量本地 SQLite/Markdown 记忆、不想额外维护 OpenViking 服务端的个人开发者;以及需要强源码审计后才能上线的团队(本卡目前仅 ★★ 未读源码,其 `viking://` 防护与隐私落点尚未逐行核验)。
- **前置条件**:必须部署或接入可用的 OpenViking 服务端;具体 DSH 版本兼容范围与运行期依赖待源码级复核。

## 业务价值

- **能算清的**:
  - **对接样板效应**:注册表内已衍生出 **3 个第三方条目**(重实现、管理工具与落到 `ui` 类的增强层 `A2chitect/dsh-openviking-enhance`),说明它已被社区当作 OpenViking 接线的默认参照系。
  - **明确扣掉星标水分**:⚠ 29,567★(2026-08-19)与实时快照高星均属 `volcengine/OpenViking` 主项目,不可算作 DSH 插件的采用量;实际下载与活跃度以 [`_data/health.md`](../../_data/health.md) 的实时快照为准。
- **只是预期(推断)**:复用官方示例可能省去初次对接 OpenViking 协议的摸索成本,但是否适合直接进生产需等源码级审计(升至 ★★★)后才能定论。

## 一屏事实

| 项 | 值 |
|----|-----|
| 官方条目 | `volcengine/OpenViking#examples/dsh-memory-plugin`([registry](../../../data/plugins/volcengine__OpenViking--examples-dsh-memory-plugin.yml)) |
| 类目 | memory |
| 自述 | pre-step 自动召回与画像注入、会话捕获、`viking://` URI 防护、recall/write 工具,依赖 OpenViking 服务端 |
| 星标 ⚠ | 29567(**宿主项目背书**) |
| 第三方衍生 | 3 条 |

## 为什么它是参考基线

**机构级宿主项目的示例插件**——星标属于 OpenViking 主仓,不代表插件本身被用。但它在名单里产生了 3 个第三方条目,说明"官方示例"确实被当成对接基线。**它不是锚**:声量归主项目,扩散只有 3,且没有形成可复用的协议面;按 `_view/03` 的口径,它是"对接基线,未成标准"。

| 衍生条目 | 类目 | 方向 |
|----------|------|------|
| A2chitect/dsh-openviking-enhance | ui | 增强层(带独立 tarball 发布) |
| Rxiain/dsh-openviking | memory | 重新实现 |
| xbzbing/dsh-openviking-manager | memory | 管理工具 |

注意 `A2chitect` 的衍生条目落在 **ui** 而不是 memory——衍生方向开始偏离原类目,是"适配层变产品"的信号。


## 看点 / 待验证

- 汇总回归:`grep -ril openviking data/plugins/ | wc -l` → 4(含锚自身)。
- 待验证:三个衍生是否都必须连 OpenViking 服务端(若是,则整个家族受同一后端可用性约束)。

## 相关档案

- memory 类全貌:[../README.md](../README.md)
- 子分类成员与横向对照:[README.md](README.md)
