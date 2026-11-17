---
name: dsh-market
description: Find published iLang DSH skills, engineering books and plugins, including pinned versions and sources, without executing them.
---

# Browse the iLang DSH market

Use this skill when the user wants to find a capability or check what is included in the toolkit.

1. Call `dsh_list_skills` through `https://dsh.ilang.guide/mcp`, or GET `https://dsh.ilang.guide/api/skills`.
2. Match the user's task against each entry's name, title and description. Preserve `kind` so a bundled skill, engineering book and separately installed plugin are not confused.
3. Report the entry's published version and upstream source when present. `get: kit` means it is bundled; `get: npm` means it is a plugin installed separately with the user's approval.
4. Follow the returned official source for usage details. A catalogue entry or schema check does not prove every workflow has run on the user's machine. Never claim to install, publish or connect an account merely by reading the catalogue.

Human-readable market: https://dsh.ilang.guide/market/
Raw catalogue: https://dsh.ilang.guide/market/registry.json
Plugin registry: https://dsh.ilang.guide/market/index.json
Authentication: none. This service only reads public records.
