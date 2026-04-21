#!/usr/bin/env python3
"""
AI-Memory LLM processing layer.

Takes converted Markdown files (output from ingest.py or transcribe.py) and
generates structured source notes using Claude.

Pipeline per file:
    1. triage model  -- extract tags, routing decision, infer title
    2. summary model -- 2-5 sentence summary, key findings, questions raised
    3. summary model -- cross-reference: find related wiki pages, suggest wikilinks

Output:
    Sources/<stem>.md  -- source note with D-003 frontmatter
    Wiki/<slug>.md     -- stub pages (full-routing only, skipped if page exists)

Routing:
    full    -- high information density, novel content -> source note + wiki stub
    summary -- useful but redundant with existing wiki -> source note only
    index   -- low value, reference material -> entry in Sources/_index.md only

--- Model config (change these to switch providers or models) ---

    DEFAULT_TRIAGE_MODEL   = "ollama/qwen3:30b-a3b"
    DEFAULT_SUMMARY_MODEL  = "ollama/qwen3:32b"

LiteLLM model string format:
    Ollama local     ollama/<name>:<tag>         e.g. ollama/qwen3:32b
    OpenRouter       openrouter/<org>/<model>    e.g. openrouter/google/gemini-2.0-flash-001
    Anthropic        claude-<model>              e.g. claude-sonnet-4-6

Provider API keys (only needed for the provider you are using):
    Ollama           no key required
    OpenRouter       export OPENROUTER_API_KEY=...
    Anthropic        export ANTHROPIC_API_KEY=...

Usage:
    python process.py                                       # batch all files in 02-converted/
    python process.py --file path/to/stem.md               # single file
    python process.py --source-type audio                  # override source-type (default: pdf)
    python process.py --vault /path/to/vault               # override vault path
    python process.py --triage-model ollama/llama4:scout   # override triage model
    python process.py --summary-model ollama/qwen3:32b     # override summary model
    python process.py --ollama-host http://localhost:11434  # override Ollama host

Requirements:
    pip install litellm
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import litellm

litellm.telemetry = False  # opt out of LiteLLM usage stats

# ---------------------------------------------------------------------------
# Model config -- edit these two lines to switch providers or models
# ---------------------------------------------------------------------------
DEFAULT_TRIAGE_MODEL  = "openai/qwen3.5:cloud"  # fast, classification -- Ollama Cloud
DEFAULT_SUMMARY_MODEL = "openai/glm-5:cloud"     # quality, summarization -- Ollama Cloud
DEFAULT_OLLAMA_HOST   = "https://ollama.com/v1"  # Ollama Cloud endpoint (local: http://localhost:11434)
# ---------------------------------------------------------------------------

CONVERTED_DIR = Path.home() / "AI-Ingestion/02-converted"
VAULT_DIR = Path("/Users/giladnass/Library/Mobile Documents/iCloud~md~obsidian/Documents/AI-Memory")

MAX_CONTENT_CHARS = 60_000  # ~15K tokens

TODAY = datetime.now().strftime("%Y-%m-%d")


def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def llm_call(model: str, system: str, user: str, max_tokens: int, ollama_host: str) -> str:
    """Single LiteLLM call. Handles provider routing via model string prefix.

    Prefixes:
        ollama/   -- local Ollama (api_base = ollama_host, no key)
        openai/   -- OpenAI-compatible endpoint (api_base = ollama_host, key from OLLAMA_API_KEY)
        bare name -- Anthropic, routed by LiteLLM automatically
    """
    kwargs: dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": max_tokens,
    }
    if model.startswith("ollama/") or model.startswith("openai/"):
        kwargs["api_base"] = ollama_host
    if model.startswith("openai/"):
        kwargs["api_key"] = os.environ.get("OLLAMA_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
    response = litellm.completion(**kwargs)
    return response.choices[0].message.content or ""


def strip_thinking(text: str) -> str:
    """Remove <think>...</think> blocks emitted by reasoning models (Qwen3, DeepSeek-R1, etc.)."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def extract_json(text: str) -> str:
    """Pull the first JSON object or array out of a string."""
    start = min(
        (text.find(c) for c in ["{", "["] if text.find(c) != -1),
        default=-1,
    )
    if start == -1:
        return text
    end = max(text.rfind("}"), text.rfind("]"))
    return text[start : end + 1] if end != -1 else text


