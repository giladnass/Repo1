---
title: Claude
type: note
permalink: ai-memory/claude
---

# Claude Code Master Context: Gilad's AI Stack
*Last updated: 2026-04-25.*
*Read this in full before making any changes. Some infrastructure is live and operational. Breaking it has real consequences.*

---

## How to Use This Document

This document covers three separate, ongoing projects that share infrastructure and personnel (one human, various AI tools) but have distinct goals. **Do not conflate them.** When working on any one project, be aware of the others — not to work on them, but to ensure your actions don't create obstacles for them. Where an action can incidentally advance or unblock another project at low cost, note it and flag it to Gilad; don't execute it unilaterally.

The three projects:

| # | Project | One-Line Goal |
|---|---|---|
| P1 | **OpenClaw / Aurora** | A self-hosted AI agent (Aurora) deployed on a cloud server, reachable via Telegram/Discord/web, capable of using tools and consuming knowledge from Gilad's full stack |
| P2 | **Shared Memory Pool** | A single MCP-accessible memory layer that every AI tool in the stack can simultaneously read from and write to, providing cross-tool persistent context |
| P3 | **Long-Term Knowledge Repository** | A living, LLM-powered, ingestion-automated, universally queryable knowledge base for all of Gilad's accumulated research, notes, and information |

P2 and P3 share the same vault and MCP infrastructure. P1 will eventually consume from P2/P3. They are not the same project.

---

## Project P1: OpenClaw / Aurora Agentic Infrastructure

### Goal
Aurora is a self-hosted AI assistant running on the Netcup server. It handles Gilad's requests via Telegram, Discord, and a web dashboard. The P1 goal is a fully operational, stable, correctly-routed agent that uses the right model at the right tier, can invoke tools (including memory and Google Workspace), and doesn't crash or fall back silently.

### Current Status
Operational. Both active blockers resolved in April 2026-04-25 session:
- U1 resolved: Trimmed brain files (DREAMS.md archived), disabled dreaming plugin, switched primary to cloud models
- U2 resolved: Updated to OpenClaw v2026.4.24, MCP tools now surfacing natively. Aurora can read/write basic-memory.
Aurora is reachable via Discord and Telegram, responds in ~3 seconds on primary model.

### Key Components

**OpenClaw binary:** `/home/openclaw/.npm-global/bin/openclaw`
Run all commands as the `openclaw` user:
```bash
sudo -u openclaw bash -c 'export PATH=/home/openclaw/.npm-global/bin:$PATH && openclaw config set ...'
```

**Critical config rule:** Never edit `openclaw.json` directly. Always use `openclaw config set`. Exception: `mcporter.json` must be edited directly (see below).

**Model config (do not change):**
- `models.mode=replace` — auto-discovery disabled. This is non-negotiable; enabling it causes OOM crashes.
- Primary: `ollama/qwen2.5:1.5b` — `contextWindow: 2048`, `maxTokens: 512`
- Fallback 1: `groq/llama-3.1-8b-instant` (14,400 req/day)
- Fallback 2: `openrouter/google/gemini-2.0-flash-001` (paid)
- OpenClaw enforces a 16k token minimum context window internally. Setting `contextWindow: 2048` in OpenClaw config while keeping `OLLAMA_NUM_CTX=16384` in Ollama is intentional and correct — they serve different purposes.

**Ollama config (do not change):**
```ini
OLLAMA_HOST=0.0.0.0
OLLAMA_NUM_CTX=16384
OLLAMA_MAX_LOADED_MODELS=1
OLLAMA_KEEP_ALIVE=5m
OLLAMA_NUM_THREADS=8
OLLAMA_FLASH_ATTENTION=1
OLLAMA_KV_CACHE_TYPE=q8_0
OLLAMA_NUM_PARALLEL=1
```
Override file: `/etc/systemd/system/ollama.service.d/override.conf`

**Ollama models installed (do not add to this list without explicit approval):**
| Model | Size | Role |
|---|---|---|
| `qwen2.5:1.5b` | ~1GB | Primary |
| `deepseek-r1:1.5b` | ~1.1GB | Reasoning fallback |
| `llama3.2:latest` | 2.0GB | Secondary |

