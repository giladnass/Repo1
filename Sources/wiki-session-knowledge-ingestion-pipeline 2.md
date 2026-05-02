---
title: wiki-session-knowledge-ingestion-pipeline
type: source
source-type: conversation
tags: [ingestion, pipeline, conversion, tools]
created: 2026-04-12
ingested: 2026-04-12
status: processed
origin: Claude.ai brainstorming session 2026-04-12
processed-to: ["[[Wiki/ingestion-pipeline]]", "[[Wiki/format-conversion-tools]]", "[[Wiki/visual-data-preservation]]"]
permalink: ai-memory/sources/wiki-session-knowledge-ingestion-pipeline
---

# Knowledge Ingestion Pipeline — Research & Decisions
**Session date:** 2026-04-12  
**Source:** Claude.ai brainstorming session  
**Status:** Draft — awaiting vault ingestion  
**Tags:** #ingestion #pipeline #tools #visual-data #video #knowledge-base #open-questions

---

## Context

This page documents research and decisions made during a session focused on designing the content ingestion pipeline for the AI Memory System. The session covered format conversion strategy, visual data preservation, video slide extraction, and the automation gap in the current setup.

Related: [[AI Memory System — To-Do List]], [[Tools Inventory]]

---

## Core Decision: Convert to MD First

**Decision:** Pre-convert all source files to Markdown before ingestion. Do not feed raw binary formats into the pipeline.

**Rationale:**
- basic-memory and most vector/wiki systems are optimized for plain text
- Conversion quality is inspectable and correctable before ingestion
- MD files are portable, Git-versionable, and human-readable
- Processing speed is dramatically faster on pre-converted text

---

## Format Conversion — Tools & Approach

### PDFs
| Use Case | Tool | Notes |
|---|---|---|
| General / complex layouts | `marker` | ML-based, handles tables and figures well |
| Simple PDFs | `pymupdf4llm` | Fast, good quality |
| Academic papers with equations | `nougat` (Meta) | Preserves LaTeX |
| **Avoid** | pdftotext, PyPDF2 | Mangle formatting |

### Office Files (DOCX, PPTX, XLSX)
- **Tool:** `pandoc`
- Batch: `for f in *.docx; do pandoc "$f" -t markdown -o "${f%.docx}.md"; done`
- PPTX: loses visual layout but preserves text + speaker notes
- XLSX: convert to CSV + summary MD

### Google Workspace
- Export to Office format first, then pandoc
- Or: `gdocs2md` Python library for direct MD export

### EPUB
- `pandoc` handles perfectly: `pandoc book.epub -t markdown -o book.md`

### Audio (meetings, lectures, podcasts)
- **Tool:** `faster-whisper` (4-8x faster than base Whisper, same model quality)
- Model: `whisper-large-v3` for best accuracy
- Output: strip timestamps from VTT/SRT → clean MD transcript
- **Audiobooks:** skip audio if text version exists

### Video (webinars, lectures, presentations)
- Extract audio first: `ffmpeg -i video.mp4 -vn -ar 16000 -ac 1 audio.wav`
- Then transcribe with Whisper
- Visual content handling: see [[Video Slide Extraction]] below

### New Tool to Evaluate
- **`docling`** (IBM, open-source, late 2024) — handles mixed visual/text PDFs natively including chart understanding. May supersede marker+custom pipeline.

---

## Storage Estimates (Post-Conversion)

| Format | Compression Ratio | Example |
|---|---|---|
| Text-heavy PDF → MD | ~2–10% of original | 5MB PDF → 100–300KB MD |
| Image-heavy PDF → MD | <1% | Discards all visual data |
| DOCX → MD | ~5–20% | 2MB DOCX → 50–200KB MD |
| EPUB → MD | ~15–30% | 3MB EPUB → 500KB–1MB MD |
| Audio → transcript MD | ~0.1–0.5% | 100MB audio → ~100KB MD |
| Video → transcript MD | ~0.01% | 1GB video → ~100KB MD |

**Bottom line:** Even a terabyte of source material produces a text library well under 10GB. Storage is not the bottleneck. Processing time (especially audio/video) is.

---

## Visual Data Preservation

