---
title: handoff
type: note
tags: [meta, session, handoff]
created: 2026-04-20
permalink: ai-memory/000-meta/handoff
---

## 2026-04-25 -- U1/U2 Resolved, Docs Synced, Model Switched to kimi-k2.5

### What Was Accomplished

**Fixed Aurora model fallback (U1) and MCP surfacing (U2):**
- OpenClaw primary switched from `minimax-m2.5:cloud` to `moonshotai/kimi-k2.5` via OpenRouter (200k ctx)
- OpenClaw gateway restarted (PID 1345643); sessions.json cleared
- Verified config: primary = kimi-k2.5, fallback 1 = groq/llama-3.1-8b-instant, fallback 2 = gemini-2.5-flash-lite
- All blockers resolved in v2026.4.24

**Synced all stale documentation to current reality:**
- CLAUDE.md: P1 operational, P3 operational, sync mechanism updated, model config updated
- MEMORY.md: Aurora model, reserveTokensFloor, KI-001/KI-004 resolved, KI-006 partially resolved
- tool-configs.md: Manus connected, Genspark blocked, model table updated
- known-issues.md: OpenClaw version bumped to 2026.4.24

**Mac vault sync hardening:**
- `vault-sync.sh` now runs `git pull origin main --rebase` before push
- LaunchAgent reloaded and verified
- 02-converted/ cleaned (bm1, bm2 deleted — already in Sources/ and Wiki/)

### What Needs Human Review

- Aurora conversation test on Discord to confirm kimi-k2.5 primary is live and fast
- ReserveTokensFloor is 512 (docs updated to reflect actual); not a constraint with 200k ctx

### Deferred Topics

- Genspark MCP: UI bug persists, deferred for later research
- Visual element preservation strategy
- Google Drive webhook auto-ingest

### What to Do Next

1. **Aurora Discord test** — send a message, confirm ~3s response on kimi-k2.5
2. **Google Drive webhook auto-ingest** — largest remaining unbuilt P3 feature
3. **Visual element preservation** — charts/images lost during conversion; design strategy

---

## 2026-04-25 -- Netcup Cron Hardened

### What Was Accomplished

**Hardened Netcup vault sync cron:**
- Root cause: `*/5 * * * *` cron running as root with `git@github.com` remote, but root had no GitHub SSH key / known_hosts entry for github.com
- Solution: moved cron from root to `openclaw` user; added `export HOME=/home/openclaw` so SSH finds keys and config
- Added github.com host key to `/home/openclaw/.ssh/known_hosts`
- Rewrote `/home/openclaw/Scripts/vault-sync.sh`:
  - `set -euo pipefail` for strict error handling
  - `git stash push --include-untracked` before `git pull origin main`
  - `git stash pop` after pull (warns but continues if merge conflict on pop)
  - Commit/push any new local changes after pull
- Cleared stale `/tmp/vault-sync.log` (was full of "Host key verification failed" entries)
- End-to-end verified: script runs as openclaw, exit 0, repo clean, up to date with `origin/main`

**Manus MCP:**
- User configured manually; waiting for Relay (Every bot) to confirm connection update

### What Needs Human Review

- `vault-sync.sh` stash behavior: if pop fails (merge conflict), stash remains and script logs warning. Monitor first few cron runs.
- Manus MCP confirmation from Relay

### Deferred Topics

- Aurora model checkup (verify kimi-k2.5 primary on Netcup)
- Clean `02-converted/` dead weight (26 dirs, ~30MB)
- Genspark MCP setup

### What to Do Next

1. **Aurora model checkup** — verify still on `moonshotai/kimi-k2.5` primary on Netcup
2. **Clean `02-converted/`** — 26 dirs of dead staging data, originals already in `03-done/`
3. **Genspark MCP setup** -- AI Browser > wrench icon > Add New MCP Server, paste endpoint URL
4. **Manus MCP status** -- check Relay bot update when available

