# system · 全局运转图

> 状态:**骨架,未消化。** 本页目前只划范围、列阅读入口,不承诺任何已验证结论。

## 定位

把 awesome-dsh-plugin 当一台机器看：一条收录 PR 从打开到变成 README 条目和站点详情页，中间流经哪些环节、谁是事实源、谁是生成物、哪里有门禁、哪里有自动化在持续改写数据。

这个仓库的本质假设是：**人只编辑少量小 YAML;README（600KB+）、站点、遥测 JSON 全部由脚本和 workflow 生产。** 读懂数据流向比读懂单个脚本更重要。

## 主要角色（按 data flow,待逐一验证）

1. **贡献者** → 提 PR,新增/修改 `data/plugins/<name>.yaml`
2. **准入门禁** → `.github/workflows/pr-check.yml` / `pr-gate.yml` / `pr-guard.yml` / `regate.yml`,调用 `scripts/check-submission.mjs`、`scripts/check-bleed.mjs`
3. **合并后重建** → `build-site.yml`:跑 `generate-readme.mjs` 更新双语 README、`build-site.mjs` 出站
4. **持续遥测** → probe-* 家族定时采集 stars/downloads/npm 版本等,写回 `data/*.json`
5. **腐坏检测** → `scan-decay.mjs` + `decay-scan.yml` 找死链、失联上游
6. **发布物** → 根目录双语 README、GitHub Pages 站点

## 待回答的全局问题

- [ ] README 和站点是否共享同一次数据加载(`scripts/lib/entries.mjs`)？
- [ ] 四个边车 JSON(added-dates/downloads/screenshots/stars)里哪些允许人工编辑,哪些只许机器写?
- [ ] regate 与 pr-guard 为什么分开,各自的触发条件是什么?
- [ ] 中英双语的权威侧是哪份,另一份如何派生?

## 阅读入口

- `contributing.md`(对外承诺的流程)
- 各 topic 的 `00-map.md`(按上面顺序)
