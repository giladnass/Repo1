---
title: OpenClaw Cost Bleed Fix — 2026-04-24
type: report
permalink: ai-memory/working-context/open-claw-cost-bleed-fix-2026-04-24
tags:
- openclaw
- aurora
- cost-fix
- netcup
- infrastructure
---

## Session: OpenClaw Cost Bleed Fix

**Date:** 2026-04-24
**System:** Netcup root server (Ubuntu 24.04) — OpenClaw / Aurora
**Scope:** Emergency cost-reduction surgery on OpenClaw config after budget alarm

---

### Issues Found

| # | Problem | Severity |
|---|---|---|
| 1 | `moonshotai/kimi-k2.5-0127` set as primary model — $0.012/heartbeat, ~$17.66/month from heartbeat alone | Critical |
| 2 | Heartbeat every 30 min, never clears session history, prompts grow to 49k+ tokens | High |
| 3 | Brain files (AGENTS.md + SOUL.md + IDENTITY.md) = 1,859 words — local model `qwen2.5:1.5b` context 2048, so OpenClaw fell through to OpenRouter on every call | High |
| 4 | OpenRouter BYOK for Gemini not routing correctly (`byok_usage_inference = 0`) | Medium |

---

### Fixes Applied

**1. Removed kimi K2.5 from all config**
- `agents.defaults.model.primary` changed from `openrouter/moonshotai/kimi-k2.5` → `ollama/qwen2.5:1.5b`
- Verified `grep -i kimi /home/openclaw/.openclaw/openclaw.json` returns `EXIT:1`

**2. Rebuilt fallback chain**
- Primary: `ollama/qwen2.5:1.5b`
- Fallback 1: `groq/llama-3.1-8b-instant`
- Fallback 2: `openrouter/google/gemini-2.5-flash-lite`
- `models.mode=replace` (auto-discovery disabled)

**3. Trimmed brain files**
- AGENTS.md: 1,478 → 261 words
- SOUL.md: 298 words (unchanged)
- IDENTITY.md: 83 words (unchanged)
- Total: 1,859 → 642 words (well under 900 target)
- Content preserved: all behavioral rules, mcporter instructions, red lines, session management
- Content cut: verbose heartbeat guide (already in HEARTBEAT.md), redundant group-chat examples, emoji reaction over-explanation

**4. Cleared bloated session history**
- `sessions.json` nuked to `{}`
- Old sessions had accumulated 49k+ token history per session

**5. Updated OpenRouter model to match BYOK config**
- OpenRouter BYOK configured in dashboard for Google AI Studio / `gemini-2.5-flash-lite`
- OpenClaw model slug updated from `google/gemini-2.0-flash-001` → `google/gemini-2.5-flash-lite`

**6. Restarted gateway and verified**
- Gateway running active
- Test call: `fallbackUsed: false`, `runner: embedded` — local model handled it

---

### Still Need Fixing
### Status Updates — 2026-04-24 (Evening)

| # | Item | Status |
|---|---|---|
| 1 | Heartbeat interval (60 min / 07:00-23:00) | ✅ Fixed — confirmed via Aurora on OpenClaw dashboard |
| 2 | BYOK routing for Gemini 2.5 Flash Lite | ✅ Configured in OpenRouter interface — **pending verification tomorrow** |
| 3 | Context window monitoring for qwen2.5:1.5b | ⏳ Check OpenClaw logs on Saturday |

### BYOK / Google AI Studio Notes

- OpenRouter BYOK reconfigured to use **Google AI Studio / Gemini Pro subscriber account**
- New API key created in **Google AI Studio under gilad.nass@gmail.com** (Gemini Pro subscriber account)
- Replaced previous key that was under giladn@giladn.com
- **Reminder (Friday → Saturday):** Verify that Gemini 2.5 Flash Lite is being used via BYOK, not charged by OpenRouter directly, and confirm it falls under the Google AI Studio Gemini Pro entitlement

### Remaining Checks

| # | Check | When |
|---|---|---|
| BYOK cost verification | Confirm Gemini 2.5 Flash Lite routes through Google AI Studio BYOK, no OpenRouter charges | Saturday morning (or prompt Gilad Friday evening) |
| Context window log review | Check OpenClaw logs for fallback events — is qwen2.5:1.5b staying local or still falling back? | Saturday |

### Files Modified on Netcup

- `/home/openclaw/.openclaw/openclaw.json` — model config updated
- `/home/openclaw/.openclaw/workspace/AGENTS.md` — trimmed from 1,478 to 261 words
- `/home/openclaw/.openclaw/agents/main/sessions/sessions.json` — cleared

### Verification Commands

```bash
# Verify no kimi
ssh netcup "grep -i kimi /home/openclaw/.openclaw/openclaw.json"

# Verify model chain
ssh netcup "sudo -u openclaw bash -c 'export PATH=/home/openclaw/.npm-global/bin:\$PATH && openclaw config get agents.defaults.model'"

# Verify brain file sizes
ssh netcup "sudo -u openclaw bash -c 'wc -w /home/openclaw/.openclaw/workspace/AGENTS.md /home/openclaw/.openclaw/workspace/SOUL.md /home/openclaw/.openclaw/workspace/IDENTITY.md'"

# Test local model
ssh netcup "sudo -u openclaw bash -c 'export PATH=/home/openclaw/.npm-global/bin:\$PATH && openclaw agent --agent main --message \"ping\" --json'"
```