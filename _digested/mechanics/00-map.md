# mechanics · 注册表机制(评估者速览)

> **默认读到本文为止。** 下面六个子目录是机制档案(投稿者/维护者视角的逐行笔记,共 ~900 行),对"理解这个项目有什么用"贡献很小。评估所需的全部数字与解读在 [`ecosystem/`](../ecosystem/00-map.md)。
> 结论基线:`main@4693e5a83`,2026-10-11(0003 已同步;site-surface/registry-data/system 已复核,其他专题源码无 diff)。

## 评估这个项目,机制层面只需要知道三件事

**1. 名单数据从哪来,能不能信?**
唯一人工编辑的东西是 `data/plugins/*.yml` 一个插件一个小文件(4489 个;投稿只带这一个文件,README 由 main 合并后自动重生成);README 和整站(约 9000 个详情 HTML + 首页/分类 HTML/catalog JSON)都是它生成的派生物。收录前有 CI 门禁挡格式垃圾与内容越界(0001 删了提交数门槛;0002 又加三条:只改 README 行不算投稿、条目文件必须能被 YAML 解析、`name` 写成 owner/repo 就必须与 url 一致),收录后探针每夜刷新 stars/downloads/截图/**能力披露**等外部事实(采集失败只标 incomplete 不会毁掉旧数据,"unknown ≠ dead")。→ **含义**:收进来的项目存在性、活跃度、安装通道是真的;描述文案本身没有事实核查,当作图书馆卡片而不是书评来用。**0002 新收获**:每个插件的"碰了什么"(十种能力 + redLines)第一次有了全生态口径,但它同样只是**披露**,不等于审计。
**2. 名单会不会烂?**
每周一个 decay 扫描给条目打 flag(消失/归档/休眠/装不上,0002 拆出"子路径目录搬走了"这一类),不确定率超过 5% 就熔断不判死,且只开 issue 提醒人、从不自动删除。**0002 新增一条同类防线**:每日拉一次**线上站点**数页面,落后 catalog 超过 300 条即红——治的是"仓库里一切正常、网站静默冻结"(dshmarket.com 曾冻结 18 天)。→ **含义**:衰老有监控、有人工兜底,不是挂了没人管的目录。
**3. 它是个什么量级的工程?**
约 6266 行 scripts + **10 条 workflow**(含把评论线程补成 widget 可读形态的 adopt-discussions),基础设施仍是纯 GitHub-Native(GitHub Actions + Pages + npm OIDC);0002 起**首次有测试**(6 个 `*.test.mjs`,其中 3 个以"不联网、不要 token"的形式进了 pr-check)。→ **含义**:这是 awesome-list 的工业化形态——一个人靠纯 GitHub-Native 工具就能维持的注册表;架构极保守,没有值得借鉴的黑科技。**变现已在 0001 落地**(AdSense 变量门控 + Giscus 评论),0002 没有新商业动作。

## 六个档案各是什么(按需再翻)

| 档案 | 记了什么 | 什么场景才有必要读 |
|------|----------|--------------------|
| [`system/`](system/00-map.md) | 全局运转图:一条 PR 从提交到上站的生命线(0002 已并入八处机制变更) | 想完整追一遍流程时从这进 |
| [`registry-data/`](registry-data/00-map.md) | YAML schema、边车 JSON 拓扑(0002 起第五张提交边车 `capabilities.json`) | ecosystem 里某个统计口径存疑,回查字段定义 |
| [`submission-gates/`](submission-gates/00-map.md) | 门禁逐行精读(0002 后为 3 道准入门 + 2 条保鲜线 + 1 条监督线,规则与理由都在变) | **投稿者**想知道自己的 PR 为什么被拒 |
| [`readme-pipeline/`](readme-pipeline/00-map.md) · [`site-surface/`](site-surface/00-map.md) | README 与站点如何生成(0002:README 同步加了三轮重试;站点加了线上体检) | 要复现构建或研究双语一致性 |
| [`probes-and-decay/`](probes-and-decay/00-map.md) | 探针家族 + 腐烂扫描 + 能力披露 + 评论线程收编 | 追问"stars/下载/能力数字怎么来的""上游合并后哪些边车会变" |

> 数字类细节的重跑入口:ecosystem 用 [`census.py`](../ecosystem/census.py) 与 [`fresh_probe.py`](../ecosystem/fresh_probe.py);机制行为的复核流程见 [`_change_log/`](../_change_log/00-index.md);**研究工具自身在 0002 修了什么**见 [`_coverage/00-index.md`](../_coverage/00-index.md) 末节。
