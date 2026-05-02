---
title: index
type: note
tags: [meta, index, vault-map]
created: 2026-04-20
permalink: ai-memory/000-meta/index
---

# Vault Content Map

*Last updated: 2026-04-22*

---

## Wiki Pages

### System / Infrastructure

| Page | Topic | Status | Updated |
|---|---|---|---|
| [[Wiki/ai-memory-system-overview]] | Top-level system description | active | 2026-04-20 |
| [[Wiki/ingestion-pipeline]] | Content ingestion architecture and automation | active | 2026-04-20 |
| [[Wiki/format-conversion-tools]] | Tool inventory by format type | active | 2026-04-20 |
| [[Wiki/visual-data-preservation]] | Strategy for preserving visual content | active | 2026-04-20 |
| [[Wiki/openclaw-aurora]] | OpenClaw agent gateway and Aurora persona | active | 2026-04-20 |
| [[Wiki/netcup-server]] | Netcup server infrastructure and services | active | 2026-04-20 |
| [[Wiki/obsidian-claude-integration-cheat-sheet]] | Obsidian + Claude workflow reference | draft | 2026-04-21 |

### ADHD

| Page | Topic | Status | Updated |
|---|---|---|---|
| [[Wiki/adhd-clinical-reference-guide]] | Clinical guidelines, diagnostic scales, epidemiology | draft | 2026-04-21 |
| [[Wiki/adhd-daily-life-tools-and-tips]] | Daily routine strategies, time management, productivity | draft | 2026-04-21 |
| [[Wiki/adhd-executive-function-strategies]] | Focus, organization, and executive function strategies | draft | 2026-04-21 |
| [[Wiki/adult-adhd-workbook-beyond-basics]] | Self-care and workbook-based strategies for adult ADHD | draft | 2026-04-21 |
| [[Wiki/cognitive-therapy-for-adult-adhd]] | CBT and self-regulation approaches for adult ADHD | draft | 2026-04-21 |
| [[Wiki/mini-adhd-coach-tools]] | Mini ADHD Coach: diagnosis, neurodiversity, mental health | draft | 2026-04-21 |
| [[Wiki/non-medication-adhd-treatments-for-children-and-teens]] | Non-medication treatments (clinician workbook) | draft | 2026-04-21 |
| [[Wiki/non-medication-adhd-treatments-for-children]] | Non-medication treatments for children (parent skills) | draft | 2026-04-21 |
| [[Wiki/the-ultimate-adhd-career-guide]] | Career planning and workplace adaptation for ADHD | draft | 2026-04-21 |

### Research / Other

| Page | Topic | Status | Updated |
|---|---|---|---|
| [[Wiki/integrity-and-competence-in-trust]] | Trust, integrity, and social cognition | draft | 2026-04-21 |
| [[Wiki/mental-models-physics-and-chemistry]] | Mental models from physics and chemistry | draft | 2026-04-21 |
| [[Wiki/seeing-is-believing]] | Optical illusions and visual perception | draft | 2026-04-21 |
| [[Wiki/tenzai-cybersecurity-startup-strategic-job-application-research]] | Tenzai cybersecurity job application research | draft | 2026-04-21 |

## Sources

| File | Type | Date | Status | Processed To |
|---|---|---|---|---|
| [[Sources/wiki-session-knowledge-ingestion-pipeline]] | conversation | 2026-04-12 | processed | [[Wiki/ingestion-pipeline]], [[Wiki/format-conversion-tools]], [[Wiki/visual-data-preservation]] |

## Working Context

| File | Topic | Status |
|---|---|---|
| [[Working-Context/knowledge-base-build-plan]] | 6-phase implementation plan | active |

## Decisions Log

[[000-Meta/decisions]] -- 8 decisions, all Active as of 2026-04-20.

## Known Issues

[[000-Meta/known-issues]] -- 6 documented issues (KI-001 through KI-006). KI-001/KI-004 resolved 2026-04-22.

## Memory Files

| File | Content |
|---|---|
| [[Memory/profile]] | Gilad's profile, working style, communication rules |
| [[Memory/tool-configs]] | Full AI tool inventory and MCP configuration |
| [[Memory/preferences]] | (empty -- populate as preferences emerge) |

## Scripts

| File | Purpose | Status |
|---|---|---|
| `Scripts/ingest.py` | Batch/single-file PDF+doc converter (pymupdf4llm + pandoc) | Active |
| `Scripts/watch.sh` | fswatch watcher -- triggers ingest.py on new files in source folder; runs as macOS LaunchAgent | Active |
| `Scripts/process.py` | LLM triage + summarization via LiteLLM (Ollama Cloud) | Active |
| `Scripts/session_end.py` | Automated session logging and MEMORY updates | Active |
| `Scripts/linkding_export.py` | Bookmark export pipeline from linkding API | Active |
| `Scripts/transcribe.py` | Audio/video transcription via faster-whisper on Netcup | Active |
| `Scripts/lint.py` | Vault validation -- frontmatter, links, orphans, naming | Active |

## Templates

| Template | Use For |
|---|---|
| [[Templates/source-note]] | Raw ingested content (Sources/) |
| [[Templates/wiki-page]] | Processed knowledge pages (Wiki/) |
| [[Templates/session-log]] | AI session records (000-Meta/log.md) |
| [[Templates/weekly-review]] | Periodic review (000-Meta/) |
