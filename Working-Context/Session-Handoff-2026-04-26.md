---
title: Session Handoff — GOG Deployment & Aurora Fixes
date: 2026-04-26
session_id: claude-code-2026-04-26
type: session-handoff
status: in-progress
---

# Session Handoff: GOG Deployment & Aurora Model Issues

## What Was Done

### GOG (gogcli) Deployed Successfully
- **Decision:** Replaced Composio with GOG CLI (not MCP) to minimize token overhead in Aurora's constrained context.
- **Binary installed** on Netcup at `/home/openclaw/.local/bin/gog`, symlinked to `/usr/local/bin/gog` for PATH visibility.
- **OAuth configured** for `gilad.nass@gmail.com` via `--manual` flow. Google Cloud Console project: `rugged-alcove-494513-t0`.
- **Services active:** Gmail, Calendar, Contacts, Drive, Sheets, Docs, Tasks, Chat, Classroom, Forms, AdWords, Apps Script.
- **Skill installed** in OpenClaw workspace: `gog@1.0.0` at `~/.openclaw/workspace/skills/gog`.
- **AGENTS.md updated** with explicit GOG command templates and CRITICAL instruction: "Do NOT use himalaya. Only use gog via exec."

### Conflicting Skills Removed
- Removed unconfigured `gmail` and `himalaya` workspace skills from `~/.openclaw/workspace/skills/`.
- Disabled `himalaya` skill in OpenClaw config via `skills.entries.himalaya.enabled = false`.

## Verified Working
- `gog gmail search "newer_than:4h" --max 5 --json` returns email threads.
- `gog calendar events primary --today --json` returns calendar events.
- Aurora (via dashboard) successfully listed last 5 emails using GOG.

## Active Problems Found (Not Fixed)

### 1. Primary Model Broken
- `moonshotai/kimi-k2.5` fails with **"Unknown model"** on every request.
- Aurora falls back to `groq/llama-3.1-8b-instant`, then to `openrouter/google/gemini-2.5-flash-lite`.

### 2. Groq Rate Limit Hit
- TPM limit: 6,000. Request size: 48,395 tokens.
- Error: `413 Request too large for model llama-3.1-8b-instant`.
- Groq is unusable for any request with full brain files loaded.

### 3. Context Bloat (Root Cause)
- Brain files total **35K–48K tokens** per request.
- **MEMORY.md** is massive (~2,000+ words) with full system status, Discord roadmap, MCP URLs, pipeline details.
- **AGENTS.md** also grew with GOG section.
- Per OpenClaw rules, brain files must stay under ~1,500 words total or context budget overflows.
- This is causing timeouts, fallback loops, and model switching.

## What Needs to Happen Next

### Immediate (before next Aurora session)
1. **Trim brain files** — Move verbose system-status content out of MEMORY.md into vault pages. Keep only concise personal context in brain files.
2. **Fix primary model** — Replace `moonshotai/kimi-k2.5` with a working model (e.g., `openrouter/google/gemini-2.5-flash-lite` or another verified OpenRouter model).
3. **Consider removing Groq fallback** — With 6K TPM limit, `llama-3.1-8b-instant` cannot handle full brain files. Either trim context or remove from fallback chain.

### File Changes on Netcup (not in git)
- `~/.openclaw/workspace/AGENTS.md` — modified (GOG section added)
- `~/.openclaw/openclaw.json` — modified (`skills.entries.himalaya.enabled = false`)
- `~/.openclaw/workspace/skills/gog/` — created
- `~/.openclaw/workspace/skills/gmail/` — deleted
- `~/.openclaw/workspace/skills/himalaya/` — deleted (workspace copy; bundled remains)
- `/usr/local/bin/gog` — symlink created
- `~/.local/bin/gog` — binary installed
- `~/.config/gogcli/` — auth tokens stored

## Decision Log
- **CLI > MCP for Google apps:** Chose `gogcli` over MCP servers because MCP system prompt overhead is unacceptable for Aurora's ~2K token budget.
- **No device flow:** Google's OAuth device flow does not support Gmail/Calendar scopes. Manual `--auth` with browser redirect is the only viable path for personal Gmail on headless server.
- **Symlink over PATH edit:** `/usr/local/bin/gog` symlink ensures OpenClaw process finds binary without modifying systemd service env.
