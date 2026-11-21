# Contributing

We welcome clean skill edits, new language profiles and verified examples. Proposed changes should solve a demonstrated user problem rather than merely add a longer prompt.

1. Open an issue describing who benefits, what breaks today, and how the change can be evaluated.
2. Keep `SKILL.md` concise. Add long educational guidance only under `references/` and load it conditionally.
3. Add or update at least one positive and one negative regression fixture when changing routing/requirements.
4. Run `python3 -m unittest discover -s tests -v && python3 tools/lint_package.py && python3 tools/run_evals.py`.
5. Do not include proprietary or unpublished scripts, real private screenshots, sponsor contracts, tokens, personal data or copyrighted third-party transcripts without rights and consent.
6. All factual feature/CLI examples require source/version/date or an observed local test. Mark invented examples plainly.
7. No network-executing CI examples, curl-pipe-shell instructions, or skill-wide permissions without security review.
8. Keep user instructions higher priority than default style guidelines. Never sacrifice factual integrity for drama.

The maintainer will review content for author provenance, accessibility and accuracy, not just grammar. See `SECURITY.md` for risky submissions and `docs/QUALITY-EVALS.md` for testing scope.
