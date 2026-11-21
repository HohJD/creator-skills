# Evidence base and boundaries

This repository operationalizes **learning principles** and **editable editorial heuristics**. There is **no scientific guarantee of viral performance**, and causality from educational research to commercial Reels should not be exaggerated.

| Research or standard | Supported takeaway | Evidence type / limitation |
|---|---|---|
| [Agent Skills specification](https://agentskills.io/specification) | `SKILL.md`, concise `name`/`description`, progressive disclosure | Open format specification |
| [Claude Code skills](https://code.claude.com/docs/en/skills) | project `.claude/skills/`, reference files, invocation | Vendor docs; can change |
| [OpenAI skill guidance](https://developers.openai.com/plugins/build/skills) | focused skills, references, scripts only when needed | Vendor docs; can change |
| [Codex skills locations](https://developers.openai.com/api/reference/cli) | project `.agents/skills/`, user `~/.agents/skills/` | Vendor docs; verify on update |
| [Diátaxis tutorial principles](https://diataxis.fr/tutorials/) | learning journeys with results early and in steps | Normative framework |
| [Google Codelabs](https://developers.google.com/codelabs) | learn by guided hands-on builds | Public design practice |
| [Cognitive load review](https://pmc.ncbi.nlm.nih.gov/articles/PMC7940870/) | signalling, reducing irrelevant load, segmenting instruction | Review article, education contexts |
| [Worked examples / cognitive architecture](https://doi.org/10.1007/s10648-019-09465-5) | novice guidance, step-wise progression, expertise differences | Research synthesis; audience-specific |
| [Effective educational videos](https://pmc.ncbi.nlm.nih.gov/articles/PMC5132380/) | conversational narration; learning aligned visuals; segmentation | Educational-video review |
| [Guo, Kim & Rubin MOOC engagement](https://juhokim.com/files/LAS2014-Engagement.pdf) | production decisions affect observed video engagement | Large observational MOOC study, not a 6-min rule or virality guarantee |
| [Psychology of curiosity](https://doi.org/10.1037/0033-2909.116.1.75) | curiosity involves noticed information gaps | Theory; hook application is editorial extrapolation |
| [WCAG 2.2](https://www.w3.org/TR/wcag/) | accessible captions for prerecorded synchronized media | Accessibility standard; platform contexts vary |
| [YouTube retention guidance](https://support.google.com/youtube/answer/9314415?hl=en) | inspect moments of retention, spikes and dips carefully | Analytics documentation; retention != learning |

## Evidence-level rubric

- **A / authoritative:** product spec, actual recorded successful demo, or robust learning-science synthesis (with scoped claims).
- **B / empirical:** strong contextual study with transfer limitations.
- **C / design framework:** actionable practice with no universal causal guarantee.
- **D / editorial experiment:** project hypothesis, e.g. three candidate hooks, demo-first sequence, exact script cadence.

Do not call all project instructions "evidence based" without distinguishing evidence type. In particular, fixed beats like 0–3s hook, 35s demonstration, 3–7s CTA are **editorial defaults**, to be personalized and measured, not scientifically proven timing.

## Verification stance

Source citations and observed output are **different** claims. A docs page describing a feature is not direct evidence your account supports it. A command working locally is not proof it works across devices or versions. A brand brief's sales claim is not independent evidence. A retention bump is not a measure of learning. A script claiming a filmed demo existed is false when only a plan exists.

## Maintainer note

Recheck official Agent Skills / Claude Code / Codex docs before each release. Limit SKILL bodies and avoid heavy dependency graphs that create prompt bloat. See [OpenAI's 2026 skill guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) on keeping descriptions and injected context focused.
