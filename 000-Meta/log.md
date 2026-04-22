---
title: log
type: note
tags: [meta, session-log]
created: 2026-04-12
permalink: ai-memory/000-meta/log
---

# Session Log

---

## 2026-04-22 -- Phase 5: Pipeline Hardened + LaunchAgent Live

**Tool:** Claude Code
**Branch:** claude/caveman-lite-vrjM3

### Accomplished

- Created `Scripts/lint.py`: full vault validation (frontmatter, vocab, naming, links, orphans, stale, em-dashes)
- Fixed 20 D-003 frontmatter errors across 000-Meta/ and Memory/ files
- Fixed Sources/wiki-session-knowledge-ingestion-pipeline.md: type corrected to source
- Updated index.md: added 14 orphan wiki pages from PDF batch processing
- Added `--move-done` to ingest.py: source files now move to `03-done/` after conversion
- Updated watch.sh: passes `--move-done` by default, added DONE_DIR
- Confirmed vault path on Mac: `/Users/giladnass/Library/Mobile Documents/iCloud~md~obsidian/Documents/AI-Memory/`
- LaunchAgent confirmed running (PID 44692)
- Diagnosed and fixed iCloud executable bit stripping (chmod +x required after iCloud sync)

### Key Findings

- iCloud Drive strips executable bits from scripts after syncing -- LaunchAgent will fail with exit code 126; fix with `chmod +x Scripts/watch.sh`
- `status: draft` in Obsidian is informational only -- draft pages are immediately searchable via Obsidian and basic-memory MCP
- `02-converted/` files are intermediate staging only; they are not auto-cleaned after process.py runs

### Deferred

- Converted-file save/delete decision flow
- Visual element preservation strategy
- Review UX (status buttons, pipeline display, Amber assessment)
- UX dashboard for full pipeline
- process.py --move-done for 02-converted cleanup

---

## 2026-04-22 -- Phase 4: Full Pipeline + Aurora MCP Integration

**Tool:** Claude Code
**Branch:** claude/caveman-lite-vrjM3

### Accomplished

- Deleted BOOTSTRAP.md from Aurora workspace (was re-running on every session)
- Updated SOUL.md: outcome-only response style, no process narration
- Set compaction.reserveTokensFloor to 20000
- Connected Aurora to basic-memory MCP via mcp-remote stdio workaround
- Aurora rebuilt workspace MEMORY.md from vault
- ingest.py confirmed working on Mac (files previously converted)
- faster-whisper confirmed deployed and tested on Netcup
- linkding full export completed
- Fixed SSH key auth on Mac (netcup_key added to keychain)

### Key Finding

