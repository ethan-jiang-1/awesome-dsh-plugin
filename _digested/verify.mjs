#!/usr/bin/env node
// `_digested/` 与 `_faq_on_digested/` 自校验：严格 UTF-8、LF 换行与单个结尾换行、
// Markdown 相对链接与锚点存在性。
// `_leverage/` 有自己独立的校验器（`node _leverage/verify.mjs`），本文件不覆盖它。
// 用法：node _digested/verify.mjs   （在仓库根执行）

import { readdirSync, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(here, '..');
const roots = ['_digested', '_faq_on_digested'];

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
const textsByFile = new Map();    // rel -> 原文，供卡片/SVG 契约复用
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

// ---------- 卡片契约：frontmatter / 八段 / 证据等级 ----------
const CARD_RE = /^_digested\/view_([^/]+)\/([^/]+)\/([0-9]{2}-[^/]+\.md)$/;
const ALLOWED_STATUS = new Set(['active', 'watch', 'stale', 'deprecated', 'frozen', 'archived']);
const REQUIRED_H2 = [
  '一屏事实', '它到底是什么', '怎么接进 DSH', '关键实现',
  '为什么它突出', '代价与边界', '可信度与复现', '待验证',
];
const WRITING_TOP3_H2 = [
  '它替谁解决什么问题', '适用面', '业务价值',
];
const WRITING_ENFORCE_SINCE = '2026-11-25';
const cards = new Map(); // rel -> meta

function parseFrontmatter(text) {
  if (!text.startsWith('---\n')) return null;
  const end = text.indexOf('\n---\n', 4);
  if (end < 0) return null;
  const meta = {};
  for (const line of text.slice(4, end).split('\n')) {
    const m = line.match(/^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$/);
    if (m) meta[m[1]] = m[2].trim();
  }
  return meta;
}

for (const rel of mdFiles) {
  const m = rel.match(CARD_RE);
  if (!m) continue;
  const text = textsByFile.get(rel) || '';
  const meta = parseFrontmatter(text);
  if (!meta) {
    fail(rel, 1, '卡片缺 frontmatter（必须以 --- 开头）');
    continue;
  }
  cards.set(rel, meta);
  for (const key of ['kind', 'domain', 'subcategory', 'repo', 'evidence', 'status', 'asof']) {
    if (!meta[key]) fail(rel, 1, `frontmatter 缺 ${key}`);
  }
  if (!['card', 'reference'].includes(meta.kind)) {
    fail(rel, 1, `kind 非法：${meta.kind}`);
  }
  if (meta.domain !== m[1]) fail(rel, 1, `domain=${meta.domain} 与路径 ${m[1]} 不一致`);
  if (meta.subcategory !== m[2]) fail(rel, 1, `subcategory=${meta.subcategory} 与路径 ${m[2]} 不一致`);
  if (!/^[^\s/]+\/[^\s/]+$/.test(meta.repo || '')) fail(rel, 1, `repo 非法：${meta.repo}`);
  if (!/^[1-3]$/.test(meta.evidence || '')) fail(rel, 1, `evidence 非法：${meta.evidence}`);
  if (meta.evidence === '3' && !/^[0-9a-f]{7,40}$/i.test(meta.commit || '')) {
    fail(rel, 1, '★★★ 卡缺合法 commit');
  }
  if (!ALLOWED_STATUS.has(meta.status)) fail(rel, 1, `status 非法：${meta.status}`);
  if (!/^20\d{2}-\d{2}-\d{2}$/.test(meta.asof || '')) fail(rel, 1, `asof 非法：${meta.asof}`);
  if (meta.kind === 'card') {
    const h2 = [...text.matchAll(/^## (.+)$/gm)].map((x) => x[1].trim());
    for (const req of REQUIRED_H2) {
      if (!h2.some((h) => h.startsWith(req))) fail(rel, 1, `卡片缺小节：## ${req}`);
    }
    if ((meta.asof || '') >= WRITING_ENFORCE_SINCE) {
      const factIdx = h2.findIndex((h) => h.startsWith('一屏事实'));
      for (const req of WRITING_TOP3_H2) {
        const idx = h2.findIndex((h) => h.startsWith(req));
        if (idx < 0) fail(rel, 1, `新卡(asof>=${WRITING_ENFORCE_SINCE})缺读者优先小节：## ${req}`);
        else if (factIdx >= 0 && idx > factIdx) {
          fail(rel, 1, `读者优先小节 ## ${req} 必须位于 ## 一屏事实 之前`);
        }
      }
    }
  }
}

// ---------- `_data/cards.json` 与 `summary.json` 必须与 frontmatter 同步 ----------
let dataCards = [];
try {
  dataCards = JSON.parse(readFileSync(join(repoRoot, '_digested/_data/cards.json'), 'utf8'));
} catch (err) {
  fail('_digested/_data/cards.json', null, `读不到或不是 JSON：${err.message}`);
}
const dataByPath = new Map(dataCards.map((c) => [c.path, c]));
const META_KEYS = ['kind', 'domain', 'subcategory', 'repo', 'commit', 'evidence', 'status', 'asof'];
for (const [rel, meta] of cards) {
  const key = rel.slice('_digested/'.length);
  const data = dataByPath.get(key);
  if (!data) {
    fail(rel, null, '`_data/cards.json` 缺这张卡；改完 frontmatter 后跑 view_data.py');
    continue;
  }
  for (const k of META_KEYS) {
    if (String(data[k] ?? '') !== String(meta[k] ?? '')) {
      fail(rel, null, `\`_data/cards.json\` 的 ${k}=${data[k]} 与 frontmatter ${meta[k]} 不一致；跑 view_data.py`);
    }
  }
}
for (const data of dataCards) {
  if (!cards.has(`_digested/${data.path}`)) {
    fail('_digested/_data/cards.json', null, `多出非卡片：${data.path}`);
  }
}

try {
  const summary = JSON.parse(readFileSync(join(repoRoot, '_digested/_data/summary.json'), 'utf8'));
  if (summary.cards !== cards.size) {
    fail('_digested/_data/summary.json', null, `cards=${summary.cards} 与实际卡片数 ${cards.size} 不一致；跑 view_data.py`);
  }
  const actualByDomain = {};
  for (const meta of cards.values()) {
    actualByDomain[meta.domain] = (actualByDomain[meta.domain] || 0) + 1;
  }
  for (const [d, n] of Object.entries(actualByDomain)) {
    if ((summary.by_domain || {})[d] !== n) {
      fail('_digested/_data/summary.json', null, `by_domain.${d}=${(summary.by_domain || {})[d]} 与实际 ${n} 不一致；跑 view_data.py`);
    }
  }
} catch (err) {
  fail('_digested/_data/summary.json', null, `读不到或不是 JSON：${err.message}`);
}

// ---------- 自动发现领域册（view_*） ----------
const domains = readdirSync(join(repoRoot, '_digested'), { withFileTypes: true })
  .filter((d) => d.isDirectory() && d.name.startsWith('view_'))
  .map((d) => d.name.slice('view_'.length))
  .sort();

// ---------- SVG 契约：每个卡必须上图谱，且证据级一致 ----------
const domainMaps = new Map();
for (const domain of domains) {
  const mapRel = `_digested/view_${domain}/plugin-map.svg`;
  let svg;
  try {
    svg = readFileSync(join(repoRoot, mapRel), 'utf8');
  } catch {
    fail(mapRel, null, '缺少领域图谱');
    continue;
  }
  const links = new Map();
  for (const mm of svg.matchAll(/<a[^>]*href="([^"]+\.md)"[^>]*>([\s\S]*?)<\/a>/g)) {
    const href = mm[1];
    if (href.endsWith('README.md')) continue;
    const target = resolve(dirname(join(repoRoot, mapRel)), href);
    if (!target.startsWith(repoRoot)) {
      fail(mapRel, null, `SVG 链接逃出仓库：${href}`);
      continue;
    }
    const key = target.slice(repoRoot.length + 1);
    const plain = mm[2].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');
    const ev = plain.match(/★{1,3}/);
    if (!ev) {
      fail(mapRel, null, `SVG 卡片缺证据级：${href}`);
      continue;
    }
    if (links.has(key)) fail(mapRel, null, `SVG 重复链接：${href}`);
    links.set(key, ev[0].length);
  }
  domainMaps.set(domain, links);
  for (const [rel, meta] of cards) {
    if (!rel.startsWith(`_digested/view_${domain}/`)) continue;
    if (!links.has(rel)) {
      fail(rel, null, `卡片未出现在 ${mapRel}`);
    } else if (links.get(rel) !== Number(meta.evidence)) {
      fail(rel, null, `SVG 证据级 ${links.get(rel)} 与 frontmatter ${meta.evidence} 不一致`);
    }
  }
  for (const key of links.keys()) {
    if (!cards.has(key)) fail(mapRel, null, `SVG 指向非卡片：${key.slice('_digested/'.length)}`);
  }
}

// ---------- 领域册的“全部 ★★★”必须真的全 3 星 ----------
for (const domain of domains) {
  const readme = `_digested/view_${domain}/README.md`;
  const text = textsByFile.get(readme) || '';
  if (!text.includes('全部 ★★★')) continue;
  const weak = [...cards].filter(([rel, meta]) =>
    rel.startsWith(`_digested/view_${domain}/`) && meta.evidence !== '3');
  for (const [rel] of weak) {
    fail(readme, null, `写了“全部 ★★★”，但 ${rel} 是 ★★ 参考卡`);
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
