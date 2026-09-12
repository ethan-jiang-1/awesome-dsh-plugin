# ecosystem · 插件生态全景

> 状态:**0001 复核完成**(数据层已按 `main@38976afd` 重算;头条事实与分类表已更新到新基线,解读为 2026-09-12 修订版)。数据快照:`main@38976afd`,2026-09-12;由 [`census.py`](census.py) 从 `data/plugins/*.yml` 现算 + [`_method/01-fresh-probe`](../_method/01-fresh-probe.md) 自采管线补充新鲜信号,可随 upstream 同步重跑。

## 这个生态是什么

DSH = **DeepSeek Harness**(`deepseek-ai/deepseek-harness`,见根 README.md:7-9):DeepSeek 官方开源的 agent harness,"一切皆插件"——模型、工具、沙箱、会话存储、UI、连 agent loop 本身都是插件位。本仓库是它的社区插件目录(awesome list),收录以 `dsh plugin add` 安装、带 `dsh.bundle` 清单的插件。

所以读这 3552 个条目的正确姿势不是"看一个 awesome 列表",而是看**一个开源 agent 框架的第三方生态在一个月内长成了什么形状**:谁在做壳、谁在补短板、谁在接进来。

## 头条事实(2026-09-12 实测,census + fresh_probe)

| 事实 | 数字 |
|------|------|
| 生态年龄 | **30 天**(2026-08-13 init;8-16 的 963 条中 837 是旧 README→yml 迁移,见 [03 §1](03-growth-maturity.md);**近 7 天日均新增已降到 39**,洪流持续退潮) |
| 条目 / 作者 | 3552 条,2291 个独立 owner,**76.5% 作者只有一件作品** |
| 官方分类 | 23 类(新增 wsl);ui 592 独占 16.7%,头部五类(ui/tools/dev/session/workflow)占 46% |
| 成熟度 | stars 中位数 **2**,75% 的条目 ≤5 星,≥100 星 47 条(星标边车冻结,头部以 fresh_probe 自采数为准) |
| **变现信号** | **站点已接 AdSense**(ads.txt 落库、build 变量门控)+ Giscus 评论——"无变现"结论作废,见 [04 §2](04-value-trend.md) |
| 信号覆盖(fresh_probe 自采) | stars 3540/3552(99.6%);npm 可归因 2558(72%),**22% 条目未发布到 npm**;有下载 50%,双无仅 10% |
| 头部来源 | 星标 Top3 仍是外部巨头(archify 53656★、OpenViking 35988★、hindsight 23210★),**新增腾讯 WeKnora(21766★)**;单一最大事件是 **dsh-web monorepo(7422★,五日 +11.6 万下载)**,见 [04](04-value-trend.md) |
| 语言/命名 | 99% 中文描述齐备;85% 仓库名以 `dsh` 开头 |

## 一套官方货架 + 三个自定义视角

官方 22 类是**收录容器**(注册表自己的货架);要回答"这生态在做什么",得换成自己的视角。注意:视角一套、轴有三条,**其中只有前两条是"分类维度",第三条(演化)是时间轴**:

1. **按场景分** → [01-scenario-taxonomy.md](01-scenario-taxonomy.md):官方 22 类逐类透视 + 重聚成十个场景带("给聊天窗做壳" vs "给 agent 做增强"两大阵营)。
2. **按技术分** → [02-tech-landscape.md](02-tech-landscape.md):34 个技术特征标签(en+zh 描述正则打标),模型阵营格局、多模态外挂模式、成本监控品类。
3. **演化与成熟度** → [03-growth-maturity.md](03-growth-maturity.md):README→yml 一次性迁移后转入增量稳态、作者结构(单件作者 vs 系列工作室)、星标/下载金字塔与"外部项目接入"现象。

## 方法与精度声明

- 统计脚本 [`census.py`](census.py) 仅用标准库:手写容错 YAML 子集解析 + 单趟 `git log --diff-filter=A` 取首录日期。重跑方式:`python3 _digested/ecosystem/census.py`。
- **新鲜下载/星标不走仓库边车**(边车冻结,见 [`_method/00-index`](../_method/00-index.md)):趋势数字来自自采管线 [`fresh_probe.py`](fresh_probe.py),方法与六坑见 [`_method/01-fresh-probe`](../_method/01-fresh-probe.md)。
- 技术标签是描述文本的正则判定,**有已知精度边界**(详见 02 文末的方法注记:如「本地推理」曾因匹配『离线』虚高到 44,剔除后实为 10;「图像生成」曾因『绘图/画图/海报』等泛匹配报 361,收紧后 32)。引用具体标签数字时以最新一次 census 输出为准。
- 97 个条目无法定位首录日期(早期批量导入先于 added-dates 基线),时间统计基于其余 3552-97 条。
- 解读性结论(场景带划分、"两大阵营")是我的归纳,不是注册表的官方口径;反例可直接报数复核。

## 待回答的问题

- [x] ~~头部 ≥100 星 48 条中,原生插件 vs 外部接入的完整名单~~ → 0001 已确认 Top 全榜外部 giants 接入持续(archify/OpenViking/hindsight/WeKnora),原生头部集中在 ui/vision(见 04 §2)
- [x] ~~npm 下载与星标的分歧名单~~ → fresh_probe 双信号交叉已可常规产出(04 §7)
- [ ] **许可协议/商用审计** → 0001 出现实质进展:站点接 AdSense(ads.txt 公开 pub-id)+ Giscus;注册表自身开始变现,插件作者的 license 审计仍未做
- [ ] **作者社区画像**:perrylink(37)、173787247(31,WSL 全家桶)、988hj7tczd-oss(27,LSP packs)等头部工作室仍未抽样定性
- [ ] wsl 类 30 条新条目 0% 下载转化:是"环境错配"还是"需求未起"(04 §8)