---

## 2026-04-24 -- watch.sh Fixed, Vault Synced, Pipeline Verified

### What Was Accomplished

**Fixed `watch.sh` "Operation not permitted" error:**
- Root cause: macOS TCC blocks script execution inside iCloud path (`~/Library/Mobile Documents/iCloud~md~obsidian/...`)
- Solution: copied `watch.sh` + `ingest.py` to `~/Scripts/` (non-iCloud path)
- Updated LaunchAgent plist (`com.giladnass.ai-memory-watcher`) to point at new local path
- Reloaded agent (PID 50187)
- Truncated 796KB error log
- End-to-end verified: dropped test HTML into `01-source/` -> watcher fired -> converted to MD in `02-converted/` -> original moved to `03-done/`
- Zero errors since reload

**Vault sync committed and pushed:**
- Committed 2026-04-24 session content: `MEMORY.md`, `handoff.md`, `log.md`, `tool-configs.md`
- Pushed to `origin/main`
- Netcup pulled cleanly, basic-memory reindexed: 87 entities embedded, 0 errors
- Note: "branch gap" was already merged (main was ahead of dev branch); this was uncommitted session work on main

### What Needs Human Review

- `~/Scripts/` now contains copies of `watch.sh` and `ingest.py` -- if you edit the vault versions, remember to sync back, or update the LaunchAgent to point at vault path once iCloud TCC is resolved
- Manus and Genspark MCP still unconfigured
- Netcup cron still uses simple `git pull` (not stash+pull hardened)

### Deferred Topics

- Netcup cron hardening
- Clean `02-converted/` dead weight (26 dirs, ~30MB)
- Mac git push hook for instant sync

### What to Do Next

1. **Manus MCP** -- Settings > Integrations > Custom MCP, paste endpoint URL
2. **Genspark MCP** -- AI Browser > wrench icon > Add New MCP Server, paste endpoint URL
3. **Aurora model verification** -- check if still on kimi-k2.5 primary on Netcup
4. **Netcup cron hardening** -- replace `git pull` with stash+pull

---

## 2026-04-24 -- Perplexity MCP Connected, EPUB Processing Confirmed Done

### What Was Accomplished

**Perplexity connected to basic-memory MCP:**
- Installed `mcp-remote` globally on Mac (`npm i -g mcp-remote`)
- Configured Perplexity Desktop app: Settings > Connectors > Advanced, using `mcp-remote` as stdio bridge
- Connection works but Perplexity can't auto-discover the project -- needs `project: "ai-memory"` passed explicitly in queries
- Updated `Memory/tool-configs.md`: Perplexity status changed from "Ready to configure" to "Connected"

**EPUB processing status verified:**
- `02-converted/` still has 26 directories (not auto-cleaned) but all content already processed into Sources/ and Wiki/
- `03-done/` has the moved originals -- pipeline completed correctly
- Crossed off handoff list: "Run process.py on EPUBs in 02-converted/"

**Vault sync confirmed up to date** (main branch, all prior dev work merged)

### What Needs Human Review

1. Perplexity MCP requires explicit `project: "ai-memory"` in queries -- may need a way to make this default
2. `02-converted/` is dead weight (26 dirs, ~30MB) -- safe to clean out?
3. Manus and Genspark still unconfigured (streamable HTTP direct, trivial setup)

### What to Do Next

1. **Manus MCP** -- Settings > Integrations > Custom MCP, paste endpoint URL
2. **Genspark MCP** -- AI Browser > wrench icon > Add New MCP Server, paste endpoint URL
3. **Aurora model verification** -- check if still on kimi-k2.5 primary on Netcup
4. **Netcup cron hardening** -- replace `git pull` with stash+pull
5. **Mac git push hook** -- instant vault sync on file save
6. **Clean `02-converted/`** -- if confirmed no longer needed

---

## 2026-04-23 -- MCP Connections Research, Aurora Diagnosis, Vault Sync Fix

