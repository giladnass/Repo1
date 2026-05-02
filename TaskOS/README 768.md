# TaskOS — local-first, Markdown-native task manager

A personal task system that lives inside your Obsidian vault. Your tasks are plain Markdown files. The app is a thin layer on top.

If TaskOS disappeared tomorrow, your tasks would still be there — readable in Obsidian, VS Code, GitHub, Finder, anywhere.

This is the **MVP** (Phase 0 + Phase 1). Capture, list, organise, complete. AI features come in a later phase but the data shape is already AI-ready.

---

## What's in this folder

```
TaskOS/
├── Tasks/
│   ├── Inbox/        ← new tasks land here
│   ├── Active/       ← in progress / scheduled
│   ├── Waiting/      ← waiting on someone else
│   ├── Someday/      ← maybe later
│   └── Completed/    ← archive (kept, not deleted)
├── Projects/         ← one Markdown file per project
├── Areas/            ← one per area of responsibility
├── People/           ← one per person you collaborate with
├── Daily/            ← daily notes
├── Templates/        ← copy-paste templates for new items
├── .system/          ← cache / generated files (always disposable)
└── README.md         ← this file
```

The folders are organisational. The **`status:`** field inside each task file is the source of truth. If a folder and a status disagree, the plugin can fix it via "Reconcile folders to status".

---

## How to start using it (in Obsidian)

1. **Open this vault in Obsidian.** This folder is already inside it.
2. Go to **Settings → Community plugins**. The "TaskOS" plugin should appear and be enabled. If it's listed but disabled, toggle it on. (If Obsidian asks you to "trust the author" because the plugin is local, click trust.)
3. Click the **check-circle icon** in the left ribbon, or run the command **"Open TaskOS panel"** from the command palette (Cmd-P).
4. Click **"+ Capture"** or press **Cmd-Shift-T** to add your first task.

That's it. No installation, no terminal, no build step.

---

## Daily use

- **Capture** — Cmd-Shift-T anywhere in Obsidian. Title is required. Everything else is optional.
- **Today** — the default view. Anything due today, overdue, or scheduled for today.
- **Inbox** — anything you captured but haven't triaged yet.
- **Upcoming / Overdue / Waiting / Someday / Completed** — filter tabs.
- **By project** — pick a project from the dropdown to see only its open tasks.
- **Click a task** to open the underlying Markdown file. Edit it freely — the plugin re-reads it.
- **Tick a task** to mark it complete. The file moves to `Tasks/Completed/`.

---

## How a task is stored

Each task is one Markdown file with a YAML "frontmatter" block at the top. Example:

```markdown
---
id: task_2026-05-02_090000_aa01
type: task
title: "Follow up with Dani about the cybersecurity deck"
status: inbox
priority: medium
due: 2026-05-03
project: "[[Cybersecurity GTM]]"
area: "[[Client Work]]"
people:
  - "[[Dani]]"
tags: [cybersecurity, deck, follow-up]
created: 2026-05-02T09:00:00+03:00
updated: 2026-05-02T09:00:00+03:00
---

# Follow up with Dani about the cybersecurity deck

## Notes

## Activity Log
- 2026-05-02 09:00 — Created
```

A few things to notice:

- **`id`** — never changes. Filenames can change, the id can't. This is what links survive on long-term.
- **Project / area / people** are written as `[[Wikilinks]]`, so Obsidian's backlinks and graph light up for free. Open `Projects/Cybersecurity GTM.md` and the "Linked mentions" panel will show every task pointing at it.
- **`status`** drives folder placement. Edit it manually if you like — the plugin will reconcile.

If you hand-edit the file in Obsidian, the plugin picks up the change.

---

## What the plugin does *not* do (yet)

This is an MVP. On purpose, these are not in this build:

- AI features (natural-language capture, daily planning, refinement, retrieval)
- Recurring tasks (the schema supports `recurrence:` but no engine yet)
- iPhone-specific UX
- A standalone web/desktop app
- Custom sync (use whatever you already use — Obsidian Sync, iCloud, Git)
- Calendar/email integrations

These are mapped out in the architecture plan and will come in later phases without changing the file format.

---

## Sync notes

Everything in this folder syncs through whatever you sync the rest of the vault with. With your current setup:

- **iCloud-synced vaults**: works. Watch for occasional "Conflict" file copies if you edit the same task on two devices simultaneously.
- **Git-synced vaults**: works, and gives you full history. Resolve any merge conflicts as normal — the small file-per-task design keeps conflicts narrow.
- **Obsidian Sync**: best CRDT-style merge experience.

The `.system/` folder is regeneratable cache. You can safely delete it; the plugin will recreate what it needs.

---

## Where the plugin lives

The plugin code is at `.obsidian/plugins/task-os/` in this vault. Three files:

- `manifest.json` — name, version, plugin id
- `main.js` — the plugin logic (plain JavaScript, no build step)
- `styles.css` — styling for the side panel

If you ever want to remove the plugin, delete that folder. Your task data in `TaskOS/` is untouched.

---

## When something looks wrong

- **A task isn't showing up.** Check its `status:` value matches the filter you're on. Click "Reconcile folders to status" in the panel footer to fix folder/status drift.
- **YAML parse error.** A red label appears next to the task title. Open the file and check the frontmatter is well-formed (indentation, quotes around strings with colons, etc.).
- **Folder is empty after a reconcile.** That just means no tasks have that status right now.
- **Cmd-Shift-T doesn't open capture.** Check Obsidian's hotkey settings — another plugin may have claimed it. Reassign in Settings → Hotkeys → "TaskOS: Quick capture task".

---

## Roadmap (what's next)

- **Phase 2a** — AI provider interface (model-agnostic), Anthropic adapter behind it
- **Phase 2b** — natural-language → structured task ("Follow up with Dani tomorrow about the deck" → fully filled-in task)
- **Phase 2c** — daily planning suggestions
- **Phase 2d** — inbox refinement and duplicate detection
- **Phase 3** — decide between a standalone Mac app and a read-mostly browser companion, depending on what's actually missing in daily use

The Markdown files don't change shape between phases. Everything new is additive.
