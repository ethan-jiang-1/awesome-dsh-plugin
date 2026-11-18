# DSH-better-sidebar — 平台级锚

> 证据等级:★★(注册表自述 + 边车读数 + 衍生条目清点);机制细节未读源码。
> 数据截止 `29b3ed46e`(2026-11-17)。⚠ 星标/下载为 2026-08-19 历史采样。

## 一屏事实

| 项 | 值 |
|----|-----|
| 条目 | `omdsh-dev/DSH-better-sidebar`([registry](../../data/plugins/omdsh-dev__DSH-better-sidebar.yml)) |
| 类目 | ui(全表最大类,2351 条) |
| 自述 | 侧边栏完整工作台:文件渲染编辑、终端、Git、子代理;三方插件可注册新 Tab |
| 星标 ⚠ | 2216(2026-08-19) |
| npm 月下载 ⚠ | 39717(2026-08-19) |
| **第三方提及** | **63 条** |

## 为什么它是锚

星标只排 ui 第二,但**模仿信号全表第一**:63 个条目在自己的名字或描述里点名它(可复现:`delta.py` ③b)。这些不是"致敬",是**接入**——git 图谱侧栏、用量回放、MD 批注器、隐身阅读器等都往它的 Tab 注册。

这改变了它的性质判定:**它不是"一个好用的侧栏插件",而是这批插件的事实平台**。平台的换代成本远高于插件——看它的动向,等于看 ui 领域 63 个衍生条目的共同契约。

## 可复现数字

```sh
python3 _digested/ecosystem/delta.py efe602e7b 29b3ed46e   # ③b 节:better-sidebar 第三方提及 63
grep -il "better-sidebar" data/plugins/*.yml | wc -l      # 65(含锚自身 2)
ls data/plugins/omdsh-dev__*.yml | wc -l                  # 44:同作者跨类系列产能
```

## 看点 / 待验证

- 作者 `omdsh-dev` 在名单里有 **44 条**条目,覆盖 ui/notify/browser/tools/security——是"系列化生产者"还是"平台+配套"的组合,需读源码确认。
- 待验证(升 ★★→★★★):注册机制是否公开稳定(三方插件注册 Tab 的 API 是否版本化)、63 个提及者里有多少真依赖它的 API、多少只是并列安装。

## 相关档案

- 类目结构与头部断层:[ecosystem/01-scenario-taxonomy](../ecosystem/01-scenario-taxonomy.md)
- ui 类全貌:[../README.md](README.md)
