import { readFile, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';
import test from 'node:test';
import { TOOLS, DOCUMENTS, SERVER_VERSION, SUPPORTED_PROTOCOLS, SITE_URL, RAW_ROOT } from '../server/content.mjs';
import { createHandler } from '../server/worker.mjs';

const root = new URL('../', import.meta.url);
const docs = new URL('docs/', root);
const json = async path => JSON.parse(await readFile(new URL(path, docs), 'utf8'));
const openapi = await json('openapi.json');
const handler = createHandler(async url => {
  assert.ok(url.startsWith(RAW_ROOT), 'public content must stay on the fixed repository origin');
  const relative = decodeURIComponent(url.slice(RAW_ROOT.length));
  assert.ok(!relative.split('/').some(part => part === '..' || part === '.'), 'reject traversal in test source');
  try { return new Response(await readFile(new URL(relative, root)), { status: 200 }); }
  catch (error) { if (error.code === 'ENOENT') return new Response('Not found', { status: 404 }); throw error; }
});

function checkSchema(schema, value, path = '$') {
  if (schema.const !== undefined) assert.deepEqual(value, schema.const, path + ' const');
  if (schema.enum) assert.ok(schema.enum.includes(value), path + ' enum');
  if (schema.type === 'object') {
    assert.ok(value !== null && typeof value === 'object' && !Array.isArray(value), path + ' object');
    for (const name of schema.required || []) assert.ok(Object.hasOwn(value, name), path + '.' + name + ' required');
    for (const [name, item] of Object.entries(value)) {
      if (schema.properties?.[name]) checkSchema(schema.properties[name], item, path + '.' + name);
      else if (schema.additionalProperties === false) assert.fail(path + '.' + name + ' not allowed');
    }
  } else if (schema.type === 'array') {
    assert.ok(Array.isArray(value), path + ' array');
    for (const [index, item] of value.entries()) checkSchema(schema.items, item, `${path}[${index}]`);
  } else if (schema.type === 'integer') {
    assert.ok(Number.isInteger(value), path + ' integer');
    if (schema.minimum !== undefined) assert.ok(value >= schema.minimum, path + ' minimum');
    if (schema.maximum !== undefined) assert.ok(value <= schema.maximum, path + ' maximum');
  } else if (schema.type) {
    assert.equal(typeof value, schema.type, path + ' type');
  }
  if (schema.format === 'uri') assert.ok(new URL(value).protocol, path + ' URI');
}

test('all published JSON files and the extensionless API catalogue parse', async () => {
  async function walk(directory) {
    for (const item of await readdir(directory, { withFileTypes: true })) {
      const path = new URL(item.name + (item.isDirectory() ? '/' : ''), directory);
      if (item.isDirectory()) await walk(path);
      else if (item.name.endsWith('.json')) JSON.parse(await readFile(path, 'utf8'));
    }
  }
  await walk(docs);
  assert.ok(Array.isArray((await json('.well-known/api-catalog')).linkset));
});

test('MCP discovery cards describe the actual current server and tools', async () => {
  const card = await json('.well-known/mcp/server-card.json');
  assert.deepEqual(card, await json('.well-known/mcp.json'));
  assert.deepEqual(card.tools, TOOLS);
  assert.equal(card.serverInfo.version, SERVER_VERSION);
  assert.equal(card.protocolVersion, SUPPORTED_PROTOCOLS[0]);
  assert.equal(card.transport.endpoint, SITE_URL + '/mcp');
  assert.equal(card.authentication.required, false);
  assert.ok(card.capabilities.tools && card.capabilities.resources);
});

test('Agent Skills point to real same-origin artifacts with exact SHA-256 digests', async () => {
  const index = await json('.well-known/agent-skills/index.json');
  assert.equal(index.$schema, 'https://schemas.agentskills.io/discovery/0.2.0/schema.json');
  assert.ok(index.skills.length > 0);
  const names = new Set();
  for (const entry of index.skills) {
    assert.match(entry.name, /^[a-z0-9]+(?:-[a-z0-9]+)*$/);
    assert.ok(!names.has(entry.name)); names.add(entry.name);
    assert.equal(entry.type, 'skill-md');
    const url = new URL(entry.url);
    assert.equal(url.origin, SITE_URL);
    const response = await handler(new Request(url));
    assert.equal(response.status, 200, entry.name);
    assert.match(response.headers.get('Content-Type'), /^text\/markdown/);
    const bytes = Buffer.from(await response.arrayBuffer());
    assert.equal(entry.digest, 'sha256:' + createHash('sha256').update(bytes).digest('hex'), entry.name);
    assert.match(bytes.toString(), new RegExp('^---\\r?\\nname: ' + entry.name + '\\r?\\n'));
  }
});

test('OpenAPI routes and parameter constraints stay aligned with public MCP tools', () => {
  assert.equal(openapi.openapi, '3.1.0');
  assert.equal(openapi.info.version, SERVER_VERSION);
  assert.equal(openapi.servers[0].url, SITE_URL);
  assert.deepEqual(openapi.security, []);
  const mappings = [
    ['/api/overview', 'dsh_overview'], ['/api/install', 'dsh_install_instructions'],
    ['/api/search', 'dsh_search_docs'], ['/api/docs', 'dsh_get_document'], ['/api/skills', 'dsh_list_skills']
  ];
  assert.deepEqual(Object.keys(openapi.paths).sort(), [...mappings.map(([path]) => path), '/healthz'].sort());
  for (const [path, name] of mappings) {
    const operation = openapi.paths[path].get;
    const tool = TOOLS.find(item => item.name === name);
    assert.equal(operation.operationId, name);
    const params = operation.parameters;
    const rename = field => name === 'dsh_search_docs' && field === 'query' ? 'q' : field;
    assert.deepEqual(params.map(item => item.name).sort(), Object.keys(tool.inputSchema.properties).map(rename).sort());
    for (const [field, schema] of Object.entries(tool.inputSchema.properties)) {
      const parameter = params.find(item => item.name === rename(field));
      assert.equal(parameter.in, 'query');
      assert.equal(Boolean(parameter.required), tool.inputSchema.required.includes(field));
      for (const key of ['type', 'minimum', 'maximum', 'minLength', 'maxLength', 'default', 'enum']) {
        const normalize = value => key === 'enum' && value ? [...value].sort() : value;
        assert.deepEqual(normalize(parameter.schema[key]), normalize(schema[key]), `${path} ${field} ${key}`);
      }
    }
  }
  assert.deepEqual(openapi.paths['/api/docs'].get.parameters[0].schema.enum, DOCUMENTS.map(doc => doc.path));
});

test('documented HTTP examples resolve and conform to their published response schemas', async () => {
  const examples = new Map([
    ['/api/overview', ''], ['/api/install', '?platform=windows'], ['/api/search', '?q=DSH&limit=2'],
    ['/api/docs', '?path=README.md'], ['/api/skills', ''], ['/healthz', '']
  ]);
  for (const [path, query] of examples) {
    const response = await handler(new Request(SITE_URL + path + query));
    assert.equal(response.status, 200, path);
    assert.match(response.headers.get('Content-Type'), /^application\/json/);
    checkSchema(openapi.paths[path].get.responses['200'].content['application/json'].schema, await response.json(), path);
    const methodResponse = await handler(new Request(SITE_URL + path + query, { method: 'POST' }));
    assert.equal(methodResponse.status, 405, path + ' must remain read-only');
  }
  for (const path of ['/api/docs', '/api/search']) {
    const response = await handler(new Request(SITE_URL + path));
    assert.equal(response.status, 400, path + ' requires query arguments');
  }
});

test('API catalogue and ARD entries resolve through the deployed Worker routing model', async () => {
  const response = await handler(new Request(SITE_URL + '/.well-known/api-catalog'));
  assert.equal(response.status, 200);
  assert.match(response.headers.get('Content-Type'), /^application\/linkset\+json/);
  assert.equal(response.headers.get('Access-Control-Allow-Origin'), '*');
  for (const links of (await response.json()).linkset) {
    for (const rel of ['service-desc', 'service-doc', 'status']) {
      for (const target of links[rel] || []) assert.equal((await handler(new Request(target.href))).status, 200, target.href);
    }
  }
  const manifest = await json('.well-known/ai-catalog.json');
  assert.ok(manifest.specVersion && manifest.host.displayName && manifest.host.identifier);
  for (const entry of manifest.entries) {
    assert.ok(entry.identifier && entry.displayName && entry.type);
    assert.ok(Boolean(entry.url) !== Object.hasOwn(entry, 'data'));
    assert.equal((await handler(new Request(entry.url))).status, 200, entry.url);
  }
});
