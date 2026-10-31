#!/usr/bin/env python3
"""四领域(杠杆)普查:leverage/census.py

回答的不是「有哪些插件」,而是「每个领域里有多少供给、供给落在哪、谁在供、
披露了什么」。与 ecosystem/census.py 共用同一份 YAML 子集解析器(直接 import,
避免两份解析口径漂移),但统计口径是本目录自己的。

用法:python3 _digested/leverage/census.py
依赖:仅标准库。

口径纪律(引用本脚本任何数字前必读):
- 命中 = 条目 en/zh 描述文本的正则匹配,**接受多标**。它是「作者声称」,
  不是实测能力;子主题计数之和大于领域命中数。
- 领域之间不互斥,一个条目可同时命中多个域;§4 给重叠矩阵。
- 能力披露来自 data/capabilities.json(2026-09-24 静态扫描快照),
  按 URL join 当前名单,覆盖率见 §6 的分母;不是新扫描、不是判决。
- 新队列口径沿用 ecosystem/census.py 的 COHORT_FROM(2026-09-12)。
- **§9 准入门是「立卡」的唯一入口。** §1–§8 的命中数是候选池,不是研究对象;
  能进卡片的条目必须过 §9 的门。抓到一个就琢磨,不是这套方法。
"""
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ECO = ROOT / "_digested" / "ecosystem" / "census.py"

_spec = importlib.util.spec_from_file_location("eco_census", ECO)
eco = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(eco)

COHORT_FROM = eco.COHORT_FROM

# ── 领域与子主题(召回优先的正则表)──────────────────────────────────────
# 每个子主题是一组关键词;一条描述命中组内任一关键词即计入该子主题。
# 这些组是为了「找到候选」,不是为了「证明分类」;卡片里的判断必须回读原文。
DOMAINS = {
    "RESHAPE 形态跃迁 (lever-reshape-product)": {
        "shell 换壳/工作台": r"工作台|workbench|vscode|ide\b|编辑器|editor|布局|layout|整站|全屏|tui|terminal ui|看板|kanban|驾驶舱|cockpit|workspace ui",
        "package 桌面/独立应用": r"desktop|electron|tauri|桌面|独立应用|standalone|app shell|启动器|launcher|安装包|installer|portable|打包为",
        "preset 身份/预设": r"agent preset|预设|preset|persona|人设|角色卡|role card|身份|identity|品牌|brand|onboarding|引导|首启|first.?run|开场",
        "dist 分发/市场": r"market|marketplace|市场|store|商店|索引|index|recipe|配方|bundle|组合包|profile|分发|distribution|上架",
    },
    "CROSS 协作拓扑 (lever-cross-boundary)": {
        "hierarchy 层级/团队": r"subagent|sub-agent|子代理|子智能体|teammate|team|团队|swarm|fleet|roster|成员|member|专家|expert",
        "orchestration 编排/扇出": r"workflow|编排|orchestrat|pipeline|dag|任务链|并行|parallel|dispatch|调度|ralph|autopilot|扇出",
        "handoff 接力/状态": r"handoff|交接|接力|takeover|接管|session sync|会话同步|跨设备|多机|resume|续接|inbox|mailbox|消息|mail",
        "transport 传输/远端": r"ssh|sftp|remote|远程|a2a|agent.?2.?agent|\bacp\b|mcp server|tunnel|隧道|worktree|\bsdk\b",
    },
    "PROVE 质量闭环 (lever-prove-output)": {
        "gate 门禁/验收": r"gate|门禁|check|校验|validate|验证|verify|verif|acceptance|验收|shipcheck|preflight|审查|review",
        "evidence 证据/账本": r"evidence|证据|receipt|回执|audit|审计|ledger|账本|provenance|溯源|trace|trajectory|replay|复现|hash.?chain",
        "artifact 产物/稳定": r"checkpoint|检查点|snapshot|快照|rollback|回滚|undo|撤销|atomic|原子|deliverable|交付|present|产物|artifact|稳定",
        "eval 评测/诊断": r"eval|评测|benchmark|score|评分|quality|质量|diagnos|诊断|clinic|metric|指标|cost|成本",
    },
    "LIMIT 信任边界 (lever-draw-limit)": {
        "sandbox 沙箱/隔离": r"sandbox|沙箱|landlock|bwrap|seccomp|隔离|jail|workspace-only|allowroots",
        "permission 权限/审批": r"permission|权限|approval|审批|authoriz|授权|policy|策略|auto.?approve|提权|escalat|rbac|role",
        "credential 凭据/密钥": r"credential|凭据|secret|密钥|vault|保险库|token|password|口令|2fa|totp|passkey|encrypt|加密|redact|脱敏|mask",
        "supply 供应链/安装前": r"supply.?chain|供应链|pre.?install|安装前|scanner|scan|静态|static|恶意|malware|cve|osv|signature|签名",
        "network 网络/暴露面": r"tunnel|隧道|firewall|防火墙|expose|暴露|reverse proxy|反代|auth gateway|登录|login|zero.?trust|零信任|e2e|端到端|whitelist|白名单",
        "data 数据/注入": r"privacy|隐私|数据权限|data access|scope|越界|leak|泄漏|injection|注入|exfil|外传|compliance|合规|pii",
    },
}