**Aurora brain files:** `/home/openclaw/.openclaw/workspace/` (`SOUL.md`, `IDENTITY.md`, `AGENTS.md`)
**Per-agent brain files:** `/home/openclaw/.openclaw/agents/main/agent/` — these load at runtime and consume context budget. Total word count must stay under ~1500 words or context budget overflows and Aurora times out.
**Session store:** `/home/openclaw/.openclaw/agents/main/sessions/sessions.json` — delete this file directly to reset session state. `openclaw sessions clear` does not exist.

**Composio (Google Workspace integration):**
- Plugin: `@composio/openclaw-plugin`, consumer key `ck_zQAH84mLsnNDinbhs3qk`
- Managed at `dashboard.composio.dev` — browser-based auth only. Never attempt CLI OAuth on the server (every invocation generates a new PKCE challenge that immediately invalidates the previous token).

**mcporter (MCP tool invocation layer):**
Config at `~/.mcporter/mcporter.json` — this takes precedence over `/home/openclaw/.openclaw/workspace/config/mcporter.json`. Always edit the home-directory file. Edit directly; `openclaw config set` does not manage this file.
Syntax uses dot notation for server/tool and colon notation for arguments:
```
basic-memory.search_notes query:"search term"
basic-memory.write_note title:"Title" content:"content"
```

### P1 Roadmap
- [x] OpenClaw deployed on Netcup
- [x] Telegram channel working
- [x] Ollama installed and tuned; OOM issue resolved
- [ ] **Fix U1:** Aurora falling back to Gemini (brain file bloat diagnosis)
- [ ] **Fix U2:** OpenClaw version bug blocking MCP tool surfacing — monitor for patch
- [ ] OpenClaw ↔ basic-memory integration (blocked by U2)
- [ ] Discord migration + multi-agent architecture (see `roadmap-openclaw-discord-migration` in vault)
- [ ] Open WebUI formally adopted as primary chat UI (currently deployed, port 3000→8080, not primary)

### P1-Specific Obstacles Solved
**OOM Crashes (A1):** `models.mode=replace` + hardcoded context windows + large model removal. See model config above.
**Config Mutation Bug (A2):** A known OpenClaw bug writes the active fallback model back into config. Clear by deleting `sessions.json` directly.
**Composio OAuth on Headless Server (A3):** Use `dashboard.composio.dev` browser flow only.
**Docker→Host Connectivity (A4):** Use `--add-host=host.docker.internal:host-gateway` and `http://host.docker.internal:11434` in container config.
**CLI User Context (A5):** All OpenClaw commands must run as the `openclaw` user with explicit PATH export.

---

## Project P2: Shared Memory Pool

### Goal
A single, always-on MCP endpoint that every AI tool in Gilad's stack — Claude Desktop, Claude.ai web, Claude mobile, Claude Code, OpenClaw, Perplexity, ChatGPT, Gemini, and others — can connect to simultaneously. Any tool can read from it and write to it. Cross-tool persistent context becomes possible: a decision made in Claude.ai is visible to OpenClaw; a note written by Claude Code is queryable by Perplexity.

### Current Status
Core infrastructure live. Claude Desktop, Claude.ai web, and Claude mobile are connected and working. All other tools either pending trivial config or blocked by the OpenClaw version bug.

### The MCP Endpoint
```
https://memory.giladn.com/mcp/ebc69cbd338019004dfd1738a033ced1e22e21ff62a41b41ef0b8caf5d9fb3a5
```
This URL is the API key. Treat it as a credential. Authentication is path-based — no header-based auth. Any tool that supports remote MCP connects by pointing at this URL.

### Connection Status
| Tool | Connection Method | Status |
|---|---|---|
| Claude Desktop (Mac) | Local stdio MCP | ✅ Working |
| Claude.ai web | Remote MCP via URL | ✅ Working |
| Claude mobile app | Remote MCP via URL | ✅ Working |
| Claude Code | Local vault + remote MCP | 🔲 Not yet connected |
| OpenClaw | mcporter → basic-memory | ⚠️ Blocked by U2 (version bug) |
| Perplexity / Manus / Genspark | Remote MCP via URL | 🔲 Pending — trivial, just URL config |
| ChatGPT | Remote MCP via URL | 🔲 Pending |
| Gemini | Google Docs bridge | ❌ Architecture designed; not built |

### The basic-memory MCP Server
basic-memory (v0.20.3) is the MCP server layer. It indexes the AI-Memory vault's Markdown files and exposes read/write tools to connected AI clients.

