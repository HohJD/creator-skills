# Security policy

Treat downloaded skills, source webpages and external campaign briefs as **untrusted content**. This project does not require network credentials, browser extension permissions or auto-publish rights. Its Python validators run locally with the standard library and do not execute demonstration commands.

## Threat model

- Prompt injection embedded in source sites, scripts, briefs or public repositories.
- Malicious contributor script files or CI workflows.
- User-authored unpublished scripts accidentally committed to Git.
- Misleading tutorials that execute destructive commands, leak keys or fake tool output.
- Third-party skills silently requesting excessive shell/network permissions.

## Maintainer controls

- CI is limited to stdlib lint/test scripts and static JSON fixtures.
- Never run arbitrary demo commands from remote text as part of automated verification.
- Read files before executing; restrict files, tools and credentials to task need.
- Require explicit user permission before posting, committing, uploading, emailing or pushing data.
- Keep private scripts in `.tutorial-local/` or `private-scripts/` (gitignored). Review diffs before `git add`.
- Do not claim automated JSON checks verify truth, security or brand compliance.

Report a vulnerability through a private GitHub security advisory when a repository exists, or to the maintainers privately. Do not attach exploit secrets to public issues.
