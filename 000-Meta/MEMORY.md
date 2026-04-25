---
title: MEMORY
type: note
tags: [meta, system, ai-memory]
created: 2026-04-20
permalink: ai-memory/000-meta/memory
---

# Persistent Context

*Last updated: 2026-04-25 -- Claude Code, session: Netcup cron hardened (stash+pull, moved to openclaw user)*

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
- **Phase 4 complete** -- Aurora connected to basic-memory MCP, memory rebuilt, SSH key auth fixed, watch.sh LaunchAgent installed
- **Phase 5 complete** -- lint.py created and clean (0 errors), D-003 frontmatter gaps fixed, index.md updated with all wiki pages, file lifecycle finalized (01-source -> 03-done), LaunchAgent confirmed running, vault path confirmed
- D-006 (MCP data contract) finalized: Active

### Aurora / OpenClaw (as of 2026-04-22)

- Primary model: `moonshotai/kimi-k2.5` via OpenRouter (200k ctx)
- Fallback 1: `ollama/minimax-m2.5:cloud` (Ollama Cloud, user: giladn)
- Fallback 2: `openrouter/google/gemini-2.0-flash-001`
- Channels: Discord (active, groupPolicy=allowlist) + Telegram (active)
- Workspace brain files: global, shared across all channels
- USER.md: correct Hebrew name spelling (גילעד), bilingual response rules
- basic-memory access via `mcporter` skill workaround (native MCP broken -- KI-006: streamable-http bug #65590/#66940)
- AGENTS.md updated with explicit mcporter instructions for Aurora
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

- **KI-001/KI-004 RESOLVED** (2026-04-22): Aurora no longer falls back to Gemini. Fixed by switching primary model to `moonshotai/kimi-k2.5` (200k ctx).
- KI-002/KI-003: Minor OpenClaw issues, see known-issues.md
- KI-005: Marker suspended (Apple Silicon MPS bug) -- pymupdf4llm used instead
- **KI-006 ACTIVE**: OpenClaw MCP streamable-http bug (issues #65590/#66940) -- workaround: mcporter skill for basic-memory calls

## Pipeline Status (as of 2026-04-22)

| Script | Status | Notes |
|---|---|---|
| `Scripts/ingest.py` | Operational | `--move-done ~/AI-Ingestion/03-done` moves originals after conversion |
| `Scripts/process.py` | Operational | `--source-type epub/pdf/etc`, needs `OLLAMA_API_KEY` env var |
| `Scripts/watch.sh` | Running as LaunchAgent | LaunchAgent: `com.giladnass.ai-memory-watcher`, PID confirmed |
| `Scripts/lint.py` | Operational | 0 errors, 16 warnings (em-dashes + broken links in immutable source) |
| `Scripts/session_end.py` | Operational | Automated session logging |
| `Scripts/linkding_export.py` | Operational | Full run completed |
| `Scripts/transcribe.py` | Operational | faster-whisper on Netcup, deployed + tested |

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

1. **Aurora model check** -- verify kimi-k2.5 primary on Netcup (may have drifted to minimax)
2. **Clean `02-converted/`** -- 26 dirs of dead staging data, originals already in 03-done/
3. **Genspark MCP setup** -- AI Browser > wrench icon > Add New MCP Server, paste endpoint URL
4. **Manus MCP status** -- check Relay bot update when available
5. **Mac git push hook** -- instant vault sync to Netcup on file save
