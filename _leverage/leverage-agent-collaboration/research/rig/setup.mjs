// Fetch and unpack the pinned artifacts the rig measures.
// Writes only under <repo>/.work/collab-rig (gitignored). No install, no build,
// no DSH process: `npm pack` + tar extraction + sha256 check.
import fs from 'node:fs/promises';
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, '../../../..');
const RIG = path.join(REPO, '.work', 'collab-rig');
const PKGS = path.join(RIG, 'pkgs');
const CACHE = path.join(REPO, '.work', 'npm-cache');

const ARTIFACTS = [
  { pkg: 'dsh-file-claim', version: '0.2.0', dir: 'fc', file: 'dsh-file-claim-0.2.0.tgz', sha256: '45bd87bc6cbb566278f3c8b1510ecd028817f8bb5365b1a8c8bd7e6b741a61db' },
  { pkg: 'dsh-teams-x', version: '0.2.0', dir: 'tx', file: 'dsh-teams-x-0.2.0.tgz', sha256: 'a546b43f773ea782a0df00d5bd4f9c4928e5e5aa63efa50dcaf52d94f618b547' },
  { pkg: '@nanmicoder/dsh-agent-teams', version: '0.1.28', dir: 'at', file: 'nanmicoder-dsh-agent-teams-0.1.28.tgz', sha256: '6d4e65144c9af5a34deec2d34e7e218ff71b35725f4886609eaf5f30c7791928' },
  { pkg: 'dsh-taskswarm2', version: '0.2.38', dir: 'ts', file: 'dsh-taskswarm2-0.2.38.tgz', sha256: 'f522cabf16d53f488dfc8a79a5e8948c754a28d88e0b355f232f1fbb12d2e656' },
];

const sha256 = (file) => crypto.createHash('sha256').update(readFileSync(file)).digest('hex');

await fs.mkdir(PKGS, { recursive: true });
await fs.mkdir(CACHE, { recursive: true });

for (const a of ARTIFACTS) {
  const tgz = path.join(PKGS, a.file);
  const dir = path.join(PKGS, a.dir);

  if (!existsSync(tgz)) {
    console.log(`pack ${a.pkg}@${a.version}`);
    execFileSync('npm', ['pack', `${a.pkg}@${a.version}`, '--pack-destination', PKGS], {
      env: { ...process.env, npm_config_cache: CACHE },
      stdio: 'pipe',
    });
  }
  if (!existsSync(tgz)) throw new Error(`missing tarball after npm pack: ${a.file}`);

  const actual = sha256(tgz);
  if (actual !== a.sha256) {
    throw new Error(`sha256 mismatch for ${a.file}\n  expected ${a.sha256}\n  actual   ${actual}`);
  }

  const pj = path.join(dir, 'package.json');
  const current = existsSync(pj) ? JSON.parse(readFileSync(pj, 'utf8')).version : undefined;
  if (current !== a.version) {
    await fs.rm(dir, { recursive: true, force: true });
    await fs.mkdir(dir, { recursive: true });
    execFileSync('tar', ['-xzf', tgz, '-C', dir, '--strip-components=1'], { stdio: 'pipe' });
    console.log(`unpack ${a.dir} <- ${a.file}`);
  } else {
    console.log(`skip   ${a.dir} (already ${a.version})`);
  }
}

console.log(`\nready: ${PKGS}`);
console.log('next:  node run-all.mjs');
