# `_data` — 卡片元数据与健康表(生成物)

这个目录是 `_digested` 的**单一数据源**。不要手改;改源后重跑:

```sh
# 1) 卡片 frontmatter 是元数据源;先在卡里改 kind/repo/commit/evidence/status/asof
# 2) 抓实时快照(需要 gh auth;npm 端点无鉴权)
python3 _digested/ecosystem/live_probe.py --asof 2026-11-19
# 3) 汇总成 cards.json / summary.json / health.md
python3 _digested/ecosystem/view_data.py
```

| 文件 | 内容 | 谁在用 |
|------|------|--------|
| `cards.json` | 40 张卡的 frontmatter + 实时 stars/pushed_at/downloads/flags | 领域册、选型矩阵、后续生成器 |
| `summary.json` | 域/子分类/证据级/状态计数 + live 覆盖率 | `_view`、领域册的计数核对 |
| `health.md` | 人读健康表:stars / pushed_at / 下载 / flags | 读者选型、每轮复核 |

口径:

- `stars` / `downloads` 来自 `_snapshots/live-2026-11-19.json`;`—` = 快照未覆盖或 npm 未发布,**不是 0**。
- `stale-candidate` 是“pushed_at 超过 90 天且卡片标 active/watch”的待复核项,不是自动判死。
- 卡片正文里的历史值仍带 `⚠` + `2026-08-19`;实时值以本目录 + 快照为准。
