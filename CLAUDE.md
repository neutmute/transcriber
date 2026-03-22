# CLAUDE.md

## Project Overview

Two standalone Python scripts for transcribing audio files and converting transcripts to subtitles.

- `transcribe.py` — transcribes an audio file to a timestamped Markdown file using local Whisper
- `md_to_srt.py` — converts that Markdown transcript to an SRT subtitle file for use in VLC

## Dependencies

```
pip install openai-whisper
```

ffmpeg must be on PATH or passed via `--ffmpeg`.

## Usage

```bash
python transcribe.py "recording.m4a" --model large-v3
python md_to_srt.py "recording.md"
```

## Output Format

`transcribe.py` produces Markdown with segments in the format:

```
**[M:SS]** Transcribed text here.
```

`md_to_srt.py` parses that format — do not change it without updating the regex in `md_to_srt.py`.
