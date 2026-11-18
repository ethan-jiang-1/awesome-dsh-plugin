#!/usr/bin/env python3
"""cardmeta.py:卡片 frontmatter 的迁移 / 抽取 / 校验辅助。

frontmatter 是卡片元数据的单一源:
  kind / domain / subcategory / repo / commit / evidence / status / asof

用法:
  python3 _digested/ecosystem/cardmeta.py --check     # 只报告缺失/不一致
  python3 _digested/ecosystem/cardmeta.py --write     # 给缺 frontmatter 的卡补上
  python3 _digested/ecosystem/cardmeta.py --json      # 输出卡片元数据 JSON
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CARD_GLOB = "_digested/view_*/*/[0-9]*.md"

STATUS_BY_PATH = {
    "view_ui/enhance-shell/02-at-file.md": "deprecated",
    "view_session/rewind-edit/02-dsh-message-edit.md": "stale",
    "view_workflow/vertical-preset/01-ai-novel-writer.md": "frozen",
    "view_workflow/multi-agent/03-dsh-workflow.md": "watch",
    "view_workflow/multi-agent/04-agent-team-gui.md": "watch",
}
REFERENCE = {"view_memory/host-backed/02-openviking.md"}
ALLOWED_STATUS = {"active", "watch", "stale", "deprecated", "frozen", "archived"}


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    meta = {}
    for line in text[4:end].splitlines():
        m = re.match(r"([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if m:
            meta[m.group(1)] = m.group(2).strip()
    return meta


def clean_repo(name):
    s = str(name or "").strip().strip("`")
    s = s.split("#", 1)[0]
    s = s.split("/tree/", 1)[0]
    parts = [p for p in s.split("/") if p]
    if len(parts) < 2:
        return None
    return f"{parts[0]}/{parts[1]}"


def infer(path):
    rel = path.relative_to(ROOT / "_digested").as_posix()
    text = path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    if meta:
        return meta

    head = "\n".join(text.splitlines()[:16])
    ev = re.search(r"证据等级[:：]\s*(★+)", head)
    commit = re.search(r"@(?:commit\s+)?([0-9a-f]{7,40})", head, re.I)
    asof = "2026-11-18"
    for line in text.splitlines():
        if "数据截止" in line:
            line = line.split("⚠", 1)[0]
            m = re.search(r"(20\d{2}-\d{2}-\d{2})", line)
            if m:
                asof = m.group(1)
            break

    repo = None
    for line in text.splitlines():
        if line.startswith("| 条目") or line.startswith("| 官方条目"):
            m = re.search(r"`([^`]+/[^`]+)`", line)
            if m:
                repo = clean_repo(m.group(1))
                break

    parts = rel.split("/")
    domain = parts[0].replace("view_", "", 1)
    subcategory = parts[1]
    if rel in REFERENCE:
        kind = "reference"
    else:
        kind = "card"
    meta = {
        "kind": kind,
        "domain": domain,
        "subcategory": subcategory,
        "repo": repo or "",
        "commit": (commit.group(1) if commit else ""),
        "evidence": str(len(ev.group(1)) if ev else ""),
        "status": STATUS_BY_PATH.get(rel, "active"),
        "asof": asof,
    }
    return meta


def render(meta):
    order = ["kind", "domain", "subcategory", "repo", "commit",
             "evidence", "status", "asof"]
    lines = ["---"]
    for key in order:
        lines.append(f"{key}: {meta.get(key, '')}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    cards = sorted(ROOT.glob(CARD_GLOB))
    rows, problems = [], []
    for p in cards:
        rel = p.relative_to(ROOT / "_digested").as_posix()
        meta = infer(p)
        rows.append({"path": rel, **meta})
        for key in ("kind", "domain", "subcategory", "repo", "evidence", "status", "asof"):
            if not meta.get(key):
                problems.append(f"{rel}: 缺 {key}")
        if meta.get("kind") == "card" and not meta.get("commit"):
            problems.append(f"{rel}: ★★★ 卡缺 commit")
        if meta.get("status") not in ALLOWED_STATUS:
            problems.append(f"{rel}: status 非法 {meta.get('status')!r}")
        if args.write and not p.read_text(encoding="utf-8").startswith("---\n"):
            p.write_text(render(meta) + p.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"prefixed {rel}")

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    if args.check or not args.write:
        for problem in problems:
            print(f"✗ {problem}", file=sys.stderr)
        print(f"{len(rows)} cards, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
