#!/usr/bin/env python3
"""
lint.py -- Vault validation per CLAUDE.md LINT protocol and D-003 schema.

Usage:
    python3 Scripts/lint.py [--vault /path/to/vault] [--strict] [--json]

Checks:
    1. Required frontmatter fields (D-003)
    2. Controlled vocabulary (type, status, confidence, source-type)
    3. Date format (YYYY-MM-DD) for created/updated/ingested
    4. File naming convention (lowercase-kebab-case.md)
    5. Broken wikilinks
    6. Orphan wiki pages (not linked from anywhere)
    7. Stale updated timestamps on wiki pages (>90 days)
    8. Em dash violations (house rule: no em dashes)

Exit codes:
    0 - Clean or warnings only
    1 - Errors found
"""

import argparse
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Constants from D-003 and D-005
# ---------------------------------------------------------------------------

VALID_TYPES = {
    "wiki", "source", "decision", "session-log",
    "weekly-review", "working-context", "template", "note",
}

VALID_STATUS_WIKI = {"active", "needs-review", "archived", "draft"}
VALID_STATUS_SOURCE = {"raw", "processed", "archived"}
VALID_CONFIDENCE = {"high", "medium", "low", "speculative"}
VALID_SOURCE_TYPES = {"pdf", "docx", "epub", "audio", "video", "url", "conversation", "note"}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WIKILINK_RE = re.compile(r"\[\[([^\[\]|]+?)(?:\|[^\[\]]+?)?\]\]")
# Kebab-case filename: lowercase letters, digits, hyphens (plus date prefix variant)
KEBAB_RE = re.compile(r"^(?:\d{4}-\d{2}-\d{2}-?)?[a-z0-9][a-z0-9\-]*\.md$")

STALE_DAYS = 90

SCAN_DIRS = {"Wiki", "Sources", "Memory", "Working-Context", "000-Meta"}
EXCLUDE_FILES = {"CLAUDE.md"}
# Sources/ filenames are auto-generated from original PDF/doc names and are immutable per D-002
SKIP_NAMING_DIRS = {"Sources"}
# Intentional exceptions to the lowercase-kebab naming rule
NAMING_EXCEPTIONS = {"MEMORY.md"}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body). Returns ({}, text) if no frontmatter."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_raw = text[3:end].strip()
    body = text[end + 4:]
    try:
        fm = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError:
        fm = None
    return fm, body


def resolve_wikilink(link: str, vault_root: Path) -> Path | None:
    """Return the resolved Path for a [[wikilink]] if it exists, else None."""
    link = link.strip()
    # May include subfolder: "Wiki/foo" or just "foo"
    candidates = [
        vault_root / (link + ".md"),
        vault_root / link,
    ]
    # Also search all scan dirs
    for d in SCAN_DIRS:
        stem = Path(link).name
        candidates.append(vault_root / d / (stem + ".md"))
        candidates.append(vault_root / d / link)
    for c in candidates:
        if c.exists():
            return c
    return None


def is_valid_date(s: object) -> bool:
    if not isinstance(s, str):
        # yaml may parse dates as date objects
        return isinstance(s, date)
    return bool(DATE_RE.match(s))


def to_date(s: object) -> date | None:
    if isinstance(s, date):
        return s
    if isinstance(s, str):
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


# ---------------------------------------------------------------------------
# Issue collector
# ---------------------------------------------------------------------------

class Issue:
    def __init__(self, level: str, path: str, check: str, message: str):
        self.level = level   # "error" | "warning"
        self.path = path
        self.check = check
        self.message = message

    def __str__(self):
        icon = "[E]" if self.level == "error" else "[W]"
        return f"{icon} {self.path}: [{self.check}] {self.message}"


# ---------------------------------------------------------------------------
# Per-file checks
# ---------------------------------------------------------------------------

