---
title: MEMORY
type: note
permalink: ai-memory/000-meta/memory
---

# Persistent Context

*Last updated: 2026-04-20 — Claude Code, session: Phase 0 foundation build*

---

## Who This Vault Belongs To

- **Owner:** Gilad
- **Primary interface:** Obsidian on Mac, synced via iCloud + GitHub (`giladnass/Repo1`)
- **AI tools with access:** Claude, Claude Code, Gemini (others — see [[Memory/tool-configs]])

## Current System State

- Vault is live and cloned to GitHub: `giladnass/Repo1`
- Development branch: `claude/caveman-lite-vrjM3`
- MCP access layer: present but details not yet documented (see [[Memory/tool-configs]])
- **Phase 0 complete** — schema locked, templates populated, 4 wiki pages created, build plan written

## Active Projects

1. **AI Memory System** — this vault. Build plan: [[Working-Context/knowledge-base-build-plan]]
2. **OpenClaw/Aurora** — agentic infrastructure project. Shares infrastructure with this vault. *Not yet documented — requires input.*
3. **Shared cross-tool memory pool** — accessible by multiple AI tools. *Not yet documented.*

## Known Infrastructure

- **Mac:** conversion pipelines (PDF via `marker`, Office/EPUB via `pandoc`)
- **Netcup server:** audio/video processing (`faster-whisper`, SAM). Details TBD.
- **Git sync:** iCloud → GitHub → this Linux environment

## Schema (Quick Reference)

All files must have: `title`, `type`, `tags`, `created`

Type vocabulary: `wiki | source | decision | session-log | weekly-review | working-context | template | note`

Tag namespacing: structural tags use `type/*`, `source-type/*` prefixes; domain tags are free-form lowercase-kebab.

File naming: `lowercase-kebab-case.md`. Date prefix only for daily notes/session logs.

Full schema: [[000-Meta/decisions]] D-003.

## Key Decisions Made

See [[000-Meta/decisions]] for full log. 8 decisions as of 2026-04-20:
- D-001: Convert to MD before ingestion
- D-002: Sources are immutable
- D-003: Frontmatter schema locked
- D-004: Tag namespacing convention
- D-005: File naming convention
- D-006: MCP data contract (Draft)
- D-007: Processing location strategy
- D-008: LLM model selection (Haiku/Sonnet/Opus by task)

## Open Questions (Requiring Human Input)

1. Which MCP server is running and what tools/endpoints does it expose?
2. What AI tools are currently connected? (to populate [[Memory/tool-configs]])
3. What is OpenClaw/Aurora? What infrastructure does it share with this vault?
4. What are the "known unresolved problems" referenced in the mission brief?
5. What is the Netcup server setup (OS, specs, access method, what's installed)?
6. What is Gilad's profile? (to populate [[Memory/profile]])

## What the Next Session Should Do

1. Human provides answers to the 6 open questions above
2. Populate [[Memory/tool-configs]] with connected tools and their capabilities
3. Begin Phase 1: verify MCP data contract (D-006) against real server
4. Then Phase 2: install and test conversion pipelines (marker, pandoc, faster-whisper)
