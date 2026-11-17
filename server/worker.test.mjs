import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createHandler, markdownForHttp } from './worker.mjs';
import { DOCUMENTS, RAW_ROOT, SITE_URL } from './content.mjs';

const root = new URL('../', import.meta.url);
const fetched = [];
async function fixtureFetch(url) {
  fetched.push(String(url));
  assert.ok(String(url).startsWith(RAW_ROOT), 'All content reads stay on the fixed public origin');
  const path = decodeURIComponent(String(url).slice(RAW_ROOT.length));
  try { return new Response(await readFile(new URL(path, root))); }
  catch { return new Response('not found', { status: 404 }); }
}
const handler = createHandler(fixtureFetch);
const headers = { 'Content-Type': 'application/json', Accept: 'application/json, text/event-stream', 'MCP-Protocol-Version': '2025-11-25' };
async function rpc(method, params = {}, custom = {}) {
  const request = new Request(`${SITE_URL}/mcp`, { method: 'POST', headers: { ...headers, ...custom.headers }, body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, params }) });
  const response = await handler(request);
  return { response, body: await response.json() };
}
async function modernRpc(method, params = {}, custom = {}) {
  const meta = { 'io.modelcontextprotocol/protocolVersion': '2026-07-28', 'io.modelcontextprotocol/clientCapabilities': {}, 'io.modelcontextprotocol/clientInfo': { name: 'test', version: '1' } };
  const body = { jsonrpc: '2.0', id: 42, method, params: { ...params, _meta: { ...meta, ...custom.meta } } };
  const requestHeaders = { ...headers, 'MCP-Protocol-Version': '2026-07-28', 'Mcp-Method': method, ...(['tools/call', 'prompts/get'].includes(method) ? { 'Mcp-Name': params.name } : method === 'resources/read' ? { 'Mcp-Name': params.uri } : {}), ...custom.headers };
  for (const key of custom.removeHeaders || []) delete requestHeaders[key];
  const response = await handler(new Request(`${SITE_URL}/mcp`, { method: 'POST', headers: requestHeaders, body: JSON.stringify(body) }));
  return { response, body: await response.json() };
}

test('modern discovery and inline tool calls require no initialization or session', async () => {
  const { response, body } = await modernRpc('server/discover');
  assert.equal(response.status, 200);
  assert.equal(body.result.resultType, 'complete');
  assert.deepEqual(body.result.supportedVersions, ['2026-07-28', '2025-11-25', '2025-06-18']);
  assert.equal(body.result._meta['io.modelcontextprotocol/serverInfo'].name, 'ilang-dsh-toolkit');
  assert.equal(response.headers.has('mcp-session-id'), false);
  const { body: result } = await modernRpc('tools/call', { name: 'dsh_overview', arguments: {} });
  assert.equal(result.result.resultType, 'complete');
  assert.equal(result.result.structuredContent.name, 'iLang DSH 工具包');
});

test('modern requests reject omitted capabilities and mismatched standard headers', async () => {
  const params = { name: 'dsh_overview', arguments: {} };
  const cases = [
    [{ meta: { 'io.modelcontextprotocol/clientCapabilities': null } }, -32602],
    [{ meta: { 'io.modelcontextprotocol/protocolVersion': undefined } }, -32602],
    [{ removeHeaders: ['Mcp-Method'] }, -32020],
    [{ removeHeaders: ['Mcp-Name'] }, -32020],
    [{ removeHeaders: ['MCP-Protocol-Version'] }, -32020],
    [{ headers: { 'Mcp-Method': 'tools/list' } }, -32020],
    [{ headers: { 'Mcp-Name': 'dsh_list_skills' } }, -32020],
    [{ headers: { 'MCP-Protocol-Version': '2025-11-25' } }, -32020],
    [{ headers: { 'Mcp-Name': '=?base64?invalid!?=' } }, -32020],
  ];
  for (const [custom, code] of cases) {
    const { response, body } = await modernRpc('tools/call', params, custom);
    assert.equal(response.status, 400);
    assert.equal(body.error.code, code);
  }
});

