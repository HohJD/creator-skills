#!/usr/bin/env python3
"""Check an SRT, WebVTT or cue-JSON track for timing and readability problems, offline."""
import argparse
import json
import re
import sys
from pathlib import Path

NETFLIX = "Netflix Timed Text Style Guide (General Requirements; English (USA)), read 2026-11-28"
RULES = {
    "SUB001": ("error", "unreadable-cue", "A cue whose timing line can't be read. Players skip it or reject the file."),
    "SUB002": ("error", "no-duration", "A cue that ends at or before it starts never appears on screen."),
    "SUB003": ("error", "out-of-order", "Cue starts must not go backwards; many players drop or reorder such cues."),
    "SUB004": ("error", "empty-cue", "A cue with no text, which shows an empty box or nothing at all."),
    "SUB005": ("warning", "overlap", "A cue that starts before the previous one ends. Legitimate for simultaneous "
               "speakers; otherwise two captions fight for the screen."),
    "SUB101": ("warning", "line-too-long", f"A line over the character limit (default 42). Source: {NETFLIX}."),
    "SUB102": ("warning", "too-many-lines", f"A cue over the line limit (default 2). Source: {NETFLIX}."),
    "SUB103": ("warning", "too-short", f"A cue shown for less than the minimum (default 833 ms, five-sixths of a "
               f"second). Source: {NETFLIX}."),
    "SUB104": ("warning", "too-long-on-screen", f"A cue shown for longer than the maximum (default 7 s). "
               f"Source: {NETFLIX}."),
    "SUB105": ("warning", "reading-speed", f"More characters per second than viewers can read (default 20 for "
               f"adult programmes, 17 for children's). Source: {NETFLIX}. Other languages have their own guides."),
}
DEFAULTS = {"max_chars": 42, "max_lines": 2, "min_ms": 833, "max_ms": 7000, "max_cps": 20.0}

TIME = r"(?:(\d+):)?(\d{2}):(\d{2})[,.](\d{3})"
TIMING = re.compile(rf"^\s*{TIME}\s*-->\s*{TIME}(?:\s+.*)?$")
TAG = re.compile(r"</?[a-zA-Z][^>]*>|\{\\[^}]*\}")


def _ms(h, m, s, f):
    return ((int(h or 0) * 60 + int(m)) * 60 + int(s)) * 1000 + int(f)


def parse(text, fmt=None):
    """Cues as dicts with start_ms, end_ms, text and the 1-based line of the timing line (None if unreadable)."""
    text = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    if fmt == "json" or (fmt is None and text.lstrip().startswith("[")):
        return [{"start_ms": c.get("start_ms"), "end_ms": c.get("end_ms"), "text": c.get("text") or "",
                 "line": None, "index": i} for i, c in enumerate(json.loads(text), start=1)]
    cues, lines, i = [], text.split("\n"), 0
    while i < len(lines):
        if not lines[i].strip() or lines[i].startswith(("WEBVTT", "NOTE", "STYLE", "REGION")):
            i = _skip_block(lines, i) if lines[i].startswith(("NOTE", "STYLE", "REGION")) else i + 1
            continue
        block_start = i
        while i < len(lines) and lines[i].strip():
            i += 1
        block = lines[block_start:i]
        at = next((k for k, line in enumerate(block) if "-->" in line), None)
        if at is None:
            if not (len(block) == 1 and block[0].strip().isdigit()):
                cues.append({"start_ms": None, "end_ms": None, "text": "\n".join(block), "line": block_start + 1})
            continue
        m = TIMING.match(block[at])
        start, end = (_ms(*m.groups()[:4]), _ms(*m.groups()[4:])) if m else (None, None)
        cues.append({"start_ms": start, "end_ms": end, "text": "\n".join(block[at + 1:]),
                     "line": block_start + at + 1})
    return cues


def _skip_block(lines, i):
    while i < len(lines) and lines[i].strip():
        i += 1
    return i


def visible(text):
    return [TAG.sub("", line).strip() for line in text.split("\n") if TAG.sub("", line).strip()]


def check(cues, **limits):
    o = {**DEFAULTS, **{k: v for k, v in limits.items() if v is not None}}
    out, prev_start, prev_end = [], None, None

    def add(code, cue, message):
        where = cue["line"] if cue.get("line") else None
        label = f"cue {cue['index']}: " if cue.get("index") and not where else ""
        out.append({"code": code, "severity": RULES[code][0], "line": where, "message": label + message})

    for cue in cues:
        start, end = cue.get("start_ms"), cue.get("end_ms")
        if type(start) is not int or type(end) is not int:
            add("SUB001", cue, "timing can't be read")
            continue
        lines = visible(cue.get("text", ""))
        if not lines:
            add("SUB004", cue, "cue has no text")
        if end <= start:
            add("SUB002", cue, f"ends at {end} ms, not after its start at {start} ms")
        if prev_start is not None and start < prev_start:
            add("SUB003", cue, f"starts at {start} ms, before the previous cue's {prev_start} ms")
        elif prev_end is not None and start < prev_end:
            add("SUB005", cue, f"starts {prev_end - start} ms before the previous cue ends")
        for line in lines:
            if len(line) > o["max_chars"]:
                add("SUB101", cue, f"line is {len(line)} characters (limit {o['max_chars']}): {line[:40]}…")
        if len(lines) > o["max_lines"]:
            add("SUB102", cue, f"{len(lines)} lines (limit {o['max_lines']})")
        duration = end - start
        if 0 < duration < o["min_ms"]:
            add("SUB103", cue, f"on screen {duration} ms (minimum {o['min_ms']})")
        if duration > o["max_ms"]:
            add("SUB104", cue, f"on screen {duration / 1000:.1f} s (maximum {o['max_ms'] / 1000:g} s)")
        chars = sum(len(line) for line in lines)
        if duration > 0 and chars / (duration / 1000) > o["max_cps"]:
            add("SUB105", cue, f"{chars / (duration / 1000):.1f} characters per second (limit {o['max_cps']:g})")
        prev_start, prev_end = start, max(end, prev_end or end)
    return out


def report(path, findings, as_json=False):
    if as_json:
        print(json.dumps([{"file": str(path), **f} for f in findings], ensure_ascii=False, indent=2))
    for f in [] if as_json else findings:
        print(f"{path}:{f['line'] or 1}: {f['code']} {f['message']}")
    return 1 if any(f["severity"] == "error" for f in findings) else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("track", type=Path)
    parser.add_argument("--format", choices=["srt", "vtt", "json"], help="default: from the file")
    parser.add_argument("--max-chars", type=int)
    parser.add_argument("--max-lines", type=int)
    parser.add_argument("--min-ms", type=int)
    parser.add_argument("--max-ms", type=int)
    parser.add_argument("--max-cps", type=float, help="20 adult, 17 children's (Netflix English)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        cues = parse(args.track.read_text(encoding="utf-8"), args.format)
    except (OSError, ValueError, AttributeError) as exc:
        parser.exit(2, f"{parser.prog}: {exc}\n")
    findings = check(cues, max_chars=args.max_chars, max_lines=args.max_lines, min_ms=args.min_ms,
                     max_ms=args.max_ms, max_cps=args.max_cps)
    sys.exit(report(args.track, findings, args.json))


if __name__ == "__main__":
    main()
