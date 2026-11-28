# Contributing

We welcome clean skill edits, new language profiles and verified examples. Proposed changes should solve a demonstrated user problem rather than merely add a longer prompt.

1. Open an issue describing who benefits, what breaks today, and how the change can be evaluated. The "Propose a skill or a skill change" template asks for exactly that; questions and early ideas go in Discussions.
2. Keep `SKILL.md` concise. Add long educational guidance only under `references/` and load it conditionally.
3. Add or update at least one positive and one negative regression fixture when changing routing/requirements. A new or renamed skill needs a `positive` and a `boundary` case in `evals/routing.json`; `python3 tools/routing_eval.py --check` fails without them.
4. Run `python3 -m unittest discover -s tests -v && python3 tools/lint_package.py && python3 tools/run_evals.py && python3 tools/routing_eval.py --check`. If you change descriptions, also run `python3 tools/routing_eval.py --run codex` and include the summary in the PR.
5. Do not include proprietary or unpublished scripts, real private screenshots, sponsor contracts, tokens, personal data or copyrighted third-party transcripts without rights and consent.
6. All factual feature/CLI examples require source/version/date or an observed local test. Mark invented examples plainly.
7. No network-executing CI examples, curl-pipe-shell instructions, or skill-wide permissions without security review.
8. Keep user instructions higher priority than default style guidelines. Never sacrifice factual integrity for drama.

## Checkers

A checker is a standard-library script in a skill's `scripts/` folder that the skill tells the agent to run. It must work from an installed copy of that skill alone, read files the user names and nothing else, and make no network calls. Give each rule a code in its skill's range (`SUB`, `CAP`, `THR`, `ALT`, `LOC`, `DIS`), a severity, and an explanation that cites the page and date a limit came from; `tools/creator_lint.py` picks new rules up automatically. Add a test in `tests/test_checkers.py` for every rule. `social-captions` and `social-thread` ship the same `check_post.py`; edit one and copy it to the other (a test checks they match).

The maintainer will review content for author provenance, accessibility and accuracy, not just grammar. See `SECURITY.md` for risky submissions and `docs/QUALITY-EVALS.md` for testing scope.