test('modern Mcp-Name accepts correctly encoded Base64 values and checks decoded equality', async () => {
  const { body } = await modernRpc('tools/call', { name: 'dsh_overview', arguments: {} }, { headers: { 'Mcp-Name': `=?base64?${btoa('dsh_overview')}?=` } });
  assert.equal(body.result.isError, false);
  const { response, body: bad } = await modernRpc('tools/call', { name: 'dsh_overview', arguments: {} }, { headers: { 'Mcp-Name': `=?base64?${btoa('another_tool')}?=` } });
  assert.equal(response.status, 400);
  assert.equal(bad.error.code, -32020);
});

test('unsupported modern versions expose supported versions and unknown methods use HTTP 404', async () => {
  const { response, body } = await modernRpc('server/discover', {}, { meta: { 'io.modelcontextprotocol/protocolVersion': '2999-01-01' }, headers: { 'MCP-Protocol-Version': '2999-01-01' } });
  assert.equal(response.status, 400);
  assert.equal(body.error.code, -32022);
  assert.equal(body.error.data.requested, '2999-01-01');
  assert.ok(body.error.data.supported.includes('2026-07-28'));
  const unknown = await modernRpc('unknown/method');
  assert.equal(unknown.response.status, 404);
  assert.equal(unknown.body.error.code, -32601);
  assert.equal((await modernRpc('initialize', { protocolVersion: '2026-07-28', capabilities: {}, clientInfo: {} })).response.status, 404);
});

test('legacy negotiation never selects the handshake-free revision', async () => {
  const { body } = await rpc('initialize', { protocolVersion: '2999-01-01', capabilities: {}, clientInfo: { name: 'old-client', version: '1' } });
  assert.equal(body.result.protocolVersion, '2025-11-25');
  assert.equal('resultType' in body.result, false);
});

test('initialization negotiates versions and exposes only implemented capabilities', async () => {
  const { response, body } = await rpc('initialize', { protocolVersion: '2025-06-18', capabilities: {}, clientInfo: { name: 'test', version: '1' } });
  assert.equal(response.status, 200);
  assert.equal(body.result.protocolVersion, '2025-06-18');
  assert.deepEqual(Object.keys(body.result.capabilities), ['tools', 'resources']);
  assert.equal(body.result.serverInfo.name, 'ilang-dsh-toolkit');
  assert.match(response.headers.get('link'), /api-catalog/);
});

test('all advertised tools execute successfully using real checked-in public sources', async () => {
  const { body: list } = await rpc('tools/list');
  assert.equal(list.result.tools.length, 5);
  const args = {
    dsh_overview: {}, dsh_install_instructions: { platform: 'windows' },
    dsh_search_docs: { query: '记忆', limit: 3 }, dsh_get_document: { path: 'README.md' }, dsh_list_skills: {},
  };
  for (const tool of list.result.tools) {
    assert.equal(tool.annotations.readOnlyHint, true);
    const { body } = await rpc('tools/call', { name: tool.name, arguments: args[tool.name] });
    assert.equal(body.result?.isError, false, `${tool.name}: ${JSON.stringify(body)}`);
    assert.deepEqual(JSON.parse(body.result.content[0].text), body.result.structuredContent);
  }
});

test('installation response preserves README prompt and does not execute the script', async () => {
  const before = fetched.length;
  const response = await handler(new Request(`${SITE_URL}/api/install?platform=windows`));
  const data = await response.json();
  const readme = await readFile(new URL('README.md', root), 'utf8');
  assert.ok(readme.includes(`> ${data.prompt}`));
  assert.match(data.prompt, /创造模式/);
  assert.equal(data.bootstrap.length, 1);
  assert.ok(data.bootstrap[0].url.endsWith('/bootstrap.ps1'));
  assert.equal(data.executesInstallation, false);
  assert.deepEqual(fetched.slice(before), [`${RAW_ROOT}README.md`]);
});

test('resources list and resource reads use the same exact document whitelist', async () => {
  const { body: list } = await rpc('resources/list');
  assert.equal(list.result.resources.length, DOCUMENTS.length);
  const { body: read } = await rpc('resources/read', { uri: list.result.resources[0].uri });
  assert.match(read.result.contents[0].text, /iLang DSH 工具包/);
  const { body: bad } = await rpc('resources/read', { uri: 'file:///etc/passwd' });
  assert.equal(bad.error.code, -32602);
});

