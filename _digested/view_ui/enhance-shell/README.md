# enhance-shell — 增强现有壳

> 在 DSH 现有界面上加东西:侧栏、Tab、注记、导航条、状态标签。不替换宿主界面。

## 定义

插件挂进已有 UI 的扩展点(slot / Tab 注册 / 装饰),用户的界面骨架不变。判定标准:卸载后原界面仍可用,只是少了一块。

## 成员(人工确认的头部例子,非全量归类)

| 条目 | 星标 ⚠ | 说明 |
|------|--------|------|
| omdsh-dev/DSH-better-sidebar | 2216 | 侧栏工作台,63 个第三方插件往它的 Tab 注册(平台级;[01-better-sidebar](01-better-sidebar.md) ★★★) |
| FSMargoo/dsh-at-file | 394 | 输入框 `@` 引用;只传路径不读内容。官方 0.2.1 已内置 `@file`,本插件自认 best-effort,且在 0.2.1-rc.5 上 Host 半疑似加载失败([02-at-file](02-at-file.md) ★★★) |
| ZSeven-W/dsh-openpencil | 119 | 设计预览/编辑;插件零渲染代码,强绑外部 Rust OpenPencil + 原生二进制;读路径不查 sandbox([03-openpencil](03-openpencil.md) ★★★) |
| omdsh-dev/dsh-annotation | 76 | 选区批注;批注=纯文本提示词,气泡里"看不见"是发完从 DOM 剪掉,零结构化字段([04-dsh-annotation](04-dsh-annotation.md) ★★★) |
| HsiangNianian/dsh-auto-continue | 26 | 重启/失败自动续跑 + 宿主侧单引擎;9 类收尾判据、9 道闸门、冷读预算;0 扩散但同名 5 家([05-auto-continue](05-auto-continue.md) ★★★) |
| Laplace-bit/dsh-smooth-stream | 33 | 流式字符揭示 + 合成层跟随弹簧;运行时改 slot component 接管,0 扩散但近义 4 家([06-smooth-stream](06-smooth-stream.md) ★★★) |
| whiteguo233/dsh-openbiliclaw | 45 | 右侧抽屉面板 |
| vlln/dsh-navbar | 41 | 会话节点导航条 |
| alingalingling/ui-status-label | 38 | 状态标签自定义 |

## 立卡条件

≥500 星,或被 ≥5 个第三方条目点名(扩散信号)。

> 本轮破例:at-file 394 星/3 家扩散、openpencil 119 星/0 扩散、annotation 76 星/7 个同名实现、auto-continue 26 星/3 804 下载、smooth-stream 33 星/937 下载,均未达门槛;按"类内第三 + 扩展点样本"、"形态独特(设计工具适配)"、"交互样本"、"高下载状态机"与"流式体验样本"立卡。门槛未变。

## 生长

这是 ui 里**最容易长出平台**的分支(better-sidebar 已证明):插件越多地往同一扩展点注册,那个扩展点就越接近标准。新卡优先看"被多少人接入",不是星标。

**但"被接入"有两种结局**。at-file 的 3 家扩散里只有 1 家(`dsh-at-any`)硬分叉它的 `inputTriggers` 源;另外 2 家分别转向官方 `ctx.fileReferences` 与工具注册——生态收敛到的是**宿主的**引用接口,不是这个插件的 `atFile` 端点。它自己的 README 也已承认被官方 `@file` 取代,2026-09-01 之后 2.5 个月无提交,Host 半依赖的 `ctx.settings.register` 在 0.2.1-rc.5 已不存在。**这是本册第一个"被宿主内置能力取代"的样本**。

openpencil 走的是另一条路:插件不含渲染代码,预览靠外部二进制、编辑靠 loopback daemon 的 iframe,自己只留能力令牌与草稿事务。**形态独特不等于可复制**——零第三方提及,私有 `.op` 格式与 20 875 行适配层把后来者挡在门外。

annotation 是**接入点稳定、编码各异**的样本:DSH 三层都没有原语(消息级装饰无槽、草稿无"引文块"、回复无字段可挂),所以 7 家同名实现各写一套格式;它们互不引用,0 代码扩散。它的批注不是结构化字段,而是 Enter 时拼进草稿的纯文本块,发完再从用户气泡 DOM 剪掉——**消息正文/会话日志里其实永久留着批注块**。

auto-continue 则是**高下载、零扩散**的样本:引擎在 host 进程单实例,9 类 `turn/end` 收尾分实时/扫描两路判定,`aborted{user|parent|hook}` 与 `blocked` 永不续跑;重复防护五层(回显 id 消费、单飞定时器、inbox 提优先级、扫描台账、交接 5min)。3 804 是 2026-08-19 边车的 npm `last-month` 值,而包首版在 2026-08-14 才发布——所以它是"首 5 天的月窗口",不是三个月累积。它没有授权层的 `/api/auto-continue-action` 是这层要盯的安全边界。

smooth-stream 是**手感型**样本:两个独立时钟——字符揭示(压力曲线 + 600cps 上限 + 收尾斜坡)与跟随弹簧(半隐式弹簧 + 合成层 transform 表达滞后);接管靠运行时改 `conversation.chat.node` 的 `entry.component`,不打宿主源码补丁。扩散 0,但同名 1 家、近义 4 家、反向需求 1 家(专门关平滑滚动),说明"需求被独立复现,实现不被引用"。

⚠ **权限边界(读源码后确认)**:

- better-sidebar 的 `path-security.ts` / `fs-operations.ts` 头注明写 **workspace 包含检查已被移除**,路由可达宿主用户可达的任何路径;`src/` 内无 sandbox 策略链引用,唯一准入是连接层的 `requestRejection`。
- at-file 的 Host 半直接 `node:fs` 遍历/`stat`,**不走 DSH 的 sandbox/policy 链**;符号链接 `realpath` 后会被跟随,词法包含检查会把 `@ext/passwd` 判成"工作区内"。
- openpencil 的读路径同样用裸 `node:fs`、不查 `sandboxPolicy`;编辑器保存绕过 DSH fs 抽象,只有两个写工具强制 sandbox 模式。

选这类"增强壳"时,面板/索引能力往往等于宿主机同权限——**扩展点是公开的,不代表权限边界是插件自己守的**。
