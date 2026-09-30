#!/usr/bin/env python3
"""fresh_probe.py — 自采新鲜成熟度信号,不依赖上游 catalog 的 npm 发布节奏。

背景:仓库边车 data/downloads.json 是冻结快照;新鲜下载量只在 Actions cache 与
dsh-plugin-catalog npm 包里,而该包的夜间发布会停(2026-09-08 后即停,见
04-value-trend.md 方法要点)。本脚本绕开它,直接从两个公开源头采:

  1. npm registry downloads API(无鉴权):
     - 非 scoped 包名走 bulk 端点(100 个/批)
     - scoped 包名 bulk 不支持,逐个并发取
  2. GitHub GraphQL(经 gh CLI 认证,需 gh auth login):
     - stargazerCount / pushedAt / isArchived,80 个 alias/批

npm 包名解析优先级:上一份本地快照 > catalog 快照(_snapshots/catalog-*.json)
> api.github.com contents API 读 repo 的 package.json "name" 字段
(raw.githubusercontent.com 在部分网络不可达,故走 contents API)。

用法:
  python3 _digested/ecosystem/fresh_probe.py            # 全量采集 + 增量报告
  python3 _digested/ecosystem/fresh_probe.py --quiet    # 只采集不打印报告

快照落在 _snapshots/snap-<UTC 日期>.json;与历史快照(含 catalog 转储)的增量
对比在报告里给出。标准库实现,与 census.py 同风格。
"""
import concurrent.futures as cf
import http.client
import json
import re
import socket
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP_DIR = HERE / "_snapshots"
GH_BATCH = 80
NPM_BULK = 100
WORKERS = 12


def log(msg):
    print(msg, file=sys.stderr, flush=True)


# ---------- npm 包名解析 ----------

def repo_of(url):
    """条目 url → 'owner/repo'(剥掉 #fragment 与 /tree/<branch>/<sub> 子路径)。"""
    base = url.split("#")[0].removeprefix("https://github.com/").rstrip("/")
    m = re.search(r"/tree/[^/]+/(.*)$", base)
    if m:
        base = base[:m.start()]
    return base.rstrip("/")


def subpath_of(url):
    """条目 url 的子路径(monorepo 包);无则 ''。"""
    if "#" in url:
        return url.split("#", 1)[1].strip("/")
    m = re.search(r"/tree/[^/]+/(.+)$", url.split("#")[0])
    return m.group(1).strip("/") if m else ""


def _gh_token():
    try:
        return subprocess.run(["gh", "auth", "token"], capture_output=True,
                              text=True, timeout=10).stdout.strip()
    except subprocess.TimeoutExpired:
        return ""


def _gh_headers():
    tok = _gh_token()
    h = {"Accept": "application/vnd.github.raw", "User-Agent": "dsh-digest-probe"}
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


class ProbeUnavailable(Exception):
    """一条回源在重试后仍然失败:这是「本轮未知」,不是「没有」。"""


def raw_npm_name(url, attempts=3):
    """经 api.github.com contents API 读 repo(或子路径)package.json 的 name。

    raw.githubusercontent.com 在部分网络不可达;api.github.com(gh 同款通道)
    可达。monorepo 条目取子路径下的 package.json。

    0002 修复:原实现只捕获 URLError,而连接被对端掐断抛的是
    http.client.RemoteDisconnected(OSError 子类,不是 URLError)——实测 942 条
    回源的长尾里它直接掀掉整轮采集。现在瞬时错误重试,仍失败则抛
    ProbeUnavailable,由调用方按「未知」处理:不写缓存(下次重试)、更不写
    None(那会把一次网络抖动固化成「未发布」,违反本目录「未知 ≠ 死亡」)。
    """
    path = (subpath_of(url) + "/" if subpath_of(url) else "") + "package.json"
    u = f"https://api.github.com/repos/{repo_of(url)}/contents/{path}?ref=HEAD"
    last = None
    for attempt in range(1, attempts + 1):
        req = urllib.request.Request(u, headers=_gh_headers())
        try:
            with urllib.request.urlopen(req, timeout=12) as r:
                text = r.read().decode("utf-8", "replace")
            return json.loads(text).get("name") or None
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None  # 该路径没有 package.json,这是事实不是失败
            last = e
        except (OSError, ValueError) as e:  # RemoteDisconnected/超时/坏 JSON
            last = e
        if attempt < attempts:
            time.sleep(1.5 * attempt)
    raise ProbeUnavailable(f"{type(last).__name__}: {last}")


