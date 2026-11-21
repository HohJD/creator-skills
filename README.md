# CreatorSkills

[![CI](https://github.com/HohJD/creator-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/HohJD/creator-skills/actions/workflows/ci.yml)

Choose a skill for the piece you're making.

| Skill | What you get | Start here |
| --- | --- | --- |
| **CarouselCraft** | A swipe post with exact card copy and a visual prompt or crop direction for every slide. | [Eight formats and their prompts](content-creation/carouselcraft/references/format-prompts.md) · [Five-card Grok Bot example](examples/grok-bot-carousel/) |
| **ScriptCraft** | A recordable video script built from your rough take, footage or sponsor brief. | [Python voiceover and shot list](examples/python-hello/README.md) |

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

By default, the installer copies both skills into `.claude/skills/` or `.agents/skills/` under your home or project directory. If you're updating an existing installation, add `--force` to back up the old copy before replacing it.

To add just CarouselCraft to an existing Codex setup, run:

```bash
python3 tools/install.py --agent codex --scope user --skill carouselcraft
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