**Installation:** Under the `openclaw` user on Netcup. Also installed locally on Mac for Claude Desktop.
**Config (server):** `~/.basic-memory/config.json` — `"default_project": "ai-memory"` (kebab-case). Never edit the SQLite DB (`memory.db`) directly — JSON config takes precedence and resets DB state on startup.
**Config (Mac):** `~/.basic-memory/config.json` — same setting.
**Systemd service:** Runs on port 8765. nginx proxies it to `memory.giladn.com`.

```bash
# Key commands:
basic-memory tool search-notes "query term"   # positional arg, NOT --query flag
basic-memory reindex
basic-memory mcp --transport streamable-http --host 0.0.0.0 --port 8765 --project AI-Memory

# Health check — this is CORRECT behavior, not an error:
# {"jsonrpc":"2.0","id":"server-error","error":{"code":-32600,"message":"Not Acceptable: Client must accept text/event-stream"}}
```

### P2 Roadmap
- [x] basic-memory installed on Mac and Netcup
- [x] nginx + Cloudflare SSL; remote MCP live at memory.giladn.com
- [x] Claude Desktop, Claude.ai web/mobile connected
- [ ] Connect Claude Code (local + remote)
- [ ] Connect Perplexity, Manus, Genspark (trivial — URL config only)
- [ ] Connect ChatGPT
- [ ] Fix OpenClaw ↔ basic-memory (blocked by P1/U2)
- [ ] Build Gemini Google Docs bridge (architecture exists; no code written)
- [ ] Git push hook on Mac for instant sync (currently 5-min cron on Netcup side only)

### P2-Specific Obstacles Solved
**basic-memory CLI syntax (B1):** Positional arg only; kebab-case project name in config.
**SQLite vs JSON config (B2):** Never edit the DB. JSON config is authoritative.
**mcporter syntax (B3):** Dot + colon notation. Home-directory `mcporter.json` takes precedence.
**OpenClaw defaulting to Composio (B4):** Unsolved — pending P1/U2 version fix.
**File creation with special characters (B6):** Use Python scripts, not heredocs (backticks break heredocs).
**NotebookLM not in Drive API (B7):** Use `notebooklm-mcp` or browser automation. Drive API returns empty results for NotebookLM notebooks.

### Gemini Bridge Architecture (Designed, Not Built)
Two Google Docs: an **Inbox** doc and a **Context** doc. A bridge script reads the vault → populates the Context doc. Gemini writes outputs to the Inbox doc → bridge script ingests those back into the vault. Zero code written; flagged for future implementation.

---

## Project P3: Long-Term Knowledge Repository

### Goal
A living, self-compounding, LLM-powered knowledge base. Everything Gilad reads, watches, or researches gets ingested, converted to structured Markdown, tagged, summarized, cross-linked, and made queryable — by any AI tool, at any time, from any device. Inspired by Andrey Karpathy's LLM Wiki concept. The end state is a fully automated ingestion pipeline: drop a PDF, paste a URL, record a voice note → it lands in the vault, processed and linked, without manual work.

### Current Status
The vault and its access layer (P2) are live. P3 itself — the intelligence and automation layer on top — has not started. The vault is currently populated manually.

### The Vault

**The only vault is AI-Memory. There are no other vaults.**

| Location | Path |
|---|---|
| Mac (primary, iCloud-backed) | `/Users/giladnass/Library/Mobile Documents/iCloud~md~obsidian/Documents/AI-Memory` |
| Netcup (server clone, Git-synced) | `/home/openclaw/AI-Memory` |
| GitHub (sync hub) | `https://github.com/giladnass/Repo1` |

**Sync mechanism:** 5-minute cron job on Netcup pulls from GitHub. Mac changes must be committed and pushed to GitHub to propagate to the server. There is currently no push hook on the Mac — sync is pull-only from the server side.

**Vault structure (do not alter):**
```
AI-Memory/
├── 000-Meta/          # Schema definitions, session logs, handoff notes, index
├── Wiki/              # Permanent knowledge pages (the "library")
├── Sources/           # Raw/processed source material (immutable originals)
├── Working-Context/   # Active project roadmaps, session handoffs
├── Templates/         # Frontmatter templates (wiki-page, weekly-review, source-note)
└── Memory/            # Persistent AI-facing context (preferences, tool configs)
```
Schema is defined in `000-Meta/CLAUDE.md`. All files: YAML frontmatter, `[[wikilinks]]`, tags.

