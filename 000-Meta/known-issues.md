---
title: known-issues
type: note
tags: [meta, known-issues, openclaw, aurora]
created: 2026-04-20
permalink: ai-memory/000-meta/known-issues
---

# Known Unresolved Issues

Documented constraints, not assigned tasks. Treat as context for design decisions. Do not attempt to fix without understanding root cause and confirming with Gilad.

---

## KI-001 -- Gemini Fallback Bug (OpenClaw)

**Status:** Resolved (2026-04-22)
**System:** OpenClaw / Aurora

**Symptom:** All Aurora sessions fell back to Gemini despite a local model configured as primary.

**Root cause:** OpenClaw enforces a 16k minimum context floor. All tested local models were below this threshold. See KI-004.

**Resolution:** Switched primary model to `moonshotai/kimi-k2.5` via OpenRouter (200k ctx). All sessions now run on the primary model. Local models retained in Ollama but not used as primary.

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

## KI-005 -- Marker PDF Converter: Apple Silicon MPS Bug

**Status:** Resolved by switching to pymupdf4llm (see D-009)
**System:** Mac (M4) / Marker / surya

**Symptom:** Marker crashed on PDFs during batch conversion with:
```
torch.AcceleratorError: index 8192 is out of bounds: 2, range 0 to 4560
```
Specifically in `surya/common/surya/encoder/__init__.py`, `unpack_qkv_with_mask`.
The CPU fallback (`--disable_multiprocessing`) was attempted but was too slow to be practical (~107s/PDF on GPU; CPU-only would be 5-10x slower for complex PDFs).

**Root cause:** Bug in the surya library's MPS (Metal Performance Shaders) backend for Apple Silicon. Triggered by PDFs that generate sequences exceeding an internal max length. Not a Marker configuration issue -- a surya dependency bug.

**Resolution:** Switched primary PDF converter to pymupdf4llm (Decision D-009). Marker remains installed for potential future use once surya fixes the MPS bug, or pending docling evaluation.

**Related:** D-009, [[Wiki/format-conversion-tools]]

---

## KI-004 -- OpenClaw 16k Minimum Context Floor

**Status:** Resolved (2026-04-22)
**System:** OpenClaw / Ollama

**Symptom:** OpenClaw silently falls back when the primary model's context is below 16k tokens.

**Root cause:** Hardcoded 16k minimum context floor in OpenClaw. Cannot be disabled via config.

**Resolution:** Switched to `moonshotai/kimi-k2.5` (200k ctx) as primary. The 16k floor is no longer a constraint. Local models under 14B remain unsuitable as primary for agentic tasks regardless of this fix.

**Related:** KI-001, [[Wiki/openclaw-aurora]]

---

## KI-006 -- OpenClaw MCP Streamable-HTTP Missing Accept Header

**Status:** Active, workaround in place
**System:** OpenClaw 2026.4.21 / bundle-mcp

**Symptom:** MCP servers using streamable-http transport fail to connect. With `"type":"http"` the client uses SSE and gets 400/401. With `"type":"streamable-http"` or `"transport":"streamable-http"` the server is silently skipped.

**Root cause:** OpenClaw bug -- streamable-http connections do not send the required `Accept: application/json, text/event-stream` header. MCP spec-compliant servers reject the request. Tracked in OpenClaw issues #65590 and #66940. Fix in PR #66966 (open, not yet released as of 2026.4.21).

**Workaround:** Use `mcp-remote` as a stdio bridge:
```json
{"command":"/home/openclaw/.npm-global/bin/mcp-remote","args":["<server-url>"]}
```
`mcp-remote` installed globally at `/home/openclaw/.npm-global/bin/mcp-remote`. Currently in use for basic-memory MCP connection.

**Related:** [[Wiki/openclaw-aurora]]
