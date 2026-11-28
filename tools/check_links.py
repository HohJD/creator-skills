#!/usr/bin/env python3
"""Fetch every external link in the skills and docs and report the ones that are gone.

Runs weekly in CI, never on pull requests, so the PR checks stay offline. It only reads status
codes; nothing fetched is parsed or run. A 403 or 429 from a site that blocks scripts is reported
as unverified, not broken: those pages open in a browser.
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = re.compile(r"https?://[^\s)\"'`<>\]]+")
PLACEHOLDER = re.compile(r"https?://(?:[\w-]+\.)?(?:example\.(?:com|org|net)|localhost|127\.0\.0\.1)\b|…|\[|\{")
BLOCKS_SCRIPTS = {"x.com", "help.x.com", "www.adobe.com", "helpx.adobe.com", "www.ap.org", "doi.org", "dl.acm.org",
                  "www.linkedin.com", "www.tiktok.com", "www.instagram.com", "help.instagram.com"}
AGENT = "Mozilla/5.0 (compatible; creator-skills-link-check; +https://github.com/AI-Talentlabs/creator-skills)"


def links(root: Path = ROOT) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for path in sorted([root / "README.md", *(root / "docs").glob("*.md"), *(root / "content-creation").rglob("*.md"),
                        *(root / "examples").rglob("*.md")]):
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for url in URL.findall(line):
                url = url.rstrip(".,;:")
                if not PLACEHOLDER.search(url):
                    found.setdefault(url, []).append(f"{path.relative_to(root)}:{n}")
    return found


def status(url: str) -> int | str:
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(url, method=method, headers={"User-Agent": AGENT})
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return response.status
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in (403, 404, 405, 501):
                continue  # some servers refuse HEAD but serve GET
            return exc.code
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            return type(exc).__name__
    return "unreachable"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--list", action="store_true", help="print the links without fetching them")
    args = parser.parse_args()
    found = links()
    if args.list:
        for url, where in found.items():
            print(url, where[0])
        return 0
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = dict(zip(found, pool.map(status, found)))
    broken = unverified = 0
    for url, code in sorted(results.items()):
        host = url.split("/")[2]
        if isinstance(code, int) and code < 400:
            continue
        if code in (401, 403, 429) or (host in BLOCKS_SCRIPTS and not (isinstance(code, int) and code in (404, 410))):
            unverified += 1
            print(f"UNVERIFIED {code} {url} ({found[url][0]})")
        else:
            broken += 1
            print(f"BROKEN {code} {url} ({', '.join(found[url])})")
    print(f"{len(found)} links: {len(found) - broken - unverified} ok, {unverified} unverified, {broken} broken.")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
