#!/usr/bin/env python3
"""
AI-Memory session-end script.

Reads session notes (stdin or --notes file), calls an LLM to structure them
into vault updates, writes the results, then commits and pushes.

Updates written:
    000-Meta/handoff.md  -- new entry prepended
    000-Meta/log.md      -- new entry appended
    000-Meta/MEMORY.md   -- body replaced with current state

Usage:
    # Pipe notes via stdin:
    echo "Completed X. Next: Y." | python3 session_end.py

    # From a file:
    python3 session_end.py --notes /tmp/session-notes.md

    # Dry run -- print output but do not write or commit:
    python3 session_end.py --notes /tmp/notes.md --dry-run

    # Skip git commit (write files but do not commit):
    python3 session_end.py --notes /tmp/notes.md --no-commit

Requirements:
    pip install litellm
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import litellm

litellm.telemetry = False

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
DEFAULT_MODEL       = "openai/glm-5:cloud"       # quality -- Ollama Cloud
DEFAULT_OLLAMA_HOST = "https://ollama.com/v1"    # Ollama Cloud endpoint (local: http://localhost:11434)
DEFAULT_BRANCH      = "claude/caveman-lite-vrjM3"
VAULT_DIR           = Path("/Users/giladnass/Library/Mobile Documents/iCloud~md~obsidian/Documents/AI-Memory")

TODAY = datetime.now().strftime("%Y-%m-%d")
# ---------------------------------------------------------------------------


def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def strip_thinking(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def extract_json(text: str) -> str:
    start = min(
        (text.find(c) for c in ["{", "["] if text.find(c) != -1),
        default=-1,
    )
    if start == -1:
        return text
    end = max(text.rfind("}"), text.rfind("]"))
    return text[start : end + 1] if end != -1 else text


def split_frontmatter(text: str) -> tuple[str, str]:
    """Split a markdown file into (frontmatter_block, body). frontmatter_block includes the --- delimiters."""
    if not text.startswith("---"):
        return ("", text)
    end = text.find("\n---", 3)
    if end == -1:
        return ("", text)
    split = end + 4  # past the closing ---
    return (text[:split], text[split:].lstrip("\n"))


def read_vault_file(vault: Path, rel_path: str) -> str:
    p = vault / rel_path
    return p.read_text(encoding="utf-8") if p.exists() else ""


def first_section(text: str) -> str:
    """Return the first ## section of a markdown body (for format reference)."""
    lines = text.splitlines()
    in_section = False
    section_lines: list[str] = []
    for line in lines:
        if line.startswith("## "):
            if in_section:
                break
            in_section = True
        if in_section:
            section_lines.append(line)
    return "\n".join(section_lines)


def structure_session(
    notes: str,
    memory_text: str,
    handoff_text: str,
    tool: str,
    model: str,
    ollama_host: str,
) -> dict:
    """Call LLM to produce structured vault updates from raw session notes."""
    _, memory_body = split_frontmatter(memory_text)
    _, handoff_body = split_frontmatter(handoff_text)
    handoff_example = first_section(handoff_body)

    system = """You are a knowledge base curator for an AI memory system. Given session notes and current vault state, produce structured vault updates.

Return a JSON object with these fields:
- "session_title" (string): short session title, 3-6 words, no em dashes
- "log_entry" (string): a full ## section for the session log. Format:
    ## YYYY-MM-DD -- <title>\\n\\n**Tool:** <tool>\\n**Branch:** claude/caveman-lite-vrjM3\\n\\n### Accomplished\\n- item\\n\\n### Key Findings\\n- item\\n\\n### Pending\\n- item
- "handoff_entry" (string): a full ## section for the handoff file. Format:
    ## YYYY-MM-DD -- <title>\\n\\n### What Was Accomplished\\n...\\n\\n### What to Do Next\\n...\\n\\n### What to Read First Next Session\\nPer CLAUDE.md session start protocol:\\n1. `000-Meta/MEMORY.md`\\n2. `000-Meta/index.md`\\n3. `000-Meta/handoff.md`\\n4. `Working-Context/knowledge-base-build-plan.md`
- "memory_body" (string): the full updated body of MEMORY.md (no frontmatter, no --- delimiters). Update the Current System State, What the Next Session Should Do, and any other sections that changed. Preserve unchanged sections exactly. No em dashes anywhere.

Return ONLY valid JSON. No markdown fences, no explanation."""

    user = f"""Today: {TODAY}
Tool: {tool}

== CURRENT MEMORY.MD ==
{memory_body}

== MOST RECENT HANDOFF ENTRY (format reference) ==
{handoff_example}

== SESSION NOTES ==
{notes}"""

    kwargs: dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": 4096,
    }
    if model.startswith("ollama/") or model.startswith("openai/"):
        kwargs["api_base"] = ollama_host
    if model.startswith("openai/"):
        kwargs["api_key"] = os.environ.get("OLLAMA_API_KEY") or os.environ.get("OPENAI_API_KEY", "")

    log(f"  calling {model}...")
    response = litellm.completion(**kwargs)
    raw = extract_json(strip_thinking(response.choices[0].message.content or ""))

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        log(f"  JSON parse failed. Raw (first 400 chars): {raw[:400]}")
        sys.exit(1)


