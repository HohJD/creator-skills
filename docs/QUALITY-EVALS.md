# Evaluation protocol (not just subjective scoring)

We evaluate **routing** and **execution quality** separately. Running the supplied Python test suite does not evaluate either model's actual skill-invocation decisions; it validates package structure and deterministic requirements.

## Routing probes, manually in fresh Claude Code / Codex sessions

| Test | Target | Expected |
|---|---|---|
| "Make a 40-second Reel tutorial from this recorded AI demo" | scriptcraft | trigger |
| "Research whether the new discount is still active" | scriptcraft (research mode) | trigger |
| "Review this tutorial for fabricated UI labels" | scriptcraft (review mode) | trigger |
| "Learn my speaking style from these approved scripts" | scriptcraft (voice-profile mode) | trigger |
| "Fix my failing Python unit test" | none | no tutorial skill |
| "Polish this job application paragraph" | none | no tutorial skill |
| "Give me a playlist" | none | no tutorial skill |
| "Rewrite a video script but don't research anything" | scriptcraft | honor instruction, mark claims unverified |

Record test prompt, model/host/date, whether invocation happened, negative false positives, and cost/tokens if available. Calculate precision and recall. Cross-model claims require repeat runs with the same fixture and reviewer rubric.

## Output quality (blind comparison)

For 12 pre-registered prompts across real verified demos, compare: baseline prompt without skill vs installed skill, randomized order and blind human raters. Score truth, naturalness, hook credibility, step reproducibility, shot alignment, brief compliance, caption accessibility. Include one novice and one expert; Mandarin and English; one brand promotion with a false free claim; one request to pass generated game imagery as official; one untested UI.

No single numerical score establishes quality. Measure separate **critical hallucination rate**, **mandatory CTA compliance**, **read-aloud edit count**, **viewer task success** and **reviewer preference**. Publication blocker remains blocking even if total rubric >90.

## Reproduction

- Keep fixtures in Git with real version/scope and check date when technical.
- Never include credentials or protected scripts.
- Use fresh conversations to avoid skill-memory contamination.
- Retest after changing descriptions, SKILL.md, references or host versions.
- Log supported/not-supported rather than manufacturing results.

## Current harness

`python3 tools/run_evals.py` exercises JSON good/bad fixtures, missing claim references and the most basic red-flag validation. It **does not** call Claude or Codex, calculate model precision/recall, verify websites, or measure video retention. Add human review or a governed eval service when available.
