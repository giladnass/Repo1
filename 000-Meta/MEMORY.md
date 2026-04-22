---
title: MEMORY
type: note
tags: [meta, system, ai-memory]
created: 2026-04-20
permalink: ai-memory/000-meta/memory
---

# Persistent Context

*Last updated: 2026-04-22 -- Claude Code, Phase 4 complete*

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
- **Phase 2 complete** -- conversion pipeline written and operational (ingest.py, process.py, watch.sh, session_end.py, linkding_export.py); PDFs processed, linkding export run, faster-whisper deployed on Netcup
- **Phase 3 complete** -- Aurora operational on Discord + Telegram, KI-001/KI-004 resolved
- **Phase 4 complete** -- Aurora connected to basic-memory MCP, memory rebuilt, SSH key auth fixed, watch.sh LaunchAgent installed
- D-006 (MCP data contract) finalized: Active

### Aurora / OpenClaw (as of 2026-04-22)

- Primary model: `moonshotai/kimi-k2.5` via OpenRouter (200k ctx)
- Fallback 1: `ollama/minimax-m2.5:cloud` (Ollama Cloud, user: giladn)
- Fallback 2: `openrouter/google/gemini-2.0-flash-001`
- Channels: Discord (active, groupPolicy=allowlist) + Telegram (active)
- Workspace brain files: global, shared across all channels
- USER.md: correct Hebrew name spelling (גילעד), bilingual response rules
- basic-memory MCP connected via `mcp-remote` stdio bridge (OpenClaw bug workaround for #65590/#66940)
- BOOTSTRAP.md deleted -- no more re-introduction on new sessions
- SOUL.md updated: no process narration, outcome-only responses
- compaction.reserveTokensFloor set to 20000
- Aurora rebuilt her workspace MEMORY.md from vault content
- SSH key auth fixed on Mac (`netcup_key` added to keychain)

## Active Projects

1. **AI Memory System** -- this vault. Build plan: [[Working-Context/knowledge-base-build-plan]]
2. **OpenClaw/Aurora** -- always-on AI agent on Netcup. See [[Wiki/openclaw-aurora]]
3. **Obsidian Codex vault** -- separate vault used by OpenClaw, synced from Google Drive to `/home/openclaw/obsidian/codex-vault` on Netcup

## Infrastructure

- **Mac (M4, 48GB):** interactive work, conversion pipelines (pymupdf4llm, pandoc), Ollama Cloud client
- **Netcup (Ubuntu 24.04, 32GB RAM, 12 vCPU, no GPU):** Ollama, OpenClaw, AnythingLLM, Open WebUI, IPTVX, faster-whisper. Details: [[Wiki/netcup-server]]
- **Ollama models on Netcup:** `qwen2.5:1.5b`, `deepseek-r1:1.5b`, `llama3.2:latest`, `llama3.2-32k` (custom 32k ctx)
- **Ollama Cloud:** logged in as `giladn` (Pro subscription); `qwen3.5:cloud` (triage), `glm-5:cloud` (summarization)

## Key Decisions Made

All decisions in [[000-Meta/decisions]] are Active as of 2026-04-22.

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

See [[000-Meta/known-issues]] for documented issues.

- **KI-001/KI-004 RESOLVED** (2026-04-22): Aurora no longer falls back to Gemini. Fixed by switching primary model to `moonshotai/kimi-k2.5` (200k ctx).
- KI-002/KI-003: Minor OpenClaw issues, see known-issues.md
- KI-005: Marker suspended (Apple Silicon MPS bug) -- pymupdf4llm used instead
- **KI-006 ACTIVE**: OpenClaw MCP streamable-http bug (issues #65590/#66940) -- workaround in place via mcp-remote

## Pipeline Status (as of 2026-04-22)

- `Scripts/ingest.py` -- PDF + doc converter, operational
- `Scripts/process.py` -- LLM triage + summarization via LiteLLM (Ollama Cloud)
- `Scripts/watch.sh` -- fswatch watcher, running as LaunchAgent on Mac
- `Scripts/session_end.py` -- automated session logging
- `Scripts/linkding_export.py` -- bookmark export pipeline, full run completed
- `Scripts/transcribe.py` -- audio/video transcription (faster-whisper on Netcup), deployed + tested

## What the Next Session Should Do

1. **LINT automation** -- set up weekly cron or Obsidian plugin for vault validation
2. **Aurora memory enrichment** -- ask Aurora to do a deeper read of the vault and expand her MEMORY.md
3. **Multi-agent Discord** -- future: additional agents per domain with channel-specific access
