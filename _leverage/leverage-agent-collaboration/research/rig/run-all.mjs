// Deterministic rig for the collaboration book (B2).
// Runs R0..R7 and writes out/results.json. No DSH process, no user profile,
// no model calls: only the published plugin artifacts + git + temp dirs.
import fs from 'node:fs/promises';
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync, spawn } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, '../../../..');
const RIG = path.join(REPO, '.work', 'collab-rig');
const TMP = path.join(RIG, 'tmp');
const OUT = path.join(RIG, 'out');
const PKGS = path.join(RIG, 'pkgs');
await fs.mkdir(TMP, { recursive: true });
await fs.mkdir(OUT, { recursive: true });

const results = {};
const rec = (id, data) => {
  results[id] = data;
  console.log(`\n## ${id}\n${JSON.stringify(data, null, 2)}`);
};
const sha256 = (file) => crypto.createHash('sha256').update(readFileSync(file)).digest('hex');
const tmpDir = async (prefix) => fs.mkdtemp(path.join(TMP, prefix));

// ---------- R0: environment + artifact provenance ----------
rec('R0', {
  node: process.version,
  platform: `${process.platform} ${process.arch}`,
  git: execFileSync('git', ['--version'], { encoding: 'utf8' }).trim(),
  artifacts: ['dsh-file-claim-0.2.0.tgz', 'dsh-teams-x-0.2.0.tgz', 'nanmicoder-dsh-agent-teams-0.1.28.tgz', 'dsh-taskswarm2-0.2.38.tgz'].map((f) => ({
    file: f,
    sha256: sha256(path.join(PKGS, f)),
  })),
});

const fc = await import(pathToFileURL(path.join(PKGS, 'fc/claim.mjs')).href);
const fcPlugin = (await import(pathToFileURL(path.join(PKGS, 'fc/index.mjs')).href)).default;

// ---------- R1: claim path scoping (pure functions of the published artifact) ----------
{
  const pairs = [
    ['exact', 'src/a.ts', 'src/a.ts'],
    ['case-insensitive', 'Src/A.TS', 'src/a.ts'],
    ['dir covers child', 'src', 'src/deep/b.ts'],
    ['child covered by dir', 'src/deep/b.ts', 'src'],
    ['prefix is not a directory', 'src/a.ts', 'src/a.ts.bak'],
    ['prefix reverse', 'src/a.ts.bak', 'src/a.ts'],
    ['root covers all', '.', 'anything/at/all'],
    ['different top dirs', 'src/a.ts', 'lib/a.ts'],
  ];
  const root = await tmpDir('r1-');
  rec('R1', {
    overlaps: pairs.map(([label, a, b]) => ({ label, a, b, overlap: fc.claimsOverlap(a, b) })),
    pathConflict: fc.pathConflict(['src'], ['src/x.ts']),
    norm: {
      rel: fc.normPath('src/a.ts', root),
      dot: fc.normPath('.', root),
      escape: fc.normPath('../outside.txt', root),
      absolute: fc.normPath('/etc/passwd', root),
    },
  });
}

// ---------- R2: stale / corrupt / orphan sidecars ----------
{
  const root = await tmpDir('r2-');
  const now = Date.now();
  const sidecar = (rel, data) => fs.writeFile(fc.claimSidecarPath(root, rel), JSON.stringify(data), 'utf8');
  await sidecar('a.txt', { tag: 's-other', files: ['a.txt'], startedAt: now - 1000, lastSeenAt: now - 1000 });
  await sidecar('b.txt', { tag: 's-other', files: ['b.txt'], startedAt: now - 900000, lastSeenAt: now - 900000 });
  await fs.writeFile(fc.claimSidecarPath(root, 'c.txt'), '{not json', 'utf8');
  await sidecar('d.txt', { tag: 's-other', files: ['d.txt'], startedAt: now, lastSeenAt: now, pid: 999999 });

  const hits = await fc.guardHits(root, ['a.txt', 'b.txt', 'c.txt', 'd.txt'], { tag: 's-me', now, staleMs: 300000 });
  let corruptRead;
  try {
    corruptRead = { ok: true, value: await fc.readClaim(root, 'c.txt') };
  } catch (error) {
    corruptRead = { ok: false, error: error.message.slice(0, 120) };
  }
  rec('R2', {
    hits,
    corruptRead,
    missingRead: await fc.readClaim(root, 'missing.txt'),
    staleMs: fc.staleMsOf({}),
  });
}

