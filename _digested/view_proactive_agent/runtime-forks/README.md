# runtime-forks — 整树分叉或 vendor 上游内核

> D1 层:把上游 `dsh-superagent` 的代码搬过来,改部署面;或把它的 `core/` 原样 vendor 进自己的仓。**本子分类 6 个成员,0 卡待立。**

## 定义

同时满足两条:

1. 仓库里有上游代码(整树 `src/` 同名文件,或 `core/` vendor 目录);
2. 复用上游的领域模型(Source/Policy/Ticket/Mandate/Assignment),不是另写一套。

按"改了多少"再分:

- **深分叉**:上游源文件基本都在、且多数有实质改动(HiSeax 92/92 全改;ctrl439 110 个 TS/TSX 里 58 个逐字节相同);
- **薄分叉**:只动部署面(desktop 只改 7 个 `src` 文件);
- **vendor**:只搬纯内核(open-a2a-net 的 `src/superagent/upstream/` 15 文件 / 2,088 行,逐字节相同)。

## 成员

| 条目 | 星标 | 形态 | 改了什么 | 页 |
|------|-----:|------|----------|----|
| HiSeax/dsh-windows-superagent | 138 | 深分叉 | Windows 路径/进程/服务 + 微信 iLink + 看板;92/92 文件改,+22 新文件 | [FAQ 深读](../../../_faq_on_digested/02_superagent-dependents/lines/01-windows-hiseax.md) |
| mengzhongjie/dsh-superagent-local | 11 | 深分叉 | 改成"本机工作区"版:workspace→主会话→工单→worker;同包名/id | [FAQ](../../../_faq_on_digested/02_superagent-dependents/lines/02-local-fork.md) |
| NelsonLongXiang/dsh-open-a2a-net | 10 | vendor | 只搬 `core/` 15 文件 + 2 个测试,逐字节相同;外层换 A2A | [FAQ](../../../_faq_on_digested/02_superagent-dependents/lines/06-vendored-engine-a2a.md) |
| jinghuaihuaxiang-star/dsh-superagent-desktop | 1 | 薄分叉 | 装进现有 profile、默认 `stateDir`、peer 放宽;npm 月下载 1,753 | [FAQ](../../../_faq_on_digested/02_superagent-dependents/lines/03-desktop-fork.md) |
| 439436269-ctrl/dsh-superagent | 0 | 深分叉 | 多仓 + IM 桥(钉钉/企微);GitHub 真 fork,npm 0.3.0 | [FAQ](../../../_faq_on_digested/02_superagent-dependents/lines/05-multi-repo-im-fork.md) |
| DASHAN-0079/dsh-superagent-adapt | 0 | 整树适配 | 上游源码改到 DSH 0.2.2-rc.3;1213 例等价性测试 | [FAQ](../../../_faq_on_digested/02_superagent-dependents/lines/04-adapt-fork.md) |

## 读法

- **先看上游文件命中率**:`diff -rq` 或 `cmp` 上游 `src/` 与目标仓;命中率越高,升级债越大。
- **再看宿主钉版**:peer 数量、是否精确钉 rc、是否必须独立 profile/junction;这决定"能不能装"。
- **最后看它补的面**:Windows、本机、桌面、版本适配、多仓、A2A——每家只补一个,没有一家全补。

## 立卡条件

默认 ≥500★ 或被 ≥5 个条目引用其协议;本层只有 HiSeax 过百星。按机制例外,下一轮优先 HiSeax(深分叉 + 唯一过百星);desktop 因"npm 月下载 1,753"可作分发样本候选,但只有 7 个文件改动,机制密度不足。
