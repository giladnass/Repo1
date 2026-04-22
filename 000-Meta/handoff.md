---
title: handoff
type: note
permalink: ai-memory/000-meta/handoff
---

# Handoff Notes

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

**OpenClaw opportunity (low-effort, high-value):**
- Configure OpenClaw with the basic-memory MCP endpoint so Aurora can write to this vault
- This would close the mobile/async ingestion gap without any additional infrastructure

**OpenClaw KI-001 fix:**
- Try switching primary model to `llama3.2:latest` (already installed on Netcup, larger context window)
- This may resolve the Gemini fallback without waiting for OpenClaw to expose a configurable minimum context

### What to Read First Next Session

Per CLAUDE.md session start protocol:
1. `000-Meta/MEMORY.md`
2. `000-Meta/index.md`
3. This handoff file
4. `Working-Context/knowledge-base-build-plan.md`