def truncate(content: str) -> str:
    if len(content) <= MAX_CONTENT_CHARS:
        return content
    return content[:MAX_CONTENT_CHARS] + "\n\n[... content truncated for processing ...]"


def load_wiki_pages(vault: Path) -> list[dict]:
    """Return [{slug, title}] for all non-meta wiki pages."""
    wiki_dir = vault / "Wiki"
    if not wiki_dir.exists():
        return []
    pages = []
    for md in sorted(wiki_dir.glob("*.md")):
        if md.stem.startswith("_"):
            continue
        slug = md.stem
        title = slug
        try:
            text = md.read_text(encoding="utf-8")
            m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', text, re.MULTILINE)
            if m:
                title = m.group(1).strip().strip('"').strip("'")
        except Exception:
            pass
        pages.append({"slug": slug, "title": title})
    return pages


def wiki_list_text(pages: list[dict]) -> str:
    if not pages:
        return "(no existing wiki pages)"
    return "\n".join(f"- [[Wiki/{p['slug']}]] -- {p['title']}" for p in pages)


def triage(content: str, stem: str, model: str, ollama_host: str) -> dict:
    """Step 1: extract tags, routing decision, infer title."""
    system = (
        "You are a knowledge base curator. Analyze the document and return a JSON object with:\n"
        '- "title" (string): clear, concise title for this document (3-8 words)\n'
        '- "tags" (array of strings): 3-8 lowercase-kebab topic tags, no namespace prefixes\n'
        '- "routing" (string): one of "full", "summary", or "index"\n'
        '  "full" = high information density, novel content worth expanding into wiki pages\n'
        '  "summary" = useful content but largely covered by existing knowledge\n'
        '  "index" = low value, reference or boilerplate material only\n\n'
        "Return ONLY valid JSON. No markdown fences, no explanation."
    )
    raw = extract_json(strip_thinking(llm_call(model, system, f"Filename: {stem}\n\n{truncate(content)}", 2048, ollama_host)))
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        log(f"  triage JSON parse failed -- using defaults. Raw: {raw[:200]}")
        result = {}
    return {
        "title": result.get("title", stem.replace("-", " ").title()),
        "tags": result.get("tags", []),
        "routing": result.get("routing", "summary") if result.get("routing") in ("full", "summary", "index") else "summary",
    }


def summarize(content: str, model: str, ollama_host: str) -> dict:
    """Step 2: summary, key findings, questions raised."""
    system = (
        "You are a knowledge base curator. Analyze the document and return a JSON object with:\n"
        '- "summary" (string): 2-5 sentences capturing the document\'s main content and value\n'
        '- "key_findings" (array of strings): 3-6 key takeaways or findings\n'
        '- "questions_raised" (array of strings): 1-4 open questions or gaps the document surfaces\n\n'
        "Return ONLY valid JSON. No markdown fences, no explanation."
    )
    raw = extract_json(strip_thinking(llm_call(model, system, truncate(content), 2048, ollama_host)))
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        log(f"  summarize JSON parse failed. Raw: {raw[:200]}")
        result = {}
    return {
        "summary": result.get("summary", ""),
        "key_findings": result.get("key_findings", []),
        "questions_raised": result.get("questions_raised", []),
    }


def cross_reference(content: str, wiki_pages: list[dict], model: str, ollama_host: str) -> list[dict]:
    """Step 3: find related existing wiki pages."""
    if not wiki_pages:
        return []
    system = (
        "You are a knowledge base curator. Given a document and a list of existing wiki pages, "
        "identify which pages are meaningfully related to the document.\n\n"
        f"Existing wiki pages:\n{wiki_list_text(wiki_pages)}\n\n"
        'Return a JSON array of objects, each with:\n'
        '- "slug" (string): the wiki page slug, e.g. "ingestion-pipeline"\n'
        '- "reason" (string): one sentence explaining the relationship\n\n'
        "Return [] if nothing is relevant. Return ONLY valid JSON. No markdown fences, no explanation."
    )
    raw = extract_json(strip_thinking(llm_call(model, system, truncate(content), 1024, ollama_host)))
    try:
        result = json.loads(raw)
        return [r for r in result if isinstance(r, dict) and "slug" in r and "reason" in r]
    except json.JSONDecodeError:
        log(f"  cross-ref JSON parse failed. Raw: {raw[:200]}")
        return []