def _registry_repo_owner(name):
    """registry.npmjs.org 元数据里的 repository 指向的 'owner'(小写)或 None。"""
    try:
        meta = _get_json(f"https://registry.npmjs.org/{urllib.parse.quote(name, safe='')}", timeout=30, attempts=3)
        if not meta:
            return None  # 404:包不存在(未发布)
        repo = meta.get("repository")
        if isinstance(repo, str):
            repo = {"url": repo}
        u = (repo or {}).get("url") or ""
        m = re.search(r"github\.com[:/]([^/]+)", u, re.I)
        return m.group(1).lower() if m else None
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
            json.JSONDecodeError, ValueError, http.client.HTTPException):
        return None


def validate_names(names, to_check):
    """校验回源解析出的包名,防『schedule』这类撞名把别人的下载量记到我们头上。

    通过条件(任一):
      a) registry 元数据 repository 指向同一 owner;
      b) 包名本身含 'dsh'(插件生态 85% 的命名习惯,且名字出自 repo 自己的
         package.json,撞上一个恰好含 dsh 的他人包概率极低)。
    元数据缺失且名字不含 dsh 的 → 丢弃。
    返回 {url: name 或 None}。
    """
    by_name = {}
    for u in to_check:
        n = names.get(u)
        if n:
            by_name.setdefault(n, []).append(u)
    owners = {u: repo_of(u).split("/")[0].lower() for u in to_check}
    ok_name = {}
    budget_end = time.monotonic() + VALIDATE_BUDGET_S
    skipped = 0
    # 不用 with:预算用尽时要 shutdown(wait=False) 把队列里剩下的丢掉,
    # 而 with 的 __exit__ 是 wait=True——它会把一千多个待办全跑完,等于没预算。
    ex = cf.ThreadPoolExecutor(VALIDATE_WORKERS)
    try:
        # 期限必须套在 worker 内部:套在消费端(f.result)没用——as_completed
        # 要等某个 future 完成才会让出,若 12 个 worker 全卡在 DNS 解析上,
        # 消费循环永远不执行,预算也就永远不触发(0002 实测卡死 40 分钟)。
        def checked(n):
            return _call_with_deadline(lambda: _registry_repo_owner(n), VALIDATE_DEADLINE_S)

        futs = {ex.submit(checked, n): n for n in by_name}
        done = 0
        for f in cf.as_completed(futs):
            n = futs[f]
            done += 1
            if done % 200 == 0:
                log(f"  校验 {done}/{len(futs)}")
            if time.monotonic() > budget_end:
                # 预算用尽:不猜具体归属,但也不无条件丢弃——退回「元数据不可用」
                # 那一条分支(名字含 dsh 或按 owner 作用域命名则通过)。校验每轮
                # 重跑,所以下轮会自动补上;宁可这轮保守,也不要空转一小时。
                skipped += 1
                meta_owner = None
            else:
                try:
                    meta_owner = f.result()
                except Exception as exc:  # 单条校验失败按「无法确认」处理(0002)
                    log(f"⚠ 校验请求失败({n}):{type(exc).__name__},按无法确认归属处理")
                    meta_owner = None
            urls = by_name[n]
            good = False
            for u in urls:
                o = owners[u]
                if meta_owner == o or n.lower().startswith(f"@{o}/"):
                    good = True
                elif "dsh" in n.lower() and meta_owner is None:
                    good = True  # 元数据没写 repository,但名字足够特异
                ok_name[u] = n if good else ok_name.get(u)
    finally:
        ex.shutdown(wait=False, cancel_futures=True)
    if skipped:
        log(f"⚠ 包名校验预算 {VALIDATE_BUDGET_S}s 用尽,剩余 {skipped} 个名字按「无法确认」处理"
            f"(下一轮自动重试;本轮归因数因此偏低)")
    dropped = [u for u in to_check if not ok_name.get(u)]
    if dropped:
        log(f"⚠ 包名校验丢弃 {len(dropped)} 条(撞名或无法确认归属),示例:"
            f"{[u.split('github.com/')[1] for u in dropped[:3]]}")
    return ok_name


