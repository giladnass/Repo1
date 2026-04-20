---
title: "Ingestion Pipeline"
type: wiki
tags: [ingestion, pipeline, automation, ai-memory]
created: 2026-04-20
updated: 2026-04-20
sources: ["[[Sources/wiki-session-knowledge-ingestion-pipeline]]"]
status: active
confidence: high
---

## Summary

The content ingestion pipeline converts raw material of any format into Markdown, then applies LLM-powered processing to produce structured source notes and wiki pages in the vault.

## Full Pipeline

```
Raw Content (PDF, DOCX, audio, video, URL, etc.)
        ↓
[Step 1: Conversion]       See [[Wiki/format-conversion-tools]]
        ↓
[Step 2: Visual Extraction] For high-value docs — charts/diagrams → MD
                            See [[Wiki/visual-data-preservation]]
        ↓
[Step 3: LLM Processing]   Tag, summarize, route, cross-reference
        ↓
[Step 4: Filing]           Source Note in Sources/  +  Wiki Page(s) in Wiki/
        ↓
[Step 5: Indexing]         Update 000-Meta/index.md + cross-link related pages
```

## What's Automatable Today

| Content Type | Automatable? | Mechanism |
|---|---|---|
| Files dropped into watched folder | ✅ | `fswatch` + conversion script |
| Google Drive new files | ✅ | Drive API + webhook |
| Audio/video batch | ✅ | Scheduled Whisper jobs on Netcup |
| Web browsing/bookmarks | ✅ | Omnivore/ArchiveBox auto-import |
| Claude Code sessions | ✅ | Filesystem access, auto-save outputs |
| Claude.ai conversations | ⚠️ Partial | No official export API |
| Manual insights/decisions | ❌ | Always needs human trigger |

## LLM Processing Step

At ingest, the LLM processing step does:
1. **Tagging** — extract topic tags from content (Haiku)
2. **Summarization** — 2–5 sentence summary (Sonnet)
3. **Routing** — decide: full ingest / summary-only / index-only (Haiku)
4. **Cross-referencing** — find related wiki pages, suggest wikilinks (Sonnet)

Use Claude API batch endpoint for non-urgent content (backlog processing). Real-time sessions use streaming.

## Routing Logic

| Signal | Route |
|---|---|
| High information density, novel content | Full ingest → Source Note + Wiki page(s) |
| Redundant with existing wiki content | Summary-only → Source Note only |
| Low value, reference material | Index-only → URL + title + tags in index MD |

## Automation Gap — Current State

The current setup (Obsidian + basic-memory + Git) is a **manually-fed filing system with good retrieval**. The automation layer does not yet exist. Building it is the goal of Phases 2–3 of the build plan.

See [[Working-Context/knowledge-base-build-plan]] for the implementation plan.

## The Claude Conversation Problem

Claude.ai has no official API for exporting conversations. Solutions:
- **Best:** Use Claude Code for knowledge-building sessions — full filesystem access, can write directly to vault
- **Workaround:** Manual export + formatting script
- **Avoid:** Browser extension capture (fragile)

## URL / Bookmark Backlog

Estimated scale: thousands of URLs.

| Stage | Tool | Purpose |
|---|---|---|
| Scrape & archive | ArchiveBox or Firecrawl API | Full page content capture |
| Auto-categorize & triage | Claude API batch | Topic, tags, ingest-worthiness, summary |
| Ingest-worthy content | Convert to MD → vault | Full ingestion |
| Index the rest | Title + summary + URL + tags in MD index | Searchable without noise |

## Related
- [[Wiki/format-conversion-tools]]
- [[Wiki/visual-data-preservation]]
- [[Wiki/ai-memory-system-overview]]
- [[Working-Context/knowledge-base-build-plan]]