def slug_from_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def build_source_note(
    stem: str,
    source_type: str,
    triage_result: dict,
    summary_result: dict,
    refs: list[dict],
    routing: str,
) -> str:
    title = triage_result["title"]
    tags = triage_result["tags"]
    all_tags = tags + [f"source-type/{source_type}", "status/processed"]
    tags_yaml = "[" + ", ".join(all_tags) + "]"
    processed_to_items = ", ".join(f'"[[Wiki/{r["slug"]}]]"' for r in refs)
    processed_to = f"[{processed_to_items}]"

    lines = [
        "---",
        f'title: "{title}"',
        "type: source",
        f"source-type: {source_type}",
        f"tags: {tags_yaml}",
        f"created: {TODAY}",
        f"ingested: {TODAY}",
        "status: processed",
        f"origin: {stem}",
        f"routing: {routing}",
        f"processed-to: {processed_to}",
        "---",
        "",
        f"# {title}",
        "",
    ]

    if summary_result["summary"]:
        lines += ["## Summary", "", summary_result["summary"], ""]

    if summary_result["key_findings"]:
        lines += ["## Key Findings", ""]
        lines += [f"- {finding}" for finding in summary_result["key_findings"]]
        lines.append("")

    if summary_result["questions_raised"]:
        lines += ["## Questions Raised", ""]
        lines += [f"- {q}" for q in summary_result["questions_raised"]]
        lines.append("")

    if refs:
        lines += ["## Related Wiki Pages", ""]
        lines += [f"- [[Wiki/{r['slug']}]] -- {r['reason']}" for r in refs]
        lines.append("")

    return "\n".join(lines)


def build_wiki_stub(stem: str, title: str, tags: list[str], summary: str) -> str:
    tags_yaml = "[" + ", ".join(tags[:4]) + "]"
    return "\n".join([
        "---",
        f'title: "{title}"',
        "type: wiki",
        f"tags: {tags_yaml}",
        f"created: {TODAY}",
        f"updated: {TODAY}",
        f'sources: ["[[Sources/{stem}]]"]',
        "status: draft",
        "confidence: low",
        "---",
        "",
        f"# {title}",
        "",
        f"> Stub created from [[Sources/{stem}]]. Expand manually.",
        "",
        summary,
        "",
    ])


def write_index_entry(sources_dir: Path, stem: str, title: str, tags: list[str]):
    index_file = sources_dir / "_index.md"
    tags_str = ", ".join(tags)
    entry = f"- [[Sources/{stem}]] -- {title} -- {tags_str} -- {TODAY}\n"
    if not index_file.exists():
        index_file.write_text(f"# Sources Index\n\n{entry}", encoding="utf-8")
    else:
        with index_file.open("a", encoding="utf-8") as f:
            f.write(entry)


def process_file(
    md_file: Path,
    vault: Path,
    source_type: str,
    triage_model: str,
    summary_model: str,
    ollama_host: str,
    wiki_pages: list[dict],
    skip_existing: bool = True,
) -> str:
    stem = md_file.stem
    sources_dir = vault / "Sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    out_note = sources_dir / f"{stem}.md"

    if skip_existing and out_note.exists():
        log(f"skip  {stem}")
        return "skipped"

    log(f"process {stem}")

    try:
        content = md_file.read_text(encoding="utf-8")
    except Exception as exc:
        log(f"ERROR reading {md_file}: {exc}")
        return "error"

    try:
        log(f"  1/3 triage ({triage_model})...")
        triage_result = triage(content, stem, triage_model, ollama_host)
        routing = triage_result["routing"]
        log(f"  routing={routing}  tags={triage_result['tags']}")

        if routing == "index":
            write_index_entry(sources_dir, stem, triage_result["title"], triage_result["tags"])
            log("  -> indexed in Sources/_index.md")
            return "indexed"

        log(f"  2/3 summarize ({summary_model})...")
        summary_result = summarize(content, summary_model, ollama_host)

        refs = []
        if routing == "full":
            log(f"  3/3 cross-reference ({summary_model})...")
            refs = cross_reference(content, wiki_pages, summary_model, ollama_host)
            log(f"  related pages: {[r['slug'] for r in refs]}")

        note_text = build_source_note(stem, source_type, triage_result, summary_result, refs, routing)
        out_note.write_text(note_text, encoding="utf-8")
        log(f"  -> {out_note}")

        if routing == "full":
            wiki_dir = vault / "Wiki"
            wiki_dir.mkdir(parents=True, exist_ok=True)
            title = triage_result["title"]
            wiki_slug = slug_from_title(title)
            stub_path = wiki_dir / f"{wiki_slug}.md"
            if not stub_path.exists():
                stub = build_wiki_stub(stem, title, triage_result["tags"], summary_result["summary"])
                stub_path.write_text(stub, encoding="utf-8")
                log(f"  -> wiki stub: {stub_path.name}")
            else:
                log(f"  -> wiki stub skipped (already exists): {stub_path.name}")

    except Exception as exc:
        log(f"ERROR {stem}: {exc}")
        return "error"

    return "processed"