### Ingestion Pipeline (Not Started)

**Core architectural decision:** All source material is pre-converted to Markdown before ingestion. Raw binary formats (PDF, DOCX, MP4, etc.) are never fed directly to basic-memory. MD is inspectable, correctable, portable, and Git-versionable.

**Processing split:**
- Lightweight conversions (PDF, Office docs, EPUB) → run on Mac
- Heavy compute (audio transcription, video frame/slide extraction) → run on Netcup overnight

**Planned tools (none installed yet):**
| Tool | Purpose | Run On |
|---|---|---|
| `marker` | PDF → Markdown (ML-based, complex layouts) | Mac |
| `pymupdf4llm` | PDF → Markdown (fast, simple PDFs) | Mac |
| `nougat` (Meta) | Academic PDFs with equations → LaTeX-preserved MD | Mac |
| `pandoc` | DOCX / PPTX / EPUB → Markdown | Mac |
| `faster-whisper` | Audio/video transcription (4–8x faster than Whisper) | Netcup |
| `docling` (IBM) | Unified document conversion incl. chart understanding | To evaluate |
| `ffmpeg` | Video frame/audio extraction | Netcup |
| `DePlot` / `ChartOCR` | Chart image → structured data table | To evaluate |
| `ArchiveBox` / Firecrawl | Web page capture and archival | To evaluate |
| `linkding` | Self-hosted bookmark manager as capture point | To evaluate |
| Claude API (batch) | Content triage, tagging, summarization | Cloud |

### P3 Roadmap
- [x] Vault created with full folder structure and schema
- [x] GitHub repo created; Git sync between Mac and Netcup operational
- [ ] Install and test ingestion conversion tools (per format)
- [ ] File watcher on Mac (`fswatch` + conversion script)
- [ ] Routing logic: full ingest vs. summary-only vs. index-only
- [ ] Google Drive webhook → auto-ingest new files
- [ ] Install `faster-whisper` on Netcup; scheduled audio/video queue
- [ ] Claude API batch processing for content triage and tagging
- [ ] Claude conversation capture: end-of-session Claude Code write-to-vault routine (U6)
- [ ] Seed vault from existing NotebookLM notebooks and research outputs
- [ ] Define "contribution contract": entry format that works across all connected tools
- [ ] Git push hook on Mac for instant sync on file save

### P3-Specific Unresolved Problem
**Claude conversation capture (U6):** Claude.ai has no official export API, so planning sessions are currently lost unless manually copied. The recommended approach: Claude Code sessions are the primary vehicle for knowledge-building work (Claude Code has full filesystem access and can write directly to the vault). A systematic end-of-session save routine needs to be designed.

---

## Shared Infrastructure

Both P2 and P3 depend on the following. Changes here affect both projects — plan accordingly.

### Netcup Server
- **OS**: Ubuntu 24.04 | **RAM**: 32GB | **CPU**: 12 vCPUs (AMD EPYC) | **No GPU**
- **Public IP**: `152.53.244.42` | **Tailscale IP**: `100.127.32.127`
- **SSH**: `Host netcup` alias in `~/.ssh/config` on Mac

**All running services:**
| Service | User | Port | Notes |
|---|---|---|---|
| OpenClaw gateway (P1) | `openclaw` | internal | `systemctl --user restart openclaw-gateway` as `openclaw` user |
| basic-memory MCP (P2/P3) | `openclaw` | 8765 | systemd auto-start |
| nginx (P2/P3) | root | 80/443 | Reverse proxy for memory.giladn.com |
| Ollama (P1) | root | 11434 | `OLLAMA_HOST=0.0.0.0` |
| AnythingLLM (P1) | root | 3001 (localhost) | SSH tunnel only |
| Open WebUI (P1) | root | 3000→8080 | `ssh -L 3003:127.0.0.1:3000` |
| IPTVX | iptvx | 9191 (public) | Unrelated; do not touch |

### Mac
- **Machine**: MacBook Pro M4, 48GB unified memory
- **Inference**: 50–80 tokens/sec (mid-size models) — use for speed-sensitive tasks
- **Netcup inference**: 30–50 tokens/sec (sub-2B models only) — use for always-on/background tasks

