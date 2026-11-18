#!/usr/bin/env python3
"""live_probe.py:给卡片/锚抓一次带日期的实时指标快照。

覆盖:
  - 全部 `_digested/view_*/*/[0-9]*.md` 卡片的仓库;
  - `data/stars.json` 里星标最高的若干仓库;
  - `data/downloads.json` 里下载最高的若干仓库。

口径:
  - 仓库:GitHub REST `repos/{owner}/{repo}`(gh CLI 鉴权),星标/archived/pushed_at;
  - 下载:npm `downloads/point/last-month/{pkg}`(无鉴权),包名先取
    `raw-name-cache.json`,缺失时回源 `package.json`;
  - 单仓/单包失败只记入 coverage.errors,不写 0,不中断整轮;
    404 的 npm 包记入 coverage.unpublished(未发布 ≠ 异常)。

用法:
  python3 _digested/ecosystem/live_probe.py --asof 2026-11-19
  python3 _digested/ecosystem/live_probe.py --asof 2026-11-19 --max-repos 60 --max-pkgs 60
"""
import argparse
import base64
import importlib.util
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SNAP_DIR = Path(__file__).resolve().parent / "_snapshots"
CARD_GLOB = "_digested/view_*/*/[0-9]*.md"

_spec = importlib.util.spec_from_file_location(
    "delta", Path(__file__).resolve().parent / "delta.py")
delta = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(delta)


def repo_from_card(path):
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        for line in text.splitlines()[1:]:
            if line == "---":
                break
            m = re.match(r"repo:\s*(\S+)", line)
            if m:
                return delta.repo_key(m.group(1))
    for line in text.splitlines():
        if line.startswith("| 条目") or line.startswith("| 官方条目"):
            m = re.search(r"`([^`]+/[^`]+)`", line)
            if m:
                return delta.repo_key(m.group(1))
    return None


def load_index():
    """返回 (entries, repo->npm, repo->urls, stars_top, downloads_top)。"""
    name_cache = json.loads((SNAP_DIR / "raw-name-cache.json").read_text())
    entries = []
    for p in sorted((ROOT / "data" / "plugins").glob("*.yml")):
        d = delta.census.parse_yml(p)
        if d and d.get("url"):
            d["repo"] = delta.repo_key(d["url"])
            entries.append(d)

    repo_npm = {}
    repo_urls = {}
    for e in entries:
        npm = name_cache.get(e["url"])
        if e["repo"]:
            repo_urls.setdefault(e["repo"], []).append(e["url"])
        if npm and e["repo"] and e["repo"] not in repo_npm:
            repo_npm[e["repo"]] = npm

    def top_from(path, n):
        try:
            data = json.loads(path.read_text())
        except OSError:
            return []
        rows = []
        for url, meta in data.items():
            repo = delta.repo_key(url)
            if not repo:
                continue
            val = meta.get("stars") if "stars" in meta else meta.get("downloads")
            if val:
                rows.append((repo, val))
        rows.sort(key=lambda kv: -kv[1])
        seen, out = set(), []
        for repo, val in rows:
            if repo in seen:
                continue
            seen.add(repo)
            out.append(repo)
            if len(out) >= n:
                break
        return out

    return (entries, repo_npm, repo_urls,
            top_from(ROOT / "data" / "stars.json", 80),
            top_from(ROOT / "data" / "downloads.json", 40))


def resolve_pkg(repo, urls):
    """从 package.json 回源 npm 名。只对卡片仓库做,控制配额。"""
    paths = []
    for url in urls:
        m = re.search(r"/tree/[^/]+/(.+)$", url)
        if m:
            paths.append(m.group(1).strip("/") + "/package.json")
    paths.append("package.json")
    seen = set()
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        data, _ = gh_json(f"repos/{repo}/contents/{urllib.parse.quote(path, safe='/')}")
        if not data or not data.get("content"):
            continue
        try:
            payload = json.loads(base64.b64decode(data["content"]).decode("utf-8"))
        except Exception:  # noqa: BLE001 - 包清单坏掉就换下一个候选
            continue
        name = payload.get("name")
        if isinstance(name, str) and name.strip():
            return name.strip()
    return None


