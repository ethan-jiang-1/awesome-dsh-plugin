#!/usr/bin/env python3
"""插件生态普查:census.py

对 data/plugins/*.yml 做(与机制无关的)内容层统计。设计为可在每次 upstream
同步后重跑——输出全文本表格,供 _digested/ecosystem/ 各文档引用与更新。

用法:python3 _digested/ecosystem/census.py
依赖:仅标准库(YAML 子集解析是手写的容错版)。
"""
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLUG = ROOT / "data" / "plugins"

# 新队列的起点:0001 审计基线当天。写死在这里,好让 04-value-trend §4 的
# 「新队列 vs 存量类目漂移」表由同一脚本复现(0001 时该表口径没有落盘,0002 补)。
COHORT_FROM = "2026-09-12"


def strip_comment(val):
    """YAML 行内注释:只有「前面是空白、且不在引号内」的 # 才起注释。

    url 里的 #sub 片段没有前置空白,描述里的 #tag / #12B7F5 都在引号内,
    两者都不能被切掉。0002 修复:此前不做剥离,投稿者把 PR 模板的注释一起
    粘进 category 行时(实测 2 条),# 后面的注释文字被当成类目名,凭空
    多出两个类目(见 0002 变更记录)。
    """
    out, quote = [], None
    for i, ch in enumerate(val):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif ch == "#" and (i == 0 or val[i - 1].isspace()):
            break
        out.append(ch)
    return "".join(out).strip()


def parse_yml(path):
    """字段白名单内的简易解析:url/name/category/tarball/description.en/zh。

    本仓库条目保证顶层平铺、值单行(contributing 约定);解析失败返回 None。
    """
    doc = {}
    in_desc = False
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    for raw in text.splitlines():
        line = raw.rstrip("\r").rstrip()
        if not line:
            continue
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), strip_comment(m.group(2))
            if key == "description":
                in_desc = not bool(val)
                continue
            doc[key] = val.strip("'\"")
            in_desc = False
            continue
        m = re.match(r"^\s+(en|zh):\s*(.*)$", line)
        if m and in_desc:
            doc[f"description.{m.group(1)}"] = strip_comment(m.group(2)).strip("'\"")
    return doc


def load_entries():
    out = []
    for p in sorted(PLUG.glob("*.yml")):
        d = parse_yml(p)
        if d and d.get("url"):
            d["file"] = p.name
            out.append(d)
        else:
            print(f"!! 解析失败:{p.name}", file=sys.stderr)
    return out


def first_add_dates():
    """单趟 git 遍历:每个条目文件的首次出现日期(diff-filter=A,含改名前的原件)。"""
    res = subprocess.run(
        ["git", "-C", str(ROOT), "log", "--reverse", "--diff-filter=A",
         "--name-only", "--date=short", "--format=@%ad", "--", "data/plugins"],
        capture_output=True, text=True)
    if res.returncode != 0:
        print("!! git 失败", res.stderr, file=sys.stderr)
        return {}
    dates = {}
    cur = None
    for line in res.stdout.splitlines():
        if line.startswith("@"):
            cur = line[1:]
        elif line.startswith("data/plugins/") and cur:
            dates.setdefault(line.split("/")[-1], cur)
    return dates


