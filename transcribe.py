#!/usr/bin/env python3
"""
Transcribe an audio file using OpenAI Whisper (local, free via pip).

Usage:
    python transcribe.py <audio_file> [--ffmpeg <ffmpeg_path>] [--model <base|large-v3>] [--output <output_path>]

    python transcribe.py "D:\Downloads\interview-2.m4a" --output D:\interview-2.txt --model base

Install dependencies:
    pip install openai-whisper
    pip install ffmpeg-python  # optional, only needed if ffmpeg isn't on PATH
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime


def transcribe(audio_path: str, ffmpeg_path: str | None, model_name: str, output_path: str | None) -> None:
    try:
        import whisper
    except ImportError:
        print("Error: openai-whisper is not installed.")
        print("Run: pip install openai-whisper")
        sys.exit(1)

    audio_file = Path(audio_path)
    if not audio_file.exists():
        print(f"Error: File not found: {audio_path}")
        sys.exit(1)

    # Point whisper at a custom ffmpeg binary if provided
    if ffmpeg_path:
        os.environ["PATH"] = str(Path(ffmpeg_path).parent) + os.pathsep + os.environ.get("PATH", "")

    print(f"Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)

    print(f"Transcribing: {audio_file.name}")
    result = model.transcribe(str(audio_file), verbose=False)

    # Build output path
    if output_path:
        md_file = Path(output_path)
    else:
        md_file = audio_file.with_suffix(".md")

    # Write markdown
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(f"# Transcript: {audio_file.name}\n\n")
        f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
        f.write("---\n\n")

        # Write with timestamps if segments are available
        segments = result.get("segments", [])
        if segments:
            for seg in segments:
                start = format_time(seg["start"])
                text = seg["text"].strip()
                f.write(f"**[{start}]** {text}\n\n")
        else:
            f.write(result["text"].strip())
            f.write("\n")

    print(f"Transcript saved to: {md_file}")


def format_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h:
        return f"{h}:{m:02}:{s:02}"
    return f"{m}:{s:02}"


def main():
    parser = argparse.ArgumentParser(description="Transcribe an audio file to Markdown using Whisper.")
    parser.add_argument("audio", help="Path to the audio file (e.g. recording.m4a)")
    parser.add_argument("--ffmpeg", help="Path to ffmpeg executable (if not on system PATH)")
    parser.add_argument(
        "--model",
        default="base",
        help="Whisper model size (default: base). Options: tiny, base, small, medium, large, large-v2, large-v3. Larger = more accurate.",
    )
    parser.add_argument("--output", help="Output markdown file path (default: same name as input with .md extension)")
    args = parser.parse_args()

    transcribe(args.audio, args.ffmpeg, args.model, args.output)


if __name__ == "__main__":
    main()
