# Evaluation protocol (not just subjective scoring)

We evaluate **routing** and **execution quality** separately. Running the supplied Python test suite does not evaluate either model's actual skill-invocation decisions; it validates package structure and deterministic requirements.

The expanded [creator trials](CREATOR-TRIALS.md) and [routing probes](CREATOR-PROBES.md) cover the additional skills.

## Automated routing eval

`evals/routing.json` turns the probes below and in [CREATOR-PROBES](CREATOR-PROBES.md) into 89 labelled requests. `python3 tools/routing_eval.py --check` validates them in CI; `--run codex` gives a model every skill's name and description, asks it to route each request, and repeats the run with the descriptions hidden as a control. Results, with the host, model and date, are in `evals/routing-results.json` and the README. The run measures descriptions, not a host's live skill loading, so keep the manual probes below for release checks.

## Routing probes, manually in fresh Claude Code / Codex sessions

| Test | Target | Expected |
|---|---|---|
| "Make a five-card before-and-after post from these two briefs, with a visual prompt for each card." | carouselcraft | exact five-card sequence, grounded comparison and reproducible directions |
| "Give me four types of carousels with a writing prompt for each. No finished post yet." | carouselcraft | four distinct types with four usable prompts |
| "Fix the previous/next arrows in my React image carousel." | none | code task rather than social content |
| "Make a 40-second Reel tutorial from this recorded AI demo" | scriptcraft | trigger |
| "Check whether the discount I mention in this sponsored tutorial is still active" | scriptcraft (research mode) | trigger |
| "Review this tutorial for fabricated UI labels" | scriptcraft (review mode) | trigger |
| "Learn my speaking style from these approved scripts" | scriptcraft (voice-profile mode) | trigger |
| "Fix my failing Python unit test" | none | no tutorial skill |
| "Polish this job application paragraph" | none | no tutorial skill |
| "Give me a playlist" | none | no tutorial skill |
| "Rewrite a video script but don't research anything" | scriptcraft | honor instruction, mark claims unverified |

Record test prompt, model/host/date, whether invocation happened, negative false positives, and cost/tokens if available. Calculate precision and recall. Cross-model claims require repeat runs with the same fixture and reviewer rubric.

## Two briefs you can try

These invented briefs exercise problems the JSON checks can't catch. Give the model the brief and skill in a fresh conversation. Keep the notes below out of the prompt.

**Light edit**

> Tidy this into a ~20-second voiceover for a screen recording, just the words. My rough take: “I always lose the quiet bit. See that little spike? That’s the mug hitting the desk. I cut just before it. There. The pause is still there, the clunk is gone.” The footage shows the waveform, cursor, cut, and the before/after playback. Keep “the quiet bit”. No CTA.

Listen for the creator's own words and room for playback. Check whether the edit adds a cause for the mistake, a new editing step or a call to action.

**Sponsored demo**

> I'm cutting a 15s sponsored spot for a fictional app called Leaf. The recording shows me drag three photos onto a page, then shows a contact sheet. English voiceover, include the exact spoken line “Leaf sponsored this video.” Their brief also requires “free forever”, and their pricing page isn't available. I'd like to end on the finished sheet.

Check the disclosure word for word. The recording supports the contact-sheet result. The price needs evidence or a change to the sponsor brief. A draft that simply drops the required price claim still leaves the creator with an unresolved brief.

**What happened on 21 November 2026.** In separate, explicitly instructed Codex runs on the first brief, both the original skill (commit `53e9c65`) and the revision kept “the quiet bit”. The original added “when I cut this too early”, a plausible cause the creator hadn't supplied. The revision stayed with the described cut and ended on “The clunk is gone.” On the sponsor brief, one run with the revision kept the exact disclosure and asked for supporting terms or approval to omit the claim. These observations cover these particular runs. Human preference, recorded duration, automatic skill selection and audience retention remain unmeasured.

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

The [22 November discovery and trials](EXPANSION-2026-11-22.md) cover the next 13 skills and the campaign-link utility.
