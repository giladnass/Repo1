---
title: MEMORY
type: note
permalink: ai-memory/000-meta/memory
---

# Persistent Context

*Last updated: 2026-04-20 -- Claude Code, Phase 1 context ingestion*

---

## Who This Vault Belongs To

- **Owner:** Gilad (Senior Product Marketing Manager, Kfar Saba, Israel)
- **Primary interface:** Obsidian on Mac, synced via iCloud + GitHub (`giladnass/Repo1`)
- **AI tools with access:** Claude, Claude Code, Gemini, NotebookLM, Aurora (via OpenClaw)
- **Full tool inventory:** [[Memory/tool-configs]]
- **Communication rule:** No em dashes in any AI output

## Current System State

- Vault is live on GitHub: `giladnass/Repo1`, branch `claude/caveman-lite-vrjM3`
- MCP access layer: basic-memory at `https://memory.giladn.com/mcp/` (token in tool-configs)
- **Phase 0 complete** -- schema locked, templates populated, 4 wiki pages, build plan written
- **Phase 1 complete** -- MCP verified, tool inventory documented, infrastructure documented
- D-006 (MCP data contract) finalized: Active

## Active Projects

1. **AI Memory System** -- this vault. Build plan: [[Working-Context/knowledge-base-build-plan]]
2. **OpenClaw/Aurora** -- always-on AI agent on Netcup. See [[Wiki/openclaw-aurora]]
3. **Obsidian Codex vault** -- separate vault used by OpenClaw, synced from Google Drive to `/home/openclaw/obsidian/codex-vault` on Netcup

## Infrastructure

- **Mac (M4, 48GB):** interactive work, conversion pipelines (marker, pandoc)
- **Netcup (Ubuntu 24.04, 32GB RAM, 12 vCPU, no GPU):** Ollama, OpenClaw, AnythingLLM, Open WebUI, IPTVX. Details: [[Wiki/netcup-server]]
- **Ollama models on Netcup:** `qwen2.5:1.5b`, `deepseek-r1:1.5b`, `llama3.2:latest`

## Key Decisions Made

All 8 decisions in [[000-Meta/decisions]] are Active as of 2026-04-20. D-006 was Draft; now Active after MCP verification.

Quick ref:
- D-001: Convert to MD before ingestion
- D-002: Sources are immutable
- D-003: Frontmatter schema (canonical)
- D-004: Tag namespacing (`type/*`, `source-type/*` prefixes for structural tags)
- D-005: File naming (lowercase-kebab, no date prefix for wiki pages)
- D-006: MCP data contract -- satisfied by basic-memory
- D-007: Processing location (Mac for conversion, Netcup for compute-heavy)
- D-008: LLM model selection (Haiku for triage, Sonnet for synthesis, Opus for vision)

## Known Issues

See [[000-Meta/known-issues]] for 4 documented OpenClaw issues. Key architectural constraint: OpenClaw's 16k minimum context enforcement conflicts with `qwen2.5:1.5b` optimal context of 2048, causing all Aurora sessions to fall back to Gemini.

## What the Next Session Should Do

1. Begin Phase 2: install and test conversion pipelines
   - `marker` on Mac for PDFs
   - `pandoc` on Mac for DOCX/EPUB
   - `faster-whisper` on Netcup for audio/video
   - `linkding` for URL capture
2. Consider: configure OpenClaw with basic-memory MCP endpoint (strategic opportunity)
3. Consider: replace `qwen2.5:1.5b` with `llama3.2:latest` as OpenClaw primary to resolve KI-001/KI-004
