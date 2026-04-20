#!/usr/bin/env python3
"""
AI-Memory audio/video transcription script (runs on Netcup).

Transcribes audio and video files to clean Markdown using faster-whisper.
Video files have audio extracted via ffmpeg before transcription.

Output structure:
    <output_dir>/<stem>/<stem>.md

Usage:
    python transcribe.py                    # batch: process all files in SOURCE_DIR
    python transcribe.py --file audio.mp3   # single file
    python transcribe.py --model medium     # faster, lower quality
    python transcribe.py --source DIR --output DIR

Requirements:
    pip install faster-whisper
    sudo apt install ffmpeg
"""

import argparse
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

SOURCE_DIR = Path.home() / "AI-Ingestion/01-source"
OUTPUT_DIR = Path.home() / "AI-Ingestion/02-converted"

AUDIO_FORMATS = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".aac", ".wma", ".opus"}
VIDEO_FORMATS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v"}
ALL_FORMATS = AUDIO_FORMATS | VIDEO_FORMATS

DEFAULT_MODEL = "large-v3"
CPU_THREADS = 8    # matches OLLAMA_NUM_THREADS; leaves headroom when Ollama is idle
NUM_WORKERS = 2    # parallel files; 2 x 8 threads fills 12 vCPUs when Ollama is idle


def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def extract_audio(video_path: Path, tmp_dir: Path) -> Path:
    wav_path = tmp_dir / f"{video_path.stem}.wav"
    log(f"  extracting audio from {video_path.name}")
    result = subprocess.run(
        [
            "ffmpeg", "-i", str(video_path),
            "-vn", "-ar", "16000", "-ac", "1",
            str(wav_path), "-y", "-loglevel", "error",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg: {result.stderr.strip()}")
    return wav_path


def transcribe_audio(audio_path: Path, model_name: str) -> tuple[str, str]:
    """Returns (transcript_text, detected_language)."""
    from faster_whisper import WhisperModel

    log(f"  loading model: {model_name} (downloads on first use -- large-v3 is ~3 GB)")
    model = WhisperModel(
        model_name,
        device="cpu",
        compute_type="int8",
        cpu_threads=CPU_THREADS,
        num_workers=NUM_WORKERS,
    )

    log("  transcribing...")
    segments, info = model.transcribe(str(audio_path), beam_size=5)

    log(f"  language: {info.language} ({info.language_probability:.0%})")

    lines = [seg.text.strip() for seg in segments if seg.text.strip()]
    return " ".join(lines), info.language


def process_file(src: Path, output_root: Path, model_name: str, skip_existing: bool = True) -> str:
    if src.suffix.lower() not in ALL_FORMATS:
        return "skipped"

    out_dir = output_root / src.stem
    out_md = out_dir / f"{src.stem}.md"

    if skip_existing and out_md.exists():
        log(f"skip  {src.name}")
        return "skipped"

    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        with tempfile.TemporaryDirectory() as tmp:
            if src.suffix.lower() in VIDEO_FORMATS:
                log(f"video {src.name}")
                audio_path = extract_audio(src, Path(tmp))
            else:
                log(f"audio {src.name}")
                audio_path = src

            transcript, lang = transcribe_audio(audio_path, model_name)

        md = (
            f"# Transcript: {src.stem}\n\n"
            f"**Source:** {src.name}  \n"
            f"**Transcribed:** {datetime.now().strftime('%Y-%m-%d')}  \n"
            f"**Language:** {lang}  \n"
            f"**Model:** {model_name}\n\n"
            f"---\n\n"
            f"{transcript}\n"
        )
        out_md.write_text(md, encoding="utf-8")
        log(f"  -> {out_md}")
        return "converted"

    except Exception as exc:
        log(f"ERROR {src.name}: {exc}")
        return "error"


def process_batch(source_dir: Path, output_root: Path, model_name: str):
    files = sorted(
        f for f in source_dir.iterdir()
        if f.is_file() and f.suffix.lower() in ALL_FORMATS
    )

    if not files:
        log(f"No audio/video files found in {source_dir}")
        return

    log(f"Found {len(files)} file(s)  |  model: {model_name}")
    counts = {"converted": 0, "skipped": 0, "error": 0}

    for f in files:
        counts[process_file(f, output_root, model_name)] += 1

    log(
        f"Done -- {counts['converted']} converted, "
        f"{counts['skipped']} skipped, {counts['error']} errors"
    )


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio/video to Markdown")
    parser.add_argument("--source", type=Path, default=SOURCE_DIR)
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--file", type=Path, help="Process a single file")
    parser.add_argument(
        "--model", default=DEFAULT_MODEL,
        choices=["tiny", "base", "small", "medium", "large-v2", "large-v3"],
        help="Whisper model (default: large-v3; use medium for faster CPU processing)",
    )
    parser.add_argument("--no-skip", action="store_true", help="Re-transcribe existing files")
    args = parser.parse_args()

    skip = not args.no_skip

    if args.file:
        if not args.file.exists():
            log(f"File not found: {args.file}")
            sys.exit(1)
        sys.exit(0 if process_file(args.file, args.output, args.model, skip) != "error" else 1)
    else:
        if not args.source.exists():
            log(f"Source directory not found: {args.source}")
            sys.exit(1)
        process_batch(args.source, args.output, args.model)


if __name__ == "__main__":
    main()