# ── 技术特征标签(按 en/zh 描述文本正则)────────────────────────────────
TAGS = {
    "MCP 协议":       r"\bmcp\b|model context protocol|modelcontextprotocol",
    "TTS 语音合成":   r"\btts\b|text.?to.?speech|语音合成|朗读|配音",
    "ASR 语音识别":   r"\basr\b|\bstt\b|speech.?recognition|whisper|语音识别|转写|听打",
    "OCR/截屏理解":   r"\bocr\b|文字识别|截图识别|screen\w*.?(?:read|understand|shot)",
    "图像生成":       r"image.?generat|image.?gen\b|文生图|生图|绘图|画画|画图|text.?to.?image|\bdall|midjourney|stable diffusion|海报|avatar.?gen|头像生成|logo.?gen|壁纸生成",
    "图像理解":       r"识图|看图|图片理解|image.?(?:analys|understand)|vision.?(?:capab|underst)",
    "视频":           r"\bvideo\b|视频|youtube|bilibili|b站|yt[- ]?transcript|小宇宙|播客",
    "RAG/知识库":     r"\brag\b|embedding|向量|知识库|knowledge\s*base|second brain|obsidian|notion|logseq|siyuan|思源|memos?",
    "Web 检索":       r"web.?search|searxng|tavily|brave.?search|duckduckgo|搜索引擎|联网搜索|arxiv|scholar|reddit|wikipedia|hacker.?news|exa\b|firecrawl|jina",
    "浏览器自动化":   r"playwright|puppeteer|selenium|\bcdp\b|chrome|browser.?use|浏览器(?:自动化|操控)?",
    "模型聚合/路由":  r"openrouter|one-?api|new-?api|litellm|aggregat|统一接口|聚合|中转|failover|回退|fallback|负载均衡|proxy",
    "OpenAI":         r"openai|gpt[- ]?[45o]",
    "Claude":         r"\bclaude\b|anthropic",
    "Gemini":         r"gemini",
    "DeepSeek":       r"deepseek(?![- ]?harness)|深度求索",
    "GLM":            r"\bglm\b|智谱|zhipu|chatglm",
    "Qwen":           r"qwen|通义千问",
    "Kimi":           r"kimi|moonshot",
    "本地推理":       r"\bollama\b|lm ?studio|\bvllm\b|llama\.?cpp|本地模型|local llm",
    "硅基流动":       r"siliconflow|硅基",
    "用量/成本监控":  r"\bcost\b|billing|quota|余额|费用|计费|用量|配额|账单|花费|credit",
    "IM 推送":        r"telegram|\btg\b|discord|slack|飞书|feishu|lark|钉钉|dingtalk|企微|企业微信|wecom|\bqq\b|ntfy|bark|pushdeer|gotify|webhook|邮件|\be-?mail\b|smtp",
    "任务/项目管理":  r"todo(?:ist)?|task(?:master|warrior)?|jira|linear|asana|clickup|kanban|看板|任务|日程|calendar|日历|滴答|ticktick|习惯|habit|番茄|pomodoro|gantt|甘特",
    "文档/写作输出":  r"resume|简历|\bcv\b|论文|paper|文献|latex|word|pdf|epub|电子书|博客|blog|公众号|推文|tweet|小红书|写作|writing|novel|小说|爆款",
    "Git/DevOps":     r"code.?review|pr.?review|pull request|commit.?message|提交信息|changelog|release.?note|\bdocker\b|kubernetes|k8s|deploy|部署|运维|\bci/?cd\b|nginx|\bssh\b|supervisor|systemd",
    "终端/命令行":    r"terminal|终端|\brepl\b|\bcli\b|tmux|命令行|zellij|iterm",
    "数据/DB":        r"\bsql\b|sqlite|postgres|mysql|mongo|redis|excel|\bcsv\b|表格|spreadsheet|supabase|数据库",
    "安全/权限":      r"sandbox|沙箱|permission|审批|approval|密钥|credential|secret|redact|脱敏|隐私|privacy|审计|audit",
    "上下文/会话工程":r"context.?window|上下文|token.?limit|compaction?|压缩记忆|会话管理|对话历史|timeline|时间线|resume.?(?:chat|session)",
    "移动/远程访问":  r"mobile|手机|pwa|远程访问|remote.*(control|access)|微信小程序|小程序|app control",
    "桌面集成":       r"\bmacos\b|\bwindows\b|linux|剪贴板|clipboard|通知中心|menubar|菜单栏|状态栏|快捷键|hotkey|桌面",
    "翻译/多语":      r"translate|translation|翻译|双语|subtitle|字幕|沉浸式",
    "娱乐/陪伴":      r"\bpet\b|宠物|game|游戏|桌宠|tamagotchi|占卜|星座|塔罗|抽卡| fortune |乙游|galgame|追番|弹幕",
    "主题美化":       r"theme|skin|主题|皮肤|壁纸|wallpaper|美化|appearance|(\bfont\b|字体)(?!.*size)",
}


def tag_of(text_lower):
    hits = []
    for label, pat in TAGS.items():
        if re.search(pat, text_lower):
            hits.append(label)
    return hits


def fmt_counter(c, total=None, n=30):
    rows = []
    for i, (k, v) in enumerate(c.most_common(n), 1):
        pct = f" ({v * 100 / total:.1f}%)" if total else ""
        rows.append(f"{i:>3}. {k:<28} {v:>5}{pct}")
    return "\n".join(rows)


