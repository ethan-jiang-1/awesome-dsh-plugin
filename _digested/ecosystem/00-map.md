# ecosystem · 插件生态全景

> 状态:**首版完成**(数据层已核验,解读为初稿)。数据快照:`main@5e7dc7eb`,2026-08-27;由 [`census.py`](census.py) 从 `data/plugins/*.yml` 现算,可随 upstream 同步重跑。

## 这个生态是什么

DSH = **DeepSeek Harness**(`deepseek-ai/deepseek-harness`,见根 README.md:7-9):DeepSeek 官方开源的 agent harness,"一切皆插件"——模型、工具、沙箱、会话存储、UI、连 agent loop 本身都是插件位。本仓库是它的社区插件目录(awesome list),收录以 `dsh plugin add` 安装、带 `dsh.bundle` 清单的插件。

所以读这 2286 个条目的正确姿势不是"看一个 awesome 列表",而是看**一个开源 agent 框架的第三方生态在两周内长成了什么形状**:谁在做壳、谁在补短板、谁在接进来。

## 头条事实(2026-08-27 实测)

| 事实 | 数字 |
|------|------|
| 生态年龄 | **14 天**(2026-08-13 init,8-16 起 bulk 收录 963 条 = 42%,此后日均 ~81 条新入) |
| 条目 / 作者 | 2286 条,1522 个独立 owner,**78% 作者只有一件作品** |
| 官方分类 | 22 类;ui 一类独占 15.7%,头部五类(ui/tools/dev/session/workflow)占近半 |
| 成熟度 | stars 中位数 **2**,75% 的条目 ≤5 星;≥100 星仅 49 条 |
| 头部来源 | 星标 Top3 全是**外部成熟大项目主动接入**(字节 volcengine/OpenViking 29567★、hindsight 20218★、archify 14283★),原生头部只在 ui/vision 层 |
| 语言/命名 | 99% 中文描述齐备;85% 仓库名以 `dsh` 开头 |

## 两套坐标系

官方 22 类是**收录容器**(注册表自己的货架);要回答"这生态在做什么",需要第二套维度:

1. **按场景分** → [01-scenario-taxonomy.md](01-scenario-taxonomy.md):官方 22 类逐类透视 + 重聚成十个场景带("给聊天窗做壳" vs "给 agent 做增强"两大阵营)。
2. **按技术分** → [02-tech-landscape.md](02-tech-landscape.md):34 个技术特征标签(en+zh 描述正则打标),模型阵营格局、多模态外挂模式、成本监控品类。
3. **演化与成熟度** → [03-growth-maturity.md](03-growth-maturity.md):land-grab→稳态的节奏、作者结构(单件作者 vs 系列工作室)、星标/下载金字塔与"外部项目接入"现象。

## 方法与精度声明

- 统计脚本 [`census.py`](census.py) 仅用标准库:手写容错 YAML 子集解析 + 单趟 `git log --diff-filter=A` 取首录日期。重跑方式:`python3 _digested/ecosystem/census.py`。
- 技术标签是描述文本的正则判定,**有已知精度边界**(详见 02 文末的方法注记:如「本地推理」曾因匹配『离线』虚高到 44,剔除后实为 10;「图像生成」曾误配任意含『图』文本 361 条,收紧后 32)。引用具体标签数字时以最新一次 census 输出为准。
- 58 个条目无法定位首录日期(早期批量导入先于 added-dates 基线),时间统计基于其余 2228 条。
- 解读性结论(场景带划分、"两大阵营")是我的归纳,不是注册表的官方口径;反例可直接报数复核。

## 待回答的问题

- [ ] omdsh-dev(37 条,dsh-tool-* 全家桶)、damonkoy/dsh-web-ui(monorepo 拆 12 子包)这类工作室型作者的第二件样本抽读
- [ ] 头部 ≥100 星 49 条中,原生插件 vs 外部接入的完整名单(现在只确认了 Top3 是外部)
- [ ] npm 下载(624 条覆盖)与星标的分歧名单:高下载低星的"沉默用户型"插件