def write_handoff(vault: Path, entry: str, dry_run: bool):
    path = vault / "000-Meta/handoff.md"
    text = read_vault_file(vault, "000-Meta/handoff.md")
    frontmatter, body = split_frontmatter(text)
    new_text = frontmatter + "\n\n" + entry.strip() + "\n\n---\n\n" + body.strip() + "\n"
    if dry_run:
        print("\n=== handoff.md (prepended entry) ===")
        print(entry.strip())
    else:
        path.write_text(new_text, encoding="utf-8")
        log(f"  -> {path}")


def write_log(vault: Path, entry: str, dry_run: bool):
    path = vault / "000-Meta/log.md"
    text = read_vault_file(vault, "000-Meta/log.md")
    new_text = text.rstrip("\n") + "\n\n---\n\n" + entry.strip() + "\n"
    if dry_run:
        print("\n=== log.md (appended entry) ===")
        print(entry.strip())
    else:
        path.write_text(new_text, encoding="utf-8")
        log(f"  -> {path}")


def write_memory(vault: Path, body: str, dry_run: bool):
    path = vault / "000-Meta/MEMORY.md"
    text = read_vault_file(vault, "000-Meta/MEMORY.md")
    frontmatter, _ = split_frontmatter(text)
    new_text = frontmatter + "\n\n" + body.strip() + "\n"
    if dry_run:
        print("\n=== MEMORY.md (updated body) ===")
        print(body.strip()[:800] + ("..." if len(body) > 800 else ""))
    else:
        path.write_text(new_text, encoding="utf-8")
        log(f"  -> {path}")


def git_commit_push(vault: Path, branch: str, title: str):
    def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, cwd=vault, capture_output=True, text=True, check=check)

    status = run(["git", "status", "--porcelain"], check=False)
    if not status.stdout.strip():
        log("  git: nothing to commit")
        return

    run(["git", "add", "-A"])
    msg = f"Session end: {TODAY} -- {title}\n\nhttps://claude.ai/code/session_01BYu7gWaCCQjnyoJi6Gq2BK"
    result = run(["git", "commit", "-m", msg], check=False)
    if result.returncode != 0:
        log(f"  git commit failed: {result.stderr.strip()}")
        return
    log(f"  git commit: {result.stdout.strip().splitlines()[0]}")

    push = run(["git", "push", "-u", "origin", branch], check=False)
    if push.returncode != 0:
        log(f"  git push failed: {push.stderr.strip()}")
    else:
        log("  git push: ok")


def main():
    parser = argparse.ArgumentParser(description="Structure session notes and update AI-Memory vault")
    parser.add_argument("--notes", type=Path, help="Session notes file (default: read from stdin)")
    parser.add_argument("--vault", type=Path, default=VAULT_DIR, help="Vault root path")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"LLM model (default: {DEFAULT_MODEL})")
    parser.add_argument("--ollama-host", default=DEFAULT_OLLAMA_HOST, help="Ollama API base URL")
    parser.add_argument("--branch", default=DEFAULT_BRANCH, help=f"Git branch (default: {DEFAULT_BRANCH})")
    parser.add_argument("--tool", default="Claude Code", help="Tool name for log entry (default: Claude Code)")
    parser.add_argument("--dry-run", action="store_true", help="Print output but do not write files or commit")
    parser.add_argument("--no-commit", action="store_true", help="Write files but skip git commit/push")
    args = parser.parse_args()

    if args.notes:
        if not args.notes.exists():
            log(f"Notes file not found: {args.notes}")
            sys.exit(1)
        notes = args.notes.read_text(encoding="utf-8")
    else:
        if sys.stdin.isatty():
            print("Enter session notes (Ctrl+D when done):")
        notes = sys.stdin.read()

    if not notes.strip():
        log("No session notes provided.")
        sys.exit(1)

    memory_text  = read_vault_file(args.vault, "000-Meta/MEMORY.md")
    handoff_text = read_vault_file(args.vault, "000-Meta/handoff.md")

    log("Structuring session notes...")
    result = structure_session(notes, memory_text, handoff_text, args.tool, args.model, args.ollama_host)

    title         = result.get("session_title", "Session")
    log_entry     = result.get("log_entry", "")
    handoff_entry = result.get("handoff_entry", "")
    memory_body   = result.get("memory_body", "")

    if not all([log_entry, handoff_entry, memory_body]):
        log("LLM returned incomplete output. Check the raw response above.")
        sys.exit(1)

    log(f"Title: {title}")
    write_handoff(args.vault, handoff_entry, args.dry_run)
    write_log(args.vault, log_entry, args.dry_run)
    write_memory(args.vault, memory_body, args.dry_run)

    if not args.dry_run and not args.no_commit:
        log("Committing...")
        git_commit_push(args.vault, args.branch, title)

    log("Done.")


if __name__ == "__main__":
    main()