### What Was Accomplished

**Aurora MCP diagnosis (KI-006):**
- OpenClaw `bundle-mcp` cannot connect to basic-memory -- both HTTP direct and stdio/mcp-remote fail
- HTTP: returns 404 (OpenClaw tries SSE handshake, basic-memory uses streamable-http)
- stdio/mcp-remote: "Connection closed" error
- Workaround established: Aurora uses `mcporter call basic-memory.<tool>` skill
- AGENTS.md on Netcup updated with explicit mcporter instructions and priority rules

**Aurora search fix (ADHD books):**
- Root cause: Netcup vault was 43 commits behind main (5-min cron failing silently due to local uncommitted changes)
- Also: basic-memory index stale after large pull
- Fix: `git stash && git pull origin main` + `basic-memory reindex --project AI-Memory`

**Gemini CLI connected to vault:**
- Configured `~/.gemini/settings.json` with basic-memory MCP endpoint via `httpUrl` (streamable-http)
- Gemini CLI now has native read/write to knowledge base
- Gemini Web has no MCP client -- CLI is the correct bridge (same model, native MCP)

**Shared memory pool research (Perplexity/Manus/Genspark/ChatGPT):**
- Perplexity: Pro plan supports custom MCP. Desktop > Settings > Connectors > Advanced. Remote servers need `mcp-remote` bridge (stdio transport)
- Manus: All plans support streamable HTTP direct. Settings > Integrations > Custom MCP
- Genspark: All plans support streamable HTTP direct. AI Browser > wrench icon > Add New MCP Server
- ChatGPT: Plus/Pro gets read-only MCP. Business/Enterprise gets full read+write. Settings > Apps > Developer Mode
- NotebookLM: No MCP client. `notebooklm-mcp` bridge from Claude Code is one-way only

**Vault housekeeping:**
- `.smart-env/` added to `.gitignore` (Smart Connections plugin cache)
- 4 commits pushed to origin/main (book batch sources + wiki stubs)
- `Memory/tool-configs.md` fully updated with all MCP connection statuses
- All dev branch changes merged to main via Mac terminal

### What Needs Human Review

1. Perplexity/Manus/Genspark MCP setup requires manual UI configuration in each tool's settings
2. ChatGPT MCP limited to read-only on Plus/Pro plan -- decide if that's worth connecting
3. Aurora may still be running on minimax-m2.5 instead of kimi-k2.5 primary -- verify on Netcup

### Deferred Topics

1. Netcup cron hardening -- replace simple `git pull` with stash+pull to prevent silent failures
2. process.py --move-done cleanup for `02-converted/` after processing
3. Visual element preservation strategy (charts/images lost in conversion)
4. Review UX -- custom interface with status buttons
5. Git push hook on Mac for instant sync to Netcup

### What to Do Next

1. Run `process.py` on EPUBs in `02-converted/` (set `OLLAMA_API_KEY` first)
2. Configure Perplexity/Manus/Genspark MCP connections (manual UI setup)
3. Verify Aurora is running on kimi-k2.5 primary model
4. Harden Netcup cron pull script
5. Consider ChatGPT MCP connection (read-only on Plus/Pro)

---

## 2026-04-22 -- Phase 5: Pipeline Hardened, LaunchAgent Live

### What Was Accomplished

**Vault validation (lint.py):**
- Created `Scripts/lint.py` -- checks D-003 frontmatter, controlled vocab, dates, naming, broken wikilinks, orphan pages, stale timestamps, em-dashes
- Fixed 20 frontmatter errors: missing `tags` and `created` across all 000-Meta/ and Memory/ files
- Fixed `Sources/wiki-session-knowledge-ingestion-pipeline.md`: corrected type to `source`, added all D-003 required source fields
- Updated `index.md`: added 14 orphan wiki pages from PDF batch (ADHD, research, tools), updated scripts table
- Result: 0 errors, 16 warnings (em-dashes in immutable sources, 4 broken links to planned-but-never-created pages)

