---
title: "分发与救生页 · dsh-market"
domain: reshape-product
kind: sample
positioning: "`dsh-market/dsh-market`：把发现与安装搬进产品，并给「起不来」留救生页。"
takeaway: "救生页活在插件栈外；界面只做一个决定；外部索引每次使用前再校验。"
read_when: "要做分发/市场/安装器；或要设计「装坏了怎么回」。"
status: observed
updated: 2026-10-31
---
# 分发与救生页 · dsh-market:分发本身就是一个产品

> **状态**:`observed` · **基线**:DSH `0.2.1-rc.3` · **读于**:2026-10-31
> **类**:`5` 分发 · **层**: 7 → 3 + 2 · **★ 9,902 / npm 813,066**（2026-10-31 实时；本线第 1）
> **一句话**:它不是"装插件的工具",而是一个**必须在宿主坏掉时还能工作的产品**——一半的机制量花在回滚、救生页和"说清楚为什么失败"上。
> **借鉴价值**:**① 全有或全无的宿主必须自带救生页,且救生页由宿主体外的 helper 在"用户已经在轮询的那个地址"上服务;② 界面只做一件事——勾选"下次启动启用哪些",写回宿主本来就认的那批配置行;③ 索引源每次使用前再校验一遍;④ 自动重启要知道自己**什么时候会把自己也杀掉**。**

