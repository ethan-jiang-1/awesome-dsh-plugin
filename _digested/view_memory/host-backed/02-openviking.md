# OpenViking — 宿主背书 + 轻衍生锚

> 证据等级:★★(注册表自述 + 衍生清点 + 生态观察);未读源码。参考坐标:`volcengine/OpenViking@2e643943d0abed02023defb9d3410a623272d292`(2026-11-18 `main` 头,仅记录未阅读)。
> 数据截止 `29b3ed46e`。⚠ 星标为 2026-08-19 历史采样。

## 一屏事实

| 项 | 值 |
|----|-----|
| 官方条目 | `volcengine/OpenViking#examples/dsh-memory-plugin`([registry](../../../data/plugins/volcengine__OpenViking--examples-dsh-memory-plugin.yml)) |
| 类目 | memory |
| 自述 | pre-step 自动召回与画像注入、会话捕获、`viking://` URI 防护、recall/write 工具,依赖 OpenViking 服务端 |
| 星标 ⚠ | 29567(**宿主项目背书**) |
| 第三方衍生 | 3 条 |

## 为什么它是锚

**机构级宿主项目的示例插件**——星标属于 OpenViking 主仓,不代表插件本身被用。但它在名单里产生了 3 个第三方条目,说明"官方示例"确实被当成对接基线:

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
