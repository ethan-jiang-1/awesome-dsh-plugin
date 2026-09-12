# 03 · regate 与 check-bleed:判决保鲜与描述污染检测

> 基线:`upstream@38976afd`(0001 复核;regate.yml 197→**218 行**,check-bleed 94 行未变)。

## regate.yml(218 行):判决是快照

核心论断在工作流头注释(:1-18):判决过期有两种方式——**被时钟过期**(0.5 天的仓库几小时后就合格了,但没人重查)和**被代码过期**(门禁本身改了,旧判决全是已不存在的代码作出的;"stale red 会被人注意到,stale green 会被合并")。所以它重跑 `PR check`(从而级联触发 gate)于以下开放 PR:

### 四个 urgent 理由(:132-172)

| 理由 | 判定 | 语义 |
|------|------|------|
| `never` | gate check-run 不存在 | PR 早于 gate 出生,或 run 死在贴出判决之前——"没被判过"与"通过"在扫队列时不可区分 |
| `stale` | 判决时间 < 门禁最后变更时间 | 门禁最后变更时刻 = `pr-gate.yml` 与 `scripts/check-submission.mjs` 两路径最近 commit 时间取大者(:70-79) |
| `aged` | conclusion=failure 且 summary 匹配 `/days old\|commit\(s\)/` 且距上次 ≥24h | "时间能解决的失败"。0001:正则保留 `commit(s)` 兼容存量判决(门槛已删,新判决只有 days old 文案);配合 check-submission 的新文案("nothing to do, no need to resubmit"),aged PR 现在**静默自愈**,作者不再被支使去重开 PR |
| `unverified` | conclusion=neutral | **gate fail-open 的闭环**:放行了但没人 vouch 的条目,`aged` 只匹配 failure、`passStale` 只匹配 success,不补这条 neutral 将永远无人复查(:147-158) |

第五个**非紧急**理由 `passStale`(:160-170):success 满 `PASS_STALE_MS = 48h`。绿灯只是"对当时那个仓库的陈述"——作者可以 force-push 掉提交、改名让 URL 404、干脆删库,绿灯依旧绿。#1022:一条"All 11 entries pass"一天后四个仓库三个跌破提交门槛一个 404,靠人肉复核才发现,"which is not a control"(不算控制手段)。

### 成本与排序纪律

- `MAX_RERUNS = 20`:从 12 提上来——重跑陈旧判决规则上线后有积压要清。
- 先收集再执行:urgent 永远优先于 speculative(«那些 PR 是被卡住的,绿的可能错只是"可能"»)。
- oldest-first 是修出来的(:84-90):`pulls.list` 返回最新在前,#2146 曾挂"aged in"判决 119 小时——每一轮 20 个名额都被更新的 PR 吃掉。
- **0001:排序从两档改三档**(blocking > revalidate > speculative):门禁文件一变更,全体 open 判决同时变 stale(~140 个),按 PR 号升序会让积压 backlog 排在真正被卡的投稿前面——"一个只等仓库满一天的插件要等两天而不是六小时",触发条件仅仅是维护者改了门禁注释。blocking(没人 vouch 或卡在时钟上)优先于 revalidate(判决大概率仍对,只是出于尽责重问);diligence yields。
- run id 不再依赖最近 100 次 run 的 SHA 索引(:92-97):任何两小时窗口外的 push 都会被静默跳过;改从 check-run 自带的 details_url 里抠 run id。
- 全部包在 try/catch 里且把 403/429 当"本轮少干点",绝不为配额紧张发红色告警(:55-56, :194-196)。
- check 本身失败的 PR 直接跳过(:130):内容错了时间治不好,重跑纯烧配额。

## check-bleed.mjs(94 行):跨条目文本污染指纹

#1348 案的产物:一个声称刷新 dsh-notifier 条目的 PR,顺手把 dsh-notifier 的新句子追加到了无关插件 dsh-cyber-particle 的描述上。发生过两次,YAML 合法、README 能再生、lint 干净——没有检查看「PR 是否碰了它不该碰的条目」。检测机制:

- 把所有条目、双语描述压空白后切成 **40 字符滑动窗口**(squashed runs,RUN=40,:31)。阈值依据:40 时全列表(~1170 个条目时代)只有五对相似,全为真实雷同;真正的污染共享远不止 40 字符。
- 哈希索引 run→文件对;跳过同 owner 对(sibling 插件天生共用样板文案,:73);带 `--base` 时仅当 PR 真的动过其中一方才报(:75)。
- **报而不拦**:相似插件合法地相似(两个 web-search 插件),这是给评审的信号不是闸门;输出明确提醒"先确认是不是误带,再当缺陷处理"(:93-94)。
- 与 pr-gate 的 modifiedNote 互补:gate 靠 diff-filter=M 列出被改写的既有条目让评审追问「为什么在这」;bleed 则回答「改写有没有夹带别人的文字」。

## 小结:三道防污染屏障

| 层 | 手段 | 抓什么 |
|----|------|--------|
| pr-gate extract(M 列表) | 流程性披露 | PR 改写了哪些既有条目 |
| check-bleed | 内容指纹 | 描述文本的跨条目串染 |
| pr-check stale-fork 守卫 | README 净增减 | fork 落后导致的成批丢失 |

三者都源于同一事故家族(#502 / #1348 / #1554/#1635/#1614),共同信条:**机械检查全绿 ≠ 内容没坏;凡是机器说不了的,就把它摆到评审眼前。**
