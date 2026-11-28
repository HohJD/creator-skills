#!/usr/bin/env python3
"""creator-lint: offline checks for creator content, with rule codes.

    python3 tools/creator_lint.py subtitles talk.srt
    python3 tools/creator_lint.py post caption.txt --platform instagram --sponsored
    python3 tools/creator_lint.py post thread.txt --platform x --thread
    python3 tools/creator_lint.py alt cards.txt --platform instagram
    python3 tools/creator_lint.py localize post.en.txt post.ms.txt post.zh.txt
    python3 tools/creator_lint.py --list-rules
    python3 tools/creator_lint.py --explain SUB105

Each check lives in the skill that uses it (scripts/ beside its SKILL.md), so an agent with only
that skill installed can run it; this file runs them all from a checkout. Exit codes: 0 no
errors, 1 errors (or any finding with --strict), 2 usage or file error.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = {
    "subtitles": "subtitle-editor/scripts/lint_captions.py",
    "post": "social-captions/scripts/check_post.py",
    "alt": "image-descriptions/scripts/check_alt.py",
    "localize": "content-localization/scripts/compare_versions.py",
}


def module(name: str):
    path = ROOT / "content-creation" / CHECKS[name]
    spec = importlib.util.spec_from_file_location(f"creator_lint_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rules() -> dict[str, tuple[str, str, str, str]]:
    """code -> (severity, name, explanation, command)."""
    return {code: (*rule, name) for name in CHECKS for code, rule in module(name).RULES.items()}


def selected(code: str, select: list[str], ignore: list[str]) -> bool:
    keep = not select or any(code.startswith(s) for s in select)
    return keep and not any(code.startswith(i) for i in ignore)


def run(args) -> list[dict]:
    mod = module(args.command)
    if args.command == "subtitles":
        text = args.file.read_text(encoding="utf-8")
        return [{"file": str(args.file), **f} for f in mod.check(mod.parse(text, args.format), max_cps=args.max_cps,
                                                                    max_chars=args.max_chars)]
    if args.command == "post":
        found = mod.check(args.file.read_text(encoding="utf-8-sig"), args.platform, thread=args.thread,
                          sponsored=args.sponsored, disclosures=args.disclosure)
        return [{"file": str(args.file), **f} for f in found]
    if args.command == "alt":
        found = mod.check(mod.load(args.file.read_text(encoding="utf-8")), args.platform, args.max_chars)
        return [{"file": str(args.file), **f} for f in found]
    source = args.source.read_text(encoding="utf-8-sig")
    return [{"file": str(p), **f} for p in args.versions
            for f in mod.compare(source, p.read_text(encoding="utf-8-sig"), p.name)]


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="creator-lint", description=__doc__.split("\n\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog="\n".join(__doc__.split("\n\n")[1:]))
    p.add_argument("--list-rules", action="store_true", help="print every rule and exit")
    p.add_argument("--explain", metavar="CODE", help="print one rule's explanation and source, then exit")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--select", default="", help="only these codes or prefixes, comma-separated (SUB,DIS601)")
    common.add_argument("--ignore", default="", help="skip these codes or prefixes")
    common.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    common.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="command")
    s = sub.add_parser("subtitles", parents=[common], help="an SRT, WebVTT or cue-JSON track")
    s.add_argument("file", type=Path)
    s.add_argument("--format", choices=["srt", "vtt", "json"])
    s.add_argument("--max-cps", type=float, help="reading speed limit (20 adult, 17 children's)")
    s.add_argument("--max-chars", type=int, help="characters per line (42)")
    s = sub.add_parser("post", parents=[common], help="a caption, a thread, or a sponsored post")
    s.add_argument("file", type=Path)
    s.add_argument("--platform", choices=["bluesky", "instagram", "threads", "x"], required=True)
    s.add_argument("--thread", action="store_true", help="posts separated by lines of ---")
    s.add_argument("--sponsored", action="store_true", help="require a disclosure")
    s.add_argument("--disclosure", action="append", default=[], help="an extra phrase that counts as disclosure")
    s = sub.add_parser("alt", parents=[common], help="image descriptions, separated by blank lines, or JSON")
    s.add_argument("file", type=Path)
    s.add_argument("--platform", choices=["instagram", "x"])
    s.add_argument("--max-chars", type=int, default=250)
    s = sub.add_parser("localize", parents=[common], help="a source text and its translations")
    s.add_argument("source", type=Path)
    s.add_argument("versions", type=Path, nargs="+")
    return p


def main(argv: list[str] | None = None) -> int:
    p = parser()
    args = p.parse_args(argv)
    table = rules()
    if args.list_rules:
        for code, (severity, name, _, command) in sorted(table.items()):
            print(f"{code}  {severity:<7}  {command:<9}  {name}")
        return 0
    if args.explain:
        rule = table.get(args.explain.upper())
        if rule is None:
            print(f"creator-lint: no rule {args.explain!r}; see --list-rules", file=sys.stderr)
            return 2
        severity, name, explanation, command = rule
        print(f"{args.explain.upper()} {name} ({severity}, `creator-lint {command}`)\n\n{explanation}")
        return 0
    if not args.command:
        p.print_help()
        return 2
    try:
        findings = run(args)
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        print(f"creator-lint: {exc}", file=sys.stderr)
        return 2
    split = lambda s: [x.strip().upper() for x in s.split(",") if x.strip()]
    findings = [f for f in findings if selected(f["code"], split(args.select), split(args.ignore))]
    if args.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
    else:
        for f in findings:
            print(f"{f['file']}:{f['line'] or 1}: {f['code']} {f['message']}")
        errors = sum(f["severity"] == "error" for f in findings)
        if findings:
            print(f"\n{len(findings)} finding{'s' * (len(findings) != 1)} ({errors} error{'s' * (errors != 1)}).")
    failing = findings if args.strict else [f for f in findings if f["severity"] == "error"]
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