def process_batch(
    converted_dir: Path,
    vault: Path,
    source_type: str,
    triage_model: str,
    summary_model: str,
    ollama_host: str,
):
    wiki_pages = load_wiki_pages(vault)
    log(f"Wiki pages loaded: {len(wiki_pages)}")

    md_files = sorted(
        stem_dir / f"{stem_dir.name}.md"
        for stem_dir in converted_dir.iterdir()
        if stem_dir.is_dir() and (stem_dir / f"{stem_dir.name}.md").exists()
    )

    if not md_files:
        log(f"No converted files found in {converted_dir}")
        return

    log(f"Found {len(md_files)} file(s)")
    counts = {"processed": 0, "indexed": 0, "skipped": 0, "error": 0}

    for md_file in md_files:
        result = process_file(
            md_file, vault, source_type,
            triage_model, summary_model, ollama_host,
            wiki_pages,
        )
        counts[result] += 1

    log(
        f"Done -- {counts['processed']} processed, {counts['indexed']} indexed, "
        f"{counts['skipped']} skipped, {counts['error']} errors"
    )


def main():
    parser = argparse.ArgumentParser(description="LLM processing layer for AI-Memory ingestion")
    parser.add_argument("--source", type=Path, default=CONVERTED_DIR,
                        help="Directory with converted MD files (batch mode)")
    parser.add_argument("--file", type=Path, help="Process a single converted MD file")
    parser.add_argument(
        "--source-type", default="pdf",
        choices=["pdf", "docx", "epub", "audio", "video", "url", "conversation", "note"],
        help="Source type for frontmatter (default: pdf)",
    )
    parser.add_argument("--vault", type=Path, default=VAULT_DIR,
                        help="Path to AI-Memory vault root")
    parser.add_argument("--triage-model", default=DEFAULT_TRIAGE_MODEL,
                        help=f"Model for triage step (default: {DEFAULT_TRIAGE_MODEL})")
    parser.add_argument("--summary-model", default=DEFAULT_SUMMARY_MODEL,
                        help=f"Model for summarize + cross-ref steps (default: {DEFAULT_SUMMARY_MODEL})")
    parser.add_argument("--ollama-host", default=DEFAULT_OLLAMA_HOST,
                        help=f"Ollama API base URL (default: {DEFAULT_OLLAMA_HOST})")
    parser.add_argument("--no-skip", action="store_true",
                        help="Reprocess files that already have source notes")
    args = parser.parse_args()

    skip = not args.no_skip

    if args.file:
        if not args.file.exists():
            log(f"File not found: {args.file}")
            sys.exit(1)
        wiki_pages = load_wiki_pages(args.vault)
        result = process_file(
            args.file, args.vault, args.source_type,
            args.triage_model, args.summary_model, args.ollama_host,
            wiki_pages, skip,
        )
        sys.exit(0 if result != "error" else 1)
    else:
        if not args.source.exists():
            log(f"Converted directory not found: {args.source}")
            sys.exit(1)
        process_batch(
            args.source, args.vault, args.source_type,
            args.triage_model, args.summary_model, args.ollama_host,
        )


if __name__ == "__main__":
    main()