def resolve_npm_names(entries, prev_map, catalog_map):
    """返回 ({url: npm_name 或 None}, raw_resolved_urls)。

    prev/catalog 命中的名字视为已验证(上游 probe 亲自解析过),不回源;
    contents API 回源解析出的名字必须过 validate_names 一致性校验。
    回源结果持久化在 _snapshots/raw-name-cache.json(含 null),避免重复烧
    GitHub contents API 配额;校验每轮重跑(只烧 npmjs,配额无虞)。
    """
    names, raw_sourced, need_raw, cached, trusted = {}, [], [], 0, 0
    cache_path = SNAP_DIR / "raw-name-cache.json"
    cache = load_json(cache_path) or {}
    for e in entries:
        u = e["url"]
        n = prev_map.get(u) or catalog_map.get(u)
        if n:
            names[u] = n
            trusted += 1
        else:
            raw_sourced.append(u)  # 缓存或回源而来,一律过校验
            if u in cache:
                names[u] = cache[u]
                cached += 1
            else:
                need_raw.append(u)
    log(f"npm 包名:快照/目录命中 {trusted},本地缓存 {cached},需回源 {len(need_raw)}")
    if need_raw:
        SNAP_DIR.mkdir(exist_ok=True)
        failed = []
        with cf.ThreadPoolExecutor(WORKERS) as ex:
            # 同 validate_names:期限套在 worker 内部,否则 as_completed 会被
            # 卡在 DNS 上的 worker 永久挡住
            futs = {ex.submit(lambda u=u: _call_with_deadline(lambda: raw_npm_name(u))): u
                    for u in need_raw}
            done = 0
            for f in cf.as_completed(futs):
                u = futs[f]
                try:
                    name = f.result()
                except Exception as exc:  # 单条未知不拖垮整轮(0002)
                    failed.append((u, str(exc)))
                    continue
                names[u] = name
                cache[u] = name
                done += 1
                if done % 200 == 0:
                    log(f"  回源 {done}/{len(need_raw)}(增量落盘)")
                    cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=1))
        cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=1))
        if failed:
            log(f"⚠ 回源失败 {len(failed)} 条(网络/限流),本轮未知、不写缓存,下次自动重试;"
                f"示例:{[u.split('github.com/')[1] for u, _ in failed[:3]]}")
    # 校验每轮重跑:回源/缓存来源的名字都可能撞名(如 repo 叫 schedule 的
    # 条目会解析到 npm 公共包 schedule),prev/catalog 来源才视为已验证
    names.update(validate_names(names, raw_sourced))
    hit = sum(1 for v in names.values() if v)
    log(f"npm 包名解析成功 {hit}/{len(names)}")
    return names, need_raw


# ---------- npm 下载量 ----------

NPM_UA = {"User-Agent": "dsh-digest-fresh-probe", "Accept": "application/json"}

# urlopen 的 timeout 管不到 DNS 解析,而一次卡死的解析能让整轮采集在
# "scoped 400/782" 上停摆四十分钟(0002 实测)。所以每个请求再套一层硬期限:
# 超时就把那个线程丢下不管(daemon,泄漏可接受),整轮继续。
CALL_DEADLINE_S = 45
# 再兜一层:任何 urlopen 忘了传 timeout 的路径也不会无限等
socket.setdefaulttimeout(30)
# 包名校验(validate_names)要逐个问 registry.npmjs.org,是全程唯一可能
# 无上限的阶段:给它单条期限 + 整体预算,宁可这轮少归因也不空转。并发压到 6:
# registry 在 12 并发下会大范围超时(0002 实测),慢总比错好。
VALIDATE_DEADLINE_S = 60
VALIDATE_BUDGET_S = 1800
VALIDATE_WORKERS = 10


def _call_with_deadline(fn, seconds=CALL_DEADLINE_S):
    box = {}

    def run():
        try:
            box["v"] = fn()
        except Exception as exc:  # 交给调用方按原有语义处理
            box["e"] = exc

    t = threading.Thread(target=run, daemon=True)
    t.start()
    t.join(seconds)
    if t.is_alive():
        raise TimeoutError(f"call exceeded {seconds}s (DNS/连接卡死)")
    if "e" in box:
        raise box["e"]
    return box.get("v")


