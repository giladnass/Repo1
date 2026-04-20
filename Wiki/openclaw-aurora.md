---
title: "OpenClaw / Aurora"
type: wiki
tags: [openclaw, aurora, netcup, agent, infrastructure]
created: 2026-04-20
updated: 2026-04-20
sources: []
status: active
confidence: high
---

## Summary

OpenClaw is a TypeScript-based AI agent gateway running as a systemd user service on the Netcup server. Aurora is the AI persona deployed through it -- accessible via Telegram, Discord, and an OpenClaw web dashboard, with a unified personality across all channels.

## Architecture

| Component | Detail |
|---|---|
| Binary | `/home/openclaw/.npm-global/bin/openclaw` |
| User | `openclaw` (dedicated systemd user) |
| Config | `openclaw config set` -- never edit `openclaw.json` directly |
| Brain files | `~/.openclaw/workspace/SOUL.md`, `IDENTITY.md`, `AGENTS.md` |

Brain files load across all channels, giving Aurora a unified identity.

## Aurora Access Points

| Channel | Detail |
|---|---|
| Telegram | `@gnass_claw_bot`, locked to Gilad's numeric Telegram ID |
| Discord | Connected |
| Web dashboard | OpenClaw web UI |

## Model Configuration

`models.mode=replace` (auto-discovery disabled to prevent unexpected model changes)

| Priority | Model | Context | Max Tokens |
|---|---|---|---|
| Primary | `ollama/qwen2.5:1.5b` | 2048 | 512 |
| Fallback 1 | `groq/llama-3.1-8b-instant` | -- | -- |
| Fallback 2 | `openrouter/google/gemini-2.0-flash-001` | -- | -- |

## Vault Relationship

OpenClaw uses the **Obsidian Codex vault** -- a separate vault from AI-Memory. The Codex vault syncs from Google Drive to `/home/openclaw/obsidian/codex-vault` on the Netcup server via rclone (hourly cron).

AI-Memory (this vault, `giladnass/Repo1`) is accessed differently -- via iCloud sync on Mac and via the basic-memory MCP endpoint. OpenClaw could be configured to query/write AI-Memory via the MCP endpoint, but this is not yet implemented.

## Strategic Opportunity

Aurora + basic-memory MCP = a potential always-on ingestion agent. If configured, Aurora could:
- Accept content via Telegram/Discord ("ingest this link/file")
- Process it through the ingestion pipeline
- Write the result directly to this vault via basic-memory MCP

This would close the automation gap for casual/mobile ingestion without requiring manual Claude Code sessions. Not yet implemented -- requires OpenClaw to be configured with the basic-memory MCP endpoint.

## Known Issues

See [[000-Meta/known-issues]] for full details:
- **KI-001:** All sessions fall back to Gemini (root cause: KI-004)
- **KI-002:** Composio/Gmail MCP tools not surfacing to agent (versions 2026.4.8-4.9)
- **KI-003:** Cross-channel memory (daily memory files) unverified
- **KI-004:** OpenClaw 16k minimum context enforcement conflicts with `qwen2.5:1.5b` optimal context of 2048 -- this is the root driver of KI-001

## Related
- [[Wiki/netcup-server]]
- [[Memory/tool-configs]]
- [[000-Meta/known-issues]]