def main():
    entries = load_entries()
    dates = first_add_dates()
    stars = json.loads((ROOT / "data" / "stars.json").read_text())
    downloads = json.loads((ROOT / "data" / "downloads.json").read_text())
    N = len(entries)
    print(f"== 条目总数 {N}(解析失败见 stderr)==\n")

    # 1 官方分类普查
    cats = Counter(e.get("category", "?") for e in entries)
    print("── ① 官方分类分布 ──")
    print(fmt_counter(cats, N, len(cats)))

    # 2 作者集中度
    owners = Counter(re.sub(r"^https://github\.com/", "", e["url"]).split("/")[0].lower() for e in entries)
    dist = Counter()
    for v in owners.values():
        if v >= 30: dist["≥30 条"] += 1
        elif v >= 10: dist["10–29"] += 1
        elif v >= 5: dist["5–9"] += 1
        elif v >= 2: dist["2–4"] += 1
        else: dist["1(单件作者)"] += 1
    print("\n── ② 作者集中度 ──")
    print(f"独立 owner 数:{len(owners)};拥有条目数分布:{dict(dist)}")
    multi = [f"{k}({v})" for k, v in owners.most_common(12)]
    print("Top 12 owner:", ", ".join(multi))

    # 3 时间演化(本生态极年轻:2026-08-13 init,故用天粒度)
    dated = [(dates.get(e['file'], '?'), e) for e in entries]
    day_all = Counter(d for d, _ in dated if d != '?')
    nodate = sum(1 for d, _ in dated if d == '?')
    days = sorted(day_all)
    cum = 0
    print("\n── ③ 每日新增(首次收录,cumulative 在括号) ──")
    print(f"(无法定位首录日期:{nodate})")
    for d in days:
        cum += day_all[d]
        bar = "#" * max(1, day_all[d] // 5)
        print(f"{d}  {day_all[d]:>4} ({cum:>4})  {bar}")
    if len(days) >= 7:
        recent = sum(day_all[d] for d in days[-7:]) / 7
        print(f"近 7 天日均新增:{recent:.0f}")

    # 最近若干天 × 分类透视
    win = days[-7:]
    top_cats = [c for c, _ in cats.most_common(10)]
    piv = defaultdict(Counter)
    tot_by_day = Counter()
    for d, e in dated:
        if d != '?' and d in win:
            piv[d][e.get('category', '?')] += 1
            tot_by_day[d] += 1
    print("\n最近 7 天 × Top10 分类(占当日新增%):")
    head = "日期       " + "".join(f"{c[:7]:>9}" for c in top_cats)
    print(head)
    for d in win:
        tot = max(1, tot_by_day[d])
        row = f"{d}  " + "".join(f"{piv[d][c] * 100 // tot:>8}%" for c in top_cats)
        print(row)

    # 4 技术特征标签(en+zh 描述合并判定,每条目去重计数)
    labeled = 0
    tag_count = Counter()
    co = Counter()
    entry_tags = {}
    for e in entries:
        text = " ".join(filter(None, [e.get("description.en"), e.get("description.zh")])).lower()
        hits = tag_of(text)
        if hits:
            labeled += 1
        entry_tags[e["url"]] = hits
        for t in hits:
            tag_count[t] += 1
        for i, a in enumerate(hits):
            for b in hits[i + 1:]:
                co[tuple(sorted((a, b)))] += 1
    print(f"\n── ④ 技术特征标签 ──(命中至少一个标签:{labeled}/{N})")
    print(fmt_counter(tag_count, N, len(tag_count)))
    print("\n高频共现(Top 15):")
    for (a, b), v in co.most_common(15):
        print(f"  {a} × {b}: {v}")

    # 标签 × 官方分类(前 6 个标签展开)
    print("\n主要标签落在哪些官方分类(前 6 标签):")
    for lab, _ in tag_count.most_common(6):
        cc = Counter(e.get('category', '?') for e in entries if lab in entry_tags[e['url']])
        tops = ", ".join(f"{c}:{v}" for c, v in cc.most_common(4))
        print(f"  {lab}({tag_count[lab]})→ {tops}")

    # 5 成熟度(stars/downloads)——统一按「join 到当前条目」的行统计,边车孤儿行单列
    urlset = {e["url"] for e in entries}
    svals = sorted(stars[u]["stars"] for u in urlset if u in stars and isinstance(stars[u], dict))
    srows = sum(1 for v in stars.values() if isinstance(v, dict))
    dvals_star = sorted(downloads[u]["downloads"] for u in urlset if u in downloads and isinstance(downloads[u], dict))
    drows = sum(1 for v in downloads.values() if isinstance(v, dict))
    med = svals[len(svals)//2]
    mean = sum(svals) / max(1, len(svals))
    above = sum(1 for x in svals if x >= 100)
    zeroish = sum(1 for x in svals if x <= 5)
    print(f"\n── ⑤ 成熟度信号(join 到当前条目) ──")
    print(f"stars 覆盖 {len(svals)}/{len(entries)} 条目(边车 {srows} 行,{srows-len(svals)} 行孤儿):"
          f"中位 {med},均值 {mean:.0f},≤5 星占 {zeroish*100//max(1,len(svals))}%,≥100 星 {above} 条")
    smap = {u: v["stars"] for u, v in stars.items() if isinstance(v, dict) and u in urlset}
    top_star = sorted(smap.items(), key=lambda kv: -kv[1])[:15]
    ent_by_url = {e["url"]: e for e in entries}
    print("Top 15 by stars(join):")
    for u, s in top_star:
        e = ent_by_url.get(u)
        cat = e.get("category") if e else "?"
        nm = (e.get("name") if e else u)[:52]
        print(f"  {s:>6}  [{cat:<9}] {nm}")
    if dvals_star:
        dmd = dvals_star[len(dvals_star)//2]
        print(f"npm 月下载覆盖 {len(dvals_star)}/{len(entries)}(边车 {drows} 行,{drows-len(dvals_star)} 行孤儿):中位 {dmd},top: "
              + ", ".join(f"{ent_by_url.get(u, {}).get('name', u)}={v['downloads']}"
                          for u, v in sorted(downloads.items(), key=lambda kv: -(kv[1]['downloads'] if isinstance(kv[1], dict) else 0))[:8] if u in urlset))

    # 6 命名与语言习惯(repo 名以 dsh 开头的占比;文件形如 owner__repo--sub.yml)
    prefixed = sum(
        1 for e in entries
        if re.sub(r"^https://github\.com/", "", e["url"]).split("/")[1].lower().startswith("dsh")
    )
    zh_ok = sum(1 for e in entries if e.get("description.zh"))
    subpath = sum(1 for e in entries if "/tree/" in e["url"])
    mono_owner = Counter()
    for e in entries:
        if "/tree/" in e["url"]:
            rp = re.sub(r"^https://github\.com/", "", e["url"]).split("/tree/")[0]
            mono_owner[rp.lower()] += 1
    print(f"\n── ⑥ 形态习惯 ──")
    print(f"dsh 前缀命名 {prefixed}/{N};中文描述齐备 {zh_ok}/{N}({zh_ok*100//N}%);"
          f"monorepo 子包条目 {subpath},来自 {len(mono_owner)} 个仓,Top5: "
          + ", ".join(f"{k}({v})" for k, v in mono_owner.most_common(5)))

    # 7 信号沉默度:有多少条目在 stars/downloads 边车里连一条成熟度信号都没有
    have_star = {u for u in urlset if u in stars and isinstance(stars[u], dict)}
    have_dl = {u for u in urlset if u in downloads and isinstance(downloads[u], dict)}
    both = len(have_star & have_dl)
    neither = len(urlset) - len(have_star | have_dl)
    star0 = sum(1 for u in have_star if stars[u].get("stars", 0) == 0)
    dl0 = sum(1 for u in have_dl if downloads[u].get("downloads", 0) == 0)
    tarb = sum(1 for e in entries if e.get("tarball"))
    print(f"\n── ⑦ 信号沉默度 ──")
    print(f"star+download 双覆盖:{both};两者皆无(完全沉默):{neither} ({round(neither*100/max(1, N))}%);"
          f"有 star 但 ==0:{star0};有下载但 ==0:{dl0};带 tarball:{tarb}")

    # 8 新队列 vs 存量的类目漂移(0002 新增;口径见文件头 COHORT_FROM)
    cohort = [e for d, e in dated if d != '?' and d >= COHORT_FROM]
    C = len(cohort)
    ccoh = Counter(e.get("category", "?") for e in cohort)
    print(f"\n── ⑧ 新队列 vs 存量({COHORT_FROM} 起首录,新队列 {C} 条) ──")
    print(f"{'category':<10}{'存量':>7}{'存量%':>8}{'新队列':>8}{'新队列%':>9}{'漂移pp':>8}")
    drift = {c: (ccoh.get(c, 0) * 100 / max(1, C)) - (n * 100 / N) for c, n in cats.items()}
    for c, n in cats.most_common(12):
        sp = n * 100 / N
        cp = ccoh.get(c, 0) * 100 / max(1, C)
        print(f"{c:<10}{n:>7}{sp:>7.1f}%{ccoh.get(c, 0):>8}{cp:>8.1f}%{cp-sp:>+7.1f}")
    ranked = sorted(drift.items(), key=lambda kv: -kv[1])
    print("上升:" + " · ".join(f"{c} {v:+.1f}" for c, v in ranked[:5] if v > 0))
    print("下降:" + " · ".join(f"{c} {v:+.1f}" for c, v in ranked[-5:] if v < 0))


if __name__ == "__main__":
    main()
