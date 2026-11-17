#!/usr/bin/env node
// Read-only live acceptance. MCP_SDK_ROOT optionally points at an installed SDK package.
import assert from 'node:assert/strict';
import { readFile, writeFile } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { SUPPORTED_PROTOCOLS } from './content.mjs';

const [endpointArgument, outputPath] = process.argv.slice(2);
if (!endpointArgument) throw new Error('Usage: node server/smoke.mjs https://host/mcp [report.json]. Set MCP_SDK_ROOT to an installed @modelcontextprotocol/sdk package directory.');
const endpoint = new URL(endpointArgument);
if (endpoint.protocol !== 'https:' && !(endpoint.protocol === 'http:' && ['localhost', '127.0.0.1', '[::1]'].includes(endpoint.hostname))) throw new Error('Use an HTTPS endpoint, or localhost for development.');
if (endpoint.username || endpoint.password) throw new Error('Do not put credentials in the endpoint URL.');
const sdkRoot = process.env.MCP_SDK_ROOT;
const clientModule = sdkRoot ? pathToFileURL(join(resolve(sdkRoot), 'dist/esm/client/index.js')).href : '@modelcontextprotocol/sdk/client/index.js';
const transportModule = sdkRoot ? pathToFileURL(join(resolve(sdkRoot), 'dist/esm/client/streamableHttp.js')).href : '@modelcontextprotocol/sdk/client/streamableHttp.js';
const [{ Client }, { StreamableHTTPClientTransport }] = await Promise.all([import(clientModule), import(transportModule)]);
let sdkVersion = 'installed package';
if (sdkRoot) sdkVersion = JSON.parse(await readFile(join(resolve(sdkRoot), 'package.json'), 'utf8')).version;
const report = { endpoint: endpoint.href, testedAt: new Date().toISOString(), sdkVersion, modern: {}, legacy: {} };
const calls = [
  ['dsh_overview', {}],
  ['dsh_install_instructions', { platform: 'windows' }],
  ['dsh_search_docs', { query: '记忆', limit: 2 }],
  ['dsh_get_document', { path: 'README.md' }],
  ['dsh_list_skills', {}],
];

let nextId = 1;
async function modern(method, params = {}) {
  const headers = { 'Content-Type': 'application/json', Accept: 'application/json, text/event-stream', 'MCP-Protocol-Version': '2026-07-28', 'Mcp-Method': method };
  if (method === 'tools/call') headers['Mcp-Name'] = params.name;
  if (method === 'resources/read') headers['Mcp-Name'] = params.uri;
  const id = nextId++;
  const response = await fetch(endpoint, { method: 'POST', headers, signal: AbortSignal.timeout(30000), body: JSON.stringify({ jsonrpc: '2.0', id, method, params: { ...params, _meta: { 'io.modelcontextprotocol/protocolVersion': '2026-07-28', 'io.modelcontextprotocol/clientInfo': { name: 'dsh-live-acceptance', version: '1.0.0' }, 'io.modelcontextprotocol/clientCapabilities': {} } } }) });
  const body = await response.json();
  assert.equal(response.status, 200, `${method}: ${JSON.stringify(body)}`);
  assert.equal(body.id, id);
  assert.equal(body.error, undefined);
  assert.equal(body.result.resultType, 'complete');
  assert.equal(body.result._meta['io.modelcontextprotocol/serverInfo'].name, 'ilang-dsh-toolkit');
  return body.result;
}
const discovery = await modern('server/discover');
assert.deepEqual(discovery.supportedVersions, SUPPORTED_PROTOCOLS);
report.modern.supportedVersions = discovery.supportedVersions;
report.modern.serverInfo = discovery._meta['io.modelcontextprotocol/serverInfo'];
const modernTools = await modern('tools/list');
assert.deepEqual(modernTools.tools.map(tool => tool.name).sort(), calls.map(([name]) => name).sort());
report.modern.tools = [];
for (const [name, args] of calls) {
  const result = await modern('tools/call', { name, arguments: args });
  assert.equal(result.isError, false, `${name}: ${JSON.stringify(result)}`);
  assert.ok(result.content[0].text.length > 0);
  if (name === 'dsh_search_docs') { assert.ok(result.structuredContent.results.length > 0); assert.deepEqual(result.structuredContent.unavailable, []); }
  report.modern.tools.push({ name, isError: result.isError, characters: result.content[0].text.length });
}
const modernResources = await modern('resources/list');
const modernRead = await modern('resources/read', { uri: modernResources.resources[0].uri });
assert.match(modernRead.contents[0].text, /iLang DSH 工具包/);
report.modern.resources = modernResources.resources.length;
report.modern.resourceRead = { uri: modernRead.contents[0].uri, characters: modernRead.contents[0].text.length };

const client = new Client({ name: 'dsh-sdk-live-acceptance', version: '1.0.0' });
const transport = new StreamableHTTPClientTransport(endpoint);
try {
  await client.connect(transport);
  report.legacy.serverInfo = client.getServerVersion();
  const listed = await client.listTools();
  assert.deepEqual(listed.tools.map(tool => tool.name).sort(), calls.map(([name]) => name).sort());
  report.legacy.tools = [];
  for (const [name, args] of calls) {
    const result = await client.callTool({ name, arguments: args });
    assert.equal(result.isError, false, `${name}: ${JSON.stringify(result)}`);
    report.legacy.tools.push({ name, isError: result.isError, characters: result.content[0].text.length });
  }
  const resources = await client.listResources();
  const read = await client.readResource({ uri: resources.resources[0].uri });
  assert.match(read.contents[0].text, /iLang DSH 工具包/);
  report.legacy.resources = resources.resources.length;
  report.legacy.resourceRead = { uri: read.contents[0].uri, characters: read.contents[0].text.length };
} finally { await client.close(); }
report.passed = true;
const serialized = JSON.stringify(report, null, 2) + '\n';
if (outputPath) await writeFile(resolve(outputPath), serialized, 'utf8');
process.stdout.write(serialized);