COMPILED = {
    d: {k: re.compile(v, re.I) for k, v in subs.items()} for d, subs in DOMAINS.items()
}

# 「高杠杆候选」:描述自述注册 seam/service/slot 或改默认行为,而不是加一个工具。
LEVER_HINT = re.compile(
    r"ctx\.[a-z]+|\bseam\b|接缝|slot|插槽|注册(?:表|一个|.*service)|register(?:s|ing)?\b|"
    r"preset|profile|patch|bundle|组合包|默认值|default",
    re.I,
)

# ── 准入门(§9)────────────────────────────────────────────────────────
# 立卡不是「抓到一个就琢磨」。入口条件有两类,**缺一不立卡**:
#   影响力(A/B/C 至少 1 条)  深度(D/E 至少 1 条)
# A 引用  仓库名被其他条目按名提到 ≥3 次(目录内 in-degree)
# B 替代  自述替换/接管官方对象(profile、启动器、官方页面、官方默认行为)
# C 接缝  描述里点名具名接缝:ctx.* / waterfall / pre-step / pre|post-execute
# D 能力  capabilities.json 披露 ≥2 个高杠杆能力;**披露为空的已收录条目同样算**
#         (空披露往往是零依赖的库或纯前端,不等于低能力;但也可能是扫描器没跑)
# E 反面  被同类插件明指不可共存 / 同一接缝的两种相反取法(需人工认定)
# ⚠ 机器只能判 A–D。E 一律由人写进卡片,脚本不敢代劳。
BASE_TOK = re.compile(r"[a-z0-9][a-z0-9-]{7,}")
SUBSTITUTE = re.compile(
    r"replaces?\s+the\s+(?:official|dsh|default)|替换(?:掉)?官方|接管官方|替代官方|"
    r"replaces?\s+dsh\s+web|整站替换|替换内核|fork\s+of|forked from|完整 fork",
    re.I,
)
HIGH_LEVERAGE = ("subagent", "workflow", "sandbox", "network", "credentials",
                 "host-runtime", "dynamic-code", "shell")


def citation_counts(entries):
    """目录内 in-degree:某仓库 basename 被多少条其他条目的描述按名提到。

    只算 basename 长度 ≥8 的全词命中。**噪声已实测存在**:`terminal`(110 次)、
    `notification`(66)、`schedule`(46)、`telegram`(34)、`calendar`(33) 都是通用词,
    它们的高分不能当成影响力。用 A 之前必须回读 `citers`,确认是真引用还是撞词。
    """
    own = {}
    for e in entries:
        name = e.get("name") or ""
        own.setdefault(name.split("#")[0].split("/")[-1].lower(), set()).add(name)
    vocab = {t for t in own if len(t) >= 8}
    indeg, citers = Counter(), defaultdict(list)
    for e in entries:
        me = (e.get("name") or "").split("#")[0].split("/")[-1].lower()
        text = (e.get("description.en", "") + " " + e.get("description.zh", "")).lower()
        for tok in (set(BASE_TOK.findall(text)) & vocab) - {me}:
            indeg[tok] += 1
            if len(citers[tok]) < 3:
                citers[tok].append(e.get("name"))
    return indeg, citers, own


def gate(entries, hits):
    """准入门:返回 {url: [证据...]}。A–D 机器判,E 留空待人补。"""
    indeg, citers, own = citation_counts(entries)
    out = {}
    for e in entries:
        url = e["url"]
        text = e.get("description.en", "") + " " + e.get("description.zh", "")
        tok = (e.get("name") or "").split("#")[0].split("/")[-1].lower()
        inf = []
        if indeg.get(tok, 0) >= 3:
            inf.append(f"A 引用×{indeg[tok]}")
        if SUBSTITUTE.search(text):
            inf.append("B 替代")
        if re.search(r"ctx\.[a-z]+|waterfall|/pre-step|/pre-execute|/post-execute", text, re.I):
            inf.append("C 接缝")
        rec = CAP.get(url)
        caps = set(rec.get("capabilities", [])) if rec else None
        deep = []
        if caps is not None and (len(caps & set(HIGH_LEVERAGE)) >= 2 or not caps):
            deep.append("D 能力" if caps else "D 零披露")
        if len(inf) >= 1 and len(deep) >= 1:
            out[url] = inf + deep
    return out, indeg, citers, own


