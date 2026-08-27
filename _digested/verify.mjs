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

if (failures.length) {
  console.error(`✗ ${failures.length} 个问题`);
  for (const f of failures) console.error('  ' + f);
  process.exit(1);
}
console.log(`✓ ${mdFiles.length} 个 Markdown 文件全部通过`);
