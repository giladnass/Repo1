---
title: tool-configs
type: note
permalink: ai-memory/memory/tool-configs
---

# AI Tool Configurations

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
| **linkding** | `http://152.53.244.42:9090` | Bookmark manager; browser extension installed. **Known bug:** "copy" button for API token in Settings > Integrations doesn't always copy -- select-all manually instead. |

| Provider | Model | Used By |
|---|---|---|
| Anthropic | Claude (all versions) | claude.ai, Claude Code |
| Groq | `llama-3.1-8b-instant` | OpenClaw fallback 1 (free tier) |
| OpenRouter | `google/gemini-2.0-flash-001` | OpenClaw fallback 2 |

---

## Other AI Tools in Active Use

| Tool | Role |
|---|---|
| NotebookLM | Synthesis layer for multi-source research |
| Gemini, Genspark, Manus | Deep research; findings brought to Claude for execution |
| Aurora (OpenClaw) | Always-on agent on Netcup via Telegram and Discord |