CAP = json.loads((ROOT / "data" / "capabilities.json").read_text(encoding="utf-8"))


def short(url):
    return re.sub(r"^https?://github\.com/", "", url).rstrip("/")


def main():
    entries = eco.load_entries()
    dates = eco.first_add_dates()
    N = len(entries)
    print(f"── 0 基线 ──")
    print(f"条目 {N};能力披露边车 {len(CAP)} 行;首录可定位 "
          f"{sum(1 for e in entries if dates.get(e['file']) not in (None, '?'))}")

    hits = {}
    for e in entries:
        text = " ".join(
            [e.get("description.en", ""), e.get("description.zh", "")]
        )
        per = {}
        for d, subs in COMPILED.items():
            matched = [k for k, rx in subs.items() if rx.search(text)]
            if matched:
                per[d] = matched
        hits[e["url"]] = per

    # ── 1 总表 ────────────────────────────────────────────────────────────
    any_hit = sum(1 for p in hits.values() if p)
    print(f"\n── 1 领域命中(描述正则,多标)──")
    print(f"{'domain':<22}{'条目':>7}{'占比':>8}")
    dom_count = {}
    for d in DOMAINS:
        n = sum(1 for p in hits.values() if d in p)
        dom_count[d] = n
        print(f"{d:<22}{n:>7}{n*100/N:>7.1f}%")
    print(f"{'至少命中一个领域':<22}{any_hit:>7}{any_hit*100/N:>7.1f}%")

    # ── 2 子主题 ──────────────────────────────────────────────────────────
    print(f"\n── 2 子主题(多标,和 > 领域命中)──")
    for d, subs in DOMAINS.items():
        print(f"\n[{d}]")
        for k in subs:
            n = sum(1 for p in hits.values() if k in p.get(d, []))
            print(f"  {k:<28}{n:>7}{n*100/N:>7.1f}%")

    # ── 3 域 × 官方类别 ───────────────────────────────────────────────────
    print(f"\n── 3 域 × 官方类别(Top5)──")
    by_url = {e["url"]: e for e in entries}
    for d in DOMAINS:
        cats = Counter(
            by_url[u].get("category", "?") for u, p in hits.items() if d in p
        )
        print(f"[{d}] " + " · ".join(f"{c} {n}" for c, n in cats.most_common(5)))

    # ── 4 重叠 ────────────────────────────────────────────────────────────
    print(f"\n── 4 域重叠(条目数)──")
    order = list(DOMAINS)
    print("        " + "".join(f"{d.split()[0]:>7}" for d in order))
    for a in order:
        row = [f"{a.split()[0]:<8}"]
        for b in order:
            n = sum(1 for p in hits.values() if a in p and b in p)
            row.append(f"{n:>7}")
        print("".join(row))
    combo = Counter(len(p) for p in hits.values() if p)
    print("命中域个数分布:" + " · ".join(f"{k} 域 {v}" for k, v in sorted(combo.items())))

    # ── 5 新队列漂移 ──────────────────────────────────────────────────────
    print(f"\n── 5 新队列 vs 存量(首录 ≥ {COHORT_FROM})──")
    cohort = [e for e in entries if (dates.get(e["file"]) or "?") >= COHORT_FROM
              and dates.get(e["file"]) not in (None, "?")]
    stock = [e for e in entries if (dates.get(e["file"]) or "?") < COHORT_FROM]
    C, S = len(cohort), len(stock)
    print(f"新队列 {C} · 存量 {S}")
    print(f"{'domain':<22}{'存量%':>8}{'新队列%':>9}{'漂移pp':>8}")
    for d in DOMAINS:
        sc = sum(1 for e in stock if d in hits[e["url"]])
        cc = sum(1 for e in cohort if d in hits[e["url"]])
        sp, cp = sc * 100 / max(1, S), cc * 100 / max(1, C)
        print(f"{d:<22}{sp:>7.1f}%{cp:>8.1f}%{cp-sp:>+8.1f}")

    # ── 6 能力披露 join(draw-limit 重点)──────────────────────────────────────────
    print(f"\n── 6 能力披露 join(capabilities.json,2026-09-24)──")
    joined = {u: CAP[u] for u in hits if u in CAP}
    print(f"URL join 覆盖 {len(joined)}/{N} ({len(joined)*100/N:.1f}%)")

    def stats(urls):
        caps = Counter()
        for u in urls:
            for c in CAP[u].get("capabilities", []):
                caps[c] += 1
        denom = max(1, len(urls))
        return {k: (caps[k], round(caps[k] * 100 / denom, 1)) for k in
                ("credentials", "network", "shell", "fs-write", "dynamic-code",
                 "host-runtime", "subagent")}

    for d in DOMAINS:
        us = [u for u, p in hits.items() if d in p and u in CAP]
        st = stats(us)
        print(f"[{d}] n={len(us)} · " + " · ".join(
            f"{k} {v[0]}({v[1]}%)" for k, v in st.items()))
    us = [u for u in joined if not hits[u]]
    st = stats(us)
    print(f"[域外条目] n={len(us)} · " + " · ".join(
        f"{k} {v[0]}({v[1]}%)" for k, v in st.items()))

    # ── 7 作者集中度 ──────────────────────────────────────────────────────
    print(f"\n── 7 作者集中度(Top5 owner)──")
    for d in DOMAINS:
        owners = Counter(
            (by_url[u].get("name") or "").split("/")[0].lower()
            for u, p in hits.items() if d in p
        )
        n = dom_count[d]
        top = owners.most_common(5)
        print(f"[{d}] " + " · ".join(f"{o} {c}" for o, c in top) +
              f" | Top5 占 {sum(c for _, c in top)*100/max(1, n):.1f}%")

    # ── 8 高杠杆候选 ──────────────────────────────────────────────────────
    print(f"\n── 8 自述接缝/组合的候选(LEVER_HINT)──")
    lev = [e for e in entries if LEVER_HINT.search(
        e.get("description.en", "") + e.get("description.zh", ""))]
    print(f"命中 {len(lev)} ({len(lev)*100/N:.1f}%)")
    per_dom = {d: sum(1 for e in lev if d in hits[e["url"]]) for d in DOMAINS}
    print("分域:" + " · ".join(f"{d.split()[0]} {n}" for d, n in per_dom.items()))

    # ── 9 准入门:谁能进卡片 ───────────────────────────────────────────────
    print(f"\n── 9 准入门(影响力 A/B/C ≥1 且 深度 D/E ≥1)──")
    passed, indeg, citers, own = gate(entries, hits)
    print(f"通过 {len(passed)}/{N} ({len(passed)*100/N:.1f}%)")
    print(f"门槛: A 目录内被按名引用 ≥3 次 · B 自述替换/接管官方对象 · "
          f"C 自述具名接缝 · D 披露 ≥2 个高杠杆能力 · E 反面教材(人工认定)")
    per_dom = {d: sum(1 for u in passed if d in hits[u]) for d in DOMAINS}
    print("分域:" + " · ".join(f"{d.split()[0]} {n}" for d, n in per_dom.items()))
    print("按官方类别:" + " · ".join(
        f"{c} {n}" for c, n in Counter(
            by_url[u].get("category", "?") for u in passed).most_common(8)))

    print(f"\n  9a 影响力证据分布(可多标)")
    tags = Counter()
    for ev in passed.values():
        for x in ev:
            tags[x.split()[0]] += 1
    for k in ("A", "B", "C", "D"):
        print(f"    {k}: {tags.get(k, 0)}")

    print(f"\n  9b 目录内被引用最多的仓库 A(前 12,含被谁提到)")
    for tok, n in indeg.most_common(12):
        who = " / ".join(sorted(own[tok])[:2])
        print(f"    {n:>4}  {tok:<28} {who}")
        print(f"          ← {', '.join(citers[tok])}")


def probe(pattern):
    """`--probe <regex>`:F 级准入(机制稀缺性)必须附一条可重跑的检索式。

    卡片里写「全库只有 2 条命中」时,读者要能用同一行命令复核。命中按
    en+zh 描述全文匹配,大小写不敏感。
    """
    entries = eco.load_entries()
    rx = re.compile(pattern, re.I)
    hit = [e for e in entries if rx.search(
        e.get("description.en", "") + " " + e.get("description.zh", ""))]
    print(f"检索式 {pattern!r} 命中 {len(hit)}/{len(entries)}")
    for e in hit:
        print(f"  {e.get('category','?'):<10} {e.get('name')}")
    return hit


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--probe":
        probe(sys.argv[2])
    else:
        main()
