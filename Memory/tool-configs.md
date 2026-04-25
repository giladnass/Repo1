---
title: tool-configs
type: note
tags: [memory, tools, mcp, infrastructure]
created: 2026-04-20
permalink: ai-memory/memory/tool-configs
---

# AI Tool Configurations

## Shared Memory Pool: Connection Status

*Last updated: 2026-04-25*

The vault (this repo) is the shared memory. basic-memory MCP is the access layer. Tools that connect to the MCP endpoint read and write to the same vault.

| Tool | Status | Method | Notes |
|---|---|---|---|
| **Claude Desktop** | Connected | Local stdio MCP | Mac, direct filesystem access |
| **Claude.ai web** | Connected | Remote MCP via URL | Configured in claude.ai MCP settings |
| **Claude mobile** | Connected | Remote MCP via URL | Same remote endpoint |
| **Claude Code** | Connected | Local vault + remote MCP | Works on dev branch `claude/caveman-lite-vrjM3` |
| **Aurora (OpenClaw)** | Connected | Native MCP + `mcporter` fallback | v2026.4.24 surfaces tools natively. mcporter still documented in AGENTS.md as fallback. |
| **Gemini CLI** | Connected | Remote HTTP (Streamable HTTP) | Configured in `~/.gemini/settings.json` with `httpUrl`. Same model as Gemini Web, with native MCP. |
| **Perplexity** | Connected | stdio via `mcp-remote` bridge | Mac Desktop app. Settings > Connectors > Advanced. `mcp-remote` at `/Users/giladnass/.nvm/versions/node/v24.14.1/bin/mcp-remote`. |
| **Manus** | Connected | Streamable HTTP (direct) | Settings > Integrations > Custom MCP. Tested: Read and Write verified. |
| **Genspark** | Blocked | Streamable HTTP (direct) | UI bug: text input field in "Add New MCP" screen is non-functional across browsers. Deferred for later research. |
| **ChatGPT** | Limited | Streamable HTTP (Apps/Developer Mode) | Plus/Pro: read-only. Business/Enterprise: full read+write. Settings > Apps > Create. Low priority. |
| **NotebookLM** | Not connected | No MCP client | Use `notebooklm-mcp` bridge from Claude Code (one-way: Claude queries NotebookLM). No bidirectional path. |
| **Gemini Web** | Not connected | No MCP client in web UI | No extension model. Use Gemini CLI instead (same model, has MCP). |

### MCP Endpoint

```
https://memory.giladn.com/mcp/ebc69cbd338019004dfd1738a033ced1e22e21ff62a41b41ef0b8caf5d9fb3a5
```

The URL path is the auth token. Path-based auth, no headers needed. Transport: streamable-http.

### Known Issue: KI-006 (OpenClaw MCP Bug)

OpenClaw's `bundle-mcp` fails to connect to basic-memory. Two approaches tried, both fail:
- HTTP direct: returns 404 (streamable-http vs SSE protocol mismatch)
- stdio/mcp-remote: "Connection closed" error

Workaround: Aurora uses the `mcporter` skill to call `mcporter call basic-memory.<tool>` directly. This works but is not native tool integration.

### Known Issue: Netcup Vault Sync

The 5-minute cron (`git pull origin main --quiet`) was failing silently due to local uncommitted changes blocking pulls. Vault was 43 commits behind (April 12 -> April 23). Fixed with `git stash && git pull`. basic-memory reindex required after large pulls (`/root/.local/bin/basic-memory reindex --project AI-Memory`).

### Key Gap: Branch Merge

Claude Code works on branch `claude/caveman-lite-vrjM3`. Obsidian and Aurora read from `main`. Changes made in Claude Code sessions are invisible to other tools until that branch is merged into `main`. This is the most significant sync gap in the current setup.

---

## MCP Access Layer -- Basic-Memory

**Server:** basic-memory (cloud-hosted)
**Version:** Unknown (cloud-managed)

> **Security note:** The MCP endpoint URL contains an auth token. If `giladnass/Repo1` is a public GitHub repository, storing the full URL here exposes the token. Store in a private file or environment variable if the repo is public. The URL structure is: `https://memory.giladn.com/mcp/<token>`.

**Exposed tools:**

