---
title: known-issues
type: note
permalink: ai-memory/000-meta/known-issues
---

# Known Unresolved Issues

Documented constraints, not assigned tasks. Treat as context for design decisions. Do not attempt to fix without understanding root cause and confirming with Gilad.

---

## KI-001 -- Gemini Fallback Bug (OpenClaw)

**Status:** Active, unresolved
**System:** OpenClaw / Aurora

**Symptom:** All Aurora sessions fall back to Gemini (`openrouter/google/gemini-2.0-flash-001`) despite `ollama/qwen2.5:1.5b` configured as primary.

**Root cause:** See KI-004. OpenClaw enforces a 16k minimum context. `qwen2.5:1.5b` is configured at ctx 2048. When OpenClaw evaluates the model, it sees the 2048 context as below the 16k minimum and silently falls back. The brain file size (suspected to push into context limits) is a contributing factor, not the root cause.

**Next diagnostic step:** `wc -w /home/openclaw/.openclaw/agents/main/agent/*.md` -- confirm brain file word count, but note this is secondary to KI-004.

**Related:** KI-004, [[Wiki/openclaw-aurora]]

---

## KI-002 -- Composio/Gmail MCP Integration (OpenClaw)

**Status:** Active, parked
**System:** OpenClaw / Aurora

**Symptom:** `@composio/openclaw-plugin` was installed and working at one point. OpenClaw versions 2026.4.8-4.9 do not surface MCP tools to the agent layer -- `mcporter` ignores API key headers.

**Current status:** Unresolved. Parked pending an OpenClaw update that addresses `mcporter` behavior. No workaround available without downgrading or patching OpenClaw.

**Related:** [[Wiki/openclaw-aurora]]

---

## KI-003 -- Aurora Cross-Channel Memory

**Status:** Active, unverified
**System:** OpenClaw / Aurora

**Symptom:** Unclear whether daily memory files (`memory/YYYY-MM-DD.md`) in the Obsidian Codex vault are being actively written and read by Aurora across sessions.

**Next diagnostic step:**
1. Check `/home/openclaw/obsidian/codex-vault/memory/` for recent files
2. Verify `AGENTS.md` contains explicit instructions for memory read/write behavior
3. Send Aurora a test message and check if memory file is created/updated

**Related:** [[Wiki/openclaw-aurora]]

---

## KI-004 -- OpenClaw 16k Minimum Context vs. qwen2.5:1.5b Optimal Context

**Status:** Active, architectural tension
**System:** OpenClaw / Ollama

**Symptom:** OpenClaw silently falls back to the next model in the chain if the primary model's context is configured below 16k tokens. `qwen2.5:1.5b` needs ctx 2048 to stay performant. These requirements are incompatible.

**Root cause:** OpenClaw's 16k minimum context enforcement is a hardcoded constraint. It cannot be disabled via config. `qwen2.5:1.5b` at ctx 16384 would consume its entire context window before producing output, causing degraded or empty responses.

**Impact:** This is the root driver of KI-001. The fallback to Gemini is not a bug in the model selection config -- it is the expected behavior given the constraint.

**Resolution options:**
1. Replace primary model with one that performs well at 16k context (`llama3.2:latest` is already installed and may be viable)
2. Wait for OpenClaw to expose a configurable minimum context setting
3. Accept Gemini as de facto primary and reconfigure the chain intentionally

**Related:** KI-001, [[Wiki/openclaw-aurora]], [[Wiki/netcup-server]]