**File lifecycle finalized:**
- Added `--move-done DIR` to `ingest.py`: source files move to `03-done/` after successful conversion
- Updated `watch.sh`: passes `--move-done ~/AI-Ingestion/03-done` by default, added `DONE_DIR` variable
- Staging structure: `01-source/` (inbox) -> `02-converted/` (intermediate) -> `03-done/` (archived originals)

**LaunchAgent:**
- Vault path confirmed: `/Users/giladnass/Library/Mobile Documents/iCloud~md~obsidian/Documents/AI-Memory/`
- LaunchAgent `com.giladnass.ai-memory-watcher` created and confirmed running (PID 44692)
- Fixed iCloud executable bit stripping: `chmod +x Scripts/watch.sh` required after iCloud sync
- Existing EPUBs processed manually via ingest.py --move-done

**Clarifications documented:**
- `status: draft` is informational only -- draft pages are immediately searchable in Obsidian and via basic-memory MCP
- `02-converted/` files are intermediate staging, not what Obsidian shows for review (wiki draft pages are)
- Review flow: open `Wiki/` draft page in Obsidian, change status to `active` if valid

### Deferred Topics (to discuss in future sessions)

1. Converted-file lifecycle: some MD files in `02-converted/` need save/delete decision flow (transcripts, reports)
2. Visual element preservation: charts/images lost during conversion; need strategy + storage approach
3. Review UX: custom interface with status buttons, pipeline display; Amber app noted; Obsidian plugin as alternative
4. UX dashboard: button-based pipeline management
5. process.py `--move-done`: cleanup for `02-converted/` after processing

### What to Do Next

1. Run process.py on EPUBs in `02-converted/` -- set `OLLAMA_API_KEY`, then: `python3 ".../Scripts/process.py" --source-type epub`
2. Shared memory check -- verify basic-memory MCP sync across Claude, Aurora, Gemini
3. Aurora memory enrichment -- ask Aurora to do deeper vault read

---

## 2026-04-21 -- Phases 3-5 Complete, Pipeline Operational

### What Was Accomplished
- Wrote process.py with three-step LLM pipeline: triage (tags, routing, title), summarization (summary, findings, questions), cross-referencing against existing wiki pages
- Integrated LiteLLM for flexible model/provider configuration at runtime
- Fixed Qwen3 reasoning model bug where thinking tokens consumed max_tokens, resolved by stripping think blocks and setting max_tokens=2048
- Successfully processed batch of 13 PDFs overnight
- Wrote session_end.py for automated session logging and MEMORY updates
- Wrote linkding_export.py for bookmark ingestion from linkding API
- Added Mac M4 48GB as primary inference machine with Ollama Cloud integration
- Switched to qwen3.5:cloud (triage) and glm-5:cloud (summarization) to avoid Mac overheating issues
- Processing time improved from 11 min locally to 2.5 min via Ollama Cloud

### What to Do Next
- Phase 6: Configure OpenClaw with basic-memory MCP endpoint for Aurora vault writes via Telegram
- Test llama3.2:latest as OpenClaw primary model to resolve KI-001/KI-004
- Set up automated LINT validation for vault files
- Run full linkding bookmark batch through linkding_export.py pipeline
- Install and test faster-whisper on Netcup for transcription

### What to Read First Next Session
Per CLAUDE.md session start protocol:
1. `000-Meta/MEMORY.md`
2. `000-Meta/index.md`
3. `000-Meta/handoff.md`
4. `Working-Context/knowledge-base-build-plan.md`

---

## 2026-04-21 -- Phases 3-5 Complete, Ollama Cloud

### What Was Accomplished