| Tool | Purpose |
|---|---|
| `write_note` | Create a new note |
| `read_note` | Read a note by path or permalink |
| `edit_note` | Update an existing note |
| `delete_note` | Delete a note (use with caution) |
| `search_notes` | Full-text search |
| `search` | Semantic search |
| `list_directory` | Browse folder contents |
| `move_note` | Rename or move a note |
| `recent_activity` | What changed recently |
| `build_context` | Assemble context from multiple notes |
| `canvas` | Canvas/whiteboard view |
| `read_content` | Read note content |
| `view_note` | View formatted note |
| `fetch` | Fetch a URL |
| `create_memory_project` | Create a new project/vault (admin) |
| `delete_project` | Delete a project (admin) |
| `list_memory_projects` | List all projects (admin) |
| `list_workspaces` | List workspaces (admin) |
| `cloud_info` | Server info (meta) |
| `release_notes` | Version info (meta) |
| `schema_infer` | Infer schema from content (meta) |
| `schema_validate` | Validate against schema (meta) |
| `schema_diff` | Diff two schemas (meta) |

**MCP Data Contract (D-006) verdict:** SATISFIED. basic-memory provides read, write, update, full-text search, semantic search, and directory browse. D-006 is now Active (was Draft).

---

## Claude.ai MCP Integrations (connected)

All tools below are connected via claude.ai MCP settings and available in Claude sessions.

| Tool | Role | Ingestion relevance |
|---|---|---|
| **Basic-Memory** | Vault read/write | Core |
| **Zapier** | Automation triggers and actions | High -- can replace `fswatch` watch folder triggers |
| **Google Drive** | File access | High -- simplifies Google Workspace ingestion (Phase 2) |
| **Gmail** | Email read/compose | Medium -- potential ingest source |
| **Google Calendar** | Calendar read/write | Low |
| **Notion** | Documents and databases | Medium -- potential ingest source |
| **Slack** | Messaging | Low |
| **monday.com** | Project management | Low |
| **Canva** | Design | Low |

---

## Server-Side (Netcup)

| Service | Type | Access |
|---|---|---|
| **Ollama** | Local inference | systemd service; accessible on Tailscale |
| **OpenClaw** | AI agent gateway | systemd user (`openclaw`); see [[Wiki/openclaw-aurora]] |
| **AnythingLLM** | LLM interface | Docker, `127.0.0.1:3001` (local only) |
| **Open WebUI** | LLM interface | Docker, `0.0.0.0:3000` mapped to `8080` (public) |

---

## Self-Hosted (Netcup)

| Service | Access | Notes |
|---|---|---|
| **linkding** | `http://152.53.244.42:9090` | Bookmark manager; browser extension installed. Configured with Singlefile for full-page HTML archiving at capture time. **Known bug:** "copy" button for API token in Settings > Integrations doesn't always copy -- select-all manually instead. |
| **Singlefile** | Browser extension | Captures bookmarked pages as single self-contained HTML files. Integrated with linkding via config at https://linkding.link/archiving/ |

| Provider | Model | Used By |
|---|---|---|
| Anthropic | Claude (all versions) | claude.ai, Claude Code |
| Google | Gemini 2.5 Pro | Gemini CLI (connected to vault via MCP) |
| OpenRouter | `moonshotai/kimi-k2.5` | OpenClaw primary (200k ctx) |
| Ollama Cloud | `minimax-m2.5:cloud` | OpenClaw fallback 1 (Pro subscription, user: giladn) |
| OpenRouter | `google/gemini-2.0-flash-001` | OpenClaw fallback 2 |
| Ollama Cloud | `qwen3.5:cloud` | process.py triage model |
| Ollama Cloud | `glm-5:cloud` | process.py summarization model |

---

## Other AI Tools in Active Use

| Tool | Role |
|---|---|
| NotebookLM | Synthesis layer for multi-source research (bridge via `notebooklm-mcp` from Claude Code) |
| Gemini CLI | Connected to vault via MCP. Same model as Gemini Web, with native read/write to knowledge base |
| Genspark, Manus | Deep research; findings brought to Claude for execution. Both support custom MCP servers (unconfigured) |
| Perplexity | Deep research. Pro plan supports custom MCP connectors (unconfigured) |
| Aurora (OpenClaw) | Always-on agent on Netcup via Telegram and Discord. Vault access via mcporter skill workaround |

