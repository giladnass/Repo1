# TaskOS — architecture & roadmap

This document captures the design decisions behind TaskOS, in plain language. Read it when you want to understand *why* something is built the way it is, or when handing the project to another developer or AI tool.

---

## Core principle

**Markdown files are the source of truth.** Everything else — the plugin, future AI features, indexes, embeddings — is a layer that can be deleted and rebuilt without losing data.

If TaskOS disappears, your tasks remain readable, editable, and migratable in any Markdown-aware tool.

---

## The platform decision

The hardest constraint is the three target platforms (Mac, iPhone, browser) having very different abilities to read local Markdown files.

| Approach | Mac | iPhone | Browser | Effort |
|---|---|---|---|---|
| **Obsidian plugin** | Excellent | Excellent (Obsidian mobile) | None | Low |
| Standalone desktop app | Excellent | None | None | Medium |
| PWA / web app | OK on Chromium only | **Not possible** for local files on iOS | OK | High |
| Native iOS app | None | Yes | None | Very high |

**Decision:** start with an **Obsidian plugin**. It gives Mac + iPhone + sync for free, leaves the door open for a standalone Mac app and a read-mostly web companion later, and never forces a proprietary format.

iPhone Safari has no real local file system access. There's no honest workaround. Obsidian mobile *is* the iPhone story.

---

## Architecture in one diagram

```
   ┌─────────────────────────────────────────────────┐
   │         The vault (Markdown files)              │  ← source of truth
   │  TaskOS/Tasks/*.md, /Projects/*.md, /Daily/*.md │
   └────────────────────┬────────────────────────────┘
                        │ read/write
   ┌────────────────────▼────────────────────────────┐
   │  Obsidian (Mac, iPhone, iPad)                   │
   │   ├── TaskOS plugin  ← this MVP                 │
   │   │     • side panel views                      │
   │   │     • quick capture modal                   │
   │   │     • status/folder reconciliation          │
   │   │     • AIProvider interface (later phase)    │
   │   └── obsidian-git, dataview, etc.              │
   └─────────────────────────────────────────────────┘
                        │
                        │ via your existing sync
   ┌────────────────────▼────────────────────────────┐
   │  Sync layer (your choice, not owned by TaskOS)  │
   │  iCloud, Obsidian Sync, Git, Dropbox, ...       │
   └─────────────────────────────────────────────────┘

   Future, optional:
   • Standalone Mac app reading the same vault folder
   • Read-mostly web app reading a Git mirror of the vault
```

---

## Folder layout

```
TaskOS/
├── Tasks/
│   ├── Inbox/      ← captured, not yet triaged
│   ├── Active/     ← in progress (includes "scheduled")
│   ├── Waiting/    ← waiting on someone
│   ├── Someday/    ← maybe later
│   └── Completed/  ← archived (also catches "canceled")
├── Projects/
├── Areas/
├── People/
├── Daily/
├── Templates/
└── .system/        ← regeneratable cache only
```

The folder a task lives in mirrors its `status:` field. **The status field is canonical.** If they disagree, run "Reconcile folders to status" — the file moves, the status stays.

---

## Schema

### Task
```yaml
id: task_2026-05-02_143012_ab12   # stable, generated, never changes
type: task
title: "..."
status: inbox|active|scheduled|waiting|someday|completed|canceled
priority: low|medium|high|critical|null
due: YYYY-MM-DD|null              # real deadline
scheduled: YYYY-MM-DD|null        # day you intend to work on it
deferred_until: YYYY-MM-DD|null
project: "[[Project Name]]"|null  # wikilink → Obsidian backlinks free
area: "[[Area Name]]"|null
people:
  - "[[Person]]"
tags: [list, of, strings]
source: null
created: ISO8601 with offset
updated: ISO8601 with offset
completed: ISO8601 with offset|null
recurrence: null                  # schema reserved for later
```

### Project
```yaml
id: project_<slug>
type: project
name: "..."
status: active|paused|archived
area: "[[Area]]"|null
created: ISO
updated: ISO
tags: [...]
```

### Daily, Area, Person
See `TaskOS/Templates/`.

**Why wikilinks for project/area/people:** Obsidian's graph and backlinks work without writing any code. A project file's "Linked mentions" pane is automatically a list of all tasks pointing at it.

---

## ID strategy

Format: `task_YYYY-MM-DD_HHMMSS_xxxx` where `xxxx` is 4 random base-36 chars.

- Sortable
- Human-readable
- Collision-resistant within a session
- Independent of filename — you can rename files freely without breaking links

The filename is `<slug>__<id>.md`. The slug is for humans browsing the folder; the id is what code relies on.

---

## AI architecture (Phase 2, designed not built)

A single TypeScript-style interface, multiple providers behind it:

```
AIProvider {
  extractTasks(text, vaultContext) -> TaskDraft[]
  planDay(tasks, date) -> DayPlan
  refineTask(task) -> TaskRefinement
  cleanInbox(tasks) -> CleanupSuggestion[]
  answerQuestion(q, retrievedDocs) -> Answer
}
```

- Default provider: Anthropic (Claude). Best at structured extraction in our experience.
- Pluggable: OpenAI, Gemini, local — same interface.
- The app **works without an API key.** Every AI feature has a non-AI fallback (manual form, plain search).
- Retrieval: keyword search first; embeddings stored under `.system/embeddings/` only when proven needed.
- Every AI write goes through preview → confirm → log. No silent rewrites.

---

## Safety rules

- Never delete a user's Markdown file. "Complete" moves to `Completed/`. "Cancel" does the same.
- Never rewrite files outside `TaskOS/`. The plugin checks `path.startsWith(rootFolder + '/')` on every operation.
- Frontmatter parse errors don't crash — they show a red badge so you can fix the file.
- All AI suggestions are dry-run by default.

---

## Sync notes

| Method | Compatibility | Watch out for |
|---|---|---|
| Obsidian Sync | Best | None significant |
| iCloud Drive | Good | Occasional `(conflict).md` copies |
| Git (obsidian-git) | Good, full history | Merge conflicts on simultaneous edits |
| Dropbox | OK | Slower mobile sync |
| Syncthing | OK | Setup overhead |

Small files (one task per file) keep conflicts narrow. The `id` field survives any conflict-resolution rename.

---

## Roadmap

| Phase | Scope | Status |
|---|---|---|
| 0 | Vault scaffold, templates, sample data | Done |
| 1 | Obsidian plugin: capture, views, status ops, reconcile | Done (this MVP) |
| 2a | AI provider interface, Anthropic adapter, settings UI | Planned |
| 2b | Natural-language capture | Planned |
| 2c | Daily planning ("plan my day") | Planned |
| 2d | Inbox refinement & duplicate detection | Planned |
| 3 | Standalone Mac app **or** read-mostly web app — decide based on real friction | Deferred |

Schema is stable across phases. Phase 2+ adds capability without breaking files written in Phase 1.

---

## Risks / open issues

1. **iPhone limitations** — Obsidian mobile plugin API is a subset of desktop. Plugin must avoid Node-only APIs. Current code uses only `obsidian` exports, which work on both.
2. **Manual file moves vs. status field** — handled by `Reconcile folders to status`, but document it for new users.
3. **YAML drift** — if a user breaks frontmatter while hand-editing, the task is hidden from views and flagged with a parse-error badge.
4. **AI cost / privacy** — opt-in per feature, no default outbound calls, redaction TODO before sending vault content to a model.
5. **Lock-in risk** — by design, zero. Markdown is the contract.
