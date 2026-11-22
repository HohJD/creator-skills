---
name: campaign-links
description: Build consistent UTM-tagged campaign URLs for newsletters, bios, posts and partner placements with a bundled offline tagger that keeps existing query values and anchors, plus a placement-to-tag map. Use when someone asks for UTM links, tracking links, campaign URLs or link tagging. Not for analysing the resulting clicks (creator-analytics) or shortening links through an external service.
license: Apache-2.0
---

# Campaign links and UTM handoff

Start with the approved destination, placement list, reporting scheme, source, medium and campaign name. Use distinct content labels when comparing creative variants. Respect existing case and account conventions. Never put personal details, emails or private identifiers into public tags. Do not tag internal navigation as if it were a new external acquisition source.

Keep the base path, unrelated query fields and any fragment. Treat signed or expiring links as unsuitable for editing until the owner supplies a taggable destination. If a submitted link already has different campaign values, report the conflict before replacing them. Give the user the final URLs and a readable placement-to-tag mapping. Distinguish an offline review from a tested redirect or verified analytics event.

For an ordinary absolute HTTP(S) URL, the bundled `scripts/tag_url.py` builds a link without contacting the destination. Resolve the script beside the installed SKILL.md and run `python3 "/path/to/campaign-links/scripts/tag_url.py" URL --source SOURCE --medium MEDIUM --campaign CAMPAIGN`; add `--content LABEL` for a variant. It preserves unrelated raw query segments and rejects duplicate or conflicting tags in the fields it manages. Quote the URL and values in a shell.

## Copyable brief

> Build campaign links to [approved URL] for [placements]. Use [existing source/medium naming scheme], campaign [name] and one content label per creative. Preserve existing query values and the page anchor.

## Worked example

**Fictional input.** A fictional newsletter uses https://example.org/guide?lang=en#tools, source studio, medium email and campaign repair-week.

**Newsletter:** `https://example.org/guide?lang=en&utm_source=studio&utm_medium=email&utm_campaign=repair-week#tools`

The language choice and tools anchor survive the edit. A test click through the real sending platform would be needed to verify its redirects and reporting.

## Source

Google Analytics documents campaign fields, URL tagging and consistent case-sensitive naming. This local helper never sends analytics. [Read the source](https://support.google.com/analytics/answer/10917952).
