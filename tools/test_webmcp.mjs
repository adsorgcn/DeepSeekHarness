import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import test from 'node:test';

const source = await readFile(new URL('../docs/agent-tools.js', import.meta.url), 'utf8');

function load({ api = true, onDocument = true, status = 200 } = {}) {
  const calls = [], registered = [], events = {};
  const context = api ? { registerTool(tool, options) { registered.push({ tool, options }); return Promise.resolve(); } } : undefined;
  const sandbox = {
    document: onDocument && context ? { modelContext: context } : {},
    navigator: !onDocument && context ? { modelContext: context } : {},
    AbortController, setTimeout, clearTimeout, console,
    addEventListener(name, handler) { events[name] = handler; },
    async fetch(path, options) {
      calls.push({ path, options });
      return { ok: status === 200, status, json: async () => path.startsWith('/api/install') ? {
        platform: 'windows', prompt: 'official installation prompt', executesInstallation: false
      } : {
        marketUrl: 'https://dsh.ilang.guide/market/', source: 'https://dsh.ilang.guide/market/registry.json',
        entries: [{ name: 'deai', description: { zh: '去 AI 味' }, kind: 'skill' }, { name: 'mem-forever', title: { zh: '记忆体' }, kind: 'skill' }]
      } };
    }
  };
  vm.runInNewContext(source, sandbox, { filename: 'agent-tools.js' });
  const tool = name => registered.find(entry => entry.tool.name === name).tool;
  return { registered, calls, events, sandbox, tool };
}

test('registers two read-only tools using modern Document or legacy Navigator API', () => {
  for (const onDocument of [true, false]) {
    const { registered } = load({ onDocument });
    assert.equal(registered.length, 2);
    assert.ok(registered.every(entry => entry.tool.annotations.readOnlyHint));
  }
});

test('does not manufacture a browser API when WebMCP is unavailable', () => {
  const result = load({ api: false });
  assert.equal(result.registered.length, 0);
  assert.equal(result.sandbox.document.modelContext, undefined);
  assert.equal(result.sandbox.navigator.modelContext, undefined);
  assert.equal(result.calls.length, 0);
});

test('installation tool only reads the requested platform instructions', async () => {
  const result = load();
  const data = await result.tool('dsh_install_instructions').execute({ platform: 'windows' });
  assert.equal(data.executesInstallation, false);
  assert.equal(data.prompt, 'official installation prompt');
  assert.equal(result.calls.length, 1);
  assert.equal(result.calls[0].path, '/api/install?platform=windows');
});

test('market search filters Chinese titles and English identifiers without changing records', async () => {
  const search = load().tool('dsh_search_skills');
  assert.equal((await search.execute({ query: '记忆' })).entries[0].name, 'mem-forever');
  assert.equal((await search.execute({ query: 'DEAI' })).entries[0].name, 'deai');
  assert.equal((await search.execute({ query: 'no-match' })).entries.length, 0);
  assert.equal((await search.execute({})).entries.length, 2);
});

test('invalid and additional arguments cannot trigger a request', async () => {
  const result = load();
  await assert.rejects(result.tool('dsh_install_instructions').execute({ platform: 'https://evil.example/' }));
  await assert.rejects(result.tool('dsh_search_skills').execute({ query: 'x'.repeat(161) }));
  await assert.rejects(result.tool('dsh_search_skills').execute({ url: 'https://evil.example/' }));
  await assert.rejects(result.tool('dsh_search_skills').execute(null));
  assert.equal(result.calls.length, 0);
});

test('HTTP errors are reported instead of presenting a successful tool result', async () => {
  const result = load({ status: 503 });
  await assert.rejects(result.tool('dsh_install_instructions').execute({}), /HTTP 503/);
});

test('page lifecycle unregisters tools and restores them after BFCache navigation', () => {
  const result = load();
  result.events.pagehide();
  assert.ok(result.registered.every(entry => entry.options.signal.aborted));
  result.events.pageshow({ persisted: true });
  assert.equal(result.registered.length, 4);
  assert.ok(!result.registered[2].options.signal.aborted);
});
