#!/usr/bin/env python3
"""delta.py:两期名单对比,产出 `_view/` 呈现层的原料。

与 census.py(全量普查,档案层)互补:delta 只回答「两期之间发生了什么」,
输出三节——① 冒出来的(新 owner/新苗子)、② 哪里热闹(类目热度变化)、
③ 锚候选(热闹领域的头部条目)。全部数字可由本脚本复现,供 _view/ 引用。

用法:python3 _digested/ecosystem/delta.py <old-ref> <new-ref>
    例:python3 _digested/ecosystem/delta.py efe602e7b 29b3ed46e
依赖:仅标准库;条目解析复用 census.parse_yml。
"""
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "census", Path(__file__).resolve().parent / "census.py")
census = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(census)

ROOT = Path(__file__).resolve().parents[2]
# 热度锚的最低门槛:类目本期新增少于这个数不认为是「热闹」。
HEAT_NEW_MIN = 40

# ③b 的锚清单:token -> 锚自身仓库(owner/repo,小写)。
# 自排除必须按仓库身份精确匹配;不能用「URL 里含 token」,否则
# `dsh-hindsight-*` / `dsh-openviking-*` 这类同名衍生会被误当成锚自身。
ANCHORS = {
    "hindsight": "vectorize-io/hindsight",
    "openviking": "volcengine/openviking",
    "ouroboros": "q00/ouroboros",
    "mirage": "strukto-ai/mirage",
    "modlens": "liustack/modlens",
    "better-sidebar": "omdsh-dev/dsh-better-sidebar",
    "tongflow": "tong-io/tongflow",
    "engramory": "tinqiao-oss/engramory",
    "misakanet": "ikalus1988/misakanet",
    "mnemon": "omdsh-dev/dsh-mnemon",
    "memento": "perrylink/dsh-memento",
}


def repo_key(url):
    """把 GitHub URL 或裸 owner/repo 归一成 owner/repo(小写)。

    剥掉 #sub、/tree/... 与 .git;非 GitHub URL 返回 None。
    """
    s = str(url or "").strip()
    m = re.search(r"github\.com[/:]([^/\s#?]+)/([^/\s#?]+)", s, re.I)
    if m:
        owner, repo = m.group(1), m.group(2)
    elif "://" not in s:
        bare = s.split("#", 1)[0].split("/tree/", 1)[0].strip("/")
        parts = [p for p in bare.split("/") if p]
        if len(parts) < 2:
            return None
        owner, repo = parts[0], parts[1]
    else:
        return None
    repo = re.sub(r"\.git$", "", repo, flags=re.I)
    return f"{owner}/{repo}".lower()


def load_tree(ref):
    """把某个 ref 的 data/plugins 解到临时目录并解析(与工作区无关,可对比任意两期)。"""
    tmp = Path(tempfile.mkdtemp(prefix="delta_"))
    subprocess.run(["git", "-C", str(ROOT), "archive", ref, "data/plugins"],
                   stdout=open(tmp / "a.tar", "wb"), check=True)
    subprocess.run(["tar", "-xf", str(tmp / "a.tar"), "-C", str(tmp)], check=True)
    entries = []
    for p in sorted((tmp / "data" / "plugins").glob("*.yml")):
        d = census.parse_yml(p)
        if d and d.get("url"):
            d["file"] = p.name
            d["owner"] = p.name.split("__")[0]
            d["repo"] = repo_key(d.get("url"))
            entries.append(d)
    return entries


def cat_stats(entries, label):
    by = defaultdict(list)
    for e in entries:
        by[e.get("category", "?")].append(e)
    owners = {c: len({e["owner"] for e in es}) for c, es in by.items()}
    single = {c: sum(1 for _, n in Counter(e["owner"] for e in es).items() if n == 1)
              for c, es in by.items()}
    print(f"\n── 类目热度({label},共 {len(entries)} 条)──")
    print(f"{'类目':<10}{'条目':>6}{'占比':>8}{'owners':>8}{'单件占比':>9}")
    for c, es in sorted(by.items(), key=lambda kv: -len(kv[1])):
        print(f"{c:<10}{len(es):>6}{len(es)*100/len(entries):>7.1f}%{owners[c]:>8}"
              f"{single[c]*100/max(owners[c],1):>8.0f}%")
    return by


def classify_hits(entries, token, anchor_repo):
    """按仓库身份把命中分成 self / name / mention 三层。

    - self:仓库 == 锚自身(monorepo 的多个子条目都算 self);
    - name:第三方仓库名里带 token(多为 fork / 同名衍生,是最强的候选);
    - mention:只有 name 字段或描述里提到 token。

    注意:这三层只是**候选**,不是采纳。同名可能是无关项目,描述提及也可能
    只是"类似 X"或"清理 X 的缓存"。最终采纳数由卡片逐条判定。
    """
    token = token.lower()
    anchor_repo = (anchor_repo or "").lower()
    tiers = {"self": [], "name": [], "mention": []}
    for e in entries:
        text = " ".join([
            str(e.get("name", "")),
            str(e.get("description.en") or ""),
            str(e.get("description.zh") or ""),
        ]).lower()
        if token not in text:
            continue
        repo = e.get("repo") or repo_key(e.get("url"))
        if repo == anchor_repo:
            tiers["self"].append(e)
        elif repo and token in repo.split("/")[-1]:
            tiers["name"].append(e)
        else:
            tiers["mention"].append(e)
    return tiers


