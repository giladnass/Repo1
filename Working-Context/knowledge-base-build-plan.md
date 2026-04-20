---
title: "Knowledge Base Build Plan"
type: working-context
tags: [meta, project, planning, ai-memory]
created: 2026-04-20
updated: 2026-04-20
status: active
---

## Mission

Build a living, intelligent, tool-accessible knowledge repository on top of the existing AI-Memory vault.

Target properties: living (auto-ingest), intelligent (LLM-powered processing at ingest time), accessible by tools (MCP/standard protocol), accessible by human (Obsidian/Markdown), broad ingest support (PDF/audio/video/web/DOCX/EPUB/conversations), standardized schema, efficient (cost/speed optimized), extensible (add vaults/tools/pipelines without redesigning the core).

---

## Current State Audit (2026-04-20)

### What Exists

| Component | Status | Notes |
|---|---|---|
| Folder structure | ✅ Good | 000-Meta, Memory, Sources, Templates, Wiki, Working-Context |
| CLAUDE.md operational protocol | ✅ Complete | Session start, INGEST, QUERY, LINT, SESSION END defined |
| Ingestion pipeline research | ✅ Rich | `Sources/wiki-session-knowledge-ingestion-pipeline.md` — actionable |
| Templates | ✅ Populated (this session) | source-note, wiki-page, session-log, weekly-review |
| decisions.md | ✅ Populated (this session) | 8 founding decisions locked |
| MEMORY.md | ✅ Populated (this session) | Partial — gaps flagged |
| index.md | ✅ Populated (this session) | |
| Wiki/ | ✅ 4 pages (this session) | Bootstrapped from source doc |
| Memory/profile.md | ❌ Empty | Requires human input |
| Memory/tool-configs.md | ❌ Empty | Requires human input |

### Gaps That Could Force Rework

These unknowns could require architectural changes if assumptions are wrong. Must be resolved before Phase 1.

1. **MCP server details** — Which server (basic-memory? custom?), version, tools/endpoints it exposes. Affects the cross-tool data contract (D-006).
2. **Connected tools inventory** — What tools are actually connected vs. pending. tool-configs.md is blank.
3. **OpenClaw/Aurora** — Not documented in vault. Mission brief says it shares infrastructure. Cannot safely make decisions touching shared infrastructure without knowing what it is.
4. **Shared cross-tool memory pool** — Architecture unknown. Affects how this vault integrates.
5. **Netcup server** — Referenced in source doc but undocumented. OS, specs, access method, what's installed.
6. **"Known unresolved problems"** — Mission brief references these but they aren't in the vault.

---

## Hard-to-Reverse Decisions

All schema, naming, and contract decisions are filed in `000-Meta/decisions.md`. Summary:

| # | Decision |
|---|---|
| D-001 | Convert to MD before ingestion |
| D-002 | Sources are immutable |
| D-003 | Frontmatter schema (canonical) |
| D-004 | Tag namespacing: structural tags use `type/*`, `source-type/*` prefixes |
| D-005 | File naming: lowercase-kebab, no date prefix for wiki pages |
| D-006 | MCP data contract (minimum viable) — Draft |
| D-007 | Processing location: Mac for conversion, Netcup for compute-heavy |
| D-008 | LLM model selection: Haiku/Sonnet/Opus by task type |

---

## Phased Plan

### Phase 0 — Foundation (This session) ✅

Bootstrap the vault so future sessions don't start from scratch.

- [x] Define and lock frontmatter schema (D-003)
- [x] Populate Templates with actual content
- [x] File 8 founding decisions to decisions.md
- [x] Process source doc into 4 wiki pages
- [x] Populate MEMORY.md, index.md
- [x] Write this plan document

**Design principle:** The schema is the most expensive thing to change. Lock it first. Everything else can be iterated.

---

### Phase 1 — MCP Access Layer (Week 1)

Verify and document what every connected tool can actually do against the data contract.

**Requires human input first** (the 6 gaps listed above).

- [ ] Document MCP server: which server, version, endpoints/tools exposed
- [ ] Populate Memory/tool-configs.md with each connected tool and its capabilities
- [ ] Verify read/write from each connected tool against D-006 contract
- [ ] Identify gaps: which tools need workarounds? which need a different access method?
- [ ] Document OpenClaw/Aurora shared infrastructure
- [ ] Finalize D-006 (MCP data contract) from Draft → Active

**Why this before pipelines:** No point building ingestion if the output can't be read by the tools that need it.

---

### Phase 2 — Ingestion Pipelines (Weeks 1–2)

Build the conversion layer that turns raw content into processable Markdown. All tooling is already researched — this is installation + scripting + testing.

**PDF/Office/EPUB (Mac):**
- [ ] Install and test `marker` (ML PDF conversion)
- [ ] Install and test `pandoc` (DOCX, EPUB, PPTX)
- [ ] Evaluate `docling` (IBM) as potential unified replacement
- [ ] Build watch folder + conversion script (`fswatch` trigger on Mac)

