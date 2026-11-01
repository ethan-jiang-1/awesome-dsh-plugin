#!/usr/bin/env node
// `_leverage/` 自校验：严格 UTF-8、LF 换行与单个结尾换行、相对链接与锚点、
// 两册的 frontmatter 契约、产品线 catalog 与 lever 卡表的双向一致、卡片影响力门槛，
// 以及产品线每张样本卡必须有「它想干什么 · 为什么值得借鉴」一节（意图/意义/用户价值/表达）。
// 自包含：只读 `_leverage/` 这一棵树，不依赖 `_digested/` 的任何脚本或数据。
// 用法：node _leverage/verify.mjs   （在仓库根执行）

import { readdirSync, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(here, '..');
const roots = ['_leverage'];

const failures = [];
function fail(file, line, msg) {
  const loc = line == null ? file : `${file}:${line}`;
  failures.push(`${loc}  ${msg}`);
}

// ---------- 收集文件 ----------
const mdFiles = [];
for (const root of roots) {
  (function walk(dir) {
    for (const name of readdirSync(join(repoRoot, dir), { withFileTypes: true })) {
      const rel = join(dir, name.name);
      if (name.isDirectory()) walk(rel);
      else if (name.name.endsWith('.md')) mdFiles.push(rel);
    }
  })(root);
}

// ---------- 内容检查 ----------
const headingsByFile = new Map(); // rel -> Set(slug)
const textsByFile = new Map(); // rel -> 原文，供 leverage frontmatter 校验复用
const warnings = [];

function githubSlug(text) {
  return text
    .trim()
    .toLowerCase()
    .replace(/[\p{P}\p{S}]/gu, '') // 去标点/符号（保留文字、数字、空格、连字符）
    .replace(/ /g, '-');
}

for (const rel of mdFiles) {
  const raw = readFileSync(join(repoRoot, rel));
  // 严格 UTF-8
  let text;
  try {
    text = new TextDecoder('utf-8', { fatal: true }).decode(raw);
  } catch {
    fail(rel, null, '不是严格 UTF-8');
    continue;
  }
  // LF 换行
  const crLine = text.split('\n').findIndex((l, i) => l.endsWith('\r')) + 1;
  if (crLine > 0) fail(rel, crLine, '含 CR，应为 LF');
  // 单个结尾换行
  if (!text.endsWith('\n')) fail(rel, null, '缺结尾换行');
  else if (text.endsWith('\n\n')) fail(rel, null, '结尾多余空行');

  const slugs = new Set();
  let inFence = false;
  text.split('\n').forEach((line, i) => {
    if (/^(```|~~~)/.test(line.trim())) {
      inFence = !inFence;
      return;
    }
    if (!inFence && /^#{1,6} /.test(line)) slugs.add(githubSlug(line.slice(line.indexOf(' ') + 1)));
    if (!inFence) {
      for (const m of line.matchAll(/\[[^\]]*\]\(([^)\s]+)(?: "[^"]*")?\)/g)) {
        checkLink(rel, i + 1, m[1]);
      }
    }
  });
  headingsByFile.set(rel, slugs);
  textsByFile.set(rel, text);
}

function checkLink(fromRel, line, target) {
  if (/^(https?:|mailto:|#|$)/.test(target)) return; // 外链与页内锚点另行处理
  let pathPart = target;
  let anchor = '';
  const hash = target.indexOf('#');
  if (hash >= 0) {
    anchor = target.slice(hash + 1);
    pathPart = target.slice(0, hash);
  }
  if (!pathPart) return; // 纯 # 锚点指向本文件
  const abs = resolve(dirname(join(repoRoot, fromRel)), decodeURIComponent(pathPart));
  if (!abs.startsWith(repoRoot)) return fail(fromRel, line, `链接逃出仓库：${target}`);
  let fsPath = abs;
  try {
    readFileSync(fsPath);
  } catch {
    return fail(fromRel, line, `链接目标不存在：${target}`);
  }
  if (anchor && fsPath.endsWith('.md')) {
    const key = fsPath.startsWith(repoRoot + '/') ? fsPath.slice(repoRoot.length + 1) : fsPath;
    const slugs = headingsByFile.get(key);
    if (slugs && !slugs.has(anchor)) fail(fromRel, line, `锚点不存在：${target}`);
  }
}

// ---------- 两册：frontmatter 契约 ----------
const LEVERAGE_PREFIX = '_leverage/leverage/';
const PRODUCT_PREFIX = '_leverage/leverage-reshape-product/';
const AGENT_PREFIX = '_leverage/leverage-agent-collaboration/';
const DOMAIN_BY_DIR = {
  // 协作册已独立成册；杠杆册只保留门禁/权限两域。
  'lever-prove-output': 'prove-output',
  'lever-draw-limit': 'draw-limit',
};
const AGENT_DOMAIN_BY_DIR = {
  'delegation': 'agent-delegation',
  'teams': 'agent-teams',
  'pipelines': 'agent-pipelines',
  'crossing': 'agent-crossing',
  'coordination': 'agent-coordination',
};
const KINDS = new Set(['index', 'charter', 'guide', 'playbook', 'card', 'sample', 'evidence']);
const STATUSES = new Set(['observed', 'inferred', 'open', 'living']);
const FM_REQUIRED = ['title', 'domain', 'kind', 'positioning', 'read_when', 'status', 'updated'];
const TAKEAWAY_REQUIRED = new Set(['card', 'sample', 'playbook']);
const BORROW_HEADING = /^#{2,3} .*(借鉴|搬走|借用|照抄|食谱|配方|移植)/m;
// 每张样本卡开头必须回答「它想干什么 / 为什么值得借鉴」（意图 · 意义 · 用户价值 · 表达）。
// 逐卡补齐期间是提醒；补齐后改为 fail（见 goal：24 张卡）。
const WHY_HEADING = /^## 它想干什么 · 为什么值得借鉴$/m;

function parseFrontmatter(text) {
  if (!text.startsWith('---\n')) return { error: '缺 frontmatter（文件必须以 --- 开头）' };
  const end = text.indexOf('\n---\n', 4);
  if (end < 0) return { error: 'frontmatter 未闭合' };
  const meta = {};
  for (const line of text.slice(4, end).split('\n')) {
    if (!line.trim()) continue;
    const m = line.match(/^([A-Za-z_][A-Za-z0-9_]*):[ \t]*(.*)$/);
    if (!m) return { error: `frontmatter 行无法解析：${line}` };
    const [, key, raw] = m;
    let value = raw.trim();
    if (value.startsWith('"')) {
      try {
        value = JSON.parse(value);
      } catch {
        return { error: `${key} 的引号值转义非法` };
      }
    }
    meta[key] = value;
  }
  return { meta };
}

for (const rel of mdFiles) {
  if (!rel.startsWith(LEVERAGE_PREFIX) && !rel.startsWith(PRODUCT_PREFIX) && !rel.startsWith(AGENT_PREFIX)) continue;
  const text = textsByFile.get(rel) ?? '';
  const parsed = parseFrontmatter(text);
  if (parsed.error) {
    fail(rel, 1, parsed.error);
    continue;
  }
  const meta = parsed.meta;

  for (const key of FM_REQUIRED) {
    if (!meta[key]) fail(rel, 1, `frontmatter 缺 ${key}`);
  }
  if (meta.title && meta.title.length > 80) fail(rel, 1, 'title 超过 80 字');
  if (meta.positioning && meta.positioning.length > 120) fail(rel, 1, 'positioning 超过 120 字');
  if (meta.read_when && meta.read_when.length > 80) fail(rel, 1, 'read_when 超过 80 字');

  let expectedDomain;
  if (rel.startsWith(PRODUCT_PREFIX)) {
    expectedDomain = 'reshape-product';
  } else if (rel.startsWith(AGENT_PREFIX)) {
    const rest = rel.slice(AGENT_PREFIX.length);
    const dir = rest.includes('/') ? rest.split('/')[0] : '';
    expectedDomain = AGENT_DOMAIN_BY_DIR[dir] ?? 'agent-collab';
  } else {
    const rest = rel.slice(LEVERAGE_PREFIX.length);
    const dir = rest.includes('/') ? rest.split('/')[0] : '';
    expectedDomain = DOMAIN_BY_DIR[dir] ?? 'layer';
  }
  if (meta.domain && meta.domain !== expectedDomain) {
    fail(rel, 1, `domain=${meta.domain} 与路径不符（应为 ${expectedDomain}）`);
  }
  if (meta.kind && !KINDS.has(meta.kind)) fail(rel, 1, `kind 非法：${meta.kind}`);
  if (meta.status && !STATUSES.has(meta.status)) fail(rel, 1, `status 非法：${meta.status}`);
  if (meta.updated && !/^\d{4}-\d{2}-\d{2}$/.test(meta.updated)) {
    fail(rel, 1, `updated 不是 YYYY-MM-DD：${meta.updated}`);
  }

  if (TAKEAWAY_REQUIRED.has(meta.kind) && !meta.takeaway) {
    fail(rel, 1, `kind=${meta.kind} 必须有 takeaway`);
  }
  if ((meta.kind === 'card' || meta.kind === 'sample') && !BORROW_HEADING.test(text)) {
    fail(rel, 1, 'card/sample 必须有借用节（标题含 借鉴/搬走/借用/照抄/食谱/配方/移植）');
  }
  if (rel.startsWith(PRODUCT_PREFIX) && meta.kind === 'sample' && !WHY_HEADING.test(text)) {
    fail(rel, 1, '缺「它想干什么 · 为什么值得借鉴」一节（意图 / 意义 / 用户价值 / 表达）');
  }
  if (meta.budget) {
    const budget = Number(meta.budget);
    if (!Number.isInteger(budget) || budget <= 0) {
      fail(rel, 1, `budget 不是正整数：${meta.budget}`);
    } else {
      const lines = text.split('\n').length - (text.endsWith('\n') ? 1 : 0);
      if (lines > budget) warnings.push(`${rel}: ${lines}/${budget} 行，超出预算`);
    }
  }
}

// ---------- 页内锚点 ----------
for (const rel of mdFiles) {
  const raw = readFileSync(join(repoRoot, rel), 'utf8');
  let inFence = false;
  raw.split('\n').forEach((line, i) => {
    if (/^(```|~~~)/.test(line.trim())) { inFence = !inFence; return; }
    if (inFence) return;
    for (const m of line.matchAll(/\[[^\]]*\]\(#([^)\s]+)\)/g)) {
      if (!headingsByFile.get(rel)?.has(decodeURIComponent(m[1]))) {
        fail(rel, i + 1, `页内锚点不存在：#${m[1]}`);
      }
    }
  });
}

// ---------- 产品线 catalog：全量 Markdown 必须一行不多一行不少 ----------
const PRODUCT_ROOT = '_leverage/leverage-reshape-product/';
const PRODUCT_CATALOG = PRODUCT_ROOT + 'catalog.md';
if (mdFiles.includes(PRODUCT_CATALOG)) {
  const text = readFileSync(join(repoRoot, PRODUCT_CATALOG), 'utf8');
  const listed = new Set();
  const seen = new Map();
  // 只把“表格行首列链接”视为目录条目，正文导航里的重复链接不算重复行。
  for (const line of text.split('\n')) {
    if (!/^\s*\|/.test(line)) continue;
    const first = line.match(/^\s*\|\s*\[`?[^\]]*`?\]\((\.\/[^)#\s]+\.md)\)/);
    if (!first) continue;
    const target = first[1].replace(/^\.\//, '');
    if (seen.has(target)) {
      fail(PRODUCT_CATALOG, null, `catalog 重复行：${target}`);
    } else {
      seen.set(target, true);
    }
    listed.add(target);
  }
  const files = mdFiles
    .filter((f) => f.startsWith(PRODUCT_ROOT))
    .map((f) => f.slice(PRODUCT_ROOT.length));
  for (const f of files) if (!listed.has(f)) fail(PRODUCT_CATALOG, null, `catalog 缺行：${f}`);
  for (const f of listed) if (!files.includes(f)) fail(PRODUCT_CATALOG, null, `catalog 多行：${f}`);
}

// ---------- 产品线 lever README：卡表必须覆盖本 lever 的全部卡片 ----------
for (const lever of ['plugin', 'profile', 'shell']) {
  const readme = `${PRODUCT_ROOT}${lever}/README.md`;
  if (!mdFiles.includes(readme)) continue;
  const text = readFileSync(join(repoRoot, readme), 'utf8');
  const linked = new Set();
  for (const m of text.matchAll(/\]\((\.\/\d{2}_[^)#\s]+\.md)\)/g)) {
    linked.add(m[1].replace(/^\.\//, ''));
  }
  const actual = mdFiles
    .filter((f) => f.startsWith(`${PRODUCT_ROOT}${lever}/`) && !f.includes('/_证据/'))
    .map((f) => f.slice(`${PRODUCT_ROOT}${lever}/`.length))
    .filter((f) => /^\d{2}_/.test(f));
  for (const f of actual) if (!linked.has(f)) fail(readme, null, `卡表缺行：${f}`);
  for (const f of linked) if (!actual.includes(f)) fail(readme, null, `卡表多行：${f}`);
}

// ---------- 产品线门槛：00-map §7 与顶部/三个 lever README 必须同数 ----------
{
  const mapPath = PRODUCT_ROOT + '00-map.md';
  if (mdFiles.includes(mapPath)) {
    const mapText = readFileSync(join(repoRoot, mapPath), 'utf8');
    const rowRe = /\| `(plugin|profile|shell)` \| ★ ≥ ([\d,]+) 或 npm 近 30 天 ≥ ([\d,]+)/g;
    const top = PRODUCT_ROOT + 'README.md';
    for (const m of mapText.matchAll(rowRe)) {
      const [, lever, star, npm] = m;
      const targets = [top, `${PRODUCT_ROOT}${lever}/README.md`];
      for (const t of targets) {
        if (!mdFiles.includes(t)) { fail(mapPath, null, `门槛目标缺失：${t}`); continue; }
        const text = readFileSync(join(repoRoot, t), 'utf8');
        if (!text.includes(`★ ≥ ${star}`)) fail(t, null, `门槛与 00-map 不一致：缺 ★ ≥ ${star}`);
        if (!text.includes(`npm 近 30 天 ≥ ${npm}`)) fail(t, null, `门槛与 00-map 不一致：缺 npm ≥ ${npm}`);
      }
    }
  }
}

// ---------- 样本卡：七列洞察表 + 每张正式卡必须有固定版本 memo ----------
{
  const isSampleCard = (rel) => /^(plugin|profile|shell)\/\d{2}_.*\.md$/.test(rel.slice(PRODUCT_ROOT.length));
  const memoFor = {
    'plugin/11_薄基座-dock.md': 'plugin/_证据/07_薄基座-dock-源码复核.md',
    'plugin/12_厚工作台-better-sidebar.md': 'plugin/_证据/06_厚工作台-better-sidebar-源码复核.md',
    'plugin/21_生成式界面-dsh-genui.md': 'plugin/_证据/08_生成式界面-dsh-genui-源码复核.md',
    'plugin/31_驾驶舱-dsh-context.md': 'plugin/_证据/09_驾驶舱-dsh-context-源码复核.md',
    'plugin/42_环境搬家-dsh-config-manager.md': 'plugin/_证据/10_环境搬家-dsh-config-manager-源码复核.md',
    'plugin/43_会话搬家-dsh-chat-import.md': 'plugin/_证据/12_会话搬家-dsh-chat-import-源码复核.md',
    'plugin/51_分发与救生页-dsh-market.md': 'plugin/_证据/13_分发与救生页-dsh-market-源码复核.md',
    'plugin/52_装坏自愈-dsh-plugin-health.md': 'plugin/_证据/14_装坏自愈-dsh-plugin-health-源码复核.md',
    'plugin/61_多端与远程-dsh-mobile.md': 'plugin/_证据/15_多端与远程-dsh-mobile-源码复核.md',
    'plugin/71_感官接入-modlens.md': 'plugin/_证据/16_感官接入-modlens-源码复核.md',
    'plugin/81_协作-dsh-agent-teams.md': 'plugin/_证据/17_协作-dsh-agent-teams-源码复核.md',
    'profile/11_全家桶-dsh-web.md': 'profile/_证据/04_全家桶-dsh-web-源码复核.md',
    'profile/12_界面套件-dsh-codex-ui.md': 'profile/_证据/10_界面套件-dsh-codex-ui-源码复核.md',
    'profile/13_组合包-dsh-suite.md': 'profile/_证据/09_组合包-dsh-suite-源码复核.md',
    'profile/14_聚合补丁-dsh-all.md': 'profile/_证据/08_聚合补丁-dsh-all-源码复核.md',
    'profile/15_接管套件-dsh-plugins-plus.md': 'profile/_证据/06_接管套件-dsh-plugins-plus-源码复核.md',
    'profile/16_套件市场-dsh-agent-plugins-market.md': 'profile/_证据/05_套件市场-dsh-agent-plugins-market-源码复核.md',
    'profile/17_闭环装配-better-session.md': 'profile/_证据/07_闭环装配-better-session-源码复核.md',
    'profile/18_视觉资产-dsh-wallpaper-engine.md': 'profile/_证据/11_视觉资产-dsh-wallpaper-engine-源码复核.md',
    'shell/11_桌面应用-dsh-desktop.md': 'shell/_证据/04_桌面应用-dsh-desktop-源码复核.md',
    'shell/12_单文件桌面壳-windowos.md': 'shell/_证据/06_单文件桌面壳-windowos-源码复核.md',
    'shell/13_内置运行时-tauriapp.md': 'shell/_证据/05_内置运行时-tauriapp-源码复核.md',
    'shell/14_终端即产品-dsh-TUI.md': 'shell/_证据/02_dsh-TUI-源码复核.md',
    'shell/15_终端工作区-seektty.md': 'shell/_证据/07_终端工作区-seektty-源码复核.md',
    'shell/91_冻结分叉-better-sidebar-N23.md': 'shell/_证据/03_冻结分叉-better-sidebar-N23-源码复核.md',
  };
  const columnCount = (line) => line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').length;
  for (const rel of mdFiles) {
    if (!rel.startsWith(PRODUCT_ROOT) || !isSampleCard(rel)) continue;
    const text = textsByFile.get(rel) ?? '';
    const fm = parseFrontmatter(text);
    if (fm.error || fm.meta.kind !== 'sample') continue;
    const card = rel.slice(PRODUCT_ROOT.length);
    const isAntiRecipe = /反例|反食谱/.test(`${fm.meta.title ?? ''} ${fm.meta.positioning ?? ''}`);
    if (!isAntiRecipe) {
      const sectionMatch = text.match(/^## 5\. 可迁移洞察[^\n]*\n([\s\S]*?)(?=^## )/m);
      if (!sectionMatch) {
        fail(rel, null, '正式样本卡缺少 `## 5. 可迁移洞察`（反例卡请标注“反例/反食谱”）');
      } else {
        const lines = sectionMatch[1].split('\n').filter((line) => /^\s*\|.*\|\s*$/.test(line));
        if (lines.length < 3) {
          fail(rel, null, '可迁移洞察表缺 header/divider/洞察行');
        } else {
          for (const [index, line] of lines.entries()) {
            if (columnCount(line) !== 7) fail(rel, null, `可迁移洞察表应为 7 列（表行 ${index + 1}）`);
          }
        }
      }
    }
    const memo = memoFor[card];
    if (!memo) fail(rel, null, '正式样本卡缺少源码复核 memo 映射');
    else if (!mdFiles.includes(PRODUCT_ROOT + memo)) fail(rel, null, `缺少固定版本证据 memo：${memo}`);
    else if (!text.includes(memo.split('/').pop())) {
      fail(rel, null, `卡片未链接其固定版本证据 memo：${memo}`);
    }
  }
}

// ---------- 协作册：每个家族样本必须有同号 memo，且卡片链接它 ----------
{
  for (const rel of mdFiles) {
    if (!rel.startsWith(AGENT_PREFIX)) continue;
    const m = rel.match(/^_leverage\/leverage-agent-collaboration\/([^/]+)\/samples\/(\d{2})-.*\.md$/);
    if (!m) continue;
    const [, family, num] = m;
    const text = textsByFile.get(rel) ?? '';
    const memoDir = `${AGENT_PREFIX}${family}/_证据/`;
    const memos = mdFiles.filter((p) => p.startsWith(memoDir) && p.split('/').pop().startsWith(num + '-'));
    if (memos.length === 0) { fail(rel, null, `缺少同号证据 memo：${family}/_证据/${num}-*.md`); continue; }
    if (!memos.some((p) => text.includes(p.split('/').pop()))) {
      fail(rel, null, `样本卡未链接其证据 memo：${memos[0].split('/').pop()}`);
    }
  }
}

// ---------- 杠杆册：机制卡/playbook 必须有“证据与边界”节（≥3 条） ----------
{
  for (const rel of mdFiles) {
    if (!rel.startsWith(LEVERAGE_PREFIX) && !rel.startsWith(AGENT_PREFIX)) continue;
    const text = textsByFile.get(rel) ?? '';
    const fm = parseFrontmatter(text);
    if (fm.error) continue;
    if (fm.meta.kind !== 'card' && fm.meta.kind !== 'playbook') continue;
    const m = text.match(/^## 证据与边界[^\n]*\n([\s\S]*?)(?=^## |$(?![\s\S]))/m);
    if (!m) { fail(rel, null, '机制卡/playbook 缺少 `## 证据与边界`'); continue; }
    const rows = m[1].split('\n').filter((line) => /^\s*\|.*\|\s*$/.test(line)).length;
    if (rows < 5) fail(rel, null, '`证据与边界` 表至少 header+divider+3 行');
  }
}

// ---------- 产品线：卡头影响力必须过门槛，或标“机制例外” ----------
{
  const mapPath = PRODUCT_ROOT + '00-map.md';
  if (mdFiles.includes(mapPath)) {
    const mapText = readFileSync(join(repoRoot, mapPath), 'utf8');
    const thresholds = new Map();
    for (const m of mapText.matchAll(/\| `(plugin|profile|shell)` \| ★ ≥ ([\d,]+) 或 npm 近 30 天 ≥ ([\d,]+)/g)) {
      const n = (v) => Number(v.replace(/,/g, ''));
      thresholds.set(m[1], [n(m[2]), n(m[3])]);
    }
    const num = (v) => Number(String(v).replace(/,/g, '')) || 0;
    for (const rel of mdFiles) {
      if (!rel.startsWith(PRODUCT_ROOT)) continue;
      const parts = rel.slice(PRODUCT_ROOT.length).split('/');
      if (parts.length !== 2 || !thresholds.has(parts[0]) || !/^\d{2}_/.test(parts[1])) continue;
      const text = readFileSync(join(repoRoot, rel), 'utf8');
      const head = text.split('\n').slice(0, 36).join('\n');
      const starM = head.match(/★\s*\**\s*([\d,]+)/);
      let npm = 0;
      for (const pat of [/npm 月下载\s*\**\s*([\d,]+)/, /npm 近 30 天\s*\**\s*([\d,]+)/, /npm\s*\**\s*([\d,]+)\**/]) {
        const m = head.match(pat);
        if (m) { npm = num(m[1]); break; }
      }
      const [starMin, npmMin] = thresholds.get(parts[0]);
      const ok = (starM && num(starM[1]) >= starMin) || npm >= npmMin;
      if (!ok && !text.includes('机制例外')) {
        fail(rel, null, `影响力未过 ${parts[0]} 门槛（★${starM ? starM[1] : 0} / npm ${npm}），且未标“机制例外”`);
      }
    }
  }
}

if (warnings.length) {
  console.warn(`⚠ ${warnings.length} 条提醒`);
  for (const w of warnings) console.warn('  ' + w);
}
if (failures.length) {
  console.error(`✗ ${failures.length} 个问题`);
  for (const f of failures) console.error('  ' + f);
  process.exit(1);
}
console.log(`✓ ${mdFiles.length} 个 Markdown 文件全部通过`);
