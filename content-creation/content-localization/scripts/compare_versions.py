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
    "LOC503": ("error", "month-mismatch", "A month in the source that a version names differently (March vs Mac vs "
               "3月), or leaves out."),
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
LITERAL = re.compile(r"(?i)\b(?:https?://|www\.)[^\s<>()\"'，。]+|[\w.+-]+@[\w-]+\.[\w.-]+|(?<![\w@])@[\w.]+")
MONTH_WORD = re.compile(r"(?i)(?<![a-z])(" + "|".join(sorted((m for m in MONTHS if m.isascii()), key=len,
                                                              reverse=True)) + r")\.?(?![a-z])")
MONTH_ZH = re.compile(r"(\d{1,2})\s*月|(十一|十二|十|[一二三四五六七八九])月")
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
        found["month"].append((int(m.group(1)) if m.group(1) else MONTHS[m.group(2) + "月"], line(m.start())))
        taken.append((m.start(), m.end()))
    for m in MONTH_WORD.finditer(text):
        word = m.group(1).lower()
        if word in ("may", "mar", "dec") and m.group(1)[0].islower():
            continue  # "may" the verb, "mar" the verb; a month is written with a capital in EN and BM
        if any(s <= m.start() < e for s, e in taken):
            continue
        found["month"].append((MONTHS[word], line(m.start())))
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
            shown = value if kind != "month" else list(MONTHS)[[*MONTHS.values()].index(value)].title()
            extra = f" ({count} of {want[value]} missing)" if want[value] > 1 else ""
            add(missing_code, None, f"{name} lacks {shown!s} from source line {src_line}{extra}")
        if kind == "number":
            for value in (have - want):
                add("LOC502", next(ln for v, ln in b[kind] if v == value), f"{name} has {value}, which the source "
                    f"doesn't")
    return out


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