def check_file(path: Path, vault_root: Path, issues: list[Issue]) -> dict | None:
    """Run all per-file checks. Returns frontmatter dict for link-graph phase."""
    rel = str(path.relative_to(vault_root))

    if path.name in EXCLUDE_FILES:
        return None

    # --- File naming (D-005) ---
    in_skip_dir = any(part in SKIP_NAMING_DIRS for part in path.parts)
    if not in_skip_dir and path.name not in NAMING_EXCEPTIONS and not KEBAB_RE.match(path.name):
        issues.append(Issue("warning", rel, "naming",
                             f"filename '{path.name}' not lowercase-kebab-case.md"))

    text = path.read_text(encoding="utf-8", errors="replace")

    # --- Frontmatter parseable ---
    fm, body = parse_frontmatter(text)
    if fm is None:
        issues.append(Issue("error", rel, "frontmatter", "YAML frontmatter is invalid/unparseable"))
        return None
    if not fm:
        issues.append(Issue("warning", rel, "frontmatter", "no YAML frontmatter block found"))
        return {}

    file_type = fm.get("type", "")

    # --- Required universal fields (D-003) ---
    for field in ("title", "type", "tags", "created"):
        if field not in fm:
            issues.append(Issue("error", rel, "frontmatter", f"missing required field '{field}'"))

    # --- type vocabulary ---
    if file_type and file_type not in VALID_TYPES:
        issues.append(Issue("error", rel, "vocab",
                             f"invalid type '{file_type}'; must be one of {sorted(VALID_TYPES)}"))

    # --- Date fields ---
    for field in ("created", "updated", "ingested"):
        if field in fm and not is_valid_date(fm[field]):
            issues.append(Issue("error", rel, "dates",
                                 f"field '{field}' value '{fm[field]}' is not ISO date (YYYY-MM-DD)"))

    # --- tags: must be a list ---
    tags = fm.get("tags")
    if tags is not None and not isinstance(tags, list):
        issues.append(Issue("error", rel, "frontmatter", "field 'tags' must be a YAML list"))

    # --- Type-specific required fields ---
    if file_type == "wiki":
        for field in ("updated", "sources", "status", "confidence"):
            if field not in fm:
                issues.append(Issue("error", rel, "frontmatter",
                                     f"wiki page missing required field '{field}'"))
        status = fm.get("status", "")
        if status and status not in VALID_STATUS_WIKI:
            issues.append(Issue("error", rel, "vocab",
                                 f"invalid status '{status}'; wiki status must be one of {sorted(VALID_STATUS_WIKI)}"))
        conf = fm.get("confidence", "")
        if conf and conf not in VALID_CONFIDENCE:
            issues.append(Issue("error", rel, "vocab",
                                 f"invalid confidence '{conf}'; must be one of {sorted(VALID_CONFIDENCE)}"))
        # Stale updated check
        updated_val = fm.get("updated")
        if updated_val:
            d = to_date(updated_val)
            if d:
                age = (date.today() - d).days
                if age > STALE_DAYS:
                    issues.append(Issue("warning", rel, "stale",
                                         f"'updated' is {age} days old (>{STALE_DAYS})"))

    elif file_type == "source":
        for field in ("source-type", "ingested", "status", "origin", "processed-to"):
            if field not in fm:
                issues.append(Issue("warning", rel, "frontmatter",
                                     f"source note missing recommended field '{field}'"))
        st = fm.get("source-type", "")
        if st and st not in VALID_SOURCE_TYPES:
            issues.append(Issue("error", rel, "vocab",
                                 f"invalid source-type '{st}'; must be one of {sorted(VALID_SOURCE_TYPES)}"))
        status = fm.get("status", "")
        if status and status not in VALID_STATUS_SOURCE:
            issues.append(Issue("error", rel, "vocab",
                                 f"invalid status '{status}'; source status must be one of {sorted(VALID_STATUS_SOURCE)}"))

    # --- Em dash check (house rule) ---
    if "—" in text:  # —
        count = text.count("—")
        issues.append(Issue("warning", rel, "em-dash",
                             f"contains {count} em dash(es) -- replace with hyphen"))

    return fm


