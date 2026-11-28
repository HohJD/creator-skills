## What and why

<!-- The creator problem this solves. Link the issue: "Fixes #12". -->

## Checklist

- [ ] `python3 -m unittest discover -s tests -v`, `python3 tools/lint_package.py`, `python3 tools/run_evals.py` and `python3 tools/routing_eval.py --check` pass
- [ ] A new or changed skill has a request that should use it and one that shouldn't in `evals/routing.json`
- [ ] Limits, formats and platform rules cite a source with a date, or an observed local test
- [ ] Invented examples are labelled as invented
- [ ] No unpublished scripts, private briefs, personal data, tokens or third-party transcripts without consent
- [ ] `CHANGELOG.md` has a line under Unreleased
