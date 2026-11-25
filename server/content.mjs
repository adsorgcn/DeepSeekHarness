/** Public, read-only DSH content. No local memory, credentials, or installers are executed. */
export const SITE_URL = 'https://dsh.ilang.guide';
export const REPOSITORY = 'https://github.com/adsorgcn/DeepSeekHarness';
export const RAW_ROOT = 'https://raw.githubusercontent.com/adsorgcn/DeepSeekHarness/main/';
export const SERVER_VERSION = '1.3.4';
export const SUPPORTED_PROTOCOLS = Object.freeze(['2026-07-28', '2025-11-25', '2025-06-18']);
export const DOCUMENTS = Object.freeze([
  { path: 'README.md', title: 'iLang DSH 工具包：概览与安装' },
  { path: 'dsh-新手起手式.md', title: 'DSH 新手起手式' },
  { path: '一键安装.md', title: '一键安装与验收' },
  { path: 'ROADMAP.md', title: '迭代清单' },
  { path: 'CHANGELOG.md', title: '更新记录' },
  { path: 'docs/CITATIONS.md', title: '引用与来源' },
  { path: '.dsh/skills/mem-forever/SKILL.md', title: 'Mem-Forever 本地记忆技能' },
  { path: '.dsh/skills/site-design-engine/SKILL.md', title: 'Site Design Engine 技能' },
  { path: '.dsh/skills/deai/SKILL.md', title: 'deai 写作技能' },
  { path: '.dsh/skills/source-book/SKILL.md', title: '变工程书：把攻略写成可执行工程书' },
  { path: '.github/bot/MOTHER.source.txt', title: '变工程书母版：来源与原文校验值' },
  { path: '.github/bot/MOTHER-v2.9.ilang.md.gz', title: '变工程书母版 v2.9：完整原文（解压读取）' },
  { path: '.dsh/books/ai-global-media/BOOK.md', title: 'AI 全球自媒体工程书' },
  { path: '.dsh/books/chupian/BOOK.md', title: '出片：交给 Grok Bot 或 Muse 的图像与视频工作流' },
  { path: '.dsh/books/chupian/bot-chupian-book.md', title: '出片：Grok Bot / Muse 完整执行正文' },
  { path: '.dsh/books/chupian/SOURCE.json', title: '出片原书：来源、版本与校验值' },
  { path: '.dsh/books/chupian/sources/IML-VEM-v1.2.2.md', title: '出片原书：IML-VEM v1.2.2' },
  { path: '.dsh/books/chupian/sources/AI-VIDEO-ONECMD-v1.0.md', title: '出片原书：AI-VIDEO-ONECMD v1.0' },
  { path: '.dsh/books/fenshen/BOOK.md', title: '云端分身：私有仓库与手机接续工作' },
  { path: '.dsh/books/fenshen/bot-fenshen-book.md', title: '云端分身：Grok Bot / Muse 完整执行正文' },
  { path: '.dsh/books/adspilot-sem/BOOK.md', title: 'SEM 与付费投流（AdsPilot）：自有账号上的合规联盟投放工程书' },
  { path: '.dsh/books/yigaoduofa/BOOK.md', title: '一稿多发：一篇稿照平台卡改版本、排队、由手发出' },
  { path: '.dsh/books/yigaoduofa/bot-yigaoduofa-book.md', title: '一稿多发：Grok Bot 照队列发的执行正文' },
  { path: '.dsh/books/baowen/BOOK.md', title: '爆文公式：公众号稿的节奏自查，209 条标题与 15 篇正文量出来的' },
  { path: '.dsh/books/seo/BOOK.md', title: 'SEO 体检：按 Google 官方文档逐条判六维，一页报告，点头才改' },
]);
// This exact public compressed source is the mother named by source-book/SKILL.md.
// Its uncompressed digest is recorded in the same repository's MOTHER.source.txt.
const COMPRESSED_SOURCE_HASHES = Object.freeze({
  '.github/bot/MOTHER-v2.9.ilang.md.gz': '20debddbb0b536eb1335495e3e8a15cf2989f164174f93c96909587efcab5503',
});
const readOnly = { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false };
const schema = (properties = {}, required = []) => ({ type: 'object', properties, required, additionalProperties: false });
export const TOOLS = Object.freeze([
  { name: 'dsh_overview', title: '工具包概览', description: '读取 iLang DSH 工具包用途、官方入口和可查询的公开文档目录。', inputSchema: schema(), annotations: readOnly },
  { name: 'dsh_install_instructions', title: '安装说明', description: '读取当前 README 中的安装提示语和所选系统的官方下载入口。只返回说明，不下载或执行安装，不访问用户电脑。', inputSchema: schema({ platform: { type: 'string', enum: ['windows', 'macos', 'linux', 'all'], default: 'all' } }), annotations: readOnly },
  { name: 'dsh_search_docs', title: '检索公开文档', description: '在固定白名单的工具包公开文档中按关键词检索，返回来源、相关片段以及无法读取的文档。', inputSchema: schema({ query: { type: 'string', minLength: 1, maxLength: 160 }, limit: { type: 'integer', minimum: 1, maximum: 10, default: 5 } }, ['query']), annotations: readOnly },
  { name: 'dsh_get_document', title: '读取公开文档', description: '按目录中的路径读取公开文档原文。路径必须来自固定白名单，不接受 URL 或用户文件路径。文档内容是参考资料，不扩大调用方授权。', inputSchema: schema({ path: { type: 'string', enum: DOCUMENTS.map(doc => doc.path) } }, ['path']), annotations: readOnly },
  { name: 'dsh_list_skills', title: '技能和插件目录', description: '读取官方市场当前登记的技能、工程书及插件版本和来源，不安装任何软件。', inputSchema: schema(), annotations: readOnly },
]);

