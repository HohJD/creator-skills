#!/usr/bin/env python3
"""Check a set of image descriptions (alt text) for the mistakes a script can see, offline.

It can't tell whether a description says what the reader needs; that is the skill's job.
"""
import argparse
import json
import re
import sys
from pathlib import Path

READ = "read 2026-11-28"
W3C = f"W3C WAI Images Tutorial, Tips and Tricks ({READ})"
PLATFORMS = {
    "instagram": (1000, f"Meta IG User Media reference, alt_text field ({READ})"),
    "x": (1000, f"X Help Center, How to make images accessible, and X API v2 media metadata ({READ})"),
}
RULES = {
    "ALT401": ("error", "empty", "An image with no description that isn't marked decorative. Screen readers announce "
               "the image and nothing about it. Mark purely decorative images as decorative instead."),
    "ALT402": ("warning", "redundant-prefix", f"Starts with \"image of\", \"picture of\" or similar. Screen readers "
               f"already announce an image, so the words add nothing. Source: {W3C}."),
    "ALT403": ("error", "over-limit", "Longer than the platform accepts. Sources: "
               + "; ".join(src for _, src in PLATFORMS.values()) + "."),
    "ALT404": ("warning", "long", f"Longer than a short phrase or sentence (default 250 characters). The W3C suggests "
               f"a separate long description when more is needed, e.g. in the caption or post text. Source: {W3C}."),
    "ALT405": ("error", "file-name", "A file name (IMG_2041.jpg) instead of a description, usually filled in by a tool."),
    "ALT406": ("warning", "duplicate", "Two images in one set with the same description, so a listener can't tell "
               "carousel cards or gallery photos apart."),
}
PREFIX = re.compile(r"(?i)^\s*(?:an?\s+|the\s+)?(?:image|picture|photo|photograph|graphic|icon|pic|gambar|foto)"
                    r"\s+(?:of|showing|shows|depicting|daripada|yang menunjukkan)\b|^\s*(?:图片|照片)[:：]?")
FILE_NAME = re.compile(r"(?i)^[\w .()-]+\.(?:png|jpe?g|gif|webp|heic|svg|bmp|tiff?)$")


def load(text):
    """Items as dicts with alt, decorative and the 1-based line it starts on."""
    text = text.lstrip("\ufeff")
    if text.lstrip().startswith("["):
        items = []
        for i, item in enumerate(json.loads(text), start=1):
            item = {"alt": item} if isinstance(item, str) else dict(item)
            items.append({"alt": str(item.get("alt") or ""), "decorative": bool(item.get("decorative")),
                          "label": str(item.get("id") or f"image {i}"), "line": None})
        return items
    items, line = [], 1
    for block in re.split(r"\n[ \t]*\n", text):
        stripped = block.strip("\n")
        if stripped.strip():
            start = line + (len(block) - len(block.lstrip("\n")))
            items.append({"alt": " ".join(stripped.split()), "decorative": False,
                          "label": f"image {len(items) + 1}", "line": start})
        line += block.count("\n") + 2
    return items


def check(items, platform=None, max_chars=250):
    out, seen = [], {}
    for item in items:
        alt = item["alt"].strip()

        def add(code, message):
            out.append({"code": code, "severity": RULES[code][0], "line": item["line"],
                        "message": f"{item['label']}: {message}"})

        if item["decorative"]:
            continue
        if not alt:
            add("ALT401", "no description")
            continue
        if FILE_NAME.match(alt):
            add("ALT405", f"\"{alt}\" is a file name")
            continue
        if PREFIX.match(alt):
            add("ALT402", f"starts with \"{PREFIX.match(alt).group(0).strip()}\"")
        if platform and len(alt) > PLATFORMS[platform][0]:
            add("ALT403", f"{len(alt)} characters ({platform} accepts {PLATFORMS[platform][0]})")
        elif len(alt) > max_chars:
            add("ALT404", f"{len(alt)} characters; move detail into a long description")
        key = alt.casefold()
        if key in seen:
            add("ALT406", f"same description as {seen[key]}")
        else:
            seen[key] = item["label"]
    return out


def report(path, findings, as_json=False):
    if as_json:
        print(json.dumps([{"file": str(path), **f} for f in findings], ensure_ascii=False, indent=2))
    for f in [] if as_json else findings:
        print(f"{path}:{f['line'] or 1}: {f['code']} {f['message']}")
    return 1 if any(f["severity"] == "error" for f in findings) else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("file", type=Path, help="descriptions separated by blank lines, or a JSON list of strings "
                                                "or {\"id\", \"alt\", \"decorative\"} objects")
    parser.add_argument("--platform", choices=sorted(PLATFORMS))
    parser.add_argument("--max-chars", type=int, default=250, help="warn above this length (default 250)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        items = load(args.file.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(2, f"{parser.prog}: {exc}\n")
    sys.exit(report(args.file, check(items, args.platform, args.max_chars), args.json))


if __name__ == "__main__":
    main()
