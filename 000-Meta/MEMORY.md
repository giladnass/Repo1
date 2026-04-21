---
title: MEMORY
type: note
permalink: ai-memory/000-meta/memory
---

# Persistent Context

*Last updated: 2026-04-21 -- Claude Code, Phases 3-5 complete*

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
- **Phase 2 complete** -- conversion scripts written, pymupdf4llm adopted (D-009), 13 PDFs processed
- **Phase 3 complete** -- process.py written, LiteLLM integration, three-step LLM pipeline operational
- **Phase 4 complete** -- session_end.py written for automated session logging
- **Phase 5 complete** -- linkding_export.py written for bookmark ingestion
- D-006 (MCP data contract) finalized: Active

## Active Projects

1. **AI Memory System** -- this vault. Build plan: [[Working-Context/knowledge-base-build-plan]]
2. **OpenClaw/Aurora** -- always-on AI agent on Netcup. See [[Wiki/openclaw-aurora]]
3. **Obsidian Codex vault** -- separate vault used by OpenClaw, synced from Google Drive to `/home/openclaw/obsidian/codex-vault` on Netcup

## Infrastructure

- **Mac M4 (48GB):** primary inference machine, conversion pipelines (marker, pandoc), Ollama Cloud client
- **Netcup (Ubuntu 24.04, 32GB RAM, 12 vCPU, no GPU):** transcription (faster-whisper), OpenClaw, AnythingLLM, Open WebUI, IPTVX. Details: [[Wiki/netcup-server]]
- **Ollama Cloud models:** `qwen3.5:cloud` (triage), `glm-5:cloud` (summarization)
- **Local Ollama models on Netcup:** `qwen2.5:1.5b`, `deepseek-r1:1.5b`, `llama3.2:latest`

## Key Decisions Made

All decisions in [[000-Meta/decisions]] are Active as of 2026-04-21.

Quick ref:
- D-001: Convert to MD before ingestion
- D-002: Sources are immutable
- D-003: Frontmatter schema (canonical)
- D-004: Tag namespacing (`type/*`, `source-type/*` prefixes for structural tags)
- D-005: File naming (lowercase-kebab, no date prefix for wiki pages)
- D-006: MCP data contract -- satisfied by basic-memory
- D-007: Processing location (Mac for conversion, cloud for inference, Netcup for transcription)
- D-008: LLM model selection (qwen3.5:cloud for triage, glm-5:cloud for synthesis)
- D-009: pymupdf4llm as primary PDF converter

## Known Issues

See [[000-Meta/known-issues]] for documented OpenClaw issues. Key architectural constraint: OpenClaw's 16k minimum context enforcement conflicts with `qwen2.5:1.5b` optimal context of 2048, causing all Aurora sessions to fall back to Gemini.

## Processing Pipeline Status (as of 2026-04-21)

- `Scripts/ingest.py` -- handles PDF (pymupdf4llm) + DOCX/EPUB/PPTX (pandoc)
- `Scripts/process.py` -- LLM processing with LiteLLM (triage, summarization, cross-referencing)
- `Scripts/session_end.py` -- automated session logging and MEMORY updates
- `Scripts/linkding_export.py` -- bookmark fetch and conversion pipeline
- `Scripts/watch.sh` -- fswatch watcher for `~/AI-Ingestion/01-source/`

## What the Next Session Should Do

1. **Phase 6: OpenClaw basic-memory MCP integration** -- configure Aurora to write to vault from Telegram
2. **Fix KI-001/KI-004:** test `llama3.2:latest` as OpenClaw primary model
3. **LINT automation:** set up automated linting/validation for vault files
4. **Full linkding batch:** run linkding_export.py to process all bookmarks
5. **Transcription setup on Netcup:** install faster-whisper, test on short audio file