### NotebookLM
Used as Gilad's primary research synthesis layer before bringing findings to Claude Code for execution. Key notebooks: "Deploying Openclaw on Netcup", "Local LLMs". Access via `notebooklm-mcp`. Use `notebook_query` with `timeout: 90`. Cannot be accessed via Google Drive API — browser/MCP only.

### CoWork
Desktop Claude client on Mac. `/schedule` for scheduled tasks. Only runs when Mac is awake. **Files are the only reliable inter-tool bridge** — do not design workflows that depend on real-time communication between claude.ai, Claude Code, CoWork, and OpenClaw.

---

## Active Unresolved Problems

### U1: Aurora Falls Back to Gemini [P1]
**Suspected cause**: Brain files in `/home/openclaw/.openclaw/agents/main/agent/` exceed the 2048-token context budget, leaving zero tokens for the user message → timeout → fallback.
```bash
sudo -u openclaw bash -c 'wc -w /home/openclaw/.openclaw/agents/main/agent/*.md'
```
If total exceeds ~1500 words: trim brain files. Move non-session-critical instructions to on-demand retrieval.

### U2: OpenClaw MCP Tool Surfacing — Version Bug [P1, blocks P2]
In OpenClaw versions 2026.4.8 and 2026.4.9, `mcporter` does not surface MCP tools to the agent layer and ignores API key headers. This blocks both Google Workspace (Composio) and basic-memory (P2) integration from OpenClaw.
Monitor: `https://github.com/openclaw/openclaw/releases`. No workaround; do not attempt to fix until a patched version is available.

### U3: Aurora Memory Writes Unconfirmed [P1]
Daily memory files (`/home/openclaw/.openclaw/workspace/memory/YYYY-MM-DD.md`) are the intended mechanism for cross-session context. Unconfirmed whether Aurora is actively writing or reading them. Check for recent files; if absent, add explicit write instructions to `AGENTS.md`.

### U4: Gemini Google Docs Bridge [P2]
Architecture designed; zero code written. Two Google Docs (Inbox + Context). Bridge script reads vault → populates Context doc → monitors Inbox doc for Gemini outputs → ingests back to vault.

### U5: Ingestion Pipeline [P3]
The entire P3 automation layer is unstarted. The vault is manually fed. No tools installed, no watchers, no routing. Largest single body of remaining work.

### U6: Claude Conversation Capture [P3]
Claude.ai has no export API. Valuable planning sessions are lost unless manually saved. Claude Code sessions writing directly to the vault is the working hypothesis for a solution.

---

## Non-Negotiable Rules

These apply across all three projects. Violations cause immediate or cascading breakage.

1. **Do not change the AI-Memory vault folder structure.** Schema in `000-Meta/CLAUDE.md` governs it; basic-memory is indexed against it.
2. **Do not edit `~/.basic-memory/memory.db` directly.** JSON config is authoritative.
3. **Do not edit `openclaw.json` directly.** Use `openclaw config set` as the `openclaw` user.
4. **`models.mode=replace` must stay set.** Auto-discovery is a catastrophic failure mode on this hardware.
5. **All OpenClaw commands must run as the `openclaw` user** with explicit PATH: `sudo -u openclaw bash -c 'export PATH=/home/openclaw/.npm-global/bin:$PATH && ...'`
6. **`mcporter.json` must be edited directly** at `~/.mcporter/mcporter.json` — not via `openclaw config set`, not the workspace config path.
7. **The MCP URL is the API key.** Do not log it or hardcode it in committed files.
8. **Use Python scripts, not heredocs,** for any file creation containing Markdown code blocks.
9. **The MCP health-check `"Not Acceptable"` curl response is correct.** Do not try to fix it.
10. **Vault syncs via Git.** Files written to AI-Memory on Mac must be committed and pushed to reach Netcup. Files written on Netcup are pulled by cron every 5 minutes.
11. **Do not add Ollama models without explicit approval.** The model set is intentionally minimal.
12. **`openclaw sessions clear` does not exist.** Delete `sessions.json` directly.
13. **Context window math is critical.** At 2048 tokens: system prompt + brain files + tool definitions + conversation history + user message must all fit. Any unchecked growth breaks the budget.
14. **Files are the only reliable inter-tool bridge.** No real-time communication assumptions.
15. **AI-Memory is the only vault.** Do not create, reference, or configure any additional vault unless explicitly instructed and documented here first.

---

*Last updated: 2026-04-25.*