> **样本档案**
> **repo**:[`dsh-market/dsh-market`](https://github.com/dsh-market/dsh-market) · **npm**:`dshmarket`(命令行装的名字);商店内显示 **Plugin Market** · **版本**:—
> **目录条目**:`data/plugins/dsh-market__dsh-market.yml`(`market`)
> **装法**:Desktop:`Settings → Plugins` 搜索安装;普通 web:`dsh plugin --profile web add dshmarket` 后重启
> **已在本地挖掘**:`_证据/02_首启与分发-原始挖掘.md` §二(8 小节,救生页/回滚/16 条降级)+ §四(上游契约速查)
> **再深挖去哪**:README 的环境变量 `DSHM_REGISTRY_URL` / `DSHM_GITHUB_PROXY`;issue #227(`allowRestart` 顶层被静默忽略)与 #139

---

## 0. 一页速览(想抄的人只看这 20 行)

| 问题 | 它的答案 | 支撑 |
|---|---|---|
| 它把开关写到哪 | **官方 patch 层**:`cordis.patch.yml` 里的 `- id: <行id>` + `disabled: true|false`;HMR 约 1s 重组合,**不用重启** | `[CAT]` README §Hot disable;`[DSH]` `dsh-app-boot/lib/index.js:61-109` |
| 为什么还要写 `dsh.profile.bundles` | 只禁用 patch 行**不够**——bundle 还在数组里就仍会被 resolve;要从数组摘掉才是真停用("disable-carrier") | `[DSH]` `dsh-app-boot/lib/index.js:1016-1024` |
| 救生页怎么活 | 由 **detached restart helper** 在**用户已经在轮询的那个地址**上服务;宿主死了它还在 | `[CAT]` README §Recovery |
| 救生页做什么 | 只做一件事:把 DSH 归咎的插件**标红且不勾选**,让用户选"下次启动启用哪些",写回同一批 patch 行 + bundles,然后**重试启动** | 同上 |
| 什么时候不给重启按钮 | **systemd 的服务主进程**(否则把 takeover 进程连同 cgroup 一起杀掉);判定要 **systemd 标记 AND 是该 unit 的主进程**(`INVOCATION_ID` 会被所有后代继承) | `[CAT]` README §Security |
| 怎么自证按钮被隐藏 | `GET /dsh-market/status` 返回 `"restart": false` | 同上 |
| 安装来源 | **只认精选 registry**,其他一律拒绝;安装端点**只接受同源 POST** | `[CAT]` README §Security |
| 索引源怎么校验 | **每次使用前**再判:可解析、http/https、**不许带凭据**、**不许带 fragment**、非规范形式直接报"用规范形式"、拒绝重复 | `[DSH]` `dsh-plugin-market/lib/types/index-url.js:8-27`、`lib/index.js:495-521` |
| 拉一份索引的上限 | 超时 **15000ms**、字节 **128 MiB**(边收边判)、缓存 TTL **600000ms**、`redirect: "error"`、同 URL 并发**共享一个 promise** | `[DSH]` `dsh-plugin-market/lib/index.js:364-367,533-551` |
| 索引格式 | `format` 必须为 **1**;违规抛 `MarketIndexError{path,reason}`,`path` 形如 `$.plugins[0].versions[1].version`;**版本数组按 SemVer 降序且不重复**;git `commit` 必须 **40 位小写 hex** | `[DSH]` `dsh-plugin-market-index/lib/index.js:8-22,226-318` |
| 目录拿不到 | **故意不做快照**:报真实原因 + 耗时 + Retry。理由原文:"对每天在长的目录,**过期答案不是降级答案,是错误答案**——今早发布的插件会被读成'不存在'" | `[CAT]` README §Degradation |
| 旧宿主 | **自我禁用**并在控制台说明,**不**渲染在不存在的原语上崩溃 | `[CAT]` README §兼容 |
| 忽略 ≠ 关闭 | 忽略只对**本次启动**有效,重启后提醒回来 | `[CAT]` README |
| 组织者护栏 | 宿主基础设施类插件**不可切换**;拒绝关掉三个入口里的**最后一个**(防自锁) | `[CAT]` + `[DSH]` `protectsManager` |
| 卸载自身 | 有一个 opt-in 清理,会**顺手删掉它写过的 disable 行**,否则被它关掉的插件永远回不来 | `[CAT]` README |

---

## 1. 它在产品里的位置

| 七层 | 动作 |
|---|---|
| **7 分发** | 目录 / 安装 / 更新 / 备份 / 一套可用的自救路径 |
| 3 槽位 | `Plugins` 页的 `Plugin Market` 标签(0.2.1+);0.2.0 及更旧走 `Settings → Plugin Market` |
| 2 表层 | 卡片、安装对话框、评论区、日志导出 |

**它的位置判断**:别人做"商店",它做"**商店 + 消防通道**"。下载量第 1 不是因为界面好看,而是因为**它是在用户最坏时刻唯一还在的东西**。

---

## 2. 机制(可照抄的部分)

### 2.1 救生页:六个要素,一个都不能少

| 要素 | 事实 | 为什么必须这样 |
|---|---|---|
| **根因** | DSH 启动**全有或全无**:一个插件加载不了,整个进程停下,而市场自己的 UI 就死在这个 host 里 | 所以救生页**不能**寄生在宿主里 |
| **页面** | 启动失败提示里多一个 **Adjust plugins**:被 DSH 归咎的插件**标红且不勾选**,用户选"下次启动启用哪些" | 页面只提供**一个决定** |
| **写入** | 通过**与热开关同一批** `cordis.patch.yml` 行(外加 `dsh.profile.bundles` 作为 disable-carrier),然后**重试启动** | 复用同一套持久层 → 用户在别处也能看到/改 |
| **谁在服务** | **detached restart helper**,在**页面本来就在轮询的那个地址**上 | 换地址 = 用户对着一个打不开的页签 |
| **独立模式** | 直接打开那个 URL 会渲染**同一页的独立版** | 记不住地址的用户也能进 |
| **何时不出现** | DSH 正常启动时**什么都不出现** | 救生页不能变成日常噪音 |

配套的三个上游原语(做同类工具时直接挂上去):

| 原语 | 用途 |
|---|---|
| `dsh rescue --from-default-profile <name>` | 用官方模板**替换**自定义 profile 再启动;实现是 staging 目录组装 + 两次 rename + 失败回滚 + 并发检测(`profile-boot-C14i-8IN.js:146-200`) |
| `sanitizeProfile` | 备份成 `cordis.patch.yml.bak-<ts>[-n]`,只保留调用方给的 recovery bundles(`app-boot:1242-1257`) |
| `--dump-default-config` | 打印不含用户层与 `--patch` 的 profile 树;上游明文把它定位为"**坏掉 `cordis.patch.yml` 的 recovery diagnostic**" |

### 2.2 重启按钮:一个会杀死自己的动作

| 事实 | 结论 |
|---|---|
| 一键重启启动一个 **detached** 替代进程 | 替代进程要**活过**原终端 |
| 重启端点**额外要求直接回环客户端**(转发请求被拒) | 防反代把它暴露到公网 |
| 重新启动的是**完全相同的** entry、参数、环境、工作目录 | 重启不能改变运行条件 |
| **systemd 的服务主进程上按钮自动隐藏** | 否则会把 takeover 进程连同该 unit 的 cgroup 一起杀掉,**服务不会回来** |
| 判定要求 **systemd 标记 AND 是 unit 主进程** | `INVOCATION_ID` 会被所有后代继承(普通终端也算) |
| `pm2` / `launchd` **未检测** | 这些部署要用户显式设 `allowRestart: false` |
| 自证 | `GET /dsh-market/status` → `"restart": false` |

配置写法(极易抄错):

```yaml
- id: dsh-market
  name: dshmarket
  config:            # 必须在 config: 下
    allowRestart: false   # 顶层写 allowRestart 会被【静默忽略】(issue #227)
```

> **两条硬规则**:① "程序能自证某个开关生效了"是好设计的标准动作——**不要只靠日志**;② 任何"重启父进程"的功能,先回答"**我会不会连自己一起杀掉**"。

### 2.3 索引源:校验放在每次使用前

| 层 | 校验 |
|---|---|
| schema | `z.array(z.string().pattern(/^https?:\/\/\S+$/u))` |
| **每次使用前** | `normalizeIndexUrl`:必须可解析、必须 http/https、**不许带账号密码**、**不许带 fragment**;非规范形式直接报 `Index URL is not in canonical form; use <canon>` |
| 去重 | `setIndexes` 拒绝重复 URL(`plugin-market/invalid-index-url … reason: "duplicate"`) |
| 拉取 | `redirect: "error"`、`accept: application/json`、`AbortSignal.any([lifetime, timeout])`、`content-length` 或累计字节超 `maxBytes` 立刻 cancel、错误信息用 `cause` 链最多 4 层拼出真实原因 |
| 并发 | 同一 URL 的并发读**共享一个 promise**(`pending` Map + `finally` 清理) |

> **为什么是"每次使用前"而不是"配置时"**:配置可以经由 settings、文件、环境变量绕过 schema。**判据是"我要不要用它",不是"它当初怎么写进来的"。**

### 2.4 索引格式:让错误自己指出位置

| 规则 | 值 |
|---|---|
| 格式版本 | `format` 必须为 **1** |
| 报错形态 | `MarketIndexError{path, reason}`,`path` 如 `$.plugins[0].versions[1].version` |
| 版本数组 | **按 SemVer 降序、不得重复**;`publishTimestamp` 必须是 [0, 10¹¹) 的整数秒 |
| git 源 | `commit` 必须 **`/^[0-9a-f]{40}$/u`**;安装 spec 拼 `git+<url>.git#<commit>[&path:/<dir>]` |
| `engines.dsh` | 不许是 `workspace:` 前缀 |
| 图标 | `data:` 只允许 svg/png/jpeg/webp base64 且解码 **≤32 KiB**;相对图标必须解析成 https **或与索引同源** |
| 字段 | `homepage` 允许 query/fragment 但要 http(s);`repository.url` **不许**带 query/fragment |

### 2.5 版本与更新:按"来源"而不是"名字"

| 规则 | 事实 |
|---|---|
| 更新语义 | npm 包比版本号;git 装比 **pinned commit vs HEAD** |
| 防"更新成另一个插件" | 从 archive 链接装的插件**只用自己的源**更新;目录里**同名**条目永不作它的更新候选 |
| 安装源优先级 | **repo 验证过的 npm** → 作者提供的 **GitHub Release 预构建 tarball** → **整仓源码**。预构建"通常几秒,且不需要本地构建脚本" |
| 构建脚本 | pnpm ≥10 默认**阻断**;放行是**逐包显式**选择,落成 `pnpm-workspace.yaml` 的 `allowBuilds: {<pkg>: true}`(拒绝通配符与 YAML 锚点) |
| 自更新通道 | stable / beta / dev(dev 需开开发者模式);**只作用于市场自己,从不作用于用户别的插件** |

### 2.6 与宿主互斥:别自造锁

上游对 profile 的所有变更都在 `withFileLock(<profile>/package.json)` 里:以 `wx` 建 `.lock` 写 PID、`ESRCH` 时接管旧锁、20→200ms 退避、默认只等 **2000ms**(`dsh-atomic-write/lib/index.js:12-16,189-220`);CLI 路线 `waitMs: 12e4`。

> **抄这条**:要和宿主互斥,就用**它那一把锁**(`<profile>/package.json.lock`),别自造;自己造锁 = 两把锁谁也保护不了谁。

---

## 3. 体验

### 3.1 首次路径(逐屏)

| 步 | 看到 | 坑 |
|---|---|---|
| 1 · 装 | Desktop:`Settings → Plugins` 搜索安装,**不用命令行**;普通 web:`dsh plugin --profile web add dshmarket` 后重启 | **桌面 App 用 `--profile web` 装会"报告成功但不出现"**——它装进了 `profiles/web`,不是 App 用的 profile |
| 2 · 打开 | `Plugins` 页 → **Plugin Market** 标签(0.2.1+);更旧走 `Settings → Plugin Market` | 入口按版本降级 |
| 3 · 浏览 | 分类、star、top/new、双语描述;卡片上直接显示 `engines.dsh` 或整锁步 peers 的宿主要求 | 兼容性"未声明就是未知",不猜 |
| 4 · 点卡片 | 作者精选截图**零额外请求**;没有精选的**在打开对话框时**才抽 README;卡片内嵌评论区 | 图片只从 GitHub 加载 |
| 5 · 装 | **先确认来源**,看实时进度;**多数插件刷新页面即生效,不用重启** | — |
| 6 · 需要重启 | 变更横幅旁给一键重启 | 见 §2.2 |
| 7 · 卸载 | 两步确认;本次会话装的**即时**移除 | — |

### 3.2 它把"降级"写成 16 条可读状态

| 情形 | 它怎么做 |
|---|---|
| 旧宿主 | **自我禁用** + 控制台说明:"如果 Plugin Market 入口从不出现,通常就是这个原因" |
| 缺 pnpm | 检测 + **一键自动装**(零术语) |
| 目录拉取失败 | 报**真实原因 + 耗时** + Retry |
| 目录拿不到 | **不做快照**(理由见 §0);镜像用 `DSHM_REGISTRY_URL` 指向同形状 `plugins.json` |
| 中国区 | npm 镜像优先、origin 兜底;区域只检测一次并记住;Git refs / README / 头像**各自一条回退序**,只在上游失败时切换,**拒收伪装成 200 的代理错误页** |
| 无精选截图 | 打开对话框时抽 README |
| 兼容性未知 | **显示"未知"**,只隐藏**确认**不兼容的 |
| 提醒 | **忽略 ≠ 关闭**:忽略只在本次启动有效 |
| 三个入口 | 可分别开关,但**拒绝关掉最后一个** |

### 3.3 模型看到的

`[DSH]` 模型的 `plugin_market` 工具返回结构化 JSON;**市场里的描述文本是第三方内容**,不得当指令执行。人在界面看到的是渲染后的卡片。

---

## 4. 证据与边界

| 口径 | 值 |
|---|---|
| ★ / npm | **9,902 / 813,066**（2026-10-31 实时；本线第 1） |
| 名单内被引 | **12** |
| 硬依赖 | `dsh web 0.1.0-rc.6` 起 |
| **已知偏差** | ① 只认精选 registry = **中心化**,新源需进白名单;② 桌面壳自带 dsh 可能比 npm 版旧(#139);③ **`config:` 是整块替换,不是深合并**——写 `config:` 会覆盖该行原有 config;④ 坏 patch 文件**启动即失败**,不静默跳过(这是对的,但用户会看到"起不来") |


---

## 5. 借鉴食谱表(本卡的产出物)

| 要解决的问题 | 照它的做法 | 你要改的地方 | 抄错的后果 |
|---|---|---|---|
| 宿主是"全有或全无" | 自带**救生页**,由宿主**进程外**的 helper 服务 | 你的"启动"可能是 worker/服务;helper 要能独立拉起 | 救生页也挂在坏掉的宿主上 → 一起起不来,用户只能删目录 |
| 救生页放哪个地址 | **用户已经在轮询的那个地址** | — | 换端口/换路径 → 用户对着一个打不开的页签 |
| 救生页给什么 | **只给一个决定**:勾选"下次启用哪些",被归咎的**标红且不勾** | 你的"配置"可能是 JSON/YAML,落成同一套持久层 | 救生页变成第二个设置中心 → 用户在这里改坏了,又没有第二个救生页 |
| 救生页写哪里 | 复用**热开关的同一批行** + 必要时改 bundles | 关键:**只禁行不够**,还要从 bundle 数组摘掉 | 图标显示"已停用",实际还在加载 |
| 一个会重启自己的按钮 | 先判"**我会不会把自己杀掉**":容器/服务管理器/主进程 | 至少覆盖 systemd、launchd、pm2、容器 | systemd 下点重启 → 服务再也不回来 |
| 按钮被隐藏了,怎么知道 | 状态端点自证(`"restart": false`) | — | 用户以为按钮坏了 / 你以为它还在 |
| 开关被静默忽略 | 把可配置项放在**框架真正读取的那一层**(此处是 `config:` 下) | 读一遍你框架的"我只把这个子对象传给插件"规则 | 写了顶层键 → 静默无效,查一天 |
| 外部索引/配置源 | **每次使用前**再校验(规范形式、无凭据、无 fragment、不重复) | 你的源可能是 URL/文件/环境变量 | 只在保存时校验 → settings/环境变量绕过,schema 形同虚设 |
| 拉远端一份清单 | 超时 + 字节上限(边收边判)+ 缓存 TTL + `redirect: "error"` + 同 URL 合并请求 | 数字按你的清单大小定 | 无字节上限 → 一个坏镜像能把内存打满;不合并 → 一次刷新打 20 个请求 |
| 清单格式演进 | 显式 `format: 1` + 违规报 **JSON 路径** + 只报第一条 | — | "格式错误"四个字 → 作者无从修 |
| 版本可复现 | git 源强制 40 位 commit;npm 源 `--save-exact` | 两层都要:协议层钉死 + 运行时不解析 `latest` | 只做一层 → 另一条路径仍会漂 |
| 更新会不会换成别的插件 | **按来源更新**:同名目录条目不作 archive 装的更新候选 | — | 用户点更新,装上了另一个同名包 |
| 目录拿不到时要不要兜底 | **先问"过期答案是不是错误答案"**:首启推荐可以兜(标注过期),**安装入口不能兜** | 报真实原因 + 耗时 + Retry | 对每天增量的目录用旧快照 → "今早发布的插件不存在" |
| 构建脚本 | 默认阻断,**逐包**显式放行,落成可审查的配置 | pnpm ≥10 / npm 的同类开关 | 用通配符全放行 → 等于任意代码执行 |
| 和宿主抢同一个文件 | 用**宿主自己那把锁**(`<profile>/package.json.lock`) | — | 自造锁 → 两把锁互不保护,写出半个 `package.json` |
| 首页要"零术语" | 缺依赖就**检测 + 一键装**,而不是让用户看 `ENOENT` | — | 首屏报错栈 → 用户在这里就流失 |
| 组织者护栏 | 基础设施类插件**不可切换**;拒绝关掉最后一个入口 | 你的"最后一个"可能是唯一的管理面 | 用户把自己锁在门外 |

---

## 6. 失效条件与降级

| 触发 | 行为 |
|---|---|
| 旧宿主 | 自我禁用 + 控制台说明入口为何不出现 |
| 缺 pnpm | 检测 + 一键自动装 |
| 目录拉取失败 | 真实原因 + 耗时 + Retry |
| 镜像故障 | `DSHM_REGISTRY_URL` 指同形状 `plugins.json`;分资源回退序;记住上次可用路由 |
| 索引源不合规 | **只列错误,永不 fetch** |
| patch 文件畸形 | 启动**大声失败**;不静默跳过;救生页提供 Adjust plugins |
| 通过自救后仍有坏插件 | `dsh rescue --from-default-profile` / `sanitizeProfile` / `--dump-default-config` 三条原语 |
| 启动失败诊断 | 写到 `$DSH_HOME/logs/startup-*.log`(目录 `0700`、文件 `0600`、`wx` 不覆盖);写不进去就整份打到 stderr **而不是谎报路径**;开头固定告警:"Raw diagnostics may contain configuration or credential values from plugin errors. Review before sharing." |
| 报 bug | 一键导出**脱敏**纯文本日志(家目录路径与凭据形状遮蔽,**不上传任何地方**) |
| WebDAV 同步 | 仅 https、**拒绝私网目标**、密码不存浏览器 |
| 认证请求 | 一律直连 `api.github.com`,**bearer token 永不发给公共加速服务**;源码包留在 canonical codeload(保住 pnpm 的 integrity 校验) |

---

## 7. 开放问题

- [ ] `[OPEN]` 只认精选 registry 换来安全,代价是**新源进不来**。能不能让"自建源"走一条**显式降级信任**的路(签名的第三方 registry)?
- [ ] `[OPEN]` 救生页只给"下次启用哪些"。**能不能也支持"回滚到上一个能跑的配置"**(带快照)?
- [ ] `[OPEN]` 它不做目录快照是对的,但用户断网时**完全看不到已装插件的说明**。这两件事能分开吗(装的操作要新鲜,已装的信息可以缓存)?
- [ ] `[OPEN]` `pm2`/`launchd`/容器未被检测,只能靠用户手设。**上游是否该提供一个"我是不是被某个 supervisor 管着"的标准信号?**
- [ ] `[OPEN]` 它和 `41_首启推荐` 在"目录拿不到"上给出**相反且都正确**的答案。这个判断("过期答案是不是错误答案")值得写进本线的口径吗?
- [ ] `[OPEN]` 自更新分三条通道,但**只作用于市场自己**。生态是否需要一套统一的"插件自更新"约定,还是应该由市场独占?
