# Codex and Claude Code compatibility

Checked on macOS on 22 November 2026 with Codex CLI 0.167.0 and Claude Code 2.1.328. This report covers local Codex and Claude Code skills.

| Check | Codex | Claude Code |
| --- | --- | --- |
| Native discovery in a clean project after one forced update | All 30 reported enabled at the project paths by the app server’s skills/list method. One project entry per skill. | All 30 appeared in both the CLI initialization list of skills and its slash-command list. |
| Explicit invocation | `$social-captions` read the project skill and returned the requested one-line caption. | `/social-captions` returned the same one-line caption. |
| CarouselCraft reference lookup | Installed file matched the source. A second live CLI call hit the account usage limit before answering. | `/carouselcraft` returned the correct heading and opening sentence for format 6 from the installed reference. |
| Project and personal installation layouts | All package files matched source in both layouts. | All package files matched source in both layouts. |
| Bundled Python tools | Subtitle export and campaign URL generation ran from the consumer project in both layouts. | The same two tools ran from the consumer project in both layouts. |
| Checkers (28 November 2026) | The five checkers (subtitle lint, post check in both caption and thread skills, alt text, localization) ran from installed copies in both layouts. | Same, in both layouts. |

The native trials used temporary project installations. The user-scope packaging tests use temporary home directories. These checks establish discovery, portability and representative execution. They do not score the editorial quality of 30 separate model outputs on each host.

Run the repeatable packaging and upgrade checks with `python3 -m unittest discover -s tests -p test_host_installations.py -v`. They cover paths with spaces and verify that a forced reinstall preserves local edits in a backup outside the discovery directory. Backups made with an older installer may already be under the skills directory; move those backups outside it if duplicate entries appear.

See the [Codex skills guide](https://developers.openai.com/codex/skills/) and [Claude Code skills guide](https://code.claude.com/docs/en/skills) for host-specific locations and invocation.

## Plugin and skills CLI (28 November 2026)

| Route | Check | Result |
| --- | --- | --- |
| Claude Code plugin, Claude Code 2.1.331 | `claude plugin validate .` | Passed. The repository root is both the marketplace (`ai-talentlabs`) and the plugin (`creator-skills`), with skills read from `content-creation/`. |
| | `claude plugin marketplace add` and `claude plugin install creator-skills@ai-talentlabs` in an empty home directory | Installed; `claude plugin details creator-skills` listed all 30 skills, and `check_post.py` ran from the plugin cache. Skills are called as `/creator-skills:<name>`. |
| skills CLI 1.9.0 (`npx skills`) | `add <repo> --list`, then `--skill social-captions --agent claude-code codex` in an empty project | Listed all 30 skills with their descriptions; installed `social-captions` with its `references/` and `scripts/` into `.agents/skills/`. |

The plugin route installs every skill; the skills CLI and `tools/install.py` can install one.
