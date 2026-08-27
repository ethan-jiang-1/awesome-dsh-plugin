# submission-gates · 提交与门禁

> 状态:**骨架,未消化。** 本页目前只划范围、列阅读入口,不承诺任何已验证结论。

## 定位

一个 3000+ PR 的注册表能不烂掉,靠的是机器门禁而不是人工 review。这个专题拆解 `.github/workflows/` 五条 workflow 与两个 check 脚本组成的准入机制。

## 范围承诺

- `pr-check.yml`(82 行)/ `pr-gate.yml`(275 行)/ `pr-guard.yml`(212 行):三者职责怎么分、什么事件触发、拦截什么
- `regate.yml`:重跑门禁的场景
- `scripts/check-submission.mjs` / `check-bleed.mjs`:校验规则清单(这条最值得逐条消化)
- `.github/pull_request_template.md`、`.github/ISSUE_TEMPLATE/*`:对人类的约定如何喂给机器校验
- 五条 workflow 合计约 1000 行,是本仓库行为密度最高的部分

## 待回答的问题

- [ ] check-bleed 查的 "bleed" 是什么?(标题/分类里混入不允许的内容?)
- [ ] 哪些规则 fail 时给出自动 fix 建议?
- [ ] ISSUE_TEMPLATE 的 list-problem 和 PR 流程的关系:报告问题走什么路径入库?
- [ ] regate 的触发者与权限边界;fork PR 拿到什么 secrets?

## 阅读入口

- `.github/workflows/pr-gate.yml`(最重的一条)
- `scripts/check-submission.mjs`
- `contributing.md`(对外口径,用 workflow 反向核对)

编号正文规范:`01-pr-gate.md` 起。