def imitation_signals(entries, anchors=None):
    """③b 模仿信号:按精确仓库身份排除锚自身,再分同名/描述两层输出候选。"""
    anchors = anchors or ANCHORS
    print("\n── ③b 模仿信号(按仓库身份排除锚自身;候选分层,采纳以卡内判定为准)──")
    print(f"  {'token':<16}{'锚自身':>6}{'同名候选':>9}{'描述候选':>9}{'第三方候选':>10}")
    for token, anchor_repo in anchors.items():
        tiers = classify_hits(entries, token, anchor_repo)
        self_n, name_n, mention_n = len(tiers["self"]), len(tiers["name"]), len(tiers["mention"])
        print(f"  {token:<16}{self_n:>6}{name_n:>9}{mention_n:>9}{name_n + mention_n:>10}")
        for label, rows in (("同名", tiers["name"]), ("描述", tiers["mention"])):
            for e in rows[:3]:
                print(f"      {label}  {e.get('name', e['file'])}  [{e.get('category')}]")
    print("  注:同名/描述命中是候选;是否算采纳以卡内逐条判定为准"
          "(如 auto-memory、message-edit 都有同名无关条目)。")


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    old_ref, new_ref = sys.argv[1], sys.argv[2]
    old = load_tree(old_ref)
    new = load_tree(new_ref)
    print(f"# delta:{old_ref}({len(old)} 条)→ {new_ref}({len(new)} 条)"
          f",净 {len(new) - len(old):+d}")

    old_files = {e["file"] for e in old}
    new_files = {e["file"] for e in new}
    old_urls = {e["url"] for e in old}
    new_urls = {e["url"] for e in new}
    # 文件级口径:新文件名=收录,消失=下架。注意 git 的改名检测(R)按内容相似度,
    # 多半是 owner 迁移——URL 已换,语义上确实是一次下架 + 一次上架,所以两侧都算。
    added = [e for e in new if e["file"] not in old_files]
    removed = [e for e in old if e["file"] not in new_files]
    print(f"新增 {len(added)} / 删除 {len(removed)} / 净 {len(new) - len(old):+d}"
          f"(文件级口径;git 会把少数同名仓换 owner 的条目显示为改名,故与 diff 的 A/D 数略有差)")

    new_by = cat_stats(new, "本期")
    old_by = cat_stats(old, "上期")

    print("\n── ② 热度变化(按本期新增排序)──")
    print(f"{'类目':<10}{'上期':>6}{'本期':>6}{'新增':>6}{'删除':>6}{'占比漂移':>9}")
    heat = []
    for c, es in sorted(new_by.items(), key=lambda kv: -len(kv[1])):
        a = len(added) and sum(1 for e in added if e.get("category") == c)
        d = sum(1 for e in removed if e.get("category") == c)
        shift = len(es) * 100 / len(new) - len(old_by.get(c, [])) * 100 / max(len(old), 1)
        mark = " ←热闹" if a >= HEAT_NEW_MIN else ""
        print(f"{c:<10}{len(old_by.get(c, [])):>6}{len(es):>6}{a:>6}{d:>6}{shift:>+8.1f}pp{mark}")
        heat.append((c, a, d, len(es)))

    print("\n── ① 新 owner(本期新增条目 ≥2 的全新作者)──")
    old_owners = {e["owner"] for e in old}
    new_owner_added = Counter(e["owner"] for e in added)
    emerging = [(o, n) for o, n in new_owner_added.most_common(40)
                if o not in old_owners and n >= 2]
    for o, n in emerging[:20]:
        cats = Counter(e.get("category") for e in added if e["owner"] == o).most_common(3)
        print(f"  {o:<28}{n:>3} 条  主要:{', '.join(f'{c}×{k}' for c, k in cats)}")
    print(f"  (共 {len(emerging)} 个新 owner 达到 ≥2 条;全部新 owner "
          f"{len(set(e['owner'] for e in added) - old_owners)} 个)")

    print("\n── ③ 锚候选(热闹类目的头部条目,按 stars 边车 join;⚠ 边车是历史采样)──")
    try:
        stars = json.loads((ROOT / "data" / "stars.json").read_text())
    except OSError:
        stars = {}
    star_of = {u: v.get("stars") for u, v in stars.items()}
    for c, a, d, total in heat:
        if a < HEAT_NEW_MIN:
            continue
        es = [e for e in new_by[c] if star_of.get(e.get("url"))]
        es.sort(key=lambda e: -(star_of[e["url"]] or 0))
        new_es = [e for e in es if e["file"] not in old_files]
        print(f"\n  [{c}] 本期 {total} 条(新增 {a}):")
        print("    存量头部:")
        for e in es[:5]:
            print(f"      {star_of[e['url']]:>7}  {e.get('name', e['file'])}")
        print("    新增头部(本期冒出来的):")
        for e in new_es[:5]:
            print(f"      {star_of[e['url']]:>7}  {e.get('name', e['file'])}")

    imitation_signals(new)

    print("\n── ①b 标签增长(34 组,按命中增量)──")
    old_tags = Counter(t for e in old for t in census.tag_of(
        (e.get("description.en", "") + " " + e.get("description.zh", "")).lower()))
    new_tags = Counter(t for e in new for t in census.tag_of(
        (e.get("description.en", "") + " " + e.get("description.zh", "")).lower()))
    for t, n in (new_tags - old_tags).most_common(15):
        print(f"  {t:<12}{old_tags.get(t, 0):>5} → {new_tags[t]:>5}(+{n})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