// ---------- R3: is the deny actually wired into tools/pre-execute? ----------
{
  const root = await tmpDir('r3-');
  const now = Date.now();
  await fs.writeFile(fc.claimSidecarPath(root, 'a.txt'), JSON.stringify({ tag: 's-other', files: ['a.txt'], startedAt: now, lastSeenAt: now }), 'utf8');

  const handlers = [];
  const noop = () => () => {};
  const ctx = new Proxy(
    {
      on(name, fn) {
        if (name === 'tools/pre-execute') handlers.push(fn);
        return noop;
      },
      get() {
        return undefined;
      },
      effect(fn) {
        try {
          const d = fn();
          return typeof d === 'function' ? d : noop;
        } catch {
          return noop;
        }
      },
      tool: noop,
      command: noop,
      logger: { debug() {}, info() {}, warn() {}, error() {} },
    },
    { get: (t, k) => (k in t ? t[k] : noop) },
  );

  let applyError = null;
  try {
    fcPlugin.apply(ctx, {});
  } catch (error) {
    applyError = error.message;
  }

  const exec = (name, args, id) => ({
    name,
    arguments: args,
    agent: { id, session: { header: { cwd: root } } },
  });
  const allow = async () => ({ kind: 'next' });
  const call = async (name, args, id) => {
    const handler = handlers[0];
    if (!handler) return { skipped: 'no handler captured' };
    const out = await handler(exec(name, args, id), allow);
    return { kind: out.kind, reason: out.reason ? out.reason.slice(0, 60) : undefined };
  };

  rec('R3', {
    applyError,
    handlers: handlers.length,
    othersClaimedWrite: await call('write', { file_path: 'a.txt' }, 's-me'),
    selfClaimedWrite: await call('write', { file_path: 'a.txt' }, 's-other'),
    otherClaimedEdit: await call('edit', { file_path: 'a.txt' }, 's-me'),
    readTool: await call('read', { file_path: 'a.txt' }, 's-me'),
    unclaimedWrite: await call('write', { file_path: 'z.txt' }, 's-me'),
    shellRedirect: await call('bash', { command: 'echo hi > a.txt' }, 's-me'),
  });
}

// ---------- R4: cross-process lost update under each plugin's own lock ----------
async function lostUpdate(modName) {
  const dir = await tmpDir(`r4-${modName}-`);
  const team = 'team1';
  const mod = modName === 'at' ? await import(pathToFileURL(path.join(PKGS, 'at/lib/state.js')).href) : await import(pathToFileURL(path.join(PKGS, 'tx/lib/state.js')).href);
  await fs.mkdir(path.join(dir, team), { recursive: true });
  const now = Date.now();
  await mod.writeTeam(dir, { id: team, name: 't', captainSessionId: 's-captain', createdAt: now, members: [], tasks: [], taskSeq: 0 });

  const run = (member) =>
    new Promise((resolve) => {
      const child = spawn(process.execPath, [path.join(HERE, '_child.mjs'), `--module=${modName}`, `--pkgs=${PKGS}`, `--root=${dir}`, `--team=${team}`, `--member=${member}`, '--delay=250'], { stdio: 'ignore' });
      child.on('exit', (code) => resolve(code));
    });
  const a = run('alpha');
  await new Promise((r) => setTimeout(r, 40));
  const b = run('beta');
  const codes = await Promise.all([a, b]);
  const final = JSON.parse(await fs.readFile(path.join(dir, team, 'team.json'), 'utf8'));
  return {
    module: modName,
    exitCodes: codes,
    members: final.members.map((m) => m.name),
    lostUpdate: final.members.length === 1,
  };
}
rec('R4a', await lostUpdate('at'));
rec('R4b', await lostUpdate('tx'));