def gh_json(path, retries=2):
    last = ""
    for attempt in range(retries + 1):
        proc = subprocess.run(
            ["gh", "api", path],
            cwd=ROOT, capture_output=True, text=True, timeout=60,
        )
        if proc.returncode == 0:
            try:
                return json.loads(proc.stdout), None
            except json.JSONDecodeError as exc:
                last = f"JSONDecodeError: {exc}"
        else:
            last = (proc.stderr or proc.stdout or "").strip()[:300]
        if attempt < retries:
            time.sleep(1.5 * (attempt + 1))
    return None, last


def npm_json(pkg):
    url = ("https://api.npmjs.org/downloads/point/last-month/"
           + urllib.parse.quote(pkg, safe=""))
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None, "unpublished"
        return None, f"HTTPError: HTTP Error {exc.code}: {exc.reason}"
    except Exception as exc:  # noqa: BLE001 - 单包失败必须继续
        return None, f"{type(exc).__name__}: {exc}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--asof", default=datetime.now(timezone.utc).date().isoformat())
    ap.add_argument("--out", default=None)
    ap.add_argument("--max-repos", type=int, default=180)
    ap.add_argument("--max-pkgs", type=int, default=180)
    ap.add_argument("--skip-npm", action="store_true")
    ap.add_argument("--no-resolve", action="store_true",
                    help="不从 package.json 回源 npm 名(省配额)")
    args = ap.parse_args()

    entries, repo_npm, repo_urls, stars_top, downloads_top = load_index()
    cards = []
    for p in sorted(ROOT.glob(CARD_GLOB)):
        repo = repo_from_card(p)
        if repo:
            cards.append(repo)

    repos = []
    seen = set()
    for repo in cards + stars_top + downloads_top:
        if repo and repo not in seen:
            seen.add(repo)
            repos.append(repo)
    repos = repos[: args.max_repos]

    errors = []
    repo_rows = {}
    for i, repo in enumerate(repos, 1):
        data, err = gh_json(f"repos/{repo}")
        if data is None:
            errors.append({"kind": "repo", "id": repo, "error": err})
            continue
        repo_rows[repo] = {
            "full_name": data.get("full_name"),
            "stars": data.get("stargazers_count"),
            "pushed_at": data.get("pushed_at"),
            "archived": data.get("archived"),
            "default_branch": data.get("default_branch"),
            "html_url": data.get("html_url"),
        }
        if i % 20 == 0:
            print(f"  repo {i}/{len(repos)} ...", file=sys.stderr)

    pkgs = []
    if not args.skip_npm:
        if not args.no_resolve:
            for repo in cards:
                if repo in repo_npm:
                    continue
                pkg = resolve_pkg(repo, repo_urls.get(repo, []))
                if pkg:
                    repo_npm[repo] = pkg
        seen_pkg = set()
        for repo in repos:
            pkg = repo_npm.get(repo)
            if pkg and pkg not in seen_pkg:
                seen_pkg.add(pkg)
                pkgs.append(pkg)
        pkgs = pkgs[: args.max_pkgs]

    pkg_rows = {}
    unpublished = []
    for i, pkg in enumerate(pkgs, 1):
        data, err = npm_json(pkg)
        if data is None:
            if err == "unpublished":
                unpublished.append(pkg)
            else:
                errors.append({"kind": "npm", "id": pkg, "error": err})
            continue
        pkg_rows[pkg] = {
            "downloads": data.get("downloads"),
            "start": data.get("start"),
            "end": data.get("end"),
        }
        if i % 20 == 0:
            print(f"  npm {i}/{len(pkgs)} ...", file=sys.stderr)

    out = Path(args.out) if args.out else SNAP_DIR / f"live-{args.asof}.json"
    payload = {
        "asof": args.asof,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "method": ("gh api repos/{repo}; api.npmjs.org downloads/point/last-month/{pkg}; "
                   "repo set = cards + top80 stars sidecar + top40 downloads sidecar"),
        "repos": repo_rows,
        "packages": pkg_rows,
        "repo_packages": {repo: repo_npm[repo] for repo in repos if repo in repo_npm},
        "coverage": {
            "repos": f"{len(repo_rows)}/{len(repos)}",
            "packages": f"{len(pkg_rows)}/{len(pkgs)}",
            "unpublished": unpublished,
            "errors": errors,
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(out)
    print(f"wrote {out}  repos {len(repo_rows)}/{len(repos)}  "
          f"packages {len(pkg_rows)}/{len(pkgs)}  errors {len(errors)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
