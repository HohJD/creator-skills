# Changelog

## Unreleased

## 0.4.0 — 2026-11-28

- Added offline checkers to five skills, with rule codes, sources and dates: `lint_captions.py` (subtitle-editor: unreadable, empty, out-of-order and overlapping cues; Netflix English line, duration and reading-speed limits), `check_post.py` (social-captions and social-thread: Instagram, Threads, Bluesky and X limits counted as each platform publishes, Instagram hashtag and @ tag caps, sponsor disclosure present, early and outside the hashtags), `check_alt.py` (image-descriptions) and `compare_versions.py` (content-localization: numbers, months, links and handles across versions).
- Added `tools/creator_lint.py`, one CLI for all checkers with `--list-rules`, `--explain`, `--select`, `--ignore`, `--strict` and `--json`.
- Added a routing eval: 89 labelled requests in `evals/routing.json`, an offline completeness check in CI, and a model run with a names-only control. First run: 89/89 with descriptions and 89/89 with names only (Codex CLI 0.172.0).
- Installable as a Claude Code plugin (`/plugin install creator-skills --marketplace AI-Talentlabs/creator-skills`) and with the skills CLI (`npx skills add AI-Talentlabs/creator-skills`).
- Added issue and pull request templates, a weekly link check, Python 3.10 in CI, and README sections on checks, results and limits. Fixed the broken link to Guo, Kim and Rubin (2014).

## 0.3.0 — 2026-11-25

- Rewrote all 30 skill descriptions to state when each skill should fire and which sibling handles near-miss requests. Lint now requires a "Use when" clause, YAML-safe descriptions and valid sibling references.

- Sharpened ScriptCraft with a job picker, a default output shape, pacing rules for English and Mandarin, an invented edit example and a pre-handover check. Cleaned up the sponsor, bilingual, longform and rubric references.

- Verified all 30 skills with Codex CLI and Claude Code discovery. Documented both invocation forms, added four-scope install checks, and moved upgrade backups outside skill discovery.

- Added 13 skills for partner work, web and social publishing, production and distribution, with an offline UTM builder and an audience-to-Story worked example.

- Added 15 creator workflows spanning social copy, subtitles, accessibility, planning, production, localization, distribution and measurement. Added a standard-library SRT/WebVTT exporter, worked examples and behavioural trial notes.

- Added CarouselCraft with eight carousel formats, reusable prompts and a five-card worked example. Install one skill by name with `--skill`.

## 0.2.0 — 2026-11-21

- Renamed public repository to CreatorSkills and consolidated four overlapping tasks into one ScriptCraft skill.
- Maintained source and verification guidance, campaign checks, creator voice, bilingual and longform modes as internal workflows.
- Updated portable install paths, documentation and CI tests for a single skill.

## 0.1.0 — 2026-11-21

- Initial research prototype with script, research, verification and voice-profile workflow prototypes.
