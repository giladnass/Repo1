---
title: CLAUDE
type: note
permalink: ai-memory/000-meta/claude
---

# AI Knowledge Base Schema

## Identity
This vault belongs to Gilad. It serves as a shared knowledge repository
accessible by multiple AI tools (Claude, Gemini, Claude Code, Genspark,
Manus, NotebookLM, and others).

## Session Start Protocol
At the start of EVERY session, read these files in order:
1. `000-Meta/MEMORY.md` — Current persistent context
2. `000-Meta/index.md` — Wiki content map
3. `000-Meta/handoff.md` — Last session's handoff notes
4. Relevant `Working-Context/` files for the active project

## Core Rules
- All markdown files MUST follow Obsidian conventions
- Use [[wikilinks]] for internal cross-references
- Every wiki page needs YAML frontmatter (title, tags, created, updated)
- The wiki is a persistent, compounding artifact — NEVER delete without cause
- YOU maintain the wiki — summarize, cross-reference, file, and bookkeep
- File good answers back into the wiki as new pages

## Operations

### INGEST (when given new source material)
1. Save raw source to `Sources/` (immutable)
2. Read and extract key information
3. Create/update relevant wiki pages in `Wiki/`
4. Update `000-Meta/index.md` with new entries
5. Log the action in `000-Meta/log.md`

### QUERY (when asked a question)
1. Search relevant wiki pages first
2. Synthesize answer from existing knowledge
3. If the answer reveals new insights, file them back into the wiki
4. Log the query in `000-Meta/log.md`

### LINT (periodic maintenance)
1. Check for contradictions between pages
2. Identify stale claims superseded by newer sources
3. Find orphan pages not linked from anywhere
4. Detect missing cross-references
5. Flag pages with outdated `updated` timestamps
6. Report findings and suggest fixes

### SESSION END
1. Write a handoff note to `000-Meta/handoff.md`:
   - What was accomplished
   - What needs human review
   - Deferred tasks
   - Suggested next steps
2. Update `000-Meta/MEMORY.md` if any persistent context changed
3. Log session summary in `000-Meta/log.md`

## Frontmatter Template
```yaml
---
title: "Page Title"
tags: [topic, subtopic]
created: YYYY-MM-DD
updated: YYYY-MM-DD
source: "[[link-to-source]]"
status: active | archived | needs-review
---