#!/usr/bin/env python3
"""
Convert a Whisper-generated Markdown transcript to an SRT subtitle file.

Usage:
    python md_to_srt.py <markdown_file> [--output <srt_path>] [--gap <seconds>]
"""

import argparse
import re
import sys
from pathlib import Path


TIMESTAMP_RE = re.compile(r"^\*\*\[(\d+:\d{2}(?::\d{2})?)\]\*\*\s+(.*)")


def parse_time(ts: str) -> float:
    """Convert M:SS or H:MM:SS to total seconds."""
    parts = ts.split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])


def seconds_to_srt(s: float) -> str:
    """Convert seconds to SRT timestamp HH:MM:SS,mmm."""
    ms = int((s % 1) * 1000)
    s = int(s)
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"


def convert(md_path: str, output_path: str | None, gap: float) -> None:
    md_file = Path(md_path)
    if not md_file.exists():
        print(f"Error: File not found: {md_path}")
        sys.exit(1)

    segments = []
    for line in md_file.read_text(encoding="utf-8").splitlines():
        m = TIMESTAMP_RE.match(line.strip())
        if m:
            segments.append((parse_time(m.group(1)), m.group(2).strip()))

    if not segments:
        print("No timestamped segments found in the markdown file.")
        sys.exit(1)

    srt_file = Path(output_path) if output_path else md_file.with_suffix(".srt")

    with open(srt_file, "w", encoding="utf-8") as f:
        for i, (start, text) in enumerate(segments):
            # End time = next segment's start minus a small gap, or start + 5s for the last
            if i + 1 < len(segments):
                end = max(start + 0.5, segments[i + 1][0] - gap)
            else:
                end = start + 5.0

            f.write(f"{i + 1}\n")
            f.write(f"{seconds_to_srt(start)} --> {seconds_to_srt(end)}\n")
            f.write(f"{text}\n\n")

    print(f"SRT saved to: {srt_file}")


def main():
    parser = argparse.ArgumentParser(description="Convert Whisper Markdown transcript to SRT.")
    parser.add_argument("markdown", help="Path to the .md transcript file")
    parser.add_argument("--output", help="Output .srt file path (default: same name as input)")
    parser.add_argument(
        "--gap",
        type=float,
        default=0.1,
        help="Gap in seconds between subtitle end and next subtitle start (default: 0.1)",
    )
    args = parser.parse_args()
    convert(args.markdown, args.output, args.gap)


if __name__ == "__main__":
    main()
