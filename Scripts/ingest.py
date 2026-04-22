#!/usr/bin/env python3
"""
AI-Memory ingestion converter.

Converts PDF, DOCX, EPUB, PPTX, and other document formats to Markdown,
placing output in a per-file subdirectory under the output root.

Output structure:
    <output_dir>/<stem>/<stem>.md

Usage:
    python ingest.py                         # batch: process all files in SOURCE_DIR
    python ingest.py --file path/to/file.pdf # single file
    python ingest.py --source DIR --output DIR

Requirements:
    pip install pymupdf4llm
    brew install pandoc  (or: pip install pandoc)
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Default directories -- override with --source and --output flags
SOURCE_DIR = Path.home() / "AI-Ingestion/01-source"
OUTPUT_DIR = Path.home() / "AI-Ingestion/02-converted"

PANDOC_FORMATS = {".docx", ".epub", ".pptx", ".odt", ".rtf", ".html"}
PDF_FORMAT = {".pdf"}
ALL_FORMATS = PDF_FORMAT | PANDOC_FORMATS


def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def convert_pdf(src: Path, out_dir: Path) -> Path:
    try:
        import pymupdf4llm
    except ImportError:
        raise RuntimeError("pymupdf4llm not installed -- run: pip install pymupdf4llm")

    out = out_dir / f"{src.stem}.md"
    md = pymupdf4llm.to_markdown(str(src))
    out.write_bytes(md.encode())
    return out


def convert_pandoc(src: Path, out_dir: Path) -> Path:
    out = out_dir / f"{src.stem}.md"
    result = subprocess.run(
        ["pandoc", str(src), "-t", "markdown", "--wrap=none", "-o", str(out)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return out


def process_file(src: Path, output_root: Path, skip_existing: bool = True, done_dir: Path | None = None) -> str:
    """
    Returns "converted", "skipped", or "error".
    If done_dir is set, successfully converted source files are moved there.
    """
    if src.suffix.lower() not in ALL_FORMATS:
        return "skipped"

    out_dir = output_root / src.stem
    out_md = out_dir / f"{src.stem}.md"

    if skip_existing and out_md.exists():
        log(f"skip  {src.name}")
        return "skipped"

    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        if src.suffix.lower() == ".pdf":
            log(f"pdf   {src.name}")
            convert_pdf(src, out_dir)
        else:
            log(f"doc   {src.name}  [{src.suffix}]")
            convert_pandoc(src, out_dir)
        log(f"  -> {out_md}")
        if done_dir is not None:
            done_dir.mkdir(parents=True, exist_ok=True)
            dest = done_dir / src.name
            src.rename(dest)
            log(f"  -> moved original to {dest}")
        return "converted"
    except Exception as exc:
        log(f"ERROR {src.name}: {exc}")
        return "error"


def process_batch(source_dir: Path, output_root: Path, done_dir: Path | None = None):
    files = sorted(
        f for f in source_dir.iterdir()
        if f.is_file() and f.suffix.lower() in ALL_FORMATS
    )

    if not files:
        log(f"No supported files found in {source_dir}")
        return

    log(f"Found {len(files)} file(s) in {source_dir}")
    counts = {"converted": 0, "skipped": 0, "error": 0}

    for f in files:
        result = process_file(f, output_root, done_dir=done_dir)
        counts[result] += 1

    log(
        f"Done -- {counts['converted']} converted, "
        f"{counts['skipped']} skipped, {counts['error']} errors"
    )


def main():
    parser = argparse.ArgumentParser(description="Convert documents to Markdown for AI-Memory ingestion")
    parser.add_argument("--source", type=Path, default=SOURCE_DIR, help="Source directory (batch mode)")
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR, help="Output root directory")
    parser.add_argument("--file", type=Path, help="Process a single file (skips batch mode)")
    parser.add_argument("--no-skip", action="store_true", help="Reconvert even if output already exists")
    parser.add_argument("--move-done", type=Path, metavar="DIR",
                        help="Move source file to DIR after successful conversion (e.g. ~/AI-Ingestion/03-done)")
    args = parser.parse_args()

    skip = not args.no_skip
    done_dir = args.move_done.expanduser() if args.move_done else None

    if args.file:
        if not args.file.exists():
            log(f"File not found: {args.file}")
            sys.exit(1)
        result = process_file(args.file, args.output, skip_existing=skip, done_dir=done_dir)
        sys.exit(0 if result != "error" else 1)
    else:
        if not args.source.exists():
            log(f"Source directory not found: {args.source}")
            sys.exit(1)
        process_batch(args.source, args.output, done_dir=done_dir)


if __name__ == "__main__":
    main()