// ---------- R5: does the published artifact even contain a cross-process lock? ----------
{
  const state = readFileSync(path.join(PKGS, 'tx/lib/state.js'), 'utf8');
  const lockNeedles = ['DSH_TEAMSX_FILE_LOCK', 'flock', '.lock', 'locks/'];
  const lockHits = lockNeedles.filter((n) => state.includes(n));
  const versions = execFileSync('npm', ['view', 'dsh-teams-x', 'versions', '--json'], {
    encoding: 'utf8',
    env: { ...process.env, npm_config_cache: path.join(RIG, '..', 'npm-cache') },
  }).trim();
  rec('R5', {
    artifactVersion: JSON.parse(readFileSync(path.join(PKGS, 'tx/package.json'), 'utf8')).version,
    lockNeedles: lockNeedles.map((n) => ({ needle: n, found: state.includes(n) })),
    atomicTempUsesWx: state.includes("'wx'"),
    versions,
    hasCrossProcessLock: lockHits.length > 0,
  });
}

// ---------- R6: task wave scheduling (dsh-taskswarm2 artifact) ----------
{
  const ts = await import(pathToFileURL(path.join(PKGS, 'ts/lib/core/discover.js')).href);
  const task = (id, deps) => ({ id, deps });
  const normal = ts.buildWaves([task('a', []), task('b', ['a']), task('c', ['a']), task('d', ['b', 'c'])]);
  const cycle = ts.buildWaves([task('x', ['y']), task('y', ['x'])]);
  const missing = ts.buildWaves([task('e', ['zzz'])]);
  rec('R6', {
    normal: normal.waves.map((w) => w.map((t) => t.id)),
    cycle: cycle.waves.map((w) => w.map((t) => t.id)),
    missing: missing.waves.map((w) => w.map((t) => t.id)),
    unresolved: Object.fromEntries(missing.unresolvedDeps),
  });
}

// ---------- R7: what a git worktree actually isolates ----------
{
  const base = await tmpDir('r7-');
  const repo = path.join(base, 'repo');
  const wt = path.join(base, 'wt');
  await fs.mkdir(repo);
  const git = (args, cwd = repo) =>
    execFileSync('git', args, {
      cwd,
      encoding: 'utf8',
      env: { ...process.env, GIT_AUTHOR_NAME: 'rig', GIT_AUTHOR_EMAIL: 'rig@example.invalid', GIT_COMMITTER_NAME: 'rig', GIT_COMMITTER_EMAIL: 'rig@example.invalid' },
    }).trim();
  git(['init', '-q']);
  await fs.writeFile(path.join(repo, 'tracked.txt'), 'base\n');
  await fs.writeFile(path.join(repo, '.gitignore'), 'ignored.txt\n');
  await fs.writeFile(path.join(repo, 'untracked.txt'), 'u\n');
  await fs.writeFile(path.join(repo, 'ignored.txt'), 'i\n');
  git(['add', 'tracked.txt', '.gitignore']);
  git(['commit', '-q', '-m', 'base']);
  git(['worktree', 'add', '-q', wt, '-b', 'lane']);
  const before = {
    trackedPresent: existsSync(path.join(wt, 'tracked.txt')),
    trackedContent: await fs.readFile(path.join(wt, 'tracked.txt'), 'utf8'),
    untrackedAbsent: !existsSync(path.join(wt, 'untracked.txt')),
    ignoredAbsent: !existsSync(path.join(wt, 'ignored.txt')),
    dotGitIsFilePointer: readFileSync(path.join(wt, '.git'), 'utf8').startsWith('gitdir:'),
  };
  await fs.appendFile(path.join(wt, 'tracked.txt'), 'lane-edit\n');
  const mainCopy = await fs.readFile(path.join(repo, 'tracked.txt'), 'utf8');
  git(['worktree', 'remove', '--force', wt]);
  rec('R7', {
    ...before,
    mainCopyUnchanged: mainCopy === 'base\n',
    branchAfterRemove: git(['branch', '--list', 'lane']),
  });
}

await fs.writeFile(path.join(OUT, 'results.json'), JSON.stringify(results, null, 2));
console.log(`\nwrote ${path.join(OUT, 'results.json')}`);