OpenClaw 2026.4.21 has a bug where streamable-http MCP servers fail silently or with 400 errors due to missing Accept header (issues #65590, #66940). Workaround: use mcp-remote as a stdio proxy. Fix in PR #66966, not yet released.

---

## 2026-04-22 -- Phase 3: Aurora Migration + KI-001/KI-004 Fix

**Tool:** Claude Code
**Branch:** claude/caveman-lite-vrjM3

### Accomplished

- Fixed `.claude/` submodule error in obsidian-git (added to .gitignore)
- Migrated Aurora to Discord: allowFrom, dmPolicy, groupPolicy configured
- Updated USER.md: Hebrew name spelling (גילעד), language rules
- Created `llama3.2-32k` Ollama custom model (Modelfile, 32k ctx) -- too small for agentic use
- Diagnosed KI-001/KI-004 root cause: 16k context floor + small local models
- Researched and implemented model chain: Kimi K2.5 (primary) > minimax-m2.5:cloud > Gemini Flash
- Verified Ollama Cloud login on Netcup (giladn, Pro)
- Resolved Discord CRITICAL security warning (groupPolicy=allowlist)
- All 3 Aurora sessions confirmed on Kimi K2.5 (200k ctx)

### Pending

- 13 PDFs on Mac (ingest.py ready)
- faster-whisper on Netcup
- basic-memory MCP integration with Aurora
- linkding full export

---

## 2026-04-20 — Phase 0: Foundation Build

**Tool:** Claude Code
**Branch:** claude/caveman-lite-vrjM3
**Session type:** System architecture + vault bootstrapping

### Accomplished

- Audited full vault state against mission requirements
- Locked 8 founding decisions (schema, naming, contracts, model strategy)
- Populated all 4 Templates with actual content (were empty stubs)
- Created `Working-Context/knowledge-base-build-plan.md` — 6-phase implementation plan
- Processed `Sources/wiki-session-knowledge-ingestion-pipeline` into 4 wiki pages:
  - `Wiki/ai-memory-system-overview.md`
  - `Wiki/ingestion-pipeline.md`
  - `Wiki/format-conversion-tools.md`
  - `Wiki/visual-data-preservation.md`
- Populated `000-Meta/MEMORY.md` with current system state and open questions
- Populated `000-Meta/index.md` with full content map
- Populated `000-Meta/decisions.md` with all founding decisions
- Added YAML frontmatter to `Sources/wiki-session-knowledge-ingestion-pipeline.md`
- Committed and pushed to `claude/caveman-lite-vrjM3`

### Sources Ingested

- `Sources/wiki-session-knowledge-ingestion-pipeline` (2026-04-12 Claude.ai session) → processed into 3 wiki pages

### Open at End of Session

- 6 questions requiring human input (see MEMORY.md)
- Phase 1 not started — requires human input on MCP server, tool inventory, OpenClaw/Aurora
- Memory/profile.md and Memory/tool-configs.md remain empty

---

## 2026-04-12 — Ingestion Pipeline Research

**Tool:** Claude.ai
**Session type:** Research and decision-making

Researched and documented: format conversion tools by type (PDF/Office/EPUB/audio/video), visual data preservation strategies, video slide extraction pipeline, processing location strategy, URL/bookmark pipeline, automation gap analysis.

Output: `Sources/wiki-session-knowledge-ingestion-pipeline.md`

Decisions made: D-001 (convert to MD first), D-007 (processing location strategy).

---

## 2026-04-20 -- Phase 1: Context Ingestion (Claude Code, continued)

**Tool:** Claude Code
**Branch:** claude/caveman-lite-vrjM3

### Accomplished

- Ingested full infrastructure context from Gilad
- Populated Memory/profile.md (working style, communication rules, stack philosophy)
- Populated Memory/tool-configs.md (full tool inventory: MCP, claude.ai integrations, Netcup services, cloud LLMs)
- Created Wiki/openclaw-aurora.md
- Created Wiki/netcup-server.md
- Created 000-Meta/known-issues.md (KI-001 through KI-004)
- Updated CLAUDE.md (added no-em-dash rule)
- Finalized D-006 (MCP contract: Draft to Active)
- Updated MEMORY.md, index.md, decisions.md, handoff.md

### Key Findings

- basic-memory satisfies D-006. MCP is fully operational.
- OpenClaw KI-001 root cause is KI-004 (16k minimum context vs. qwen2.5:1.5b optimal 2048).
- Codex vault (OpenClaw) and AI-Memory are separate vaults -- no current integration.
- No GPU on Netcup -- SAM visual extraction is CPU-only.
- Zapier + Google Drive already connected to claude.ai -- Phase 2 automation simpler than planned.
- Strategic opportunity: Aurora + basic-memory MCP = always-on ingestion agent.

---

## 2026-04-20 -- Phase 2: Conversion Pipeline (Claude Code, continued)

**Tool:** Claude Code
**Branch:** claude/caveman-lite-vrjM3

### Accomplished

- Diagnosed Marker instability: surya Apple Silicon MPS bug (KI-005); CPU fallback too slow
- Decision D-009: switched primary PDF converter to pymupdf4llm
- Added KI-005 to known-issues.md
- Written Scripts/ingest.py (PDF via pymupdf4llm, DOCX/EPUB/PPTX via pandoc, batch + single-file modes)
- Written Scripts/watch.sh (fswatch watcher for source folder)
- Updated format-conversion-tools.md with corrected tool status
- Updated decisions.md, known-issues.md, MEMORY.md, index.md

### Pending

- 13 PDFs in queue on Mac -- need `pip install pymupdf4llm && python3 Scripts/ingest.py`
- Pandoc conversion untested (installed but no test run documented)
- faster-whisper on Netcup not yet set up
- linkding not yet set up

---

## 2026-04-21 -- Phases 3-5 Complete, Ollama Cloud

**Tool:** Claude Code
**Branch:** claude/caveman-lite-vrjM3

### Accomplished
- Phase 3 complete: wrote process.py with three-step LLM pipeline (triage, summarization, cross-referencing)
- Refactored process.py to use LiteLLM for runtime model/provider switching
- Fixed Qwen3 reasoning model bug (thinking tokens consuming max_tokens)
- Batch of 13 PDFs processed successfully overnight
- Phase 4 complete: wrote session_end.py for automated session logging
- Phase 5 complete: wrote linkding_export.py for bookmark ingestion
- Mac M4 48GB established as primary inference machine
- Switched to Ollama Cloud (qwen3.5:cloud for triage, glm-5:cloud for summarization)
- Reduced processing time: 2.5 min/doc vs 11 min locally

### Key Findings
- Qwen3 reasoning models emit thinking tokens that count against max_tokens, requiring strip + higher limit
- LiteLLM provides clean abstraction for swapping models without code changes
- Cloud inference prevents Mac M4 overheating on batch jobs
- Netcup role narrowed to transcription only; inference moved to Mac + cloud

### Pending
- Phase 6: OpenClaw basic-memory MCP integration
- Fix KI-001/KI-004 by testing llama3.2:latest as OpenClaw primary
- LINT automation setup
- Full linkding bookmark batch export and processing

---

## 2026-04-21 -- Session End Script Test Run

**Tool:** Claude Code
**Branch:** claude/caveman-lite-vrjM3

### Accomplished
- Executed session_end.py with --pbpaste flag for clipboard-based session logging
- Verified script integration with vault automation pipeline

### Key Findings
- session_end.py successfully reads from clipboard and routes to LLM processing
- Phase 4 automation working as designed

### Pending
- Phase 6: OpenClaw basic-memory MCP integration
- Test llama3.2:latest as OpenClaw primary model
- LINT automation setup
- Full linkding batch processing
- Transcription setup on Netcup

---

## 2026-04-21 -- Phases 3-5 Complete, Pipeline Operational

**Tool:** Claude Code
**Branch:** claude/caveman-lite-vrjM3

### Accomplished
- Phase 3 complete: wrote process.py with three-step LLM pipeline (triage, summarization, cross-referencing)
- Refactored to use LiteLLM for runtime model/provider configuration
- Fixed Qwen3 reasoning bug: thinking tokens consumed max_tokens, resolved by stripping think blocks and raising max_tokens to 2048
- Batch of 13 PDFs processed successfully overnight
- Phase 4 complete: wrote session_end.py for automated session logging
- Phase 5 complete: wrote linkding_export.py for bookmark ingestion
- Added Mac M4 48GB as primary inference machine
- Switched to Ollama Cloud models (qwen3.5:cloud for triage, glm-5:cloud for summarization to avoid Mac overheating)

### Key Findings
- LiteLLM integration allows flexible model/provider flags at runtime
- Qwen3 reasoning models require stripped think blocks and max_tokens=2048 minimum
- Ollama Cloud processing: 2.5 min/doc vs 11 min locally on Mac
- Netcup role refined to transcription only

### Pending
- Phase 6: OpenClaw basic-memory MCP integration for Aurora vault writes via Telegram
- Test llama3.2:latest as OpenClaw primary model to resolve KI-001/KI-004
- Set up automated LINT validation for vault files
- Run full linkding bookmark batch through pipeline
- Install and test faster-whisper on Netcup for transcription
