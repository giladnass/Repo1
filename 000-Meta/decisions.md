---
title: decisions
type: note
tags: [meta, decisions, schema]
created: 2026-04-20
permalink: ai-memory/000-meta/decisions
---

# Decisions Log

Hard-to-reverse architectural decisions for the AI-Memory system. Each entry includes the decision, rationale, date, and status. Changing any of these requires a new decision entry explaining the migration path.

---

## D-001 — Convert to Markdown Before Ingestion
**Date:** 2026-04-12
**Status:** Active
**Source:** [[Sources/wiki-session-knowledge-ingestion-pipeline]]

All source files are pre-converted to Markdown before ingestion. Raw binary formats (PDF, DOCX, audio, video, etc.) are not fed directly into processing pipelines.

**Rationale:** basic-memory and vector systems are optimized for plain text. Conversion quality is inspectable and correctable before ingestion. MD is portable, Git-versionable, and human-readable. Processing speed is dramatically faster on pre-converted text.

**Implications:** Requires a conversion step for every non-MD source. Introduces conversion tooling as a dependency (see [[Wiki/format-conversion-tools]]).

---

## D-002 — Sources Are Immutable
**Date:** 2026-04-20
**Status:** Active

Files placed in `Sources/` are never edited after creation. New information goes into `Wiki/` pages. Corrections go in wiki pages with a note referencing the original source.

**Exception:** Adding missing YAML frontmatter to a source file is permitted (metadata only, not content).

**Rationale:** Preserves the provenance chain. Sources represent what was captured at ingest time; wiki pages represent current synthesized understanding. Immutability makes the system trustworthy.

---

## D-003 — Frontmatter Schema (Canonical)
**Date:** 2026-04-20
**Status:** Active

**All files** must include:
- `title` (string) — human-readable page title
- `type` (controlled vocab) — `wiki | source | decision | session-log | weekly-review | working-context | template | note`
- `tags` (array) — lowercase-kebab strings
- `created` (ISO date YYYY-MM-DD)

**Wiki pages** additionally require:
- `updated` (ISO date)
- `sources` (array of wikilinks)
- `status` — `active | needs-review | archived | draft`
- `confidence` — `high | medium | low | speculative`

**Source notes** additionally require:
- `source-type` — `pdf | docx | epub | audio | video | url | conversation | note`
- `ingested` (ISO date)
- `status` — `raw | processed | archived`
- `origin` (string) — URL, filename, or provenance description
- `processed-to` (wikilink) — points to the wiki page(s) derived from this source

See `Templates/` for canonical file templates.

**Rationale:** Consistent frontmatter enables LLM-powered filtering, cross-tool interoperability, and automated maintenance (LINT). Must be locked early because changing it requires migrating all existing content.

---

## D-004 — Tag Namespacing Convention
**Date:** 2026-04-20
**Status:** Active

Structural/system tags use namespace prefixes:
- `type/*` — mirrors the `type` frontmatter field (useful for tag-based search in Obsidian)
- `source-type/*` — format of origin material
- `status/*` — mirrors the `status` field

Domain/topic tags are free-form: lowercase-kebab, no namespace, no spaces.

Valid examples: `ingestion`, `llm`, `tools`, `video-processing`, `source-type/pdf`, `status/needs-review`

**Rationale:** Namespace prefixes enable prefix-based filtering by any tool. Domain tags stay unrestricted to avoid taxonomy overhead. The convention is self-documenting.

---

## D-005 — File Naming Convention
**Date:** 2026-04-20
**Status:** Active

- All files: `lowercase-kebab-case.md`
- Wiki pages: no date prefix. Date is in frontmatter `created` field.
- Daily notes / session logs: `YYYY-MM-DD.md` or `YYYY-MM-DD-description.md`
- No version numbers in filenames — use git history for versioning
- Folder structure is fixed; do not create ad-hoc subfolders without a documented decision

**Rationale:** Stable filenames make wikilinks durable across time. Date-prefixed files are time-indexed; wiki pages are topic-indexed.

---

## D-006 — MCP Data Contract (Minimum Viable)
**Date:** 2026-04-20
**Status:** Active (verified 2026-04-20)

Any AI tool interacting with this vault must support:
- **Read** — retrieve a page by permalink or filename
- **Search** — full-text search across wiki pages
- **Filter** — by frontmatter fields (type, tags, status)
- **Write** — create a new page conforming to D-003 schema
- **Update** — modify an existing page, updating the `updated` timestamp

Tools that cannot meet this contract may participate read-only via direct file access (vault is plain Markdown on the filesystem, synced via Git).

**Verification (2026-04-20):** basic-memory is confirmed as the MCP server. It exposes `write_note`, `read_note`, `edit_note`, `delete_note`, `search_notes`, `search` (semantic), `list_directory`, `move_note`, `recent_activity`, `build_context`, and more. All contract requirements are satisfied. D-006 is now Active.

See [[Memory/tool-configs]] for the full tool inventory.

---

## D-007 — Processing Location Strategy
**Date:** 2026-04-12
**Status:** Active
**Source:** [[Sources/wiki-session-knowledge-ingestion-pipeline]]

| Content Type | Where to Process | Why |
|---|---|---|
| PDF/Office/EPUB conversion | Mac | Fast, low compute |
| Audio/video transcription | Netcup server | Compute-heavy, unattended overnight |
| Visual extraction pipeline | Netcup server | SAM requires CPU/GPU headroom |
| URL scraping | Netcup server | Long-running, network-bound |
| LLM API calls (tagging, summarization) | Either | API-bound, not compute-bound |

---

## D-009 -- Primary PDF Converter: pymupdf4llm (replaces Marker)
**Date:** 2026-04-20
**Status:** Active
**Supersedes:** Marker as primary PDF converter

`pymupdf4llm` replaces `marker` as the primary PDF-to-Markdown converter.

**Why Marker was dropped:** Marker's dependency `surya` has an Apple Silicon MPS bug that crashes on PDFs generating long sequences (`torch.AcceleratorError: index 8192 is out of bounds`). CPU fallback is too slow to be practical. See KI-005 in [[000-Meta/known-issues]].

**Why pymupdf4llm:** No ML models, no MPS dependency, runs fast on any hardware. Good quality for text-based PDFs. Limitation: does not handle visually complex PDFs (charts, figures) as well -- addressed by the visual extraction pipeline for high-value documents when needed.

**Future:** Evaluate `docling` (IBM) as potential unified replacement. Marker remains installed for retry when surya fixes the MPS bug.

**Script:** `Scripts/ingest.py`

---

## D-008 — LLM Model Selection Strategy
**Date:** 2026-04-20
**Status:** Active

| Task | Model | Rationale |
|---|---|---|
| Routing, tagging, triage | claude-haiku-4-5 | Fast, cheap, sufficient for classification |
| Summarization, cross-referencing | claude-sonnet-4-6 | Balanced quality and cost |
| Visual extraction, complex synthesis | claude-opus-4-7 | Best quality; use sparingly |

Use Claude API batch endpoint for non-urgent processing (tagging backlogs, summarizing large queues). Real-time interactive sessions use streaming.

**Rationale:** Not every operation needs the best model. Routing decisions at ingest cost fractions of a cent each at Haiku pricing; doing them at Opus pricing would make large-scale ingestion economically unsustainable.
