#!/usr/bin/env python3
"""
AI-Memory linkding export pipeline.

Fetches bookmarks from linkding, downloads Singlefile HTML captures,
converts to Markdown, and writes to the AI-Ingestion converted directory
ready for process.py.

For each bookmark with a Singlefile HTML asset:
    1. Download HTML from linkding API
    2. Convert to Markdown via pandoc
    3. Write to ~/AI-Ingestion/02-converted/<slug>/<slug>.md

Then run:
    python3 Scripts/process.py --source-type url

Usage:
    python3 Scripts/linkding_export.py               # all bookmarks with snapshots
    python3 Scripts/linkding_export.py --limit 50    # first 50 (test run)
    python3 Scripts/linkding_export.py --tag ai      # bookmarks tagged 'ai'
    python3 Scripts/linkding_export.py --unread      # unread only

Run from: Mac (writes to ~/AI-Ingestion/02-converted on Mac).
Linkding is on Netcup at a public IP -- accessible from Mac directly.
For large batches, run from Netcup with --linkding-url http://localhost:9090
and rsync output to Mac afterward.

Requirements:
    pip install requests
    brew install pandoc  (already installed)
    export LINKDING_API_TOKEN=<token from linkding Settings > Integrations>
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import requests

LINKDING_URL = "http://152.53.244.42:9090"
OUTPUT_DIR   = Path.home() / "AI-Ingestion/02-converted"
PAGE_SIZE    = 100


def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def make_slug(title: str, bookmark_id: int) -> str:
    """Generate a unique, filesystem-safe slug from title + bookmark ID."""
    if title:
        cleaned = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        cleaned = cleaned[:60].rstrip("-")
    else:
        cleaned = ""
    suffix = f"bm{bookmark_id}"
    return f"{cleaned}-{suffix}" if cleaned else suffix


def fetch_bookmarks(base_url: str, token: str, tag: str, unread: bool) -> list[dict]:
    """Fetch all bookmarks from linkding, handling pagination."""
    headers = {"Authorization": f"Token {token}"}
    params: dict = {"limit": PAGE_SIZE, "offset": 0}
    if tag:
        params["q"] = f"#{tag}"
    if unread:
        params["unread"] = "yes"

    bookmarks = []
    while True:
        resp = requests.get(
            f"{base_url}/api/bookmarks/",
            headers=headers, params=params, timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        bookmarks.extend(data["results"])
        log(f"  fetched {len(bookmarks)} / {data['count']}")
        if not data["next"]:
            break
        params["offset"] += PAGE_SIZE
    return bookmarks


def get_html_asset(base_url: str, token: str, bookmark_id: int) -> tuple[int, str] | None:
    """Return (asset_id, display_name) for the first complete HTML asset, or None."""
    headers = {"Authorization": f"Token {token}"}
    resp = requests.get(
        f"{base_url}/api/bookmarks/{bookmark_id}/assets/",
        headers=headers, timeout=30,
    )
    if resp.status_code != 200:
        return None
    data = resp.json()
    assets = data.get("results", data) if isinstance(data, dict) else data
    for asset in assets:
        ct = asset.get("content_type", "")
        if "html" in ct.lower() and asset.get("status") == "complete":
            return asset["id"], asset.get("display_name", "snapshot.html")
    return None


def download_asset(base_url: str, token: str, bookmark_id: int, asset_id: int) -> bytes:
    headers = {"Authorization": f"Token {token}"}
    resp = requests.get(
        f"{base_url}/api/bookmarks/{bookmark_id}/assets/{asset_id}/",
        headers=headers, timeout=60,
    )
    resp.raise_for_status()
    return resp.content


def html_to_markdown(html_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
        f.write(html_bytes)
        tmp_path = Path(f.name)
    try:
        result = subprocess.run(
            ["pandoc", str(tmp_path), "-f", "html", "-t", "markdown", "--wrap=none"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
        return result.stdout
    finally:
        tmp_path.unlink(missing_ok=True)


def build_markdown(md_body: str, bookmark: dict) -> str:
    """Prepend a metadata header to the converted Markdown body."""
    title = bookmark.get("title") or bookmark.get("url", "")
    url = bookmark.get("url", "")
    tags = ", ".join(bookmark.get("tag_names", []))
    date_added = (bookmark.get("date_added") or "")[:10]
    description = bookmark.get("description", "")
    notes = bookmark.get("notes", "")

    lines = [f"# {title}", "", f"**URL:** {url}  ", f"**Saved:** {date_added}  "]
    if tags:
        lines.append(f"**Tags:** {tags}  ")
    if description:
        lines += ["", description]
    if notes:
        lines += ["", f"**Notes:** {notes}"]
    lines += ["", "---", ""]

    return "\n".join(lines) + "\n" + md_body


def process_bookmark(
    bookmark: dict,
    base_url: str,
    token: str,
    out_root: Path,
    skip_existing: bool,
) -> str:
    bm_id = bookmark["id"]
    slug = make_slug(bookmark.get("title") or "", bm_id)
    out_file = out_root / slug / f"{slug}.md"

    if skip_existing and out_file.exists():
        return "skipped"

    asset = get_html_asset(base_url, token, bm_id)
    if not asset:
        return "no-snapshot"

    asset_id, _ = asset
    try:
        html_bytes = download_asset(base_url, token, bm_id, asset_id)
        md = build_markdown(html_to_markdown(html_bytes), bookmark)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(md, encoding="utf-8")
        log(f"  -> {slug}")
        return "converted"
    except Exception as exc:
        log(f"  ERROR bm{bm_id} ({bookmark.get('url', '')}): {exc}")
        return "error"


def main():
    parser = argparse.ArgumentParser(description="Export linkding bookmarks to Markdown")
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR,
                        help="Output directory (default: ~/AI-Ingestion/02-converted)")
    parser.add_argument("--limit", type=int, default=0,
                        help="Max bookmarks to process, 0 = all (default: 0)")
    parser.add_argument("--tag", default="",
                        help="Filter by tag")
    parser.add_argument("--unread", action="store_true",
                        help="Only unread bookmarks")
    parser.add_argument("--no-skip", action="store_true",
                        help="Reprocess already-converted bookmarks")
    parser.add_argument("--linkding-url", default=LINKDING_URL,
                        help=f"Linkding base URL (default: {LINKDING_URL})")
    args = parser.parse_args()

    token = os.environ.get("LINKDING_API_TOKEN")
    if not token:
        log("ERROR: LINKDING_API_TOKEN environment variable not set")
        sys.exit(1)

    skip = not args.no_skip
    args.output.mkdir(parents=True, exist_ok=True)

    log(f"Fetching bookmarks from {args.linkding_url}...")
    bookmarks = fetch_bookmarks(args.linkding_url, token, args.tag, args.unread)

    if args.limit:
        bookmarks = bookmarks[: args.limit]

    log(f"Processing {len(bookmarks)} bookmarks")
    counts = {"converted": 0, "skipped": 0, "no-snapshot": 0, "error": 0}

    for bm in bookmarks:
        result = process_bookmark(bm, args.linkding_url, token, args.output, skip)
        counts[result] += 1

    log(
        f"Done -- {counts['converted']} converted, {counts['skipped']} skipped, "
        f"{counts['no-snapshot']} no snapshot, {counts['error']} errors"
    )
    if counts["converted"] > 0:
        log("Next: python3 Scripts/process.py --source-type url")


if __name__ == "__main__":
    main()
