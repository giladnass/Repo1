---
title: Format Conversion Tools
type: wiki
tags:
- ingestion
- tools
- conversion
- ai-memory
created: 2026-04-20
updated: 2026-04-20
sources:
- '[[Sources/wiki-session-knowledge-ingestion-pipeline]]'
status: active
confidence: high
permalink: ai-memory/wiki/format-conversion-tools
---

## Summary

Tool inventory for converting source material of each format into Markdown before vault ingestion. All conversion happens pre-ingestion (Decision D-001). Run on Mac for lightweight formats; on Netcup server for compute-heavy formats (Decision D-007).

## PDFs

| Use Case | Tool | Status | Notes |
|---|---|---|---|
| **Primary (all PDFs)** | `pymupdf4llm` | Active | Fast, no ML models, no Apple Silicon GPU issues |
| Complex layouts / figures | `marker` | Suspended | Apple Silicon MPS bug (KI-005); reinstated when surya fixes it |
| Academic papers with equations | `nougat` (Meta) | Not yet evaluated | Preserves LaTeX |
| Unified visual+text | `docling` (IBM) | To evaluate | May replace both marker and pymupdf4llm |
| **Avoid** | pdftotext, PyPDF2 | -- | Mangle formatting |

**Note on Marker:** Marker was the original primary choice but crashes on Apple Silicon due to a surya MPS bug (Decision D-009, KI-005). pymupdf4llm does not handle charts and embedded figures as well but is reliable and fast for text-based PDFs, which covers the majority of use cases.

## Office Files (DOCX, PPTX, XLSX)

- **Tool:** `pandoc`
- Batch DOCX: `for f in *.docx; do pandoc "$f" -t markdown -o "${f%.docx}.md"; done`
- PPTX: loses visual layout but preserves text + speaker notes
- XLSX: convert to CSV + summary MD

## Google Workspace

- Export to Office format first, then pandoc
- Or: `gdocs2md` Python library for direct MD export

## EPUB

- `pandoc` handles perfectly: `pandoc book.epub -t markdown -o book.md`

## Audio (meetings, lectures, podcasts)

- **Tool:** `faster-whisper` (4–8× faster than base Whisper, same model quality)
- **Model:** `whisper-large-v3` for best accuracy
- Output: strip timestamps from VTT/SRT → clean MD transcript
- **Run on:** Netcup server (unattended overnight)
- **Audiobooks:** skip audio transcription if text version exists

## Video (webinars, lectures, presentations)

1. Extract audio: `ffmpeg -i video.mp4 -vn -ar 16000 -ac 1 audio.wav`
2. Transcribe with Whisper (above)
3. For visual content (slides, charts): see [[Wiki/visual-data-preservation]]

## Unified Tool to Evaluate

- **`docling`** (IBM, open-source, late 2024) — handles mixed visual/text PDFs natively including chart understanding. May supersede marker + custom visual pipeline. *Status: not yet evaluated.*

## Storage Estimates Post-Conversion

| Format | Compression Ratio | Example |
|---|---|---|
| Text-heavy PDF → MD | ~2–10% of original | 5 MB PDF → 100–300 KB MD |
| Image-heavy PDF → MD | <1% | Discards visual data |
| DOCX → MD | ~5–20% | 2 MB DOCX → 50–200 KB MD |
| EPUB → MD | ~15–30% | 3 MB EPUB → 500 KB–1 MB MD |
| Audio → transcript MD | ~0.1–0.5% | 100 MB audio → ~100 KB MD |
| Video → transcript MD | ~0.01% | 1 GB video → ~100 KB MD |

Even a terabyte of source material produces a text library well under 10 GB. **Processing time is the bottleneck, not storage.**

## Scripts

- `Scripts/ingest.py` -- batch and single-file converter (PDF via pymupdf4llm, others via pandoc)
- `Scripts/watch.sh` -- fswatch watcher that triggers ingest.py on new files

## Processing Location

| Format | Location | Why |
|---|---|---|
| PDF/Office/EPUB | Mac | Fast, low compute |
| Audio/video | Netcup server | Compute-heavy, unattended |

See Decision D-007 in [[000-Meta/decisions]].

## Related
- [[Wiki/ingestion-pipeline]]
- [[Wiki/visual-data-preservation]]