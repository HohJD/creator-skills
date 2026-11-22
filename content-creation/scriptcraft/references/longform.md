# Longer developer build-along (2 to 20+ minutes)

## Goal is transfer, not watch time

A viewer should finish able to reproduce a small working result, understand the mechanism, modify it once, and debug one likely failure. Let prior knowledge determine guidance. Duration follows the smallest complete learning arc.

## Structure

1. **Outcome preview:** show actual finished program/feature or test output.
2. **Learning contract:** who this is for, prerequisites, what they will have.
3. **Minimal setup:** versions/OS/permissions only when needed; link to fuller docs.
4. **First working path:** show smallest successful end-to-end example with checkpoints.
5. **What changed and why:** one model or concept at a time after proof.
6. **One variation:** edit one parameter, rerun, observe difference.
7. **Failure + diagnosis:** reproduce a likely safe error, trace it, fix it.
8. **Verify:** test current version, compare observed results to promised.
9. **Transfer:** recap mental model and useful extension.

### Annotations for a production table

When the creator asks for a full production plan, give each substantial beat: Narration, Screen, Expected observation, User action, Claim/evidence ID, Failure if likely, Approximate time. For a script-only request, keep the voiceover clean and put only the exact commands, paths and labels in short shot notes. Keep every terminal command, path, feature flag and UI label exact. A user should never be forced to infer which tab/menu a narrator means.

## Multimedia cognition

Avoid unrelated background motion during explanation; point/zoom when referring to complex UI; chunk setup into checkpoints; explain code's purpose instead of reading it aloud; teach one fresh concept at a time when audience is novice. Provide a transcript and review captions manually.

## Reality checks

Do not imply an unrun command succeeded. Record environment version, demo stdout, source URLs and check date. If access is impossible, show a planned test scene with `[RECORD AFTER RUNNING]`. Exact syntax must be validated locally or against primary docs.
