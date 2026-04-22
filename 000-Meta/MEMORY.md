---
title: MEMORY
type: note
permalink: ai-memory/000-meta/memory
---

# Persistent Context

*Last updated: 2026-04-22 -- Claude Code, Aurora migration + KI-001/KI-004 fix*

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
- **Phase 2 complete** -- conversion pipeline written (ingest.py, watch.sh), 13 PDFs pending Mac run
- **Phase 3 complete** -- Aurora operational on Discord + Telegram, KI-001/KI-004 resolved
- D-006 (MCP data contract) finalized: Active

### Aurora / OpenClaw (as of 2026-04-22)

- Primary model: `moonshotai/kimi-k2.5` via OpenRouter (200k ctx)
- Fallback 1: `ollama/minimax-m2.5:cloud` (Ollama Cloud, user: giladn)
- Fallback 2: `openrouter/google/gemini-2.0-flash-001`
- Channels: Discord (active, groupPolicy=allowlist) + Telegram (active)
- Workspace brain files: global, shared across all channels
- USER.md: correct Hebrew name spelling (גילעד), bilingual response rules
- Sessions reset 2026-04-22; workspace MEMORY.md sparse (one entry), will rebuild naturally

## Active Projects

1. **AI Memory System** -- this vault. Build plan: [[Working-Context/knowledge-base-build-plan]]
2. **OpenClaw/Aurora** -- always-on AI agent on Netcup. See [[Wiki/openclaw-aurora]]
3. **Obsidian Codex vault** -- separate vault used by OpenClaw, synced from Google Drive to `/home/openclaw/obsidian/codex-vault` on Netcup

## Infrastructure

- **Mac (M4, 48GB):** interactive work, conversion pipelines (marker, pandoc)
- **Netcup (Ubuntu 24.04, 32GB RAM, 12 vCPU, no GPU):** Ollama, OpenClaw, AnythingLLM, Open WebUI, IPTVX. Details: [[Wiki/netcup-server]]
- **Ollama models on Netcup:** `qwen2.5:1.5b`, `deepseek-r1:1.5b`, `llama3.2:latest`, `llama3.2-32k` (custom 32k ctx)
- **Ollama Cloud:** logged in as `giladn` (Pro subscription)

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

See [[000-Meta/known-issues]] for documented issues.

- **KI-001/KI-004 RESOLVED** (2026-04-22): Aurora no longer falls back to Gemini. Fixed by switching primary model to `moonshotai/kimi-k2.5` (200k ctx), which exceeds the 16k minimum context floor.
- KI-005: Marker suspended (Apple Silicon MPS bug) -- pymupdf4llm used instead
- KI-002/KI-003: Minor OpenClaw issues, see known-issues.md

## Pipeline Status (as of 2026-04-22)

- pymupdf4llm: adopted (D-009), Marker suspended (KI-005)
- Pandoc: installed and working
- `Scripts/ingest.py`: written and ready
- `Scripts/watch.sh`: written and ready
- **13 PDFs pending conversion** -- run `python3 Scripts/ingest.py` on Mac

## What the Next Session Should Do

1. **Run the 13-PDF batch on Mac:** `pip install pymupdf4llm && python3 Scripts/ingest.py`
2. **Start watch.sh** on Mac: `brew install fswatch && ./Scripts/watch.sh`
3. **Install faster-whisper on Netcup** for audio/video transcription
4. **Set up linkding** for URL capture
5. **Connect Aurora to basic-memory MCP** -- high-value: lets Aurora write to this vault from any channel
6. **Run full linkding export** (no `--limit` flag)