# ---------------------------------------------------------------------------
# Cross-file checks (link graph)
# ---------------------------------------------------------------------------

def check_links(
    file_data: dict[Path, dict],
    vault_root: Path,
    issues: list[Issue],
):
    """Check broken wikilinks and orphan wiki pages."""

    # Build map: all existing files by stem and by relative path
    existing: set[str] = set()
    for p in file_data:
        existing.add(p.stem.lower())
        rel = str(p.relative_to(vault_root))
        existing.add(rel.lower().replace(".md", "").replace("\\", "/"))

    # Track which wiki pages are referenced
    wiki_files = {p for p in file_data if p.parent.name == "Wiki"}
    referenced: set[Path] = set()

    for path, fm in file_data.items():
        if fm is None:
            continue
        rel = str(path.relative_to(vault_root))
        text = path.read_text(encoding="utf-8", errors="replace")
        links = WIKILINK_RE.findall(text)

        for link in links:
            # Resolve and track
            resolved = resolve_wikilink(link, vault_root)
            if resolved is None:
                issues.append(Issue("warning", rel, "broken-link",
                                     f"wikilink [[{link}]] -- no matching file found"))
            else:
                if resolved in wiki_files:
                    referenced.add(resolved)

    # Orphan wiki pages: wiki pages not referenced by any other file
    # (Index page itself is allowed to be unreferenced)
    orphans = wiki_files - referenced
    for p in sorted(orphans):
        rel = str(p.relative_to(vault_root))
        issues.append(Issue("warning", rel, "orphan",
                             "wiki page not linked from any other file"))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Vault LINT validator")
    parser.add_argument("--vault", default=None,
                        help="Path to vault root (default: parent of Scripts/)")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors (exit 1 if any warnings)")
    parser.add_argument("--json", action="store_true", dest="json_out",
                        help="Output results as JSON")
    args = parser.parse_args()

    # Resolve vault root
    if args.vault:
        vault_root = Path(args.vault).resolve()
    else:
        vault_root = Path(__file__).resolve().parent.parent

    if not vault_root.is_dir():
        print(f"ERROR: vault root not found: {vault_root}", file=sys.stderr)
        sys.exit(1)

    # Collect markdown files
    md_files: list[Path] = []
    for scan_dir in SCAN_DIRS:
        d = vault_root / scan_dir
        if d.is_dir():
            md_files.extend(d.rglob("*.md"))

    if not md_files:
        print(f"No markdown files found under {vault_root}")
        sys.exit(0)

    issues: list[Issue] = []
    file_data: dict[Path, dict] = {}

    # Per-file checks
    for path in sorted(md_files):
        fm = check_file(path, vault_root, issues)
        file_data[path] = fm

    # Cross-file checks
    check_links(file_data, vault_root, issues)

    # Output
    errors = [i for i in issues if i.level == "error"]
    warnings = [i for i in issues if i.level == "warning"]

    if args.json_out:
        out = {
            "vault": str(vault_root),
            "files_checked": len(md_files),
            "errors": [{"path": i.path, "check": i.check, "message": i.message} for i in errors],
            "warnings": [{"path": i.path, "check": i.check, "message": i.message} for i in warnings],
        }
        print(json.dumps(out, indent=2))
    else:
        print(f"Vault LINT -- {vault_root}")
        print(f"Files checked: {len(md_files)}")
        print()
        if not issues:
            print("Clean -- no issues found.")
        else:
            if errors:
                print(f"ERRORS ({len(errors)}):")
                for i in errors:
                    print(f"  {i}")
                print()
            if warnings:
                print(f"Warnings ({len(warnings)}):")
                for i in warnings:
                    print(f"  {i}")
                print()
            print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s)")

    has_errors = bool(errors) or (args.strict and bool(warnings))
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