test('untrusted paths, unknown arguments and invalid search limits cannot trigger fetches', async () => {
  const before = fetched.length;
  for (const args of [{ path: 'env/keys.env' }, { path: '../../README.md' }, { path: 'https://evil.test/a' }, { path: 'README.md', url: 'https://evil.test' }]) {
    const { body } = await rpc('tools/call', { name: 'dsh_get_document', arguments: args });
    assert.equal(body.error.code, -32602);
  }
  for (const args of [{ query: ' ', limit: 2 }, { query: 'a', limit: 0 }, { query: 'a', limit: 1.5 }, { query: 'a'.repeat(161) }]) {
    const { body } = await rpc('tools/call', { name: 'dsh_search_docs', arguments: args });
    assert.equal(body.error.code, -32602);
  }
  assert.equal(fetched.length, before);
});

test('MCP rejects malformed payloads and unsupported transport versions', async () => {
  const cases = [
    ['{', headers, 400],
    ['[]', headers, 400],
    ['{}', headers, 400],
    [JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'ping' }), { ...headers, 'MCP-Protocol-Version': '2999-01-01' }, 400],
    ['{}', { ...headers, Accept: 'application/json' }, 406],
    ['{}', { ...headers, 'Content-Type': 'text/plain' }, 415],
    ['{}', { ...headers, Origin: 'null' }, 403],
    ['{}', { ...headers, Origin: 'http://attacker.test' }, 403],
    ['x'.repeat(65537), headers, 413],
  ];
  for (const [body, requestHeaders, status] of cases) {
    const response = await handler(new Request(`${SITE_URL}/mcp`, { method: 'POST', headers: requestHeaders, body }));
    assert.equal(response.status, status);
  }
  assert.equal((await handler(new Request(`${SITE_URL}/mcp`))).status, 405);
});