**Audio/Video (Netcup):**
- [ ] Install and test `faster-whisper` with `whisper-large-v3`
- [ ] Build batch queue for overnight audio/video processing
- [ ] Build ffmpeg pre-processing step (extract audio from video)

**URL/Bookmarks:**
- [ ] Set up `linkding` as capture point (self-hosted bookmark manager)
- [ ] Evaluate ArchiveBox vs. Firecrawl for page archival
- [ ] Build triage pipeline: URL → archive → Claude API classify → route

See [[Wiki/ingestion-pipeline]] and [[Wiki/format-conversion-tools]] for the full tool inventory and rationale.

**Why this before LLM processing:** The LLM processing step is just an additional stage appended to this pipeline. Get the pipeline working end-to-end first.

---

### Phase 3 — LLM Processing Layer (Weeks 2–3)

Add intelligence after conversion: auto-tag, auto-summarize, route, cross-reference.

- [ ] Build ingest script: converted MD → Claude API → structured source note
- [ ] Auto-tagging prompt (Haiku): extract topic tags from content
- [ ] Auto-summarization (Sonnet): 2–5 sentence summary
- [ ] Routing logic (Haiku): full ingest / summary-only / index-only
- [ ] Cross-referencing (Sonnet): find related wiki pages, suggest wikilinks
- [ ] Visual extraction pipeline for high-value docs (Opus): charts/diagrams → MD
- [ ] Configure Claude API batch endpoint for non-urgent processing queues

**Routing thresholds:**

| Signal | Route |
|---|---|
| High info density, novel content | Full ingest → Source Note + Wiki page(s) |
| Redundant with existing wiki content | Summary-only → Source Note only |
| Low value, reference material | Index-only → URL + title + tags in index MD |

**Why batch API matters:** A large URL backlog or media archive processed at real-time API costs would be expensive. Batch processing (async, ~50% cost reduction) makes bulk ingestion economically viable.

---

### Phase 4 — Conversation Capture (Week 3)

Close the loop: ensure AI sessions themselves become vault content.

- [ ] Formalize Claude Code session output format (this session is the template)
- [ ] Build session-end script: writes handoff, MEMORY, log, wiki pages, commits
- [ ] Evaluate Claude.ai export workarounds for non-Claude Code sessions
- [ ] Decide: should each Claude Code session auto-commit to git?

Claude Code is already the best solution here. This session is proof of concept: full filesystem access + can write to vault directly. The gap is making it automatic and consistent, not manual and dependent on remembering.

---

### Phase 5 — URL Pipeline (Week 4)

Handle the existing bookmark backlog (estimated: thousands of URLs).

- [x] Deploy linkding (done in Phase 2)
- [x] Page archival: Singlefile browser extension captures full HTML at save time -- ArchiveBox and Firecrawl are not needed
- [ ] Build linkding export -> ingest pipeline: pull archived HTML from linkding API, convert to MD via `ingest.py` (HTML already supported), feed to LLM triage
- [ ] Build Claude API batch triage job: ingest-worthy? -> full / summary / index
- [ ] Process high-value URLs first (manually curated seed set)

**Archival decision:** Singlefile + linkding replaces ArchiveBox/Firecrawl. HTML captured by Singlefile is already handled by `Scripts/ingest.py` (pandoc converts HTML to MD). The remaining gap is pulling archived HTML out of linkding via its REST API and routing it into the ingestion queue.

---

### Phase 6 — Integration & Extension (Month 2)

Requires gap answers from Phase 1 before this can be designed.

- [ ] OpenClaw/Aurora integration (shared infrastructure — document first)
- [ ] Shared cross-tool memory pool connection
- [ ] Additional AI tool connections beyond currently connected set
- [ ] Periodic LINT automation (weekly cron job)
- [ ] Weekly review automation

---

## What Makes the Next Component Easier

Each phase deliberately lowers the cost of the next:

- **Phase 0 schema** → Phase 3 LLM prompts can rely on consistent structure; no parsing variance
- **Phase 1 tool docs** → Phase 6 integration knows exactly what each tool can/can't do
- **Phase 2 pipelines** → Phase 3 just appends an LLM step to an existing working pipeline
- **Phase 3 processing** → Phase 5 URL pipeline reuses the same routing/tagging logic
- **Phase 4 conversation capture** → Every future session auto-bootstraps the knowledge base
- **Phase 5 URL backlog** → Most content is already processed when Phase 6 extensions arrive

---

## Open Questions Requiring Human Input

1. Which MCP server is running and what does it expose?
2. What AI tools are currently connected? (to populate Memory/tool-configs.md)
3. What is OpenClaw/Aurora and what infrastructure does it share with this vault?
4. What are the "known unresolved problems" referenced in the mission brief?
5. What is the Netcup server setup (OS, specs, access method, what's installed)?
6. What is Gilad's profile for Memory/profile.md?
