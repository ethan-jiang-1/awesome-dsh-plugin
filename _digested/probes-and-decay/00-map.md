# probes-and-decay · 探针与衰减

> 状态:**骨架,未消化。** 本页目前只划范围、列阅读入口,不承诺任何已验证结论。

## 定位

列表的生命周期问题:收进来之后怎么办。probe-* 家族定期回到外部世界采集事实(stars、downloads、npm 版本、上游 README、截图),scan-decay 找失联和死链。这个专题拆"活着的数据怎么保鲜"。

## 范围承诺

- probe 家族各自的输入输出与写回目标:
  - `probe-stars.mjs` → `data/stars.json`
  - `probe-downloads.mjs` → `data/downloads.json`
  - `probe-npm.mjs`、`probe-updates.mjs`、`probe-readmes.mjs`、`probe-screenshots.mjs`、`probe-tarballs.mjs`
- `scripts/scan-decay.mjs` + `.github/workflows/decay-scan.yml`:腐坏判据与处置动作
- `scripts/publish-catalog.mjs` / `publish-updates.mjs`:探针结果的发布面
- 调度方式(定时?手动?)与限流礼貌(rate limit 处理)

## 待回答的问题

- [ ] 探针全量扫还是增量?2288 个插件一轮要多少次外部调用?
- [ ] scan-decay 发现死 repo 之后做什么:打标、开 issue 还是自动移除?
- [ ] probe-updates 和 probe-npm 的分工(版本号 vs 发布时间?)
- [ ] 外部 API 凭证从哪来,fork 上能否复跑整套探针?

## 阅读入口

- `.github/workflows/decay-scan.yml`(最短,先看调度)
- `scripts/probe-stars.mjs`(代表性样本)
- `scripts/lib/entries.mjs`(确认读取形态一致)

编号正文规范:`01-probe-family.md` 起。
