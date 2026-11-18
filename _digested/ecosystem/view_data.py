#!/usr/bin/env python3
"""view_data.py:把卡片 frontmatter + 实时快照汇总成单一数据源。

产出:
  _digested/_data/cards.json    每张卡的元数据 + 实时指标
  _digested/_data/health.md     人读的健康/衰减表
  _digested/_data/summary.json  域/子分类/证据级/状态计数

用法:python3 _digested/ecosystem/view_data.py
"""
import importlib.util
import json
import sys
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "_digested" / "_data"
SNAP = Path(__file__).resolve().parent / "_snapshots" / "live-2026-11-19.json"

_spec = importlib.util.spec_from_file_location(
    "cardmeta", Path(__file__).resolve().parent / "cardmeta.py")
cardmeta = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cardmeta)

_spec2 = importlib.util.spec_from_file_location(
    "live_probe", Path(__file__).resolve().parent / "live_probe.py")
live_probe = importlib.util.module_from_spec(_spec2)
_spec2.loader.exec_module(live_probe)


def load_snapshot():
    if not SNAP.exists():
        return {"asof": None, "repos": {}, "packages": {}, "coverage": {}}
    return json.loads(SNAP.read_text())


def days_since(iso):
    if not iso:
        return None
    try:
        d = datetime.fromisoformat(iso.replace("Z", "+00:00")).date()
    except ValueError:
        return None
    return (date.today() - d).days


def main():
    snap = load_snapshot()
    repo_npm = dict(live_probe.load_index()[1])
    repo_npm.update({k: v for k, v in snap.get("repo_packages", {}).items() if v})
    cards = []
    for p in sorted(ROOT.glob(live_probe.CARD_GLOB)):
        meta = cardmeta.infer(p)
        repo = live_probe.repo_from_card(p) or meta.get("repo", "").lower()
        live = snap.get("repos", {}).get(repo, {})
        pkg = repo_npm.get(repo)
        dl = snap.get("packages", {}).get(pkg, {}) if pkg else {}
        flags = []
        if live.get("archived"):
            flags.append("archived")
        age = days_since(live.get("pushed_at"))
        if age is not None and age > 90 and meta.get("status") in {"active", "watch"}:
            flags.append(f"stale-candidate({age}d)")
        if age is not None and age <= 90 and meta.get("status") == "stale":
            flags.append(f"status-maybe-fixed({age}d)")
        if not live:
            flags.append("no-live-repo")
        cards.append({
            "path": p.relative_to(ROOT / "_digested").as_posix(),
            **meta,
            "stars_live": live.get("stars"),
            "pushed_at": live.get("pushed_at"),
            "archived": live.get("archived"),
            "npm": pkg,
            "downloads_live": dl.get("downloads"),
            "downloads_window": (f"{dl.get('start')}~{dl.get('end')}" if dl else None),
            "flags": flags,
        })

    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "cards.json").write_text(
        json.dumps(cards, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    by_domain = Counter(c["domain"] for c in cards)
    by_status = Counter(c["status"] for c in cards)
    by_evidence = Counter(c["evidence"] for c in cards)
    summary = {
        "asof_cards": max((c["asof"] for c in cards), default=None),
        "asof_live": snap.get("asof"),
        "cards": len(cards),
        "by_domain": dict(by_domain),
        "by_status": dict(by_status),
        "by_evidence": dict(by_evidence),
        "live_coverage": snap.get("coverage", {}),
    }
    (DATA / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 卡片健康表(生成物)",
        "",
        f"> 生成:`python3 _digested/ecosystem/view_data.py`;"
        f"实时快照 `{snap.get('asof')}`;结构 asof `{summary['asof_cards']}`。",
        "> `stars` / `downloads` 来自 live 快照;`—` = 快照未覆盖或未发布,不是 0。",
        "",
        "| 卡 | 域 | 证据 | 状态 | stars | pushed_at | 下载/月 | flags |",
        "|----|----|------|------|-------|-----------|---------|-------|",
    ]
    for c in sorted(cards, key=lambda x: (x["domain"], x["subcategory"], x["path"])):
        lines.append(
            f"| [{c['path'].split('/')[-1]}](../{c['path']}) | {c['domain']} | "
            f"{'★' * int(c['evidence'])} | {c['status']} | "
            f"{c['stars_live'] if c['stars_live'] is not None else '—'} | "
            f"{(c['pushed_at'] or '—')[:10]} | "
            f"{c['downloads_live'] if c['downloads_live'] is not None else '—'} | "
            f"{', '.join(c['flags']) or ''} |")
    (DATA / "health.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {DATA}/cards.json, summary.json, health.md ({len(cards)} cards)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
