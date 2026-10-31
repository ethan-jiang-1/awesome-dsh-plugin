#!/usr/bin/env node
// catalog.mjs — 从每篇 Markdown 的 frontmatter 生成 catalog.md（零依赖）
//
// 用法（在仓库根执行）：
//   node _digested/leverage/catalog.mjs            # 重新生成 catalog.md
//   node _digested/leverage/catalog.mjs --check    # 只校验是否过期（过期 exit 1）
//   node _digested/leverage/catalog.mjs --stats    # 打印角色分布、行数与预算
//
// 纪律：catalog 是生成物，不手改。新增/修改任何 frontmatter 后重跑本脚本；
// verify.mjs 只校验 frontmatter 本身，不负责这份清单是否新鲜。

import { readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { dirname, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const SELF = join(HERE, 'catalog.md');
const SELF_REL = 'catalog.md';

const DOMAINS = [
  ['layer', '层共享件'],
  ['reshape-product', 'RESHAPE · 产品形态'],
  ['cross-boundary', 'CROSS · 协作边界'],
  ['prove-output', 'PROVE · 质量门禁'],
  ['draw-limit', 'LIMIT · 安全监管链'],
];
const DOMAIN_SET = new Set(DOMAINS.map(([d]) => d));

const KINDS = ['charter', 'index', 'guide', 'playbook', 'card', 'sample', 'evidence'];
const KIND_ORDER = new Map(KINDS.map((k, i) => [k, i]));
const STATUS = new Set(['observed', 'inferred', 'open', 'living']);
const DOMAIN_LABEL = new Map(DOMAINS);
const REQUIRED = ['title', 'domain', 'kind', 'positioning', 'read_when', 'status', 'updated'];
const TAKEAWAY_REQUIRED = new Set(['card', 'sample', 'playbook']);

const SELF_META = {
  title: 'catalog · 全量文件清单',
  domain: 'layer',
  kind: 'index',
  positioning: '全部 Markdown 的 kind、定位、能拿走什么、什么时候读（本文件由脚本生成）。',
  takeaway: '',
  read_when: '想一次看全所有文件，或按关键词找入口。',
  status: 'living',
};

function walk(dir, out = []) {
  for (const name of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, name.name);
    if (name.isDirectory()) walk(p, out);
    else if (name.name.endsWith('.md')) out.push(p);
  }
  return out;
}

function relPath(abs) {
  return relative(HERE, abs).split(sep).join('/');
}

// 只解析本仓库自己写的那套扁平 YAML：key: value，值可用双引号包。
function parseFrontmatter(abs) {
  const text = readFileSync(abs, 'utf8');
  if (!text.startsWith('---\n')) throw new Error(`${relPath(abs)}: 缺 frontmatter`);
  const end = text.indexOf('\n---\n', 4);
  if (end < 0) throw new Error(`${relPath(abs)}: frontmatter 未闭合`);
  const meta = {};
  for (const line of text.slice(4, end).split('\n')) {
    if (!line.trim()) continue;
    const m = line.match(/^([A-Za-z_][A-Za-z0-9_]*):[ \t]*(.*)$/);
    if (!m) throw new Error(`${relPath(abs)}: 无法解析 frontmatter 行: ${line}`);
    const [, key, raw] = m;
    let value = raw.trim();
    if (value.startsWith('"')) {
      try {
        value = JSON.parse(value);
      } catch {
        throw new Error(`${relPath(abs)}: ${key} 的引号值不是合法 JSON 转义: ${raw}`);
      }
    } else if (value === '') {
      value = '';
    }
    meta[key] = value;
  }
  return { meta, text };
}

function naturalCompare(a, b) {
  return a.localeCompare(b, 'zh', { numeric: true, sensitivity: 'base' });
}

function cell(v) {
  const s = (v ?? '').toString().trim();
  return (s === '' ? '—' : s).replace(/\|/g, '\\|');
}

function lineCount(text) {
  return text.split('\n').length - (text.endsWith('\n') ? 1 : 0);
}

function load() {
  const entries = [];
  for (const abs of walk(HERE)) {
    const rel = relPath(abs);
    if (rel === SELF_REL) continue;
    const { meta, text } = parseFrontmatter(abs);
    entries.push({ path: rel, meta, lines: lineCount(text) });
  }
  entries.push({ path: SELF_REL, meta: SELF_META, lines: 0, self: true });
  const rank = (e) => {
    if (/(^|\/)README\.md$/.test(e.path)) return 0;
    if (e.path === 'BORROW.md') return 1;
    return 10 + (KIND_ORDER.get(e.meta.kind) ?? 99);
  };
  entries.sort((a, b) => {
    const ra = rank(a);
    const rb = rank(b);
    if (ra !== rb) return ra - rb;
    return naturalCompare(a.path, b.path);
  });
  return entries;
}

function maxUpdated(entries) {
  const dates = entries.filter((e) => !e.self).map((e) => e.meta.updated).filter(Boolean).sort();
  return dates.length ? dates[dates.length - 1] : '1970-01-01';
}

function render(entries) {
  const counts = Object.fromEntries(KINDS.map((k) => [k, 0]));
  for (const e of entries) counts[e.meta.kind] = (counts[e.meta.kind] ?? 0) + 1;
  const kindLine = KINDS.filter((k) => counts[k]).map((k) => `${k} ${counts[k]}`).join(' · ');

  const fm = [
    '---',
    `title: "${SELF_META.title}"`,
    'domain: layer',
    'kind: index',
    `positioning: "${SELF_META.positioning}"`,
    `read_when: "${SELF_META.read_when}"`,
    'status: living',
    `updated: ${maxUpdated(entries)}`,
    '---',
  ].join('\n');

  const lines = [
    fm,
    '# catalog · 全量文件清单',
    '',
    '> **这是生成物，不要手改。** 改任何一个文件的 frontmatter 之后运行 `node _digested/leverage/catalog.mjs`。',
    '> 校验：`--check`（过期即失败） · 统计：`--stats`（角色分布、行数、超预算）。',
    `> **共 ${entries.length} 篇**：${kindLine}。`,
    '',
    '**六列怎么用**：`定位`答「它是什么」，`能拿走什么`答「值不值得打开」，`什么时候读`用任务词写，能直接 grep。',
    '',
  ];

  for (const [domain, label] of DOMAINS) {
    const rows = entries.filter((e) => e.meta.domain === domain);
    if (!rows.length) continue;
    lines.push(`## ${label} ｜ \`${domain}\``, '');
    lines.push('| 文件 | kind | 定位 | 能拿走什么 | 什么时候读 | 状态 |');
    lines.push('|---|---|---|---|---|---|');
    for (const e of rows) {
      const label2 = e.self ? 'catalog.md（本文件）' : `\`${e.path.split('/').pop()}\``;
      const href = e.self ? './catalog.md' : `./${e.path}`;
      lines.push(
        `| [${label2}](${href}) | ${e.meta.kind} | ${cell(e.meta.positioning)} | ${cell(e.meta.takeaway)} | ${cell(e.meta.read_when)} | ${e.meta.status} |`,
      );
    }
    lines.push('');
  }

  const other = entries.filter((e) => !DOMAIN_SET.has(e.meta.domain));
  if (other.length) {
    lines.push('## 未归类', '', '| 文件 | domain | kind | 定位 |', '|---|---|---|---|');
    for (const e of other) lines.push(`| \`${e.path}\` | ${e.meta.domain} | ${e.meta.kind} | ${cell(e.meta.positioning)} |`);
    lines.push('');
  }

  return lines.join('\n').replace(/\n+$/, '\n');
}

function main() {
  const args = process.argv.slice(2);
  const entries = load();
  const out = render(entries);

  if (args.includes('--stats')) {
    const byKind = Object.fromEntries(KINDS.map((k) => [k, 0]));
    const byDomain = {};
    let over = 0;
    for (const e of entries) {
      byKind[e.meta.kind] = (byKind[e.meta.kind] ?? 0) + 1;
      byDomain[e.meta.domain] = (byDomain[e.meta.domain] ?? 0) + 1;
      if (e.meta.budget) {
        const budget = Number(e.meta.budget);
        if (Number.isFinite(budget) && e.lines > budget) {
          over += 1;
          console.log(`超出预算: ${e.path}  ${e.lines}/${budget} 行`);
        }
      }
    }
    console.log(`文件: ${entries.length}`);
    console.log('角色: ' + KINDS.filter((k) => byKind[k]).map((k) => `${k} ${byKind[k]}`).join(' · '));
    console.log('分域: ' + DOMAINS.filter(([d]) => byDomain[d]).map(([d]) => `${d} ${byDomain[d]}`).join(' · '));
    console.log(`超预算: ${over}`);
    return;
  }

  if (args.includes('--check')) {
    let current = '';
    try {
      current = readFileSync(SELF, 'utf8');
    } catch {
      console.error('✗ catalog.md 不存在，先运行 node _digested/leverage/catalog.mjs');
      process.exit(1);
    }
    if (current !== out) {
      const a = current.split('\n');
      const b = out.split('\n');
      const i = a.findIndex((line, idx) => line !== b[idx]);
      console.error('✗ catalog.md 已过期（frontmatter 变了但清单没重生成）');
      console.error(`  第一处差异在第 ${i + 1} 行：`);
      console.error(`  现有: ${JSON.stringify(a[i] ?? '')}`);
      console.error(`  应为: ${JSON.stringify(b[i] ?? '')}`);
      process.exit(1);
    }
    console.log(`✓ catalog.md 是最新的（${entries.length} 篇）`);
    return;
  }

  writeFileSync(SELF, out, 'utf8');
  console.log(`✓ 已生成 catalog.md（${entries.length} 篇）`);
}

main();