### The Problem
Converting to MD discards non-textual elements. This causes two losses:
1. **Data loss** — information encoded only in the visual (chart values, diagram relationships)
2. **Utility loss** — inability to use, reconstruct, or reference the visual in future work

### Preservation Strategies by Visual Type

#### Charts & Graphs (highest risk)
Recommended: combine both approaches
- **Data extraction:** `ChartOCR` or `DePlot` (Google) → structured table in MD
- **Vision LLM description:** feed image to Claude/GPT-4V → descriptive text + key values

Output format in MD:
```markdown
## Figure 3: Revenue by Region 2020–2023
**Type:** Grouped bar chart  
**Key finding:** APAC overtook EMEA in Q3 2022 ($4.2B vs $3.8B)  
**Data table:** [reconstructed values]
```

#### Diagrams & Flowcharts
- Vision LLM → Mermaid diagram syntax
- Mermaid is text-based, renders visually in Obsidian, and is fully reconstructible
- Works well for discrete structured diagrams; approximate for complex/artistic ones

#### Tables
- Already handled well by `marker` and `pandoc` → markdown tables
- No special handling needed

#### Equations / Formulas
- `nougat` converts to LaTeX (text-based, renders in Obsidian)

#### Photos, Illustrations, Infographics
- Vision LLM descriptive text (informational content preserved, not visual form)
- For infographics: structured extraction prompt — list every data point, statistic, label

### Automated Visual Extraction Pipeline (Proposed)
1. `marker` converts PDF → MD + extracts images to `/figures/`
2. Batch script classifies each image via Claude API (chart / diagram / table / photo)
3. Routes to appropriate handler based on type
4. Inserts result back into MD at correct position

### Content Tiering (Practical Approach)
- **Full visual extraction:** high-value technical documents (research, reports with charts)
- **Text-only MD:** books, general reading, transcripts
- **Slide decks:** get source PDF if possible; extract text + speaker notes

> ⚠️ **Open Discussion Flagged:** A broader framework is needed for deciding which visual types have significantly more value in near-original form, how to store/link media alongside text, and how to evaluate media relevance over time as information evolves. This needs a dedicated brainstorming session. See [[Open Questions]] below.

---

## Video Slide Extraction

### Use Case
Video lectures where the presenter shows slides not available separately. Goal: extract slides as a PDF (and optionally a per-slide summary MD), synchronized with the transcript.

### Pipeline

```
Input video
    ↓
ffmpeg → extract frame every 2 seconds
    ↓
Perceptual hash deduplication → keep unique frames
    ↓
Vision LLM classifier → "does this frame contain a slide?"
    ↓ (yes)
SAM or Vision LLM → bounding box of slide region → crop
    ↓
Quality filter → remove blurry/transitioning frames
    ↓
img2pdf → extracted_slides.pdf
    ↓
Optional: Claude API → title + summary per slide → MD
Optional: Sync slide timestamps with transcript
```

### Layout Handling
| Layout | Approach |
|---|---|
| Screen share / pip overlay | OpenCV crop — remove corner box |
| Presenter beside projected screen | SAM segmentation or Vision LLM bounding box |
| Full-screen slides only | No processing needed — just deduplicate |

### Key Tools
- `PySceneDetect` or perceptual frame differencing for transition detection
- `ffmpeg` for frame extraction
- `SAM` (Meta Segment Anything) for presenter isolation
- `imagehash` (Python) for deduplication
- `img2pdf` or Pillow for PDF compilation

### Existing Tools to Evaluate First
- `video2slides` (Python, GitHub)
- `slide-extractor` (academic origin)
- Descript (commercial)
- Otter.ai (captures slides from recorded meetings)

### High-Value Feature: Slide-Transcript Sync
Design the pipeline to output a combined document showing each slide alongside the portion of the transcript spoken while it was displayed. Significantly enhances future retrieval and reference value.

**Run on:** Netcup server (SAM is compute-heavy; batch overnight)

---

## Processing Location Strategy

| Content Type | Where to Process | Why |
|---|---|---|
| PDF/Office/EPUB conversion | Mac | Fast, low compute |
| Audio/video transcription | Netcup server | Compute-heavy, unattended overnight |
| Visual extraction pipeline | Netcup server | SAM requires GPU/CPU headroom |
| URL scraping | Netcup server | Long-running, network-bound |

