# Transcriber

Transcribes audio files to Markdown using [OpenAI Whisper](https://github.com/openai/whisper) — runs locally, no API key required.

## Requirements

- Python 3.9+
- [ffmpeg](https://ffmpeg.org/download.html) (must be on PATH, or pass `--ffmpeg`)

## Installation

```bash
pip install openai-whisper
```

## Usage

```bash
python transcribe.py <audio_file> [options]
```

### Examples

```bash
# Basic usage — outputs Interview Recording.md next to the input file
python transcribe.py "D:\Downloads\Interview Recording.m4a"

# Specify ffmpeg location if not on PATH
python transcribe.py "D:\Downloads\Interview Recording.m4a" --ffmpeg "C:\ffmpeg\bin\ffmpeg.exe"

# Use a more accurate model
python transcribe.py "D:\Downloads\Interview Recording.m4a" --model small

# Custom output path
python transcribe.py "D:\Downloads\Interview Recording.m4a" --output "D:\Transcripts\interview.md"
```

## Options

| Argument | Description | Default |
|----------|-------------|---------|
| `audio` | Path to the audio file | *(required)* |
| `--model` | Whisper model size (see below) | `base` |
| `--ffmpeg` | Path to ffmpeg executable | uses system PATH |
| `--output` | Output `.md` file path | same location as input |

## Models

| Model | Speed | Accuracy | Download size |
|-------|-------|----------|---------------|
| `tiny` | Fastest | Lowest | ~75 MB |
| `base` | Fast | Good | ~145 MB |
| `small` | Moderate | Better | ~465 MB |
| `medium` | Slow | Great | ~1.5 GB |
| `large` | Slower | Best | ~2.9 GB |
| `large-v2` | Slower | Better than large | ~2.9 GB |
| `large-v3` | Slowest | **Most accurate** | ~2.9 GB |

Model weights are downloaded automatically on first use and cached locally.

## Output Format

The transcript is saved as a Markdown file with timestamped segments:

```markdown
# Transcript: Interview Recording.m4a

*Generated: 2026-03-22 14:30*

---

**[0:00]** Welcome to the interview...

**[0:12]** Today we're talking about...
```
