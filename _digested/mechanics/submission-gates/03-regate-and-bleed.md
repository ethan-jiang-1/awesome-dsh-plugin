# 03 · regate 与 check-bleed:判决保鲜与描述污染检测

> 基线:`upstream@c18ba4a0d`(0002 复核;regate.yml 218→**369 行**,check-bleed 94 行未变)。

## regate.yml(369 行):判决是快照

核心论断在工作流头注释(:1-18):判决过期有两种方式——**被时钟过期**(0.5 天的仓库几小时后就合格了,但没人重查)和**被代码过期**(门禁本身改了,旧判决全是已不存在的代码作出的;"stale red 会被人注意到,stale green 会被合并")。所以它重跑 `PR check`(从而级联触发 gate)于以下开放 PR:

### 理由分类(0001 四类 urgent → 0002 **六个 blocking + 三个调度档**)

| 理由 | 判定 | 语义 |
|------|------|------|
| `never` | gate check-run 不存在 | PR 早于 gate 出生,或 run 死在贴出判决之前——"没被判过"与"通过"在扫队列时不可区分 |
| `stale` | 判决时间 < **门禁**最后变更时间 | `gateChangedAt` = `pr-gate.yml` 与 `scripts/check-submission.mjs` 两路径最近 commit 取大者(:90-94,与 0001 相同) |
| **`checkStaleRed`(0002 新增)** | 红 `check` 的判决时间 < **检查**最后变更时间 | **0002 的核心新论点:过期证据不只属于 gate**。`checkChangedAt`(:95-99)覆盖 `.github/workflows/pr-check.yml`、`scripts/build-site.mjs`、`scripts/generate-readme.mjs`、`scripts/lib` 四个输入,注释解释:"`check` … builds the WHOLE catalog, so it fails for reasons that have nothing to do with the pull request"——**#4731 在 2026-09-08→09-12 让每一个开放 PR 都红着** |
| `aged` | conclusion=failure 且 summary 匹配 `/days old\|commit\(s\)/`(:223)且距上次 ≥24h | "时间能解决的失败"。正则仍保留 `commit(s)` 分支兼容存量判决(门槛已删,**该分支现在大概已是死代码**,未证实);配合 check-submission 的文案,aged PR **静默自愈**,作者不再被支使去重开 PR |
| `unverified` | conclusion=neutral | **gate fail-open 的闭环**:放行了但没人 vouch 的条目,`aged` 只匹配 failure、`passStale` 只匹配 success,不补这条 neutral 将永远无人复查 |
| **`faulted`(0002 新增)** | gate conclusion=failure 且标题是 `The gate could not run`,冷却 1 小时 | 门禁自己跑挂不是投稿的问题(#5083 因限流 fault 于 2026-09-14,"was still sitting on that verdict nine days later")。冷却用内联 `3600*1000`(:249-252),没有抽成命名常量 |
| `passStale`(**非紧急**) | success 满 `PASS_STALE_MS = 48h`(:262) | 绿灯只是"对当时那个仓库的陈述"——作者可以 force-push 掉提交、改名让 URL 404、干脆删库,绿灯依旧绿。#1022:一条"All 11 entries pass"一天后四个仓库三个跌破提交门槛一个 404,靠人肉复核才发现,"which is not a control" |

### 0002 的第二个新论点:新鲜的红才是否决票

```js
if (checkRedFresh && !aged && !unverified && !faulted) continue   // :298
```

0001 的写法是"check 本身失败的 PR 直接跳过(:147):内容错了时间治不好,重跑纯烧配额"。0002 把它收窄成**只有"新鲜的红"**才否决,并且豁免 `aged`/`unverified`/`faulted` 三类——注释:"all three mean the gate itself needs re-asking"。**#5533 因此被连续跳过 9 次**。`never`、`stale`、`passStale` 仍在否决之下。

### 成本与排序纪律

- `MAX_RERUNS = 20`:从 12 提上来——重跑陈旧判决规则上线后有积压要清。
- oldest-first 是修出来的(:100-107):`pulls.list` 返回最新在前,#2146 曾挂"aged in"判决 119 小时——每一轮 20 个名额都被更新的 PR 吃掉。
- 排序三档(blocking > revalidate > speculative):门禁文件一变更,全体 open 判决同时变 stale(~140 个),按 PR 号升序会让积压 backlog 排在真正被卡的投稿前面——"一个只等仓库满一天的插件要等两天而不是六小时"。**0002:blocking 档新增 `faulted` 与 `checkStaleRed`**(:302/:304);diligence yields。
- run id 不再依赖最近 100 次 run 的 SHA 索引(:113-118):任何两小时窗口外的 push 都会被静默跳过;改从 check-run 自带的 details_url 里抠 run id。
- **403 不再等于限流(0002 重写,:316-364)**:只有 `429`、或 403 且正文匹配 `/rate limit/i` 才终止本轮;`tooOld`(运行时间超过一个月,403 + `/over a month ago/i`)现在**跳过该 PR 并点名**,继续处理其余(:333-346)。事故:**#932 在 2026-09-18 跨过 30 天,把 8 轮里的 7 轮打死**;当时有 28 个开放 PR 挂着超龄 run。另一个误判案例:#5582 的 "This workflow is already running" 也是 403,同样不该停。
- 全部包在 try/catch 里且把配额紧张当"本轮少干点",绝不为配额紧张发红色告警。

## check-bleed.mjs(94 行,**未变**):跨条目文本污染指纹

#1348 案的产物:一个声称刷新 dsh-notifier 条目的 PR,顺手把 dsh-notifier 的新句子追加到了无关插件 dsh-cyber-particle 的描述上。发生过两次,YAML 合法、README 能再生、lint 干净——没有检查看「PR 是否碰了它不该碰的条目」。检测机制:

- 把所有条目、双语描述压空白后切成 **40 字符滑动窗口**(squashed runs,RUN=40,:31)。阈值依据:40 时全列表(~1170 个条目时代)只有五对相似,全为真实雷同;真正的污染共享远不止 40 字符。
- 哈希索引 run→文件对;跳过同 owner 对(sibling 插件天生共用样板文案,:73);带 `--base` 时仅当 PR 真的动过其中一方才报(:75)。
- **报而不拦**:相似插件合法地相似(两个 web-search 插件),这是给评审的信号不是闸门;输出明确提醒"先确认是不是误带,再当缺陷处理"(:93-94)。
- 与 pr-gate 的 modifiedNote 互补:gate 靠 diff-filter=M 列出被改写的既有条目让评审追问「为什么在这」;bleed 则回答「改写有没有夹带别人的文字」。

## 小结:0002 之后的六道防污染屏障

| 层 | 手段 | 抓什么 |
|----|------|--------|
| pr-check 条目路径守卫 | 路径形状匹配 | 添加路径 ≠ readEntries() glob 的放错层级条目(#3914/#3622) |
| pr-check README-row 守卫(0002 新增) | 生成行 ↔ 投稿文件对应 | 只改生成行、没带 yml 的 PR(#5845/#3168) |
| pr-gate extract(M 列表) | 流程性披露 | PR 改写了哪些既有条目 |
| pr-gate YAML 解析(0002 新增) | 语法可解析 | 名字对但内容不是 YAML、被 readEntries 静默丢弃(#4680) |
| check-bleed | 内容指纹 | 描述文本的跨条目串染 |
| pr-check stale-fork 守卫 | **条目文件**净增减 | fork 落后导致的成批丢失 |

六者同源于一个事故家族(#502 / #1348 / #1554/#1635/#1614/#3914/#3622/#5845/#4680),共同信条:**机械检查全绿 ≠ 内容没坏;凡是机器说不了的,就把它摆到评审眼前。**

## 待复核

- [ ] **0002**:`commit(s)` 分支是否真已无判决命中(正则仍在 regate.yml:223)——需拉一次开放 PR 队列的 summary 抽样
- [ ] **0002**:`faulted` 的 1 小时冷却是否够——#5083 那次 fault 的根因是限流,冷却期内配额未必恢复
