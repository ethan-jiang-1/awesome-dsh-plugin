// R4 child: one "process" that reads a team record, waits, then writes it back.
// Used to show whether the plugin's lock serializes across OS processes.
import { readFileSync } from 'node:fs';
import { setTimeout as sleep } from 'node:timers/promises';
import { pathToFileURL } from 'node:url';

const args = Object.fromEntries(
  process.argv.slice(2).map((a) => {
    const [k, ...v] = a.replace(/^--/, '').split('=');
    return [k, v.join('=')];
  }),
);

const mod =
  args.module === 'at'
    ? await import(pathToFileURL(`${args.pkgs}/at/lib/state.js`).href)
    : await import(pathToFileURL(`${args.pkgs}/tx/lib/state.js`).href);

const { root, team, member } = args;
const delay = Number(args.delay ?? 0);

await mod.withTeamLock(`team:${root}:${team}`, async () => {
  const state = mod.readTeamSync(root, team); // read inside the lock
  state.members.push({
    id: `s-${member}`,
    name: member,
    joinedAt: Date.now(),
    status: 'idle',
  });
  await sleep(delay); // widen the read-modify-write window
  await mod.writeTeam(root, state); // atomic rename, no cross-process merge
});

console.log(`child ${member} wrote ${readFileSync(`${root}/${team}/team.json`, 'utf8').length} bytes`);
