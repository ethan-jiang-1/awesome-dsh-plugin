#!/usr/bin/env node
// 研究材料自校验：严格 UTF-8、LF 换行与单个结尾换行、Markdown 相对链接与锚点存在性。
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
(function walk(dir) {
  for (const name of readdirSync(join(repoRoot, dir), { withFileTypes: true })) {
    const rel = join(dir, name.name);
    if (name.isDirectory()) walk(rel);
    else if (name.name.endsWith('.md')) mdFiles.push(rel);
  }
})(roots[0]);
(function walk(dir) {
  for (const name of readdirSync(join(repoRoot, dir), { withFileTypes: true })) {
    const rel = join(dir, name.name);
    if (name.isDirectory()) walk(rel);
    else if (name.name.endsWith('.md')) mdFiles.push(rel);
  }
})(roots[1]);

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

// ---------- leverage：frontmatter 契约 ----------
const LEVERAGE_PREFIX = '_digested/leverage/';
const DOMAIN_BY_DIR = {
  'lever-reshape-product': 'reshape-product',
  'lever-cross-boundary': 'cross-boundary',
  'lever-prove-output': 'prove-output',
  'lever-draw-limit': 'draw-limit',
};
const KINDS = new Set(['index', 'charter', 'guide', 'playbook', 'card', 'sample', 'evidence']);
const STATUSES = new Set(['observed', 'inferred', 'open', 'living']);
const FM_REQUIRED = ['title', 'domain', 'kind', 'positioning', 'read_when', 'status', 'updated'];
const TAKEAWAY_REQUIRED = new Set(['card', 'sample', 'playbook']);
const BORROW_HEADING = /^#{2,3} .*(借鉴|搬走|借用|照抄|食谱|配方|移植)/m;

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
  if (!rel.startsWith(LEVERAGE_PREFIX)) continue;
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

  const rest = rel.slice(LEVERAGE_PREFIX.length);
  const dir = rest.includes('/') ? rest.split('/')[0] : '';
  const expectedDomain = DOMAIN_BY_DIR[dir] ?? 'layer';
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