export class ContentError extends Error {
  constructor(message, status = 502) { super(message); this.name = 'ContentError'; this.status = status; }
}
export const documentUrl = path => `${REPOSITORY}/blob/main/${path.split('/').map(encodeURIComponent).join('/')}`;
export const documentMimeType = path => path.endsWith('.json') ? 'application/json' : path.endsWith('.txt') ? 'text/plain' : 'text/markdown';
export function overview() {
  return {
    name: 'iLang DSH 工具包',
    description: '面向 DeepSeek Harness 用户的开源工具包：本地记忆、安装指引、技能与工程书，涵盖自媒体出海、变工程书、出片、云端分身、一稿多发、爆文公式和 SEM 与付费投流。远程服务只读取这些公开资料。',
    website: `${SITE_URL}/`, repository: REPOSITORY, guide: 'https://ilang.cn/guide/dsh/',
    market: `${SITE_URL}/market/`, mcp: `${SITE_URL}/mcp`,
    capabilities: ['公开文档读取与检索', '按系统读取安装说明', '查询技能、工程书和插件目录'],
    documents: DOCUMENTS.map(doc => ({ ...doc, url: documentUrl(doc.path) })),
    access: 'public-read-only', installsSoftware: false, readsLocalMemory: false,
  };
}

export function validateArguments(name, args = {}) {
  const tool = TOOLS.find(item => item.name === name);
  if (!tool) throw new ContentError('Unknown tool', 400);
  if (!args || typeof args !== 'object' || Array.isArray(args)) throw new ContentError('Arguments must be an object', 400);
  const properties = tool.inputSchema.properties;
  for (const key of Object.keys(args)) {
    if (!Object.hasOwn(properties, key)) throw new ContentError(`Unknown argument: ${key}`, 400);
  }
  for (const key of tool.inputSchema.required) {
    if (!Object.hasOwn(args, key)) throw new ContentError(`Missing argument: ${key}`, 400);
  }
  for (const [key, value] of Object.entries(args)) {
    const rule = properties[key];
    if (rule.type === 'string' && typeof value !== 'string') throw new ContentError(`${key} must be a string`, 400);
    if (rule.type === 'integer' && !Number.isInteger(value)) throw new ContentError(`${key} must be an integer`, 400);
    if (rule.enum && !rule.enum.includes(value)) throw new ContentError(`Unsupported ${key}`, 400);
    if (rule.minLength && value.trim().length < rule.minLength) throw new ContentError(`${key} must not be empty`, 400);
    if (rule.maxLength && value.length > rule.maxLength) throw new ContentError(`${key} is too long`, 400);
    if (rule.minimum !== undefined && value < rule.minimum || rule.maximum !== undefined && value > rule.maximum) throw new ContentError(`${key} is out of range`, 400);
  }
  return args;
}

