---
title: roadmap-openclaw-discord-migration
type: note
permalink: ai-memory/working-context/roadmap-openclaw-discord-migration
tags:
- roadmap
- openclaw
- discord
- aurora
- multi-agent
---

# Roadmap: OpenClaw — Discord Migration & Multi-Agent Architecture

## The Vision
Move primary OpenClaw interaction from Telegram to Discord, while:
- Preserving Aurora's personality and soul from Telegram
- Using Discord's server/channel structure as the foundation for multiple specialized agents
- Each agent focuses on a different life domain

## Why Discord over Telegram
- Channels map naturally to life domains (one channel per agent/topic)
- Better threading for complex conversations
- Richer bot ecosystem and permissions model
- Easier to have multiple agents coexist without confusion
- Better for long-form context and file sharing

## Multi-Agent Architecture (to design)
Each agent = a Discord channel + a specialized persona + a focused skill set.

Possible domains (to be decided with Gilad):
- Personal assistant / daily life (Aurora — the existing soul, migrated)
- Work / career / professional projects
- Health & wellness
- Knowledge & learning (connected to the shared memory system)
- Finance
- Creative projects

## Aurora Migration Requirements
- Preserve Aurora's voice, personality, and behavioral patterns from Telegram
- Export/document Aurora's SOUL.md and USER.md before migration
- Ensure continuity of memory — Aurora should "remember" who Gilad is
- Test Aurora in Discord before decommissioning Telegram instance

## Open Questions
- Which life domains should have dedicated agents?
- Should agents share memory (same basic-memory project) or have isolated memory?
- How do agents hand off to each other when a topic crosses domains?
- Should there be a "coordinator" agent that routes to specialized ones?

## Dependencies
- OpenClaw Discord extension (already exists: /home/openclaw/.npm-global/lib/node_modules/openclaw/dist/extensions/discord/)
- OpenClaw basic-memory integration (must be fixed first)
- Aurora's Telegram soul/config documented and exported

## Status
Not started. Depends on OpenClaw basic-memory fix being completed first.