---

## URL / Bookmark Backlog

**Priority: Low (but infrastructure worth setting up now)**

Estimated scale: thousands of URLs, possibly much more.

### Proposed Pipeline

| Stage | Tool | Purpose |
|---|---|---|
| Scrape & archive | ArchiveBox (self-hosted) or Firecrawl API | Full page content capture |
| Auto-categorize & triage | Claude API batch calls | Topic, tags, ingest-worthiness, summary |
| Ingest worthy content | Convert approved pages to MD → vault | Full ingestion |
| Index the rest | Title + summary + URL + tags in MD index | Searchable without noise |

### Tools to Evaluate
- **`linkding`** — self-hosted bookmark manager, tagging, full-text search
- **`Omnivore`** — open-source read-later + highlight + MD export
- **`Raindrop.io`** — managed option, bulk import/export, AI tagging

**Action:** Set up linkding now as a capture point, even before processing the backlog.

---

## Automation Gap — Current State vs. Vision

### The Gap
The current setup (Obsidian + basic-memory + Git) is a **manually-fed filing system with good retrieval**. The vision — automatic ingestion, living knowledge base — requires an automation layer that does not yet exist.

### What's Automatable Today
| Content Type | Automatable? | Mechanism |
|---|---|---|
| Files dropped into watched folder | ✅ | `fswatch` + conversion script |
| Google Drive new files | ✅ | Drive API + webhook |
| Audio/video batch | ✅ | Scheduled Whisper jobs |
| Web browsing/research | ✅ | Omnivore/ArchiveBox auto-import |
| Claude.ai conversations | ⚠️ Partial | No official export API |
| Manual insights/decisions | ❌ | Always needs human trigger |

### The Claude Conversation Problem
Claude.ai has **no official API for exporting conversations**. This means sessions like this one cannot be auto-ingested without workarounds:
- Browser extension capture (fragile)
- Manual export + formatting script
- **Use Claude Code for knowledge-building sessions** — has full filesystem access, can auto-save outputs

### Required Build Work
1. Ingestion pipelines per content type (conversion scripts)
2. Watchers/triggers for new content
3. Claude conversation capture solution
4. Routing logic (full ingest vs. summary vs. index only)

**Estimated effort:** 2–4 weeks of focused setup

---

## Prioritized Action Plan (from this session)

1. ✅ Install `marker`, `pandoc`, `faster-whisper` on Mac + Netcup
2. ✅ Batch-convert PDFs, Office, EPUBs → MD; spot-check quality
3. ✅ Set up Whisper on Netcup; queue audio/video batch overnight
4. ✅ Set up `linkding` as bookmark capture point
5. ⬜ Design ingestion automation layer (watchers, triggers, routing)
6. ⬜ Design URL pipeline (ArchiveBox/Firecrawl + Claude API triage)
7. ⬜ Evaluate `docling` as unified document conversion tool
8. ⬜ Try `video2slides` on sample lecture video
9. ⬜ Build slide-transcript sync prototype

---

## Open Questions

- [ ] **Visual data preservation framework** — What types of visual information have significantly more value in near-original form? How should media be stored/linked alongside text? How to evaluate media relevance over time? *(flagged for dedicated brainstorming session)*
- [ ] **Claude conversation capture** — What's the best long-term solution? Claude Code workflow? Browser extension? Manual cadence?
- [ ] **Ingestion automation architecture** — What triggers what? How granular should routing logic be?
- [ ] **docling evaluation** — Does it replace marker + custom visual pipeline, or complement it?

---

## References & Links
- [marker](https://github.com/VikParuchuri/marker)
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- [docling](https://github.com/DS4SD/docling)
- [DePlot](https://github.com/google-research/google-research/tree/master/deplot)
- [SAM](https://github.com/facebookresearch/segment-anything)
- [video2slides](https://github.com/excitedleigh/video2slides)
- [ArchiveBox](https://archivebox.io/)
- [Firecrawl](https://firecrawl.dev/)
- [linkding](https://github.com/sissbruecker/linkding)
- [Omnivore](https://omnivore.app/)