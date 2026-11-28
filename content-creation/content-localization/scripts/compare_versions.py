#!/usr/bin/env python3
"""Compare a source text with its translations: the numbers, months, links, emails and handles must match.

Words are the translator's job; these tokens are not. Run it on EN, BM and 中文 versions of one
post, carousel or newsletter before publishing.
"""
import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

RULES = {
    "LOC501": ("error", "number-missing", "A number in the source (a price, date, count or percentage) that a version "
               "drops or changes. 2,500 and 2500 are the same number; full-width digits are read as digits."),
    "LOC502": ("warning", "number-added", "A number in a version that the source doesn't have: a converted price, a "
               "typo, or a detail the translator added."),
    "LOC503": ("error", "date-mismatch", "A month, or a day paired with its month, that differs between the source and "
               "a version: March vs April, 6 March vs 12 March, or a month only one of them names. March, Mac and 3月 "
               "are the same month."),
    "LOC504": ("error", "literal-changed", "A link, email address or @handle that a version drops or changes. These "
               "must be copied exactly, never translated."),
}
MONTHS = {}
for n, names in enumerate([
        "january jan januari 一月", "february feb februari 二月", "march mar mac 三月", "april apr 四月",
        "may mei 五月", "june jun 六月", "july jul julai 七月", "august aug ogos ogo 八月",
        "september sep sept 九月", "october oct okt oktober 十月", "november nov 十一月",
        "december dec dis disember 十二月"], start=1):
    for name in names.split():
        MONTHS[name] = n
# A link may touch Chinese text on either side, so it starts after any non-ASCII-word character and stops at CJK
# characters and punctuation (full-width punctuation is already ASCII after NFKC, and trailing marks are trimmed).
CJK = "\u3000-\u303f\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uff00-\uffef"
LITERAL = re.compile(rf"(?i)(?<![A-Za-z0-9])(?:https?://|www\.)[^\s<>()\"'{CJK}]+"
                     rf"|[A-Za-z0-9.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+|(?<![A-Za-z0-9@])@[A-Za-z0-9_.]+")
MONTH_WORD = re.compile(r"(?i)(?<![a-z])(" + "|".join(sorted((m for m in MONTHS if m.isascii()), key=len,
                                                              reverse=True)) + r")\.?(?![a-z])")
MONTH_ZH = re.compile(r"(\d{1,2})\s*月(?:\s*(\d{1,2})\s*[日号])?|(十一|十二|十|[一二三四五六七八九])月")
DAY_BEFORE = re.compile(r"(\d{1,2})(?:st|nd|rd|th|hb)?\s+$", re.I)
DAY_AFTER = re.compile(r"^\s+(\d{1,2})(?:st|nd|rd|th)?(?!\d|:)", re.I)
NUMBER = re.compile(r"\d+(?:[,\u2009\u202f ]\d{3})*(?:\.\d+)?")


def tokens(text):
    """Numbers, months and literals in `text`, each with the line it is on."""
    text = unicodedata.normalize("NFKC", text)
    found, taken = {"number": [], "month": [], "literal": []}, []

    def line(i):
        return text.count("\n", 0, i) + 1

    for m in LITERAL.finditer(text):
        found["literal"].append((m.group(0).rstrip(".,;:!?"), line(m.start())))
        taken.append((m.start(), m.end()))
    for m in MONTH_ZH.finditer(text):
        month = int(m.group(1)) if m.group(1) else MONTHS[m.group(3) + "月"]
        found["month"].append((f"{month}-{int(m.group(2))}" if m.group(2) else str(month), line(m.start())))
        taken.append((m.start(), m.end()))
    for m in MONTH_WORD.finditer(text):
        word = m.group(1).lower()
        if word in ("may", "mar", "dec") and m.group(1)[0].islower():
            continue  # "may" the verb, "mar" the verb; a month is written with a capital in EN and BM
        if any(s <= m.start() < e for s, e in taken):
            continue
        lead = max(0, m.start() - 8)
        before, after = DAY_BEFORE.search(text[lead:m.start()]), DAY_AFTER.match(text[m.end():])
        if before:
            taken.append((lead + before.start(1), lead + before.end(1)))
        elif after:
            taken.append((m.end() + after.start(1), m.end() + after.end(1)))
        day = before or after
        token = f"{MONTHS[word]}-{int(day.group(1))}" if day else str(MONTHS[word])
        found["month"].append((token, line(m.start())))
    for m in NUMBER.finditer(text):
        if any(s <= m.start() < e for s, e in taken):
            continue
        value = re.sub(r"[,\u2009\u202f ]", "", m.group(0))
        value = value.rstrip("0").rstrip(".") if "." in value else value.lstrip("0") or "0"
        found["number"].append((value, line(m.start())))
    return found


def compare(source, version, name="version"):
    a, b, out = tokens(source), tokens(version), []

    def add(code, ln, message):
        out.append({"code": code, "severity": RULES[code][0], "line": ln, "message": message})

    for kind, missing_code in (("number", "LOC501"), ("month", "LOC503"), ("literal", "LOC504")):
        want, have = Counter(v for v, _ in a[kind]), Counter(v for v, _ in b[kind])
        for value, count in (want - have).items():
            src_line = next(ln for v, ln in a[kind] if v == value)
            extra = f" ({count} of {want[value]} missing)" if want[value] > 1 else ""
            add(missing_code, None, f"{name} lacks {_shown(kind, value)} from source line {src_line}{extra}")
        if kind in ("number", "month"):
            for value in (have - want):
                add("LOC502" if kind == "number" else "LOC503", next(ln for v, ln in b[kind] if v == value),
                    f"{name} has {_shown(kind, value)}, which the source doesn't")
    return out


def _shown(kind, value):
    if kind != "month":
        return value
    month, _, day = value.partition("-")
    name = next(n for n, v in MONTHS.items() if v == int(month)).title()
    return f"{day} {name}" if day else name


def report(path, findings, as_json=False):
    if as_json:
        print(json.dumps([{"file": str(path), **f} for f in findings], ensure_ascii=False, indent=2))
    for f in [] if as_json else findings:
        print(f"{path}:{f['line'] or 1}: {f['code']} {f['message']}")
    return 1 if any(f["severity"] == "error" for f in findings) else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("source", type=Path)
    parser.add_argument("versions", type=Path, nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        source = args.source.read_text(encoding="utf-8-sig")
        versions = [(p, p.read_text(encoding="utf-8-sig")) for p in args.versions]
    except OSError as exc:
        parser.exit(2, f"{parser.prog}: {exc}\n")
    status = 0
    for path, text in versions:
        status |= report(path, compare(source, text, path.name), args.json)
    sys.exit(status)


if __name__ == "__main__":
    main()
