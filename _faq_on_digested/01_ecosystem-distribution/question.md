# Q01 · 当前收录的插件呈什么分布?——技术、业务、用户体验三个视角

## 问题

2026-08-27 提出这一问时,`data/plugins/*.yml` 已有 2286 条(生态仅诞生 14 天)。逐个看既不现实也不必要,真正的问题是:**这堆东西按三个不同的透镜各自呈现什么结构**——

1. **技术上**:它们靠什么实现?技术的重心在算法、在集成、还是在壳?
2. **业务上**:谁在生产?有没有商业模式或至少是商业姿态?
3. **用户体验上**:创新发生在哪里?替代了应用,还是寄生在既有窗口里?

## 背景

提问者的站位是**评估者**:想知道这个生态"在发生什么、值什么",不是想成为其中作者。因此三个视角都以"能形成判断"为标准取舍细节。

## 使用的数据与来源

- `_digested/ecosystem/census.py`(标准库脚本)输出@ `main@5e7dc7eb`,2026-08-27:分类分布、34 技术标签、共现对、作者集中度、首录日期演化、stars/npm 成熟度;
- 为本题补充的两个专项统计(脚本逻辑同 census.load_entries,正则如下):
  - **壳件词汇**:`面板|sidebar|侧栏|输入框|chat.? ?window|panel|状态栏|menubar|气泡` 在 en+zh 描述上的命中;
  - **聚合型仓库**:repo 名匹配 `hub|packs?|collection|-plugins$|^plugins-|bundle` 的独立 repo 及其贡献条目数;
- [`_digested/ecosystem/01-scenario-taxonomy.md`](../../_digested/ecosystem/01-scenario-taxonomy.md)、[`02-tech-landscape.md`](../../_digested/ecosystem/02-tech-landscape.md)、[`03-growth-maturity.md`](../../_digested/ecosystem/03-growth-maturity.md);
- 根 `README.md`:7-9(DSH 定义)@ `main@5e7dc7eb`。

## 答案

见 [answer.md](answer.md)。
