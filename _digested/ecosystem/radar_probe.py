#!/usr/bin/env python3
"""radar_probe.py — 分层热度雷达(Tier 2 纯 GraphQL 批量星标 + Tier 3 过线补 npm)。

为什么独立于 fresh_probe.py:
  fresh_probe.py 全量回源 package.json 会撞穿 GitHub REST 5000/hr 限额。
  本脚本把采集分成两层:
    - Tier 2:纯 GitHub GraphQL(80 仓/批)批量查 stargazerCount / forkCount /
      createdAt / pushedAt / isArchived / isFork;扫一期新增(~1300 仓)仅 ~17 次请求,
      扫全库(~12000 仓)仅 ~150 次请求,不消耗 REST contents 配额。
    - Tier 3:仅对星标 >= 阈值(默认 30)的新增候选仓回源 package.json + npm 月下载。

用法:
  # 扫两期之间新增仓(Tier 2 + Tier 3)
  python3 _digested/ecosystem/radar_probe.py --delta 29b3ed46e 8f1a1800e --asof 2026-11-27
  # 扫全库唯一仓的实时星标(仅 Tier 2,产出 _snapshots/stars-<asof>.json)
  python3 _digested/ecosystem/radar_probe.py --full --asof 2026-11-27
"""
import argparse
import importlib.util
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SNAP_DIR = HERE / "_snapshots"
GH_BATCH = 80
DSH_BIRTH = "2026-08-13"
VALID_IDENT = re.compile(r"^[A-Za-z0-9_.-]+$")

_spec_d = importlib.util.spec_from_file_location("delta", HERE / "delta.py")
delta = importlib.util.module_from_spec(_spec_d)
_spec_d.loader.exec_module(delta)

_spec_l = importlib.util.spec_from_file_location("live_probe", HERE / "live_probe.py")
live_probe = importlib.util.module_from_spec(_spec_l)
_spec_l.loader.exec_module(live_probe)


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def split_valid_repo(repo_key):
    """验证 owner/repo 标识符安全性,防止 GraphQL 注入。"""
    if not repo_key or "/" not in repo_key:
        return None
    parts = repo_key.split("/")
    if len(parts) != 2:
        return None
    owner, name = parts
    if not (VALID_IDENT.match(owner) and VALID_IDENT.match(name)):
        return None
    return owner, name


def build_graphql_query(repos):
    """为一批 (alias_idx, owner, name) 构造 GraphQL 查询字符串。"""
    parts = []
    for idx, owner, name in repos:
        parts.append(
            f'r{idx}: repository(owner:"{owner}",name:"{name}")'
            f'{{nameWithOwner stargazerCount forkCount createdAt pushedAt isArchived isFork}}'
        )
    return "query{" + " ".join(parts) + "}"


def classify_origin(meta, has_subpath=False):
    """启发式区分「主项目/预存仓背书」与「DSH 生态原生新仓」。

    注意:这是启发式信号,不是源码审计结论。
    """
    created = (meta.get("created_at") or "")[:10]
    if created and created < DSH_BIRTH:
        return "pre-dsh-host"
    if has_subpath:
        return "monorepo-subpath"
    if meta.get("is_fork"):
        return "github-fork"
    return "dsh-native"


