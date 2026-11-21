#!/usr/bin/env python3
"""Export verified cue data as basic UTF-8 SubRip or WebVTT."""
import argparse
import json
import sys
from html import escape
from pathlib import Path


def timestamp(ms, separator):
    seconds, fraction = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}{separator}{fraction:03}"


def render(cues, fmt):
    if fmt not in {"srt", "vtt"}:
        raise ValueError("format must be srt or vtt")
    if not isinstance(cues, list) or not cues:
        raise ValueError("expected a nonempty JSON array of cues")
    blocks = ["WEBVTT"] if fmt == "vtt" else []
    separator = "." if fmt == "vtt" else ","
    previous_start = 0
    for number, cue in enumerate(cues, start=1):
        if not isinstance(cue, dict):
            raise ValueError(f"cue {number}: expected an object")
        start, end, text = (cue.get(key) for key in ("start_ms", "end_ms", "text"))
        if type(start) is not int or type(end) is not int:
            raise ValueError(f"cue {number}: start_ms and end_ms must be integers")
        if start < previous_start or end <= start:
            raise ValueError(f"cue {number}: timestamps must be in order with positive duration")
        if not isinstance(text, str) or not text.strip() or "\x00" in text:
            raise ValueError(f"cue {number}: expected plain cue text")
        lines = text.strip().splitlines()
        if any(not line.strip() for line in lines):
            raise ValueError(f"cue {number}: a blank line would end the cue")
        content = "\n".join(lines)
        if fmt == "vtt":
            content = escape(content, quote=False)
        interval = f"{timestamp(start, separator)} --> {timestamp(end, separator)}"
        prefix = f"{number}\n" if fmt == "srt" else ""
        blocks.append(f"{prefix}{interval}\n{content}")
        previous_start = start
    return "\n\n".join(blocks) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--format", choices=["srt", "vtt"], required=True)
    args = parser.parse_args()
    try:
        cues = json.loads(args.input.read_text(encoding="utf-8-sig"))
        track = render(cues, args.format)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"{parser.prog}: {exc}\n")
    sys.stdout.buffer.write(track.encode("utf-8"))


if __name__ == "__main__":
    main()