**Phase 3 (LLM Processing Layer):**
- Wrote `Scripts/process.py` with three-step pipeline: triage (tags, routing, title), summarization (summary, findings, questions), cross-referencing against existing wiki pages
- Refactored to use LiteLLM so model and provider are runtime flags
- Fixed Qwen3 reasoning model bug where thinking tokens consumed max_tokens and returned empty output
- 13 PDF batch processed successfully overnight

**Phase 4 (Session Automation):**
- Wrote `Scripts/session_end.py` to accept free-form notes and structure into handoff + log + MEMORY update, then commit and push

**Phase 5 (Linkding Integration):**
- Wrote `Scripts/linkding_export.py` to fetch bookmarks from linkding API, download Singlefile HTML, convert via pandoc, drop into 02-converted for process.py

**Infrastructure Evolution:**
- Mac M4 48GB added as primary inference machine
- Switched to Ollama Cloud (qwen3.5:cloud for triage, glm-5:cloud for summarization) to avoid Mac overheating
- Processing time improved: 2.5 min/doc vs 11 min locally
- Netcup role narrowed to transcription only

### What to Do Next

**Phase 6 (OpenClaw Integration):**
1. Configure OpenClaw with basic-memory MCP endpoint so Aurora can write to vault from Telegram
2. Test `llama3.2:latest` as OpenClaw primary model to resolve KI-001/KI-004 (Gemini fallback issue)

**LINT Automation:**
- Set up automated linting/validation for vault files

**Linkding Batch:**
- Run full bookmark export and processing through the pipeline

**Transcription on Netcup:**
- Install and test faster-whisper for audio/video transcription

### What to Read First Next Session
Per CLAUDE.md session start protocol:
1. `000-Meta/MEMORY.md`
2. `000-Meta/index.md`
3. `000-Meta/handoff.md`
4. `Working-Context/knowledge-base-build-plan.md`

---

## 2026-04-22 -- Phase 4 Complete: Full Pipeline Operational + Aurora MCP Connected

### What Was Accomplished