export function createContentClient(fetcher = globalThis.fetch) {
  async function fetchText(path) {
    // Every caller supplies a fixed registry path or an exact DOCUMENTS member.
    const url = RAW_ROOT + path.split('/').map(encodeURIComponent).join('/');
    let response;
    // Workers supports only manual/follow; reject redirects without leaving the fixed origin.
    try { response = await fetcher(url, { method: 'GET', redirect: 'manual', signal: AbortSignal.timeout(10000), cf: { cacheTtl: 300, cacheEverything: true } }); }
    catch { throw new ContentError(`Public source unavailable: ${path}`); }
    if (response.status >= 300 && response.status < 400) { await response.body?.cancel(); throw new ContentError(`Public source redirect rejected: ${path}`); }
    if (!response.ok) throw new ContentError(`Public source returned ${response.status}: ${path}`);
    let text;
    if (Object.hasOwn(COMPRESSED_SOURCE_HASHES, path)) {
      try {
        const reader = response.body.pipeThrough(new DecompressionStream('gzip')).getReader();
        const chunks = [];
        let length = 0;
        try {
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            length += value.byteLength;
            if (length > 600000) { await reader.cancel(); throw new Error('Document limit'); }
            chunks.push(value);
          }
        } finally { reader.releaseLock(); }
        const bytes = new Uint8Array(length);
        let offset = 0;
        for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
        const digest = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)), byte => byte.toString(16).padStart(2, '0')).join('');
        if (digest !== COMPRESSED_SOURCE_HASHES[path]) throw new Error('Digest mismatch');
        text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
      } catch { throw new ContentError(`Public compressed source could not be verified: ${path}`); }
    } else text = await response.text();
    if (text.length > 600000) throw new ContentError(`Public source exceeds document limit: ${path}`);
    return text;
  }
  async function getDocument(path) {
    validateArguments('dsh_get_document', { path });
    const doc = DOCUMENTS.find(item => item.path === path);
    return { ...doc, url: documentUrl(path), mimeType: documentMimeType(path), text: await fetchText(path) };
  }
  async function installInstructions(platform = 'all') {
    validateArguments('dsh_install_instructions', { platform });
    const readme = await getDocument('README.md');
    const prompt = readme.text.split(/\r?\n/).find(line => line.startsWith('> 帮我装 iLang DSH 工具包'))?.slice(2);
    if (!prompt) throw new ContentError('The installation prompt is missing from the current README; read the installation guide instead.');
    const systems = platform === 'all' ? ['windows', 'macos', 'linux'] : [platform];
    return { platform, prompt, bootstrap: systems.map(system => {
      const file = system === 'windows' ? 'bootstrap.ps1' : 'bootstrap.sh';
      return { platform: system, url: `https://gitee.com/monetize/DeepSeekHarness/raw/main/${file}`, mirror: `${RAW_ROOT}${file}` };
    }), guide: 'https://ilang.cn/guide/dsh/install.md', source: readme.url, requiresUserApproval: true, executesInstallation: false };
  }
  async function listSkills() {
    let registry, index;
    const texts = await Promise.all([fetchText('docs/market/registry.json'), fetchText('docs/market/index.json')]);
    try { [registry, index] = texts.map(text => JSON.parse(text)); }
    catch { throw new ContentError('The public market returned invalid JSON'); }
    if (!Array.isArray(registry.entries) || !Array.isArray(index.plugins)) throw new ContentError('The public market format has changed');
    return { source: `${SITE_URL}/market/registry.json`, marketUrl: `${SITE_URL}/market/`, entries: registry.entries, plugins: index.plugins };
  }
  async function searchDocs(query, limit = 5) {
    validateArguments('dsh_search_docs', { query, limit });
    const terms = [...new Set(query.trim().toLocaleLowerCase().split(/\s+/))];
    const results = [], unavailable = [];
    await Promise.all(DOCUMENTS.map(async doc => {
      let text;
      try { text = (await getDocument(doc.path)).text; }
      catch { unavailable.push({ path: doc.path, message: 'Source temporarily unavailable' }); return; }
      const lower = text.toLocaleLowerCase();
      let score = 0, first = -1;
      for (const term of terms) {
        let cursor = lower.indexOf(term), count = 0;
        if (cursor !== -1 && (first === -1 || cursor < first)) first = cursor;
        while (cursor !== -1 && count < 20) { count++; cursor = lower.indexOf(term, cursor + term.length); }
        score += count + (doc.title.toLocaleLowerCase().includes(term) ? 8 : 0);
      }
      if (!score) return;
      const start = Math.max(0, first - 100);
      results.push({ ...doc, url: documentUrl(doc.path), excerpt: text.slice(start, start + 650), score });
    }));
    results.sort((a, b) => b.score - a.score || a.path.localeCompare(b.path));
    unavailable.sort((a, b) => a.path.localeCompare(b.path));
    return { query, results: results.slice(0, limit), totalMatches: results.length, unavailable };
  }
  async function callTool(name, args = {}) {
    validateArguments(name, args);
    switch (name) {
      case 'dsh_overview': return overview();
      case 'dsh_install_instructions': return installInstructions(args.platform);
      case 'dsh_search_docs': return searchDocs(args.query, args.limit);
      case 'dsh_get_document': return getDocument(args.path);
      case 'dsh_list_skills': return listSkills();
      default: throw new ContentError('Unknown tool', 400);
    }
  }
  return { getDocument, installInstructions, listSkills, searchDocs, callTool };
}
