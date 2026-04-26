---
title: MEMORY
type: note
tags: [meta, system, ai-memory]
created: 2026-04-20
permalink: ai-memory/000-meta/memory
---

# Persistent Context

*Last updated: 2026-04-27 -- Claude Code, session: Aurora model regression discovered*

---

## Who This Vault Belongs To

- **Owner:** Gilad (Senior Product Marketing Manager, Kfar Saba, Israel)
- **Primary interface:** Obsidian on Mac, synced via iCloud + GitHub (`giladnass/Repo1`)
- **AI tools with vault access (confirmed):** Claude.ai, Claude Code, Aurora via OpenClaw, Gemini CLI, Perplexity (mcp-remote bridge)
- **AI tools ready to configure:** Manus (streamable HTTP direct), Genspark (streamable HTTP direct)
- **AI tools limited/blocked:** NotebookLM (no MCP client, one-way bridge only), ChatGPT (Plus/Pro read-only), Gemini Web (no MCP client)
- **Full connection status:** [[Memory/tool-configs]]
- **Full tool inventory:** [[Memory/tool-configs]]
- **Communication rule:** No em dashes in any AI output

## Current System State

- Vault is live on GitHub: `giladnass/Repo1`, branch `claude/caveman-lite-vrjM3`
- MCP access layer: basic-memory at `https://memory.giladn.com/mcp/` (token in tool-configs)
- **Phase 0 complete** -- schema locked, templates populated, 4 wiki pages, build plan written
- **Phase 1 complete** -- MCP verified, tool inventory documented, infrastructure documented
- **Phase 2 complete** -- conversion pipeline written and operational (ingest.py, process.py, watch.sh, session_end.py, linkding_export.py); PDFs processed, linkding export run, faster-whisper deployed on Netcup
- **Phase 3 complete** -- Aurora operational on Discord + Telegram, KI-001/KI-004 resolved
- **Phase 3a complete** -- DECISION: Discord/Telegram remain primary interfaces; Open WebUI explicitly NOT adopted as primary (runs on 3000→8080 as optional SSH-tunnel access only)
- **Phase 4 complete** -- Aurora connected to basic-memory MCP, memory rebuilt, SSH key auth fixed, watch.sh LaunchAgent installed
- **Phase 5 complete** -- lint.py created and clean (0 errors), D-003 frontmatter gaps fixed, index.md updated with all wiki pages, file lifecycle finalized (01-source -> 03-done), LaunchAgent confirmed running, vault path confirmed
- D-006 (MCP data contract) finalized: Active
- **U3 Aurora memory writes** -- FIXED: `memory/` directory created, seed file written, AGENTS.md updated with explicit daily persistence rules
- **U4 gemini_bridge.py operational** -- OAuth working, token cached, Context + Inbox Google Docs created, push/pull verified
- **U6 session_capture.py operational** -- end-to-end validation complete, auto-capture working
- **Aurora model regression discovered** -- `kimi-k2.5` returns "Unknown model", Groq fallback rate-limited, falls back to Gemini Flash Lite with ~20s response times

### Aurora / OpenClaw (as of 2026-04-27)

- Primary model: `moonshotai/kimi-k2.5` via OpenRouter -- **REGRESSION: returns "Unknown model" error**
- Fallback 1: `groq/llama-3.1-8b-instant` (14,400 req/day) -- **rate-limited**: 6000 TPM vs ~47K needed
- Fallback 2: `openrouter/google/gemini-2.5-flash-lite` -- current active, ~20s response times
- Channels: Discord (active, groupPolicy=allowlist) + Telegram (active)
- Workspace brain files: global, shared across all channels
- USER.md: correct Hebrew name spelling (גילעד), bilingual response rules
- basic-memory access: native MCP working in v2026.4.24; mcporter fallback still documented
- AGENTS.md updated with explicit mcporter instructions for Aurora
- AGENTS.md updated with daily persistence rules (memory directory created)
- BOOTSTRAP.md deleted -- no more re-introduction on new sessions
- SOUL.md updated: no process narration, outcome-only responses
- compaction.reserveTokensFloor: 512 (not a constraint with 200k ctx model)
- Aurora rebuilt her workspace MEMORY.md from vault content
- SSH key auth fixed on Mac (`netcup_key` added to keychain)
- OpenClaw version: 2026.4.24

## Active Projects

