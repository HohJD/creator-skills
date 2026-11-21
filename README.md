# CreatorSkills

[![CI](https://github.com/HohJD/creator-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/HohJD/creator-skills/actions/workflows/ci.yml)

**ScriptCraft** helps you turn a screen recording, rough take or sponsor brief into a video tutorial you can record. Give it the words you already have and tell it what's on screen. You can ask for a light edit, a full script with shots, or a second pair of eyes on a claim before you publish.

Here's a line from the sample Python tutorial. The viewer has just run a file that prints a greeting.

> See where it says “Hello, tutorial”? Let's put your name there. In the line that starts with “return”, change “tutorial” to “Sam”. Leave the quotes.

[Run the demo and see the rough take, finished voiceover and shots.](examples/python-hello/README.md)

## Install ScriptCraft

You'll need Python 3.10 or newer. Clone the repository, then pick the command for the agent you use.

```bash
git clone https://github.com/HohJD/creator-skills.git
cd creator-skills
```

| Agent | Install for your account | Install in one project (replace the path) |
| --- | --- | --- |
| Claude Code | `python3 tools/install.py --agent claude --scope user` | `python3 tools/install.py --agent claude --scope project --target /path/to/project` |
| Codex | `python3 tools/install.py --agent codex --scope user` | `python3 tools/install.py --agent codex --scope project --target /path/to/project` |

The installer copies [the skill folder](content-creation/scriptcraft/) into `.claude/skills/` or `.agents/skills/` under your home or project directory. If you're updating an existing installation, add `--force` to back up the old copy before replacing it.

## Try it on your own footage

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