def _get_json(u, timeout=15, attempts=6):
    """GET JSON,429/5xx 按窗口退避重试。

    api.npmjs.org 约 40 个单独请求就限流(上游 probe-downloads.mjs 2026-08-19
    实测,94/134 scoped 包连续数天空返回即此因);429 是"晚点再问",退避重试
    能过,硬扛并发永远过不了。404 = 包不存在(未发布),返回 None。
    """
    wait = 1.0
    for attempt in range(1, attempts + 1):
        try:
            req = urllib.request.Request(u, headers=NPM_UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if (e.code == 429 or e.code >= 500) and attempt < attempts:
                ra = e.headers.get("retry-after")
                s = float(ra) if ra and ra.replace(".", "", 1).isdigit() else wait
                time.sleep(s)
                wait *= 2
                continue
            raise
        except (OSError, ValueError, http.client.HTTPException):
            # OSError 涵盖 URLError/超时/连接被掐;HTTPException 涵盖
            # IncompleteRead(响应体读一半就断,0002 实测打死过一整轮)——
            # 它既不是 OSError 也不是 ValueError,所以必须显式列出。
            if attempt < attempts:
                time.sleep(wait)
                wait *= 2
                continue
            raise
    return None


def fetch_downloads(names):
    """返回 {url: 上月下载量}。unscoped 批量(100/批),scoped 逐个+退避。

    npm bulk 端点只要混进一个 scoped 名就整体拒绝(实测),scoped 只能逐个;
    逐个对限流器而言并发无意义,只烧配额,故低并发 + _get_json 指数退避。
    """
    by_name = {}
    for u, n in names.items():
        if n:
            by_name.setdefault(n, u)
    unscoped = sorted(n for n in by_name if not n.startswith("@"))
    scoped = sorted(n for n in by_name if n.startswith("@"))
    out = {}

    def record(name, val):
        if name in by_name:
            d = None if val is None else (val or {}).get("downloads")
            out[by_name[name]] = d if isinstance(d, int) else 0

    for i in range(0, len(unscoped), NPM_BULK):
        chunk = unscoped[i:i + NPM_BULK]
        q = ",".join(urllib.parse.quote(n, safe="") for n in chunk)
        try:
            d = _call_with_deadline(
                lambda: _get_json(f"https://api.npmjs.org/downloads/point/last-month/{q}"), 90)
            if isinstance(d, dict) and "downloads" not in d:
                for n, v in d.items():
                    record(n, v)
            elif isinstance(d, dict):
                record(d.get("package", chunk[0]), d)
        except Exception as e:  # 整批失败记 0,下一轮重采
            log(f"bulk 批次失败({chunk[0]}…):{e}")
        if (i // NPM_BULK) % 10 == 0:
            log(f"npm bulk {i + len(chunk)}/{len(unscoped)}")

    if scoped:
        log(f"npm scoped 逐个(退避重试):{len(scoped)}")
        done = 0

        def one(n):
            u = f"https://api.npmjs.org/downloads/point/last-month/{urllib.parse.quote(n, safe='')}"
            try:
                return n, _call_with_deadline(lambda: _get_json(u, attempts=3))
            except Exception:  # 该包本轮放弃,记 0
                return n, None

        with cf.ThreadPoolExecutor(3) as ex:
            for n, d in ex.map(one, scoped):
                record(n, d)
                done += 1
                if done % 200 == 0:
                    log(f"  scoped {done}/{len(scoped)}")
    ok = sum(1 for v in out.values() if v)
    log(f"下载量取到 {len(out)} 个包(非零 {ok})")
    return out


# ---------- GitHub GraphQL ----------

def fetch_stars(entries):
    """gh api graphql 批量取 stargazerCount/pushedAt/isArchived。返回 {url: {...}}。

    注意:单个 alias 失败会让 gh 以 rc=1 退出,但 data 里仍有其余结果,
    所以 rc!=0 也要解析 stdout;repo 归一后按仓去重、结果回填到同仓全部条目。
    """
    by_repo = {}
    for e in entries:
        by_repo.setdefault(repo_of(e["url"]), []).append(e["url"])
    repos = sorted(by_repo)
    out = {}

    for i in range(0, len(repos), GH_BATCH):
        chunk = repos[i:i + GH_BATCH]
        alias = " ".join(
            f'r{j}: repository(owner:"{r.split("/")[0]}",name:"{r.split("/")[1]}")'
            f'{{stargazerCount pushedAt isArchived}}'
            for j, r in enumerate(chunk))
        q = f"query{{{alias}}}"
        data = {}
        try:
            p = subprocess.run(["gh", "api", "graphql", "-f", f"query={q}"],
                               capture_output=True, text=True, timeout=60)
            data = json.loads(p.stdout).get("data") or {}
        except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError) as e:
            log(f"GraphQL 批次失败({chunk[0]}…):{e}")
            continue
        for j, r in enumerate(chunk):
            v = data.get(f"r{j}")
            if v:
                for url in by_repo[r]:
                    out[url] = {"stars": v["stargazerCount"],
                                "pushedAt": v["pushedAt"],
                                "archived": v["isArchived"]}
        if (i // GH_BATCH) % 10 == 0:
            log(f"graphql {i + len(chunk)}/{len(repos)}")
    log(f"star 取到 {len(out)} 个条目")
    return out


# ---------- 快照与报告 ----------

def load_json(p):
    try:
        return json.loads(p.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def latest_snapshot():
    snaps = sorted(SNAP_DIR.glob("snap-*.json"))
    return snaps[-1] if snaps else None


def main():
    quiet = "--quiet" in sys.argv
    sys.path.insert(0, str(HERE))
    from census import load_entries
    entries = load_entries()

    prev_path = latest_snapshot()
    prev = load_json(prev_path) if prev_path else None
    # 增量基线此刻就定死:上一份 snap,否则最近一份 catalog 转储。
    # 不能等到报告时再取——那时今天刚写的快照会成为"自己的基线"(全 0 增量)。
    base = prev
    if not base:
        cats = sorted(SNAP_DIR.glob("catalog-*.json"))
        base = load_json(cats[-1]) if cats else None
    prev_map = {u: v.get("npm") for u, v in (prev or {}).get("entries", {}).items()}
    catalog_map = {}
    for c in sorted(SNAP_DIR.glob("catalog-*.json")):
        d = load_json(c) or {}
        catalog_map.update({u: v.get("npm") for u, v in d.get("entries", {}).items()
                            if v.get("npm")})
    catalog_map = {u: n for u, n in catalog_map.items() if n}

    names, _ = resolve_npm_names(entries, prev_map, catalog_map)
    dl = fetch_downloads(names)
    gh = fetch_stars(entries)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    snap = {
        "date": today, "count": len(entries),
        "entries": {e["url"]: {"npm": names.get(e["url"]),
                               "dl": dl.get(e["url"], 0),
                               **(gh.get(e["url"], {}))}
                    for e in entries},
    }
    SNAP_DIR.mkdir(exist_ok=True)
    out = SNAP_DIR / f"snap-{today}.json"
    out.write_text(json.dumps(snap, ensure_ascii=False, indent=1))
    log(f"快照写入 {out}")

    if quiet:
        return
    # ---- 增量报告(基线已在 main 开头定死)----
    pe = (base or {}).get("entries", {})
    pd = (base or {}).get("date", "?")
    rows, unattr = [], 0
    for e in entries:
        u = e["url"]
        ent = snap["entries"][u]
        d1 = ent.get("dl") or 0
        if not ent.get("npm"):
            # npm 名缺失(未发布/撞名被弃)→ 下载不可归因,退出增量统计,
            # 否则会产生 d0>0→d1=0 的假负增量污染类目流向
            unattr += 1
            d1 = None
        d0 = (pe.get(u) or {}).get("dl") or 0
        s1 = ent.get("stars") or 0
        rows.append({"name": e.get("name", u), "cat": e.get("category", "?"),
                     "d0": d0, "d1": d1,
                     "delta": (d1 - d0) if d1 is not None else None,
                     "stars": s1, "new": u not in pe})
    have = [r for r in rows if r["d1"] is not None]
    tot1 = sum(r["d1"] for r in have)
    tot0 = sum(r["d0"] for r in have)
    print(f"\n== 快照 {pd} → {today}(条目 {len(rows)},npm 可归因 {len(have)})==")
    print(f"npm 不可归因(未发布到 npm 或包名撞名弃用):{unattr}")
    print(f"下载总量(可归因部分){tot0} → {tot1}"
          f"({f'+{(tot1-tot0)/tot0*100:.0f}%' if tot0 else 'n/a'})")
    print("\n-- 增量榜 Top25 --")
    for r in sorted([r for r in rows if r["delta"] is not None],
                    key=lambda r: -r["delta"])[:25]:
        tag = " 🆕" if r["new"] else ""
        print(f"+{r['delta']:>7} ({r['d0']:>6}→{r['d1']:>6}) {r['stars']:>6}★ "
              f"[{r['cat']:^9}]{tag} {r['name']}")
    silent = sum(1 for r in rows if not r["d1"] and not r["stars"])
    withdl = sum(1 for r in rows if r["d1"])
    print(f"\n有下载 {withdl}({100*withdl/len(rows):.0f}%),双无 {silent}({100*silent/len(rows):.0f}%)")
    if pd:
        from collections import Counter
        c = Counter()
        for r in have:
            c[r["cat"]] += r["delta"]
        t = sum(c.values()) or 1
        print("-- 增量下载类目 Top8 --")
        for cat, v in c.most_common(8):
            print(f"{cat:>10}: {v:>8} ({100*v/t:5.1f}%)")


if __name__ == "__main__":
    main()
