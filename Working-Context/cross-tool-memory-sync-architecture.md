---
title: Cross-Tool Memory Sync Architecture (Draft)
type: note
created: 2026-04-27
status: draft
permalink: ai-memory/working-context/cross-tool-memory-sync
---

# Cross-Tool Memory Sync Architecture

*User prompt: "I want the shared memory between the AI tools to be as updated as possible... It has to run automatically."*

**Status:** Draft — user requested time to think. Do not implement until user approves.

---

## Problem

Session capture is manual. `session_capture.py` only runs when the user remembers to trigger it. When switching from Tool A to Tool B, Tool B starts blind unless the user explicitly ran capture first. This breaks the "Tool B continues from where Tool A stopped" goal.

---

## Proposed Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  TOOL A (Claude Code)          TOOL B (Aurora)               │
│  ├─ JSONL log (local)          ├─ JSONL log (Netcup)      │
│  └─ MCP client                 └─ MCP client              │
│         │                            │                     │
│         └────────┬───────────────────┘                     │
│                  ▼                                         │
│         ┌──────────────┐                                   │
│         │ basic-memory │  ← shared MCP server (Netcup)   │
│         │   MCP API    │     latency: < 1 second          │
│         └──────┬───────┘                                   │
│                │                                           │
│                ▼                                           │
│    ┌──────────────────────┐                              │
│    │  Vault (Git-backed)  │  ← Obsidian, durability      │
│    │  AI-Memory on Mac   │                              │
│    └──────────────────────┘                              │
│                                                            │
│  ┌────────────────────────────────────────────────────┐ │
│  │  SYNC ORCHESTRATOR (LaunchAgent, every 10 min)      │ │
│  │  1. Extract raw transcript (Claude Code JSONL)      │ │
│  │  2. Extract raw transcript (Aurora JSONL via SSH)  │ │
│  │  3. Pull Gemini Inbox                              │ │
│  │  4. Write drafts to basic-memory MCP               │ │
│  │  5. If session ended: LLM summarize + vault commit│ │
│  │  6. Git push + trigger Netcup pull                 │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Tiered Sync (Key Idea)

| Tier | Frequency | Content | Destination | Cost |
|---|---|---|---|---|
| **Hot** | Every 10 min | Raw transcript, bullet list of turns | basic-memory MCP | Cheap (no LLM) |
| **Cold** | Session end only | LLM summary, structured handoff | Vault Git + basic-memory | Expensive (LLM call) |

**Rationale:** Hot sync gives Tool B immediate continuity. Cold sync gives archival quality. Don't pay LLM cost every 10 min.

---

## Per-Tool Capture Strategy

| Tool | Can Auto-Capture? | Hot Sync Method | Cold Sync Method |
|---|---|---|---|
| **Claude Code** | Yes | Read JSONL every 10 min | `session_capture.py` on exit |
| **Aurora/OpenClaw** | Yes | Read session JSONL on Netcup | Similar script, Ollama local summary |
| **Gemini** | Yes | `gemini_bridge.py --watch` | Already ingests on pull |
| **Claude Desktop** | No | Opaque sessions | Manual `/memory save` or accept loss |
| **Claude.ai web** | No | No export API | Manual copy or accept loss |
| **Perplexity** | No | Opaque | Manual or accept loss |
| **Manus** | No | Opaque | Manual or accept loss |
| **ChatGPT** | Limited | Plus/Pro read-only | Manual or accept loss |

---

## Serialization Guarantee

**Requirement:** Ingest from A before retrieve by B.

**How:**

1. Tool B's session start protocol already reads `MEMORY.md` and `handoff.md`
2. Add step: **Tool B queries basic-memory MCP for `recent_activity`** at session start
3. The orchestrator writes hot-sync notes to basic-memory every 10 min
4. Max lag: 10 minutes (acceptable for human switching)
5. Git sync provides durable backup; MCP is the fast path

**Tool B startup protocol:**
```
1. basic-memory.recent_activity(limit=5)  ← sees Tool A's hot-sync notes
2. Read MEMORY.md
3. Read handoff.md
4. Continue work
```

---

## Implementation: `sync_orchestrator.py`

A single daemon running as LaunchAgent `com.giladnass.ai-memory-sync-orchestrator` every 10 minutes.

**Core loop:**
```python
def run():
    changed = False

    # 1. Claude Code hot sync
    if claude_jsonl_has_new_turns():
        raw = extract_raw_transcript(claude_jsonl)
        basic_memory.write_note(
            title=f"Claude-Code-Draft-{timestamp}",
            content=raw,
            directory="Working-Context/Drafts"
        )
        changed = True

    # 2. Aurora hot sync (SSH to Netcup)
    if aurora_jsonl_has_new_turns():
        raw = ssh_extract_latest_session()
        basic_memory.write_note(
            title=f"Aurora-Draft-{timestamp}",
            content=raw,
            directory="Working-Context/Drafts"
        )
        changed = True

    # 3. Gemini Inbox pull
    if gemini_bridge_pull() > 0:
        changed = True

    # 4. Commit if changed
    if changed:
        git_commit_push()
        ssh_netcup("cd AI-Memory && git pull")

    # 5. Check session end (idle > 20 min)
    if claude_session_idle():
        session_capture.py  # or LLM summary
```

---

## Open Questions (User to Decide)

1. **Cadence:** Confirm 10 minutes, or prefer 5 / 20?
2. **Idle threshold:** How many minutes of inactivity = "session ended"? (Suggest 20 min)
3. **Draft retention:** Keep raw drafts permanently or delete after cold sync? (Suggest delete)
4. **Manual override:** Should `/sync` command exist in tools for immediate trigger?

---

## Why Progress Doesn't Evaporate

**Three persistence layers:**

1. **Vault (AI-Memory):** Git-backed Markdown. Every change is committed and pushed. Survives forever.
2. **basic-memory MCP:** SQLite index on the vault. Fast query layer for tools. Auto-rebuilds from vault.
3. **GitHub:** Central sync hub. Mac pushes instantly, Netcup pulls every 5 min. Both directions covered.

**Session continuity mechanism:**
- This file lives in the vault
- It is committed to Git
- It is indexed by basic-memory
- Any tool (Claude Code, Aurora, Gemini) can read it via MCP
- It will be there in the next session

**To recall this plan:**
- Ask Claude Code: "find the cross-tool memory sync architecture plan"
- Claude Code will query basic-memory MCP and find this file
- Or navigate to: `Working-Context/cross-tool-memory-sync-architecture.md`

---

*Last updated: 2026-04-27*
*Status: Draft — awaiting user approval before implementation*
