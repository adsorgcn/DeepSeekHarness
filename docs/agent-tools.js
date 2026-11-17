/* Public, read-only WebMCP tools. No browser API is polyfilled or impersonated. */
(() => {
  'use strict';
  const context = document.modelContext || navigator.modelContext;
  if (!context || typeof context.registerTool !== 'function') return;
  let lifecycle;

  function argumentsOnly(args, allowed) {
    if (!args || typeof args !== 'object' || Array.isArray(args) ||
        Object.keys(args).some(key => !allowed.includes(key))) {
      throw new TypeError('Invalid tool arguments.');
    }
  }

  async function getJson(path, options) {
    const controller = new AbortController();
    const signal = options && options.signal;
    const cancel = () => controller.abort();
    if (signal && signal.aborted) cancel();
    if (signal) signal.addEventListener('abort', cancel, { once: true });
    const timeout = setTimeout(cancel, 10000);
    try {
      const response = await fetch(path, { signal: controller.signal, headers: { Accept: 'application/json' } });
      if (!response.ok) throw new Error('DSH public API returned HTTP ' + response.status);
      return await response.json();
    } finally {
      clearTimeout(timeout);
      if (signal) signal.removeEventListener('abort', cancel);
    }
  }

  const tools = [
    {
      name: 'dsh_install_instructions',
      title: 'iLang DSH 安装说明',
      description: 'Read the official DSH toolkit installation prompt and platform-specific bootstrap links. This tool only reads instructions; it does not install software or change the computer.',
      inputSchema: { type: 'object', properties: { platform: { type: 'string', enum: ['all', 'windows', 'macos', 'linux'], description: 'Target operating system; defaults to all.' } }, additionalProperties: false },
      annotations: { readOnlyHint: true },
      execute: async (args = {}, options) => {
        argumentsOnly(args, ['platform']);
        const platform = args.platform === undefined ? 'all' : args.platform;
        if (!['all', 'windows', 'macos', 'linux'].includes(platform)) throw new TypeError('Unsupported platform.');
        return getJson('/api/install?platform=' + platform, options);
      }
    },
    {
      name: 'dsh_search_skills',
      title: '搜索 iLang DSH 技能市场',
      description: 'Search the public iLang DSH market by name or description. Returns published skill, engineering book and plugin records with their source and version. Does not install or execute them.',
      inputSchema: { type: 'object', properties: { query: { type: 'string', maxLength: 160, description: 'Chinese or English name/description text; omit to list all records.' } }, additionalProperties: false },
      annotations: { readOnlyHint: true },
      execute: async (args = {}, options) => {
        argumentsOnly(args, ['query']);
        if (args.query !== undefined && (typeof args.query !== 'string' || args.query.length > 160)) throw new TypeError('Query must be at most 160 characters.');
        const data = await getJson('/api/skills', options);
        const query = (args.query || '').trim().toLocaleLowerCase();
        const entries = data.entries.filter(entry => !query || JSON.stringify([entry.name, entry.title, entry.description, entry.kind]).toLocaleLowerCase().includes(query));
        return { query, marketUrl: data.marketUrl, source: data.source, entries };
      }
    }
  ];

  function register() {
    lifecycle = new AbortController();
    for (const tool of tools) {
      Promise.resolve(context.registerTool(tool, { signal: lifecycle.signal })).catch(error => {
        console.warn('DSH WebMCP registration failed for ' + tool.name + ':', error);
      });
    }
  }
  register();
  addEventListener('pagehide', () => lifecycle.abort());
  addEventListener('pageshow', event => { if (event.persisted) register(); });
})();
