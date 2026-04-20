---
title: "AI Memory System — Overview"
type: wiki
tags: [meta, system, ai-memory]
created: 2026-04-20
updated: 2026-04-20
sources: []
status: active
confidence: high
---

## Summary

The AI Memory System is a living, intelligent knowledge repository that captures, processes, and makes permanently queryable everything Gilad reads, watches, researches, or thinks about. It is accessible by multiple AI tools via MCP and browseable as plain Markdown in Obsidian.

## Design Goals

- **Living:** continuously ingests new content; self-updates and cross-links
- **Intelligent:** LLM-powered tagging, summarization, triage, and cross-referencing at ingest time
- **Accessible by tools:** any AI tool (Claude, Gemini, etc.) can query and write via a standard protocol
- **Accessible by human:** browseable in Obsidian, searchable from any device, readable as plain Markdown
- **Broad ingest support:** PDFs, web pages, videos, audio, DOCX, EPUB, conversations, voice notes
- **Standardized:** schema and format that works across AI tools and tech stacks
- **Efficient:** optimizes cost/speed — not every operation needs the best model
- **Extensible:** add vaults, tools, or pipelines without redesigning the core

## System Architecture

```
Raw Content (any format)
        ↓
[Conversion Layer]  marker / pandoc / faster-whisper / scraper
        ↓
Markdown  →  Sources/ (immutable)
        ↓
[LLM Processing Layer]  Claude API — tag, summarize, route, cross-reference
        ↓
Source Note (Sources/) + Wiki Page(s) (Wiki/)
        ↓
[MCP Access Layer]  all connected AI tools can read/write
        ↓
Obsidian (human)  +  Git (versioned, synced across devices)
```

## Folder Structure

| Folder | Purpose |
|---|---|
| `000-Meta/` | System files: MEMORY, index, decisions, log, handoff |
| `Memory/` | Persistent context: profile, preferences, tool configs |
| `Sources/` | Immutable raw ingested content (converted to MD) |
| `Templates/` | Frontmatter + structure templates for each note type |
| `Wiki/` | Processed, synthesized knowledge pages |
| `Working-Context/` | Active project documents (living, not archived) |

## Related Systems

- **OpenClaw/Aurora** — agentic infrastructure project. Shares infrastructure with this vault. *Not yet documented — requires input.*
- **Shared cross-tool memory pool** — accessible by multiple AI tools. *Not yet documented.*

## Build Plan

See [[Working-Context/knowledge-base-build-plan]] for the 6-phase implementation plan.

## Key Decisions

See [[000-Meta/decisions]] for the full decisions log (8 decisions as of 2026-04-20).

## Related
- [[Wiki/ingestion-pipeline]]
- [[Wiki/format-conversion-tools]]
- [[Wiki/visual-data-preservation]]
- [[Memory/tool-configs]]
