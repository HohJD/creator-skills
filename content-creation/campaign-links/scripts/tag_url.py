#!/usr/bin/env python3
"""Build one public campaign URL offline, preserving unrelated query segments."""
import argparse
from urllib.parse import quote_plus, unquote_plus, urlsplit, urlunsplit

FIELDS = ("utm_source", "utm_medium", "utm_campaign", "utm_content")


def tag_url(url, *, source, medium, campaign, content=None):
    if any(ch.isspace() or ord(ch) < 32 for ch in url):
        raise ValueError("destination contains whitespace or control characters")
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname or parts.username is not None:
        raise ValueError("use an absolute public HTTP(S) URL without credentials")
    parts.port  # Validate any explicit port.
    values = dict(zip(FIELDS, (source, medium, campaign, content)))
    if content is None:
        del values["utm_content"]
    for key, value in values.items():
        if not isinstance(value, str) or not value.strip() or value.strip() != value:
            raise ValueError(f"{key} must have a nonempty value without outer whitespace")
    segments = parts.query.split("&") if parts.query else []
    seen = set()
    for segment in segments:
        raw_key, _, raw_value = segment.partition("=")
        key = unquote_plus(raw_key)
        lower = key.lower()
        if lower in {"signature", "sig", "x-amz-signature", "x-goog-signature"}:
            raise ValueError("use an unsigned destination for tagging")
        if lower not in FIELDS:
            continue
        if key != lower or key in seen:
            raise ValueError(f"ambiguous existing campaign field: {key}")
        seen.add(key)
        if key in values and unquote_plus(raw_value) != values[key]:
            raise ValueError(f"existing {key} conflicts with requested value")
    for key, value in values.items():
        if key not in seen:
            segments.append(f"{key}={quote_plus(value)}")
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "&".join(segments), parts.fragment))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    for name in ("source", "medium", "campaign"):
        parser.add_argument(f"--{name}", required=True)
    parser.add_argument("--content")
    args = parser.parse_args()
    try:
        print(tag_url(**vars(args)))
    except ValueError as exc:
        parser.exit(2, f"{parser.prog}: {exc}\n")


if __name__ == "__main__":
    main()
