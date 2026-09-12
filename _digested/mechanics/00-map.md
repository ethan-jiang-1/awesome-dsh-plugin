# mechanics · 注册表机制(评估者速览)

> **默认读到本文为止。** 下面六个子目录是机制档案(投稿者/维护者视角的逐行笔记,共 ~770 行),对"理解这个项目有什么用"贡献很小。评估所需的全部数字与解读在 [`ecosystem/`](../ecosystem/00-map.md)。
> 结论基线:`main@38976afd`,2026-09-12(0001 已复核;本页与各专题 map 同步更新)。

## 评估这个项目,机制层面只需要知道三件事

**1. 名单数据从哪来,能不能信?**
唯一人工编辑的东西是 `data/plugins/*.yml` 一个插件一个小文件(3552 个;0001 起**投稿只带这一个文件**,README 由 main 合并后自动重生成);README 和整站(约 7160 页)都是它生成的派生物。收录前有 CI 门禁挡格式垃圾与内容越界(0001:提交数门槛已删、新增路径守卫),收录后探针每夜刷新 stars/downloads/截图等外部事实(采集失败只标 incomplete 不会毁掉旧数据,"unknown ≠ dead")。→ **含义**:收进来的项目存在性、活跃度、安装通道是真的;但描述文案本身没有事实核查,当作图书馆卡片而不是书评来用。

**2. 名单会不会烂?**
每周一个 decay 扫描给条目打 flag(消失/归档/休眠),不确定率超过 5% 就熔断不判死,且只开 issue 提醒人、从不自动删除。→ **含义**:衰老有监控、有人工兜底,不是挂了没人管的目录。

**3. 它是个什么量级的工程?**
约 4600 行 scripts + 8 条 workflow(约 1470 行),基础设施仍是纯 GitHub-Native(GitHub Actions + Pages + npm OIDC)。→ **含义**:这是 awesome-list 的工业化形态——一个人靠纯 GitHub-Native 工具就能维持的注册表;架构极保守,没有值得借鉴的黑科技。~~没有隐藏的商业逻辑~~——**此结论 0001 已推翻**:站点接入 AdSense(变量门控,ads.txt 落库)与 Giscus 评论,变现动作首次落地(详见 [site-surface](site-surface/00-map.md) 与 [ecosystem/04](../ecosystem/04-value-trend.md))。

## 六个档案各是什么(按需再翻)

| 档案 | 记了什么 | 什么场景才有必要读 |
|------|----------|--------------------|
| [`system/`](system/00-map.md) | 全局运转图:一条 PR 从提交到上站的生命线 | 想完整追一遍流程时从这进 |
| [`registry-data/`](registry-data/00-map.md) | YAML schema、边车 JSON 拓扑 | ecosystem 里某个统计口径存疑,回查字段定义 |
| [`submission-gates/`](submission-gates/00-map.md) | 门禁逐行精读(0001 后为 3 道准入门 + 2 条保鲜线 + 1 条监督线) | **投稿者**想知道自己的 PR 为什么被拒 |
| [`readme-pipeline/`](readme-pipeline/00-map.md) · [`site-surface/`](site-surface/00-map.md) | README 与站点如何生成 | 要复现构建或研究双语一致性 |
| [`probes-and-decay/`](probes-and-decay/00-map.md) | 探针家族 + 腐烂扫描 | 追问"stars 数字怎么来的""上游合并后哪些边车会变" |

> 数字类细节的重跑入口:ecosystem 用 [`census.py`](../ecosystem/census.py) 与 [`fresh_probe.py`](../ecosystem/fresh_probe.py);机制行为的复核流程见 [`_change_log/`](../_change_log/00-index.md)。