**Aurora improvements:**
- BOOTSTRAP.md deleted -- re-introduction sequence no longer runs on every new session
- SOUL.md updated: outcome-only responses, no step-by-step narration
- `compaction.reserveTokensFloor` set to 20000 -- prevents context overflow resets
- basic-memory MCP connected via `mcp-remote` stdio bridge
  - Root cause: OpenClaw 2026.4.21 bug (issues #65590/#66940) -- streamable-http missing Accept header
  - Workaround: mcp-remote installed globally at `/home/openclaw/.npm-global/bin/mcp-remote`
  - Fix pending: PR #66966 (not yet released)
- Aurora rebuilt her workspace MEMORY.md from vault content via basic-memory tools

**Pipeline completed:**
- ingest.py ran on Mac -- files already converted from prior session, 0 new errors
- faster-whisper confirmed deployed and tested on Netcup
- linkding full export completed

**Infrastructure:**
- SSH key auth fixed on Mac -- `netcup_key` added to macOS keychain, `UseKeychain yes` in config

### What to Do Next

1. Start `watch.sh` on Mac for ongoing automation
2. Run `Scripts/process.py` on converted linkding output to ingest into vault
3. Update `Memory/tool-configs.md` -- model chain changed, Groq removed
4. Update `000-Meta/known-issues.md` -- mark KI-001/KI-004 resolved, add OpenClaw MCP bug

---

## 2026-04-22 -- Aurora on Discord + KI-001/KI-004 Resolved

### What Was Accomplished

**Obsidian/Mac fixes:**
- `.claude/` added to `.gitignore` -- resolved obsidian-git submodule error on every auto-commit
- Git binary path confirmed in Obsidian git plugin settings (resolves "git does not exist" on Mac)

**Aurora -- Discord migration:**
- Aurora added to Discord; `channels.discord.allowFrom` set to Gilad's user ID (string array format)
- `dmPolicy: pairing` set for Discord DMs
- `groupPolicy: allowlist` set -- resolves CRITICAL security warning (any guild could trigger)
- Bot renamed to "Aurora" in Discord Developer Portal; re-invite required after rename
- Brain files confirmed global -- same workspace (SOUL.md, USER.md, etc.) shared across Telegram and Discord
- USER.md updated: correct Hebrew spelling `גילעד`, bilingual response rules (no language mixing)

**KI-001/KI-004 fixed:**
- Root cause confirmed: OpenClaw 16k minimum context floor excluded all local models under 14B
- `llama3.2-32k` custom Ollama model created (32k ctx via Modelfile) -- still too small for agentic tasks
- Fix: switched primary model to `moonshotai/kimi-k2.5` via OpenRouter (200k ctx)
- Fallback chain: Kimi K2.5 > `ollama/minimax-m2.5:cloud` > `openrouter/google/gemini-2.0-flash-001`
- All 3 active sessions confirmed on Kimi K2.5; dreaming sessions on Gemini (expected)
- Ollama Cloud login verified on Netcup (user: giladn, Pro subscription)

### State of Aurora

Stable and operational. Both Discord and Telegram channels active. Primary model working. Sessions were reset during model transition -- workspace MEMORY.md sparse (one entry), will rebuild through conversation.

### What to Do Next

1. Connect Aurora to basic-memory MCP endpoint (lets Aurora write to this vault from any channel)
2. Run 13-PDF batch on Mac: `pip install pymupdf4llm && python3 Scripts/ingest.py`
3. Install faster-whisper on Netcup
4. Run full linkding export (no `--limit`)

---

## 2026-04-20 -- Phases 0 and 1 Complete

### What Was Accomplished

Both Phase 0 (Foundation) and Phase 1 (MCP Access Layer + Infrastructure Documentation) are complete.

**Phase 0 (earlier this session):**
- Schema locked (8 decisions)
- All templates populated
- 4 wiki pages from prior source doc
- Build plan written

**Phase 1 (this continuation):**
- Memory/profile.md and Memory/tool-configs.md populated
- Wiki pages created for OpenClaw/Aurora and Netcup server
- Known issues documented (KI-001 through KI-004)
- D-006 (MCP data contract) finalized: Active
- CLAUDE.md updated with no-em-dash rule

### State of the Vault

The vault is now a functional knowledge base. Schema is locked, infrastructure is documented, known issues are tracked, and the MCP access layer is verified. 6 wiki pages, 1 source, 1 working context document, all meta files populated.

### Security Action Required

Check whether `giladnass/Repo1` is a public or private GitHub repository. `Memory/tool-configs.md` contains a note about the basic-memory MCP endpoint URL containing an auth token. If the repo is public, that token should not be committed -- move it to a private file or environment variable.

### Phase 2 Progress

Conversion scripts written. Marker suspended (KI-005). pymupdf4llm adopted (D-009).

**Scripts ready to run on Mac:**
- `Scripts/ingest.py` -- PDF + doc converter
- `Scripts/watch.sh` -- fswatch watcher

### What to Do Next

**On Mac (immediate):**
```bash
pip install pymupdf4llm
python3 Scripts/ingest.py           # processes 13 PDFs in ~/AI-Ingestion/01-source/
python3 Scripts/ingest.py --file somefile.docx  # test pandoc path

brew install fswatch
./Scripts/watch.sh                  # start ongoing watch folder
```

**On Netcup:**
```bash
pip install faster-whisper
```
Test on a short audio file, then queue the audio/video batch overnight.

**OpenClaw (optional but high-value):**
- Configure basic-memory MCP endpoint in OpenClaw so Aurora can write to this vault from Telegram
- Try `llama3.2:latest` as OpenClaw primary model (resolves KI-001/KI-004)

### What to Read First Next Session

Per CLAUDE.md session start protocol:
1. `000-Meta/MEMORY.md`
2. `000-Meta/index.md`
3. This handoff file
4. `Working-Context/knowledge-base-build-plan.md`