1. **AI Memory System** -- this vault. Build plan: [[Working-Context/knowledge-base-build-plan]]
2. **OpenClaw/Aurora** -- always-on AI agent on Netcup. See [[Wiki/openclaw-aurora]]
3. **Obsidian Codex vault** -- separate vault used by OpenClaw, synced from Google Drive to `/home/openclaw/obsidian/codex-vault` on Netcup

## Infrastructure

- **Mac (M4, 48GB):** interactive work, conversion pipelines (pymupdf4llm, pandoc), Ollama Cloud client
- **Vault path on Mac:** `/Users/giladnass/Library/Mobile Documents/iCloud~md~obsidian/Documents/AI-Memory/`
- **iCloud note:** iCloud strips executable bits from scripts after sync -- run `chmod +x Scripts/watch.sh` if LaunchAgent fails with exit code 126
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

- **KI-001/KI-004 RESOLVED** (2026-04-25): Aurora no longer falls back to Gemini. Fixed by switching primary model to `moonshotai/kimi-k2.6` (200k ctx) and trimming brain files.
- KI-002/KI-003: Minor OpenClaw issues, see known-issues.md
- KI-005: Marker suspended (Apple Silicon MPS bug) -- pymupdf4llm used instead
- **KI-006 PARTIALLY RESOLVED** (2026-04-25): OpenClaw v2026.4.24 surfaces MCP tools natively. mcporter fallback still documented but no longer required for basic-memory access.
- **KI-007 Aurora model regression** (2026-04-27): Primary `kimi-k2.5` returns "Unknown model", Groq fallback rate-limited, resulting in slow Gemini Flash Lite responses (~20s). Fix options: switch to `kimi-k2.6`, debug OpenRouter key, or replace Groq fallback.

## Pipeline Status (as of 2026-04-27)

| Script | Status | Notes |
|---|---|---|
| `Scripts/ingest.py` | Operational | `--move-done ~/AI-Ingestion/03-done` moves originals after conversion |
| `Scripts/process.py` | Operational | `--source-type epub/pdf/etc`, needs `OLLAMA_API_KEY` env var |
| `Scripts/watch.sh` | Running as LaunchAgent | LaunchAgent: `com.giladnass.ai-memory-watcher`, PID confirmed |
| `Scripts/lint.py` | Operational | 0 errors, 16 warnings (em-dashes + broken links in immutable source) |
| `Scripts/session_end.py` | Operational | Automated session logging |
| `Scripts/linkding_export.py` | Operational | Full run completed |
| `Scripts/transcribe.py` | Operational | faster-whisper on Netcup, deployed + tested |
| `Scripts/gemini_bridge.py` | Operational | OAuth working, Context + Inbox Google Docs created |
| `Scripts/session_capture.py` | Operational | Tested end-to-end, updates handoff/log/MEMORY |

### Staging Folder Structure (Mac)

```
~/AI-Ingestion/
  01-source/    <- drop files here (inbox)
  02-converted/ <- raw .md conversions (intermediate, not auto-cleaned yet)
  03-done/      <- originals after successful conversion
```

### Pipeline Behavior

- `draft` status in Obsidian is informational only -- draft pages ARE searchable via Obsidian and basic-memory MCP immediately
- Review = open draft wiki page in Obsidian, change `status: draft` to `status: active` if good
- `02-converted/` files are not auto-cleaned after process.py runs (pending improvement)

## Deferred Design Topics (discuss in future sessions)

1. **Converted-file lifecycle** -- some MD files in `02-converted/` need to be preserved as-is (transcripts, reports); need save/delete decision flow
2. **Visual element preservation** -- charts and images in source docs are lost during conversion; need a strategy to preserve and link visuals to their summaries
3. **Review UX** -- custom interface with status buttons (draft -> active), pipeline status display; Amber app noted as possible editor component; Obsidian plugin as alternative
4. **UX dashboard** -- button-based interface for the full pipeline (convert, summarize, review, commit) with process queue display
5. **process.py --move-done** -- add cleanup for `02-converted/` after successful processing (mirrors ingest.py behavior)

## What the Next Session Should Do

1. **Fix Aurora model routing** -- choose approach: A) switch primary to `kimi-k2.6`, B) debug OpenRouter key, or C) replace Groq fallback with higher-throughput model
2. **U5 Drive webhook + visual preservation** -- design strategy for auto-ingest and chart/image retention
3. **Genspark MCP setup** -- deferred: UI bug blocks text input in Add New MCP screen
