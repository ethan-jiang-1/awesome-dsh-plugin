# single-purpose — 单点工具

> 解决一个问题:转换、检索、计算、对接单一服务。

## 定义

一个插件完成一件明确的事:转换、检索、计算、对接单一服务。判定标准:去掉它就少一种能力,而不是少一个工作方式。

## 成员(人工确认)

| 条目 | 星标 ⚠ | 说明 |
|------|--------|------|
| superdesigndev/treg | 477 | 类内 ⚠ 最高;星标属主项目,DSH 面只有 150 行(一行 MCP + 一页 skill;[01](01-treg.md) ★★★) |
| zhaoolee/notes#dsh-plugin | 147(仓库级) | 对话→便签双通道;插件 808 行 HTTP 客户端,PNG 由服务端 headless Chromium 渲染,默认出网([03](03-notes.md) ★★★) |
| taxueseek/argo#dsh-plugin | 101 | 统一搜索 + 证据核验;主项目约 20 万行 Python,插件 6,561 行;默认只露 2 个原生工具([02](02-argo.md) ★★★) |
| Anionex/dsh-computer-use | 22 | macOS Accessibility 快照 + `stateHash` 重校验;182 个测试;⚠下载 360,实时月下载 6,570([04](04-dsh-computer-use.md) ★★★) |
| xiehuan123/dsh-deepread | 20 | 五种精读模式共用「分段提炼 → 合并」流水线;预算 preflight + 后台 jobs;下载 1,974([05](05-dsh-deepread.md) ★★★) |

## 立卡条件

≥800 星(工具类头部门槛高于其他类)。

> 本轮破例:treg 477 / notes 147 / argo 101 / computer-use 22 / deepread 20 均未达 800;按"类内头部 + 五种接入形态(托管 MCP / 自研客户端 / HTTP 客户端 / 桌面控制参考实现 / 精读工作流)"立卡。门槛未变。

## 生长

**"单点工具"有五种完全不同的实现代价**:

- **treg** 是 150 行 vendor 适配层——一行远程 MCP + 一页生成的 SKILL.md,4,197 个 endpoint、凭据注入、计费全在托管服务后面。它可抄,但抄了只得到"指向同一服务的配置"。
- **argo** 是 4 千行自研 DSH 客户端——17 个文件、6,561 行(其中 718 行原生工具由 Python 生成),底下是 198,081 行 Python 的搜索基础设施;默认只暴露 2 个原生工具,其余按需。它不可抄,因为能力在主项目。
- **notes** 是 808 行 HTTP 客户端——两条能力共用一个工具的一次 if/else:不配置 baseUrl 就默认 POST 作者的演示服务器,由服务端 Playwright+Chromium 截本应用前端出 PNG;配置了 baseUrl 才走自建服务整工作区读改写。渲染、分页、图片落盘都不在插件里。
- **computer-use** 是**机制密度型参考实现**——macOS Accessibility 快照 + `stateHash` 动作前重校验 + scoped permissions + 182 个测试;⚠ 星标只有 22,但 2026-11-18 的 npm 月下载已到 6,570。它卖的不是"接一个服务",是"怎么安全地驱动桌面"。
- **deepread** 是**工作流型单点工具**——五种模式其实是同一条 `splitChunks(6000 字/20 段) → 逐段 JSON 提炼 → 合并` 的参数化;外面套预算 preflight(零模型调用)、URL 缓存与官方 `jobs`(可取消、无恢复)。1,974 下载对 20 星,≈99:1;它卖的是"把精读做成流程",不是"一次摘要"。

五者的星标大多属主项目、第三方提及都为零。**读 tools 的头部不能按星标读**:⚠ 477 的 treg 在 DSH 侧只有 150 行,⚠ 101 的 argo 有 6,561 行,⚠ 147 的 notes 只有 808 行且默认出网,⚠ 22 的 computer-use 有 182 个测试与实时月下载 6,570,⚠ 20 的 deepread 有 1,974 下载。
