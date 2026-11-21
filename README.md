# CreatorSkills

> A growing library of practical AI-agent skills for content creators. **Start with ScriptCraft:** create videos people want to watch and can actually learn from.

[![CI](https://github.com/HohJD/creator-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/HohJD/creator-skills/actions/workflows/ci.yml)

This is a portable, open-source [Agent Skills](https://agentskills.io/specification) repository for **Claude Code** and **OpenAI Codex**. More creative skills can be added later; today there is intentionally **one** production-oriented content-creation skill.

## Current skill

| Category | Skill | What it does |
| --- | --- | --- |
| `content-creation/` | **[ScriptCraft](content-creation/scriptcraft/SKILL.md)** (`scriptcraft`) | Researches, writes, rewrites, personalizes, storyboards and reviews accurate, watchable video tutorials. Covers Reels, TikTok, Shorts, XHS, longer YouTube screencasts, sponsored briefs and bilingual narration. |

**Not a generic prompt**: ScriptCraft can use official docs and reproducible demo evidence, generate honest filmable hooks, preserve a creator's proven speaking style, and perform a pre-publication factual and brief-compliance audit. The local validators catch structure problems and certain red flags; they do *not* prove that the generated script or a changing product feature is true.

## Repository layout

```text
creator-skills/
├── content-creation/
│   └── scriptcraft/
│       ├── SKILL.md              # the one installable skill
│       ├── references/           # deep guidance loaded as needed
│       └── assets/               # briefs, ledgers, production templates
├── docs/                        # research evidence, style, evaluation plans
├── examples/                    # fictional examples, not private campaigns
├── schemas/                     # structured script and claim contracts
├── fixtures/                    # regression tests
├── tools/                       # safe local installer / validators
├── tests/                       # unit tests
└── .github/workflows/           # CI
```

Future skills can live alongside `scriptcraft/` under `content-creation/`, or in other category folders after the installer is extended. The current installer searches under `content-creation/`.

## Install

Python 3.10+ recommended. Clone or download this repository and run from its root:

```bash
python3 tools/install.py --agent claude --scope project --target /path/to/project
python3 tools/install.py --agent codex --scope project --target /path/to/project
```

Or install to your account:

```bash
python3 tools/install.py --agent claude --scope user
python3 tools/install.py --agent codex --scope user
```

This copies the single `scriptcraft/` directory into `.claude/skills/scriptcraft` for Claude Code or `.agents/skills/scriptcraft` for Codex (project scope), or the corresponding home folders for user scope. Existing installs are protected; `--force` backs up before replacing. Restart or refresh your agent if needed. Copying installs local instructions only; it never executes demonstration commands or publishes content.

## Try it

Invoke `/scriptcraft` in Claude Code or `$scriptcraft` in Codex when explicit invocation is supported, or ask naturally:

```text
Use scriptcraft to write a 45-second Reel from my recorded AI demo.
Start with the actual output, then explain the 2-3 steps I used. Keep it
conversational, with a shot plan, a truthful hook, and one useful CTA.
Don't invent product behaviour, menu labels, free offers, or my results.
```

**Modes inside one skill:** `research` (verify changing tool features), `write` (script), `review` (truth/filming/campaign checks), `voice-profile` (derive an opt-in local style profile), `shortform`, `longform`, `sponsored`, and `mandarin`.

```text
Use scriptcraft to analyse these scripts I've approved and my rewrite notes.
Only learn repeated patterns from my own words. Save an abstract style guide
locally to .tutorial-local/voice-profile.md. Don't include private scripts in Git.
```

Sponsored and technical work should keep an evidence ledger (input, action, observed output, checked source/date) rather than treating creative copy as proof.

## Run the local checks

```bash
python3 -m unittest discover -s tests -v
python3 tools/lint_package.py
python3 tools/run_evals.py
python3 tools/validate_package.py fixtures/valid-package.json
```

No external Python packages are required. The automated cases verify packaging, installation, JSON consistency and basic problems. They do *not* test Claude/Codex skill triggering or measure video retention, writing quality or technical truth. See [evaluation protocol](docs/QUALITY-EVALS.md) for controlled model and human tests.

## Ethics, privacy, provenance

- Creator examples are invented or fully licensed; unpublished scripts and campaign briefs are not included.
- Personal script-analysis results must remain local in `.tutorial-local/`, which is gitignored.
- Claims like “free”, “just launched”, “fastest”, generated output, endorsements and sponsored CTAs need verification and appropriate disclosure.
- Keep the *creator's* style without pretending unobserved personal experiences happened.
- Avoid fake hooks, fabricated stats, untested menus, prompt-injection instructions and destructive demonstrations.

Research foundations and their limits are documented in [evidence](docs/EVIDENCE.md). This independent project is not affiliated with Anthropic or OpenAI.

## License and contributions

[Apache-2.0](LICENSE). Contributions welcomed under [CONTRIBUTING.md](CONTRIBUTING.md). Review [SECURITY.md](SECURITY.md) before contributing third-party scripts, links, commands or executable examples.
