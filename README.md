# CreatorSkills

**Open-source skills and tools for creators.**

By [AI Talent Labs](https://www.ai-talentlabs.com) · [Browse the skills](https://www.ai-talentlabs.com/library) · [Getting started](https://www.ai-talentlabs.com/getting-started) · [MCP & API](https://www.ai-talentlabs.com/agents)

[![CI](https://github.com/AI-Talentlabs/creator-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/AI-Talentlabs/creator-skills/actions/workflows/ci.yml)

CreatorSkills is a library of 30 skills for creators who write, film, edit and publish with Codex or Claude Code. Bring the material you actually have: a rough take, two photos, a transcript, a sponsor brief or a small set of analytics. Five of the skills ship offline checkers, so platform limits, subtitle timing and sponsor disclosures are counted, not guessed.

**Start here:** [ScriptCraft](content-creation/scriptcraft/SKILL.md) for what you say on camera, [CarouselCraft](content-creation/carouselcraft/SKILL.md) for swipe posts, [Social captions](content-creation/social-captions/SKILL.md) for the words under them.

[![A five-card carousel made with CarouselCraft](examples/grok-bot-carousel/preview.jpg)](examples/grok-bot-carousel/)

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

**Claude Code plugin** (Claude Code 2.1.275 or later), all 30 skills in one step:

```text
/plugin install creator-skills --marketplace AI-Talentlabs/creator-skills
```

Plugin skills are namespaced, so you call them as `/creator-skills:social-captions`. On older versions, run `/plugin marketplace add AI-Talentlabs/creator-skills`, then `/plugin install creator-skills@ai-talentlabs`.

**Any agent the [skills CLI](https://github.com/vercel-labs/skills) supports** (Codex, Claude Code, Cursor and others):

```bash
npx skills add AI-Talentlabs/creator-skills                          # pick skills and agents interactively
npx skills add AI-Talentlabs/creator-skills --skill social-captions  # one skill
```

**From a clone**, with the bundled installer. You'll need Python 3.10 or newer. Clone the repository, then pick the command for the agent you use.

```bash
git clone https://github.com/AI-Talentlabs/creator-skills.git
cd creator-skills
```

| Agent | Install for your account | Install in one project (replace the path) |
| --- | --- | --- |
| Claude Code | `python3 tools/install.py --agent claude --scope user` | `python3 tools/install.py --agent claude --scope project --target /path/to/project` |
| Codex | `python3 tools/install.py --agent codex --scope user` | `python3 tools/install.py --agent codex --scope project --target /path/to/project` |

Use `$skill-name` in Codex and `/skill-name` in Claude Code. The [prompt library](docs/CREATOR-PROMPTS.md) gives both commands for every skill. See the [cross-host compatibility report](docs/HOST-COMPATIBILITY.md) for versions, checks and results.

By default, the installer copies all skills into `.claude/skills/` or `.agents/skills/` under your home or project directory. If you're updating an existing installation, add `--force` to back up the old copy before replacing it. Backups live in `creator-skills-backups/` beside the host’s `skills/` directory, outside skill discovery.

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

## Check before you post

Five skills carry a small standard-library checker in their `scripts/` folder, and the agent runs it before handing work over. From a clone you can run all of them as one linter, with rule codes in the style of ruff:

```bash
python3 tools/creator_lint.py subtitles talk.vtt                                 # timing, line length, reading speed
python3 tools/creator_lint.py post caption.txt --platform instagram --sponsored  # length, hashtags, disclosure
python3 tools/creator_lint.py post thread.txt --platform x --thread              # each post against X's weighted 280
python3 tools/creator_lint.py alt cards.txt --platform instagram                 # empty, "image of", duplicates
python3 tools/creator_lint.py localize post.en.txt post.ms.txt post.zh.txt       # prices, dates, links match
python3 tools/creator_lint.py --list-rules
python3 tools/creator_lint.py --explain SUB105
```

```text
caption.txt:4: DIS602 disclosure "#ad" is not in the first line
caption.txt:4: DIS603 "#ad" sits among 4 hashtags
```

Every limit cites the page it came from and the date it was read (`--explain` prints it). Exit code 1 means an error, 0 means none (warnings print but pass unless you add `--strict`), and `--json` gives machine-readable output.

## Results

**Routing.** [`evals/routing.json`](evals/routing.json) holds 89 requests: 35 that should use a particular skill (at least one per skill), 30 nearby requests, one per skill, that should go to a named sibling or to no skill, and 24 hard requests worded so the skill names alone point the wrong way. [`tools/routing_eval.py`](tools/routing_eval.py) gives a model every skill's name and description and asks it to pick one skill or none per request.

| Requests | With descriptions | Names only (control) |
| --- | --- | --- |
| Should use the skill | 35/35 | 35/35 |
| Should go elsewhere | 30/30 | 30/30 |
| Hard (names mislead) | 24/24 | 24/24 |

Run on 28 November 2026 with Codex CLI 0.172.0 (gpt-6.1-sol, medium reasoning); every answer is in [`evals/routing-results.json`](evals/routing-results.json). The control matters as much as the score: with this model, the skill names alone route every request, so routing isn't where the library is weak. The eval stays as a guard. A new skill that overlaps an existing one shows up as a miss. It's a proxy for how hosts choose skills, not a recording of one.

**Checkers.** 26 unit tests cover each rule, including the counting examples X, Threads and Bluesky publish (`Hello, world! 👋` is 16 on X; a family emoji is 25 on Threads and 1 on Bluesky).

## Limits

- **The checkers count; they don't judge.** A caption within the limit can still be dull or wrong, and alt text without "image of" can still miss what the reader needs. Taste, accuracy and voice are the skills' job and yours.
- **Platform counts are as published, and platforms change them.** Instagram's composer doesn't say how it counts emoji, and its in-app hashtag limit (5) is lower than its API's (30). Within a few characters of a limit, check in the composer.
- **Subtitle defaults are Netflix's English rules.** Other languages, players and children's content need other limits; pass them as flags.
- **The disclosure check follows the FTC's guidance** and knows the words "ad", "sponsored", iklan, ditaja, 广告 and 赞助. It doesn't encode any country's law, and it can't tell whether a post is sponsored; you tell it with `--sponsored`.
- **The localization check compares digits, months, links and handles.** A discount written as 八折 instead of 20% off, or a number spelled out in words, is reported as a mismatch for a person to confirm.
- **No skill posts, schedules or sends anything.** They draft; you publish.

## Development

The checks run with the Python standard library:

```bash
python3 -m unittest discover -s tests -v
python3 tools/lint_package.py
python3 tools/run_evals.py
python3 tools/routing_eval.py --check
python3 tools/validate_package.py fixtures/valid-package.json
```

These check the installer, skill files, checkers, routing cases and structured script examples, offline. `python3 tools/routing_eval.py --run codex` reruns the routing eval with your Codex login, and `python3 tools/check_links.py` fetches every cited link (it also runs weekly in CI). For editorial quality, the [evaluation guide](docs/QUALITY-EVALS.md) covers read-aloud edits, accuracy and whether a viewer can follow the demo. The [source notes](docs/EVIDENCE.md) explain the research behind the guidance.

Contributions are welcome. See [how to contribute](CONTRIBUTING.md) and the [security policy](SECURITY.md). CreatorSkills is an independent project released under the [Apache License 2.0](LICENSE).
