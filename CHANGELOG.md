# Changelog

## Unreleased

- Added four growth skills: Creator benchmark, Hook lab, Collab pitch and Rate card, with routing probes and prompts.

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
