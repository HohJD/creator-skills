# CreatorSkills

[![CI](https://github.com/HohJD/creator-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/HohJD/creator-skills/actions/workflows/ci.yml)

CreatorSkills is a library of 30 skills for creators who write, film, edit and publish with Codex or Claude Code. Bring the material you actually have: a rough take, two photos, a transcript, a sponsor brief or a small set of analytics.

### Which caption do you need?

| Where the words go | Skill | Try it |
| --- | --- | --- |
| Under the post | [Social captions](content-creation/social-captions/SKILL.md) | [Seven copyable caption prompts](content-creation/social-captions/references/caption-prompts.md) |
| In sync with the video | [Subtitle editor](content-creation/subtitle-editor/SKILL.md) | [Sample SRT, WebVTT and cue data](examples/creator-captions/) |
| In the image's accessible description | [Image descriptions](content-creation/image-descriptions/SKILL.md) | Describe the information the reader needs from a still, chart or swipe post. |

### Pick the job

| Stage | Skills |
| --- | --- |
| Research and plan | [Content planner](content-creation/content-planner/SKILL.md) · [Interview guide](content-creation/interview-guide/SKILL.md) · [Prepublication fact check](content-creation/creator-fact-check/SKILL.md) |
| Write and design | [ScriptCraft](content-creation/scriptcraft/SKILL.md) · [CarouselCraft](content-creation/carouselcraft/SKILL.md) · [Video title and thumbnail](content-creation/title-thumbnail/SKILL.md) |
| Film and edit | [Shot list and B-roll](content-creation/shoot-plan/SKILL.md) · [Clip selection](content-creation/clip-selects/SKILL.md) · [Subtitle editor](content-creation/subtitle-editor/SKILL.md) |
| Publish and adapt | [Social captions](content-creation/social-captions/SKILL.md) · [Image descriptions](content-creation/image-descriptions/SKILL.md) · [Creator newsletter](content-creation/newsletter-editor/SKILL.md) · [Podcast show notes](content-creation/podcast-notes/SKILL.md) · [Content repurposing](content-creation/content-repurpose/SKILL.md) · [Localization](content-creation/content-localization/SKILL.md) |
| After publication | [Community replies](content-creation/community-replies/SKILL.md) · [Creator analytics](content-creation/creator-analytics/SKILL.md) |

### More creator workflows

| Job | Skills |
| --- | --- |
| Get the assignment right | [Audience listening](content-creation/audience-listening/SKILL.md) · [Creator media kit](content-creation/creator-media-kit/SKILL.md) · [Sponsor and UGC brief](content-creation/campaign-brief/SKILL.md) |
| Publish in another format | [Search article](content-creation/search-article/SKILL.md) · [Content refresh](content-creation/content-refresh/SKILL.md) · [Vertical Stories](content-creation/vertical-stories/SKILL.md) · [Social thread](content-creation/social-thread/SKILL.md) |
| Direct the production | [Visual prompt packs](content-creation/visual-prompt-pack/SKILL.md) · [Storyboards](content-creation/storyboard-sequence/SKILL.md) · [Live rundown](content-creation/live-rundown/SKILL.md) |
| Prepare the handoff | [Audio description](content-creation/audio-description/SKILL.md) · [Asset credits](content-creation/asset-credits/SKILL.md) · [Campaign links and UTM builder](content-creation/campaign-links/SKILL.md) |

**Try three skills together:** [Turn reader comments into a three-frame Story and two trackable links](examples/audience-to-story/).

[Browse prompts and worked examples](docs/CREATOR-PROMPTS.md) · [Eight carousel formats](content-creation/carouselcraft/references/format-prompts.md) · [Five-card Grok Bot example](examples/grok-bot-carousel/) · [Earlier trials](docs/CREATOR-TRIALS.md) · [Latest discovery and trials](docs/EXPANSION-2026-11-22.md)

## Install

You'll need Python 3.10 or newer. Clone the repository, then pick the command for the agent you use.

```bash
git clone https://github.com/HohJD/creator-skills.git
cd creator-skills
```

| Agent | Install for your account | Install in one project (replace the path) |
| --- | --- | --- |
| Claude Code | `python3 tools/install.py --agent claude --scope user` | `python3 tools/install.py --agent claude --scope project --target /path/to/project` |
| Codex | `python3 tools/install.py --agent codex --scope user` | `python3 tools/install.py --agent codex --scope project --target /path/to/project` |

By default, the installer copies all skills into `.claude/skills/` or `.agents/skills/` under your home or project directory. If you're updating an existing installation, add `--force` to back up the old copy before replacing it.

To add just the social caption skill to an existing Codex setup, run:

```bash
python3 tools/install.py --agent codex --scope user --skill social-captions
```

## Make a carousel

Use `$carouselcraft` in Codex or `/carouselcraft` in Claude Code. For example:

> Turn these two versions of a sponsor brief into a five-slide before-and-after carousel for video editors. Show the date that moved, the two edits it affects and the exact prompt I can reuse. Give me the words and visual direction for each card.

The [prompt library](content-creation/carouselcraft/references/format-prompts.md) also covers tutorials, checklists, comparisons, troubleshooting, photo stories, teardowns and prompt packs.

## Write a video script

Attach the clip or paste your rough take and a few notes about what happens on screen. Use `$scriptcraft` in Codex or `/scriptcraft` in Claude Code. For example:

> Tidy this into a 30-second voiceover. Keep my opening line. There's a pause halfway through where you hear the before and after, so leave room for that. Just give me the words I'd say.

For a longer screencast, ask for chapters and the result viewers should see after each step. For Mandarin narration, specify the audience and whether you want English shot notes or subtitles. For sponsored work, supply the required wording and what you've actually tested. The [fictional sponsor example](examples/sponsored-fictional/README.md) shows how to plan a shoot when the product demo is still missing.

If you share your own scripts to build a voice profile, save the profile in the gitignored `.tutorial-local/` folder. Keep unpublished scripts and private briefs out of contributions.

## Development

The checks run with the Python standard library:

```bash
python3 -m unittest discover -s tests -v
python3 tools/lint_package.py
python3 tools/run_evals.py
python3 tools/validate_package.py fixtures/valid-package.json
```

These check the installer, skill files and structured script examples. For editorial quality, the [evaluation guide](docs/QUALITY-EVALS.md) covers read-aloud edits, accuracy and whether a viewer can follow the demo. The [source notes](docs/EVIDENCE.md) explain the research behind the guidance.

Contributions are welcome. See [how to contribute](CONTRIBUTING.md) and the [security policy](SECURITY.md). CreatorSkills is an independent project released under the [Apache License 2.0](LICENSE).