test('MCP notifications return 202 without a JSON-RPC body', async () => {
  const response = await handler(new Request(`${SITE_URL}/mcp`, { method: 'POST', headers, body: JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized' }) }));
  assert.equal(response.status, 202);
  assert.equal(await response.text(), '');
});

test('source outages are visible as tool errors and partial-search diagnostics', async () => {
  const failing = createHandler(async () => new Response('offline', { status: 503 }));
  const request = new Request(`${SITE_URL}/mcp`, { method: 'POST', headers, body: JSON.stringify({ jsonrpc: '2.0', id: 9, method: 'tools/call', params: { name: 'dsh_get_document', arguments: { path: 'README.md' } } }) });
  const result = await (await failing(request)).json();
  assert.equal(result.result.isError, true);
  assert.match(result.result.content[0].text, /503/);
  const search = await (await failing(new Request(`${SITE_URL}/api/search?q=memory`))).json();
  assert.equal(search.results.length, 0);
  assert.equal(search.unavailable.length, DOCUMENTS.length);
});

test('HTML and Markdown negotiation preserve the page and declare Vary', async () => {
  const html = await handler(new Request(`${SITE_URL}/`));
  assert.match(html.headers.get('content-type'), /text\/html/);
  assert.match(await html.text(), /<!doctype html>/i);
  const md = await handler(new Request(`${SITE_URL}/`, { headers: { Accept: 'text/markdown' } }));
  assert.match(md.headers.get('content-type'), /text\/markdown/);
  assert.equal(md.headers.get('vary'), 'Accept');
  assert.match(await md.text(), /# iLang DSH 工具包/);
  const disabled = await handler(new Request(`${SITE_URL}/`, { headers: { Accept: 'text/markdown;q=0, text/html' } }));
  assert.match(disabled.headers.get('content-type'), /text\/html/);
  assert.equal(await (await handler(new Request(`${SITE_URL}/`, { method: 'HEAD' }))).text(), '');
});

test('HTTP Markdown resolves repository links while MCP resources retain original bytes', async () => {
  const homepage = await (await handler(new Request(`${SITE_URL}/`, { headers: { Accept: 'text/markdown' } }))).text();
  assert.ok(homepage.includes('https://github.com/adsorgcn/DeepSeekHarness/blob/main/' + encodeURIComponent('插件点评-ilang视角.md')));
  assert.ok(homepage.includes(`${RAW_ROOT}assets/social-preview.png`));
  const install = await (await handler(new Request(`${SITE_URL}/${encodeURIComponent('一键安装.md')}`))).text();
  assert.ok(install.includes('https://github.com/adsorgcn/DeepSeekHarness/blob/main/docs/LEDGER.md'));
  const original = await readFile(new URL('README.md', root), 'utf8');
  const { body } = await rpc('resources/read', { uri: `dsh://docs/${encodeURIComponent('README.md')}` });
  assert.equal(body.result.contents[0].text, original);
});

test('Markdown URL rewriting respects source subdirectories and leaves code examples intact', () => {
  const input = '[guide](../README.md#start)\n[ref]: ../README.md\n![photo](../assets/image.png)\n`[sample](relative.md)`\n```md\n[sample](relative.md)\n```\n[external](https://example.com/)\n';
  const rendered = markdownForHttp(input, 'docs/PASTE.md');
  assert.ok(rendered.includes('[guide](https://github.com/adsorgcn/DeepSeekHarness/blob/main/README.md#start)'));
  assert.ok(rendered.includes('[ref]: https://github.com/adsorgcn/DeepSeekHarness/blob/main/README.md'));
  assert.ok(rendered.includes(`![photo](${RAW_ROOT}assets/image.png)`));
  assert.ok(rendered.includes('`[sample](relative.md)`'));
  assert.ok(rendered.includes('```md\n[sample](relative.md)\n```'));
  assert.ok(rendered.includes('[external](https://example.com/)'));
});

test('HTTP API rejects unsupported methods and query arguments', async () => {
  assert.equal((await handler(new Request(`${SITE_URL}/api/install?os=linux`))).status, 400);
  assert.equal((await handler(new Request(`${SITE_URL}/api/search?q=abc&limit=999`))).status, 400);
  assert.equal((await handler(new Request(`${SITE_URL}/api/docs?path=env/keys.env`))).status, 400);
  assert.equal((await handler(new Request(`${SITE_URL}/api/unknown`))).status, 404);
  assert.equal((await handler(new Request(`${SITE_URL}/api/skills`, { method: 'POST' }))).status, 405);
});

test('asset origin cannot point back at the public host', async () => {
  const response = await handler(new Request(`${SITE_URL}/redesign.css`), { STATIC_ORIGIN: `${SITE_URL}/` });
  assert.equal(response.status, 503);
});

test('all outbound fetches use Workers-supported manual redirects and reject 3xx without following', async () => {
  const requests = [];
  const redirecting = createHandler(async (url, init) => {
    // Cloudflare's native Request rejects redirect:error before sending anything.
    // This mirrors the platform restriction observed during live deployment.
    assert.ok(['follow', 'manual'].includes(init.redirect), 'Workers supports only follow/manual');
    assert.equal(init.redirect, 'manual', 'Public source requests must never auto-follow');
    requests.push(String(url));
    return new Response('redirect', { status: 302, headers: { Location: 'https://outside-allowlist.example/private' } });
  });
  const source = await redirecting(new Request(`${SITE_URL}/api/docs?path=README.md`));
  assert.equal(source.status, 502);
  assert.match((await source.json()).error, /Public source redirect rejected/);
  const asset = await redirecting(new Request(`${SITE_URL}/redesign.css`));
  assert.equal(asset.status, 502);
  assert.equal((await asset.json()).error, 'Static origin redirect rejected');
  assert.equal(asset.headers.has('location'), false);
  assert.deepEqual(requests, [`${RAW_ROOT}README.md`, `${RAW_ROOT}docs/redesign.css`]);
});

test('network failures do not expose runtime diagnostic text', async () => {
  const failing = createHandler(async () => { throw new TypeError('private runtime diagnostic'); });
  for (const path of ['/api/docs?path=README.md', '/redesign.css']) {
    const response = await failing(new Request(`${SITE_URL}${path}`));
    assert.equal(response.status, 502);
    assert.doesNotMatch(await response.text(), /diagnostic|TypeError/);
  }
});
