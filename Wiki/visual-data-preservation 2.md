---
title: Visual Data Preservation
type: wiki
tags:
- ingestion
- visual
- llm
- tools
- ai-memory
created: 2026-04-20
updated: 2026-04-20
sources:
- '[[Sources/wiki-session-knowledge-ingestion-pipeline]]'
status: active
confidence: medium
permalink: ai-memory/wiki/visual-data-preservation
---

## Summary

Converting source material to Markdown discards non-textual elements. This page documents the strategy for preserving information encoded in visual content (charts, diagrams, photos, equations) when that information would otherwise be lost.

## The Problem

Two types of loss when discarding visuals:
1. **Data loss** — information encoded only in the visual (chart values, diagram relationships, infographic statistics)
2. **Utility loss** — inability to use, reconstruct, or reference the visual in future work

## Preservation Strategy by Visual Type

### Charts & Graphs (highest data-loss risk)

Recommended: combine both approaches.

- **Data extraction:** `ChartOCR` or `DePlot` (Google) → reconstructed table in MD
- **Vision LLM description:** Claude/GPT-4V → descriptive text + key values

Output format in MD:
```markdown
## Figure 3: Revenue by Region 2020–2023
**Type:** Grouped bar chart
**Key finding:** APAC overtook EMEA in Q3 2022 ($4.2B vs $3.8B)
**Data table:** [reconstructed values]
```

### Diagrams & Flowcharts

- Vision LLM → Mermaid diagram syntax
- Mermaid is text-based, renders visually in Obsidian, and is fully reconstructible
- Works well for discrete structured diagrams; approximate for complex/artistic ones

### Tables

- Already handled well by `marker` and `pandoc` → markdown tables
- No special handling needed

### Equations / Formulas

- `nougat` converts to LaTeX (text-based, renders in Obsidian)

### Photos, Illustrations, Infographics

- Vision LLM descriptive text (informational content preserved, visual form is not)
- For infographics: structured extraction prompt — list every data point, statistic, label

## Automated Visual Extraction Pipeline (Proposed)

```
marker converts PDF → MD + extracts images to /figures/
        ↓
Batch classify each image via Claude API
(chart / diagram / table / photo)
        ↓
Route to appropriate handler per type
        ↓
Insert result back into MD at correct position
```

Run on Netcup server (SAM is compute-heavy).

## Content Tiering — Where to Apply

| Content Type | Visual Treatment |
|---|---|
| High-value technical docs (research, reports with charts) | Full visual extraction |
| Books, general reading, transcripts | Text-only MD |
| Slide decks | Get source PDF if possible; extract text + speaker notes |

Apply full visual extraction selectively — it is expensive (API calls per image) and slow. Reserve it for documents where visual content carries significant information not duplicated in text.

## Video Slide Extraction

For video lectures where slides aren't available separately. Goal: extract slides as a PDF synchronized with the transcript.

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
- `PySceneDetect` or perceptual frame differencing — transition detection
- `ffmpeg` — frame extraction
- `SAM` (Meta Segment Anything) — presenter isolation
- `imagehash` (Python) — deduplication
- `img2pdf` or Pillow — PDF compilation

### Tools to Evaluate First
- `video2slides` (Python, GitHub)
- `slide-extractor` (academic)
- Descript (commercial)
- Otter.ai (captures slides from recorded meetings)

### High-Value Feature: Slide-Transcript Sync
Design the pipeline to output a combined document showing each slide alongside the portion of the transcript spoken while it was displayed. Significantly enhances future retrieval and reference value.

## Open Questions

- What types of visual information have significantly more value in near-original form?
- How should media files be stored and linked alongside text in the vault?
- How to evaluate media relevance over time as information evolves?

*(These require a dedicated design session before building the automated visual extraction pipeline.)*

## Related
- [[Wiki/format-conversion-tools]]
- [[Wiki/ingestion-pipeline]]