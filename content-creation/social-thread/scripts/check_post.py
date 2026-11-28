#!/usr/bin/env python3
"""Check a caption or a thread against a platform's text limits, and a sponsored post for its disclosure.

Counts follow each platform's published rule where one exists, and are estimates otherwise: run
the platform's own composer before relying on a post that is within a few characters of a limit.
This file is shared by the social-captions and social-thread skills; keep both copies identical.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

READ = "read 2026-11-28"
PLATFORMS = {
    "instagram": (2200, f"Meta IG User Media reference, caption field ({READ})"),
    "threads": (500, f"Meta Threads API overview, limitations ({READ})"),
    "bluesky": (300, f"Bluesky app.bsky.feed.post lexicon, maxGraphemes ({READ})"),
    "x": (280, f"X developer docs, Counting characters, and twitter-text config v3 ({READ})"),
}
FTC = f"FTC, Disclosures 101 for Social Media Influencers ({READ})"
RULES = {
    "CAP201": ("error", "over-limit", "Text longer than the platform allows. Instagram counts characters, Threads counts "
               "emoji as their UTF-8 bytes, Bluesky counts graphemes, X weighs CJK and emoji as 2 and every URL as 23. "
               "Sources: " + "; ".join(src for _, src in PLATFORMS.values()) + "."),
    "CAP202": ("warning", "hashtags-app", f"More than 5 hashtags. Instagram's Help Center says up to 5 tags on a post "
               f"(since December 2025); with more, the post or comment won't go out ({READ}, as quoted by several "
               f"schedulers; the page renders client-side)."),
    "CAP203": ("error", "hashtags-api", f"More than 30 hashtags, the ceiling in Meta's IG User Media reference ({READ})."),
    "CAP204": ("error", "mentions-api", f"More than 20 @ tags, the ceiling in Meta's IG User Media reference ({READ})."),
    "CAP205": ("error", "over-bytes", f"Bluesky text over 3,000 UTF-8 bytes, the lexicon's maxLength ({READ})."),
    "THR301": ("error", "empty-post", "A post in a thread with no text."),
    "DIS601": ("error", "no-disclosure", f"A sponsored post with no disclosure. Terms such as \"ad\", \"advertisement\" "
               f"and \"sponsored\", or a plain sentence naming the brand and what you got, are what the FTC accepts. "
               f"Source: {FTC}. Also recognised: iklan, ditaja, tajaan, 广告, 赞助."),
    "DIS602": ("warning", "disclosure-late", f"The disclosure is not in the first line (or the first post of a thread), "
               f"so readers who don't tap \"more\" miss it. Source: {FTC}."),
    "DIS603": ("warning", "disclosure-in-hashtags", f"The disclosure is mixed into a group of hashtags, where the FTC says "
               f"it is likely to be missed. Source: {FTC}."),
}

URL = re.compile(r"(?i)\b(?:https?://|www\.)[^\s<>()]+")
HASHTAG = re.compile(r"(?<![\w#&])#\w+")
MENTION = re.compile(r"(?<![\w@])@[\w.]+")
DISCLOSURE = re.compile(r"(?i)(?<![\w])#?(?:ad|advert(?:isement)?|sponsored|paid partnership|iklan|ditaja|tajaan)"
                        r"(?![\w])|广告|赞助")
X_LIGHT = ((0, 4351), (8192, 8205), (8208, 8223), (8242, 8247))


def _emoji(cp):
    return (0x1F000 <= cp <= 0x1FAFF or 0x2600 <= cp <= 0x27BF or 0x2300 <= cp <= 0x23FF
            or 0x2B00 <= cp <= 0x2BFF or cp in (0x00A9, 0x00AE, 0x203C, 0x2049, 0x2122, 0x2139, 0x3030, 0x303D))


def _joins(cp):
    """Code points that attach to the one before: combining marks, ZWJ, variation selectors, skin tones, tags."""
    return (cp == 0x200D or 0xFE00 <= cp <= 0xFE0F or 0x1F3FB <= cp <= 0x1F3FF or 0xE0020 <= cp <= 0xE007F
            or cp == 0x20E3 or unicodedata.category(chr(cp)) in ("Mn", "Me"))


def clusters(text):
    """Approximate grapheme clusters: enough for emoji sequences, flags and combining accents."""
    out, prev_zwj = [], False
    for ch in unicodedata.normalize("NFC", text):
        cp = ord(ch)
        flag = 0x1F1E6 <= cp <= 0x1F1FF and out and len(out[-1]) == 1 and 0x1F1E6 <= ord(out[-1]) <= 0x1F1FF
        if out and (_joins(cp) or prev_zwj or flag):
            out[-1] += ch
        else:
            out.append(ch)
        prev_zwj = cp == 0x200D
    return out


def length(text, platform):
    text = unicodedata.normalize("NFC", text)
    if platform == "instagram":
        return len(text)
    if platform == "bluesky":
        return len(clusters(text))
    if platform == "threads":
        return sum(len(c.encode()) if any(_emoji(ord(ch)) for ch in c) else len(c) for c in clusters(text))
    total, rest = 0, URL.sub(lambda m: "\0", text)
    for c in clusters(rest):
        if c == "\0":
            total += 23
        elif any(_emoji(ord(ch)) for ch in c):
            total += 2
        else:
            total += sum(1 if any(a <= ord(ch) <= b for a, b in X_LIGHT) else 2 for ch in c)
    return total


def _line_of(text, offset):
    return text.count("\n", 0, offset) + 1


def check(text, platform, *, thread=False, sponsored=False, disclosures=(), limit=None):
    out = []
    add = lambda code, line, message: out.append({"code": code, "severity": RULES[code][0], "line": line,
                                                   "message": message})
    cap = limit or PLATFORMS[platform][0]
    posts, offset = [], 0
    for part in (re.split(r"(?m)^---[ \t]*$", text) if thread else [text]):
        posts.append((part, offset))
        offset += len(part) + 3
    if thread and len(posts) > 1 and not posts[-1][0].strip():
        posts.pop()  # a closing --- separates nothing
    for n, (post, start) in enumerate(posts, start=1):
        body, lead = post.strip("\n"), len(post) - len(post.lstrip("\n"))
        label = f"post {n}: " if thread else ""
        if thread and not body.strip():
            add("THR301", _line_of(text, start + min(lead, 1)), f"post {n} is empty")
            continue
        line = _line_of(text, start + lead)
        size = length(body, platform)
        if size > cap:
            add("CAP201", line, f"{label}{size} counted on {platform} (limit {cap})")
        if platform == "bluesky" and len(body.encode()) > 3000:
            add("CAP205", line, f"{label}{len(body.encode())} bytes (limit 3000)")
        if platform == "instagram":
            tags, mentions = len(HASHTAG.findall(body)), len(MENTION.findall(body))
            if tags > 30:
                add("CAP203", line, f"{label}{tags} hashtags (API limit 30)")
            elif tags > 5:
                add("CAP202", line, f"{label}{tags} hashtags (Instagram allows 5 on a post)")
            if mentions > 20:
                add("CAP204", line, f"{label}{mentions} @ tags (API limit 20)")
    if sponsored:
        _disclosure(text, posts, thread, disclosures, add)
    return out


def _disclosure(text, posts, thread, extra, add):
    pattern = re.compile("|".join([DISCLOSURE.pattern[4:], *map(re.escape, extra)]), re.I) if extra else DISCLOSURE
    # Links, handles and emails aren't read as words: "ad" in a URL or @sponsoredlamp discloses nothing.
    readable = re.sub(r"\S*@\S+|" + URL.pattern[4:], lambda m: " " * len(m.group(0)), text, flags=re.I)
    hits = list(pattern.finditer(readable))
    if not hits:
        add("DIS601", 1, "sponsored, but no disclosure (ad, sponsored, iklan, 广告…) found")
        return
    first = posts[0][0].lstrip("\n")
    head_end = len(posts[0][0]) - len(first) + len(first if thread else first.split("\n", 1)[0])
    if hits[0].start() >= head_end:
        where = "the first post" if thread else "the first line"
        add("DIS602", _line_of(text, hits[0].start()), f"disclosure \"{hits[0].group(0)}\" is not in {where}")
    lines = text.split("\n")
    if all(m.group(0).startswith("#") and len(HASHTAG.findall(lines[_line_of(text, m.start()) - 1])) >= 3
           for m in hits):
        line = _line_of(text, hits[0].start())
        add("DIS603", line, f"\"{hits[0].group(0)}\" sits among {len(HASHTAG.findall(lines[line - 1]))} hashtags")


def report(path, findings, as_json=False):
    if as_json:
        print(json.dumps([{"file": str(path), **f} for f in findings], ensure_ascii=False, indent=2))
    for f in [] if as_json else findings:
        print(f"{path}:{f['line'] or 1}: {f['code']} {f['message']}")
    return 1 if any(f["severity"] == "error" for f in findings) else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("file", type=Path, help="the caption, or a thread with posts separated by a line of ---")
    parser.add_argument("--platform", choices=sorted(PLATFORMS), required=True)
    parser.add_argument("--thread", action="store_true", help="the file is a thread: posts split on --- lines")
    parser.add_argument("--sponsored", action="store_true", help="the post is paid or gifted: require a disclosure")
    parser.add_argument("--disclosure", action="append", default=[],
                        help="an extra phrase that counts as the disclosure, e.g. 'Thanks to Acme for the free kit'")
    parser.add_argument("--limit", type=int, help="override the platform limit")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        text = args.file.read_text(encoding="utf-8-sig")
    except OSError as exc:
        parser.exit(2, f"{parser.prog}: {exc}\n")
    findings = check(text, args.platform, thread=args.thread, sponsored=args.sponsored,
                     disclosures=args.disclosure, limit=args.limit)
    sys.exit(report(args.file, findings, args.json))


if __name__ == "__main__":
    main()