def _run_graphql_batch(batch, retries=2):
    q = build_graphql_query(batch)
    last_err = ""
    for attempt in range(retries + 1):
        try:
            proc = subprocess.run(
                ["gh", "api", "graphql", "-f", f"query={q}"],
                cwd=ROOT, capture_output=True, text=True, timeout=75,
            )
            if proc.stdout.strip():
                body = json.loads(proc.stdout)
                if isinstance(body, dict) and "data" in body and body["data"] is not None:
                    return body["data"], None
                last_err = (proc.stderr or proc.stdout)[:300]
            else:
                last_err = (proc.stderr or f"rc={proc.returncode}")[:300]
        except (subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
            last_err = f"{type(exc).__name__}: {exc}"
        if attempt < retries:
            time.sleep(2.0 * (attempt + 1))
    return None, last_err


def fetch_repos_graphql(repo_keys, batch_size=GH_BATCH):
    """批量 GraphQL 获取仓库星标与活跃度。返回 (repos_dict, errors_list)。"""
    valid = []
    errors = []
    for rk in sorted(set(repo_keys)):
        sp = split_valid_repo(rk)
        if not sp:
            errors.append({"kind": "repo", "id": str(rk), "error": "invalid repo key"})
            continue
        valid.append((rk, sp[0], sp[1]))

    out = {}
    total = len(valid)
    for start in range(0, total, batch_size):
        chunk = valid[start:start + batch_size]
        indexed = [(j, o, n) for j, (_, o, n) in enumerate(chunk)]
        data, err = _run_graphql_batch(indexed)
        if data is None and len(chunk) > 10:
            # 批次整体失败时拆半重试,避免单条畸形仓打翻整批
            mid = len(chunk) // 2
            merged = {}
            for sub in (chunk[:mid], chunk[mid:]):
                sub_indexed = [(j, o, n) for j, (_, o, n) in enumerate(sub)]
                sub_data, sub_err = _run_graphql_batch(sub_indexed)
                if sub_data is None:
                    for rk, _, _ in sub:
                        errors.append({"kind": "repo", "id": rk, "error": sub_err})
                else:
                    for j, (rk, _, _) in enumerate(sub):
                        merged[rk] = sub_data.get(f"r{j}")
            for rk, v in merged.items():
                if v:
                    out[rk] = _normalize_gql_node(v)
                else:
                    errors.append({"kind": "repo", "id": rk, "error": "not found or inaccessible"})
        elif data is None:
            for rk, _, _ in chunk:
                errors.append({"kind": "repo", "id": rk, "error": err})
        else:
            for j, (rk, _, _) in enumerate(chunk):
                v = data.get(f"r{j}")
                if v:
                    out[rk] = _normalize_gql_node(v)
                else:
                    errors.append({"kind": "repo", "id": rk, "error": "not found or inaccessible"})
        done = min(start + batch_size, total)
        if (start // batch_size) % 5 == 0 or done == total:
            log(f"  graphql {done}/{total} (ok={len(out)}, err={len(errors)})")
    return out, errors


def _normalize_gql_node(v):
    return {
        "full_name": v.get("nameWithOwner"),
        "stars": v.get("stargazerCount"),
        "forks": v.get("forkCount"),
        "created_at": v.get("createdAt"),
        "pushed_at": v.get("pushedAt"),
        "archived": v.get("isArchived"),
        "is_fork": v.get("isFork"),
    }


def load_workspace_entries():
    entries = []
    for p in sorted((ROOT / "data" / "plugins").glob("*.yml")):
        d = delta.census.parse_yml(p)
        if d and d.get("url"):
            d["file"] = p.name
            d["owner"] = p.name.split("__")[0]
            d["repo"] = delta.repo_key(d["url"])
            entries.append(d)
    return entries


def write_json_atomic(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def run_delta(old_ref, new_ref, asof, star_threshold, out_path):
    old = delta.load_tree(old_ref)
    new = delta.load_tree(new_ref)
    old_files = {e["file"] for e in old}
    added = [e for e in new if e["file"] not in old_files]

    repo_entries = {}
    for e in added:
        rk = e.get("repo")
        if rk:
            repo_entries.setdefault(rk, []).append(e)

    log(f"delta {old_ref}..{new_ref}: added entries={len(added)}, unique repos={len(repo_entries)}")
    repos_data, errors = fetch_repos_graphql(repo_entries.keys())

    # Tier 3: 对星标 >= star_threshold 的新仓补查 npm 月下载
    name_cache_path = SNAP_DIR / "raw-name-cache.json"
    name_cache = json.loads(name_cache_path.read_text(encoding="utf-8")) if name_cache_path.exists() else {}
    hot_repos = [
        rk for rk, meta in sorted(repos_data.items(), key=lambda kv: -(kv[1].get("stars") or 0))
        if (meta.get("stars") or 0) >= star_threshold
    ]
    log(f"Tier 3: {len(hot_repos)} repos >= {star_threshold}★, resolving npm packages...")
    repo_packages = {}
    packages = {}
    unpublished = []
    for rk in hot_repos:
        urls = [e["url"] for e in repo_entries[rk]]
        pkg = None
        for u in urls:
            if name_cache.get(u):
                pkg = name_cache[u]
                break
        if not pkg:
            pkg = live_probe.resolve_pkg(rk, urls)
        if not pkg:
            continue
        repo_packages[rk] = pkg
        if pkg in packages or pkg in unpublished:
            continue
        dl, err = live_probe.npm_json(pkg)
        if dl is None:
            if err == "unpublished":
                unpublished.append(pkg)
            else:
                errors.append({"kind": "npm", "id": pkg, "error": err})
        else:
            packages[pkg] = {
                "downloads": dl.get("downloads"),
                "start": dl.get("start"),
                "end": dl.get("end"),
            }

    ranked = []
    for rk, meta in sorted(repos_data.items(), key=lambda kv: -(kv[1].get("stars") or 0)):
        es = repo_entries[rk]
        has_subpath = any(("#" in e["url"] or "/tree/" in e["url"]) for e in es)
        origin = classify_origin(meta, has_subpath=has_subpath)
        pkg = repo_packages.get(rk)
        dl = packages.get(pkg, {}).get("downloads") if pkg else None
        ranked.append({
            "repo": rk,
            "full_name": meta.get("full_name") or rk,
            "stars": meta.get("stars"),
            "forks": meta.get("forks"),
            "created_at": meta.get("created_at"),
            "pushed_at": meta.get("pushed_at"),
            "archived": meta.get("archived"),
            "is_fork": meta.get("is_fork"),
            "origin": origin,
            "categories": sorted({e.get("category", "?") for e in es}),
            "entry_count": len(es),
            "sample_name": es[0].get("name", es[0]["file"]),
            "npm": pkg,
            "downloads_last_month": dl,
        })

    payload = {
        "asof": asof,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "mode": "delta",
        "range": {"from": old_ref, "to": new_ref},
        "star_threshold_npm": star_threshold,
        "method": (
            "Tier 2: gh api graphql (80 repos/batch) on all unique repos added in from..to; "
            f"Tier 3: package.json + npm last-month downloads for repos >= {star_threshold} stars"
        ),
        "coverage": {
            "added_entries": len(added),
            "repos": f"{len(repos_data)}/{len(repo_entries)}",
            "hot_repos_ge_threshold": len(hot_repos),
            "packages_published": len(packages),
            "unpublished": unpublished,
            "errors": errors,
        },
        "ranked": ranked,
        "repos": repos_data,
        "repo_packages": repo_packages,
        "packages": packages,
    }
    out = Path(out_path) if out_path else SNAP_DIR / f"radar-{old_ref}-to-{new_ref}-{asof}.json"
    write_json_atomic(out, payload)
    print(f"wrote {out}  repos {len(repos_data)}/{len(repo_entries)}  "
          f"hot(>={star_threshold}★) {len(hot_repos)}  npm {len(packages)}  errors {len(errors)}")
    return 0


def run_full(asof, out_path):
    entries = load_workspace_entries()
    repo_entries = {}
    for e in entries:
        rk = e.get("repo")
        if rk:
            repo_entries.setdefault(rk, []).append(e)

    log(f"full scan: entries={len(entries)}, unique repos={len(repo_entries)}")
    repos_data, errors = fetch_repos_graphql(repo_entries.keys())

    payload = {
        "asof": asof,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "mode": "full-stars",
        "method": "Tier 2 full catalog: gh api graphql (80 repos/batch) across all unique data/plugins/*.yml repos",
        "coverage": {
            "entries": len(entries),
            "repos": f"{len(repos_data)}/{len(repo_entries)}",
            "errors_count": len(errors),
            "errors_sample": errors[:30],
        },
        "repos": repos_data,
    }
    out = Path(out_path) if out_path else SNAP_DIR / f"stars-{asof}.json"
    write_json_atomic(out, payload)
    print(f"wrote {out}  entries {len(entries)}  repos {len(repos_data)}/{len(repo_entries)}  errors {len(errors)}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="分层热度雷达(GraphQL 星标 + 高星补 npm)")
    ap.add_argument("--delta", nargs=2, metavar=("OLD_REF", "NEW_REF"),
                    help="扫两期之间新增仓库(Tier 2 + Tier 3)")
    ap.add_argument("--full", action="store_true",
                    help="扫全库唯一仓库实时星标(仅 Tier 2)")
    ap.add_argument("--asof", default=datetime.now(timezone.utc).date().isoformat())
    ap.add_argument("--star-threshold", type=int, default=30,
                    help="Tier 3 补查 npm 的最低星标门槛(默认 30)")
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)

    if bool(args.delta) == bool(args.full):
        ap.error("请二选一指定 --delta <old> <new> 或 --full")
    if args.delta:
        return run_delta(args.delta[0], args.delta[1], args.asof, args.star_threshold, args.out)
    return run_full(args.asof, args.out)


if __name__ == "__main__":
    sys.exit(main())
